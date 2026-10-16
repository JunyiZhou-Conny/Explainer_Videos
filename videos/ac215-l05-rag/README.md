# AC215 · Lecture 5 — Introduction to RAG: chunk, embed, load, query, chat

A follow-along walkthrough of the Lecture 5 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**: [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag), branch `main` @
[`e17a39f`](https://github.com/dlops-io/llm-rag/tree/e17a39f35bc07b440f573def480adaf4703f8b91), the
whole README: *What you'll build*, *Prerequisites*, *Setup GCP Service Account*, *Run LLM RAG
Container*, *Chunk Documents*, *Generate Embeddings*, *Load Embeddings into Vector Database*, *Query
the Vector Database*, *Chat with LLM* and *Advanced RAG: Semantic Chunking (Semantic Splitting)*. A
retrieval-augmented generation (RAG) system over eleven cheese books: a CLI container cuts the books
into chunks, Vertex AI's `gemini-embedding-001` turns each chunk into 256 numbers, a Chroma vector
database in a second container stores them, and each question is embedded the same way, matched
against the chunks and handed to `gemini-3.1-flash-lite` with the nearest ten. The README's last
section, *Agents*, is Lecture 6's tutorial: one command is previewed at the end.

A few panels quote other commits of the same repo for comparison, not followed:
[`68e0bde`](https://github.com/dlops-io/llm-rag/tree/68e0bdecba017b506c7646d710b1fbf1bc6b31fc) (the
staff's committed `outputs/`, whose recorded vectors the video loads for real),
[`96d5fd7`](https://github.com/dlops-io/llm-rag/tree/96d5fd78d24607e20ae84d5339ed62abaadff17d) (the
older Tolminc book, replaced on September 22, 2026) and the `pipenv` branch @
[`0b671ed`](https://github.com/dlops-io/llm-rag/tree/0b671ede29d4b37ecd530da493485b015adad4da) (last
year's `cli.py`, which still sent the system instruction).

Watch it with the README open and your own clone, `~/AC215/llm-rag` beside `~/AC215/secrets`, and
Docker with Compose from the earlier lectures. The steps that call Google (embed, query, chat,
semantic chunking) also need a Google Cloud project with billing, a service-account key and the
Vertex AI API switched on. The tracker top left shows the README step; pause at every `▶ your turn`
to run the command; a gray `extra` tag marks a check that isn't in the README, and a gray "Lecture 5 ·
slides …" tag top right points to the lecture slides the scene stands on. The video was recorded on
Linux (Docker Engine 29.8.2, Compose v5.6.0) **without a Google key**: Docker, chunking and the
database ran for real, the embeddings are the staff's recorded vectors, and wherever the code calls
Google, it shows the command, the real error a missing key gives, and what to look for with your
key. Series format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every
command:
[MLOps_Learning · guides/L05-rag.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L05-rag.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l05-rag.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l05-rag.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l05-rag_part1.mp4` | part 1, DURATION_P1: build the index — chunk, embed, load (S01–S09). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l05-rag_part2.mp4` | part 2, DURATION_P2: ask the index — query, filters, chat, semantic chunking (S10–S16). Not in Git: rebuilt with `--no-render` |
| `output/ac215-l05-rag.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l05-rag.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l05-rag.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks (bigger chunks, the hidden overlap, stripping the Gutenberg license, the book that lost its author, the same IDs in two collections, the system instruction switched on, semantic chunking on one book), debugging and think questions, with answers |
| `assets/exercise-checks/` | what was run to check `exercises.md`, in throwaway containers of the tutorial's own image, with every log |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the instructor's slides (the main deck and the "Advanced RAG" supplement) in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (a fresh Docker Engine 29.8.2 standing in for the laptop, 2026-10-16, no Google key; the load steps and the database checks on the staff's recorded vectors from `68e0bde`); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at the pinned commit (and a few files from `96d5fd7` and the `pipenv` branch) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: how many chunks a
7,808-character story makes with windows of 350 characters that overlap by 20, why recursive
splitting makes 14,228 chunks from the same chunk size, whether vectors shorter than 1 change which
chunks count as nearest under cosine, what ten results are about when the question is about Tolminc
but the filters keep one other book and the word "Italian", and whether semantic chunking can run
its chunk step without a key. Five test-yourself questions close the video (answers in
`exercises.md`).

**Part 1 · build the index — chunk, embed, load**

1. **A model that never read the book** — the tutorial's question, "How is Tolminc cheese made?",
   and a knowledge base of eleven books: ten old cheese books from Project Gutenberg and the
   instructor's fictional short story; the lecture's four weaknesses of a plain LLM, two of which RAG
   goes after; three roads (paste every book into the prompt, fine-tune, or hand the model the most
   relevant pages: an open-book exam); the lecture's four questions (embedding, vector database,
   query, context); how to follow along, and what a recording without a Google key shows.
2. **Two lanes, one database** — RAG in five boxes, where the database never talks to the model; the
   two lanes: books → chunks → embedding model → vectors → database once, offline; question → the
   same model → query vector → nearest chunks → prompt → LLM for every question; the lecture's three
   phases (indexing, retrieval, augmentation and generation); one `cli.py` flag per box; why both
   lanes must use the same embedding model; where each box runs (the chunker in your container, both
   models at Google, paid per use, the database in a second container with its files on your
   laptop).
3. **Your key, your folders, your project** — the Docker check (`docker compose`, with a space); the
   clone the README links but doesn't print, and a `secrets/` folder beside it, under the exact name
   `llm-rag`; the service account `llm-service-account`, its two roles and its JSON key, renamed into
   `secrets/`; a key that spends your project's money, and a `.gitignore` with no `secrets` line;
   lecture 4's three gates; two small slips (Storage Admin is never used, and the Vertex AI API must be
   switched on); `cd llm-rag`, the commit the video was recorded on, and your Project ID (not the
   name) on line 7 of `docker-shell.sh`.
4. **One script, two containers** — lectures 3 and 4 at once: `docker-shell.sh` exports three values
   and calls `docker compose run --rm`; `docker-compose.yml` as a picture: the network by name, the
   CLI service built from the folder if missing, two mounts (`/app`, `/secrets`), two environment
   slots, Chroma from Docker Hub under a fixed name with port 8000 published, its data in
   `docker-volumes/`, and the course's web tools let in; the venv outside `/app`, so editing `cli.py`
   needs no rebuild; `sh docker-shell.sh`: a "not found" that is harmless, an 81-second build whose
   112 MB context is mostly git history, kept in the image for lack of a `.dockerignore`; the banner
   (Python 3.12.15, uv 0.13.1) that says "activated" before it activates; the container's prompt and
   ID.
5. **Names, mounts, and two traps** — from a second terminal: `docker ps` (the CLI container isn't
   called `llm-rag-cli`), `docker inspect` and the three mounts; the Project ID and the key's path
   inside the container; the CLI reaching Chroma by name, and your laptop through `localhost:8000`;
   Chroma's data folder, created by Docker and owned by root; trap one, typing the compose command
   yourself (blank variables, and even chunking dies at startup); trap two, a clone with another name
   (an empty, root-owned folder mounted over your code); the `latest` tag and three version numbers
   that don't match: pin a tag.
6. **Cutting the books: a ruler** — why chunk (one vector per book averages its topics; a chunk is
   what you retrieve and paste); the README's chunk visualizer; char-split as a ruler of 350
   characters that overlap by 20, counting characters, not words; 24 chunks for the story,
   8,248 in all, no key needed; the seam where a word is cut and made whole again, against the
   lecture's chunks that sit end to end; chunk files in `outputs/` on your laptop, git-ignored; the
   Gutenberg header and license, chunked like the rest.
7. **Recursive split and its hidden overlap** — only a chunk size; scissors that look for a blank
   line, then a line break, then a space; 35 chunks for the story, 14,228 in all; the library's
   default overlap of up to 200 characters that the README never mentions, and shorter chunks;
   overlap as insurance that is embedded, stored and paid for; the lecture's point: chunks should
   follow the document's structure.
8. **Meaning as direction: embeddings** — one vector per chunk, similar meanings in similar
   directions; the lecture's personality game: cosine compares angles and picks the first candidate,
   the dot product counts length and would pick the second; `gemini-embedding-001`'s 3,072 numbers,
   of which the code keeps the first 256; batches of 100 and five retries; the same model for the
   questions later; the embed steps (the first paid call; the real no-key error; what to look for,
   and what each failure means, with your key; about 89 and 148 calls); the staff's committed
   vectors, made from chunk files identical to ours; vectors of length 0.369 to 0.402, and why cosine
   doesn't mind.
9. **Load: records, an index, a folder on your disk** — what a vector database adds to an ordinary
   one; a record (ID, text, metadata, vector) and an ID that hashes the book's name and the row; one
   collection per chunk type, deleted and rebuilt by every load, with cosine as its measure; the
   index (HNSW, a layered graph); the load steps: 0 files before any embeddings, then 8,248 and
   14,228 records from the staff's vectors; dimension 256, fixed by the first insert; a book that
   lost its author and year to a file name cut at its first dot; a 60 MB database file and two index
   folders on your laptop; the course's Chroma UI, reading your database through port 8000.

**Part 2 · ask the index — query, filters, chat, semantic chunking**

10. **Exit, and the index survives** — `exit` removes the CLI container but leaves Chroma running and
    port 8000 taken; `docker compose down` and its two harmless warnings; the database stays on your
    disk; a new `sh docker-shell.sh` with no pull and no build (`docker compose build` after a
    `git pull` that changes the dependencies); both collections back, and an extra `--get` that
    returns the same ten IDs: the data never lived in the container.
11. **Asking the database: rank and cut** — the question becomes a query vector through the same
    model; the lecture's scores, sorted and cut at top K (10 here); similarity in the lecture,
    cosine distance in Chroma (one minus the similarity: smaller is closer); no distance threshold;
    the query steps: a `load()` label copied from the load code, then the stop at the key while
    embedding the question, before any search; with your key, results as lists of lists, which is
    why chat reads item zero.
12. **Filters come first** — the code's query: 10 results, one book and the word "Italian"; 8,248
    chunks → 1,355 → 64, none about Tolminc; a stand-in search with a stored story chunk's vector:
    10 story chunks without filters, 10 from *The Complete Book of Cheese* with them; Chroma filters
    before ranking, where the lecture filters after; only one of four query variants runs; `$contains`
    filters, it doesn't rank; the extra `--get` and the Gutenberg header in the first records.
13. **Chat: the prompt is the whole trick** — the lecture's final prompt (system prompt, query,
    context); chat's prompt: the question and ten unfiltered chunks, sent to Gemini 3.1 Flash Lite;
    the system instruction defined on line 40 and never sent, and its one-line fix; the model's
    weights unchanged: delete the collection and the knowledge is gone; the chat steps (one
    embedding call and one Gemini call per question; what to look for with your key); the opening
    question answered: details of the fictional story can only come from your chunks; the course's
    chat tool, and your own question on line 372.
14. **Semantic chunking: cut where meaning shifts** — the lecture's walk with a 0.8 threshold; the
    code's rule: every sentence's window embedded, the distance between neighbors drawn like a
    seismograph, cuts at the gaps above the 95th percentile; why the chunk step itself needs the key;
    the README's three-step command, failing on the first book here; about 528 embedding calls to
    chunk and about 90 to embed, 10 to 20 minutes: try one book first; very uneven chunks.
15. **Beyond naïve RAG: what the lecture adds** — pre-retrieval and post-retrieval stages; semantic
    chunking as the one advanced lever the tutorial implements; query rewriting (and how it can
    invent details); hybrid search with keywords and vectors, and reciprocal rank fusion on the
    lecture's example (0.75, 0.67, 0.42); re-ranking with a slower model that reads question and
    chunk together; none of it in `cli.py`.
16. **Tear down, a stale index, recap** — `exit`, `docker compose down`, the images that remain
    (2.11 GB and 826 MB), `git status` with only your edit; nothing running in Google Cloud, and the
    key kept beside the repo and deleted when the course ends; the stale index: the staff's recorded
    agent run retrieved text from an older Tolminc book, so rebuild the index when the books change;
    a preview of lecture 6's agent, which chose its own retrieval tool, and the lecture's Self-RAG;
    the four questions answered; five test-yourself questions.

The README's small mistakes are pointed out kindly, with the fix: it links the repo but prints no
clone command; it asks for a Storage Admin role nothing uses, and never says to switch on the Vertex
AI API (without it, the first embedding call fails with `SERVICE_DISABLED` after five retries);
there is no `.dockerignore`, so the image carries 103 MB of git history with an old copy of the
staff's database (add one: exercises D3); the banner says "activated" before it activates (cosmetic);
`container_name: llm-rag-cli` isn't used by `docker compose run` (find the name with `docker ps`);
the clone must be named `llm-rag`, or Docker mounts an empty, root-owned folder over your code;
`chromadb/chroma:latest` is unpinned (pin a tag); the Gutenberg header and license are chunked,
embedded and retrieved like the text (strip them); "overlapping" doesn't say that recursive-split
uses the library's default of up to 200 characters (set `chunk_overlap`); one book loses its author
and year to `filename.split(".")[0]` (use `os.path.splitext`, delete its old files, chunk, embed
and load again); `--query` prints `load()`; the README promises "various types of filters", but
only variant 4 runs, and its filters exclude every Tolminc chunk (uncomment variant 1); the system
instruction is defined but never sent (pass it in a `config` argument, as the `pipenv` branch did);
chat's question has two question marks (harmless); and leaving isn't in the README: `exit` alone
leaves Chroma running and port 8000 taken (`docker compose down`). The staff's committed `out.txt`
answers from an older book than today's: an index is a snapshot.

## Rebuild

```bash
python -m explainer.build videos/ac215-l05-rag -q l                          # fast draft
python -m explainer.build videos/ac215-l05-rag --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l05-rag --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l05-rag --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l05-rag --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders.

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); this video is made for study
with the instructor's permission. The lecture's slides are redrawn in our own pictures, never shown.
The Google Cloud console and the course's web tools (the chunk visualizer, the Chroma UI and the
chat tool) are schematic drawings (tagged `illustration`), not screenshots; no Google account or key
was used or shown.*
