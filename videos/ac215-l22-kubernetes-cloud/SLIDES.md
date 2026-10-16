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

## This video and the slides

**Basis.** The video is not scripted yet. This folder holds only `SLIDES.md` and `digest.md`: there is no `BRIEF.md`, `script.md`, `ASSETS.md` or `assets/terminal/`. The map below therefore uses the hook and the ten planned chapters in [`digest.md`](digest.md) §8, the study guide (`MLOps_Learning/guides/L22-kubernetes-cloud.md`) and every slide: the extracted text and all five contact sheets, re-read for this section. With no captures yet, "what the tutorial does today" means `cheese-app-v3` `main` @ `3ecef56`. For the conflicts I re-read these in that clone on 2026-10-16:
- the warm-up in the README (lines 517–581: `--num-nodes 2` at 541, `componentstatuses` at 484 and 559) and its Mermaid diagram (457–474);
- the two demo manifests, `src/deployment/deploy-k8s-tic-tac-toe.yml` and `src/deployment/emoji.yaml`;
- the cluster and its node pool (`deploy_k8s/create_cluster.py:14`, `:24`, `:52`, `:63-71`), and the one-time `get-credentials` command (`:192-199`, `--zone {region}` at `:197`);
- the Service types (`setup_containers.py:98`, `:183`, `:332`) and the Helm release with its `LoadBalancer` Service (`setup_loadbalancer.py:11-46`, `:23`);
- the toolbox (`src/deployment/Dockerfile:30`, `:33`, `:44`) and its `docker run`, which publishes no ports (`docker-shell.sh:34-50`).

When `assets/terminal/` and `ASSETS.md` exist, re-check Conflicts 4, 6, 7, 8 and 14 against them: the `gcloud … create` table, the `get-credentials` line, `kubectl version`, `componentstatuses`, and a port-forward. If they disagree, the captures win.

**Pictures.** The README has no images, only one Mermaid diagram of the request path (README 457–474). The slides add the motivation story (5, 9, 13), container vs Kubernetes deployment (19) and the parts of a cluster (22–26). No slide draws the cheese app running on the cluster: slide 22 aims it at an empty cluster, and slide 41 hands over to the README. The digest's §1 diagram is the only picture of the finished system.

### 1. Map: planned chapters ↔ slides

| # | Planned chapter (`digest.md` §8) | Slides on the same ground | Relation |
|---|---|---|---|
| Hook | One VM, 300 classmates, a 2 a.m. reboot: who notices, who fixes it, who pays? | 4–11 | Same concept. Slide 7 is the hook's "who fixes it": the owner calls Support, who logs in over SSH and restarts the container. Slides 8–11 add backup copies that still need a human. The lecture's story uses a demo app (one frontend, two APIs), not the cheese app. |
| 1 | From one box to a fleet (≈3 min) | 12–15, 17, 19, 21–22; 32–40 (the warm-up) | Same concept, and the tutorial applies it. Slide 12's three asks and slide 19's two pictures are the chapter's idea. Slides 21–22 are its visual: the L20 VM, then the same app aimed at a cluster. The chapter's on-screen warm-up is slides 32–40 almost command for command (README 517–581). Conflicts 4, 7, 8, 12. |
| 2 | Anatomy of a GKE cluster (≈4 min) | 18, 22–26, 36–37 | Same concept for the control plane and the worker nodes. Slides 24–26 name the components that the plan lists only in one line (Gap 1). Node pools, regional vs zonal, private nodes and Cloud NAT are tutorial-only. Conflicts 9, 10. |
| 3 | Desired state, not commands (≈4 min) | 7 and 11 (the manual restart), 15 ("Failovers"), 18, 25 (controller manager), 29 (`delete pods --all`), 30, 36 (Pod names), 39 (Deployment) | Same concept. Slide 18's "K8s handles the rest" and slide 30's "Declaratively" are the chapter's thesis; slide 39 says the Deployment keeps its Pods running. ReplicaSets, the controller loop and Jobs are tutorial-only. Conflict 2. |
| 4 | Names that survive: labels, Services, DNS, namespaces (≈3 min) | 18, 27–29, 35, 39 (Service) | Same concept for the Service ("allows pods to die", slide 39). Labels and selectors, cluster DNS and namespaces are tutorial-only; the slide-39 YAML even drops the selector (Conflict 12). Slides 29 and 35 show the default namespace without naming the idea. |
| 5 | The journey of one click (≈5 min) | 5 and 21 (NGINX in front, on a VM), 24–26 (Cloud Provider API, kube-proxy), 38–39 (`LoadBalancer`, 80 → 8080), 12 and 15 (load balancing) | The tutorial applies it with a different pattern: one load balancer in front of an Ingress controller, not one per Service (Conflict 11). Ingress, Helm, the Host header, `sslip.io` and `ROOT_PATH` are tutorial-only. Conflict 13 (slide 21's ports). |
| 6 | Identity without key files (≈4 min) | 27 (kubectl talks to the Kubernetes API), 33 (`get-credentials`) | Mostly tutorial-only. The lecture's one identity step is "connect to the cluster" (Conflict 6). Kubeconfig, the exec plugin and Workload Identity are not on the slides. |
| 7 | Disks that follow Pods (≈3 min) | none (21 draws the vector DB container; 13 duplicates every part) | Tutorial-only. The chapter explains why slide 13's duplication cannot simply be applied to the API and the vector DB (Conflict 2). |
| 8 | Run it: `pulumi up` end to end (≈5 min) | 21–22 (`pulumi` in the toolbox), 41 (the handover), 28, 34–37 (checks) | The tutorial applies what slide 41 only announces: running the Pulumi code for the cheese app. Everything inside `pulumi up` is tutorial-only. Conflicts 5, 6, 7, 8. |
| 9 | Scaling at two levels (≈4 min) | 12, 15, 18 (CPU, memory, custom metrics), 39 (`replicas: 2`), 43 ("Automatically Adjusting", "Reduce Cost") | Same concept, but the lecture states it and the repo applies only half of it (Conflict 1). Requests, bin-packing and the two levels are tutorial-only; slide 43's "better infrastructure utilization" is the bin-packing in three words. |
| 10 | Tear down and audit (≈2 min) | 40, 44 | Same concept. The tutorial applies it with `pulumi destroy`, not `gcloud … delete` (Conflict 5). Orphaned load balancers and disks are tutorial-only. |
| Recap | Six recap questions | 15, 20, 30, 43 | Lecture-only material that can carry the content recap the plan lacks (Gap 6). |
| — | not in the plan | 1–3, 16, 31, 42 (title, outline, dividers); 6, 10, 14 (live demos); 17 (the name and its history); 45 | Lecture-only. Slide 17's etymology has one use (Gap 8). |

### 2. Already in common

| # | Concept | Chapter ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | One VM needs a human whenever something breaks | Hook, §1 ↔ 4–7, 11 | Yes, closely. The plan's "who notices, who fixes it" is slide 7. Its extra question, "who pays?", is slide 43's cost point. |
| 2 | Kubernetes is an orchestrator: it runs containers across a cluster of VMs | §1 ↔ 17, 19 | Yes. The plan's "VM tower cracks, containers land on node tiles" is slide 19's left-to-right picture. |
| 3 | What it automates: restarts (failover), spreading traffic (load balancing), scaling | §1 ↔ 12, 15 | Yes, and the plan's list is longer (place, discover, roll out). The plan does not use the lecture's three-item checklist (Gap 2), and the tutorial delivers each item only in part (Conflicts 1, 2). |
| 4 | A cluster is a control plane that decides plus worker nodes that run containers | §2 ↔ 18, 22–23 | Yes. The plan's "brain and muscle" is slide 22's single panel with arrows to three workers. The plan adds what GKE changes: Google runs the brain, and the muscle comes in node pools (Conflict 9). |
| 5 | Declare the desired state; Kubernetes carries it out | §3 ↔ 18, 30 | Yes. The plan's thermostat and controller loop are the mechanism behind slide 18's "K8s handles the rest", which the slides do not show. |
| 6 | A Deployment says what runs in a Pod and how many copies, and keeps them running | §3 ↔ 39 | Yes. The plan adds the ReplicaSet in between, and slide 36's Pod names (`web-854b4968b9-…`) already carry its hash. |
| 7 | A Service routes traffic to one Pod or many, so Pods can die | §4 ↔ 39 | Yes. The plan adds what makes it work, the label selector, which the slide's YAML leaves out (Conflict 12). |
| 8 | `kubectl` is the client, and it talks only to the API server | §1, §8 ↔ 22, 24, 27 | Yes. Slide 27's grammar, `kubectl [command] [TYPE] [NAME] [flags]`, is not in the plan (Gap 3). |
| 9 | `gcloud` creates and deletes the cluster; `kubectl` works inside it | §1 (warm-up) ↔ 32–36, 40 | Yes for the warm-up. For the cheese app, Pulumi takes `gcloud`'s place (Conflict 5). |
| 10 | The warm-up: apply the tic-tac-toe manifest, read the external IP, open the game | §1 ↔ 38 | Yes, command for command (README 563–575). |
| 11 | In the default namespace, `kubectl get all` shows only `service/kubernetes` | §4, §8 ↔ 35 | Yes. Slide 35's almost empty output is exactly what students see after the cheese app is deployed (digest Step 8). The slide shows it for a new cluster; the plan uses it to introduce namespaces. |
| 12 | A Service of type `LoadBalancer` asks the cloud for an external IP | §5 ↔ 24–25 (Cloud Provider API, "IP addresses"), 38–39 | Partly. Same mechanism, but in the cheese app only the NGINX controller's Service has that type (Conflict 11). |
| 13 | Kubernetes can scale apps by CPU and memory | §9 ↔ 18, 43 | Yes on the idea. The plan is more precise: the HPA measures usage against requests, and this repo has no HPA (Conflict 1). |
| 14 | The platform handles node failures | §2, §3 ↔ 25 | Yes. The plan's node auto-repair (`create_cluster.py:68`) is GKE's form of it. |
| 15 | You build from the same laptop setup as L20; only the target changes | §1, §8 ↔ 21–22 | Yes. The slides' "Local Computer" with its CLI list is our deployment container (Conflict 7). |
| 16 | Delete the cluster when you are done | §10 ↔ 40, 44 | Yes. The plan adds what a delete can leave behind. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Who does what inside the cluster (slides 23–26).** The plan's §2 names the control plane's parts in one line and never draws the worker side. Students who know the parts can read their own failures:
   - a Pod stuck in `Pending` is the scheduler finding no room (digest §6 item 11);
   - `ImagePullBackOff` is the kubelet failing to pull (item 7);
   - a deleted Pod that comes back is a controller at work;
   - `EXTERNAL-IP <pending>` is the controllers waiting on the cloud provider API;
   - every `kubectl` command goes to the API server.

   **Carry it in** §2: re-draw slide 24 for GKE, in the deck's three beats (22 → 23 → 24). Then reuse that one diagram in §3 (the controllers), §5 (the cloud provider API gives the load balancer its IP), §8 (which part each status line comes from) and §9 (the scheduler and Pending).
2. **The three asks as a running checklist (slides 12, 15).** Failover, load balancing, scaling: the lecture's whole motivation in three words, ticked green on slide 15. The plan has no recurring structure that ties its ten chapters back to why Kubernetes exists. **Carry it in** the hook (ask the three questions), then tick one item per chapter: failover in §3 (the Pod comes back, with Conflict 2's footnote), load balancing in §5, scaling in §9 (with Conflict 1's honest note). Close the recap on the ticked list.
3. **The `kubectl` grammar (slides 27–29).** The guide's checklist holds about forty working `kubectl` commands. `kubectl [command] [TYPE] [NAME] [flags]` lets a student read every one of them, and `-n cheese-app-namespace` is just a flag. **Carry it in** §1 at the first `kubectl get`, as a four-slot card; in §4, drop `-n cheese-app-namespace` into the flags slot.
4. **Before and after (slides 9, 13, 19).** On slide 9 each backup sits on the same VM as its original, so a VM failure still takes both down, and someone still switches by hand. Slide 13 spreads copies over nodes and lets Kubernetes do the switching. That is a ready-made pause-and-ponder, and slide 19 compresses the same contrast into one picture. **Carry it in** the hook and §1: retell slide 9 in the series style and pause, then use slide 19 as the transition to the cluster. Warn here that "Kubernetes deployment" (a way of deploying) is not the `Deployment` object of §3.
5. **The two manifests side by side (slides 38–39).** The plan's §1 runs the tic-tac-toe warm-up but shows no YAML, and §3–§4 jump straight to Pulumi Python. The 35-line `deploy-k8s-tic-tac-toe.yml` is the smallest complete Deployment-and-Service pair a student will see, and the cheese app's Python sets the same fields. **Carry it in** at the end of §1 (or in §4): show the real file, bracket the Deployment and the Service as slide 39 does, and draw the `run: web` link the slide leaves out (Conflict 12). Then cut to `setup_containers.py:57-64` and `:97-106`, which have the same shape.
6. **The payoff, for the content recap (slides 20, 30, 43).** The plan ends with questions but no content recap, which the series' content gates require. Slide 43's five advantages map onto what the student built: self-service (one `pulumi up`), lower cost through better use of the machines (requests and bin-packing, §9), automatic adjustment (the node autoscaler), smooth running (self-healing, §3), simpler development (the same images as L20). **Carry it in** the recap, as five lines, each tied to a chapter.
7. **The cluster in the console (slide 37; README 544–549).** The README's warm-up asks students to click through Kubernetes Engine → the cluster → Nodes, and the console is where many will look first when something fails. The plan never shows it. **Carry it in** §1 or §8 as a short re-drawn panel (no screenshot): Clusters, Workloads, Services & Ingress, filtered to `cheese-app-namespace`. Label it a re-drawing until a capture exists.
8. **Where the name comes from (slide 17).** "Helmsman" explains the ship's-wheel logo and the name of Helm, the chart tool that installs the NGINX controller in §5. **Carry it in** §5, as one sentence when Helm appears.

### 4. Conflicts

No captures exist yet, so "today" is the repo at `3ecef56`, re-read as listed under Basis. The captures will decide once they are made.

| # | Slides say | Tutorial today | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **Kubernetes scales apps on CPU, memory or custom metrics** (slide 18); "Scaling" is ticked (15); apps adjust automatically to load (43). The deck's only replica count is `replicas: 2` in the tic-tac-toe YAML (39). | The cheese app sets no `replicas` (each Deployment runs one Pod) and creates no HorizontalPodAutoscaler. The one automatic layer is the node pool's autoscaler, 1 to 2 nodes (`create_cluster.py:63-66`), which reacts to Pending Pods, not to load. The README's title says "Scaling", but it has no scaling step (digest erratum 3). Milestone 5 asks for a manual scaling demo. | The code | "Kubernetes can scale on load; slide 18 is right. This repo switches on one layer, the nodes. The Pod layer is yours to turn: `kubectl scale` for the milestone, an HPA if you add one." In §9, tick slide 15's "Scaling" only after node #2 arrives, and draw the Pod-level tick dashed (available, not configured). |
| 2 | **Failover to a backup.** The owner asks for a backup server to fall back on (8); slide 13 shows every part as several Pods on two nodes; "Failovers" is ticked (15). | Every cheese-app Deployment runs one Pod. When it dies, the ReplicaSet makes a new one: a short outage, not a switch to a standby (digest §9 E1). The nodes sit in one zone (`node_locations=["us-central1-a"]`, `create_cluster.py:71`), so the regional control plane survives a zone failure but the app does not. The API and the vector DB cannot simply get a second replica on another node, because their disks are ReadWriteOnce (digest §3.5, §6 item 10). | The code | "Kubernetes automates what Support did by hand: notice, and restart. A hot backup, as in slide 13, needs two replicas. The frontend could have them today; the two parts with a disk can't, without other storage." Use this as the bridge from §3 to §7. |
| 3 | **One cluster per component**: three Kubernetes clusters (frontend, API 1, API 2), two nodes each (13). | One regional cluster `cheese-app-cluster`, one node pool of 1–2 `n2d-standard-2` nodes, and one namespace `cheese-app-namespace` holding all three Deployments and the loader Job (digest §1). | The code | "The demo split the app over three clusters to keep the picture clear. The usual pattern, and the cheese app's, is one cluster: the parts are separate Deployments, kept together by a namespace." Draw one cluster box. |
| 4 | **Warm-up cluster**: `gcloud container clusters create test-cluster --num-nodes 1 --zone us-east1-c` (32–33); the output table shows `e2-medium`, 1 node, GKE `1.20.9-gke.701`. Slide 37's console shows the same cluster with 2 nodes. | README line 541 uses `--num-nodes 2`, same name and zone, and leaves the machine type at GKE's default. The cheese app's own nodes are `n2d-standard-2` (`create_cluster.py:14`). | The README (`--num-nodes 2`); the slide's versions are years old | Show the README's command. "The slide makes one node; the README makes two, so the two tic-tac-toe Pods can land on different machines. Either works." Don't show the slide's output table; capture today's. |
| 5 | **`gcloud` creates and deletes clusters** (32, 40). Slide 34 says you need `kubectl` to create a cluster and deploy an app to it. | For the cheese app, Pulumi creates the regional cluster, its node pool and its network (`pulumi up`, digest Step 7) and removes them (`pulumi destroy`, Step 14). `gcloud` creates only the warm-up `test-cluster`. `kubectl` never creates a cluster; it manages objects inside one. | The code | "Slides 32–40 are the warm-up done by hand, and the README does it the same way. The cheese app's cluster is code: the `gcloud` line becomes `gcp.container.Cluster`, the delete becomes `pulumi destroy`." Say once that `kubectl` does not create clusters. |
| 6 | **Connecting kubectl**: `gcloud container clusters get-credentials test-cluster --zone us-east1-c --project ac215-project` (33), right after a create whose output already says a kubeconfig entry was generated. | For the warm-up, `create` writes the kubeconfig, so no extra step is needed in that session. For the cheese app, Pulumi runs `get-credentials` once, at create time, in a container started with `--rm` (`create_cluster.py:192-199`, `docker-shell.sh:34`), and passes the region to `--zone` (`:197`). In a later session `kubectl` has no kubeconfig and reports `connection refused` (digest §6 item 2). The fix is `gcloud container clusters get-credentials cheese-app-cluster --region us-central1 --project <PROJECT>`. `ac215-project` is the instructor's project. | The code; `--region` is the unambiguous form for a regional cluster | "Slide 33's command tells kubectl where the cluster is and how to log in. Pulumi runs it for you once, and your next container session forgets it, so keep this line handy: `--region us-central1`, your own project." |
| 7 | **Install `gcloud` and `kubectl` first** (32, 34). The "Local Computer" CLI list is `gcloud`, `docker`, `kubectl`, `pulumi` (21–26). The outputs show kubectl `v1.22.1` and a `1.20.9-gke.701` cluster (33–36). | Only Docker is installed on the laptop. The deployment container ships gcloud with `gke-gcloud-auth-plugin` (`Dockerfile:30`), kubectl from the 1.34 channel (`:33`), Helm (`:44`) and Pulumi, and sets `USE_GKE_GCLOUD_AUTH_PLUGIN=True` (`docker-shell.sh:45`). GKE upgrades the cluster itself (`auto_upgrade`, `create_cluster.py:69`). | The toolbox (kubectl 1.34) | "The slides' 'local computer' is, for us, the deployment container on your laptop. The tools are already in it, plus two the slides don't list: Helm and the GKE auth plugin." Show today's `kubectl version --client`, not the slide's. |
| 8 | **`kubectl get componentstatuses`** lists the scheduler, the controller manager and two etcd members, all `Healthy` (35). | The README still runs it (lines 484, 559), but the command has been deprecated since Kubernetes 1.19 and prints a warning; on GKE it may show little (digest §6 item 19). | Deprecated | Use slide 35's list as a picture of the control plane's parts, not as a check. If the README's line appears on screen, say the warning is expected; check health with `kubectl get nodes`. |
| 9 | **Master nodes**: the control plane is "Master Node 1–3" (23), with its components drawn inside the cluster (24–26) and reported by `componentstatuses` (35). | On GKE, Google runs the control plane. For `cheese-app-cluster` it is regional (`location=region`, `create_cluster.py:24`) and reached at a public endpoint. Its machines never appear: `kubectl get nodes` lists only workers, as slide 36 itself shows (one node, ROLES `<none>`). Kubernetes docs now say "control plane", not "master". | GKE's managed control plane | Draw the control plane as a greyed box labelled "run by Google", with the four components inside, outside the node pool. "On GKE you rent the brain: you talk to it, but you never see its machines." |
| 10 | **Docker on every node** (19, 22); slide 26 says the container runtime will be Docker. | The node pool uses `image_type="cos_containerd"` (`create_cluster.py:52`), so the runtime is containerd. Kubernetes removed its built-in Docker Engine support in v1.24. Images built with Docker run unchanged. | containerd | Label the runtime box "containerd". "You still build with Docker; the node runs the same image with containerd." |
| 11 | **One `LoadBalancer` Service per app**, each with its own external IP (38–39; `emoji.yaml` on 28–29 does the same). Kube-proxy balances traffic between the app's parts and the outside world (26). Slides 5 and 21 put an NGINX container in front. | The cheese app's three Services are `ClusterIP`, reachable only inside the cluster (`setup_containers.py:98`, `:183`, `:332`). The one `LoadBalancer` Service belongs to the F5 NGINX Ingress Controller, installed by Helm (`setup_loadbalancer.py:11-46`, `:23`), and an Ingress routes by host and path. The README's Mermaid diagram (457–474) draws this path. NGINX sends requests straight to Pod IPs; kube-proxy carries in-cluster Service traffic such as API → vector DB (digest §3.3). | The code | "Tic-tac-toe opens one door per app. The cheese app opens one door and puts a receptionist behind it: the NGINX controller reads host and path and picks the Service. That's L20's nginx container again, now configured from an Ingress object." In `kubectl get svc -n cheese-app-namespace`, point out that only the controller's row has an EXTERNAL-IP. |
| 12 | **Slide 39's YAML**: the Deployment has `replicas`, `containers`, `image` and `ports` directly under `spec`; the Service has `ports` and `type`. Neither has a name, a selector or a Pod template. | `deploy-k8s-tic-tac-toe.yml` has `metadata.name: web`, `selector.matchLabels` with `run: web`, a `template` carrying the same label, and a Service `selector` of `run: web` (lines 1–35). Kubernetes rejects a Deployment without a selector and a template, and a Service without a selector routes to nothing. | The file | Show the real file, not the slide's. "The slide trims the YAML down to its two jobs. The lines it trims are the glue: the label `run: web`, which the Deployment puts on its Pods and the Service looks for." |
| 13 | **Slide 21's cheese app**: the API reaches the vector DB on "TCP/IP 5432"; four containers (NGINX, API, frontend, vector DB) on one VM. | ChromaDB listens on 8000 (`CHROMADB_PORT=8000` in both L20's `deploy_single_vm` and L22's `setup_containers.py`); 5432 is PostgreSQL's port. A fifth, one-shot loader fills the vector DB; in L22 it becomes a Job. | 8000; five containers | Label the link "8000". "One more container does quiet work: the loader, which on Kubernetes becomes a Job that runs once." Draw the loader dashed. |
| 14 | **Port-forward to your browser**: `kubectl port-forward svc/emojirain 8080:80`, "so you can open it in your browser" (29). | In the course, `kubectl` runs inside the deployment container, which publishes no ports (`docker run` without `-p`, `docker-shell.sh:34-50`). The forwarded port opens on the container's localhost, where the laptop's browser cannot reach it. The guide's alternative: `kubectl port-forward svc/api 9000:9000 -n cheese-app-namespace &`, then `curl localhost:9000/api-service/status` in the same container (digest §3.4). | The code | "Port-forward works; it forwards into the container you typed it in. Test it with `curl` right there, or use the app's public address." |

Not counted as conflicts:
- Slide 28's comment names `example-service.yaml`, but the command applies `emoji.yaml`, which creates a ConfigMap, a two-replica Deployment and a `LoadBalancer` Service. The file is in `src/deployment/`, but no README step uses it (digest erratum 13).
- Slide 22 labels the third worker "Worker Node 2" again; slide 39 has "Decares" twice; slide 41 has "an pulumi code".
- Slide 41's link lands on "Deployment with Scaling using Kubernetes". The cluster steps are under the next H2, "Create & Deploy Cluster" (digest erratum 14). The video should name both headings.
- Slide 25 gives the controller manager the job of talking to the cloud about nodes and IP addresses. Upstream Kubernetes puts that in a separate cloud controller manager, and on GKE the node autoscaler is a Google-run component. This is a simplification, not a contradiction.
- "Worker Plane" (slides 23–26) is the lecture's own term; the Kubernetes docs say worker nodes (or data plane).
- Slide 29's `kubectl delete pods --all` is right for the default namespace. For the cheese app it needs `-n cheese-app-namespace`, and the Pods come back: a pause-and-ponder (see Proposals), not a conflict.
- The live demos (slides 6, 10, 14) ran the instructor's deployments of a demo app whose source is not in the tutorial repositories.
- Slide 17's history (announced by Google in June 2014; its three creators) has no tutorial counterpart.

### 5. Proposals for the BRIEF and script authors

**General**
- **One master diagram: slide 24, re-drawn for GKE.** Build it in §2 in the deck's three beats: slide 22 (one control plane with arrows to the workers), slide 23 (two planes), slide 24 (the components and their arrows). Use today's labels:
  - the control plane as a greyed box "run by Google", with API server, etcd, scheduler and controllers inside (Conflict 9);
  - the workers as "node pool: 1–2 × n2d-standard-2, us-central1-a";
  - the runtime as containerd (Conflict 10);
  - the laptop box as the deployment container, with gcloud, kubectl, helm and pulumi (Conflict 7);
  - the "Cloud Provider API" box outside the cluster, its arrow labelled "nodes, load-balancer IP".

  Then add the tutorial-only layers: the VPC and the NAT funnel (§2), the namespace (§4), the load balancer and the Ingress (§5). Reuse the diagram in §3, §5, §8 and §9 (Gap 1).
- **Slide 15's checklist as a tracker** (Gap 2): three items in a corner, ticked in §3, §5 and §9, with the caveats of Conflicts 1 and 2.
- **Retell the motivation story; don't show it.** The roles are the app owner and the operator ("Support"); the app is a frontend with two APIs (slides 4–11). Re-draw slides 5, 9 and 13 in the series style. Do not show or link the live demos.
- **Tag each chapter with one GREY `lecture_ref(22, "a–b")`**, using the ranges below. The slides themselves never appear on screen.
- **Length.** The plan runs about 37 minutes, over the 25–35 target, and the digest already suggests folding §4 into §3 and §5, and §7 into §9, for about 32 minutes. The lecture supports that cut: it spends nothing on disks or identity and most of its time on motivation and architecture. Bring lecture material in by replacing, not adding:
  - slide 24's diagram replaces part of §2's zone-tile animation;
  - slide 9's pause replaces one of the plan's three pauses, or joins them if the total stays near one per two minutes;
  - slide 39's YAML replaces scrolling terminal in §1.
- **Pause-and-ponder candidates from the lecture**, alongside the plan's three:
  - at slide 9, in the hook: "Support put each backup on the same VM as its original. What still takes the app down, and who switches?";
  - at slide 29, in §3: "You run `kubectl delete pods --all -n cheese-app-namespace`. Which Pods come back, and which one doesn't?" (the Deployments' Pods return; the finished loader Pod does not);
  - at slide 38, in §5: "In `kubectl get svc -n cheese-app-namespace`, which Service has an external IP, and why only one?"

**Per chapter**
- **Hook · Lecture 22 · slides 4–11.** Keep the plan's question and tell it as slide 7's story: the crash, the phone call, the SSH session. Then slide 9's three VMs and the pause. End on slide 12's three asks.
- **§1 · Lecture 22 · slides 12–22, 32–40.** One sentence from slide 17: an orchestrator for containers on a cluster of VMs. Slide 19's before-and-after as the transition, with the warning about the word "deployment" (Gap 4). Slides 21–22: the L20 VM, then the same app aimed at a cluster, with `kubectl` joining the toolbox. Then the warm-up exactly as the README has it (Conflict 4), with slide 27's grammar card at the first `kubectl get` (Gap 3). Close on the tic-tac-toe YAML, bracketed as on slide 39, with the labels drawn (Gap 5, Conflict 12).
- **§2 · Lecture 22 · slides 22–26.** The master diagram, in three beats. One line per component in the lecture's words: API server, etcd, scheduler, controller manager; kubelet, kube-proxy, runtime. Then the GKE specifics: a regional control plane run by Google, a node pool in one zone, private nodes and NAT (tutorial-only).
- **§3 · Lecture 22 · slides 7, 18, 25, 30, 39.** Open on slide 7's "restart the container": that is now the ReplicaSet's job. Slide 18's "K8s handles the rest" captions the thermostat. Point at slide 36's Pod names to show the ReplicaSet hash. Tick "Failover" with Conflict 2's footnote. Add the `delete pods --all` pause here.
- **§4 · Lecture 22 · slides 27, 29, 35, 39.** Slide 39's Service bullet (Pods may die) and the `run: web` link, then the cheese app's `run: frontend`. Slide 35's almost empty `kubectl get all` is the cue for namespaces; then `-n` goes into slide 27's flags slot.
- **§5 · Lecture 22 · slides 5, 21, 24, 26, 38–39.** Start from what students know: one NGINX in front (slides 5, 21). Then slide 38's one door per app, and Conflict 11's one door with a receptionist. On the master diagram, light the Cloud Provider API arrow as the load balancer gets its IP. Slide 17's helmsman when Helm appears (Gap 8). Tick "Load balancing".
- **§6 · Lecture 22 · slides 27, 33.** One line: slide 33's `get-credentials` is the login step, and the rest of identity is tutorial-only. Then Conflict 6's `--region` line as a card.
- **§7 (or inside §9) · no slides.** Say that the lecture duplicates everything (slide 13) and that this chapter shows why two parts of the cheese app can't be duplicated that way (Conflict 2).
- **§8 · Lecture 22 · slides 21–22, 34–37, 41.** Open on slide 41's handover, in our words ("now the cheese app, as Pulumi code"), and name both README headings. During the waits, light the master-diagram component behind each Pulumi status line. Show `kubectl get nodes` and `kubectl get pods -n cheese-app-namespace` with today's output (Conflicts 7, 8), and slide 37's console as a re-drawn panel (Gap 7).
- **§9 · Lecture 22 · slides 12, 15, 18, 39, 43.** Start from slide 18's promise, then Conflict 1's honest picture: the node layer is on, the Pod layer is yours. Set slide 39's `replicas: 2` against the cheese app's missing field. Slide 43's "better infrastructure utilization" captions the bin-packing animation. Tick "Scaling".
- **§10 · Lecture 22 · slides 40, 44.** Slide 40's delete becomes `pulumi destroy` (Conflict 5). Show slide 44's message as a GOLD "Don't forget to delete" card without the meme, then the leftover checks.
- **Recap · Lecture 22 · slides 15, 20, 30, 43.** Replay the three-item checklist with what did each job in the cheese app: the ReplicaSet (failover), the Ingress controller and the Services (load balancing), the node autoscaler and `kubectl scale` (scaling). Then slide 43's five advantages as five lines, each tied to a chapter (Gap 6).
- **Recap questions.** Keep the plan's six, and add three:
  - "Which control-plane part decides where a new Pod runs, and which one notices that a Pod died?" (slides 24–25)
  - "In the opening story, what did Support do by hand, and which Kubernetes object does it for the cheese app?" (slides 7, 11, 15)
  - "Why does `kubectl get all` show only `service/kubernetes`?" (slide 35)

**Terms**
- Use the lecture's words: *orchestration*, *cluster*, *node (VM)*, *Pod*, *Deployment*, *Service*, *control plane*, *worker node*, *API server*, *etcd*, *scheduler*, *controller manager* / *controllers*, *kubelet*, *kube-proxy*, *container runtime*, *cloud provider API*, `kubectl`, *failover*, *load balancing*, *scaling*, *declarative*, *replicas*, `LoadBalancer`.
- Add the tutorial's words where the lecture stops (the slides use none of these): *namespace*, *ReplicaSet*, *label* / *selector*, *Job*, *PersistentVolumeClaim*, *node pool*, *cluster autoscaler*, *HorizontalPodAutoscaler*, *resource requests*, *Ingress* / *Ingress controller*, *Helm*, *kubeconfig*, *Workload Identity*, *Kubernetes service account*, *private nodes*, *Cloud NAT*, `sslip.io`.
- Qualify, don't repeat:
  - "Master node": control plane, run by Google on GKE.
  - "Worker Plane": worker nodes, here one node pool.
  - "Docker" as the node runtime: containerd.
  - "Kube Proxy": kube-proxy.
  - "Container Deployment" / "Kubernetes Deployment" (slide 19): ways of deploying, not the `Deployment` object.
  - "Local Computer": the deployment container on your laptop.
  - "install gcloud / kubectl": already in the deployment container.
  - "3 k8s clusters": one cluster for the whole app.
  - "TCP/IP 5432": port 8000.
