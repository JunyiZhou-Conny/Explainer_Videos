# Brief · AC215 L10 — Connecting to the cloud: who checks that it's you, and how does a page find a database?

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture-slide digest and scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** They are newer (2026-10-19 22:11 – 2026-10-20 01:49 UTC)
and were made by running the README's commands as written, in README order — up to the honest,
documented failure wherever a real Google credential would be needed (this sandbox has none):

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| api-service script on an existing network | digest §6 #1 predicted the abort from reading the code | **live**: `Error response from daemon: network with name cheese-app-network already exists`, exit 1 (`laptop/31`); the fix applied (`32`), the rerun clean (`33`) |
| chunk counts | digest §2 estimated ~8.2 k / ~14.2 k offline | **8,248** char-split / **14,228** recursive-split, live (`laptop/27`); deterministic at this pin of the books and langchain-text-splitters 0.3.11 |
| first cloud call | digest §4: `GET /rag/embedding` in `/docs` returns 256 floats | here it is an honest **500** with the full `DefaultCredentialsError` traceback (`33`, `37`); the success body is `recorded` (source `rag.py:218-223`, 256 floats, values never shown) |
| when auth fails | digest §4 hinted errors surface at the call | confirmed and sharpened: `genai.Client` builds with **no credentials** — uvicorn starts cleanly with an empty `/secrets`, and the error surfaces **per request** as a 500 (`33`); the CLI likewise imports fine and dies only inside `--embed` (`24`) |
| Chroma CORS env + `/data` persistence | digest §10 open question ("does `chroma:latest` still honour them?") | **yes, at the time of recording** (image digest `1e0b73a187a2…`, API `"1.0.0"`): preflight from `:3200` allowed, `:3300` gets no header (`60`/`61`); `chroma.sqlite3` survives `compose down` (`72`, `74`). The tag is unpinned — say "at the time of recording" |
| FastAPI `@app.on_event` deprecation | digest §10 open question | no warning in the captured log at this pin (`33`) — don't mention it |
| the SA's name, roles, mount depth | slides: `data-service-account`, one storage role, `../secrets`, `-p 8090:9100` (SLIDES conflicts 1–4) | the README + captures: `llm-service-account`, Storage Admin **plus** Gemini Enterprise Agent Platform User, `../../secrets`, unprefixed `-p` that `docker ps` shows as `0.0.0.0:…` (`22`, `39`, `54`) — the video says each difference kindly (see Errata) |
| hook | digest §8 opens on the finished chat answer on screen | **no answer text is documented anywhere** (ASSETS "What cannot run here"): the hook is a schematic `illustration` wireframe with no output text |
| length | digest §8: ≈26 min at 155 wpm (~4,000 words) | series voice is ~174 wpm: plan **~4,200 words ≈ 24 min narration**, ~28–30 min with typing, output and ponders |

## Audience and goal

An AC215 student who has done L1–L9: they have a GCP project (L1), know images, containers, bind
mounts, Compose and published ports (L2–L4), have seen the L5 RAG stack and L8 fine-tuning, and
just built the L9 pre-commit gate (whose `detect-private-key` hook starts earning its keep today).
New to them: service accounts and JSON keys, ADC, IAM, networking *between* containers and the
host browser, and CORS. They watch with their own clone of
[dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0) open, pausing to run each
command. **This lecture bills**: the embedding build and every chat/agent question make real
Vertex AI calls against the student's project — GOLD tags mark each one, and the video ends on the
teardown checklist.

After the video they can:
- create a service account, grant roles, download a JSON key and place it in `secrets/` *outside*
  every repo — and say why the key is a password, not config;
- explain ADC's three lookup places, which one a container uses, and how a long-lived key becomes
  a ~60-minute bearer token that rides on every request (the private key never leaves the laptop);
- read an auth failure by layer: `DefaultCredentialsError` = authentication (path/mount), 403 =
  authorization (role, project, or API enablement) — and name the (principal, role, resource)
  cell a 403 is asking about;
- trace `-v HOST:CONTAINER` from `$(pwd)/../../secrets` to `/secrets`, and predict what Docker
  does when the host path doesn't exist (silently creates it empty);
- explain why the CLI dials `llm-rag-chromadb:8000` while their browser rings `localhost:8000`,
  why `next dev`'s `localhost:3000` is unreachable from the host, and what each number in
  `-p 3200:3000` means;
- follow one chat question as three cross-origin calls from the browser, and say what CORS
  actually checks (the page's origin, enforced by the browser, configured by the server — and
  ignored by `curl`);
- run `docker compose down` without fear, knowing where the vectors live and what would really
  delete them;
- fix the api-service script's network abort, and shut everything down (containers, network, and
  stale service-account keys).

## Length and parts

~28–30 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm); the plan below
totals **~4,200**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S09** (~2,530 words, ~17.5 min): identity and the cloud — the map, the service
  account and key, the secrets portal, the network, the chunking run that dies at the exact moment
  credentials are first needed, ADC and the bearer token, the IAM grid, and the API service
  brought up (through the line-14 abort) to its first — recorded — successful cloud call.
- **Part 2 = S10–S15** (~1,670 words, ~11 min): addresses and the browser — container DNS vs
  `localhost`, the frontend's two ports from three angles, the browser as integrator and the CORS
  bouncer, the agent and the fine-tuned endpoint, what survives `compose down` (and GCS as the
  cloud version), teardown and recap.

The cut is the app's own seam: part 1 ends when **the auth chain closes** — the whole file → ADC →
JWT → token → bearer → 200 picture lit, the API answering on port 9000 — with one question parked
for part 2: "the API is up on your laptop. How does a web page find it — and who else can?"
Part 2 answers both halves.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop: the host shell, the host filesystem, the browser's home | GREY |
| the cloud: Google's building, Vertex AI, GCS, the token endpoint | BLUE |
| containers and images: llm-rag-cli, llm-rag-chromadb, api-service, frontend | TEAL |
| system-wide / host-owned (little this lecture: Docker Desktop itself) | ORANGE |
| project-owned, protected: the `secrets/` folder, the JSON key, the mounted `/secrets` | GREEN (turning RED when the key lands inside a repo or an invented danger beat needs it) |
| tools: docker, compose, gcloud, uv, pipenv, npm, uvicorn, next | PURPLE |
| errors and refusals: `DefaultCredentialsError`, 403, 500, the aborted script, CORS "no header" | RED |
| your turn, the README tracker, the current step | YELLOW |
| money: every Vertex AI call the student's run makes; storage/egress on the GCS beat | GOLD |
| lookups, paths, network routes: the Docker networks (drawn as PINK streets), Docker DNS, the ADC lookup walk, published-port tunnels, the three browser calls | PINK |
| future / elsewhere: the hosted deployment (deleted), L11's GCS, L13+'s metadata server, federation | GREY, dashed |

Episode-local semantics (keep consistent): **the key is GREEN** (project-owned, isolated — the
same green as a venv) and the **bearer token is a small BLUE ticket with a timer** (it belongs to
the cloud conversation, not to you). Docker networks are PINK streets per the SLIDES proposal —
not the slides' green panels. An **open door** (an unprefixed published port) is drawn neutral,
never "safe"; the `127.0.0.1:` narrowing closes its street side.

## Running example

- **The laptop** (a fresh Docker 29.8.2 engine standing in for Docker Desktop, linux/amd64): user
  `student`, prompts from the captures (`student@laptop:~$`, `student@laptop:~/cheese-app-v0/llm-rag$`
  …); terminal title `laptop`. "Architecture: x86_64" on screen; say once "aarch64 on Apple
  Silicon — no special flags needed" (digest gotcha 15).
- **Inside containers**: prompts are each capture's own — `app@<id>:/app$` (llm-rag and
  api-service; the id changes every run, say once), `(app) app@<id>:/app$` after `pipenv shell`,
  root `…:/app#` in the frontend's node container.
- **The sandbox, honestly**: this recording machine has **no GCP credentials** — and L10 is the
  lecture about credentials. The video says so plainly, once, early (S05/S06): the key file in the
  folder shots is an obviously-invalid stand-in, removed before the cloud steps, so every cloud
  call shows the *exact missing-key failure a student with a misplaced key gets* — the single most
  common L10 failure (digest §6 #2). Successes a student sees are `recorded` with named sources.
  Never pretend the failure is a surprise; it is the lesson.
- **Project id**: always `your-gcp-project` (the captured edits `20`/`30` write exactly that). The
  README's default `ac215-project` and the instructor's project number `129349313346` appear only
  inside quoted source lines and RED story beats — never as ours.
- **Versions**, all "at the time of recording": Docker 29.8.2 / compose v5.6.0; Python 3.12.15,
  uv 0.13.2, chromadb client 1.1.0, google-genai 1.39.1 (CLI) / 2.28.0 (API), fastapi 0.142.2;
  node 20.20.2, npm 10.8.2, Next.js 14.2.4; ChromaDB `"1.0.0"` from an **unpinned**
  `chroma:latest`. npm's deprecation lines and Next's telemetry notice are real — a student sees
  them too.
- **Capture-only crops**: the harness's readiness/stop lines in `33` (`GET /` probe,
  `GET /capture-done … 404`) and `51` (the same 404 line) are cropped — ASSETS.md flags them. The
  builds in `21`/`33` show no base-image pull rows (capture-only rebuilt bases): show them as they
  are and say nothing. Chroma's "Up 2 minutes" against "Created 4 hours ago" in `54` is a sandbox
  restart artifact — never load-bearing.

## Visual set pieces (the 3Blue1Brown part)

- **V1 · The auth chain (S06 teaser, S07 in full, S09 payoff).** Five links drawn left to right:
  the GREEN key file → ADC's magnifying glass → a signed JWT envelope → the BLUE token desk
  (`oauth2.googleapis.com/token`) → a bearer ticket with a ~60-minute timer, stapled to each HTTPS
  request flying into the cloud. In S06 the chain *breaks at the first link*: the magnifying glass
  finds nothing at `/secrets/llm-service-account.json` and the whole chain greys out — the
  captured `DefaultCredentialsError` under it. S07 builds the chain properly, slot by slot. S09
  closes it: the same chain behind `GET /rag/embedding`, ending in a `recorded` 200 of 256 bars.
  The timer runs out once and a fresh ticket mints itself.
- **V2 · The IAM grid (S08, reprise S13).** Principals (you, `llm-service-account`, the
  instructor's SA) × resources (`your-gcp-project`, `ac215-project`, project `129349313346`);
  role tokens dropped into cells — `roles/aiplatform.user` GREEN in your column, Storage Admin
  GREY ("granted, unused by v0"). Three request arrows test three cells: green, 403, 403. In S13
  the tuned-endpoint arrow re-fires: the *resource path* picks the column.
- **V3 · The secrets portal (S04, payoffs S05/S06/S09).** A file tree of `AC215/`; a cursor at
  `api-service/` climbs `..` `..` to `secrets/`; a glowing tube connects it to `/secrets` inside a
  container silhouette; the env-var label slides along the tube and snaps onto the file. The
  Ponder-1 replay: the key saved *inside* the repo — the cursor still climbs to `AC215/secrets`,
  an empty folder pops into existence, `/secrets` is empty.
- **V4 · One server, two addresses (S10, S11).** One Chroma box, two arrows in: PINK
  `llm-rag-chromadb:8000` from the CLI inside the street bubble; GREY `localhost:8000` from the
  browser through a wall door labelled `8000→8000`. In S11 the frontend's door reads `3200→3000`
  and the number **morphs** as the arrow passes (slide 9's tunnel). A 0–65535 number line (10 s):
  system / registered ("pick yours here": 3000, 3200, 8000, 9000) / dynamic ("a high throw-away
  port the OS picks"). The `0.0.0.0` beat: the door faces every street the laptop is on;
  `127.0.0.1:` bricks up the Wi-Fi side.
- **V5 · The browser is the integrator + the CORS bouncer (S01 teaser, S12 in full).** One chat
  question as three PINK packets from the browser: (1) to door 9000 with a bearer ticket riding to
  the cloud and 256 small bars coming back; (2) to door 8000, where a bouncer checks the packet's
  `Origin: http://localhost:3200` stamp against a two-line guest list (an OPTIONS preflight knocks
  first) and ten chunks come back; (3) to door 9000 with question + chunks, the answer returns.
  Replay with a `:3300` stamp: the bouncer at 8000 gives no header, packet 3 is never sent, and
  the API's door would still have answered — its guest list is `*`. A `curl` figure walks straight
  past the bouncer (no browser, no bouncer).
- **V6 · The running map (built S02, grows every scene, final in S15).** This episode's gate-table
  analogue. A GREY laptop house with its own loopback; two PINK streets (`llm-rag-network`,
  `cheese-app-network`) with TEAL houses that light up as each container starts; doors through the
  laptop wall labelled `8000→8000`, `9000→9000`, `3200→3000`; the browser figure on the laptop
  floor, outside every street; the BLUE Google building across a public street with an IAM-guarded
  door and a GOLD meter beside it; the GREEN `secrets/` drawer feeding tubes into two houses.
  Each scene adds its piece; S15 shows it complete and then tears it down.

## README step tracker (ReadmeTracker, top-left)

Six trackers. The README's section headings are the tracker titles, so "step k of N" matches what
the viewer scrolls past.

- **A · Prerequisites & Service Account** (`README.md:41-75`), 5 steps: Docker + clone · Create
  `llm-service-account` + roles · JSON key → `secrets/` · Folder tree check · Create the network
- **B · Build the Vector DB** (`README.md:79-106`), 5 steps: Edit GCP_PROJECT · docker-shell ·
  cli char-split · cli recursive-split · Exit (Chroma stays up)
- **C · Run API Service Container** (`README.md:125-149`), 4 steps: Edit GCP_PROJECT ·
  docker-shell · uvicorn_server · /docs
- **D · Run Frontend Container** (`README.md:153-180`), 4 steps: docker-shell · npm install ·
  npm run dev · Open :3200
- **E · The five UI steps** (`README.md:184-255`), 5 steps: Text Chunking · Vector DB UI · Chat ·
  Cheese Expert Agent · Pavlos Cheese Model (edit `rag.py:22` + open)
- **F · Shut down** (`README.md:106` + digest §2 checklist), 2 steps: Ctrl-C + exit each ·
  docker compose down — network rm and key hygiene as extras

Steps the README does not have (`git log`, `ls`/`tree`, the second network create, `docker
network ls/inspect`, `docker ps`, the curl checks, the auth-check one-liner, **the line-14 fix**,
the DNS demo `41`–`45`, the CORS preflights `38`/`60`–`62`, `63`, the persistence checks
`71`–`74`, `76`) are marked `extra` in the tracker caption and the narration ("this one isn't in
the README"). S07, S08 and S10 are concept scenes with no tracker (S10's demo commands are all
extras). The "Optional: LLM RAG Tutorial" section (README:110-122) is named once in narration as
L05 material and left to exercises.md.

## Scene plan

Notation: `laptop/NN` = `assets/terminal/laptop/NN-*.txt`; line numbers are file lines (line 1 is
the `$` command and is never printed; `[exit N]` is never printed). ▶ = README command with a
`your turn` tag at real checkpoints. CODE(file: a-b) quotes `assets/source/` at the pin.
`lecture_ref(10, "a–b")` per AC215_SERIES rule 9; spans from SLIDES.md.

**S01 · Three phone calls, one question (~240 words) — `s01_hook.py` · `Hook`.** Cold open, no
tracker; `lecture_ref(10, "4, 11–13")` on the closing line. A schematic `/chat` page, tagged
`illustration`, wireframe only: the question "How is tolminc cheese made?" typed, the answer area
and a "References · 10 chunks" drawer drawn as empty frames — **no answer text exists in any
source, so none appears**. Freeze; three PINK arrows leave the *browser*: `:9000`, `:8000`,
`:9000` (V5 teaser). "When you ask about cheese, your browser makes three phone calls — two to a
Python server, one to a database — and then Google's datacenter answers. Who checks that it's
*you*? And how does a web page find a database hidden inside a Docker container?" Zoom out to the
V6 skeleton. The lecture's own trick (slide 4), on this app's three riddles: `-p 3200:3000` — two
numbers, why? `localhost:9000` — which machine is that? `llm-rag-chromadb` — a name; where's the
address? Each gets answered by a later scene; and slide 11's flip closes the open: once anything
can knock, the question becomes *who's allowed in*. How to follow along: your own clone, Docker
Desktop, **a GCP project with billing** — GOLD: this lecture makes real Vertex AI calls; every
billing moment carries this tag, and the video ends on the teardown. Six trackers, `▶ your turn`,
the study guide has every command.

**S02 · One laptop, three containers, one cloud (~260) — `s02_map.py` · `TheMap`.** Tracker A1;
`lecture_ref(10, "5–6, 11")`. V6 built piece by piece from the digest §1 diagram: the GREY laptop
house (every house has its own loopback — slide 5's rule), two PINK streets, three TEAL houses
drawn hollow (nothing runs yet), the browser figure on the laptop floor *outside every street*,
the BLUE Google building across the public street with a guarded door. Who calls whom, honestly
up front: the CLI calls Vertex and Chroma; the **browser** calls everything else; the API never
talks to Chroma — the README says so itself (README:127) and it surprises everyone. ▶ clone
(README:44 — a prerequisite; the README gives no command, narration says the address is the repo
page) → `laptop/01`; extra `git log` → `02` (HEAD `cb6fb945…`, 2026-10-08 — the digest's pin);
extra `ls` → `03`: highlight `llm-rag/`, `api-service/`, `frontend-ai-chatbot/` — "one house
each" (the committed `.DS_Store` gets one kind word, or none). Kindly (erratum 7): the app's own
home page animates a *hosted* architecture — nginx on a GCP VM — because this app used to live at
a public URL; the `deployment/` folder that did it was deleted (commit `2bc29dd`). You are running
the local version; this video draws what *you* run.

**S03 · An identity for code (~300) — `s03_identity.py` · `IdentityForCode`.** Tracker A2→A3;
`lecture_ref(10, "24–25, 31–38")`. Concept before clicks: a service account is an identity for
software — an ID badge minted with the email
`llm-service-account@your-gcp-project.iam.gserviceaccount.com`, clipped to a server (slide 25's
arrow, no human in the loop). Slide 31's rule walked for this app (SLIDES gap 4): not a metered
public call (API key), not an app acting for a consenting user (OAuth) — code calling Vertex AI in
*your* project, so a service account. The rule's last line, honestly (conflict 5): "outside GCP →
federation" — federation needs someone to vouch for your code the way GitHub vouches for its
Actions; a laptop has nobody, so the course hands you a key, and you treat it like a password. ▶
Console steps (README:48-56) as a schematic console tagged `illustration` — never a screenshot,
never a logo: IAM & Admin → Service accounts → create `llm-service-account` → grant **Storage
Admin** and **Gemini Enterprise Agent Platform User** ("Vertex AI User" in older projects — same
role id `roles/aiplatform.user`, `llm-finetuning/README.md:44-46`) → KEYS → ADD Key (Create New
Key) → JSON → the download moves to `secrets/llm-service-account.json`. The console's two real
warnings redrawn as banners in our own words (slide 37): keys are a risk if leaked; Google
disables keys it finds in public repositories. Kindly (conflicts 1–2): the lecture's demo creates
`data-service-account` with one storage role — that is next week's account (L11); this app needs
the Gemini role, and the Storage Admin grant rides along for L08 reuse (the lecture's own
least-privilege rule, slide 45, would say Storage Object Admin, and only when needed). The key
card unfolds, `illustration`, every field zeroed/`PLACEHOLDER` (digest §3.1): `type`,
`project_id`, `client_email`, `private_key`, `token_uri`; `private_key` glows RED — one factor,
"something you have", works from anywhere, no second step, until the key is deleted (gap 5).
Suggested `gcloud` equivalents (digest step 1) shown small, `extra`, for the console-averse.

**S04 · Two filesystems, one folder (~280) — `s04_secrets.py` · `SecretsPortal`.** Tracker A3→A4;
`lecture_ref(10, "38, 42")`. V3 in full: the cursor starts at `api-service/` ($(pwd)), hops `..`
`..`, lands on `AC215/secrets`; the tube connects it to `/secrets` in a container silhouette; the
label `GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json` slides along and snaps
onto the file. CODE(api-service/docker-shell.sh: 6-14): `SECRETS_DIR=$(pwd)/../../secrets/` is a
**host** path; `GOOGLE_APPLICATION_CREDENTIALS="/secrets/…"` is a **container** path — two
filesystems, one folder, and the env var only makes sense after the mount.
CODE(llm-rag/docker-compose.yml: 11): the same portal from Compose, `../../secrets` resolved
against the compose file's folder. Conflict 3, one line: the lecture's slide mounts `../secrets` —
same portal, different stairs; count the `../` from where the script sits (L11's repos sit one
level shallower). ▶ Make the folder and place the key → `laptop/04` (`mkdir ../secrets`), `05`
(`tree -L 2`: `secrets/llm-service-account.json` **beside** `cheese-app-v0` — README:60-67
exactly; our key is a stand-in, see S05), `06` (`llm-service-account.json`, not `.json.json` — the
tip is `llm-finetuning/README.md:67`). Then the quiet horror: CODE(.gitignore: 1-7) ignores
`docker-volumes` and `outputs` — **not** `secrets/`. Nothing protects a key you put inside the
repo. **PONDER 1 (8 s)**: "Paul saves his key as `cheese-app-v0/secrets/llm-service-account.json`
— inside the repo — and runs `sh docker-shell.sh` from `api-service/`. What does the container see
at `/secrets`, and what happens on the first embedding call?" Answer, replayed in V3:
`$(pwd)/../../secrets` resolves to `AC215/secrets`, which doesn't exist; Docker **silently creates
it empty**; `/secrets` is empty; the first call dies with `DefaultCredentialsError: File
/secrets/llm-service-account.json was not found.` — and his key now sits in a git tree no
`.gitignore` rule protects.

**S05 · A network, a compose file, a running Chroma (~260) — `s05_vectordb.py` ·
`NetworkAndShell`.** Tracker A5, then B1→B2; `lecture_ref(10, "9–10")`. ▶ the network command
(README:74) → `laptop/10` (the id — a PINK street laid, no houses yet); extra: the same command
again → `11` (exit 0, silent — `inspect … || create` is **idempotent**; remember this shape, it
returns in S09); extras `docker network ls` / `inspect` → `12`/`13`. ▶ edit `GCP_PROJECT`
(README:84) → `20`: `your-gcp-project` goes into `llm-rag/docker-shell.sh:7` (sed is our editor;
you use yours — and the same edit comes again for the API). ▶ `sh docker-shell.sh` (README:88) →
`21` (istep; pick ranges): compose pulls `chromadb/chroma`, builds `llm-rag-cli` (uv sync), starts
`llm-rag-chromadb` on `llm-rag-network` — Compose names the default network
(CODE docker-compose.yml: 1-3) and both services join it: slide 10's "networking for free". The
`pull access denied … Building` line, honestly: it just means the image isn't on Docker Hub, so
Compose builds it locally. `Container is running!!!`, `Architecture: x86_64`, Python 3.12.15, the
`app@…:/app$` prompt. Extras inside (digest's sanity check): `ls -la /secrets` — the key file,
through the portal (V3 payoff) — and here the video says it plainly, once: **this recording
machine has no Google account; this file is an obviously-invalid stand-in** so the folder shots
match the README's tree, and it is removed before the cloud steps — so in the next scene you will
see the *exact* failure a missing key gives, the most common L10 mistake. `echo` of both env vars:
Compose interpolates them **from the wrapper's shell** (CODE docker-compose.yml: 14-15) — which is
why you always launch through `docker-shell.sh` (gotcha 5; pays off honestly in S14's warnings).

**S06 · Chunks for free, embeddings need a key (~300) — `s06_chunks.py` · `ChunksNeedAKey`.**
Tracker B3→B5; `lecture_ref(10, "13")` on the GOLD beat. ▶ `python cli.py --chunk --embed --load
--chunk_type char-split` (README:94) → `laptop/24`: `chunk()` runs **for real** — `Number of files
to process: 11`, per-book chunk counts, pandas heads. GOLD, before the bill: `--embed` sends about
7 M characters across the two runs to `gemini-embedding-001` — your run bills your project (say
"check the current pricing page"; never invent an amount; slide 13's runaway-bill warning in one
line). Then `embed()` reaches for the key — and the chain breaks at the first link (V1 teaser):
`DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` The key is an
identity; without it there is no token, and the very first cloud request dies at *authentication*.
On your machine, with a real key, the run continues — `recorded`, from the code's own prints
(cli.py:231, 236/240, 278, 283/285, 157/159-160; what the step does: README:98-105): embeddings
per book, `Creating collection: char-split-collection`, delete-or-create, `Finished inserting N
items…`. ▶ recursive-split (README:95) → `25` (same shape; recursive makes **more** chunks because
`RecursiveCharacterTextSplitter` keeps langchain's default `chunk_overlap=200` — cli.py:199-200).
Extras: `ls outputs/` → `26` — the JSONLs on the host through the `/app` mount, including
`chunks-char-split-Womans Institute Library of Cookery.jsonl`, the title truncated at its first
`.` — digest gotcha 18 in the wild, kindly, with the `os.path.splitext` fix (that book's chunks
get no author, so the agent's author filter can never find them); counts → `27`: **8,248** /
**14,228** (deterministic at this pin); one real chunk → `28`: Tolminc cheese — the very chunk the
hook's question will retrieve. ▶ `exit` (B5): **ChromaDB keeps running** (README:106) — extra
`docker ps` → `22`: Up, `0.0.0.0:8000->8000/tcp` (hold that column for part 2); extra curl →
`23`: `"1.0.0"` ("at the time of recording") — the same route the UI will use (hooks.jsx:14).

**S07 · ADC: from key file to bearer token (~300) — `s07_adc.py` · `AdcToToken`.** Concept scene,
no tracker; `lecture_ref(10, "19–31, 42")`. Open on slide 42's chain redrawn with this app's line:
CODE(api-service/api/routers/rag.py: 14-27) — `genai.Client(vertexai=True, project=GCP_PROJECT,
location="global")`, and **nothing in the repo opens the key file**. The "reads the key" box opens
into V1. The magnifying glass walks ADC's three places, each labelled with the lecture's identity
(SLIDES gap 1): (1) the file named by `GOOGLE_APPLICATION_CREDENTIALS` — a service-account key:
this tutorial; (2) the gcloud user file from `gcloud auth application-default login` — *you*,
through an OAuth consent screen (the fallback when an organization blocks key creation, gotcha
13); (3) the metadata server — the account attached to the VM, Cloud Run service or pod you run
on (GREY dashed: L13–L15). Inside these containers only slot 1 exists. Slot 1 lights: the key's
`private_key` becomes a pen, signs a small JWT envelope; the envelope flies to the token desk
(`oauth2.googleapis.com/token`) and returns a glowing BLUE ticket with a ~60-minute timer; the
ticket staples itself to each outgoing request — `Authorization: Bearer <token>` — and the private
key **never leaves your machine**. The timer dies; a fresh ticket mints itself. One bridge line
(gap 2): this is the same token desk the lecture's OAuth diagram ends at — minus the person; the
consent screen drops out because nobody is there to consent. The live proof of the lookup: extra
`laptop/29` — `google.auth.default()` with an empty `/secrets` → the same `DefaultCredentialsError`;
slot 1 pointed at nothing, and in a container slots 2 and 3 are empty. Misconception, said
kindly: setting the env var on your Mac authenticates nothing — the path must exist *inside the
container*; that is V3's whole point, and why the scripts set a container path and mount a host
folder separately.

**S08 · IAM: may this identity do this, here? (~270) — `s08_iam.py` · `IamGrid`.** Concept scene,
no tracker; `lecture_ref(10, "26, 35, 42, 45")`. Authentication proved *who*; authorization
decides *what, where*. V2: the grid — principals × resources, role tokens in cells:
`roles/aiplatform.user` GREEN in (`llm-service-account`, `your-gcp-project`); Storage Admin GREY
beside it ("granted, never used by v0 — it waits for L08-style bucket work; slide 45 would grant
Object Admin, and only when needed"). Three arrows test three cells: your embed → your project —
green; the same embed with the scripts' unedited `GCP_PROJECT="ac215-project"` — RED **403**
(gotcha 3a: the default string ships in both files; that is why the edit is a tracked step,
twice); a tuned-model call → project `129349313346` — RED 403 (held for S13). The error ladder
(digest §3.3/E3), as a two-layer card: `DefaultCredentialsError` or 401 → *authentication* — no
token; check the path, the mount, the filename. **403** → authentication *worked* and
*authorization* failed — a missing role, the wrong project, or the API not enabled. Kindly
(erratum 2): **no README in this repo tells you to enable the Vertex AI API** — it was probably
done in an earlier lecture; if not, the 403 names it ("has not been used in project …") with an
enable link, or `gcloud services enable aiplatform.googleapis.com` (suggested, `extra`). **PONDER
2 (8 s)**: "Your key works for embeddings. You paste the instructor's fine-tuned endpoint
`projects/129349313346/…`. Which part of the request decides *whose* IAM is checked —
`GCP_PROJECT`, the key's `project_id`, or the endpoint path?" Answer: the resource — the endpoint
path; your principal has no role in that project, so 403 (S13 lands it). One closing line (gap 9):
one key, many services — the same identity reaches Vertex through one role and a bucket through
another; grants differ, the badge doesn't.

**S09 · Run the API, and survive line 14 (~320) — `s09_api.py` · `ApiService`.** Tracker C1→C4.
▶ edit `GCP_PROJECT` (README:130) → `laptop/30` (the second of the two files — api-service/
docker-shell.sh:9). ▶ `sh docker-shell.sh` (README:134) → `31`: **the script dies** — `Error
response from daemon: network with name cheese-app-network already exists`, exit 1. Kindly, the
episode's biggest erratum (digest #1), now live: CODE(api-service/docker-shell.sh: 6-14) —
line 14 runs a *bare* `docker network create` under `set -e` (line 4), so the script aborts every
time the network already exists — including right after the README's own network step. The line
arrived in the very last commit. The fix, extra → `32`: make line 14 the README:74 idempotent form
— the exact shape S05 taught (`inspect … || create`). ▶ again → `33` (istep; crop the harness
lines): the pipenv build from `Pipfile.lock` — 170 pinned packages, slow first build, say once —
the green help text, `(app) …:/app$`. ▶ `uvicorn_server` (README:140): `Uvicorn running on
http://0.0.0.0:9000` (hold `0.0.0.0` for part 2), `Startup tasks`, `Application startup
complete.` Then the finding the captures nailed down: `genai.Client` builds with **no
credentials** — uvicorn starts *cleanly* with an empty `/secrets`; the failure is per-request:
extra `37` — `GET /rag/embedding` → **500**, and `33` shows the full `DefaultCredentialsError`
traceback in the debug log. A green startup is not an authenticated startup. With a real key —
`recorded` (rag.py:218-223): `{"embedding": [...]}`, a list of **256 floats** (values never
shown; `EMBEDDING_DIMENSION = 256` must match the CLI's — rag.py:17, cli.py:26) — and V1 closes:
file → ADC → JWT → token → bearer → 200, the whole chain lit at once. Extras: curl root → `34`
(`{"message":"Welcome to the API Service"}`); ▶ `/docs` (README:149) → `35` (200, text/html; the
Swagger page drawn `illustration`); the route list → `36` — the README's five `/rag` endpoints
live (plus `GET /`, which the table never claimed). End of part 1 on V6: the BLUE building's door
opens for our badge; the API house glows on its street. Parked for part 2: "the API is up on your
laptop. How does a web page find it — and who else can?"

**S10 · A name is not localhost (~290) — `s10_names.py` · `TwoAddresses`.** Concept + live demo,
no tracker (every command `extra`); `lecture_ref(10, "5–6, 10")`. V4 part 1: one Chroma box, two
arrows in — the CLI dialed `llm-rag-chromadb:8000` (CODE llm-rag/cli.py: 30-31) on the PINK
street; your browser will ring `localhost:8000` through the published door. Each container has its
own network namespace, so **its own localhost** — slide 5's "every house has one" read from
inside the box. Docker DNS is the street's phone book (slide 10): names survive restarts, IPs
don't — extra `13`/`40` network inspects show the real addresses ("yours will differ — which is
the point: dial names, not IPs"). The three-step proof, live (digest E5, all captured while the
API ran): extra `41` — from inside the API container, `http://llm-rag-chromadb:8000` → `Name or
service not known`: different street, no entry in this phone book. **PONDER 3 (8 s)**: "You want
the *API* itself to query Chroma. What URL does it use, and what single Docker command makes that
name resolvable?" Answer, live: extra `42` — `docker network connect cheese-app-network
llm-rag-chromadb` — and extra `43`: the same URL now returns `b'"1.0.0"'` (Docker DNS on a shared
street); and the third angle, extra `44`: `http://localhost:8000` from inside the API container is
`Connection refused` — inside a container, localhost is *that container*. Extra `45` disconnects:
back to the tutorial's state — nothing in v0 needs the shortcut, because the browser makes every
call (README:127; the stale `next.config.js` rewrites that point at a container name that doesn't
exist here are one kind line — erratum 6 — "use `localhost:9000/docs`, as the README says").

**S11 · One server, two addresses (~320) — `s11_frontend.py` · `FrontendPorts`.** Tracker D1→D4;
`lecture_ref(10, "4, 7–9")`. ▶ `sh docker-shell.sh` (README:161) → `laptop/50` (istep): the
`Dockerfile.dev` build (node:20-alpine + bash — you run npm yourself), the root `…:/app#` prompt.
▶ `npm install` (README:167): `added 773 packages` — npm's deprecation warnings are real; the
`node_modules` lands on the **host** through the bind mount (run npm only inside the container, or
delete the folder when switching — gotcha 16, one line). ▶ `npm run dev` (README:168) → `51`
(**crop the stop-cue line**): `▲ Next.js 14.2.4`, `✓ Ready`, and the line that fools everyone:
**`Local: http://localhost:3000`** — the *container's* view. The money shot, three angles, all
live: extra `53` — the host's `localhost:3000` → `Failed to connect` (nothing is published on
3000); ▶ open `http://localhost:3200` (README:177) → extra `52` — `HTTP 200`,
`<title>RAG App</title>`; extra `55` — *inside* the container, `localhost:3000` answers with the
same page. One server, two addresses. V4 part 2: the wall door `3200→3000`, the number morphing as
the arrow passes — slide 9's tunnel with this app's numbers; `docker ps` → `54`: the
`0.0.0.0:3200->3000/tcp` column beside Chroma's (never read `54`'s uptimes aloud). The number line
(gap 6, ten seconds): 0–65535 in three bands — system (22, 80, 443), registered ("pick yours
here": 3000, 3200, 8000, 9000), dynamic ("a high, throw-away port the OS picks" for every outbound
call your browser makes). Then the honest beat (conflict 4 + gap 3): `0.0.0.0` has now appeared
twice, and they are different facts — uvicorn *listens* on all the container's interfaces so the
tunnel can reach it (CODE api-service/docker-entrypoint.sh: 7), and Docker *publishes* on all the
laptop's interfaces unless you write a prefix: port_toy (L04) wrote `-p 127.0.0.1:8090:9100`; this
app writes none, so the doors face your Wi-Fi too — anyone on your network can reach them, and
CORS is not that protection (next scene). The one-token narrowing, narration + diagram only (no
fake capture): `-p 127.0.0.1:9000:9000`. The Chrome note (README:179-180), one hedged line:
"the README says Chrome; locally, others should work too — stick with the instructions."

**S12 · The browser is the integrator (~320) — `s12_browser.py` · `BrowserIntegrator`.** Tracker
E1→E3; `lecture_ref(10, "11, 13")` on the closing beat (CORS itself is tutorial-only). First,
where the page learns the API's address: CODE(frontend-ai-chatbot/.env.development: 1-4) +
CODE(src/services/Common.js: 1-2) — `NEXT_PUBLIC_…` is **baked into the JavaScript sent to your
browser**, so it must be an address *the host browser* can reach: `localhost:9000`, never a
container name (E8; S10's lesson from the other side). ▶ Text Chunking (README:188) → extra `56`
(200 + title; the splitting runs **in the browser** — no API, no cloud, no bill; one beat, drawn
`illustration`). ▶ Vector DB UI (README:202) → extra `57`; the form's defaults
(`http://localhost:8000`, `default_tenant`, `default_database` — chromaui/page.jsx:23-27),
Connect → `GET /api/v2/version`, then collections (hooks.jsx:14, 43): browser → host door 8000.
Honest: *our* collections list is `[]` (extra `63` — nothing could be embedded without
credentials); the populated sidebar — `char-split-collection`, `recursive-split-collection` — is
`recorded` (README:103/206). ▶ Chat (README:215) → extra `58`; V5 in full on one question
(CODE src/components/chat/ChatComponent.jsx: 161-173): packet 1 — `GET :9000/rag/embedding`, the
bearer ticket rides to the cloud, 256 bars come back (GOLD: each question = one embedding + one
generation on your bill); packet 2 — `POST :8000/…/collections/<id>/query`, `n_results: 10`
(CODE src/services/DataService.js: 34-43): an *origin* is scheme + host + port, so `:3200`,
`:9000` and `:8000` are three different origins; a JSON POST knocks first with an OPTIONS
preflight, and the bouncer checks the page's `Origin` stamp against Chroma's two-line guest list
(CODE llm-rag/docker-compose.yml: 26 — the instructors' hosted site, and your `localhost:3200`);
packet 3 — `POST :9000/rag/llm-response`, question + ten chunks, the answer returns. The guest
list, live: extra `60` — preflight from `Origin: http://localhost:3200` →
`access-control-allow-origin: http://localhost:3200`; extra `61` — the same preflight from
`:3300` → **no header at all** (the browser would refuse to read); extra `38` — the API answers
`*` to anyone (CODE api-service/api/service.py: 13-20; `allow_credentials=False` is what makes a
literal `*` legal). **PONDER 4 (8 s)**: "You republish the frontend at `-p 3300:3000` and ask a
question. Which of the three calls fails — and does `curl` care?" Answer: call 1 succeeds (the
API's list is `*`), call 2 is blocked by the browser (no header for `:3300` — `61`), call 3 is
**never sent** (`getRagResponse` awaits call 2 first); `curl` ignores all of it — CORS is enforced
by the *browser*, configured by the *server*, keyed on the *page's* origin; and `127.0.0.1:3200`
is a different origin from `localhost:3200` (gotcha 8). The answer area: described, not shown —
what to look for is an answer plus a "References" drawer of ten chunks with book, author and
`dist` (cosine distance: lower = closer; README:217-222) — wireframe `illustration`, **no answer
text**. Closing beat (gap 3): CORS decides *which page may read* the reply; nothing here decides
*who may call* — slide 13's unprotected AI endpoint is running on your laptop, spending your key.

**S13 · The agent, and a model that isn't yours (~230) — `s13_agent.py` · `AgentAndTuned`.**
Tracker E4→E5. ▶ Cheese Expert Agent (README:232): the flow as a diagram over code
(CODE rag.py: 150-171 and 173-215 highlights; browser side ChatComponent.jsx:176-198): Gemini is
*forced* to pick a retrieval tool — `get_book_by_author` or `get_book_by_search_content` — and the
API swaps the search text for its embedding; the browser queries Chroma (author-filtered when that
tool won); the API loops up to `MAX_AGENT_STEPS = 5`, calling the server-side
`pavlos_fun_fact_tool` as it pleases. GOLD: one agent question = 1 embedding + 3–7 generation
calls (digest §2). What to look for — described, **no output panel** (nothing documents any answer
text): the reply ends with a highlighted **Pavlos' fun fact** paragraph (README:236-239,
ChatComponent.jsx:22-28). ▶ Pavlos Cheese Model (README:247, 249): edit
`FINE_TUNE_GENERATIVE_MODEL` — CODE(rag.py: 14-27) shows the default: the *instructor's* endpoint,
`projects/129349313346/locations/us/endpoints/…` — to your own from L08 (the trainer prints it:
CODE(llm-finetuning/gemini-finetuner/cli.py: 91-96)); uvicorn reloads by itself (`rag.py` is under
`api/`; its neighbour `agent_tools.py` is *not* — gotcha 12, one line: Ctrl-C and rerun for that
one). V2 reprise, Ponder 2 lands: the endpoint path is the **resource** — leave the default and
your 403 arrives from a project you have no role in (nothing documents that error's exact text →
no output panel; the second client with `location="us"`, CODE rag.py: 110-120, in one breath; the
L08 `base_url` question is unverified — exercises.md, never claimed). GOLD: tuned-model calls bill
whichever project owns the endpoint.

**S14 · What survives: volumes now, buckets next (~260) — `s14_persist.py` · `WhatSurvives`.**
Tracker F1→F2; `lecture_ref(10, "40–45")`. Containers are disposable — every run here was `--rm`
(extra `46`: the API container already gone). State lives where it is mounted. ▶ `docker compose
down` in `llm-rag` (README:106) → `70`: Chroma stopped and removed, `llm-rag-network` removed —
and two real `"variable is not set"` warnings, because we ran `down` outside the wrapper script:
gotcha 5's interpolation mechanism, caught in the wild (one kind line). Extra `71`: nothing
running. Extra `72`: `docker-volumes/chromadb/chroma.sqlite3` **survived**. **PONDER 5 (6 s)**:
"After `docker compose down`, are your embeddings gone? What *would* make them gone?" Answer: no —
the data lives in the bind-mounted folder (`./docker-volumes/chromadb:/data`,
CODE docker-compose.yml: 18-26); deleting `llm-rag/docker-volumes/` is what loses them — and
re-running `--load` rebuilds collections cleanly, because the CLI deletes-then-creates
(cli.py:281-289). The proof: extra `73` — the same `sh docker-shell.sh` brings Chroma back over
the same folder; extra `74` — `"1.0.0"` again, same data directory, collections intact. Then the
cloud half (slides 40–45, redrawn): a bind mount is a folder *this laptop* can see; a **GCS
bucket** is a folder *any authorized machine* can see — the folder tree melts into a flat key
space (slide 41: "folders" are name prefixes), and the credentials story is the one you already
know: CODE(llm-finetuning/dataset-creator/cli.py: 279-294) — `storage.Client()` with no key path
(ADC again, same key), a Storage role authorizing the writes; the read side in one line
(mega-pipeline/transcribe_audio/cli.py:36-43). v0 never calls GCS — that is why Storage Admin sat
GREY in the grid — L11 exercises it for real. Slide 45's four rules as a card: Object Admin over
Admin; keep buckets private; prefix the globally-unique name; **delete what you don't need** —
storage and egress bill (GOLD, GREY-dashed future).

**S15 · Tear down, recap, and what's next (~250) — `s15_recap.py` · `Recap`.** Tracker F;
`lecture_ref(10, "26, 31, 53")`. Teardown, captured: the API and frontend died with Ctrl-C +
`exit` in their own scenes (`--rm` cleaned up — `46`); ▶ `docker compose down` once more → `75`
(idempotent, clean); extra `76` — `docker network rm cheese-app-network`. **Nothing idles in the
cloud**: no VM, no bucket, no deployed endpoint was created (digest §2) — what can keep costing is
the **key**: hygiene, said (suggested, `extra` card): `gcloud iam service-accounts keys list` /
`keys delete` — delete keys you no longer use; if one ever reaches GitHub, delete it in IAM
immediately (history rewriting is not enough — and L9's `detect-private-key` hook is the gate that
catches it first). The debugging flowchart (digest §8 ch10), each error pointing at its set piece:
`DefaultCredentialsError` → path/mount (V3); 401 → authentication, no token (V1); 403 → role /
project / API (V2); `Failed to fetch` or a CORS line in the console → origin (V5); `port is
already allocated` / name conflict → doors and names (V4); the script dies on the network →
line 14. V6 complete, then unlit. "Test yourself", five questions one at a time with a thumbnail
of their picture (answers in exercises.md):
1. Name ADC's three places, and which one this tutorial fills.
2. Why is `GOOGLE_APPLICATION_CREDENTIALS` set to `/secrets/…` and not to a path on your Mac?
3. The CLI dials `llm-rag-chromadb:8000`; your browser rings `localhost:8000`. Why can't they
   swap?
4. You serve the frontend at `http://localhost:3300`. Which component breaks first, and why does
   the API keep working?
5. You got a 403 on `/rag/embedding`. Three distinct causes — and how do you tell them apart?
Footer cards: exercises.md, and the study guide
(`MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md`). Next, GREY dashed: L11 creates
`data-service-account` and finally exercises GCS for real (buckets, prefixes — and a *bucket's*
CORS list for a localhost UI); later, code running *inside* the cloud fills ADC's third slot
(L13–L15), and slide 31's federation returns when CI needs to deploy (L21+).

## Ponder questions (summary)

| # | scene | question (as on the card) | answer (said right after the timer) |
| --- | --- | --- | --- |
| 1 | S04 (8 s) | "Paul saved his key *inside* the repo\n(`cheese-app-v0/secrets/…`) and runs the script\nfrom `api-service/`. What does `/secrets` hold,\nand what happens on the first embedding?" | `$(pwd)/../../secrets` = `AC215/secrets`, which doesn't exist; Docker silently creates it empty; `/secrets` is empty; `DefaultCredentialsError: File /secrets/llm-service-account.json was not found.` — and the key sits in an unprotected git tree (digest §3.4, gotcha 2/14) |
| 2 | S08 (8 s) | "Your key works for embeddings. You paste\nthe instructor's endpoint `projects/129349313346/…`.\nWhich part decides *whose* IAM is checked:\n`GCP_PROJECT`, the key's `project_id`, or the path?" | The endpoint path — the resource. Your principal has no role in project 129349313346, so 403 (digest §3.8, erratum 4; lands in S13) |
| 3 | S10 (8 s) | "You want the API itself to query Chroma.\nWhat URL does it use, and what single Docker\ncommand makes that name resolvable?" | `http://llm-rag-chromadb:8000` after `docker network connect cheese-app-network llm-rag-chromadb` — shown live (`laptop/41`→`43`); `localhost:8000` would be the API container itself (`44`) |
| 4 | S12 (8 s) | "You republish the frontend at `-p 3300:3000`\nand ask a question. Which of the three calls\nfails — and does `curl` care?" | Call 1 succeeds (API allows `*`, `38`), call 2 is browser-blocked (no CORS header for `:3300`, `61`), call 3 is never sent (the code awaits call 2); `curl` ignores CORS throughout (digest E1, §3.6) |
| 5 | S14 (6 s) | "After `docker compose down`,\nare your embeddings gone?\nWhat *would* make them gone?" | No — `chroma.sqlite3` lives in the bind-mounted `docker-volumes/chromadb` (`72`, `74`); deleting that folder loses them; `--load` rebuilds via delete-then-create (cli.py:281-289) |

Each is answerable from the picture or capture shown just before it.

## Errata and version drift to state (kindly, with the fix)

1. **The api-service script aborts on an existing network** (digest #1; **live** in `31`):
   `docker-shell.sh:14`'s bare `docker network create` under `set -e` dies every time the network
   exists — including right after the README's own network step; the line arrived in the final
   commit `cb6fb94`. Fix: the README:74 idempotent form on line 14 (`32`) (S09).
2. **Nothing tells you to enable the Vertex AI API** (digest §2, gotcha 3c) — probably done in an
   earlier lecture; if not, the first call 403s with an enable link. Fix (suggested):
   `gcloud services enable aiplatform.googleapis.com` (S08, one line).
3. **The default `GCP_PROJECT="ac215-project"` 403s for everyone** (gotcha 3a) — and it must be
   edited in **two** files (`llm-rag/docker-shell.sh:7`, `api-service/docker-shell.sh:9`); the
   README says to, the two-file part is what bites (S05, S09; the RED grid arrow in S08).
4. **Storage Admin is granted but v0 never touches GCS** (erratum 2) — pre-granted for L08-style
   reuse; by the lecture's own slide 45, Storage Object Admin would do, and only when needed
   (S03, S08 grey token, S14).
5. **The fine-tuned endpoint is hard-coded to the instructor's project** (erratum 4); README:247
   says to replace it; the default 403s. The possible missing regional `base_url` (erratum 5) is
   **unverified — never claim it**; exercises.md (S13).
6. **Stale `next.config.js` rewrites** point at `rag-system-api-service`, which doesn't exist here
   → `localhost:3200/docs` fails; use `localhost:9000/docs` as README:149 says (erratum 3,
   gotcha 11) (S10, one line).
7. **The home page and its animated diagram describe the *hosted* deployment** (erratum 8) — the
   `deployment/` folder that implemented it was deleted in `2bc29dd`; you run the local version
   (S02).
8. **Book-name truncation** (gotcha 18; **visible live** in `26`): `filename.split(".")[0]` drops
   the metadata of "Womans Institute Library of Cookery. Volume 2…", so the agent's author filter
   can never select it. Fix: `os.path.splitext` (S06).
9. **Names drift across sources** (SLIDES conflicts 1–2, 6): the slides' `data-service-account` is
   L11's account; "Gemini Enterprise Agent Platform User" = "Vertex AI User" =
   `roles/aiplatform.user` (README:52, llm-finetuning/README.md:44-46); the slides' Mega-Pipeline
   retelling uses this week's conventions, not what L03 students ran (S03, S14 — one kind line
   each).
10. **`chromadb/chroma:latest` is unpinned** (gotcha 17): the CORS env var and `/data` persistence
    are honored **at the time of recording** (`"1.0.0"`, digest `1e0b73a187a2…`) and could drift;
    pin a tag if a new image breaks (S06/S12, "at the time of recording").
11. **Lazy auth** (captures settled digest §10's open question): the Gemini client constructs
    without credentials; uvicorn starts green with an empty `/secrets` and each request 500s —
    a green startup is not an authenticated startup (S09; the finding, stated as a lesson).
12. **Version drift, "at the time of recording"**: every number in the Running-example list; npm's
    deprecation warnings and Next's telemetry notice are real (S09, S11); `docker compose down`
    outside the wrapper prints two real "variable is not set" warnings — the interpolation
    mechanism visible (gotcha 5) (S14).

## Costs and teardown

This lecture **bills** (the series' first since L08). GOLD tags, exactly where the student's own
run spends money:
- **S06**: the `--embed` runs — ~2.7 M characters of books becoming ~7 M embedded characters
  across both splitters (digest §2's estimate, corroborated by the live chunk counts 8,248 /
  14,228). Say "this bills your project; check the current pricing page" — never an amount.
- **S12**: each Chat question = 1 embedding + 1 generation (`max_output_tokens` 3000).
- **S13**: each Agent question = 1 embedding + 3–7 generation calls; tuned-model calls bill
  whichever project owns the endpoint.
**Nothing idles**: no VM, bucket or deployed endpoint is created (digest §2). Teardown, captured:
Ctrl-C + `exit` ends each `--rm` container (`33`, `51`, `46`); `docker compose down` (`70`, `75`);
`docker network rm cheese-app-network` (`76`); vectors persist in `docker-volumes/chromadb` —
delete that folder only to really reset. Said only (suggested): key hygiene —
`gcloud iam service-accounts keys list` / `keys delete` for keys you no longer use (S15); GCS
rules and `gcloud storage rm -r` belong to E7/L11 (S14's card).

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order:

| README instruction | README line | scene |
| --- | --- | --- |
| Clone the repo (prerequisite; no command given — narration says so) | 44 | S02 |
| Console: create `llm-service-account`, grant 2 roles, JSON key → `secrets/` | 46-56 | S03 (`illustration`) |
| Folder structure (tree; `mkdir ../secrets` is our `extra` editor action) | 58-67 | S04 |
| `docker network inspect cheese-app-network >/dev/null 2>&1 \|\| docker network create cheese-app-network` | 74 | S05 |
| Edit `GCP_PROJECT` in `llm-rag/docker-shell.sh` | 84 | S05 |
| `sh docker-shell.sh` (llm-rag) | 88 | S05 |
| `python cli.py --chunk --embed --load --chunk_type char-split` | 94 | S06 |
| `python cli.py --chunk --embed --load --chunk_type recursive-split` | 95 | S06 |
| exit; ChromaDB keeps running; (`docker compose down` to stop) | 106 | S06 (exit), S14 (down) |
| Optional: LLM RAG Tutorial | 110-122 | named in S06 narration; exercises.md |
| Edit `GCP_PROJECT` in `api-service/docker-shell.sh` | 130 | S09 |
| `sh docker-shell.sh` (api-service; aborts, fixed, rerun) | 134 | S09 |
| `uvicorn_server` | 140 | S09 |
| `http://localhost:9000/docs` | 149 | S09 (curl evidence `35`; UI `illustration`) |
| `sh docker-shell.sh` (frontend) | 161 | S11 |
| `npm install` | 167 | S11 |
| `npm run dev` | 168 | S11 |
| `http://localhost:3200` (+ Chrome note) | 177, 179-180 | S11 (curl evidence `52`) |
| `http://localhost:3200/chunkviz` | 188 | S12 |
| `http://localhost:3200/chromaui`, connect to `http://localhost:8000` | 202 | S12 |
| `http://localhost:3200/chat`, pick a collection, ask | 215 | S12 |
| `http://localhost:3200/agent`, ask | 232 | S13 |
| Edit `FINE_TUNE_GENERATIVE_MODEL` in `api-service/api/routers/rag.py` | 247 | S13 |
| `http://localhost:3200/finetunechat` | 249 | S13 |
| API Endpoints table | 259-269 | S09 (`36` shows it live) |

The five "Go to http://localhost:3200/…" steps have their server-side half captured (`52`, `56`,
`57`, `58`) and their page behaviour drawn `illustration` from `source/` (ASSETS "What cannot run
here"); the console steps are `illustration` with README field values; the Vertex-dependent
outputs are `recorded` with named sources; everything else is live.

## Notes for script and scene authors

- Shared code (`scenes/common.py`, started from L09's): tracker factories `tracker_a` …
  `tracker_f` with the step lists above; prompts `P_LAPTOP`, `P_LLMRAG`, `P_API` (+ pipenv
  variant), `P_FRONTEND_ROOT` — container prompts come from each capture; tags `extra_tag`,
  `illustration_tag`, `recorded_tag`, `your_turn`, and the GOLD `cost_tag`. Set-piece classes:
  `AuthChain` (V1), `IamGrid` (V2), `SecretsPortal` (V3), `PortDoor`/`TwoArrows` (V4),
  `CorsBouncer`/`PacketReplay` (V5), `AppMap` (V6, persistent state across scenes).
- **The sandbox framing is load-bearing**: say once, early (S05→S06), that this recording machine
  has no Google account, the key in the folder shots is an obviously-invalid stand-in, and it was
  removed before the cloud steps so the captures show the exact missing-key failure. After that,
  every failure beat is a lesson, not an apology; every success is `recorded` + source. Never
  imply the failure was unexpected, and never show the placeholder's content as a real key (its
  421 B size is never load-bearing).
- `istep` captures (`21`, `33`, `50`, `51`) hold whole sessions: pick line ranges per typed
  command. Crop: `33`'s stray `GET /` access line and `GET /capture-done … 404`; `51`'s
  `/capture-done` line. `21`/`33` show no base-pull rows (capture-only rebuilt bases) — say
  nothing. Progress bars appear redrawn — crop to stable lines.
- `63` is honestly `[]`; `54`'s ChromaDB uptime is a restart artifact; `70`'s warnings are real
  and teachable. Long lines (tracebacks, pip/npm warnings) fold with `wrap`.
- The instructor's endpoint path and `ac215-project` appear **only** inside CODE panels quoting
  the repo's own files and in RED story beats; every terminal shows `your-gcp-project`.
- The name "Pavlos" appears only inside captured/quoted repo content (the book metadata in `28`,
  the "Pavlos' fun fact" label, file names) — allowed as data; never added by us. Narration may
  say "the instructor's project / endpoint". The prompt user is `student`.
- Redraw every lecture diagram in series style; never the console screenshots (slides 32–38), the
  hand-drawn OAuth/API-key images (18, 20–22) or the film still (54). One `lecture_ref` per scene
  as assigned.
- Chinese glossary heads-up: service account, key, token, bearer token, ADC, IAM, principal,
  role, CORS, preflight, origin, bind mount, mount, port, localhost, Docker DNS, endpoint,
  embedding, bucket, prefix stay English; 认证 (authentication) vs 授权 (authorization) per
  `i18n` glossary conventions when that stage comes.

## Things never to do on screen

Series rules:
- No slide images, console screenshots, Google/GCP logos, memes or the film still: redraw the
  idea, cite slides via `lecture_ref`; the console is a schematic `illustration` with README
  field values.
- No real person's name on screen beyond quoted repo content (above); no hand-typed output: every
  terminal line comes from `assets/terminal/`; `recorded` panels name their source (cli.py's own
  prints, README:98-105/103/206, rag.py:218-223); there are **no** `expected` panels in this
  episode.
- No command spelled differently from the README (the `sed` edits in `20`/`30`/`32` are editor
  actions, marked `extra`/narrated as "update the file"; the fix in `32` is explicitly *ours*,
  with the README:74 form as its source).

Lecture-specific:
- **No real-looking key material, ever**: key fields drawn zeroed with `PLACEHOLDER`; never render
  a plausible private key, key id, or client id; the project id on screen is always
  `your-gcp-project`.
- **No invented outputs**: no chat/agent/fine-tuned answer text (describe the References drawer
  and the fun-fact highlight instead — no output panel); no embedding float values (bars or
  `[…256 floats…]`); no invented 403 body for the endpoint; no invented prices or token counts
  beyond digest §2's estimates (say "estimate").
- Never claim `--embed`/`--load`/chat success live; never show a populated collections list
  without the `recorded` tag (`63` is `[]`).
- Never say the API connects to ChromaDB (README:127), that the frontend calls the API
  server-side, or that `cheese-app-network` carries any traffic in v0 (nothing in the current code
  needs it — digest Excerpt 2).
- Never present CORS as protecting the database (curl walks past the bouncer), never present an
  unprefixed `-p` as safe-by-default, and never colour the open `:9000` door GREEN.
- Never state versions, timings, image digests, Chroma's `"1.0.0"`, package counts or chunk
  counts without "at the time of recording" (the chunk counts 8,248 / 14,228 are deterministic at
  this pin — still say it once).
- Never show `54`'s uptimes, the harness lines in `33`/`51`, or base-image/CA rows.

## Left for exercises.md (not in the video)

Digest E1 in full (move the port to 3300: the `localStorage`-per-origin wrinkle and the exact
console messages); E4's second half (`GOOGLE_APPLICATION_CREDENTIALS= python -c …` and the
metadata-server probe delay); E5's Docker-Desktop extra (`host.docker.internal`); E6 (remove
Storage Admin, predict nothing breaks); E7 (the GCS hands-on with your own bucket + slide 45's
rules + cleanup); E8 beyond S12's one line; gotcha 13 (org blocks key creation → user-ADC
fallback, mounting `~/.config/gcloud`); gotcha 16 details (musl vs mac binaries); erratum 5 (the
`base_url` question, unverified); erratum 10 (the agent's repeated tool-choice call); the dead
`/chatui` page and unused `session_id` (erratum 11); the optional L05 `llm-rag` tutorial
(README:110-122); the "who can knock on `0.0.0.0:9000`" recap question with the `127.0.0.1:`
fix; digest recap Q1–Q6 not used in S15.
