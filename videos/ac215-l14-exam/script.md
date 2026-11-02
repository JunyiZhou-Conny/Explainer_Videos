# AC215 · Lecture 14 — Serverless Deployment (exam edition) — narration script & visual plan (v1)

Audience: an AC215 student the day before Quiz 4. They have done L1–L13 (a VM, containers, `docker run -p`, a
service-account key in `secrets/`, a Vertex AI training job), have seen Lecture 14 and probably skimmed the
`serverless-deployment` README, but have not internalised *why* each answer is right. They watch on a laptop with no
clone open. This is an **exam edition**, not a follow-along: no README tracker, no `your turn` tags, no terminal
captures, no command-by-command walk, and **no live runs** — every panel is source text from the repos or our own
drawing.

Goal (BRIEF.md "Audience and goal"): after the video they can answer conceptual multiple-choice questions on this
lecture and say why each wrong option is wrong: (1) pick a Cloud Run service or job from the container's lifecycle
(listens and answers vs runs to completion and exits; on demand or by Cloud Scheduler) and recognise a job that never
finishes because it started the web server; (2) predict which bill moves when idle time, request count or minimum
instances change; (3) say what you hand over for a Cloud Run function (source + `requirements.txt` + an entry-point
name; Google builds the image) vs a Cloud Run service (an image), and how each is invoked; (4) separate "who may call
it" from "who it runs as", know the runtime service account needs no key and that attaching it needs Service Account
User; (5) argue for preprocessing at the endpoint (thin clients, one deployment updates or rolls back every client);
(6) say which function the exported model must register as `serving_default` — the one that preprocesses **and** calls
the model — and what goes wrong with preprocessing alone or the raw model.

Sources of truth: `BRIEF.md` (design, binding); the Lecture 14 slides (`../ac215-l14-serverless-deployment/SLIDES.md`,
17 pages) and Lecture 15 slides 11–17 (`../ac215-l15-vertex-ml-workflows/SLIDES.md`), cited by PDF page; the demo repos
as they are today, copied unchanged into `assets/source/serverless-deployment/` (`main` @ `46cc62f`) and
`assets/source/model-deployment/` (`main` @ `cf0b7c7`); `../ac215-l14-serverless-deployment/digest.md` only for
mechanisms that did not change since its older commit (functions-framework calls the entry point by name, Cloud Build
turns source into an image, request-based billing, cold starts). Where the slides and the repo differ, the panel shows
the repo and the SAY says in one sentence what each shows (S04: "Cloud Functions" vs Cloud Run functions, and "without
managing containers"; S07: `tf.saved_model.save` vs `ExportArchive`). Cloud Scheduler is not in this README; S02 says so.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most about 55
  words; the recap may run a little longer) and become the subtitles. Plain spoken English: no backticks, no symbols,
  no markdown. Identifiers are on screen and said in words: `hello_http` → "hello underscore HTTP",
  `preprocess_image` → "preprocess image", `serving_function` → "serving function", `serving_default` → "serving
  default", `bytes_inputs` → "bytes inputs", `min_replica_count` → "minimum replica count", `google.auth.default` →
  "google auth default", `tf.saved_model.save` → "the saved model save call", `__main__.py` → "the package's main
  module", `main.py` and `requirements.txt` as "main.py" and "the requirements file". Numbers as digits ("224 by 224",
  "8080", "403", "5 minutes"); a number that matters gets its own short sentence. Never a "!" after a digit. No prices
  or free-tier numbers.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences` splits only there;
  the split drives TTS gaps, subtitle cues and the one-to-one Chinese alignment). No sentence opens with a lower-case
  identifier or file name. No `'s` after a digit or on a word with a lexicon entry. No abbreviations with inner dots
  ("e.g.", "vs.") in SAY. American spelling on screen and in SAY ("gray"; the colour constants stay GREY).
- Names. The instructor's full name never appears, spoken or on screen (the slide decks' title pages are never
  redrawn). The SAY says "the lecture" or "the slides". No real person's name anywhere. The service-account email is
  shown only as `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com` exactly as the README writes it;
  buckets only as `gs://YOUR_INPUT_BUCKET/…` and `gs://YOUR_OUTPUT_BUCKET/…`. A key is a dashed GOLD key glyph,
  crossed out, never a value. No project ids, no real-looking keys.
- No live runs. This lecture's video has no captures: there is no terminal panel, no typed command, no `recorded` or
  `expected` output box. The console is never drawn as a screenshot; where a console form is suggested (S01's job, S02's
  Execute button, S05's toggles), it is a schematic chip with the README's field names, tag `illustration`.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves.
- `CODE(repo/path: a–b)`: `code_panel(...)` quoting `assets/source/repo/path` from line a to b with the real line
  numbers, header `path · lines a–b` (repo prefix dropped in the header for `serverless-deployment`; `model-deployment/`
  kept, since both repos have a `README.md`). At most 12 rows on screen; lines longer than 65 characters wrap
  (continuation rows indented, a GRAY ↪). `(folded)`: only the listed lines, a GRAY `…` row between gaps. README
  excerpts are code panels of `README.md` lines (markdown shown as plain text, `**` stripped, line numbers kept). An
  *excerpt chip* quotes an exact sub-string of one line, headed `path · line N (excerpt)`. Lit lines: a YELLOW bar
  behind the named line(s) unless the SHOW names another colour.
- `PONDER(10 s, Pn)`: the multiple-choice ponder. The SAY before it speaks a short stem. After that SAY block, the
  question card (YELLOW outline, lower two-thirds of the frame) shows the shortened question and four options A–D,
  each a row with its letter in a circle; a YELLOW timer bar drains under it (P1 10 s, P2 10 s, P3 12 s: BRIEF's 8 s
  lengthened so the card can be read). While a card is up, everything else in the frame fades to ≤ 20 % opacity.
  Nothing during the timer shows the answer. The next SAY block(s) reveal: the right option's row fills YELLOW with a
  ✓; under each wrong option a one-line RED reason writes in (the text given in the SHOW) as the SAY reaches it; then
  the card fades. Three in the video: P1 (end of S02), P2 (end of S03), P3 (S07, a prediction before the plugs). They
  are new scenarios (BRIEF.md "Ponder questions"); the course's practice questions are never quoted, paraphrased or
  answered. `PONDER(6 s, "…")` with a quoted line (S06) is L08's one-line `pause_and_ponder`, no options.
- `RULE: "…"`: the scene's exam-rule card: a GREEN-outlined card at the bottom third titled "exam rule", the rule in
  two lines, written in as the SAY says it; it shrinks into the S01 exam map slot it fills (top strip, see S01), so the
  map fills scene by scene. S08 reuses the six cards, splitting S03's into rules 2 and 3.
- `Lecture: 14 · 14.` under a scene header lists the slides the scene stands on. `LECTURE 14 · 14` in a SHOW line: from
  that SAY block on, the GRAY `lecture_ref(14, "14")` tag sits top right ("Lecture 14 · slide 14"; "slides" for a
  range), until a SHOW changes it. `LECTURE 15 · 13` → `lecture_ref(15, "13")`. The slides are never shown: every
  lecture picture is our own redrawing in the series colours with the slide's structure and terms; no slide image, QR
  code, meme, logo or screenshot. The lecture's own colours (slide 10: blue = dedicated hardware, green = serverless)
  are not copied: both rows are BLUE, the difference is shape (solid rack vs dashed instance).

Colours (BRIEF.md table): GREY clients and "you"; BLUE cloud (Cloud Run, the VM as a solid rack, serverless instances
as a dashed outline that exists only while called, the Vertex AI endpoint, buckets, Cloud Scheduler, service-account
badges); TEAL the image and its containers; ORANGE the base image's Python (S04 only); GREEN what you own and ship
(`main.py`, `requirements.txt`, `hello_http`, `serve`/`batch` code, the SavedModel, `serving_function`, the
preprocessing gear); PURPLE tools and frameworks (functions-framework, gunicorn, Cloud Build, the TensorFlow model
server); RED errors and wrong answers; YELLOW "look here now" (request pulses, timers, the right option); GOLD money
(meters, idle shading, the min-instances drip, the absent key); PINK routes and triggers (HTTP requests, URLs, query
strings, the Scheduler trigger, `gs://` paths, base64 bodies).

Notes for scene authors
- Every scene ends on an empty frame; ≤ 3 visual groups at once; something moves every ~4 s except ponder timers.
- Set pieces V1–V6 (BRIEF.md) are shared objects in `scenes/common.py`: `LifecycleStrip` (V1), `TwoMeters` (V2),
  `HandoverGrid` (V3), `TwoDoors` (V4), `ThinClients` (V5), `ServingPlug` (V6), plus `mcq_ponder(...)` for the
  PONDER cards and `exam_map()` / `rule_card()` for the RULE cards.
- Exam map and lecture tag share the top: the map occupies x ∈ [−6.6, 3.2], y ≈ 3.3; `lecture_ref` stays right of
  x = 3.4. The map is dimmed to 35 % except the active slot; slots show icon + number only (the label appears only on
  the active slot).
- Toolkit pieces: from `explainer/devops.py` `box`, `chip`, `tag`, `lecture_ref`, `check_mark`, `cross_mark`,
  `code_panel`, `server` (VM rack), `cloud`, `laptop`, `browser_window`, `file_glyph`, `step_badge` (option letters);
  from `explainer/components.py` `person_icon`, `timeline` (24-hour axis, S06 release bars), `connect`,
  `highlight_box`, `pause_and_ponder` (S06). New small shapes in `scenes/common.py`: ear glyph, gear, version dial,
  slider, clock, token, doors, plug and socket, and `mcq_ponder` (reusing `ponder_card`'s timer bar, the `card[3]`
  pattern).
- Lexicon entries added for this script (`# AC215 L14-exam`): gunicorn, main.py, 403, "a 403", "A 403". Checked and
  fine without one: JPEG, base64, HTTPS, HTTP, Vertex, JSON, cron, Scheduler, 224, lockstep, invocations; 8080 and
  README's have entries. The cheese names are on screen only, never spoken.
- Word budget (BRIEF.md): S01 190 · S02 290 · S03 290 · S04 260 · S05 250 · S06 240 · S07 290 · S08 180 = 1,990
  (allowed 1,800–2,300).

---

## S01 · A job that never finishes — `s01_hook.py` · `Hook`

Lecture: 14 · 14.

SHOW: Cold open, no tag. A schematic job chip (BLUE, tag `illustration`) writes in top left: "Cloud Run job ·
translation-audio", under it a TEAL image block `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` and
a small GRAY chip "the same image as the working web app". A GREY "Execute" button presses; a YELLOW pulse runs into
the V1 job strip, which starts drawing left to right across the middle (TEAL block, a running clock above it).
SAY: Here is a Cloud Run job called translation audio. It uses the same image as a translation web app that works perfectly. We press Execute, and the job starts.

SHOW: The strip keeps growing; the clock spins past 1, 2, 3, 4 minutes; the output bucket icon at the right edge
(BLUE, `gs://YOUR_OUTPUT_BUCKET/run-001/`) stays empty. At "5 minutes" a RED wall slams down in front of the strip,
labelled "task timeout · 5 min" (excerpt chip `README.md · line 778 (excerpt)`: "set **Task timeout** to `5`"); the
strip end turns RED, a RED "execution failed" chip.
SAY: Minutes pass. Nothing lands in the output bucket, and the job never says it is done. It runs straight into the task timeout we gave it. 5 minutes, and the platform stops it.

SHOW: The strip shrinks to the top. CODE(serverless-deployment/tutorial/app/Dockerfile: 11–12), line 12 `CMD ["python",
"-m", "translation_demo", "serve"]` lit RED on "serve". Then, under it, CODE(serverless-deployment/README.md: 1035–1036,
1044) (folded): the table header and the row "Job starts a server instead of finishing | Command `python` and separate
batch arguments", the row lit YELLOW.
SAY: The clue is the last line of the Dockerfile: its default command starts the web server. The README's troubleshooting table even lists the symptom: a job that starts a server instead of finishing.

SHOW: The panels fade. A YELLOW question writes across the middle (no timer): "Same image, same code. Why does the web
app work — and the job never end?" Under it, a beat later, two tiny strips grow from one TEAL image block: a web-app
strip answering YELLOW pulses, and a job strip that runs on and on.
SAY: Same image, same code. So why does the web app work, while the job never ends? Hold that question.

SHOW: The question moves up and shrinks. The exam map builds along the top strip: five empty GRAY-outlined slots
writing in left to right as the SAY names them, each with a small icon: "1 · service or job" (two tiny strips), "2 ·
who pays for idle" (a GOLD meter), "3 · what you hand over" (a 2×2 grid), "4 · who calls, who it runs as" (two doors),
"5 · the model endpoint" (a gear + plug). A GRAY caption under them: "Quiz 4 · Lecture 14 (+ Lecture 15 · slides
11–17)".
SAY: For the quiz, this lecture comes down to five ideas. Service or job. Who pays for idle time. What you hand over to deploy. Who may call your code, and who it runs as. And the model endpoint: where preprocessing lives, and which function it calls.

SHOW: A GRAY specimen tag "Lecture 14 · slide 14" pulses once top right; a GRAY code-panel header specimen
`__main__.py · lines 1–1` pulses once; a GRAY chip "no live runs · concepts, not clicks". The map stays (dimmed) at
the top for S02; everything else fades.
SAY: The gray tag, top right, names the lecture slide behind each idea.

---

## S02 · Service or job: read the lifecycle — `s02_lifecycle.py` · `ServiceOrJob`

Lecture: 14 · 14.

SHOW: LECTURE 14 · 14. The map's slot 1 pulses YELLOW. A redrawn slide-14 line writes in GRAY: "Run containers as
service or job." Below it the V1 TEAL image block, with two GREEN command tags hanging under it, `serve` and `batch`.
CODE(serverless-deployment/tutorial/app/translation_demo/__main__.py: 1–1) above the block, line 1 lit; then the
panel grows to lines 12–13 (folded) with `"serve"` and `"batch"` and their help texts lit GREEN.
SAY: The lecture says Cloud Run runs a container as a service or a job. The demo app shows both: one image, two startup commands, serve or batch.

SHOW: The panel switches to CODE(…/__main__.py: 22–26), lines 23–24 lit (`PORT` default "8080", `--bind
0.0.0.0:{port}`); a PURPLE "gunicorn" chip slides out of the `serve` tag. The service strip draws: a dashed BLUE
instance with an ear glyph "listening on :8080"; YELLOW request pulses arrive from the left (PINK arrows), each answered
by a return arrow.
SAY: Serve starts gunicorn, a web server, on the port Cloud Run gives it, 8080 by default. Then it waits, and answers each request that arrives.

SHOW: A burst of pulses: a second dashed instance splits off (a GRAY chip "max instances 2"), both answer; the pulses
stop, both instances dissolve to nothing ("scale to zero"). A PINK URL chip `https://…run.app` stays above the strip.
SAY: That shape is a service. It has a URL, adds instances when traffic rises, and can scale to zero when it stops. It never finishes on purpose: listening is its job.

SHOW: The service strip shrinks to the upper half. The job strip draws under it from the `batch` tag: one TEAL block
running through four GREEN segments as each is named: "read", "translate", "speak", "save", then a hard right edge
"exit 0". CODE(…/__main__.py: 52–61): lines 53–57 light in step with the segments; then lines 58–61 light RED and a
second, short strip ends in a RED edge "exit 1"; line 59's comment "so execution status is truthful" lights YELLOW.
SAY: Batch has a different shape. It reads the passage, translates it, generates speech, saves the files, and exits. If a step fails, it exits with status 1, so the execution shows failed, not a false success.

SHOW: The code panel switches to CODE(serverless-deployment/README.md: 582–585), line 585 "That is a **job**, rather
than an HTTP service waiting for requests" lit YELLOW. Beside the job strip: a crossed-out PINK URL chip and a GRAY chip
"no URL · it exits" (excerpt chip `README.md · line 833 (excerpt)`: "The job exits; it does not provide a web URL").
SAY: The README calls this a job: no URL, nothing waiting for requests. Something starts it, and it runs to completion.

SHOW: S01's endless RED-edged strip returns from the top and lands on the job row, its `serve` tag lit RED. CODE(
serverless-deployment/README.md: 747–748) lights "This replaces the image's web-server command". The `serve` tag
transforms into a GREEN chip row `python` · `-m translation_demo batch …` (excerpt chip `README.md · lines 755–765`,
the argument chips shown with `gs://YOUR_INPUT_BUCKET/…`, `gs://YOUR_OUTPUT_BUCKET/…`); the endless strip is cut and
snaps into the four-segment job shape with its "exit 0" edge.
SAY: Now the hook. The job inherited the image's default command, serve, so it started a web server and waited for requests that never come. The fix: the command python, with the batch arguments. Same image, and now the strip ends.

SHOW: The two strips side by side, small. Above the job strip: a GREY "Execute" button presses, a PINK trigger drops
onto the strip, it runs and ends. Then a BLUE Cloud Scheduler clock (no logo) appears beside it with a GRAY caption
"not in this README"; at each "night" tick on a small timeline a PINK trigger drops and a new job strip runs and ends.
SAY: Who presses start? In the README, you click Execute. For a nightly run, the usual trigger is Cloud Scheduler, which this README does not use.

SHOW: The strips and the Scheduler clock fade out (everything else ≤ 20 %). PONDER P1 card. Question: "A container
indexes new documents from a bucket, writes embeddings to another bucket, then exits. It runs once an hour. Best fit?"
A · "Cloud Run service, min instances 1, looping" · B · "Cloud Run job, run hourly by Cloud Scheduler" · C · "Cloud
Run service that indexes at startup, then exits" · D · "Compute Engine VM with a cron entry".
SAY: Try one. A container indexes new documents and exits, once an hour. Read the lifecycle, not the product names.
PONDER(10 s, P1)

SHOW: Reveal. B fills YELLOW ✓, GREEN note "finite work · runs to completion · billed only while it runs". RED reasons
write in under A "pays for an always-on instance · between requests its CPU is throttled, so a loop stalls", under C "a
service must keep listening on $PORT · exiting = a crashed instance", under D "works, but the VM bills every idle
minute between runs".
SAY: B, a job on a Cloud Scheduler timetable: it runs to completion and costs nothing between runs. A pays for an instance all hour, and an idle service's CPU is throttled, so the loop stalls. C breaks the service contract: an instance that exits has crashed. D works, but the VM is paid for all hour while it idles. Why that matters is next.

SHOW: The card fades. RULE: "runs, writes output, exits · 'every night' → job (+ Cloud Scheduler) / answers requests ·
URL · port → service". The card shrinks into map slot 1, which turns GREEN-ticked. Everything else fades.
SAY: So the rule: if the question says it runs, writes its output and exits, or that it runs every night, pick a job. If it says it answers requests, has a URL, or listens on a port, pick a service.

---

## S03 · Who pays for the idle hours? — `s03_meter.py` · `IdleMeter`

Lecture: 14 · 8, 11, 14, 16; then 15 · 11.

SHOW: LECTURE 14 · 8, 11, 14. Map slot 2 pulses. Three GRAY lecture chips write in and stack top left: "brings down
code execution cost" (slide 8), "pay only for the time your code runs" (11), "only pay when your code is running" (14).
V2 builds: a 24-hour axis (00:00 to 24:00) across the middle, with nine YELLOW request ticks scattered in two clusters.
SAY: The lecture promises you pay only while your code runs. Let's make that exact: two meters, one day. The yellow ticks are requests.

SHOW: Top row: a solid BLUE VM rack at the left, a GOLD bar meter on the right filling at a constant rate as a cursor
sweeps the day; the stretches between ticks shade GOLD ("idle · billed").
SAY: The top row is a virtual machine. Its meter runs from boot to shutdown, requests or not. The gold shading is idle time, and you pay for all of it.

SHOW: Bottom row: at each tick a dashed BLUE instance blinks into existence for an instant and vanishes; its GOLD meter
steps up by one small block per tick, flat in between. CODE(serverless-deployment/README.md: 281–283) beside it,
"Request-based" and "Minimum number of instances `0`" lit GOLD.
SAY: The bottom row is a function, or a Cloud Run service with request-based billing and minimum instances 0, as in the README. Its meter moves only with invocations and how long each one runs.

SHOW: Transform 1. The panel fades. The axis stretches (the idle gaps widen, the ticks keep their count and width); the
VM meter grows by the added gold; the function meter does not move (a GRAY "+0" chip). A YELLOW caption "more idle
time".
SAY: Now stretch the quiet gaps between requests. The VM meter grows, because idle hours are still provisioned hours. The function meter does not move at all: no requests, no charge.

SHOW: LECTURE 14 · 16. On the bottom row, after the longest gap, a small GRAY puff appears in front of the first tick's
instance and the tick is delayed by a beat (RED "cold start"). Excerpt chip `README.md · line 223 (excerpt)` with the
minimum-instances sentence. A GOLD slider "minimum instances" moves from 0 to 1: a faint dashed instance stays on along
the whole bottom row with its own steady GOLD drip, and the puff on the first tick after the gap disappears; during the
next burst a second instance still starts with a small GRAY puff, chip "fewer cold starts, not none".
SAY: Zero idle cost has a price, and slide 16 names it: the cold start. After a quiet stretch, the first request waits while an instance starts. The README's remedy is minimum instances. Set it to 1, and a warm instance stays on for the first request, with its own meter running.

SHOW: The always-on instance and its drip lift up into the VM row, beside the rack (a GRAY bracket "always on").
LECTURE 15 · 11. A BLUE "Vertex AI endpoint" card slides into the same row; excerpt chip `model-deployment/cli.py ·
line 215`: `min_replica_count=1` lit GOLD, next to excerpt chip `model-deployment/README.md · line 66 (excerpt)`: "This is
the part that costs money."
SAY: That always-on instance now sits in the VM row. So does next lecture's Vertex AI endpoint: its deploy call asks for a minimum replica count of 1, which the README calls the part that costs money.

SHOW: The meters and chips fade to a single GRAY "?" (everything else ≤ 20 %), then the PONDER P2 card. Question:
"Ignore free tiers. Same work on a Cloud Run function (min instances 0) and on an always-on VM. Next month: twice the
requests, same length, same days. Which bill changes?" A · "Only the VM's" · B · "Only the function's" · C · "Both
double" · D · "Neither: serverless has no minimum charge".
SAY: Test it on a new case. Twice as many requests, each just as long, in the same days. Which bill changes?
PONDER(10 s, P2)

SHOW: Reveal. The meters come back and transform 2 plays: the axis is one day again, every tick splits into two (18
ticks), the function meter climbs block by block, the VM meter stays exactly where it was (a GRAY "flat" chip, small
GRAY footnote "until it runs out of capacity"). B fills YELLOW ✓, GREEN note "more invocations · more execution time".
RED reasons write in: A "the VM bills provisioned hours: unchanged"; C "the VM is flat with traffic"; D "no minimum ≠
free work: idle is free, requests are not".
SAY: B, only the function's. Watch: every request splits in two, and the function meter climbs, since every invocation and its running time are billed. The VM meter does not move, because it bills provisioned hours: A is backwards, and C is wrong. D confuses no minimum charge with free work.

SHOW: The card fades. A GOLD-outlined card: "Is anything always on?" with two arrows drawing one after the other as
they are said: "idle time → always-on bills only" and "requests × duration → pay-per-use bill only"; a chip "serverless
= cheap" is struck RED on "is not". Then RULE: "idle time changes → only always-on bills move (VM · min instances ≥ 1 ·
endpoint replica) / request count or duration changes → only the pay-per-use bill moves"; it shrinks into map slot 2.
Everything else fades.
SAY: So the rule is not, serverless is cheap. The rule is: is anything always on? Idle time moves only the bills of always-on things. Request count and duration move only the pay-per-use bill.

---

## S04 · Function or container: what you hand over — `s04_handover.py` · `WhatYouHandOver`

Lecture: 14 · 10–12, 14–15.

SHOW: LECTURE 14 · 10. Map slot 3 pulses. V3: a GREEN code block "Simple Translate App" at the left (our drawing of the
slide's sketch, three comment lines only) with four arrows to a 2×2 grid: rows "virtual machine" (solid BLUE racks) and
"serverless" (dashed BLUE outlines), columns "a code file" (`main.py` page) and "a container" (TEAL box). The two VM
cells tick in with GRAY chips "Lecture 1", "Lecture 2"; the two serverless cells light YELLOW.
SAY: Next, what you hand over. The lecture deploys one translate app four ways: virtual machine or serverless, code file or container. Earlier lectures filled the VM row. Today fills the serverless row.

SHOW: LECTURE 14 · 11–12. The serverless-file cell zooms open. Three GREEN items slide in: a `main.py` page, a
`requirements.txt` page, and a name tag "entry point: hello_http". CODE(serverless-deployment/tutorial/function/main.py:
3–12): line 7 `@functions_framework.http` lit PURPLE, line 8 `def hello_http(request):` lit GREEN, lines 9–11
(`request.args.get` with defaults) lit PINK. Then CODE(…/function/requirements.txt: 1–2) below it, small.
SAY: For a function you hand over a source file, its requirements file, and one name. The file is main.py: an HTTP handler called hello underscore HTTP, which reads the text and two language codes from the request.

SHOW: CODE(serverless-deployment/README.md: 150–151), "not the filename or service name" lit YELLOW. The name tag
pulses and a thin PINK thread ties it to line 8's `hello_http`.
SAY: That name is the entry point: the Python function the framework should call. Not the file name, and not the service name.

SHOW: The three items flow right into a PURPLE "Cloud Build" box; out comes a TEAL image that drops into a BLUE
"Artifact Registry" shelf, then runs as a dashed BLUE instance whose inner PURPLE layer "functions-framework" reaches
for `hello_http` by its name (a GREEN arrow). CODE(serverless-deployment/README.md: 212–216), "publishes an application
image in Artifact Registry" and "at **build time**, not on every request" lit.
SAY: Then Google builds. Cloud Build installs the requirements, configures the Functions Framework, and publishes an image to Artifact Registry. This happens once, at build time, not on every request.

SHOW: The name tag flips to "entry point: main"; the framework's arrow searches the file, finds no `def main`, and snaps
RED; a RED "function build failed" chip and a GRAY chip "build logs · README.md line 1038" (row "Function build fails | Build
logs, runtime, requirements, entry point…"). The tag flips back to `hello_http`, the arrow turns GREEN again.
SAY: The framework finds your function by that name. Type main as the entry point, and there is nothing called main to find. The function build fails, and its build logs tell you why.

SHOW: Two GRAY lecture chips: slide 11 "without managing servers or containers" with "managing" underlined YELLOW,
and the slides' product name "Cloud Function" beside the README's path "Cloud Run → Services → Write a function"
(excerpt chip `README.md · line 99 (excerpt)`); a TEAL container outline fades in around the running function.
SAY: Slide 11 says a function runs without managing containers. You do not manage one, but Google still builds one. And the slides' Cloud Functions are now Cloud Run functions.

SHOW: LECTURE 14 · 14–15. The serverless-container cell zooms open: a PINK image URL chip
`cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` goes straight to a dashed BLUE revision, with no build
box (a GRAY struck-out "Cloud Build"). CODE(serverless-deployment/tutorial/app/Dockerfile: 1–12) (folded: 1, 2, 11,
12): line 1 `FROM python:3.12-slim-bookworm` lit ORANGE, line 2's `PORT=8080` and line 12 `CMD …` lit GREEN (line 11
`EXPOSE` stays unlit: it only documents the port); the instance gains the ear "listening on :8080". Excerpt chip
`README.md · lines 273–274 (excerpt)`: "Deploy one revision from an existing container image".
SAY: For a Cloud Run service, you hand over a finished image by its URL. Deploying it builds nothing: the image was built beforehand. Its Dockerfile picks the base Python, the default port, 8080, and the startup command. You control all three.

SHOW: Both cells' instances side by side. A PINK URL with a query string writes onto the function's instance:
`…?text=Good%20afternoon%20everyone&src=en&dest=fr` (excerpt chip `README.md · line 163`), the three parameters light
in turn and flow into lines 9–11's `request.args.get`; then `dest=fr` swaps to `dest=el` without any build animation
(excerpt chip `README.md · line 171 (excerpt)`: "the same endpoint accepts different inputs without a redeploy").
SAY: Both are called through an HTTPS URL. The function takes new inputs through its query string, with no redeploy.

SHOW: The two instances slide together and become one dashed BLUE instance with a TEAL container inside; caption "a
function is a container you did not write". RULE: "source + requirements + entry point → function (Google builds the
image) / your image · OS libraries · startup command → Cloud Run service"; it shrinks into map slot 3. Everything else
fades.
SAY: Both end as the same thing: a container instance on Cloud Run. A function is a container you did not write. On the quiz, source plus an entry point means a function. Your own image, or your own startup command, means a service.

---

## S05 · Who may call it, who it runs as, where to look — `s05_identity.py` · `TwoQuestions`

Lecture: 14 · 16.

SHOW: Map slot 4 pulses. V4: a BLUE service box "translation-demo" center with a door on each side. CODE(
serverless-deployment/README.md: 361–362) above it, "who may call our public app" lit PINK, "what the running app may
access" lit BLUE.
SAY: Every deployed service faces two permission questions, and the README keeps them separate. Who may call our public app? And what may the running app access?

SHOW: Left door, "who may call it". A schematic toggle "Allow public access" (tag `illustration`, excerpt chip
`README.md · line 281 (excerpt)`): ON — a GREY browser's PINK request passes through the door; OFF — the next request
bounces RED with "403", and the code box inside stays dark.
SAY: The left door is the caller. With public access allowed, any browser's request gets in. Without it, a caller with no permission is turned away with a 403, before your code even runs.

SHOW: Right door, "who it is when it calls out". A BLUE badge pins onto the instance: "translation-demo-runtime"
(email chip `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com`); two role chips attach: "Agent
Platform User", "Service Usage Consumer". CODE(serverless-deployment/README.md: 374–380) (folded: 374–376, 380), line
380 "You do not need to create or download a key" lit YELLOW; a dashed GOLD key glyph appears and is crossed out.
SAY: The right door is who your code is when it calls out. The web app wears a service account badge, translation demo runtime, with two roles: Agent Platform User and Service Usage Consumer. You do not create or download a key.

SHOW: The left door and the README panel fade first. CODE(serverless-deployment/tutorial/app/translation_demo/speech.py:
101–109), lines 102–105
`google.auth.default(...)` lit BLUE, line 109's message ("Configure local ADC or attach an authorized runtime service
account") lit GRAY. A small token glyph flows from a BLUE "Cloud Run" platform block into the badge, then a PINK request
leaves the right door toward a BLUE "Agent Platform" block.
SAY: The code just asks for default credentials, and on Cloud Run the platform hands it a token for the attached account. No key file anywhere.

SHOW: A GREY "you" figure at the bottom; a thin arrow from "you" to the badge, labelled "Service Account User"
(CODE(serverless-deployment/README.md: 432–434), "to attach it" lit). A GRAY chip "a deployment permission ≠ the
badge's roles".
SAY: One more arrow, from you. To attach that badge to a service, your own identity needs Service Account User on it. That is a deployment permission, separate from what the badge itself may do.

SHOW: A second, smaller BLUE box "translation-audio (job)" slides in beside the service with its own badge
"translation-audio-job"; four chips attach: BLUE "Agent Platform User", "Service Usage Consumer", PINK "Storage Object
Viewer · input bucket", "Storage Object Creator · output bucket" (CODE(serverless-deployment/README.md: 681–690)
(folded: 681–682, 683–685, 686–688, 689–690)). The web badge gets a GRAY "no bucket roles" chip.
SAY: The job gets its own badge. It has the same two Agent Platform roles, plus Storage Object Viewer on the input bucket and Storage Object Creator on the output bucket. The web app's account needs no bucket roles, because its audio goes straight to the browser. One badge per workload.

SHOW: LECTURE 14 · 16. The doors fade. A GRAY lecture chip "limited control and debugging" (slide 16). Three log
windows light up in turn as named: "build logs" (function build), "service logs" (a failed request), "job execution
logs". CODE(serverless-deployment/README.md: 1038–1040, 1043, 1045) (folded): line 1038 with the build-logs window,
line 1040 ("Speech request is denied | Attached identity…") lit BLUE, line 1045 ("Output folder is empty or incomplete |
Execution status, logs…") with the job-execution-logs window; excerpt chip `README.md · lines 228–229 (excerpt)`:
"inspect logs rather than treating a completed build as proof that translation worked", lit YELLOW.
SAY: Slide 16 warns that serverless is harder to debug. The README says where to look: build logs when a function build fails, service logs when a request fails, and the job's execution logs. A finished build is not proof that it works.

SHOW: RULE: "who may call → public access · refused at the door, code never runs / what the code may touch → the
service account's roles (no key) · a denied call from your code → fix the badge"; it shrinks into map slot 4.
Everything else fades.
SAY: The rule: public access answers who may call, and a refused caller is stopped before your code runs. The service account answers what your code may touch. When your own code is denied, fix the badge's roles, not the caller.

---

## S06 · Where preprocessing lives — `s06_preprocess.py` · `ThinClients`

Lecture: 15 · 11, 13.

SHOW: LECTURE 15 · 11. Map slot 5 pulses. A dashed BLUE Cloud Run instance morphs into a BLUE "Vertex AI endpoint"
box at the right. Two GREY clients write in at the left: a phone app and a web page.
SAY: To serve a trained model, the next lecture uses a Vertex AI endpoint, and the quiz asks where its preprocessing should live. Picture two clients: a phone app, and a web page.

SHOW: LECTURE 15 · 13. V5: each client gets a GREEN gear icon; beside the first client's gear a GREEN chip column writes
in as named: "decode JPEG", "scale to 0–1", "resize 224×224" (shown once; the second client's gear stays unlabelled);
a PINK arrow from each gear carries a "float tensor" chip to the endpoint.
SAY: Each client carries the same gear: decode the JPEG, scale the pixels to between 0 and 1, and resize to 224 by 224. Only then does it send numbers to the model. That is two copies of one recipe, in two code bases.

SHOW: The web page's gear quietly changes one step ("resize: crop first", RED outline); its arrow's tensor chip turns
RED and travels along the arrow into the endpoint at "quietly receives another"; the web page's answer bubble turns
RED. A GRAY lecture chip: "client-side brittleness" (slide 13).
SAY: The lecture calls this client-side brittleness. Every client preprocesses slightly differently, and a model trained on one recipe quietly receives another.

SHOW: Both gears lift off the clients and merge into one GREEN gear inside the endpoint. The arrows now carry PINK
`{"bytes_inputs": {"b64": "…"}}` chips (excerpt chip `model-deployment/README.md · line 191`). CODE(
model-deployment/README.md: 60–60) (wrap), "The preprocessing travels with the model, so every client gets exactly the
same preprocessing that was used in training" lit YELLOW.
SAY: Now move the gear into the endpoint. Clients send raw JPEG bytes, wrapped as base64, because JSON cannot carry raw bytes. The preprocessing travels with the model, so every client gets exactly the preprocessing used in training.

SHOW: CODE(model-deployment/cli.py: 245–255): lines 250–253 (the base64 `instances` list) lit PINK, line 255
`endpoint.predict(instances=instances)` lit YELLOW; a GRAY chip "no resize · no normalize" next to the phone.
SAY: Look at the repo's own client. It reads the image files, base64 encodes them, and calls predict. No resizing, no normalizing. That is a thin client.

SHOW: A version dial on the endpoint, "v1". It turns to "v2": the gear gets a RED tooth ("bad resize") and both
clients' answer bubbles turn RED at the same instant. It turns back to "v1": both turn healthy at the same instant
(a YELLOW flash on both). GRAY chip "one deployment · no client release".
SAY: Now ship a bad resize in version 2. Both clients break at once. Roll back to version 1, and both are healthy at the same instant. One deployment fixed everyone, with no client release.

SHOW: Replay, labelled "preprocessing on the clients": the gears return to the clients, the version dial grays out.
SAY: Now put the gears back on the clients. What does the same rollback cost?
PONDER(6 s, "Gears on the clients: what does one rollback cost?")

SHOW: The fix becomes two horizontal release bars on a `timeline` (no GOLD): "phone app · app-store review" ending
late, "web deploy" ending early; between their right ends a RED band "clients disagree".
SAY: Two releases: a phone update waiting in app store review, and a web deploy. They land at different times, and in between, the clients disagree.

SHOW: RULE: "several clients · update or roll back once · no client release → preprocessing at the endpoint / on the
clients → every client re-released in lockstep"; it shrinks into map slot 5 (half-filled: the gear). Everything else
fades.
SAY: The rule: when the question says several clients, one place to update or roll back, and no client release, put preprocessing at the endpoint. Preprocessing on the clients means every client is re-released in lockstep.

---

## S07 · Register serve: preprocess, then model — `s07_signature.py` · `ServeSignature`

Lecture: 15 · 14.

SHOW: LECTURE 15 · 14. Map slot 5 pulses again. V6: a pipeline of blocks left to right, writing in as named: PINK
"JPEG bytes" → GREEN "decode" → GREEN "to float" → GREEN "resize" → GREEN "model" → four bars "parmigiano · gruyere ·
brie · gouda" (labels from `model-deployment/README.md · line 187`).
SAY: Preprocessing at the endpoint works only if the endpoint calls the right function. Here is the chain: JPEG bytes, decode, convert to floats, resize, the model, and four probabilities, one per cheese.

SHOW: CODE(model-deployment/cli.py: 100–105): line 102 `decode_jpeg`, 103 `convert_image_dtype(…, tf.float32)`, 104
`resize(…, size=(224, 224))` light in step with the three GREEN blocks; a bracket "preprocess_image" closes around
them; line 105 `return resized` lit, and a small 224×224×3 image glyph pops out of the bracket.
SAY: In the repo, preprocess image does the first three steps, for one image. It returns an image, not an answer.

SHOW: CODE(model-deployment/cli.py: 107–114): line 109 `input_signature=[tf.TensorSpec([None], tf.string)]` lit PINK
("a batch of strings"), lines 111–113 `tf.map_fn(preprocess_image, …)` lit GREEN, line 114 `prediction_model(images,
training=False)` lit GREEN; a larger bracket "serving_function" closes around all five blocks, with a small GRAY alias
chip "a.k.a. serve" under it. Line 108's comment ("The argument name (bytes_inputs) is the key clients must use") lit
YELLOW, linking to S06's PINK request chip.
SAY: The serving function takes a batch of strings, maps preprocess image over each one, then calls the model. Preprocessing and inference, in one function. Its argument, bytes inputs, is the key clients use. Exam questions may call this function serve: not the web app's serve command, but the function that preprocesses, then predicts.

SHOW: CODE(model-deployment/cli.py: 116–123): line 122 `add_endpoint(name="serving_default", fn=serving_function)` lit
YELLOW. An export socket labelled `serving_default` appears on a GREEN "SavedModel" block, empty; a PURPLE "model
server" box connects to it. A GRAY lecture chip "slide 14: tf.saved_model.save(…, signatures={"serving_default": …})"
beside lines 117–119 (the comment) lit GRAY.
SAY: The export registers it under the name serving default, and the model server calls whatever sits behind that name. The slide saves it with a different call; the idea is the same.

SHOW: The socket stays, empty, docked at the right; everything else ≤ 20 %. PONDER P3 card. Question: "serving_default
is the raw model. The phone app sends resized float arrays; a new web client sends JPEG bytes. One place to fix or roll
back preprocessing: what do they register?" A · "The raw model: the server decodes JPEGs" · B · "preprocess_image" ·
C · "A function: preprocess each image, then call the model" · D · "The raw model, plus the resize code copied into the
web client".
SAY: Before we try plugs, one last check. A phone app sends float arrays, a new web client sends JPEG bytes, and the team wants one place to fix preprocessing. What should they register?
PONDER(12 s, P3)

SHOW: Reveal by plugs. The card docks small at the right; each plug carries its option letter badge. Plug B: a GREEN
plug "preprocess_image" pushes into the socket; a request's JPEG bytes go in and a 224×224×3 image glyph comes out (RED
✗, "no prediction"); on the card, under B, RED "returns 224×224 images, not predictions".
SAY: Try B first: register preprocess image alone. A request comes back as a 224 by 224 image. Nothing was classified.

SHOW: Plug A/D: the plug "raw model" pushes in; the socket's label changes to "expects float tensors 224×224×3"; the
PINK bytes chip bounces RED; S06's gears jump back onto the two GREY clients (V5 rewound), the RED "clients disagree"
band flickers once. On the card, RED under A "the server only turns base64 into bytes · the signature decides what they
become"; under D "two copies to keep in sync · every rollback = two client releases".
SAY: A and D keep the raw model. It demands float tensors, so JPEG bytes no longer fit. The server only turns base64 back into bytes. The gears jump back onto every client: two copies to keep in sync.

SHOW: Plug C: "serving_function" pushes in; bytes go in, the four probability bars rise, brie tallest, YELLOW. On the
card, C fills YELLOW ✓, GREEN note "after one switch to bytes · every later fix or rollback = one deployment". CODE(
model-deployment/cli.py: 157–163) (folded: 157–158, 160, 163): line 158 `signature_def["serving_default"]` and line
163 `signature.inputs["bytes_inputs"]` lit YELLOW; line 160's comment lit GRAY. The card fades.
SAY: C, the serving function: bytes go in, probabilities come out. The phone app switches to sending bytes once; after that, one exported version holds the recipe, and every fix or rollback is one deployment. The repo's test step loads serving default and feeds it bytes inputs, as the server will.

SHOW: S04's name tag "entry point: hello_http" slides in on the left, the socket "serving_default" on the right, and a
YELLOW bracket joins them: "the platform calls the name you register".
SAY: This echoes the function's entry point: the platform calls exactly the name you registered, and nothing downstream can fix a wrong one.

SHOW: RULE: "register the function that does preprocessing AND inference / preprocess alone → images · raw model →
every client preprocesses"; it shrinks into map slot 5, which is now full and GREEN-ticked. Everything else fades.
SAY: The rule: register the function that does preprocessing and inference. Preprocessing alone returns images, and the raw model makes every client preprocess.

---

## S08 · Seven rules for Tuesday — `s08_recap.py` · `Recap`

Lecture: 14 · 16; 15 · 16–17.

SHOW: The exam map expands into a list of seven rule rows, each with its set-piece icon at the left (V1's two strips,
V2's two meters, V2's cold-start puff, V3's grid, V4's two doors, V5's single gear, V6's plug); rows 1–3 write in as
named, the rest stay as empty outlines.
SAY: Seven rules for Tuesday. One: read the lifecycle. If it listens, it is a service; if it runs and exits, it is a job, started on demand or by Cloud Scheduler. Two: idle time costs only what is always on. Three: pay-per-use bills invocations and execution time, and zero idle cost buys you cold starts.

SHOW: Rows 4–5 write in: "function = source + requirements + entry point (Google builds the image) · service = your
image"; "who may call (public access) ≠ who it runs as (service account · no key)".
SAY: Four: a function is source, requirements and an entry point, and Google builds the image; a service is your own image. Five: who may call it is not who it runs as, and the runtime service account needs no key.

SHOW: Rows 6–7 write in: "preprocess at the endpoint: one deployment updates or rolls back every client"; "register
the serving function (serve) = preprocess, then model · the platform calls the name you register". All seven rows glow YELLOW once.
SAY: Six: preprocess at the endpoint, so one deployment updates or rolls back every client. Seven: register the serving function that preprocesses and then calls the model, because the platform calls exactly the name you register.

SHOW: LECTURE 15 · 16–17. The list shrinks left. Right: a two-column card (our drawing of the comparison's last row)
"Vertex AI Online Prediction · serve a trained model in production" vs "Cloud Run · ML as part of a broader app".
LECTURE 14 · 16: under it three GRAY chips "vendor lock-in", "cold starts", "harder debugging".
SAY: Which one to use? The next lecture's rule of thumb: Vertex AI to serve a trained model in production, Cloud Run when the model is part of a broader app. And remember the costs on slide 16: vendor lock-in, cold starts, harder debugging.

SHOW: Everything fades except a small GRAY line "AC215 · Lecture 14 · exam edition"; it fades to an empty frame.
SAY: That's the lecture in seven rules. Good luck on Tuesday.
