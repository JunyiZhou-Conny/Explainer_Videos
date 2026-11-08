# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** L22 creates a GKE cluster with Pulumi, and
the recording sandbox has **no GCP project, no Google account and no credentials**. Everything that
runs on a machine you own was captured live on **2026-11-07 (20:47–21:16 UTC)**: the deployment
toolbox (`sh docker-shell.sh`) failing as committed, the two one-line fixes, the toolbox built and
started; every gcloud, Pulumi and kubectl command of the README's K8s sections, typed at the
toolbox prompt. Every command that needs Google stops at its **honest first error** ("You do not
currently have an active account selected", "PULUMI_ACCESS_TOKEN must be set …", `invalid_grant:
account not found`). Then three things go further, each clearly labelled:

1. **Pulumi on its local file backend** (`pulumi login --local`, no account): the README's stack and
   config commands, `preview`, `up` and `destroy` on the unchanged `deploy_images` and `deploy_k8s`
   programs, up to their first Google call. `deploy_k8s` first stops at a Python `TypeError` because
   the image stack has no outputs; with a capture-only stand-in image stack (placeholder tags) its
   real plan appears: **`+ 23 to create`** (`laptop/c20`), and `pulumi up` stops at the first resource,
   the VPC (`laptop/c21`).
2. **A stand-in cluster** (kind, "Kubernetes in Docker", 1 control plane + 2 workers, Kubernetes
   v1.34.11) in the laptop's Docker engine. The toolbox's own kubectl talks to it, so the README's
   kubectl commands (`kubectl get all`, `get nodes`, `componentstatuses`, the tic-tac-toe warm-up's
   `kubectl apply` / `get services`, the shell-into-a-Pod commands, the debugging block) run
   **verbatim against a real API server**. It is NOT GKE: no cloud load balancer (the Service's
   `EXTERNAL-IP` stays `<pending>`), no node pool or autoscaler, no Workload Identity. Every scene
   that shows a `kind/` file carries the tag `stand-in: kind, not GKE` (or says it in one line).
3. `expected/`: the README's own `Outputs:` block (IPs replaced by placeholders). Console steps are
   `illustration`s. No output was invented.

**Breakages and surprises found on the recording day** (the video states them kindly, with the fix):

1. **The toolbox still does not build as committed** (`laptop/b02`), exactly as found for L20 on
   2026-11-05: `FROM python:3.13-slim-bullseye` (`src/deployment/Dockerfile:4`) → 22 × `404 Not Found`
   from the `bullseye-security` pool at `Dockerfile:11-12`, then `docker-shell.sh` (no `set -e`) runs
   `docker run` anyway → `Unable to find image 'cheese-app-deployment:latest' locally` / `pull access
   denied`, exit 125. With **both** L20 fixes in one edit (`b02a`: `python:3.13-slim-bookworm`;
   `google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin` at `Dockerfile:30`) it builds in
   **92.3 s** (`b03`). Fix 2 matters twice here: the gke-gcloud-auth-plugin is what GKE's kubeconfig
   calls for every `kubectl` request.
2. **The Dockerfile's kubectl 1.34 pin is not the kubectl you get** (`b10`, `b12`, `b14`, `kind/k02`).
   Google's apt repository also ships a package named `kubectl` (version `1:592.0.0-0`, epoch 1), which
   outranks the pkgs.k8s.io 1.34 package that `Dockerfile:33-41` adds; `/usr/bin/kubectl` is a link to
   gcloud's **dispatcher**. With no cluster, `kubectl version --client` says `v1.35.9-dispatcher` (the
   digest expected `v1.34.x`); against the 1.34 stand-in, `kubectl version` picks a matching client:
   `Client Version: v1.34.12-gke.300…`, `Server Version: v1.34.11`. Harmless; worth one sentence.
3. **`deploy_k8s` needs `deploy_images` to have run on the same backend** (`laptop/c13`, `c14`). With an
   image stack that has no outputs, `pulumi preview` fails before planning anything:
   `File "/app/deploy_k8s/setup_containers.py", line 70` `lambda tags: tags[0]` →
   `TypeError: 'NoneType' object is not subscriptable`. README:416 ("only required if you have NOT
   already done this") means: done once, into the same state bucket. That is the error a student sees
   who skips it or logs into a different bucket.
4. **The plan is real and matches the digest's count** (`c20`): Network, Subnetwork, Cluster, Router,
   RouterNat, NodePool, the `gke_k8s_v2` provider, `connect-k8s-command`, Namespace, the Helm release
   `nginx-f5`, two PVCs, `api-ksa`, `api-gsa-wi-user`, Deployments `frontend` / `vector-db` / `api`,
   Services `frontend-service` / `vector-db-service` / `api-service`, Job `vector-db-loader`, Ingress
   `cheese-app-ingress`, plus two reads (`StackReference organization/deploy-images/dev`,
   `nginx-ingress-service`): `+ 23 to create`. Outputs: only `cluster_name: "cheese-app-cluster"` is
   known at preview time; `app_url`, `ip_address` … are `[unknown]` until the cluster exists.
5. **The README's `Outputs:` block is older than the code** (`expected/readme-pulumi-outputs.txt` vs
   `c20`): the code exports `ip_address` (`deploy_k8s/__main__.py:48`), not `nginx_ingress_ip`, and the
   Ingress is `cheese-app-ingress` (`setup_loadbalancer.py:65`), not `nginx-ingress` (digest Step 7).
6. **The debugging block uses a namespace that does not exist** (`kind/k30-k43`): every command with
   `cheese-app-cluster-namespace` answers `namespaces "cheese-app-cluster-namespace" not found`; the
   app's namespace is `cheese-app-namespace`. The `<pod-name>` placeholders are shell redirections:
   `syntax error near unexpected token 'newline'` (k34) or `pod-name: No such file or directory`
   (k36, k38). Replace them entirely.
7. **The leftover config keys show up** (`c12`): `pulumi config` in `deploy_k8s` lists `setupSSL false`
   and `security:ssh_user sa_…` from the committed `Pulumi.dev.yaml` (unused by the program; the
   `sa_` number is the instructor's OS Login user: mask it in a frame, e.g. `sa_000000000000000000000`).
8. Confirmed as the digest predicted: plain `kubectl version` before any cluster → `The connection
   to the server localhost:8080 was refused` (b11, harmless); `kubectl get all` in `default` shows only
   `service/kubernetes` (k03); `kubectl get componentstatuses` → `Warning: v1 ComponentStatus is
   deprecated in v1.19+` and three `Healthy` rows (k06); `kubectl get pods --namespace=cheese-app-namespace`
   on a cluster without the app → `No resources found in cheese-app-namespace namespace.` (k20).

## Which commit

**Pinned: `main` @ `3ecef56fea879ac480d260c0906cd95baf05179a`** (2025-11-28 16:00:06 −0500, "v4->v3").

- On 2026-11-07 `git ls-remote` (`laptop/p03`) still gave `HEAD` = `main` = `3ecef56`; the laptop's fresh
  clone is at that commit (`laptop/p02`). Branches for comparison only: `cluster-updates` `e55178c`,
  `pipenv` `0012c9a`. The unmerged staff branch is masked as `work/‹staff›` in every capture (`d1e860d`,
  unchanged since the L20 captures of 2026-11-05) and is never named on screen.

## `source/` — the tutorial's own files

From [dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) at `3ecef56`, copied unchanged
with `git show 3ecef56:<path>` at the repo's relative paths (executable bits as committed). Course
material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's permission.
Not copied: images, `deploy_single_vm/` (L20), `emoji.yaml` / `visualizer.yaml` (demo YAMLs not in the
README), `frontend-simple/`, the vector-db books.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the K8s sections: APIs 396-402, toolbox 404-413, images 415-434, cluster 436-455, the Mermaid traffic diagram 457-474 (its dotted edge points from the vector-db Service to the loader Job; the data flows the other way), kubectl 476-486, shell into a Pod 488-493, outputs 495-507, delete 509-512; the warm-up 517-581 (`gcloud container clusters create` 541, console 544-549, apply 565, services 570, delete 580); debugging 589-657 (the K8s half 618-657). **Lines 499, 500, 505 hold the README's sample IP addresses: a panel that quotes 498-506 shows `<IP>` instead (use `expected/readme-pulumi-outputs.txt`)** |
| `src/deployment/Dockerfile` | the toolbox: `FROM python:3.13-slim-bullseye` (4, breakage 1), apt 11-12, gcloud repo 15-18, Docker repo 21-26, `google-cloud-sdk …` (29-30, breakage 2), kubectl `K8S_MINOR=1.34` (33-41, surprise 2), helm 44, pulumi 47-48, `PULUMI_CONFIG_PASSPHRASE=""` 51, uv 54-55, user `app` 58-61, `uv sync --frozen` 70, entrypoint 73 |
| `src/deployment/docker-shell.sh` | env 7-17 (`SECRETS_DIR` three levels up 9, `GCP_PROJECT` 13, region/zone 14-15, `PULUMI_BUCKET` 17), attach-if-running 23-25, build `--platform=linux/amd64` 31, `docker run` mounts 34-50 (`USE_GKE_GCLOUD_AUTH_PLUGIN=True` 45) |
| `src/deployment/docker-entrypoint.sh` | banner 3-7, `activate-service-account` 10, project 11, `configure-docker` 13, bucket 15-20, `pulumi login` 23, stacks 26-27, `/bin/bash` 30 |
| `src/deployment/deploy-k8s-tic-tac-toe.yml` | the warm-up: Deployment `web`, `replicas: 2`, `run: web` labels, image `dlops/tic-tac-toe`, port 8080 (2-22); Service `web` `type: LoadBalancer` 80 → 8080 (24-35) |
| `src/deployment/deploy_images/{Pulumi.yaml, Pulumi.dev.yaml, __main__.py}` | registry 14-15, timestamp tags 13/25, the three `docker_build.Image`s 23-71, the `-ref`/`-tags` exports 34-35, 53-54, 73-74 |
| `src/deployment/deploy_k8s/__main__.py` | the four calls 19-40, region hard-coded 15, `setupSSL = False` 17, exports 43-49 |
| `src/deployment/deploy_k8s/create_network.py` | VPC, subnet `10.0.0.0/19`, router, Cloud NAT |
| `src/deployment/deploy_k8s/create_cluster.py` | the regional cluster 20-41 (private nodes 30-34, Workload Identity 35-37), node pool 44-72 (`n2d-standard-2` 14, autoscaling 1-2 63-66, `node_locations` 71), kubeconfig 77-131, provider 134-138, namespace 141-145, KSA 151-162, IAM binding 184-189, `get-credentials` command 192-199 |
| `src/deployment/deploy_k8s/setup_containers.py` | the StackReference 10-14 (and `tags[0]` at 70, surprise 3), PVCs, the three Deployments + Services, the loader Job, the API Pod's env |
| `src/deployment/deploy_k8s/setup_loadbalancer.py`, `setup_loadbalancer_ssl.py` | Helm release `nginx-f5` 11-46, the Service read 49-59, `sslip.io` host 60, Ingress 62-117 (name 65) |
| `src/deployment/deploy_k8s/{Pulumi.yaml, Pulumi.dev.yaml, Pulumi.ssl.yaml}` | project `deploy-k8s`; the committed config with the instructor's project id and `sa_` user (surprise 7) |
| `src/deployment/{pyproject.toml, uv.lock, .python-version, .gitignore, .docker-tag, docker_config.json, README.md}` | the toolbox's Python deps (pulumi, pulumi-gcp, -kubernetes, -command, -docker-build); `.gitignore` ignores `/pulumi-*` |
| `src/api-service/{Dockerfile, docker-entrypoint.sh, pyproject.toml}`, `api/service.py`, `api/utils/{chat_utils,llm_rag_utils,llm_cnn_utils,llm_utils}.py`, `api/routers/llm_rag_chat.py` | `ROOT_PATH` mount and `/status` → `{"version": "3.0"}` (`service.py`), `CHROMADB_HOST`/`PORT`, the CNN model download, `/persistent` paths |
| `src/frontend-react/{Dockerfile, next.config.js}`, `src/components/layout/Footer.jsx`, `src/services/{DataService,Common}.js`, `src/app/chat/page.jsx` | the footer's `/api-service/status` call, the chat page's default model |
| `src/frontend-react/.env.production` (tracked as `env.production`: `.gitignore` drops `.env.*`) | **one deviation:** line 3 `NEXTAUTH_SECRET=` keeps its key but its committed value is replaced by `<value not copied: see ASSETS.md>` (credential-like, series rule); line 2 `NEXT_PUBLIC_BASE_API_URL=/api-service` unchanged |
| `src/vector-db/{Dockerfile, docker-entrypoint.sh, pyproject.toml, cli.py}` | the loader the Job runs (`--download --load`) |
| `.gitignore` | the repo root's |

**Names (series rule).** `src/vector-db/cli.py:75` and `:440` contain the instructor's name: a code panel
that quotes those lines masks it as `‹instructor›`. Captures are masked at capture time (`run_steps.sh`
`mask`, the name read at run time from the tutorial's own page, never written here); none contained it.
**Ids:** the README commands contain the instructor's project id `ac215-project`; they were run verbatim
(they are what a student types before replacing it), as in L20. `docker-shell.sh`'s `GCP_PROJECT` was set
to the placeholder `your-gcp-project` (`b01`), so the toolbox's own messages show the placeholder.

## `terminal/` — real terminal sessions

Captured **2026-11-07 20:47–21:16 UTC** by `terminal/capture.sh`, which runs `terminal/run_steps.sh` in
a fresh disposable "laptop" container, one segment at a time:

```
bash assets/terminal/capture.sh relay laptop-setup pre tb-commit tb-shell tb-wait tb-readme tb-local \
     tb-local2 kind-up kind-readme kind-readme2 kind-extra kind-extra2 kind-down tb-close laptop-teardown
docker rm -f l22-relay
```

Each README command runs exactly as printed (read from the README's own lines by `readme a b`, so it is
byte-identical), in README order, and its output goes to its own file: `$ command`, the output,
`[exit N]`. Steps whose name contains `-x-` are extras (not in the README). `istep`/`ctstep` files ran
in a real pseudo-terminal (`ptyrun.py`, 100×40): `b02`, `b03`, `kind/k22`, `k43`, `k51`. All other
toolbox commands (`cstep`) were typed into the running toolbox with `docker exec` (no terminal), which
is why the Pulumi commands print `PULUMI_ACCESS_TOKEN must be set … non-interactive` rather than the
browser-login offer a terminal shows (that one is L20's `laptop/b14`).

| folder | environment | README section |
| --- | --- | --- |
| `laptop/` | a fresh, empty Docker engine standing in for a laptop with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2), Alpine, user `student` in the `docker` group, git 2.54.0, curl, python3, openssl; home = the README's parent folder (`cheese-app-v3/`, `secrets/`). The toolbox (`cheese-app-deployment`, 2.61 GB) runs in this engine with its socket mounted, as on a laptop | "Start Deployment Docker Container" (404-413), images (415-434), cluster (436-455), kubectl without a cluster (476-492), delete (509-512), the warm-up's gcloud create/delete (541, 580) |
| `kind/` | **stand-in, not GKE**: kind v0.31.0 in the same laptop engine, cluster `test-cluster` (kindest/node:v1.34.11; `test-cluster-control-plane`, `-worker`, `-worker2`); the toolbox joins kind's Docker network and gets kind's kubeconfig (capture-only), so its kubectl runs the README's commands | warm-up 551-575; main 476-493; debugging 618-657; extras |
| `expected/` | — | the README's `Outputs:` block (below) |

Versions at the time of recording (from `b03`, `b10`, `b14`, `c03`, `k01`, `k02`): Google Cloud SDK
**592.0.0** (core 2026.10.30, gsutil 5.38, bundled Python 3.14.9, gke-gcloud-auth-plugin package
592.0.0, which prints `Kubernetes v37.0.0-22-gb501ae55e`); kubectl = gcloud's dispatcher
(`v1.35.9-dispatcher`, or `v1.34.12-gke.300…` against a 1.34 server); Helm **v3.22.1**; Pulumi
**v3.274.1**; uv 0.13.7; Python 3.13.18 (toolbox); Pulumi plugins kubernetes 4.23.0, docker 4.9.0,
gcp 9.3.0, docker-build 0.0.15, command 1.1.3; kind v0.31.0 / Kubernetes v1.34.11.

### `laptop/` — the toolbox, gcloud and Pulumi

| file | README step | what it shows |
| --- | --- | --- |
| `p00-x-env.txt` | extra | 2026-11-07, Docker 29.8.2, git 2.54.0, kind v0.31.0, no images |
| `p01-clone.txt`, `p02-x-git-log.txt`, `p03-x-ls-remote.txt` | extra (the README has no clone command) | `Cloning into 'cheese-app-v3'...`; `3ecef56… 2025-11-28 16:00:06 -0500 v4->v3`; the branches, `work/‹staff›` masked |
| `p04-mkdir-secrets.txt`, `p05-x-tree.txt` | README:236-259 (L20's service accounts; `deployment.json` goes in `secrets/` next to the repo) | `secrets/deployment.json` (a placeholder, capture-only below); `src/deployment/` and `deploy_k8s/` listings |
| `b01-x-set-project.txt` | extra (L20's README:266-267, digest Step 3: set `GCP_PROJECT` before the first run) | `13:export GCP_PROJECT="your-gcp-project" # Change to your GCP Project` |
| **`b02-docker-shell.txt`** | **README:405-406 `cd deployment` + `sh docker-shell.sh`, as committed**, in a terminal | `Container 'cheese-app-deployment' is not running. Building …`, `ERROR [ 2/16] RUN apt-get update && apt-get install -y curl …`, 22 × `E: Failed to fetch https://deb.debian.org/debian-security/pool/updates/main/… 404 Not Found`, `ERROR: failed to build`, `Unable to find image 'cheese-app-deployment:latest' locally`, `pull access denied`, exit 125 (breakage 1). The URLs read `https://` and end in `[IP: 172.17.0.1 38722]` only because of the recording proxy (capture-only): a student sees `http://` and their mirror's IP; crop that column |
| `b02a-x-fix-dockerfile.txt` | extra: both fixes | the `git diff` of `Dockerfile`: `-FROM python:3.13-slim-bullseye` / `+FROM python:3.13-slim-bookworm`; `-google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin` / `+google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin` |
| **`b03-docker-shell-fixed.txt`** | README:406 again, in a terminal; the shell stayed open for everything below | `[+] Building 92.3s (21/21) FINISHED` (step `[ 8/16]` the gcloud packages 41.4 s, `[ 9/16]` kubectl 14.0 s), then the entrypoint: `Container is running!!!`, `Architecture: x86_64`, `Python 3.13.18`, `uv 0.13.7`; **`ERROR: (gcloud.auth.activate-service-account) … deployment@your-gcp-project… ('invalid_grant: Invalid grant: account not found'`**; `Updated property [core/project].`; the credHelpers warning + `Adding credentials for: us-docker.pkg.dev`; `Bucket does not exist. Creating...` → no credentials; `Logging into Pulumi using GCS bucket: gs://your-gcp-project-pulumi-state-bucket` → `error: could not log in to the state backend`; `BucketNotFoundException: 404`, `No stacks found.`; the prompt `root@<id>:/app#`, `exit` (typed by tb-close) |
| `b10-gcloud-version.txt` | README:408 | `Google Cloud SDK 592.0.0` … `gke-gcloud-auth-plugin 0.5.21`, `kubectl 1.35.9` |
| `b11-kubectl-version.txt` | README:409 | `Client Version: v1.35.9-dispatcher`, `Kustomize Version: v5.7.1`, **`The connection to the server localhost:8080 was refused - did you specify the right host or port?`**, exit 1 (no cluster yet; harmless) |
| `b12-kubectl-version-client.txt` | README:410 | `Client Version: v1.35.9-dispatcher` (surprise 2) |
| `b13-gcloud-auth-list.txt` | README:413 | **`No credentialed accounts.`**; with a real key the README expects `deployment@<project>.iam.gserviceaccount.com` active |
| `b14-x-tools.txt` | extra (surprise 2) | `/usr/bin/kubectl -> ../lib/google-cloud-sdk/bin/kubectl`, `kubectl 1:592.0.0-0` from Google's repo, `google-cloud-cli 592.0.0-0`, Helm v3.22.1, Pulumi v3.274.1, uv, Python, the env (`GCP_PROJECT=your-gcp-project`, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json`, `PULUMI_BUCKET=gs://your-gcp-project-pulumi-state-bucket`, `USE_GKE_GCLOUD_AUTH_PLUGIN=True`, `PULUMI_CONFIG_PASSPHRASE=` empty), `/secrets`, `/app` |
| `b15-gke-create-test-cluster.txt` | README:541 (warm-up "Create Cluster") | `ERROR: (gcloud.container.clusters.create) You do not currently have an active account selected.` |
| `b20`-`b23` (`images-stack-init`, `-config-set`, `-preview`, `-up`) | README:420, 421, 428, 433, verbatim (`cd deploy_images`) | each `error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions`, exit 3: the GCS backend login failed in `b03`, so Pulumi has no backend |
| `b30`, `b31-…-1..3`, `b32`, `b33` | README:440, 441-443, 449, 454, verbatim (`cd deploy_k8s`) | the same `PULUMI_ACCESS_TOKEN` error, exit 3 |
| `b40`-`b44-kubectl-noconfig-*.txt` | README:478-480, 484-485, before any cluster | 5 × `memcache.go … dial tcp 127.0.0.1:8080: connect: connection refused`, then `The connection to the server localhost:8080 was refused`, exit 1: no kubeconfig yet (Pulumi's `connect-k8s-command` writes it) |
| `b45-kubectl-get-pods-ns-noconfig.txt` | README:490, before any cluster | the same |
| `b50-k8s-destroy.txt` | README:511 | the `PULUMI_ACCESS_TOKEN` error |
| `b51-gke-delete-test-cluster.txt` | README:580 | `ERROR: (gcloud.container.clusters.delete) You do not currently have an active account selected.` |
| `b52-x-get-credentials.txt` | extra (what `create_cluster.py:192-199` runs; digest Step 8's re-connect) | the same "no active account" error |
| `c00-x-login-local.txt` | extra: Pulumi's file backend, no account | `Logged in to <id> as root (file://~)` |
| `c01`, `c02` | README:420, 421 verbatim, local backend | `Created stack 'dev'`; config set silent |
| `c03-x-images-preview.txt` | README:428, local backend | the five provider plugins downloaded, `+ docker-build:index:Image build-cheese-app-{vector-db-cli,frontend-react,api-service} create`, three × `warning: Skipping preview build because some inputs are unknown.` (preview builds nothing), `Outputs:` with three `…-tags` `us-docker.pkg.dev/ac215-project/cheese-app-repository/cheese-app-…:20261107205032` (a new timestamp every run) and three `-ref` `[unknown]`, `+ 4 to create`. `pulumi up` was **not** run here: it builds the three images (the API image ~5 GB) and pushes them; L20's `laptop/b35b` captured that build up to the push's `403 Forbidden` |
| `c10`, `c11-…-1..3` | README:440-443 verbatim, local backend | `Created stack 'dev'`; the three config sets silent (README:441 has no `--stack`; it works because `stack init` selected `dev`) |
| `c12-x-k8s-config.txt` | extra | `gcp:project ac215-project`, both `security:…_email`s, and the leftovers `setupSSL false`, `security:ssh_user sa_…` (surprise 7: mask the number) |
| **`c13-x-k8s-preview.txt`** | README:449, local backend | `read pulumi:pulumi:StackReference organization/deploy-images/dev`, `+ gcp:compute:Network cheese-app-vpc create`, then **`setup_containers.py", line 70` `lambda tags: tags[0]` `TypeError: 'NoneType' object is not subscriptable`**, `+ 2 to create`, `1 errored`, exit 1 (surprise 3) |
| `c14-x-k8s-up.txt` | README:454, local backend | the same TypeError in the preview phase; nothing created |
| `c15-x-k8s-destroy.txt`, `c16-x-stacks.txt` | README:511, local backend; extra | an empty destroy (`Duration: 1s`, "…history and configuration … are still maintained … `pulumi stack rm dev`"); `organization/deploy-images/dev`, `organization/deploy-k8s/dev` (the name `setup_containers.py:10` looks up), `~/.pulumi/stacks/<project>/dev.json`, the plugins cached in `src/deployment/pulumi-plugins/` |
| **`c20-x-k8s-preview-with-tags.txt`** | README:449, local backend, after the capture-only stand-in image stack (below) | the real plan of the unchanged program: 21 creates + 2 reads, **`+ 23 to create`** (surprise 4); `Outputs:` `cluster_name: "cheese-app-cluster"`, the rest `[unknown]` |
| **`c21-x-k8s-up-with-tags.txt`** | README:454, same | the preview again, then `Updating (dev)`: **`gcp:compute:Network cheese-app-vpc creating failed`** `Error creating Network: Post "https://compute.googleapis.com/compute/beta/projects/ac215-project/global/networks?alt=json": oauth2: cannot fetch token: 400 Bad Request` `{"error":"invalid_grant","error_description":"Invalid grant: account not found"}`, then Pulumi's Python shutdown tracebacks (crop them), `+ 1 created` (the stack), `2 errored`, exit 1: the VPC is the first thing that needs Google |
| `c22-x-k8s-after-up.txt`, `c23-x-k8s-destroy.txt` | extra; README:511 | the stack holds 4 entries (stack, StackReference, two default providers), no outputs; destroy `- 1 deleted` |

### `kind/` — the README's kubectl commands on the stand-in cluster

| file | README step | what it shows |
| --- | --- | --- |
| `k00-x-kind-env.txt` | extra | 2026-11-07 20:51 UTC, kind v0.31.0, Docker engine 29.8.2 |
| `k01-x-kind-create.txt` | extra: **stand-in** for README:541 `gcloud container clusters create test-cluster --num-nodes 2 …` | the config (1 control plane + 2 workers; the `containerdConfigPatches` block is capture-only, labelled in the file, see below), `Creating cluster "test-cluster" ...` with kind's ✓ lines (node image, nodes, control plane, CNI, StorageClass, joining workers), `Set kubectl context to "kind-test-cluster"`. Crop the patch block in a frame |
| `k02-kubectl-version.txt` | README:409/532 | `Client Version: v1.34.12-gke.300.1+a8b9abb5a77ce6`, `Kustomize Version: v5.7.1`, `Server Version: v1.34.11` (surprise 2: gcloud's dispatcher matched the server) |
| `k03-kubectl-553.txt` | README:553 = 478 `kubectl get all` | only `service/kubernetes ClusterIP 10.96.0.1 … 443/TCP`: you are in `default` |
| `k04-kubectl-554.txt`, `k05-kubectl-555.txt` | README:554-555 = 479-480 | `kube-system` Pods: coredns ×2, etcd, kindnet ×3, kube-apiserver, kube-controller-manager, kube-proxy ×3, kube-scheduler; `local-path-storage`; (k04 also Services, DaemonSets, Deployments, ReplicaSets). On GKE the control-plane Pods are hidden (Google runs them) and you see `gke-*`/`kube-system` agents instead: say so |
| `k06-kubectl-559.txt` | README:559 = 484 | `Warning: v1 ComponentStatus is deprecated in v1.19+`, `controller-manager Healthy ok`, `scheduler Healthy ok`, `etcd-0 Healthy ok` |
| `k07-kubectl-560.txt` | README:560 = 485 | three nodes `Ready`, `v1.34.11` (control-plane + 2 workers; GKE's warm-up has 2 workers and a hidden control plane) |
| `k10-kubectl-apply-tic-tac-toe.txt` | README:565 (in `/app`) | `deployment.apps/web created`, `service/web created` |
| `k11-kubectl-get-services.txt` | README:570, right away | `web LoadBalancer 10.96.52.79 <pending> 80:31366/TCP 0s` |
| `k12-x-rollout.txt` | extra | `rollout status`: 0 → 1 → 2 of 2 available; the two Pods on **different workers** (`test-cluster-worker2`, `test-cluster-worker`) |
| `k13-kubectl-get-services-later.txt` | README:570, 43 s later | still `<pending>`: kind has no cloud load balancer. On GKE an external IP appears after 1-2 min; that view is an `illustration` with `<EXTERNAL-IP>` |
| `k20-kubectl-get-pods-ns.txt` | README:490 | `No resources found in cheese-app-namespace namespace.` (no cheese app on the stand-in) |
| `k21-kubectl-get-pod-api.txt`, `k22-kubectl-exec-api.txt` | README:491, 492 (k22 in a terminal) | `Error from server (NotFound): namespaces "cheese-app-namespace" not found`: the README's Pod name `api-c4fb784b-2llgs` is an example; use yours from README:490 |
| `k30`-`k43-debug-*.txt` | README:620, 623, 626, 631, 634, 635, 638, 639, 642, 643, 646, 649, 653, 656 (k43 in a terminal), verbatim | surprise 6: `namespaces "cheese-app-cluster-namespace" not found` (13 ×), `No resources found in cheese-app-cluster-namespace namespace.` (631), the `<pod-name>` redirection errors (634, 638, 642) |
| `k50-x-get-deploy-rs-pods.txt` | extra (digest §3.2-3.3) | Deployment `web` → ReplicaSet `web-5cd9789488` (`pod-template-hash`) → two Pods; Service `web` with `SELECTOR run=web`; `endpoints/web 10.244.1.2:8080,10.244.2.2:8080`; `--show-labels` |
| `k51-x-exec-web.txt` | extra (README:492's mechanism on a Pod that exists) | `kubectl exec --stdin --tty deployment/web -- /bin/sh`, typed `hostname; ls; exit` → `web-5cd9789488-5h48s`, `Dockerfile docker-shell.sh index.html script.js style.css` |
| `k52-x-dns.txt` | extra (digest §3.3: a Service is a name) | a busybox Pod: `Name: web.default.svc.cluster.local`, `Address: 10.96.52.79` (= the Service's CLUSTER-IP in k11), `wget http://web` → `<title>CodePen - Tic Tac Toe</title>` |
| `k53-x-delete-pod.txt`, `k54-x-pods-after-delete.txt` | extra (digest §0.4 "Try", §3.2) | `pod "web-5cd9789488-5h48s" deleted`; at once a new `web-5cd9789488-lmk52 0/1 ContainerCreating 1s`; 15 s later `1/1 Running` |
| `k55-x-scale.txt`, `k56-x-scale-back.txt` | extra (digest Step 12, Milestone 5) | `kubectl scale deployment web --replicas=4` → 4 Pods spread over both workers, `endpoints web … + 1 more...`; back to 2 |
| `k57-x-port-forward.txt` | extra: the stand-in's way to "View the App" (README:573-575) | `kubectl port-forward service/web 8080:80` → `HTTP/1.1 200 OK`, `<!DOCTYPE html>`, `Forwarding from 127.0.0.1:8080 -> 8080` |
| `k60`-`k62-x-job-*.txt` | extra: the run-to-completion Job pattern of the `vector-db-loader` (`setup_containers.py:199-243`) and README:626/646's commands on a Job that exists | `job.batch/hello-job created`, `condition met`, `Complete 1/1`, Pod `Completed`; `kubectl logs job/hello-job` → `loading...` `done`; `kubectl describe job` (Pods Statuses `1 Succeeded`, Events `SuccessfulCreate`, `Completed`) |
| `k63-x-namespaces.txt` | extra | the namespaces; create `cheese-app-namespace`, `No resources found …`, delete |
| `k64-x-events.txt` | extra (digest Step 11) | `kubectl get events --sort-by=.lastTimestamp`: Scheduled → Pulled → Created → Started; ReplicaSet `SuccessfulCreate` after the delete in k53 |
| `k65-x-kubeconfig.txt` | extra (digest §3.7 contrast) | context `kind-test-cluster`, `server: https://test-cluster-control-plane:6443`, a `client-certificate-data` user (redacted). GKE's kubeconfig (`create_cluster.py:104-116`) has an `exec:` user that runs `gke-gcloud-auth-plugin` instead |
| `k80-x-kubectl-delete.txt`, `k81-x-kind-delete.txt` | extra (digest Part 0.5 tip; cleanup) | `deployment.apps "web" deleted`, `service "web" deleted` (on GKE this is what removes the cloud LB before the cluster goes); `Deleting cluster "test-cluster" ...`; the laptop's images (toolbox 2.61 GB, kindest/node 903 MB) |

Recording order note: `k55`-`k63` ran before the final `k52`-`k54` and `k64` (see "Re-runs"), so the Pod
ages differ between files.

### `expected/`

| file | source | used for |
| --- | --- | --- |
| `readme-pulumi-outputs.txt` | README.md:497-506 at `3ecef56` (the README's own "results of Pulumi" block, README:495-507), unchanged except its sample IP addresses replaced by `<IP>` / `<control-plane IP>` | the `expected` panel at "View the App", next to the current export names from `deploy_k8s/__main__.py:43-49` (surprise 5) |

### capture-only (not part of the tutorial)

- **The recording proxy.** The sandbox reaches the internet only through a TLS-intercepting HTTPS proxy on
  the host's loopback. `proxy_relay.py` (container `l22-relay`, port 38722) forwards it onto Docker's
  bridge; the laptop trusts its CA; Docker client `proxies` pass it to builds and containers.
  `laptop/capture-only/python_3.13-slim-{bullseye,bookworm}.Dockerfile` (+ `-build.txt`): the two base
  images re-tagged under the same names with the proxy CA, https Debian sources and the relay as proxy,
  so the tutorial's Dockerfile builds unchanged (and so the toolbox inherits that proxy setting).
  Docker Hub's anonymous pull limit answered `429 Too Many Requests` on the recording day, so base
  images came from `mirror.gcr.io` (same images) under their Docker Hub names.
- **The key.** `secrets/deployment.json` is a well-formed service-account file around a throwaway RSA key
  generated at capture time for **no account** (`client_email deployment@your-gcp-project…`;
  `laptop/capture-only/placeholder-deployment.json`, private key elided; the key was never written to the
  repository). It makes gcloud and Pulumi's providers fail where a student's would succeed.
- **The stand-in image stack** (`laptop/capture-only/standin-images-Pulumi.yaml`, `standin-images-up.txt`):
  a three-line Pulumi YAML program under the project name `deploy-images`, stack `dev`, that only exports
  the three `cheese-app-…-tags` with **placeholder** tags (`…/cheese-app-api-service:placeholder` etc.);
  nothing is built or pushed. It exists only so `c20`/`c21` can show `deploy_k8s`'s plan; a scene that
  uses `c20`/`c21` says the image tags are placeholders.
- **The kind wiring** (`kind/capture-only/wiring.txt`): each node's containerd got the proxy CA and
  `mirror.gcr.io` as a Docker Hub mirror (`/etc/containerd/certs.d/docker.io/hosts.toml`), then a restart;
  the toolbox joined kind's network (`endpoint … already exists` in that file: the network was joined by
  an earlier attempt) and got `kind get kubeconfig --internal` at `/root/.kube/config`. The toolbox
  commands of the `kind*` segments ran with `NO_PROXY` including `test-cluster-control-plane` (the
  inherited capture proxy would otherwise swallow the API calls). The `containerdConfigPatches` in
  `k01`'s config: the sandbox kernel refuses a negative `oom_score_adj` (runc's default for the pause
  container; even the host refuses `echo -998 > /proc/self/oom_score_adj`), and the nested cgroup v1 has
  no systemd slices, so containerd clamps OOM scores (`restrict_oom_score_adj`) and uses the cgroupfs
  driver. Without them kind stopped at `kubeadm init` (`wait-control-plane`, `connection refused`); a
  laptop with Docker Desktop needs neither.
- **Re-runs on the day.** `kind-up` ran twice (the first `kind create` failed as just described; its
  `k00`/`k01` were overwritten). `kind-readme` ran twice: its first pass lacked the `NO_PROXY` setting and
  timed out in `kubectl`; its leftover process, stopped by PID, overwrote `k06`/`k07`, so `kind-readme2`
  re-ran those two. In `kind-extra`, `k52`'s first form (`kubectl run --rm -i`, no terminal) printed
  nothing and `k53`'s Pod lookup missed `NO_PROXY`; `kind-extra2` re-ran `k52`-`k54` and `k64`. The scripts
  in this folder carry the fixed versions. Docker images, the dind volume and the kind cluster were
  removed after the capture.
- `ptyrun.py` and `proxy_relay.py` are L20's, unchanged.

## What cannot run here, and how the video shows it

| README step | why not | how the video shows it |
| --- | --- | --- |
| Enable the APIs (README:396-402, warm-up 519-525) | console | `illustration`: the five API names (+ Vertex AI, digest §2); "Google Container Registry API" (523) is obsolete: say Artifact Registry |
| Service accounts, roles, key (README:236-259), the missing `iam.serviceAccounts.setIamPolicy` role (digest §2), the Artifact Registry repository (digest §2) | IAM / console, no account | `illustration`s with the README's role lists and the digest's suggested fix; `laptop/p05` shows where the key goes |
| `gcloud auth list` showing the account (413) | no account | `b13` (`No credentialed accounts.`) + one line on what a student sees instead |
| `gcloud container clusters create test-cluster …` (541) and `… delete` (580) | no account, billing | `b15`/`b51` honest errors, then the kind stand-in (`k01`, labelled) for everything kubectl does after it. Nothing records GKE's create output in the repo; the scene does not show a fake table |
| "Checkout the cluster in GCP" console clicks (544-549) | console | `illustration` (schematic, never a screenshot): Clusters → `test-cluster` → Nodes → Pods; Compute Engine VMs |
| `http://<YOUR EXTERNAL IP>` (573-575) | no cloud LB | `k13` (`<pending>`, stand-in) + `k57` (port-forward to the same Service, extra) + an `illustration` of the game in a browser |
| `pulumi stack init` / `config set` / `preview` / `up` / `destroy` on the GCS backend (420-433, 440-454, 511) | `pulumi login gs://…` needs the deployment key (`b03`) | `b20`-`b33`, `b50` honest errors; the same commands on the local backend (`c00`-`c23`, tagged `extra`) up to the TypeError (`c13`) and, with the labelled stand-in stack, the real 23-resource plan (`c20`) and the first Google call (`c21`) |
| `pulumi up` in `deploy_images` (433) building and pushing three images | ~5 GB API image (disk), push needs an account | `b23` honest error, `c03`'s preview; L20's `laptop/b35b` is the real in-Pulumi build up to the push's 403 |
| `pulumi up` in `deploy_k8s` creating the cluster and the app (454), 15-25 min | no account, billing | `c20`'s plan as the resource tree, an `illustration` of the dependency order (digest Step 7), GOLD cost tags; never a fake progress log |
| The `Outputs:` block (495-507) | needs the real run | `expected/readme-pulumi-outputs.txt` (tagged `expected`), with the current export names from `__main__.py:43-49` (surprise 5) |
| kubectl against the real cluster (478-492): the cheese-app Pods, the Ingress, PVCs | no GKE cluster | the README's commands on the kind stand-in (`k03`-`k22`, labelled), plus the stand-in extras for the mechanisms (`k50`-`k65`). Cheese-app-specific listings (Pods `api-…`, `vector-db-loader` `Completed`, PVCs `Bound`, the Ingress host) are not recorded anywhere: the scene names what to look for, without an output panel |
| Debugging block on the real loader Job (618-657) | no cheese app | `k30`-`k43` verbatim (the namespace erratum is real on any cluster) + `k60`-`k62` on a Job that exists; the corrected commands (digest Step 11) shown typed, without output |
| The app in the browser, the footer's `API version: 3.0`, a RAG chat reply (digest Step 10) | no deployment, no Vertex AI | `illustration` (no screenshot), citing `Footer.jsx` / `service.py` |
| `pulumi destroy` against real resources (511) and the leftover audit (digest §2) | nothing was created | `c15`/`c23` on the local backend + an `illustration` of the reverse-order teardown and the leftover checklist; GOLD cost tags from the digest's table |
| `sudo docker …` commands of "Debugging Containers" (593-614) | they are L20's VM commands | not repeated here: L20's `vm/52-57` captured them |
