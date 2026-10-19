# Exercise checks · ac215-l05-rag (2026-10-16, 15:04–15:58 UTC)

What was run to verify `exercises.md`, beyond the captures in `assets/terminal/`, which the answers
cite directly (`laptop/NN`, `cli-container/NN`, `recorded-embeddings/NN`). Logs and the check scripts
are in [`logs/`](logs/). Paths in them are shortened: `<checks>` is the scratch folder of these
checks, `<work>` its working copies of the repo.

## Setup (disposable; nothing from the repo ran on the host)

- Docker Engine 29.8.2, Compose v5.6.0, linux/amd64, on the session machine. Every image, container
  and network was named `l05ex*`.
- Work copy: `git clone` of the read-only `dlops-io/llm-rag` clone at `e17a39f` (the pinned commit);
  each check ran on its own copy of it (`b1`, `b3`, `b4`, `c6`, `c7`, …) so the clone stayed clean.
- The tutorial's image, `l05ex-cli`: its own `Dockerfile`, built unchanged with `logs/bld.sh`. The
  sandbox's TLS-intercepting proxy needs its CA inside builds, so `python:3.12-slim-bookworm`
  (`sha256:34386ef0…`, the same base as the capture) was given the CA and https apt sources as
  `l05ex/base:3.12` (`logs/check-base.Dockerfile`) and substituted through a named build context;
  the Dockerfile kept its `FROM` line. Side effect: BuildKit numbers the steps `[1/6] RUN …` instead
  of `[2/6] RUN …`. Result: Python 3.12.15, uv 0.13.1, 123 packages, chromadb 1.1.0, google-genai
  1.39.1, langchain-text-splitters 0.3.11 (`logs/build-baseline.log`): the capture's versions.
- `logs/crun.sh` runs a command in a throwaway container of that image, as user `app` in `/app`, with
  a work copy mounted on `/app`, an empty `/secrets`, `GCP_PROJECT=your-project-id` and
  `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json` (as `docker-shell.sh` sets
  them), and `/.venv` activated as `docker-entrypoint.sh:12` does: what the student types at the
  container's prompt. No network unless a check needs one.
- Chroma: the capture's server image, `chromadb/chroma@sha256:1e0b73a1…` (`latest` = `1.5.9`;
  `chroma 1.4.4` inside), as `l05ex-chroma` on a private network `l05ex-net` with the network alias
  `llm-rag-chromadb`, so the unchanged `cli.py` finds it by name. Its `/data` was a scratch folder.
- Vectors: the staff's 22 `embeddings-*.jsonl` files from `68e0bde` (as `recorded-embeddings/00`),
  loaded with the README's own `python cli.py --load …` commands.
- Compose checks (C3, C4, D4): the tutorial's `docker-compose.yml`, `docker-shell.sh`,
  `docker-entrypoint.sh` and `cli.py` in two folders both named `l05ex-rag`, with the compose file's
  fixed names and its host port renamed so nothing could collide with other work on the same Docker
  engine (`logs/compose-renames.diff`: `llm-rag-network` → `l05ex-rag-network`, the two
  `container_name`s → `l05ex-rag-cli` / `l05ex-rag-chromadb`, `../llm-rag` → `../l05ex-rag`,
  `8000:8000` → `18766:8000`, the image names → the local ones, so nothing was pulled or built).
  `sh docker-shell.sh` was run exactly as the README says, without a terminal.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| baseline | `bld.sh l05ex-cli` in a fresh clone | `transferring context: 112.07MB` (the capture's 112.26MB also held the 188 kB `chroma.sqlite3` Chroma had just created); `Installed 123 packages`; image 2.11GB / 537MB, as `laptop/14` |
| B1 | `cli.py:185-186` → 700 / 100, `python cli.py --chunk --chunk_type char-split`, `wc -l outputs/chunks-char-split-*.jsonl` (`b1-a-chunk-700-100.log`) | story `13`, `4537 total` |
| Q3, B1, B2 | `chunk_counts.py`: the tutorial's splitters on the eleven books (`b1-b2-chunk-counts.log`) | char-split 350/20: story 24, 8,248; 700/100: 13, 4,537; 700/20: 12, 4,007; recursive-split default: 35, 14,228; `chunk_overlap=20`: 28, 10,551; `chunk_overlap=0`: 28, 10,542; `1 + ⌈(len − 350)/330⌉` = every book's char-split count; `RecursiveCharacterTextSplitter()` default `chunk_overlap` 200, separators `['\n\n', '\n', ' ', '']` |
| Q3 | chunk lengths in the staff's files (`q3-chunk-lengths.log`) | char-split median 350; recursive-split median 297, longest 349, 100 % shorter than 350 |
| B3 | the START/END patch (`b3-strip.patch.py`) after `cli.py:181`, then chunk (`b3-strip-gutenberg.log`) | 11 books, `7656 total`; 2 chunks still contain "Project Gutenberg" (*Hints on cheese-making…* row 579, *The Book of Cheese* row 0) |
| B4 | chunk at `e17a39f`, then `cli.py:178` → `os.path.splitext(filename)[0]`, `book_key_check.py`, chunk again, `--embed` (`b4-*.log`) | old name not a `book_mappings` key, new name is; id prefixes `53b50dfe8ba86654` → `318f802bd1ab68d7`; old and new chunk files side by side (1,505 rows each); `Number of files to process: 12` (then the no-key error) |
| B5 | `python cli.py --load --chunk_type char-split` and `recursive-split` on the staff's vectors (logs trimmed to the step lines), then `--get` for each, through `get_summary.py` (ids, lengths, first 12 characters) (`b5-*.log`) | 8,248 and 14,228 inserted; both `--get` return `1021665fac86c5a5-0` … `-9`; char-split documents all 350 characters, recursive-split 283–346 |
| Q5, B6 | `sysinstr_check.py`: chat's `generate_content` call with `BaseApiClient.request` replaced, so the request is captured and nothing leaves (`b6-system-instruction-request.log`) | as committed: request keys `['_url', 'contents']`; with `config=types.GenerateContentConfig(system_instruction=SYSTEM_INSTRUCTION)`: `['_url', 'contents', 'generationConfig', 'systemInstruction']` |
| B7 | `semantic_calls.py`: the tutorial's `SemanticChunker` on each book, with a stand-in embedding function that counts the calls `generate_text_embeddings` would make and returns random vectors (`b7-semantic-calls.log`) | story: 108 sentences, 3 calls, 7 chunks, 1 embed call; all books: 26,080 windows, 528 calls, 1,318 chunks, 92 embed calls (chunk lengths in this log come from random vectors and mean nothing) |
| B7 | `small_collection.py`: a 7-record collection queried with `n_results=10` (`b7-b-ten-of-seven.log`) | 7 documents, no error |
| C1 | `python cli.py --get --chunk_type semantic-split` before any semantic load (`c1-get-semantic-not-found.log`) | `cli.py`, line 411, in get → `chromadb.errors.NotFoundError: Collection [semantic-split-collection] does not exist`, exit 1 |
| C2 | `--get` from a container on Docker's default bridge, outside the app's network (`c2-a-outside-network.log`); then `cli.py:30` → `os.environ.get("CHROMADB_HOST", "llm-rag-chromadb")` with `CHROMADB_HOST=localhost`, in a container sharing Chroma's network namespace (`c2-b-host-from-env.log`) | first exception `httpx.ConnectError: [Errno -2] Name or service not known`, last `ValueError: Could not connect to a Chroma server. Are you sure it is running?`, raised at `cli.py:406`; with the env var: the ten ids |
| C3 | a container publishing host port 18766, then `sh docker-shell.sh`; remove it, `sh docker-shell.sh` again; then `docker compose down` and start again (`g6-*.log`; run three times) | `Bind for 0.0.0.0:18766 failed: port is already allocated`, exit 1, `l05ex-rag-chromadb` left `Created`; the retry starts it with an empty PORTS column, `networks: {}`, heartbeat `curl: (7) Failed to connect`; from the app network `getent hosts` exits 2 and `chromadb.HttpClient` raises `Could not connect to a Chroma server`; after `down` + start: `8000/tcp -> 0.0.0.0:18766`, `networks: l05ex-rag-network`, heartbeat OK |
| C4 | a container named `l05ex-rag-chromadb` started by hand, then `sh docker-shell.sh`; `docker rm -f`, again (`g7-a`, `g7-b`) | `Conflict. The container name "/l05ex-rag-chromadb" is already in use by container "…". You have to remove (or rename) that container to be able to reuse that name.`, exit 1; after `rm -f` it starts |
| C4 | copy A running, then `sh docker-shell.sh` in copy B, a second folder with the same name (`g7-c`, `g7-d`) | no error: `Container l05ex-rag-chromadb Recreate` / `Recreated`; its `/data` now comes from copy B's `docker-volumes/chromadb` |
| C5 | `dim_check.py`: `query_embeddings` with 256 and 768 numbers on the loaded char-split collection (`c4-dimension-768.log`); `query_texts_check.py` with `query_texts` (`c5-query-texts.log`, with network for the model download; progress bar shortened) | 256: 10 results; 768: `chromadb.errors.InvalidArgumentError: Collection expecting embedding with dimension of 256, got 768`; `query_texts`: the collection's `embedding_function` is `default`, Chroma downloads `all-MiniLM-L6-v2` (79.3M), then `… dimension of 256, got 384` |
| C6 | `uv add rank-bm25` and the import in one throwaway container (network for PyPI); `git diff --stat` on the copy; a new container from the same image; a rebuild (`bld.sh`) and a container of it (`c6-*.log`) | `+ rank-bm25==0.2.2`; `pyproject.toml` and `uv.lock` changed on the host; new container: `ModuleNotFoundError: No module named 'rank_bm25'`; rebuild: `Installed 124 packages`, import OK |
| C7 | a copy owned by uid 1001, mode 755, no `outputs/`; chunk as `app` (uid 1000); then `mkdir outputs && chmod a+w outputs` (`c7-*.log`) | `PermissionError: [Errno 13] Permission denied: 'outputs'` from `cli.py:168`, exit 1; after the chmod: exit 0, 11 files owned by uid 1000 |
| D1 | `space_check.py`: brute-force top 10 by cosine and by squared L2, every stored char-split vector as the query; the same after normalizing; a Chroma collection without `hnsw:space` (`d1-cosine-vs-l2.log`) | lengths 0.342–0.405; same top 10 in the same order for 458 of 8,248 queries, same set for 2,650; normalized: 0 of 165 sampled differ; default space reported `l2`; the stand-in query's top 10 are story chunks in both spaces |
| D2 | `git` on the read-only clone (`d2-stale-index-git.log`) | today's book: 0 lines with `transhumance`; `85bba32^` (= `96d5fd7`, 2026-09-20): 3; `85bba32` (2026-09-22) changed the book and added `out.txt`; `out.txt:73` holds the line; `grep -n SYSTEM_INSTRUCTION cli.py` → line 40 only; no `secrets` line in `.gitignore` |
| D3 | a copy with the staff's `outputs/` and a loaded `docker-volumes/`, built without and with the four-line `.dockerignore` (`dot-dockerignore.txt`); the second build from a fresh copy of the folder, because BuildKit sends only changed files to a folder it has seen (`d3-*.log`) | context 257.74MB vs 4.58MB; `/app` 247M (`.git` 103M, `outputs` 82M, `docker-volumes` 58M) vs 4.5M; images 2.31GB / 597MB vs 1.89GB / 429MB |
| D4 | `docker compose down -v` in a copy, then `ls -la docker-volumes/chromadb`, `docker volume ls` (`d4-down-v.log`) | container and network removed; `chroma.sqlite3` still there; no volumes |
| D5 | Docker Hub's tag API for `latest`, `1.5.9`, `1.4.4`, `1.1.0` (`d4-chroma-tags.log`; the registry itself answered `429 Too Many Requests`) | `latest` and `1.5.9`: `sha256:1e0b73a1…`; no `1.4.4` tag; `1.1.0`: `sha256:df33933c…` (2025-09-16) |
| D6, D7 | `by_hand.py`: the lecture's table (A41) and RRF example (B44–B48) recomputed (`d5-d6-by-hand.log`) | cosine 0.9866 / 0.9756 / 0.8861; dot 80.15 / 81.24 / 60.50; Euclidean 1.673 / 2.093 / 4.498; RRF 0.75 / 0.6667 / 0.4167; with the fourth paragraph: k = 0 → 1 2 4 3, k = 60 → 1 4 2 3 |

## Not run (and why)

- Anything that calls Google: there is no key or Google account here. The answers to B6 (the model's
  answers with and without the system instruction), B7 (the real semantic run; its call and chunk
  counts were checked with a stand-in), and the `--embed` / `--load` after B1, B3 and B4 say what
  to expect and what was checked instead. The `--query` and `--chat` failures in C1 and C5 were
  reproduced by the same Chroma calls without the embedding call in front of them.
- Running `cli.py` on a real laptop (C2): a container outside the network stood in for the laptop,
  and one sharing Chroma's network namespace for its `localhost`. The `KeyError` without
  `GCP_PROJECT` and the f-string's need for Python 3.12 follow from the code (`cli.py:23`,
  `:388-391`) and were not run.
- `docker compose build` (C6): the same `Dockerfile` was built with `docker build`.
- C3/C4 with the compose file's real names and port 8000, and on Docker Desktop: renamed (see
  Setup) to avoid colliding with other work on the shared engine.
- The `1.1.0` Chroma server as a pin (D5): only its tag was looked up.

## Incident, and cleanup

- A first attempt at the Compose checks loaded both images into a Docker-in-Docker "laptop" (as the
  capture does). The session machine's disk ran out while the Chroma image was unpacking, at about
  15:44 UTC ("no space left on device"; 461 MB free). That laptop, its volume, three check images
  and the larger work copies were removed at once (4.3 GB free again by about 15:46 UTC), and the
  Compose checks ran on the shared engine with renamed resources instead. Other jobs writing to disk
  in those two minutes may have failed.
- Removed afterwards: every `l05ex*` container (`l05ex-chroma`, the port blocker, the Compose
  containers, all `--rm` runs), the networks `l05ex-net` and `l05ex-rag-network`, the images
  `l05ex-cli-noignore`, `l05ex-cli-ignore`, `l05ex-cli-bm25`, `l05ex-cli`, `l05ex/base:3.12`, and the
  scratch folder's work copies. The build cache of these builds was left in place (no shared prune).
