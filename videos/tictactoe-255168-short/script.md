# 井字棋为什么恰好有 255,168 种对局？ (4-minute short) — bar-by-bar plan (v2)

The condensed, music-led cut of `videos/tictactoe-255168`: no voice, a synthesized score, bilingual
captions (Chinese first for Bilibili; an English-first master from the same picture). 106 bars at
100 BPM = 4:14.4. The picture, the captions and the music are planned together here, bar by bar.
Numbers, boards and the glossary come from the long version; every one of them is re-checked by
`assets/check_short.py` (run it after any edit to this file, `captions.yaml` or `video.yaml`; run it
with `/opt/explainer-venv/bin/python` to include the music checks against today's composer).

Spine: **"How many games?"** (c01, asked again for chess in c26, answered by c29). Running
objects: **game A** (the cold-open game, X0 O3 X1 O4 X2), **the light pen** (it draws the first
grid, walks the search and retraces game A at the end) and **the tree** (S02's tree of 9! fill
orders, which becomes the 255,168-leaf "galaxy" in S05 and returns in S06–S09).

---

## Review log

**v2 (after three reviews of v1: facts, language, story and music).** v1's c17 (recursion) is cut, so
v1's c18–c30 are now c17–c29; ids below are v2's. Every must-fix is applied:
- c06 no longer calls the excess "games" (must-get-right item 2). It asks what 9! counted too often,
  and c08 answers that.
- c24 and c25 now ask about mistakes and answer with the result ("结果总是平局 / it is always a
  draw").
- The tree is named: c17 says 整棵树 and S02 tags "所有顺序的树 · THE TREE OF ORDERS", so c29's 这棵树
  points at something named.
- The recursion caption is cut: it crowded the acceleration. The plate tags now gloss 递归 and 回溯
  in the picture, without the un-introduced 函数.
- c07 uses the glossary's 真实的对局. c19 names only the action (删掉“判断输赢”，再跑一遍), so the
  silence holds the result and c20 names it.
- S07 and S08 are regrouped. The ledger ends on a double frame (255,168 over 9!). The results come
  straight from the ledger. There is one fly-back. The minimax wave gets 4 bars. Game A's mistake
  gets 2 bars with an inset board.
- S06's payoff now shows in the picture: ring 9 is tone-mapped with headroom, and at 67.1 it takes
  S02's look.
- Music: video.yaml now names the chords at the cues: the title on vi, bVI at the turn, I5 for the
  draw, E Lydian at 93.1, resolves at 59.1, 77.1, 101.1 and 104.1, and no boom from the silences.
  Scene joins use the soft thump. There are no motif marks. `music.chords` (the bar-by-bar
  progression), `music.joins` (segues) and hit `size` hold the rest. The toolkit's composer, being
  built alongside, now reads all three. The checker runs it on the plan: every bar's chord, key, boom,
  thump and silence comes out as planned (see "Music build notes").

Suggestions taken:
- The cold open is now a real puzzle: "=?" before "≠", c02 is a question, and a mirrored copy backs
  "flipped".
- A low D pedal keeps D as home (E9/D).
- The ledger's bass climbs E–F#–G#–A–B to D.
- The chess climax ends with the light pen trying the search on the chess strip.
- Digit labels and a "10 times per box" note go on the strips, plus "1 后面跟着 120 个零" (glossary
  H3) and 估计 in c27.
- Section labels are Chinese first, with §5 and §6 split. S04 has less text.
- The plate shows 8 lines. The coda's layout and camera are fixed.
- A new Act IV opener, c21 (a question about multiplying, not subtracting).
- Smaller caption fixes: c03, c04, c05, c10, c11, c12, c16, c22, c23, c27, c28, c29.
- The checker now also verifies every printed time.

Not taken:
- An inset following game A's leaf in S06. The re-run's arm passes game A 0.14 s into bar 65, too
  early to see.
- A label at S05 bar 54. Bars 54–58 stay wordless, and c17 names the tree.

For the user to decide:
- The colour exception. Two glowing families, X cool and O warm, against "one accent colour" (see
  Format).

---

## Acceptance checklist

Reviewers check every item; the ones marked ⚙ are also checked by `assets/check_short.py`.

### The must-get-right list (content.md §4a)

1. [ ] ⚙ **A game is the ordered list of moves, and flipped or turned versions count separately.**
   S01 bars 5–8: the same final board in another order gets "=?" and then "≠". A quarter-turned
   copy and its mirror image each get "≠". c03 states the rule. No symmetry-reduced count appears
   anywhere (neither 26,830 nor 31,896).
2. [ ] ⚙ **9! counts the orders that fill a full board; the overcount is per game: a game that ends on
   move k is counted (9 − k)! times (24, 6, 2, 1, 1; 0! = 1).**
   - S02 calls 9! *orders*, never games. c06 asks what 9! "counted too often", which c08 answers.
   - S03 shows game A counted 24 times and the ×24 ×6 ×2 ×1 ×1 row.
   - S07 stretches each ledger segment by its own factor into the line of 9!, under the unstretched
     line of 255,168.
   - Nothing on screen says or implies "9! minus some games". 362,880 and 255,168 are compared
     (S02 bar 19) and multiplied (S07), never subtracted.
3. [ ] ⚙ **The earliest end is move 5 (X's third mark); O's earliest win is move 6; draws happen only
   on a full board at move 9, and some full boards are X wins (81,792 X wins + 46,080 draws).**
   - S03 bar 29: c10 and "第 3 个 X：第 5 步".
   - S03 bars 30–31: the end-move row starts at 5, and move 6 is an O win.
   - S07 bars 73–74: the move-9 bar is cyan, then grey.
4. [ ] ⚙ **1,440 = 8 lines × 3! orders × 6 × 5 places for O's two marks, valid because nobody can have
   three marks before move 5; 5,328 = 5,760 − 432, where the 432 are move orders in which X's three
   marks already made a line parallel to O's (12 such pairs of lines × 3! × 3! orders).** S04 bars
   33–39. The 5,328 appears only as a silent annotation.
5. [ ] ⚙ **The program is an exhaustive depth-first search with undo: each finished game is counted
   exactly once, and the stopping rule is what removes the ghost continuations. It does not play
   random games and it is not "AI".**
   - S05 walks the program's real first six games in its real order: a RED undo after every branch
     and a stop bar at every leaf.
   - Then it sweeps the whole tree clockwise, in order (c15–c17).
   - S06 deletes the stop, and the ghosts come back.
6. [ ] ⚙ **X wins more games (131,184 vs 77,904), but perfect play is a draw.** S07 bars 79–80 (c23).
   S08 bars 82–89: c24, c25, and game A's one mistake, O3 on move 2, with only the centre keeping
   the draw. The first-move puzzle is cut, not half told.
7. [ ] ⚙ **Shannon (1950) gave about 10¹²⁰ as an estimate and lower bound for chess, not a count; about
   10⁸⁰ atoms is also an estimate. Keep "at least" and "about".** S08 bars 93–95:
   - c27 says 估计至少 / "By Shannon's estimate … at least".
   - c28 says 约 / "about".
   - The strip labels say 至少 / 大约 and （估计）.
8. [ ] ⚙ **Totals: Σ = 255,168; X 131,184, O 77,904, draws 46,080; Σ count × (9 − k)! = 362,880.**
   S05 bar 59, S07 bars 73–80. The per-first-move counts (corner 27,732, edge 29,592, centre 25,872)
   are never stated. The S05 counter only passes through the running totals at the wedge boundaries
   (27,732, 57,324, …, 255,168).

### Format (STYLE_PLAN §2)

- [ ] ⚙ 106 bars at 100 BPM = 4:14.4.
  - Every BARS block is whole bars and prints its own times.
  - Cuts and morphs start on a downbeat, and arrivals land on beats.
  - Counts run on subdivisions: 0.3 s for a few, 0.15 s for many.
- [ ] Silent puzzle cold open: bars 1–3 have no words at all. The puzzle is shown before it is
  answered ("=?" → "≠"). The title hits the downbeat of bar 10 (0:21.6, 8.5 % of the runtime) with a
  riser into it.
- [ ] Four acts, each opened by a question caption: I c04 (S02), II c06 (S03–S04), III c14
  (S05–S06), IV c21 (S07–S08). Then the coda (S09).
- [ ] One turn, marked by sound. c19 names the action. Bar 63 is a tape stop. Bar 64 is one bar of
  near-black and digital silence: only the struck winner check, faint, and the still light pen. Then
  the hit (S06).
- [ ] A widening scale: one board → the tree of 362,880 orders → the galaxy of 255,168 games → digit
  strips of 6, 81 and 121 boxes.
- [ ] A callback: game A, the opening image (left third, same board, same notes), replays in bars
  101–102 while the light pen retraces its path in the tree. The title returns.
- [ ] ⚙ 29 captions, one short sentence each, zh + en.
  - At most 20 Han characters and 14 English words, and at most 5.5 Han characters or 3.6 words a
    second.
  - At least 40 % of the runtime is picture-only (the checker prints the share).
  - At least 10 s without words while the counter runs to 255,168.
  - No caption over the title hit or the turn.
- [ ] ⚙ Section labels read "§n · 中文 · ENGLISH". Every label inside the picture is bilingual, and
  content labels set their English at 22 px or more at 1080p.
- [ ] No frame is still for 3 s or more: every hold below says what keeps moving (ALIVE).
- [ ] Before building S05–S06: render 1080p stills of the galaxy at 59.1 (ring 9 with 35 % of its slots
  lit) and just before 67.1 (ring 9 full, before it takes S02's look). The first must read as a
  visibly dimmer, mottled band next to the second.
- [ ] **The user confirms the colour exception.** The user asked for one glowing accent colour with a
  meaning. The plan uses two families, X cool and O warm, because the game has two players. O is kept
  a step darker than X, and every hero number glows only in the colour of what it counts.
- [ ] Music:
  - At least 80 % of logged events have an onset within 30 ms.
  - −14 ± 1 LUFS and ≤ −1 dBTP; L/R correlation > 0.
  - ⚙ Today's composer plays the named chords, keys, booms and silences of video.yaml. The "todo"
    lines are done, or knowingly waived, before the final mix.
  - **The user listens and signs off.**
- [ ] Nothing from the reference videos: no footage, music, captions, title layouts or series
  branding (the end line points to our own long version).

### Hero shots

- ★1 **S05 bars 49–59, the galaxy.** The search lights all 255,168 games.
  - The walk accelerates through the rest of the first wedge (49–50), then sweeps one first-move wedge
    per bar (51–58).
  - 12 s pass without words (c17 → c18).
  - It lands on 255,168, set like the title, with the first tonic since the opening.
- ★2 **S06 bars 64–67, the turn.** One bar of silence. Then every early leaf streams outwards into
  its grey ghost games until ring 9 is full. At 67.1 the whole ring takes S02's look and repeats its
  flare: the tree of 362,880 orders.
- ★3 **S07 bars 72–77, the ledger.**
  - The rings unroll into bars by end move, and the bars join into one line of 255,168.
  - Each segment drops a copy stretched by its ghost factor, and the copies join into one line of 9!.
  - The double frame: 255,168 over 362,880, each segment joined to its partner.
- (the climax) **S08 bars 90–98.** The pull-out along the 121-box chess strip. Then the light pen
  tries the search on it and stalls after 6 boxes.

---

## Conventions

**Clock.** 100 BPM: a beat is 0.6 s (36 frames at 60 fps), a bar is 2.4 s, and beat 0 falls on
frame 0. Bar n starts at (n − 1) × 2.4 s. "12.3" is bar 12, beat 3; "12.3+" is the eighth note
after it. Each `BARS a-b:` block is whole bars. A scene is several shots, and shot boundaries are
downbeats.

**Scenes** are `BeatScene`s (`explainer.short`).
- `play(..., beats=n)` starts on the next beat; `wait_bars(k)` waits whole bars.
- `self.mark(kind, ...)` uses the composer's kinds: hit, riser, count, particles, fx, silence and so
  on. The structural ones live in `video.yaml` music.cues.
- Every mobject gets a sound tag. X and O marks carry their square's pitch: `"X@C#5"`, `"O@G#4"`,
  from video.yaml `square_pitches`. The other tags are `"ghost@D4"`, `"draw"`, `"undo"` and `"pen"`.
- Small hits are `fx` marks: `sound="thump"` is a soft hit, `sound="boom"` a medium one with no riser.
- The `[mark: …]` notes in the SOUND lines are those calls. Everything else the composer reads from
  the event log.

Reuse from `videos/tictactoe-255168/scenes/`: `Board`, `mark`, `ghost`, `mini_board`, `win_line`,
`program_lines` (common.py), the ghost shuffle (s03) and the minimax helpers (s09). New: the galaxy,
the light pen, glow and halo sprites, slot-machine digits, digit strips, the HUD readouts and the
short style profile.

**Colour means something** (these are the only colours):

| what | colour |
|---|---|
| X: its marks, its win lines, X-win leaves and bars | cool family `#DDFFFF` → `#A3EBEF` → `#5AA9B4` → `#1B3438` |
| O: the same for O, one step darker than X | warm family `#F6C965` → `#CFA463` → `#784C2E` → `#442100` |
| draws | grey-white `#C8CCCC`, soft glow, no hue |
| ghost moves (never played) | dashed `#7D8484` at 35 %, **never glow** |
| RED `#FC6255` | undo / erase, the deleted line, "too many", "X already won", O's mistake |
| the light pen (the search) | white-hot core `#FFFFFF`, neutral halo |
| hero numbers | white core; the halo in the colour of what they count (1,440 cyan; 255,168 cool left, warm right; 362,880 neutral) |
| fill orders (S02's tree), line art, labels | hairline `#C8CCCC`, secondary `#7D8484`, on `#050505` |

Among marks and points, glow means *a real game*. Ghosts never light up, and S02's fill orders are
neutral white-grey points.

**Type.**
- Hero numbers: Inter Black, one per shot. The landing at 59.1 sets 255,168 exactly like the title.
- Maths: small and to the side in EB Garamond italic. Read it or not, nothing is lost.
- Tracked title words: Montserrat Light.
- Labels and HUD: letter-spaced Noto Sans Mono caps plus Noto Serif CJK SC.
- **Every word inside the picture is bilingual**, Chinese first, then tracked English: "8 条获胜线 · 8
  LINES". So the zh-first and en-first masters share one picture; only the burned-in captions differ.
  Labels that carry content set their English at 22 px or more at 1080p.
- Numbers are exact and comma-grouped everywhere (255,168). Maths in labels uses half-width
  brackets: 8 × 6 × (6 × 5 × 4).

**Layout.**
- One hero object, centred or on the left third; numbers go on the right third.
- The bottom 15 % is reserved for captions and the top 8 % for the HUD: the section label top-left
  (`video.yaml` sections, "§n · 中文 · ENGLISH") and live readouts top-right. Both are fixed in the
  frame (`BeatScene.hud` / `fix`).
- Captions are burned in after the render, so camera moves never drag them.

**The tree ("the galaxy")**, one geometry in S02 and S05–S09.
- It is radial, with the root at (−2.0, +0.3).
- Ring d (after d moves) sits at radius r_d = 2.9 · (d/9)^0.75 units: 0.56, 0.94, 1.27, 1.58, 1.87,
  2.14, 2.40, 2.65, 2.90.
- Every node splits its angular wedge equally among its children, clockwise in square order 0 → 8,
  starting at 12 o'clock. So a game that ends after k moves owns (9 − k)! of the 9! slots on the
  circle, which is exactly how many times 9! counted it.
- The angular share of ring k is its share of 9!: rings 5–9 hold 9.5 / 8.8 / 26.4 / 20.0 / 35.2 %.
- The program's depth-first order is the clockwise order.
- Game A's leaf sits on ring 5 at 10.12° clockwise from 12 o'clock: it is the 7,317th game the
  program finds. In S02's tree, the 24 fill orders that begin with game A's moves hold exactly the
  same 24 slots.
- Leaves are additive gaussian splats (radius ≈ 0.012, radial jitter ≤ 0.03), **tone-mapped with
  headroom**. Single slots are far below a pixel (ring 9 is about 2,500 px around at 1080p), so the
  brightness of a band is what tells a 35 % ring from a full one: no clipping before 100 %.
- Internal nodes are fainter dust. Edges are drawn only for rings 1–2 and along the light pen's path.

**Motion.**
- Arrivals ease out; zoom-throughs ease in (expo).
- Fast moves take 0.5–1.0 s, with 3–5 fading ghost copies as motion blur.
- No pop or elastic easing, and no sentence is ever "written".
- Holds stay alive (ALIVE: grain, a breathing glow, a slow drift, a live counter).

**Sound means something** (the audio twin of the colours):

| event | sound |
|---|---|
| X mark | FM bell at its square's pitch, panned to the square |
| O mark | glass tone (bar modes 1 / 2.76 / 5.40) at its square's pitch |
| draw leaf | soft wooden pluck |
| ghost mark | the same pitch, glass with a reversed attack, filtered, quiet, wet |
| undo / anything RED | short reverse whoosh |
| leaf found | a tick and a ping in the winner's timbre |
| N things counted | N ticks on the subdivision, rising |
| a hit (video.yaml cue) | sub boom (250 → 45 Hz, plus its 2nd harmonic for phones), a chord change on the downbeat, a riser 1–2 bars before |
| a scene join | the soft sub thump (a cut) or nothing (a segue, `music.joins`) |
| the light pen | a soft pulse on the beat |

Square pitches (so a game is a melody), D Lydian:

```
 C#5  D5  E5        squares 0 1 2
 G#4  A4  B4                3 4 5
 D4   E4  F#4               6 7 8
```

- Game A = C#5 G#4 D5 A4 E5 (**the motif**).
- Game B = the same five notes in another order.
- The turned copy = E5 D5 B4 A4 F#4 (other notes, falling); its mirror = C#5 D5 G#4 A4 D4.
- The program's first game = C#5 D5 E5 G#4 A4 B4 D4.

**Harmony.** D Lydian, in the composer's vocabulary. Chords change only on bar lines.

| roman | chord |
|---|---|
| I | Dmaj9 |
| II | E9 |
| iii | F#m9 |
| Vsus | Asus4 (A D E G# B) |
| vi | Bm9 |
| slash chords | E9/D, Bm9/D, E9/G#: a bass note under the chord |
| bVI | B♭maj7♯11, borrowed for the turn |
| I5 | D5, an open fifth: the draw |

- IV (G#m7♭5) and vii are never used.
- **The tonic chord is held back while a question stands, but the tonic note is not.**
  - Dmaj9 sounds only at the opening (1–3), when the program lands on 255,168 (59–60), when the
    ledger stacks to 9! (77–78) and in the coda (101–106).
  - A low D pedal sits under S03 (21–25) and the walk in S05 (43–46): E9/D is the Lydian question
    chord. So the ear keeps D as home, and the landing at 59.1 sounds like a homecoming, not a lift
    to IV of A.
- The climax lifts to E Lydian (93–98: Emaj9, F#9) and comes home through Asus4 (99).
- Every SOUND line ends with the block's chords ("Chords: 26–27 F#m9 · 28 Bm9."). The checker compares
  them with `video.yaml` music.chords, the bar-by-bar map.
- Brightness (the pad's low-pass) follows the amount of motion. Loudness stays near −14 LUFS; the
  drama comes from drop-outs and hits.

**Captions** live in `captions.yaml`, per scene, in the toolkit's format: `at` is "bar:beat" from 0
inside the scene, `dur` is in seconds.
- They are quoted here verbatim, with the same moment in this file's bar.beat numbering and in
  seconds. The checker compares all three.
- Most start half a beat after the picture event they name. A question starts on the beat that
  raises it.
- Each stays up while its evidence is on screen.

---

## Overview

| scene | bars | time | part | picture | captions |
|---|---|---|---|---|---|
| S01 | 1–11 | 0:00.0–0:26.4 | cold open, title | game A; same board in another order =? → ≠; turned and mirrored ≠; counter → **255,168** | c01–c03 |
| S02 | 12–20 | 0:26.4–0:48.0 | Act I | the tree of fill orders, 9 × 8 × … × 1 = 9! = 362,880 > 255,168 | c04–c06 |
| S03 | 21–32 | 0:48.0–1:16.8 | Act II | game A stops on move 5; its 24 ghost endings; ×24 ×6 ×2 ×1 ×1 | c07–c11 |
| S04 | 33–40 | 1:16.8–1:36.0 | Act II | 8 × 6 × 30 = 1,440 as an odometer; 5,760 − 432; the tangle | c12–c13 |
| S05 | 41–61 | 1:36.0–2:26.4 | Act III | ★1 the search: first six games, then the galaxy of 255,168 | c14–c18 |
| S06 | 62–69 | 2:26.4–2:45.6 | Act III, the turn | ★2 strike the winner check; silence; the ghosts return: 362,880 | c19–c20 |
| S07 | 70–80 | 2:45.6–3:12.0 | Act IV | ★3 rings → ledger → ×(9 − k)! → 255,168 over 9!; X / O / draws | c21–c23 |
| S08 | 81–98 | 3:12.0–3:55.2 | Act IV | minimax wave → grey root; game A's mistake; strips 6 / 121 / 81 boxes | c24–c28 |
| S09 | 99–106 | 3:55.2–4:14.4 | coda | back into the galaxy; game A replays along its path; title | c29 |

---

## S01 · How many games? 有多少种对局？ — `scenes/s01_open.py` · `ColdOpen`

Bars 1–11 (0:00.0–0:26.4) · cold open (a silent puzzle) and the title · HUD: none

BARS 1-1: (0:00.0–0:02.4)
- SHOW: Pure black, film grain, vignette. A hairline 3×3 grid (size 4.2, centred) draws itself one
  line per beat (1.1 left vertical, 1.2 right vertical, 1.3 top, 1.4 bottom), each led by the light
  pen, a white-hot dot with a small halo. Camera: a slow push-in, frame 1.00 → 0.97 over bars 1–3.
- CAPTION: —
- SOUND: Near silence (about −24 LUFS short-term). Four soft low plucks, one per line, on the beats;
  a quiet pad fades in under them. Chords: 1 Dmaj9.

BARS 2-3: (0:02.4–0:07.2)
- SHOW: Game A, one mark per beat: X0 (2.1), O3 (2.2), X1 (2.3), O4 (2.4), X2 (3.1).
  - An X is two strokes drawn in 0.25 s in the X core colour with a stacked-stroke glow; an O is one
    circle stroke in the O core colour.
  - A small grey move number (1–5) settles into the lower-right corner of each square as its mark
    lands.
  - 3.2: the top-row win line sweeps from square 0 to 2 in one beat, cyan, full glow, and the three
    X's brighten.
  - 3.3–3.4: hold; the glow breathes (ALIVE).
- CAPTION: —
- SOUND: Each mark is its square's note, X bell / O glass: C#5 · G#4 · D5 · A4 · E5, the motif,
  each panned to its square (sound tags "X@C#5" …). The win line is a 3-note upward bell run
  (C#6 D6 E6) with a soft air whoosh. Chords: 2–3 Dmaj9.

BARS 4-4: (0:07.2–0:09.6)
- SHOW: 4.1: the camera eases right so board A sits on the left third (1 beat, ease-out). A second
  grid draws on the right third, one line per beat (4.1–4.4), led by the pen.
- CAPTION c01: 「井字棋有多少种不同的对局？」 / "How many different games of tic-tac-toe are there?" (s01_open at "3:0.5" = 4.1+; 0:07.5–0:11.0)
- SOUND: The chord changes on the downbeat: the Lydian II, so the question opens. Four plucks for
  the new grid, panned right. Chords: 4 E9.

BARS 5-5: (0:09.6–0:12.0)
- SHOW: Game B on the right board, twice as fast, on eighth notes: X2 (5.1), O4 (5.1+), X0 (5.2),
  O3 (5.2+), X1 (5.3), with move numbers. 5.4: its top-row win line. Both boards now show the same
  final position with different move numbers.
- CAPTION c02: 「最后的棋盘一样：算一种对局，还是两种？」 / "Same final board: one game or two?" (s01_open at "4:3" = 5.4; 0:11.4–0:14.8)
- SOUND: The same five notes in another order, panned right: E5 · A4 · C#5 · G#4 · D5 (the motif
  scrambled), then the win run. Chords: 5 E9.

BARS 6-6: (0:12.0–0:14.4)
- SHOW: 6.1: a hairline "=?" lands between the boards. 6.1–6.3: a light runs through the move
  numbers 1 → 5 on both boards at once, one number per half beat (6.1, 6.1+, 6.2, 6.2+, 6.3). The
  eye sees the same squares lit in a different order. 6.4: the "=?" turns into "≠" with a glow pulse.
- CAPTION: —
- SOUND: 6.1: a soft suspended tone under the "=?". 6.1–6.3: both orders' notes in counterpoint on
  the half beats (left board's motif against the right board's scramble). 6.4: a soft thump for the
  "≠" [mark: fx sound="thump"]. Chords: 6 Bm9.

BARS 7-7: (0:14.4–0:16.8)
- SHOW: 7.1: board B dissolves into dust. A copy of board A, with its numbers, lifts and slides into
  B's place (7.1–7.2), and a "=?" stands between them. 7.2–7.4: the copy turns a quarter turn
  clockwise about its centre (ease-in-out, 3 motion-blur ghost copies) while its move numbers ride on
  arcs to their new squares: X2 O1 X5 O4 X8, the win line now down the right column.
- CAPTION c03: 「顺序不同，或棋盘翻转、旋转：都算不同的对局」 / "A different order, or a flipped or turned board: a different game." (s01_open at "6:3.5" = 7.4+; 0:16.5–0:20.1)
- SOUND: Six plucks panned left to right across the turn. Chords: 7 F#m9.

BARS 8-8: (0:16.8–0:19.2)
- SHOW: 8.1: the "=?" becomes "≠". 8.2: the turned copy flips over, a card flip about its vertical
  axis in one beat, into X0 O1 X3 O4 X6: game A mirrored in its diagonal, X down the left column.
  8.3: "≠" pulses again. 8.4: everything falls towards the centre (ease-in-expo) and both boards
  shrink to points.
- CAPTION: — (c03 continues)
- SOUND: 8.1: the turned game's notes as a falling figure on sixteenths, E5 · D5 · B4 · A4 · F#4.
  8.2: a soft air whoosh for the flip and its notes on sixteenths, C#5 · D5 · G#4 · A4 · D4. The
  title's 2-bar riser starts at 8.1. Chords: 8 Asus4.

BARS 9-9: (0:19.2–0:21.6)
- SHOW: In the black centre, a slot-machine counter of six digit columns scrambles: digits roll under
  black occluders with vertical ghost blur, accelerating, framed by four hairline corner brackets.
  9.4+: the frame darkens for half a beat (the breath).
- CAPTION: —
- SOUND: The riser peaks and the ticks accelerate on sixteenths. 9.4+: everything drops to silence for
  half a beat (video.yaml cue; no boom of its own). Chords: 9 Asus4.

BARS 10-10: (0:21.6–0:24.0)
- SHOW: 10.1 TITLE HIT: one white flash frame; the digits lock on **255,168**.
  - The number is Inter Black, white core, about 30 % of the frame height. Its halo is cool on the
    left half and warm on the right: X and O.
  - Under it, the wide-tracked "T I C - T A C - T O E" (Montserrat Light) and a tiny mono line
    "井字棋 · 不同的对局 · DIFFERENT GAMES".
  - Camera: slow push-in 1.00 → 0.96. ALIVE: the halo breathes; grain.
- CAPTION: —
- SOUND: The biggest boom of the film plus a bright shimmer, on vi: the number is given but not yet
  explained, so the tonic is held back (a deceptive cadence; video.yaml cue `title`, chord vi).
  Chords: 10 Bm9.

BARS 11-11: (0:24.0–0:26.4)
- SHOW: 11.1–11.2: the title dissolves. The number's glyph outlines break into about 3,000 particles,
  cool and warm, that drift apart, and the tracked words fade. 11.3–11.4: the particles swirl inwards
  and collapse into one point at (−2.0, +0.3). The point becomes a tiny empty board, the root of the
  tree, with the light pen sitting on it (a match cut into S02).
- CAPTION: —
- SOUND: The boom's tail. The particles are a soft granular shimmer whose pitch falls as they
  converge. Chords: 11 Bm9.

---

## S02 · Fill the board 填满棋盘 — `scenes/s02_fill.py` · `FillOrders`

Bars 12–20 (0:26.4–0:48.0) · Act I, opened by c04 · HUD §1 · top-right readout "顺序 · ORDERS" (the running
product) · the scene join at 12.1 is a segue

BARS 12-12: (0:26.4–0:28.8)
- SHOW: The root, an empty mini-board, breathes at (−2.0, +0.3), and the pen pulses on it. The camera
  is close (frame 0.45). A faint dashed guide circle for ring 1 draws clockwise from 12 o'clock
  (12.1–12.4).
- CAPTION c04: 「先不管输赢，填满棋盘有多少种顺序？」 / "Forget winning: in how many orders can the board fill up?" (s02_fill at "0:0.5" = 12.1+; 0:26.7–0:30.3)
- SOUND: A low A pedal starts and stays under the whole product (tension), with a soft pulse on beats
  1 and 3. Chords: 12 Asus4.

BARS 13-14: (0:28.8–0:33.6)
- SHOW: Ring 1. The pen sends nine child mini-boards out from the root, one per eighth note (13.1,
  13.1+, …, 13.4+, 14.1). Each carries one cyan X on a different square, squares 0 to 8 clockwise, and
  each trails a hairline edge. 14.1: a "9" lands on the right third and the readout shows 9.
  Ring 2. Under the first child (X on 0), the 8 O replies appear one per eighth note (14.1+ … 15.1).
  They show as small boards in a lens beside the branch, each with one amber O on a different empty
  square, and each drops its point onto ring 2.
- CAPTION: —
- SOUND: The 9 first moves are 9 bells at their squares' pitches, in square order (C#5 D5 E5 G#4 A4
  B4 D4 E4 F#4), and the 8 replies are 8 glass notes. The "9" adds the first note (D) of a chord built
  in fifths over the A pedal, one note per factor. [mark: count n=9 every=0.3; count n=8 every=0.3]
  Chords: 13–14 Asus4.

BARS 15-17: (0:33.6–0:40.8)
- SHOW: 15.1: copies of that bundle of 8 drop under the other 8 first moves (one shimmer, 1 beat):
  "× 8", readout 72.
  - Then one factor per half bar: 15.3 "× 7" → 504 (ring 3: 504 points spray along the ring), 16.1
    "× 6" → 3,024 (ring 4), 16.3 "× 5" → 15,120 (ring 5).
  - Then one per beat: 17.1 "× 4" → 60,480, 17.2 "× 3" → 181,440, 17.3 "× 2" → 362,880, 17.4
    "× 1" → 362,880 (rings 6–9).
  - From ring 3 on, nodes are neutral white-grey points: orders, not games.
  - The camera pulls out from 0.45 to 1.0 (15.1–17.4, ease-in-out) so the ring of 9 fits.
- CAPTION: —
- SOUND: Each factor is a tick plus one more note on the fifths chord, tagged by pitch (D, A, E, B,
  F#, C#, G#, then D and A an octave up). The pulse doubles to eighths in bar 16 and to sixteenths in
  bar 17. Each ring's spray is a cloud of grains, denser ring by ring, and the filter opens with
  every ring. [mark: count n=9 (factors)] Chords: 15–17 Asus4.

BARS 18-18: (0:40.8–0:43.2)
- SHOW: 18.1 HIT: ring 9 flares, 362,880 points as one dense luminous circle, and settles (this flare
  frame comes back exactly at 67.1).
  - A tiny tag at the ring: "所有顺序的树 · THE TREE OF ORDERS".
  - On the right third, the hero number **362,880** (Inter Black, neutral halo). Small beneath it,
    in EB Garamond italic: "9 × 8 × 7 × 6 × 5 × 4 × 3 × 2 × 1 = 9! = 362,880", with a tag under the
    "9!": "9 的阶乘 · NINE FACTORIAL".
  - ALIVE: the ring turns slowly (0.5°/s); grain.
- CAPTION c05: 「从 9 一直乘到 1，叫 9 的阶乘：362,880」 / "Multiplying from 9 down to 1 is called nine factorial: 362,880." (s02_fill at "6:0.5" = 18.1+; 0:41.1–0:44.7)
- SOUND: A medium boom (video.yaml hit, Vsus). The fifths chord blooms into all seven notes of D
  Lydian over the A pedal: bright but unresolved. Chords: 18 Asus4.

BARS 19-19: (0:43.2–0:45.6)
- SHOW: 19.1: the title's 255,168 drifts in under 362,880 (smaller, cool-left / warm-right halo).
  19.2: a RED ">" lands between them: "362,880 > 255,168". No difference is shown: the overcount is
  per game, not a subtraction. ALIVE: the ring keeps turning.
- CAPTION c06: 「比 255,168 还多：9 的阶乘多算了什么？」 / "More than 255,168: what did nine factorial count too often?" (s02_fill at "7:3" = 19.4; 0:45.0–0:48.8)
- SOUND: The RED ">" is a soft rub (a G natural against the chord's G#) that fades. Chords: 19 Bm9.

BARS 20-20: (0:45.6–0:48.0)
- SHOW: The question hangs while the camera dives (ease-in-expo, 1 bar) into ring 9 at 10.12°, where
  the 24 orders that begin with game A's five moves sit. Rings rush past as motion-blurred streaks
  and the numbers fly off the edges. 20.4: the frame fills with one glowing point, which resolves
  into 24 dim points (those 24 orders).
- CAPTION: —
- SOUND: A reverse swell over the bar into the downbeat of bar 21 (the cut's 1-bar riser); the A
  pedal stops at 20.4. Chords: 20 Bm9.

---

## S03 · Games stop early 对局会提前结束 — `scenes/s03_ghosts.py` · `GhostGames`

Bars 21–32 (0:48.0–1:16.8) · Act II, opened by c06 · HUD §2 · top-right readout during the shuffle
"已列出的顺序 · ORDERS SHOWN"

BARS 21-22: (0:48.0–0:52.8)
- SHOW: 21.1: the 24 points gather into board A's grid, full size and centred (the opening board).
  Game A replays one mark per beat (21.1–22.1) with its move numbers. 22.2: the top-row win line
  sweeps, cyan. 22.3: the game stops. On a thin move timeline under the board (slots 1–9), a small
  hairline stop bar drops after slot 5, and a tiny tag appears by the board: "第 5 步 · X 赢 · MOVE 5
  · X WINS".
- CAPTION c07: 「真实的对局，有人赢了就结束」 / "A real game ends as soon as someone wins." (s03_ghosts at "1:1.5" = 22.2+; 0:51.3–0:54.6)
- SOUND: The motif returns (C#5 G#4 D5 A4 E5) over a low D pedal, then the win run. 22.3: a muted
  pluck for the stop. Chords: 21–22 E9/D.

BARS 23-25: (0:52.8–1:00.0)
- SHOW: But 9! kept going.
  - 23.1–23.4: four ghost marks fill the empty squares one per beat, dashed and dim, never glowing,
    with ghost move numbers 6–9: O on 6, X on 5, O on 8, X on 7. In this order no second line forms;
    ghost lines are never drawn.
  - 24.1–25.3: the ghosts run through all 24 orders of the four squares, one per sixteenth note
    (24 × 0.15 s = 3.6 s). Numbers and marks flicker to each new arrangement (moves 6 and 8 are always
    O, 7 and 9 always X), and the readout counts 1 → 24.
  - 25.3: it lands on 24, and "4 × 3 × 2 × 1 = 24" writes small under the board.
  - 25.4: hold; the ghosts shimmer (ALIVE).
  - Picture only: the flicker is the reasoning.
- CAPTION: —
- SOUND: Ghost notes at the same square pitches (D4 B4 F#4 E4) in the ghost timbre. The shuffle is 24
  faint glassy ticks on sixteenths, rising in pitch. 25.3: a small hit [mark: fx sound="thump"]. The
  pad thins to a filtered colour with slow reversed swells, the D pedal still under it.
  [mark: count n=24 every=0.15, sound "ghost"] Chords: 23–25 Bm9/D.

BARS 26-28: (1:00.0–1:07.2)
- SHOW: 26.1: the 24 ghost endings fan out behind the board as 24 faint copies (a spread deck, ±40°):
  those 24 orders again. Every copy shares the same five bright real moves and shows a different
  dashed ending. 27.4: a tiny label above the fan, "幽灵对局 · GHOST GAMES". Bar 28: the fan drifts
  slowly, and the five real moves pulse once (ALIVE).
- CAPTION c08: 「9 的阶乘把这一局算了 24 次」 / "Nine factorial counted this one game 24 times." (s03_ghosts at "5:0.5" = 26.1+; 1:00.3–1:03.7)
- CAPTION c09: 「这些编出来的对局，叫“幽灵对局”」 / "These made-up games are called ghost games." (s03_ghosts at "6:3.5" = 27.4+; 1:04.5–1:08.0)
- SOUND: 26.1: the fan is 24 ghost grains staggered over one beat; the D pedal lifts. 27.4: a soft
  glass chord for the name. Chords: 26–27 F#m9 · 28 Bm9.

BARS 29-29: (1:07.2–1:09.6)
- SHOW: 29.1: the fan folds back into the board, and the board shrinks onto the left end of the move
  timeline (slots 1–9: X's slots 1, 3, 5, 7, 9 as cyan ticks, O's as amber). 29.2–29.4: X's slots 1,
  3 and 5 light one by one, and at slot 5 the label "第 3 个 X：第 5 步 · X'S 3RD MARK: MOVE 5" appears.
- CAPTION c10: 「一局最早也要到第 5 步才结束」 / "The earliest a game can end is move 5." (s03_ghosts at "8:3.5" = 29.4+; 1:09.3–1:12.3)
- SOUND: Three rising bells on X's slots, the third left ringing. Chords: 29 E9.

BARS 30-31: (1:09.6–1:14.4)
- SHOW: Above slots 5–9, one tiny real board per end move rises. Each trails its ghost endings as a
  dashed hairline fan, with its win line glowing in the winner's colour.
  - move 5, XXXOO.... (game A, X): 24 ghost endings
  - move 6, XX.OOOX.. (O): 6
  - move 7, XOXOXOX.. (X): 2
  - move 8, XXOOOOX.X (O): 1
  - move 9, XOXOXOOXX (X): no ghost moves
  - Their multipliers land one per beat: ×24 (30.1), ×6 (30.2), ×2 (30.3), ×1 (30.4), ×1 (31.1).
  - 31.2–31.4: the fans breathe (ALIVE).
- CAPTION c11: 「结束得越早，身后拖着的幽灵对局就越多」 / "The earlier a game ends, the more ghost games it drags along." (s03_ghosts at "10:1.5" = 31.2+; 1:12.9–1:16.5)
- SOUND: Five notes stepping down (fewer ghosts, simpler sound), each followed by its ghost grains:
  24, 6, 2, 1, none. Chords: 30 E9 · 31 F#m9.

BARS 32-32: (1:14.4–1:16.8)
- SHOW: The move-5 board glides to the centre and grows, while the other tiny boards and the timeline
  fade (32.1–32.3). 32.4: three hairline panel frames draw above it, left, centre and right.
- CAPTION: —
- SOUND: The cut's 1-bar riser into S04. Chords: 32 Asus4.

---

## S04 · Counting by hand 手算 — `scenes/s04_by_hand.py` · `ByHand`

Bars 33–40 (1:16.8–1:36.0) · Act II · HUD §2 · top-right readout "第 5 步 · MOVE 5" (from bar 36: the count)

BARS 33-35: (1:16.8–1:24.0)
- SHOW: Three panels count the games X wins on move 5, one panel per bar. X marks and lines are cyan,
  O marks amber. Picture only.
  - Panel 1 (bar 33): the 8 winning lines flash on a mini-board, one per eighth note (3 rows,
    3 columns, 2 diagonals) → "8 条获胜线 · 8 LINES" (34.1).
  - Panel 2 (bar 34): X's three marks on the top row take all 6 move orders (1-3-5, 1-5-3, 3-1-5,
    3-5-1, 5-1-3, 5-3-1), one per eighth note (34.1–34.3+) → "3 × 2 × 1 = 6 种顺序 · 6 ORDERS" (34.4).
  - Panel 3 (bar 35): O's first mark hops through the 6 other squares on six sixteenths from 35.1.
    O's second mark then steps through the 5 left on five eighths (35.2+, 35.3, 35.3+, 35.4, 35.4+),
    slow enough to read as 6 × 5 → "6 × 5 = 30 种放法 · 30 PLACES FOR O" (36.1).
- CAPTION: —
- SOUND: The pulse layer comes in. Panel 1 is 8 bells on eighths, rising. Panel 2 is 6
  bell-and-glass pairs. Panel 3 is 6 glass ticks on sixteenths, then 5 on eighths. Each total lands
  with a small chime. [mark: count n=8 every=0.3; count n=6 every=0.3; count n=6 every=0.15; count n=5
  every=0.3] Chords: 33–35 E9.

BARS 36-36: (1:24.0–1:26.4)
- SHOW: The odometer. The three panels tick together as one counter (panel 3 turns fastest, panel 2
  steps once every 30, panel 1 once every 180), while the centre board flickers through the actual
  games, accelerating into a blur. The centre counter rolls 0 → 1,440. Small, under it:
  "8 × 6 × 30 = 1,440".
- CAPTION: —
- SOUND: Three layered tick streams (a 32nd-note blur, a glass note every 30, a bell every 180),
  accelerating over the hit's riser. [mark: count n=1440] Chords: 36 F#m9.

BARS 37-37: (1:26.4–1:28.8)
- SHOW: 37.1: the counter lands on **1,440** (hero number, cyan halo: these are X's wins), and the
  panels dim. 37.2: under the formula, why nothing needs subtracting fades in small: "第 5 步之前，谁都凑
  不齐三个棋子 · NOBODY HAS 3 MARKS BEFORE MOVE 5". ALIVE: the halo breathes.
- CAPTION c12: 「X 在第 5 步赢下的对局：1,440 种」 / "Games that X wins on move 5: 1,440." (s04_by_hand at "4:0.5" = 37.1+; 1:26.7–1:29.7)
- SOUND: A hit (video.yaml, Vsus): the A chord answers, the tonic still held back. Chords: 37 Asus4.

BARS 38-38: (1:28.8–1:31.2)
- SHOW: 38.1–38.2: the 1,440 and the panels slide to the left third. 38.3: a silent annotation on the
  right third, small, for those who read it: move 6. Board XX.OOOX.. with O's middle row amber: "O
  连成一线：8 × 6 × (6 × 5 × 4) = 5,760 · O COMPLETES A LINE".
- CAPTION: —
- SOUND: 38.3: one glass note (O's count). Chords: 38 Bm9.

BARS 39-40: (1:31.2–1:36.0)
- SHOW: 39.1: a board XXXOO...., with X's top row cyan and O's would-be third mark dashed on square
  5, is stamped RED "X 已经赢了 · X ALREADY WON": "12 × 6 × 6 = 432". 39.2: "5,760 − 432 = 5,328".
  39.3: to the right, three placeholders "第 7 步 ? · MOVE 7 ?", "第 8 步 ? · MOVE 8 ?", "第 9 步 ? ·
  MOVE 9 ?". Hairline arrows start to cross between them and the boards. By bar 40 the arrows have
  knotted into one dense tangle in the centre that keeps tightening (ALIVE: the knot writhes).
- CAPTION c13: 「再往后，手算就成了一团乱麻」 / "After that, counting by hand becomes a tangled mess." (s04_by_hand at "6:3" = 39.4; 1:33.0–1:36.0)
- SOUND: 39.1: the RED stamp, a short reverse whoosh and a low thud. From 39.3 a dissonant cluster
  swells: all nine square notes at once, detuned, brightness rising. It cuts dead on 41.1. Chords:
  39–40 Bm9.

---

## S05 · Play every game 探索每一局 — `scenes/s05_search.py` · `EveryGame` ★1

Bars 41–61 (1:36.0–2:26.4) · Act III, opened by c14 · HUD §3

**HUD and plate.**
- Top right, a live readout "对局计数 · GAMES COUNTED 000,000". From bar 54 it also shows "调用次数 ·
  CALLS" and "撤销次数 · UNDOS".
- A small plate at the left edge, tagged "程序 · THE PROGRAM". It shows file lines 23–27, then "⋯",
  31, "⋯", 33, 34 of the long video's `assets/play_all_games.py`, with the comments removed so one
  picture serves both languages: `def explore(player):`, the winner check, the full-board check, the
  move, the recursive call and the undo. It is mono and grey, with the active line highlighted.

BARS 41-42: (1:36.0–1:40.8)
- SHOW: 41.1: the knot snaps (one flash frame). Its threads straighten and vanish, leaving a tiny
  empty root board at (−2.0, +0.3), the same place as in S02. 41.2–41.4: the plate fades in at the
  left edge with its tag. Bar 42: the light pen appears on the root and pulses on the beats. ALIVE:
  grain, the pen's pulse.
- CAPTION c14: 「要是让电脑把每一局都下一遍呢？」 / "What if a computer plays every game, one by one?" (s05_search at "0:0.5" = 41.1+; 1:36.3–1:39.9)
- SOUND: The cut: a hit (video.yaml, Vsus), then near silence. A low A drone and a soft pulse on every
  beat (the pen) leave the question open. Chords: 41–42 Asus4.

BARS 43-44: (1:40.8–1:45.6)
- SHOW: The camera is close on the first wedge (frame 0.35). The pen walks down the program's first
  game, one move per beat, drawing a hairline edge behind it: X0 (43.1), O1 (43.2), X2 (43.3), O3
  (43.4), X4 (44.1), O5 (44.2), X6 (44.3). An inset board beside the pen shows each position.
  - 44.3: X's 2-4-6 diagonal lights in the inset, and the leaf on ring 7 lights cyan.
  - 44.4: a dashed ghost stub tries to continue past the leaf and is cut off by a small stop bar (the
    stopping rule). The counter shows 1.
  - The plate highlights the move line (file line 31) and the recursive call (33), and at the leaf
    the winner check (24–25).
- CAPTION: —
- SOUND: Each move is its square's note (X bell, O glass): C#5 D5 E5 G#4 A4 B4 D4, a run down the
  tree over a low D pedal. The leaf is a bright bell ping and a tick; the stop bar is a muted pluck.
  Chords: 43–44 E9/D.

BARS 45-46: (1:45.6–1:50.4)
- SHOW:
  - 45.1: a RED eraser swipes X6 off the inset, and the pen steps back up to ring 6 (the edge it leaves
    stays, dimmed).
  - 45.2 X7, 45.3 O6, 45.4 X8 → X's 0-4-8 diagonal: leaf 2 lights cyan on ring 9 (counter 2).
  - 46.1 RED undo X8, 46.2 RED undo O6, 46.3 O8, 46.4 X6 → X's 2-4-6 diagonal: leaf 3 (counter 3).
  - The plate's undo line (34) flashes RED at every erase.
- CAPTION c15: 「先试走一步，往下探索，再撤销」 / "Try a move, explore what follows, then undo it." (s05_search at "5:0.5" = 46.1+; 1:48.3–1:51.8)
- SOUND: Undo is a short reverse whoosh on the beat; moves are square notes; leaves are bell pings.
  Chords: 45–46 Bm9/D.

BARS 47-48: (1:50.4–1:55.2)
- SHOW: Twice as fast, on eighth notes. Counter 6 at the end.
  - Undo X6, O8, X7 (47.1, 47.1+, 47.2). X8 → leaf 4: X wins on move 7 (47.2+).
  - Undo X8, O5 (47.3, 47.3+). O6, X5, O7, X8 → leaf 5: X wins on move 9 (47.4 … 48.1+).
  - Undo X8, O7 (48.2, 48.2+). O8, X7 → leaf 6: the board is full with no line, the first draw, a
    grey-white leaf (48.3+).
  - The plate highlights the full-board check (26–27) at the draw.
- CAPTION c16: 「有人赢了，或者棋盘满了，这一局就下完了」 / "Someone won, or the board is full: that game is finished." (s05_search at "7:3.5" = 48.4+; 1:54.9–1:58.7)
- SOUND: The same sounds on eighths; the D pedal lifts; the draw leaf is a soft wooden pluck. Chords:
  47–48 E9.

BARS 49-50: (1:55.2–2:00.0)
- SHOW: The walk accelerates through the rest of the first wedge (games 7 … 27,732): sixteenths, then
  faster than the eye.
  - The inset flickers; leaves light along the front in their colours; tiny RED sparks at the tips are
    the undos.
  - The camera starts to pull out (49.1 → 53.1, ease-in-out).
  - 50.3–50.4: on the plate, the recursive call (33) gets the tag "递归：explore 调用自己 · RECURSION:
    explore CALLS ITSELF". The undo line (34) gets "回溯：撤销，退回来再试 · BACKTRACKING: UNDO, STEP
    BACK, TRY AGAIN".
  - 51.1: the counter crosses the end of the first wedge exactly on the downbeat: 27,732.
- CAPTION: — (picture only: the plate tags name the two ideas)
- SOUND: The pulse goes to sixteenths. The leaf pings thicken into a texture of grains, in the
  proportions being lit: bells for X leaves, glass for O, wood for draws. The undos are a soft
  granular hiss. Brightness rises with the rate of leaves. [mark: particles] Chords: 49 Bm9 · 50
  F#m9.

BARS 51-53: (2:00.0–2:07.2)
- SHOW: Now the search is a sweep. The frontier is a faint radial arm turning clockwise at one
  first-move wedge (40°) per bar. Behind it the leaves light (rings 5, 7 and 9 cyan, rings 6 and 8
  amber, draws grey-white on ring 9), and the internal nodes remain as faint dust. The counter at the
  downbeats: 57,324 (52.1), 85,056 (53.1), 114,648 (54.1).
- CAPTION c17: 「按顺序走遍整棵树，一局也不漏」 / "In order, through the whole tree, without missing a game." (s05_search at "11:2.5" = 52.3+; 2:03.9–2:07.5)
- SOUND: One chord per wedge, changing as the arm crosses each wedge line on the downbeat. The grain
  texture continues and the brightness keeps rising. Chords: 51 E9 · 52 F#m9 · 53 Bm9.

BARS 54-58: (2:07.2–2:19.2)
- SHOW: No words for 12 s. Wedges 5–9, one per bar.
  - The counter at the downbeats: 140,520 (55.1), 170,112 (56.1), 197,844 (57.1), 227,436 (58.1).
  - The camera has pulled out to the whole galaxy (ring 9 fills the picture's height) and now drifts
    with a slow rotation.
  - The light builds into 255,168 leaves on five rings: the inner two sparse (1,440 and 5,328
    points), the outer ones dense.
  - Under the counter, "调用次数 · CALLS" and "撤销次数 · UNDOS" run live.
  - 58.4+: half a beat of darkness as the arm reaches 12 o'clock.
- CAPTION: —
- SOUND: One chord per wedge. A noise riser runs through bars 57–58, and the pulse doubles. 58.4+:
  everything drops out for half a beat (video.yaml cue; no boom of its own). [mark: riser at 57.1
  bars=2] Chords: 54 Asus4 · 55 Bm9 · 56 F#m9 · 57 E9 · 58 Asus4.

BARS 59-59: (2:19.2–2:21.6)
- SHOW: 59.1 LANDING: one flash frame; the galaxy flares once and settles.
  - The counter locks on **255,168**, on the right third, set exactly like the title: the same weight,
    the halo cool on the left and warm on the right.
  - The readouts settle on "调用次数 · CALLS 549,946" and "撤销次数 · UNDOS 549,945".
  - ALIVE: slow rotation, breathing glow.
- CAPTION c18: 「每一局只算一次：255,168」 / "Every game counted exactly once: 255,168." (s05_search at "18:0.5" = 59.1+; 2:19.5–2:22.9)
- SOUND: A big boom (video.yaml hit) and the first tonic since the opening (video.yaml resolve), wide
  and bright. Chords: 59 Dmaj9.

BARS 60-61: (2:21.6–2:26.4)
- SHOW: The galaxy turns slowly (camera drift, slight zoom-in towards the inner rings); the five rings
  read clearly. ALIVE.
- CAPTION: —
- SOUND: The pulse thins to quarter notes. Chords: 60 Dmaj9 · 61 Bm9.

---

## S06 · Delete one check 删掉“判断输赢” — `scenes/s06_turn.py` · `DeleteCheck` ★2 (the turn)

Bars 62–69 (2:26.4–2:45.6) · Act III · HUD §3 · readout "对局计数 · GAMES COUNTED" · the scene join at 62.1 is a
segue

BARS 62-62: (2:26.4–2:28.8)
- SHOW: 62.1: the plate glides to the centre-left and grows 1.6×, and the galaxy behind it dims to
  40 %. The winner check (file lines 24–25: `if winner(board) is not None:` / `return 1`) highlights,
  tagged "判断输赢 · WINNER CHECK". 62.2: a RED strike draws across both lines.
- CAPTION c19: 「删掉“判断输赢”，再跑一遍」 / "Delete the winner check, and run it again." (s06_turn at "0:1.5" = 62.2+; 2:27.3–2:30.7)
- SOUND: The strike is a reverse whoosh; the pad thins. Chords: 62 Bm9.

BARS 63-63: (2:28.8–2:31.2)
- SHOW: The program starts again: the galaxy's light drains towards the root over the bar, and the
  counter resets to 000,000 (63.4).
- CAPTION: —
- SOUND: A tape stop: the pads and pulse glide down an octave over the bar and stop (video.yaml cue).
  Chords: 63 Bm9.

BARS 64-64: (2:31.2–2:33.6)
- SHOW: Near-black. Only the struck winner check, faint, and the light pen sitting still on the empty
  root remain. The pen does not pulse. The grain moves.
- CAPTION: —
- SOUND: One bar of digital silence (video.yaml cue, no boom of its own). The pen's missing pulse is
  what you hear. Chords: 64 —.

BARS 65-66: (2:33.6–2:38.4)
- SHOW: 65.1 HIT: the search re-runs at full speed, one full turn of the arm over these two bars.
  - Every leaf on rings 5–8 no longer stops. Its light streams outwards as pale streaks and splits into
    its ghost continuations: (9 − k)! unglowing grey points on ring 9 inside its own wedge (24 for each
    move-5 game, then 6, 2 and 1).
  - The real move-9 leaves keep their colours and their glow.
  - The inner rings empty out, and ring 9 fills in completely, visibly brighter and smoother than the
    35 % band of S05 (the tone mapping's headroom).
  - The counter races. As it passes 255,168 (about 66.2+), that value flashes RED in the HUD and is
    overrun.
- CAPTION: —
- SOUND: The hit: a sub boom on bVI, outside the key (the wrong world; video.yaml hit, the only boom
  here). Then a swarm of ghost glass tones, dense, wide and detuned, rises with the counter over the
  next hit's riser. [mark: particles, sound "ghost"] Chords: 65–66 B♭maj7♯11.

BARS 67-67: (2:38.4–2:40.8)
- SHOW: 67.1: the counter lands on **362,880**. The whole ring changes to S02's neutral fill-order
  look (grey and colours alike) and repeats the 18.1 flare frame exactly: this is S02's tree of 9!
  orders. 67.2: S02's label "9 × 8 × … × 1 = 9! = 362,880 · 9 的阶乘" flies in from the left and docks
  beside the counter. ALIVE: the ring shimmers.
- CAPTION c20: 「362,880：幽灵对局全回来了」 / "362,880: the ghost games are back." (s06_turn at "5:2.5" = 67.3+; 2:39.9–2:43.2)
- SOUND: A hit (video.yaml, Vsus): S02's bloom chord returns as the flare repeats. Chords: 67 Asus4.

BARS 68-69: (2:40.8–2:45.6)
- SHOW: 68.1: the RED strike pulses once. 69.1: it erases, and the winner check is back. The ghost
  points stream back inwards along their streaks and fade (69.1–69.4), and the inner rings light
  again in their colours. At 70.1 the five-ring galaxy is restored.
- CAPTION: —
- SOUND: The ghost swarm plays in reverse and dies away. Chords: 68 E9 · 69 Asus4.

---

## S07 · 255,168, explained 255,168 是怎么来的 — `scenes/s07_ledger.py` · `Ledger` ★3

Bars 70–80 (2:45.6–3:12.0) · Act IV, opened by c21 · HUD §4 · readout "Σ 255,168" · the scene join at 70.1 is a
segue. One length scale for the whole scene: 1 unit = 30,240 (games or orders), so 9! = 12 units.

BARS 70-71: (2:45.6–2:50.4)
- SHOW: The galaxy, restored. Tiny ring labels appear at the 12 o'clock end of rings 5–9, one per
  beat (70.1 … 71.1): "第 5 步 · MOVE 5" … "第 9 步 · MOVE 9". 71.2–71.4: the rings ease slightly
  apart. ALIVE: slow rotation.
- CAPTION c21: 「255,168 种对局，怎么变成了 362,880？」 / "How do 255,168 games become 362,880?" (s07_ledger at "0:0.5" = 70.1+; 2:45.9–2:49.5)
- SOUND: Five soft notes for the labels, rising. Chords: 70–71 Asus4.

BARS 72-74: (2:50.4–2:57.6)
- SHOW: The rings become bars.
  - 72.1–72.3: the circle is cut at 12 o'clock and unrolls. Each ring straightens into a horizontal
    row 12 units long, stacked from move 5 (top) to move 9 (bottom), every point at its slot, so each
    row shows its ghost gaps.
  - 72.3–73.1: each row's points slide left and close the gaps, becoming a solid bar as long as its
    number of games: 1,440 (0.05 units, a short glowing stub), 5,328 (0.18), 47,952 (1.59), 72,576
    (2.40), 127,872 (4.23).
  - Labels land one per beat: 1,440 (73.1), 5,328 (73.2), 47,952 (73.3), 72,576 (73.4), and
    81,792 + 46,080 (74.1; the move-9 bar is cyan, then grey). Colours: moves 5, 7 and 9 cyan, moves
    6 and 8 amber.
  - 74.2–74.3: the five bars slide end to end into one line in the upper third, 8.44 units long.
  - 74.4: "Σ = 255,168" lands at its right end. ALIVE: the points shimmer inside the bars.
- CAPTION: —
- SOUND: One note per label: bell for X's bars, glass for O's, a wooden pluck for the draws. The bass
  climbs E – F# – G# on the bar lines (the tonic held back). [mark: count n=5 every=0.6] Chords: 72
  E9 · 73 F#m9 · 74 E9/G#.

BARS 75-76: (2:57.6–3:02.4)
- SHOW: The ghosts come back as multipliers, one per beat: "× 24" (75.1), "× 6" (75.2), "× 2" (75.3),
  "× 1" (75.4), "× 1" (76.1), each docking on its segment of the top line.
  - Each segment drops a copy to a second line below. The copy stretches by its factor as dashed grey
    ghost slots open between its points; the ×1 copies just drop.
  - The copies dock end to end, left to right, and their labels roll to 34,560, 31,968, 95,904,
    72,576, 127,872.
  - 76.2–76.4: hairlines draw from the ends of each top segment to the ends of its stretched partner:
    five fans, widest for move 5.
- CAPTION: —
- SOUND: Each multiplier is a flurry of N ghost grains (24, 6, 2, 1, 1). The A pedal returns, and
  S02's fifths stack rebuilds over it, one note per multiplier, under the hit's riser. The bass steps
  A (75.1) → B (76.1), then falls to D on 77.1. Chords: 75 Asus4 · 76 Bm9.

BARS 77-78: (3:02.4–3:07.2)
- SHOW: 77.1 HIT: the bottom line locks at exactly 12 units, "= 362,880", and "9! · 9 的阶乘" docks
  under it (the third time it appears). The double frame holds the whole film: 255,168 games on top,
  362,880 orders below, each segment joined to its ×(9 − k)! partner. Bar 78 (ALIVE): a light runs
  along the top line, down the hairlines and along the bottom line.
- CAPTION c22: 「乘上各自被算的次数，加起来又是 9 的阶乘」 / "Multiply each by how often it was counted, and add: nine factorial again." (s07_ledger at "7:0.5" = 77.1+; 3:02.7–3:06.7)
- SOUND: A boom (video.yaml hit) and the tonic (video.yaml resolve). The pedal falls from A to D, so
  S02's question chord finally resolves. Chords: 77–78 Dmaj9.

BARS 79-80: (3:07.2–3:12.0)
- SHOW: 79.1–79.2: the bottom line and its hairlines fade. 79.1–79.4: the top line's segments regroup
  by colour into three bars on the same scale: X's wins (cyan, 4.34 units: moves 5 and 7 and the
  move-9 X wins), O's wins (amber, 2.58), draws (grey-white, 1.52). Labels land on beats: "X 赢
  131,184 · X WINS" (80.1), "O 赢 77,904 · O WINS" (80.2), "平局 46,080 · DRAWS" (80.3). ALIVE:
  shimmer.
- CAPTION c23: 「先走的 X 赢了一半多一点的对局」 / "X, who goes first, wins just over half of all games." (s07_ledger at "10:0.5" = 80.1+; 3:09.9–3:13.4)
- SOUND: A bell, a glass tone and a wooden pluck for the three labels. Chords: 79 Bm9 · 80 E9.

---

## S08 · Perfect play, and chess 双方都不失误，还有国际象棋 — `scenes/s08_bigger.py` · `BiggerGames`

Bars 81–98 (3:12.0–3:55.2) · Act IV · HUD §5 (bars 81–89), §6 (bars 90–98) · the scene join at 81.1 is a segue

BARS 81-82: (3:12.0–3:16.8)
- SHOW: 81.1–81.2: the three result bars hold (ALIVE: shimmer). 81.3–82.1: they fly back into the
  galaxy (ease-in-out, 2 beats). This is the only return to the galaxy in Act IV. 82.1: the internal
  nodes (the dust on rings 1–8) brighten a little, and the root glows white: the tree, ready to be
  read from the bottom up.
- CAPTION c24: 「那先走的 X 只要不失误，就一定能赢吗？」 / "If X goes first and makes no mistakes, can X always win?" (s08_bigger at "1:0.5" = 82.1+; 3:14.7–3:18.1)
- SOUND: A soft granular sweep with the flight; 82.1: a single held bell. Chords: 81 F#m9 · 82 Bm9.

BARS 83-86: (3:16.8–3:26.4)
- SHOW: Picture only: the colours climb the tree, one ring per half bar.
  - The leaves keep their colours. Each internal node takes the best result among its children for
    the player to move: ring 8 (X to move) on 83.1, ring 7 (O) 83.3, ring 6 (X) 84.1, ring 5 (O)
    84.3, ring 4 (X) 85.1, ring 3 (O) 85.3, ring 2 (X) 86.1, ring 1 (O) 86.3.
  - A small label rides the wave front, alternating "轮到 X 时：挑对 X 最好的 · BEST FOR X" and "轮到 O
    时：挑对 O 最好的 · BEST FOR O".
  - The inner rings visibly drain of colour: ring 2 ends with 48 cyan and 24 grey, ring 1 with all 9
    grey.
- CAPTION: —
- SOUND: A descending arpeggio, one note per ring, bell on X's turns and glass on O's, each on a chord
  tone of a falling progression. The section cue's 1-bar riser runs under bar 86. Chords: 83 E9 · 84
  F#m9 · 85 Bm9 · 86 Asus4.

BARS 87-87: (3:26.4–3:28.8)
- SHOW: 87.1: the root turns GREY with a soft flare. ALIVE: the grey root breathes; slow rotation.
- CAPTION c25: 「可要是双方都不失误，结果总是平局」 / "But if neither side makes a mistake, it is always a draw." (s08_bigger at "6:0.5" = 87.1+; 3:26.7–3:30.3)
- SOUND: An open fifth D–A with no third (a draw: neither major nor minor) and the soft thump
  (video.yaml section cue, I5). Chords: 87 D5.

BARS 88-89: (3:28.8–3:33.6)
- SHOW: 88.1: game A's leaf (ring 5) is ringed, and its path lights back to the root. 88.3: an inset
  board opens beside the path's second step: game A after move 2.
  - X on 0 in cyan; O on 3 in RED, "O 的失误 · O'S MISTAKE".
  - The centre square glows grey, "只有下中心才能保住平局 · ONLY THE CENTRE KEEPS THE DRAW".
  - 89.1–89.3: the inset plays on faintly, X1 O4 X2, to X's top row (the game was lost from move 2).
  - 89.4: hold, ALIVE.
- CAPTION: —
- SOUND: 88.3: the RED tag is a minor-second rub that resolves. 89.1–89.3: the motif's last three notes
  (D5 A4 E5), faint. Chords: 88–89 Bm9.

BARS 90-92: (3:33.6–3:40.8)
- SHOW: 90.1: the camera pulls out, and the galaxy shrinks into one small glowing box (90.1–90.3).
  That box is the first box of a digit strip "2 5 5 1 6 8": 6 boxes, labelled "井字棋 · 6 位数 ·
  TIC-TAC-TOE · 6 DIGITS". 90.4: below it a second strip begins, a "1" and then zeros, one box per
  sixteenth note and then faster, 121 boxes in all. The camera pulls back along it (frame 1.0 → 2.6,
  the widening scale) as it runs on towards 93.1.
- CAPTION c26: 「那国际象棋，有多少种对局？」 / "And how many games of chess are there?" (s08_bigger at "9:0.5" = 90.1+; 3:33.9–3:37.1)
- SOUND: Every box is a tick, and the run accelerates into a buzz. The climax hit's 2-bar riser runs
  through 91–92. [mark: count n=121] Chords: 90 E9 · 91 Bm9 · 92 Asus4.

BARS 93-93: (3:40.8–3:43.2)
- SHOW: 93.1 HIT, the climax: the 121st box lands.
  - Above the strip: "国际象棋：至少 1 后面跟着 120 个零（香农，1950 年，估计） · CHESS: AT LEAST 1
    FOLLOWED BY 120 ZEROS (SHANNON 1950, ESTIMATE)".
  - At its end: "121 位数 · 121 DIGITS".
  - The tic-tac-toe strip, tiny at the far left, glows, tagged "全部下完 · ALL PLAYED OUT": the only
    one that has been played out.
  - ALIVE: slow drift.
- CAPTION c27: 「国际象棋估计至少有 10 的 120 次方种对局」 / "By Shannon's estimate, chess has at least 10¹²⁰ games." (s08_bigger at "12:0.5" = 93.1+; 3:41.1–3:44.9)
- SOUND: The biggest hit since the title. The key lifts a whole tone to E Lydian (video.yaml act and
  hit, size 0.95, second only to the title), the brightest and loudest moment (about −11 LUFS
  short-term). Chords: 93 Emaj9.

BARS 94-95: (3:43.2–3:48.0)
- SHOW: A third strip grows between the two, 81 boxes in a fast run (94.1–95.1), stopping two-thirds
  of the way along the chess strip. Its label: "可观测宇宙中的原子：大约 1 后面跟着 80 个零（估计） ·
  ATOMS IN THE OBSERVABLE UNIVERSE: ABOUT 1 FOLLOWED BY 80 ZEROS (ESTIMATE)", and at its end "81 位数 ·
  81 DIGITS". ALIVE: drift.
- CAPTION c28: 「整个可观测宇宙也只有约 10 的 80 次方个原子」 / "The whole observable universe has only about 10⁸⁰ atoms." (s08_bigger at "14:0.5" = 95.1+; 3:45.9–3:49.9)
- SOUND: The atoms' run is softer ticks; 95.1: a low bell. Chords: 94–95 Emaj9.

BARS 96-98: (3:48.0–3:55.2)
- SHOW: 96.1: under the strips, small: "每多一个格子，就大 10 倍 · EACH EXTRA BOX: 10 TIMES BIGGER" (so
  two-thirds of the length is not two-thirds of the number).
  - 96.1–97.4: picture only. The light pen comes back and starts the S05 sweep on the chess strip: a
    faint radial arm, its grain texture. It lights the first box, then the next, and stops after 6
    boxes, as many as the whole of tic-tac-toe fills (255,168 has 6 digits).
  - Bar 98: the pen pulses at box 6 while the 115 dark boxes ahead fade into the grain. The camera
    keeps drifting back.
- CAPTION: —
- SOUND: The pen's soft pulse returns, with S05's grain texture, thin. From bar 98 the filter slowly
  closes for the return. Chords: 96–97 F#9 · 98 Emaj9.

---

## S09 · One tree 同一棵树 — `scenes/s09_callback.py` · `SameTree`

Bars 99–106 (3:55.2–4:14.4) · coda · HUD: none

BARS 99-100: (3:55.2–4:00.0)
- SHOW: 99.1: the camera rushes back (ease-in-expo, streak blur) to the 6-box strip and through it
  into the galaxy (99.1–99.4). Bar 100: a zoom-through towards game A's leaf on ring 5 (10.12°). 100.4:
  the leaf blooms and opens into game A's empty grid (as 20.4 → 21.1). In the same beat the camera
  pulls back: the grid settles on the left third at the opening size, and the galaxy, scaled to 0.6,
  re-forms on the right (root at (+2.6, +0.3)).
- CAPTION: —
- SOUND: A reverse noise swell and a pitch glide down a whole tone into D (video.yaml section cue and
  act: back in D). The resolve's riser runs into 101.1. Chords: 99–100 Asus4.

BARS 101-102: (4:00.0–4:04.8)
- SHOW: The opening image: game A's board on the left third (same grid, same size, move numbers),
  the galaxy on the right. Game A replays one mark per beat (101.1–102.1). In sync, the light pen
  retraces its path in the galaxy from the root to its leaf, one segment per move. 102.2: the top-row
  win line sweeps, and the leaf flares cyan.
- CAPTION c29: 「255,168 种对局，每一局都是这棵树上的一条路」 / "255,168 games: each one is a path through this tree." (s09_callback at "3:1.5" = 102.2+; 4:03.3–4:06.9)
- SOUND: The motif, the same five square notes as in bars 2–3, now over the tonic (video.yaml
  resolve); then the win run. Chords: 101–102 Dmaj9.

BARS 103-103: (4:04.8–4:07.2)
- SHOW: All 255,168 paths shimmer once, a wave of light from the root outwards (103.1–103.4); the
  board's glow breathes.
- CAPTION: —
- SOUND: A soft upward sweep of grains (every game, once). Chords: 103 Dmaj9.

BARS 104-104: (4:07.2–4:09.6)
- SHOW: 104.1: the board and the galaxy dim to 30 %, and the title re-forms centred over them:
  **255,168**, the tracked "T I C - T A C - T O E" and "井字棋 · 不同的对局 · DIFFERENT GAMES" (the
  layout of bar 10). ALIVE: the halo breathes.
- CAPTION: —
- SOUND: A rolled tonic chord (video.yaml resolve) and the motif's last note, E5, on the bell.
  Chords: 104 Dmaj9.

BARS 105-106: (4:09.6–4:14.4)
- SHOW: 105.1: the end line fades in under the title (`video.yaml` end_card): "完整版、程序和练习：
  见视频简介 · FULL VERSION, PROGRAM AND EXERCISES: SEE THE DESCRIPTION". Bar 106: everything fades
  to black; the last frame (4:14.4) is black.
- CAPTION: —
- SOUND: The tail rings out and reaches silence at 254.4 s. [mark: end] Chords: 105–106 Dmaj9.

---

## Music build notes (today's composer)

`check_short.py`, run with `/opt/explainer-venv/bin/python`, plays the plan's scene list and the
`video.yaml` music block through the toolkit's `explainer.music`. No render is needed. It checks:
- The named chords at the cues, and E Lydian from 93.1 and D from 99.1.
- The tonic chord only where the plan has it (never on the title).
- Booms only at the nine hits, in the planned order of size (title > 93.1 > 59.1 > 65.1 > 77.1 >
  18.1, 41.1, 67.1 > 37.1).
- The soft thump only at the real scene cuts (21.1, 33.1, 41.1) and the two section cues (87.1,
  99.1). Nothing at the segues (12.1, 62.1, 70.1, 81.1).
- The breaths at 9.4+ and 58.4+, the tape stop in bar 63 and the silent bar 64, none of them with a
  boom of its own.
- Every bar's chord, as `music.chords` has it. This includes the slash basses: the D pedal under
  21–25 and 43–46, and the bass E–F#–G#–A–B → D in 72–77.

**State of the toolkit.** The composer reads `music.chords`, `music.joins` and hit `size` only in the
toolkit's current working tree, which another agent is building and has not committed. The committed
version (21ce3af) ignores all three. It would then plan its own 2-bar cycle (starting on degree IV,
G#m7♭5♭9, which this plan never uses), thump and rise into every join, and play every hit at one size.

The checker keeps these as "todo" lines, so a regression shows without failing the plan. After the
first full composition it also compares `build/music/*/score.json` bar by bar. The square notes come
from the scenes' sound tags (`"X@C#5"`), so they need nothing from `video.yaml`.

---

## Left out (they live in the long version, the description and `exercises.md`)

- The guess prompt and every ponder card (questions are captions followed by picture instead).
- The board code (the list of 9, `WIN_LINES`, `winner()`), and the explore() walkthrough line by line
  (the plate is only a figure here).
- The definition of "function" and the recursion caption (the plate tags name 递归 and 回溯).
- The 2 + 1 + 2 = 5 zoom, and the "delete the undo line" experiment (it prints 3).
- The corner / edge / centre first-move puzzle (teased in the description) and "more games is not a
  better move" (it only makes sense with that puzzle).
- How chess programs look a few moves ahead.
- The recap and challenge cards.

## Numbers on screen (all recomputed by `assets/check_short.py`)

| where | number | what it is |
|---|---|---|
| S01, S05, S09 | 255,168 | different games (ordered move lists) |
| S02, S06, S07 | 362,880 = 9! | orders that fill the board; running products 9, 72, 504, 3,024, 15,120, 60,480, 181,440, 362,880, 362,880 |
| S03 | 24 = 4 × 3 × 2 × 1 | ghost endings of game A (9! counts it 24 times) |
| S03, S07 | ×24 ×6 ×2 ×1 ×1 | (9 − k)! for games ending on moves 5–9 |
| S04 | 8 × 6 × 30 = 1,440 | X wins on move 5 |
| S04 | 5,760 − 432 = 5,328 (12 × 6 × 6 = 432) | O wins on move 6 |
| S07 | 1,440 · 5,328 · 47,952 · 72,576 · 81,792 + 46,080 → Σ 255,168 (8.44 units) | games by end move (move 9: X wins + draws) |
| S07 | 34,560 · 31,968 · 95,904 · 72,576 · 127,872 → 362,880 (12 units) | each × its ghost factor |
| S07 | X 131,184 · O 77,904 · draws 46,080 | by result (X: 51.4 %, "just over half") |
| S05 HUD | 27,732 · 57,324 · 85,056 · 114,648 · 140,520 · 170,112 · 197,844 · 227,436 · 255,168 | counter at the end of each first-move wedge |
| S05 HUD | 549,946 calls · 549,945 undos | explore() calls; every mark placed is erased |
| S08 | 48 cyan, 24 grey (ring 2); 9 grey (ring 1) | the minimax wave's inner rings |
| S08 | 6 · 121 · 81 boxes | digits of 255,168, of 10¹²⁰, of 10⁸⁰ (the pen stalls after 6) |
| S08 | ≥ 10¹²⁰ (Shannon 1950, estimate) · ≈ 10⁸⁰ (estimate) | chess games · atoms in the observable universe |
