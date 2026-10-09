# How these explainer videos are made: one human, one AI agent, and a lot of measuring

A behind-the-scenes explainer about this repository's own videos. It covers the privacy-paper
video, the tic-tac-toe video and their Chinese versions: who did what (one human, one AI agent and
its sub-agents), how an agent checks a video it cannot watch or hear, what went wrong, and what to
improve next. It is for curious viewers of the other videos. No Manim, programming or
machine-learning background is assumed.

| file | what it is |
| --- | --- |
| `output/how-these-videos-are-made.mp4` | the video (1080p60, narrated, 13:40) |
| `output/how-these-videos-are-made.srt` | subtitles |
| `output/chapters.txt` | chapter timestamps (paste into a YouTube/Bilibili description) |
| `output/transcript.md` | full narration by chapter |
| `script.md` | narration (SAY) and visual plan (SHOW), with its review log and the honesty rules |
| `ASSETS.md`, `assets/` | the real material on screen (frames, code, quotes, run records) and the source of every number |
| `scenes/` | Manim source, one file per chapter |

## What it covers

1. **Made by something that can't watch it.** An early draft's paused frame read "4 × 3 × 2 … 12".
   A simulated 12-year-old reviewer caught it.
2. **What the user asked for.** The vision (a video as a mentor, then something interactive), and the four
   requests.
3. **Who did what.** The human picked the topics, the audiences and the program; the agent did the
   rest. Where the time went, and what it cost.
4. **A script that is code.** SAY and SHOW lines, and "review before animating" (written down, then broken
   the same day).
5. **The audio is the clock.** The animation waits for the voice. Timing inside a sentence is
   estimated, which is why one scene carries 20 hand-set shifts.
6. **Checking without eyes or ears.** Contact sheets, frame grabs, a lint, self-checks on the numbers,
   and a speech recognizer.
7. **Reviewers who pretend.** A director and a simulated viewer, a reviewer across scenes, and skeptical
   verifiers.
8. **Same video, second language.** Translation aligned sentence by sentence, the Chinese voice test,
   and a subtitle bug that flipped a sentence's meaning.
9. **Bugs in the machinery.** Stale audio, stale renders, and a fixer that claimed a fix it hadn't made.
10. **What to improve next.** First what only people can do, then a licensed Chinese voice, timing by
    words, subtitles that understand sentences, and video and playground on one page.
11. **A recipe, and a request.** Six steps, the goal, and a request: if anything sounded wrong, say so,
    with the time.

## How it was kept honest

- The user is never named. Their words are quoted with only filler words removed (`assets/quotes.yaml`).
- The cost appears only on screen, always with its label: "API list-price equivalent for the whole
  session up to Oct 7 · all four requests, not the cost of one video".
- Every reconstruction is tagged on screen. Every number has a source in `ASSETS.md`.
- The narration passed a speech-recognizer round trip, with no misread words
  (`assets/en_asr_roundtrip.yaml`). No person has checked it by ear yet.

The lessons behind chapters 3 and 10 are written up for the next videos in
[docs/PLAYBOOK.md](../../docs/PLAYBOOK.md).
