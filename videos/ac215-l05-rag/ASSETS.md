# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

Copied unchanged with `git show <commit>:<path>` (each file checked against its git blob hash), at
the repo's own relative paths, so that a code panel's `path · lines a–b` matches a viewer's clone.
[dlops-io/llm-rag](https://github.com/dlops-io/llm-rag), branch **`main`**, commit
`e17a39f35bc07b440f573def480adaf4703f8b91` (2026-10-07, "Merge pull request #2 from
obalatel/revert-1-demo-podcast"; still the head of `main` on 2026-10-16, `terminal/laptop/05-x-ls.txt`):

- `README.md` (the whole tutorial: intro and What you'll build `:1-23`, Prerequisites `:45-48`,
  Setup GCP Service Account `:52-69`, Run LLM RAG Container `:75-85`, Chunk Documents `:91-116`,
  Generate Embeddings `:122-138`, Load Embeddings `:144-165`, Query `:171-186`, Chat `:192-214`,
  Semantic Chunking `:220-236`; Agents `:242-271` belongs to L06);
- `Dockerfile`, `docker-compose.yml`, `docker-shell.sh` and `docker-entrypoint.sh` (both mode 755,
  as committed), `pyproject.toml`, `uv.lock`, `.gitignore`;
- `cli.py` (the whole pipeline), `semantic_splitter.py`, `agent_tools.py` (L06, for the preview);
- `out.txt` (the staff's committed `--agent` run, see `expected/`);
- `input-datasets/books/Tolminc Cheese.txt` (the instructor's short story, 7,808 characters; the
  chunking scenes quote it). The ten Project Gutenberg books are not copied (2.7 MB; their file
  names and chunk counts are in the captures).

Older versions, for the "what changed" and "stale index" beats:

- `source/pipenv-branch/`: branch `pipenv`, commit `0b671ede29d4b37ecd530da493485b015adad4da`
  (2025-03-04, last year's version): `cli.py` (applies `SYSTEM_INSTRUCTION` through
  `GenerativeModel(..., system_instruction=...)`, lines 62-64, which this year's code no longer does,
  digest E1), `docker-compose.yml` (Chroma 0.x, mount `/chroma/chroma`), `docker-shell.sh` (still
  runs `docker network create` and `docker build` itself).
- `source/tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt`: the Tolminc book as it
  was at `96d5fd78d24607e20ae84d5339ed62abaadff17d` (2026-09-20), the parent of `85bba32`
  (2026-09-22), which replaced it with today's fictional story. `out.txt` retrieved text from this
  older version ("transhumance", "PDO regulations", "Soča Valley": 3, 2 and 6 matching lines here,
  0 in today's book; digest E7, Exercise 8).

Not copied: `images/llm-rag-flow-{1,2,3}.png` (the README's diagrams; scenes redraw the two
pipelines). Course material by the AC215 teaching staff (Harvard IACS), used for study with the
instructor's permission.

## `terminal/` — real terminal sessions

Captured on **2026-10-16, 00:52–00:57 UTC** by `terminal/capture.sh` (which starts a fresh "laptop")
and `terminal/run_steps.sh` (which types the README's commands one by one). The digest's pinned
commit is unchanged since its 2026-10-13 verification, so the captures and the digest describe the
same code. Each file starts with the command (`$ ...`; a multi-line command, such as a
`python - <<'EOF'` block, keeps its lines), then its output, then its exit status (`[exit N]`);
ANSI colour codes are removed. Every README command of the RAG part (README.md:45-236) is run in
README order, exactly as written. Files with `x-` in their name are **extras** (not README steps:
checks, gotcha demos); scenes mark them `extra`.

| folder | what |
| --- | --- |
| `laptop/` | your laptop's terminal: clone, the `docker-shell.sh` edit, `sh docker-shell.sh` (build, Chroma, banner), second-terminal checks, teardown and the restart test |
| `cli-container/` | typed at the `llm-rag-cli` container's prompt (`app@…:/app$`): every `python cli.py …` command of the README, plus checks |
| `recorded-embeddings/` | the README's two `--load` commands run for real on the **staff's own embeddings files** (committed in the repo's history), and what the loaded database then answers |
| `gotchas/` | extras: gotcha G5 (Compose without the script) and G1 (a clone not named `llm-rag`) |
| `expected/` | what the README documents for the steps that need Google Cloud (its "This will:" lists) and the staff's recorded `out.txt`; first line of each says where it comes from |
| `capture-only/` | not tutorial material: the base-image Dockerfile the capture needs and its build log, and per-folder timings (UTC time and duration of each step; for terminal sessions the seconds to exit) |
| `capture.sh`, `run_steps.sh`, `tty_session.py`, `proxy_relay.py` | the scripts that made all of the above (`tty_session.py` and `proxy_relay.py` are L04's helpers, copied unchanged) |

Chronological order (the folders interleave): `laptop/00-15`, `cli-container/00-16`,
`laptop/16`, `cli-container/20-31`, `laptop/17-18`, `cli-container/32-61`,
`recorded-embeddings/00-09`, exit, `laptop/20-24`, `cli-container/70`, `laptop/25-27`, then
`gotchas/` (same laptop).

### The machines and versions

- **Laptop:** a fresh, empty Docker Engine **29.8.2** (client and engine, API 1.56, linux/amd64),
  Docker Compose **v5.6.0**, buildx v0.37.2, git 2.54.0, curl 8.22.0 (`laptop/00-x-env.txt`); user
  `student` (uid 1000), workspace `~/AC215` holding `llm-rag/` and `secrets/` side by side, as the
  README's layout (README.md:64-69). There is **no service-account key** anywhere (no GCP account
  here): `~/AC215/secrets/` exists but is empty.
- **The `llm-rag-cli` image** (built by Compose from the tutorial's `Dockerfile`):
  `python:3.12-slim-bookworm` (Debian 12), **Python 3.12.15**, pip 26.2.1 (the `--upgrade pip`
  of `Dockerfile:29`), **uv 0.13.1** (from `pip install uv`, `Dockerfile:30`), apt installs 57 packages
  for `build-essential curl libpq5`; `uv sync --frozen` installs 123 packages into `/.venv` exactly as
  `uv.lock` pins them, among them chromadb 1.1.0, google-genai 1.39.1, google-auth 2.41.1,
  langchain 0.3.27, langchain-community 0.3.30, langchain-text-splitters 0.3.11, numpy 2.3.3,
  pandas 2.3.3, openai 1.109.1, openai-agents 0.3.2 (`cli-container/03-x-packages.txt`). Image size
  2.11 GB on disk, 537 MB content (`laptop/14-x-images.txt`).
- **The Chroma server:** `chromadb/chroma:latest`, digest `sha256:1e0b73a1…` (created
  2026-05-05T01:49:45Z), which Docker Hub's API still listed under both `latest` and `1.5.9` on
  2026-10-16 (same amd64 manifest). Inside, `chroma --version` prints **`chroma 1.4.4`** and
  `GET /api/v2/version` answers **`"1.0.0"`** (`laptop/11b-x-chroma-version.txt`,
  `laptop/11-x-version.txt`): none of the three numbers matches another. 826 MB on disk, 176 MB
  content. The image sets no `USER`, so the database files are owned by root.
- Versions move: narration says "at the time of recording" for Python 3.12.15, uv 0.13.1, the Chroma
  server and the Docker/Compose versions.

### `laptop/` — your laptop's terminal

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | date and versions |
| `01-x-docker-check.txt` | extra (Prerequisites "Have Docker installed", README.md:47) | `docker --version`, `docker compose version` |
| `02-clone.txt` | README.md:48 (the README links the repo; the clone command itself is not printed) | `git clone https://github.com/dlops-io/llm-rag.git` → `Cloning into 'llm-rag'...` |
| `03-x-mkdir-secrets.txt` | extra (layout README.md:64-69) | `mkdir secrets; ls` → `llm-rag  secrets` (terminal view) |
| `04-cd.txt` | README.md:79 ("inside the `llm-rag` folder") | `cd llm-rag` |
| `05-x-ls.txt` | extra | the repo's files; `e17a39f (HEAD -> main, origin/main, …)` = the pinned commit (terminal view, wrapped at 80 columns) |
| `05b-x-git-size.txt` | extra (G15) | **`.git` is 103 MB** (`size-pack: 102.45 MiB`): the history keeps the staff's 90.9 MB `chroma.sqlite3` and their `outputs/` from the reverted "Demo podcast" PR (`68e0bde`, removed in `58dd602`), so every clone downloads them |
| `06-x-edit-gcp-project.txt` | README.md:80 | `git diff docker-shell.sh`: line 7 `ac215-project` → the **placeholder** `your-project-id`, made by a capture-only `sed`; a student types their own Project ID in an editor |
| `07-docker-shell.txt` (+ `.plain.txt`) | README.md:83-85 | `sh docker-shell.sh` in a terminal (80×40): `[+] run 9/9`, `Image chromadb/chroma:latest Pulled 12.1s`, `Network llm-rag-network Created`, `Container llm-rag-chromadb Created`; then **`Image llm-rag-cli Pulling` / `failed to resolve reference "docker.io/library/llm-rag-cli:latest": … not found`** (Compose v5 first tries Docker Hub, then builds); `Image llm-rag-cli Building`, `[+] Building 81.5s (13/13) FINISHED` (`[2/6]` apt + pip + uv 20.2 s, `[5/6] RUN uv sync --frozen` 6.7 s, export 53.9 s; build context **112.26 MB**); `Container llm-rag-llm-rag-cli-run-90678535ddef Created`; the entrypoint banner (`Container is running!!!`, `Architecture: x86_64`, `Python version: Python 3.12.15`, `UV version: uv 0.13.1 …`, `Activating virtual environment...`) and the prompt `app@92c5bfd26089:/app$`; `exit` typed at the end of the session. `.plain.txt` = the full build log (596 lines) |
| `08-x-docker-ps.txt` | extra (digest step 3 check) | `llm-rag-chromadb` with `0.0.0.0:8000->8000/tcp`, and the CLI container named **`llm-rag-llm-rag-cli-run-<id>`**, not `llm-rag-cli`: the `container_name` of `docker-compose.yml:9` is not used by `docker compose run` (Compose v5.6.0 here) |
| `09-x-network-ls.txt` | extra | `llm-rag-network` (bridge), created by Compose (`docker-compose.yml:1-3`) |
| `10-x-heartbeat.txt` | extra (digest step 3) | `curl http://localhost:8000/api/v2/heartbeat` → `{"nanosecond heartbeat":…}` through the published port |
| `11-x-version.txt`, `11b-x-chroma-version.txt` | extra (E9) | `"1.0.0"`; `chroma 1.4.4`; the image digest and date (see above) |
| `12-x-cors-allowed.txt`, `12b-x-cors-other.txt` | extra (README.md:162-165, `docker-compose.yml:25-26`) | with `Origin: https://ac215-llm-rag.dlops.io` the answer carries `access-control-allow-origin: https://ac215-llm-rag.dlops.io`; with another origin it does not: why the course's Chroma UI page may read your local database |
| `13-x-docker-volumes.txt` | extra | right after start, `docker-volumes/chromadb/` already exists on the laptop with a 188 KB `chroma.sqlite3`, owned by **root** |
| `14-x-images.txt` | extra | `llm-rag-cli` 2.11 GB, `chromadb/chroma:latest` 826 MB, the base image |
| `14b-x-image-contents.txt` | extra (G15, E15) | inside the built image: `/app/.git` is 103 MB, `/.venv` 439 MB, and **`/app/docker-volumes/chromadb/chroma.sqlite3` is baked in**: Compose started Chroma (which created `docker-volumes/`) before it built the CLI image, and with no `.dockerignore`, `COPY . ./` (`Dockerfile:48`) took both |
| `15-x-mounts.txt` | extra | CLI: `~/AC215/llm-rag -> /app`, `~/AC215/secrets -> /secrets`; Chroma: `~/AC215/llm-rag/docker-volumes/chromadb -> /data` |
| `16-x-outputs-on-laptop.txt` | extra | after the chunk steps the files are on the laptop, owned by `student` (container user `app` is uid 1000 too) |
| `17-x-collections.txt`, `17b-x-collection-names.txt` | extra (after `cli-container/30-31`) | Chroma's REST listing (terminal view, 80 columns): both collections, `"metadata":{"hnsw:space":"cosine"}`, `"space":"cosine"`, Chroma's own `"embedding_function":{… "name":"default"}` (unused: the code passes vectors), `"dimension":null` (nothing inserted yet); 17b is the same reduced to names and dimensions |
| `18-x-docker-volumes-after-load.txt` | extra | still only `chroma.sqlite3` (empty collections create no index folders) |
| `20-x-ps-after-exit.txt` | extra (G8, Exercise 7) | after `exit`: the CLI container is gone (`--rm`), **`llm-rag-chromadb` is still Up** with port 8000 |
| `21-x-compose-down.txt` | extra (digest teardown, step 14) | `docker compose down` from the laptop: two `WARN[0000] The "GCP_PROJECT" / "GOOGLE_APPLICATION_CREDENTIALS" variable is not set. Defaulting to a blank string.` lines (the variables live only in `docker-shell.sh`; harmless here), then `[+] down 2/2`: container and network removed |
| `22-x-after-down.txt` | extra | no containers, no `llm-rag-network`; `docker-volumes/chromadb/` still holds the loaded database (`chroma.sqlite3` 59.8 MB and two UUID index folders, from `recorded-embeddings/`) |
| `23-x-docker-shell-again.txt` | extra (digest step 8, restart test) | second `sh docker-shell.sh`: `[+] run 2/2` (network, Chroma), **no pull, no build** (the image exists), banner, prompt, `exit` |
| `24-x-collection-names-after-restart.txt` | extra (README.md:160 "persistent") | both collections are back with `"dimension":256`; see also `cli-container/70-x-get-after-restart.txt` |
| `25-x-compose-down-final.txt`, `26-x-images.txt` | extra | `down` again; the three images remain |
| `27-x-git-status.txt` | extra | ` M docker-shell.sh` only; `outputs/`, `docker-volumes/` and `__pycache__/` are ignored (`.gitignore:3-5`) |

### `cli-container/` — typed at the container's prompt

While the session of `laptop/07-docker-shell.txt` was open, each command below ran in that same
container, as user `app` in `/app`, after activating `/.venv` exactly as `docker-entrypoint.sh:12`
does, so that each gets its own file and exit status (`docker exec` from a second terminal, stderr
joined to stdout inside the container; the output is what the session's terminal would show). The
prompt to draw is the session's, `app@<id>:/app$`. These files are not wrapped (scenes fold long
lines); pandas prints its tables for an 80-column width.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-whoami.txt`, `01-x-env.txt`, `02-x-ls.txt` | extra | user `app`, `/app`, `/.venv/bin/python`, Python 3.12.15, uv 0.13.1; `GCP_PROJECT=your-project-id`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json`, `/secrets` **empty**; the repo through the bind mount (02 in a terminal, columns) including `docker-volumes` |
| `03-x-packages.txt` | extra | the locked versions (above) |
| `04-x-chroma-by-name.txt` | extra (digest C8) | `getent hosts llm-rag-chromadb` → `172.19.0.2`; `curl http://llm-rag-chromadb:8000/api/v2/heartbeat` works by container name on the Compose network |
| `10-chunk-char-split.txt` | README.md:102-104 | the full real output: `CLI Arguments: Namespace(chunk=True, …, chunk_type='char-split')`, `chunk()`, `Number of files to process: 11`, then per book `Processing file:` / `Number of chunks: N` / `Shape: (N, 2)` / the DataFrame head (Gutenberg books start with `﻿The Project Gutenberg eBook of …`, E18). Order is the file system's (`The Complete Book of Cheese` first here) |
| `11-x-wc-char-split.txt` | extra | per book and **`8248 total`**; Tolminc 24, The Book of Cheese 2047 (the digest's table, confirmed) |
| `12-x-overlap-char-split.txt` | extra (V: chunk overlap) | Tolminc chunk 0 ends `'anized list of things she intended to ac'`, chunk 1 starts `'s she intended to accomplish during her '`: a mid-word cut and the 20-character overlap |
| `13-chunk-recursive-split.txt`, `14-x-wc-recursive-split.txt` | README.md:108-110 + extra | the full real output; **`14228 total`**, Tolminc 35, The Book of Cheese 3569 |
| `15-x-recursive-chunks.txt` | extra (E14) | Tolminc recursive chunks 0-2: chunk 0 ends at "nobody hurried."; chunk 1 **starts again** at "## Chapter One…" (the hidden default overlap of up to 200 characters) and stops at a word boundary |
| `16-x-ls-outputs.txt` | extra | 22 chunk files, 8.2 MB |
| `20-embed-char-split.txt` | README.md:128-131 (first line) | **Kept as instructive**: `embed()`, `Number of files to process: 11`, the first file (`Hand-book on cheese making`, `Shape: (395, 2)`, its head), then the first `embed_content` call asks for credentials and fails: `google.auth.exceptions.DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`, exit 1. Credentials are loaded lazily on the first request (`_api_client.py` `_access_token`), which is why chunking worked without a key (G2) |
| `22-x-after-embed.txt` | extra | no `embeddings-*` files were written; `/secrets` is empty |
| `30-load-char-split.txt`, `31-load-recursive-split.txt` | README.md:150-153 | real, exit 0, but with nothing to load: `load()`, `Creating collection: char-split-collection`, **`Collection 'char-split-collection' did not exist. Creating new.`**, `Created new empty collection …`, `Collection: Collection(name=char-split-collection)`, then **`Number of files to process: 0`** (the symptom of a skipped or failed embed). The first lines are exactly a first-time student's; the inserts are in `recorded-embeddings/01-02` |
| `32-x-load-again.txt` | extra | a second load prints **`Deleted existing collection 'char-split-collection'`** instead (load always rebuilds, `cli.py:280-289`) |
| `40-query-char-split.txt` | README.md:177-180 (first line) | **Kept as instructive**: it prints **`load()`** (the copy-paste label, `cli.py:310`, E3), then fails embedding the question (`cli.py:319` → `generate_query_embedding`, `cli.py:79`) with the same `DefaultCredentialsError`, before Chroma is touched |
| `42-x-get.txt` | extra (E13, `--get` is not in the README) | works without a key (no Vertex call): `get()`, `Results: {'ids': [], 'embeddings': None, 'metadatas': [], 'documents': [], 'data': None, 'uris': None, 'included': ['metadatas', 'documents']}` on the empty collection |
| `60-semantic-split.txt` | README.md:226-228 | **Kept as instructive**: `chunk()`, `Processing file: input-datasets/books/The Complete Book of Cheese.txt`, then the traceback runs `cli.py:212` → `semantic_splitter.py:275` → `:229` → `:206` (`_calculate_sentence_distances`) → `cli.py:98` `generate_text_embeddings` → `DefaultCredentialsError`: **semantic chunking calls the embedding API already in the chunk phase**, unlike char-split and recursive-split |
| `61-x-after-semantic.txt` | extra | no semantic files were written |
| `70-x-get-after-restart.txt` | extra (restart test) | in the second session (after `docker compose down` and a new `sh docker-shell.sh`): `--get` returns the 10 *The Complete Book of Cheese* records loaded before the restart: the database survived on the laptop's disk |

Run but **not kept** (each ends in the same `DefaultCredentialsError` at the same place as the kept
capture of its section, so it adds nothing; timings in `capture-only/cli-container-timings.txt`):
`python cli.py --embed --chunk_type recursive-split` (README.md:130), `python cli.py --query
--chunk_type recursive-split` (:179), `python cli.py --chat --chunk_type char-split` and
`--chunk_type recursive-split` (:199-200; they print `chat()` and fail at `cli.py:373`, the
question's embedding). Scenes type these commands and show no output panel, or say "the same
error, for the same reason" when they show the no-key path at all.

### `recorded-embeddings/` — the README's `--load` with the staff's own embeddings

`--embed` needs Vertex AI, so this capture could not make embeddings. The staff, however, committed
their whole `outputs/` folder (22 chunk files and 22 embeddings files, made with
`gemini-embedding-001`, 256 numbers per chunk) in `68e0bde` (2026-10-07, "ported api and
frontend-react to llm-rag", part of the "Demo podcast" PR, under `llmrag/outputs/`). The PR was
reverted and the files removed (`58dd602`), but they stay in `main`'s history, so every clone has
them. **Their 22 chunk files are byte-identical to the ones `cli-container/10` and `13` made here**
(checked with sha1), so their embeddings are exactly what `--embed` would have produced for these
chunks (with the staff's Vertex AI call, at their time). `00-x-copy-staff-embeddings.txt` copies the
embeddings files into `outputs/` (an extra, typed on the laptop; it stands in for a successful
`--embed`); everything after it is a real run. Scenes tag these panels `recorded` (real program
output on the staff's recorded vectors) and say where the vectors come from.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-copy-staff-embeddings.txt` | extra (stands in for README.md:128-131) | `git ls-tree … 68e0bde llmrag/outputs/ … git show "68e0bde:$f" > "outputs/${f##*/}"` → 22 files, 82 MB |
| `01-load-char-split.txt` | README.md:150-151 | the real load: `Deleted existing collection 'char-split-collection'` (the empty one from `cli-container/30`; a first load says `did not exist. Creating new.`, see `cli-container/30`), `Number of files to process: 11`, then per book `Processing file: outputs/embeddings-char-split-….jsonl`, `Shape: (N, 3)`, a DataFrame head with the `embedding` column (`[-0.0324312225, -0.0027327591, …`), `Inserted 500 items...` … `Finished inserting N items into collection 'char-split-collection'`; the 11 books add up to **8,248** |
| `02-load-recursive-split.txt` | README.md:152 | the same for `recursive-split-collection`, **14,228** items |
| `03-x-collection-names.txt` | extra | both collections now `"dimension":256` (fixed by the first insert) |
| `04-x-docker-volumes.txt` | extra (README.md:160) | on the laptop: `chroma.sqlite3` (59.8 MB) plus **two UUID-named folders**, one HNSW index per collection; 82 MB in all, owned by root |
| `05-x-get.txt` | extra (E13) | `--get`: 10 ids `1021665fac86c5a5-0` … `-9` (16 hex characters of the book name's SHA-256, then the row, `cli.py:127-130`), metadata `{'book': 'The Complete Book of Cheese', 'author': 'Bob Brown', 'year': 2024}` (key order varies), documents = the first 10 chunks in storage order, which are the **Project Gutenberg header and licence** (E18, G23), `'included': ['metadatas', 'documents']`, no `distances` (no ranking) |
| `06-x-vector-norms.txt` | extra (ponder: are the vectors unit length?) | Tolminc's 24 vectors, 256 numbers each, first five `[0.0139, 0.0075, 0.0099, -0.0664, -0.0192]`; **lengths 0.369 to 0.402, not 1**: truncated `gemini-embedding-001` vectors are not normalised, which cosine ignores and L2 would not (Exercise 5) |
| `07-x-metadata-per-book.txt` | extra (E8) | `count: 8248`; one metadata dict per book; **`{'book': 'Womans Institute Library of Cookery'}` has no author or year** (the book name is cut at the first dot, `cli.py:178`) |
| `08-x-filter-counts.txt` | extra (E2, C5) | `collection.get` counts with the README query's filters: all 8248; `where book = The Complete Book of Cheese` 1355; **and `$contains 'Italian'` 64**; and `$contains 'Tolminc'` **0**; any book containing `Tolminc` 3. So `--query`'s filters (`cli.py:354-359`) leave 64 candidates, none about Tolminc |
| `09-x-query-by-chunk-vector.txt` | extra (C5) | `collection.query` with a **stand-in query vector**: the stored embedding of a Tolminc chunk (`8440accaceb0ce96-6`, a dialogue passage; not the README's question, whose embedding needs Vertex AI). No filter: 10 Tolminc chunks, cosine distances 0.0000 (itself) to 0.1627. With the README query's `where` + `where_document`: 10 *Complete Book of Cheese* chunks at 0.2833 to 0.3123. Filters are applied **before** ranking; top-k always fills its 10 slots |

### `gotchas/` — extras on the same laptop, after `laptop/27`

| file | gotcha | what it shows |
| --- | --- | --- |
| `01-x-g5-compose-run-direct.txt` | G5 | `docker compose run --rm llm-rag-cli` without the script: the two `WARN … variable is not set. Defaulting to a blank string.` lines, Chroma and the network start, the banner, then at the prompt `python cli.py --chunk --chunk_type char-split` **fails at import**: `cli.py:35` `genai.Client(...)` with an empty project calls `google.auth.default()` and gets `DefaultCredentialsError: File  was not found.` (an empty file name between the two spaces), followed by `Exception ignored in: <function Client.__del__ …> … AttributeError: 'Client' object has no attribute '_api_client'`; `exit` (session exit status 1) |
| `02-x-g5-compose-down.txt` | | cleanup |
| `03-x-g1-clone-as-main.txt` | G1, E10 | a second workspace `~/AC215-zip`: `git clone … llm-rag-main` stands in for GitHub's "Download ZIP" (which unpacks `llm-rag-main/`), `mkdir secrets` |
| `04-x-g1-docker-shell.txt` | G1 | `sh docker-shell.sh` in `llm-rag-main/` (the image already exists, so no build): Compose project `llm-rag-main`, container `llm-rag-main-llm-rag-cli-run-<id>`, then **`/bin/bash: docker-entrypoint.sh: No such file or directory`**, exit 127 |
| `05-x-g1-stray-folder.txt` | G1 | why: Docker created the missing bind-mount source `../llm-rag` as an **empty folder owned by root** and mounted it over `/app` |
| `06-x-g1-compose-down.txt` | | cleanup |

### How these captures differ from a student's laptop

- **The laptop.** A `docker:29.8.2-dind` container with its own network namespace stands in for
  Docker Desktop (as in L04): `localhost:8000` and the fixed names `llm-rag-chromadb` /
  `llm-rag-network` are the laptop's alone. Its shell is Linux bash as user `student`; `sh` is
  BusyBox `sh` (on a Mac it is bash in POSIX mode, on Ubuntu dash): `docker-shell.sh` only exports
  and calls `docker compose`, so the output is the same. The architecture is x86_64: on Apple
  Silicon the banner says `Architecture: aarch64` (both images are multi-arch).
- **Terminal view vs plain.** `docker compose` sessions, `curl` on the laptop, `ls` and the
  collection listing ran in a real 80×40 pseudo-terminal (`tty_session.py`, rendered with `pyte`
  0.8.2): the file is what the terminal shows at the end, wrapped at 80 columns. The other files ran
  without a terminal and are not wrapped. `07-docker-shell.plain.txt` is the build's step-by-step
  log, replayed with `docker buildx history logs`.
- **Base image and apt.** Builds here need the recording proxy's CA certificate and https apt
  sources. `capture-only/base-python-3.12-slim-bookworm.Dockerfile` rebuilt `python:3.12-slim-bookworm`
  *under the same name* inside the laptop (log: `capture-only/base-python-3.12-slim-bookworm-build.txt`;
  the pulled image is `sha256:34386ef0…`), so the tutorial's `Dockerfile` builds unchanged. Visible
  effects: the `[1/6] FROM …@sha256:60c8fd1…` digest is the rebuilt image's; no base-image download
  appears in the build (a student's first build pulls `python:3.12-slim-bookworm`, ~48 MB); apt's
  `Get:` lines say `https://deb.debian.org`; inside the CLI container `env` would also show
  `SSL_CERT_FILE`, `REQUESTS_CA_BUNDLE`, `PIP_CERT` and the proxy variables.
- **Proxy and registry mirror.** The laptop's engine, git and curl reach the internet through a
  capture-only relay (`proxy_relay.py`) to the recording machine's proxy, and pull Docker Hub images
  through `mirror.gcr.io`; the pull lines are the same either way.
- **No key, no Google Cloud.** Every Vertex AI call stops at `DefaultCredentialsError`; nothing
  reached Google. `your-project-id` is a placeholder, not a project.
- **Ownership and modes.** The laptop's `student` and the image's `app` are both uid 1000, so the
  container writes `outputs/` as on Docker Desktop. `drwxrwsrwx` / `-rw-rw-rw-` and the setgid bits
  come from the capture's umask and parent folder, not from the tutorial. On a Linux laptop whose
  user is not uid 1000, `outputs/` may not be writable (G14); Chroma's files are root's on every
  Linux host.
- **Ids, times and file order** (container ids, collection UUIDs, heartbeat values, build times, the
  order `glob` returns the books in) change on every run.

### Things the captures found (README vs reality)

1. **Compose tries Docker Hub before building.** On the first `sh docker-shell.sh`, Compose v5.6.0
   prints `Image llm-rag-cli Pulling` and `failed to resolve reference
   "docker.io/library/llm-rag-cli:latest": … not found`, then builds (`laptop/07`). Harmless, but it
   looks like an error; the README says nothing about it.
2. **Chroma starts before the CLI image is built, and the image bakes in `docker-volumes/` and
   `.git`.** The build context is 112 MB: `.git` is 103 MB because the history carries the staff's
   90.9 MB `chroma.sqlite3` and `outputs/`; there is no `.dockerignore`, so the image holds
   `/app/.git` and a copy of the just-created `chroma.sqlite3` (`laptop/05b`, `07`, `14b`). The bind
   mount hides both at run time.
3. **The CLI container is not called `llm-rag-cli`.** `docker compose run` names it
   `llm-rag-llm-rag-cli-run-<id>` (`laptop/08`); `container_name: llm-rag-cli` (`docker-compose.yml:9`) is not used by
   `docker compose run`.
4. **`exit` leaves Chroma running**, and `docker compose down` from your own terminal warns about two
   unset variables (`laptop/20`, `21`): harmless, because `down` needs neither.
5. **Chroma's version strings disagree:** tag `latest` = `1.5.9` on Docker Hub, `chroma --version` =
   1.4.4, `/api/v2/version` = 1.0.0, client library 1.1.0 (`laptop/11`, `11b`; E9). It works.
6. **The query's filters leave no Tolminc text:** 64 Bob Brown chunks contain "Italian", none
   contains "Tolminc" (`recorded-embeddings/08`), confirming digest E2 with Chroma itself.
7. Confirmed from the digest: chunk counts 8,248 / 14,228 (Tolminc 24 / 35), the mid-word cut and
   20-character overlap, recursive-split's hidden overlap, the `load()` label of `--query` (E3), the
   Woman's Institute book without author/year (E8), `--get` (E13), the Gutenberg licence in the
   first chunks (E18), the empty-folder failure of G1 and the import-time failure of G5.

### Slides and captures

`SLIDES.md` lists where the lecture and the tutorial differ. Two of those differences are settled by
real output here: Chroma reports cosine **distances** (smaller is closer; 0.0000 for a chunk's own
vector, `recorded-embeddings/09`), not similarity scores; and its `where` / `where_document`
filters act **before** ranking (the filtered top 10 are all from Bob Brown's book, at larger
distances than the unfiltered ones), not as post-processing after ranking. The scenes show the
captures and say so kindly.

## `expected/` — what the tutorial documents (not captures)

Each file starts with a `#` line naming its source (repo, commit, file and lines); a command line
is marked `$`. The README prints **no output** for any step, so the README files are its own
descriptions of what a step does ("This will:"), not program output; scenes use them as text, never
in a terminal panel.

| file | source | used for |
| --- | --- | --- |
| `readme-chunk-this-will.txt` | README.md:112-116 | reference (the real chunk runs exist) |
| `readme-embed-this-will.txt` | README.md:133-138 | what `--embed` does (`gemini-embedding-001`; `text-embedding-004` retired on January 14, 2026) |
| `readme-load-this-will.txt` | README.md:155-160 | what `--load` does; the persistence claim of README.md:160 |
| `readme-query-this-will.txt` | README.md:182-186 | what `--query` does ("Apply various types of filters", E2) |
| `readme-chat-this-will.txt` | README.md:203-209 | what `--chat` does (sample query with one "?", E4) |
| `readme-semantic-this-will.txt` | README.md:230-236 | what the semantic run does |
| `out-txt-agent-run.txt` | `out.txt`, all 137 lines (= `source/out.txt`) | **recorded**: the staff's `python cli.py --agent --chunk_type char-split` run of 2026-09-22 04:01 UTC (`out.txt:34`), `model_version='gemini-3.1-flash-lite'`. It shows that the model answered at location `global` on that date, the retrieved chunks (`out.txt:70-93`, text from the **old** Tolminc book: the stale-index beat, E7), and the agent flow for the L06 preview. Not an output of any L05 README command |

## Illustrations (no capture is possible; schematic drawings tagged `illustration`)

| what | based on |
| --- | --- |
| GCP console: IAM & Admin › Service accounts › Create `llm-service-account`; roles **Storage Admin** and **Gemini Enterprise Agent Platform User** ("Vertex AI User" in older projects); the account › KEYS › ADD KEY › Create new key › JSON; the downloaded file renamed `llm-service-account.json` and moved into `secrets/` | README.md:52-69 (no screenshot, no logo, no key content, no real project id); the empty `secrets/` folder and `/secrets` are real (`laptop/03`, `cli-container/01`) |
| Enabling the Vertex AI API (`aiplatform.googleapis.com`), which the README never mentions (E6) | digest §2; the console page drawn schematically |
| Vertex AI answering: the embedding call (texts → 256 numbers) and `generate_content` (prompt → answer) | `cli.py:75-121`, `:388-399`; the vectors' real shape and values from `recorded-embeddings/06`; no invented answer text |
| The course web tools (`/chunkviz`, `/chromaui`, `/chat`, README.md:95, :162, :211) in Chrome | the README's links (all four pages answered HTTP 200 on 2026-10-16); the CORS check is real (`laptop/12`, `12b`); no screenshot of the site |

## Not captured, and how the video shows them

| README step | why | on screen |
| --- | --- | --- |
| Create the service account, grant roles, download the JSON key (README.md:52-62) | GCP console; needs a GCP account; the key is a credential | console illustration (above); never a key's content |
| Edit `GCP_PROJECT` (README.md:80) with a real Project ID | needs your project | the placeholder edit `laptop/06` (your-project-id) |
| `python cli.py --embed --chunk_type char-split` / `recursive-split` succeeding (README.md:128-131) | needs the key and Vertex AI (paid) | the command typed exactly; `cli-container/20` for the no-key failure (if shown at all); the README's description `expected/readme-embed-this-will.txt`; the real vectors from the staff's files (`recorded-embeddings/06`). Nothing documents the success output, so no invented one; narration says what to look for (per book `Processing file`, a second table with an `embedding` column, `embeddings-*.jsonl` files) |
| `python cli.py --load …` with embeddings (README.md:150-153) | needs embed's files | **real**, on the staff's embeddings: `recorded-embeddings/01-02` (tag `recorded`) |
| `python cli.py --query …` succeeding (README.md:177-180) | the question's embedding needs Vertex AI | the command typed exactly; `cli-container/40` (the `load()` label, then the key error) if the no-key path is shown; the filters' effect from real Chroma runs: `recorded-embeddings/08` (64 survivors, 0 about Tolminc) and `09` (filtered vs unfiltered top 10 with a stand-in vector, tagged `extra`); no invented `Results:` dict |
| `python cli.py --chat …` succeeding (README.md:199-200) | needs Vertex AI (embedding + Gemini) | the command typed exactly; no output panel (nothing in the repo documents a `--chat` run); narration says what to look for (`10`, `INPUT_PROMPT:`, `LLM Response:`); the closest recorded Gemini answer is the L06 `--agent` run (`expected/out-txt-agent-run.txt`), shown only as that |
| `python cli.py --chunk --embed --load --chunk_type semantic-split` succeeding (README.md:227) | ~528 embedding calls in the chunk phase alone | the command typed exactly; `cli-container/60` shows where it needs the API (the traceback through `semantic_splitter.py:206`) |
| The web tools: chunk visualiser, Chroma UI, chat tool (README.md:95, :162, :211) | a browser on an external site | illustration (above); the real CORS answer `laptop/12` |
| Agents (`python cli.py --agent --chunk_type char-split`, README.md:258) | L06's topic; needs Vertex AI | preview only, from `expected/out-txt-agent-run.txt` |

## Re-running

```bash
cd videos/ac215-l05-rag
export CA_BUNDLE=/root/.ccr/ca-bundle.crt   # only behind the recording proxy (with HTTPS_PROXY set)
export PYTHON=<a python with pyte>          # pip install pyte; renders the terminal views
bash assets/terminal/capture.sh main        # ~5 min; the laptop's volume grows to ~4 GB
bash assets/terminal/capture.sh gotchas     # ~1 min, on the same laptop; removes the laptop and relay at the end
```

`main` empties `laptop/`, `cli-container/` and `recorded-embeddings/` first and deletes the four
redundant failure captures listed above after running them; `gotchas` empties `gotchas/`. Ids,
UUIDs, timestamps, build times and the newest package versions (pip, uv, the Chroma image behind
`latest`) change on every run.
