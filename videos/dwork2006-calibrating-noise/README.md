# Calibrating Noise to Sensitivity — the paper that invented differential privacy

An explainer video of **Dwork, McSherry, Nissim & Smith, *Calibrating Noise to Sensitivity in
Private Data Analysis* (TCC 2006)** — the paper that introduced what is now called differential
privacy and won the 2017 Gödel Prize.

| file | what it is |
| --- | --- |
| `output/dwork2006-calibrating-noise.mp4` | the full video (1080p60, narrated, ~24 min) |
| `output/dwork2006-calibrating-noise_part1.mp4` / `_part2.mp4` | the same video in two parts (definition → Laplace mechanism; budget → separation → legacy) |
| `output/dwork2006-calibrating-noise.srt` | subtitles |
| `output/chapters.txt` | chapter timestamps (paste into a YouTube/Bilibili description) |
| `output/transcript.md` | full narration by chapter |
| `output/zh/dwork2006-calibrating-noise.mp4` | **中文版**: the Chinese version (Mandarin narration, Chinese on-screen text, bilingual subtitles burned in); see [`i18n/zh/README.md`](i18n/zh/README.md) |
| `output/zh/dwork2006-calibrating-noise_part1.mp4` / `_part2.mp4` | the Chinese version in two parts |
| `output/zh/dwork2006-calibrating-noise.zh.srt`, `.en.srt`, `.zh-en.srt` / `.ass` | its subtitle files (Chinese, English on the Chinese timing, bilingual) |
| `output/dwork2006-calibrating-noise.zh-en.mp4` | the English video with bilingual subtitles burned in (Chinese above, English below): the upload copy for Bilibili |
| `output/dwork2006-calibrating-noise.zh.srt`, `.zh-en.srt` / `.ass` | Chinese and bilingual subtitles for the English video |
| `i18n/zh/` | the Chinese translation (narration, on-screen text, glossary) and companions (exercises, playground, digest) |
| `exercises.md` | do these after watching: pen-and-paper problems + a 15-minute coding task |
| `playground.html` | open in a browser: set ε, switch Laplace/Gaussian/uniform noise, and play the attacker |
| `digest.md` | page-referenced notes on the paper, glossary, small errata in the paper |
| `script.md` | narration (SAY) and visual plan (SHOW) — the single source of truth for the video |
| `scenes/` | Manim source, one file per chapter |

## What you'll learn

Eight *pause and ponder* moments ask you to predict before the video reveals: rounding as a fix,
the ε of Warner's coin, a histogram's sensitivity, why not uniform noise, why ε ≳ 1/n, splitting a
budget, why an interactive analyst can't just ask everything, and whether the 2020 Census broke the
paper's impossibility result. Three test-yourself questions close the video.

1. **The differencing attack** — why exact aggregate counts are not private.
2. **Where the paper sits** — randomized response, failed anonymization, Dinur–Nissim
   reconstruction, SuLQ → this paper.
3. **The setup** — a trusted curator answers queries with f(x) + noise.
4. **Defining privacy** — ε-indistinguishability: one row changes any output's probability by at
   most e^ε.
5. **Why so strict** — statistical distance vs. ratios; the "publish a random row" counterexample; why a private mechanism must be random.
6. **Sensitivity** — counts, histograms (S = 2 for any number of bins), and a bad example.
7. **The Laplace mechanism** — the log-ratio picture, the one-line proof, why not Gaussian.
8. **The payoff** — noise independent of n: privacy for individuals, accuracy for populations; why ε ≳ 1/n (the hybrid argument).
9. **The privacy budget** — adaptive queries (Theorem 1) and big savings for histograms.
10. **Beyond counting** — covariance, min-cuts, sampling, general metric spaces.
11. **The separation** — one-shot releases can't answer most parity counts unless n is
    exponential in d.
12. **Legacy** — the name "differential privacy", (ε, δ), the exponential mechanism, composition,
    local DP, DP-SGD, the 2020 US Census.
13. **Recap and questions.**

## Rebuild

```bash
python -m explainer.build videos/dwork2006-calibrating-noise -q l   # fast draft
python -m explainer.build videos/dwork2006-calibrating-noise        # 1080p60
python -m explainer.build videos/dwork2006-calibrating-noise --lang zh   # the Chinese version (docs/LANGUAGES.md)
```

Narration: Kokoro (`af_heart`), generated locally. To re-voice with ElevenLabs set
`ELEVENLABS_API_KEY` and change `voice:` in `video.yaml`.

*The paper page shown in the video is reproduced for commentary and teaching; the paper is © its
authors and Springer (LNCS 3876).*
