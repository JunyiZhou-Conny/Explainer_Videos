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

1. **The project has reached deployment and automation.** On the roadmap the class is in late
   Prototype, inside the box that holds "Build Better Models", "ML Workflow" and the start of
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
   Production needs a repeatable, traceable sequence from data to training to deployment.
   Slide 20 shows the problem: four components, each driven by a person at its own CLI. Slide 21
   asks whether the flow can be automated and answers "Vertex AI Pipelines". *Slides 19–21.*
10. **What ML workflow management does.** It coordinates the end-to-end steps, records which
    task depends on which and runs them in the right order, and makes runs reproducible, so the
    same code can re-run on new data. It also handles scheduling, monitoring and resource
    allocation. *Slide 22.*
11. **Vertex AI Pipelines is Google's managed orchestrator.** You define each step in Python, and
    Vertex runs the steps serverlessly, reproducibly and at scale. It is built on Kubeflow, but
    you set up no Kubernetes. *Slides 19, 24.*
12. **Kubeflow is the machine and the DSL is the recipe.** Kubeflow is an open-source system for
    running ML workflows on Kubernetes. The DSL (domain-specific language) is a small, purpose-
    built way to describe pipeline steps and how they connect. It is written in Python, so it is
    not a new language to learn. *Slides 25–27.*
13. **Writing a pipeline has three moves: components, pipeline, compile.** A component is a
    decorated Python function with typed inputs and outputs. The pipeline function wires
    components together by passing one task's `.output` into the next call. The compiler then
    writes the whole graph to a YAML file. The toy example squares `a` and `b`, adds the squares
    and takes the square root. With the defaults 3 and 4, the answer is 5. *Slides 28–29.*
14. **From DSL to a running pipeline.** You write the workflow with the KFP DSL. The compiler
    produces YAML. The Google Cloud SDK sends that YAML to Vertex AI. Vertex AI runs the steps one
    by one, serverlessly. An SDK is a set of tools and libraries for controlling a platform from
    your own code, the "remote control for Vertex AI". In code: build an `aip.PipelineJob` from
    the YAML with a pipeline root and a caching flag, then call `job.run()`. *Slides 30, 32, 33.*
15. **Your own containers need three things.** (1) Make each container callable: it accepts
    inputs and produces outputs. (2) Build the images and push them to a registry that Vertex AI
    can reach. (3) Describe in `kfp.dsl` how the steps connect. That structure is a DAG, which
    fixes what runs first and what depends on what. *Slide 34.*
16. **One image, two modes.** "Callable" here means changing the Dockerfile's entry point from an
    interactive shell to a shell script. The script branches on whether arguments were passed.
    With no arguments (development), it authenticates gcloud with the service-account key, sets
    the project and opens a shell for testing the CLI. With arguments (production), it runs Python
    with them, so `docker run … cli.py --search` executes one task and exits. *Slides 35–36.*
17. **The Cheese App pipeline is a four-step chain.** Each step has its own duties:
    - Data Collector: download images, upload them to GCP.
    - Data Processor: verify images, remove duplicates, convert to TFRecords.
    - Model Training: train, save the model.
    - Model Deploy: upload to the registry, deploy an endpoint.

    *Slides 37–39.*
18. **The whole stack in one chain.** DSL (your recipe) → compiler (YAML, the printed
    instructions) → SDK (the factory operator who submits it) → Kubeflow (the engine that runs
    it) → Vertex AI Pipelines (manages the run serverlessly, step by step). Each container is a
    worker in the factory, and the DAG tells the workers what to do and in what order. *Slide 40.*

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
    step forward through POC, the last one reaching into early Prototype
  - "Build Better Models" and "ML Workflow": stacked in late Prototype
  - "Build Cheese App": in MVP
  - "Deployment, Scaling & Automation": from mid-Prototype to the end of MVP

  A red dashed rectangle encloses Build Better Models, ML Workflow and the start of Deployment,
  Scaling & Automation. That rectangle marks "you are here".
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
  red, and grey curved arrows run to them from four coloured labels on the right:
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
  - pink "Save Model with the new model signature" → the `signatures=` line of
    `tf.saved_model.save`

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

  The graph the code defines is diamond-shaped. Two independent `square` tasks (inputs `a`=3 and
  `b`=4) can run in parallel. Both feed `add`, and `add` feeds `square_root`, which returns 5.0.
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
  `ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]`. Curved arrows from both entry-point lines
  converge on one blue label, "Change entrypoint to a shell file". Purpose: making a container
  callable is a one-line change plus a script.
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
| "TF Records" | 37 | The README also says the processor converts to TFRecord format, but on `main` it no longer does, and training does not read the processor's output (`digest.md` §10, item 2). |
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
  - `FROM python:3.9-slim-buster` — this is the old Pipenv-era base image. On `main` the step
    images use `python:3.12-slim-bookworm` or `python:3.13-slim-bullseye`.
  - `RUN --chown=app:app . /app` (*sic*). `--chown` belongs to `COPY`/`ADD`, and the repo has
    `COPY --chown=app:app . ./`.
  - Before: `ENTRYPOINT ["uv", "shell"]`. uv has no `shell` subcommand (checked with uv 0.11:
    "unrecognized subcommand"). The line reads like `pipenv shell` with the tool name swapped.
  - After: `ENTRYPOINT ["/bin/bash","./docker-entrypoint.sh"]` — the repo has the same line
    without `./`.
- **Slide 36** (`docker-entrypoint.sh`):
  - `args = "$@"` (*sic*). Bash does not allow spaces around `=`, and the repo has `args="$@"`.
  - `if [[ -z ${args} ]];`
  - `gcloud auth activate-service-account --key-file $GOOGLE_APPLICATION_CREDENTIALS`
  - `gcloud config set project $GCP_PROJECT`
  - `uv shell` (see above). In the repo, the two pipeline step images (data-collector,
    data-processor) have this argument fork, but with no arguments they activate `/.venv` and
    `exec /bin/bash`, and they do no gcloud login. The `workflow`, `model-training` and
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
- **Best practice for choosing a host** (slide 16): Vertex AI for serving trained models in
  production; Cloud Run for bringing ML into broader applications or pipelines. The trade-off
  (slides 16–17): Vertex is specialised and managed, while Cloud Run is general but leaves ML
  monitoring and model versioning to you.
- **Automate instead of running steps by hand.** Production needs a repeatable, traceable
  sequence (slide 19). Workflow management makes runs reproducible and repeatable on new data,
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
