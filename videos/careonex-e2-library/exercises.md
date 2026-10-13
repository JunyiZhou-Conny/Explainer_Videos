# E2 · Answers

**1. Why does extract hash the text and not the downloaded file?** Because the downloaded bytes of a
web page change without the content changing. In our test 5 of the 11 web pages came back with
different bytes when downloaded twice a few seconds apart (an nj.gov bot-protection script, va.gov
nonces), while their extracted text was identical. A text hash changes only when what a reader sees
changes, so `extract.json` can list the documents whose rules may have moved.

**2. Why is the heading path stamped on every chunk?** A chunk is retrieved on its own. Without its
headings, "Countable income limit 2026: $4,855 per month" could belong to any program. With
"… > JACC (Jersey Assistance for Community Caregiving) 2026" on top, both the embedding and the agent
know which program the number belongs to. (The open item about the Side-by-Side table is exactly the
case where this protection does not reach: the program name lives in a table row, not in a heading.)

**3. One new PDF joins the source list: which containers do real work on the next run?** All five run;
only the new document costs anything. `data` finds the bucket and changes nothing. `ingest` downloads
everything again, but skips every source whose hash is already stored, and uploads the new PDF. (A web page whose bytes changed for
invisible reasons is uploaded and extracted again too, but its text hash is the same, so `chunk`
skips it: that is the point of hashing the text.)
`extract` skips every text whose raw hash and extractor version match, and converts the new PDF.
`chunk` skips every document whose text hash and chunker version match, and writes the new chunks.
`kb-sync` finds the existing index, knowledge base and data source, and starts an ingestion job, which
embeds the new chunks. (The catalog is baked into the data image, so the image must be rebuilt first;
`run` builds before it runs.)
