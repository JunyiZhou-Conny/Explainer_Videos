# Exercise checks · ac215-l22-kubernetes-cloud (2026-11-07, 22:24–23:15 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/`, which
the answers cite directly (`laptop/<id>`, `kind/<id>`; provenance in [`ASSETS.md`](../../ASSETS.md)). Logs and the
check scripts are in [`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with
`[exit N]`, as in `assets/terminal/run_steps.sh`; where a step pipes into `grep`, `tail`, `head` or `sort`,
`[exit N]` is the last command's status. In the logs, `<logs>` is this `logs/` folder and `<scratch>` a scratch
folder outside the repository (the kind and Helm binaries), deleted afterwards.

There was **no Google account, no GCP project and no credentials**, as in the captures. Nothing here created a
cloud resource or called a Google API except one anonymous image pull that was refused (C7). No tutorial code
ran on the host: the only repository files used are `src/deployment/deploy-k8s-tic-tac-toe.yml` (copied
unchanged from `assets/source/`, at `3ecef56`, into the stand-in's control-plane node) and the routing lines of
`src/api-service/api/service.py` (copied into [`rootpath_app.py`](logs/rootpath_app.py), run in a disposable
container). Everything else is a small manifest written for these checks, in
[`logs/manifests/`](logs/manifests/), each with a header that says what it stands in for. No log contains a
person's name, a key, a real project ID or a public IP address; the addresses in the logs are the stand-in's
private ones (`10.96.…`, `10.244.…`, `172.18.…`), and the project is the placeholder `your-gcp-project`.

## Setup (disposable)

- Docker Engine 29.8.2 on the session machine, started for these checks (no images or containers at the
  start), and the recording's proxy relay (`assets/terminal/proxy_relay.py`) so the stand-in's nodes could
  download. Both were stopped afterwards.
- [`kind-setup.sh`](logs/kind-setup.sh) ([`kind-setup.log`](logs/kind-setup.log)): the **stand-in cluster**
  `l22ex`, kind v0.31.0 with `kindest/node:v1.34.11` (the version of the video's `kind/` captures; Kubernetes
  v1.34.11, containerd 2.3.4), one control plane and two workers, with the same capture-only wiring as the
  video's `kind-up` segment (the proxy's CA in each node, `mirror.gcr.io` for Docker Hub images, the two
  containerd patches the sandbox kernel needs; see the script's header and ASSETS.md "capture-only"). It is
  **not GKE**: no cloud load balancer (a `LoadBalancer` Service stays `<pending>`), no node pool, no cluster
  autoscaler, no Workload Identity, and its disks are local to one node. Every kind node reports the session
  machine's 4 CPUs and 16 GB.
- kubectl: the node image's own kubectl v1.34.11, run inside the control-plane node container with the cluster's
  admin kubeconfig ([`lib.sh`](logs/lib.sh), `kstep`); the manifests are copied to `/work` there. The toolbox
  (the video's `cheese-app-deployment`) was not used: its kubectl is gcloud's dispatcher, which picks a v1.34
  client against this server anyway (`kind/k02`).
- Helm v3.22.1 (the toolbox's version, `laptop/b14`), copied into the control-plane node for B8.
- [`fastapi.sh`](logs/fastapi.sh): FastAPI 0.120.4 and Starlette 0.49.3, as pinned in `src/api-service/uv.lock` at
  `3ecef56`, in `python:3.13-slim-bookworm`; network only for pip; the app is called through Starlette's
  `TestClient` (no server).

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| setup | [`k8s.sh`](logs/k8s.sh) `setup`: `kubectl apply -f deploy-k8s-tic-tac-toe.yml` ([`k8s.log`](logs/k8s.log)) | two `web` Pods on the two workers; ReplicaSet `web-5cd9789488` (the same hash as the video's capture); `web LoadBalancer … <pending> 80:32440/TCP` |
| Q1 | `q1`: delete one web Pod, then the events | `Killing` (kubelet), `SuccessfulCreate` (replicaset-controller), `Scheduled … to l22ex-worker` (default-scheduler), `Pulled`/`Created`/`Started` (kubelet) |
| B1, Q3 | `b1`: `kubectl label pod <pod> run=debug --overwrite` | 3 Pods; the endpoint slice drops the relabelled Pod's address and gains the new one's; `ownerReferences:` empty |
| B2 | `b2`: `kubectl set env deployment/web COLOR=blue`, then `kubectl rollout undo` | new ReplicaSet `web-77d995cd45` 2/2, old `web-5cd9789488` 0; after the undo the reverse |
| B3 | `b3`: [`crasher.yaml`](logs/manifests/crasher.yaml) at 5 s, 15 s, 45 s; logs; describe; delete the Pod | same Pod name, `Running 0` → `Running 1 (4s ago)` → `Error 2 (25s ago)`; `Exit Code: 1`, `Restart Count: 2`, `Back-off restarting failed container`; after the delete a new name, `RESTARTS 0` |
| B4 | `b4`: `curl` of the NodePort on each node's address, from the control-plane node | `200` from all three nodes, including the control plane (no web Pod) |
| B5, Q3 | `b5`: Service `vector-db` in `cheese-app-namespace`; `nslookup` from busybox Pods in `default` and in `cheese-app-namespace` | from `default`: `vector-db` and `vector-db.cheese-app-namespace` `NXDOMAIN`, the full `.svc.cluster.local` name resolves; from `cheese-app-namespace`: `vector-db` resolves; the two `search` lines |
| B6, C6 | `b6`: [`fat.yaml`](logs/manifests/fat.yaml) (3-CPU request), 1 then 3 replicas; `describe node`, `describe pod` | `Allocatable: cpu: 4`, `100m` requested; two `Running` (one per worker), one `Pending`: `0/3 nodes are available: 1 node(s) had untolerated taint(s), 2 Insufficient cpu. …` |
| B7 | `b7`: metrics-server v0.8.0 (with `--kubelet-insecure-tls`, kind only), `kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=4`, then `kubectl set resources … --requests=cpu=50m` ([`hpa-first-cluster.log`](logs/hpa-first-cluster.log)) | without a request: `cpu: <unknown>/50%`, `missing request for cpu in container web of Pod …`; with `50m`: `cpu: 0%/50%`. See "Re-runs" for the run in `k8s.log` |
| C1 | `c1`: [`loader-job.yaml`](logs/manifests/loader-job.yaml) (the loader Job's shape: one container `vector-db-loader`), then README:620 and two corrections | `namespaces "cheese-app-cluster-namespace" not found` (as `kind/k30`); `error: container wait-for-chromadb is not valid for pod vector-db-loader-p6k5z`; without `-c`: the Job's output |
| C4 | `c4`: [`entry.Dockerfile`](logs/manifests/entry.Dockerfile) (an ENTRYPOINT script, as `src/vector-db/Dockerfile:51`), imported into the workers; [`loader-args.yaml`](logs/manifests/loader-args.yaml) and [`loader-command.yaml`](logs/manifests/loader-command.yaml) | `args`: `Complete`, `entrypoint received: cli.py --download --load --chunk_type recursive-split`; `command`: `StartError`, `exec: "cli.py": executable file not found in $PATH`, `Exit Code: 128`, Job `Failed` |
| C5 | `c5`: [`failing-job.yaml`](logs/manifests/failing-job.yaml) (`backoffLimit: 3`, `restartPolicy: Never`) | 4 Pods in `Error` (73 s, 63 s, 43 s, 3 s old), `0 Succeeded / 4 Failed`, `BackoffLimitExceeded` |
| C7 | `c7`: [`placeholder-image.yaml`](logs/manifests/placeholder-image.yaml) (a never-pushed tag in the placeholder project) | `ErrImagePull` / `ImagePullBackOff`; `failed to authorize: failed to fetch anonymous token: … 403 Forbidden` |
| B8, Q4 | [`ingress.sh`](logs/ingress.sh) ([`ingress.log`](logs/ingress.log)): F5's chart `nginx-ingress` 2.3.1 from `https://helm.nginx.com/stable` (controller 5.2.1) with the values of `setup_loadbalancer.py:19-44` ([`nginx-f5-values.yaml`](logs/manifests/nginx-f5-values.yaml): NodePort instead of LoadBalancer, IPv6 off), the Ingress of `setup_loadbalancer.py:62-117` as YAML ([`cheese-app-ingress.yaml`](logs/manifests/cheese-app-ingress.yaml)), two `traefik/whoami` stand-ins as `frontend:3000` and `api:9000` ([`ingress-backends.yaml`](logs/manifests/ingress-backends.yaml)); `curl` with the `Host` header | controller Service `nginx-f5-nginx-ingress-controller`; Host `<node IP>.sslip.io`: `/`, `/status` → frontend; `/api-service/status`, `/api-service`, `/api-service/` → api, path unchanged; **`/api-servicex/status` → api**; Host `<node IP>`: `404 Not Found` for `/` and `/api-service/status`; generated config: `server_name <IP>.sslip.io;`, `location /api-service {`, `location / {` |
| Q4, B8 | [`fastapi.sh`](logs/fastapi.sh) ([`fastapi.log`](logs/fastapi.log)) | `ROOT_PATH='/api-service'`: `/api-service/status -> 200 {"version":"3.0"}`, `/api-service/ -> 200`, `/api-service -> 307`, `/api-servicex/status -> 404`, `/status -> 404`; `ROOT_PATH=''`: only `/status -> 200` |

## Re-runs (as recorded)

- The cluster was created once at 22:24 UTC for trial runs of the scripts, deleted, and created again at 22:51
  for the full run: `kind-setup.log` (up) → `k8s.log` (all sections in order) → `ingress.log` → `fastapi.log` →
  `kind-setup.log` (down). On the first cluster, `b3` used `kubectl logs --previous`, which answered `unable to
  retrieve container logs`; the script now prints the current container's log and `describe`.
- `kind-setup.log`'s last step (`kubectl get nodes`) failed with `chdir to cwd ("/work") … no such file or
  directory`: the folder is created by `k8s.sh setup`, whose first step lists the nodes. The script now creates it
  first.
- **B7 in `k8s.log`**: on the fresh cluster, metrics-server's API stayed `False (FailedDiscoveryCheck)` (`bad
  status … 403` from its discovery check) for the whole section, and a second run on the same cluster gave the
  same; so the HPA there shows `<unknown>` for lack of metrics, not for lack of requests. On the first cluster,
  after one failed run and a by-hand re-apply, the metrics API became available and the same `b7` section gave the
  result the exercise quotes: [`hpa-first-cluster.log`](logs/hpa-first-cluster.log). The 403 was not explained.
- `ingress.log` is the second run of `ingress.sh` on the full-run cluster: the first printed no location blocks
  (a grep pattern that missed tab indentation; fixed). On the first cluster the controller had stopped at
  `socket() [::]:80 failed (97: Address family not supported by protocol)`: the sandbox kernel has no IPv6, hence
  `disableIPV6: true` in the values (capture-only, not needed on GKE).
- `c4`: `kind load docker-image` failed on the first cluster (`unknown containerd config version: 4`); the image is
  imported with `docker save | ctr -n k8s.io images import -` into each worker instead.

## Not run (and why)

- **Everything that needs Google**: the GKE clusters, the cloud load balancer, node pools and the cluster
  autoscaler, Workload Identity, Vertex AI, Artifact Registry pushes and pulls with credentials, `gcloud container
  clusters get-credentials`, `pulumi up` and `destroy` against GCP. Their answers (Q5, B6's GKE half, C3, C7's
  causes, C9, D2–D5) cite the code at `3ecef56`, the captured first errors and GKE's documented behaviour, and
  say "not checked here".
- **`Multi-Attach` (Q5, D2)**: kind's `standard` storage class makes node-local volumes, so a second Pod is pinned
  to the volume's node (or stays `Pending`) instead of failing to attach; it cannot reproduce a Compute Engine
  disk.
- **The cheese app's own images** (the API image is about 5 GB, and they are never pushed anywhere here): B8's
  backends are stand-ins; the API's routing was checked separately with its own code (`fastapi.sh`).
- **C9** (a config key typo) and **C10** (line 74) are answered from the code and `laptop/c03`, `c12`; no Pulumi
  run was needed.
- **Chroma's data path (D5)**: from the digest's registry check of 2026-11-07; no Chroma Pod was restarted.

## Cleanup

Every object was deleted by its script (`kubectl delete …`, `helm uninstall nginx-f5`), then the cluster with
`kind delete cluster --name l22ex` (`kind-setup.log`, "down": `Deleted nodes: ["l22ex-worker2"
"l22ex-control-plane" "l22ex-worker"]`), kind's Docker network `kind`, and every image pulled or built for these
checks (`kindest/node:v1.34.11`, `python:3.13-slim-bookworm`, `l22ex/entrypoint:1`): `docker images` was empty
afterwards. The Docker daemon and the proxy relay started for the checks were stopped by their process IDs. The
scratch folder (the kind binary, Helm, trial logs) was outside the repository. Nothing was written outside the
containers, the scratch folder and this folder.
