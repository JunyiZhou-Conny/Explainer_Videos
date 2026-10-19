# L14 lecture slides — Serverless Deployment: Cloud Functions, Cloud Run

Source: one deck, `L14_serverless_deployment` (17 slides), titled "Lecture 14: Serverless
Deployment: Cloud Functions, Cloud Run" (AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are
the instructor's lecture slides (PDF), provided by the student for study; the PDFs are not in this
repository; slide numbers are PDF page numbers. This digest was written from the deck's extracted
text and from every slide image (contact sheets plus enlarged single pages for slides 5, 6 and 10).
Everything below is paraphrased; only short titles, terms, URLs and single code lines are quoted.
The tutorial side of the lecture is in [`digest.md`](digest.md).

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
the requirement to listen on `$PORT`, public access and invoker permissions, the service account
for a job, minimum instances, billing models or clean-up. A scene that needs any of these must
take it from `digest.md`.

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

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Serverless" | 1, 3, 4, 7–10, 13, 16 | Same word. The slides define it by on-demand execution and cost. The digest's "scale to zero" is never named on the slides. |
| "Cloud Function" / "Cloud Functions" | 1, 3, 4, 7, 9–13 | The README and today's console say **"Cloud Run -> Functions"** (Cloud Run functions). Since 2024 Google has called the product by that name (formerly Cloud Functions 2nd gen). The slide link `console.cloud.google.com/functions` redirects into Cloud Run. |
| "Cloud Run" (slides 3–4 say "Cloud Runs") | 1, 3, 4, 7, 9, 10, 13–15 | Same product. The README's path is "Deploy container" → service. |
| "service" / "job" (containers run as either) | 14 | The README covers the service in "Running App in Cloud Run" and the job only in a bonus section (anchor `#setup-cloud-run-job--service-account`) that the slides do not link. |
| "Deployment Options" | 10 | The tutorial does not use this phrase. It fits the four-way comparison. |
| "Virtual Machine", "Dedicated Hardware" vs "Serverless" | 10 | "Dedicated Hardware" is the slides' name for the VM side (L1–L2 `simple-translate`). |
| "Container" (also "containers", "containerized") | 10, 11, 14 | Same as the tutorial's Docker image or container. |
| "Simple Translate App" | 10 | The tutorial app. Its handler is `hello_http` in the README and `translate_http` in the repo's `main.py`. |
| "Triggered by events" (file upload, HTTP request, database update) | 11 | The tutorial uses only the HTTP trigger (`@functions_framework.http`). |
| "Scales automatically", "Scale out easily" | 11, 14 | The digest speaks of autoscaling, scale-out and scale to zero, with min/max instances. |
| "Enable GCP APIs" | 12, 15 | The README's "Click ENABLE" step (Build, Functions, Logging and Pub/Sub APIs for the function). |
| "Create a python code file" | 12 | In the README you paste `main.py` and `requirements.txt` into the console's inline editor. The README never mentions the console's **entry point** field; it already says `hello_http`, which matches the README's handler (`digest.md` Step 4). |
| "Deploy Docker Image in Cloud Run" | 15 | The README deploys the prebuilt `dlops/simple-translate-http:latest` from Docker Hub. |
| "Vendor lock-in", "Cold starts", "Limited control and debugging" | 16 | The tutorial does not discuss lock-in. Cold starts show up in the console's "Set to 1 to reduce cold starts" hint (digest §3.2). |
| "Training Job (Vertex AI)", "Model Deployment (Vertex AI)", "Pipeline (Vertex AI)" | 9 | L13 `model-training` and L15 `model-deployment` / `ml-workflow`. |
| "POC", "Prototype", "MVP" | 5 | Project phases used across the course. |
| "Data Collector", "Data Processor", "Model Training", "Model Deploy" | 6 | The Cheese App component names. "Cloud Storage" and "Vertex AI" are the GCP services shown. |

## Commands and code on the slides

The slides contain no shell or `gcloud` commands. The only code is the sketch on slide 10, and
the only addresses are the console and tutorial links on slides 12 and 15.

- Slide 10: `translator = Translator()`
- Slide 10: `text = "Welcome to AC215. Everyone knows the moon's made of cheese"` (split over
  two lines on the slide)
- Slide 10: `src = "en"` and `dest = "es"`
- Slide 10: `results = translator.translate(text,src,dest)`
- Slide 10: `return = results.text` (slide shorthand, not valid Python. The tutorial handler
  ends with `return results.text` and passes `src=`/`dest=` as keywords. The README's default
  text reads "…the moon is made out of cheese".)
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
- No readings, demos or homework are listed beyond these.

## This video and the slides

**Basis.** The video is not scripted yet. This folder has no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`, so the map below uses the nine planned chapters in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L14-serverless-deployment.md`) and every slide: the extracted text and both contact sheets. With no captures yet, "what the tutorial does today" means the repo at `4eaf343` and the two Docker Hub images, as verified in `digest.md`. For this section I re-checked three things at the source: the README headings, handler and `translate` call at `4eaf343`; the `translate` signature in the googletrans 4.0.0rc1 sdist whose hash `uv.lock` pins, and in 4.0.2 (Conflict 3); and the fact that L2 ran its container on a GCP VM (`ac215-l02-containers-1/digest.md`). When `assets/terminal/` and `ASSETS.md` exist, re-check the Conflicts against them. If they disagree, the captures win.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | The idle-VM problem (1.5 min) | 8, 10 (the two ticked VM cells) | Same concept. The hook asks the question that slide 8's "brings down code execution cost" answers. The plan does not use the roadmap slides 5–6, though they would fit here. |
| 2 | One function, three homes (2 min) | 9, 10, 14 ("service or job") | Same concept, sorted differently. The lecture's grid has four homes: a file or a container, on a VM or serverless. The plan's three homes (function, service, job) are all serverless. The `request.args` animation is tutorial-only, because the slide's sketch has no handler. |
| 3 | Who actually runs your function? (2.5 min) | 11 ("without managing servers or containers") only | Tutorial-only. The lecture never opens the box. functions-framework, Flask, gunicorn and `0.0.0.0:$PORT` come from the repo, and they refine slide 11 (Conflict 2). |
| 4 | Path A: Cloud Run functions in the console (3 min) | 11, 12 (and cell 3 of slide 10) | Same concept, and the tutorial applies it. Slide 12's four steps outline the README section. Conflicts 1, 3 and 5. |
| 5 | The container contract (2 min) | 14 ("containerized apps") only | Tutorial-only. `$PORT`, `0.0.0.0`, amd64 and "no local state" are not on the slides. |
| 6 | Path B: deploy a container you already have (2.5 min) | 14, 15 (and cell 4 of slide 10) | Same concept, and the tutorial applies it. "Deploy Docker Image in Cloud Run" is the README's "Deploy one revision from an existing container image". Tags, digests and the 2024 image are tutorial-only. |
| 7 | Scale to zero, cold starts and the bill (3 min) | 8, 11, 14, 16 (cold starts) | Same concept. The lecture states pay-per-use, automatic scaling and cold starts. The plan adds the mechanism: scale to zero, concurrency, min instances, request-based vs instance-based billing (Conflict 4). |
| 8 | Who may call it, and who is it when it calls out? (2.5 min) | 14 ("service or job") | Mixed. Services vs jobs is the same concept. Invoker IAM, the runtime service account and the job's argument handling are tutorial-only. Neither slide 15's link nor the course site points to the README's job section. |
| 9 | Clean-up and recap (1.5 min) | 16 (the cons), 9 (the "NEXT" brace) | The recap could stand on lecture ground, but the plan does not use it yet. Clean-up is tutorial-only: the lecture's "only pay when your code is running" leaves it out (Conflict 4). |
| — | not in the plan | 1–4, 7, 13, 17 (title, announcements, outline, dividers, close); 5–6 (roadmap, components); 16 (vendor lock-in, limited control and debugging) | Lecture-only. |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Serverless: your code runs only when needed, with no server to set up, so cost follows use | ch1, ch7 ↔ 8 | Yes. The plan sharpens it: serverless does not mean there are no servers, it means you stop deciding when they exist (`digest.md` §3.1). That agrees with the lecture's "no setup of servers". |
| 2 | The VM is the baseline: earlier lectures put the app on dedicated hardware | ch1 ↔ 10 (cells 1–2, ticked) | Yes. The hook ("your translator has lived on a VM since Lecture 1") is slide 10's two ticked blue cells. L1 ran the app on a VM and L2 ran its container on one, as the ticks say. |
| 3 | The same Simple Translate code moves to a new host | ch2 ↔ 10 | Yes in spirit. The slide's code is a script sketch, not the handler that gets deployed (Conflict 3). |
| 4 | A Cloud Function: you hand over code, and the platform runs it when an event such as an HTTP request arrives | ch2, ch4 ↔ 11, 12 | Yes, with one refinement. The plan's "a function is a container you did not write" (`digest.md` §3.4) goes further than slide 11's "without managing … containers". Both hold if the video stresses *managing* (Conflict 2). |
| 5 | Deploying a function: open the console page, enable the APIs, write the code, deploy | ch4 ↔ 12 | Yes. Slide 12's steps are the README section in brief. The plan adds what the slide leaves out (Conflict 5). |
| 6 | Cloud Run runs a container you bring; you deploy an image | ch6 ↔ 14, 15, 10 (cell 4) | Yes. |
| 7 | Containers run as a service or as a job | ch2, ch8 ↔ 14 | Yes. The lecture names both; the README shows the job only in its bonus section. |
| 8 | You pay only while code runs | ch1, ch7 ↔ 11, 14 | Yes for compute with the console defaults. The plan's billing chapter shows when it stops being true (Conflict 4). |
| 9 | Scaling is automatic | ch7 ↔ 11 ("no manual setup"), 14 ("scale out easily") | Yes. The plan adds scale to zero, concurrency, and the clamp between min and max instances. |
| 10 | Cold start: after idle time, the platform must allocate and initialize before the first call | ch7 ↔ 16 | Yes on the mechanism. The plan widens it in two ways. A cold start also happens on scale-out, whenever no warm instance is free, not only after inactivity. And the plan shows the knob that trades money for it (min instances = 1), where the lecture lists it only as a downside. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **The four deployment options as a 2×2 (slide 10).** Rows: a VM (dedicated hardware) or serverless. Columns: what you hand over, a code file or a container. L1–L2 filled the VM row, and today fills the serverless row: path A is the file cell, path B the container cell. The plan's "three homes" never shows the grid. Without it the student loses the lecture's map of where each README section sits, and of why path A asks for source while path B asks for an image. **Carry it in** ch2 (build the grid), then ch4 and ch6 (light the cell each path fills).
2. **Limited control and debugging (slide 16).** In this tutorial every failure shows up away from your code:
   - the build log: entry-point mismatch, a bad `requirements.txt`;
   - the revision status: nothing listening on `$PORT`;
   - the Logs tab: googletrans 500s;
   - a job's execution logs: a *Succeeded* badge on a failed Gemini call.

   The lecture names the cost, and the tutorial shows where to look. **Carry it in** ch4 (build log), ch5 (a revision that never becomes ready) and ch8 (job logs, not the badge), as a recurring "where do you look?" beat.
3. **Where L14 sits in the project (slides 5–6).** On the roadmap, deployment starts in the middle of the Prototype phase, inside the "you are here" box. Of the four Cheese App components, only "Model Deploy" is unticked, and Milestone 3 asks students to "Deploy your model or API using Cloud Functions or Cloud Run" (`digest.md` §7). This tells the student why the tutorial matters to their own project. **Carry it in** ch1, ten seconds after the hook, or in ch9.
4. **One idea across three weeks (slides 8–9).** Serverless is a family: the Vertex AI training job last week (L13, a GPU only for the training step), Cloud Functions and Cloud Run today, Vertex AI model deployment and pipelines next (L15). None of the planned chapters bridges to L13 or L15. **Carry it in** ch1 (a callback to L13) and ch9 (the road to L15).
5. **Event triggers (slide 11).** A function can start on a file upload, an HTTP request or a database change. The tutorial uses only HTTP (`@functions_framework.http`). That may also be why the function's API dialog asks for the Pub/Sub API (`digest.md` §2): Pub/Sub likely carries the event triggers (an inference, not checked). **Carry it in** ch4, in one sentence.
6. **Vendor lock-in (slide 16).** Moving serverless code between clouds is hard, but the tutorial can give a more precise answer. functions-framework is open source, and the repo's own image runs it in a plain Docker container you can start on your laptop (`docker-entrypoint.sh:18`; `digest.md` Step 1). Path B's image runs anywhere that runs amd64 containers. The Google-specific parts are the console set-up, IAM and the build pipeline. **Carry it in** ch9 (recap) or ch3.

### 4. Conflicts

| # | Slides say | Tutorial today (repo `4eaf343`, Docker Hub images, README screenshots) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **The product name** (slides 1, 3, 4, 7, 9–13): "Cloud Function(s)", reached at `https://console.cloud.google.com/functions` (slide 12), a product separate from Cloud Run (slides 9, 10). | README.md:8 says "Cloud Run -> Functions". Since 2024 the product has been called *Cloud Run functions* (formerly Cloud Functions 2nd gen), and it runs on Cloud Run. The slide's link still works, but it redirects to Cloud Run's create-service page with the Function card (`digest.md` Step 2). The deployed function gets a `…run.app` URL, not README.md:76's `cloudfunctions.net` one. | The README and console naming | "The lecture uses the product's long-time name, Cloud Functions. Google has since moved it under Cloud Run as *Cloud Run functions*, and the slide's link still takes you there." Show the new name on screen once, with the old one in brackets. |
| 2 | **A function has no container.** Slide 10 draws cell 3 as a bare `main.py` next to cell 4's "Container"; slide 11 says "without managing servers or containers". | Cloud Build packs `main.py` + `requirements.txt` into an image whose process is `functions-framework --target <entry point>`. The image is stored in Artifact Registry and runs as a Cloud Run revision (`digest.md` §3.4). The repo's `docker-entrypoint.sh:18` hand-builds the same container. | Both, at different levels: the slide shows what you hand over, the tutorial shows what runs | "The lecture's grid sorts by what *you* hand over. Under the hood Google turns your file into a container too. That's why there's an image to clean up at the end." |
| 3 | **The translate code** (slide 10): a top-level script ending in `return = results.text` that calls `translator.translate(text,src,dest)` positionally, with the default text "…the moon's made of cheese". | The deployed code is an HTTP handler (`hello_http` at README.md:29, `translate_http` at `main.py:6`). It reads `text`, `src` and `dest` from `request.args` and calls `translator.translate(text, src=src, dest=dest)` (README.md:57, `main.py:25`). In googletrans 4.0.0rc1 the signature is `translate(self, text: str, dest='en', src='auto')` (`googletrans/client.py:173` in the sdist that `uv.lock` pins), and 4.0.2 keeps that order. The slide's positional call would therefore ask for Spanish → English, the reverse of what its variables intend. The default text is "…the moon is made out of cheese" (README.md:47), or just "Welcome to AC215" (`main.py:15`). | The README and repo code | Treat the slide as a sketch: "Here's the lecture's sketch of the app; here's the handler you actually deploy." Show the keyword call and add one sentence: "Pass `src=` and `dest=` by name. In this library the second position is the destination." |
| 4 | **You pay only while code runs** (slide 11: "Pay only for the time your code runs"; slide 14: "Only pay when your code is running"; slide 8: lower cost). | This holds for compute with the console defaults, request-based billing and minimum instances 0 (`images/cloud-run-create.png`). Instance-based billing or min instances ≥ 1 bills idle time. Some costs are not for your code running at all: Cloud Build minutes on every deploy, and the Artifact Registry image and source bucket a function deploy leaves behind. A job's Gemini tokens are billed on top of its compute. The README has no clean-up section (`digest.md` §2, erratum 9). | The console's billing settings and the digest's cost table | "That's true for the compute, with the defaults you'll see. Change either setting and the meter runs while idle. What the build leaves behind is billed as storage until you delete it, which is what the clean-up chapter is for." |
| 5 | **What you hand over for a function** (slide 12): "Create a python code file", then "Deploy code as Cloud Function". | The console asks for three things: `main.py`; `requirements.txt` (`functions-framework==3.*`, `googletrans==4.0.0rc1`); and a *Function entry point*, which must equal the `def` name (`hello_http`). The README also has you pick a runtime ("Python 3.10", README.md:19) and "Allow public access". Clicking "Create" deploys the template first; then you paste the code and click "Save and Deploy" (README.md:16-71). | The README (the slide is an outline) | "The lecture's 'a Python file' is the short version. The console wants the file, its dependency list, and the name of the function to call." The entry-point mismatch (`digest.md` §6 #5) belongs here. |

Not counted as conflicts:
- Slides 3–4 say "Cloud Runs", a typo for Cloud Run.
- Slide 10's ticked "Virtual Machine + Container" matches L2, which ran the image on a GCP VM.
- The tutorial links on slides 12 and 15 match README headings at `4eaf343`.
- Slide 16 ties cold starts to inactivity. That is the common case; chapter 7 adds scale-out.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag each chapter that stands on lecture ground with one GREY `lecture_ref(14, "a–b")`, using the ranges below. Re-draw every lecture diagram in the series style. Never show slide images or the QR codes.
- Make slide 10's grid the video's **running map** (gap 1): build it in ch2, light the cell each path fills in ch4 and ch6, and bring it back in ch9. This is the lecture's organising picture and the strongest link between lecture and tutorial.
  - Do not copy the lecture's colour code. Its green for "serverless" would collide with the series' GREEN, which means project-owned and isolated.
  - Draw both rows in BLUE (both are cloud). Mark the difference with the shape: a solid server rack for the VM, and a dashed instance outline for serverless, which appears only when called.
  - Use TEAL for the container column, a check mark for the cells done in L1–L2, and YELLOW for today's two cells.
- The plan targets about 20 minutes, against the series' 25–35. Gaps 1–4 add roughly 3–4 minutes of lecture-backed content without padding.
- When captures are made, record these as `recorded`: the function's build log, the service's Revisions and Logs pages, and a job execution's logs. Then re-check Conflicts 1, 4 and 5 against them (console wording, billing defaults, button labels).

**Per chapter**
- **Ch1 · Lecture 14 · slides 5–8.**
  - After the hook, spend ten seconds on a re-drawn slide-5 roadmap with the dashed "you are here" box over the Prototype phase.
  - Then show slide 6's four component tiles: "Model Deploy" is the only one unticked. Say that Milestone 3 asks for exactly this (gap 3).
  - Give slide 8's four bullets as the answer to the hook. Name L13's Vertex AI training job as last week's serverless (gap 4).
- **Ch2 · Lecture 14 · slides 9–10, 14.**
  - Open with slide 10: one code panel and four arrows fanning out, re-laid as the 2×2 grid (`SLIDES.md` § Diagrams). The two VM cells tick in (L1, L2); the two serverless cells stay YELLOW.
  - Then split the serverless-container cell into slide 14's *service* and *job*. That gives the plan's "three homes".
  - Run the `request.args` animation on the real handler. Show the slide's sketch only as a faded "lecture sketch" (Conflict 3).
- **Ch3 · Lecture 14 · slide 11.**
  - Use slide 11's "without managing servers or containers" as the set-up line, then open the box: Flask → gunicorn → container → Cloud Run. Say *managing*, not "no container" (Conflict 2).
  - For gap 6, one sentence: functions-framework is open source and runs in plain Docker on your laptop, so this layer travels with you.
- **Ch4 · Lecture 14 · slides 11–12.**
  - Lay out slide 12's four steps as the chapter's checklist and map each one to its README clicks. Step 3, "Create a python code file", expands into the three inputs (Conflict 5).
  - Name the product both ways once (Conflict 1). Add slide 11's event triggers in one line (gap 5).
  - Make the build log the first "where do you look?" beat (gap 2).
  - End by lighting cell 3 of the grid, then show that a container sits underneath (Conflict 2).
- **Ch5 · no lecture slide.** Tutorial-only, so no `lecture_ref`. A revision that never becomes ready is the second "where do you look?" beat (gap 2).
- **Ch6 · Lecture 14 · slides 14–15.** Use slide 15's three steps as the chapter's checklist: "Deploy Docker Image in Cloud Run" becomes the README's "Deploy one revision from an existing container image". Light cell 4 of the grid.
- **Ch7 · Lecture 14 · slides 11, 14, 16.**
  - Open with the lecture's two promises as GOLD cost tags ("pay only while code runs", "scales automatically") and slide 16's cold start as a RED tag. The animation then shows when each one holds.
  - The min-instances toggle answers the cold-start downside. Instance-based billing and min instances ≥ 1 are the fine print on "pay only while code runs" (Conflict 4).
- **Ch8 · Lecture 14 · slide 14.**
  - "The lecture names two ways to run a container, a *service* and a *job*. Here is the job." Note in one line that the job section is a README bonus that neither slide 15's link nor the course site points to.
  - The job's execution logs are the third "where do you look?" beat: the *Succeeded* badge is not proof (gap 2).
- **Ch9 · Lecture 14 · slides 9, 16.**
  - Clean-up comes first. The compute meter has stopped, but the leftover storage is still billed (Conflict 4).
  - Then recap with slide 16's three downsides as a checklist the tutorial answers:
    - cold starts: min instances;
    - limited control and debugging: the three places to look;
    - vendor lock-in: the portable container vs the Google-specific set-up (gaps 2, 6).
  - Close on slide 9's "NEXT" brace: Vertex AI model deployment and pipelines in L15 (gap 4).
- **Recap card.** Keep the plan's six questions, and add two:
  - "Place paths A and B on the lecture's 2×2: what do you hand over, and where does it run?"
  - "Name the lecture's three downsides of serverless, and what this tutorial gives you for each."

**Terms**
- Use the lecture's words: *serverless*, *Deployment Options*, *dedicated hardware*, *Cloud Function* (then *Cloud Run functions*, its current name), *Cloud Run*, *service* and *job*, *triggered by events*, *scales automatically*, *vendor lock-in*, *cold start*, *limited control and debugging*, *Model Deploy* (the Cheese App component), *POC / Prototype / MVP*.
- Add the tutorial's words where the lecture stops: *entry point*, *functions-framework*, *revision*, *container contract*, `$PORT`, *scale to zero*, *min instances*, *request-based billing*, *invoker*, *runtime service account*, *tag* and *digest*, *Artifact Registry*.
- Qualify, don't repeat:
  - "without managing containers": there is a container, and Google manages it;
  - "pay only while code runs": with the default billing and min instances 0, and storage is extra.
