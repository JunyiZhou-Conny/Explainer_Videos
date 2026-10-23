# AC215 · Lecture 10 — Connecting to the cloud: who checks that it's you, and how does a page find a database? — narration script & visual plan (v1)

Audience: an AC215 student who has done L1–L9 (a GCP project, images and containers, bind mounts,
Compose, published ports, the L5 RAG stack, L8 fine-tuning, the L9 pre-commit gate). New to them:
service accounts and JSON keys, ADC, IAM, networking between containers and the host browser, and
CORS. They watch with their own clone of `dlops-io/cheese-app-v0` open and a GCP project with
billing, pausing to run every command. This lecture bills: the embedding build and every chat and
agent question make real Vertex AI calls against the student's project (GOLD tags, shutdown at the
end).

Goal: after the video they can create a service account, grant its roles, download a JSON key and
place it in `secrets/` outside every repo, and say why the key is a password, not config; name
ADC's three lookup places, say which one a container uses, and trace how a long-lived key becomes
a one-hour bearer token while the private key stays on the laptop; read an auth failure by layer
(`DefaultCredentialsError` = no identity file → no token; 403 = authorization: role, project or
API enablement) and name the (principal, role, resource) cell a 403 asks about; trace
`-v HOST:CONTAINER` from `$(pwd)/../../secrets` to `/secrets` and predict what Docker does when the
host path is missing; explain why the CLI dials `llm-rag-chromadb:8000` while the browser rings
`localhost:8000`, why `next dev`'s `localhost:3000` fails on the host, and what each number in
`-p 3200:3000` means; follow one chat question as three cross-origin calls and say what CORS
checks (the page's origin, enforced by the browser, configured by the server, ignored by `curl`);
run `docker compose down` knowing where the vectors are kept; fix the api-service script's network
abort; and shut everything down, including stale keys.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest), `assets/` (see `ASSETS.md`). Where the digest or the slides and the
captures disagree, the captures win. Nothing in a terminal panel is typed by hand: every output
line below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each) and become the
  subtitles. Plain spoken English: no backticks, no symbols, no parentheses; commands and paths are
  said in words ("sh docker-shell.sh", "dash p, 3200 colon 3000", "slash secrets", "localhost 9000
  slash docs") while the exact spelling is on screen. File, tool and service names are written as
  they are and said by lexicon entries (`explainer/lexicon.yaml`; existing: docker-shell.sh,
  docker-compose.yml, pipenv, ADC, RAG, Tolminc, 127.0.0.1, 0.0.0.0, 3.12.15; added for L10:
  idempotent, splitext, Next.js, 14.2.4, 1.0.0, 3200, 3300, 443, 401, 403, and the guards
  "a 401", "A 401", "a 403", "A 403"). The lexicon splice turns an "a" directly before an entry
  into the letter name, so no SAY line puts a bare "a" before an entry word ("the pipenv shell",
  never "a pipenv shell"); the 401/403 guards cover those two. "Tolminc" is always capitalized in
  SAY (the lexicon entry is case-sensitive). No `'s` after a word with a lexicon entry, except `README's` ("the three places
  ADC looks", never "ADC's places"). Numbers as digits; never a "!" after a digit. Versions, package
  counts, build times, chunk counts and Chroma's `"1.0.0"` are said with "at the time of
  recording". HTTP status codes are digits ("a 403"); the lexicon says them "four oh three".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the Chinese alignment). No
  sentence opens with a command, flag, tool or file name ("An extra git log shows…", "Then a dash v
  flag mounts…"). No homographs: never "read", "live", "close", "lead", "tear", "record" as a noun;
  the main clause comes first so the Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent timer); the card is removed at the start of the next block. Five in the video (BRIEF):
  S04, S08, S10, S12 (8 s each) and S14 (6 s).
- `TERM(laptop/NN: lines)`: a terminal beat. `laptop/NN` is the one file
  `assets/terminal/laptop/NN-*.txt`. The scene types the command written just before it in the
  SHOW line (in backticks, exactly as the README spells it; extras exactly as the capture's line 1
  spells them), then prints those lines. Line 1 of every capture is its `$ …` command and is never
  printed; the `[exit N]` line is never printed. Inside the line list:
  - `…` = print one `…` line;
  - `wrap` = fold long lines (`Terminal.print(..., wrap=True)`): tracebacks, npm warnings, the
    `CLI Arguments` line, curl's long OPTIONS commands;
  - `squeeze` = a table re-aligned with two-space gutters, an empty trailing column dropped;
  - `→ (no output)`: the prompt simply returns.
- Typed lines at a container prompt. The `istep` captures (`21`, `24`, `25`, `29`, `33`, `50`,
  `51`, `73`) hold the prompt and the typed line together (`app@f9965bfbee29:/app$ python cli.py …`).
  The scene sets the terminal's prompt to the capture's own (`app@<id>:/app$`, `(app) app@<id>:/app$`
  after `pipenv shell`, root `<id>:/app#` in the frontend's node container) and types the rest of
  that line. The capture opened a fresh llm-rag container for each CLI command (`24`, `25`), so the
  container id changes between them; the `exit` that ended `24` (line 186) is never typed, and a
  GREY chip at the second command says "our capture: a fresh container for each command · stay in
  yours" (S06); S06 says once that the id changes every run. The frontend capture likewise split
  `npm install` (`50`) and `npm run dev` (`51`) across two sessions: `50`'s `exit` (line 50) and
  `51`'s re-entry are never typed, the prompt simply becomes `6c23fe52ca92:/app#` under the same
  kind of GREY chip (S11).
- Crops (ASSETS.md): `33` lines 42 (the harness's readiness `GET /`) and 164 (`GET /capture-done …
  404`) are never printed; `51` lines 54–55 (`/_not-found`, `/capture-done`) are never printed;
  `21`/`33`/`50`/`51` show no base-image pull rows and nothing is said about it; `54`'s
  ChromaDB CREATED/STATUS columns are never printed or spoken; the placeholder key's 421-byte
  size (`06`, `21`) is never highlighted.
- Second terminal. The extras `34`–`45` ran in a second shell while uvicorn served in the first
  (`33`); `52`–`58` likewise while `next dev` served (`51`). The scene shows them in a second
  terminal titled `laptop · second terminal`, prompt `student@laptop:~/cheese-app-v0/api-service$`
  (resp. `…/frontend-ai-chatbot$`). The CORS checks `60`–`63` ran from `student@laptop:~$`.
- Terminal size: the house `term()` (12.6 wide, 22 pt, 65 characters a row, full width). A typed
  command is never cut: it folds at a space onto an indented row; the very long one-liners (the
  `docker exec … urlopen(…)` probes, the curl preflights, the `sed` edits) are shown small in a
  strip and fold. When a picture needs the frame, the terminal shrinks to a 3-row strip along the
  bottom edge; a full terminal and a picture never share the frame.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` from line a to b, header
  `path · lines a–b`; never more than 12 lines on screen at once. Neighbour-repo panels carry the
  repo in the header (`llm-finetuning · gemini-finetuner/cli.py · lines 89–96`). A "README card" is
  a GREY quote of README text with the header `README.md · line n`.
- `TRACKER A3`: the `ReadmeTracker`, top-left, in every walkthrough scene, moves to that step.
  `TRACKER A3 · extra`: same step, caption gets " · extra" while a command the README doesn't have
  is on screen. Six trackers (BRIEF):
  - A = "Prerequisites & Service Account" (`README.md:41-75`), 5 steps: 1 Docker + clone ·
    2 Create llm-service-account + roles · 3 JSON key → secrets/ · 4 Folder tree check ·
    5 Create the network.
  - B = "Build the Vector DB" (`README.md:79-106`), 5 steps: 1 Edit GCP_PROJECT · 2 docker-shell ·
    3 cli char-split · 4 cli recursive-split · 5 Exit (Chroma stays up).
  - C = "Run API Service Container" (`README.md:125-149`), 4 steps: 1 Edit GCP_PROJECT ·
    2 docker-shell · 3 uvicorn_server · 4 /docs.
  - D = "Run Frontend Container" (`README.md:153-180`), 4 steps: 1 docker-shell · 2 npm install ·
    3 npm run dev · 4 Open :3200.
  - E = "The five UI steps" (`README.md:184-255`), 5 steps: 1 Text Chunking · 2 Vector DB UI ·
    3 Chat · 4 Cheese Expert Agent · 5 Pavlos Cheese Model (README heading text, quoted).
  - F = "Shut down" (`README.md:106` + digest §2 checklist), 2 steps: 1 Ctrl-C + exit each ·
    2 docker compose down.
  S07, S08 and S10 are concept scenes with no tracker; S01 has none until the preview.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says "extra" the first time each kind appears (`git log`, `ls`, `tree`, the second
  network command, `docker network ls/inspect`, `docker ps`, the curls, the auth one-liner, the
  line-14 fix, the DNS demo, the CORS preflights, the persistence checks, `docker network rm`). The
  three `sed` edits (`20`, `30`, `32`) carry the GREY tag "our editor" (`20`, `30`: README says
  "update", `sed` is our editor) or `extra` (`32`: the fix is ours).
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per README step);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every console step, browser page, key card and
  Swagger page (schematic; no screenshots, no logos); `recorded · <source>` on every success a
  student sees that this machine could not produce (cli.py's own prints + README.md:98–105, the
  256-float body from rag.py:218–223, S09's door opening for the badge, S12's whole V5 flow, the
  populated collections list from README.md:103/206);
  `at the time of recording` beside Docker 29.8.2, Python 3.12.15, Next.js 14.2.4, `"1.0.0"`, the
  package counts, the build time and the chunk counts when first shown; `erratum` on every
  README/repo slip (the narration says "a small slip" or "a small gap", never "erratum"); the GOLD
  `cost_tag()` ("this bills your project") at S01 (intro, the checklist line), S06 (`--embed`),
  S12 (chat) and S13 (agent, tuned endpoint), and GOLD-on-GREY-dashed on S14's storage rule card.
  There are no `expected` panels in this episode.
- The honest framing (BRIEF, binding): S05's last block says once, plainly, that this machine has
  no Google account and the key in the folder listings is an obviously invalid stand-in removed before
  the cloud steps. From S06 on, every credential failure is taught as the lesson (no identity file →
  no bearer token) and every success carries `recorded` + its source. No chat, agent or tuned-model
  answer text ever appears: those beats describe what to look for, with no output panel.
- `lecture_ref(10, "a–b")` (GREY, top right): one per scene as assigned in the BRIEF (S09 and S13
  have none); spans from SLIDES.md. Lecture diagrams are redrawn in series style; no slide images,
  console screenshots, hand-drawn OAuth images, memes or the film still.
- Spelling on screen and in the subtitles: American ("gray", "authorize").
- Semantic colours (BRIEF, fixed for the whole video):

  | meaning | colour |
  | --- | --- |
  | your laptop: the host shell, the host filesystem, the browser's home | GREY |
  | the cloud: Google's building, Vertex AI, GCS, the token desk, the bearer ticket | BLUE |
  | containers and images: llm-rag-cli, llm-rag-chromadb, api-service, frontend | TEAL |
  | system-wide / host-owned: Docker Desktop itself (little this lecture) | ORANGE |
  | project-owned, protected: `secrets/`, the JSON key, the mounted `/secrets` (RED when the key lands inside a repo) | GREEN |
  | tools: docker, compose, gcloud, uv, pipenv, npm, uvicorn, next | PURPLE |
  | errors and refusals: `DefaultCredentialsError`, 403, 500, the aborted script, the missing CORS header | RED |
  | your turn, the README tracker, the current step | YELLOW |
  | money: every Vertex AI call the student's run makes; storage on S14's card | GOLD |
  | lookups, paths, routes: the Docker networks (PINK streets), Docker DNS, ADC's lookup walk, published-port tunnels, the three browser calls | PINK |
  | future / elsewhere: the deleted hosted deployment, L11's buckets, the metadata server, federation | GREY, dashed |

  Episode-local semantics: the key is GREEN, the bearer token a small BLUE ticket with a timer. An
  open door (an unprefixed published port) is drawn neutral GREY, never GREEN; the `127.0.0.1:`
  narrowing bricks up its Wi-Fi side. The CORS bouncer stands at the browser (CORS is enforced by
  the browser, configured by the server). The guest list never travels: it stays on the Chroma
  house, Chroma checks the page's `Origin` stamp against it and sends back a one-origin pass
  (`access-control-allow-origin: http://localhost:3200`) or nothing, and the bouncer compares that
  pass with the stamp. For a preflighted call, no pass means the query is never sent.
- Running example. The laptop: user `student`, terminal title `laptop`; prompts from the captures:
  `student@laptop:~$`, `student@laptop:~/cheese-app-v0$`, `…/cheese-app-v0/llm-rag$`,
  `…/cheese-app-v0/api-service$`, `…/cheese-app-v0/frontend-ai-chatbot$`. In these captures the
  course folder is the home folder: V3's tree is labelled `AC215/` with a GREY caption "here:
  ~" (S04). A fresh Docker 29.8.2 engine (`x86_64`) stands in for Docker Desktop. The project id
  on screen is always `your-gcp-project`; `ac215-project` and project `129349313346` appear only
  inside CODE panels quoting the repo and in RED story beats. The name "Pavlos" appears only
  inside quoted repo content (tracker E5's README heading, the chunk in `28`, the "Pavlos' fun
  fact" label, the `pavlos_fun_fact_tool` name); the narration says "the instructor" and "the
  fine-tuned cheese model".
- V6, the running map (BRIEF): built in S02 and kept as persistent state (`AppMap`); each scene
  lights its piece (streets S05, Chroma S05, API S09, frontend S11, doors S06/S09/S11, the secrets
  drawer S04) and S15 shows it complete, then unlit.
- Length and parts: narration 4,280 words (`python -m explainer.script`, which counts words; its
  minute figure assumes 155 wpm and is ignored; part 1 = 2,559, part 2 = 1,721). At Kokoro
  af_heart speed 0.9 (≈174 wpm raw) that is ≈24.5 min of narration, ≈28–30 min with typing,
  outputs and ponder timers. Part 1 = S01–S09
  (identity and the cloud, ending when the auth chain closes), part 2 = S10–S15 (addresses and the
  browser). Each part ends on an empty frame.

Notes for scene authors
- TERM/PANEL line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes
  the output body, so pick index = file line − 1.
- Never print `[exit N]` lines, the crops listed above, or the placeholder key's content. Strip a
  trailing `[exit N]` from the last output line too, not only whole `[exit N]` lines (single-line
  captures carry it inline: `23:2`, `34:2`, `37:8`, `63:2`, `74:2`).
- Shared code (`scenes/common.py`, started from L09's): tracker factories `tracker_a` …
  `tracker_f` with the step lists above; prompts `P_LAPTOP_HOME`, `P_REPO`, `P_LLMRAG`, `P_API`,
  `P_FRONTEND` (container prompts come from each capture); tags `extra_tag`, `illustration_tag`,
  `recorded_tag`, `your_turn`, `cost_tag` (GOLD). Set pieces: `AuthChain` (V1), `IamGrid` (V2),
  `SecretsPortal` (V3), `PortDoor` + `TwoArrows` (V4), `CorsBouncer` + `PacketReplay` (V5),
  `AppMap` (V6).
- Never: a real-looking key, key id or client id (fields drawn zeroed, `PLACEHOLDER`); invented
  output (no answer text, no embedding values, no 403 body for the endpoint, no prices); a populated
  collections list without `recorded`; "the API talks to ChromaDB", "the frontend calls the API
  server-side", or `cheese-app-network` carrying traffic in v0 (S10's connect is an experiment,
  undone at once); CORS as protection for the database; an unprefixed door drawn GREEN or called
  safe; `54`'s uptimes.

---

## S01 · Three phone calls, one question — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. A schematic browser window (tag `illustration`), address bar
`localhost:3200/chat`. A question bubble types the README's example, quoted: "How is tolminc
cheese made?" (README.md · line 215). Below it an answer frame and a collapsed drawer labelled
"References · 10 chunks". On "appears", 4–5 GREY skeleton bars (no glyphs) grow into the answer
frame; on "ten book passages", the drawer slides open to 10 empty GREY rows: no answer text
anywhere.
SAY: Here is a cheese chatbot, running on your own laptop. You ask it how Tolminc cheese is made. An answer appears, with ten book passages as references.

SHOW: Freeze. The page dims; the browser figure steps out of the window. Three PINK arrows leave
the browser one after another, numbered ① `:9000`, ② `:8000`, ③ `:9000` (V5 teaser). Arrows ① and
③ continue as thin BLUE lines to a BLUE building at the top right, "Google Cloud".
SAY: Behind that one answer, your browser makes three calls. Two go to a Python server on port 9000, and one goes to a database on port 8000. Behind both server calls, Google's datacenter does the heavy lifting. So who checks that it is really you? And how does a web page find a database hidden inside a Docker container?

SHOW: Zoom out to the V6 skeleton: a GREY laptop house, PINK street stubs, three hollow TEAL
houses, the BLUE building across a public street. Three riddle cards drop in one at a time, each
on its own sentence and fading to a small label before the next (only one card on screen besides
the map; slide 4's trick, this app's numbers): `-p 3200:3000` "two numbers: why?",
`localhost:9000` "which machine is that?", `llm-rag-chromadb` "a name: where is the address?". A
fourth card, slide 11's flip, after the third has faded: a door with a knocker, "once anything can
knock: who's allowed in?". The three labels are kept for S15's recap. `lecture_ref(10, "4, 11–13")` top
right from here to the end of the scene.
SAY: Three small riddles hide in this app. The flag dash p, 3200 colon 3000, has two numbers; why? And localhost 9000: which machine is that? And llm-rag-chromadb is only a name; where is its address? Each one gets its answer today. Then the real question arrives: once anything can knock, who is allowed in?

SHOW: A checklist card: "✓ your clone of cheese-app-v0", "✓ Docker Desktop running", "✓ a GCP
project with billing", the GOLD `cost_tag()` beside the third line ("this lecture bills"). Layout
preview: `tracker_a(1)` appears top-left with a YELLOW ring; the ring cycles the six tracker titles
A–F as "six sections" is said. A 2-row strip terminal (GREY tag "preview", prompt
`student@laptop:~$`) shows a YELLOW `▶ your turn` row tag, then a GREY `extra` row tag, then a GREY
`recorded` chip (one after the other, never stacked). Fade out.
SAY: To follow along you need your clone of cheese-app-v0, Docker Desktop, and a Google Cloud project with billing. This lecture makes real, paid calls to Vertex AI; a gold tag marks each one, and the video ends by shutting everything down. The tracker in the top left follows the README's six sections. A yellow your-turn tag means pause and run it, and a gray extra tag marks a check that is not in the README. Every command is in the study guide, linked below.

---

## S02 · One laptop, three containers, one cloud — `s02_map.py` · `TheMap`

SHOW: TRACKER A1 (tracker A appears: "README › Prerequisites & Service Account", 5 dots). GREY tag
`lecture_ref(10, "5–6, 11")` top right, whole scene. V6 built piece by piece: a GREY laptop house
with a small loop arrow "localhost · 127.0.0.1" (slide 5's rule: every house has one); two
streets inside it, `llm-rag-network` and `cheese-app-network`, drawn as GREY dashed outlines
(caption "planned"; S05 turns each one solid PINK when it is created); three hollow TEAL houses:
`llm-rag` (the loader CLI + Chroma) on the first street, `api-service` and `frontend` on the second.
SAY: First, the map, which stays with us all lecture. Your laptop is one house, and every house has its own loopback address, localhost, which always means this machine. Docker lays two private streets inside it, one per network. Three services will stand on them: the vector database with its loader, the API server, and the web frontend. Each house lights up when its container starts.

SHOW: The browser figure appears on the laptop floor, outside every street. Across a wide public
street, the BLUE Google building with a guarded door. Arrows draw in, honest about who calls whom:
loader → BLUE building and loader → Chroma (PINK, along its street); browser → frontend, browser →
API, browser → Chroma (PINK, from the floor); API → BLUE building. No arrow between API and
Chroma: a GREY strike-through chip quotes README.md · line 127, "it does not connect to ChromaDB".
SAY: Your browser stands on the laptop floor, outside every street. Across the public street sits Google's building, with a guarded door. Now, who calls whom? The loader calls Google and the database. The API calls Google. Your browser calls everything else. And the API never talks to the database; the README says so itself, which surprises almost everyone. Part 2 shows why the browser does so much.

SHOW: TRACKER A1. Full-width laptop terminal (title `laptop`, prompt `student@laptop:~$`). A README
card (`README.md · line 44`): "Cloned this repository to your local machine", GREY caption "no
address given; this is the repo". It types `git clone https://github.com/dlops-io/cheese-app-v0`
→ TERM(laptop/01: 2), then `cd cheese-app-v0` → (no output); the prompt becomes
`student@laptop:~/cheese-app-v0$`. A GREY chip on the terminal title: "Docker 29.8.2 · at the time
of recording" (laptop/00, line 4; not spoken). `▶ your turn`.
SAY: Time to type. The README's prerequisites are short: have Docker installed, and clone this repository. The README gives no address, so here is the repo's address. Pause, and clone it.

SHOW: TRACKER A1 · extra. It types `git log -1 --format='%H %ci'` (extra) → TERM(laptop/02: 2);
`cb6fb945…` and `2026-10-08` highlight. Then `ls -la` (extra) → TERM(laptop/03: 2–11);
`llm-rag` (line 11), `api-service` (9) and `frontend-ai-chatbot` (10) highlight in turn, each
flying a small TEAL chip to its house on the map.
SAY: Two extras, not in the README. An extra git log shows the commit this video uses, from October 8th, 2026; if yours is newer, details may differ. A listing shows llm-rag, api-service, and frontend-ai-chatbot: one folder per house.

SHOW: A kind card, tag `erratum`: a GREY dashed miniature of a hosted setup (a web server on a
cloud machine) crossed out, caption "the app's home page animates the hosted version · its
deployment/ folder was deleted in 2bc29dd"; beside it the solid local map. Fade out.
SAY: One small gap. The app's own home page animates a hosted version, with a web server on a cloud machine. The files for that setup were deleted from the repo. You are running the local version, and this map draws exactly what you run.

---

## S03 · An identity for code — `s03_identity.py` · `IdentityForCode`

SHOW: TRACKER A2. GREY tag `lecture_ref(10, "24–25, 31–38")` top right, whole scene. Concept
first (slide 25 redrawn): an ID badge is minted, GREEN outline, reading
`llm-service-account@your-gcp-project.iam.gserviceaccount.com`; it clips onto a small TEAL server
box; an arrow runs from the server to the BLUE building; no human figure anywhere.
SAY: The second prerequisite creates an identity, but not for you. A service account is an identity for software. Its email looks like this badge: llm-service-account, at your project. Code wears it when it calls Google, with no person and no login screen.

SHOW: Slide 31's rule as a four-row decision card, redrawn: "public metered call → API key" · "an
app acting for a consenting user → OAuth" · "code calling Google → service account" · "code outside
Google, vouched for → federation" (GREY dashed). A YELLOW pointer walks down and stops on row 3,
then slides to row 4, where a CI-runner chip is stamped "vouched for" and a laptop chip "nobody
vouches".
SAY: The lecture gives a rule for choosing. A metered public call gets an API key. An app acting for a consenting user gets OAuth, the sign in with Google flow. Our code calls Vertex AI in your own project, so it gets a service account. The rule's last line says code outside Google should use federation. That needs someone to vouch for your code, the way GitHub vouches for code running in GitHub Actions. A laptop has nobody, so the course hands you a key file instead.

SHOW: TRACKER A2. A schematic console (tag `illustration`; no screenshot, no logo) with the field
values of README.md · lines 48–52, step by step: "IAM & Admin → Service accounts" → "Create service
account · name: llm-service-account" → "Grant this service account access to project: Storage Admin
· Gemini Enterprise Agent Platform User". A small GREY chip under the second role: "formerly
Vertex AI User · role ID roles/aiplatform.user · llm-finetuning README.md:44–46". `▶ your turn`. A
small GREY `extra` card in the corner, not spoken: the `gcloud iam service-accounts create …` and
`gcloud projects add-iam-policy-binding …` equivalents (digest §4 step 1), with `YOUR_PROJECT_ID`.
SAY: Now the console steps. Open IAM and Admin, then Service accounts. Create one named llm-service-account. Grant it two roles, bundles of permissions: Storage Admin, and Gemini Enterprise Agent Platform User. The second role was formerly called Vertex AI User; it is the same role underneath. Pause and create yours.

SHOW: A kind card, tag `erratum`, three lines: "slides: data-service-account, one storage role →
next week's account (L11)" · "this app: the Gemini role does the work; Storage Admin rides along for
L08 reuse" · "slide 45: Storage Object Admin, and only when needed".
SAY: Two notes on the slides. The lecture's demo creates a data service account with one storage role; that is next week's account. And this app never touches storage; that role rides along from the fine-tuning lecture. Grant both anyway, as the README says. The lecture's rule, least privilege, meaning only the access you need, would grant less; part 2 comes back to it.

SHOW: TRACKER A3. Console continued (`illustration`, README.md · lines 54–55): the account → tab
"KEYS" → "ADD Key (Create New Key)" → "JSON"; a file icon downloads. Two banners redrawn in our own
words: "a leaked key is a risk" · "Google disables keys it finds in public repositories". The key
card unfolds (`illustration`): `"type": "service_account"`, `"project_id": "your-gcp-project"`,
`"client_email": "llm-service-account@…"`, `"private_key": "PLACEHOLDER"`,
`"token_uri": "https://oauth2.googleapis.com/token"`, every id zeroed. `private_key` glows RED with
a chip "something you have · one factor". `▶ your turn`.
SAY: On the account's Keys tab, add a key, choose JSON, and a file downloads. Pause and make yours. Inside are your project, the account's email, a token address we use later, and a private key. That private key is the whole secret. It is one factor, something you have, and it works from anywhere, with no second step, until someone deletes or disables it. Treat this file like a password, never like config.

---

## S04 · Two filesystems, one folder — `s04_secrets.py` · `SecretsPortal`

SHOW: TRACKER A3. GREY tag `lecture_ref(10, "38, 42")` top right, whole scene. V3: a file tree
`AC215/` (GREY caption "your course folder · here: ~") holding `cheese-app-v0/` (`llm-rag/`,
`api-service/`, `frontend-ai-chatbot/`) and, beside the repo, `secrets/` in GREEN.
CODE(cheese-app-v0/api-service/docker-shell.sh: 6–11); line 8 `export SECRETS_DIR=$(pwd)/../../secrets/`
highlights. A cursor starts at `api-service/` (label "$(pwd)"), hops `..` to `cheese-app-v0/`,
`..` to `AC215/`, and lands on `secrets/`.
SAY: The README says to copy the key into a secrets folder. Which folder, exactly? The API's script answers on line 8. The path starts where you run it, in api-service. It climbs up twice and lands on the secrets folder, beside the repo, not inside it.

SHOW: A glowing tube connects `AC215/secrets/` to `/secrets` inside a TEAL container silhouette.
CODE(cheese-app-v0/api-service/docker-shell.sh: 19–27) replaces the first panel; line 23
`-v "$SECRETS_DIR":/secrets` highlights, then line 24 `-e GOOGLE_APPLICATION_CREDENTIALS=…` with
line 10's value shown above it, `"/secrets/llm-service-account.json"`. The label
`GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json` slides along the tube and snaps
onto the file, where a small GREY "Google library" chip inside the silhouette reads it. Two
captions: "host path" (GREY, under the tree) and "container path" (TEAL, under the silhouette).
SAY: Then a dash v flag mounts that host folder at slash secrets, inside the container. The secrets directory is a path on your laptop. The Google application credentials variable, which tells Google's library where the key file is, points to slash secrets, a path inside the container. Two filesystems, one folder, and that variable only makes sense after the mount.

SHOW: CODE(cheese-app-v0/llm-rag/docker-compose.yml: 10–12), line 11 `- ../../secrets:/secrets`
highlighted; the same tube redraws from `llm-rag/`, two hops to the same `secrets/`. A GREY note:
"slides: ../secrets · L11's repos sit one level shallower".
SAY: The loader's compose file builds the same portal, counted from its own folder: up two levels, to the same secrets. The lecture's slide climbs only once, because its repos sit one level shallower. Always count the climbs from where the script sits.

SHOW: TRACKER A3 · extra. Laptop terminal, prompt `student@laptop:~/cheese-app-v0$`. It types
`mkdir ../secrets` (extra; GREY tag "the README shows a tree, not a command") → TERM(laptop/04: →
(no output)). TRACKER A3: a GREY file icon slides from "Downloads" into `secrets/` and is renamed
`llm-service-account.json` (`illustration`). TRACKER A4 · extra: it types `cd ..` → (no output),
prompt `student@laptop:~$`; then `tree -L 2 .` (extra) → TERM(laptop/05: 2–11) beside a README card
(`README.md · lines 60–67`), the two trees matching folder for folder (`05`'s line 4, `README.md`,
dimmed: the README's tree omits it). A GREY chip: "no tree? ls -la secrets (next line) checks the
same thing". Then `ls -la secrets` (extra) → TERM(laptop/06: 2–5), the file name highlighted; a
GREY chip: "not .json.json · llm-finetuning README.md:67". `▶ your turn`.
SAY: Make the folder beside your clone, as an extra, then move the download in and rename it llm-service-account dot json. Check that name: hidden extensions can leave dot json dot json. An extra tree view shows the README's layout. Pause and match it.

SHOW: CODE(cheese-app-v0/.gitignore: 1–7); lines 6–7 highlight GREY; a RED dashed slot below
line 7 where no `secrets/` rule exists, caption "no rule for secrets/".
SAY: Now a quiet trap. The repo's gitignore lists the Docker volumes and the outputs. It has no rule for secrets. Nothing protects a key you put inside the repo.

SHOW: The tree with a misplaced key: `cheese-app-v0/secrets/llm-service-account.json` (RED
outline); `AC215/secrets/` beside the repo is absent.
PONDER(8 s, "You save the key inside the repo,\ncheese-app-v0/secrets/llm-service-account.json,\nthen run sh docker-shell.sh from api-service/.\nWhat is in /secrets, and what happens\non the first embedding call?")
SAY: Something to ponder. Suppose you save the key inside the repo instead, in cheese-app-v0 slash secrets, and run the API script from api-service. What does the container find in slash secrets, and what happens on the first embedding call?

SHOW: V3 replay: the cursor still climbs two levels to `AC215/`, finds no `secrets/`; an empty
GREEN-outlined folder pops into existence there with a chip "created by Docker, empty"; the tube
carries nothing; `/secrets` in the silhouette is empty. A RED line under it, quoted from
TERM(laptop/33: 162), the API's own instance (identical text): `google.auth.exceptions.DefaultCredentialsError: File /secrets/llm-service-account.json was not found.`
The misplaced key inside the repo turns RED: "inside a git tree · no rule protects it". Fade out.
SAY: The cursor still climbs twice, to a folder that does not exist. Docker does not complain; it silently creates that folder, empty. So slash secrets is empty, and the first embedding call fails with a default credentials error: file not found. Meanwhile your key sits in a git tree that nothing protects.

---

## S05 · A network, a compose file, a running Chroma — `s05_vectordb.py` · `NetworkAndShell`

SHOW: TRACKER A5. GREY tag `lecture_ref(10, "9–10")` top right, whole scene. Laptop terminal,
prompt `student@laptop:~$`. It types
`docker network inspect cheese-app-network >/dev/null 2>&1 || docker network create cheese-app-network`
(README.md line 74; folds) → TERM(laptop/10: 2). On the map the dashed `cheese-app-network`
outline from S02 turns solid PINK, no houses yet. `▶ your turn`.
SAY: Last prerequisite: the Docker network. The README's command inspects it quietly, and creates it only if that fails. Pause and run it.

SHOW: TRACKER A5 · extra. A YELLOW "?" over the command line, held 2 s on the spoken question; then
it types the same command again (extra; folds) → TERM(laptop/11: → (no output)); a GREEN chip
"exit 0 · nothing new", caption "safe to run twice". Then
`docker network ls` (extra) → TERM(laptop/12: 2–6; squeeze), `cheese-app-network` highlighted. A
GREY sticky note parks in the corner: "inspect … || create · remember this shape".
SAY: What happens if you run it again, as an extra? Nothing: no error, no second network. A command that is safe to run twice is called idempotent. Remember this shape; it comes back soon.

SHOW: TRACKER B1 (tracker B appears: "README › Build the Vector DB", 5 dots). It types
`cd cheese-app-v0/llm-rag` → (no output), prompt `student@laptop:~/cheese-app-v0/llm-rag$`.
CODE(cheese-app-v0/llm-rag/docker-shell.sh: 6–12), line 7 `export GCP_PROJECT="ac215-project" # CHANGE TO YOUR PROJECT ID`
RED. A strip types the edit, shown small with the GREY tag "our editor; use yours" (the `sed` of
TERM laptop/20's line 1; folds) → TERM(laptop/20: 2–5), line 3 `export GCP_PROJECT="your-gcp-project"`
GREEN. `▶ your turn`.
SAY: In the llm-rag folder, the shell script ships with a default project name that is not yours. Update the GCP project variable to your own project ID; we use the sed tool, you use any editor. Pause and edit it. The API needs the same edit later.

SHOW: TRACKER B2. It types `sh docker-shell.sh` (README.md line 88) → TERM(laptop/21: 2–8, …, 34,
…, 37–41). Lines 3–5 (`chromadb/chroma:latest Pulled`, `Network llm-rag-network Created`,
`Container llm-rag-chromadb Created`) highlight one by one; on the map the dashed `llm-rag-network`
outline turns solid PINK and the Chroma house lights TEAL. Lines 6–8 (`pull access denied … Building`) get a GREY chip "not
on Docker Hub → built locally". Lines 38 `Architecture: x86_64` and 40 `Python version: Python
3.12.15` highlight, with `at the time of recording`. CODE(cheese-app-v0/llm-rag/docker-compose.yml:
1–3) small: "every service joins this network". `▶ your turn`.
SAY: Now the README's command: sh docker-shell.sh. Pause and run it. Compose pulls Chroma, creates a network called llm-rag-network, and starts the database on it. Every service in this compose file joins that network automatically. The line that says pull access denied is harmless: that image is not on Docker Hub, so Compose builds it locally. The container's architecture is x86 here; Apple Silicon says aarch64, and needs no special flags.

SHOW: TRACKER B2 · extra. At the capture's prompt `app@3c41bc0606ad:/app$` it types
`ls -la /secrets` (extra) → TERM(laptop/21: 44–47), the file name highlighted (not its size); V3's
tube lights on the map. Then `echo $GOOGLE_APPLICATION_CREDENTIALS $GCP_PROJECT` (extra) →
TERM(laptop/21: 49). CODE(cheese-app-v0/llm-rag/docker-compose.yml: 13–15) small, caption "copied
from the shell that runs compose".
SAY: Two extra checks inside. The key file shows up in slash secrets, through the portal. And both variables are set, copied by Compose from the launching script, which is why you always start through it.

SHOW: A GREY card whose three lines build on their sentences: "This recording machine has no
Google account. · The key file in the folder listings is an obviously invalid stand-in. · It was
removed before the cloud steps." On "fails exactly the way a missing key fails", a RED chip
`DefaultCredentialsError` ("what a missing key looks like") flies onto the first, empty slot of a
small V1 outline as a teaser; then a GREY `recorded` chip ("a success you will see on your
machine · source named") settles under the card. The terminal's `exit` (laptop/21: 50–51)
is not shown: S06 continues inside a container.
SAY: One honest note about this recording. This machine has no Google account. The key file you just saw is an obviously invalid stand-in. It is there so the folder listings match the README, and it was removed before the cloud steps. So from here on, every cloud call fails exactly the way a missing key fails. That is the most common mistake in this lecture, and you will learn it on sight. Every success you will see on your machine is tagged recorded, with its source.

---

## S06 · Chunks for free, embeddings need a key — `s06_chunks.py` · `ChunksNeedAKey`

SHOW: TRACKER B3. Terminal at the capture's prompt `app@f9965bfbee29:/app$`; a GREY chip: "our
capture opened a fresh container for each command · staying in one works too". It types
`python cli.py --chunk --embed --load --chunk_type char-split` (README.md line 94; the capture's
line 12; folds) → TERM(laptop/24: 14–17, …, 43–44). Line 15 `Number of files to process: 11` and
lines 43–44 (`Processing file: …/Tolminc Cheese.txt`, `Number of chunks: 24`) highlight.
`▶ your turn` (the GOLD tag of the next block lands on the same command line).
SAY: Inside the container, the README's first command chunks, embeds and loads, with char split. The ID in the prompt changes every run. Chunking runs for real: 11 books, cut into short passages, and the Tolminc book becomes 24 chunks.

SHOW: The GOLD beat, before the next lines print: GOLD `cost_tag()` "this bills your project" on
the command line; a small GOLD meter; slide 13's warning redrawn as one line, "an unprotected AI
endpoint invites runaway bills". GREY tag `lecture_ref(10, "13")` top right during this block only.
SAY: Before the next step, a gold tag. The embed step sends every chunk to Google's embedding model, about 7 million characters across both runs, by our estimate. That bills your project; check the current pricing page. The lecture warns about runaway bills, and this is where they start.

SHOW: TERM(laptop/24: 115–117, …, 125, …, 165–166, …, 185; wrap). Line 166
`http_request.headers['Authorization'] = f'Bearer {self._access_token()}'` YELLOW; line 185 RED.
V1 teaser above the terminal strip: five link slots, left to right (key file · ADC's magnifying
glass · signed JWT · token desk · bearer ticket); the glass looks into an empty `/secrets`, finds
nothing, and the whole chain greys out. Then `exit` (line 186) → the laptop prompt returns.
SAY: Here is that missing-key failure. The embed step stops while building its authorization header, a bearer token, which needs a key. Default credentials error: file slash secrets slash llm-service-account dot json was not found. No key, no token, so the very first cloud request dies at authentication.

SHOW: A GREY card, tag `recorded · cli.py prints (231, 236, 278, 285, 159–160) + README.md:98–105`,
the success checkpoints as plain lines in the code's own words: `embed()` · `Number of files to
process: 11` · `Creating collection: char-split-collection` · `Collection 'char-split-collection'
did not exist. Creating new.` · `Finished inserting N items into collection
'char-split-collection'` (a literal N). No timings, no counts.
SAY: On your machine, with a real key, the run continues. It embeds every book, creates the char split collection, and finishes inserting the items, book by book.

SHOW: TRACKER B4. At the capture's prompt `app@ae87a706e772:/app$` it types
`python cli.py --chunk --embed --load --chunk_type recursive-split` (README.md line 95; folds) →
TERM(laptop/25: 14–17, …, 185; wrap); line 17 `Number of chunks: 2147` and line 185 highlighted, the
GOLD tag again. `▶ your turn`. TRACKER B5: it types `exit` (README.md line 106's "after you exit";
the capture's line 186) → TERM(laptop/25: 187), and the laptop prompt
`student@laptop:~/cheese-app-v0/llm-rag$` returns. `▶ your turn`. TRACKER B5 · extra: it types
`wc -l outputs/chunks-char-split-*.jsonl | tail -1; wc -l outputs/chunks-recursive-split-*.jsonl | tail -1`
(extra; folds) → TERM(laptop/27: 2–3), `8248` and `14228` highlighted with `at the time of
recording`; CODE(cheese-app-v0/llm-rag/cli.py: 184–200) small, lines 186 (`chunk_overlap = 20`) and
199–200 (no overlap given) highlighted, caption "default overlap: 200".
SAY: The second command does the same with recursive split. Pause and run both, then type exit. An extra count shows 8,248 chunks for char split and 14,228 for recursive split, at the time of recording. Recursive split makes more chunks because it keeps a default overlap of 200 characters.

SHOW: TRACKER B5 · extra. It types `ls -la outputs | head -16` (extra) → TERM(laptop/26: 5–15);
line 15 `chunks-char-split-Womans Institute Library of Cookery.jsonl` highlights YELLOW. A kind
card, tag `erratum`: CODE(cheese-app-v0/llm-rag/cli.py: 177–178), `filename.split(".")[0]` RED,
caption "cut at the first dot → no author metadata · fix: os.path.splitext". Then
`head -1 'outputs/chunks-char-split-Tolminc Cheese.jsonl' | cut -c1-300` (extra; folds) →
TERM(laptop/28: 2; wrap), caption "the book the opening question asks about".
SAY: The chunk files land on your laptop through the app mount. One small slip shows here: a book title is cut at its first dot, so its chunks get no author, and the agent's author filter never finds them. The fix is splitext. Last, one real Tolminc chunk.

SHOW: TRACKER B5 · extra. A README card (`README.md · line 106`): "ChromaDB keeps running after you
exit the CLI container … To stop it, run docker compose down inside llm-rag", GREY chip "we stop it
in part 2". It types `docker ps` (extra) → TERM(laptop/22: 2–3; squeeze), the
`0.0.0.0:8000->8000/tcp` cell ringed GREY ("hold this for part 2"); on the map a neutral GREY door
`8000→8000` opens in the laptop wall. `curl -s http://localhost:8000/api/v2/version` (extra) →
TERM(laptop/23: 2), `"1.0.0"` with `at the time of recording`. A GREY note: "Optional: LLM RAG
Tutorial (README.md:110–122) · L05 material · exercises.md". Fade out.
SAY: After that exit, the README says ChromaDB keeps running, and an extra docker ps confirms it, on port 8000. An extra curl asks for its version: 1.0.0, at the time of recording. The README also says how to stop it, with docker compose down; that comes at the very end. Its optional RAG tutorial is lecture 5 material.

---

## S07 · ADC: from key file to bearer token — `s07_adc.py` · `AdcToToken`

SHOW: No tracker (concept scene). GREY tag `lecture_ref(10, "19–31, 42")` top right, whole scene.
CODE(cheese-app-v0/api-service/api/routers/rag.py: 14–27); line 26
`llm_client = genai.Client(vertexai=True, project=GCP_PROJECT, location="global")` YELLOW; a GREY
chip "no key path anywhere". Slide 42's chain redrawn beside it: "mounted key → env var → client →
?? → IAM check"; the "??" box opens into V1.
SAY: So what failed, exactly? Look at the line that builds the API's Google client. It names a project and a location, and nothing else. Nothing in this repo ever opens the key file. A library does it for you, by a convention called application default credentials, or ADC.

SHOW: V1's magnifying glass walks three slots: (1) "the file named by
GOOGLE_APPLICATION_CREDENTIALS · a service-account key · this tutorial" GREEN; (2) "gcloud auth
application-default login · you, through a consent screen" GREY; (3) "the metadata server · the
account attached to a VM, a Cloud Run service, a pod" GREY dashed, chip "L13–L15". A TEAL container
outline closes around the slots: slots 2 and 3 inside it are empty boxes.
SAY: ADC looks in three places, in order. First, the file named by the Google application credentials variable: a service account key, which is this tutorial. Second, a login file that the gcloud tool writes for you, as a person. Third, the metadata server, when your code runs inside Google's cloud. Inside these containers, only the first place exists.

SHOW: Slot 1 lights. The key card slides out; its `private_key` field morphs into a pen and signs a
small envelope labelled "JWT · signed". The envelope flies to a BLUE desk labelled
`oauth2.googleapis.com/token` (the key card's own `token_uri` glows as it passes), and a small BLUE
ticket returns with a timer "≈ 60 min". The ticket staples onto three outgoing HTTPS requests
labelled `Authorization: Bearer …`; the pen and the key card stay on the laptop side, GREEN.
SAY: Now the clever part. The library signs a small note with your private key, a JSON web token, and sends it to Google's token desk, the address written in your key file. Back comes an access token, valid for about an hour. That token rides on every request as a bearer header. Your private key never leaves your machine; only the short-lived ticket travels.

SHOW: The ticket's timer runs out; the ticket greys, and a fresh one mints itself through the same
chain. A GREY bridge card: the lecture's OAuth flow (slides 19–23 redrawn, small) ending at the
same desk, its consent-screen step crossed out, caption "same desk · no person, no consent screen".
SAY: When the hour runs out, the library quietly gets a new token. This is the same token desk that the lecture's OAuth diagram ends at. The consent screen simply drops out, because no person is there to consent.

SHOW: Strip terminal, prompt `student@laptop:~/cheese-app-v0/llm-rag$`. It types
`sh docker-shell.sh` → TERM(laptop/29: 6–7), then at the capture's prompt `app@bccd254e50ae:/app$`
`ls -la /secrets` (extra) → TERM(laptop/29: 13–15), no file; then the one-liner (extra; folds)
`python -c "import google.auth; c, p = google.auth.default(); print(type(c).__name__, getattr(c, 'service_account_email', None), p)"`
→ TERM(laptop/29: 17, …, 25–26, …, 30; wrap); line 30 RED. On V1, slot 1 points at an empty
`/secrets`; slots 2 and 3 stay empty. Then `exit` (line 31) → laptop prompt.
SAY: Here is ADC caught in the act, as an extra. With slash secrets empty, a one-line Python check asks ADC who we are. The first place points at a missing file, and the other two do not exist in a container, so it gives up with the same error.

SHOW: A misconception card: a GREY laptop terminal with
`export GOOGLE_APPLICATION_CREDENTIALS=~/secrets/llm-service-account.json` crossed out RED, caption
"on your Mac: authenticates nothing in a container"; beside it the correct pair, host folder → mount
→ container path, drawn as V3's tube. Fade out.
SAY: One common mix-up. Setting that variable on your Mac authenticates nothing inside a container. The path must exist inside the container. That is why the scripts set a container path, and mount the host folder separately.

---

## S08 · IAM: may this identity do this, here? — `s08_iam.py` · `IamGrid`

SHOW: No tracker (concept scene). GREY tag `lecture_ref(10, "26, 35, 42, 45")` top right, whole
scene. A title card: "authentication: who are you? · authorization: what may you do, and where?".
V2: the grid. Rows (principals): `you`, `llm-service-account`, "the instructor's account". Columns
(resources): `your-gcp-project`, `ac215-project`, `project 129349313346`. A GREEN role token
`roles/aiplatform.user` drops into (llm-service-account, your-gcp-project); a GREY token "Storage
Admin · granted, unused by v0" lands beside it.
SAY: Authentication proved who you are. Authorization decides what you may do, and where. Google calls this IAM: a grid of identities, roles, and resources. Your service account holds the Gemini user role in your project, and that green cell does all the work. Storage Admin sits beside it, granted but never used by this app.

SHOW: Three PINK request arrows fire in turn. (1) embed → `your-gcp-project`: GREEN check. (2) the
same embed with the unedited default, CODE(cheese-app-v0/api-service/docker-shell.sh: 9) beside it
(`ac215-project` RED) → RED "403". (3) a tuned-model call → `project 129349313346` → RED "403",
parked with a GREY pin "part 2".
SAY: Three requests test three cells. An embedding in your own project is allowed. The same call with the script's unedited default project is refused with a 403, because your account has no role there. That is why you edit both scripts. The third arrow waits for part 2.

SHOW: The error ladder, a two-rung card. Lower rung, RED: "DefaultCredentialsError, or 401 →
authentication: no token · check the path, the mount, the file name". Upper rung, RED: "403 →
authentication worked, authorization failed · missing role · wrong project · API not enabled".
SAY: Now the error ladder. A default credentials error, or a 401, means no token at all: check the path, the mount, and the file name. A 403 means authentication worked, but authorization failed. The cause is a missing role, the wrong project, or an API that is not enabled.

SHOW: A kind card, tag `erratum`: "no README in this repo says to enable the Vertex AI API ·
probably done in an earlier lecture · if not, the 403 says so, with an enable link". Under it a
small GREY `extra` chip: `gcloud services enable aiplatform.googleapis.com`.
SAY: That last cause is a small gap: no README here tells you to enable the Vertex AI API. It was probably done in an earlier lecture. If not, the 403 names it, with a link, and one extra gcloud command enables it.

SHOW: The grid returns; arrow (3)'s target column pulses.
PONDER(8 s, "Your key works for embeddings. You paste the\ninstructor's endpoint projects/129349313346/….\nWhich part decides whose IAM is checked:\nGCP_PROJECT, the key's project_id, or the path?")
SAY: Something to ponder. Your key works for embeddings. Now you paste the instructor's fine-tuned endpoint, which begins with projects and a long number. Which part decides whose IAM is checked: the project variable, the project inside your key, or the endpoint path?

SHOW: The endpoint path lights as the resource; arrow (3) lands in column `project 129349313346`,
row `llm-service-account`: an empty cell, RED 403. Then a closing picture: one GREEN badge, two
doors, a Vertex door ("Gemini role") and a GREY dashed bucket door ("storage role"), caption "one
badge · grants differ". Fade out.
SAY: The path. The endpoint is the resource, and it names someone else's project, where your account has no role. So it is a 403; part 2 shows it. And one badge can open many doors: the same identity reaches Vertex through one role, and a storage bucket through another. Grants differ; the badge does not.

---

## S09 · Run the API, and survive line 14 — `s09_api.py` · `ApiService`

SHOW: TRACKER C1 (tracker C appears: "README › Run API Service Container", 4 dots). It types
`cd ../api-service` → (no output), prompt `student@laptop:~/cheese-app-v0/api-service$`. A strip
types the edit, shown small with the GREY tag "our editor" (TERM laptop/30's line 1; folds) →
TERM(laptop/30: 2–6), line 4 `export GCP_PROJECT="your-gcp-project"` GREEN. `▶ your turn`.
SAY: Last stretch of part 1, the API. In the api-service folder, make the second project-name edit. Pause and do it.

SHOW: TRACKER C2. It types `sh docker-shell.sh` (README.md line 134) → TERM(laptop/31: 2), RED.
The map's API house stays dark. `▶ your turn`.
SAY: Then the README's command, sh docker-shell.sh. Pause and run it. It dies at once: the network already exists.

SHOW: TRACKER C2 · extra. A kind card, tag `erratum`. CODE(cheese-app-v0/api-service/docker-shell.sh:
1–16): line 4 `set -e` YELLOW, line 14 `docker network create cheese-app-network` RED. S05's sticky
note returns beside it: "inspect … || create". A strip types the fix (extra; shown small, folds)
→ TERM(laptop/32: 2), the new line 14 GREEN.
SAY: This is the biggest slip in the repo, and it is not your fault. Line 14 creates the network unconditionally, and set dash e, on line 4, stops the script at the first error. So it fails every time the network exists, including right after the README's own network step. The line arrived in the repo's very last commit. The fix is the shape you met earlier: make line 14 the README's inspect-or-create command. This fix is ours, an extra.

SHOW: TRACKER C2. It types `sh docker-shell.sh` again → TERM(laptop/33: 3, 16, …, 26–32), then the
prompt `(app) app@ed21c759d782:/app$`. Line 3 `Building 188.2s` and line 16 `RUN pipenv sync`
highlight with `at the time of recording`; the GREEN help text (lines 28–30) lists
`uvicorn_server`. TRACKER C3: at that prompt it types `uvicorn_server` (README.md line 140) →
TERM(laptop/33: 35–41). Line 36 `Uvicorn running on http://0.0.0.0:9000` is ringed GREY ("hold
0.0.0.0 for part 2"); line 41 `Application startup complete.` GREEN. On the map the API house
lights, and a neutral GREY door `9000→9000` opens in the laptop wall. `▶ your turn` on both.
SAY: Run the script again. The first build installs 170 pinned packages from Pipfile.lock, which took about three minutes at the time of recording. You land in a pipenv shell. Type uvicorn server, and the API starts on port 9000, listening on 0.0.0.0. Pause and run both.

SHOW: TRACKER C3 · extra. A second terminal (title `laptop · second terminal`, prompt
`student@laptop:~/cheese-app-v0/api-service$`) types
`curl -s -i 'http://localhost:9000/rag/embedding?text=hello'` (extra) → TERM(laptop/37: 2, 8) RED.
The server terminal prints TERM(laptop/33: 46, …, 104–105, …, 143, …, 162; wrap): the access line
`"GET /rag/embedding?text=hello HTTP/1.1" 500 Internal Server Error`, the frame in `rag.py`, the
bearer line YELLOW, the final `DefaultCredentialsError` RED. V1 above the strip: the first link
greys out again.
SAY: The server started cleanly with an empty secrets folder, because the Google client is built without credentials. The failure waits for the first real request. An extra curl asks for an embedding and gets a 500. The server log shows the same default credentials error, raised while building the bearer header. A green startup is not an authenticated startup.

SHOW: A GREY card, tag `recorded · rag.py:218–223 · EMBEDDING_DIMENSION = 256 (rag.py:17)`:
`{"embedding": [ … 256 floats … ]}` drawn as 256 thin BLUE bars, no values; CODE(cheese-app-v0/llm-rag/cli.py:
26) small beside it, `EMBEDDING_DIMENSION = 256`, caption "must match". V1 runs in full above it:
key file → ADC → signed JWT → token desk → bearer ticket → `200`, every link lit at once.
SAY: With a real key, the same request returns a list of 256 numbers, the embedding. That length must match the loader's, or the database queries fail. And the whole chain lights up: key file, lookup, signed note, token desk, bearer ticket, and a 200.

SHOW: TRACKER C4 · extra. The second terminal types `curl -s http://localhost:9000/` (extra) →
TERM(laptop/34: 2); `curl -s -o /dev/null -w '%{http_code} %{content_type}\n' http://localhost:9000/docs`
(extra; folds) → TERM(laptop/35: 2), with a schematic Swagger page (tag `illustration`) beside it;
then the route list (extra; the `curl … openapi.json | python3 -c …` line, shown small, folds) →
TERM(laptop/36: 2–7) beside a README card (`README.md · lines 263–269`). `▶ your turn` on the
README's `/docs` step (README.md line 149).
SAY: The README's last step here: open localhost 9000 slash docs in your browser. Pause and look. Extra curls show the welcome message, the docs page, and the README's five routes, plus a root route.

SHOW: End of part 1 on V6: the BLUE building's door opens for the badge; the API house glows on
its street. A YELLOW question card slides in: "The API is up on your laptop. How does a web page
find it, and who else can?" Fade to an empty frame (end of part 1).
SAY: The auth chain is complete, and the API is answering on your laptop. Leave it running. Part 2 asks two questions: how does a web page find this API, and who else can?

---

## S10 · A name is not localhost — `s10_names.py` · `TwoAddresses`

SHOW: No tracker (every command is an extra). GREY tag `lecture_ref(10, "5–6, 10")` top right,
whole scene. V4: one Chroma box, two arrows in. A PINK arrow `llm-rag-chromadb:8000` from the loader
house, along the `llm-rag-network` street, with CODE(cheese-app-v0/llm-rag/cli.py: 30–31) beside it.
A GREY arrow `localhost:8000` from the browser on the laptop floor, through the wall door
`8000→8000`.
SAY: Part 2 starts with addresses, and this scene has no README steps: every command is an extra. The loader dialed the database by name: llm-rag-chromadb, port 8000. Your browser will ring localhost 8000, through a door in the laptop wall. One server, two addresses. Why can they not swap?

SHOW: Each TEAL house grows its own small loop arrow "localhost" (slide 5's rule, now from inside a
container). Then a phone book on each street (slide 10 redrawn): `llm-rag-network` lists
`llm-rag-chromadb`, `cheese-app-network` lists `llm-rag-analysis-api-service`. A strip shows
`docker network inspect cheese-app-network` (extra) → TERM(laptop/40: 30–37), line 35
`"IPv4Address": "172.19.0.2/16"` highlighted, caption "the API's address on its street · yours will
differ".
SAY: Each container has its own network namespace, so each one has its own localhost. Inside a container, localhost means that container. Names work through Docker DNS, a phone book on each street. Addresses change when containers restart, but names do not. This extra inspect shows the API's address on its street. Yours will differ, which is the point: dial names, not addresses.

SHOW: Strip terminal, second terminal prompt `student@laptop:~/cheese-app-v0/api-service$` (the API
still running). It types
`docker exec llm-rag-analysis-api-service python -c "import urllib.request; print(urllib.request.urlopen('http://llm-rag-chromadb:8000/api/v2/version', timeout=10).read())"`
(extra; shown small, folds) → TERM(laptop/41: 47) RED. On the map, a probe from the API house finds
no `llm-rag-chromadb` in its street's phone book.
SAY: Now the proof, all extras. From inside the API container, ask for the database by name. Name or service not known. The API's street has no entry for that name.

SHOW: The API house pulses with a YELLOW "?".
PONDER(8 s, "You want the API itself to query Chroma.\nWhat URL does it use, and what single\nDocker command makes that name resolvable?")
SAY: Something to ponder. Suppose you want the API itself to query the database. What address would it use, and what single Docker command makes that name resolve?

SHOW: It types `docker network connect cheese-app-network llm-rag-chromadb` (extra) →
TERM(laptop/42: → (no output)); on the map the Chroma house grows a second door onto
`cheese-app-network`, and its name joins that street's phone book. The same exec (extra; folds) →
TERM(laptop/43: 2), `b'"1.0.0"'` GREEN. Then the localhost variant
`docker exec llm-rag-analysis-api-service python -c "import urllib.request; print(urllib.request.urlopen('http://localhost:8000/api/v2/version', timeout=10).read())"`
(extra; folds) → TERM(laptop/44: 45) RED; the probe loops back into the API house itself.
SAY: Connect the database to the API's network as well, and the same name answers with Chroma's version. Docker DNS works on a shared street. And localhost 8000, from inside the API? Connection refused. Inside a container, localhost is that container, and nothing there listens on 8000.

SHOW: It types `docker network disconnect cheese-app-network llm-rag-chromadb` (extra) →
TERM(laptop/45: → (no output)); the second door vanishes, caption "back to the tutorial's state". A
README card (`README.md · line 127`): "it does not connect to ChromaDB". A kind card, tag
`erratum`: CODE(cheese-app-v0/frontend-ai-chatbot/next.config.js: 19–25), line 23
`"http://rag-system-api-service:9000/docs"` dimmed RED, caption "no such container here · use
localhost:9000/docs". Fade out.
SAY: Then disconnect it, back to the tutorial's setup. That was only an experiment. Nothing in this app needs that shortcut, because the browser makes every call. One small slip: the frontend's config still forwards its docs path to a container name that does not exist here. For the API docs, use localhost 9000 slash docs, as the README says.

---

## S11 · One server, two addresses — `s11_frontend.py` · `FrontendPorts`

SHOW: TRACKER D1 (tracker D appears: "README › Run Frontend Container", 4 dots). GREY tag
`lecture_ref(10, "4, 7–9")` top right, whole scene. A new terminal, prompt
`student@laptop:~/cheese-app-v0/frontend-ai-chatbot$`. It types `sh docker-shell.sh` (README.md
line 161) → TERM(laptop/50: 3, …, 9, …, 19); the root prompt `d263d94eb5c2:/app#` appears.
CODE(cheese-app-v0/frontend-ai-chatbot/docker-shell.sh: 8–11) small, `-p 3200:3000` highlighted.
`▶ your turn`.
SAY: Leave the API running, and open a new terminal in the frontend folder. Run its shell script; pause and do it. The image holds just Node and a shell, so you run npm yourself; the hash sign means you are root.

SHOW: TRACKER D2. At the prompt it types `npm install` (README.md line 167) → TERM(laptop/50:
22–26, …, 28; wrap); the deprecation lines GREY, line 28 `added 773 packages, and audited 774
packages in 1m` with `at the time of recording`. A small V3 echo: `node_modules/` appears in the
host folder through the `/app` tube. `exit` (line 50) → laptop prompt; `sh docker-shell.sh` again
→ prompt `6c23fe52ca92:/app#` (the capture ran each step in its own session). TRACKER D3: it types
`npm run dev` (README.md line 168) → TERM(laptop/51: 23–36); the telemetry notice (31–34) prints
GREY; line 26 `▲ Next.js 14.2.4` with `at the time of recording`; line 27
`- Local:        http://localhost:3000` ringed RED-dashed, caption "the container's view"; line 36
`✓ Ready in 1648ms` GREEN. `▶ your turn` on both.
SAY: Then npm install: 773 packages at the time of recording, with deprecation warnings you will see too. They land in your folder through the mount, so run npm only inside the container. Then npm run dev. Next.js says ready, version 14.2.4 at the time of recording, and prints the line that fools everyone: local, localhost 3000. Pause and run both.

SHOW: TRACKER D4 · extra. A second terminal (prompt `student@laptop:~/cheese-app-v0/frontend-ai-chatbot$`)
shows three angles, stacked: (a) `curl -sS --max-time 10 http://localhost:3000/` (extra) →
TERM(laptop/53: 2) RED; (b) `curl -s --max-time 300 -o /tmp/l10-home.html -w 'HTTP %{http_code}\n' http://localhost:3200/ && grep -o '<title>[^<]*</title>' /tmp/l10-home.html`
(extra; shown small, folds) → TERM(laptop/52: 2–3) GREEN; (c)
`docker exec llm-rag-analysis-frontend-ai-chatbot wget -qO- -T 10 http://localhost:3000/ | grep -o '<title>[^<]*</title>'`
(extra; shown small, folds) → TERM(laptop/55: 2) GREEN. Then a schematic browser at
`localhost:3200` (tag `illustration`). `▶ your turn` on the README's step (README.md line 177).
SAY: Three extra checks, from three angles. From your laptop, localhost 3000 fails to connect. From your laptop, localhost 3200 answers with the RAG app. And from inside the container, localhost 3000 answers with the same page. Now open localhost 3200 in your browser; pause and look.

SHOW: V4 part 2: the wall door `3200→3000`; an arrow from the browser passes through and the
number riding on it morphs 3200 → 3000 (slide 9's tunnel). Then `docker ps` (extra) →
TERM(laptop/54: 2–3; squeeze) — the frontend row only, its `0.0.0.0:3200->3000/tcp` cell
highlighted (the Chroma row is not printed: its uptime is a capture artifact).
SAY: That is the tunnel. The flag dash p, 3200 colon 3000, means that host port 3200 forwards to container port 3000. Next listens on 3000 inside its own house, and your browser knocks on 3200 outside. One server, two addresses. An extra docker ps shows the same door.

SHOW: The 0–65535 number line (10 s): three bands, "0–1023 · system" (22, 80, 443), "1024–49151 ·
registered · pick yours here" (3000, 3200, 8000, 9000 drop in), "49152–65535 · dynamic · a
throw-away port the OS picks for each outgoing call".
SAY: Port numbers come in three bands. The low ones belong to the system, like 80 and 443. The middle band is where you pick yours: 3000, 3200, 8000, and 9000. The top band holds throw-away ports that your computer picks for every outgoing call.

SHOW: The honest beat, 0.0.0.0 twice. Left: CODE(cheese-app-v0/api-service/docker-entrypoint.sh:
6–9), `--host 0.0.0.0` highlighted, caption "listen: every interface of the container". Right: the
`0.0.0.0:3200->3000/tcp` cell, caption "publish: every interface of the laptop". On the map the
wall doors face two sides, the laptop's loopback and a "Wi-Fi" street; a GREY neighbour figure on
the Wi-Fi street walks up to door 9000 (all doors neutral GREY, never GREEN). Then a diagram only,
no capture: `-p 127.0.0.1:9000:9000` bricks up the Wi-Fi side of door 9000; GREY caption "port_toy
(L04) wrote 127.0.0.1:".
SAY: Now 0.0.0.0 has appeared twice, and they are different facts. The API server listens on all of the container's interfaces, so the tunnel can reach it. Docker publishes on all of your laptop's interfaces, unless you add a prefix. The ports lecture wrote 127.0.0.1 before its port, but this app writes none. So these doors face your Wi-Fi too, and anyone on that network can knock. Adding 127.0.0.1 before the host port bricks up that side.

SHOW: A small GREY note card: README.md · lines 179–180, "Use Chrome browser for best
performance", caption "likely inherited from the hosted L05 site". Fade out.
SAY: The README also says to use Chrome. Locally, other browsers should work too, but stick with the instructions.

---

## S12 · The browser is the integrator — `s12_browser.py` · `BrowserIntegrator`

SHOW: TRACKER E1 (tracker E appears: "README › The five UI steps", 5 dots).
CODE(cheese-app-v0/frontend-ai-chatbot/.env.development: 1–4), line 4
`NEXT_PUBLIC_BASE_API_URL=http://localhost:9000` YELLOW; CODE(cheese-app-v0/frontend-ai-chatbot/src/services/Common.js:
1–2) below it. An arrow carries the address out of the container into a JavaScript bundle, which
flies to the browser on the laptop floor.
SAY: Where does the page learn the API's address? From this setting, baked into the JavaScript your browser downloads. So it must be an address your browser can reach: localhost 9000, never a container name.

SHOW: TRACKER E1. A schematic browser at `localhost:3200/chunkviz` (`illustration`): book text
splits into coloured chunks inside the window; no arrow leaves the laptop. A strip shows TERM(laptop/56:
2–3) (extra; the curl shown small). `▶ your turn`. TRACKER E2: the browser at
`localhost:3200/chromaui` (`illustration`), the form's defaults from
CODE(cheese-app-v0/frontend-ai-chatbot/src/app/chromaui/page.jsx: 22–27): `http://localhost:8000`,
`default_tenant`, `default_database`; "Connect" sends a PINK arrow from the browser to door 8000.
A strip on `student@laptop:~$` types
`curl -s http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections`
(extra; folds) → TERM(laptop/63: 2), `[]`, caption "ours: empty"; beside it a GREY card, tag
`recorded · README.md:103, 206`: "char-split-collection · recursive-split-collection". `▶ your turn`.
SAY: Step 1 of 5, text chunking, runs entirely in your browser: no API, no cloud, no bill. Step 2 is the vector database UI: connect to localhost 8000 with the defaults. Pause and try both. Our extra listing is empty, because nothing could be embedded here; yours shows two collections.

SHOW: TRACKER E3. The browser at `localhost:3200/chat` (`illustration`), the README's example
question typed; GOLD `cost_tag()` "each question: 1 embedding + 1 generation". V5 in full beside
CODE(cheese-app-v0/frontend-ai-chatbot/src/components/chat/ChatComponent.jsx: 161–173): packet ①
`GET :9000/rag/embedding` (line 163) carries the question to door 9000; a BLUE bearer ticket rides
on to the BLUE building; 256 small bars return. `▶ your turn`.
SAY: Step 3 is the chat, with a gold tag: each question costs one embedding and one Gemini answer. Pause and ask one. Now follow it as three calls. Call one goes to the API, which asks Google, and 256 numbers come back.

SHOW: Packet ② `POST :8000/…/collections/<id>/query` (line 164), with
CODE(cheese-app-v0/frontend-ai-chatbot/src/services/DataService.js: 34–43), line 36
`"n_results": 10` highlighted. An origin card: `http://localhost:3200` · `:9000` · `:8000`,
"scheme + host + port: three origins". A small OPTIONS packet knocks first at door 8000; Chroma
hands back its two-line guest list, CODE(cheese-app-v0/llm-rag/docker-compose.yml: 25–26); the
bouncer figure stands at the browser's edge and checks the page's `Origin: http://localhost:3200`
stamp against it. Ten chunk cards return.
SAY: Call two sends those numbers to the database, for the 10 nearest chunks. An origin is scheme, host and port, so a page from 3200 calling 8000 crosses origins. The browser first knocks with a preflight, and the database answers from its guest list: the course's hosted site, and localhost 3200. Your browser is the bouncer that enforces it.

SHOW: Packet ③ `POST :9000/rag/llm-response` (lines 165–171): the question plus ten chunks; an
empty answer frame returns (no text). A strip on `student@laptop:~$` types the preflight (extra;
shown small, folds)
`curl -s -D - -o /dev/null -X OPTIONS -H 'Origin: http://localhost:3200' -H 'Access-Control-Request-Method: POST' http://localhost:8000/api/v2/tenants/default_tenant/databases/default_database/collections`
→ TERM(laptop/60: 2, 6) GREEN; then the same with `Origin: http://localhost:3300` (extra) →
TERM(laptop/61: 2–6), a RED dashed gap where line 6 of the first answer stood, caption "no
access-control-allow-origin". Then TERM(laptop/38: 2, 6) (extra; the preflight to the API from part
1's second terminal, `Origin: http://localhost:3300`): `access-control-allow-origin: *`, with
CODE(cheese-app-v0/api-service/api/service.py: 13–20) small.
SAY: Call three sends the question and ten chunks to the API, and the answer returns. An extra preflight from origin 3200 gets the allow origin header; from 3300, it is missing. The API answers with a star: any page may use its replies.

SHOW: Both doors pulse; a `:3300` stamp hovers over a fresh packet.
PONDER(8 s, "You republish the frontend at -p 3300:3000\nand ask a question. Which of the three calls\nfails, and does curl care?")
SAY: Something to ponder. You republish the frontend on port 3300 and ask a question. Which of the three calls fails, and does curl care?

SHOW: V5 replay with the `:3300` stamp: ① GREEN (the API's `*`); ② the bouncer at the browser
refuses to hand Chroma's reply to the page, RED; ③ never leaves the browser, GREY dashed, caption
"awaits call 2 · ChatComponent.jsx:163–171". A `curl` figure walks straight to door 8000, past no
bouncer, and gets an answer. A last chip: "127.0.0.1:3200 ≠ localhost:3200".
SAY: Call one works, because the API allows anyone. Call two is blocked by the browser. Call three is never sent, because the code waits for call two. And curl ignores all of it. CORS is enforced by the browser, configured by the server, and keyed on the page's origin.

SHOW: The chat wireframe (`illustration`): an answer area and a "References" drawer of ten rows
labelled book · author · dist (README.md:217–222), all empty outlines, caption "what to look for".
Then the closing beat: the map's door 9000, neutral GREY, with a GOLD meter beside it; slide 13's
warning redrawn: "an unprotected AI endpoint". GREY tag `lecture_ref(10, "11, 13")` top right during
this block. Fade out.
SAY: On screen, look for an answer and a drawer of ten references, with book, author and distance. Last thought: CORS decides which page may see a reply, but nothing here decides who may call. An open AI endpoint, spending your key, is running on your laptop.

---

## S13 · The agent, and a model that isn't yours — `s13_agent.py` · `AgentAndTuned`

SHOW: TRACKER E4. The browser at `localhost:3200/agent` (`illustration`), the README's example
question as a quote (README.md · line 232). The flow as a three-step strip over code:
① browser → `GET :9000/rag/agent_call`, CODE(cheese-app-v0/api-service/api/routers/rag.py: 150–171),
lines 160–163 highlighted (the search text becomes an embedding); a choice chip
`get_book_by_author` / `get_book_by_search_content`; ② browser → Chroma `:8000`, CODE(cheese-app-v0/frontend-ai-chatbot/src/services/DataService.js:
45–47) small (`"where": { "author": author }`); ③ browser → `POST :9000/rag/llm-agent-response`,
CODE(cheese-app-v0/api-service/api/routers/rag.py: 190–203) with a chip `MAX_AGENT_STEPS = 5`
(rag.py:83), a loop arrow, and a server-side tool chip `pavlos_fun_fact_tool` (quoted name). GOLD
`cost_tag()` "1 embedding + 3 to 7 generation calls". `▶ your turn`.
SAY: Step 4 is the cheese expert agent. Pause and ask it something. Here Gemini must first pick a retrieval tool: search by author, or search by content. The API turns the search text into an embedding, and your browser queries the database, filtered by author when that tool won. Then the API loops up to five times, and Gemini may call a fun fact tool on the server. A gold tag: one agent question costs one embedding and three to seven generation calls.

SHOW: The answer frame (`illustration`), empty outlines, its last paragraph drawn as an amber box
labelled "Pavlos' fun fact" (README.md · line 239; CODE(cheese-app-v0/frontend-ai-chatbot/src/components/chat/ChatComponent.jsx:
22–28) small, line 24 highlighted). No answer text.
SAY: On your screen, look for an answer that ends with a highlighted fun fact paragraph.

SHOW: TRACKER E5. CODE(cheese-app-v0/api-service/api/routers/rag.py: 14–27), line 22
`FINE_TUNE_GENERATIVE_MODEL = "projects/129349313346/locations/us/endpoints/7652952773041848320"`
RED, a GREY label "the instructor's endpoint"; a README card (`README.md · line 247`). Beside it
CODE(llm-finetuning/gemini-finetuner/cli.py: 89–96), header
`llm-finetuning · gemini-finetuner/cli.py · lines 89–96`, line 92 `Tuned model endpoint:` GREEN. A
YELLOW edit arrow carries "your endpoint" into line 22. A small chip: "rag.py is under api/ →
reloads · agent_tools.py is not → control C, uvicorn_server again". `▶ your turn`.
SAY: Step 5 is the fine-tuned cheese model. The README says to update this endpoint to your own, the one your trainer printed in the fine-tuning lecture. Pause and paste yours. The server reloads by itself, because this file sits under the api folder. Its neighbour, the agent tools file, is not watched; for that one, press control C and start the server again.

SHOW: V2 reprise: the grid returns; S08's parked arrow re-fires from the browser at
`localhost:3200/finetunechat` (`illustration`): the endpoint path picks column `project
129349313346`, row `llm-service-account`, empty cell, RED 403; no error panel (caption "nothing
documents this error's exact text"). CODE(cheese-app-v0/api-service/api/routers/rag.py: 110–113)
small, line 111 `location="us"` highlighted. GOLD `cost_tag()` "tuned-model calls bill the
endpoint's project". Fade out.
SAY: Here the ponder from part 1 lands. Leave the default, and the endpoint path points into the instructor's project, where your account has no role: a 403. This call also uses a second client, in the U S location, as tuned models need. And a final gold tag: tuned model calls bill whichever project owns the endpoint.

---

## S14 · What survives: volumes now, buckets next — `s14_persist.py` · `WhatSurvives`

SHOW: TRACKER F1 (tracker F appears: "README › Shut down", 2 dots). GREY tag
`lecture_ref(10, "40–45")` top right, whole scene. The API terminal gets `^C` → TERM(laptop/33:
165–170), then `exit` → TERM(laptop/33: 173); the frontend terminal gets `^C` → TERM(laptop/51: 56),
then `exit` → TERM(laptop/51: 65) (the npm notice, lines 58–62, is not printed). The map's API and
frontend houses go dark; their doors brick up. Then `docker ps` (extra) → TERM(laptop/46: 2–3;
squeeze): only Chroma. `▶ your turn`.
SAY: Time to shut things down, and see what survives. In the API and frontend terminals, press control C, then type exit. Pause and do it. Both containers ran with dash dash rm, so an extra docker ps shows only the database left.

SHOW: TRACKER F2. Prompt `student@laptop:~/cheese-app-v0/llm-rag$`. It types `docker compose down`
(README.md line 106) → TERM(laptop/70: 2–9; wrap). Lines 4–9 (Chroma stopped and removed,
`llm-rag-network` removed) highlight; the Chroma house and its street vanish from the map. Lines
2–3, the two `variable is not set` warnings, YELLOW, with CODE(cheese-app-v0/llm-rag/docker-compose.yml:
13–15) beside them. `▶ your turn`. Then `docker ps` (extra) → TERM(laptop/71: 2): an empty table.
SAY: Now the README's stop command, docker compose down, inside llm-rag. Pause and run it. The database and its network are removed. Two warnings say variables are not set, because we ran this outside the shell script, and Compose fills those blanks from your shell. That is part 1's mechanism, caught in the wild.

SHOW: TRACKER F2 · extra. It types `ls -la docker-volumes/chromadb` (extra) → TERM(laptop/72: 2–5),
`chroma.sqlite3` highlighted GREEN; on the map the Chroma house is gone, but a GREEN folder stays lit
where it stood.
PONDER(6 s, "After docker compose down,\nare your embeddings gone?\nWhat would make them gone?")
SAY: An extra listing shows the database file still on disk. Something to ponder: after compose down, are your embeddings gone? And what would make them gone?

SHOW: CODE(cheese-app-v0/llm-rag/docker-compose.yml: 18–24), line 24
`- ./docker-volumes/chromadb:/data` YELLOW. Then `sh docker-shell.sh` (extra; the README's command
re-used) → TERM(laptop/73: 2–4, …, 12), `exit` → TERM(laptop/73: 14); then
`curl -s http://localhost:8000/api/v2/version` (extra) → TERM(laptop/74: 2), `"1.0.0"`, caption
"same folder, served again". A RED trash glyph hovers over `llm-rag/docker-volumes/`, caption "this
deletes them"; CODE(cheese-app-v0/llm-rag/cli.py: 280–288) small, caption "a reload deletes, then
creates".
SAY: No. The data sits in a folder on your laptop, mounted into the container at slash data. Containers come and go; mounted folders stay. An extra restart brings the database back over that same folder. Deleting the docker volumes folder is what loses your embeddings, and a fresh load rebuilds cleanly, because the loader deletes and then recreates each collection.

SHOW: Slides 40–45 redrawn: the bind-mounted folder ("a folder this laptop can see") morphs into a
GCS bucket ("a folder any authorized machine can see"); the folder tree melts into a flat list of
names with shared prefixes (slide 41). CODE(llm-finetuning/dataset-creator/cli.py: 276–294), header
`llm-finetuning · dataset-creator/cli.py · lines 276–294`, line 279
`storage_client = storage.Client()` YELLOW, chip "no key path: ADC again". One GREY line for the read
side: CODE(mega-pipeline/transcribe_audio/cli.py: 36–39), header
`mega-pipeline · transcribe_audio/cli.py · lines 36–39`.
SAY: The cloud version of a mounted folder is a storage bucket, a folder any authorized machine can see. Its folders are only name prefixes. The storage client takes no key path, so ADC finds the same key, and a storage role authorizes the writes.

SHOW: The IAM grid's GREY Storage Admin token pulses: "this is what it was for". Slide 45's four
rules as a card, GREY dashed "L11", the last rule GOLD: "Storage Object Admin over Storage Admin ·
keep buckets private · prefix the globally unique name · delete what you don't need: storage and
egress bill". Fade out.
SAY: This app never calls a bucket, which is why Storage Admin sat gray in the grid; next lecture uses one for real. The lecture's four rules: grant object admin, not full admin; keep buckets private; prefix their globally unique names; and delete what you no longer need, because storage and downloads cost money.

---

## S15 · Tear down, recap, and what's next — `s15_recap.py` · `Recap`

SHOW: TRACKER F2 · extra (the README's command again, after our extra restart). GREY tag
`lecture_ref(10, "26, 31, 53")` top right, whole scene. It types `docker compose down` →
TERM(laptop/75: 4–9) (lines 2–3, the same two warnings, print small and GREY). `▶ your turn`. Then
`docker network rm cheese-app-network` (extra) → TERM(laptop/76: 2). The map's streets vanish; the
laptop is empty except the GREEN secrets drawer.
SAY: If you tried the restart too, run docker compose down once more. An extra command then removes the shared network. Pause, and leave your machine clean.

SHOW: The BLUE building, GREY: "nothing idles in the cloud · no VM · no bucket · no deployed
endpoint". The GREEN key card turns over: a GREY `extra` card, small, "key hygiene":
`gcloud iam service-accounts keys list --iam-account=…` and
`gcloud iam service-accounts keys delete KEY_ID --iam-account=…`. A RED chip: "a key on GitHub →
delete it in IAM now · rewriting history is not enough". A turnstile arch labelled
`detect-private-key` (L09's gate).
SAY: Nothing idles in the cloud: no machine, no bucket, no deployed endpoint. What can keep costing you is the key. List your keys, and delete the ones you no longer use. If a key ever reaches GitHub, delete it in IAM at once; rewriting history is not enough. Last lecture's private key hook is the gate that catches it first.

SHOW: The debugging flowchart, each error pointing at its set piece's thumbnail:
`DefaultCredentialsError` → path and mount (V3) · `401` → no token (V1) · `403` → role, project,
API (V2) · `Failed to fetch` or a CORS line in the console → origin (V5) · `port is already
allocated` or a name conflict → doors and names (V4) · "the script dies on the network" → line 14.
Then V6 complete, every house and door lit; then everything unlit.
SAY: When something breaks, find its layer. A default credentials error: the path or the mount. A 401: no token. A 403: role, project, or API. Failed to fetch, or a CORS line in the console: the page's origin. Port already allocated: a door is taken. And a script that dies on the network: line 14.

SHOW: A card "Test yourself". One question at a time (≥ 24 pt, ≤ 3 lines), each with a thumbnail of
its picture; earlier ones collapse into a label list at left. Q1 "Name ADC's three places, and the
one this tutorial fills." (the magnifying glass) · Q2 "Why is GOOGLE_APPLICATION_CREDENTIALS set to
/secrets/… and not to a path on your Mac?" (the tube) · Q3 "The CLI dials llm-rag-chromadb:8000;
your browser rings localhost:8000. Why can't they swap?" (two arrows) · Q4 "You serve the frontend
at http://localhost:3300. Which component breaks first, and why does the API keep working?" (the
bouncer) · Q5 "You got a 403 on /rag/embedding. Three distinct causes: how do you tell them apart?"
(the grid). Labels: "ADC" · "the portal" · "two addresses" · "origins" · "403".
SAY: 5 questions to test yourself. One: name the three places ADC looks, and the one this tutorial fills. Two: why does the key variable point to slash secrets, not to a path on your Mac? Three: the loader dials the database by name, your browser by localhost; why can they not swap? Four: with the frontend on port 3300, which call breaks first, and why does the API keep working? Five: a 403 on the embedding route has three causes; how do you tell them apart?

SHOW: The label list stays at left. Footer cards: "Answers: exercises.md" and "Study guide + every
command: MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md". A "Next" card, GREY dashed:
"L11 · data-service-account, real buckets, a bucket's CORS list" · "L13–L15 · ADC's third place,
inside the cloud" · "L21+ · federation for CI". Everything fades to an empty frame (end of part 2).
SAY: Answers are in the exercises; every command is in the study guide. Next lecture brings a new service account, and real buckets with a CORS list of their own. Later, code inside Google's cloud fills the third place ADC looks, and federation returns for CI.
