# CareOneX E2 · Building the library: from 20 public documents to 232 searchable passages

## 00:00 — Two halves
CareOneX has two halves. One half talks to a family on the phone. The other half runs long before any call: it builds the library that every answer comes from.
This episode is about the library: five containers that turn 20 public documents into 232 searchable passages.
Why build a library at all? When a caller asks about an income limit, the agent, the AI assistant on the phone, must answer from an official document. It is not allowed to answer from memory, because these numbers change every year.
So every answer starts as one of these passages. Let's follow a document through the five containers, one at a time.

## 00:52 — The source list
Everything starts with one spreadsheet, the source list. It names 20 public documents that the team approved.
More than half come from New Jersey's Division of Aging Services. The rest come from Medicaid, Medicare, Veterans Affairs and Disability Services. 11 are web pages, 8 are PDFs, and 1 is a summary the team wrote from the state's 2026 documents.
Each row carries what an answer needs later: the program, the web address, the date the rules took effect, and a fingerprint of the file, called a hash.
The source list is the pipeline's only input. To add a document, you add a row and rebuild, because the list is built into the data container's image.

## 01:46 — data and ingest → raw/
S3 is Amazon's file storage. A bucket is one top-level folder in it, and each file inside is called an object. The first container, data, makes sure the team's bucket exists. It keeps old versions of every file, it is encrypted, and it holds public documents only. No caller information ever goes into it.
Its name starts with ac215 on purpose. The team's S3 permissions only reach buckets whose names start with ac215, so nothing in this course can touch the company's production buckets, which are named careonex.
The second container, ingest, downloads every document and computes its hash. If the bucket already holds a file with that hash, it skips it. Otherwise it uploads the new version.
Next to every file it writes a small sidecar of metadata: the program, the year, the state, the effective date. Later, search can filter on these fields, for example only JACC.
Every run also writes a manifest: exactly which file versions it saw. That manifest is the version of the whole dataset.

## 03:06 — extract → text/
Here is something we tested while making this video. We downloaded every document twice, a few seconds apart, the same way ingest does. All 8 PDFs came back identical, and still matched their hash in the source list. But 5 of the 11 web pages came back with different bytes the second time.
The text on those pages had not changed. On nj.gov, a bot-protection script with a random number is sometimes added at the end. On va.gov, a fresh random code, called a nonce, is stamped on dozens of tags every time. So the hash of a downloaded file cannot tell you whether the rules changed.
That is extract's job. It turns every file into clean text, written as Markdown: plain text with a few symbols for structure, like a # before a heading. The hash of that text is the real signal that a document's content moved.
Getting web pages right took three versions. Version 1 used a library that guesses the main content, and it silently dropped eligibility paragraphs. Version 2 deleted navigation first, but nj.gov wraps the whole page inside its navigation bar, so pages came out empty. Version 3 finds the main region first, and only then strips.
PDFs go through a library called pymupdf4llm. It keeps headings, and it turns tables into Markdown tables, so a number stays in the same row as its label.

## 04:54 — chunk → chunks/
Search should not hand the agent a 22-page guide. It should return a passage short enough to read at once, and specific enough to answer one question. So the chunk container cuts every document into pieces called chunks.
Rule one: a heading starts a new chunk, and every chunk carries its full path of headings. So the line "income limit 4,855 dollars" never travels without the word JACC.
A table stays in one chunk. Only a table bigger than the cap is split, between rows, with its first row repeated on every piece. Long text is split at paragraph or sentence breaks, aiming for about 1,600 characters, with a cap of 2,800. Scraps under 200 characters are merged into a neighbour.
On all 20 documents this gives 232 chunks. The two longest PDFs, the program guide and the Medicare booklet, make up almost half of them. Most chunks are far below the target: the median is about 850 characters, because headings come often.
Each chunk is stored as its own file, with its own sidecar. That sidecar must stay under 1 kilobyte: Bedrock silently skips any chunk whose metadata is bigger, and still reports the job as complete.

## 06:27 — kb-sync → vectors
The last container, kb-sync, turns every chunk into a vector. An embedding model, Amazon Titan Text Embeddings v2, reads the chunk and returns 1,024 numbers. Titan runs on Bedrock, Amazon's service for using AI models without running them yourself.
Think of those numbers as a direction in a space with 1,024 axes. Chunks with similar meaning point in similar directions, and the angle between two of them, measured by cosine similarity, is how search compares them.
The vectors live in an S3 Vectors index, a store built for searching vectors, called program-kb. On top sits a Bedrock Knowledge Base whose data source is the chunks folder. Its own chunking is switched off, because our chunk container has already done that job.
kb-sync starts an ingestion job and waits for it to finish. Then it writes the knowledge base's ID into the bucket, which is how the retrieve container finds it.
Why S3 Vectors? It costs cents a month, while the alternatives start at about 45 or 175 dollars a month. The price is speed: about a tenth to a third of a second per search, and on a phone call every tenth of a second counts.

## 07:58 — What is solid, what is open
Two habits run through the whole pipeline. Each container owns one folder of the bucket and leaves the others alone. And each one skips work that is already done, so running everything again is cheap and safe.
Now, what is open. Three things turned up while we made this video. First, one page, Veterans Affairs' Home and Community Based Services, comes out of extract as little more than the site menu. Its list of services sits in an element named flex-menu, and the rule that strips menus throws it away.
Second, two sources disagree. The JACC web page caps services at 1,156 dollars a month. The state's 2026 side-by-side table, and the team's summary built from it, say 1,090. Both are 2026, so "prefer the newest year" cannot settle it.
Third, that same table hides its program names. They survive extraction, in the table's second row. But when the chunker splits a big table, it repeats only the first row. So the chunk that holds 1,090 dollars never says JACC.
An update from the same evening: Marco's branch works on open item 3. Its new chunker repeats the row with the program names, and we checked that the 1,090 dollar chunk now says JACC. But his new table reader fails on the real PDF, and retrieve now drops the table's unverified chunks, so for now the table does not reach the agent at all. Open items 1 and 2 are unchanged there. Episode 6 has the details.
Also open: nothing re-runs this pipeline on a schedule yet, and the team's summary is updated by hand.
Three questions to test yourself. Why does extract hash the text and not the downloaded file? Why is the heading path stamped on every chunk? And when one new PDF is added to the list, which containers do real work on the next run?
Next episode: what happens when a question arrives, and how retrieve finds the right 5 passages among these 232.
