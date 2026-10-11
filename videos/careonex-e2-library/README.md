# CareOneX E2 · Building the library

*From 20 public documents to 232 searchable passages.* Part of the series
[CareOneX, layer by layer](../careonex-series/SERIES.md). About 10 minutes, no narrator: English on
screen, bilingual subtitles (中文 above, English below) burned in.

**Watch:** `output/careonex-e2-library.zh-en.mp4` (subtitles burned in). The clean picture is
`output/careonex-e2-library.mp4`, with sidecar subtitles `.srt` (English), `.zh.srt`, `.zh-en.srt/.ass`.

**Source:** `nadirbt/careonex-agents`, branch `data-retrieval` at `d96a4ad` (the pipeline code is the
same on `feat/sonic_with_rag` at `eff4a96`). Every number was checked by running the team's own extract
and chunk code offline: see [`../careonex-series/checks/`](../careonex-series/checks/README.md).

| # | Chapter | What you should take away |
| --- | --- | --- |
| 1 | Two halves | the system has a batch half (build the library) and a live half (answer a caller) |
| 2 | The source list | `ragfile_list.csv` is the only input: 20 approved public documents |
| 3 | data and ingest → `raw/` | one versioned bucket, `ac215-*` naming as a security boundary, hash-or-skip, sidecars, manifests |
| 4 | extract → `text/` | why the text (not the file) is hashed; three versions of the HTML converter; PDF tables |
| 5 | chunk → `chunks/` | heading paths on every chunk, the table rule, 1,600 / 2,800 / 200, the 1 KB sidecar trap |
| 6 | kb-sync → vectors | Titan v2 embeddings, cosine similarity, S3 Vectors + Bedrock KB with chunking off, cost vs. latency |
| 7 | What is open | three problems found while making the video (below) |

## Found while making this video

1. **The VA "Home and Community Based Services" page loses its content in extract** (560 characters,
   2 chunks, mostly the site menu): its service list is a `<ul class="flex-menu">`, which the
   menu-stripping rule in `services/extract/careonex_extract/convert.py` removes.
2. **The JACC monthly service cap disagrees between two 2026 sources**: the JACC page says $1,156 per
   participant per month; the 2026 Side-by-Side table and the team's curated summary say $1,090.
   `prefer_latest` in retrieve cannot resolve a same-year conflict.
3. **The Side-by-Side table's chunk with "$1,090" never says "JACC"**: the program names are in the
   table's second row; when `chunk` splits a table it repeats only the first row (group titles).
   (The 2026-10-07 notes say the names were lost in extraction; they survive extraction.)

**Update, same evening (Marco's branch `feat/sonic_with_rag_updated@1591ed2`, see E6):** item 3 is fixed
at the chunking step (chunker v4 repeats the header row, so the "$1,090" chunk names JACC), but the new
DoAS table reader (extract v5) fails on the real PDF and retrieve now drops unverified chunks of that
table, so for now the table does not reach the agent. Items 1 and 2 are unchanged there. Chapter 7
has a short beat on this; the checks are in [`../careonex-series/checks/marco/`](../careonex-series/checks/marco/README.md).

Questions to test yourself (answers in [exercises.md](exercises.md)):
1. Why does extract hash the text and not the downloaded file?
2. Why is the heading path stamped on every chunk?
3. One new PDF joins the source list: which containers do real work on the next run?

## Rebuild

```bash
python -m explainer.build videos/careonex-e2-library            # 1080p60 + output/<id>.zh-en.mp4
python -m explainer.build videos/careonex-e2-library -q l       # fast draft
```
