# Exercise checks · ac215-l18-apis-frontend (2026-11-05, 15:31–15:48 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/laptop/`, which
the answers cite directly (`a…` v1, `b…`/`d…`/`f…`/`e…` `main`, `c…` branch `2025`; provenance in
[`ASSETS.md`](../../ASSETS.md)). The check scripts and their logs are in [`logs/`](logs/). Every step in a log starts
with its command (`$ …`) and ends with `[exit N]`, as in `assets/terminal/run_steps.sh`; where a step pipes into
`grep` or `tail`, `[exit N]` is the last command's status. In the logs, `$SCRATCH` stands for the session's scratch
folder, `<logs>` for this `logs/` folder and `$HTTPS_PROXY` for the session proxy.

There was **no Google account, no GCP project and no key**: `GOOGLE_APPLICATION_CREDENTIALS` was never set and
`GCP_PROJECT` was the placeholder `your-gcp-project`. Nothing called Gemini or the embedding model successfully; the
one chat that tried (B5) failed at the credential lookup. No log contains a person's name, a key or a real project
ID; the session ID is the captures' placeholder `00000000-0000-4000-8000-000000000001`.

## Setup (disposable; nothing from the repositories ran on the host)

- Docker Engine 29.8.2 on the session machine. Code: v1's `api/service.py` at `ce03a10` (from `assets/source/`);
  `main`'s `src/api-service/` and `src/frontend-react/nginx.conf.template` from a `git archive` of the read-only
  clone at `e98fa55`, byte-identical to `447b5c3` for every file under `src/api-service/` (checked with `cmp` against
  `assets/source/cheese-app-v2/`; only the README and `src/docker-compose.yml` changed between the two commits).
  Each was copied into a scratch folder and mounted at `/app`, as `docker-shell.sh` mounts your code.
- [`setup.sh`](logs/setup.sh) ([`setup.log`](logs/setup.log)) builds two **check-only** images (not tutorial
  files; the session proxy's CA is added so pip, uv and apt can download):
  - [`py312-check.Dockerfile`](logs/py312-check.Dockerfile) → `l18ex/py312:check`: `python:3.12-slim-bookworm`
    (Python 3.12.16) with v1's `uv.lock` versions of the four packages `service.py` needs (FastAPI 0.120.4,
    Starlette 0.49.3, pydantic 2.12.3, uvicorn 0.38.0) and curl, user `app` (uid 1000).
  - [`api313-check.Dockerfile`](logs/api313-check.Dockerfile) → `l18ex/api313:check`: `python:3.13-slim-bookworm`
    (Python 3.13.18), uv 0.13.6 and user `app` as in `Dockerfile.dev`, every package of `main`'s `uv.lock` (dev
    group included: FastAPI 0.162.0, uvicorn 0.54.0, chromadb-client 1.5.9, google-genai 2.34.0, pytest 9.2.0)
    **except TensorFlow**. **Difference from the real image:** no TensorFlow, so the CNN never loads in it. The API
    imports TensorFlow only inside `load_cnn_model` and `make_prediction` (`llm_cnn_utils.py:27`, `:46`), so
    everything else runs as in the real container; where a check needs the model step to finish, a stand-in module
    [`tfstub/tensorflow/__init__.py`](logs/tfstub/tensorflow/__init__.py) (check-only, *not* TensorFlow) returns a
    placeholder from `load_model`. Nothing in these checks predicts a cheese; the real CNN's answer is the capture
    `b39`.
- [`vite-check.Dockerfile`](logs/vite-check.Dockerfile) → `l18ex/vite:check` (built by [`vite.sh`](logs/vite.sh)):
  `node:24.22.1-bookworm-slim` (Dockerfile.dev's base) with only `vite@8.3.5` (the version in `package-lock.json`)
  and curl. No React, no app code: B7 is about the proxy alone.
- Docker Hub answered `429 Too Many Requests` to the `chromadb/chroma:1.5.9` and `node` pulls, so those two came
  from `mirror.gcr.io` (Google's Docker Hub mirror). The Chroma image's digest,
  `sha256:1e0b73a187a2…` ([`api.log`](logs/api.log)), is the image ID the captures' `chromadb/chroma:1.5.9` shows
  (`e04`). `nginx:1.31.8-alpine`, `python:3.12-slim-bookworm` and `python:3.13-slim-bookworm` came from Docker Hub.
- [`lib.sh`](logs/lib.sh): the `step` function. Every check publishes host ports **19000, 18080, 13000** where the
  README uses 9000, 8080, 3000, and names its containers and network `l18ex-…`, so nothing could collide with other
  work on the machine.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| B1 | [`v1.sh`](logs/v1.sh) "B1": uvicorn `--host 127.0.0.1`, then `0.0.0.0`, published `-p 19000:9000` ([`v1.log`](logs/v1.log)) | 127.0.0.1: inside the container `{"message":"Welcome to AC215"}`; from the host `curl: (56) Recv failure: Connection reset by peer` while `docker port` shows `9000/tcp -> 0.0.0.0:19000`; 0.0.0.0: the welcome from the host |
| B2 | `v1.sh` "B2, B3": the README's uvicorn line with `--reload`, the README's `square_root` and a `/hypot/{x}` route appended | `StatReload detected changes in 'api/service.py'. Reloading...`; `5.0`, `3.0`, `422` with `"loc":["path","x"]`; OpenAPI: `x path required`, `y query optional`, default 0 |
| B3 | same; and [`api.sh`](logs/api.sh) "B3, B5" on `main`'s API ([`api.log`](logs/api.log)) | v1 `/square_root?x=3&y=4` → `307`, `location: …/square_root/?x=3&y=4`; `-L` → `5.0` after 1 redirect; POST → 307, followed → `405 {"detail":"Method Not Allowed"}`; `?x=abc` → 422 `"loc":["query","x"]`. `main`: `/api/newsletters/?limit=1` → 307 to `/api/newsletters?limit=1`; POST `/api/llm/chats/` → 307 to `/api/llm/chats` |
| B4 | `v1.sh` "B4": two simultaneous requests to a 2-second `time.sleep` route, `async def` and `def` | `two requests to /slow_async took 4.0 s`; `… /slow_def took 2.0 s` |
| B5 | `api.sh` "B3, B5": the chat routes of `main`'s API, no key | no header → 422 `missing`; `X-Session-ID: string` and `../../etc` → 422 `string_pattern_mismatch`; `{"content":""}` → 422 `Message must contain text or an image`; an image in `llm-cnn` with no model → 503 `The CNN model is still loading`; `{"content":…,"mode":"llm"}` → `Internal Server Error` 500, log `google.auth.exceptions.DefaultCredentialsError`; `persistent/` stays empty (nothing saved) |
| (A, setup) | `api.sh`: `pytest -q` in the check image | `26 passed in 0.61s` (the capture `b44` shows the same 26 in the real image) |
| C2, Q3 | `api.sh` "C2": a root-owned folder (`drwxr-xr-x root root`) mounted at `/persistent`, the TF stand-in on `PYTHONPATH` | `Application startup complete.`, then `PermissionError: [Errno 13] Permission denied: '/persistent/experiments'`; `/readyz` still `503 {"detail":"CNN model is loading"}` 10 s later; Identify → 503 `The CNN model is still loading` |
| C3, Q3 | `api.sh` "C3": model files in place (placeholders, read only by the stand-in), API and Chroma 1.5.9 on a private network, Chroma aliased `cheese-app-vector-db` | before Chroma: `/healthz` 200, `/readyz` `503 {"detail":"Chroma: Could not connect to a Chroma server. Are you sure it is running?"}`; Chroma started (fresh, no collection) → `200 {"ok":true}`; stopped → `503 {"detail":"Chroma: [Errno -2] Name or service not known"}`; started again → 200. The API was never restarted |
| B6 | [`nginx.sh`](logs/nginx.sh) "B6": nginx 1.31.8 with `main`'s template, `API_URL` as the production Dockerfile sets it, a two-file `dist/`, the API as `cheese-app-api-service` ([`nginx.log`](logs/nginx.log)) | `/healthz` 200 text/plain; `/api/newsletters?limit=1` 200 application/json, `Server: nginx/1.31.8`, `['Spanish Cheese Journey']`, API log `GET /api/newsletters?limit=1`; `/newsletters`, `/chat?model=llm` 200 text/html; asset 200 with `Cache-Control: public, max-age=31536000, immutable`; `/assets/nope.js` 404; `/nope.js` 200 text/html; pages `Cache-Control: no-cache` |
| C4 | `nginx.sh` "C4", "C4 (b)" | no API: `[emerg] host not found in upstream "cheese-app-api-service" in /etc/nginx/conf.d/default.conf:14`, exit code 1 (as `e01`); API stopped after nginx started: `/api/…` → `504`, `upstream timed out (110: Operation timed out) while connecting to upstream`; `/newsletters` still 200 |
| C5 | `nginx.sh` "C5": `proxy_pass ${API_URL}/;` | `{"detail":"Not Found"} [HTTP 404]`; API log `"GET /newsletters?limit=1 HTTP/1.1" 404 Not Found` |
| C6 | `v1.sh` "C6": v1's `CORSMiddleware`, a `HTTPException(500)` route and a `1 / 0` route, then the middleware removed (`grep -c` still finds 1 line: the import) | with: GET → `access-control-allow-origin: *`; preflight → 200, `allow-methods: DELETE, GET, HEAD, OPTIONS, PATCH, POST, PUT`, `max-age: 600`, `allow-headers: content-type,x-session-id`; `/handled` → 500 **with** the header; `/boom` → `Internal Server Error` 500 **without** it, `ZeroDivisionError` in the log. Without: GET 200, no header; preflight `405 Method Not Allowed`, `allow: GET` (as `b43` on `main`) |
| B7 | [`vite.sh`](logs/vite.sh): Vite 8.3.5 with `main`'s `server` block, proxy target unchanged, then `'http://localhost:9000'` ([`vite.log`](logs/vite.log)) | by name: `200`, `server: uvicorn`; localhost: `502 Bad Gateway`, `[vite] http proxy error: /api/newsletters?limit=1`, `Error: connect ECONNREFUSED 127.0.0.1:9000` |
| C8 | [`shell.sh`](logs/shell.sh): a stand-in with `docker-entrypoint.dev.sh`'s bash mechanics (define, `export -f`, `exec /bin/bash`), then `docker exec` ([`shell.log`](logs/shell.log)) | PID 1's environment holds `BASH_FUNC_api_server%%`; in the exec'd shell `type: api_server: not found`. That `pytest` works in the second shell is the capture `b44` |

## Not run (and why)

- **Anything with Gemini or the embedding model**: needs a Google project and key. The answers use the code, the
  captured first errors (`b06`, `b38`, `b40`, `c28`) and `docs/contract.md`, and say so.
- **The real TensorFlow model in these checks**: the 2 GB wheel was left out of the check image; the model's
  real download, load and prediction are in the captures (`b21`, `b24`, `b26`, `b39`). A first attempt at C3 let the
  stand-in download the model packet from GitHub through the session proxy, which answered `504 Gateway Time-out`;
  the check then used placeholder files instead (the stand-in never reads them).
- **A browser**: the browser's CORS decisions (hiding an answer, the console message) were not observed; the checks
  send the browser's requests with curl (`Origin`, the preflight headers) and read the headers a browser decides on.
  Swagger UI's own behaviour in `/api/docs` was not checked.
- **D1–D4** are reasoning questions; their facts come from the code, the captures and the checks above.

## Cleanup

Every check container was removed by name and each script's last step counts 0 containers named `l18ex-…`; the
networks `l18ex-net` were removed. The images `l18ex/py312:check`, `l18ex/api313:check`, `l18ex/vite:check` and the
pulled bases were deleted afterwards. Nothing was written outside the containers, the session's scratch folder and
this folder.
