# Checks behind E6 (Marco's branch)

Every MEASURED number in E6 and in the "Marco's branch" notes of E0 / E2 comes from these runs.
Source: `nadirbt/careonex-agents`, branch `feat/sonic_with_rag_updated` at `1591ed2` (Marco Ren,
2026-10-10). Everything runs offline on files Marco committed, with his own code and the PyMuPDF
version his `uv.lock` pins (1.28.2). Nothing touches AWS, so nothing here re-runs a live search.

| File | What it does | Result (2026-10-10) |
| --- | --- | --- |
| `marco_metrics.py` → `marco_metrics.json` | his scorer (`evaluation/chunking_retrieval_benchmark.py score`) on his graded A/B/C file; stats of his saved 40-question feedback run | A/B/C averages below; best NDCG per question: A 9 · C 7 · tie 6 · B alone 0 · no helpful passage anywhere 3. Feedback run: extra searches used 18/40, top 5 unchanged 23/40, median 430 → 514.5 ms, p90 514 → 1,009 ms, **0 of 788 passages graded** |
| `replay_planner.py` → `planner_replay.json` | today's `plan_feedback_queries` on the 40 saved first searches | extra search for 17/40: 16 rewrites of the caller's words (`question_rewrite_used`), 1 from a retrieved heading (`feedback_used`); none for 23 (`no_safe_expansion` 14, `unverified_provider_claim` 6, `already_supported` 3) |
| `marco_extract_check.py` → `extract_v5_report.json` | his extract (v5) + chunk (v4) on the 20 real source documents | 19 documents → 257 chunks; the Side-by-Side PDF **fails**: "page 1: program columns could not be verified"; VA HCBS page still 560 characters |
| `doas_pages.py` → `doas_pages.json` | the ruled tables PyMuPDF finds on each page of that PDF | pages 1-2: **9** columns (empty spacer columns after CHSP and after OAA), the reader needs 7; pages 3-4: 7 columns, but the header says "MSPs:" (no QMB/SLMB) and HAAAD/NJHAP sits on a second header row |
| `table_chunk_check.py` | his chunker (v4) on the Side-by-Side text as the E2 extractor wrote it | the "$1,090" chunk now starts with the header row `|Field|MLTSS/PACE|JACC|SRCP|AADSP|CHSP|OAA|`: **names JACC** (E2 open item 3 fixed at the chunking step) |

A/B/C chunking, 25 questions, top 5, grades marked provisional in his file:

| Chunker | Precision@5 | MRR@5 | NDCG@5 | Latency |
| --- | --- | --- | --- | --- |
| A legacy (v2, how the main library was built) | **0.520** | 0.686 | **0.598** | 418 ms |
| B section-safe (v4, the branch default) | 0.472 | 0.671 | 0.535 | 406 ms |
| C hierarchical (children ~950 chars, parents ≤ 2,400) | 0.504 | **0.733** | 0.576 | 408 ms |

NDCG averages leave out the 3 questions where no library returned a helpful passage (their ideal
score is 0). The "ideal order" in his NDCG is built from every passage any of the three libraries
returned for the question, not from the whole library.

Re-run:

```bash
git clone -b feat/sonic_with_rag_updated https://github.com/nadirbt/careonex-agents marco
python -m venv v && v/bin/pip install pymupdf==1.28.2 pymupdf4llm==1.28.2 markdownify==1.2.3 beautifulsoup4==4.15.0 lxml==6.1.3
python3 -I marco_metrics.py marco marco_metrics.json
v/bin/python -I replay_planner.py marco planner_replay.json
v/bin/python -I marco_extract_check.py marco/services <downloads from ../reproduce_pipeline.py> out
v/bin/python -I doas_pages.py <downloads>/nj_doas_programs_side_by_side_2026.pdf doas_pages.json
v/bin/python -I table_chunk_check.py marco/services <E2 extract output>/nj_doas_programs_side_by_side_2026.pdf.md
```
