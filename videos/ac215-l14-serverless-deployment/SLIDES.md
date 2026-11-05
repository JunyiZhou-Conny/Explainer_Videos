# L14 lecture slides — Serverless Deployment: Cloud Functions, Cloud Run

Source: one deck, `L14_serverless_deployment` (17 slides), titled "Lecture 14: Serverless
Deployment: Cloud Functions, Cloud Run" (AC215/E115, SEAS/Harvard). These are
the instructor's lecture slides (PDF), provided by the student for study; the PDFs are not in this
repository; slide numbers are PDF page numbers. This digest was written from the deck's extracted
text and from every slide image (contact sheets plus enlarged single pages for slides 5, 6 and 10).
Everything below is paraphrased; only short titles, terms, URLs and single code lines are quoted.
The tutorial side of the lecture is in [`digest.md`](digest.md), which follows the
tutorial repo `dlops-io/serverless-deployment` at **`46cc62f`** (`main`, 2026-10-22, the commit the
course link serves). The slides predate that commit's rewrite: they were made for the old ~150-line
README (`4eaf343`), so where slides and README disagree, the README at `46cc62f` and the captures in
`assets/` decide what the video shows (§4 below; `digest.md` §10).

## Outline

The deck has three numbered sections (slide 3). Divider slides repeat the outline with the
current section in bold.

- Slide 1 · title slide
- Slide 2 · announcements: midterm presentations
- Slide 3 · outline (Recap; Serverless: Cloud Functions; Serverless: Cloud Run, spelled "Cloud Runs" on slides 3–4)
- Slides 4–6 · **1. Recap**
  - 4 · section divider ("Recap" in bold)
  - 5 · "Review: Cheese App Status": the project roadmap from POC to Prototype to MVP
  - 6 · "Cheese App Development": the four pipeline components and where they live on GCP
- Slides 7–12 · **2. Serverless: Cloud Functions**
  - 7 · section divider
  - 8 · what serverless means
  - 9 · the kinds of serverless on GCP, tied to last week, today and next week
  - 10 · "Deployment Options": one translate app, four ways to deploy it
  - 11 · what a Cloud Function is
  - 12 · "Tutorial: Cloud Function": the deployment steps and the tutorial link
- Slides 13–16 · **3. Serverless: Cloud Run**
  - 13 · section divider
  - 14 · what Cloud Run is
  - 15 · "Tutorial: Cloud Run": the deployment steps and the tutorial link
  - 16 · "Cons of Serverless Architectures" (applies to both products)
- Slide 17 · closing "THANK YOU!!!" image

## Key ideas

1. **The project has reached deployment.** On the Cheese App roadmap, data collection,
   experiment tracking and baseline models lie behind the class. The current focus is better models, the ML
   workflow and the start of "Deployment, Scaling & Automation", all inside the Prototype
   phase. Of the four pipeline components, collector, processor and training are finished;
   "Model Deploy" is the one left. (Slides 5, 6)
2. **Serverless means code runs only when it is needed.** You do not set up servers. Expensive
   hardware such as a GPU is used only for the step that needs it (the lecture's example is the
   training step of a pipeline), so running code costs less. (Slide 8)
3. **Serverless is a family of GCP products, and this course walks through it in order.** Cloud
   Function and Cloud Run are today's topic. A Vertex AI training job was last week. Model
   deployment and pipelines on Vertex AI come next. (Slide 9)
4. **The same app can be deployed four ways, and the four form a 2×2.** One axis is what you
   hand over: a plain code file (`main.py`) or a container. The other is where it runs: a virtual
   machine on dedicated hardware, or serverless. VM + file and VM + container are already done
   (earlier lectures, ticked). Cloud Function (file, serverless) and Cloud Run (container,
   serverless) are new. (Slide 10)
5. **A Cloud Function is lightweight code with no server or container to manage.** An event
   starts it, for example a file upload, an HTTP request or a database change. You pay only while
   it runs, and it scales on its own without setup. (Slide 11)
6. **Deploying a Cloud Function takes four steps:** open the Functions page of the console,
   enable the GCP APIs it needs, write a Python file, and deploy it. The details are in the
   tutorial README. (Slide 12)
7. **Cloud Run runs a whole container with no server to manage.** The container runs either
   as a *service* or as a *job*. You pay only while code is running, and it scales out easily.
   (Slide 14)
8. **Deploying to Cloud Run means handing it a Docker image.** Open the Cloud Run page, enable
   the APIs, and deploy the image. The details are in the tutorial README. (Slide 15)
9. **Serverless has costs as well as benefits.** Each provider builds and exposes it
   differently, so moving to another cloud is hard (vendor lock-in). A function that has been
   idle starts slowly on its next call because the platform must allocate and initialize it
   again (cold start). And because execution is spread out over infrastructure you do not
   control, debugging is harder. (Slide 16)

What the slides leave to the tutorial: they do not show the HTTP handler or functions-framework,
the entry point, the requirement to listen on `$PORT`, public access and invoker permissions, the
runtime service account and Application Default Credentials, the speech call, Cloud Storage buckets,
a job's command and arguments, minimum instances, concurrency, billing models or clean-up. A scene
that needs any of these takes it from `digest.md` and the captures.

## Diagrams

- **Slide 5 · project roadmap (Gantt-style).** A wide light-blue arrow runs left to right across
  the top, with three phase labels: "POC", "Prototype", "MVP". Dashed vertical lines mark the
  phase boundaries. Under it are horizontal bars, staggered in time:
  - "Design Cheese App": a long bar from the start of POC to the end of Prototype.
  - "Data Collection": the first part of POC.
  - "Setup Experiment Tracking": most of POC, ending just past the Prototype boundary.
  - "Build Baseline Models": mid-POC into early Prototype.
  - "Build Better Models" and "ML Workflow": stacked bars inside Prototype.
  - "Build Cheese App": in MVP.
  - "Deployment, Scaling & Automation": a long bar from mid-Prototype to the end of MVP.

  A red dashed rectangle surrounds the Prototype-phase block, from just after the POC boundary
  to the end of Prototype: Build Better Models, ML Workflow, and the first part of Deployment,
  Scaling & Automation (that bar starts mid-Prototype). That rectangle is the "you are here"
  marker. Purpose: place this lecture on the project timeline.
- **Slide 6 · Cheese App components on GCP.** Four colored tiles in a row, each with a number
  badge above and an icon:
  - 1 "Data Collector" (red, download icon)
  - 2 "Data Processor" (blue, gears)
  - 3 "Model Training" (yellow, light bulb)
  - 4 "Model Deploy" (green, light bulb in a circle)

  Tiles 1–3 carry a green check mark; tile 4 does not. Below them is a dashed box labelled
  "Google Cloud Platform" that holds "Cloud Storage" (left) and "Vertex AI" (right). The arrows:
  - Collector: a red elbow arrow into Cloud Storage (writes data).
  - Processor: a blue double-headed vertical arrow to the storage side (reads and writes).
  - Training: a gold arrow down into the Vertex AI side.
  - Deploy: a green elbow arrow into the Vertex AI side from the right.

  Purpose: show that only deployment remains, and that it plugs into the same cloud.
- **Slide 9 · annotated list (timeline braces).** Five bullet items, grouped by colored curly
  braces on the right:
  - Cloud Function and Cloud Run → "TODAY" (magenta)
  - Training Job (Vertex AI) → "LAST WEEK" (green)
  - Model Deployment (Vertex AI) and Pipeline (Vertex AI) → "NEXT" (orange)

  Purpose: show serverless as one idea that spans training, serving and pipelines across three
  weeks.
- **Slide 10 · "Deployment Options" fan-out.** On the left, a dashed panel titled "Simple
  Translate App" holds a short, syntax-colored Python sketch with three commented parts: set up
  the translator, run the translation, return the result. From the panel's right edge, four
  curved arrows fan out to four numbered target boxes:
  - **1** "Virtual Machine" (server-rack icon): a blue-bordered box holding a tiny `main.py`
    page. Caption "Dedicated Hardware". Blue arrow, green check.
  - **2** "Virtual Machine": a blue-bordered box labelled "Container", holding a dashed orange
    inner box with the code. Caption "Dedicated Hardware". Blue arrow, green check.
  - **3** "Cloud Function" (cloud icon with `</>`): a green-bordered box holding a `main.py`
    page. Caption "Serverless". Green arrow, no check.
  - **4** "Cloud Run" (cloud-run icon): a green-bordered box labelled "Container" with the
    dashed orange inner box. Caption "Serverless". Green arrow, no check.

  The color code carries the message: blue = dedicated hardware, green = serverless. The inner
  content alternates between a bare file and a container. Purpose: one unchanged piece of code,
  two choices (package as file or as container × run on a VM or serverless), and today fills the
  two serverless cells. A re-draw can lay the four targets out as a 2×2 grid (rows: VM /
  serverless; columns: file / container) with the code block feeding all four.
- **Slides 12 and 15** each carry a QR code beside the tutorial link (not a diagram).
  **Slide 17** is a closing "THANK YOU!!!" picture (not a diagram).

## Terms the lecture uses

The right-hand column compares each term with the tutorial README at `46cc62f` (README line numbers
are from that commit) and with `digest.md`.

| Lecture term | Slides | Note on the tutorial README (`46cc62f`) / digest |
|---|---|---|
| "Serverless" | 1, 3, 4, 7–10, 13, 16 | Same word. The slides define it by on-demand execution and cost. The digest's "scale to zero" (README.md:218-224) is never named on the slides. |
| "Cloud Function" / "Cloud Functions" | 1, 3, 4, 7, 9–13 | Since 2024 Google calls the product *Cloud Run functions* (formerly Cloud Functions 2nd gen). The README never opens a separate Functions page: it goes **Cloud Run → Services → Write a function** (README.md:99). |
| "Cloud Run" (slides 3–4 say "Cloud Runs") | 1, 3, 4, 7, 9, 10, 13–15 | Same product. Parts 2–4 of the README all run on it. |
| "service" / "job" (containers run as either) | 14 | Both are now main parts of the README: Part 2 deploys a **service** (`translation-demo`, README.md:235), Part 4 a **job** (`translation-audio`, README.md:580). |
| "Deployment Options" | 10 | The tutorial does not use this phrase. Its four-part table (README.md:12-17) fits the serverless row of the slide's grid. |
| "Virtual Machine", "Dedicated Hardware" vs "Serverless" | 10 | "Dedicated Hardware" is the slides' name for the VM side (L1–L2 `simple-translate`). |
| "Container" (also "containers", "containerized") | 10, 11, 14 | Same as the tutorial's image or container; README.md:237-240 opens Part 2 with "a working containerized web app on your laptop". |
| "Simple Translate App" | 10 | Part 1's handler is `hello_http` (`tutorial/function/main.py:8`); Parts 2–4 run a web app, `translation_demo`, from one prebuilt image. The repo root still holds a 2025 `main.py` (`translate_http`) that the README never uses (`digest.md` §10, erratum 4). |
| "Triggered by events" (file upload, HTTP request, database update) | 11 | The tutorial uses only the HTTP trigger (`@functions_framework.http`, `tutorial/function/main.py:7`). |
| "Scales automatically", "Scale out easily" | 11, 14 | The README sets Part 2's limits: min 0, max 2 instances, concurrency 4 (README.md:282-290). The digest adds scale to zero and the instance formula (§3.1). |
| "Enable GCP APIs" | 12, 15 | Part 1: "enable required APIs if prompted" (README.md:102). Part 3 enables the Agent Platform API by name (README.md:366-367). |
| "Create a python code file" | 12 | The console wants `main.py`, a `requirements.txt` with two exact pins (`functions-framework==3.10.2`, `googletrans==4.0.0rc1`) and a **Function entry point** `hello_http`, on runtime Python 3.12 (README.md:104, 124-152). |
| "Deploy Docker Image in Cloud Run" | 15 | Part 2.2: **Deploy container → Deploy one revision from an existing container image** with `cgumb/ac215-translation-demo:lecture14-agent-platform-20261022` (README.md:272-278). The older `dlops/*` images are no longer referenced. |
| "Vendor lock-in", "Cold starts", "Limited control and debugging" | 16 | The README does not discuss lock-in. Its "More detail" box explains cold starts and says minimum instances "can keep capacity warm" (README.md:210-233). Its troubleshooting table (README.md:1035-1046) is a practical answer to limited debugging. |
| "Training Job (Vertex AI)", "Model Deployment (Vertex AI)", "Pipeline (Vertex AI)" | 9 | L13 `model-training` and L15 `model-deployment` / `ml-workflow`. The README's Part 3 uses the **Agent Platform** API, the console's current name for what earlier lectures called the Vertex AI API (`digest.md` §2). |
| "POC", "Prototype", "MVP" | 5 | Project phases used across the course. |
| "Data Collector", "Data Processor", "Model Training", "Model Deploy" | 6 | The Cheese App component names. "Cloud Storage" and "Vertex AI" are the GCP services shown. The README ties L14 to the Cheese App backend: "application code around the model" (README.md:7-10). |

## Commands and code on the slides

The slides contain no shell or `gcloud` commands. The only code is the sketch on slide 10, and
the only addresses are the console and tutorial links on slides 12 and 15.

- Slide 10: `translator = Translator()`
- Slide 10: `text = "Welcome to AC215. Everyone knows the moon's made of cheese"` (split over
  two lines on the slide)
- Slide 10: `src = "en"` and `dest = "es"`
- Slide 10: `results = translator.translate(text,src,dest)`
- Slide 10: `return = results.text` (slide shorthand, not valid Python. The deployed handler at
  `46cc62f` builds a `Translator()` per request and ends with
  `return Translator().translate(text, src=source, dest=destination).text`, passing source and
  destination by keyword (`tutorial/function/main.py:12`). Its default text is just
  `"Welcome to AC215"` (line 9); the default languages match the slide, `en` → `es`.)
- Slide 12: `https://console.cloud.google.com/functions`
- Slide 15: `https://console.cloud.google.com/run`

## What the lecture stresses

- **Cost follows use.** Serverless brings execution cost down (slide 8). Cloud Functions bill
  only for the time your code runs (slide 11), and Cloud Run only while code is running
  (slide 14).
- **No server management.** There is no server setup (slide 8), and no server *or container* to
  manage for a function (slide 11). For Cloud Run you still bring the container, but no servers
  (slide 14).
- **Scaling without manual work.** Functions scale automatically "no manual setup" (slide 11);
  Cloud Run scales out easily (slide 14).
- **Use expensive hardware only where needed.** GPUs only for the training step (slide 8).
- **The design trade-off: what you hand over.** A code file (Cloud Function) or a container
  (Cloud Run). This mirrors the VM options of earlier lectures, so the step from L1–L2 is the
  same code on a new host (slide 10).
- **Serverless has downsides** (slide 16), introduced with "While serverless computing offers
  numerous benefits…":
  - **Vendor lock-in.** Implementations and APIs differ between clouds, so migrating is hard.
  - **Cold starts.** After a period of inactivity, the first call is delayed while resources are
    allocated and the function is initialized.
  - **Limited control and debugging.** The execution environment is distributed and the
    infrastructure is hidden.
- **Deadlines.** The midterm presentations have "(No late days)" (slide 2).

## Pointers

- Slide 2: midterm presentation **Schedule** (a link) and the submission **guidelines** on Ed.
- Slides 5–6: the Cheese App project roadmap. Deployment is the next milestone step.
- Slide 9: last week's Vertex AI training job (L13 `model-training`); next lecture's Vertex AI
  model deployment and pipeline (L15).
- Slide 12: console `https://console.cloud.google.com/functions`. Tutorial "Running App as Cloud
  Function": `https://github.com/dlops-io/serverless-deployment#running-app-as-cloud-function`
  (with a QR code beside it).
- Slide 15: console `https://console.cloud.google.com/run`. Tutorial "Running App in Cloud Run":
  `https://github.com/dlops-io/serverless-deployment#running-app-in-cloud-run` (with a QR code
  beside it).
- **Both tutorial anchors are dead at `46cc62f`.** The headings they name existed only in the old
  README (`4eaf343`: "Running App as Cloud Function", "Running App in Cloud Run"). Today's README
  has "Part 1: Deploy a translation function" … "Part 4" (README.md:91, 235, 355, 580), so both
  links, like the course tutorials page's, open the top of the README (`digest.md` §10, erratum 1).
  Read them as "start at the top: Part 1 is the function, Parts 2–4 are Cloud Run".
- No readings, demos or homework are listed beyond these.

## This video and the slides

**Basis.** The video is scripted: [`script.md`](script.md) (v2, review merge 2026-11-04) has 16
scenes, and its SHOW lines carry `LECTURE 14 · a–b` marks, which become the GREY
`lecture_ref(14, "a–b")` tag. It follows the README at **`46cc62f`** ([`BRIEF.md`](BRIEF.md),
decision "follow `46cc62f`"), with real captures in `assets/` ([`ASSETS.md`](ASSETS.md)). The old
README at `4eaf343`, against which this digest was first written, is kept in
`assets/source/at-4eaf343/` for comparison only. The conflicts below were rebuilt against `46cc62f`
from `digest.md` §10 and the captures; where they and this file disagree, the captures win.

### 1. Scene map: script scenes ↔ slides

Slide spans are the `LECTURE 14` marks in each scene's SHOW lines, in order of appearance.

| Scene | Title (`script.md`) | Slides cited | What the scene takes from the lecture |
|---|---|---|---|
| S01 | It works on localhost | 8 | The hook's answer, closing beat: an instance that exists only while requests arrive, and a meter that moves only then (slide 8's "code runs only when needed"). |
| S02 | One app, four ways to deploy it | 5; 6; 8–9; 10 | Slide 5's roadmap with "you are here"; slide 6's four Cheese App tiles, Model Deploy unticked (plus Milestone 3); slide 8's three phrases; slide 10's grid built as V1 `DeployGrid` (Gap 1), with the README's four parts dropped into its serverless row. Ends on the two erratum cards: dead anchors (Conflict 6) and the old course-map pin. |
| S03 | Before you begin: project, region, clone | none | Tutorial-only (project ID, Toronto region vs `us-central1`, the unused root files). |
| S04 | Part 1: write a function | 11; 11–12; 10; 11–12; 11–12 | Slide 11 as event triggers with HTTP lit "today" (Gap 5); slide 12's four steps as a checklist; the product name (Conflict 1); slide 10's sketch vs the handler (Conflict 3); "create a Python file" expanded into three inputs (Conflict 5). |
| S05 | What runs your function? | 10–11; 16 | Slide 11's "without managing servers or containers", then the container Google builds anyway (Conflict 2); the first "where do you look?" place, the build log (slide 16, Gap 2). |
| S06 | Call it with a query string | 11; 16 | Slide 11's HTTP trigger as the query string; slide 16's cold start over the local stand-in's shutdown, with the README's cold-start note. |
| S07 | Part 2: the prebuilt app on your laptop | 10, 14 | The grid's container cell lights; slide 14's "containerized apps". |
| S08 | Deploy the same image | 14–15; 11, 14 | Slide 14 in one line and slide 15's three steps as the checklist; slides 11/14's "pay only when your code runs", qualified by billing mode and min instances (Conflict 4). |
| S09 | Who may call it, and who it runs as | none | Tutorial-only (invoker vs runtime identity). |
| S10 | Attach the identity, turn on speech | 16 | "Limited control and debugging" made workable: the error message names the badge or setting (Gap 2). |
| S11 | Develop locally with ADC | none | Tutorial-only (ADC with impersonation). |
| S12 | Finite work: a job and two buckets | 14; 9 | Slide 14's "service or job"; slide 9's L13 training-job brace as the same finite shape (Gap 4). |
| S13 | Command, arguments and the job's badge | 14 | The job half of slide 14; command and arguments are tutorial-only. |
| S14 | Execute it and collect the files | 16 | The third place to look: a green check is not proof, the manifest is (Gap 2). |
| S15 | From the terminal, then the helper | none | Tutorial-only (`--args` overrides, the helper script). |
| S16 | Clean up, and what serverless costs | 16; 9 | Clean-up has no tag. Then slide 16's three cons, each with its answer from the tutorial (Gaps 2, 6); slide 9's "NEXT" brace to L15 (Gap 4). |
| — | not in the video | 1–4, 7, 13, 17 | Lecture-only: title, announcements, outline, dividers, closing image. Every content slide (5, 6, 8–12, 14–16) is used at least once. |

### 2. Already in common

| # | Concept | Scenes ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Serverless: your code runs only when needed, with no server to set up, so cost follows use | S01, S02, S08 ↔ 8 | Yes. The video sharpens it: serverless does not mean there are no servers, it means you stop deciding when they exist (`digest.md` §3.1). |
| 2 | The VM is the baseline: earlier lectures put the app on dedicated hardware | S02 ↔ 10 (cells 1–2, ticked) | Yes. The grid's top row ticks in as L1 and L2. L1 ran the app on a VM and L2 ran its container on one. |
| 3 | The same translate code moves to a new host | S02, S04 ↔ 10 | Yes in spirit. The slide's code is a script sketch, not the handler that gets deployed (Conflict 3). |
| 4 | A Cloud Function: you hand over code, and the platform runs it when an event such as an HTTP request arrives | S04, S06 ↔ 11, 12 | Yes, with one refinement: Google still builds a container from your file (Conflict 2). |
| 5 | Deploying a function: open the console page, enable the APIs, write the code, deploy | S04 ↔ 12 | Yes as an outline; the console path and the inputs changed (Conflicts 1, 5). |
| 6 | Cloud Run runs a container you bring; you deploy an image | S07, S08 ↔ 14, 15, 10 (cell 4) | Yes. Part 2.2 is "Deploy one revision from an existing container image". |
| 7 | Containers run as a service or as a job | S12, S13 ↔ 14 | Yes, and at `46cc62f` the README treats both as main parts (Part 2 service, Part 4 job). |
| 8 | You pay only while code runs | S08 ↔ 11, 14 | Yes for compute with the README's settings (request-based, min 0). The video adds what bills anyway (Conflict 4). |
| 9 | Scaling is automatic | S08 ↔ 11, 14 | Yes. The video adds scale to zero, concurrency 4 and the clamp between min 0 and max 2. |
| 10 | Cold start: after idle time, the platform must allocate and initialize before the first call | S06, S16 ↔ 16 | Yes on the mechanism. The README adds that there is no fixed inactivity interval (README.md:218-224), and the video shows min instances ≥ 1 as the knob that trades money for it. |

### 3. Slide content beyond the tutorial, and where the video carries it

All six gaps found in the first pass are now in the script.

1. **The four deployment options as a 2×2 (slide 10).** Rows: VM or serverless; columns: a code
   file or a container. Built in S02 (V1 `DeployGrid`), Part 1 in the file cell (S04–S05), the
   container cell lit in S07, split into service | job in S12, complete again in S16.
2. **Limited control and debugging (slide 16).** Every failure in this tutorial shows up away from
   your code. The video's three places to look: the build log (S05, entry-point mismatch, capture
   `dev/29`), the service logs (S06 provider timeout, S10 speech denied), and the job's logs and
   manifest, because a green check only means exit 0 (S14). S16 collects them.
3. **Where L14 sits in the project (slides 5–6).** S02 opens on the roadmap and the four Cheese
   App tiles, with Milestone 3's "deploy your model or API using Cloud Functions or Cloud Run".
4. **One idea across three weeks (slides 8–9).** S02 (slide 8's phrases), S12 (L13's training job
   as the same finite shape), S16 (the "NEXT" brace to L15).
5. **Event triggers (slide 11).** S04: file upload and database change go grey, the HTTP request
   stays lit as today's trigger.
6. **Vendor lock-in (slide 16).** S16: functions-framework and the image both ran on a laptop
   (captures `dev/22`, `laptop/`); the console, IAM and the build are the Google-specific parts.

### 4. Conflicts (slides vs README at `46cc62f`)

Numbers 1–5 keep the numbering `BRIEF.md` and `script.md` cite; 6 is new with `46cc62f`.

| # | Slides say | Tutorial today (README `46cc62f`, captures) | Current | How the video puts it |
|---|---|---|---|---|
| 1 | **The product name** (slides 1, 3, 4, 7, 9–13): "Cloud Function(s)", opened at `console.cloud.google.com/functions` (slide 12), a product separate from Cloud Run (slides 9, 10). | The product is now *Cloud Run functions* (formerly Cloud Functions 2nd gen), and it runs on Cloud Run. The README never uses the Functions page: **Cloud Run → Services → Write a function**, which opens **Create service** (README.md:99-100). The deployed function is a Cloud Run service with a `…run.app` URL. Console labels come from the README and its GIFs, not seen live (`digest.md` §10). | The README and console naming | S04: a product-name card (tag `erratum`), "Cloud Functions" → "Cloud Run functions (formerly Cloud Functions 2nd gen)", then the README card for line 99. |
| 2 | **A function has no container.** Slide 10 draws cell 3 as a bare `main.py` next to cell 4's "Container"; slide 11 says "without managing servers or containers". | Cloud Build turns `main.py` + `requirements.txt` into an image (README.md:212-216; base `python312` in the gcloud path, README.md:197), stores it in Artifact Registry and runs it as a revision whose process is functions-framework serving `hello_http` through Flask and gunicorn (`digest.md` §3.4; captures `dev/21-22`). That image outlives the service and is clean-up step 4 (README.md:1018-1028). | Both, at different levels: the slide shows what you hand over, the tutorial shows what runs | S05: the quote stays true ("you don't *manage* them"), and a container builds itself behind it. S16 removes the leftover image. |
| 3 | **The translate code** (slide 10): a script with one module-level `Translator()`, the long "…moon's made of cheese" default, ending in `return = results.text`, calling `translator.translate(text,src,dest)` by position. | The deployed handler `hello_http` reads `text`, `src`, `dest` from `request.args`, builds a `Translator()` per request and calls `.translate(text, src=source, dest=destination)` (`tutorial/function/main.py:8-12`); default text `"Welcome to AC215"`. In googletrans 4.0.0rc1, the version `tutorial/function/requirements.txt:2` pins, the signature is `translate(self, text, dest='en', src='auto')` (`googletrans/client.py:173`), so the slide's positional call would ask for Spanish → English. | The README and repo code | S04: the sketch fades in as a GREY "lecture sketch" (tag `erratum`), its second slot flashes as `dest`, then the handler's keywords light: "the handler passes them by name". |
| 4 | **You pay only while code runs** (slide 11: "Pay only for the time your code runs"; slide 14: "Only pay when your code is running"; slide 8: lower cost). | True for compute with Part 2's settings, **request-based** billing and minimum instances 0 (README.md:281-283). Instance-based billing or min ≥ 1 bills idle time. Other costs do not depend on your code running: Cloud Build on every function deploy, the image left in Artifact Registry, the two buckets (with soft-delete retention), and Gemini text-to-speech per call in Parts 3–4. The README now has a clean-up section (README.md:1018-1028), but it omits soft-deleted objects and the build's source archives and logs (`digest.md` §10, erratum 7). | The README's billing settings and `digest.md` §3.3 | S08: the quote plus "with these two settings", and min 1 / instance-based as the fine print. GOLD cost tags where each cost starts (S04, S08, S10, S12–S14). S16: the README's checklist plus the two things it leaves out. |
| 5 | **What you hand over for a function** (slide 12): "Create a python code file", then "Deploy code as Cloud Function". | The console asks for runtime **Python 3.12** and **Allow public access** (README.md:104-105), creates the service from a template, then in the Source editor you replace `main.py` and `requirements.txt` (two exact pins: `functions-framework==3.10.2`, `googletrans==4.0.0rc1`) and set **Function entry point** `hello_http`, which must equal the `def` name (README.md:124-152). A wrong entry point fails at start-up with functions-framework's "expected to contain a function named …" (capture `dev/29`). | The README (the slide is an outline) | S04: the checklist's third item expands into three chips, `main.py`, `requirements.txt`, `entry point: hello_http`; S05 shows the mismatch in the build log. |
| 6 | **The tutorial links** (slides 12, 15): `…/serverless-deployment#running-app-as-cloud-function` and `#running-app-in-cloud-run`. | Those headings existed only at `4eaf343`. At `46cc62f` the README's sections are "Part 1: Deploy a translation function" through "Part 4" (README.md:91, 235, 355, 580), so both links (and the course tutorials page's) open the top of the README (`digest.md` §10, erratum 1). | The README | S02: an erratum card with each link, "no such section today", and "start at the top · Part 1 = function · Parts 2–4 = Cloud Run". |

Not counted as conflicts:
- Slides 3–4 say "Cloud Runs", a typo for Cloud Run.
- Slide 10's ticked "Virtual Machine + Container" matches L2, which ran the image on a GCP VM.
- Slide 15's "Deploy Docker Image in Cloud Run" still holds; only the image changed (now
  `cgumb/ac215-translation-demo:…`, deployed by tag in the click path; the digest is published at
  README.md:1068-1070, erratum 6, said in S08).
- The README goes on to a runtime identity, speech and a Cloud Storage job (Parts 3–4), which the
  slides do not show beyond slide 14's "service or job". That is tutorial-only content, not a
  disagreement.
- The slides name no runtime; the old README's Python 3.10 vs today's 3.12 is a README-to-README
  change, said once in S04.
- Slide 16 ties cold starts to inactivity. That is the common case; the README adds that there is
  no fixed interval, and a scale-out with no free warm instance causes one too.

### 5. Lecture tags and redraw rules (as scripted)

- One GREY `lecture_ref(14, "a–b")` per `LECTURE 14` mark, with the spans in §1. Scenes S03, S09,
  S11 and S15, and S16's clean-up blocks, are tutorial-only and carry no tag.
- Every lecture picture is redrawn in the series style: no slide images, QR codes, logos or
  screenshots. Slide 10's colour code is not copied, because its green for "serverless" would
  collide with the series' GREEN: both grid rows are BLUE, a solid rack for a VM and a dashed
  outline for serverless; TEAL marks the container column, ticks the L1–L2 cells, YELLOW today's.
- Lecture terms the video uses: *serverless*, *Deployment Options*, *dedicated hardware*, *Cloud
  Function* (then *Cloud Run functions*), *Cloud Run*, *service* and *job*, *triggered by events*,
  *scales automatically*, *vendor lock-in*, *cold start*, *limited control and debugging*, *Model
  Deploy*, *POC / Prototype / MVP*. The tutorial's words take over where the lecture stops: *entry
  point*, *functions-framework*, *revision*, `PORT`, *scale to zero*, *min instances*,
  *concurrency*, *request-based billing*, *invoker*, *runtime service account*, *ADC*, *tag* and
  *digest*, *Artifact Registry*, *command* and *arguments*.
- Qualify, don't repeat: "without managing containers" (there is one, and Google manages it); "pay
  only while code runs" (with request-based billing and min 0; builds, storage and speech are
  extra).
