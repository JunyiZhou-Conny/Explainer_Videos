# Review record: AC215 · Lecture 6 — LLM: Agents I: function calling by hand, ADK, MCP, many agents, the harness

Follow-along of [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag) `main` @ `e17a39f` (section
*Agents*, with the three lecture 5 steps it stands on),
[dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk) `main` @ `f89faa7` (the
whole root README) and three Colab notebooks (Cheese Quiz, Travel Planner, Cheese Newsletter · Harness;
saved outputs only). The issue of record is Explainer_Videos#43. The work is in the series draft PR
Explainer_Videos#44 ("AC215: L05 and L06 in production", branch `claude/mlops-learning-videos-7b5use`).
Claude Code cloud sessions (Claude) produced it:

- **Captures:** 2026-10-18, 22:58–23:00 UTC (llm-rag laptop and container) and 23:31–23:33 UTC (a fresh
  Debian 12 "laptop" with no Python, for ADK), without a Google or OpenAI key (`ASSETS.md`).
- **QA draft:** the 480p draft (31:02, parts 15:18 + 15:43) committed in `983e36e` (2026-10-20 18:35 UTC).
- **Whole-video QA:** seven watchers on that draft, one fixer for each scene with findings (15: S01, S02,
  S04–S16), one narration/subtitle fixer, and 16 verifiers (merged output
  `/root/ac215-backup/args/l06qa_merged.json`). Fixes committed in `34d721b` (2026-10-20 21:44 UTC); the
  verifiers' corrections in `3534ba8` (2026-10-21 03:03 UTC).
- **Finishing pass** (`/root/ac215-backup/tasks/w5f2e5y3g.output`, 18 agents; commit `705f7f1`,
  2026-10-21 14:36 UTC): shared `scenes/common.py` fixes and their verifier, a plan of 14 text items and
  6 scenes with items (each scene followed by a verifier), then a sweep of all 16 scenes for L05's three
  defect patterns and a verifier of the sweep.
- **1080p60 renders:** all 16 scenes, 2026-10-21 14:36:58–15:20:13 UTC (`build/logs/`); every render is
  newer than its scene file and `common.py` (measured check).
- **Previous final cut (reviewed 2026-10-21, 31:12.1):** scene segments 15:21–15:37 UTC
  (`build/stitch_h/`), the clean cut and its subtitles at 15:40, the zh-en copy, chapters and transcript at
  16:03, the parts at 16:04–16:05 UTC. Subtitles, chapters and transcript committed in `7c95e6b` (17:47
  UTC).
- **Final-cut checks of that cut:** five agent checks on 2026-10-21 (evidence files written 17:50–19:04
  UTC); the coordinator saved their returned text as
  `build/final-review/report-{tags,asr,visual,pairs,measured}.md` (19:06 UTC). All five reports were read
  in full for this record.
- **Fix round 1** (plan `/root/ac215-backup/args/l06-fix1.json`; reports
  `/root/ac215-backup/tasks/wg1tqwn5j.output` and, for the S10 verifier that a usage limit had stopped,
  `/root/ac215-backup/tasks/wy402fgmb.output`): one text agent and its verifier (P1, P2, T1–T4; the
  verifier found T3 not done and did it), then five scene groups (S08; S12 + S07 + S14; S04; S02 + S03;
  S10), each a fixer and a verifier on a fresh 720p render. Committed in `980d756` (2026-10-24 18:00 UTC).
- **Re-render and re-stitch (the cut this record describes, 31:14.9):** the ten changed scenes (S02, S03,
  S04, S06, S07, S08, S10, S12, S14, S15) re-rendered at 1080p60 on 2026-10-24 (render logs and stitch
  inputs 18:14–18:50 UTC); the clean cut and its subtitles at 18:53, the zh-en copy, chapters and
  transcript at 19:13, the parts at 19:14–19:15 UTC; committed in `6311d49` (19:17 UTC). The other six
  stitch inputs are the 2026-10-21 renders. The tracked files in `output/` are identical to `6311d49`.
- **Re-check of the re-stitched cut** (2026-10-27): three agent checks, measured, ASR and the changed
  scenes, with their evidence in `build/recheck/`; and, for this update, the two review-bot threads
  (`build/recheck/bots/`) and the subtitle text against the previous cut
  (`build/recheck/text_diff_vs_prev.json`).
- **This record:** first complete version 2026-10-23, written before fix round 1 ran, from the five
  reports, and checked by a separate agent the same day (machine checks only: it re-measured the four
  MP4s, loudness, audio MD5s, cue counts and times, chapters, SAY, word and anchor counts and the render
  logs, viewed the frames the gates rely on, corrected eight statements and fixed the README's telemetry
  command, item 27). **Updated 2026-10-27** after fix round 1 and the re-stitch: items 1–18 moved to
  "Fixed" or "Accepted" with the re-check's times and evidence, the measured numbers replaced from
  `build/recheck/measured.json`, the coordinator's decisions on items 25–29 recorded, the review-bot
  threads checked, and every time from S06's reworded sentence on converted to the new cut. `README.md`'s
  durations and chapter blocks were updated to match in the same update.

This record is based on the five reports of the previous cut and the evidence folders beside them, the
QA, finishing and fix-round outputs named above, the re-check's three results and `build/recheck/`,
`script.md`, `BRIEF.md`, `ASSETS.md` and `SLIDES.md`, and `output/*.srt` for cue times. Verified facts
and unclaimed reviews are kept in separate sections.

**Conventions in this record:**
- **Times** are mm:ss in the re-stitched cut (`output/ac215-l06-agents-1.mp4`, 31:14.9) in the gates,
  the items and "Verified", except where marked *prev* (the previous final cut, 31:12.1) or *draft* (the
  480p QA draft, 31:02). The sections "Whole-video QA", "Finishing pass" and "Final-cut checks of the
  previous cut" keep the times of the cut they describe.
- **Previous cut to this cut** (`build/recheck/prev-srt/` aligned cue by cue with `output/`, and the
  scene starts in `build/recheck/measured.json`): no change up to *prev* 10:29.4 (S01–S05 and S06 before
  its reworded sentence); +0.283 s from *prev* 10:31.7 to 18:41.0 (the rest of S06, S07–S09, S10 before
  SAY[1]'s reworded sentence); +1.300 s from *prev* 18:45.2 to 19:47.7 (S10 between its two reworded
  sentences); +2.133 s from *prev* 19:54.0 to 28:44.4 (the rest of S10, S11–S14, S15 before its reworded
  sentence); +2.716 s from *prev* 28:47.1 (the rest of S15, S16). The four reworded sentences themselves
  are new audio (items 3–6). Times carried over from the review of the previous cut and not re-measured
  were converted this way; where a time is a cue start or end it was read from the new `.srt`.
- **Draft times** are up to about 9.5 s earlier than the same moment in the previous final cut (fixes
  after the draft moved the scene starts by 0 s in S01, +4.1 to +5.7 s in S02–S08, +6.3/+6.4 s in S09–S10
  and +8.6 to +9.5 s in S11–S16; `build/qa/scenes.json` against the previous `measured.json`).
- **Cue numbers** name their file: `.srt` (491 cues), `.zh.srt` (417) or `.zh-en.srt` (487); the
  numberings differ. Against the previous tracks (490 / 417 / 489): in the new `.srt`, #314 is a new cue
  and the cues after it are numbered one higher than before; in the new `.zh-en.srt`, the cues after #84
  are one lower and those after #142 two lower; `.zh.srt` numbers are unchanged. Cue numbers marked *prev* are the previous tracks'.
- **Evidence paths** are relative to `build/final-review/` (the previous cut) unless they start with
  `recheck/`, which is `build/recheck/` (the re-stitched cut). Both folders are git-ignored and exist
  only in the producing session; a successor re-runs the checks to reproduce them. In
  `build/final-review/`, `writer/` holds a frame the earlier draft's writer grabbed, `verifier/` frames
  of the previous cut from a check of that draft, `writer2/` the record's SRT listing (`srt-dump.txt`)
  and `verifier2/` the 2026-10-23 verification's loudness logs, English cue listing and four frames
  (`clean_750.0.png`, `clean_860.5.png`, `clean_889.8.png`, `clean_1188.15.png`). In `build/recheck/`,
  `finalcut/<scene>/` holds the changed-scene check's frames, named `f_<full-cut time>_s<scene time>.png`,
  and in its `contact/` folder `zhen_NN.png` sheets of the burned copy, one frame every 2 s.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle from the staff's recorded run, not on a value proposition.
   - "Here's a question for a cheese expert" (00:00.0); two lines of `out.txt` print a function call and
     its arguments before the answer (00:06.6–00:14.5); "Ten passages came back, all from one book,
     filtered by author. But Gemini runs in Google's data center, where localhost means nothing."
     (00:15.2–00:24.3); "So who searched your database, and who chose the book?" (00:24.6–00:27.5). The
     two questions shrink into a small YELLOW card top right that stays to the end of S01 (frames
     00:30–01:54.5 in `verifier/sheet_s01_ycard.png`); S07 brings the card back to answer it.
   - The lecture's bigger version follows: the Paris trip that must replan, and what LLMs and RAG lack
     (00:27.8–00:44.8, slides 20–22).
   - **Payoff:** "So, who searched your database? Gemini wrote the call and chose the book; your Python
     ran it, on your laptop." (S07, 12:38.0–12:45.1).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. BRIEF.md ("Visual
   set pieces") defines eight; each is animated before or with the commands it explains:
   - **V1, three lanes, then the anatomy (S02):** one question, the same `gpt-4o` in three lanes: one
     call (02:29.0), a workflow whose Python orders 11 calls (02:35.9–02:58.6), an agent with a hosted
     web search that stops on its own (03:02.9–03:15.3); the lanes fold into the lecture's anatomy,
     "dynamic control, the steering wheel" (03:32.5), "an agent isn't a smarter model" (03:35.1).
   - **V2, the envelope (S03):** "Every call is a fresh envelope" (03:54.8); seven sheets change the top
     pick; "Memory is paper you put back in the envelope" (04:31.3); the swapped roles (04:51.5).
   - **V3, the model writes the call, your code makes it (S04 build; S06–S07 run):** the lecture's RAG
     ladder shrinks to a menu of two hand-written declarations (05:13.9–06:21.9); the three duties
     (06:24.2–06:36.0); the stage, "The model never gets your database, only a menu" (07:16.7); call 1,
     the dispatcher and call 2 with the thought signature (S06 09:36.7–11:21.4, S07 11:22.0–12:24.7).
   - **V4, the loop and its stop rule (S08):** the hub unrolls into a loop (14:04.9–14:16.6), "a reply
     with no function call is the final response" (14:18.4), the caps and `MaxTurnsExceeded`
     (14:37.2–14:48.8), dynamic control greyed out because a framework writes it (14:49.1).
   - **V5, which Python, which wheel (S09):** with no Python, uv downloads CPython 3.15.0; `onnxruntime`
     has wheels only up to 3.14; `uv python pin 3.13` (17:13.5–17:48.4).
   - **V6, the shared whiteboard (S11):** output keys write cells, placeholders read them, "The agents
     never call each other" (20:54.2–21:18.9).
   - **V7, one protocol, one plug per server (S12):** three tool families (22:13.2–22:27.2), ten custom
     integrations (22:27.5–22:42.6), MCP as a shared protocol (22:42.9–22:56.1), the tutorial's three
     plugs from 22:56.4.
   - **V8, turnstile and receipt (S14, S15):** a finalize call only proposes, PENDING, and only an
     explicit yes copies pending to approved (26:48.0–27:07.1); success is a receipt and a file on disk
     (28:53.2–29:07.7); a rule left in the prompt slips through, "a note is not a check" (29:18.3).

   **Lecture slides:** a GREY "Lecture 6 · slide(s) …" tag top right in 14 of the 16 scenes (all but S05
   and S10, whose `script.md` header says `Lecture: none`), 29 tags in all. Each cites the slides of its
   scene's `Lecture:` line in `script.md` (from S01's 20–22 to S16's 41 and 32–33), except S01's second
   tag, "slides 51–53", a layout sample shown while the narration explains the tag (00:59.97–01:03.8). The
   slides are redrawn, never shown. `SLIDES.md` digests the deck and maps the ten planned chapters to it;
   its "This video and the slides" section predates the script (finishing plan).

   **How this was checked:** QA's two director watchers read every draft contact sheet against the SHOW
   lines. In the previous cut, the visual check read all 625 tiles of the burned copy (one every 3 s), and
   the tags check found the cited picture on screen across the tag spans except two swapped-in tags that
   led their picture and three spans that outlived it (items 7, 8, 11, 12, 14). Fix round 1 changed only
   when those five tags enter or leave (the fixers' reports name no added or removed tag), and the
   re-check's changed-scene check found each now on its picture (items under "Fixed"); small leads under
   1.5 s are accepted (item 24). In the re-stitched cut the changed-scene check read the burned copy's
   contact sheets of the ten re-rendered scenes (one frame every 2 s) and frames at every fix.
3. **Pause-and-ponder moments and a recap** ✔ by Conny's decision for the series (2026-10-21, see below):
   five ponders, against AGENTS.md's aim of one every 2 minutes.
   - **Ponders:** five cards (`ponder_at`), each followed by a silent timer. No English cue plays during
     a timer (the longest cue gap, 9.85 s at 06:40.8–06:50.6, is S04's timer), and the momentary loudness
     during every timer is at most −129.1 LUFS (`recheck/measured.json`). Each answer starts as its timer
     ends:

     | scene | question (card text, condensed) | card | timer | answer starts |
     |---|---|---|---|---|
     | S04 | Nine author names, eleven books: at least how many books can `get_book_by_author` never reach, and can the agent still get to them? | 06:42.1 | 8 s | 06:50.6 "Two books." |
     | S08 | Call 2 passes the tools but no `tool_config`; if Gemini answers with another function call, what does `cli.py` do? | 13:46.4 | 8 s | 13:55.0 "It prints a response whose only part is a function call" |
     | S09 | No Python on the laptop, the project asks for 3.10 or newer: which Python will `uv sync` use? | 17:04.6 | 6 s | 17:11.2 "Then install: uv sync."; the answer 17:13.5–17:23.0 (CPython 3.15.0) |
     | S13 | The classifier answers "Simple", with a capital S: which handler runs? | 25:49.1 | 6 s | 25:55.7 "The else branch: clarification." |
     | S14 | In turn 3 the model got `needs_confirmation`: why can't it call `finalize_itinerary` again to approve its own plan? | 27:07.9 | 8 s | 27:16.5 "Because apply_confirmation runs on the human's message" |

     Frames of each card on the burned copy of the previous cut: `measured/frame-zhen-t406.0.png`,
     `t830.0`, `t1027.5`, `t1550.0`, `t1630.0`. The card text is `script.md`'s `PONDER` lines word for
     word. BRIEF.md's ponder table asks the same five questions; only its S04 wording differs ("which
     books can the agent never reach by author, and is it for the same reason?").
   - **Rate:** 0.16 per minute. It is 402.1 s from the start to the first card, then 415.8, 189.6, 517.9
     and 72.2 s from each timer's end to the next card, and 238.4 s from the last timer's end to the end.
     The longest stretch without one is 17:11.2–25:49.1 (8:38). AGENTS.md's aim would be about 15–16 at
     this length.
   - **Not counted as ponders:** S03's "Spot it" card ("Can you spot the slip?", 04:45.9): `script.md`
     says "no timer", but a line draws under "Spot it" for 4 s with the code on screen before the answer
     (04:51.5; `verifier/sheet_s03_spot.png`); and S12's 5 s silent beat after "do you see a problem?"
     (asked at 22:32.3; silence 22:34.7–22:40.0). Separately, 16 spoken "pause" lines tell the viewer to
     stop and run a step, from "pause to run the setup" (02:15.2) to "pause, and run the demo" (29:29.7);
     S01's "Pause at each yellow your-turn tag" (01:03.3) explains the convention.
   - **Recap** ✔: S16 (from 29:36.2) tears down (29:36.2–30:09.7), fills the lecture's anatomy with the
     tutorial's code and adds the two pieces to the lecture's formula, "a loop the framework runs, and
     checks that your own code enforces" (30:11.0–30:42.2), then asks five test-yourself questions and
     points to the answers in `exercises.md` (30:42.4–31:12.7; frames of the previous cut
     `measured/frame-zhen-t1820.0.png`, `t1845.0.png`). Part 1 closes on "In part 2, a framework runs
     this loop for us." (15:18.6–15:21.5); part 2 opens on "Part 2: frameworks own the loop." (15:24.6).
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」 — keep the current density: 3–5 ponders per lecture, plus a spoken
     recap and test questions.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** `script.md`'s conventions are 1–3 sentences and at most about 60 words per SAY
     block, sentences under 30 words. Every block is 44 words or fewer and every sentence under 30 words
     (the longest has 29); 152 of the 153 blocks have 1–3 sentences, and S05's "The agent needs the index
     from lecture 5. Kept that database? …" has four short ones (33 words). Commands, flags and paths
     are said in words ("dot env", "uv python pin 3.13"); versions that will change are said "at the time
     of recording".
   - **Size:** 153 SAY lines and 4,307 words, identical block for block to the 153 narration blocks in
     the 1080p60 render sidecars; the series budget is 3,900–4,300, so this is 7 words over its top (fix
     round 1 added 8: S06 +1, S10 +4, S15 +3). Kokoro `af_heart` at speed 0.9. Pace 137.8 wpm over the
     runtime and 152.3 wpm over the 1,697.3 s of voice (90.5 % of the runtime); per scene 137.0 (S09) to
     164.4 (S15) wpm over voice time.
   - **Anchors:** 679 `vo.wait_until` calls in the 16 scene files (26 in S03 to 58 in S09; 670 with a
     literal phrase, 9 with an expression; fix round 1 added S14's "pause, and run the four turns"). The
     16 1080p60 render logs (`build/logs/`, ten of them from 2026-10-24) contain no "anchor not found" and
     no translation warning (`recheck/render_logs.json`).
   - **Ear fixes after the draft:** the QA's ASR watcher found four words Kokoro read the wrong way
     ("tear down" as "teer", the noun "lives", "Resending" as "resenting", the noun "use") and four
     hard-to-hear phrases ("Kept that database?", the recap's "checks your code enforces", "dollars out
     of", "ours stopped"). Seven L06-only lexicon entries fixed the readings ("Before part 2, tear down"
     14:59.6, "Pause and tear down" 15:17.0, "Tear down" 29:36.2, "Approval lives" 26:59.8, "Resending"
     12:22.0, "Kept that database?" 08:59.7, "use agents" 26:11.5). SAY lines were reworded: "checks
     that your own code enforces" (30:37.5); in the finishing pass "the web server stopped" (was "ours
     stopped", 20:09.7), "2,690 of the 6,000 dollars" (was "2,690 dollars out of 6,000", 27:33.1),
     "check yours" (20:45.1) and "uv run adk telemetry disable" (reworded again in fix round 1, item 6).
     Three sentences holding version numbers were split so a sentence mark times their cues ("the banner
     prints." 08:13.0, "It also lists Chroma and sentence-transformers." 16:57.9, "But picking one still
     fails…" 19:27.8).
   - **Fix round 1** reworded four sentences after the previous cut's ASR (items 3–6): "…both
     declarations with the enum, mode ANY and temperature zero." (S06, 10:25.7–10:31.7), "…change it
     later with this command: uv run ADK telemetry disable." (S10, 18:39.8–18:46.3), "The log says it
     loaded the dot env at the repository root, and found the root agent in baseline dot agent." (S10,
     19:49.1–19:55.9) and "Then send email wrote the HTML to a file." (S15, 28:46.6–28:49.5). The ASR
     re-check hears all four as written.
   - **These lines in the previous cut's ASR:** only three appeared in its triage (`triage-base.txt`;
     *prev* cue numbers), all as recogniser noise: cue 132 (a first word dropped at the clip start; the
     large model matches), cue 464 ("Ctrl" heard as "control") and cue 429, which the large model hears
     as "…line by line, $2,690 of the $6,000." (`asr-large-clips.json`), so "of the" is audible.
   - **Caveats:** the previous cut's ASR found six low-severity weak spots (items 3–5, fixed in fix round
     1, and accepted item 23) and a narration delay behind the picture and subtitles that grows at each
     scene join (accepted item 19; re-measured on this cut at +0.05 to +0.16 s).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers
     ("newcomer", one per part), a subtitle watcher, a follow-up watcher and an ASR watcher. The
     newcomers are agents that worked from the draft's contact sheets, exact 480p frames and the English
     `.srt`, with the READMEs open; they reported 21 of the findings.
   - **58 timestamped findings: 2 must, 27 should, 29 nit.** Both musts and all 27 shoulds are fixed, and
     each fix was checked by a verifier (per scene in the QA round; in the finishing pass by the shared
     verifier or the scene's verifier): scene and narration fixes on fresh 720p or 480p renders or TTS
     clips, subtitle fixes in the yaml and on the tracks the QA text fixer replayed from the draft's clips
     (the S06 and S12 verifiers say they did not rebuild the tracks themselves; the final pairs check
     read the result). Of the 29 nits, 27 are fixed (6 of
     them in the finishing pass), one is worked around in the episode (cue timing inside a sentence: three
     sentence splits; the toolkit fix is deferred) and one is partly fixed (the S13 Guild panel). Details
     under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified" (`recheck/measured.json`, measured on the
   re-stitched cut).
   - **Duration:** 31:14.9 (1874.889 s), inside the series' 25–35 min; parts 15:24.7 (924.655 s) and
     15:50.2 (950.235 s), which sum to 0.001 s more than the full cut.
   - **Loudness:** −16.1 LUFS integrated in the clean cut, the zh-en copy and part 2, −16.0 LUFS in part
     1; LRA 2.3–2.5 LU; true peak −2.7 dBTP (clean cut, zh-en and part 1) and −2.8 dBTP (part 2). The
     build's target is −16 LUFS with true peak at or below −1.5 dBTP: **every file meets it** (the
     previous cut measured −2.6 / −2.6 / −2.7 / −2.8 dBTP).
   - **Caption bounds:** in the burned layout every subtitle lies inside x 428–1489, y 991–1063 (part 2:
     x 459–1459), in the band below the picture (which ends at y 938), and none falls in the 40 px side
     margins (libass render of each `.zh-en.ass` at 1 fps, 1,648 frames with text in the full cut;
     `recheck/bbox-*.log`). On 14 burned frames at the fix moments the glyphs sit in rows 992–1062
     (changed-scene check).
   - **Music balance:** does not apply. L06, like L02–L05, has no score: `video.yaml` has no `music:` key,
     and the ponder timers measure as silence.
   - **Subtitle sync:** no cue's speech starts more than 1 s after the cue (491 cues; median 0.04 s,
     largest 0.61 s at cue 92, 05:47.1, or 0.69 s with the measured narration lag; ASR re-check,
     `recheck/onset.json`), with the narration delay of accepted item 19 on top.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.
   Review moments optional since 2026-10-22 (AGENTS.md): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」

   **ASR round trip.** The round trip of the 2026-10-23 record (`report-asr.md`) ran on the previous
   stitch: base.en over the whole clean cut (490 cues, 213 with some difference, 4,349 words recognised);
   after removing number, identifier, possessive and punctuation differences, 124 differences in 114 cues
   remained (`triage-base.txt`); 62 of those cues were re-run with large-v3-turbo on their own audio (30
   match word for word) and nine doubtful ones again with 2 s of context. The large model recovered every
   word base.en seemed to drop or garble, among them the *prev* 11:43–11:49 passage and "Agent
   Development Kit runs" (*prev* 15:28.2); it left six low-severity weak spots (items 3–5, accepted item
   23). Since that run the narration of three scenes changed: **S06** (SAY[4]), **S10** (SAY[1] and
   SAY[7]) and **S15** (SAY[2]). The re-check of 2026-10-27 (`recheck/asr-summary.json`) ran the round
   trip again on this cut: base.en over the whole clean cut (491 cues, 213 with some difference, 4,363
   words recognised against 4,225 subtitle words; 131 differences after removing number, identifier and
   cue-boundary noise, `recheck/triage-base.txt`), and large-v3-turbo on the four reworded sentences with
   0.3 s and 2 s of context, which hears each as written (items 3–6). The re-check found the base.en
   turnover in unchanged cues to be recogniser noise: S01's audio is sample-identical to the previous
   cut's and base.en still changed there, and the 11 newly differing cues it re-ran with large-v3-turbo
   all match apart from the homophone "won"/"one" (cue 459). The rest of the narration is the previous
   cut's audio: identical within a 5 ms shift up to S06's reworded sentence, the same narration
   re-encoded elsewhere (correlation 0.984–0.994). The zh-en copy carries the same audio (audio stream MD5
   `94d30dd3f0fec89d531d9a84797ccf16` in both).

## Whole-video QA (480p draft, 2026-10-20/21; times are draft times)

**Watchers and findings** (`l06qa_merged.json`, key `result`):

| watcher | must | should | nit | what it read |
|---|---|---|---|---|
| director, part 1 (S01–S08) | 0 | 2 | 4 | sheets 001–020 against SHOW/SAY and the `.srt`; exact frames |
| newcomer, part 1 | 1 | 4 | 6 | all 20 sheets, the `.srt`, the llm-rag README, single frames |
| director, part 2 (S09–S16) | 1 | 9 | 4 | sheets 020–039, single frames, a frame-difference motion check |
| newcomer, part 2 | 0 | 4 | 6 | sheets 20–39, the `.srt`, the ADK and module READMEs, about 30 frames |
| subtitles | 0 | 3 | 4 | every cue: 488 zh-en, 416 zh, 490 English, against the glossary |
| follow-ups | 0 | 1 | 0 | `QA_FOLLOWUPS.md` does not exist; rebuilt from PR #44's review-bot threads |
| ASR | 0 | 4 | 5 | base.en over the draft, large-v3-turbo on 42 clips, Kokoro G2P on every SAY |
| **total** | **2** | **27** | **29** | 36 scene, 9 subtitle, 8 narration, 5 shared-code findings |

**The two musts, and how each was fixed:**
- **S06, draft 11:10 (newcomer, fact):** the ▶ your-turn card told a viewer with a key to run the whole
  `--agent` command, but its GOLD cost line said "1 Gemini call · paid"; the run makes two Gemini calls
  and one embedding call, as S07 itself says. **Fix:** the line now reads "2 Gemini calls + 1
  embedding call per run · paid" (fixer, then the S06 verifier's wording); the "1 paid call" chip by
  the call strip, which counts the calls so far, is unchanged. Verified on fresh 720p frames; in the
  previous final cut the card shows it at *prev* 11:18.5 (`writer/clean_678.5_s06_turn_card.png`, read
  for this record).
- **S14, draft 26:53 (director, picture):** the GREEN "pending → approved" tag on line 61 was taller
  than a 20 pt code row, and its opaque box covered the tops of "↪ context.pending_proposal.copy()", the
  line the narration stresses. **Fix:** a local `row_tag()`, a dark pill 0.04 shorter than the row
  pitch with no outline, for both the full and the folded panel, with asserts that it stays between
  lines 60 and 61's second rows. Verified at 720p; in the previous final cut the `copy()` row is clear at
  *prev* 27:03 (`frames/zh_1623.png`, read for this record).

**The shoulds (27), all fixed:**
- **Follow-along:** S05's your-turn moment now shrinks the terminal to a strip and shows a GREY card
  with `sh docker-shell.sh`; S07 prints `head -4`'s lines (the old book's title); S02 and S14 (and S15,
  in the finishing pass) say where to open each notebook (course site or study guide; S01's "You need"
  card gained "three Colab notebooks · links in the study guide" in the finishing pass); S12's timeout
  tip names the `npx` command, and a chip warns that Ubuntu 22.04's apt Node (v12) is too old; S10's chip
  (QA round) and narration (finishing) say `uv run adk telemetry disable`.
- **Picture and pacing:** S07's unsent call 2 now stays unsent (a GREY dashed `recorded · the staff's
  call 2` envelope crosses instead); S08 names the two frameworks with chips ("OpenAI Agents SDK",
  "Microsoft Agent Framework"); S14 and S15 lowered the Colab frame so the tracker caption clears its
  tab; S14's plan card got its `recorded` tag and its emphasis now lands on "asks for a yes"; S13's
  trees stay up through the question with no empty frame; S10's undo output and the `--port 8080`
  success are held long enough to read; S16's Ctrl+C box is legible for about 2 s (S16 verifier: about
  1.9 s; on the previous cut's frames from *prev* 29:36.2 to 29:37.4, gone by 29:38.0,
  `verifier/sheet_s16_ctrlc.png`); S09 no longer brings the stale beat-4 `.env` rows back during `uv
  sync` (the follow-up watcher's Bugbot thread; checked on this cut, see "Re-check").
- **Subtitles:** `"mode": "ANY"` stays in one English cue (the director's and the subtitle watcher's
  findings); the `--load` command is no longer split in the Chinese tracks; S09's clause sits over its
  own English.
- **Narration:** the three lexicon readings and the recap line (gate 4).
- **Shared:** `Terminal.print(wrap=True)` folded words mid-word throughout; fixed in the finishing pass
  by a word-boundary wrap in `common.py` (below).

**The nits (29):** 27 fixed: S01's tag legend (now glossed), sample-command caption and MCP gloss; S04's
4.1 s still panel; S06's "the SDK ran nothing" caption; S07's `total_token_count` note; S08's two yellow
fills that hid their own words; S11's model tag; S12's scrambled three-plug morph and its `.adk` entry;
S14's finalize_plan/finalize_itinerary link; S16's `__pycache__` rows and `.venv` chip; five subtitle nits
(one a duplicate of the `"mode": "ANY"` should); two lexicon nits; and in the finishing pass the shared
wrap (two) and ▶-header repeats (two) and the two narration nits the QA text fixer had left ("ours
stopped", "dollars out of"). **Worked around:** the cue-timing nit (three cues that split a sentence with
a version number were 1.0–1.2 s off): the finishing pass split those sentences; the toolkit fix
(`explainer/build.py` `split_cues` weighting by spoken length) is deferred to the toolkit PR. **Partly
fixed:** S13's Guild tree beside the cell 68 panel (lines 1–8 show `mozzarella_tool`/`format_quiz` and
not `vegan_specialist`): a caption "Cheese Quiz Guild · 4 of its 6 tools" explains it; the panel itself is
unchanged because `script.md` fixes it at lines 1–8 and a folded 1–6, 8–11 panel needs about 14 rows.

**Verifiers:** 16 verifier reports (S01, S02, S04–S16, and one for the "tear down" lexicon in S08/S16;
S03 had no finding, and its Bugbot thread did not reproduce). Four verifiers also edited their scene:
S06 (the cost wording, and the timing of the "the SDK ran nothing" tag and caption), S11 (the moved tag's
swell left the safe area and touched the extra card; it now flares instead), S15 (an older overlap the QA
had not reported: a tag over line 116) and S16 (the timing after the shutdown box).

### Finishing pass (2026-10-21, 18 agents, commit `705f7f1`)

- **Shared `common.py` (one agent, then a verifier):** a word-boundary wrap for terminal output
  (`wrap_output`: 43 breaks in the dry runs, 37 at spaces and 6 after `,`, `/` or `-`, none mid-word),
  `turn_card(header=None)` as the default (one "your turn" per ▶ card), L05's scroll fix (leaving rows
  fade in place first), and sequential old-out-then-new-in swaps for the tracker, sections, lecture tags,
  container titles and gate labels; plus the critics' requests (`src_panel` colours a wrapped string as
  one, one bar per wrapped line, shorter time tags). The verifier dry-ran all 16 scenes with the old and
  new code: every voice-block start, play and end time identical.
- **Plan:** 14 text items, 6 scenes with items, 14 skipped with reasons (among them: no slide items,
  because the lecture tags are already in 14 scenes; the deferred toolkit items; the optional "OpenAI
  Agents SDK" SAY and S02 spoken line; S14's "checked state"/"a finalize tool" reductions, judged not worth
  a re-voice; S16's Ctrl+C output skipping lines 365–366 without a `…`, which a 3-row strip cannot show).
- **Text agent:** the SAY changes in gate 4, the `script.md` SHOW lines that had drifted from the
  scenes, `i18n/zh` g1/g2 and the glossary; `python -m explainer.i18n check` printed OK.
- **Scene agents and verifiers:** S01's eighth "You need" row (its verifier added a 1.0 s hold so the
  unspoken row can be read: S01 grew to 115.1 s); new anchors in S09, S10, S11 and S14 (S10's verifier
  split the "address already in use" flash onto the spoken words); S15's where-to-open caption (its
  verifier staged the caption's exit before cell 16 so they never overlap) and the "you and a friend"
  tag lifted off line 8's bar.
- **Sweep for L05's patterns** (copy flights over text, fills hiding their own label, double-exposed
  swaps): a dry-run analyser flagged 115 candidates; 87 were real, 82 fixed and 5 partly fixed or not
  fixed (S04's cards brushing the HTTPS label, and the S10 scroll at draft-chapter time 18:50, left
  because `_make_room` is shared code). The sweep verifier checked about 69 of the changes on fresh 720p
  previews, fixed 14 that were defective, 2 problems it found itself and 2 candidates the sweep had called
  "not real" (S09's ponder-card swap, S12's absorbed `{…}`), gave S04's cards their own lanes, and judged
  the S10 scroll not real ("the rows scroll in place"). The sweep's occlusion check also had hits in S03,
  S04, S06, S10, S11, S14, S15 and S16 that nobody looked at.
- **What the finishing reports left open:** S13's panel (above); S04's thin seam between adjacent line
  bars (`explainer/devops.py`, toolkit); S01's legend word "no key" against S06's "real run · no key";
  the tracker's harmless divide-by-zero warning; S10's ▶ card arriving about 1.4 s after "Pause" (a
  deliberate 1 s hold); S14's turnstile passing over "runs first" and "the human" for about 1 s during a
  move (about *prev* 27:19). The sweep restaged that move: frames of the previous cut at *prev*
  27:19.2–27:20.4 show the turnstile fading out at the corner and in at its destination, crossing neither
  label (`verifier/sheet_s14_turnstile.png`).

## Final-cut checks of the previous cut (1080p60, 2026-10-21)

Times in this section are in the previous cut (31:12.1). Its findings are items 1–29 below; fix round 1
fixed or decided items 1–18. Five agent checks, each from its own report:
- **Tags** (`report-tags.md`): all 29 `lecture_ref` tags leave before their scene ends, overlap nothing
  (10 fps box scan) and spell "slide"/"slides" correctly; 24 fade in with the picture they cite, three
  lead it by 1.0–1.4 s (item 24) and two swapped-in tags by about 1.4–2.7 s (items 7, 11); a 4 fps
  sweep of the top-right corner over the whole film found only the expected segments; every tag swap,
  measured frame by frame, ghosts at most 5.5 % while the other tag is visible (no double exposure). Two
  minor timing defects (items 7, 11), three long spans (items 8, 12, 14), small leads and tight
  placements (accepted, item 24). The review-bot list it was given was empty.
- **ASR** (`report-asr.md`): the narration is intelligible (gate 6); six weak spots (items 3–5, 23); no
  cue's speech starts more than 1 s late; the narration delay at scene joins (item 19).
- **Visual** (`report-visual.md`): 40 contact sheets (625 tiles, every 180th frame of the burned copy),
  plus strips and crops at doubtful moments. No blocking defect: nothing clipped or outside the frame, no
  black or missing scene, no garbled glyphs, no tag stuck between scenes, every scene starts and ends on
  an empty frame. One real minor render defect (item 9) and five brief transient overlaps (items 15–18),
  two holds just over 4 s (items 10, 13), one glitch-looking row that is authentic (item 21), three
  sub-second effects (item 22) and the two subtitle pairings of items 1–2.
- **Pairs** (`report-pairs.md`): all 489 bilingual cues read in full; no meaning swaps between a Chinese
  line and its English, or between neighbouring cues; every condition and time clause in the same cue as
  its partner; no command, path, flag or placeholder split across a line or cue in the zh-en and zh
  tracks. Two minor pairing blemishes (items 1–2) and three commands broken across lines in the
  English-only `.srt` (items 6, 20). The one-word overhang at zh-en #247/#248 (15:26–15:30, "runs" / 跑)
  is noted as not a defect.
- **Measured** (`report-measured.md`, `measured.json`): every measured check passed; no defects, a few
  observations (item 25).

**Where the checks disagree** (neither is a defect):
- **Widest subtitle line.** The visual check gives 1526 px (the English line at 14:07.09) of 1840 px
  usable; the measured check gives 1062 px at 848 s (x 428–1489, libass render, cross-checked on burned
  frames). Its burned frame at 14:08 (`measured/frame-zhen-t848-widest-caption.png`, read for this
  record) shows that English line spanning about x 428–1490, so this record uses the measured figure.
  Both checks agree the line fits. (The re-check measures the same widest line, 1062 px at 848 s.)
- **S03's "Spot it" card.** The measured check counts it as "no timer" (as `script.md` says); the visual
  check lists 04:46.5–04:51.5 among the timed stretches, because a line draws under the card for 4 s
  (`s03_envelope.py`, `Create(uline)`, 4.0 s). Gate 3 counts five ponders.

## Re-check of the re-stitched cut (2026-10-27)

Three agent checks of `6311d49`'s outputs, each read in full for this update; nothing tracked was
modified and nothing re-rendered:
- **Measured** (`recheck/measured.json`; its key `changed_vs_final_review` lists 137 changed figures):
  every measured check passes; all four MP4s decode in full; every true peak is at or below −1.5 dBTP
  (gate 6, "Verified"). Observations: S10 grew by 1.850 s (not the ~2.4 s first estimated), S06 by
  0.283 s and S15 by 0.583 s, 2.716 s in all; `README.md` still quoted the previous cut and its S11–S16
  chapter times (`recheck/readme_check.json`; fixed in this update); zh-en #293 shows the command alone on
  both lines (item 25).
- **ASR** (`recheck/asr-summary.json`): the four reworded sentences are heard as written (items 3–6); no
  cue's speech starts more than 1 s after its cue; 491 cues compared, 213 differing as before, the
  turnover recogniser noise (gate 6); one minor new timing finding (item 30).
- **Changed scenes** (`recheck/finalcut/`): every fix of the ten re-rendered scenes is in the cut (items
  under "Fixed"); the tags enter and leave with their pictures; no new overlap; every changed scene's
  last state before its fade carries no tag (`recheck/finalcut/lastframes_prefade.png`) and its last
  frame is empty; the subtitle changes P1, P2 and T1–T4 are in all three tracks; burned subtitles cannot
  cover the picture (the zh-en burn scales the picture to rows 0–937 and draws the subtitles in the band
  below; the `.ass` has 487 events in one style with no `\pos`, `\an` or `\move` override). Nothing to
  send back.
- **Review bots:** the list given to the checks was empty. PR #44 carries three Cursor Bugbot threads,
  all from 2026-10-20 and all still unresolved on GitHub; two are on L06 and were checked on this cut for
  this update:
  - **S09 "Stale terminal lines during uv sync"** (`s09_adk_setup.py`): **verified fixed.** The QA round
    fixed it; S09 was not re-rendered since. At 17:12.0 the laptop terminal returns empty, and at
    17:16.0 it shows only `uv sync` and its output, with no `.env` rows above (`recheck/bots/clean_1032.0.png`,
    `clean_1036.0.png`; `clean_1047.0.png` at 17:27.0, the error).
  - **S03 "Target stroke hits live sheets"** (`s03_envelope.py`, the beat-7 move): **verified not
    reproducing.** The two sheet frames are red as the envelope starts to move (04:57.6, stroke pixels
    about RGB 234/106/93, the RED `#FC6255`; `recheck/bots/clean_297.6.png`) and after the move they are
    GREY and PINK (04:59.5, about 140/140/148 and 224/146/173, `#8A8F98` and `#F28FB5`;
    `recheck/bots/clean_299.5.png`), so the red does not come back.
  - The third thread is on L05 (`videos/ac215-l05-rag/scenes/s16_recap.py`). No bot thread is newer
    than 2026-10-20.

## Items

Fix round 1's plan (`/root/ac215-backup/args/l06-fix1.json`) is the coordinator's; its IDs are in
brackets. Items 1–18 were open for that round: 17 are fixed and one optional item (10) was left as it
is. Items 19–24 are the plan's `accepted` list. For items 25–29 the coordinator decided after the
review: 25, 26 and 29 accepted as recorded, 27 and 28 fixed. Item 30 is new in the re-check.

### Fixed in fix round 1 (`980d756`; re-rendered and re-stitched in `6311d49`)

Times are in the re-stitched cut; *prev* marks where the defect was in the previous cut. Each fix was
also checked by the fix round's verifier on a fresh 720p render (reports named above).

**Subtitle text** (`i18n/zh/narration/g1.yaml`):

1. **[P1] S04, zh-en #84, 05:32.250–05:37.029: fixed.** One cue, 在 llm-rag 里，Agents 一节就是菜单只有两项的
   Agentic RAG, over the whole English sentence "llm-rag's Agents section is Agentic RAG with a menu of
   two." (*prev* two cues #84/#85 with the English repeated). The text agent kept 菜单 (29.4 units, inside
   the 30-unit band) instead of the planned wording. `.zh.srt` #69 is one cue as well. Evidence:
   `recheck/subtitle_items.json` ("P1").
2. **[P2] S05, zh-en #141–#142, 09:07.643–09:15.025: fixed, with one side effect.** 我们没有密钥 pairs
   with "We had no key," and 所以 embed 用的是课程团队 commit 过的 embedding with "so the staff's committed
   embeddings stood in for the embed step." (#142, 09:11.244–09:15.025; *prev* #143/#144 with the English
   repeated). Because 我们没有密钥 lasts 0.82 s, the build merges it into the cue before: #141
   (09:07.643–09:11.244) reads 否则就重新分块、向量化、加载。我们没有密钥 over "Otherwise, chunk, embed and load
   again. We had no key,". Both lines say the same thing in the same order, but "We had no key," shows
   about 2.8 s before it is spoken (the English `.srt` has it in #147, from 09:10.417); the fix round's
   text verifier left it as the reviewer-tested wording (item 30). `.zh.srt` keeps the sentence in one
   cue, #120 (09:10.417–09:15.025). Evidence: `recheck/subtitle_items.json` ("P2").

**Narration** (each re-voiced its scene; every `wait_until` anchor still occurs):

3. **[T1] S15, `.srt` #450, 28:46.551–28:49.452 (*prev* #449, 28:44.4): fixed.** SAY[2] now says
   "Then send email wrote the HTML to a file." (was "…saved the HTML."); subtitles "Then send_email wrote
   the HTML to a file." and 然后 send email 把 HTML 写进了一个文件. Both models hear "Then send email, wrote
   the HTML to a file."; large-v3-turbo gives "wrote" 0.995 and 0.997 probability (0.3 s and 2 s of
   context). The send_email row and "Saved HTML" appear while "wrote the HTML to a file" is said
   (28:47.45–28:48.65), and the next change lands on "That run had four readers" (28:49.77). S15 grew by
   0.583 s. Evidence: `recheck/clips/s15_cues450_pad0.3_1726.25-1729.75.wav`,
   `recheck/asr-large-sentences.json`, `recheck/finalcut/s15/sheet.png`, `f_28m47.20_s033.000.png`,
   `f_28m48.80_s034.600.png`.
4. **[T2] S10, `.srt` #313–#314, 19:49.051–19:55.878 (*prev* #313, 19:47.8): fixed.** SAY[7] now says
   "The log says it loaded the dot env at the repository root, and found the root agent in baseline dot
   agent." (was "…the root dot env file…"); subtitles "The log says it loaded the .env / at the
   repository root," (#313) and "and found the root_agent in baseline.agent." (#314), Chinese 日志说它加载了
   repo 根目录下的 .env. Both models hear "…loaded the .env at the repository root and found the root
   agent in baseline.agent."; "root.n file" is gone (base.en's "and and" is one word counted in both
   cues at the #313/#314 join). The PINK box and "the root .env" tag arrive at 19:49.95–19:50.55 and
   `baseline.agent` turns GREEN at 19:52.85, on their words. Evidence:
   `recheck/clips/s10_cues313-314_pad0.3_1188.75-1196.18.wav`, `recheck/asr-large-sentences.json`,
   `recheck/finalcut/s10/sheet_chip_log.png`, `f_19m50.22_s090.500.png`, `f_19m53.32_s093.600.png`.
5. **[T3] S06, `.srt` #170, 10:29.511–10:31.727 (*prev* 10:29.5): fixed** by the fix round's text
   verifier after the text agent had left it (Kokoro's phonemes matched the four good cues and the speed
   did not differ, so the plan's "leave it" condition did not hold). SAY[4] now says "…both declarations
   with the enum, mode ANY and temperature zero." (was "…mode ANY, temperature zero."); subtitle
   '"mode": "ANY" and temperature zero.'. Both models hear "mode any and temperature zero" (large-v3-turbo:
   "mode" 0.93, "any" 0.93 with 0.3 s of context); "modini" is gone. The highlights: enum at 10:28.75
   (large-v3-turbo puts the word at 10:29.17), `"mode": "ANY"` at 10:29.73 (10:29.89), temperature at
   10:30.60 (10:30.63). S06 grew by 0.283 s. Evidence:
   `recheck/clips/s06_cues169-170_pad0.3_625.41-632.03.wav`, `recheck/asr-large-sentences.json`,
   `recheck/finalcut/s06/strip_highlights.png`, `f_10m28.65_s052.000.png`, `f_10m29.35_s052.700.png`,
   `f_10m30.10_s053.450.png`.
6. **[T4, optional] S10, `.srt` #294–#295, 18:39.799–18:46.263 (part 2 `.srt` #46–#47; *prev* #295,
   18:41.0): fixed.** SAY[1] now says "Answer as you like; change it later with this command: uv run ADK
   telemetry disable."; the English `.srt` shows "Answer as you like; / change it later with this
   command:" (#294), then "uv run adk telemetry disable." on its own (#295, 18:44.004–18:46.263).
   Large-v3-turbo hears "…change it later with this command. UV run ADK telemetry disable." (base.en's
   "run run" is one word counted in both cues at the join). The `uv run adk telemetry disable · change it
   later` chip is up from 18:41.33 and while the command is spoken (18:44.22, 18:45.92). Side effects: the
   zh-en #293 now shows the command on both lines (accepted, item 25), and "uv run" is heard about 0.39 s
   before #295 appears (item 30). With T2, S10 grew by 1.850 s. Evidence:
   `recheck/clips/s10_cues294-295_pad0.3_1119.50-1126.56.wav`, `recheck/asr-large-sentences.json`,
   `recheck/subtitle_items.json` ("T2 + T4"), `recheck/finalcut/s10/f_18m41.62_s021.900.png`,
   `f_18m44.22_s024.500.png`, `f_18m45.92_s026.200.png`.

**Scenes** (each scene's length is unchanged unless its narration changed):

7. **[S08] "slide 41": fixed.** The tag now fades in with the anatomy at 14:50.25–14:50.85 (*prev* from
   14:49.0, over the max-turns picture); there is no tag at 14:49.28 (the max-turns picture fading) or
   14:49.98, and it leaves with the anatomy at 14:59.63–15:00.13. Evidence:
   `recheck/finalcut/s08/sheet_41.png`, `f_14m49.28_s079.600.png`, `f_14m49.98_s080.300.png`,
   `f_14m50.53_s080.850.png`, `f_14m59.88_s090.200.png`.
8. **[S08] "slides 35–40": fixed by shortening it.** The tag stays over the hub and its unrolling into
   the loop track, because the SHOW line before that SAY puts both under LECTURE 35–40 (and `SLIDES.md`:
   slide 39 draws the cycle), and fades at the start of the next SAY, the stop rule (14:16.88–14:17.28;
   up at 14:16.58, gone at 14:17.48). *Prev* it stayed to 14:49.0 over the stop rule, `runner.py` and the
   cap chips. Loose end, not changed: `script.md`'s SHOW line for the stop-rule SAY does not say "The
   lecture tag leaves" (the S08 verifier's note). Evidence: `recheck/finalcut/s08/sheet_3540.png`,
   `f_14m16.58_s046.900.png`, `f_14m17.08_s047.400.png`, `f_14m17.48_s047.800.png`.
9. **[S08] "plain text" chip and the exit arrow: fixed.** The chip keeps `reply_card()`'s place above
   the arrow (moved 0.25 right) and has an opaque backing while the gate passes it: from 14:20.28 to
   14:23.88 no line crosses its text, and the gate posts pass behind it (14:22.58). Evidence:
   `recheck/finalcut/s08/strip_chip.png`, `strip_chip_wide.png`, `f_14m20.28_s050.600.png`,
   `f_14m22.58_s052.900.png`, `f_14m23.88_s054.200.png`.
11. **[S12] "slide 53": fixed.** "slide 52" stays through the red ripple (which now starts 0.4 s
    earlier, with "Every tool becomes a custom integration") and the pause (22:40.65, 22:42.35) and fades
    during the MCP morph (22:43.10); neither tag is up at 22:43.40 and 22:43.60; "slide 53" fades in with
    the trunk (22:43.95) and leaves with its picture at 23:01.40–23:02.00. It never sits over the
    slide-52 picture (*prev* from 22:38.25, about 2.7 s early). Evidence:
    `recheck/finalcut/s12/sheet_53.png`, `f_22m42.35_s029.200.png`, `f_22m43.40_s030.250.png`,
    `f_22m43.95_s030.800.png`.
12. **[S07] "slide 39": fixed.** The tag fades with the "interpret its outputs" duty chip at
    12:24.93–12:25.63 (*prev* it stayed to 12:49.6); no tag over the staff's answer panel (12:27.95,
    12:33.45), the hook-answer card (12:39.95) or the start of SAY[8] (12:50.15, 12:50.45), and none
    flashes back. Evidence: `recheck/finalcut/s07/sheet_tag.png`, `f_12m24.75_s063.300.png`,
    `f_12m25.75_s064.300.png`, `f_12m39.95_s078.500.png`, `f_12m50.45_s089.000.png`.
13. **[S14, optional] the end-of-scene hold: fixed, differently from the plan.** Instead of trimming
    the 2 s hold `script.md` asks for, the ▶ tag of the last your-turn card pulses once at "pause, and
    run the four turns" (28:09.23–28:09.83, largest at 28:09.54; one new anchor). The longest still
    stretch fell from 4.75 s (*prev* 28:06.5–28:11.25) to about 3.6 s (28:09.83 to the fade at 28:13.42).
    The "slides 36–37" tag leaves with its picture at 28:07.48–28:07.98. Evidence:
    `recheck/finalcut/s14/sheet_end.png`, `f_28m09.54_s112.370.png`, `f_28m14.19_s117.020.png`.
14. **[S04] "slides 8–14": fixed.** The tag fades with the six-box column as it becomes llm-rag's two
    menu cards (05:33.05–05:34.05; *prev* it stayed to 05:44.3); no tag at 05:34.10, 05:38.85 or
    05:43.85. The fix round's verifier noted that L05's slide-8 strip stays about 4 s after the tag
    leaves (the harmless direction; left). Evidence: `recheck/finalcut/s04/strip_tag_tr.png`,
    `sheet_tag.png`, `f_05m32.75_s018.900.png`, `f_05m34.10_s020.250.png`, `f_05m43.85_s030.000.png`.
15. **[S04] cards over "Gemini / location global": fixed.** Both cards now fade in just above the Gemini
    chip, in the cloud's top bump: the `{name, args}` card at 07:20.33 and the reply-lines card at
    07:26.80 (*prev* over the label at 07:20.0–07:20.8 and 07:26.8–07:27.6); the label stays clean
    through both fades and flights. Evidence: `recheck/finalcut/s04/strip_cards.png`,
    `f_07m20.45_s126.600.png`, `f_07m26.90_s133.050.png`, `f_07m27.20_s133.350.png`.
16. **[S10] the swap at "The log says": fixed.** It is now sequential, 0.5 s in all: the old panels fade
    out at 19:49.15–19:49.40 (the second terminal's text first, then its frame); at 19:49.42 only the
    laptop strip is left; the terminal grows and the "this video: baseline, mcp_tools" card fades in
    under the tracker at 19:49.40–19:49.65. At no frame are two texts readable at once (*prev* double
    exposure at 19:47.85–19:48.35). Evidence: `recheck/finalcut/s10/sheet_swap.png`,
    `f_19m49.22_s089.500.png`, `f_19m49.42_s089.700.png`, `f_19m49.58_s089.860.png`,
    `f_19m49.82_s090.100.png`.
17. **[S02] the diamond: fixed.** Lane 2's diamond pulses in place (03:05.77–03:05.97) while the small
    diamond fades in at the right end of the gpt-4o pill, in one 0.8 s step (03:05.57–03:06.37); nothing
    crosses "your Python decides the order" or the "o" of gpt-4o. The fix round's verifier noted that at
    the pulse's peak the diamond's tip touches its own arrow for about 0.2 s (no text involved). Evidence:
    `recheck/finalcut/s02/strip_diamond.png`, `f_03m05.77_s070.670.png`, `f_03m06.17_s071.070.png`.
18. **[S03] the role labels: fixed.** Both swaps (04:52.48–04:53.38, which had the same crossing, and
    04:56.47–04:57.37) now fade the old labels out, leave both rows empty for a moment (04:52.92,
    04:56.94) and fade the new ones in; the labels never cross, and both end states are unchanged.
    Evidence: `recheck/finalcut/s03/strip_swap_b6.png`, `strip_swap_b7.png`, `f_04m52.92_s063.600.png`,
    `f_04m56.94_s067.620.png`.

### Accepted (the coordinator's decisions)

Item 10 was left as it is in fix round 1 (optional); items 19–24 are the plan's `accepted` list, with
the plan's reason; items 25, 26 and 29 were accepted as recorded after the review.

10. **[S08, optional] 15:19.3–15:23.8: the end-of-scene your-turn hold ("exit / docker compose down") is
    still frozen about 4.5 s** (*prev* 15:19.0–15:23.5), 0.5 s over the 4 s limit; narration ends at
    15:21.5. **Reason:** `script.md` asks for a 2 s hold, and 2.2 s of the frozen stretch has narration; a
    deliberate "pause and do it" hold (QA's part-2 director also called such holds deliberate).
    Evidence: `recheck/finalcut/s08/f_15m18.18_s108.500.png`, `f_15m21.68_s112.000.png`,
    `f_15m23.68_s114.000.png`; *prev* `sheets/static-scan.txt`, `sheets/freezes-clean.txt`.
19. **Narration plays behind the subtitles and pictures, by an amount that grows at each scene join.**
    In the previous cut, constant within a scene: +47.5 ms in S01, then 62.5, 65, 75, 77.5, 80, 97.5,
    97.5, 100, 115, 132.5, 147.5, 155, 162.5, 165 and +167.5 ms in S16; the zh-en copy identical; the
    parts restart at +47.5 ms (part 1 to +97.5, part 2 to +115). Re-measured on this cut at 10 ms
    resolution: +0.05 s in S01, +0.08 s in S06, +0.11 s in S10, +0.15 s in S15 and +0.16 s in S16 (the
    same method gave +0.18 s for S16 of the previous cut; `recheck/asr-summary.json`, "onset"). The
    visible effect is that word-anchored highlights in S11–S16 land about 0.1–0.15 s before their word.
    **Reason:** a toolkit issue (`explainer/build.py` joins the scenes' AAC audio with the concat demuxer
    without trimming each segment's 1024-sample encoder lead-in; the model predicts every step within
    2.5 ms), task #15, affecting every episode stitched this way; below the ITU-R BT.1359 limit for late
    audio (about 185 ms); not fixable inside L06. Evidence: `lag.log`, `lag-parts.log` (*prev*, ASR §5).
20. **The English `.srt` breaks the two 47-character commands:** cue 139 (08:43.5, "python cli.py --agent
    / --chunk_type char-split.") and cue 149 (09:17.0, the same for `--load`) against a 44-character
    line. **Reason:** toolkit (`explainer/subtitles.py`, `_two_lines` / `_reflow_en`), task #15; the
    burned zh-en asset is unaffected (pairs F3).
21. **S07, about 12:54–13:06: the "Soča" row of the `out.txt` word-count table sits one column left.**
    **Reason:** authentic: `assets/terminal/laptop/10-x-old-words.txt` shows the same, because bash
    `printf %-18s` pads by bytes and "č" is 2 bytes. Evidence: `frames/crop_s07_soca_row_13m00.png`
    (*prev*; visual item 7).
22. **Sub-second effects:** 01:12, the highlight pulse scales "built, not sent" until it touches its pill
    outline; 28:38.1, the frame border shows through the "recorded · the staff's last saved run" tag as it
    fades in; 14:14.8–14:16.2, "decision maker" visibly morphs into "model". **Reason:** too small to cost
    a re-render. Evidence (*prev*): `frames/crop_legend_built_not_sent_1m12_1m13.png`,
    `frames/strip_s15_recorded_tag_28m36.png`, `frames/zh_855.png` (visual item 9).
23. **The remaining ASR weak spots:** "transhumance" heard "transhumans" (cues 202 and 209, 12:26.5 and
    12:49.9; the narration defines it at once), "comes from checked state" heard "check state" (cue 432,
    27:42.6), "a finalize tool" heard "a finalized tool" (cue 414, 26:28.7). **Reason:** the subtitles and
    the screen carry the exact words; no change. The finishing plan had already skipped the last two, for
    a different reason: consonant reductions with the meaning intact by ear, not worth re-voicing S14.
    These sentences' audio is unchanged in this cut (the same narration re-encoded). Evidence (*prev*
    cue numbers): `clips-wide/cue202_744.21-751.25.wav`, `clips-wide/cue431_1658.45-1666.10.wav`,
    `clips/cue413_1586.31-1590.84.wav`, `compare-large.txt`.
24. **Tag leads under 1.5 s and tight placements:** S01 "slides 20–22" leads its card by 1.4 s from
    00:27.75 (`script.md` puts the tag first), S02 "slides 16–18" by 1.35 s from 02:35.9, S04 "slides
    8–14" by 1.0 s from 05:13.9; the S07 duty chip sits 5 px below its tag (by design), the S16 anatomy's
    top edge 8 px below "slide 41" and "slides 32–33" (x ≈ 1456–1756), S01's caption 7 px below its tag.
    **Reason:** the plan accepts them as they are; none overlaps.
25. **Measured observations (information; accepted as recorded):** in zh-en cues #23 (01:31.357,
    「Docker、Chroma、uv」) and #293 (18:43.977, *prev* #295 at 18:42.535) the top line has no Chinese
    character (both cues have two lines, so `tools/release_episode.py`'s check, which counts lines,
    passes). Since T4, #293 reads "uv run adk telemetry disable" over "uv run adk telemetry disable.", so
    the burned copy shows the same command twice (it used to read "… / with uv run adk telemetry
    disable."); **accepted by the coordinator:** a command-only cue keeps the command verbatim in both
    lines (glossary rule). The zh-en copy has one more video frame than the clean cut (112,488 against
    112,487, 16.7 ms), added by the burn; the narration starts at 0.000 s with no lead-in (each scene's
    voice starts 0.1–0.3 s after its cut); the part videos carry no burned subtitles (only the full zh-en
    copy does); the audio language tag is "und"; the video bitrate is about 0.29 Mbps at 1080p60.
26. **Near-still stretches (information; accepted as recorded):** besides items 10 and 13, three
    stretches move only very slightly (fewer than 50 changed pixels in a 480×270 sample): 10:56.5–11:01.8
    (S06, under narration), 24:28.9–24:32.9 (S12 your-turn card) and 30:52.7–30:57.0 (S16 recap question
    3). Measured on the previous cut (`sheets/static-scan.txt`, visual item 6); the times are converted,
    not re-measured.
29. **Smaller nits left by QA and finishing (accepted as recorded;** none re-checked one by one on the
    final frames): S13's Guild panel (partly fixed, see QA); S04's thin seam between adjacent line bars
    (toolkit); S01's legend word "no key" against S06's "real run · no key"; S10's ▶ card about 1.4 s
    after "Pause" (deliberate); S16's Ctrl+C output skipping lines 365–366 without a `…` (follows
    `script.md`); the tracker's divide-by-zero log warning; the S10 terminal scroll the sweep called real
    and its verifier not real (the previous cut's visual check did not flag it).

### Fixed outside the fix round

27. **README text:** `README.md`'s chapter-10 summary and its errata paragraph gave the bare `adk
    telemetry disable`, which the QA's part-2 newcomer found fails outside the project's environment;
    the video, `script.md` and the glossary say `uv run adk telemetry disable`. Both README places say
    `uv run adk telemetry disable` (fixed in the 2026-10-23 verification, commit `2b05085`).
28. **Release prerequisites:** `video.yaml` has its `publish:` block (added in `2b05085`), which
    `tools/release_episode.py` reads and the legacy release workflow checks before rendering
    (`docs/PUBLISHING.md`). The coordinator decided that this record needs no `QA_FOLLOWUPS.md`: the
    review-bot threads are recorded under "Re-check" (both L06 threads checked on this cut).

### Open (new in the re-check, no decision recorded)

30. **Two subtitle timing side effects of fix round 1 (information):** (a) S10, `.srt` #295 (18:44.004):
    "uv run" is heard about 0.39 s before the line "uv run adk telemetry disable." appears, so it plays
    under "…with this command:"; the split point is interpolated, with no word mark inside the sentence.
    Eight mid-sentence joins already in the cut do the same, by 0.35–0.75 s (cues 16, 157, 267, 287, 323,
    373, 414, 474); the ASR re-check calls it not a gate issue, and the command chip is on screen from
    18:41.33 (`recheck/joins.json`). (b) S05, zh-en #141 shows "We had no key," about 2.8 s before it is
    spoken (item 2).

## Verified (re-stitched cut, `6311d49`; re-check 2026-10-27)

- **Files** (`recheck/measured.json`): all four MP4s decode in full with no error (`ffmpeg -v error`, exit
  0; `recheck/decode-*.log`). 1920×1080 at 60 fps, H.264 High, yuv420p; AAC-LC 48 kHz stereo; `moov`
  before `mdat` in all four.

  | file | duration | frames | size | video kbps |
  |---|---|---|---|---|
  | `ac215-l06-agents-1.mp4` | 1874.889 s (31:14.9) | 112,487 | 107.0 MiB | 293.1 |
  | `ac215-l06-agents-1.zh-en.mp4` | 1874.889 s | 112,488 | 105.3 MiB | 285.9 |
  | `_part1.mp4` | 924.655 s (15:24.7) | 55,475 | 51.7 MiB | 283.6 |
  | `_part2.mp4` | 950.235 s (15:50.2) | 57,012 | 55.2 MiB | 302.3 |

  The video streams of the two parts sum to 1874.783 s, exactly the clean cut's video stream and the
  sum of the 16 scene stitch inputs; their frames sum to 112,487. The ten re-rendered stitch inputs date
  from 2026-10-24 and each matches its sidecar's duration. Against the previous cut: S06 104.517 →
  104.800 s, S10 123.117 → 124.967 s, S15 81.383 → 81.967 s, the other 13 scenes unchanged; the cut is
  2.716 s longer, S07–S10 start 0.283 s later, S11–S15 2.133 s and S16 2.717 s.
- **Loudness** (EBU R128, true peak): −16.1 / −16.1 / −16.0 / −16.1 LUFS, LRA 2.4 / 2.4 / 2.3 / 2.5 LU,
  true peak −2.7 / −2.7 / −2.7 / −2.8 dBTP (clean, zh-en, part 1, part 2; `recheck/ebur128-*.log`). The
  zh-en audio is a straight copy of the clean cut's (identical audio stream MD5,
  `94d30dd3f0fec89d531d9a84797ccf16`).
- **Subtitles** (all nine files): numbered in order, sorted, inside the runtime, never overlapping or
  empty, none under 0.8 s (shortest 1.000 s English and Chinese, 1.358 s zh-en), at most two lines,
  Chinese always above English. Cue counts: full 491 / 417 / 487, part 1 248 / 207 / 243, part 2
  243 / 210 / 244 (`.srt` / `.zh.srt` / `.zh-en.srt`); the parts add up to the full counts and part 2's
  cues are the full cut's shifted by 924.583 s (±1 ms), with identical text. Each `.zh-en.ass` matches its
  `.zh-en.srt` (487 / 243 / 244 events, 0 mismatches). The last cue ends at 31:12.744, 2.145 s before the
  end; reading speed peaks at 4.58 words/s (English) and 7.81 characters/s (Chinese). The 762 distinct
  characters are the same set as in the previous cut's tracks, all of which rendered in Noto Sans CJK SC
  (the previous visual check). Every fix-round subtitle item (P1, P2, T1–T4) is in all three tracks
  (`recheck/subtitle_items.json`).
- **Burned layout:** the picture is scaled to 1670×938 at the top and every cue is one Chinese line (50
  px) over one English line (33 px) in the band below (`WrapStyle: 2`); in the previous cut, spot frames
  at commands (`python cli.py --load`, `docker compose down`, `ls -a`, `uv run adk web --port 8080`, the
  MCPToolset code) showed every command fully visible (`sheets/subtitle-spotcheck.txt`); in this cut the
  `.ass` has one style and no position overrides, and the glyphs on 14 burned frames at the fix moments
  sit in rows 992–1062 (changed-scene check).
- **Chapters:** `chapters.txt` has the 16 titles of `video.yaml` in order, each at the true scene start
  rounded down to the second (up to 0.90 s early, S13); `chapters_part1.txt` and `chapters_part2.txt`
  follow the same rule (part 2 measured from 924.583 s). Against the previous cut, S11–S16 moved from
  20:22 / 22:11 / 24:31 / 26:15 / 28:12 / 29:33 to 20:24 / 22:13 / 24:33 / 26:17 / 28:14 / 29:36, and part
  2's last six from 04:58 / 06:46 / 09:07 / 10:50 / 12:47 / 14:09 to 05:00 / 06:48 / 09:09 / 10:52 / 12:49
  / 14:11; part 1 is unchanged. The README's two chapter blocks equal `chapters.txt` and
  `chapters_part2.txt` (part 1 is the first eight lines), updated and checked for this record.
- **Scene boundaries:** the first and last frames of all 16 scenes are empty background (no pixel above
  60, maximum grey 14–16; `recheck/scene-ends.txt`); no tag crosses a scene boundary (previous cut's tags
  sweep; for the ten re-rendered scenes, `recheck/finalcut/lastframes_prefade.png`).
- **Narration against the script:** 153 SAY lines and 4,307 words in `script.md`, the same in the 153
  render voice blocks; 679 `wait_until` anchors; no "anchor not found" and no translation warning in the
  16 render logs (`recheck/render_logs.json`).
- **Ponders and recap:** five ponder cards with timers of 8, 8, 6, 6 and 8 s, silent during the timer
  (momentary loudness at most −136.3 / −132.3 / −131.1 / −129.3 / −129.1 LUFS); the recap and test
  questions in S16 (gate 3).
- **Lecture tags:** 29 tags across 14 scenes; in the previous cut no tag overlapped anything and no swap
  was double-exposed (tags check); the five tags fix round 1 changed now enter and leave with the
  pictures they cite, with no overlap (items 7, 8, 11, 12, 14).
- **Defect patterns from L05:** in the previous cut no fill hid its own label in the dense frames checked
  at full size (the your-turn cards, the PENDING stamps at *prev* 26:51 and 27:03, the sticky note at
  *prev* 29:12) and no tag swap was double-exposed; the copy flights and overlaps it left (items 9 and
  15–18) are fixed in this cut.
- **QA's must fixes:** on the previous cut's frames, the S06 card's cost line (*prev* 11:18.5) and the
  clear `copy()` row (*prev* 27:03) (QA section); fix round 1 changed S06 only in item 5's sentence and
  S14 only by item 13's pulse.
- **Recorded and no-key steps are labelled on screen** (previous cut's visual check; times converted):
  "recorded · the staff's run, September 22, 2026" (12:30), "recorded · the staff's last saved run"
  (25:23, 26:35, 28:38), "at the time of recording", and "built, not sent", "no key" and "stand-in" on the
  steps run without a key; the QA's part-2 director found a "recorded", "with your key" or "illustration"
  label on every step that needs a key.
- **Bilingual pairs:** the previous cut's pairs check read all 489 zh-en cues (no meaning swap; no
  command, path, flag or placeholder split across a line or cue in the zh-en and zh tracks). 479 of the
  487 zh-en cues of this cut have the same text as before (`recheck/text_diff_vs_prev.json`); the other
  eight are the P1, P2 and T1–T4 cues, read in the re-check (items 1–6, 25).
- **Review bots:** both L06 Bugbot threads on PR #44 checked on this cut (S09 fixed, S03 not
  reproducing; "Re-check").
- **Provenance** (`ASSETS.md`, not re-run here): every terminal panel prints from real captures of
  2026-10-18 (Docker Engine 29.8.2, Compose v5.6.0, uv 0.13.1, Python 3.12.15 in the container; ADK
  2.12.0, CPython 3.15.0 then 3.13.16, Node.js v24.22.0 on the ADK laptop), including the two requests
  google-genai built and printed but never sent, the failing `uv sync`, the refused folder names, both
  MCP servers and the port clash. Model answers are the staff's saved outputs (`out.txt` of 2026-09-22;
  the notebooks' saved cells), tagged `recorded`. The GCP console, Vertex AI answering, AI Studio, the
  ADK dev UI, Colab's menus, the quiz widget, the newsletter preview and the hosted Cheese Agent Tool
  page are schematic drawings tagged `illustration`.

## Not claimed

- **No human listened to or watched this cut.** The listening sign-off is waived for the series (gate
  6); the ASR round trips are a machine substitute. The QA's simulated viewers and every check above are
  agents working from contact sheets, single frames, audio clips and subtitle text.
- **The Chinese subtitles were reviewed by agents only:** the QA's subtitle watcher read every cue of
  the draft against the glossary, the pairs check read all 489 zh-en cues of the previous cut, and the
  re-check read the eight changed ones. No human translator or native proofreader has read them. The
  `.zh.srt` track was checked mechanically and for split commands, not re-read for meaning.
- **Steps the captures could not run** (`ASSETS.md`, "Not captured"): every Vertex AI and Gemini call
  (both `--agent` calls, and `--embed`, for which the staff's committed embeddings stand in;
  `GCP_PROJECT` is a placeholder and `secrets/` was empty); the AI Studio key (the one request that
  reached Google carried the placeholder key and was refused); chatting with the ADK agents; ADK modules
  2, 4, 5 and 6; all three Colab notebooks (OpenAI). They are shown from the staff's saved outputs, the
  real printed requests and illustrations, and no claim is made that they behave the same with a key
  today.
- **Docker Hub and the capture machines:** the base image was rebuilt locally with the recording proxy's
  CA (a student's first build also pulls it; no pull is shown), Docker Hub images came through
  `mirror.gcr.io`, and the Chroma server's version was not recorded. The laptops are containers (a
  `docker:29.8.2-dind` engine, a `debian:12` box), not Docker Desktop or a Mac; the ADK capture used
  CPU-only PyTorch (a student sees 189 packages and about 3 GB of CUDA packages on a Linux PC); its
  telemetry question was answered "n".
- **What the checks did not cover:** the previous cut's visual check sampled one frame every 3 s plus
  strips at doubtful moments, so a transient shorter than that may be missed; the QA and sweep fixes were
  not each re-verified on the final frames (only through that sampling, the targeted strips and the
  frames named above); only the burned zh-en copy was read tile by tile: the clean cut was viewed
  through the tags check's frames and a few single frames, and the part MP4s were probed, decoded and
  loudness-measured but viewed at one frame each (in this cut, not viewed); the sweep's occlusion hits in
  eight scenes were never looked at; nobody checked `exercises.md`, `transcript.md`'s wording or the
  study guide in this review; the narration-delay cause (item 19) is a model that fits the measurements,
  not a toolkit change tested here. In the re-stitched cut, the changed-scene check viewed only the ten
  re-rendered scenes (contact sheets every 2 s of the burned copy and frames at each fix); the six
  unchanged scenes (S01, S05, S09, S11, S13, S16) reuse the 2026-10-21 stitch inputs and were checked
  through their first and last frames, the measured and ASR checks and, for S09, the bot-thread frames.
  Times carried over from the previous review are converted by the scene shifts, not re-measured, and
  the gate-2 and item times inside the re-rendered scenes that no fix touched were not re-viewed.
- **Not yet done:** the release (`tools/release_episode.py`: tag, upload with checksums, catalog,
  `PUBLISH.md`) and the Bilibili upload. The release workflow re-renders every scene on the pinned
  engine and writes `<id>.validation.json`, which does not exist yet; duration, frames, loudness, cue
  counts and chapters must be re-checked on those files. The two L06 Bugbot threads on PR #44 are still
  unresolved on GitHub (checked above, not resolved).
