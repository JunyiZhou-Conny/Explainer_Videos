# 井字棋为什么恰好有 255,168 种对局？（4 分钟版） · Why are there exactly 255,168 games of tic-tac-toe? (the 4-minute version)

The condensed, music-led cut of [the tic-tac-toe video](../tictactoe-255168/). It has no narrator.
The picture carries the reasoning, 29 bilingual captions name the conclusions, and a score composed
in code from the picture's own event log is in the foreground: every cut, reveal and count is heard,
and each square of the board has its own note, so every game is also a melody. Picture and music
share one 100 BPM beat grid (a bar is 2.4 s): 106 bars, 4:14.

| file | what it is |
| --- | --- |
| `output/tictactoe-255168-short.mp4` | the Chinese-first master (Chinese caption above, English below), for Bilibili |
| `output/tictactoe-255168-short.en-first.mp4` | the English-first master, from the same picture |
| `output/tictactoe-255168-short.nomusic.mp4`, `.music.wav` | the picture without the score, and the score alone (written by the build, not committed: `python -m explainer.build videos/tictactoe-255168-short --no-render`) |
| `output/tictactoe-255168-short.zh.srt`, `.en.srt`, `.zh-en.srt` | the captions as subtitle files |
| `output/chapters.txt`, `transcript.md` | chapters (bilingual titles) and every caption by scene |
| `script.md` | the bar-by-bar plan: picture, caption and sound for every bar range, with the acceptance checklist |
| `captions.yaml`, `video.yaml` | the captions; the grid, look, music plan (chords, cues, levels) and scene list |
| `assets/check_short.py` | re-checks every number, board, caption, bar and music cue of the plan |
| `scenes/` | the scenes (`explainer.short.BeatScene`), one per section |

How a short is made, and how to make another: [docs/SHORTS.md](../../docs/SHORTS.md).

## Before publishing

- **Listen to it.** No person has heard the score yet. The reviews measured it (loudness of each hit,
  sync of every note to its picture event, no clicks) but could not judge how it sounds.
- **The two accent colours.** The plan uses two glowing families, X cool and O warm, as an
  exception to "one accent colour", because the game has two players. Every colour is set in
  `scenes/common.py` and `video.yaml`.
- The music is synthesized for this video by the toolkit (`explainer/music.py`): no samples or
  third-party recordings are used.
