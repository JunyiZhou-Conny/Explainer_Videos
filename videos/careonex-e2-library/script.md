# CareOneX E2 · Building the library — script & visual plan (v1)

Series: *CareOneX, layer by layer* (`videos/careonex-series/SERIES.md`). Pilot episode.

Audience: the CareOneX team (AC215), each of whom built one layer with an AI agent and wants to
understand the others. Knows Python and what an LLM is; may not know S3, embeddings or Bedrock.
Goal: after this episode a viewer can explain what each of the five pipeline containers does,
why it exists, what it writes where, and what is still open.

**No narrator.** `SAY:` lines are not spoken: they are the subtitles (English below, Chinese above,
burned in under the picture). Their on-screen time comes from a reading pace of ~2.2 words/s
(`video.yaml`: `voice: {backend: silent, speed: 0.85}`). So: short sentences, digits for numbers,
one idea per sentence. On-screen text stays short (labels, not sentences): the subtitles carry the
explanation.

Verified against: `nadirbt/careonex-agents` branch `data-retrieval` at `d96a4ad` (pipeline code is
the same on `feat/sonic_with_rag` at `eff4a96`). Numbers from re-running the team's own extract and
chunk code on all 20 sources (`videos/careonex-series/checks/`): 232 chunks, same as the live
index. Live facts (232 vectors, ACTIVE) from `services/voice/NOTES-2026-10-07.md`.

Conventions
- `SHOW:` what is on screen during the `SAY:` line after it.
- Semantic colours (the series kit): our containers = BLUE · stored data (S3 prefixes, files,
  chunks) = GREEN · AWS managed (Bedrock, Titan, S3 Vectors, KB) = ORANGE · caller = WHITE ·
  question / query = YELLOW · problems = RED.

---

## S01 · Two halves — `s01_map.py` · `TwoHalves`

SHOW: The system map builds up: top half "1 · build the library" (source list → data → ingest →
extract → chunk → kb-sync, the S3 prefixes, the Knowledge Base), bottom half "2 · answer a caller"
(caller → voice ↔ Nova 2 Sonic; voice → lookup_program_info → retrieve → Knowledge Base).
SAY: CareOneX has two halves. One half talks to a family on the phone. The other half runs long before any call: it builds the library that every answer comes from.

SHOW: The bottom half fades to 15 %; the top half is outlined. Title card: "E2 · Building the library".
SAY: This episode is about the library: five containers that turn 20 public documents into 232 searchable passages.

SHOW: Map out. A YELLOW question strip: "What is the JACC income limit for one person?" Under it a
GREEN passage (from the JACC page) with "$4,855 for an individual" highlighted, and a small tag
"JACC page · nj.gov · 2026".
SAY: Why build a library at all? When a caller asks about an income limit, the agent must answer from an official document. It is not allowed to answer from memory, because these numbers change every year.

SHOW: The passage shrinks to a dot labelled "1 of 232"; the top half of the map returns, and a dot
travels along the chain from the source list to the Knowledge Base.
SAY: So every answer starts as one of these passages. Let's follow a document through the five containers, one at a time.

---

## S02 · The source list — `s02_catalog.py` · `Catalog`

SHOW: A spreadsheet panel `ragfile_list.csv`, 20 rows (file names), header with the key columns.
SAY: Everything starts with one spreadsheet, the source list. It names 20 public documents that the team approved.

SHOW: The rows regroup into blocks by publisher: NJ Division of Aging Services 11 · Veterans
Affairs 3 · NJ Medicaid (DMAHS) 2 · Medicare 2 · NJ Disability Services 1 · CareOneX summary 1. Then
three chips: 11 web pages · 8 PDFs · 1 Markdown.
SAY: More than half come from New Jersey's Division of Aging Services. The rest come from Medicaid, Medicare, Veterans Affairs and Disability Services. 11 are web pages, 8 are PDFs, and 1 is a summary the team wrote from the state's 2026 documents.

SHOW: The JACC page row opens into a card: program "JACC", source_url, kind "html",
effective_date "2026-09-28", sha256 "c5befe69…".
SAY: Each row carries what an answer needs later: the program, the web address, the date the rules took effect, and a fingerprint of the file, called a hash.

SHOW: Card out. The spreadsheet slides into a BLUE container "data" (an image): caption
"add a document = add a row, rebuild the image".
SAY: The source list is the pipeline's only input. To add a document, you add a row and rebuild, because the list is built into the data container's image.

---

## S03 · data and ingest → raw/ — `s03_ingest.py` · `Ingest`

SHOW: The GREEN bucket frame `ac215-program-kb-<account-id>` with chips: versioned · encrypted ·
public documents only.
SAY: The first container, data, makes sure one S3 bucket exists. It is versioned and encrypted, and it holds public documents only. No caller information ever goes into it.

SHOW: Two name-spaces side by side: `ac215-*` (course) and `careonex-*` (production, RED). The team
permission set's S3 resource line `arn:aws:s3:::ac215-*`; its arrow to `careonex-*` is blocked.
SAY: Its name starts with ac215 on purpose. The team's S3 permissions only reach buckets whose names start with ac215, so nothing in this course can touch the company's production buckets, which are named careonex.

SHOW: ingest (BLUE): a row of the source list → download → sha256 → compare with the hash stored
on the object in S3. Two documents: the PACE flyer, hash equal → "unchanged · skip"; the JACC page
on a first run, nothing stored yet → "upload".
SAY: The second container, ingest, downloads every document and computes its hash. If the bucket already holds a file with that hash, it skips it. Otherwise it uploads the new version.

SHOW: The upload lands at `raw/nj_doas/nj_doas_jacc.html`, with a sidecar
`nj_doas_jacc.html.metadata.json` shown as JSON (program, year, jurisdiction, effective_date, …).
SAY: Next to every file it writes a small sidecar of metadata: the program, the year, the state, the effective date. Later, search can filter on these fields, for example only JACC.

SHOW: `snapshots/<date>-<hash>/manifest.json`: a list of object keys with version ids and
statuses (uploaded / unchanged).
SAY: Every run also writes a manifest: exactly which file versions it saw. That manifest is the version of the whole dataset.

---

## S04 · extract → text/ — `s04_extract.py` · `Extract`

SHOW: Two columns: "8 PDFs" and "11 web pages", each document downloaded twice, seconds apart,
with ingest's own settings. The 8 PDFs: GREEN ticks, "same bytes; same hash as the source list".
The web pages: 6 GREEN "same both times", 5 RED "different bytes the second time" (NJ Medicaid
MLTSS, JACC, the 3 VA pages).
SAY: Here is something we tested while making this video. We downloaded every document twice, a few seconds apart, the same way ingest does. All 8 PDFs came back identical, and still matched their hash in the source list. But 5 of the 11 web pages came back with different bytes the second time.

SHOW: The real differences: nj.gov — a bot-protection script tag appended to one copy
(`<script src="/_Incapsula_Resource?…&cb=314814079">`); va.gov — a random `nonce="…"` on dozens of
tags, different in each copy. Then for all 5 pages: "extracted text: identical" (GREEN).
SAY: The text on those pages had not changed. On nj.gov, a bot-protection script with a random number is sometimes added at the end. On va.gov, a fresh random code, called a nonce, is stamped on dozens of tags every time. So the hash of a downloaded file cannot tell you whether the rules changed.

SHOW: extract (BLUE): raw HTML → [keep the main region] → [strip scripts, navigation, footer,
forms] → Markdown; raw PDF → [pymupdf4llm] → Markdown with tables. Output `text/…/nj_doas_jacc.html.md`
with its text hash.
SAY: That is extract's job. It turns every file into clean text, written as Markdown. The hash of that text is the real signal that a document's content moved.

SHOW: A version timeline: v1 "trafilatura guesses the content" → RED "dropped nj.gov eligibility
paragraphs"; v2 "strip navigation first" → RED "nj.gov puts the page inside its navigation bar →
empty"; v3 "find the main region first, then strip" → GREEN.
SAY: Getting web pages right took three versions. Version 1 used a library that guesses the main content, and it silently dropped eligibility paragraphs. Version 2 deleted navigation first, but nj.gov wraps the whole page inside its navigation bar, so pages came out empty. Version 3 finds the main region first, and only then strips.

SHOW: A PDF table cell "Up to $1,090/mo." → Markdown table row `| Service Limitations | … | Up to $1,090/mo. | … |`.
SAY: PDFs go through a library called pymupdf4llm. It keeps headings, and it turns tables into Markdown tables, so a number stays in the same row as its label.

---

## S05 · chunk → chunks/ — `s05_chunk.py` · `Chunk`

SHOW: A tall strip "Program Guide · 22 pages · 51,856 characters" next to a short strip "one
passage · ~1,600 characters".
SAY: Search should not hand the agent a 22-page guide. It should return a passage short enough to read at once, and specific enough to answer one question. So the chunk container cuts every document into pieces called chunks.

SHOW: The team's summary (8,546 characters) with its headings; cuts appear at the headings → 12
chunks; each gets its heading path stamped on top, e.g. "…program limits for 2026 > JACC … 2026".
SAY: Rule one: a heading starts a new chunk, and every chunk carries its full path of headings. So the line "income limit 4,855 dollars" never travels without the word JACC.

SHOW: Three rule chips with small pictures: "a table stays whole (unless it alone exceeds the cap:
then split between rows, first row repeated)" · "aim for 1,600 characters, cap 2,800" · "merge
scraps under 200".
SAY: A table stays in one chunk. Only a table bigger than the cap is split, between rows, with its first row repeated on every piece. Long text is split at paragraph or sentence breaks, aiming for about 1,600 characters, with a cap of 2,800. Scraps under 200 characters are merged into a neighbour.

SHOW: A bar chart: chunks per document (20 bars, largest first): Program Guide 68, Medicare booklet
40, MLTSS guidance 19, …, VA community services 2. A counter: 232.
SAY: On all 20 documents this gives 232 chunks. The two longest PDFs, the program guide and the Medicare booklet, make up almost half of them. Most chunks are far below the target: the median is about 850 characters, because headings come often.

SHOW: The S3 layout: `chunks/nj_doas/nj_doas_jacc.html/0002-….md` + `.metadata.json`; a meter on
the sidecar reading "< 1 KB".
SAY: Each chunk is stored as its own file, with its own sidecar. That sidecar must stay under 1 kilobyte: Bedrock silently skips any chunk whose metadata is bigger, and still reports the job as complete.

---

## S06 · kb-sync → vectors — `s06_vectors.py` · `Vectors`

SHOW: One chunk (JACC eligibility) → ORANGE box "Titan Text Embeddings v2" → a column of numbers
`[0.021, -0.113, 0.067, …]` labelled "1,024 numbers".
SAY: The last container, kb-sync, turns every chunk into a vector. An embedding model, Amazon Titan Text Embeddings v2, reads the chunk and returns 1,024 numbers.

SHOW: A 2D picture of the space (caption: "1,024 directions, drawn in 2"): chunk dots in clusters
(JACC limits, Medicare home health, VA benefits); two arrows from the origin and the angle between
them, labelled "cosine similarity".
SAY: Think of those numbers as a direction in a space with 1,024 axes. Chunks with similar meaning point in similar directions, and the angle between two of them, measured by cosine similarity, is how search compares them.

SHOW: The stack builds: S3 Vectors bucket + index `program-kb` (1,024 dims · cosine · float32) ←
Bedrock Knowledge Base `ac215-program-kb` → data source `chunks/` with "chunking: NONE".
SAY: The vectors live in an S3 Vectors index called program-kb. On top sits a Bedrock Knowledge Base whose data source is the chunks folder. Its own chunking is switched off, because our chunk container has already done that job.

SHOW: An ingestion job bar fills to 232 / 232 → "COMPLETE". `config/knowledge-base.json` is written
(knowledge_base_id …) and an arrow points to a dimmed `retrieve` box: "next episode".
SAY: kb-sync starts an ingestion job and waits for it to finish. Then it writes the knowledge base's ID into the bucket, which is how the retrieve container finds it.

SHOW: Three bars for the monthly floor: S3 Vectors "cents" · Aurora pgvector "~$45" · OpenSearch
Serverless "~$175"; under them a latency note: "S3 Vectors: ~100–300 ms per query; OpenSearch: tens of ms".
SAY: Why S3 Vectors? It costs cents a month, while the alternatives start at about 45 or 175 dollars a month. The price is speed: about a tenth to a third of a second per search, and on a phone call every tenth of a second counts.

---

## S07 · What is solid, what is open — `s07_open.py` · `OpenItems`

SHOW: The five containers in a row, each over its own prefix (run reports go under snapshots/),
each with its "skip if" key: ingest — file hash · extract — file hash + extractor version · chunk —
text hash + chunker version · kb-sync — get-or-create.
SAY: Two habits run through the whole pipeline. Each container owns one folder of the bucket and leaves the others alone. And each one skips work that is already done, so running everything again is cheap and safe.

SHOW: Open item 1 (RED tag "found while making this video"): the VA "Home and Community Based
Services" page → its extracted text is mostly the VA site menu (560 characters, 2 chunks); the
page's list of services sits in an element named `flex-menu`, which the strip rule removes.
SAY: Now, what is open. Three things turned up while we made this video. First, one page, Veterans Affairs' Home and Community Based Services, comes out of extract as little more than the site menu. Its list of services sits in an element named flex-menu, and the rule that strips menus throws it away.

SHOW: Open item 2: the JACC monthly service cap: JACC web page "$1,156 per participant per month"
vs. 2026 Side-by-Side table and the team summary "up to $1,090/mo." — both 2026.
SAY: Second, two sources disagree. The JACC web page caps services at 1,156 dollars a month. The state's 2026 side-by-side table, and the team's summary built from it, say 1,090. Both are 2026, so "prefer the newest year" cannot settle it.

SHOW: Open item 3: that table's chunk with "$1,090" — its first row says only "MEDICAID WAIVER
PROGRAM … NON-MEDICAID WAIVER"; the row with the program names (MLTSS/PACE · JACC · SRCP …) stayed
in an earlier chunk. The word JACC appears nowhere in the chunk. Small note: "Caroline's notes:
names lost in extraction → they survive extraction (row 2); the split drops them".
SAY: Third, that same table hides its program names. They survive extraction, in the table's second row. But when the chunker splits a big table, it repeats only the first row. So the chunk that holds 1,090 dollars never says JACC.

SHOW: Also open (GREY): nothing re-runs the pipeline on a schedule; the team summary is updated by hand
each January and March.
SAY: Also open: nothing re-runs this pipeline on a schedule yet, and the team's summary is updated by hand.

SHOW: Ponder card with three questions.
SAY: Three questions to test yourself. Why does extract hash the text and not the downloaded file? Why is the heading path stamped on every chunk? And when one new PDF is added to the list, which containers do real work on the next run?

SHOW: Closing: the map, top half dimmed, the arrow retrieve → Knowledge Base lit YELLOW: "Next: E3 · Finding the right passage".
SAY: Next episode: what happens when a question arrives, and how retrieve finds the right 5 passages among these 232.
