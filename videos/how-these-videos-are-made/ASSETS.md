# ASSETS: the real material each scene needs

Everything the scenes of `script.md` show as **real** (`[REAL Axx]`) or draw from real data
(`[DATA]`), with the exact source and the command that puts it into `assets/`. Copy everything
into `videos/how-these-videos-are-made/assets/` **before the first render**: `assets/*` counts as
a source of every scene, so a later copy marks all scenes stale.

Rules
- Nothing here renders this video. The only optional render is A03, of an *old commit*, in a
  scratch folder outside the repo.
- Never write the user's name into an asset. Git author fields become the role `user` / `agent`
  (A11 does this); quotes are attributed to "the user".
- `build/` folders are gitignored and re-rendered in place. Frames grabbed from them show the
  current state (after every fix). No pre-fix render survives, so every "before" picture is either
  a git text artefact, the A03 re-render, or a labelled reconstruction.
- Line numbers are pinned to commit `bb3fc1e` (the fact-sheet snapshot) with `git show`, so they
  stay valid while other sessions edit the working tree. Frames of finished videos are pinned to
  the commit that holds the mp4 (A04: `68d6c23`), because `output/` may be re-burned later.
- Revised for script v2 (2026-10-07, repo at `60258b4`): A03, A04, A06, A09, A10, A14, A20, A28,
  A31, A32, A38, A40, A41, A42 changed; A44 added; A29 is no longer used (optional cut-in).
  Final check of v2 (repo at `d4043cd`): A06 cards (3) and (4), A11 counts, A30, A44 and the
  scene-code and subtitle numbers updated.
- Marks: **V** = re-checked against the repo, git, run records or the transcript; **N** = from the
  research notes, not re-checked (re-check before rendering if it is shown as a number).

Setup (run once, from anywhere):

```bash
R=/home/user/Explainer_Videos
V=$R/videos/how-these-videos-are-made
A=$V/assets; mkdir -p $A
TTT=$R/videos/tictactoe-255168
DP=$R/videos/dwork2006-calibrating-noise
M=$TTT/build/media_h/s03_stop/videos/s03_stop/1080p60/GamesStop.mp4   # tic-tac-toe S03, 1080p60, rendered Oct 6 00:47 (after fix 1478d81)
SESSION=/root/.claude/projects/-home-user-Explainer-Videos/adc341c3-ac8a-5473-8400-37660bb7dde0
WF=$SESSION/workflows
TRANSCRIPT=$SESSION.jsonl
PY=/opt/explainer-venv/bin/python
SCRATCH=${SCRATCH:-/tmp/how-these-videos-scratch}; mkdir -p $SCRATCH     # use your session scratchpad
cd $R
```

## Index

| id | scenes | what | kind | file(s) in `assets/` |
|---|---|---|---|---|
| A01 | S01, S06 | contact sheet of tic-tac-toe S03 (+ the 23.0 s tile) | REAL image | `ttt_s03_sheet_01.png`, `ttt_s03_tile_23s.png` |
| A02 | S06, S07 | 4 frames 0.2 s apart, ghost shuffle moving | REAL frames | `ttt_s03_moving_19.6.png` … `_20.2.png` |
| A03 | S01, S07 | the "12" tally and the frozen shuffle, before the fix (draft only) | re-render of `8a922bf` (optional) or RECON | `old_s03_tally_12.png`, `old_s03_frozen_*.png` |
| A04 | S08 (base of the RECON), S09 | Chinese tic-tac-toe final at 11:43, fixed subtitle | REAL frame (mp4 from git `68d6c23`) | `ttt_zh_1143.png` |
| A05 | S02 | Karpathy line, as quoted | REAL text | (text in the scene) |
| A06, A06b, A06c | S02, S08, S11 | the user's words (3 requests) | REAL text, lightly cleaned | `quotes.yaml` |
| A07 | S02 | privacy video at 2:30, lineage timeline | REAL frame | `dp_0230.png` |
| A08 | S02 | tic-tac-toe video at 5:30, explore() code | REAL frame | `ttt_0530.png` |
| A09 | S03 | the user's original program + the cleaned one | REAL code | `user_original_program.py`, `play_all_games.py` |
| A10 | S01, S07 | QA notes, rounds 1 and 2 (persona quotes, counts) | REAL text | `qa_round1.txt`, `qa_round2.txt` |
| A11 | S03 | commit timeline up to `bb3fc1e` | DATA | `commits.csv` |
| A12 | S03 | usage-limit stops | DATA (N) | `usage_limits.csv` |
| A13 | S04 | WORKFLOW.md motto and "review first" heading | REAL text | (text) |
| A14 | S04 | privacy paper page 270 + digest erratum | REAL image + text | `dp_paper_p270.png` |
| A15 | S04, S05 | tic-tac-toe `script.md` excerpts | REAL text | `ttt_script_excerpt.md` |
| A16 | S04, S05 | `s01_hook.py` anchors; `SAY = NARRATION["S03"]` | REAL code | `ttt_s01_hook_115-122.py` |
| A17 | S05 | sentence marks of S03 `SAY[1]` | DATA | `ttt_s03_say1_marks.json` |
| A18 | S05 | audio of S03 `SAY[1]` + envelope | REAL audio (drawn) | `ttt_s03_say1.wav`, `ttt_s03_say1_env.csv` |
| A19 | S05 | speech-recognizer word times of that clip | REAL data | `ttt_s03_say1_words.txt` |
| A20 | S05 | hand shift + its comment, `s03_stop.py` | REAL code | (text) |
| A21 | S05 | `voice.py` line 463 (word times dropped) | REAL code | (text) |
| A22 | S06 | lint output for tic-tac-toe S03 | REAL console text | `ttt_s03_lint.txt` |
| A23 | S06 | `_check_numbers()` | REAL code | (text) |
| A24 | S03, S06 | `play_all_games.py` prints 255168 | REAL console text | `play_all_games.out` |
| A25 | S07 | `.animate` code before the fix (`8a922bf`) | REAL code | (text) |
| A26 | S07 | `moves_to()` after the fix | REAL code | (text) |
| A27 | S08 | aligned narration entry + anchors | REAL text | `ttt_zh_g1_entry.yaml` |
| A28 | S08 | voice bake-off results | REAL text / DATA | (text) |
| A29 | (not used in v2) | glossary rows 行 → 记录, bin → 桶 | REAL text | (text) |
| A30 | S08 | the Chinese subtitle cue, before (RECON frame) and after | REAL text (+ RECON frame) | (text) |
| A31 | S09 | voice stamp of a Chinese render | REAL text | `ttt_zh_s03_voice.json` |
| A32 | S09 | Chinese privacy QA: 103 → 75 → 12 | DATA | (numbers) |
| A33 | S10 | Laplace Mechanism Playground screenshot | REAL screenshot | `dp_playground.png` |
| A34 | S10, S11 | Tic-Tac-Toe Game Counter screenshot | REAL screenshot | `ttt_playground.png` |
| A35 | S09 | commit messages `cd67aa4`, `5be60d7` | REAL text | (text) |
| A36 | S08, S10 | `docs/LANGUAGES.md` lines 8–9, 60 | REAL text | (text) |
| A37 | S08 | frame-fingerprint report "all 721 frames match" | REAL text | (text) |
| A38 | S07 | Dev → Dan, budget bar drawn five ways | REAL text | (text) |
| A40 | S03 | session cost counter (live value) | DATA | → `video.yaml` `live.cost_usd` |
| A41 | S04 | misfiled DCAN PDF | REAL text | (text) |
| A42 | S07 | round-1 QA prompt line (English, simulated kid): "… that is the video." | REAL text | (text) |
| A43 | S04 | false start: builder runs started / killed | DATA (V) | (times) |
| A44 | S09 | stale renders seen in file dates: the privacy newcomer review ("The renders are older than the source.") and the agent's own date check before `5be60d7` | REAL text | (text) |

---

## Frames, sheets and images

### A01 · Contact sheet, tic-tac-toe S03 (V)
```bash
cp $TTT/build/sheets/s03_stop_GamesStop/sheet_01.png $A/ttt_s03_sheet_01.png      # 1950×1110, 4×4 tiles
# the 23.0 s tile (row 3, column 4): tiles are 480×270 with padding 6 and margin 6
ffmpeg -v error -y -i $A/ttt_s03_sheet_01.png -vf crop=480:270:1464:558 $A/ttt_s03_tile_23s.png
```
- The 23.0 s tile shows the fixed layout: "4 × 3 × 2 × 1" on the formula line, "ghost endings
  counted: 19" under the board. Tiles 18.9–23.0 s all show the tally under the board. In S01 the
  tally gets a GREY gloss arrow, "a running count, now under the board", so 19 doesn't read as
  another bug.
- **Do not use the 25.0 s tile**: it catches a second "24" mid-flight. That is an intended
  `TransformFromCopy` to the "counted 24 times" label, not the bug.
- If the sheet is gone, rebuild it straight from the 1080p render into `assets/` (same filter as
  `explainer/preview.py`, at 2 s per tile):
  `ffmpeg -v error -y -i $M -vf "drawtext=text='%{pts\:hms}':x=8:y=8:fontsize=h/18:fontcolor=yellow:box=1:boxcolor=black@0.6,fps=1/2,scale=480:-2,tile=4x4:padding=6:margin=6:color=white" -frames:v 1 $A/ttt_s03_sheet_01.png`
  (add `fontfile=` as `explainer/preview.py` does if ffmpeg finds no default font; timestamps then
  start at 00:00:00.000 instead of .933, so re-check the crop).

### A02 · Four frames 0.2 s apart, the shuffle moving (V)
```bash
for t in 19.6 19.8 20.0 20.2; do ffmpeg -v error -y -ss $t -i $M -frames:v 1 $A/ttt_s03_moving_$t.png; done
```
Checked: the dashed ghost marks are in different squares from frame to frame ("ghost endings
counted" 2 → 3). These are the "after" frames in S07 and the motion check in S06.

### A03 · Before the fix: the "12" on the formula line and the frozen shuffle (optional re-render)
These existed only in the round-1 draft (the 12:03 480p draft reviewed by QA run `wf_4be30e32`,
Oct 5 23:25); `1478d81` (23:56) fixed both before the final cut `525bf2a`, so no finished video
showed them. Caption them as a draft (S01). The bug was in `s03_stop.py` at commit `8a922bf` (fixed in `1478d81`): the GREEN counter sat at
the position of the final "24" on the formula line (`count_tex(k + 2, formula[8].get_center(), …)`),
and every `.animate` was built before playing. Re-rendering that commit reproduces both, as a real
render of the old code:
```bash
OLD=$SCRATCH/old_8a922bf; mkdir -p $OLD && git -C $R archive 8a922bf | tar -x -C $OLD
cd $OLD && EXPLAINER_CACHE=$R/.cache/tts KOKORO_MODEL_DIR=/opt/tts-models PYTHONPATH=$OLD \
  $PY -m explainer.preview videos/tictactoe-255168/scenes/s03_stop.py GamesStop -q m --every 0.5
# then full-size frames where the contact sheet shows "4 × 3 × 2 … 12" and the frozen ghosts
# (block SAY[1] starts at about 10.2 s; "4 times 3" is spoken about 20.5 s into the scene):
cd $OLD && EXPLAINER_CACHE=$R/.cache/tts KOKORO_MODEL_DIR=/opt/tts-models PYTHONPATH=$OLD \
  $PY -m explainer.preview videos/tictactoe-255168/scenes/s03_stop.py GamesStop -q m --at 20.6,21.0,21.4,21.8,22.2
cd $R
```
- Copy the chosen frames to `$A/old_s03_tally_12.png` and `$A/old_s03_frozen_1.png` …
  `_4.png` (4 frames 0.2 s apart during the shuffle, the same spacing as the A02 "after" strip,
  where the ghosts don't move). Timing check: the old shuffle ran 23 steps between about 17.6 and
  23.4 s of the scene (`qa_round1.txt` line 125; step durations `max(0.17, 0.45·0.9^k)` scaled to
  the budget), about 0.25 s per step, so 4 frames 0.2 s apart show the counter moving by only one
  or two steps.
- On screen the tag reads **"re-rendered from the old code (commit 8a922bf)"**.
- Check the frames really show the bug (renders are not perfectly reproducible; the old narration
  may be re-synthesised if it is not in the cache). The QA note to match: `qa_round1.txt` line 30
  ("'4 × 3 × 2      12' and '4 × 3 × 2 × 1      22'") and line 125 (the shuffle "does not play").
- **Fallback (RECON):** build the frame in Manim from today's S03 layout: the board, the formula
  "4 × 3 × 2" and a GREEN "12" where "= 24" will go; for the frozen strip, 4 identical boards
  0.2 s apart with the counter at 9, 10, 10, 11 (consistent with about 0.25 s per step). Tag:
  **"reconstruction"**.

### A04 · Chinese tic-tac-toe final at 11:43, the fixed subtitle (V)
Pinned to the final-cut commit: the working-tree `output/zh/tictactoe-255168.mp4` may be re-burned
with the newer subtitle tool before the assets are copied, and then 703.0 s would no longer show
the `68d6c23` cue.
```bash
git -C $R show 68d6c23:videos/tictactoe-255168/output/zh/tictactoe-255168.mp4 > $SCRATCH/ttt_zh_68d6c23.mp4
ffmpeg -v error -y -ss 703.0 -i $SCRATCH/ttt_zh_68d6c23.mp4 -frames:v 1 $A/ttt_zh_1143.png
```
Shows the game tree (轮到 X / 轮到 O) and, in the subtitle band, "不是。电脑能做的，不只是统计对局" over
"No. A computer can do more than count." (cue `00:11:42,030 --> 00:11:45,400`). The burned
version scales the picture to 87 % and puts the subtitles in their own band. S09 shows this frame
as is (caption "real frame · Chinese tic-tac-toe final cut"); S08's broken frame is this picture
with the old cue text redrawn in the band (A30, "reconstruction").

### A07 · Privacy video at 2:30, the lineage map (V)
```bash
ffmpeg -v error -y -ss 150 -i $DP/output/dwork2006-calibrating-noise.mp4 -frames:v 1 $A/dp_0230.png
```
Warner 1965 → disclosure control → Sweeney 1997 → Evfimievski 2003, with the Sweeney table.
(A second real frame, the Laplace derivation in semantic colour, is at 690 s if a scene needs it.)

### A08 · Tic-tac-toe video at 5:30, explore() (V)
```bash
ffmpeg -v error -y -ss 330 -i $TTT/output/tictactoe-255168.mp4 -frames:v 1 $A/ttt_0530.png
```
The real `explore()` code panel with "← someone won?" and a small board.

### A14 · Privacy paper, page 270 (Definition 1) and the erratum (V)
```bash
cp $DP/assets/paper_p6.png $A/dp_paper_p270.png          # 1195×1834, printed page 270
git show bb3fc1e:videos/dwork2006-calibrating-noise/digest.md | sed -n '29,30p;81p'
```
- The line "mean 0, and standard deviation λ." sits at about y = 1245 px of 1834 (68 % down),
  x ≈ 120–600 px: underline it in WHITE (no zoom box in v2). Show the page with
  `components.paper_page()`.
- The sticky note quotes digest lines 29–30 exactly: "the true standard deviation is √2·λ — λ is
  the scale". (Line 81 says the same in short: "p. 270: "standard deviation λ" for Lap(λ) — the
  scale is λ, the std is √2λ.") It is an error in the paper, not a typo: S04 says "mistakes".

### A33, A34 · Playground screenshots (headless Chromium is installed)
```bash
HS=/opt/pw-browsers/chromium_headless_shell-1194/chrome-linux/headless_shell
$HS --no-sandbox --hide-scrollbars --virtual-time-budget=3000 --window-size=1280,800 \
    --screenshot=$A/dp_playground.png  file://$DP/playground.html     # "Laplace Mechanism Playground"
$HS --no-sandbox --hide-scrollbars --virtual-time-budget=3000 --window-size=1280,800 \
    --screenshot=$A/ttt_playground.png file://$TTT/playground.html    # "Tic-Tac-Toe Game Counter"
```
Google Fonts may be blocked, so the page falls back to system fonts; that's fine. If the
screenshots fail, show the pages' real titles on GREY window frames and tag them "reconstruction".

---

## The user's words (A06, A06b, A06c)

Source: the user messages in `$TRANSCRIPT` (pick them by timestamp; other records may quote the same
words): first request 2026-10-04T15:28:29Z, voice-dictated;
Chinese request 2026-10-06T01:31:00Z; this video's request 2026-10-07T20:13:45Z). Extract to
check the wording:
```bash
/usr/bin/python3 -I - "$TRANSCRIPT" <<'EOF'
import json, sys
for line in open(sys.argv[1]):
    try: r = json.loads(line)
    except ValueError: continue
    m = r.get("message") or {}
    if m.get("role") != "user": continue
    c = m.get("content") or ""; t = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    if any(k in t for k in ("cognitive offloading", "code switching between", "how you build these explainer")):
        print("=====", r.get("timestamp")); print(t[:9000])
EOF
```
The first request opens with a pasted post (the Karpathy part); the user's own words start at
"So this is something that I uh, came across…". Write the cleaned texts below to
`$A/quotes.yaml`. Cleaning = filler words and false starts removed ("uh", "um", repeated words,
"overload, uh, offloading" → "offloading"), nothing else; `…` marks a cut. Hedges ("I feel
like", "I think") are not filler: keep them. Cards on screen are cut with `…` to about 15 words so
they can be read while the narration runs. Captions: "— the user (dictated; filler words removed)"
for the first request; "— the user (request for the Chinese versions)" for A06b, which is quoted
verbatim (it was not dictated and has no fillers). The S02 request cards are summaries in the
third person, captioned "requests, summarized"; they are not quotes.

| card | lightly cleaned (on screen) | original (for the check) |
|---|---|---|
| S02 (1) | "Our brain is a neural net … it takes hardship, turmoil, dedication, pain … to train ourselves." (full cleaned text: "Our brain is a neural net, and we're training our brain to update its parameter. And I think it takes hardship, turmoil, dedication, pain, essentially, to train ourselves.") | "Our our brain is a neural net, and we're training our brain um, to update its parameter. And I think it only it takes hardship, turmoil, dedication, pain, essentially, to to train ourselves." |
| S02 (2) | "AI is very patient, but at the same time, I'm doing a lot of cognitive offloading." | "Yeah, AI is very patient, but at the same time, I'm doing a lot of cognitive offloading." |
| S02 (3) | "It's like the explainer video is a mentor …" (the request continues "and it's kind of paving the path") | "it's like the explainer video is is, is a mentor as a mentor and it's it's kind of paving the path" |
| S02 (3b) | "they're never isolated" (a separate small card: in the request it comes before card 3) | "but th they're never isolated, right?" |
| S02 (4) | "What is the next step? … I feel like it's definitely something interactive, something that demands the user to actually create …" (keeps the hedge "I feel like"; the request continues "generate stuff, right?") | "what is the next step? And I feel like it's definitely something interactive, something that demands the user to actually create, generate stuff, right?" |
| S11 | "I felt like LLM should not just be cognitive offloading; it should be something that can actually help us to make knowledge more accessible, but at the same time achieve some sort of the same level of learning." | "And I felt like LLM should not just be cognitive overload, uh, offloading; it sh should be something that can actually help us to make knowledge more accessible, but at the same time achieve some sort of the same level of of learning." |
| S08 (A06b) | verbatim excerpt: "… there are a lot of terms that are derived from English and would thus sound weird directly translate that into Chinese." (no grammar edits) | "…I want it to be code switching between the English language and Chinese language. The thing is that there are a lot of terms that are derived from English and would thus sound weird directly translate that into Chinese." |
| S02 request card 3 (summary) | "subtitles in both languages": paraphrase of "This is a good example where you have both English and Chinese subtitles, and thus it would benefit more people." (do not show the Bilibili URL; it carries tracking parameters) | |
| S02 request card 4 (A06c, summary) | "this video: how they're built, and what to improve", from "how you build these explainer videos … what are you looking to improve in the future" | "can you build a explainer video in terms of how you build these explainer videos? Like what did you do, and what are you looking to improve in the future when making these videos" |

S02 request card 1 (summary) "a privacy paper from a friend": the source is "the PDF that my
friend sent me that he's working on … I want it to be fair … I have no idea what this paper is
about". The paper is Dwork, McSherry, Nissim and Smith (TCC 2006), not the friend's own paper.
S02 SAY 1 "a researcher with more papers to read than time" paraphrases "a researcher who is
currently learning reinforcement learning … a lot of paper I need to read, but I don't really
have the dedicated time to do so".

A05 (Karpathy, as quoted): `sed -n 7,8p README.md` → "The output format I am most bullish on is
fully custom / bespoke explainer videos generated on any arbitrary topic." — Andrej Karpathy. The
same words open the first request. Not checked against the original post: caption "as quoted".

---

## Code and text excerpts (all `git show bb3fc1e:` unless noted)

### A09 · The user's original program (V) and the cleaned version
```bash
/usr/bin/python3 -I - "$TRANSCRIPT" > $A/user_original_program.py <<'EOF'
import json, sys
for line in open(sys.argv[1]):
    try: r = json.loads(line)
    except ValueError: continue
    if not str(r.get("timestamp", "")).startswith("2026-10-05T21:53"): continue
    m = r.get("message") or {}
    c = m.get("content") or ""; t = c if isinstance(c, str) else " ".join(x.get("text", "") for x in c if isinstance(x, dict))
    if "WIN_LINES" in t:
        s = t.index("WIN_LINES = ("); e = t.index("print(play_all_games())") + len("print(play_all_games())")
        print(t[s:e]); break
EOF
$PY $A/user_original_program.py            # prints 255168 (the program was complete and runnable)
cp $TTT/assets/play_all_games.py $A/play_all_games.py
diff $A/user_original_program.py $A/play_all_games.py | head -40
```
Highlight in S03: only `next_player = "0" if player == "X" else "X"` (a zero) and the GREEN
`255168`. The comments stay visible, verbatim and unhighlighted (they are the user's own words;
the diff chip "comments rewritten" already makes the point). The agent's changes: "0" → "O",
comments rewritten. The program arrived pasted in the request, opening with a task docstring
("Write a program that writes every tic tac toe outcome…"), so S03 says the user "supplied" it.

### A10 · QA notes, tic-tac-toe rounds 1 and 2 (V; no names inside)
```bash
cp $TTT/build/qa_round1.txt $TTT/build/qa_round2.txt $A/
sed -n '2p;7p;30p;38p;125p' $A/qa_round1.txt; sed -n '2p;62p' $A/qa_round2.txt
```
- Round 1, line 30 (S01): "Paused frames read '4 × 3 × 2      12' and '4 × 3 × 2 × 1      22',
  which look like wrong multiplication."
- Round 1, line 38 (S07): "… couldn't work out what X0 meant (X's zeroth move?)." (the bubble
  starts with "…": the source line reads "…so I saw 'O3' under a mark labelled 2 and couldn't
  work out…"; do not add "I")
- Round 1, line 2: "about 8/10"; round 2, line 2: "VERDICT: 8.5/10"; round 2, line 62: "25 are
  fixed and 5 are partly fixed. I found nothing "wrong" this round."
- Counts for the S07 funnel (fact sheet 2d, re-checked by the v1 facts review): round 1 = 30
  issues (3 wrong, 13 confusing, 14 polish); round 2 = the director re-checked all 30 (25 fixed,
  5 partly, 0 wrong) plus 18 new or remaining notes (some overlap between the kid and the
  director, and some are round-1 leftovers: label them "18 new or remaining notes").
- The score card 8/10 → 8.5/10 is not independent: the round-2 kid prompt says "You may skim
  qa_round1.txt to know what another kid struggled with" (`$WF/scripts/qa2-ttt-video-wf_494cce6b-731.js`
  line 47). Show it only with both caveats: "a model's guess, not a real child's · the second kid
  had read the first one's notes".
- Label every quote "a simulated 12-year-old (AI persona)" or "AI director".

### A13 · WORKFLOW.md (V)
```bash
git show 41eca34:docs/WORKFLOW.md | sed -n '4p;67p;73p'     # as committed at 16:07 on Oct 4
```
"Every step leaves a file behind, so you can stop, review, and resume." · "## 4. Review the script
(before any animation)" · "Fixing a sentence here costs seconds; fixing it after animation costs a
re-render."

### A15 · Tic-tac-toe script.md (V)
```bash
git show bb3fc1e:videos/tictactoe-255168/script.md | sed -n '12,22p'   # conventions + colour table ("never '9!'")
git show bb3fc1e:videos/tictactoe-255168/script.md | sed -n '74,84p'   # S03 header + SHOW/SAY beats
git show bb3fc1e:videos/tictactoe-255168/script.md | sed -n '44p'      # the SAY line A16 narrates
```

### A16 · Anchors in code (V)
```bash
git show bb3fc1e:videos/tictactoe-255168/scenes/s01_hook.py | sed -n '115,122p'
git show bb3fc1e:videos/tictactoe-255168/scenes/s03_stop.py | sed -n '28p'     # SAY = NARRATION["S03"]
git show bb3fc1e:videos/tictactoe-255168/scenes/common.py  | sed -n '31p'     # NARRATION = load_narration(PROJECT / "script.md")
```
Lines 123–126 of `s01_hook.py` are an i18n comment and the ponder card: cut the panel at 122.

### A17 · Sentence marks of S03 `SAY[1]` (V)
```bash
$PY -c "import json; b = json.load(open('${M%.mp4}.subs.json'))[1]; print(json.dumps(b))" > $A/ttt_s03_say1_marks.json
```
`start 10.233`, `end 33.252` (23.02 s); marks `[[0, 0.0], [96, 8.533], [172, 14.571], [211, 17.579],
[257, 20.437]]` (character offset, seconds). The toolkit's estimate for a phrase = linear in the
character offset inside its sentence (`explainer/voice.py`, `Clip.time_of`): "counted those"
(offset 16) → 16/96 × 8.533 = 1.42 s.

### A18 · The audio of that block, and an envelope to draw (V)
```bash
ffmpeg -v error -y -ss 10.233 -t 23.019 -i $M -vn -ac 1 -ar 24000 $A/ttt_s03_say1.wav
$PY - "$A/ttt_s03_say1.wav" "$A/ttt_s03_say1_env.csv" <<'EOF'
import sys, wave, numpy as np
w = wave.open(sys.argv[1]); x = np.frombuffer(w.readframes(w.getnframes()), np.int16) / 32768
hop = w.getframerate() // 50                                   # one value per 20 ms
env = [float(np.sqrt(np.mean(x[i:i + hop] ** 2))) for i in range(0, len(x), hop)]
open(sys.argv[2], "w").write("t,rms\n" + "".join(f"{i * 0.02:.2f},{v:.5f}\n" for i, v in enumerate(env)))
EOF
```
Draw the waveform from the CSV (no audio is played in this video except the narration).

### A19 · Speech-recognizer word times (V)
The research for this video ran faster-whisper large-v3-turbo on that clip (it took about 90 s on
4 CPU cores). Save this as `$SCRATCH/asr_words.py` (not in the repo) and run it:
```python
import sys
from faster_whisper import WhisperModel
m = WhisperModel("/opt/tts-eval/models/faster-whisper-large-v3-turbo", device="cpu", compute_type="int8", cpu_threads=4)
segs, info = m.transcribe(sys.argv[1], language=sys.argv[2] if len(sys.argv) > 2 else "en", word_timestamps=True, beam_size=5)
for s in segs:
    for w in s.words:
        print(f"{w.start:6.2f} {w.end:6.2f} {w.word}")
```
```bash
/opt/tts-eval/asr-venv/bin/python $SCRATCH/asr_words.py $A/ttt_s03_say1.wav en > $A/ttt_s03_say1_words.txt
```
Expected: "362" 0.24–1.56 s, ",880" 1.56–3.26 s, "counted" 3.26–4.00 s, "as" 5.64 s, "4" (in "4
times 3") 10.42 s. Errors vs the estimate: "counted those" +1.8 s, "as if the players" +1.0 s,
"4 times 3" −1.1 s. The same script on this video's own clips is the pronunciation check for the
watch list in `script.md`.

### A20 · The hand shift and its comment (V)
```bash
git show bb3fc1e:videos/tictactoe-255168/scenes/s03_stop.py | sed -n '90,92p;317p'
```
"(e.g. a spoken "362,880" lasts ~3 s but is only 7 characters)." · `wait_for(self, vo, "counted
those", shift=2.2)`. The scene carries 20 `shift=` arguments from −1.1 s to +2.2 s (fact sheet
2c, V). One is 0.0 (line 522), and two phrases are shifted twice with the same value (lines
564/567 and 568/571), so S05 says "about 20". They were set by the agent from pauses in the audio
("measured from the pauses in this narration's audio"), not by ear: call them "hand-set", never
"hand-measured". Language versions switch them off (`if i18n.active(): shift = 0.0`, lines 97–98).

### A21 · Word times are dropped (V)
```bash
git show bb3fc1e:explainer/voice.py | sed -n '463p'
```
`asyncio.run(edge_tts.Communicate(text, self.voice, rate=rate).save(str(out)))`. edge-tts 7.2.8's
`Communicate` can stream `WordBoundary` events; `.save()` keeps only the audio. The installed
Kokoro ONNX model outputs only audio (no durations), so English word times must be measured.

### A22 · Lint output (run it; a dry run, no frames drawn)
```bash
PYTHONPATH=$R $PY -m explainer.check $TTT/scenes/s03_stop.py GamesStop > $A/ttt_s03_lint.txt 2>&1; echo "exit $?" >> $A/ttt_s03_lint.txt
git show bb3fc1e:explainer/check.py | sed -n '1,9p;100,111p'     # the three flags and their print format
```
Show the real output. If it is clean, show it as clean, and show the flag formats
(`[  t s] OUT …`, `[  t s] SMALL 18.0pt Text 'label'`, the final leftover list) as "output format",
not as a finding.

### A23 · Numbers proved by the scene (V)
```bash
git show bb3fc1e:videos/tictactoe-255168/scenes/s03_stop.py | sed -n '62,72p'
grep -hE '^\s*assert\b' $TTT/scenes/*.py | wc -l        # 82
```

### A24 · The real program prints 255168 (V)
```bash
$PY $TTT/assets/play_all_games.py | tee $A/play_all_games.out          # 255168
```
Show as a terminal: `python assets/play_all_games.py` → `255168`. Scenes S06–S07 of the
tic-tac-toe video show its lines 23–35 (`common.py` line 150: `PROGRAM = PROGRAM_PATH.read_text()`, so the panel is the file itself).

### A25, A26 · The `.animate` pitfall, before and after (V)
```bash
git show 8a922bf:videos/tictactoe-255168/scenes/s03_stop.py | sed -n '280,282p'   # before
git show bb3fc1e:videos/tictactoe-255168/scenes/s03_stop.py | sed -n '200,203p'   # after (moves_to)
```
Before: `steps.append(([ghosts[start[cur[p]]].animate(path_arc=arc) .move_to(spot[p] +
offset[start[cur[p]]]) for p in moved], durations[k - 1], 0))`. After: `def moves_to(moves,
path_arc: float):` … `"""… The `.animate`s are made only when the step plays."""` `return lambda:
[m.animate(path_arc=path_arc).move_to(p) for m, p in moves]`. Cause (QA round 1, line 125): each
`.animate` overwrites the mobject's single `.target`, so every mark jumps to its final spot.

### A27 · An aligned narration entry (V)
```bash
git show bb3fc1e:videos/tictactoe-255168/i18n/zh/narration/g1.yaml | sed -n '21,30p' > $A/ttt_zh_g1_entry.yaml
```
One English SAY line (3 sentences) → 3 Chinese sentences, and anchors including
`"Flipped or turned": "翻转"`. 417 = 158 (tic-tac-toe) + 259 (privacy) sentence pairs.

### A28 · Voice bake-off (V)
Source: `$WF/wf_4ab45a89-932.json` (workflow `zh-tts-bakeoff`) and commit `875166f`.
```bash
git log -1 --format=%B 875166f | sed -n '3,6p'
grep -o "noise/epsilon/Claude heard as Nice/Excellent/Clark" $WF/wf_4ab45a89-932.json | head -1
grep -o "Ranking within edge-tts:[^\"]\{0,120\}" $WF/wf_4ab45a89-932.json | head -1
grep -o "None of this has been checked by ear." $WF/wf_4ab45a89-932.json | head -1
```
- zh-CN-XiaoxiaoNeural: composite 0.933, term recall 0.82; "noise → Nice, epsilon → Excellent,
  Claude → Clark" (what the recognizer heard; the run notes say "not verified by ear").
- zh-CN-XiaoyiNeural: 0.991, 17/17 terms, 10/10 numbers, by the judge's fuzzy match (for Claude
  Shannon it heard "Cloud Shannon"): S08 says "passed all 17 test terms", not "got them right".
- en-US-BrianMultilingualNeural (male, an English multilingual voice): 0.997, the top score.
  en-US-AvaMultilingualNeural (female, English multilingual): 0.991–0.995, 17/17. Ranking line:
  "Brian 0.997 > Ava 0.991-0.995 > Xiaoyi = William 0.991 > Emma 0.979 > Yunxi 0.973 > Xiaoxiao
  0.93-0.97"; the record's noise floor is about 0.04, so Ava and Xiaoyi are level. Xiaoyi was
  picked as a native Mandarin female voice, to match the English narrator (`875166f`). It was
  not the "female runner-up".
- Scoreboard labels on screen: "Brian (male, English-first) 0.997 · Ava (female, English-first)
  0.991–0.995 · Xiaoyi (native Mandarin) 0.991 · Xiaoxiao 0.933".
- Then a round trip of all 417 sentences with Xiaoyi (commit `2f452bb`, N).

### A29 · The voice changed the wording (V; not used in script v2, kept as an optional cut-in)
```bash
git show bb3fc1e:videos/dwork2006-calibrating-noise/i18n/zh/GLOSSARY.md | sed -n '16,17p'
```
Row 行 was read xíng (transcribed 型/形), so it became 记录; "bin" was read as 病 in a video full
of 病人, so it became 桶. These were measured with a speech recognizer on the earlier voices.

### A30 · The subtitle cue, before and after (V)
```bash
git show 6f9e57c:videos/tictactoe-255168/output/tictactoe-255168.zh.srt | sed -n '618,620p'        # before: the English video's Chinese sidecar (written in 7a5ec3c), timed 10:48
grep -o "11:42 then reads “不是电脑能做的，不只是统计对局”" $WF/wf_f49ebc60-495.json | head -1           # before, in the Chinese draft, as a QA reviewer quoted it
git show 68d6c23:videos/tictactoe-255168/output/zh/tictactoe-255168.zh-en.srt | sed -n '876,879p'  # after, 00:11:42,030
```
Before: "不是电脑能做的，不只是统计对局" (reads "It's not what a computer can do, not just counting
games"). After: "不是。电脑能做的，不只是统计对局" / "No. A computer can do more than count." Cause and
fix: `cd67aa4` (merged cues keep their sentence punctuation); found by both Chinese QA personas
(`$WF/wf_f49ebc60-495.json`, V: both quote "不是电脑能做的，不只是统计对局" and blame the subtitle
merger, not the translation). The burned frame of the broken cue was never kept: the S08 "before"
frame is A04 with the old text redrawn in the band, tagged "reconstruction · the old cue text, as
both QA reviewers quoted it". The `6f9e57c` file has the same text but belongs to the English
video (its Chinese sidecar), so it is supporting evidence, not the source of the Chinese frame.

### A31 · Voice stamp (V) — copy it now
The file is in a gitignored `build/` folder and is rewritten by the next Chinese render, so copy it
before anything re-renders. It was written Oct 7 02:31 (by the stamp feature, `638db72`), after the
Chinese final cut `68d6c23` (Oct 6 17:52). Caption it "voice stamp of a Chinese scene render
(tic-tac-toe scene 3)", not "final cut".
```bash
cp $TTT/build/media_h_zh/s03_stop/voice.json $A/ttt_zh_s03_voice.json    # {"speed": 1.0, "tts": "edge", "voice": "zh-CN-XiaoyiNeural"}
```

### A32 · Chinese privacy QA: reviewers → fixer → verifier (V counts; V example)
Source: `$WF/wf_b21332a2-5a8.json` (workflow `zh-qa-fix-dp`, 16 agents = 4 groups, each with a
director, a simulated grad student, a fixer and a skeptical verifier). 103 findings (1 wrong, 21
confusing, 81 polish) → 75 fixer changes (18/16/19/22 by group) → 12 verifier corrections (2/2/3/5)
(fact sheet 2d, recomputed). Not shown: "35 skipped" (changes and skips don't map one to one to
findings, so 75 + 35 > 103 would invite a wrong sum). The bounce-back example (shown as "claimed:
×1.12, within the limit · measured: ×1.153, over the 15 % limit"):
```bash
grep -o "The fixer's report puts the SuLQ block at x1.12. It is actually 19.896 s against 17.259 s, x1.153" $WF/wf_b21332a2-5a8.json | head -1
```

### A35 · Commit messages (V)
```bash
git log -1 --format=%s cd67aa4     # Subtitles: keep sentence punctuation in merged cues; clause-aligned English; 2-line cues
git log -1 --format=%B 5be60d7 | sed -n '3,5p'   # "A plain build used to reuse any existing scene movie, so edited scenes were silently stitched from stale renders. …"
git log -1 --format=%s 638db72     # Toolkit fixes found by fact-checking the language docs (the voice.json stamp)
```

### A36 · LANGUAGES.md (V)
```bash
git show bb3fc1e:docs/LANGUAGES.md | sed -n '8,9p;60p'
```
"The English video is never touched: every language-specific change in a scene is guarded by
`i18n.active()` or is a refactor that builds the same objects, and that is checked frame by
frame." · "**Publishing:** the free Edge endpoint is not licensed for published videos." The
Azure backend exists (`explainer/voice.py`) but had produced 0 clips when the script was written:
there is no `.cache/tts/azure/` and no AZURE env vars (`ls $R/.cache/tts`; re-check right before
the render, S10 says "when this script was written").

### A37 · Frame-fingerprint report (V)
```bash
grep -o "Identical: all 721 frames of the English 480p preview match the framemd5 baseline[^\"]\{0,60\}" $WF/wf_c68e2867-dcd.json | head -1
```
On screen: "tic-tac-toe scene 1, English 480p preview: all 721 frames match". Other scenes
reported 779, 1,533, 945/945, 749/749, 1,585/1,585 frames (N). Some scenes render
nondeterministically, but not always: privacy s02 differed in 2 of 4 runs (`wf_b21332a2`), and
tic-tac-toe S08 renders differ from each other by 84–124 frames (`wf_c68e2867`). So the footnote
says "a few scenes don't render exactly the same every time", never "never".

### A38 · Cross-scene drift in the privacy video (V)
```bash
f=$(ls $WF/wf_7f255fc6-*.json); grep -o "renamed the row 'Dev' to 'Dan'[^\"]\{0,80\}" $f | head -1
f=$(ls $WF/wf_acf0396b-*.json); grep -o "is drawn five different ways" $f | head -1
```
"Dev" in S05/S06, "Dan" in S03/S04. The rename was made by the `qa-dp-video` agent assigned the
scene group S04–S07 (`wf_7f255fc6`, `args.groups[1]`): a reviewer looking across a run of scenes,
not one that "watched the whole video". On screen: faded-BLUE bar "cross-scene reviewer
(whole-video QA pass)". The budget bar became a shared `common.budget_bar()` (commit `9020ce5`).

### A41 · The misfiled DCAN PDF (V)
```bash
git show --stat --format= b035291 | grep dcan          # literature/pdfs/20_chen2016dcan_1604.02678.pdf
git log -1 --format=%B 41eca34 | grep -i misfiled       # "Replace four misfiled PDFs (wrong arXiv ids) …"
f=$(ls $WF/wf_6c3794e7-*.json); grep -o "Topological Pressure of Proper Map" $f | head -1
grep -o "most likely arXiv 1604.02677" $f | head -1
```
Four PDFs were the wrong paper (DCAN, Cellpose, TopoLoss, MILD-Net); three were replaced, Cellpose
is flagged for the user to fetch. The flip-card moment is redrawn: tag "reconstruction". The
catalog agent wrote that DCAN is "most likely arXiv 1604.02677": label it "most likely
1604.02677", not "≠".

### A42 · The QA prompt (V)
S07 depicts the English tic-tac-toe review, so it quotes the English round-1 prompt for the
simulated kid (run `wf_4be30e32`, the one that found the "12" and the X0 labels), stored in the
run record's `script` field:
```bash
/usr/bin/python3 -I -c "import json,sys; s=json.load(open(sys.argv[1]))['script']; i=s.index('go through the contact sheets'); print(s[i:i+150])" $WF/wf_4be30e32-fea.json
# → go through the contact sheets of every scene in order while reading the subtitles for the same times (the srt) — that is the video.
```
Caption: "from the round-1 QA prompt (tic-tac-toe)". The line "You cannot hear the audio." exists
only in the Chinese QA prompts (`$WF/scripts/zh-qa-ttt-wf_f49ebc60-495.js` line 39): don't use it
for the English review.

### A44 · Stale renders, seen in the file dates (V)
```bash
f=$(ls $WF/wf_acf0396b-*.json); grep -o "The renders are older than the source.\*\* All 13 renders date from[^\"]\{0,90\}" $f | head -1
```
"**The renders are older than the source.** All 13 renders date from about 18:24–18:34, before
commit 5b369a5 (18:47) and other edits." (the privacy video's newcomer QA, Oct 4). Show the first
sentence, without the asterisks, captioned "a reviewer · privacy video, Oct 4".

The fix itself (`5be60d7`, Oct 6 00:07) followed the agent's own date check, not this note: at
2026-10-06T00:06:51Z the transcript shows it listing
`build/media_l/s06_explore/videos/s06_explore/480p15/Explore.mp4` dated 2026-10-05 23:24:02
after a rebuild, while `s06_explore.py` had been edited since (commit `36f3450`, Oct 6 00:05:52).
Draw that pair as text (DIAGRAM, caption "the agent · tic-tac-toe, Oct 6"). Check:
```bash
TZ=UTC git log -1 --date=format-local:'%F %H:%M:%S' --format='%h %ad %s' 36f3450
```
S09 says only "The file dates gave it away", which covers both.

---

## Data for charts

### A11 · Commit timeline, frozen at bb3fc1e (V)
```bash
git log bb3fc1e --reverse --date=iso-strict --format='%aI%x09%an%x09%s' | $PY -c "
import sys, csv, datetime as dt
req = [('setup', '2026-10-04T00:00'), ('privacy', '2026-10-04T15:28'), ('tictactoe', '2026-10-05T21:53'),
       ('chinese', '2026-10-06T01:31')]
w = csv.writer(sys.stdout); w.writerow(['utc', 'role', 'wip', 'phase'])
for line in sys.stdin:
    t, author, subject = line.rstrip('\n').split('\t', 2)
    u = dt.datetime.fromisoformat(t).astimezone(dt.timezone.utc)
    phase = [p for p, s in req if u.strftime('%Y-%m-%dT%H:%M') >= s][-1]
    w.writerow([u.strftime('%Y-%m-%d %H:%M'), 'agent' if author == 'Claude' else 'user', subject.startswith('WIP'), phase])
" > $A/commits.csv
```
Expected: 98 rows; 2 `user` (Oct 4 14:56 and 15:22), 96 `agent`; 28 WIP; per day Oct 4 21 · Oct 5
21 · Oct 6 50 · Oct 7 6. The file holds no names. Later commits (this video's own, and the
subtitle rounds) are left out on purpose; at `d4043cd` the repo has 103 commits (101 by the agent,
2 by the user, 32 WIP). The narration says "about a hundred, all but two by the agent": re-count
right before the render (`git rev-list --count HEAD`) and switch to "over a hundred" above about
110.

### A12 · Usage-limit stops (N: from the research notes; "at least 6" is V)
Write `$A/usage_limits.csv` by hand (UTC; `reset` = when the limit lifted, `resumed` = when work
restarted, empty if unknown):
```
stop,reset,resumed
2026-10-04 19:17,2026-10-04 20:20,
2026-10-06 04:55,,
2026-10-06 10:15,2026-10-06 12:50,
2026-10-06 15:45,,
2026-10-06 18:51,2026-10-06 22:50,2026-10-07 02:12
2026-10-07 06:37,2026-10-07 07:10,2026-10-07 20:09
```
Draw a band from `stop` to `resumed` (or `reset`) where known, a plain tick otherwise. The two
restarts that came from the user's messages get a small PINK tick: "the user: 'Please continue'"
(2026-10-07T02:12:20Z, "I hit my usage limit while you were working, but it has reset now. Please
continue from where you left off.") and "the user: 'Try again'" (2026-10-07T20:09:29Z), both V
against the transcript.

### A43 · The false start (V, from the run records)
```bash
$PY - $WF <<'EOF'
import json, glob, sys, datetime as dt
for f in sorted(glob.glob(sys.argv[1] + "/wf_*.json")):
    d = json.load(open(f))
    if d.get("workflowName") == "build-dp-scenes":
        s = dt.datetime.fromtimestamp(d["startTime"] / 1000, dt.timezone.utc)
        print(f.split("/")[-1], d["status"], d["agentCount"], "start", s.strftime("%H:%M:%S"), "end", d["timestamp"])
EOF
```
3 runs × 2 agents = 6 builders; started 16:12:55–16:13:15 UTC, killed 16:24:19 UTC on Oct 4. The
guide with "review first" was committed at 16:07 (`41eca34`).

### A40 · Session cost counter (live value)
```bash
/usr/bin/python3 -I - "$TRANSCRIPT" <<'EOF'
import json, sys
last = None
for line in open(sys.argv[1]):
    if '"cost-state"' in line:
        try: last = json.loads(line)
        except ValueError: pass
print(round(last["totalCostUSD"], 2))
EOF
```
Snapshot when script v1 was written: 1435.16; when v2 was written (repo at `60258b4`): **1507.47**. Copy the latest value into `video.yaml`
→ `live.cost_usd` once, right before the final render; the counter keeps rising while this video
is made in the same session. On screen always with the full label (in `video.yaml`
`live.cost_label`): "API list-price equivalent for the whole session · all four requests, not the
cost of one video".

### Other numbers used on screen (fact sheet, V unless marked)
- 183 sub-agents in 46 workflow runs (42 completed, 4 killed) before this video; agents by phase:
  privacy + library 45 · tic-tac-toe 42 · Chinese 96.
- Privacy video: request Oct 4 15:28 → final `5fc0837` 21:29; 24:13.6; parts 14:48.1 + 9:25.6.
  Tic-tac-toe: request Oct 5 21:53 → final `525bf2a` Oct 6 01:00 (3 h 07 min); 12:36.6.
  Chinese tic-tac-toe: `68d6c23`, 13:38.7. Chinese privacy: 1080p final not rendered (only 480p
  drafts, older than the QA fixes `a824463`).
- Lexicon 17 entries; toolkit 3,521 lines at `bb3fc1e`. Scene code per minute of video (V, all
  `scenes/*.py`): tic-tac-toe 5,040 lines at the English final `525bf2a` for 12.6 min, about 400
  (5,292 at `bb3fc1e`, with the Chinese-adaptation branches); privacy 7,532 lines at `5fc0837` for
  24.2 min, about 310 (7,636 at `bb3fc1e`). So "about 400" is only the tic-tac-toe figure; S10
  shows both and the narration gives no number.
- Subtitle tool v3, round 1: 19 of 21 issues fixed, 2 partly (the implementer's own report,
  `wf_21e5261a`); 441 cues changed; reviewers found 11 regressions. Rounds 2 and 3 were committed
  as WIP after the fact sheet (`7c6fcc0` 21:14, `5b78118` 21:50); `tests/test_subtitles.py` has
  35 tests at `60258b4`. Round 3 was then committed as `3aace23` (22:42, 44 tests), whose message
  says "Both adversarial editors judge round 3 a clear net improvement" and "A fourth round
  addresses the remaining regressions" (the agent's own report, N). The script no longer quotes a
  failing-test count.
- English privacy video, part 2, starts on a black frame (0.02–0.87 s) with the voice at 0.088 s
  (V by the v1 facts review).
- Chinese privacy video: only 480p drafts in `output/zh/` (Oct 6 15:08) when v2 was written; the
  1080p final cut is in progress elsewhere. Re-check before rendering (S10 card 3).
