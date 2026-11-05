# Brief · AC215 L14 — Serverless deployment: hand over the code, keep the answers

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture-slide digest and scene
map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides and the
captures disagree, the captures win.** The captures are newer (2026-11-04 09:24–09:35 UTC). They
were made by running the README's commands as written, in README order. Wherever a Google account,
a GCP project or a browser sign-in would be needed, the run stops at the honest, documented first
error, because this sandbox has none of them.

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**: every slide that the tutorial applies, and every README step of
all four parts, in order. The published exam edition `videos/ac215-l14-exam/` (concept-first, 15:20)
is a sibling. This video reuses its verified facts, its colour choices and its "do / don't say"
list, but it walks the README.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which README | `units.json` and the course map pin `4eaf343` (the old ~150-line README: Python 3.10, `functions-framework==3.*`, `dlops/simple-translate-http`). `SLIDES.md` was written against it | **`46cc62f`** (`main`, 2026-10-22). It was still `HEAD` on 2026-11-04 and is what the course link serves. Every capture's `02-git-log.txt` shows it, and the exam edition quotes it. **Decision (taken): follow `46cc62f`.** `4eaf343` appears only in one kind sentence (S02) and in `assets/source/at-4eaf343/` |
| the clone | digest Step 0 gives `git clone …` | README:38-39 says "Clone or download" and spells no command. The usual `git clone` is in `laptop/01` and is tagged `extra` for its spelling |
| `YOUR_PROJECT_ID` | digest assumes gcloud asks you to sign in | gcloud **rejects the placeholder first**: "must be a valid project ID, not the project name [YOUR_PROJECT_ID]" (`gcloud/05`, `09`, `10`). The sign-in error only comes with a valid-format stand-in (`gcloud/18`, `19`). `docs/lifecycle.md`'s own `--project=YOUR_PROJECT_ID` stops too (`gcloud/15`, `16`) |
| translation provider | README:228-231 warns that it can fail | **it failed once for real**: 1 of 7 function requests got a 500 with a `ReadTimeout` traceback (`dev/provider-timeout/`), and the retry succeeded. This becomes S06's "where do you look?" beat |
| one argument chip | digest gotcha 11: `No module named  translation_demo batch …` | the real text is `Error while finding module specification for ' translation_demo batch …' (ModuleNotFoundError: No module named ' translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage')`: a leading space, and the name is cut at the first dot (`laptop/44`) |
| arguments without a command | digest E2: "exact Cloud Run error text not recorded" | Docker's analogue, live: `exec: "-m": executable file not found in $PATH`, exit 127 (`laptop/45`). Tag it "Docker's analogue". The Cloud Run text stays unrecorded |
| gunicorn start-up | digest: four lines | 26.2.0 prints a **fifth** line, `Control socket listening at …`. Neither server logs requests. functions-framework prints **nothing** while it serves (`laptop/10`, `dev/11`, `dev/22`) |
| the process | digest: `os.execvp` replaces Python | confirmed: `docker top` lists two **gunicorn** processes (master and worker), not `python -m translation_demo` (`laptop/13`). The USER column reads `student` because the image's `app` user is UID 1000 (say it once) |
| entry point mismatch | digest: `File /workspace/main.py …` | the local stand-in says `File /home/student/serverless-deployment/tutorial/function/main.py is expected to contain a function named 'translate'. Found: 'hello_http' instead` (`dev/29`). On Cloud Run the path is the build's `/workspace/main.py` |
| function runtime | slides / old README: Python 3.10, `functions-framework==3.*` | Python **3.12**, `functions-framework==3.10.2` (README:104, `requirements.txt:1`) |
| length | digest §8: ~4,000 words | plan **~4,250 words ≈ 24.4 min narration**, ~30–32 min with typing, outputs and ponders |

## Audience and goal

An AC215 student who has done L1–L13:
- a GCP project with billing (L1);
- images, containers, `docker run -p` and `PORT` (L2–L4, `port_toy`);
- a service-account JSON key in `secrets/` (L3, L10);
- uv (L1);
- last week's Vertex AI training job (L13).

They have seen Lecture 14. They watch with their clone of
[dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment) open, Docker
running, gcloud installed and their own project selected, and they pause to run each step.
**This lecture creates billable cloud resources**: two Cloud Run services, a job, two buckets, an
Artifact Registry image and Gemini text-to-speech calls. GOLD tags mark each one, and the video ends
on the teardown checklist.

After the video they can:
- place the README's four parts on the lecture's 2×2 of deployment options: what you hand over (a
  file or a container) and where it runs (a VM or serverless);
- deploy the Part 1 handler as a Cloud Run function. They know the three things the console wants
  (`main.py`, `requirements.txt`, the **entry point** `hello_http`), what Cloud Build turns them
  into, and what a wrong entry point prints. They can call it with a query string;
- run the prebuilt image on their laptop, read every part of `docker run --rm -p 8086:8080 …`, and
  explain the container contract (`PORT`, `0.0.0.0`, one image whose `CMD` starts gunicorn);
- deploy the **same image** as a Cloud Run service. They can read min 0 / max 2 / concurrency 4
  against gunicorn's 4 threads, request-based billing, revisions, and a tag vs a digest;
- keep two questions apart: **who may call** the app (Allow public access) and **who the app runs
  as** (the attached runtime service account, no key). They know that attaching an account takes
  *their own* Service Account User, and they know impersonated ADC for local development;
- run the same image as a **job**. They can explain why the container command is `python` and why
  the eleven arguments are separate chips, and they know what a job that "never finishes" did
  wrong;
- prove success by finding a `manifest.json` (not a green badge), submit new work with `--args`
  overrides and the helper, and tear everything down, including what the README forgets.

## Length and parts

~30–32 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm). The plan below
totals **~4,250**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S08** (~2,150 words, ~15–16 min): **hand over code, hand over an image.** The
  hook, the lecture's map, before you begin, README Part 1 (the function: form, build, query
  string) and Part 2 (the image on your laptop, then the same image as a public service).
- **Part 2 = S09–S16** (~2,100 words, ~15–16 min): **identity and finite work.** README Part 3
  (the runtime identity, speech, local ADC), Part 4 (buckets, the job's own identity, command vs
  arguments, executions and their files, the terminal and the helper), clean-up, the lecture's
  three cons, and the recap.

The cut is the README's own seam between "public, anonymous, stateless" (Parts 1–2) and "the app
acts as someone and leaves files behind" (Parts 3–4). Part 1 ends on the **public URL serving the
same page your laptop served**, with cell 4 of the grid lit and one question parked for part 2.
The page's button still reads "Play audio · enable in part 3", so the question is: "to speak, the
app must call an API that wants to know *who is calling*. Who is it?"

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| your laptop, the browser, "you" the deployer, the local ADC file on your disk | GREY |
| the cloud: Cloud Run (the function's service, `translation-demo`, the job), Cloud Build, Artifact Registry, both buckets, Agent Platform, the runtime service-account **badges** (cloud principals). A VM is a **solid** rack; a serverless instance is a **dashed** outline that exists only while it is needed | BLUE |
| the image and its containers: `cgumb/ac215-translation-demo:…`, the image Cloud Build makes from `main.py`, an instance's inner box | TEAL |
| shared, project-wide or outside your control: the project-level role bindings (Agent Platform User, Service Usage Consumer on the *whole* project), the default compute account, googletrans' unofficial public endpoint | ORANGE |
| what you own and pin: `main.py` + `requirements.txt` (`==3.10.2`, `==4.0.0rc1`), the `hello_http` name tag, `uv.lock` / `--frozen`, the image **digest**, the per-bucket grants (Viewer on input, Creator on output) | GREEN |
| tools: gcloud, docker, uv, functions-framework, gunicorn, the helper `run_job.py` | PURPLE |
| errors and "don't": the placeholder rejection, the sign-in error, `MissingTargetException`, the 500 timeout, 400/405/503, the one-chip error, exit 1 / 127, the job that runs into its timeout | RED |
| your turn, the README tracker, today's two grid cells, the ponder timer | YELLOW |
| money: Cloud Build minutes, request-based billing, min instances, Gemini TTS calls, bucket storage (and soft delete), the leftover function image, the teardown card | GOLD |
| routes and addresses: URLs, the query string and its `?` / `&`, ports and `-p` doors, JSON POST arrows, `gs://` URIs, the argv conveyor | PINK |
| the past and the future (L1 VM, L2 container on a VM, L3 key file, L13 training job, L15 endpoints and pipelines) | GREY, dashed |

The lecture's own colour code on slide 10 (blue = dedicated hardware, green = serverless) is **not**
copied, because it would collide with the series' GREEN. Both grid rows are BLUE, since both are
cloud. The difference is the shape: a solid rack for a VM, a dashed instance for serverless (SLIDES
§5). Argument chips are WHITE-outlined boxes; only their `gs://` values are PINK.

## Running example

- **The laptop** (`laptop/`: a fresh `docker:29.8.2-dind` engine standing in for Docker Desktop,
  linux/amd64): user `student`, terminal title `laptop`, prompts `student@laptop:~$`, then
  `…:~/serverless-deployment$`. Say once: "on Apple Silicon this amd64 image runs under emulation;
  Cloud Run needs amd64 anyway" (digest §3.5).
- **The dev machine** (`dev/`: Debian 12, Python 3.12.15, uv 0.13.7) for Part 3.3 and the local
  function stand-in. It is drawn as the **same GREY laptop**, with the terminal title `laptop · dev
  shell`. Say once that it is a second terminal on the same laptop.
- **The gcloud terminal** (`gcloud/`: Google Cloud SDK 592.0.0, **no account signed in**), title
  `laptop · gcloud`.
- **The sandbox, honestly** (said once, in S03, then never apologised for). This recording machine
  has no Google account and no project:
  - every gcloud box runs until its **first honest error**, which is exactly what a student sees who
    forgets to replace `YOUR_PROJECT_ID` or to run `gcloud auth login`;
  - every console step is a schematic `illustration` with the README's own field values;
  - what only the cloud can show is tagged `recorded` and quoted from the README and its GIF
    captions (`expected/`);
  - Part 1's handler answers for real through the same functions-framework 3.10.2 that the build
    installs, tagged `extra · local stand-in`.
- **Placeholders, everywhere** (README's own): `YOUR_PROJECT_ID`, `YOUR_INPUT_BUCKET` /
  `YOUR_OUTPUT_BUCKET`, `YOUR_GLOBALLY_UNIQUE_…`, `YOUR_GOOGLE_ACCOUNT_EMAIL`; the valid-format
  stand-in `your-project-id` only in `gcloud/18-19`, tagged `extra`. Emails as the README writes them
  (`translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com`). The function URL is never
  invented: the console's URL field is drawn as `https://translate-function-…run.app`, with the
  middle elided, and is tagged `illustration`.
- **The image name** is typed verbatim wherever the README has it. The narration calls it "the
  tutorial's public image" and never reads out or explains its namespace.
- **Versions**, all "at the time of recording":
  - Docker 29.8.2, git 2.54.0;
  - image digest `sha256:c17b6db0…dbe72e`, which **equals README:1069** (say "same bytes, same
    digest" instead of a date);
  - Python 3.12.15, gunicorn 26.2.0, uv 0.13.7 (41 packages; flask 3.1.3, googletrans 4.0.0rc1,
    httpx 0.13.3);
  - functions-framework 3.10.2 (pinned by the README);
  - Google Cloud SDK 592.0.0.
- **Crops**: timestamps and PIDs in gunicorn lines stay (they are real), but are never read aloud;
  the eleven layer ids in `laptop/10:5-15` collapse to first, `…`, last; the helper's run ids
  (`run-20261104-093454-e2f3270ddd46`) are "yours will differ"; the 41 `+` lines of `dev/10` show
  first lines, `…`, the six direct dependencies highlighted.

## Visual set pieces (the 3Blue1Brown part)

Class names go in `scenes/common.py`. None collides with a scene class in `video.yaml`.

- **V1 · `DeployGrid` — the lecture's running map (slide 10; built S02, cell 3 S04/S05, cell 4
  S08, split S12, complete S16).** A GREEN code card on the left, "Simple Translate". This is a
  **faded "lecture sketch"** of slide 10's script: three comment lines (set up, translate, return),
  never the slide's positional call. Four PINK arrows fan out from it, then settle into a 2×2.
  - Rows: **VM / dedicated hardware** (solid BLUE racks) and **serverless** (dashed BLUE
    outlines).
  - Columns: **a file** (`main.py`) and **a container** (TEAL box).
  - The VM cells tick in GREY-dashed, labelled "L1" and "L2". The serverless cells glow YELLOW:
    "today". The README's four-part table (README:12-17) then slots in under the serverless row:
    Part 1 under the file cell, and Parts 2–4 under the container cell.
  - S05: the file cell's lid lifts, revealing a TEAL box inside ("Google built one", Conflict 2).
  - S12: the container cell splits into **service | job** (slide 14).
  - S16: the three cons (slide 16) hang under the serverless row, and each gets its answer chip.
- **V2 · `InstanceStrip` — scale to zero, scale out, cold start, the meter (S01 preview, S03
  concept, S08 numbers, S16 reprise).** A horizontal time axis with PINK request pulses.
  - Top row, the L1 VM: one solid rack and a GOLD meter rising at a constant rate, its idle
    stretches shaded.
  - Bottom row, serverless: a dashed TEAL-in-BLUE instance appears at the first pulse after
    silence. A small grey puff marks the **cold start**: container start → `serve` → gunicorn binds
    the port (`__main__.py:22-26`). The instance answers, then dissolves after the traffic stops
    (**scale to zero**). The GOLD meter moves only under the pulses (request-based).
  - A burst splits a second instance off (**scale out**). The `max = 2` ceiling is a hard line, and
    each instance shows **4 slots**, which are gunicorn's 4 threads (`__main__.py:25`, concurrency 4,
    README:289).
  - A `min instances` slider 0 → 1 lights a faint always-on instance with its own GOLD drip: it
    has joined the VM row (Conflict 4).
  - An `instance-based` toggle turns the meter on for an instance's whole lifetime.
  - No prices on the meter; it is a picture of *which* time is billed.
- **V3 · `BuildLine` — a function is a container you did not write (S05; callback S16).** Three
  GREEN inputs from the console form: `main.py`, `requirements.txt` and a name tag `entry point:
  hello_http`.
  - They slide into a PURPLE "Cloud Build" box (buildpacks, base `python312`, README:212-216):
    requirements installed **once, at build time**. A TEAL image drops onto a BLUE "Artifact
    Registry" shelf, and a revision starts from it.
  - Inside the dashed instance, PURPLE functions-framework → Flask → gunicorn on `0.0.0.0:$PORT`
    (`_cli.py:32-33`), and an arrow labelled by the **name** reaches into `main.py` and grabs
    `def hello_http`.
  - Replay with a tag reading `translate`: the arrow finds no such def and snaps RED,
    `MissingTargetException` (`dev/29:28`).
  - Coda: the same three steps on your laptop (`dev/20-22`) as a GREY mirror. "This layer travels
    with you", which is the honest half of the vendor-lock-in answer.
  - S16 callback: the image is still on the Artifact Registry shelf after the service is deleted,
    with a GOLD tag.
- **V4 · `QueryToArgs` — one URL, many inputs (S06; contrast in S07).** The URL
  `…/?text=Good%20afternoon%20everyone&src=en&dest=fr` types in.
  - It splits at `?` (PINK hinge) and at each `&`. `%20` melts into spaces.
  - Three key=value pairs fly into the three `request.args.get(...)` lines of `main.py:9-11`, and
    the defaults (`"Welcome to AC215"`, `"en"`, `"es"`) grey out wherever a key arrived. With no
    query string the defaults light up instead: Bienvenido a AC215 (`dev/23`).
  - Line 12's keyword call `translate(text, src=…, dest=…)` gets a GREEN highlight on the two
    keywords (Conflict 3: by name, because the library's second position is `dest`).
  - An ORANGE arrow leaves Google Cloud for googletrans' public endpoint and comes back with text.
  - S07 contrast: the web page sends the same three fields as a **JSON body** in a POST
    (`index.html:76-80`). The Part 1 query string sent to the web app bounces RED 405 (`laptop/26`).
- **V5 · `PortEnvelope` — the container contract (S07; reprise S08, S11).**
  - The image's `CMD [python -m translation_demo serve]` (`laptop/16:12`) starts a Python process.
    `os.execvp` **morphs** it into gunicorn, which takes its place, same PID (`__main__.py:24-26`;
    `laptop/13` shows only gunicorn, 1 master and 1 worker, 4 threads).
  - gunicorn opens an envelope `PORT=8080` (the image's `ENV`, `laptop/16:17`) and binds
    `0.0.0.0:8080`, an ear facing every interface.
  - The GREY laptop wall gets a PINK door `8086` piped to the container's `8080` (`-p 8086:8080`,
    `laptop/12`). Knocking on `localhost:8080` from the laptop is refused (`laptop/14`).
  - Extra (`laptop/30-36`): `-e PORT=9090` moves the ear, the pipe still ends at 8080, `curl` gets
    "Connection reset"; `-p 8086:9090` reconnects it.
  - S08: Cloud Run takes the place of `-p`: it sets `PORT` (README:285 "Container port `8080`") and
    knocks on it. Nobody answering means the revision never becomes ready.
- **V6 · `IdentityDoors` — who may call it, who it runs as (S09, S10, S11, S13).** A BLUE service
  box with two doors.
  - **Left door, "who may call it"**: a GREY browser's PINK request passes because *Allow public
    access* is set (gcloud: `--no-invoker-iam-check`). With it off, the request bounces RED 403.
  - **Right door, "who it is when it calls out"**: a BLUE badge `translation-demo-runtime` is
    pinned on the instance. Two ORANGE project-wide role chips hang from it: Agent Platform User
    ("may call the model") and Service Usage Consumer ("may bill the quota project",
    `speech.py:102-105`). Cloud Run hands the badge a short-lived token (a ticket, never a key),
    and the call goes on to Agent Platform in `us-central1`. A dashed GOLD key glyph is crossed
    out: "no key file" (README:380). That is L3's `secrets/` key, GREY-dashed, retired.
  - A third, thinner arrow from GREY "you" to the badge: *attaching* it takes **your** Service
    Account User (README:432-434).
  - S11: on the laptop, an **impersonation ribbon** runs from "you" to the same badge (Token
    Creator) and drops an ADC file on the GREY disk. `gcloud auth login` is drawn as a *different*
    GREY card, labelled "gcloud's own login".
  - S13: a second badge, `translation-audio-job`, carries the same two ORANGE chips plus two GREEN
    bucket-scoped chips (Viewer → input, Creator → output). The web badge gets no bucket chip
    (README:689-690).
- **V7 · `LifecycleStrips` — one image, two programs (S12, S13; S01 shadow).** One TEAL image block
  with two startup commands hanging under it, `serve` and `batch` (`__main__.py:1,12-13`).
  - *Service strip*: the V2 instance with its ear, answering pulses, no right edge.
  - *Job strip*: four segments (read → translate → speak → save, `__main__.py:52-57`), a hard
    right edge "exit 0", or a RED "exit 1" if any step fails (`:58-61`; `laptop/42`, `43`). No ear
    and no URL.
  - **Command vs arguments** (S13): two slots over the image, `ENTRYPOINT: []` (empty,
    `laptop/16:11`) and `CMD: [python -m translation_demo serve]`.
    - The console's **Container command** chip `python` drops into the ENTRYPOINT slot, and the
      eleven **argument** chips (README:755-765) replace CMD one by one. They lay out as an argv
      conveyor: `python` `-m` `translation_demo` `batch` `--input-uri` `gs://…` …
    - Failure replays, each from a real capture:
      - all eleven pasted into **one** chip: a single fat argv element, so Python looks for a
        module named `' translation_demo batch --input-uri gs://…/passage'` (`laptop/44`, RED);
      - arguments with **no command**: `-m` lands in the program slot (`laptop/45`, Docker's
        analogue, exit 127);
      - command and arguments left at the image default: the strip grows an ear, never reaches an
        edge, and runs into the RED "task timeout 5 min" wall (README:1044).
- **V8 · `AttemptFolders` — a result you can prove (S14, S15; P5).** The BLUE output bucket with a
  prefix tab `run-001/` (yours, chosen in the arguments).
  - Each execution drops a new folder named by a UUID (`storage.py:37-38`; recorded `de2f41…`).
  - `translated.txt` and `speech.wav` arrive with a GREEN "create only" stamp (`if_generation_match=0`).
  - `manifest.json` `"status": "complete"` arrives **last** as the receipt (`storage.py:48-55`).
  - A replay with a failure after the audio: two files, **no receipt**, so the folder is not a
    success (README:887-897).
  - A second execution lands **beside** the first and never on top of it.
  - S15: the helper's run prefix is `run-<UTC timestamp>-<12 hex>/` (`gcloud/11`), and its last
    line, "Downloaded results", only lights once it finds a receipt (README:992-993, `recorded`).

## README step tracker (ReadmeTracker, top-left)

One tracker per README subsection, titled with the README's own heading, so that "step k of N"
matches the numbered list a viewer scrolls past. README = `README.md` @ `46cc62f`. The gcloud boxes
are **alternatives, not extra steps** (README:19-21): when one is typed, the tracker stays on the
console step it replaces, with the caption `gcloud alternative`. Step titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **BB · Before you begin** | 26-89 | Select project · Billing, permissions · Choose region · Clone repo · Terminal setup (5) |
| **1.1 · Create the function** | 97-109 | Write a function · Enable APIs · Name, region · Python 3.12 · Public access · Source editor (6) |
| **1.2 · Supply the code** | 124-152 | Replace main.py · Replace requirements · Entry point · Save and redeploy (4) |
| **1.3 · Call the endpoint** | 154-173 | Copy URL · Default call · Query string · Other languages · Check logs (5) |
| **2.1 · Try it locally** | 242-268 | docker run · Open localhost · Translate · Ctrl+C (4) |
| **2.2 · Deploy the same image** | 270-296 | Deploy container · Image URL · Name, region · Public, request-based · Scaling 0–2 · Container settings · Request settings · Create · Open URL · Revisions, logs (10) |
| **3.1 · API and identity** | 364-380 | Enable API · Create account · Name and ID · Two roles · Record email (5) |
| **3.2 · Attach and speak** | 430-458 | Open service · Security tab · Three variables · View diff · Wait rollout · Play audio · Read logs (7) |
| **3.3 · Develop locally** | 504-578 | Token Creator · ADC login · uv sync · Run serve · cd ../.. (5) |
| **4.1 · Two buckets** | 593-621 | Create bucket · Unique name · Wizard settings · Output bucket · Upload passage · Copy URI (6) |
| **4.2 · Job identity** | 677-694 | Create account · Project roles · Input: Viewer · Output: Creator · Web unchanged (5) |
| **4.3 · Create the job** | 731-785 | Deploy container · Same image · Name, 1 task · Command python · Eleven arguments · Three variables · Timeout, retries · Service account · Create (9) |
| **4.4 · Execute, collect** | 826-852 | Execute · View logs · Attempt folder · Three files · Download (5) |
| **4.5 · From the terminal** | 909-956 | Bucket variables · Upload passage · Execute overrides · Download results (4) |
| **4.6 · The helper** | 969-1016 | Run helper · Open results (2) |
| **CU · Clean up** | 1018-1028 | Download results · Delete services, job · Buckets, accounts · Function image (4) |

Steps the README does not have are marked `extra` in the tracker caption and in the narration
("this one isn't in the README"). They include:
- `git log`, `ls`, the curl checks (`laptop/11-14`, `21-26`), `docker ps` / `top` / image digest
  and config (`12`, `13`, `15`, `16`);
- the PORT=9090 experiment (`30-36`), the local `batch` rehearsals (`41-47`);
- the function stand-in (`dev/20-29`, `extra · local stand-in`), the offline tests and plan
  (`dev/15-17`);
- `gcloud auth list` (`gcloud/03`), the valid-format stand-in runs (`gcloud/18-19`), the helper's
  `--dry-run` / `--help` / `gs://` check (`gcloud/11-13`, README:1000-1002 names the options), and
  the lifecycle plans (`gcloud/15-17`, `20-22`).

S01 and S02 are concept beats with no tracker. S16's lecture recap has none.

## Scene plan

Notation:
- `laptop/NN` = `assets/terminal/laptop/NN-*.txt`, and `dev/NN`, `gcloud/NN`, `expected/…`
  likewise. Line numbers are file lines: line 1 starts the `$` command and is typed, never printed;
  `[exit N]` is never printed.
- ▶ = a README step that the viewer must do, with a `your turn` tag at real checkpoints (about one
  per subsection).
- CODE(file: a-b) quotes `assets/source/` at `46cc62f` with real line numbers, ≤ 12 lines on
  screen. README excerpts are code panels of `README.md`.
- CONSOLE = a schematic console form, tagged `illustration`, with the README's field values. Never a
  screenshot, never a logo.
- `lecture_ref(14, "a–b")` per AC215_SERIES rule 9, with spans from SLIDES.md §1.

### Part 1 · Hand over code, hand over an image

**S01 · It works on localhost (~210 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
`lecture_ref(14, "8")` on the closing beat.
- The broken thing, as a picture. A GREY laptop shows a translation page (schematic, drawn from
  `laptop/11`: the title "Translate · AC215", a Translate button, the disabled "Play audio · enable
  in part 3"). It works: Bonjour à tous (`laptop/21`, real).
- A classmate on another laptop types the same address, `localhost:8086`. The PINK request curls
  back into *their own* machine: nothing there (no capture is claimed; it is a picture of what
  `localhost` means, README:238-240 "Sharing `localhost` does not make it available on another
  person's computer").
- Option 1 from L1: rent a VM (V2's top row). The app is public, but the GOLD meter climbs all
  night while nobody translates anything.
- The question on screen: *"Can this page have a public URL and cost nothing while nobody is using
  it?"*
- Teaser: the dashed instance of V2's bottom row blinks on at a request and dissolves after. "That
  is what serverless means. By the end of this video, the same image will also run as a job that
  reads a passage from a private bucket, speaks it in French and exits, leaving three files and a
  receipt."
- How to follow along: clone, Docker, gcloud, your own project with billing; sixteen small README
  trackers; `▶ your turn`; the study guide has every command. "Follow the console steps first; the
  gcloud boxes are alternatives" (README:19-21).

**S02 · One app, four ways to deploy it (~250) — `s02_map.py` · `FourWays`.** No tracker.
`lecture_ref(14, "5–10")`.
- Slide 5 redrawn small: POC → Prototype → MVP, with a dashed "you are here" box over Prototype.
- Slide 6's four Cheese App tiles: Collector, Processor and Training are ticked, and **Model
  Deploy** is the one left. Milestone 3 asks for exactly this: "deploy your model or API using
  Cloud Functions or Cloud Run" (digest §7).
- Slide 8 in one line: code runs only when needed; no servers to set up; expensive hardware only
  for the step that needs it.
- Slide 9 as three dashed braces: last week's Vertex AI training job (L13), **today** Cloud
  Functions and Cloud Run, next the Vertex AI endpoint and pipelines (L15). Serverless is one idea
  across three weeks.
- **V1 built**: one code card, four arrows, the 2×2. VM + file (L1) and VM + container (L2) tick
  in; today's two cells glow YELLOW. The README's four-part table (README:12-17) slides under the
  serverless row.
- The README's framing sentence (README:7-10): "we deploy the **application code around the
  model**", the same role the Cheese App backend will play.
- Errata, kindly, in two sentences:
  - the course page's two links point at section anchors that the rewritten README no longer has
    ("start at the top: Part 1 is the function, Parts 2–4 are Cloud Run", erratum 1);
  - the course map still names an older commit, and we follow the README the link serves today,
    `46cc62f`, rewritten on 2026-10-22 (erratum 3).

**S03 · Before you begin (~250) — `s03_setup.py` · `BeforeYouBegin`.** Tracker BB 1→5. No
lecture_ref (README only).
- ▶ BB1–3 as one CONSOLE strip:
  - the project selector, with **project ID vs display name** side by side (README:28-31): "the ID
    is the one with no spaces; the command boxes need it";
  - billing and permissions (README:32-34; "if your course project restricts these, ask course
    staff first");
  - region **Toronto `northamerica-northeast2`**, plus a dashed second pin, **`us-central1`**, for
    the speech model "in part 3". Two different settings (README:35-37).
- The worksheet table (README:46-55) as five name cards. They return in later scenes: the
  function's service, the web service, the web runtime account, the job, the job's runtime
  account. Two bucket cards stay blank until Part 4.
- ▶ BB4 Clone: `laptop/01` (tagged `extra` for its spelling, since the README says "clone or
  download"), extra `02` (`46cc62f`), extra `03` / `04`. Two observations:
  - the repo root still holds the 2025 files (`main.py`, `Dockerfile`, …), which the README never
    uses. "Everything today lives under `tutorial/`; don't build the root Dockerfile" (erratum 4);
  - `tutorial/function/` holds Part 1's two files; `tutorial/app/` holds the app inside the image.
- ▶ BB5 Terminal setup (README:73-82): `gcloud auth login` is typed with no output panel (a browser
  sign-in), plus the "before" picture, extra `gcloud/03` `No credentialed accounts.`. Then the seven
  exports, `laptop/05` verbatim (the echo shows the two emails and the image).
- One line: "this logs **gcloud** in. It is not the app's identity; that comes in part 3"
  (README:86-87).
- **The sandbox, said once**: no Google account here, so every gcloud box runs until its first
  honest error, the console is drawn, and cloud results are quoted from the README's own recording.
  Shown immediately: `gcloud/05:5` (the placeholder rejected). Surprise 1, kindly: "replace
  `YOUR_PROJECT_ID` with your real project ID. gcloud checks the format before it even asks who you
  are" (`gcloud/18:6` is that next error).

**S04 · Part 1: write a function (~280) — `s04_function.py` · `WriteAFunction`.** Tracker 1.1 1→6,
then 1.2 1→4. `lecture_ref(14, "11–12")`.
- Slide 11 in one picture: a function is lightweight code, **triggered by events** (a file upload,
  an HTTP request, a database change: three PINK lightning bolts; today only HTTP), billed while it
  runs, scaling by itself.
- Slide 12's four steps as a checklist that maps onto the README: open the console page, enable the
  APIs, create a Python file, deploy.
- **Conflict 1, said once**: the lecture says *Cloud Functions*; Google has moved it under Cloud Run
  as **Cloud Run functions** (formerly Cloud Functions 2nd gen). The slide's link still lands there.
  The README goes **Cloud Run → Services → Write a function** (README:99).
- ▶ CONSOLE 1.1: Write a function → Create service; "enable APIs if prompted"; name
  `translate-function` (the first worksheet card flies in); region; **Python 3.12** (note: "the
  slides and the old README said 3.10"); **Allow public access**; Create; the Source editor
  (README:99-109).
- GOLD tag: "a function is billed as a Cloud Run service; every deploy also runs a build".
- ▶ 1.2: CODE(`tutorial/function/main.py: 3-12`):
  - `@functions_framework.http`;
  - `def hello_http(request)`;
  - three `request.args.get` lines with defaults;
  - line 12's keyword call.

  CODE(`requirements.txt: 1-2`): two exact pins (GREEN): "two lines, two exact versions; the newer
  googletrans is async and would break this sync handler" (gotcha 2, one sentence).
- ▶ **Function entry point** = `hello_http`: a name tag flies from the form field to the `def` line
  and clicks. The README's own sentence: "the Python function the serving framework should call,
  not the filename or service name" (README:150-151).
- ▶ **Save and redeploy**; "wait for the revision to become ready". Conflict 5, kindly: "the
  slide's 'create a Python file' is the short version; the console wants the file, its
  dependencies, and the name of the function to call."
- The slide-10 sketch fades in beside the handler as a GREY "lecture sketch": "the lecture's sketch
  of the app; this is the handler you actually deploy" (Conflict 3).

**S05 · What runs your function? (~280) — `s05_build.py` · `InsideTheFunction`.** No tracker step
advances (1.2 step 4, "under the hood"). `lecture_ref(14, "10–11")`.
- **V3** in full: the build (README:212-216; recorded caption "Building source: Google assembles the
  runnable image", `expected/part1:12`) → Artifact Registry → revision → functions-framework →
  gunicorn on `0.0.0.0:$PORT` → the name lookup.
- **Conflict 2, said kindly**: slide 11's "without managing servers or containers" is true; you
  don't *manage* one. But Google builds one, and that is why there is an image to clean up at the
  end. V1's file cell lifts its lid: a TEAL box inside.
- The GREY mirror on your laptop, extra and tagged `local stand-in`:
  - `dev/20` (the two files);
  - `dev/21` (a venv with exactly the two pins installs functions-framework 3.10.2, Flask 3.1.3,
    gunicorn 26.2.0, googletrans 4.0.0rc1: "what the build installs");
  - `dev/22` (`functions-framework --target hello_http` prints **nothing** while it serves:
    surprise 6, "silence is normal here").
- **PONDER 1** (8 s), after the mirror. Answer:
  - the build succeeds, because the requirements are fine;
  - the framework fails when it starts and looks for the name: `dev/29:28`
    `MissingTargetException: … is expected to contain a function named 'translate'. Found:
    'hello_http' instead`, shown with the traceback cropped to first line, `…`, last line;
  - on Cloud Run the path reads `/workspace/main.py`, and you find it in the logs, not in your
    code. "The first of three places to look" (slide 16, limited control and debugging, gap 2).
- One sentence on lock-in (gap 6): functions-framework is open source and just ran on a laptop;
  the Google-specific part is the console and IAM around it.

**S06 · Call it with a query string (~290) — `s06_endpoint.py` · `CallTheEndpoint`.** Tracker 1.3
1→5. `lecture_ref(14, "11, 16")`.
- ▶ Copy the **URL** from **service details**, not the build page (README:156-157). CONSOLE with
  an elided `…run.app` URL.
- ▶ Default call: `recorded` "English → Spanish (Bienvenido a AC215)" (`expected/part1:3`). The same
  handler on the local stand-in: `dev/23` → Bienvenido a AC215.
- ▶ Query string: **V4**. `recorded` Bonjour à tous, then the stand-in `dev/25`. ▶ Other
  languages: `dev/26`–`28` (Greek, Hindi, `zh-cn` 大家下午好), one line each.
- The README checkpoint (README:171-173): same endpoint, different inputs, no redeploy; `src` and
  `dest` are languages, not regions.
- ▶ Check logs: `recorded` GET 200 (`expected/part1:9-10`).
- **Where do you look, beat 2**: the provider really timed out once while we recorded
  (`dev/provider-timeout/`). The client got `500 Internal Server Error`, and the server log shows
  `httpcore._exceptions.ReadTimeout` through `main.py:12`. The retry worked.
  - The README's own warning (README:228-231): "inspect logs rather than treating a completed build
    as proof that translation worked".
  - The ORANGE arrow to googletrans' unofficial endpoint flashes: "not Google Cloud's API, not
    yours; it can rate-limit or change."
- `gcloud alternative` (README:194-205), typed verbatim:
  - the deploy reaches `gcloud/05` (placeholder) and, with a real-format ID, `gcloud/18` (sign in);
  - `FUNCTION_URL=$(…describe…)` is typed with no output panel;
  - the `curl --get` lines run **verbatim** against the stand-in (`dev/24`) → Bonjour à tous. Say
    that `--data-urlencode` builds the same `%20` string that V4 just took apart.
- The "More detail" box in two sentences (README:218-224): a cold start starts *an instance of your
  built app*, not a new VM; there is no fixed idle interval to predict it. That links to V2 (S08).

**S07 · Part 2: the prebuilt app on your laptop (~290) — `s07_local.py` · `RunTheImage`.**
Tracker 2.1 1→4. `lecture_ref(14, "10, 14")`.
- README:237-240's framing: you already have a working containerized app; `localhost` is yours
  alone.
- ▶ `docker run --rm -p 8086:8080 \ cgumb/…` (README:246-249), verbatim → `laptop/10`:
  - `Unable to find image … locally`, then layers (first, `…`, last);
  - **`Digest: sha256:c17b6db0…`** (line 16): "same bytes as README line 1069";
  - the five gunicorn lines (18-22). Point at `Listening at: http://0.0.0.0:8080`; the fifth line
    is new in this gunicorn version.
- **V5**: `CMD` → `serve` → `os.execvp` → gunicorn. Extras: `laptop/16:11-12` (`Entrypoint: []`,
  `Cmd: [python -m translation_demo serve]`, "remember these two slots; they matter in part 4");
  `laptop/13` (gunicorn ×2, one worker × 4 threads; the USER column says `student` because both
  are UID 1000); the door `8086 → 8080` (`laptop/12`); `laptop/14` (8080 refused on the laptop:
  gotcha 5).
- ▶ Open localhost:8086: `laptop/11` (200, `Server: gunicorn`, the title, the disabled button).
- ▶ Translate: what the button sends, `laptop/21` → `{"dest":"fr","src":"en","text":"Bonjour à
  tous"}`, "the browser decodes that escape: Bonjour à tous". V4's contrast: the same fields as JSON
  in a POST; Part 1's query string here → **405** (`laptop/26`); a bad language → **400**
  (`laptop/25`).
- ▶ Play audio is disabled. What it would send: `laptop/24` → **503** "Speech is disabled. Enable
  it for part 3 …".
- ▶ Ctrl+C: `laptop/10:23-26`, a clean shutdown, because gunicorn is the container's main process
  and receives the signal.
- Extra, brief (`laptop/30-36`): `-e PORT=9090` → `Connection reset by peer` (`31`) while the log
  says 9090 (`32`); `-p 8086:9090` fixes it (`34`/`35`). "The right-hand number must be where the
  app listens; in the cloud, Cloud Run sets that number for you."

**S08 · Deploy the same image (~290) — `s08_service.py` · `DeployTheImage`.** Tracker 2.2 1→10.
`lecture_ref(14, "14–16")`.
- Slide 14 in one line (Cloud Run runs a whole container, as a service or a job, with no server to
  manage). Slide 15's three steps as the checklist: open Cloud Run, enable the APIs, deploy an
  image.
- ▶ CONSOLE 2.2, field by field (README:272-290):
  - Deploy container; **Deploy one revision from an existing container image**; the image URL, the
    same string as on the laptop;
  - `translation-demo` (worksheet card); region;
  - **Allow public access**, **Request-based**;
  - **Auto scaling, min `0`, max `2`**;
  - Container port `8080` (V5's envelope: "Cloud Run sets `PORT` and knocks"), 512 MiB, CPU 1,
    "leave command and arguments unchanged";
  - Request timeout `120`, **concurrency `4`**; Create.
- **V2 with the numbers**:
  - concurrency 4 = gunicorn's 4 threads (`__main__.py:25`, `laptop/13`), so Cloud Run never hands
    an instance more than it can serve;
  - max 2 → at most 8 in flight;
  - request-based + min 0 → the meter moves only under requests, which is the lecture's "pay only
    when your code runs" **with these two settings**;
  - min 1 / instance-based light the idle drip (Conflict 4).
  - GOLD tag.
- **PONDER 2** (8 s). Answer: 2 instances (the ceiling), 8 slots, so the other two wait for a free
  slot and can be refused. Raise max instances, or raise concurrency *together with* the threads.
  Min instances doesn't help (digest E6).
- ▶ Create → `recorded` "Creation completed: open the public service URL"; ▶ Open URL → "Bonjour à
  tous; speech is still disabled" (`expected/part2:3-4`). ▶ Revisions and logs: "A revision is a
  deployed version of the service's image and configuration" (README:295-296), `recorded` POST
  /api/translate 200.
- README checkpoint (314-315): "this deployment did not need to build our source". V1's container
  cell lights: no Cloud Build box this time.
- **Tag vs digest**: the console pasted a *tag*, a movable sticky note; the revision records the
  **digest**, the box's serial number (extra `laptop/15`; README:1066-1070). "For a deployment you
  must reproduce later, deploy by digest" (erratum 6, kindly).
- `gcloud alternative` (README:320-325): typed with no output panel.
- **End of part 1**: the public page, the same as `laptop/11`, with "Play audio · enable in part 3"
  pulsing. The parked question: "to speak, the app has to call an API that asks *who is calling*.
  Who is it?"

### Part 2 · Identity and finite work

**S09 · Who may call it, and who it runs as (~250) — `s09_identity.py` · `RuntimeIdentity`.**
Tracker 3.1 1→5. No lecture_ref (identity is tutorial-only, SLIDES "What the slides leave to the
tutorial").
- README:361-362, quoted as the scene's title card: "Two permissions questions are separate: who may
  call our public app, and what the running app may access."
- **V6**, left door first. *Allow public access* answers the first question; gcloud spells it
  `--no-invoker-iam-check` (`docs/lifecycle.md:78-79`). An org policy can forbid it, and then the
  URL answers 403 (gotcha 4).
- **PONDER 3** (6 s). Answer: no. That door only admits callers. Calling Agent Platform is the
  *right* door, and nothing is pinned there yet. Before Part 3 the service runs as the project's
  default compute account (digest open question: said as "normally", not as fact).
- ▶ CONSOLE 3.1 (README:366-380):
  - Agent Platform API, "the console's current name for what earlier lectures called Vertex AI";
    ID `aiplatform.googleapis.com`;
  - Create service account: name *Translation demo runtime*, ID `translation-demo-runtime` (the
    worksheet card), the email;
  - **Agent Platform User** + **Service Usage Consumer**, each with its one-line reason. The second
    exists because `speech.py:102-105` sends the project as the **quota project**;
  - leave both principal fields empty; Done;
  - "**You do not need to create or download a key**" (README:380), with V6's crossed-out key, and
    L3's `secrets/` key as a dashed callback.
- `recorded`: "runtime account Enabled, No keys" (`expected/part3:2`).
- `gcloud alternative` (README:411-420): typed with no output panel. ORANGE on the two `projects
  add-iam-policy-binding` lines ("project-wide").

**S10 · Attach the identity, turn on speech (~250) — `s10_speech.py` · `EnableSpeech`.** Tracker
3.2 1→7. `lecture_ref(14, "16")`.
- The prerequisite, before step 1: attaching takes **your** Service Account User on that account
  (README:432-434), V6's third arrow.
- Erratum 8, kindly: README:378-379 says "we add your developer access separately in 3.3", but 3.3
  grants Token Creator. Nothing grants Service Account User; project Owners already have it, and
  in a restricted project you ask course staff.
- ▶ CONSOLE 3.2:
  - Security tab → the runtime account (check its email);
  - Variables & Secrets → three rows: `ENABLE_SPEECH=true`, `GOOGLE_CLOUD_PROJECT`=your project ID,
    `GOOGLE_CLOUD_LOCATION=us-central1` (the dashed us-central1 pin from S03 now connects: region ≠
    model location, README:495-498);
  - **View diff & redeploy** → Deploy changes → a **new revision** (V2's instance is replaced, not
    edited).
- The speech path, drawn: browser → `POST /api/speech` → `synthesize()` checks `ENABLE_SPEECH`,
  then size, then language (`speech.py:75-82`) → ADC finds the badge's token (`speech.py:102-105`)
  → Agent Platform `gemini-2.5-flash-tts` in `us-central1` (CODE `speech.py: 91-92`, the URL
  template) → WAV back to the browser. **No bucket**.
- ▶ **Reload**, because the page reads the flag when it loads (`web.py:15`, gotcha 6). Translate →
  Play audio: `recorded` "The player shows Pause: generated French audio is playing"
  (`expected/part3:12`).
- GOLD tag: Gemini TTS per request.
- ▶ Read logs (README:457-458). The failure side is real: `laptop/24` (speech disabled → 503) is
  what you get with the flag missing. The app's own messages map to causes (`speech.py:108-119`):
  no identity / 401 / 403 / 404 → 503 "Agent Platform access denied. Check the caller identity,
  enabled API, inference permissions, and quota project.", and 429 / others → 502.
- Slide 16's *limited control and debugging*: "the message tells you which badge or setting to
  check. Read it before you change permissions."
- `gcloud alternative` (README:488-493): typed with no output panel.

**S11 · Develop locally with ADC (~260) — `s11_localdev.py` · `LocalDevelopment`.** Tracker 3.3
1→5. No lecture_ref.
- Why (README:506-509): edit and test against the real API without publishing an image per edit.
- **ADC** in one picture: the same `google.auth.default()` line finds the badge's token on Cloud Run
  and a file on your laptop (README:508-509).
- **V6 impersonation ribbon**: you sign in as yourself and receive short-lived tokens *as* the
  runtime account; no private key is downloaded (README:512-514).
- Callback, L3: then a JSON key in `secrets/`; now no key exists at all.
- ▶ Token Creator grant, CONSOLE (README:519-525): "replace any preselected role; don't leave
  Service Account Admin". Plus the IAM Service Account Credentials API.
- ▶ ADC login: the five commands (README:540-549), typed with no output panel (browser sign-in).
  - `gcloud auth login` ≠ `gcloud auth application-default login`: two GREY cards, two files
    (README:86-87, gotcha 9).
  - "The ADC file stays on your machine: not in Git, not in the image" (README:551-552).
- ▶ `cd tutorial/app` + `uv sync --frozen` → `dev/10`: CPython 3.12.15, `.venv`, `Installed 41
  packages`, the six direct pins highlighted.
  - `--frozen`: "install exactly the lock, never re-resolve" (GREEN, L1 callback).
  - extra `dev/17` `uv tree`: the six direct dependencies, one line.
- ▶ Run serve (README:561-563), verbatim → `dev/11`: gunicorn on `0.0.0.0:8086`; here `PORT` is
  set by you (V5).
  - Extra `dev/12`: the button now reads **Play audio**. Extra `dev/13`: Bonjour à tous.
  - Extra `dev/14`: speech → 503 "Google credentials are unavailable. Configure local ADC or attach
    an authorized runtime service account." That is the missing ADC login, honestly, and exactly
    what you see if you skip that step.
- ▶ `cd ../..` (`dev/18`).
- One line: the app guide's 17 offline tests pass (`dev/15`), which the exercises cover.

**S12 · Finite work: a job and two buckets (~250) — `s12_buckets.py` · `JobAndBuckets`.** Tracker
4.1 1→6. `lecture_ref(14, "9, 14")`.
- README:582-585: a person waiting for an answer vs a program that should "read its input,
  translate it, generate speech, save the files, and exit". That is a **job**.
- **V7** strips: service (ear, no edge) vs job (four segments, exit). Slide 14: "a container runs as
  a service or as a job"; V1's container cell splits.
- Slide 9's brace: L13's Vertex AI training job was the same shape, finite work on rented hardware.
- Why buckets: a job has no URL and its container's disk vanishes when it exits, so the input comes
  from Storage and the results go back to Storage (README:887-891). "A remote container cannot read
  a filename on your laptop" (README:918-919).
- ▶ CONSOLE 4.1, the wizard (README:595-613):
  - a globally unique name (e.g. project ID + `-translation-input`);
  - Region (Toronto), Standard;
  - **Enforce public access prevention** + **Uniform**;
  - default soft delete, no versioning;
  - Confirm → "Public access: Not public".
- ▶ Output bucket: repeat. GOLD tag: storage bills while objects exist, and soft delete keeps
  deleted ones for a while (S16).
- ▶ Upload passage: extra `laptop/40`, the real four-line passage (131 characters). CONSOLE
  `run-001/` folder + upload. ▶ Copy URI: `gs://YOUR_INPUT_BUCKET/run-001/passage.txt`, PINK.
- One line: `run-001` is a *prefix you chose*, not a real directory (README:887-889).
- `gcloud alternative` (README:660-673): typed with no output panel.

**S13 · Command, arguments and the job's badge (~310) — `s13_job.py` · `CommandAndArgs`.** Tracker
4.2 1→5, then 4.3 1→9. `lecture_ref(14, "14")`.
- ▶ 4.2 CONSOLE (README:679-690): `translation-audio-job` (worksheet card), the same two project
  roles, then **Storage Object Viewer on input** and **Storage Object Creator on output**. V6's
  second badge with two GREEN bucket-scoped chips; the web badge stays unchanged ("its audio goes
  straight to the browser").
- One line on least privilege: Creator can create files but cannot read, list or overwrite them,
  which is all this job needs (`storage.py` creates only, digest E3).
- README checkpoint 692-694: *your* identity needs separate rights to upload, execute and read.
- `gcloud alternative` (README:710-722): typed with no output panel.
- ▶ 4.3 CONSOLE (README:737-785):
  - Jobs → Deploy container → **Create job**; the same image; `translation-audio`, **1 task**;
  - **Container command** `python` (press Enter → a chip): "this replaces the image's web-server
    command" (README:747-748);
  - **the eleven argument chips**, one at a time, with V7's conveyor;
  - the three variables; **timeout 5 min, retries 0** (GOLD: retries can duplicate paid work);
  - the job's badge by **email** (the selector shows the name);
  - leave **Execute job immediately** unchecked; Create.
- **V7 command vs arguments**, with the real slots (`laptop/16:11-12`): command → ENTRYPOINT,
  arguments → CMD. No shell anywhere: each chip is exactly one argv element (README:750-753).
- Rehearsed for real with the same image, all extra:
  - `laptop/41` `--plan` (status `plan_only`, 131 characters, the five steps);
  - `laptop/42` `Batch failed: Speech is disabled …` **exit 1** (the truthful exit,
    `__main__.py:58-61`, CODE);
  - `laptop/43` `Batch failed: Google credentials are unavailable …`: "on Cloud Run the job's
    badge supplies that".
- The README's warning, made real: `laptop/44`, the whole block in one chip → `No module named '
  translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage'`. Read it as "one
  argument containing spaces, cut at the first dot".
- **PONDER 4** (8 s). Answer: arguments replace CMD, and the image has no ENTRYPOINT, so `-m`
  becomes the program. Docker's analogue: `laptop/45`, `exec: "-m": executable file not found in
  $PATH`, exit 127. And with *nothing* changed, the job starts the web server and waits until the
  5-minute timeout fails it: the README's troubleshooting row "Job starts a server instead of
  finishing" (README:1044).
- `gcloud alternative` (README:815-822): typed with no output panel. `--command=python` and the
  comma-separated `--args` are the same eleven values (`gcloud/07` help: "--command: Entrypoint for
  the container image").

**S14 · Execute it and collect the files (~250) — `s14_execute.py` · `ExecuteAndCollect`.** Tracker
4.4 1→5. `lecture_ref(14, "16")`.
- ▶ Execute (README:828-829). ▶ History → the green check, `recorded` `translation-audio-hq9f5`
  succeeded (`expected/part4:3`). → Tasks → View logs: "The job exits; it does not provide a web
  URL" (README:833).
- What the log line contains: the JSON shape from `expected/part4-task-log-shape.txt`
  (`illustration`, keys from `storage.py:48-56`: `output_uri`, `manifest_uri`, `status`,
  `artifacts`, `execution`, `task_attempt`), with placeholders, never invented values.
- ▶ Attempt folder + three files: **V8**. `recorded` `run-001/de2f41…/`, with the README's
  three-row table (`translated.txt`, `speech.wav`, `manifest.json`).
- Create-only uploads and the manifest last: "**the receipt**".
- Slide 16's debugging beat, the third place to look: "a green check says the process exited 0. The
  manifest says the work is complete. Partial files without a manifest don't establish success"
  (README:893-895).
- **PONDER 5** (6 s). Answer: no. A new UUID folder lands beside the first; uploads are create-only
  (V8 replay). The run is not exactly-once, though: a retry repeats paid work, which is why retries
  are 0.
- ▶ Download (README:844-848): the CONSOLE download icons.
- GOLD: one job execution = its task's running time + one TTS call.
- `gcloud alternative` (README:871-877): execute `--wait` + `mkdir -p results` + recursive copy,
  typed with no output panel. `--wait` waits but does not stream your app's logs (README:879-880).
- README checkpoint (850-852): "the task finished, the process stopped, and its files remain in
  Storage".

**S15 · From the terminal, then the helper (~260) — `s15_terminal.py` · `FromTheTerminal`.**
Tracker 4.5 1→4, then 4.6 1→2. No lecture_ref.
- The prerequisite (README:911-914): executing **with overrides** needs `run.jobs.runWithOverrides`
  on *you* (gotcha 14). That is your permission, not the job's badge.
- ▶ Bucket variables + ▶ upload: `gcloud/09`, verbatim (the two exports + `gcloud storage cp
  ./passage.txt "gs://$INPUT_BUCKET/run-002/passage.txt"`). It reaches the placeholder error again
  ("you know this one by now: put your real project ID in").
- ▶ Execute overrides (README:936-943), typed with no output panel: **`--args` replaces the whole
  argument list, for this execution only**. A V7 replay: the eleven chips are swapped for a new
  set; `run-002`, `es`. The saved job still says French (README:954-956). Leave out one flag and it
  is gone for that run (gotcha 15). `recorded`: "successful Spanish job execution" (README:963-964).
- ▶ Download results: typed with no output panel.
- ▶ Run helper (README:974-979), verbatim → `gcloud/10`:
  - it **prints each gcloud command first** (`$ gcloud storage cp … run-20261104-…-<hex>/passage.txt`);
  - it stops at the first failure: "Helper stopped: gcloud failed with exit status 1. Later steps
    were not run."
- Extra `gcloud/11` `--dry-run` (README:1000) shows **all three** commands it would run: upload to
  a fresh `run-<timestamp>-<hex>/`, `jobs execute … --args=… --wait --quiet`, the recursive
  download. V8: a new prefix per run.
- Extra `gcloud/13`: `--input-bucket=gs://…` is refused, "a plain name, without slashes" (gotcha
  13).
- ▶ Open results: `recorded`, "It prints Downloaded results only after finding a complete
  manifest" (README:992-993). The receipt again. One line: the helper needs only Python and a
  signed-in gcloud; the job gets ADC from its badge (README:1006-1008).

**S16 · Clean up, and what serverless costs (~270) — `s16_recap.py` · `CleanUpRecap`.** Tracker CU
1→4. `lecture_ref(14, "9, 16")`.
- ▶ The README's checklist (README:1020-1028) as a GOLD card that empties item by item:
  - download what you want to keep;
  - delete `translate-function` and `translation-demo`, then the job;
  - delete the objects and buckets, then the two runtime accounts once they are detached;
  - delete **the function's image in Artifact Registry** (V3's callback: the image is still on the
    shelf after the service is gone).
- Added, kindly (erratum 7):
  - soft-deleted objects stay recoverable, and billable, for the retention period
    (`docs/lifecycle.md:176-177`);
  - the build also leaves source archives and logs (`docs/lifecycle.md:205-210`);
  - keep the shared public image and other course resources.
- Optional, one line: the scripted practice stack. Extra `gcloud/20`: its plan lists every resource
  a clean-up must cover, including the job **by digest**. It is a plan by default and changes
  things only with `--apply`.
- **Slide 16's three cons as a checklist that the tutorial answers** (V1 complete):
  - **cold starts** → min instances, which trades money for warmth (V2 drip);
  - **limited control and debugging** → the three places to look: the build log (S05), the service
    logs (S06/S10), the job's logs and manifest (S14);
  - **vendor lock-in** → the image and functions-framework ran on your laptop; the Google-specific
    parts are the console, IAM and the build.
- Slide 9's "NEXT" brace: L15, a Vertex AI endpoint for a trained model, then pipelines.
- Recap questions, five, one at a time (answers in `exercises.md`). Ends on an empty frame.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 210 | S09 RuntimeIdentity | 250 |
| S02 FourWays | 250 | S10 EnableSpeech | 250 |
| S03 BeforeYouBegin | 250 | S11 LocalDevelopment | 260 |
| S04 WriteAFunction | 280 | S12 JobAndBuckets | 250 |
| S05 InsideTheFunction | 280 | S13 CommandAndArgs | 310 |
| S06 CallTheEndpoint | 290 | S14 ExecuteAndCollect | 250 |
| S07 RunTheImage | 290 | S15 FromTheTerminal | 260 |
| S08 DeployTheImage | 290 | S16 CleanUpRecap | 270 |
| **part 1** | **2,140** | **part 2** | **2,100** |

Total ≈ **4,240** words ≈ 24.4 min of narration. Typing, outputs, CONSOLE fills and five ponder
timers bring it to ~30–32 min.

## Ponder questions

There are five timed ponders, as Conny decided on 2026-10-21 (3–5 per video). REVIEW.md marks
content gate 3 met with that decision. Each one is quiz-style, with a YELLOW timer, and is
answerable from the picture or capture shown just before it. Option cards are optional for the
script; the answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S05 (8 s) | "You paste `main.py` but type `translate`\nas the entry point. Does the build fail?\nIf not, what fails, and where do you see it?" | The build succeeds (the requirements are fine). The framework fails at start-up when it looks the name up: `MissingTargetException … expected to contain a function named 'translate'. Found: 'hello_http'` (`dev/29:28`), in the logs |
| 2 | S08 (8 s) | "Concurrency 4, max instances 2.\nTen people press Translate at once.\nHow many instances — and the last two?" | Two instances (the ceiling), eight slots. The other two wait for a free slot and can be refused. Fix: max instances, or concurrency together with gunicorn's threads; min instances doesn't help |
| 3 | S09 (6 s) | "The service allows public access.\nDoes that let it call Agent Platform?" | No. Public access answers *who may call it*; calling out needs an identity with roles: the runtime service account (README:361-362) |
| 4 | S13 (8 s) | "You fill all eleven argument chips\nbut leave Container command empty.\nWhat does the container try to run?" | Arguments replace CMD, and there is no ENTRYPOINT, so `-m` becomes the program and the container cannot start (Docker's analogue `laptop/45`: exit 127). With nothing changed, it would start the web server and time out (README:1044) |
| 5 | S14 (6 s) | "Execute the same job again,\nsame arguments. Is the first\nresult overwritten?" | No. A new UUID attempt folder; create-only uploads; each attempt has its own manifest. A retry still repeats paid work, so retries stay 0 |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Place Part 1 and Part 2 on the lecture's 2×2: what do you hand over, and who builds the image in
   each case?
2. Which two settings make the meter run while nobody is using the app, and what does min
   instances buy you?
3. "Who may call it" and "who it runs as": which setting answers each in this tutorial, and why
   is no key file needed?
4. Why does the job set a **command** and eleven **separate** arguments, and what happens with
   neither?
5. Name the lecture's three downsides of serverless, and what this tutorial gives you for each.

(Digest recap Q4 on bucket roles, SLIDES' "place paths A and B" variant, and E6's Little's-law
version go to exercises.md.)

## Errata and version drift to state (kindly, with the fix)

1. **The course links land on no section** (course page and slides 12/15:
   `#running-app-as-cloud-function`, `#running-app-in-cloud-run`). Those headings existed at
   `4eaf343`. Fix: start at the top; Part 1 is the function, Parts 2–4 are Cloud Run (S02).
2. **Slides vs today's README** (SLIDES Conflicts 1, 3, 5): Cloud Functions → *Cloud Run
   functions* (S04); the slide's script sketch vs the deployed handler, so pass `src=`/`dest=` by
   name (S04/S06); "create a Python file" → file + requirements + entry point (S04); Python 3.10
   → 3.12 (S04).
3. **The course map pins an older commit** (`4eaf343`); the link serves `46cc62f` (S02, one
   clause).
4. **Unused 2025 files at the repo root** (`main.py`, `cli.py`, `Dockerfile`, …), never mentioned
   by the README, which says to work from the root. Don't build the root Dockerfile; the app's
   image comes from `tutorial/app/` (S03).
5. **`YOUR_PROJECT_ID` is refused as a project ID** before any sign-in (`gcloud/05`), also in
   `docs/lifecycle.md`'s own example (`gcloud/15`). Fix: your real ID (S03, S06, S15).
6. **A mutable tag in the click path** (README:276-278, 741-743); the digest appears only at
   README:1068-1070. Deploy by digest when it must be reproducible (S08).
7. **Clean-up stops short**: soft-delete retention and the build's source archives and logs (S16).
8. **README:378-379** promises developer access in 3.3, but nothing grants the **Service Account
   User** needed in 3.2. Owners have it; in restricted projects, ask staff (S10).
9. **"Pay only while code runs"** (slides 11, 14) holds for compute with request-based billing and
   min instances 0. Builds, stored images, buckets and TTS calls are extra (S08, S16, Conflict 4).
10. **"Without managing … containers"** (slide 11): true, but Google still builds one. That is why
    there is an image to delete (S05).
11. **Version drift, "at the time of recording"**: gunicorn 26.2.0's fifth start-up line; uv
    0.13.7; gcloud 592.0.0; the googletrans endpoint's availability on any given day (S06); the
    console labels (from the README and its GIFs, not seen live; "if a label differs, look for the
    same field").
12. Not in the video (exercises only): `.dockerignore` patterns that miss nested `__pycache__`
    (digest erratum 5, harmless).

## Costs and teardown

This lecture **creates billable cloud resources and calls a paid model**. GOLD tags appear exactly
where each one starts. No prices are stated as fact: "check the pricing page", and the free-tier
figures are not quoted.
- **S04**: the function, billed as a Cloud Run service, plus Cloud Build time on each deploy, plus
  the image the build stores in Artifact Registry.
- **S08**: `translation-demo`, request-based with min 0 and max 2 (the guardrails). Min ≥ 1 or
  instance-based billing makes idle time cost (V2).
- **S10**: Gemini TTS per Play audio.
- **S12**: two buckets, Standard storage; soft delete keeps deleted objects.
- **S13/S14**: each job execution (task time + one TTS call); retries 0, timeout 5 min.

Teardown (S16), the README's four items plus the two additions above. Each item is a card line
spoken in the same words. Nothing here is captured (console). The scripted alternative
`tutorial/tear_down.py` is shown only as a plan (`gcloud/16`, `21`: it needs the manifest that
`--apply` writes).

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order (`46cc62f`).

| README instruction | README line | scene |
| --- | --- | --- |
| Select project, check the project ID | 28-31 | S03 (CONSOLE) |
| Billing and permissions | 32-34 | S03 (CONSOLE) |
| Region `northamerica-northeast2`; speech `us-central1` later | 35-37 | S03 (CONSOLE) |
| Clone or download the repository; work from the root | 38-41 | S03 (`laptop/01`, `extra` spelling) |
| Worksheet of names | 46-55 | S03 (cards) |
| Terminal setup: `gcloud auth login` | 74 | S03 (typed, no panel; `gcloud/03` before) |
| Terminal setup: the seven `export` lines | 75-81 | S03 (`laptop/05`) |
| 1.1 Write a function … Create, Source editor | 99-109 | S04 (CONSOLE) |
| 1.2 Replace `main.py`, `requirements.txt`; entry point `hello_http`; Save and redeploy | 126-152 | S04 (CODE + CONSOLE) |
| 1.3 Copy URL; default call; `?text=Good%20afternoon%20everyone&src=en&dest=fr`; `el`/`hi`/`zh-cn`; Logs 200 | 156-169 | S06 (`recorded`; stand-in `dev/23`, `25`-`28`) |
| Part 1 gcloud: `gcloud run deploy translate-function …` | 195-198 | S06 (`gcloud/05`, `18`) |
| Part 1 gcloud: `FUNCTION_URL=$(gcloud run services describe …)` | 200-201 | S06 (typed, no panel) |
| Part 1 gcloud: `curl --get "$FUNCTION_URL" --data-urlencode …` | 202-204 | S06 (`dev/24`, stand-in URL) |
| 2.1 `docker run --rm -p 8086:8080 cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` | 246-249 | S07 (`laptop/10`) |
| 2.1 Open http://localhost:8086; Translate; Play audio disabled; Ctrl+C | 251-255 | S07 (`laptop/11`, `21`, `24`, `10:23-26`) |
| 2.2 Deploy container … Revision History, Logs | 272-296 | S08 (CONSOLE; `recorded`) |
| Part 2 gcloud: `gcloud run deploy "$WEB_SERVICE" …` | 320-325 | S08 (typed, no panel) |
| 3.1 Agent Platform API; create `translation-demo-runtime`; two roles; record email | 366-380 | S09 (CONSOLE; `recorded`) |
| 3.1 gcloud: `services enable` + `service-accounts create` + two `add-iam-policy-binding` | 411-420 | S09 (typed, no panel) |
| 3.2 Security → account; three env vars; View diff & redeploy; reload, Play audio; Logs | 436-458 | S10 (CONSOLE; `recorded`) |
| 3.2 gcloud: `gcloud run services update "$WEB_SERVICE" …` | 488-493 | S10 (typed, no panel) |
| 3.3 Token Creator grant; IAM Service Account Credentials API | 519-525 | S11 (CONSOLE) |
| 3.3 `export DEVELOPER_EMAIL=…` · `services enable iamcredentials…` · `add-iam-policy-binding … tokenCreator` · `application-default login --impersonate-service-account` · `set-quota-project` | 540-549 | S11 (typed, no panel) |
| 3.3 `cd tutorial/app` · `uv sync --frozen` | 559-560 | S11 (`dev/10`) |
| 3.3 `ENABLE_SPEECH=true … PORT=8086 uv run python -m translation_demo serve` | 561-563 | S11 (`dev/11`; `12`-`14`) |
| 3.3 `cd ../..` | 567 | S11 (`dev/18`) |
| 4.1 two buckets (wizard); `run-001` folder; upload `passage.txt`; copy URI | 595-621 | S12 (CONSOLE; `laptop/40`) |
| 4.1 gcloud: exports, `services enable storage…`, two `buckets create`, `storage cp` | 660-673 | S12 (typed, no panel) |
| 4.2 `translation-audio-job`; project roles; Viewer on input; Creator on output | 679-690 | S13 (CONSOLE) |
| 4.2 gcloud: create + two project bindings + two bucket bindings | 710-722 | S13 (typed, no panel) |
| 4.3 Create job: image, name, 1 task, command `python`, eleven arguments, variables, timeout/retries, service account, Create | 737-785 | S13 (CONSOLE; rehearsals `laptop/41`-`45`) |
| 4.3 gcloud: `gcloud run jobs create "$JOB_NAME" …` | 815-822 | S13 (typed, no panel) |
| 4.4 Execute; History; View logs; output folder; three files; download | 828-848 | S14 (`recorded`; log shape `illustration`) |
| 4.4 gcloud: `jobs execute … --wait` · `mkdir -p results` · `storage cp --recursive …run-001` | 871-877 | S14 (typed, no panel) |
| 4.5 `export INPUT_BUCKET=…` / `OUTPUT_BUCKET=…` | 921-927 | S15 (`gcloud/09:1-2`) |
| 4.5 `gcloud storage cp ./passage.txt "gs://$INPUT_BUCKET/run-002/passage.txt" --project=…` | 929-934 | S15 (`gcloud/09`) |
| 4.5 `gcloud run jobs execute "$JOB_NAME" … --args="…run-002…es…" --wait` | 936-943 | S15 (typed, no panel; `recorded`) |
| 4.5 `mkdir -p results` · `gcloud storage cp --recursive "gs://$OUTPUT_BUCKET/run-002" ./results …` | 945-951 | S15 (typed, no panel) |
| 4.6 `python tutorial/run_job.py ./passage.txt …` | 974-979 | S15 (`gcloud/10`; extra `11`, `13`, `19`) |
| Clean up (four items) | 1020-1028 | S16 (card) |

The `docs/lifecycle.md` commands are optional and are not README steps: S16 shows one plan
(`gcloud/20`), and the rest go to exercises.

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, started from L11's):
  - tracker factories `tracker_bb`, `tracker_11` … `tracker_46`, `tracker_cu`, with the step lists
    above (titles ≤ 3 words) and a `gcloud alternative` caption variant;
  - prompts `P_LAPTOP` (+ `~/serverless-deployment`, `~/serverless-deployment/tutorial/app`),
    taken from each capture;
  - tags `your_turn`, `extra_tag` (variants `extra · local stand-in`, `extra · Docker's analogue`),
    `illustration_tag`, `recorded_tag`, `cost_tag` (GOLD), `lecture_ref`;
  - a `console_form(title, rows)` helper for the schematic CONSOLE panels, with no Google
    branding;
  - a `chip_row(values)` helper for the argument chips;
  - set-piece classes `DeployGrid` (V1, persistent state across scenes), `InstanceStrip` (V2),
    `BuildLine` (V3), `QueryToArgs` (V4), `PortEnvelope` (V5), `IdentityDoors` (V6),
    `LifecycleStrips` (V7), `AttemptFolders` (V8).
  - **Never reuse a scene class name** (`video.yaml`) for a helper.
- **The sandbox framing is load-bearing.** It is said once, in S03. Afterwards every gcloud error
  is the lesson, and every cloud success is `recorded` with its source. The local stand-in for
  Part 1 is always tagged. Never imply that a failure surprised us, and never claim a deploy, an
  IAM grant, a bucket, an execution or a download happened live.
- **gcloud boxes with no output panel**: the command is typed verbatim, and the narration says
  what to look for ("a URL", "Done", "the execution name"). No panel and no invented line.
- **CONSOLE panels**: field labels and values only from the README lines cited above. Button labels
  as the README writes them (**Write a function**, **Save and redeploy**, **View diff & redeploy**,
  **Deploy changes**, **Execute**). Never draw progress numbers, URLs with ids, or execution ids
  except the README's `translation-audio-hq9f5` / `de2f41…`.
- **Long lines**: `laptop/44:2` and `45:2` fold with `wrap` or are cropped from the meaningful
  phrase on. `gcloud/10:5`, `11:5-8` fold. The `dev/29` traceback shows first line, `…`, last line.
  `dev/10` shows lines 2-4, `…`, `Installed 41 packages`, then the six direct pins.
- **Never read aloud**: timestamps, PIDs, layer ids, the helper's random suffixes, the image's
  namespace.
- **Personal data**: no instructor name anywhere (‹instructor› if one must be referred to: "the
  course's console recording"). README:257-258's "instructor's local run" is said as "the course's
  recording". The developer email is always `YOUR_GOOGLE_ACCOUNT_EMAIL`.
- **Lexicon heads-up** (script stage): gunicorn (exists), googletrans ("Google trans"),
  functions-framework, `hello_http` ("hello H-T-T-P"), `translation_demo`, `zh-cn`, `8086` /
  `8080` (say "eighty eighty-six", "eighty eighty"), `0.0.0.0` (a phrase key, as L16's IP entries),
  `us-central1`, `northamerica-northeast2`, `execvp`, argv, ADC (exists), IAM (exists),
  `--frozen`, `hq9f5`, UUID, `.wav`. Check phonemes with `explainer/voice.py`. Every spoken decimal
  version is keyed as in L13.
- **Chinese glossary heads-up**: these stay English: serverless, Cloud Run, Cloud Run functions,
  Cloud Build, Artifact Registry, function, entry point, functions-framework, gunicorn, revision,
  instance, cold start, scale to zero, concurrency, min/max instances, request-based billing,
  service, job, task, execution, image, tag, digest, container command/arguments, chip, argv,
  service account, runtime identity, ADC, impersonation, IAM, role, bucket, prefix, manifest,
  query string, endpoint. Use 无服务器 only beside "serverless" on first use, as the exam edition's
  glossary does (reuse `../ac215-l14-exam/i18n/zh/glossary.yaml` where it agrees).

## Things never to do on screen

Series rules:
- No slide images, QR codes, console screenshots, the README's GIFs, or Google/GCP logos. Redraw
  the idea and cite slides via `lecture_ref`. The console is a schematic `illustration` with README
  field values and **no invented values**: no URLs with real-looking hashes, no prices, no
  execution ids beyond the README's.
- No real person's name, e-mail or account on screen (the prompt user is `student`; placeholders
  above). The instructor is never named in frames or subtitles. The image's namespace appears only
  inside the verbatim image string.
- No hand-typed output: every terminal line comes from `assets/terminal/`. `recorded` panels name
  their source (README line or GIF caption); stand-in panels are tagged.
- No command spelled differently from the README (the clone and the stand-in URL in `dev/24:1` are
  marked `extra`).
- No credentials: no key, token, ADC file content or project id that looks real.

Lecture-specific:
- Don't say "serverless means no servers" or "a function has no container". Say *you don't manage
  them*, and that Google builds the container.
- Don't say "you only pay while code runs" without "with request-based billing and min instances
  0", or call the function's image free.
- Don't present `dev/` results as the deployed function's: they are the same handler under the
  same framework, on a laptop, tagged so.
- Don't draw the job with a URL or a port, or the web service with a bucket.
- Don't say `gcloud auth login` gives the app credentials, or that public access lets the app call
  Agent Platform.
- Don't call the Cloud Run error for "arguments without a command" by `laptop/45`'s text: that is
  Docker's analogue, tagged so.
- Don't tell viewers to delete the shared public image, or to set retries above 0 on the first
  walkthrough.
- Don't build or mention building the repo-root `Dockerfile` as the tutorial's image.

## Left for exercises.md (not in the video)

- Digest E1 (PORT=9090 in full; the video shows it briefly), E2 both cases, E3 (Creator without
  read), E4 (entry point; the video's ponder), E5 (speech denied: the check order), E6 (Little's
  law), E7 (three identities), E8 (tag vs digest pull).
- The app guide's 17 offline tests (`dev/15`) and `batch --plan` (`dev/16`); `batch --help`
  (`laptop/47`); a bad URI (`laptop/46`, exit 2); the lifecycle scripts' 25 tests (`gcloud/17`) and
  `tear_down.py`'s missing-manifest stop (`gcloud/21`).
- The `.dockerignore` nested `__pycache__` erratum; the old README at `4eaf343` vs today (digest
  §7, "What changed"); the `pipenv` branch.
- Container credential mounts and rootless Docker (`tutorial/app/README.md:168-191`); the input
  limits (5,000 characters, 20,000 bytes, 4,000 UTF-8 bytes of speech text).
