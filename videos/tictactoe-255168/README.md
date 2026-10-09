# Why are there exactly 255,168 games of tic-tac-toe?

An explainer video for middle-school students (about 11–14). It asks one question with a
surprisingly exact answer, then answers it twice: by careful counting, and with a 20-line Python
program that plays every possible game. No algebra or programming background is assumed.

| file | what it is |
| --- | --- |
| `output/tictactoe-255168.mp4` | the full video (1080p60, narrated, 12:36) |
| `output/tictactoe-255168.srt` | subtitles |
| `output/chapters.txt` | chapter timestamps (paste into a YouTube/Bilibili description) |
| `output/transcript.md` | full narration by chapter |
| `output/zh/tictactoe-255168.mp4` | **中文版**: the Chinese version (Mandarin narration, Chinese on-screen text, bilingual subtitles burned in); see [`i18n/zh/README.md`](i18n/zh/README.md) |
| `output/zh/tictactoe-255168.zh.srt`, `.en.srt`, `.zh-en.srt` / `.ass` | its subtitle files (Chinese, English on the Chinese timing, bilingual) |
| `output/tictactoe-255168.zh-en.mp4` | the English video with bilingual subtitles burned in (Chinese above, English below): the upload copy for Bilibili |
| `output/tictactoe-255168.zh.srt`, `.zh-en.srt` / `.ass` | Chinese and bilingual subtitles for the English video |
| `i18n/zh/` | the Chinese translation (narration, on-screen text, glossary) and companions (exercises, playground, program) |
| `assets/play_all_games.py` | the program from the video: `python assets/play_all_games.py` prints `255168` |
| `exercises.md` | do these after watching: pencil-and-paper warm-ups and "change one line" coding challenges, with answers |
| `playground.html` | open in a browser: play moves on a board and watch how many games are still possible, split by X wins, O wins and draws |
| `assets/verify_counts.py` | checks every number in the video |
| `script.md` | narration (SAY) and visual plan (SHOW): the single source of truth for the video |
| `scenes/` | Manim source, one file per chapter |

## What you'll learn

Five *pause and ponder* moments ask you to guess or work something out before the video shows
the answer:

- How many games are there?
- How many games does X win on move 5?
- What happens without the undo line?
- What happens without the winner check?
- Which first move leads to the most games?

1. **How many games?** A game is the whole list of moves, in order.
2. **Filling the board: nine factorial.** Choices multiply: 9 × 8 × 7 × … × 1 = 362,880. That is
   too many.
3. **Games stop early.** "Ghost games" are made-up endings after a win. One game that ends on
   move 5 was counted 24 times. By hand: 8 × 6 × 30 = 1,440 games end on move 5.
4. **Counting by hand gets messy.** Move 6 is 5,760 − 432 = 5,328, and after that hand counting
   becomes a tangle, so we use plan B.
5. **Teaching a computer the rules.** The board as a list, the 8 winning lines, and the `winner`
   function.
6. **Exploring every game.** A recursive `explore`, a two-square worked example, the game tree,
   and undo (backtracking).
7. **Change one line.** Without undo the program prints 3. Without the winner check it prints
   362,880.
8. **255,168, explained.**
   - Games by the move they end on, and how they add back up to nine factorial.
   - Who wins: 131,184 X wins, 77,904 O wins, 46,080 draws.
   - The edge-start puzzle.
9. **Bigger games, and your turn.**
   - Perfect play is a draw (minimax).
   - Why chess can't be counted this way: at least 10¹²⁰ games (Shannon).
   - Recap and challenges.

## Rebuild

```bash
python -m explainer.build videos/tictactoe-255168 -q l   # fast draft
python -m explainer.build videos/tictactoe-255168        # 1080p60
python -m explainer.build videos/tictactoe-255168 --lang zh   # the Chinese version (docs/LANGUAGES.md)
```

Narration: Kokoro (`af_heart`), generated locally. To re-voice with ElevenLabs, set
`ELEVENLABS_API_KEY` and change `voice:` in `video.yaml`.
