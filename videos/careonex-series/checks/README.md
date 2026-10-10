# Checks behind the numbers in the CareOneX videos

Every number or claim in an episode that is not read straight off the code comes from one of these
runs. All of them use the team's own code (`nadirbt/careonex-agents`, `data-retrieval@d96a4ad`,
identical pipeline on `feat/sonic_with_rag@eff4a96`). They use the same library versions as the
team's `uv.lock` (pymupdf4llm 1.28.2, markdownify 1.2.3, beautifulsoup4 4.15.0, lxml 6.1.3) and run
offline: nothing touches AWS.

| File | What it does | Result (2026-10-10) |
| --- | --- | --- |
| `ragfile_list.csv` | the source list at that commit | 20 sources: 11 HTML, 8 PDF, 1 Markdown |
| `reproduce_pipeline.py` | fetch every source, run the team's `to_markdown` (extract) and `chunk_markdown` (chunk, 1600 / 2800 / 200) | **232 chunks**, the same count as the live index (232 vectors, `services/voice/NOTES-2026-10-07.md`) |
| `pipeline_report.json` | per document: bytes, Markdown characters, chunks | Program Guide 68 chunks, Medicare booklet 40, …; median chunk 854 characters, one chunk 3,074 (a single table row), one 181 |
| `html_hashes.py` | download every web page twice, seconds apart, with ingest's User-Agent | 5 of 11 pages change bytes between the two downloads (2 nj.gov, 3 va.gov); all 8 PDFs match the source list's hash |
| `text_hash_check.py` | extract both copies of those 5 pages | the extracted text is identical in all 5 |

Findings that became "open items" in E2:

1. **VA Home and Community Based Services page** → 560 characters of Markdown, mostly the VA site
   menu (2 chunks). The page's list of services is a `<ul class="flex-menu">`; `html_to_markdown`
   strips elements whose class contains "menu" when they are small and hold no `<article>`/`<h1>`.
2. **JACC monthly service cap disagrees**: the JACC page (byte-identical to the source list's hash,
   so this is exactly what was ingested) says "$1,156 per participant per month, plus care
   management"; the 2026 Side-by-Side PDF and the team's curated summary say "Up to $1,090/mo."
3. **The Side-by-Side table's program names** are in its second row (the first row holds group
   titles: "MEDICAID WAIVER PROGRAM … NON-MEDICAID WAIVER"). Extraction keeps them. The chunker
   splits the table (it exceeds 2,800 characters) and repeats only the first row, so the chunk with
   "Up to $1,090/mo." (chunk 5 of 12) never contains "JACC".

A first run used a browser User-Agent for one download and saw *every* web page change. That was
wrong: nj.gov's bot protection injects a script for some clients. The table above is from the rerun
with ingest's own User-Agent.

Re-run (any machine with internet):

```bash
python -m venv v && v/bin/pip install pymupdf4llm==1.28.2 markdownify==1.2.3 beautifulsoup4==4.15.0 lxml==6.1.3 requests
git clone -b data-retrieval https://github.com/nadirbt/careonex-agents
v/bin/python -I reproduce_pipeline.py careonex-agents/services downloads out
v/bin/python -I html_hashes.py careonex-agents/services/data/catalog/ragfile_list.csv twice
v/bin/python -I text_hash_check.py careonex-agents/services twice
```
