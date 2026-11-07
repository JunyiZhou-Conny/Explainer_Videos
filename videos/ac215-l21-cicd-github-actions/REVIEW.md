# Review record: AC215 · Lecture 21 — CI/CD with GitHub Actions II: one push, six fresh machines

Follow-along of the Lecture 21 tutorial, *Automating Software Development: CI/CD with GitHub Actions II*, on
[dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd) `main` @ `b8458ff` (2025-11-13, "demo class
1"; the only branch, still the head of `main` on 2026-11-06, `assets/terminal/laptop/01-ls-remote.txt`): README **Part
5: GitHub Actions (Remote CI)** (README:277–365) step by step, then the README's **Part 6: Branch Protection**
(README:369–397) as extras. Parts 1–4 of the same README were Lecture 9 (`videos/ac215-l09-ci-testing/`); this video
refers back to them and does not redo them. Claude Code sessions (Claude) produced it. Verified facts and unclaimed
reviews are kept in separate sections.

- **Origin:** issue #116. Built end to end on 2026-11-06/07 by this coordinator's agents: digest (every runnable claim
  run in disposable containers), live captures, brief, script + four independent reviews
  (`build/review_{accuracy,followalong,pedagogy,spoken}.md`, `build/review_merge_log.md`), `scenes/common.py`, 16 scenes
  each with a fresh critic, zh subtitles, `exercises.md`, `README.md`; the study guide (MLOps_Learning) follows after
  release. Build-complete commit `1daa74e` (2026-11-07 17:09 UTC; "SLIDES.md credits the course staff"). Usage-limit
  interruptions and container restarts were resumed from run ids; no work was lost (per the coordinator).
- **Captures:** 2026-11-06 (`ASSETS.md`; `terminal/laptop/00-env.txt`), in fresh disposable containers. The laptop
  stand-in is `docker:29.8.2-dind` (git 2.54.0, pre-commit 4.7.0, user `student`); a bare repository on it stands in for
  "your repository" on GitHub. Every README Part 5 command ran as printed, in README order. **All six `ci.yml` jobs ran
  locally, live, two ways:** each job on its own fresh stand-in runner with an empty Docker engine, executing the
  workflow's own `run:` scripts (`runner/run1`, `run2`, `run3`, `run-demo`, `noload`), and `act` 0.2.97 reading the same
  `ci.yml` (`laptop/62-act-push.txt`); both agree on every job result. `uses:` steps that need GitHub are replaced by
  recorded stand-ins (`-standin` files).
- **GitHub-hosted runs could not be captured** (the recording sandbox cannot push to GitHub; `ASSETS.md`, "Why there is no
  hosted GitHub Actions run"). The Actions tab, the run graph page, Settings → Secrets, Settings → Branches, a pull
  request and the Slack message are labelled `illustration`s built from `ci.yml` and the README, never presented as a
  hosted run; the narration says so at 11:11.3–11:33.0 (`.srt` cues 197–203: "…the GitHub pages you see are drawings built
  from the workflow file, marked illustration. Every log line in them is real.").
- **Real findings the video shows:** the unit-tests coverage step crashes (`PermissionError` on
  `coverage/style_*.css`, pytest exit 3; `runner/run1/unit-tests/05`), `continue-on-error` hides it and the upload finds
  no files (16:44.0–16:51.4, cues 293–296); in a clone, README Part 5's `git commit -m "Add CI pipeline"` says `nothing
  to commit, working tree clean` and no run starts (09:22.7, cue 168; `laptop/11`).
- **Slides:** `SLIDES.md` (35-page deck, credited to "the course staff") is redrawn, never shown. Slide 11's imagined
  Slack reply is never shown (`report-tags.md` tags 21 and 23: no author, no reply, no instructor name).
- **QA draft:** the 480p draft (28:20.85 per the QA output; `build/qa/draft.mp4` is now a dangling link to the deleted
  `output/ac215-l21-cicd-github-actions_480p15.mp4`, so it was not re-measured), subtitles in `build/qa/` dated 2026-11-07 17:31 UTC
  (commit `4f078f6`).
- **Whole-video QA:** run `wf_ccd4f7c9-594`, output `/root/ac215-backup/tasks/l21-qa-wppefzlic.output` (2026-11-07 19:06
  UTC), key `result`. 36 agents: seven watchers, 13 scene fixers, one narration/subtitle fixer and 15 scene verifiers.
  The run log reads "L21: 47 issues from 7/7 watchers". QA fixes committed in `8c2b886`, `09fffef` and `c3ec15b`
  (2026-11-07 18:25–19:09 UTC). The coordinator also fixed Black's `✨ 🍰 ✨` (S12), drawn as empty boxes: `common.emo_line`
  now draws them (`c3ec15b`). Lexicon PR #121 merged to `main` as `131f2c3` (Buildx, "under uses"; per the coordinator).
- **Finishing pass:** none. The coordinator's list of finishing-pass outputs for L21 is empty (`[]`).
- **1080p60 renders:** all 16 scenes, render logs written 2026-11-07 19:17–19:42 UTC (`build/logs/`); S09 and S13
  re-rendered after fix round 1 (logs 20:47 and 20:48). None of the 16 logs contains "anchor not found" (this record's
  writer grepped them).
- **Final cut:** 28:54.7 (1734.698 s); parts 12:36.3 + 16:18.4. File times (UTC, 2026-11-07): the clean cut and the
  full-cut subtitles 20:52; the burned copy, `chapters.txt` and `transcript.md` 21:09; part 1 21:10; part 2 21:11. The MP4s
  are not in Git (release assets).
- **Final-cut checks:** two rounds; the coordinator saved each check's returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md`, round 1 kept as `report-*-round1.md`. All five reports
  exist and were read in full for this record.
  - Round 1 ran on the first stitch (`7968be6`, 20:16 UTC): tags all 26 pass; ASR no real problem; visual one should
    (S13's `Oh no! 💥 💔 💥` as three grey boxes, 22:21); pairs: five places where one English sentence was repeated under
    2–3 zh fragments.
  - Fix round 1 (`c077bc5`, 20:42 UTC): 💥 and 💔 drawn in `common.emo_line`; S09 and S13 re-rendered; five zh lines and one
    `en_display` re-cut to the English clause stops; re-stitched and re-burned. Still 28:54 (part 1 12:36, part 2 16:18):
    the S09 and S13 renders kept their lengths (87.767 s, 140.747 s; `report-measured.md`).
  - Round 2 re-ran **visual, pairs and measured** on the files now in `output/`: all round-1 items verified, no
    regression, measured passes.
  - **The tags and ASR reports are round 1's** (`report-tags.md` and `report-asr.md` are byte-identical to their
    `-round1` copies), run on the pre-fix cut. The fix round changed no narration. This record's writer compared the
    current `.srt` with `asr.json`: 506 cues each, identical times; the one text difference is cue 232 (13:15.5), where
    the new `en_display` adds a comma ("…from the Dockerfile, and names it…"). The audio of the re-rendered S09 and S13
    was not transcribed again (the loudness of the whole cut was re-measured).

**Conventions:**
- **Times** are mm:ss in the full cut (`output/ac215-l21-cicd-github-actions.mp4`, 1734.698 s), except in "Whole-video QA",
  which keeps the 480p draft's times (marked *draft*).
- **Cue numbers** name their file: `.srt` (506 cues) or `.zh-en.srt` (515).
- **Evidence paths** are relative to `build/final-review/`. That folder is git-ignored and exists only in the producing
  session; a successor re-runs the checks to reproduce it.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a broken thing, not a value proposition: a run that is red while its summary says every test
   passed.
   - "You push the course's own code, untouched, to a repository of your own." (`.srt` cue 1, 00:00.0); "Soon after, one
     log says: unit tests, success." … "All tests passed." (cues 2–5, 00:04.9–00:12.7); "And the same file, run end to
     end, ends like this: job Lint and Format Check failed." (cues 6–7, 00:15.0–00:18.4); "Five machines green, one red,
     and the whole run red. The pipeline says every test passed, and the pipeline failed. Both are true." (cues 8–10);
     "So which machine said no, and why didn't the summary hear it?" (cue 11, 00:30.1).
   - **Payoff, on the viewer's own push:** part 1 ends on run 1's real verdict (S07, from 10:46.9); in S11, "And here is
     the hook, answered." (cue 330, 18:52.5) "Lint isn't in needs, so its failure never reaches the summary." (cue 331,
     18:54.6); the one-line fix (cue 336, 19:10.6).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. `BRIEF.md` ("Visual set pieces")
   defines eight, each animated next to the files and logs it explains:
   - **V1, the checks move from one laptop to the shared repository (`HookChain`, slides 2–7, 14–16):** S02's laptop chain
     (hygiene ×7 → Black → Flake8, no tests), a second laptop without `pre-commit install`, then the server door:
     "A pre-receive hook runs before the push is accepted," (cue 43, 02:22.0), "A post-receive hook runs after the code is
     in," (cue 46, 02:30.2), "GitHub.com doesn't run your own pre-receive scripts." (cue 49, 02:40.0). Reused in S13:
     `--no-verify` bypasses every laptop gate (cues 389–390, 22:04.7–22:09.7) and "CI caught what --no-verify let
     through" (cue 395, 22:26.4).
   - **V2, the CI loop and the course's pipeline (`CiLoop` + `PipelineStrip`, slides 21, 25–27):** drawn open in S03 (slide
     21 tag 03:49.4–04:03.0), the five-box strip from 04:04.4, then a thin strip under the tracker through part 2; the
     loop with ✓/✗ marks in S07 (12:07.1–12:12.2), closed by the fix commit in S12 (20:10.8–20:20.4), and twice in S16: with the
     "Deploy (CD) · lecture 23" box (27:33.8–27:40.6) and in the recap from "Once more, the loop." (cue 489, 27:58.2).
   - **V3, when the robot wakes up (`TriggerLanes`, slides 23–25):** branch lanes and sparks for `main`/`develop` pushes;
     "GitHub makes a temporary merge of your branch into main," (cue 112, 06:19.5); a GOLD runs meter; "It's the bell,
     not the gate: a red run doesn't undo the push." (cue 122, 06:52.8).
   - **V4, the YAML becomes a graph (`JobGraph`, slides 26–27):** S05's row of five stages becomes the job graph, "Now
     each needs line draws one arrow." (cues 133–138, 07:28.0–07:42.9), with the lint → summary arrow missing; S07's run
     graph coloured node by node (cue 195, 11:02.9); S11's three result tokens and the hook's answer (18:52.5).
   - **V5, build once, every job starts empty (`ImageSuitcase`, slides 27, 31):** S08: the Buildx slip (cue 234, 13:25.6),
     "docker save folds the image into one file, about 176 megabytes." (cue 238, 13:39.1), every check job's `docker load
     -i` (cue 244, 13:58.9); after ponder 3 the room without a load is turned away at Docker Hub, "pull access denied.
     Exit code 125" (cues 254–256, 14:38.9–14:43.8).
   - **V6, every step is a gate that reads an exit code (`ExitGates`, slides 22, 27):** S09, "Every command ends with an exit
     code." (cue 266, 15:19.9), Black's "Exit code 1, so the gate shuts." (cue 272, 15:35.5), Flake8 skipped; S10's coverage
     gate, "Exit code 3." shunted by `continue-on-error`, the `if: always()` upload with no files (cues 293–296,
     16:44.0–16:51.4); S13's run 3.
   - **V7, one runner, two containers, one port (`SystemTestRig`, slide 27):** S10, `curl -f` knocks on `localhost:9000`
     (cue 310, 17:38.6), the test container with `--network host` (cue 312, 17:49.0), two `if: always()` steps (cue 315,
     17:59.1), "the curl gate makes it fail loudly instead" (cue 319, 18:16.6).
   - **V8, who calls whom, and the bell that can't ring (`SlackRoute`, slides 7, 9–12):** S14, "A webhook is GitHub calling
     an outside address when something happens:" (cues 416–417, 23:54.8–23:58.1), Slack's incoming webhook (cue 422,
     24:12.3), the secret masked as `***` (cue 432, 24:50.6), the check step skipped in the demo run (cue 443, 25:23.0), the
     one-line fix `if: always()` (cue 446, 25:33.5).

   **Lecture slides:** a GREY "Lecture 21 · slide(s) …" tag top right, **26 tags** in the cut (`report-tags.md`): S01 1, S02
   4, S03 4, S04 3, S05 1, S07 1, S08 1, S09 1, S10 1, S11 1, S12 1, S13 2, S14 2, S15 1, S16 2; none in S06. Cited: slides
   1 + 4, 2–3, 5–6 (twice), 7, 7 + 9, 10–12, 11, 14–16, 16 + 26–27, 17, 18–20, 21 (three times), 22, 22 + 27, 23, 24, 25,
   25–27, 26–27, 27, 27 + 31, 29–31, 32–34. The deck is redrawn, never shown (`SLIDES.md`).
   - All 26 tags pass (round 1, four frames per tag, `tags/sheet_tagNN.png`, plus a 4 fps corner scan): each on screen only
     while its picture is up, "slide" for one and "slides" for several, no overlap, none outliving its scene. Three lead
     their picture by 0.6–1.6 s inside the same voice block (tags 9, 15, 22), as `script.md`'s convention allows.
   - Accepted: S13's "slides 29–31" tag stays through terminal-only beats (item A3).
3. **Pause-and-ponder moments and a recap**: ✔ for the ponders, by Conny's decision for the series (accepted item A1); ✔
   for the recap.
   - **Ponders:** five, each a card with the question spoken, then a silent linear 8.0 s timer; no narration overlaps any
     timer and the answer starts exactly when it ends (`measured.json` "scenes.ponders"; questions from `script.md` lines
     471, 639, 723, 891, 1022; answers from the `.srt`).

     | # | scene | question (from `script.md`) | asked | timer | answer starts |
     |---|---|---|---|---|---|
     | 1 | S04 | You push three commits to feature/login. How many CI runs start? Then you open a PR into main: how many now? | 05:50.8 (cue 103) | 06:00.9 | 06:08.9 "None for the three pushes: the branch filter." (cue 108) |
     | 2 | S07 | This run turns red, as in the opening. Is your push on main in your repository, or did the red run refuse it? | 11:33.2 (cue 204) | 11:43.7 | 11:51.7 "Yes, it's on main:" (cue 207) |
     | 3 | S08 | Delete the 'Load Docker image' step from unit-tests. Which step fails, and with what error? | 14:18.0 (cue 250) | 14:25.1 | 14:33.1 "The "Run unit tests" step." (cue 252) |
     | 4 | S11 | The demo commit computes sqrt(2·z) instead of sqrt(z). Which jobs turn red, and what does Test Summary say now? | 19:25.1 (cue 341) | 19:31.0 | 19:39.0 "Integration: red, 1 failed and 9 passed." (cue 343) |
     | 5 | S13 | A teammate commits a private key file with --no-verify and pushes to main. Which job of this pipeline catches it? | 23:17.9 (cue 409) | 23:25.9 | 23:33.9 "None. The detect-private-key hook is a local hook only." (cue 411) |

   - **Rate:** 5 cards in 28:54.7, about 0.35 per 2 minutes (one per 5.8 minutes, `report-measured.md`), against
     AGENTS.md's aim of one per 2 minutes (about 14 for this length). Part 1 has 2, part 2 has 3. The first timer starts
     at 06:00.9; the longest gap between two timers is 342.8 s (06:00.9 to 11:43.7); after the last timer ends (23:33.9)
     the video runs 320.8 s more.
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」: keep the current density, which that record gives as 3–5 ponders per lecture plus a
     spoken recap and test questions. L21's five ponders are inside that series density and below AGENTS.md's aim.
   - **Recap:** S16 "Non-determinism, CD next, and recap" from 27:18.4 (96.17 s).
     - 27:18.4–27:40.3: the lecture's machine-learning twist (non-determinism in every stage; version everything, automate
       retraining and testing, as Milestone 5 asks, monitor, roll out with care) and continuous deployment as Lecture 23
       (cues 476–481).
     - 27:40.3–27:58.2: the clean-up (switch to main, delete `feature/test-protection` here and on GitHub, remove the branch
       rule, the Slack secret and webhook, disable the workflow on a private repository, L09's Docker cleanup; cues
       482–488).
     - 27:58.2–28:12.3: "Once more, the loop." event, fresh machines and the artifact, exit-code gates, the summary's
       `needs` (cues 489–493).
     - 28:12.3–28:50.1: "Test yourself, pausing on each." (cue 494) and five questions (cues 495–505); "Answers are in the
       exercises and the study guide." (cue 506).
     - Part 1 (12:36) has no recap of its own; it ends on run 1's verdict and the parked question "In part 2 we open every
       log" (open nit).
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** commands and keys are spoken in words with the literal form in the subtitle's `en_display` (`git
     reset --hard HEAD~1` read "Git reset, hard, head tilde 1", `--all-files` "all files", `runs-on: ubuntu-latest` "runs
     on, ubuntu latest", the key `on` read "the key called on, just the word on", `M` read "the letter M, for modified");
     log lines quoted verbatim (`would reformat /app/api/utils.py`, `pull access denied`, `✅ All tests passed!`).
   - **Size:** 140 SAY blocks, 4,362 words (`measured.json`), 62 words (1.4 %) above the script's 3,900–4,300 target after
     the QA additions (accepted item A2). Kokoro `af_heart` at speed 0.9: 1,629.4 s of voice (93.9 % of the runtime),
     160.6 wpm over the voice and 150.9 wpm over the runtime.
   - **Anchors:** 649 `wait_until` anchors across the 16 scene files (S01–S16: 26, 36, 36, 32, 32, 48, 40, 44, 39, 59, 44,
     42, 52, 43, 37, 39; none in `common.py`). None of the 16 render logs contains "anchor not found".
   - **Pronunciation:** the QA ASR watcher found two real ear problems, both fixed and re-voiced: "The key named on lists
     the events" heard as "unlists"/"unless" (S03, now "Next comes the key called on, just the word on.", cue 85, 04:51.3) and "shows
     M twice" heard as "shows them twice" (S13, now "git status --short shows the letter M, for modified, twice.", cue 387, 21:55.9). The final ASR found
     no mispronunciation and no swallowed word (gate 6).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: a director and a simulated target viewer ("newcomer") per part, a subtitle
     watcher, a follow-ups watcher and an ASR watcher, from contact sheets, frames pulled from the draft, the scene code,
     the subtitle files, the README and the captures.
   - **47 timestamped findings: 2 must, 21 should, 24 nit.** Both musts were fixed, checked by independent verifiers, and
     are verified on the final cut by this record's writer (see "Verified"). What stayed open is listed under
     "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`measured.json`, round 2, measured on the final files).
   - **Duration:** 28:54.7 (1734.698 s), inside the series' 25–35 min. The parts are 12:36.3 (756.312 s) and 16:18.4
     (978.421 s); they sum to 0.035 s more than the full cut; part 1 ends on the S07/S08 boundary (756.20 s).
   - **Loudness:** −16.1 LUFS integrated in all four files; LRA 2.1 LU; true peak −2.7 dBTP (part 1: −2.8).
   - **Caption bounds** (`report-measured.md`, `report-visual.md`, `report-pairs.md`): every one of the 515 `.zh-en.srt`
     cues is exactly two lines, one per language; the burn file `.zh-en.ass` has `WrapStyle: 2` and exactly one `\N` per
     Dialogue line (515), so no cue wraps to a third line. Chinese 50 px over English 33 px. Measured with Noto Sans CJK,
     the widest rendered line is 1,506 px (the English line of `.zh-en.srt` cue 485; the widest Chinese line is cue 412's,
     1,504 px), against 1,840 px usable. Terminal and code
     panels end above y ≈ 900 and the subtitles start at y ≈ 985 (10 spot checks over commands, `frames-r2/subs_spot10.png`).
   - **Music balance:** does not apply. L21, like the other AC215 lectures, has no score: `video.yaml` has no `music:` key.
   - **Subtitle sync** (`report-asr.md`, onset check with base.en word timestamps over all 506 cues, doubtful ones
     re-timed with large-v3-turbo): median onset lag 0.15 s; no cue's audio starts more than 1 s after the cue. The one
     base.en flag (cue 331, 18:54.6, 1.23 s) is a recognition gap: large-v3-turbo has "lint" at 1134.12 s, 0.49 s before the
     cue.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip** (`report-asr.md`, round 1, on the pre-fix clean cut with the same narration; subtitles equal but for
   one comma, see the header):
   - faster-whisper `base.en` (2 threads) over the whole cut: 506 cues compared, 4,407 words recognised, 207 cues with some
     difference (`asr.json`, `asr-base.log`).
   - `large-v3-turbo` re-ran the doubtful windows on their own clips (`asr-large-clips.json`, `asr-large-clips2.json`).
     Every word base.en lost or changed is spoken: e.g. cue 17 (00:50), 45 (02:26), 161/164 (09:00–09:10), 314 (17:57),
     329–331 (18:50–18:58), 411–413 (23:33–23:41).
   - The rest is recogniser noise: numbers written out (about 45 cues), command names split or misheard (about 60: git →
     "get", Buildx → "build x", flake8 → "flake eight"), homophones (about 30), words counted across a cue boundary (about
     60) and punctuation read aloud in commands (about 15). No real problem. Four cosmetic subtitle/voice wording
     differences are open nits.

## Whole-video QA (480p draft, 28:20.85; times are *draft* times)

**Watchers and findings** (`l21-qa-wppefzlic.output`, key `result`):

| watcher | must | should | nit |
|---|---|---|---|
| director, part 1 | 0 | 3 | 4 |
| newcomer, part 1 | 0 | 4 | 3 |
| director, part 2 | 0 | 3 | 4 |
| newcomer, part 2 | 1 | 1 | 5 |
| subtitles | 1 | 8 | 8 |
| follow-ups | 0 | 0 | 0 |
| ASR | 0 | 2 | 0 |
| **total** | **2** | **21** | **24** |

- **By target:** 19 scene, 18 subtitles, 8 narration, 2 shared code.
- **By kind:** 17 subtitle, 7 text, 6 picture, 6 follow-along, 3 pacing, 3 narration, 2 fact, 2 lexicon, 1 continuity.
- **By scene:** S06 7, S13 6, S15 4, S02 3, S05 3, S07 3, S09 3, S11 3, S16 3, S01 2, S03 2, S08 2, S10 2, S14 2, S04 1,
  S12 1.
- **Facts:** the part-2 director checked exit 125 (no load), exit 3 (coverage), exit 1 (Black), 11/10/5 passed, the demo
  run's 1 failed/9 passed and 2 failed/3 passed against the captures; the part-1 newcomer checked the `needs` lines
  44/73/108/131/175, `retention-days 1`, the line-2 comment erratum, the seven hygiene hooks and Black/Flake8 at 120
  columns on `^src/`: all match. One fact should: S06's only chip sat beside the bug commit `c3b227f` while the narration
  said "the second undid a bug" (fixed: two chips, "undid it" on `b8458ff`, "planted it · → part 2" on `c3b227f`). No
  watcher found an instructor name, webhook URL, token or IP in the subtitles; the S14 Slack card shows no name.
- **Follow-ups watcher:** found no `QA_FOLLOWUPS.md` for L21 (none exists in the episode folder or in its history); the 16
  render logs hold only routine Manim warnings. No issues.
- **Subtitle watcher:** one D9 clause swap (S14, the must below), four bilingual pairing shifts, four `.zh.srt` line breaks
  inside a term or command (`远程 / Git hook`, `git remote / set-url origin`, `continue-on-error: / false`, `分别 / 向上取整`),
  `runs-on: / ubuntu-latest` split across cues, a GitHub label quoted short ("Require status checks to pass"), two zh
  sentences opening with a lower-case artifact, and the shared English line wrapper (open, below).
- **ASR watcher:** no lexicon problem ("Buildx" heard as "build X": the new entry works); two ear problems (S03 "on" →
  "unless", S13 "M" → "them"), both fixed.

**The musts, and how they were fixed:**
- **M1, S13 *draft* 22:09: the clean-up after `--no-verify` was wrong for a viewer who committed** (newcomer part 2).
  `git restore` resets `service.py` to the messy `quick fix` commit, which stays on local `main` pushed or not; the
  narration gave a fix only "if you pushed it too", so a viewer who committed but did not push would carry the bad commit
  into Part 6. **Fix:** the narration/subtitle fixer rewrote SAY[7] ("Here, git restore only throws away Black's fix in the
  working copy. If you followed along, the messy commit is on your main now, pushed or not. Not pushed yet? Git reset,
  hard, head tilde 1, drops it. Pushed? Run pre-commit run, all files, then add, commit and push, before part 6.") with
  matching zh and `en_display`, re-pointed three anchors, and changed "Push it." to "We push it." (agreeing with "you can
  just watch"); the S13 verifier found the picture still had one "pushed it too?" card and finished it in
  `s13_noverify.py` beat 7: two GREY cards and one "shown, not run" tag (under the "not pushed?" card), "not pushed?" with `git reset --hard HEAD~1` and
  "pushed?" with the red ✗ `main` mark and the four commands, each flashed on its words. **On the final cut:** cues
  405–408 (`.zh-en.srt`, 22:38.0–22:52.7) carry the new lines; at 22:52.0 both cards are on screen above the laptop
  terminal (`writer/must_s13_1372.0.png`).
- **M2, S14 *draft* 23:21: a D9 clause swap in the bilingual band** (subtitles). The zh put "when something happens" first,
  so cue 417 showed 所谓 webhook，就是在发生某件事时 under "A webhook is GitHub calling an outside address". **Fix:** the zh
  item in `i18n/zh/narration/g2.yaml` re-ordered as the watcher gave it. **On the final cut:** `.zh-en.srt` cue 423
  (23:54.8) pairs 所谓 webhook，就是 GitHub 去调用一个外部地址 with "A webhook is GitHub calling an outside address", and cue
  424 (23:58.1) 在发生某件事的时候：… with "when something happens: …"; the round-2 pairs check found no swap in any cue.

**The shoulds, examples by kind** (fixed and verified, except those under "Still open"):
- **Follow-along:** S06's fork route now gets run 1 (SAY[8] adds `git commit --allow-empty -m "Trigger CI"` then `git push`;
  the S06 verifier added the GREY "not in README · shown, not run" code card and a `▶ your turn` tag; on the final cut at
  10:41.0, `writer/s06_empty_commit_641.0.png`); S06's clone gets a `▶ your turn` tag; S11 says of the demo run "We ran this
  one for you: just watch." (cue 340, 19:22.7).
- **Pictures, pacing, text:** S02's "at the time of recording" chip no longer covers line 29's URL, and its tag swap no
  longer cross-fades; S07's troubleshooting cards stay about 8 s instead of 2 s; S06's sign-in chip stays readable; S08's
  "extra" tag leaves with its log; S13's 3-row strip keeps the `git commit --no-verify` row, and its "not in CI" chips no
  longer overlap; S05's cost tag cites "per GitHub's billing docs" instead of an internal file.
- **Narration and subtitles:** 20 of 25 items applied by the narration/subtitle fixer (S03 "runner" introduced and "on"
  re-worded, S13 M and clean-up, S06 empty commit, S11 watch-only, the pairing shifts, line breaks, the S15 label in full,
  zh openings); `python -m explainer.i18n check … --lang zh` printed OK; S03, S06, S11 and S13 were re-voiced.
- **Nits also fixed:** S01's tags ("live · our fresh machine", "act (a local runner) · same file"); S07's run-graph labels;
  S09/S12's Black emoji (coordinator, `common.emo_line`); S11's "after the fix" Summary turns red; S12's
  `externally-managed-environment` tag (on screen at 20:31.5, `writer/s12_pip_hint_1231.5.png`); S14's 4.3 s still frame;
  S15's tracker " · extra"; S16's clean-up row without a bare `git restore`.

**Still open after QA, and why:**
- **S06 *draft* 09:03, "The second undid a bug planted in class; we'll run it later."** (narration nit; final 09:10.7,
  `.srt` cue 164): a SAY edit for a nit was outside the fixer's rules. On screen the two chips now name both commits
  correctly; the audio still says "the second", which reads as the lower `git log` row.
- **S15 *draft* 26:41, "Here, git checkout -- puts the test file back."** (narration nit; final 27:14.6, cue 475): it works
  only because the recording did not commit; for a viewer who ran the README's add/commit/push it does nothing. Same
  reason; the S16 clean-up deletes that branch (cues 482–484, 27:40.3–27:47.6).
- **S12 *draft* 20:05, the `externally-managed-environment` hint is on screen only:** the tag is there (20:31.5); the
  narration does not mention it (nit; a SAY change needs a re-voice).
- **Shared code, not in any scene fixer's files:**
  - The stand-in runners' timings show in job-log panels (`11 passed in 0.04s`, `#16 DONE 19.8s`, `2 failed, 3 passed in
    0.34s`; S08, S10, S11) against the script's rule "never quoted"; `common.run_log()` crops ids and addresses but not
    durations (unchanged).
  - The English-only `.srt` line wrapper still breaks inside literals: `if:` / `always()` (cues 296, 443, 446; 16:51.4,
    25:23.0, 25:33.5), `runs-on:` / `ubuntu-latest` (cue 225, 12:53.2), `"Require` / `a pull request…` (cue 453, 25:58.0). The
    burned `.zh-en` copy is unaffected (one English line per cue).
- **Small leftovers named by verifiers:** "Pause and clone yours." was not added to S06's narration (the `▶ your turn` tag
  is on screen); `i18n/zh/GLOSSARY.md:243` still quotes 用 git checkout 把测试文件还原 without `--`.
- **Source drift (not rendered):** `script.md:1003`, S13's beat-7 SHOW, still describes one card "pushed it too?" (the scene
  draws "not pushed?" and "pushed?"). `README.md`'s chapter summaries 6 and 13 predate the QA fixes: 6 does not mention the
  empty-commit route, 13 says "clean up with `git restore` (and fix it if you pushed it)".

## Final-cut checks (1080p60, 2026-11-07)

- **Tags** (`report-tags.md`, round 1 on the pre-fix cut): 26 tags timed from the `events.json` sidecars plus scene offsets
  that match `chapters.txt` (offsets sum to 1734.60 s against 1734.70 s), four frames each
  (`tags/frames/tagNN_{a_in,b_mid,c_pre,d_post}_<t>.png`, sheets `tags/sheet_tagNN.png`), cross-checked by a 4 fps scan of
  the top-right corner (the same 20 on-screen stretches). No defect. The S12 review-bot item is verified: `All done! ✨ 🍰 ✨`
  (on screen 21:16.1–21:20.5) draws two gold stars and a cake wedge, no grey boxes (`tags/frames/s12_black_1279.50*.png`).
  S12 was not re-rendered in fix round 1; the round-2 visual check saw S13's tag still up at 22:22.
- **ASR** (`report-asr.md`, round 1): intelligible throughout; no real problem; four cosmetic wording differences.
- **Visual** (`report-visual.md`, round 2, on the re-burned `.zh-en.mp4`, written 21:09:07):
  - 37 contact sheets regenerated from the new file (4×4 tiles, one frame every 3 s, 0:00–28:51), all read
    (`sheets/sheet_01…37.png`), plus 26 full-size frames, crops and 0.5 s strips (`frames-r2/`).
  - **Fixed:** S13's Black log reads `Oh no! ✸ 💔 ✸` at 22:21–22:23 like S09's at 15:33–15:42, no grey box in any 0.5 s frame,
    no double draw (`frames-r2/emoji_strip_s09_s13.png`, `frames-r2/f_22m22.png`).
  - **Verified:** the changed zh lines burn in as one Chinese line over one English line, nothing clipped
    (`frames-r2/subs_changed_lines.png`).
  - Strict `freezedetect` (n=0.0003, 960 px, 10 fps) over the re-rendered S09 and S13: no hold of 4 s or more
    (`freezedetect_r2_s09_s13.log`); the other scenes keep round 1's result (`freezedetect_n0003.log`, two holds, A6).
  - Scene ends at the S08→S09, S09→S10, S12→S13 and S13→S14 cuts are empty (`frames-r2/end_*.png`); round 1 checked all
    16 (`scene_ends/`, luma 14).
  - No black or missing scene, nothing outside the frame, no clipped text, no tag stuck; garbled text only in transient
    morphs (A4).
  - Series rules: no instructor or staff name on screen; the webhook only as
    `https://hooks.slack.com/services/<your-webhook-path>` (24:45–24:57); the Slack cards show generic field names; the
    only addresses are localhost/0.0.0.0:9000 and runner paths.
- **Pairs** (`report-pairs.md`, round 2, `.zh-en.srt` written 20:52, 515 cues): **PASS.** All cues read zh against en; no
  meaning swap, including every 如果/因为/当/只要/只有…才/除非/时/之后 clause; one zh and one en line per cue; no break inside a
  command, path, flag or placeholder; no two neighbouring cues share an English line (round 1 had five such groups, all
  fixed: cues 132, 173–174, 233–234, 307, 513–514; crops `pairs-r2-sheet.png`). The burned `.ass` matches the SRT in all
  515 lines; parts concatenate to the full file. Eight minor one-cue-away cases remain (A7).
- **Measured** (`report-measured.md`, round 2, `measured.json`, evidence `measured-r2-frames/`, `*-r2*`): all four MP4s
  decode with exit 0 and no errors; formats, loudness, subtitles, chapters and durations pass; the stitch contains the new
  S09 and S13 renders (PSNR 44.6 dB and 46.0 dB against the scene MP4s). It repeats three known gaps, all decided below:
  ponder density (A1), the word count (A2), part 1 without its own recap (open nit).

## Accepted items (coordinator decisions)

- **A1. Five ponders in 28:54.7** (about 0.35 per 2 minutes), below AGENTS.md's aim of one per 2 minutes. Accepted under
  Conny's 2026-10-21 decision to keep the current density of 3–5 ponders per lecture (「我觉得可以保留现在的密度」); see
  gate 3.
- **A2. The script is 62 words over its ceiling:** 4,362 words against the 3,900–4,300 target (1.4 % over), after the QA
  additions (S06 empty commit, S13 clean-up, S11 "just watch", S03 runner).
- **A3. S13's "Lecture 21 · slides 29–31" tag stays through terminal-only beats** (tag 20, 1290.58–1351.80 s, i.e.
  21:30.6–22:31.8; the terminal-only beats 21:39–21:51 and 22:00–22:09, `sheets/sheet_28.png`, `sheet_29.png`). Kept: slide
  30 is the `--no-verify` command itself, so the picture is the command; `script.md` keeps the tag until "LECTURE off".
- **A4. Transient morph smears** of about 0.5–1 s, never read as a still (`report-visual.md` finding 4): 07:24, 07:33,
  07:42, 08:15, 09:33–09:34.8, 17:15, 18:36–18:37, 19:24, 22:23.0, 23:24, 25:15.
- **A5. The S13 "live · stand-in runner" chip touches the descender of "unchanged."** on the log panel's last line at
  22:21 (`frames-r2/crop_22m22_chip.png`; identical in round 1, not caused by the fix).
- **A6. Two holds of about 4 s under narration:** 06:23.8–06:28.0 in S04 (`sheets/sheet_09.png`) and 28:16.8–28:20.8 in
  S16, "Test yourself" question 1, an intended pause (`sheets/sheet_35.png`).
- **A7. Eight minor `.zh-en.srt` cases where a word sits one cue away from its English** (`report-pairs.md` a–h, with the
  yaml item to fix each): 68–69 (03:52.0, 构建), 73–74 (04:05.6, "is built"), 175–176 (09:58.1, 运行), 354–355 (20:12.2, 再
  commit 一次), 380–381 (21:23.6, 一个 commit), 431–432 (24:21.8, 失败也包括在内), 433–434 (24:30.1, 分支、commit),
  436–437 and 490–491 (加; 这里…都要删). Nothing is reversed or contradicted.
- **A8. The QA nits left open** (listed under "Still open after QA"). A narration change needs a re-voice, a re-render and
  a re-burn; none changes meaning.

## Open nits (not ruled on one by one; left for the coordinator)

None blocks release. Each needs a narration, yaml, scene, toolkit or metadata change, which this record does not make.
- **Bilibili description:** `video.yaml` `publish.description_zh` credits the instructor by name (`report-measured.md`
  notes, still open from round 1). Not in the video or subtitle files, but it goes on the Bilibili page and the series
  rules say no instructor name.
- **Four subtitle/voice wording differences** (`report-asr.md`): 23:33.9 (cue 411) the subtitle reads "The
  detect-private-key hook is a local hook only." while the voice says "Detect private key is a local hook only."; 25:00
  (cue 435) `enabled=true or enabled=false` spoken "enabled, true, or false"; 26:00.9 (cue 454) the second "…before
  merging" is not spoken (the voice ends at "to pass"); 27:41.9 (cue 483) "feature/" is not spoken ("the test protection
  branch"). Cue 345 (19:46.7) runs about 0.2 s past its end.
- **Fourteen `.zh-en.srt` cues whose top line has no Chinese** (`measured.json` "zhen_first_line_no_han"), each verbatim log
  text, a command or job names from the zh track: cues 3, 4, 5, 7, 123, 273, 276, 277, 313, 329, 330, 370, 394, 480 (e.g.
  00:08.5 `Integration tests，success`, 15:33.3 `1 file would be reformatted`, 22:06.6 `git commit --no-verify -m "quick
  fix"`); `.zh.srt` has 8 of the same kind. Intended per `i18n/zh/README.md` and the glossary's verbatim rule.
- **Part 1 has no recap of its own** (12:36; it ends on run 1's verdict and "In part 2 we open every log").
- **Chapters:** every start is the scene start rounded down (up to 0.975 s early, S13: 21:29 against 21:29.97).
- **Frame rate:** 60 fps (the 1080p60 scene renders, as in L02–L20); the repo default for new episodes is 30 fps. The
  burned copy has one more video frame (104,077) than the clean cut (104,076).
- **No `QA_FOLLOWUPS.md`** for L21, and no Bugbot thread was copied into the episode folder.
- **Process note:** the round-2 visual check removed its own stale sheets with `rm -f FR/sheets/sheet_*.png` (a wildcard,
  inside `build/final-review/sheets/` only, as its report says).

## Verified (final render)

All numbers are from `measured.json` and the five reports, on the files in `output/` as they are now (written 2026-11-07
20:52–21:11 UTC), except the tags and ASR results, which are round 1's (see the header).

- **Files:** H.264 High, yuv420p, 1920×1080 at 60 fps, AAC LC 48 kHz stereo at about 179 kb/s. Each decodes in full with
  exit 0 and no errors (`decode-r2_*.log`).

  | file | duration | video frames | size (bytes) | loudness | LRA | true peak |
  |---|---|---|---|---|---|---|
  | `ac215-l21-cicd-github-actions.mp4` | 1734.698 s (28:54.7) | 104,076 | 99,807,691 | −16.1 LUFS | 2.1 LU | −2.7 dBTP |
  | `ac215-l21-cicd-github-actions.zh-en.mp4` | 1734.698 s | 104,077 | 97,931,515 | −16.1 | 2.1 | −2.7 |
  | `ac215-l21-cicd-github-actions_part1.mp4` | 756.312 s (12:36.3) | 45,372 | 38,058,684 | −16.1 | 2.1 | −2.8 |
  | `ac215-l21-cicd-github-actions_part2.mp4` | 978.421 s (16:18.4) | 58,704 | 61,762,067 | −16.1 | 2.1 | −2.7 |

  The 16 scene MP4s sum to 1734.588 s; parts sum to 1734.733 s (+0.035 s against the full cut). Part 1 is byte-identical
  in size to round 1 (S01–S07 unchanged); part 2 changed (61,774,451 → 61,762,067 B).
- **Subtitles:** `.srt` 506 cues, `.zh.srt` 439, `.zh-en.srt` 515. Part 1 has 219 / 189 / 220, part 2 287 / 250 / 295; each
  language's parts equal its full file in cues and text (part 2 offset 756.2 s).
  - In all nine files the indexes are sequential, the cues in order, inside the runtime, with no overlaps and none shorter
    than 0.8 s; the shortest are 1.000 s (`.srt`), 1.209 s (`.zh.srt`) and 1.100 s (`.zh-en.srt`). The last cue ends at
    1733.25 s (28:53.3).
  - Every `.zh-en.srt` cue has exactly two lines, no line empty, no English line with Chinese characters.
  - A grep of `output/*.srt`, `transcript.md` and `chapters*.txt` found no IPs, Slack webhook URLs, token patterns
    (`xox*`, `ghp_`, `AKIA`, `sk-`), 32-hex ids or instructor name (`report-measured.md`).
- **Chapters:** 16 entries, titles equal to `video.yaml`'s in order, each start the floor of the scene's real start (within
  0.975 s). `chapters_part1.txt` has 7 entries, `chapters_part2.txt` 9 (part 2 at 00:00, 02:13, 03:41, 05:44, 07:33, 08:53,
  11:14, 13:04, 14:42). `README.md` now carries them and the durations (this pass).
- **Scenes:** all 16 present and in order (S01 93.48 s, S02 110.83, S03 116.98, S04 96.28, S05 103.27, S06 126.02, S07
  109.33, S08 133.75, S09 87.77, S10 123.40, S11 108.52, S12 80.35, S13 140.75, S14 110.17, S15 97.53, S16 96.17); the tags
  and visual checks matched every boundary to the cumulative sidecar durations; every scene ends on an empty frame.
- **Narration:** 140 SAY blocks, 4,362 words, 160.6 wpm over 1,629.4 s of voice; 649 anchors; no "anchor not found" in the
  16 render logs.
- **Lecture tags:** 26 tags, each checked on frames 0.3 s after fade-in, mid-span, 0.3 s before fade-out and 0.5 s after;
  none overlapping, none outliving its scene.
- **The QA musts on the final cut** (frames extracted by this record's writer from the burned copy): S13's two clean-up
  cards, "not pushed?" `git reset --hard HEAD~1` and "pushed?" ✗ `main` with `pre-commit run --all-files` · `git add .` ·
  `git commit -m "Format service.py"` · `git push`, at 22:52.0 (`writer/must_s13_1372.0.png`), with the subtitle "Run
  pre-commit run --all-files, then add, commit and push,"; S14's re-ordered webhook pair at 23:54.8 (`.zh-en.srt` cues
  423–424, read in the file). Also re-checked: S06's empty-commit card at 10:41.0 (`writer/s06_empty_commit_641.0.png`) and
  S12's pip hint at 20:31.5 (`writer/s12_pip_hint_1231.5.png`).
- **Privacy:** no instructor or staff name, key, token or real IP on screen or in the subtitles; the webhook URL is a
  placeholder; slide 11's imagined reply is not shown.
- **Provenance** (`ASSETS.md`):
  - Terminal lines come from the 2026-11-06 captures in `assets/terminal/` (`laptop/`, `runner/`); each README command ran
    as printed, in README order, with extras tagged `extra`; nothing in a terminal panel is typed by hand. Code panels
    quote `assets/source/cheese-app-ci-cd/` copied unchanged at `b8458ff`; older versions (`c3b227f`, `140f138`,
    `199abd9`) from the repository's history.
  - Live: the clone, `nothing to commit` (exit 1), the push to the stand-in repository (run 1), the Lecture 9 fix and run
    2, the `--no-verify` sequence and run 3, the demo commit's run, the no-load run (exit 125), Part 6's `def broken()` (11
    passed) and `def test_broken` (1 failed, 11 passed), `act -l` and `act push`.
  - `recorded`: the README screenshot's run graph and timings (54 s / 22 / 18 / 20 / 39 / 4 s), transcribed, the image not
    copied. `illustration`: the Actions tab, run pages, Settings → Secrets, Settings → Branches, the pull request, the Slack
    message. Billing minutes come from GitHub's billing docs (digest §2), not measured.

## Not claimed

- **No human listened to this cut** or watched it. The listening gate rests on the series waiver quoted under gate 6, and
  the audio was checked only by machine (the ASR round trip and the onset check, on the round-1 cut).
- **The tags and ASR checks did not run on the final files.** They ran on the round-1 cut; the fix round re-rendered S09 and
  S13 (picture only, same lengths) and changed subtitle text (five zh lines, one `en_display` comma), but the audio of the
  re-rendered scenes was not transcribed again and their tags were not re-framed (the round-2 visual check covered those
  scenes by its own sampling).
- **The Chinese subtitles were reviewed by agents only:** the QA subtitle watcher, the narration/subtitle fixer, the scene
  verifiers and the pairs check. No human translator or native reviewer read them.
- **No GitHub-hosted run was observed.** No push reached GitHub, no Actions run ran on GitHub's `ubuntu-latest` machines,
  no artifact was stored by GitHub, no repository secret was set, no branch protection rule was created and no pull
  request was blocked. The Actions tab, run pages, step lists, the settings pages and the PR are `illustration`s; the
  stand-in runners differ from a hosted VM (Alpine, root shell, `uses:` steps replaced by stand-ins; `ASSETS.md`).
  Whether a hosted run gives exactly the same results on a later day was not re-checked.
- **No Slack workspace was used:** no incoming webhook was created and no message was sent or received; the Slack
  message is drawn from the payload template. **No fork** was made and no "enable workflows" click happened; the fork
  route's `Everything up-to-date` and the empty-commit workaround are described, the latter "shown, not run".
- **No Docker Hub login or GCP step** is part of this lecture; the only Docker Hub contact is the no-load run's `pull access
  denied` (exit 125).
- **The visual check sampled one frame every 3 s**, plus targeted frames; motion between samples was checked only by
  `freezedetect`. The round-2 contact sheets were read on the burned copy only; the two part files were measured (probe,
  decode, loudness, subtitles, chapters, frame counts) but not sampled visually on their own.
- **Most QA fixes were verified only on previews** (720p `--at` frames and `--every 2` sheets before the 1080p60 renders),
  not one by one on the final cut. This record's writer re-checked the two musts, S06's empty-commit card and S12's pip hint
  on final-cut frames or subtitle files (`writer/`); the final-cut checks cover the rest only by their own sampling and
  reading of every cue.
- **Stated as the coordinator gave them, not checked here:** lexicon PR #121 (`131f2c3`); the digest's container runs; the
  independent script reviews and per-scene critics beyond their files; the resumed interruptions.
- **Review bots:** no `QA_FOLLOWUPS.md` exists for L21, and nothing in this record checks Bugbot threads on an L21 PR.
- **`README.md` durations and chapters were filled in this pass** from `measured.json` and `chapters*.txt`; its chapter
  summaries were not reviewed by a separate agent (two predate QA fixes, see "Still open").
- **Every check in this record is an agent's.**

## Fix round after the final-cut checks

- **Round 1 findings fixed** (commit `c077bc5`, 2026-11-07 20:42 UTC):
  - S13: `Oh no! 💥 💔 💥` drawn instead of three grey boxes (💥 and 💔 now drawn by `common.emo_line`; S09's local overlay
    and the shared glyphs do not stack).
  - Five zh lines (cues at 07:32.9, 09:49.9, 13:15.5, 17:27.6, 28:44.2) and one `en_display` (13:15.5) re-cut to the English
    clause stops, so no English sentence repeats under zh fragments.
  - S09 and S13 re-rendered at 1080p60 (logs 20:47–20:48), the cut re-stitched (20:52) and re-burned (21:09), still 28:54
    (part 1 12:36, part 2 16:18); scene durations unchanged.
- **Round-2 checks on the new files** (`report-visual.md`, `report-pairs.md`, `report-measured.md`): all items verified, no
  regressions; measured passes (I −16.1 LUFS, TP −2.7 dBTP). The tags and ASR reports are from round 1.
