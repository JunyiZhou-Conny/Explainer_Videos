# L22 lecture slides — Scaling: Kubernetes (cloud)

Source: one deck, `L22_scaling_kubernetes_cloud` (45 slides), titled "Lecture 22: Scaling:
Kubernetes (cloud)" (AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's
lecture slides (PDF), provided by the student for study; the PDFs are not in this repository;
slide numbers are PDF page numbers. The page numbers printed in the slide footers agree with the
PDF pages (slides 1, 27–29, 44 and 45 print none). This digest was written from the deck's
extracted text, from all five contact sheets, and from enlarged views of slides 5, 9, 13, 19,
21, 22, 24–26, 37, 39, 44 and 45. The link targets behind the demo and tutorial links (slides 6,
10, 14, 41) were read from the PDF's link annotations. Everything below is paraphrased; only
short titles, terms, URLs and single code lines are quoted. The tutorial side of the lecture is
in [`digest.md`](digest.md); `§` references below point there.

## Outline

The deck has four sections (slide 2). Divider slides repeat the outline with the current section
in bold (slides 3, 16, 31, 42).

- Slide 1 · title slide (Harvard shield, course badge AC215/E115)
- Slide 2 · outline: Motivation; Introduction to Kubernetes; Tutorial: Deploying a Kubernetes
  Cluster; Advantages of using Kubernetes
- Slides 3–15 · **Motivation** (a story: "Pavlos" wants an app, "*Support*" runs it)
  - 3 · section divider ("Motivation" in bold)
  - 4 · Pavlos wants one frontend and two backends (diagram: Frontend → API 1, API 2)
  - 5 · "Motivation - 3 Containers in 1 VM": Support's architecture, one VM with an NGINX
    container in front of two API services and the frontend (diagram)
  - 6 · live demo link, "Demo… [3 Containers in 1 VM]"
  - 7 · what happens when a container crashes: Pavlos must call Support, who SSHes in, restarts
    a container to reset its memory, or relaunches a dead one
  - 8 · "Motivation - 3 Containers in 3 VM": Pavlos asks for the app on several servers so one
    can fail over to a backup (quoted request)
  - 9 · Support's answer: three VMs, a second copy of each API (diagram)
  - 10 · live demo link, "Demo… [3 Containers in 3 VMs]"
  - 11 · "Problems": switching to the backup API is still manual, and Support still SSHes in to
    restart or relaunch containers
  - 12 · "Motivation - Kubernetes": can failovers, load balancing, scaling and other key
    processes be automated? "Kubernetes to the rescue..."
  - 13 · "Kubernetes to the Rescue": the app on three K8s clusters with two nodes each (diagram)
  - 14 · live demo link, "Demo… [Kubernetes Cluster]"
  - 15 · "Kubernetes": the three requests (failovers, load balancing, scaling) now ticked green
- Slides 16–30 · **Introduction to Kubernetes**
  - 16 · section divider
  - 17 · "Kubernetes (K8s) to the Rescue": what K8s is (an orchestration tool for distributed
    containers across a cluster of nodes), the Greek origin of the name, and its 2014 origin at
    Google
  - 18 · same title: building blocks that scale by CPU, memory or custom metrics; a
    "primary-replica architecture" with node components and a "control plane"; core concepts
    pods, services, deployments; users define rules and K8s does the rest
  - 19 · "Container vs Kubernetes Deployment" (diagram)
  - 20 · "Why Kubernetes?": four reasons
  - 21 · "How do we build with Kubernetes?": recap of the cheese app on one VM (diagram)
  - 22 · same title: the cheese app's target, a cluster with a control plane and worker nodes,
    with `kubectl` added to the CLI tools (diagram)
  - 23 · "K8s Components & Architecture": control plane of master nodes, worker plane of worker
    nodes (diagram)
  - 24 · same title: the components inside the control plane and a worker node (diagram)
  - 25 · same diagram with a callout explaining the control-plane components
  - 26 · same diagram with a callout explaining the worker-node components
  - 27 · "kubectl": what it is, and its command syntax
  - 28 · "kubectl": apply a manifest, then list deployments, pods and services
  - 29 · "kubectl": port-forward, delete all pods, apply a whole directory
  - 30 · "Kubernetes Summary": four points
- Slides 31–41 · **Tutorial: Deploying a Kubernetes Cluster**
  - 31 · section divider
  - 32 · "Create Kubernetes Cluster": install `gcloud` first; create and delete clusters with
    it; example command for a 1-node cluster and its progress line
  - 33 · same title: the finished create output (cluster table) and the `get-credentials`
    command to connect
  - 34 · "Deploying to Kubernetes Cluster": install `kubectl`; client version vs server
    version (the server call fails with "connection refused")
  - 35 · same title: `kubectl get all` and `kubectl get componentstatuses` with output
  - 36 · same title: `kubectl get nodes` and `kubectl get pods` with output
  - 37 · same title: the cluster in the GCP console (Kubernetes Engine screenshot)
  - 38 · same title: `kubectl apply` of the tic-tac-toe manifest, then `kubectl get services`
    showing an external IP
  - 39 · same title: the Deployment YAML and the Service YAML side by side, each with two
    bullets on its role
  - 40 · "Deleting a Kubernetes Cluster": the `gcloud … delete` command and its confirmation
  - 41 · "Tutorial: Deploying a Kubernetes Cluster": run the Pulumi code for the cheese app;
    tutorial link and QR code
- Slides 42–43 · **Advantages of using Kubernetes**
  - 42 · section divider
  - 43 · five advantages
- Slide 44 · "DON'T FORGET TO DELETE" (meme)
- Slide 45 · closing meme (the extracted text reads "THANK YOU", which is not visible on the
  rendered page)

## Key ideas

1. **One VM is a single point of failure that needs a human.** Support runs the three
   containers on one VM behind an NGINX container. When a container crashes, the app owner has
   to call Support, who logs in over SSH and restarts or relaunches it by hand. (Slides 4–7)
2. **More servers add redundancy, not automation.** Spreading the app over three VMs with a
   backup copy of each API means a failure no longer takes everything down, but switching to the
   backup is still manual and crashed containers still wait for someone to SSH in. (Slides 8–11)
3. **What we actually want automated: failover, load balancing and scaling.** The lecture frames
   Kubernetes as the answer to exactly these three requests, and ticks all three off once the
   app runs on K8s clusters. (Slides 12–15)
4. **Kubernetes is a container orchestrator for a cluster of VMs.** It manages distributed
   containers across many nodes. The name comes from the Greek word for a helmsman, the person
   who steers a ship and keeps it on course; Google announced it in June 2014. (Slide 17)
5. **You declare the rules; Kubernetes carries them out.** Users state how containers should be
   managed and K8s handles the rest, scaling on CPU, memory or custom metrics. The core objects
   are pods, services and deployments. The summary repeats this as "Deploy Applications
   Declaratively". (Slides 18, 30)
6. **From one Docker host to many coordinated nodes.** In a plain container deployment, all
   containers share one VM's Docker engine. In a Kubernetes deployment, each node has its own
   runtime, copies of the same app sit on several nodes, and Kubernetes coordinates them all.
   (Slide 19)
7. **Why Kubernetes: automation and a standard way to run services.** It automates and manages
   microservices, bridges development and operations, standardizes cloud deployments and
   handles day-to-day management of applications. (Slides 20, 30)
8. **Building with Kubernetes keeps the same laptop workflow but changes the target.** The
   cheese app moves from containers on one Compute Engine VM to a cluster. The developer still
   works from a local computer with `gcloud`, `docker` and `pulumi`; the new tool is `kubectl`.
   (Slides 21, 22)
9. **A cluster is a control plane plus a worker plane.** The control plane (one or more master
   nodes) decides; the worker nodes (1 to N) run the containers. (Slides 18, 22, 23)
10. **Control-plane components each have one job.** The API server is the single entry point;
    etcd stores the cluster's state and configuration; the scheduler decides which worker node
    gets each application; the controller manager watches the nodes, handles node failures by
    replicating work elsewhere, provides endpoints to reach the app from outside, and asks the
    cloud provider for resources such as nodes and IP addresses. (Slides 24, 25)
11. **Worker-node components run and connect the Pods.** The kubelet takes instructions from the
    API server and manages the containers on its node; kube-proxy balances network traffic
    between the app's components and the outside world; the container runtime hosts Pods, which
    hold one or more containers. (Slides 24, 26)
12. **`kubectl` is the client for the control plane.** It talks to the cluster through the
    Kubernetes API, with the pattern command, resource type, name, flags. You apply manifests,
    list what was created, forward a port to your machine, and delete resources. (Slides 27–29)
13. **Two tools, two jobs on GKE.** `gcloud` creates, connects to and deletes the cluster itself;
    `kubectl` manages everything inside it. The same cluster is visible in the GCP console.
    (Slides 32–37, 40)
14. **A Deployment keeps Pods alive; a Service lets them die.** The Deployment manifest declares
    what runs in a Pod and how many replicas to keep, and keeps them running. The Service
    manifest declares how traffic reaches those Pods, so individual Pods can die and be replaced
    without clients noticing. A Service of type `LoadBalancer` gets an external IP that maps
    port 80 to container port 8080. (Slides 38, 39)
15. **The cheese app is deployed the same way, but with Pulumi.** The tutorial does by code what
    the slides did by hand. (Slide 41)
16. **The payoff: self-service, cheaper, elastic and smoother.** Teams deploy on their own,
    infrastructure is used more fully (lower cost), capacity adjusts to load, apps keep running
    smoothly, and development gets simpler. (Slide 43)
17. **Clusters cost money until you delete them.** The deck ends its tutorial part with the
    delete command and closes with "DON'T FORGET TO DELETE". (Slides 40, 44)

## Diagrams

- **Slide 4 · the app Pavlos wants.** A blue box "Frontend" on the left with two grey arrows
  fanning right to a green box "API 1" (upper) and an orange box "API 2" (lower). Purpose: the
  shape of the demo app, one frontend calling two independent backends.
- **Slide 5 · three containers in one VM.** At the top, a small screenshot of the demo web page
  ("Deployment Demo" in a dark-blue title bar; two panels, API 1 and API 2, each with small
  buttons that read like "consume memory" and "kill", a URL field and an "Enable Monitoring"
  checkbox; legible only at low resolution). A double-headed arrow labelled "HTTP 80" connects
  the page to a light-blue-grey box labelled "Virtual Machine". Inside: a green "NGINX
  Container" in the top middle; "API Service 1" bottom left with an arrow into NGINX labelled
  "HTTP 9000"; "API Service 2" bottom middle with an arrow up into NGINX labelled "HTTP 9001";
  "Frontend" bottom right with an arrow into NGINX labelled "HTTP 3000". Purpose: everything
  sits behind one reverse proxy on one machine, so the machine is the single point of failure.
  The demo buttons are how the lecture provokes a crash.
- **Slide 9 · three containers in three VMs.** The same demo page at the top, joined by one
  upward arrow to a horizontal bus that drops to three "Virtual Machine" boxes. VM 1: only
  "Frontend", exposed directly ("HTTP 80", no NGINX). VM 2: "NGINX Container" above two boxes
  both labelled "API Service 1", on "HTTP 9000" and "HTTP 9001". VM 3: the same with two copies
  of "API Service 2". Purpose: redundancy by duplication. Note for scene authors: each backup
  copy sits on the same VM as its original, so the copies survive a container crash but not a
  VM failure, and someone still has to switch between them (slide 11). This is a good
  pause-and-ponder setup.
- **Slide 13 · the app on Kubernetes.** The same demo page and bus, now dropping to three
  light-blue boxes, each labelled "Kubernetes Cluster" and captioned below "Frontend", "API 1"
  and "API 2". Each cluster holds two green boxes "Node (VM)", and each node holds two red
  squares. Two floating labels "Pods", placed between the clusters, point thin lines at the red
  squares. Purpose: every part of the app now runs as several Pods spread over several nodes,
  so a dead Pod or node has a twin. Note for scene authors: one cluster per component is the
  demo's layout; the tutorial runs the whole cheese app in a single cluster
  (`cheese-app-cluster`) and a single namespace (§1).
- **Slide 15 · the checklist.** Not a mechanism: "Failovers", "Load balancing", "Scaling" with a
  green tick each. Useful as a recurring on-screen checklist.
- **Slide 19 · container deployment vs Kubernetes deployment.** Left, captioned "Container
  Deployment": one box "Node (VM)" holding six containers in two rows (App1, App2, App3 / App3,
  App2, App3), each drawn as an "App" block on a "Bins/lib" block inside a dashed border marked
  "Container", each in its own colour; all six stand on one wide blue "Docker" bar (whale logo).
  A grey block arrow points right. Right, captioned "Kubernetes Deployment": a box "Kubernetes
  Cluster" with five "Node" boxes (three on top, two below). Each node holds three dashed
  container groups (two coloured blocks each) on its own blue "Docker" bar. Three of the nodes
  carry the same blue/green/red trio, so the same apps are replicated across nodes. Thin blue
  lines run from every node to a Kubernetes logo (blue heptagon with a ship's wheel) at the
  bottom centre. Purpose: from one host packed with containers to a fleet of hosts, each with
  its own runtime, coordinated by one controller.
- **Slide 21 · the cheese app on one VM (recap of L20).** Left: a pink box "Local Computer" with
  an "IDE/ CLI" bar and six small dotted green squares labelled "Containers". A grey block arrow
  points right, with the caption "CLI:" over `gcloud`, `docker`, `pulumi`. Right: a pale
  blue-grey box "Compute Instance (Virtual Machine)" holding four green boxes: "NGINX Container"
  at the top; "API Service Container" (left) with an arrow up and into NGINX, labelled "HTTP
  9000"; "Cheese FrontEnd App Container" (right) with an arrow up and into NGINX, labelled "HTTP
  3000"; "Vector DB Container" (bottom) with an arrow into the API service, labelled "TCP/IP
  5432". Purpose: the starting point the cluster replaces. Note for scene authors: the cheese
  app's vector DB is ChromaDB on port 8000 (`CHROMADB_PORT=8000` in both L20's
  `deploy_single_vm/setup_containers.py` and L22's `deploy_k8s/setup_containers.py`); 5432 is
  PostgreSQL's port. The one-shot vector-db loader container is not drawn.
- **Slide 22 · the same app, aimed at a cluster.** The same "Local Computer" box and arrow; the
  CLI list now reads `gcloud`, `docker`, `kubectl`, `pulumi`, with `kubectl` large and red. The
  target is a dashed box "Kubernetes Cluster": on its left a tall empty grey panel "Control
  Plane"; on its right three green boxes, each with a "Docker" label over a blue rectangle,
  labelled "Worker Node 1", "Worker Node 2", "Worker Node 2" (the third label repeats; read it
  as node 3). Three blue arrows fan out from the control plane's right edge to the three
  workers. Purpose: one brain directs many workers, and `kubectl` is how you talk to the brain.
- **Slide 23 · masters and workers.** Same left side (CLI list with all four tools). Inside the
  dashed "Kubernetes Cluster": a grey column "Control Plane" with grey boxes "Master Node 1",
  "Master Node 2", a column of dots, "Master Node 3"; and a light-green column "Worker Plane"
  with dotted-green boxes "Worker Node 1", "Worker Node 2", dots, "Worker Node N". Purpose: both
  planes can be several machines (a replicated control plane, N workers). Note for scene
  authors: on GKE the control plane is run by Google and never shows up as nodes; `kubectl get
  nodes` lists only workers (slide 36 shows one, with ROLES `<none>`).
- **Slide 24 · components and arrows (the key architecture diagram).** Same left side. Inside the
  dashed "Kubernetes Cluster":
  - Control Plane (grey panel): "Scheduler" and "Controllers" side by side at the top (the
    Controllers box is drawn as a stack of cards, i.e. several controllers); below them a white
    "Kubernetes API server"; below that a cylinder "etcd". Double-headed arrows join Scheduler
    ↔ API server, Controllers ↔ API server and API server ↔ etcd. From the top of the
    Controllers stack a thick arrow leaves the cluster upward and turns right into an orange box
    "Cloud Provider API" outside the cluster.
  - Worker Plane (light-green panel): "Worker Node 1" holds a dark-grey "Kube Proxy", a white
    "Kubelet", and a blue area "Container Runtime" containing two purple-outlined boxes "Pod 1"
    and "Pod 2", each with three dotted "container" boxes. Below: dotted outlines "Worker Node
    2", dots, "Worker Node N".
  - Wiring: one arrow leaves the API server to the right and splits into two arrowheads, one
    into Kube Proxy and one into Kubelet. Kube Proxy → Pods (one-way arrow); Kubelet ↔ Pods
    (two-way arrow).

  Purpose: every component talks through the API server; only the controllers talk to the
  cloud; the kubelet is the API server's hands on each node. A re-draw can build this in three
  beats: control plane, one worker node, then the arrows.
- **Slide 25 · control-plane callout.** The slide-24 diagram with its worker side covered by a
  red-bordered panel "The control plane has:" listing API server (methods to access Kubernetes
  directly), etcd (backend for service discovery, stores cluster state and configuration),
  Scheduler (assigns applications to worker nodes) and Controller manager (tracks worker nodes;
  handles node failures and replicates if needed; provides endpoints to reach the app from
  outside; talks to the cloud provider about nodes and IP addresses). Purpose: a legend for the
  left half.
- **Slide 26 · worker-node callout.** The slide-24 diagram with its control-plane side covered
  by a red-bordered panel "The worker node consists of:" listing Kubelet (talks to the API
  server, manages containers on its node), Kube Proxy (load-balances traffic between components
  and to the outside world) and Container Runtime ("In our case this will be Docker"; hosts Pods
  that run container instances). Purpose: a legend for the right half.
- **Slide 37 · GCP console.** Screenshot of "Kubernetes Engine → Kubernetes clusters" with the
  left menu (Clusters, Workloads, Services & Ingress, Applications, Configuration, Storage,
  Object Browser, Migrate to containers, Config Management) and one row: green status,
  `test-cluster`, `us-east1-c`, 2 nodes, 4 vCPUs, 8 GB. Not a mechanism; it shows where to look.
- **Slide 39 · the two manifests side by side.** Left, "Deployment YAML" (dark code panel) with
  the bullets "Deployment:" what is in a Pod and how many replicas; keeps the Pod running.
  Right, "Service YAML" with the bullets "Service:" how traffic is routed to one Pod or many
  replicas; lets Pods die. Purpose: the two-object pattern (workload + stable entry point).
  Note for scene authors: the YAML is abridged. It omits `metadata.name`, the `selector` and the
  Pod `template`, and puts `containers` directly under `spec`, which Kubernetes would reject.
  The real `src/deployment/deploy-k8s-tic-tac-toe.yml` links the two objects through the label
  `run: web` (Deployment `selector.matchLabels` and template labels, Service `selector`). Draw
  that label link; it is the mechanism the slide leaves out.
- **Pictures that are not diagrams:** slide 1 (Harvard shield), slides 17–18 (Kubernetes logo),
  slides 32–36, 38 and 40 (terminal output, quoted below), slide 41 (QR code for the tutorial
  link), slide 44 (photo of a man labelled "Prof. Pavlos" hurling a bag towards a blue dumpster,
  captioned "Delete! Delete! Delete!"), slide 45 (an animated-film celebration scene captioned
  "When the lecture is finally over!", one character labelled "Students").

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Pavlos", "*Support*" | 4–15 | Story roles: the app owner and the operations team. Not in the tutorial. |
| "Frontend", "API 1", "API 2"; "API Service 1/2" | 4–13 | The lecture's demo app (a "Deployment Demo" page plus two APIs), not the cheese app. Its source is not in any tutorial repository we have. |
| "Virtual Machine", "Compute Instance (Virtual Machine)" | 5, 9, 21 | L20's `deploy_single_vm`. |
| "NGINX Container" | 5, 9, 21 | L20's nginx container with a hand-written `nginx.conf`. In L22 the tutorial replaces it with the F5 NGINX Ingress Controller (installed by Helm) plus an Ingress object (§3.4). The slides never say "Ingress". |
| "Failovers", "Load balancing", "Scaling" | 12, 15 | In the tutorial: failover = the ReplicaSet recreating Pods and GKE repairing nodes; load balancing = GCP load balancer → NGINX → Service; scaling = only the node-pool autoscaler (1–2 nodes); no `replicas` or HPA in the cheese-app code (§3.6, erratum 3). |
| "Kubernetes Cluster", "K8s cluster", "K8s" | 13, 17–26 | README says "K8s cluster"; the code's cluster is `cheese-app-cluster`, one regional GKE cluster. |
| "Node (VM)", "Node" | 13, 19 | A GKE node. The tutorial groups nodes in a node pool (`n2d-standard-2`); "node pool" never appears on the slides. |
| "Pods", "Pod 1", "Pod 2" | 13, 18, 24, 26 | Same meaning. |
| "orchestration tool", "managing distributed containers" | 17 | Not in the README. |
| "kubernḗtēs", "helmsman" | 17 | Etymology only. The ship's-wheel logo, and the name of Helm (the chart tool the tutorial uses), follow from it. |
| "primary-replica architecture" | 18 | The lecture's name for the control-plane / worker split. Not in the README. |
| "control plane" | 18, 22–25 | Not in the README; the digest uses it (§3.1). On GKE it is Google-managed and reached at `cluster.endpoint`. |
| "pods, services and deployments" | 18 | The tutorial also creates Jobs, PersistentVolumeClaims, a Namespace, a Kubernetes service account and an Ingress. |
| "Container Deployment" vs "Kubernetes Deployment" | 19 | Here "deployment" means a way of deploying, not the `Deployment` object of slide 39. Keep the two apart in narration. |
| "Bins/lib" | 19 | A container's libraries and binaries layer. |
| "Microservices", "Dev + Ops" | 20 | Framing only. |
| "Local Computer", "IDE/ CLI", "Containers" | 21–26 | In the course the tools live in the deployment container started by `sh docker-shell.sh`, not on the laptop itself (§4, Step 3). |
| "CLI: gcloud, docker, kubectl, pulumi" | 21–26 | The toolbox also holds `helm` and `gke-gcloud-auth-plugin`, which the slides do not show. `kubectl` is pinned to 1.34 there. |
| "Control Plane" / "Worker Plane" | 22–26 | "Worker Plane" is the lecture's coinage; Kubernetes docs say "worker nodes" (or "data plane"). |
| "Worker Node 1 … N" | 22–26 | Nodes of the node pool. |
| "Master Node 1–3" | 23 | Older Kubernetes wording; current docs say "control plane nodes". Invisible on GKE. |
| "Kubernetes API server", "etcd", "Scheduler", "Controllers" / "Controller manager" | 24, 25 | Not in the README. The slide's controller-manager list folds in jobs that upstream Kubernetes gives a separate cloud controller manager (talking to the cloud provider). |
| "Cloud Provider API" | 24–26 | On GKE, how a `LoadBalancer` Service gets its external IP (slide 38) and how the node autoscaler adds VMs. |
| "Kubelet", "Kube Proxy", "Container Runtime" | 24, 26 | The program is spelled `kube-proxy`. |
| "Docker" as the node runtime | 19, 22, 26 | GKE nodes in the tutorial run containerd (`image_type="cos_containerd"`, `create_cluster.py:52`); Kubernetes dropped its built-in Docker Engine support in v1.24. Images built with Docker run unchanged. |
| `kubectl` | 22, 27–29, 34–38 | Same. |
| "gcloud … the GCPs command-line tool" | 32 | Same. In the tutorial, Pulumi (not `gcloud`) creates the cheese-app cluster; `gcloud` creates only the warm-up `test-cluster`. |
| "test-cluster" | 32–40 | The README's warm-up, "Create Simple Kubernetes Cluster Tutorial" (§4 Part 0). |
| "Kubernetes Engine" | 37 | The GKE console. |
| "Deployment YAML", "Service YAML" | 39 | `deploy-k8s-tic-tac-toe.yml`. The cheese app's objects are written in Pulumi Python (`deploy_k8s/setup_containers.py`), not YAML. |
| "replicas" | 39 | The tic-tac-toe Deployment sets 2; the cheese-app Deployments set none (default 1). |
| `LoadBalancer` (Service type) | 38, 39 | In the cheese app only the NGINX controller's Service is `LoadBalancer`; the app's Services are `ClusterIP` (§3.3). |
| "emojirain", `emoji.yaml` | 28, 29 | `src/deployment/emoji.yaml`: a ConfigMap, a 2-replica `emojirain` Deployment (`nginx:alpine`) and a `LoadBalancer` Service. Not referenced by the README (erratum 13). |
| "Deploying a Kubernetes Cluster" | 2, 31, 41 | README headings: "Deployment with Scaling using Kubernetes" and "Create & Deploy Cluster". |
| "Abstracting Infrastructure", "Standardize", "Declaratively", "Daily Management" | 30 | Summary keywords. |
| "Self-Service", "Reduce Cost", "Automatically Adjusting", "Smoothly", "Development" | 43 | Advantage keywords. |

**Tutorial vocabulary the slides never use:** namespace, ReplicaSet, labels and selectors (the
slide-39 YAML even drops them), Ingress and Ingress controller, Helm, PersistentVolumeClaim, Job,
node pool, cluster autoscaler, HorizontalPodAutoscaler, Workload Identity, Kubernetes service
account, kubeconfig, Cloud NAT, private nodes, `sslip.io`. The video has to introduce these from
the tutorial (§3).

### Slips and dated details on the slides (do not repeat in narration)

- Slide 21: the vector DB link is labelled "TCP/IP 5432"; the cheese app's ChromaDB uses port
  8000.
- Slide 22: the third worker is labelled "Worker Node 2" again.
- Slide 26: the runtime is "Docker"; on GKE it is containerd (see the table).
- Slide 28: the comment names `example-service.yaml`, but the command applies `emoji.yaml`, which
  creates three objects, not just a service.
- Slide 29: port-forwarding "so you can open it in your browser" does not work as-is from the
  course toolbox. `kubectl` runs inside the deployment container, which publishes no ports, so
  the forwarded port is only reachable inside the container (§3.4). Use the Service's external
  IP, or `curl` from inside the container.
- Slides 32–33: the example creates a 1-node cluster (`--num-nodes 1`); the README's warm-up uses
  2 nodes, and the console screenshot on slide 37 shows 2. The outputs are old (GKE
  `1.20.9-gke.701`, kubectl `v1.22.1`); today's toolbox ships kubectl 1.34.
- Slide 33: `--project ac215-project` is the instructor's project ID; students use their own.
- Slide 34: says kubectl is needed "To create a Kubernetes cluster"; `gcloud` (or Pulumi) creates
  clusters, `kubectl` only manages what is inside. In the course, kubectl is preinstalled in the
  deployment container.
- Slide 35: `kubectl get componentstatuses` has been deprecated since Kubernetes 1.19 and prints
  a warning (§6, item 19).
- Slide 39: abridged YAML (see Diagrams); "Decares" should read "Declares" (twice).
- Slide 41: "Run an pulumi code" (typo). The link opens the README's "Deployment with Scaling
  using Kubernetes" section; the cluster steps are under the next H2, "Create & Deploy Cluster"
  (erratum 14).

## Commands and code on the slides

- Slide 27: `kubectl [command] [TYPE] [NAME] [flags]`
- Slide 28: `kubectl apply -f emoji.yaml`
- Slide 28: `kubectl get deployments` · `kubectl get pods` · `kubectl get svc`
- Slide 29: `kubectl port-forward svc/emojirain 8080:80`
- Slide 29: `kubectl delete pods --all` (commented as deleting all Pods in the default namespace)
- Slide 29: `kubectl apply -f <directory>`
- Slides 32, 33: `gcloud container clusters create test-cluster --num-nodes 1 --zone us-east1-c`
- Slide 32 (progress line): `Creating cluster test-cluster in us-east1-c...`
- Slide 33 (output): `kubeconfig entry generated for test-cluster.`, then a table row with
  `test-cluster`, `us-east1-c`, `e2-medium`, `1`, `RUNNING`
- Slide 33: `gcloud container clusters get-credentials test-cluster --zone us-east1-c --project ac215-project`
- Slide 34: `kubectl version --client` (prints a `Client Version: version.Info{…GitVersion:"v1.22.1"…}` line)
- Slide 34: `kubectl version` (client line, then `The connection to the server localhost:8080 was refused - did you specify the right host or port?`)
- Slide 35: `kubectl get all` (output: only `service/kubernetes`, `ClusterIP`, `443/TCP`)
- Slide 35: `kubectl get componentstatuses` (output: `scheduler`, `controller-manager`, `etcd-0`,
  `etcd-1`, all `Healthy`)
- Slide 36: `kubectl get nodes` (output: one node `gke-test-cluster-default-pool-…`, `Ready`,
  ROLES `<none>`)
- Slide 36: `kubectl get pods` (output: two Pods `web-854b4968b9-…`, `1/1`, `Running`)
- Slide 38: `kubectl apply -f deploy-k8s-tic-tac-toe.yml` (output: `deployment.apps/web created`,
  `service/web created`)
- Slide 38: `kubectl get services` (output: `web`, `LoadBalancer`, an external IP highlighted in
  red, `80:32088/TCP`)
- Slide 39, Deployment YAML (key lines): `apiVersion: apps/v1` · `kind: Deployment` ·
  `replicas: 2` · `image: dlops/tic-tac-toe` · `imagePullPolicy: IfNotPresent` · `name: web` ·
  `containerPort: 8080`
- Slide 39, Service YAML (key lines): `apiVersion: v1` · `kind: Service` · `port: 80` ·
  `targetPort: 8080` · `type: LoadBalancer`
- Slide 40: `gcloud container clusters delete test-cluster --zone us-east1-c` (output: a list of
  clusters to delete, the prompt `Do you want to continue (Y/n)?`, then
  `Deleting cluster test-cluster...done.`)

No Pulumi code, Dockerfile or cheese-app manifest appears on the slides; slide 41 hands that over
to the tutorial.

## What the lecture stresses

- **Manual operations do not scale.** Every crash means a call to Support and an SSH session
  to restart or relaunch a container (slides 7, 11). Even with backup copies, switching to them
  is manual (slide 11).
- **Automate the three things operators do by hand:** failover, load balancing and scaling
  (slides 12, 15).
- **Declare, don't script.** Users define the rules for container management and Kubernetes
  handles the rest (slide 18); the summary names declarative deployment explicitly (slide 30).
- **Scale on metrics.** K8s can scale applications on CPU, memory or custom metrics (slide 18).
  The slides show no scaling command; the only replica count anywhere is `replicas: 2` in the
  tic-tac-toe YAML (slide 39). The tutorial has the same gap (erratum 3), and Milestone 5 asks
  for a scaling demonstration (§7, Step 12).
- **The control plane is the single entry point.** All components meet at the API server, and
  `kubectl` talks only to it (slides 24, 27).
- **Deployment and Service have different jobs.** The Deployment keeps Pods running; the
  Service routes traffic and "allows pods to die" (slide 39).
- **Order of tools:** install and use `gcloud` first to create and connect to a cluster, then
  `kubectl` to deploy (slides 32–34). Until you connect, `kubectl version` fails on the server
  half (slide 34).
- **Check the cluster in the console too** (slide 37).
- **Delete clusters when you are done.** The tutorial section ends with the delete command
  (slide 40), and the deck's last content slide is "DON'T FORGET TO DELETE" (slide 44).
- **Why it is worth it:** automating microservices, bridging Dev and Ops, standardizing cloud
  deployments and daily management (slide 20); abstracted infrastructure (slide 30);
  self-service deployment, lower cost through better utilization, automatic adjustment to load,
  smooth running, simpler development (slide 43).
- **Design trade-off shown by the story:** redundancy without orchestration (slide 9) protects
  against a crash only if a human notices and switches; orchestration adds the automatic
  reaction (slides 11–15).

## Pointers

- **Slides 6, 10, 14: live demos.** Each slide is one link. The link targets embedded in the
  PDF open one "Deployment Demo" page with query parameters `title`, `api1` and `api2`, i.e. one
  frontend told where its two APIs live:
  - slide 6: everything on `demo-1-vm.dlops.io` (APIs at `/api1` and `/api2`);
  - slide 10: the frontend on `demo-3-vms-1.dlops.io`, the APIs on `demo-3-vms-2.dlops.io` and
    `demo-3-vms-3.dlops.io`;
  - slide 14: three bare IP addresses (frontend, API 1, API 2), consistent with one cluster per
    component (slide 13).

  These were the instructor's class-time deployments. Do not assume they are still up, and do
  not show them in the video; the demo's source is not in the tutorial repositories.
- **Slide 41: the tutorial.**
  `https://github.com/dlops-io/cheese-app-v3?tab=readme-ov-file#deployment-with-scaling-using-kubernetes`,
  with a QR code. The anchor is valid (README line 392), but the cluster steps continue under
  "Create & Deploy Cluster" (README line 436; digest erratum 14).
- **Slides 28–29, 38–39: files in the tutorial repository.** `emoji.yaml` and
  `deploy-k8s-tic-tac-toe.yml` are both in `cheese-app-v3/src/deployment/`. The tic-tac-toe
  steps match the README's optional warm-up (§4 Part 0); `emoji.yaml` is not in the README.
- **Slide 21: "Remember the Cheese App Architecture"** points back to L20's single-VM deployment
  (cross-reference, not on the slide: `deploy_single_vm` in the same repository).
- **Slide 37: the GCP console**, Kubernetes Engine → Clusters.
- No readings, homework or milestone notes appear on the slides. (The tutorial digest, §7 and
  Step 12, ties scaling to Milestone 5, and L23 automates this deployment with GitHub Actions.)
