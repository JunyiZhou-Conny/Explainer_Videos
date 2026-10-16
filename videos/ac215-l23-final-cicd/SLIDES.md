# L23 lecture slides — Final Deployment and Review

Source: one deck, `L23_final_deployment_and_review` (38 slides), titled "Lecture 23: Final
Deployment and Review" (AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's
lecture slides (PDF), provided by the student for study; the PDFs are not in this repository;
slide numbers are PDF page numbers. Several slides were pasted in from other decks and print a
different footer number (slide 10 prints "6", slide 12 prints "7", slide 29 prints "67", and the
image on slide 24 carries its old "14"); this file always uses the PDF page. It was written from
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
   and tested (the CI half), then deployed and monitored (the CD half). Every stage reports back
   to the developers as notifications. The review version inserts "Release" between Test and
   Deploy. (Slides 7, 36)
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
    mount source code, secrets and a persistent folder, and the browser talks REST/JSON to one and
    gets HTML from the other (slide 35); CI/testing is the commit → build → test → release →
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
- **Close the loop:** every stage notifies the developers, not just the tests (slides 7, 36).
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
| 22 | Lecture 2-4 | L02 slide 10 ("Environments vs Virtualization vs Containerization"); L01's VM/venv summary | `ac215-l01-vms-venvs`, `ac215-l02-containers-1` |
| 23 | Lecture 2-4 (title reused) | L03 slide 25 (the audio pipeline) | `ac215-l03-mega-pipeline` |
| 24 | Lecture 5 | L03 slides 67–68 and L04 slides 39–40 ("Scenario 2") | `ac215-l03-mega-pipeline`, `ac215-l04-flexible-workflow-ports` |
| 25 | Lecture 6: App Design | L12 ("Solution Architecture"); also L18a | no tutorial episode for L12 |
| 26 | Lecture 6: Data Labeling… | L11 (Label Studio, slide 5 onward) | `ac215-l11-data-labeling-versioning` |
| 27 | Lecture 7 | not found in the text of the decks provided | (nearest: `ac215-l08-llm-finetuning`) |
| 28 | Lecture 8-9: RAGs | L05 (RAG I and RAG II) | `ac215-l05-rag` |
| 29 | Lecture 10: Agents | L07a slide 36 ("Autonomous Orchestrators") | `ac215-l06-agents-1`, `ac215-l07-agent-harness` |
| 30 | Lecture 11: LoRA | L08 (fine-tuning; LoRA, QLoRA) | `ac215-l08-llm-finetuning` |
| 31 | Lecture 11: Distillation | only named, in L13 slide 5 (one of the "levers") | — |
| 32 | Lecture 12 | L13 slide 24 onward ("Package & Upload to GCP", "Model Trainer CLI") | `ac215-l13-training-workflows` |
| 33 | Lecture 13 | L15 slide 12 onward ("Update Model Signature", "Model Endpoints") | `ac215-l15-vertex-ml-workflows` |
| 34 | Lecture 14: ML Pipelines | L15 | `ac215-l15-vertex-ml-workflows` |
| 35 | Lecture 15-16 | L18a/L18b (APIs, MCP, frontend) | `ac215-l18-apis-frontend` |
| 36 | Lecture 17-18: CI, Testing | L09 (software development for ML, tests) and L21 (slide 21's CI loop) | `ac215-l09-ci-testing`, `ac215-l21-cicd-github-actions` |
| 37 | Lecture 19-20 | L20 (Pulumi) and L22 (Kubernetes); the routing picture matches the L22 tutorial's NGINX ingress | `ac215-l20-deployment-pulumi`, `ac215-l22-kubernetes-cloud` |

  On screen, cite this year's numbers (or the episode titles), not the slide labels, so viewers
  can find the matching video.
