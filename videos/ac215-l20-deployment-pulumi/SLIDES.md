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
