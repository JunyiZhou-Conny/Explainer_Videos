# AC215 · Lecture 16 — System Tradeoffs: networking, runtime config and capacity (with L10) (exam edition) — narration script & visual plan (v2: accuracy + exam reviews merged)

Audience: an AC215 student the day before Quiz 4. They sat Lectures 10 and 16 (or skimmed them), have run the cheese
app's containers on their laptop (`docker-shell.sh`, `localhost:9000`, the `secrets/` folder), and may never have
deployed anything into a VPC. They watch on a laptop with no clone open, to prepare for conceptual multiple-choice
questions, not to type along.

Goal (BRIEF.md "Audience and goal"): after the video they can answer conceptual questions on these lectures **and say
why each wrong option is wrong**: (1) laptop vs cloud — `localhost` is the machine the code runs on, a private IP
(10.x, 172.16–31.x, 192.168.x) is not routed on the internet, a port picks the service, `0.0.0.0` listens on every
interface, the public reaches a DNS name → load balancer :443 → private target :8000, a security group is an inbound
allow-list and is stateful; (2) VPC routing — a CIDR block cut into subnets, the public route table sends `0.0.0.0/0`
to the Internet Gateway and the private one to a NAT Gateway, both send `10.0.0.0/16` to `local`, the most specific
match wins; (3) NAT — translate out, remember the mapping, map replies back, accept nothing unsolicited; NAT down →
internet egress fails, VPC-internal traffic (the database, the ALB to the tasks) still works; (4) the browser is
outside the VPC — frontend JavaScript calls the public HTTPS endpoint (or a relative path the front door routes),
never `localhost` or `10.x`; NAT does not help inbound; (5) build once, configure at startup — one immutable image
promoted unchanged, runtime values and authorized secrets injected at startup (secret manager; on the laptop a mounted
`secrets/` folder + `GOOGLE_APPLICATION_CREDENTIALS`), never in the image, the source or Git; (6) capacity — max
replicas = ⌊(DB connection limit − other clients) ÷ connections per replica⌋, set as the autoscaler's max; (7) data
store — relational + vector needs in one managed database → PostgreSQL + pgvector.

Sources of truth: `BRIEF.md` (design, binding); the **Lecture 16 deck** text (81 slides; PDF page numbers; the
primary source; there is no L16 `SLIDES.md` or digest), cited `lecture_ref(16, …)`; the **Lecture 10** digest
`../ac215-l10-cloud-connect/SLIDES.md` (55 slides; PDF page numbers) and the tutorial digest
`../ac215-l10-cloud-connect/digest.md`, cited `lecture_ref(10, …)`; the study guide
`MLOps_Learning/guides/L10-cloud-connect-cheese-app-v0.md`; `assets/source/<repo>/<path>`, the files at the commits in
`video.yaml` (`cheese-app-v0@cb6fb94`, `cheese-app-v2@14f2a14`). Where the slides and the repo differ, the panel shows
the repo and the SAY says what each shows, in one clause (S02: the lecture's FastAPI on :8000 and `-p 8080:8000`, the
course repo's :9000 and `-p 9000:9000`; S05: the key file name; S06: ChromaDB stands in for a SQL connection pool).

Conventions
- **Exam edition.** No README tracker, no `▶ your turn`, no terminal captures, no typed commands, no `recorded` or
  `expected` output boxes, **no live runs**: this lecture's video runs nothing. Every mechanism is an animated diagram
  (V1–V6, BRIEF.md "Visual set pieces"); code and README panels are evidence beside it. Every mechanism scene (S02–S07)
  ends with a YELLOW **takeaway card** "If the question says X → think Y" (one visual group, centred lower third),
  spoken as the scene's last SAY, then an empty frame. S08 collects the seven rules.
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most about 55
  words; ponder answers and the recap may run a little longer) and become the subtitles. Plain spoken English: no
  backticks, no symbols, no markdown. Identifiers are on screen and said in words: `localhost:9000` → "localhost
  9000", `-p 9000:9000` → "dash p, 9000 to 9000", `0.0.0.0` → "0.0.0.0" (the voice reads it "zero dot zero dot zero
  dot zero"; check), `0.0.0.0/0` → "0.0.0.0 slash 0", `10.0.0.0/16` → "10.0.0.0 slash 16", `/24` → "slash 24",
  `api.example.com` → "api dot example dot com", `/api` → "slash api", `NEXT_PUBLIC_BASE_API_URL` → "next public base
  API URL", `GOOGLE_APPLICATION_CREDENTIALS` → "Google Application Credentials", `os.environ` → "os dot environ",
  `/secrets` → "slash secrets", `myapp:v1.4` → "my app, version 1.4", `LOG_LEVEL=debug` → "log level debug",
  `APP_ENV` → "app env", `.gitignore` → "git ignore", `proxy_pass` → "proxy pass". IP addresses are written as
  digits with dots (as L02 did with 127.0.0.1); Kokoro reads `10.` as a sentence end and the rest as decimals, so
  `explainer/lexicon.yaml` (block `# AC215 L16-exam`) carries "dot" readings for `10.0.0.0`, `10.0.2.5`, `10.0.3.7`,
  `192.168`, `172.16`, `172.31` and reads `NAT` as "nat" (no `say=` override needed; `0.0.0.0` is read correctly).
  Never write "NAT's" or "10.0.2.5's" (lexicon words take no `'s`). The option letter "A" is always followed by a
  comma in a SAY ("A, the Internet Gateway, would …"), or Kokoro reads it as the article. Numbers as
  digits; a number that matters gets its own short sentence ("Divide by 15."). No "!" after a digit. Times as "9 in
  the morning", never "a.m.".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits only there;
  the split drives the TTS gaps, the subtitle cues and the one-to-one Chinese alignment). No sentence opens with a
  lower-case identifier or file name. No `'s` after a digit or on a word with a lexicon entry. No abbreviations with
  inner dots ("e.g.", "vs.") in SAY. American spelling on screen and in the SAY ("gray", "neighbor"; the colour
  constants stay GREY).
- **Names.** The instructor's full name never appears, spoken or on screen (neither deck's title page is redrawn).
  The SAY says "the lecture" or "the slides"; commit authors and README persona chips are "the course staff". Never
  shown: `cheese-app-v0/README.md:20-21`, `:36`, `:232-249`. The quoted ranges contain no person's name (checked:
  `cheese-app-v0/api-service/docker-entrypoint.sh:6-9`, `docker-shell.sh:19-27`, `README.md:173-175`,
  `frontend-ai-chatbot/.env.development:4`, `.env.production:2`, `src/services/Common.js:2`;
  `cheese-app-v2/src/api-service/docker-shell.sh:23-33`, `api/utils/llm_rag_utils.py:18-25`, `:56-57`,
  `src/vector-db/docker-compose.yml:19-28`, `README.md:25`).
- **No secrets.** No credentials, keys, project numbers or endpoint ids. Never quote `cheese-app-v0`'s
  `api-service/api/routers/rag.py`; never open `cheese-app-v2`'s `.env.development` / `.env.production` (neither is in
  `assets/source/`). The secret in V4 and in P2 is a GOLD key glyph or `…`, never a value. `ac215-project` appears
  only where it sits on the same line as "CHANGE TO YOUR PROJECT ID" (no panel below quotes that line).
- `SHOW:` lines describe what is on screen during that SAY, and what moves. ≤ 3 visual groups at once; something moves
  every ~4 s except during ponder timers.
- `Lecture: …` under a scene header lists the slides the scene stands on, per deck. `LECTURE 16 · a–b` in a SHOW line:
  from that SAY block on, the GRAY `lecture_ref(16, "a–b")` tag sits top right ("Lecture 16 · slides a–b"; "slide" for
  one) until a SHOW changes it; `LECTURE 10 · a–b` likewise with `lecture_ref(10, …)`. One tag at a time: where a scene
  stands on both decks, the tag switches to L10 while the L10 idea is on screen and back after. S01 explains the tag
  once. The slides are never shown: every lecture picture is our own redrawing in the series colours with the slide's
  structure and terms (L10 slide 11's table, L16 slide 13's two route tables, slide 14's NAT path, slide 16's three
  subnets, slide 27's numbered DNS path, slide 64's two request paths, slide 21's one image with two value cards,
  slide 22's secret manager, slide 52's four boxes, slide 76's triptych); no slide image, meme, QR code, logo (AWS,
  Google Cloud, Nginx, Docker, PostgreSQL, ChromaDB) or console screenshot.
- **The lecture draws AWS; the course runs on GCP.** On screen the AWS-style names of the lecture's picture (VPC,
  subnet route tables, Internet Gateway, NAT Gateway, ALB, ECR, Route 53), with a small GRAY chip "the lecture's
  picture (AWS names)" the first time each diagram appears. S02 names the GCP neighbors once (slide 59; slide 68 in
  S07). Never say GCP subnets have their own route tables, or that Cloud NAT is a route's next hop.
- `CODE(repo/path: a–b)`: `code_panel(...)` quoting `assets/source/repo/path` from line a to b with the real line
  numbers, header `path · lines a–b` (the repo name kept as the first path segment, since both repos share file
  names: `cheese-app-v0/api-service/docker-shell.sh · lines 19–27`). At most 12 rows on screen; a longer range is
  shown *folded* (only the listed lines, a GRAY `…` row between gaps, header suffix `(folded)`). Lines longer than 65
  characters wrap (continuation rows indented, a GRAY ↪). Lit lines: a YELLOW bar behind the named line(s) unless the
  SHOW names another colour. An *excerpt chip* quotes an exact sub-string of one line, headed `path · line N
  (excerpt)`.
- **Renamed on copy.** `cheese-app-v0/frontend-ai-chatbot/.env.development` and `.env.production` are stored as
  `assets/source/cheese-app-v0/frontend-ai-chatbot/env.development` and `env.production` (the repo `.gitignore`
  ignores `.env.*`); content unchanged. Their panel headers show the real path:
  `cheese-app-v0/frontend-ai-chatbot/.env.development · line 4`.
- `PANEL(repo/README.md: a–b)`: a README text panel (same frame as a code panel, markdown shown as plain text, `**`
  and backticks stripped, link targets dropped, line numbers kept), header `repo/README.md · lines a–b`.
- **Invented examples** (the hook's alarms, the ponders, S06's 100 slots, S07's tables and SQL, the baked Dockerfile
  line in S05) are drawn on GRAY-outlined cards or schematic canvases with the tag `illustration`, never with a
  `path · lines` header, never in the repo-panel frame. Names are the lecture's own placeholders: `api.example.com`,
  `app.example.com`, `myapp:v1.4`, `api-alb`, `fastapi-tg`, `10.0.2.5`, `34.120.45.67` (slide 4's public IP).
- `PONDER(10 s, "question")`: the multiple-choice ponder (`mcq_ponder`). The SHOW before it gives the card: a YELLOW-outlined
  card in the lower two thirds with the question, four option rows A–D (letter in a circle) and a 10-second YELLOW
  timer bar that drains; tag `illustration`. The SAY that introduces it reads the stem (not the options) and ends
  "Pause here if you want." Answers are C (P1), D (P2), B (P3); option lengths kept balanced. Nothing on
  screen during the timer shows the answer. The next SAY block reveals: the right row fills YELLOW with a ✓; under each
  wrong option a one-line RED reason writes in (text given in the SHOW) as the SAY reaches it; then the card fades.
  Three in the video: P1 (S03), P2 (S05), P3 (S06), all new (BRIEF.md "Ponder questions"); the practice questions
  Q14–Q18 are never quoted, paraphrased or answered, and their numbers never appear.
- `TAKEAWAY: "…"`: the scene's YELLOW takeaway card, written in as its SAY speaks it; in S08 it returns as one of the
  seven rule rows.
- Packet glyph, the same everywhere: a small envelope with `src → dst` printed on it (e.g. `10.0.2.5:52134 →
  34.x:443`); the field that changes (NAT's source rewrite) flashes YELLOW, then settles. The ALB does not rewrite a
  packet: it ends the HTTPS connection and sends a new HTTP envelope (source = the ALB, destination = the task :8000). A
  dropped packet turns RED and evaporates; a refused connection sparks RED.
- Semantic colours (BRIEF.md "Colours"; series table applied):

  | meaning | colour |
  | --- | --- |
  | your laptop and the visitor's machine: the browser, `localhost` / `127.0.0.1`, the host side of `-p 9000:9000`, the laptop's `secrets/` folder | GREY |
  | the cloud: the VPC box (`10.0.0.0/16`), its subnets (public solid outline; private the same BLUE with a small padlock), the Internet Gateway, the NAT Gateway, the ALB, Route 53 (only; the public resolver is ORANGE), the managed PostgreSQL service, the secret manager | BLUE |
  | containers and images: `myapp:v1.4` (one image, one digest), FastAPI tasks / replicas, the ChromaDB container, the registry shelf | TEAL |
  | shared, not yours: the public internet cloud, the public DNS resolver `1.1.1.1`, OS-chosen ephemeral source ports (`:52134`), other clients holding database connections (the admin console, a batch job) | ORANGE |
  | what the project owns and sets: runtime values per environment (`APP_ENV`, `LOG_LEVEL`, `FEATURE_FLAG`), the app's schema (users, orders, FK lines), the replica's own connection pool | GREEN |
  | tools: Docker, uvicorn, Nginx, the autoscaler (signal → policy), the pgvector extension | PURPLE |
  | failures and "avoid this": a dropped packet, `too many connections`, a key baked into an image layer, a `10.x` or `localhost` URL in browser code, the reason under a wrong option | RED |
  | "look here now": the packet in flight, the route row being matched, the ponder card and timer, the takeaway cards | YELLOW |
  | money and secrets: the secret's key glyph (never a value), the DB tier's price tag | GOLD |
  | routes and lookups: route-table rows, DNS lookup arrows, request paths, the NAT mapping table, the connection pipes from replicas to the database | PINK |
  | outside this lecture (Kubernetes details, multi-AZ, CDN internals) | GREY dashed |

- Visual set pieces V1–V6 (BRIEF.md) live in `scenes/common.py`: `Packet` (the envelope), `Host` (laptop / VPC box
  with subnets), `RouteTable` (PINK rows, a YELLOW match bar), `NatNotebook` (V2), `TwoPaths` (V3), `ImageConveyor` +
  `LayerStack` (V4), `SlotGrid` + `Autoscaler` (V5), `ChipSorter` (V6), plus `mcq_ponder(...)`, `takeaway(...)`,
  `illustration_card(...)` and `lecture_ref`.
- Running example (BRIEF.md "Running example"): browser → `api.example.com` → ALB in the public subnet `10.0.1.0/24`
  → FastAPI tasks in the private app subnet `10.0.2.0/24` (one at `10.0.2.5:8000`, slide 4) → PostgreSQL at
  `10.0.3.7` in the private data subnet `10.0.3.0/24`; outbound calls to an external LLM API (`34.x:443`, ORANGE)
  through the NAT Gateway; the static frontend from `app.example.com`. On the laptop: FastAPI on `0.0.0.0:9000`,
  `-p 9000:9000`, the frontend on `localhost:3200` calling `http://localhost:9000`, the key mounted at `/secrets`.

Notes for scene authors
- **Ports: slides vs repo.** The L16 deck's FastAPI listens on `0.0.0.0:8000` and publishes with `docker run -p
  8080:8000 myapp:v1.4` (slides 18–19); the course repo's API listens on `0.0.0.0:9000` and publishes `-p 9000:9000`
  (`cheese-app-v0/api-service/docker-entrypoint.sh:7`, `docker-shell.sh:20`). S02 shows the repo on the laptop and the
  lecture's :8000 in the cloud picture, and says so once. L10's slide 9 tunnel uses 8090 → 9100 (the Containers II
  toy); we draw the tunnel with the repo's 9000 → 9000 and do not quote L10's numbers.
- **Key file names differ.** L10 slide 42 mounts `data-service-account.json`; `cheese-app-v0` points
  `GOOGLE_APPLICATION_CREDENTIALS` at `/secrets/llm-service-account.json` (`api-service/docker-shell.sh:10`, not
  quoted); `cheese-app-v2` at `/secrets/ml-workflow.json` (`src/api-service/docker-shell.sh:29`, quoted in S05). The
  mechanism is identical; S05 shows v2's line and never names a file in the SAY.
- **S06's stand-in.** `llm_rag_utils.py:57` creates a ChromaDB `HttpClient` at import, one per API process. It is not
  a PostgreSQL pool and holds HTTP connections, not database sessions; the SAY says "stands in for". A GRAY chip on
  the panel: "the course's vector DB client · stands in for a SQL connection pool".
- **NEXT_PUBLIC.** That `NEXT_PUBLIC_` variables are inlined into the browser bundle at build time is Next.js
  behaviour, not on the slides; S04 says it as a plain fact in one sentence, with no lecture tag change.
- **S04's relative `/api`.** `.env.production:2` sets `NEXT_PUBLIC_BASE_API_URL=/api`. The repo does not contain the
  front door that routes `/api` (its Nginx/ingress config arrives in later lectures); S04 shows the routing as slide
  24's rule (Nginx `location /api/ { proxy_pass http://10.0.2.5:8000; }` = ALB `path /api/* -> fastapi-tg`) and slide
  32's layout B, tagged `lecture's picture`, never as a repo panel.
- **Stateful firewall vs NAT.** Slide 9/11's stateful firewall (replies to an allowed connection come back) and slide
  14's NAT mapping (replies are mapped back to the private address) are separate ideas; draw the first as a gate on the
  task (S02), the second as the notebook at the NAT Gateway (S03). Never merge them.
- **Slide subtleties:** route rows read `10.0.0.0/16 → local route` (slides 13–14); the public route is "necessary,
  not sufficient" (slide 13 caption); slide 52's caption "Downstream limits still bound the result"; slide 68's "High
  availability and recovery are configurations — not defaults"; slide 80's order "Trace the request · Name the
  contract · Choose the boundary · Select a service · Measure and revise".
- **V5 numbers (illustration):** 100 slots; ORANGE other clients 10 (admin console 4, batch job 6); pools of 20 → 4
  replicas fit (80 + 10 = 90; a fifth needs 20 more, only 10 free → RED). These are not the practice question's
  numbers (Q16 is never echoed) and not P3's.
- **P3 numbers:** pools of 15, other clients 30, 10 replicas at peak → 180 needed; tiers 150 / 200 / 250 / "keep 100
  + raise max"; answer 200. (Changed from BRIEF.md's P3 by the exam review M3: the forward computation is V5's, so the
  ponder tests the same rule from the tier side.)
- **Buildability (exam review S13).** `explainer.devops` gives `laptop`, `server`, `cloud`, `box`, `chip`, `tag`,
  `lecture_ref`, `check_mark`, `cross_mark`, `browser_window`, `layer_bar`, `file_glyph`, `folder_glyph`, `code_panel`;
  `explainer.components` gives `connect` and `database_rows`. `Packet`, `RouteTable`, `NatNotebook`, `SlotGrid`,
  `ChipSorter`, `mcq_ponder`, `takeaway` do not exist yet: write them in `scenes/common.py` first. S05's folded panel
  needs L08's `src_panel(path, [23, 25, 27, (29, 33)])` (raises on > 12 rows). PANEL(cheese-app-v2/README.md: 25) wraps
  to ~5 rows: find the lit clause with L08's `wrap_output` + `wrapped_glyphs`. The S02 excerpt chip is
  `code_span(code, 1, "--host 0.0.0.0 --port 9000")` on the 6–9 panel. The CIDR counter is plain `Text`
  ("2¹⁶ = 65,536"), not MathTex.
- Words that may need lexicon entries (checked with `explainer/voice.py`; block `# AC215 L16-exam` in
  `explainer/lexicon.yaml` holds the IP addresses and NAT): VPC, CIDR, NAT, ALB, DNS, pgvector, PostgreSQL,
  ChromaDB, uvicorn, FastAPI, Nginx, AlloyDB, autoscaler, localhost, SSH, HTTPS, "os dot environ", "git ignore",
  the IP addresses above. No sentence says "a" directly before one of these words if its entry starts with a vowel
  sound ("an SSH"). Never "a NAT" in a SAY: Kokoro reads "a" before a lexicon word as the letter A, so write "the NAT
  Gateway".
- i18n `en_display` candidates (spoken → literal): localhost 9000 → `localhost:9000`; dash p, 9000 to 9000 → `-p
  9000:9000`; api dot example dot com → `api.example.com`; slash api → `/api`; next public base API URL →
  `NEXT_PUBLIC_BASE_API_URL`; Google Application Credentials → `GOOGLE_APPLICATION_CREDENTIALS`; os dot environ →
  `os.environ`; slash secrets → `/secrets`; my app, version 1.4 → `myapp:v1.4`; log level debug → `LOG_LEVEL=debug`;
  git ignore → `.gitignore`; proxy pass → `proxy_pass`; slash 16 → `/16`.
- Word budget (BRIEF.md, ±15 %): S01 170 · S02 300 · S03 380 · S04 280 · S05 320 · S06 260 · S07 230 · S08 170 =
  2,110 (allowed 1,800–2,300).

---

## S01 · Launch day: three alarms — `s01_launch.py` · `LaunchDay`

Lecture: L16 71; L10 4.

SHOW: Cold open, no lecture tag. Tag `illustration`. Left: a GREY laptop with a small TEAL container box "cheese
app". A curved arrow carries the box right into a BLUE VPC map (slide 71's layout plus slide 16's NAT Gateway, our
redrawing: a GREY browser at the top, a BLUE ALB, TEAL FastAPI tasks, a BLUE database, a BLUE NAT Gateway at the edge). A GRAY clock chip "launch
morning · 8:00".
SAY: Launch day for the Cheese App. Last week it ran on a laptop. This morning it runs in the cloud, inside a private network. Within an hour, three alarms go off.

SHOW: Alarm 1: a RED bell over the NAT Gateway. A chat bubble "asking the language model…" shows a RED timeout clock;
below it, "chat history" loads from the database with a GREEN ✓.
SAY: First alarm. Chat answers that call an outside language model time out. Yet the saved chat history, read from the database, loads fine.

SHOW: Alarm 2: a RED bell over the browser. The page renders (GREEN ✓ on "page"), but its "Predict" button spins
briefly, then shows a RED "Network Error". Beside it, a small GREY laptop thumbnail labelled "developer's laptop" with
the same button and a GREEN ✓.
SAY: Second alarm. The page loads for every visitor, but the Predict button fails. On the developer's laptop, the same button worked.

SHOW: Alarm 3: the clock chip flips to "9:00". A GRAY traffic line doubles; three new TEAL replicas pop in next to the
first three; the fourth connects (GREEN ✓), the fifth and sixth flash RED labels `too many connections` (tag
`illustration`); a GRAY CPU gauge beside them reads low.
SAY: Third alarm. At 9 in the morning traffic doubles, and the autoscaler adds replicas. The newest ones fail with too many connections, while their processors sit idle.

SHOW: A quieter fourth marker: the TEAL image glyph on a registry shelf is X-rayed; a GOLD key glyph glows inside one
layer, outlined RED. No bell.
SAY: And one problem nobody has noticed yet. The production key is sitting inside the container image.

SHOW: The map shrinks to the top. The plan builds left to right as the SAY names each item, six small icons with
labels: "addresses" (a house with a door), "routes and NAT" (two PINK rows), "the browser" (a GREY window), 
"configuration" (a TEAL image and GREEN cards), "capacity" (a grid of slots), "the database" (a BLUE cylinder).
SAY: Each alarm is one mechanism from Lectures 10 and 16. We go from addresses, to routes and NAT, to the browser, to configuration, to capacity, and finally to the database.

SHOW: A GRAY specimen tag "Lecture 16 · slide 71" pulses once top right; a GRAY code-panel header specimen
`cheese-app-v0/api-service/docker-shell.sh · lines 19–27` pulses once; a GRAY chip "no live runs · concepts, not
clicks". Then an empty frame.
SAY: The gray tag, top right, names the slides behind each idea. Nothing here is a live run.

---

## S02 · From localhost to a front door — `s02_address.py` · `LaptopToCloud`

Lecture: L10 4–11; L16 3–4, 8–11, 18–20, 27, 59.

SHOW: LECTURE 10 · 9. V1 begins. A GREY laptop holds a sealed TEAL container; inside, a PURPLE "uvicorn" chip and a
TEAL "FastAPI" box with a door labelled `:9000`. Right: CODE(cheese-app-v0/api-service/docker-entrypoint.sh: 6–9),
line 7 lit, the excerpt `--host 0.0.0.0 --port 9000` underlined YELLOW. The container's outline shows several small
"interface" sockets, and `0.0.0.0` draws a YELLOW bracket around all of them; then a second, RED bracket closes around
only the inner `127.0.0.1` socket, chip "loopback · only this container"; it dissolves.
SAY: Start on the laptop. In the course app, uvicorn starts FastAPI inside a container, on host 0.0.0.0, port 9000. That host means listen on every interface. Bound to 127.0.0.1 instead, it would answer only from inside the container.

SHOW: The panel Transforms to CODE(cheese-app-v0/api-service/docker-shell.sh: 19–27), line 20 lit. A PINK tunnel draws
from a GREY door "laptop :9000" through the container wall to the TEAL door ":9000". A GREY browser packet `→
localhost:9000` loops inside the laptop, through the tunnel, and reaches FastAPI (GREEN ✓).
SAY: The container is sealed off until you publish a port. Dash p, 9000 to 9000, is the tunnel from the laptop's door into the container's.

SHOW: The panel Transforms to PANEL(cheese-app-v0/README.md: 173–175), lines 174–175 lit. A GREY label "localhost =
this machine" writes over the laptop.
SAY: So the README says the app is served at localhost 3200, and it calls the API at localhost 9000. Localhost always means this machine: the one the code runs on.

SHOW: LECTURE 16 · 4, 8. The panel fades. A street of BLUE house outlines with numbers; one house, its doors labelled
`:8000`, `:5432`. Two labels: "IP address = street address → picks the machine", "port = door → picks the service".
Then a small table writes in (slide 8): `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` under the header "private
(RFC 1918)", and `34.120.45.67` under "public".
SAY: An IP address picks the machine, and a port picks the service on it. Addresses that start with 10, with 192.168, or with 172.16 through 172.31 are private. The internet does not route them.

SHOW: LECTURE 16 · 4, 18. The laptop dissolves; the same TEAL box lands in a BLUE VPC box, in a private app subnet,
with the address `10.0.2.5` and the lecture's door `:8000`. A GRAY chip: "lecture: :8000 · course repo: :9000". An
ORANGE internet cloud at the left sends a packet `→ 10.0.2.5`; it hits the internet edge and evaporates RED.
SAY: Move the same container into the cloud. Inside the private network it gets the address 10.0.2.5. A packet from the internet cannot reach it: nobody out there has a route to a private address.

SHOW: LECTURE 10 · 11. Lecture 10's table redrawn: three rows (address · who can reach it · getting traffic in), two
columns. The laptop column ("private address · your router keeps the world out") morphs cell by cell into the cloud
column: "public IP and DNS name", "firewall closed by default", "load balancer out front".
SAY: Lecture 10 sums it up. On the laptop, your router keeps the world out. In the cloud, the public finds you by a DNS name, a firewall starts closed, and a load balancer lets traffic in.

SHOW: LECTURE 16 · 27. Slide 27's numbered path, redrawn: GREY browser `api.example.com` → (1) an ORANGE public resolver `1.1.1.1` → (2)
BLUE "Route 53" (authoritative) → (3) the ALB's IP back → (4) to the browser; then (5) a PINK HTTPS arrow to the BLUE
ALB `api-alb` in the public subnet `10.0.1.0/24`. The packet's destination field reads `ALB-IP:443`.
SAY: The browser asks a resolver for api dot example dot com, the resolver asks the authoritative DNS, and the load balancer's public address comes back. Then the browser connects to the load balancer on port 443.

SHOW: LECTURE 16 · 11, 20, 26. At the ALB the HTTPS envelope opens (GRAY chip "TLS ends here", slide 26) and the ALB
sends a new HTTP envelope: source flashes YELLOW to `ALB 10.0.1.x`, destination to `10.0.2.5:8000`; it enters the
private app subnet and stops at a GRAY gate in front of the task: the rule card "allow · TCP 8000 · source: ALB"
(slide 11's rule, with slide 24's ALB in Nginx's place). A second, ORANGE stranger packet tries the gate and bounces
RED. The task's reply walks back through the gate with a GREEN "stateful: reply allowed" chip.
SAY: The load balancer ends the HTTPS connection and sends its own request to the task's port 8000. There, a security group allows only the load balancer, on port 8000. A stranger's packet bounces, and the reply goes back out, because the firewall remembers the connection.

SHOW: LECTURE 16 · 20, 59. Two small cards: "administrative access · SSH → the machine", "client access · HTTPS →
the service". Then a GRAY neighbors strip: "EC2 ↔ Compute Engine (slide 59) · ALB ↔ Cloud Load Balancing · NAT Gateway
↔ Cloud NAT (not on the slides)"; each GCP name slides in under its AWS twin as the SAY names it.
SAY: SSH reaches the machine, while clients reach the service. The lecture draws Amazon names. On Google Cloud the neighbors are Compute Engine, Cloud Load Balancing and Cloud NAT.

SHOW: The canvas fades. TAKEAWAY: "`localhost` → the machine the code runs on · `10.x` → private, unreachable from the
internet · public clients → DNS name → load balancer :443 → private target :8000". Then an empty frame.
SAY: If the question says localhost, think: the machine the code runs on. A 10 dot address: private, unreachable from the internet. Public clients: a DNS name, the load balancer on 443, then the private target on 8000.

---

## S03 · Private subnets, route tables and NAT — `s03_nat.py` · `RouteAndNat`

Lecture: L16 5–7, 9, 12–16, 28.

SHOW: LECTURE 16 · 5, 15–16. V2 begins. A BLUE VPC box `10.0.0.0/16`, a gated-community gate at its edge. A CIDR ruler
writes in below: 32 small bit cells, the first 16 filled BLUE ("fixed"), the rest WHITE ("vary"); a counter beside
reads `2¹⁶ = 65,536`; the bar shifts to 24 fixed cells, counter `2⁸ = 256`.
SAY: Now the first alarm: the language model times out, but the database answers. A VPC is one block of addresses, here 10.0.0.0 slash 16. The slash counts the fixed bits out of 32. Slash 16 leaves 16 bits to vary: 65,536 addresses. Slash 24 leaves 8: 256.

SHOW: The ruler fades. The VPC splits into three subnets (slide 16): public `10.0.1.0/24` (solid BLUE, the ALB and the
NAT Gateway), private app `10.0.2.0/24` (padlock, TEAL FastAPI tasks), private data `10.0.3.0/24` (padlock, BLUE
PostgreSQL at `10.0.3.7`). Outside: the Internet Gateway on the VPC edge and the ORANGE internet. A GRAY chip: "the
lecture's picture · the cheese app repos contain no network config".
SAY: The lecture cuts it into three subnets. A public one for the load balancer. A private app subnet for the FastAPI tasks. A private data subnet for the database.

SHOW: LECTURE 16 · 13. Two route tables side by side, PINK rows. Public: `10.0.0.0/16 → local route`, `0.0.0.0/0 →
Internet Gateway`. Private: `10.0.0.0/16 → local route`, `0.0.0.0/0 → NAT Gateway`. The first rows pulse together
("same"); the second rows' right cells flash YELLOW ("the only difference").
SAY: Every subnet has a route table. Both send the VPC's own block to the local route. The only difference is the default row, 0.0.0.0 slash 0. A public subnet sends it to the Internet Gateway, a private subnet to the NAT Gateway.

SHOW: Slide 13's caption as a GRAY strip under the public table: "route = necessary, not sufficient · public IP +
firewall rules also decide". Then the private table shrinks onto a FastAPI task as its little route card.
SAY: A route alone is not enough, slide 13 adds: the machine also needs a public address and an open firewall.

SHOW: A YELLOW packet leaves the task: `10.0.2.5:52134 → 10.0.3.7:5432`. On the route card both rows light; the `/16`
row gets a thicker YELLOW bar labelled "longer prefix wins". The packet travels inside the VPC to the database (GREEN
✓).
SAY: A packet for the database at 10.0.3.7 matches both rows, and the most specific match wins: slash 16 beats slash 0. The packet stays inside, on the local route.

SHOW: LECTURE 16 · 14. A second packet: `10.0.2.5:52134 → 34.x:443` (the LLM API, ORANGE). Only the `0.0.0.0/0` row
lights. The packet travels to the BLUE NAT Gateway in the public subnet. A PINK notebook opens beside NAT with one
line: `10.0.2.5:52134 ↔ NAT-IP:61001`. The source field flashes YELLOW and becomes `NAT-IP:61001`; the packet exits
through the Internet Gateway.
SAY: A packet for the language model API matches only the default row, so it goes to the NAT Gateway. NAT rewrites the private source to its own public address, writes the mapping in its notebook, and sends it out.

SHOW: The reply returns `34.x:443 → NAT-IP:61001`; the notebook line glows; the destination field flashes YELLOW and
becomes `10.0.2.5:52134`; the reply reaches the task (GREEN ✓). Then an ORANGE packet arrives from outside
`→ NAT-IP:62000` with no notebook line; it turns RED and drops.
SAY: The reply comes back, NAT finds the line, and hands it to the task. A packet nobody asked for has no line, so it is dropped. NAT only carries connections that start inside. Nothing uninvited gets in, which keeps the private subnet private.

SHOW: The NAT Gateway turns RED with a "down" chip. A new LLM packet follows the default row and stalls at the dead
hop (RED); a second ORANGE packet `→ package mirror :443` follows the default row and stalls at the same dead hop. At
the same time a database packet flows on the local route (GREEN ✓), and an ALB → task request flows
too (GREEN ✓).
SAY: Now NAT fails. Every call to the internet stalls at the dead hop. But the database packet still matches the local route, and the load balancer still reaches the tasks. That is the first alarm.

SHOW: The canvas clears. PONDER P1 card (tag `illustration`). Question: "A worker in a **private** subnet must download
model weights from a public website at startup. Nobody on the internet may open a connection to it. Where should its
route for `0.0.0.0/0` point?" A · the Internet Gateway, and give the worker a public IP · B · the local route · C · a
NAT Gateway in a public subnet · D · the load balancer.
SAY: First question. A worker in a private subnet downloads model weights from a public website at startup, and nobody on the internet may open a connection to it. Where should its default route point? Pause here if you want.
PONDER(10 s, "Where should the worker's default route point?")

SHOW: Reveal. C fills YELLOW ✓, GREEN note "out + replies back · nothing uninvited in". RED reason under A: "makes the
subnet public · a direct inbound path, guarded only by firewall rules".
SAY: C. NAT carries the worker's request out, maps the reply back, and refuses uninvited connections. A, the Internet Gateway, would download too, but it makes the subnet public, a direct path in, guarded only by firewall rules.

SHOW: RED reason under B: "local covers only 10.0.0.0/16 · the website is outside". Under D: "brings requests in to
targets · not a way out". The card fades.
SAY: B fails: the local route covers only the VPC's own block, and the website is outside it. D fails: a load balancer brings requests in to its targets. It is not a way out.

SHOW: TAKEAWAY: "private subnet → `0.0.0.0/0` goes to NAT · NAT carries only connections that start inside, replies come
back, nothing uninvited gets in · NAT down → internet calls fail, VPC-internal traffic (DB) still works". Then an empty frame.
SAY: If the question says private subnet, think: the default route goes to NAT. NAT only carries connections that start inside. And if NAT is down, internet calls fail, while traffic inside the VPC, like the database, still works.

---

## S04 · The browser lives outside the VPC — `s04_browser.py` · `BrowserOutside`

Lecture: L16 23–24, 27, 30–32, 62–64, 71; L10 11.

SHOW: LECTURE 16 · 30, 62–64. V3 begins. Slide 64's layout redrawn: the BLUE VPC on the right (public subnet with the
ALB; private app subnet with "FastAPI tasks ×3"); top left a GREY browser on a visitor's laptop, clearly outside the
VPC; bottom left a BLUE "static host / CDN" `app.example.com`. Path 1: three file glyphs `HTML`, `CSS`, `JS` fly from
the static host to the browser and unpack; the `JS` gear starts turning on the visitor's laptop.
SAY: Now the second alarm, the failing button. Loading a page is two trips. First the browser downloads HTML, CSS and JavaScript from a static host. Then that JavaScript runs on the visitor's own machine, and calls the API.

SHOW: A YELLOW outline traces the VPC's border, then the browser's laptop: two separate boxes. GRAY caption from slide
64: "Static delivery stays outside the VPC; application requests enter at the ALB."
SAY: So the browser lives outside the VPC. Static files never enter it, and every API request must come in through the front door, the load balancer.

SHOW: Left: CODE(cheese-app-v0/frontend-ai-chatbot/.env.development: 4) (header shows the real path; stored as
`env.development`), then below it CODE(cheese-app-v0/frontend-ai-chatbot/src/services/Common.js: 2), both lit. A PINK
arrow from the variable name on line 4 to `process.env.NEXT_PUBLIC_BASE_API_URL` on line 2.
SAY: Now the course app. In development, the frontend takes its API address from next public base API URL, and that variable says localhost 9000. On the developer's laptop, that was exactly where the API ran.

SHOW: Race, version 1: from the visitor's browser a GREY request `→ http://localhost:9000` curls straight back into
the visitor's own laptop; a GREY empty door ":9000 · nothing listens"; the request sparks RED. The URL text turns RED.
SAY: Ship that to a visitor, and localhost means the visitor's laptop. Nothing listens there, so the request fails. That is the second alarm.

SHOW: Version 2: the same browser, request `→ http://10.0.2.5:8000`; it wanders inside the visitor's own network, never
reaches the ORANGE internet's far side, and evaporates RED; the VPC never sees it. Version 3: `→ https://api.example.com` → the DNS lookup arrows (from S02) → ALB → a task, GREEN ✓.
SAY: Swap in the private address, 10.0.2.5, and the request never reaches the VPC: that address means something only inside the visitor's own network. The public HTTPS name works: DNS, the load balancer, then a task.

SHOW: The panels Transform into CODE(cheese-app-v0/frontend-ai-chatbot/.env.production: 2) (real path in the header;
stored as `env.production`), `/api` lit. LECTURE 16 · 32, 24. The V3 canvas fades. Beside the panel, slide 32's layout
B redrawn (tag `lecture's picture`): the GREY browser → one BLUE public front door `app.example.com` (ALB or Nginx) in
the public subnet; from it two PINK arrows, `/` → a TEAL Next.js server and `/api/*` → TEAL FastAPI `10.0.2.5:8000` in
the private app subnet.
SAY: The production file says just slash api. A relative path goes back to the host that served the page. That works when one public front door serves both the page and the API, the lecture's layout B, and routes slash api to FastAPI.

SHOW: The front door's rule writes in under it as slide 24's two cards joined by a YELLOW "=": GREEN-outlined
`location /api/ { proxy_pass http://10.0.2.5:8000; }` and `listener :443 · path /api/* -> fastapi-tg · fastapi-tg ->
targets :8000`. The `10.0.2.5` sits inside a small BLUE VPC outline. A GRAY chip: "separate static host → name the
public API address".
SAY: Slide 24 writes that rule twice, as an Nginx proxy pass or a load balancer path rule. With a separate static host, the code must name the public API address instead.

SHOW: The `10.0.2.5` in the proxy card pulses YELLOW inside the BLUE outline; a RED ✗ chip "never in browser code"
appears beside the browser.
SAY: Notice where the private address lives: in the proxy's config, inside the VPC. Never in browser code.

SHOW: The route cards and code panel fade; a small `JS` file glyph lands in the browser, GRAY chip over it:
"`NEXT_PUBLIC_…` → compiled in at build time · every visitor downloads it". The BLUE NAT Gateway appears beside the
front door with a one-way PINK arrow pointing **out**; an inbound arrow from the browser
bounces off it.
SAY: Two more facts. Next public variables are compiled into the JavaScript at build time, so every visitor downloads them: public by design, never a secret. And NAT does not help here: it only carries traffic that starts inside the VPC.

SHOW: The canvas fades. TAKEAWAY: "code runs in the browser → it is outside the VPC → call the public HTTPS endpoint
(ALB / domain), never `localhost` or `10.x` · NAT doesn't help inbound". Then an empty frame.
SAY: If the question says code that runs in the browser, think: it is outside the VPC. Call the public HTTPS endpoint, never localhost or a 10 dot address. NAT does not help inbound.

---

## S05 · Build once, configure at startup — `s05_config.py` · `BuildOnce`

Lecture: L16 17, 21–22, 29; L10 42–43.

SHOW: LECTURE 16 · 17, 29. V4 begins. Slide 29's three numbered steps redrawn: (1) a GRAY "source + Dockerfile" card →
`docker build -t myapp:v1.4 .` → a TEAL image `myapp:v1.4` with a digest stamp `sha256:…` lands on the TEAL registry
shelf "ECR"; (2) "deploy · pull + start myapp:v1.4" into the private app subnet; (3) a browser request reaches it.
SAY: Now the quiet problem, the key inside the image. First, how a release should work. Build the image once, push it with a version tag, and every deployment pulls that exact version. No rebuild.

SHOW: LECTURE 16 · 21. The image slides along a conveyor through three stops, "dev", "staging", "prod"; the digest
stamp never changes (a YELLOW check under it at each stop). At each stop a container starts and GREEN runtime-value
cards plug in: dev `APP_ENV=dev · LOG_LEVEL=debug · FEATURE_FLAG=true`, prod `APP_ENV=prod · LOG_LEVEL=info ·
FEATURE_FLAG=false`.
SAY: The image is immutable. It moves from development to staging to production, and its digest never changes. What differs is the runtime values plugged in when the container starts: log level debug in development, info in production.

SHOW: LECTURE 16 · 22. A BLUE "secret manager" box. A PINK path labelled "authorized delivery · workload identity"
carries a GOLD key glyph to the running container, into the process's environment (a GREEN `os.getenv(…)` chip), not
into the image. A GRAY strip: "Never place secrets in: source code, container images, or Git". A small chip: "grant
only the secrets this workload needs".
SAY: Secrets follow the same rule. A secret manager delivers the key at startup, only to the workload that is authorized for it. Never place secrets in source code, in container images, or in Git.

SHOW: LECTURE 10 · 42. The laptop half: a GREY host folder `secrets/` with a GOLD key glyph; a PINK `-v` tunnel to
`/secrets` inside the TEAL container; the env var label `GOOGLE_APPLICATION_CREDENTIALS=/secrets/…json` slides along
it and snaps onto the file. Right: CODE(cheese-app-v2/src/api-service/docker-shell.sh: 23, 25, 27, 29–33) (folded),
lines 25 and 29 lit.
SAY: The course already does the laptop version. The run script mounts the secrets folder at slash secrets, and points Google Application Credentials at the key's path inside the container.

SHOW: The laptop half fades. The docker-shell panel slides left and shrinks;
CODE(cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py: 18–25) writes in on the right, lines 19, 24 and 25 lit;
PINK arrows run from lines 30, 32 and 33 of the left panel to them. Then the left panel fades.
SAY: The project and the ChromaDB host arrive as environment variables too. The app reads them with os dot environ when it starts.

SHOW: The panel Transforms to PANEL(cheese-app-v2/README.md: 25) (one long line, wrapped), the clause "we do not want any secure information in
Git" lit. The `secrets/` folder sits next to the repo folder, outside it.
SAY: The README says why: we do not want any secure information in Git. The key lives next to the repository, never inside it.

SHOW: Contrast (tag `illustration`): a GRAY card "Dockerfile · ENV LLM_API_KEY=…"; the image is X-rayed: its config
card (the GOLD key glows RED on it) and its layer stack; a GRAY `docker inspect` chip reads the key off the config card;
three copies of the image fly to "laptop", "CI runner", "prod host", each carrying the glowing config card. A RED
"rotate key → rebuild" chip, then "dev image ≠ prod image".
SAY: Now the wrong way. Bake the key into the image, and anyone who can pull the image can read it. Rotating it means a rebuild, and per environment images mean what you tested is not what you ship.

SHOW: The canvas clears. PONDER P2 card (tag `illustration`). Question: "A teammate adds `ENV LLM_API_KEY=…` to the
Dockerfile and pushes the image to the team's **private** registry. Which statement is true?" A · Safe: only the team
can reach the registry · B · Safe, as long as `.env` is in `.gitignore` · C · A risk only for the production image ·
D · Anyone who can pull the image can read the key.
SAY: Second question. A teammate bakes an API key into the Dockerfile and pushes the image to the team's private registry. Which statement is true? Pause here if you want.
PONDER(10 s, "Key baked into a private image: which statement is true?")

SHOW: Reveal. D fills YELLOW ✓, GREEN note "inject at startup from a secret store". RED reason under A: "private = many
people and machines · copied to every host".
SAY: D. The image's settings and layers are readable by anyone who pulls it, and changing the key means a rebuild. A, the private registry, is still a long list of people and machines, and the image is copied to every host.

SHOW: RED reason under B: "the key is in the Dockerfile → in Git and in the image". Under C: "dev images leak too ·
per-environment images break build once". The card fades.
SAY: B fails: the key is written in the Dockerfile, which is in Git, and in the image. Ignoring a different file changes nothing. C fails too: development images leak, and separate images break build once.

SHOW: TAKEAWAY: "same image promoted dev → staging → prod · environment values and authorized secrets injected at
startup → never rebuild per environment, never bake a secret". Then an empty frame.
SAY: If a question asks how to move an image to production, think: the same image, promoted unchanged. Environment values and authorized secrets are injected at startup. Never rebuild per environment, and never bake a secret.

---

## S06 · Autoscaling meets the connection budget — `s06_capacity.py` · `ConnectionBudget`

Lecture: L16 43–45, 52, 55, 67.

SHOW: LECTURE 16 · 52. V5 begins. Slide 52's four boxes in a row: "Signal" (CPU, concurrent requests, queue depth) →
PURPLE "Policy" (target · min · max) → "Desired count" → "Capacity". A GRAY traffic line rises; the desired count
ticks 3 → 4 → 5. The caption writes in YELLOW: "Downstream limits still bound the result."
SAY: Now the third alarm. An autoscaler measures a signal, like processor use, applies a policy with a target, a minimum and a maximum, and asks for that many replicas. But downstream limits still bound the result.

SHOW: The boxes shrink to a strip on top (the PURPLE autoscaler stays). Right: a BLUE database panel of 100 socket
slots (10 × 10), tag `illustration`. ORANGE plugs fill 10 slots, labelled "admin console 4", "batch job 6".
SAY: The database accepts a fixed number of connections, here 100. Other clients already hold some: an admin console, a batch job.

SHOW: Left: CODE(cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py: 56–57), line 57 lit, GRAY chip "the
course's vector DB client · stands in for a SQL connection pool". A TEAL replica appears with a GREEN pool of 20 PINK
pipes that plug into free slots.
SAY: Each replica opens its own connections. In the course app, every API process creates its own database client at import. That client is ChromaDB, standing in here for a connection pool.

SHOW: The autoscaler stamps out replicas 2, 3, 4; each pool plugs 20 pipes in; the slots fill (90 used). Replica 5
appears; its pipes find only 10 free slots and spark RED, label `too many connections` (tag `illustration`); its
requests turn RED while a GRAY CPU gauge on it reads low.
SAY: The autoscaler adds replicas, each plugging its pool into free slots, until the slots run out. The next replica cannot connect, though its processor is idle.

SHOW: The arithmetic assembles from the picture: the 100 slots → "limit"; the ORANGE block → "− other clients"; one
GREEN pool → "÷ connections per replica"; brackets `⌊ ⌋` close around it, YELLOW "round down". Below: `⌊(100 − 10) ÷
20⌋ = ⌊4.5⌋ = 4`. The autoscaler's max dial turns to 4; a YELLOW cap line draws across the replica row.
SAY: So read the rule off the picture. 100 slots, minus 10 for the other clients, leaves 90. Divide by 20 per replica: 4.5. A replica cannot open half a pool, so round down to 4, and set 4 as the autoscaler's maximum.

SHOW: LECTURE 16 · 45, 55, 67. Three small GRAY chips: "pending work when capacity lags (45)", "concurrency changes
downstream pressure (55)", "pooling is the team's job (67)". Two relief valves light GREEN: "connection pooler or
smaller pools", "bigger DB tier" (GOLD price tag); a third, "raise max only", turns RED.
SAY: To go higher, add a connection pooler or shrink each pool, or buy a bigger database tier. Raising the maximum alone does not help.

SHOW: The canvas clears. PONDER P3 card (tag `illustration`). Question: "Each API replica opens a pool of **15**
connections. Other clients hold **30**. At peak the service needs **10** replicas. Which is the smallest database tier
that works?" A · 150 connections · B · 200 connections · C · 250 connections · D · keep the 100-connection tier and
raise the autoscaler maximum to 10.
SAY: Third question. Each replica opens 15 connections, other clients hold 30, and at peak you need 10 replicas. Which is the smallest database tier that works? Pause here if you want.
PONDER(10 s, "Smallest database tier that fits 10 replicas?")

SHOW: Reveal. B fills YELLOW ✓, with `30 + 10 × 15 = 180 ≤ 200`. RED reason under A: "150 holds the pools, not the 30
others · 180 > 150".
SAY: B, 200. Ten pools of 15 make 150, plus 30 others: 180. That fits under 200.

SHOW: RED reason under C: "works, but 200 already fits · GOLD price tag". Under D: "a higher max adds no connections ·
180 > 100". The card fades.
SAY: A, 150, holds the pools but forgets the other clients. C, 250, works, but costs more than it needs to. D: a higher maximum adds no connections, so the extra replicas fail.

SHOW: TAKEAWAY: "DB connection limit given → max replicas = ⌊(limit − other clients) ÷ connections per replica⌋ · set
it as the max: the autoscaler doesn't know the DB limit". Then an empty frame.
SAY: If the question gives a database connection limit, think: the limit minus other clients, divided by connections per replica, rounded down. And set it as the maximum, because the autoscaler does not know the database limit.

---

## S07 · Relational plus vectors: one database — `s07_database.py` · `OneDatabase`

Lecture: L16 65–68, 71, 75–76.

SHOW: LECTURE 16 · 76. V6 begins (tag `illustration`). Requirement chips drop from the top: GREEN `users` and `orders`
tables with a PINK foreign-key line between them; a GREEN bracket "transaction: all or nothing"; a PINK
vector chip "find the 5 most similar cheeses" with distance rays. Slide 76's triptych labels them: "relational",
"vector", and above both, "both → often PostgreSQL + pgvector".
SAY: The last mechanism is where the data lives. Classify it first. Users and orders, linked by foreign keys, saved in transactions that are all or nothing: that is relational. Find the five most similar cheeses: that is vector search.

SHOW: Left: CODE(cheese-app-v2/src/vector-db/docker-compose.yml: 19–28), lines 20 and 23 lit; a TEAL ChromaDB
container beside it with a GRAY chip "team patches + backs up".
SAY: Today the course runs ChromaDB as its own container. It is a vector store with metadata, and the team operates it: patches, backups and recovery are yours.

SHOW: LECTURE 16 · 65–66. The panel fades. Three candidate boxes: TEAL "ChromaDB on a VM", BLUE "PostgreSQL service +
pgvector", BLUE "vector search service". The chips try each box: the vector chip lands in all three; the FK and
transaction chips bounce RED off the first and third.
SAY: The lecture compares three homes: ChromaDB on a virtual machine, a PostgreSQL service with pgvector, and a vector search service. Vector chips land everywhere. Foreign keys and transactions bounce off the two vector-only homes.

SHOW: A fourth combo: a relational box and a vector box joined by a PINK sync arrow; an `orders` row appears in the
first, its embedding is missing in the second, and the arrow drifts RED.
SAY: You could run two databases. But then they must stay in sync, and one day an order exists in one while its embedding is missing from the other.

SHOW: Only the PostgreSQL + pgvector box holds every chip. Its table `cheeses` gains a PURPLE `embedding vector(256)`
column beside its GREEN relational columns; below, a GRAY-outlined SQL card (tag `illustration`): `SELECT name FROM
cheeses WHERE in_stock ORDER BY embedding <-> :q LIMIT 5;`.
SAY: Only PostgreSQL with pgvector takes every chip. The vector column sits beside the relational columns in the same table, and one query filters with SQL and orders by similarity.

SHOW: LECTURE 16 · 67–68. Two columns: "provider operates · hosts, storage, patching, backup mechanisms" (BLUE) and
"team owns · schema, queries, migrations, pooling, restore tests" (GREEN). Below, a GRAY strip "Google Cloud: Cloud SQL
for PostgreSQL · AlloyDB" and slide 68's line in YELLOW: "High availability and recovery are configurations, not
defaults." The chips "hosts", "patching" drop into the BLUE column, "schema … restore tests" into the GREEN one as the
SAY names them.
SAY: Managed means the provider runs the hosts and the patching. Your team still owns the schema, queries, pooling and restore tests. On Google Cloud: Cloud SQL for PostgreSQL, or AlloyDB.

SHOW: The canvas fades. TAKEAWAY: "relational + vector needs in ONE managed database → PostgreSQL + pgvector: foreign
keys, transactions and similarity search in one place". Then an empty frame.
SAY: If the question says relational and vector needs in one managed database, think: PostgreSQL plus pgvector. Foreign keys, transactions and similarity search, in one place.

---

## S08 · Seven rules for the quiz — `s08_recap.py` · `Recap`

Lecture: L16 71, 75–80.

SHOW: Seven empty rule rows, each with a 1-second thumbnail of its diagram at the left. Row 1 (V1's DNS → ALB path)
writes in: "`localhost` = the machine the code runs on · `10.x` / `172.16–31.x` / `192.168.x` private · public → DNS
→ load balancer :443 → target :8000".
SAY: Seven rules for the quiz. One: localhost is the machine the code runs on, and 10 dot addresses are private. The public reaches a DNS name and a load balancer.

SHOW: Rows 2 (the route card) and 3 (the NAT notebook): "VPC = CIDR block cut into subnets · most specific route wins
· `0.0.0.0/0` → IGW (public) or NAT (private)"; "NAT carries only connections that start inside · NAT down → internet
fails, DB still works".
SAY: Two: a VPC is an address block cut into subnets, and the most specific route wins. Three: NAT only carries connections that start inside. If it fails, internet calls fail, and the database still answers.

SHOW: Rows 4 (the two paths) and 5 (the conveyor): "browser is outside the VPC → public HTTPS endpoint, never
`localhost` / `10.x`"; "one image promoted · values + secrets at startup · never in image, source or Git".
SAY: Four: the browser is outside the VPC, so it calls the public HTTPS endpoint. Five: build one image, and inject settings and secrets when it starts.

SHOW: Rows 6 (the slot grid) and 7 (the triptych): "max replicas = ⌊(limit − other clients) ÷ per replica⌋ · set it
as the max"; "relational + vector in one DB → PostgreSQL + pgvector". All seven rows glow YELLOW once.
SAY: Six: maximum replicas is the connection limit minus other clients, divided by each pool, rounded down. Seven: relational plus vectors in one managed database means PostgreSQL with pgvector.

SHOW: LECTURE 16 · 14, 71. The list shrinks left. Right: slide 71's complete picture redrawn, plus slide 14's NAT
Gateway in the public subnet: CDN → browser; browser → ALB (public subnet) → FastAPI tasks (private app) → PostgreSQL +
pgvector (private data); NAT for calls out. The three
alarm bells from S01 turn GREEN one by one; the X-rayed image shows no key.
SAY: Here is the whole picture, every alarm fixed. Static files from the edge, requests through the load balancer, tasks in the private app subnet, PostgreSQL in the data subnet, and NAT for calls out.

SHOW: LECTURE 16 · 80. A row of five numbered steps: "trace the request · name the contract · choose the boundary ·
select a service · measure and revise"; step 1 glows YELLOW. Everything fades except a small GRAY line "AC215 ·
Lecture 16 · exam edition", then an empty frame.
SAY: When a question looks hard, do what the lecture does last. Trace the request first. Good luck on the quiz.
