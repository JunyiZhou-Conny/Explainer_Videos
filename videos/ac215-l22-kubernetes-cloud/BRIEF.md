# Brief · AC215 L22 — Scaling: Kubernetes in the cloud (the cheese app on GKE)

This is the design of the video, written before the script. Series rules are in `docs/AC215_SERIES.md`.
Facts come from `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture deck, 45 slides,
with its scene map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides
disagree with the captures, the captures win.** The captures are newer: 2026-11-07, 20:47–21:16 UTC,
`cheese-app-v3` `main` @ `3ecef56` (re-checked with `git ls-remote` that day, `laptop/p03`). Each
README command was run as written, in README order, on two stand-ins:
- an empty Docker engine for the laptop (`laptop/`, `docker:29.8.2-dind`, user `student`), inside which
  the deployment toolbox ran every gcloud, Pulumi and kubectl command of the K8s sections;
- a **kind** cluster ("Kubernetes in Docker", 1 control plane + 2 workers, Kubernetes v1.34.11) in that
  same engine (`kind/`): a real API server for the README's kubectl commands, and **not GKE**.

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**:
- the L22 deck, slide by slide, wherever the tutorial applies it (motivation 4–15, the cluster's parts
  17–30, the hand-run warm-up 32–40, the handover 41, the payoff 43–44);
- every README step of the four K8s sections of `cheese-app-v3/README.md`, in order within each:
  - "Create Simple Kubernetes Cluster Tutorial", README:517-581 (the warm-up);
  - "Deployment with Scaling using Kubernetes", README:392-434;
  - "Create & Deploy Cluster", README:436-512;
  - the K8s half of "Debugging Containers", README:618-657.

**Section order.** The README prints the warm-up *after* the cheese-app sections, as an optional
tutorial; the lecture does it *first* (slides 32–40, then 41 hands over to the cheese app). We follow
the lecture: Part 1 is the warm-up, Part 2 the cheese app. Inside every section the README's order is
kept exactly. S04 says this in one sentence ("the README keeps this tutorial at the end, as an
optional extra; the lecture does it first, and so do we, because it is the gentlest first contact
with kubectl"). The warm-up's toolbox start (README:527-536) and the main section's (404-413) are the
same commands: the first time (S04) is the full story with the breakage; the second (S10) is a fast
re-type.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which commit | `main` @ `3ecef56`; an unmerged staff branch exists | `p03` on 2026-11-07: `main` still `3ecef56`. The staff branch is masked as `work/‹staff›` in the capture and **never named or shown**: crop the branch list to `main` (and, if needed, `cluster-updates`, `pipenv`) |
| `sh docker-shell.sh` | digest §2: fails twice as committed (found 11-05 in L20) | **still fails on 11-07** (`b02`: 22 × `404 Not Found` from `bullseye-security`, `pull access denied`, exit 125). With **both** L20 fixes in one edit (`b02a`, shown as a `git diff`) it builds in **92.3 s** (`b03`). Fix 2 is the package that every GKE `kubectl` call needs (`gke-gcloud-auth-plugin`) |
| kubectl version | digest Step 3: `Client Version: v1.34.x` (Dockerfile:33 pins 1.34) | **`v1.35.9-dispatcher`** (`b11`, `b12`): Google's apt repo ships its own `kubectl` package (`1:592.0.0-0`, `b14`), which wins; `/usr/bin/kubectl` is gcloud's dispatcher. Against the 1.34 stand-in it picks a matching client, `v1.34.12-gke.300…` (`k02`). Harmless: one sentence in S04 |
| warm-up `gcloud … create` | slides 32–33 show a create table (years old) | **nothing records today's output.** `b15`: `You do not currently have an active account selected.` Then the kind stand-in (`k01`, labelled, its containerd patch block cropped). Never a fake gcloud table |
| `kubectl get services` | slide 38 shows an external IP; digest 0.4: `<pending>` then an IP | `k11`/`k13`: `web LoadBalancer … <pending> 80:31366/TCP`, still `<pending>` 43 s later: **kind has no cloud load balancer**. The IP view is an `illustration` with `<EXTERNAL-IP>`; the app is reached with `port-forward` (`k57`, extra) |
| `kubectl get componentstatuses` | slide 35: four `Healthy` rows; digest: deprecated | `k06`: `Warning: v1 ComponentStatus is deprecated in v1.19+`, then three `Healthy` rows. Show it, say the warning is expected, check health with `kubectl get nodes` |
| `kubectl get nodes` | slide 36: one GKE node, ROLES `<none>` | `k07`: three nodes on the stand-in, **one of them `control-plane`**. On GKE the control plane is Google's and never listed: say so on the frame |
| `deploy_k8s` preview | digest Step 6: "about 23 resources to create" | the README's Pulumi commands stop at `PULUMI_ACCESS_TOKEN must be set …` (`b20`–`b33`, no state bucket). On Pulumi's local backend (extra): `c13` **`TypeError: 'NoneType' object is not subscriptable`** at `setup_containers.py:70` because the image stack has no outputs; with the capture-only stand-in image stack (placeholder tags) the real plan: **`+ 23 to create`** (`c20`) — the digest's count, confirmed |
| `pulumi up` | digest Step 7: 15–25 min, then Outputs | `c21`: **`gcp:compute:Network cheese-app-vpc creating failed`** … `invalid_grant`: the VPC is the first resource that needs Google. Everything after it is an `illustration` of the dependency order (digest Step 7), never a progress log |
| the Outputs block | README:497-506 | `expected/readme-pulumi-outputs.txt` (IPs as `<IP>`), tagged `expected`. **Older than the code**: the code exports `ip_address` (`__main__.py:48`), not `nginx_ingress_ip`, and the Ingress is `cheese-app-ingress` (`setup_loadbalancer.py:65`); `c20`'s output keys confirm the current names |
| kubectl on the app (README:478-492) | digest Step 8: what you should see | no cheese app anywhere. `b40`–`b45`: before any kubeconfig → `The connection to the server localhost:8080 was refused` (the "new session" symptom); `k20`/`k21` on the stand-in: `No resources found in cheese-app-namespace namespace.` / `namespaces "cheese-app-namespace" not found`. The cheese-app listings are **described, never printed** |
| debugging block (README:618-657) | digest erratum 2 | `k30`–`k43`: 13 × `namespaces "cheese-app-cluster-namespace" not found`, `No resources found …` (631), and the `<pod-name>` placeholders as shell errors (`syntax error near unexpected token 'newline'`, `pod-name: No such file or directory`) |
| `pulumi config` | digest Step 5: leftover keys | `c12`: `setupSSL false` and `security:ssh_user sa_…`. **Mask the number** as `sa_000000000000000000000` |
| length | digest §8: ten chapters ≈ 37 min; merge to ≈ 32 | the plan below is **~4,280 words ≈ 24.6 min of narration**, ~31–33 min with typing, outputs and five ponders |

## Audience and goal

The viewer is an AC215 student who has done L1–L21:
- cloud VMs, SSH, deleting what you create (L1–L2);
- Docker images, containers, ports, `docker-shell.sh`, Docker networks and container names (L2–L4);
- service accounts and JSON keys in `secrets/` next to the repo (L10, L15);
- the cheese app's four services (API, frontend, vector DB, one-shot loader) locally (L18);
- **L20**: the same repo's deployment toolbox (and its two one-line fixes), Pulumi stacks and state,
  `preview` / `up` / `destroy`, the `deploy_images` stack with timestamp tags and `StackReference`,
  and the cheese app on **one VM** behind an nginx container.

They have seen Lecture 22 ("Scaling: Kubernetes (cloud)"). They watch with
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) cloned next to their `secrets/`
folder, Docker Desktop running and a GCP project with billing, pausing to run each step. **Real money
is involved**: a GKE cluster's management fee, its nodes, a load balancer, a NAT gateway and two disks
(GOLD tags; the teardown closes each part).

After the video they can:
- say what Kubernetes automates that L20's VM could not — the lecture's three asks: **failover, load
  balancing, scaling** — and what in the cheese app does each job (and which part is left to them);
- draw a cluster: a **control plane** (API server, etcd, scheduler, controllers; run by Google on GKE)
  and **worker nodes** (kubelet, kube-proxy, containerd, Pods), and say which part is behind a given
  symptom (`Pending`, `ImagePullBackOff`, a Pod that comes back, `EXTERNAL-IP <pending>`);
- read `kubectl [command] [TYPE] [NAME] [flags]`, and use `get`, `apply -f`, `exec`, `logs`,
  `describe`, `delete`, `scale`, `port-forward` and `-n`;
- do the warm-up: start the toolbox (with its two fixes), create a test cluster with `gcloud`, look
  around with `kubectl`, deploy tic-tac-toe, find its external IP, and delete the cluster;
- explain a Deployment → ReplicaSet → Pod chain, why a deleted Pod comes back, and how a Service
  finds its Pods through a **label** (`run: web`), a stable name and cluster DNS; and why
  `kubectl get all` shows almost nothing (namespaces);
- run the cheese app's two Pulumi projects in order (`deploy_images`, then `deploy_k8s`), read its
  23-resource plan, and know what `pulumi up` builds in which order and what it waits for;
- trace one click from the browser to a Pod: `<IP>.sslip.io` → load balancer → NGINX Ingress
  controller → Service → Pod, and say why a bare IP gives a 404;
- reconnect `kubectl` in a new session (`get-credentials --region`), shell into a Pod, read a Job's
  logs with the **corrected** namespace;
- scale the frontend by hand (Milestone 5), and explain the two levels (Pods vs nodes), resource
  requests, `Pending`, the 1–2 node autoscaler, and why the API with its disk cannot simply scale;
- tear down with `pulumi destroy` and audit what may survive it.

## Length and parts

The video runs ~31–33 minutes. Narration is 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm).
The plan below totals **~4,280 words**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S08** (~2,070 words, ~15 min): **Kubernetes by hand.** The lecture's story (slides
  4–15), what an orchestrator is and what a cluster is made of (17–30), and the README's warm-up
  (517–581, slides 32–40) on the stand-in: toolbox, test cluster, tic-tac-toe, self-healing, labels,
  Services, namespaces, delete.
- **Part 2 = S09–S16** (~2,210 words, ~16.5 min): **the cheese app as code.** Slide 41's handover;
  the two cheese-app README sections (392–512): setup, images, the `deploy_k8s` stack, its plan and
  `pulumi up`, the request path, kubectl on the app, the debugging block (618–657), scaling, destroy,
  the recap (slides 15, 20, 30, 43–44).

The cut is the lecture's own seam: slide 40 deletes the test cluster, and slide 41 turns to "run the
Pulumi code for the cheese app". Part 1 ends on S08's empty frame after the test cluster is gone (GOLD
"Don't forget to delete" said, the meter stopped). Part 2 opens on the same cluster picture, now
filled with the cheese app.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop and everything on it: Docker Desktop, the browser, "Local Computer / IDE / CLI" (slides 21–26), the deployment toolbox's outline; **the kind stand-in cluster** (it lives on the laptop: GREY outline, dashed, tag `stand-in: kind, not GKE`) | GREY |
| the cloud: GCP's outline, the **GKE cluster** outline, the control plane box (BLUE, greyed, "run by Google"), worker nodes (VMs), the node pool, the VPC and subnet, Cloud Router / NAT, the external load balancer, persistent disks, Artifact Registry, the GCS state bucket, Vertex AI, the cloud provider API | BLUE |
| containers, images and **Pods** (TEAL circles; containers inside them), the toolbox container `cheese-app-deployment`, `dlops/tic-tac-toe` | TEAL |
| shared, cluster- or OS-owned: `kube-system` and its Pods, the `default` namespace, `service/kubernetes`, Google's apt repo (its `kubectl` package), Debian's archives | ORANGE |
| project-owned, declared: manifests (`deploy-k8s-tic-tac-toe.yml`), the Pulumi programs and stack config, **desired state**, Deployment / ReplicaSet / Job / PVC cards, `cheese-app-namespace`, timestamp image tags | GREEN |
| tools: kubectl, gcloud, helm, pulumi and its providers, docker, kind, gke-gcloud-auth-plugin | PURPLE |
| errors and "don't": every honest first error (`404 Not Found`, `pull access denied`, `invalid_grant`, `no active account`, `PULUMI_ACCESS_TOKEN must be set`, `connection refused`, `TypeError`, `not found`), README lines that are wrong, `Pending` that never ends, `Multi-Attach` | RED |
| your turn, the README tracker, the thing to look at now, ponder timers, the **three-asks checklist ticks** | YELLOW |
| money: the cluster fee, nodes, load balancer, NAT, disks, registry storage; "Don't forget to delete" | GOLD |
| lookups and routes: **Services** (a Service is a routing rule, not a process), labels and selectors (`run: web` stickers), endpoints, cluster DNS names, ports, Ingress rules, `sslip.io`, request arrows, the kubeconfig's server URL, the `StackReference` pipe | PINK |
| the past and the future, and what is possible but not configured: L20's VM, L23, the slides' "Docker" runtime label and "master node" wording, the HPA, a second API replica | GREY, dashed |

Pods are always TEAL and never change colour by state; their **status** is a small word under them
(`Running` WHITE, `ContainerCreating` YELLOW, `Pending` RED, `Completed` GREY).

## Running example

- **The laptop** is a fresh Docker engine: `student@laptop:~/cheese-app-v3/src/deployment$`. The README's
  `cd deployment` (405, 528) means `src/deployment` from the repo root: say it once (S04).
- **The toolbox** prompt is `root@<id>:/app#`, then `/app/deploy_images#`, `/app/deploy_k8s#`. The
  container id is never read aloud.
- **The sandbox, said once (S02's follow-along beat), never apologised for again.** This machine has no
  Google account: everything that runs on a machine you own is real and complete; every command that
  needs Google stops at its honest first error, and the narration says what yours prints instead ("with
  your key, this says …"), **said, never shown**.
- **The stand-in cluster (S05–S08, S14–S15)**, said plainly in S05: "where the README creates a GKE cluster,
  we start a small real cluster on the laptop with a tool called kind. Same API server, same kubectl,
  same YAML; but no Google: no cloud load balancer, no node pool, no autoscaler. It's not in the README;
  don't run it — your cluster is the real one." Every `kind/` panel carries the tag
  `stand-in: kind, not GKE` (GREY), and the extras also carry `extra`.
- **Pulumi's local backend (S10–S12, S16)** is an `extra`: "the README keeps Pulumi's state in a bucket;
  we can't reach one, so to show the plan we point Pulumi at a local folder, `pulumi login --local`. Not
  in the README; don't run it." `c20`/`c21` additionally say "the image tags here are placeholders"
  (the capture-only stand-in image stack), on screen.
- **Placeholders.** `your-gcp-project` is the project in the toolbox's own messages (`b01`, `b03`). The
  README's `ac215-project` stays where a README command prints it (`b21`, `b31`, `c02`, `c11`, `c12`,
  `c03`'s tags, `c21`'s URL) with a GREY tag "the README's default · change to yours". The `sa_…` number
  is always `sa_000000000000000000000`. **No public IP ever**: the README's sample IPs are `<IP>`
  (`expected/`), the browser shows `http://<EXTERNAL-IP>` / `http://<IP>.sslip.io`. The stand-in's
  private cluster addresses (`10.96.…`, `10.244.…`) may stay in panels (private ranges of a deleted
  cluster) and are never read aloud.
- **Versions, all "at the time of recording"**: Google Cloud SDK 592.0.0, gke-gcloud-auth-plugin 0.5.21,
  kubectl = gcloud's dispatcher (1.35.9; 1.34.12-gke against a 1.34 server), Helm v3.22.1, Pulumi
  v3.274.1 (plugins kubernetes 4.23.0, gcp 9.3.0), Python 3.13.18, uv 0.13.7; the stand-in kind v0.31.0
  with Kubernetes v1.34.11; toolbox image 2.61 GB.
- **Crops**: `b02` the `[IP: 172.17.0.1 …]` proxy column; `k01` the `containerdConfigPatches` block;
  `c21` Pulumi's Python shutdown tracebacks; `p03` the staff branch line; `b03` keep the entrypoint's
  error lines, drop the gsutil migration notices. Never read aloud: ids, hashes (except the ReplicaSet's
  `pod-template-hash`, which is the point of S07), timestamps.

## Visual set pieces (the 3Blue1Brown part)

The class names go in `scenes/common.py`. None collides with a scene class in `video.yaml`.

- **V1 · `MasterDiagram` — the lecture's cluster, re-drawn for GKE (slides 22–26).** The spine of the
  video: S03 builds it, S05, S06, S07, S12, S13, S15 reuse it, lighting one part at a time.
  - **Left:** a GREY "your laptop" box; inside it the TEAL toolbox with four PURPLE tool chips `gcloud`
    `docker` `pulumi` and, arriving last and largest, **`kubectl`** (slide 22's red `kubectl`, here
    PURPLE with a YELLOW flash). Two small extra chips the slides don't list: `helm`, `gke-gcloud-auth-plugin`.
  - **Right:** a BLUE dashed "Kubernetes cluster" box, built in the deck's three beats:
    1. *slide 22:* one tall BLUE-greyed **control plane** panel with three arrows fanning to three
       **worker nodes** (BLUE boxes, "Node (VM)");
    2. *slide 23:* the planes get names — "control plane: run by Google" (a GREY dashed caption: the
       slides say "master nodes"; GKE hides them) and "worker nodes: node pool, 1–2 × n2d-standard-2,
       us-central1-a";
    3. *slide 24:* inside the control plane, **API server** (centre), **etcd** (a cylinder below it),
       **scheduler** and **controllers** (a stack of cards) above, each joined to the API server only;
       inside worker node 1, **kubelet**, **kube-proxy** and a **container runtime** strip labelled
       `containerd` (the slide's "Docker" crossed out in GREY dashed: "you still build with Docker; the
       node runs the image with containerd") holding two TEAL Pods with container dots.
  - **Arrows:** kubectl → API server (the only door: "every kubectl command goes here"); API server →
    kubelet and kube-proxy; kubelet ↔ Pods; controllers → an outside BLUE box **"cloud provider API"**
    (slide 24), its arrow labelled "nodes, load-balancer IP".
  - **Callouts** (slides 25–26), one line each, in the lecture's words: API server = the single entry
    point; etcd = the cluster's memory (state and config); scheduler = picks a node for each Pod;
    controllers = keep watching and fix the difference, and ask the cloud for nodes and IPs; kubelet =
    the API server's hands on each node; kube-proxy = routes Service traffic; runtime = runs the
    containers.
  - **Symptom lamps** (reused later): `Pending` lights the scheduler (S15), a Pod that comes back lights
    the controllers (S07), `EXTERNAL-IP <pending>` lights the cloud-provider arrow and leaves it RED on
    the stand-in (S06), `ImagePullBackOff` lights the kubelet (S14, one line).
- **V2 · `FleetMorph` — one box, three boxes, a fleet (slides 4–13, 19; S01–S02).**
  - Slide 5 re-drawn: one BLUE VM with a TEAL nginx container in front of three TEAL boxes (Frontend,
    API 1, API 2). A PINK "HTTP 80" door. One TEAL box cracks RED; a small GREY phone rings, an
    "operator" figure walks in through a PINK SSH tunnel and restarts it by hand (slide 7). A clock
    reads 2:00 a.m.
  - Slide 9 re-drawn: three VMs; VM 2 holds API 1 and a backup copy, VM 3 API 2 and its copy. Ponder 1
    sits here. Then the answer animates: VM 2 itself goes dark, taking both copies; the switch to the
    backup is still a hand on a lever.
  - Slide 12's three asks appear as a checklist card, **Failover · Load balancing · Scaling**, which
    shrinks into the top-right corner and returns at S07, S13, S15 and S16 to be ticked.
  - Slide 19, the morph that answers it: the one VM packed with containers on one "Docker" bar
    (left) *transforms* into a cluster of node boxes each with its own runtime strip, the same TEAL
    trio repeated on several nodes, thin lines to one control plane (right). Caption under the left:
    "a way of deploying" — "not the `Deployment` object you'll meet in S06" (Gap 4).
- **V3 · `LabelLink` — two objects, one sticker (slide 39 made honest; S06, S08).**
  - The real `deploy-k8s-tic-tac-toe.yml` (35 lines) split in two code panels: Deployment (lines 2–22)
    and Service (24–35), bracketed as slide 39 does: GREEN bracket "Deployment: what runs in a Pod, how
    many copies, keep them running"; PINK bracket "Service: how traffic reaches them; lets Pods die".
  - The lines slide 39 trims light up: `selector.matchLabels run: web` (9–10), the template's
    `labels run: web` (13–14), the Service's `selector run: web` (33–34). A PINK sticker `run: web`
    flies from the template onto each TEAL Pod the Deployment makes; the Service throws a PINK lasso
    around "every Pod wearing `run: web`".
  - `port: 80 → targetPort: 8080 → containerPort: 8080` drawn as a PINK path of three ports.
  - S08: the lasso becomes the endpoints list (`10.244.1.2:8080,10.244.2.2:8080`, from `k50`) and a DNS
    card `web.default.svc.cluster.local → 10.96.52.79` (`k52`): the name stays while Pods change.
- **V4 · `ControllerLoop` — desired state, kept (S07; reused in S12 for the Job, S15 for scaling).**
  - A GREEN Deployment card `web · replicas: 2` emits a GREEN ReplicaSet card `web-5cd9789488` (the
    `pod-template-hash`), which emits two TEAL Pods `web-5cd9789488-5h48s`, `-bmkj5`: the three-part
    name is drawn as three coloured segments (Deployment / ReplicaSet hash / Pod suffix).
  - The loop itself: a ring of three arrows **observe → compare → act** around the controllers box of
    V1, with a counter "desired 2 · actual 2".
  - A Pod is struck (`kubectl delete pod`), fades; the counter flips RED "desired 2 · actual 1"; a new
    Pod grows with the same middle segment and a new suffix `-lmk52` (`k53`, `k54`). Thermostat
    caption: "you set the number; the controller keeps it true".
  - `replicas: 4` (`k55`): the counter jumps, two Pods grow on the two workers; back to 2 (`k56`).
  - The **Job** cousin (S12, S15): a GREEN Job card emits one Pod that runs, turns `Completed` GREY and
    is *not* replaced; an hourglass "Pulumi waits for Complete" between the loader Job and the API card.
- **V5 · `CheeseBlueprint` — the whole cheese app on GKE (digest §1; S09, S12, S14, S16).**
  - Starts as L20's single VM (GREY dashed, from S01's memory): nginx, API, frontend, vector DB, the
    dashed loader. The VM *dissolves into* the V1 cluster and each piece finds its K8s form, one row of
    the L20 → L22 table at a time: containers → Deployments, the loader → a Job, the Docker network's
    names → Services + cluster DNS, `/mnt/disk-1` folders → two PVCs on BLUE disks, the nginx container
    → the NGINX Ingress controller + an Ingress, the `gcp-service.json` key → Workload Identity (no key),
    "restart policy" → the ReplicaSet, "one VM" → a node pool 1–2.
  - Around it: a BLUE VPC `cheese-app-vpc` with subnet `10.0.0.0/19`; nodes with their public-IP badge
    peeled off ("private nodes") and a BLUE **Cloud NAT** funnel at the VPC edge (outbound only); a
    GREEN `cheese-app-namespace` frame holding the app; the BLUE external load balancer at the door.
  - Labels from the code: `frontend :3000`, `api :9000`, `vector-db :8000`, `vector-db-loader` (Job),
    `persistent-pvc 5Gi`, `chromadb-pvc 10Gi`, `nginx-f5`, `cheese-app-ingress`.
- **V6 · `ResourceTree` — the plan grows in dependency order (S11, S12, S16).**
  - `c20`'s 23 lines become nodes of a tree, coloured by provider: BLUE gcp (Network, Subnetwork,
    Router, RouterNat, Cluster, NodePool, IAMMember), PURPLE provider/command (`gke_k8s_v2`,
    `connect-k8s-command`), GREEN kubernetes objects (Namespace, ServiceAccount, two PVCs, three
    Deployments, three Services, Job, Ingress), the Helm release `nginx-f5`; two PINK *reads* drawn as
    dashed outlines (StackReference `organization/deploy-images/dev`, `nginx-ingress-service`). A counter
    ticks to **`+ 23 to create`**.
  - S12 (illustration): the tree fills in dependency order (digest Step 7): network → cluster (the slow
    one: a GOLD-ringed clock, "15–25 min, our estimate") → node pool → provider (from a kubeconfig made
    of outputs) → namespace, KSA, IAM binding → PVCs, frontend and vector-db → **Job hourglass** → API
    → (in parallel) Helm release → its load balancer IP → the `sslip.io` host → Ingress last. On the
    real capture (`c21`), only the first BLUE node turns RED: the VPC.
  - S16: the tree empties in reverse; three ghost icons blink outside it (a forwarding rule, a `pvc-…`
    disk, the registry images with a padlock `retain_on_delete`).
- **V7 · `RequestJourney` — one click, every hop (README:457-474, slides 5, 21, 24, 26, 38; S13).**
  - The README's Mermaid diagram re-drawn left to right as lanes (no Mermaid styling): Browser → LB
    Service → NGINX Ingress Controller → Frontend Service :3000 (`/`) and API Service :9000
    (`/api-service`) → API → Vector-DB Service :8000; the loader Job with its arrow **into** the vector
    DB (the README draws it the other way: GREY ghost of the README's arrow flips around, erratum).
  - A packet glyph travels: a DNS bubble `<IP>.sslip.io → <IP>`; the BLUE load-balancer door (made by
    GKE because the controller's Service is `type: LoadBalancer` — V1's cloud-provider arrow lights);
    a node; the NGINX figure reads a two-row routing table from the Ingress (`host <IP>.sslip.io`;
    `/api-service` → `api:9000`, `/` → `frontend:3000`, `setup_loadbalancer.py:79-104`); the prefix is
    **kept** (no scissors this time, unlike L20) so the API mounts under `ROOT_PATH=/api-service`; the Pod
    answers `{"version":"3.0"}`.
  - Second packet `/` returns HTML, which *spawns* a new packet from the browser to `/api-service/…`
    (`NEXT_PUBLIC_BASE_API_URL=/api-service`, `.env.production:2`): the browser, not the frontend Pod,
    calls the API.
  - Ponder 3 here: a packet with `Host: <IP>` matches no row and bounces back with a RED 404.
  - Comparison strip: tic-tac-toe opens **one door per app** (its own LoadBalancer); the cheese app opens
    **one door with a receptionist** (one LoadBalancer, NGINX behind it; its three app Services are
    `ClusterIP`).
- **V8 · `BinPacking` — two levels of scaling (S15; slides 12, 15, 18, 39, 43).**
  - A BLUE node rectangle as a shelf of capacity ("allocatable ≈ 6 Gi of the 8 GB"), filled with blocks
    sized by their **requests**: frontend `250m / 2Gi` (fat), Chroma `100m / 128Mi`, NGINX `100m /
    128Mi`, the API with **no request** (drawn as a block with a dashed outline and a "?").
  - `kubectl scale deployment frontend --replicas=3`: two more fat blocks drop; the third doesn't fit
    and hovers RED `Pending` (the scheduler lamp of V1); a second node slides in from the right (the
    cluster autoscaler, `max_node_count=2`) and the block lands. `--replicas=5`: two blocks hover for
    good beside a RED badge `max 2 nodes`.
  - The API's BLUE disk is chained to node 1 (`ReadWriteOnce`); a second API block on node 2 reaches
    for it and a RED chain `Multi-Attach` snaps (ponder 4).
  - Two labelled levers: **Pods** (you: `kubectl scale`; an HPA would, dashed GREY: "not configured
    here, and it needs requests") and **nodes** (GKE's autoscaler, 1–2: on).

Two small helpers, not set pieces: **`AsksChecklist`** (slide 12/15's three items, top right, ticks
YELLOW; S15's Pod-level tick dashed) and **`KubectlGrammar`** (slide 27's four slots `command · TYPE ·
NAME · flags`, used in S03 and S08 where `-n cheese-app-namespace` drops into the flags slot).

## README step tracker (ReadmeTracker, top-left)

One tracker per README section, titled with the README's own heading. Steps the README does not have
are marked `extra` in the tracker caption and in the narration ("this one isn't in the README"). Step
titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **W · Create Simple Kubernetes Cluster Tutorial** | 517-581 | Enable APIs · Run toolbox · Check tools · Auth check · Create cluster · See console · Try kubectl · Deploy app · Get IP · View app · Delete cluster (11) |
| **D · Deployment with Scaling using Kubernetes** | 392-434 | Enable APIs · Run toolbox · Check tools · Auth check · Images stack · Images preview · Images up (7) |
| **C · Create & Deploy Cluster** | 436-512 | Cluster stack · Config keys · Preview · Pulumi up · Try kubectl · Shell into Pod · View app · Delete cluster (8) |
| **G · Debugging Containers (Kubernetes)** | 618-657 | Job logs · Find pod · Pod logs · API logs (4) |

Command ↔ capture map (README line → file):
- W: 519-525 → illustration; 528 `cd deployment`, 529 `sh docker-shell.sh` → `b02` (as committed),
  `b02a` (extra fix), `b03`; 531-533 → `b10`, `b11`, `b12`; 536 → `b13`; 541 → `b15` then `k01` (stand-in,
  extra); 544-549 → illustration; 553-555 → `k03`, `k04`, `k05`; 559-560 → `k06`, `k07`; 565 → `k10`;
  570 → `k11`, `k13` (+ `k12` extra); 573-575 → `k57` (extra) + illustration; 580 → `k80` (extra tip),
  `b51`, `k81` (extra).
- D: 396-402 → illustration; 405-406 → re-typed, `b03`'s prompt; 408-410 → `b10`-`b12`; 413 → `b13`;
  420-421 → `b20`, `b21` then `c00`-`c02` (extra); 428 → `b22`, `c03`; 433 → `b23` (+ L20's `b35b`, said).
- C: 440-443 → `b30`, `b31-1..3`, then `c10`, `c11-1..3`, `c12` (extra); 449 → `b32`, `c13`, `c20`; 454 →
  `b33`, `c21` (+ `c14` said); 457-474 → V7; 478-480, 484-485 → `b40`-`b44` (+ `b52` extra, and S05's `k03`-`k07`
  recalled); 490-492 → `b45`, `k20`, `k21`, `k22` (+ `k51` extra); 497-507 → `expected/`; 511 → `b50`, `c15`/`c23`.
- G: 620-656 → `k30`-`k43` (all 14, as a fast montage of four groups); the corrected commands typed with
  no output; `k60`-`k62` (extra) on a Job that exists.

S01–S03 and S09 have no tracker. S07 keeps W at "View app" with the caption `extra`. S15's scaling half
has no README step (`extra`, Milestone 5). S16's recap has none after "Delete cluster".

## Scene plan

Notation:
- `bNN`, `cNN`, `pNN` = `assets/terminal/laptop/…`; `kNN` = `assets/terminal/kind/…`; `expected/` =
  `assets/terminal/expected/`. Line 1 of a capture is the `$` command (typed, never printed); `[exit N]`
  is never printed.
- ▶ = a README step the viewer must do. A YELLOW `▶ your turn` tag appears at real checkpoints only.
- CODE(path: a-b) quotes `assets/source/` with real line numbers, ≤ 12 lines on screen.
- `lecture_ref(22, "a–b")`, GREY, top right, **only while that slide's picture or idea is on screen**.
  Slide images never appear. Story roles are "the app owner" and "the operator" (slides 4–11), never a
  person's name.

### Part 1 · Kubernetes by hand

**S01 · Who restarts it at 2 a.m.? (~230 words) — `s01_hook.py` · `Hook`.** Cold open, no tracker.
`lecture_ref(22, "4–11")`, then `(22, "12")`.
- The broken thing first: V2's single VM (slide 5) — nginx in front of a frontend and two APIs. At 2:00
  a.m. one API container dies. Who notices? The app owner, when users complain. Who fixes it? The
  operator, over SSH, by hand (slide 7). "In L20 you were that operator: one stopped container took the
  whole site down, and you restarted it yourself."
- Slide 8's request: "put it on several servers". Slide 9 re-drawn: three VMs, a backup copy beside each
  API.
- **PONDER 1 (8 s):** "Each backup sits on the same VM as its original. Name one failure that still takes
  that API down, and say who switches to the backup." Answer: the VM itself (its disk, its network) takes
  both copies; and a human still pulls the lever (slide 11).
- Slide 12: what we want automated is three things — failover, load balancing, scaling. The
  `AsksChecklist` card appears and shrinks top-right. "Today's tool for all three: Kubernetes."

**S02 · From one box to a fleet (~250) — `s02_orchestrator.py` · `Orchestrator`.** No tracker.
`lecture_ref(22, "17–19")`, then `(22, "21–22")`.
- Slide 17 in one sentence: an orchestrator for containers across a cluster of machines; the name is
  Greek for helmsman (the ship's wheel; Helm, the chart tool in Part 2, borrows it). No logo.
- Slide 19 as V2's morph: one Docker host → many nodes, each with its own runtime, the same app copied
  across nodes, one control plane coordinating. The word warning: "Kubernetes deployment" here means a
  way of deploying; the `Deployment` object is something else (S06).
- Slides 21–22: L20's cheese app on one VM (V5's opening frame, GREY dashed) → the same laptop, aimed at a
  cluster; the CLI list gains `kubectl`. "Same toolbox as L20; the tools are already inside it, plus two the
  slides don't list: Helm and the GKE auth plugin."
- How to follow along: one repo, cheese-app-v3, `secrets/` next to it; Docker Desktop; a GCP project with
  billing (GOLD: a cluster costs money by the hour; each part ends with a delete). The README tracker
  top-left, code panels with path and lines, `▶ your turn`; the study guide has every command. The
  sandbox sentence (see "Running example"), said here once. Which commit: `main` at `3ecef56`; `git log
  -1` tells you yours (`p02`, extra).
- Map of the video: Part 1, the lecture's warm-up by hand; Part 2, the cheese app as code.

**S03 · Inside a cluster: brain and workers (~300) — `s03_anatomy.py` · `ClusterAnatomy`.** No tracker.
`lecture_ref(22, "22–26")`, then `(22, "27")`.
- V1 in the deck's three beats (22 → 23 → 24), then the callouts of slides 25–26, one per component,
  in the lecture's words (see V1).
- GKE's two amendments, said kindly: Google runs the control plane — you talk to it, you never see its
  machines (the slides' "master nodes"); and the runtime is `containerd`, not Docker (`create_cluster.py:52`
  `cos_containerd`, CODE line only) — images you build with Docker run unchanged.
- Every arrow starts at the API server: "kubectl talks to exactly one thing". The `KubectlGrammar` card
  (slide 27): `kubectl get pods`, `kubectl delete pod web-…`, `kubectl get svc -n …` slot into
  command · TYPE · NAME · flags.
- One line that seeds later scenes: "When something is stuck, ask which of these parts is waiting." The
  four symptom lamps blink once, unlabelled, to be named in S06, S07, S14 and S15.

**S04 · The toolbox, still fixed twice (~260) — `s04_toolbox.py` · `Toolbox`.** Tracker W 1–4.
`lecture_ref(22, "32, 34")`.
- The section-order sentence (see top). ▶ W1 Enable APIs as an `illustration` (README:521-525): Compute
  Engine, Service Usage, Cloud Resource Manager, Kubernetes Engine; "Google Container Registry API"
  (524) crossed GREY: it has been shut down, enable **Artifact Registry API** instead (erratum).
- ▶ W2 `cd deployment` (= `src/deployment`), `sh docker-shell.sh` (`b02`, in a terminal): `Building …`,
  `ERROR [ 2/16] RUN apt-get update && apt-get install -y curl …`, two of the 22 `404 Not Found` lines
  (proxy column cropped), `ERROR: failed to build`, `pull access denied`. "If you did L20, you have seen
  this: the same two one-line fixes." `docker-shell.bat` (529) does not exist: on Windows use WSL.
- Extra `b02a`: the `git diff`, both fixes highlighted RED → GREEN (`bullseye` → `bookworm`;
  `google-cloud-sdk` → `google-cloud-cli`, with its `-gke-gcloud-auth-plugin` — "this one is the plugin every
  GKE kubectl call will use").
- ▶ `b03`: `[+] Building 92.3s (21/21) FINISHED`, then the entrypoint, trimmed: `Container is
  running!!!`, `invalid_grant … account not found`, `could not log in to the state backend` — "with
  your key, these say Activated and Logged in". `▶ your turn`.
- ▶ W3 `b10` (first and last lines: `Google Cloud SDK 592.0.0`, `gke-gcloud-auth-plugin`, `kubectl
  1.35.9`), `b11` (`The connection to the server localhost:8080 was refused`: harmless, there is no
  cluster yet — the server half of `version` has nobody to ask), `b12` `Client Version:
  v1.35.9-dispatcher`. Kindly: the Dockerfile pins 1.34, but Google's own `kubectl` package wins; it is
  a dispatcher that picks a client to match your cluster (S05 shows it picking 1.34).
- ▶ W4 `b13` `No credentialed accounts.` → "yours lists `deployment@<your project>` as active".

**S05 · A test cluster and a first look (~270) — `s05_test_cluster.py` · `TestCluster`.** Tracker W 5–7.
`lecture_ref(22, "32–33")`, then `(22, "35–37")`.
- ▶ W5 `gcloud container clusters create test-cluster --num-nodes 2 --zone us-east1-c` → `b15` (RED: no
  active account). What yours does: a few minutes, a cluster table, and a kubeconfig entry written for
  you (slide 33's "kubeconfig entry generated"). The slide makes one node; the README two, so the two
  tic-tac-toe Pods can land on different machines. GOLD tag: "billed per node-hour while it exists".
- The stand-in sentence. `k01` (extra, stand-in): `Creating cluster "test-cluster" ...`, the ✓ lines,
  `Set kubectl context to "kind-test-cluster"` (patch block cropped). V1 lights: one control plane +
  two workers, on the laptop (GREY dashed outline).
- ▶ W6 See console: an `illustration` of slide 37's view, schematic and unbranded — Kubernetes clusters →
  `test-cluster` → Nodes → Pods; Compute Engine → the node VMs (README:545-549). "Your nodes are ordinary
  VMs: you'll find them in Compute Engine."
- ▶ W7 `k02` `Client Version: v1.34.12-gke…`, `Server Version: v1.34.11` (the dispatcher matched).
  `k03` `kubectl get all` → only `service/kubernetes` (ORANGE): "you're in the `default` namespace; S08
  explains". `k04`/`k05` first lines: `kube-system` Pods — on the stand-in you can see the control
  plane's own Pods (etcd, kube-apiserver, kube-scheduler, kube-controller-manager: V1's boxes, by name);
  on GKE they're hidden, and you see Google's node agents instead. `k06`: the deprecation warning, three
  `Healthy` rows ("expected; check health with `get nodes`"). `k07`: three nodes `Ready`, one
  `control-plane` ("on GKE: two workers, no control plane in the list"). `▶ your turn`.

**S06 · Two objects: a Deployment and a Service (~270) — `s06_tic_tac_toe.py` · `TicTacToe`.** Tracker
W 8–10. `lecture_ref(22, "38–39")`, then `(22, "24–25")`.
- V3: the real YAML. Kindly: the slide trims it to its two jobs; the trimmed lines are the glue.
  CODE(`src/deployment/deploy-k8s-tic-tac-toe.yml`: 2-22) then (24-35).
- ▶ W8 `kubectl apply -f deploy-k8s-tic-tac-toe.yml` → `k10` `deployment.apps/web created`, `service/web
  created`. "apply sends a wish to the API server; nothing has run yet" — V1: the API server writes it to
  etcd, the scheduler picks two nodes, two kubelets start the containers. Extra `k12`: `rollout status`
  0 → 2 of 2, the two Pods on **different workers**.
- ▶ W9 `kubectl get services` → `k11`: `web LoadBalancer 10.96.52.79 <pending> 80:31366/TCP`. The port
  mapping read once: 80 outside, 31366 on every node, 8080 in the container.
- **PONDER 2 (8 s):** "43 seconds later it still says `<pending>` (`k13`). Which part of the cluster
  picture is waiting, and on what?" Answer: the controllers, on the cloud provider API — on GKE they ask
  Google for a load balancer and an IP in a minute or two; kind has no cloud to ask. V1's cloud arrow
  goes RED on the stand-in.
- ▶ W10 View app: on GKE, `http://<EXTERNAL-IP>` shows the game (`illustration`, schematic browser, no
  real IP). On the stand-in (extra) `k57`: `kubectl port-forward service/web 8080:80` → `HTTP/1.1 200 OK`,
  `<!DOCTYPE html>`. Kindly (slide 29): in the course, kubectl runs inside the toolbox container, which
  publishes no ports — a port-forward opens inside that container, so test it with `curl` there.

**S07 · Desired state: Pods that come back (~260) — `s07_self_healing.py` · `SelfHealing`.** Tracker W
10 (`extra`). `lecture_ref(22, "7, 18, 30, 36, 39")`.
- Slide 7's "restart the container" becomes a controller's job. V4 with `k50`: `deployment.apps/web`
  → `replicaset.apps/web-5cd9789488` → `pod/web-5cd9789488-5h48s`, `-bmkj5`; the hash is the
  `pod-template-hash` label (`--show-labels`). Slide 36's Pod names carry the same shape.
- **PONDER 3 (8 s):** "You delete one of the two web Pods. A second later, how many web Pods are there,
  and which part of the new one's name stays the same?" Answer `k53`: `pod "web-5cd9789488-5h48s"
  deleted`, and already `web-5cd9789488-lmk52 0/1 ContainerCreating 1s`; `k54` 15 s later both
  `Running`. Two Pods; same ReplicaSet hash, new suffix. The loop: observe → compare → act.
- Tick **Failover** on the checklist, with its honest footnote: "a restart, not a hot standby — with one
  replica there's a short gap; slide 13's twins need `replicas: 2`".
- Extras `k55`/`k56`: `kubectl scale deployment web --replicas=4` → four Pods spread over both workers,
  `endpoints web … + 1 more`; back to 2. "Hold on to `scale`: Milestone 5 asks for it (S15)."
- Slide 18/30: "declare, don't script" — you set the number; Kubernetes keeps it true. Contrast in one
  line: L20's Docker restart policy restarted a container on the same machine; a ReplicaSet places a new
  Pod wherever there is room.

**S08 · Labels, Services, namespaces — then delete (~230) — `s08_stable_names.py` · `StableNames`.**
Tracker W 11 (after extras). `lecture_ref(22, "27–29, 35, 39")`, then `(22, "40, 44")`.
- Pods are mortal: the new Pod got a new IP (`10.244.1.7` vs `.2`, `k54`). V3's lasso → `k50`'s
  `endpoints/web 10.244.1.2:8080,10.244.2.2:8080`; extra `k52`: from a throwaway Pod,
  `web.default.svc.cluster.local` → `10.96.52.79` (the Service's cluster IP) and the game's `<title>`.
  The name stays; the Pods behind it change. This is how the cheese app's API finds `vector-db` (S12).
- Extra `k51`: `kubectl exec --stdin --tty deployment/web -- /bin/sh` → `hostname` prints a Pod name:
  README:492's mechanism, which S14 uses.
- Namespaces, the reason `get all` looked empty: extra `k63` — `default`, `kube-system`, … ; a folder
  for objects; `kubectl` looks in `default` unless you pass `-n`. The `KubectlGrammar` card: `-n
  cheese-app-namespace` drops into the flags slot.
- ▶ W11 Delete: extra tip first, `k80` `kubectl delete -f …` → `deployment.apps "web" deleted`,
  `service "web" deleted` ("on GKE this releases the load balancer while the cluster still exists").
  ▶ `gcloud container clusters delete test-cluster --zone us-east1-c` → `b51` (RED, no account); yours
  asks `Do you want to continue (Y/n)?` (said). Extra `k81` the stand-in deleted. GOLD card "Don't forget
  to delete" (slide 44's message, no meme); the meter stops. Empty frame: end of Part 1.

### Part 2 · The cheese app as code

**S09 · The cheese app's cluster, as code (~250) — `s09_blueprint.py` · `Blueprint`.** No tracker.
`lecture_ref(22, "21–22, 41")`.
- Slide 41's handover in our words: now the cheese app, as Pulumi code. Kindly: the course link lands on
  "Deployment with Scaling using Kubernetes"; the cluster steps continue under the next heading, "Create
  & Deploy Cluster" — the tracker shows both (erratum 14).
- V5: L20's VM dissolves into the cluster, row by row (see V5). One cluster for the whole app (slide
  13's three clusters were for the demo's picture), one namespace, private nodes with Cloud NAT.
- CODE(`src/deployment/deploy_k8s/__main__.py`: 19-40): four calls — network, cluster, containers,
  load balancer — the four files of `deploy_k8s/`; `setupSSL = False` (17): the HTTPS variant is off.
- GOLD: what runs while it's up — the regional cluster's management fee, 1–2 `n2d-standard-2` nodes, a
  load balancer, a NAT gateway, two disks: "roughly five to eight dollars a day, by our estimate: check
  the pricing calculator, and destroy the same day". Registry images outlive `destroy` (S16).

**S10 · Setup and the images stack (~280) — `s10_images.py` · `ImagesStack`.** Tracker D 1–7.
`lecture_ref(22, "21–22")`.
- ▶ D1 Enable APIs `illustration` (README:398-402): the five, plus **Vertex AI API**, which the API Pods
  call (digest §2).
- Setup the README leaves out, as `illustration`s (digest §2): the two service accounts from L20
  (README:236-259: `deployment` for everything the toolbox does — and, here, the nodes' identity;
  `gcp-service` for the API Pods, **no key file needed** in the cluster); the extra role the README's list
  very likely misses (Pulumi must write an IAM policy on `gcp-service`: grant `deployment` Service Account
  Admin on it — "we couldn't run this; it follows from the documented roles"); the Artifact Registry
  repository `cheese-app-repository`, which no code creates. `p05` shows where `deployment.json` goes.
- ▶ D2–D4 the same toolbox commands again, fast (README:405-413; outputs `b10`-`b13`); "if the toolbox is
  still running, `docker-shell.sh` just attaches".
- ▶ D5 `cd deploy_images`, `pulumi stack init dev`, `pulumi config set gcp:project ac215-project --stack
  dev` → `b20`, `b21`: `PULUMI_ACCESS_TOKEN must be set …` (RED): "the toolbox couldn't log into your
  state bucket (S04), so Pulumi has no backend; with your key these print `Created stack 'dev'`". The
  local-backend sentence; extras `c00`–`c02`: `Created stack 'dev'`.
- ▶ D6 `pulumi preview --stack dev` → `b22`, then `c03` (extra): three `+ … Image build-cheese-app-…
  create`, `Skipping preview build`, three `…-tags` with a timestamp, `+ 4 to create`. V5's three images
  flow to Artifact Registry; the `-tags` outputs are what `deploy_k8s` reads through a `StackReference`.
- ▶ D7 `pulumi up --stack dev -y` → `b23` (RED). "This builds three images, the API one about five
  gigabytes; L20 showed that build to its push. **Skip it if you did it in L20**" (README:416), and that
  "skip" has a condition S11 makes visible. `▶ your turn`.

**S11 · deploy_k8s: config and a 23-resource plan (~270) — `s11_plan.py` · `ClusterPlan`.** Tracker C
1–3. `lecture_ref(22, "41")`.
- ▶ C1–C2 `cd ../deploy_k8s` (README 437's "from the `deployment` folder"), the four commands (README:440-443)
  → `b30`, `b31-1..3` (the same RED line), then extras `c10`, `c11-1..3`. GREY tag "the README's default
  · change to yours" on every `ac215-project`. What the two `security:` keys feed: the nodes' service
  account and the Workload Identity binding (CODE `create_cluster.py`: 9-12, ≤ 4 lines). Extra `c12`
  `pulumi config`: your three keys plus two leftovers from the committed file, `setupSSL` and
  `security:ssh_user sa_000…` (masked): unused, harmless. A typo here fails silently later (`get()`
  returns `None`): check with `pulumi config`.
- ▶ C3 `pulumi preview --stack dev --refresh` → `b32` (RED), then extra `c13`: `setup_containers.py",
  line 70`, `lambda tags: tags[0]`, **`TypeError: 'NoneType' object is not subscriptable`**. Kindly: this is
  what you see if you skip the images stack, or ran it into a different bucket — `deploy_k8s` reads the
  image tags from `organization/deploy-images/dev` in the same backend. CODE(`setup_containers.py`: 68-71).
- With the stand-in image stack (said on screen: "placeholder image tags, nothing built"), extra `c20`:
  V6 grows from the real lines to **`+ 23 to create`**; `Outputs:` — only `cluster_name:
  "cheese-app-cluster"` is known; `app_url`, `ip_address` … are `[unknown]` until the cluster exists.
  `▶ your turn` (your preview should show the same 23, with real tags).

**S12 · pulumi up: what builds, in what order (~280) — `s12_pulumi_up.py` · `PulumiUp`.** Tracker C 4.
`lecture_ref(22, "24–25, 33")`.
- ▶ C4 `pulumi up --stack dev --refresh -y` → `b33` (RED); extra `c21`: the preview again, then
  `Updating (dev)` and **`gcp:compute:Network cheese-app-vpc creating failed`** … `invalid_grant` (tracebacks
  cropped): "the VPC is the first thing that needs Google; everything after this is a picture, not a
  recording". `▶ your turn` (GOLD: from here the meter runs).
- V6 as an `illustration` of the dependency order (digest Step 7), with V1/V5 lamps: network and NAT;
  the cluster (the long wait, "15 to 25 minutes, our estimate"); the node pool; a kubeconfig built from
  the cluster's outputs → the Kubernetes provider (`depends_on` the node pool, so no Pod is created
  before there are nodes); the namespace, the KSA and its IAM binding; PVCs, frontend, vector-db; the
  loader **Job** and V4's hourglass — Pulumi waits for *Complete*, and only then creates the API (CODE
  `setup_containers.py`: 319-321, the API's `depends_on=[vector_db_loader_job]`); in parallel Helm installs the
  NGINX controller, whose LoadBalancer Service makes the controllers ask the cloud provider API for an
  IP (V1's arrow, this time GREEN); the Ingress last.
- Identity in two beats (digest §3.7, ≤ 70 words): kubectl and Pulumi reach the API server with a
  kubeconfig whose user is the `gke-gcloud-auth-plugin` (fix 2 from S04) — no cluster password; and the
  API Pod wears a Kubernetes service account `api-ksa` that Workload Identity swaps for `gcp-service` at the
  door to Vertex AI — no JSON key inside the cluster.
- One thing to keep (erratum 12): Pulumi runs `get-credentials` once, at create, in this `--rm` container;
  the next session forgets it (S14).

**S13 · The journey of one click (~290) — `s13_one_click.py` · `OneClick`.** Tracker C 4 → (Mermaid,
README:457-474). `lecture_ref(22, "5, 21, 38–39")`, then `(22, "24, 26")`.
- What students know first: L20's nginx container in front (slides 5, 21). Slide 38's tic-tac-toe opened
  one door per app; the cheese app opens one door with a receptionist (V7's comparison strip).
- V7 in full on the README's own diagram (re-drawn). Helm installs the receptionist (the helmsman again,
  one clause). CODE(`setup_loadbalancer.py`: 79-91, then 96-104): the host rule and the two paths.
  The Ingress is only a rule object; the NGINX controller reads it and does the work — L20's `nginx.conf`,
  now generated.
- The prefix is kept, so the API lives under `ROOT_PATH=/api-service` (CODE `src/api-service/api/service.py`: 13, 50);
  the browser makes the API calls (`.env.production`: 2). The API reaches Chroma by the Service name
  `vector-db:8000` (S08's DNS). Kindly: the README's dotted arrow points from the vector DB to the loader;
  the data flows from the Job into the DB.
- **PONDER 4 (8 s):** "You open `http://<IP>/` — the same load balancer, without `.sslip.io`. What
  answers?" Answer: NGINX's 404: the Ingress rule only matches `Host: <IP>.sslip.io`; same door, wrong
  name on the booking. Use `app_url`.
- Tick **Load balancing**: the cloud's load balancer at the door, NGINX across the Pods behind each Service.

**S14 · kubectl on the app, and the outputs (~290) — `s14_explore.py` · `ExploreApp`.** Tracker C 5–7.
`lecture_ref(22, "34–37")`.
- ▶ C5 the five commands of README:478-485 → `b40`-`b44` montage: five × `connection refused` to
  localhost:8080. "On the recording day there was no cluster. You'll see exactly this in any *new* toolbox
  session: the kubeconfig Pulumi wrote died with the old container." The fix, typed (extra `b52`, RED no
  account): `gcloud container clusters get-credentials cheese-app-cluster --region us-central1 --project
  <your project>` — kindly, the code passes the region to `--zone`; `--region` says what it means.
- What yours shows, **described, no output panel**: `get all` again only `service/kubernetes`; with `-n
  cheese-app-namespace`, Pods `frontend-…`, `vector-db-…`, `api-…`, the NGINX controller, a
  `vector-db-loader-…` Pod `Completed`, `job.batch/vector-db-loader 1/1`; `get nodes` one node (two if the
  autoscaler added one). On S05's stand-in we saw what these commands look like (recall `k03`/`k07`
  thumbnails, tagged stand-in).
- ▶ C6 README:490-492: `b45` (refused), then on the stand-in `k20` `No resources found in cheese-app-namespace
  namespace.`, `k21`/`k22` `namespaces "cheese-app-namespace" not found` — "`api-c4fb784b-2llgs` is the
  README author's Pod; use the name from your first command". S08's `k51` reminds what `exec` gives you;
  inside the API Pod try `env | grep ROOT_PATH` (said). `▶ your turn`.
- ▶ C7 View app: `expected/readme-pulumi-outputs.txt` (tagged `expected`) beside the code's export names
  (CODE `__main__.py`: 43-49): kindly, the README's block is older — `ip_address`, not `nginx_ingress_ip`;
  `cheese-app-ingress`, not `nginx-ingress` (`c20` printed the current keys). Then an `illustration` of the
  browser at `http://<IP>.sslip.io`: the footer's `API version: 3.0` is the whole path working
  (`Footer.jsx` → `/api-service/status`); pick the RAG model in chat to prove Vertex AI and Chroma. First
  minute 502/503: the API is still loading TensorFlow.

**S15 · Logs, then scaling at two levels (~290) — `s15_scaling.py` · `LogsAndScaling`.** Tracker G 1–4,
then `extra`. `lecture_ref(22, "12, 15, 18, 39, 43")`.
- ▶ G1–G4 the debugging block (README:620-656), all fourteen, as a fast montage in four groups (`k30`–`k43`):
  `namespaces "cheese-app-cluster-namespace" not found`, and the `<pod-name>` lines as shell errors
  (`syntax error near unexpected token 'newline'`). Kindly, two fixes: the namespace is
  `cheese-app-namespace`, and the Job has one container (drop `-c wait-for-chromadb`); replace
  `<pod-name>` entirely, brackets included. The corrected trio typed, no output: `kubectl logs -n
  cheese-app-namespace job/vector-db-loader`, `kubectl describe job vector-db-loader -n cheese-app-namespace`,
  `kubectl logs deployment/api -n cheese-app-namespace -f`. Extras `k60`–`k62` show the same commands on a
  Job that exists on the stand-in: `loading...`, `done`, `1 Succeeded`. Disk erratum, one line: today's
  Chroma writes to `/data`, so its PVC at `/chroma/chroma` stays empty and a vector-db restart needs the
  Job again (fix: mount `/data`).
- Scaling. Slide 18's promise (CPU, memory, custom metrics) and the honest picture: the README's title says
  scaling, but the code has no `replicas` and no autoscaler for Pods (erratum 3); it switches on the node
  layer (CODE `create_cluster.py`: 63-66). V8 with the frontend's request (CODE `setup_containers.py`:
  79-82): `kubectl scale deployment frontend --replicas=3 -n cheese-app-namespace` (typed, extra, no output;
  the stand-in's `k55` recalled as the shape) → `Pending` → node #2 → fits; `--replicas=5` → `max 2`.
  Slide 39's `replicas: 2` vs the cheese app's missing field; slide 43's "better utilization" is this
  packing.
- **PONDER 5 (10 s):** "Now scale `api` to 3. Some Pods land on the second node. What happens to them, and
  can the autoscaler fix it?" Answer: stuck `ContainerCreating` with `Multi-Attach`: the API's disk is
  ReadWriteOnce and attached to node 1; more nodes don't help — the limit is the disk. The frontend
  (no disk) scales; the parts with disks need other storage.
- Tick **Scaling**: the node level solid, the Pod level dashed ("available, yours to turn: `kubectl
  scale` for the milestone; an HPA needs requests, and the API has none"). Scale back to 1.

**S16 · Destroy, audit, recap (~260) — `s16_recap.py` · `Recap`.** Tracker C 8. `lecture_ref(22, "40,
44")`, then `(22, "15, 20, 30, 43")`.
- ▶ C8 `pulumi destroy --stack dev --refresh -y` → `b50` (RED); extra `c23` on the local backend (`- 1
  deleted`). V6 empties in reverse: Ingress and Helm release → app objects → namespace → node pool →
  cluster → NAT → VPC. GOLD audit card (digest §2, our suggestions, typed, no output):
  `gcloud container clusters list`, `gcloud compute forwarding-rules list`, `gcloud compute disks list`
  (look for `pvc-…`); load balancers and disks are deleted asynchronously and can be orphaned; registry
  images stay (`retain_on_delete`) — delete them in the console; L20's VM if still up. "Don't forget to
  delete" (slide 44's message). `▶ your turn`.
- Content recap: the checklist returns with what did each job in the cheese app — failover: the
  ReplicaSet (and node auto-repair); load balancing: the cloud LB + NGINX Ingress + Services; scaling:
  the node autoscaler, and `kubectl scale` in your hands. Slide 43's five payoffs as five short lines,
  each tied to a scene: self-service (one `pulumi up`), lower cost (packing by requests, S15), automatic
  adjustment (node autoscaler), smooth running (self-healing, S07), simpler development (the same images
  as L20).
- Recap questions (five, one at a time; answers in `exercises.md`):
  1. Which control-plane part decides where a new Pod runs, and which notices that a Pod died?
  2. Why does `kubectl get all` show only `service/kubernetes`, and what flag fixes it?
  3. How does the `web` Service know which Pods are its own, and why does the API reach Chroma at
     `vector-db:8000`?
  4. Trace one click from `<IP>.sslip.io` to the API Pod; why does the bare IP give a 404?
  5. Why can the frontend scale to three but the API cannot, and what does the autoscaler add?
- Next: L23 runs the same two `pulumi up`s from GitHub Actions on every merge. Point to the study guide
  and exercises in MLOps_Learning. Empty frame.

## Ponder questions (5, timed, each answerable at that point)

| # | scene | question | answer (said after the timer) |
| --- | --- | --- | --- |
| 1 | S01 (8 s) | Each backup sits on the same VM as its original. Name one failure that still takes that API down, and who switches to the backup? | the VM itself (disk, network) takes both copies; a human still switches (slide 11) |
| 2 | S06 (8 s) | `EXTERNAL-IP` still `<pending>` after 43 s. Which part of the cluster is waiting, and on what? | the controllers, on the cloud provider API; kind has no cloud, GKE answers in 1–2 min |
| 3 | S07 (8 s) | Delete one of two web Pods: how many a second later, and which part of the new name stays? | two (one `ContainerCreating`); `web-5cd9789488-` stays, the suffix is new (`k53`) |
| 4 | S13 (8 s) | `http://<IP>/` without `.sslip.io`: what answers? | NGINX's 404: the Ingress rule matches only `Host: <IP>.sslip.io` |
| 5 | S15 (10 s) | Scale `api` to 3; Pods on node 2: what happens, can the autoscaler fix it? | `Multi-Attach`, stuck `ContainerCreating`: the RWO disk is on node 1; no — the limit is the disk |

Five quiz ponders in ~32 minutes, inside the series' 3–5 (Conny confirmed this density on 2026-10-21;
REVIEW.md marks gate 3 met with that decision).

## Errata to state (kindly, with the fix)

1. **The toolbox does not build as committed** (`b02`, still on 2026-11-07) → `Dockerfile:4`
   `bullseye` → `bookworm`; `Dockerfile:30` `google-cloud-sdk…` → `google-cloud-cli
   google-cloud-cli-gke-gcloud-auth-plugin` (`b02a`, the same two edits as L20).
2. **The kubectl 1.34 pin is not the kubectl you get** (`b12`): gcloud's dispatcher, `v1.35.9`, picks a
   matching client per cluster (`k02`). Harmless.
3. **`kubectl version` before a cluster** (README:409/532) → `connection refused` (`b11`): expected; use
   `--client`.
4. **"Google Container Registry API"** (README:524) is obsolete → Artifact Registry API; "GCR" in the
   heading (415) → the code pushes to Artifact Registry.
5. **`docker-shell.bat`** (README:529) does not exist → WSL.
6. **Missing setup** (digest §2): the Artifact Registry repository is never created; the `deployment`
   account very likely lacks the right to write the Workload Identity binding → the two one-time fixes,
   flagged as unverified here; Vertex AI API on.
7. **`deploy_k8s` needs `deploy_images` in the same backend** (`c13`: `TypeError … tags[0]`) → "skip if
   done" means done into this state bucket.
8. **The Outputs block is older than the code** (`expected/` vs `c20`): `ip_address`, `cheese-app-ingress`.
9. **The Mermaid arrow** (README:466) points from the vector DB to the loader → the Job loads into the DB.
10. **The kubeconfig does not survive the session** (`b40`–`b44`), and the code passes the region to
    `--zone` → `get-credentials cheese-app-cluster --region us-central1 --project <yours>`.
11. **The debugging block uses old names** (`k30`–`k43`): `cheese-app-cluster-namespace`,
    `wait-for-chromadb`, `<pod-name>` → `cheese-app-namespace`, one container, your Pod's name.
12. **No scaling step despite the title** (README:392) → `kubectl scale` (Milestone 5); no HPA, no requests
    on the API.
13. **Chroma's data path** (digest §6.14): today's image writes to `/data`, the PVC is at `/chroma/chroma` →
    mount `/data`.
14. **The course link lands on the first heading**; the cluster steps are under "Create & Deploy Cluster".
15. Leftover config keys (`c12`: `setupSSL`, `security:ssh_user`) are unused → ignore; never show the number.

Slide points, said as kindly as the README's: the node runtime is containerd, not Docker (slide 26); GKE
hides the control plane (slides 23, 36); one cluster, not three (slide 13); slide 39's YAML is abridged
(the label glue); `componentstatuses` is deprecated (slide 35); the README's warm-up makes 2 nodes where
slide 32 makes 1; a port-forward from the toolbox stays inside the toolbox (slide 29); slide 21's
vector-DB port is 8000, not 5432 (drawn correctly, not mentioned unless the slide's picture is on screen).

## Costs and teardown

- **Warm-up (S05–S08):** a zonal 2-node cluster — GOLD "billed per node-hour while it exists"; deleted in
  S08 (`kubectl delete -f` first, then `gcloud … delete`).
- **Cheese app (S12–S16):** the GOLD meter starts at `pulumi up` (S12) and lists, from the digest's table
  (approximate, "check the pricing calculator"): the regional cluster's management fee (≈ $0.10/h; the
  free-tier credit covers zonal or Autopilot clusters only), 1–2 `n2d-standard-2` nodes, the load
  balancer, Cloud NAT, two persistent disks; **≈ $5–8 per day**. Destroy the same day.
- **What `destroy` does not remove:** Artifact Registry images (`retain_on_delete`), the state bucket, L20's
  VM if still running, and anything orphaned by asynchronous deletion (forwarding rules, `pvc-…` disks,
  firewall rules) → S16's audit commands.
- Part 1 ends with the test cluster deleted; Part 2 with `destroy` and the audit.

## Things never to do

Series list:
- No slide images, PDF pages, the deck's memes or photos in a frame or a repository (re-draw the idea,
  cite the slide number); no live demo links from slides 6, 10, 14.
- No Google/GCP or Kubernetes logos (no ship's wheel), no console screenshots (schematic drawings tagged
  `illustration`).
- No real person's name on screen or in subtitles: the instructor is `‹instructor›` (e.g. in
  `src/vector-db/cli.py:75, 440` if ever quoted); the story's roles are "the app owner" and "the
  operator"; the prompt user is `student`. No staff names.
- No hand-typed "output": every terminal panel comes from `assets/terminal/`.
- No command spelled differently from the README (`ac215-project` stays in README commands, with its
  GREY tag; the viewer is told to change it).
- No credentials, keys, tokens, project ids, account numbers or public IPs that look real.

Lecture-specific:
- Never name or show the unmerged staff branch (`work/‹staff›` in committed text only); crop `p03`.
- Never show the `sa_…` number unmasked (`c12`, `Pulumi.dev.yaml:4`) or the `NEXTAUTH_SECRET` line's
  value.
- Never show the README's sample IP addresses (README:499, 500, 505): use `expected/`'s `<IP>`.
- Never present the kind stand-in as GKE: every `kind/` panel carries `stand-in: kind, not GKE`; never call
  kind's control-plane node something you'd see on GKE.
- Never fake GKE's create table, a `pulumi up` progress log, the real Outputs, the cheese-app Pod listings
  or the app's pages: those are `illustration`s or descriptions, said as "yours shows …".
- Never show `c20`/`c21` without "placeholder image tags" on screen.
- Never say the nodes run Docker, that kubectl creates clusters, or that the cheese app scales its Pods by
  itself.
- Never leave `[IP: 172.17.0.1 …]` (`b02`), kind's `containerdConfigPatches` (`k01`) or `c21`'s Python
  tracebacks in a frame.
