# How these explainer videos are made — narration script & visual plan (v1)

Audience: viewers of the other two videos, and anyone curious how an AI agent can make an
explainer: a researcher, a student, a Bilibili or YouTube viewer. No Manim, programming or
machine-learning background assumed; the only idea we lean on is "an AI that writes and runs
code". Goal: understand (1) the pipeline: paper → digest → a script that is code → animation timed
to a synthetic voice → video with subtitles, (2) who did what: one human, one agent, many
sub-agents, many tools, (3) how an agent that can't hear or watch checks its work, by turning what
it can't perceive into things it can measure, and which real bugs that caught, (4) what is still
unverified, and what to improve next.

Facts: every number comes from the meta-video fact sheet (`FACTSHEET.md`, research snapshot
2026-10-07, repo HEAD `bb3fc1e`), using its corrected values, and its honesty notes and the user's
decisions are binding. Numbers that keep moving (the commit count, the cost counter) are phrased so
they stay true, or live in one place (see "Live values"). Every real asset a scene needs, with the
command that extracts it, is listed in `ASSETS.md` (ids `A01`…).

Conventions
- `SAY:` lines are spoken verbatim (one `voiceover` block each) and become subtitles. Written for
  the ear: symbols are spelled out ("4 times 3", "percent"); numbers that matter are written as
  digits (the narrator reads them correctly), small counts as words; never "9!", and never end a
  SAY sentence on a digit followed by "!". No abbreviations with full stops ("e.g."). A quotation
  never ends a sentence that is followed by another sentence in the same SAY line (the sentence
  splitter needs `. ` before a capital, and the Chinese version needs one sentence per English
  sentence).
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
    on-screen tag **"reconstruction"** (GREY rounded tag, top-right, 22 pt). Where `ASSETS.md`
    offers a re-render of the old commit instead (A03), the tag reads **"re-rendered from the old
    code (commit 8a922bf)"**.
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
  | not yet verified / still open | **dashed YELLOW outline** + the tag "not yet verified" |

  Ponder cards are the toolkit's standard card (solid YELLOW border, "Pause and ponder"); only a
  *dashed* YELLOW outline means "not yet verified". Emphasis uses WHITE `Indicate`/`Circumscribe`,
  not `highlight_box` (which is YELLOW).
- People: "the user" only, never a name, on screen or in narration. Charts drawn from git must
  replace the author field with "the user" / "the agent". The user's words are quoted lightly
  cleaned (filler words removed, meaning unchanged), with the caption "— the user (dictated;
  filler words removed)".
- Phrasing guardrails (binding, from the fact sheet): "a simulated 12-year-old", never "a
  12-year-old"; "the speech recognizer heard …", never "the voice said …"; "no recorded human
  review yet"; "183 sub-agents in 46 workflow runs, before this video"; the Karpathy line is "as
  quoted" in the request and the README; no numbers on 3Blue1Brown's production effort; the cost
  is only ever shown with its full label.
- Chinese characters on screen use Noto Sans CJK SC (the English build does not switch fonts by
  itself).
- Code on screen: the toolkit's code style, real excerpts only, with file path and line numbers
  as a GREY caption.
- Icons the toolkit lacks (headphones, play button, pen, clock, terminal window, video-player
  frame, "AI" badge) are drawn from Manim primitives in `scenes/common.py`; no icon fonts or
  outside SVGs. People are `person_icon`; papers and files are `paper_card`-style cards.
- Every scene starts and ends on an empty frame (STYLE_GUIDE §3); chapter titles are the
  `video.yaml` scene titles.
- Spelling: American, on screen and in SAY ("color", "catalog", "recognizer", "math"), to match
  the subtitles of the tic-tac-toe video.
- Tone: friendly, concrete, honest; no hype. "The agent" = Claude Code; "sub-agents" = the agents
  it launches in workflows. One idea per beat.
- Pronunciation watch list (the English voice has never been checked by ear either): Manim
  ("MAN-im"), Karpathy, 3Blue1Brown, Bilibili, Claude. Before the final render, run the
  speech-recognizer round trip on these SAY lines (ASSETS.md A19 shows the command) and add
  `explainer/lexicon.yaml` entries if needed (a shared file: the main agent's call).
- S11's last beat assumes this video is built with this same toolkit. If it isn't, cut its first
  two sentences.

Live values (the only numbers that must be refreshed before the final render)

| value | lives in | snapshot when this script was written | how to refresh |
|---|---|---|---|
| session cost counter | `video.yaml` → `live.cost_usd` (read by `scenes/common.py`; never spoken) | 1435.16 (USD, last `cost-state` record) | ASSETS.md A40 |
| commit timeline | `assets/commits.csv`, frozen at `bb3fc1e` (98 commits) | narration says "about a hundred, all but two by the agent" | ASSETS.md A11 |

Editing `video.yaml` marks every scene stale, so update the cost once, right before the final
render. On screen the cost always carries the label "API list-price equivalent for the whole
session · all four requests, not the cost of one video".

---

## S01 · Made by something that can't watch it — `s01_hook.py` · `Hook`

SHOW: Black frame. A GREY video-player frame (rounded rectangle, pause icon, scrubber) fades in
holding the tic-tac-toe "before" frame: the board with X's top row YELLOW and the faded, dashed
ghost marks; on the right, the formula line reads "4 × 3 × 2", a gap, then a GREEN "12". Tag
top-right: "reconstruction" (or the re-render tag, if A03 exists). Caption under the player:
"from 'Why are there exactly 255,168 games of tic-tac-toe?' · made for ages 11 to 14".
[RECON A03]
SAY: Here's a paused frame from one of these videos, a video about tic-tac-toe for kids around 12. Look at the line on the right: 4 times 3 times 2, and then 12.

SHOW: PONDER(6 s, "A 12-year-old pauses here.\nWhat would they think went wrong?") with the frame
still visible, dimmed to 40 %.
SAY: Pause for a moment. If you were 12, what would you think went wrong here?

SHOW: The card leaves. The GREEN "12" glides down under the board, and the frame cross-fades to the
real fixed layout (A01, the 23.0 s tile, cropped: the formula line reads "4 × 3 × 2 × 1" and
"ghost endings counted: 19" sits under the board); the tag changes to "real frame, after the
fix". A RED tag points at the old spot: "the math was right · the layout was wrong". A faded-BLUE
`person_icon` with a small "AI" badge
enters left, with a speech bubble from the QA notes (A10, `qa_round1.txt` line 30): "Paused frames
read '4 × 3 × 2      12' … which look like wrong multiplication." Label under the icon: "a
simulated 12-year-old (an AI reviewer)". [RECON A03 → REAL A01; REAL A10]
SAY: It looks like bad multiplication, but the math was right. The 12 was a separate counter on its way to 24, sitting on the formula's line. The layout lied. And the reviewer who caught it wasn't a child. It was an AI, told to watch like a 12-year-old.

SHOW: Everything shrinks to the left. A row of icons builds: one PINK `person_icon` ("the user"),
one BLUE icon ("the agent: Claude Code"), a cluster of small faded-BLUE icons ("sub-agents"). Over
the BLUE and faded-BLUE icons, a GREY headphones glyph and a GREY play-button glyph appear, each
struck through in RED. [DIAGRAM]
SAY: Here's the strange part. Almost everything in these videos was written, animated and checked by AI. And none of that AI can hear the narration, or watch the animation. So how does it know any of it works?

SHOW: Title "How these videos are made"; four chips line up under it and pulse as they are named:
"the pipeline" (GREY) · "who did what" (half PINK, half BLUE) · "how it's checked" (GREEN) ·
"what still needs a human" (dashed YELLOW outline). [DIAGRAM]
SAY: Here's how these explainers get made: the pipeline, who did what, how an agent that can't watch checks its work, and what still needs a human.

---

## S02 · What the user asked for — `s02_ask.py` · `TheAsk`

SHOW: A short lineage row of GREY `paper_card`-style cards joined by `connect` arrows:
"3Blue1Brown · explainer videos animated with code" → "Manim · the library written for them" →
"Manim Community Edition · v0.21.0, used here" → a BLUE card "explainers built by an AI agent".
Above the last card, a GREY quote card: "fully custom / bespoke explainer videos generated on any
arbitrary topic", caption "Andrej Karpathy, as quoted in the first request and the repo README".
[REAL A05; DIAGRAM]
SAY: The look comes from 3Blue1Brown, the user's first reference, and Manim, the animation library made for those videos. The idea of an AI making them comes from a post by Andrej Karpathy, quoted in the first request.

SHOW: PINK quote cards, one at a time, each captioned "— the user (dictated; filler words
removed)": (1) "Our brain is a neural net, and we're training our brain to update its parameter.
And I think it takes hardship, turmoil, dedication, pain, essentially, to train ourselves."
(2) "AI is very patient, but at the same time, I'm doing a lot of cognitive offloading." The
words "cognitive offloading" turn RED. Exact card texts: ASSETS.md A06. [REAL A06]
SAY: The user's own words go further. "Our brain is a neural net," they said, and training it takes hardship. AI is patient, but in their words, "I'm doing a lot of cognitive offloading."

SHOW: Cards (1) and (2) slide up small. Card (3): "It's like the explainer video is a mentor, and
it's kind of paving the path." with a second line, "They're never isolated.", beside the real
lineage frame of the privacy video (A07, at 2:30: Warner 1965 → disclosure control → Sweeney 1997
→ Evfimievski 2003), caption "papers are never isolated". Card (4): "What is the next step? …
It's definitely something interactive, something that demands the user to actually create,
generate stuff." The word "interactive" gets a dashed YELLOW outline and the tag "not built yet".
[REAL A06, A07]
SAY: So a video should be a mentor, showing how papers connect, because they're never isolated. And video is only a first step. The next one, the user said, is something interactive, where the learner has to make things.

SHOW: The cards clear. Four PINK request cards drop onto a date axis, Oct 4 to Oct 7: "1 · a
friend's paper (differential privacy) + organize my paper library" with the A07 thumbnail · "2 ·
tic-tac-toe, for a middle-school kid, with my own program" with the A08 thumbnail · "3 · Chinese
versions that code-switch, with subtitles in both languages" · "4 · this video: how you build
them, and what to improve". [REAL A06, A06b, A06c, A07, A08; DATA dates from the request log]
SAY: Then came four requests. A friend's paper on privacy, picked so the user wouldn't already know it. A tic-tac-toe video, for a middle-school kid. Chinese versions of both. And this one.

---

## S03 · Who did what — `s03_team.py` · `Team`

SHOW: Four columns build left to right: PINK "the user" (one `person_icon`); BLUE "the agent:
Claude Code · one long session" (one icon); faded BLUE "sub-agents" (a grid of 183 small dots
filling in, label "183 sub-agents · 46 workflow runs · before this video"); GREY "tools" (chips:
"Manim · animation" · "Kokoro · English voice, local" · "edge-tts · Chinese voice, online" ·
"faster-whisper · speech recognizer" · "FFmpeg · video" · "jieba · Chinese word breaks" · "LaTeX ·
math"). [DATA fact sheet 2a; DIAGRAM]
SAY: Here's the team. One human: the user. One AI agent: Claude Code, in one long session. Under it, 183 sub-agents, launched in parallel in 46 workflow runs before this video. And tools: Manim, a voice for each language, a speech recognizer, and video tools.

SHOW: The PINK column expands into a checklist, ticking as each item is named: "chose the topics
and the audiences" · "uploaded 36 PDFs" · "gave the tic-tac-toe counts" · "wrote the program". A
real code panel slides up: the user's original program (A09), with
`next_player = "0" if player == "X" else "X"` and `# undo before trying another square i suppose`
highlighted, and a GREEN terminal line under it: `255168`. Then a small diff chip: `"0"` → `"O"`
(BLUE) · "comments rewritten". [REAL A09, A24]
SAY: The user decided what was worth learning, and for whom. They uploaded 36 PDFs, gave the tic-tac-toe numbers, and wrote the program that video teaches. It already worked. The agent only changed a zero into the letter O, and rewrote the comments.

SHOW: The BLUE column expands: "toolkit · scripts · scenes · translations · voices · subtitles ·
reviews · renders". Then the commit ribbon (A11): one tick per commit from Oct 4 to Oct 7 (UTC),
the first two PINK ("the user"), the rest BLUE; the Oct 6 burst labelled "50 commits that day";
28 ticks carry a small GREY dot, "WIP checkpoint"; GREY bands mark the usage-limit stops (A12),
with the counter "usage-limit stops: at least 6". Footer: "about 100 commits · 2 by the user".
[DATA A11, A12]
SAY: The agent did the rest, including all but two of about a hundred commits. Over four days, work stopped at least six times on usage limits, and each time it picked up again, because every step leaves a file behind.

SHOW: Two speed bars under the ribbon: "privacy video: request 15:28 → final cut 21:29 · about 6
hours (24 min of video, plus the library and the toolkit)" · "tic-tac-toe: 3 h 07 min (12 min 37 s
of video)". Then, centered, a GREY counter card counts up to the live value from `video.yaml`
(`live.cost_usd`), formatted "$1,435.16", with the fixed two-line label: "API list-price
equivalent for the whole session" / "all four requests · not the cost of one video".
[DATA git + ffprobe; live value]
SAY: It was fast, too: about six hours from request to final cut for the privacy video, and just over three for tic-tac-toe. The session's cost counter is on screen, as the API list-price equivalent for the whole session, all four requests, not one video.

---

## S04 · A script that is code — `s04_script.py` · `ScriptIsCode`

SHOW: A file pipeline grows left to right, GREY file cards each "written" by a small BLUE pen:
"paper.pdf" → "catalog.yaml" → "digest.md · page numbers + errata" → "script.md" → "scenes/*.py" →
"output/ · mp4, subtitles, chapters". The motto types in above: "Every step leaves a file behind,
so you can stop, review, and resume." [REAL A13; DIAGRAM]
SAY: The pipeline is a chain of files: a paper goes into a catalog, then a digest with page numbers, a script, animation code, and finally the video. Every step leaves a file behind, so you can stop, review, and resume.

SHOW: Two catches pop off the first cards. On "catalog.yaml": a filename card
"20_chen2016dcan_1604.02678.pdf" flips over to "inside: a math paper on topological pressure",
with "1604.02678 ≠ 1604.02677" in RED and a tally "4 of 36 PDFs: the wrong paper" (the flip is a
redrawn moment: tag "reconstruction"; the filename and the tally are real, A41). On "digest.md":
page 270 of the privacy paper (A14) slides in; a GREY box zooms on "mean 0, and standard deviation
λ." and a GREEN sticky note quotes the digest: "erratum: the true standard deviation is √2·λ".
[RECON flip; REAL A41, A14]
SAY: Each file gets checked. Library agents read the papers themselves, not just the file names, and found that 4 of the 36 PDFs were the wrong paper. And the privacy digest lists the paper's own typos.

SHOW: Zoom into the real tic-tac-toe `script.md` (A15): the colour table first, then the S03 block.
`SHOW:` lines get a GREY side bar labelled "the picture"; `SAY:` lines an ORANGE side bar labelled
"spoken word for word". An arrow runs from the SAY line to a small code chip
`SAY = NARRATION["S03"]` ("the scene reads this file"). Then the convention line lights up: "say
'nine factorial', never '9!'". [REAL A15, A16]
SAY: The script is the heart of it. Each beat has a SHOW line, the picture, and a SAY line, exactly what the voice will speak, which the animation code reads straight from this file. It's written for the ear: nine factorial is spelled out, since an exclamation mark in a subtitle looks like math.

SHOW: Two GREY clocks: "fix a sentence in script.md: seconds" vs "fix it after animation: a
re-render". Then the false start as a time lane (Oct 4, UTC): at 16:07 the guide is committed,
with its real heading (A13, `docs/WORKFLOW.md` at `41eca34`): "4. Review the script (before any
animation)"; at 16:12–16:13 six faded-BLUE builder icons start (3 runs × 2 agents) while the
review lane is still running; at 16:24 all six turn RED and fade ("stopped: the script was still
changing"). [REAL A13; DATA A43]
SAY: So the script is reviewed before any animation: a sentence costs seconds to fix, an animation costs a re-render. The agent learned this the hard way. On day one, it started six scene builders while the review was still running, and minutes later all six were stopped.

---

## S05 · The audio is the clock — `s05_clock.py` · `AudioClock`

SHOW: A real code panel (A16): `s01_hook.py` lines 115–122 of the tic-tac-toe video
(`with self.voiceover(SAY[2]) as vo:` … `vo.wait_until("A hundred")` … `vo.wait_until("A million")`
… `vo.wait_until("Pause the video")`). Above it, the real SAY line it narrates (A15): "Take a guess.
A hundred? A million? Pause the video and write your guess down." Each quoted phrase in the code
glows ORANGE as it is named here, and the same words light up in the SAY line. [REAL A16, A15]
SAY: Now the animation. Here the voice is made first, and the animation waits for words, not seconds. This code says: when the voice says "A hundred", show a hundred. When it says "A million", show a million.

SHOW: An ORANGE audio timeline drawn from real data (A17, tic-tac-toe S03, its second SAY line, `SAY[1]`):
the clip as a 23-second waveform bar (A18); GREEN ticks at its five sentence starts (0, 8.5, 14.6,
17.6, 20.4 s) labelled "sentence starts: exact"; a BLUE bracket around the clip, "one voiceover
block". Inside the first sentence its characters spread evenly along the bar, and ORANGE anchor
pins drop at their character positions, with a dashed YELLOW outline: "inside a sentence:
estimated from character counts". [DATA A17; REAL A18]
SAY: The voice speaks one sentence at a time, so every sentence start is known exactly. Inside a sentence, the toolkit has to guess. It assumes every character takes the same time to say.

SHOW: PONDER(8 s, "Say it out loud: 362,880\nIt's 7 characters. How many seconds does it take?")
above a strip of 7 equal boxes: 3 · 6 · 2 · , · 8 · 8 · 0.
SAY: Pause and try it. The number 362,880 is only 7 characters long. Say it out loud. How long does it take?

SHOW: The 7 boxes stretch to fit the real waveform (A18): GREEN word bars from the speech
recognizer (A19) put "362" at 0.24–1.56 s and ",880" at 1.56–3.26 s. The estimated pin for
"counted those" (1.42 s, dashed YELLOW) slides right to the measured word start (3.26 s, GREEN),
leaving a RED gap labelled "+1.8 s". Caption: "word times measured for this video".
[REAL A18, A19; DATA A17]
SAY: About three seconds: three hundred sixty-two thousand, eight hundred eighty. So the guess for the next words lands almost two seconds early. To measure that for this video, a speech recognizer timed every word.

SHOW: Real code (A20): the comment in `s03_stop.py` lines 90–92 ("(e.g. a spoken "362,880" lasts
~3 s but is only 7 characters)") and line 317, `wait_for(self, vo, "counted those", shift=2.2)`,
with `shift=2.2` glowing ORANGE. A GREEN counter: "hand-measured shifts in this one scene: 20".
Then a GREY code chip from `explainer/voice.py` line 463 (A21),
`edge_tts.Communicate(text, self.voice, rate=rate).save(str(out))`, with a dashed YELLOW note:
"this service can send word times · only the audio is kept". [REAL A20, A21]
SAY: The fix so far is manual: this one scene carries 20 hand-measured shifts, like, move this by 2.2 seconds. Yet the online voice used for Chinese can send a time for every word. The toolkit keeps only the audio.

---

## S06 · Checking without eyes or ears — `s06_watch.py` · `Watching`

SHOW: PONDER(8 s, "You can't hear the video,\nand you can't press play.\nHow would you check it?")
next to the struck-through headphones and play-button glyphs from S01.
SAY: Pause and think. Suppose you can't hear, and you can't press play. How would you check a video?

SHOW: The real contact sheet (A01) fills the frame in a GREY border; a WHITE highlight walks along
its yellow timestamps (00:00:00.933, 00:00:02.933, …). A caption builds: "16 stills · one every 2
seconds · time burned in yellow". A small BLUE agent icon "looks" at the grid along a GREY sight
line. [REAL A01]
SAY: The agent's answer: turn time into pictures. The toolkit renders a quick draft and tiles a still from every two seconds into one grid, with the time stamped in yellow. An agent can look at an image, so this is how it watches.

SHOW: Four real frames 0.2 s apart (A02: 19.6, 19.8, 20.0 and 20.2 s of tic-tac-toe scene 3) in a
strip; GREEN rings mark the ghost marks that moved between neighbouring frames. Caption: "frames
0.2 s apart: did anything move?". [REAL A02]
SAY: Between stills, things can go wrong, so to check motion, it grabs frames a fifth of a second apart. If they're all the same, nothing moved.

SHOW: Three GREEN check chips appear in a column, each opening a real excerpt. (1) "lint, without
drawing a frame": the real console output of `explainer.check` on tic-tac-toe scene 3 (A22), beside
its three flags "OUT · off screen", "SMALL · under 20 points", "LEFT · still on screen at the end".
(2) "numbers proved by the scene": `_check_numbers()` from `s03_stop.py` lines 62–72 (A23), one
`assert` line glowing, with "82 asserts in the tic-tac-toe scenes". (3) "the code on screen is the
real program": a terminal, `python assets/play_all_games.py` → `255168` (A24). [REAL A22, A23, A24]
SAY: Then it measures everything it can. A lint runs each scene without drawing a frame, and flags anything off screen, text that's too small, or objects left behind. The scenes recompute the numbers they show, with 82 checks in the tic-tac-toe code. And the program on screen is the real file, which really prints 255,168.

---

## S07 · Reviewers who pretend — `s07_reviewers.py` · `Reviewers`

SHOW: A review loop: the BLUE agent hands a "draft video" card to two faded-BLUE reviewer icons,
"director" and "a simulated 12-year-old". What each receives floats in: "contact sheets",
"subtitles = what you hear", "a role". A real line from a QA prompt (A42): "You cannot hear the
audio." Then a speech bubble from the simulated kid (A10, `qa_round1.txt` line 38): "I couldn't
work out what X0 meant (X's zeroth move?)". [REAL A10, A42; DIAGRAM]
SAY: Then come the reviewers. They get the stills, the subtitles as a stand-in for sound, and a role: a director, or a sharp but ordinary 12-year-old. That simulated kid found real problems, like move labels it couldn't decode.

SHOW: A funnel for tic-tac-toe (A10): round 1 "30 issues: 3 wrong · 13 confusing · 14 polish" →
"fix round" → round 2 "all 30 re-checked: 25 fixed · 5 partly fixed · 0 wrong · 18 new". The
"12 on the formula line" item from S01 is pulled out of the round-1 list and glows. Beside it a
score card "8/10 → 8.5/10" in a dashed YELLOW outline, tag "a model's guess, not a real child".
[DATA A10]
SAY: Round one found 30 issues, including that 12 on the formula line. In round two, fresh reviewers re-checked each one: 25 were fixed, and 5 only partly. The simulated kid's score rose from eight to eight and a half out of ten, a model's guess, not a real child's.

SHOW: The frozen shuffle, before and after. Left, "before": four frames 0.2 s apart in which the
ghost marks don't move while a GREEN counter ticks 6 → 12 → 18 → 24, RED tag "frozen" [RECON A03,
or the A03 re-render]; under it the real old code (A25, `s03_stop.py` at `8a922bf`, lines 280–282):
`steps.append(([ghosts[start[cur[p]]].animate(path_arc=arc) .move_to(...) for p in moved], …))`,
with `.animate` RED. Right, "after": the real moving strip (A02); under it the real fix (A26,
`s03_stop.py` lines 200–203): `def moves_to(moves, path_arc): … return lambda: [m.animate(path_arc=path_arc).move_to(p) for m, p in moves]`,
with `lambda` GREEN and its docstring "The `.animate`s are made only when the step plays."
[RECON A03; REAL A25, A26, A02]
SAY: The director caught a subtler bug. The scene should shuffle 4 marks through all 24 orders, but the board froze while the counter ticked on. The cause, a known Manim pitfall: every move was prepared before any played, so each overwrote the last. Now each move is prepared as it plays.

SHOW: Five mini scene cards from the privacy video, each with a small faded-BLUE builder icon:
the name tags read "Dan" in scenes 3 and 4 and "Dev" in scenes 5 and 6, with a RED "≠"; a wide
BLUE "whole-video reviewer" bar sweeps across all five and the tags settle on "Dan". Below, five
differently drawn budget bars collapse into one shared drawing. Source caption: "privacy video,
whole-video QA notes" (A38). [DIAGRAM; DATA A38]
SAY: Some problems only show across scenes. In the privacy video, agents building different scenes named the same person Dan in one part and Dev in another. Only reviewers who watched the whole video could see that.

---

## S08 · Same video, second language — `s08_language.py` · `SecondLanguage`

SHOW: A PINK request card (A06b): "I want it to be code switching between the English language
and Chinese language. … there are a lot of terms that are derived from English and would thus
sound weird directly translated into Chinese." Then a real aligned entry (A27, tic-tac-toe
`i18n/zh/narration/g1.yaml` lines 21–30): the English SAY line split into its three sentences on
the left, the three Chinese sentences on the right, joined one to one by GREY lines. A counter:
"417 sentence pairs · both videos". [REAL A06b, A27]
SAY: Next, Chinese. The user asked to keep English terms that would sound weird translated, with subtitles in both languages. The key rule: each English sentence gets exactly one Chinese sentence, 417 pairs across both videos.

SHOW: In the same entry, the anchor `"Flipped or turned": "翻转"` glows ORANGE, and an ORANGE pin
jumps from the English words to the Chinese word on a small Chinese audio bar. Then two columns of
frame fingerprints scroll: "English render, before" vs "after the Chinese edits", rows turning
GREEN "=", footer "all 721 frames match" (scene 1, A37). The real rule from `docs/LANGUAGES.md`
(A36): "The English video is never touched". A dashed YELLOW footnote: "a few scenes never render
exactly the same twice". [REAL A27, A36, A37; DATA]
SAY: The animation still waits for English words, now re-aimed at the matching Chinese ones. To prove the English video didn't change, the agent compares a fingerprint of every frame, before and after. That works for most scenes, though a few never render quite the same twice.

SHOW: The voice bake-off (A28): an ORANGE waveform labelled "Mandarin voice 1 ·
zh-CN-XiaoxiaoNeural" flows into a GREY box "speech recognizer", which prints in RED "noise →
Nice", "epsilon → Excellent", "Claude → Clark". Then "voice 2 · zh-CN-XiaoyiNeural" → GREEN "17 of
17 terms · 10 of 10 numbers". A small scoreboard: "Brian (male) 0.997 · Ava 0.991–0.995 · Xiaoyi
0.991 · Xiaoxiao 0.933". Footer in a dashed YELLOW outline: "chosen by speech recognition · not
yet checked by ear". [REAL A28]
SAY: Then, which voice? The agent can't listen, so it asked a speech recognizer what it heard. From the first Mandarin voice, it heard "Nice" for noise, "Excellent" for epsilon, and "Clark" for Claude. A second voice got all 17 test terms right, and was chosen. Nobody has checked it by ear yet.

SHOW: A glossary card (A29, privacy video `i18n/zh/GLOSSARY.md` lines 16–17): "bin" → heard as
病 ("disease", RED, struck out), context tag "a video full of 病人, patients" → 桶 ("bucket",
GREEN). A second row: 行 ("row", heard as xíng) → 记录 ("record"). [REAL A29]
SAY: These checks even changed the wording. The recognizer heard bin as the Chinese word for disease, in a video full of patients. So bin became the word for bucket.

SHOW: The real frame of the Chinese tic-tac-toe video at 11:43 (A04): the game tree under 轮到 X /
轮到 O, and in the band below "不是。电脑能做的，不只是统计对局" over "No. A computer can do more
than count." Then a redrawn copy (tag "reconstruction · text from the old subtitle file, commit
6f9e57c", A30): the 。 lifts out and the two cues fuse into "不是电脑能做的，不只是统计对局",
glossed "It's not what a computer can do, not just counting games", with a RED "meaning flipped"
stamp; the English line underneath stays the same. [REAL A04, A30; RECON A30]
SAY: And one tiny bug flipped a meaning. The narrator says: No. A computer can do more than count. But the subtitle tool glued that short "No" onto the next line without its full stop, so the Chinese read: it's not what a computer can do. Both Chinese-speaking AI reviewers caught it on their own.

SHOW: PONDER(10 s, "The English line underneath was correct.\nSo why did this look like a translation mistake?")
over the reconstructed frame.
SAY: Pause on this one. The English line underneath was right. So why did this bug look like a bad translation?

---

## S09 · Bugs in the machinery — `s09_machinery.py` · `Machinery`

SHOW: The broken cue splits into two layers: "content: the translation" with a GREEN ✓, and
"tool: the subtitle merger" with a RED ✗ and the real fix commit subject (A35, `cd67aa4`):
"Subtitles: keep sentence punctuation in merged cues". Then a file timeline: scene files edited,
their renders older, each with a RED tag "older than source", under the real commit line (A35,
`5be60d7`): "A plain build used to reuse any existing scene movie, so edited scenes were silently
stitched from stale renders." Then the real voice stamp of a Chinese render (A31):
`{"speed": 1.0, "tts": "edge", "voice": "zh-CN-XiaoyiNeural"}`, with a GREEN tag "every render now
records its voice". [REAL A35, A31; DATA]
SAY: Because the translation was fine. The bug was in the subtitle tool, and tool bugs often look like content bugs. Once, edited scenes were quietly stitched from old renders, so reviewers judged old pictures. Now a scene is rendered again whenever it's older than its sources, or was voiced differently.

SHOW: Three lanes for the Chinese privacy video's QA (A32): "reviewers · 4 groups × (director +
simulated grad student) · 103 findings" → "fixer · 75 changes · 35 skipped, with reasons" →
"skeptical verifier · 12 corrections". One change card bounces back from the verifier lane with a
RED note from the run record: "length ratio 1.153, not 1.12: over the 15 % limit". [DATA A32]
SAY: Fixes need checking too. For the Chinese privacy video, reviewers found 103 problems, and a fixer made 75 changes. Then a skeptical verifier checked the fixer's work, and made 12 more corrections.

SHOW: Two columns. PINK "decided by the user": "the topics" · "the audiences" · "Chinese,
code-switched" · "this video". BLUE "decided by the agent · worth a second look", each item in a
dashed YELLOW outline: "privacy video: 24 min, not the 12–15 its own prompt suggests → cut into 2
parts" · "Chinese voice: the top scorer was male → a female voice, to match the English" · "which
English words to keep: argued by simulated Chinese readers" · "small edits to the user's
program". [DATA fact sheet 6]
SAY: Some choices were the agent's own, and worth a second look. The privacy video ran to 24 minutes, against the 12 to 15 its own guide suggests, so it was cut in two. The top-scoring Chinese voice was male, so the agent picked a female runner-up to match the English. And which English words to keep was argued by simulated readers, not real ones.

---

## S10 · What to improve next — `s10_next.py` · `WhatNext`

SHOW: A ranked board with six empty slots, titled with the rule: "the biggest gaps sit where
measuring runs out". Card 1 slides in, dashed YELLOW outline: "human ears and real learners". A
PINK `person_icon` with headphones replaces the RED-struck headphones over the agent icons (from
S01). Sub-lines: "no recorded human review of the narration yet, English or Chinese" · "English
narration: never checked with speech recognition either" · "every 'viewer' so far: an AI persona"
· "learning not measured: no quiz, no data". [DIAGRAM; DATA fact sheet 6]
SAY: So what's next? The biggest gaps sit exactly where measuring runs out. First, human ears and real learners. There's no recorded human review of any narration yet, every viewer so far was simulated, and nobody has measured what anyone learned.

SHOW: Card 2, "a licensed Chinese voice": the real line from `docs/LANGUAGES.md` (A36), "the free
Edge endpoint is not licensed for published videos" → "Azure AI Speech: same voices, licensed ·
clips made so far: 0" → "switching re-voices all 417 sentences, then re-times them". Card 3,
"word-level timing": the S05 pin snaps from its estimate onto the GREEN word bar; "then delete the
20 hand shifts" · "add a lint for sync, overlaps and dead air". [REAL A36; DATA]
SAY: Second, a licensed Chinese voice: the free service used now isn't licensed for published videos, and the licensed route hasn't made a single clip yet. Third, timing by words, not characters: keep the word times, or measure them, and the hand-measured shifts can go.

SHOW: Card 4, "subtitles that understand sentences": a cue cut at the wrong place is re-cut by a
GREY "parser" box that proposes and a GREEN "rules" box that checks; facts underneath: "newest
version, round 1: 19 of 21 issues fixed · 11 regressions" · "several of its 24 tests still fail" ·
"privacy video, Chinese: final cut not rendered yet". Card 5, "interactivity": the two real
playground screenshots (A33 "Laplace Mechanism Playground", A34 "Tic-Tac-Toe Game Counter") sit
apart from a video frame, then merge into one window, where a ponder card in the video opens the
playground in the same state, with an "answer saved" chip. [REAL A33, A34; DIAGRAM]
SAY: Fourth, subtitles: the newest rule-based version fixed most of its targets, but made 11 other cues worse. A sentence parser could propose the cuts, and the rules could check them. Fifth, closest to the user's vision: interactivity. Each playground is still a separate page. Next, a pause in the video should open it in the same state, and keep your answer.

SHOW: Card 6, "cheaper videos": a GREEN bar "scene code: about 420 lines per minute of video"
shrinks as a shelf of reusable parts fills (board · game tree · code panel · counter · paper
card). A small footnote card: "privacy part 2 opens on a black frame, voice at 0.088 s → add a
lead-in". [DATA]
SAY: Sixth, cheaper videos. Each minute of the tic-tac-toe video took about 420 lines of scene code. A shared library of boards, trees and code panels would cut that down.

---

## S11 · A recipe, and a request — `s11_recipe.py` · `Recipe`

SHOW: A recipe card writes itself, one line per sentence, each in its semantic colour: "1 · a
human picks the learner and the question" (PINK) · "2 · script first, as code" (GREY) · "3 · let
the audio be the clock" (ORANGE) · "4 · independent reviewers, including a simulated viewer"
(faded BLUE) · "5 · measure what you can't perceive" (GREEN) · "6 · keep every step on disk"
(GREY). [DIAGRAM]
SAY: Want to try this yourself? Here's the recipe. A human picks the learner and the question. Write the script first, as code. Let the audio be the clock. Use independent reviewers, including one who pretends to be your viewer. Measure what you can't perceive. And keep every step on disk.

SHOW: The PINK quote returns (A06): "I felt like LLM should not just be cognitive offloading; it
should be something that can actually help us to make knowledge more accessible, but at the same
time achieve some sort of the same level of learning." — the user (dictated; filler words
removed).
[REAL A06]
SAY: And keep the goal in sight. As the user put it, this should not just be cognitive offloading. It should make knowledge easier to reach, and still leave the learning to you.

SHOW: Last frame: the tic-tac-toe playground screenshot (A34) on the left; on the right a PINK
`person_icon` with headphones; between them the line "this video was made the same way", and
under it, in a dashed YELLOW outline, "no human had listened to it when this script was written".
Then everything fades out. [REAL A34; DIAGRAM]
SAY: One last thing. This video was made the same way, so it has the same blind spot: when this script was written, no human had listened to it. If you're hearing this, you may be the first. That's exactly the feedback this pipeline is missing.
