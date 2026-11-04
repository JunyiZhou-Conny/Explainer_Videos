# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** the recording sandbox has **no GCP
credentials** (see the skill's environment rules), and L10 is the lecture *about* credentials.
Everything local — clone, secrets-folder convention, Docker network, both image builds, ChromaDB,
uvicorn, Next.js, ports, container DNS, CORS, persistence — is captured live. Every step that
needs a real Google credential is captured up to its **honest, documented failure**
(`DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`, the exact text
of digest §6 #2), and the success output a student would see is tagged `recorded` with its source
below. No output was invented.

## `source/` — the tutorials' own files

### `source/cheese-app-v0/`

From [dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0) at commit
`cb6fb94576aa37bb0b94a8745e5e94e6a504f4bb` (main, 2026-10-08; still the head of `main` on
2026-10-19, verified in `terminal/laptop/02-git-log.txt`), copied unchanged with
`git show <commit>:<path>`, relative paths preserved. Course material by the AC215 teaching staff
(Harvard IACS), used for study with the instructor's permission.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (269 lines): SA setup (46-67), network (69-75), vector DB (79-106), API (125-149), frontend (153-180), the five UI steps (184-255), endpoint table (259-269) |
| `.gitignore` | ignores `docker-volumes` and `outputs` — **not** `secrets/` (digest §3.4) |
| `llm-rag/docker-shell.sh` | `GCP_PROJECT` to edit (7), `GOOGLE_APPLICATION_CREDENTIALS=/secrets/…` (8), `docker compose run --rm` (12) |
| `llm-rag/docker-compose.yml` | `llm-rag-network` (1-3), `../../secrets:/secrets` + `../llm-rag:/app` (11-12), shell-interpolated env (14-15), `container_name: llm-rag-chromadb` (20), `8000:8000` (21-22), `./docker-volumes/chromadb:/data` (23-24), the CORS guest list (26) |
| `llm-rag/Dockerfile`, `docker-entrypoint.sh` | python:3.12-slim base, uv sync, user `app`; the "Container is running!!!" banner and venv activation |
| `llm-rag/cli.py` | `GCP_PROJECT` from env (23), `CHROMADB_HOST="llm-rag-chromadb"` (30-31), the ADC-backed client (35-36), chunk/embed/load (164-306), delete-then-create (281-289), the `filename.split(".")[0]` bug (178) |
| `llm-rag/agent_tools.py`, `semantic_splitter.py`, `pyproject.toml`, `uv.lock`, `README.md` | the CLI's tools, the optional L05 tutorial, the pins (chromadb 1.1.0, google-genai 1.39.1, langchain 0.3.27) |
| `api-service/docker-shell.sh` | Excerpts 1-2 of the digest: `SECRETS_DIR=$(pwd)/../../secrets/` (8), `GCP_PROJECT` (9), the **non-idempotent** `docker network create` (14), the `docker run` with `-p 9000:9000`, both mounts, both env vars, `--network` (19-27) |
| `api-service/Dockerfile`, `docker-entrypoint.sh`, `Pipfile`, `Pipfile.lock` | pipenv sync of 170 pins; `uvicorn_server` = `uvicorn api.service:app --host 0.0.0.0 --port 9000 … --reload-dir api/` (7); `DEV=1` → `pipenv shell` (25-26) |
| `api-service/api/service.py` | CORS `allow_origins=["*"]` (13-20), `Startup tasks` (25), the welcome route (29-32) |
| `api-service/api/routers/rag.py` | `os.environ["GCP_PROJECT"]` (15), the instructor's endpoint (22), the ADC client (26), `generate_query_embedding` (89-95), the `location="us"` ft_client (110-120), the five endpoints (218-265) |
| `api-service/agent_tools.py` | the two retrieval tools + server-side `pavlos_fun_fact_tool` |
| `frontend-ai-chatbot/docker-shell.sh`, `Dockerfile.dev`, `Dockerfile` | `-p 3200:3000`, `--network cheese-app-network` (11); node:20-alpine + bash; the unused production build |
| `frontend-ai-chatbot/.env.development`, `.env.production`, `src/services/Common.js` | `NEXT_PUBLIC_BASE_API_URL=http://localhost:9000` baked into browser JS; `/api` in production |
| `frontend-ai-chatbot/next.config.js` | the stale `rag-system-api-service` rewrites (16, 23, 30; digest errata #3) |
| `frontend-ai-chatbot/package.json` | `next 14.2.4`, `WATCHPACK_POLLING=true next dev` |
| `src/services/DataService.js` | every browser HTTP call; the Chroma v2 query POST (34-43) |
| `src/hooks/hooks.jsx` | the Chroma UI's `GET {url}/api/v2/version` (14) and collections calls |
| `src/components/chat/ChatComponent.jsx` | the browser-orchestrated RAG flow (161-173), agent flow (176-198), auto-selected collection (228-231) |
| `src/components/chatui/ChatComponent.jsx` | the dead `/chatui` page's wrong arguments (digest errata #11) |
| `src/components/textchunk/TextChunkComponent.jsx` | in-browser splitting, no cloud (247, 272-274) |
| `src/components/architecture/ArchitectureDiagram.jsx` | the animated diagram that still draws the *hosted* topology (digest errata #8) |
| `src/app/page.jsx`, `src/app/chromaui/page.jsx` | the home-page cards and "hosted on Google Cloud" text; the Chroma UI's defaults + `localStorage` (16-27) |

### Neighbour repos (context the digest's code tour quotes; none of them run in L10)

| snapshot | from | what a panel quotes |
| --- | --- | --- |
| `source/llm-finetuning/README.md`, `dataset-creator/cli.py`, `gemini-finetuner/cli.py` | [dlops-io/llm-finetuning](https://github.com/dlops-io/llm-finetuning) @ `44ef6f0a70315aa0a551b8565ca862679a87c1eb` | the role-rename note (README:44-46), key tips (README:64-69); GCS upload with ADC (dataset-creator/cli.py:279-294, digest Excerpt 12); the `location="us"` + `base_url` client (gemini-finetuner/cli.py:25-33) and the endpoint print (91-96) |
| `source/mega-pipeline/transcribe_audio/cli.py` | [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) @ `c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc` | GCS download with ADC (36-43) |
| `source/llm-rag/README.md` | [dlops-io/llm-rag](https://github.com/dlops-io/llm-rag) @ `e17a39f35bc07b440f573def480adaf4703f8b91` (the standalone L05 repo) | the old hosted-frontend links (95-98, 162-165…), origin of the "Use Chrome" note (digest gotcha #20) and of the §7 diff |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured **2026-10-19 22:11–22:18 UTC** (segments `pre` … `api2`) and **2026-10-20 01:44–01:49
UTC** (`fe1` … `down`; the recording sandbox restarted in between — see capture-only notes) by
`terminal/capture.sh`, which runs `terminal/run_steps.sh` inside one fresh disposable container,
one segment at a time. Each README command runs exactly as written, in README order, and its
output goes to its own file: the file starts with the command (`$ ...`), then the output, then its
exit status (`[exit N]`; single-line outputs carry it inline). Steps that are not in the README
are marked *extra* below and in `run_steps.sh`.

Two kinds of file, as in L02/L09: **`step` files** (no terminal, plain output) and **`istep`
files** (a real pseudo-terminal via `ptyrun.py`, 110×50; the lines a person would type at the
container prompt are typed when the prompt appears — `python cli.py …`, `uvicorn_server`,
`npm install`, Ctrl-C as the `^C` byte; progress bars appear redrawn, colours are dropped).

| folder | environment | source it follows |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's machine with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2, compose v5.6.0, linux/amd64), user `student` in the `docker` group, git 2.54.0, curl, tree | cheese-app-v0 `README.md`, top to bottom |

### `laptop/` — the README top to bottom

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, `Linux x86_64`, Docker 29.8.2, Compose v5.6.0, git 2.54.0 |
| `01-clone.txt` | Prerequisites: "Cloned this repository" (README:44; this is the repo's address) | the clone |
| `02-git-log.txt` | extra | HEAD = `cb6fb945…` 2026-10-08: the clone equals the digest's pin |
| `03-ls.txt` | extra | the repo's top level (including the committed `.DS_Store`, digest errata #14) |
| `04-mkdir-secrets.txt` | SA setup step 7 / folder tree (README:56-67; the README shows the tree, not a command) | `mkdir ../secrets` from inside the repo — the folder the `../../secrets` mounts resolve to |
| `05-tree.txt` | the README:60-67 folder structure (extra) | `tree -L 2`: `secrets/llm-service-account.json` **beside** `cheese-app-v0`, exactly the README tree (the key file is a placeholder, see below) |
| `06-ls-secrets.txt` | extra (digest step-1 checkpoint) | `llm-service-account.json`, not `.json.json` |
| `10-network-create.txt` | "Create the Docker Network" (README:74) | the network id — created |
| `11-network-create-again.txt` | extra | the same README command again: exit 0, silent — idempotent (contrast with `31`) |
| `12/13-network-*.txt` | extra | `docker network ls`, `inspect` (subnet, no containers yet) |
| `20-edit-gcp-project.txt` | Build the Vector DB step 2 (README:84 says to edit; `sed` is the editor here) | `GCP_PROJECT="your-gcp-project"` in `llm-rag/docker-shell.sh:7` |
| `21-docker-shell.txt` | step 3: `sh docker-shell.sh` (README:88), typed inside: extras `ls -la /secrets`, `echo $GOOGLE_APPLICATION_CREDENTIALS $GCP_PROJECT`, `exit` | 110×50 terminal: compose pulls `chromadb/chroma`, builds `llm-rag-cli` (uv sync 7.5 s), starts `llm-rag-chromadb`, `Container is running!!!`, `Architecture: x86_64`, Python 3.12.15, the `app@…:/app$` prompt; `/secrets` shows the (placeholder) key through the mount; both env vars set |
| `22-docker-ps.txt` | extra (README:106's claim) | ChromaDB still Up after the CLI exit, `0.0.0.0:8000->8000/tcp` |
| `23-curl-chroma-version.txt` | extra (digest §4 checkpoint; same route as `hooks.jsx:14`) | `"1.0.0"` from `http://localhost:8000/api/v2/version` |
| `24-cli-char-split.txt` | step 4, first command verbatim (README:94) | chunk() runs **for real**: `Number of files to process: 11`, per-book `Number of chunks`, pandas heads; then embed() reaches for credentials and fails honestly — `DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` (digest §6 #2 verbatim), exit 1. The embed/load success a student sees is `recorded`, see below |
| `25-cli-recursive-split.txt` | step 4, second command verbatim (README:95) | same: chunk() real (2147/1198/2623/… chunks per book), embed() the documented failure |
| `26-outputs-ls.txt` | extra | the chunk JSONLs on the host through the `/app` mount — including `chunks-char-split-Womans Institute Library of Cookery.jsonl`, the title truncated at its first `.` — digest gotcha #18 visible in the wild |
| `27-chunk-counts.txt` | extra | **8,248** char-split and **14,228** recursive-split chunks — the digest §2 estimates (~8.2 k / ~14.2 k) confirmed live |
| `28-chunk-sample.txt` | extra | one real chunk of "Tolminc Cheese" (author Pavlos Protopapas) |
| `29-auth-check.txt` | extra (digest §4 step 3 suggested sanity check) | `/secrets` now empty; `google.auth.default()` → the documented `DefaultCredentialsError` — what ADC does when slot 1 points at a missing file |
| `30-edit-gcp-project.txt` | Run API Service step 2 (README:130) | `GCP_PROJECT="your-gcp-project"` in `api-service/docker-shell.sh:9` |
| `31-docker-shell-aborts.txt` | step 3 verbatim, unmodified script (README:134) | **the digest's gotcha #1, live**: `Error response from daemon: network with name cheese-app-network already exists`, exit 1 — `docker-shell.sh:14`'s bare `docker network create` under `set -e` |
| `32-fix-network-line.txt` | extra (the digest §4 step 4.2 fix) | line 14 replaced by the README:74 idempotent form |
| `33-docker-shell.txt` | step 3 again + step 4: `uvicorn_server` (README:140), Ctrl-C, `exit` | 110×50 terminal: the pipenv build (170 pins), green help text, `(app) …:/app$` prompt, uvicorn to `Application startup complete.`; the `GET /rag/embedding` **500** with the full `DefaultCredentialsError` traceback in the debug log (the honest no-credentials state, exactly where digest §4 says it surfaces); `^C`, clean shutdown. The access-log lines for `GET /` (readiness probe) and `GET /capture-done 404` (the harness's stop cue) are capture-only artifacts — scenes crop them |
| `34-curl-root.txt` | extra (README:147) | `{"message":"Welcome to the API Service"}` |
| `35-curl-docs.txt` | extra (README:149) | `/docs` answers `200 text/html` |
| `36-openapi-routes.txt` | extra (README:259-269) | the live route list: the five `/rag` endpoints of the README's table, plus `GET /` |
| `37-curl-embedding.txt` | extra (digest's "first real cloud call" check) | `HTTP/1.1 500 Internal Server Error` — honest here; the matching traceback is in `33`; the success body is `recorded`, see below |
| `38-cors-api.txt` | extra (service.py:17) | preflight from a *wrong* origin (`:3300`) still gets `access-control-allow-origin: *` — FastAPI's guest list is "anyone" |
| `39-docker-ps.txt` | extra | API + ChromaDB running, port columns `9000->9000`, `8000->8000` |
| `40-network-inspect.txt` | extra | `cheese-app-network` with the API container attached |
| `41-exec-dns-fail.txt` | extra (digest E5 a) | from inside the API container, `http://llm-rag-chromadb:8000` → `Name or service not known` — different network, no DNS |
| `42-network-connect.txt` | extra (E5 b) | `docker network connect cheese-app-network llm-rag-chromadb` |
| `43-exec-dns-ok.txt` | extra (E5 b) | the same URL now returns `b'"1.0.0"'` — Docker DNS on a shared network |
| `44-exec-localhost-fail.txt` | extra (E5 c) | `http://localhost:8000` from inside the API container → `Connection refused` — `localhost` is the container itself |
| `45-network-disconnect.txt` | extra | back to the tutorial's state |
| `46-docker-ps-after.txt` | extra | `--rm` removed the API container; ChromaDB stays |
| `50-docker-shell-npm-install.txt` | Run Frontend (README:161), `npm install` (README:167) typed inside | build of `Dockerfile.dev`, the root `…:/app#` prompt, `added 773 packages` (npm 10.8.2's deprecation warnings included); `node_modules` lands on the host through the bind mount |
| `51-npm-run-dev.txt` | `npm run dev` (README:168), Ctrl-C, `exit` | `▲ Next.js 14.2.4`, **`Local: http://localhost:3000`** (the container's own view — digest gotcha #10), `✓ Ready in 1648ms`, the `✓ Compiled /…` lines as each page is first requested; the `GET /capture-done 404` line is the harness's stop cue (capture-only), then `^C`, exit |
| `52-curl-home.txt` | extra (README:177) | `http://localhost:3200/` → `HTTP 200`, `<title>RAG App</title>` |
| `53-curl-3000-fail.txt` | extra (digest gotcha #10) | `http://localhost:3000/` from the host → `Failed to connect` — nothing is published on 3000 |
| `54-docker-ps.txt` | extra | the `0.0.0.0:3200->3000/tcp` column, ChromaDB beside it |
| `55-exec-localhost-3000.txt` | extra (digest §3.5) | *inside* the container, `localhost:3000` answers with the same page — one server, two addresses |
| `56/57/58-curl-*.txt` | extra (README:188, 202, 215) | `/chunkviz`, `/chromaui`, `/chat` each `HTTP 200` + title — the server-side half of the three UI steps; what the pages *do* happens in a browser (see below) |
| `60-cors-preflight-3200.txt` | extra (digest §3.6; docker-compose.yml:26) | OPTIONS preflight with `Origin: http://localhost:3200` → `access-control-allow-origin: http://localhost:3200` — on the guest list |
| `61-cors-preflight-3300.txt` | extra | the same preflight from `:3300` → **no** `access-control-allow-origin` header — the browser would block the read (digest E1) |
| `62-cors-get-3200.txt` | extra | a simple GET with the good origin also carries the header |
| `63-curl-collections.txt` | extra | the collections list is `[]` — honest: nothing could be embedded/loaded without credentials. The populated list (`char-split-collection`, `recursive-split-collection`) is `recorded`, README:103/206 |
| `70-compose-down.txt` | README:106 | `docker compose down` inside `llm-rag`: ChromaDB stopped and removed, `llm-rag-network` removed — plus compose's real "variable is not set" warnings (the interpolation mechanism of digest gotcha #5, visible because `down` runs outside `docker-shell.sh`) |
| `71-docker-ps-after.txt` | extra | nothing running |
| `72-volumes-persist.txt` | extra (digest §3.7) | `docker-volumes/chromadb/chroma.sqlite3` survived the containers |
| `73-chroma-back.txt` | extra (the same README:88 command) | `sh docker-shell.sh` re-creates the network and ChromaDB from the same folder; exit |
| `74-curl-version-again.txt` | extra | `"1.0.0"` again — same data directory |
| `75-compose-down-again.txt`, `76-network-rm.txt` | extra (digest §2 shutdown checklist) | the machine left clean, `docker network rm cheese-app-network` |
| `capture-only/` | not part of the tutorial | the two base-image re-tags (Dockerfiles + build logs), the placeholder key and its move log — see below |

## What cannot run here, and what was recorded instead

- **The GCP console (SA setup steps 1-6, README:46-55).** Browser clicks; scenes draw a schematic
  console tagged `illustration` (never a screenshot or logo). The field values to draw come from
  `source/cheese-app-v0/README.md:46-56`: name **`llm-service-account`**; roles **Storage Admin**
  and **Gemini Enterprise Agent Platform User** ("Vertex AI User" in older projects; same role
  `roles/aiplatform.user` — `source/llm-finetuning/README.md:44-46`); **KEYS → ADD Key (Create
  New Key) → JSON**; the download moved to `secrets/llm-service-account.json`. The key file's
  *fields* (`type`, `project_id`, `private_key`, `client_email`, `token_uri`) are drawn as an
  `illustration` from digest §3.1; never render a plausible private key.
- **Every Vertex AI call.** No credentials exist here, so `--embed`/`--load` success, the
  `/rag/embedding` body, chat, agent and fine-tuned answers cannot be captured. What the captures
  show instead is the *documented failure* at the exact moment credentials are first needed
  (`24`, `25`, `29`, `33`+`37`). For the success path:
  - `python cli.py … --embed --load` checkpoints → tag `recorded`, sources: README:98-105 (what
    the step does) and the code's own prints — `cli.py:231` (`embed()`), `:236/240` (file
    counts), `:278` (`Creating collection: …`), `:283/285` (`Deleted existing collection …` /
    `Collection '…' did not exist. Creating new.`), `:157/159-160` (`Inserted N items…`,
    `Finished inserting N items into collection '…'`). Do not invent timings or request counts
    beyond digest §2's estimates (now corroborated by `27-chunk-counts.txt`).
  - `GET /rag/embedding?text=hello` success → tag `recorded`: `{"embedding": [...]}`, a list of
    256 floats — source `rag.py:218-223` with `EMBEDDING_DIMENSION = 256` (`rag.py:17`); the
    README's endpoint table names the route (README:263-265). Never show concrete float values.
  - **Chat / Agent / Pavlos-model answers: no source documents their text.** Nothing in the repo
    stores an example answer, and there is no Colab. Scenes show the command/flow and *describe
    what to look for* (an answer plus a "References" drawer of 10 chunks, README:217-222; an
    answer ending in a highlighted **Pavlos' fun fact** paragraph, README:236-239 +
    `ChatComponent.jsx:22-28`) **without an output panel**.
- **The browser UI itself** (`/chunkviz`, `/chromaui`, `/chat`, `/agent`, `/finetunechat`,
  DevTools Network tab). Drawn as schematics tagged `illustration`; the live server-side half is
  captured (`52`-`58`), the pages' XHR flows come from `source/` (`ChatComponent.jsx:161-198`,
  `DataService.js`, `hooks.jsx`). The populated Chroma UI sidebar (`char-split-collection`,
  `recursive-split-collection`) is `recorded` from README:103/206; the live list here is honestly
  empty (`63`).
- **Step 5 of 5, the fine-tuned endpoint edit (README:247).** Requires a student's own L08
  endpoint; the default (`rag.py:22`) points at the instructor's project `129349313346` and the
  digest expects a 403 for everyone else (errata #4). Nothing documents that error's exact text,
  so scenes show `rag.py:22` from `source/` and describe the edit (the new value is printed by
  L08's trainer, `source/llm-finetuning/gemini-finetuner/cli.py:91-96`) without an output panel.
- **The optional LLM RAG tutorial (README:110-122)** is L05 material ("not required to run the
  app"); out of L10's capture scope. Its file is snapshotted (`source/cheese-app-v0/llm-rag/README.md`).
- **"Use Chrome" (README:179-180)** is prose; digest gotcha #20 has the likely origin.

## Capture-only deviations (the recording sandbox vs a student's machine)

None of the tutorial's commands were changed; the environment around them was:

- **Proxy relay and Docker client proxies.** The sandbox reaches the internet only through a
  TLS-intercepting HTTPS proxy on the host's loopback. `proxy_relay.py` (container `l10-relay`)
  forwards the bridge gateway to it; the laptop engine and its containers get it through
  `~/.docker/config.json`'s `proxies` setting (what Docker Desktop has under Settings ›
  Resources › Proxies). Invisible in the outputs.
- **Capture-only base images.** `python:3.12-slim-bookworm` (used by `llm-rag/Dockerfile` and
  `api-service/Dockerfile`) and `node:20-alpine` (`Dockerfile.dev`) were rebuilt with the proxy's
  CA, https apt sources and CA env vars (`SSL_CERT_FILE`, `PIP_CERT`, `REQUESTS_CA_BUNDLE`,
  `UV_NATIVE_TLS` / `NODE_EXTRA_CA_CERTS`, `NPM_CONFIG_CAFILE`) and re-tagged under the same
  names, so every tutorial build runs unchanged (`laptop/capture-only/{python,node}-base.Dockerfile`
  + build logs). Effects a student will not see: a fresh student build pulls the base layers where
  `21`/`33` show none, and `docker history` would show the extra CA rows. Scenes crop those.
- **The placeholder key.** `secrets/llm-service-account.json` in `05`/`06`/`21` is an obviously
  invalid stand-in (`project_id: "your-gcp-project"`, zeroed ids,
  `PLACEHOLDER-THIS-IS-NOT-A-REAL-KEY` in place of a private key —
  `laptop/capture-only/placeholder-key.json`). It exists so the folder-structure steps can show
  the README's tree. It was moved out before the cloud steps (`capture-only/placeholder-key-moves.txt`),
  so those fail with the *documented* missing-file error rather than an undocumented parse error
  on the fake key. Its size (421 B) differs from a real key (~2.3 KB); scenes showing `06`/`21`
  should avoid making the byte size load-bearing. Never show its content as a real key.
- **`your-gcp-project`** is the stand-in project ID written into both `docker-shell.sh` edits
  (`20`, `30`) — deliberately placeholder-looking, per the series rule against real-looking IDs.
- **Readiness probes and stop cues.** The harness waits for each server with a quiet curl loop
  and tells the pty when to Ctrl-C by requesting `/capture-done`; one stray `GET /` access line
  and a `GET /capture-done … 404` line appear in `33` and `51`. Scenes crop them.
- **A sandbox restart between `api2` and `fe1`** (2026-10-19 → 2026-10-20) stopped the capture
  container; it was restarted with its filesystem and inner images intact (a stale containerd pid
  file was replaced first), and the ChromaDB container was started again by hand — which is why
  `54-docker-ps.txt` shows ChromaDB "Created 4 hours ago / Up 2 minutes". A first `fe1`/`fe2`
  attempt before the restart never typed its commands (wrong prompt pattern for the root
  `…:/app#` prompt) and was discarded and re-captured whole; no partial output was kept.
- **The laptop baseline** (bash, git, curl, tree, python3 for `ptyrun.py`, user `student` in the
  `docker` group) is not part of the tutorial; `docker:dind` ships the compose plugin like Docker
  Desktop does. `hub_retry` (Docker Hub 429s) was armed but unused — there are no retry logs.

## Differences and findings vs the digest, found while running

- **Digest confirmed live:** gotcha #1 (the api-service script abort, `31`); the chunk counts
  (§2's ~8.2 k / ~14.2 k → 8,248 / 14,228, `27`); the `Womans Institute…` filename truncation
  (gotcha #18, visible in `26`); `CHROMA_CORS_ALLOW_ORIGINS` honored and `/data` persistence
  working on the current `chromadb/chroma:latest` (§10 open question — answered yes for digest
  sha `1e0b73a187a2…`, API version string `"1.0.0"`; the tag is unpinned, so this can drift);
  `GET /api/v2/version` and the v2 collections route exist (`23`, `63`).
- **Digest §4's lazy-auth claim is right:** `genai.Client(vertexai=True, …)` constructs without
  credentials; uvicorn starts cleanly with an empty `/secrets`, and the `DefaultCredentialsError`
  surfaces per-request as a 500 in the debug log (`33`, `37`) — not at startup. Likewise the CLI
  imports fine and fails only inside `--embed` (`24`).
- **FastAPI's startup** (`@app.on_event`, §10 open question): `Startup tasks` printed and the
  app ran; **no deprecation warning appeared** in the captured log at this pin.
- **Compose quirk a student also sees:** `docker compose run` first prints
  `Image llm-rag-cli Pulling … pull access denied … Building` before building locally (`21`) —
  harmless, it just means the image isn't on Docker Hub.
- **`docker compose down` outside the wrapper script prints the two "variable is not set"
  warnings** (`70`) — the digest gotcha #5 interpolation mechanism, captured incidentally.
- **The OpenAPI route list** (`36`) carries `GET /` in addition to the README table's five
  `/rag` routes — the table is about `/rag` only, not wrong.
- **npm 10.8.2 deprecation warnings** during `npm install` (`50`) and Next.js's anonymous
  telemetry notice (`51`): real, a student sees them too.

## Versions at the time of recording (2026-10-19/20)

| what | version |
| --- | --- |
| laptop Docker (stand-in for Docker Desktop) | client + engine 29.8.2, compose v5.6.0, buildx, containerd image store, linux/amd64 |
| laptop git | 2.54.0 |
| llm-rag image | base `python:3.12-slim-bookworm` → Python 3.12.15, uv 0.13.2; uv.lock pins: chromadb 1.1.0, google-genai 1.39.1, google-auth 2.41.1, langchain 0.3.27, langchain-text-splitters 0.3.11, pandas 2.3.3 (126 locked packages) |
| api-service image | same base; Pipfile.lock pins: fastapi 0.142.2, uvicorn 0.54.0, google-genai 2.28.0, google-auth 2.60.0, google-cloud-storage 3.16.0 (170 packages) |
| ChromaDB | `chromadb/chroma:latest`, digest `sha256:1e0b73a187a2…` at pull time, `/api/v2/version` → `"1.0.0"` (**unpinned tag** — digest gotcha #17) |
| frontend | `node:20-alpine` → node v20.20.2, npm 10.8.2; Next.js 14.2.4, 773 npm packages |

Things that vary between runs and must be said with "at the time of recording" or cropped:
container ids and hostnames in prompts (`app@3c41bc0606ad`), image digests and sizes, build/pull
timings (`✓ Ready in 1648ms`, `added 773 packages in 1m`), the ChromaDB image digest and its
`"1.0.0"` version string, npm's "new major version" notice, dates in HTTP headers, and the
ChromaDB uptime in `54` (restart note above). The chunk counts (8,248 / 14,228) are deterministic
for this pin of the books and `langchain-text-splitters` 0.3.11.

## Re-running the captures

```
export HTTPS_PROXY=http://127.0.0.1:<port>  CA_BUNDLE=<proxy CA bundle>   # sandbox only
bash assets/terminal/capture.sh laptop setup
bash assets/terminal/capture.sh laptop pre net rag1 rag2 rag3 rag4 api1 api2 fe1 fe2 cors down
bash assets/terminal/capture.sh laptop teardown
docker rm -f l10-relay
```

Needs Docker with privileged containers. The container persists between segment calls, so a long
capture can run in parts; a re-run of a segment overwrites only that segment's files. Segment
order matters (`rag1` leaves ChromaDB running for everything through `cors`; `api1` must precede
`api2`). Without `HTTPS_PROXY`/`CA_BUNDLE` the capture-only parts (relay, CA, base re-tags,
hub retries) are skipped.

## Gate

Every command of the cheese-app-v0 README has a capture above, exactly as written, in README
order: the clone, the network command, both `docker-shell.sh` runs with their in-container
commands (`python cli.py …` ×2, `uvicorn_server`, `npm install`, `npm run dev`), and
`docker compose down`. The README lines without a live capture each have a documented reason and
source: the GCP console steps 1-6 (browser → `illustration`, field values from README:46-56), the
two `GCP_PROJECT` edits and the `rag.py:22` endpoint edit (editor actions; the edits/lines are
captured or snapshotted), the five "Go to http://localhost:3200/…" browser steps (server-side
half captured in `52`-`58`, flows from `source/`, UI as `illustration`), the Vertex-dependent
outputs (`recorded` from README text and the code's own prints, as listed), and the optional L05
tutorial (out of scope). The cloud steps are captured to their honest, documented failure; no
output was invented. Capture-only logs live under `laptop/capture-only/`.
