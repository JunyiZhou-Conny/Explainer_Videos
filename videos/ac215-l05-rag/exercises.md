# Exercises · AC215 L5 — Introduction to RAG: chunk, embed, load, query, chat

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real captures from
2026-10-16 (`assets/terminal/`), or were checked the same day in throwaway containers of the
tutorial's own image (Python 3.12.15, uv 0.13.1, chromadb 1.1.0, google-genai 1.39.1,
langchain-text-splitters 0.3.11) against the same Chroma server image, loaded with the staff's
recorded vectors (`68e0bde`). [`assets/exercise-checks/README.md`](assets/exercise-checks/README.md)
lists every command; a file name ending in `.log` or `.diff` below is one of its
[`logs/`](assets/exercise-checks/logs/), and `laptop/…`, `cli-container/…`, `recorded-embeddings/…`
name captures in `assets/terminal/`. There was **no Google key**: items marked *with your key*
need one, and their answers say exactly what was checked without it. Container IDs, collection
UUIDs and the order of the books will differ on your laptop.

---

## Part A · The five questions from the end of the video

**Q1. Which `cli.py` flags belong to each lane, and what must both lanes share?**

<details><summary>Answer</summary>

- **Indexing lane** (the README's "Step 1: Chunk -> Embed -> Load", `README.md:5`): `--chunk`
  (`cli.py:164-227`), `--embed` (`:230-264`) and `--load` (`:267-306`). It runs once, offline, and
  is slow; you run it again only when the books or the chunking change.
- **Query lane** ("Step 2: Query -> Embed -> Retrieve -> LLM -> Generate Answer", `README.md:9`):
  `--query` (`:309-361`) and `--chat` (`:364-399`). It runs for every question.

Both lanes must use **the same embedding model with the same settings**: `EMBEDDING_MODEL =
"gemini-embedding-001"` and `EMBEDDING_DIMENSION = 256` (`cli.py:25-26`). The chunks go through
`generate_text_embeddings` (`:87-121`), the question through `generate_query_embedding` (`:75-84`),
and both ask that model for 256 numbers. Only then do question and chunks live in the same space,
so "nearby" means "similar in meaning". Chroma checks only the size: a vector of another length is
refused outright (C5), but a 256-number vector from a different model would be accepted and
compared, with meaningless results.

Both lanes also meet in the same collection: `--chunk_type` names it, `f"{method}-collection"`, at
both ends (`:277`, `:316`, `:370`). Query the char-split collection with `--chunk_type char-split`.
One exception to "chunking needs no key": `--chunk_type semantic-split` already calls the model while
chunking (S14, B7).
</details>

**Q2. Why does the CLI reach the database at `llm-rag-chromadb:8000`, and who uses the published
port 8000?**

<details><summary>Answer</summary>

Compose puts both containers on one user-defined network, `llm-rag-network`
(`docker-compose.yml:1-3`; `Network llm-rag-network Created` in `laptop/07`). On such a network,
Docker's DNS answers container names: inside the CLI container, `getent hosts llm-rag-chromadb`
printed `172.19.0.2` (`cli-container/04`), and `cli.py:30-31` hard-codes that name and port. Port
8000 is the port Chroma listens on **inside its own container**; another container on the network
talks to it directly, without any publishing.

`ports: - 8000:8000` (`docker-compose.yml:21-22`, shown as `0.0.0.0:8000->8000/tcp` in
`laptop/08`) opens a door on your **laptop**. It's for programs that aren't on the network:
- you, with `curl http://localhost:8000/api/v2/heartbeat` (`laptop/10`);
- your browser, running the course's Chroma UI page, which reads your local database through
  localhost port 8000. Chroma's CORS setting (`docker-compose.yml:25-26`) lets that site in:
  with `Origin: https://ac215-llm-rag.dlops.io` the answer carries
  `access-control-allow-origin: https://ac215-llm-rag.dlops.io` (`laptop/12`), with another origin
  it doesn't (`laptop/12b`).

The CLI never uses the published door. If you changed it to `8001:8000`, the CLI would keep
working; only you and the browser would need the new number (C3).
</details>

**Q3. What does `chunk_overlap` buy and cost, and why did recursive-split make 14,228 chunks?**

<details><summary>Answer</summary>

**It buys** insurance against cutting an idea in half. Char-split's windows overlap by 20
characters (`cli.py:185-186`): chunk 0 of the story ends `…things she intended to ac`, and chunk 1
backs up 20 characters, `s she intended to accomplish during her` (`cli-container/12`), so
"accomplish" is whole in at least one chunk, and its vector sees the word.

**It costs** repetition. Every repeated character is embedded (your project pays for the text it
sends), stored, and can be retrieved twice, so near-duplicates take places in the top 10 and space in
the prompt. More overlap also means more chunks and more embedding calls.

**Why 14,228.** `cli.py:199-200` gives `RecursiveCharacterTextSplitter` only `chunk_size=350`. Its
library default is `chunk_overlap=200` (checked: `RecursiveCharacterTextSplitter()._chunk_overlap`
is `200`), so up to 200 characters of each chunk repeat the end of the previous one: chunk 1 of the
story starts again with `## Chapter One: The First Slice` (`cli-container/15`). The README says
"overlapping" (`README.md:17`, `:93`), not how much. And because the splitter cuts only at a blank
line, a line break or a space (in that order), every chunk ends before 350 characters: median 297,
longest 349, where char-split's are 350 (`q3-chunk-lengths.log`). Our counts with the same splitter
(`b1-b2-chunk-counts.log`):

| recursive-split, chunk size 350 | chunks (all books) | the story |
| --- | --- | --- |
| `chunk_overlap=0` | 10,542 | 28 |
| `chunk_overlap=20` (as char-split) | 10,551 | 28 |
| default (200), as in `cli.py` | **14,228** | **35** |

So of the 5,980 chunks it makes beyond char-split's 8,248, about 2,300 come from the shorter,
boundary-cut chunks and about 3,700 from the hidden overlap. To choose another value, pass
`chunk_overlap=` yourself (B2).
</details>

**Q4. Why did the README's `--query` return no Tolminc text?**

<details><summary>Answer</summary>

Only variant 4 of the query runs (`cli.py:352-359`); variants 1 to 3 are commented out
(`:325-350`), although the README promises "various types of filters" (`README.md:186`). Variant 4
asks for 10 results with two filters: `where={"book": "The Complete Book of Cheese"}` and
`where_document={"$contains": "Italian"}` (case-sensitive). In the loaded char-split collection
(`recorded-embeddings/08`):

| chunks | count |
| --- | --- |
| all | 8,248 |
| from *The Complete Book of Cheese* | 1,355 |
| from that book, containing "Italian" (the query's two filters) | 64 |
| from that book, containing "Tolminc" | **0** |
| from any book, containing "Tolminc" | 3 |

Chroma applies the filters **first** and ranks only what survives, and top-K fills its 10 places
whenever 10 candidates are left, however far they are. With a stand-in query (the stored vector of
one story chunk, because the real question needs Google to become a vector), no filter returned 10
story chunks at cosine distances 0.0000 (the chunk itself) to 0.1627; with the code's filters, 10
chunks of *The Complete Book of Cheese* at 0.2833 to 0.3123 (`recorded-embeddings/09`). No Tolminc
chunk can survive these filters, whatever the question's vector is. The lecture draws metadata
filtering after ranking (A54–A55); done that way, it would have dropped all 10 story chunks and
returned nothing.

The fix: uncomment variant 1 (`cli.py:326-331`), which has no filter. Variant 4 still runs and prints
after it. The code is mounted, so no rebuild; it needs your key, like any query.
</details>

**Q5. What is the tutorial's prompt missing compared with the lecture's final prompt, and what is
the one-line fix?**

<details><summary>Answer</summary>

The lecture's final prompt has three parts: a system prompt (how to behave), the user's query, and
the retrieved context (A57–A59). `chat()` sends only the last two: `INPUT_PROMPT` is the question
followed by the 10 chunks joined by newlines (`cli.py:388-391`), and the call is
`generate_content(model=GENERATIVE_MODEL, contents=INPUT_PROMPT)` (`:394-396`). The system prompt
exists: `SYSTEM_INSTRUCTION` (`:40-58`) says to answer only from the chunks and to say so when they
don't contain enough. But `grep -n SYSTEM_INSTRUCTION cli.py` finds only line 40: it's never sent.

The fix is one argument in that call:

```python
    response = llm_client.models.generate_content(
        model=GENERATIVE_MODEL, contents=INPUT_PROMPT,
        config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)
    )
```

Checked without a key, by capturing the request just before it would leave: as committed, its body
holds only `contents`; with the fix it also carries `systemInstruction`, starting with "You are an
AI assistant specialized in cheese knowledge…" (`b6-system-instruction-request.log`). Last year's
`pipenv` branch did send it (`pipenv-branch/cli.py:62-64`). Without it, the README's "answers
grounded in your documents" (`README.md:21`) rests on the chunks alone.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Bigger chunks.** In your editor, set `chunk_size = 700` and `chunk_overlap = 100` on
`cli.py` lines 185–186. Predict the story's chunk count, then in the container run
`python cli.py --chunk --chunk_type char-split` and `wc -l outputs/chunks-char-split-*.jsonl`. What
else must you run before `--chat` uses the new chunks?

<details><summary>Answer</summary>

The first window takes 700 characters and each one after it adds 700 − 100 = 600 new ones:
1 + ⌈(7,808 − 700) / 600⌉ = 1 + ⌈11.8⌉ = **13** chunks for the story, and **4,537** in total, against
24 and 8,248 before (`b1-a-chunk-700-100.log`). With 350 and 330, the same formula gives every book's
count in the video's run (checked on all eleven).

The new chunk files overwrite the old ones (same names). But the collection doesn't change: the load
step reads the `embeddings-…` files (`cli.py:293-294`), which only the embed step writes. So run
`python cli.py --embed --chunk_type char-split` (with your key: 51 calls in batches of 100, instead of
89) and then `python cli.py --load --chunk_type char-split`. Run the load alone after re-chunking and
you reload the old 350-character chunks.

Each retrieved chunk now carries twice the context, so chat's 10 results put about 7,000 characters
into the prompt instead of 3,500, with fewer distinct passages per character. Undo: `git checkout
cli.py`, then chunk (and, if you embedded, embed and load) again.
</details>

**B2. Make the hidden overlap visible.** On `cli.py` line 200, change `chunk_size=chunk_size)` to
`chunk_size=chunk_size, chunk_overlap=20)` and run
`python cli.py --chunk --chunk_type recursive-split`, then
`wc -l outputs/chunks-recursive-split-*.jsonl`. Predict: back to 8,248, or somewhere between?

<details><summary>Answer</summary>

Between: **10,551** in total, **28** for the story (`b1-b2-chunk-counts.log`; with
`chunk_overlap=0`: 10,542 and 28). The overlap made about 3,700 of the 14,228. The remaining
difference from char-split is the cutting rule itself: the splitter only cuts at a blank line, a line
break or a space, so every chunk stops before 350 characters (median 297, Q3) and more of them are
needed. Undo with `git checkout cli.py` and chunk again.
</details>

**B3. Strip the Project Gutenberg header and license.** Ten of the eleven books start with a
Project Gutenberg header and end with its license, which are chunked like the rest (S06, S12). In
`chunk()`, right after `input_text = f.read()` (line 181), add, indented one level less (at the
`with` line's level):

```python
        start = input_text.find("*** START OF")
        if start != -1:
            input_text = input_text[input_text.index("\n", start) + 1:]
        end = input_text.find("*** END OF")
        if end != -1:
            input_text = input_text[:end]
```

Predict how many char-split chunks disappear, and what happens to the story. Run
`python cli.py --chunk --chunk_type char-split`, `wc -l outputs/chunks-char-split-*.jsonl` and
`grep -c "Project Gutenberg" outputs/chunks-char-split-*.jsonl`.

<details><summary>Answer</summary>

**7,656** chunks instead of 8,248: 592 fewer (7.2 %), all from the ten Gutenberg books; the story
keeps its **24** (it has no markers, so both `if`s leave it alone) (`b3-strip-gutenberg.log`). Two
chunks still mention Project Gutenberg: a closing line that one book places *before* its END marker
(*Hints on cheese-making…*) and a note at the start of *The Book of Cheese*. Markers do most of the
cleaning, not all of it: look at what you index. To use the cleaner chunks, embed (with your key:
81 calls instead of 89) and load again. Undo with `git checkout cli.py`.
</details>

**B4. The book that lost its author.** Fix `cli.py` line 178 to
`book_name = os.path.splitext(filename)[0]` and run `python cli.py --chunk --chunk_type char-split`
without deleting anything first. Predict the Woman's Institute book's new file name, and the
`Number of files to process:` that `python cli.py --embed --chunk_type char-split` will print.

<details><summary>Answer</summary>

`filename.split(".")[0]` cut `Womans Institute Library of Cookery. Volume 2_ Milk, Butter and Cheese
Eggs Vegetables.txt` at its first dot, so the book was stored as `Womans Institute Library of
Cookery`, which isn't a key of `book_mappings` (`cli.py:70`), and its chunks got no author or year
(`cli.py:135-138`; `recorded-embeddings/07`). `os.path.splitext` removes only the extension: the new
name matches the key (`b4-b-after-fix.log`).

The new file is `chunks-char-split-Womans Institute Library of Cookery. Volume 2_ Milk, Butter and
Cheese Eggs Vegetables.jsonl` (1,505 rows), **beside** the old one, and the embed step prints
`Number of files to process: 12` before it reaches Google. Embedding and loading now would put the
book into the collection twice: the record IDs start with a hash of the book's name
(`cli.py:127-130`), so old and new rows get different IDs (`53b50dfe8ba86654-…` and
`318f802bd1ab68d7-…`). Delete the old files first:
`rm outputs/*"Womans Institute Library of Cookery.jsonl"` removes the old chunk and embeddings files
of both chunk types, and nothing else (checked on file names). Then chunk both types again, and, with
your key, embed and load them. (Checked: the name, the key match, the two files and the 12. The load
with the new metadata needs new embeddings, so it wasn't run.)
</details>

**B5. Same IDs, different chunks.** After loading both collections, run
`python cli.py --get --chunk_type char-split` and `python cli.py --get --chunk_type recursive-split`
(`--get` is an extra, not in the README, and needs no key). Predict the ten IDs of the second run.

<details><summary>Answer</summary>

The same ten: `1021665fac86c5a5-0` … `1021665fac86c5a5-9` in both collections (`b5-c-get-*.log`). An
ID is 16 hex characters of the SHA-256 of the book's name plus the chunk's row number
(`cli.py:127-130`), and both chunkers number their rows from 0. The documents differ: char-split's
are 350 characters each; recursive-split's are 283 to 346 characters, cut between words.
Both lists begin with the Gutenberg header (B3). An ID names a row *within one collection*, not a
passage of the book: never compare IDs across chunk types.
</details>

**B6. Turn the system instruction on (with your key).** In `chat()`, change the question on line
372 to `"What is the capital of France?"` and run `python cli.py --chat --chunk_type char-split`.
Then add the fix from Q5 and run it again. Predict both answers.

<details><summary>Answer</summary>

Both runs retrieve 10 cheese chunks: the question has no cheese in it, but there's no distance
threshold, so the nearest 10 come back anyway (S11).
- **As committed**, the model gets "What is the capital of France?" and 10 unrelated chunks, with no
  instruction about them. Expect a plain answer from its own memory.
- **With the fix**, `SYSTEM_INSTRUCTION` says to use only the chunks, to say when they don't contain
  enough, and to "politely redirect the conversation back to cheese-related subjects"
  (`cli.py:41`, `:47`, `:54`). Expect a refusal or a redirect.

Not run here (no key). What was checked: that the fix sends `systemInstruction` and the committed
call doesn't (Q5). Each run costs one embedding call and one Gemini call. Undo with
`git checkout cli.py`.
</details>

**B7. Semantic chunking on one book (with your key).** On your laptop, in `~/AC215/llm-rag`, move
every book but the story aside:

```bash
mkdir books-aside
mv input-datasets/books/*.txt books-aside/
mv "books-aside/Tolminc Cheese.txt" input-datasets/books/
```

Then, in the container, run the README's `python cli.py --chunk --embed --load --chunk_type
semantic-split`. The story has 108 sentences (by the splitter's rule, `semantic_splitter.py:118`).
Predict the number of embedding calls the chunk phase makes, the `Number of chunks:` it prints, and
the number `python cli.py --chat --chunk_type semantic-split` prints after `Results:`.

<details><summary>Answer</summary>

- **Chunk phase: 3 calls.** Every sentence gets a window (itself and one neighbor on each side), and
  the 108 windows are embedded in batches of 50 (`semantic_splitter.py:206`): 50 + 50 + 8.
- **`Number of chunks: 7`.** The 108 windows give 107 gaps. The cut line is their 95th percentile
  (`semantic_splitter.py:92`, `:137-141`), and only gaps strictly above it are cut
  (`:239-243`): the 6 biggest of the 107, so 7 chunks. The count doesn't depend on the vectors'
  values, only on how many sentences there are (barring two gaps of exactly equal size).
- **Embed phase: 1 call** (semantic chunks go in batches of 15, `cli.py:248-250`), then the load
  inserts 7 records into `semantic-split-collection`.
- **Chat prints `7`**: it asks for 10 (`cli.py:380-383`), and Chroma returns what exists (checked
  with a 7-record collection, `b7-b-ten-of-seven.log`). Chat costs one more embedding call and one
  Gemini call.

So the story alone costs 4 embedding calls to index. Our count for all eleven books, with a stand-in
for the embedding function that counts calls instead of making them: 26,080 windows → **528** calls
to chunk, 1,318 chunks → **92** calls to embed (`b7-semantic-calls.log`; the video's "about 528" and
"about 90"). Put the books back afterwards: `mv books-aside/*.txt input-datasets/books/ && rmdir
books-aside`. The semantic collection keeps only the story until you run the command again on all
the books.
</details>

---

## Part C · Debugging

**C1. "Collection does not exist."** After the char-split and recursive-split steps, a classmate
runs `python cli.py --chat --chunk_type semantic-split`. The embedding values print, then the
traceback ends with `chromadb.errors.NotFoundError: Collection [semantic-split-collection] does not
exist`. Why, and what are the fixes?

<details><summary>Answer</summary>

Each chunk type has its own collection, `f"{method}-collection"` (`cli.py:277`, `:370`), and only the
load step creates one. Nothing ever loaded `semantic-split-collection`: the semantic command wasn't
run, or it failed before its load step (S14: without a working key it dies in the chunk phase, before
anything is saved). Chat embeds the question first (`:373`), so the classmate paid for that call
before `get_collection` (`:377`) failed. The same error, with no key needed:
`python cli.py --get --chunk_type semantic-split` (`c1-get-semantic-not-found.log`).

Fixes: use a chunk type you loaded (`--chunk_type char-split`), or build the semantic one (B7: one
book first). To see what exists, on the laptop:
`curl -s http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections`
lists the collections (the extra check of S09 and S10). Other ways to lose a collection: a deleted
`docker-volumes/` folder, or Chroma started from another copy of the repo (C4).
</details>

**C2. "Could not connect to a Chroma server."** To skip Docker, a student makes a Python 3.12 venv
on the laptop, installs the dependencies, `export`s `GCP_PROJECT`, and runs
`python cli.py --get --chunk_type char-split` in `~/AC215/llm-rag`. Chroma is up (`docker ps` shows
it). The last line is `ValueError: Could not connect to a Chroma server. Are you sure it is
running?`. What's wrong, and what would make it work?

<details><summary>Answer</summary>

Read the first exception of the chain, not the last: `httpx.ConnectError: [Errno -2] Name or
service not known` (`c2-a-outside-network.log`, run from a container that isn't on the Compose
network, as the laptop isn't). `CHROMADB_HOST = "llm-rag-chromadb"` (`cli.py:30`) is a name that
only Docker's DNS on `llm-rag-network` knows (Q2). Chroma is running; the name just doesn't exist on
the laptop. (Two earlier traps on the way there: without `GCP_PROJECT`, `cli.py:23` stops with
`KeyError: 'GCP_PROJECT'`; and the f-string at `cli.py:388-391` puts a backslash inside an
expression, which only Python 3.12 or newer accepts.)

The intended fix is to run it in the container, where the name resolves. To run it from the laptop,
use the published door: `localhost`, port 8000. Make the host configurable,
`CHROMADB_HOST = os.environ.get("CHROMADB_HOST", "llm-rag-chromadb")`, and `export
CHROMADB_HOST=localhost`. Checked from a container that shares Chroma's network namespace, so that
its `localhost:8000` is Chroma, as the published port makes it on a laptop: `--get` returned the ten
IDs (`c2-b-host-from-env.log`). Embedding calls would also need `GOOGLE_APPLICATION_CREDENTIALS`
pointing at the key's laptop path (`../secrets/llm-service-account.json`). A later course repo does
exactly this: `cheese-app-v2`'s `src/vector-db/cli.py` (line 32) reads `CHROMADB_HOST` from the
environment.
</details>

**C3. Port 8000 is taken, and then something stranger.** `sh docker-shell.sh` fails:
`Error response from daemon: failed to set up container networking: driver failed programming
external connectivity on endpoint llm-rag-chromadb (…): Bind for 0.0.0.0:8000 failed: port is
already allocated`. The student stops the other program and runs `sh docker-shell.sh` again. It
starts, but `docker ps` shows `llm-rag-chromadb` with an empty PORTS column, `curl
http://localhost:8000/api/v2/heartbeat` can't connect, and in the container every Chroma step says
`Could not connect to a Chroma server`. Explain both, and give the fix.

<details><summary>Answer</summary>

First error: another program already holds port 8000 on the laptop: another Chroma (a second
project, or a leftover `llm-rag-chromadb` started elsewhere), a dev server, anything. `docker ps`
shows a container that publishes 8000; otherwise look for a program listening on 8000.

Second: the failed start left a half-made `llm-rag-chromadb` behind, in state `Created`. The next
`sh docker-shell.sh` reuses it, and on Docker Engine 29.8.2 it starts **with no network at all**:
`docker port` prints nothing, `docker inspect` shows `networks: {}`, and the heartbeat fails
(`g6-b-retry-without-down.log`). From a container on the app's network, the name doesn't resolve
(`getent hosts` exits 2) and `chromadb.HttpClient` raises `Could not connect to a Chroma server`
(`g6-e-third-run-cli-view.log`). The check ran with check-only names and port 18766, so the logs say
`l05ex-rag-chromadb` and `18766` where yours say `llm-rag-chromadb` and `8000`
(`compose-renames.diff`); it reproduced all three times.

Fix: after freeing the port, run `docker compose down` in `~/AC215/llm-rag` (it removes the
half-made container and the network), then `sh docker-shell.sh`. Chroma then publishes the port and
joins the network: `8000/tcp -> 0.0.0.0:…`, `networks: llm-rag-network`, heartbeat OK
(`g6-c-down-then-start.log`). If you'd rather keep the other program, change the left side to
`8001:8000` (`docker-compose.yml:22`). The CLI doesn't care (Q2), but your `curl` and the course's
Chroma UI, which reads `localhost:8000` (S09), would need the new number.
</details>

**C4. "The container name is already in use", or silently someone else's database.** (a)
`sh docker-shell.sh` fails with `Conflict. The container name "/llm-rag-chromadb" is already in use
by container "…". You have to remove (or rename) that container to be able to reuse that name.` (b)
Another student has two copies of the repo, `~/AC215/llm-rag` and `~/Desktop/llm-rag`, and starts the
second one. No error at all, but `--query` now fails with `NotFoundError` (C1). Explain both.

<details><summary>Answer</summary>

`container_name: llm-rag-chromadb` (`docker-compose.yml:20`) is a fixed, machine-wide name. Compose
names a project after the folder that holds the compose file.

(a) A container with that name exists and belongs to a **different** project (a copy in a folder
with another name, or the `demo-podcast` branch's compose file in `llmrag/`), or to none (started by
hand with `docker run --name`). Compose refuses to take its name (`g7-a-name-in-use.log`). Fix:
`docker compose down` in the folder that started it, or `docker rm -f llm-rag-chromadb`; then
`sh docker-shell.sh` works (`g7-b-fix.log`).

(b) Both folders are called `llm-rag`, so both copies are **the same project**. Compose finds "its"
Chroma, sees that the settings differ (the bind-mount source is another folder), and recreates it:
`Container … Recreate` / `Recreated`, now mounting the **Desktop** copy's `docker-volumes/chromadb`
(`g7-c-copy-a-mounts.log`, `g7-d-copy-b-start.log`). That folder holds no collections, hence the
`NotFoundError`. Nothing is lost: the index is still in `~/AC215/llm-rag/docker-volumes/`. Run
`docker compose down`, then start from the copy you meant. Better: keep one copy.
</details>

**C5. The dimension trap.** A teammate "improves" retrieval: `EMBEDDING_DIMENSION = 768`
(`cli.py:26`), then `--chat` without re-embedding. When that fails, they replace `query_embeddings=`
with `query_texts=[query]` in the query call. What happens each time?

<details><summary>Answer</summary>

- **768 numbers:** the collection's dimension was fixed at 256 by its first insert
  (`recorded-embeddings/03`, `"dimension":256`). Chroma refuses the query:
  `chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 256, got
  768` (`c4-dimension-768.log`, a 768-number vector sent straight to the collection; with `cli.py`
  you'd first pay for the 768-number embedding of the question).
- **`query_texts`:** Chroma embeds the text **itself**, with the collection's own embedding function,
  which is Chroma's default (`'embedding_function': {'name': 'default'}`), a small local model that it
  downloads first (79 MB) and that makes 384 numbers. Refused again: `Collection expecting embedding
  with dimension of 256, got 384` (`c5-query-texts.log`). If the sizes had matched, the query would
  have run, and returned nonsense: a vector from another model, in another space (Q1).

Fix: change the model or the dimension only together with a full re-embed and re-load, so both lanes
use the same setting.
</details>

**C6. A package that disappears.** To try BM25 (S15), a student runs `uv add rank-bm25` in the
container; `python -c "import rank_bm25"` works. The next day, after `exit` and a new
`sh docker-shell.sh`, the same import says `ModuleNotFoundError: No module named 'rank_bm25'`,
although `pyproject.toml` lists it. Why, and what's the fix?

<details><summary>Answer</summary>

`uv add` did two things in two places (`c6-*.log`):
- it edited `pyproject.toml` and `uv.lock` in `/app`, which is your folder on the laptop, so those
  edits stayed (`git diff --stat` on the laptop: both files changed);
- it installed the package into `/.venv`, which lives in the container (`Dockerfile:18`, outside the
  mount), and `docker compose run --rm` deletes the container on exit.

The next `sh docker-shell.sh` starts a new container from the old image, built before the change,
and Compose builds only when the image is missing. Fix: rebuild the image, so `uv sync --frozen`
(`Dockerfile:45`) installs from the new lock: `docker compose build`, then `sh docker-shell.sh`.
Checked with a `docker build` of the same Dockerfile: `Installed 124 packages` (one more than the
original 123), and the import works in a new container. Commit `pyproject.toml` and `uv.lock`, so a
teammate's build gets the package too. The same applies after a `git pull` that changes them (S10).
</details>

**C7. `PermissionError` on a Linux laptop.** On a Linux machine whose user has uid 1001,
`python cli.py --chunk --chunk_type char-split` ends with `PermissionError: [Errno 13] Permission
denied: 'outputs'` (from `os.makedirs` at `cli.py:168`). On a Mac it works. Why, and what's the fix?

<details><summary>Answer</summary>

The container runs as user `app`, uid 1000 (`Dockerfile:31`, `:38`), and writes into your folder
through the bind mount. On Linux, the folder keeps your uid (1001) and mode `drwxr-xr-x`, so uid 1000
may not create `outputs/` in it (`c7-a-permission-denied.log`). Docker Desktop on a Mac or Windows
maps ownership for you, and on Linux it works when your uid is 1000, as in the recording
(`laptop/16`: the files are `student`'s).

Fix, on the laptop in `~/AC215/llm-rag`: `mkdir outputs && chmod a+w outputs`. Checked: chunking
then exits 0 and writes 11 files, owned by uid 1000 (`c7-b-after-chmod.log`). The reverse happens
with Chroma's folder: its container runs as root, so `docker-volumes/` is root's (`laptop/13`), and
deleting it on Linux needs `sudo rm -rf docker-volumes`.
</details>

---

## Part D · Think

**D1. Does the distance measure matter?** Suppose `load()` created the collection without
`metadata={"hnsw:space": "cosine"}` (`cli.py:287-288`). Would the 10 nearest chunks change? When
would they not?

<details><summary>Answer</summary>

Without it, Chroma uses its default space, `l2`: squared straight-line distance (checked: a
collection created without the setting reports `space: l2`). For vectors of length 1,
‖a − b‖² = 2 − 2·cos(a, b), so both measures rank identically. These vectors aren't length 1: the
256-number prefix of `gemini-embedding-001`'s output isn't normalized, and the 8,248 char-split
vectors have lengths from 0.342 to 0.405 (`d1-cosine-vs-l2.log`; the story's alone, 0.369 to 0.402,
`recorded-embeddings/06`). So length leaks into the ranking.

Checked with every stored vector as a query, by brute force: the top 10 by L2 equals the top 10 by
cosine, in the same order, for only 458 of the 8,248 queries (5.6 %), and as the same set for 2,650
(32 %). After scaling every vector to length 1, cosine and L2 agreed on all 165 sampled queries. Keep
`"hnsw:space": "cosine"`, or normalize every vector before you add or query it. The lecture's
measure table says the same: cosine ignores magnitude, which is what you want for text embeddings
(A45–A47; S08's ponder).
</details>

**D2. Why did the staff's run find "transhumance"?** Line 73 of the committed `out.txt` (the staff's
`--agent` run of September 22, 2026, `out.txt:34`) retrieved "…known as transhumance, shaped not just
the economic life…", but `grep -c transhumance "input-datasets/books/Tolminc Cheese.txt"` prints `0`.
Explain. Then decide which of these changes need chunk → embed → load again: (a) editing a book;
(b) a new `chunk_size`; (c) a new `GENERATIVE_MODEL`; (d) a new `EMBEDDING_MODEL` or
`EMBEDDING_DIMENSION`; (e) a new question on line 372.

<details><summary>Answer</summary>

The database answered from what had been loaded, not from today's files. The book before commit
`85bba32` (its parent `96d5fd7`, September 20) was a different text about Tolminc, with
`transhumance` on 3 lines; `85bba32` (September 22) replaced it with today's fictional story and
added `out.txt` in the same commit (`d2-stale-index-git.log`). The staff's collection still held
chunks of the old book when they made the run. The query side never reads `input-datasets/`.

(a) Yes: the index is a snapshot. (b) Yes: new chunks need new vectors and a new load (B1).
(c) No: the generative model only reads the prompt; the index doesn't change. (d) Yes, all of it:
the question would be embedded the new way while the stored vectors are the old ones (C5).
(e) No: a new question is just a new query against the same index. A habit worth keeping: note
which commit of the books an index was built from.
</details>

**D3. Write a `.dockerignore` for this repo.** The build context was 112 MB (`laptop/07`), mostly
`.git`, and the image keeps `/app/.git` and a copy of `chroma.sqlite3` (`laptop/14b`). What would
you put in it, what must stay out of it, and what changes?

<details><summary>Answer</summary>

```text
.git
outputs/
docker-volumes/
__pycache__/
```

(and `secrets/` as a guard, in case a key ever lands inside the repo). Don't exclude
`pyproject.toml` or `uv.lock` (`COPY … pyproject.toml uv.lock* ./`, `Dockerfile:42`, then
`uv sync --frozen`) or `docker-entrypoint.sh` (the image's `ENTRYPOINT`, `Dockerfile:51`).

Checked on a copy that also held a full `outputs/` (the 82 MB of embeddings files) and a loaded
`docker-volumes/` (`d3-*.log`):

| | without | with the four lines |
| --- | --- | --- |
| build context sent | 257.74 MB | 4.58 MB |
| `/app` in the image | 247 MB (`.git` 103 MB, `outputs` 82 MB, `docker-volumes` 58 MB) | 4.5 MB |
| image | 2.31 GB (597 MB content) | 1.89 GB (429 MB content) |

At run time nothing changes: the bind mount puts your whole folder over `/app` anyway, which is why
the problem is easy to miss. What changes is every build (a few MB to send instead of hundreds, and
the last layer no longer changes whenever the database or `outputs/` change) and every push:
anything copied into a layer, data or a key, ships with the image (L02, L04).
</details>

**D4. A clean slate?** A teammate says `docker compose down -v` wipes the database. After it, what
is still on your laptop, and how would you really start the index from scratch? Do you ever need
to?

<details><summary>Answer</summary>

`down -v` removes the containers, the network, and **volumes**: named volumes declared in the compose
file and anonymous ones. This compose file declares none; Chroma's data is a **bind mount** of your
folder. Checked: after `down -v`, `docker-volumes/chromadb/chroma.sqlite3` is still there and
`docker volume ls` is empty (`d4-down-v.log`). Also still there: the images (`llm-rag-cli` 2.11 GB,
`chromadb/chroma:latest` 826 MB, the Python base, `laptop/26`), `outputs/`, the key in `../secrets`
and, in Google Cloud, the service account and its key.

To start the index from scratch: `docker compose down`, then delete the folder (on Linux
`sudo rm -rf docker-volumes`, because it's root's). You rarely need to: every load step deletes its
collection and creates it again (`cli.py:280-289`; `cli-container/32`: `Deleted existing collection
'char-split-collection'`). Deleting the folder matters only for collections you no longer load, or a
database that won't open.
</details>

**D5. Pin the database server.** `docker-compose.yml:19` says `chromadb/chroma:latest`. What did
`latest` mean on the day of the recording, why is that a problem for a team, and what would you write
instead?

<details><summary>Answer</summary>

On 2026-10-16 Docker Hub listed `latest` and `1.5.9` with the same digest, `sha256:1e0b73a1…`, an
image created on May 5, 2026 (`d4-chroma-tags.log`; it's the image the recording pulled,
`laptop/11b`). Inside it, `chroma --version` says `chroma 1.4.4` and the API version is `"1.0.0"`
(`laptop/11`, `11b`), and the client library is `chromadb 1.1.0`, pinned by `uv.lock`. It worked.
But `latest` is whatever was
newest when *each* student first pulled it, and a later `docker pull` (or a new laptop) silently
changes the server under a client that stays the same.

Write a tag, `image: chromadb/chroma:1.5.9` (the server this video ran), or the digest itself,
`chromadb/chroma@sha256:1e0b73a1…`, which can never move. Upgrade on purpose: the server tag and the
client in `uv.lock` together, then load again and test. (A `1.1.0` server tag also exists, matching
the client's version; it wasn't tested here.)
</details>

**D6. Fuse a fourth paragraph.** The lecture's hybrid-search example (B44–B48) ranks three paragraphs
by BM25 and by vectors and fuses them with RRF, each list giving w / (k + rank), with k = 0 and
w = 0.5: 0.75, 0.67, 0.42. Add a fourth paragraph that both retrievers rank **2nd**, pushing the
others down. Compute the fused order with k = 0, then with k = 60 (a common default).

<details><summary>Answer</summary>

New ranks (BM25, vectors): paragraph 1 (3, 1), paragraph 2 (1, 4), paragraph 3 (4, 3), paragraph 4
(2, 2).

| paragraph | k = 0 | k = 60 |
| --- | --- | --- |
| 1 · riverbank early | 0.5/3 + 0.5/1 = **0.667** | 0.016133 |
| 2 · bank, borrow money | 0.5/1 + 0.5/4 = 0.625 | 0.016009 |
| 3 · swimming, riverbank | 0.5/4 + 0.5/3 = 0.292 | 0.015749 |
| 4 · new, 2nd in both | 0.5/2 + 0.5/2 = 0.500 | **0.016129** |

k = 0: 1, 2, 4, 3. k = 60: 1, 4, 2, 3 (`d5-d6-by-hand.log`). With k = 0 a single first place
(1/1 = 1) outweighs two second places; a larger k flattens the differences between ranks, so being
good in both lists beats being best in one. The weights and k are choices you tune, not facts
(B46). The tutorial has no keyword retriever and no fusion: `$contains` only filters (S12, S15).
</details>

**D7. The personality game with a ruler.** In the lecture's game (A40–A47), cosine similarity picks
the first candidate (0.987 recomputed; the slide shows 0.986), and the dot product would pick the
second (81.24 against 80.15, S08). Who wins with Euclidean distance, and what does that say about
choosing a measure for text?

<details><summary>Answer</summary>

Euclidean distance from the instructor's five scores: first candidate **1.673**, second 2.093,
third 4.498 (`d5-d6-by-hand.log`). The first candidate wins, as with cosine. Euclidean distance
squares each trait's difference before adding them up, so one big gap counts a lot: the second
candidate's emotional stability (2.7 against 4.5) costs more than the first candidate's biggest gap,
extroversion (3.3 against 4.8). The dot product instead rewards the second candidate's bigger numbers
(a longer arrow, 8.85 against 8.63).

Three measures, two different winners: the measure is a modeling choice. For personality scores,
the size of each number means something, so Euclidean distance is a fair choice. For text
embeddings, meaning lives in the direction; the tutorial's vectors vary in length (0.34 to 0.41),
and nothing in the task wants that to count, so you compare directions: cosine (D1).
</details>
