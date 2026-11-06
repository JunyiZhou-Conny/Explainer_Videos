# Exercises · AC215 L18 — APIs and frontend: a FastAPI service, a simple page and a React app

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-05 (`assets/terminal/laptop/`: a fresh Docker 29.8.2 engine standing in for your laptop,
both clones side by side, provenance in [`ASSETS.md`](ASSETS.md)), and the extra checks run for
these exercises, listed with their scripts and logs in
[`assets/exercise-checks/`](assets/exercise-checks/README.md). The repositories are
`dlops-io/cheese-app-v1` at `ce03a10` and `dlops-io/cheese-app-v2` at `447b5c3` (`main`), with
Tutorial 24 from branch `2025` (`14f2a14`); `README:NN` means line NN of v2's README at `447b5c3`,
`v1 README:NN` the v1 README. Nothing here used a Google account or key: whatever needs Gemini is
answered from the code and the captured first error, and the answer says so. Versions are those at
the time of recording; yours may be newer. The checks publish host ports 19000, 18080 and 13000
where the README uses 9000, 8080 and 3000: use the README's ports.

---

## Part A · The five questions from the end of the video

**Q1. Trace one newsletters request on `main` through the lecture's steps. Which container does
the browser talk to, and at which step does the API's port come in?**

<details><summary>Answer</summary>

The browser talks only to the **frontend container**, `cheese-app-frontend-react`, through
`localhost:3000`. Port 9000 comes in at the step the lecture never draws, **3½: the courier**.

1. **Request:** the page asks for a *relative* path, `useGet('/api/newsletters?limit=2')`
   (`src/routes/Home.jsx:40`), which `fetch(path, …)` sends (`src/lib/api.js:44`) to the page's own
   origin, `http://localhost:3000`.
2. **Forward to the published port:** Docker maps the laptop's 3000 to the container's 5173
   (`-p 3000:5173`, `src/frontend-react/docker-shell.sh:21`; `d10`: `0.0.0.0:3000->5173/tcp`).
3. **Into the container:** Vite listens on 5173 on every interface (`host: true`,
   `vite.config.js:10`).
3½. **The courier:** Vite's proxy rule sends everything under `/api` to
   `http://cheese-app-api-service:9000` (`vite.config.js:13`): the API container **by name**, on
   `cheese-app-network`. This is where 9000 appears.
4. **The function runs:** uvicorn hands the request to FastAPI, which matches the router mounted at
   `/api/newsletters` (`api/service.py:36`) and runs `get_newsletters` (`routers/newsletter.py:16-25`).
5. **The response** goes back the same way, through Vite: `d04` shows `server: uvicorn` on a
   request to port **3000**.
6. **The page shows it.**

The API's own published port (`-p 9000:9000`) is **not** on this path: it is for you (`/api/docs`,
the probes, curl). Unplug the API from the network and the browser's call fails at step 3½ with
`502` from Vite (`d09`), although 9000 is still published.
</details>

**Q2. What do `api.service:app`, `--host 0.0.0.0` and `--reload` each do, and why does
`/square_root` answer 307?**

<details><summary>Answer</summary>

- **`api.service:app`** is an address, not a file name: import the module `api.service` (folder
  `api/`, file `service.py`, relative to the working directory `/app`) and use its variable `app`,
  the `FastAPI(...)` object (v1 `api/service.py:5`). uvicorn is the **server** (it owns the port and
  speaks HTTP); FastAPI is the **app** it calls.
- **`--host 0.0.0.0`**: listen on every interface of the container: its own loopback *and* its
  network interface, where Docker's port forwarding arrives. With `127.0.0.1` the container can
  reach itself but your browser can't (Part B1).
- **`--reload`** (with `--reload-dir api/`): a reloader process watches `api/` and restarts the app
  when a file changes: `StatReload detected changes in 'api/service.py'. Reloading...` (`a03`). That
  is why saving the file is enough.

**307:** the README declares the route **with** a trailing slash, `@app.get("/square_root/")`
(v1 README:54). A request to `/square_root` matches nothing, and FastAPI (Starlette's
`redirect_slashes`) answers `307 Temporary Redirect` with `location: …/square_root/` (`a09`). A
browser follows it silently; curl needs `-L`. 307, unlike 301/302, keeps the method and body, so even
a POST is redirected as a POST (Part B3). On `main` the demo route has no slash
(`/api/square_root`, README:108), and there the slash version is the one that gets redirected.
</details>

**Q3. `/healthz` vs `/readyz`: what does each one check in this API?**

<details><summary>Answer</summary>

- **`/healthz`** (liveness, `api/service.py:43-45`) checks nothing: if the process can run a route,
  it answers `200 {"ok":true}`. It said 200 while `/readyz` said 503 (`b22`, `b23`).
- **`/readyz`** (readiness, `api/service.py:48-56`) checks two things, in order: the **CNN model is
  loaded** (`503 {"detail":"CNN model is loading"}` until the background thread finishes, `b23`;
  `200` about nine seconds later, `b24`), and **Chroma answers a heartbeat** (`503 {"detail":"Chroma:
  …"}` otherwise; exercise check C3: `Chroma: Could not connect to a Chroma server. Are you sure it
  is running?`).

What `/readyz` does **not** check: Gemini, your key or project (the exercise check reached `200`
with no Google credentials at all), or whether the books are loaded (it reached `200` against a
fresh, empty Chroma; Cheese books would then say "The vector DB is empty", README:229). Liveness
answers "should this process be restarted?"; readiness answers "should it get traffic yet?"
(Part D2).
</details>

**Q4. Where does a chat stay between two messages, and why can any copy of the API answer it?**

<details><summary>Answer</summary>

In a **file**. `ChatHistoryManager` saves each chat as
`/persistent/chat-history/<mode>/<session id>/<chat id>.json`, and each image beside it under
`images/<chat id>/<message id>.png` (`api/utils/chat_utils.py:28-60`). `/persistent` is your
`persistent-folder/` on the laptop: `b42` lists
`persistent-folder/chat-history/llm-cnn/00000000-0000-4000-8000-000000000001/<chat>.json` and the
photo under `llm-cnn/images/…`. The browser keeps the session ID (a random UUID in
`localStorage`, `src/lib/api.js:17-29`) and sends it as `X-Session-ID` with every call.

On every message, the route opens that file, rebuilds the conversation from it, adds your message
and the reply, saves, and forgets (`routers/chat.py:35-43`, 69-76; README:135-136: "Nothing about a
chat stays in memory"). So any copy of the API that **sees the same files** can answer the next
message. The catch: "the same files". Two copies on two machines with two separate disks would not
find each other's chats (Part D1).
</details>

**Q5. Which file decides where `/api` goes in development, which in production, and why did the
2025 API need `CORSMiddleware` while `main`'s does not?**

<details><summary>Answer</summary>

- **Development:** `src/frontend-react/vite.config.js`, line 13:
  `proxy: { '/api': process.env.API_URL || 'http://cheese-app-api-service:9000' }`.
- **Production:** `src/frontend-react/nginx.conf.template`, lines 13-14:
  `location /api/ { proxy_pass ${API_URL}; … }`, with `API_URL=http://cheese-app-api-service:9000`
  set in the production `Dockerfile` (line 13) and filled in by nginx's entrypoint when the container
  starts (`d21`: `Running envsubst on /etc/nginx/templates/default.conf.template`).

**CORS:** the 2025 simple frontend was served by `http-server` on **8080**, and its JavaScript
called the API at **9000** directly (`newsletters-main.js:3` `baseURL: 'http://localhost:9000'`,
`chat-main.js:2`). Same host, different port, so a **different origin**: the browser reads the
answer to the page only if the API says it may, with `access-control-allow-origin: *` (`c25`), and
for the chat POST (JSON plus a custom `X-Session-ID` header) it first sends an `OPTIONS` preflight
(`c27`). `main`'s page calls its **own** origin and Vite or nginx forwards: same origin, nothing to
permit, so the API dropped the middleware (`docs/contract.md:6-7`: "the API needs no CORS"). What
changed is the origin the page calls, not the browser and not the API's security.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Which interface?** In the v1 API container (`sh docker-shell.sh` in
`cheese-app-v1/src/api-service`), start uvicorn with `--host 127.0.0.1` instead of `0.0.0.0`:

```bash
uvicorn api.service:app --host 127.0.0.1 --port 9000 --reload --reload-dir api/
```

Predict, then try: (a) `curl -s http://localhost:9000/` from a second shell **inside** the container
(`docker exec -it cheese-app-api-service bash`); (b) `http://localhost:9000/` from your laptop.

<details><summary>Answer</summary>

(a) Works: `{"message":"Welcome to AC215"}`. (b) Fails: `curl: (56) Recv failure: Connection reset
by peer` (a browser shows "connection was reset"), although `docker port` still says
`9000/tcp -> 0.0.0.0:…` (exercise check B1). Docker's forwarded connection arrives on the
container's network interface, not on its loopback, and nothing listens there. Restart with
`--host 0.0.0.0` and (b) answers. This was the video's first ponder; the lecture's slide labels the
inside "localhost:9000", which is true only from inside the container.
</details>

**B2. Path or query?** Add a second route to v1's `api/service.py` and save:

```python
@app.get("/hypot/{x}")
async def hypot(x: float, y: float = 0):
    return (x**2 + y**2) ** 0.5
```

Predict `/hypot/3?y=4`, `/hypot/3` and `/hypot/abc`, and what `/docs` says about `x` and `y`.

<details><summary>Answer</summary>

`5.0`, `3.0`, and `422` with `{"type":"float_parsing","loc":["path","x"],"msg":"Input should be a
valid number, unable to parse string as a number","input":"abc"}` (exercise check B2). A name in
`{…}` in the path becomes a **path** parameter, always required; any other argument is a **query**
parameter, optional when it has a default. The OpenAPI schema behind `/docs` says exactly that:
`x path required number`, `y query optional number, default 0`. You restarted nothing: the log shows
`StatReload detected changes in 'api/service.py'. Reloading...`. Compare the video's
`?x=abc`: same 422, but `"loc":["query","x"]`.
</details>

**B3. Follow the slash.** Predict status and `location` for each, then check with `curl -i` (add
`-L` to follow):

1. v1: `curl -i 'http://localhost:9000/square_root?x=3&y=4'`
2. v1: `curl -i -X POST 'http://localhost:9000/square_root?x=3&y=4'`
3. `main`: `curl -i 'http://localhost:9000/api/newsletters/?limit=1'`
4. `main`: a POST to `/api/llm/chats/` (with a slash)

<details><summary>Answer</summary>

All four answer `307 Temporary Redirect` (exercise checks B3):

1. `location: http://localhost:9000/square_root/?x=3&y=4`; with `-L`, `5.0` after one redirect. The
   query string is kept.
2. Also 307, to the same location: the redirect happens before FastAPI looks at the method. Followed,
   the POST stays a POST and the GET-only route answers 405.
3. The other direction: `location: http://localhost:9000/api/newsletters?limit=1`. `main`'s routers
   declare their root as `""` (`routers/newsletter.py:16`), so the slash-less path is the real one
   and needs no redirect (the test `test_newsletters_need_no_redirect`).
4. `location: http://localhost:9000/api/llm/chats`. A browser re-sends the POST with its body. Each
   redirect is one more round trip: the 2025 pages pay it on every newsletters load and every chat
   message (`c25`, `c28`). Call the exact path.
</details>

**B4. `def` or `async def`?** README:137-138 says the chat routes are plain `def` "so one slow
answer does not stop the API". Test the claim in the v1 API: add two routes that block for two
seconds, then fire two requests at the same time at each and time them.

```python
import time

@app.get("/slow_async")
async def slow_async():
    time.sleep(2)  # a blocking call inside async def
    return "done"

@app.get("/slow_def")
def slow_def():
    time.sleep(2)
    return "done"
```

```bash
time (curl -s localhost:9000/slow_async & curl -s localhost:9000/slow_async & wait)
time (curl -s localhost:9000/slow_def   & curl -s localhost:9000/slow_def   & wait)
```

<details><summary>Answer</summary>

`/slow_async`: **about 4 s**; `/slow_def`: **about 2 s** (exercise check B4: `4.0 s` and `2.0 s`).
An `async def` route runs on the server's single event loop, and a blocking call inside it
(`time.sleep`, a synchronous Gemini, Chroma or TensorFlow call) freezes that loop: every other
request waits, the probes included. FastAPI runs a plain `def` route in a worker thread, so the two
sleeps overlap. Use `async def` only when everything slow inside is awaited.
</details>

**B5. The chat contract, by hand.** With `main`'s API running (no frontend needed), predict the
status and `detail` for each, then send them:

```bash
S=00000000-0000-4000-8000-000000000001
curl -s -X POST localhost:9000/api/llm/chats -H 'Content-Type: application/json' -d '{"content":"hi"}'
curl -s -X POST localhost:9000/api/llm/chats -H 'Content-Type: application/json' -H 'X-Session-ID: test' -d '{"content":"hi"}'
curl -s localhost:9000/api/llm/chats -H 'X-Session-ID: ../../etc'
curl -s -X POST localhost:9000/api/llm/chats -H 'Content-Type: application/json' -H "X-Session-ID: $S" -d '{"content":""}'
curl -s -X POST localhost:9000/api/llm/chats -H 'Content-Type: application/json' -H "X-Session-ID: $S" -d '{"content":"How is cheese made?","mode":"llm"}'
```

<details><summary>Answer</summary>

Exercise check B5:

1. `422`, `"type":"missing","loc":["header","X-Session-ID"]`.
2. `422`, `"type":"string_pattern_mismatch"`: the header must look like a UUID
   (`routers/chat.py:20-21`).
3. `422`, the same mismatch. That is the reason for the pattern: the session ID becomes part of a
   file path ("Both ids end up in file paths, so only a UUID gets through", `chat.py:19`), so
   `../../etc` never reaches the disk.
4. `422 {"detail":"Message must contain text or an image"}` (`chat.py:36-37`): this one is the
   route's own check, after validation.
5. The extra field `"mode"` is **ignored** (the `ChatMessage` model has `content` and `image` only,
   `chat_utils.py:12-14`), and the message goes to Gemini. With your key: a new chat with your
   message and Gemini's reply. Without one, as in the check: `500 Internal Server Error`, and the
   API's terminal shows the reason (`DefaultCredentialsError` with no key; `RefreshError …
   invalid_grant` with an unusable one, `b38`). Then `find persistent-folder/chat-history`: nothing
   was saved, because the file is written only after the reply (`chat.py:40-42`).
</details>

**B6. What does nginx serve?** Build and run the production image as `e98fa55`'s README did
(`docker build -t cheese-app-frontend-react:prod .` in `src/frontend-react`, then
`docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod`, with the
API running). Predict status and content type for: `/healthz`, `/api/newsletters?limit=1`,
`/newsletters`, `/chat?model=llm`, an asset that exists, `/assets/nope.js` and `/nope.js`.

<details><summary>Answer</summary>

From `nginx.conf.template` (checked with the same template and nginx 1.31.8, exercise check B6):

| path | answer | which block |
| --- | --- | --- |
| `/healthz` | `200 text/plain` (`ok`) | `location = /healthz`, nginx's own, for the kubelet (line 9) |
| `/api/newsletters?limit=1` | `200 application/json`, `Server: nginx/1.31.8` | `location /api/`, passed on with the full path: the API's log shows `GET /api/newsletters?limit=1` |
| `/newsletters`, `/chat?model=llm` | `200 text/html`: `index.html` | `location /` → `try_files $uri /index.html`; React Router picks the page |
| `/assets/index-….js` | `200 application/javascript`, `Cache-Control: public, max-age=31536000, immutable` | `location /assets/` (hashed names, cached for a year) |
| `/assets/nope.js` | `404` | `try_files $uri =404`: a missing bundle must fail loudly |
| `/nope.js` | `200 text/html` | outside `/assets/`, so the page fallback applies |

Pages get `Cache-Control: no-cache`, so a new deploy's `index.html` (with new bundle names) is
fetched every time. The captures show the same with the real build (`d22`–`d25`).
</details>

**B7. The proxy's `localhost`.** In `vite.config.js`, change the proxy target to
`'http://localhost:9000'` and restart `npm run dev`. Predict what `/api/newsletters` on port 3000
returns, and what Vite's terminal says.

<details><summary>Answer</summary>

`502 Bad Gateway`, and in Vite's terminal `[vite] http proxy error: /api/newsletters?limit=1` with
`Error: connect ECONNREFUSED 127.0.0.1:9000` (exercise check B7, Vite 8.3.5; with the default
target, the same request answered `200`, `server: uvicorn`). The proxy runs **inside the frontend
container**, where `localhost` is that container itself, and nothing listens on its 9000; that the
laptop publishes 9000 doesn't matter. Pages load but stay empty. Put the target back (it is also
overridable with `API_URL`, line 13). Compare `d09`: the right name with the API unplugged gives
`getaddrinfo ENOTFOUND cheese-app-api-service`, also a 502.
</details>

---

## Part C · Debugging

**C1. "No such file or directory."** You follow v1 README:41 and type `cd cheese-app-v1/api-service`.
What happens, what is the fix, and why does the fix matter beyond the `cd`?

<details><summary>Answer</summary>

`cd: cheese-app-v1/api-service: No such file or directory` (`a01`): the folder is
`cheese-app-v1/src/api-service` (and `src/frontend-simple` for v1 README:75). It matters beyond the
`cd` because `docker-shell.sh` finds your key and data **relative to where you run it**:
`SECRETS_DIR=$(pwd)/../../../secrets/` and `PERSISTENT_DIR=$(pwd)/../../../persistent-folder/`
(v1 `docker-shell.sh:9-10`). Three levels up from `src/api-service` is the folder that holds the
clones, `secrets/` and `persistent-folder/` (`p06`). Run it from anywhere else and Docker mounts a
folder that doesn't exist, and on Linux creates it as root (C2).
</details>

**C2. `/readyz` never turns 200.** On a Linux laptop, `main`'s API starts, `/healthz` says 200,
but minutes later `/readyz` still says `503 {"detail":"CNN model is loading"}`, and Identify says
`503 The CNN model is still loading`. Scrolling up in the API's terminal you find
`PermissionError: [Errno 13] Permission denied: '/persistent/experiments'`. What happened?

<details><summary>Answer</summary>

`persistent-folder/` didn't exist when you first ran `docker-shell.sh`, so Docker created it for the
bind mount, **owned by root**; the container runs as `app` (uid 1000) and cannot create
`experiments/` in it. The model thread dies with the `PermissionError`, `cnn_model` stays `None`, and
`/readyz` reports "loading" forever (exercise check C2 reproduced exactly this with a root-owned
folder). Waiting won't help; this is the one "loading" that is a failure, and the traceback is in the
log, not in the HTTP answer. Fix: `sudo chown -R 1000:1000 persistent-folder` (or create it yourself
before the first run, as step 3 of the setup says, `p05`), then restart `api_server`. Docker Desktop
on macOS and Windows hides this.
</details>

**C3. `/readyz` says `Chroma: …`.** You started the API first, then remembered the vector DB. `/readyz`
answers `503 {"detail":"Chroma: Could not connect to a Chroma server. Are you sure it is running?"}`.
Do you have to restart the API after starting Chroma?

<details><summary>Answer</summary>

No. Start Chroma (`docker compose up -d chromadb` in `src/vector-db`, README:228; the service is
called `chromadb` in `src/vector-db/docker-compose.yml:19`, its container `cheese-app-vector-db`),
and the next `/readyz` says `200`. The client connects on first use and a failed connection is not
cached (`llm_rag_utils.py:38-42`). The exercise check C3 did exactly this: `Chroma: Could not
connect…` → Chroma started → `200`; Chroma stopped → `503 {"detail":"Chroma: [Errno -2] Name or
service not known"}` (its name left the network's phone book) → started again → `200`, with no API
restart. Last year's API could not even start without Chroma: it connected at import time (digest,
gotcha 15; not re-run here).
</details>

**C4. The production container exits at once.** `docker run --rm --network cheese-app-network -p
8080:80 cheese-app-frontend-react:prod` prints a few entrypoint lines and stops. What does the last
line say, and what is the fix? What happens if the API stops *after* nginx has started?

<details><summary>Answer</summary>

`nginx: [emerg] host not found in upstream "cheese-app-api-service" in
/etc/nginx/conf.d/default.conf:14`, exit 1 (`e01`; exercise check C4). Line 14 of the generated
config is `proxy_pass ${API_URL};` after `envsubst`: nginx resolves that name **when it starts**,
and no container of that name is on the network. Start the API first (`./docker-shell.sh` and
`api_server`), on `cheese-app-network`, then nginx. Vite is lazier: it looks the name up per request,
so it starts fine and answers 502 per call (B7). If the API goes away later, nginx keeps the address
it resolved: requests to `/api/…` hang and end in `504 Gateway Time-out` (`upstream timed out … while
connecting to upstream`), while the pages themselves still load (exercise check C4).
</details>

**C5. One extra character.** A classmate "tidies" the template to `proxy_pass ${API_URL}/;`. The image
builds, the container starts, pages load, but every newsletter, podcast and chat call answers
`{"detail":"Not Found"}`. Why?

<details><summary>Answer</summary>

With a URI part after the address (here the trailing `/`), nginx **replaces** the matched location
prefix `/api/` with it: `/api/newsletters?limit=1` reaches the API as `/newsletters?limit=1`, which
`main`'s API doesn't have (exercise check C5: the API's log shows `"GET /newsletters?limit=1 HTTP/1.1"
404 Not Found`). Without a URI part, nginx passes the full path (the template's comment, line 11:
"nginx passes /api on, full path included"), and `main`'s routes all start with `/api`
(`docs/contract.md:6-7`: "nothing strips a prefix"). Remove the slash.
</details>

**C6. "Blocked by CORS policy."** (a) A classmate serves the 2025 `newsletters.html` from 8080 but
starts `main`'s API on 9000. The browser console blames CORS. What two things are wrong? (b) On the
2025 stack, a request that crashes the API also shows up as a "CORS error", while the captured chat
error (`c28`) came through readable. Why the difference?

<details><summary>Answer</summary>

(a) `main`'s API has no CORS middleware: a GET from another origin gets `200` with **no**
`access-control-allow-origin` header, so the browser hides the answer from the page, and the chat
page's preflight `OPTIONS` gets `405 Method Not Allowed`, `allow: GET` (`b43`). And the 2025 page
calls `/newsletters` without the `/api` prefix: even curl gets `404 {"detail":"Not Found"}` from
`main`'s API (its log in exercise check C5: `"GET /newsletters?limit=1 HTTP/1.1" 404 Not Found`). Run the 2025 page with the 2025 API (as the video does), or use the React
app on 3000.

(b) An `HTTPException`, even a 500, is turned into a response inside the app, so `CORSMiddleware`
adds its header: the 2025 chat's `500 {"detail":"Failed to generate response: …"}` carries
`access-control-allow-origin: *` (`c28`), and the browser shows the real error. An **unhandled**
exception is answered by Starlette's outermost error handler, outside the middleware: `500 Internal
Server Error` with no CORS header, so the browser reports a CORS failure (exercise check C6, on v1's
app: `/handled` → 500 with the header; `/boom` (`1 / 0`) → 500 without it, and
`ZeroDivisionError` in the server's log). Read the server's terminal before touching CORS settings.
</details>

**C7. Switching to branch `2025`.** `git switch 2025` refuses with "Your local changes to the
following files would be overwritten by checkout", listing four files. Which edits are those, how do
you switch without losing them, and which second key name does the 2025 vector DB want?

<details><summary>Answer</summary>

Your project-ID edits (`src/api-service/docker-shell.sh`, `src/vector-db/docker-shell.sh`,
`src/docker-compose.yml`) and the demo route in `src/api-service/api/service.py` (`c01`). The
branch has different versions of those files, so Git won't overwrite your changes. `git stash`, then
`git switch 2025` (`c01b`: "branch '2025' set up to track 'origin/2025'"); back on `main`, `git
stash pop` restores them. On the branch, set the project ID again (`c04`), and copy the key under the
name the 2025 vector-db script reads, `GOOGLE_APPLICATION_CREDENTIALS="/secrets/llm-service-account.json"`
(2025 `vector-db/docker-shell.sh:10`), while its API reads `ml-workflow.json` (2025
`api-service/docker-shell.sh:29`): `cp ../secrets/ml-workflow.json ../secrets/llm-service-account.json`
(`c03`). The 2025 README names only the first. With a real key, the 2025 chat still fails, because
its Gemini model has been retired (the video, S14).
</details>

**C8. `api_server: command not found`.** The API runs in one terminal. In a second terminal you run
`./docker-shell.sh` again; it says "Container 'cheese-app-api-service' is already running. Shelling
into it...". `pytest` works there (`b44`), but `api_server` is "command not found". Why? And what
goes wrong if the running container is last year's API?

<details><summary>Answer</summary>

`api_server` is a bash **function**, defined and `export -f`'d by `docker-entrypoint.dev.sh`
(lines 12-16) in the container's first shell, so only that shell and its children have it. The
second terminal is `docker exec -it cheese-app-api-service /bin/bash` (`docker-shell.sh:16-18`): a
new process, not a child of that shell. Exercise check C8 shows it with the same bash mechanics: the
function is in PID 1's environment (`BASH_FUNC_api_server%%`), and `type api_server` in the exec'd
shell says `not found`. `pytest` is a program on `PATH` (Dockerfile.dev puts the venv's `bin` on
`PATH`), so it works anywhere. The server is already running in the first terminal anyway.

The script checks only the **name** (`grep -qx` on `docker ps` names). v1, the 2025 API and `main`
all call their container `cheese-app-api-service`, so a leftover v1 or 2025 container gets you a
shell in the old code, whose function is `uvicorn_server` (2025 `docker-entrypoint.sh`) and whose
routes have no `/api` prefix. `docker ps` first; `docker stop cheese-app-api-service`.
</details>

---

## Part D · Think

**D1. Two copies of the API.** In Lectures 19–22 the API runs as several copies behind a load
balancer. The README says any copy can answer a chat (README:135-136). What must the copies share for
that to be true, and what would a user see if each copy had its own `/persistent`?

<details><summary>Answer</summary>

They must share the **chat files** (and should share the model folder, so each copy doesn't download
the model again). The code keeps no chat state in memory, but it does keep it on disk, at
`/persistent/chat-history/…`. With separate disks, a follow-up that lands on another copy gets
`404 Chat not found` (`chat.py:73-74`), and the **Recent** list shows different chats depending on
which copy answered. Stateless *process* plus shared *storage*: a volume every copy mounts, a bucket
or a database. That is the next step when the app scales (README:136 points to `cheese-app-v3`).
</details>

**D2. Probes in the wrong place.** Kubernetes can restart a container whose liveness probe fails,
and stop sending traffic to one whose readiness probe fails. What would happen if someone set
**both** probes to `/readyz`?

<details><summary>Answer</summary>

On every start, the model load (about nine seconds in the capture, longer on a cold download) fails
the liveness probe; if it takes longer than the probe allows, the container is restarted, starts
loading again, and never comes up. And when Chroma has a hiccup, every API copy fails `/readyz`
together and is restarted, although restarting fixes nothing (C3 recovers by itself). With the
intended split, `/healthz` keeps a healthy-but-busy process alive and `/readyz` only holds traffic
back (the video's second ponder: wait, don't restart).
</details>

**D3. "Just add CORS to be safe."** A teammate wants to add `CORSMiddleware(allow_origins=["*"])` to
`main`'s API "so nothing gets blocked". Is that safer? When would you add CORS, and how?

<details><summary>Answer</summary>

It isn't safer: CORS is not a protection the API turns on, but a permission it hands out. The
browser's same-origin policy is the protection; `allow_origins=["*"]` lets every website's
JavaScript read your API's answers in a user's browser. Clients without a browser (curl, scripts,
another server) never ask about CORS at all (C6, `b43`), so it does nothing against them. `main`
needs none because the page and its calls share one origin (Q5). Add it only when a page on a
different origin really must call the API directly (a frontend on its own domain, say), and then list
that origin, with only the methods and headers it uses.
</details>

**D4. Dev vs production frontend.** Compare the container on 3000 (`npm run dev`) with the one on
8080 (`:prod`): what serves the files, what is in the image, what happens when the API is missing,
and what stays the same?

<details><summary>Answer</summary>

| | dev (`Dockerfile.dev`) | production (`Dockerfile`) |
| --- | --- | --- |
| serves | Vite on 5173, transforming your source on each request, hot reload | nginx on 80, serving the files `vite build` made |
| image | Node and npm, no app code (your folder is mounted, `node_modules` in a named volume): 331 MB | nginx plus `dist/` only (the Node stage is thrown away): 94.8 MB (`d27`) |
| API missing | starts anyway; each `/api` call answers 502 (`d09`) | refuses to start: `host not found in upstream` (C4) |
| `/api` rule | `vite.config.js:13` | `nginx.conf.template:13-14` |

What stays the same: the page code calls relative `/api/...` paths on its own origin, the courier
forwards by container name to port 9000, and the API itself, its code and its port, doesn't change.
That is the lecture's production slide: only the outside changes.
</details>
