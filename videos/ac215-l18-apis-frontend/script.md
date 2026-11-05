# AC215 · Lecture 18 — APIs and frontend: one request, four containers, two ways past the browser — narration script & visual plan (v2, 2026-11-05: four review lenses merged, log in `build/review_merge_log.md`)

Audience: an AC215 student who has done L1–L17: images, containers, `-p HOST:CONTAINER`, bind mounts
and `docker-shell.sh` (L2–L4), a Docker network and container names (L4, L10's cheese-app-v0), the
`llm-rag` chunk → embed → Chroma pipeline (L5), the cheese CNN (L13), the `ml-workflow.json` key in
`secrets/` (L15) and a GCP project with the Vertex AI API on (L1, L15). They have seen Lecture 18
(both decks, "APIs" and "Frontend"). New to them: uvicorn (the server) vs FastAPI (the app),
`api.service:app`, `--host 0.0.0.0`, `--reload`, a function becoming a URL (query string, 422, 307,
`/docs`), static files from `http-server`, routers and prefixes, liveness vs readiness probes, chats
kept as files behind an `X-Session-ID`, a single-page app with Vite and React Router, the dev-server
proxy and one origin, the nginx production image, Docker Compose, and CORS with its preflight. They
watch with clones of `dlops-io/cheese-app-v1` and `dlops-io/cheese-app-v2` open, Docker running and
about 10 GB free, pausing to run every step. **Everything runs on the laptop**; the only cloud calls
are Gemini and the embedding model on Vertex AI, with the viewer's own key (GOLD tags where they
happen). Nothing in this lecture creates a billable cloud resource.

Goal (BRIEF "Audience and goal"): after the video they can trace one request the lecture's way, hop
by hop (browser → published port → container port → uvicorn → the FastAPI function → JSON back) and
say what changes in production (only the outside); start FastAPI under uvicorn in a container and
explain `api.service:app`, `--host 0.0.0.0`, `--reload`, and why `/square_root` answers 307 and
`?x=abc` answers 422; serve static files with `http-server` and say what runs where; bring up v2's
containers on `cheese-app-network`, load 14,356 chunks into Chroma, check `/healthz` vs `/readyz`,
find the routes in `/api/docs` and run `pytest`; explain how a chat survives without memory; run the
React app on 3000 and explain why the browser never sees 9000 (Vite in dev, nginx in production
forward `/api` by container name on one origin, so `main`'s API needs no CORS); switch to branch
`2025`, run last year's simple frontend, and spot a CORS preflight and a 307 in the API log; bring
everything up with `docker compose up --build`, and clean up, including what `prune` leaves behind.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest or the slides and the captures disagree, the captures win, and the
video says so kindly. **Which README** (BRIEF table, ASSETS "Which commit"): v1 = `README.md` @
`ce03a10` (`main`); v2 = `README.md` @ **`447b5c3`** (`main` as a student clones it on 2026-11-05,
after two moves that morning) for the Environment Setup, Vector DB, Backend APIs, React Frontend
Setup, Setup & Run and Docker Cleanup sections; "Production images" from `e98fa55`'s README
(lines 197–215, all `extra`, S12); "Tutorial (24): Simple Frontend App" and the 2025 vector DB and
API from branch **`2025` = `14f2a14`** (S14, S15), the commit `units.json` and the published exam
edition `../ac215-l16-exam/` name. Nothing in a terminal panel is typed by hand: every output line
below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown,
  no raw symbols (`/`, `=`, `%`, `&`, `$`, `→`, `_` in a word the voice reads); commands, flags and
  paths are on screen and said in words ("change into src, vector db", "slash api", "x equals 2",
  "Control C", "sh docker-shell.sh", "npm run dev", "docker compose up with build"). File names
  are said "service dot py", "index dot html", "main dot js", "main dot jsx", "App dot jsx", "api
  dot js", "vite dot config dot js", "chat dot py", "cli dot py", "newsletters dot html", "chat dot
  html"; `docker-shell.sh`, `pytest`, `0.0.0.0`, `127.0.0.1` are written as such (lexicon
  entries, see "Notes"); `14,356` is written as such and needs no entry; `api_server` is said "API server" and `uvicorn_server` "uvicorn server". Container names are said in words ("cheese app API
  service", "cheese app network", "cheese app vector db"). Numbers are digits; never a "!" after a
  digit; no `'s` after a digit (the voice drops it: "the version 1 page", not "Version 1's page"); no spoken decimals (5.0 is "five point zero", 94.8 MB is "about 95", 4.583 GB "about four
  and a half gigabytes", 58.22 "58 percent"). Tool versions sit on screen with "at the time of
  recording" and are not spoken; Python 3.12 / 3.13 are named where the banner shows them.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name ("Then uvicorn …",
  "Run pytest …", never "uvicorn …" at a sentence start). No `'s` on a word with a lexicon entry or
  candidate (uvicorn, nginx, Vite, Chroma, FastAPI, CORS). No bare "a" right before a lexicon entry or
  candidate ("the 503", "status 422"). No homographs: never "read", "live", "lives", "close",
  "lead", "tear", "minute(s)", "content", "record" (so "stay" for a chat between messages, "600
  seconds" for `max-age=600`, "the middle block" for B36's Content). No abbreviations with inner
  dots. American spelling on screen and in SAY ("gray", "behavior"; colour constants stay GREY).
    The main clause comes first so the Chinese subtitles keep English clause order.
- **Spoken step numbers follow the README's own numbered lists**, not the tracker's dots: the BRIEF's
  trackers split each README "cd + docker-shell" step into two dots (and T23 runs two README sections),
  so the SAY says "Step 1: change into …, and run docker-shell.sh", "Step 2: …" as the README numbers
  them, and README headings without numbers are said by name ("Demo route:", "API docs:", "Review the
  code:", "Review the app:"). For T23 the SAY says "Vector DB steps 1 to 3" and "Backend steps 1, 2
  and 4". The tracker keeps its BRIEF step titles, which name the action, so both read true.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on
  an empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). Five in the video,
  BRIEF's table and numbers, Conny's 2026-10-21 density decision: P1 S03 (8 s), P2 S07 (8 s), P3 S11
  (8 s), **P5 S12 (6 s)**, P4 S15 (8 s) (P5 plays before P4; the cards carry no number). The SAY
  before each card speaks the question; the answer is the next SAY. Nothing during the timer shows
  the answer.
- `TERM(id: lines)`: a terminal beat. `id` is the capture `assets/terminal/laptop/<id>-*.txt` (`a03`
  = `a03-docker-shell-api.txt`, `a20b`, `c01b`); the five `f04-*` files are named in full
  (`f04-docker-compose-up`, `f04-curl-3000`, `f04-curl-api-docs`, `f04-x-compose-ps`,
  `f04-x-readme-url`). The scene types the command written just before it in the SHOW line (in
  backticks, exactly as the README spells it; extras exactly as the capture's line 1 spells it,
  folding with ` \`), then prints the listed **file** lines. Line 1 is the `$ …` command: typed,
  never printed; `[exit N]` is never printed. Inside the list: `…` = print one `…` line; `wrap` =
  fold long lines (`Terminal.print(…, wrap=True)`); `from "…"` = print that long line from the
  quoted phrase on, after a `…`; `→ (no output)` = the prompt simply returns. Blank output lines
  are dropped. Heredoc edits (`a05:1–7`, `a23:1–9`, `b27:1–14`) are never typed: they stand for the
  viewer's editor (a GREY chip "your editor"; the README says "open … in your editor"), and the
  terminal types only the capture's `git … diff` line (`a05:8`, `a23:10`, `b27:15`, `b03:2`,
  `f01:2`, extra) and prints the diff. For `b03` and `f01` the `sed` line (line 1) is typed with a
  GREY chip "or edit the file" (extra).
- Prompts (constructed; captures hold only the command): `student@laptop:~$` (the folder that holds
  both clones), `student@laptop:~/cheese-app-v1/src/api-service$`,
  `…:~/cheese-app-v1/src/frontend-simple$`, `student@laptop:~/cheese-app-v2$`,
  `…:~/cheese-app-v2/src/vector-db$`, `…/src/api-service$`, `…/src/frontend-react$`, `…/src$`,
  `…/src/frontend-simple$`. Inside containers the prompt is the capture's own line (`app@<id>:/app$`,
  `<id>:/app#`, `node@<id>:/app$`), printed from the file, never typed. Terminal titles: `laptop`
  (the main terminal of each section), `laptop · second tab` (curl checks while a server runs in the
  foreground, as the README's "open … in your browser"), `laptop · new terminal` where the README
  says "in a new terminal".
- **Browser steps** ("open http://localhost:… in your browser"): a schematic GREY browser window
  (`browser_window(url, rows)`, tag `illustration`, no screenshot, no logo) with its address bar in
  PINK and only what the captured HTML or JSON says the page holds; the curl capture beside it, typed
  in a `second tab` strip and marked `extra` ("the same request, from a terminal").
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` with the real line numbers,
  header `path · lines a–b`; at most 12 lines on screen. `cheese-app-v2/…` = `447b5c3`;
  `cheese-app-v2-at-14f2a14/…` = branch `2025`; `cheese-app-v2-at-e98fa55/README.md` for
  "Production images". A "README card" is a GREY quote of README text, header `README.md · lines a–b`
  (markdown stripped). `cheese-app-v1/src/frontend-simple/index.html:57`, the same paragraph at
  `14f2a14`, and `cheese-app-v2/src/vector-db/cli.py:76` name the instructor: they are never in a
  panel's line range (if one ever is, it shows `‹instructor›`).
- `EXPECTED(expected/<file>: lines)` / `RECORDED(…)`: a GREY-outlined panel quoting those lines of
  `assets/terminal/expected/<file>` (the `#` header lines dropped), tagged `expected · <source>` or
  `recorded · <source>` (e.g. "docs/contract.md:31–44", "README:223–233").
- `TRACKER [k] n`: the `ReadmeTracker`, top-left in every walkthrough scene, for README section `k`
  at step n. `TRACKER [k] n · extra` = same step, caption " · extra" while a command the README does
  not have is on screen. Titles are the README's own headings (never an anchor); the `e98fa55` and
  `2025` trackers carry their commit in the caption. Step titles ≤ 3 words (BRIEF table):
  - [SE] "README › Setup Environments · Environment Setup" (v1:14–35, v2:20–50), 4: 1 Clone v1 ·
    2 Clone v2 · 3 Local folders · 4 Project ID.
  - [A] "README › Backend API Container" (v1:37–67), 8: 1 Go to folder · 2 Build & run · 3 Start
    uvicorn · 4 Test root · 5 Add route · 6 Try route · 7 Add params · 8 View docs.
  - [F] "README › Frontend App (Simple) Container" (v1:71–97), 6: 1 Go to folder · 2 Build & run ·
    3 http-server · 4 Test 8080 · 5 Edit index · 6 Refresh page.
  - [C1] "README › Docker Cleanup" (v1:100–106, caption "cheese-app-v1"), 4: 1 Container ls ·
    2 Stop containers · 3 System prune · 4 Image ls.
  - [V] "README › Tutorial: Vector DB for RAG Setup" (v2:52–79), 5: 1 cd vector-db · 2 docker-shell ·
    3 Load database · 4 Try chat · 5 exit.
  - [B] "README › Tutorial: Backend APIs" (v2:81–145), 10: 1 cd api-service · 2 docker-shell ·
    3 api_server · 4 Check probes · 5 Demo route · 6 Try route · 7 API docs · 8 GET newsletters ·
    9 Review code · 10 pytest.
  - [R] "README › Tutorial: React Frontend Setup" (v2:147–190), 7: 1 cd frontend · 2 docker-shell ·
    3 npm run dev · 4 Open 3000 · 5 Review app · 6 Review code · 7 npm run check.
  - [P] "README @ e98fa55 › Production images" (e98fa55:197–215, caption "earlier README · extra"),
    5: 1 Stop dev · 2 docker build · 3 docker run · 4 Open 8080 · 5 Compare sizes.
  - [S] "README › Tutorial: Setup & Run Cheese App" (v2:192–221), 6: 1 Project ID · 2 Stop
    containers · 3 cd src · 4 compose up · 5 Open app · 6 compose down.
  - [C2] "README › Docker Cleanup" (v2:235–246), 2: 1 compose down · 2 system prune.
  - [T23] "README @ branch 2025 › Tutorial (23): Vector DB · Backend APIs" (2025:40–95, caption
    "branch 2025 · 14f2a14"), 7: 1 cd vector-db · 2 docker-shell · 3 Load database · 4 cd
    api-service · 5 docker-shell · 6 uvicorn_server · 7 Verify 9000.
  - [T24] "README @ branch 2025 › Tutorial (24): Simple Frontend App" (2025:147–183, same caption),
    6: 1 cd frontend · 2 docker-shell · 3 http-server · 4 Home page · 5 Newsletters · 6 Chat.
  S01, S02's first half, S10's first half (until `cd src/frontend-react`) and S16 have no tracker.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says "extra" the first time each kind appears. `extra · our spelling` on `p01`, `p02`,
  `p05` (the READMEs say "Clone or download" and show a tree, not a command).
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README
  section); the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every browser window, the prerequisites card, the
  lecture redrawings that show cloud machinery; `expected · docs/contract.md` (S09), `recorded ·
  README:223–233` (troubleshooting rows, S09, S11); `erratum` on every README or slide slip (the SAY
  says "a small slip" or "a small note", never "erratum"); `at the time of recording` beside every
  version on first show; GOLD `cost_tag()` where a call with the viewer's own key would be billed:
  S06 (`--chat`: embedding + Gemini), S09 (Ask, Cheese books), S11 (Chat review); a GOLD-outlined
  "disk" chip in S07 (the 4.2 GB API image), S14 (branch 2025 builds its own images) and S16; the S01
  chip "about 10 GB free · more for branch 2025". No price
  anywhere.
- `LECTURE 18 · a–b (Deck)` in a SHOW line: from that block on, the GREY `lecture_ref(18, "a–b
  (Deck)")` tag (`explainer.devops`) sits top right ("Lecture 18 · slides a–b (APIs)"; "slide" for
  one) **only while that slide's picture or idea is on screen**: the SHOW that changes the picture
  removes it ("LECTURE off"). Deck names as the student sees them on the PDFs: "APIs" and
  "Frontend"; the A/B notation of SLIDES.md never appears. Every lecture picture is our own
  redrawing in series colours with the slide's structure and terms: no slide image, logo, smiley or
  screenshot; the lecture's colours (red request arrows, the gold API box, A44's six coloured
  groups) are not copied.
- **The sandbox framing** (BRIEF "Running example", load-bearing): said once, in S06 (block 3).
  Afterwards every Google error is the lesson, "with your key, …" is the only way a Gemini answer is
  mentioned, and no answer text appears anywhere (none was captured or documented).

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| the laptop, the browser, its tab and address bar, the host's ports and DNS, `secrets/` and `persistent-folder/` on the host | GREY |
| the cloud: Vertex AI (Gemini, `text-embedding-004`), the lecture's GCP boundary, cluster and Artifact Registry in the blueprint | BLUE |
| containers and images: `cheese-app-api-service`, `cheese-app-vector-db`, `cheese-app-vector-db-cli`, `cheese-app-frontend-react` (dev and `:prod`), `cheese-app-frontend-simple`, nginx's container | TEAL |
| shared, not yours: the default bridge network, Docker's build cache, the shared `node_modules` volume, the browser's built-in rules (same-origin policy), port numbers everyone collides on (8000, 8080, 9000) | ORANGE |
| what the project owns and pins: `pyproject.toml`/`uv.lock`, `package.json`/`package-lock.json`, the chat JSON files, Chroma's collection `recursive-split-collection`, `cheese-app-network` (the app's private LAN), `docs/contract.md`, pytest's green `26 passed` | GREEN |
| tools: uvicorn, FastAPI, `http-server`, Vite, nginx, Docker Compose, pytest, npm | PURPLE |
| errors and "don't": `No such file or directory`, 422, 404, 405, 500, 502, 503, `RefreshError`, `[emerg] host not found`, `git switch` refused, the README slips, a secret inside the repo | RED |
| your turn, the README tracker, the hop being traced now, the ponder timer | YELLOW |
| money: Gemini and embedding calls on Vertex AI (with your own key), disk (~10 GB; the 4.2 GB API image) | GOLD |
| routes and addresses: URLs, paths, query strings, `-p` doors, request/response arrows, the numbered hops, origins, headers (`X-Session-ID`, `Origin`, `access-control-*`), the proxy hop | PINK |
| the past and the future (L5's RAG, L13's CNN, L15's key; L19–L22's cluster, NGINX, Artifact Registry) | GREY, dashed |

A44's route groups are WHITE-outlined chips (GREEN when this repo has the router, GREY dashed when
not); A30–A33's MCP service is GREY dashed (not in this repo).

Running example
- **The laptop** (`laptop/`: a fresh, empty Docker 29.8.2 engine standing in for Docker Desktop,
  Compose v5.6.0, linux/amd64, git 2.54.0, user `student`): `cheese-app-v1/`, `cheese-app-v2/`,
  `secrets/`, `persistent-folder/` side by side in one parent folder (`p06`); that layout is what
  `../../../secrets` resolves to. On screen once (S03, GREY chip, not spoken): "your prompt shows
  your own user; on a Mac the banner says aarch64".
- **The key, honestly**: `secrets/ml-workflow.json` is a well-formed service-account file around a
  throwaway key for no account (`capture-only/placeholder-key.json` is its shape; never shown as a
  panel). Said once (S06). The successful reply's **shape** is `expected/02-chat-contract.txt`,
  tagged `expected`.
- **Placeholders**: project id `your-gcp-project` (`b03`, `f01`, `c04`); session id
  `00000000-0000-4000-8000-000000000001` from the curl captures (on screen, never read: "a session
  ID"). No real-looking key, token or project id anywhere.
- **Versions** (on screen with "at the time of recording", not spoken): Docker 29.8.2, Compose
  v5.6.0; v1: Python 3.12.16, uv 0.13.7, http-server 14.1.1; `main`: Python 3.13.18, uv 0.13.6,
  Chroma 1.5.9, pytest 9.2.0, Node v24.22.1, npm 11.19.1, Vite 8.3.5, nginx 1.31.8; 2025: Python
  3.12.16, `chromadb/chroma:latest` (image created 2026-05-05). Image sizes: API 4.2 GB, React dev
  331 MB, React prod 94.8 MB.
- **Crops**: the branch name in `p04`, `b01`, `c01b`, `c31` (a staff member's name) is cropped or
  masked (`p04`: show lines 2–4 only; `c01b`/`c31`: line 2 / line 4 cut after `447b5c3`, the rest
  "…"); dates, PIDs, container ids, network ids, hashed asset names and UUIDs are never read aloud;
  long build logs show first lines, `…`, last lines.

Length and parts: narration **4,292** words (`python -m explainer.script`, which counts SAY words;
its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm) that is
≈24.7 min of narration, ≈31–33 min with typing, build and load outputs, browser drawings and five
ponder timers. Per scene (BRIEF target · ±15 % band):

| scene | words (BRIEF · band) | scene | words (BRIEF · band) |
| --- | --- | --- | --- |
| S01 Hook | 214 (220 · 187–253) | S10 ReactShell | 308 (310 · 264–357) |
| S02 Blueprint | 248 (250 · 213–288) | S11 OneOrigin | 290 (290 · 247–334) |
| S03 ServerAndApp | 322 (290 · 247–334) | S12 NginxImage | 280 (260 · 221–299) |
| S04 FunctionToUrl | 227 (250 · 213–288) | S13 ComposeUp | 218 (220 · 187–253) |
| S05 StaticPages | 237 (270 · 230–311) | S14 Branch2025 | 264 (290 · 247–334) |
| S06 VectorDb | 284 (270 · 230–311) | S15 CorsPreflight | 314 (310 · 264–357) |
| S07 AliveAndReady | 273 (260 · 221–299) | S16 Recap | 248 (220 · 187–253) |
| S08 ScreensToRoutes | 265 (280 · 238–322) | | |
| S09 ChatIsAFile | 300 (270 · 230–311) | | |
| **part 1** | **2,370** (2,360) | **part 2** | **1,922** (1,900) |

Every scene is inside its band. Tight: S16 (248, ceiling 253), S03 (322, ceiling 334) and the total
(4,292 of the series' 4,300 ceiling), so any later addition names its cut in the same scene; re-run the counter after any
edit.
Part 1 = S01–S09 (the API, the lecture's APIs deck; ends on `26 passed` and the parked question
"the browser will talk to port 3000: how does that reach 9000?"). Part 2 = S10–S16 (the frontend,
the Frontend deck; ends on the last test-yourself card, then an empty frame). The cut is the README's
own seam, "Keep this container running." (v2:145).

Notes for scene authors
- Shared code (`scenes/common.py`, started from L14's/L13's): tracker factories `tracker_se`,
  `tracker_a`, `tracker_f`, `tracker_c1`, `tracker_v`, `tracker_b`, `tracker_r`, `tracker_p`,
  `tracker_s`, `tracker_c2`, `tracker_t23`, `tracker_t24` with the step lists above and the commit
  caption variants; prompts (`P_LAPTOP`, `P_V1_API`, `P_V1_FRONT`, `P_V2`, `P_V2_VDB`, `P_V2_API`,
  `P_V2_REACT`, `P_V2_SRC`, `P_V2_SIMPLE`); tags `your_turn`, `extra_tag` (+ `our spelling`,
  `branch 2025` variants), `illustration_tag`, `expected_tag(source)`, `recorded_tag(source)`,
  `erratum_tag`, `cost_tag(text)` (GOLD), `lecture_ref`; `browser_window(url, rows)`; set pieces
  `RequestTrace` (V1), `ArchitectureMap` (V2), `ServerAppDiagram` (V3), `RouteTree` (V4),
  `TwoLocalhosts` (V5), `ProbeLamps` (V6), `ChatFile` (V7), `OneShell` (V8). Never reuse a scene
  class name for a helper.
- **V1 + V5, one layout** (S11, S12, S15, S16): from S06 on, V1's laptop interior *is* V5 (same box
  positions, GREEN cable, phone book); those scenes only add V1's browser, divider and arrows. Define
  it once in `common.py`.
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the output
  body, so pick index = file line − 1. Assert the picked text for every highlighted line.
- **V1 `RequestTrace`, one layout for the whole video** (S01, S03, S05, S11, S12, S15): GREY browser
  window left (address bar), dashed vertical divider, GREY laptop outline right with TEAL container
  boxes; PINK arrows with YELLOW numbered circles, captions in the series' words: "1 request" →
  "2 the laptop forwards it to the published port" → "3 the port is mapped into the container" →
  "4 the function runs" → "5 the response comes back" → "6 the page shows it". Optional hop **0**
  (an `OPTIONS` scout, S15) and hop **3½** (a PURPLE courier box inside the frontend container,
  labelled "?" in S01, "Vite" in S11, "nginx" in S12). A 307 is a small U-turn on arrow 1.
- **BRIEF corrections found while scripting** (captures win):
  - `d02:25–27`: the React dev banner says `Installing dependencies...` then **`up to date in
    571ms`** (the named volume already held the packages in the kept run), not "added 257
    packages" (BRIEF S10, ASSETS d02). The SAY says your first run installs everything
    (`docker-entrypoint.dev.sh:8` "a full install only the first time"). `d02:3`: the dev image
    built in 0.4 s (cached base).
  - `e03:32`: `docker system prune` reclaimed **4.583GB** (and deleted `cheese-app-network`,
    `e03:9–10`), not 5.328GB (BRIEF S13).
  - `d12:27`: `✓ built in 470ms` (as BRIEF says; ASSETS' 767ms is stale). Not spoken.
  - `f04-docker-compose-up` Ctrl-C lines are **142–151** (BRIEF: 143–151).
  - v1's `service.py` already carries `CORSMiddleware(allow_origins=["*"])` (`service.py:7–14`), like
    the 2025 API; only `main` dropped it. S03 says "we come back to this at the very end".
  - The 2025 chat page posts to `/llm/chats/` and the router's path is `/llm/chats`: the 307 goes
    from the slash to no slash (`c11:82`, `c28:2–6`); for newsletters it goes the other way
    (`c11:79–80`). S15 says "the paths differ by one slash", not which way.
  - `c05`/`c10`/`c20` are typed from the folder that holds the clones (the 2025 README's starting
    point, `cd cheese-app-v2/src/…`); `c01`–`c04` ran inside `cheese-app-v2/`. S14 shows a GREY chip
    "from the folder above cheese-app-v2" (no `cd ..` capture exists; not typed).
  - `c06` exits the vector-db shell after the load (`c06:198`); the 2025 README says "keep this
    container running", and Chroma does keep running (Compose `run`), as `c07` shows.
  - `b21:613` is the API's `^C` (S12 stops the API before `e01`); the API's last requests before it
    are `b21:610–612`.
- Lexicon (merge stage, 2026-11-05): added under "# AC215 L18" `Vite`/`vite` ("veet"),
  `healthz`/`Healthz` ("health zee"), `readyz`/`Readyz` ("ready zee"), `"5173"` ("fifty-one
  seventy-three") and the phrase key `"cli dot py"` ("C-L-I dot pie"); no other video's SAY uses
  them. Left alone on purpose (spoken review #20): uvicorn (L09, L10, L16 shipped its current sound),
  nginx/NGINX, FastAPI, CORS, JSON, `422`/`307`/`502` (published videos say them in full), `src`
  ("S R C", as in ten other scripts, not "source"), `2025`, `14,356`. Original heads-up, kept for
  reference (script stage; check phonemes with `explainer/voice.py`, phrase keys where another video
  uses the bare word): uvicorn
  ("you-vee-corn"), FastAPI, Vite ("veet"), nginx and NGINX ("engine-x"), Chroma, `http-server`,
  `uvicorn_server` (said "uvicorn server"), `docker-shell.sh` (exists), `healthz` /
  `readyz` ("health-z", "ready-z"), `"0.0.0.0"` and `127.0.0.1` (exist), `"9000"`, `"3000"`,
  `"8000"`, `"5173"` ("fifty-one seventy-three"), `"8080"` (exists), CORS ("cores"), preflight, JSX
  ("J S X"), UUID, axios, `14,356`, `"307"`, `"422"`, `"500"`, `"502"`, `"503"` (exists), `"404"`,
  `"405"` (exist), parmigiano and Tolminc (exist), StatReload, WatchFiles, Formaggio, Gemini,
  Swagger (not spoken), `AC215` (exists), "llm", "llm cnn", "llm rag" (spelled "L L M", "L L M C N
  N", "L L M rag"), "ml workflow" ("M L workflow"), "src" ("source"), "dist" (not spoken), "GCP".
- Subtitle display for the i18n stage (`en_display`): sh docker-shell.sh → `sh docker-shell.sh`;
  slash api → `/api`; slash docs → `/docs`; api dot service colon app → `api.service:app`; host
  0.0.0.0 → `--host 0.0.0.0`; reload → `--reload`; square root → `square_root`; x equals 2 and y
  equals 10 → `x=2&y=10`; five point zero → `5.0`; service dot py / index dot html / main dot js /
  main dot jsx / App dot jsx / api dot js / vite dot config dot js / chat dot py / cli dot py /
  newsletters dot html / chat dot html → the file names; cheese app network → `cheese-app-network`;
  cheese app API service → `cheese-app-api-service`; cheese app vector db → `cheese-app-vector-db`;
  change into src, vector db → `cd src/vector-db` (and the other `cd` lines); healthz / readyz →
  `/healthz` / `/readyz`; llm, llm cnn, llm rag → `llm`, `llm-cnn`, `llm-rag`; Control C → `Ctrl+C`;
  docker compose up with build → `docker compose up --build`; access control allow origin, star →
  `access-control-allow-origin: *`; ml workflow dot json → `ml-workflow.json`; llm service account
  dot json → `llm-service-account.json`; uvicorn server → `uvicorn_server`; API server →
    `api_server`; X session ID → `X-Session-ID`; localhost 9000 / 3000 / 8080 → `localhost:9000` …;
  slash api, square root → `/api/square_root`; slash api, newsletters → `/api/newsletters`; slash api,
  docs → `/api/docs`; slash api, llm, chats → `/api/llm/chats`; slash chat → `/chat`; get status →
  `get_status`; settings dot py → `settings.py`; change into src, api service / frontend react /
  cheese app v2, src, frontend simple → `cd src/api-service` / `cd src/frontend-react` /
  `cd cheese-app-v2/src/frontend-simple`; node modules → `node_modules`; tagged prod → `:prod`; x
  equals 3 and y equals 4 → `x=3&y=4`; Git switch 2025 → `git switch 2025`; docker ps → `docker ps`;
  plain def → plain `def`; type y for yes → type `y`; the quoted log/slide phrases in quotes
  ("Application startup complete", "how is cheese made", "use Gemini to generate text", "well, not
  really, we need to build it", "invalid grant, account not found", "host not found in upstream",
  "CNN model is loading"). In zh all of these stay English (glossary rule). Metaphors for the zh
  glossary, rendered the same way every time: "permission slip" → 许可条; "the courier" / "three and a
  half" → 信使 / 第 3.5 步; "phone book" → 通讯录 (DNS); "the leaves of this tree" → 这棵树的叶子;
  "stamps out" → 批量生成; "step zero, the preflight" → 第 0 步：预检.
- Never: the instructor's name (`‹instructor›`), a slide image or long slide text, a Google logo or
  console screenshot, a real-looking key or project id, a Gemini or RAG **answer**, Next.js or MCP
  for anything this repo runs, "the frontend container calls the API" in the 2025 stack (the
  browser does), "the browser calls 9000" on `main` (it calls 3000), CORS as a server-side block or
  an API security feature, `e98fa55`'s Production images or branch `2025` as today's README steps,
  `--host 127.0.0.1` as advice, `npm install` on the host, "parmigiano" as a bug in the app.

---

## S01 · Who answered on port 3000? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. A full-width terminal slides in, title `laptop`, prompt
`student@laptop:~$`. It types `curl -s -i 'http://localhost:3000/api/newsletters?limit=2' | sed -n '1,8p'`
(extra; tag `extra`) → TERM(d04: 2, 5–7). On "port 3000" the `3000` in the typed URL glows PINK;
on "two newsletters" line 2 `HTTP/1.1 200 OK` ticks GREEN; on "who answered" line 5
`server: uvicorn` turns YELLOW and a small PURPLE chip "the API's server · port 9000" points at it.
SAY: Here is a request to port 3000, where this app's frontend runs. It asks for two newsletters and gets them. But look who answered: uvicorn, the API's server, and the API listens on port 9000.

SHOW: The terminal shrinks to the top half. Below it a second strip, title `laptop · branch 2025`
(tag `extra · branch 2025`), types the line 1 of `c25` (folds) → TERM(c25: 2–7, wrap); both
`access-control-allow-origin: *` lines (4, 7) YELLOW; a GREY chip "last year's version of the
same app".
SAY: Last year's version of this app worked differently. Its page called port 9000 directly, and every answer carried a permission slip: access control allow origin, star.

SHOW: A third strip (title `laptop`, tag `extra`) types line 1 of `b43` (folds) → TERM(b43: 2–3)
only (the GET, with no `access-control-*` line; the 405 half of the capture is not shown). A GREY
ghost line "access-control-allow-origin" appears where the header would be and is struck through
RED. The three strips fade; a YELLOW card settles in the centre: "The page talks to 3000. The
answer comes from 9000. Who carried it?"
SAY: This year's API sends no such slip at all. So who carried the request from 3000 to 9000, and why did last year's page need permission?

SHOW: LECTURE 18 · 27 (Frontend). The card shrinks to a strip at the top. **V1 `RequestTrace`** at
full size: the GREY browser window (address `localhost:3000/chat`), the dashed divider, the GREY
laptop with TEAL boxes `cheese-app-frontend-react · 3000`, `cheese-app-api-service · 9000` and a
small `cheese-app-vector-db · 8000`; outside the laptop a BLUE dashed cloud "Vertex AI · Gemini".
The six YELLOW circles light in order along PINK arrows, each caption writing on with its phrase
(request → forwards → mapped → function runs → response → shows it). Then between circles 3 and 4
a small PURPLE box with "?" pops up inside the frontend container, circle "3½".
SAY: The lecture draws one chat message as six numbered steps: request, forward, map into a container, run a function, respond, show it. We add one step it never draws: three and a half, the courier.

SHOW: LECTURE 18 · 19–21 (APIs). The camera pulls back from the laptop: **V2 `ArchitectureMap`**
appears around it as a GREY dashed silhouette with only the right cluster box drawn (four TEAL boxes
NGINX, Cheese App, API Service, Vector DB); S02 fills the silhouette layer by layer. The three PINK port
labels `3000`, `9000`, `8000` fly from V1's boxes onto the cluster's edges. A GREEN chip "App is
ready!" pops over the cluster, then a RED line strikes it and a GREY caption writes under it: "Well
not really, we need to build it" (no smiley).
SAY: Zoom out, and this is the lecture's blueprint for the whole app, with the same three ports. The lecture calls the app ready, then admits: well, not really, we need to build it. Today we build the right-hand side, on your laptop.

SHOW: LECTURE off. The map fades. Four GREY chips line up, one per phrase: "cheese-app-v1 +
cheese-app-v2", "Docker running", "about 10 GB free · more for branch 2025", and a GOLD-outlined "your Google key · chat
answers only".
SAY: To follow along, clone both repositories, keep Docker running, and free about 10 gigabytes. Your Google key matters only for the chat answers.

SHOW: The chips fade. Top-left a sample YELLOW `ReadmeTracker` ("README › Tutorial: Backend APIs ·
step 1 of 10"); in the middle a small sample code panel header `api/service.py · lines 43–56`; beside
a sample command a YELLOW `▶ your turn` pulses, each on its phrase. Everything fades; empty frame.
SAY: The tracker in the corner names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it.

---

## S02 · The blueprint, and your folders — `s02_blueprint.py` · `Blueprint`

SHOW: No tracker. LECTURE 18 · 4–5 (APIs). A4 redrawn small: a wide GREY arrow with "POC",
"Prototype", "MVP" and dashed boundaries; under it the bar "Build Cheese App" with a dashed YELLOW
box. It slides up; A5's board builds: left panel "ML pipeline" with five small tiles (Data Collector,
Data Processor, Model Training, Model Deploy, Vector DB) and a GREEN tick; right panel "App Dev" with two
WHITE-outlined tiles "Backend API" and "Frontend", pulsing YELLOW on "the app".
SAY: First, where this lecture sits. The course project has its machine learning pipeline; what is still missing is the app: a backend API and a frontend.

SHOW: LECTURE 18 · 7–13 (APIs). The board clears. **V2** builds layer by layer, one layer per
phrase: a title chip "technical architecture · the system's blueprint"; two GREY bands
"developers · data scientists" (top left) and "users" (top right), each with a browser icon;
GREY-outlined boxes "GitHub" and "Colab notebooks" (no logos); a BLUE "Vertex AI" panel with a
small "Gemini" box; the BLUE dotted GCP boundary around Vertex AI and a GREY "App" box. On "protocol and port" PINK
labels write onto the arrows: "HTTPS 443" (browser ↔ Colab, browser ↔ Vertex AI), "HTTP/HTTPS 80"
(users ↔ app).
SAY: The lecture draws the system as a technical architecture, the blueprint, one layer at a time. Developers, users, GitHub and Colab sit outside the cloud, Vertex AI inside, and every arrow is labeled with its protocol and port.

SHOW: LECTURE 18 · 14–19 (APIs). The next layers, ~2 s each: a BLUE "GCS bucket · data & models";
a BLUE "Artifact Registry" with image rows; a BLUE "persistent disk" joined by "NFS"; the right box
"single compute instance / Kubernetes cluster" fills with four TEAL boxes: "NGINX" on top, "Cheese
App" (PINK "HTTP 3000" into NGINX), "API Service" ("HTTP 9000"), "Vector DB" ("HTTP 8000" to the
API).
SAY: Then come a bucket, a registry of images and a persistent disk. On the right sits a cluster: NGINX in front, the app on 3000, the API on 9000, the vector database on 8000.

SHOW: LECTURE off. The cluster box lifts out of the BLUE boundary and slides down into a GREY laptop
outline at the bottom right; its four boxes keep their ports; the rest of the map dims to GREY
dashed. A one-line GREY chip under it: "the same building blocks have AWS and Azure names (slide
22)".
SAY: Today, that whole right-hand side runs on your laptop.

SHOW: LECTURE 18 · 43 (APIs). The laptop shrinks left. A43's rule redrawn on the viewer's real tree
(TERM(p06: 2–4, 7–8, 11, 17–18, 24–31) as a tidy tree, not a terminal; v1's seven `.gitkeep`-only
folders collapse into one GREY chip "+ 7 empty folders", `frontend-simple` (11) stays visible):
`cheese-app-v1/` and `cheese-app-v2/` each with a GREEN "Git root" bracket and `src/` holding one
folder per service;
`secrets/` and `persistent-folder/` beside them, outside both brackets, with a GREY label "secrets
outside the Git folder". A small GREY card "v1 keeps empty folders for the slide's services · v2 holds only
the three it runs" (no `erratum` tag).
SAY: The lecture's folder rule: one Git folder per app, one folder per service under src, and secrets outside the Git folder. Version 1 even keeps empty folders for the services it does not run; version 2 holds only its three.

SHOW: LECTURE off. TRACKER [SE] 1. Full-width terminal `laptop`, prompt `student@laptop:~$`. It
types `git clone https://github.com/dlops-io/cheese-app-v1.git` (tag `extra · our spelling`) →
TERM(p01: 2); TRACKER [SE] 2: `git clone https://github.com/dlops-io/cheese-app-v2.git` →
TERM(p02: 2). A README card (`README.md · line 18`): "Clone or download from here". `▶ your turn`.
SAY: Steps 1 and 2: clone both repositories. The READMEs say clone or download; git clone is our spelling. Pause and clone them.

SHOW: TRACKER [SE] 3. It types `mkdir -p secrets persistent-folder` (tag `extra · our spelling`) →
TERM(p05: → (no output)). The tree from block 5 returns small at the right; `secrets/` and
`persistent-folder/` glow GREY, owner chip "student" on each (TERM(p06: 34, 39) beside them,
the owner columns YELLOW); a GREY ghost "root" owner chip appears and is struck RED: "on Linux, Docker would
create them as root". `ml-workflow.json` slides into `secrets/` (GREY, no content shown).
SAY: Step 3: next to the clones, create secrets and persistent folder yourself. Left to Docker on Linux, they would belong to root, and the container could not write there. Your ml workflow key goes into secrets.

SHOW: TRACKER [SE] 3 · extra. The strip types line 1 of `p04` (extra; folds) → TERM(p04: 2–4)
(the branch lines below are not shown). `447b5c3` on lines 2 and 4 YELLOW, `refs/heads/2025` line 3
PINK (hashes not read; no timeline chips). A GREY folder icon `frontend-simple` drops off `main` and lands on a branch
labelled `2025`. Fade; empty frame.
SAY: One thing changed on the day we recorded: the main branch of version 2 moved twice. We follow main as you clone it today. The simple frontend the lecture teaches now sits on a branch called 2025, which we visit at the end.

---

## S03 · v1: a server, an app, a port — `s03_server.py` · `ServerAndApp`

SHOW: No tracker yet. LECTURE 18 · 25–26 (APIs). A25 redrawn: a GREY laptop left, a GREY server
right, a loop of two PINK arrows "HTTP request" (top) and "HTTP response" (bottom); an envelope
travels the loop once. On "a port", the server grows four small doors labelled `22`, `80`, `443`
(lecture) and, in YELLOW, the tutorial's `9000`, `8080`, `3000`, `8000`.
SAY: A browser sends a request; a server sends a response. A port picks which program gets it: public sites leave the default 80 and 443 out of the address; ours show the port.

SHOW: LECTURE 18 · 27–28 (APIs). The loop shrinks. A27's ladder as one chip that Transforms during
the first sentence: "API" → "Web API (over HTTP)" → "REST API (HTTP methods: GET, POST, PUT, DELETE)"
→ "FastAPI" (PURPLE). On "Every client", A28's picture: three GREY client chips (browser, mobile, edge) whose PINK "REST / JSON" lines merge
into one line that crosses a dashed divider to one TEAL "API" box, which fans out to "stores",
"databases", "models".
SAY: In this course, an API means a REST API, built with FastAPI. Every client talks to that one API, and only the API talks to the stores.

SHOW: LECTURE off. TRACKER [A] 1 (tracker appears: "README › Backend API Container", 8 dots).
Full-width terminal `laptop`, prompt `student@laptop:~$`. A README card (`README.md · line 41`):
"go to the location where cheese-app-v1/api-service". It types `cd cheese-app-v1/api-service` →
TERM(a01: 2) RED. TRACKER [A] 1 · extra: it types `cd cheese-app-v1/src/api-service && ls` (extra,
tag `erratum` on the README card: "add src/") → TERM(a02: 2–7).
SAY: Part 1, cheese app version 1. Step 1: go to the API folder; the README's path misses src, so this fails. A small slip: add src.

SHOW: TRACKER [A] 2. The terminal shrinks to a strip; CODE(cheese-app-v1/src/api-service/docker-shell.sh:
13–21) beside it: line 13 (`docker build`) PURPLE; on "removes itself" `--rm` (16) rings GREY; on
"mounts" the three `-v` lines (17–19) GREEN; on "publishes" line 20 `-p 9000:9000` rings PINK and a
small tunnel picture draws: a GREY laptop wall door `9000` piped to a TEAL container door `9000`.
The prompt becomes `student@laptop:~/cheese-app-v1/src/api-service$`; it types `sh docker-shell.sh`.
`▶ your turn`.
SAY: Step 2: sh docker-shell.sh. It builds the image, then starts a container that removes itself on exit, mounts your code, and publishes port 9000 to 9000. Pause and run it.

SHOW: The build finishes as the block starts: TERM(a03: 3, …, 30–37); line 3 `Building 49.9s` GREY, line 32 `Container is running!!!`
GREEN, lines 35–36 with the chip "at the time of recording"; a GREY chip "your prompt shows your
own user · on a Mac: aarch64" (not spoken). Line 38's prompt `app@…:/app$` stays. On "Step 3",
TRACKER [A] 3; at the container prompt it types
`uvicorn api.service:app --host 0.0.0.0 --port 9000 --log-level debug --reload --reload-dir api/ "$@"`
(README:47, folds into two rows). **V3 `ServerAppDiagram`** builds to the right as the terminal
shrinks to a 3-row strip: a TEAL container; inside, a PURPLE box "uvicorn · the server" holding a
PINK socket `:9000`; inside that, a smaller PURPLE card "FastAPI · the app" with an empty route
table.
SAY: Step 3: the README's long uvicorn line. Here, uvicorn is the server: it owns the port and speaks HTTP. FastAPI is the app inside it.

SHOW: The typed `api.service:app` splits into three PINK chips that fly onto the card: "folder
`api/`", "file `service.py`", "variable `app`".
SAY: The phrase api dot service colon app is an address: folder api, file service dot py, variable app.

SHOW: On "every interface" `--host 0.0.0.0` lights. The TEAL container shows two plates: a GREY
"lo · 127.0.0.1" inside, and a GREY "eth0" on the wall where the tunnel ends. The GREEN `0.0.0.0`
badge on the socket draws a line to both; on "where the tunnel arrives" a PINK request walks in
through eth0. On "reload", `--reload --reload-dir api/` lights and a small eye icon watches the
`api/` folder. On "the last part", `"$@"` lights with a GREY chip "extra arguments · none here".
SAY: Host 0.0.0.0 means every interface: the container's own loopback, and its network interface, where the tunnel arrives. Reload restarts the app when a file in api changes; the last part passes on extra arguments.

SHOW: TERM(a03: 39–44); line 40 `Uvicorn running on http://0.0.0.0:9000` PINK, line 41
`Started reloader process [12] using StatReload` PURPLE (PID not highlighted), line 44 GREEN.
SAY: The log agrees: 0.0.0.0, port 9000, a reloader watching api, startup complete.

SHOW: CODE(cheese-app-v1/src/api-service/api/service.py: 5–14) beside V3: line 5 (`app = FastAPI(...)`)
PURPLE; lines 8–14 (`add_middleware(CORSMiddleware, … allow_origins=["*"] …)`) boxed GREY with a
chip "part 2's ending". On "and one route" the panel swaps to CODE(…/service.py: 17–20): lines
18–20 (`@app.get("/")`) YELLOW, and a row "GET / → get_index" writes into V3's route table.
SAY: In service dot py, the app adds CORS middleware, which matters at the very end, and one route: GET slash returns a welcome.

SHOW: TRACKER [A] 4. LECTURE 18 · 34–41 (APIs). **V1** returns (no frontend box): the browser
window at `localhost:9000`, the laptop with one TEAL `cheese-app-api-service` box. The `second tab`
strip types `curl -s -i http://localhost:9000/` (extra: "the same request, from a terminal") →
TERM(a04: 2, 4, 6, 8); `200 OK` GREEN, `server: uvicorn` PURPLE; the browser drawing (tag
`illustration`) shows `{"message":"Welcome to AC215"}`. `▶ your turn`.
SAY: Step 4: open localhost 9000. An extra curl shows the same reply: status 200 from uvicorn, and the welcome. Pause and try it.

SHOW: The six hops animate with this request, captions writing on: 1 the browser asks
`localhost:9000/`; 2 the laptop forwards it to the published port (the PINK door); 3 the port is
mapped into the container (the tunnel); 4 `get_index` runs (V3's route row flashes); 5 the JSON
comes back; 6 the page shows it.
SAY: That is the lecture's trip: forwarded to the published port, mapped into the container, the function runs, and the JSON comes back.

SHOW: Inside the TEAL box the lecture's label "localhost:9000" appears in GREY (tag `erratum`, a
small GREY card "slide 37"), then morphs into "port 9000 of the container · listening on 0.0.0.0".
SAY: One kind note: the slide labels the inside of the container localhost 9000. Take it as port 9000 of the container: uvicorn listens on 0.0.0.0.

SHOW: LECTURE off. V3 alone, both plates kept: the socket's badge flips to `127.0.0.1` and draws
a line to `lo` only; the `eth0` plate stays unconnected. Two dashed PINK arrows, unanswered: one from a small terminal icon inside the container ("curl inside"), one from the
browser through the tunnel. Nothing else moves.
PONDER(8 s, "uvicorn listens on --host 127.0.0.1\ninside the container instead.\ncurl from inside the container: works?\nYour browser on localhost:9000: works?")
SAY: So, a quick test. If uvicorn listened on 127.0.0.1 instead, would a curl from inside the container work? And your browser on localhost 9000?

---

## S04 · A Python function becomes a URL — `s04_route.py` · `FunctionToUrl`

SHOW: TRACKER [A] 4. The card leaves. V3 runs the ponder: the inside arrow reaches the `127.0.0.1`
loopback and gets a GREEN tick; the browser's arrow comes through the tunnel, arrives on the
container's network interface (the GREY "eth0" plate drawn before the ponder), finds no listener and stops RED. The badge
flips back to `0.0.0.0` and the arrow walks in GREEN.
SAY: Inside, yes: the container's own loopback answers. From the browser, no: the forwarded request arrives on the container's network interface, where nothing listens. That is why the README says 0.0.0.0.

SHOW: TRACKER [A] 5. LECTURE 18 · 39–41 (APIs). (No separate A39 card: on "decorated Python
function" the diff's `@app.get` line gets a PURPLE bracket "decorator → route".) A README card (`README.md · lines 52–58`) with the
`square_root` snippet; a GREY chip "your editor" (the heredoc is not typed). The terminal strip
(`second tab`, prompt `…/cheese-app-v1/src/api-service$`) types `git -C ~/cheese-app-v1 diff`
(extra) → TERM(a05: 13–21); the `+` lines GREEN; on "x squared plus y squared" the diff line
`z = x**2 + y**2` YELLOW.
SAY: Step 5: the lecture writes a route as a decorated Python function. Add the README's square root function at the end of service dot py, and save. It returns the square root of x squared plus y squared.

SHOW: The uvicorn terminal (strip above): TERM(a03: 47–54); line 47 `StatReload detected changes in
'api/service.py'. Reloading...` YELLOW. In V3, the PURPLE app card slides out and a fresh one slides
in, its route table now two rows: `GET /` and `GET /square_root/`.
SAY: In the server's terminal, StatReload sees the change and swaps in a fresh app. You restarted nothing.

SHOW: LECTURE off. TRACKER [A] 6. **V4 `RouteTree`**: the URL `http://localhost:9000/square_root/`
splits into PINK tokens (scheme, host, port, path). The path token finds its row in the table; the
signature `square_root(x: float = 1, y: float = 2)` lights, defaults 1 and 2 YELLOW, with the
body row `√(x² + y²)` under it. Strip types
`curl -s http://localhost:9000/square_root/; echo` (extra) → TERM(a06: 2); the browser drawing
shows the same number. `▶ your turn`.
SAY: Step 6: open square root, with its trailing slash. No arguments, so the defaults 1 and 2 apply: the square root of 5. Pause and try it.

SHOW: TRACKER [A] 7. The URL grows `?x=2&y=10`; the query splits into PINK chips `x=2` and `y=10`
that fly into the signature, replacing the defaults; the body row shows `√(2² + 10²)`, then
`10.198039027185569` folds back as JSON.
Strip: `curl -s 'http://localhost:9000/square_root/?x=2&y=10'; echo` (extra) → TERM(a07: 2).
SAY: Step 7: add x equals 2 and y equals 10. The query string fills the function's arguments, and back comes the square root of 104.

SHOW: TRACKER [A] 7 · extra. Strip: line 1 of `a08` → TERM(a08: 2 wrap, 3): `x=abc` hits the
`float` hint and bounces RED, `float_parsing` YELLOW, `[HTTP 422]` RED.
SAY: Two extras. A letter instead of a number bounces off the float type hint with 422.

SHOW: Strip: line 1 of `a09` → TERM(a09: 2, 6): the path without the slash makes a PINK U-turn on
V4: `307 Temporary Redirect`, `location: …/square_root/`.
SAY: Without the trailing slash, FastAPI answers 307 and points to the slash version.

SHOW: The uvicorn strip: TERM(a03: 55–59); the status column of each line writes in colour (200
GREEN ×3, 422 RED, 307 PINK); IPs and ports stay GREY.
SAY: The server's log shows each request with its status. 200, 200, 200, 422, 307.

SHOW: TRACKER [A] 8. Strip: `curl -s http://localhost:9000/docs | grep -E '<title>|openapi.json|swagger'`
(extra) → TERM(a10: 3, 6); `<title>API Server - Swagger UI</title>` and `url: '/openapi.json'`
YELLOW. V4's route table unfolds into a GREY browser drawing (tag `illustration`, address
`localhost:9000/docs`): two rows `GET /` and `GET /square_root/`, the second expanded with "x ·
number · default 1", "y · number · default 2" (from `a11:32–48`, chip `extra`) and a "Try it out"
button. (No `▶` here: the next block says "pause".)
SAY: Step 8: open slash docs. FastAPI built this page from your code: x and y appear as numbers, with their defaults, and you can try a call right there.

SHOW: The type hints in the signature glow, and two GREEN threads run from them: one to the 422
bounce, one to the docs rows. A caption: "type hints → validation + docs"; `▶ your turn` beside the docs drawing's "Try it out". Fade; empty frame.
SAY: The type hints became the validation and the documentation. Pause and try one call from the docs page.

---

## S05 · Files for the browser: the simple frontend — `s05_static.py` · `StaticPages`

SHOW: No tracker. LECTURE 18 · 16–17 (Frontend). Three cards fan out: "HTML · structure", "CSS ·
style", "JavaScript · behavior", the third with a PURPLE badge "the only programming language of
the three". Then CODE(cheese-app-v1/src/frontend-simple/index.html: 4–12) with a second small panel
CODE(cheese-app-v1/src/frontend-simple/index.html: 74–75): `<title>` (10) GREY-boxed "HTML", the
`styles.css` link (11) "CSS", `<script src="main.js">` (74) "JavaScript".
SAY: Now the other half of version 1: a page. The lecture splits a page into HTML for structure, CSS for style and JavaScript for behavior. In version 1, index dot html links all three.

SHOW: LECTURE off. TRACKER [F] 1 (tracker: "README › Frontend App (Simple) Container", 6 dots). A
second terminal `laptop · new terminal`, prompt `student@laptop:~$`, types
`cd cheese-app-v1/frontend-simple` → TERM(a19: 2) RED; extra `cd cheese-app-v1/src/frontend-simple && ls`
→ TERM(a20: 2–7); tag `erratum` "add src/".
SAY: Step 1: go to the frontend folder. Same slip as before: add src.

SHOW: TRACKER [F] 2. It types `sh docker-shell.sh` → TERM(a20b: 3, …, 28–29); TRACKER [F] 3: at the
prompt (`a20b:30`) it types `http-server` → TERM(a20b: 31, 33, 37, 45–47); line 37 `Cache: 3600
seconds` YELLOW; on "inside the container" lines 46–47 get a GREY bracket "container addresses";
a PINK door `8080 → 8080` draws on the laptop wall. `▶ your turn`.
SAY: Steps 2 and 3: pause, run sh docker-shell.sh, then http-server inside the container. It serves this folder on port 8080, with a one-hour cache. The addresses it prints are inside the container; your laptop uses 8080.

SHOW: TRACKER [F] 4. LECTURE 18 · 18–23 (Frontend). **V1**: the browser window at
`localhost:8080`, the laptop with a TEAL `cheese-app-frontend-simple` box holding a PURPLE
"http-server" and a stack of GREEN file icons (`index.html`, `main.js`, `styles.css`). The hops
animate: request → door → container; a **file** (the `index.html` icon) travels back; the browser
renders it (drawing, tag `illustration`, from `a21`: header "🧀 Formaggio.me is here!"). Hop 4's
caption "4 the function runs" Transforms into "4 a file is read", with a GREY ghost of S03's caption. Strip:
line 1 of `a21` (extra) → TERM(a21: 2–7); `cache-control: max-age=3600` YELLOW.
SAY: Step 4: open localhost 8080. This is the lecture's first trip: the request reaches http-server, a file comes back, and the browser draws it. Pause and open it.

SHOW: TRACKER [F] 4 · extra. Strip: line 1 of `a22` → TERM(a22: 2–4); line 2 "Sample Podcast Data
(This would normally come from an API)" YELLOW. In V1 a dashed GREY second arrow from the page
toward port 9000 appears with a "?" and stays undrawn; a GREY chip "part 2".
SAY: An extra look at main dot js: the podcasts are sample data, which would normally come from an API. Part 2 adds that second trip.

SHOW: LECTURE off. TRACKER [F] 5. A README card (`README.md · lines 86–95`) shows the README's
snippet: `<body>` … `</body>`, tag `erratum`: the outer `<body>` lines and "🧀 Welcome to the cheese
identification App!" turn RED ("an old whole body · would drop the page and its script tag"); only
the `<p>…</p>` lines stay GREEN. Chip "your editor". Strip types
`git -C ~/cheese-app-v1 diff -- src/frontend-simple/index.html` (extra) → TERM(a23: 15–23); `+`
lines GREEN.
SAY: Step 5: add a paragraph to index dot html. A small note: the README's snippet is an old whole body, and pasting it would drop the page and its script tag. Add only the paragraph.

SHOW: TRACKER [F] 6. The browser drawing refreshes (a GREY reload sweep), the new line appears
under the hero. Strip: line 1 of `a24` (extra) → TERM(a24: 2–4), line 3 YELLOW. Extra: line 1 of
`a25` → TERM(a25: 2–3); `max-age=3600` YELLOW with a GREY chip "hard refresh · or http-server -c-1".
(No `▶` here: the pause cue was step 4's.)
SAY: Step 6: refresh, and the new text appears. Edits to main dot js may need a hard refresh, because http-server lets the browser cache files for an hour.

SHOW: TRACKER [C1] 1 · extra (tracker: "README › Docker Cleanup · cheese-app-v1", 4 dots). In
`laptop`: line 1 of `a26` → TERM(a26: 2–4), two running rows, with a GREY chip "check: both still
running". TRACKER [C1] 2 (Stop containers): both terminals `^C` and `exit` (TERM(a03: 62, 69–70) and
TERM(a20b: 57–58, 60–61)). Then the README's `docker container ls` → TERM(a30: 2): the two rows
collapse into the empty header (Transform), GREY chip "--rm: they removed themselves".
SAY: To clean up, press Control C and type exit in both terminals. The container list is then empty, because both removed themselves.

SHOW: TRACKER [C1] 3 `docker system prune` → TERM(a31: 2–8, …, 17); `[y/N] y` YELLOW; TRACKER [C1]
4 `docker image ls` → TERM(a32: 2–8). Fade; empty frame.
SAY: Docker system prune asks first, so type y for yes; the image list shows what stays.

---

## S06 · v2: four containers, and the cheese books — `s06_vectordb.py` · `VectorDb`

SHOW: No tracker. A README card (`README.md · lines 5–10`, the four-row table) morphs into **V5
`TwoLocalhosts`**' outline: a GREY laptop with four TEAL boxes, `cheese-app-vector-db` (door
`8000`), `cheese-app-vector-db-cli` (no door), `cheese-app-api-service` (door `9000`),
`cheese-app-frontend-react` (door `3000`), and a GREEN cable `cheese-app-network` under them.
SAY: Now version 2, the real app: four containers on one Docker network. Chroma, the vector database, on 8000; a loader; the API on 9000; and the React frontend on 3000.

SHOW: A card EXPECTED(expected/01-prerequisites.txt: 4–8) drawn as a checklist (tag `illustration ·
README:13–18`): a BLUE "Google Cloud project + Vertex AI API", a GREY key file "ml-workflow.json ·
Vertex AI User" (no content), a GOLD-outlined "about 10 GB". A GOLD `cost_tag("with your key:
chat and embedding calls bill your project")` hangs on the BLUE item.
SAY: The prerequisites: a Google Cloud project with the Vertex AI API, the ml workflow key with the Vertex AI User role, and about 10 gigabytes. With your key, chat and embedding calls bill your project.

SHOW: The key icon gets a GREY chip "this recording: a well-formed key for no account". A small
diagram: everything inside the laptop GREEN-ticked; one PINK arrow out to the BLUE Vertex AI cloud
with a RED "account not found" on its tip.
SAY: One honest note: our recording's key file is well-formed but belongs to no account. Everything that does not call Google works exactly as for you; the first Google call fails, and we show where.

SHOW: TRACKER [SE] 4 (the setup tracker returns for its last step). Terminal `laptop`, a GREY chip
"cd ~/cheese-app-v2" (the move from S05's folder), prompt `student@laptop:~/cheese-app-v2$`. It types line 1 of `b03` (tag `extra`, chip "or edit both
files") and `git diff` → TERM(b03: 3–4, 7, 11–12, 16–17, 20, 24–25); the `+` lines' placeholder
`your-gcp-project` GREEN.
SAY: Last setup step: put your project ID into both docker-shell scripts. Ours shows a placeholder.

SHOW: TRACKER [V] 1 (tracker: "README › Tutorial: Vector DB for RAG Setup", 5 dots). LECTURE 18 · 45
(APIs): a small GREY card "slide 45 · step 1: make sure the vector database is running". It types
`cd src/vector-db` → TERM(b05: → (no output)); TRACKER [V] 2: `./docker-shell.sh`. `▶ your turn`.
SAY: The lecture's first step: make sure the vector database is running. Step 1: change into src, vector db, and run docker-shell.sh. Pause and run them.

SHOW: LECTURE off. TERM(b06: 2, 3, …, 24, 27–28); line 2 (the network id) gets a GREY chip "docker
network create · cheese-app-network" (id not read), line 27 `chromadb/chroma:1.5.9 Pulled` with the
chip "at the time of recording", line 28 `Container cheese-app-vector-db Created` TEAL. In V5 the
GREEN cable draws and the `cheese-app-vector-db` box lights. Beside it CODE(cheese-app-v2/src/vector-db/docker-compose.yml:
19–25) only: `8000:8000` (23) PINK on "publishing 8000", `./docker-volumes/chromadb:/data` (25)
GREEN on "a folder on your laptop" (`external: true` is covered by the terminal's network chip).
SAY: The script creates the network, builds the loader, and Compose starts Chroma, publishing 8000 and keeping its data in a folder on your laptop.

SHOW: TRACKER [V] 3. TERM(b06: 31–34, 36–42): the banner and its three commands. At the prompt
(line 44) it types `python cli.py --download --load --chunk_type recursive-split` → TERM(b06: 50,
52, 53, 65, …, 197, 208); a YELLOW counter beside the terminal sums the "Finished inserting" numbers
book by book (923, 714, 3569, 926, 2623, 1198, 1146, 678, 2147, 269, 163, read from
`b06:65, 78, 97, 110, 127, 141, 155, 168, 184, 196, 208`) and lands on **14,356** GREEN. `▶ your turn`.
SAY: Step 2, inside the container: download and load the cheese books. Eleven files, one finished line per book, 14,356 chunks in all. Pause while yours loads.

SHOW: A GREY dashed card "Lecture 5 · chunk → embed" slides in beside the counter, an arrow
"downloaded, not recomputed" pointing at the `outputs/` folder (extra `b09`: TERM(b09: 25–27) small,
`78.8M outputs`, `50.9M docker-volumes/chromadb`).
SAY: These are the RAG lecture's chunks and embeddings, downloaded, not recomputed.

SHOW: TRACKER [V] 4. It types `python cli.py --chat --chunk_type recursive-split` → TERM(b06: 211,
212, 219–222, …, 297 wrap); line 297 `google.auth.exceptions.RefreshError: ('invalid_grant: Invalid
grant: account not found', …)` RED. GOLD `cost_tag` on the Vertex AI arrow in a small inset. A GREY
chip "with your key: an answer from the books".
SAY: Step 3: chat. The first Google call, embedding the question, fails here: invalid grant, account not found. With your key, an answer from the books appears instead.

SHOW: CODE(cheese-app-v2/src/vector-db/cli.py: 370–378); line 377 `query = "How is cheese made?"`
YELLOW, a GREY note chip "fixed question · edit this line" (`cli.py:519–561` read no input).
SAY: A small note: chat always asks its own fixed question, how is cheese made; there is no place to type yours. To ask another, edit that line in cli dot py.

SHOW: TRACKER [V] 5 (the README's step 4). It types `exit` → TERM(b06: 299). TRACKER [V] 5 · extra: strip types line 1
of `b07` → TERM(b07: 2–3), `0.0.0.0:8000->8000/tcp` PINK; then line 1 of `b10` → TERM(b10: 2);
V5's phone book card opens on the cable; on "turns its name into an address" its first entry writes
on as name, an arrow, then the address: `cheese-app-vector-db → 172.19.0.2`. Fade; empty frame.
SAY: Step 4: exit. Chroma keeps running on 8000, as an extra docker ps shows, and the network's phone book now turns its name into an address.

---

## S07 · Start the API: alive, then ready — `s07_ready.py` · `AliveAndReady`

SHOW: TRACKER [B] 1 (tracker: "README › Tutorial: Backend APIs", 10 dots). A terminal
`laptop · new terminal`, prompt `student@laptop:~/cheese-app-v2$`. A README card (`README.md ·
lines 85–86`): "In a new terminal, from the cheese-app-v2 folder … The first build takes a few
minutes, because of TensorFlow". It types `cd src/api-service` → TERM(b20: → (no output));
TRACKER [B] 2: `./docker-shell.sh`. `▶ your turn`.
SAY: Backend APIs. In a new terminal, from the cheese app v2 folder: step 1, change into src, api service, and run docker-shell.sh. The first build takes a while, because of TensorFlow, so pause and start it.

SHOW: TERM(b21: 2–3, …, 24, 25–28, 31–35); line 2 `Building cheese-app-api-service
(Dockerfile.dev)...` PURPLE, line 3 `136.2s` YELLOW; the banner lines with "at the time of
recording"; the two commands `api_server` and `pytest` GREEN. A GOLD-outlined "disk" chip "this
image: 4.2 GB" (from `b46:3`, extra) at the side.
SAY: The banner offers two commands: API server and pytest.

SHOW: CODE(cheese-app-v2/src/api-service/docker-shell.sh: 14–34) (scrolls in two pages of ≤ 12
lines): lines 16–18 (already running → `docker exec`) YELLOW on "already runs"; then lines 26–28
(`/secrets:ro`, `/persistent`, `-p 9000:9000`) and 33 (`--network cheese-app-network`) on their
phrases. Under lines 16–18 a GREY chip: "a leftover v1 API counts too · docker ps · docker stop
cheese-app-api-service" (v1, 2025 and main share the container name). In V5 (small, bottom right)
the API box joins the GREEN cable.
SAY: This script checks first: if the container already runs, it just opens a shell in it. Otherwise it mounts secrets without write access, mounts your persistent folder, publishes 9000, and joins the network.

SHOW: TRACKER [B] 3. At the prompt (`b21:37`) it types `api_server`. CODE(cheese-app-v2/src/api-service/docker-entrypoint.dev.sh:
12–16): line 13, the uvicorn line, YELLOW; a small V3 icon beside it ("same server, same app
address"). `▶ your turn`.
SAY: Step 2: API server. It is almost the same uvicorn line as before, pointing at api dot service colon app. Pause and start it.

SHOW: TERM(b21: 39–40, 43, 44–46); line 43 `Application startup complete.` GREEN at once; then lines
44–46 (TensorFlow, `oneDNN`, `cpu_feature_guard`) arrive GREY with a bracket "from a background
thread".
SAY: Application startup complete arrives at once. Only after it do TensorFlow's lines appear, from a background thread that loads the cheese classifier.

SHOW: **V6 `ProbeLamps`** on the TEAL API box: two lamps, `/healthz` and `/readyz`. Behind the
readiness lamp, two wires: a CNN progress ring (filling) and a Chroma heartbeat line to the
vector-db box. CODE(cheese-app-v2/src/api-service/api/service.py: 19–23): line 22
(`threading.Thread(target=llm_cnn_utils.load_cnn_model …`) YELLOW; then on "healthz"
CODE(…/service.py: 43–45) on the `/healthz` lamp, and on "readyz" CODE(…/service.py: 48–56), lines
50–51 and 53 lighting on their wires.
SAY: That is the design: the API answers right away while the model loads. Two probes say how far along it is: healthz and readyz.

SHOW: TRACKER [B] 4. Strip `second tab`: `curl -s -i http://localhost:9000/healthz` (extra) →
TERM(b22: 2, 8): the `/healthz` lamp GREEN. `curl -s -i http://localhost:9000/readyz` (extra) →
TERM(b23: 2, 8): `503` RED, the lamp amber, the ring half full. The uvicorn strip shows TERM(b21:
48–60) scrolling (the 503 lines RED). The lamp stays amber (`b24` and the last 200 belong to the
ponder's answer). (No `▶` here: step 3's block said "pause".)
SAY: Step 3: healthz says 200: the process is alive. Readyz says 503, CNN model is loading.

SHOW: TRACKER [B] 4 · extra. Strip: line 1 of `b26` → TERM(b26: 13–14, 18–20);
`mobilenetv2_train_base_True.keras` GREEN; a GREY `persistent-folder/` icon on the laptop wall
gains the model file, with a chip "downloaded once · reused on every start".
SAY: An extra look: the model is downloaded once into your persistent folder, and every start reuses it.

SHOW: Strip: line 1 of `b25` → TERM(b25: 2–5): two RED `404`. A tiny map: root `/` holds only
`healthz` and `readyz` (V6's lamps); a PINK branch `/api` holds everything else (from
`service.py:1–7`, a CODE strip of those lines). Then RECORDED(expected/04-troubleshooting.txt: 9–10,
14) small, tag `recorded · README:228–229, 233` (Chroma down, vector DB empty, port already
allocated: what to do), no SAY change.
SAY: Another extra: the version 1 habits fail. Slash and slash docs answer 404; everything the browser calls is under slash api, and only the probes stay at the root.

SHOW: V6 frozen: `/healthz` GREEN, `/readyz` amber, the ring part-filled. Nothing else moves.
PONDER(8 s, "/healthz says 200, /readyz says 503.\nRestart the container,\nor just wait?")
SAY: So, a quick test. Healthz says 200 and readyz says 503. Do you restart the container, or wait?

SHOW: The card leaves. Strip types `curl -s -i http://localhost:9000/readyz` again → TERM(b24: 2,
8), `200` GREEN, chip "about 9 s later, here"; the uvicorn strip adds TERM(b21: 61) (the 200 GREEN);
the ring fills, the readiness lamp turns GREEN. Then a GREY dashed thought bubble "Kubernetes
(Lectures 19, 22) can use these" holds a small load balancer sending PINK traffic only to
GREEN-ready boxes, and a restart arrow tied to the liveness lamp. Fade; empty frame.
SAY: Wait: about nine seconds later, readyz says 200: the model is loaded and Chroma answers. A restart would only start the loading over. Kubernetes, which you meet in lectures 19 and 22, can use exactly these two probes: restart on liveness, send traffic on readiness.

---

## S08 · Screens decide the routes — `s08_routes.py` · `ScreensToRoutes`

SHOW: TRACKER [B] 4. LECTURE 18 · 29 (APIs). A29 redrawn: three gray phone outlines "Newsletters",
"Podcasts", "Chat" (a photo bubble "What type of cheese is this?"). From each a PINK thread grows
upward to a data chip: "newsletters", "podcasts", "chat + photo".
SAY: Which routes does the API need? The lecture starts from the screens: newsletters, podcasts, and a chat that takes a photo. Each screen needs data, and each kind of data becomes a group of routes.

SHOW: LECTURE 18 · 44 (APIs). The chips become A44's six WHITE-outlined route groups (Newsletters,
Podcasts, LLM Chat, LLM + CNN Chat, RAG Chat, Agent Chat). **V4 `RouteTree`** grows below from
CODE(cheese-app-v2/src/api-service/api/service.py: 31–40): a root `/api`; branches `newsletters` (36)
and `podcasts` (37); then a PURPLE stamp "create_router" (38–40) prints three identical chat
branches labelled `llm`, `llm-cnn`, `llm-rag`, each with `chats`; WHITE sub-labels "Ask",
"Identify" and "Cheese books" write under the three branches, each on its word (S09 and S11 reuse
them). The chips snap onto their
branches and turn GREEN; "Agent Chat" stays GREY dashed, unattached (tag `erratum`, "slide 44: six ·
this repo: five routers").
SAY: In service dot py, newsletters and podcasts get a router each under slash api. Then one function stamps out three chat routers: Ask, Identify and Cheese books. The lecture shows six groups; agent chat has no router in this repository.

SHOW: LECTURE 18 · 30–33 (APIs). The tree dims. One GREY-dashed diagram, browser → API → back ends,
and an agent box that moves: it slides behind the API while an MCP box fades in (A30), the MCP box
fades out (A31), then the agent slides out front as the client (A32). Under it a one-line chip (A33):
"REST API · for apps · FastAPI | MCP · for agents · FastMCP · not in this repo".
SAY: The lecture also shows three places an agent can sit, with or without an MCP service. This repository has none.

SHOW: LECTURE 18 · 39–41 (APIs). A GREY card with the slide's one-file form `@app.get("/newsletters")`
(tag `erratum`, "the idea") beside the real path on V4: `/api` + `newsletters` + `/`; a PINK label
writes `/api/newsletters`.
SAY: And the slide's one-file route is the idea. The repository puts the same function in a router, mounted at slash api, newsletters.

SHOW: LECTURE off. TRACKER [B] 5. A README card (`README.md · lines 106–112`), chip "your editor".
Strip types `git diff api/service.py` (extra) → TERM(b27: 20–29); `+` lines GREEN; on V4 a new leaf
`square_root` appears under `/api`. The uvicorn strip: TERM(b21: 65, 70–72) (`StatReload detected
changes`).
SAY: Demo route: add the README's function after get status, and save. The server reloads by itself.

SHOW: V6's readiness lamp drops to amber; extra: strip line 1 of `b30` → TERM(b30: 2–3), the lamp
GREEN again.
SAY: This loads the model again, and readyz is back to 200 shortly after.

SHOW: TRACKER [B] 6. Strip: `curl -s http://localhost:9000/api/square_root; echo` (extra) →
TERM(b28: 2); then `curl -s 'http://localhost:9000/api/square_root?x=3&y=4'; echo` (extra) →
TERM(b29: 2), `5.0` GREEN; the browser drawing (tag `illustration`) shows the same. `▶ your turn`.
SAY: Then open slash api, square root: the square root of 5 again. With x equals 3 and y equals 4, it answers five point zero. Pause and try both.

SHOW: TRACKER [B] 7. Strip: line 1 of `b31` (extra) → TERM(b31: 2–4); `/api/openapi.json`
YELLOW. TRACKER [B] 7 · extra: line 1 of `b32` (folds) → TERM(b32: 2, 3–27) shown as V4's leaves
filling the tree, 25 rows; a GREY counter "25 operations".
SAY: API docs: they moved to slash api, docs. An extra listing shows all 25 operations: the leaves of this tree.

SHOW: TRACKER [B] 8. The browser drawing of `/api/docs` (tag `illustration`) expands
`GET /api/newsletters`, `limit = 2`, Execute. Strip: line 1 of `b33` (the curl the docs page shows) →
TERM(b33: 5–9, 15–19, 25–26) (the progress meter, lines 2–4, dropped); the two `"title"` lines
YELLOW. LECTURE 18 · 41 (APIs): a small GREY card "slide 41: a JSON list of newsletters". Extra:
line 1 of `b34` → TERM(b34: 2–3), RED. `▶ your turn`.
SAY: In the docs, pause and try get newsletters with a limit of 2. Two newsletters come back as JSON, newest first: the lecture's example, now real. An unknown ID gets 404, newsletter not found.

SHOW: LECTURE off. TRACKER [B] 9. A README card (`README.md · lines 123–132`) becomes a file map
beside V4: `service.py` on the root, `settings.py` as a GREY gear, the routers on their branches,
three utils files `llm_utils.py` (Ask), `llm_cnn_utils.py` (Identify), `llm_rag_utils.py` (Cheese
books) hanging from the three chat branches, `chat_utils.py` as a GREEN folder icon "saves chats".
Fade; empty frame.
SAY: Review the code: the README's table maps each file. Service dot py builds the app, settings dot py holds every setting, the routers hold the routes, and one utils file per chat mode does the work.

---

## S09 · A chat is a file, not a memory — `s09_chat.py` · `ChatIsAFile`

SHOW: TRACKER [B] 9. LECTURE 18 · 27 (Frontend). A GREY card redraws B27's handler box "use
Gemini to generate text" with its route label `/chat` (tag `erratum`). Beside it
CODE(cheese-app-v2/src/api-service/api/routers/chat.py: 58–67) then (…: 69–76): line 58
`@router.post("/chats")` and line 69 `@router.post("/chats/{chat_id}")` YELLOW; on "the real path"
a PINK label writes `/api/llm/chats`.
SAY: The lecture's chat handler says: use Gemini to generate text. In the repository, one route starts a chat and another continues it. The real path names the mode: slash api, llm, chats.

SHOW: LECTURE off. **V7 `ChatFile`** alone, no code yet: the browser holds a small PINK key
labelled `X-Session-ID` (a UUID). A POST envelope carries the key and one message; the API box opens
a GREEN file `chat-history/llm-cnn/<session>/<chat>.json`, appends two lines (user, reply), saves,
and its own memory bubble empties ("forgets").
SAY: How does the API remember a conversation? It does not: with every message, the browser sends a session ID, one random UUID per browser. The API opens that session's chat file, adds your message and the reply, saves, and forgets.

SHOW: TRACKER [B] 9 · extra. CODE(…/chat.py: 19–23) small: line 21 (`Header(alias="X-Session-ID",
pattern=UUID_PATTERN)`) YELLOW. Strip: line 1 of `b36` (folds) → TERM(b36: 2 wrap, 3): an envelope
without the key bounces RED, `missing … X-Session-ID` YELLOW, `422`. Line 1 of `b37` → TERM(b37:
2–3): an empty envelope bounces, `422`.
SAY: Two extras: no session ID, or an empty message, gets 422.

SHOW: Strip: line 1 of `b39` (folds; the photo payload is the repo's own
`news-letters/assets/blue-cheese.jpg`, a GREY chip names it) → TERM(b39: 2 from "\"role\":\"cnn\"",
3); `"prediction_label":"parmigiano","accuracy":58.22` YELLOW, `[HTTP 200]` GREEN. In V7 a small
PURPLE "CNN" box beside the API answers with a GREY chip "a guess"; no network arrow leaves the
laptop (chip "photo step: offline"); a GREY dashed arrow "follow-up question → Gemini" stays undrawn.
SAY: Identify's photo step works fully offline. We send the repository's own blue cheese photo, and the CNN guesses parmigiano, at 58 percent. A follow-up question would go to Gemini.

SHOW: Extras: line 1 of `b42` → TERM(b42: 2–3); the two paths' `llm-cnn/` and `.json` GREEN, the
UUIDs GREY. V7's file icon gets the same path; a photo icon lands in a separate
`chat-history/llm-cnn/images/` folder, not beside the file.
SAY: An extra listing shows it on disk: one JSON file per chat under your session, and the photo in the mode's images folder.

SHOW: Line 1 of `b38` (folds) → TERM(b38: 2–3): `Internal Server Error`, `[HTTP 500]` RED. The
uvicorn strip shows TERM(b21: 92, 93, …, 174–179, …, 261 wrap): the `start_chat` → `add_turn` →
`respond` frames GREY, line 261 `RefreshError … account not found` RED. In V7, a PINK arrow from the
API to a BLUE "Vertex AI · Gemini" cloud carries a GOLD `cost_tag("with your key: billed")` and
stops RED at the cloud. EXPECTED(expected/02-chat-contract.txt: 11–15) small, tag `expected ·
docs/contract.md:38–42`: the reply shape `{message_id, role: "assistant", content}`.
SAY: Ask mode calls Gemini, and here it stops: Internal Server Error, status 500. The API's terminal shows why: the same invalid grant, account not found. With your key, Gemini's answer has this shape.

SHOW: RECORDED(expected/04-troubleshooting.txt: 11–12), tag `recorded · README:230–231`; the
"Gemini: 403 / 404" cells get a GREEN chip "API answers 502" (`llm_utils.py:85–86`); beside the
table a GREY tag "not in the table" with an arrow to a RED "500 + RefreshError in the API
terminal" (no `erratum` tag: the README is incomplete for this case, not wrong).
SAY: A small note: the README's table covers Gemini 403 and 404, reported as 502. A key Google cannot sign in with fails earlier, as a plain 500, so check the API's terminal first.

SHOW: A README card (`README.md · lines 134–138`). On "any copy", V7 duplicates the API box: a
second TEAL copy answers the next message by opening the same GREEN file. On "plain def", three
PURPLE thread lanes appear in one API box; one lane holds a slow Gemini call while the others pass
quick requests.
SAY: Two more README notes. Each message rebuilds the conversation from the saved file, so any copy of the API can answer. And routes written with plain def run in threads, so one slow answer does not block the rest.

SHOW: TRACKER [B] 10. A second terminal `laptop · new terminal`, prompt
`…/cheese-app-v2/src/api-service$`, types `./docker-shell.sh` → TERM(b44: 2) (line 2 YELLOW,
"already running · shelling in"); at the prompt (line 3) it types `pytest` → TERM(b44: 5, 11, 13–14,
16); line 16 `26 passed in 0.51s` GREEN, growing a GREEN badge. `▶ your turn`.
SAY: Last, the tests: in a second terminal, in the same folder, docker-shell.sh again opens a shell in the running container. Run pytest: 26 passed. Pause and run it.

SHOW: The badge settles on V5's API box. A README card (`README.md · line 145`): "Keep this
container running." The browser window (GREY, empty) appears left with `localhost:3000` in its
address bar; a PINK dashed arrow leaves it toward the laptop and stops at a YELLOW "?" before the
`9000` door. Fade; empty frame.
SAY: Keep this container running. The API is ready, but nobody can use it from a browser yet. In part 2 the browser talks to port 3000, so how does that reach 9000?

---

## S10 · Why a framework: React with Vite — `s10_react.py` · `ReactShell`

SHOW: No tracker. A title card "Part 2 · the frontend" over V5's laptop, the API box GREEN-badged on
9000; on "up on port 9000" the API's GREEN badge pulses; on "a page that uses it" an empty GREY
browser window slides in, with a dashed PINK arrow toward the laptop.
SAY: Part 2: the frontend. The API is up on port 9000; now a page that uses it.

SHOW: LECTURE 18 · 30–31 (Frontend). **V8 `OneShell`**, part a: four separate GREY page outlines
"Home", "Newsletters", "Podcasts", "Chat", each carrying its own small header strip, script chip
and style chip. A click on one link sends a GREY reload sweep over a whole page; chips "nothing
shared", "every page loads separately", "slow" write on.
SAY: The lecture starts with one HTML page per feature. Each carries its own header, script and style; nothing is shared, and every click loads a whole page: slow.

SHOW: LECTURE 18 · 32–33 (Frontend). The four pages collapse into one outline "single-page app ·
components"; a row of four GREY framework chips (names as on B33, no logos) with "React"
highlighted YELLOW.
SAY: The fix is a single-page app built from components, with a framework. The lecture names the common ones and picks React.

SHOW: LECTURE 18 · 35–37 (Frontend). V8, part b: a component card "function → markup (JSX)"; then
the shell: "Header · defined once" (top), a middle block, "Footer" (bottom). The middle block swaps
Home → Newsletters → Chat while the header stays put (a YELLOW pin on it).
SAY: In React, a component is a function that returns markup, written in JSX. The app is one shell: a header defined only once, a footer, and in between a block that changes with each page.

SHOW: A GREY chip under the React chip writes "React + Vite (dev server, build) + React Router
(pages)", tag `erratum` "today's repo". CODE(cheese-app-v2/src/frontend-react/src/main.jsx: 17–24):
each `path` (`chat`, `newsletters`, `newsletters/:id`, `podcasts`, `*`) and the `index` row fly into a
PINK address bar above the shell, one per phrase.
SAY: Today's repository uses React with Vite, a development server and build tool, plus React Router. In main dot jsx, a route table maps each address to a page, with a star that catches everything else.

SHOW: CODE(cheese-app-v2/src/frontend-react/src/App.jsx: 15–17, 52–59) (header open, header close,
`<Outlet />`, footer): line 17 `<header` → the shell's header, line 55 `<Outlet />` → the middle
block (now labelled "Outlet"), line 59 `<footer` → the footer; the shell's YELLOW pin on the header
pulses once. LECTURE off at the end of the block.
SAY: In App dot jsx, the header and footer are written once, and between them sits the outlet, the window where the current page appears.

SHOW: TRACKER [R] 1 (tracker: "README › Tutorial: React Frontend Setup", 7 dots). A terminal `laptop ·
new terminal`, prompt `student@laptop:~/cheese-app-v2$` (the README: "from the cheese-app-v2 folder"); it types `cd src/frontend-react` →
TERM(d01: → (no output)); TRACKER [R] 2: `./docker-shell.sh`. CODE(cheese-app-v2/src/frontend-react/docker-shell.sh:
14–23) beside it: line 19 (`-v "$(pwd)":/app`) GREEN, line 20 (`…-node_modules:/app/node_modules`)
ORANGE with a chip "named volume", line 21 `-p 3000:5173` PINK, line 22 `--network
cheese-app-network` GREEN. In V5, the frontend box joins the cable with door `3000 → 5173`.
`▶ your turn`.
SAY: React setup, in a new terminal from the cheese app v2 folder: step 1, change into src, frontend react, and run docker-shell.sh. It mounts your code, keeps node modules in a named volume, publishes 3000 to port 5173, and joins the network. Pause and run it.

SHOW: TERM(d02: 2–3, 21–27, 29–33); lines 23–24 with "at the time of recording"; line 27 `up to
date in 571ms` YELLOW, with a GREY chip "your first run: a full install into the volume"
(`docker-entrypoint.dev.sh:8`).
SAY: The banner shows Node and npm. Your first run installs the dependencies into the volume; ours was already up to date.

SHOW: TRACKER [R] 3. At the prompt (`d02:35`) it types `npm run dev` → TERM(d02: 37–38, 80, 82–83);
line 80 `VITE v8.3.5 ready` PURPLE; lines 82–83 get a GREY bracket "inside the container"; on
"use 3000" V5's door `3000 → 5173` pulses PINK. `▶ your turn`.
SAY: Step 2: npm run dev. Vite is ready and prints two addresses on 5173; both are inside the container, so on your laptop, use 3000. Pause and start it.

SHOW: TRACKER [R] 4. The browser window (tag `illustration`) opens `localhost:3000`. Strip `second
tab`: line 1 of `d03` (extra) → TERM(d03: 2, 23, 26–27); `<div id="root"></div>` and
`/src/main.jsx` YELLOW. The drawing shows an empty page with one `root` box that fills from the
script.
SAY: Step 3: open localhost 3000. The HTML is almost empty: one div called root and a script, main dot jsx. The whole app is one page and its JavaScript.

SHOW: TRACKER [R] 4 · extra. Strip: line 1 of `d08` → TERM(d08: 2–6); every `200 text/html` YELLOW,
`/nope` included. The PINK address bar over V8's shell cycles `/podcasts`, `/newsletters`,
`/chat?model=llm`, `/nope`; the middle block swaps to the matching page and, for `/nope`, to
"Not found". Fade; empty frame.
SAY: An extra check: every address, even one that does not exist, returns the same HTML. The browser picks the page, not the server.

---

## S11 · One origin: the Vite proxy — `s11_proxy.py` · `OneOrigin`

SHOW: TRACKER [R] 4. LECTURE 18 · 24–26 (Frontend). V1: the browser window `localhost:3000`, its
page JavaScript firing a PINK data arrow (the lecture's picture: "the page's JavaScript calls the
API"). CODE(cheese-app-v2/src/frontend-react/src/lib/api.js: 17–24) small (`localStorage` YELLOW),
then CODE(…/api.js: 33–44): line 34 (`'X-Session-ID': sessionId()`) PINK, line 44
(`fetch(path, options)`) YELLOW with a chip "path = /api/… · relative".
SAY: Now the hook's answer. In the lecture, the page's JavaScript calls the API. Here, every call in api dot js goes to a relative path starting with slash api, with the session ID from local storage.

SHOW: LECTURE off. CODE(cheese-app-v2/src/frontend-react/vite.config.js: 5–15): line 13 (`proxy:
{ '/api': … 'http://cheese-app-api-service:9000' }`) YELLOW; line 10 (`host: true`) PINK; line 11
`5173`. V1's hop **3½**: the "?" box inside the frontend container flips to a PURPLE courier
labelled "Vite".
SAY: And vite dot config dot js holds the courier: a proxy rule that forwards slash api to cheese app API service, port 9000, by container name.

SHOW: **V1 + V5**: every arrow from the browser lands on door `3000`; inside, the Vite courier
carries each `/api` envelope along the GREEN `cheese-app-network` cable to the API box, looking up
the name in the phone book on the way. The `9000` door stays, dimmed, labelled "for /api/docs and
curl". Strip: line 1 of `d04` again → TERM(d04: 2, 5) (`server: uvicorn` YELLOW).
SAY: So the browser only ever talks to localhost 3000. Vite, in the frontend container, carries each slash api request across the network. That is why uvicorn answered on 3000.

SHOW: A PINK origin label splits into three chips "http" · "localhost" · "3000"; the page and every
API call share it (two arrows, one label). A GREY chip "same-origin policy · the browser's rule"
stays quiet (ORANGE outline); S01's permission-slip icon returns, struck GREY "not needed". No `b43`
strip here (seen in S01). CODE(cheese-app-v2/docs/contract.md: 6–7) as a GREEN card (not spoken).
SAY: An origin is the scheme, the host and the port. The page and its API calls share one origin, so the browser has nothing to object to, and the API needs no permission slip.

SHOW: V5 alone: the browser, outside the laptop's network, holds an envelope addressed
`http://cheese-app-api-service:9000`. Nothing else moves.
PONDER(8 s, "Could the page's JavaScript call\nhttp://cheese-app-api-service:9000\ndirectly?")
SAY: So, a quick test. Could the page's JavaScript call the API by its container name, port 9000, directly?

SHOW: The card leaves. The envelope goes to the laptop's GREY DNS desk, which has no page for that
name: RED "not found". Inside the cable, the phone book lights for Vite's courier, nginx (GREY
dashed, "part 2's next scene") and the API.
SAY: No. The JavaScript runs in your browser, on the laptop, and the laptop's DNS knows no container names. Only code inside the network can use them: the Vite proxy, nginx, the API.

SHOW: TRACKER [R] 4 · extra. Strip: line 1 of `d09` (folds) → TERM(d09: 3), `[HTTP 502]` RED; on V5
the API box is unplugged from the cable for one beat: the courier comes back with a RED `502` and an
empty envelope. The Vite terminal shows TERM(d02: 85–86), `ENOTFOUND cheese-app-api-service` RED.
RECORDED(expected/04-troubleshooting.txt: 13), tag `recorded · README:232`. The API plugs back in.
SAY: An extra experiment: unplug the API from the network for one request. The browser gets 502 with an empty body: the README's troubleshooting row for pages that load empty.

SHOW: TRACKER [R] 5. The browser drawing (tag `illustration`, from EXPECTED(expected/03-review-the-app.txt:
4–11)) steps through Home, Podcasts, Newsletters (each with a PINK `/api/…` arrow through the
courier), then Chat with three mode chips: Identify → extra line 1 of `d07` → TERM(d07: 3) `[HTTP
200]` GREEN; Ask → extra line 1 of `d06` → TERM(d06: 2–3) RED, GOLD `cost_tag` on the Gemini hop;
Cheese books with "How is Tolminc cheese made?" (README:172) → extra line 1 of `b40` → TERM(b40: 2–3)
RED; a "Recent" sidebar lists the session's chats, a GREY reload sweep, and they are still there
(README:174). `▶ your turn`.
SAY: Review the app: home, podcasts and newsletters load through the API, and the Recent tab keeps your chats across a reload. In chat, Identify works through the proxy; Ask, and Cheese books with its Tolminc question, get the same 500. Pause and click through.

SHOW: TRACKER [R] 6. A README card (`README.md · lines 177–185`) lays its rows onto the files
just seen (`vite.config.js`, `main.jsx`, `api.js`, `routes/`, `components/`, `styles.css`) and holds
about 4 s.
TRACKER [R] 7. A terminal `laptop · new terminal`, prompt `…/src/frontend-react$`, types
`./docker-shell.sh` → TERM(d12: 2); at the prompt it types `npm run check` → TERM(d12: 6, 9, 11,
24–25, 27); line 6 YELLOW; line 25 `dist/assets/index-….js` GREEN (hash not read). Fade; empty frame.
SAY: The README's code table names the files we just saw; pause to match each one. Then, in a second terminal in the same folder, docker-shell.sh again opens a shell in the running container; run npm run check: a lint, a format check and a production build. That build is what production serves.

---

## S12 · Production: nginx instead of Vite — `s12_production.py` · `NginxImage`

SHOW: TRACKER [P] 1 (tracker: "README @ e98fa55 › Production images", caption "earlier README ·
extra", 5 dots). A README card (`cheese-app-v2-at-e98fa55/README.md · lines 197–201`, tag `erratum`
"removed from today's README"), beside a GREY chip "files still in main: Dockerfile ·
nginx.conf.template". First, on "who serves", V1's courier box "Vite" is struck GREY with a "?".
SAY: In production, Vite does not run, so who serves the files and forwards slash api? Nginx does. Today's README dropped this section on the recording day, but its files are still in main, so we run the earlier README's commands, marked extra.

SHOW: CODE(cheese-app-v2/src/frontend-react/Dockerfile: 3–16) (two pages of ≤ 12 lines): stage 1
(3–8, `npm ci`, `npm run build`) PURPLE "Node"; stage 2 (12–16, `FROM nginx:1.31.8-alpine`, line 15
`COPY --from=build /app/dist …`) TEAL; an arrow carries a GREEN `dist/` folder from stage 1 to stage
2; the Node box stays behind, dimmed.
SAY: The production Dockerfile has two stages. The first builds the app with Node. The second starts from nginx and copies in only the built files.

SHOW: CODE(cheese-app-v2/src/frontend-react/nginx.conf.template: 11–19): line 13 `location /api/ {`
and 14 `proxy_pass ${API_URL};` YELLOW; then CODE(…/nginx.conf.template: 28–32): line 31
`try_files $uri /index.html;` GREEN; on "missing asset" lines 23–26 (`location /assets/`, `try_files
$uri =404`) GREY. V1's courier box re-labels "nginx".
SAY: The nginx template has the same rule as Vite: slash api goes to the API container. Any other page address gets index dot html, so the router can choose the page; only a missing asset is a real 404.

SHOW: TRACKER [P] 1. In the Vite terminal: TERM(d02: 88, 91–92) (`^C`, `exit`). TRACKER [P] 2:
prompt `…/src/frontend-react$`, types `docker build -t cheese-app-frontend-react:prod .` →
TERM(d20: 2, 4, …, 101, 103, 120, …, 123, 133); line 101 `vite v8.3.5 building …`, 123 `COPY
--from=build /app/dist …` TEAL.
SAY: Stop the dev server with Control C and exit, then build the production image, tagged prod. Its first stage runs the same Vite build you just checked.

SHOW: TRACKER [P] 3. It types `docker run --rm --network cheese-app-network -p 8080:80 cheese-app-frontend-react:prod`
(folds) → TERM(d21: 8, 12); line 8 `Running envsubst on …` YELLOW (chip "API_URL filled in"), line
12 `nginx/1.31.8` with "at the time of recording". TRACKER [P] 4: strip `second tab`, line 1 of
`d22` → TERM(d22: 2–6), `Server: nginx/1.31.8` PURPLE; line 1 of `d23` → TERM(d23: 2–4, wrap); line
1 of `d25` → TERM(d25: 2–4), the two `200 text/html` GREEN and `/assets/ 404` GREY. (No browser
drawing here: block 7 draws `localhost:8080` in V1; no `▶`: this section is extra.)
SAY: Run it on the network, publishing 8080 to port 80. Open localhost 8080: the server is now nginx, slash api still reaches the API, and a deep link still gets the page.

SHOW: TRACKER [P] 5. Strip: `docker images | grep cheese-app-frontend-react` → TERM(d27: 2–3); two
bars grow: `331MB` (dev, TEAL with a PURPLE "Node" band) and `94.8MB` (prod, TEAL, thin); a chip "no
Node, no Vite · files and one proxy rule".
SAY: Compare the sizes: 331 megabytes for the dev image, about 95 for production. No Node, no Vite: just files and one proxy rule.

SHOW: LECTURE 18 · 42 (APIs). **V1**, production version: the address becomes `localhost:8080`, the
courier is nginx, the inner part (the API on 9000) does not move; the outer part (address, front
server) glows YELLOW, the inner part GREEN "unchanged". A GREY chip "slide 42: a domain on 443 ·
Lecture 20: NGINX in front on a VM, port 80" (no `erratum` tag: the slide is ahead of the tutorials,
not wrong).
SAY: The lecture's production slide: only the outside changes. In lecture 20, NGINX goes in front on a cloud machine, on port 80; the API's code and port stay the same.

SHOW: LECTURE off. Tag `extra` on this whole beat. The prod container: `^C` (TERM(d21: 27–28)). The
API terminal: TERM(b21: 613, 620–621) (`^C`, `exit`): V5's API box goes dark; the S09 pytest shell
(the second API terminal, still inside the container) closes in the same beat (`exit`, no capture
line printed). The prod container box stands alone on the cable,
about to start. Nothing else moves.
PONDER(6 s, "The production frontend container\nwon't start while the API is down.\nWhy would a page server care?")
SAY: As an extra, stop it, stop the API too, and start the production container again. It will not start. So, a quick test: why would a page server care whether the API is up?

SHOW: The card leaves. Strip types line 1 of `e01` (extra) → TERM(e01: 8, 11); line 11 `[emerg] … host not
found in upstream "cheese-app-api-service" … default.conf:14` RED. CODE(…/nginx.conf.template: 14)
small, `proxy_pass ${API_URL}` RED; nginx's courier looks up the name in the phone book at start-up
and finds no entry. A GREEN chip "start the API first". Fade; empty frame.
SAY: It exits at once: host not found in upstream. Nginx looks up the proxy target's name when it starts, and the API is gone. Start the API first.

---

## S13 · One command, then clean up — `s13_compose.py` · `ComposeUp`

SHOW: TRACKER [S] 1 (tracker: "README › Tutorial: Setup & Run Cheese App", 6 dots). A README card
(`README.md · line 193`): "Instead of three terminals, one command builds and starts the whole
app." Terminal `laptop`, prompt `student@laptop:~/cheese-app-v2$`: line 1 of `f01` (tag `extra`,
chip "or edit the file") and `git diff src/docker-compose.yml` → TERM(f01: 7, 11–12, 16, 20–21);
the two `+` lines GREEN.
SAY: Instead of three terminals, one command. Step 1: put your project ID into the compose file in src. It appears twice.

SHOW: CODE(cheese-app-v2/src/docker-compose.yml: 7–10) then (…: 18–22) then (…: 34–40) then
(…: 55–63): the four service names TEAL as they appear (`vector-db` 8, `vector-db-loader` 19,
`api-service` 34, `frontend-react` 55), line 22 (the loader's entrypoint) YELLOW with a chip "check ·
load only if empty".
SAY: The file names the same four services. The loader first checks whether the books are already in Chroma, and loads them only if not.

SHOW: TRACKER [S] 2. A README card (`README.md · lines 198–199`). A GREY chip "cd src/vector-db";
prompt `…/src/vector-db$`, types
`docker compose down` → TERM(f02: 2–7, wrap); lines 2–3 GREY (chip "set by docker-shell.sh ·
harmless here"), line 7 `Removed`.
SAY: Step 2: stop whatever still runs, then docker compose down in src, vector db. Compose warns about two unset variables; the shell scripts set them, so this is harmless.

SHOW: TRACKER [S] 3. A GREY chip "cd ../.."; prompt `student@laptop:~/cheese-app-v2$`, types `cd src`
→ TERM(f03: → (no output)); TRACKER [S] 4: `docker compose up --build`. `▶ your turn`.
SAY: Step 3: change into src, and docker compose up with build. Pause and run it.

SHOW: TERM(f04-docker-compose-up: 3, …, 66–68 wrap, 70–76); lines 66–68 (`WARN … network … exists
but was not created by compose`, the volume) ORANGE with a chip "warnings, not errors"; lines
73–76 (`Created`) TEAL, one per container.
SAY: Two warnings: the network and the volume already exist, made by the shell scripts. They are warnings, not errors. Then four containers are created.

SHOW: TERM(f04-docker-compose-up: 98–99, 109, 118, 124, 130); one line per service, each lighting
its box on **V2**'s laptop (Chroma `Saving data to: /data`, uvicorn on 9000, `VITE v8.3.5 ready`,
`vector-db-loader-1 exited with code 0`). On the loader's line, V2's NGINX box Transforms into a TEAL
`vector-db-loader` box that lights and then goes GREY ("exited 0"), with a GREY chip "dev: no NGINX ·
that was S12's image"; the three other boxes light on their lines. Extra: strip line 1 of
`f04-x-compose-ps` → TERM(f04-x-compose-ps: 2–6); `Exited (0)` GREEN. Then a GREY README card
(`README.md · lines 210–211, 215–216`): "Later runs reuse the images and skip the load" · "To open a
shell in a running container, for example to run pytest, run its docker-shell.sh as before".
SAY: Chroma, uvicorn and Vite start together, and the loader exits with 0: it found the books already loaded.

SHOW: TRACKER [S] 5. Strip: line 1 of `f04-curl-3000` (extra) → TERM(f04-curl-3000: 2–3); line 1
of `f04-curl-api-docs` → TERM(f04-curl-api-docs: 2–3). A README card (`README.md · line 213`):
`http://localhost:900/api/docs`, `900` RED (tag `erratum`); extra: line 1 of `f04-x-readme-url` →
TERM(f04-x-readme-url: 2) RED. (No cost tag here: S09 and S11 tagged the chat cost.)
SAY: Step 4: open localhost 3000 and the API docs. A small slip: the README prints port 900; use 9000.

SHOW: TRACKER [S] 6. In the compose terminal: TERM(f04-docker-compose-up: 142–151) (`^C`, the
containers `Stopped`); then `docker compose down` → TERM(f10: 8, 9, 13, 17) (one `Removed` per
container). V2's boxes go dark one by one.
SAY: Step 5: Control C, then docker compose down removes all four containers.

SHOW: TRACKER [C2] 1 (tracker: "README › Docker Cleanup", 2 dots). A GREY chip "cd vector-db"; prompt `…/src/vector-db$`:
`docker compose down` → TERM(e02: 4 from "No resource found"); TRACKER [C2] 2: `docker system
prune` → TERM(e03: 2–8, 9–10, …, 32); `[y/N] y` YELLOW, `cheese-app-network` deleted, `Total
reclaimed space: 4.583GB` GREEN.
SAY: Docker cleanup: compose down in vector db finds nothing left. Docker system prune asks first, then deletes the network and about four and a half gigabytes of build cache.

SHOW: Extra: line 1 of `e04` → TERM(e04: 3–6, …, 13–14); `cheese-app-api-service:latest 4.2GB`
GOLD, `cheese-app-frontend-react-node_modules` ORANGE (tag `erratum` "the cleanup misses it"); a GREY
chip `docker volume rm cheese-app-frontend-react-node_modules` · `docker image rm …`. Fade; empty
frame.
SAY: Prune keeps every tagged image, including the API's image of over 4 gigabytes, and the node modules volume. Remove those by name if you need the disk.

---

## S14 · Tutorial 24 lives on branch 2025 — `s14_branch.py` · `Branch2025`

SHOW: No tracker yet. A GREY branch diagram: `main` (`447b5c3`, folders `api-service`,
`frontend-react`, `vector-db`) and `2025` (`14f2a14`, the same plus `frontend-simple` YELLOW, and
last year's `api-service` with a chip "serves it"). On "disk is tight" a GOLD-outlined "disk" chip:
"branch 2025 builds its own API image · budget about 10 GB more · short on space? `docker image rm
cheese-app-api-service cheese-app-vector-db-cli cheese-app-frontend-react cheese-app-frontend-react:prod`".
SAY: Now Tutorial 24, the lecture's simple frontend. Main dropped it on the recording day; branch 2025 keeps it, with last year's API, which serves it. Branch 2025 builds its own big images: if your disk is tight, remove main's images first.

SHOW: Terminal `laptop`, prompt `student@laptop:~/cheese-app-v2$`, tag `extra` on each line: types
`git switch 2025` → TERM(c01: 2–8); lines 2 and 8 RED, the four file names YELLOW ("your edits").
Then `git stash && git switch 2025` → TERM(c01b: 2 from "WIP on main: 447b5c3", cut after
`447b5c3`, 3–4); line 4 GREEN.
SAY: Git switch 2025 refuses at first: your edits to four files would be overwritten. An extra stash puts them aside.

SHOW: Line 1 of `c02` (extra) → TERM(c02: 2–6); `14f2a14` YELLOW, `frontend-simple` GREEN. Then
line 1 of `c03` (extra) → TERM(c03: 2–3), `llm-service-account.json` YELLOW (tag `erratum`, "the
2025 vector-db script reads this name", CODE(cheese-app-v2-at-14f2a14/src/vector-db/docker-shell.sh:
10) small); then line 1 of `c04` (extra) → TERM(c04: 2–4).
SAY: An extra log shows last year's commit, with frontend simple. Its vector db script wants a second key name, so copy your key under it, and set your project ID again.

SHOW: TRACKER [T23] 1 (tracker: "README @ branch 2025 › Tutorial (23): Vector DB · Backend APIs",
caption "branch 2025 · 14f2a14", 7 dots). Prompt `student@laptop:~$` with a GREY chip "from the
folder above cheese-app-v2". It types `cd cheese-app-v2/src/vector-db` → TERM(c05: → (no output));
TRACKER [T23] 2: `sh docker-shell.sh` → TERM(c06: 3, …, 22–23, 26–30); a GREY chip by the typed line:
"docker-compose: command not found? → docker compose run --rm --service-ports cheese-app-vector-db-cli"
(the 2025 script calls the hyphenated form, `docker-shell.sh:20`); TRACKER [T23] 3: at the
prompt (line 33) `python cli.py --download --load --chunk_type recursive-split` → TERM(c06: 41, …,
197), with S06's counter flashing to **14,356** at once, and a GREY chip "your folder still holds
main's data · output may differ slightly". Extra: line 1 of `c07` (folds) → TERM(c07: 2–3),
`chromadb/chroma:latest` YELLOW with "at the time of recording". Then TERM(c06: 198) (the `exit`).
SAY: Vector DB steps 1 to 3, from the folder above cheese app v2, as the 2025 README spells them, end in the same load: 14,356 chunks. Its Chroma image is tagged latest and still works. Leave with exit; Chroma keeps running.

SHOW: TRACKER [T23] 4. A new terminal strip titled `laptop · new terminal`, prompt `student@laptop:~$`
(the folder that holds both clones): `cd cheese-app-v2/src/api-service` →
TERM(c10: → (no output)); TRACKER [T23] 5: `sh docker-shell.sh` → TERM(c11: 3, …, 20, 21–25, 28–30);
TRACKER [T23] 6: at the prompt (line 32) `uvicorn_server` → TERM(c11: 34–35, …, 49–50, …, 67, 72,
74). `▶ your turn`.
SAY: Backend steps 1, 2 and 4, in a new terminal from the folder that holds both clones: change into the API folder, sh docker-shell.sh, and uvicorn server. Pause and start it.

SHOW: Line 35 `using WatchFiles` YELLOW beside a GREY ghost "StatReload (main)"; lines 49–50
(`Loading CNN Model...`, the model path) and 67 (`Total params`) YELLOW, *before* line 74
`Application startup complete.`; V6's two lamps appear small and GREY dashed with a chip "no
probes yet". A GREY README card tagged "read along · same idea as main" (`2025 README.md · lines
82–86`, step 3 "Review Container Configuration": `-p 9000:9000`, `-e DEV=1`, `docker-entrypoint.sh`)
and one chip "2025 docs: localhost:9000/docs (no /api)" (README:110–113, 140–143).
SAY: Two differences from main: the reloader is WatchFiles, and the model loads before application startup complete, so start-up waits, with no readiness probe.

SHOW: TRACKER [T23] 7. Strip `second tab`: `curl -s -i http://localhost:9000/` (extra) →
TERM(c12: 2, 4, 8). Extra: line 1 of `c13` (folds) → TERM(c13: 2–5, 7); then line 1 of `c14`
(folds) → TERM(c14: 3–9), the `llm-rag` and `llm-agent` lines GREY "still commented out"; two GREY
README cards (`2025 README.md · lines 96–104` and `116–127`) tagged `erratum` "already in the code,
except RAG and agent · don't paste again".
SAY: Then verify localhost 9000: welcome to AC215. A small note: the demo route and the routers the 2025 README asks you to enable are already in the code, except RAG and agent. Don't paste them again, or the route is duplicated.

SHOW: A small API → Gemini arrow carries a GREY model chip "2025's model · us-central1"; on "retired"
the chip is struck RED (tag `erratum`, "with a key, chat fails until the model and region are
updated"); on "main uses" a GREEN chip slides in from a `main` label.
SAY: Also, last year's Gemini model is retired: even with a key, its chat fails until the model and region are updated; main uses a current one.

SHOW: CODE(cheese-app-v2-at-14f2a14/src/api-service/api/service.py: 14–21): lines 15–16
(`add_middleware(CORSMiddleware`) and 18 (`allow_origins=["*"]`) YELLOW; a PINK permission-slip
icon "access-control-allow-origin: *" peels off line 18. Fade; empty frame.
SAY: And what matters next: CORS middleware that allows every origin, the permission slip main no longer needs.

---

## S15 · Last year's pages: CORS and the preflight — `s15_cors.py` · `CorsPreflight`

SHOW: TRACKER [T24] 1 (tracker: "README @ branch 2025 › Tutorial (24): Simple Frontend App", 6
dots). A terminal `laptop · new terminal`, prompt `student@laptop:~$`: `cd cheese-app-v2/src/frontend-simple`
→ TERM(c20: → (no output)); TRACKER [T24] 2: `sh docker-shell.sh` → TERM(c21: 3, …); TRACKER [T24]
3: `http-server` → TERM(c21: 22, 26, 34–36). `▶ your turn`.
SAY: Tutorial 24, step 1: change into cheese app v2, src, frontend simple. Steps 2 and 3: sh docker-shell.sh, then http-server on 8080. Pause and start it.

SHOW: TRACKER [T24] 4. Strip `second tab`: line 1 of `c22` (extra) → TERM(c22: 2–5); the two nav
links YELLOW. The browser drawing (tag `illustration`) at `localhost:8080/index.html` with links
"Newsletters", "Cheese Assistant".
SAY: Home page: open index dot html. The landing page links to two more pages: newsletters and chat.

SHOW: TRACKER [T24] 5. LECTURE 18 · 24–26 (Frontend). Strip: line 1 of `c23` → TERM(c23: 2, 7–8);
the axios script and `newsletters-main.js` YELLOW. Extra: line 1 of `c24` → TERM(c24: 2–3);
`baseURL: 'http://localhost:9000'` PINK. **V1**, B24–B26 exactly: the page arrives from the 8080
box (first trip), then its JavaScript fires a second PINK arrow straight at the laptop's `9000` door.
SAY: Newsletter feature: open newsletters dot html. Its script names the API: localhost 9000. This is the lecture's second trip: the page came from 8080, and its JavaScript calls 9000 itself.

SHOW: The origin label of the page `http · localhost · 8080` and of the target `http · localhost ·
9000` sit side by side; the port chips differ (RED outline): "different origin". The browser
window grows an ORANGE checkpoint on its outgoing arrow, "did the server allow this origin?".
SAY: Same laptop, different port, so a different origin. Now the browser checks every answer: did the server allow this origin?

SHOW: Extra: line 1 of `c25` (folds) → TERM(c25: 2–7, wrap); both `access-control-allow-origin: *`
YELLOW; the checkpoint opens GREEN.
SAY: An extra curl sends what the browser sends. The API answers with access control allow origin, star: permission granted.

SHOW: On V1, arrow 1 makes a small PINK U-turn labelled `307` (`/newsletters` → `/newsletters/`).
The uvicorn strip: TERM(c11: 79–80); `307` PINK, `200` GREEN. A small GREY card "slides 24–26:
/newsletters · the router: /newsletters/" (tag `erratum`).
SAY: First comes 307, then 200: the paths differ by one slash, an extra round trip.

SHOW: TRACKER [T24] 6. LECTURE 18 · 27 (Frontend). Strip: line 1 of `c26` → TERM(c26: 2, 4–6). The
browser drawing at `chat.html`, a text box "How is cheese made?" (README:180). V1 with B27's six
steps, and a new circle **0** before 1: a small PINK `OPTIONS` scout leaves first.
SAY: Chat feature: open chat dot html and ask how cheese is made. Now the browser adds a step the lecture never draws: step zero, the preflight.

SHOW: Extra: line 1 of `c27` (folds) → TERM(c27: 2–6); `access-control-allow-headers:
content-type,x-session-id` YELLOW, `access-control-max-age: 600` PINK (tag `extra`, not labelled "exactly what the browser sends": it
preflights `/llm/chats`; CORSMiddleware answers any preflight before routing, so the headers are the
same). The scout, drawn with the page's URL `/llm/chats/`, returns with a badge; only then does the
POST (step 1) leave.
SAY: A JSON post with a custom header makes the browser ask first, with an OPTIONS request. The answer allows any origin, these methods and these two headers, for 600 seconds.

SHOW: The uvicorn strip: TERM(c11: 81–82, 85 wrap, …, 146); `OPTIONS /llm/chats … 200` GREEN,
`POST /llm/chats/ … 307` PINK, line 146 `500` RED. Extra: line 1 of `c28` (folds) → TERM(c28: 2, 6–8,
13–14 wrap); line 13 `access-control-allow-origin: *` YELLOW on the 500.
SAY: The log: OPTIONS 200, then the post bounces with 307 and ends in 500, the same Gemini error. That 500 carries the permission header too, so the browser shows the real error.

SHOW: LECTURE off. Two panels side by side with neutral captions: "2025: page on 8080 → API on
9000" (V1 with step 0, ORANGE checkpoint) and "main: page on 3000 → Vite → API" (V1 with the Vite
courier, no checkpoint). No origin labels, no "ask permission" or "one origin" words. Under both a
GREY line: "CORS: the browser's rule, about the server's permission · curl and /api/docs never see it".
SAY: So CORS is the browser's rule about the server's permission; curl and the docs page never meet it.

SHOW: The two panels freeze. Nothing else moves.
PONDER(8 s, "Last year's page needed CORS.\nThis year's React app does not.\nWhat changed: the API,\nthe browser, or the origin it calls?")
SAY: So, a quick test. Last year's page needed CORS, and this year's React app does not. What changed: the API, the browser, or the origin it calls?

SHOW: The card leaves. The full captions write on now: "· ask permission" on the left, "· one
origin" on the right. On the right panel, the page's origin and the call's origin glow as one PINK
label; the left panel's two labels separate. A GREY chip on the right API box: "middleware dropped:
nothing needs it".
SAY: The origin. The React page calls its own origin, and a proxy forwards: nothing to permit. The API then dropped the middleware, because nothing needed it.

SHOW: Both 2025 terminals: TERM(c21: 45–46, 48–49) and TERM(c11: 147, 152–155) (`^C`, `exit`).
Extras: line 1 of `c30` → TERM(c30: 2); a GREY chip "cd ~/cheese-app-v2", then at the explicit prompt
`student@laptop:~/cheese-app-v2$` line 1 of `c31` → TERM(c31: 2–4, line 4 cut after `447b5c3`);
a GREY chip `git stash pop` "restores your earlier edits, if you want them" (typed, no output: not
captured). Fade; empty frame.
SAY: To stop, Control C and exit in both terminals. As extras, stop last year's Chroma, discard the branch's edits and switch to main; git stash pop restores yours.

---

## S16 · Tear down, recap, and what's next — `s16_recap.py` · `Recap`

SHOW: No tracker. A GOLD-outlined checklist card "Clean up · all done once already", one line per
phrase, each ticking GREEN on it: "Ctrl-C and exit in every container terminal (--rm deletes them)",
"docker compose down · src/vector-db, or src if you used Compose", "branch 2025: stop its Chroma,
git switch main", "docker system prune · check its list first (other projects too)", "what prune
keeps: docker volume rm cheese-app-frontend-react-node_modules · docker image ls, then remove the
cheese-app-* and chromadb images by name if you need the space" (GOLD "disk" chip), "your key stays
in secrets/, outside every repository".
SAY: Before you go, a cleanup checklist, all done once already. Exit every container, compose down, back to main, prune after checking its list; then remove the node modules volume and big images by name. Your key stays in secrets.

SHOW: The card fades. **V1 as the whole trip on main**, one hop per phrase: the browser at
`localhost:3000/newsletters`; door `3000 → 5173`; the courier box showing "Vite" with "nginx"
beneath it (dev / prod); the courier walking the GREEN cable by name to uvicorn (`0.0.0.0:9000`);
FastAPI's `/api/newsletters` router leaf (V4 mini) runs. The JSON comes back the same way and one
PINK origin label covers page and call. S01's YELLOW card "Who carried it?" returns and is ticked
GREEN.
SAY: Here is the whole trip, with the hook answered: the browser talks only to 3000. Inside, Vite in development or nginx in production carries slash api by name to uvicorn on 9000, where a router runs the function. The JSON comes back the same way: one origin, no permission needed.

SHOW: LECTURE 18 · 19–21 (APIs). The trip shrinks. **V2** one last time: the laptop's four TEAL boxes
rise back into the lecture's cluster; NGINX (seen in S12), Artifact Registry and the persistent disk
light GREY dashed with chips "Lectures 19–22". The struck-through "App is ready!" returns, its
caption "we need to build it" now with a small GREEN tick beside "the pieces".
SAY: Back to the lecture's blueprint. Your four boxes rise into the cluster. NGINX in front, the registry and the persistent disk are still dashed: the next lectures build them.

SHOW: LECTURE 18 · 46 (APIs), then LECTURE 18 · 40–41 (Frontend). A GREY card "your project: draw
your solution and technical architecture", then two GREY repo chips "App Building Crash Course",
"App Building Template" (names only, no URLs).
SAY: For your project, the lecture asks you to draw your solution and technical architecture, and points to a crash course and a template repository.

SHOW: LECTURE off. A YELLOW "Test yourself" card, question 1 of 5 (answers in `exercises.md`):
"Trace one newsletters request on main through the lecture's steps. Which container does the browser
talk to, and at which step does the API's port come in?" A small V1 outline beside it, hops
unnumbered; on "browser" the browser pulses once.
SAY: Test yourself, pausing on each. One: trace a newsletters request on main. Which container does the browser talk to, and where does port 9000 come in?

SHOW: Question 2 (a small V3 icon; the three parts pulse in turn): "What do api.service:app,
--host 0.0.0.0 and --reload each do, and why does /square_root answer 307?"
SAY: Two: what do api dot service colon app, host 0.0.0.0 and reload each do, and why does square root without a slash answer 307?

SHOW: Question 3 (V6's two lamps, each pulsing once): "/healthz vs /readyz: what does each one check
in this API?"
SAY: Three: healthz and readyz. What does each one check in this API?

SHOW: Question 4 (a small GREEN file icon that pulses on "copy"): "Where does a chat stay between two
messages, and why can any copy of the API answer it?"
SAY: Four: where does a chat stay between two messages, and why can any copy of the API answer it?

SHOW: Question 5 (two small courier icons "Vite", "nginx" and a permission slip, each pulsing once):
"Which file decides where /api goes in development, which in production, and why did the 2025 API
need CORSMiddleware while main's does not?" A GREY chip "answers: exercises.md". Fade out; empty
frame.
SAY: Five: which file decides where slash api goes in development, which in production, and why did last year's API need CORS while main's does not?
