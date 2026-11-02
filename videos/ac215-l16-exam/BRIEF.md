# Brief · AC215 L16 — System Tradeoffs: networking, runtime config and capacity (with L10) (exam edition)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md` and
`.claude/skills/ac215-video/SKILL.md` (scene-code pitfalls, never-do list). Facts, in order of
authority:

1. **The Lecture 16 deck** ("System Tradeoffs: Performance, Cost, and Design Choices", 81 slides),
   read from its extracted text (the deck is course material in the session scratchpad, never in
   git; there is no L16 `SLIDES.md` or digest). It is the **primary source**: the quiz's networking,
   configuration, scaling and data-store questions are taught there. Cite with `lecture_ref(16, …)`.
2. **The Lecture 10 deck** ("Connecting to the Cloud"), through
   `../ac215-l10-cloud-connect/SLIDES.md` (digest with slide numbers) and
   `../ac215-l10-cloud-connect/digest.md` (the verified tutorial digest), both read-only. It opens
   the video (laptop vs cloud, credentials mounted at runtime). Cite with `lecture_ref(10, …)`.
3. **The demo repos** `cheese-app-v0` (L10's tutorial) and `cheese-app-v2` (the later course app),
   copied unchanged into `assets/source/<repo>/<path>` at the commits in `video.yaml`.

**This is an exam edition, not a follow-along.** It teaches the mechanisms that Quiz 4 tests about
these lectures, each as a real animated diagram, with code and README panels from the demo repos as
evidence. It does not walk a README: no README tracker, no "▶ your turn" tags, no terminal captures,
no `ASSETS.md` capture list. Every code panel quotes `assets/source/` with its real `path · lines a–b`.

**One file was renamed on copy, content unchanged.** The repo `.gitignore` ignores `.env.*`, so
`cheese-app-v0/frontend-ai-chatbot/.env.development` and `.env.production` are stored as
`assets/source/cheese-app-v0/frontend-ai-chatbot/env.development` and `env.production`. Their panel
headers still show the real path (`frontend-ai-chatbot/.env.development · line 4`).

**The lecture draws AWS; the course runs on GCP.** L16's pictures use AWS names (VPC, subnet route
tables, NAT Gateway, Internet Gateway, ALB, ECR, Route 53). The quiz uses the lecture's picture, so
the video does too: AWS-style terms on screen, and one sentence in S02 for the GCP neighbours
(Compute Engine, Cloud NAT, Cloud Load Balancing, Artifact Registry, Secret Manager, Cloud SQL /
AlloyDB; slides 59, 68). Never claim GCP subnets have their own route tables.

## Audience and goal

An AC215 student **the day before Quiz 4**. They sat Lectures 10 and 16 (or skimmed them), have run
the cheese app's containers on their laptop (`docker-shell.sh`, `localhost:9000`, the `secrets/`
folder), and may never have deployed anything into a VPC. They want to walk into the quiz able to
reason, not recite.

After the video they can answer conceptual multiple-choice questions on these lectures **and say why
each wrong option is wrong**:
- **laptop vs cloud** (L10 slides 4–11, L16 3–4, 8–11, 18–20, 27): `localhost` is *this machine*;
  a private IP (10.x, 172.16–31.x, 192.168.x) is not routed on the internet; a port picks the
  service; `0.0.0.0` means "listen on every interface"; the public reaches a **DNS name** that
  resolves to a **load balancer** out front, which forwards :443 to the private target's :8000;
  a security group is an allow-list on inbound ports, and replies to allowed traffic come back
  statefully;
- **VPC routing** (L16 5–7, 12–16): a VPC is a CIDR block cut into subnets; a **public** subnet's
  route table sends `0.0.0.0/0` to the Internet Gateway, a **private** subnet's sends it to a
  **NAT Gateway**; both send the VPC CIDR to `local`; the most specific matching route wins;
- **NAT** (L16 9, 14): translates a private source address on the way out, remembers the mapping,
  maps the reply back, and **accepts no unsolicited inbound connection**; if NAT fails, only
  traffic to the internet fails — VPC-internal traffic (the database, the ALB to the tasks) still
  flows on the local route;
- **the browser is outside the VPC** (L16 23–24, 27, 30–32, 62–64, 71): a static frontend's
  JavaScript runs on the visitor's machine, so it must call the **public HTTPS endpoint** (the API
  domain → ALB, or a relative path the front door routes), never `localhost` or a `10.x` address;
  NAT does nothing for inbound requests;
- **build once, configure at startup** (L16 17, 21–22, 29; L10 42–43): one immutable image is
  promoted unchanged through environments; runtime values (`APP_ENV`, `LOG_LEVEL`, feature flags)
  and **secrets** are injected when the container starts — from a secret manager in the cloud, or on
  the laptop by mounting `secrets/` and pointing `GOOGLE_APPLICATION_CREDENTIALS` at the in-container
  path — never baked into the image, the source or Git;
- **capacity** (L16 43–45, 52, 55, 67): the autoscaler turns a signal into a desired replica count,
  but downstream limits bound it: **max replicas = ⌊(DB connection limit − other clients) ÷
  connections per replica⌋**;
- **data store** (L16 65–68, 71, 75–76): relational data (users, foreign keys, transactions) **and**
  vectors (embeddings, similarity search) in **one managed database → PostgreSQL + pgvector**.

## Length and format

**12–15 minutes**, one part (no `parts:` key). Narration **~2,100 words** (range 1,800–2,300;
Kokoro `af_heart`, speed 0.9, ~150 wpm in this series ≈ 14 min of speech); three ponder timers (8 s
each) and the diagrams' silent beats add under a minute. Scene budgets below are targets (±15 %).

Every mechanism scene (S02–S07) ends on a YELLOW **takeaway card**: "If the question says *X* →
think *Y*." S08 collects them as seven rules of thumb. The three PONDER beats are **new** quiz-style
multiple-choice questions (never the practice questions Q14–Q18, never their wording or numbers).

## The lectures behind it

Every scene teaching a slide idea carries the GREY `lecture_ref` tag (top right); where a scene
stands on both decks, show the L16 tag and switch to the L10 tag while the L10 idea is on screen
(one tag at a time). The diagrams echo the lecture's own pictures in series colours:
- L10 slide 11's laptop-vs-cloud table (address / who can reach it / getting traffic in) as the
  S02 morph; L10 slide 42's `docker run` → mounted key → env var → IAM check as S05's laptop half;
- L16 slide 13's two route tables side by side, slide 14's private server → NAT (in the public
  subnet) → Internet Gateway, slide 16's three-subnet VPC (public 10.0.1.0/24, private app
  10.0.2.0/24, private data 10.0.3.0/24), slide 27's numbered DNS → ALB path, slide 64's "two
  request paths", slide 21's one image with two runtime-value cards, slide 22's secret manager →
  workload, slide 52's signal → policy → desired count → capacity strip, slide 76's
  vector / relational / both triptych.

Slide subtleties to keep right:
- the VPC CIDR is `10.0.0.0/16`; the route row reads `10.0.0.0/16 → local route` (slides 13–14);
- slide 13's caption: a public-subnet route is necessary, not sufficient — a public IP and firewall
  rules also decide reachability. Say it once in S03;
- slide 9 and 11: a stateful firewall lets the replies of an allowed connection back in; NAT does
  the same job for addresses (slide 14). Keep the two ideas separate on screen;
- slide 24: Nginx `proxy_pass http://10.0.2.5:8000` and the ALB rule `path /api/* → fastapi-tg`
  are the *same route*, run by different operators. The private address appears **inside** the VPC
  (the proxy's config), never in the browser's code.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop and the visitor's machine: the browser, `localhost` / `127.0.0.1`, the host side of `-p 9000:9000`, the laptop's `secrets/` folder | GREY |
| the cloud: the VPC box (`10.0.0.0/16`), its subnets (public subnet solid outline; private subnets the same BLUE with a small padlock), the Internet Gateway, the NAT Gateway, the ALB, Route 53 / the DNS resolver, the managed PostgreSQL service, the secret manager | BLUE |
| containers and images: `myapp:v1.4` (one image, one digest), FastAPI tasks / replicas, the ChromaDB container, the registry shelf | TEAL |
| shared, not yours: the public internet cloud, OS-chosen ephemeral source ports (`:52134`), other clients holding database connections (the admin console, a batch job) | ORANGE |
| what the project owns and sets: runtime values per environment (`APP_ENV`, `LOG_LEVEL`, `FEATURE_FLAG`), the app's schema (users, orders, foreign-key lines), the replica's own connection pool | GREEN |
| tools: Docker, uvicorn, Nginx, the autoscaler (signal → policy), the pgvector extension | PURPLE |
| failures and "avoid this": a dropped packet, a refused connection (`too many connections`), a key baked into an image layer, a `10.x` or `localhost` URL in browser code, the ✗ beside a wrong option | RED |
| "look here now": the packet in flight, the route row being matched, the ponder timer, the takeaway cards | YELLOW |
| money and secrets: the secret's **key glyph** (never a value), the DB tier's price tag in S07 | GOLD |
| routes and lookups: route-table rows, the DNS lookup arrows, request paths, the NAT mapping table, the connection "pipes" from replicas to the database | PINK |
| outside this lecture (Kubernetes details, multi-AZ, CDN internals) | GREY dashed |

Packet glyphs are the same everywhere: a small envelope with `src → dst` printed on it; the field
that changes (NAT's source rewrite, the ALB's port change) flashes YELLOW, then settles.

## Running example

- **The Cheese App, deployed the lecture's way** (slides 16, 28, 64, 71): browser → `api.example.com`
  → ALB in the public subnet `10.0.1.0/24` → FastAPI tasks in the private app subnet `10.0.2.0/24`
  (one at `10.0.2.5:8000`, slide 4) → PostgreSQL in the private data subnet `10.0.3.0/24`; outbound
  calls to an external LLM API go through the NAT Gateway. The static frontend comes from
  `app.example.com` (a CDN or static host). These names are the lecture's own placeholders.
- **On the laptop** (L10, `cheese-app-v0`): FastAPI on `0.0.0.0:9000` in a container, published with
  `-p 9000:9000`; the Next.js frontend on `localhost:3200` calling `http://localhost:9000`; the key
  in `../../secrets/` mounted at `/secrets`.
- **Invented examples** (the hook, the ponders, S06's numbers, S07's tables) use neutral names and
  the GREY `illustration` tag; they are never styled as repo panels (no `path · lines` header).

## Visual set pieces (mechanisms, not cards)

- **V1 · Same container, different street (S02).** A GREY laptop holds a sealed TEAL container
  (FastAPI listening on `0.0.0.0:9000`; panel `docker-entrypoint.sh:7`). The browser's request to
  `localhost:9000` loops inside the laptop and passes the `-p 9000:9000` tunnel (slide 9 of L10).
  Then the laptop dissolves and the same TEAL box lands in a BLUE VPC on a street of addresses: it
  now has a private address `10.0.2.5`; an ORANGE internet packet addressed to `10.0.2.5` hits the
  internet edge and evaporates (no public route). A DNS lookup (slide 27, numbered 1–4) turns
  `api.example.com` into the ALB's public IP; the packet reaches the ALB on :443, the port field
  flips YELLOW to :8000 and the packet enters the private subnet. A security-group gate on the task
  checks "source = ALB, port 8000" (allow-list, slide 11); a stranger's packet bounces RED; the
  reply walks back through the gate unchecked (stateful).
- **V2 · The route lookup and the NAT notebook (S03).** Slide 16's three subnets. Each private
  server carries a little route table (two PINK rows). Packets leave a FastAPI task: to `10.0.3.7`
  (the DB) — both rows match, the `/16` row is longer and lights YELLOW, the packet stays inside;
  to `34.x` (an LLM API) — only `0.0.0.0/0` matches, the packet goes to the NAT Gateway. NAT opens a
  notebook (PINK table: `10.0.2.5:52134 ↔ NAT-IP:61001`), rewrites the source field, sends it out
  through the Internet Gateway; the reply comes back to `:61001`, NAT looks it up and rewrites the
  destination to `10.0.2.5:52134`. An unsolicited packet arrives at NAT from outside: no notebook
  line → dropped RED. Then the NAT Gateway turns RED (outage): the next internet-bound packet stalls
  at a dead hop; the DB packet keeps flowing on the local row; the ALB → task request keeps flowing.
  A CIDR ruler (slides 5, 7) appears once: 32 bits, prefix fixed, the rest vary → 2^(32−prefix).
- **V3 · Two request paths (S04).** Slide 64's layout. Path 1: HTML/CSS/JS files fly from the
  static host / CDN to the browser and **unpack** there (the JS gear starts turning on the visitor's
  laptop, outside the VPC). Path 2: the JS fires a request. Three versions race from the same
  browser: `http://localhost:9000` curls back into the visitor's own laptop (nothing listens: RED);
  `http://10.0.2.5:8000` leaves for the internet and dies at the edge (private, not routed: RED);
  `https://api.example.com` → DNS → ALB → tasks (GREEN ✓). The NAT Gateway, beside the ALB, is
  shown with a one-way arrow pointing **out** — an inbound arrow bounces off it.
- **V4 · One image, many startups (S05).** A TEAL image `myapp:v1.4` with a digest stamp is built
  once and placed on the registry shelf. It slides along a conveyor through dev → staging → prod
  (the digest stamp never changes). At each stop a container starts and GREEN runtime-value cards
  plug in (`LOG_LEVEL=debug` → `info`), and a GOLD key glyph arrives from the BLUE secret manager
  along a PINK "authorized delivery" path (slide 22) into the process's environment, not into the
  image. Contrast: a key baked into a Dockerfile layer — the image's layer stack is X-rayed and the
  key glows RED in layer 4 for anyone who pulls it; changing it means a rebuild. Laptop half (L10
  slide 42): the host `secrets/` folder is tunnelled to `/secrets` by `-v`, and the env var
  `GOOGLE_APPLICATION_CREDENTIALS=/secrets/…json` slides along it and snaps onto the file.
- **V5 · The connection budget (S06).** The database is a BLUE panel of socket slots (a grid of
  100). ORANGE plugs fill some slots (other clients). The PURPLE autoscaler reads a rising traffic
  signal (slide 52) and stamps out TEAL replicas; each replica runs a GREEN pool of N PINK pipes that
  plug into free slots. The slots fill; the next replica's pipes find none and spark RED
  (`too many connections`), and its requests fail even though CPU is fine. Then the arithmetic
  assembles itself from the picture: (limit − other) ÷ per-replica, floored, and the autoscaler's
  max-replica dial is set to that number (the YELLOW cap line).
- **V6 · Two shapes of data, one engine (S07).** Requirement chips drop from the top: `users`,
  `orders` (FK line between them), "transfer must be all-or-nothing" (a transaction bracket),
  "find the 5 most similar cheeses" (an embedding vector, PINK distance rays). Three candidate
  boxes (slide 66): ChromaDB on a VM, PostgreSQL + pgvector service, a vector search service. Each
  chip tries to land in each box: vector chips land everywhere, relational chips and transactions
  bounce off the vector-only boxes (RED); a "two databases" combo works but grows a sync arrow that
  drifts RED (an order written in one, its embedding missing in the other). Only PostgreSQL +
  pgvector takes all chips; a `vector` column appears beside the relational columns of the same
  table, and one query uses both (`WHERE` + `ORDER BY embedding <-> :q LIMIT 5`, tag
  `illustration`).

## Scene plan

Budgets total **~2,110 words**. Slide numbers are PDF page numbers of each deck; code panels quote
`assets/source/<repo>/<path>` with real line numbers, ≤ 12 lines on screen at a time.

**S01 · Launch day: three alarms (~170 words).** L16 71 (the complete picture), L10 4. No code. Cold
open on a broken thing (tag `illustration`): the Cheese App moves from a laptop to a VPC, and on
launch morning the map lights three alarms. (1) The page loads for everyone, but the Predict button
spins — though it worked on the developer's laptop. (2) Chat answers that call an outside LLM API
time out — yet the saved chat history, read from the database, loads fine. (3) At 9 a.m. traffic
doubles, the autoscaler adds replicas, and the new ones fail with "too many connections" while CPU
is idle. Plus a fourth, quieter problem nobody noticed: the production key is inside the image.
"Each alarm is one mechanism from these two lectures." Map of the video: addresses → routes and NAT
→ the browser → configuration → capacity → the database. No takeaway card (the hook only asks).

**S02 · From localhost to a front door (~300).** L10 5–11; L16 3–4, 8–11, 18–20, 27. V1.
Panels: `cheese-app-v0/api-service/docker-entrypoint.sh:6-9` (`uvicorn … --host 0.0.0.0 --port
9000`), `cheese-app-v0/api-service/docker-shell.sh:19-27` (`-p 9000:9000`), and
`cheese-app-v0/README.md:173-175` ("Serve the app at `http://localhost:3200`", "Call the API at
`http://localhost:9000`"). Vocabulary: IP = street address, port = door, `localhost` = this
machine, private ranges (slide 8 of L16: RFC 1918) vs public, `0.0.0.0` = every interface. L10
slide 11's three rows (address, who can reach it, getting traffic in) morph from the laptop column
to the cloud column: public IP and DNS name, a firewall closed by default, a load balancer out
front. Administrative access (SSH) reaches the machine; client access reaches the service (L16
20). One sentence on GCP neighbours (see top). Takeaway: *"`localhost` → the machine the code runs
on; `10.x` → private, unreachable from the internet; public clients → DNS name → load balancer
:443 → private target :8000."*

**S03 · Private subnets, route tables and NAT (~380).** L16 5–7, 9, 12–16, 28. V2. No repo panel
(the cheese app repos contain no VPC config; say so in one clause). The VPC as a gated community
cut into streets (slide 15–16); CIDR in one beat (32 bits, `/16` = 65,536, `/24` = 256). The two
route tables side by side (slide 13): the only difference is where `0.0.0.0/0` goes. Most specific
match wins. Why a private subnet: the database and the app tasks need no inbound path from the
internet. NAT's notebook: translate out, map replies back, refuse the uninvited. The outage beat:
NAT fails → every internet-bound call fails; anything matching `10.0.0.0/16` keeps working,
including the database and the ALB's requests to the tasks. Slide 13's caption ("necessary, not
sufficient") in one clause. PONDER 1 (8 s). Takeaway: *"Private subnet → `0.0.0.0/0` goes to NAT;
NAT = outbound only, replies come back, nothing uninvited gets in; NAT down → internet calls fail,
VPC-internal traffic (DB) still works."*

**S04 · The browser lives outside the VPC (~280).** L16 23–24, 27, 30–32, 62–64, 71; L10 11. V3.
Panels: `cheese-app-v0/frontend-ai-chatbot/.env.development:4`
(`NEXT_PUBLIC_BASE_API_URL=http://localhost:9000`, file stored as `env.development`),
`…/src/services/Common.js:2` (the base URL is read from that variable), and
`cheese-app-v0/frontend-ai-chatbot/.env.production:2` (`/api`, stored as `env.production`). The page
loads, then the JS calls the API (slide 30): the JS runs on the visitor's machine. On the developer's
laptop `localhost:9000` happened to be the API — for a visitor it is their own laptop (resolves
alarm 1). A `10.x` address is private. The working choice is the public HTTPS endpoint; the
production file's relative `/api` asks the same host that served the page, and the front door
routes `/api/*` to FastAPI (slide 24's `location /api/` = the ALB's `path /api/*` rule; slide 32
layout B). Note in one sentence: `NEXT_PUBLIC_` values are compiled into the JavaScript the browser
downloads, so they are public by design (never a secret). NAT only helps traffic that starts inside.
Takeaway: *"Code that runs in the browser → it is outside the VPC → call the public HTTPS endpoint
(ALB / domain), never `localhost` or `10.x`; NAT doesn't help inbound."*

**S05 · Build once, configure at startup (~320).** L16 17, 21–22, 29; L10 42–43. V4. Slide 29's
three numbered steps (build + push, deploy pulls the exact tag, requests). Slide 21: one immutable
image, dev and prod differ only in runtime values. Slide 22: secrets are injected at startup by an
authorized delivery; "never place secrets in source code, container images, or Git"; grant only
the secrets this workload needs. The laptop version the course already uses (L10 slide 42):
panels `cheese-app-v2/src/api-service/docker-shell.sh:23-35` (`-v "$SECRETS_DIR":/secrets`,
`-e GOOGLE_APPLICATION_CREDENTIALS=/secrets/ml-workflow.json`, `-e GCP_PROJECT`, `-e CHROMADB_HOST`
…), `cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:18-25` (the app reads
`os.environ[…]` at startup), and `cheese-app-v2/README.md:25` ("we do not want any secure
information in Git"). Why bake = bad: anyone who can pull the image can read every layer;
rotating a key means a rebuild and a new image for every environment; dev and prod would need
different images, so what you tested is not what you ship. PONDER 2 (8 s). Takeaway: *"Same image
promoted dev → staging → prod; environment values and authorized secrets injected at startup →
never rebuild per environment, never bake a secret."*

**S06 · Autoscaling meets the connection budget (~260).** L16 43–45, 52, 55, 67. V5. Panel:
`cheese-app-v2/src/api-service/api/utils/llm_rag_utils.py:56-57` (each replica process opens its own
database client at import — the course's ChromaDB, standing in for "every replica holds its own
connections"; say "stands in for", not "this is PostgreSQL"). Slide 52: signal → policy (target,
min, max) → desired count → capacity, and the caption "downstream limits still bound the result".
Slide 45: work can remain pending when capacity lags. Slide 55: concurrency changes downstream
pressure. The formula appears from the picture; rounding is always **down** (a partial replica
cannot hold a partial pool). Relief valves in one sentence: a connection pooler or smaller pools
(slide 67: pooling is the team's job), or a bigger DB tier — raising the replica max alone does not
help. PONDER 3 (8 s). Takeaway: *"If the question gives a DB connection limit → max replicas =
⌊(limit − other clients) ÷ connections per replica⌋; the autoscaler won't respect it unless you set
the max."*

**S07 · Relational plus vectors: one database (~230).** L16 65–68, 71, 75–76. V6. Panel:
`cheese-app-v2/src/vector-db/docker-compose.yml:19-28` (the course runs ChromaDB as its own
container today: a vector store, and the team operates it — slide 65's first column). Slide 76:
classify the data first — vector, relational, or both; "both → often PostgreSQL + pgvector". Slide
66's three columns (operations, data model, recovery). Slide 67: managed PostgreSQL — the provider
patches and backs up; the team still owns schema, queries, migrations, pooling and restore tests.
Slide 68: GCP names (Cloud SQL for PostgreSQL, AlloyDB); "high availability and recovery are
configurations, not defaults". Takeaway: *"Relational + vector needs in ONE managed database →
PostgreSQL + pgvector: foreign keys, transactions and similarity search in one place."*

**S08 · Seven rules for the quiz (~170).** L16 75–80. The seven rules (below) appear one by one,
each with a one-second thumbnail of its diagram; the closing image is slide 71's complete picture
redrawn with all three alarms from S01 turned GREEN, then slide 80's decision order in one line
("trace the request first"). Ends on an empty frame.

## Ponder questions (new; 4 options, 8 s timer, then why each wrong option is wrong)

| # | scene | question (on screen, tag `illustration`) | options | answer and why the others fail |
| --- | --- | --- | --- | --- |
| 1 | S03 | A worker in a **private** subnet must download model weights from a public website at startup. Nobody on the internet may open a connection to it. Where should its route for `0.0.0.0/0` point? | A the Internet Gateway, and give the worker a public IP · B a NAT Gateway in a public subnet · C the local route · D the load balancer | **B.** NAT carries the worker's outbound request and maps the reply back, and refuses uninvited inbound connections. A works, but the worker becomes reachable from the internet. C: `local` only covers the VPC's own CIDR; the website is outside it. D: a load balancer brings requests *in* to targets; it is not an outbound path. |
| 2 | S05 | To make the image "just work", a teammate adds `ENV LLM_API_KEY=…` to the Dockerfile and pushes the image to the team registry. Which statement is true? | A It's safe because the registry is private · B Anyone who can pull the image can read the key, and changing it means rebuilding — inject it at startup from a secret store instead · C It's safe as long as `.env` is in `.gitignore` · D It only matters for the production image | **B.** Image layers and their metadata are readable by anyone who pulls the image; the key now lives in every copy and every environment, and rotating it means a new build. A: "private" is a long list of people and machines, and the image is copied to every host. C: `.gitignore` protects files in Git, not an image. D: dev images leak too, and per-environment images break "build once". |
| 3 | S06 | A managed database allows **200** connections. A reporting job keeps **20** open and the admin console **10**. Each API replica opens a pool of **15**. What is the largest safe autoscaler maximum? | A 13 · B 11 · C 12 · D no limit needed: the autoscaler adds replicas only while CPU is high | **B** = ⌊(200 − 20 − 10) ÷ 15⌋ = ⌊170 ÷ 15⌋ = 11 (11 × 15 = 165 ≤ 170). A = ⌊200 ÷ 15⌋ ignores the other clients. C rounds 11.3 up to 12 (180 > 170: the twelfth replica's pool can't fully open). D: CPU says nothing about the database's limit; the scaler happily adds replicas that then fail. |

(The ponder numbers are deliberately different from the practice questions' numbers.)

## The seven rules (S08; also the exercises' answer key later)

1. `localhost` is the machine the code runs on; `10.x` / `172.16–31.x` / `192.168.x` are private and
   not routed on the internet. Public clients reach a DNS name → load balancer :443 → private
   target :8000.
2. A VPC is a CIDR block cut into subnets. Route lookup: the most specific match wins — the VPC CIDR
   goes `local`; `0.0.0.0/0` goes to the Internet Gateway (public subnet) or the NAT Gateway
   (private subnet).
3. NAT is outbound only: it rewrites the source, remembers the mapping, maps replies back, and
   accepts no unsolicited inbound connection. NAT down → internet calls fail; VPC-internal traffic
   (the database, the ALB to the tasks) still works.
4. The browser runs on the visitor's machine, outside the VPC: frontend JavaScript calls the public
   HTTPS endpoint (or a relative path the front door routes), never `localhost` or a `10.x` address.
   NAT doesn't help inbound.
5. Build one immutable image and promote it unchanged; inject runtime values (`LOG_LEVEL`, …) and
   authorized secrets at startup (secret manager; on the laptop, a mounted `secrets/` folder +
   `GOOGLE_APPLICATION_CREDENTIALS`). Never in the image, the source or Git.
6. Autoscaling is bounded downstream: max replicas = ⌊(DB connection limit − other clients) ÷
   connections per replica⌋, rounded down, and set as the scaler's max.
7. Relational + vector needs in one managed database → PostgreSQL + pgvector (foreign keys,
   transactions, similarity search).

## Things never to do on screen

- Never quote, paraphrase or answer the practice questions Q14–Q18; the ponders above are new, with
  different numbers and situations. The hook's alarms illustrate mechanisms and are never phrased as
  a question with options.
- No slide images, PDF pages, memes or QR codes; redraw the idea and cite it with `lecture_ref`.
- No AWS, Google Cloud, Nginx, Docker, PostgreSQL or ChromaDB logos; no console screenshots
  (schematic drawings tagged `illustration`).
- No real person's name (the instructor, commit authors, the README's persona chips): say "the
  course staff". Never show `cheese-app-v0/README.md:20-21`, `:36`, `:232-249`.
- No credentials, keys, project numbers or endpoint ids. **Never quote `cheese-app-v0`'s
  `api-service/api/routers/rag.py`** (it contains project-number endpoint paths) and **never open
  `cheese-app-v2`'s `.env.development` / `.env.production`** (they hold a committed auth secret); they
  are not in `assets/source/` on purpose. The secret in V4 and in ponder 2 is a GOLD key glyph or
  `…`, never a value. `ac215-project` in `docker-shell.sh` may appear only as the course's
  placeholder ("CHANGE TO YOUR PROJECT ID" is on the same line).
- No terminal output: this edition runs nothing and shows no captures; no invented console output.
  `too many connections` in V5 is a label on the diagram (tag `illustration`), not a log.
- Invented code (the `illustration` SQL in S07, the Dockerfile line in ponder 2) is never styled as
  a repo panel.
- Never say GCP subnets have their own route tables, or that Cloud NAT is a route's next hop; keep
  the AWS-style picture labelled as the lecture's picture.
- Never put a `10.x` address or `localhost` in browser code as if it could work in production; the
  private address appears only inside the VPC (proxy config, route rows, the target).
