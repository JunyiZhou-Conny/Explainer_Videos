# L23 lecture slides — Final Deployment and Review

Source: one deck, `L23_final_deployment_and_review` (38 slides), titled "Lecture 23: Final
Deployment and Review" (AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's
lecture slides (PDF), provided by the student for study; the PDFs are not in this repository;
slide numbers are PDF page numbers. Several slides were pasted in from other decks and print a
different footer number (slide 10 prints "6", slide 12 prints "7", slide 29 prints "67", the
image on slide 24 carries its old "14", and the image on slide 23 shows the cut-off top of an old
one); this file always uses the PDF page. It was written from
the deck's extracted text and from every contact sheet, with enlarged renders of slides 4, 6, 7,
10, 12, 19, 20, 22–37. Everything below is paraphrased; only short titles, terms, URLs and single
code lines are quoted. The tutorial side of the lecture (`dlops-io/cheese-app-v4`) is in
[`digest.md`](digest.md).

## Outline

Slide 2 lists two sections, "Motivation" and "Automation"; slide 3 repeats it with "Motivation"
in bold as the section divider. The deck then adds an unlisted third part, "Review" (slide 21),
with one recap slide per earlier lecture. The lecture numbers printed on the review slides do
**not** match this year's deck numbering (see Pointers for the mapping).

- Slide 1 · title slide
- Slides 2–3 · outline (2) and "Motivation" divider (3)
- Slide 4 · **Motivation**: a joke web app, "Pavlos + Olivera Thanksgiving Lunch", whose
  "Turkey Cooking Time Predictor" forecasts when the turkey will be done
- Slides 5–20 · **Automation** (no divider slide of its own)
  - 5–6 · "Automation": the five operations to automate (5 as a list, 6 as illustrated cards)
  - 7 · "CI / CD": the loop diagram, Codebase → Build → Test → Deploy → Monitor
  - 8–10 · "Continuous Integration (CI)": definition by purpose (8), reworded around many
    developers and a shared repository (9), the same with a pipeline picture (10)
  - 11–12 · "Continuous Deployment / Delivery (CD)": deployment defined, delivery greyed out
    (11); both side by side with pictures (12)
  - 13–14 · "CI in AI/ML": what CI catches in ML and its challenges (14 is 13 with one sentence
    removed)
  - 15 · "CD in AI/ML": benefits and challenges
  - 16 · "CI/CD Providers and Tools": six logos
  - 17 · "How to Implement CI/CD": we already have a deployment container
  - 18 · "How to Implement CD": GitHub Actions drives that container
  - 19 · "Cheese App: CI CD": the whole app, GitHub, GitHub Actions and GCP on one diagram
  - 20 · "Tutorial: Continuous Integration, Continuous Deployment": workflow file, the
    `/deploy-app` commit keyword, links and a QR code
- Slides 21–37 · **Review** (course recap, one picture per earlier lecture)
  - 21 · "Review" divider
  - 22 · "Lecture 2-4: Environments vs Virtualization vs Containerization": three layer stacks
  - 23 · same title reused, but the picture is the six-step audio pipeline sharing a GCS bucket
  - 24 · "Lecture 5: Docker Workflows": team workflow, "Scenario 2 (later stages of
    development)"
  - 25 · "Lecture 6: App Design": the "Solution Architecture" (Process / Execution / State)
  - 26 · "Lecture 6: Data Labeling and Data Versioning": unlabeled → labeled, "How do we do
    this?"
  - 27 · "Lecture 7: Instruction based GPT => ChatGPT": three training steps
  - 28 · "Lecture 8-9: RAGs": the indexing / retrieval / generation diagram
  - 29 · "Lecture 10: Agents": from deterministic workflows to autonomous agents
  - 30 · "Lecture 11: Fine Tuning LLMs (LoRA, qLoRA)": the LoRA side path
  - 31 · "Lecture 11: Distillation": a photo of a kitchen still (visual pun)
  - 32 · "Lecture 12: Weight and Biases/VertexAI serveless training" [sic]: package, upload,
    run training jobs
  - 33 · "Lecture 13: Model Deployment with VertexAI": five steps to an endpoint
  - 34 · "Lecture 14: ML Pipelines": the four-step pipeline graph
  - 35 · "Lecture 15-16: API, MCP, Frontend": API and frontend containers in development
  - 36 · "Lecture 17-18: CI, Testing": the slide-7 loop with a "Release" stage added
  - 37 · "Lecture 19-20: Pulumi, Kubernetes": a screenshot of the ingress routing diagram
- Slide 38 · "THANK YOU"

## Key ideas

1. **Motivation: a model is only useful once it is deployed and kept current.** Slide 4 shows a
   tongue-in-cheek web page that predicts when the Thanksgiving turkey will be ready, with a
   live temperature curve, a "NOW" marker and a confidence band. The slide has no text about
   CI/CD; the link to automation was presumably spoken. A fair reading (ours, not the slide's):
   even a toy prediction app must be running somewhere and refreshed as new readings arrive.
   (Slide 4)
2. **Five things to automate.** Running data-pipeline jobs, training and deploying models,
   deploying the frontend, deploying the backend, and building and pushing Docker containers.
   (Slides 5, 6)
3. **CI/CD is one loop with feedback.** Developers commit to the codebase; the codebase is built
   and tested (the CI half), then deployed and monitored (the CD half). Every stage after Codebase
   reports back to the developers as notifications. The review version inserts "Release" between
   Test and Deploy. (Slides 7, 36)
4. **CI runs a set of scripts automatically on every push.** It keeps integrating changes into
   the production branch, runs automated tests, enforces coding standards and performs static
   analysis, so that many developers can share one repository and the code stays working.
   (Slides 8–10)
5. **Coding standards and static analysis are different checks.** Standards are about style and
   consistency; static analysis looks for likely defects and security weaknesses without running
   the code. (Slides 8–10)
6. **Delivery vs deployment: is a human in the loop?** Continuous delivery extends CI so the
   software can be released reliably at any moment, but a person still presses "release".
   Continuous deployment pushes every integrated change to production automatically. Both are
   abbreviated "CD". (Slides 11, 12)
7. **CI for ML integrates code, data and models, and that makes it expensive.** Its job is to
   catch problems in data quality, code correctness and model performance early. The tension is
   between frequent integration and the cost of training and of long tests on big data and
   complex pipelines, plus keeping evolving data, features and model versions compatible.
   (Slides 13, 14)
8. **CD for ML releases models, data and pipelines once they pass validation.** On top of CI's
   benefits it adds performance validation (metrics must stay within a tolerance) and cloud
   scalability. Its challenges are data drift, validating complex models such as LLMs, and cost.
   (Slide 15)
9. **Many CI/CD services exist; the course uses GitHub Actions.** TeamCity, GitHub, GitLab,
   Jenkins, CircleCI and TravisCI are shown. (Slides 16, 18)
10. **Implementation = reuse the deployment container, triggered by GitHub.** That container can
    already build Docker images, run Vertex AI pipeline jobs and deploy the app to the K8s
    cluster. GitHub Actions watches commits, builds and runs the container, and calls its CLI to
    build and push release images, run Vertex AI jobs with the new images, and roll the new app
    images onto the cluster. (Slides 17, 18) *Tutorial check:* in `cheese-app-v4` the Vertex
    jobs are submitted by a separate `workflow` container, and CI does not rebuild the ML images
    (digest §6 #3); the slide's single-container design matches the older Pipenv/Ansible branch.
11. **The cheese app's CI/CD map.** The dev team commits to GitHub; GitHub Actions builds and
    deploys onto Google Cloud (Storage, Vertex AI, Kubernetes), which serves the users. The app's
    components form one chain: Data Collector → Data Processor → Model Training → Model Deploy →
    Backend API → Frontend. (Slide 19)
12. **In the tutorial, the commit message is the trigger.** A workflow file in `.github/workflows`
    defines the deployment steps; putting `/deploy-app` in the commit message starts it.
    (Slide 20)
13. **Review, part 1 — isolation and containers.** Virtual environments isolate only Python
    libraries on one OS; VMs each carry a full OS on a hypervisor; containers carry only their
    libraries and share the host OS through Docker (slide 22). Independent containers can form a
    pipeline by exchanging files through a shared bucket (slide 23), and a team settles on one
    image via pull requests that a lead consolidates and publishes (slide 24).
14. **Review, part 2 — the app as three layers.** A process layer (people developing, running
    ML tasks, using the app), an execution layer (notebooks, ML pipeline, LLMs, frontend,
    backend) and a state layer (source control, artifact registry, data store, knowledge base),
    linked by human interaction, CLI automation and HTTP(S). (Slide 25)
15. **Review, part 3 — data and LLM techniques.** Labeling turns unlabeled images in a bucket
    into labeled training data with a labeling tool in a container (slide 26); ChatGPT-style
    models come from supervised fine-tuning, a reward model, then reinforcement learning
    (slide 27); RAG indexes chunked documents as embeddings, retrieves by query embedding and
    feeds the context to an LLM (slide 28); agents sit at the autonomous end of a spectrum that
    starts at rule-based workflows (slide 29); LoRA trains a small side path parallel to frozen
    weights (slide 30); distillation is shown only as a pun (slide 31).
16. **Review, part 4 — training, deploying and orchestrating on Vertex AI.** Code moves from
    notebook to Python package to a tarball in GCS, and a CLI container launches serverless
    training jobs (slide 32); a deployment CLI container updates a saved model's signature,
    uploads it to GCS and the Model Registry, and deploys an endpoint (slide 33); a pipeline
    chains collector, processor, training and deploy (slide 34).
17. **Review, part 5 — serving and shipping.** In development the API and frontend containers
    each mount their source code, the API container also mounts secrets and a persistent folder,
    and the browser talks REST/JSON to one and gets HTML from the other (slide 35); CI/testing is the commit → build → test → release →
    deploy → monitor loop (slide 36); on Kubernetes an ingress controller routes `/` to the
    frontend and `/api/` to the API, which talks to the vector DB (slide 37).

## Diagrams

- **Slide 6 · five operations as cards.** Five rounded cards in a row joined by right arrows,
  each an icon plus caption: "Running data pipeline jobs" (gears, a pipe into a database),
  "Model training & model deployment" (an "AI" brain → rocket, servers), "Frontend deployment"
  (a web page with an arrow up to a cloud tagged "DEPLOY"), "Backend deployment" (a server and an
  "<API>" window, arrow to a cloud tagged "DEPLOY"), "Building & Pushing Docker containers" (the
  Docker whale, arrow up to a cloud tagged "PUSH"). The arrows only order the list; they do not
  claim a strict sequence. Purpose: what the lecture wants to hand over to automation.
- **Slide 7 · the CI/CD loop.** Top row: a red dashed rectangle around three solid red boxes,
  "Codebase" → "Build" → "Test", then an arrow into a blue dashed rectangle around two blue
  boxes, "Deploy" → "Monitor". Red = CI, blue = CD. Above the row, tool logos: GitHub and GitLab
  (over Codebase/Build), the red-and-green theatre masks of Playwright (over Test), Jenkins and
  TeamCity, Docker, Kubernetes (over the CD half). Bottom left: "Developers", with a solid arrow
  labelled "Commits" going up into "Codebase". A thick black vertical bar beside "Developers"
  receives four dashed lines coming down from Build, Test, Deploy and Monitor; the caption under
  them is "Notifications". Purpose: code flows right, feedback flows back to the people. Re-draw
  as a loop: a commit dot runs along the boxes, and each box drops a notification back.
- **Slide 36 · the same loop with "Release".** Identical layout to slide 7, but the blue group
  has three boxes, "Release" → "Deploy" → "Monitor", and five dashed notification lines (Build,
  Test, Release, Deploy, Monitor). Purpose: delivery's release gate made explicit. (L21's slide
  21 drew only the red half; see [L21 SLIDES](../ac215-l21-cicd-github-actions/SLIDES.md).)
- **Slide 10 · CI as a pipe of quality checks.** Left: three developer avatars with arrows into a
  "Shared Repository" (a browser-like window with code lines). An arrow leads into a horizontal
  pipe titled "Automated Quality Checks" holding three icon tiles in order: "Running automated
  tests" (a gear with a bug and a green check), "Enforcing coding standards" (code brackets and a
  set square), "Performing static code analysis" (a magnifier over code with a warning sign). A
  bracket arc spans the three tiles. The pipe exits into "Functional Codebase" (a document with a
  green check). The slide's note highlights "Coding standards" ↔ "style and consistency" and
  "Static code analysis" ↔ "identifying potential defects and vulnerabilities". Purpose: many
  people, one repository, automatic gate, working code out.
- **Slide 12 · delivery vs deployment, side by side.** Left half, "Continuous Delivery (CD)":
  code windows travel along a pipe and stop at a gate (a barrier). Beyond it, a person sits above
  a big red push-button labelled "RELEASE", and only then does an arrow reach a server stack
  labelled "PRODUCTION". Right half, "Continuous Deployment (CD)": code windows stream through a
  glowing red/blue ring labelled "AUTO DEPLOY" and continue straight into servers with a rocket
  launching from them, labelled "PRODUCTION". Notes under each half: a person stays in the loop
  (delivery); changes are "automatically passed" into production (deployment). Purpose: the only
  difference is who presses release. Re-draw: one conveyor, a toggle swaps the human button for
  the ring.
- **Slide 19 · "Cheese App: CI CD" (same picture as the README's `images/ci-cd.png`, with one
  difference).** Top/right arc of six pastel boxes joined by curves: "Data Collector" (pink) →
  "Data Processor" (blue) → "Model Training" (yellow) → "Model Deploy" (green), drawn as blue
  curves with small circle endpoints; then a magenta curve from "Model Deploy" down into "Backend
  API" (lavender), and a magenta arrow left from "Backend API" to "Frontend" (grey-blue). In the
  middle, "Dev Team" with faint double arrows to each of the six boxes and three arrows down
  "(Commits)" onto a bar; a dashed line runs from that bar right and down to a second bar whose
  three arrows "(Commits)" enter a "GitHub" box containing "Code", "Branches", "Actions". Along
  the bottom, the flow goes right to left: GitHub → a grey block arrow → a red dashed box "GitHub
  Actions" holding two red boxes, "Build" (right) linked to "Deploy" (left) → a grey block arrow
  → a blue box "Google Cloud Platform" holding "Storage", "Vertex AI", "Kubernetes". Far left:
  "Users" above a dark screenshot of the Formaggio chat page, joined to the GCP box by a grey
  vertical double arrow. Difference: the README image's GitHub Actions box reads "Build" →
  "Release" → "Deploy"; the slide drops "Release". Purpose: one map of the whole system and the
  path from commit to cloud. Caveat for scene authors: the Model Deploy → Backend API link is not
  implemented in v4 (digest C7, errata 8).
- **Slide 22 · venvs vs VMs vs containers.** Three columns, each standing on the same two dark
  bands, "Operating System" over "Infrastructure":
  - "Virtual Environments": a dark-blue "Python" band carries three dashed boxes (blue, green,
    red), each "AppN" over "Libs" over the label "Venv".
  - "Virtualization": a grey "Hypervisor" band carries three tall dashed boxes, each "AppN" over
    "Bins/lib" over a large "OS", labelled "VM".
  - "Containerization": a blue "Docker" band (with the whale) carries six dashed boxes in two
    rows of three, each "AppN" over "Bins/lib", labelled "Container" (top row blue/green/red,
    bottom row gold/purple/mauve; the bottom row's labels read App3, App2, App3).

  Purpose: what each layer isolates and what it duplicates; the VM column is visibly taller
  because each VM carries an OS. Re-draw as three stacks that build upward layer by layer.
- **Slide 23 · the audio pipeline (title reused from slide 22).** Five pastel boxes in a row
  joined by hollow arrows, with numbered circles: (1) "Record Audio" (red microphone) → (2)
  "Transcribe Audio" (blue) → (3) "Generate Text" (yellow) → (5) "Translate Text" (purple) → (6)
  "Synthesise Audio" (green speaker). A second green "Synthesise Audio" box, (4), sits above
  "Translate Text" and receives a hollow arrow from the "Generate Text" side. Below, a wide grey
  box "GCS Bucket" / "Audio + Text Files" (cloud icon): Record Audio sends a one-way red arrow
  into it; Transcribe, Generate, Translate and step 4 have vertical double arrows to it; step 6
  has a green double arrow to it. Purpose: independent containers coordinate only through files
  in a shared bucket. This is the L03 mega-pipeline (podcast) tutorial.
- **Slide 24 · Docker team workflow, Scenario 2.** Left: three stacked tinted boxes labelled
  "Windows" (green), "Linux" (pink), "Mac" (blue), each with three yellow squares (code) and a
  people icon of the same colour. A long hollow arrow points right to a dotted box "Source
  Control" containing "GitHub". Above it, a pink box labelled "'Senior' Developer" with a red
  people icon. To the right, a dotted box "Images" containing "DockertHub" [sic]. Text: developers
  open pull requests, sometimes including Dockerfile or Pipfile changes; the senior developer
  reviews and merges them, folds the changes into a new Dockerfile and Pipfiles, builds new
  images and pushes them to Docker Hub. Purpose: the manual build-and-publish role that CI/CD
  now automates.
- **Slide 25 · Solution Architecture.** Three horizontal bands:
  - "Process" (pink, top): a people icon and three wide boxes, "Develop App", "AI/ML Tasks",
    "Upload picture, view predictions".
  - "Execution" (dashed, middle): "Interactive Notebooks" (yellow; "Notebooks"), "ML Pipeline"
    (blue; "Data Collector", "Data Processor", "Model Training", "Model Deploy"), "Frontend"
    (grey-blue; "Cheese App"), "LLMs" (green; "Frontier LLMs", "Fine tuned LLMs"), "Backend"
    (lavender; "API Service", "Vector DB Service").
  - "State" (grey, bottom): "Source Control", "Artifact Registry", "Data Store", "Knowledge
    Base", each with an icon.

  Arrows: "Develop App" ↕ State (a long double arrow on the left); "AI/ML Tasks" → Notebooks
  "(Human Interactions)" and → ML Pipeline "(CLI + Automation)"; "Upload picture…" → Frontend
  "(Human Interactions)"; Notebooks ↕ State; Notebooks/ML Pipeline ↕ LLMs "(HTTP / HTTPS)"; LLMs
  ↔ Backend "(HTTPS)"; Frontend ↕ Backend "(HTTP / HTTPS)"; Execution ↕ State "(Protocol
  specific)". Purpose: the layered map that every later lecture filled in.
- **Slide 26 · data labeling flow.** Top: "Unlabeled" (a dashed box of six cheese photos) → a
  long green arrow under the red question "How do we do this?" → "Labeled" (rows "brie", "gouda",
  "parmigiano", "gruyere", each with photos) → green arrow → (4) "Colab {training}" (a yellow
  panel) ↔ a people icon. Bottom: (1) unlabeled images go down into "GCS Bucket:
  cheese-app-data-demo", a dotted box holding two folders, `cheeses_unlabeled` (red) and
  `cheeses_labeled` (green). (2) The bucket ↕ a "Data Labeling" box holding "Container". (3) The
  container → "Label Studio" (a window of cheese photos); people ↕ the container and ↔ Label
  Studio. A light-blue connector links the bucket and the Colab panel. Purpose: the concrete
  answer to "how": a labeling container plus Label Studio, storing both folders in one bucket.
- **Slide 27 · ChatGPT in three steps.** Three rounded boxes stepping down to the right, joined
  by curved arrows: "Supervised fine tuning model" (blue) → "Training a reward model" (green) →
  "Fine-tuning the model with reinforcement learning" (purple). Purpose: the training recipe as a
  staircase.
- **Slide 28 · RAG.** Three dashed regions with numbered blue circles:
  - "Indexing" (red, top): "Knowledge Base" (database icon) → (1) "Chunking" → "Documents" → a
    tall pale column "Embedding Model" → (2) "Document Embedding" → a tall cylinder "Vector
    Database".
  - "Retrieval" (green, lower middle): "User" → (3) "User Query" → the same Embedding Model
    column → (4) "Query and embedded Query" → the same Vector Database.
  - "Augmentation & Generation" (blue, right): (5) "Prompt + query + context" → "LLM".
  - (6) "LLM Response": a line from the LLM back along the bottom to the user.

  Both the Embedding Model column and the Vector Database cylinder span the indexing and
  retrieval regions, showing they are shared. Purpose: offline indexing vs online query path.
- **Slide 29 · from workflows to agents.** Two header boxes: "Traditional Component —
  Deterministic Execution" (left) and "AI Agent — Autonomous Execution" (right). Five small
  flow graphs between them, each starting at "event": "Directed Graphs" (if/else branches, a
  loop, blue "end"), "Workflow Orchestrators" (branches, a loop, "end"), "Workflow Orchestrators
  (with ML)" (green ML nodes "summarize" and "classify", "end"), "Hybrid Orchestrators" (plain
  nodes mixed with green "agent" nodes, blue "goal"), "Autonomous Orchestrators" (an "agent"
  node with dotted links to options and a sub-agent, two "goal" nodes). Along the bottom, a pink
  double-headed arrow is a spectrum, labelled left to right "Rule-based Systems" / "Predictable",
  "Data Driven Workflows", "ML-Enhanced Tasks", "LLM-Enhanced Tasks", "Structured Output",
  "Guided Tool Selection", "Full Agent Autonomy". Purpose: autonomy is a dial, and "end" turns
  into "goal" as you move right.
- **Slide 30 · LoRA.** Bottom: a red bar "x" of width "d". Two block arrows go up from it: left
  into a blue square "Pretrained Weights", W ∈ ℝ^(d×d); right into an orange trapezoid
  "A = N(0, σ²)", which narrows to width "r" and feeds a second orange trapezoid "B = 0" that
  widens back. Arrows from both paths meet at a blue "+" and enter a red bar "h" at the top.
  Caption: the reparameterization runs parallel to the original model. Purpose: only the thin
  A/B side path is trained; the shown initialisation (A random, B zero) means training starts
  from the unchanged model.
- **Slide 32 · serverless training.** (2) "Package & Upload to GCP": a "Notebook" pane (Colab
  logo, code) → green arrow → a "Python File" pane → green arrow → "Packaged Python files" (a
  TAR.GZ file icon) → a long green arrow into a dashed "GCP" box, where a "GCS Bucket" holds the
  TAR.GZ. Below the arrows, a green "Model Trainer CLI Container" has two grey arrows up into the
  packaging step and one arrow right into "Vertex AI". (3) "Create & Run Training Jobs": inside
  Vertex AI, three "Job" boxes each hold a "Container" with the TAR.GZ, with resources "CPU,
  RAM, GPU", "CPU, RAM, GPU", "CPU, RAM"; a green arrow brings the tarball down from the bucket.
  The step numbering starts at 2 on this slide. Purpose: the trainer CLI container packages code
  once and launches many managed jobs that pull it.
- **Slide 33 · model deployment on Vertex AI.** Five red-numbered steps: (1) "Get Saved Model"
  (an orange bulb "Saved Model", arrow down into the container); (2) "Update Model Signature"
  ("Saved Model + Update Signatures": a code pane plus a green bulb, arrow up from the
  container); (3) "Upload to GCS" (green arrow into a "GCS Bucket" with a green bulb, inside a
  dashed "GCP" box); (4) "Upload to Model Registry" (a grey arrow from a green "Model Deployment
  CLI Container" into "Vertex AI", where a "Model Registry" panel holds two bulbs); (5) "Deploy
  Model Endpoint" (a green arrow from the registry panel into a "Model Endpoints" panel showing
  bulbs with link icons). A green arrow also runs from the bucket down into Vertex AI. Purpose:
  the ordered hand-offs from a saved model to a callable endpoint.
- **Slide 34 · ML pipeline graph.** Four nodes in a zigzag, joined by curved grey arrows, each
  with a box icon and a check mark in a coloured square: "Data Collector" (red) → "Data
  Processor" (blue) → "Model Training" (brown) → "Model Deploy" (green). It looks like a Vertex AI
  Pipelines run graph with every step succeeded. Purpose: the same four steps as slide 19's arc,
  now as one orchestrated pipeline.
- **Slide 35 · API and frontend containers in development.** Two green boxes, "API Service
  Container" (left) and "Frontend App Container" (right), each with a "Terminal" icon and a
  double arrow beside it. A "Browser" icon at top centre; a line labelled "REST / JSON" joins it
  to the API container and one labelled "HTML" to the frontend container. Red-numbered notes:
  (1) "Mount Source Code into Container" (a dashed "Source Code" box under each container, arrow
  up labelled "Mount"); (2) "Mount other folders" ("Persistent Folder" and "Secrets" boxes below,
  joined to the API container by "Mount" lines); (3) "API exposes python functions"; (4) "UI on
  Browser"; (5, blue) "Edit Code from VS Code", a blue line that feeds both Source Code boxes.
  Purpose: the development set-up, edit on the host and run in containers.
- **Slide 37 · Kubernetes routing (a screenshot).** Dark background, white boxes, from a
  diagram viewer whose zoom/pan buttons cover the last box: "Browser" → (edge label
  `nginx-ip.sslip.io/`) → "Ingress Controller", which forks: edge `/` → "Frontend Service
  NodePort:3000"; edge `/api/` → "API Service NodePort:9000" → edge `vector-db:8000` → a box
  starting "Vector… Node…" (cut off). Purpose: one URL, path-based routing to services.
  Differences from the tutorial: v3/v4 route `/api-service` (not `/api/`) and use ClusterIP
  services, and v4 replaces the NGINX ingress with a Google HTTPS load balancer (digest C8).
- **Not mechanism diagrams, but carrying content:**
  - Slide 4 · the turkey predictor: an orange header "Pavlos + Olivera Thanksgiving Lunch"
    ("When to come !!! We take the agony out with technology"); a card "Turkey Cooking Time
    Predictor" ("The turkey is currently half baked…", the model estimates the remaining time); a
    plot "Turkey Temperature Curve" of internal temperature (°F) against time (minutes): a rising
    blue curve from about 75 °F, a green dash-dot "NOW" line at 100 min, a red dashed target line
    at 162 °F, and a widening blue confidence band for the forecast beyond NOW (the legend also
    lists a "Confidence Interval Bayes"). A readout gives the estimated remaining time (100
    minutes) and a joke "95% confidence interval" telling guests to arrive in 75 minutes. Footer:
    "Precision Cooking Through Questionable Math™".
  - Slide 16 · six logos with captions: TeamCity, Github, GitLab, Jenkins, CircleCI, TravisCI.
  - Slide 20 · a QR code next to the tutorial links.
  - Slide 31 · a photo of a home distillation set-up: a large steel pot and a small pot on a gas
    stove, joined by flexible metal tubes. A visual pun on model distillation (big teacher, small
    student); no mechanism is drawn.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Automation" | 2, 3, 5, 6 | The README's title is "Cheese App - Automation". |
| "CI / CD", "CI CD" | 7, 16, 19, 20 | README: "Continuous Integration and Continuous Deployment (CI/CD)"; both workflow files are named "Continuous Integration and Continuous Deployment". |
| "Codebase", "Build", "Test", "Deploy", "Monitor", "Commits", "Developers", "Notifications" | 7, 36 | In the tutorial, notifications are the Actions run status; there is no Test stage (README: "The CI part is not implemented"). |
| "Release" (as a stage) | 36 | Absent from slide 7 and slide 19; present in the README image's GitHub Actions box. |
| "Continuous Integration (CI)" | 8–10, 13, 14 | README defines it the same way (frequent integration into a shared repository, automatic build and test, codebase always functional). |
| "production branch" | 8 | In the tutorial: `main`, the only branch the workflows listen to. |
| "coding standards", "static code analysis" | 8–10 | Not in v4; in L21's tutorial, Black and Flake8. |
| "Shared Repository", "Automated Quality Checks", "Functional Codebase" | 10 | README: "shared repository", "functional state". |
| "Continuous Deployment (CD)", "Continuous Delivery (CD)" | 11, 12 | Both in the README. The README frames delivery as automated delivery to staging/testing environments, ready but not necessarily released; the slides frame it as "keeping a person in the loop". The README says the tutorial does only continuous deployment. |
| "RELEASE", "PRODUCTION", "AUTO DEPLOY" | 12 | Picture labels. |
| "CI in AI/ML", "CD in AI/ML" | 13–15 | Not in the README. |
| "Data quality", "Code correctness", "Model performance" | 13, 14 | Not checked by v4's workflows. |
| "Performance validation", "within tolerance", "Data drift" | 15 | Not in v4 (MS5 asks for validation thresholds; digest §7). |
| "CI/CD Providers and Tools" | 16 | The tutorial uses GitHub Actions only. |
| "deployment container" | 17, 18 | The `deployment` image `cheese-app-deployment` built from `src/deployment` (L20's toolbox). In v4 it builds images and deploys to K8s; Vertex jobs come from the separate `workflow` container (`src/workflow`). |
| "GitHub Actions" | 18–20 | Same; two workflows, `app-ci-cd-gcp.yml` and `ml-ci-cd-gcp.yml`. |
| "Invoke CLI in deployment container" | 18 | In v4 the runner passes a script name, `deploy-k8s-update.sh`, which runs two `pulumi up`s; there is no CLI program in the deployment container any more (the Pipenv-era branch had `cli.py` there). |
| "Vertex AI pipeline jobs", "Vertex AI jobs" | 17, 18 | README: "Vertex AI Pipelines", triggered by `/run-ml-pipeline`, `/run-data-collector`, `/run-data-processor` (not on the slides). |
| "K8s cluster" | 17, 18 | `cheese-app-cluster` on GKE, managed by the `deploy_k8s` Pulumi stack. |
| "Github / Workflow file" | 20 | `.github/workflows/*.yml`. |
| `/deploy-app` | 20 | Matches `app-ci-cd-gcp.yml:9`. The README's prose says `/run-deploy-app` (`README.md:162`), which does not deploy (digest §6 #1); the slide is right. |
| "Data Collector", "Data Processor", "Model Training", "Model Deploy" | 19, 25, 34 | Same names in the README component list and the Vertex pipeline. |
| "Backend API" | 19 | README: "API Service" (`src/api-service`); slide 25 also says "API Service". |
| "Frontend" | 19, 25 | README: "React Frontend" (`src/frontend-react`; Next.js per the digest). Slide 25 calls the app "Cheese App". |
| "Dev Team", "Users" | 19 | Picture labels. |
| "Google Cloud Platform": "Storage", "Vertex AI", "Kubernetes" | 19 | The tutorial uses GCS (state bucket, ML data), Artifact Registry (images, not drawn), Vertex AI and GKE. |
| "Virtual Environments", "Virtualization", "Containerization", "Hypervisor", "Bins/lib", "Venv" | 22 | L01–L02 vocabulary. |
| "GCS Bucket", "Audio + Text Files" | 23 | L03 mega-pipeline. |
| "'Senior' Developer", "Scenario 2 (later stages of development)", "Source Control", "Images" | 24 | L03/L04 vocabulary. |
| "Solution Architecture", "Process", "Execution", "State", "Interactive Notebooks", "ML Pipeline", "Frontier LLMs", "Fine tuned LLMs", "Vector DB Service", "Artifact Registry", "Data Store", "Knowledge Base" | 25 | L12 app-design vocabulary. |
| "Unlabeled", "Labeled", "Data Labeling", "Label Studio" | 26 | L11. |
| "Supervised fine tuning model", "reward model", "reinforcement learning" | 27 | No tutorial in this series. |
| "Chunking", "Document Embedding", "Embedding Model", "Vector Database", "Indexing", "Retrieval", "Augmentation & Generation" | 28 | L05. |
| "Traditional Component", "Deterministic Execution", "AI Agent", "Autonomous Execution", "Workflow Orchestrators", "Hybrid Orchestrators", "Autonomous Orchestrators", "Full Agent Autonomy" | 29 | L06–L07. |
| "Pretrained Weights", "reparameterization (LoRA)" | 30 | L08. |
| "Model Trainer CLI Container", "Packaged Python files", "Job" | 32 | L13. |
| "Model Deployment CLI Container", "Update Model Signature", "Model Registry", "Model Endpoints" | 33 | L15. In v4 the Model Deploy step uploads to the registry and creates a new endpoint each run (digest §6 #15). |
| "Persistent Folder", "Secrets", "Mount Source Code into Container" | 35 | L18; v4's API keeps a PVC at `/persistent` on GKE. |
| "Ingress Controller", "NodePort" | 37 | L22. The tutorial's services are ClusterIP behind an ingress, and the API path is `/api-service`. |

## Commands and code on the slides

The slides show no workflow YAML, no Pulumi code and no Docker commands.

- Slide 20 (the "Basic format" block):
  - `# Basic format`
  - `git add`
  - `git commit -m "your message /deploy-app"`
  - `git push`

  Note: a bare `git add` stages nothing (Git replies "Nothing specified, nothing added."); the
  README's `git add .` is the working form. Use that on screen.
- Slide 20 URLs: `https://github.com/dlops-io/cheese-app-v4/tree/main/.github/workflows`,
  `https://github.com/dlops-io/cheese-app-v4#cheese-app---automation`,
  `https://github.com/dlops-io/cheese-app-v4/actions`
- Slide 30 (LoRA labels): `W ∈ ℝ^(d×d)`, `A = N(0, σ²)`, `B = 0`, and the dimensions `d`, `r`,
  with input `x` and output `h`
- Slide 32 (tiny code in the notebook and Python-file panes): `def get_dataset():`,
  `def get_model_1():`, `def get_model_2():`, `train_data, val_data = get_dataset(...)`,
  `model_1 = build_model_1(...)`, `training_results = model_1.fit(...)`; the Python-file
  version ends `model = ...` and `training_results = model.fit(...)`
- Slide 26: bucket `cheese-app-data-demo`, folders `cheeses_unlabeled`, `cheeses_labeled`
- Slide 37 (edge labels): `nginx-ip.sslip.io/`, `/`, `/api/`, `vector-db:8000`, and the ports
  `NodePort:3000`, `NodePort:9000`

## What the lecture stresses

- **Automate everything that ships:** data jobs, training and model deployment, frontend,
  backend, and image builds (slides 5, 6).
- **Close the loop:** every stage after Codebase notifies the developers, not just the tests
  (slides 7, 36).
- **Know the two kinds of check:** coding standards (style, consistency) vs static analysis
  (defects and vulnerabilities, found without running the code); the distinction is repeated on
  three slides and highlighted on slide 10 (slides 8–10).
- **Delivery vs deployment is the human release button** (slides 11, 12, notes on both).
- **CI for ML has a cost trade-off:** frequent integration vs the compute cost of training and
  long-running tests on large data and complex pipelines; keep data, features and model
  versions compatible as they evolve (slides 13, 14).
- **CD for ML must validate before releasing:** metrics within tolerance; watch for data drift;
  complex models such as LLMs are hard to validate; cost is a challenge (slide 15).
- **Do not build new machinery; automate what you have.** The deployment container already does
  the work; GitHub Actions only has to run it on each commit (slides 17, 18).
- **The trigger lives in the commit message** (`/deploy-app`, slide 20).
- **Review emphases:** LoRA "runs parallel" to the original model (slide 30, the deck's only
  "Notice" line); the labeling question "How do we do this?" (slide 26); in the team Docker
  workflow, one senior developer consolidates and publishes images (slide 24), the manual job
  that CI/CD replaces.
- **Honest naming:** slide 17 says "CI/CD" but slide 18 narrows it to "How to Implement CD",
  which matches the README's admission that v4 implements only continuous deployment.

## Pointers

- **Slide 20: the tutorial.** The workflows folder, the README section "Cheese App - Automation"
  (`#cheese-app---automation`, a valid anchor), and the instructor's Actions run list, with a QR
  code. The deck mentions only `/deploy-app`; the ML keywords (`/run-ml-pipeline`,
  `/run-data-collector`, `/run-data-processor`) are README-only.
- **Not on the slides (tutorial only, for scene authors):** the Actions secret
  `GOOGLE_APPLICATION_CREDENTIALS`, Pulumi stacks and the state bucket, timestamp image tags and
  the rolling update, the `workflow` container for the ML lane, the switch to a Google HTTPS load
  balancer, and cost and clean-up. All are in the digest.
- **Slide 16: CI/CD services named:** TeamCity, GitHub, GitLab, Jenkins, CircleCI, TravisCI.
- **No readings, homework or milestone notes appear on the slides.** (The digest, §7, ties v4 to
  Milestone 5 and the final showcase from the course site.)
- **Review slides → this year's decks → this series.** The review's lecture numbers come from a
  different numbering than this year's decks. The table maps each review slide to the 2025 deck
  where its picture or terms appear (found by text match) and to the series episode folder.

| Slide | Label on the slide | 2025 deck (where it appears) | Series episode |
|---|---|---|---|
| 22 | Lecture 2-4 | L03 slide 4 (the "Recap" with the same "Docker" band); L02 slide 10 (the original, whose band reads "Container Program"); L01 slide 73 (the venv/VM summary) | `ac215-l01-vms-venvs`, `ac215-l02-containers-1` |
| 23 | Lecture 2-4 (title reused) | L03 slide 25 (the audio pipeline) | `ac215-l03-mega-pipeline` |
| 24 | Lecture 5 | L03 slides 67–68 and L04 slides 39–40 ("Scenario 2") | `ac215-l03-mega-pipeline`, `ac215-l04-flexible-workflow-ports` |
| 25 | Lecture 6: App Design | L12 ("Solution Architecture"); also L18a | no tutorial episode for L12 |
| 26 | Lecture 6: Data Labeling… | L11 (Label Studio, slide 5 onward) | `ac215-l11-data-labeling-versioning` |
| 27 | Lecture 7 | not found in the text of the decks provided | (nearest: `ac215-l08-llm-finetuning`) |
| 28 | Lecture 8-9: RAGs | L05 (RAG I and RAG II) | `ac215-l05-rag` |
| 29 | Lecture 10: Agents | L07a slide 36 ("Autonomous Orchestrators") | `ac215-l06-agents-1`, `ac215-l07-agent-harness` |
| 30 | Lecture 11: LoRA | L08 (fine-tuning; LoRA, QLoRA) | `ac215-l08-llm-finetuning` |
| 31 | Lecture 11: Distillation | only named, as a bullet: L01 slide 10 ("Distillation & compression") and L13 slide 5 (under "Better/Faster Models") | — |
| 32 | Lecture 12 | L13 slide 24 onward ("Package & Upload to GCP", "Model Trainer CLI") | `ac215-l13-training-workflows` |
| 33 | Lecture 13 | L15 slide 12 onward ("Update Model Signature", "Model Endpoints") | `ac215-l15-vertex-ml-workflows` |
| 34 | Lecture 14: ML Pipelines | L15 | `ac215-l15-vertex-ml-workflows` |
| 35 | Lecture 15-16 | L18a/L18b (APIs, MCP, frontend) | `ac215-l18-apis-frontend` |
| 36 | Lecture 17-18: CI, Testing | L09 (software development for ML, tests) and L21 (slide 21's CI loop) | `ac215-l09-ci-testing`, `ac215-l21-cicd-github-actions` |
| 37 | Lecture 19-20 | L20 (Pulumi) and L22 (Kubernetes); the routing picture matches the L22 tutorial's NGINX ingress | `ac215-l20-deployment-pulumi`, `ac215-l22-kubernetes-cloud` |

  On screen, cite this year's numbers (or the episode titles), not the slide labels, so viewers
  can find the matching video.

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only [`digest.md`](digest.md) and this
file: there is no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. So the map below uses
the nine planned chapters in `digest.md` §8, the study guide
(`MLOps_Learning/guides/L23-final-cicd-deployment.md`) and every slide: the extracted text, all five
contact sheets, and enlarged renders of slides 19 and 20. With no captures yet, "the tutorial today"
means `dlops-io/cheese-app-v4` at the digest's pinned commit `033f187`, which is still the head of
`main` in a fresh clone on 2026-10-16. For this section I re-checked these at the source, in that
clone:
- README.md: the promise to "test, execute, monitor, deploy, and scale" (`:3`); the Model Deploy
  bullet (`:8`); the three definitions and "The CI part is not implemented" (`:151-157`);
  `/run-deploy-app` (`:162`); `/deploy-app` and `git add .` (`:188-192`);
- `images/ci-cd.png`: its GitHub Actions box reads Build → Release → Deploy, where slide 19's reads
  Build → Deploy;
- `app-ci-cd-gcp.yml:1-9`, `:32-56` (builds `src/deployment` and runs it with the single argument
  `deploy-k8s-update.sh`) and `ml-ci-cd-gcp.yml:1-9`, `:32-35`, `:55`, `:75`, `:95` (builds
  `src/workflow` and runs `python cli.py --data_collector`, `--data_processor` or `--pipeline`);
- `src/deployment/`: `deploy-k8s-update.sh` (two `pulumi up`s), `deploy-ml-images.sh` (nothing calls
  it), and no Vertex AI code anywhere in the folder (grep for `aiplatform` and `vertex`);
- the `origin/pipenv` branch, whose deployment folder did carry `cli.py` with `aip.PipelineJob` and
  `run-ml-pipeline.sh`, and whose ML workflow ran `cheese-app-deployment sh run-ml-pipeline.sh`;
- `deploy_k8s`: `setupSSL: "true"` (`Pulumi.dev.yaml:7`), the Ingress paths `/api-service` and `/`
  (`setup_loadbalancer_ssl.py:70`, `:83`), ClusterIP Services (`setup_containers.py:98`, `:183`,
  `:359`) and the NEG and BackendConfig annotations on the API Service (`:354-355`); the same path
  and Service types in the digest's copy of `cheese-app-v3` (L22);
- `src/workflow/model.py:67-104`: the `model_deploy` component uploads `gs://<bkt>/model` to the
  Model Registry and deploys it; it changes no signature;
- a bare `git add`, run with git 2.43.0 in a throwaway repo: it prints "Nothing specified, nothing
  added.", exits 0 and stages nothing.

When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 1, 3, 4 and 6–9 against them. If
they disagree, the captures win.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | The deploy button is a sentence (1.5 min) | 20 (commit with `/deploy-app` in the message); 12 (the red RELEASE button a person presses); 7 (commits enter the loop) | The tutorial applies it. The plan's self-pressing red button is slide 12's release button, but the plan doesn't say so (gap 1). |
| 2 | The whole course on one map (3 min) | 19 (the Cheese App CI/CD map); 21–37 (the review: one picture per earlier lecture); 25 (the three-layer architecture); 5–6 (the five operations to automate) | Same concept. The plan's recap map is the review section made concrete. Its "pull the loop apart" is exactly where the code leaves slide 19 (Conflicts 2–3). The five operations are not used (gap 4). |
| 3 | Bootstrap once, by hand (3 min) | 17 (we already have a deployment container); 24 (a senior developer builds and pushes the images by hand) | Mostly tutorial-only: stacks, registry, keys, the secret. Slide 17's premise is what this checklist makes true; slide 24 is the job CD takes over (gap 5). |
| 4 | Two sieves for one string (2.5 min) | 18 (GitHub Actions monitors code commits); 20 (the keyword) | The tutorial applies it. `on: push`, `contains()`, `head_commit` and the case-insensitive substring match are tutorial-only. Slide 20 has the keyword right where one README sentence doesn't (Conflict 6). |
| 5 | One crate, two operators (3 min) | 17–18 (build and run the deployment container; "Invoke CLI" in it); 35 (in development, the source code is mounted into the containers); 16 (other CI/CD services) | Same concept; the tutorial applies it with a script, not a CLI, and with a second container for the ML lane (Conflict 1). Baked code, the Docker socket and the identity hops are tutorial-only. |
| 6 | Follow the timestamp (3.5 min) | 18 (build and push images "for release", deploy them to the K8s cluster); 19 (Build → Deploy); 36 (Release before Deploy) | The tutorial applies it. Timestamp tags, the state bucket, `StackReference` and the rolling update are tutorial-only; "release" is drawn three ways (Conflict 3). |
| 7 | The front door changed (2 min) | 37 (L22's routing: one URL, `/` and `/api/` behind an ingress controller) | Same concept, different implementation: v4 replaces the NGINX controller with a Google HTTPS load balancer, and the API path is `/api-service` (Conflict 8). Health checks and managed certificates are tutorial-only. |
| 8 | The ML lane (3 min) | 5–6 (data pipeline jobs; model training and deployment); 13–15 (CI and CD for ML); 17–18 (Vertex jobs from the deployment container, with newly built images); 34 (the four-step pipeline graph); 32–33 (training jobs; model deployment); 19 (the arc) | Same concept; the tutorial applies it with its own container and with step images CI never rebuilds (Conflict 1). Validation and drift are lecture-only (gap 3). Slide 33's steps are split differently in the pipeline (Conflict 9). |
| 9 | Do it, break it, clean it up (3.5 min) | 20 (the basic commands); 7, 36 (Monitor and Notifications); 15 (cost as a challenge of CD) | The tutorial applies it. The README's mismatches, the green run that deployed nothing and the shutdown list are tutorial-only. Slide 20's bare `git add` is Conflict 7. |
| — | not in the plan | 1–3, 21, 38 (title, outline, dividers, close); 4 (the turkey predictor); 8–10 (CI defined: tests, coding standards, static analysis); 11 (delivery and deployment in words); 13–14 (CI for ML); 16 (providers); 22–23, 26–31 (the review of environments and containers, the audio pipeline, labeling, ChatGPT's training, RAG, agents, LoRA, distillation) | Lecture-only. 8–11 are gaps 1–2, 13–14 gap 3, 16 gap 6, 4 gap 7. The LLM review slides (27–31) fall on boxes ch2 already badges (the API's chat, RAG and agent routes). |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | A commit message starts the deployment: a workflow file in `.github/workflows` holds the steps, `/deploy-app` in the message triggers them | ch1, ch4 ↔ 20 | Yes, word for word. The plan adds what the slide leaves out: every push to `main` runs both workflows, and only the job is skipped. |
| 2 | Don't build new machinery: GitHub Actions builds the deployment container and runs it on each commit | ch3, ch5 ↔ 17–18 | Yes for the app lane; ch5's "one crate, two operators" is slide 17's premise. It differs on the ML lane and on "CLI" (Conflict 1). |
| 3 | Build and push images for release, then deploy them to the K8s cluster | ch6 ↔ 18, 19 | Yes. The slide states the two steps; the plan follows one tag from the build to the pod. |
| 4 | One map of the system: Dev Team → GitHub → GitHub Actions → Google Cloud (Storage, Vertex AI, Kubernetes) → Users, over the chain of six components | ch2 ↔ 19 | Partly. The plan redraws the map, then splits it into two loops, because the Model Deploy → Backend API link is not in the code (Conflict 2). |
| 5 | The CI/CD loop: commits, build, test, (release,) deploy, monitor, with notifications back to the developers | digest C1 (the gates track with the CI gates greyed out) ↔ 7, 36 | Yes. The digest's track is slides 7/36 with the red half switched off. No chapter uses it yet (gap 2). |
| 6 | CI, delivery and deployment are three different promises | digest C1 (the restaurant analogy), guide §3.1 ↔ 8–12 | Partly. Both say CI integrates and tests, and both say deployment needs no human. They define delivery differently (Conflict 5). |
| 7 | This tutorial implements the CD half only | digest C1's misconception, §7 (MS5) ↔ 18 ("How to Implement CD") | Yes. Slide 18's heading drops "CI", as `README.md:157` does; slide 20's title and the workflow names keep it (Conflict 4). |
| 8 | Data pipeline jobs, training and model deployment run automatically on Vertex AI | ch8 ↔ 5–6, 15, 17–18, 34 | Yes on what runs: the same four steps with the same names. It differs on which container submits them and which images they use (Conflict 1). |
| 9 | One URL, path-based routing to the services | ch7 ↔ 37 | Partly: the same shape, a different front door and path (Conflict 8). |
| 10 | Every earlier lecture built a part of the final app | ch2 (the recap map with lecture badges), guide §7 ↔ 21–37 | Yes. The plan badges the boxes with this year's lecture numbers; the review slides print another year's numbers (see Pointers). |
| 11 | Cost is a challenge of CD for ML | ch8 (the endpoint meter), ch9 (the bill meter) ↔ 15 | Yes. The plan makes it concrete: another endpoint billed 24/7 on every `/run-ml-pipeline`, new image tags on every deploy. |
| 12 | In development, the code is mounted into the containers | ch5 (the laptop/runner split), guide §8 E6 ↔ 35 | Yes, for the laptop half. Slide 35 mounts the API's and the frontend's source; ch5's laptop half mounts the deployment code the same way (`docker-shell.sh:37`). On the runner the deployment container's own code is baked in (`ADD --chown=app:app . /app`, `Dockerfile:72`), while the app folders are still mounted (`app-ci-cd-gcp.yml:43-47`). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Delivery vs deployment is a question of who presses release, and in v4 a person presses it
   (slides 11–12).** In the lecture's terms, continuous delivery keeps a person in the loop who
   decides to release, and continuous deployment passes every integrated change into production by
   itself. In v4 a push to `main` deploys nothing unless someone types `/deploy-app`: that keyword is
   slide 12's red RELEASE button, with no tests in front of it. The README calls the tutorial
   continuous deployment (`README.md:157`), but its own definition (`:155`) requires the automated
   tests to pass first (Conflict 5). This is what MS5 changes: drop the keyword, deploy on every
   merge to `main`, and put L21's tests in front (guide §8 E7). **Carry it in** ch1 (20 s: label the
   plan's red button RELEASE) and ch9's outro (30 s, with a new pause-and-ponder; see the proposals).
2. **The CI half of the loop, and notifications that tell the truth (slides 7–10, 36).** The
   lecture's loop has a red CI half (Codebase → Build → Test) and a blue CD half (Release → Deploy →
   Monitor), and every stage after Codebase reports back to the developers. CI is defined by what
   it runs: automated tests, coding standards (style and consistency) and static analysis (defects
   and vulnerabilities, found without running the code). v4 builds, releases and deploys, but its
   Test box is empty and nothing monitors automatically (Conflict 4), and its one notification, the
   run's colour, can be wrong: with no `set -e` in
   `deploy-k8s-update.sh`, a failed image build followed by an unchanged K8s update reports green
   (guide §6 #4). The digest sketches the gates track (C1), but no chapter uses it. **Carry it in**
   ch1 (last 20 s: draw the loop and grey out Test) and ch9 (the green run that deployed nothing is
   the notification line telling a lie; the Monitor box is the footer check and
   `kubectl rollout status`).
3. **CD for ML releases a model only after it passes validation (slides 13–15).** The lecture
   wants CI for ML to catch data-quality, code and model-performance problems early; it warns that
   training cost and long tests on large data pull against frequent integration; and it asks CD to
   release a model only when its metrics stay within tolerance, while watching for data drift. v4's
   `/run-ml-pipeline` deploys whatever the training step produced, to a new endpoint each run, with
   no metric check, and the trainer does not even read the freshly processed data (digest C7). MS5
   asks for validation thresholds and for retraining when new data arrives (guide §7). **Carry it
   in** ch8 (30 s: a dashed "metrics within tolerance?" gate between Model Training and Model
   Deploy) and the recap card.
4. **The five operations as a scorecard (slides 5–6).** The lecture lists what it wants automated:
   data pipeline jobs, model training and deployment, frontend deployment, backend deployment, and
   building and pushing images. Scoring v4 shows the student what is still manual. Data jobs
   (`/run-data-collector`, `/run-data-processor`) and training plus deployment (`/run-ml-pipeline`)
   are automated. Frontend and backend are automated, but only together: one keyword rebuilds and
   rolls all three images. Building and pushing is automated for the three app images and **not**
   for the two ML step images (`deploy-ml-images.sh`, by hand; guide §6 #3). **Carry it in** ch2
   (20 s after the map splits: slide 6's five cards get a tick, a shared bracket or a half tick) or
   as the recap's first card.
5. **The job CD takes over: the senior developer (slide 24).** In the team Docker workflow of
   L03/L04, one senior developer merges the pull requests, rebuilds the images and pushes them. In
   v4 the runner does that job on every keyword, with the same toolbox container a person uses on
   the laptop. **Carry it in** ch3 or ch5 (one sentence; a small figure hands its key to the runner).
6. **Thin YAML, thick container (slide 16).** The slide names six CI/CD services. Because v4's
   workflow only builds a container and runs it with one argument, nearly all the deploy logic lives
   in `src/deployment` (and `src/workflow`); moving to another service would mean rewriting two
   short workflow files (56 and 96 lines), not the deployment (our reasoning, not on the slide). **Carry it in** ch5 (one sentence over the crate).
7. **Why deploy at all (slide 4).** The deck opens on a joke web app that predicts when the
   Thanksgiving turkey will be done, with a forecast band that widens past "NOW". The slide says
   nothing about CI/CD; our reading is that a prediction is only useful if it is served and kept
   current as new readings arrive. Low value for doing the tutorial, but a friendly way into the ML
   lane. **Carry it in** ch8's first 10 s if time allows; never show the slide.

### 4. Conflicts

| # | Slides say | Tutorial today (the repo at `033f187`) | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **One deployment container does everything, through a CLI** (slides 17–18): it builds images, runs the Vertex AI pipeline jobs and deploys to the K8s cluster; GitHub Actions builds it and invokes its CLI to build and push release images, run Vertex jobs with the newly built images, and deploy. | Two workflows, two containers. `app-ci-cd-gcp.yml` builds `src/deployment` and passes the script name `deploy-k8s-update.sh` (`:35`, `:56`): two `pulumi up`s, no CLI. `ml-ci-cd-gcp.yml` builds `src/workflow` (`:32-35`) and runs `python cli.py --pipeline` (or `--data_collector`, `--data_processor`) there. `src/deployment` holds no Vertex AI code. CI never rebuilds the data-collector and data-processor images: the pipeline uses whatever `deploy-ml-images.sh` last pushed by hand (digest §6 #3). The slides describe the older `origin/pipenv` design, where the ML workflow ran `cheese-app-deployment sh run-ml-pipeline.sh` (and even there the image rebuild line was commented out). | The repo | Ch5: "The lecture keeps everything in one toolbox. v4 splits it: the deployment crate for the app, a smaller workflow crate for Vertex." Ch8, before pause-and-ponder #3: "and the step images are whatever you last built by hand." |
| 2 | **One chain from data to users** (slide 19, and the README's `images/ci-cd.png`): Data Collector → Data Processor → Model Training → Model Deploy → Backend API → Frontend, all driven by commits. | Two lanes that don't touch. The API loads a fixed CNN from a GitHub release (`llm_cnn_utils.py:124`); `/run-ml-pipeline` deploys to a new Vertex endpoint that nothing calls; the trainer downloads a fixed dataset instead of the processor's output (digest C7, errata 8). | The code | Ch2, as planned: draw the slide's chain first, then pull it apart. "This is the course's map, and the goal. In v4 the arrow from Model Deploy to the API is still to be built: that is MS5." |
| 3 | **What happens inside GitHub Actions** (slide 19 vs the README image and slide 36): slide 19's box holds Build → Deploy; the README's copy of the same picture holds Build → Release → Deploy; slide 36's loop has a Release stage, slide 7's doesn't. | One job with two container steps. Inside "Run Deploy App", `deploy_images` builds the three images and pushes them with a timestamp tag (the release, in effect), and `deploy_k8s` deploys them (`deploy-k8s-update.sh:1-9`). There is no separate release step or gate. | The code; both pictures are fair summaries of it | Ch6: two boxes for the two `pulumi up`s, with the push between them tagged "release = `:<timestamp>`". "The lecture's pictures differ by one box. In this repo, the release is the moment the tagged image lands in the registry." |
| 4 | **CI/CD** (slide 20's title "Tutorial: Continuous Integration, Continuous Deployment" and its "Steps to apply CI / CD"; slides 7 and 36 draw Test and Monitor stages). | No test, lint, static-analysis or monitoring step runs in either workflow, though both are named "Continuous Integration and Continuous Deployment" (`:1`). `README.md:3` promises to test, execute, monitor, deploy and scale; `:157` says the CI part is not implemented. Slide 18's own heading, "How to Implement CD", agrees with `:157`. | The repo and `README.md:157` | Ch1 and ch9: "The lecture draws the whole loop. This tutorial wires every box except Test; the tests are the pipeline you built in L21, and MS5 asks you to join them." |
| 5 | **Delivery vs deployment** (slides 11–12): delivery keeps a person in the loop who decides to release; deployment passes integrated changes into production automatically. | The README defines delivery as automated delivery to staging or testing environments, ready but not necessarily released (`README.md:153`), and deployment as automatic deployment once all automated tests pass (`:155`); it says the tutorial does deployment (`:157`). In the code, a person decides every release by typing `/deploy-app`, and no tests run. | Both definitions are common; the code settles what v4 is: an automated deploy that a person triggers, with nothing tested first | Don't argue it, ask it (the new pause-and-ponder in ch9): "By the lecture's definitions, the keyword is delivery's release button. Deploy on every merge, behind tests, and it becomes continuous deployment." |
| 6 | **The keyword** (slide 20): `/deploy-app`. | `app-ci-cd-gcp.yml:9` tests `'/deploy-app'`, and `README.md:188`, `:192` agree. `README.md:162` says `/run-deploy-app`, which wakes the ML job and deploys nothing (guide §6 #1). | The slide and the workflow | Ch4, in pause-and-ponder #1's answer: "The lecture slide has it right; one sentence in the README doesn't." |
| 7 | **The basic commands** (slide 20): `git add`, then `git commit -m "your message /deploy-app"`, then `git push`. | A bare `git add` stages nothing (git 2.43.0: "Nothing specified, nothing added.", exit code 0); the commit then has nothing to commit, and the push sends nothing new. `README.md:191` has `git add .`. | The README | No narration. Type `git add .` on screen; if a caption is wanted: "the slide's shorthand, written out". |
| 8 | **Routing** (slide 37, the L22 review): an ingress controller at `nginx-ip.sslip.io/` sends `/` to a Frontend Service on NodePort 3000 and `/api/` to an API Service on NodePort 9000, which calls `vector-db:8000`. | `setupSSL: "true"` gives a GCE Ingress, i.e. a Google HTTPS load balancer with a global static IP and a managed certificate, at `https://<static-ip>.sslip.io`. The paths are `/api-service` and `/` (`setup_loadbalancer_ssl.py:70`, `:83`); the Services are ClusterIP (`setup_containers.py:98`, `:183`, `:359`), the API's with NEG and BackendConfig annotations (`:354-355`). L22's NGINX version also used `/api-service` and ClusterIP (`cheese-app-v3`: `setup_loadbalancer.py:84`, `setup_containers.py:98`, `:183`, `:332`). | The code | Ch7: start from slide 37's shape, then swap the doorman. "Same routing, new front door. The API lives under `/api-service`, and Google now checks that it answers before sending anyone in." |
| 9 | **Model deployment in five steps** (slide 33, the L15 review): get the saved model, update its signature, upload it to GCS, upload it to the Model Registry, deploy an endpoint, all from a Model Deployment CLI container. `README.md:8` also says the Model Deploy step updates the signature. | In v4's pipeline the trainer saves the model with its serving signature (`ml-workflow`'s `trainer/task.py`, per the L15 digest). The Model Deploy component only uploads `gs://<bkt>/model` to the Registry and deploys it, to a new endpoint on every run (`src/workflow/model.py:67-104`; guide §6 #15). | The code | Ch8, one sentence: "In the pipeline the trainer already adds the signature, so Model Deploy does the lecture's last two steps, and makes a new endpoint each time." |

Not counted as conflicts:
- The review slides print lecture numbers from another year's schedule (see Pointers); slides 10,
  12, 23, 24 and 29 print footer numbers from their source decks. Both are inside the deck.
- Slide 24's image registry is Docker Hub (spelled "DockertHub"); v4 pushes to Artifact Registry.
  The slide is accurate for the L03/L04 workflow it reviews.
- Slide 18 says GitHub Actions monitors code commits. v4 watches pushes to `main` and reads only
  the last commit's message; that is a narrowing, which ch4 makes exact, not a contradiction.
- Slide 32's Model Trainer CLI container launches training jobs; in v4 the pipeline's training
  component launches them. Both designs exist in the course (L13, L15).
- Slides 13–14 integrate code, data and models "into a shared repository"; v4 keeps its data in
  GCS and its model in a GitHub release and on Vertex. That is an omission (gap 3).
- Slide 6's arrows between the five cards only order the list.
- Slide 35's mounted source code and v4's baked code are each right in their place (in common, 12).
- Slide 20's QR code was not decoded (40 dpi page, no decoder installed). Its three printed URLs
  point at things that exist in the clone: `.github/workflows`, the README heading "Cheese App -
  Automation" (anchor `#cheese-app---automation`) and the repository's Actions tab.

### 5. Proposals for the BRIEF and script authors

**General**
- Tag each chapter that stands on lecture ground with one GREY `lecture_ref`. L23 has one deck,
  so plain ranges are enough: `lecture_ref(23, "17–18")` reads "Lecture 23 · slides 17–18". Use
  the PDF page numbers listed here, never the footers. Re-draw every lecture diagram in the series
  style; never show the slide images, the turkey page, the distillation photo or the QR code.
- **Spine: slide 36's loop as the video's progress strip.** Six boxes, Codebase → Build → Test →
  Release → Deploy → Monitor, with a Notifications line back to a Developers bar (slide 7's
  layout). Test stays a dashed GREY outline for the whole video, labelled "L21" (Conflict 4).
  Ch1 lights Codebase, ch4 the arrow out of it, ch5 Build, ch6 Release and Deploy, ch7 the front of
  Deploy, ch9 Monitor and the Notifications line, which turns RED when the `set -e` lie shows
  (gap 2). Ch8 adds a second, thinner strip for the ML lane with its Build box half lit (only the
  workflow container is built). Colours: runners BLUE, containers and images TEAL, the current box
  YELLOW, failures RED, cost GOLD, routes PINK.
- **Second frame: slide 19's map in ch2**, redrawn with slide 19's two Actions boxes, then pulled
  apart into the app gear and the ML gear (Conflicts 2–3), then slide 6's five cards scored
  (gap 4). Badge the boxes with this year's lecture numbers, not the review slides' labels.
  Optionally lay the badges on slide 25's three bands (Process, Execution, State). Don't build one
  card per review slide; seventeen cards would eat the chapter.
- **Hook.** Keep the plan's hook (eleven characters, and the README's `/run-deploy-app`). Pause-and-
  ponder #1's answer gains one line: the lecture slide has the right keyword (Conflict 6).
- **One new pause-and-ponder (ch9), from slides 11–12 and Conflict 5.** "By the lecture's
  definitions, is v4 continuous delivery or continuous deployment? What would you change to make
  it the other?" *Answer:* a person decides each release by typing the keyword, which is
  delivery's release button; and nothing is tested first, so it isn't the README's continuous
  deployment either. Deploying on every merge to `main`, behind L21's tests, makes it continuous
  deployment, which is what MS5 asks for (guide §8 E7).
- **Time.** The plan is about 25 minutes. Gaps 1–6 add about 3–3.5 minutes and gap 7 another 10 s,
  which brings the video to about 28–29 minutes, inside the 25–35 range; nothing needs to be cut.
- **Captures.** When they are made, record:
  - the Actions tab after one push: two runs, one with its job skipped;
  - the "Run Deploy App" log with `deploy-k8s-update.sh` echoed and the two Pulumi updates, images
    first (Conflicts 1, 3);
  - a `/run-data-collector` run whose log ends in a pipeline submitted from `cheese-app-workflow`
    (Conflict 1);
  - `kubectl describe ingress -n cheese-app-namespace` showing the `gce` class annotation and the
    `/api-service` rule, and `kubectl get svc` showing ClusterIP (Conflict 8);
  - the Vertex pipeline graph with four green nodes, the new model and the new endpoint
    (Conflict 9).

  Then re-check Conflicts 1, 3, 4 and 6–9 against them.

**Per chapter**
- **Ch1 · `lecture_ref(23, "11–12, 20")`.** Label the plan's self-pressing button RELEASE and say
  once whose finger it is: "you press it, by typing the keyword" (gap 1). Last 20 s: the strip
  appears with Test greyed out (gap 2, Conflict 4).
- **Ch2 · `lecture_ref(23, "5–6, 19, 21–37")`.** Slide 19's map, the split into two gears with the
  dashed "TODO (MS5)" arrow (Conflict 2), then the five-operations scorecard (gap 4). Name the
  review once: "the lecture closes by walking back through every earlier lecture; here are its
  boxes in the app."
- **Ch3 · `lecture_ref(23, "17, 24")`.** Open on slide 17's premise as the checklist's first line:
  the toolbox must work by hand before a robot can run it. One sentence on slide 24's senior
  developer, whose job the runner is about to take (gap 5).
- **Ch4 · `lecture_ref(23, "18, 20")`.** Make slide 18's "monitoring code commits" exact: pushes to
  `main`, the last commit's message, a substring in any case. Conflict 6 in pause-and-ponder #1.
- **Ch5 · `lecture_ref(23, "17–18, 35")`.** The crate's button reads `deploy-k8s-update.sh`, not
  "CLI" (Conflict 1). The laptop half of the split screen mounts the code, as slide 35's
  containers do; the runner half has the deployment code baked in. One sentence on slide 16
  (gap 6).
- **Ch6 · `lecture_ref(23, "18–19, 36")`.** The strip lights Build → Release → Deploy; the release
  is the push of the timestamp-tagged image (Conflict 3). Pause-and-ponder #2 as planned.
- **Ch7 · `lecture_ref(23, "37")`.** Slide 37's routing re-drawn, then the swap: NGINX doorman out,
  Google front desk in; `/api/` becomes `/api-service`, NodePort becomes ClusterIP behind the load
  balancer (Conflict 8).
- **Ch8 · `lecture_ref(23, "13–15, 17–18, 34")`.**
  - Optional first 10 s: the turkey idea in one sentence (gap 7).
  - Slide 34's four nodes are the Vertex graph; the second, smaller crate submits them
    (Conflict 1), and pause-and-ponder #3 lands on the stale step images.
  - The dashed "metrics within tolerance?" gate and a "new data → retrain" arrow, both labelled
    MS5 (gap 3). One sentence for Conflict 9.
- **Ch9 · `lecture_ref(23, "7, 11–12, 20")`.**
  - `git add .` on screen (Conflict 7).
  - The green run that deployed nothing is the Notifications line lying (gap 2); verifying the
    footer and `kubectl rollout status` is the Monitor box.
  - The new pause-and-ponder (gap 1, Conflict 5).
  - Outro: the strip with Test lit "from L21" and the keyword gone, as MS5's goal.
- **Recap card.** Keep the plan's six questions, and add two:
  - "Which of the lecture's five automated operations does v4 still leave to a person?" (Building
    and pushing the two ML step images, `deploy-ml-images.sh`; and frontend and backend can only be
    deployed together.)
  - "In the lecture's terms, is typing `/deploy-app` continuous delivery or continuous deployment,
    and what does MS5 change?" (Delivery's release button; MS5 deploys every merge to `main`,
    behind tests.)

**Terms**
- Use the lecture's words: *automation*, *CI/CD*, *continuous integration*, *continuous delivery*,
  *continuous deployment*, *release*, *production*, *deployment container*, *workflow file*,
  *notifications*, *monitor*, *coding standards*, *static code analysis*, *performance validation*
  ("within tolerance"), *data drift*, *Vertex AI pipeline jobs*, *K8s cluster*, *ingress
  controller*.
- Add the tutorial's words where the lecture stops: *workflow*, *job*, *step*, *runner*, `if:`,
  `contains()`, `head_commit`, *repository secret*, *toolbox container*, *Docker socket*,
  *timestamp tag*, *Pulumi state bucket*, `StackReference`, *rolling update*, *GCE Ingress*,
  *BackendConfig*, *managed certificate*, *Vertex endpoint*.
- Bridge each pair once:
  - the lecture's "invoke CLI in the deployment container" is `deploy-k8s-update.sh` in the app
    lane and `python cli.py --pipeline` in the separate `workflow` container;
  - the lecture's "release" is pushing the images with a fresh timestamp tag;
  - the lecture's "Backend API" is `api-service`;
  - the lecture's "Monitor" is, here, the run's colour, the footer versions and
    `kubectl rollout status`;
  - the lecture's ingress controller is, in v4, Google's load balancer, set up from the Ingress.
- Avoid "the deployment container runs the Vertex pipelines" (Conflict 1), "the new model goes
  into the app" (Conflict 2), "CI/CD" for v4 without "the CD half" (Conflict 4),
  `/run-deploy-app` (Conflict 6), a bare `git add` (Conflict 7), and "NGINX" or `/api/` for v4
  (Conflict 8).
