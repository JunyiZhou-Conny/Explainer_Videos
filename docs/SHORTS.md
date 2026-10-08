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
        self.count(marks, every="eighth")                     # one mark (and one note) per eighth note

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
| `self.on_bar()`, `self.on_beat()`, `self.wait_to("half")` | wait to the next grid point (nothing if on one) |
| `self.wait_beats(n)`, `self.wait_bars(n)`, `self.wait()` (one beat) | holds; they keep updaters (particles, drifts) running |
| `self.until("12:2")` | wait until bar 12, beat 2 of this scene (bars and beats from 0) |
| `self.count(mobs, every="eighth" \| "quarter" \| 0.25)` | reveal one item per step, logged as a count |
| `self.now`, `self.beat`, `self.bar`, `self.grid.label(self.now)` | where you are: `"3:2"` |

Grid points are whole frames (a beat is 36 frames at 60 fps, 9 at 15 fps), so timings do not drift
across a scene or across the stitched video. A play without `beats`/`bars` starts wherever the last
one ended, so follow off-grid moves with `self.on_beat()` or a `beats=` play.

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
time, so a wording fix needs no re-render (only a re-stitch: `--no-render`).

**Marks and sounds**: the composer reads the event log (section 5), so tell it what a moment means.
`self.mark(kind, dur=…, **data)` binds to the play that starts at the same moment; `self.play(...,
kind="reveal", sound="glass")` is the same as a keyword. Kinds: `cut`, `section`, `hit`, `title`,
`resolve` (the tonic arrives), `riser`, `silence` (dur), `tape_stop` (dur), `count` (n, every or
times), `particles`, `motif` (name: a recurring figure), `end`. Per object, `mobject.sound = "X"`
names its sound; `music.sounds` in video.yaml maps names to instruments (`bell`, `glass`, `pluck`)
or effects (`tick`, `whoosh_rev` for a RED erase, `shimmer`, `boom`).

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
scenes:
  - {file: scenes/s01_cold_open.py, cls: ColdOpen, title: "How many games?"}
  - {file: scenes/s02_fill.py,      cls: FillOrders, title: "Nine factorial"}
```

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
sidecars, the `.ass` files, `chapters.txt` and a caption `transcript.md`. It prints, and writes to
`build/stitch_*/<id>.qa.json`, the share of the runtime with no caption (aim ≥ 40 %), how many cuts
are on bar lines, the music's loudness, true peak and stereo correlation, and the share of visual
events with a note or effect within 30 ms.

`finish:` values: `true`, a strength (`grain: 4`, `bloom: 0.5`, `vignette: 0.6`, the vignette
angle in radians), or a dict (`bloom: {strength: 0.55, threshold: 0.6, radius: 6, wide: 28}`: blur
sigmas in px at 1080p). The pass costs about 3× real time at 1080p60; grain also makes files larger
(CRF 18 with grain is about 8 MB per 10 s at 1080p60; `--crf 20` about 5.5 MB).

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

At most `density` (3) ordinary accents a second; counts and structure always sound. Settings in
video.yaml `music:` — `key`, `mode` (lydian, ionian/major, mixolydian, dorian, aeolian/minor,
phrygian), `mood` (bright / warm / dark: filters, reverb, sparkle), `palette` (glass / soft / pluck:
which instrument plays which role), `sounds`, `acts` (key changes: `[{at: s05_turn, key: A, mode:
major}]`, `at` a scene stem, `"123.4s"` or a bar number), `density`, `pulse`, `lufs` (-14), `peak`
(-1), `seed`. Outputs in `build/stitch_*/music/<id>/` (or `build/music/<quality>/` from the CLI):
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
speech. The music is ducked under the narration (150 ms look-ahead, 120 ms attack, 0.45 s hold,
600 ms release; the bed 12 dB, the accents 7 dB), sits 6 LU under the voice between sentences and
at least 15 LU under it while someone speaks (`music.duck: {depth, accents, gap, under}`); the voice
stays as built (-16 LUFS). Outputs: `<id>.mp4` with the mix, `<id>.nomusic.mp4` (the narration-only
master, exactly as before), `<id>.music.wav`; parts get the same. Without `--music` or a `music:`
block nothing changes. The event logs come from the scene renders, so scenes rendered before the
logger existed need one re-render (`--only <scene>`); the picture and narration of a re-render are
identical. A translated version (`--lang zh`) has its own logs and so its own timing.

## 6. Making the pilot

Draft order, as in the style plan: the cold open and title (about 24 s, bars 0–10) at final look
and sound first, a listening round, then the rest. Reuse the long version's verified numbers,
component code and Chinese glossary; restyle with the short palette; time on the grid; write
captions.yaml; build at `-q l` while iterating, `-q h` for the final.
