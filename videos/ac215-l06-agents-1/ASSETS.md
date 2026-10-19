# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing, a notebook output) is read
from a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

Copied unchanged with `git show <commit>:<path>` (each file checked against its git blob hash), at the repo's own
relative paths, so that a code panel's `path · lines a–b` matches a viewer's clone. Course material by the AC215
teaching staff (Harvard IACS), used for study with the instructor's permission.

- **`source/llm-rag/`**: [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag), branch `main`, commit
  `e17a39f35bc07b440f573def480adaf4703f8b91` (2026-10-07; still the head of `main` on 2026-10-18,
  `terminal/laptop/04-x-git-log.txt`): `README.md` (the Agents section is `:242-271`; L05's sections it stands on are
  Prerequisites `:45-48`, Setup GCP Service Account `:52-69`, Run LLM RAG Container `:75-85`, Load Embeddings
  `:144-165`), `cli.py` (`agent()` `:421-478`), `agent_tools.py` (the two `FunctionDeclaration`s `:9-38, 52-66`, the
  functions `:41-49, 69-75`, the dispatcher `:84-127`), `out.txt` (the staff's recorded `--agent` run, see
  `expected/`), `semantic_splitter.py`, `Dockerfile`, `docker-compose.yml`, `docker-shell.sh` and
  `docker-entrypoint.sh` (both mode 755, as committed), `pyproject.toml`, `uv.lock`, `.gitignore`, and
  `input-datasets/books/Tolminc Cheese.txt` (today's book: "Author: Pavlos Protopapas", a fictional story about Mara).
- **`source/llm-rag-tolminc-before-85bba32/input-datasets/books/Tolminc Cheese.txt`**: the same book at
  `96d5fd78d24607e20ae84d5339ed62abaadff17d` (2026-09-20), the parent of `85bba32` (2026-09-22, "llm and agent with
  updated pavlos book"), which rewrote it **and** added `out.txt`. `out.txt`'s retrieved text comes from this older
  version (`terminal/laptop/10-x-old-words.txt`; digest E2, G7).
- **`source/llm-agent-google-adk/`**: [dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk),
  branch `main` (its only branch), commit `f89faa79de744f6a046e30dff24b3b6f1d73720b` (2025-12-02; still the head
  of `main` on 2026-10-18): all 53 tracked text files at their paths (the root `README.md`, `QUICKSTART.md`,
  `pyproject.toml`, `.env.example`, `.gitignore`, and every module folder `1-baseline/` … `6-rag/`). Not copied:
  `demo.gif`.
- **`source/colab/<notebook>/cell-NN.py|.md`**: every non-empty cell of the three Colab notebooks of the lecture
  (`cheese-quiz`, `travel-planner`, `cheese-newsletter`), its source unchanged; `NN` is the cell's 0-based index in
  the `.ipynb` (Colab shows no numbers; the digest uses the same indices). Made by `terminal/colab_outputs.py` from
  the notebooks as downloaded on 2026-10-17 (Colab links in `expected/` headers; notebooks have no commit). **One
  change:** `cheese-newsletter/cell-16.redacted.py` is the `USERS` list with the course staff's first names and
  e-mail addresses replaced by `<reader1>`… / `<email>` (lines 8-11; everything else in the cell is unchanged and
  keeps its line numbers). Scenes never show those names.

## `terminal/` — real terminal sessions

Captured on **2026-10-18, 22:58–23:00 UTC** (llm-rag) and **23:31–23:33 UTC** (ADK) by `terminal/capture.sh` (which
starts a fresh "laptop") and `terminal/run_steps.sh` (which types the commands one by one). Each file starts with
the command (`$ ...`; a multi-line command, such as a `python - <<'EOF'` block, keeps its lines), then its output,
then its exit status (`[exit N]`); ANSI colour codes are removed. Every README command of the two sections is run in
README order, exactly as written. Files with `x-` in their name are **extras** (not README steps: checks, fixes,
gotcha demos); scenes mark them `extra`. Per-step UTC times and durations: `capture-only/*-timings.txt`.

| folder | what |
| --- | --- |
| `laptop/` | llm-rag, your laptop's terminal: clone, the `docker-shell.sh` edit, `sh docker-shell.sh` (build, Chroma, banner), second-terminal checks, the staff's embeddings, teardown |
| `cli-container/` | llm-rag, typed at the `llm-rag-cli` container's prompt (`app@…:/app$`): `--agent` before and after the collection exists, `--load`, `--get`, and extras that show both requests to Gemini and run the tool dispatcher |
| `adk-laptop/` | llm-agent-google-adk, your laptop's terminal: the whole root README (clone, `cd`, `cp .env.example .env`, `uv sync`, `uv run adk web`), what fails and the fixes, MCP over stdio, the port-8000 clash |
| `mcp-remote/` | the Cheese Quiz's remote MCP server (Colab cell 54), spoken to with `curl`: `initialize`, `tools/list`, `tools/call` |
| `expected/` | what the tutorial documents for steps that cannot run here: README text, the staff's `out.txt`, the Colab notebooks' saved outputs; first line of each says where it comes from |
| `capture-only/` | not tutorial material: the base-image Dockerfile the llm-rag capture needs and its build log (L05's file, unchanged), per-folder timings |
| `capture.sh`, `run_steps.sh`, `colab_outputs.py`, `tty_session.py`, `proxy_relay.py` | the scripts that made all of the above (`tty_session.py` and `proxy_relay.py` are L04's helpers, copied unchanged from L05) |

Chronological order: `laptop/00-07`, `cli-container/00-11`, `laptop/08`, `cli-container/20-34`, `laptop/09-11`,
exit, `laptop/12-14`; then (a second laptop) `adk-laptop/00-39`, `mcp-remote/01-04`. `laptop/11-x-hosted-agent.txt`
was re-run alone at 23:01 UTC on the same laptop after its command was corrected (the first form printed the
recording proxy's reply instead of the site's status).

### The machines and versions

- **llm-rag laptop** (as in L05): a fresh, empty Docker Engine **29.8.2** (client and engine, API 1.56,
  linux/amd64), Docker Compose **v5.6.0**, git 2.54.0, curl 8.22.0 (`laptop/00-x-env.txt`); user `student`
  (uid 1000), workspace `~/AC215` holding `llm-rag/` and `secrets/` side by side (README.md:64-69; the digest writes
  `~/Desktop/AC215`). There is **no service-account key**: `~/AC215/secrets/` exists but is empty.
- **The `llm-rag-cli` image**, built by Compose from the tutorial's `Dockerfile` on the first `sh docker-shell.sh`:
  `python:3.12-slim-bookworm`, **Python 3.12.15**, **uv 0.13.1**, `uv sync --frozen` installs 123 packages into
  `/.venv` as `uv.lock` pins them, among them **chromadb 1.1.0, google-genai 1.39.1, google-auth 2.41.1**
  (`cli-container/01-x-packages.txt`; the same set as L05). Build 40.5 s here. The Chroma server is
  `chromadb/chroma:latest` as pulled at 22:58 UTC (its version was not recorded in this capture; L05 recorded
  `chroma 1.4.4` for the same tag on 2026-10-16).
- **ADK laptop:** a fresh `debian:12` container (Debian 12 bookworm, Linux x86_64), git 2.39.5, **uv 0.13.1**
  (Astral's installer), **Node.js v24.22.0** (the newest LTS on nodejs.org) with **npm 11.19.1**, **no Python of its
  own** (`adk-laptop/00-x-env.txt`). uv downloads **CPython 3.15.0** by default; after the pin **CPython 3.13.16**.
  Installed (README `uv sync`, unpinned): **google-adk 2.12.0**, google-genai 2.31.0, litellm 1.106.0, fastapi
  0.141.1, uvicorn 0.54.0, mcp 2.3.0, chromadb 1.5.9, sentence-transformers 6.1.0, onnxruntime 1.31.0, torch
  2.14.1(+cpu here, see below); `.venv` 1.6 GB (`adk-laptop/14-x-packages.txt`). With the digest's pin: google-adk
  1.27.5, google-genai 1.75.0, mcp 1.30.0 (`adk-laptop/21-x-uv-add-pin.txt`). npx fetched
  `@modelcontextprotocol/server-filesystem` (latest on the npm registry that day: 1.0.0).
- Versions move: narration says "at the time of recording" for every version above.

### `laptop/` — your laptop's terminal (llm-rag)

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | date and versions |
| `01-clone.txt` | README.md:48 (Prerequisites "Cloned this repository"; the command is not printed) | `git clone https://github.com/dlops-io/llm-rag.git` → `Cloning into 'llm-rag'...` |
| `02-x-mkdir-secrets.txt` | extra (layout README.md:64-69) | `mkdir secrets; ls` → `llm-rag  secrets` (terminal view) |
| `03-cd.txt` | README.md:79 ("inside the `llm-rag` folder") | `cd llm-rag` |
| `04-x-git-log.txt` | extra | `e17a39f Merge pull request #2 from obalatel/revert-1-demo-podcast` = the pinned commit |
| `05-x-edit-gcp-project.txt` | README.md:80 | `git diff docker-shell.sh`: line 7 `ac215-project` → the **placeholder** `your-project-id`, made by a capture-only `sed` |
| `06-docker-shell.txt` (+ `.plain.txt`) | README.md:83-85 | `sh docker-shell.sh` in an 80×40 terminal: `[+] run 8/8`, `Image chromadb/chroma:latest Pulled 13.4s`, `Network llm-rag-network Created`, `Container llm-rag-chromadb Created`; `Image llm-rag-cli Pulling` / **`pull access denied for llm-rag-cli, repository does not exist or may require 'docker login'`** (Compose tries Docker Hub first, then builds; see the differences below), `[+] Building 40.5s (13/13) FINISHED` (context **112.26 MB**), `Container llm-rag-llm-rag-cli-run-61b50b7d6730 Created`, the entrypoint banner (`Container is running!!!`, `Architecture: x86_64`, `Environment ready! Virtual environment activated.`, `Python version: Python 3.12.15`, `UV version: uv 0.13.1 …`, `Activating virtual environment...`) and the prompt `app@abcf218747d0:/app$`; `exit` at the end. `.plain.txt` = the build's step log (591 lines) |
| `07-x-docker-ps.txt` | extra | `llm-rag-llm-rag-cli-run-<id>` (no published port) and `llm-rag-chromadb` with `0.0.0.0:8000->8000/tcp` |
| `08-x-copy-staff-embeddings.txt` | extra (stands in for L05's `--embed`, README.md:128) | the 11 `embeddings-char-split-*.jsonl` files of the staff's commit `68e0bde` (see `cli-container/20`), 31 MB |
| `09-x-book-changed.txt` | extra (digest G7, chapter 4 twist) | `git show --stat 85bba32`: `Tolminc Cheese.txt` 311 lines changed and `out.txt` added in the same commit (2026-09-22); today's book starts `Author: Pavlos Protopapas` / `# Tolminc: A Cheese, a Valley, and the Art of Waiting` / `*A fictional tale inspired by Alpine cheesemaking*` |
| `10-x-old-words.txt` | extra (E2) | `transhumance`, `Soča`, `Monastic`, `cultural artifact`: 2/3/1/2 lines in `out.txt`, **0** in today's book, 3/7/1/1 in the book before `85bba32` |
| `11-x-hosted-agent.txt` | extra (README.md:268) | the hosted Cheese Agent Tool answers `200 text/html; charset=utf-8` |
| `12-x-ps-after-exit.txt` | extra (digest G4) | after `exit`: the CLI container is gone (`--rm`), **`llm-rag-chromadb` is still up** with port 8000 |
| `13-x-compose-down.txt` | extra (digest teardown B6) | `docker compose down`: the two `WARN[0000] The "GOOGLE_APPLICATION_CREDENTIALS" / "GCP_PROJECT" variable is not set. Defaulting to a blank string.` lines, then `[+] down 2/2`, container and network removed |
| `14-x-git-status.txt` | extra | ` M docker-shell.sh` only |

### `cli-container/` — typed at the container's prompt (llm-rag)

While the session of `laptop/06-docker-shell.txt` was open, each command ran in that container, as user `app` in
`/app`, after activating `/.venv` exactly as `docker-entrypoint.sh:12` does (`docker exec` from a second terminal,
stderr joined to stdout; the output is what the session's terminal shows). The prompt to draw is the session's,
`app@<id>:/app$`. These files are not wrapped (scenes fold long lines).

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-whoami.txt` | extra | `app`, `/app`, `/.venv/bin/python`, Python 3.12.15, `GCP_PROJECT=your-project-id`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json`, `/secrets` **empty** |
| `01-x-packages.txt`, `02-x-help.txt` | extra | chromadb 1.1.0, google-auth 2.41.1, google-genai 1.39.1; `cli.py --help` lists `--agent  Chat with LLM Agent` |
| `10-agent-no-collection.txt` | README.md:258, on a fresh clone (digest G6) | **Kept as instructive**: `CLI Arguments: Namespace(… agent=True, chunk_type='char-split')`, `agent()`, then `cli.py:429` `client.get_collection(...)` → **`chromadb.errors.NotFoundError: Collection [char-split-collection] does not exist`**, exit 1: the agent needs L05's collection, and fails before any Gemini call |
| `11-x-get-no-collection.txt` | extra (digest B2) | `--get` fails the same way (`cli.py:411`) |
| `20-load-char-split.txt` | L05 README.md:150 | the real load of the staff's embeddings: `Collection 'char-split-collection' did not exist. Creating new.`, `Number of files to process: 11`, per book `Shape: (N, 3)` and the `embedding` column, `Finished inserting 24 items…` for Tolminc; **8,248** chunks in all (`34`) |
| `21-x-get.txt` | extra (digest B2) | `Results: {'ids': ['1021665fac86c5a5-0', …], …, 'metadatas': [{'author': 'Bob Brown', 'book': 'The Complete Book of Cheese', 'year': 2024}, …` (key order varies) |
| `30-agent.txt` | **README.md:258** | **Kept as instructive**: `agent()`, the printed `user_prompt_content:  parts=[Part(text="Describe where cheese making is important in Pavlos's book?")] role='user'` (`cli.py:440`), then the first `generate_content` (`cli.py:441`) asks for credentials and fails: **`google.auth.exceptions.DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`**, exit 1. Credentials load lazily on the first request, so the collection lookup (`cli.py:429`) passed |
| `31-x-call1-request.txt` | extra (C2, "the envelope") | **the request of call 1, exactly as google-genai 1.39.1 would send it**: `cli.agent()` runs unchanged; a 6-line stand-in for the SDK's transport (`api.request = show`) prints the URL and JSON body and stops. `POST https://aiplatform.googleapis.com/v1beta1/projects/your-project-id/locations/global/publishers/google/models/gemini-3.1-flash-lite:generateContent`; `contents` = the user turn; `tools[0].functionDeclarations` = both declarations with the 9-name `enum` and `"type": "STRING"/"OBJECT"`; **`"toolConfig": {"functionCallingConfig": {"mode": "ANY"}}`**; `"generationConfig": {"temperature": 0.0}`; then `-- stopped here: nothing was sent to Vertex AI --`, exit 1. No `systemInstruction` (E3). Nothing was sent, nothing answered |
| `32-x-mode-any.txt` | extra | `FunctionCallingConfig(mode="any")` → `mode=<FunctionCallingConfigMode.ANY: 'ANY'>` (the lower-case string maps to ANY) |
| `33-x-dispatch-recorded-call.txt` | extra (C2: "your code makes the call") | the **FunctionCall the model wrote in the staff's run** (`out.txt:20-27`: `get_book_by_author`, `author='Pavlos Protopapas'`, `search_content='cheese making importance location'`, `id='call_1212960'`) goes through the tutorial's own `agent_tools.execute_function_calls` against this laptop's collection. **Stand-in:** `embed_func` (Vertex AI) is replaced by a function returning the stored vector of Tolminc chunk `8440accaceb0ce96-6` (the first in storage order that mentions "curd"), so *which* 10 of the book's 24 chunks come back is not what the real query would return. Real: `Function: get_book_by_author`, `Calling function with args: Pavlos Protopapas , cheese making importance location`, `Response:` 10 chunks of **today's** book (Mara, Anja, curd, wheels), `function_responses: 1 part, name='get_book_by_author', response keys=['content'], 3509 characters`. Then the **request of call 2** (`cli.py:465-477`), printed the same way: `contents` = user turn; the model's turn with **`"thoughtSignature": "AY89a186…"`** (the bytes of `out.txt:28`) and `functionCall {id, args, name}`, `role: model`; a third content with `functionResponse {name, response: {content: …}}` and **no role**; `tools` again; **no `toolConfig`** (AUTO) and `"generationConfig": {}`; stopped, nothing sent |
| `34-x-authors.txt` | extra (P1, E4) | `chunks in char-split-collection: 8248`; per enum author: Langworthy & Hunt 401, Twamley 545, Newell 395, Curtis 640, Thom & Fisk 2047, Reid 522, Bob Brown 1355, Brooks 636, Pavlos Protopapas **24**; **unreachable by author:** `'Cottage Cheese Recipe Book'` 178 chunks (`author = 'Milk Industry Foundation'`, not in the enum) and `'Womans Institute Library of Cookery'` 1505 chunks (`author = None`: the name is cut at the first dot) |

`20`-`34` stand on the staff's embeddings: `--embed` needs Vertex AI, so (as in L05's `recorded-embeddings/`)
`laptop/08` copies the `embeddings-char-split-*` files the staff committed in `68e0bde` (2026-10-07, the reverted
"Demo podcast" PR, under `llmrag/outputs/`; still in `main`'s history, so every clone has them;
`gemini-embedding-001`, 256 numbers per chunk, made from today's book: 24 Tolminc lines). The `--load` and
everything after it are real runs.

### `adk-laptop/` — your laptop's terminal (llm-agent-google-adk)

The root README's commands (README.md:74-119) in order, on a laptop with no Python of its own, in
`~/AC215/llm-agent-google-adk`. `uv`/`adk web` sessions and `ls` ran in a real 80×40 terminal (wrapped at 80
columns); the rest without one.

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | date and versions; `no python3 on PATH` |
| `01-clone.txt` | README.md:77 (`git clone <repository-url>`; the URL filled in) | `Cloning into 'llm-agent-google-adk'...` |
| `02-cd-as-written.txt` | README.md:78 | **`cd google-adk-tutorial` → `No such file or directory`**, exit 1 (E8: the folder is `llm-agent-google-adk`) |
| `03-cd.txt` | README.md:78, with the real folder name | `cd llm-agent-google-adk` |
| `04-x-ls.txt` | extra | the repo: `1-baseline` … `6-rag`, `QUICKSTART.md`, `pyproject.toml`, `.env.example`, no `uv.lock` (git-ignored, `.gitignore:34`) |
| `05-cp-env.txt` | README.md:84 | `cp .env.example .env` |
| `06-x-env-file.txt` | extra (README.md:85 "add your GOOGLE_API_KEY": not done, no key here) | the copied file's settings: `GOOGLE_API_KEY=your_google_ai_api_key_here` (placeholder), `AWS_OPENAI_API_KEY=…`, **`GEMINI_MODEL=gemini-2.5-flash`** (digest G2), `ENVIRONMENT=development` |
| `07-uv-sync.txt` | **README.md:100** | **Kept as instructive; the README's `uv sync` fails on a fresh machine:** `Using CPython 3.15.0`, `Creating virtual environment at: .venv`, `Resolved 189 packages in 3.46s`, then `error: Distribution onnxruntime==1.31.0 … can't be installed because it doesn't have a source distribution or wheel for the current platform` / `hint: You're using CPython 3.15 (cp315), but onnxruntime (v1.31.0) only has wheels with the following Python ABI tags: cp311, cp312, cp313, cp313t, cp314, cp314t`, exit 2. uv 0.13.1 picks the newest CPython when it finds none; onnxruntime comes in through `chromadb` (`pyproject.toml:18`) |
| `08-x-after-failed-sync.txt` | extra | what the failed sync left: `.venv` (CPython 3.15) and a `uv.lock` of 189 packages with **`google-adk` 2.11.0 and 2.12.0** (2.11.0 for Python 3.10) |
| `09-x-python-pin.txt` | extra (**the fix**, not in the README) | `uv python pin 3.13` → ``Pinned `.python-version` to `3.13` `` |
| `10-x-sync-plan.txt` | extra | `uv sync --dry-run` on this Linux PC, no capture override: `Using CPython 3.13.16`, `Would download 167 packages`, the `+` list with **torch 2.14.1, triton 3.8.0 and 15 `nvidia-*` packages** (CUDA; about 3 GB). A Mac's plan has none of the CUDA packages |
| `11-x-capture-only-uv-config.txt` | **capture-only** (not a student step) | the uv config the capture adds from here on (`index-strategy = "unsafe-best-match"`, extra index `https://download.pytorch.org/whl/cpu`) and the failed sync's lockfile removed (`ls uv.lock` → no such file) |
| `12-uv-sync.txt` | **README.md:100, again** | now real and complete: `Using CPython 3.13.16`, `Removed virtual environment at: .venv`, `Creating virtual environment at: .venv`, `Resolved 171 packages`, `Prepared 148 packages`, `Installed 148 packages`, the `+` list (`google-adk==2.12.0`, `onnxruntime==1.31.0`, **`torch==2.14.1+cpu`**), exit 0. A student's second sync says `Resolved 189 packages` and installs plain `torch==2.14.1` (plus, on Linux PCs, the CUDA packages) |
| `13-x-adk-version.txt`, `14-x-packages.txt` | extra | `adk, version 2.12.0`; the versions above; `.venv` 1.6 GB |
| `15-adk-web.txt` | **README.md:116** | `uv run adk web` in a terminal: first **the telemetry question** (`Help improve the ADK (CLI and Web UI) by allowing Google to collect pseudonymized usage data?` … `This is OFF by default.` … **`Enable telemetry? [Y/n]: `**; Enter means yes; the capture typed `n`), INFO lines, two `[EXPERIMENTAL]` UserWarnings, `Started server process`, the box `ADK Web Server started` / `For local testing, access at http://127.0.0.1:8000.`, `Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)`; the request log of `16`-`18`; Ctrl+C → `ADK Web Server shutting down...`, `Aborted!` |
| `16-x-dev-ui.txt` | extra (README.md:119 "open http://localhost:8000") | `/` → `307 -> http://localhost:8000/dev-ui/` (the browser lands on the dev UI) |
| `17-x-list-apps.txt` | extra (what the UI's agent dropdown lists) | ADK 2.12: **seven** entries, `1-baseline`, `2-litellm`, `3-mcp-tools`, `4-production-ready.app`, `5-custom-agent`, `6-rag.1-vertex-rag-engine`, `6-rag.2-custom-chromadb-rag` |
| `18-x-select-1-baseline.txt` | extra (picking `1-baseline` in the UI; digest G1) | `{"detail":"Invalid agent name: '1-baseline'. Agent names must be valid Python identifiers or paths separated by dots (letters, digits, underscores, and dots)."}` (HTTP 404, `15`'s log) |
| `19-x-quickstart-file.txt` | extra (QUICKSTART.md:24; G9) | `uv run adk web 1-baseline/agent.py` → `Error: Invalid value for '[AGENTS_DIR]': Directory '1-baseline/agent.py' is a file.`, exit 2 |
| `20-x-adk-without-web.txt` | extra (2-litellm/README.md:74 etc.; G10) | `uv run adk` → the usage and command list (2.12: `api_server`, `create`, `deploy`, `eval`, `run`, `telemetry`, `web`, …), exit 2: nothing starts |
| `21-x-uv-add-pin.txt` … `26-x-select-1-baseline-pinned.txt` | extra (**the digest's G1 fix A, which is not enough**) | `uv add "google-adk>=1.8.0,<1.28"` → `- google-adk==2.12.0` / `+ google-adk==1.27.5` (and 43 more changes); `adk, version 1.27.5`; `git diff pyproject.toml` (line 10); `uv run adk web` (no telemetry question in 1.27.5); the list is now the four folders `["1-baseline","2-litellm","3-mcp-tools","5-custom-agent"]`; but picking `1-baseline` → `Internal Server Error`: the log (`24`) shows **`pydantic_core._pydantic_core.ValidationError: 1 validation error for App` / `Invalid app name '1-baseline': must be a valid identifier consisting of letters, digits, and underscores.`** The loader accepts the name; the web server's `App(name=app_name)` does not |
| `27-x-undo-pin.txt` | extra | `git checkout pyproject.toml; uv sync --upgrade-package google-adk` → back to `google-adk==2.12.0` |
| `28-x-rename.txt` | extra (**the fix that works**) | `mv 1-baseline baseline; mv 3-mcp-tools mcp_tools; mv 5-custom-agent custom_agent; ls` |
| `29-x-adk-web-renamed.txt` | extra (README.md:116 after the rename) | `uv run adk web` again (2.12); its log shows `GET /dev/apps/baseline/build_graph 200 OK`, the sessions, and for `33` **`google.genai.errors.ClientError: 400 INVALID_ARGUMENT. {'error': {'code': 400, 'message': 'API key not valid. Please pass a valid API key.', …`**: the placeholder key reached Google and was refused |
| `30-x-list-apps-renamed.txt` | extra | the list now has `baseline`, `custom_agent`, `mcp_tools` |
| `31-x-select-baseline.txt` | extra (C6) | the agent tree the UI loads, from `/dev/apps/baseline/build_graph`: `TravelPlannerPipeline \| Sequential itinerary planning pipeline` with `ItineraryValidator` / `TravelPlanner` / `TripSummarizer`, each `model gemini-2.5-flash` (from the root `.env`), `output_key itinerary_validation` / `travel_plan` / `trip_summary` and its instruction (`Using {itinerary_validation}, …`, `… based on {travel_plan}. …`); no tools |
| `32-x-new-session.txt` | extra (C6: the empty whiteboard) | a new session: `{"id":"…","appName":"baseline","userId":"student","state":{},"events":[],…}` |
| `33-x-send-placeholder-key.txt` | extra (what happens before you add your key) | a trip request sent through `POST /run` → `Internal Server Error` (the reason is in `29`'s log: API key not valid) |
| `34-x-node.txt` | extra (3-mcp-tools/README.md:53-64) | `v24.22.0`, `11.19.1` |
| `35-x-mcp-toolset.txt` | extra (C5, Excerpt 8; no model involved) | the agent's own `MCPToolset` (`mcp_tools/agent.py`, = `3-mcp-tools/agent.py:20-29`) starts `npx -y @modelcontextprotocol/server-filesystem <folder>` as a child process: `Secure MCP Filesystem Server running on stdio`, `Client does not support MCP Roots, using allowed directories set from server args: [ '…/mcp_tools' ]`, an `npm notice` about npm 12.2.0; **`tools the agent sees: ['list_directory', 'read_file', 'search_files']`**, **`tools the server offers: 14 [...]`** (`read_text_file`, `write_file`, `edit_file`, … filtered out by `tool_filter`); `list_directory` → `[FILE] .env.example`, `[FILE] README.md`, `[DIR] __pycache__`, `[FILE] agent.py`, `[FILE] pyproject.toml` |
| `36-x-port-8000-busy.txt` | extra (digest G3, Exercise 4) | with a Chroma server on port 8000 (`{"nanosecond heartbeat":…}`), `uv run adk web` prints its banner, then **`ERROR:    [Errno 98] error while attempting to bind on address ('127.0.0.1', 8000): address already in use`**, shuts down, exit 3 |
| `37-x-adk-web-port-8080.txt`, `38-x-list-apps-8080.txt` | extra (the G3 fix) | `uv run adk web --port 8080` starts (`Uvicorn running on http://127.0.0.1:8080`); the list answers on 8080 |
| `39-x-git-status.txt` | extra | ` M pyproject.toml` is gone (undone); the renamed folders show as deleted + untracked; `?? .python-version`; ignored: `.env`, `.venv/`, `uv.lock`, `__pycache__/`. ADK keeps each agent's sessions in `<agent>/.adk/` (inside `baseline/`), which the repo's `.gitignore` does not list |

### `mcp-remote/` — the Cheese Quiz's MCP server, with curl (extras, from the ADK laptop)

| file | what it shows |
| --- | --- |
| `01-x-browser-get.txt` | a plain GET of `https://pavlos-fun-facts.dlops.io/mcp` (what a browser does) → `HTTP/2 406`, `{"jsonrpc":"2.0","id":"server-error","error":{"code":-32600,"message":"Not Acceptable: Client must accept text/event-stream"}}`: the server is up; it speaks MCP, not web pages |
| `02-x-initialize.txt` | JSON-RPC `initialize` → an SSE `event: message` with `"protocolVersion":"2025-06-18"`, capabilities (`tools`, `prompts`, `resources`), `"serverInfo":{"name":"Pavlos Cheese MCP","version":"1.16.0"}`; the `mcp-session-id` header (shown as `<id>`) |
| `03-x-tools-list.txt` | `notifications/initialized`, then `tools/list` → one tool, `pavlos_fun_fact_mcp`, "Return one random fun fact from Pavlos about cheese. Call multiple times if you want several facts.", empty `inputSchema` |
| `04-x-tools-call.txt` | `tools/call pavlos_fun_fact_mcp {}` → `{"fact":"Browned spots on grilled cheese = Maillard reaction (not caramelization).","generated_at":1792365989}` as text content and `structuredContent`, `"isError":false` |

### How these captures differ from a student's laptop

- **The llm-rag laptop.** A `docker:29.8.2-dind` container with its own network namespace stands in for Docker
  Desktop (as in L04/L05). Its shell is Linux bash as user `student`; `sh` is BusyBox `sh` (`docker-shell.sh` only
  exports and calls `docker compose`). x86_64: on Apple Silicon the banner says `Architecture: aarch64`.
- **Image store.** This laptop's engine stores images with the classic overlay2 driver (containerd image store off,
  to halve its disk use). Visible effect: Compose's failed pull of `llm-rag-cli` reads `pull access denied for
  llm-rag-cli, repository does not exist or may require 'docker login'`; with the containerd store (Docker Desktop's
  default, L05's capture) it reads `failed to resolve reference "docker.io/library/llm-rag-cli:latest": … not
  found`. Both are harmless and are followed by the build. The build's export step is faster here (4.4 s).
- **Base image, proxy, mirror** (as in L05): `python:3.12-slim-bookworm` was rebuilt under the same name with the
  recording proxy's CA and https apt sources (`capture-only/base-python-3.12-slim-bookworm.Dockerfile`, build log
  next to it), so the tutorial's `Dockerfile` builds unchanged; no base-image download appears in the build (a
  student's first build pulls it). Both laptops reach the internet through `proxy_relay.py`; the llm-rag laptop
  pulls Docker Hub images through `mirror.gcr.io`.
- **The ADK laptop** is a `debian:12` container, not a Mac: Node from nodejs.org's Linux binaries (on a Mac:
  `brew install node`, `3-mcp-tools/README.md:57`), uv from Astral's installer (L01). Its home folder is a 3 GB
  in-memory filesystem (capture-only). `~/.npmrc` carries the proxy and CA for npm (capture-only): `npx`, started by
  MCP's stdio client, receives only `HOME`, `PATH`, `USER`, … from its parent, not the proxy variables. A laptop
  with direct internet needs neither.
- **PyTorch.** From `11-x-capture-only-uv-config` on, uv takes PyTorch's CPU-only Linux wheel
  (`torch==2.14.1+cpu`) instead of the CUDA build (torch 2.14.1 + triton 3.8.0 + 15 `nvidia-*` packages, about 3 GB,
  more than the recording machine could hold; `10-x-sync-plan`). The extra index changes `12`'s `Resolved 171
  packages` (189 for a student), its `+` list (no CUDA packages; the `+cpu` suffix) and the pin step's `Resolved 200
  packages`. A Mac gets no CUDA packages either: its `+` list matches `12` minus the `+cpu` suffix. Everything ADK
  does afterwards is the same with either PyTorch (`adk web` never imports it).
- **Telemetry.** `15` answered ADK 2.12's question with `n`, so later runs on this laptop do not ask again (the
  answer is stored in `~/.adk/config.json`); 1.27.5 never asks.
- **The port clash (`36`).** On a student's laptop, llm-rag's `llm-rag-chromadb` publishes port 8000 through Docker.
  Here a `chromadb/chroma` container (the image L05's captures used, `sha256:1e0b73a1…`) runs in the laptop's own
  network namespace (`docker run --network container:l06-adk`) and binds port 8000 directly. The error `adk web`
  prints is the same.
- **No keys, no Google Cloud, no OpenAI.** Every Vertex AI call stops at `DefaultCredentialsError` or before the
  request is sent (`31`, `33`); the only request that reached Google is `adk-laptop/33`'s, with the placeholder key
  of `.env.example`, which Google refused. `your-project-id` is a placeholder, not a project. The Colab notebooks
  were not run.
- **Ids, times and order** (container ids, session ids, the fun fact, build times, the order of DataFrame columns
  and metadata keys) change on every run.

### Things the captures found (README vs reality, and corrections to the digest)

1. **The ADK README's `uv sync` fails on a fresh machine today.** uv 0.13.1 downloads the newest CPython (3.15.0),
   and `onnxruntime` 1.31.0 (pulled in by `chromadb`) has no cp315 wheels (`adk-laptop/07`). Fix: `uv python pin
   3.13` (any of 3.11-3.14 works), then `uv sync` again (`09`, `12`). The digest's resolution check ran on a
   Python 3.12 image and did not meet this.
2. **The digest's G1 fix A (pin `google-adk<1.28`) does not make `1-baseline` runnable in `adk web`.** Under 1.27.5
   the loader accepts `1-baseline`, but `adk web` wraps the agent in `App(name=app_name)`, whose validator rejects
   any name that is not a Python identifier (`adk-laptop/24`, `26`). The wheels of 1.19.0 (current at the repo's
   last commit), 1.21.0, 1.23.0, 1.25.0 and 1.27.5 all have this check (`apps/app.py` `validate_app_name`,
   `cli/adk_web_server.py` `get_runner_async`; read, not run). **What works: give the folders Python-identifier
   names** (`mv 1-baseline baseline`, … `adk-laptop/28`-`31`) and keep today's ADK 2.12. Symlinks were tried outside
   the recorded run and not kept: with 1.27.5, symlinks in a separate `agents/` folder (the digest's fix B) fail when
   the UI creates a session (`Invalid app_name 'baseline': resolves outside base directory`); with 2.12, symlinks
   are not listed in the dropdown.
3. **ADK 2.12 asks about telemetry** the first time `adk web` runs in a terminal, before the server starts; Enter
   means yes, although the text says it is off by default (`adk-laptop/15`). The README does not mention it.
4. **ADK 2.12's dropdown lists seven entries**, including dotted nested ones (`4-production-ready.app`,
   `6-rag.1-vertex-rag-engine`, `6-rag.2-custom-chromadb-rag`; `17`). The digest's "exactly four" holds for 1.27.5
   (`25`), not for 2.12's web server.
5. **The placeholder key fails only when you send a message:** `adk web` starts and loads agents with
   `GOOGLE_API_KEY=your_google_ai_api_key_here`; the first message gets `400 … API key not valid` in the server log
   and `Internal Server Error` in the browser (`29`, `33`).
6. Confirmed from the digest: `cd google-adk-tutorial` fails (E8, `02`); `adk web <file>` (G9, `19`); `adk` without
   `web` (G10, `20`); the port-8000 clash and `--port 8080` (G3, `36`-`38`); MCP's `tool_filter` passes 3 of the
   server's 14 tools and `list_directory` returns the module's four files plus `__pycache__` (C5, `35`); the remote
   MCP server answers `initialize` / `tools/list` with `pavlos_fun_fact_mcp` and a plain GET with 406 (A7,
   `mcp-remote/`); `--agent` on a fresh clone fails at `get_collection` (G6, `cli-container/10`); with the
   collection, it fails at the first `generate_content` for want of a key (B3, `30`); `mode="any"` is sent as
   `"mode": "ANY"`, and call 2 has no tool config (Excerpts 3-4, `31`-`33`); the model's `thought_signature` travels
   back as `thoughtSignature` and the function response carries no `id` (Excerpt 5); two books are unreachable by
   author, 178 and 1,505 chunks (E4, P1, `34`); `out.txt` quotes the old book (E2, G7, `laptop/10`); `exit` leaves
   Chroma running (G4, `laptop/12`).
7. New, small: ADK writes each agent's sessions into `<agent>/.adk/` inside the repo, which the repo's `.gitignore`
   does not cover (`39`); `uv add` already syncs, and `uv sync` after it would do nothing (`21`).

### Slides and captures

`SLIDES.md` asks to re-check Conflicts 1, 2, 4 and 5 against the captures:

- **1 (`--agent` is one lap, not a loop):** the two requests (`31`, `33`) are the whole conversation `agent()` has
  with Gemini; call 2 carries no tool config, so a second tool call would only be printed. Consistent.
- **2 (`mode="any"` forces a search):** `"toolConfig": {"functionCallingConfig": {"mode": "ANY"}}` is in the real
  request (`31`). Consistent.
- **4 (one connection per MCP server):** a child process over stdio (`adk-laptop/35`) and a remote server over
  streamable HTTP with its own session id (`mcp-remote/`). Consistent.
- **5 (the travel planner is a rehearsal):** the Travel Planner's saved run books nothing ("Nothing has been booked",
  "fictional planning only", `expected/colab-travel-planner-c27-turn4-yes.txt`), and ADK's `1-baseline` is three
  `LlmAgent`s with no tools (`adk-laptop/31`). Consistent.

## `expected/` — what the tutorial documents (not captures)

Each file starts with a `#` line naming its source. `expected` = text the tutorial documents (scenes use it as
text, never in a terminal panel); `recorded` = real program output saved by the course staff (tag `recorded` on
screen, and say where it comes from).

| file | kind | source | used for |
| --- | --- | --- | --- |
| `readme-agents-this-will.txt` | expected | llm-rag README.md:261-271 | what `--agent` does ("This will:"), the hosted Cheese Agent Tool, "Use Chrome" |
| `out-txt-agent-run.txt` | **recorded** | llm-rag `out.txt`, all 137 lines (= `source/llm-rag/out.txt`) | the staff's `--agent` run of 2026-09-22 04:01 UTC (`gemini-3.1-flash-lite`, location global): the `FunctionCall` (`out.txt:20-27`) with its `thought_signature` (`:28`), the `Function calls:` list (`:56-63`), `Calling function with args: Pavlos Protopapas , cheese making importance location` (`:67`), the retrieved chunks (`:70-93`, **old book**), the answer (`:104-113`, about the Soča Valley), tokens 247 + 1,269 (`:49`, `:135`). The only successful `--agent` output that exists |
| `adk-readme-running-agents.txt` | expected | ADK README.md:109-119 | "open http://localhost:8000 … select the agents" (the UI is an illustration) |
| `adk-4-production-ready-api.txt` | expected | ADK 4-production-ready/README.md:54-62 | the FastAPI wrapper's `/health`, `/chat`, `/chat/stream` shapes (module 4 not run) |
| `colab-cheese-quiz-c13-download.txt` | recorded | Cheese Quiz cell 13 | the two `gdown` downloads (`quiz-schema.json` 2.10k, `quiz-ui.html` 10.8k) |
| `colab-cheese-quiz-c21-base-llm.txt` | recorded | cell 21 | `🧠 BaseLLM: Making single API call...`, the answer, `Tokens: 293, Time: 2.81s` |
| `colab-cheese-quiz-c25-reasoning-llm.txt`, `-c26-reasoning-steps.txt` | recorded | cells 25-26 | the five-step trace (**eleven** `Making single API call...` lines), `Sub-questions explored: 4`, `Total tokens: 701, Time: 39.34s`; the six step outputs |
| `colab-cheese-quiz-c31-simple-agent.txt` | recorded | cell 31 | `🤖 SimpleAgent: Running with web_search …`, the researched answer with sources, `Tools used: 1`, `Time: 13.29s` |
| `colab-cheese-quiz-c38…c44-step1…step7-*.txt` | recorded | cells 38-44 | the seven context layers' answers (C4); step 2 is the swapped-roles cell (E1) |
| `colab-cheese-quiz-c48-fun-facts-tool.txt`, `-c49-tool-agent.txt`, `-c50-tools-called.txt` | recorded | cells 48-50 | the first tool: the agent's answer, `I am a tool` ×3 (E14), `1. pavlos_fun_fact_tool  args={}` ×3 and the three fact dicts (one repeated) |
| `colab-cheese-quiz-c54-remote-mcp.txt` | recorded | cell 54 | the answer with the remote MCP server's tool |
| `colab-cheese-quiz-c57-fastmcp-server.txt`, `-c59-local-mcp.txt` | recorded | cells 57, 59 | `FastMCP server starting on http://127.0.0.1:8000/mcp` (saved from an older version of the cell; the code now uses 8001, E14), the FastMCP banner; the uvicorn log `"POST /mcp HTTP/1.1" 200 OK` interleaved with `Pavlos Fun Fact Tool Called` |
| `colab-cheese-quiz-c64-stilton.txt`, `-c65-brie.txt` | recorded | cells 64-65 | two Guild specialists alone: Stilton's cited facts, Brie's `QuizDraft(...)` |
| `colab-cheese-quiz-c75-guild-star-wars.txt`, `-c77-guild-greek.txt` | recorded | cells 75, 77 | three `ERROR:openai.agents:Error getting response` lines each (C7), and the quiz the Guild produced (the widget's embedded quiz data as JSON) |
| `colab-travel-planner-c24-turn1.txt` … `-c27-turn4-yes.txt`, `-c29-chat-loop.txt` | recorded | cells 24-27, 29 | turn 1 `Kind: clarification`; turn 2 the five `[tool]` calls and `Kind: options`; turn 3 `[tool] finalize_plan: …`, `Kind: clarification` and the exact JSON proposal; turn 4 (`yes`) `Kind: itinerary` and the budget report computed by Python (`"total_usd": 2690.0`, `"remaining_usd": 3310.0`, costs 880 / 1000 / 600 / 150 / 60); the interactive loop's start |
| `colab-cheese-newsletter-c08-install.txt` | recorded | Newsletter cell 8 | the pip progress lines (final states) |
| `colab-cheese-newsletter-c27-run-demo.txt` | recorded | cell 27 | per reader `Generating newsletter for <city> · 2026-09`, `[tool] researcher_agent`, `[tool] editor_agent` (×4 for Summerville), `[tool] send_email: validating and saving HTML (mock)`, `Saved HTML: /content/newsletter_output/<reader1>-2026-09-25fd23e3.html (8005 bytes). No email sent.`, `Created 4 mock emails. No email was sent.`, the four receipts. **Readers' names replaced** by `<reader1>`-`<reader4>` (course staff) |
| `colab-cheese-newsletter-c30-preview-1.txt`, `-c31-preview-2.txt` | recorded | cells 30-31 | the two saved HTML previews as text (names and addresses replaced): "LOCAL EMAIL PREVIEW · NOT SENT", the Summerville letter with `Promotion URL: https://shop.lowesfoods.com/…` inside an offer (E15) |

All `colab-*` files were extracted by `terminal/colab_outputs.py` from the notebooks' saved outputs: the staff's
last runs (Cheese Quiz 2026-09-23; Newsletter 2026-09-20 13:27 UTC; Travel Planner: no date stored). Each header
names the notebook, its Colab link and the cell. Saved outputs may predate the current code of their cell (E14:
cells 49, 57; Newsletter cell 27 shows four readers, the current `USERS` has two).

## Illustrations (no capture is possible; schematic drawings tagged `illustration`)

| what | based on |
| --- | --- |
| GCP console: the service account `llm-service-account` with its role, the JSON key into `secrets/` (L05's drawing) | llm-rag README.md:52-69; the empty `secrets/` and `/secrets` are real (`laptop/02`, `cli-container/00`) |
| Vertex AI / Gemini answering call 1 (a `functionCall`) and call 2 (the answer) | the real request bodies `cli-container/31`, `33`; the answer's shape and text only from `expected/out-txt-agent-run.txt` (tagged `recorded`) |
| Google AI Studio: "Create API key", the key pasted into `.env` | ADK README.md:88-94; never a key's content |
| The ADK dev UI in a browser: the agent dropdown, the chat, the Events and State tabs | ADK README.md:111-119; the dropdown's real entries `adk-laptop/17`, `30`; the agent tree `31`; the empty session `32`; no screenshot |
| Colab: File › Save a copy in Drive; the Secrets panel (`OPENAI_API_KEY`, Notebook access); Runtime › Disconnect and delete runtime | digest A1-A2, D1, E1; no screenshot |
| The Cheese Quiz widget and the Newsletter preview | the recorded quiz data and preview text in `expected/` |
| The hosted Cheese Agent Tool page (README.md:268) | only its HTTP status is real (`laptop/11`) |

## Not captured, and how the video shows them

| step | why | on screen |
| --- | --- | --- |
| `python cli.py --agent --chunk_type char-split` succeeding (llm-rag README.md:258) | needs the service-account key and Vertex AI (paid) | the command typed exactly; the real failure `cli-container/30` if the no-key path is shown; the real requests `31`/`33` (tag `extra`); the staff's run `expected/out-txt-agent-run.txt` (tag `recorded`, with "made with the old book"); narration says what to look for (`LLM Response:` with a `function_call`, `Function: get_book_by_author`, `Response:`, the second `LLM Response:` with text) |
| `--embed` for the collection (L05 README.md:128) | needs Vertex AI | the staff's embeddings, `laptop/08` + the real `--load` `cli-container/20` (as in L05) |
| Edit `GCP_PROJECT` with a real Project ID (README.md:80) | needs your project | the placeholder edit `laptop/05` |
| "Edit .env and add your GOOGLE_API_KEY"; AI Studio key (ADK README.md:85, 88-94) | needs a Google account and a key | illustration; `adk-laptop/06` shows the placeholder; `29`/`33` what the placeholder does |
| Chatting with `baseline`, `mcp_tools`, `custom_agent` in `adk web` (the UI's events and state) | needs a Gemini key | the agent tree `31`, the empty session `32`, MCP without a model `35`; no invented model replies or event views |
| The three Colab notebooks | need an OpenAI key (paid) | their saved outputs in `expected/colab-*` (tag `recorded`) |
| ADK modules 2, 4, 5, 6 run with a model (`2-litellm`, `uvicorn app.main:app`, `simple_custom_agent.py`, `conditional_agent.py`, the RAG agents) | need keys; not in the root README | code panels from `source/`; module 4's documented API `expected/adk-4-production-ready-api.txt`; no output panel |

## Re-running

```bash
cd videos/ac215-l06-agents-1
export CA_BUNDLE=/root/.ccr/ca-bundle.crt   # only behind the recording proxy (with HTTPS_PROXY set)
export PYTHON=<a python with pyte>          # pip install pyte; renders the terminal views
bash assets/terminal/capture.sh rag         # ~3 min; the laptop's Docker volume grows to ~2.3 GB, removed at the end
CHROMA_IMAGE=<optional local chromadb/chroma image id> bash assets/terminal/capture.sh adk   # ~4 min; 3 GB in RAM
python3 -I assets/terminal/colab_outputs.py <folder with the three .ipynb> .
```

Start from empty capture folders: the scripts overwrite the files they write and remove nothing (`KEEP=1` keeps a
laptop for inspection). Ids, times, the fun fact, build times and the newest versions (uv, CPython, ADK and its
dependencies, Node, the Chroma image behind `latest`) change on every run.
