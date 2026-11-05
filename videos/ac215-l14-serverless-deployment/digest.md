# L14 · Serverless Deployment: Cloud Functions, Cloud Run — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166039/ (not accessible from here). The course
  tutorials page (`harvard-iacs.github.io/2026-AC215/tutorials_demo/`, fetched live on 2026-11-04) lists
  "Cloud Function" → `github.com/dlops-io/serverless-deployment#running-app-as-cloud-function` and
  "Cloud Run" → `…#running-app-in-cloud-run`, i.e. the repo's **default branch, unpinned**. AWS variant:
  "Coming Soon". Colab notebooks: none.
- **Pinned commit (what this video follows): `main` @ `46cc62fd8b1ac94ce733571a834b46002d8dd8c4`**
  (`46cc62f`, 2026-10-22 09:26:24 -0400, "Point student setup instructions to the main repository").
  Checked on 2026-11-04 with `git ls-remote`: it is still `HEAD`/`main` on GitHub, so it is the README a
  student reaches from the course link today. The published exam edition `videos/ac215-l14-exam/` quotes
  the same commit.
  - The course map (`MLOps_Learning/course/lectures.yaml:33`) and the batch `units.json` still name
    `4eaf3433a3430f51306e67247287a124d0c35710` (2025-10-20 21:53:06 -0400, "updates"). Between the two,
    28 commits on 2026-10-21/22 replaced the ~150-line README with a **1,079-line four-part tutorial**
    (function → web-app service → runtime identity + speech → job with Cloud Storage) and a new app under
    `tutorial/`. The two README anchors the course page links no longer exist (§10, erratum 1).
  - Other branches: `codex/four-part-tutorial` @ `fadf1b9` (the rewrite's working branch; `46cc62f` is its
    tip plus one README line), `pipenv` @ `fb0cb7f` (the 2024 code).
- **README parts this lecture covers:** all of it. The course page's two sections ("Cloud Function", "Cloud
  Run") now map onto Part 1 (function) and Parts 2–4 (Cloud Run service, its identity, Cloud Run job).
  Headings: `## Before you begin` (README.md:26), `## Part 1` (91), `## Part 2` (235), `## Part 3` (355),
  `## Part 4` (580), `## Clean up after the tutorial` (1018), `## Troubleshooting and further reading` (1030).
- **The one container image Parts 2–4 deploy:** `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`
  (README.md:58-60, 276-278, 741-743), a personal Docker Hub namespace (do not name its owner on screen).
  Inspected read-only through the registry API on 2026-11-04:
  - manifest digest `sha256:c17b6db09f7402febb582bf327920ec9ca4eee113f5ddefa38e9da5619dbe72e`, equal to the
    digest README.md:1068-1070 and `tutorial/app/README.md:228-229` publish; single-platform `linux/amd64`
    (no manifest list, no variant), tag pushed 2026-10-22 05:17 UTC;
  - config: base `python:3.12-slim-bookworm` (Python 3.12.15), `ENV PYTHONUNBUFFERED=1
    PYTHONDONTWRITEBYTECODE=1 PORT=8080`, `WORKDIR /app`, `USER app`, `EXPOSE 8080`, no ENTRYPOINT,
    `CMD ["python","-m","translation_demo","serve"]` — the layer history is exactly `tutorial/app/Dockerfile:1-12`;
  - its `translation_demo/*.py`, `templates/index.html`, `examples/passage.txt`, `pyproject.toml` and
    `requirements.lock` are byte-identical to `tutorial/app/` at `46cc62f` (diffed). It also carries
    `translation_demo/__pycache__/*.pyc` (§10, erratum 5).
  - Two older tags exist (`lecture14-batch-50d8201`, `lecture14-ui-speech-4096c0f`, 2026-10-21); the README
    uses neither.
- **External code checked:** `functions-framework` **3.10.2** (the version `tutorial/function/requirements.txt:1`
  pins), wheel from PyPI (uploaded 2026-06-17; still the latest release on 2026-11-04):
  `src/functions_framework/_cli.py`, `_function_registry.py`, `_http/gunicorn.py`.
- **Context repos** (none is run in this lecture): `simple-translate` `62f821b`, `port_toy` `d190c71`,
  `mega-pipeline` `c6bbc9b`, `cheese-app-v0` `cb6fb94`, `model-training` `b9aee1c`.
- **Slides:** `SLIDES.md` in this folder (17 slides). It was written against `4eaf343`; where it and the
  `46cc62f` README differ, the README (and later the captures) decide what the video shows (§10, erratum 2).

---

## 1. What you build

One translation app, deployed four ways on Google Cloud, none of them a VM you manage. The README's own
table (README.md:12-17):

| Part | What you do | New idea |
|---|---|---|
| 1 | Paste a 6-line handler into Cloud Run's function editor and call its URL with `?text=…&src=…&dest=…` | You supply **code**; Google builds the runnable image |
| 2 | Run a prebuilt web UI on your laptop, then deploy **the same image** as a Cloud Run service | Deploy an existing container image |
| 3 | Attach a **runtime service account** to that service and turn on "Play audio" (Gemini text-to-speech through Agent Platform) | The identity the app *runs as*, with no key file |
| 4 | Run the same image as a Cloud Run **job**: read a passage from a private bucket, translate it, synthesize speech, write `translated.txt`, `speech.wav`, `manifest.json`, exit | Finite work whose results persist in Cloud Storage |

The README frames the point (README.md:7-10): the translation model is an external service; we deploy
the **application code around the model** — accept input, call a model service, return a result — the
same role the Cheese App's backend will play.

```
YOUR LAPTOP                                    GOOGLE CLOUD PROJECT  (Cloud Run region: northamerica-northeast2, Toronto)
+---------------------------------+
| repo serverless-deployment/     |  Part 1   console "Write a function" (inline editor)
|  tutorial/function/main.py  ----+--------> main.py + requirements.txt + entry point hello_http
|  tutorial/function/requirements |            -> Cloud Build (buildpacks, base python312) -> Artifact Registry image
|                                 |            -> Cloud Run service "translate-function"   URL https://…run.app/?text=…&src=en&dest=fr
|                                 |                 functions-framework --target hello_http on $PORT
| docker run --rm -p 8086:8080    |
|   cgumb/ac215-translation-demo  |  Part 2   "Deploy container", same image (tag; digest sha256:c17b6db0…)
|   :lecture14-agent-platform-…   +--------> Cloud Run service "translation-demo"  (public, request-based billing,
|   -> http://localhost:8086      |            min 0 / max 2 instances, 1 CPU, 512 MiB, concurrency 4, timeout 120 s)
|                                 |            container CMD: python -m translation_demo serve -> gunicorn 0.0.0.0:$PORT, 1 worker x 4 threads
|                                 |  Part 3   + service account translation-demo-runtime (Agent Platform User, Service Usage Consumer)
|                                 |            + env ENABLE_SPEECH=true, GOOGLE_CLOUD_PROJECT, GOOGLE_CLOUD_LOCATION=us-central1
|                                 |            browser -> POST /api/speech -> ADC token (metadata server) ->
|                                 |            us-central1-aiplatform.googleapis.com … gemini-2.5-flash-tts:generateContent -> WAV -> browser
| (optional) ADC + impersonation  |
|   uv run python -m              |  Part 4   Cloud Run job "translation-audio", same image, command "python",
|   translation_demo serve        |            args -m translation_demo batch --input-uri gs://IN/run-001/passage.txt
|                                 |                 --src en --dest fr --output-uri gs://OUT/run-001/
| gcloud storage cp / run jobs    |            service account translation-audio-job (+ Object Viewer on IN, Object Creator on OUT)
|   execute --args=… --wait       +--------> read passage -> translate -> speech -> write
| python tutorial/run_job.py      |            gs://OUT/run-001/<uuid4 hex>/{translated.txt, speech.wav, manifest.json} -> exit 0
+---------------------------------+

Every text translation (Parts 1-4) leaves Google Cloud for googletrans 4.0.0rc1's *unofficial* web endpoint
(no credentials). Only speech (Parts 3-4) and Storage (Part 4) use a Google identity.
```

The repo root still holds the 2025 files (`main.py`, `cli.py`, `Dockerfile`, `docker-entrypoint.sh`,
`docker-shell.sh`, `pyproject.toml`, `uv.lock`), unchanged since `4eaf343`, which the new README never
mentions (§10, erratum 4). Everything the README uses lives under `tutorial/`.

---

## 2. Prerequisites and costs

**Accounts and local installs** (README.md:28-41)
- Your **course project** selected in the console; check the **project ID**, not only the display name
  (README.md:28-31). Billing enabled, and permission to create Cloud Run resources, service accounts and
  buckets and to grant their roles (README.md:32-34).
- A region: the README uses **Toronto, `northamerica-northeast2`** for Cloud Run and buckets; the speech model
  uses **`us-central1`**, a separate setting introduced in Part 3 (README.md:35-37).
- A clone of the repo; terminal examples run from the **repository root** (README.md:38-39). Docker for the
  local demo in Part 2; Python and the Google Cloud CLI for the helper in Part 4; the console-only path needs
  neither (README.md:39-41). `uv` only for the optional local development in Part 3 (README.md:556).
- Worksheet of names (README.md:46-55): function service `translate-function`, web service
  `translation-demo`, web runtime account `translation-demo-runtime`, job `translation-audio`, job runtime
  account `translation-audio-job`, plus two globally unique bucket names you choose in Part 4.
- **Terminal setup** (collapsed, README.md:66-89), run once before any gcloud box:
  ```bash
  gcloud auth login
  export PROJECT_ID=YOUR_PROJECT_ID
  export REGION=northamerica-northeast2
  export IMAGE=cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
  export WEB_SERVICE=translation-demo
  export JOB_NAME=translation-audio
  export WEB_EMAIL="translation-demo-runtime@${PROJECT_ID}.iam.gserviceaccount.com"
  export JOB_EMAIL="translation-audio-job@${PROJECT_ID}.iam.gserviceaccount.com"
  ```
  The README stresses that `gcloud auth login` sets up the **CLI** identity, not the application's ADC
  (README.md:86-87).
- Console first: the "Equivalent gcloud commands" boxes are **alternatives**, not extra steps (README.md:19-21).

**APIs**
- Part 1: whatever "Write a function" prompts for (README.md:102); the gcloud path "may prompt you to enable
  APIs or create a build repository" (README.md:191-192). `docs/lifecycle.md:70-71` lists what a fresh
  project needs: Cloud Run, Cloud Build, Artifact Registry, Agent Platform, Cloud Storage, IAM and IAM Service
  Account Credentials.
- Part 3: **Agent Platform API** = `aiplatform.googleapis.com` (README.md:366-367, 383-384) — the console's
  current name for what earlier lectures called the Vertex AI API; its user role "Agent Platform User" is
  `roles/aiplatform.user`. Local impersonation also needs the **IAM Service Account Credentials API**
  (`iamcredentials.googleapis.com`, README.md:524-525, 542).
- Part 4: Cloud Storage (`storage.googleapis.com`, README.md:664; normally already on).

**Identities, keys and secrets: where the code expects them**
- **No key file anywhere.** Part 1 and text translation need no Google credentials at all (googletrans calls
  a public endpoint; `tutorial/app/README.md:40-41`). Speech and Storage use **Application Default
  Credentials**: `google.auth.default(...)` (`tutorial/app/translation_demo/speech.py:101-105`) and
  `storage.Client(...)` (`storage.py:19-20`). On Cloud Run ADC comes from the **attached service account**;
  locally from `gcloud auth application-default login` (optionally impersonating that account).
- Two runtime accounts, one per workload (README.md:368-380, 677-690):
  - `translation-demo-runtime`: **Agent Platform User** + **Service Usage Consumer** on the project; no Storage role.
  - `translation-audio-job`: the same two roles, **Storage Object Viewer** on the input bucket only, **Storage
    Object Creator** on the output bucket only.
- Your own (developer) identity needs, separately (README.md:422-427, 432-434, 724-727, 911-914):
  **Service Account User** (`iam.serviceAccounts.actAs`) on each runtime account to attach it; for local
  impersonation **Service Account Token Creator** on the web account (README.md:519-524); to execute with
  argument overrides `run.jobs.run` + `run.jobs.runWithOverrides` (role **Cloud Run Jobs Executor With
  Overrides**); upload access to the input bucket and read access to the output bucket. Project Owners have
  all of these already.
- App configuration is environment variables, not secrets: `ENABLE_SPEECH`, `GOOGLE_CLOUD_PROJECT`,
  `GOOGLE_CLOUD_LOCATION` (README.md:444-448, 772-776), optional `VERTEX_TTS_MODEL` (default
  `gemini-2.5-flash-tts`) and `VERTEX_TTS_VOICE` (default `Kore`) (`speech.py:83-86`), and `PORT`
  (`__main__.py:23`, image default 8080). Cloud Run itself injects `CLOUD_RUN_EXECUTION` and
  `CLOUD_RUN_TASK_ATTEMPT` into job tasks, which the manifest records (`storage.py:50-51`).

**What costs money, and how to shut it down.** The README's clean-up (README.md:1018-1028) covers the first
four rows; the rest are added.

| Billable resource | Created in | How to remove |
|---|---|---|
| Cloud Run function `translate-function` (Cloud Run service billing) + **Cloud Build** time for each (re)deploy | Part 1 | Cloud Run → select → Delete (README.md:1021) or `gcloud run services delete translate-function --region=$REGION` |
| Cloud Run service `translation-demo` | Part 2 | same (README.md:1021) |
| Cloud Run job `translation-audio` (vCPU/GiB-seconds per execution) | Part 4 | Jobs → Delete (README.md:1021-1022) or `gcloud run jobs delete …` |
| **Artifact Registry** image the function build produced | Part 1 | README.md:1026-1028: remove "its unused image"; keep the shared repository if other work uses it (`docs/lifecycle.md:205-210`) |
| Two buckets + objects (Standard storage; soft delete keeps deleted objects recoverable — and billable — for the default 7 days, `docs/lifecycle.md:94, 176-177`) | Part 4 | delete objects and buckets (README.md:1023-1024) |
| **Gemini TTS** calls (per request, both the web "Play audio" and every job execution) | Parts 3–4 | stop calling; delete service/job |
| Function source upload / build logs in Google-managed buckets [added] | Part 1 | review Cloud Storage and Artifact Registry separately (`docs/lifecycle.md:205-210`) |
| Service accounts (free, but remove: README.md:1024-1025) | Parts 3–4 | IAM → Service Accounts → Delete, after detaching |

Cost intuition (verify at cloud.google.com/run/pricing; numbers said "at the time of recording"):
- Request-based billing with min instances 0 (the README's choice, README.md:281-283) charges CPU and memory
  only while a request is being handled, plus a per-request fee; Cloud Run's monthly free tier (for years
  180,000 vCPU-seconds, 360,000 GiB-seconds, 2 million requests per billing account) dwarfs this tutorial.
- The README caps the web service at **max 2 instances** (README.md:282-283) and the job at **0 retries, 5-minute
  timeout** (README.md:778-780): the guardrails that bound a mistake.
- Real surprise-bill routes: min instances ≥ 1 (one always-on vCPU for 30 days ≈ 2.59 M vCPU-seconds, ~14× the
  free tier), instance-based billing, retries on a paid job (README.md:895-897), leftover images and buckets.

---

## 3. Concepts this tutorial teaches

### 3.1 Serverless = you hand over the server's lifecycle — scale to zero, scale out ★ ANIMATE
- **Explanation:** "Serverless" still runs on servers; you stop deciding *when* one exists. You hand over a
  unit (source for a function, an image for a service or job) plus limits (CPU, memory, max instances,
  concurrency, timeout). The platform starts instances when requests arrive, adds more under load, and removes
  them when traffic stops (**scale to zero**). README.md:218-224: a cold start "initializes an instance of the
  built application; it does not necessarily boot a new VM", scaling to zero "applies to app instances, while
  Google's routing infrastructure remains available", and "there is no fixed inactivity interval" to predict
  the next cold start.
- **Mental model:** instances ≈ ⌈in-flight requests / concurrency⌉, clamped to [min, max]. With Part 2's
  settings: concurrency 4, max 2 → at most 8 requests in progress at once.
- **Analogy:** a VM is a restaurant staffed 24/7; serverless calls cooks in when orders arrive.
- **Misconception:** "My instance remembers the last request." Successive requests can reach different
  instances (README.md:343-344); anything in memory or on local disk may vanish. Part 4 therefore writes its
  results to Cloud Storage, not the container's filesystem (README.md:887-891).

### 3.2 Cold starts and the min-instances knob ★ ANIMATE
- **Explanation:** a request with no free warm instance waits for: image ready → container start → `python -m
  translation_demo serve` → `os.execvp("gunicorn", …)` (`__main__.py:24-26`) → gunicorn imports
  `translation_demo.web:create_app()` and binds the port → only then the request. For the function: buildpack
  image → functions-framework imports `main.py` and starts gunicorn. README.md:223-224: minimum-instance
  settings "can keep capacity warm when that matters".
- **Mental model:** latency = cold-start tax (once per new instance) + per-request work. Dependency
  installation happens at **build time**, not per request (README.md:216). This code builds the googletrans
  `Translator` **inside** each request (`tutorial/function/main.py:12`, `translation.py:33`) and imports
  googletrans lazily on first use (`translation.py:29-31`), so the first translation on a new instance also
  pays that import.
- **Misconception:** "Cold start = slow handler code." Mostly it is process start, imports and framework
  init. The slides list cold starts as a con of serverless (slide 16).

### 3.3 Request-based vs instance-based billing ★ ANIMATE
- **Explanation:** **Request-based** (selected in README.md:281): pay CPU and memory only while an instance
  handles at least one request, plus a per-request fee; CPU is throttled outside requests. **Instance-based**:
  pay for each instance's whole lifetime, with CPU always on. A **job** bills its tasks' running time.
- **Mental model:** request spikes on a timeline. VM = the whole rectangle; request-based = area under the
  spikes (overlapping requests on one instance billed once); instance-based = area under the "instance alive"
  step function; job = one bar from start to exit.
- **Misconception:** "Serverless is always cheaper." At steady high load an always-on instance or VM can be.
  It wins for spiky, idle-heavy traffic such as a class demo — and slide 11/14's "pay only while your code
  runs" holds for compute only with these defaults (min 0, request-based).

### 3.4 Cloud Run functions vs Cloud Run services: a function is a container you did not write ★ ANIMATE
- **Explanation:** Part 1 hands over **source + `requirements.txt` + an entry-point name** (README.md:150-151:
  "the Python function the serving framework should call, not the filename or service name"). The build
  "receives your source, uses Google's build tooling to assemble a Python environment, installs the
  requirements, configures the Functions Framework, and publishes an application image in Artifact Registry"
  (README.md:212-215). The gcloud equivalent makes that explicit: `gcloud run deploy translate-function
  --source=tutorial/function --function=hello_http --base-image=python312` (README.md:195-198). The result is
  an ordinary **Cloud Run service** whose process is functions-framework with `--target hello_http`
  (`_cli.py:24`: `--target`, env `FUNCTION_TARGET`). Part 2 hands over a finished image whose own `CMD` starts
  a server.
- **Mental model:**

  | | Part 1: Cloud Run function | Part 2: Cloud Run service from an image |
  |---|---|---|
  | You provide | `main.py` + `requirements.txt` + entry point `hello_http` | image `cgumb/ac215-translation-demo:…` |
  | Who builds | Cloud Build + buildpacks, at deploy | already built (`tutorial/app/Dockerfile`), no build at deploy (README.md:314-315) |
  | Server process | functions-framework 3.10.2 → gunicorn | `python -m translation_demo serve` → gunicorn (`__main__.py:22-26`) |
  | Runtime | "Python 3.12" picked in the console (README.md:104) / `--base-image=python312` | `python:3.12-slim-bookworm` (`Dockerfile:1`) |
  | Typical unit | one handler, query-string in, text out | a whole app: HTML page + two JSON routes (`web.py:13-54`) |
- **Analogy:** send a recipe and they cook it (function) vs bring your own food truck and they give you a
  parking spot and customers (service).
- **Misconception:** "Cloud Functions and Cloud Run are different products." The README creates the function
  from **Cloud Run → Services → Write a function** (README.md:99-101); what was "Cloud Functions (2nd gen)"
  is now "Cloud Run functions", served by Cloud Run. The slides still say "Cloud Function" and link
  `console.cloud.google.com/functions` (slide 12).

### 3.5 The container contract: `$PORT`, `0.0.0.0`, amd64, no local state ★ ANIMATE
- **Explanation:** a Cloud Run service container must listen for HTTP on **all interfaces** at the port in
  the **`PORT`** env var (8080 by default), be built for **linux/amd64**, and not rely on local state. Both
  servers in this tutorial honour it:
  - function: `@click.option("--host", envvar="HOST", type=click.STRING, default="0.0.0.0")` and
    `@click.option("--port", envvar="PORT", type=click.INT, default=8080)` (functions-framework 3.10.2,
    `_cli.py:32-33`);
  - web app: `port = int(os.environ.get("PORT", "8080"))` then `gunicorn --bind 0.0.0.0:{port}`
    (`__main__.py:23-24`); the image also sets `ENV … PORT=8080` (`Dockerfile:2`).
  README.md:284-287 has you verify **Container port `8080`** in the console. `EXPOSE 8080` (`Dockerfile:11`)
  is documentation only; Cloud Run uses its container-port setting.
- **Mental model:** Cloud Run hands the container an envelope `PORT=8080`, then knocks on that port from
  outside; nobody answers → the revision never becomes ready.
- **Misconception:** "`-p 8086:8080` tells Cloud Run the port." No: `-p` maps *your laptop's* 8086 to the
  container's 8080 (README.md:246-251, Lecture 4's `port_toy`, which reads `PORT` the same way at
  `port_toy/gateway/gateway.py:51`). Cloud Run sets `PORT` and connects to it.

### 3.6 Images, registries, tags vs digests
- **Explanation:** an image is named `registry/repo:tag` (Docker Hub implied for `cgumb/…`). A **tag** is a
  movable label; a **digest** (`sha256:…`) is the immutable content hash. The README pastes the **tag**
  (README.md:276-278) and prints the **digest** at the end (README.md:1066-1070: "The public image's Linux
  AMD64 digest is: `sha256:c17b6db0…`"); the optional practice-stack script deploys by digest because "a tag
  can change later" (`docs/lifecycle.md:63-67`). A Cloud Run revision records the digest it resolved at
  deploy time.
- **Artifact Registry** is GCP's own registry; Part 1's build silently stores its image there
  (README.md:214-215, 1026). Lecture 13 already pulled Google's prebuilt training images from it
  (`model-training/cli.sh:31`, `us-docker.pkg.dev/vertex-ai/training/…`).
- **Mental model / analogy:** a tag is a sticky note on a box, the digest the box's serial number; "the
  latest edition" vs the ISBN.
- **Misconception:** "If the image owner pushes a new build under the same tag, my service changes." Not
  until you deploy a new revision. And one image, two programs: Parts 2–4 run the *same* image; only the
  startup command differs (3.8).

### 3.7 Two IAM questions: who may *call* the app vs what the app may *access* ★ ANIMATE
- **Explanation:** README.md:361-362: "Two permissions questions are separate: **who may call our public
  app**, and **what the running app may access**. A service account answers the second one."
  - **Invocation:** "Allow public access" (README.md:105, 281) lets anyone call the URL. The gcloud
    equivalents use `--no-invoker-iam-check` (README.md:198, 323), which `docs/lifecycle.md:78-79` says
    matches the console's **Allow public access**: the Cloud Run invoker IAM check is switched off (older
    tutorials did this by granting `roles/run.invoker` to `allUsers`).
  - **Runtime identity:** the service account attached under **Security** (README.md:437-439; gcloud
    `--service-account`, README.md:491). Client libraries find it through ADC (from the metadata server) — "You
    do not need to create or download a key" (README.md:380).
  - **Deploy-time permission:** attaching an account needs `iam.serviceAccounts.actAs` (**Service Account
    User**) on it — your permission, separate from the account's runtime roles (README.md:422-427, 432-434).
  - **Least privilege per workload:** the web account gets no Storage role because its audio "goes straight to
    the browser" (README.md:689-690); the job account gets read on the input bucket only and create on the
    output bucket only (README.md:683-688).
- **Mental model:** two badges: a visitor pass at the front door (invocation) and an employee badge the code
  wears when it goes out (service account). Plus a third, yours: the right to pin a badge on someone.
- **Misconception:** "Public means it can call Agent Platform" — or the reverse. Independent. And
  **Service Usage Consumer** is not decoration: `speech.py:102-105` sends the project as the **quota
  project**, which needs `serviceusage.services.use` (README.md:375-376: "the second permits API
  quota/billing").

### 3.8 Services vs jobs; command vs arguments ★ ANIMATE
- **Explanation:** README.md:582-585: a person waits for an interactive request; a program that should "read
  its input, translate it, generate speech, save the files, and exit" is a **job**, not "an HTTP service
  waiting for requests". A job has no URL and no port; it runs N tasks (here 1, README.md:745) and an
  execution succeeds when every task exits 0.
  - The image's default is the web server: `CMD ["python","-m","translation_demo","serve"]` (`Dockerfile:12`),
    no ENTRYPOINT. In Cloud Run, **Container command** replaces the image's ENTRYPOINT and **Container
    arguments** replace its CMD. The job sets command `python` (README.md:746-748: "This replaces the image's
    web-server command") and eleven separate arguments (README.md:749-766), so the task runs
    `python -m translation_demo batch --input-uri … --src en --dest fr --output-uri …`.
  - Arguments are **individual chips** (README.md:750-753): one value per chip; Cloud Run passes each chip as
    one argv element, with no shell in between.
  - `gcloud run jobs execute … --args=…` replaces the **whole** argument list for that execution only; the
    job's saved defaults still point at the first French example (README.md:954-956).
  - Exit status is truthful: any failure prints `Batch failed: …` to stderr and `raise SystemExit(1)`
    (`__main__.py:58-61`, comment: "A failing job must exit unsuccessfully so execution status is truthful").
- **Mental model:** a service is a shop with opening hours; a job is a one-off delivery that ends with a
  receipt (`manifest.json`).
- **Misconception:** "A job is a service that happens to stop." If you leave the image's command alone, the
  task starts gunicorn and **never exits** until the 5-minute task timeout fails it (README.md:1044: "Job
  starts a server instead of finishing → Command `python` and separate batch arguments").

### 3.9 Application Default Credentials and impersonation (local development)
- **Explanation:** README.md:506-514: develop locally against the real API without publishing an image per
  edit; ADC "lets the same code discover credentials locally and on Cloud Run". To test *the runtime
  account's* permissions locally, **impersonate** it: you sign in as yourself and obtain short-lived tokens as
  the account (needs **Service Account Token Creator** on it, README.md:519-524), so no private key is
  downloaded. Commands: `gcloud auth application-default login --impersonate-service-account="$WEB_EMAIL"`
  and `gcloud auth application-default set-quota-project "$PROJECT_ID"` (README.md:547-548).
- **Contrast with L3/L10:** `mega-pipeline` handed students a JSON key file for `secrets/`
  (`mega-pipeline/README.md:97-99`, `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json` at
  README.md:195). L14 removes the key: attached identity in the cloud, impersonated ADC on the laptop.
- **Misconception:** "`gcloud auth login` is enough." That logs in the CLI; the app reads ADC, a separate
  file set up by `gcloud auth application-default login` (README.md:86-87, `tutorial/app/README.md:100-101`).
  The ADC file is still a credential: keep it out of Git and images (README.md:552-553).

### 3.10 Durable outputs from a finite job: unique attempt folders and a completion marker
- **Explanation:** each task writes under `<output-uri>/<uuid4 hex>/` (`storage.py:37-38`), uploads
  `translated.txt` and `speech.wav` with `if_generation_match=0` (create only, never overwrite;
  `storage.py:41-47`), then writes `manifest.json` with `"status": "complete"` **last** (`storage.py:48-55`).
  README.md:887-897: `run-001` is your chosen prefix, not an auto-numbered directory; re-executing creates a
  new attempt folder; partial files without a manifest "do not establish success"; retries can duplicate paid
  work. The helper only reports success after finding a complete manifest (`run_job.py:66-72`).
- **Why Object *Creator* suffices:** the job never reads or overwrites output; create-only uploads need just
  `storage.objects.create`. It cannot even list its own results — you read them with your identity
  (README.md:692-693).

---

## 4. Step-by-step walkthrough

> Convention: **[README]** steps are quoted from `46cc62f` in README order; **[added]** steps are not in the
> README. Console clicks cannot be captured here (no GCP credentials): the video draws them as `illustration`
> with the README's field values; outputs come only from captures or from what the README records.

**Step 0 — Before you begin [README.md:26-89]**
- Select your course project and check its **project ID** (28-31); confirm billing and permissions (32-34);
  choose the region — Toronto `northamerica-northeast2`; speech later uses `us-central1` (35-37); clone the
  repo and work from its root (38-41). Fill the worksheet (46-55). Note the image (58-60).
- Optional, for every gcloud box: the **Terminal setup** block (73-82, quoted in §2).
- [added] `git clone https://github.com/dlops-io/serverless-deployment.git && cd serverless-deployment && git log -1 --format='%h %ci'`
  → `46cc62f 2026-10-22 09:26:24 -0400` at the time of recording.

**Step 1 — Part 1.1: create the function [README.md:97-122]**
1. Console **Cloud Run → Services → Write a function** (opens **Create service**; on a narrow window under
   **More actions**) (99-101).
2. Enable required APIs if prompted (102).
3. **Service name** `translate-function`, your region (103).
4. **Runtime** **Python 3.12** (104).
5. **Authentication** → **Allow public access** → **Create** (105-106).
6. Wait; open the **Source** editor; the initial service may contain sample code (107-109).
- Under the hood: a Cloud Run service is created from Google's template and built once.
- GIF `images/console/function-setup.gif` (111-122) — "real screenshots" with added pointer rings; API
  enablement "conditional".

**Step 2 — Part 1.2: supply the code and dependencies [README.md:124-152]**
1. **Edit source** if read-only; replace `main.py` with `tutorial/function/main.py` (126-140):
   ```python
   import functions_framework
   from googletrans import Translator

   @functions_framework.http
   def hello_http(request):
       text = request.args.get("text", "Welcome to AC215")
       source = request.args.get("src", "en")
       destination = request.args.get("dest", "es")
       return Translator().translate(text, src=source, dest=destination).text
   ```
2. Replace `requirements.txt` (142-148):
   ```text
   functions-framework==3.10.2
   googletrans==4.0.0rc1
   ```
3. **Function entry point** = `hello_http` (150-151).
4. **Save and redeploy**; wait for the revision to become ready (152).
- Under the hood: the build installs the two requirements at build time and configures functions-framework to
  call `hello_http` (212-216).

**Step 3 — Part 1.3: call the endpoint [README.md:154-233]**
1. Copy the **URL** from **service details** (not the build details page) (156-157).
2. Open it with no arguments → the default `"Welcome to AC215"` translated English → Spanish (158-159).
3. Append `?text=Good%20afternoon%20everyone&src=en&dest=fr` to **your** URL (160-164).
4. Try `dest=el`, `dest=hi`; Simplified Chinese is `dest=zh-cn` (166-167).
5. **Observability → Logs**: find the requests, confirm HTTP **200** (168-169).
- Checkpoint (171-173): same endpoint, different inputs, no redeploy; `?` starts the query string, `&`
  separates parameters; `src`/`dest` are languages, not regions.
- Recorded result (README.md:180-184): the French request returned **Bonjour à tous** with HTTP **200** in the
  request log.
- gcloud alternative (194-205):
  ```bash
  gcloud run deploy translate-function \
    --project="$PROJECT_ID" --region="$REGION" \
    --source=tutorial/function --function=hello_http --base-image=python312 \
    --no-invoker-iam-check

  FUNCTION_URL=$(gcloud run services describe translate-function \
    --project="$PROJECT_ID" --region="$REGION" --format='value(status.url)')
  curl --get "$FUNCTION_URL" \
    --data-urlencode 'text=Good afternoon everyone' \
    --data-urlencode 'src=en' --data-urlencode 'dest=fr'
  ```
- "More detail" box (210-233): build vs request time, cold starts, googletrans is an external provider —
  "inspect logs rather than treating a completed build as proof that translation worked" (228-231).
- If it fails: build log (requirements typo, entry point ≠ `def` name → functions-framework raises
  `File /workspace/main.py is expected to contain a function named '<target>'. Found: … instead`,
  `_function_registry.py:57-61`; the `/workspace` path is the buildpack's app directory [added]); `403` →
  public access not set or blocked by an org policy; `500` → googletrans failure in Logs (README.md:1037-1039).

**Step 4 — Part 2.1: try the prebuilt app locally [README.md:242-268]**
1. With Docker running (244-249):
   ```bash
   docker run --rm -p 8086:8080 \
     cgumb/ac215-translation-demo:lecture14-agent-platform-20261022
   ```
2. Open http://localhost:8086 (251).
3. Type a sentence, pick languages, **Translate**; the translation appears in the other box (252-253).
4. **Play audio** is disabled (label "Play audio · enable in part 3", `index.html:51`); stop the container
   with **Ctrl+C** (254-255).
- Under the hood: `CMD` → `python -m translation_demo serve` → `os.execvp` replaces Python with gunicorn bound to
  `0.0.0.0:8080`, 1 worker, 4 threads, 90 s worker timeout (`__main__.py:22-26`). Because gunicorn becomes
  PID 1, Ctrl+C (forwarded by `docker run`) stops it cleanly. The page (`GET /`) sends `POST /api/translate`
  with a JSON body `{text, src, dest}` (`index.html:76-80`), not a query string as in Part 1
  (`tutorial/app/README.md:16-18`).
- [added] extra checks for captures: `curl -s localhost:8086 | head`, `curl -s -X POST localhost:8086/api/translate
  -H 'Content-Type: application/json' -d '{"text":"Good afternoon everyone","src":"en","dest":"fr"}'`
  (expected JSON `{"dest":"fr","src":"en","text":"…"}`, `web.py:38`), and the same against `/api/speech`
  (expected 503 `{"error":"Speech is disabled. …"}`, `speech.py:75-76` + `web.py:50-51`).

**Step 5 — Part 2.2: deploy the same image [README.md:270-353]**
1. **Cloud Run → Services → Deploy container** (272).
2. **Deploy one revision from an existing container image**; **Container image URL** = the image (273-278).
3. **Service name** `translation-demo`, your region (280).
4. **Allow public access**, **Request-based** billing (281).
5. **Auto scaling**, **Minimum number of instances** `0`, **Maximum number of instances** `2` (282-283).
6. **Containers, Networking, Security → Containers → Edit Container → Settings**: verify **Container port**
   `8080`, **Memory** **512 MiB**, **CPU** `1`; leave command and arguments; **Done** (284-287).
7. **Requests**: **Request timeout** `120` s, **Maximum concurrent requests per instance** `4`; no speech
   variables yet (288-290).
8. **Create**, wait for ready (291).
9. Open the **URL**, repeat the translation; speech still disabled (292-293).
10. **Revision History**, then **Observability → Logs**: "A revision is a deployed version of the service's
    image and configuration" (294-296).
- Checkpoint (314-315): someone else can use the app; "this deployment did not need to build our source".
- gcloud alternative (320-325):
  ```bash
  gcloud run deploy "$WEB_SERVICE" \
    --project="$PROJECT_ID" --region="$REGION" --image="$IMAGE" \
    --no-invoker-iam-check --min-instances=0 --max-instances=2 \
    --cpu=1 --memory=512Mi --concurrency=4 --timeout=120
  ```
  Re-running the tutorial on a service that already has speech: remove `ENABLE_SPEECH` (327-329).
- "More detail" (334-351): why a container (packaged, tested app; control over system libraries and startup);
  the browser keeps the page between requests, so a web UI can still scale to zero; the app is the
  **application backend**: browser → our app → external translation provider → our app → browser.
- Note [added]: concurrency `4` equals the gunicorn thread count (`__main__.py:25`), so Cloud Run never sends
  an instance more requests than it has threads.

**Step 6 — Part 3.1: enable the API and create the app's identity [README.md:364-428]**
1. **APIs & Services → Library → Agent Platform API** → enable if needed (366-367; already-enabled page:
   386-395).
2. **IAM & Admin → Service Accounts → Create service account** (368).
3. Name `Translation demo runtime`, ID `translation-demo-runtime`; email
   `translation-demo-runtime@YOUR_PROJECT_ID.iam.gserviceaccount.com`; optional description "Calls Gemini
   speech for the translation app" (369-373).
4. **Create and continue** → **Permissions (optional)**: **Agent Platform User**, **Add another role →
   Service Usage Consumer** → **Continue** → leave **Service account users role** and **Service account
   admins role** empty → **Done** (374-379).
5. Record the email; no key (380).
- gcloud alternative (411-420):
  ```bash
  gcloud services enable aiplatform.googleapis.com --project="$PROJECT_ID"
  gcloud iam service-accounts create translation-demo-runtime \
    --project="$PROJECT_ID" --display-name='Translation demo runtime'
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$WEB_EMAIL" --role=roles/aiplatform.user --condition=None
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$WEB_EMAIL" \
    --role=roles/serviceusage.serviceUsageConsumer --condition=None
  ```

**Step 7 — Part 3.2: attach the identity and enable speech [README.md:430-502]**
- Prerequisite: your identity needs **Service Account User** on the runtime account (432-434).
1. **Cloud Run → Services → translation-demo** (436).
2. **Security** tab → **Service account** → the runtime account; check its email (437-439).
3. **Containers → Variables & Secrets → Environment variables**: fill **Name 1 / Value 1**, then **Add
   variable** twice (440-448): `ENABLE_SPEECH`=`true`, `GOOGLE_CLOUD_PROJECT`=your project ID,
   `GOOGLE_CLOUD_LOCATION`=`us-central1`.
4. **View diff & redeploy** → **Review changes to be deployed**, keep **Serve this revision immediately** →
   **Deploy changes** (450-452).
5. Wait for update, revision, traffic (453-454).
6. Reload the URL, translate English → French, **Play audio**; replay with the browser's controls (455-456).
7. On failure: read the UI message and the service **Logs** before changing permissions (457-458).
- Checkpoint (460-462): the app calls an authenticated API as its attached account; audio returns to the
  browser; no bucket in this part.
- gcloud alternative (488-493):
  ```bash
  gcloud run services update "$WEB_SERVICE" \
    --project="$PROJECT_ID" --region="$REGION" \
    --service-account="$WEB_EMAIL" \
    --update-env-vars="ENABLE_SPEECH=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1"
  ```
  Service region ≠ model location; defaults `gemini-2.5-flash-tts`, voice `Kore` (495-498).
- Under the hood: `POST /api/speech` with `{text, dest}` (`index.html:95-97`) → `synthesize()` checks
  `ENABLE_SPEECH`, ≤ 4,000 UTF-8 bytes, a supported language (`speech.py:75-82`) → ADC token
  (`speech.py:102-105`) → `POST https://us-central1-aiplatform.googleapis.com/v1beta1/projects/<project>/locations/us-central1/publishers/google/models/gemini-2.5-flash-tts:generateContent`
  (`speech.py:91-92`) → base64 PCM (mono, 24 kHz, 16-bit) wrapped as WAV (`speech.py:38-48`) → `audio/wav`
  back to the browser (`web.py:54`). The page's flag `speech_enabled` is rendered at page load
  (`web.py:15`), hence "reload".
- Failure mapping (`speech.py:108-119` → `web.py:48-53`): no credentials / 401 / 403 / 404 →
  `SpeechConfigurationError` → HTTP **503** with e.g. "Agent Platform access denied. Check the caller
  identity, enabled API, inference permissions, and quota project."; 429 / other errors → **502**.

**Step 8 — Part 3.3: how would you develop this locally? [README.md:504-578] (collapsed, optional)**
1. Grant your user **Service Account Token Creator** on `translation-demo-runtime` (**Principals with access →
   Grant access**; replace any preselected role, do not leave Service Account Admin) and enable the **IAM
   Service Account Credentials API** (519-525).
2. Commands (540-549):
   ```bash
   export DEVELOPER_EMAIL=YOUR_GOOGLE_ACCOUNT_EMAIL
   gcloud services enable iamcredentials.googleapis.com --project="$PROJECT_ID"
   gcloud iam service-accounts add-iam-policy-binding "$WEB_EMAIL" \
     --project="$PROJECT_ID" --member="user:$DEVELOPER_EMAIL" \
     --role=roles/iam.serviceAccountTokenCreator --condition=None

   gcloud auth application-default login --impersonate-service-account="$WEB_EMAIL"
   gcloud auth application-default set-quota-project "$PROJECT_ID"
   ```
   Browser sign-in; the ADC file stays local; you may need **Service Usage Consumer** yourself in a restricted
   project (551-555).
3. Run the app with uv (558-564):
   ```bash
   cd tutorial/app
   uv sync --frozen
   ENABLE_SPEECH=true GOOGLE_CLOUD_PROJECT="$PROJECT_ID" \
     GOOGLE_CLOUD_LOCATION=us-central1 PORT=8086 \
     uv run python -m translation_demo serve
   ```
   Open http://localhost:8086; edit and restart locally; `cd ../..` afterwards (566-568). Containers with
   mounted ADC, rootless Docker, builds: `tutorial/app/README.md` (570-572, its lines 168-191).
- Capturable here [added]: `uv sync --frozen` and `serve` with speech **off**, and the offline checks in
  `tutorial/app/README.md:22-27` (`uv run python -m unittest discover -s tests -v`; `batch --plan`), inside a
  container. The impersonated login and the speech call need GCP credentials and are not capturable.

**Step 9 — Part 4.1: create your input and output buckets [README.md:593-675]**
1. **Cloud Storage → Buckets → Create** (595).
2. Globally unique input bucket name, e.g. project ID + `-translation-input`; **Continue** (596-597).
3. Wizard (598-613): **Region** = your region; **Standard** class, hierarchical namespace unchecked; **Enforce
   public access prevention** checked and **Uniform** access; soft delete with default retention, no object
   versioning, no retention policy; **Create** → **Confirm** in "Public access will be prevented"; check the
   **Configuration** tab: region, Standard, **Public access: Not public**.
4. Repeat for the output bucket (614).
5. Save `tutorial/app/examples/passage.txt` locally; in the input bucket **Objects → Create folder `run-001`**,
   open it, **Upload → Upload files** → `passage.txt` (615-618).
6. Open `passage.txt` → **Object details → Live object → Cloud Storage URI** → copy:
   `gs://YOUR_INPUT_BUCKET/run-001/passage.txt` (619-621).
- The sample passage (`examples/passage.txt:1-4`) is a four-line poem ("The evening rain has passed. …").
- gcloud alternative (660-673):
  ```bash
  export INPUT_BUCKET=YOUR_GLOBALLY_UNIQUE_INPUT_BUCKET
  export OUTPUT_BUCKET=YOUR_GLOBALLY_UNIQUE_OUTPUT_BUCKET

  gcloud services enable storage.googleapis.com --project="$PROJECT_ID"
  gcloud storage buckets create "gs://$INPUT_BUCKET" \
    --project="$PROJECT_ID" --location="$REGION" \
    --uniform-bucket-level-access --public-access-prevention
  gcloud storage buckets create "gs://$OUTPUT_BUCKET" \
    --project="$PROJECT_ID" --location="$REGION" \
    --uniform-bucket-level-access --public-access-prevention
  gcloud storage cp tutorial/app/examples/passage.txt \
    "gs://$INPUT_BUCKET/run-001/passage.txt" --project="$PROJECT_ID"
  ```

**Step 10 — Part 4.2: a separate identity for the job [README.md:677-729]**
1. Create service account ID `translation-audio-job` (679-680).
2. Grant **Agent Platform User** and **Service Usage Consumer** on the project; record the email (681-682).
3. **Input bucket → Permissions → Grant access**: job email, **Storage Object Viewer**, **Save** (683-685).
4. **Output bucket → Permissions → Grant access**: job email, **Storage Object Creator**, **Save** (686-688).
5. Leave the web account unchanged (689-690).
- Checkpoint (692-694): the job can read input, call the model and create output; your own identity needs
  separate permission to upload, execute and read results.
- gcloud alternative (710-722):
  ```bash
  gcloud iam service-accounts create translation-audio-job \
    --project="$PROJECT_ID" --display-name='Translation audio job'
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$JOB_EMAIL" --role=roles/aiplatform.user --condition=None
  gcloud projects add-iam-policy-binding "$PROJECT_ID" \
    --member="serviceAccount:$JOB_EMAIL" \
    --role=roles/serviceusage.serviceUsageConsumer --condition=None
  gcloud storage buckets add-iam-policy-binding "gs://$INPUT_BUCKET" \
    --member="serviceAccount:$JOB_EMAIL" --role=roles/storage.objectViewer
  gcloud storage buckets add-iam-policy-binding "gs://$OUTPUT_BUCKET" \
    --member="serviceAccount:$JOB_EMAIL" --role=roles/storage.objectCreator
  ```
  Restricted projects: Service Account User to attach; **Cloud Run Jobs Executor With Overrides** for
  `run.jobs.runWithOverrides` (724-727).

**Step 11 — Part 4.3: create the job [README.md:731-824]**
- Prerequisite: Service Account User on the job account (733-735).
1. **Cloud Run → Jobs → Deploy container** (page title **Create job**) (737-738).
2. Same image URL (739-743).
3. **Job name** `translation-audio`, region, **1 task** (745).
4. **Containers, Connections, Security → Containers** (expand the row's chevron if collapsed) → **Edit
   Container → Settings** → **Container command** `python`, press **Enter** to make a chip (746-748).
5. **Container arguments**, one chip each, buckets replaced (749-766):
   `-m` · `translation_demo` · `batch` · `--input-uri` · `gs://YOUR_INPUT_BUCKET/run-001/passage.txt` · `--src` ·
   `en` · `--dest` · `fr` · `--output-uri` · `gs://YOUR_OUTPUT_BUCKET/run-001/`. "Do not paste the whole block
   into one argument field."
6. **Variables & Secrets**: the same three variables; **Done** (768-776).
7. **Task capacity**: **Task timeout** `5` **minute**, **Number of retries per failed task** `0`; keep
   **Memory** 512 MiB, **CPU** 1, **Number of tasks** 1 (778-780).
8. **Security** → **Service account** `translation-audio-job@YOUR_PROJECT_ID.iam.gserviceaccount.com`, chosen by
   its email (the selector shows the display name) (781-783).
9. Leave **Execute job immediately** unchecked → **Create** (784-785).
- gcloud alternative (815-822):
  ```bash
  gcloud run jobs create "$JOB_NAME" \
    --project="$PROJECT_ID" --region="$REGION" --image="$IMAGE" \
    --service-account="$JOB_EMAIL" --command=python \
    --args="-m,translation_demo,batch,--input-uri,gs://$INPUT_BUCKET/run-001/passage.txt,--src,en,--dest,fr,--output-uri,gs://$OUTPUT_BUCKET/run-001/" \
    --set-env-vars="ENABLE_SPEECH=true,GOOGLE_CLOUD_PROJECT=$PROJECT_ID,GOOGLE_CLOUD_LOCATION=us-central1" \
    --tasks=1 --max-retries=0 --task-timeout=300 --memory=512Mi --cpu=1
  ```
- [added] capturable rehearsal of the same argv locally, offline (`tutorial/app/README.md:213-218`):
  `docker run --rm cgumb/ac215-translation-demo:lecture14-agent-platform-20261022 python -m translation_demo batch --plan --text-file examples/passage.txt --src en --dest fr --output-uri gs://YOUR_OUTPUT_BUCKET/fresh-run-prefix`
  → the JSON plan of `__main__.py:42-49` (`"status": "plan_only"`, five steps, `"implemented": true`).

**Step 12 — Part 4.4: execute it and collect the files [README.md:826-907]**
1. **Jobs → translation-audio → Execute** (narrow toolbar: **More actions ⋮**) (828-829).
2. Wait for the green check in **History**; open the execution → **Tasks → View logs**: completion, execution
   ID and the exact `output_uri` (830-833) — the JSON printed by `__main__.py:62`, i.e.
   `output_uri`, `manifest_uri`, `status: complete`, `artifacts`, `execution`, `task_attempt`
   (`storage.py:48-56`). "The job exits; it does not provide a web URL."
3. **Cloud Storage → output bucket → run-001** → the uniquely named attempt folder (834-835).
4. Files (836-842): `translated.txt` (the translated passage), `speech.wav` (its audio), `manifest.json`
   (completion status and output locations).
5. Download icons; for a WAV in a media tab **Play**, then **⋮ → Download** (844-848).
- Checkpoint (850-852): "the task finished, the process stopped, and its files remain in Storage".
- Recorded (README.md:859-860): execution `translation-audio-hq9f5`, attempt folder `run-001/de2f41…/`.
- gcloud alternative (871-877):
  ```bash
  gcloud run jobs execute "$JOB_NAME" \
    --project="$PROJECT_ID" --region="$REGION" --wait
  mkdir -p results
  gcloud storage cp --recursive "gs://$OUTPUT_BUCKET/run-001" ./results \
    --project="$PROJECT_ID"
  ```
  `--wait` waits for completion but does not stream application logs (879-880).
- "More detail" (885-905): prefixes vs folders, create-only uploads, manifest last, retries, limits (5,000
  characters, 20,000-byte object, 4,000 UTF-8 bytes of speech input).

**Step 13 — Part 4.5: submit another passage from the terminal [README.md:909-967]**
- Prerequisite (911-914): you need `run.jobs.run` + `run.jobs.runWithOverrides`, upload on input, read on output.
1. If you used only the console: expand **Terminal setup** and set the bucket variables (921-927):
   ```bash
   export INPUT_BUCKET=YOUR_INPUT_BUCKET
   export OUTPUT_BUCKET=YOUR_OUTPUT_BUCKET
   ```
2. Save a new short UTF-8 `passage.txt` locally and upload it (929-934):
   ```bash
   gcloud storage cp ./passage.txt "gs://$INPUT_BUCKET/run-002/passage.txt" \
     --project="$PROJECT_ID"
   ```
3. Execute the **existing** job with argument overrides (936-943):
   ```bash
   gcloud run jobs execute "$JOB_NAME" \
     --project="$PROJECT_ID" --region="$REGION" \
     --args="-m,translation_demo,batch,--input-uri,gs://$INPUT_BUCKET/run-002/passage.txt,--src,en,--dest,es,--output-uri,gs://$OUTPUT_BUCKET/run-002/" \
     --wait
   ```
4. Download (945-951):
   ```bash
   mkdir -p results
   gcloud storage cp --recursive "gs://$OUTPUT_BUCKET/run-002" ./results \
     --project="$PROJECT_ID"
   ```
- Spanish this time, new input path and output prefix; overrides replace the whole argument list for this
  execution only; use a fresh prefix per submission (953-956). "A remote container cannot read a filename on
  your laptop" (918-919) — hence upload first.

**Step 14 — Part 4.6: the helper [README.md:969-1016]**
```bash
python tutorial/run_job.py ./passage.txt \
  --project="$PROJECT_ID" --region="$REGION" --job="$JOB_NAME" \
  --input-bucket="$INPUT_BUCKET" --output-bucket="$OUTPUT_BUCKET" \
  --src=en --dest=fr --download-dir=./results
```
(README.md:974-979.) It prints each gcloud command (`$ …`, `run_job.py:15-18`), uploads to
`gs://IN/run-<UTC yyyymmdd-HHMMSS>-<12 hex>/passage.txt` (`run_job.py:47-49`), executes with `--args=…
--wait --quiet` (`run_job.py:58-59`), prints `Cloud outputs: …`, downloads, and prints `Downloaded results: …`
only after finding a complete manifest with both files (`run_job.py:60-72`; README.md:981-984, 991-993).
Options (1000-1011): `--dry-run`, `--no-download`, `--help`; bucket **names** without `gs://`; no custom run
name; needs only Python and a signed-in gcloud (stdlib only); on failure it stops and keeps partial files.
- [added] capturable here: `python tutorial/run_job.py tutorial/app/examples/passage.txt --project=YOUR_PROJECT_ID
  --input-bucket=YOUR_INPUT_BUCKET --output-bucket=YOUR_OUTPUT_BUCKET --dry-run` (prints the three commands;
  run it in a container). The real run needs credentials.

**Step 15 — Clean up [README.md:1018-1028]**
1. Download results you want to keep. 2. Delete the function and web service, then the job (check names
against the worksheet). 3. Delete input/output objects and buckets; remove the two service accounts once no
longer attached. 4. Remove the function's unused Artifact Registry image; keep unrelated course resources and
the shared public image.
- [added] also: the function's source/build artifacts (`docs/lifecycle.md:205-210`), and soft-deleted bucket
  data stays billable for its retention period (`docs/lifecycle.md:176-177`). Optional scripted practice stack
  and teardown: `tutorial/spin_up.py` / `tutorial/tear_down.py`, dry-run unless `--apply`
  (`docs/lifecycle.md:46-61, 149-166`; README.md:1060-1064).

**Step 16 — Troubleshooting table [README.md:1033-1053]** — ten symptom → check rows, e.g. "Play audio is
disabled → `ENABLE_SPEECH=true`, deployed revision, and page reload"; "Job starts a server instead of finishing
→ Command `python` and separate batch arguments"; "Helper cannot launch with overrides → Your gcloud caller's
override permission, not the runtime account's Storage role".

---

## 5. Code tour

```
serverless-deployment/                      (main @ 46cc62f)
|- README.md                     the four-part console-first tutorial (1,079 lines)
|- images/console/*.gif, *.png   annotated console recordings the README embeds
|- docs/lifecycle.md             optional scripted practice stack + teardown
|- tutorial/
|  |- function/main.py           Part 1 handler hello_http (12 lines)
|  |- function/requirements.txt  functions-framework==3.10.2, googletrans==4.0.0rc1
|  |- app/                       the image of Parts 2-4 (package translation_demo)
|  |  |- Dockerfile, .dockerignore, pyproject.toml, requirements.lock, uv.lock
|  |  |- translation_demo/__main__.py   CLI: serve | batch
|  |  |- translation_demo/web.py        Flask: GET /, POST /api/translate, POST /api/speech
|  |  |- translation_demo/translation.py  validate + googletrans
|  |  |- translation_demo/speech.py   Gemini TTS over REST with ADC -> WAV
|  |  |- translation_demo/storage.py  gs:// read, create-only writes, manifest
|  |  |- translation_demo/templates/index.html   the UI
|  |  |- examples/passage.txt, tests/, README.md (development guide)
|  |- run_job.py                 Part 4.6 helper (stdlib + gcloud)
|  |- spin_up.py, tear_down.py, lifecycle/   scripted stack (docs/lifecycle.md)
|  |- gif_steps.json, label_gifs.py, tests/  recording + helper tests
|- main.py cli.py Dockerfile docker-entrypoint.sh docker-shell.sh pyproject.toml uv.lock
|                                2025 files, unchanged since 4eaf343, not used by the README
`- .gitignore
```

**`tutorial/function/main.py:7-12`** — quoted in §4 Step 2.
- `@functions_framework.http` registers `hello_http` as an HTTP function; functions-framework later finds it by
  the name given as target (`_cli.py:24`, `_function_registry.py:51-61`).
- `request` is a Flask request; `request.args.get(name, default)` reads the query string with a default
  (`"Welcome to AC215"`, `"en"`, `"es"`).
- `Translator()` per request; `.translate(...)` is a blocking call to googletrans' unofficial endpoint (sync API
  of 4.0.0rc1); no `try/except`, so a provider failure is an HTTP 500. Returning a `str` → 200 text body.

**`tutorial/app/Dockerfile:1-12`**
```dockerfile
FROM python:3.12-slim-bookworm
ENV PYTHONUNBUFFERED=1 PYTHONDONTWRITEBYTECODE=1 PORT=8080
WORKDIR /app
COPY requirements.lock ./
RUN pip install --no-cache-dir -r requirements.lock
COPY pyproject.toml ./
COPY translation_demo ./translation_demo
COPY examples ./examples
RUN pip install --no-cache-dir --no-deps . && useradd --uid 1000 --create-home app
USER app
EXPOSE 8080
CMD ["python", "-m", "translation_demo", "serve"]
```
- Dependencies first (cached layer), then code: a code-only change reuses the `pip install` layer.
- `requirements.lock` is a `uv export` of `uv.lock` (its header, lines 1-2): flask 3.1.3, google-auth 2.62.0,
  google-cloud-storage 3.17.1, googletrans 4.0.0rc1, gunicorn 26.2.0, httpx 0.13.3, requests 2.34.2
  (`requirements.lock:19, 25, 33, 43, 45, 57, 89`).
- Non-root user `app` (uid 1000). `CMD`, no `ENTRYPOINT` — which is why a Cloud Run job can swap the whole
  command line (3.8).
- `.dockerignore:1-7` excludes `.venv`, `__pycache__`, `*.pyc`, `tests`, … at the context root.

**`tutorial/app/translation_demo/__main__.py:9-26`** (CLI and the `serve` branch)
```python
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("serve", help="Start the HTTP service")
    batch = commands.add_parser("batch", help="Translate a passage, generate speech, save outputs, and exit")
    ...
    if args.command == "serve":
        port = int(os.environ.get("PORT", "8080"))
        os.execvp("gunicorn", ["gunicorn", "--bind", f"0.0.0.0:{port}",
                              "--workers", "1", "--threads", "4", "--timeout", "90",
                              "translation_demo.web:create_app()"])
```
- Docstring line 1: "One image, different startup commands: serve or batch."
- `batch` options (lines 14-20): exactly one of `--text-file` / `--input-uri`; `--src` (default `en`),
  `--dest` (default `fr`), required `--output-uri`, `--plan`.
- `os.execvp` replaces the Python process with gunicorn (PID 1 in a container), so signals reach the server
  directly. 1 worker × 4 threads; Part 2 sets Cloud Run concurrency to 4 to match.

**`__main__.py:51-62`** (the `batch` branch)
```python
    try:
        if text is None:
            text = read_text(args.input_uri)
        validate(text, args.src, args.dest)
        translated = translate(text, args.src, args.dest)
        audio, mime_type = synthesize(translated, args.dest)
        result = save_artifacts(args.output_uri, translated, audio, mime_type)
    except Exception as exc:
        # A failing job must exit unsuccessfully so execution status is truthful.
        print("Batch failed: " + str(exc), file=__import__("sys").stderr)
        raise SystemExit(1) from exc
    print(json.dumps(result, indent=2))
```
- Read → validate → translate → speak → save → print, the five steps the `--plan` output lists
  (`__main__.py:46-47`). Before that, `split_uri` checks both URIs (lines 32-40); a bad URI is an argparse
  error (exit 2).

**`translation_demo/web.py:9-38`** — `create_app()`: `MAX_CONTENT_LENGTH` 32 KiB (11); `GET /` renders the
page with `speech_enabled=enabled()` (13-15); `inputs()` requires a JSON object, defaults `src="en"`,
`dest="fr"` (17-25); `POST /api/translate` → 400 on bad input, **502** "The translation provider could not
complete the request." on provider failure, else JSON `{text, src, dest}` (27-38). `POST /api/speech` (40-54):
400 / 503 / 502 by exception type, else WAV with `Cache-Control: no-store`.

**`translation_demo/translation.py:3-34`** — nine languages (`en es fr de el hi ja zh-cn zh-tw`, 3-13);
`validate` rejects empty text, > 5,000 characters, unsupported codes (16-24); `translate` imports
`httpx`/googletrans lazily and sets a 20 s timeout (27-34). Comment line 29: imported "here so offline UI and
contract checks do not load the provider".

**`translation_demo/speech.py:74-124`** — see §4 Step 7. Key lines: `enabled()` accepts `1/true/yes`
(34-35); env defaults (83-86); regional host unless `global` (91); request body asks the model to "Read the
following text aloud, without adding commentary" with `responseModalities: ["AUDIO"]`, a locale from
`LOCALES` (19-23) and `prebuiltVoiceConfig.voiceName` (93-100); ADC with `quota_project_id=project`
(102-105); status mapping (112-119). The module docstring explains the REST call: it "keeps this adapter
independent of googletrans's older httpx pin" (line 4).

**`translation_demo/storage.py:10-56`** — `split_uri` requires `gs://bucket/path`, no `?`/`#` (10-16);
`read_text` checks size ≤ 20,000 bytes and downloads with `if_generation_match` pinned to the inspected
generation (23-30); `save_artifacts` (33-56), see 3.10.

**`tutorial/run_job.py:47-72`** — see §4 Step 14. Configuration values must be plain names (no slashes or
commas) because commas delimit `gcloud --args` (35-39).

**functions-framework 3.10.2 (external)**
- `_cli.py:24` `--target` (env `FUNCTION_TARGET`); `_cli.py:32-33` host `0.0.0.0` / port from `PORT`
  (quoted in 3.5); `_function_registry.py:27` default source `./main.py`; `_function_registry.py:57-61` the
  missing-target message.
- `_http/gunicorn.py:32-41`: gunicorn with `WORKERS` (default 1) × `THREADS` (default `cpu_count × 4`),
  log level `GUNICORN_LOG_LEVEL` (default `"error"`), `CLOUD_RUN_TIMEOUT_SECONDS`. So the function's
  per-instance threads depend on its CPU count, while the web app fixes 4.

**Root legacy files (not part of the README):** `main.py` (`translate_http`), `Dockerfile` (uv, `/.venv`),
`docker-entrypoint.sh` (`uv run functions-framework --target translate_http`), `docker-shell.sh` (builds
`simple-translate` for `linux/amd64/v2`). Identical to `4eaf343`; mention once, do not teach.

---

## 6. Gotchas and common errors

1. **Wrong entry point (Part 1).** `requirements` fine, build or start fails: functions-framework cannot find
   the configured target (`_function_registry.py:57-61`). Fix: the **Function entry point** must equal the
   `def` name, `hello_http` (README.md:150-151, 1038).
2. **Copying the newer googletrans.** `googletrans==4.0.2` (used by `simple-translate/pyproject.toml:9`) is
   async; with the sync handler, `.translate(...)` returns a coroutine and `.text` raises
   `AttributeError: 'coroutine' object has no attribute 'text'`. Keep `googletrans==4.0.0rc1`
   (`tutorial/function/requirements.txt:2`, `tutorial/app/pyproject.toml:10`).
3. **Translation fails while everything is "green".** googletrans scrapes an unofficial Google endpoint that
   can rate-limit or change. Function → HTTP 500; web app → 502 "The translation provider could not complete
   the request." (`web.py:35-37`); job → `Batch failed: …`, exit 1. Check Logs, not the build status
   (README.md:228-231, 1039).
4. **Public access refused.** An organization policy can forbid public endpoints (`docs/lifecycle.md:18-19`);
   the URL then answers 403. Resolve with course staff (README.md:32-34).
5. **Wrong local port.** `docker run --rm -p 8086:8080 …` → open **8086**, not 8080 (README.md:246-251). If 8086
   is taken, change the left number only; the right one is where gunicorn listens (`PORT`, default 8080).
6. **"Play audio" stays disabled.** `ENABLE_SPEECH` missing or not `true/1/yes`, the change not deployed, or
   the page not reloaded — the flag is rendered at page load (`web.py:15`; README.md:1040).
7. **Speech denied (503 in the UI).** Runtime account not attached (the service then runs as the project's
   default compute service account [added]), Agent Platform API off, **Service Usage Consumer** missing (the
   code sends a quota project, `speech.py:104`), or a wrong location (README.md:1041). Message:
   "Agent Platform access denied. Check the caller identity, enabled API, inference permissions, and quota
   project." (`speech.py:112-113`).
8. **Can't attach the service account.** `iam.serviceAccounts.actAs` denied → you need **Service Account
   User** on that account (README.md:422-427, 432-434, 733-735). Its runtime roles don't give *you* anything.
9. **`gcloud auth login` ≠ ADC.** Local speech fails with "Google credentials are unavailable…"
   (`speech.py:108-109`) until `gcloud auth application-default login` (README.md:86-87, 547).
   Impersonation also needs **Token Creator** + the IAM Service Account Credentials API (README.md:519-525).
10. **Job never finishes.** Command left at the image default → gunicorn starts and waits for requests until
    the 5-minute timeout fails the task (README.md:746-748, 1044).
11. **Arguments pasted into one chip.** The whole block becomes a single argv element after `python`;
    Python reads everything after `-m` in that element as one module name and fails with
    `No module named  translation_demo batch …` (exit 1; reproduced with a local `python3`). One value per
    chip (README.md:750-753).
12. **Job can't read or write.** Wrong `gs://` path, or grants on the wrong account/bucket: Object Viewer on
    *input*, Object Creator on *output*, for the **job** account (README.md:683-688, 1043).
13. **Bucket names.** Globally unique; the helper wants **names** without `gs://` (README.md:1002) — it
    rejects anything but `[A-Za-z0-9][A-Za-z0-9._-]*` (`run_job.py:37-39`).
14. **Overrides need your permission.** `gcloud run jobs execute --args=…` needs `run.jobs.runWithOverrides`
    on *your* identity (README.md:911-914, 1046).
15. **Overrides replace all arguments.** Leaving out one flag in `--args` drops it for that execution; the
    saved job still has the French defaults (README.md:954-956).
16. **Empty-looking output.** Each execution writes to a new UUID folder under the prefix; success means a
    `manifest.json` with `"status": "complete"` (README.md:887-897, 1045). Partial folders can exist after a
    failure or retry.
17. **Limits.** > 5,000 characters or > 20,000 bytes of input, or > 4,000 UTF-8 bytes of translated speech
    text, is rejected (README.md:899-902; `translation.py:19-20`, `storage.py:27-28`, `speech.py:79-80`).
18. **Region vs model location.** Cloud Run in Toronto, speech in `us-central1`; `GOOGLE_CLOUD_LOCATION` is the
    model location, not the service region (README.md:495-498).
19. **Surprise charges.** Min instances ≥ 1, instance-based billing, job retries, leftover buckets (soft
    delete), function images (README.md:1018-1028; `docs/lifecycle.md:176-177, 205-210`).

---

## 7. Where this sits in the course

**Earlier lectures**
- **L1–L2 (`simple-translate`):** the same translator on a VM, then in a container; "Delete your VM when you're
  done. A running VM keeps charging even when idle." (`simple-translate/README.md:62`).
- **L3 (`mega-pipeline`):** a service-account **JSON key** downloaded into `secrets/`
  (`mega-pipeline/README.md:95-99`) and `ENV GOOGLE_APPLICATION_CREDENTIALS=secrets/mega-pipeline.json`
  (README.md:195). L14 replaces the key with an attached identity and impersonated ADC.
- **L4 (`port_toy`):** published vs container ports; reading `PORT` from the environment
  (`port_toy/gateway/gateway.py:51`).
- **L10 (`cheese-app-v0`):** secrets kept outside the repo, mounted at `/secrets`
  (`cheese-app-v0/README.md:146`).
- **L13 (`model-training`):** serverless *training*: a Vertex AI custom job with a prebuilt image from
  `us-docker.pkg.dev/vertex-ai/training/…` (`model-training/cli.sh:31-37`). Slide 9: "Training Job (Vertex
  AI) — LAST WEEK".

**What L14 adds:** serverless *serving* and finite work — HTTP functions (functions-framework), the Cloud
Run container contract, scale to zero / cold starts / request-based billing, invocation vs runtime identity,
ADC and impersonation, jobs with durable outputs in Cloud Storage. The README ties it to the Cheese App: the
backend that "accept[s] input, call[s] a model service, and return[s] a result" (README.md:9-10); slides 5–6
place it at the "Model Deploy" stage.

**Next:** L15 (`model-deployment`, `ml-workflow`): Vertex AI endpoints and pipelines — slide 9's "Model
Deployment (Vertex AI) / Pipeline (Vertex AI) — NEXT". L18+: the FastAPI backend that would run as a Cloud Run
service; L22 Kubernetes takes the scaling knobs back.

**What changed since `4eaf343` (for viewers who saw the old README or the slides)**
- Old: function `hello_http` with a cheese default sentence and `functions-framework==3.*`, Python 3.10
  runtime; Cloud Run service from `dlops/simple-translate-http:latest`; bonus job `dlops/simple-translate-gemini`
  with argument `cli.py --text Ready+to+go+home?`.
- New (2026-10-21/22): Python 3.12, `functions-framework==3.10.2`, Toronto region, a web UI image under
  `cgumb/…`, speech via a runtime identity, a job with private buckets, a terminal helper, a clean-up section.
- The old `dlops/*` images are no longer referenced.

---

## 8. Video plan (suggestion)

**Hook:** a broken thing — a Cloud Run job that starts, prints nothing useful and is killed at its 5-minute
timeout, while a "Translate" web page that worked on `localhost` is invisible to a friend. "Same image. Why
does one run forever and the other not exist?" Answered by S12 (command vs arguments) and S07 (deploy the
image).

**Target length:** 25–35 minutes, two parts; ~4,000 narrated words at ~174 wpm. Part 1 = Before you begin,
Part 1 (function), Part 2 (web service). Part 2 = Part 3 (identity, speech, ADC), Part 4 (job), clean-up.

**Scene sketch (14 scenes; README tracker steps in brackets)**
1. **Hook + map** (slides 1–10): the 2×2 of slide 10 (file/container × VM/serverless) with today's two cells;
   the README's four-part table (README.md:12-17).
2. **What serverless means** (slides 8, 11, 14, 16): scale-to-zero strip, request-based meter, cold-start bar.
3. **Before you begin** [step 0]: project ID, region Toronto vs model `us-central1`, worksheet, terminal setup.
4. **Part 1.1–1.2** [steps 1–2]: Write a function form (illustration); `tutorial/function/main.py:7-12`;
   requirements; the entry point thread from field to `def`.
5. **Inside the function** (3.4–3.5): source → Cloud Build → Artifact Registry → revision; functions-framework
   `_cli.py:32-33`; **Ponder 1** (entry point `main` vs `hello_http`: what fails, and where?).
6. **Part 1.3** [step 3]: URL + query string split into `request.args`; `zh-cn`; Logs 200; curl alternative.
7. **Part 2.1** [step 4]: `docker run --rm -p 8086:8080 …` captured; the page; JSON POST vs query string;
   speech disabled.
8. **Part 2.2** [step 5]: Deploy container form (illustration); min 0 / max 2 / concurrency 4 ↔ 4 threads;
   revisions; tag vs digest. **Ponder 2** (6 requests in flight, concurrency 4, max 2: how many instances, and
   what happens to the 9th?).
9. **Two doors** (3.7) [step 6]: who may call vs what the app may access; create `translation-demo-runtime`.
10. **Part 3.2** [step 7]: attach + three env vars + View diff & redeploy; the speech call path; **Ponder 3**
    (Play audio returns "Agent Platform access denied": list three causes).
11. **Part 3.3** [step 8]: ADC + impersonation vs L3's key file; local `uv run … serve`.
12. **Service vs job** (3.8) [steps 9–11]: buckets, job account with scoped roles, command `python` + eleven
    chips; the never-ending job explained. **Ponder 4** (what does the task run if you set only the arguments?).
13. **Part 4.4–4.6** [steps 12–14]: execute, logs JSON, attempt folder + manifest last; `--args` override; the
    helper (dry-run captured).
14. **Clean up + recap** [step 15]: checklist; seven-line recap.

**Recap questions**
1. What do you hand Cloud Run for a function, and for a service? Who builds the image in each case?
2. Which two settings make the meter run while nobody is using the app?
3. Name the two permission questions and which settings answer each in this tutorial.
4. Why does the web account need no Storage role while the job account needs two bucket roles?
5. Why does the job set a **command** and eleven **separate arguments**?
6. How do you know an execution really succeeded?

---

## 9. Exercises

**E1 — Ports, predict then run (hands-on).** Run
`docker run --rm -e PORT=9090 -p 8086:8080 cgumb/ac215-translation-demo:lecture14-agent-platform-20261022`, then
`curl -s localhost:8086`. Predict first. Then fix it without removing `-e PORT=9090`.
- Answer: `serve` binds `0.0.0.0:$PORT` = 9090 (`__main__.py:23-24`); Docker forwards host 8086 → container 8080,
  where nothing listens, so curl gets an empty reply / reset. Fix: `-p 8086:9090`. Cloud Run does the same in
  reverse: it chooses `PORT` and connects to it.

**E2 — The never-ending job (debugging).** A classmate's job created from the same image, with arguments
filled in but **Container command** left empty, fails after exactly five minutes. Another classmate set the
command but left the arguments empty. What does each task run?
- Answer: Cloud Run's *arguments* replace the image's `CMD`; the image has no `ENTRYPOINT` (`Dockerfile:12`).
  Case 1: with no command and no `ENTRYPOINT`, the first argument `-m` becomes the program to execute, so
  the container cannot start (exact Cloud Run error text not recorded here — check the logs). Case 2: `python`
  with no arguments and no terminal reads its program from an empty stdin and should exit 0 at once (a local
  `python3 < /dev/null` does): a "successful" execution that wrote nothing. Only
  command `python` + the eleven arguments runs `batch`; the five-minute case is the one where the image
  default (`serve`) was kept (README.md:1044).

**E3 — Create without read (conceptual).** The job account has only Storage Object **Creator** on the output
bucket. Why does writing three files work, and why can't the job overwrite an earlier result or list the
folder?
- Answer: `storage.py` only creates new objects (`if_generation_match=0`, lines 46 and 54-55) under a fresh
  UUID prefix; create needs `storage.objects.create` only. Overwrite would need delete, list needs
  `storage.objects.list` — neither is in Object Creator. Reading results is your job, with your identity.

**E4 — Entry point mismatch (debugging).** You paste `tutorial/function/main.py` but type `translate` in
**Function entry point**. What message appears in the logs, and where does it come from?
- Answer: `File /workspace/main.py is expected to contain a function named 'translate'. Found: 'hello_http'
  instead` (format `_function_registry.py:57-61`). Fix the field, or rename the `def`.

**E5 — Speech denied (debugging).** After Part 3.2, **Play audio** shows "Agent Platform access denied. Check
the caller identity, enabled API, inference permissions, and quota project." List what you check, in order.
- Answer: which account the revision runs as (Security tab); that account's **Agent Platform User** and
  **Service Usage Consumer** (`speech.py:104` sends a quota project); the Agent Platform API enabled;
  `GOOGLE_CLOUD_PROJECT` = the project with those grants; `GOOGLE_CLOUD_LOCATION` where the model exists. The
  browser sees HTTP 503 (`web.py:50-51`). README.md:457-458, 1041.

**E6 — Concurrency and instances (conceptual).** The web service gets 3 translations per second, each taking
2 s (provider latency). Concurrency 4, max instances 2. How many requests are in flight, how many instances,
and what if traffic doubles?
- Answer: Little's law L = λ·W = 3 × 2 = 6 in flight → ⌈6/4⌉ = 2 instances (the cap). At 6 req/s, 12 in
  flight but only 2 × 4 = 8 slots: the rest wait and some fail (Cloud Run answers 429 when no instance can take
  a request). Raising max instances, or concurrency together with gunicorn threads (`__main__.py:25`), fixes it;
  min instances does not.

**E7 — Two identities and your own (conceptual).** For (a) a teammate who should deploy the job, (b) the
job itself, (c) you testing speech locally as the web account: list principal, role, resource.
- Answer: (a) `user:teammate@…` — Service Account User on `translation-audio-job` (+ Cloud Run deploy rights);
  (b) `serviceAccount:translation-audio-job@PROJECT.iam.gserviceaccount.com` — Agent Platform User + Service
  Usage Consumer on the project, Object Viewer on input, Object Creator on output; (c) your user — Service
  Account Token Creator on `translation-demo-runtime` (+ IAM Service Account Credentials API). None implies
  another.

**E8 — Tag vs digest (hands-on, offline).** `docker pull` the image by tag and by
`cgumb/ac215-translation-demo@sha256:c17b6db09f7402febb582bf327920ec9ca4eee113f5ddefa38e9da5619dbe72e`;
compare `docker images --digests`. Which reference would you put in a deployment you must reproduce in May?
- Answer: same bytes today; only the digest is guaranteed to stay so (README.md:1066-1070,
  `docs/lifecycle.md:65-67`).

---

## 10. Errata and open questions

**Errata (evidence-based, `46cc62f`)**
1. **The course links land on no section.** The tutorials page (fetched 2026-11-04) and slides 12/15 link
   `…/serverless-deployment#running-app-as-cloud-function` and `#running-app-in-cloud-run`. Those headings
   existed at `4eaf343`; at `46cc62f` the headings are "Part 1: Deploy a translation function" … (README.md:91,
   235, 355, 580), so the links open the top of the README. Kind fix: "start at the top; Part 1 is the function,
   Parts 2–4 are Cloud Run".
2. **Slides vs today's README.** Slide 12 opens `console.cloud.google.com/functions` and says "Create a python
   code file"; the README goes **Cloud Run → Services → Write a function** (README.md:99). Slide 10's code
   builds one module-level `Translator()` with the long "…moon's made of cheese" default; the README handler
   creates it per request with default `"Welcome to AC215"` (`tutorial/function/main.py:9-12`). Slide 15's
   "Deploy Docker Image in Cloud Run" holds, but the image is now `cgumb/ac215-translation-demo:…`, and the
   README goes on to identity, speech and a job, which the slides do not show (slide 14 mentions "service or
   job").
3. **The course map pins an older commit.** `MLOps_Learning/course/lectures.yaml:33` and `units.json` say
   `4eaf343`; the course link serves `main` = `46cc62f`, whose README is a different tutorial (28 commits on
   2026-10-21/22).
4. **Unused 2025 files at the repo root.** `main.py`, `cli.py`, `Dockerfile`, `docker-entrypoint.sh`,
   `docker-shell.sh`, `pyproject.toml`, `uv.lock` are unchanged from `4eaf343` and never mentioned, yet
   README.md:38-39 says to work from the repository root — a viewer may build the root `Dockerfile` by
   mistake. The tutorial's image is built from `tutorial/app/` (`tutorial/app/README.md:204-209`).
5. **`.dockerignore` patterns only match at the build-context root.** `__pycache__` and `*.pyc`
   (`tutorial/app/.dockerignore:2-3`) do not exclude `translation_demo/__pycache__/`; the published image
   contains six `translation_demo/__pycache__/*.cpython-312.pyc` files (seen in its `COPY translation_demo`
   layer). Harmless (they match the sources), but `**/__pycache__` is the intended pattern.
6. **Mutable tag in the click path.** Console steps paste the tag (README.md:276-278, 741-743); the digest is
   only at README.md:1068-1070. Deploying by `@sha256:` pins it.
7. **Clean-up stops short.** README.md:1018-1028 covers services, job, buckets, accounts and the function's
   image, but not soft-delete retention (data stays recoverable and billable, `docs/lifecycle.md:176-177`) or
   the build's source archives and logs (`docs/lifecycle.md:205-210`).
8. **"We add your developer access separately in section 3.3"** (README.md:378-379): 3.3 grants Token Creator
   for impersonation; the **Service Account User** needed to attach the account in 3.2 (README.md:432-434) is
   not granted by any console step — fine for project Owners, a blocker in a restricted project.

**Open questions / could not determine here**
- The Ed lesson (slides, any updated instructions) was not accessible.
- Console labels and dialogs ("Write a function", "Save and redeploy", "View diff & redeploy", "Containers,
  Networking, Security" vs "Containers, Connections, Security", the API prompts) are from the README and its
  GIFs, not seen live; no GCP credentials here.
- Whether the console's **Allow public access** disables the invoker IAM check or adds an `allUsers` binding
  in every project: the repo says the former (`docs/lifecycle.md:78-79`; gcloud boxes use
  `--no-invoker-iam-check`).
- The default **Maximum concurrent requests per instance** the console gives a function created by "Write a
  function" (Part 1 does not set it).
- Which service account Part 1 and Part 2 run as before Part 3 (normally the project's default compute
  account) and whether it has broad roles in students' projects; the README does not say.
- Whether googletrans' unofficial endpoint answers from Cloud Run egress IPs on recording day (the README
  warns, README.md:228-231).
- Whether `gemini-2.5-flash-tts` and voice `Kore` stay available in `us-central1` (README.md:496-498: "Model
  availability, language support, and quota depend on the selected model/location").
- Free-tier figures and prices: verify on the pricing page at recording time.
