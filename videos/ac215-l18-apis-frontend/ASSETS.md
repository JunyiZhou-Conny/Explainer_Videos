# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** L18 runs entirely on the student's laptop
in Docker, so almost everything is captured live, on 2026-11-05, in a fresh, empty Docker engine
that stands in for that laptop: both repositories cloned, every `docker-shell.sh` built and run,
uvicorn/FastAPI answering, the demo routes added and reloaded, `/api/docs`, `pytest` (26 passed),
the vector DB loaded (14,356 chunks), the CNN identifying a cheese photo, the React dev server
(Vite) on 3000 with its `/api` proxy, `npm run check`, the nginx production image on 8080,
`docker compose up --build`, and the 2025 simple frontend calling the 2025 API with CORS. The only
thing that cannot run here is **Gemini on Vertex AI** (no Google account, no project, no key):
every Gemini call is captured up to its honest first error, `invalid_grant: account not found`,
and nothing in the video shows a Gemini answer (nothing in the repository documents one; see
"What cannot run here").

## Which commit

The course site's tutorials page links the repositories' default branches, unpinned. On
2026-11-05 `git ls-remote` (`terminal/laptop/p04-x-ls-remote.txt`) gave:

- **`dlops-io/cheese-app-v1`: `main` = `ce03a1029dd6f655a86e3e3edc99bb5938f0cbf8`**
  (2025-11-02 07:33:53 −0500, "gitignore"), the commit `units.json` names. Followed as is.
- **`dlops-io/cheese-app-v2`: `main` = `447b5c3c2c06d724e86dddf70e1a244dbe3d7c47`**
  (2026-11-05 07:52:33 −0500, "Merge pull request #2", whose one commit `55ffda8` is "updated
  readme + added docker compose"). **`main` moved twice on the recording day**: at 07:23 to
  `e98fa55` (the digest's pin: "removed frontend simple", "upgraded vector-db", "code cleanup",
  131 files), then at 07:52 to `447b5c3`. Between `e98fa55` and `447b5c3` only `README.md` and a
  new `src/docker-compose.yml` changed; every other file this video quotes is byte-identical
  (checked with `cmp`). The 2025 state is kept as branch **`2025` = `14f2a1420b43…`** (2025-11-16,
  "image chat fix"), the commit `units.json` and the published exam edition `videos/ac215-l16-exam/`
  name.

What the video follows, and why:

| README section | commit | why |
| --- | --- | --- |
| v1, whole README | `ce03a10` | `main`, unchanged |
| "Tutorial: Environment Setup / Vector DB for RAG Setup / Backend APIs" (the course's "Tutorial 23") | **`447b5c3`** (`main`) | what a student clones today. The code is `e98fa55`'s; the README dropped the "(23)" from the headings, so the course site's anchor `#tutorial-23-backend-apis` no longer exists |
| "Tutorial: React Frontend Setup" (the course's "Tutorial 25") | **`447b5c3`** | same; its "Review the app" and `npm run check` steps are unchanged; anchor `#tutorial-25-react-frontend-setup` is gone too |
| "Production images" (nginx, `cheese-app-frontend-react:prod`) | `e98fa55`'s README (lines 197-215) | **removed from the README at `447b5c3`** (replaced by "Setup & Run Cheese App"), but the production `Dockerfile` and `nginx.conf.template` are still in `main`, and the lecture's frontend deck covers serving built files. Captured as extras with the commands as `e98fa55` printed them (`d20`-`d28`) |
| "Tutorial: Setup & Run Cheese App" (`docker compose up --build`) | `447b5c3` | new on the recording day; captured (`f01`-`f11`) |
| **"Tutorial (24): Simple Frontend App"** | **`14f2a14`** (branch `2025`) | **`main` removed it** (commit `5104923` "removed frontend simple", no `src/frontend-simple/` at HEAD), but the lecture teaches it (frontend deck: the simple frontend on 8080 and `http-server`) and the course site still links its anchor. The 2025 pages call 2025 routes (`http://localhost:9000/newsletters`, `/llm/chats/`, CORS) that `main`'s API no longer serves (it has `/api/...` and no CORS), so the whole 2025 stack (vector DB + API + simple frontend) runs at `14f2a14` (`c01`-`c31`) |

The video says this kindly: "the course repository changed on the day we recorded; the simple
frontend now lives on the `2025` branch, `git switch 2025` to follow along, and `git switch main`
to come back."

## `source/` — the tutorial's own files

Copied unchanged with `git show <commit>:<path>`, at the repositories' relative paths, so a code
panel's `path · lines a–b` matches a viewer's clone. Executable bits as committed. Course material
by the AC215 teaching staff (Harvard IACS), used for study with the instructor's permission. The
`images/` folders (architecture PNGs) are not copied.

**Names (series rule).** `cheese-app-v1/src/frontend-simple/index.html:57` (and the same "About"
paragraph in `cheese-app-v2-at-14f2a14/src/frontend-simple/index.html`) and the book metadata in
`cheese-app-v2/src/vector-db/cli.py:76` contain the instructor's full name: a code panel that quotes
those lines masks it as `‹instructor›`. The terminal captures were masked at capture time (none
contained it in the end). The branch name `work/shivas` (and the merge subject "Merge pull request
#2 from dlops-io/work/shivas") names a teaching-staff member: it appears in `p03`, `p04`, `b01`,
`c01b`, `c31`; a scene that shows those lines crops or masks the branch name.

| folder | commit | files |
| --- | --- | --- |
| `cheese-app-v1/` | `ce03a10` | `README.md` (106 lines), `.gitignore`, `src/api-service/{Dockerfile, docker-shell.sh, docker-entrypoint.sh, pyproject.toml, uv.lock, api/service.py}`, `src/frontend-simple/{Dockerfile, docker-shell.sh, index.html, main.js, styles.css}` |
| `cheese-app-v2/` | `447b5c3` (`README.md`, `src/docker-compose.yml`); everything else identical at `e98fa55` | `README.md` (246 lines), `.gitignore`, `docs/contract.md`, `src/docker-compose.yml`; `src/vector-db/{Dockerfile, docker-shell.sh, docker-compose.yml, docker-entrypoint.sh, pyproject.toml, uv.lock, cli.py, .gitignore, .dockerignore}`; `src/api-service/{Dockerfile, Dockerfile.dev, docker-shell.sh, docker-entrypoint.dev.sh, pyproject.toml, uv.lock, .dockerignore, .gitignore}`, `api/**.py`, `tests/*.py`; `src/frontend-react/{Dockerfile, Dockerfile.dev, docker-shell.sh, docker-entrypoint.dev.sh, vite.config.js, package.json, package-lock.json, nginx.conf.template, index.html, eslint.config.js, .dockerignore, .gitignore, .prettierrc.json, .prettierignore}`, `src/**.{jsx,js,css}` |
| `cheese-app-v2-at-e98fa55/` | `e98fa55` | `README.md` only (240 lines): the "Tutorial (23)/(25)" headings and "Production images" (197-215) |
| `cheese-app-v2-at-14f2a14/` | `14f2a14` | `README.md` (247 lines; Tutorial (24) at 147-183); `src/frontend-simple/{Dockerfile, docker-shell.sh, index.html, index-simple.html, main.js, styles.css, newsletters.html, newsletters-main.js, newsletters-style.css, chat.html, chat-main.js, chat-style.css}`; `src/api-service/{Dockerfile, docker-shell.sh, docker-entrypoint.sh, pyproject.toml, api/service.py, api/routers/{newsletter, podcast, llm_chat}.py, api/utils/{llm_utils, chat_utils}.py}`; `src/vector-db/{Dockerfile, docker-shell.sh, docker-compose.yml, docker-entrypoint.sh, pyproject.toml}` |

Lines code panels are likely to quote (all checked against the copies):

| file | lines | what |
| --- | --- | --- |
| `cheese-app-v1/README.md` | 41, 44, 47, 52-58, 64-67, 75, 78, 82, 86-95, 100-106 | the v1 steps (API folder without `src/` at 41 and 75; the uvicorn line at 47; the `square_root` snippet 52-58; the stale `<body>` snippet 88-95; cleanup) |
| `cheese-app-v1/src/api-service/docker-shell.sh` | 13-21 | `docker build`, `docker run --rm --name … -ti`, the three `-v` mounts, `-p 9000:9000` |
| `cheese-app-v1/src/api-service/api/service.py` | 1-20 | `FastAPI(...)`, `CORSMiddleware(allow_origins=["*"])`, `GET /` |
| `cheese-app-v1/src/frontend-simple/Dockerfile` | 1-15 | `node:20-alpine`, `npm install -g http-server`, `ADD --chown=app:app` (no user `app` in the image) |
| `cheese-app-v1/src/frontend-simple/main.js` | 37-52 | "Sample Podcast Data (This would normally come from an API)" |
| `cheese-app-v2/README.md` | 3-10, 13-18, 20-50, 52-79, 81-145, 147-190, 192-221, 223-233, 235-246 | intro table, Prerequisites, the four "Tutorial:" sections, Troubleshooting, Docker Cleanup. Typos as printed: "http://localhost:900/api/docs" (213) |
| `cheese-app-v2/src/vector-db/docker-shell.sh`, `docker-compose.yml` | 1-17; 1-27 | network create, build, `docker compose run --rm`; Chroma `1.5.9` on 8000, `./docker-volumes/chromadb:/data` |
| `cheese-app-v2/src/api-service/docker-shell.sh` | 14-34 | network, "already running. Shelling into it..." (16-18), `docker run` with `/secrets:ro`, `--network cheese-app-network` |
| `cheese-app-v2/src/api-service/docker-entrypoint.dev.sh` | 9-27 | `uv sync --frozen`, the `api_server` function, the banner |
| `cheese-app-v2/src/api-service/api/service.py` | 19-56 | lifespan thread, `docs_url="/api/docs"`, `get_status` (31-33), routers (36-40), `/healthz`, `/readyz` |
| `cheese-app-v2/src/api-service/api/settings.py` | 5-23 | `GCP_PROJECT` required, `global`, `gemini-3.8-flash`, CNN URL |
| `cheese-app-v2/src/api-service/api/routers/chat.py` | 19-23, 35-43, 58-76 | UUID header, `add_turn`, start/continue routes |
| `cheese-app-v2/src/api-service/api/utils/llm_cnn_utils.py` | 26-69 | download + load in a thread, `make_prediction`, the 503 while loading |
| `cheese-app-v2/docs/contract.md` | 6-7, 31-44, 46-54 | "the API needs no CORS", chat shapes, status codes |
| `cheese-app-v2/src/frontend-react/vite.config.js` | 6-15 | `host: true`, 5173, `proxy: { '/api': … 'http://cheese-app-api-service:9000' }` |
| `cheese-app-v2/src/frontend-react/docker-shell.sh` | 15-23 | named volume over `/app/node_modules`, `-p 3000:5173` |
| `cheese-app-v2/src/frontend-react/src/lib/api.js` | 6-44 | session id in `localStorage`, `X-Session-ID`, relative `fetch` |
| `cheese-app-v2/src/frontend-react/Dockerfile`, `nginx.conf.template` | 1-16; 9-33 | two stages, `npm ci` + `vite build` → `nginx:1.31.8-alpine`; `/healthz`, `location /api/ { proxy_pass ${API_URL}; }`, SPA fallback |
| `cheese-app-v2/src/docker-compose.yml` | 1-68 | the four services, `vector-db-loader`'s `--get … || --download --load` entrypoint, `GCP_PROJECT` twice |
| `cheese-app-v2-at-14f2a14/README.md` | 147-183 | Tutorial (24): `cd cheese-app-v2/src/frontend-simple`, `sh docker-shell.sh`, `http-server`, the three pages |
| `cheese-app-v2-at-14f2a14/src/api-service/api/service.py` | 1-42 | CORS `allow_origins=["*"]`, `/square_root/` already present (30-33), four routers on, RAG/agent commented (37-42) |
| `cheese-app-v2-at-14f2a14/src/frontend-simple/newsletters-main.js`, `chat-main.js` | 3, 7; 2, 15-19, 30-32 | `baseURL: 'http://localhost:9000'`, `axios.get(…/newsletters?limit=…)`; the session header; `POST …/chats/` |

## `terminal/` — real terminal sessions

Captured on **2026-11-05** (UTC 12:58-14:16) by `terminal/capture.sh` + `terminal/run_steps.sh`.
Each file starts with the command (`$ ...`), then its output, then `[exit N]`. Interactive steps
(`docker-shell.sh` and everything typed at the container prompt, a server stopped with Ctrl-C) are
recorded in a pseudo-terminal by `terminal/ptyrun.py` (100×40): one file holds the whole session,
build output first. While a server runs in one terminal, a second shell runs the curl checks (each
its own file), exactly what "open http://localhost:… in your browser" asks. File names: `pNN`
setup, `aNN` v1, `bNN` Tutorial 23 (main), `dNN` Tutorial 25 + production image (main), `fNN` Setup &
Run (compose), `eNN` cleanup, `cNN` Tutorial 24 (branch 2025). **`-x-` in a name = extra** (not a
README step: a check the video uses, marked `extra` in the tracker).

| folder | environment |
| --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for the student's laptop: `docker:29.8.2-dind` (client + engine 29.8.2, Compose v5.6.0, linux/amd64), Alpine, user `student` (uid 1000) in the `docker` group, git 2.54.0, curl 8.23.0, python3, openssl. Its home folder is the README's parent folder: `cheese-app-v1/`, `cheese-app-v2/`, `secrets/`, `persistent-folder/` side by side |
| `laptop/capture-only/` | not tutorial steps: the capture-only base images (below), their build logs, the Docker Hub retry log, the placeholder key's shape |
| `expected/` | README / contract text for what cannot run here (below) |

Versions seen in the captures (say "at the time of recording"): v1 API image Python 3.12.16, uv 0.13.7
(the Dockerfile's unpinned `pip install uv`), FastAPI 0.120.4 / uvicorn 0.38.0 (v1 `uv.lock`);
main's API Python 3.13.18, uv 0.13.6 (pinned), FastAPI 0.162.0, uvicorn 0.54.0, TensorFlow-cpu
2.21.0, chromadb-client 1.5.9, google-genai 2.34.0, pytest 9.2.0; Chroma server `chromadb/chroma:1.5.9`
(REST API version "1.0.0"); Node v24.22.1, npm 11.19.1, Vite 8.3.5, nginx 1.31.8; `http-server`
14.1.1 on `node:20-alpine`; the 2025 stack: Python 3.12.16, uv 0.13.7, `chromadb/chroma:latest`
(image created 2026-05-05), TensorFlow 2.19.0. Image sizes on disk: main's API **4.2 GB** (790 MB
content), vector-db CLI 813 MB, React dev 331 MB, React prod **94.8 MB**, v1 API 860 MB, simple
frontend 218 MB.

### `laptop/` — setup (`p`)

| file | README step | what it shows |
| --- | --- | --- |
| `p00-x-env.txt` | extra | date, Docker 29.8.2, Compose v5.6.0, git 2.54.0, an empty image list |
| `p01-clone-v1.txt`, `p02-clone-v2.txt` | v1 README:17-18, v2 README:22-23 "Clone or download" (no command spelled out; the usual `git clone`) | `Cloning into 'cheese-app-v1'...` / `'cheese-app-v2'...` |
| `p03-x-git-log.txt`, `p04-x-ls-remote.txt` | extra ("Which commit") | `ce03a10`, `447b5c3`; remote branches incl. `origin/2025`; `refs/heads/2025` = `14f2a14` |
| `p05-mkdir.txt` | v1 README:20-36, v2 README:25-45 (the READMEs show the tree, not a command) | `mkdir -p secrets persistent-folder` — created by the student, so they are not root-owned (digest gotcha 5) |
| `p06-x-tree.txt` | extra (README:33-45 tree) | the side-by-side layout; `secrets/ml-workflow.json` (the placeholder, see below) |

### `laptop/` — cheese-app-v1 (`a`), `ce03a10`, the whole README

| file | README step | what it shows |
| --- | --- | --- |
| `a01-cd-readme-path.txt` | README:41 "go to … `cheese-app-v1/api-service`" | `cd: cheese-app-v1/api-service: No such file or directory`, exit 1: the README's path lacks `src/` (erratum) |
| `a02-x-cd-api-src.txt` | extra (the path that exists) | `cd cheese-app-v1/src/api-service && ls` |
| `a03-docker-shell-api.txt` | README:44 `sh docker-shell.sh` + README:47 the uvicorn line, typed verbatim incl. `"$@"` | BuildKit build (49.9 s: apt + uv), `Container is running!!!`, `Architecture: x86_64`, `Python 3.12.16`, `uv 0.13.7`, prompt `app@<id>:/app$`; uvicorn: `Uvicorn running on http://0.0.0.0:9000`, `Started reloader process [12] using StatReload`, `Application startup complete.`; after the edit `StatReload detected changes in 'api/service.py'. Reloading...`; the access log of every request below (incl. `422`, `307`); `^C`, `Stopping reloader process`, `exit` |
| `a04-curl-root.txt` | README:48 "Test … http://localhost:9000/" | `200`, `server: uvicorn`, `{"message":"Welcome to AC215"}` |
| `a05-edit-service.txt` | README:50-58 "Add the following code at the end of the file" (the editor's change, made with `cat >>`) | the appended route and `git diff` |
| `a06-curl-square-root.txt`, `a07-curl-square-root-params.txt` | README:59, :61 | `2.23606797749979`; `?x=2&y=10` → `10.198039027185569` |
| `a08-x-square-root-bad.txt`, `a09-x-square-root-no-slash.txt` | extra | `?x=abc` → 422 `float_parsing`; `/square_root` → `307 Temporary Redirect`, `location: …/square_root/` |
| `a10-docs.txt`, `a11-x-openapi.txt` | README:64-67 `/docs`; extra | `<title>API Server - Swagger UI</title>`, `url: '/openapi.json'`; the full OpenAPI JSON (x, y `number`, defaults 1 and 2) |
| `a12-x-docker-ps.txt` | extra | `cheese-app-api-service` `0.0.0.0:9000->9000/tcp` |
| `a19-cd-frontend-readme-path.txt`, `a20-x-cd-frontend-src.txt` | README:75 (again without `src/`); extra | `No such file or directory`; the real folder |
| `a20b-docker-shell-frontend.txt` | README:78 `sh docker-shell.sh` + README:82 `http-server` | the `node:20-alpine` build (`ADD --chown=app:app` builds under BuildKit although the image has no user `app`), prompt `<id>:/app#`, `http-server version: 14.1.1`, `Cache: 3600 seconds`, `Available on: http://127.0.0.1:8080 / http://172.18.0.3:8080` (container addresses), the request log, `^C`, `http-server stopped.` |
| `a21-curl-8080.txt` | README:83 | `200`, `cache-control: max-age=3600`, `<title>Formaggio.me</title>`, `🧀 Formaggio.me is here!`, `<script src="main.js">` |
| `a22-x-main-js.txt` | extra | `main.js:37` "Sample Podcast Data (This would normally come from an API)": the v1 page never calls the API |
| `a23-edit-index.txt`, `a24-curl-8080-after.txt` | README:85-97 (add a `<p>`) | the README's `<p>` text added inside the hero section (not the README's whole stale `<body>`, which would drop `main.js`), `git diff`; the new text served |
| `a25-x-cache-header.txt`, `a26-x-docker-ps.txt` | extra | `main.js` cached for 3600 s (why edits may need a hard refresh); both containers |
| `a30-docker-container-ls.txt`, `a31-docker-system-prune.txt`, `a32-docker-image-ls.txt` | README:100-106 Docker Cleanup | no containers left (`--rm`); the prune prompt `[y/N] y` (only build cache to delete); the images that stay |

### `laptop/` — cheese-app-v2 `main` (`b`): Environment Setup, Vector DB, Backend APIs

| file | README step (`447b5c3`) | what it shows |
| --- | --- | --- |
| `b01-x-git-log.txt`, `b02-x-ls.txt` | extra | `447b5c3`, `## main...origin/main`; `src/` has `api-service`, `docker-compose.yml`, `frontend-react`, `vector-db` |
| `b03-set-project.txt` | README:47-50 "Change `GCP_PROJECT` … in both files" | `sed` to the placeholder `your-gcp-project` + `git diff` (the repo's own default `ac215-project` on the `-` lines) |
| `b04-x-ls-secrets.txt` | extra (checkpoint) | `../secrets: ml-workflow.json`, empty `../persistent-folder` |
| `b05-cd-vector-db.txt` | README:58 | `cd src/vector-db` |
| `b06-docker-shell-vector-db.txt` | README:62 `./docker-shell.sh`, README:67 `python cli.py --download --load --chunk_type recursive-split`, README:75 `python cli.py --chat --chunk_type recursive-split`, README:78 `exit` | the network id printed by `docker network create`, the build (29.2 s), `chromadb/chroma:1.5.9 Pulled`, `Container cheese-app-vector-db Created`, the CLI container `vector-db-cheese-app-vector-db-cli-run-<id>` (Compose's run name, not `container_name`), banner (Python 3.13.18, uv 0.13.6, the three commands); load: `Created new empty collection 'recursive-split-collection'`, `Number of files to process: 11`, per book `Shape:`/`Inserted 500 items...`/`Finished inserting N items` — 923, 714, **3569**, 926, 2623, 1198, 1146, 678, 2147, 269, 163 = **14,356**; `--chat`: `chat()` then a traceback ending `google.auth.exceptions.RefreshError: ('invalid_grant: Invalid grant: account not found', …)` at the first Vertex call (the query embedding, `cli.py:378` → `:84`), exit 1 after `exit` |
| `b07-x-docker-ps.txt`, `b08-x-chroma-heartbeat.txt` | extra (README:78-79 "Chroma keeps running") | `cheese-app-vector-db` Up, `0.0.0.0:8000->8000/tcp`; `{"nanosecond heartbeat":…}`, API version `"1.0.0"` |
| `b09-x-host-folders.txt`, `b10-x-network.txt` | extra | `outputs/`: the zip + 11 `chunks-…` + 11 `embeddings-…` (78.8 MB), `docker-volumes/chromadb` 50.9 MB on the laptop; `cheese-app-network` holds `cheese-app-vector-db 172.19.0.2` |
| `b20-cd-api.txt` | README:88 | `cd src/api-service` |
| `b21-docker-shell-api.txt` | README:92 `./docker-shell.sh`, README:97 `api_server` | `Building cheese-app-api-service (Dockerfile.dev)...`, build **136.2 s** (`uv sync --frozen` + a long export: TensorFlow), banner + `Checked 84 packages`, the two commands; uvicorn `Started reloader process [16] using StatReload`, `Application startup complete.` at once, then TensorFlow's start-up lines (oneDNN, CPU features) from the lifespan thread; access log: `/readyz` 503 ×n then 200; `/` and `/docs` 404; `StatReload detected changes` + restart (the model reloads); every request below; three `ERROR: Exception in ASGI application` tracebacks ending in `RefreshError … account not found` (Ask, Cheese books, Ask via Vite); `^C`, `exit` |
| `b22-healthz.txt` | README:101 | `200 {"ok":true}` |
| `b23-readyz-loading.txt`, `b24-readyz-ready.txt` | README:102-103 | `503 {"detail":"CNN model is loading"}` at 13:49:35; `200 {"ok":true}` at 13:49:44 (download + load took ~9 s here) |
| `b25-x-old-urls.txt` | extra (digest gotcha 2) | `/` and `/docs` → `{"detail":"Not Found"}` 404 |
| `b26-x-persistent.txt` | extra | `persistent-folder/experiments/experiment_1760994796.zip` (9.0 MB), `data_details.json`, `mobilenetv2_train_base_True.keras` (and the zip's `__MACOSX/` folder) |
| `b27-edit-service.txt` | README:105-112 "add this after `get_status`" | the route inserted after line 33, `git diff` |
| `b28-curl-square-root.txt`, `b29-curl-square-root-3-4.txt` | README:114, :115 | `2.23606797749979`; `5.0` |
| `b30-x-readyz-after-reload.txt` | extra (gotcha 3) | `200` again shortly after the reload |
| `b31-api-docs.txt`, `b32-x-openapi-paths.txt` | README:119; extra | `<title>Cheese App API - Swagger UI</title>`, `url: '/api/openapi.json'`; all 25 operations (`/api/status`, `/api/square_root`, newsletters ×3, podcasts ×3, 5 per chat mode ×3, `/healthz`, `/readyz`); `info.version` `0.1.0` |
| `b33-get-newsletters.txt` | README:120 "Try `GET /api/newsletters`" (the curl the docs page shows, with `limit=2`) | curl's progress meter, then two newsletters, newest first ("Spanish Cheese Journey", "The Art of Blue Cheese") |
| `b34-x-newsletter-404.txt`, `b35-x-podcasts.txt` | extra | `{"detail":"Newsletter not found"}` 404; one podcast ("Spanish Cheese", 00:05:36), its MP3 `200 audio/mpeg 658930 bytes` |
| `b36-x-chat-no-session.txt`, `b37-x-chat-empty.txt` | extra (gotcha 7) | 422 `missing … X-Session-ID`; 422 `Message must contain text or an image` |
| `b38-x-chat-ask.txt` | extra (README:170 "Ask") | **`Internal Server Error` [HTTP 500]**: Gemini auth fails (see "What cannot run here") |
| `b39-x-chat-identify.txt` | extra (README:171 "Identify") | the repo's own `news-letters/assets/blue-cheese.jpg` sent as base64 → `200`, a chat with a `cnn` message: **`"prediction_label": "parmigiano", "accuracy": 58.22`** — real, offline; the CNN calls a blue cheese parmigiano (a good ponder) |
| `b40-x-chat-books.txt` | extra (README:172 "How is Tolminc cheese made?") | 500 (the embedding call fails the same way) |
| `b41-x-chats-list.txt`, `b42-x-chat-history.txt` | extra | the saved chat for session …0001 (user message with `image_path`, the `cnn` reply); `[]` for another session id; the files: `chat-history/llm-cnn/<session>/<chat>.json` + `chat-history/llm-cnn/images/<chat>/<message>.png` |
| `b43-x-cors-none.txt` | extra (digest 3.4, gotcha 12) | with `Origin: http://localhost:8080`: `200` and **no `access-control-*` header**; a preflight `OPTIONS` → `405 Method Not Allowed`, `allow: GET` (main has no CORS) |
| `b44-pytest.txt` | README:140-143 `pytest` (in a second terminal: `./docker-shell.sh` again) | `Container 'cheese-app-api-service' is already running. Shelling into it...`, `platform linux -- Python 3.13.18, pytest-9.2.0`, `cachedir: /home/app/.cache/cheese-app-api/pytest`, `collected 26 items`, `tests/test_chat.py` 17 + `tests/test_service.py` 9, **`26 passed in 0.51s`** |
| `b45-x-docker-ps.txt`, `b46-x-docker-images.txt` | extra | API + Chroma running; image sizes (API 4.2 GB) |

### `laptop/` — `main` (`d`): React Frontend Setup, and the production image

| file | README step | what it shows |
| --- | --- | --- |
| `d01-cd-frontend.txt` | README:152 | `cd src/frontend-react` |
| `d02-docker-shell-react.txt` | README:156 `./docker-shell.sh`, README:161 `npm run dev` | `Building cheese-app-frontend-react (Dockerfile.dev)...` (no app code in the image), `Node version: v24.22.1`, `npm version: 11.19.1`, `Installing dependencies...`, `added 257 packages in 7s`, npm's "new major version" notice, the two commands, prompt `node@<id>:/app$`; `VITE v8.3.5 ready in 297 ms`, `➜ Local: http://localhost:5173/`, `➜ Network: http://172.19.0.4:5173/` (container addresses: the laptop uses 3000); during `d09`: `[vite] http proxy error: /api/newsletters?limit=2`, `Error: getaddrinfo ENOTFOUND cheese-app-api-service`. Vite clears the screen when it starts: the run of blank lines before `VITE` is that, not output |
| `d03-curl-3000.txt` | README:164 "Open http://localhost:3000" | `200`, the dev `index.html`: `/@react-refresh`, `/@vite/client`, `<title>Formaggio</title>`, `<div id="root">`, `/src/main.jsx` |
| `d04-x-curl-3000-api.txt` | extra (README:13 old intro, contract.md:6-7) | `/api/newsletters` **through port 3000**: `200`, `server: uvicorn`: Vite forwarded it |
| `d05-x-curl-3000-main.txt` | extra | `/src/main.jsx` as Vite serves it (transformed JSX) |
| `d06-x-chat-via-3000.txt`, `d07-x-identify-via-3000.txt` | extra | Ask through the proxy → 500 (Gemini auth); Identify through the proxy → 200 with the `cnn` reply |
| `d08-x-routes.txt` | extra | `/`, `/podcasts`, `/newsletters`, `/chat?model=llm`, even `/nope` → `200 text/html` (client-side routing) |
| `d09-x-api-unreachable.txt` | extra (digest open question 7) | API disconnected from `cheese-app-network` for one request: the browser's `/api/...` gets **`502` with an empty body** from Vite |
| `d10-x-docker-ps.txt`, `d11-x-volume.txt` | extra | three containers, `0.0.0.0:3000->5173/tcp`; the named volume `cheese-app-frontend-react-node_modules` (207 entries, 193 MB) |
| `d12-npm-run-check.txt` | README:187-190 `npm run check` (second terminal: `./docker-shell.sh` shells in) | `eslint . && prettier --check . && vite build`: `All matched files use Prettier code style!`, `✓ 2385 modules transformed.`, the `dist/` listing (`index-DQWKRz1J.js 440.48 kB │ gzip: 137.31 kB`), `✓ built in 767ms` |
| `d20-x-docker-build-prod.txt` | extra: `e98fa55` README:203 `docker build -t cheese-app-frontend-react:prod .` (run as a script: BuildKit's plain progress) | stage `build`: `npm ci` (`added 257 packages … 4 moderate severity vulnerabilities`), `npm run build`; stage 2 `FROM nginx:1.31.8-alpine`, the template and `dist/` copied |
| `d21-x-docker-run-prod.txt` | extra: `e98fa55` README:207 | nginx's entrypoint: `Running envsubst on /etc/nginx/templates/default.conf.template to /etc/nginx/conf.d/default.conf`, `nginx/1.31.8`, worker processes, the access log (`/api/newsletters?limit=1` 200, `/newsletters` 200, `/assets/` 404); `^C` → `signal 2 (SIGINT) received, exiting` |
| `d22-curl-8080.txt` … `d26-x-docker-ps.txt` | `e98fa55` README:210 (open 8080); extras | `Server: nginx/1.31.8`, the built `index.html` with hashed `/assets/index-DQWKRz1J.js`; `/api/...` through nginx 200; nginx's own `/healthz` → `ok`; deep links → `200 text/html` (SPA fallback); container list |
| `d27-x-docker-images-grep.txt` | extra: `e98fa55` README:213-215 | `cheese-app-frontend-react:latest 331MB` vs **`:prod 94.8MB`** |
| `d28-x-image-history.txt` | extra | the prod image's layers: `COPY /app/dist` 766 kB on top of nginx |
| `e01-x-prod-without-api.txt` | extra (digest gotcha 11), after the API stopped | `[emerg] host not found in upstream "cheese-app-api-service" in /etc/nginx/conf.d/default.conf:14`, exit 1 |

### `laptop/` — `main` (`f`): "Tutorial: Setup & Run Cheese App" (new in `447b5c3`), and cleanup (`e`)

| file | README step | what it shows |
| --- | --- | --- |
| `f01-set-project-compose.txt` | README:195-196 "change `GCP_PROJECT` … in `src/docker-compose.yml`. It appears twice." | `sed` to the placeholder + `git diff` (two hunks) |
| `f02-docker-compose-down-vector-db.txt` | README:198-199 "`docker compose down` in `src/vector-db`" | Compose's warnings that `GOOGLE_APPLICATION_CREDENTIALS` / `GCP_PROJECT` are not set (they come from `docker-shell.sh`), then `cheese-app-vector-db` stopped and removed |
| `f03-cd-src.txt` | README:203 | `cd src` |
| `f04-docker-compose-up.txt` | README:207 `docker compose up --build`, README:218 Ctrl-C | `Building 0.5s (30/30)` (every image already built by the sections before), **`WARN a network with name cheese-app-network exists but was not created by compose. Set external: true`** and the same for the `node_modules` volume (warnings, not errors), four containers created incl. `src-vector-db-loader-1`, the Chroma banner (`Saving data to: /data`), uvicorn + TensorFlow lines, `up to date in 889ms`, `VITE v8.3.5 ready`, the access log, Ctrl-C shutdown |
| `f04-curl-3000.txt`, `f04-curl-api-docs.txt` | README:213 "Open http://localhost:3000 … /api/docs" | 200 `Formaggio`; 200 `Cheese App API - Swagger UI` on port **9000** |
| `f04-x-readme-url.txt` | extra (README:213 as printed) | `http://localhost:900/api/docs` → `curl: (7) Failed to connect to localhost:900` (typo for 9000) |
| `f04-x-compose-ps.txt`, `f04-x-loader-logs.txt` | extra | `src-vector-db-loader-1 Exited (0)` after its `--get` check found the books (no reload: the data from `b06` is in `vector-db/docker-volumes/chromadb`); its log is empty (output sent to `/dev/null`) |
| `f04-x-readyz.txt`, `f04-x-api-via-3000.txt` | extra | `/readyz` 200; a newsletter through Vite |
| `f10-docker-compose-down.txt`, `f11-x-left-over.txt` | README:219-221 | all four containers removed; the volume and `cheese-app-network` remain |
| `e02-docker-compose-down.txt` | README:237-240 (Docker Cleanup, in `src/vector-db`) | nothing left to remove ("No resource found …" after `f10`) |
| `e03-docker-system-prune.txt`, `e04-x-left-over.txt` | README:243-246; extra | `[y/N] y`, `Total reclaimed space: 5.328GB` (build cache); what `prune` keeps: every tagged image and the `node_modules` volume (digest erratum 8) |

### `laptop/` — branch `2025` = `14f2a14` (`c`): "Tutorial (24): Simple Frontend App" with its vector DB and API

| file | README step (`14f2a14`) | what it shows |
| --- | --- | --- |
| `c01-git-switch.txt` | extra (the switch the video asks for) | refused: `Your local changes to the following files would be overwritten by checkout:` (the project-id and demo-route edits) |
| `c01b-x-stash-switch.txt` | extra | `git stash && git switch 2025` → `branch '2025' set up to track 'origin/2025'` |
| `c02-x-git-log.txt` | extra | `14f2a14 … image chat fix`; `src/` has `frontend-simple` again |
| `c03-x-second-key-name.txt` | extra (digest erratum 14) | the same placeholder copied to `llm-service-account.json`, the name the 2025 vector-db script reads |
| `c04-x-set-project.txt` | README:23-25 / the scripts' "CHANGE TO YOUR PROJECT ID" | the two placeholder edits |
| `c05-cd-vector-db.txt` | README:46 | `cd cheese-app-v2/src/vector-db` |
| `c06-docker-shell-vector-db.txt` | README:51 `sh docker-shell.sh`, README:56 load, `exit` | the hyphenated `docker-compose run --rm --service-ports` works on this engine (`docker:29.8.2-dind` ships `docker-compose`; no shim was needed), `chromadb/chroma:latest Pulled`, banner (`Environment ready! Virtual environment activated.`, Python 3.12.16, uv 0.13.7), the same 11 files and 14,356 chunks |
| `c07-x-docker-ps.txt` | extra (digest open question 4) | `chromadb/chroma:latest` today = image created 2026-05-05; the 2025 client talks to it (the load and the API work) |
| `c10-cd-api.txt` | README:74 | `cd cheese-app-v2/src/api-service` |
| `c11-docker-shell-api.txt` | README:79 `sh docker-shell.sh`, README:92 `uvicorn_server` | build 79.0 s; `Started reloader process [11] using **WatchFiles**` (the 2025 lock has `watchfiles`), TensorFlow's CUDA-stub warnings (full `tensorflow` 2.19, no GPU), **`Loading CNN Model...` and the Keras model summary before `Application startup complete.`** (the 2025 API loads the CNN at import: start-up waits for it); access log: `GET /newsletters?limit=100` **307** → `GET /newsletters/?limit=100` 200; `OPTIONS /llm/chats` 200; `POST /llm/chats/` 307 → `POST /llm/chats` 500 with `Error generating response: ('invalid_grant: …')` |
| `c12-x-curl-root.txt`, `c13-x-square-root-present.txt`, `c14-x-routers.txt` | README:94 "Verify … http://localhost:9000"; README:96-108 and 116-138 (extras instead of pasting) | `{"message":"Welcome to AC215"}`; `/square_root/` is already in `service.py:30-33` (pasting the README's snippet again would duplicate it, erratum 10); four routers on, RAG/agent commented; the live route list (no `/api` prefix) |
| `c20-cd-frontend-simple.txt` | README:153 | `cd cheese-app-v2/src/frontend-simple` |
| `c21-docker-shell-frontend.txt` | README:158 `sh docker-shell.sh`, README:163 `http-server` | the same `http-server 14.1.1` start; the page requests; Ctrl-C |
| `c22-curl-index.txt` | README:170 `/index.html` | `200`, `Formaggio.me`, the two new nav links `/newsletters.html`, `/chat.html` (re-captured after the run with the same container image and a corrected grep, `http-server` started directly by `docker run`; the first version's pattern missed the leading `/`) |
| `c23-curl-newsletters-page.txt`, `c24-x-newsletters-js.txt` | README:174-176 | the page loads axios from a CDN and `newsletters-main.js`; the JS hard-codes `baseURL: 'http://localhost:9000'` and calls `/newsletters?limit=…` (no slash) |
| `c25-x-browser-newsletters.txt` | extra: what that page's `axios.get` sends, with the browser's `Origin: http://localhost:8080` | `307` (`location: …/newsletters/?limit=100`) then `200`, both with **`access-control-allow-origin: *`** |
| `c26-curl-chat-page.txt` | README:179 | `chat.html` with axios + marked + `chat-main.js` |
| `c27-x-browser-preflight.txt` | extra: the browser's CORS preflight for the chat POST (custom `X-Session-ID` header) | `200`, `access-control-allow-origin: *`, `allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`, `max-age: 600`, `allow-headers: content-type,x-session-id` |
| `c28-x-browser-chat.txt` | extra: README:180 "How is cheese made?" as the page sends it | `307` → `500` `{"detail":"Failed to generate response: ('invalid_grant: …')"}` — with the CORS header, so a browser would show the error, not a CORS failure |
| `c29-x-docker-ps.txt`, `c30-x-stop.txt`, `c31-x-git-switch-main.txt` | extra | the three 2025 containers (8080, 9000, 8000); Chroma stopped; back to `main` |

## What cannot run here, and how the video shows it

| step | why | how it is shown |
| --- | --- | --- |
| Prerequisites: a GCP project with the Vertex AI API, the `ml-workflow.json` key with Vertex AI User (README:15-17) | no Google account, project or key in the recording sandbox | a schematic console drawing tagged `illustration` (no screenshot, no logo), with the names from `expected/01-prerequisites.txt` (README:13-18 + `ml-workflow` README:100-112, L15) |
| The key file itself | no credentials may exist here | `secrets/ml-workflow.json` is a well-formed service-account file around a **throwaway RSA key generated at capture time for no account** (never written to this repository; its shape with the key removed is `laptop/capture-only/placeholder-key.json`): project `your-gcp-project`, account `placeholder-not-a-real-account@…`. Google's libraries load it, so everything that does not call Google works exactly as for a student, and the first Google call fails honestly |
| Every Gemini / embedding answer: `cli.py --chat` (`b06`), Ask and Cheese books (`b38`, `b40`, `d06`), the 2025 chat (`c28`) | needs Vertex AI | the real captured failure: `RefreshError: ('invalid_grant: Invalid grant: account not found', …)`; the API answers `500 Internal Server Error` (main: the `RefreshError` is not a `genai` `APIError`, so `ask_gemini`'s `502 "Gemini: …"` mapping does not catch it; 2025: `500 {"detail":"Failed to generate response: …"}`). The video says: "with your real key, this is where Gemini's answer appears". It shows **no answer text**: no README, repo file or notebook documents one. The shape of a successful reply is `expected/02-chat-contract.txt` (`docs/contract.md:31-44`), tagged `expected` |
| The browser views (Home, Podcasts, Newsletters, Chat with Recent) | no browser in the sandbox | the pages' HTML, routes and API calls are captured with curl (`d03`-`d08`, `d22`-`d25`, `a21`, `c22`-`c28`); the browser itself is a schematic drawing tagged `illustration`, following `expected/03-review-the-app.txt` (README:166-174) |
| Troubleshooting rows "Gemini: 403 / 404" (README:230-231) | need a real project | quoted from `expected/04-troubleshooting.txt`, tagged `recorded` (README text). The live captures add what a rejected key looks like (500 + `RefreshError`) |

## `capture-only` — what the recording sandbox changed, and why

None of these is a tutorial step; none appears in a scene as one.

- **Proxy.** The sandbox reaches the internet only through an HTTPS proxy on the host's loopback
  that re-signs TLS. `terminal/proxy_relay.py` (container `l18-relay`) makes it reachable from
  Docker's bridge; the laptop's Docker client config passes it to every build and container.
- **Base images with the proxy's CA.** `python:3.12-slim-bookworm`, `python:3.13-slim-bookworm`,
  `node:20-alpine` and `node:24.22.1-bookworm-slim` were rebuilt inside the laptop with that CA
  (+ https Debian sources, `SSL_CERT_FILE`/`REQUESTS_CA_BUNDLE`/`PIP_CERT`/`UV_SYSTEM_CERTS`,
  `NODE_EXTRA_CA_CERTS`) and re-tagged under the same names, so every tutorial Dockerfile builds
  unchanged (`laptop/capture-only/*-base.Dockerfile` + build logs). `chromadb/chroma` and
  `nginx:1.31.8-alpine` download nothing and are used as published. Docker Hub's anonymous rate
  limit was hit while pulling bases; `capture-only/hub-retries.txt` counts the retries.
- **Docker's image store for part `c`.** The 2025 API image (full TensorFlow 2.19 + chromadb with
  onnxruntime) ran the recording disk out of space while exporting under the containerd image
  store (Docker 29's default, which keeps big layers about twice during a build): the first attempt
  failed with `no space left on device` and was discarded. Part `c` was recorded on a fresh laptop
  (`capture.sh setup-classic`) with Docker's classic `overlay2` image store, after `reset-old`
  re-created the state `c01`-`c04` had left (both clones, the placeholder keys, `git switch 2025`,
  the project id). Nothing a student sees depends on the image store; on a laptop, budget the
  README's "about 10 GB" per stack.
- **Order.** Parts were recorded `p`, `a`, `b`+`d`+`f`+`e` (one run, the API kept running across
  `b` and `d` as the README says: "Keep this container running"), then `c`. The `b`/`d`/`f`/`e` run
  was recorded twice: the first produced the same results but its base images set a deprecated uv
  variable (`UV_NATIVE_TLS`) whose warning appeared in the banner; the second, kept here, starts
  from an empty engine and a fresh clone (`capture.sh prune bases reset-v2 head`).
- **Readiness probes** (`wait_http`, `wait_code`) and the cue files that tell a server's terminal
  to press Ctrl-C send their own quiet requests: the extra `GET /`, `GET /healthz` and `/readyz`
  lines in the servers' access logs come from them.
- **Name masking.** `run_steps.sh` reads the instructor's name from the v1 page at run time and
  replaces it by `‹instructor›` in every capture; no capture contained it.

## Re-running

```bash
export HTTPS_PROXY=...   CA_BUNDLE=/path/to/proxy-ca.pem   # only behind the recording proxy
bash assets/terminal/capture.sh setup pre v1 head
bash assets/terminal/capture.sh teardown setup-classic reset-old old-run   # part c, as recorded
bash assets/terminal/capture.sh teardown && docker rm -f l18-relay
```

`old` (the `c01`-`c04` switch from the edited `main` checkout) runs after `head` on the same laptop.
Clean-up after the recording: the laptop container and its volume, the relay and the two host images
(`docker:29.8.2-dind`, `python:3.12-slim-bookworm`) were removed.
