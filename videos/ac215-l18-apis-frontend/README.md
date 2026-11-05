# AC215 · Lecture 18 — APIs and frontend: a FastAPI service, a simple page and a React app

A follow-along walkthrough of the Lecture 18 tutorials of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *APIs + Frontend*, in two repositories:

- [dlops-io/cheese-app-v1](https://github.com/dlops-io/cheese-app-v1), branch `main` @
  [`ce03a10`](https://github.com/dlops-io/cheese-app-v1/tree/ce03a1029dd6f655a86e3e3edc99bb5938f0cbf8),
  its whole README: *Setup Environments*, *Backend API Container*, *Frontend App (Simple) Container*
  and *Docker Cleanup*;
- [dlops-io/cheese-app-v2](https://github.com/dlops-io/cheese-app-v2), branch `main` @
  [`447b5c3`](https://github.com/dlops-io/cheese-app-v2/tree/447b5c3c2c06d724e86dddf70e1a244dbe3d7c47)
  (2026-11-05): *Tutorial: Environment Setup*, *Tutorial: Vector DB for RAG Setup*, *Tutorial: Backend
  APIs* (the course's Tutorial 23), *Tutorial: React Frontend Setup* (Tutorial 25), *Tutorial: Setup &
  Run Cheese App*, *Troubleshooting* and *Docker Cleanup*; plus the *Production images* section of the
  README one push earlier
  ([`e98fa55`](https://github.com/dlops-io/cheese-app-v2/tree/e98fa551c5d380517c6dc775ae626ea1a828e4d3),
  shown as extras), and **Tutorial (24): Simple Frontend App** from branch `2025` @
  [`14f2a14`](https://github.com/dlops-io/cheese-app-v2/tree/14f2a1420b43e9f24e977a9e67b53d7e2614013d).

**Which commit.** The course page links the repositories' default branches, and cheese-app-v2's `main`
moved twice on the recording day: at 07:23 (−0500) to `e98fa55` ("removed frontend simple", "upgraded
vector-db", "code cleanup", 131 files), then at 07:52 to `447b5c3` (an updated README and a new
`src/docker-compose.yml`; every other file is the same). `447b5c3` is what a student clones today, so
the video follows it. It no longer has the simple frontend that the lecture teaches (and the course
page still links), so that part comes from branch `2025` = `14f2a14`, the commit the course map and
the published exam edition [`../ac215-l16-exam/`](../ac215-l16-exam/) name, run with its own vector
DB and API, because the 2025 pages call routes `main`'s API no longer serves. The video says so
kindly: `git switch 2025` to follow along, `git switch main` to come back. Details in
[`ASSETS.md`](ASSETS.md), "Which commit".

A page on port 3000 asks for two newsletters, and the answer comes from uvicorn, the API's server on
port 9000. Last year's version of the same app needed every answer to carry a CORS permission slip;
this year's API sends none. Who carried the request? The video builds the answer the lecture's way,
one request, hop by hop: a Python function becomes a URL in cheese-app-v1, then cheese-app-v2 runs
four containers on one Docker network (Chroma with the cheese books, the API with its probes, routers
and chat files, a React app), Vite in development and nginx in production carry `/api` across by
container name on one origin, `docker compose up --build` starts the whole app, and branch `2025`
shows last year's simple frontend with CORS and its preflight.

Watch it with both clones open, Docker running and about 10 GB free (more for branch `2025`), and
pause at every `▶ your turn` to run the command. **Everything runs on your laptop**: nothing here
creates a billable cloud resource. Only the chat answers call Vertex AI (Gemini and the embedding
model) with your own key from Lecture 15; a GOLD tag marks each place. The tracker top left shows the
README step; a gray `extra` tag marks a command that isn't in the README, and a gray "Lecture 18 ·
slides …" tag top right points to the lecture slides (the *APIs* and *Frontend* decks) the scene
stands on.

The terminal sessions were recorded on 2026-11-05 in a fresh, empty Docker 29.8.2 engine standing in
for your laptop (Compose v5.6.0, git 2.54.0). Everything that runs on the laptop ran live: both
`docker-shell.sh` builds, uvicorn and FastAPI, the demo routes, `/docs` and `/api/docs`, the 14,356
chunks loaded into Chroma, `/healthz` and `/readyz`, the CNN naming a cheese photo, `pytest`
(26 passed), the Vite dev server and its proxy, `npm run check`, the nginx production image,
`docker compose up --build`, the 2025 simple frontend with CORS, and the clean-up. That machine had
**no Google account, no project and no key** (its key file is well formed but belongs to no account):
every Gemini or embedding call is shown up to its honest first error, `invalid_grant: account not
found`, and no Gemini answer appears anywhere. The browser is a schematic drawing tagged
`illustration`, filled with what the captured HTML and JSON say. Project IDs on screen are
placeholders. Series format: [`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with
every command: [MLOps_Learning · guides/L18-apis-frontend.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L18-apis-frontend.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l18-apis-frontend.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l18-apis-frontend.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l18-apis-frontend_part1.mp4` | part 1, DURATION_P1: the API — from a Python function to a four-container backend (S01–S09). Release asset, not in Git |
| `output/ac215-l18-apis-frontend_part2.mp4` | part 2, DURATION_P2: the frontend — React, one origin, nginx, and last year's CORS (S10–S16). Release asset, not in Git |
| `output/ac215-l18-apis-frontend.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l18-apis-frontend.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l18-apis-frontend.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging and think questions, with answers; what was re-run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of both slide decks in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-05, a fresh Docker engine, no Google account); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `ce03a10`, `447b5c3` (with `e98fa55`'s README for *Production images*) and `14f2a14` |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean
video and the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whether a server
listening on `127.0.0.1` inside its container still answers a curl from inside and your browser
outside; whether to restart or wait when `/healthz` says 200 and `/readyz` says 503; whether the
page's JavaScript could call `http://cheese-app-api-service:9000` directly; why a production page
server refuses to start while the API is down; and what changed between last year's page, which
needed CORS, and this year's React app, which doesn't. Five test-yourself questions close the video
(answers in `exercises.md`).

**Part 1 · the API: from a Python function to a four-container backend**

1. **Who answered on port 3000?** — a request to the frontend's port answered by uvicorn, the API's
   server on 9000; last year's answers carried `access-control-allow-origin: *`, this year's carry
   nothing; the lecture's six numbered steps of one chat message plus the step it never draws, 3½,
   the courier; the lecture's blueprint ("well, not really, we need to build it"); what you need
   (both clones, Docker, about 10 GB, your Google key only for chat answers); how the tracker, code
   panels and `▶ your turn` work.
2. **The blueprint, and your folders** — where the app sits next to the ML pipeline; the lecture's
   technical architecture layer by layer, with the cluster's NGINX, app on 3000, API on 9000 and
   vector database on 8000, which you run on your laptop; the folder rule (one Git folder per app,
   one per service under `src`, secrets outside Git); clone both repositories; create `secrets/` and
   `persistent-folder/` yourself so Docker doesn't make them root's; `main` moved twice on the
   recording day, and the simple frontend now sits on branch `2025`.
3. **v1: a server, an app, a port** — requests, responses and ports; a REST API with FastAPI as the
   one door to the stores; the README's path without `src/`; `sh docker-shell.sh` (`--rm`, mounted
   code, `-p 9000:9000`); uvicorn is the server, FastAPI the app; `api.service:app`, `--host
   0.0.0.0`, `--reload`; the welcome route and the CORS middleware v1 already has; the lecture's trip
   to `localhost:9000`, and what "localhost" means on the slide.
4. **A Python function becomes a URL** — why `0.0.0.0` (the ponder's answer); the README's
   `square_root` route as a decorated function, picked up by StatReload; defaults and the query
   string; `?x=abc` answers 422 from the `float` type hint; no trailing slash answers 307; the
   server's log; `/docs`, built from your code.
5. **Files for the browser: the simple frontend** — HTML, CSS and JavaScript; `http-server` on 8080
   with a one-hour cache (the addresses it prints are the container's); the lecture's first trip;
   `main.js`'s sample podcasts that would normally come from an API; the README's stale `<body>`
   snippet (add only the paragraph); hard refresh; the v1 clean-up and `docker system prune`.
6. **v2: four containers, and the cheese books** — Chroma on 8000, a loader, the API on 9000, React
   on 3000, one Docker network; the prerequisites and what bills your project; the recording's key
   that belongs to no account; your project ID in both scripts; `./docker-shell.sh` in
   `src/vector-db` (network, build, Compose starts Chroma); `--download --load`: 11 books, 14,356
   chunks, downloaded, not recomputed; `--chat` fails at the first Google call here, and always asks
   its own fixed question; Chroma keeps running, and the network's phone book knows its name.
7. **Start the API: alive, then ready** — `./docker-shell.sh` in `src/api-service` (a slow first
   build: TensorFlow), `api_server`; the script opens a shell in a running container instead of
   starting a second; startup completes at once while a background thread loads the CNN; `/healthz`
   200, `/readyz` 503 "CNN model is loading", then 200; the model downloaded once into your persistent
   folder; v1's `/` and `/docs` now answer 404; Kubernetes' liveness and readiness probes.
8. **Screens decide the routes** — the lecture designs routes from the screens; newsletters and
   podcasts routers under `/api`, one function stamping out the three chat routers (the lecture's
   agent group and MCP service aren't in this repository); the demo route `/api/square_root` (and
   `5.0`); `/api/docs` with all 25 operations; `GET /api/newsletters` with a limit of 2, newest first,
   and a 404 for an unknown ID; the README's code table.
9. **A chat is a file, not a memory** — `/api/llm/chats`; the session ID (one random UUID per
   browser) and one JSON file per chat; 422 without a session ID or with an empty message; Identify
   offline: the CNN calls a blue cheese parmigiano, at 58 percent; the files on disk; Ask stops at
   a 500 here, and the shape Gemini's answer has with your key; a rejected key is a plain 500, not the
   README's 403/404; any copy of the API can answer, and plain `def` routes run in threads; `pytest`
   in a second terminal: 26 passed. Keep this container running.

**Part 2 · the frontend: React, one origin, nginx, and last year's CORS**

10. **Why a framework: React with Vite** — one HTML page per feature vs a single-page app of
    components; JSX; the app shell with a header written once; React with Vite and React Router: the
    route table in `main.jsx` and the outlet in `App.jsx`; `./docker-shell.sh` in
    `src/frontend-react` (a named volume for `node_modules`, `-p 3000:5173`, the network);
    `npm run dev` prints 5173, you open 3000; an almost empty HTML page; every address returns the
    same page, because the browser picks the page.
11. **One origin: the Vite proxy** — `api.js` calls relative `/api` paths with the session ID from
    local storage; the proxy rule in `vite.config.js` is the courier, to the API by container name;
    an origin is scheme, host and port, and one origin needs no permission slip; the laptop's DNS
    knows no container names; the API unplugged for one request gives 502 with an empty body;
    reviewing the app (Identify works, Ask and Cheese books stop at the same 500); `npm run check`,
    whose build is what production serves.
12. **Production: nginx instead of Vite** — *Production images* from the earlier README, marked
    extra; the two-stage Dockerfile; the nginx template's `/api` rule and its fallback to
    `index.html` (only a missing asset is a real 404); build `:prod`, run it on 8080; 331 MB vs about
    95 MB; the lecture's production slide: only the outside changes, NGINX in front in Lecture 20; the
    production container won't start without the API: `host not found in upstream`.
13. **One command, then clean up** — `GCP_PROJECT` twice in `src/docker-compose.yml`; the four
    services, with a loader that loads the books only if they are missing; `docker compose down` in
    `src/vector-db` (two harmless warnings); `docker compose up --build` in `src` (the network and
    volume "already exist" warnings, the loader exits with 0); the README's port 900 is 9000;
    `docker compose down`; Docker Cleanup: `prune` deletes the network and about four and a half
    gigabytes of build cache, and keeps every tagged image and the `node_modules` volume.
14. **Tutorial 24 lives on branch 2025** — `git switch 2025` refuses until you `git stash`; last
    year's commit; a second key name for its vector DB; the same 14,356 chunks with a Chroma image
    tagged `latest`; the 2025 API: WatchFiles, the model loads before startup completes, no
    readiness probe; its demo route and routers are already in the code (don't paste them again);
    its Gemini model is retired; and CORS middleware that allows every origin.
15. **Last year's pages: CORS and the preflight** — `http-server` on 8080 and three pages; the
    newsletters page calls `localhost:9000` itself: a different origin, so the browser checks every
    answer for `access-control-allow-origin`; a 307 for one slash; the chat's JSON post with a
    custom header makes the browser ask first, with an `OPTIONS` preflight (allowed origins, methods
    and two headers, for 600 seconds); the 500 carries the header, so the browser shows the real
    error; CORS is the browser's rule about the server's permission; stop, `git switch main`,
    `git stash pop`.
16. **Tear down, recap, and what's next** — the clean-up checklist (exit every container, compose
    down, back to `main`, prune after checking its list, remove the `node_modules` volume and the big
    images by name; your key stays in `secrets/`); the whole trip on `main` with the hook answered;
    the lecture's blueprint, with the registry, the persistent disk and NGINX in front still to come
    (Lectures 19–22); your project's architecture; five test-yourself questions.

The README's and the slides' small slips are pointed out kindly, with the fix: cheese-app-v2's `main`
changed on the recording day, so the simple frontend is on branch `2025` and the course page's
"Tutorial 23/24/25" links land at the top of the README (follow the section names); *Production
images* was dropped from the README while its Dockerfile and nginx template stayed (shown from the
earlier README, as extras); v1's two `cd` paths lack `src/`; v1's `<p>` snippet is an old whole
`<body>` that would drop the page's script (add only the paragraph); `--chat` always asks the same
question (edit the line in `cli.py`); a key Google cannot sign in with fails as a plain 500, not the
Troubleshooting table's "Gemini: 403/404" (read the API's terminal); Compose's "network/volume
already exists" warnings are harmless; the README's `localhost:900` is 9000; the clean-up leaves the
`node_modules` volume and every tagged image (remove them by name); on branch `2025`, `git switch`
needs a `git stash` first, the vector DB reads a second key name, the demo route and routers are
already in the code, and the Gemini model is retired; and where the slides differ from the
repository: the slide's one-file route vs a router under `/api`, `/chat` vs `/api/llm/chats`, the
agent group and MCP service this repository doesn't have, "localhost:9000" inside the container vs
`0.0.0.0`, and "React" meaning React with Vite and React Router today.

## Rebuild

```bash
python -m explainer.build videos/ac215-l18-apis-frontend -q l                          # fast draft
python -m explainer.build videos/ac215-l18-apis-frontend --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l18-apis-frontend --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l18-apis-frontend --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l18-apis-frontend --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes
once, then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy
from the scene renders. The captures can be re-run with `assets/terminal/capture.sh` (see
[`ASSETS.md`](ASSETS.md), "Re-running"); the exercise checks with the scripts in
[`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app tutorials are used
for study with the instructor's permission and quoted at their pinned commits. The lecture's slides
are redrawn in our own pictures, never shown. The browser and the Google Cloud prerequisites are
schematic drawings (tagged `illustration`), never screenshots; the recording used no Google account
or credentials, and every project ID on screen is a placeholder.*
