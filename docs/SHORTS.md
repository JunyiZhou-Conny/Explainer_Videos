# Shorts: condensed, music-led versions

A **short** is a 3:30–5:00 cut of a video with **no narrator**: the picture carries the reasoning,
bilingual captions (one Chinese line, one English line) name the conclusions, and a score composed
from the picture itself is in the foreground. Picture and music share one clock, a 100 BPM beat
grid (a beat is 0.6 s, a bar 2.4 s), so cuts land on bar lines and every object that appears gets
its own sound. The long, narrated videos are unchanged; they can get the same music, ducked under
the voice (see [Music for narrated videos](#music-for-narrated-videos)).

```
videos/<id>-short/
  video.yaml          format: short, tempo, captions, music, finish, scenes
  captions.yaml       every caption, Chinese and English, per scene
  scenes/*.py         BeatScene subclasses (explainer.short)
  output/             <id>.mp4 (+ <id>.en-first.mp4), <id>.nomusic.mp4, <id>.music.wav,
                      <id>.zh.srt / .en.srt / .zh-en.srt / .<layout>.ass, chapters.txt, transcript.md
```

## 1. The format (the rules the toolkit is built around)

- **Length** 3:30–5:00 (about 4:15). Every shot is a whole number of bars; a scene ends on a bar
  line (BeatScene pads its end with a moving hold).
- **Captions**: 25–30 lines, 400–550 Chinese characters in all; each line at most about 20 CJK
  characters and 14 English words, up for 3–4 s (captions are timed for reading, not snapped to the
  beat). At least 40 % of the runtime has no words: that is where the reasoning happens.
- **Structure**: a silent puzzle cold open, the title hit on a downbeat at bar 8–10, 3–4 acts each
  opened by a question or a date, one turn marked by sound (silence, a tape stop), a widening scale,
  a callback to the first image. No ponder cards, recap cards or chapter cards: a question caption
  is followed by 1–2 bars of picture; recap questions go in the description and `exercises.md`.
- **Pacing**: a visual idea every 6–7 s, a major change every 3–4 s, cuts and morphs on bar lines,
  arrivals on beats, counts on subdivisions (an eighth note, 0.3 s, for a few items; a sixteenth,
  0.15 s, for many). No frame is ever still: keep particles, a slow camera drift, a live counter or a
  breathing glow running during holds. Ease-out for arrivals, ease-in-expo for zoom-throughs; no
  elastic easing; never `Write` a whole sentence.
- **Cut whole beats, never half an explanation.** Each short has a must-get-right list (the facts
  it may not bend); review rounds check it.

## 2. Look

| | |
|---|---|
| background | `BG` `#050505` (pure black) |
| line art | hairlines: `hairline(m)` = 2 px `INK` `#C8CCCC`; `INK_DIM` `#7D8484` secondary; `faint_grid()` `#151515` |
| accent | **one family per video, with a meaning**: `ACCENTS["cool"]` (core `#DDFFFF` → mid `#A3EBEF` → glow `#5AA9B4` → halo `#1B3438`) or `ACCENTS["warm"]`. `RED` only means wrong / deleted / fails. A video that needs two players (X and O) may use both families |
| glow | `glow(m)` stacked strokes under an object, `glowing(m)` = glow + object, `halo(r)` a soft light sprite, `light_dot()` a photon / pen head, `PenWrite(m)` draws with a light dot on the tip |
| particles | `ParticleField(positions)`: thousands of points splatted per frame with a gaussian core and glow (20k points ≈ 20 ms a frame at 1080p). Simulations in closed form, so any time and rewinds are exact: `gas(n, box, start="left")`, `drift(n)`, `dissolve(points)`, `gather(points, T)`, `sample_points(mobject, n)`. `field.set_speed(-1)` rewinds |
| numbers | `RollingCounter(value, digits)`: an odometer whose digits roll; `.roll_to(v)`, `.land(v)` (scramble, then settle left to right) |
| type | Chinese: `cjk(s)` Noto Serif CJK SC (Song/Ming). Title: `title_card("井", "TIC-TAC-TOE", "255,168 GAMES")` (huge bold glyph, wide-tracked Montserrat, tiny mono). One heavy number a scene: `hero_number("255,168")` (Inter Black). Formula labels: `oldstyle("S = k log W")` (EB Garamond italic) or `MathTex(..., tex_template=style.OLDSTYLE_TEX)`. HUD: `tracked(s)` letter-spaced mono caps |
| HUD | `self.fig(3, "GHOST GAMES", "幽灵对局")` top left, `self.hud("TICK 007", corner=UR)`: drawn in screen space, so they stay put when the camera moves; drafting ornaments `brackets(m)`, `crosshair(p)` |
| layout | one hero object (centre or left third), or two equal panels, or object left + number right. The bottom 15 % is the captions' band, the top 8 % the HUD's |
| finishing | `finish:` in video.yaml: bloom on bright strokes, film grain, vignette (an ffmpeg pass at stitch time) |

Fonts are free OFL fonts installed by `setup/install.sh` (Ubuntu: `fonts-noto-cjk fonts-noto-core
fonts-noto-mono fonts-montserrat fonts-inter fonts-ebgaramond`; the licence files are in
`/usr/share/doc/<package>/copyright`). Their names are in `explainer/style.py` (`FONT_CJK_SERIF`,
`FONT_TRACKED`, `FONT_HEAVY`, `FONT_OLDSTYLE`, `FONT_MONO`); `style.font_available(name)` checks one.
Installing them changes nothing in the long videos (checked glyph by glyph and frame by frame).

## 3. Writing a scene

```python
from manim import *
from explainer.short import *          # BeatScene, palette, glow, particles, counters, type helpers

class ColdOpen(BeatScene):             # MovingCameraScene + beat grid + event log + captions
    def construct(self):
        self.fig(1, "HOW MANY GAMES", "多少局")              # HUD, fixed in the frame
        board = VGroup(*[hairline(Line([x, -1.5, 0], [x, 1.5, 0])) for x in (-0.5, 0.5)],
                       *[hairline(Line([-1.5, y, 0], [1.5, y, 0])) for y in (-0.5, 0.5)])
        self.play(LaggedStart(*map(Create, board), lag_ratio=0.25), bars=1)   # starts on the next bar

        self.caption("games")                                 # captions.yaml line, shown from now
        marks = VGroup(*[hairline(Circle(0.3), ACCENTS["warm"].mid).move_to(p)
                         for p in ([0, 0, 0], [-1, 1, 0], [1, -1, 0])])
        for m in marks:
            m.sound = "O"                                     # semantic sound: O is glass
        marks[2].sound = "O@C#5"                              # ... and this one is always C#5
        self.count(marks, every="eighth")                     # one mark (and its own note) per eighth note

        dust = self.add_field(ParticleField(drift(800), color=INK_DIM))   # keeps the hold alive
        n = RollingCounter(0, digits=6).to_edge(RIGHT)
        self.fix(n)                                           # a readout that ignores the camera
        self.play(n.roll_to(255168), self.zoom_to(board, width=6), bars=2,
                  rate_func=rate_functions.ease_in_out_cubic)

        self.mark("silence", dur=self.bar)                    # the turn: one bar of nothing ...
        self.wait_bars(1)
        self.mark("title")                                    # ... then the title hit
        self.play(FadeIn(glowing(title_glyph("井", 3.4, ACCENTS["cool"].core))), FadeOut(board, marks, n),
                  self.camera_home(), beats=2)
        self.wait_bars(2)                                     # the scene ends on a bar line anyway
```

**The grid** (video.yaml `tempo:`, default 100 BPM; a class can set `bpm = …`):

| call | what it does |
|---|---|
| `self.play(anim, beats=2)` | wait for the next beat, then play for exactly 2 beats |
| `self.play(anim, bars=1)` | wait for the next bar line, then play for 1 bar |
| `self.play(anim, run_time=0.9)` / `self.play(anim)` | start now (any length, whole frames) |
| `self.play(anim, beats=1, on="bar")` | start on the next bar, last one beat |
| `self.on_bar()`, `self.on_beat()`, `self.wait_to("eighth")` | wait to the next grid point (nothing if on one) |
| `self.wait_beats(n)`, `self.wait_bars(n)`, `self.wait()` (one beat) | holds; they keep updaters (particles, drifts) running |
| `self.until("12:2")` | wait until bar 12, beat 2 of this scene (bars and beats from 0) |
| `self.count(mobs, every="eighth" \| "sixteenth" \| 0.25)` | reveal one item per step (seconds, or a unit), logged as a count |
| `self.now`, `self.beat`, `self.bar`, `self.grid.label(self.now)` | where you are: `"3:2"` |

Units are note names, a beat being a quarter note: `"bar"` = `"whole"` (4 beats), `"half"` (2),
`"beat"` = `"quarter"`, `"eighth"` (0.3 s), `"sixteenth"` (0.15 s), `"triplet"`; or a number of beats.
Positions in scene code and captions.yaml are `"bar:beat"` counted from 0 (`"2:1.5"`), a bare number
is whole bars, `"7.2s"` seconds; a dotted `"10.1"` is refused (that is video.yaml's 1-based
`bar.beat`, see section 5).

Grid points are whole frames at 30 and 60 fps (a beat is 36 frames at 60 fps), so timings do not
drift across a scene or across the stitched video. At the 15 fps draft (`-q l`) beats and bars are
whole frames (9 and 36) but an eighth note is 4.5 frames and a sixteenth 2.25: `beats=0.5` plays
round to whole frames and drift until the next `beats=`/`bars=` play or `on_beat()` re-snaps, so
check fine timing at `-q m` or `-q h`. A play without `beats`/`bars` starts wherever the last one
ended, so follow off-grid moves with `self.on_beat()` or a `beats=` play.

**Captions** live in `captions.yaml` (see `explainer/captions.py` for the format):

```yaml
s01_cold_open:                         # scene file stem (or class name; or the class's captions_key)
  - id: games
    zh: 井字棋有多少种不同的对局？
    en: How many different games of tic-tac-toe are there?
  - zh: 终局一样，顺序不同，就是两局。
    en: Same final board, different order. Two different games.
    at: "6:0"                          # placed by the grid (bar 6 of the scene), no code needed
    beats: 6                           # optional length; default: reading time (about 5 CJK chars/s)
```

`self.caption("games")` shows a line now; `self.caption()` the next line not yet shown;
`self.caption(zh="…", en="…")` inline text. The text is read again from captions.yaml at stitch
time, so a wording fix needs no re-render (only a re-stitch: `--no-render`): the log records which
key the scene read (`captions_key`, else the file stem, else the class name) and the stitch reads
the same one; a line without an `id` is found again by its text, else by its place in the list. A
line the render placed that captions.yaml no longer has is reported (`WARNING … left out`), and an
inline line keeps the text it was rendered with.

**Marks and sounds**: the composer reads the event log (section 5), so tell it what a moment means.
`self.mark(kind, dur=…, **data)` binds to the play that starts at the same moment; `self.play(...,
kind="reveal", sound="glass")` is the same as a keyword. Kinds: `cut`, `section`, `hit`, `title`,
`resolve` (the tonic arrives), `riser`, `silence` (dur), `tape_stop` (dur), `count` (n, every or
times), `particles`, `motif` (name: a recurring figure), `end`. Per object, `mobject.sound = "X"`
names its sound; `music.sounds` (or a `music.palette` map) in video.yaml maps names to instruments
(`bell`, `glass`, `pluck`, `wood`, `glass_rev`: a glass note played backwards) or effects (`tick`,
`blip`, `whoosh_rev` for a RED erase, `shimmer`, `boom`); common other names work too
(`reversed_glass`, `reverse_whoosh`, `sub_boom`, `soft_pulse`, `marimba` …). A tag may fix the note:
`m.sound = "X@C#5"` (so each square of a board has its own pitch and a game is heard as a melody);
`"@C#5"` is the default instrument at that note.

In a `self.count(...)` each item sounds as its own tag says (instrument and note); items without a
tag use the count's `sound=`, then video.yaml's `count` entry (`music.sounds` or the palette map),
then the palette's count instrument (glass for the `glass` palette); unpitched notes climb through
the chord (`pitch="flat"`: they repeat one). More than 24 unpitched items become ticks. A `count:
tick` entry makes every untagged count tick. The palette's `cut` entry sets the sound of scene cuts.

**Camera**: `self.play(self.zoom_to(cup, width=1), beats=4, rate_func=rate_functions.ease_in_expo)`
(zoom-through), `self.zoom_to(scale=3)` (pull out), `self.camera_home()`, `self.drift((0.04, 0),
zoom=0.005)` / `self.stop_drift()` for a slow move during holds. Stroke widths scale with the zoom,
as with a real lens. Fixed mobjects (`self.fix`, `self.hud`, `self.fig`) are drawn last, on top.

**Checks**: `python -m explainer.preview videos/<id>/scenes/s01.py ColdOpen` (contact sheets, with
the captions burned in as the short will show them) and `python -m explainer.check …` (off-frame
and small text; the HUD is exempt, and a short may end with objects on screen; it prints the
scene's length in bars).

## 4. video.yaml and building

```yaml
id: tictactoe-255168-short
title: "255,168"
format: short
tempo: 100
captions: {layouts: [zh-first, en-first]}    # zh-first (Bilibili), en-first (YouTube), zh, en
music: {key: D, mode: lydian, mood: bright, palette: glass, sounds: {X: bell, O: glass}}
finish: {bloom: true, grain: true, vignette: true}
voice: none                                  # (a short has no narrator)
scenes:
  - {file: scenes/s01_cold_open.py, cls: ColdOpen, bars: [1, 11], title: "How many games?"}
  - {file: scenes/s02_fill.py,      cls: FillOrders, bars: [12, 20], title: "Nine factorial"}
```

`bars: [a, b]` (optional, counted from 1) is where the plan puts a scene; the stitch warns when a
render does not start at bar a or is not b − a + 1 bars long.

```bash
python -m explainer.build videos/<id> -q l           # draft (480p15): render, stitch, captions, music
python -m explainer.build videos/<id>                # final 1080p60
python -m explainer.build videos/<id> --no-render    # captions.yaml or music settings changed: re-stitch only
python -m explainer.build videos/<id> --layout en-first --no-finish --no-music
python -m explainer.music videos/<id> -q l --report  # just the score: build/music/<quality>/
```

The stitch joins the scenes (each a whole number of bars), runs the finishing pass once (cached in
`build/stitch_*/<id>.finished.mp4`), burns the captions into the picture for each layout (no band:
zh-first puts the Chinese baseline at 87 % of the height, glyphs about 39 px tall at 1080p, with the
English in letter-spaced mono capitals under it; en-first swaps them), composes and masters the
music, and writes `<id>.mp4` (first layout), `<id>.<layout>.mp4` (the others), `<id>.nomusic.mp4`
(the same picture, a silent track), `<id>.music.wav`, the `.zh.srt`, `.en.srt` and `.zh-en.srt`
sidecars, the `.ass` files, `chapters.txt` and a caption `transcript.md`. A short has music unless
video.yaml says `music: false` (or `--no-music`). The stitch prints, and writes to
`build/stitch_*/<id>.qa.json`:

| number | what it checks | aim |
|---|---|---|
| `picture_only` | share of the runtime with no caption | ≥ 40 % |
| `cuts_on_bars`, `cuts_rayleigh` | cuts on bar lines; how tightly they sit on the bar grid (R = 1: all on it) | all; R = 1 |
| `scenes_whole_bars`, `bar_plan` | every scene a whole number of bars; where video.yaml `bars:` planned it | all |
| `plays_on_beat`, `plays_on_16th`, `plays_rayleigh_beat` | play starts on the beat grid | most on beats |
| `sync.picture_delay_frames` | measured on the joined picture: frames from each logged play (that starts out of a still picture) to its first visible change; `early` counts changes before the play | ≥ 1 frame (the start frame shows alpha 0), about 0.1 s for a smooth fade; early 0 |
| `sync.audio_lag_ms`, `sync.frames_match` | measured on the shipped `<id>.mp4`: its sound against `music.wav` (cross-correlation), its frame count against the joined picture | 0 ms; true |
| `sync.motion_share` | share of seconds in which the picture moves | ≥ 75 % |
| `lufs`, `true_peak_dbtp`, `lr_correlation` | the master's loudness, peaks, mono safety | −14, ≤ −1, > 0 |
| `clicks`, `clicks_dry_accents` | discontinuities in the music (1 ms bursts above 7 kHz) away from any planned onset | 0 |
| `score_coverage` | share of visual events the composer gave a sound (a check of the composer, not of sync) | ≈ 100 % |
| `dropped_in_silences` | accents left out because a planned silence would have cut them to a blip | — |

Together the measured numbers make the sync end to end: picture events appear where the log says
(1 frame after the play starts: that frame still shows alpha 0), the score puts each sound at the
logged time, and the shipped file's sound sits exactly where the score put it.

`finish:` (or `look: {post: ...}`) values: `true`, a strength (`grain: 4`, `bloom: 0.5`, `vignette: 0.6`, the vignette
angle in radians), or a dict (`bloom: {strength: 0.55, threshold: 0.6, radius: 6, wide: 28}`: blur
sigmas in px at 1080p; `bloom: [6, 28]` gives the two sigmas; `vignette: "PI/5"` works too). The
pass costs about 3× real time at 1080p60; grain also makes files larger
(CRF 18 with grain is about 8 MB per 10 s at 1080p60; `--crf 20` about 5.5 MB). The pass writes a
high-quality intermediate (CRF 16; `finish: {crf: N}` changes it: at CRF 12 a 4-minute short with
grain passed 3 GB); every master is encoded from it at the master CRF, also when a layout has no
captions.

**Caption type** (zh-first, at 1080p): Chinese Noto Serif CJK SC glyphs 38 px tall, baseline at 87 %;
the English line in Noto Sans Mono capitals 22 px tall (the plan's size; the reference's 14 px is
too small on a phone), letter-spaced 5 px, baseline at 92.5 %. A line wider than 86 % of the frame
wraps at balanced word gaps (the Chinese line moves up). The longest English lines of the pilot
(c05, c17) are one line at 83–84 % of the width.

## 5. Music

`explainer/music.py` composes **one continuous score per video** from every scene's
`<Scene>.events.json` (written by every VoiceScene and BeatScene; see `explainer/events.py`) placed
on the stitched timeline, and synthesizes it in NumPy/SciPy: pads (three detuned voices, slow
LFOs), bass, FM bells, glass (struck-bar modes), plucks, ticks, sub booms (250 → 45 Hz with their
2nd harmonic, for phone speakers), noise risers and whooshes, a shimmer, a synthetic 2.8 s stereo
reverb. No samples and no third-party audio: nothing to license or attribute, nothing for content
matching to find (optional description line: “音乐：为本视频由代码生成 / Music generated in code for
this video”). The same logs and settings always give the same samples.

| in the picture (event log) | in the music |
|---|---|
| a cut between scenes, `cut`, `section` | a chord change on the downbeat, a soft sub thump, a 1-bar riser into it |
| `hit`, `title` | a boom and a shimmer, a 2-bar riser into it; on `title` the tonic and a rolled chord |
| a reveal (`Create`, `FadeIn`, `Write` …) | one note: bells for small marks (rising through the chord in a run), plucks for text, a rolled chord for big titles, an upward run for a long line, a shimmer for a light; panned to the object's x on screen |
| a count (`self.count`, `CounterLand`, `CounterRoll`) | one note or tick per item on the item's own time, rising; an odometer gets ticks that follow its speed |
| `silence` (dur) | digital silence, then a boom on the return |
| `tape_stop` (dur) | the music slows and falls to a stop, silent until the next hit or cut |
| `resolve` | the tonic arrives (it is withheld until then; a suspended dominant prepares it) |
| motion (number and size of moving things, camera moves, particles) | the pads' low-pass opens (brightness follows motion, loudness does not) |
| the beat grid (shorts) | chords change on bar lines (every 2 bars inside a phrase); a soft pulse of ticks and chord tones on the grid when the picture is busy, from the title on |

At most `density` (3) ordinary accents a second; counts and structure always sound. Structure that
is said twice sounds once: cues of one family (`cut`/`section`, `hit`/`title`, `silence`, …) less than
a beat apart are merged (the scene's time, video.yaml's chord / key / mode; title wins over hit), and
a silence whose return has a `hit` or `title` leaves the boom to it. An accent that would start in a
planned silence, or within 0.12 s before one, is left out (the drop-out would cut it to a 30 ms
blip); every synthesized sound ends with a short fade, so none stops with a click. Settings in
video.yaml `music:` — `key`, `mode` (lydian, ionian/major, mixolydian, dorian, aeolian/minor,
phrygian), `mood` (bright / warm / dark: filters, reverb, sparkle, bass and accent levels),
`palette` (glass / soft / pluck: which instrument plays which role; or a map of sound tags, as
`sounds`), `sounds`, `acts` (key changes), `cues`, `chords`, `joins`, `levels`, `density`, `pulse`,
`lufs` (-14), `peak` (or `true_peak_dbtp`, -1), `seed`. The tempo is video.yaml's `tempo` (or `grid: {bpm}`, or `music.bpm`).

Structure can also be written in video.yaml instead of scene code, on the whole video's timeline:

```yaml
music:
  cues:
    - {at: "10.1", kind: title, chord: vi}          # the number is given, not yet explained
    - {at: "63.1", kind: tape_stop, bars: 1}
    - {at: "64.1", kind: silence, bars: 1}           # the turn
    - {at: "65.1", kind: hit, chord: bVI}            # outside the key
    - {at: "93.1", kind: hit, key: E, size: 0.9}     # the climax lifts the key; size 0-1: how big a hit
  acts: [{at: s08_bigger, key: E, mode: lydian}]
  chords: {1: I, 4: II, 6: vi, 21: II/D, 64: rest, 65: bVI}   # optional: the progression, bar by bar
  joins: {"12.1": segue}                             # a scene join that continues the picture
```

`chords:` (optional) writes the harmony bar by bar instead of letting the composer plan it: each
entry is the chord from that bar (from 1, or a `"bar.beat"` position) on, a roman numeral in the key
that holds there (`acts` / cue `key:`), `"/D"` a bass note (`II/D`), `rest` no pads or bass; a cue's
own `chord:` fills in where the map has none. `joins:` marks scene joins that are not cuts (`segue`:
no thump, no riser, the chord carries on). `levels:` (optional) is a fader over the whole score, so a
cold open can start near silence and build into its title: `{"1.1": {bed: -16, accents: -9}, "2.1": -8,
"9.4+": 0}` gives dB at positions (a number: both stems; `bed` = pads, bass, risers; `accents` = the
event-locked notes and hits), linear in dB between them and held after the last; the loudness target
still applies to the whole score. A count mark's `gain` (`self.mark("count", ..., gain=0.6)`) makes one
phrase softer or louder without moving its notes.

Positions in video.yaml count as musicians do, from 1: `"10.1"` is bar 10, beat 1 (bar n starts at
(n − 1) × 2.4 s), `"12.3+"` the eighth note after bar 12 beat 3, a bare `12` bar 12; `"9:0"` is the
0-based notation of scenes and captions.yaml, `"123.4s"` seconds, a scene stem that scene's start.
`chord:` names the chord at a structure point: a scale degree (`vi`, `IV`, `Vsus`), an open fifth
(`I5`: neither major nor minor) or a borrowed root (`bVI`, `bVII`: a maj7♯11 chord there); `key:` /
`mode:` on a cue change the key from there. Only these fields are read: a chord or key written in a
`note:` is a comment to people (`{at: "93.1", kind: hit, key: E}`, `{at: "99.1", kind: section,
chord: Vsus, key: D}`). Without a name, the tonic is withheld until a `title` or
`resolve` and prepared by a suspended dominant. Outputs in `build/stitch_*/music/<id>/` (or
`build/music/<quality>/` from the CLI):
`score.json` (chords, notes, effects, silences), `cues.json`, `score.mid` (open it in any DAW),
`bed.wav` and `accents.wav` (the two stems), `music.wav`, `report.json`.

**Mastering**: a short's music is normalized to -14 LUFS integrated (BS.1770, gated) with true peaks
at or below -1 dBTP (a look-ahead limiter), and checked for L/R correlation > 0 (mono-safe on phone
speakers).

**Nobody involved in making it can hear it.** The numbers say the levels, peaks and sync are right;
only a person listening can say whether it sounds good. Listen before publishing, and say what is
wrong with the time.

### Music for narrated videos

`python -m explainer.build videos/<id> --music` (or a `music:` block in its video.yaml) adds the
score to a long video after the usual stitch, in free time (no grid): chords change on cuts and big
reveals at least 2 s apart, ponder cards become a ticking riser, ordinary accents thin out under
speech. The music is ducked under the narration: it starts down 150 ms before each stretch of speech
and is fully down 120 ms later (before the first syllable), stays down until 0.45 s after the speech
ends (so it does not pump between words), then comes back over 600 ms (the bed 12 dB, the accents
7 dB; deeper if needed so that it sits at least 15 LU under the speech, and 6 LU under the voice
between sentences: `music.duck: {depth, accents, gap, under}`). The voice stays as built (-16 LUFS)
and is mixed from the loudness-normalized narration before its AAC encode, so it is encoded only
once. Outputs: `<id>.mp4` with the mix, `<id>.nomusic.mp4` (the narration-only master, exactly as
before), `<id>.music.wav`; parts get the same, and the bilingual `<id>.<lang>-en.mp4`
is burned from the music version. Without `--music` or a `music:`
block nothing changes. The event logs come from the scene renders, so scenes rendered before the
logger existed need one re-render (`--only <scene>`); the picture and narration of a re-render are
identical. A translated version (`--lang zh`) has its own logs and so its own timing.

## 6. Making the pilot

Draft order, as in the style plan: the cold open and title (about 24 s, bars 0–10) at final look
and sound first, a listening round, then the rest. Reuse the long version's verified numbers,
component code and Chinese glossary; restyle with the short palette; time on the grid; write
captions.yaml; build at `-q l` while iterating, `-q h` for the final.
