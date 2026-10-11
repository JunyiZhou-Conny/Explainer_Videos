# CareOneX E6 · Measuring search: Marco's experiments

*Chunking, feedback search, merging and answer checks: what Marco changed, and what the evidence on
his branch does and does not show.* Part of the series [CareOneX, layer by layer](../careonex-series/SERIES.md).
About 10 minutes, no narrator: English on screen, bilingual subtitles (中文 above, English below) burned in.
Watch after E0 and E2.

**Watch:** `output/careonex-e6-measuring-search.zh-en.mp4` (subtitles burned in). The clean picture is
`output/careonex-e6-measuring-search.mp4`, with sidecar subtitles `.srt` (English), `.zh.srt`, `.zh-en.srt/.ass`.

**Source:** `nadirbt/careonex-agents`, branch `feat/sonic_with_rag_updated` at `1591ed2` (Marco Ren,
2026-10-10). Every MEASURED number comes from rerunning his own code on the files he committed, offline:
see [`../careonex-series/checks/marco/`](../careonex-series/checks/marco/README.md). Nothing touched AWS.
Knowledge Base IDs are shortened on screen on purpose.

| # | Chapter | What you should take away |
| --- | --- | --- |
| 1 | What is on Marco's branch | one commit, 213 files, mostly evaluation data; three dials around `retrieve` plus answer checking |
| 2 | Scoring a search | precision@5, MRR and NDCG on a toy example; no human grades, no score |
| 3 | Three ways to cut | chunkers A (legacy), B (section-safe, v4), C (hierarchical); three staging libraries; 375 hand grades |
| 4 | What the chunking test shows | A best on precision and NDCG, C on MRR, B never best alone; B is the new default |
| 5 | Feedback search | six steps; where an extra search comes from; model-free vs `intent`; reciprocal rank fusion; today's weights only reorder |
| 6 | The 40-question run | extra search for 18 of 40, top 5 unchanged for 23, slower tail; **0 of 788 passages graded** |
| 7 | Checking the spoken answer | `text_eval`: WER, word cosine, phrases, lookup checks; similarity is not correctness |
| 8 | Fixes, and what is still open | the DoAS table chain, voice safety, the open list |

## Found while making this video

1. **With today's merge weights, an extra search cannot add a new passage to the top 5.** In
   `retrieve()` the first search fetches 10 candidates and its reciprocal-rank points count 1.5×. A
   passage found only by the extra search scores at most 1/61 ≈ 0.016; the first search's 10th result
   scores 1.5/70 ≈ 0.021. Run with his own `reciprocal_rank_fusion`, the merged top 5 is always the first
   search's top 5 reordered, unless the first search returned fewer than 5 (`checks/marco/rrf_reach.py`).
   The code comment ("require a novel supplemental-only hit … before RRF can promote it") suggests new
   passages were meant to get in. (The saved 40-question run merged with equal weights, so it does not
   show this.)
2. **The feedback run is ungraded**: all 788 saved passages have `relevance: null`. It measures speed and
   how often the list changes, not whether results got better.
3. **Chunker B, the new default (`CHUNKER_VERSION` 4), is never best on its own** in his A/B/C grades
   (A 9, C 7, ties 6, none useful 3; averages in the checks README). Grades are marked provisional.
4. **The new DoAS table reader (extract v5) fails on the real 2026 PDF**: pages 1-2 have 9 ruled
   columns (two empty spacer columns) where it requires 7; on pages 3-4 the header says "MSPs:" without
   QMB/SLMB and HAAAD/NJHAP sits on a second header row. Because retrieve drops unverified chunks of that
   table, the table currently reaches the agent from nowhere but the team summary.
5. **The branch commits the AWS account number and the staging Knowledge Base IDs** to a public
   repository (README, `docs/EVALUATION.md`, evaluation files). Not a secret by itself, but the team's
   setup guide kept them out; worth a team decision.

Questions to test yourself:
1. Why can a search with a perfect MRR still have a low precision?
2. Why can today's extra search reorder the top 5 but not add to it?
3. Why is high word similarity not proof of a correct answer?

## Rebuild

```bash
python -m explainer.build videos/careonex-e6-measuring-search            # 1080p60 + output/<id>.zh-en.mp4
python -m explainer.build videos/careonex-e6-measuring-search -q l       # fast draft
```
