# Brief · AC215 L14 — Serverless Deployment (exam edition)

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md` (colours,
`lecture_ref` tags, never-do list) and `docs/STYLE_GUIDE.md`. This is **not** a follow-along: no
README tracker, no "your turn" tags, no terminal captures, no command-by-command walk. It is a
concept-first explainer for the night before Quiz 4. The full follow-along episode is the separate,
future `videos/ac215-l14-serverless-deployment/`; this folder only reads its `SLIDES.md` and `digest.md`.

**Sources, and which one wins.**
- Lecture 14 slides (17 pages; `../ac215-l14-serverless-deployment/SLIDES.md`, cite PDF page numbers).
- Lecture 15 slides 11–17 for the serving-signature half of the quiz (`../ac215-l15-vertex-ml-workflows/SLIDES.md`):
  Quiz 4 tests preprocessing placement and the serving signature, which the lecture series teaches
  with the `model-deployment` tutorial. The GREY tag then reads "Lecture 15 · slide n".
- The demo repos as they are **today** (copied unchanged into `assets/source/<repo>/<path>`):
  `dlops-io/serverless-deployment` `main` @ `46cc62f` (2026-10-22) and `dlops-io/model-deployment`
  `main` @ `cf0b7c7` (2026-10-27).
- `../ac215-l14-serverless-deployment/digest.md` was verified at the older `4eaf343` (README of ~150
  lines, Docker Hub `dlops/simple-translate-http`). Since then the README was rewritten into four parts
  (function, web-app service, runtime identity, job) with the image
  `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`. **Code panels quote the current
  clone**; the digest is used only for mechanisms that did not change (functions-framework looks up
  the entry point by name, Cloud Build turns source into an image, request-based billing, cold starts).

## Audience and goal

An AC215 student the day before Quiz 4. Has done L1–L13 (VMs, containers, `docker run -p`, a
service-account key in `secrets/`, a Vertex AI training job), has seen Lecture 14 and probably skimmed
the README, but has not internalised *why* each answer is right. Watching on a laptop, no clone open.

After the video they can answer conceptual multiple-choice questions on this lecture **and say why
each wrong option is wrong**:
1. pick Cloud Run **service** or **job** from a container's lifecycle (listens and answers vs runs to
   completion and exits; on demand or by Cloud Scheduler), and recognise a job that "never finishes"
   because it started the web server;
2. predict which bill moves when idle time, request count or minimum instances change (functions and
   Cloud Run with min instances 0 bill invocations and execution time; a VM, or anything with an
   always-on instance, bills provisioned time including idle);
3. say what you hand over for a Cloud Run function (source + `requirements.txt` + an **entry point**
   name; Google builds the image) vs a Cloud Run service (an image), and what invocation, identity
   and logs look like for each;
4. separate the two permission questions (who may **call** it vs who it **runs as**), know the runtime
   service account needs no key, and that you need Service Account User to attach it;
5. argue for preprocessing **at the endpoint** (thin clients; one deployment updates or rolls back
   every client; client-side preprocessing needs coordinated client releases);
6. say which function the exported model must register as its serving signature — the one that
   preprocesses **and** calls the model — and what goes wrong with preprocessing alone or the raw model.

## Length and parts

12–15 minutes. Narration **~1,990 words** (1,800–2,300; Kokoro `af_heart`, speed 0.9, budgeted at
~150 wpm for this series' pacing ≈ 13.3 min), plus three ponder timers and answer reveals (~1 min).
**One part** (no `parts:` key in `video.yaml`).

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 190 | S05 TwoQuestions | 250 |
| S02 ServiceOrJob | 290 | S06 ThinClients | 240 |
| S03 IdleMeter | 290 | S07 ServeSignature | 290 |
| S04 WhatYouHandOver | 260 | S08 Recap | 180 |
| | | **total** | **1,990** |

Budgets are targets (±15 %); the total must stay inside 1,800–2,300.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop and the **clients**: the browser, the phone app, the web page, "you" the deployer | GREY |
| the cloud: Cloud Run (services, jobs, functions), the Vertex AI endpoint, the VM, Cloud Storage buckets, Cloud Scheduler; **runtime identities** (the service-account badge is a cloud principal). VMs are a solid rack; serverless instances are a **dashed** outline that appears only while called | BLUE |
| the image and its containers: `cgumb/ac215-translation-demo:…`, the image Cloud Build makes for a function, a running instance's inner box | TEAL |
| the base image's own Python (`python:3.12-slim-bookworm`, `Dockerfile:1`; S04 only) | ORANGE |
| what you own and ship: `main.py`, `requirements.txt`, the `hello_http` handler, the app's `serve`/`batch` code, the exported SavedModel and its `serving_function`, the preprocessing logic | GREEN |
| tools and frameworks: functions-framework, gunicorn, Cloud Build, the TensorFlow model server | PURPLE |
| errors and wrong answers: the job that never finishes, an entry-point mismatch, a 403, a client on the old preprocessing, a wrong plug; the ✗ on a wrong option | RED |
| "look here now": the current request pulse, the ponder timer, the right option's highlight | YELLOW |
| money: both meters, idle-time shading, the minimum-instances drip, the endpoint's always-on machine; the (absent) key glyph, dashed and crossed | GOLD |
| routes and triggers: HTTP requests and URLs, query strings, the Scheduler trigger, `gs://` paths, the base64 request body | PINK |

The lecture's own colour code (slide 10: blue = dedicated hardware, green = serverless) is **not**
copied: both rows are BLUE (cloud); the difference is shape (solid rack vs dashed instance).

## Visual set pieces (the 3Blue1Brown part)

- **V1 · Lifecycle strips (S01, S02, S08).** One TEAL image block with two startup commands hanging
  under it: `serve` and `batch` (`__main__.py:1,12-13`). Each command draws a horizontal time strip.
  *Service strip*: a dashed BLUE instance appears when the first PINK request pulse arrives, stays
  open with a "listening on :8080" ear, answers each pulse with a return arrow, and dissolves after
  the traffic stops (scale to zero); a second instance splits off during a burst (max 2). *Job strip*:
  a block that runs through four labelled segments (read → translate → speak → save,
  `__main__.py:52-57`), then a hard right edge "exit 0" (or "exit 1", `:58-61`); no ear, no URL.
  A BLUE Cloud Scheduler clock drops a PINK trigger onto the job strip "every night"; a GREY
  "Execute" button does the same on demand. In S01 the job strip is drawn with the image's default
  `CMD … serve` (`Dockerfile:12`): it never reaches an edge, runs into the RED "task timeout 5 min"
  wall (`README.md:778-779`). Transformation: the hook's endless strip is cut into the job shape
  when the command becomes `python -m translation_demo batch …` (`README.md:747-766`).
- **V2 · Two meters on one day (S03).** A 24-hour axis with YELLOW request ticks. Top row: a solid
  BLUE VM rack; a GOLD meter fills at a constant rate from boot to shutdown, idle stretches shaded
  GOLD. Bottom row: a dashed function instance blinks into existence at each tick; its GOLD meter
  advances only by (invocations, milliseconds). Transform 1: the idle gaps stretch (the axis grows,
  ticks unchanged) → VM meter grows, function meter frozen. Transform 2: the ticks double on a fixed
  day → function meter doubles, VM flat. Transform 3: a "minimum instances" slider 0 → 1 lights a
  faint always-on instance with its own GOLD drip — it has joined the VM row; at 0, a small grey puff
  marks a cold start on the first tick after idle. A Vertex AI endpoint card (`min_replica_count=1`,
  `cli.py:210-218`) slides into the always-on row.
- **V3 · What you hand over (S04).** Slide 10's four deployment options redrawn as a 2×2: rows VM /
  serverless, columns *a file* / *a container*; L1–L2's VM cells ticked, today's two cells YELLOW.
  The file cell opens: GREEN `main.py` + `requirements.txt` + a name tag "entry point:
  `hello_http`" → PURPLE Cloud Build → a TEAL image dropped into Artifact Registry → runs as a
  Cloud Run instance whose PURPLE functions-framework calls `hello_http` by name. A mismatched name
  tag ("main") makes the arrow from framework to code snap RED. The container cell: an image URL goes
  straight to a revision, no build step; the instance's ear on port 8080. Both end in the same
  dashed BLUE instance: "a function is a container you did not write."
- **V4 · Two doors and a badge (S05).** A BLUE service box with a door on each side. Left door, "who
  may call it": a GREY browser's PINK request passes when *Allow public access* is set, bounces RED
  (403) when it is not. Right door, "who it is when it calls out": a BLUE service-account badge
  pinned on the instance (`translation-demo-runtime`), a token flowing from the platform to the
  badge, the request going on to Agent Platform with two role chips (Agent Platform User, Service
  Usage Consumer, `README.md:374-376`); a dashed GOLD key glyph crossed out ("no key file",
  `README.md:380`). A third, smaller arrow from GREY "you" to the badge: attaching it needs Service
  Account User (`README.md:432-434`). For the job: a second badge with bucket chips (Viewer on input,
  Creator on output, `README.md:683-688`). Then three log windows (build, service, job execution) light
  up in turn as the README's troubleshooting rows name them (`README.md:1035-1046`).
- **V5 · Thin clients, one door (S06).** Two GREY clients (a phone app, a web page), each carrying a
  GREEN preprocessing gear (decode, scale to 0–1, resize 224×224) before a PINK arrow to a BLUE
  endpoint. The gears lift off both clients and merge into one gear inside the endpoint; the arrows
  now carry raw JPEG bytes wrapped as `{"b64": …}` (`model-deployment/README.md:189-194`). Then a
  version dial on the endpoint: v1 → v2 (a bad resize, RED) → back to v1: both clients turn healthy at
  the same instant. Replay with client-side gears: rollback becomes two release trains (an app-store
  review queue, a web deploy) leaving at different times, and a RED mismatch window between them.
- **V6 · The serving plug (S07).** A pipeline of blocks: JPEG bytes → decode → float → resize →
  model → four probabilities (parmigiano, gruyere, brie, gouda). An export socket labelled
  `serving_default` on the SavedModel. Three plugs are tried in turn: `preprocess_image` alone — out
  comes a 224×224×3 image, not probabilities (RED); the raw model — the socket now demands float
  tensors, and the gears jump back onto the clients (RED, V5 rewound); `serving_function` (map the
  preprocessing over the batch, then call the model, `cli.py:109-114`) — probabilities come out
  (YELLOW). Echo of V3's name tag: "the platform calls the name you register".

## The lecture behind it

| scene | lecture_ref | used for |
| --- | --- | --- |
| S01 | 14 · 14 | "a container runs as a service or as a job" |
| S02 | 14 · 14 | service vs job |
| S03 | 14 · 8, 11, 14, 16; then 15 · 11 | pay only while code runs; cold starts; the endpoint cost alert |
| S04 | 14 · 10–12, 15 | the four deployment options; deploying a function; deploying an image |
| S05 | 14 · 16 | limited control and debugging → where to look |
| S06 | 15 · 13 | move preprocessing into the serving function; client-side brittleness; easier rollback |
| S07 | 15 · 14 | the annotated serving-signature code |
| S08 | 14 · 16; 15 · 16–17 | the cons; Vertex AI Online Prediction vs Cloud Run (one rule) |

Kindly-stated differences (one sentence each, where the scene touches them): the slides say "Cloud
Functions"; the README creates it under **Cloud Run → Services → Write a function** (Cloud Run
functions). Slide 15 of L15 saves with `tf.saved_model.save(..., signatures=...)`; the current repo uses
Keras' `ExportArchive.add_endpoint("serving_default", ...)` (`cli.py:116-123`) — same idea, the comment
says why. Slide 11 of L14 says a function is "without managing … containers": you don't manage one,
but Google still builds one (`README.md:212-216`).

## Scene plan

The scene list is final (`video.yaml`):

| # | file | class | title |
| --- | --- | --- | --- |
| S01 | `scenes/s01_hook.py` | `Hook` | A job that never finishes |
| S02 | `scenes/s02_lifecycle.py` | `ServiceOrJob` | Service or job: read the lifecycle |
| S03 | `scenes/s03_meter.py` | `IdleMeter` | Who pays for the idle hours? |
| S04 | `scenes/s04_handover.py` | `WhatYouHandOver` | Function or container: what you hand over |
| S05 | `scenes/s05_identity.py` | `TwoQuestions` | Who may call it, who it runs as, where to look |
| S06 | `scenes/s06_preprocess.py` | `ThinClients` | Where preprocessing lives |
| S07 | `scenes/s07_signature.py` | `ServeSignature` | Register serve: preprocess, then model |
| S08 | `scenes/s08_recap.py` | `Recap` | Seven rules for Tuesday |

Code panels use `code_panel(source, path, first_line, …)` from `assets/source/<repo>/<path>` with the
real line numbers, ≤ 12 lines on screen. README excerpts are code panels of `README.md` lines.

**S01 · A job that never finishes (~190).** Lecture 14 · 14. Cold open on a broken thing. A job
`translation-audio` is created from the web app's image; Execute; the V1 strip runs… and runs… into
the RED timeout wall. Panel: `serverless-deployment/tutorial/app/Dockerfile:12` (`CMD … "serve"`),
then the README's own troubleshooting row "Job starts a server instead of finishing → Command
`python` and separate batch arguments" (`README.md:1044`). The question on screen (no timer): "Same
image, same code. Why does the web app work and the job never end?" Then a 15-second exam map: the
five things Quiz 4 asks about this lecture as five empty slots (lifecycle, billing, what you hand over,
identity, the model endpoint) that S02–S07 fill.

**S02 · Service or job: read the lifecycle (~290).** Lecture 14 · 14. V1 in full. Panels:
`tutorial/app/translation_demo/__main__.py:1` (docstring "One image, different startup commands"),
`:12-13` (two subcommands), `:22-26` (serve → gunicorn on `0.0.0.0:$PORT`), `:52-62` (batch: read,
translate, speak, save, print, exit; `:58-61` a failure exits 1 "so execution status is truthful"),
`README.md:582-585` ("That is a **job**, rather than an HTTP service waiting for requests"),
`README.md:747-748` (Container command `python` "replaces the image's web-server command"), and
`README.md:833` ("The job exits; it does not provide a web URL"). Answer the hook. Cloud Scheduler
appears as the trigger for "every night" (not in this README; said so). **PONDER 1** (below).
Takeaway card: *If the question says "runs, writes its output, exits" or "every night" → job (+
Scheduler). If it says "answers requests", "URL", "port" → service.*

**S03 · Who pays for the idle hours? (~290).** Lecture 14 · 8, 11, 14, 16, then 15 · 11. V2. Panels:
`README.md:281-283` (Request-based billing, minimum instances 0, maximum 2), `README.md:218-224`
(cold start; scale to zero applies to instances; minimum instances keep capacity warm),
`model-deployment/cli.py:210-218` (`min_replica_count=1`: an always-on machine, "the part that costs
money", `model-deployment/README.md:66`). "Serverless" is not the rule; *is anything always on?* is.
Cold start as the price of zero idle cost (slide 16). **PONDER 2** (below). Takeaway: *If the question
changes idle time → only always-on things' bills change (VM, min instances ≥ 1, an endpoint with a
minimum replica). If it changes request count or duration → only the pay-per-use bill changes.*

**S04 · Function or container: what you hand over (~260).** Lecture 14 · 10–12, 15. V3. Panels:
`tutorial/function/main.py:3-12` (`@functions_framework.http`, `def hello_http(request)`,
`request.args.get` with defaults), `tutorial/function/requirements.txt:1-2`, `README.md:150-151`
("Set the **Function entry point** to `hello_http`. This is the Python function the serving framework
should call, not the filename or service name."), `README.md:212-216` (Cloud Build installs the
requirements, configures the Functions Framework, publishes an image in Artifact Registry — at build
time, not per request), `README.md:272-274` (Deploy container → an existing image URL), and
`tutorial/app/Dockerfile:1,11-12` (ORANGE base, port 8080, CMD). Invocation: the same URL with a
query string (`README.md:162-163`, `?text=…&src=en&dest=fr`; "no redeploy for new inputs",
`:171`). Takeaway: *If the question says "you supply source and an entry point" → function (Google
builds the image; the entry point must name the def). If it says "you supply an image / control the
OS libraries or startup command" → Cloud Run service. Either way it ends up as a container on Cloud Run.*

**S05 · Who may call it, who it runs as, where to look (~250).** Lecture 14 · 16. V4. Panels:
`README.md:361-362` ("Two permissions questions are separate: who may call our public app, and what
the running app may access"), `README.md:374-380` (two roles; "You do not need to create or download a
key"), `README.md:432-434` (Service Account User on the runtime account to attach it),
`README.md:683-690` (job account: Object Viewer on input, Object Creator on output; the web account
does not need them), `tutorial/app/translation_demo/speech.py:101-109` (`google.auth.default` — the
credentials come from the attached account, or local ADC), `README.md:1038-1046` (where to look: build
logs for a function build, service logs, job execution logs; "a completed build is not proof",
`:228-229`). Takeaway: *Public access answers "who may call"; the service account answers "what the
code may touch". A 403 from inside the app is the badge's roles, not the caller's.*

**S06 · Where preprocessing lives (~240).** Lecture 15 · 13. V5. Bridge sentence: Cloud Run hosts
any container; for a trained model, next lecture's Vertex AI endpoint plays the same role, and the
quiz asks where the preprocessing goes. Panels: `model-deployment/README.md:59-60` ("The
preprocessing travels with the model, so every client gets exactly the same preprocessing that was
used in training"), `model-deployment/cli.py:245-255` (the client only base64-encodes bytes and calls
`predict`). Rollback replay (V5). Takeaway: *If the question says "several clients", "update or roll
back once", "no client release" → preprocessing at the endpoint. Client-side preprocessing = every
client re-released in lockstep.*

**S07 · Register serve: preprocess, then model (~290).** Lecture 15 · 14. V6. Panels:
`model-deployment/cli.py:100-105` (`preprocess_image`: decode, convert to float, resize 224×224),
`:107-114` (`serving_function` with `input_signature=[tf.TensorSpec([None], tf.string)]`, `map_fn`,
then `prediction_model(images, training=False)`), `:120-123` (`add_endpoint(name="serving_default",
fn=serving_function)`), `:157-163` (`--test` loads `serving_default` and feeds `bytes_inputs`, as the
server will), `model-deployment/README.md:193` (`bytes_inputs` is the argument's name). Link back to
S04: the function's entry point and the model's serving signature are the same idea — the platform
calls exactly the name you registered. **PONDER 3** (below). Takeaway: *If the question asks what to
register → the function that does preprocessing **and** inference. Preprocess alone returns images;
the raw model makes every client preprocess.*

**S08 · Seven rules for Tuesday (~180).** Lecture 14 · 16; 15 · 16–17. V1's two strips, V2's two
meters, V3's grid, V4's two doors, V5's single gear, V6's plug return as small icons beside each rule:
1. Read the lifecycle: listens → service; runs and exits → job (on demand or Cloud Scheduler).
2. Idle time costs only what is always on: VMs, minimum instances, endpoint replicas.
3. Pay-per-use bills invocations × execution time; zero idle cost buys cold starts.
4. Function = source + requirements + entry point (Google builds the image); service = your image.
5. "Who may call" (public access / invoker) is not "who it runs as" (the service account; no key).
6. Preprocess at the endpoint: one deployment updates or rolls back every client.
7. Register `serve` = preprocess then model; the platform calls the name you register.
One closing line on L15 slides 16–17 (Vertex AI to serve a trained model; Cloud Run when ML is part of
a broader app) and the cons (slide 16: lock-in, cold starts, debugging). Ends on an empty frame.

## Ponder questions (new; never the practice questions)

Each: question card + four options A–D, an 8-second YELLOW timer, then the right option highlighted
and a RED one-line reason under each wrong option. Wording below is the design; the script may
tighten it.

**P1 (end of S02).** "A container reads all new documents in a bucket, writes their embeddings to
another bucket, and exits. It should run once an hour. Which deployment fits best?"
- A. A Cloud Run service with minimum instances 1 that runs the indexing loop — ✗ pays for an
  always-on instance between runs, and a service is meant to listen for requests, not loop.
- **B. A Cloud Run job, executed every hour by Cloud Scheduler** — ✓ finite work, runs to completion,
  billed only while it runs.
- C. A Cloud Run service whose container does the indexing at startup and then exits — ✗ a service
  must keep listening on `$PORT`; a container that exits is a failed instance, not a finished one.
- D. A Compute Engine VM with a cron entry — ✗ works, but you pay for the 55 idle minutes of every
  hour, and you manage the server.

**P2 (end of S03).** "Ignore free tiers. Your translation endpoint runs as a Cloud Run function
(minimum instances 0) and, for comparison, on an always-on VM. Next month you get twice as many
requests, each just as long, in the same 24-hour days. Which bill changes?"
- A. Only the VM's — ✗ the VM bills provisioned hours, and they did not change.
- **B. Only the function's** — ✓ invocations and execution time doubled; the VM was paid for anyway.
- C. Both double — ✗ the VM's bill is flat with traffic until you add machines.
- D. Neither, because serverless has no minimum charge — ✗ "no minimum" means idle is free, not that
  work is free.

**P3 (in S07, before the takeaway).** "A team exports a cheese classifier whose `serving_default`
is the raw Keras model. Their phone app resizes and normalises before sending float arrays. They add a
web client that sends JPEG bytes, and want one place to fix or roll back preprocessing. What should
they register?"
- A. Keep the raw model; the model server decodes JPEGs for you — ✗ the server only base64-decodes
  to bytes; the signature decides what those bytes become.
- B. `preprocess_image` as `serving_default` — ✗ it returns 224×224 images, not predictions.
- **C. A serving function that maps the preprocessing over the batch, then calls the model** — ✓
  both clients send bytes; preprocessing lives in one exported version.
- D. Keep the raw model and copy the resize code into the web client — ✗ two copies to keep in sync;
  every change or rollback needs coordinated releases of both clients.

## Things never to do on screen

- Never quote, paraphrase closely or answer the course's practice questions (Q6, Q7, Q9, Q10); the
  ponders above are new scenarios.
- No README walk-through: no console click sequences, no `gcloud` commands typed in a terminal, no
  captures, no "your turn" tags, no README tracker. Short README excerpts appear only as evidence.
- No slide images, QR codes or console screenshots; no Google/GCP logos (schematic shapes only, tagged
  `illustration` where a console form is suggested).
- No project ids, emails or keys that look real: the account email is shown as
  `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com` exactly as the README writes it;
  bucket paths as `gs://YOUR_INPUT_BUCKET/…`.
- No prices or free-tier numbers stated as current fact (the quiz is about *which* bill moves, not
  how much).
- Don't say "serverless means no servers" or "a function has no container": say *you don't manage*
  them.
- No real person's name on screen.
