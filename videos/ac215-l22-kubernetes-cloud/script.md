# AC215 · Lecture 22 — Scaling: Kubernetes in the cloud (the cheese app on GKE) — narration script & visual plan (v2, 2026-11-07: four reviews merged, see `build/review_merge_log.md`)

Audience: an AC215 student who has done L1–L21: cloud VMs, SSH and deleting what you create (L1–L2);
Docker images, containers, ports, `docker-shell.sh`, Docker networks and container names (L2–L4);
service accounts and JSON keys in `secrets/` next to the repo (L10, L15); the cheese app's API,
frontend, vector DB and loader locally (L18); and **L20**: the same repo's deployment toolbox with its
two one-line fixes, Pulumi stacks and state, `preview` / `up` / `destroy`, the `deploy_images` stack
with timestamp tags and `StackReference`, and the cheese app on one VM behind an nginx container.
They have seen Lecture 22 ("Scaling: Kubernetes (cloud)", 45 slides). New to them: orchestration,
the control plane and worker nodes, kubectl, Pods, Deployments, ReplicaSets, Services, labels and
selectors, namespaces, Jobs, PVCs, node pools and the cluster autoscaler, Ingress and its
controller, Helm, kubeconfig, Workload Identity, private nodes and Cloud NAT, `sslip.io`. They watch
with `dlops-io/cheese-app-v3` cloned next to their `secrets/` folder, Docker running and a GCP
project with billing, pausing to run each step. **Real money is involved**: a test cluster in Part 1,
a regional GKE cluster with nodes, a load balancer, NAT and two disks in Part 2 (GOLD tags; each part
ends with a delete).

Goal (BRIEF "Audience and goal"): after the video they can say what Kubernetes automates that L20's
VM could not (the lecture's three asks: failover, load balancing, scaling) and what in the cheese app
does each job; draw a cluster (API server, etcd, scheduler, controllers run by Google; kubelet,
kube-proxy, containerd and Pods on the workers) and name the part behind `Pending`,
`ImagePullBackOff`, a Pod that comes back, `EXTERNAL-IP <pending>`; read `kubectl [command] [TYPE]
[NAME] [flags]`; do the warm-up (toolbox with its two fixes, `gcloud … create`, kubectl, tic-tac-toe,
external IP, delete); explain Deployment → ReplicaSet → Pod, labels and Services, cluster DNS and
namespaces; run `deploy_images` then `deploy_k8s`, read the 23-resource plan and the order `pulumi
up` builds in; trace one click `<IP>.sslip.io` → load balancer → NGINX Ingress controller → Service
→ Pod and say why a bare IP gives 404; reconnect kubectl with `get-credentials --region`, shell into a
Pod, read a Job's logs with the corrected namespace; scale the frontend by hand and explain Pods vs
nodes, requests, `Pending`, the 1–2 node autoscaler and why the API with its disk cannot simply
scale; destroy and audit what survives.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md` (lecture
digest + scene map, binding next to the digest: docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest or the slides and the captures disagree, the captures win, and the
video says so kindly. **Which README**: `dlops-io/cheese-app-v3` `README.md` @ **`3ecef56`** (`main`,
2025-11-28, unchanged on the recording day per `laptop/p03`; the course site links `main`), sections
"Create Simple Kubernetes Cluster Tutorial" (README:517–581, done first, as the lecture does),
"Deployment with Scaling using Kubernetes" (392–434), "Create & Deploy Cluster" (436–512) and the
Kubernetes half of "Debugging Containers" (618–657). Branches `cluster-updates` and `pipenv` are
comparison only; an unmerged staff branch exists (`work/‹staff›` in committed text only) and is
**never named or shown**. Nothing in a terminal panel is typed by hand: every output line below names
its capture file and line numbers. Captures: 2026-11-07, 20:47–21:16 UTC.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at most
  about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown, no raw
  symbols (`/`, `=`, `%`, `&`, `$`, `→`, `_`, `<`, `>`, `—`); commands, flags and paths are on screen
  and said in words ("pulumi up, stack dev, refresh, dash y", "dash n, cheese app namespace",
  "slash api service"). File and folder names are said "deploy images", "deploy k8s", "setup
  containers dot py", "create cluster dot py", "Pulumi dot dev dot yaml"; `docker-shell.sh` is
  written as such (lexicon entry exists). Kubernetes names are said in words ("cheese app namespace",
  "vector db loader", "api ksa", "kube system"). Numbers are digits for ports, versions, counts that
  echo a terminal and step-like numbers ("port 8080", "replicas 4", "plus 23 to create"); small
  everyday counts may be words ("two nodes"). Never a "!" after a digit, no `'s` after a digit, no
  spoken decimals ("version three point zero", "about 92 seconds"; versions stay on screen with "at the
  time of recording"). Times of day are words ("two in the morning"), never "a.m.".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name (never "kubectl …",
  "pulumi …", "gcloud …", "nginx …" at a sentence start: write "The kubectl tool …", "Now get all …").
  No `'s` on a word with a lexicon entry or candidate (Pulumi, kubectl, gcloud, nginx, Helm, Chroma,
  etcd, Kubernetes). No bare "a" right before a lexicon entry or candidate ("one kubectl command",
  "the Helm chart"). No homographs: never "read", "reads", "live", "lives", "close", "lead", "tear",
  "minute(s)", "content", "record", "row" (use "look up", "sit", "stay", "check", "delete it all", "a
  short wait", "a quarter of an hour", "line"). The main clause comes first, so the Chinese subtitles
  keep English clause order.
- **README headings, not numbers.** The README's K8s sections have no numbered lists: the SAY names
  each step by its README heading or action ("Create Cluster", "Try some kubectl commands", "Get the
  Loadbalancer external IP"). The tracker's step numbers are on screen, never spoken.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on an
  empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). Five in the video, BRIEF's
  table and numbers, Conny's 2026-10-21 density decision: P1 S01, P2 S06, P3 S07, P4 S13 (8 s each),
  P5 S15 (10 s). The SAY before each card speaks the question; the answer is the next SAY. Nothing
  during the timer shows the answer.
- `TERM(id: lines)`: a terminal beat. `bNN`, `cNN`, `pNN` = `assets/terminal/laptop/<id>-*.txt`
  (`b02a`, `b31-1..3` = `b31-k8s-config-set-1..3`, `c11-1..3` = `c11-x-k8s-config-set-1..3`); `kNN` =
  `assets/terminal/kind/<id>-*.txt`. The scene types the command written just before it in the SHOW
  line (in backticks, exactly as the README spells it; extras exactly as the capture's line 1 spells
  it, folding with ` \`; `typed crop "…"` = type line 1 only up to the quoted text, a prefix that is
  itself the whole command whose output is printed), then prints the listed **file** lines. Line 1 is
  the `$ …` command: typed, never printed; `[exit N]` is never printed. Inside the list: `…` = print one
  `…` line; `wrap` = fold long lines; `crop "…"` = print that line only up to and including the quoted
  text; `→ (no output)` = the prompt simply returns. Blank output lines are dropped. kind's emoji
  (`k01`) are printed as captured; if the terminal font lacks a glyph, that glyph alone is dropped.
- Prompts (constructed; captures hold only the command): the laptop `student@laptop:~$`,
  `student@laptop:~/cheese-app-v3/src$`, `student@laptop:~/cheese-app-v3/src/deployment$`, title
  `laptop`. Inside the toolbox the prompt is the string printed by `b03:77` (`root@<id>:/app#`; the
  scene reuses that printed string, the id is never read aloud), then `…:/app/deploy_images#` and
  `…:/app/deploy_k8s#` after the `cd`s; title `laptop · toolbox`. The kubectl beats on the stand-in
  run at the same toolbox prompt (the toolbox's own kubectl talks to kind, ASSETS "kind wiring"), title
  `laptop · toolbox · stand-in`; `k01` and `k81` (kind itself) run at `student@laptop:~$`, title
  `laptop · stand-in`.
- **Masking at load time** (BRIEF "Running example"): `c12:8`'s `sa_` + 21 digits → `sa_000000000000000000000`;
  the README's `ac215-project` stays where a README command prints it (`b21`, `b31-1..3`, `c02`,
  `c11-1..3`, `c12`, `c03`'s tags, `c21`'s URL) with the GREY `default_tag` "the README's default ·
  change to yours"; `your-gcp-project` is the placeholder of `b03`, `b14`, `b52`. `b02`'s `[IP:
  172.17.0.1 38722]` column is cropped (`crop "404  Not Found"`); `k01:8–14` (the capture-only
  `containerdConfigPatches`) and `c21`'s Python tracebacks (`c21:60–161`, `c21:173–270`) are never
  printed; `p02:7` / `p03:6` (the staff branch) are never printed and `p02:1` is typed only up to
  `"%s'"` (see S02). README lines 499, 500, 505 (sample IPs) never appear: the outputs block comes from
  `expected/`. The stand-in's private addresses (`10.96.…`, `10.244.…`) may stay in panels and are
  never read aloud; nor are ids, hashes (except the ReplicaSet's `pod-template-hash`, the point of
  S07, shown, not read digit by digit) and timestamps.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` with the real line numbers, header
  `path · lines a–b`; at most 12 lines on screen. Paths are relative to `assets/source/`
  (`src/deployment/…`, `src/api-service/…`, `src/frontend-react/…`). A "README card" is a GREY quote of
  README text, header `README.md · lines a–b` (markdown stripped).
- `EXPECTED(expected/readme-pulumi-outputs: lines)`: a GREY-outlined panel quoting those lines of
  `assets/terminal/expected/readme-pulumi-outputs.txt` (line 1 is its provenance comment, never
  printed), tagged `expected · README:497–506`. The only `expected` panel (S14).
- `TRACKER [k] n`: the `ReadmeTracker`, top-left in every walkthrough scene, for README section `k` at
  step n; `TRACKER [k] n · extra` = same step, caption " · extra" while a command the README does not
  have is on screen. Titles are the README's own headings. Step titles ≤ 3 words (BRIEF table):
  - [W] "README › Create Simple Kubernetes Cluster Tutorial" (README:517–581), 11: 1 Enable APIs ·
    2 Run toolbox · 3 Check tools · 4 Auth check · 5 Create cluster · 6 See console · 7 Try kubectl ·
    8 Deploy app · 9 Get IP · 10 View app · 11 Delete cluster.
  - [D] "README › Deployment with Scaling using Kubernetes" (392–434), 7: 1 Enable APIs · 2 Run
    toolbox · 3 Check tools · 4 Auth check · 5 Images stack · 6 Images preview · 7 Images up.
  - [C] "README › Create & Deploy Cluster" (436–512), 8: 1 Cluster stack · 2 Config keys · 3 Preview ·
    4 Pulumi up · 5 Try kubectl · 6 Shell into Pod · 7 View app · 8 Delete cluster.
  - [G] "README › Debugging Containers" (618–657, its Kubernetes half), 4: 1 Job logs (620–626) ·
    2 Find pod (631) · 3 Pod logs (634–643) · 4 API logs (646–656).
  S01–S03 and S09 have no tracker; S16 has none after its destroy blocks.
- `LECTURE 22 · a–b` in a SHOW line: the GREY `lecture_ref(22, "a–b")` tag (`explainer.devops`) top right
  ("Lecture 22 · slides a–b"; "slide" for one) **for that SHOW block only**: it fades in with the
  redrawn lecture picture or idea and fades out at the end of the block. `LECTURE (held)` in the next
  block keeps it, only while the same picture stays on screen. A SHOW line without a LECTURE mark has no
  lecture tag. Every lecture picture is our own redrawing in series colours with the slide's structure
  and terms: no slide image, QR code, meme, photo, logo (no ship's wheel), demo link or screenshot. The
  story's roles are "the app owner" and "the operator", never a person's name. Spoken bridges to the
  lecture: at most one short sentence per scene ("the lecture draws it in three steps").
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says "extra" the first time each kind appears in a scene. Variants: `extra · not for you`
  on `c00` (Pulumi's local backend, a recording workaround) and every later `cNN` panel carries
  `extra`; `extra · our spelling` on the corrected commands typed without output (S14, S15, S16).
- **The stand-in.** Every panel from `kind/` carries the GREY tag `stand-in: kind, not GKE` (top right
  of the terminal) in addition to any `extra`; the V1 cluster drawn on the laptop has a GREY dashed
  outline. `c20`/`c21` additionally carry the GREY tag `placeholder image tags · nothing built`.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per tracker group);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every console view, browser window, the `pulumi up`
  dependency animation (S12), the teardown animation (S16) and every lecture redrawing that shows
  cloud machinery as working; `expected · README:497–506` (S14); `erratum` on every README or slide
  slip (the SAY says "a small note" or "a small slip", never "erratum"); `at the time of recording`
  beside every version on first show; `default_tag` (see Masking). GOLD `cost_tag()` where a billable
  resource appears: the test cluster (S05), the cheese app's cluster, nodes, load balancer, NAT and
  disks (S09, S12), registry storage (S16); the GOLD "Don't forget to delete" card (S08, S16). Prices
  only in S09, as "roughly … by our estimate".
- **The sandbox framing** (BRIEF "Running example", load-bearing): said once, in S02. Afterwards every
  Google or Pulumi-backend error is the next line of the lesson, and "yours prints …" is said, never
  shown as output. Never imply that a GKE cluster, a `pulumi up`, a push or the app ever ran here.

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| the laptop and everything on it: Docker Desktop, the browser, the toolbox's outline; the kind stand-in cluster (GREY dashed outline, tag `stand-in: kind, not GKE`) | GREY |
| the cloud: GCP's outline, the GKE cluster outline, the control plane box (BLUE, greyed, "run by Google"), worker nodes, node pool, VPC and subnet, Cloud Router / NAT, the external load balancer, persistent disks, Artifact Registry, the state bucket, Vertex AI, the cloud provider API | BLUE |
| containers, images and Pods (TEAL circles, container dots inside), the toolbox `cheese-app-deployment`, `dlops/tic-tac-toe` | TEAL |
| shared, cluster- or OS-owned: `kube-system` and its Pods, the `default` namespace, `service/kubernetes`, Google's apt repo and its `kubectl` package, Debian's archives | ORANGE |
| project-owned, declared: manifests, Pulumi programs and stack config, desired state, Deployment / ReplicaSet / Job / PVC cards, `cheese-app-namespace`, timestamp image tags | GREEN |
| tools: kubectl, gcloud, helm, pulumi and its providers, docker, kind, gke-gcloud-auth-plugin | PURPLE |
| errors and "don't": every honest first error, README lines that are wrong, a `Pending` that never ends, `Multi-Attach` | RED |
| your turn, the README tracker, the thing to look at now, ponder timers, the three-asks ticks | YELLOW |
| money: cluster fee, nodes, load balancer, NAT, disks, registry storage; "Don't forget to delete" | GOLD |
| lookups and routes: Services, labels and selectors (`run: web` stickers), endpoints, DNS names, ports, Ingress rules, `sslip.io`, request arrows, the kubeconfig's server, the `StackReference` pipe | PINK |
| the past, the future, and what is possible but not configured: L20's VM, L23, the slides' "Docker" runtime and "master node" wording, the HPA, a second API replica | GREY, dashed |

Pods are always TEAL and never change colour by state; their status is a small word under them
(`Running` WHITE, `ContainerCreating` YELLOW, `Pending` RED, `Completed` GREY).

Running example
- **The laptop** (`laptop/`, a fresh Docker 29.8.2 engine, user `student`): `cheese-app-v3/` and
  `secrets/` side by side (`p05`); `secrets/deployment.json` is a well-formed file around a throwaway
  key for **no account** (never shown as a panel). The README's `cd deployment` (405, 528) is typed from
  `~/cheese-app-v3/src`; S04 says "from the S R C folder" once.
- **The toolbox** `cheese-app-deployment` (2.61 GB, `k81:6`), built after the two L20 fixes (`b02a`).
- **The stand-in cluster** (S05–S08, S14, S15): kind v0.31.0, `test-cluster`, one control plane + two
  workers, Kubernetes v1.34.11, in the laptop's engine. Said plainly once in S05; every panel tagged.
- **Pulumi's local backend** (S10–S12, S16): `pulumi login --local` (`c00`), `extra · not for you`, said
  once in S10.
- **Placeholders**: `your-gcp-project`; the README's `ac215-project` with its `default_tag`;
  `sa_000000000000000000000`; no public IP anywhere (browser bars say `http://<EXTERNAL-IP>` and
  `http://<IP>.sslip.io`; the outputs come from `expected/` with `<IP>`).
- **Versions** (on screen with "at the time of recording", not spoken): Google Cloud SDK 592.0.0,
  gke-gcloud-auth-plugin 0.5.21, kubectl `v1.35.9-dispatcher` (`v1.34.12-gke.300…` against the 1.34
  stand-in), Helm v3.22.1, Pulumi v3.274.1 (plugins kubernetes 4.23.0, gcp 9.3.0), Python 3.13.18, uv
  0.13.7; kind v0.31.0, Kubernetes v1.34.11; toolbox 2.61 GB.

Length and parts: narration target 3,900–4,300 words (`python -m explainer.script`, which counts SAY
words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm),
≈24 min of narration, ≈31–33 min with typing, outputs, illustrations and five ponder timers.
Per-scene counts against the BRIEF budgets are in the table at the end ("Word count").
Part 1 = S01–S08 (Kubernetes by hand: slides 4–40, the README's warm-up on the stand-in; ends on S08's
empty frame after the test cluster is deleted and the GOLD "Don't forget to delete" card). Part 2 =
S09–S16 (the cheese app as code: slide 41's handover, README:392–512 and 618–657, slides 5, 15, 18,
21–26, 33–36, 38–41, 43–44; ends on the L23 pointer, then an empty frame). The cut is the lecture's own seam (slide
40 deletes the test cluster, slide 41 turns to the Pulumi code).

Notes for scene authors
- Shared code (`scenes/common.py`, started from L20's): tracker factories `tracker_w`, `tracker_d`,
  `tracker_c`, `tracker_g` with the step lists above; prompts `P_LAPTOP`, `P_SRC`, `P_DEPLOY` and the
  toolbox prompt string taken from `b03:77` (+ `/app/deploy_images`, `/app/deploy_k8s` variants); tags
  `your_turn`, `extra_tag` (+ `not for you`, `our spelling`), `standin_tag`, `placeholder_tag`,
  `illustration_tag`, `expected_tag(source)`, `erratum_tag`, `cost_tag(text)` (GOLD), `default_tag`,
  `lecture_ref`; `browser_window(url, rows)`; `console_view(path, rows)`; the `sa_` masking helper; set
  pieces `MasterDiagram` (V1: `beat22()`, `beat23()`, `beat24()`, `callout(part)`, `lamp(part,
  colour)`, `laptop_box(chips)`, `standin=True` for the GREY dashed outline), `FleetMorph` (V2),
  `LabelLink` (V3), `ControllerLoop` (V4, with `job=True` for the Job cousin), `CheeseBlueprint` (V5),
  `ResourceTree` (V6), `RequestJourney` (V7), `BinPacking` (V8), plus `AsksChecklist` and
  `KubectlGrammar`. Never reuse a scene class name for a helper.
- **The AsksChecklist** lives top right **below** the `lecture_ref` slot (they must never overlap):
  created in S01, shown small in S07, S13, S15 and S16 only (it fades with each scene's end), ticks
  YELLOW; S15's Pod-level half-tick is dashed.
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the output
  body, so pick index = file line − 1. Assert the picked text for every highlighted line.
- **BRIEF corrections and precisions found while scripting** (captures and sources win):
  - `k80:1` also deletes `job/hello-job` (`k80:4`), which S08 has not introduced yet: S08 types `k80:1`
    with `typed crop "deploy-k8s-tic-tac-toe.yml"` and prints `k80:2–3` only.
  - `k53:2` and `k80:2–3` end in "… deleted from default namespace" (newer kubectl wording), not just
    "deleted": print as captured.
  - `k50` has a deprecation `Warning: v1 Endpoints is deprecated …` on line 2: printed GREY, not read.
  - The cheese app's Services are named `frontend`, `vector-db`, `api` (`setup_containers.py:94`,
    `:328`); `frontend-service`, `vector-db-service`, `api-service` are Pulumi's resource names in `c20`.
    The V7 lanes use the Service names with ports (as the README's diagram does).
  - The Dockerfile's kubectl pin is `src/deployment/Dockerfile:33` (`ARG K8S_MINOR=1.34`); the API
    Deployment has no `resources` block at all (`setup_containers.py:246–322`), frontend requests are
    at `:79–82`, Chroma's at `:154–155` (`100m` / `128Mi`), NGINX's at `setup_loadbalancer.py:26–30`.
  - `docker-shell.sh:34` runs the toolbox with `--rm` (why the kubeconfig is gone next session, S12/S14).
  - `b52:1` is `get-credentials … --zone us-central1 --project your-gcp-project`, i.e. what
    `create_cluster.py:192–198` runs; the corrected `--region` form is a typed card (no output).
  - BRIEF's S15 "`--replicas=5` → two blocks hover for good" depends on node sizes we did not measure:
    the SAY says "some stay pending"; V8 shows one or two hovering blocks, labelled `illustration`.
- Lexicon (merge stage, `explainer/lexicon.yaml` "# AC215 L22", phonemes checked with
  `KokoroBackend.phonemize`): etcd, Etcd, kubeconfig, containerd, kubelet, kubelets, "deploy k8s",
  "zone us east 1 c", docker-shell.bat, "sslip dot io", "502 or 503" added; kubectl, Pulumi / pulumi,
  docker-shell.sh, dlops, gcloud, nginx, Kubernetes already sound right. Earlier candidates: gcloud ("gee cloud"), nginx ("engine x"), Kubernetes ("koo-ber-NET-eez"), etcd
  ("et see dee"), kubelet ("cube let"), "kube proxy" ("cube proxy"), "kube system" ("cube system"),
  containerd ("container dee"), kubeconfig ("cube config"), ReplicaSet ("replica set"), Helm, Chroma,
  sslip ("ess ess lip"), "io" in "sslip dot io" ("eye oh"), GKE ("G K E"), WSL ("W S L"), "S R C",
  "k8s" in "deploy k8s" ("K eight S"), "ksa" ("K S A"), tic-tac-toe, bookworm, bullseye, Debian,
  Vertex, TensorFlow, "pvc" ("P V C"), "multi attach" (plain words).
- Subtitle display for the i18n stage (`en_display`): slash api service → `/api-service`; slash api
  service slash status → `/api-service/status`; slash data → `/data`; chroma chroma → `/chroma/chroma`;
  deploy images → `deploy_images`; deploy k8s → `deploy_k8s`; setup containers dot py →
  `setup_containers.py`; create cluster dot py → `create_cluster.py`; cheese app namespace →
  `cheese-app-namespace`; cheese app cluster namespace → `cheese-app-cluster-namespace`; cheese app
  cluster → `cheese-app-cluster`; cheese app ingress → `cheese-app-ingress`; cheese app repository →
  `cheese-app-repository`; vector db → `vector-db`; vector db loader → `vector-db-loader`; wait for
  chromadb → `wait-for-chromadb`; api ksa → `api-ksa`; kube system → `kube-system`; test cluster →
  `test-cluster`; us east 1 c → `us-east1-c`; us central 1 → `us-central1`; run web → `run: web`;
  replicas 4 → `--replicas=4`; dash n → `-n`; dash f → `-f`; dash y → `-y`; refresh → `--refresh`;
  pulumi login local → `pulumi login --local`; pulumi up, stack dev, refresh, dash y → `pulumi up
  --stack dev --refresh -y`; G C P project → `gcp:project`; Pulumi access token must be set →
  `PULUMI_ACCESS_TOKEN must be set`; ROOT PATH → `ROOT_PATH`; ip address → `ip_address`; nginx ingress
  ip → `nginx_ingress_ip`; app URL → `app_url`; setup SSL → `setupSSL`; web dot default dot svc dot
  cluster dot local → `web.default.svc.cluster.local`; sslip dot io → `sslip.io`; gcp service →
  `gcp-service`; zone us east 1 c → `zone us-east1-c`; docker-shell.sh line 13 → `docker-shell.sh:13`;
  Milestone 5 → as is; google cloud SDK →
  `google-cloud-sdk`; google cloud CLI → `google-cloud-cli`; docker-shell.bat → as is; get credentials
  → `get-credentials`; region flag → `--region`; zone flag → `--zone`; port forward → `port-forward`;
  the quoted errors in quotes ("no active account", "connection refused", "invalid grant, account not
  found", "none type is not subscriptable", "namespace not found", "syntax error", "no such file",
  "no credentialed accounts", "created stack dev", "multi attach"). In zh all of these stay English
  (glossary rule). Metaphors for the zh glossary, rendered the same way every time: "the brain" →
  大脑; "the hands" → 双手; "lamps" → 指示灯; "the thermostat" → 恒温器; "a sticker" → 贴纸; "a lasso"
  → 套索; "one door with a receptionist" → 一扇门加一位前台; "the meter" → 计费表; "the lever" → 拉杆;
  "the toolbox" → 工具箱 (the container keeps its English name on screen). "Switch over by hand" (S01)
  → 手动切换 (the v1 "pull the lever" idiom is gone: 拉闸 would mean the opposite). "kind" stays English as
  code everywhere, also in "the kind cluster".
- Never: the instructor's name (`‹instructor›`), staff names, the staff branch's name, a slide image or
  long slide text, a Google/GCP or Kubernetes logo, a console or browser screenshot, a real-looking key,
  token, project id, `sa_` number or public IP, a fake GKE create table, a `pulumi up` progress log, the
  real Outputs, the cheese-app Pod listings or app pages shown as output; the kind stand-in presented as
  GKE; "the nodes run Docker"; "kubectl creates clusters"; "the cheese app scales its Pods by itself";
  `c20`/`c21` without "placeholder image tags"; the local backend as a step to follow; "destroy removes
  everything".

---

## S01 · Who restarts it at 2 a.m.? — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. LECTURE 22 · 4–5. **V2 `FleetMorph`**, slide 5 redrawn: a BLUE box
"VM" centre; inside it a TEAL box `nginx` at the top and three TEAL boxes under it, `Frontend`,
`API 1`, `API 2`, each joined to nginx by a short PINK line. A PINK door "HTTP 80" on the VM's top
edge; a GREY browser window drops above it with a PINK arrow down to the door. On "who restarts it" a
YELLOW "?" settles beside the VM.
SAY: Here is a small app on one virtual machine: a web server in front, a frontend and two APIs behind it. If one of them crashes in the night, who restarts it?

SHOW: LECTURE 22 · 7. A GREY clock face top left turns to "2:00 a.m.". `API 1` cracks and turns RED;
the PINK request arrow from the browser now bounces off with a small RED "×". A GREY phone icon beside
the VM shakes ("the app owner"), then a GREY figure "the operator" slides in along a PINK tunnel labelled
"SSH" into the VM; `API 1` flips back to TEAL.
SAY: At two in the morning, one API container crashes. The app owner finds out when users complain, and the operator logs in over SSH and restarts it by hand.

SHOW: A GREY-dashed chip slides in beside the VM: "L20 · one VM · Docker restarts containers · nobody
restarts the VM". It pulses once, then fades.
SAY: In lecture 20, Docker could restart a crashed container, but only on that one machine: if the machine itself failed, the whole site waited for you.

SHOW: LECTURE 22 · 8–9. The VM transforms into three BLUE VMs side by side: VM 1 holds `Frontend` (PINK
door "HTTP 80"); VM 2 holds a TEAL `nginx` above `API 1` and a dashed TEAL `API 1 · backup`; VM 3 holds a
TEAL `nginx` above `API 2` and a dashed TEAL `API 2 · backup` (slide 9's layout). Above them a GREY speech card in our words: "put it on several servers".
SAY: So the app owner asks for several servers. The operator answers with three machines, and a backup copy beside each API.

SHOW: LECTURE (held). The two backup boxes glow YELLOW. A YELLOW question card settles under the VMs.
SAY: Each backup sits on the same machine as its original. Name one failure that still takes that API down, and say who switches to the backup.
PONDER(8 s, "Each backup sits on the same VM\nas its original.\nWhat still takes that API down,\nand who switches to the backup?")

SHOW: LECTURE 22 · 9, 11. VM 2 goes dark and turns RED as a whole, taking `API 1` and its backup with
it. Then a GREY lever appears beside VM 3 with a GREY hand on it, captioned "switch: by hand".
SAY: The machine itself: one failed disk or network takes both copies at once. And even when a backup survives, a person still has to switch over by hand.

SHOW: LECTURE 22 · 12. The VMs fade. **`AsksChecklist`** grows centre: a card with three empty boxes,
"Failover", "Load balancing", "Scaling", each line lighting YELLOW on its phrase, with a GREY
one-liner under each ("a working copy takes over", "requests spread across copies", "more copies when
busy").
SAY: The lecture wants three jobs done with nobody awake. Failover: a working copy takes over. Load balancing: requests spread across copies. Scaling: more copies when traffic grows.

SHOW: The card shrinks into the top-right corner (below the lecture-tag slot). The word "Kubernetes"
writes in the centre in WHITE, then everything fades; empty frame.
SAY: This card stays in the corner, and we tick each item once we see what does the job. The tool for all three is Kubernetes.

---

## S02 · From one box to a fleet — `s02_orchestrator.py` · `Orchestrator`

SHOW: No tracker. LECTURE 22 · 17. The word "Kubernetes" centre; under it a GREY line "Greek: helmsman,
the one who steers" (no wheel, no logo); a small GREY-dashed chip "Helm · part 2" slides in under it.
Then a one-line definition in WHITE: "an orchestrator: runs containers across a cluster of machines, and
keeps them as you declared".
SAY: Kubernetes is an orchestrator: it runs containers across a cluster of machines and keeps them the way you declared. The name is Greek for helmsman, and Helm, a tool in part 2, borrows it.

SHOW: LECTURE 22 · 19. **V2's morph.** Left: one BLUE machine with a long GREY bar "Docker" and five
TEAL boxes on it, caption "container deployment". It *transforms* into the right side: three BLUE node
boxes, each with its own thin runtime strip and the same TEAL trio (`Frontend`, `API 1`, `API 2`) spread
over them, thin lines from each node up to one BLUE-greyed box "control plane"; caption "Kubernetes
deployment".
SAY: On the left, one machine runs every container on one Docker engine. On the right, many machines, called nodes, share the containers, and one control plane coordinates them.

SHOW: LECTURE (held). Under the right caption a GREY-dashed note writes the two words side by side, so
the eye sees what the ear cannot: "deployment = a way of deploying · ≠ `Deployment`, the object (S06)";
the word `Deployment` glows GREEN once.
SAY: A word of warning: here, deployment means a way of deploying, not the Deployment object we meet later.

SHOW: LECTURE 22 · 21–22. **V5's opening frame**: a GREY-dashed box "L20 · one VM" with TEAL `nginx`,
`api-service`, `frontend`, `vector-db` and a dashed `loader`; on the left a GREY "your laptop" box with
the TEAL toolbox and three PURPLE chips `gcloud`, `docker`, `pulumi`. The VM *transforms* into a BLUE
dashed "Kubernetes cluster" outline; a fourth chip `kubectl` arrives, the largest, flashing YELLOW, then
two smaller chips `helm` and `gke-gcloud-auth-plugin`.
SAY: In lecture 20 the cheese app ran on one machine. Now the same app goes to a cluster, and the tools gain kubectl. Our toolbox already has it, plus Helm and the GKE auth plugin, which the slides do not list.

SHOW: The diagram shrinks to the left. Chips slide in on the right, one per phrase: GREY "cheese-app-v3 +
secrets/ beside it", GREY "Docker running", GREY "a GCP project with billing", then a GOLD `cost_tag`
"clusters cost money by the hour · each part ends with a delete".
SAY: To follow along: cheese app version 3 with your secrets folder beside it, Docker, and a Google Cloud project with billing. A cluster costs money by the hour, so each part ends by deleting it.

SHOW: The chips fade. Samples appear one per phrase, each fading as the next arrives (at most two on
screen), each in the place it will occupy and with one Indicate: top left a YELLOW `ReadmeTracker`
"README › Create Simple Kubernetes Cluster Tutorial · step 1 of 11"; centre a small code panel header
`src/deployment/deploy-k8s-tic-tac-toe.yml · lines 2–22`; a sample command with a YELLOW `▶ your
turn`; top right a GREY sample tag "Lecture 22 · slides 4–11".
SAY: The tracker names the README step, code panels name their file and lines, and your turn means pause and run it. A grey tag in the corner names the lecture slides.

SHOW: The samples fade. A GREY card with two columns: left "a machine you own → real, complete" (GREEN
tick), right "Google → stops at its first honest error" (RED dot); a third line spans both: "kubectl →
a small stand-in cluster on the laptop, labelled `stand-in`"; GREY footer "and we say what yours prints".
SAY: One honest note: our recording machine has no Google account. What runs on a machine you own is real; every Google step stops at its first honest error, and we say what yours prints.

SHOW: A full-width terminal `laptop`, prompt `student@laptop:~$`. It types line 1 of `p02` (extra;
`typed crop "%s'"`, i.e. `git -C cheese-app-v3 log -1 --format='%H %ci %s'`) → TERM(p02: 2). The hash
glows YELLOW (not read), the date `2025-11-28` PINK, the message `v4->v3` GREY. A GREY chip: "the course
site links: main". (The branch list, `p02:3–7`, is never printed.)
SAY: We follow main, the branch the course site links, at this November 2025 commit. Git log tells you which one you have.

SHOW: The terminal fades. Two GREY cards side by side: "Part 1 · by hand · the lecture's warm-up" (a
small cluster with a TEAL game Pod) and "Part 2 · as code · the cheese app on GKE" (a small V5). Fade;
empty frame.
SAY: Part 1 does the lecture's warm-up by hand. Part 2 deploys the cheese app as code.

---

## S03 · Inside a cluster: brain and workers — `s03_anatomy.py` · `ClusterAnatomy`

SHOW: No tracker. LECTURE 22 · 22. **V1 `MasterDiagram`, beat 22**: on the left the GREY "your laptop"
box with the TEAL toolbox and its PURPLE chips (`kubectl` largest); on the right a BLUE dashed
"Kubernetes cluster" box with one tall BLUE-greyed panel "control plane" and three PINK arrows fanning
out to three BLUE boxes "worker node (VM)".
SAY: Let's open the cluster. The lecture draws it in three steps. First: one control plane, with arrows to several worker nodes, each an ordinary virtual machine.

SHOW: LECTURE 22 · 23. Beat 23: the control plane gets the caption "control plane · run by Google" and a
GREY-dashed footnote "slides: master nodes"; the workers get a bracket "worker nodes · node pool: 1–2 ×
n2d-standard-2 · us-central1-a".
SAY: Second, the two planes get names. The control plane is the brain. On GKE, Google runs it, and you never see its machines. The workers carry your containers: for the cheese app, a pool of one or two nodes.

SHOW: LECTURE 22 · 24–25. Beat 24, each part introduced by what it does: inside the control plane, the
box "API server" grows first, and a YELLOW pulse runs kubectl → API server as its WHITE callout "the
single entry point" writes; then a BLUE cylinder "etcd" grows below it and the pulse drops a GREEN
`desired state` card into it as "the cluster's memory: state and config" writes. Two boxes "scheduler"
and "controllers" (a stack of three cards) wait above, greyed, each joined to the API server only.
SAY: Third, the parts. The API server is the single entry point; every other part talks only to it. Etcd is the memory of the cluster: its state and configuration.

SHOW: LECTURE (held). The pulse continues from the API server to the scheduler, which lights and picks
one worker (the worker flashes) as "picks a node for each Pod" writes; then to the controllers, where a
ring arrow turns as "keep watching, fix the difference" writes. A BLUE box "cloud provider API" appears
outside the cluster box; a PINK arrow from the controllers to it, labelled "nodes, load-balancer IP".
SAY: The scheduler picks a node for each new Pod. The controllers keep watching and fix any difference between what you asked for and what runs; some of them ask the cloud for nodes and addresses.

SHOW: LECTURE 22 · 26. Worker node 1 zooms a little: inside it "kubelet", "kube-proxy" and a strip
"container runtime: containerd" holding two TEAL Pod circles with container dots. Callouts: kubelet
"the API server's hands on this node"; kube-proxy "routes Service traffic"; runtime "runs the
containers".
SAY: On every worker, the kubelet is the hands of the API server: it starts and stops the containers. Kube proxy routes traffic for Services, and a container runtime runs the containers, grouped in Pods.

SHOW: LECTURE (held). On the runtime strip, a GREY-dashed word "Docker" (the slide's label) is crossed
out over `containerd` (tag `erratum`). A one-line panel slides in: CODE(src/deployment/deploy_k8s/create_cluster.py:
52), `image_type="cos_containerd"` YELLOW.
SAY: A small note: the slide names Docker as the runtime. On GKE it is containerd, line 52 of create cluster dot py. You still build images with Docker, and they run unchanged.

SHOW: The callouts fade. Recap at 1.5× speed: a YELLOW pulse travels kubectl → API server ("the only
door"), then the API server → etcd (a GREEN card "desired state" drops into the cylinder); then the
arrowheads point the other way, scheduler → API server and the kubelets of two nodes → API server,
labelled "watch".
SAY: Now follow the arrows. Every kubectl command goes to one place, the API server, which stores your wish in etcd. The scheduler and the kubelets pick up their work from it.

SHOW: LECTURE 22 · 27. V1 shrinks to the top. **`KubectlGrammar`** card centre: four PURPLE slots
`command · TYPE · NAME · flags`. Three examples that S05 runs slot in one after another: `kubectl get
nodes` (`get` / `nodes` / — / —), `kubectl get pods` (`get` / `pods` / — / —), `kubectl get pods
--all-namespaces` (`get` / `pods` / — / `--all-namespaces`). The NAME slot stays empty, with a GREY
chip "optional · one object".
SAY: The lecture gives kubectl one grammar: a command, a type, an optional name, and flags. Get nodes. Get pods. Get pods, with a flag for every namespace.

SHOW: The card fades; V1 returns full size. Four small lamps blink once, unlabelled: on the scheduler, on
the controllers, on the cloud-provider arrow, on the kubelet. Fade; empty frame.
SAY: When something is stuck, ask which of these parts is waiting. Four lamps on this picture will light up later, each with a symptom you will meet.

---

## S04 · The toolbox, still fixed twice — `s04_toolbox.py` · `Toolbox`

SHOW: TRACKER [W] 1. Two GREY README cards stacked: "Deployment with Scaling using Kubernetes · 392",
"Create & Deploy Cluster · 436", then "Create Simple Kubernetes Cluster Tutorial · 517". The third card
slides to the top, with a GREY chip "lecture order: slides 32–40 first".
SAY: The README keeps this warm-up after the cheese app's deployment. The lecture does it first, and so do we: it is the gentlest first contact with kubectl.

SHOW: TRACKER [W] 1. A schematic console list (tag `illustration`, no logo), README card `README.md ·
lines 521–525`: "Compute Engine API", "Service Usage API", "Cloud Resource Manager API", "Google Container
Registry API", "Kubernetes Engine API", each with an "Enable" button that ticks GREEN on its phrase. The
fourth line is struck through GREY (tag `erratum`) and a GREEN replacement writes beside it: "Artifact
Registry API".
SAY: First, enable five APIs in the console. A small slip: Google Container Registry has been shut down. Enable Artifact Registry instead.

SHOW: TRACKER [W] 2. Full-width terminal `laptop`, prompt `student@laptop:~/cheese-app-v3/src$`.
It types `cd deployment` → (no output); the prompt becomes `…/src/deployment$`. It types `sh docker-shell.sh`
→ TERM(b02: 2, 12 wrap, …, 150 crop "404  Not Found", 151 crop "404  Not Found", …, 166 wrap, 167, 168 wrap).
Line 12 (`ERROR [ 2/16] RUN apt-get update …`) RED; the two `404  Not Found` endings RED; line 168's `pull
access denied` RED.
SAY: Then start the toolbox: from the S R C folder, change into deployment and run docker-shell.sh. As committed, it fails: 404 Not Found from Debian, then pull access denied.

SHOW: The terminal shrinks to a strip. CODE(src/deployment/Dockerfile: 4) with `python:3.13-slim-bullseye`
ORANGE, a GREY chip "bullseye's security pool: gone". Beside it a GREY note (tag `erratum`):
"`docker-shell.bat` (README:529): not in the repo → use WSL".
SAY: If you did lecture 20, you have seen this: the base image is Debian bullseye, whose security packages are gone. On Windows there is no docker-shell.bat. Use WSL.

SHOW: TRACKER [W] 2 · extra. The terminal grows back. It types line 1 of `b02a` (extra; folds) →
TERM(b02a: 10, 11, 19, 20): lines 10 and 19 RED, 11 and 20 GREEN. On "auth plugin" the words
`google-cloud-cli-gke-gcloud-auth-plugin` on line 20 glow PURPLE.
SAY: The fix is the same two one-line edits, an extra here. Bullseye becomes bookworm, and google cloud SDK becomes google cloud CLI, with its GKE auth plugin. Every kubectl call to GKE goes through that plugin.

SHOW: TRACKER [W] 2 · extra. It types line 1 of `b01` (extra; folds) → TERM(b01: 2); `your-gcp-project`
YELLOW, with a GREY chip "L20 · README:267 · your project id" (the GREY `default_tag` stays on the
README's `ac215-project`).
SAY: As in lecture 20, also put your project on line 13 of docker-shell.sh.

SHOW: It types `sh docker-shell.sh` again → TERM(b03: 3, …, 31, 36 wrap, 70, 71 crop "state backend", 77).
Line 3's `92.3s` GREEN, with a GREY chip "Apple Silicon: emulated amd64 · much slower"; line 31
`Container is running!!!` TEAL, lines 36 and 71 RED. The last printed line
(`b03:77`) becomes the live toolbox prompt; the terminal title becomes `laptop · toolbox`.
SAY: Run it again: it builds in about 92 seconds and starts. The login then fails, because our key belongs to no account; with yours, these lines say activated and logged in.

SHOW: A YELLOW `▶ your turn` beside the toolbox prompt.
SAY: Pause here and start your toolbox; the rest of this part runs at its prompt.

SHOW: TRACKER [W] 3. LECTURE 22 · 34. It types `gcloud --version` → TERM(b10: 2, …, 9, 11), tag `at the time of recording`;
`kubectl version` → TERM(b11: 2, 4), line 4 ORANGE; `kubectl version --client` → TERM(b12: 2). Under line
4, a small V1 thumbnail: the laptop's kubectl arrow points at an empty dashed box "no cluster yet".
SAY: Next, check the tools. The gcloud tool and its auth plugin are there. Plain kubectl version prints the client, then connection refused: there is no cluster yet, so the server half has nobody to ask.

SHOW: `b12:2` `v1.35.9-dispatcher` glows YELLOW. Beside it CODE(src/deployment/Dockerfile: 33)
`ARG K8S_MINOR=1.34`, and a GREY chip (tag `erratum`): "Google's own kubectl package wins → a dispatcher
that picks a matching client".
SAY: A small surprise: the Dockerfile pins one kubectl version, but Google's own package wins: a dispatcher that matches each cluster.

SHOW: TRACKER [W] 4. It types `gcloud auth list` → TERM(b13: 3) RED. A GREY chip beside it: "yours:
deployment@<your project>.iam.gserviceaccount.com · active". Fade; empty frame.
SAY: Last, check that you are authenticated: gcloud auth list. Ours says no credentialed accounts; yours lists the deployment service account as active.

---

## S05 · A test cluster and a first look — `s05_test_cluster.py` · `TestCluster`

SHOW: TRACKER [W] 5. LECTURE 22 · 32–33. Toolbox terminal, prompt from `b03:77`. It types
`gcloud container clusters create test-cluster --num-nodes 2 --zone us-east1-c` → TERM(b15: 2) RED. A GOLD
`cost_tag` slides in: "test cluster · billed per node-hour while it exists"; a YELLOW `▶ your turn`
beside the typed command.
SAY: Now Create Cluster: gcloud container clusters create test cluster, two nodes, zone us east 1 c. Ours stops at once: no active account. Pause and run yours; it costs money every hour it exists.

SHOW: The terminal shrinks to a strip. A GREY card (no output panel): "yours: a short wait · a table with
`test-cluster` · kubeconfig entry generated". Beside it two node boxes, each with one TEAL Pod, and a GREY
chip "slide 32: 1 node · README: 2 nodes".
SAY: Yours takes a short wait, prints a table, and adds an entry to your kubeconfig so kubectl knows where to go. The slide makes one node; the README two, so two copies can land on different machines.

SHOW: TRACKER [W] 5 · extra. A second terminal `laptop · stand-in`, prompt `student@laptop:~$`, tags
`extra` and `stand-in: kind, not GKE`. It types line 1 of `k01` (folds) → TERM(k01: 2–7, 15, 17, 19, 21,
23, 25, 27, 29, 30). Lines 5–7 (`control-plane`, `worker`, `worker`) PURPLE.
SAY: To keep going, we start a small real cluster on the laptop with a tool called kind: one control plane, two workers. Same API server, same kubectl, same YAML, but no Google. It is not in the README; don't run it.

SHOW: The terminal fades. V1 returns, its cluster outline now GREY dashed with the tag `stand-in: kind,
not GKE`; the control plane loses its "run by Google" caption and shows a GREY chip "a container you can
see"; two workers remain.
SAY: Here even the control plane is a container we can see; on GKE, Google hides it.

SHOW: TRACKER [W] 6. LECTURE 22 · 37. A schematic console (tag `illustration`, no logo), README card
`README.md · lines 545–549`: a path that lights one crumb per phrase, "Kubernetes Engine › Clusters ›
test-cluster › Nodes › node › Pods"; then a second panel "Compute Engine › VM instances" with two BLUE
rows "node VM".
SAY: Next, look around the console: Kubernetes Engine, your cluster, its nodes, and the Pods on each node. In Compute Engine, your nodes are ordinary virtual machines.

SHOW: TRACKER [W] 7 · extra. LECTURE 22 · 34. Toolbox terminal, title `laptop · toolbox · stand-in`, tags
`extra`, `stand-in: kind, not GKE`. It types `kubectl version` → TERM(k02: 2, 4); `v1.34.12-gke…` and
`v1.34.11` glow YELLOW together.
SAY: Then try some kubectl commands. First an extra, kubectl version: the dispatcher picked a client that matches the server's version.

SHOW: TRACKER [W] 7. LECTURE 22 · 35. It types `kubectl get all` → TERM(k03: 2–3); line 3
`service/kubernetes` ORANGE, a GREY chip "namespace: default".
SAY: The first README command, get all, shows only a service named kubernetes, the door to the API server itself. We are looking in the namespace called default; more on that later.

SHOW: It types `kubectl get all --all-namespaces` → TERM(k04: 2, 5, 9, 10, 14, …, 18–19); then
`kubectl get pods --all-namespaces` → TERM(k05: 2–15). In `k05`, lines 5, 9, 10, 14 (etcd,
kube-apiserver, kube-controller-manager, kube-scheduler) glow BLUE, and a small V1 thumbnail lights the
matching four boxes; the namespace column `kube-system` ORANGE.
SAY: With all namespaces, kube system appears, and here you can spot the control plane by name: etcd, the API server, the controller manager, the scheduler. On GKE those stay hidden.

SHOW: It types `kubectl get componentstatuses` → TERM(k06: 2–6), line 2 ORANGE with a GREY chip
"deprecated since 1.19: expected"; then `kubectl get nodes` → TERM(k07: 2–5); line 3 `control-plane`
GREY with a chip "GKE: not listed", lines 4–5 GREEN. A YELLOW `▶ your turn` beside the last command. Fade;
empty frame.
SAY: Component statuses prints a deprecation warning, which is expected, then three healthy lines. Get nodes is the better check: three nodes ready here; yours shows two workers and no control plane. Pause and try all five.

---

## S06 · Two objects: a Deployment and a Service — `s06_tic_tac_toe.py` · `TicTacToe`

SHOW: TRACKER [W] 8. LECTURE 22 · 38–39. **V3 `LabelLink`, picture first**: a GREEN card `Deployment ·
web · keep 2` emits two TEAL Pods (each gets a PINK sticker `run: web`); a PINK door `Service · web ·
:80` throws a lasso around both. On "The Deployment says" the GREEN card *TransformFromCopy*s into
CODE(src/deployment/deploy-k8s-tic-tac-toe.yml: 3–14) on the left (GREEN bracket "Deployment: what runs in
a Pod, how many copies, keep them running"); on "The Service says" the PINK door does the same into
CODE(src/deployment/deploy-k8s-tic-tac-toe.yml: 24–35) on the right (PINK bracket "Service: how traffic
reaches them; lets Pods die"). The picture shrinks to a strip under the panels.
SAY: The warm-up deploys a small game, tic-tac-toe, from one file with two objects. The Deployment says what runs in a Pod, how many copies, and to keep them running. The Service says how traffic reaches them, and lets Pods die.

SHOW: LECTURE (held). Line 7 `replicas: 2` GREEN; lines 9–10 (`matchLabels: run: web`) and 13–14
(`labels: run: web`) PINK on the left, lines 33–34 (`selector: run: web`) PINK on the right. A GREY chip
"slide 39 trims these lines" (tag `erratum`). The PINK sticker on each Pod in the strip and the PINK lasso
Indicate together with lines 13–14 and 33–34.
SAY: The slide trims the lines that glue them together. The template gives every Pod a label, run web, and both objects find their Pods by that label, not by name.

SHOW: The left panel scrolls to CODE(src/deployment/deploy-k8s-tic-tac-toe.yml: 15–22): line 17
`dlops/tic-tac-toe` TEAL, line 21 `containerPort: 8080` PINK. A PINK path of three ports draws under the
panels: `port: 80` (line 30) → `targetPort: 8080` (line 32) → `containerPort: 8080` (line 21).
SAY: Each Pod runs the image dlops tic-tac-toe, listening on port 8080. The Service listens on port 80 and forwards to 8080.

SHOW: The panels fade. Toolbox terminal (tags `stand-in: kind, not GKE`), strip at the bottom; above it a
small V1. It types `kubectl apply -f deploy-k8s-tic-tac-toe.yml` → TERM(k10: 2–3) GREEN. LECTURE 22 ·
24–25. On "wish" a GREEN card flies kubectl → API server → etcd; on "scheduler" the scheduler picks two
workers; on "kubelets" two kubelets start two TEAL Pods.
SAY: Deploy the app: kubectl apply, dash f, and the file. Apply only hands a wish to the API server; the scheduler picks two nodes, and their kubelets start the containers.

SHOW: TRACKER [W] 8 · extra. It types line 1 of `k12` (extra; folds) → TERM(k12: 2–4, 6 wrap, 7 wrap); the
NODE column of lines 6–7 (`test-cluster-worker2`, `test-cluster-worker`) YELLOW.
SAY: An extra check, rollout status, watches it happen: zero, then one of two available, then rolled out, on two different workers.

SHOW: TRACKER [W] 9. LECTURE 22 · 38. It types `kubectl get services` → TERM(k11: 2–4). On line 4: `LoadBalancer`
BLUE, `<pending>` YELLOW, `80:31366/TCP` PINK with three small PINK labels beneath it: "80 outside",
"31366 on every node", and "8080 in the Pod".
SAY: Next, kubectl get services. The web Service is a load balancer: port 80, mapped to 31366 on every node, and on to 8080 in the Pod. Its external IP says pending.

SHOW: It types `kubectl get services` again (same README command) → TERM(k13: 4); `43s` and `<pending>`
YELLOW. V1 small above, all lamps dark. A YELLOW question card.
SAY: 43 seconds later it still says pending. Which part of the cluster picture is waiting, and on what?
PONDER(8 s, "EXTERNAL-IP is still <pending>\nafter 43 seconds.\nWhich part of the cluster is waiting,\nand on what?")

SHOW: LECTURE 22 · 24. The controllers lamp lights YELLOW; the PINK arrow to "cloud provider API" turns
RED on the stand-in with a GREY chip "no cloud here"; a GREY-dashed ghost arrow beside it, "GKE: a
load balancer and an IP, after a short wait".
SAY: The controllers, waiting on the cloud provider. On GKE they ask Google for a load balancer and an address, which arrives after a short wait. The kind cluster has no cloud to ask.

SHOW: TRACKER [W] 10. A schematic browser window (tag `illustration`, `browser_window`), address bar
`http://<EXTERNAL-IP>`, inside it a 3 × 3 grid of empty squares; README card `README.md · lines 574–575`;
a YELLOW `▶ your turn` beside the address bar.
SAY: Pause: on GKE, wait for the external IP, copy it into your browser, and the game appears.

SHOW: TRACKER [W] 10 · extra. Toolbox terminal (tags `extra`, `stand-in: kind, not GKE`). It types line
1 of `k57` (extra; folds) → TERM(k57: 2, 13, 14); `HTTP/1.1 200 OK` GREEN. LECTURE 22 · 29: a GREY chip
(tag `erratum`): "a port-forward started in the toolbox opens inside the toolbox → test it with curl
there". Fade; empty frame.
SAY: On the stand-in, an extra: port forward to the Service, then curl: 200 OK. The lecture suggests it for your browser, but from the toolbox the port opens inside the container: test it there.

---

## S07 · Desired state: Pods that come back — `s07_self_healing.py` · `SelfHealing`

SHOW: TRACKER [W] 10 · extra. LECTURE 22 · 7. A small GREY redrawing of S01's operator restarting
`API 1` by hand; the operator figure *transforms* into a BLUE-greyed "controllers" box. `AsksChecklist`
small, top right.
SAY: Back to the night-time problem: who restarts the container? In Kubernetes, a controller does. Let's watch one work.

SHOW: LECTURE 22 · 36. Toolbox terminal (tags `extra`, `stand-in: kind, not GKE`). It types line 1 of
`k50` (extra; folds) → TERM(k50: 2, 3–4 wrap, 6–7 wrap, 9–11 wrap); line 2 GREY. Then **V4
`ControllerLoop`** builds above by *TransformFromCopy*: `deployment.apps/web` from line 3 flies up and
becomes the GREEN card `deployment.apps/web · replicas: 2`; `replicaset.apps/web-5cd9789488` from line 6
becomes the GREEN ReplicaSet card; the two Pod names from lines 9–10 become TEAL Pods
`web-5cd9789488-5h48s`, `web-5cd9789488-bmkj5`, whose names split on arrival into three coloured
segments (GREEN `web` · GREEN-outlined `5cd9789488` · TEAL suffix). The terminal then dims to 40 %.
SAY: An extra listing shows the chain. The Deployment named web owns a ReplicaSet, whose name adds a hash of the Pod template. The ReplicaSet owns two Pods, each with that hash and a short random suffix.

SHOW: The terminal shows TERM(k50: 20–22); the `pod-template-hash=5cd9789488` part of lines 21–22
YELLOW, `run=web` PINK.
SAY: The labels confirm it: every Pod carries the template hash and the run web label.

SHOW: LECTURE 22 · 18, 30. The terminal shrinks to a strip. Around the controllers box a ring of three
YELLOW arrows "observe → compare → act"; a counter beside it "desired 2 · actual 2" GREEN, with a small
dial glyph (two arcs and a needle) whose needle swings back on "keeps it true"; a GREY caption "you set
the number; the controller keeps it true".
SAY: The ReplicaSet controller runs a loop: observe the Pods, compare with the number you declared, act on the difference. You set the number; the controller keeps it true, like a thermostat.

SHOW: The terminal grows back. It types line 1 of `k55` (extra; folds) → TERM(k55: 2, 7–10 wrap, 13); in V4 the counter jumps to
"desired 4", two Pods grow, one on each worker; line 13's `+ 1 more...` PINK. Then line 1 of `k56`
(extra) → TERM(k56: 2, 4–5); two Pods fade, the counter returns to 2 (V4 goes 2 → 4 → 2 before any
delete). A GREY chip `Milestone 5 · manual scaling`.
SAY: First, one more extra: kubectl scale, replicas 4. Two more Pods appear, spread over both workers, and the Service already lists them. Scale back to 2, and remember this command: your project's Milestone 5 asks for it.

SHOW: Pod `…-5h48s` glows YELLOW. A YELLOW question card.
SAY: Now delete one of the two web Pods. A second later, how many web Pods are there, and which part of the new name stays the same?
PONDER(8 s, "Delete one of the two web Pods.\nA second later: how many?\nWhich part of the new name\nstays the same?")

SHOW: It types line 1 of `k53` (extra; folds) → TERM(k53: 2–5); line 5 `ContainerCreating` YELLOW. In
V4: Pod `…-5h48s` is struck and fades; the counter flips RED "desired 2 · actual 1"; a new Pod grows with
the same GREEN-outlined middle segment and a new TEAL suffix `lmk52`.
SAY: Two. The delete returns, and a new Pod is already being created. Its name keeps the ReplicaSet hash, with a new suffix.

SHOW: It types line 1 of `k54` (extra) → TERM(k54: 2–4 wrap); both `Running` GREEN; the counter returns
GREEN "desired 2 · actual 2".
SAY: 15 seconds later, both run. Nobody logged in: the loop noticed, and acted.

SHOW: The `AsksChecklist` grows a little: "Failover" ticks YELLOW, with a GREY footnote "a restart, not a
hot standby · keep replicas: 2", then shrinks back. LECTURE 22 · 13, 39.
SAY: That ticks failover, with an honest footnote: it is a restart, not a hot standby. With one replica there is a short gap, which is why the game's file asks for two replicas.


SHOW: The terminal fades. Two GREY cards: left (GREY dashed) "L20 · Docker restart policy · same
machine", right GREEN "ReplicaSet · a new Pod wherever there is room". A WHITE line under them: "Declare,
don't script." Fade; empty frame.
SAY: In lecture 20, Docker restarted a container on the same machine. A ReplicaSet places a new Pod wherever there is room. Declare the result, don't script the steps.

---

## S08 · Labels, Services, namespaces, then delete — `s08_stable_names.py` · `StableNames`

SHOW: TRACKER [W] 10 · extra. LECTURE 22 · 39. Two small strips: `k50:10` and `k54:4` with their IP
columns (`10.244.1.2`, `10.244.1.7`) YELLOW (never read). **V3**: a PINK lasso closes around "every Pod
wearing `run: web`"; under it TERM(k50: 19) (`endpoints/web 10.244.1.2:8080,10.244.2.2:8080`) PINK, with a
GREY chip "recorded before the delete in S07"; then a V3 animation (tag `illustration`) swaps `10.244.1.2`
for `10.244.1.7` in the list.
SAY: Pods are mortal: the new Pod got a new address. So how does traffic find it? The Service keeps a list of every Pod wearing its label, and that list follows the Pods.

SHOW: Toolbox terminal (tags `extra`, `stand-in: kind, not GKE`). It types line 1 of `k52` (extra; folds)
→ TERM(k52: 4–5, 11). A PINK DNS card forms beside it: `web.default.svc.cluster.local → 10.96.52.79`, and
a GREY line ties `10.96.52.79` to the CLUSTER-IP of `k11:4` (small inset).
SAY: An extra from a throwaway Pod: the name web dot default dot svc dot cluster dot local points to the Service, and fetching just web returns the game page. The name stays while the Pods change.

SHOW: A small GREY-dashed V5 chip: TEAL `api` → PINK `vector-db:8000` "(part 2)".
SAY: This is how the cheese app's API will find its database: by the Service name, vector db.

SHOW: It types `kubectl exec --stdin --tty deployment/web -- /bin/sh` (extra; `k51:1`), then at the `$`
prompt `hostname; ls; exit` (`k51:2`) → TERM(k51: 3–4); line 3 TEAL, with a GREY chip "recorded before
the delete in S07".
SAY: Another extra: kubectl exec into the web Deployment. Hostname prints the name of one Pod, and the game's files are inside. The README shells into the API the same way.

SHOW: LECTURE 22 · 35. It types line 1 of `k63` (extra; folds) → TERM(k63: 2–7, 8–10). Beside it GREY
folder icons, one per namespace: `default` and `kube-system` ORANGE, then a GREEN folder
`cheese-app-namespace` appears empty and is deleted.
SAY: Why did get all look empty? Namespaces: folders for objects. Without a flag, kubectl looks only in default; this extra lists them, then creates and deletes the cheese app namespace.

SHOW: LECTURE 22 · 27. The `KubectlGrammar` card returns: `-n cheese-app-namespace` drops into the
flags slot, PINK.
SAY: So in part 2, every command about the app gets dash n, cheese app namespace, in the flags slot.

SHOW: TRACKER [W] 11 · extra. It types line 1 of `k80` (extra; `typed crop "deploy-k8s-tic-tac-toe.yml"`)
→ TERM(k80: 2–3). A GREY chip: "on GKE: releases the load balancer while the cluster still exists"; a
YELLOW `▶ your turn` beside the typed line.
SAY: Before deleting the cluster, an extra tip: kubectl delete with the same file. On GKE, this releases the load balancer while the cluster still exists.

SHOW: TRACKER [W] 11. LECTURE 22 · 40. It types `gcloud container clusters delete test-cluster --zone us-east1-c`
→ TERM(b51: 2) RED. A GREY chip: "yours: Do you want to continue (Y/n)? → Y".
SAY: Then delete the cluster: gcloud container clusters delete test cluster, zone us east 1 c. Yours asks whether to continue; answer yes.

SHOW: Laptop terminal `laptop · stand-in` (tags `extra`, `stand-in: kind, not GKE`). It types line 1 of
`k81` (`typed crop "--name test-cluster"`) → TERM(k81: 2–3). The GREY-dashed stand-in cluster drawing
fades out.
SAY: We delete the stand-in too.

SHOW: LECTURE 22 · 44. A GOLD card centre: "Don't forget to delete"; the GOLD `cost_tag` from S05 slides in
and its meter stops. A YELLOW `▶ your turn` beside the card. Fade; empty frame.
SAY: The lecture's last word fits here: don't forget to delete. Pause, check that your test cluster is gone, and part 1 is done.

---

## S09 · The cheese app's cluster, as code — `s09_blueprint.py` · `Blueprint`

SHOW: No tracker. LECTURE 22 · 41. Two GREY README cards: "Deployment with Scaling using Kubernetes ·
392" (a PINK arrow "course link lands here" points at it) and "Create & Deploy Cluster · 436" (a GREY chip
"the cluster steps", tag `erratum`). Under them the two tracker titles in small YELLOW.
SAY: Part 2: the cheese app on GKE, as Pulumi code. The course link lands on Deployment with Scaling using Kubernetes; the cluster steps continue under the next heading, Create and Deploy Cluster.

SHOW: LECTURE 22 · 21–22. **V5 `CheeseBlueprint`**: the GREY-dashed L20 VM (`nginx`, `api-service`,
`frontend`, `vector-db`, dashed `loader`) *dissolves into* the V1 cluster. A two-column table builds on
the right, one line per phrase: "container → Deployment" (three TEAL boxes become GREEN Deployment cards
with Pods), "loader → Job" (the dashed loader becomes a GREEN Job card).
SAY: Here is the plan, piece by piece from lecture 20. Each long-running container becomes a Deployment. The one-shot loader becomes a Job: it retries a failed run a few times, and once it succeeds, it stays done.

SHOW: Table lines: "container names on a Docker network → Services + DNS names" (PINK name tags
`frontend`, `api`, `vector-db`); "folders on /mnt/disk-1 → two PVCs on cloud disks" (BLUE disks
`persistent-pvc 5Gi`, `chromadb-pvc 10Gi`).
SAY: Container names on a Docker network become Services with DNS names. The folders on the VM disk become two persistent volume claims, each backed by a cloud disk.

SHOW: Table lines: "nginx container → NGINX Ingress controller + Ingress" (`nginx-f5`,
`cheese-app-ingress`); "gcp-service.json → Workload Identity (no key)"; "restart policy → ReplicaSet";
"one VM → node pool 1–2".
SAY: The nginx container becomes an Ingress controller with an Ingress rule. The JSON key becomes Workload Identity, with no key file at all. One machine becomes a pool of one or two nodes.

SHOW: The table fades. Around the cluster a BLUE frame `cheese-app-vpc · subnet 10.0.0.0/19`; the nodes'
small public-IP badges peel off ("private nodes"); a BLUE funnel "Cloud NAT · outbound only" at the
VPC edge; a GREEN frame `cheese-app-namespace` around the app; a BLUE load-balancer door at the edge. A
small GREY scene chip lands beside each label that returns: `Workload Identity → S12`, `Ingress → S13`,
`PVC → S15`.
SAY: Around it, a private network. The nodes get no public addresses; a Cloud NAT gateway lets them reach out, for example to pull Chroma from Docker Hub. The app sits in one namespace, behind one load balancer.

SHOW: CODE(src/deployment/deploy_k8s/__main__.py: 19–30), then it scrolls to (31–40). The four calls light
in turn, each with a GREY chip naming its file: `create_network.py`, `create_cluster.py`,
`setup_containers.py`, `setup_loadbalancer.py`. A small inset of line 17 `setupSSL = False` with a GREY
chip "HTTPS variant: off".
SAY: The program in deploy k8s says the same in four calls, one per file: the network, the cluster, the containers, the load balancer. Line 17 keeps the HTTPS variant switched off.

SHOW: A GOLD cost card (`cost_tag`), one line per phrase: "regional cluster · management fee", "1–2 ×
n2d-standard-2 nodes", "load balancer", "Cloud NAT", "2 disks"; total "≈ $5–8 per day · our estimate ·
check the pricing calculator". A GREY chip: "registry images outlive destroy (S16)". Fade; empty frame.
SAY: While it is up, it costs money: the fee of a regional cluster, one or two nodes, a load balancer, one NAT gateway and two disks. By our estimate, roughly five to eight dollars a day: check the pricing calculator, and destroy it the same day.

---

## S10 · Setup and the images stack — `s10_images.py` · `ImagesStack`

SHOW: TRACKER [D] 1. A schematic console list (tag `illustration`), README card
`README.md · lines 398–402`: the five APIs tick GREEN one after another; a sixth line slides in YELLOW,
"Vertex AI API · the API Pods call it" (tag `extra`).
SAY: This section enables the five APIs again; turn on the Vertex AI API too, which the API Pods call.

SHOW: Two key cards (tag `illustration`, README card `README.md · lines 236–259`): a BLUE key with a RED
rim `deployment` "the toolbox, Pulumi · and here: the nodes' identity"; a GREEN key `gcp-service` "the
API Pods · through Workload Identity · no key file in the cluster".
SAY: You also need the two service accounts from lecture 20. The deployment account does what the toolbox does, and here it is also the nodes' identity. The gcp service account is for the API Pods, with no key file.

SHOW: Two GREY cards (tag `illustration`): "IAM › Service accounts › gcp-service › Permissions: grant
`deployment` · Service Account Admin" with a GREY chip "unverified here · follows from the documented
roles"; under it a GREY chip "or, as project owner: `gcloud iam service-accounts add-iam-policy-binding
gcp-service@<your project>.iam.gserviceaccount.com --member=serviceAccount:deployment@<your
project>.iam.gserviceaccount.com --role=roles/iam.serviceAccountAdmin`" (folds); and "Artifact Registry ›
Create repository: `cheese-app-repository` · location: us", under it a GREEN card (tag `extra · our
spelling`, no output) `gcloud artifacts repositories create cheese-app-repository
--repository-format=docker --location=us`.
SAY: Two one-time steps the README leaves out. The deployment account very likely needs Service Account Admin on gcp service; we could not test this. And create the registry repository, cheese app repository, which no code creates.

SHOW: A laptop terminal strip (tag `extra`): TERM(p05: 2, 6–7, 11) shows `cheese-app-v3` and `secrets`
side by side and `deployment.json` inside `secrets` (a GREY chip "placeholder key for no account").
SAY: The deployment key goes in the secrets folder, beside the repository, as in lecture 20.

SHOW: TRACKER [D] 2, then 3, then 4, fast. The six README commands (README:405–413) appear as a fast
re-type, in README order, each with its one-line output from part 1. A laptop terminal (title `laptop`,
prompt `student@laptop:~/cheese-app-v3/src$`): `cd deployment` → (no output), the prompt becomes
`…/src/deployment$`; `sh docker-shell.sh` → TERM(b03: 31) and the `b03:77` prompt, the title becomes
`laptop · toolbox`; then the four checks at the toolbox prompt: `gcloud --version` → TERM(b10: 2);
`kubectl version` → TERM(b11: 4); `kubectl version --client` → TERM(b12: 2); `gcloud auth list` →
TERM(b13: 3) RED.
SAY: Then the toolbox steps from part 1, the same commands; if the toolbox is still running, the script simply attaches to it.

SHOW: TRACKER [D] 5. A GREY README card `README.md · line 416`: "only required if you have NOT already
done this". It types `cd deploy_images` → (no output); `pulumi stack init dev` → TERM(b20: 2) RED;
`pulumi config set gcp:project ac215-project --stack dev` → TERM(b21: 2) RED, with the GREY
`default_tag` on `ac215-project`.
SAY: Next, the images stack, only if you have not built it before: change into deploy images, pulumi stack init dev, and set G C P project to yours. Ours says Pulumi access token must be set: our bucket login failed, so Pulumi falls back to its cloud service.

SHOW: TRACKER [D] 5 · extra. It types `pulumi login --local` (tag `extra · not for you`) → TERM(c00: 2);
then the two README commands again → TERM(c01: 2) GREEN, `c02` → (no output).
SAY: To show the rest, we point Pulumi at a local folder, a recording workaround: don't run it. Now the stack is created, as yours is.

SHOW: TRACKER [D] 6. It types `pulumi preview --stack dev` → TERM(b22: 2) RED; then (extra, local) the
same command → TERM(c03: 29, 31–33, 40, …, 50–52 wrap, …, 63). Line 29 `pulumi:pulumi:Stack` GREY with a
chip `+1 · the stack itself`, lines 31–33 GREEN, line 40 ORANGE, the timestamp `20261107205032` in line 51
YELLOW (not read), line 63 `+ 4 to create` YELLOW.
SAY: Then pulumi preview, stack dev: three image builds, skipped in a preview, and three tags stamped with the time. Plus 4 to create: three images and the stack itself.

SHOW: The terminal shrinks to a strip. V5 mini: three TEAL images fly to a BLUE "Artifact Registry"
box; the three `-tags` outputs become one PINK pipe labelled `StackReference
organization/deploy-images/dev` running to a GREEN box `deploy_k8s`.
SAY: Those tag outputs matter: deploy k8s looks them up through a stack reference, to know which images to run.

SHOW: TRACKER [D] 7. It types `pulumi up --stack dev -y` → TERM(b23: 2) RED. A GREY-dashed chip "L20 ·
the real build, up to the push · the API image ≈ 5 GB"; a GREY chip "Apple Silicon: a long build is
normal"; a YELLOW `▶ your turn`. Fade; empty frame.
SAY: Last, pulumi up, stack dev, dash y: it builds and pushes three images. Skip it if you did it in lecture 20, with one condition we meet next; otherwise, pause and run it.

---

## S11 · deploy_k8s: config and a 23-resource plan — `s11_plan.py` · `ClusterPlan`

SHOW: TRACKER [C] 1. LECTURE 22 · 41. Toolbox terminal. It types `cd /app/deploy_k8s` (tag `extra · our
spelling`: README:437 says "cd into deploy_k8s from the deployment folder"; a GREY chip "works from either
folder") → (no output); the prompt becomes `…/app/deploy_k8s#`. It types
`pulumi stack init dev` → TERM(b30: 2) RED; then (extra, local) → TERM(c10: 2) GREEN.
SAY: Now Create and Deploy Cluster. From the deployment folder, change into deploy k8s and run pulumi stack init dev: the same token error, and on the local backend, created stack dev.

SHOW: TRACKER [C] 2. It types the three README lines (README:441–443) one after another: `pulumi config
set gcp:project ac215-project` → TERM(b31-1: 2); `pulumi config set
security:gcp_service_account_email deployment@ac215-project.iam.gserviceaccount.com --stack dev` (folds) →
TERM(b31-2: 2); `pulumi config set security:gcp_ksa_service_account_email
gcp-service@ac215-project.iam.gserviceaccount.com --stack dev` (folds) → TERM(b31-3: 2); all three RED
lines dim once the third prints. Then (extra, local) the same three re-run as one quick block,
`type_time=0.5` each, no output (`c11-1..3`), with a GREEN chip `✓ local · same three keys`. Every
`ac215-project` gets the GREY `default_tag`.
SAY: Then three config keys: your project, and two service account emails, deployment and gcp service. Replace ac215 project with yours in all three.

SHOW: CODE(src/deployment/deploy_k8s/create_cluster.py: 9–12). Line 9 BLUE with a GREY chip "→ the nodes'
service account (line 50)"; lines 10–12 GREEN with a chip "→ the API's Kubernetes service account (line
158)".
SAY: Line 9 takes the deployment email: the nodes run as that account. Line 10 takes the gcp service email, which the API Pods will act as.

SHOW: TRACKER [C] 2 · extra. It types `pulumi config; pulumi stack ls` (extra) → TERM(c12: 2–8), line 8
masked to `sa_000000000000000000000`; lines 3 and 8 GREY with a chip "leftovers · unused"; lines 4, 6, 7
GREEN.
SAY: An extra, pulumi config, lists your three keys and two leftovers from the committed file, setup SSL and an SSH user, which the program never uses. A typo in a key name fails quietly later, so check this list.

SHOW: TRACKER [C] 3. It types `pulumi preview --stack dev --refresh` → TERM(b32: 2) RED; then (extra, local)
the same → TERM(c13: 7, 10, …, 31–34, 37–38). Line 34 RED. Beside the terminal, CODE(src/deployment/deploy_k8s/setup_containers.py:
68–71) with line 70 RED, and above it a small CODE(src/deployment/deploy_k8s/setup_containers.py: 10–13) with
line 10 PINK.
SAY: Then Preview: pulumi preview, stack dev, refresh. On the local backend, a Python error at line 70 of setup containers: none type is not subscriptable. The program asked the images stack for its tags, and got nothing.

SHOW: The panels fade. One BLUE state bucket holds two stacks: `deploy_images` with an empty GREY outputs
box ("init + preview only, no up") and `deploy_k8s`; the PINK `StackReference` pipe between them reaches
the empty box and breaks RED. Then a `pulumi up` stamp fills the box with three tags and the pipe joins
GREEN; caption "same bucket · up finished".
SAY: You see this if the images stack never finished pulumi up in this same state bucket. Skipping it is safe only when it already ran there.

SHOW: TRACKER [C] 3 · extra. Tags `extra`, `placeholder image tags · nothing built`. It types `pulumi
preview --stack dev --refresh` → TERM(c20: 8–11, 13–14, 16–33 as a fast scroll, 45). **V6
`ResourceTree`** grows beside it from the printed lines as seven group boxes in dependency order (text
≥ 20 pt): `network ×4` BLUE, `cluster + pool ×2` BLUE, `provider ×2` PURPLE, `identity ×3` GREEN/BLUE,
`storage ×2` GREEN, `app ×7` GREEN (3 Deployments, 3 Services, Job), `ingress ×2` (Helm `nginx-f5`,
Ingress); the group being spoken expands in place to its member names, then collapses; the badges sum to
the counter `+ 23 to create` YELLOW.
SAY: So we gave the program a stand-in images stack with placeholder tags; nothing is built. Now the real plan appears: the network, the cluster, the node pool, the Kubernetes objects, and plus 23 to create.

SHOW: In V6, two PINK dashed outlines blink: `StackReference organization/deploy-images/dev` and
`nginx-ingress-service` ("reads"). The terminal shows TERM(c20: 35–42): line 38 `cluster_name:
"cheese-app-cluster"` GREEN, the `[unknown]` values GREY.
SAY: Two more lines are lookups, not counted in the 23: the stack reference and the nginx Service. In the outputs, only the cluster name is known; the address and the URL wait until the cluster exists.

SHOW: A YELLOW `▶ your turn` beside the preview command. Fade; empty frame.
SAY: Pause and run your preview: you should see the same 23, with real image tags.

---

## S12 · pulumi up: what builds, in what order — `s12_pulumi_up.py` · `PulumiUp`

SHOW: TRACKER [C] 4. Toolbox terminal. It types `pulumi up --stack dev --refresh -y` → TERM(b33: 2) RED;
then (extra, local; tags `extra`, `placeholder image tags · nothing built`) the same → TERM(c21: 45, 47, 55,
58, 165 wrap, 166 crop "account not found\"}"). Line 58 `**creating failed**` RED; line 166's
`invalid_grant` RED.
SAY: Then the big one: pulumi up, stack dev, refresh, dash y. On the local backend the update starts, and the very first resource, the network, fails: invalid grant, account not found.

SHOW: The terminal shrinks to a strip. A GREY chip: "the first resource that needs Google · from here:
a picture, not a recording". A YELLOW `▶ your turn` and a GOLD `cost_tag` "the meter starts".
SAY: The network is the first thing that needs Google, so from here on this is a picture. Pause and start yours; from now on, the meter runs.

SHOW: LECTURE 22 · 24–25. V6 again (tag `illustration`, the seven groups; no V1 in this scene until the
nginx beat), filling in dependency order: the `network` group expands, BLUE `cheese-app-vpc` →
`cheese-app-subnet` fill; then two branches fill side by side: `cheese-app-router` → `cheese-app-nat`, and
`cheese-app-cluster` with a GOLD-ringed clock "15–25 min · our estimate".
SAY: Pulumi follows the dependencies. First the network and its subnet. Then, side by side, the router with its NAT gateway, and the cluster, the long wait: a quarter of an hour or more, by our estimate.

SHOW: `cheese-app-pool` fills, its group badge showing two small node boxes. A GREY card "kubeconfig,
built from the cluster's outputs" slides into the PURPLE provider node `gke_k8s_v2`; CODE(src/deployment/deploy_k8s/create_cluster.py:
134–138) with line 137 `depends_on=[node_pool]` YELLOW.
SAY: Then the node pool. A Kubernetes provider, built from the cluster outputs, waits for that pool, so no Pod is created before there are nodes.

SHOW: The code panel fades. The groups fill: `identity` (GREEN `cheese-app-namespace`, `api-ksa`, then
the BLUE `api-gsa-wi-user`), `storage` (`persistent-pvc`, `chromadb-pvc`), then in `app` the `frontend`,
`vector-db` and their Services.
SAY: Through it come the namespace, the service account of the API and its binding, the two disk claims, the frontend and the vector database.

SHOW: The GREEN `vector-db-loader` Job node fills, with V4's Job cousin: one TEAL Pod runs and turns
`Completed` GREY; a YELLOW hourglass "Pulumi waits for Complete" sits between the Job and the `api` node.
CODE(src/deployment/deploy_k8s/setup_containers.py: 319–321), line 320 YELLOW. Then `api` fills.
SAY: Next, the loader Job fills the vector database. Pulumi creates the API only after the Job completes: lines 319 to 321 set that dependency.

SHOW: LECTURE (held). The code panel fades. In parallel (a second branch of V6): `nginx-f5` fills; in a
small V1 inset that fades in for this block only, its Service (`type: LoadBalancer`) lights the
controllers lamp, and the arrow to "cloud provider API" turns GREEN this
time; a BLUE door with `<IP>` returns; `<IP>.sslip.io` writes PINK; `cheese-app-ingress` fills last.
SAY: In parallel, Helm installs the nginx Ingress controller. Its Service asks for a load balancer, so the controllers ask the cloud for an address: the part 1 lamp, green this time. That address becomes a host name, and the Ingress comes last.

SHOW: Identity, beat 1: a GREY kubeconfig card with `user: exec: gke-gcloud-auth-plugin` PURPLE (a chip
"fix 2 from S04"), beside a GREY-dashed stand-in card from TERM(k65: 4, 6–7) (`client-certificate-data:
<redacted>`, tag `stand-in: kind, not GKE`) for contrast; the kubectl arrow into the API server.
SAY: Identity, in two parts. Pulumi and kubectl reach the API server through the GKE auth plugin, fix two from the toolbox, so there is no cluster password.

SHOW: Identity, beat 2: the TEAL API Pod wears a GREEN badge `api-ksa`; at the edge, at a BLUE door
"Vertex AI", the badge is swapped for a GREEN key `gcp-service` ("Workload Identity"); a GREY chip "no
JSON key inside the cluster".
SAY: And the API Pod wears its Kubernetes service account, which Workload Identity swaps for gcp service at the door to Vertex AI. No JSON key sits in the cluster.

SHOW: CODE(src/deployment/deploy_k8s/create_cluster.py: 192–198) with lines 195–197 YELLOW; a GREY chip
"runs once, at create, inside this toolbox · docker-shell.sh runs it with --rm". The toolbox icon fades:
"next session: no kubeconfig (S14)". The code panel fades; a GREY "if yours stops" card, one line each:
"403 at api-gsa-wi-user → Service Account Admin (S10)"; "stuck at vector-db-loader → logs (S15), then
`kubectl delete job vector-db-loader -n cheese-app-namespace` and up again"; "ImagePullBackOff → `kubectl
describe pod … -n cheese-app-namespace`: repository missing, or images not built"; "quota → delete
lecture 20's VM, request more"; and a GREEN chip "success: Outputs with app_url (S14)". Fade; empty
frame.
SAY: Keep in mind: Pulumi connects kubectl once, inside this toolbox, which is removed when you exit. The next session starts unconnected.

---

## S13 · The journey of one click — `s13_one_click.py` · `OneClick`

SHOW: TRACKER [C] 4. LECTURE 22 · 5, 21, 38–39. Comparison strip, three panels: GREY-dashed "L20 · one
nginx container in front"; "tic-tac-toe · one LoadBalancer per app" (a BLUE door per app); "cheese app ·
one door with a receptionist" (one BLUE door, a figure `nginx` behind it, three PINK paths).
`AsksChecklist` small, top right.
SAY: Lecture 20 put one nginx container in front. The game opened its own load balancer, one door per app. The cheese app opens one door, with a receptionist behind it.

SHOW: A README card `README.md · line 457`, then **V7 `RequestJourney`**, the README's diagram
(README:459–474) redrawn left to right as lanes: GREY `Browser` → BLUE `LoadBalancer Service` → TEAL
`nginx Ingress Controller` → PINK `frontend · ClusterIP 3000` (path `/`) and PINK `api · ClusterIP 9000`
(path `/api-service`) → PINK `vector-db · ClusterIP 8000`; a GREEN `vector-db-loader` Job below.
SAY: The README draws the path: browser, load balancer, the nginx Ingress controller, then the frontend on 3000 or the API on 9000, and the vector database on 8000.

SHOW: The README's dotted arrow appears as a GREY ghost from `vector-db` to the Job (tag `erratum`), then
flips around: a GREEN dotted arrow from the Job into `vector-db`, "one-time load".
SAY: A small slip: the README draws the dotted arrow from the vector database to the loader. The data flows the other way, from the Job into the database.

SHOW: LECTURE 22 · 24, 26. A packet glyph leaves the browser: a PINK bubble `<IP>.sslip.io → <IP>`; it
passes the BLUE load-balancer door (in a small V1 inset, the cloud-provider arrow glows GREEN), reaches a
node, and stops at the `nginx` figure; a GREY chip "installed by Helm".
SAY: Follow one click. Your IP dot sslip dot io points back to that same IP, with no setup at all. The packet passes the cloud load balancer and lands on the nginx controller.

SHOW: CODE(src/deployment/deploy_k8s/setup_loadbalancer.py: 79–90): line 79 `host=host` PINK, line 84
`path="/api-service"` YELLOW, line 90 `number=9000`; then it scrolls to (96–104): line 97 `path="/"`, line
103 `number=3000`. The `nginx` figure holds a routing card built from them: a PINK header `host:
<IP>.sslip.io` (from line 79), under it "`/api-service` → api:9000" and "`/` → frontend:3000". On "for
that host" the header Indicates.
SAY: The Ingress rule starts with the host name: for that host, slash api service goes to the API on 9000, every other path to the frontend on 3000. The controller follows that rule, like the nginx dot conf of lecture 20, now generated.

SHOW: A packet `/api-service/status` reaches the `api` Pod with its prefix intact (a GREY-dashed pair of
scissors from L20 appears and is crossed out). CODE(src/api-service/api/service.py: 13) and
(src/api-service/api/service.py: 50) as two one-line insets; a GREEN chip `ROOT_PATH=/api-service`
(`setup_containers.py:310–311`). The Pod answers a PINK bubble `{"version": "3.0"}`.
SAY: This time the prefix is kept: nothing strips it. The API mounts itself under its root path, slash api service, so slash api service slash status answers version three point zero.

SHOW: A second packet `/` returns a GREY page icon to the browser; the page *spawns* a new packet from the
browser itself to `/api-service/…`. CODE(src/frontend-react/.env.production: 2) inset,
`NEXT_PUBLIC_BASE_API_URL=/api-service` YELLOW.
SAY: The page comes from the frontend; then your browser calls the API directly, at slash api service.

SHOW: The `api` Pod sends a PINK arrow to `vector-db:8000`; S08's DNS card flashes beside it.
SAY: Inside the cluster, the API reaches Chroma by its Service name, vector db, on port 8000.

SHOW: A new packet leaves the browser with a PINK label `http://<IP>/` (no `.sslip.io`). A YELLOW question
card.
SAY: Now open the bare IP: the same load balancer, without sslip dot io. What answers?
PONDER(8 s, "http://<IP>/ — the same load balancer,\nwithout .sslip.io.\nWhat answers?")

SHOW: The packet reaches the `nginx` figure, which checks the header of its card: `Host: <IP>` ≠
`<IP>.sslip.io` (the header flashes RED); the packet bounces back RED `404`.
SAY: The nginx controller answers 404 Not Found. The rule matches only that host name, so the same door with the wrong name finds no route. Use the app URL from the outputs.

SHOW: The `AsksChecklist` grows a little: "Load balancing" ticks YELLOW, with a GREY footnote "cloud LB at
the door · nginx · Services across Pods". Fade; empty frame.
SAY: That ticks load balancing: the cloud load balancer at the door, nginx behind it, and each Service spreading requests across its Pods.

---

## S14 · kubectl on the app, and the outputs — `s14_explore.py` · `ExploreApp`

SHOW: TRACKER [C] 5. LECTURE 22 · 34–36. Toolbox terminal, a fast montage of the five README commands
(README:478–480, 484–485): `kubectl get all` → TERM(b40: 7); `kubectl get all
--all-namespaces` → TERM(b41: 7); `kubectl get pods --all-namespaces` → TERM(b42: 7); `kubectl get
componentstatuses` → TERM(b43: 7); `kubectl get nodes` → TERM(b44: 7). Each line 7 RED.
SAY: Next, try some kubectl commands. With no cluster here, all five say connection refused. You will see exactly this in any new toolbox session: the kubeconfig Pulumi wrote went away with the old container.

SHOW: TRACKER [C] 5 · extra. LECTURE 22 · 33. It types `gcloud container clusters get-credentials
cheese-app-cluster --zone us-central1 --project your-gcp-project` (extra; folds) → TERM(b52: 2) RED. Then
a GREEN card (tag `extra · our spelling`, no output): `gcloud container clusters get-credentials
cheese-app-cluster --region us-central1 --project <your project>`, `--region` YELLOW, with a GREY chip
(tag `erratum`) "the code passes the region to `--zone`".
SAY: The fix is the command Pulumi ran, an extra here: gcloud container clusters get credentials, cheese app cluster. The code passes the region to the zone flag; write region, which says what it means.

SHOW: A GREY card "what yours shows" (no output panel), one line per phrase: "`get all` → only
`service/kubernetes`"; "`-n cheese-app-namespace` → frontend-…, vector-db-…, api-…, the nginx controller,
vector-db-loader-… `Completed`, job.batch/vector-db-loader 1/1"; "`get nodes` → 1 node (2 if the
autoscaler added one)". Beside it two small GREY thumbnails of `k03` and `k07` from S05, tagged `stand-in:
kind, not GKE`.
SAY: Once connected, get all still shows only the kubernetes Service, because the app sits in its own namespace. With dash n, cheese app namespace, yours lists the frontend, database, API and nginx controller Pods, and a loader Pod marked completed. Get nodes shows one node, or two.

SHOW: TRACKER [C] 6. The three README commands (README:490–492): `kubectl get pods
--namespace=cheese-app-namespace` → TERM(b45: 7) RED (the toolbox without a kubeconfig). The other two,
`kubectl get pod api-c4fb784b-2llgs --namespace=cheese-app-namespace` and `kubectl exec --stdin --tty
api-c4fb784b-2llgs --namespace=cheese-app-namespace  -- /bin/bash` (folds), are typed verbatim into a GREY
README card, without output (`k20`–`k22`, the stand-in's answers, are not printed); the Pod name
`api-c4fb784b-2llgs` is struck GREY with a YELLOW chip "← the name your first command prints".
SAY: The next README step shells into a Pod. The Pod name in the README is the author's own; use the name your first command prints.

SHOW: A small GREY recall of S08's `k51` strip (tag `stand-in: kind, not GKE`), then a GREEN card (tag
`extra · our spelling`, no output) `env | grep ROOT_PATH`, a GREY chip "yours: ROOT_PATH=/api-service"
(`setup_containers.py:310–311`), then a second GREEN line `exit` and the prompt back at
`…:/app/deploy_k8s#`. A YELLOW `▶ your turn`.
SAY: Inside, you get a shell in the API container, just as we did in the game. Print its environment and look for ROOT PATH. Pause and try it.

SHOW: TRACKER [C] 7. EXPECTED(expected/readme-pulumi-outputs: 2–9) on the left, tagged `expected ·
README:497–506`; CODE(src/deployment/deploy_k8s/__main__.py: 43–49) on the right. `ingress_name :
"nginx-ingress"` and `nginx_ingress_ip` RED (tag `erratum`); line 48 `ip_address` GREEN; a GREY chip
"setup_loadbalancer.py:65 → cheese-app-ingress"; a small inset of `c20:40` (`ip_address : [unknown]`).
SAY: To view the app, the README shows an outputs block a little older than the code. Today the address is called ip address, not nginx ingress ip, and the Ingress is called cheese app ingress.

SHOW: A schematic browser window (tag `illustration`), address bar `http://<IP>.sslip.io`: a plain page
outline with a header "Formaggio" bar and a footer line `API version: 3.0` YELLOW; a PINK arrow from the
footer to `/api-service/status`. A YELLOW `▶ your turn` beside the address bar. Then a GREY chip "chat ›
model: RAG (`/chat?model=llm-rag`)".
SAY: Pause and open your app URL. A footer that says API version three point zero proves the whole path works: it asks slash api service slash status. Then pick the RAG model in the chat; a reply proves Vertex AI and Chroma too.

SHOW: A GREY chip: "first moments: 502 / 503 → the API is still loading TensorFlow · wait, retry". Fade;
empty frame.
SAY: Right after deploying you may see 502 or 503: the API is still loading TensorFlow. Wait, and try again.

---

## S15 · Logs, then scaling at two levels — `s15_scaling.py` · `LogsAndScaling`

SHOW: TRACKER [G] 1. Toolbox terminal (tag `stand-in: kind, not GKE`). It types `k30:1` live → TERM(k30: 2)
RED. Then TRACKER [G] 1→4 steps quickly while a GREY README card `README.md · lines 620–656` lists the
other 13 commands verbatim, at once (LaggedStart FadeIn, 1.5 s). Every `cheese-app-cluster-namespace`
on the card turns RED in one sweep (Indicate), and a RED badge `✗ 14/14` stamps the card; under it, on
"most", a GREY strip TERM(k33: 2) (`No resources found …`) for the one that answers differently.
SAY: The README's debugging block has 14 kubectl commands. As typed, they all fail; most say the namespace, cheese app cluster namespace, is not found.

SHOW: Two printed strips below the card (no typing): TERM(k34: 2) (`syntax error near unexpected token`)
and TERM(k36: 2) (`pod-name: No such file or directory`), RED; on the card the `<` and `>` of `<pod-name>`
glow PINK with a label "redirection" (tag `erratum`).
SAY: Lines with pod name in angle brackets are shell redirections: replace the whole placeholder, brackets included.

SHOW: A GREEN card (tag `extra · our spelling`, no output), five lines typed one by one: `kubectl logs -n
cheese-app-namespace job/vector-db-loader`, `kubectl describe job vector-db-loader -n
cheese-app-namespace`, `kubectl get pods -n cheese-app-namespace | grep vector-db-loader`, `kubectl logs
-n cheese-app-namespace vector-db-loader-xxxxx` (a GREY chip "your pod's name"), `kubectl logs
deployment/api -n cheese-app-namespace -f`. A GREY chip: "drop `-c wait-for-chromadb`: the Job has one
container". A YELLOW `▶ your turn`.
SAY: Two fixes: the namespace is cheese app namespace, and the Job has one container, so drop the wait for chromadb flag. Pause and try them.

SHOW: TRACKER [G] 4 · extra. On the stand-in (tags `extra`, `stand-in: kind, not GKE`): line 1 of `k60`
(folds) → TERM(k60: 2–5, 8); `kubectl logs job/hello-job` → TERM(k61: 2–3); `kubectl describe job
hello-job` → TERM(k62: 18, 41–42). V4's Job cousin beside it: a GREEN Job card emits one TEAL Pod that
runs, turns `Completed` GREY and is not replaced.
SAY: On a Job that exists, an extra on the stand-in, the same commands work: done, one succeeded. Nothing replaces a finished Job's Pod.

SHOW: A GREY note (tag `erratum`): CODE(src/deployment/deploy_k8s/setup_containers.py: 150) `mount_path="/chroma/chroma"`
beside a GREY chip "today's chroma image writes to /data". Fade.
SAY: A small note: after a database restart, run the loader again; the chip shows why.

SHOW: Tracker caption `extra`. LECTURE 22 · 18. A GREY card "scale by CPU, memory, custom metrics"; under it
a GREY README heading card "Deployment with **Scaling** using Kubernetes" (tag `erratum`) and two RED
crosses "no `replicas` · no Pod autoscaler"; then CODE(src/deployment/deploy_k8s/create_cluster.py: 63–66)
with lines 64–65 GREEN.
SAY: Now scaling. The lecture promises scaling on CPU, memory or custom metrics, but the code sets no replicas and no Pod autoscaler. It switches on the node layer: one to two nodes.

SHOW: LECTURE 22 · 43. **V8 `BinPacking`** (tag `illustration`): a BLUE node rectangle as a shelf,
"allocatable: less than its 8 GB", filled with blocks sized by their requests: a fat TEAL `frontend 250m /
2Gi`, small `vector-db 100m / 128Mi`, small `nginx 100m / 128Mi`, and an `api` block with a dashed
outline and a "?" ("no request"). CODE(src/deployment/deploy_k8s/setup_containers.py: 79–82) inset, line
80 YELLOW.
SAY: The scheduler packs Pods onto nodes by their requests. The frontend asks for a quarter CPU and 2 gigabytes. Chroma and nginx ask for little, and the API for nothing, so nobody can plan for it.

SHOW: A GREEN card (tag `extra · our spelling`, no output): `kubectl scale deployment frontend --replicas=3
-n cheese-app-namespace`, with a GREY chip `Milestone 5 · show scaling`. Two fat blocks drop onto the shelf; one fits, the next hovers RED `Pending`, and
V1's scheduler lamp lights in a small inset. A second node slides in from the right (GREY chip "cluster
autoscaler · max 2") and the block lands. A small GREY recall of `k55` (tag `stand-in`): "the same command
on the game".
SAY: Scale the frontend to 3; Milestone 5 asks you to show scaling. A copy that does not fit waits, pending, until the autoscaler adds a second node. Ask for many more, and some stay pending: the pool stops at two.

SHOW: A BLUE disk `persistent-pvc` is chained to node 1 under the `api` block; a PINK chip `ReadWriteOnce ·
one node at a time` (CODE inset `src/deployment/deploy_k8s/setup_containers.py: 24`). A RED chip "thought
experiment · don't run it". A YELLOW question card.
SAY: The API's disk attaches to one node at a time. Suppose you scaled the API to 3, and some copies landed on the second node. What happens to them, and can the autoscaler fix it?
PONDER(10 s, "Suppose api had 3 replicas.\nSome Pods land on node 2.\nWhat happens to them,\nand can the autoscaler fix it?")

SHOW: A second `api` block on node 2 reaches for the disk; the RED chain snaps `Multi-Attach`; the block
stays YELLOW `ContainerCreating`. A third node outline appears GREY-dashed and is crossed out RED ("more
nodes don't help").
SAY: They stay stuck creating, with a multi attach error: the disk already sits on node 1. More nodes do not help; the limit is the disk.

SHOW: The `AsksChecklist` grows a little: "Scaling" gets a solid YELLOW tick on "nodes: automatic" and a
dashed tick on "Pods: `kubectl scale` · an HPA needs requests" (GREY dashed). A GREEN typed line (tag
`extra · our spelling`, no output): `kubectl scale deployment frontend --replicas=1 -n
cheese-app-namespace`. Fade; empty frame.
SAY: That ticks scaling, in two levels: nodes automatically, Pods in your hands; a Pod autoscaler on CPU needs requests, and the API has none. Scale back to 1 when you are done.

---

## S16 · Destroy, audit, recap — `s16_recap.py` · `Recap`

SHOW: TRACKER [C] 8. LECTURE 22 · 40. Toolbox terminal. It types `pulumi destroy --stack dev --refresh -y`
→ TERM(b50: 2) RED; then (extra, local) the same → TERM(c23: 21–22). Beside it V6 (tag `illustration`)
empties in reverse: Ingress and `nginx-f5` → the app objects → namespace → node pool → cluster → NAT →
VPC; the GOLD meter winds down.
SAY: Last, delete the cluster: pulumi destroy, stack dev, refresh, dash y. Ours has nothing real to delete; yours deletes what this stack created, in reverse order, from the Ingress down to the network.

SHOW: LECTURE 22 · 44. A GOLD audit card (tag `extra · our spelling`, no output), four lines typed:
`gcloud container clusters list`, `gcloud compute forwarding-rules list`, `gcloud compute disks list`,
`gcloud compute firewall-rules list`, with a GREY chip "look for pvc-… disks" and a GREY chip "destroy
failed with 'resource is in use'? delete these, then destroy again". Three ghost icons blink outside the empty tree: a forwarding rule, a
`pvc-…` disk, the registry images with a padlock `retain_on_delete`.
SAY: Then check what may survive, our suggestion: list clusters, forwarding rules, disks and firewall rules. Those are deleted in the background and can be left behind; look for disks named pvc.

SHOW: The padlock on the registry images glows GOLD, with a GREY chip "Artifact Registry ›
cheese-app-repository › delete images"; a GREY-dashed L20 VM icon blinks. A GOLD "Don't
forget to delete" card and a YELLOW `▶ your turn`.
SAY: Registry images stay on purpose: delete them in the console. Delete the lecture 20 machine too, if it still runs. Pause and check.

SHOW: No tracker. LECTURE 22 · 15. The `AsksChecklist` returns at full size, every item ticked, and
writes what did each job: Failover → "ReplicaSet · node auto-repair"; Load balancing → "cloud LB · nginx
Ingress · Services"; Scaling → "node autoscaler · `kubectl scale`".
SAY: Back to the three asks. Failover: the ReplicaSet brings Pods back, and node auto repair replaces broken machines. Load balancing: the cloud load balancer, nginx and the Services. Scaling: the node autoscaler, and kubectl scale in your hands.

SHOW: LECTURE 22 · 43. Five short lines appear one per phrase; for each, a tiny thumbnail of its scene's
picture (V6 for S12, V8 for S15, V4 for S07) *TransformFromCopy*s into its GREY scene chip: "self-service ·
one `pulumi up` (S12)", "lower cost · packing by requests (S15)", "automatic adjustment · node autoscaler
(S15)", "smooth running · self-healing (S07)", "simpler development · L20's images (S10)".
SAY: The lecture lists five payoffs. Self-service: one pulumi up. Lower cost: Pods packed by their requests. Automatic adjustment: the node autoscaler. Smooth running: self-healing. Simpler development: the same images as lecture 20.

SHOW: Clear. A YELLOW card "Test yourself · 1/5": "Which control-plane part decides where a new Pod runs,
and which notices that a Pod died?"; on the sentence boundary it Transforms into 2/5: "Why does `kubectl
get all` show only `service/kubernetes`, and what flag fixes it?"
SAY: Test yourself. Which control plane part decides where a new Pod runs, and which one notices that a Pod died? Why does get all show only the kubernetes Service, and what flag fixes it?

SHOW: Card 2/5 Transforms into 3/5: "How does the `web` Service know which Pods are its own, and why does
the API reach Chroma at `vector-db:8000`?", then 4/5: "Trace one click from `<IP>.sslip.io` to the API Pod.
Why does the bare IP answer 404?"
SAY: How does the web Service know its Pods, and why does the API reach Chroma at vector db? Trace one click from sslip dot io to the API Pod; why does the bare IP answer 404?

SHOW: Card 4/5 Transforms into 5/5: "Why can the frontend scale to 3 but the API cannot, and what does the
autoscaler add?" After it fades: a GREY pointer card "answers: exercises.md · study guide (MLOps_Learning)".
SAY: Why can the frontend scale to 3 but the API cannot, and what does the autoscaler add? Answers are in the exercises and the study guide.

SHOW: A GREY-dashed roadmap chip slides in: "L23 · cheese-app-v4 · the two `pulumi up` runs from GitHub
Actions, on every merge". Fade; empty frame.
SAY: Next, in lecture 23, the two Pulumi programs, in version 4 of the app, run from GitHub Actions on every merge.

---

## Word count

`python -m explainer.script videos/ac215-l22-kubernetes-cloud/script.md` (SAY words; re-run after any
edit). At ≈174 wpm: ≈24.6 min of narration, ≈31–33 min with typing, outputs, illustrations and five
ponder timers (46 s). 151 SAY blocks, none over 48 words. Every scene is inside its BRIEF band (target
±15 %).

| scene | words (BRIEF · band) | scene | words (BRIEF · band) |
| --- | --- | --- | --- |
| S01 Hook | 214 (230 · 196–265) | S09 Blueprint | 244 (250 · 213–288) |
| S02 Orchestrator | 259 (250 · 213–288) | S10 ImagesStack | 285 (280 · 238–322) |
| S03 ClusterAnatomy | 280 (300 · 255–345) | S11 ClusterPlan | 268 (270 · 230–311) |
| S04 Toolbox | 277 (260 · 221–299) | S12 PulumiUp | 286 (280 · 238–322) |
| S05 TestCluster | 271 (270 · 230–311) | S13 OneClick | 295 (290 · 247–334) |
| S06 TicTacToe | 275 (270 · 230–311) | S14 ExploreApp | 265 (290 · 247–334) |
| S07 SelfHealing | 260 (260 · 221–299) | S15 LogsAndScaling | 304 (290 · 247–334) |
| S08 StableNames | 240 (230 · 196–265) | S16 Recap | 274 (260 · 221–299) |
| **part 1** | **2,076** (2,070) | **part 2** | **2,221** (2,210) |

**Total 4,297** (series band 3,900–4,300; BRIEF ~4,280). The total sits 3 words under the ceiling:
any later addition names its cut in the same scene. Cuts already made to fit (each kept on screen as a
chip or in the SHOW): the API image size (S10), "Helm installed it" (S13, a chip), the request-path
re-wording of README:461–465 (S13 says it as one chain), the slides' "node agents" aside (S05); at the
merge: the slide-13 "three clusters" aside (S09, slide 13 stays tagged in S07), the stand-in answers of
README:491–492 (S14, typed into a README card), the Chroma path detail (S15, a chip), "every stand-in
panel carries this grey label" (S05, the tag is on screen).
