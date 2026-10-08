# How these explainer videos are made — narration script & visual plan (v2)

<!--
Review log (v1 → v2, 2026-10-07). Four independent reviews of v1: facts, honesty, a fresh
viewer, spoken flow. Every must-fix item was applied, some in a different wording; the
exceptions are listed under "Rejected or changed".

Changed (main points)
- Truer framing. S01: the "12" frame is from an early draft (it never reached a finished video).
  S02: the paper came from a friend; the user hadn't read it, to keep the test fair. S03: the
  user "supplied" the program, not "wrote" it. S04: the agent wrote "review first" into its own
  guide, then broke it the same day (it did not "learn the hard way"). S07: a cross-scene
  reviewer (faded BLUE), not one that "watched the whole video". S09: fixers and verifiers are
  plural (4 groups); "103 points, most of them polish"; "35 skipped" is gone; one reviewer, who
  noticed the stale renders, instead of "reviewers judged old pictures".
- Guardrails. "a simulated 12-year-old, sharp but ordinary"; "no record yet of anyone checking
  it by ear"; "every test viewer on record"; "another voice passed all 17 test terms" (the
  recognizer's fuzzy match, which heard "Cloud Shannon"), not "got them right"; no "never" about
  render reproducibility.
- Voice-choice error fixed. The top scorer was Brian, a male voice built for English, not a
  Chinese voice. Ava (female, English-first) scored about as well as Xiaoyi, so Xiaoyi was not
  the "female runner-up". It was picked as a native Mandarin female voice.
- Quotes. Only filler words are removed. Card 4 keeps "I feel like". The Chinese request is
  quoted verbatim. The X0 bubble has no added "I". A42 is now the English round-1 prompt line,
  not the Chinese one. S11 says "AI should not just be", not "this should not just be".
- Stale facts. The subtitle numbers are labelled "first review round"; the test count is
  dropped; "not rendered / 0 clips when this script was written". The cost snapshot is
  1507.47. The live values gained rows for the facts that can change before rendering.
- Clarity for a fresh viewer. "The user", Manim, workflow runs, the synthetic voice, the
  toolkit, commits, lint and playground are now introduced on first use. S01 no longer says
  the AI "watched". S06 answers both halves of its ponder ("and sound into text").
- S05 ponder. It compares the number with the 7-letter word "example", and the narration no
  longer reads the number before the pause.
- S08 ponder. The cause is no longer given before the question; S09 opens with the answer.
- S10 has four groups instead of six items. People first: the agent's judgement calls moved
  here from S09, which now holds only tool bugs. Then engineering, then subtitles.
  Interactivity comes last and hands over to S11.
- S11 ends on a concrete request ("say so, with the time") and drops "you may be the first".
- For the voice. "say line" and "show line" are lowercase (the voice spells out "SAY"). Decimals
  are written in words ("two point two"). The shifts are "hand-set" (set by the agent), not
  "hand-measured".
- Screen load. The quote cards are cut with "…". S04 has no zoom box. S07 shows one code line
  per panel. Future features carry "idea · not built yet".
- Cuts for length. The bin/bucket beat (S08), the real-program line (S06; S03 already shows it
  printing 255168), the recognizer sentence (S05, now an on-screen caption), the 8 → 8.5 score
  (S07, now on screen with both caveats), "It was fast, too", and the "0 clips" clause (S10, on
  screen). S10's judgement calls are one spoken sentence; the details are on screen.
- Length. v1 had 1,808 words, about 12:10 at the tic-tac-toe video's measured pace (0.385 s per
  word, plus 32 s of ponders). v2 has 1,777 words in 46 say lines, about 11:58. The cost is still
  never spoken as a number, but S03 now says "at API list prices".

Rejected or changed
- Facts, A31 caption "Chinese tic-tac-toe final cut, commit 68d6c23": rejected. The
  voice.json stamp was written Oct 7 02:31, after 68d6c23 (Oct 6 17:52). It is captioned
  "voice stamp of a Chinese scene render (tic-tac-toe scene 3)" instead. A04 is pinned to
  68d6c23, as suggested.
- Facts, S04: the two "9!" rules. Not narrated. The narration says only that nine factorial is
  spelled out "for the ear", so it gives no wrong reason. The screen shows the real convention
  line.
- Viewer, S05 ponder wording: changed. Speaking "362,880" before the pause gives the answer
  away (spoken reviewer), so the narration says "the number on screen".
- Viewer, S01 "told to review the video like a 12-year-old": changed to the spoken reviewer's
  "pretending to be a 12-year-old". The guardrail bans calling the persona "a 12-year-old",
  not saying it pretends to be one, and this wording sets up S07's title.
- Honesty, S11 "nothing in its pipeline can hear it": changed to "the agent that made it can't
  listen to it". In S08 a speech recognizer "heard" words, and the two lines would clash.
- Viewer, S03 "to launch several agents at once": changed to "to launch sub-agents, each with
  one job", with no "at once". Many runs were pipelines, not parallel (facts).
- Viewer suggestions not taken: "The voice you're hearing now is one of them" (length; S11
  makes the same point under the same condition); "and even pointed to the line of code" (the
  note says "around line 280"; length); "like a build that reuses a stale cache" (the audience
  is not assumed to code).
- Spoken, S08: deleting the bin/bucket beat was accepted, for length and because it is hard to
  follow by ear. A29 stays in ASSETS.md as an optional cut-in.
- Spoken, cards of 15 words or fewer: kept, except card 4 (19 words), which keeps the user's
  hedge "I feel like" (honesty).
- Viewer, the S08 sentence on cues "re-aimed" at Chinese words: dropped rather than reworded.
  S08's first beat now gives the reason for the one-to-one rule ("every animation cue still
  has a sentence to wait for").

Final check of v2 (2026-10-07, repo at d4043cd): every number, date, quote and claim re-checked
against git, the run records and the transcript. Changed:
- S01: "Here's what a paused frame looked like in an early draft" (the picture is a re-render or a
  reconstruction, so "This is a paused frame" overclaimed).
- S02: "The user's own words go further" (after the Karpathy sentence, "Their" could mean him).
  Cards (3) and (4) end on "…", since the quotes continue in the request.
- S03: the edge-tts chip says "via Microsoft Edge" (edge-tts is a third-party library).
- S08: the 27-word fingerprint sentence is split in two. The broken-cue tag cites the QA
  reviewers' quotes: the old .srt in 6f9e57c is the English video's Chinese sidecar, not the
  Chinese draft.
- S09: the 。 was lost when the short cue 不是。 was merged into the next one, not when "two
  short subtitles" merged. "One reviewer noticed …" became "The file dates gave it away": the
  fix (5be60d7) followed the agent's own date check (transcript, Oct 6 00:06), not the Oct 4
  reviewer note, which stays on screen as an earlier sighting.
- S10: "about 400 lines per minute" holds only for tic-tac-toe (privacy: 7,532 lines / 24.2 min
  ≈ 310), so the number left the narration and the bar shows both. "Nobody has measured what
  anyone learned" became "there's no measure yet" (the friend may have reported back off the
  record). Card 3 adds round 3 (3aace23) and round 4. Live values refreshed (103 commits, 44
  tests).
- Length: 1,780 words in 46 say lines and 152 sentences, about 11:56 to 11:59.
-->

Audience: viewers of the other two videos, and anyone curious how an AI agent can make an
explainer: a researcher, a student, a Bilibili or YouTube viewer. No Manim, programming or
machine-learning background assumed; the only idea we lean on is "an AI that writes and runs
code", and every technical word gets a few-word gloss the first time it is spoken (workflow,
toolkit, commit, lint, playground). Goal: understand (1) the pipeline: paper → digest → a script
that is code → animation timed to a synthetic voice → video with subtitles, (2) who did what: one
human, one agent, many sub-agents, many tools, (3) how an agent that can't hear or watch checks
its work, by turning what it can't perceive into things it can measure, and which real bugs that
caught, (4) what is still unverified, and what to improve next.

Facts: every number comes from the meta-video fact sheet (`FACTSHEET.md`, research snapshot
2026-10-07, repo HEAD `bb3fc1e`), using its corrected values, re-checked by the four v1 reviews at
HEAD `60258b4` and by a final check of v2 at HEAD `d4043cd`. Its honesty notes and the user's
decisions are binding. Numbers that keep moving
(the commit count, the cost counter, the "when this script was written" facts) are phrased so they
stay true, or live in one place (see "Live values"). Every real asset a scene needs, with the
command that extracts it, is listed in `ASSETS.md` (ids `A01`…).

Conventions
- `SAY:` lines are spoken verbatim (one `voiceover` block each) and become subtitles. Written for
  the ear: symbols are spelled out ("4 times 3", "percent"); numbers that matter are written as
  digits (the narrator reads them correctly), small counts as words; decimals in words ("two point
  two": the voice reads "2.2." as "two. two"); never "9!", and never end a SAY sentence on a digit
  followed by "!". No abbreviations with full stops ("e.g."). Inside SAY, the script's own line
  types are written in lowercase ("a say line", "a show line"): the voice spells out "SAY". A
  quotation never ends a sentence that is followed by another sentence in the same SAY line (the
  sentence splitter needs `. ` before a capital, and the Chinese version needs one sentence per
  English sentence).
- Translatable: short sentences, one idea each, no English-only wordplay; each sentence makes sense
  on its own (the Chinese version translates sentence by sentence, one to one).
- `SHOW:` lines describe what is on screen during that `SAY:` line. Each ends with a source tag:
  - `[REAL Axx]` real material shown as is (frame, contact sheet, code, SRT text, paper page,
    quote). A GREY 20 pt source caption sits in the bottom-left corner ("real contact sheet ·
    tic-tac-toe video, scene 3"). Real artefacts keep their own colours and sit in a thin GREY
    frame, so they read as exhibits, not as this video's colour code.
  - `[DATA]` drawn in Manim from real numbers or real text (the source is named).
  - `[DIAGRAM]` an explanatory drawing that claims to be nothing more.
  - `[RECON Axx]` a redrawn picture of something that no longer exists. It always carries the
    on-screen tag **"re-created for this video"** (GREY rounded tag, top-right, 22 pt; it said
    "reconstruction" until the fresh-viewer review of the draft). Where `ASSETS.md` offers a
    re-render of the old commit instead (A03), the tag reads **"the old draft, redrawn from its
    saved code"** (was "re-rendered from the old code (commit 8a922bf)"). On-screen words avoid
    developer jargon: "review", not "QA"; "voice test", not "bake-off"; "self-checks", not "asserts".
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer), then remove the card at the start of the next block. As in the tic-tac-toe video,
  the card comes in on the word "Pause" (`vo.wait_until("Pause")`), so the question is already on
  screen when the viewer pauses.
- Semantic colours (fixed for the whole video):

  | role | colour |
  |---|---|
  | the human (the user) | **PINK** |
  | the main agent (Claude Code) | **BLUE** |
  | sub-agents (workflow agents, reviewer personas) | **faded BLUE** (BLUE at 45 % opacity) |
  | tools, files, code panels | **GREY** |
  | audio, voice, spoken words, anchors | **ORANGE** |
  | a measured check (lint, assert, speech recognizer, frame fingerprint) | **GREEN** |
  | a bug or a failure | **RED** |
  | not yet verified / still open / not built yet | **dashed YELLOW outline** + a tag ("not yet verified", "idea · not built yet") |

  Ponder cards are the toolkit's standard card (solid YELLOW border, "Pause and ponder"); only a
  *dashed* YELLOW outline means "still open". Emphasis uses WHITE `Indicate`/`Circumscribe`,
  not `highlight_box` (which is YELLOW).
- People: "the user" only, never a name, on screen or in narration. Charts drawn from git must
  replace the author field with "the user" / "the agent". The user's words are quoted lightly
  cleaned (filler words removed, meaning unchanged; `…` marks a cut), with the caption "— the
  user (dictated; filler words removed)" for the first request and "— the user (request for the
  Chinese versions)" for the third, which is quoted verbatim. Summaries of the requests are
  written in the third person and captioned "requests, summarized", so they never read as quotes.
- Phrasing guardrails (binding, from the fact sheet): "a simulated 12-year-old", never "a
  12-year-old"; "the speech recognizer heard …", never "the voice said …"; "no recorded human
  review yet"; "183 sub-agents in 46 workflow runs, before this video"; the Karpathy line is "as
  quoted" in the request and the README; no numbers on 3Blue1Brown's production effort; the cost
  is only ever shown with its full label. Perception verbs ("watch", "see", "listen") are not used
  for AI reviewers, except S06's deliberate "this is how it watches".
- Chinese characters on screen use Noto Sans CJK SC (the English build does not switch fonts by
  itself).
- Code on screen: the toolkit's code style, real excerpts only, with file path and line numbers
  as a GREY caption. Panels show one or two lines; the rest is faded.
- Icons the toolkit lacks (headphones, play button, pen, clock, terminal window, video-player
  frame, "AI" badge) are drawn from Manim primitives in `scenes/common.py`; no icon fonts or
  outside SVGs. People are `person_icon`; papers and files are `paper_card`-style cards.
- Every scene starts and ends on an empty frame (STYLE_GUIDE §3); chapter titles are the
  `video.yaml` scene titles.
- Spelling: American, on screen and in SAY ("color", "catalog", "recognizer", "math"), to match
  the subtitles of the tic-tac-toe video.
- Tone: friendly, concrete, honest; no hype. "The agent" = Claude Code; "sub-agents" = the agents
  it launches in workflows. One idea per beat.
- Pronunciation watch list (there is no recorded check by ear of the English voice either): every
  SAY sentence was run through the voice's own phonemizer (`kokoro_onnx.tokenizer`, espeak), with
  no audio made. Manim, Karpathy, 3Blue1Brown and Claude come out right. So do v2's new words:
  Mandarin, epsilon, lint, playground, example, cataloging, re-render, API, PDFs and "say line" /
  "show line". A speech-recognizer round trip of all 46 say lines (assets/en_asr_roundtrip.yaml: 0.9 % word
  differences) found one misread name, Andrej, now fixed in `lexicon.yaml`. In v1, "SAY" was spelled out and "2.2." was
  split in two; both are fixed above. Before the final render, run the speech-recognizer round
  trip on all SAY lines (ASSETS.md A19 shows the command). Bilibili and Xiaoyi stay out of SAY
  (both are misread).
- S11's last beat assumes this video is built with this same toolkit. If it isn't, cut its second
  and third sentences ("This video was made the same way …" and "You can.").

Live values (refresh right before the final render; they are the only facts that may change)

| value | lives in | snapshot when this script was written | how to refresh |
|---|---|---|---|
| session cost counter | `video.yaml` → `live.cost_usd` (read by `scenes/common.py`; never spoken) | 1507.47 (USD, last `cost-state` record, at `60258b4`) | ASSETS.md A40 |
| cost label | `video.yaml` → `live.cost_label`, rendered as is (split into two lines at " · ") | "… all four requests …" | if a fifth request arrives before the render, ask the user; the label and S03's last SAY say "all four requests" |
| commit timeline | `assets/commits.csv`, frozen at `bb3fc1e` (98 commits) | 103 commits at `d4043cd` (101 by the agent, 2 by the user, 32 WIP); narration says "over a hundred, all but two by the agent" (118 at the scene review) | ASSETS.md A11; above about 110 commits, say "over a hundred" |
| subtitle tool | S10 card 3 (S10 say line 4 speaks only of round 1) | round 1: 19 of 21 fixed (own report), 11 regressions; round 2 WIP (`7c6fcc0`); round 3 committed as `3aace23` (44 tests; its commit note: "Both adversarial editors judge round 3 a clear net improvement"); round 4 under way | `git log --oneline -- explainer/subtitles.py`; reword card 3's round-3/round-4 line to the latest reviewed round |
| Chinese privacy final cut | S10 card 3 ("not rendered when this script was written") | only 480p drafts in `output/zh/` (Oct 6 15:08) | `ls -la videos/dwork2006-calibrating-noise/output/zh/` |
| licensed (Azure) clips | S10 card 2 ("0 when this script was written") | no `.cache/tts/azure/`, no AZURE env vars | `ls .cache/tts` |
| recorded human listening | S08 SAY 3, S10 SAY 1 | none on record | the transcript; ask the user |

Editing `video.yaml` marks every scene stale, so update it once, right before the final render. On
screen the cost always carries the label "API list-price equivalent for the whole session · all
four requests, not the cost of one video".

---

## S01 · Made by something that can't watch it — `s01_hook.py` · `Hook`

SHOW: Black frame. A GREY video-player frame (rounded rectangle, pause icon, scrubber) fades in
holding the tic-tac-toe "before" frame: the board with X's top row YELLOW and the faded, dashed
ghost marks; on the right, the formula line reads "4 × 3 × 2", a gap, then a GREEN "12". Tag
top-right: "the old draft, redrawn from its saved code" (A03 exists: a real frame of the
old code, re-rendered at commit 8a922bf). Caption under the player:
"from a draft of 'Why are there exactly 255,168 games of tic-tac-toe?' · made for ages 11 to 14".
[REAL A03 re-render]
SAY: Here's what a paused frame looked like in an early draft of one of these videos, about tic-tac-toe, for kids around 12. Look at the line on the right: 4 times 3 times 2, and then 12.

SHOW: PONDER(6 s, "If you were 12,\nwhat would you think went wrong?") with the frame still visible,
dimmed to 40 %.
SAY: Pause for a moment. If you were 12, what would you think went wrong here?

SHOW: The card leaves. The GREEN "12" glides down under the board, and the frame cross-fades to the
real fixed layout (A01, the 23.0 s tile, cropped: the formula line reads "4 × 3 × 2 × 1" and
"ghost endings counted: 19" sits under the board, with a GREY gloss arrow "a running count, now
under the board"); the tag changes to "real frame, after the fix". A RED tag points at the old
spot: "the math was right · the layout was wrong". A faded-BLUE `person_icon` with a small "AI"
badge enters left, with a speech bubble from the review notes (A10, `qa_round1.txt` line 30): "Paused
frames read '4 × 3 × 2      12' … which look like wrong multiplication." Label under the icon: "a
simulated 12-year-old (an AI reviewer)". [REAL A03 re-render → REAL A01; REAL A10]
SAY: It looks like bad multiplication, but the math was right. The 12 was a running count on its way to 24, sitting on the formula's line. The layout lied. And the reviewer who caught it wasn't a child. It was an AI, pretending to be a 12-year-old.

SHOW: Everything shrinks to the left. A row of icons builds: one PINK `person_icon` ("the user"),
one BLUE icon ("the agent: Claude Code"), a cluster of small faded-BLUE icons ("sub-agents"). Three
GREY chips drop out of the BLUE icons as they are named: "script" · "animation code" · "checks".
Over the BLUE and faded-BLUE icons, a GREY headphones glyph and a GREY play-button glyph appear,
each struck through in RED. [DIAGRAM]
SAY: Now the strange part. Almost everything in these videos was made by AI agents: the script, the animation code, and the checks. And none of them can hear the narration, or press play. So how do they know any of it works?

SHOW: Title "How these videos are made"; five chips line up under it and pulse as they are named:
"the pipeline" (GREY) · "who did what" (half PINK, half BLUE) · "how it's checked" (GREEN) · "the
Chinese versions" (GREY, with a small 中) · "what still needs a human" (dashed YELLOW outline).
[DIAGRAM]
SAY: This video covers the pipeline, who did what, how work gets checked without eyes or ears, the Chinese versions, and what still needs a human.

---

## S02 · What the user asked for — `s02_ask.py` · `TheAsk`

SHOW: A PINK `person_icon` ("the user") with a stack of GREY paper cards growing beside it, faster
than a small GREY clock can tick. Then a short lineage row of GREY `paper_card`-style cards joined
by `connect` arrows: "3Blue1Brown · explainer videos animated with code" → "Manim · the Python
library written for them" → "Manim Community Edition · v0.21.0, used here" → a BLUE card
"explainers built by an AI agent". Above the last card, a GREY quote card: "fully custom /
bespoke explainer videos generated on any arbitrary topic", caption "Andrej Karpathy, as quoted in
the first request and the repo README". [REAL A05; DIAGRAM]
SAY: It started with one person, the user: a researcher with more papers to read than time. The look comes from 3Blue1Brown, whose videos are animated in Manim, where every frame is drawn by code. The idea for this project came from a post by Andrej Karpathy, as quoted in the first request.

SHOW: PINK quote cards, one at a time, each captioned "— the user (dictated; filler words
removed)": (1) "Our brain is a neural net … it takes hardship, turmoil, dedication, pain … to
train ourselves." (2) "AI is very patient, but at the same time, I'm doing a lot of cognitive
offloading." The words "cognitive offloading" turn RED. Exact card texts: ASSETS.md A06. [REAL A06]
SAY: The user's own words go further: our brain is a neural net, and training it takes hardship. AI is patient, they said, but they were doing a lot of cognitive offloading.

SHOW: Cards (1) and (2) slide up small. Card (3): "It's like the explainer video is a mentor …", and
a second small card, "they're never isolated", beside a small thumbnail of the privacy video's
lineage map (A07, at 2:30: Warner 1965 → disclosure control → Sweeney 1997 → Evfimievski 2003),
caption "papers are never isolated · the privacy video at 2:30". Card (4): "What is the next step?
… I feel like it's definitely something interactive, something that demands the user to actually
create …". The word "interactive" gets a dashed YELLOW outline and the tag "idea · not built yet".
[REAL A06, A07]
SAY: A video should be a mentor, showing how papers connect, because they're never isolated. And video is only a first step: the next is something interactive, where the learner has to make things.

SHOW: The cards clear. Four PINK request cards drop onto a date axis, Oct 4 to Oct 7, with a GREY
caption "requests, summarized": "1 · a privacy paper from a friend (differential privacy) +
organize the paper library" with the A07 thumbnail · "2 · tic-tac-toe, for a middle-school kid,
with a program the user supplied" with the A08 thumbnail · "3 · Chinese versions that
code-switch, with subtitles in both languages" · "4 · this video: how they're built, and what to
improve". [REAL A07, A08; DATA dates from the request log, A06]
SAY: Then came four requests. A privacy paper from a friend, which the user hadn't read, to keep the test fair. A tic-tac-toe video, for a middle-school kid. Chinese versions of both. And this video.

---

## S03 · Who did what — `s03_team.py` · `Team`

SHOW: Four columns build left to right: PINK "the user" (one `person_icon`); BLUE "the agent:
Claude Code · one long session" (one icon); faded BLUE "sub-agents" (a grid of 183 small dots
filling in, label "183 sub-agents · 46 workflow runs · before this video"); as the workflow is
explained, a small GREY script card "workflow script" launches three of the dots, each with a job
tag: "build one scene" · "review" · "translate". GREY "tools" (chips: "Manim · animation" ·
"Kokoro · text-to-speech, English, local" · "edge-tts · online text-to-speech via Microsoft Edge
(Chinese)" · "faster-whisper · speech recognizer" · "FFmpeg · video" · "jieba · Chinese word
breaks" · "LaTeX · math"). [DATA fact sheet 2a; DIAGRAM]
SAY: The team: one human, the user. One AI agent: Claude Code. Under it, 183 sub-agents in 46 workflow runs, before this video. A workflow is a script the agent writes to launch sub-agents, each with one job. And tools, like a synthetic voice for each language and a speech recognizer.

SHOW: The PINK column expands into a checklist, ticking as each item is named: "chose the topics
and the audiences" · "uploaded 36 PDFs" · "gave the tic-tac-toe counts" · "supplied the program".
A real code panel slides up: the user's original program (A09), its comments visible verbatim and
unhighlighted, with only `next_player = "0" if player == "X" else "X"` highlighted, and a GREEN
terminal line under it: `255168`. Then a small diff chip: `"0"` → `"O"` (BLUE) · "comments
rewritten", and a GREY caption: "the cleaned file is the code on screen in the tic-tac-toe video".
[REAL A09, A24]
SAY: The user decided what was worth learning, and for whom. They uploaded 36 PDFs, gave the tic-tac-toe numbers, and supplied the program that video teaches. It already worked. The agent only changed a zero into the letter O, and rewrote the comments.

SHOW: The BLUE column expands: "toolkit · scripts · scenes · translations · voices · subtitles ·
reviews · renders". Then the commit ribbon (A11): one tick per commit from Oct 4 to Oct 7 (UTC),
the first two PINK ("the user"), the rest BLUE; a GREY gloss "commit = a saved version of the
project"; the Oct 6 burst labelled "50 commits that day"; 28 ticks carry a small GREY dot, "WIP
checkpoint"; GREY bands mark the usage-limit stops (A12), with the counter "usage-limit stops: at
least 6"; two of the restarts carry a small PINK tick, "the user: 'Please continue'" (Oct 7 02:12)
and "the user: 'Try again'" (Oct 7 20:09). Footer: "about 100 commits · 2 by the user".
[DATA A11, A12]
SAY: The agent did the rest. It wrote the toolkit that runs the pipeline, and made all but two of over a hundred commits, the project's saved versions. In under a week, work stopped at least six times on usage limits, and each time picked up where it left off.

SHOW: Two speed bars under the ribbon: "privacy video: request 15:28 → final cut 21:29 · about 6
hours (24 min of video, plus the paper library and the toolkit)" · "tic-tac-toe: request 21:53 →
final cut 01:00 · about 3 hours (12 min 37 s of video)". Then, centered, a GREY counter card
counts up to the live value from `video.yaml` (`live.cost_usd`), formatted "$1,507.47", with the
label `live.cost_label` rendered as is in two lines: "API list-price equivalent for the whole
session" / "all four requests, not the cost of one video". [DATA git + ffprobe; live value]
SAY: From request to final cut, the privacy video took about six hours, and tic-tac-toe just over three. And the cost on screen, at API list prices, is for the whole session: all four requests, not one video.

---

## S04 · A script that is code — `s04_script.py` · `ScriptIsCode`

SHOW: A file pipeline grows left to right, GREY file cards each "written" by a small BLUE pen:
"paper.pdf" → "catalog.yaml" → "digest.md · page numbers + the paper's mistakes" → "script.md" → "scenes/*.py" →
"output/ · mp4, subtitles, chapters". The motto types in above: "Every step leaves a file behind,
so you can stop, review, and resume." [REAL A13; DIAGRAM]
SAY: The pipeline is a chain of files: a paper, a catalog entry, a digest with page numbers, a script, animation code, and the video. Every step leaves a file behind, so you can stop, review, and resume.

SHOW: Two catches pop off the first cards. On "catalog.yaml": a filename card
"20_chen2016dcan_1604.02678.pdf" flips over to "inside: a math paper on topological pressure",
with "1604.02678 · DCAN is most likely 1604.02677" in RED and a tally "4 of 36 PDFs: the wrong
paper" (the flip is a redrawn moment: tag "re-created for this video"; the filename and the tally are real,
A41). On "digest.md": page 270 of the privacy paper (A14) slides in, the line "mean 0, and
standard deviation λ." underlined in WHITE, and a GREEN sticky note quotes the digest: "the true
standard deviation is √2·λ — λ is the scale". [RECON flip; REAL A41, A14]
SAY: Each file gets checked. Agents cataloging the papers read them, not just their names, and found that 4 of the 36 PDFs were the wrong papers. And the privacy digest even lists the paper's own mistakes.

SHOW: Zoom into the real tic-tac-toe `script.md` (A15): the colour table first, then the S03 block.
`SHOW:` lines get a GREY side bar labelled "the picture"; `SAY:` lines an ORANGE side bar labelled
"spoken word for word". An arrow runs from the SAY line to a small code chip
`SAY = NARRATION["S03"]` ("the scene reads this file"). Then the convention line lights up: "say
'nine factorial', never '9!'". [REAL A15, A16]
SAY: In the script, each beat pairs a show line, the picture, with a say line: the exact words the voice will speak. The animation code reads those words straight from this file. It's written for the ear: nine factorial is spelled out in words.

SHOW: Two GREY clocks: "fix a sentence in script.md: seconds" vs "fix it after animation: a
re-render". Then the false start as a time lane (Oct 4, UTC): a faded-BLUE review lane, "script
review · 15:47 → 16:30"; at 16:07 the guide is committed, with its real heading (A13,
`docs/WORKFLOW.md` at `41eca34`): "4. Review the script (before any animation)"; at 16:12–16:13
six faded-BLUE builder icons start (3 runs × 2 agents) while the review lane is still running; at
16:24 all six turn RED and fade ("stopped at 16:24, before the review was done"). [REAL A13; DATA A43]
SAY: So other agents review the script before any animation: a sentence costs seconds to fix, a scene costs a re-render. The agent wrote that rule into its own guide on day one. Minutes later, it started six sub-agents building scenes while the review was still running. Eleven minutes after that, all six were stopped.

---

## S05 · The audio is the clock — `s05_clock.py` · `AudioClock`

SHOW: A real code panel (A16): `s01_hook.py` lines 115–122 of the tic-tac-toe video
(`with self.voiceover(SAY[2]) as vo:` … `vo.wait_until("A hundred")` … `vo.wait_until("A million")`
… `vo.wait_until("Pause the video")`). Above it, the real SAY line it narrates (A15): "Take a guess.
A hundred? A million? Pause the video and write your guess down." Each quoted phrase in the code
glows ORANGE as it is named here, and the same words light up in the SAY line. [REAL A16, A15]
SAY: Now the animation. In this pipeline, the voice is made first, and the animation waits for words, not seconds. This code says: when the narration reaches "A hundred", show a hundred. When it reaches "A million", show a million.

SHOW: An ORANGE audio timeline drawn from real data (A17, tic-tac-toe S03, its second SAY line,
`SAY[1]`): the clip as a 23-second waveform bar (A18); GREEN ticks at its five sentence starts,
labelled once, "sentence starts: exact" (no numeric labels). Inside the first sentence its
characters spread evenly along the bar, and ORANGE anchor pins drop at their character positions,
with a dashed YELLOW outline: "inside a sentence: estimated from character counts".
[DATA A17; REAL A18]
SAY: The voice speaks one sentence at a time, so every sentence start is known exactly. Inside a sentence, the toolkit has to guess. It assumes every character takes the same time to say.

SHOW: PONDER(8 s, "362,880 has 7 characters,\nas many as the word 'example'.\nSay both out loud.
How much longer is the number?") above two strips of 7 equal boxes: 3 · 6 · 2 · , · 8 · 8 · 0
and e · x · a · m · p · l · e.
SAY: Pause and try it. The number on screen has 7 characters, as many as the word example. Say both out loud. How much longer does the number take?

SHOW: The "example" strip fades (no time is claimed for it). The 7 number boxes stretch to fit the
real waveform (A18): GREEN word bars from the speech recognizer (A19) put "362" at 0.24–1.56 s and
",880" at 1.56–3.26 s. The estimated pin for "counted those" (1.42 s, dashed YELLOW) slides right
to the measured word start (3.26 s, GREEN), leaving a RED gap labelled "+1.8 s". Caption: "word
times measured by a speech recognizer for this video, on this one clip". [REAL A18, A19; DATA A17]
SAY: About three seconds: three hundred sixty-two thousand, eight hundred eighty. Far longer than the word. So the toolkit's guess for the words right after it lands almost two seconds early.

SHOW: Real code (A20): the comment in `s03_stop.py` lines 90–92 ("(e.g. a spoken "362,880" lasts
~3 s but is only 7 characters)") and line 317, `wait_for(self, vo, "counted those", shift=2.2)`,
with `shift=2.2` glowing ORANGE. A GREEN counter: "hand-set shifts in this one scene: about 20".
Then a GREY code chip from `explainer/voice.py` line 463 (A21),
`edge_tts.Communicate(text, self.voice, rate=rate).save(str(out))`, with a dashed YELLOW note:
"this service can send word times · only the audio is kept". [REAL A20, A21]
SAY: The fix so far is manual: this one scene carries about 20 hand-set shifts, the biggest two point two seconds. Yet the online voice used for Chinese can send a time for every word. The toolkit keeps only the audio.

---

## S06 · Checking without eyes or ears — `s06_watch.py` · `Watching`

SHOW: PONDER(8 s, "You can't hear the video,\nand you can't press play.\nHow would you check it?")
next to the struck-through headphones and play-button glyphs from S01.
SAY: Pause and think. Suppose you can't hear, and you can't press play. How would you check a video?

SHOW: The real contact sheet (A01) fills the frame in a GREY border; a WHITE highlight walks along
its yellow timestamps (00:00:00.933, 00:00:02.933, …). A caption builds: "16 stills · one every 2
seconds · time burned in yellow". A small BLUE agent icon "looks" at the grid along a GREY sight
line. On "sound into text", a GREY chip slides in beside the headphones glyph: "subtitles ·
speech-recognizer transcripts". [REAL A01; DIAGRAM]
SAY: The agent's answer: turn time into pictures, and sound into text. The toolkit renders a quick draft, and tiles a still from every two seconds into one grid. An agent can look at an image, so this is how it watches.

SHOW: Four real frames 0.2 s apart (A02: 19.6, 19.8, 20.0 and 20.2 s of tic-tac-toe scene 3) in a
strip; GREEN rings mark the ghost marks that moved between neighbouring frames. Caption: "frames
0.2 s apart: did anything move?". [REAL A02]
SAY: Between stills, things can go wrong, so to check motion, it grabs frames a fifth of a second apart. If they're all the same, nothing moved.

SHOW: Two GREEN check chips appear in a column, each opening a real excerpt. (1) "lint, without
drawing a frame": the real console output of `explainer.check` on tic-tac-toe scene 3 (A22), beside
its three flags "OUT · off screen", "SMALL · under 20 points", "LEFT · still on screen at the end".
(2) "the scenes check themselves": `_check_numbers()` from `s03_stop.py` lines 62–72 (A23), one
`assert` line glowing, with "82 checks in the tic-tac-toe scenes · most of them on numbers".
[REAL A22, A23]
SAY: Then it measures everything it can. A checker called a lint runs each scene without drawing a frame, and flags anything off screen, text that's too small, or objects left behind. And the tic-tac-toe scenes check themselves, with 82 checks, most of them on the numbers shown.

---

## S07 · Reviewers who pretend — `s07_reviewers.py` · `Reviewers`

SHOW: A review loop: the BLUE agent hands a "draft video" card to two faded-BLUE reviewer icons,
"director" and "a simulated 12-year-old", tagged "fresh agents · didn't build it". What each
receives floats in: "contact sheets", "subtitles = the sound", "a role". A real line from the
round-1 review instructions for the simulated kid (A42), GREY caption "from the round-1 review
instructions (tic-tac-toe)": "go through the contact sheets of every scene in order while reading
the subtitles for the same times … — that is the video." ("(the srt)" cut, marked "…"). Then a speech bubble from the simulated kid
(A10, `qa_round1.txt` line 38): "… couldn't work out what X0 meant (X's zeroth move?)".
[REAL A10, A42; DIAGRAM]
SAY: Next come the reviewers, fresh agents that didn't build the video. They get the stills, the subtitles as a stand-in for sound, and a role: a director, or a simulated 12-year-old, sharp but ordinary. That simulated kid found real problems, like move labels it couldn't decode.

SHOW: A funnel for tic-tac-toe (A10): round 1 "30 issues: 3 wrong · 13 confusing · 14 polish" →
"fix round" → round 2 "a fresh director re-checked all 30: 25 fixed · 5 partly fixed · 0 wrong",
plus "18 new or remaining notes". The "12 on the formula line" item from S01 is pulled out of the
round-1 list and glows. Beside it, small, a score card in a dashed YELLOW outline: "simulated kid:
8/10 → 8.5/10 · a model's guess, not a real child's · the second kid had read the first one's
notes". [DATA A10]
SAY: Round one found 30 issues, including that 12 on the formula line. In round two, a fresh director re-checked each one: 25 were fixed, and 5 only partly.

SHOW: The frozen shuffle, before and after. Left, "before": four frames 0.2 s apart, the same
spacing as the "after" strip, in which the ghost marks don't move while the GREEN counter creeps on
(A03, re-rendered from the old code: the counter reads 5, 5, 6, 7), RED tag "frozen", plus the
A03 tag "the old draft, redrawn from its saved code"; under it one line of the real old code (A25, `s03_stop.py` at
`8a922bf`, line 280): `ghosts[start[cur[p]]].animate(path_arc=arc) .move_to(...)`, with `.animate`
RED, the rest faded. Right, "after": the real moving strip (A02); under it one line of the real fix
(A26, `s03_stop.py` line 203): `return lambda: [m.animate(path_arc=path_arc).move_to(p) for m, p in moves]`,
with `lambda` GREEN and the docstring as a GREY caption: "The `.animate`s are made only when the
step plays." [REAL A03 re-render, A25, A26, A02]
SAY: The director caught a subtler bug. The scene should shuffle 4 marks through all 24 orders, but the board froze while the counter ticked on. The cause is a Manim pitfall: every move was prepared before any played, so each overwrote the last. Now each move is prepared as it plays.

SHOW: Four mini scene cards from the privacy video (scenes 3 to 6), each with a small faded-BLUE
builder icon: the name tags read "Dan" in scenes 3 and 4 and "Dev" in scenes 5 and 6, with a RED
"≠". A wide faded-BLUE bar labelled "cross-scene reviewer (whole-video review)" sweeps across the
cards and the tags settle on "Dan". Below, five differently drawn budget bars collapse into one
shared drawing. Source caption: "privacy video, whole-video review notes" (A38). [DIAGRAM; DATA A38]
SAY: Some problems only show across scenes. In the privacy video, agents building different scenes named the same person Dan in one part and Dev in another. Only a reviewer looking across scenes could catch that.

---

## S08 · Same video, second language — `s08_language.py` · `SecondLanguage`

SHOW: A PINK request card (A06b), verbatim: "… there are a lot of terms that are derived from
English and would thus sound weird directly translate that into Chinese." Caption: "— the user
(request for the Chinese versions)". On "The key rule", a real aligned entry (A27, tic-tac-toe
`i18n/zh/narration/g1.yaml` lines 21–30): the English SAY line split into its three sentences on
the left, the three Chinese sentences on the right, joined one to one by GREY lines; the anchor
`"Flipped or turned": "翻转"` glows ORANGE and an ORANGE pin jumps from the English words to the
Chinese word. A counter: "417 sentence pairs · both videos". [REAL A06b, A27]
SAY: On to Chinese. The user asked to keep English terms that would sound weird translated, with subtitles in both languages. The key rule: one Chinese sentence for each English sentence, so every animation cue still has a sentence to wait for.

SHOW: One GREY "scene code" card feeds two outputs, "English video" and "Chinese video". Then two
columns of frame fingerprints scroll: "English render, before" vs "after the Chinese edits", rows
turning GREEN "=", footer "tic-tac-toe scene 1, English 480p preview: all 721 frames match" (A37).
The real rule from `docs/LANGUAGES.md` (A36): "The English video is never touched". A dashed YELLOW
footnote: "a few scenes don't render exactly the same every time". [REAL A36, A37; DIAGRAM]
SAY: Both languages share the same scene code, so the agent checks that the English video didn't change. It compares a fingerprint of every frame, before and after. A few scenes don't render exactly the same every time, but most match.

SHOW: The voice bake-off (A28): an ORANGE waveform labelled "Mandarin voice 1 ·
zh-CN-XiaoxiaoNeural" flows into a GREY box "speech recognizer", which prints in RED "noise →
Nice", "epsilon → Excellent", "Claude → Clark". Then "the chosen voice · zh-CN-XiaoyiNeural" →
GREEN "17 of 17 terms · 10 of 10 numbers", with a GREY footnote "a fuzzy match: 'Claude Shannon'
came back as 'Cloud Shannon'". A small scoreboard: "Brian (male, English-first) 0.997 · Ava
(female, English-first) 0.991–0.995 · Xiaoyi (native Mandarin) 0.991 · Xiaoxiao 0.933". Footer in a
dashed YELLOW outline: "chosen by speech recognition · no recorded check by ear yet". [REAL A28]
SAY: Then, which voice? The agent can't listen, so it asked a speech recognizer. With the first Mandarin voice, the recognizer heard "Nice" where the script said noise, and "Excellent" where it said epsilon. Another voice passed all 17 test terms, and was chosen. There's no record yet of anyone checking it by ear.

SHOW: A redrawn frame of the Chinese tic-tac-toe video at 11:43 (A30 on the A04 picture, tag
"re-created for this video · the old cue text, as both AI reviewers quoted it"): the game tree under 轮到 X /
轮到 O, and in the band below "不是电脑能做的，不只是统计对局" over the English line "No. A computer can
do more than count." The Chinese line is glossed "It's not what a computer can do, not just
counting games", with a RED "meaning flipped" stamp; the English line stays WHITE. Two small
faded-BLUE reviewer icons each raise a RED flag on the cue. [RECON A30; REAL A04]
SAY: And one subtitle flipped a meaning. The English narration answers with a short no, then says a computer can do more than count. The Chinese subtitle said the opposite: that this is not something a computer can do. Both AI reviewers of the Chinese version caught it.

SHOW: PONDER(10 s, "The English is right.\nThe Chinese says the opposite.\nIs this a translation mistake?")
over the reconstructed frame.
SAY: Pause on this one. The English line is right, and the Chinese says the opposite. Was this a bad translation?

---

## S09 · Bugs in the machinery — `s09_machinery.py` · `Machinery`

SHOW: The real fixed frame (A04, the Chinese final cut at 11:43, commit 68d6c23), caption "real
frame · Chinese tic-tac-toe final cut": the band reads "不是。电脑能做的，不只是统计对局"; the 。
pulses WHITE. The cue splits into two layers: "content: the translation" with a GREEN ✓, and
"tool: the subtitle merger" with a RED ✗ and the real fix commit subject (A35, `cd67aa4`):
"Subtitles: keep sentence punctuation in merged cues; …". [REAL A04, A35]
SAY: It wasn't. The translation had a full stop after that no, but the subtitle tool dropped it when it merged that short subtitle into the next. Tool bugs often look like content bugs.

SHOW: A file timeline: scene files edited, their movies older, each with a RED tag "older than
source" [DIAGRAM], under the real commit line (A35, `5be60d7`): "A plain build used to reuse any
existing scene movie, so edited scenes were silently stitched from stale renders." On "file
dates", two real date checks: a faded-BLUE reviewer icon holds the note from the privacy video's
newcomer review (A44, caption "a reviewer · privacy video, Oct 4"): "The renders are older than the
source."; and the BLUE agent icon lines up the dates it listed just before the fix (A44, caption
"the agent · tic-tac-toe, Oct 6"): "Explore.mp4 · Oct 5, 23:24" vs "s06_explore.py · committed Oct 6,
00:05", with a RED "older than source". Then the real voice stamp of a Chinese scene render (A31):
`{"speed": 1.0, "tts": "edge", "voice": "zh-CN-XiaoyiNeural"}`, caption "voice stamp of a Chinese
scene render (tic-tac-toe scene 3)", with a GREEN tag "every render now records its voice".
[REAL A35, A44, A31; DIAGRAM]
SAY: Another tool bug: a plain build used to reuse old scene movies, so edited scenes were quietly stitched from out-of-date footage. The file dates gave it away: the movies were older than the code. Now a scene is rendered again whenever it's older than its sources, or its voice has changed.

SHOW: Three lanes for the Chinese privacy video's QA (A32): "reviewers · 4 groups × (director +
simulated grad student) · 103 findings, 81 of them polish" → "4 fixers · 75 changes" → "4
skeptical verifiers · 12 corrections". One change card bounces back from the verifier lane with a
RED note from the run record: "claimed: ×1.12, within the limit · measured: ×1.153, over the
15 % limit". [DATA A32]
SAY: Fixes need checking too. For the Chinese privacy video, reviewers raised 103 points, most of them polish, and fixers made 75 changes. Then skeptical verifiers checked the fixers' work, and made 12 more corrections. One fixer said a passage now fit its time limit. It didn't.

---

## S10 · What to improve next — `s10_next.py` · `WhatNext`

SHOW: A board with four empty slots, titled with the rule: "the biggest gaps sit where measuring
runs out". Card 1 slides in, dashed YELLOW outline: "only people can do this". A PINK
`person_icon` with headphones replaces the RED-struck headphones over the agent icons (from S01).
Sub-lines: "no recorded human review of the narration yet, English or Chinese" · "English
narration: checked by a speech recognizer for this video, no human listening yet" · "every test
viewer on record: an AI persona" · "learning not measured: no quiz, no data". [DIAGRAM; DATA fact
sheet 6]
SAY: So what's next? The biggest gaps sit exactly where measuring runs out. First, what only people can do. There's no recorded human review of any narration yet. Every test viewer on record was simulated, and there's no measure yet of what anyone learned.

SHOW: Card 1 opens into two columns. PINK "decided by the user": "the topics" · "the audiences" ·
"Chinese, code-switched" · "this video". BLUE "decided by the agent · worth a second look", each
item in a dashed YELLOW outline: "privacy video: 24 min, not the 12–15 its own instructions
suggest → also cut into 2 parts" · "Chinese voice: the top scorer was male and English-first → a
native Mandarin female voice, to match the English (another female voice scored about as well)" ·
"which English words to keep: argued by simulated Chinese readers" · "small edits to the user's
program". [DATA fact sheet 6, A28]
SAY: People should also revisit the agent's own calls, like the length of the privacy video and the choice of Chinese voice.

SHOW: Card 2, "engineering", with three sub-cards, each tagged "idea · not built yet" in a dashed
YELLOW outline. "A licensed Chinese voice": the real line from `docs/LANGUAGES.md` (A36), "the free
Edge [service] is not licensed for published videos" ("endpoint" swapped for viewers, in brackets) → "Azure AI Speech: same voices, licensed ·
clips made when this script was written: 0" → "switching re-voices all 417 sentences, then re-times
them". "Word-level timing": the S05 pin snaps from its estimate onto the GREEN word bar; "then
delete the hand-set shifts · add a lint for sync, overlaps and dead air". "Shared parts": a GREEN
bar "scene code per minute of video: about 400 lines (tic-tac-toe) · about 310 (privacy)" shrinks
as a shelf of reusable parts fills (board · game tree · code panel · counter · paper card). A small
footnote card: "also: the English privacy video, part 2, opens on a black frame, voice at 0.088 s →
add a lead-in". [REAL A36; DATA]
SAY: Second, engineering: a licensed Chinese voice, since the free service isn't licensed for published videos. Timing should follow words, not characters, so the hand-set shifts can go. And shared parts would shrink the scene code.

SHOW: Card 3, "subtitles that understand sentences": a cue cut at the wrong place is re-cut by a
GREY "parser" box that proposes and a GREEN "rules" box that checks (tag "idea · not built yet");
facts underneath: "rule-based rewrite, first review round: 19 of 21 issues fixed (its own report)
· reviewers found 11 regressions" · "four rounds in all: 49 tests; rule tuning stopped at diminishing returns (its commit note)" · "privacy video, Chinese: final cut rendered with the new subtitles". [DATA]
SAY: Third, subtitles. Hand-written rules decide where to cut each sentence into subtitle lines. In its first review round, the newest version fixed most of its targets, but made 11 other subtitles worse. A sentence parser could propose the cuts, and the rules could check them.

SHOW: Card 4, "interactivity": the two real playground screenshots (A33 "Laplace Mechanism
Playground", A34 "Tic-Tac-Toe Game Counter") sit apart from a video frame, then merge into one
window, where a ponder card in the video opens the playground in the same state, with an "answer
saved" chip; the merged window carries the dashed YELLOW tag "idea · not built yet".
[REAL A33, A34; DIAGRAM]
SAY: Last, and closest to the user's vision: interactivity. The first two videos each come with a playground, a small web page to try the idea yourself, but it sits apart from the video. Next, pausing the video should open it right there, in the same state, and keep your answer.

---

## S11 · A recipe, and a request — `s11_recipe.py` · `Recipe`

SHOW: A recipe card writes itself, one line per sentence, each in its semantic colour: "1 · a
human picks the learner and the question" (PINK) · "2 · script first, as code" (GREY) · "3 · let
the audio be the clock" (ORANGE) · "4 · independent reviewers, including a simulated viewer"
(faded BLUE) · "5 · measure what you can't perceive, and check the fixes" (GREEN) · "6 · keep
every step in a file" (GREY). [DIAGRAM]
SAY: Want to try this yourself? A human picks the learner and the question. Write the script first, as code. Let the audio be the clock. Use independent reviewers, including a simulated viewer. Measure what you can't perceive, and check the fixes too. And keep every step in a file.

SHOW: The PINK quote returns (A06): "I felt like LLM should not just be cognitive offloading; it
should be something that can actually help us to make knowledge more accessible, but at the same
time achieve some sort of the same level of learning." — the user (dictated; filler words
removed). [REAL A06]
SAY: Above all, remember the goal. As the user put it, AI should not just be cognitive offloading. It should make knowledge easier to reach, and still let you learn just as deeply.

SHOW: Last frame: the tic-tac-toe playground screenshot (A34) on the left; on the right the BLUE
agent icon with the RED-struck headphones, and the line "this video was made the same way"; under
it, in a dashed YELLOW outline, "checked by measuring · the agent that made it can't listen to it".
On "You can.", a PINK `person_icon` with headphones appears beside it, and under it a GREY chip:
"something sounded wrong? say so, with the time". Then everything fades out. [REAL A34; DIAGRAM]
SAY: One last thing. This video was made the same way, so it has the same blind spot: the agent that made it can't listen to it. You can. If anything sounded wrong, or lost you, say so, with the time. That's exactly the feedback this pipeline is missing.
