# L15 lecture slides — ML Workflows with Vertex AI

**Provenance.** One deck: `Lecture15_L15_ml_workflows_with_vertex_ai.pdf` (deck name
`L15_ml_workflows_with_vertex_ai`), 42 slides, titled "Lecture 15: ML Workflows with Vertex AI"
(AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's lecture slides (PDF),
provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page
numbers. This digest is written in our own words from the deck's extracted text and from every
slide image: all five contact sheets, plus enlarged renders of the slides with diagrams or code
(6, 7, 10, 12, 14, 20, 21, 28, 29, 32, 33, 35, 36, 37, 41, 42). Only short titles, terms, URLs
and single code lines are quoted. The tutorial side (repos `dlops-io/model-deployment` and
`dlops-io/ml-workflow`) is documented in [`digest.md`](digest.md). Where this file says "the repo"
or "the README", it means those two repos at the commits recorded there.

## Outline

The agenda on slide 4 has three numbered sections, and the third has one sub-item. Section
dividers (5, 9, 18, 23) repeat the agenda with the current part in bold. From slide 18 on,
section 2 is shortened to "Serverless: Model Deployment". Three slides repeat the slide before
them with a meme added (26, 31, 38), and the last two are picture slides (41, 42).

- **Slide 1 · title.** "Lecture 15: ML Workflows with Vertex AI".
- **Slides 2–3 · announcements.** MS3 grading and the slide-upload deadline (2). Free GPUs,
  models and LLM credits for AIxBio projects, with a giveaway meme GIF (3).
- **Slide 4 · agenda.** Recap; Serverless: Model Deployment with Vertex AI Online Prediction;
  ML Workflow Management, with the sub-item Vertex AI Pipelines.
- **Slides 5–8 · 1. Recap.**
  - 5 · divider ("Recap" in bold)
  - 6 · "Review: Cheese App Status", the POC → Prototype → MVP roadmap
  - 7 · "Cheese App Development": four components on GCP, three ticked
  - 8 · "Recap": Cloud Functions and Cloud Run from L14
- **Slides 9–17 · 2. Serverless: Model Deployment with Vertex AI Online Prediction.**
  - 9 · divider
  - 10 · "Vertex AI": the console sidebar, with four entries mapped to course stages
  - 11 · what serverless model deployment is, with a cost alert and a "burning money" meme
  - 12 · "Serverless Model Deployment": the five-step deployment diagram
  - 13 · "Model Signature": why the signature must change (development vs production)
  - 14 · "Update Model Signature": annotated TensorFlow code
  - 15 · "Tutorial: Serverless Model Deployment": steps, links and a QR code
  - 16 · Vertex AI Online Prediction vs Cloud Run, as bullet points
  - 17 · the same comparison as a ten-row table
- **Slides 18–22 · 3. ML Workflow Management.**
  - 18 · divider
  - 19 · "From Deployment to Workflow Automation"
  - 20 · "ML Workflow: Cheese App", headed "How do we execute these steps?"
  - 21 · the same diagram, headed "Can we automate this flow?" → "Vertex AI Pipelines"
  - 22 · "What is ML Workflow Management?"
- **Slides 23–40 · 3 (sub-item). Vertex AI Pipelines.**
  - 23 · divider ("Vertex AI Pipelines" in bold)
  - 24 · "What is Vertex AI Pipelines?"
  - 25 · "Kubeflow and the DSL"
  - 26 · slide 25 again, overlaid with a meme captioned "What's a DSL?"
  - 27 · "What is a DSL?"
  - 28 · "Building Vertex AI Pipelines": component code (`@dsl.component`)
  - 29 · "Building Vertex AI Pipelines": pipeline code (`@dsl.pipeline`) and compiling to YAML
  - 30 · "From DSL to Running the Pipeline": four steps and the recipe analogy
  - 31 · slide 30 again, overlaid with a meme captioned "What's a SDK?"
  - 32 · "What is SDK", with a You → SDK → Vertex AI sketch
  - 33 · "Running Vertex AI Pipelines": `PipelineJob` code
  - 34 · "Building Vertex AI Pipelines": three steps for your own containers
  - 35 · "Making Container Callable": the Dockerfile entry point, before and after
  - 36 · "Making Container Callable": `docker-entrypoint.sh` with two modes
  - 37 · "Building Vertex AI Pipelines": the Cheese App pipeline graph with each step's duties
  - 38 · slide 37 again, overlaid with a meme captioned "IT'S THAT SIMPLE"
  - 39 · "Tutorial: Vertex AI Pipelines": steps, links and a QR code
  - 40 · "Putting It All Together — From Recipe to Factory"
- **Slide 41 · image only.** A meme GIF captioned "DELETE!!" with no other text. The slide does
  not say what to delete. Coming after a lecture that deploys a billed endpoint (cost alert on
  slide 11), it reads as a reminder to delete cloud resources. That reading is ours.
- **Slide 42 · close.** The text layer reads "THANK YOU". The visible content is a talk-show
  GIF with the captions "Prof. Pavlos" and "Students".

Count check: 1 + 2 + 1 + 4 + 9 + 5 + 18 + 1 + 1 = 42 slides.

## Key ideas

1. **The project has reached deployment and automation.** On the roadmap the class is in the
   Prototype phase, inside the box that holds "Build Better Models", "ML Workflow" and the start of
   "Deployment, Scaling & Automation". Of the four Cheese App components, collector, processor
   and training carry a tick. "Model Deploy" is the one still open. *Slides 6–7.*
2. **Recap of L14.** Cloud Functions run small, event-driven tasks, which suits automating steps
   such as data preparation. Cloud Run runs whole containers, which suits serving models or APIs.
   *Slide 8.*
3. **Vertex AI holds the whole ML lifecycle in one console.** Four sidebar entries map to course
   stages: Workbench for notebooks, Training for training jobs, Online prediction for serverless
   deployment, and Pipelines for building the ML workflow. Today covers the last two. *Slide 10.*
4. **Serverless model deployment puts a trained model behind an endpoint with no servers to
   manage.** It supports online or batch prediction, runs on CPU or GPU, and scales out easily.
   An online endpoint costs money for as long as it is up, and the slide flags this as an alert.
   *Slide 11.*
5. **Deployment is five steps driven from one CLI container.** (1) get the saved model;
   (2) update its signature; (3) upload it to a GCS bucket; (4) upload it to the Vertex AI Model
   Registry; (5) deploy it to an endpoint. The bucket holds the files, the registry holds the
   catalogue entry, and the endpoint is the live service. *Slides 12, 15.*
6. **Move preprocessing into the model.** In a notebook you resize and normalise by hand, one
   cell at a time. A production endpoint should accept raw image bytes and do the preprocessing
   itself on the server, so one request does everything. Otherwise each client prepares data
   slightly differently ("Client-side brittleness"). Keeping the logic in one place also makes
   rollback and versioning easier. *Slide 13.*
7. **How to change the signature in TensorFlow.** Write a per-image preprocessing function. Wrap
   it in a `tf.function` whose input is a batch of strings, and map it over the batch. Chain that
   into the model call inside a serving function. Save the model with that function as its
   `serving_default` signature. *Slide 14.*
8. **Vertex AI Online Prediction vs Cloud Run.** Vertex AI is built for serving ML models: you
   deploy a model directly, and it adds autoscaling, model versioning and A/B testing, monitoring
   and drift detection, batch prediction, and ML-aware IAM. Cloud Run runs any container: you
   must containerise and configure it yourself, it scales on HTTP traffic, and ML monitoring and
   model versioning are up to you. The rule of thumb: use Vertex AI to serve trained models in
   production, and Cloud Run when ML is one part of a broader application. *Slides 16–17.*
9. **From one manual deployment to an automated workflow.** So far each step was run by hand.
   Production needs the data → training → deployment sequence to run by itself, the same way
   each time, with a record of what ran.
   Slide 20 shows the problem: four components, each driven by a person at its own CLI. Slide 21
   asks whether the flow can be automated and answers "Vertex AI Pipelines". *Slides 19–21.*
10. **What ML workflow management does.** It drives the steps from data collection to
    deployment, knows which step needs which and runs them in that order, and makes a run
    repeatable: unchanged code can be run again on fresh data. Scheduling, monitoring and
    resource allocation are part of its job too. *Slide 22.*
11. **Vertex AI Pipelines is Google's managed orchestrator.** Each step is written in Python;
    Vertex executes them with no servers for you to manage, the same way every time, at whatever
    scale is needed. Kubeflow sits underneath, but you set up no Kubernetes. *Slides 19, 24.*
12. **Kubeflow is the machine and the DSL is the recipe.** Kubeflow is an open-source ML-workflow
    engine built on Kubernetes. The DSL (domain-specific language) is a small, purpose-
    built way to describe pipeline steps and how they connect. It is written in Python, so it is
    not a new language to learn. *Slides 25–27.*
13. **Writing a pipeline has three moves: components, pipeline, compile.** A component is a
    decorated Python function with typed inputs and outputs. The pipeline function wires
    components together by passing one task's `.output` into the next call. The compiler then
    writes the whole graph to a YAML file. The toy example squares `a` and `b`, adds the squares
    and takes the square root. With the defaults 3 and 4, the answer is 5. *Slides 28–29.*
14. **From DSL to a running pipeline.** You write the workflow with the KFP DSL. The compiler
    produces YAML. The Google Cloud SDK sends that YAML to Vertex AI. Vertex AI runs the steps one
    by one, serverlessly. An SDK is a toolkit of libraries that lets your own program drive a
    platform; the slide calls it your "remote control for Vertex AI". In code: build an `aip.PipelineJob` from
    the YAML with a pipeline root and a caching flag, then call `job.run()`. *Slides 30, 32, 33.*
15. **Your own containers need three things.** (1) Make each container callable: it accepts
    inputs and produces outputs. (2) Build the images and push them to a registry that Vertex AI
    can reach. (3) Describe in `kfp.dsl` how the steps connect. That structure is a DAG, which
    settles the order of the steps and their dependencies. *Slide 34.*
16. **One image, two modes.** "Callable" here means changing the Dockerfile's entry point from an
    interactive shell to a shell script. The script branches on whether arguments were passed.
    With no arguments (development), it authenticates gcloud with the service-account key, sets
    the project and opens a shell for testing the CLI. With arguments (production), it runs Python
    with them, so `docker run … cli.py --search` executes one task and exits. *Slides 35–36.*
17. **The Cheese App pipeline is a four-step chain.** Each step has its own duties:
    - Data Collector: download images, upload them to GCP.
    - Data Processor: verify images, check for duplicates, convert to TFRecords.
    - Model Training: train, save the model.
    - Model Deploy: upload to the registry, deploy an endpoint.

    *Slides 37–39.*
18. **The whole stack in one chain.** DSL (your recipe) → compiler (YAML, the printed
    instructions) → SDK (the factory operator who submits it) → Kubeflow (the engine that runs
    it) → Vertex AI Pipelines (manages the run serverlessly, step by step). The containers play
    the factory's workers, and the DAG is their running order. *Slide 40.*

**What the slides leave to the tutorial.** The slides do not cover the following. A scene that
needs any of them must take it from `digest.md`:
- the prediction request format: base64 JPEG in `{"b64": …}` under the key `bytes_inputs`
- `model_call` and the 224×224 decode, convert and resize inside `preprocess_image` (both elided
  on slide 14)
- the prebuilt serving container image
- `traffic_split`, replica counts and machine type
- undeploying and deleting the endpoint
- `@dsl.container_component` / `dsl.ContainerSpec`, which is how the repo wraps the data
  collector and processor images (slides 28–29 show only lightweight `@dsl.component` functions)
- `.after()` ordering edges, which is how the repo chains the four Cheese App steps
- what `pipeline_root` and `enable_caching` do
- the service account a pipeline runs as (`job.run(service_account=…)`)
- the launcher pattern, where the training step starts a separate Vertex custom training job
- the fact that the step images live on Docker Hub

## Diagrams

- **Slide 6 · project roadmap (Gantt-style).** This is the picture of L14 slide 5. A wide
  light-blue arrow runs along the top with the labels "POC", "Prototype" and "MVP". Dashed
  vertical lines mark the phase boundaries. Pastel bars sit below, staggered in time:
  - "Design Cheese App": a long bar across POC and Prototype
  - "Data Collection", "Setup Experiment Tracking" and "Build Baseline Models": short bars that
    step forward through POC, the last two crossing a little into early Prototype
  - "Build Better Models" and "ML Workflow": stacked, spanning most of Prototype
  - "Build Cheese App": in MVP
  - "Deployment, Scaling & Automation": from mid-Prototype to the end of MVP

  A red dashed rectangle, covering most of the Prototype column, encloses Build Better Models, ML
  Workflow and the start of Deployment, Scaling & Automation. The slide gives it no label; it
  marks where the class is now.
- **Slide 7 · Cheese App components on GCP.** Four coloured tiles in a row, each with a number
  badge above and an icon:
  - 1 "Data Collector" (red, download icon)
  - 2 "Data Processor" (blue, gears)
  - 3 "Model Training" (yellow, light bulb)
  - 4 "Model Deploy" (green, light bulb in a ring)

  Tiles 1–3 carry a green tick and tile 4 does not. Below the tiles is a dashed "Google Cloud
  Platform" box that holds "Cloud Storage" (left) and "Vertex AI" (right). The arrows:
  - collector: a red elbow arrow into Cloud Storage (it writes)
  - processor: a blue two-headed arrow to Cloud Storage (it reads and writes)
  - training: a gold arrow down into Vertex AI
  - deploy: a green elbow arrow into Vertex AI from the right

  Purpose: only deployment is left, and it lands in Vertex AI.
- **Slide 10 · Vertex AI console map (annotated screenshot).** On the left is a tall, narrow
  screenshot of the Vertex AI sidebar. Its group headings are Tools, Notebooks, Vertex AI Studio,
  Build with Gen AI, Data, Model development, and Deploy and use. Four entries are outlined in
  red, and grey arrows (curved, except the straight top one) run to them from four coloured
  labels on the right:
  - blue "Build ML Workflow" → **Pipelines** (top, under Tools)
  - green "JupyterLab notebooks" → **Workbench** (under Notebooks)
  - pink "Training pipelines and jobs" → **Training** (under Model development)
  - yellow "Serveless deployment" (sic) → **Online prediction** (bottom, under Deploy and use)

  Purpose: one product spans the lifecycle; today uses the bottom and top entries. A re-draw can
  show a four-row sidebar with the L13 row (Training) already done and the two L15 rows lighting
  up. L13 slide 21 has the same map with three entries.
- **Slide 12 · serverless model deployment, five steps (the central deployment diagram).** The
  left half is your machine. The right half is a dashed box labelled **GCP** (Google Cloud logo).
  Pink numbered step labels 1–5 sit beside the arrows. A light-bulb icon stands for the model:
  orange for the original model, green once the signature has been updated.
  - **1 "Get Saved Model"**: a dashed box with an orange bulb, labelled "Saved Model". A grey
    elbow arrow runs from it down into a green box at the bottom centre, **"Model Deployment CLI
    Container"**.
  - **2 "Update Model Signature"**: a grey arrow goes from the CLI container up into a second
    dashed box. It holds a small code thumbnail, a plus sign and a green bulb, and is labelled
    "Saved Model + Update Signatures".
  - **3 "Upload to GCS"**: a hollow green arrow runs from the step-2 box right into a grey **"GCS
    Bucket"** panel at the top of the GCP box, which now holds a green bulb.
  - A hollow green arrow runs down from the bucket into a blue-grey **"Vertex AI"** panel. The
    panel holds two framed boxes: **"Model Registry"** (two green bulbs) and **"Model
    Endpoints"** (two bulbs in rings, each with a chain-link icon, i.e. reachable). A hollow
    arrow runs from Registry to Endpoints.
  - **4 "Upload to Model Registry"** and **5 "Deploy Model Endpoint"** label a single grey arrow
    from the CLI container right into the Vertex AI panel. Step 4 is written above the arrow and
    step 5 below it.

  Purpose: separate the stored artefact (bucket), the catalogue entry (registry) and the running
  service (endpoint), and show that one local container drives every step. Re-draw note: in the
  repo, steps 2 and 3 happen in one call, because `tf.saved_model.save` writes straight to
  `gs://` (`python cli.py --prepare`). Steps 4 and 5 are one command, `python cli.py --deploy`.
- **Slide 14 · annotated serving-signature code.** A dashed code panel with three coloured
  callouts on the right, each joined to the code by a curved grey arrow:
  - blue "Define preprocessing function" → `preprocess_image`
  - green "Define @tf.function for new model signature" → the two decorated functions
    `preprocess_function` and `serving_function`
  - pink "Save Model with the new model signature" → the `tf.saved_model.save(` call (the
    arrow lands on its `prediction_model,...,` line, just above `signatures=`)

  The mechanism a scene can draw: a batch of byte strings → `preprocess_function` (maps
  `preprocess_image` over the batch) → a dict keyed `"model_input"` → `model_call` →
  results. The whole chain is stored under the name `serving_default`.
- **Slides 20–21 · the manual workflow (before picture).** The four tiles of slide 7 again,
  numbered 1–4, with no ticks. Under each tile is a pale two-headed vertical arrow to a group-of-
  people icon in the tile's colour, labelled **"CLI"**: a human drives every step at a terminal.
  The solid arrows into the dashed "Google Cloud Platform" box are the same as on slide 7. The
  only difference between the two slides is the red headline: slide 20 says "How do we execute
  these steps?". Slide 21 says "Can we automate this flow?", followed by a grey hollow arrow to
  a blue "Vertex AI Pipelines". Purpose: motivate orchestration. Re-draw idea: four people at
  four terminals, then one orchestrator replaces them.
- **Slides 28–29 · sample pipeline (annotated code; the graph is implied, not drawn).**
  - Slide 28's callouts: blue "Import kubeflow pipeline" → `from kfp import dsl`; green "Define
    pipeline components" → three `@dsl.component` functions.
  - Slide 29's callouts: pink "Define Pipeline, an orchestration of how you want your component
    tasks to run" → `@dsl.pipeline`; green "Compile pipeline into a yaml file" →
    `compiler.Compiler().compile(`.

  The graph the code defines is Y-shaped: two branches merge. Two independent `square` tasks
  (inputs `a`=3 and `b`=4) can run in parallel. Both feed `add`, and `add` feeds `square_root`, which returns 5.0.
  Every edge here is a data edge made by passing `.output`. This is the picture to draw for "the
  DAG is built from data dependencies".
- **Slide 32 · You → SDK → Vertex AI.** A small black line drawing at the bottom: a box with the
  Python logo labelled "You (Python code)" → arrow → a box "SDK" → arrow → a cloud "Vertex AI".
  An "SDK" monitor icon sits in the top-right corner. Purpose: the SDK sits between your code and
  the platform.
- **Slide 33 · annotated pipeline-job code.** Three callouts: blue "Import Google Cloud SDK" →
  the import line; green "Create a pipeline job" → `aip.PipelineJob(` and its arguments; pink
  "Run pipeline job in Vertex AI" → `job.run()`.
- **Slide 35 · Dockerfile before and after.** Two dashed code panels titled "Dockerfile". The
  left one sits lower and the right one higher. Both start from the same base image, elide the
  middle with dots, and copy the source. Only the last line differs. The left panel ends with
  `ENTRYPOINT ["uv", "shell"]` and the right panel with
  `ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]`. A curved arrow runs from the left panel's
  entry-point line down to one blue label, "Change entrypoint to a shell file", and a second
  curved arrow runs from that label up to the right panel's entry-point line. Purpose: making a
  container callable is a one-line change plus a script.
- **Slide 36 · the entry-point script forks.** A dashed panel with `docker-entrypoint.sh`.
  It stores the arguments, then an `if [[ -z ${args} ]]` test splits it into two branches:
  - A blue callout, top right, reads "Development mode: Authenticated to GCP, run a shell to test
    cli inside container". It points into the `then` branch: `gcloud auth
    activate-service-account`, `gcloud config set project`, open a shell.
  - A pink callout, bottom, reads "Production mode: Run container using 'docker run ... cli.py
    —search'". It points at the `else` line, `uv run python $args`.

  Re-draw: one container image with a switch on its input. No arguments routes to an interactive
  shell with credentials. Arguments route to a single CLI run that exits.
- **Slide 37 · Cheese App pipeline graph (the central pipeline diagram).** On the left are four
  white node boxes in a zig-zag (left, right, left, right): **Data Collector** (maroon),
  **Data Processor** (navy), **Model Training** (brown/gold) and **Model Deploy** (green). Each
  node has an open-box icon in its colour and a round check badge at its right end, like a
  succeeded run in the Vertex AI Pipelines console graph. Grey curved arrows link
  them in order 1 → 2 → 3 → 4. On the right, a column of four pastel cards (pink, blue, yellow,
  green) lines up with the nodes and lists each step's duties (key idea 17). Purpose: the target
  topology, a linear chain where every step succeeds. **Slide 38** is the same picture with an
  "IT'S THAT SIMPLE" meme over the middle. Re-draw note: in the repo the edges are `.after()`
  ordering edges with no data passed. Data moves through files in the bucket, and on `main` the
  processor no longer writes TFRecords (`digest.md` §3.6 and §10, item 2).
- **Slide 40 · recipe-to-factory chain (a list, not a drawing).** It is five numbered items that
  can be drawn as a left-to-right assembly line: DSL (recipe) → compiler (printed YAML) → SDK
  (operator) → Kubeflow (engine) → Vertex AI Pipelines (manager). Containers are the workers and
  the DAG is their job sheet.
- **Not diagrams:**
  - slide 17 is a comparison table (key idea 8)
  - slides 15 and 39 carry QR codes beside the tutorial links
  - slides 3, 11, 26, 31, 38, 41 and 42 carry meme images, and slide 1 the Harvard shield

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Vertex AI Online Prediction" / "Online prediction" | 4, 5, 9, 10, 11, 16, 17 | Same name as the console entry. The README says it deploys "as an endpoint in Vertex AI Online prediction". |
| "Serverless model deployment" | 4, 5, 9, 11–15, 18, 23 | The README title is "Cheese App: Model Deployment Demo". In the repo the endpoint runs on one always-on node (`min_replica_count=1`), so here "serverless" means no servers to manage, not scale to zero. |
| "online" vs "batch" prediction | 11, 17 | The tutorial uses only online prediction. |
| "Saved Model", "Get Saved Model" | 12 | In the repo, `--prepare` downloads a `.keras` model from a GitHub release (the README says it used to come from W&B) and writes a TF SavedModel. |
| "Model Signature", "Update Model Signature", "Update Model Serving Signature" | 12–15 | The README calls this step "Prepare Model for Deployment" (`python cli.py --prepare`). The ml-workflow README says the Model Deploy step does it, but in the pipeline code the trainer does (`digest.md` §10, item 2). The digest says "serving signature" / `serving_default`. |
| "serving function", "preprocessing function" | 13, 14 | The same function names as `model-deployment/cli.py`. |
| "Client-side brittleness" | 13 | The digest calls the same risk training/serving skew. |
| "raw image bytes" | 13 | On the wire, the client base64-encodes the JPEG as `{"b64": …}` under the key `bytes_inputs`. The slides do not show this. |
| "GCS Bucket", "Upload to GCS" | 12, 15 | README "Create GCS Bucket"; the variable is `GCS_MODELS_BUCKET_NAME`. |
| "Model Registry", "Upload to Model Registry" | 12, 15 | README "Vertex AI Model Registry"; in the SDK, `aiplatform.Model.upload`. |
| "Model Endpoints", "Deploy Model Endpoint", "Deploy Model as an Endpoint" | 12, 15 | README "Model Endpoints". `model.deploy` creates a new Endpoint, and `--deploy` does the registry upload and the deploy together. |
| "Model Deployment CLI Container" | 12 | The `model-deployment` container that `docker-shell.sh` starts. |
| "ML Workflow", "ML Workflow Management" | 4–6, 9, 10, 18–23 | README title "Cheese App: ML Workflow Management". |
| "Vertex AI Pipelines" | 4, 5, 9, 18, 19, 21, 23–26, 28, 29, 33, 34, 37–40 | Same. |
| "Kubeflow" (slide 28's code comment: "Kubeflow Pipelines") | 19, 24–26, 28, 40 | Strictly, the part used is Kubeflow Pipelines (KFP v2): the `kfp` SDK and its compiled YAML format. Vertex runs that YAML on a managed backend, so no Kubeflow or Kubernetes cluster is ever visible to you. The digest says "KFP". |
| "DSL" (Domain-Specific Language), "KFP DSL (kfp.dsl)" | 25–31, 34, 40 | The digest's "pipeline DSL". |
| "component", "pipeline components", "component tasks" | 28, 29 | The slides show only lightweight `@dsl.component` functions. The repo's data steps use `@dsl.container_component` returning `dsl.ContainerSpec`, and its training and deploy steps use `@dsl.component(base_image=…, packages_to_install=…)`. |
| "Pipeline" (`@dsl.pipeline`), "orchestration" | 19, 24, 29 | Same. |
| "compiler", "YAML file", "printed recipe card" / "printed instructions" | 29, 30, 40 | The digest calls the file a PipelineSpec YAML. The repo files are `pipeline.yaml`, `sample-pipeline1.yaml`, `data_collector.yaml` and others. |
| "SDK", "Google Cloud SDK (google.cloud.aiplatform)", "Google Cloud AI Platform SDK" | 30–33, 40 | The package is `google-cloud-aiplatform`, the Vertex AI SDK for Python. "Google Cloud SDK" usually means the `gcloud` CLI tools, which are a different thing; keep the two apart on screen. |
| "Pipeline Job" (`aip.PipelineJob`) | 33 | Same. In the repo, `job.run(service_account=GCS_SERVICE_ACCOUNT)`; the README grants the "Service Account User" role for it. |
| `PIPELINE_ROOT`, `enable_caching` | 33 | Shown but not explained. Per the digest, `pipeline_root` is the GCS folder for step outputs and metadata, and `enable_caching=False` forces every step to re-run. |
| "Make containers callable", "Making Container Callable" | 34–36, 39 | No README heading uses this name. The README goes straight to "Build & Push Images". |
| "Build & push images" to "Artifact Registry or Container Registry" | 34, 39 | The README pushes to **Docker Hub** (`docker push <USER NAME>/<IMAGE_NAME>`). The pipeline pulls `dlops/cheese-app-data-collector` and `dlops/cheese-app-data-processor`. Google has since retired Container Registry in favour of Artifact Registry. |
| "DAG (Directed Acyclic Graph)" | 34, 40 | The digest separates data edges (`.output`, slide 29) from ordering edges (`.after()`, the Cheese App pipeline). |
| "Development mode" / "Production mode" | 36 | In the repo: the interactive container started by `docker-shell.sh`, vs the arguments Vertex passes to the step image. |
| "Data Collector", "Data Processor", "Model Training", "Model Deploy" | 7, 20, 21, 37, 38 | Same component names as the README. |
| "TF Records" | 37, 38 | The README also says the processor converts to TFRecord format, but on `main` it no longer does, and training does not read the processor's output (`digest.md` §10, item 2). |
| "Workbench" / "JupyterLab notebooks", "Training" / "Training pipelines and jobs", "Pipelines" / "Build ML Workflow" | 10 | Console entries (see L13 slide 21). |
| "POC", "Prototype", "MVP"; "MS3" | 6; 2 | Project phases; milestone 3. |
| "Cloud Functions", "Cloud Runs" (sic) | 8 | L14's products. Google now calls the first one "Cloud Run functions" (see the L14 SLIDES.md). |

## Commands and code on the slides

The slides contain no shell commands to type, apart from the `docker run` hint on slide 36. The
code lines below are quoted exactly as the slides show them, including slide typos (marked
*sic*), with a note where the repo differs.

- **Slide 14** (serving signature):
  - `def preprocess_image(bytes_input):` — its body is elided as `resized = ...`. In the repo it
    decodes the JPEG, converts it to float32 and resizes it to 224×224.
  - `@tf.function(input_signature=[tf.TensorSpec([None], tf.string)])`
  - `def preprocess_function(bytes_inputs):`
  - `preprocess_image, bytes_inputs, dtype=tf.float32, back_prop=False` — the arguments of
    `tf.map_fn(`. `dtype` and `back_prop` are deprecated arguments, and TF prints warnings.
  - `return {"model_input": decoded_images}`
  - `def serving_function(bytes_inputs):`
  - `results = model_call(**images)` — `model_call` is not defined on the slide. In the repo it
    is a concrete function of the Keras model with a `[None, 224, 224, 3]` float input named
    `model_input`.
  - `signatures={"serving_default": serving_function},` — inside `tf.saved_model.save(`, after
    `prediction_model,...,`.
- **Slide 28** (components):
  - `from kfp import dsl`
  - `@dsl.component`
  - `def square(x: float) -> float:`
  - `def add(x: float, y: float) -> float:`
  - `def square_root(x: float) -> float:`
- **Slide 29** (pipeline and compile):
  - `@dsl.pipeline`
  - `def sample_pipeline(a: float = 3.0, b: float = 4.0) -> float:`
  - `sum_task = add(x=a_sq_task.output, y=b_sq_task.output)`
  - `return square_root(x=sum_task.output).output`
  - `compiler.Compiler().compile(` with `sample_pipeline, package_path="sample-pipeline.yaml"`.
    The `compiler` import (`from kfp import compiler`) is not shown. The repo compiles to
    `sample-pipeline1.yaml`, which is the name slide 33 loads.
- **Slide 33** (run):
  - `from import google.cloud.aiplatform import aip` (*sic*, not valid Python). The repo has
    `import google.cloud.aiplatform as aip`.
  - `job = aip.PipelineJob(`
  - `template_path="sample-pipeline1.yaml",`
  - `pipeline_root=PIPELINE_ROOT,`
  - `enable_caching=False,`
  - `job.run()` — the repo passes `service_account=GCS_SERVICE_ACCOUNT`.
- **Slide 35** (Dockerfile):
  - `FROM python:3.9-slim-buster` — this is the old Pipenv-era base image. On `main` the two
    pipeline step images (data-collector, data-processor) use `python:3.12-slim-bookworm`; the
    local `workflow` and `model-training` images use `python:3.13-slim-bullseye`.
  - `RUN --chown=app:app . /app` (*sic*). `--chown` belongs to `COPY`/`ADD`, and the repo has
    `COPY --chown=app:app . ./`.
  - Before: `ENTRYPOINT ["uv", “shell”]` (*sic*: curly quotes around `shell`, which would also
    break Docker's JSON form; normalised to `["uv", "shell"]` elsewhere in this file). uv has no
    `shell` subcommand (checked with uv 0.11:
    "unrecognized subcommand"). The line reads like `pipenv shell` with the tool name swapped.
  - After: `ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]` — the repo has the same line
    without `./`.
- **Slide 36** (`docker-entrypoint.sh`):
  - `args = "$@"` (*sic*). Bash does not allow spaces around `=`, and the repo has `args="$@"`.
  - `if [[ -z ${args} ]];`
  - `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`
  - `gcloud config set project $GCP_PROJECT`
  - `uv shell` (see above). In the repo, the two pipeline step images (data-collector,
    data-processor) have this argument fork, but they activate `/.venv` before the test, their
    no-argument branch only runs `exec /bin/bash`, and they do no gcloud login. The `workflow`, `model-training` and
    `model-deployment` entrypoints do the gcloud login but have no fork. Slide 36 merges the
    two patterns into one script.
  - `uv run python $args`
  - Callout: `docker run ... cli.py —search` (an em dash on the slide; the flag is `--search`).
- **Module names in prose:** `kfp.dsl` (30, 34), `google.cloud.aiplatform` (30).

## What the lecture stresses

- **Endpoints cost money while they are up.** "For online predictions there is an ongoing cost"
  and, in red, "Alert: Continuous cost to keep endpoint up", next to a "burning money" meme
  (slide 11). The image-only "DELETE!!" slide that closes the content (41) most likely makes the
  same point.
- **Preprocess on the server, not in each client** (slide 13):
  - the endpoint should take raw bytes
  - one request does everything
  - each client preprocessing slightly differently is a source of bugs ("Client-side
    brittleness")
  - one central copy of the logic makes rollback and versioning easier

  "Bottom line": preprocessing and inference belong together in the endpoint.
- **Best practice for choosing a host** (slide 16): Vertex AI when the job is serving a trained
  model in production; Cloud Run when ML is one piece of a larger app or pipeline. The trade-off
  (slides 16–17): Vertex is specialised and managed, while Cloud Run is general but leaves ML
  monitoring and model versioning to you.
- **Automate instead of running steps by hand.** Production needs the sequence automated,
  repeatable and traceable (slide 19). Workflow management makes runs reproducible and repeatable on new data,
  and handles dependencies, order, scheduling, monitoring and resources (slide 22).
- **Managed means no Kubernetes work** (slides 24–25).
- **The DSL is not a new language** ("Remember:", slide 27); it is plain Python with decorators.
- **Containers must be callable and reachable** (slide 34): each step container takes inputs
  and produces outputs, and its image must sit in a registry Vertex AI can pull from.
- **The DAG decides order and dependencies** (slides 34, 40).
- **Keep one image for development and production** (slides 35–36): the entry point switches on
  whether arguments are present.
- **"IT'S THAT SIMPLE"** (slide 38) is played as irony over the four-step pipeline.

**Cautions for scene authors.** These are our notes, not the lecture's:
- **Pick one analogy mapping and use it consistently.** Slide 30 calls the SDK "the chef who
  follows" the recipe, while slide 40 calls it the operator who *sends* the YAML, with Kubeflow
  as the engine that runs it. Use slide 40's mapping: the SDK only submits; it never executes
  steps.
- **Slides 16–17 describe what the platform offers, not what the tutorial uses.**
  - The repo deploys with `min_replica_count=1` and `max_replica_count=1`, so the "built-in
    autoscaling" is never exercised.
  - Drift detection comes from Vertex AI Model Monitoring, which has to be configured.
  - Cloud Run has revisions with traffic splitting, so the versioning contrast concerns
    ML-model versioning only.
- **Slide 37's step cards describe the intended design.** On `main`, TFRecords are not produced
  and training does not read the processor's output (`digest.md` §10).

## Pointers

- **Slide 2:** MS3 updates.
  - A "peer and self evaluation" on Canvas (a link): 1 point for the evaluation itself, and 4
    points of adjustment based on peer, self and TF evaluation of contribution and meeting
    attendance.
  - 20 points for the presentation, judged on technical depth, business acumen, clarity and
    structure, visual communication, and engagement and delivery.
  - Upload slides to Canvas by noon on Tuesday.
- **Slide 3:** free GPUs, models and LLM credits for AIxBio projects. The slide gives no link.
- **Slide 8:** L14 (`dlops-io/serverless-deployment`), recapped.
- **Slide 10:** the Vertex AI console entries Pipelines, Workbench, Training and Online
  prediction.
- **Slide 15:**
  - Tutorial "Serverless Model Deployment": `https://github.com/dlops-io/model-deployment`
  - "View Model Endpoints": `https://console.cloud.google.com/vertex-ai/online-prediction/endpoints`
  - "View Model Registry": `https://console.cloud.google.com/vertex-ai/models`
  - A QR code beside the links
- **Slide 39:**
  - Tutorial "Cheese App Workflows":
    `https://github.com/dlops-io/ml-workflow#cheese-app-ml-workflow-management`
  - "View Vertex AI Pipelines": `https://console.cloud.google.com/vertex-ai/pipelines/runs`
  - A QR code beside the links
- **Slides 6–7:** the Cheese App roadmap. Model Deploy is the remaining component, and the
  training step from L13 is shown as done.
- **Slide 41:** an implied clean-up reminder; the slide has no text. For the actual clean-up
  commands (undeploy, then delete the endpoint), see `digest.md` §2.
- The slides list no readings, demos or homework beyond these.

## This video and the slides

**Basis.** The video is not scripted yet. This folder has no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the ten planned sections in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L15-vertex-ml-workflows.md`) and every slide: the extracted text, all five contact sheets, and the enlarged renders of slides 33 and 36, re-checked for the code conflicts. With no captures yet, "what the tutorial does today" means the two repos at the commits recorded in `digest.md` (`model-deployment` @ `3fbf63f`, `ml-workflow` @ `972ffbb`). The Dockerfiles, entrypoints, the `--sample` submit code and the deploy settings were re-read in those clones on 2026-10-16. When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 4, 6, 8 and 9 against them; if they disagree, the captures win.

**Two README images are lecture diagrams.** `model-deployment/images/serverless-model-deployment.png` is the same drawing as slide 12 (five numbered steps, the CLI container, the GCS bucket, Registry and Endpoints). `ml-workflow/images/ml-pipeline.png` is the same graph as the left half of slide 37 (four boxes with check badges), without the duty cards. Plan section 1 puts the first image on screen, section 6's animation ends on the second, and section 9's console graph has the same four-step shape, so those beats already stand on lecture ground.

### 1. Map: planned sections ↔ slides

| # | Planned section (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | Cold open: from file to answer (2 min) | 6–7, 10–12 | Same concept. Slide 12 is the deployment picture, with the bucket, the registry and the endpoints. The plan's "runtime" slot (the prebuilt serving image) is tutorial-only: the slides never show it. |
| 2 | The serving signature (5 min) | 12 (steps 1–3), 13–15 | Same concept, and the tutorial applies it. `python cli.py --prepare` runs slide 14's code with the elided parts filled in, and does slide 12's steps 1–3 in one command. |
| 3 | Registry vs endpoint (4 min) | 11, 12 (steps 4–5), 15, 16–17 | The tutorial applies slides 12 and 15: `python cli.py --deploy` does steps 4 and 5 together. DeployedModel, `traffic_split` and `sync=False` are tutorial-only. The Vertex-vs-Cloud-Run comparison (16–17) is lecture-only (gap 2). |
| 4 | Speaking the endpoint's language (4 min) | 13 (the "raw image bytes" goal), 15 (the "View Model Endpoints" link) | Mostly tutorial-only. The lecture states the goal; the `{"b64": …}` wrapper and the `bytes_inputs` key come from the repo. |
| 5 | Turn the meter off (2 min) | 11 (cost alert), 41 | Same concept. The undeploy and delete commands are tutorial-only (and not in the README either, `digest.md` §2). |
| 6 | Why a pipeline? (3 min) | 7, 19–22, 24 | Same concept. The plan's "four terminals and a stick figure running between them" is slide 20's picture, and the move to a DAG is slide 21's answer. |
| 7 | Components: lunchbox vs recipe (5 min) | 27–28, 34–36 | Same concept for lightweight Python components (28) and callable containers (34–36). Container components (`dsl.ContainerSpec`) and the argument re-splitting puzzle are tutorial-only. |
| 8 | Tracing and compiling (5 min) | 25–30, 34 (step 3) | The tutorial applies it: `python cli.py --sample` is slides 28–29's code. Tracing at decoration time and `.after()` edges are tutorial-only. |
| 9 | Running on Vertex (5 min) | 30–33, 34 (step 2), 37–39 | The tutorial applies it (`python cli.py --pipeline`; the console graph is slide 37's graph). Service accounts, the launcher and the GCS noticeboard are tutorial-only, and the plan's twist contradicts slide 37's cards (Conflicts 1–3). |
| 10 | Debugging tour and recap (3 min) | 40, 41 | Slide 40 is the lecture's own recap (gap 3). The debugging list is tutorial-only. |
| — | not in the plan | 1–5, 8, 9, 18, 23, 42; 26, 31, 38 | Lecture-only: title, announcements, agenda and section dividers, the L14 recap (8), the close. 26, 31 and 38 repeat 25, 30 and 37 with a meme added. |

### 2. Already in common

| # | Concept | Section ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Serving needs an artifact in a bucket, a registry entry and a live endpoint, all driven from one local CLI container | §1, §3 ↔ 12, 15 | Mostly. Of the plan's triad (artifact, runtime, address), the artifact and the address are slide 12's GCS bucket and Model Endpoints. The runtime (the serving image) has no box on the slide, and the slide's Model Registry has no slot in the triad (the plan brings it in at §3). The digest's "all calls go out from your laptop" is slide 12's single "Model Deployment CLI Container". |
| 2 | Preprocessing belongs inside the model; the endpoint takes raw bytes | §2 ↔ 13 | Yes. The lecture's "Client-side brittleness" is the digest's training/serving skew (§3.1). The lecture adds an argument the plan lacks: one central copy of the logic makes rollback and versioning easier. |
| 3 | The serving-signature code: per-image preprocessing, `tf.map_fn` over a string batch, a serving function, saved as `serving_default` | §2 ↔ 14 | Yes, line for line. `model-deployment/cli.py:94-122` is slide 14 with the bodies filled in (decode, convert, resize to 224×224; `model_call`). |
| 4 | Registering is not deploying; an endpoint costs money while it is up | §3, §5 ↔ 11, 12, 41 | Yes. The plan is more concrete (one always-on node, a new endpoint on every deploy), which sharpens slide 11's alert. |
| 5 | From people at four CLIs to automation | §6 ↔ 19–21 | Yes, closely: the same four components, and the same move from a person at each terminal to one automated flow. |
| 6 | Workflow management records dependencies and runs steps in order | §6, §8 ↔ 22, 34 (step 3), 40 | Yes on order. The lecture's "re-run with new data" does not hold for this repo (Conflict 2). |
| 7 | Vertex AI Pipelines is managed Kubeflow Pipelines; no cluster to set up | §8, §9 ↔ 19, 24–25 | Yes. The digest says "Kubeflow Pipelines (KFP) v2 DSL" (§1), the lecture says "Kubeflow"; see Terms. |
| 8 | A component is a decorated Python function with typed inputs and outputs; the DSL is plain Python | §7 ↔ 27–28 | Yes for lightweight components. The plan goes further: the cheese pipeline's data steps are container components, which the slides do not show. |
| 9 | Passing `.output` wires the DAG, and the compiler writes it to YAML | §8 ↔ 29 | Yes. It is the same sample (squares of 3 and 4 → add → square root = 5.0). The plan adds tracing and the second edge type, `.after()`. |
| 10 | Python DSL → YAML → SDK → Vertex AI runs the steps | §8, §9 ↔ 30, 32–33, 40 | It agrees on the mechanism. The analogies differ: the digest uses a play and a conductor (§3.6–3.7), the lecture a recipe and a factory, and slides 30 and 40 disagree with each other (Conflict 10). |
| 11 | Submitting with `aip.PipelineJob(...)` and `.run()` | §9 ↔ 33 | Yes. The repo adds `aip.init` and the service account (Conflict 9). |
| 12 | A step container must be callable: its entry point branches on whether arguments were passed | §7 ↔ 34–36 | Partly. The plan uses `docker-entrypoint.sh` only for the `brie+cheese` puzzle and never states the lecture's point, one image with a development and a production mode (gap 1). |
| 13 | Step images must sit in a registry Vertex can pull from | §7, §9 ↔ 34, 39 | Yes in principle. The registry differs (Conflict 6). |
| 14 | The Cheese App pipeline is a four-step linear chain that ends with every step ticked | §6, §9 ↔ 7, 20–21, 37–39 | Yes on topology: the README's `ml-pipeline.png` is slide 37's graph. The step duties and the meaning of the arrows differ (Conflicts 1–3). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **One image, two modes: what makes a container a pipeline step (slides 34–36).** Slide 34's three steps (make each container callable, build and push the image, describe the DAG) are a checklist for all of Part B. Slides 35–36 say what "callable" means: the entry point becomes a script that opens a shell when no arguments are given (development mode) and runs the CLI and exits when they are (production mode). This explains what students see. `sh docker-shell.sh` drops them into a shell, while Vertex runs `cli.py --search …` from the same image, and that is why testing the collector by hand in B2 means anything for B7. **Carry it in** §7, before the `brie+cheese` pause and ponder, and plant it in §6 when B2–B3 run at speed.
2. **Why a Vertex endpoint and not Cloud Run (slides 8, 16–17).** The student deployed to Cloud Run one lecture ago and will ask why this needs a different service. The lecture's answer: Vertex serves a model directly and adds ML extras; Cloud Run runs any container you build. The rule of thumb is Vertex for serving trained models and Cloud Run when ML is one part of a larger app. The cost difference is the one the student will feel: Cloud Run can scale to zero, while this endpoint keeps a node running (Conflict 4). **Carry it in** §3, as a two-column card, with one line repeated in §5.
3. **The recipe-to-factory chain as the content recap; the SDK as a remote control (slides 30, 32, 40).** The plan ends on a debugging checklist, but the content gates require a content recap. Slide 40's five links (DSL → compiler → SDK → Kubeflow → Vertex AI Pipelines, with containers as workers and the DAG as their order) are that recap, and slide 32's "remote control" line explains in one sentence what `aip` is. **Carry it in** §8 (introduce the chain and the SDK) and §10 (replay it as the recap).
4. **Where things live in the console (slides 10, 15, 39).** One Vertex AI sidebar holds Workbench, Training (L13), Online prediction and Pipelines. The tutorial's console checks happen on the Endpoints, Model Registry and Pipelines runs pages, which slides 15 and 39 link to. **Carry it in** §1 (the four-row sidebar) and as the console beats in §3, §4 and §9.
5. **Where L15 sits in the project (slides 6–7).** On the roadmap the class is in Prototype, with "Build Better Models", "ML Workflow" and the start of deployment inside the red box. Of the four components, only Model Deploy is not ticked yet. Slide 7's arrows also show what each component touches: the collector writes to Cloud Storage, the processor reads and writes it, and training and deploy go to Vertex AI. **Carry it in** §1 (ten seconds, as orientation) and §6 (as the starting picture).
6. **What else workflow management does (slides 22, 24).** It handles scheduling, monitoring and resource allocation, and makes runs reproducible. The tutorial touches resources (`.set_cpu_limit("500m")`) and monitoring (the console graph). Nothing schedules the pipeline: L23 triggers it from GitHub Actions. **Carry it in** §6 as a four-item card that ticks what this repo uses, and in §10.
7. **Online vs batch prediction (slides 11, 17).** Vertex offers both, and the tutorial only uses online prediction. **Carry it in** §3, in one sentence.

### 4. Conflicts

No captures exist yet, so "today" is the repo at the digest's commits. The captures will decide once they are made.

| # | Slides say | Tutorial today | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **The processor's duties** (slides 37–38): verify images, check for duplicates, "Convert to TF Records". `ml-workflow/README.md:5` says the same. | The processor removes duplicates with difPy, deletes undecodable JPEGs and uploads `clean.zip`. TFRecords are no longer made: the import is commented out (`ml-workflow/src/data-processor/cli.py:19`), and `--prepare` crashes and was removed from the pipeline in commit `dd5253d` (`digest.md` §6 item 9, §7). | The repo | "The lecture's card shows the processor this pipeline was designed with, and the older version of the repo really did write TFRecords. Today it stops at `clean.zip`." Grey out the third line of the re-drawn card. |
| 2 | **Data flows down the chain** (slides 19, 22, 37): a sequence that handles data → training → deployment, and the same code can re-run on new data. | The edges are `.after()` ordering edges with no data passed (`ml-workflow/src/workflow/cli.py:229`, `:244`, `:252`). The trainer downloads the fixed `cheese_4_labels.zip` from GitHub (`ml-workflow/src/model-training/package/trainer/task.py:103-107`), so `raw.zip` and `clean.zip` are never read downstream (`digest.md` §10 item 2). | The repo | "The lecture's arrow is what a pipeline is for. In this repo the arrow between processor and trainer only sets the order: training brings its own dataset. Exercise E4 turns it back into a data edge." This is the plan's §9 twist; tag it with slide 37 so it reads as "the lecture's picture, looked at closely". |
| 3 | **Where the signature is updated** (slides 12, 15): a deployment step done from the Model Deployment CLI container. `ml-workflow/README.md:7` also gives it to Model Deploy. | Part A matches the slide in substance, but `--prepare` does steps 1–3 in one call and `--deploy` does steps 4–5. In the pipeline, the trainer writes the signature when it saves the model (`ml-workflow/src/model-training/package/trainer/task.py:350-383`), and the deploy component only uploads and deploys (`ml-workflow/src/workflow/model.py:70-104`). That matches slide 37's own deploy card ("Upload to Registry", "Deploy model Endpoint") but not the README. | The code | "Same signature, different place. In Part A you add it just before deploying; in the pipeline the trainer adds it as it saves." Show the two-command grouping of slide 12's five steps. |
| 4 | **"Serverless" and scaling** (slides 11, 16–17): deploy with no servers, scale out easily, built-in autoscaling. | Both deploys pin `min_replica_count=1`, `max_replica_count=1` (`model-deployment/cli.py:146-147`, `ml-workflow/src/workflow/model.py:100-101`): one always-on node (`n1-standard-2` by SDK default in Part A, `n1-standard-4` in Part B), billed 24/7 with zero traffic and never scaled to zero, and every deploy creates a new endpoint. | Both: the platform can autoscale if `max_replica_count` > 1, but this tutorial pins one node | "Serverless here means no server for *you* to manage, not no server running. Unlike your Cloud Run service from last lecture, this endpoint does not scale to zero, which is why the lecture flags the cost." |
| 5 | **ML extras** (slides 16–17): versioning and A/B testing, built-in monitoring and drift detection; Cloud Run has "no native support" for model versioning. | The tutorial uses none of them. Each deploy gets `traffic_split={"0": 100}` on a fresh endpoint, and no Model Monitoring job is configured. Cloud Run does have revisions with traffic splitting, so the lecture's contrast holds for *ML model* versions (the registry), not for deployments in general. | Both: the features exist and are opt-in | "These are things Vertex *can* do; this tutorial switches none of them on. Exercise E5 tries the A/B split on one endpoint." Mark them "available, not used here" on the comparison card. |
| 6 | **Where step images live** (slides 34, 39): push to Artifact Registry or Container Registry; "Build & Push Image" is a tutorial step. | The pipeline pulls `dlops/cheese-app-data-collector` and `dlops/cheese-app-data-processor` from **Docker Hub** (`ml-workflow/src/workflow/cli.py:27-28`). The README pushes with `docker push <USER NAME>/<IMAGE_NAME>` and says the step "has already been done" (`ml-workflow/README.md:131-138`). Google has since retired Container Registry. Vertex runs amd64 images, which the slides do not mention (`digest.md` §6 item 2). | The repo (Docker Hub); Artifact Registry for a Google-hosted registry | "Any registry Vertex can pull from works. The course images are public on Docker Hub and already pushed, so you skip this step unless you change the step code. If you host images on Google, use Artifact Registry: Container Registry is gone. Whatever you push must include amd64." |
| 7 | **The Dockerfile** (slide 35): `FROM python:3.9-slim-buster`, a `RUN --chown=app:app . /app` line, and `ENTRYPOINT ["uv", "shell"]` before the change. | The step images use `FROM python:3.12-slim-bookworm`, `COPY --chown=app:app . ./` and `ENTRYPOINT ["/bin/bash","docker-entrypoint.sh"]` (`ml-workflow/src/data-collector/Dockerfile:2`, `:50`, `:53`). uv has no `shell` subcommand; the slide's "before" line reads like `pipenv shell` from the Pipenv era. | The repo | "The lecture's point is the one-line switch from an interactive shell to a script. Here is the real file." Show the repo's last line, not the slide's "before" line. |
| 8 | **The entry-point script** (slide 36): one script whose development branch authenticates gcloud with the key, sets the project and runs `uv shell`; written `args = "$@"`. | The step images fork exactly as the slide says, but they activate `/.venv` before the test and their no-argument branch only runs `exec /bin/bash`, with no gcloud login. The production branch is the slide's `uv run python $args` (`ml-workflow/src/data-processor/docker-entrypoint.sh`). The `workflow`, `model-training` and `model-deployment` entrypoints log in to gcloud but do not fork (`ml-workflow/src/workflow/docker-entrypoint.sh`). Bash needs `args="$@"` with no spaces. | The repo | "The switch is real and it is the whole idea. The step images need no gcloud login: locally the libraries read your key through `GOOGLE_APPLICATION_CREDENTIALS`, and on Vertex the pipeline's service account supplies the credentials." This links to `digest.md` §3.8. |
| 9 | **Submitting the job** (slide 33; slide 29 for the file name): `from import google.cloud.aiplatform import aip`, no `aip.init`, `job.run()` with no arguments. Slide 29 compiles to `sample-pipeline.yaml`, slide 33 loads `sample-pipeline1.yaml`. | `import google.cloud.aiplatform as aip`, then `aip.init(project=GCP_PROJECT, staging_bucket=BUCKET_URI)`. The sample compiles to and loads `sample-pipeline1.yaml`, and the job runs with `job.run(service_account=GCS_SERVICE_ACCOUNT)` (`ml-workflow/src/workflow/cli.py:299-314`). That service account is why the README adds the Service Account User role. | The repo | Show the repo's lines in the code panel. "One argument the slide leaves out matters: the pipeline runs *as* the `ml-workflow` service account, and your key needs permission to act as it." |
| 10 | **Who does what in the analogy** (slide 30 vs slide 40): on slide 30 the SDK is "the chef who follows" the recipe card; on slide 40 it is the operator who sends the YAML, and Kubeflow is the engine that runs it. | The SDK (`google-cloud-aiplatform`) builds a create request from the YAML, submits it and polls until the run ends (`digest.md` §3.7). Vertex's managed backend runs the steps; no Kubeflow cluster of yours is involved. | Slide 40 | Use slide 40's mapping only: "the SDK hands the instructions in and watches; it never cooks." Avoid "Google Cloud SDK" for this package, because that name usually means the `gcloud` tools. |
| 11 | **Reproducible and traceable** (slides 19, 22, 24). | Two holes in this repo. The lightweight components install `packages_to_install=["google-cloud-aiplatform"]` unpinned at run time (`ml-workflow/src/workflow/model.py:6`, `:68`), so the same YAML can behave differently next month. The training launcher calls `job.run(..., sync=False)` (`:62`), so a failed training job can still show a ticked step, and Model Deploy may then deploy the previous run's model (`digest.md` §6 item 10, E7). | The repo | "Vertex records every run, its graph and its parameters. Reproducibility is something your code still has to earn: pin versions, and let a failed step fail." Make this the last two lines of the §10 checklist. |

Not counted as conflicts:
- Slide 14's deprecated `dtype`/`back_prop` arguments match the repo; TF prints warnings for both.
- Slide 28's components set no `base_image`, and neither do the repo's copies of them (`ml-workflow/src/workflow/cli.py:277-289`). kfp 2.14.6 warns and uses `python:3.9` (`digest.md` §4 B10). The repo's training and deploy components do set `base_image="python:3.10"`.
- Slide 8's names ("Cloud Functions", "Cloud Runs") belong to L14.
- The deck says Lecture 15, as `tutorials_demo.md` does, while the course site's week page says 14 (`digest.md` §10 item 13). The series follows the deck.
- The README's stale mushroom output is a README-vs-code issue, not a slide issue.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag every section that stands on lecture ground with one grey `lecture_ref(15, "a–b")`, using the ranges below. When the README's two diagrams (slides 12 and 37) are on screen in §1, §6 and §9, re-draw them in the series style rather than showing the PNGs: laptop GREY, cloud BLUE, containers TEAL, money GOLD. Re-drawn, they can show today's facts, such as the dashed ordering arrow, the greyed TFRecords line and the signature inside training.
- **One analogy family per part.** The digest's concept notes (§3) and plan (§8) between them use eight metaphors: vending machine, recipe card and kitchen, customs officer, taxi meter, lunchbox, play, conductor, noticeboard. The lecture owns "recipe" for the *pipeline definition* (slides 25, 30, 40). Keep "recipe" for Part B, following slide 40: recipe → printed instructions → operator → engine → manager, with workers and a job sheet. In §3, call the registry entry a *catalogue card* instead of a "recipe card". Keep the play analogy (digest §3.6) out of §8, and if §9 borrows the conductor of digest §3.7, make it slide 40's factory manager instead.
- **Length.** The plan is about 38 minutes, against the series target of 25–35. Bring the lecture ideas in by replacing material, not adding it. Shrink the §10 debugging tour to a 60-second checklist (the study guide's §6 carries the details) and give that time to the slide-40 recap. Fold §5 into the end of §3 (both are about the meter).
- Gap 1's three-step checklist from slide 34 (callable → build & push → DAG) can sit as a small tracker in the corner through §7–§9, the way the README tracker does.

**Per section**
- **§1 · Lecture 15 · slides 6–12.** After the hook, show slide 6's roadmap with its red current-position box (unlabelled on the slide) for ten seconds, then slide 7's four tiles with Model Deploy the only one unticked. Re-draw slide 10 as a four-row sidebar: Workbench, Training (lit in L13), Online prediction and Pipelines (today). The three slots (artifact, runtime, address) then land on slide 12's GCS bucket, a serving image, and Model Endpoints. Say once that the slide has no box for the runtime and that the tutorial adds it.
- **§2 · Lecture 15 · slides 12–14.** Open with slide 13's development-vs-production contrast: notebook cells that resize and normalise one by one, against one request carrying raw bytes. Say "client-side brittleness" once, then "training/serving skew". Add the lecture's second reason: one copy of the logic makes rollback and versioning easier. Use slide 14's three call-outs as the beats (*define preprocessing function* → *define the `@tf.function` signature* → *save with `serving_default`*) and fill the elisions with the repo's code. Draw slide 12's steps 1–3 as one `--prepare` arrow (Conflict 3).
- **§3 · Lecture 15 · slides 11–12, 15–17.** Draw steps 4–5 as one `--deploy` arrow and caption the taxi meter with slide 11's alert. Then the gap-2 card: Vertex endpoint vs Cloud Run (from L14), covering who builds the server, what scales, and which ML extras exist. Mark autoscaling, versioning and monitoring "available, not used here" (Conflicts 4–5) and add the one-line note on online vs batch prediction. The console beat is slide 15's "View Model Registry" and "View Model Endpoints" pages.
- **§4 · Lecture 15 · slide 13.** Bridge in one sentence: "The lecture says *raw image bytes*. On the wire that means base64 inside `{"b64": …}`, under the signature's input name." Everything else here is tutorial-only.
- **§5 · Lecture 15 · slides 11, 41.** Call back to slide 11's alert. Slide 41 is a picture slide with only "DELETE!!" on it, which reads as a clean-up reminder (our reading): render that word as a GOLD card over the meter, then the commands. No meme images.
- **§6 · Lecture 15 · slides 7, 19–22.** Re-draw slide 20 and then slide 21: four tiles with a person at a CLI under each, then the headline changes from "How do we execute these steps?" to "Can we automate this flow?" and one Vertex AI Pipelines box replaces the four people. Keep slide 7's arrow colours for what each step touches. Close on slide 22's four duties as a card with ticks for this repo: order ✓, resources ✓ (`set_cpu_limit`), monitoring ✓ (console graph), scheduling ✗ (L23). "Re-run with new data" stays open until §9.
- **§7 · Lecture 15 · slides 27–28, 34–36.** Start with slide 34's three steps (gap 1). For "callable", draw slide 36 as one TEAL image with a switch: no arguments → shell (development mode, what `sh docker-shell.sh` gives you); arguments → `cli.py --search …` runs and exits (production mode, what Vertex does). Then the existing pause and ponder about `brie+cheese`. Code panels show the repo's Dockerfile line and entrypoint (Conflicts 7–8). For the split screen: slide 28's `@dsl.component` functions are the Python-component half; container components are tutorial-only, so say "the lecture shows this kind; the cheese pipeline also uses that kind". For the registry, say Docker Hub, pre-pushed, amd64 (Conflict 6).
- **§8 · Lecture 15 · slides 25–30.** Use slide 27's reminder that the DSL is not a new language, just Python with decorators. Draw slide 29's Y-shaped graph: two `square` tasks side by side → `add` → `square_root` = 5.0, with solid data arrows. Then the plan's tracing animation and the dashed `.after()` arrow as what the cheese pipeline uses instead. End on slide 30's four steps with the first two lit, and introduce slide 40's chain here (gap 3).
- **§9 · Lecture 15 · slides 32–33, 37–39.** Draw slide 32's sketch (You → SDK → Vertex AI) with "remote control" as the caption. The SDK submits and waits (Conflict 10). The code panel shows the repo's submit lines with `service_account=` highlighted (Conflict 9). Then re-draw slide 37 with its duty cards and play the plan's twist on the lecture's own picture: the TFRecords line greys out (Conflict 1), the processor → training arrow turns dashed "ordering only" (Conflict 2), and the signature moves into the training card (Conflict 3). The console beat is slide 39's "View Vertex AI Pipelines" runs page.
- **§10 · Lecture 15 · slide 40.** For the content recap, replay slide 40's chain with this lecture's real artefacts under each link: `ml_pipeline()` → `pipeline.yaml` → `PipelineJob.run(service_account=…)` → Vertex's managed KFP backend → the console graph. Show slide 12's five steps as the Part A mini-chain (`--prepare`, `--deploy`). Then the short debugging checklist, ending with Conflict 11's two lines.
- **Recap questions.** Add "Why does the endpoint take raw bytes instead of a 224×224 array? Give the lecture's two reasons" (slide 13). Add "When would you choose Cloud Run instead of a Vertex endpoint, and which one keeps billing at zero traffic?" (slides 16–17). Add "What makes a container callable, and what does the same image do with and without arguments?" (slides 34–36). Keep the plan's six.

**Terms**
- Use the lecture's words: *Vertex AI Online Prediction*, *serverless model deployment*, *model signature* / *serving signature*, *client-side brittleness*, *GCS bucket*, *Model Registry*, *Model Endpoints*, *Model Deployment CLI Container* (once, then `model-deployment-cli`), *ML workflow management*, *Vertex AI Pipelines*, *DSL*, *component*, *pipeline*, *compiler*, *YAML*, *SDK*, *PipelineJob*, *callable container*, *development mode* / *production mode*, *DAG*.
- Add the repo's words where the lecture stops: *prebuilt serving container*, *DeployedModel*, *traffic split*, *container component* vs *lightweight Python component*, *data edge* (`.output`) vs *ordering edge* (`.after()`), *pipeline root*, *service account*, *launcher*.
- Qualify, don't repeat:
  - "serverless": no servers to manage, not scale to zero.
  - "Kubeflow": say "Kubeflow Pipelines (KFP)" once; you never see a Kubeflow cluster.
  - "Google Cloud SDK": say "the Vertex AI SDK for Python (`google-cloud-aiplatform`)" and keep `gcloud` separate.
  - "autoscaling, versioning, drift detection": available, not used here.
  - "Convert to TF Records": the processor's old duty.
