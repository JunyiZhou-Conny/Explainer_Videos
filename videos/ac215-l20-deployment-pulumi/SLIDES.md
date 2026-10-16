# L20 lecture slides — Deployment: Pulumi

Source: one deck, `L20_deployment_pulumi_updated` (30 slides), titled "Lecture 20: Deployment:
Pulumi" (AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's lecture slides
(PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are PDF
page numbers. This digest was written from the deck's extracted text, from every contact sheet, and
from enlarged single slides for 4, 7, 8, 12, 14, 17, 21–24, 26 and 27. The link targets on slides 8
and 28 were read from the PDF's link annotations. Everything below is paraphrased; only short
titles, terms, URLs and single code lines are quoted. The tutorial side of the lecture is in
[`digest.md`](digest.md).

## Outline

The deck has two numbered sections (slide 2). Divider slides repeat the outline with the current
section in bold.

- Slide 1 · title slide
- Slide 2 · outline (Recap; Deployment), nothing highlighted
- Slides 3–5 · **1. Recap**
  - 3 · section divider ("Recap" in bold)
  - 4 · "Recap: Cheese App Status": the POC → Prototype → MVP roadmap, with "Deployment, Scaling &
    Automation" marked as the current step
  - 5 · "Recap: APIs & Frontend App": everything so far runs on the local computer, and it now has
    to reach users from a server
- Slides 6–28 · **2. Deployment**
  - 6 · section divider ("Deployment" in bold)
  - 7 · "Deployment: Goal": the target architecture (laptop → one GCP VM running four containers)
  - 8 · "Tutorial: Deployment Steps (Manual)": the four manual stages, a tutorial link and a QR code
  - 9 · "Deployment Automation": too many manual steps to track, so automate (Pulumi logo)
  - Slides 10–18 · **Pulumi, the tool**
    - 10 · "Pulumi": what it is (infrastructure automation, infrastructure as code)
    - 11 · "Pulumi: History": founders, languages, where programs run, code instead of YAML/DSL
    - 12 · "Pulumi: Principles": six principles around the logo
    - 13 · "Pulumi: Concepts": the six concepts (CLI commands, programs, stacks, resources, state,
      providers)
    - 14 · "Pulumi: Concepts": "How Pulumi Works" (your machine → cloud providers)
    - 15 · "Pulumi: Commands": seven common CLI commands
    - 16 · "Pulumi: Running Programs": what `pulumi up [options]` does, and three flags
    - 17 · "Pulumi: Programs": declarative programs, with a GCS-bucket example in Python
    - 18 · "Pulumi: Stacks": isolated environments, per-stack state and config, naming convention
  - Slides 19–27 · **Deploying the Cheese App with Pulumi**
    - 19 · "Deployment Steps (Pulumi / Automation)": the six automated steps
    - 20 · "Setup local container /GCP": APIs, two service accounts, the local deployment container
    - 21 · "Build & Push Docker Images to GCR": diagram build-up, stage 1 (registry)
    - 22 · "Create Compute Instance (VM)": stage 2 (empty VM, bucket, persistent volume)
    - 23 · "Setup Docker Containers in VM": stage 3 (three app containers)
    - 24 · "Setup Web Server to expose App": stage 4 (NGINX, wiring, browser on port 80)
    - 25 · "Why did we need 2 service accounts?": what each account may do
    - 26 · "Why did we need 2 service accounts?": the full diagram annotated with three numbered
      credential needs
    - 27 · "Test the App": the finished diagram again
  - 28 · "Tutorial: Deployment to GCP (Pulumi)": the tutorial link, four steps and a QR code
- Slide 29 · "DON'T FORGET TO DELETE" (above a glitch-art picture)
- Slide 30 · "THANK YOU!!!" (a cartoon-dog image on a blue square)

## Key ideas

1. **The project is now in its deployment phase.** On the roadmap the red you-are-here box has moved
   from "Build Cheese App" (L18) to "Deployment, Scaling & Automation". That bar runs from the middle
   of Prototype to the end of MVP, so deployment, scaling and automation are the remaining lectures.
   (4)
2. **Working locally is not the same as being available.** Everything built so far (the APIs and the
   frontend of L18) runs on the student's own computer. Users can reach it only after it is deployed
   to a server. (5)
3. **The goal is one cloud VM running the whole app behind NGINX.** On GCP, one "Compute Instance
   (Virtual Machine)" hosts four containers. NGINX is the only one the outside world talks to, on
   HTTP 80. Behind it are the frontend (HTTP 3000) and the API service (HTTP 9000), and the API
   service uses the vector DB (HTTP 8000). Outside the VM but inside GCP, a GCS bucket holds models
   (HTTPS 443) and a GCE persistent volume holds local files (NFS). (7, 24, 27)
4. **The manual route has four stages.** Push the API and frontend images to Docker Hub. Create a VM
   and prepare it (Docker, folders, permissions). Run the containers on their own Docker network.
   Put NGINX in front as a reverse proxy that routes to the API and the frontend. (8)
5. **Too many manual steps is the reason to automate.** The lecture names the problem as keeping
   track of many steps, and the answer is a tool that does them for you. (9)
6. **Pulumi is infrastructure as code in ordinary programming languages.** Programs are written in
   Python, TypeScript, Go, C# or Java. They cover creating and deleting servers and clusters,
   installing and configuring software, and setting up networks. Because the infrastructure is code,
   it goes into GitHub and can be shared. (10, 11)
7. **Pulumi runs on one machine and talks to the cloud through its APIs.** A program runs on a
   workstation or a CI/CD runner. It uses functions, classes and loops instead of a YAML file or a
   domain-specific language. Pulumi was founded in 2017. (11)
8. **Six principles characterise the tool.** Real programming languages, declarative
   infrastructure, component-based architecture, multi-cloud support, state management with
   previews, and test-driven infrastructure. (12)
9. **How Pulumi works: desired state in, API calls out.** The CLI runs your program, and the program
   describes the infrastructure you want. Pulumi compares that desired state with the current one
   and sends API calls to the providers (AWS, Azure, GCP, Kubernetes …). The providers create, update
   or delete the resources. The slide's banner sums it up: Pulumi manages infrastructure through
   cloud APIs. (14)
10. **Six concepts organise the tool, but only three get slides of their own.** The six are CLI
    commands, programs, stacks, resources, state and providers. The commands (15–16), programs (17)
    and stacks (18) get their own slides. Providers appear only in the diagram on 14. State is
    mentioned in passing (12, 14, 16, 18), and resources only as what gets created, updated or
    deleted. (13–18)
11. **`pulumi up` is preview, confirm, apply.** It runs the program to work out the desired state,
    shows which resources would be created, updated or deleted, and asks before changing anything.
    Flags skip the prompt (`--yes`), pick the environment (`--stack <name>`) and re-read reality
    first (`--refresh`). `pulumi preview` only shows the plan. `pulumi destroy` removes everything
    in the stack, and `pulumi refresh` syncs the state with the real infrastructure. (15, 16)
12. **Programs are declarative even though they are code.** You describe what should exist (a
    bucket, with a location and a website setting), and Pulumi works out how to create it. Loops,
    conditionals, functions and classes are available to build that description. (17)
13. **A stack is one isolated copy of the infrastructure.** Dev, staging and production are separate
    stacks of the same program. Each has its own state and its own configuration values. The
    suggested naming is project plus environment, such as `cheese-app-dev`. (18)
14. **The automated deployment has six steps.** Set up a local container that can reach GCP. Build
    the images and push them to a registry. Create the VM. Provision it with the software it needs.
    Start the Docker containers on it. Add a web server that exposes the app. Slides 21–24 draw steps
    2, 3, 5 and 6 as one picture that grows. Step 4 (provisioning) has no picture of its own. (19,
    21–24)
15. **Setup before the first deployment.** Enable the GCP APIs, create two service accounts, give
    the local deployment container their secret keys, and tell it which GCP project to use. (20)
16. **Two service accounts keep powers apart.** `deployment` has admin rights on the group's
    project, because it must create the VM and SSH into it. `gcp-service` only needs to read: images
    from the registry, and models from the class bucket. It also needs Vertex AI access for
    inference. The admin key stays with the developer's deployment container, and the narrow key is
    what the running app uses. (20, 25, 26)
17. **Test from a browser.** The finished system is checked by opening the app in a browser, which
    reaches it through NGINX on port 80. (27)
18. **The tutorial does these steps in its four stages, and you clean up afterwards.** The Pulumi
    tutorial builds and pushes the images, creates the VM, provisions it, and deploys the API,
    frontend and NGINX containers. The deck closes with a reminder to delete what you created. (28,
    29)

## Diagrams

- **4 · project roadmap (Gantt-style).** A wide light-blue arrow runs left to right with three phase
  labels, "POC", "Prototype" and "MVP". Grey dashed vertical lines mark the two phase boundaries and
  the end. Below it are staggered horizontal bars:
  - "Design Cheese App" (peach): from the start to a little past the Prototype/MVP boundary.
  - "Data Collection" (blue-grey): early POC.
  - "Setup Experiment Tracking" (pink): POC, just crossing into Prototype.
  - "Build Baseline Models" (light green): late POC into early Prototype.
  - "Build Better Models" (light green) and "ML Workflow" (pale yellow): stacked, inside Prototype.
  - "Build Cheese App" (blue-grey): all of MVP.
  - "Deployment, Scaling & Automation" (lilac): from mid-Prototype to the end of MVP.

  A red dashed rectangle surrounds the lilac bar. Purpose: place the lecture on the project
  timeline. Compared with L18's version of the same chart, the marker has moved down one bar.
- **7 · "Deployment: Goal" (from laptop to cloud).** Left: a pink box "Local Computer" holding a
  white "IDE/ CLI" bar and six small dashed green squares in two rows of three, labelled
  "Containers". A big grey hollow arrow points right. Right: a dashed rectangle labelled **GCP**.
  - Inside GCP, a large blue-grey panel "Compute Instance (Virtual Machine)" holds four green boxes:
    "NGINX Container" (top centre), "API Service Container" (left), "Cheese Front-End App
    Container" (right) and "Vector DB Container" (bottom centre).
  - Wiring (thin grey elbow lines): API Service → NGINX labelled "HTTP 9000"; Front-End → NGINX
    labelled "HTTP 3000"; Vector DB → API Service labelled "HTTP 8000". The arrowheads point *at*
    NGINX and *at* the API service, the reverse of the request direction. A re-draw should pick one
    convention and say which.
  - Below the VM, two stores joined to it by hollow double-headed arrows: "GCS Bucket" (grey, cloud
    icon, "Models") over "HTTPS 443", and "GCE Persistent Volume" (lilac, "Local Models,
    Experiments") over "NFS".
  - Above the GCP box, a screenshot of the running app (dark UI, a chat with a cheese photo) is
    joined to it by a double-headed arrow labelled "HTTP 80".

  Purpose: the whole lecture in one picture. The containers that ran on the laptop end up on one VM
  that users reach on port 80.
- **12 · six principles (hub layout).** The Pulumi logo sits in the centre. Six rounded boxes sit
  around it in a hexagon, with no connecting lines: "Real Programming Languages" (top left),
  "Declarative Infrastructure" (top right), "Multi-Cloud Support" (left), "Component-Based
  Architecture" (right), "State Management & Previews" (bottom left) and "Test-Driven
  Infrastructure" (bottom right). Purpose: a checklist, not a mechanism. Each box is one word or
  two, with no explanation on the slide.
- **14 · "How Pulumi Works".** Two rounded boxes, one above the other, joined by a hollow down
  arrow.
  - Top: "Your Machine / CICD", with four bullets in order: the CLI runs your program; the program
    defines desired state; Pulumi compares desired with current; Pulumi makes API calls to
    providers.
  - Bottom: "Cloud Providers", with three bullets: AWS, Azure, GCP, K8s and others; they receive the
    API calls; they create, update or delete resources.

  Left of the boxes, two short paragraphs restate it. A full-width caption underneath reads
  "PULUMI MANAGES INFRASTRUCTURE THROUGH CLOUD APIs". Purpose: the engine loop. A scene can animate
  the four top bullets as a pipeline (run → desired → diff → calls) and let the arrow carry the
  calls down. "Current" state is named but not shown. The digest's three trees (code, state, cloud)
  fill that gap (digest §3.2).
- **21–24 and 27 · the deployment picture, built up step by step.** Each slide keeps the previous
  one and adds a layer, so a scene can animate it the same way. The fixed frame:
  - **Top left:** a pink box "Developers - Deployment Containers" with an "IDE/ CLI" bar and three
    dashed green "Containers" squares. A hollow down arrow drops from it into GCP.
  - **The GCP outline** is dotted and stepped. On the left it starts low, just under the arrow tip.
    On the right it rises higher, so the area where the VM will appear sits level with the
    developers' box.
  - **Bottom left inside GCP:** a light-blue panel "Google Container Registry (GCR)" with three
    blue bars: "Cheese App Image", "API Service Image" and "Vector DB CLI".

  The build order:
  - **21** ("Build & Push Docker Images to GCR"): only the frame. The developers' arrow lands on the
    registry, and the right half of GCP is empty.
  - **22** ("Create Compute Instance (VM)"): an *empty* blue-grey panel "Compute Instance (Virtual
    Machine)" appears on the right. Below it are "GCS Bucket" ("Models", HTTPS 443) and "GCE
    Persistent Volume" ("Local Models, Leaderboard", NFS), each with a double-headed arrow up to the
    VM.
  - **23** ("Setup Docker Containers in VM"): a grey arrow points from the registry to the VM. Three
    green boxes appear in the VM with port labels above them but no lines between them: "API Service
    Container" (HTTP 9000), "Vector DB Container" (HTTP 8000) and "Cheese App Container" (labelled
    **HTTP 80** here).
  - **24** ("Setup Web Server to expose App"): "NGINX Container" appears at the top of the VM. The
    same wiring as slide 7 appears (API → NGINX "HTTP 9000", Cheese App → NGINX "HTTP 3000", Vector
    DB → API "HTTP 8000"). The app screenshot appears above the GCP outline, joined to it by a
    double arrow "HTTP 80".
  - **27** ("Test the App"): identical to 24. The new title turns the picture into a test: the
    browser at the top is the check.

  Purpose: map each automated step (19) to the part of the system it creates. Port 80 moves from
  the frontend (23) to NGINX (24). That shift is the point of step 6: before the web server, the
  frontend would face users directly; after it, only NGINX does. No container for the vector-DB
  loader is drawn, although its image ("Vector DB CLI") is in the registry.
- **26 · who needs which key.** The full slide-24 picture without the screenshot (the HTTP 80 arrow
  stays). Three red dashed callouts, each with a numbered pink circle and a red file name above it:
  1. On the developers' down arrow, file `deployment.json`: "Need admin access to create VM, SSH
     etc".
  2. Between the registry and the VM, on the image-pull arrow, file `gcp-service.json`: "Need read
     access to GCR".
  3. On the VM ↔ GCS-bucket link (the callout covers the "HTTPS 443" and "GCS Bucket" labels), file
     `gcp-service.json`: "Need read access to models from **class bucket**".

  Purpose: show that the powerful key is used only at the edge where infrastructure is built, and
  the read-only key is used where the running system reads images and models. The PDF's text layer
  also contains a "TCP/IP 5432" label near the API container, hidden behind the VM panel and not
  visible on the slide. It is a leftover; nothing in L20 uses port 5432.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Deployment, Scaling & Automation" | 4 | The roadmap bar that L20–L23 fill. The README's title is "Cheese App - Deployment & Scaling". |
| "deploy", "local computer", "server" | 5, 7 | — |
| "Deployment: Goal" | 7 | — |
| "Local Computer" (7) → "Developers - Deployment Containers" (21–27), "IDE/ CLI", "Containers" | 7, 21–27 | The tutorial's deployment container `cheese-app-deployment`, started with `sh docker-shell.sh` from `src/deployment` (digest §4 B3). |
| "Compute Instance (Virtual Machine)", "Compute Engine VM", "VM Instance" | 7, 19, 22–28 | An `n2d-standard-2` Ubuntu 22.04 VM created by `create_instance.py`, plus a VPC and three firewall rules (80/443/22) that the slides do not draw (digest §4 B10). |
| "NGINX Container", "web server", "reverse proxy" | 7, 8, 19, 24, 28 | The container `nginx` (`nginx:stable`) on ports 80/443 with `nginx.conf` routing `/api-service/` → `api-service:9000` and `/` → `frontend:3000` (digest §3.8). |
| "API Service Container" / "API Service Image" | 7, 21–27 | Container `api-service`, image `cheese-app-api-service:<timestamp>`. |
| "Cheese Front-End App Container" (7), "Cheese App Container" / "Cheese App Image" (21–27), "Frontend" (8, 28) | 7, 8, 21–28 | Container `frontend`, image `cheese-app-frontend-react`. The slides never call it React or Next.js. |
| "Vector DB Container", "Vector DB CLI" | 7, 21–27 | Container `vector-db` (`chromadb/chroma:latest`), plus the one-shot loader container `vector-db-loader` built from `cheese-app-vector-db-cli`. The slides draw no loader container. |
| "GCS Bucket" / "Models", "class bucket" | 7, 22–27, 26 | In v3 the API's CNN is downloaded from a GitHub release, not from a bucket (`api/utils/llm_cnn_utils.py:122-124`; the code comment says it should come from a GCS bucket). The only bucket the tutorial uses is the Pulumi **state** bucket `<proj>-pulumi-state-bucket`, which the slides never show. |
| "GCE Persistent Volume", "Local Models, Experiments" (7) / "Local Models, Leaderboard" (22–27), "NFS" | 7, 22–27 | The tutorial attaches a 50 GB `pd-standard` disk as a block device, mounted at `/mnt/disk-1` (digest §4 B10). It is not NFS. |
| "Google Container Registry (GCR)" vs "GAR" | 19, 20 vs 21, 25, 26, 28 | The code pushes to **Artifact Registry** (`us-docker.pkg.dev/<proj>/cheese-app-repository`), and the README heading says "Google Artifact Registry". GCR is the retired product name that the slides and parts of the README still use (digest §10 erratum 3). |
| "Docker Hub", "dedicated network" | 8 | Manual route only. The network is `cheese-app-network` (manual) and `appnetwork` (Pulumi). |
| "Deployment Automation", "infrastructure automation", "infrastructure as code", "Everything is code" | 9, 10, 17 | Same idea as the digest's IaC (digest §3.1). |
| "real programming languages", "familiar constructs", "not YAML or DSL (Domain Specific Language)" | 10, 11, 17 | The tutorial's programs are Python (`runtime: python`, `toolchain: uv`). |
| The six principles: "Real Programming Languages", "Declarative Infrastructure", "Component-Based Architecture", "Multi-Cloud Support", "State Management & Previews", "Test-Driven Infrastructure" | 12 | The tutorial uses no component resources and no tests. Its "multi-cloud" is GCP plus the `command` and `docker` providers. |
| "Pulumi CLI Commands", "Programs", "Stacks", "Resources", "State", "Providers" | 13 | The tutorial also uses projects (`Pulumi.yaml`), config namespaces, a self-managed GCS state backend, Outputs and `StackReference`. None of these appear on the slides (digest §3.3–3.5). |
| "desired state", "current", "Cloud Providers", "Your Machine / CICD" | 14 | In the tutorial, "your machine" is the deployment container. CI/CD comes in L21/L23. |
| "stack (environment)", `<project>-<environment>`, `cheese-app-dev` | 15, 16, 18 | The tutorial does not follow this naming. Its stacks are called `dev`, inside two projects `deploy-images` and `deploy-single-vm`, and one stack refers to the other as `organization/deploy-images/dev`. |
| "Provision the server", "Provision Instance" | 19, 28 | `provision_instance.py`: nine chained remote commands (format and mount the disk, apt, Docker CE, docker group). |
| "service accounts" `deployment` / `gcp-service`; key files `deployment.json` / `gcp-service.json`; "secret keys" | 20, 25, 26 | Same names and files as the README. The README's roles: `deployment` = Compute Admin, Compute OS Login, Artifact Registry Administrator, Kubernetes Engine Admin, Service Account User, Storage Admin. `gcp-service` = Storage Object Viewer, Vertex AI Administrator, Artifact Registry Reader. |
| "group GCP project" | 25 | Course-project wording: the deployment targets the group's own project, not the instructor's `ac215-project`, which the committed files hardcode (digest §6 gotcha 5). |

The slides never use these tutorial words: Artifact Registry repository creation, VPC, firewall,
network tags, SSH key, OS Login, `sa_…` user, `pulumi login`, state bucket, `pulumi stack init`,
`pulumi config set`, `Pulumi.yaml` / `Pulumi.dev.yaml`, Output / `apply`, `StackReference`,
timestamp tags, Docker-over-SSH, `remote.Command`, `retain_on_delete`, `ROOT_PATH`, `/status`.
A video that follows the slides has to introduce them itself, from the digest.

## Commands and code on the slides

The slides contain no shell commands apart from the Pulumi CLI list. There are no `docker`,
`gcloud` or `ssh` commands.

- 15 (each with a one-line description on the slide):
  - `pulumi new <template>`: create a project from a template
  - `pulumi up`: preview and deploy changes
  - `pulumi preview`: preview without deploying
  - `pulumi destroy`: tear down every resource in the stack
  - `pulumi stack`: manage stacks (environments)
  - `pulumi config`: manage configuration values
  - `pulumi refresh`: refresh the state to match the actual infrastructure
- 16: `pulumi up [options]`, with the flags `--yes`, `--stack <name>` and `--refresh`. The tutorial
  combines all three as `pulumi up --stack dev --refresh -y`.
- 17 (Python, in a dotted panel):
  - `# Example: Create a GCS bucket in Google Cloud`
  - `import pulumi`
  - `import pulumi_gcp as gcp`
  - `# Create a GCS bucket`
  - `bucket = gcp.storage.Bucket("my-bucket",`
  - `location="US",`
  - `website=gcp.storage.BucketWebsiteArgs(`
  - `main_page_suffix="index.html",`
  - `)` and `)` to close

  The snippet exports nothing (`pulumi.export`), and the tutorial never creates a bucket this way.
  Its programs build images (`docker_build.Image`) and create a VM (`gcp.compute.Instance`). The
  closest tutorial excerpts are in digest §5, excerpts 4 and 6.
- 18: `<project>-<environment>`, `cheese-app-dev`, `cheese-app-prod`.
- 20, 26: key file names `deployment.json`, `gcp-service.json`.
- Port and protocol labels in the diagrams (7, 22–27): `HTTP 80`, `HTTP 3000`, `HTTP 9000`,
  `HTTP 8000`, `HTTPS 443`, `NFS`.
- 28: the URL `https://github.com/dlops-io/cheese-app-v3?tab=readme-ov-file#deployment-to-gcp-single-vm-instance`.

## What the lecture stresses

- **Automate because manual steps don't scale.** The lecture names the manual deployment's problem
  as the number of steps to keep track of (9). The answer is code that can live in GitHub and be
  shared (10).
- **Real code, not configuration files.** Pulumi's point of difference is general-purpose languages
  with functions, classes, loops and conditionals, rather than YAML or a DSL (10, 11, 12, 17).
- **Declarative: say what, not how.** You describe the desired infrastructure, and Pulumi works out
  the steps by comparing it with the current state (12, 14, 17).
- **Everything goes through cloud APIs.** The one all-caps line in the deck: Pulumi manages
  infrastructure through cloud APIs (14).
- **Preview before you apply.** `pulumi up` shows the plan and asks for confirmation. `--yes` skips
  that safety step, and `pulumi preview` shows the plan without applying it (12, 15, 16). The
  tutorial always runs `preview` first and then `up … -y`.
- **Keep environments apart with stacks,** each with its own state and config (18).
- **Least privilege with two service accounts.** An admin account builds the infrastructure, and a
  read-only account serves the running app. "your" is highlighted in red on 25: each group uses its
  own project (20, 25, 26). The digest adds a caveat. The VM itself runs as the powerful
  `deployment` account, and the image pull goes through the Docker provider with the deployment
  container's credentials, so the clean split on 26 is the design intent rather than what the code
  enforces (digest §3.7, §6 gotcha 19).
- **One public door.** Only NGINX faces the browser, on port 80. The other ports stay inside the VM
  (7, 24).
- **Clean up.** A slide of its own: "DON'T FORGET TO DELETE" (29). The VM and disks cost money
  until `pulumi destroy`, and the registry images survive even that (digest §2, §4 B13).
- **Inconsistencies to watch for when re-drawing:**
  - Registry name: "GAR" on 19 and 20, "GCR" on 21, 25, 26 and 28. The code uses Artifact
    Registry.
  - Frontend port: "HTTP 80" on 23, "HTTP 3000" on 7, 24, 26 and 27. The tutorial's frontend
    listens on 3000. Use 3000 and keep 80 for NGINX.
  - Persistent-volume label: "Local Models, Experiments" on 7, "Local Models, Leaderboard" on 22–27.
    It is drawn as NFS, but the tutorial attaches a block disk at `/mnt/disk-1`.
  - The bucket of models (22–27) and the "class bucket" callout (26) do not match v3's code, which
    downloads its model from GitHub. The bucket that actually matters, the Pulumi state bucket, is
    missing from the slides.
  - The manual steps (8) mention only the API service and the frontend. The README also runs the
    vector DB, its loader and NGINX (digest §10 erratum 14).
  - 11 has a doubled word ("Programs programs run …").
  - 26 carries a hidden "TCP/IP 5432" label in its text layer, which the slide does not show.
  - Step 4 of 19 (provisioning) has no diagram, and the slides skip SSH / OS Login setup (README
    lines 282–316). Neither the VPC nor the firewall rules are drawn.

## Pointers

- 8: "Cheese App - Deployment to GCP (Manual)" links to
  `https://github.com/dlops-io/cheese-app-v3?tab=readme-ov-file#cheese-app---deployment--scaling`.
  That is the README's top heading ("Cheese App - Deployment & Scaling"). The manual section
  ("Deployment to GCP (Manual)", README line 4, anchor `#deployment-to-gcp-manual`) starts right
  under it. A QR code sits beside the link. It was not decoded here and is presumably the same
  link.
- 28: "Cheese App - Deployment to GCP (Pulumi)" links to
  `https://github.com/dlops-io/cheese-app-v3?tab=readme-ov-file#deployment-to-gcp-single-vm-instance`
  (README line 225, "Deployment to GCP (Single VM Instance)"). The visible URL text and the link
  agree. A QR code sits beside it (not decoded).
- Slide → tutorial mapping, for scene planning. Step 1 of 19 (and 20) is the deployment container
  and README lines 229–316. Step 2 is `deploy_images/`. Steps 3–6 are, in order,
  `create_instance.py`, `provision_instance.py`, `setup_containers.py` and `setup_webserver.py` in
  `deploy_single_vm/` (digest §4 B9–B10). The order on the slides matches the code's four phases
  exactly.
- 4: the roadmap. Deployment, scaling and automation continue in L21 (CI/CD), L22 (Kubernetes) and
  L23. "Scaling" and Kubernetes are not covered in this deck, although the same README continues
  with "Deployment with Scaling using Kubernetes".
- 29: the clean-up reminder; the tutorial's step is `pulumi destroy --stack dev --refresh -y` in
  `deploy_single_vm` (README line 389).
- The slides list no readings, demos, homework or milestone notes beyond these.

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only `SLIDES.md` and `digest.md`: there is no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the ten planned chapters in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L20-deployment-pulumi.md`) and every slide: the extracted text and all four contact sheets, re-read for this section. With no captures yet, "what the tutorial does today" means `cheese-app-v3` `main` @ `3ecef56`. For the conflicts I re-read these in that clone on 2026-10-16: the VM's service account and scopes (`src/deployment/deploy_single_vm/create_instance.py:135-145`, `deploy_single_vm/Pulumi.dev.yaml:5`, README line 355); the key upload and the Docker provider's registry auth (`setup_containers.py:44-63`, `:79-98`); the five containers and their ports (`setup_containers.py:110-247`, `setup_webserver.py:71-102`, `nginx.conf:26`); what lives on the data disk (`setup_containers.py:65-76`, `:149-153`, `:228-229`, `src/api-service/api/utils/llm_cnn_utils.py:34` and `:122-124`, `chat_utils.py:9`); and the README's roles and Pulumi commands (lines 241–255, 332–389). When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 1, 5, 6 and 7 against them (the registry host in the `pulumi up` output; `df` and `sudo docker container ls` on the VM). If they disagree, the captures win.

**No README image is a lecture diagram.** The cheese-app-v3 README has no images, so slides 7 and 21–27 are the only drawings of the target system. The digest's §1 diagram shows the same system from the tutorial's side, including what the slides leave out: the state bucket, the VPC and firewall, and the SSH paths.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| 1 | The 20-command problem (≈3 min) | 4–5, 7–11 | Same concept, and the tutorial applies it. Part A is slide 8's four manual stages, and the chapter's thesis is slide 9's "too many steps to keep track of". Slides 10–11 (infrastructure as code, real languages, kept in GitHub) are the answer the chapter ends on. Slide 7's goal picture is not in the plan (Gap 4). Conflict 7 (the container count). |
| 2 | The control room (≈3 min) | 14 (the "Your Machine / CICD" box), 19 (step 1), 20, 21–27 (the "Developers - Deployment Containers" box), 25 | The tutorial applies slide 20: enable the APIs, create two service accounts, give the container their keys, set the project. The mounts, Docker-out-of-Docker and the state-bucket login are tutorial-only. What the two keys are for (25–26) has no beat in the plan (Gap 1). |
| 3 | Desired state vs reality (≈4 min) | 12, 14, 16, 17 | Same concept. Slide 14's four bullets (run the program → desired state → compare with current → API calls to providers) are the plan's engine loop, and the plan's three trees draw the "current" state that slide 14 names but does not show. Conflict 9 qualifies the slide's "through cloud APIs". |
| 4 | Projects, stacks, config, state, secrets (≈3 min) | 13, 15 (`pulumi stack`, `pulumi config`), 18 | Same concept for stacks and config. Projects (`Pulumi.yaml`), the self-managed GCS backend, Outputs and the empty passphrase are tutorial-only. Conflict 8 (stack names). |
| 5 | Act I: images with timestamps (≈3 min) | 19 (step 2), 21, 28 ("Build & Push Images") | The tutorial applies it: `deploy_images` is step 2 and slide 21's registry panel. Timestamp tags, `retain_on_delete` and `StackReference` are tutorial-only. Conflict 1. |
| 6 | Act II: the VM and its fences (≈3 min) | 19 (step 3), 22, 7 | The tutorial applies it: `create_instance.py` is step 3, slide 22's empty VM with its disk. The VPC, the firewall rules, network tags and the IP as an Output are tutorial-only; the slides draw no network. Conflicts 4 and 5. |
| 7 | Act III: provisioning with commands (≈3 min) | 19 (step 4), 28 ("Provision Instance") | The tutorial applies a step that the slides name but never draw. `remote.Command`, idempotency and the `blkid` guard are tutorial-only. Conflict 9. |
| 8 | Act IV: containers over SSH and the request's journey (≈4 min) | 19 (steps 5–6), 23–24, 27, 7, 8 (stage 4, the reverse proxy), 25–26 | Same concept, and the tutorial applies it: `setup_containers.py` is slide 23, `setup_webserver.py` is slide 24, and the browser on port 80 is slide 27's test. Docker-over-SSH, `appnetwork` DNS, prefix stripping and `ROOT_PATH` are tutorial-only. Conflicts 2, 3, 6 and 7. |
| 9 | Change, refresh, destroy (≈3 min) | 15 (`destroy`, `refresh`), 16 (`--refresh`), 29 | Same concept. Checksum triggers, drift and `retain_on_delete` are tutorial-only. Slide 29's reminder is the chapter's closing card. |
| 10 | Recap and bridge to Kubernetes (≈1.5 min) | 4, 12, 19 | Slide 19's six steps are the lecture's own summary and can carry the content recap (Gap 2). The bridge to GKE fits slide 4's "Scaling", but the deck does not cover Kubernetes: tutorial-only (L22). |
| — | not in the plan | 1–3, 6, 30; parts of 11–12 | Lecture-only: title, outline, section dividers, the close. Pulumi's history (11) and three of slide 12's six principles (component-based architecture, multi-cloud support, test-driven infrastructure) have no tutorial counterpart (Gap 7). |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Manual deployment works but has too many steps, so automate it | §1 ↔ 8, 9 | Yes. The plan's reasons (it cannot be repeated, reviewed or undone) are sharper than "keeping track of steps", and slide 29's reminder backs the "undone". |
| 2 | Infrastructure as code, in a real language, kept in git | §1, §3 ↔ 10, 11, 17 | Yes. The programs are Python (`runtime: python`, `toolchain: uv`). The course's own Ansible playbooks (digest §3.1, §7) make slide 11's "not YAML or DSL" concrete. |
| 3 | Declarative: describe what should exist; Pulumi works out how | §3 ↔ 12, 17 | Yes. The plan goes further: constructors only register resources, and the engine decides the order. It holds for steps 2–3 and 5–6; step 4 is shell scripts (Conflict 9). |
| 4 | The engine loop: run the program, diff desired against current, call the providers | §3 ↔ 14 | Yes, closely. Slide 14's "compares desired vs. current" is the plan's diff, and "makes API calls to providers" is its provider calls. The plan adds state as the third tree. |
| 5 | `pulumi up` previews, asks, then applies; `preview` only plans; `--refresh` re-reads reality; `--stack` picks the stack | §3, §5, §9 ↔ 15, 16 | Yes. The README always runs `preview` and then `up … -y`, so the confirmation that slide 16 describes never appears on screen (Gap 3). |
| 6 | A stack is one isolated copy with its own state and config | §4 ↔ 18 | Partly. The plan's class-and-instance analogy fits, but the plan never says why you would want a second stack, and that is the lecture's whole point: the same program for dev, staging and production (Gap 6). The names differ (Conflict 8). |
| 7 | Pulumi runs on one machine and talks out to the cloud | §2 ↔ 11, 14, 21–27 | Yes. The plan's control room is slide 14's "Your Machine / CICD" box and the slides' "Developers - Deployment Containers". The CI/CD runner arrives in L23. |
| 8 | The automated deployment is a fixed sequence: images, VM, provisioning, containers, web server | §5–§8 ↔ 19, 21–24, 28 | Yes, one to one. Acts I–IV follow steps 2–6 in the order of the code's phases (`deploy_single_vm/__main__.py:14-26`). The plan just never names the steps (Gap 2). |
| 9 | Images go to a registry first, and the VM pulls them from there | §5, §8 ↔ 21, 23 (the registry → VM arrow) | Yes on the flow. The registry's name differs (Conflict 1), and so does the identity that pulls (Conflict 2). |
| 10 | The VM gets a separate persistent disk | §6 ↔ 22 | Yes on "a disk beside the VM". What kind of disk, and what is on it, differ (Conflict 5). |
| 11 | The containers share a dedicated Docker network | §8 ↔ 8 (stage 3) | Yes: `cheese-app-network` by hand, `appnetwork` in Pulumi. |
| 12 | One public door: only NGINX faces the browser, on port 80, and it routes to the API and the frontend; the test is a browser on port 80 | §8 ↔ 7, 8 (stage 4), 24, 27 | Yes. The plan adds the firewall gates and the prefix scissors, and its `curl …/api-service/status` is the precise version of slide 27's test. The slides' arrows run the other way (see "Not counted"). |
| 13 | Clean up afterwards | §9 ↔ 15 (`destroy`), 29 | Yes. The lecture's reminder covers more than the README, which never deletes the Part A VM. The plan adds what survives `destroy`. |
| 14 | Two service accounts with different powers | §2 (only `gcloud auth list`), recap question 3 ↔ 20, 25–26 | Partly. The digest explains identity (§3.7), but the plan gives it no beat (Gap 1), and the code blurs the lecture's split (Conflicts 2 and 3). |
| 15 | Where L20 sits: the deployment phase begins, scaling comes next | §10 ↔ 4 | Yes. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Two keys, two jobs (slides 20, 25–26).** The student creates both accounts in B2, drops both keys into `secrets/`, and in B10 has to type an email into `security:gcp_service_account_email`. The lecture gives the reason for the split: `deployment` builds the infrastructure and needs admin rights on the group's own project, while `gcp-service` is what the running app uses to read images and call Vertex AI. Slide 26 shows where each key is needed. The plan only asks about it in a recap question. **Carry it in** §2, as slide 25's two-row card when the keys enter the control room, and in §8, as slide 26's three callouts over the finished picture, amended by Conflicts 2 and 3.
2. **The six steps as the spine, and the picture that grows (slides 19, 21–24, 27–28).** Slide 19's list maps one to one onto the files: step 1 is `docker-shell.sh`, step 2 is `deploy_images/`, and steps 3–6 are `create_instance.py`, `provision_instance.py`, `setup_containers.py` and `setup_webserver.py`. Slides 21–24 grow one picture a step at a time. With this map a student can tell from the `pulumi up` output which step is running and which file to open when it fails. **Carry it in** §2 (introduce the six-step tracker and tick step 1), §5–§8 (each Act opens on its slide's state of the picture and ticks its step), and §10 (replay as the content recap).
3. **Preview, confirm, apply, and what `-y` skips (slides 15–16).** Students copy `pulumi up --stack dev --refresh -y` without knowing that plain `pulumi up` would show the plan and ask first. Reading the plan matters here, because a new Ubuntu image can turn the next `up` into a VM replacement (digest §6 gotcha 20, §4 B12). **Carry it in** §3: decode the README's command flag by flag over slide 16's three flags. Repeat one line in §9 before the redeploy. Slide 15's seven-command card goes in §4.
4. **The goal picture (slides 5, 7).** Slide 5's two lines state the problem (everything runs on your computer; users need a server), and slide 7 is the destination: the laptop's containers on one VM in GCP, reached on port 80. The digest's §1 diagram is too dense for a first view. **Carry it in** §1, right after the hook, as the target the twenty commands build by hand.
5. **A minimal program before the real ones (slide 17).** Slide 17's six-line program shows the shape of every resource (a constructor, a logical name, arguments) without the repo's noise. **Carry it in** §3 as the first code panel, then cut to the repo's `gcp.compute.Firewall` (digest §5 excerpt 6), which has the same shape. Say once that the bucket example is not part of the tutorial.
6. **Stacks are for environments (slide 18).** The same program can run as dev, staging and production, each with its own state and config values. The tutorial only ever has `dev`, so the reason for stacks never shows. **Carry it in** §4, as one sentence and a card of three stacks under one program.
7. **Pulumi in one breath, and the six principles as a scorecard (slides 10–12).** Founded in 2017, programs in Python, TypeScript, Go, C# or Java, run from a workstation or a CI runner. Of the six principles, this tutorial uses real languages, declarative resources, and state with previews. It does not use components, multiple clouds or tests. **Carry it in** §1 (one sentence) and §10 (the scorecard, with ticks).
8. **Where L20 sits (slide 4).** The red box has moved to "Deployment, Scaling & Automation", the bar that the remaining lectures fill. **Carry it in** §1 (ten seconds) and §10 (the bridge to L21–L23).

### 4. Conflicts

No captures exist yet, so "today" is the repo at `3ecef56`, re-read as listed under Basis. The captures will decide once they are made.

| # | Slides say | Tutorial today | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **The registry is "Google Container Registry (GCR)"** (slides 21, 25, 26, 28); slides 19–20 say "GAR". The registry is simply there. | The code pushes to **Artifact Registry**, `us-docker.pkg.dev/<proj>/cheese-app-repository/...` (`deploy_images/__main__.py:14-15`), and the README's heading says "Google Artifact Registry". Container Registry is retired. Nothing creates the repository: neither the slides, the README nor the code (digest §10 errata 1 and 3). | Artifact Registry | "Slide 19 already says GAR; the diagram still carries the older name, GCR. Same box, today's name: Artifact Registry. One thing the picture assumes: the repository must exist, so you create it once." Label the re-drawn panel "Artifact Registry" and add the `gcloud artifacts repositories create` beat. |
| 2 | **`gcp-service` reads the images on the VM** (slide 20: "To read containers from GAR in VM"; slide 25; slide 26, callout 2, with `gcp-service.json` on the registry → VM arrow). | Pulumi's Docker provider pulls on the VM's daemon, but with registry credentials resolved from the deployment container's Docker config (credHelpers → gcloud), that is, as `deployment` (`setup_containers.py:92-96`, `docker_config.json`, `docker-shell.sh:39`; digest §3.7). The `gcp-service` login that `setup_containers.py:59-60` performs on the VM only serves a manual `docker pull` by the SSH user without `sudo`. | The code | "The lecture's rule is the right one: the machine that runs the app should only be able to read images. In this repo, Pulumi's own pulls borrow your deployment key from the laptop. The `gcp-service` login on the VM is there for a pull you type by hand." Draw callout 2 with a small amendment arrow from the laptop's key. |
| 3 | **The VM side holds only the narrow key** (slides 25–26). Slide 25 says `gcp-service` is for Vertex AI inference, but slide 26 draws no Vertex AI link. | The VM's attached account is whatever `security:gcp_service_account_email` says, and the README sets it to `deployment@…` (README line 355, `Pulumi.dev.yaml:5`, `create_instance.py:135-145`). Its scopes limit the VM's own token to read-only storage plus logging, monitoring and tracing. The `gcp-service` key is uploaded to `/srv/secrets` and mounted into `api-service` and the loader for Gemini and the embeddings (`setup_containers.py:44-63`, `:220`). The README gives `gcp-service` "Vertex AI Administrator", more than the slide's "to perform inference". | The code | "The config key is named for `gcp-service`, but the README fills in the deployment account, so the VM itself carries the powerful identity, held back only by its scopes. The containers use the narrow key for Vertex AI: that is the arrow slide 26 leaves out." Add a PINK api-service → Vertex AI arrow labelled `gcp-service.json`. A candidate exercise is to try the narrower account in that config key; it is untested here. |
| 4 | **The VM reads models from a GCS bucket** over HTTPS 443 (slides 7, 22–27). Slide 26's callout 3 calls it the "class bucket". | Nothing on the VM reads a bucket. The API downloads its CNN from a GitHub release into `/persistent/experiments` (`llm_cnn_utils.py:34`, `:122-124`; the code's own comment says it should come from your bucket). The loader downloads pre-computed embeddings from a GitHub release (`src/vector-db/cli.py:487`). `GCS_BUCKET_NAME=cheese-app-models` is passed but never read (`setup_containers.py:222`). The one bucket the tutorial uses is the Pulumi state bucket, which the laptop uses and no slide draws. | The code | "The bucket is where models belong once training feeds deployment, and the code's comment agrees. In v3 the model comes from a GitHub release, so our picture greys the box out and adds the bucket the tutorial really uses: Pulumi's memory, next to your laptop." |
| 5 | **A "GCE Persistent Volume" over NFS**, labelled "Local Models, Experiments" (slide 7) or "Local Models, Leaderboard" (slides 22–27). | A 50 GB `pd-standard` block disk attached to the VM, formatted ext4 and mounted at `/mnt/disk-1` (`create_instance.py:92-97`, `provision_instance.py:24-57`). `api-service` sees `/mnt/disk-1/persistent` as `/persistent` (the downloaded model in `/persistent/experiments`, plus chat history), and ChromaDB gets `/mnt/disk-1/chromadb` (`setup_containers.py:65-76`, `:149-153`, `:228-229`). There is no NFS and no leaderboard. | The code; slide 7's label is accurate | "It is a second disk plugged into the VM, not a network share. Slide 7's 'Local Models, Experiments' is literally the folder `/persistent/experiments`." Draw a disk with a cable, not a network link. Keep the ChromaDB path caveat to the guide (digest §6 gotcha 23). |
| 6 | **The frontend is on HTTP 80** (slide 23). Slides 7, 24, 26 and 27 say HTTP 3000. | The frontend publishes 3000 (`setup_containers.py:114-119`). nginx publishes 80 and 443 (`setup_webserver.py:78-83`) and listens on 80 (`nginx.conf:26`), and the firewall opens 80, 443 and 22. | 3000 for the frontend; 80 belongs to nginx | Label the frontend 3000 throughout. To keep slide 23 → 24's story, tell it this way: "Without nginx, a visitor would need `:3000` for the page and `:9000` for the API, and the firewall lets neither in." |
| 7 | **The containers** are the API and the frontend (slide 8, manual), or the API, frontend and NGINX (slide 28). Slides 7 and 23–24 draw four long-running containers. The registry holds a "Vector DB CLI" image, but no loader container is drawn. | Both routes run five containers: `frontend`, `vector-db` (`chromadb/chroma:latest`), a one-shot `vector-db-loader` (`rm=True`), `api-service` and `nginx` (`setup_containers.py:110-247`, `setup_webserver.py:71-102`; README Part A runs the same five by hand, digest §10 erratum 14). | Five | "The lecture lists the containers you will talk to. Two more do quiet work: the vector DB, which the API needs at start-up, and a loader that fills it and leaves." Animate the loader as a dashed TEAL box that appears, fills the vector DB and vanishes. |
| 8 | **Stack names** follow `<project>-<environment>`, such as `cheese-app-dev` (slide 18). | Two Pulumi projects, `deploy-images` and `deploy-single-vm`, each with a stack called `dev`. Their full names are `organization/<project>/dev`, and the VM program reads the images stack as `organization/deploy-images/dev` (`setup_containers.py:27`). | The tutorial's names, which the code depends on | "Pulumi already files each stack under its project, so `dev` inside `deploy-images` is unambiguous. Its full name is what StackReference uses. The slide's pattern is a naming habit; don't rename these stacks, or the reference breaks." |
| 9 | **Pulumi manages infrastructure through cloud APIs.** Providers are AWS, Azure, GCP, K8s, and they create, update or delete resources; programs are declarative (slides 12, 14, 17). | That holds for steps 2–3 (the docker-build and gcp providers). Step 4 runs shell scripts over SSH (`remote.Command`), which have only a `create` script and no update or delete. Pulumi records that a script ran, not what it changed. Steps 5–6 drive the VM's Docker daemon over SSH (the docker provider), so the containers stay declarative (digest §3.6). | Both: the banner is true for cloud resources; the inside of the VM is reached through SSH | "Pulumi talks to anything with an API. For the inside of the VM, the API is SSH and the Docker daemon. Containers can still be diffed; shell scripts are an escape hatch Pulumi cannot look into, which is why they must be safe to re-run." Use this as the bridge into §7. |

Not counted as conflicts:
- The arrowheads on slides 7, 24, 26 and 27 point at NGINX and at the API service, against the direction of a request. Draw requests going browser → nginx → services → vector DB and say once which way the arrows go.
- Slide 26's "TCP/IP 5432" exists only in the text layer and is not visible.
- Slide 8's link lands on the README's top heading, just above the manual section.
- Slide 16's `--yes` is the README's `-y`.
- `pulumi new` (slide 15) is never run: both projects are committed with their `Pulumi.yaml`.
- Slide 17's bucket program is a generic example, not tutorial code.
- nginx publishes 443 and the firewall opens it, but `nginx.conf` has no TLS listener. This is tutorial-only; the slides only draw HTTP 80.
- The deck says Lecture 20, while the course schedule labels the entry Lecture 19 (study guide, versions note). The series follows the deck.

### 5. Proposals for the BRIEF and script authors

**General**
- **One master diagram.** Re-draw slides 7 and 21–27 in the series style (laptop GREY, cloud and VM BLUE, containers TEAL, request routes PINK, cost GOLD) and grow it exactly as the deck does: 21 (registry) → 22 (empty VM and disk) → 23 (containers) → 24 (nginx and the browser) → 27 (test). Use today's labels: Artifact Registry (Conflict 1), frontend `:3000` (Conflict 6), a disk at `/mnt/disk-1` (Conflict 5), the models bucket greyed and the Pulumi state bucket beside the laptop (Conflict 4), the loader as a dashed box (Conflict 7), and an api-service → Vertex AI arrow (Conflict 3). Draw arrows in the request direction. Then add the tutorial-only layers the slides lack: the VPC outline with three firewall gates (80, 443, 22) in §6, and the SSH tunnel in §7–§8.
- **Tag each chapter with one GREY `lecture_ref(20, "a–b")`**, using the ranges below. The slides themselves never appear on screen.
- **A six-step tracker** (Gap 2) sits in a corner from §2 to §8, beside the README tracker. Each step shows its file name and ticks as its Act ends.
- **Two parts, cut where the deck cuts.** Part 1 is §1–§4 (manual deployment and Pulumi the tool, slides 4–18, about 13 min). Part 2 is §5–§10 (the six steps, slides 19–29, about 17.5 min).
- **Length.** The plan is about 30.5 minutes, inside the 25–35 target. Bring lecture material in by replacing, not adding. Slide 7 replaces part of §1's scrolling terminal. The identity card in §2 replaces the plugin-cache mount, which can go. Slide 26 in §8 fits if the Kubernetes side panel there shrinks to one line, since §10 already bridges to L22.
- **Pause-and-ponder candidates from the lecture**, alongside the plan's three: at slide 26 in §8, "which key would you hand to the VM, and why not the other?"; at slide 16 in §3, "what does `-y` skip, and when would you not want to skip it?"; at slide 18 in §4, "what would you change to deploy a second, production copy of this app?"

**Per chapter**
- **§1 · Lecture 20 · slides 4–11.** After the hook, show slide 4's roadmap for ten seconds, with the red box on "Deployment, Scaling & Automation". Then slide 5's problem in one line and slide 7's goal picture, re-drawn (Gap 4). Run the Part A montage under slide 8's four stage names (Push to Docker Hub, Setup VM Environment, Deploy Containers, Configure Web Server), with the vector DB and loader added (Conflict 7). Close on slide 9's sentence, then slides 10–11 in one breath: infrastructure as code, in Python, kept in GitHub, not YAML or a DSL. The course's old Ansible playbooks were YAML.
- **§2 · Lecture 20 · slides 19–20, 25.** Name the container with slide 14's "Your Machine / CICD" and slide 20's checklist. Show slide 25 as a card: `deployment` builds everything (admin on *your* group's project), and `gcp-service` is what the running app uses. Say "your" with the slide's emphasis: the group's project, not `ac215-project`. Then add the setup beats the slides skip: the Artifact Registry repository, and the SSH key with OS Login (`sa_…`). End with the six-step tracker and step 1 ticked.
- **§3 · Lecture 20 · slides 12–17.** Open on slide 17's minimal program, then cut to the repo's firewall resource (Gap 5). Animate slide 14's four bullets as a pipeline that feeds the plan's three trees, captioned with slide 14's banner. Then decode `pulumi up --stack dev --refresh -y` over slide 16's three flags and say what `-y` skips (Gap 3). Keep pause-and-ponder 1.
- **§4 · Lecture 20 · slides 13, 15, 18.** Show slide 15's seven commands as a card, lit as the tutorial uses them (`stack`, `config`, `preview`, `up`, `destroy`, and `refresh` as the `--refresh` flag), with `new` greyed. Slide 18: three stack cards (dev, staging, prod) under one program, each with its own state and config (Gap 6), then Conflict 8's line on names. After that come the tutorial-only parts: projects, the state bucket, the passphrase.
- **§5 · Lecture 20 · slides 19, 21.** Open on slide 21's frame: the developers' box drops into the registry, and the VM half is empty. Label the registry "Artifact Registry" once with "(GCR on the slides)" (Conflict 1). Tick step 2.
- **§6 · Lecture 20 · slides 19, 22.** Slide 22's empty VM appears with its disk drawn as a disk (Conflict 5) and the models bucket greyed (Conflict 4). Then the tutorial-only layer: VPC, gates, and the IP envelope. Tick step 3.
- **§7 · Lecture 20 · slides 14, 19.** Say that this is the one step the lecture names but does not draw, because it happens inside the VM. Bring back slide 14's banner with a footnote, "… and SSH" (Conflict 9), then the dominoes and pause-and-ponder 2. Tick step 4.
- **§8 · Lecture 20 · slides 23–27.** At slide 23's state, three containers appear (frontend labelled 3000), plus the dashed loader (Conflict 7). At slide 24, nginx appears and port 80 moves to it; then the request's journey. Then slide 26's three callouts over the finished picture, with the amendments for Conflicts 2 and 3 and the Vertex AI arrow (Gap 1). End on slide 27's title, "Test the App": the browser, then `curl …/api-service/status`. Tick steps 5 and 6.
- **§9 · Lecture 20 · slides 15–16, 29.** Use slide 15's `destroy` and `refresh` lines as captions. Repeat the `-y` warning before the redeploy (Gap 3). Show slide 29's message as a GOLD "Don't forget to delete" card just before `pulumi destroy`, without the slide's image, then list what survives: the registry images, the state bucket and the Part A VM.
- **§10 · Lecture 20 · slides 4, 12, 19.** For the content recap, replay slide 19's six steps with the artefact under each: `docker-shell.sh`, `deploy_images`, `create_instance.py`, `provision_instance.py`, `setup_containers.py`, `setup_webserver.py`. Then slide 12's principles as a ticked scorecard (Gap 7). Bridge on slide 4's bar: "Automation" is L21 and L23, "Scaling" is L22.
- **Recap questions.** Keep the plan's six. Add: "What does `pulumi up` do before it changes anything, and what does `-y` skip?" (slides 15–16). Add: "Which of the six steps can Pulumi inspect afterwards, and which does it only remember running?" (slides 14 and 19, Conflict 9). Add: "Why might you keep two stacks of the same program?" (slide 18).

**Terms**
- Use the lecture's words: *deploy*, *server*, *infrastructure as code*, *infrastructure automation*, *real programming languages*, *declarative*, *desired state* / *current state*, *Pulumi CLI*, *program*, *stack*, *resource*, *state*, *provider*, *preview*, *confirmation*, *Compute Instance (VM)*, *web server* / *reverse proxy*, *service account*, `deployment` / `gcp-service`, *deployment container* (for the slides' "Developers - Deployment Containers").
- Add the repo's words where the lecture stops: *project* (`Pulumi.yaml`), *config namespace*, *state backend* / *state bucket*, *Output* and `apply`, *StackReference*, `remote.Command`, *Docker provider over SSH*, *VPC*, *firewall rule*, *network tag*, *OS Login* and the `sa_…` user, *timestamp tag*, `retain_on_delete`, *drift*.
- Qualify, don't repeat:
  - "GCR": say Artifact Registry.
  - "NFS persistent volume": say a persistent disk attached to the VM.
  - "Leaderboard": drop it.
  - "class bucket": not used in v3.
  - "through cloud APIs": and through SSH for the inside of the VM.
  - "multi-cloud": many providers, one cloud here.
  - `cheese-app-dev`: `dev`, in two projects.
