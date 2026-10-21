# Review record: AC215 · Lecture 6 — LLM: Agents I: function calling by hand, ADK, MCP, many agents, the harness

Follow-along of [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag) `main` @ `e17a39f` (section
*Agents*, with the three lecture 5 steps it stands on),
[dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk) `main` @ `f89faa7` (the
whole root README) and three Colab notebooks (Cheese Quiz, Travel Planner, Cheese Newsletter · Harness;
saved outputs only). The issue of record is Explainer_Videos#43. The work is in the series working PR
Explainer_Videos#44 (branch `claude/mlops-learning-videos-7b5use`). Claude Code cloud sessions (Claude)
produced it:

- **Captures:** 2026-10-18, 22:58–23:00 UTC (llm-rag laptop and container) and 23:31–23:33 UTC (a fresh
  Debian 12 "laptop" with no Python, for ADK), without a Google or OpenAI key (`ASSETS.md`).
- **QA draft:** the 480p draft (31:02, parts 15:18 + 15:43) committed in `983e36e` (2026-10-20 18:35 UTC).
- **Whole-video QA:** seven watchers on that draft, one fixer per scene with findings, one
  narration/subtitle fixer, and a verifier per scene (merged output
  `/root/ac215-backup/args/l06qa_merged.json`). Fixes committed in `34d721b` (21:44 UTC); the
  verifiers' corrections in `3534ba8` (2026-10-21 03:03 UTC).
- **Finishing pass** (`/root/ac215-backup/tasks/w5f2e5y3g.output`, 18 agents; commit `705f7f1`,
  2026-10-21 14:36 UTC): shared `scenes/common.py` fixes and their verifier, a plan of 14 text items and
  6 scenes with items (each scene followed by a verifier), then a sweep of all 16 scenes for L05's three
  defect patterns and a verifier of the sweep.
- **1080p60 renders:** all 16 scenes, 2026-10-21 14:36:59–15:20:13 UTC (`build/logs/`); every render is
  newer than its scene file and `common.py` (measured check).
- **Final cut (the cut this record describes):** scene segments 15:21–15:37 UTC, the clean cut and its
  subtitles at 15:40, the zh-en copy, chapters and transcript at 16:03, the parts at 16:04–16:05 UTC.
  Subtitles, chapters and transcript are committed in `7c95e6b` (17:47 UTC); the 16 text files in
  `output/` are byte-identical to that commit (measured check, pairs check).
- **Final-cut checks:** five agent checks on 2026-10-21, about 17:47–19:04 UTC; the coordinator saved
  their returned text as `build/final-review/report-{tags,asr,visual,pairs,measured}.md` (19:06 UTC).
  **All five reports are present.**
- **This record:** first version, 2026-10-21, written before the fix round. Every defect found in the
  final cut is listed under "Open items for the fix round" as open, with its evidence and a possible
  fix; none is accepted or waived here.

This record is based on the five reports, `measured.json` and the evidence folders beside them, the QA
and finishing outputs named above, `script.md`, `BRIEF.md`, `ASSETS.md` and `SLIDES.md` (as committed in
`7c95e6b`), and `output/*.srt` for cue times. Verified facts and unclaimed reviews are kept in separate
sections.

**Conventions in this record:**
- **Times** are mm:ss in the full final cut (`output/ac215-l06-agents-1.mp4`, 31:12.1), except where
  marked *draft*. Draft times refer to the 480p QA draft (31:02); later fixes moved the scene starts by
  0 s (S01), +4.1 to +5.7 s (S02–S08), +6.3/+6.4 s (S09–S10) and +8.6 to +9.5 s (S11–S16)
  (`build/qa/scenes.json` against `measured.json`), so a draft time is up to about 9.5 s earlier than the
  same moment in the final cut.
- **Cue numbers** name their file: `.srt` (490 cues), `.zh.srt` (417) or `.zh-en.srt` (489); the
  numberings differ.
- **Evidence paths** are relative to `build/final-review/` (git-ignored; it exists only in the producing
  session, so a successor re-runs the checks to reproduce it). `writer/` holds the one frame this record's
  writer grabbed.

## Content gates (AGENTS.md)

1. **Hook** ✔. S01 opens on a puzzle from the staff's recorded run, not on a value proposition.
   - "Here's a question for a cheese expert" (00:00.0); two lines of `out.txt` print a function call and
     its arguments before the answer (00:06.6–00:14.5); "Ten passages came back, all from one book,
     filtered by author. But Gemini runs in Google's data center, where localhost means nothing."
     (00:15.2–00:24.3); "So who searched your database, and who chose the book?" (00:24.6–00:27.5). The
     two questions stay as a small YELLOW card top right until S07 answers them.
   - The lecture's bigger version follows: the Paris trip that must replan, and what LLMs and RAG lack
     (00:27.8–00:44.8, slides 20–22).
   - **Payoff:** "So, who searched your database? Gemini wrote the call and chose the book; your Python
     ran it, on your laptop." (S07, 12:37.7–12:44.8).
2. **Intuition before formalism, with an animated mechanism for each core idea** ✔. BRIEF.md ("Visual
   set pieces") defines eight; each is animated before the commands it explains:
   - **V1, three lanes, then the anatomy (S02):** one question, the same `gpt-4o` in three lanes: one
     call (02:29.0), a workflow whose Python orders 11 calls (02:35.9–02:58.6), an agent with a hosted
     web search that stops on its own (03:02.9–03:15.6); the lanes fold into the lecture's anatomy,
     "dynamic control, the steering wheel" (03:32.5), "an agent isn't a smarter model" (03:35.1).
   - **V2, the envelope (S03):** "Every call is a fresh envelope" (03:54.8); seven sheets change the top
     pick; "Memory is paper you put back in the envelope" (04:31.3); the swapped roles (04:51.5).
   - **V3, the model writes the call, your code makes it (S04 build; S06–S07 run):** the lecture's RAG
     ladder shrinks to a menu of two hand-written declarations (05:13.9–06:18.6); the three duties
     (06:24.2–06:34.4); the stage, "The model never gets your database, only a menu" (07:16.7); call 1,
     the dispatcher and call 2 with the thought signature (S06 09:36–11:21, S07 11:21.7–12:24.4).
   - **V4, the loop and its stop rule (S08):** the hub unrolls into a loop (14:04.6–14:13.9), "a reply
     with no function call is the final response" (14:18.2), the caps and `MaxTurnsExceeded`
     (14:36.9–14:44.9), dynamic control greyed out because a framework writes it (14:48.8).
   - **V5, which Python, which wheel (S09):** with no Python, uv downloads CPython 3.15.0; `onnxruntime`
     has wheels only up to 3.14; `uv python pin 3.13` (17:13.2–17:43.5).
   - **V6, the shared whiteboard (S11):** output keys write cells, placeholders read them, "The agents
     never call each other" (20:52.1–21:12.6).
   - **V7, one protocol, one plug per server (S12):** three tool families (22:11–22:21.8), ten custom
     integrations (22:25.3–22:37.8), MCP as a shared protocol (22:40.8–22:49.3), the tutorial's three
     plugs from 22:54.3.
   - **V8, turnstile and receipt (S14, S15):** a finalize call only proposes, PENDING, and only an
     explicit yes copies pending to approved (26:45.9–27:04.9); success is a receipt and a file on disk
     (28:50.4–29:05.0); a rule left in the prompt slips through, "a note is not a check" (29:15.5).

   **Lecture slides:** a GREY "Lecture 6 · slide(s) …" tag top right in 14 of the 16 scenes (all but S05
   and S10, whose script says `Lecture: none`), 29 tag spans in all, each citing the slides listed under
   its scene header in `script.md` (from S01 20–22 to S16 41 and 32–33; the mapping is in `SLIDES.md`).
   The slides are redrawn, never shown.

   **How this was checked:** QA's two director watchers read every draft contact sheet against the SHOW
   lines. In the final cut, the visual check read all 625 tiles of the burned copy (one every 3 s), and
   the tags check found the cited picture on screen across all 29 tag spans, except two swapped-in tags
   that lead their picture by about 1.4–2.7 s and three long spans that `script.md` allows (open items 2,
   3 and 15).
3. **Pause-and-ponder moments and a recap** ✔ by Conny's decision for the series (2026-10-21, see below):
   five ponders, against AGENTS.md's aim of one every 2 minutes.
   - **Ponders:** five cards, each followed by a silent timer; no English cue plays during a timer (the
     longest cue gap, 9.85 s at 06:40.8–06:50.6, is S04's timer) and the momentary loudness during every
     timer is at most −129 LUFS (`measured.json`). Each answer starts as its timer ends:

     | scene | question (card text, condensed) | card | timer | answer starts |
     |---|---|---|---|---|
     | S04 | Nine author names, eleven books: how many books can `get_book_by_author` never reach, and can the agent still get to them? | 06:42.1 | 8 s | 06:50.6 "Two books." |
     | S08 | Call 2 passes the tools but no `tool_config`; if Gemini answers with another function call, what does `cli.py` do? | 13:46.2 | 8 s | 13:54.8 "It prints a response whose only part is a function call" |
     | S09 | No Python on the laptop, the project asks for 3.10 or newer: which Python will `uv sync` use? | 17:04.3 | 6 s | 17:10.9, the answer at 17:13.2–17:19.0 (CPython 3.15.0) |
     | S13 | The classifier answers "Simple", with a capital S: which handler runs? | 25:47.0 | 6 s | 25:53.6 "The else branch: clarification." |
     | S14 | In turn 3 the model got `needs_confirmation`: why can't it call `finalize_itinerary` again to approve its own plan? | 27:05.8 | 8 s | 27:14.4 "Because apply_confirmation runs on the human's message" |

     Frames of each card on the burned copy: `measured/frame-zhen-t406.0.png`, `t830.0`, `t1027.5`,
     `t1550.0`, `t1630.0`.
   - **Rate:** 0.16 per minute. The gaps are 6:42 from the start to the first ponder, then 415.5,
     189.6, 516.0 and 72.2 s, and 237.7 s from the last to the end; the longest stretch without one is
     17:10.9–25:47.0 (8:36). AGENTS.md's aim would be about 15–16 at this length.
   - **Not counted as ponders:** S03's "Spot it" card ("Can you spot the slip?", 04:45.9, then a 4 s
     hold with the code on screen and no timer; the answer at 04:51.5) and S12's 5 s silent beat after
     "do you see a problem?" (22:30.1). Separately, 16 spoken "pause" lines tell the viewer to stop and
     run a step, from "pause to run the setup" (02:15.2) to "pause, and run the demo" (29:27.0).
   - **Recap** ✔: S16 (from 29:33.5) tears down (29:33.5–30:07.0), fills the lecture's anatomy with the
     tutorial's code and adds the two pieces to the lecture's formula, "a loop the framework runs, and
     checks that your own code enforces" (30:08.3–30:39.5), then asks five test-yourself questions and
     points to the answers in `exercises.md` (30:39.7–31:10.0; frames `measured/frame-zhen-t1820.0.png`,
     `t1845.0.png`). Part 1 closes on "In part 2, a framework runs this loop for us." (15:18.3–15:21.3);
     part 2 opens on "Part 2: frameworks own the loop." (15:24.3).
   - **Decided by Conny (2026-10-21), as recorded in `videos/ac215-l05-rag/REVIEW.md` gate 3:**
     「我觉得可以保留现在的密度」 — keep the current density: 3–5 ponders per lecture, plus a spoken
     recap and test questions.
4. **Narration written for the ear, with word-anchored cues** ✔.
   - **Spoken style:** `script.md`'s conventions apply: SAY blocks of 1–3 sentences, sentences under 30
     words; commands, flags and paths said in words ("dot env", "uv python pin 3.13"); versions that
     will change said "at the time of recording"; no sentence opens with a command or with "ADK".
   - **Size:** 153 SAY lines and 4,299 words, identical block for block to the 153 narration blocks in
     the 1080p60 render sidecars; the series budget is 3,900–4,300, so this is at the top. Kokoro
     `af_heart` at speed 0.9. Pace 137.8 wpm over the runtime and 152.2 wpm over the 1,694.5 s of voice
     (90.5 % of the runtime); per scene 137.0 (S09) to 163.4 (S08) wpm over voice time.
   - **Anchors:** 678 `vo.wait_until` calls in the 16 scene files (26 in S03 to 58 in S09; 669 with a
     literal phrase, 9 with an expression). The 16 1080p60 render logs (`build/logs/`) contain no
     "anchor not found" line (writer's grep).
   - **Ear fixes after the draft:** the QA's ASR watcher found four words Kokoro read the wrong way
     ("tear down" as "teer", the noun "lives", "Resending" as "resenting", the noun "use") and three
     hard-to-hear phrases. Seven L06-only lexicon entries fixed the readings ("Before part 2, tear down"
     14:59.4, "Pause and tear down" 15:16.7, "Tear down" 29:33.5, "Approval lives" 26:57.6, "Resending"
     12:21.7, "Kept that database?" 08:59.7, "use agents" 26:09.3). SAY lines were reworded: "checks that
     your own code enforces" (30:34.8); in the finishing pass "the web server stopped" (was "ours
     stopped", 20:07.5), "2,690 of the 6,000 dollars" (was "2,690 dollars out of 6,000", 27:31.0),
     "check yours" (20:43.0) and "uv run adk telemetry disable" (18:41.0). Three sentences holding
     version numbers were split so a sentence mark times their cues ("the banner prints." 08:13.0, "It
     also lists Chroma and sentence-transformers." 16:57.6, "But picking one still fails…" 19:26.5).
     None of these lines is among the final ASR's residual differences (`triage-base.txt`), and the
     large model hears "2,690 of the 6,000 dollars" as written (`asr-large-clips.json`, cue 429).
   - **Caveats:** the final ASR found six low-severity weak spots (open item 14) and a narration delay
     of 47.5–167.5 ms behind the picture and subtitles that grows at each scene join (open item 4).
5. **Simulated-target-viewer QA over the full draft** ✔.
   - Seven watchers reviewed the 480p draft: two directors and two simulated target viewers
     ("newcomer", one per part), a subtitle watcher, a follow-up watcher and an ASR watcher. The
     newcomers are agents that worked from the draft's contact sheets, exact 480p frames and the English
     `.srt`, with the READMEs open; they reported 21 of the findings.
   - **58 timestamped findings: 2 must, 27 should, 29 nit.** Both musts and all 27 shoulds are fixed and
     were checked by a verifier per scene on fresh 720p (or 480p) renders. Of the 29 nits, 27 are fixed
     (6 of them in the finishing pass), one is worked around in the episode (cue timing inside a sentence:
     three sentence splits; the toolkit fix is deferred) and one is partly fixed (the S13 Guild panel).
     Details under "Whole-video QA".
6. **Measured checks** ✔. The numbers are under "Verified (final render)" (`measured.json`).
   - **Duration:** 31:12.1 (1872.088 s), inside the series' 25–35 min; parts 15:24.3 (924.349 s) and
     15:47.8 (947.834 s), which sum to 0.095 s more than the full cut.
   - **Loudness:** −16.1 LUFS integrated in the clean cut, the zh-en copy and part 2, −16.0 LUFS in part
     1; LRA 2.3–2.5 LU; true peak −2.6 dBFS (clean cut and zh-en), −2.7 (part 1), −2.8 (part 2). The
     build's target is −16 LUFS with true peak at or below −1.5: **every file meets it.**
   - **Caption bounds:** in the burned layout every subtitle lies inside x 428–1489, y 991–1063, in the
     band below the picture (which ends at y 938), and none falls in the 40 px side margins (libass render
     of each `.zh-en.ass` at 1 fps, confirmed within 1 px on three burned frames).
   - **Music balance:** does not apply. L06, like L02–L05, has no score: `video.yaml` has no `music:` key,
     and the ponder timers measure as silence.
   - **Subtitle sync:** no cue's speech starts more than 1 s after the cue (median 0.04 s, largest
     0.69 s; ASR check), with the narration delay of open item 4 on top.

   **Human review:** the series waiver stands in for a listening sign-off.

   Listening sign-off: waived by Conny for the AC215 series (Explainer_Videos#29, 2026-10-15): 「不需要，我现在对视频质量很满意的」 — no human listened to this cut; the ASR round trip below is the substitute.

   **ASR round trip on this cut** (`report-asr.md`): base.en over the whole clean cut (490 cues, 213 with
   some difference, 4,349 words recognised). After removing number, identifier, possessive and
   punctuation differences, 124 differences in 114 cues remained (`triage-base.txt`); 62 of those cues
   were re-run with large-v3-turbo on their own audio (30 match word for word) and nine doubtful ones
   again with 2 s of context. The large model recovers every word base.en seemed to drop or garble, among
   them the 11:43–11:49 passage and "Agent Development Kit runs" (15:28.2). No mispronounced or
   swallowed word needs a re-render; six low-severity weak spots remain (open item 14). The zh-en copy
   carries the same audio (audio stream MD5 `2ff0ebdd92491881ee563f32cdde290d` in both).

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
  final cut the card shows it at 11:18.5 (`writer/clean_678.5_s06_turn_card.png`).
- **S14, draft 26:53 (director, picture):** the GREEN "pending → approved" tag on line 61 was taller
  than a 20 pt code row, and its opaque box covered the tops of "↪ context.pending_proposal.copy()", the
  line the narration stresses. **Fix:** a local `row_tag()`, a dark pill 0.04 shorter than the row
  pitch with no outline, for both the full and the folded panel, with asserts that it stays between
  lines 60 and 61's second rows. Verified at 720p; in the final cut the `copy()` row is clear at 27:03
  (`frames/zh_1623.png`).

**The shoulds (27), all fixed:**
- **Follow-along:** S05's your-turn moment now shrinks the terminal to a strip and shows a GREY card
  with `sh docker-shell.sh`; S07 prints `head -4`'s lines (the old book's title); S02 and S14 (and S15,
  in the finishing pass) say where to open each notebook (course site or study guide; S01's "You need"
  card gained "three Colab notebooks · links in the study guide"); S12's timeout tip names the `npx`
  command, and a chip warns that Ubuntu 22.04's apt Node (v12) is too old; S10's chip and narration say
  `uv run adk telemetry disable`.
- **Picture and pacing:** S07's unsent call 2 now stays unsent (a GREY dashed `recorded · the staff's
  call 2` envelope crosses instead); S08 names the two frameworks with chips ("OpenAI Agents SDK",
  "Microsoft Agent Framework"); S14 and S15 lowered the Colab frame so the tracker caption clears its
  tab; S14's plan card got its `recorded` tag and its emphasis now lands on "asks for a yes"; S13's
  trees stay up through the question with no empty frame; S10's undo output and the `--port 8080`
  success are held long enough to read; S16's Ctrl+C box is legible for about 2.5 s; S09 no longer
  brings the stale beat-4 `.env` rows back during `uv sync` (the follow-up watcher's Bugbot thread).
- **Subtitles:** `"mode": "ANY"` stays in one English cue; the `--load` command is no longer split in
  the Chinese tracks; S09's clause sits over its own English.
- **Narration:** the three lexicon readings and the recap line (gate 4).
- **Shared:** `Terminal.print(wrap=True)` folded words mid-word throughout; fixed in the finishing
  pass by a word-boundary wrap in `common.py` (below).

**The nits (29):** 27 fixed, among them S01's tag legend (now glossed), S01's sample-command caption and
MCP gloss, S04's 4.1 s still panel, S08's two yellow fills that hid their own words, S12's scrambled
three-plug morph, S11's model tag, S14's finalize_plan/finalize_itinerary link, S16's `__pycache__` rows
and `.venv` chip, four subtitle nits, two lexicon nits, and in the finishing pass the shared wrap and
▶-header repeats and the two narration nits the QA text fixer had left ("ours stopped", "dollars out
of"). **Worked around:** the cue-timing nit (three cues that split a sentence with a version number
were 1.0–1.2 s off): the finishing pass split those sentences; the toolkit fix (`explainer/build.py`
`split_cues` weighting by spoken length) is deferred. **Partly fixed:** S13's Guild tree beside the
cell 68 panel (lines 1–8 show `mozzarella_tool`/`format_quiz` and not `vegan_specialist`): a caption
"Cheese Quiz Guild · 4 of its 6 tools" explains it; the panel itself is unchanged because `script.md`
fixes it at lines 1–8 and a folded 1–6, 8–11 panel needs about 14 rows.

**Verifiers:** 16 verifier reports (S01, S02, S04–S16, and one for the "tear down" lexicon in S08/S16;
S03 had no finding, and its Bugbot thread did not reproduce). Four verifiers also edited their scene:
S06 (the cost wording and the caption timing), S11 (the moved tag's swell left the safe area and
touched the extra card), S15 (an older overlap the QA had not reported) and S16 (the timing after the
shutdown box).

### Finishing pass (2026-10-21, 18 agents, commit `705f7f1`)

- **Shared `common.py` (one agent, then a verifier):** a word-boundary wrap for terminal output
  (`wrap_output`: 43 breaks in the dry runs, 37 at spaces, none mid-word), `turn_card(header=None)` as
  the default (one "your turn" per ▶ card), L05's scroll fix (leaving rows fade in place first), and
  sequential old-out-then-new-in swaps for the tracker, sections, lecture tags, container titles and
  gate labels; plus the critics' requests (`src_panel` colours a wrapped string as one, one bar per
  wrapped line, shorter time tags). The verifier dry-ran all 16 scenes with the old and new code: every
  voice-block start, play and end time identical.
- **Plan:** 14 text items, 6 scenes with items, 14 skipped with reasons (among them: no slide items,
  because the lecture tags are in 14 scenes; the deferred toolkit items; the optional "OpenAI Agents
  SDK" SAY and S02 spoken line; S14's "checked state"/"a finalize tool" reductions, judged not worth a
  re-voice; S16's Ctrl+C output skipping lines 365–366 without a `…`, which a 3-row strip cannot show).
- **Text agent:** the SAY changes in gate 4, the `script.md` SHOW lines that had drifted from the
  scenes, `i18n/zh` g1/g2 and the glossary; `python -m explainer.i18n check` printed OK.
- **Scene agents and verifiers:** S01's eighth "You need" row (its verifier added a 1.0 s hold so the
  unspoken row can be read: S01 grew to 115.1 s); new anchors in S09, S10, S11 and S14 (S10's verifier
  split the "address already in use" flash onto the spoken words); S15's where-to-open caption (its
  verifier staged the caption's exit before cell 16 so they never overlap) and the "you and a friend"
  tag lifted off line 8's bar.
- **Sweep for L05's patterns** (copy flights over text, fills hiding their own label, double-exposed
  swaps): a dry-run analyser flagged 115 candidates; 87 were real, 82 fixed and 5 only partly fixed or
  not fixed (among them S04's cards brushing the HTTPS label, and the S10 scroll at 18:50, left because
  `_make_room` is shared code).
  The sweep verifier checked about 69 of the changes on fresh 720p previews, fixed 14 that were
  defective, 2 problems it found itself and 2 candidates the sweep had called "not real" (S09's
  ponder-card swap, S12's absorbed `{…}`), gave S04's cards their own lanes, and judged the S10 scroll
  not real. Its occlusion check's hits in S03, S04, S06, S10, S11, S14, S15 and S16 were not looked at.
- **What the finishing reports left open:** S13's panel (above); S04's thin seam between adjacent line
  bars (`explainer/devops.py`, toolkit); S01's legend word "no key" against S06's "real run · no key";
  the tracker's harmless divide-by-zero warning; S10's ▶ card arriving about 1.4 s after "Pause" (a
  deliberate 1 s hold); S14's turnstile passing over "runs first" and "the human" for about 1 s during a
  move (scene 64.4–65.4 s, about 27:19); the sweep later restaged S14's moves and the final visual check
  did not report it.

## Final-cut checks (1080p60, 2026-10-21)

Five agent checks, each from its own report:
- **Tags** (`report-tags.md`): all 29 `lecture_ref` tags fade in with the picture they cite, leave before
  their scene ends, overlap nothing (10 fps box scan) and spell "slide"/"slides" correctly; a 4 fps
  sweep of the top-right corner over the whole film found only the expected segments; every tag swap,
  measured frame by frame, ghosts at most 5.5 % while the other tag is visible (no double exposure).
  Two minor timing defects and three long spans (open items 2, 3, 15). The review-bot list it was given
  was empty.
- **ASR** (`report-asr.md`): the narration is intelligible (gate 6); six weak spots; the narration
  delay at scene joins.
- **Visual** (`report-visual.md`): 40 contact sheets (625 tiles, every 180th frame of the burned copy),
  plus strips and crops at doubtful moments. No blocking defect: nothing clipped or outside the frame,
  no black or missing scene, no garbled glyphs, no tag stuck between scenes; one real minor render
  defect and five brief transient overlaps (open items 1, 5, 6, 7 and 9), two holds just over 4 s (item
  10), one glitch-looking row that is authentic (item 11) and three sub-second effects (item 12).
- **Pairs** (`report-pairs.md`): all 489 bilingual cues read in full; no meaning swaps between a
  Chinese line and its English, or between neighbouring cues; every condition and time clause in the
  same cue as its partner. Two minor pairing blemishes and three commands broken across lines in the
  English-only `.srt` (open items 8, 13).
- **Measured** (`report-measured.md`, `measured.json`): every measured check passes (gate 6 and
  "Verified"); no defects, five observations (open items 16 and 17).

## Open items for the fix round

Open in the final cut, most important first. None is accepted yet; the coordinator decides each.

1. **S08, 14:19.8–14:22.5 (about 2.7 s), real but minor: the exit arrow strikes through the "plain
   text" chip** while "a reply with no function call is the final response" is spoken. Cause:
   `scenes/s08_loop.py:385` centres the chip on the arrow (overriding `reply_card()`'s place above it,
   `scenes/common.py:3953`), and `chip()` has only a 0.16 fill. Possible fix: move only x, or an opaque
   fill. Evidence: `frames/strip_s08_plaintext_chip_14m21-14m23.png`,
   `frames/crop_s08_plaintext_14m20.1.png`, `frames/zh_861.png`.
2. **S12, from 22:38.25: the "slide 53" tag leads its picture by about 2.7 s.** It swaps in over the
   slide-52 picture (red custom-code blocks, "10 integrations"); the MCP morph starts at 22:40.75. The
   swap follows `script.md` (start of SAY[2]), but that SAY opens on "Every tool becomes a custom
   integration", still slide 52's point (`s12_mcp.py:605`). Evidence:
   `tags/frames/t20_a_after_in_1358.40.png`, `tags/frames/t20_e_53_before_morph_1360.00.png`.
3. **S08, from 14:48.97: the "slide 41" tag leads its picture by about 1.4–2 s.** It swaps in over the
   max-turns picture (fading 14:49.2–14:49.7) and then the bare loop track; the anatomy fades in only at
   14:50.4–14:51.0 (`s08_loop.py:506`). Possible fix: run `lref_swap` after the fade-out, or with
   `FadeIn(A)`. Evidence: `tags/frames/t12_d_gone_889.47.png`,
   `tags/frames/t12_e_41_before_anatomy_890.00.png`.
4. **Narration plays 47.5–167.5 ms behind the subtitles and pictures, growing at each scene join**
   (toolkit, likely every episode stitched this way). Constant within a scene: +47.5 ms in S01, then
   62.5, 65, 75, 77.5, 80, 97.5, 97.5, 100, 115, 132.5, 147.5, 155, 162.5, 165 and +167.5 ms in S16; the
   zh-en copy is identical; the parts restart at +47.5 ms (part 1 to +97.5, part 2 to +115). Likely
   cause: `explainer/build.py` joins the scenes' AAC audio with the concat demuxer (`-c copy`) without
   trimming each segment's 1024-sample (21.3 ms) encoder lead-in; the model predicts every step within
   2.5 ms. Below the ITU-R BT.1359 limit for late audio (about 185 ms); the visible effect is that
   word-anchored highlights in S11–S16 land about 0.1–0.15 s before their word. Not a blocker; a toolkit
   fix for the coordinator. Evidence: `lag.log`, `lag-parts.log`.
5. **S04, 07:20.0–07:20.8 and 07:26.8–07:27.6, transient: cards fade in on top of the cloud's
   "Gemini / location global" label** (the `{name, args}` card, later the reply-lines card); the label
   shows through while they fade, then is covered until the card flies off. The sweep had already
   rerouted these cards. Evidence: `frames/crop_gemini_cards_7m20-7m27.png`,
   `frames/crop_gemini_second_card_7m25.5-7m26.9.png`.
6. **S10, 19:47.85–19:48.35 (about 0.5 s), transient double exposure:** the "this video: baseline,
   mcp_tools" card arrives over the fading dev-UI browser, then the incoming laptop terminal rises under
   the outgoing one, whose header crosses the `uv run adk web` line at 19:48.15. Evidence:
   `frames/strip_s10_terminal_swap_19m47.9-19m48.3.png`, `frames/strip_s10_19m47-19m49.png`.
7. **S02, 03:05.9–03:06.3, cosmetic copy flight:** the small diamond flying from lane 2 to the gpt-4o
   pill crosses the dimmed caption "your Python decides the order" and the "o" of "gpt-4o". Evidence:
   `frames/crop_s02_diamond_over_caption_3m06.png`, `frames/strip_s02_diamond_flight_3m05-3m06.png`.
8. **Subtitle pairing, two blemishes** (designed fallback of `_split_like`; nothing swapped):
   - zh-en #84/#85, 05:32.250–05:37.299: one English line, "llm-rag's Agents section is Agentic RAG
     with a menu of two.", under two Chinese cues; #85 (菜单上只有两项) reads as a 1.5 s fragment.
     Suggested zh: 「在 llm-rag 里，Agents 一节就是只有两项的 Agentic RAG。」 (one cue; `g1.yaml` S04[2]).
   - zh-en #143/#144, 09:10.417–09:15.025: one English line, "We had no key, so the staff's committed
     embeddings stood in for the embed step.", under two cues, and #143 ends on the dangling 「所以 embed
     这一步」. Suggested zh: 「我们没有密钥，所以 embed 用的是课程团队 commit 过的 embedding。」, which pairs
     clause by clause (`g1.yaml` S05[7]).
   Evidence: `pairs/band_334.0.png`, `pairs/band_336.5.png`, `pairs/band_551.5.png`,
   `pairs/band_553.8.png`, `frames/zh_555.png`.
9. **S03, 04:56.8–04:57.2, cosmetic:** the swapped `role "user"` and `role "system"` labels pass through
   each other on straight paths; the end state at 04:57.5 is correct. Evidence:
   `frames/strip_s03_role_swap_4m56-4m58.png`.
10. **Two holds frozen slightly longer than 4 s, outside the ponder timers:** 15:19.0–15:23.5 (4.5 s,
    end of S08, on the your-turn card "exit / docker compose down"; narration ends at 15:21.25) and
    28:06.5–28:11.25 (4.75 s, end of S14, on the Travel Planner your-turn card). Both are deliberate
    "pause and do it" holds, 0.5–0.75 s over the limit. Three more stretches move only slightly
    (10:56.25–11:01.5, 24:26.75–24:30.75, 30:50.0–30:54.25). Evidence: `sheets/static-scan.txt`,
    `sheets/freezes-clean.txt`.
11. **S07, about 12:54–13:06, low, authentic:** in the `out.txt` word-count table the "Soča" row and its
    boxes sit one column left. This matches the capture (`assets/terminal/laptop/10-x-old-words.txt`:
    `printf %-18s` pads by bytes and "č" is 2 bytes), but a viewer may read it as a glitch. Evidence:
    `frames/crop_s07_soca_row_13m00.png`.
12. **Sub-second effects, for completeness:** 01:12, the highlight pulse scales "built, not sent" until
    it touches its pill outline; 28:36.0, the frame border shows through the "recorded · the staff's
    last saved run" tag as it fades in; 14:14.5–14:15.9, "decision maker" visibly morphs into "model".
    Evidence: `frames/crop_legend_built_not_sent_1m12_1m13.png`, `frames/strip_s15_recorded_tag_28m36.png`,
    `frames/zh_855.png`.
13. **English-only `.srt` breaks three commands across lines** (not the burned zh-en asset):
    `.srt` cue 139 (08:43.5, "python cli.py --agent / --chunk_type char-split."), cue 149 (09:17.0,
    the same for `--load`; both are 47 characters against a 44-character line) and cue 295 (18:41.0,
    "change it later with uv run / adk telemetry disable.", avoidable as "change it later with / uv run
    adk telemetry disable."). Toolkit: `explainer/subtitles.py` (`_two_lines` / `_reflow_en`).
    Evidence: `pairs-breaks.log`.
14. **ASR weak spots, low severity** (both models hear the same, even with 2 s of context; the subtitle
    and the screen carry the exact words): 28:44.4 cue 449 "Then send_email saved the HTML." heard as
    "send email, save the HTML" (the one most worth rewording if S15 is re-rendered); 27:40.5 cue 431
    "checked state" heard "check state"; 19:47.8 cue 313 "the root .env file" heard "root.n file";
    10:29.5 cue 170 the fifth "mode ANY" heard "modini" (the other four are heard correctly); 12:26.2
    and 12:49.6 cues 202/209 "transhumance" heard "transhumans" (defined at once in the narration);
    26:26.6 cue 413 "a finalize tool" heard "a finalized tool". Cue numbers are the `.srt`'s. Evidence:
    `clips-wide/`, `clips/`, `compare-large.txt`.
15. **Three tag spans outlive their cited picture** (allowed by `script.md`'s "until a SHOW changes it"
    rule; the coordinator may tighten): S07 "slide 39" stays to 12:49.6, about 24.6 s after the
    "interpret its outputs" chip leaves (12:25.0); S08 "slides 35–40" stays to 14:49.0, about 33 s after
    the hub unrolls into the track (14:14.5–14:15.9); S04 "slides 8–14" stays to 05:44.3, about 12 s
    after the column shrinks to the two menu cards (05:32.3). Small leads under 1.5 s (S01, S02, S04
    tags) and three tight but clear gaps (5–8 px) were judged acceptable.
16. **Measured observations (information):** in zh-en cues #23 (01:31.357, 「Docker、Chroma、uv」) and #295
    (18:42.535, the command `uv run adk telemetry disable`) the top line has no Chinese character; the
    zh-en copy has one more video frame than the clean cut (112,325 against 112,324); the audio language
    tag is "und"; the part videos carry no burned subtitles (only the full zh-en copy does); the video
    bitrate is about 0.29 Mbps at 1080p60; the narration starts at 0.000 s with no lead-in (every
    scene's voice starts 0.1–0.3 s after its cut).
17. **Episode files:** `README.md`'s chapter 10 summary and its errata paragraph still give the bare
    `adk telemetry disable`, which the QA found fails outside the project's environment; the video now
    says `uv run adk telemetry disable`. `video.yaml` has no `publish:` block yet, which the release
    workflow requires. `QA_FOLLOWUPS.md` does not exist (the follow-up watcher rebuilt the list from PR
    #44's review-bot threads: one did not reproduce, the other was fixed in S09).

## Verified (final render)

- **Files** (`measured.json`): all four MP4s decode in full with no error (`ffmpeg -v error`, exit 0).
  1920×1080 at 60 fps, H.264 High, yuv420p; AAC-LC 48 kHz stereo; `moov` before `mdat` in all four.

  | file | duration | frames | size |
  |---|---|---|---|
  | `ac215-l06-agents-1.mp4` | 1872.088 s (31:12.1) | 112,324 | 106.7 MiB |
  | `ac215-l06-agents-1.zh-en.mp4` | 1872.083 s | 112,325 | 105.2 MiB |
  | `_part1.mp4` | 924.349 s (15:24.3) | 55,458 | 51.8 MiB |
  | `_part2.mp4` | 947.834 s (15:47.8) | 56,866 | 55.0 MiB |

  The video streams of the two parts sum to 1872.067 s, exactly the clean cut's video stream and the
  sum of the 16 scene renders.
- **Loudness** (EBU R128, true peak): −16.1 / −16.1 / −16.0 / −16.1 LUFS, LRA 2.4 / 2.4 / 2.3 / 2.5 LU,
  true peak −2.6 / −2.6 / −2.7 / −2.8 dBFS (clean, zh-en, part 1, part 2). The zh-en audio is a straight
  copy of the clean cut's (identical audio stream MD5).
- **Subtitles** (all nine files): numbered in order, sorted, inside the runtime, never overlapping or
  empty, none under 0.8 s (shortest 1.000 s English and Chinese, 1.358 s zh-en), at most two lines,
  Chinese always above English. Cue counts: full 490 / 417 / 489, part 1 248 / 207 / 245, part 2
  242 / 210 / 244 (`.srt` / `.zh.srt` / `.zh-en.srt`); the parts add up to the full counts and part 2's
  cues are the full cut's shifted by exactly 924.300 s. Each `.zh-en.ass` matches its `.zh-en.srt`
  (0 timing or text mismatches). The last cue ends 2.06 s before the end; reading speed peaks at 4.58
  words/s (English) and 7.81 characters/s (Chinese). All 762 distinct characters render in Noto Sans CJK
  SC (visual check).
- **Burned layout:** the picture is scaled to 1670×938 at the top and every cue is one Chinese line (50
  px) over one English line (33 px) in the band below (`WrapStyle: 2`); spot frames at commands
  (`python cli.py --load`, `docker compose down`, `uv run adk web --port 8080`, the MCPToolset code)
  show every command fully visible.
- **Chapters:** `chapters.txt` has the 16 titles of `video.yaml` in order, each at the true scene start
  rounded down to the second (up to 0.85 s early, S04); `chapters_part1.txt` and `chapters_part2.txt` follow the
  same rule (part 2 measured from 924.3 s). The visual check found every chapter time equal to the
  computed scene start.
- **Scene boundaries:** the first and last frames of all 16 scenes are empty background (maximum grey
  14–16; `sheets/scene-ends.txt`); no tag crosses a scene boundary (tags sweep, visual check).
- **Narration against the script:** 153 SAY lines and 4,299 words in `script.md`, the same in the 153
  render voice blocks; 678 `wait_until` anchors; no "anchor not found" in the render logs.
- **Ponders and recap:** five ponder cards with timers of 8, 8, 6, 6 and 8 s, silent during the timer
  (momentary loudness at most −129 LUFS); the recap and test questions in S16 (gate 3).
- **Lecture tags:** 29 spans across 14 scenes, each over its cited picture, no overlap, no double
  exposure in any swap (tags check).
- **Defect patterns from L05, on the final frames:** no fill hides its own label in the dense frames
  checked at full size (the your-turn cards, the PENDING stamps at 26:51 and 27:03, the sticky note at
  29:12) and no tag swap is double-exposed. The remaining instances are open items 1, 5, 6, 7 and 9.
- **Recorded and no-key steps are labelled on screen** (visual check): "recorded · the staff's run,
  September 22, 2026" (12:30), "recorded · the staff's last saved run" (25:21, 26:33, 28:36), "at the
  time of recording", and "built, not sent", "no key" and "stand-in" on the steps run without a key; the
  QA's part-2 director found a "recorded", "with your key" or "illustration" label on every step that
  needs a key.
- **Bilingual pairs:** no meaning swap in the 489 zh-en cues; no command, path, flag or placeholder
  split across a line or cue in the zh-en and zh tracks (pairs check).
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
  6); the ASR round trip is a machine substitute. The QA's simulated viewers are agents working from
  contact sheets, single frames and subtitle text.
- **The Chinese subtitles were reviewed by agents only:** the QA's subtitle watcher read every cue of
  the draft against the glossary, and the pairs check read all 489 zh-en cues of the final cut. No
  human translator or native proofreader has read them. The `.zh.srt` track was checked mechanically
  and for split commands, not re-read for meaning.
- **Steps the captures could not run** (`ASSETS.md`, "Not captured"): every Vertex AI and Gemini API
  call (both `--agent` calls and `--embed`, which the staff's committed embeddings stand in for;
  `GCP_PROJECT` is a placeholder and `secrets/` was empty); the AI Studio key; chatting with the ADK
  agents; ADK modules 2, 4, 5 and 6; all three Colab notebooks (OpenAI). They are shown from the
  staff's saved outputs, the real printed requests and illustrations, and no claim is made that they
  behave the same with a key today.
- **Docker Hub and the capture machines:** the base image was rebuilt locally with the recording proxy's
  CA (a student's first build also pulls it; no pull is shown), Docker Hub images came through
  `mirror.gcr.io`, and the Chroma server's version was not recorded. The laptops are containers (a
  `docker:29.8.2-dind` engine, a `debian:12` box), not Docker Desktop or a Mac; the ADK capture used
  CPU-only PyTorch (a student sees 189 packages and about 3 GB of CUDA packages on a Linux PC); its
  telemetry question was answered "n".
- **What the checks did not cover:** the visual check sampled one frame every 3 s plus strips at
  doubtful moments, so a transient shorter than that may be missed; the QA and sweep fixes were not each
  re-verified on the final frames (only through that sampling and the targeted strips); the sweep's
  occlusion hits in eight scenes were never looked at; nobody checked `exercises.md`, `transcript.md`'s
  wording or the study guide in this review; the narration-delay cause (open item 4) is a model that
  fits the measurements, not a toolkit change tested here.
- **Not yet done:** the fix round, a re-check of its changes, the `publish:` block, the release
  (`<id>.validation.json` is written by the release workflow) and the Bilibili upload.
