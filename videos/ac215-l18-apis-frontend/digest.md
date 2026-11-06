# L18 · APIs + Frontend — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166043/ (not readable from here. This digest is built from the repos, the live course site and the lecture slides.)
- **Course-site map.** The tutorials page (`harvard-iacs.github.io/2026-AC215/tutorials_demo/`, fetched live 2026-11-05) lists four tutorials for L18: "Frontend and FastAPI" (cheese-app-v1, repo root), "Backend and FastAPI" (v2 `#tutorial-23-backend-apis`), "Frontend Simple" (v2 `#tutorial-24-simple-frontend-app`) and "Frontend React" (v2 `#tutorial-25-react-frontend-setup`). All three v2 links point at the repo's default branch, `main`.
- **Verified 2026-11-05 with `git ls-remote`:**
  - `dlops-io/cheese-app-v1`: `main` = `ce03a1029dd6f655a86e3e3edc99bb5938f0cbf8` (2025-11-02 07:33:53 -0500, "gitignore"), unchanged. Also `pipenv` = `348d00107784dc023377ddfec0f5c9fa468ed2c2` (pre-`uv` snapshot, not used).
  - `dlops-io/cheese-app-v2`: `main` = **`e98fa551c5d380517c6dc775ae626ea1a828e4d3`** (2026-11-05 07:23:43 -0500, "Merge pull request #1 from dlops-io/work/shivas"; its four commits, 2026-10-31: `17c58df` "code cleanup", `a9fef93` "Update code", `5104923` "removed frontend simple", `3b9a2d1` "upgraded vector-db"). The old main is preserved as branch **`2025`** = `14f2a1420b43e9f24e977a9e67b53d7e2614013d` (2025-11-16 09:16:15 -0500, "image chat fix"), the commit `units.json` names. Also `pipenv` = `adaa2acd…`, `work/shivas` = `3b9a2d1…`.
- **Pin decision (what the course points students to today).** The course site links `main`, so the default is HEAD `e98fa55`. HEAD still has the README sections "Tutorial (23): Environment Setup / Vector DB for RAG Setup / Backend APIs" and "Tutorial (25): React Frontend Setup" (`cheese-app-v2/README.md:25`, `:57`, `:86`, `:152`), so **Tutorial 23 and Tutorial 25 follow HEAD `e98fa55`**. HEAD **dropped "Tutorial (24): Simple Frontend App"** and the whole `src/frontend-simple/` folder (commit `5104923`), yet the lecture teaches it (L18b slides 18-23 walk through `cheese-app-frontend-simple:8080` and `http-server`; slide 28 is "Tutorial: Frontend Simple") and the course site still links its now-dead anchor. So **Tutorial 24 is pinned to `14f2a14` (branch `2025`)**. Because the 2025 simple frontend calls 2025 routes (`http://localhost:9000/newsletters`, `/llm/chats/`, CORS) that HEAD's API no longer serves (HEAD has `/api/...` and no CORS), Tutorial 24 must run against the **2025 API too**: a whole 2025 stack (vector-db + api-service + frontend-simple at `14f2a14`). The published exam edition `videos/ac215-l16-exam/` quotes `14f2a14`, consistent with this.
- **Path notation in this digest:** `cheese-app-v1/…` = v1 @ `ce03a10`; `cheese-app-v2/…` = v2 @ `e98fa55` (HEAD); `cheese-app-v2@2025/…` = v2 @ `14f2a14` (branch `2025`). Every `path:line` was checked with `sed -n` at that commit.
- **Repos cited only for context:** `dlops-io/cheese-app-v0` `main` `cb6fb94576aa37bb0b94a8745e5e94e6a504f4bb` (2026-10-08; the L10 app). `dlops-io/cheese-app-v3` `main` `3ecef56fea879ac480d260c0906cd95baf05179a` (2025-11-28; still the 2025 edition; an unmerged branch `work/shivas` = `976c4bb…` exists, not inspected). `dlops-io/ml-workflow` `main` `37300090aa6c75581f713a48ff21d21f7b0916f0` (2026-10-27; L15, creates the `ml-workflow.json` key).
- **README sections covered:**
  - `cheese-app-v1/README.md`: the whole file (Prerequisites, Setup Environments, Backend API Container, View API Docs, Frontend App (Simple) Container, Docker Cleanup).
  - `cheese-app-v2/README.md` @ HEAD: the intro table, Prerequisites, Tutorial (23) Environment Setup, Vector DB for RAG Setup, Backend APIs, Tutorial (25) React Frontend Setup, Production images, Troubleshooting, Docker Cleanup. HEAD's README has no "Tutorial (24)" heading at all; its three "Tutorial (23)" H2s are at `:25`, `:57`, `:86`. The README numbers (23/24/25) are tutorial numbers, not lecture numbers.
  - `cheese-app-v2@2025/README.md`: `## Tutorial (24): Simple Frontend App` (`:147-183`), plus the 2025 Vector DB and Backend sections it depends on (`:40-145`).
- **Colab notebooks:** none for L18.

---

## 1. What you build

You build the full-stack skeleton of "Formaggio", the cheese app, in Docker on your laptop, in three passes.

- **v1** (`ce03a10`) is the minimum. One Python container runs a FastAPI app under `uvicorn` on port 9000, and one Node container serves static HTML/JS on 8080 with `http-server`. You add a route (`/square_root/`) and watch it appear in `/docs`. The v1 page never calls the API (its podcasts are hard-coded).
- **v2 HEAD** (`e98fa55`) is the real multi-service app, four containers on one Docker network `cheese-app-network` (`cheese-app-v2/README.md:3-10`). A **vector-db** stack (Compose) starts Chroma (`chromadb/chroma:1.5.9`) on 8000 and a CLI container that downloads pre-computed cheese-book embeddings into the collection `recursive-split-collection`. The **api-service** serves content (`/api/newsletters`, `/api/podcasts`) and three chat modes built from one router factory (`/api/llm` "Ask", `/api/llm-cnn` "Identify", `/api/llm-rag` "Cheese books"), plus `/healthz`, `/readyz` and docs at `/api/docs`. It calls Gemini on Vertex AI (`gemini-3.8-flash`, `location="global"`), Chroma by container name, and a TensorFlow CNN it downloads in a background thread at start-up. The **frontend-react** dev container runs **Vite** (React 19 + React Router, no Next.js) on container port 5173, published as host 3000. The page only ever calls relative `/api/...` on its own origin, and **the Vite dev server inside the frontend container forwards `/api` to `http://cheese-app-api-service:9000` over the Docker network**. So the browser talks to one origin and the API needs no CORS (`cheese-app-v2/docs/contract.md:6-7`). In production, nginx plays Vite's role.
- **v2 2025** (`14f2a14`, only for Tutorial 24) is the older design: the browser JS calls `http://localhost:9000` directly through the published port, and the API allows it with `CORSMiddleware(allow_origins=["*"])`. The simple frontend (`http-server`, 8080) is a different origin from the API, which is exactly why CORS exists in that code.

```text
 YOUR LAPTOP (host OS + Docker)  — v2 HEAD e98fa55                              GOOGLE CLOUD
 =============================================================================  ======================
  BROWSER (on the host)                                                          Vertex AI, location global
   http://localhost:3000/chat?model=llm                                          gemini-3.8-flash
     | (1) GET page + JS from :3000                                              text-embedding-004 (256-d)
     | (2) fetch('/api/llm/chats') — SAME origin :3000, header X-Session-ID              ^
     v                                                                                   | (5) HTTPS, OAuth token from
 ---- published ports -p HOST:CONTAINER ------------------------------------------------|---- /secrets/ml-workflow.json
   3000:5173                                9000:9000 (also reachable directly:         |
     |                                       /api/docs, /healthz, /readyz)              |
 +---v-------------------------------+   +-----v----------------------------------------+-+
 | cheese-app-frontend-react         |   | cheese-app-api-service                         |
 | node:24.22.1-bookworm-slim, user  |   | python:3.13-slim-bookworm, user app (uid 1000) |
 |  node; `npm run dev` = vite :5173 |   | `api_server` -> uvicorn api.service:app        |
 | /app <- src/frontend-react (bind) |   |   --host 0.0.0.0 --port 9000 --reload          |
 | /app/node_modules <- named volume |   | /app <- src/api-service (bind)                 |
 | (3) Vite proxy: /api ->           |-->| /secrets <- ../../../secrets (read-only)       |
 |  http://cheese-app-api-service:9000   | /persistent <- ../../../persistent-folder      |
 | net: cheese-app-network           |   |   chat-history/<mode>/<session>/<chat>.json    |
 +-----------------------------------+   |   experiments/ (CNN .keras, from github.com)   |
                                          | net: cheese-app-network                        |
                                          +----------------------+-------------------------+
                                                                 | (4) HTTP cheese-app-vector-db:8000
          docker compose (src/vector-db)                         v      (Docker DNS, container name)
 +-----------------------------------------+  (0) load  +------------------------------------------+
 | cheese-app-vector-db-cli (one-off)      |----------->| cheese-app-vector-db  chromadb/chroma:1.5.9|
 | python cli.py --download --load         |  HTTP 8000 | published 8000:8000                      |
 |   --chunk_type recursive-split          |            | ./docker-volumes/chromadb:/data          |
 | /app <- src/vector-db, /secrets (ro)    |            | collection "recursive-split-collection"  |
 | (0a) cheese-books-embeddings.zip, GitHub|            | net: cheese-app-network (external)       |
 +-----------------------------------------+            +------------------------------------------+
```

The numbered flows: (0) you load the vector DB once. (1) the browser fetches the page and JS from the Vite dev server. (2) the page calls `/api/...` on its own origin. (3) Vite, a Node process inside the frontend container, forwards the call to the API by container name. (4) on a "Cheese books" question the API embeds the question and queries Chroma by container name. (5) every text answer calls Gemini (a photo sent in "Identify" mode goes only to the local CNN).

For Tutorial 24 (2025 stack) replace the left half: a `cheese-app-frontend-simple` container (`node:20-alpine` + `http-server`, `8080:8080`, default bridge, no network) only serves files; the browser's axios calls go straight to `http://localhost:9000` (cross-origin, CORS), and the API listens at `/newsletters`, `/llm/chats`, … without the `/api` prefix.

---

## 2. Prerequisites and costs

**Accounts**
- A GCP project with billing and the **Vertex AI API** enabled. You need it only for chat answers and `cli.py --chat`. Newsletters, podcasts, `/api/square_root`, `/healthz`, the CNN "Identify" reply and all of v1 work without GCP (you still need internet for the image builds, the CNN download and the embeddings zip).
- No cloud resources are created. HEAD no longer passes the unused `GCS_BUCKET_NAME` that the 2025 scripts set (`cheese-app-v2@2025/src/api-service/docker-shell.sh:12`).

**Local installs**
- Docker Desktop (macOS/Windows) or Docker Engine with the **compose plugin**: HEAD's vector-db script calls `docker compose` (`cheese-app-v2/src/vector-db/docker-shell.sh:17`). The 2025 script still calls the hyphenated `docker-compose` (`cheese-app-v2@2025/src/vector-db/docker-shell.sh:20`).
- Ports 3000, 8000 and 9000 free (`cheese-app-v2/README.md:19`), plus 8080 for the production-image step and for Tutorial 24.
- About 10 GB of free disk (`cheese-app-v2/README.md:23`). The API image installs `tensorflow-cpu==2.21.0` on x86_64 and `tensorflow==2.21.0` on aarch64 (`cheese-app-v2/src/api-service/pyproject.toml:13-14`). No host Python or Node is needed.
- The HEAD README runs `./docker-shell.sh`; the three scripts are committed executable (mode 100755). `sh docker-shell.sh` also works.

**Folder layout the scripts assume** (`cheese-app-v2/README.md:30-50`). `docker-shell.sh` in `src/api-service` resolves `$(pwd)/../../../secrets/` and `…/persistent-folder/` (`cheese-app-v2/src/api-service/docker-shell.sh:7-8`), and the vector-db compose file mounts `../../../secrets` (`cheese-app-v2/src/vector-db/docker-compose.yml:10`). Both point *next to* the repo folder:

```text
AC215/                      <- e.g. ~/Desktop/AC215
  cheese-app-v1/
  cheese-app-v2/            (main = e98fa55; `git switch 2025` for Tutorial 24)
  secrets/
    ml-workflow.json          <- read by v2 HEAD api-service AND vector-db-cli (and by the 2025 API)
    llm-service-account.json  <- read only by the 2025 vector-db-cli
  persistent-folder/          <- api-service, mounted at /persistent (v1, 2025 and HEAD)
```

**Secrets and environment variables (v2 HEAD):**

| Container | Env var | Value | Set at |
|---|---|---|---|
| api-service | `GOOGLE_APPLICATION_CREDENTIALS` | `/secrets/ml-workflow.json` | `cheese-app-v2/src/api-service/docker-shell.sh:29` |
| api-service | `GCP_PROJECT` | `"ac215-project" # CHANGE TO YOUR PROJECT ID` | `cheese-app-v2/src/api-service/docker-shell.sh:9` |
| api-service | `CHROMADB_HOST` / `CHROMADB_PORT` | `cheese-app-vector-db` / `8000` | `cheese-app-v2/src/api-service/docker-shell.sh:10-11` |
| api-service (defaults, not set by the script) | `GCP_LOCATION`, `GENERATIVE_MODEL`, `EMBEDDING_MODEL`, `PERSISTENT_DIR` | `global`, `gemini-3.8-flash`, `text-embedding-004`, `/persistent` | `cheese-app-v2/src/api-service/api/settings.py:7`, `:10`, `:11`, `:17` |
| vector-db-cli | `GOOGLE_APPLICATION_CREDENTIALS` | `/secrets/ml-workflow.json` | `cheese-app-v2/src/vector-db/docker-shell.sh:7`, passed via `cheese-app-v2/src/vector-db/docker-compose.yml:13` |
| vector-db-cli | `GCP_PROJECT` | `"ac215-project"` | `cheese-app-v2/src/vector-db/docker-shell.sh:6` |
| frontend-react (dev) | `API_URL` (optional) | default `http://cheese-app-api-service:9000` | `cheese-app-v2/src/frontend-react/vite.config.js:13` |
| frontend-react (prod) | `API_URL` | `http://cheese-app-api-service:9000` | `cheese-app-v2/src/frontend-react/Dockerfile:13` |

- One key, one name, at HEAD: "The `ml-workflow.json` service account key from the `ml-workflow` tutorial. The account needs the **Vertex AI User** role." (`cheese-app-v2/README.md:21-22`). L15's `ml-workflow` account has Storage Admin, Vertex AI Administrator and Service Account User (`ml-workflow/README.md:108-112` at `3730009`); Vertex AI Administrator includes everything Vertex AI User grants.
- Secrets are mounted read-only at HEAD (`/secrets:ro`, `cheese-app-v2/src/api-service/docker-shell.sh:26`, `cheese-app-v2/src/vector-db/docker-compose.yml:10`).
- The 2025 stack (Tutorial 24) expects **two** names: the API reads `/secrets/ml-workflow.json` (`cheese-app-v2@2025/src/api-service/docker-shell.sh:29`), the vector-db CLI `/secrets/llm-service-account.json` (`cheese-app-v2@2025/src/vector-db/docker-shell.sh:10`). `--download --load` never calls Vertex, so a missing second file only bites with `--embed`/`--query`/`--chat`.

**Billable resources**
- Only Vertex AI requests. Every Ask/Identify text message is one Gemini call, and the whole saved history is re-sent each time (`cheese-app-v2/src/api-service/api/utils/llm_utils.py:79-84`, `:92-94`), so long chats cost more per message. Each "Cheese books" text message adds one embedding call (`cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:45-54`, `:73`). `cli.py --chat` makes one embedding and one Gemini call. `cli.py --download --load` makes **no** Vertex calls (`cheese-app-v2/src/vector-db/cli.py:473-485`, `:272-311`); `--embed` would bill.
- **Shutting down** (`cheese-app-v2/README.md:229-240`): Ctrl-C and `exit` in the API and frontend shells (both `docker run --rm`), then `docker compose down` in `src/vector-db`, then optionally `docker system prune`. Not covered by the README: the named volume `cheese-app-frontend-react-node_modules` survives `docker system prune` (it removes volumes only with `--volumes`); remove it with `docker volume rm cheese-app-frontend-react-node_modules`. `docker network rm cheese-app-network` is optional. Nothing in the cloud to delete.

---

## 3. Concepts this tutorial teaches

### 3.1 REST: an API is a set of nouns (paths) you act on with verbs (HTTP methods)  **[ANIMATE]**
- **Explanation.** A REST API exposes *resources* at URLs: `/api/newsletters`, `/api/newsletters/{id}`, `/api/llm/chats/{chat_id}`. A client sends a *request* (method, path, query, headers, optional JSON body); the server returns a *response* (status code, headers, body, usually JSON). GET reads, POST creates or acts. At HEAD, `POST /api/llm/chats` *starts* a chat and `POST /api/llm/chats/{chat_id}` *continues* one (`cheese-app-v2/src/api-service/api/routers/chat.py:58-67`, `:69-76`, mounted under `/api/llm` at `cheese-app-v2/src/api-service/api/service.py:38`).
- **Mental model.** A function call over the network. Method + path name the function; query, path and body carry the arguments; the JSON response is the return value. FastAPI makes this literal: `square_root(x, y)` *is* the handler for `GET /api/square_root?x=3&y=4`.
- **Analogy.** A restaurant order slip: table number = path, "add"/"cancel" = method, items = body; the kitchen returns a plate plus a ticket stamped 200 or 404.
- **Status codes carry meaning.** HEAD's API is a good model: `404` for a missing newsletter or chat, `422` for a missing/invalid session id or an empty message, `400` for an unreadable image, `502` when Gemini fails, `503` while the CNN loads or Chroma is down (`cheese-app-v2/docs/contract.md:46-54`). The 2025 code answered an unknown newsletter id with a 500 (`cheese-app-v2@2025/src/api-service/api/routers/newsletter.py:40-42`, unhandled `FileNotFoundError`); HEAD returns 404 (`cheese-app-v2/src/api-service/api/routers/newsletter.py:31-33`).
- **Animation idea.** A request envelope flies from the browser; it splits into method / path / query / headers / body, the parts slot into `square_root(x: float = 1, y: float = 2)`, and `5.0` folds back into a JSON envelope stamped 200.

### 3.2 FastAPI: decorators build a route table, type hints build validation and docs  **[ANIMATE]**
- **Explanation.** `app = FastAPI(...)` (`cheese-app-v2/src/api-service/api/service.py:26-28`) holds a routing table. `@app.get("/api/status")` registers a function under a (method, path) key. An `APIRouter()` is a mini-table; `app.include_router(router, prefix="/api/newsletters")` grafts it in (`cheese-app-v2/src/api-service/api/service.py:36`), so the router's `""` becomes `/api/newsletters` and `"/{newsletter_id}"` becomes `/api/newsletters/{newsletter_id}` (`cheese-app-v2/src/api-service/api/routers/newsletter.py:16`, `:28`). HEAD goes one step further: `chat.create_router(model, respond)` is a *function that builds a router*, called three times with a different `respond` (`cheese-app-v2/src/api-service/api/service.py:38-40`, `cheese-app-v2/src/api-service/api/routers/chat.py:31`). Type hints become validation: `x: float` rejects `?x=abc` with **422**; `limit: int | None = None` is an optional query param; a pydantic `BaseModel` parameter (`ChatMessage`, `cheese-app-v2/src/api-service/api/utils/chat_utils.py:12-14`) means "parse the JSON body"; `Annotated[str, Header(alias="X-Session-ID", pattern=UUID_PATTERN)]` reads a header and requires it to look like a UUID (`cheese-app-v2/src/api-service/api/routers/chat.py:20-21`). FastAPI publishes the table as OpenAPI and serves interactive docs, at HEAD under `/api/docs` and `/api/openapi.json` (`cheese-app-v2/src/api-service/api/service.py:27`).
- **Mental model.** A tree of routes; routers are branches mounted under prefixes; each leaf has a typed signature FastAPI checks before your code runs.
- **Analogy.** A building directory: floor (prefix) → room (path) → door policy (types).
- **Misconception.** "`/newsletters` and `/newsletters/` are the same." They are different routes; Starlette answers the "wrong" one with a **307** redirect. The 2025 simple frontend hits this (§4 C4). HEAD defines `""` routes and the frontend calls exactly `/api/newsletters`, so no redirect (`cheese-app-v2/src/api-service/tests/test_service.py:10-13` asserts it).
- **Animation idea.** Draw the route tree; each `include_router(..., prefix=...)` snaps a sub-tree onto `/api`; one `create_router` "stamp" prints three identical chat sub-trees labelled llm / llm-cnn / llm-rag; then `/api/docs` unfolds from the tree.

### 3.3 ASGI server vs. app: uvicorn, `--host 0.0.0.0`, `--reload`, lifespan, dev vs. prod
- **Explanation.** FastAPI is the *app*, a Python object; **uvicorn** is the *server* that owns the socket, parses HTTP and calls the app. `api.service:app` means "import `api/service.py`, use its variable `app`" (run from `/app`, the WORKDIR). `--host 0.0.0.0` listens on all container interfaces so Docker's port forward reaches it. `--reload --reload-dir api/` restarts the worker whenever a file under `api/` changes. At HEAD the dev shell defines `api_server` (`cheese-app-v2/src/api-service/docker-entrypoint.dev.sh:12-16`); the production image instead runs `uvicorn api.service:app --host 0.0.0.0 --port 9000` as its `CMD`, as uid 1000, with no reload (`cheese-app-v2/src/api-service/Dockerfile:22-24`). (The 2025 code switched between `uvicorn_server` and `uvicorn_server_production` with `DEV=1`, `cheese-app-v2@2025/src/api-service/docker-entrypoint.sh:14-20`, `:32-38`.)
- **Lifespan and readiness.** HEAD's `lifespan` starts a background thread that downloads/loads the CNN (`cheese-app-v2/src/api-service/api/service.py:19-23`), so uvicorn accepts requests immediately. `/healthz` ("is the process up?") always answers `{"ok": true}`; `/readyz` ("can it do its job?") answers 503 until the model is loaded and Chroma answers a heartbeat (`cheese-app-v2/src/api-service/api/service.py:43-56`). These are the liveness/readiness probes Kubernetes uses later (L19/L22).
- **Sync vs. async routes.** HEAD's chat routes are plain `def`, because Gemini, Chroma and the CNN are blocking calls; FastAPI runs a `def` route in a thread pool so one slow answer does not block the event loop (`cheese-app-v2/README.md:142-143`, `cheese-app-v2/src/api-service/api/routers/chat.py:1-7`). An `async def` that called them directly would stall every other request.
- **Mental model.** A receptionist (uvicorn) answers the phone and hands each call to the specialist (your app); with `--reload`, a supervisor swaps in a fresh specialist whenever you edit the manual.
- **Misconception.** "`127.0.0.1` inside the container is my laptop." It is the container's own loopback; a server bound to it cannot be reached through `-p 9000:9000`.

### 3.4 Same-origin policy, CORS, and the proxy that makes CORS unnecessary  **[ANIMATE]**
- **Explanation.** An *origin* is scheme + host + port. A page from `http://localhost:8080` may *send* a request to `http://localhost:9000`, but the browser lets the JS *read* the response only if the server says so with `Access-Control-Allow-Origin`. For "non-simple" requests (a JSON POST, or any request with a custom header like `X-Session-ID`) the browser first sends a **preflight** `OPTIONS`.
  - **v1 and the 2025 stack use CORS.** `CORSMiddleware` with `allow_origins=["*"]`, `allow_methods=["*"]`, `allow_headers=["*"]` answers yes to everything (`cheese-app-v1/src/api-service/api/service.py:8-14`, `cheese-app-v2@2025/src/api-service/api/service.py:15-21`). The 2025 simple frontend's axios instance adds `X-Session-ID` to every chat request (`cheese-app-v2@2025/src/frontend-simple/chat-main.js:16-23`), so chat requests are preflighted; Starlette's preflight reply carries `Access-Control-Max-Age: 600` by default, so the browser reuses it for 10 minutes.
  - **v2 HEAD avoids cross-origin requests altogether.** The page calls relative `/api/...` (`cheese-app-v2/src/frontend-react/src/lib/api.js:1-3`, `:44`), i.e. its own origin `localhost:3000`; the Vite dev server forwards `/api` to the API container (`cheese-app-v2/src/frontend-react/vite.config.js:13`), and in production nginx does (`cheese-app-v2/src/frontend-react/nginx.conf.template:13-19`). There is no `CORSMiddleware` at HEAD (`cheese-app-v2/src/api-service/api/service.py:10-40`): "nothing strips a prefix and the API needs no CORS" (`cheese-app-v2/docs/contract.md:6-7`). That is also why every API route lives under `/api`: the same path must work through Vite, through nginx and on the API itself.
- **Mental model.** CORS is enforced **by the browser, about the server's permission**. `curl` and `/api/docs` (same origin as the API) never see a CORS error. A same-origin proxy sidesteps the question: the browser only ever talks to one origin.
- **Analogy.** A bouncer (the browser) checks a guest list the club (API) publishes. CORS = get on the guest list. Proxy = send a friend who already works inside.
- **Misconception (2025 stack).** "A CORS error means my CORS config is wrong." An unhandled Python exception becomes a 500 sent by Starlette's outermost `ServerErrorMiddleware`, *outside* `CORSMiddleware`, so it carries no CORS header and the browser reports "No 'Access-Control-Allow-Origin' header" (axios: "Network Error"). Check the uvicorn terminal first (example: the RAG follow-up bug, §10). Errors raised as `HTTPException` *are* CORS-stamped.
- **Animation idea.** Take 1 (2025): browser on :8080 → OPTIONS scout to :9000 → green badge → POST. Take 2 (HEAD): browser → :3000 only; inside the frontend box a small "Vite" courier carries the request across the Docker network to the API; no badge needed.

### 3.5 Where code runs, and two meanings of "localhost"  **[ANIMATE]**
- **Explanation.** Inside Docker, containers on the user-defined network `cheese-app-network` reach each other by **container name** through Docker's embedded DNS: the API reaches Chroma at `cheese-app-vector-db:8000` (`cheese-app-v2/src/api-service/api/settings.py:14-15`), and at HEAD the Vite dev server reaches the API at `cheese-app-api-service:9000` (`cheese-app-v2/src/frontend-react/vite.config.js:13`). All three scripts create the network if missing and join it (`cheese-app-v2/src/api-service/docker-shell.sh:14`, `:33`; `cheese-app-v2/src/frontend-react/docker-shell.sh:8`, `:22`; `cheese-app-v2/src/vector-db/docker-compose.yml:1-4`). From the host, the browser reaches containers only through **published ports** (`-p 3000:5173`, `-p 9000:9000`, `8000:8000`).
- **Who calls whom at HEAD.** Browser → `localhost:3000` (published) → Vite in the frontend container → `cheese-app-api-service:9000` (container DNS) → API → `cheese-app-vector-db:8000` (container DNS). The frontend container *does* talk to the API now, server-side, through its proxy. In the 2025 stack it did not: the browser called `localhost:9000` itself, and the simple-frontend container sat on the default bridge serving files only.
- **Mental model.** Each container is its own little machine with its own `localhost`. A Docker network is a private LAN with a phone book of container names. `-p HOST:CONTAINER` drills a hole from the laptop into one container port; the two numbers need not match (`3000:5173`).
- **Analogy.** Apartments in a building: neighbours knock by name (container DNS); visitors from the street use the buzzer number (published port).
- **Misconception.** "Put `http://cheese-app-api-service:9000` in the browser code." The browser runs on the laptop and resolves names with the laptop's DNS, which knows no container names. Container names only work in code that runs inside a container on the network: Vite's proxy, nginx, the API itself.
- **Animation idea.** Zoom out from a laptop to reveal boxes, each with its own floating "localhost" label. The request leaves the tab, enters through buzzer 3000, a courier inside the frontend box looks up "cheese-app-api-service" in the phone book drawn on the network cable, walks to the API box, which looks up "cheese-app-vector-db".

### 3.6 Stateless HTTP and where chat state lives
- **Explanation.** HTTP forgets each request. At HEAD chat state lives in exactly two places: (1) the browser keeps a session id in `localStorage` and sends it as `X-Session-ID` on every request (`cheese-app-v2/src/frontend-react/src/lib/api.js:5`, `:17-29`, `:34`); (2) the API writes each chat as JSON under `/persistent/chat-history/<mode>/<session_id>/<chat_id>.json` and each photo as a file under `…/<mode>/images/<chat_id>/<message_id>.png` (`cheese-app-v2/src/api-service/api/utils/chat_utils.py:28-36`, `:49-60`). **Nothing about a chat stays in memory**: every message reloads the chat file and rebuilds the Gemini history from it (`cheese-app-v2/src/api-service/api/routers/chat.py:35-43`, `:72`; `cheese-app-v2/src/api-service/api/utils/llm_utils.py:54-76`), "so any copy of the API can answer it. We need that when we scale in `cheese-app-v3`" (`cheese-app-v2/README.md:140-141`).
- **Contrast with 2025.** The 2025 API cached live Gemini `Chat` objects in a process-local dict `chat_sessions` (`cheese-app-v2@2025/src/api-service/api/utils/llm_utils.py:47`) and rebuilt only on a cache miss; the 2025 simple frontend made a new `uuid()` per page load (`cheese-app-v2@2025/src/frontend-simple/chat-main.js:14`), so a reload started a new, empty history.
- **The session id is not a login.** Anyone who knows (or guesses) a UUID can read that session's chats; HEAD only enforces the UUID *shape*, which also stops path tricks like `../` in file paths (`cheese-app-v2/src/api-service/api/routers/chat.py:19-23`; tested in `cheese-app-v2/src/api-service/tests/test_chat.py:19`).
- **Mental model.** The disk is the source of truth; the header is your locker key.

### 3.7 Frontends: DOM scripting vs. React components in a Vite single-page app  **[ANIMATE]**
- **Explanation.**
  - The simple frontend (v1, 2025) is plain files: `newsletters.html` loads axios from a CDN and `newsletters-main.js` fetches JSON and string-builds `innerHTML` cards (`cheese-app-v2@2025/src/frontend-simple/newsletters-main.js:24-49`).
  - HEAD's React app is a **Vite** project with **React Router** (`cheese-app-v2/src/frontend-react/package.json:7`, `:18-21`). `index.html` has one `<div id="root">` and loads `src/main.jsx` (`cheese-app-v2/src/frontend-react/index.html:11-12`). `main.jsx` declares the URL → component table: `/` Home, `/chat`, `/newsletters`, `/newsletters/:id`, `/podcasts`, `*` NotFound, all nested in `<App />` (`cheese-app-v2/src/frontend-react/src/main.jsx:13-28`). `App.jsx` draws the header and footer once and renders the current page in `<Outlet />` (`cheese-app-v2/src/frontend-react/src/App.jsx:15-66`), which is the slides' "header defined only once". Pages hold state with `useState`, fetch in `useEffect` (`useGet`, `cheese-app-v2/src/frontend-react/src/lib/useGet.js:5-19`), and every API path lives in `src/lib/api.js`.
  - Unlike the 2025 Next.js app there is no server rendering, no `'use client'`, no `NEXT_PUBLIC_*` env vars: the browser gets static JS, and the only address in the code is the relative `/api`.
- **Mental model.** `UI = f(state)`: a fetch updates state, React re-renders. Navigation between pages happens in the browser (client-side routing); the server only ever sends `index.html` plus the bundle, which is why nginx falls back to `index.html` for unknown paths (`cheese-app-v2/src/frontend-react/nginx.conf.template:28-32`).
- **Analogy.** The simple site is a hand-painted poster you repaint for each change; React is a scoreboard wired to the score.
- **Animation idea.** The route table in `main.jsx` morphs into a URL bar; the header box stays put while the `<Outlet />` window swaps Home → Chat → Podcasts.

### 3.8 The container dev loop: bind mounts + hot reload, and what goes in a production image
- **Explanation.** Each dev container mounts its source over `/app` (`cheese-app-v2/src/api-service/docker-shell.sh:25`, `cheese-app-v2/src/frontend-react/docker-shell.sh:19`, `cheese-app-v2/src/vector-db/docker-compose.yml:11`), so edits on the host are instantly visible; uvicorn `--reload` and Vite's HMR pick them up. Dependencies stay out of the bind mount: the API's venv is baked into the dev image at `/home/app/.venv` (`cheese-app-v2/src/api-service/Dockerfile.dev:6`, `:17-18`), and the frontend's `node_modules` lives in a **named volume** mounted over `/app/node_modules` (`cheese-app-v2/src/frontend-react/docker-shell.sh:20`), installed by the entrypoint on each start (`cheese-app-v2/src/frontend-react/docker-entrypoint.dev.sh:10`). Each dev entrypoint also runs `uv sync --frozen` / `npm install` on start, so a changed lock file is picked up without a rebuild (`cheese-app-v2/src/api-service/docker-entrypoint.dev.sh:8-9`).
- **Production images** hold only what runs: the API's two-stage `Dockerfile` copies a venv and `api/`, `news-letters/`, `podcasts/`, runs as uid 1000 (`cheese-app-v2/src/api-service/Dockerfile:3-24`); the frontend's builds `dist/` with Node and serves it from `nginx:1.31.8-alpine` with no Node at all (`cheese-app-v2/src/frontend-react/Dockerfile:3-16`).
- **Misconception.** "Rebuild the image after every code change." In dev you rebuild only when the Dockerfile changes; in prod, every change is a new image.

---

## 4. Step-by-step walkthrough

### Part A — cheese-app-v1 ("Frontend and FastAPI", `ce03a10`)

**A0. Clone, then create the sibling folders.**
- Clone `dlops-io/cheese-app-v1` (`cheese-app-v1/README.md:17-18`). From the folder that contains it, `mkdir -p secrets persistent-folder`. The README asks only for `secrets` (`cheese-app-v1/README.md:22`), but its tree and the script also use `persistent-folder` (`cheese-app-v1/README.md:34`, `cheese-app-v1/src/api-service/docker-shell.sh:10`).
- Under the hood: `docker run -v` with a missing host path makes Docker create it, **root-owned on Linux**, where the container user `app` (uid 1000) cannot write. Harmless in v1 (nothing writes), it matters in v2 (§6).

**A1. Build and enter the API container.**
- Command (`cheese-app-v1/README.md:44`): `sh docker-shell.sh`, run **from `cheese-app-v1/src/api-service`**. The README says "`cheese-app-v1/api-service`" (`cheese-app-v1/README.md:41`), without `src/`.
- Under the hood (`cheese-app-v1/src/api-service/docker-shell.sh:13-21`): `docker build -t cheese-app-api-service` from `FROM python:3.12-slim-bookworm` (`cheese-app-v1/src/api-service/Dockerfile:2`); installs `uv`, creates user `app` uid 1000 (`:30`), copies `pyproject.toml uv.lock*` and runs `uv sync --frozen` into `/home/app/.venv` (`:17`, `:39-42`). `docker run --rm -ti` mounts `.`→`/app`, `../../../secrets/`→`/secrets`, `../../../persistent-folder/`→`/persistent`, publishes `-p 9000:9000`. The entrypoint activates the venv and `exec /bin/bash` (`cheese-app-v1/src/api-service/docker-entrypoint.sh:11-14`).
- Checkpoint: `Container is running!!!`, `Architecture: aarch64` or `x86_64`, the Python and uv versions, a prompt `app@<id>:/app$`.
- If it fails: `Conflict. The container name "/cheese-app-api-service" is already in use` → v1, 2025 and HEAD all use this name; `docker ps`, `docker stop cheese-app-api-service`. `port is already allocated` → something else holds 9000 (e.g. L10's API).

**A2. Start uvicorn.**
- Command (`cheese-app-v1/README.md:47`): `uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"`. The trailing `"$@"` was copied from a script and expands to nothing when typed.
- Checkpoint: `Uvicorn running on http://0.0.0.0:9000 (Press CTRL+C to quit)`, `Started reloader process [...] using StatReload` (v1's lock has no `watchfiles`), `Application startup complete.`. `http://localhost:9000/` returns `{"message":"Welcome to AC215"}` (`cheese-app-v1/src/api-service/api/service.py:18-20`).

**A3. Add a route and watch reload.**
- Append to `api/service.py` (`cheese-app-v1/README.md:52-58`):
  ```
  @app.get("/square_root/")
  async def square_root(x: float = 1, y: float = 2):
      z = x**2 + y**2
      return z**0.5
  ```
- Checkpoint: the reloader logs the change and restarts the worker. `http://localhost:9000/square_root/` → `2.23606797749979` (√5); `?x=2&y=10` → `10.198039027185569` (√104); `?x=abc` → 422; `/square_root` (no slash) → 307 redirect to `/square_root/`.
- If it fails: an `IndentationError` in the uvicorn terminal; fix and save, it reloads.

**A4. Explore `/docs`** (`cheese-app-v1/README.md:64-67`): `http://localhost:9000/docs` lists `GET /` and `GET /square_root/`, with `x`, `y` as `number` query params, defaults 1 and 2; "Try it out" → Execute.

**A5. Simple frontend container.**
- In a **second terminal**: `cd cheese-app-v1/src/frontend-simple` (README says `cheese-app-v1/frontend-simple`, `cheese-app-v1/README.md:75`), `sh docker-shell.sh` (`:78`), then `http-server` (`:82`).
- Under the hood: `node:20-alpine` + bash + global `http-server` (`cheese-app-v1/src/frontend-simple/Dockerfile:1-7`); the script mounts the folder at `/app` and publishes `8080:8080` (`cheese-app-v1/src/frontend-simple/docker-shell.sh:18-20`).
- Checkpoint: `http://localhost:8080/` shows "🧀 Formaggio.me is here!" and two podcast cards that are **hard-coded** ("Sample Podcast Data (This would normally come from an API)", `cheese-app-v1/src/frontend-simple/main.js:37-52`). The v1 page does not call the API.
- Edit `index.html` (`cheese-app-v1/README.md:86-95`) and refresh. The README's snippet is a bare `<body>` from an older template; add a `<p>` inside the existing hero section (`cheese-app-v1/src/frontend-simple/index.html:41-44`) instead of replacing the body, which would also drop `<script src="main.js">` (`:74`). If the change does not show, `http-server` caches for 3600 s by default: hard-refresh, or restart with `http-server -c-1`.
- `http-server` also prints a `172.17.x.x` address: the container IP, not reachable from macOS/Windows. Use `localhost`.

**A6. Clean up** (`cheese-app-v1/README.md:100-106`): exit both shells, then `docker container ls`, `docker system prune`, `docker image ls`.

### Part B — cheese-app-v2 HEAD `e98fa55`: Tutorial (23) Environment, Vector DB, Backend APIs

**B0. Clone, folders, project id** (`cheese-app-v2/README.md:25-55`).
- Clone `dlops-io/cheese-app-v2` next to v1 (`:27-28`). (An existing clone from 2025: `git pull` on `main`.)
- Next to it, `secrets/` with `ml-workflow.json`, and `persistent-folder/` (`:32-36`). Create both yourself (Linux, §6 #5).
- Set `GCP_PROJECT` in **both** `src/api-service/docker-shell.sh` and `src/vector-db/docker-shell.sh` (`:52-55`; the lines are `cheese-app-v2/src/api-service/docker-shell.sh:9` and `cheese-app-v2/src/vector-db/docker-shell.sh:6`).
- Checkpoint: `ls ../secrets` (from `cheese-app-v2`) lists `ml-workflow.json`.

**B1. Vector DB** (`cheese-app-v2/README.md:57-84`).
- Commands: `cd src/vector-db`, `./docker-shell.sh`, then inside `python cli.py --download --load --chunk_type recursive-split`.
- Under the hood:
  - `docker-shell.sh` creates `cheese-app-network` if missing (`cheese-app-v2/src/vector-db/docker-shell.sh:11`), builds `cheese-app-vector-db-cli` (`:14`; `python:3.13-slim-bookworm`, uv, user `app`, deps baked in, `cheese-app-v2/src/vector-db/Dockerfile:1-20`) and runs `docker compose run --rm cheese-app-vector-db-cli` (`cheese-app-v2/src/vector-db/docker-shell.sh:17`).
  - Compose first starts the dependency `chromadb` (`cheese-app-v2/src/vector-db/docker-compose.yml:17-18`): `chromadb/chroma:1.5.9` ("the same version as chromadb-client"), container `cheese-app-vector-db`, `8000:8000`, data in `./docker-volumes/chromadb:/data` (`:19-27`). Both services join the external `cheese-app-network` (`:1-4`).
  - The CLI entrypoint prints the banner and the three suggested commands, then opens bash (`cheese-app-v2/src/vector-db/docker-entrypoint.sh:13-24`; with arguments it would `exec python "$@"` instead, `:9-11`).
  - `--download` fetches `github.com/dlops-io/datasets/releases/download/v4.0/cheese-books-embeddings.zip` into `outputs/` and `extractall()`s it into `/app` (`cheese-app-v2/src/vector-db/cli.py:473-485`). Every entry starts with `outputs/`, so it unpacks to `/app/outputs/` (11 `chunks-recursive-split-*.jsonl` + 11 `embeddings-recursive-split-*.jsonl`), visible on the host in `src/vector-db/outputs/` (git-ignored, `cheese-app-v2/src/vector-db/.gitignore:5`). (Zip listing verified in October against the same URL.)
  - `--load` connects with `chromadb.HttpClient`, deletes and recreates `recursive-split-collection` with cosine distance (`cheese-app-v2/src/vector-db/cli.py:279-294`), then inserts every `outputs/embeddings-recursive-split-*.jsonl` in batches of 500 (`:297-310`, `:129-164`).
- Checkpoint: `Created new empty collection 'recursive-split-collection'`, `Number of files to process: 11`, then per file `Processing file: …`, `Shape: …`, repeated `Inserted N items...` and `Finished inserting N items into collection 'recursive-split-collection'`. The per-file counts add up to 14,356 chunks (largest: *The Book of Cheese*, 3,569; counted from the zip in October). README: "about a minute" (`cheese-app-v2/README.md:75-76`).
- **Step 3 (new at HEAD):** `python cli.py --chat --chunk_type recursive-split` (`cheese-app-v2/README.md:78-81`). It ignores any typed question: it always asks the fixed query "How is cheese made?", prints the query embedding, the top-10 Chroma results and the prompt, then `LLM Response: …` from `gemini-3.8-flash` on `location="global"` (`cheese-app-v2/src/vector-db/cli.py:369-404`, `:27`, `:31`). Needs the key and project id. Capture note: the printed `Results:` include chunk metadata, and one book's metadata names the course instructor (`cheese-app-v2/src/vector-db/cli.py:76`); mask as ‹instructor› in any capture.
- Step 4: `exit`. **Chroma keeps running** (`docker ps` shows `cheese-app-vector-db`), data in `src/vector-db/docker-volumes/chromadb` (`cheese-app-v2/README.md:83-84`).
- If it fails: `Bind for 0.0.0.0:8000 failed` → another Chroma (L10's, or the 2025 stack's) is up. `Number of files to process: 0` → `--download` failed or you are not in `/app`.

**B2. API service** (`cheese-app-v2/README.md:86-108`).
- Commands, in a new terminal: `cd src/api-service`, `./docker-shell.sh` (first build "takes a few minutes, because of TensorFlow"), then inside `api_server`.
- Under the hood:
  - The script creates the network if missing (`cheese-app-v2/src/api-service/docker-shell.sh:14`). **If a container named `cheese-app-api-service` is already running it just `docker exec`s a shell into it** (`:16-18`). Otherwise it builds from `Dockerfile.dev` (`:21`) and runs with the code/secrets(ro)/persistent mounts, `-p 9000:9000`, the credentials, project and Chroma env vars, and `--network cheese-app-network` (`:24-34`).
  - `Dockerfile.dev`: `python:3.13-slim-bookworm`, `uv==0.13.6`, user `app` uid 1000, `uv sync --frozen` into `/home/app/.venv` at build time (`cheese-app-v2/src/api-service/Dockerfile.dev:1-18`).
  - The entrypoint prints the banner, re-runs `uv sync --frozen`, activates the venv, defines and exports `api_server` = `uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload --reload-dir api/ "$@"`, lists the commands (`api_server`, `pytest`) and `exec /bin/bash` (`cheese-app-v2/src/api-service/docker-entrypoint.dev.sh:3-27`). No `DEV` switch, no `--log-level debug`.
  - On import, nothing heavy happens: settings are read (`GCP_PROJECT` is required, `cheese-app-v2/src/api-service/api/settings.py:5`), the genai client object is created (`cheese-app-v2/src/api-service/api/utils/llm_utils.py:15`), TensorFlow is imported only inside the CNN functions (`cheese-app-v2/src/api-service/api/utils/llm_cnn_utils.py:1-5`, `:27`), and the Chroma client is created on first use (`cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:38-42`). The lifespan thread then downloads `experiment_1760994796.zip` from `github.com/dlops-io/models/releases/download/v4.0/` into `/persistent/experiments` (first start only) and loads `mobilenetv2_train_base_True.keras` (`cheese-app-v2/src/api-service/api/settings.py:21-23`, `cheese-app-v2/src/api-service/api/utils/llm_cnn_utils.py:26-42`).
- Checkpoint (`cheese-app-v2/README.md:105-108`): `Uvicorn running on http://0.0.0.0:9000`, `Started reloader process [...] using StatReload` (HEAD's lock has no `watchfiles`), `Application startup complete.` almost at once. `http://localhost:9000/healthz` → `{"ok":true}`. `http://localhost:9000/readyz` → `503 {"detail":"CNN model is loading"}` until the model is loaded (first time: download + TensorFlow import), then `{"ok":true}` if Chroma answers.
- If it fails: `KeyError: 'GCP_PROJECT'` → you ran uvicorn outside the container. `/readyz` → `503 {"detail":"Chroma: …"}` → B1's Chroma is down; `docker compose up -d chromadb` in `src/vector-db` (`cheese-app-v2/README.md:222`). `/readyz` stuck on "CNN model is loading" with a traceback in the log → the thread failed (no internet, or Linux permissions on `persistent-folder`, §6 #5).

**B3. Demo route** (`cheese-app-v2/README.md:110-120`).
- Add after `get_status` in `api/service.py` and save:
  ```python
  @app.get("/api/square_root")
  def square_root(x: float = 1, y: float = 2):
      z = x**2 + y**2
      return z**0.5
  ```
- Checkpoint: the worker reloads (and the lifespan reloads the CNN from `/persistent`, so `/readyz` is briefly 503 again). `http://localhost:9000/api/square_root` → `2.23606797749979`; `?x=3&y=4` → `5.0`. The route is *not* already in HEAD's `service.py` (unlike `14f2a14`, which shipped `/square_root/` pre-added, `cheese-app-v2@2025/src/api-service/api/service.py:30-33`).

**B4. API docs** (`cheese-app-v2/README.md:122-125`).
- `http://localhost:9000/api/docs` (not `/docs`, which is now a 404). Title "Cheese App API". Operations: `GET /api/status`, `GET /api/newsletters`, `/api/newsletters/{newsletter_id}`, `/api/newsletters/image/{image_name}`, the three podcast routes, and for each of `llm`, `llm-cnn`, `llm-rag`: `GET/POST …/chats`, `GET/POST …/chats/{chat_id}`, `GET …/images/{chat_id}/{message_id}.png`, plus `/healthz`, `/readyz` (and `/api/square_root` if added).
- Try `GET /api/newsletters` with `limit=2`: two objects, newest `dts` first (`cheese-app-v2/src/api-service/api/routers/newsletter.py:16-25`).
- `GET /api/podcasts/audio/9f2b7e84-5623-4029-bcfd-f99f2d7611e8-EN.mp3` → 200 `audio/mpeg` (`cheese-app-v2/src/api-service/api/routers/podcast.py:38-44`).
- Chat routes in `/api/docs`: fill **`X-Session-ID` with a UUID** (any v4 UUID). Missing or non-UUID → 422 before any Gemini call (`cheese-app-v2/src/api-service/api/routers/chat.py:20-21`). An empty body `{}` → 422 "Message must contain text or an image" (`:36-37`).

**B5. Review the code and run the tests** (`cheese-app-v2/README.md:127-150`).
- The README's file table (`:128-137`) matches the tree; §5 walks through it. Its two notes: chats are rebuilt from saved history per message (stateless), and the routes are plain `def` (thread pool) (`:139-143`).
- `pytest` inside the container (`:145-148`): 26 tests (`tests/test_service.py` 9, `tests/test_chat.py` 17). They need no GCP and no Chroma: `conftest.py` sets a fake `GCP_PROJECT` and a temp `PERSISTENT_DIR` before importing the app and monkeypatches `ask_gemini`, the CNN and Chroma (`cheese-app-v2/src/api-service/tests/conftest.py:11-50`); `TestClient` without a `with` block skips the lifespan, so the real CNN never loads (`:19-22`). pytest's cache goes to `$HOME/.cache/...` to stay off the bind mount (`cheese-app-v2/src/api-service/pyproject.toml:30-34`).
- "Keep this container running" (`cheese-app-v2/README.md:150`).

### Part C — Tutorial (24) Simple Frontend App, on branch `2025` (`14f2a14`)

HEAD removed this section and folder; the lecture teaches it. Run it as the whole 2025 stack, *instead of* (not next to) the HEAD containers, since names and ports collide.

**C0. Switch to the 2025 code.** Stop the HEAD stack (Ctrl-C/`exit` in the API and frontend shells; `docker compose down` in `src/vector-db`). Then in `cheese-app-v2`: `git fetch && git switch 2025` (or a second clone checked out at `14f2a14`). Add `llm-service-account.json` to `secrets/` (copy of `ml-workflow.json` is fine) and set `GCP_PROJECT` in `cheese-app-v2@2025/src/api-service/docker-shell.sh:11` and `cheese-app-v2@2025/src/vector-db/docker-shell.sh:9`.

**C1. 2025 vector DB** (`cheese-app-v2@2025/README.md:40-65`): `cd src/vector-db`, `sh docker-shell.sh` (uses `docker-compose`, `cheese-app-v2@2025/src/vector-db/docker-shell.sh:20`; on a compose-plugin-only machine run `docker compose run --rm --service-ports cheese-app-vector-db-cli` yourself), then `python cli.py --download --load --chunk_type recursive-split`. Chroma here is `chromadb/chroma:latest` with the mount `./docker-volumes/chromadb:/chroma/chroma` (`cheese-app-v2@2025/src/vector-db/docker-compose.yml:20-25`); HEAD's compose comment says Chroma 1.x keeps its data in `/data` (`cheese-app-v2/src/vector-db/docker-compose.yml:25`), so in the 2025 stack the data lives only inside the container. The `--load` output is the same as B1.

**C2. 2025 API** (`cheese-app-v2@2025/README.md:67-94`): `cd src/api-service`, `sh docker-shell.sh`, then `uvicorn_server`. The README's step 3 asks you to review `-p 9000:9000`, `-e DEV=1` and the entrypoint's dev/prod split (`:82-86`; `cheese-app-v2@2025/src/api-service/docker-shell.sh:23-35`, `cheese-app-v2@2025/src/api-service/docker-entrypoint.sh:14-38`). Differences from HEAD that you will see:
- Importing `api.service` imports all six router modules (`cheese-app-v2@2025/src/api-service/api/service.py:4-7`); the RAG utils build `chromadb.HttpClient` at import (`cheese-app-v2@2025/src/api-service/api/utils/llm_rag_utils.py:57`), so the API **will not start without Chroma** (`ValueError: Could not connect to a Chroma server`), and the CNN is downloaded/loaded at import (`cheese-app-v2@2025/src/api-service/api/utils/llm_cnn_utils.py:110-149`), so startup takes long and every reload repeats it.
- Routes have no `/api` prefix; docs at `http://localhost:9000/docs`; `GET /` → `{"message":"Welcome to AC215"}`; `/square_root/` is already in the code (`cheese-app-v2@2025/src/api-service/api/service.py:25-33`), so do not paste the README's demo route (`cheese-app-v2@2025/README.md:96-108`) a second time.
- The README shows only the newsletter router enabled and says "Enable all the routes" (`cheese-app-v2@2025/README.md:116-138`); the code already has four enabled, RAG and Agent commented (`cheese-app-v2@2025/src/api-service/api/service.py:37-42`). The README's file names `newsletters.py`/`podcasts.py` (`:131-132`) are really `newsletter.py`/`podcast.py`.
- `GENERATIVE_MODEL = "gemini-2.0-flash-001"` at `us-central1` (`cheese-app-v2@2025/src/api-service/api/utils/llm_utils.py:19-22`): retired June 1, 2026 (§6 #8), so chat answers fail unless patched. HEAD's own fix is the template: `gemini-3.8-flash` at `location="global"`, keeping `text-embedding-004` (`cheese-app-v2/src/api-service/api/settings.py:7-11`). In the 2025 code that means editing `GCP_LOCATION` and `GENERATIVE_MODEL` in `api/utils/llm_utils.py`, `llm_cnn_utils.py` and `llm_rag_utils.py`.

**C3. Simple frontend** (`cheese-app-v2@2025/README.md:147-165`): in a third terminal `cd cheese-app-v2/src/frontend-simple`, `sh docker-shell.sh`, `http-server`. Same image name and port as v1's (`cheese-app-frontend-simple`, 8080).

**C4. Test the application** (`cheese-app-v2@2025/README.md:167-183`):
- `http://localhost:8080/index.html`: the landing page; the only diff from v1's `index.html` is two nav links, "Newsletters" and "Cheese Assistant".
- `http://localhost:8080/newsletters.html`: three cards with images. The API terminal logs `GET /newsletters?limit=100` → **307**, then `GET /newsletters/?limit=100` → 200, because the JS omits the slash (`cheese-app-v2@2025/src/frontend-simple/newsletters-main.js:7`); images from `/newsletters/image/<file>` (`:15-17`). No preflight: these are plain `axios.get` calls without custom headers.
- `http://localhost:8080/chat.html`: ask "How is cheese made?". The API log shows an `OPTIONS` preflight, `POST /llm/chats/` → 307, then `POST /llm/chats` (`cheese-app-v2@2025/src/frontend-simple/chat-main.js:30-32`); later messages may show no `OPTIONS` (cached for 600 s). A JSON file appears in `persistent-folder/chat-history/llm/<uuid>/`. Without the model patch, the page says "Sorry, there was an error processing your message." and the uvicorn log shows the Vertex 404.
- The README says to review `newsletters.html`/`chat.html` (`:176`, `:181`); the API code is in `newsletters-main.js` and `chat-main.js`, which hard-code `http://localhost:9000` (`cheese-app-v2@2025/src/frontend-simple/chat-main.js:2`, `newsletters-main.js:3`).
- Afterwards: stop the 2025 containers (`docker stop cheese-app-vector-db` etc.) and `git switch main` before Part D.

### Part D — cheese-app-v2 HEAD `e98fa55`: Tutorial (25) React Frontend Setup, Production images

Bring the HEAD vector DB (B1, `docker compose up -d chromadb` is enough once loaded) and API (B2) back up first.

**D1. Start the frontend** (`cheese-app-v2/README.md:154-169`).
- Commands, in a new terminal: `cd src/frontend-react`, `./docker-shell.sh`, then inside `npm run dev`; open **`http://localhost:3000`**. No separate `npm install` step any more: the entrypoint runs it.
- Under the hood:
  - The script creates the network if missing, `docker exec`s into an already running `cheese-app-frontend-react` if there is one, else builds `Dockerfile.dev` and runs it with the folder bind-mounted at `/app`, a named volume `cheese-app-frontend-react-node_modules` over `/app/node_modules`, `-p 3000:5173`, and `--network cheese-app-network` (`cheese-app-v2/src/frontend-react/docker-shell.sh:8-23`).
  - `Dockerfile.dev`: `node:24.22.1-bookworm-slim`, pre-creates `/app/node_modules` owned by `node` so the fresh named volume is writable, `USER node`, no app code or dependencies baked in (`cheese-app-v2/src/frontend-react/Dockerfile.dev:1-14`).
  - The entrypoint prints Node/npm versions, runs `npm install --no-fund --no-audit` (a full install only the first time, since `node_modules` persists in the volume), lists `npm run dev` and `npm run check`, and opens bash (`cheese-app-v2/src/frontend-react/docker-entrypoint.dev.sh:3-21`).
  - `npm run dev` = `vite` (`cheese-app-v2/src/frontend-react/package.json:7`): listens on all interfaces, port 5173, `strictPort`, and proxies `/api` to `process.env.API_URL || 'http://cheese-app-api-service:9000'` (`cheese-app-v2/src/frontend-react/vite.config.js:9-14`).
- Checkpoint: `VITE v8.3.5 ready in … ms`, `➜ Local: http://localhost:5173/`, `➜ Network: http://172.x.x.x:5173/`. **Those are the container's addresses; from the laptop use `http://localhost:3000`** (`-p 3000:5173`). The home page loads two podcasts and two newsletters through `/api` (`cheese-app-v2/src/frontend-react/src/routes/Home.jsx:39-40`).
- If it fails: `port is already allocated` for 3000 → another dev server (or L10's frontend) holds it. Pages with no content → the API is not running or `api_server` not started (`cheese-app-v2/README.md:226`); the Vite terminal then shows `http proxy error` for `/api/...`.

**D2. Review the app** (`cheese-app-v2/README.md:171-179`).
- **Home**: a composer; typing a question navigates to `/chat?model=llm`, attaching a photo to `/chat?model=llm-cnn`, carrying the message in router state (`cheese-app-v2/src/frontend-react/src/routes/Home.jsx:42-46`), and Chat sends it once (`cheese-app-v2/src/frontend-react/src/routes/Chat.jsx:66-73`).
- **Podcasts, Newsletters** load through the API; `/newsletters/:id` renders the newsletter's HTML `detail` with `dangerouslySetInnerHTML` (`cheese-app-v2/src/frontend-react/src/routes/Newsletter.jsx:27`).
- **Chat** has three modes (`cheese-app-v2/src/frontend-react/src/routes/Chat.jsx:8-27`): **Ask** (`llm`), **Identify** (`llm-cnn`: a photo gets a "Our model thinks this is <label>" card with a confidence bar, `cheese-app-v2/src/frontend-react/src/components/ChatMessage.jsx:5-21`, then text questions go to Gemini, which is told the label), **Cheese books** (`llm-rag`; README suggests "How is Tolminc cheese made?"). After each answer the URL becomes `/chat?model=<mode>&id=<chat_id>` (`:57`). Chats appear under **Recent** for the current mode and survive a reload (`cheese-app-v2/README.md:179`), because the session id is in `localStorage`. Capture note: Tolminc answers can quote the book's author, the course instructor; mask as ‹instructor›.
- Photos are shrunk in the browser to at most 512 px JPEG before upload (`cheese-app-v2/src/frontend-react/src/lib/image.js:1-13`).

**D3. Review the code** (`cheese-app-v2/README.md:181-195`). Read `vite.config.js`, `src/main.jsx`, `src/lib/api.js`, `src/routes/Chat.jsx`, `src/components/`. Then `npm run check` = `eslint . && prettier --check . && vite build` (`cheese-app-v2/src/frontend-react/package.json:11`); it leaves a `dist/` folder (git-ignored).

**D4. Production images** (`cheese-app-v2/README.md:197-215`).
- Ctrl-C, `exit`, then from `src/frontend-react`: `docker build -t cheese-app-frontend-react:prod .` and `docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod`; open `http://localhost:8080`.
- Under the hood: stage 1 `npm ci` + `npm run build` on `node:24.22.1-bookworm-slim` (built on the builder's own platform, `--platform=$BUILDPLATFORM`); stage 2 `nginx:1.31.8-alpine` with `ENV API_URL=http://cheese-app-api-service:9000` and the template copied to `/etc/nginx/templates/` (`cheese-app-v2/src/frontend-react/Dockerfile:3-16`), which the nginx image's entrypoint fills in with `envsubst` at start. nginx serves `dist/`, passes `/api/` on with the full path (`proxy_pass ${API_URL};`), caches hashed `/assets/` forever, answers its own `/healthz`, and falls back to `index.html` for client-side routes (`cheese-app-v2/src/frontend-react/nginx.conf.template:1-33`).
- Checkpoint: the same app on 8080, "no Vite and no Node now"; `docker images | grep cheese-app-frontend-react` shows the dev and `prod` tags and their sizes (`cheese-app-v2/README.md:210-215`).
- If it fails: nginx exits at start with `host not found in upstream "cheese-app-api-service:9000"` → the API container is not running on `cheese-app-network` (nginx resolves a literal `proxy_pass` host when it loads its config; Vite, by contrast, resolves per request).
- The API's production image (`cheese-app-v2/src/api-service/Dockerfile`) exists but the README does not build it here; L20 does.

**D5. Troubleshooting and cleanup** (`cheese-app-v2/README.md:217-240`): the README's own table maps `/readyz` 503s, "The vector DB is empty", `Gemini: 403`/`PERMISSION_DENIED`, `Gemini: 404` ("Google retired the model. Change `GENERATIVE_MODEL` in `api/settings.py`"), empty pages and `port is already allocated` to fixes. Cleanup: Ctrl-C/`exit`, `docker compose down` in `src/vector-db`, then `docker system prune` (check the list first, `:236-237`).

---

## 5. Code tour

```text
cheese-app-v1/src/  (ce03a10)
  api-service/                Dockerfile (python 3.12 + uv), docker-shell.sh, docker-entrypoint.sh (venv + bash)
    api/service.py            FastAPI app with CORS and one route "/"
  frontend-simple/            node:20-alpine + http-server; index.html, main.js (hard-coded podcasts), styles.css
  data-collector/ … vector-db/   empty placeholders (.gitkeep)

cheese-app-v2/  (e98fa55, HEAD)
  docs/contract.md            the routes, messages, errors and settings frontend and API agree on
  src/vector-db/
    docker-shell.sh           network, build CLI image, `docker compose run --rm`
    docker-compose.yml        cli service + chromadb/chroma:1.5.9 (/data) on cheese-app-network
    cli.py                    --download/--chunk/--embed/--load/--query/--chat/--get/--agent (RAG data prep from L05)
  src/api-service/
    docker-shell.sh           env vars, network, exec-if-running, Dockerfile.dev, mounts, -p 9000:9000
    Dockerfile.dev / docker-entrypoint.dev.sh   dev image; defines api_server
    Dockerfile                production: 2 stages, venv in /opt/venv, uid 1000, CMD uvicorn
    api/service.py            app (docs at /api/docs), lifespan, routers under /api, /healthz, /readyz
    api/settings.py           every env-driven setting (project, location, models, Chroma, CNN URL)
    api/routers/              newsletter.py, podcast.py, chat.py (create_router: one factory, three modes)
    api/utils/                chat_utils.py (ChatMessage, ChatHistoryManager), llm_utils.py (Ask, Gemini helpers),
                              llm_cnn_utils.py (Identify), llm_rag_utils.py (Cheese books)
    tests/                    conftest.py, test_service.py, test_chat.py (26 tests, fakes for Gemini/CNN/Chroma)
    news-letters/, podcasts/  JSON + assets served by the API (stand-in for a GCS bucket)
  src/frontend-react/
    Dockerfile.dev, docker-shell.sh, docker-entrypoint.dev.sh   dev container (Vite, node_modules volume)
    Dockerfile, nginx.conf.template                             production: build with Node, serve with nginx
    vite.config.js            dev server :5173, proxy /api -> cheese-app-api-service:9000
    index.html, src/main.jsx  the root div; the route table
    src/App.jsx               header/footer once + <Outlet />
    src/lib/                  api.js (every API call, session id), useGet.js, image.js
    src/routes/               Home, Chat, Newsletters, Newsletter, Podcasts, NotFound
    src/components/           ChatMessage, Composer, NewsletterCard, PodcastRow

cheese-app-v2@2025/src/  (14f2a14, Tutorial 24 only)
  frontend-simple/            index.html, newsletters.html/-main.js, chat.html/chat-main.js (axios from CDN)
  api-service/                CORS app, 7 routers incl. llm_rag_chat / llm_agent_chat, DEV=1 entrypoint
```

**(1) The app, its lifespan and the route table**: `cheese-app-v2/src/api-service/api/service.py:19-40`
```python
@asynccontextmanager
async def lifespan(app: FastAPI):
    # In the background, so the API answers while the model loads; /readyz says when it is done
    threading.Thread(target=llm_cnn_utils.load_cnn_model, daemon=True).start()
    yield


app = FastAPI(
    title="Cheese App API", lifespan=lifespan, docs_url="/api/docs", openapi_url="/api/openapi.json"
)


@app.get("/api/status")
def get_status():
    return {"version": "2.0.0"}


app.include_router(newsletter.router, prefix="/api/newsletters")
app.include_router(podcast.router, prefix="/api/podcasts")
app.include_router(chat.create_router("llm", llm_utils.respond), prefix="/api/llm")
app.include_router(chat.create_router("llm-cnn", llm_cnn_utils.respond), prefix="/api/llm-cnn")
app.include_router(chat.create_router("llm-rag", llm_rag_utils.respond), prefix="/api/llm-rag")
```
- Code before `yield` runs once when the server starts, code after it on shutdown. Starting a thread there lets the API answer `/healthz` and content routes while TensorFlow loads.
- `docs_url`/`openapi_url` move the docs under `/api`, so they are reachable through the same `/api` proxy as everything else.
- The three chat routers come from one factory; the prefixes are exactly the `model` strings the frontend sends (`llm`, `llm-cnn`, `llm-rag`). There is no CORS middleware.

**(2) Liveness vs. readiness**: `cheese-app-v2/src/api-service/api/service.py:43-56`
```python
@app.get("/healthz")
def healthz():
    return {"ok": True}


@app.get("/readyz")
def readyz():
    if llm_cnn_utils.cnn_model is None:
        raise HTTPException(503, "CNN model is loading")
    try:
        llm_rag_utils.chroma_client().heartbeat()
    except Exception as e:  # noqa: BLE001 - whatever went wrong, this pod is not ready
        raise HTTPException(503, f"Chroma: {e}")
    return {"ok": True}
```
- Liveness: "restart me if this fails". Readiness: "do not send me traffic yet". They stay at the root (not under `/api`), where a Kubernetes probe or a person checks them directly on port 9000.

**(3) One router factory for every chat mode**: `cheese-app-v2/src/api-service/api/routers/chat.py:19-43`
```python
# Both ids end up in file paths, so only a UUID gets through
UUID_PATTERN = r"^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$"
SessionId = Annotated[str, Header(alias="X-Session-ID", pattern=UUID_PATTERN)]
ChatId = Annotated[str, Path(pattern=UUID_PATTERN)]
MessageId = Annotated[str, Path(pattern=UUID_PATTERN)]


def make_title(message: ChatMessage) -> str:
    title = message.content or "Image chat"
    return f"{title[:50]}..." if len(title) > 50 else title


def create_router(model: str, respond: Callable[[ChatHistoryManager, list[dict], dict], dict]) -> APIRouter:
    router = APIRouter()
    chat_manager = ChatHistoryManager(model=model)

    def add_turn(chat: dict, message: ChatMessage, session_id: str) -> dict:
        if not message.content and not message.image:
            raise HTTPException(status_code=422, detail="Message must contain text or an image")

        user_message = {**message.model_dump(), "message_id": str(uuid.uuid4()), "role": "user"}
        reply = respond(chat_manager, chat["messages"], user_message)
        chat["messages"] += [user_message, {"message_id": str(uuid.uuid4()), **reply}]
        chat_manager.save_chat(chat, session_id)
        return chat
```
- `Annotated[..., Header(...)]` is the modern way to declare a header parameter; the regex makes FastAPI reject anything that is not a UUID with 422, which protects the file paths built from it.
- A *mode* only supplies `respond(chat_manager, past_messages, message) -> reply`. Everything else (ids, titles, saving, the four routes at `:45-76` and the image route at `:78-84`) is shared.
- `add_turn` is the whole state machine of a chat: validate, ask the mode for a reply given the *saved* history, append both messages, save the file.

**(4) The request body and the chat files**: `cheese-app-v2/src/api-service/api/utils/chat_utils.py:12-14`, `:49-60`
```python
class ChatMessage(BaseModel):
    content: str | None = Field(None, description="The message content")
    image: str | None = Field(None, description="The image content")
```
```python
    def save_chat(self, chat: dict, session_id: str) -> None:
        """Save a chat to a file. Images are saved separately and replaced by their path."""
        for message in chat["messages"]:
            if message.get("image"):
                message["image_path"] = self._save_image(
                    chat["chat_id"], message["message_id"], message["image"]
                )
            message.pop("image", None)

        os.makedirs(os.path.join(self.history_dir, session_id), exist_ok=True)
        with open(self._chat_path(chat["chat_id"], session_id), "w", encoding="utf-8") as f:
            json.dump(chat, f, indent=2, ensure_ascii=False)
```
- The body model has only `content` and `image` (a base64 string, with or without a `data:` prefix, `:17-22`); unknown fields are ignored.
- The base64 photo never stays in the JSON: it becomes a file and the message keeps `image_path`, which the frontend turns into `/api/<mode>/images/<chat_id>/<message_id>.png` (`cheese-app-v2/src/frontend-react/src/lib/api.js:65`).

**(5) Talking to Gemini with a rebuilt history**: `cheese-app-v2/src/api-service/api/utils/llm_utils.py:79-94`
```python
def ask_gemini(system_instruction: str, history: list[types.Content], parts: list) -> str:
    """Send one message to Gemini, with the conversation so far"""
    config = types.GenerateContentConfig(system_instruction=system_instruction)
    chat = llm_client.chats.create(model=settings.GENERATIVE_MODEL, config=config, history=history)
    try:
        text = chat.send_message(parts).text
    except errors.APIError as e:
        raise HTTPException(status_code=502, detail=f"Gemini: {e}")
    if not text:
        raise HTTPException(status_code=502, detail="Gemini returned no text")
    return text


def respond(chat_manager: ChatHistoryManager, past_messages: list[dict], message: dict) -> dict:
    history = to_history(past_messages, chat_manager)
    return {"role": "assistant", "content": ask_gemini(SYSTEM_INSTRUCTION, history, message_parts(message))}
```
- A fresh Gemini `Chat` per request, seeded with `history` from the saved file (`to_history`, `:54-76`): assistant turns become `ModelContent`, a `cnn` reply becomes the user line "We have already identified the image of a cheese as <label>" (`:60-63`), user turns get their saved photo back.
- The system instruction (the "cheese expert" persona, `:18-32`) *is* passed now (2025 defined one but never passed it).
- Vertex errors become a 502 with the reason in `detail`, which `api.js` shows to the user (`cheese-app-v2/src/frontend-react/src/lib/api.js:49-53`).
- Settings come from one module: `genai.Client(vertexai=True, project=settings.GCP_PROJECT, location=settings.GCP_LOCATION)` (`:15`), with `GCP_LOCATION="global"` because "Current Gemini models answer on the global endpoint only: a region such as us-central1 gives a 404" and `GENERATIVE_MODEL="gemini-3.8-flash"` (`cheese-app-v2/src/api-service/api/settings.py:6-10`).

**(6) Identify: CNN for photos, Gemini for words**: `cheese-app-v2/src/api-service/api/utils/llm_cnn_utils.py:64-69`
```python
def respond(chat_manager: ChatHistoryManager, past_messages: list[dict], message: dict) -> dict:
    if not message.get("image"):
        return llm_utils.respond(chat_manager, past_messages, message)
    if cnn_model is None:
        raise HTTPException(status_code=503, detail="The CNN model is still loading")
    return {"role": "cnn", "results": make_prediction(decode_image(message["image"]))}
```
- A photo never reaches Gemini in this mode's first turn: `make_prediction` resizes to 224×224, scales to [0, 1], predicts, applies softmax if the last layer lacks it, and returns `{prediction_label, accuracy}` (`:45-61`). Follow-up text goes to Gemini with the label (and the photo) in the rebuilt history.

**(7) Cheese books: retrieve, then generate**: `cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:38-42`, `:57-76`
```python
@cache
def chroma_client() -> chromadb.ClientAPI:
    """Connect on first use, so the API can start before Chroma does. A failed connection is not
    cached, so the next call tries again."""
    return chromadb.HttpClient(host=settings.CHROMADB_HOST, port=settings.CHROMADB_PORT)
```
```python
def find_chunks(query: str) -> list[str]:
    embedding = generate_query_embedding(query)
    try:
        collection = chroma_client().get_collection(name=COLLECTION_NAME)
        results = collection.query(query_embeddings=[embedding], n_results=5)
    except NotFoundError:
        raise HTTPException(status_code=503, detail="The vector DB is empty: load it first (see vector-db)")
    except (ChromaError, ValueError, httpx.TransportError) as e:
        raise HTTPException(status_code=503, detail=f"Chroma: {e}")
    return results["documents"][0]


def respond(chat_manager: ChatHistoryManager, past_messages: list[dict], message: dict) -> dict:
    if message.get("image"):
        parts = message_parts(message)
    else:
        chunks = "\n".join(find_chunks(message["content"]))
        parts = [f"{message['content']}\n{chunks}"]
    history = to_history(past_messages, chat_manager)
    return {"role": "assistant", "content": ask_gemini(SYSTEM_INSTRUCTION, history, parts)}
```
- `@cache` + lazy creation is the fix for 2025's "API will not start without Chroma".
- The query is embedded with the same model and dimension as the stored vectors (`text-embedding-004`, 256, `cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:45-54`; `settings.py:11-12`, "Must match what `vector-db` loaded with", `cheese-app-v2/docs/contract.md:65`). The top-5 chunks are appended to the question, and the RAG system instruction ("based solely on the information provided in the text chunks", `:15-33`) is now really applied.

**(8) The API dev container**: `cheese-app-v2/src/api-service/docker-shell.sh:16-34`
```bash
if docker ps --format "{{.Names}}" | grep -qx "${IMAGE_NAME}"; then
    echo "Container '${IMAGE_NAME}' is already running. Shelling into it..."
    docker exec -it "$IMAGE_NAME" /bin/bash
else
    echo "Building ${IMAGE_NAME} (Dockerfile.dev)..."
    docker build -t "$IMAGE_NAME" -f Dockerfile.dev .

    # Run the container
    docker run --rm --name "$IMAGE_NAME" -ti \
        -v "$BASE_DIR":/app \
        -v "$SECRETS_DIR":/secrets:ro \
        -v "$PERSISTENT_DIR":/persistent \
        -p 9000:9000 \
        -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json \
        -e GCP_PROJECT="$GCP_PROJECT" \
        -e CHROMADB_HOST="$CHROMADB_HOST" \
        -e CHROMADB_PORT="$CHROMADB_PORT" \
        --network cheese-app-network \
        "$IMAGE_NAME"
fi
```
- Running the script a second time gives you a second shell in the same container (handy for `pytest` next to a running server).
- Three mounts: code (in the repo), keys (outside, read-only), state (outside). `-p` is the browser's door; `--network` is the LAN to Chroma and to the frontend's proxy.

**(9) The frontend's single door to the API**: `cheese-app-v2/src/frontend-react/src/lib/api.js:31-63`
```javascript
async function request(path, body) {
  const options = {
    method: body === undefined ? 'GET' : 'POST',
    headers: { 'X-Session-ID': sessionId() },
    signal: AbortSignal.timeout(130_000), // a little longer than the API gives Gemini
  }
  if (body !== undefined) {
    options.headers['Content-Type'] = 'application/json'
    options.body = JSON.stringify(body)
  }

  let response
  try {
    response = await fetch(path, options)
  } catch {
    throw new Error("Couldn't reach the API. Check that it's running.")
  }
  const data = await response.json().catch(() => null)
  if (!response.ok) {
    throw new Error(
      typeof data?.detail === 'string' ? data.detail : `The API answered ${response.status}.`,
    )
  }
  return data
}

export const get = (path) => request(path)

export const getChats = (model) => get(`/api/${model}/chats?limit=30`)
export const getChat = (model, chatId) => get(`/api/${model}/chats/${chatId}`)
export const startChat = (model, message) => request(`/api/${model}/chats`, message)
export const continueChat = (model, chatId, message) =>
  request(`/api/${model}/chats/${chatId}`, message)
```
- Plain `fetch`, no axios, no base URL: `fetch('/api/…')` goes to the page's own origin.
- The session id comes from `localStorage` (created once with `crypto.getRandomValues`, because `crypto.randomUUID()` needs HTTPS or localhost, `:8-29`).
- The API's `detail` strings (422/502/503 reasons) surface as the error text in the chat page.

**(10) The proxy**: `cheese-app-v2/src/frontend-react/vite.config.js:5-15`
```javascript
// The browser always calls /api/... on its own origin. In dev, Vite forwards that to the API
// container by name, on cheese-app-network; in production, nginx does (nginx.conf.template).
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    host: true, // listen on all interfaces, so the container's published port reaches it
    port: 5173,
    strictPort: true,
    proxy: { '/api': process.env.API_URL || 'http://cheese-app-api-service:9000' },
  },
})
```
- `host: true` is the frontend's `--host 0.0.0.0`. `proxy` is why the frontend container must be on `cheese-app-network`.

**(11) The chat page**: `cheese-app-v2/src/frontend-react/src/routes/Chat.jsx:48-64`
```javascript
  async function send(message) {
    setError('')
    setFailed(null)
    setPending(message)
    try {
      const saved = chatId
        ? await continueChat(model, chatId, message)
        : await startChat(model, message)
      setChat(saved)
      setParams({ model, id: saved.chat_id })
    } catch (e) {
      setError(e.message)
      setFailed(message)
    } finally {
      setPending(null)
    }
  }
```
- Optimistic UI: the pending message shows at once with "Thinking…" (`:174-175`); the API returns the *whole chat*, which replaces local state; `setParams` writes `model` and `id` into the URL, and on reload an effect fetches that chat (`:76-85`). A second effect refreshes the Recent list after every answer (`:88-96`).

**(12) Simple frontend (2025): one axios instance, one header**: `cheese-app-v2@2025/src/frontend-simple/chat-main.js:11-23`
```javascript
const api = axios.create({
    baseURL: BASE_API_URL
});
const sessionId = uuid();
// Add request interceptor to include session ID in headers
api.interceptors.request.use((config) => {
    if (sessionId) {
        config.headers['X-Session-ID'] = sessionId;
    }
    return config;
}, (error) => {
    return Promise.reject(error);
});
```
- `BASE_API_URL = 'http://localhost:9000'` (`:2`): a host address, because this JS runs in the browser, and a different origin from the page on 8080, hence CORS.
- `uuid()` per page load: a reload is a new "user".

---

## 6. Gotchas and common errors

HEAD (`e98fa55`) unless marked **[2025]**.

1. **Vite says 5173, the laptop needs 3000.** `npm run dev` prints `Local: http://localhost:5173/` and a `172.x` Network address; both are inside the container. The script publishes `-p 3000:5173` (`cheese-app-v2/src/frontend-react/docker-shell.sh:21`). Open `http://localhost:3000`.
2. **Old URLs are 404s now.** `http://localhost:9000/` and `/docs` return `{"detail":"Not Found"}`: there is no root route and the docs moved to `/api/docs` (`cheese-app-v2/src/api-service/api/service.py:27`). Use `/healthz` for "is it up?".
3. **`/readyz` is 503 for a while, and again after every save.** The CNN loads in a background thread on each start; `--reload` restarts the worker and the lifespan, so after each edit under `api/` the model reloads (from `/persistent`, no re-download). Meanwhile an Identify photo returns 503 "The CNN model is still loading" (`cheese-app-v2/src/api-service/api/utils/llm_cnn_utils.py:67-68`). Wait for `/readyz` → `{"ok":true}`.
4. **"Cheese books" errors.** `Chroma: …` (503) → Chroma is down: `docker compose up -d chromadb` in `src/vector-db`. "The vector DB is empty: load it first (see vector-db)" (503) → run B1's `--download --load` (`cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:62-65`, `cheese-app-v2/README.md:222-223`). The API itself starts fine without Chroma.
5. **Linux: Docker creates missing bind-mount folders as root.** Containers run as uid 1000 (`app`, `node`). A root-owned `persistent-folder` makes the CNN thread fail (`PermissionError` traceback in the log, `/readyz` stuck at "CNN model is loading") and every chat save fail. Fix: `mkdir -p secrets persistent-folder` yourself before the first run, or `sudo chown -R 1000:1000 persistent-folder`. The same applies to `src/vector-db/outputs` if your host uid is not 1000 (the CLI runs as uid 1000 and writes into the bind mount). Docker Desktop on macOS/Windows hides this.
6. **Same container name, wrong container.** `cheese-app-api-service` is the API container name in v1, 2025 and HEAD (`cheese-app-v1/src/api-service/docker-shell.sh:7`, `cheese-app-v2@2025/src/api-service/docker-shell.sh:7`, `cheese-app-v2/src/api-service/docker-shell.sh:5`). HEAD's script silently `docker exec`s into *any* running container with that name (`:16-18`), so a leftover v1 or 2025 API gives you a shell in the old code. `docker ps` first; `docker stop cheese-app-api-service`. Ports collide too: 9000 (all APIs, L10's), 8000 (Chroma: L10, 2025, HEAD), 8080 (v1/2025 simple frontend and HEAD's production frontend).
7. **Session id in `/api/docs`.** Chat routes require `X-Session-ID` shaped like a UUID: missing or `test` → 422 (`cheese-app-v2/src/api-service/api/routers/chat.py:21`). Paste a UUID (`python -c "import uuid;print(uuid.uuid4())"` in the container).
8. **Gemini model and location.** HEAD uses `gemini-3.8-flash` at `location="global"` (`cheese-app-v2/src/api-service/api/settings.py:7`, `:10`; same in `cheese-app-v2/src/vector-db/cli.py:27`, `:31`). Google's Vertex AI "Model versions and lifecycle" page (read 2026-11-05) lists `gemini-3.8-flash` released September 2, 2026, retiring "September 2, 2027 or later"; `gemini-2.0-flash` retired June 1, 2026 (replacement listed: `gemini-3.5-flash-lite`); `gemini-2.5-flash` retired October 20, 2026; `text-embedding-004` available until April 1, 2027. Symptoms: `Gemini: 404` → retired model or a region endpoint; `Gemini: 403`/`PERMISSION_DENIED` → wrong `GCP_PROJECT`, API not enabled, or the account lacks Vertex AI User (`cheese-app-v2/README.md:224-225`). `GENERATIVE_MODEL`, `GCP_LOCATION` and `EMBEDDING_MODEL` can be overridden by env var. **[2025]** `gemini-2.0-flash-001` at `us-central1` is retired, so every 2025 chat fails until patched (C2).
9. **Do not change the embedding model on one side.** The stored vectors were made with `text-embedding-004` at 256 dimensions. Changing `EMBEDDING_MODEL` in the API alone keeps shapes valid but makes retrieval meaningless. Re-embed (`python cli.py --chunk --embed --load --chunk_type recursive-split`, billable) with the same model on both sides. `text-embedding-004` itself retires April 1, 2027.
10. **Frontend dependencies live in a volume.** `node_modules` is the named volume `cheese-app-frontend-react-node_modules`, not a host folder, so your editor on the host may flag unresolved imports, and `docker system prune` does not reset it. To start clean: `docker volume rm cheese-app-frontend-react-node_modules`. Never `npm install` on the host into this folder and expect the container to use it.
11. **Production frontend needs the API first.** `docker run … cheese-app-frontend-react:prod` exits with nginx `host not found in upstream` when `cheese-app-api-service` is not running on `cheese-app-network` (D4).
12. **No CORS at HEAD.** Any page served from another origin that calls `http://localhost:9000/api/...` (for example a hand-made test page, or the 2025 simple frontend) is blocked by the browser, and the 2025 pages also call paths without `/api` (404). `curl` and `/api/docs` work. Go through the proxy (3000 or 8080), or add `CORSMiddleware` deliberately.
13. **Slow first build, big image.** TensorFlow 2.21 (`cheese-app-v2/src/api-service/pyproject.toml:13-14`); "About 10 GB of free disk space". Apple Silicon gets `tensorflow` (aarch64 wheel in `uv.lock`), Intel/AMD gets the smaller `tensorflow-cpu`. Expect `Architecture: aarch64` in the banner on a Mac.
14. **`--chat` always asks the same question.** `cli.py --chat` ignores input and asks "How is cheese made?" (`cheese-app-v2/src/vector-db/cli.py:377`); edit the line to ask something else.
15. **[2025] The API will not start without Chroma**, even with the RAG router disabled (import-time `chromadb.HttpClient`, `cheese-app-v2@2025/src/api-service/api/utils/llm_rag_utils.py:57`, imported unconditionally at `cheese-app-v2@2025/src/api-service/api/service.py:7`). Start C1 first.
16. **[2025] "CORS error" that is really a server crash.** RAG follow-ups (`cheese-app-v2@2025/src/api-service/api/routers/llm_rag_chat.py:99`, `message["content"]` on a pydantic object) and other unhandled exceptions return a 500 without CORS headers; the browser blames CORS. Read the uvicorn traceback.
17. **[2025] `docker-compose: command not found`** on compose-plugin-only installs (`cheese-app-v2@2025/src/vector-db/docker-shell.sh:20`): run `docker compose run --rm --service-ports cheese-app-vector-db-cli`.
18. **[2025/v1] Edits to the simple frontend do not show.** `http-server` caches for 3600 s; the `<meta http-equiv="Cache-Control">` tags (`cheese-app-v1/src/frontend-simple/index.html:7-9`) do not cover JS/CSS. Use `http-server -c-1` or hard-refresh.
19. **[2025] Simple-frontend chat quirks.** CNN replies render empty (the reply has `results`, not `content`; `chat-main.js` prints `.content`, `cheese-app-v2@2025/src/frontend-simple/chat-main.js:161-164`); the image × button calls a global `removeImage()` that only exists as a method (`cheese-app-v2@2025/src/frontend-simple/chat.html:27`, `chat-main.js:197`); clicking a newsletter card calls an undefined `handleNewsletterClick` (`cheese-app-v2@2025/src/frontend-simple/newsletters-main.js:27`).

---

## 7. Where this sits in the course

- **What you already have.**
  - L02/L04: containers, ports and Docker networks.
  - L05: the `llm-rag` chunk → embed → Chroma pipeline; `vector-db/cli.py` is a copy of it, agent code included.
  - L10 (`cheese-app-v0`, rebuilt October 2026): a FastAPI + Next.js RAG app on host ports 9000 / 3200, `gemini-3.1-flash-lite` and `gemini-embedding-001` at `location="global"` (`cheese-app-v0/llm-rag/cli.py:24-27`, `cheese-app-v0/frontend-ai-chatbot/docker-shell.sh:11`).
  - L13: the MobileNetV2 cheese classifier whose trained artifact the API downloads.
  - L15 (`ml-workflow`): the service account and key file this API reuses.
- **What L18 adds.** Code organisation for a real app (`src/<service>/`, one container per concern), a REST API with routers, request models, file-backed stateless chat, health/readiness probes and tests, and two frontends that consume it, one cross-origin with CORS (simple), one same-origin through a proxy (React). Milestone 4 asks for exactly this: "Building APIs with FastAPI and connecting them to user-facing frontends (simple and React-based)", with the frontend at e.g. `http://localhost:3000` and the API at e.g. `http://localhost:9000` (course site, `harvard-iacs.github.io/2026-AC215/milestone4/`, read 2026-11-05).
- **What comes next.**
  - L19, "Scaling: Kubernetes (local)": the course site still says the tutorial is "coming soon" (read 2026-11-05).
  - L20/L22 use `cheese-app-v3` (main `3ecef56`, still the 2025 edition: `api_app` mounted under `ROOT_PATH`, `/status`, CORS, Next.js `output: "standalone"`, `cheese-app-v3/src/api-service/api/service.py:13-50`, `cheese-app-v3/src/frontend-react/next.config.js:12`). v2 HEAD already contains the pieces those lectures need (`/api` prefix + nginx entrance, `/healthz`/`/readyz`, stateless chats "when we scale in `cheese-app-v3`", numeric `USER 1000:1000` "so Kubernetes can check runAsNonRoot", `cheese-app-v2/src/api-service/Dockerfile:21-22`), and v3 has an unmerged `work/shivas` branch, so v3 is probably about to be upgraded the same way (not verified).

**Version diffs**

*v1 → v2@2025* (`git diff --no-index --stat cheese-app-v1/src cheese-app-v2@2025/src`: "116 files changed, 81783 insertions(+), 6 deletions(-)", mostly the books, `uv.lock` and `package-lock.json`): 6 routers + utils, `square_root` pre-added, CORS, `DEV` switch, simple-frontend newsletters/chat pages, a Next.js 15 React app, the vector-db stack; the API, simple-frontend Dockerfiles and `main.js`/`styles.css` are byte-identical to v1.

*v2@2025 → v2 HEAD* (`git diff --stat 14f2a14 e98fa55`: "131 files changed, 6060 insertions(+), 18293 deletions(-)"):

```text
 README.md                         rewritten: 4-container table, single key, ./docker-shell.sh, api_server,
                                   /healthz /readyz, /api/square_root, pytest, Tutorial 24 removed,
                                   Vite React, Production images, Troubleshooting, docker compose down
 docs/contract.md                  new: routes, messages, errors, settings
 api-service/api/service.py        /api prefix, lifespan thread, /healthz /readyz, no CORS, no "/" route
 api-service/api/settings.py       new: env-driven settings (global, gemini-3.8-flash)
 api-service/api/routers/chat.py   new: create_router() replaces llm_chat / llm_cnn_chat / llm_rag_chat
                                   (llm_agent_chat, test_router and llm_agent_utils deleted)
 api-service/tests/                new: 26 pytest tests with fakes
 api-service/Dockerfile(.dev)      python 3.13, uv 0.13.6; dev image + 2-stage prod image
 api-service/docker-shell.sh       exec-if-running, Dockerfile.dev, secrets :ro, no DEV / GCS_BUCKET_NAME
 frontend-simple/**                deleted (5104923 "removed frontend simple")
 frontend-react/**                 Next.js 15 App Router -> Vite 8 + React 19 + React Router 8 + Tailwind 4;
                                   node_modules volume, -p 3000:5173, on cheese-app-network; nginx prod image
 vector-db/                        chroma 1.5.9 at /data, docker compose, python 3.13, ml-workflow.json,
                                   langchain_text_splitters, --chat/--agent ported to google-genai
```

---

## 8. Video plan (suggestion)

**Hook question.** "You type *How is cheese made?* at `localhost:3000` and press Enter. The page never mentions port 9000, and the API has no CORS. So how does your question reach FastAPI, and why did last year's version of this very app need CORS to do the same thing?"

**Target length:** ~32 minutes in two parts (~5,000 spoken words at 155 wpm), with the viewer's terminal and editor open side by side.

**Before filming:** HEAD needs no model patch (`gemini-3.8-flash`, global). The 2025 stack for Tutorial 24 does: either patch C2's three utils files (and say so on screen), or show newsletters working and the chat error honestly. Mask the instructor's name in any `--chat` output or Tolminc answer.

| # | Chapter | The one idea | Visual | On screen |
|---|---|---|---|---|
| 1 | Cold open (2 min) | An app is several cooperating processes | §1 diagram builds box by box; a message token travels browser → :3000 → Vite → API → Chroma → Vertex → back | `docker ps` with 4 containers; the chat answering |
| 2 | v1: a Python function becomes a URL (4 min) | REST = function call over HTTP; FastAPI turns a signature into route + validation | `…/square_root/?x=2&y=10` splits into tokens that slot into `square_root(x, y)`; `?x=abc` bounces with 422 | v1 `docker-shell.sh`, uvicorn command, the edit, `/docs` |
| 3 | Inside the container: server vs app, 0.0.0.0, reload (3 min) | uvicorn owns the socket; binding decides reachability | Two nested boxes; `-p 9000:9000` tunnel; 127.0.0.1 version hits a wall; save → "swap worker" | v1 entrypoint, `Started reloader process` |
| 4 | Static frontend (2 min) | The frontend container serves files; the browser runs them | Files fly to the browser, JS wakes up there; v1 has no arrow to the API | `http-server`, `main.js:37-52`, `-c-1` |
| 5 | v2 setup: vector DB + API (5 min) | Compose + network; lazy clients; liveness vs readiness | Network cable with a phone book; `/healthz` green while `/readyz` turns from amber to green as the CNN loads | B1/B2 commands, `--load` output, `/readyz` 503 → 200, `/api/square_root`, `/api/docs` |
| 6 | Routers, bodies, stateless chats (4 min) | One router factory, pydantic body, UUID header, history rebuilt from disk | `create_router` stamps three sub-trees; a JSON body morphs into `ChatMessage`; a chat file grows message by message | `service.py:36-40`, `chat.py:31-43`, a JSON file in `persistent-folder`, `pytest` |
| 7 | Tutorial 24 on the 2025 branch: CORS (4 min) | Cross-origin calls need the server's permission; preflight | :8080 page → OPTIONS scout → badge → POST to :9000; the 307 slash redirect | `git switch 2025`, `http-server`, API log with OPTIONS / 307 |
| 8 | React + Vite: one origin, a proxy (5 min) | The browser only talks to :3000; Vite forwards `/api` by container name | Courier inside the frontend box; route table → URL bar; `<Outlet />` swapping pages | `docker-shell.sh` (React), `npm run dev` (5173 vs 3000), `vite.config.js`, `api.js`, `Chat.jsx` |
| 9 | Production image + debugging tour (3 min) | nginx replaces Vite; read the server's `detail` first | dev vs prod image sizes; checklist: Chroma up → readyz → key/project → model → logs | D4 commands, `docker images`, README troubleshooting table |

**Pause-and-ponder (quiz-style, with a timer):**
1. End of ch. 3: "If uvicorn listened on `--host 127.0.0.1` inside the container, would `curl localhost:9000` *inside the container* work? Would your browser?" (Yes, then no.)
2. Ch. 5: "`/healthz` says ok but `/readyz` says 503. Should a load balancer restart this container, or just not send it traffic yet?" (Not send traffic: it is alive, not ready.)
3. Ch. 7/8: "The 2025 simple frontend needed CORS; HEAD's React app does not. What changed: the API, the browser, or the *origin* the page calls?" (The origin: React calls its own origin and Vite forwards.)
4. Ch. 8: "Could the browser call `http://cheese-app-api-service:9000` directly?" (No: container names resolve only inside Docker networks; the laptop's DNS does not know them.)

**Recap questions (end):**
1. What does `api.service:app` refer to, and from which directory must uvicorn run?
2. Name the two ways containers are reached at HEAD, and which one the browser uses.
3. Why did the 2025 chat send an `OPTIONS` request first, and why does HEAD's not?
4. Where are chat histories stored, and why can any copy of the HEAD API answer any chat?
5. What is the difference between `/healthz` and `/readyz`?
6. Which file decides where `/api` goes in development, and which in production?

---

## 9. Exercises

**E1 (hands-on, v1).** Add `@app.get("/hypot/{x}")` with `x: float` as a *path* parameter and `y: float = 0` as a *query* parameter, returning `(x**2 + y**2)**0.5`. Predict `/hypot/3?y=4`, `/hypot/3`, `/hypot/abc`.
*Answer:* 5.0, 3.0, and a 422 `float_parsing` error naming `path` → `x`. `/docs` shows `x` required (path), `y` optional (query, default 0). It reloads automatically because the file is under `api/`.

**E2 (predict, networking).** In `vite.config.js`, change the proxy target to `http://localhost:9000` and restart `npm run dev`. What happens to the home page, and why?
*Answer:* No podcasts or newsletters; the Vite terminal logs `http proxy error … ECONNREFUSED`. The proxy runs *inside the frontend container*, where `localhost` is that container itself, not the API. Inside Docker, use the container name. (Setting `API_URL` would override the default without editing the file, `cheese-app-v2/src/frontend-react/vite.config.js:13`.)

**E3 (debugging, readiness).** Start the HEAD API before Chroma. Which of `/healthz`, `/readyz`, `GET /api/newsletters`, an Ask question and a Cheese-books question work? Then start Chroma without reloading the API.
*Answer:* `/healthz`, newsletters and Ask work (Ask only needs Gemini); `/readyz` and Cheese books return 503 "Chroma: …". Once Chroma is up, both recover without a restart, because a failed connection is not cached (`cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:38-42`). Contrast: the 2025 API would not even start (§6 #15).

**E4 (debugging + CORS, 2025 stack).** Enable the RAG router in the 2025 API, send a first RAG question from a page on another origin, then a follow-up. The follow-up fails with a "CORS" error. Find the real bug.
*Answer:* The uvicorn terminal shows `TypeError: 'ChatMessage' object is not subscriptable` at `cheese-app-v2@2025/src/api-service/api/routers/llm_rag_chat.py:99`. Unhandled exceptions become 500s outside `CORSMiddleware`, so no `Access-Control-Allow-Origin` header. Fix: `message_dict["content"]`. (The 2025 React app is the easiest client; the 2025 simple frontend has no RAG option.)

**E5 (conceptual, state).** In HEAD's Identify mode, upload a cheese photo (you get, say, "brie, 93%"), then ask "How should I store it?". Does Gemini know what "it" is? Now save a file under `api/` (forcing a reload) and ask again. What changes?
*Answer:* Yes both times, and nothing changes: every message rebuilds the history from the saved chat file, where the `cnn` reply becomes "We have already identified the image of a cheese as brie" and the photo is re-attached (`cheese-app-v2/src/api-service/api/utils/llm_utils.py:54-76`). (In the 2025 code the first answer could *not* know, because the cached Gemini session never heard the label; only a reload rebuilt it from disk.)

**E6 (hands-on, contracts).** Add a field `"mode": "llm"` to a `POST /api/llm/chats` body in `/api/docs`. Then send `{"content": ""}`. Predict both responses.
*Answer:* The extra field is ignored (pydantic drops unknown fields), so you get a new chat. `{"content": ""}` → 422 "Message must contain text or an image" (`cheese-app-v2/src/api-service/api/routers/chat.py:36-37`), before any Gemini call.

**E7 (conceptual, RAG).** Someone "upgrades" only `EMBEDDING_MODEL` to another 256-dimensional model via env var, leaving Chroma alone. Nothing crashes. What breaks?
*Answer:* Retrieval quality, silently: query vectors live in a different space from the stored `text-embedding-004` vectors, so the top-5 chunks are essentially arbitrary. Re-embed with the same model on both sides (`cheese-app-v2/docs/contract.md:65`).

**E8 (hands-on, React Router).** Create `src/routes/About.jsx` that renders `<h1>About Formaggio</h1>`, add `<Route path="about" element={<About />} />` in `src/main.jsx`, and a `{ to: '/about', label: 'About' }` entry in `LINKS` in `App.jsx`. Predict the URL and whether you must restart `npm run dev`.
*Answer:* `http://localhost:3000/about`; no restart, Vite hot-reloads. The page gets the header/footer from `App.jsx`. In the production image, opening `/about` directly works because nginx falls back to `index.html` (`cheese-app-v2/src/frontend-react/nginx.conf.template:29-32`).

---

## 10. Errata and open questions

**Errata (with evidence)**
1. **Tutorial 24 removed from `main` while the course still links it.** The course site's "Frontend Simple" link (`…cheese-app-v2?tab=readme-ov-file#tutorial-24-simple-frontend-app`, read 2026-11-05) and the L18b slides teach the simple frontend; HEAD `e98fa55` has no such section or folder (`5104923` "removed frontend simple"). The 2025 version survives on branch `2025` (`14f2a14`).
2. **Slide links point at anchors that exist in neither version**: `#setup-environments`, `#frontend-app-simple`, `#frontend-app-react` (L18a slide 45, L18b slides 28 and 38) vs. the actual "Tutorial (23)/(24)/(25)" headings.
3. **HEAD README: "Do the Cheese Shop tutorial first"** (`cheese-app-v2/README.md:12-13`). No Cheese Shop tutorial is listed for L18 on the course site, and no public `dlops-io` repo of that name answered `git ls-remote`.
4. **Three H2s say "Tutorial (23)"** (HEAD `cheese-app-v2/README.md:25`, `:57`, `:86`; 2025 `:12`, `:40`, `:67`), and HEAD jumps from 23 to 25.
5. **Stale architecture images.** `cheese-app-v2/images/container-architecture-1.png` and `-2.png` (unchanged since 2025, still in HEAD's README tree at `:42`) show an older "Mushroom Identifier" app and are not referenced by the README.
6. **`--chat` ignores your question** (`cheese-app-v2/src/vector-db/cli.py:377`), though the README says "Try a question" (`cheese-app-v2/README.md:78`).
7. **Chat images keep a `.png` name whatever their format.** The browser uploads JPEG (`cheese-app-v2/src/frontend-react/src/lib/image.js:12`); the API writes the bytes to `<message_id>.png` and serves them as `image/png` (`cheese-app-v2/src/api-service/api/utils/chat_utils.py:35-43`, `cheese-app-v2/src/api-service/api/routers/chat.py:84`). Browsers sniff the real type, so it displays; the name and `Content-Type` are wrong.
8. **HEAD README cleanup misses the `node_modules` volume** (`cheese-app-v2/README.md:229-240`): `docker system prune` leaves `cheese-app-frontend-react-node_modules`.
9. **The book metadata in `vector-db/cli.py` names the instructor** (`cheese-app-v2/src/vector-db/cli.py:76`, also `agent_tools.py:28` and the `--agent` prompt at `cli.py:440`); it can surface in `--chat` output and in "Cheese books" answers about Tolminc cheese. Not an error in the code, but a masking requirement for this series.
10. **[2025] README steps describe an older `service.py`.** Adding `square_root` and "Enable all the routes" (`cheese-app-v2@2025/README.md:96-104`, `:116-138`) while the code already has `square_root` and four routers (`cheese-app-v2@2025/src/api-service/api/service.py:30-40`); pasting it again gives a duplicate route and FastAPI's `Duplicate Operation ID` warning in `/docs`.
11. **[2025] Router file names** `newsletters.py`/`podcasts.py` (`cheese-app-v2@2025/README.md:131-132`) are `newsletter.py`/`podcast.py`.
12. **[2025] "three containers" then four listed** (`cheese-app-v2@2025/README.md:3-7`); HEAD fixed this with a four-row table.
13. **[2025] RAG follow-up bug** at `cheese-app-v2@2025/src/api-service/api/routers/llm_rag_chat.py:99` (500 on every second RAG message); the identical CNN bug was fixed in `7e61318`. Gone at HEAD (routers rewritten).
14. **[2025] Two key file names** (`ml-workflow.json` vs `llm-service-account.json`); the README names only the first (`cheese-app-v2@2025/README.md:25`). HEAD uses one.
15. **[2025] Retired model** `gemini-2.0-flash-001` (`cheese-app-v2@2025/src/api-service/api/utils/llm_utils.py:22` and copies), retired June 1, 2026; HEAD moved to `gemini-3.8-flash` at `global`.
16. **[2025] "Review the code in `newsletters.html`/`chat.html`"** (`cheese-app-v2@2025/README.md:176`, `:181`): the logic is in `newsletters-main.js`/`chat-main.js`.
17. **[2025 and v1] Simple-frontend Dockerfile `ADD --chown=app:app . /app`** with no user `app` in `node:20-alpine` (`cheese-app-v2@2025/src/frontend-simple/Dockerfile:13`, `cheese-app-v1/src/frontend-simple/Dockerfile:13`). BuildKit falls back to uid 0 and builds; the legacy builder (`DOCKER_BUILDKIT=0`) fails with "no such user: app" (tested in October with a minimal Dockerfile on Docker 29.8.2).
18. **v1 README paths** "`cheese-app-v1/api-service`" and "`cheese-app-v1/frontend-simple`" (`cheese-app-v1/README.md:41`, `:75`) lack `src/`; the scripts' `../../../secrets` only resolves from `src/<service>`.
19. **Stale v1 README edit snippet** (`cheese-app-v1/README.md:88-95`, "🧀 Welcome to the cheese identification App!") predates the Formaggio page; pasted as a whole `<body>` it removes the page and the `main.js` script tag.

**Open questions (could not determine from the sources)**
1. **The Ed lesson's content** was not accessible. If Ed tells students to use the `2025` branch for everything, or a different repo, follow Ed.
2. **Whether `text-embedding-004` answers on the `global` endpoint.** HEAD assumes so (`cheese-app-v2/src/api-service/api/settings.py:7`, `:11`); untested here (no credentials). First real call in the captures decides.
3. **Whether the 2025 API (chromadb client 1.3.0) works with HEAD's `chromadb/chroma:1.5.9` server**, if someone mixes stacks. This digest avoids it by running the 2025 stack with its own compose file; untested.
4. **What `chromadb/chroma:latest` resolves to today** for the 2025 stack, and whether its client 1.3.0 still talks to it. Capture C1 to find out.
5. **The "Cheese Shop" tutorial** HEAD's README requires first: where it lives and whether L18 students are meant to do it.
6. **v3's `work/shivas` branch** (`976c4bb`): probably the same upgrade for L20/L22, not inspected.
7. **Vite's exact behaviour when the API is down** (status code and body the browser sees): the frontend shows either "Couldn't reach the API…" or "The API answered 500." depending on it. Capture D1 with the API stopped to know which.
