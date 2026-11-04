# AC215 · Lecture 14 — Serverless deployment: a function, a service and a job on Cloud Run — narration script & visual plan (v2, review merge 2026-11-04)

Audience: an AC215 student who has done L1–L13: a GCP project with billing (L1), images,
containers, `docker run -p` and `PORT` (L2–L4), a service-account JSON key in `secrets/` (L3,
L10), uv (L1) and last week's Vertex AI training job (L13). They have seen Lecture 14. New to
them: Cloud Run functions (what the console wants, what Cloud Build makes of it, the entry point),
the container contract on Cloud Run (`PORT`, `0.0.0.0`, one image whose `CMD` starts gunicorn),
min/max instances, concurrency and request-based billing, revisions, tag vs digest, the runtime
service account (no key) vs public access, ADC with impersonation, Cloud Run jobs with a container
command and separate arguments, and job outputs proven by a manifest. They watch with their clone
of `dlops-io/serverless-deployment` open, Docker running, gcloud installed and their own project
selected, pausing to run every step. **This lecture creates billable cloud resources and calls a
paid model** (GOLD tags where each starts, the clean-up checklist at the end).

Goal (BRIEF "Audience and goal"): after the video they can place the README's four parts on the
lecture's 2×2 (a file or a container × a rented machine or serverless); deploy Part 1's handler as
a Cloud Run function with `main.py`, `requirements.txt` and the entry point `hello_http`, say what
Cloud Build turns them into and what a wrong entry point prints, and call it with a query string;
run the prebuilt image locally and read every part of `docker run --rm -p 8086:8080 …`; deploy the
same image as a service and read min 0 / max 2 / concurrency 4 against gunicorn's 4 threads,
request-based billing, revisions, tag vs digest; keep "who may call it" (Allow public access) apart
from "who it runs as" (the attached runtime account, no key), know that attaching it takes their own
Service Account User, and use impersonated ADC locally; run the same image as a job, explain the
`python` command and the eleven separate argument chips and what a job that never finishes did
wrong; prove success by a `manifest.json`, submit new work with `--args` overrides and the helper,
and clean everything up, including what the README leaves out.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest or the slides and the captures disagree, the captures win, and the
video says so kindly. **README = `README.md` @ `46cc62f`** (`main` on 2026-11-04, the commit the
course link serves and the exam edition `../ac215-l14-exam/` quotes); the course map's older pin
`4eaf343` appears only in S02's one kind sentence. Nothing in a terminal panel is typed by hand:
every output line below names its capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown,
  no raw symbols (`/`, `=`, `%`, `&`, `$`, `→`); commands, flags and paths are on screen and said in
  words ("publish port 8086 to 8080", "percent 20", "gs, your input bucket, run zero zero one",
  "Control C", "translation demo serve"). `hello_http` is said "hello underscore HTTP" (as in the
  exam edition), `run-001` / `run-002` "run zero zero one / two", `zh-cn` "Z H dash C N",
  `translation_demo` "translation demo", files as "main.py" (lexicon entry), "the requirements
  file", "manifest dot json", "translated dot txt", "speech dot wav", "passage dot txt". Numbers
  are digits; never a "!" after a digit. No tool version is spoken: versions sit on screen with
  "at the time of recording"; Python 3.12 / 3.10 are the README's (3.12) and the old README's
  (3.10) runtimes and are said plainly. No prices or free-tier numbers anywhere.
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name (never "gunicorn …"
  or "googletrans …" at a sentence start: "Then gunicorn …", "The googletrans library …"). No
  `'s` on a word with a lexicon entry or candidate. No bare "a" right before a lexicon entry or
  candidate (the splicer reads it as the letter): "the 403", never "a 8080". No homographs: never
  "read", "live", "lives", "close", "lead", "tear" (so "clean up", never "teardown" in SAY),
  "minute", "content", "record" (so "note the email"). No abbreviations with inner dots. American
  spelling on screen and in SAY ("gray"; the colour constants stay GREY). The main clause comes
  first so the Chinese subtitles keep English clause order.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on
  an empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). Five in the video,
  BRIEF's table, Conny's 2026-10-21 density decision: P1 S05 (8 s), P2 S08 (8 s), P3 S09 (6 s),
  P4 S13 (8 s), P5 S14 (6 s). The SAY before each card speaks the question; the answer is the next
  SAY. Nothing during the timer shows the answer.
- `TERM(laptop/NN: lines)`: a terminal beat. `laptop/NN` is the one file
  `assets/terminal/laptop/NN-*.txt` (`dev/NN`, `gcloud/NN`, `dev/provider-timeout/NN` likewise).
  The scene types the command written just before it in the SHOW line (in backticks, exactly as
  the README spells it; extras exactly as the capture's first line(s) spell them), then prints the
  listed **file** lines. The `$ …` command lines are typed, never printed (a multi-line command
  occupies lines 1–k: `laptop/10:1–2`, `laptop/16:1–6`, `dev/10:1–2`, `dev/11:1–3`,
  `dev/24:1–4`, `gcloud/05:1–4`, `gcloud/09:1–4`, `gcloud/10:1–4`, `gcloud/11:1–4`,
  `gcloud/18:1–5`, `gcloud/20:1–4`, `laptop/41`–`43:1–4`); `[exit N]` is never printed. Inside
  the line list: `…` = print one `…` line; `wrap` = fold long lines (`Terminal.print(…, wrap=True)`);
  `from "…"` = print that long line from the quoted phrase on, after a `…`; `→ (no output)` = the
  prompt simply returns. Blank output lines (`laptop/21:3`, `24:3`, …) are dropped.
- **No output panel** (BRIEF "Notes"): a gcloud box whose success the repo documents nowhere as
  text, or that needs a browser sign-in, is typed verbatim and gets no panel; a GREY chip under
  it says "needs your project · no output shown", and the SAY says what to look for. Never an
  invented line.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` (at `46cc62f`) from line a to b
  with the real line numbers, header `path · lines a–b`; at most 12 lines on screen. A "README
  card" is a GREY quote of README text, header `README.md · lines a–b` (markdown stripped).
- `CONSOLE(…)`: a schematic console form drawn with `console_form(title, rows)` (no Google
  branding, no logo, never a screenshot), tag `illustration`, with field labels and values only
  from the README lines named. Button labels as the README writes them (**Write a function**,
  **Create**, **Save and redeploy**, **View diff & redeploy**, **Deploy changes**, **Execute**).
  No URLs with ids, no progress numbers, no execution ids except the README's
  `translation-audio-hq9f5` / `de2f41…`.
- `RECORDED(expected/<file>: lines)`: a GREY-outlined panel quoting those lines of
  `assets/terminal/expected/<file>` (the bracketed source column dropped), tag `recorded ·
  <source>` naming the README line or GIF caption ("README:183", "function GIF"). These are what
  the course's console recording shows; the SAY says "the README's recording" or "the recording".
  `expected/part4-task-log-shape.txt` is tagged `illustration` (it is a shape, not an output).
- `TRACKER [k] n`: the `ReadmeTracker`, top-left in every walkthrough scene, for README subsection
  `k`, at step n. `TRACKER [k] n · extra` = same step, caption " · extra" while a command the
  README does not have is on screen; `· extra · local stand-in` for the function stand-in (dev/20–29);
  `· gcloud alternative` while a README gcloud box is typed (the boxes are alternatives, not extra
  steps, README:19-21, so the tracker stays on the console step they replace). One tracker per README
  subsection, titled with the README's own heading (BRIEF table), step titles ≤ 3 words:
  - [BB] "README › Before you begin" (README:26-89), 5: 1 Select project · 2 Billing, permissions ·
    3 Choose region · 4 Clone repo · 5 Terminal setup.
  - [1.1] "README › 1.1 Create the function" (97-109), 6: 1 Write a function · 2 Enable APIs ·
    3 Name, region · 4 Python 3.12 · 5 Public access · 6 Source editor.
  - [1.2] "README › 1.2 Supply the code" (124-152), 4: 1 Replace main.py · 2 Replace requirements ·
    3 Entry point · 4 Save and redeploy.
  - [1.3] "README › 1.3 Call the endpoint" (154-173), 5: 1 Copy URL · 2 Default call · 3 Query
    string · 4 Other languages · 5 Check logs.
  - [2.1] "README › 2.1 Try it locally" (242-268), 4: 1 docker run · 2 Open localhost ·
    3 Translate · 4 Ctrl+C.
  - [2.2] "README › 2.2 Deploy the same image" (270-296), 10: 1 Deploy container · 2 Image URL ·
    3 Name, region · 4 Public, request-based · 5 Scaling 0–2 · 6 Container settings · 7 Request
    settings · 8 Create · 9 Open URL · 10 Revisions, logs.
  - [3.1] "README › 3.1 API and identity" (364-380), 5: 1 Enable API · 2 Create account · 3 Name
    and ID · 4 Two roles · 5 Record email.
  - [3.2] "README › 3.2 Attach and speak" (430-458), 7: 1 Open service · 2 Security tab · 3 Three
    variables · 4 View diff · 5 Wait rollout · 6 Play audio · 7 Read logs.
  - [3.3] "README › 3.3 Develop locally · optional" (504-578; the README's collapsed "Try it locally"), 5: 1 Token Creator · 2 ADC login · 3 uv sync ·
    4 Run serve · 5 cd ../..
  - [4.1] "README › 4.1 Two buckets" (593-621), 6: 1 Create bucket · 2 Unique name · 3 Wizard
    settings · 4 Output bucket · 5 Upload passage · 6 Copy URI.
  - [4.2] "README › 4.2 Job identity" (677-694), 5: 1 Create account · 2 Project roles · 3 Input:
    Viewer · 4 Output: Creator · 5 Web unchanged.
  - [4.3] "README › 4.3 Create the job" (731-785), 9: 1 Deploy container · 2 Same image · 3 Name,
    1 task · 4 Command python · 5 Eleven arguments · 6 Three variables · 7 Timeout, retries ·
    8 Service account · 9 Create.
  - [4.4] "README › 4.4 Execute, collect" (826-852), 5: 1 Execute · 2 View logs · 3 Attempt folder ·
    4 Three files · 5 Download.
  - [4.5] "README › 4.5 From the terminal" (909-956), 4: 1 Bucket variables · 2 Upload passage ·
    3 Execute overrides · 4 Download results.
  - [4.6] "README › 4.6 The helper" (969-1016), 2: 1 Run helper · 2 Open results.
  - [CU] "README › Clean up" (1018-1028), 4: 1 Download results · 2 Delete services, job ·
    3 Buckets, accounts · 4 Function image.
  S01, S02, S16's lecture recap and test-yourself blocks have no tracker.
- `(extra)` after a command: not in the README. A small GREY tag `extra` (or a variant) sits beside
  the typed line, and the SAY says "extra" the first time each kind appears (S03: the clone's
  spelling and git log; S05: the local stand-in; S07: docker checks). Later extras are marked on
  screen and named briefly.
- `▶ your turn`: a YELLOW tag beside the command or form at a real checkpoint (about one per README
  subsection); the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every CONSOLE form, the hook's page and classmate
  laptop, the V-diagrams' pictures of cloud machinery and the task-log shape; `recorded · <source>`
  on every cloud success; `extra · local stand-in` on the function stand-in (dev/20–29,
  provider-timeout); `extra · Docker's analogue` on `laptop/45`; `erratum` on every README/slide
  slip (the SAY says "a small note" or "a small gap", never "erratum"); `at the time of recording`
  beside every version on first show; the GOLD `cost_tag()` at S04 (function + build + stored
  image), S08 (`translation-demo`), S10 (Gemini TTS per Play audio), S12 (two buckets, soft delete),
  S13 (retries 0, timeout 5 min), S14 (one execution) and S16's checklist card. No price anywhere:
  each cost tag says what bills, and "check the pricing page".
- `LECTURE 14 · a–b` in a SHOW line: from that block on, the GREY `lecture_ref(14, "a–b")` tag
  (`explainer.devops`) sits top right ("Lecture 14 · slides a–b"; "slide" for one), until a SHOW
  changes or removes it. Spans from SLIDES.md §1 as assigned in the BRIEF. Every lecture picture is
  our own redrawing in series colours with the slide's structure and terms: no slide image, QR
  code, logo, meme or screenshot; slide 10's colour code is not copied (both grid rows BLUE; a
  solid rack for a VM, a dashed outline for serverless).
- **The sandbox framing** (BRIEF, load-bearing): said once, in S03 (block 8). Afterwards every
  gcloud error is the lesson, every cloud success is `recorded` with its source, and the local
  function stand-in is always tagged. Never imply a failure surprised us; never claim a deploy, an
  IAM grant, a bucket, an execution or a download happened live.

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| your laptop, the browser, "you" the deployer, the local ADC file, the classmate's laptop | GREY |
| the cloud: Cloud Run (the function's service, `translation-demo`, the job), Cloud Build, Artifact Registry, both buckets, Agent Platform, the runtime service-account **badges**. A VM is a **solid** rack; a serverless instance a **dashed** outline that exists only while needed | BLUE |
| the image and its containers: `cgumb/ac215-translation-demo:…`, the image Cloud Build makes from `main.py`, an instance's inner box | TEAL |
| shared, project-wide or outside your control: project-level role chips (Agent Platform User, Service Usage Consumer), the default compute account, googletrans' unofficial public endpoint | ORANGE |
| what you own and pin: `main.py` + `requirements.txt` (`==3.10.2`, `==4.0.0rc1`), the `hello_http` name tag, `uv.lock` / `--frozen`, the image **digest**, the per-bucket grants (Viewer on input, Creator on output) | GREEN |
| tools: gcloud, docker, uv, functions-framework, gunicorn, the helper `run_job.py` | PURPLE |
| errors and "don't": the placeholder rejection, the sign-in error, `MissingTargetException`, the 500 timeout, 400 / 405 / 503, the one-chip error, exit 1 / 127, the job that runs into its timeout | RED |
| your turn, the README tracker, today's two grid cells, the ponder timer | YELLOW |
| money: Cloud Build, request-based billing, min instances, Gemini TTS calls, bucket storage and soft delete, the leftover function image, the clean-up card | GOLD |
| routes and addresses: URLs, the query string and its `?` / `&`, ports and `-p` doors, JSON POST arrows, `gs://` URIs, the argv conveyor | PINK |
| the past and the future (L1 VM, L2 container on a VM, L3 key file, L13 training job, L15 endpoints and pipelines) | GREY, dashed |

Argument chips are WHITE-outlined boxes; only their `gs://` values are PINK.

Running example
- **The laptop** (`laptop/`: a fresh Docker 29.8.2 engine standing in for Docker Desktop,
  linux/amd64, git 2.54.0): terminal title `laptop`, prompts `student@laptop:~$` (before the clone)
  and `student@laptop:~/serverless-deployment$`. A second terminal on the same laptop, titled
  `laptop · second tab`, holds the extras run while a server is in the foreground.
- **The dev shell** (`dev/`: Debian 12, Python 3.12.15, uv 0.13.7), drawn as the **same GREY
  laptop**, terminal title `laptop · dev shell`; prompts `student@laptop:~/serverless-deployment$`,
  `…/serverless-deployment/tutorial/app$` (S11) and `…/serverless-deployment/tutorial/function$`
  (the function stand-in, S05; `dev/21` runs from the repository root). Said once (S05): "a second
  terminal on the same laptop".
- **The gcloud terminal** (`gcloud/`: Google Cloud SDK 592.0.0, **no account signed in**), title
  `laptop · gcloud`, prompt `student@laptop:~/serverless-deployment$`. The S03 exports are drawn
  in this terminal: every README command that uses `$PROJECT_ID` and friends runs in the shell
  that ran them (S11's dev shell carries the chip "same terminal as your exports").
- **Placeholders, everywhere** (the README's own): `YOUR_PROJECT_ID`, `YOUR_INPUT_BUCKET` /
  `YOUR_OUTPUT_BUCKET`, `YOUR_GLOBALLY_UNIQUE_…`, `YOUR_GOOGLE_ACCOUNT_EMAIL`; the valid-format
  stand-in `your-project-id` only in `gcloud/18`–`20`, tagged `extra`. Emails as the README writes
  them. The function's URL is never invented: drawn `https://translate-function-…run.app` with the
  middle elided, tag `illustration`. The image name is typed verbatim; the SAY calls it "the
  tutorial's public image" and never reads its namespace.
- **Crops** (BRIEF): gunicorn timestamps and PIDs stay on screen but are never read aloud;
  `laptop/10`'s eleven layer lines show first, `…`, last; the helper's run ids get a GREY chip
  "yours will differ"; `dev/10`'s 41 `+` lines show the six direct pins only.

Length and parts: narration **4,297** words (`python -m explainer.script`, which counts SAY
words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm)
that is ≈24.7 min of narration, ≈30–32 min with typing, outputs, CONSOLE fills and five ponder
timers. Part 1 = S01–S08 (hand over code, hand over an image; ends on the public page with "Play
audio · enable in part 3" pulsing and the parked question). Part 2 = S09–S16 (identity and finite
work; ends on the last test-yourself card, then an empty frame). Per scene (BRIEF target · ±15 %
band):

| scene | words (BRIEF · band) | scene | words (BRIEF · band) |
| --- | --- | --- | --- |
| S01 Hook | 194 (210 · 179–242) | S09 RuntimeIdentity | 240 (250 · 213–288) |
| S02 FourWays | 228 (250 · 213–288) | S10 EnableSpeech | 273 (250 · 213–288) |
| S03 BeforeYouBegin | 247 (250 · 213–288) | S11 LocalDevelopment | 287 (260 · 221–299) |
| S04 WriteAFunction | 288 (280 · 238–322) | S12 JobAndBuckets | 240 (250 · 213–288) |
| S05 InsideTheFunction | 254 (280 · 238–322) | S13 CommandAndArgs | 318 (310 · 264–357) |
| S06 CallTheEndpoint | 281 (290 · 247–334) | S14 ExecuteAndCollect | 273 (250 · 213–288) |
| S07 RunTheImage | 324 (290 · 247–334) | S15 FromTheTerminal | 223 (260 · 221–299) |
| S08 DeployTheImage | 320 (290 · 247–334) | S16 CleanUpRecap | 307 (270 · 230–311) |
| **part 1** | **2,136** (2,140) | **part 2** | **2,161** (2,100) |

Every scene is inside its band (merge log: `build/review_merge_log.md`). Tight: S07 (324/334),
S16 (307/311), S15 (223, floor 221) and the total (4,297 of the series' 4,300
ceiling), so any later addition names its cut in the same scene. Re-run the counter after any edit.

Notes for scene authors
- Shared code (`scenes/common.py`, started from L11's): tracker factories `tracker_bb`,
  `tracker_11` … `tracker_46`, `tracker_cu` with the step lists above and a `gcloud alternative`
  caption variant; prompts `P_LAPTOP`, `P_REPO`, `P_APP`, `P_FUNC`; tags `your_turn`, `extra_tag`
  (+ `local stand-in`, `Docker's analogue` variants), `illustration_tag`, `recorded_tag(source)`,
  `cost_tag(text)` (GOLD), `erratum_tag`, `lecture_ref`; `console_form(title, rows)`;
  `chip_row(values)`; set pieces `DeployGrid` (V1), `InstanceStrip` (V2), `BuildLine` (V3),
  `QueryToArgs` (V4), `PortEnvelope` (V5), `IdentityDoors` (V6), `LifecycleStrips` (V7),
  `AttemptFolders` (V8). Never reuse a scene class name for a helper.
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1. For the multi-line commands listed under TERM, check
  how `capture()` splits command and output before picking, and assert the picked text.
- BRIEF corrections found while scripting: the slides name no Python runtime (SLIDES.md
  "Commands and code on the slides"); only the old README at `4eaf343` said 3.10, so S04 says "the
  older README said 3.10" (BRIEF S04 had "the slides and the old README"); `dev/10` lines 1–2
  are the two typed commands (`cd tutorial/app`, `uv sync --frozen`), so its output starts at
  line 3 (BRIEF said "lines 2-4");
  the provider-timeout 500 is in `dev/provider-timeout/28` (the `zh-cn` request), not `23`;
  `laptop/41`–`43` use `--text-file examples/passage.txt` (the image's copy) where the job uses
  `--input-uri`; `dev/18` types `cd ../..; pwd` (the `; pwd` is ours, GREY chip "extra: pwd").
- Lexicon (`explainer/lexicon.yaml`, block "# AC215 L14", added at the review merge): `"8086"`,
  `"9090"`, `"405"`, `"503"`, `section 3.3` / `Section 3.3`, `Bienvenido a AC215`, `Bonjour à tous`,
  `A M D 64`, `same digest` / `by digest` (noun stress; multi-word so other videos' "digest" keeps
  its cache). Existing and used: `AC215`, `ADC`, `IAM`, `gunicorn`, `main.py`, `"8080"`,
  `"0.0.0.0"`, `us-central1`, `"403"`, `"3.12"`, `"3.10"`. Checked fine without entries (spoken
  review): googletrans, mebibytes, Gemini, uv, 512, 41, 17, 1000, Z H dash C N.
- Subtitle display for the i18n stage (`en_display` in `i18n/zh/narration/*.yaml`; spoken review
  #21): hello underscore HTTP → `hello_http`; Z H dash C N → `zh-cn`; percent 20 → `%20`; run zero
  zero one / two → `run-001` / `run-002`; translated dot txt / speech dot wav / manifest dot json /
  passage dot txt → the file names; translation demo serve → `translation_demo serve`; dash m,
  translation demo, batch → `-m, translation_demo, batch`; no invoker IAM check →
  `--no-invoker-iam-check`; uv sync with frozen → `uv sync --frozen`; ENABLE SPEECH / GOOGLE CLOUD
  PROJECT / GOOGLE CLOUD LOCATION → the variable names; A M D 64 → `amd64`; Control C → `Ctrl+C`;
  gs prefix → `gs://` prefix. In zh all of these stay English (glossary rule).
- Chinese glossary heads-up: BRIEF "Notes" list; reuse `../ac215-l14-exam/i18n/zh/glossary.yaml`
  where it agrees.
- Never: a real-looking key, token, ADC file content or project id; the instructor's name (the SAY
  says "the course's recording" / "the README's recording"); a console screenshot or the README's
  GIFs; an invented URL, execution id, attempt id beyond `de2f41…`, price or free-tier number; a
  job drawn with a URL or a port; the web service drawn with a bucket; `dev/` results presented as
  the deployed function's; "serverless means no servers" or "a function has no container";
  "you only pay while code runs" without "request-based billing and minimum 0"; `laptop/45` called
  the Cloud Run error (it is Docker's analogue); building the repo-root `Dockerfile`; telling
  viewers to delete the shared public image or to set retries above 0.

---

## S01 · It works on localhost — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. A GREY laptop slides in; on its screen a schematic page (tag
`illustration`, drawn from `laptop/11`: title "Translate · AC215", two text boxes, two language
selectors, a Translate button, a grey disabled "Play audio · enable in part 3"). "Good afternoon
everyone" types into the left box, the right selector flips to `fr`, Translate pulses, and on
"Bonjour à tous" the right box fills with `Bonjour à tous` (the real answer of `laptop/21`). The
address bar reads `localhost:8086` in PINK.
SAY: Here is a translation page running on your laptop. Type good afternoon everyone, choose French, press Translate, and it answers: Bonjour à tous.

SHOW: A second GREY laptop slides in on the right, labelled "a classmate" (tag `illustration`).
`localhost:8086` types into its address bar; a PINK request arrow leaves it, curls back into the
same laptop, and finds an empty socket: a RED "nothing here". A README card (`README.md · lines
238–240`): "Sharing `localhost` does not make it available on another person's computer."
SAY: Now send the address to a classmate. On their laptop, localhost 8086 finds nothing, because localhost always means this machine, and nothing runs on theirs.

SHOW: The classmate laptop shrinks away. V2 `InstanceStrip` top row builds: a solid BLUE rack
labelled "VM · lecture 1" (GREY-dashed "L1" chip), a time axis running "evening → night →
morning" (no clock values), a GOLD meter rising at a constant rate. A few PINK request pulses near
the start; long empty stretches after them shade GOLD ("idle, still billed").
SAY: Lecture 1 gave one fix: rent a virtual machine. The page gets a public address, but the machine is billed all night, while nobody translates anything.

SHOW: The rack dims. A YELLOW question card settles centre: "Can this page have a public URL —
and cost nothing while nobody is using it?"
SAY: So here is today's question. Can this page have a public URL, and cost nothing while nobody is using it?

SHOW: LECTURE 14 · 8. The question card fades out upward (gone, not parked). V2's bottom row builds under the
rack row: same time axis; at the first PINK pulse a dashed BLUE outline with a TEAL box inside
blinks on, answers, and dissolves after the pulses stop; the GOLD meter under it moves only under
pulses. On "By the end", V2's two rows shrink left as one group, and on the right a preview
silhouette builds, GREY-dashed: a BLUE bucket → a TEAL box with no ear → a
second bucket receiving three small file icons and a receipt; a hard right edge "exit".
SAY: That is the promise of serverless. A copy of your app appears when a request arrives and disappears when the traffic stops. By the end, the same image also runs as a job. It takes a passage from a private bucket, speaks it in French, saves its files and exits.

SHOW: Clear to a checklist of four GREY chips, one per phrase: "your clone", "Docker", "gcloud",
"your project + billing".
SAY: To follow along, have your clone, Docker, the gcloud tool and your own project with billing ready.

SHOW: The chips fade. Top-left, a sample YELLOW `ReadmeTracker` ("README › 1.1 Create the function ·
step 1 of 6") fades in; beside a sample command a YELLOW `▶ your turn` tag pulses. On "console
steps first", a GREY chip with header `README.md · lines 19–21`: "console first · gcloud boxes =
alternatives". Everything fades; empty frame.
SAY: A tracker in the corner names the README step, and a yellow tag, your turn, means pause and run it. Follow the console steps first; the gcloud boxes are alternatives, not extra steps.

---

## S02 · One app, four ways to deploy it — `s02_map.py` · `FourWays`

SHOW: No tracker. LECTURE 14 · 5. Slide 5 redrawn small: a wide GREY arrow with three phase labels
"POC", "Prototype", "MVP", dashed boundaries; three thin bars under it ("Build better models", "ML
workflow", "Deployment, scaling & automation"); a dashed YELLOW box over the Prototype block with
the chip "you are here".
SAY: First, where this lecture sits: inside the prototype phase of the course project, where deployment begins.

SHOW: LECTURE 14 · 6. The roadmap slides up and away. Four tiles in a row (our shapes, series
colours, no icons from the slide): "1 Data Collector", "2 Data Processor", "3 Model Training", "4
Model Deploy". Ticks write into tiles 1–3; tile 4 pulses YELLOW. A small GREY card under it:
"Milestone 3: deploy your model or API using Cloud Functions or Cloud Run" (digest §7).
SAY: Of the Cheese App's four parts, three are done. Model deploy is left, and milestone 3 asks you to deploy your model or API with Cloud Functions or Cloud Run.

SHOW: LECTURE 14 · 8–9. The tiles fade. Three short GREY lines write in, one per phrase, each with a
tiny moving picture: "code runs only when needed" (a dashed instance blinking on and off), "no
servers to set up" (a struck-through rack), "expensive hardware only for the step that needs it"
(one step of three lighting GOLD).
SAY: The lecture's serverless: code runs only when needed, no servers to set up, and costly hardware only for the step that needs it.

SHOW: The three lines fade. Three braces on a timeline, alone: GREY-dashed "LAST WEEK · Vertex AI
training job (L13)", YELLOW "TODAY · Cloud Functions · Cloud Run", GREY-dashed "NEXT · Vertex AI
endpoint · pipelines (L15)".
SAY: Last week's Vertex AI training job was one case; today, functions and Cloud Run; next week, endpoints and pipelines.

SHOW: LECTURE 14 · 10. **V1 `DeployGrid` built.** Left: a GREEN code card "Simple Translate",
faded, labelled "lecture sketch", holding three comment lines only (`# set up the translator`,
`# translate`, `# return the text`). Four PINK arrows fan out from it and settle into a 2×2.
Columns (headers write in on "Across"): "a file · main.py" and "a container" (TEAL box). Rows (on
"Down"): "rented machine · dedicated hardware" (solid BLUE racks) and "serverless" (dashed BLUE
outlines). On "top row", the two rack cells tick in GREY-dashed, labelled "L1" and "L2"; on
"bottom", the two serverless cells glow YELLOW, chip "today".
SAY: Its map is one app, four ways to deploy it. Across, what you hand over, a code file or a container; down, where it runs, a rented machine or serverless. Lectures 1 and 2 filled the top row; today fills the bottom.

SHOW: The README's four-part table (README card, `README.md · lines 12–17`, columns "Part" and
"New idea" only) slides under the grid; its rows detach as four chips: "1 Deploy a function" drops
under the file cell; "2 Deploy a web app", "3 Add speech", "4 Run a job" stack under the
container cell; chip 4 gets a small "job" label.
SAY: The README's four parts sit in that bottom row. Part 1 hands over a file. Parts 2 to 4 hand over one image, first as a web service, then as a job.

SHOW: A README card (`README.md · lines 7–10`), "We are deploying the **application code around the
model**, not training or hosting the translation model ourselves." The phrase "application code
around the model" goes GREEN. Beside it, a tiny GREY-dashed "Cheese App backend" box with an
arrow to an ORANGE "model service" cloud.
SAY: And notice what we deploy. Not the translation model, which an outside service runs, but the application code around it. Your Cheese App backend will play that role.

SHOW: Two GREY note cards with tag `erratum`. Card 1: the course page's two links
`…#running-app-as-cloud-function` and `…#running-app-in-cloud-run`, each with a RED "no such
section today" and a GREEN arrow "start at the top · Part 1 = function · Parts 2–4 = Cloud Run".
Card 2: "course map pin `4eaf343` (2025)" struck GREY, and "README the link serves: `46cc62f` ·
2026-10-22" in GREEN. Fade out; the grid shrinks to a corner icon kept for later scenes; empty
frame.
SAY: Two small notes. The course page links to sections the rewritten README no longer has, so start at the top. And we follow the README the course link serves now, not the older commit in the course map.

---

## S03 · Before you begin: project, region, clone — `s03_setup.py` · `BeforeYouBegin`

SHOW: TRACKER [BB] 1 (tracker appears: "README › Before you begin", 5 dots). No lecture_ref
(README only). CONSOLE(project selector, README:28-31): a top bar with a project picker; two
fields side by side, "display name: My Course Project" and "project ID: `YOUR_PROJECT_ID`"; on
"the ID", the ID field rings YELLOW with the chip "no spaces · the command boxes need this one".
TRACKER [BB] 2: CONSOLE(README:32-34) a row of four GREY checks: "billing enabled", "create Cloud
Run resources", "create service accounts", "create buckets", and a GREY chip "restricted? ask
course staff first".
SAY: Before you begin. Select your course project and check its project ID, not just its display name; the command boxes need the ID. Confirm billing is on and that you may create these resources; if not, ask course staff first.

SHOW: TRACKER [BB] 3. CONSOLE(README:35-37): no map (the toolkit has no geography): a plain GREY
"regions" line with two pins, a solid BLUE `northamerica-northeast2 · Toronto` and a dashed BLUE
`us-central1 · speech model · part 3`. A GREY chip between them: "two different settings".
SAY: Choose a region: the README uses Toronto. The speech model later uses us-central1, a separate setting for part 3.

SHOW: The worksheet (README card, `README.md · lines 46–55`) breaks into seven name cards along the
bottom: `translate-function`, `translation-demo`, `translation-demo-runtime`, `translation-audio`,
`translation-audio-job` (BLUE cards; the two account cards carry a small badge outline) and two
blank BLUE bucket cards "you choose · part 4". The cards shrink into a strip that later scenes pull
from.
SAY: The worksheet names what you will create: the function, the web service, the job, two runtime accounts, and two buckets you name in part 4.

SHOW: TRACKER [BB] 4. Full-width terminal, title `laptop`, prompt `student@laptop:~$`. A README card
(`README.md · lines 38–39`): "Clone or download the repository …", GREY chip "the README spells no
command". It types `git clone https://github.com/dlops-io/serverless-deployment.git` (extra: its
spelling) → TERM(laptop/01: 2); `▶ your turn`. Then `cd serverless-deployment` → (no output);
prompt `student@laptop:~/serverless-deployment$`. TRACKER [BB] 4 · extra: it types
`git log -1 --format='%H %ci %s'` (extra) → TERM(laptop/02: 2), `46cc62fd8b1a…` and `2026-10-22`
YELLOW.
SAY: Step 4: clone the repository. The README says clone or download, so our git clone is extra, and so is the git log showing the commit we follow. Pause and clone it.

SHOW: TRACKER [BB] 4 · extra. It types `ls` (extra) → TERM(laptop/03: 2–12); lines 2 `Dockerfile`,
4 `cli.py`, 5 `docker-entrypoint.sh`, 6 `docker-shell.sh`, 9 `main.py`, 10 `pyproject.toml`, 12
`uv.lock` dim GREY with a tag
`erratum` and chip "2025 files · the README never uses them · don't build this Dockerfile"; line
11 `tutorial` YELLOW. Then `ls tutorial tutorial/function tutorial/app tutorial/app/translation_demo`
(extra) → TERM(laptop/04: 32–34, 13–21); `function/`'s two files GREEN with the chip "part 1",
`app/`'s `Dockerfile` and `translation_demo` TEAL with the chip "the image of parts 2–4".
SAY: An extra listing shows older files at the root, including main.py and a Dockerfile, which the README never uses; don't build them. Today's work sits under tutorial: function for part 1, app for the image.

SHOW: TRACKER [BB] 5. The terminal title changes to `laptop · gcloud`. A README card (`README.md ·
lines 66–72`, "Terminal setup — run once before using any gcloud command boxes"). TRACKER [BB] 5 ·
extra: it types `gcloud auth list` (extra) → TERM(gcloud/03: 3); line 3 GREY. Then it types
`gcloud auth login` (README:74) with no output panel; a GREY chip "browser sign-in · no output
shown". Beside it a GREY card "gcloud's own login" with a small PURPLE gcloud icon; a second,
outlined card "the app's identity · part 3" stays empty (README:86-87).
SAY: Then the terminal setup, starting with gcloud auth login, a browser sign-in; an extra auth list shows no accounts yet. It logs in the gcloud tool, not the app; the app's identity comes in part 3.

SHOW: TRACKER [BB] 5. Terminal `laptop · gcloud` (the shell every later gcloud box and S11's `uv run`
use), prompt `student@laptop:~/serverless-deployment$`. It types, with `type_time=0.5` each,
the seven README exports (README:75-81) as `laptop/05` lines 1–7 spell them, then
`echo "$WEB_EMAIL"; echo "$JOB_EMAIL"; echo "$IMAGE"` (extra) → TERM(laptop/05: 9–11). The
`${PROJECT_ID}` inside lines 6–7 and `YOUR_PROJECT_ID` inside the echoed emails link with a PINK
thread. `YOUR_PROJECT_ID` in line 1 pulses YELLOW with the chip "put your real project ID here".
`▶ your turn`.
SAY: Seven exports follow: project, region, image, two names and two account emails built from your project ID. Pause and run them with your real ID.

SHOW: The terminal shrinks to a 3-row strip at the bottom. A GREY card, centred: "This recording
machine: no Google account · no project". Three short lines write in under it, one per phrase:
"gcloud boxes → run to their first honest error", "console → drawn (`illustration`)", "cloud
results → quoted from the README's recording (`recorded`)". Fade out; empty frame.
SAY: About this recording: this machine has no Google account and no project. So every gcloud box runs until its first honest error, the console is drawn, and cloud results come from the README's own recording.

---

## S04 · Part 1: write a function — `s04_function.py` · `WriteAFunction`

SHOW: No tracker yet. LECTURE 14 · 11. Slide 11 in one picture: a small GREEN `main.py` page in a
dashed BLUE outline; three PINK lightning bolts strike it, labelled "file upload", "database
change", "HTTP request"; the first two go GREY-dashed and the third stays PINK with the chip
"today". A GOLD meter under it ticks only while a bolt is active; on "scales by itself" the
outline duplicates once.
SAY: Part 1: a function. The lecture calls it lightweight code that an event starts, like a file upload, a database change, or today, an HTTP request. It is billed while it runs and scales by itself.

SHOW: LECTURE 14 · 11–12. Slide 12's four steps as a GREY checklist: "open the console page",
"enable the APIs", "create a Python file", "deploy". A product-name card (tag `erratum`): "Cloud
Functions" (the lecture's name) → "Cloud Run functions (formerly Cloud Functions 2nd gen)"; a
GREY chip "the slide's link still lands here". Then a README card (`README.md · line 99`):
"open **Cloud Run → Services** and select **Write a function**".
SAY: Its four steps: open the console, enable the APIs, write a Python file, deploy. One name has changed: Cloud Functions are now Cloud Run functions, so the README starts at Cloud Run, Services, Write a function.

SHOW: TRACKER [1.1] 1 (tracker appears: "README › 1.1 Create the function", 6 dots). The checklist
shrinks to the right edge. CONSOLE(README:99-103): "Cloud Run → Services" with a **Write a
function** button that pulses (GREY chip "narrow window: under More actions", README:100-101), then
the form "Create service". TRACKER [1.1] 2: a GREY dialog
"Enable required APIs? · Enable" (README:102, chip "only if prompted"). TRACKER [1.1] 3: "Service
name" fills `translate-function` (the first worksheet card flies up from the strip into the field);
"Region" fills `northamerica-northeast2 (Toronto)`.
SAY: That opens Create service. Enable the APIs if it asks. Name the service translate-function and choose your region.

SHOW: TRACKER [1.1] 4: "Runtime" → **Python 3.12**; a GREY chip with tag `erratum`: "the older README
(`4eaf343`): Python 3.10 · the slides name no runtime". TRACKER [1.1] 5: "Authentication" → **Allow
public access**, a tiny GREY browser icon beside it ("anyone with the URL"); **Create**.
SAY: For the runtime, pick Python 3.12; the older README said 3.10. Choose Allow public access, so anyone with the URL may call it, then Create.

SHOW: TRACKER [1.1] 6: the form gives way to a schematic "Source" editor with two tabs, `main.py` and
`requirements.txt`, holding GREY sample lines ("sample code · replaced next"). `▶ your turn`. A GOLD
`cost_tag`: "billed as a Cloud Run service · every deploy runs a build · the build stores an image ·
check the pricing page".
SAY: Open the Source editor; pause and create yours. A gold tag: the function bills as a Cloud Run service, and every deploy runs a build.

SHOW: TRACKER [1.2] 1 (tracker 1.2 appears, 4 dots). A GREY chip "read-only? select Edit source"
(README:126). CODE(tutorial/function/main.py: 3–12) slides into the `main.py` tab. On "decorator", line 7 `@functions_framework.http` YELLOW; on "hello
underscore HTTP", line 8's `hello_http` GREEN; on "text, source and destination", lines 9–11 light
one by one, each default (`"Welcome to AC215"`, `"en"`, `"es"`) underlined GREY; line 12 stays
plain until the next block.
SAY: Replace main.py with the tutorial's handler. The decorator marks an HTTP function called hello underscore HTTP. It takes text, source and destination from the request, each with a default.

SHOW: LECTURE 14 · 10. The V1 grid's "lecture sketch" card fades in on the left, GREY, beside the code panel, its
three comment lines plus a GREY note "the slide calls `translate(text, src, dest)` by position".
A small GREY signature card under it (googletrans 4.0.0rc1, digest / SLIDES Conflict 3):
`translate(text, dest='en', src='auto')`; the second slot `dest` flashes RED under the sketch's
second argument, then line 12's keywords flash GREEN. Tag `erratum` on the sketch.
SAY: Beside it, the lecture's sketch passes source second, by position. In this library the second slot is the destination, so source and destination would swap; the handler passes them by name.

SHOW: TRACKER [1.2] 2. LECTURE 14 · 11–12. The sketch fades. CODE(tutorial/function/requirements.txt: 1–2) slides into
the `requirements.txt` tab; both `==` pins GREEN, chip "two exact versions". A GREY chip under
line 2: "newer googletrans: async · breaks this sync handler" (digest gotcha 2).
SAY: Replace the requirements file with two exact pins. The newer googletrans is asynchronous and would break this simple handler.

SHOW: TRACKER [1.2] 3. CONSOLE field "Function entry point" types `hello_http`; a GREEN name tag
lifts off the field, flies to line 8 of the code panel and clicks onto `def hello_http`. A README
card (`README.md · lines 150–151`): "This is the Python function the serving framework should call,
not the filename or service name." TRACKER [1.2] 4: **Save and redeploy** pulses; a GREY status
line "Waiting for the revision to become ready" (README:152). `▶ your turn`.
SAY: Set the Function entry point to hello underscore HTTP. In the README's words, it is the Python function the framework should call, not the file name or service name. Select Save and redeploy and wait for the revision. Pause and do it.

SHOW: LECTURE 14 · 11–12. Slide 12's checklist returns from the right edge; its third item "create a Python file" (tag
`erratum`) expands into three GREEN chips: `main.py`, `requirements.txt`, `entry point: hello_http`.
Fade out; empty frame.
SAY: So the slide's step, create a Python file, is the short version. The console wants the file, its dependencies and the name of the function to call.

---

## S05 · What runs your function? — `s05_build.py` · `InsideTheFunction`

SHOW: TRACKER [1.2] 4 (no step advances: "under the hood"). LECTURE 14 · 10–11. A GREY quote card
(slide 11): "without managing servers or containers" (tag `erratum`); on "you don't manage them",
the word "managing" underlines YELLOW; on "builds a container anyway", a TEAL box outline draws
itself behind the quote.
SAY: What runs your function? The lecture says you manage no servers or containers, and that is true: you don't manage them. But Google builds a container anyway.

SHOW: **V3 `BuildLine`.** Three GREEN inputs on the left: `main.py`, `requirements.txt`, a name tag
`entry point: hello_http`. They slide into a PURPLE box "Cloud Build" (inner labels "buildpacks ·
base python312": README:197 `--base-image=python312`, and `gcloud/06`'s help text for `--source`,
"otherwise it will use Google Cloud buildpacks"); on "once, at build time", a GREEN stamp "pip install · build
time, not per request". A TEAL image drops out onto a BLUE shelf "Artifact Registry"; an arrow
from the shelf starts a dashed BLUE instance labelled "revision". A small `recorded · function
GIF` chip: RECORDED(expected/part1-function-recorded.txt: 12) "Building source: Google assembles
the runnable image".
SAY: Save sends your three inputs to Cloud Build. It installs the requirements once, at build time, configures the Functions Framework, and publishes an image to Artifact Registry. Cloud Run starts a revision from that image.

SHOW: Zoom into the dashed instance: nested boxes, PURPLE "functions-framework" → "Flask app" →
"gunicorn" bound to a PINK ear `0.0.0.0:$PORT` (tag `illustration`). A PINK request enters the ear;
an arrow labelled by the GREEN name tag `hello_http` reaches into a GREEN `main.py` card, finds `def
hello_http`, and the answer flows back out.
SAY: In each instance, the Functions Framework runs a small Flask app under gunicorn, on every interface, at the port Cloud Run provides. On each request, it looks up your function by the entry point name and calls it.

SHOW: Pull back to the V1 grid (from the corner icon): the "file · serverless" cell's lid lifts and
reveals a TEAL box inside, chip "Google built one". A small GOLD chip on the Artifact Registry shelf:
"stays after you delete the service · clean up at the end".
SAY: So the lecture's file cell has a container inside. That is why there is an image to clean up at the end.

SHOW: TRACKER [1.2] 4 · extra · local stand-in. Full-width terminal, title `laptop · dev shell`
(chip "a second terminal on the same laptop"), prompt `student@laptop:~/serverless-deployment$`.
It types `cat tutorial/function/main.py; echo ---; cat tutorial/function/requirements.txt`
(extra) → TERM(dev/20: 8–9, …, 14–16). Then it types
`python3 -m venv ~/fn-venv && ~/fn-venv/bin/pip install -q -r tutorial/function/requirements.txt && ~/fn-venv/bin/pip list 2>/dev/null | grep -iE 'functions-framework|googletrans|flask|gunicorn|httpx'`
(extra; folds) → TERM(dev/21: 5–9); a GREY chip on the terminal title "functions-framework 3.10.2
· Flask 3.1.3 · gunicorn 26.2.0 · at the time of recording"; a GREEN chip "what the build installs".
SAY: This layer also runs on your laptop, as an extra local stand-in. The same two pins install the Functions Framework, Flask, gunicorn and googletrans, as the build does.

SHOW: It types `cd tutorial/function` (extra, no output); the prompt becomes
`student@laptop:~/serverless-deployment/tutorial/function$`. It types
`~/fn-venv/bin/functions-framework --target hello_http` (extra) and the terminal stays empty for
three seconds; a GREY chip "serving · no log line · log level: error". (The `^C` of dev/22: 2 is
shown at the end of S06, when the stand-in stops.)
SAY: Start it with target hello underscore HTTP, and it prints nothing while it serves. That silence is normal: the framework logs only errors.

SHOW: The terminal shrinks to a strip. V3 is shown static and un-run: the PURPLE Cloud Build box
dim, no stamp, no image on the shelf. The name tag reads `translate` in a plain WHITE outline.
Nothing moves except the timer.
PONDER(8 s, "You paste main.py but type translate\nas the entry point. Does the build fail?\nIf not, what fails, and where do you see it?")
SAY: You paste main.py but type translate as the entry point. Does the build fail? If not, what fails, and where would you see it?

SHOW: The card leaves. V3 runs: its build stage gets a GREEN tick "requirements installed". In the
starting instance, the `translate` arrow reaches into `main.py`, finds no such def, and snaps RED;
the revision box turns RED "revision not ready". A GREY chip "README:1038 lists entry point under
Function build fails". TRACKER [1.2] 4 ·
extra · local stand-in: in the strip it types `timeout 20 ~/fn-venv/bin/functions-framework --target
translate` (extra) → TERM(dev/29: 2, …, 28 wrap); `'translate'` and `'hello_http'` in line 28 RED
and GREEN.
SAY: Installing the requirements works; they are fine. But the deployment fails. When the new revision starts, the framework looks for the name: main.py should contain a function named translate, but it found hello underscore HTTP.

SHOW: A GREY chip on line 28: "on Cloud Run: `/workspace/main.py` · in the logs". A small GREY
"where do you look?" card appears with three slots; slot 1 fills: "the build and start-up logs"
(slots 2 and 3 stay empty for later). LECTURE 14 · 16 (slide 16: "limited control and
debugging"). Fade out; empty frame.
SAY: On Cloud Run, you find this in the logs, not in your code. That is the first of three places to look.

---

## S06 · Call it with a query string — `s06_endpoint.py` · `CallTheEndpoint`

SHOW: TRACKER [1.3] 1 (tracker appears: "README › 1.3 Call the endpoint", 5 dots). No lecture_ref
yet. CONSOLE(README:156-157): "service details" with a URL field `https://translate-function-…run.app`
(middle elided, tag `illustration`) and a copy icon that pulses; beside it a GREY-dashed "build
details" page with a RED "not here" chip.
SAY: Step 1: in service details, copy the URL near the top; the build page is not your app's address.

SHOW: TRACKER [1.3] 2. A browser bar (tag `illustration`) with the elided URL and no query string.
RECORDED(expected/part1-function-recorded.txt: 3) "Default request: English → Spanish (Bienvenido a
AC215)", tag `recorded · function GIF`. Below, a 3-row strip `laptop · second tab` (the stand-in
server holds the dev shell's foreground) tagged `extra · local stand-in`: TRACKER [1.3] 2 · extra · local stand-in; it types
`curl -s -w '\n[HTTP %{http_code}]\n' http://localhost:8080/` (extra) → TERM(dev/23: 2–3).
SAY: Step 2: open it with no arguments; the README's recording shows the default in Spanish: Bienvenido a AC215. Our local stand-in, the same handler under the same framework, agrees.

SHOW: TRACKER [1.3] 3. LECTURE 14 · 11 (the "HTTP request" trigger). **V4 `QueryToArgs`.** `?text=Good%20afternoon%20everyone&src=en&dest=fr`
(README:163) types after the URL in PINK. On "question mark", it splits at `?` (PINK hinge); on
"ampersands", at each `&`; on "percent 20", each `%20` melts into a space. Three key=value pairs fly
into CODE(tutorial/function/main.py: 9–12)'s lines 9–11; each default greys out as its key arrives.
SAY: Step 3: append the query string. The question mark begins it, ampersands split the pairs, and percent 20 is an encoded space. Each pair fills one line of the handler, and its default steps aside.

SHOW: RECORDED(expected/part1-function-recorded.txt: 5) "The translation request returned Bonjour à
tous", tag `recorded · README:182-183`. Strip, TRACKER [1.3] 3 · extra · local stand-in:
`curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=fr'` → TERM(dev/25:
2). TRACKER [1.3] 4: three quick lines, one per language, only the `dest=` value PINK:
`…&dest=el'` → TERM(dev/26: 2); `…&dest=hi'` → TERM(dev/27: 2); `…&dest=zh-cn'` → TERM(dev/28: 2)
(each typed in full as the capture's line 1 spells it; `el` at normal speed, `hi` and `zh-cn` with
`type_time=0.6`). `▶ your turn`. An ORANGE arrow from the
handler leaves a dashed "Google Cloud" outline toward an ORANGE cloud "googletrans' public
endpoint" and back with each answer.
SAY: The recording shows Bonjour à tous, and so does the stand-in. Step 4: try Greek, Hindi, or Z H dash C N for simplified Chinese. Pause and try a few.

SHOW: A README card (`README.md · lines 171–173`): "**Checkpoint:** the same endpoint accepts
different inputs without a redeploy. … The `src` and `dest` parameters identify languages, not cloud
regions." On "languages", a GREY chip `src=en` beside a struck-through BLUE region pin.
SAY: The checkpoint: one endpoint, different inputs, no redeploy; and source and destination are languages, not regions.

SHOW: TRACKER [1.3] 5. CONSOLE "Observability → Logs" (README:168-169): a log list with one row
lit; RECORDED(expected/part1-function-recorded.txt: 10) "Find the matching French query and verify
GET 200", tag `recorded · function GIF`. The where-to-look card from S05 returns small: slot 2
lights "the service logs".
SAY: Step 5: open Observability, Logs. The recording found its French request with status 200.

SHOW: TRACKER [1.3] 5 · extra · local stand-in. Strip `laptop · second tab`, a GREY chip "our first
recording run · kept on purpose" (`dev/provider-timeout/`): it types
`curl -s 'http://localhost:8080/?text=Good%20afternoon%20everyone&src=en&dest=zh-cn'` →
TERM(dev/provider-timeout/28: 2 wrap) RED. Then the client strip **Transforms** into the server
strip (never both at once): TERM(dev/provider-timeout/22: 2, …, 25–26, …, 82); line 25's
`main.py", line 12, in hello_http` YELLOW, with a mini `main.py` line 12 beside it as its target;
line 82's `ReadTimeout` RED. A GREEN chip "retried: `大家下午好`" (the re-run of the same `zh-cn`
request, dev/28: 2; the chip shows no file id).
SAY: While we recorded, the provider timed out once: the client got status 500, and the server log showed the timeout, raised from line 12 of main.py. A retry soon after worked.

SHOW: A README card (`README.md · lines 226–229`), "Provider failures and quotas can affect a demo;
inspect logs rather than treating a completed build as proof that translation worked." The ORANGE
arrow to googletrans' endpoint flashes; chips "unofficial", "not Google Cloud's API", "not yours ·
can rate-limit or change".
SAY: The README warns: the googletrans library wraps an unofficial outside service, so check the logs, not a finished build.

SHOW: TRACKER [1.3] 1 · gcloud alternative, caption "replaces 1.1–1.2" (the deploy box replaces the
console's create and supply steps). Full-width terminal, title `laptop · gcloud`, prompt
`student@laptop:~/serverless-deployment$`. A README card header "Equivalent gcloud commands —
deploy and call the function" (README:188-189). It types
`gcloud run deploy translate-function \ --project="$PROJECT_ID" --region="$REGION" \ --source=tutorial/function --function=hello_http --base-image=python312 \ --no-invoker-iam-check`
(README:195-198, four rows) → TERM(gcloud/05: 5–8) RED. Then (extra, GREY chip "a valid-format
stand-in, still a placeholder") `export PROJECT_ID=your-project-id` and the same four lines →
TERM(gcloud/18: 6–9) RED: `You do not currently have an active account selected.` … `gcloud auth
login`. A GREEN chip "`--function` = the entry point (gcloud help)". A GREY chip under the deploy
box (README:191-192): "first time: may ask to enable APIs or create a repository · answer y".
SAY: Now the gcloud alternative. In a new project it may first ask to enable APIs or create a repository; answer yes. With the placeholder, the deploy stops at the project ID check; with a real-format ID, it asks you to sign in first.

SHOW: It types `FUNCTION_URL=$(gcloud run services describe translate-function \ --project="$PROJECT_ID" --region="$REGION" --format='value(status.url)')`
(README:200-201) with no output panel; GREY chip "needs your project · stores the URL · no output".
The strip `laptop · second tab` (TRACKER [1.3] 3 · gcloud alternative · extra · local stand-in):
it types `FUNCTION_URL=http://localhost:8080` (extra, GREY chip "stand-in URL") and the README's
three curl lines verbatim (README:202-204) → TERM(dev/24: 5). V4 replays in reverse, small: the
three `--data-urlencode` values join into `?text=Good%20afternoon%20everyone&src=en&dest=fr`.
SAY: The next line stores the URL; the curl lines ran unchanged against the stand-in and answered Bonjour à tous.

SHOW: LECTURE 14 · 16 (cold starts). The dev shell's server terminal receives `^C` (TERM(dev/22: 2))
and the stand-in stops; it types `cd ../..` (extra, no output) and the prompt returns to
`student@laptop:~/serverless-deployment$`. A README card (`README.md · lines 218–223`, "More detail"): "A cold start initializes an instance of the
built application; it does not necessarily boot a new VM … There is no fixed inactivity interval to
rely on …". A tiny V2 preview: a dashed instance blinks on at a pulse after a gap, a small grey
puff "cold start". Fade out; empty frame.
SAY: From the README's More detail box: a cold start starts an instance of your app, not necessarily a new machine. No fixed idle time predicts it.

---

## S07 · Part 2: the prebuilt app on your laptop — `s07_local.py` · `RunTheImage`

SHOW: TRACKER [2.1] 1 (tracker appears: "README › 2.1 Try it locally", 4 dots). LECTURE 14 · 10, 14.
A README card (`README.md · lines 237–240`): "Now imagine you already have a working containerized web
app on your laptop. … Sharing `localhost` does not make it available on another person's
computer." The V1 grid icon lights its container cell.
SAY: Part 2. Now imagine a containerized web app already working on your laptop. Sharing localhost shares nothing, so we deploy that same image.

SHOW: Full-width terminal, title `laptop`, prompt `student@laptop:~/serverless-deployment$`. It types
`docker run --rm -p 8086:8080 \ cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`
(README:246-249, two rows) and `▶ your turn` appears beside it. On "remove when done", `--rm` rings
GREY; on "publish port", `-p 8086:8080` rings PINK and V5's door picture is drawn small beside the
terminal: a GREY laptop wall with a PINK door `8086` piped to a container ear `8080`.
SAY: Step 1, with Docker running: docker run, remove when done, publish port 8086 to 8080, and the tutorial's public image. Pause and run it.

SHOW: TERM(laptop/10: 3–5, …, 15–17); line 16 `Digest: sha256:c17b6db09f74…dbe72e` YELLOW; a README
card slides beside it (`README.md · line 1069`) with the same digest, and the two strings match
character by character, chip "same bytes, same digest". A GREY chip "linux/amd64 · Apple Silicon:
emulated · Cloud Run needs amd64" (digest §3.5).
SAY: The digest equals the README's: same bytes, same digest. The image is built for A M D 64, which Cloud Run needs; on Apple Silicon it runs under emulation.

SHOW: The terminal scrolls: TERM(laptop/10: 18–22). Line 19 `Listening at: http://0.0.0.0:8080 (1)`
PINK, a small GREY chip on it "every network interface"; line 22 `Control socket listening at …`
with a GREY chip "recent gunicorn (25.1 and later) · 26.2.0 at the time of recording" (on screen
only, not spoken); timestamps and PIDs stay unhighlighted.
SAY: Then gunicorn listens on 0.0.0.0, port 8080: every network interface, so connections from outside the container reach it.

SHOW: The terminal shrinks to a strip. **V5 `PortEnvelope`, part a.** TRACKER [2.1] 1 · extra: in a
strip `laptop · second tab`, it types the `docker image inspect --format 'Os/Arch: …'` command of
`laptop/16` lines 1–6 (extra; folds, small) → TERM(laptop/16: 11–12, 17). The two output lines
**Transform** into two slots over a TEAL image block: `ENTRYPOINT: []` (empty, GREY) and
`CMD: [python -m translation_demo serve]` (TEAL). On "arguments you pass", a GREY ghost chip "your
arguments" slides into the CMD slot, pushes the old CMD out, then reverts. A YELLOW chip "part 4" on
the pair. The strip fades.
SAY: How did Python turn into gunicorn? First, the image has two start-up slots: an empty entrypoint, and a command, translation demo serve. Docker runs the entrypoint, then the command, and arguments you pass replace the command; part 4 depends on this.

SHOW: **V5, part b.** The slots pair stays small at the top. The CMD starts a PURPLE "python"
process; CODE(tutorial/app/translation_demo/__main__.py: 22–26) beside it, line 23 (`PORT`) and
line 24 (`os.execvp("gunicorn", …`) YELLOW; on "replaces itself", the python process morphs into a
PURPLE "gunicorn" box (same outline, same place), which opens an envelope `PORT=8080` and grows a
PINK ear `0.0.0.0:8080`; line 25's `--workers 1 --threads 4` GREEN, four slots appear in the box.
SAY: That command takes its port from the PORT variable and replaces itself with gunicorn: 1 worker, 4 threads.

SHOW: TRACKER [2.1] 1 · extra. Strip `laptop · second tab`: `docker top $(docker ps -q) -o pid,user,args`
(extra) → TERM(laptop/13: 2, 3–4 from "{gunicorn}"), both rows' `{gunicorn}` YELLOW (no USER
chip). Then `docker ps --format 'table {{.Image}}\t{{.Command}}\t{{.Ports}}'`
(extra) → TERM(laptop/12: 2–3), `0.0.0.0:8086->8080/tcp` PINK; the door picture from block 2
returns. Then `curl -sS http://localhost:8080/` (extra) → TERM(laptop/14: 2) RED; a knock on the
wall at "8080" bounces.
SAY: Extra checks agree. Docker top shows only gunicorn, a master and a worker; no Python is left. Docker ps shows the door, 8086 outside and 8080 inside, so 8080 on the laptop is refused.

SHOW: TRACKER [2.1] 2. A browser (tag `illustration`) opens `http://localhost:8086` (README:251).
TRACKER [2.1] 2 · extra: strip `curl -s -i http://localhost:8086/ | grep -E 'HTTP/|Server:|Content-Type:|<title>|speech-button'`
(extra; folds) → TERM(laptop/11: 2–3, 5–6 wrap); `200 OK`, `Server: gunicorn`, the title and
`disabled … Play audio · enable in part 3` YELLOW; the drawn page shows the same disabled button.
SAY: Step 2: open localhost 8086. An extra curl shows status 200 from gunicorn, the title, and the disabled Play audio button.

SHOW: TRACKER [2.1] 3. The drawn page: text "Good afternoon everyone", `en` → `fr`, Translate. A PINK
JSON envelope `{text, src, dest}` flies from the page to the ear (CODE(tutorial/app/translation_demo/templates/index.html: 76–80)
small at the side, `method: 'POST'` and `JSON.stringify` PINK). TRACKER [2.1] 3 · extra: strip
`curl -s -w '\n[HTTP %{http_code}]\n' -X POST -H 'Content-Type: application/json' -d '{"text": "Good afternoon everyone", "src": "en", "dest": "fr"}' http://localhost:8086/api/translate`
(extra; folds) → TERM(laptop/21: 2, 4); `à` YELLOW with the chip "the browser shows: à"; the
page's right box fills `Bonjour à tous`. A GREY chip "captured during a second run of the same
command (laptop/20)". `▶ your turn`.
SAY: Step 3: translate. The button sends JSON in a post request and gets back Bonjour à tous, once the browser decodes that escape. Pause and try it.

SHOW: TRACKER [2.1] 3 · extra. V4's contrast: Part 1's query string flies at the app as a GET and
bounces RED: strip `curl -s -w '\n[HTTP %{http_code}]\n' 'http://localhost:8086/api/translate?text=Good%20afternoon%20everyone&src=en&dest=fr' | tail -3`
(extra) → TERM(laptop/26: 2, 4). Then the `dest: "xx"` request of `laptop/25` line 1 (extra) →
TERM(laptop/25: 2, 4), RED.
SAY: The query string from part 1 gets 405 here, method not allowed: this app wants JSON posts. A made-up language gets 400.

SHOW: TRACKER [2.1] 4. The page's "Play audio · enable in part 3" pulses GREY. TRACKER [2.1] 4 · extra:
strip, the `/api/speech` request of `laptop/24` line 1 (extra; folds) → TERM(laptop/24: 2, 4) RED.
Back in the main terminal, `^C` → TERM(laptop/10: 23–26); V5's gunicorn box receives a small
"SIGINT" arrow straight in (chip "main process · gets the signal") and folds away cleanly. `--rm`
sweeps the container away; the TEAL image stays on the shelf.
SAY: Step 4: Play audio is disabled, and its request gets 503: speech is disabled. Stop with Control C; gunicorn is the main process, so it shuts down cleanly.

SHOW: TRACKER [2.1] 4 · extra. A small strip: `docker run -d --name port-demo --rm -e PORT=9090 -p 8086:8080 cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`
(extra; folds) → (container id, not printed); `curl -sS http://localhost:8086/` → TERM(laptop/31: 2)
RED; `docker logs port-demo 2>&1 | head -4` → TERM(laptop/32: 3), `9090` YELLOW. V5: the ear moves to
9090 while the PINK pipe still ends at 8080.
SAY: One extra experiment: set PORT to 9090 but keep the pipe at 8080, and the connection resets; the log shows gunicorn on 9090.

SHOW: TRACKER [2.1] 4 · extra. `docker stop port-demo` (TERM(laptop/33: 2), `type_time=0.6`) and
the run with `-p 8086:9090` (laptop/34, line 1) → `curl -s http://localhost:8086/ | grep -o '<title>.*</title>'`
→ TERM(laptop/35: 2) GREEN; the pipe reattaches to the ear. A BLUE chip "Cloud Run: sets PORT and
knocks on it". `docker stop port-demo` (laptop/36, `type_time=0.6`). Fade out; empty frame.
SAY: Pipe to 9090 instead, and it answers. The right-hand number must be where the app listens.

---

## S08 · Deploy the same image — `s08_service.py` · `DeployTheImage`

SHOW: No tracker for this block. LECTURE 14 · 14–15. Slide 14 in one line (GREY card): "Cloud Run:
a whole container · as a service or a job · no server to manage". Slide 15's three steps as a GREY
checklist: "open Cloud Run", "enable the APIs", "deploy an image".
SAY: The lecture's Cloud Run runs a whole container, as a service or a job. Its steps: open Cloud Run, enable the APIs, deploy an image.

SHOW: TRACKER [2.2] 1 (tracker appears: "README › 2.2 Deploy the same image", 10 dots). CONSOLE
(README:272-280): "Cloud Run → Services → **Deploy container**"; "Create service"; the radio
"Deploy one revision from an existing container image" selected. TRACKER [2.2] 2: "Container image
URL" fills `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`; a PINK thread links it
to the same string in S07's `docker run` (a GREY ghost of the terminal line). TRACKER [2.2] 3:
"Service name" `translation-demo` (the worksheet card flies in), region Toronto.
SAY: Open Cloud Run, Services, Deploy container, and choose Deploy one revision from an existing container image. Paste the same image, name it translation-demo, and choose your region.

SHOW: TRACKER [2.2] 4: "Authentication" **Allow public access**; "Billing" **Request-based**.
TRACKER [2.2] 5: "Service scaling" **Auto scaling**, "Minimum number of instances" `0`, "Maximum
number of instances" `2` (README:281-283).
SAY: Select Allow public access and Request-based billing. Under scaling, minimum 0 instances and maximum 2.

SHOW: TRACKER [2.2] 6: "Containers, Networking, Security → Edit Container → Settings":
"Container port" `8080`, "Memory" `512 MiB`, "CPU" `1`, and a GREY note "leave the image's command
and arguments unchanged" (README:284-287). On "knocks on it", V5's envelope returns small: a BLUE
Cloud Run hand writes `PORT=8080` and knocks on the ear. TRACKER [2.2] 7: "Requests" → "Request
timeout" `120`, "Maximum concurrent requests per instance" `4` (README:288-290).
SAY: In the container settings: port 8080, 512 mebibytes, 1 CPU, and the command left alone; Cloud Run sets PORT and knocks on it. Then a 120 second timeout and 4 concurrent requests per instance.

SHOW: **V2 `InstanceStrip` with the numbers.** One dashed BLUE instance with a TEAL inner box and
four slots, labelled "4 threads (`__main__.py:25`) = concurrency 4" (a GREY chip "`--threads 4` in
the process list"). PINK pulses fill the slots; a second instance splits off; a hard YELLOW ceiling
line "max = 2" over the pair (no in-flight counter yet).
SAY: Why 4? Each instance runs gunicorn with 4 threads, so it never gets more than it can serve.

SHOW: V2's bottom row: the GOLD meter moves only under pulses; between bursts both instances
dissolve (chip "scale to zero"). A slider `min instances 0 → 1` moves: a faint instance stays lit
with its own GOLD drip (chip "joins the VM row"); then a toggle `Request-based → Instance-based`:
the meter runs for each instance's whole lifetime. Both reset to 0 / Request-based. A GOLD
`cost_tag`: "request-based + min 0: billed while serving · min ≥ 1 or instance-based: idle time
billed · check the pricing page". LECTURE 14 · 11, 14. A GREY quote (slides 11, 14, tag
`erratum`): "pay only when your code runs" + GREEN "with these two settings".
SAY: With request-based billing and a minimum of 0, the meter moves only while requests are served. That is the lecture's promise: pay only when your code runs. A minimum of 1, or instance-based billing, bills idle time too.

SHOW: Ten PINK request dots line up at the left edge, a YELLOW "Translate ×10" label.
PONDER(8 s, "Concurrency 4, max instances 2.\nTen people press Translate at once.\nHow many instances — and the last two?")
SAY: Concurrency 4, maximum 2 instances. Ten people press Translate at once. How many instances start, and what happens to the last two?

SHOW: The card leaves. The ten dots flow: two instances fill, 4 + 4 slots; on "with 8 slots", a
counter "8 in flight, at most"; the ceiling line glows;
two dots wait in a GREY queue, one of them flashes RED "may be refused". Three GREY fix chips: "raise
max instances" (GREEN tick), "raise concurrency + threads together" (GREEN tick), "raise min
instances" (RED cross, chip "warmth, not capacity").
SAY: Two instances, the ceiling, with 8 slots. The other two wait for a free slot and can be refused. Raise the maximum, or raise concurrency together with the threads; a higher minimum doesn't help.

SHOW: TRACKER [2.2] 8: **Create**; RECORDED panels one at a time, each replacing the last
(Transform), all tagged `recorded · container GIF`: (expected/part2-service-recorded.txt: 3)
"Creation completed: open the public service URL"; TRACKER [2.2] 9: (… : 4) "The public web app
returns Bonjour à tous; speech is still disabled"; TRACKER [2.2] 10: (… : 5–6) "Revision History … ·
POST /api/translate entry: HTTP status 200". On "A revision is", a small card "rev 1 · image +
settings" draws under a dashed instance (S10's "revision 2" replaces it), with a README card
(`README.md · lines 295–296`): "A revision is a deployed version of the service's image and
configuration." `▶ your turn`.
SAY: Select Create; the recording shows the public page answering Bonjour à tous, speech still disabled. Then check Revision History and Logs. A revision is a deployed version of the image and its settings. Pause and deploy yours.

SHOW: V1 grid: the "container · serverless" cell lights YELLOW, and V3's PURPLE Cloud Build box
appears GREY-dashed with a GREY cross: "no build this time" (README card, `README.md · lines
314–315`, "this deployment did not need to build our source").
SAY: Nothing was built this time.

SHOW: V1 and V3 fade. Two labels on the TEAL image: a movable sticky note
`:lecture14-agent-platform-20261022` ("tag") and an engraved serial number `@sha256:c17b…dbe72e`
("digest", GREEN). TRACKER [2.2] 10 · extra: a strip types
`docker image inspect --format '{{index .RepoDigests 0}}' cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`
(extra; folds) → TERM(laptop/15: 2) (no README card: S07 already matched the digest to README:1069).
Tag `erratum` on the console's image field: "a tag in the click path · deploy by digest to reproduce".
SAY: The console took a tag, a movable label; the revision keeps the digest, a fixed fingerprint. To reproduce a deployment later, deploy by digest.

SHOW: TRACKER [2.2] 8 · gcloud alternative. Terminal `laptop · gcloud` types
`gcloud run deploy "$WEB_SERVICE" \ --project="$PROJECT_ID" --region="$REGION" --image="$IMAGE" \ --no-invoker-iam-check --min-instances=0 --max-instances=2 \ --cpu=1 --memory=512Mi --concurrency=4 --timeout=120`
(README:321-324, four rows) with no output panel; the flags light in four groups as they type
(image · access · scaling · resources); GREY chip "needs your project · no output shown".
SAY: The gcloud alternative sets the same values in one command.

SHOW: The drawn public page (tag `illustration`, the same page as `laptop/11`) with an elided BLUE
URL `https://translation-demo-…run.app`; its "Play audio · enable in part 3" button pulses YELLOW.
A YELLOW parked-question card: "To speak, the app must call an API that asks who is calling. Who is
it?" Fade out; empty frame. (End of part 1.)
SAY: First half done: your laptop's page at a public URL. But Play audio still waits: to speak, the app must call an API that asks who is calling. Who is it?

---

## S09 · Who may call it, and who it runs as — `s09_identity.py` · `RuntimeIdentity`

SHOW: No tracker for this block; no lecture_ref in this scene (identity is tutorial-only, SLIDES
"What the slides leave to the tutorial"). A title card, README card (`README.md · lines 361–362`):
"Two permissions questions are separate: **who may call our public app**, and **what the running app
may access**." The parked question from S08 docks under it.
SAY: Part 3. The README separates two questions: who may call our public app, and what the running app may access.

SHOW: **V6 `IdentityDoors`.** A BLUE service box `translation-demo` with two doors. Left door, label
"who may call it": a GREY browser's PINK request passes, because a switch "Allow public access" is
on; a GREY chip `--no-invoker-iam-check` (`docs/lifecycle.md:78-79`). The switch flips off: the
request bounces RED `403`; a GREY chip "an organization policy can forbid public access". The
switch flips back on. The right door, "who it is when it calls out", stays empty and dim.
SAY: The first door, who may call it, is Allow public access; gcloud spells it no invoker IAM check. If an organization policy forbids it, the URL answers 403.

SHOW: A PINK arrow tries to leave through the right door toward a BLUE "Agent Platform" cloud.
PONDER(6 s, "The service allows public access.\nDoes that let it call Agent Platform?")
SAY: So, a quick test. The service allows public access. Does that let it call Agent Platform?

SHOW: The card leaves. The left door's switch stays on, irrelevant (GREY); the outbound arrow stops at
the empty right door, RED. A dashed ORANGE badge "default compute account" hangs on the right door,
GREY chip "normally, until you attach one".
SAY: No. That door only admits callers. Calling out goes through the other door, as whatever identity the service runs as; until you attach one, that is normally the project's default compute account.

SHOW: TRACKER [3.1] 1 (tracker appears: "README › 3.1 API and identity", 5 dots). CONSOLE
(README:366-367, 382-384): "APIs & Services → Library" → "Agent Platform API" → **Enable**, chip
"service ID `aiplatform.googleapis.com`"; a GREY chip "earlier lectures: Vertex AI".
SAY: Step 1: in the API Library, enable the Agent Platform API, the console's current name for what earlier lectures called Vertex AI.

SHOW: TRACKER [3.1] 2: CONSOLE "IAM & Admin → Service Accounts → Create service account" (README:368).
TRACKER [3.1] 3: "Service account name" `Translation demo runtime`, "Service account ID"
`translation-demo-runtime` (the worksheet card flies in), the email line
`translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com` (README:369-371). On V6, a BLUE
badge `translation-demo-runtime` forms.
SAY: Steps 2 and 3: create a service account named Translation demo runtime, with the ID translation-demo-runtime.

SHOW: TRACKER [3.1] 4: "Permissions (optional)": **Agent Platform User**, then **Add another role →
Service Usage Consumer** (README:374-379). On V6, two ORANGE chips hang from the badge: "Agent
Platform User · may call the model" and "Service Usage Consumer · may bill the quota project".
CODE(tutorial/app/translation_demo/speech.py: 102–105), line 104 `quota_project_id=project` YELLOW.
Then "Principals with access (optional)": both fields left empty; **Done**.
SAY: Step 4: two roles. Agent Platform User lets it call the model. Service Usage Consumer lets it charge calls to a quota project: the project whose quota and bill they count against. The app names your project there. Leave both principal fields empty and select Done.

SHOW: TRACKER [3.1] 5. The email copies to a GREY note. A README card (`README.md · line 380`):
"You do not need to create or download a key." On V6, a dashed GOLD key glyph crosses out; a
GREY-dashed callback card "L3 · `secrets/…json` key" slides in and is retired beside it.
RECORDED(expected/part3-speech-recorded.txt: 2) "Filtered result: runtime account Enabled, No keys",
tag `recorded · identity GIF`. `▶ your turn`.
SAY: Step 5: note the account's email. No key to create or download: in lecture 3 a JSON key sat in a secrets folder; here none exists. The recording shows the account enabled, with no keys; pause and create yours.

SHOW: TRACKER [3.1] 4 · gcloud alternative. Terminal `laptop · gcloud` types README:412-419 verbatim,
all eight rows, no `…`, `type_time=0.9` per command:
`gcloud services enable aiplatform.googleapis.com --project="$PROJECT_ID"`,
`gcloud iam service-accounts create translation-demo-runtime \ --project="$PROJECT_ID" --display-name='Translation demo runtime'`,
`gcloud projects add-iam-policy-binding "$PROJECT_ID" \ --member="serviceAccount:$WEB_EMAIL" --role=roles/aiplatform.user --condition=None`,
`gcloud projects add-iam-policy-binding "$PROJECT_ID" \ --member="serviceAccount:$WEB_EMAIL" \ --role=roles/serviceusage.serviceUsageConsumer --condition=None`
(each folded), no output panel; the two `projects add-iam-policy-binding` lines ring ORANGE with the chip
"project-wide". Fade out; empty frame.
SAY: The gcloud alternative enables the API, creates the account, and adds the two roles; both bindings are on the whole project.

---

## S10 · Attach the identity, turn on speech — `s10_speech.py` · `EnableSpeech`

SHOW: TRACKER [3.2] 1 (tracker appears: "README › 3.2 Attach and speak", 7 dots), step 1 not yet
lit (prerequisite). V6 returns: a thin GREY arrow from a GREY "you" figure to the badge, labelled
"Service Account User · `iam.serviceAccounts.actAs`" (README:432-434); a GREY chip "your deployment
right ≠ the badge's roles".
SAY: Attaching the account takes a permission of yours: Service Account User on that account. That is your deployment right, separate from the account's own roles.

SHOW: TRACKER [3.2] 1: CONSOLE "Cloud Run → Services → translation-demo" (README:436). TRACKER [3.2]
2: the **Security** tab; "Service account" selector → `translation-demo-runtime`; its email
`translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com` rings YELLOW against the S09 note
(README:437-439). On V6, the badge pins onto the right door.
SAY: Step 1: open translation-demo. Step 2: on the Security tab, choose your runtime account, and check its email.

SHOW: Beside the Security tab, a README card (`README.md · lines 378–379`), "We add your developer
access separately in section 3.3." (tag `erratum`); two GREEN chips only: "owner: already has it"
and "restricted: ask course staff".
SAY: A small gap: the README promises this access in section 3.3, but that section grants Token Creator instead. Project owners already have it; in a restricted project, ask course staff.

SHOW: TRACKER [3.2] 3: "Containers → Variables & Secrets → Environment variables": three rows fill
(README:444-448): `ENABLE_SPEECH` `true`; `GOOGLE_CLOUD_PROJECT` "Your project ID"; and
`GOOGLE_CLOUD_LOCATION` `us-central1`; a GREY chip "fill Name 1 / Value 1, then Add variable"
(README:441-442). On "two different settings", S03's dashed `us-central1` pin
reappears and connects to the third row; the solid Toronto pin stays on the service (README:495-498).
SAY: Step 3: three environment variables. ENABLE SPEECH, true; GOOGLE CLOUD PROJECT, your project ID; and GOOGLE CLOUD LOCATION, us-central1. The service runs in Toronto, the model in us-central1: two different settings.

SHOW: TRACKER [3.2] 4: **View diff & redeploy** → "Review changes to be deployed" (the three
variables GREEN), a CONSOLE row "Serve this revision immediately ✓ (leave on)" → **Deploy changes**
(README:450-452). TRACKER [3.2] 5 (on "wait for the rollout"): V2's instance dissolves and
a fresh dashed instance labelled "revision 2" takes its place, chip "replaced, not edited".
SAY: Step 4: View diff and redeploy, keep Serve this revision immediately on, then Deploy changes. That makes a new revision; the old instance is replaced, not edited. Step 5: wait for the rollout.

SHOW: The speech path, drawn left to right (tag `illustration`), no code panels: GREY browser → PINK
`POST /api/speech` → the instance; on the path three small gates light in order, labelled "flag",
"≤ 4,000 bytes" and "language" (`speech.py:75-82`); then the pinned badge hands back a short-lived
ticket (never a key), labelled "ADC" on "Application Default Credentials"; a PINK arrow to a BLUE
"Agent Platform · gemini-2.5-flash-tts · us-central1" (`speech.py:91-92`); a WAV icon flows
straight back to the browser. A GREY crossed-out bucket: "no bucket". Groups: the path, the badge
with its ticket, the crossed bucket.
SAY: Here is the speech path. The app checks the flag, the size and the language, then asks Google's auth library for a token; on Cloud Run, the badge supplies it. That lookup is Application Default Credentials. Gemini speech in us-central1 sends audio straight back; no bucket.

SHOW: TRACKER [3.2] 6. A GREY chip "the page checks the flag when it loads" with CODE(tutorial/app/
translation_demo/web.py: 13–15), `speech_enabled=enabled()` YELLOW. The drawn page reloads: the
button now reads "Play audio"; Translate, then Play audio. RECORDED(expected/part3-speech-recorded.txt:
12) "The player shows Pause: generated French audio is playing", tag `recorded · speech GIF`. A GOLD
`cost_tag`: "Gemini TTS · billed per Play audio · check the pricing page". `▶ your turn`.
SAY: Step 6: reload the page, because it checks the flag when it loads. Then Translate and Play audio; the recording shows French audio playing. A gold tag: each Play audio is a paid model call.

SHOW: TRACKER [3.2] 7. TERM(laptop/24: 2) returns small, GREY chip "captured in S07: the flag
missing". CODE(tutorial/app/translation_demo/speech.py: 108–119): line 109 ("Google credentials are
unavailable …") and line 113 ("Agent Platform access denied. Check the caller identity, enabled API,
inference permissions, and quota project.") YELLOW; a small mapping beside it: "no identity / 401 /
403 / 404 → 503", "429 / others → 502" (`web.py:50-53`). The where-to-look card's slot 2 glows.
SAY: Step 7: if it fails, check the message and the logs before changing permissions. Without the flag, you get our captured 503: speech is disabled. A missing identity or a denied call each has its own message.

SHOW: LECTURE 14 · 16. A GREY chip "limited control and debugging" over the mapping, then a GREEN
chip "the message names the badge or setting". TRACKER [3.2] 3 · gcloud alternative: terminal
`laptop · gcloud` types `gcloud run services update "$WEB_SERVICE" \ --project="$PROJECT_ID" --region="$REGION" \ --service-account="$WEB_EMAIL" \ --update-env-vars="ENABLE_SPEECH=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1"`
(README:489-492, four rows) with no output panel. Fade out; empty frame.
SAY: That is limited control and debugging, made workable. The gcloud alternative makes the same change in one command.

---

## S11 · Develop locally with ADC — `s11_localdev.py` · `LocalDevelopment`

SHOW: TRACKER [3.3] 1 (tracker appears: "README › 3.3 Develop locally · optional", 5 dots), step not
yet lit. No lecture_ref. A GREY chip "needs uv · docs.astral.sh/uv" (README:556). A README card (`README.md · lines 506–509`): "You should not need to publish an
image for every code edit. … **Application Default Credentials (ADC)** lets the same code discover
credentials locally and on Cloud Run." One line of code, `google.auth.default(…)` (from
CODE(tutorial/app/translation_demo/speech.py: 102)), sits between two arrows: up to a BLUE "Cloud
Run: the badge's token", down to a GREY "your laptop: an ADC file".
SAY: Section 3.3 is optional, and needs uv: how would you develop locally, without publishing an image for every edit? Application Default Credentials lets the same code find a token on Cloud Run and a file on your laptop.

SHOW: **V6 impersonation ribbon.** A GREY "you" figure signs in (a GREY card "your Google account");
a PINK ribbon runs from "you" to the BLUE `translation-demo-runtime` badge, labelled "Token Creator";
short-lived tickets flow back along it and drop a GREY "ADC file" on the GREY laptop disk. A dashed
GOLD key glyph crossed out: "no private key downloaded" (README:512-514). A GREY-dashed L3 card
"`secrets/` key file" slides in and greys out.
SAY: To test the runtime account's real permissions, your laptop impersonates it. You sign in as yourself and receive short-lived tokens as that account; no private key is ever downloaded.

SHOW: TRACKER [3.3] 1. CONSOLE (README:519-525): "IAM & Admin → Service Accounts →
translation-demo-runtime → Principals with access → Grant access"; "New principals"
`YOUR_GOOGLE_ACCOUNT_EMAIL`; "Role" **Service Account Token Creator**; a RED-struck chip "Service
Account Admin · don't leave it"; **Save**; then "APIs & Services → Library → IAM Service Account
Credentials API → Enable". RECORDED(expected/part3-speech-recorded.txt: 4) "Token Creator on this
account; inherited project roles", tag `recorded · impersonation GIF`.
SAY: Step 1: on the runtime account, grant your own user Service Account Token Creator. Replace any preselected role, and don't leave Service Account Admin. Enable the IAM Service Account Credentials API too.

SHOW: TRACKER [3.3] 1 · gcloud alternative. Terminal `laptop · gcloud` types README:541-545 verbatim,
all five rows, no `…`, `type_time=0.8` per command (folding):
`export DEVELOPER_EMAIL=YOUR_GOOGLE_ACCOUNT_EMAIL`,
`gcloud services enable iamcredentials.googleapis.com --project="$PROJECT_ID"`,
`gcloud iam service-accounts add-iam-policy-binding "$WEB_EMAIL" \ --project="$PROJECT_ID" --member="user:$DEVELOPER_EMAIL" \ --role=roles/iam.serviceAccountTokenCreator --condition=None`;
no output panel; the three are bracketed by a GREY chip "= step 1, as commands (README:538)".
SAY: Step 2 begins with three commands that repeat step 1 from the terminal; if you used the console, skip them.

SHOW: TRACKER [3.3] 2. The bracket fades. It types README:547-548 verbatim:
`gcloud auth application-default login --impersonate-service-account="$WEB_EMAIL"` and
`gcloud auth application-default set-quota-project "$PROJECT_ID"`; no output panel; GREY chip
"browser sign-in · no output shown". Two GREY cards side by side: "`gcloud auth login` → gcloud's
own login" and "`gcloud auth application-default login` → the app's ADC file" (README:86-87). They
give way to a README card (`README.md · lines 551–552`): "The ADC file stays on your machine; it
does not go into Git or the image." A GREY chip (README:552-554): "you also need to use the quota
project · restricted? Service Usage Consumer from course staff". `▶ your turn`.
SAY: Then two new ones: an application default login, impersonating the runtime account, and its quota project. It is separate from gcloud auth login, and its file stays on your machine, never in Git or the image. Pause and sign in; a restricted project may also need Service Usage Consumer for you.

SHOW: TRACKER [3.3] 3. Terminal `laptop · dev shell`, prompt `student@laptop:~/serverless-deployment$`.
It types `cd tutorial/app` and `uv sync --frozen` (README:559-560, as `dev/10` lines 1–2) →
TERM(dev/10: 3–4, …, 14, 23, 25, 27, 31, 32, 50); prompt becomes
`student@laptop:~/serverless-deployment/tutorial/app$`; `Installed 41 packages` YELLOW; the six
direct pins GREEN; a GREY chip on the title "Python 3.12.15 · uv 0.13.7 · at the time of recording".
A GREEN lock icon on `--frozen`: "install exactly the lock · never re-resolve" (L1 callback). TRACKER
[3.3] 3 · extra: `uv tree --depth 1` (extra) → TERM(dev/17: 3–9).
SAY: Step 3: change into the tutorial app folder, and run uv sync with frozen. It installs 41 packages exactly as the lock file says. An extra uv tree shows the six direct dependencies.

SHOW: TRACKER [3.3] 4. A GREY chip on the terminal title: "same terminal as your exports ·
`$PROJECT_ID` must be set". It types
`ENABLE_SPEECH=true GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \ GOOGLE_CLOUD_LOCATION=us-central1 PORT=8086 \ uv run python -m translation_demo serve`
(README:561-563, three rows) → TERM(dev/11: 4–8); line 5 `Listening at: http://0.0.0.0:8086` PINK.
V5's envelope: this time a GREY hand (you) writes `PORT=8086`. `▶ your turn`.
SAY: Step 4: in the terminal with your exports, start the app with the three variables and PORT set to 8086; this time you set the port. Pause, run it, then translate and Play audio at localhost 8086; with your sign-in, it speaks.

SHOW: TRACKER [3.3] 4 · extra. Strip `laptop · second tab`:
`curl -s http://localhost:8086/ | grep -E '<title>|speech-button'` (extra) → TERM(dev/12: 3 wrap),
`>Play audio<` GREEN (no "enable in part 3"); the translate request of `dev/13` line 1 (extra; folds)
→ TERM(dev/13: 2, 4); the speech request of `dev/14` line 1 (extra; folds) → TERM(dev/14: 2, 4) RED,
"Google credentials are unavailable …". On V6 the ADC file slot on the laptop disk is empty; GREY
chip "no sign-in on this recording machine = what skipping step 2 looks like". Then `^C` in the main
terminal → TERM(dev/11: 10–12).
SAY: Extra checks: the button now says Play audio, and translation works. Speech answers 503: Google credentials are unavailable. That is the missing sign-in, what you see if you skip step 2.

SHOW: TRACKER [3.3] 5. It types `cd ../..; pwd` (GREY chip "extra: pwd") → TERM(dev/18: 2); prompt
`student@laptop:~/serverless-deployment$`. A GREY chip, not typed: "the app guide's 17 offline
tests · exercises". Fade out; empty frame.
SAY: Step 5: go back up two levels to the repository root.

---

## S12 · Finite work: a job and two buckets — `s12_buckets.py` · `JobAndBuckets`

SHOW: No tracker for this block. LECTURE 14 · 14. A README card (`README.md · lines 582–585`): "…
The program should read its input, translate it, generate speech, save the files, and exit. That
is a **job** …". A GREY person waiting at a browser on the left; a sealed GREY envelope "audio
edition · collect later" on the right.
SAY: Part 4. A web request has a person waiting, but a translated audio edition should take its input, translate it, speak it, save the files and exit. That is a job.

SHOW: **V7 `LifecycleStrips`.** One TEAL image block; two startup commands hang under it, `serve`
and `batch` (CODE(tutorial/app/translation_demo/__main__.py: 12–13) small). Service strip: V2's
instance with its PINK ear, pulses answered, no right edge. Job strip: four segments "take input →
translate → speak → save" (`__main__.py:52-57`), a hard right edge "exit 0"; no ear, no URL. On V1,
the "container · serverless" cell splits into "service | job".
SAY: The lecture says a container runs as a service or as a job. Same image, two programs: serve keeps listening, with no end; batch walks four steps and exits.

SHOW: LECTURE 14 · 9. A GREY-dashed brace "LAST WEEK · Vertex AI training job (L13)" drops beside the
job strip; its own small strip (start → train → save → exit) matches the shape.
SAY: You have seen this shape before: last week's Vertex AI training job was finite work too: start, train, save, exit.

SHOW: The job strip's instance: no URL; when it exits, its little disk icon vanishes (chip "local
disk gone"). A BLUE input bucket on the left feeds a PINK `gs://…` arrow in; a BLUE output bucket on
the right receives files. A GREY laptop with `passage.txt` tries to hand it straight in and is
blocked: README card (`README.md · lines 918–919`), "a remote container cannot read a filename on
your laptop".
SAY: A job has no URL, and its disk vanishes when it exits. So input comes from Storage and results go back there; a remote container cannot see a file on your laptop.

SHOW: TRACKER [4.1] 1 (tracker appears: "README › 4.1 Two buckets", 6 dots). CONSOLE
(README:595-613): "Cloud Storage → Buckets → **Create**". TRACKER [4.1] 2: "Get started" name
`YOUR_GLOBALLY_UNIQUE_INPUT_BUCKET` with the hint "e.g. your project ID + `-translation-input`".
TRACKER [4.1] 3: the wizard sections write in one per phrase: "Region · northamerica-northeast2
(Toronto)", "Standard", "Enforce public access prevention ✓ · Uniform", "Soft delete: default
retention · no versioning"; **Create** → "Public access will be prevented · **Confirm**" → header
"Public access: Not public". `▶ your turn`.
SAY: Step 1: Cloud Storage, Buckets, Create. Step 2: a globally unique name, such as your project ID plus translation input. Step 3: region Toronto, class Standard, public access prevention, uniform access, default soft delete, then Create and Confirm. Pause and create it.

SHOW: TRACKER [4.1] 4: the form repeats quickly for `YOUR_GLOBALLY_UNIQUE_OUTPUT_BUCKET`; the two
blank worksheet bucket cards fill. A GOLD `cost_tag`: "two buckets · storage bills while files exist
· soft delete keeps deleted files for a while · check the pricing page".
SAY: Step 4: repeat for a separate output bucket. A gold tag: storage bills while files exist, and soft delete keeps deleted ones for a while.

SHOW: TRACKER [4.1] 5 · extra. Strip `laptop`: `cat tutorial/app/examples/passage.txt` (extra) →
TERM(laptop/40: 2–5). TRACKER [4.1] 5: CONSOLE "Objects → Create folder `run-001` → Upload → Upload
files → `passage.txt`" (README:615-618). TRACKER [4.1] 6: "Object details → Live object → Cloud
Storage URI" with a copy icon: `gs://YOUR_INPUT_BUCKET/run-001/passage.txt` in PINK (README:619-621).
`▶ your turn`.
SAY: Step 5: create a folder named run zero zero one in the input bucket and upload the sample passage, four short lines. Step 6: copy its Storage URI. Pause, upload and copy the URI.

SHOW: The URI splits into PINK segments; `run-001/` gets a GREY chip "a prefix you chose · not a
directory" (README:887-891). TRACKER [4.1] 4 · gcloud alternative: terminal `laptop · gcloud` types
README:661-672 verbatim, every row as the README spells it (the two `export … BUCKET=YOUR_GLOBALLY_UNIQUE_…`
lines, `gcloud services enable storage.googleapis.com …`, the two `gcloud storage buckets create …
--uniform-bucket-level-access --public-access-prevention` commands and the `gcloud storage cp
tutorial/app/examples/passage.txt …` command; the `…` here abbreviates this note only, never the
frame), folding, `type_time=0.8` per command, with no output panel. Fade out; empty frame.
SAY: That run zero zero one is a prefix you chose, not a real directory. The gcloud alternative makes both buckets and uploads the passage in one block.

---

## S13 · Command, arguments and the job's badge — `s13_job.py` · `CommandAndArgs`

SHOW: TRACKER [4.2] 1 (tracker appears: "README › 4.2 Job identity", 5 dots). LECTURE 14 · 14.
CONSOLE (README:679-682): "Create service account", ID `translation-audio-job` (worksheet card).
TRACKER [4.2] 2: the same two project roles. On V6, a second BLUE badge `translation-audio-job`
forms with the same two ORANGE chips.
SAY: Section 4.2: the job gets its own identity. Create translation-audio-job, give it the same two project roles, and note its email.

SHOW: TRACKER [4.2] 3: CONSOLE "input bucket → Permissions → Grant access": the job email, **Storage
Object Viewer**, **Save**; a GREEN chip "Viewer → input" hangs from the job badge, tied to the input
bucket only. TRACKER [4.2] 4: the same on the output bucket with **Storage Object Creator**; GREEN
chip "Creator → output". A GREY chip under Creator: "create · not list, open or overwrite" (digest
E3; `storage.py` only creates). TRACKER [4.2] 5: the web badge stays as it was, a GREY chip "no
bucket chip · its audio goes straight to the browser" (README:689-690).
SAY: Then, per bucket: Storage Object Viewer on the input, and Storage Object Creator on the output, which adds files but cannot list or overwrite them. The web account needs neither.

SHOW: A README card (`README.md · lines 692–694`), "**Checkpoint:** … Your own console/CLI identity
needs separate permission to upload passages, launch executions, and read results." A GREY "you"
figure gets three thin GREY arrows: "upload", "execute", "see results". `▶ your turn`.
SAY: Your own identity needs separate rights to upload, execute and see results. Pause and create the account and both grants.

SHOW: TRACKER [4.2] 2 · gcloud alternative. A strip `laptop · gcloud` types README:711-721 verbatim,
all eleven rows, no `…`, `type_time=0.9` per command (folding, small):
`gcloud iam service-accounts create translation-audio-job \ --project="$PROJECT_ID" --display-name='Translation audio job'`,
`gcloud projects add-iam-policy-binding "$PROJECT_ID" \ --member="serviceAccount:$JOB_EMAIL" --role=roles/aiplatform.user --condition=None`,
`gcloud projects add-iam-policy-binding "$PROJECT_ID" \ --member="serviceAccount:$JOB_EMAIL" \ --role=roles/serviceusage.serviceUsageConsumer --condition=None`,
`gcloud storage buckets add-iam-policy-binding "gs://$INPUT_BUCKET" \ --member="serviceAccount:$JOB_EMAIL" --role=roles/storage.objectViewer`,
`gcloud storage buckets add-iam-policy-binding "gs://$OUTPUT_BUCKET" \ --member="serviceAccount:$JOB_EMAIL" --role=roles/storage.objectCreator`;
no output panel.
SAY: The gcloud alternative creates the account and adds all four grants.

SHOW: TRACKER [4.3] 1 (tracker appears: "README › 4.3 Create the job", 9 dots). A GREY "you" arrow
to the job badge, "Service Account User" (README:733-735). CONSOLE
(README:737-745): "Cloud Run → Jobs → **Deploy container**" → page title "Create job". TRACKER [4.3]
2: the image URL `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` (PINK thread to
S08's field). TRACKER [4.3] 3: "Job name" `translation-audio`, region, "Number of tasks" `1`.
SAY: Section 4.3: attaching this account again takes your Service Account User on it. In Cloud Run, Jobs, Deploy container opens Create job. The same image, the name translation-audio, 1 task.

SHOW: TRACKER [4.3] 4: "Edit Container → Settings → Container command": `python` types, Enter, and
becomes a WHITE chip (README:746-748). **V7 command vs arguments:** over the TEAL image, the two
slots from S07 (`laptop/16:11-12`): `ENTRYPOINT: []` and `CMD: [python -m translation_demo serve]`.
The `python` chip drops into the empty ENTRYPOINT slot (GREY chip "gcloud help: --command =
Entrypoint for the container image", `gcloud/07:23`).
SAY: Container command: python, then Enter to make a chip. It fills the entrypoint slot, which this image left empty.

SHOW: TRACKER [4.3] 5: "Container arguments": the eleven values of README:755-765 type one at a time,
each followed by Enter, each becoming a WHITE chip (the two `gs://` values PINK, their bucket
placeholders YELLOW "replace with yours"). On the first argument chip, the old CMD lifts out of its
slot as one piece and fades GREY; the eleven chips then fill the slot one at a time. At the end,
ENTRYPOINT `python` and the CMD chips slide together into one argv conveyor (Transform): `python` `-m`
`translation_demo` `batch` `--input-uri` `gs://…/passage.txt` `--src` `en` `--dest` `fr`
`--output-uri` `gs://…/run-001/`. A GREY chip "no shell · one chip = one argv element" (README:750-753).
SAY: Container arguments: eleven values, each its own chip, and together they take the command slot's place. Dash m, translation demo, batch, input URI and your passage, source en, destination fr, output URI and your prefix. Each chip is one item of the argument list.

SHOW: TRACKER [4.3] 6: "Variables & Secrets": the same three rows as S10 (README:772-776), GREY chip
"select Done after all three" (README:770). TRACKER
[4.3] 7: "Task timeout" `5` "minute", "Number of retries per failed task" `0`, Memory 512 MiB, CPU 1,
tasks 1 (README:778-780); a GOLD `cost_tag`: "retries repeat paid work · keep 0 · a 5-min ceiling".
TRACKER [4.3] 8: **Security** → "Service account"
`translation-audio-job@YOUR_PROJECT_ID.iam.gserviceaccount.com`, chip "choose by email · the
selector shows the name". TRACKER [4.3] 9: "Execute job immediately" unchecked; **Create**. `▶ your turn`.
SAY: Then the same three variables, a task timeout of 5 minutes, and 0 retries, because a retry repeats paid work. On Security, choose the job's account by its email. Leave Execute job immediately unchecked, then select Create; pause and build it.

SHOW: TRACKER [4.3] 5 · extra. Strip: `laptop/44` line 1 (extra; folds) → TERM(laptop/44: 2,
from "(ModuleNotFoundError", wrap) RED. V7 replay: the eleven chips melt into **one** fat WHITE chip
after `python`; Python reads it as one argument starting with `-m`, whose module name is the rest:
`' translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage'`; the leading space
and the cut at the first dot (`passage|.txt`) ring RED. A README card (`README.md · lines 751–752`):
"Do not paste the whole block into one argument field."
SAY: Paste all eleven into one chip, and Python looks for a module with that whole sentence as its name. The name is cut at the first dot.

SHOW: V7 resets: `ENTRYPOINT: []` empty again, the eleven chips in the CMD slot, no `python` chip.
PONDER(8 s, "You fill all eleven argument chips\nbut leave Container command empty.\nWhat does the container try to run?")
SAY: Now the other mistake. You fill all eleven argument chips but leave Container command empty. What does the container try to run?

SHOW: The card leaves. With the ENTRYPOINT slot empty, the first chip `-m` slides into the program
position and turns RED. TRACKER [4.3] 4 · extra · Docker's analogue: strip `laptop/45` line 1 (extra;
folds) → TERM(laptop/45: 2, from "exec:", wrap) RED, chip "exit 127" (tag `extra · Docker's
analogue` — not Cloud Run's text).
SAY: The arguments replace the default command, and with no entrypoint, dash m becomes the program. Docker's version fails: executable not found.

SHOW: The strip fades. The third case, both slots at the image default: the job strip grows an ear,
never reaches its right edge, and runs into a RED wall "task timeout 5 min"; README card
(`README.md · line 1044`): "Job starts a server instead of finishing · Command `python` and
separate batch arguments".
SAY: With nothing changed, the job starts the web server and waits until the timeout fails it after 5 minutes.

SHOW: TRACKER [4.3] 9 · gcloud alternative. Terminal `laptop · gcloud` types README:816-821 verbatim,
all six rows, no `…`:
`gcloud run jobs create "$JOB_NAME" \ --project="$PROJECT_ID" --region="$REGION" --image="$IMAGE" \ --service-account="$JOB_EMAIL" --command=python \ --args="-m,translation_demo,batch,--input-uri,gs://$INPUT_BUCKET/run-001/passage.txt,--src,en,--dest,fr,--output-uri,gs://$OUTPUT_BUCKET/run-001/" \ --set-env-vars="ENABLE_SPEECH=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1" \ --tasks=1 --max-retries=0 --task-timeout=300 --memory=512Mi --cpu=1`
(folding) with no output panel; the `--args` value splits at its commas into the same eleven chips;
GREY chip "gcloud help: --command = Entrypoint" (`gcloud/07:23`). Fade out; empty frame.
SAY: The gcloud alternative passes the same eleven values, comma separated, with command python.

---

## S14 · Execute it and collect the files — `s14_execute.py` · `ExecuteAndCollect`

SHOW: TRACKER [4.4] 1 (tracker appears: "README › 4.4 Execute, collect", 5 dots). LECTURE 14 · 16.
CONSOLE (README:828-830): "Cloud Run → Jobs → translation-audio → **Execute**" (chip "narrow
toolbar: More actions ⋮"); "History" gets a row with a green check:
RECORDED(expected/part4-job-recorded.txt: 3) "History shows translation-audio-hq9f5 succeeded", tag
`recorded · README:859`. V7's job strip runs its four segments and hits "exit 0".
SAY: Section 4.4: open the job and select Execute. The recording shows it succeeding, with a green check in History.

SHOW: TRACKER [4.4] 1 · extra. Strip `laptop`: the batch of `laptop/42` lines 1–4 (extra; the image's
own `examples/passage.txt`, no speech flag) → TERM(laptop/42: 5) RED, chip "exit 1";
CODE(tutorial/app/translation_demo/__main__.py: 58–61) small, line 59 ("A failing job must exit
unsuccessfully so execution status is truthful.") YELLOW; V7's job strip's right edge flips to RED
"exit 1", then back to "exit 0".
SAY: What would a red mark mean? Our extra laptop run without the speech flag exits with status 1, an honest failure, so History tells the truth.

SHOW: TRACKER [4.4] 2: "execution → Tasks → View logs" (README:830-833); a log panel tagged
`illustration`: CODE-style quote of `expected/part4-task-log-shape.txt` lines 2–12 (placeholders in
angle brackets, chip "the shape · keys from `storage.py:48-56`"). A README card (`README.md · line
833`): "The job exits; it does not provide a web URL." V7's job strip shows no ear.
SAY: Step 2: open the execution, then Tasks, View logs. The job exits; it has no web URL. Its last output is a JSON summary with the output and manifest locations, status complete, and the files.

SHOW: TRACKER [4.4] 3. **V8 `AttemptFolders`.** The BLUE output bucket with a prefix tab `run-001/`
(chip "yours, from the arguments"); a folder drops in named `de2f41…/` (RECORDED(expected/part4-job-
recorded.txt: 5), tag `recorded · README:860`; no chip yet, the name is only "random").
TRACKER [4.4] 4: the README's table (README card, `README.md · lines 838–842`) and three file icons:
`translated.txt`, `speech.wav`, `manifest.json`.
SAY: Step 3: open your output bucket, then run zero zero one. Inside is a folder with a random name. Step 4: three files: translated dot txt, speech dot wav, and manifest dot json.

SHOW: V8 replays the arrival order: `translated.txt` and `speech.wav` land with GREEN stamps "create
only" (CODE(tutorial/app/translation_demo/storage.py: 41–55) small, line 46's
`if_generation_match=0` GREEN); `manifest.json` `"status": "complete"` lands **last** (lines 48–55),
a GREEN receipt ribbon on it.
SAY: The order matters. Each upload is create-only, and the manifest, saying complete, is written last. It is the receipt.

SHOW: V8 replay with a failure after the audio: two files, no receipt; the folder outline turns RED
"not a success". The where-to-look card returns: slot 3 fills "the job's logs and manifest". A README
card (`README.md · lines 893–895`): "Partial text/audio files without a completion manifest do not
establish success." A green check icon beside the receipt: "exit 0 ≠ work complete".
SAY: So, the third place to look. A green check says the process exited with 0; the manifest says the work is complete. Files without a manifest prove nothing.

SHOW: The bucket with one attempt folder.
PONDER(6 s, "Execute the same job again,\nsame arguments. Is the first\nresult overwritten?")
SAY: Execute the same job again, with the same arguments. Is the first result overwritten?

SHOW: The card leaves. A second folder with a different random name lands **beside** the first, chip
"a random UUID per attempt" (`storage.py:37-38`); the first stays untouched (a GREEN shield on its files, "create only"). A GOLD chip: "a retry =
paid work again · retries 0" (README:895-897).
SAY: No. A new attempt folder lands beside the first, and create-only uploads cannot overwrite. But it is not exactly once: a retry repeats paid work, which is why retries are 0.

SHOW: TRACKER [4.4] 5: CONSOLE object list with download icons (README:844-848); the text opens in a
GREY tab; the WAV in a media tab, "⋮ → Download". RECORDED(expected/part4-job-recorded.txt: 10) "The
text download opens the complete French translation". `▶ your turn`. A GOLD `cost_tag`: "one
execution = its task's running time + one TTS call · check the pricing page".
SAY: Step 5: download the text and the audio with the icons. Pause and run your job. A gold tag: each execution bills its running time plus one speech call.

SHOW: TRACKER [4.4] 1 · gcloud alternative. Terminal `laptop · gcloud` types README:872-876 verbatim:
`gcloud run jobs execute "$JOB_NAME" \ --project="$PROJECT_ID" --region="$REGION" --wait`,
`mkdir -p results`, `gcloud storage cp --recursive "gs://$OUTPUT_BUCKET/run-001" ./results \ --project="$PROJECT_ID"`,
with no output panel; `--wait` gets a GREY chip "waits · does not stream app logs" (README:879-880).
SAY: The gcloud alternative executes with wait, makes a results folder, and copies the output down. The wait flag does not stream your app's logs.

SHOW: A README card (`README.md · lines 850–852`): "**Checkpoint:** the task finished, the process
stopped, and its files remain in Storage." V7's job strip ends at its edge; V8's bucket keeps its
folders. Fade out; empty frame.
SAY: The README's checkpoint: the task finished, the process stopped, and its files remain in Storage.

---

## S15 · From the terminal, then the helper — `s15_terminal.py` · `FromTheTerminal`

SHOW: TRACKER [4.5] 1 (tracker appears: "README › 4.5 From the terminal", 4 dots), not yet lit. No
lecture_ref. A README card (`README.md · lines 911–914`): "Your signed-in user needs permission to
execute the job **with overrides** (`run.jobs.run` and `run.jobs.runWithOverrides`) …". On V6, a
thin GREY arrow from "you" to the job, labelled "run with overrides · yours", beside the job badge's
own chips ("not the badge's").
SAY: Section 4.5: new work from the terminal. First, a permission of yours: running a job with overrides needs its own right, separate from the job account's roles.

SHOW: TRACKER [4.5] 1. Terminal `laptop · gcloud`, prompt `student@laptop:~/serverless-deployment$`.
A GREY chip "console only so far? run Terminal setup first" (README:921-922). It types
`export INPUT_BUCKET=YOUR_INPUT_BUCKET` and `export OUTPUT_BUCKET=YOUR_OUTPUT_BUCKET`
(README:925-926). TRACKER [4.5] 2: a README card (`README.md · line 929`), "Save a new short UTF-8
passage as `passage.txt` on your laptop", GREY chip "short · under 5,000 characters" (README:900-901);
it types `cp tutorial/app/examples/passage.txt ./passage.txt` (tag `extra · or write your own`; the
capture's own step, `run_steps.sh:281`) → (no output); then
`gcloud storage cp ./passage.txt "gs://$INPUT_BUCKET/run-002/passage.txt" \ --project="$PROJECT_ID"`
(README:932-933) → TERM(gcloud/09: 5 wrap) RED.
SAY: Console only so far? Run the terminal setup first. Save a short passage, under 5,000 characters, as passage dot txt in the repository root, or copy the sample. Export both bucket names and upload it under run zero zero two; it stops at the placeholder again.

SHOW: TRACKER [4.5] 3. It types README:939-942 verbatim:
`gcloud run jobs execute "$JOB_NAME" \ --project="$PROJECT_ID" --region="$REGION" \ --args="-m,translation_demo,batch,--input-uri,gs://$INPUT_BUCKET/run-002/passage.txt,--src,en,--dest,es,--output-uri,gs://$OUTPUT_BUCKET/run-002/" \ --wait`
(folding) with no output panel. V7 replay: the whole row of eleven chips lifts out of the CMD slot
and a new row drops in; `run-002` and `es` YELLOW; the saved job card behind still shows `fr` and
`run-001` (README:953-956). In a ghost replay `--dest es` is removed: the saved card's `--dest fr`
chip tries to slide into the gap and is stopped by a RED bar "no merge"; a GREY chip from the program
fills it instead, "left out → the program's default (`--dest` = fr, `__main__.py:18`), not the job's
saved value" (gotcha 15; `gcloud/08`: "an execution will be created with the input values").
`▶ your turn`.
SAY: Step 3: execute the existing job with overrides. They replace the whole argument list for this execution only: a new path and Spanish. The saved job still says French, and a flag you leave out is not taken from it.

SHOW: TRACKER [4.5] 4. It types `mkdir -p results` and
`gcloud storage cp --recursive "gs://$OUTPUT_BUCKET/run-002" ./results \ --project="$PROJECT_ID"`
(README:948-950) with no output panel. RECORDED(expected/part4-job-recorded.txt: 12) "Upload the
passage / Execute the job with overrides / Download the results", tag `recorded · README:963-964
("successful Spanish job execution")`.
SAY: Step 4: after it succeeds, make the results folder and copy run zero zero two down. The README's recording shows a successful Spanish execution.

SHOW: TRACKER [4.6] 1 · extra (tracker appears: "README › 4.6 The helper", 2 dots). It types the
helper command of README:975-978 with `--dry-run` appended (`gcloud/11` lines 1–4; extra;
README:1000 names the option) → TERM(gcloud/11: 5 wrap, 6 wrap, 7, 8 wrap); the three `$ gcloud`
lines number 1, 2, 3 in PURPLE; the run id `run-20261104-093455-9d593d979e7f` GREY, chip "a UTC
timestamp + 12 random hex · yours will differ"; V8: a fresh prefix tab `run-<timestamp>-<hex>/`
appears in both buckets beside `run-001/` and `run-002/`.
SAY: Section 4.6: the helper combines all three. An extra dry run shows its plan. It uploads to a fresh run folder named by the time and a random part, executes with the eleven arguments, and downloads.

SHOW: TRACKER [4.6] 1. It types
`python tutorial/run_job.py ./passage.txt \ --project="$PROJECT_ID" --region="$REGION" --job="$JOB_NAME" \ --input-bucket="$INPUT_BUCKET" --output-bucket="$OUTPUT_BUCKET" \ --src=en --dest=fr --download-dir=./results`
(README:975-978) → TERM(gcloud/10: 5 wrap, 6, …, 14); line 5's leading `$ gcloud storage cp` PURPLE
("prints each command first"), the run id GREY chip "yours will differ", line 14 RED "Helper
stopped … Later steps were not run." A GREY chip with header `README.md · line 1002`: "bucket
**names**, without `gs://`" (the refusal is captured in `gcloud/13`, not shown). `▶ your turn`.
SAY: Run for real, it prints each gcloud command before running it and stops at the first failure. Pause and run it with your names.

SHOW: TRACKER [4.6] 2. RECORDED(expected/part4-job-recorded.txt: 13) "It prints Downloaded results
only after finding a complete manifest.", tag `recorded · README:992-993`; CODE(tutorial/run_job.py:
66–72) small, lines 67–72 YELLOW. V8's receipt ribbon flashes on a downloaded attempt folder and
`speech.wav` plays as a small waveform (tag `illustration`). A GREY chip (README:1006-1008): "the
helper needs Python + signed-in gcloud · the job gets ADC from its badge". Fade out; empty frame.
SAY: Step 2: open the result folder and play speech dot wav. The helper prints downloaded results only after it finds a complete manifest: the receipt again.

---

## S16 · Clean up, and what serverless costs — `s16_recap.py` · `CleanUpRecap`

SHOW: TRACKER [CU] 1 (tracker appears: "README › Clean up", 4 dots). No lecture_ref. A GOLD
checklist card (README:1020-1028), items writing in as the SAY reaches them: "1 download what you
want to keep" (ticks); TRACKER [CU] 2: "2 delete `translate-function`, `translation-demo`, then the
job `translation-audio`" (the worksheet cards fly in and dissolve one by one).
SAY: Clean up. Step 1: download what you want to keep. Step 2: delete translate-function and translation-demo, then the job.

SHOW: TRACKER [CU] 3: "3 delete the objects and buckets, then the two runtime accounts once
detached" (two bucket cards, then two badges, dissolve). TRACKER [CU] 4: "4 the function's image in
Artifact Registry": V3's Artifact Registry shelf returns with the function's TEAL image still on it,
GOLD tag "still billed as storage"; it is removed. `▶ your turn` beside the GOLD checklist.
SAY: Step 3: delete your buckets and the two runtime accounts once nothing uses them. Step 4: the function's image in Artifact Registry, still there after the service is gone. Pause and delete them all now.

SHOW: Three added GOLD lines under the card, tag `erratum` ("what the README's list leaves out"):
"soft-deleted files: recoverable and billable for the retention period" (`docs/lifecycle.md:176-177`);
"the build leaves source archives and logs" (`docs/lifecycle.md:205-210`); and a GREEN line "keep the
shared public image · others use it" (README:1027-1028). Under them, a GREY `extra` line, chips
only, not typed and not captured ("optional"): "on your laptop: `gcloud auth application-default
revoke` · `docker image rm cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` ·
`rm -rf ~/fn-venv`".
SAY: Three additions. Soft-deleted files stay billable for a while; the build also leaves source archives and logs. And keep the shared public image; others use it.

SHOW: TRACKER [CU] 4. A README card, small (`README.md · lines 1035–1046`, the Symptom | Check
table), GREY chip "stuck? start here". A second GREY chip, silent (README:1061-1064,
`docs/lifecycle.md:3-4`): "optional: a scripted separate practice stack · its own names · its clean
up removes only its own · `gcloud/20`". Fade out.
SAY: Stuck on a step? The README ends with a troubleshooting table of symptoms and checks.

SHOW: No tracker from here. The V1 grid returns complete. On "a file", the file cell's lid lifts on
its TEAL box and the Part 1 chip pulses. On "one image", the container cell's "service | job" halves
pulse in turn, each with a tiny icon: V2's dissolving instance, then V8's receipt.
SAY: Here is the whole map. Part 1 handed over a file, and Cloud Build made the image. Parts 2 to 4 handed over one image: a service that scales to zero, and a job that exits with a receipt.

SHOW: LECTURE 14 · 16. Slide 16's three cons hang under the serverless row as RED
cards: "cold starts", "limited control and debugging", "vendor lock-in". On "cold starts", its card
gets a GREEN answer chip "min instances ≥ 1 · warmth for money", with V2's always-on instance and
its GOLD drip.
SAY: Now the lecture's three downsides, and our answers. Cold starts: a minimum of 1 keeps an instance warm, for money.

SHOW: The second card gets its answer chip: the where-to-look card with all three slots lit, "build
and start-up logs · Part 1", "service logs · Parts 1, 3", "job logs + manifest · Part 4".
SAY: Limited control and debugging: three places to look, the build logs, the service logs, and the job's logs and manifest.

SHOW: The third card gets its answer: GREY laptop icons "functions-framework ran here" and "the image
ran here"; BLUE chips "console", "IAM", "Cloud Build" as "the Google-specific parts".
SAY: Vendor lock-in: the image and the Functions Framework ran on your laptop; only the console, the permissions and the build are Google's.

SHOW: LECTURE 14 · 9. Slide 9's braces return: the "NEXT" brace lights GREY-dashed "L15 · Vertex AI endpoint for a
trained model · pipelines"; the grid and cons shrink away.
SAY: Next lecture: a Vertex AI endpoint for a trained model, then pipelines.

SHOW: A YELLOW "Test yourself" card, question 1 of 5 (answers in `exercises.md`): "Place Parts 1 and
2 on the lecture's 2×2: what do you hand over, and who builds the image in each case?" A small V1
grid outline beside it, cells empty; on "hand over", the outline pulses once (cells stay empty).
SAY: Test yourself, pausing on each. One: place parts 1 and 2 on the lecture's map. What do you hand over, and who builds the image?

SHOW: Question 2 replaces it (a small V2 meter icon that ticks once on "meter"): "Which two settings make the meter run while
nobody is using the app, and what does min instances buy you?"
SAY: Two: which two settings make the meter run while nobody uses the app, and what does a minimum instance buy?

SHOW: Question 3 (a small two-door V6 icon; each door pulses once on its phrase): "Who may call it, and who it runs as: which setting
answers each, and why is no key file needed?"
SAY: Three: who may call it, and who it runs as. Which setting answers each, and why is no key file needed?

SHOW: Question 4 (a small chip row that pulses once on "eleven"): "Why does the job set a command and eleven separate arguments,
and what happens with neither?"
SAY: Four: why does the job set a command and eleven separate arguments, and what happens with neither?

SHOW: Question 5 (three small RED con cards, each pulsing once in turn): "Name the lecture's three downsides of serverless, and
what this tutorial gives you for each." A GREY chip "answers: exercises.md". Fade out; empty frame.
SAY: Five: name the lecture's three downsides of serverless, and what this tutorial gives you for each.
