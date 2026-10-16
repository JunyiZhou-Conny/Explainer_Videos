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
- Slide 3 · outline (Recap; Serverless: Cloud Functions; Serverless: Cloud Run)
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
   workflow and the start of "Deployment, Scaling & Automation", at the end of the Prototype
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
  - "Data Collection" and "Setup Experiment Tracking": short bars early in POC.
  - "Build Baseline Models": late POC into early Prototype.
  - "Build Better Models" and "ML Workflow": stacked bars inside Prototype.
  - "Build Cheese App": in MVP.
  - "Deployment, Scaling & Automation": a long bar from mid-Prototype to the end of MVP.

  A red dashed rectangle surrounds the late-Prototype block: Build Better Models, ML Workflow,
  and the first part of Deployment, Scaling & Automation. That rectangle is the "you are here"
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
| "Create a python code file" | 12 | In the README you paste `main.py` and `requirements.txt` into the console's inline editor and set the **entry point**. |
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
  (Cloud Run). This mirrors the VM options of earlier lectures, so the step from L1–L2 is
  "same code, new host" (slide 10).
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
