# AC215 · Lecture 22 — Scaling: Kubernetes in the cloud (the cheese app on GKE)

A follow-along walkthrough of the Lecture 22 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Scaling: Kubernetes (cloud)*:
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3), branch `main` @
[`3ecef56`](https://github.com/dlops-io/cheese-app-v3/tree/3ecef56fea879ac480d260c0906cd95baf05179a)
(2025-11-28, "v4->v3"), its README sections *Create Simple Kubernetes Cluster Tutorial* (README:517–581,
done first, as the lecture does), *Deployment with Scaling using Kubernetes* (README:392–434), *Create &
Deploy Cluster* (README:436–512) and the Kubernetes half of *Debugging Containers* (README:618–657).

**Which commit.** The course page links the repository's default branch, unpinned. On the recording day,
2026-11-07, `git ls-remote` still gave `main` = `3ecef56` (`laptop/p03`), the same commit as Lecture 20's
video, so the video follows that README. The branches `cluster-updates` and `pipenv` are used for
comparison only. Check `git log -1` in your clone: if `main` has moved, parts of this video may no longer
match the README you open. Details in [`ASSETS.md`](ASSETS.md), "Which commit".

At two in the morning, one container of a one-VM app crashes: who restarts it? The video answers with
the lecture's three asks (failover, load balancing, scaling) and shows what in Kubernetes does each job.
Part 1 is the lecture's warm-up by hand: a cluster's parts (the control plane's API server, etcd,
scheduler and controllers; the workers' kubelet, kube-proxy and containerd), the deployment toolbox (which
still needs two one-line fixes to build), a test cluster, kubectl, and the tic-tac-toe game as a
Deployment and a Service: labels, a Pod that comes back by itself, cluster DNS, namespaces, then delete.
Part 2 deploys the cheese app to GKE as Pulumi code: the images stack, `deploy_k8s` and its 23-resource
plan, the order `pulumi up` builds in, one click traced from `<IP>.sslip.io` to the API Pod, kubectl on
the app, logs, scaling at two levels, then `destroy` and an audit of what survives.

Watch it with your own clone of cheese-app-v3 next to a `secrets/` folder, Docker running and a GCP
project with billing, and pause at every `▶ your turn` to run the command. **This lecture creates
billable resources**: a test cluster with two nodes (part 1), then a regional GKE cluster with one or two
nodes, a load balancer, a Cloud NAT gateway and two disks (part 2, roughly five to eight dollars a day by
our estimate); a GOLD tag marks each place, and each part ends by deleting what it made. The tracker top
left shows the README step; a gray `extra` tag marks a command that isn't in the README, and a gray
"Lecture 22 · slides …" tag top right points to the lecture slides the scene stands on.

The terminal sessions were recorded on 2026-11-07 on a fresh Docker 29.8.2 engine standing in for your
laptop, with the deployment toolbox built from `src/deployment/` (Google Cloud SDK 592.0.0, kubectl as
gcloud's dispatcher, Helm v3.22.1, Pulumi v3.274.1, Python 3.13.18). That machine had **no Google
account and no credentials**. Everything that runs on a machine you own ran live: the toolbox's build
(and its failure as committed), every tool check, and every gcloud, Pulumi and kubectl command of the
README, each shown up to its honest first error (`You do not currently have an active account selected`,
`PULUMI_ACCESS_TOKEN must be set`, `invalid_grant: account not found`); the video says what yours prints.
Pulumi also ran on its local file backend, tagged `extra · not for you`, up to the real 23-resource plan
(with placeholder image tags) and its first Google call. The README's kubectl commands ran verbatim
against a **stand-in cluster** on the laptop, kind v0.31.0 with Kubernetes v1.34.11, labelled `stand-in:
kind, not GKE` on every panel. The console, the browser, a successful `pulumi up` and the teardown are
schematic drawings tagged `illustration`; the README's own `Outputs:` block is the one `expected` panel.
Project IDs and `sa_…` users on screen are placeholders. Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L22-kubernetes-cloud.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L22-kubernetes-cloud.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l22-kubernetes-cloud.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, 30:26.3 (1826.3 s). Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l22-kubernetes-cloud.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l22-kubernetes-cloud_part1.mp4` | part 1, 14:19.7 (859.7 s): Kubernetes by hand — the cluster, its parts and a test deployment (S01–S08). Release asset, not in Git |
| `output/ac215-l22-kubernetes-cloud_part2.mp4` | part 2, 16:06.7 (966.7 s): the cheese app on GKE as Pulumi code — plan, traffic, scaling, teardown (S09–S16). Release asset, not in Git |
| `output/ac215-l22-kubernetes-cloud.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l22-kubernetes-cloud.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l22-kubernetes-cloud.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions, hands-on predict-then-run tasks, debugging and think questions, with answers; what was run to check them (on a second kind stand-in cluster) is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slide deck in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-07, a fresh Docker engine and the kind stand-in, no Google account); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `3ecef56` (one credential-like value left out, see ASSETS.md) |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean
video and the two part cuts) are release assets.

## Chapters

Paste-ready in `output/chapters.txt` (and `chapters_part1.txt`, `chapters_part2.txt` for the parts). Part 1 (14:20) is chapters 00:00–12:39 below; part 2 (16:07) restarts at 00:00 with "The cheese app's cluster, as code", its chapters at 00:00, 01:40, 03:33, 05:23, 07:37, 09:53, 11:40, 14:10.

```
00:00 Who restarts it at 2 a.m.?
01:29 From one box to a fleet
03:05 Inside a cluster: brain and workers
04:54 The toolbox, still fixed twice
06:54 A test cluster and a first look
08:47 Two objects: a Deployment and a Service
10:49 Desired state: Pods that come back
12:39 Labels, Services, namespaces, then delete
14:19 The cheese app's cluster, as code
15:59 Setup and the images stack
17:53 deploy_k8s: config and a 23-resource plan
19:43 pulumi up: what builds, in what order
21:57 The journey of one click
24:13 kubectl on the app, and the outputs
26:00 Logs, then scaling at two levels
28:29 Destroy, audit, recap
```

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: what still takes an API
down when its backup sits on the same VM; which part of the cluster is waiting while `EXTERNAL-IP` says
`<pending>`; how many web Pods there are a second after you delete one, and which part of the new name
stays; what answers the bare IP without `.sslip.io`; and what happens to API copies that land on a
second node. Five test-yourself questions close the video (answers in `exercises.md`).

**Part 1 · Kubernetes by hand: the cluster, its parts and a test deployment**

1. **Who restarts it at 2 a.m.?** — a small app on one VM, one crashed API container and an operator who
   logs in over SSH; lecture 20's Docker restarts a container but not the machine; three VMs with a backup
   beside each API, and why that is not enough; the lecture's three asks: failover, load balancing,
   scaling.
2. **From one box to a fleet** — Kubernetes as an orchestrator ("helmsman"; Helm borrows the name); one
   Docker engine versus nodes and a control plane; "deployment" the way of deploying versus the
   `Deployment` object; the cheese app from one VM to a cluster, with kubectl, Helm and the GKE auth plugin
   in the toolbox; what you need and what it costs; the tracker, code panels and `▶ your turn`; what the
   recording machine can and cannot show; which commit (`git log`).
3. **Inside a cluster: brain and workers** — the lecture's picture in three steps: the API server (the
   single entry point), etcd, the scheduler and the controllers, run by Google on GKE; on each worker the
   kubelet, kube-proxy and the runtime, which is containerd on GKE, not Docker (`image_type="cos_containerd"`);
   the arrows: every kubectl call goes to the API server; kubectl's grammar, `command TYPE NAME flags`.
4. **The toolbox, still fixed twice** — the README keeps the warm-up last, the lecture does it first; five
   APIs (Artifact Registry, not the retired Container Registry); `sh docker-shell.sh` fails as committed
   (Debian bullseye's security packages are gone, then `pull access denied`); the two one-line fixes,
   bookworm and `google-cloud-cli` with its GKE auth plugin; no `docker-shell.bat` (use WSL); the build,
   the login that fails without an account; tool checks: `kubectl version` refuses without a cluster,
   and the kubectl you get is gcloud's dispatcher, not the 1.34 pin; `gcloud auth list`.
5. **A test cluster and a first look** — `gcloud container clusters create test-cluster --num-nodes 2
   --zone us-east1-c` (it costs money while it exists), our honest error, and the kind stand-in with one
   control plane and two workers; the console's clusters, nodes and Pods (an illustration); `kubectl get
   all` shows only `service/kubernetes`; all namespaces, where the stand-in shows the control plane by name
   (GKE hides it); `componentstatuses` is deprecated; `get nodes`.
6. **Two objects: a Deployment and a Service** — the game's file: the Deployment (what runs, how many
   copies, keep them running) and the Service (how traffic reaches them); the `run: web` label that glues
   them, which slide 39 trims; ports 80 → 8080; `kubectl apply` hands a wish to the API server; rollout
   status on two workers; `get services` and an external IP that stays `<pending>` (the controllers wait
   on the cloud, and kind has none); viewing the game, and why a port-forward from the toolbox stays inside
   the toolbox.
7. **Desired state: Pods that come back** — Deployment → ReplicaSet (named with the Pod template's hash)
   → Pods; the controller's loop, observe → compare → act; `kubectl scale --replicas=4` and back (Milestone
   5 asks for it); delete a Pod and a new one is created at once; failover ticked, with a footnote: a
   restart, not a hot standby; declare, don't script.
8. **Labels, Services, namespaces, then delete** — Pods are mortal and change address; the Service's list
   follows the label; `web.default.svc.cluster.local` from a throwaway Pod, which is how the API will find
   `vector-db`; `kubectl exec` into a Pod; namespaces as folders, and `-n cheese-app-namespace` for part 2;
   `kubectl delete -f` first (it releases the load balancer), then delete the test cluster: don't forget
   to delete.

**Part 2 · the cheese app on GKE as Pulumi code: plan, traffic, scaling, teardown**

9. **The cheese app's cluster, as code** — the course link lands on one heading, the cluster steps sit
   under the next; lecture 20's pieces mapped: containers → Deployments, the loader → a Job, container
   names → Services with DNS names, folders → two persistent volume claims, nginx → an Ingress controller
   and an Ingress rule, the JSON key → Workload Identity, one VM → a pool of one or two nodes; a private
   network with Cloud NAT; the four calls of `deploy_k8s/__main__.py` (HTTPS off); roughly five to eight
   dollars a day.
10. **Setup and the images stack** — the APIs again, plus Vertex AI; the two service accounts (here
    `deployment` is also the nodes' identity); two one-time steps the README leaves out (Service Account
    Admin on `gcp-service`, unverified; create the registry repository); the toolbox steps again;
    `deploy_images`: `stack init`, `config set`, the backend error, Pulumi's local backend for the
    recording; the preview's three timestamp tags and `+ 4 to create`; the tags reach `deploy_k8s` through a
    stack reference; `pulumi up` builds and pushes.
11. **deploy_k8s: config and a 23-resource plan** — `stack init` and three config keys (your project,
    the two service-account emails, and where `create_cluster.py` uses them); `pulumi config` shows two
    unused leftovers, and why a typo fails quietly; the preview's Python error (`'NoneType' object is not
    subscriptable`) when the images stack never finished `up` in the same backend; with placeholder tags
    the real plan: network, cluster, node pool, the Kubernetes objects, `+ 23 to create`, two lookups, and
    outputs that stay unknown until the cluster exists.
12. **pulumi up: what builds, in what order** — the local backend stops at the network
    (`invalid_grant: account not found`); from there a picture: network and subnet, the router with NAT
    and the cluster side by side (a quarter of an hour or more), the node pool, a Kubernetes provider that
    waits for it, namespace, service account and binding, the two disks, frontend and vector DB, the
    loader Job that the API waits for, Helm's nginx Ingress controller and its load-balancer address, the
    Ingress last; identity in two parts (the GKE auth plugin, Workload Identity); Pulumi connects kubectl
    once, inside a toolbox that is removed when you exit.
13. **The journey of one click** — one door with a receptionist (versus one load balancer per app); the
    README's diagram, and its dotted arrow that points the wrong way; `<IP>.sslip.io` → the cloud load
    balancer → the nginx controller → the Ingress rule (host, then `/api-service` → api:9000, the rest →
    frontend:3000); the prefix is kept, and the API mounts itself under `ROOT_PATH`; the page, then the
    browser calls the API; the API finds Chroma as `vector-db:8000`; the bare IP answers 404; load
    balancing ticked.
14. **kubectl on the app, and the outputs** — the README's kubectl commands in a new toolbox session:
    connection refused, because the kubeconfig went with the old container; `get-credentials` with
    `--region`, not `--zone`; what yours shows with `-n cheese-app-namespace`; shell into the API Pod with
    the name your cluster prints, and look for `ROOT_PATH`; the README's outputs block is older than the
    code (`ip_address`, `cheese-app-ingress`); open the app URL: the footer's API version and a RAG reply;
    502/503 while the API still loads TensorFlow.
15. **Logs, then scaling at two levels** — the README's 14 debugging commands all fail (an old namespace,
    `<pod-name>` redirections, an init container that no longer exists) and the corrected ones; a Job on
    the stand-in; Chroma's data path and why to run the loader again after a database restart; the README
    promises scaling, the code switches on only the node level (1–2 nodes); requests and bin packing;
    `kubectl scale` the frontend to 3, a `Pending` copy and the autoscaler's second node; why the API with
    its one-node disk cannot simply scale (`Multi-Attach`); scaling ticked, in two levels.
16. **Destroy, audit, recap** — `pulumi destroy --stack dev --refresh -y`, in reverse order; what can
    survive (forwarding rules, firewall rules, `pvc-…` disks, the registry images on purpose, lecture 20's
    VM) and four `gcloud … list` commands to check; the three asks and what did each job; the lecture's five
    payoffs; five test-yourself questions; next, lecture 23 runs both Pulumi programs from GitHub Actions.

The README's and the slides' small slips are pointed out kindly, with the fix: the deployment toolbox
does not build as committed (bookworm instead of bullseye, `google-cloud-cli` instead of
`google-cloud-sdk`); `docker-shell.bat` is not in the repository (use WSL); "Google Container Registry API"
and "GCR" are now Artifact Registry; `kubectl version` before a cluster exists prints `connection
refused` (harmless), and the kubectl you get is gcloud's dispatcher, not the Dockerfile's 1.34 pin; the
course link lands on "Deployment with Scaling using Kubernetes", but the cluster steps continue under
"Create & Deploy Cluster"; nothing creates the Artifact Registry repository, and the `deployment` account
very likely needs Service Account Admin on `gcp-service` (unverified here); "only required if you have NOT
already done this" means `deploy_images` finished `pulumi up` in the same state bucket (otherwise
`'NoneType' object is not subscriptable`); the committed `Pulumi.dev.yaml` carries two unused keys; the
Mermaid diagram's dotted arrow points from the vector DB to the loader, but the Job loads into the
database; the kubeconfig does not survive the toolbox session, and the code passes the region to
`--zone` (use `get-credentials … --region us-central1`); the README's Pod name is the author's (use yours);
the `Outputs:` block is older than the code (`ip_address`, `cheese-app-ingress`); the debugging block uses
`cheese-app-cluster-namespace` and `-c wait-for-chromadb`, which no longer exist, and its `<pod-name>`
placeholders are shell redirections; Chroma's PVC is mounted at `/chroma/chroma`, where today's image no
longer writes (it uses `/data`); and despite the title, the code scales only nodes (1–2): no replicas, no
Pod autoscaler, no requests on the API. Where the slides differ from today's code: the node runtime is
containerd, not Docker; GKE hides the control plane; slide 32 makes one node where the README makes two;
slide 39's YAML leaves out the label lines that connect the objects; `componentstatuses` is deprecated; and
a port-forward started in the toolbox opens inside the toolbox, not on your laptop.

## Rebuild

```bash
python -m explainer.build videos/ac215-l22-kubernetes-cloud -q l                          # fast draft
python -m explainer.build videos/ac215-l22-kubernetes-cloud --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l22-kubernetes-cloud --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l22-kubernetes-cloud --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l22-kubernetes-cloud --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once,
then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the
scene renders. The captures can be re-run with `assets/terminal/capture.sh` (see [`ASSETS.md`](ASSETS.md),
"`terminal/` — real terminal sessions"); the exercise checks with the scripts in
[`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-v3 tutorial is used
for study with the instructor's permission and quoted at its pinned commit. The lecture's slides are
redrawn in our own pictures, never shown. The Google Cloud console, the browser and a successful `pulumi
up` are schematic drawings (tagged `illustration`), never screenshots; the kubectl panels come from a kind
stand-in cluster, labelled as such, not from GKE; the recording used no Google account and no
credentials, and every project ID and `sa_…` user on screen is a placeholder.*
