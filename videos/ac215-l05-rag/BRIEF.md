# Brief · AC215 L5 — Introduction to RAG (follow-along: llm-rag)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture: decks A and B) and
`assets/` (real captures, see `ASSETS.md`). **Where the digest and the captures disagree, the
captures win.** They are newer (2026-10-16, 00:52–00:57 UTC; the pinned commit `e17a39f` is still
the head of `main`) and were made on the machine the video shows:

| topic | digest | captures (use these) |
| --- | --- | --- |
| the CLI container's name | `llm-rag-cli` (`container_name`, `docker-compose.yml:9`) | `llm-rag-llm-rag-cli-run-90678535ddef`: `docker compose run` does not use `container_name` (Compose v5.6.0; `laptop/07:37-38`, `08`) |
| first `sh docker-shell.sh` | "builds the image, a few minutes"; no pull | Chroma is pulled (12.1 s) and created **first**; then `Image llm-rag-cli Pulling` / `failed to resolve reference "docker.io/library/llm-rag-cli:latest": … not found` (Compose asks Docker Hub first; harmless), then `Building 81.5s` (`[2/6]` apt + pip + uv 20.2 s, `[5/6] RUN uv sync --frozen` 6.7 s, export 53.9 s), build context **112.26 MB** (`laptop/07:2-10`, `21-27`) |
| the banner | `Architecture: aarch64`, Python 3.12.x, uv x.y.z | `x86_64` (Apple Silicon prints `aarch64`), `Python 3.12.15`, `uv 0.13.1` (`laptop/07:39-44`); the prompt `app@92c5bfd26089:/app$` |
| what the image holds | no `.dockerignore`: `outputs/`, `docker-volumes/` on a *re*build (G15) | already on the **first** build: `/app/.git` is 103 MB (the history keeps the staff's 90.9 MB database, `laptop/05b`) and `/app/docker-volumes/chromadb/chroma.sqlite3` is baked in, because Chroma created it before the build (`14b`); image 2.11 GB (`14`) |
| Chroma's version | `latest` = 1.5.9 | Docker Hub: `latest` = `1.5.9`, digest `sha256:1e0b73a1…`; `chroma --version` → `1.4.4`; `/api/v2/version` → `"1.0.0"`; client library 1.1.0 (`laptop/11`, `11b`; `cli-container/03`). It works |
| chunk counts | 8,248 / 14,228; Tolminc 24 / 35 (the digest author's own script) | confirmed by the CLI itself (`cli-container/10`, `11`, `13`, `14`); the books come in file-system order (`The Complete Book of Cheese` first), not alphabetically |
| the overlap | `…ac` / `s she…` (measured) | confirmed: `'anized list of things she intended to ac'` / `'s she intended to accomplish during her '` (`12`); recursive chunk 1 **starts again** at `## Chapter One…` (`15`) |
| `--embed` without a key | `DefaultCredentialsError` (G2) | at the first call, not before: `embed()`, the first book's table, then `cli.py, line 98` → `File /secrets/llm-service-account.json was not found.`; no `embeddings-*` file written (`20`, `22`). Chunking ran without a key |
| the embeddings | not run; size estimates | the staff's own `gemini-embedding-001` files, committed in `68e0bde` (2026-10-07) and removed in `58dd602`, still in every clone's history: 22 files, 82 MB; their 22 chunk files are byte-identical to ours, so their vectors are what `--embed` makes for these chunks (`recorded-embeddings/00`, ASSETS) |
| `--load` | `Inserted 500 items...` … `Finished inserting N items` | without embeddings: `did not exist. Creating new.`, then `Number of files to process: 0`, exit 0 (`cli-container/30`, `31`); with the staff's: **8,248** and **14,228** items (`recorded-embeddings/01`, `02`) |
| on disk | `chroma.sqlite3` + UUID folders | right after start: a 188 KB `chroma.sqlite3` owned by **root** (`laptop/13`); after both loads: 59.8 MB + **two** UUID index folders, 82 MB (`recorded-embeddings/04`); an empty collection has `"dimension":null` (`laptop/17b`), a loaded one `256` (`recorded-embeddings/03`) |
| the vectors | 256 numbers; "need not be unit length" | 256 each; first five `[0.0139, 0.0075, 0.0099, -0.0664, -0.0192]`; lengths **0.369 to 0.402** (`recorded-embeddings/06`) |
| `--query` without a key | not discussed | prints `load()` (E3), then fails embedding the question (`cli.py:319` → `:79`) **before** it touches Chroma (`cli-container/40`) |
| the query's filters | 64 "Italian" chunks, 0 about Tolminc (the digest author's count) | confirmed by Chroma: 8,248 → 1,355 (`where book`) → 64 (`$contains "Italian"`) → 0 with "Tolminc"; 3 chunks in the whole collection contain "Tolminc" (`recorded-embeddings/08`). With a stand-in query vector (a stored Tolminc chunk's): unfiltered top 10 all Tolminc at 0.0000–0.1627, filtered top 10 all *The Complete Book of Cheese* at 0.2833–0.3123 (`09`) |
| the Woman's Institute book | no author or year (E8) | confirmed: `{'book': 'Womans Institute Library of Cookery'}` (`recorded-embeddings/07:22`) |
| `--get` (not in the README) | 10 records, no distances | confirmed: ids `1021665fac86c5a5-0` … `-9`, documents = the Project Gutenberg header and licence, no `distances` (`recorded-embeddings/05`); `[]` on an empty collection (`cli-container/42`) |
| after `exit` | Chroma keeps running (G8) | confirmed (`laptop/20`); `docker compose down` from your own terminal first prints two `WARN … variable is not set. Defaulting to a blank string.` lines: harmless (`21`) |
| restart | "query works without reloading" (not run) | `[+] run 2/2`, no pull, no build; both collections back with dimension 256; `--get` returns the same 10 records (`laptop/22`, `23`, `24`; `cli-container/70`) |
| G5 (Compose without the script) | `File  was not found.` at import (from reading the source) | confirmed, even for `--chunk`, after the two WARN lines (`gotchas/01:1-4`, `:16`, `:55`) |
| G1 (a clone not named `llm-rag`) | the entrypoint is missing; an empty folder is mounted | confirmed: `/bin/bash: docker-entrypoint.sh: No such file or directory`, exit 127; a root-owned, empty `../llm-rag` appears (`gotchas/04`, `05`) |
| semantic split | ~528 API calls in the chunk phase (estimate) | confirmed that the chunk phase calls the embedding API: the traceback runs `cli.py:212` → `semantic_splitter.py:275` → `:229` → `:206` → `cli.py:98` (`cli-container/60`); the call count is not measured |

## Audience and goal

An AC215 student who has done L1–L4: VMs and uv; a given Dockerfile and Docker Hub; the
mega-pipeline with a service-account key, `docker-shell.sh` and the `../secrets` mount; port_toy's
container networks, name lookup, published ports and Compose. They know Python and basic ML and
have used an LLM, but have never built a retrieval system or used a vector database. They watch
with their clone of [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag) open in
`~/AC215/llm-rag` (beside `~/AC215/secrets`), pausing to type each command.

After the video they can:
- say what RAG is (retrieve, then generate; the model is unchanged) and why the lecture rejects
  pasting every book into the prompt and fine-tuning for this job; draw the two lanes that share one
  embedding model and one database, and put each `cli.py` flag in its lane;
- set up the folders (`llm-rag/` and `secrets/` side by side, the clone named exactly `llm-rag`),
  create the service account with the Vertex role, place and name the key, enable the Vertex AI
  API (the README forgets this), and set `GCP_PROJECT` to their Project ID;
- start the two-container app with `sh docker-shell.sh`, read `docker-compose.yml` as a picture
  (network by name, a published port for the laptop, three bind mounts for code, key and data), and
  recognise the harmless first-run "not found", the run-container's real name, and the two ways the
  start goes wrong (Compose without the script; a clone with another name);
- run both chunkers, predict the char-split count from size and overlap, see the mid-word cut, and
  explain recursive-split's hidden 200-character overlap;
- explain an embedding as a direction, cosine similarity and Chroma's cosine *distance* (smaller is
  closer), the 256 numbers, why query and chunks must use the same model, and why the vectors'
  length doesn't matter for cosine;
- load a collection and say what a record holds, why `load` always rebuilds, what an index is for,
  and where the database lives on their disk (and that it survives `exit` and `docker compose down`);
- read a query: top-k with `where` and `where_document` filters that act **before** ranking, and
  predict why the README's query returns Italian cheeses rather than Tolminc;
- explain the chat prompt (question + 10 chunks), that the system instruction is defined but never
  sent, and the one-line fix;
- explain semantic chunking (sentence windows, distances, the 95th-percentile cut) and why it
  needs the API already at `--chunk`; name the lecture's other levers (query rewriting, hybrid
  search with RRF, re-ranking, Self-RAG) and which of them the tutorial does not implement;
- tear down: `exit`, `docker compose down`, what stays on disk, key hygiene, and why an index goes
  stale when the books change.

## Length and parts

~31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,240** (part 1 ~2,410, part 2 ~1,830). The cut follows the lecture's own phases (B5):
- **Part 1 = S01–S09, build the index** (Indexing: chunk → embed → load): what RAG is, the key and
  the project, the two containers, both chunkers, embeddings, the load into Chroma (~13.9 min of
  narration, ~17.5 min with typing, outputs and three ponders). It ends on a loaded database and
  "in part 2, we ask it questions".
- **Part 2 = S10–S16, ask the index** (Retrieval, Augmentation & Generation): the index survives a
  restart, nearest neighbours, filters, the chat prompt, semantic chunking, what the lecture adds,
  teardown and recap (~10.5 min of narration, ~13.5 min with outputs and two ponders). It opens with
  a fresh `sh docker-shell.sh`, as a student coming back another day would.
Word budgets per scene are targets (±15 %).

## The lecture behind the tutorial (SLIDES.md)

Two decks by the instructor, cited by PDF page: **A** = "Lecture 5: Introduction to RAG" (A1–A64),
**B** = the supplement "Advanced RAG" (B1–B89). S01 says once what the GREY `lecture_ref` tag means
("Lecture 5 · slides A16–A19"; a B number is the supplement). Deck A walks the naïve-RAG pipeline
box by box; the video walks the same pipeline command by command, so the scenes reuse its master
map (A16, B5), its terms (knowledge base, chunking, embedding model, vector database, query,
context, prompt, top-K) and its worked examples (the personality game A40–A43, the rank-and-cut
A48–A53, the final prompt A57–A59, the semantic-chunking walk B21–B33, RRF B46–B48, re-ranking
B51–B65). Deck B's other levers have **no code in the tutorial**: S15 teaches them as concepts only,
under a "concept · not in the tutorial's code" tag.

SLIDES.md has no scene map yet; the per-scene slide ranges in the scene plan are this brief's map,
for the mapping pass to check. Where the slides and the captures disagree, the captures decide what
the scene shows, and the narration says so kindly in one sentence:

| # | slides | tutorial / captures | scene |
| --- | --- | --- | --- |
| 1 | similarity *scores*, higher is better (A48–A53) | Chroma returns cosine *distance* = 1 − similarity, smaller is closer: 0.0000 for a chunk's own vector (`recorded-embeddings/09`) | S11 |
| 2 | metadata filtering is post-processing, after ranking (A54–A55) | Chroma's `where` / `where_document` act **before** ranking; top-k is chosen among the survivors (`08`, `09`) | S12 |
| 3 | the final prompt has a system prompt (A58–A59) | `SYSTEM_INSTRUCTION` is defined (`cli.py:40-58`) but never sent (`:394-396`, digest E1) | S13 |
| 4 | semantic chunking: an anchor walks the sentences, join while similarity ≥ 0.8 (B21–B33) | every sentence gets a ±1 window, consecutive windows' cosine distances, cut above the **95th percentile** (`semantic_splitter.py:91-96`, `:134-141`, `:239-243`) | S14 |
| 5 | "Indexing" means three things (A32–A38 search structure; B5 the offline phase; B13 better chunking) | the README calls the offline phase "Chunk -> Embed -> Load" (`README.md:5`) | S02, S09 (say which sense) |

The slides never show code, Docker, ChromaDB, Gemini, overlap or recursive splitting: those come
from the digest and the captures. Slips on the slides are not copied (SLIDES.md "Terms": A62's
title, "Euclidian", B59 vs B60, …). Never show a slide image or a meme; redraw the idea.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: `~/AC215`, the `llm-rag/` and `secrets/` folders, `outputs/` and `docker-volumes/chromadb/` as folders on your disk; the browser (Chrome, the course's web tools); the published host door `:8000` | GREY |
| Google Cloud: your project, IAM and the service account, the Vertex AI API; the two models, drawn as one tall **embedding model** box shared by both lanes (`gemini-embedding-001`) and an **LLM** box (`gemini-3.1-flash-lite`); the LLM's answer; Docker Hub | BLUE |
| containers and images: the CLI container (`llm-rag-cli` image) and the Chroma container (`chromadb/chroma:latest`), the vector-database cylinder inside it, the `llm-rag-network` rail, container-side ports | TEAL |
| system parts inside the image: the Debian base, the apt layer, the image's Python 3.12.15 | ORANGE |
| project-owned data and recipe: the books' pages once cut, chunk cards, document vectors, records, the two collections; the recipe files (`Dockerfile`, `pyproject.toml`, `uv.lock`, `docker-compose.yml`) and `/.venv` | GREEN |
| tools: docker, Compose, git, uv, `docker-shell.sh`; the three chunkers as tools — a ruler (`CharacterTextSplitter`), scissors (`RecursiveCharacterTextSplitter`), a seismograph (`SemanticChunker`) | PURPLE |
| errors and "avoid this": `DefaultCredentialsError`, exit 127, the first-run "not found" (drawn RED, then greyed "harmless"), the unplugged system-instruction cable, Project Gutenberg licence chunks (junk in the index), stale chunks | RED |
| your turn, the README tracker, "look here now", the top-K cut line, the semantic threshold line | YELLOW |
| money: every call to Vertex AI (embedding batches, the chat call), the key glyph (whoever holds it spends your project's money) | GOLD |
| lookups and routes: the question and its query vector, similarity arcs and the search beam, filter masks' edges, the name lookup `llm-rag-chromadb → 172.19.0.2`, the three bind-mount routes, the `8000:8000` arrow, `GOOGLE_APPLICATION_CREDENTIALS` as a signpost | PINK |
| a future thing (L06 agents, L08 fine-tuning) and the lecture's concepts with no code here (S15) | GREY, dashed |

Chunk cards and document vectors are GREEN whatever book they come from; a book is shown by a
label or a position, never by a colour. A filter dims what it removes to GREY at low opacity. The
system instruction is a GREY dashed ghost card. The key is always a GOLD key glyph; its content is
never drawn.

## Running example

- The laptop: user `student`, host `laptop`, workspace `~/AC215` (as captured, ASSETS):
  `student@laptop:~/AC215$`, then `student@laptop:~/AC215/llm-rag$`. Say once (S03): on a Mac (zsh,
  `%`) or in Windows the prompt looks different; on Windows run `sh docker-shell.sh` from WSL or Git
  Bash (G22, study guide). The G1 demo uses a second workspace, `student@laptop:~/AC215-zip$`.
- The CLI container: `app@92c5bfd26089:/app$` (first session, `laptop/07`), `app@390fe47a277a:/app$`
  (after the restart, `laptop/23`), `app@2af936bbf5b9:/app$` (the G5 demo). Say once (S04) that the
  part after `app@` is the container id and changes every run.
- Project: `GCP_PROJECT="your-project-id"`, the captures' placeholder (`laptop/06`, `cli-container/01`);
  narration: "type your own Project ID — the ID, not the name". Never a real-looking project id.
- The question: `"How is tolminc cheese made?"` (`cli.py:318`, `README.md:184`); chat's copy has two
  question marks (`cli.py:372`).
- The knowledge base: 11 books (`Number of files to process: 11`): ten Project Gutenberg books and
  the instructor's short story `Tolminc Cheese.txt` (7,808 characters; line 4 says *A fictional tale
  inspired by Alpine cheesemaking*). Narration: "the instructor's short story", never a name.
  *The Complete Book of Cheese* is named by its title, never by its author.
- Ids: `1021665fac86c5a5-0` = the first 16 hex digits of the SHA-256 of `The Complete Book of Cheese`
  + `-` + the row (`cli.py:127-130`); the stand-in query chunk is `8440accaceb0ce96-6` (Tolminc).
- Builds: show `[+] Building 81.5s`, the `[2/6]`, `[5/6]`, `[6/6]` steps and `Image llm-rag-cli Built`;
  cut the `=> =>` sub-lines (except `transferring context: 112.26MB`, line 21, for S04's beat), the `[internal]` lines and `[1/6] FROM …@sha256:60c8fd1…` (the capture's
  rebuilt base). Say once (S04): your first build also downloads `python:3.12-slim-bookworm` (~48 MB).
- Long outputs: first and last lines with a `…` line. Tracebacks: the first `/app/…` frame that
  matters and the last line. Wide outputs (`docker ps`, the collection listing) wrap at 80 columns;
  highlight the cell being discussed. pandas tables print as captured.
- Versions are "at the time of recording": Docker Engine 29.8.2, Compose v5.6.0, Python 3.12.15,
  uv 0.13.1, chromadb 1.1.0, google-genai 1.39.1, Chroma server (`latest`).

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Two lanes, one database (S02; mini-map in S06–S14).** The lecture's naïve-RAG pipeline
  (A16, numbered as on B5) redrawn. Top lane: GREEN book pages (the knowledge base) → a PURPLE
  chunking tool → a tall BLUE **embedding model** box that spans both lanes → GREEN vectors → a TEAL
  cylinder (the vector database). Bottom lane: a PINK question → the *same* BLUE box → a PINK query
  vector → the cylinder → a prompt card ("prompt + query + context") → a BLUE LLM box → the answer
  back to the user. B5's three dashed regions fade in: Indexing (top lane), Retrieval (query lane
  and cylinder), Augmentation & Generation (prompt and LLM). Then the README's steps pin under the
  boxes with their flags: Chunk `--chunk`, Embed `--embed`, Load `--load` | Query `--query`, Chat
  `--chat`; its two step titles (`README.md:5`, `:9`) label the lanes. The shared box gets one rule:
  "same model, same kind of vector, both lanes". A second layer says where each box runs: the chunker
  in the CLI container (no network), both models at Google (pay per call, your key), the cylinder
  in its own container with its data on your laptop. From S06 on, a small copy sits bottom right
  with the active box lit, as the deck walks its pipeline.
- **V2 · Two containers, one network, three windows (S04, S05; lifecycle in S10, S16).** The
  laptop (GREY) with `~/AC215/llm-rag/` and `~/AC215/secrets/` side by side. Two TEAL boxes: the CLI
  container (`/app`, `/secrets`, and the GREEN `/.venv` outside both, `Dockerfile:18`) and the Chroma
  container (`/data`, listening on `:8000`). Compose lays the TEAL rail `llm-rag-network`
  (`docker-compose.yml:1-3`) with a PINK phone book `llm-rag-chromadb → 172.19.0.2`
  (`cli-container/04`). Three PINK mount routes (`../llm-rag → /app`, `../secrets → /secrets`,
  `./docker-volumes/chromadb → /data`; real paths `laptop/15`); a PINK `8000:8000` arrow through a
  GREY street door for curl and Chrome; a dashed BLUE line from the CLI box out to Vertex AI with
  the GOLD key riding it. `docker-shell.sh`'s three `export` lines drop values into the compose
  file's `$GCP_PROJECT` and `$GOOGLE_APPLICATION_CREDENTIALS` slots (interpolation; with no export
  the slots stay blank, S05's G5). S10: `exit` removes only the CLI box (`--rm`) while Chroma keeps
  glowing; `docker compose down` removes the Chroma box and the rail; the GREY data folder stays;
  `sh docker-shell.sh` puts a new box over the same folder.
- **V3 · Ruler and scissors (S06, S07).** The Tolminc story as a long ribbon of real text
  (`source/input-datasets/books/Tolminc Cheese.txt`, from line 3 on). char-split: a PURPLE ruler
  window of 350 characters slides with a stride of 330; where two windows meet, a 20-character band
  glows in both; the cut lands mid-word, `…intended to ac` | `s she intended to accomplish…`
  (`cli-container/12`); a counter ticks to 24. recursive-split: PURPLE scissors hunt for `\n\n` gaps
  first, then `\n`, then spaces, so every cut is between words; a wide band (up to 200 characters,
  the library default) repeats the end of one chunk at the start of the next: chunk 1 starts again
  at `## Chapter One…` (`15`); the counter ticks to 35. Coda: two bars for the whole corpus, 8,248
  vs 14,228 (`11`, `14`). The lecture's own example echoes small at the side: the 50-character
  piece ending `artificial intelli` (B15).
- **V4 · Meaning as direction (S08; reused in S11).** Chunk cards fly into a 3-D sphere and each
  becomes a GREEN arrow from the origin (caption: "drawn in 3-D; each real vector has 256
  numbers"); arrows about milk and curd cluster, arrows of licence text sit elsewhere (an
  illustration, not a measurement). A 3,072-cell bar (the model's full output) is cut to its first
  256 cells (`output_dimensionality`, `cli.py:101-102`). The lecture's personality game (A40–A43):
  the instructor and three candidates as five-number vectors (Big Five scores), redrawn as arrows in
  a 2-D sketch; cosine (the angle, A42's formula) picks A (0.986 / 0.976 / 0.886); the dot product,
  which also counts length, would pick B (81.2 vs 80.2, SLIDES.md); a measure is a choice (A44–A47).
  Then the real numbers: the first five of a Tolminc vector and the lengths 0.369–0.402
  (`recorded-embeddings/06`): our arrows are shorter than 1, and cosine only looks at the angle.
- **V5 · Records, a highway index, a folder on your disk (S09; S10).** GREEN arrows drop into rows
  with four cells: id (`1021665fac86c5a5-0`), document (the chunk text), metadata
  (`{book, author, year}`), embedding. Rows stack into a collection, one per chunk type
  (`f"{method}-collection"`, `cli.py:277`), created with `{"hnsw:space": "cosine"}`. The slow scan
  (A33–A36): a PINK pointer walks down 8,248 rows with a ticking counter. The index (A37–A38):
  the rows lift into a layered graph — a sparse "highway" layer on top, denser layers below — and
  the pointer hops down in a handful of steps (HNSW, the index Chroma builds; labelled "our
  illustration of HNSW"). Zoom out: the cylinder sits in the TEAL Chroma box, its contents pour
  through the PINK `/data` route into the GREY `docker-volumes/chromadb/` folder: `chroma.sqlite3`
  (59.8 MB) and two UUID folders, one index per collection (`recorded-embeddings/04`).
- **V6 · Rank, cut — and filter first (S11, S12).** S11, the lecture's A48–A53: a column of stored
  vectors and the PINK query vector; similarity scores appear (the lecture's example numbers 0.57,
  0.77, 0.43, 0.93, tagged as such), the column re-sorts, a YELLOW K-line cuts it. Then the flip:
  each score becomes 1 − score and the arrow of "better" turns upside down — Chroma reports
  distances, smaller is closer. S12: the 8,248 GREEN points of the char-split collection;
  `where book = The Complete Book of Cheese` dims all but 1,355; `$contains "Italian"` dims all but
  64 (`recorded-embeddings/08`). The stand-in query vector (a stored Tolminc chunk) shines a PINK
  beam: without the mask its 10 nearest are Tolminc chunks at 0.0000–0.1627; with the mask the beam
  must reach the far survivors, all from *The Complete Book of Cheese*, at 0.2833–0.3123 (`09`). A
  small strip of the lecture's A32 stages (Indexing → Vector Database → Querying → Post Processing)
  shows the filter box sliding from Post Processing to *before* Querying: what Chroma does.
- **V7 · The final prompt (S13).** The lecture's three blocks (A58–A59): a system prompt, the query,
  the context. In the tutorial the query is PINK, the context is ten GREEN chunk cards, and the
  system prompt is a GREY dashed ghost card labelled `SYSTEM_INSTRUCTION` (`cli.py:40`). The query
  and the cards stack into one prompt card in the shape of `cli.py:388-391` (question, then the
  chunks joined by newlines); it flows into the BLUE LLM box and an answer comes out (no text: what
  the answer *should* draw from is shown as arrows back to the cards). The ghost's cable hangs
  unplugged (RED): `generate_content(model=…, contents=INPUT_PROMPT)` has no `config`
  (`cli.py:394-396`). The fix plugs it in (`config=types.GenerateContentConfig(system_instruction=…)`,
  labelled "fix, not in the repo"); last year's branch had it plugged (`pipenv-branch/cli.py:62-64`).
- **V8 · A seismograph of meaning (S14).** A row of sentence tiles (the regex `(?<=[.?!])\s+`,
  `semantic_splitter.py:118`). A ±1 bracket slides over every sentence; each three-sentence window
  goes through the BLUE embedding box (a GOLD tick per batch of 50, `:206`) and comes out as an
  arrow; the cosine distance between each window and the next plots as a PINK curve over the text;
  a YELLOW line rises to the 95th percentile of all distances (`:91-96`, `:137-141`); the spikes
  above it become cuts (`:239-243`), and the ribbon falls apart into chunks of very different
  lengths. The lecture's version (B21–B33: an anchor, groups, 0.89 / 0.85 / 0.68, threshold 0.8)
  plays small at the side first, then the code's rule replaces it.

## README step tracker (ReadmeTracker, top-left)

Step titles ≤ 3 words. The tracker's section is the README heading (a short label where the heading
is long). `README.md` of `dlops-io/llm-rag`, branch `main` @ `e17a39f`:

- *Prerequisites* (`:45-48`): Docker installed · Clone repo (2)
- *Setup GCP Service Account* (`:52-69`), label "Service Account": Open console · Create account ·
  Grant roles · Keys tab · Add JSON key · Rename, save (6; README item 4, "This will create a
  service account", folds into step 2)
- *Run LLM RAG Container* (`:75-85`), label "Run Container": cd llm-rag · Set GCP_PROJECT · Run
  script (3)
- *Chunk Documents* (`:91-116`), label "Chunk": Visualiser · Char split · Recursive split (3)
- *Generate Embeddings* (`:122-138`), label "Embed": Embed char · Embed recursive (2)
- *Load Embeddings into Vector Database* (`:144-165`), label "Load": Load char · Load recursive ·
  Chroma UI (3)
- *Query the Vector Database* (`:171-186`), label "Query": Query char · Query recursive (2)
- *Chat with LLM* (`:192-214`), label "Chat": Chat char · Chat recursive · Chat tool (3)
- *Advanced RAG: Semantic Chunking* (`:220-236`), label "Semantic Chunking": Semantic run (1)
- *Agents* (`:242-271`), label "Agents (L06)": Run agent (1) — preview only, S16

Ordering notes (say them in a clause where they occur):
1. The README links the chunk visualiser (`:95`) before the two chunk commands; S06 shows it first,
   as the idea V3 animates (the tool itself is drawn, tagged `illustration`).
2. The captures ran `--load` once *before* there were embeddings (`cli-container/30`, `31`), then
   again on the staff's embeddings (`recorded-embeddings/01`, `02`). S09 shows the first briefly
   (the first-time messages and the `0` files symptom of a failed embed), then the recorded loads;
   that is why the recorded run says `Deleted existing collection`.
3. The restart (S10) is not in the README (it only claims persistence, `:160`): it sits between the
   parts so that part 2 starts with a fresh `sh docker-shell.sh` (tracker *Run Container* step 3
   again).
4. The README's "Chat tool" (`:211`) and "Chroma UI" (`:162`) are links, not commands: drawn as a
   browser window, tagged `illustration`.
5. *Agents* is L06's tutorial (course map; digest header): the command appears once in S16 under a
   `preview` tag.

Steps the README does not have are marked `extra` in the tracker caption and in the narration
("this one isn't in the README"): `docker --version; docker compose version`, `mkdir secrets; ls`,
enabling the Vertex AI API (console), `ls -a; git log --oneline -1`, `docker ps`, `docker inspect`
(mounts), `echo $GCP_PROJECT … ls -la /secrets`, `getent hosts llm-rag-chromadb; curl …`,
`curl http://localhost:8000/api/v2/heartbeat`, `ls -la docker-volumes/chromadb`, the G5 demo
(`docker compose run --rm llm-rag-cli`), the G1 demo (a clone named `llm-rag-main`), `wc -l
outputs/…`, the overlap and recursive-chunk one-liners, `ls -la outputs`, the staff-embeddings copy,
the vector-length check, the collection listings, the metadata-per-book check, `--get`, the filter
counts, the stand-in query, the CORS check, `exit`, `docker ps -a`, `docker compose down`, `docker
images`, `git status`.

## Scene plan

Each scene names the slides it stands on (`Lecture:`; the GREY `lecture_ref` tag shows that range)
or "none" when the lecture does not cover the step.

### Part 1 — build the index

**S01 · A model that never read the book (~220 words).** Lecture: A6–A11. Cold open on the README's
question, `How is tolminc cheese made?` (`cli.py:318`), typed into a chat box (drawn). The knowledge
base appears: eleven books, one of them the instructor's short story — a panel of
`Tolminc Cheese.txt · lines 3-4` (`# Tolminc: A Cheese, a Valley, and the Art of Waiting`, *A
fictional tale inspired by Alpine cheesemaking*). "A model trained before this story existed has
never read it. Ask it anyway, and it will answer — from somewhere else." The lecture's four LLM
weaknesses as four quick chips (A6: stale training data, no specialised knowledge, hallucination, no
sources; A7: RAG fixes the first two). Three roads (A8–A10) as three paths from a pile of books to
the BLUE LLM: paste everything (the prompt overflows: "garbage", RED cross), fine-tune (a slow
clock; "that's lecture 8", GREY dashed), RAG: a librarian hands the model ten relevant pages — an
open-book exam (digest C1; our image, untagged: deck B uses the exam for another point, paid off
in S16). The lecture's crowded map of RAG techniques (A11) as a blurred
GREY sketch with four glowing questions — *what is an embedding? a vector database? a query? the
context?* — "this video answers all four, with commands". How to follow along: the README tracker
(top left), `lecture_ref` (top right; A = the main deck, B = the supplement), code panels with
`path · lines`, ▶ your turn, and the tags `recorded`, `expected`, `illustration`, `extra`. Honest
limit, said once: recorded on 16 October 2026 on a Linux laptop with Docker Engine 29.8.2 and
Compose v5.6.0 (`laptop/00`, two lines) without a Google key: Docker, chunking and the database ran
for real; the embeddings are the teaching staff's own recorded vectors; wherever the code calls
Google you see the command, the real no-key error and what to look for. Every command is in the
study guide in MLOps_Learning.

**S02 · Two lanes, one database (~260).** Lecture: A12–A16, B5–B6. No commands. A12 first: user →
"RAG" (a small gear cluster) → vector database → retrieved texts → "full prompt" → LLM → response;
the database talks only to the RAG code, never to the LLM. Then V1 grows out of it (A16), with B5's
numbers 1–6 and its three phases. The README's own words pin onto the lanes: `Step 1: Chunk -> Embed
-> Load` (`README.md:5`) over the top lane, `Step 2: Query -> Embed -> Retrieve -> LLM -> Generate
Answer` (`:9`) over the bottom one, and the five steps of `:17-21` (redrawn as text, no emoji) under
the boxes with their `cli.py` flags. Two rules, said slowly: the top lane runs once, offline, and is
slow and costs a little; the bottom lane runs per question; and **both lanes go through the same
embedding model**, or the question and the chunks don't live in the same space. "Indexing" here
means the whole top lane (B5's sense; the lecture also uses the word for the search structure, S09).
V1's second layer: what runs where — the chunker inside your CLI container, both models at Google
(GOLD: pay per call; nothing keeps running in the cloud — no VM, no bucket), the database in its
own container with its files on your laptop. Close on the CLI container's box: "every step is one
`python cli.py --<step>` inside it; first, let's get that container running."

**S03 · Your key, your folders, your project (~270).** Lecture: none. Tracker *Prerequisites*:
extra `docker --version; docker compose version` (`laptop/01`: 29.8.2, v5.6.0; the script needs
`docker compose` with a space); the README links the repo, the clone command is not printed: ▶
`git clone https://github.com/dlops-io/llm-rag.git` (`laptop/02`). Extra `mkdir secrets; ls`
(`03`: `llm-rag  secrets`): the layout of `README.md:64-69` — side by side, and the clone keeps the
name `llm-rag` (S05 shows why). Tracker *Service Account* as a schematic console (tagged
`illustration`, no logo): Service accounts › Create `llm-service-account` › roles Storage Admin and
Gemini Enterprise Agent Platform User ("Vertex AI User" in older projects) › KEYS › Add key ›
Create new key › JSON; the GOLD key drops into `secrets/` renamed `llm-service-account.json`. GOLD
tag: "this file spends your project's money". Panel `.gitignore · lines 1-5`: no `secrets` line —
the key stays outside the repo because it is *beside* it. L04's three gates come back (V3 of L04 in
miniature): who (the key), may (the role), switched on (the API). Errata, kindly: (1) nothing here
uses Cloud Storage (no storage call anywhere in the code, digest E5) — the Vertex role is the one that
matters; (2) the README never says to enable the **Vertex AI API** (E6): extra, in the console
(illustration) — without it the first embed fails with `SERVICE_DISABLED`. Tracker *Run Container*:
▶ `cd llm-rag` (`04`); extra `ls -a; git log --oneline -1` (`05`: the files, `e17a39f`, the pinned
commit); ▶ set `GCP_PROJECT` in `docker-shell.sh` (README step 2), shown as the real diff (`06`: line
7, `ac215-project` → `your-project-id`): "type your own Project ID, the one inside your key — not the
project's name; leave line 8 alone, it's a path inside the container". If you skip the edit, calls go
to the course's project and Google answers with a permission error (G3). ▶ your turn.

**S04 · One script, two containers (~290).** Lecture: none. Tracker *Run Container* step 3. Bridge
from L04: port_toy's two containers on one network, the mega-pipeline's `../secrets` mount —
"today, both at once". V2 first, built from the files: panel `docker-shell.sh · lines 6-12` (three
exports, then `docker compose run --rm $IMAGE_NAME`), panels `docker-compose.yml · lines 1-17` and
`· lines 18-26`: the network name; the CLI service (`image:` + `build: .`, the two mounts, the two
`$` slots, `depends_on: chromadb`); the Chroma service (`chromadb/chroma:latest`, `container_name:
llm-rag-chromadb`, `8000:8000`, `./docker-volumes/chromadb:/data`, the CORS line, "for the course's
web tools, S09"). One clause on `/.venv` (`Dockerfile:18`, `:45`): the venv lives outside `/app`, so
the code mount can't hide it — edit `cli.py` on your laptop, rerun, no rebuild (L2/L3 callback).
Concept done, then ▶ `sh docker-shell.sh` (`laptop/07`, trimmed: 1–9, 10, 21, 22, 25, 26, `…`,
36–45): Chroma is pulled and created first; `Image llm-rag-cli Pulling` / `failed to resolve
reference … not found` — "it looks like an error; it isn't: Compose asks Docker Hub for an image of
that name first, finds none, and builds" (RED → GREY "harmless"); `Building 81.5s`; the build
context is 112 MB (line 21) — mostly `.git` (103 MB, `05b`: the history still holds the staff's
database) — and with no `.dockerignore` the image keeps `.git` and the brand-new `chroma.sqlite3`
(`14b`; the mount hides both at run time; fix in exercises); `Container
llm-rag-llm-rag-cli-run-90678535ddef Created`; the banner (`Python 3.12.15`, `uv 0.13.1` at the time
of recording; `Architecture: x86_64` here, `aarch64` on Apple Silicon — both images run natively);
the prompt `app@92c5bfd26089:/app$` — "the part after `app@` is the container id". One clause,
kindly: the banner says "activated" one line before it activates (`docker-entrypoint.sh:6` vs
`:12`; cosmetic). Your first build also downloads `python:3.12-slim-bookworm`; the next start skips
the build (S10). ▶ your turn.

**S05 · Names, mounts, and two traps (~240).** Lecture: none. All extras, each confirming a piece
of V2. From a second laptop terminal: `docker ps` (`laptop/08`, NAMES and PORTS cells highlighted):
`llm-rag-chromadb` with `0.0.0.0:8000->8000/tcp`, and the CLI container is
`llm-rag-llm-rag-cli-run-…`, not `llm-rag-cli` — kindly: `docker compose run` ignores
`container_name` (`docker-compose.yml:9`), so look the name up with `docker ps`. `docker inspect …`
(`15`): the three mounts exactly as drawn. Inside the container: `echo GCP_PROJECT=…; ls -la /secrets`
(`cli-container/01`): your project ID arrived; `/secrets` is empty here — yours lists the key. By
name: `getent hosts llm-rag-chromadb; curl …/api/v2/heartbeat` (`04`: `172.19.0.2`, a heartbeat) —
the phone book on the rail (L04). From the laptop: `curl http://localhost:8000/api/v2/heartbeat`
(`laptop/10`) — the published door, for you and the browser; the CLI doesn't need it. `ls -la
docker-volumes/chromadb` (`13`): the folder already exists, owned by **root** (on Linux you'll need
`sudo` to delete it, S16). Two traps, both real: **G5** — typing the Compose command yourself, extra
`docker compose run --rm llm-rag-cli` (`gotchas/01:1-4`): two `WARN … variable is not set.
Defaulting to a blank string.` lines, and even `--chunk` dies at import (`:16`, `:55`:
`DefaultCredentialsError: File  was not found.` — two spaces around an empty file name): the `$`
slots are filled from *your* shell, so always start through the script. **G1** — a clone with
another name (`gotchas/03`, `04:5-8`: `/bin/bash: docker-entrypoint.sh: No such file or directory`,
exit 127; `05:5-6`): `../llm-rag:/app` names the folder; Docker creates an empty, root-owned
`llm-rag` and mounts it over your code. Fix: keep the name (or change the mount to `.:/app`), and
delete the stray folder. One clause (`11`, `11b`): `latest` is unpinned, and the server's three
version numbers disagree (1.5.9 tag, 1.4.4, "1.0.0"); pin a tag for a team (exercise). ▶ your turn.

**S06 · Cutting the books: a ruler (~280).** Lecture: A19–A22, B14–B15. Tracker *Chunk*. Why cut
at all: a whole book as one vector blurs every question into one point, and eleven books don't fit
in a prompt; the chunk is the unit you retrieve *and* the unit you paste (A20–A21: "so the model can
focus"). V1 mini-map: Chunking lit. Step 1, the visualiser (`README.md:95`, tagged `illustration`:
a browser window, "open it in Chrome"). V3's ruler, then panel `cli.py · lines 183-194`
(`chunk_size = 350`, `chunk_overlap = 20`, `separator=''`: characters, not words). PONDER 1 (8 s):
"The story is 7,808 characters. Windows of 350 that overlap by 20 — how many chunks?" Answer: each
new chunk adds 330 new characters, ⌈(7,808 − 20) / 330⌉ = 24. ▶ `python cli.py --chunk --chunk_type
char-split` (`cli-container/10`, trimmed: 1–4, 5–9, `…`, 32–34, `…`, 104): `Number of files to
process: 11`, the first book, `Number of chunks: 24` for Tolminc. No key needed: char-split's branch of
`chunk()` never calls Google. Extra `wc -l outputs/chunks-char-split-*.jsonl` (`11`: 24 … `8248 total`). Extra, the
overlap (`12`): `'…things she intended to ac'` / `'s she intended to accomplish…'` — the ruler cut a
word in half, the 20-character band repeats it (the lecture's `intelli|gence`, B15). The files are on
your laptop (extra `ls -la outputs | head -5`, `laptop/16`: owned by `student`, git-ignored). Look at
row 0 of each Gutenberg book in the output: `The Project Gutenberg eBook of …` — every one of those
books starts (and ends) with licence text, which gets chunked like the rest (E18; "remember this in
part 2"). ▶ your turn.

**S07 · Recursive split and its hidden overlap (~220).** Lecture: B16–B19. Tracker *Chunk* step 3.
Panel `cli.py · lines 196-205`: only `chunk_size=350` — no overlap given. V3's scissors: separators
`\n\n`, `\n`, space, then characters; cuts fall between words. ▶ `python cli.py --chunk --chunk_type
recursive-split` (`13`: 1–4, `…`, 32–33: `Number of chunks: 35`, `…`, 104). Extra `wc -l
outputs/chunks-recursive-split-*.jsonl` (`14`: 35 … `14228 total`). PONDER 2 (8 s): "Same chunk
size, 350. Why 14,228 chunks instead of 8,248?" Answer with extra `15` (lines 8–14): chunk 1 starts
*again* at `## Chapter One…` — the splitter's library default is `chunk_overlap=200` (E14: the
README says "overlapping" but not how much), and cutting at boundaries makes chunks shorter than
350. Overlap is insurance against cutting an idea in half, but every repeated character is embedded,
stored and paid for. The lecture's B16–B19: a ruler runs one section into the next; the ideal chunks
follow the document's own structure. Recursive goes part of the way (paragraphs); semantic chunking
(S14) goes further. V1: Chunking done.

**S08 · Meaning as direction: embeddings (~330).** Lecture: A24–A28, A40–A47. Tracker *Embed*. V4
first: the embedding model turns a chunk into one vector (A25; a sentence embedding, not a word
embedding, A28), similar meaning → similar direction; the personality game and its two measures.
Panel `cli.py · lines 22-27` (`gemini-embedding-001`, `EMBEDDING_DIMENSION = 256`, `GCP_LOCATION =
"global"`) and `· lines 96-106` (`embed_content(contents=batch, output_dimensionality=…)`; batches of
100 at `:252-253`; on an API error it retries after 5, 10, 20, 40, 80 s, `:108-119`). V1: the shared
box lights in both lanes — `generate_query_embedding` (`:75-84`) asks the same model for the same 256
numbers. ▶ `python cli.py --embed --chunk_type char-split` (`cli-container/20`, tagged `no key`:
lines 1–6, `…`, the `cli.py, line 98` frame (21–22), last line 73): "this is the first command that
calls Google: on our machine it stops at the key, on yours it runs". What to look for with your key
(caption citing `cli.py:240-264`): per book `Processing file: outputs/chunks-char-split-…`, a 5-second
pause (`:256`), a second table with an `embedding` column, and `embeddings-*.jsonl` files beside the
chunks. ▶ `python cli.py --embed --chunk_type recursive-split` (command only). GOLD tag: about 89
calls for char-split and 148 for recursive-split, a few cents each by the digest's estimate — check
the current price list. How the video continues without a key: the staff committed their `outputs/`
in `68e0bde` and removed it in `58dd602`; every clone still carries it; their 22 chunk files are
byte-identical to ours, so their vectors are what this command makes (a card from
`recorded-embeddings/00`: `68e0bde`, 22 files, 82 MB; tagged `recorded`, the command is not typed).
Extra `06` (recorded): 24 rows, 256 numbers each, the first five, lengths 0.369–0.402. PONDER 3
(8 s): "These vectors are not length 1. Does that change which chunks count as nearest in our
collection?" Answer: not with cosine, which only sees the angle (`hnsw:space: cosine`, S09); with
L2 distance (Chroma's default) or a dot product, length would leak into the ranking — exactly the
game's lesson.

**S09 · Load: records, an index, a folder on your disk (~300).** Lecture: A30–A38. Tracker *Load*.
Why a database (A31: SQL finds `WHERE price BETWEEN 10 AND 50`, not "meaning like this"). V5:
records, the collection, the slow scan, the index ("indexing" in the A32–A38 sense). Panel
`cli.py · lines 280-290` (delete, then create with `{"hnsw:space": "cosine"}`: every load is a full
rebuild) and `· lines 126-138` (ids from the book name's hash; metadata looked up per book). ▶
`python cli.py --load --chunk_type char-split`, first as captured before any embeddings existed
(`cli-container/30`: `did not exist. Creating new.`, `Created new empty collection`, `Number of files
to process: 0`, exit 0 — "if you see 0, your embed step didn't finish"), then on the staff's vectors
(`recorded-embeddings/01`, tagged `recorded`: 1–10, 11–12 (the `embedding` column), 19–22 (`Inserted
500 items...` … `Finished inserting 1355 items`), `…`, 152–154); the eleven books add up to 8,248. ▶
`python cli.py --load --chunk_type recursive-split` (`02`: first lines, `…`, 163–165; 14,228). Extras:
`03` (`"dimension":256`, fixed by the first insert; an empty collection said `null`, `laptop/17b`);
`07` (lines 11, 13, 22): `count: 8248`, one book's metadata, and the Woman's Institute book with **no
author or year** — erratum, kindly: `filename.split(".")[0]` (`cli.py:178`) cut its name at the first
dot, so it misses its `book_mappings` key (`:70`); fix with `os.path.splitext` and reload (E8). On
the laptop (`recorded-embeddings/04`): `chroma.sqlite3` 59.8 MB and two UUID folders — one HNSW index
per collection — 82 MB, owned by root; the README's persistence claim (`:160`) gets its proof in
S10. Step 3, the Chroma UI (`:162`): a browser window (illustration) reading *your* local database;
it can, because Chroma answers that one web origin (extra `laptop/12` vs `12b`: the
`access-control-allow-origin` line appears only for `https://ac215-llm-rag.dlops.io`;
`docker-compose.yml:26`); the README asks for Chrome. ▶ your turn. Close part 1: the V1 top lane
glows end to end; "the index is built. In part 2 we ask it questions — after checking it survives
closing the laptop." Clean frame.

### Part 2 — ask the index

**S10 · Exit, and the index survives (~190).** Lecture: none. V2's lifecycle. Extra `exit`
(`laptop/07:45-46`); extra `docker ps -a` (`laptop/20`): the CLI container is gone (`--rm`) but
`llm-rag-chromadb` is still Up, port 8000 still taken (G8). Extra `docker compose down` (`21`):
two `WARN … variable is not set` lines — harmless: the variables live only in `docker-shell.sh`,
and `down` needs neither — then the container and the network removed. Extra (`22`): no
containers, no network, but `docker-volumes/chromadb/` still holds 59.8 MB and both index folders.
Tracker *Run Container* step 3, again: ▶ `sh docker-shell.sh` (`23`): `[+] run 2/2`, no pull, no
build — the image exists (one clause: after a `git pull` that changes `pyproject.toml` or the
Dockerfile, run `docker compose build`, G9), the banner, `app@390fe47a277a:/app$`. Extra (`24`):
both collections back with `"dimension":256`; extra `--get` (`cli-container/70`, the ids only):
the same ten records as before the restart. "The container was disposable; the data never lived in
it." ▶ your turn.

**S11 · Asking the database: rank and cut (~290).** Lecture: A39, A48–A53. Tracker *Query*. V1: the
bottom lane lights. V6's first half: the question goes through the same BLUE box, becomes a PINK
vector, and is compared with stored vectors; the lecture's scores, re-sort, the K-line; then the flip
to Chroma's distances, said kindly: "the lecture ranks by similarity, higher is better; Chroma reports
cosine distance, one minus the similarity — smaller is closer. Same order, opposite direction." Every
query returns exactly K results, relevant or not: nothing in this code sets a distance threshold. Panel
`cli.py · lines 309-323` (the query text, `generate_query_embedding`, `get_collection`) and `· lines
352-361` (variant #4, revealed in S12). ▶ `python cli.py --query --chunk_type char-split`
(`cli-container/40`, tagged `no key`: lines 1–3, the `cli.py, line 319` and `line 79` frames, last
line 64). Erratum, kindly: it prints `load()` — a copy-paste label (`cli.py:310`, E3). It stops before
it ever reaches Chroma: the question must become a vector first, and only the same Google model can
make one in the same space. ▶ `python cli.py --query --chunk_type recursive-split` (command only).
What to look for with your key (caption citing `cli.py:320`, `:360-361`): `Embedding values:` with 256
numbers, `Query: How is tolminc cheese made?`, then `Results:` — a dict of **lists of lists**, one
inner list per query: `ids`, `distances`, `metadatas`, `documents`; that's why the code reads
`results["documents"][0]` (`:386`). No `Results:` values are shown: none were recorded.

**S12 · Filters come first (~290).** Lecture: A54–A55. Tracker *Query* (still). Panel `cli.py · lines
352-361`: `n_results=10`, `where={"book": "The Complete Book of Cheese"}`, `where_document={"$contains":
"Italian"}`. PONDER 4 (8 s): "The question is about Tolminc. This query keeps only one book and only
chunks containing the word 'Italian'. What will the ten results be about?" Answer with real Chroma
runs on the loaded collection (extra, tagged `recorded`): the counts (`recorded-embeddings/08`): 8,248
→ 1,355 → 64 → **0** containing "Tolminc"; V6's mask. Then the stand-in query (`09`, tagged `stand-in`:
"a stored Tolminc chunk's vector, because the question itself needs Google to become a vector"): no
filter → ten Tolminc chunks at 0.0000 (itself) to 0.1627; with `cli.py`'s filters → ten chunks of *The
Complete Book of Cheese* at 0.2833–0.3123. Filters act **before** ranking, and top-k fills its ten
slots with whatever survives, however far. Said kindly: the lecture places metadata filtering in
post-processing, after ranking (A54); Chroma filters first. Erratum, kindly: the README says "Apply
various types of filters" (`:186`), but only variant #4 runs; #1–#3 are commented out (`:325-350`) —
uncomment #1 (no filter) to see Tolminc chunks; no rebuild, the code is mounted. `$contains` is a
case-sensitive *keyword filter*, not keyword ranking (S15). Extra, `python cli.py --get --chunk_type
char-split` (not in the README, `cli.py:402-418`; `recorded-embeddings/05`, trimmed to the ids and the
first document's opening): the same `where`, no ranking, no `distances` — and the ten records are the
Project Gutenberg header and licence (E18 payoff): strip it before chunking, then re-chunk, re-embed,
re-load.

**S13 · Chat: the prompt is the whole trick (~280).** Lecture: A57–A62. Tracker *Chat*. V1: the prompt
card and the LLM light. Panel `cli.py · lines 380-399`: the query again with **no** filter, `n_results=10`;
`INPUT_PROMPT` = the question, then the ten chunks joined by newlines (an f-string expression with
`"\n"` that needs Python 3.12, which is why the image pins it); `generate_content(model=GENERATIVE_MODEL,
contents=INPUT_PROMPT)`. V7: the lecture's three blocks; the ghost card; the unplugged cable. Panel
`cli.py · lines 40-47` (the instruction's first lines: answer only from the chunks; say so when they
don't contain enough). Erratum, kindly (E1): defined, never sent; the README promises answers
"grounded in your documents, not its own training data" (`:21`), but nothing tells the model so; last
year's version sent it (`pipenv-branch/cli.py · lines 62-64`); the fix, one argument (V7, "fix, not in
the repo"). "The LLM itself is unchanged" (A61–A62): no weights move; delete the collection and the
knowledge is gone. ▶ `python cli.py --chat --chunk_type char-split`, ▶ `python cli.py --chat
--chunk_type recursive-split`: commands only, no output panel ("on our machine both stop at the same
key error, at `cli.py:373`"). What to look for (caption citing `cli.py:365-399`): `Query: How is tolminc
cheese made??` (two question marks, E4 — the README shows one), `Results:`, `10`, `INPUT_PROMPT:` with
your chunks, `LLM Response:`. A test of grounding: the story is fiction (book line 4), so an answer
about Mara, her grandfather and the curd came from your chunks; an answer about real-world rules for
Tolminc came from the model's memory — or from an old index (S16). Compare the two chunk types'
answers. Step 3, the chat tool (`:211`, illustration). GOLD: one embedding call and one Gemini call per
question.

**S14 · Semantic chunking: cut where meaning shifts (~270).** Lecture: B13–B34. Tracker *Semantic
Chunking*. The lecture's B19: chunks that follow the document's sections are "the optimal way". V8:
the lecture's anchor walk first (small), then the code's rule, said kindly: "the slides join sentences
while similarity stays above 0.8; this code measures every gap and cuts the biggest 5 %". Panels
`semantic_splitter.py · lines 91-96` (`"percentile": 95`) and `· lines 239-243` (the cut indices).
Panel `cli.py · lines 207-215`: the chunker is handed `generate_text_embeddings` — the same Google
function as `--embed`. PONDER 5 (8 s): "char-split ran `--chunk` without a key. Can semantic-split?"
Answer: no — to find where meaning shifts it must embed every sentence window first. ▶ `python cli.py
--chunk --embed --load --chunk_type semantic-split` (`cli-container/60`, tagged `no key`: lines 1–5,
the frames `cli.py, line 212`, `semantic_splitter.py, line 229`, `line 206`, `cli.py, line 98`, last
line 75): it fails inside `chunk()`, on the first book, before a single chunk is saved. GOLD: the digest
estimates ~26,000 sentences ≈ 528 embedding calls just to chunk the corpus, ~90 more to embed the
chunks; budget time for 429 retries (the backoff covers short ones, G13). Try it on one book first
(move the others out of `input-datasets/books/` for a moment). Chunks come out very uneven, and a
single-topic book still gets cut at its top 5 % of gaps. Not in the README, one clause: afterwards
`--chat --chunk_type semantic-split` works the same way. ▶ your turn (with your key).

**S15 · Beyond naïve RAG: what the lecture adds (~210).** Lecture: B6–B10, B35–B65. Tagged "concept ·
not in the tutorial's code" throughout; no commands. B6–B10's frame as a strip: Indexing → Retrieval →
Augmentation & Generation, with a Pre-Retrieval and a Post-Retrieval column; S14's semantic chunking
lights in Pre-Retrieval — the one advanced lever this tutorial implements. Three short beats, GREY
dashed: (1) Pre-Retrieval, query rewriting (B36–B39): a cluttered question becomes "Where do dolphins
live?"; a vague one can make the rewriter invent details. (2) Retrieval, hybrid search (B42–B48): a
keyword ranking (BM25) and a vector ranking of the three "Chester … bank" paragraphs merge by
Reciprocal Rank Fusion, each list adding w / (k + rank): with k = 0 and w = 0.5 the scores are 0.75,
0.67, 0.42 — the near-paraphrase wins; contrast: the tutorial's `$contains` only filters by a word.
(3) Post-Retrieval, re-ranking (B51–B65): a fast retriever (a bi-encoder: vectors made before the
question existed, like our 8,248) brings back 25 candidates with the right ones scattered; a slow
cross-encoder reads each (question, chunk) pair and reorders them — "strong together". Close: none of
these is in `cli.py`; they are what you'd reach for when naïve retrieval brings back the wrong ten.

**S16 · Tear down, a stale index, recap (~300).** Lecture: B68–B76, A63. Teardown (extras): ▶ `exit`;
`docker compose down` (`laptop/25`: the harmless WARNs, container and network removed); `docker
images` (`26`): `llm-rag-cli` 2.11 GB, `chromadb/chroma:latest` 826 MB, the base 198 MB — `docker
image rm` them if you need the space; `git status` (`27`): only `docker-shell.sh` modified, while
`outputs/` and `docker-volumes/` are ignored and stay on your disk (on Linux `docker-volumes/` is
root's: `sudo rm -rf docker-volumes` if you want it gone). GOLD: nothing keeps running in Google
Cloud; you paid per call. The key is a long-lived credential: keep it in `secrets/` beside the repo
(inside it, it isn't ignored and `COPY . ./` would bake it into the image, G20), and delete it in IAM
when the course ends. The stale index (E7, G18): the staff's recorded run of 22 September (`out.txt`,
the L06 agent; `expected/out-txt-agent-run.txt:74`) retrieved "…known as transhumance, shaped not just
the economic life…" — text from the *old* Tolminc book (panel `tolminc-before-85bba32/…/Tolminc
Cheese.txt`, an excerpt of line 102), replaced the same day by today's fictional story (line 4). The
database answers from what was loaded, not from what's on disk now: when the books change, re-run
chunk → embed → load. L06 preview, tracker *Agents (L06)*: ▶ `python cli.py --agent --chunk_type
char-split` (`README.md:258`, command only, tagged `preview`); from the staff's recorded run, one
line: `Function: get_book_by_author` (`expected/out-txt-agent-run.txt:65`) — the model chose a retrieval
tool itself. The lecture's Self-RAG (B74–B76: a Retrieve token decides *whether* to look things up,
critique tokens check relevance and support) is the same idea taken further (my link, not the
slides'). Recap: A11/A63's blurred map returns and its four questions light up answered (embedding,
vector database, query, context). Recap questions (5, on screen one at a time, answers in
exercises.md): (1) which `cli.py` flags belong to the indexing lane and which to the query lane, and
what must both lanes share; (2) why the CLI reaches the database at `llm-rag-chromadb:8000`, and who
uses the published port 8000; (3) what `chunk_overlap` buys and costs, and why recursive-split made
14,228 chunks from the same `chunk_size`; (4) why the README's `--query` returned no Tolminc text;
(5) what the tutorial's prompt is missing compared with the lecture's final prompt, and the one-line
fix. Study guide and exercises in MLOps_Learning. Clean frame.

## Ponder questions (summary)

| # | scene | question | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S06 | 7,808 characters, windows of 350 overlapping by 20: how many chunks? | 24: each new chunk adds 330 characters, ⌈7,788 / 330⌉ (`cli-container/10`, `11`) |
| 2 | S07 | Same `chunk_size` 350: why 14,228 recursive chunks instead of 8,248? | a hidden default overlap of up to 200 characters, and boundary cuts make chunks shorter (`15`) |
| 3 | S08 | The vectors' lengths are 0.369–0.402, not 1: does that change the nearest chunks? | not with cosine (angle only); it would with L2 or a dot product (`recorded-embeddings/06`; A44–A47) |
| 4 | S12 | Tolminc question, filters "The Complete Book of Cheese" + "Italian": what are the ten results about? | Italian cheeses from that book; none mentions Tolminc: filters act before ranking (`08`, `09`) |
| 5 | S14 | char-split ran `--chunk` without a key; can semantic-split? | no: it embeds every sentence window to find the cuts (`cli-container/60`) |

## Errata to state (kindly, with the fix)

1. **The system instruction is never sent** (`cli.py:40-58` vs `:394-396`; `README.md:21`) → pass it:
   `config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)`; last year's code did
   (`pipenv-branch/cli.py:62-64`) (S13).
2. **Enabling the Vertex AI API is missing** (`README.md:45-69`) → enable `aiplatform.googleapis.com`
   in your project (S03).
3. **Storage Admin is never used** (`README.md:57`; no storage call in the code) → the Vertex role is
   the one the code needs; grant only what's used (S03).
4. **`--query` runs one variant, whose filters exclude the question's topic** (`README.md:185-186` vs
   `cli.py:325-361`; real `recorded-embeddings/08`) → uncomment variant #1 to see unfiltered results
   (S12).
5. **`--query` prints `load()`** (`cli.py:310`; real `cli-container/40:3`) — a label only (S11).
6. **Chat's question has two question marks** (`cli.py:372` vs `README.md:205`) — harmless (S13).
7. **One book loses its author and year** (`cli.py:178`, `:70`; real `recorded-embeddings/07:22`) →
   `os.path.splitext(filename)[0]`, then re-chunk, re-embed, re-load (S09).
8. **recursive-split's overlap is 200, unstated** (`README.md:17`, `:93` vs `cli.py:199-200` + the
   library default; real `cli-container/15`) → set `chunk_overlap` explicitly if you want another
   value (S07).
9. **The corpus still carries the Project Gutenberg header and licence** (real `cli-container/10`
   row 0s, `recorded-embeddings/05`) → strip outside the START/END markers before chunking (S06, S12).
10. **The clone must be named `llm-rag`** (`docker-compose.yml:12`; real `gotchas/04`, `05`) → keep the
    name or mount `.:/app`; delete the stray root-owned folder (S05).
11. **The CLI container isn't called `llm-rag-cli`** (`docker-compose.yml:9`; real `laptop/08`) → find it
    with `docker ps` (S05).
12. **The first start prints a "not found" pull error** (real `laptop/07:6-8`) — harmless: Compose then
    builds (S04).
13. **No `.dockerignore`** (`Dockerfile:48`; real `laptop/14b`): the image carries `.git` (103 MB) and a
    copy of `chroma.sqlite3` → add one with `.git`, `outputs/`, `docker-volumes/`, `__pycache__/` (S04,
    one clause; exercises).
14. **`chromadb/chroma:latest` is unpinned** (`docker-compose.yml:19`; real `laptop/11`, `11b`) → pin a
    tag for a team (S05, one clause).
15. **The banner says "activated" before it activates** (`docker-entrypoint.sh:6`, `:12`) — cosmetic
    (S04, one clause).
16. **`out.txt` comes from an older book** (real `expected/out-txt-agent-run.txt:74` vs today's
    `Tolminc Cheese.txt`) → an index is a snapshot; rebuild it when the books change (S16).

Slides vs captures (not errata of the tutorial; said kindly where they occur): similarity vs
distance (S11), filtering before ranking (S12), the system prompt (S13), the semantic-chunking rule
(S14).

Not on screen (exercises or study guide only): unused `openai` / `openai-agents` and imports (E11);
`task_type` for asymmetric embeddings (E16); the course-site lecture numbering (E17); the batch-size
question for `gemini-embedding-001` (Q2); `query_texts` silently using Chroma's own embedding function;
changing `EMBEDDING_DIMENSION` without re-embedding; port 8000 already taken (G6); a container-name
conflict with another copy (G7); `uv add` lost on exit (G16); Windows line endings (G22); running
`cli.py` on the laptop (G11).

## Costs and teardown

- **Your project pays per call, and only per call.** Embedding (`gemini-embedding-001`): ~89 calls for
  char-split, ~148 for recursive-split, ~528 + ~90 for semantic-split; one call per query; chat adds
  one Gemini call (`gemini-3.1-flash-lite`). The digest estimates the whole tutorial, done twice, at
  well under $2 of credits; it could not verify prices, so the narration says "a few cents" and "check
  the current price list". GOLD tags in S02 (the frame), S08 (embed), S13 (chat), S14 (semantic).
  Nothing here was billed: the recording had no key.
- **Nothing to delete in the cloud**: no VM, no bucket, no endpoint (S02, S16).
- **The key** is a long-lived credential: beside the repo, never in it, never in an image; delete it in
  IAM when the course ends (S03, S16).
- **Local teardown (S16):** `exit` (the CLI container is removed, `--rm`), `docker compose down` (Chroma
  and the network; `exit` alone leaves Chroma running and port 8000 taken, S10); the index and the
  chunk files stay in `docker-volumes/` and `outputs/` (git-ignored; `docker-volumes/` is root's on
  Linux); `docker image rm llm-rag-cli chromadb/chroma:latest` frees ~2.9 GB if you need it.

## README commands checklist (for the follow-along review)

| README command | where | scene (capture) |
| --- | --- | --- |
| "Have Docker installed" | `README.md:47` | S03 (`laptop/01`, extra check) |
| repo link → `git clone https://github.com/dlops-io/llm-rag.git` (the command is not printed) | `:48` | S03 (`laptop/02`) |
| console: service account, two roles, KEYS › JSON, rename into `secrets/` | `:54-69` | S03 (illustration; `laptop/03`) |
| "inside the `llm-rag` folder" → `cd llm-rag` | `:79` | S03 (`laptop/04`) |
| update `GCP_PROJECT` in `docker-shell.sh` | `:80` | S03 (`laptop/06`) |
| `sh docker-shell.sh` | `:84` | S04 (`laptop/07`); S10 (`23`) |
| chunk visualiser (link) | `:95` | S06 (illustration) |
| `python cli.py --chunk --chunk_type char-split` | `:103` | S06 (`cli-container/10`) |
| `python cli.py --chunk --chunk_type recursive-split` | `:109` | S07 (`13`) |
| `python cli.py --embed --chunk_type char-split` | `:129` | S08 (`20`, no key) |
| `python cli.py --embed --chunk_type recursive-split` | `:130` | S08 (command only) |
| `python cli.py --load --chunk_type char-split` | `:151` | S09 (`30`; `recorded-embeddings/01`) |
| `python cli.py --load --chunk_type recursive-split` | `:152` | S09 (`recorded-embeddings/02`; `31` not shown) |
| Chroma UI (link) | `:162` | S09 (illustration; `laptop/12`, `12b`) |
| `python cli.py --query --chunk_type char-split` | `:178` | S11 (`40`, no key) |
| `python cli.py --query --chunk_type recursive-split` | `:179` | S11 (command only) |
| `python cli.py --chat --chunk_type char-split` | `:199` | S13 (command only) |
| `python cli.py --chat --chunk_type recursive-split` | `:200` | S13 (command only) |
| Chat tool (link) | `:211` | S13 (illustration) |
| `python cli.py --chunk --embed --load --chunk_type semantic-split` | `:227` | S14 (`60`, no key) |
| `python cli.py --agent --chunk_type char-split` (L06) | `:258` | S16 (preview, command only; `expected/out-txt-agent-run.txt:65`) |

## Things never to do on screen

Series rules:
- No slide images, no memes, no PDF pages, no README figures (`images/llm-rag-flow-*.png`): redraw
  the idea and cite the slide number with `lecture_ref`.
- No Google/GCP logos or console screenshots: schematic drawings tagged `illustration` (service
  account, roles, keys, the API library, the course's web tools in a browser frame). No screenshot of
  `ac215-llm-rag.dlops.io`.
- No real person's name in captions, labels or narration: the prompt user is `student`; the Tolminc
  story is "the instructor's short story"; books are named by title, never by author. Never show a
  line that contains the instructor's name: `Tolminc Cheese.txt:1`, `cli.py:71`, `:435`,
  `README.md:263`, `agent_tools.py:28`, `pipenv-branch/cli.py:78`, `:407`, `out.txt` lines
  8, 22, 58, 67, 104 (`expected/out-txt-agent-run.txt` 9, 23, 59, 68, 105), `cli-container/10:36`,
  `13:36`, `15:3`, `recorded-embeddings/01:145`, `02:156`, `07:21`. Also never show the credit lines
  `semantic_splitter.py:102-105` or the Gutenberg producers' names inside `recorded-embeddings/05`
  (trim to the ids and the first document's opening). Public-domain authors' names appear only if a
  quoted metadata dict cannot be trimmed; prefer `07` lines 11, 13, 22 (an organisation and a book
  with no author).
- No hand-typed output: every terminal line comes from `assets/terminal/`; `recorded` panels say the
  vectors are the staff's (`68e0bde`); the stand-in query says it is a stored chunk's vector;
  `expected/` README descriptions are text, never styled as a terminal; "what to look for" is a
  caption citing `cli.py` lines.
- No command spelled differently from the README. Commands the README implies but doesn't print (the
  clone) are said as such.
- No credentials, keys or real-looking project ids: `your-project-id` only; never draw the key's
  content. The course's project id `ac215-project` appears only inside the diff line the viewer must
  edit (`laptop/06:10`), never in captions, labels or narration.

Lecture-specific:
- Never present a Google call as if it succeeded: no output panel for a working `--embed`, `--query`,
  `--chat` or semantic run; no invented `Embedding values:`, `Results:`, `INPUT_PROMPT:` or `LLM
  Response:`; no invented answer text. V7's answer is a shape, not words.
- Never present `out.txt` as the output of an L05 command: it is the staff's L06 `--agent` run from
  2026-09-22, against an older book; show only line 65 (the tool name) and line 74 (the stale chunk).
- Never present `docker compose run --rm llm-rag-cli` as a way to start: it is the G5 demo, labelled
  "the wrong way".
- Never show the capture's plumbing: the Docker-in-Docker laptop, `proxy_relay.py`, `mirror.gcr.io`,
  the CA variables, the rebuilt base image (`[1/6] FROM …@sha256:60c8fd1…`), `https://deb.debian.org`
  apt lines from the `.plain.txt` log, the `docker exec` that typed `cli-container/` commands, or the
  `git ls-tree … git show` copy command of `recorded-embeddings/00` (the copy is a card, not a typed
  command).
- Never state prices as verified, and never claim a step was billed.
- Never draw the HNSW graph, the 3-D embedding space or the clusters as measurements: they carry
  "our illustration".

## Left for exercises.md (not in the video)

Bigger chunks (`chunk_size = 700`, `chunk_overlap = 100` → 13 for Tolminc) and the need to re-embed and
re-load; the missing `semantic-split-collection` (`NotFoundError`); "Could not connect to a Chroma
server" from the laptop and the `CHROMADB_HOST` fix; the system instruction with an off-topic question
("What is the capital of France?"); cosine vs L2 on non-unit vectors; `EMBEDDING_DIMENSION = 768`
without re-embedding, and `query_texts`; what is still running after `exit`, and what `down` keeps; why
`out.txt` found "transhumance"; a `.dockerignore` for this repo; pinning Chroma; RRF by hand for a
fourth paragraph; the personality game with Euclidean distance.
