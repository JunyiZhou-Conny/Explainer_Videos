# Brief · AC215 L18 — APIs and frontend: one request, four containers, two ways past the browser

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the two lecture decks and their scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** The captures are newer (2026-11-05, UTC 12:58–14:16), made by
running every README command as written, in a fresh, empty Docker engine that stands in for the
student's laptop (`docker:29.8.2-dind`, user `student`).

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**: both decks (APIs, Frontend) slide by slide wherever the tutorial
applies them, and every README step of cheese-app-v1 and cheese-app-v2, in order. The published exam
edition `videos/ac215-l16-exam/` quotes cheese-app-v2 @ `14f2a14` for related items; this video
follows what a student clones today and says where that differs.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which commit (v2) | `units.json`: `14f2a14`; digest: `main` = `e98fa55` | **`main` moved twice on the recording day**: 07:23 → `e98fa55` (simple frontend removed, vector-db upgraded, clean-up), 07:52 → **`447b5c3`** (README rewritten + `src/docker-compose.yml`; every other quoted file byte-identical to `e98fa55`). **Decision (taken): Tutorials 23 and 25 follow `447b5c3`; Tutorial 24 (the simple frontend) is pinned to `14f2a14` = branch `2025`, because `main` dropped it but the lecture teaches it; "Production images" is shown from `e98fa55`'s README as extras, because `447b5c3` replaced that section with "Setup & Run Cheese App" while the Dockerfile and `nginx.conf.template` stay on `main`.** v1 stays at `ce03a10` (`main`, unchanged) |
| README headings | "Tutorial (23)/(24)/(25)" | `447b5c3` headings read "Tutorial: Environment Setup", "Tutorial: Vector DB for RAG Setup", "Tutorial: Backend APIs", "Tutorial: React Frontend Setup", "Tutorial: Setup & Run Cheese App". The course site's anchors `#tutorial-23-…`/`#tutorial-25-…` no longer exist; the slides' anchors (`#setup-environments`, `#frontend-app-simple`, `#frontend-app-react`) never did. The tracker names the heading, never an anchor |
| React framework | SLIDES Conflict 7: Next.js 15 App Router (written against `14f2a14`) | **Vite 8.3.5 + React 19 + React Router 8** (`package.json:18-32`, `d02`, `d12`). No Next.js, no `NEXT_PUBLIC_*`, no `layout.jsx`: the lecture's "header defined only once" is `App.jsx` (header, `<Outlet />`, footer). SLIDES' Next.js wording is superseded |
| CORS | digest §3.4 (main has none) | confirmed: `b43` — with `Origin: http://localhost:8080`, `200` and **no `access-control-*` header**; preflight `OPTIONS` → **405**, `allow: GET`. The 2025 stack answers with `access-control-allow-origin: *` (`c25`, `c27`, `c28`) |
| Gemini failure | README Troubleshooting: "Gemini: 403 / 404" | a key Google rejects gives **HTTP 500 `Internal Server Error`** on `main` (`b38`, `b40`, `d06`): `RefreshError: invalid_grant: account not found` is not mapped to the 502 path. 2025: `500 {"detail":"Failed to generate response: …"}` (`c28`). No Gemini answer text exists anywhere in the assets; none is ever shown |
| Vite when the API is gone | digest open question 7 | `d09`: **`502`, empty body**; Vite's log: `http proxy error … ENOTFOUND cheese-app-api-service` (`d02:85-86`) |
| CNN | digest: "brie, 93 %" as an example | the real offline answer on the repo's own `blue-cheese.jpg`: **`"parmigiano"`, `58.22`** (`b39`). Say it plainly: a model's label is a guess with a confidence |
| 2025 stack | digest: may need `docker compose` shim, `chroma:latest` uncertain | hyphenated `docker-compose` works on this engine; `chromadb/chroma:latest` (created 2026-05-05) still talks to the 2025 client (`c06`, `c07`); the 2025 API loads the CNN at import, so start-up waits for it (`c11`) |
| `npm run check` | ASSETS: "built in 767ms" | the capture says `✓ built in 470ms` (`d12:27`). Never read aloud anyway |
| length | digest §8: ~5,000 words at 155 wpm | plan **~4,260 words ≈ 24.5 min narration**, ~31–33 min with typing, outputs and five ponders |

## Audience and goal

An AC215 student who has done L1–L17:
- Docker images, containers, `-p HOST:CONTAINER`, bind mounts, `docker-shell.sh` (L2–L4);
- a Docker network and container names (L4, L10's cheese-app-v0);
- the `llm-rag` chunk → embed → Chroma pipeline (L5), the cheese CNN (L13), the `ml-workflow.json`
  service-account key in `secrets/` (L15);
- a GCP project with the Vertex AI API on (L1, L15).

They have seen Lecture 18 (both decks). They watch with clones of
[dlops-io/cheese-app-v1](https://github.com/dlops-io/cheese-app-v1) and
[dlops-io/cheese-app-v2](https://github.com/dlops-io/cheese-app-v2) open, Docker Desktop running,
about 10 GB free, and they pause to run each step. **Everything runs on the laptop**; the only cloud
calls are Gemini and the embedding model on Vertex AI (GOLD tag where they happen).

After the video they can:
- trace one request the lecture's way, hop by hop: browser → published port → container port →
  uvicorn → the FastAPI function → JSON back; and say what changes in production (only the outside);
- start a FastAPI app under uvicorn in a container, explain `api.service:app`, `--host 0.0.0.0`,
  `--reload`, and why `/square_root` answers 307 and `?x=abc` answers 422;
- serve static files with `http-server` and say what runs where: the container sends files, the
  browser runs the JavaScript;
- bring up v2's four containers on `cheese-app-network`, load 14,356 chunks into Chroma, read
  `/healthz` vs `/readyz`, find the routes in `/api/docs`, and run `pytest`;
- explain how a chat survives without memory: an `X-Session-ID`, a JSON file per chat, the history
  rebuilt on every message;
- run the React app on 3000 and explain why the browser never sees port 9000: Vite (dev) and nginx
  (prod) forward `/api` by container name on one origin, so `main`'s API needs no CORS;
- switch to branch `2025`, run last year's simple frontend, and read a CORS preflight and a 307 in
  the API log;
- bring the whole app up with `docker compose up --build`, and clean up, including what `prune`
  leaves behind.

## Length and parts

~31–33 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm). The plan below
totals **~4,260**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S09** (~2,360 words, ~17–18 min): **the API** — the lecture's APIs deck. The hook,
  the blueprint and the folders, cheese-app-v1 (an API and a static page), then v2: the vector DB,
  the API's probes, its routes and docs, chats as files, `pytest`.
- **Part 2 = S10–S16** (~1,900 words, ~14–15 min): **the frontend** — the lecture's Frontend deck.
  Why a framework, the React dev server, the one-origin proxy, the production image, Compose and
  clean-up, then Tutorial 24 on branch `2025` (the simple frontend, CORS), and the recap.

The cut is the README's own seam: "Run the tests inside the container … **Keep this container
running.**" (README:140-145), which is also the seam between the two decks. Part 1 ends on
`26 passed` and a parked question: "the API is ready, but nobody can use it from a browser yet. The
browser will talk to port 3000. How does that reach 9000?"

**Why Tutorial 24 comes last** (said in S02 and S14, once each): it now lives on another branch, with
its own vector DB and API on the same ports 8000 and 9000. Doing it after `main`'s clean-up means one
switch, no clashing containers, and every step matches the captures (they were recorded in this
order). The lecture's simple-frontend ideas that come before React (B16–B23: files vs code) are
taught on v1's simple frontend in S05, so the framework motivation in S10 still has its "before".

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop, the browser, its tab and address bar, the host's ports and DNS, `secrets/` and `persistent-folder/` on the host | GREY |
| the cloud: Vertex AI (Gemini, `text-embedding-004`), the lecture's GCP boundary, cluster and Artifact Registry in the blueprint | BLUE |
| containers and images: `cheese-app-api-service`, `cheese-app-vector-db`, `cheese-app-vector-db-cli`, `cheese-app-frontend-react` (dev and `:prod`), `cheese-app-frontend-simple`, nginx's container | TEAL |
| shared, not yours: the default bridge network, Docker's build cache, the shared `node_modules` volume, the browser's built-in rules (same-origin policy), port numbers everyone collides on (8000, 8080, 9000) | ORANGE |
| what the project owns and pins: `pyproject.toml`/`uv.lock`, `package.json`/`package-lock.json`, the chat JSON files, Chroma's collection `recursive-split-collection`, `cheese-app-network` (the app's private LAN), `docs/contract.md`, pytest's green `26 passed` | GREEN |
| tools: uvicorn, FastAPI, `http-server`, Vite, nginx, Docker Compose, pytest, npm | PURPLE |
| errors and "don't": `No such file or directory`, 422, 404, 405, 500, 502, 503, `RefreshError`, `[emerg] host not found`, `git switch` refused, the README typos, a secret inside the repo | RED |
| your turn, the README tracker, the hop being traced now, the ponder timer | YELLOW |
| money: Gemini and embedding calls on Vertex AI (with your own key), disk (~10 GB; the 4.2 GB API image) | GOLD |
| routes and addresses: URLs, paths, query strings, `-p` doors, request/response arrows, the numbered hops, origins, headers (`X-Session-ID`, `Origin`, `access-control-*`), the proxy hop | PINK |
| the past and the future (L5's RAG, L13's CNN, L15's key; L19–L22's cluster, NGINX, Artifact Registry) | GREY, dashed |

The lecture's own colours (red request arrows, gold "API Service" box, six coloured route groups on
A44) are **not** copied: requests are PINK, the API is a TEAL container, and A44's six groups are
WHITE-outlined chips (GREEN when switched on in this repo, GREY dashed when not). A30–A33's MCP
service is GREY dashed (not in this repo).

## Running example

- **The laptop**: user `student`, terminal title `laptop`, prompts taken from each capture:
  `student@laptop:~$`, `…:~/cheese-app-v1/src/api-service$`, `…:~/cheese-app-v2/src/…$`; inside
  containers `app@<id>:/app$` (API, vector-db CLI), `<id>:/app#` (http-server), `node@<id>:/app$`
  (Vite). Container ids are never read aloud. Say once: "your prompt shows your own user; on a Mac
  the banner says `aarch64` and the API gets the `tensorflow` wheel".
- **Folders side by side** (`p05`, `p06`): `cheese-app-v1/`, `cheese-app-v2/`, `secrets/`,
  `persistent-folder/` in one parent folder. That layout is what `../../../secrets` resolves to.
- **The key, honestly** (said once, in S06, then never apologised for): this recording machine has
  no Google account. `secrets/ml-workflow.json` is a well-formed file around a throwaway key for no
  account (its shape without the key: `capture-only/placeholder-key.json`; never shown as a panel
  with values). Everything that does not call Google works exactly as for you; the first Google call
  fails honestly with `invalid_grant: account not found`. "With your real key, this is where
  Gemini's answer appears." The successful reply's **shape** is `expected/02-chat-contract.txt`
  (`docs/contract.md:31-44`), tagged `expected`.
- **The browser** is a schematic GREY window tagged `illustration` (no screenshot), with the address
  bar and what the captured HTML says the page holds (`d03`, `d22`, `a21`, `c22`, `c23`, `c26`;
  `expected/03-review-the-app.txt`). Every "open … in your browser" step is shown with its curl
  capture beside the drawing.
- **Placeholders**: project id `your-gcp-project` (`b03`, `f01`, `c04`); the session id
  `00000000-0000-4000-8000-000000000001` from the curl captures. No real-looking key, token or
  project id anywhere.
- **Versions, all "at the time of recording"**: Docker 29.8.2, Compose v5.6.0; v1: Python 3.12.16,
  uv 0.13.7, FastAPI 0.120.4, uvicorn 0.38.0, http-server 14.1.1; `main`: Python 3.13.18, uv
  0.13.6, FastAPI 0.162.0, uvicorn 0.54.0, tensorflow-cpu 2.21.0, pytest 9.2.0, Chroma 1.5.9, Node
  v24.22.1, npm 11.19.1, Vite 8.3.5, nginx 1.31.8; 2025: Python 3.12.16, TensorFlow 2.19.0. Image
  sizes: API 4.2 GB, React dev 331 MB, React prod **94.8 MB**.
- **Crops**: the branch name in `p03`, `p04`, `b01`, `c01b`, `c31` (a staff member's name) is
  cropped or masked; dates, PIDs, container ids and hashed asset names are never read aloud; long
  build logs show first lines, `…`, last lines.

## Visual set pieces (the 3Blue1Brown part)

Class names go in `scenes/common.py`. None collides with a scene class in `video.yaml`.

- **V1 · `RequestTrace` — the lecture's hop-by-hop request (A34–A41 = B7–B14, B18–B27, A42; the
  video's spine: S01, S03, S05, S11, S12, S15).** One fixed layout throughout, as the lecture keeps
  it: the GREY browser window on the left with its address bar, a dashed vertical divider, a GREY
  laptop outline on the right with TEAL container boxes inside. PINK request arrows with YELLOW
  numbered circles, captioned in the series' words:
  1 request → 2 the host forwards it to the published port → 3 the port is mapped into the
  container → 4 the function runs → 5 the response comes back → 6 the browser (or its JavaScript)
  shows it.
  - S01: B27's chat trip at `localhost:3000/chat` on `main`, with a hop **3½** the lecture never
    draws: a small PURPLE "Vite" courier inside the frontend box carries the request on to
    `cheese-app-api-service:9000`. The `server: uvicorn` header (`d04`) lights up at step 5.
  - S03: the A34–A38 steps on v1's `localhost:9000/`, the `-p 9000:9000` door drawn as a tunnel.
  - S05: B18–B23's first trip (`:8080`, a file comes back); v1 ends there: no second arrow.
  - S11: main's version: **every** arrow from the browser lands on 3000; the courier crosses the
    GREEN network cable. The 9000 door is still there (for `/api/docs`, `curl`), dimmed.
  - S12: A42's production version: the address becomes `localhost:8080`, nginx replaces the courier,
    the inner part (API on 9000) does not move. One line: "only the outside changes".
  - S15: B24–B27 exactly: the page's JavaScript fires a second arrow straight at `localhost:9000`, and
    the browser adds a step **0**: a PINK `OPTIONS` scout that must come back with an
    `access-control-allow-origin` badge before the POST may leave. A 307 bounce (`/llm/chats/` →
    `/llm/chats`) is a small U-turn on arrow 1.
- **V2 · `ArchitectureMap` — the lecture's technical architecture (A8–A21; S01 closing beat, S02, S13,
  S16).** Built the lecture's way, one layer per beat, in series colours: the two GREY bands
  (developers / users), GitHub and Colab outside, the BLUE GCP boundary with Vertex AI (Gemini), the
  GCS bucket, Artifact Registry, the persistent disk, and the right-hand cluster box. Every edge gets
  a PINK protocol + port label ("HTTPS 443", "HTTP 9000", "HTTP 3000", "HTTP 8000"). At A19 the
  cluster fills with four TEAL boxes: NGINX, Cheese App (3000), API Service (9000), Vector DB (8000).
  - S01: zoom out from the laptop of V1 to this picture; the three ports carry over. A20's "App is
    ready!" chip appears and is immediately struck through by A21's "Well not really, we need to build
    it" (no smiley drawn).
  - S02: the full build, ~40 s, then the camera pulls the cluster box *down into the laptop*: "today,
    all of it runs here". The A22 GCP/AWS/Azure table is one line, not drawn.
  - S13: `docker compose up` lights the same four boxes on the laptop (`f04`: four containers, the
    loader instead of NGINX in dev).
  - S16: the cluster dims back to dashed: L19–L22 build it.
- **V3 · `ServerAppDiagram` — uvicorn owns the socket, FastAPI is the app (S03, S07).** A TEAL container;
  inside, a PURPLE uvicorn box holding the port, and inside that a smaller FastAPI "app" card that
  holds a route table. `api.service:app` splits into "folder `api/` · file `service.py` · variable
  `app`". Two listening badges: `127.0.0.1` (only the container's own loopback; the forwarded
  request from the `-p` tunnel hits a wall) vs `0.0.0.0` (every interface; the request walks in).
  `--reload`: a save in `api/` makes uvicorn swap the app card for a fresh one
  (`StatReload detected changes`, `a03:47`); in S07 the swap also restarts the CNN loader, so the
  readiness lamp drops to amber again (`b30`).
- **V4 · `RouteTree` — a function becomes a URL, routers graft under prefixes (S04, S08).**
  - S04: `http://localhost:9000/square_root/?x=2&y=10` splits into PINK tokens; `x=2`, `y=10` fly
    into the signature `square_root(x: float = 1, y: float = 2)` and `10.198…` folds back as JSON
    (`a07`). `?x=abc` bounces off the `float` hint with a RED 422 (`a08`); `/square_root` without the
    slash makes a U-turn: 307 → `/square_root/` (`a09`). `/docs` unfolds from the route table
    (`a10`).
  - S08: the tree: a root `/api`, branches `newsletters`, `podcasts`, then one `create_router` stamp
    printing three identical chat branches labelled `llm` / `llm-cnn` / `llm-rag`
    (`service.py:36-40`), plus `/healthz` and `/readyz` at the root. A44's six chips hover above and
    snap onto the matching branches; RAG snaps, Agent stays GREY dashed (no router in this repo).
    `/api/docs` unfolds into the real 25 operations (`b32`).
- **V5 · `TwoLocalhosts` — published ports vs container names (S06, S11).** Zoom from the GREY
  laptop into TEAL boxes, each with its own floating "localhost" label. A GREEN cable
  `cheese-app-network` with a small phone book: `cheese-app-vector-db → 172.19.0.2` (real, `b10`),
  `cheese-app-api-service`, `cheese-app-frontend-react`. Visitors from the browser come in through
  GREY "buzzer" doors (published ports `-p 3000:5173`, `-p 9000:9000`, `8000:8000`); neighbours
  knock by name. The lecture's rule (A24, A28) is the caption: **one front door** — every client
  speaks to the API; only the API talks to Chroma and to Vertex AI.
  - S11: the browser tries the name `cheese-app-api-service`: the laptop's DNS has no page for it
    (ponder 3). Vite's courier, inside the network, looks the name up and walks over. When the API is
    unplugged from the cable, the courier comes back with a RED `502` and an empty envelope (`d09`).
- **V6 · `ProbeLamps` — liveness vs readiness (S07).** Two lamps on the API container:
  `/healthz` (GREEN as soon as uvicorn answers, `b22`) and `/readyz` (amber "CNN model is loading",
  503, `b23`, → GREEN 9 s later, `b24`). Behind the readiness lamp, two wires: the CNN thread
  (a progress ring filling as the `.keras` file loads from `persistent-folder`, `b26`) and Chroma's
  heartbeat. A thought bubble shows where this goes: a load balancer that sends traffic only to
  GREEN-ready boxes (L19/L22, GREY dashed).
- **V7 · `ChatFile` — a chat is a file, not a memory (S09).** The browser holds a small locker key
  (`X-Session-ID`, a UUID). Each POST carries the key and one message; the API opens
  `chat-history/llm-cnn/<session>/<chat>.json` (GREEN file, real path from `b42`), appends the user
  turn and the reply, saves, and forgets. A second API copy appears and answers the next message from
  the same file: "any copy can answer". A missing key bounces with 422 (`b36`); an empty message with
  422 (`b37`).
- **V8 · `OneShell` — one page per feature vs one app shell (S10).** B30–B32: four separate HTML
  pages, each carrying its own header, script and style, each loading separately (a GREY page-reload
  sweep each time; caption "slow", "nothing shared"). Then B36–B37: they collapse into one shell:
  Header (written once) · Content · Footer; the content block swaps Home → Newsletters → Chat while
  the header stays put. The labels then become code: `main.jsx`'s route table (`/`, `chat`,
  `newsletters`, `newsletters/:id`, `podcasts`, `*`) morphs into the address bar, and `App.jsx`'s
  `<Outlet />` is the content window.

## README step tracker (ReadmeTracker, top-left)

One tracker per README section, titled with the README's own heading (the 2025 and `e98fa55` ones
carry their commit in the caption). Steps the README does not have are marked `extra` in the tracker
caption and in the narration ("this one isn't in the README"). Step titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **SE · Setup Environments** (v1 + v2 "Environment Setup") | v1:14-35, v2:20-50 | Clone v1 · Clone v2 · Local folders · Project ID (4) |
| **A · Backend API Container** (v1) | v1:37-67 | Go to folder · Build & run · Start uvicorn · Test root · Add route · Try route · Add params · View docs (8) |
| **F · Frontend App (Simple)** (v1) | v1:71-97 | Go to folder · Build & run · http-server · Test 8080 · Edit index · Refresh page (6) |
| **C1 · Docker Cleanup** (v1) | v1:100-106 | Container ls · Stop containers · System prune · Image ls (4) |
| **V · Vector DB for RAG** | v2:52-79 | cd vector-db · docker-shell · Load database · Try chat · exit (5) |
| **B · Backend APIs** | v2:81-145 | cd api-service · docker-shell · api_server · Check probes · Demo route · Try route · API docs · GET newsletters · Review code · pytest (10) |
| **R · React Frontend Setup** | v2:147-190 | cd frontend · docker-shell · npm run dev · Open 3000 · Review app · Review code · npm run check (7) |
| **P · Production images** (`e98fa55` README) | e98fa55:197-215 | Stop dev · docker build · docker run · Open 8080 · Compare sizes (5) |
| **S · Setup & Run Cheese App** | v2:192-221 | Project ID · Stop containers · cd src · compose up · Open app · compose down (6) |
| **C2 · Docker Cleanup** | v2:235-246 | compose down · system prune (2) |
| **T23 · 2025: Vector DB & APIs** (`14f2a14`) | 2025:40-95 | cd vector-db · docker-shell · Load database · cd api-service · docker-shell · uvicorn_server · Verify 9000 (7) |
| **T24 · Tutorial (24): Simple Frontend** (`14f2a14`) | 2025:147-183 | cd frontend · docker-shell · http-server · Home page · Newsletters · Chat (6) |

Extras (captured, marked `extra`): `p03`/`p04` (which commit), `p06` (tree), `a02`/`a20` (the paths
that exist), `a08`/`a09`/`a11`/`a12`, `a22`, `a25`/`a26`, `b01`/`b02`, `b04`, `b07`–`b10`, `b25`,
`b26`, `b30`, `b32`, `b34`–`b43`, `b45`/`b46`, `d04`–`d11`, the whole P tracker (`d20`–`d28`, from
`e98fa55`'s README), `e01`, `e04`, `f04-x-*`, `f11`, `c01b`, `c02`, `c03`, `c07`, `c12`–`c14`,
`c24`, `c25`, `c27`–`c31`.

S01 has no tracker; S10 opens on the lecture (no tracker until `cd src/frontend-react`); S16's recap
has none.

## Scene plan

Notation:
- `aNN`, `bNN`, … = `assets/terminal/laptop/aNN-*.txt`; `expected/0N` = `assets/terminal/expected/`.
  Line 1 of a capture is the `$` command (typed, never printed); `[exit N]` is never printed.
- ▶ = a README step the viewer must do; a YELLOW `▶ your turn` tag at real checkpoints (about one per
  tracker).
- CODE(path: a-b) quotes `assets/source/` with real line numbers, ≤ 12 lines on screen.
  `cheese-app-v2/…` = `447b5c3`; `cheese-app-v2-at-14f2a14/…` = branch `2025`;
  `cheese-app-v2-at-e98fa55/README.md` for "Production images".
- `lecture_ref(18, "a–b (APIs)")` / `lecture_ref(18, "a–b (Frontend)")`, GREY, top right, **only
  while that slide's picture or idea is on screen** (SLIDES "Proposals: General"). Never show the
  A/B notation.

### Part 1 · The API

**S01 · Who answered on port 3000? (~220 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
- The puzzle, as real output: `curl -i http://localhost:3000/api/newsletters?limit=2` (`d04`): the
  request went to port 3000, the frontend's port, and the answer says **`server: uvicorn`**, the
  API's server on port 9000. Beside it, last year's version of the same app (`c25`): the page called
  9000 itself, and the answer carries `access-control-allow-origin: *`. "This year's API sends no
  such header (`b43`). So who carried the request across, and why did last year's need permission?"
  The question stays on screen: *"The page talks to 3000. The answer comes from 9000. Who carried
  it?"*
- V1 at full size, `lecture_ref(18, "27 (Frontend)")`: B27's numbered chat round trip; hop 3½ (the
  courier) is a "?" until S11.
- V2 teaser, `lecture_ref(18, "19–21 (APIs)")`: zoom out to the lecture's blueprint, the three ports
  3000 / 9000 / 8000 carry over; "App is ready!" struck through by "we need to build it". "Today we
  build the right-hand side, on your laptop."
- How to follow along: two repos, Docker, ~10 GB free; the README tracker top-left, code panels with
  path and lines, `▶ your turn`; the study guide has every command. Your Google key is needed only
  for the chat answers.

**S02 · The blueprint, and your folders (~250) — `s02_blueprint.py` · `Blueprint`.**
- `lecture_ref(18, "4–5 (APIs)")`: A4's roadmap in one beat (POC → Prototype → MVP, "Build Cheese
  App" boxed) and A5's progress board: ML pipeline ticked, **App Dev** = Backend API + Frontend.
- `lecture_ref(18, "7–21 (APIs)")`: V2 built layer by layer (≈ 40 s): a technical architecture is
  the system's blueprint (A7); three kinds of people (A8–A10); every arrow labelled with protocol
  and port (A13); the cluster filled (A19). Then the cluster slides into the laptop. One sentence on
  A22: the same building blocks have AWS and Azure names.
- `lecture_ref(18, "43 (APIs)")`: A43's rule redrawn on the viewer's real tree: one Git root per app,
  one folder per service under `src/`, **secrets outside the Git folder**. Kindly: the slide's
  tree is the whole project; each tutorial repo holds only what it needs, and v2 wants
  `ml-workflow.json` (Conflicts 4, 5).
- Tracker SE 1–3: ▶ `p01`, `p02` (`git clone …`, marked `extra` for its spelling: the READMEs say
  "Clone or download", v1:17-18, v2:22-23), ▶ `p05` `mkdir -p secrets persistent-folder`, extra
  `p06` (the side-by-side tree; crop to the top level). Say why you create them yourself: Docker
  on Linux would create them as root (digest gotcha 5).
- Which commit, kindly, in three sentences (extra `p04`, branch name cropped): `cheese-app-v2`'s
  `main` changed twice on the day we recorded; we follow it (`447b5c3`), and Tutorial 24, the
  simple frontend the lecture teaches, now lives on branch `2025`, which we visit at the end.

**S03 · v1: a server, an app, a port (~290) — `s03_server.py` · `ServerAndApp`.** Tracker A 1–4.
- `lecture_ref(18, "25–28 (APIs)")`: A25's request/response loop; A26's port (22, 80, 443 vs the
  tutorial's 9000, 8080, 3000, 8000: public URLs hide 80/443, tutorial URLs carry their port);
  A27's ladder as a four-step card: API → Web API → REST API → FastAPI; A28: one connector between
  every client and the stores.
- ▶ `a01`: the README's `cd` (v1:41) without `src/` → `No such file or directory` (RED); erratum,
  kindly; extra `a02` the path that exists.
- CODE(`cheese-app-v1/src/api-service/docker-shell.sh`: 13-21): `docker build`, `--rm --name`, the
  `-v` mounts, **`-p 9000:9000`**. ▶ `a03` `sh docker-shell.sh`: build (first and last lines),
  `Container is running!!!`, `Python 3.12.16`, `uv 0.13.7` (`a03:32-36`).
- V3: ▶ the uvicorn line typed exactly as v1:47 (`a03:38`), then each part explained: `api.service:app`,
  `--host 0.0.0.0`, `--port 9000`, `--reload --reload-dir api/`, `"$@"` (passes extra arguments
  through; nothing here). Real start-up lines `a03:40-44`.
- CODE(`cheese-app-v1/src/api-service/api/service.py`: 1-20): `FastAPI(...)`, the CORS middleware
  ("we come back to this at the very end"), `@app.get("/")`.
- ▶ `a04` (`curl -i`: `200`, `server: uvicorn`, `{"message":"Welcome to AC215"}`), with V1's A34–A38
  steps as captions, `lecture_ref(18, "34–38 (APIs)")`. Kindly (Conflict 8): the slide labels the
  inside of the container `localhost:9000`; read it as "port 9000 of the container", because
  uvicorn listens on `0.0.0.0`.
- **PONDER 1** (8 s).

**S04 · A Python function becomes a URL (~250) — `s04_route.py` · `FunctionToUrl`.** Tracker A 5–8.
- Ponder 1's answer in the first sentence.
- `lecture_ref(18, "39–41 (APIs)")`: A39's one-file route as the shape you are about to write.
- ▶ `a05`: the README snippet (v1:53-58) appended to `service.py`; the `git diff`. The uvicorn
  terminal: `StatReload detected changes in 'api/service.py'. Reloading...` (`a03:47`): V3's swap.
- V4: ▶ `a06` (`2.23606797749979`, the defaults 1 and 2), ▶ `a07` (`?x=2&y=10` →
  `10.198039027185569`); extras `a08` (`?x=abc` → 422 `float_parsing`) and `a09` (no slash → 307,
  `location: …/square_root/`); the access log lines `a03:55-59`.
- ▶ `a10` `/docs`: `<title>API Server - Swagger UI</title>`, `url: '/openapi.json'`; the browser
  drawing of the docs page (`illustration`), with x and y as numbers with defaults (`a11`, extra).
  "The type hints became the validation and the docs."

**S05 · Files for the browser: the simple frontend (~270) — `s05_static.py` · `StaticPages`.**
Tracker F 1–6, then C1 1–4.
- `lecture_ref(18, "16–17 (Frontend)")`: HTML = structure, CSS = style, JavaScript = behaviour, the
  only programming language of the three; B17's anatomy mapped onto v1's own `index.html`
  (CODE `cheese-app-v1/src/frontend-simple/index.html`, a ≤ 12-line excerpt of the head and the
  script tag; **line 57 masked as ‹instructor› if it is ever in view**, better out of view).
- ▶ `a19` (README path without `src/` again, RED) → extra `a20`. ▶ `a20b`: `sh docker-shell.sh`,
  `http-server`: `http-server version: 14.1.1`, `Cache: 3600 seconds`, `Available on:` two
  container addresses ("inside the container; your laptop uses 8080").
- V1, `lecture_ref(18, "18–23 (Frontend)")`: B18–B23's trip: the request reaches `http-server`, a
  **file** comes back, the browser renders it. ▶ `a21` (`200`, `cache-control: max-age=3600`,
  `<title>Formaggio.me</title>`). Extra `a22`: `main.js:37` "Sample Podcast Data (This would
  normally come from an API)": v1's page never makes the second trip. "Hold on to that: part 2 adds
  it."
- ▶ `a23`/`a24`: add the `<p>` (v1:86-97). Erratum, kindly: the README's snippet is a whole old
  `<body>`; pasting it as is would drop the page and its script tag. Add only the `<p>`. Extra
  `a25`: `main.js` is cached for an hour, so a hard refresh (or `http-server -c-1`) shows JS edits.
- Ctrl-C, `exit` in both terminals (`a03`, `a20b` tails). ▶ C1: `a30` (no containers: `--rm`),
  `a31` (`docker system prune`, `[y/N] y`), `a32` (the images that stay). One sentence on the v1
  frontend Dockerfile's `ADD --chown=app:app` (no such user; BuildKit builds it anyway): exercises,
  not the video.

**S06 · v2: four containers, and the cheese books (~270) — `s06_vectordb.py` · `VectorDb`.**
Tracker SE 4, then V 1–5.
- The README's intro table (v2:5-10) becomes V2's laptop: four TEAL boxes, three ports. Prerequisites
  (v2:13-18) as an `illustration` card from `expected/01-prerequisites.txt`: a GCP project with the
  Vertex AI API, `ml-workflow.json` with **Vertex AI User**, ~10 GB. The sandbox key, said once
  (Running example). GOLD tag: "with your key, chat and embedding calls are billed to your project".
- ▶ `b03`: `GCP_PROJECT` in both scripts, placeholder `your-gcp-project` (the `git diff`); extra `b04`.
- `lecture_ref(18, "45 (APIs)")`: A45's first step, "make sure the vector database is running".
- V5, first half: ▶ `b05`, ▶ `b06` `./docker-shell.sh`: the network id from
  `docker network create`, `chromadb/chroma:1.5.9 Pulled`, `Container cheese-app-vector-db Created`
  (`b06:27-30`); the CLI prompt. CODE(`cheese-app-v2/src/vector-db/docker-compose.yml`, the Chroma
  service: port 8000, `./docker-volumes/chromadb:/data`, the external network).
- ▶ `--download --load --chunk_type recursive-split` (`b06:44-208`): `Number of files to process:
  11`, one `Finished inserting …` line per book, a counter summing to **14,356** (923 … 163), first
  and last books shown, the rest `…`. One sentence linking L5: these are the same chunk-and-embed
  outputs, downloaded instead of recomputed.
- ▶ `--chat` (`b06:209-297`): the honest first error at the query embedding: `RefreshError:
  ('invalid_grant: Invalid grant: account not found', …)` (first line, `…`, last line). "With your
  key: an answer from the books." Erratum, kindly: `--chat` asks its own fixed question, "How is
  cheese made?" (`cli.py:377`), whatever you type; edit that line to ask another. ▶ `exit`.
- Extras: `b07` (Chroma still up, `0.0.0.0:8000->8000`), `b08` (heartbeat), `b10`
  (`cheese-app-vector-db 172.19.0.2` on `cheese-app-network`): the first entry in V5's phone book.

**S07 · Start the API: alive, then ready (~260) — `s07_ready.py` · `AliveAndReady`.** Tracker B 1–4.
- ▶ `b20`, ▶ `b21` `./docker-shell.sh`: `Building cheese-app-api-service (Dockerfile.dev)...`, the
  136 s build (TensorFlow: "the first build takes a few minutes"), the banner. CODE(`cheese-app-v2/
  src/api-service/docker-shell.sh`: 14-34): exec-if-running (16-18), `/secrets:ro`,
  `/persistent`, `-p 9000:9000`, `--network cheese-app-network`.
- ▶ `api_server`; CODE(`docker-entrypoint.dev.sh`: 12-16) shows it is V3's uvicorn line with
  `api.service:app`. `Application startup complete.` arrives at once; TensorFlow's lines follow from
  a background thread.
- V6 with CODE(`api/service.py`: 19-23, 43-56): the lifespan thread, `/healthz`, `/readyz`.
  ▶ `b22` (`200 {"ok":true}`), ▶ `b23` (`503 {"detail":"CNN model is loading"}` at 13:49:35), ▶ `b24`
  (`200` at 13:49:44: about nine seconds here). Extra `b26`: the model in `persistent-folder`
  (`mobilenetv2_train_base_True.keras`): downloaded once, reused on every start.
- Extra `b25`: the v1 habits fail: `/` and `/docs` → 404. "Everything the browser calls is under
  `/api`; the probes stay at the root" (`service.py:1-7`).
- **PONDER 2** (8 s), answered right after: wait, it is alive, not ready; Kubernetes in L19/L22
  uses exactly these two probes.

**S08 · Screens decide the routes (~280) — `s08_routes.py` · `ScreensToRoutes`.** Tracker B 5–9.
- `lecture_ref(18, "29, 44 (APIs)")`: A29's three wireframe screens (newsletters, podcasts, a chat
  that takes a photo) → each needs data → A44's route groups → V4's tree on
  CODE(`api/service.py`: 31-40). Kindly (Conflict 3, updated by the captures): the lecture shows six
  groups; this repo has five routers: newsletters, podcasts, and one `create_router` stamped three
  times (Ask, Identify, Cheese books). Agent chat has no router here.
- `lecture_ref(18, "30–33 (APIs)")`, 20 s: where an agent can sit (behind the API with an MCP
  service, behind the API without one, or as the client) and REST vs MCP. "No MCP service in this
  repo; the lecture's picture is where this is heading."
- Kindly (Conflict 1): the slide's `@app.get("/newsletters")` in one file is the idea; the repo puts
  the same function in a router mounted at `/api/newsletters`.
- ▶ `b27`: the demo route "after `get_status`" (v2:106-112, the `git diff`); `StatReload` and, extra
  `b30`, `/readyz` back to 200 after the CNN reloads. ▶ `b28` (`2.23606797749979`), ▶ `b29`
  (`?x=3&y=4` → `5.0`).
- ▶ `b31` `/api/docs` (`Cheese App API - Swagger UI`, `url: '/api/openapi.json'`); extra `b32`: all
  25 operations, the tree's leaves. ▶ `b33` "Try `GET /api/newsletters`" (`limit=2`: "Spanish Cheese
  Journey", "The Art of Blue Cheese", newest first) — A41's JSON, now real. Extra `b34`: an unknown
  id → `404 {"detail":"Newsletter not found"}`.
- ▶ Review the code: the README's table (v2:123-132) as a file map, one beat.

**S09 · A chat is a file, not a memory (~270) — `s09_chat.py` · `ChatIsAFile`.** Tracker B 9–10.
- `lecture_ref(18, "27 (Frontend)")`: B27's handler, "use Gemini to generate text", next to the real
  pair CODE(`api/routers/chat.py`: 58-76): start (`POST …/chats`) and continue
  (`POST …/chats/{chat_id}`). Kindly (Conflict 2): the slide's `/chat` is shorthand; the real path
  names the mode, `/api/llm/chats`.
- V7 with CODE(`chat.py`: 19-23, 35-43): the UUID header, `add_turn`. Extras `b36` (no session id →
  422) and `b37` (empty message → 422) as V7's bounces.
- Extra `b39`, Identify, fully offline: the repo's own `blue-cheese.jpg` → `200`, a `cnn` reply,
  **`"prediction_label": "parmigiano", "accuracy": 58.22`**. "A blue cheese, called parmigiano, at
  58 percent. The API passes on what the model guessed, confidence included." Extras `b41`/`b42`:
  the chat file and the photo on disk under `persistent-folder/chat-history/llm-cnn/…`.
- Extra `b38`, Ask: `Internal Server Error`, `[HTTP 500]`; in the uvicorn terminal, the
  `RefreshError … account not found` traceback (`b21`, first and last lines). GOLD tag on the Gemini
  hop. "With your key, Gemini's answer appears here." The reply's shape: `expected/02` (`expected`).
  Erratum, kindly: the README's Troubleshooting lists "Gemini: 403/404"; a key Google rejects shows up
  as a plain 500 — read the API's terminal first.
- The README's two notes (v2:134-138): history rebuilt from disk ("any copy of the API can answer";
  the second API copy in V7) and plain `def` routes run in a thread.
- ▶ `b44` `pytest` in a second terminal: `Container 'cheese-app-api-service' is already running.
  Shelling into it...`, `collected 26 items`, **`26 passed in 0.51s`** (GREEN). "Keep this container
  running." Part 1 ends on the parked question (see Length and parts).

### Part 2 · The frontend

**S10 · Why a framework: React with Vite (~310) — `s10_react.py` · `ReactShell`.** No tracker for
the first half; then tracker R 1–4.
- Recap in one breath: the API is up on 9000; now a page that uses it.
- `lecture_ref(18, "30–37 (Frontend)")`: V8: one HTML page per feature (B30), its problems (B31:
  nothing shared, every page loads separately: slow), the fix (B32: a single-page app of components,
  with a framework); B33's frameworks, React highlighted; B35: components in JSX; B36–B37: Header /
  Content / Footer, "header defined only once".
- Kindly (Conflict 7, updated): "The lecture says React. In today's repo that is React with Vite, a
  development server and build tool, and React Router for the pages." CODE(`src/main.jsx`: 13-28,
  the route table) and CODE(`src/App.jsx`, the lines with `<header>`, `<Outlet />`, `<footer>`):
  B37's two labels land on them.
- ▶ `d01`, ▶ `d02` `./docker-shell.sh`: `Building cheese-app-frontend-react (Dockerfile.dev)...`,
  `Node version: v24.22.1`, `Installing dependencies...`, `added 257 packages`; CODE(`docker-shell.sh`:
  15-23): the code mounted, `node_modules` in a **named volume**, `-p 3000:5173`, the network.
- ▶ `npm run dev`: `VITE v8.3.5 ready`, `Local: http://localhost:5173/`, `Network: http://172.19.0.4:5173/`
  (`d02:80-83`). "Both are addresses inside the container. On your laptop: 3000." ▶ `d03`: open
  3000: `<title>Formaggio</title>`, one `<div id="root">`, `/src/main.jsx`: the whole app is one
  page and a script. Extra `d08`: `/podcasts`, `/newsletters`, `/chat?model=llm`, even `/nope` →
  `200 text/html`: the browser picks the page (V8's address bar).

**S11 · One origin: the Vite proxy (~290) — `s11_proxy.py` · `OneOrigin`.** Tracker R 5–7.
- The hook's answer. `lecture_ref(18, "24–26 (Frontend)")`: the lecture's picture: the page's
  JavaScript calls the API. CODE(`src/lib/api.js`, the relative `/api` base and the session id in
  `localStorage`, ≤ 12 lines) and CODE(`vite.config.js`: 5-15): `proxy: { '/api': …
  'http://cheese-app-api-service:9000' }`, `host: true`, 5173.
- V1 + V5: the browser only ever talks to `localhost:3000`; Vite, a Node process inside the frontend
  container, forwards `/api` by container name across `cheese-app-network`. Extra `d04` again:
  `server: uvicorn` through port 3000. An origin = scheme + host + port; one origin → the browser has
  nothing to object to, so the API needs no CORS (extra `b43`: no `access-control-*` header, preflight
  405). `docs/contract.md:6-7` says it in the repo's words.
- **PONDER 3** (8 s), answered right after with V5: the laptop's DNS knows no container names; only
  code that runs inside the network can use them (Vite's proxy, nginx, the API).
- Extra `d09`: unplug the API from the network for one request → the browser gets `502` with an
  empty body; Vite logs `ENOTFOUND cheese-app-api-service` (`d02:85-86`). Troubleshooting row
  "Pages load with no content".
- ▶ Review the app (v2:166-174) as the browser `illustration` (`expected/03`): Home, Podcasts,
  Newsletters load through the API; Chat's three modes: extra `d07` Identify through the proxy →
  `200` with the `cnn` reply, extra `d06` Ask → `500` (as in S09). "Recent" lists the session's chats.
- ▶ Review the code: the README's table (v2:177-185) in one beat. ▶ `d12` `npm run check`:
  `eslint . && prettier --check . && vite build`, `All matched files use Prettier code style!`,
  `✓ 2385 modules transformed.`, `dist/assets/index-….js 440.48 kB`. "That build is what production
  serves."

**S12 · Production: nginx instead of Vite (~260) — `s12_production.py` · `NginxImage`.** Tracker P
(`e98fa55` README) 1–5, all extras.
- Kindly: the README you clone today no longer has this section (it was replaced by "Setup & Run"
  on the recording day); the files are still in `main`, and the lecture's architecture puts NGINX in
  front, so we run it from the earlier README's commands (marked `extra`).
- CODE(`cheese-app-v2/src/frontend-react/Dockerfile`: 1-16): two stages, `npm ci` + `vite build` →
  `nginx:1.31.8-alpine`, only `dist/` copied. CODE(`nginx.conf.template`: 9-33): `/healthz`,
  `location /api/ { proxy_pass ${API_URL}; }`, hashed `/assets/` cached forever, `try_files $uri
  /index.html` for every page.
- `d20` build (first and last lines), `d21` run (`Running envsubst …`, `nginx/1.31.8`), `d22`
  (`Server: nginx/1.31.8`, the built `index.html`), `d23` (`/api/...` through nginx: `200`), `d25`
  (a deep link → `200 text/html`, the SPA fallback), `d27`: **331 MB vs 94.8 MB**. "No Node, no
  Vite: files and one proxy rule."
- V1, `lecture_ref(18, "42 (APIs)")`: A42's point kept: going to production changes the outside
  (the address, nginx in front), not the API code or its port 9000. Kindly (Conflict 9): the
  lecture's production slide shows a domain on 443; the course builds that with NGINX in Lecture 20.
- **PONDER 5** (6 s), then `e01`: with the API stopped, the prod container exits at once:
  `[emerg] host not found in upstream "cheese-app-api-service"` (RED). nginx resolves the name when it
  starts. Fix: start the API first.

**S13 · One command, then clean up (~220) — `s13_compose.py` · `ComposeUp`.** Tracker S 1–6, then
C2 1–2.
- "Instead of three terminals, one command" (v2:193). ▶ `f01`: `GCP_PROJECT` in
  `src/docker-compose.yml`, twice (two hunks). CODE(`src/docker-compose.yml`, ≤ 12 lines at a time):
  the four services, the loader's `--get … || --download --load` entrypoint.
- ▶ `f02`: stop what runs (Ctrl-C, `exit`, then `docker compose down` in `src/vector-db`; Compose
  warns that two variables are unset: they come from `docker-shell.sh`, harmless here). ▶ `f03`
  `cd src`.
- ▶ `f04-docker-compose-up` (`docker compose up --build`): the two WARN lines (an existing network
  and volume "not created by compose": warnings, not errors; `f04:66-68`), four containers created
  (`f04:73-76`), Chroma's banner, uvicorn, `VITE v8.3.5 ready`. V2: the laptop's four boxes light up
  together. Extra `f04-x-compose-ps`: the loader `Exited (0)`: it found the books already loaded.
- ▶ Open the app: `f04-curl-3000`, `f04-curl-api-docs` (port 9000). Erratum, kindly: the README
  prints `localhost:900` (v2:213); extra `f04-x-readme-url`: `Failed to connect`. Use 9000.
- ▶ Ctrl-C (`f04:143-151`), ▶ `f10` `docker compose down`. ▶ C2: `e02` (nothing left in
  `src/vector-db`), `e03` `docker system prune` (`[y/N] y`, `Total reclaimed space: 5.328GB`).
  Extra `e04`: what prune keeps: every tagged image (the API's 4.2 GB) and the `node_modules` volume
  (erratum: the cleanup misses it; `docker volume rm cheese-app-frontend-react-node_modules`).

**S14 · Tutorial 24 lives on branch 2025 (~290) — `s14_branch.py` · `Branch2025`.** Tracker T23 1–7.
- Kindly, the second time: the simple frontend the lecture teaches was removed from `main` on the
  recording day; it lives on branch `2025`, together with last year's API, which serves it. One
  switch, then everything matches.
- ▶ `c01` `git switch 2025` refused (RED): your edits to four files; extra `c01b`
  `git stash && git switch 2025` (branch name cropped in the stash line). Extra `c02`: `14f2a14`,
  `src/` has `frontend-simple` again.
- Extra `c03`: last year's vector-db script reads a second key name, `llm-service-account.json`
  (erratum: the 2025 README names only one); extra `c04`: the two project-id edits.
- ▶ `c05`/`c06`: `cd cheese-app-v2/src/vector-db`, `sh docker-shell.sh` (2025's README spelling),
  the same load: 11 files, 14,356 chunks (first/last lines only, "you have seen this"); extra `c07`
  (`chromadb/chroma:latest`, still compatible at the time of recording).
- ▶ `c10`/`c11`: `cd cheese-app-v2/src/api-service`, `sh docker-shell.sh`, `uvicorn_server`.
  Differences worth one line each: `WatchFiles` instead of `StatReload`; the CNN loads **before**
  `Application startup complete.` (no readiness probe yet: this is what `main` improved). ▶ Verify
  9000: extra `c12` `{"message":"Welcome to AC215"}`. Errata, kindly: the 2025 README's demo route and
  "enable the routes" steps are already done in the code (`c13`: `service.py:30-33`; `c14`: four
  routers on) — don't paste them again (a duplicate route). The 2025 Gemini model is retired
  (digest gotcha 8); with a key, its chat would still fail until the model name is updated.
- CODE(`cheese-app-v2-at-14f2a14/src/api-service/api/service.py`: 14-22): `CORSMiddleware`,
  `allow_origins=["*"]`: the permission slip `main` no longer needs.

**S15 · Last year's pages: CORS and the preflight (~310) — `s15_cors.py` · `CorsPreflight`.**
Tracker T24 1–6.
- ▶ `c20`/`c21`: `cd cheese-app-v2/src/frontend-simple`, `sh docker-shell.sh`, `http-server`.
  ▶ Home page `c22` (`Formaggio.me`, links to `/newsletters.html`, `/chat.html`).
- `lecture_ref(18, "24–26 (Frontend)")`: ▶ Newsletters `c23`: the page loads axios and
  `newsletters-main.js`; extra `c24`: `baseURL: 'http://localhost:9000'`. V1, B24–B26 exactly: the
  page came from 8080, its JavaScript calls 9000 itself: a **different origin**. Extra `c25`: `307`
  (`/newsletters` → `/newsletters/`), then `200`, both with `access-control-allow-origin: *`. The
  uvicorn log (`c11:79-80`): `GET /newsletters?limit=100 307` then `200`. Kindly (Conflict 1): the
  lecture's route has no slash; the router's does; the log shows the one extra round trip.
- `lecture_ref(18, "27 (Frontend)")`: ▶ Chat `c26`; V1 with step **0**: a JSON POST with a custom
  `X-Session-ID` header makes the browser send a preflight first. Extra `c27`: `OPTIONS` → `200`,
  `access-control-allow-methods: …`, `access-control-allow-headers: content-type,x-session-id`,
  `access-control-max-age: 600` (the browser reuses the answer for ten minutes). The log
  (`c11:81-82, 146`): `OPTIONS /llm/chats 200`, `POST /llm/chats/ 307`, `POST /llm/chats 500`.
  Extra `c28`: the 500 carries the CORS header, so a browser shows the real error, not a CORS one.
- CORS in one sentence: the browser enforces it, about the server's permission; `curl` and
  `/api/docs` never see it. Side by side: 2025 = ask permission on every new origin; `main` = one
  origin, a proxy inside.
- **PONDER 4** (8 s), answered: the origin the page calls. The API then dropped the middleware
  because nothing needs it.
- Stop: Ctrl-C and `exit` in the two terminals; extra `c30` (`docker stop cheese-app-vector-db`);
  extra `c31` (`git checkout -- . && git switch main`, branch name cropped): back to `main` (`git
  stash pop` restores your earlier edits if you want them; shown without output, not captured).

**S16 · Tear down, recap, what's next (~220) — `s16_recap.py` · `Recap`.** No tracker.
- Teardown card (see "Costs and teardown"), each line spoken.
- V2 last time, `lecture_ref(18, "19–21 (APIs)")`: the laptop's four boxes rise back into the
  lecture's cluster; NGINX (S12), Artifact Registry, the persistent disk light GREY dashed: L19–L22
  build it. "Well not really, we need to build it" — now with the pieces in hand.
- `lecture_ref(18, "46 (APIs)")` + `lecture_ref(18, "40–41 (Frontend)")`, 15 s: your own app: draw
  your project's solution and technical architecture; the app-building crash course and template
  repos (names only).
- Recap questions (5, one at a time; answers in exercises.md) — see below. Point to the study guide
  and exercises in MLOps_Learning.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 220 | S10 ReactShell | 310 |
| S02 Blueprint | 250 | S11 OneOrigin | 290 |
| S03 ServerAndApp | 290 | S12 NginxImage | 260 |
| S04 FunctionToUrl | 250 | S13 ComposeUp | 220 |
| S05 StaticPages | 270 | S14 Branch2025 | 290 |
| S06 VectorDb | 270 | S15 CorsPreflight | 310 |
| S07 AliveAndReady | 260 | S16 Recap | 220 |
| S08 ScreensToRoutes | 280 | | |
| S09 ChatIsAFile | 270 | | |
| **part 1** | **2,360** | **part 2** | **1,900** |

Total ≈ **4,260** words ≈ 24.5 min of narration. Typing, build/load outputs, the browser drawings
and five ponder timers bring it to ~31–33 min. If the script runs long, trim S02's blueprint build
and S14's repeated load first; never trim a README command.

## Ponder questions

Five timed ponders, as Conny decided on 2026-10-21 (3–5 per video); REVIEW.md marks content gate 3
met with that decision. Each is quiz-style with a YELLOW timer and answerable from what was shown
just before. The answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S03 (8 s) | "uvicorn listens on --host 127.0.0.1\ninside the container instead.\ncurl from inside the container: works?\nYour browser on localhost:9000: works?" | Inside: yes (the container's own loopback). Browser: no — the forwarded request arrives on the container's network interface, where nothing listens. That is why it is `0.0.0.0` (V3) |
| 2 | S07 (8 s) | "/healthz says 200, /readyz says 503.\nRestart the container,\nor just wait?" | Wait. The process is alive; it is not ready yet (the CNN is loading). A restart would start the loading over. Orchestrators route traffic on readiness and restart on liveness |
| 3 | S11 (8 s) | "Could the page's JavaScript call\nhttp://cheese-app-api-service:9000\ndirectly?" | No. The JavaScript runs in your browser, on the laptop, whose DNS knows no container names. Only code inside the network (Vite's proxy, nginx, the API) can use them |
| 4 | S15 (8 s) | "Last year's page needed CORS.\nThis year's React app does not.\nWhat changed: the API,\nthe browser, or the origin it calls?" | The origin: the React page calls its own origin (3000) and a proxy forwards; same origin, nothing to permit. The API dropped the middleware as a consequence |
| 5 | S12 (6 s) | "The production frontend container\nwon't start while the API is down.\nWhy would a page server care?" | nginx resolves `cheese-app-api-service` for `proxy_pass` when it starts (`nginx.conf.template:14`); no such host → `[emerg]`, exit 1 (`e01`). Start the API first |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Trace one newsletters request through the lecture's steps on `main`. Which container does the
   browser talk to, and at which step does the API's port come in?
2. What do `api.service:app`, `--host 0.0.0.0` and `--reload` each do, and why does `/square_root`
   answer 307?
3. `/healthz` vs `/readyz`: what does each one check in this API?
4. Where does a chat live between two messages, and why can any copy of the API answer it?
5. Which file decides where `/api` goes in development, which in production, and why does the 2025
   API need `CORSMiddleware` while `main`'s does not?

(SLIDES' extra recap items — "at which step does the frontend container take part" and "the file that
fixes reuse" — and digest recap Q1/Q2 go to exercises.md.)

## Errata and drift to state (kindly, with the fix)

1. **`main` changed on the recording day** (`e98fa55`, then `447b5c3`): the simple frontend (the
   course's Tutorial 24) is gone from `main` → `git switch 2025` (S02, S14). The "(23)/(25)" headings
   are gone, so the course site's anchors and the slides' tutorial links land at the top of the
   README → follow the section names (S02, tracker only).
2. **"Production images" was removed from the README at `447b5c3`** while its Dockerfile and nginx
   template remain → shown from `e98fa55`'s README, marked `extra` (S12).
3. **v1 README paths lack `src/`** (v1:41, :75) → `cd cheese-app-v1/src/api-service`,
   `…/src/frontend-simple` (S03, S05).
4. **v1's `<p>` snippet is an old whole `<body>`** (v1:88-95) → add only the `<p>` (S05).
5. **`localhost:900`** (v2:213) → 9000 (S13).
6. **A rejected key shows as 500, not "Gemini: 403/404"** (Troubleshooting v2:230-231) → read the
   API terminal; check the key, project, role (S09).
7. **`--chat` asks a fixed question** (`cli.py:377`) → edit the line (S06).
8. **Cleanup leaves the `node_modules` volume and every tagged image** (v2:235-246, `e04`) →
   `docker volume rm …`, `docker image rm …` if you need the disk (S13, S16).
9. **`docker compose up` warns about the network and volume** that the shell scripts made →
   harmless; the README could mark them `external: true` (S13).
10. **2025: `git switch` refuses with edits** → `git stash` first (S14).
11. **2025: two key names** (`llm-service-account.json`) and **already-applied README steps**
    (`square_root`, routers) → copy the key under both names; don't paste the steps again (S14).
12. **2025: a retired Gemini model** (`gemini-2.0-flash-001`, digest gotcha 8) → with a key, the
    2025 chat still fails until updated; `main` uses a current model (S14, one clause).
13. **Slides vs repo** (SLIDES Conflicts, updated by the captures): one-file route vs router + `/api`
    prefix (S08); `/chat` vs `/api/llm/chats` (S09); six route groups and MCP vs five routers, no
    agent, no MCP (S08); `data-service.json` vs `ml-workflow.json` and the idealized tree (S02);
    `localhost:9000` inside the container vs `0.0.0.0` (S03); "React" = React + Vite + React Router
    today (S10); A42's domain on 443 vs NGINX in L20 (S12).
14. Not in the video (exercises only): the v1/2025 simple-frontend Dockerfile's `ADD --chown=app:app`
    (no such user; BuildKit builds it); the stale `container-architecture-*.png` images; the 2025
    simple-frontend chat quirks (digest gotcha 19); chat photos saved as `.png` whatever their format.

## Costs and teardown

Nothing in this lecture creates a billable cloud resource. GOLD tags appear only where a call **with
your own key** would be billed: the vector-db `--chat` (S06), Ask / Cheese books (S09, S11), the
compose run (S13, one tag). No prices are stated. Disk is the other cost: ~10 GB, the API image
alone 4.2 GB (GOLD-outlined "disk" chip in S07 and S16).

Teardown card (S16), each line spoken:
1. Ctrl-C and `exit` in every container terminal (the `--rm` containers delete themselves).
2. `docker compose down` in `src/vector-db` (or in `src` after Compose).
3. Branch `2025`: stop its Chroma, `git switch main`.
4. `docker system prune`, and check its list first: it removes other projects' stopped containers and
   build cache too.
5. What prune keeps: `docker volume rm cheese-app-frontend-react-node_modules`; the images
   (`docker image ls`, then remove the 4.2 GB API image if you need the space).
6. Your key stays in `secrets/`, outside every repository; never commit it.

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order per section.

| README instruction | README line | capture | scene |
| --- | --- | --- | --- |
| v1 · Clone or download | v1:17-18 | `p01` (`git clone`, extra spelling) | S02 |
| v2 · Clone or download | v2:22-23 | `p02` | S02 |
| create `secrets`, `persistent-folder` next to the repos | v1:20-35, v2:25-45 | `p05`, `p06` | S02 |
| go to `cheese-app-v1/api-service` | v1:41 | `a01` (fails), `a02` | S03 |
| `sh docker-shell.sh` | v1:44 | `a03` | S03 |
| `uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"` | v1:47 | `a03:38` | S03 |
| test `http://localhost:9000/` | v1:48 | `a04` | S03 |
| add `square_root` at the end of `api/service.py` | v1:50-58 | `a05` | S04 |
| `http://localhost:9000/square_root/`, `…/?x=2&y=10` | v1:59, :61 | `a06`, `a07` | S04 |
| `http://localhost:9000/docs` | v1:66 | `a10` | S04 |
| go to `cheese-app-v1/frontend-simple` | v1:75 | `a19` (fails), `a20` | S05 |
| `sh docker-shell.sh`, `http-server` | v1:78, :82 | `a20b` | S05 |
| test `http://localhost:8080/` | v1:83 | `a21` | S05 |
| add a `<p>` in `index.html`, refresh | v1:85-97 | `a23`, `a24` | S05 |
| `docker container ls` · stop · `docker system prune` · `docker image ls` | v1:103-106 | `a30`–`a32` | S05 |
| change `GCP_PROJECT` in both `docker-shell.sh` | v2:47-50 | `b03` | S06 |
| `cd src/vector-db` · `./docker-shell.sh` | v2:58, :62 | `b05`, `b06` | S06 |
| `python cli.py --download --load --chunk_type recursive-split` | v2:67 | `b06:44` | S06 |
| `python cli.py --chat --chunk_type recursive-split` | v2:75 | `b06:209` | S06 |
| `exit` | v2:78 | `b06:298` | S06 |
| `cd src/api-service` · `./docker-shell.sh` | v2:88, :92 | `b20`, `b21` | S07 |
| `api_server` | v2:97 | `b21` | S07 |
| `/healthz`, `/readyz` | v2:101-103 | `b22`–`b24` | S07 |
| add `/api/square_root` after `get_status` | v2:106-112 | `b27` | S08 |
| `/api/square_root`, `?x=3&y=4` | v2:114-115 | `b28`, `b29` | S08 |
| `/api/docs`, try `GET /api/newsletters` | v2:119-120 | `b31`, `b33` | S08 |
| review the code (table) | v2:122-138 | source panels | S08, S09 |
| `pytest` | v2:142 | `b44` | S09 |
| `cd src/frontend-react` · `./docker-shell.sh` · `npm run dev` | v2:152, :156, :161 | `d01`, `d02` | S10 |
| open `http://localhost:3000` | v2:164 | `d03` | S10 |
| review the app (Home, Podcasts, Newsletters, Ask, Identify, Cheese books, Recent) | v2:166-174 | `illustration` + `d06`–`d08`, `expected/03` | S11 |
| review the code (table) | v2:176-185 | source panels | S11 |
| `npm run check` | v2:189 | `d12` | S11 |
| `e98fa55` · Ctrl-C, `exit`; `docker build -t cheese-app-frontend-react:prod .` | e98fa55:201-203 | `d20` (extra) | S12 |
| `e98fa55` · `docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod` | e98fa55:207 | `d21` (extra) | S12 |
| `e98fa55` · open 8080; `docker images \| grep cheese-app-frontend-react` | e98fa55:210-214 | `d22`, `d27` (extra) | S12 |
| `GCP_PROJECT` in `src/docker-compose.yml` (twice) | v2:195-196 | `f01` | S13 |
| stop running containers; `docker compose down` in `src/vector-db` | v2:198-199 | `f02` | S13 |
| `cd src` · `docker compose up --build` | v2:203, :207 | `f03`, `f04` | S13 |
| open 3000 and `/api/docs` | v2:213 | `f04-curl-3000`, `f04-curl-api-docs` (+ `f04-x-readme-url`) | S13 |
| Ctrl-C · `docker compose down` | v2:218-221 | `f04`, `f10` | S13 |
| Docker Cleanup: `docker compose down` · `docker system prune` | v2:237-246 | `e02`, `e03` | S13 |
| 2025 · `cd cheese-app-v2/src/vector-db` · `sh docker-shell.sh` · load | 2025:46, :51, :56 | `c05`, `c06` | S14 |
| 2025 · `cd cheese-app-v2/src/api-service` · `sh docker-shell.sh` · `uvicorn_server` · verify 9000 | 2025:74, :79, :92, :94 | `c10`, `c11`, `c12` | S14 |
| 2025 · `cd cheese-app-v2/src/frontend-simple` · `sh docker-shell.sh` · `http-server` | 2025:153, :158, :163 | `c20`, `c21` | S15 |
| 2025 · `/index.html` · `/newsletters.html` · `/chat.html` | 2025:170, :174-176, :179-181 | `c22`, `c23`, `c26` | S15 |

The Troubleshooting table (v2:223-233) is quoted row by row where its symptom appears (S07 readyz,
S09 Gemini, S11 empty pages, S13 port allocated) from `expected/04`, tagged `recorded`.

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, start from L14's/L13's):
  - tracker factories `tracker_se`, `tracker_a`, `tracker_f`, `tracker_c1`, `tracker_v`, `tracker_b`,
    `tracker_r`, `tracker_p`, `tracker_s`, `tracker_c2`, `tracker_t23`, `tracker_t24`, with the step
    lists above and a caption variant for the commit (`e98fa55 README`, `branch 2025 · 14f2a14`);
  - prompts per capture (`P_LAPTOP`, `P_V1_API`, `P_V2_SRC`, container prompts read from the capture
    line, never typed);
  - tags `your_turn`, `extra_tag`, `illustration_tag`, `expected_tag`, `recorded_tag`, `cost_tag`
    (GOLD), `lecture_ref`;
  - a `browser_window(url, rows)` helper for the schematic browser (`illustration`), no logos;
  - set-piece classes `RequestTrace` (V1, the spine: one layout, numbered hops, optional hop 0 and
    3½, swappable middle box: Vite / nginx / none), `ArchitectureMap` (V2), `ServerAppDiagram` (V3),
    `RouteTree` (V4), `TwoLocalhosts` (V5), `ProbeLamps` (V6), `ChatFile` (V7), `OneShell` (V8).
    A helper never reuses a scene class name from `video.yaml`.
- **The sandbox framing is load-bearing.** Said once in S06. Afterwards every Google error is the
  lesson, `with your key, …` is the only way a Gemini answer is mentioned, and no answer text appears.
- **Long outputs**: `b06` load (show the counter, first/last books), `b21` (build: first lines, `…`,
  last; the TensorFlow lines collapse), `d20`, `f04` (pick the WARN lines, the four `Created` lines,
  one line per service), `c06`, `c11` (as `b06`/`b21`). The uvicorn access-log lines are the best
  evidence in this video: show them beside the curl that caused them.
- **Never read aloud**: dates, PIDs, container ids, network ids, hashed asset names, UUIDs (say "a
  UUID"), the `[HTTP …]` suffix (a curl option, say "status 422").
- **Masking**: `‹instructor›` for `cheese-app-v1/src/frontend-simple/index.html:57`, the same "About"
  paragraph at `14f2a14`, and `cheese-app-v2/src/vector-db/cli.py:76` — better: keep these lines out
  of every panel. Crop the branch name in `p03`, `p04`, `b01`, `c01b`, `c31`.
- **Lexicon heads-up** (script stage): uvicorn ("you-vee-corn"), FastAPI, Vite ("veet"), nginx
  ("engine-x"), Chroma, `http-server`, `api_server`, `uvicorn_server`, `healthz`/`readyz` ("health-z",
  "ready-z"), `0.0.0.0` (phrase key as in L14), `5173`, `9000`, `8080`, `3000`, `8000` (say "port
  nine thousand", "eighty-eighty", "three thousand", "eight thousand", "fifty-one seventy-three"),
  CORS ("cores"), preflight, JSX, `localStorage`, `X-Session-ID`, UUID, parmigiano, Tolminc, 307, 422,
  `14,356`, `.keras`, `--rm`.
- **Chinese glossary heads-up**: stay English: API, REST API, FastAPI, uvicorn, route, router, prefix,
  endpoint, request, response, status code, query, header, JSON, port, published port, container,
  image, network, volume, bind mount, Docker Compose, Chroma, vector DB, embedding, RAG, CNN, Gemini,
  probe, liveness, readiness, session ID, frontend, backend, HTML, CSS, JavaScript, React, Vite,
  React Router, component, JSX, single-page app, dev server, proxy, nginx, origin, CORS, preflight,
  build, `dist`, branch, stash, pytest. Reuse `../ac215-l16-exam/i18n/zh/glossary.yaml` where it
  agrees.

## Things never to do on screen

Series rules:
- No slide images, page renders or long slide text; re-draw the idea and cite with `lecture_ref`,
  only while the picture is on screen. No Google/GCP logos, console or browser screenshots.
- No real person's name: the instructor is never named on screen or in subtitles (`‹instructor›`);
  the prompt user is `student`; the staff member's branch name is cropped.
- No hand-typed output: every terminal line comes from `assets/terminal/`; `expected` and
  `recorded` panels name their source.
- No command spelled differently from the README (the `git clone` spelling and all `e98fa55`
  commands are `extra`).
- No credentials: no key, token, key-file content or project id that looks real (`your-gcp-project`
  only).

Lecture-specific:
- Never show or describe a Gemini or RAG **answer** (none was captured or documented).
- Don't say the frontend container calls the API in the 2025 stack (the browser does), or that the
  browser calls 9000 on `main` (it calls 3000; Vite or nginx forwards).
- Don't call CORS a server-side block or a security feature of the API; the browser enforces it.
- Don't say Next.js for today's React app, or MCP / agent chat for anything this repo runs.
- Don't present `e98fa55`'s Production images or the 2025 branch as today's README steps: always
  tagged with their commit.
- Don't advise `--host 127.0.0.1`, editing `docker-shell.sh` ports blindly, `npm install` on the
  host, or committing `secrets/`.
- Don't pass the CNN's "parmigiano" off as a bug in the app: it is the model's guess, reported
  honestly.

## Left for exercises.md (not in the video)

- Digest E1 (`/hypot/{x}` path vs query), E2 (proxy target `localhost:9000`), E3 (API before Chroma),
  E4 (2025 RAG follow-up 500 looks like CORS), E5 (Identify then "how should I store it?"),
  E6 (extra field / empty content), E7 (embedding model on one side), E8 (an `/about` route).
- `a11` (the OpenAPI JSON), `b35` (podcasts + the MP3), `d05` (transformed JSX), `d10`/`d11`
  (containers, the volume's 193 MB), `d24`/`d28` (nginx `/healthz`, image layers),
  `f04-x-loader-logs` (empty), `b09` (78.8 MB of outputs + 50.9 MB of Chroma data).
- The v1 frontend Dockerfile user, the stale architecture PNGs, `.png` for JPEG photos, the
  `pipenv` branches.
