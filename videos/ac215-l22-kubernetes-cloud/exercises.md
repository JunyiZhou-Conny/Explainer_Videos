# Exercises · AC215 L22 — Scaling: Kubernetes in the cloud (the cheese app on GKE)

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-07 (`assets/terminal/`: `laptop/…` is a fresh Docker 29.8.2 engine standing in for your laptop,
with the deployment toolbox built after its two one-line fixes; `kind/…` is the **stand-in cluster**,
kind v0.31.0 with Kubernetes v1.34.11, one control plane and two workers; provenance in
[`ASSETS.md`](ASSETS.md)), and the extra checks run for these exercises on a second kind cluster of the
same version (`l22ex`), listed with their scripts and logs in
[`assets/exercise-checks/`](assets/exercise-checks/README.md). The repository is `dlops-io/cheese-app-v3`
at `3ecef56` (`main`); `README:NN` means its README's line NN, and code references are `path:line` under
`src/`. Nothing here used a Google account or a key: kind is **not GKE** (no cloud load balancer, no
node pool, no autoscaler, no Workload Identity). Whatever only GKE can show is worked out from the code,
the lecture and Kubernetes' documented behaviour, and the answer says so. Versions are those at the time
of recording; yours may be newer. Pod names, hashes, ports and private addresses (`10.96.…`, `10.244.…`,
`172.18.…`) differ on every cluster. Wherever an answer shows `<IP>`, `your-gcp-project` or the
README's `ac215-project`, put your own.

The hands-on tasks run on the warm-up's test cluster (part 1: the game, namespace `default`) or on
your cheese-app cluster (part 2: add `-n cheese-app-namespace`). Every task creates something: delete
it afterwards, and delete the cluster the same day.

---

## Part A · The five questions from the end of the video

**Q1. Which control-plane part decides where a new Pod runs, and which notices that a Pod died?**

<details><summary>Answer</summary>

- **Where:** the **scheduler** (`kube-scheduler`). It picks a node for every Pod that has none yet,
  from the nodes' free capacity (their *requests*, not their actual use: B6) and their taints.
- **Noticing:** the **controllers** (`kube-controller-manager`), here the ReplicaSet controller. It
  watches through the API server, sees "desired 2, actual 1" and creates a new Pod; the scheduler
  places it; that node's **kubelet** starts its container. Nobody calls anybody: each part watches the
  API server, which stores the wish in etcd (Lecture 22, slides 24–26).

One delete on the stand-in shows the chain in the event list
([`k8s.log`](assets/exercise-checks/logs/k8s.log), "Q1"): `Killing · kubelet` (the old Pod),
`SuccessfulCreate · replicaset-controller · Created pod: web-5cd9789488-lfcrp`,
`Scheduled · default-scheduler · Successfully assigned default/web-5cd9789488-lfcrp to l22ex-worker`,
then `Pulled`, `Created`, `Started` from the kubelet. The video's capture is `kind/k53`, `k54`, `k64`.

One distinction worth keeping: if only the **container** crashes, the Pod is still there and the
**kubelet** on its node restarts the container in place (same Pod name, `RESTARTS` goes up: B3). The
ReplicaSet controller acts when a **Pod** is gone: deleted, evicted, or lost with its node.
</details>

**Q2. Why does `kubectl get all` show only `service/kubernetes`, and what flag fixes it?**

<details><summary>Answer</summary>

kubectl looks in one **namespace** at a time, and without a flag that is `default` (or whatever your
kubeconfig's context names). In `default` there is only the Service `kubernetes`, the door to the API
server itself (`kind/k03`). The cheese app lives in `cheese-app-namespace`
(`deploy_k8s/create_cluster.py:141-145`; everything in `setup_containers.py` and `setup_loadbalancer.py`
sets `namespace=namespace.metadata.name`). Fixes:

- `-n cheese-app-namespace` (or `--namespace=cheese-app-namespace`, as README:490–492 write it);
- `--all-namespaces` (`-A`) to see every namespace, `kube-system` included (`kind/k04`, `k05`);
- or make it the default for your context:
  `kubectl config set-context --current --namespace=cheese-app-namespace`.

On the game of part 1, `get all` does show `web`, because `deploy-k8s-tic-tac-toe.yml` names no
namespace and lands in `default`.
</details>

**Q3. How does the `web` Service know which Pods are its own, and why does the API reach Chroma at
`vector-db:8000`?**

<details><summary>Answer</summary>

**Labels.** The Deployment's template stamps every Pod with `run: web`
(`src/deployment/deploy-k8s-tic-tac-toe.yml:13-14`); the Service's `selector: run: web` (`:33-34`) is a
query that is re-run all the time, and its result is the endpoint list: `endpoints/web
10.244.1.2:8080,10.244.2.2:8080` (`kind/k50`). When a Pod is replaced, its new address joins the list
(`k54`). Names play no part: take the label off a Pod and it drops out of the list at once, still
running (B1).

**Names.** A Service gets a stable virtual IP and a DNS name, `<service>.<namespace>.svc.cluster.local`
(`kind/k52`: `web.default.svc.cluster.local` → `10.96.52.79`, the CLUSTER-IP of `k11`). The cheese app's
Chroma Service is called `vector-db` and listens on 8000 (`setup_containers.py:176-196`), and the API
Pod gets `CHROMADB_HOST=vector-db` and `CHROMADB_PORT=8000` (`:297-304`). The short name works because a
Pod's `/etc/resolv.conf` searches its own namespace first: in `cheese-app-namespace` the search list
starts with `cheese-app-namespace.svc.cluster.local`, and `vector-db` resolves; from `default` it does not
(B5). This is lecture 20's "containers find each other by name on a Docker network", now done by the
cluster's DNS, and it survives every Pod replacement because the name belongs to the Service.
</details>

**Q4. Trace one click from `<IP>.sslip.io` to the API Pod. Why does the bare IP answer 404?**

<details><summary>Answer</summary>

1. **DNS:** `sslip.io` answers any name `<IP>.sslip.io` with `<IP>` itself, so no DNS setup is needed.
   The program builds that host name from the load balancer's IP (`setup_loadbalancer.py:59-60`).
2. **Load balancer:** `<IP>` belongs to the Service of the Helm release `nginx-f5`, `type: LoadBalancer`
   (`setup_loadbalancer.py:11-46`; Pulumi reads it back at `:49-58` as `nginx-ingress-service`). GKE's
   controllers asked Google for that load balancer and address. It forwards to a node.
3. **NGINX Ingress controller** (a Pod, F5's chart `nginx-ingress` 2.3.1): it compares the request's
   **`Host` header** with the Ingress rule, `host=<IP>.sslip.io` (`:79`), then the path: `/api-service`
   (`pathType: Prefix`) → Service `api`, port 9000 (`:83-93`); everything else → Service `frontend`, port
   3000 (`:96-106`).
4. **Service → Pod:** the `api` Service (`setup_containers.py:325-343`, selector `run: api`) forwards to an
   API Pod on 9000.
5. **The path is kept:** the API receives `/api-service/status` with its prefix. Nothing strips it,
   unlike L20's nginx `proxy_pass …/`. The Pod has `ROOT_PATH=/api-service` (`setup_containers.py:309-312`),
   and the app mounts its routes under it (`src/api-service/api/service.py:13, 50`), so `/api-service/status`
   answers `{"version":"3.0"}` (`:34-36`). This is the call the footer makes
   (`frontend-react/.env.production:2`, `NEXT_PUBLIC_BASE_API_URL=/api-service`).

**The bare IP:** same load balancer, same controller, but the browser now sends `Host: <IP>`. No rule
has that host, so the controller's default server answers `404 Not Found`. Use `app_url` from the
outputs.

Checked on the stand-in with the same chart and version, the repo's Ingress written as YAML and two
stand-in backends that print what they receive ([`ingress.log`](assets/exercise-checks/logs/ingress.log)):
with `Host: <IP>.sslip.io`, `/api-service/status` reached the `api` stand-in as `GET /api-service/status`
and `/` reached `frontend`; with `Host: <IP>`, both answered `<title>404 Not Found</title>`. The
`ROOT_PATH` half was checked with the API's routing code and its pinned FastAPI 0.120.4
([`fastapi.log`](assets/exercise-checks/logs/fastapi.log)): `ROOT_PATH='/api-service' GET
/api-service/status -> 200 {"version":"3.0"}`, and `GET /status -> 404`. The cloud load balancer itself
was not checked (the stand-in used a NodePort).
</details>

**Q5. Why can the frontend scale to 3 but the API cannot, and what does the autoscaler add?**

<details><summary>Answer</summary>

- **The frontend** keeps nothing on disk and every Pod requests the same `cpu: 250m`, `memory: 2Gi`
  (`setup_containers.py:79-82`). `kubectl scale deployment frontend --replicas=3 -n cheese-app-namespace`
  asks for three; the scheduler places each copy on a node with 2 Gi of unreserved memory left. An
  `n2d-standard-2` has 8 GB, of which GKE keeps a part for the system, and nginx, Chroma and the system
  Pods take their share: when a copy does not fit, it stays `Pending` (B6, C6).
- **The autoscaler** (`create_cluster.py:63-66`: `min_node_count=1`, `max_node_count=2`) is the **node**
  level: when a Pod is `Pending` because no node has room, it adds a node, up to two; when nodes stay
  under-used, it removes one. It never adds Pods. Ask for many more replicas and some stay `Pending`
  for good: the pool stops at two.
- **The API** mounts `persistent-pvc`, a `ReadWriteOnce` disk (`setup_containers.py:17-30`, `:265-271`,
  `:286-290`): a Compute Engine disk attaches to **one node** at a time. A second API Pod on the same node
  could share it; one on the other node waits in `ContainerCreating` with a `Multi-Attach error`, and more
  nodes cannot help, because the limit is the disk. The API also has **no `resources` block**
  (`:273-315`), so the scheduler cannot plan for it, and a Pod autoscaler on CPU cannot work (B7).

So in this repository, scaling is: nodes automatically (1–2), Pods by hand (`kubectl scale`, as
Milestone 5 asks), and only for stateless Deployments with requests. The `Multi-Attach` and GKE
autoscaler behaviour were **not checked here**: kind has no node pool, and its local disks pin a Pod to
the disk's node instead of failing; the answer rests on the code and GKE's documented behaviour.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Take a Pod out of its Service.** With the game running (2 replicas), pick one web Pod and change
its label: `kubectl label pod <one web pod> run=debug --overwrite`. Predict: how many Pods exist a few
seconds later, which ones does the Service send traffic to, and who owns the relabelled Pod? Then check
with `kubectl get pods -L run`, `kubectl get endpointslices -l kubernetes.io/service-name=web` and
`kubectl get pod <that pod> -o jsonpath='{.metadata.ownerReferences}'`.

<details><summary>Answer</summary>

Three Pods. The ReplicaSet counts the Pods that match **its** selector (`run=web`,
`pod-template-hash=…`); it now sees one, so it creates a replacement. The relabelled Pod keeps running,
but the Service's endpoint list no longer contains it, and the ReplicaSet has released it: its
`ownerReferences` are empty. On the stand-in ([`k8s.log`](assets/exercise-checks/logs/k8s.log), "B1"):
`web-5cd9789488-lfcrp` shows `RUN debug`, a new `web-5cd9789488-zbj4x` is 7 s old, and the endpoints went
from `10.244.2.2,10.244.1.3` to `10.244.2.2,10.244.1.4`; `ownerReferences:` prints nothing. Delete the
orphan yourself (`kubectl delete pod …`): nothing else will. This is a real debugging trick: pull a
misbehaving Pod out of traffic and keep it alive to inspect it.
</details>

**B2. Change the template.** Run `kubectl get rs -l run=web`, then
`kubectl set env deployment/web COLOR=blue` and `kubectl get rs -l run=web` again. Predict the names.
Then `kubectl rollout undo deployment/web` and predict once more.

<details><summary>Answer</summary>

The ReplicaSet's name is the Deployment's name plus a **hash of the Pod template**. A new environment
variable is a new template, so a **new ReplicaSet** appears and the old one is scaled to 0 (it is kept
for rollbacks): `web-5cd9789488 0 0 0` and `web-77d995cd45 2 2 2`, its Pods named
`web-77d995cd45-…`. The undo restores the old template, so the **old** ReplicaSet scales back to 2 and the
new one to 0 (`k8s.log`, "B2"). The hash is computed from the template only, which is why the video's
capture and this check, on two different kind clusters, both got `web-5cd9789488` from the same file.
Scaling (`--replicas`) is **not** a template change: it keeps the same ReplicaSet (`kind/k55`).
</details>

**B3. A crash is not a delete.** Apply
[`manifests/crasher.yaml`](assets/exercise-checks/logs/manifests/crasher.yaml), a Deployment whose
container prints `started`, waits 8 s and exits with code 1. Predict what `kubectl get pods -l
run=crasher` shows after 5 s, 15 s and 45 s, and whether the Pod's name changes. Then delete the Pod
and predict again.

<details><summary>Answer</summary>

The **same Pod** stays; its container is restarted in place by the **kubelet**, and the waits between
restarts grow (10 s, 20 s, 40 s … up to 5 minutes: `CrashLoopBackOff`). On the stand-in: `Running 0`
at 5 s, `Running 1 (4s ago)` at 15 s, `Error 2 (25s ago)` at 45 s, all for `crasher-6dd5c85dd5-lp7nj`;
`kubectl describe` shows `Last State: Terminated`, `Exit Code: 1`, `Restart Count: 2` and `Back-off
restarting failed container` (`k8s.log`, "B3"). `kubectl logs <pod>` shows `started`, `crashing`
(`--previous` shows the run before). After `kubectl delete pod`, the ReplicaSet makes a **new** Pod
(`crasher-6dd5c85dd5-rld67`, `RESTARTS 0`). Restarting forever does not fix a bug: the status column
tells you to read the logs. For the cheese app this is what an API that cannot reach Chroma at start-up
can look like (digest §6, item 13).
</details>

**B4. "Mapped to 31366 on every node."** `kubectl get service web` shows `80:<nodePort>/TCP`. Predict
whether that port answers on a node that runs **no** web Pod. On kind, try it from the control-plane
node, which runs none.

<details><summary>Answer</summary>

Yes. kube-proxy on **every** node forwards the NodePort to the Service's Pods, wherever they are. The
stand-in's control-plane node (no web Pod; it does not run app Pods) answered `200`, like both workers
(`k8s.log`, "B4": `l22ex-control-plane=… -> 200`). A `LoadBalancer` Service is a NodePort Service plus a
cloud load balancer in front: on GKE the load balancer sends traffic to the nodes, and kube-proxy takes
it from there. The NodePort is assigned at random from 30000–32767 (`31366` in the video, `32440` here).
On GKE the default firewall does not open NodePorts to the internet (and the cheese app's nodes have
no public address at all), so from outside, test through the external IP.
</details>

**B5. Names across namespaces.** Create the namespace `cheese-app-namespace` and a Service `vector-db`
in it (`kubectl create service clusterip vector-db --tcp=8000:8000 -n cheese-app-namespace`). From a
throwaway Pod in `default`, predict which of these resolve: `vector-db`,
`vector-db.cheese-app-namespace`, `vector-db.cheese-app-namespace.svc.cluster.local`. Then the same short
name from a Pod in `cheese-app-namespace`.

<details><summary>Answer</summary>

From `default`: `vector-db` fails (`NXDOMAIN` for `vector-db.default.svc.cluster.local`,
`vector-db.svc.cluster.local`, `vector-db.cluster.local`), and so does `vector-db.cheese-app-namespace`
**with busybox's `nslookup`**, which does not apply the search list to a name that contains a dot; the
full name
`vector-db.cheese-app-namespace.svc.cluster.local` resolves to the Service's IP. From a Pod inside
`cheese-app-namespace`, the short `vector-db` resolves, because that Pod's search list starts with
`cheese-app-namespace.svc.cluster.local` (`k8s.log`, "B5": `search default.svc.cluster.local …` versus
`search cheese-app-namespace.svc.cluster.local …`). With a normal resolver (glibc, as in the API's
Python image), `vector-db.cheese-app-namespace` also works, through the `svc.cluster.local` search entry;
that form was not tested here. Rule: the short name works inside its namespace; from elsewhere, add
the namespace. This is why the API and Chroma must be in the same namespace for
`CHROMADB_HOST=vector-db`.
</details>

**B6. Requests decide the packing.** Apply
[`manifests/fat.yaml`](assets/exercise-checks/logs/manifests/fat.yaml) (one Pod requesting 3 CPUs),
then scale it to 3. Each stand-in node offers 4 CPUs (`kubectl describe node` → `Allocatable`).
Predict where the three Pods go. On your GKE cluster, the same question is
`kubectl scale deployment frontend --replicas=3 -n cheese-app-namespace`.

<details><summary>Answer</summary>

One per worker, and the third `Pending`: each worker has 4 CPUs allocatable with 100m already
requested, so after one 3-CPU Pod only 0.9 CPU is left, and the control-plane node is tainted against
app Pods. The scheduler counts **requests**, not real use (the Pods only `sleep`). Stand-in result: two
`Running` on `l22ex-worker` and `l22ex-worker2`, one `Pending`, with `FailedScheduling … 0/3 nodes are
available: 1 node(s) had untolerated taint(s), 2 Insufficient cpu` (`k8s.log`, "B6 / C6"). On GKE, with
the frontend's `2Gi` memory request, the third copy may or may not fit on one node, depending on what
else runs there; if it does not, the **cluster autoscaler** adds the second node and the `Pending` Pod
lands there after a few minutes. That GKE half was not run here (kind has no autoscaler). Scale back
with `--replicas=1` when you are done.
</details>

**B7. A Pod autoscaler needs requests.** With metrics-server running (GKE has it; on kind install it),
run `kubectl autoscale deployment web --cpu-percent=50 --min=2 --max=4` and predict `kubectl get hpa web`
after a minute. Then give the Pods a request, `kubectl set resources deployment web --requests=cpu=50m`,
and predict again. On your cluster, the same experiment on `frontend` and `api` (README has no HPA).

<details><summary>Answer</summary>

The game's container has **no requests** (`requests: {}`), so the HPA has no denominator for "50 % of
the request": `TARGETS cpu: <unknown>/50%`, condition `ScalingActive False`, `failed to get cpu
utilization: missing request for cpu in container web of Pod web-5cd9789488-…`. With `cpu=50m`, a
minute and a half later: `cpu: 0%/50%` and the HPA works
([`hpa-first-cluster.log`](assets/exercise-checks/logs/hpa-first-cluster.log)). On the cheese app,
`frontend` has a request (`250m`, `setup_containers.py:80`) and would show a percentage; `api` has none
and would show `<unknown>`, and even with one it could not spread across nodes (Q5). `kubectl autoscale`
also warns that `--cpu-percent` is deprecated in favour of `--cpu=50%`. Delete the HPA afterwards
(`kubectl delete hpa web`). Note: in the full re-run on a fresh stand-in cluster, metrics-server's API
never became available (`FailedDiscoveryCheck`), and the HPA showed `<unknown>` both times for that other
reason (`k8s.log`, "B7"); when `kubectl top pods` fails, fix metrics first.
</details>

**B8. Follow the Ingress.** On your cheese-app cluster, predict who answers, and which path it
receives, for `http://<IP>.sslip.io` + `/`, `/status`, `/api-service/status`, `/api-service`,
`/api-servicex/status`, and for `http://<IP>/`. Check with `curl -i` and the API's logs
(`kubectl logs deployment/api -n cheese-app-namespace`).

<details><summary>Answer</summary>

| request (`Host: <IP>.sslip.io` unless said) | the controller sends it to | the API app answers |
| --- | --- | --- |
| `/`, `/status` | `frontend:3000`, path unchanged | — (the frontend's pages) |
| `/api-service/status` | `api:9000`, as `/api-service/status` | `200 {"version":"3.0"}` |
| `/api-service` | `api:9000`, as `/api-service` | `307` redirect to `/api-service/` |
| `/api-servicex/status` | **`api:9000`**, as `/api-servicex/status` | `404 {"detail":"Not Found"}` |
| `Host: <IP>`, any path | nobody: the controller's own `404 Not Found` | — |

The surprise is `/api-servicex/status`. The Kubernetes spec says a `Prefix` path matches whole path
segments, so `/api-service` should not match `/api-servicex`. The F5 controller, however, writes the rule
as a plain nginx prefix location, `location /api-service {`, and nginx prefixes match characters: the
request went to the API stand-in ([`ingress.log`](assets/exercise-checks/logs/ingress.log): "the location
blocks the controller generated", and the `/api-servicex/status` request answered by `api-…`). The app
then rejects it, because it is mounted at `/api-service` (`fastapi.log`: `GET /api-servicex/status -> 404`).
Harmless here, but it is why a controller's behaviour, not only the spec, decides your routing. The
table's routing half was checked on the stand-in with the same chart and version (2.3.1, controller
5.2.1) and stand-in backends; the right column with the API's own routing code. Not checked: the real
frontend's answers and the cloud load balancer.
</details>

---

## Part C · Debugging

**C1. The README's first debugging line.** `kubectl logs -n cheese-app-cluster-namespace
job/vector-db-loader -c wait-for-chromadb` (README:620) prints `error: error from server (NotFound):
namespaces "cheese-app-cluster-namespace" not found …`. You fix the namespace and get a second error.
Which, and why? What is the right command?

<details><summary>Answer</summary>

The debugging block was written for an earlier version of the program, with a namespace named after
the cluster and a Job with an init container `wait-for-chromadb` (digest, erratum 2). Today the
namespace is `cheese-app-namespace` (`create_cluster.py:143`) and the Job has **one** container,
`vector-db-loader` (`setup_containers.py:211-235`). With the namespace fixed:
`error: container wait-for-chromadb is not valid for pod vector-db-loader-p6k5z`. Drop `-c`:
`kubectl logs -n cheese-app-namespace job/vector-db-loader` prints the loader's output (checked on a Job
of the same shape, [`k8s.log`](assets/exercise-checks/logs/k8s.log), "C1"; the README's line as
captured: `kind/k30`). The same two fixes apply to all 14 lines of README:620–656, `deployment/api`
included (`kubectl logs deployment/api -n cheese-app-namespace -f`).
</details>

**C2. Angle brackets.** README:634 is `kubectl logs -n cheese-app-cluster-namespace <pod-name>`. Pasted
as is, it prints `syntax error near unexpected token 'newline'`; README:638 (`… <pod-name> -c
wait-for-chromadb`) prints `pod-name: No such file or directory`. Neither message mentions kubectl. Why?

<details><summary>Answer</summary>

The shell reads `<` and `>` before kubectl runs: `<pod-name>` means "read input from the file
`pod-name`, then redirect output to …". In 634 the `>` is followed by the end of the line: a syntax
error, nothing runs (`kind/k34`). In 638 the `>` is followed by `-c`, which is valid, so the shell tries to
open the file `pod-name`, which does not exist (`kind/k36`). Replace the **whole** placeholder, brackets
included, with your Pod's name from `kubectl get pods -n cheese-app-namespace | grep vector-db-loader`.
The same holds for the README's sample Pod names (`api-c4fb784b-2llgs`, `vector-db-loader-9gr5m`): they are
the author's, not yours.
</details>

**C3. kubectl worked yesterday.** You deployed yesterday. Today you start the toolbox again, and
`kubectl get pods -n cheese-app-namespace` prints `The connection to the server localhost:8080 was
refused - did you specify the right host or port?`. Is the cluster down?

<details><summary>Answer</summary>

No. kubectl has no kubeconfig, and with none it falls back to `localhost:8080`. The kubeconfig was
written by one `gcloud container clusters get-credentials …` that Pulumi ran at create time
(`create_cluster.py:192-198`) **inside the toolbox container**, and `docker-shell.sh` runs that container
with `--rm` (`:34`): it went away when you exited. A Pulumi `command.local.Command` runs once, at create,
so a later `pulumi up` does not write it again either. Fix, once per toolbox session:
`gcloud container clusters get-credentials cheese-app-cluster --region us-central1 --project <your project>`.
The code passes the region to `--zone`; `--region` says what it means. The captures show the symptom
(`laptop/b40`–`b45`, before any cluster) and the command up to its first error without an account
(`b52`); a successful `get-credentials` was not run here.
</details>

**C4. `command` or `args`?** On the comparison branch `cluster-updates`, the loader's container is given
`command=["cli.py", "--download", "--load", "--chunk_type", "recursive-split"]`
(`cluster-updates:src/deployment/deploy_k8s/__main__.py:426-432`); `main` gives the same list as
`args=[…]` (`setup_containers.py:227-233`). The image's Dockerfile ends with
`ENTRYPOINT ["/bin/bash","docker-entrypoint.sh"]` (`src/vector-db/Dockerfile:51`). Predict the loader
Pod's status in each case.

<details><summary>Answer</summary>

`command` replaces the image's **ENTRYPOINT**, `args` replaces its **CMD**. With `args`, the entrypoint
script runs and receives `cli.py --download …`, then runs `uv run python $args`
(`src/vector-db/docker-entrypoint.sh:14-22`): the same as `docker run <image> cli.py …` in lecture 20.
With `command`, the runtime tries to execute a program named `cli.py`, which is not on `$PATH`: the
container never starts. Checked with an image shaped the same way (an ENTRYPOINT script that prints
its arguments, [`manifests/entry.Dockerfile`](assets/exercise-checks/logs/manifests/entry.Dockerfile)):
`loader-args` `Complete`, logs `entrypoint received: cli.py --download --load --chunk_type
recursive-split`; `loader-command` `StartError`, `exec: "cli.py": executable file not found in $PATH`,
`Exit Code: 128`, Job `Failed` (`k8s.log`, "C4"). In Pulumi, this Job would fail, and on `main` the API
waits for it (D1).
</details>

**C5. "Retry up to 4 times."** `setup_containers.py:206` says `backoff_limit=3,  # Retry up to 4 times on
failure`. If the loader fails every time, how many loader Pods do you find, and how long does it take
the Job to give up?

<details><summary>Answer</summary>

**Four** Pods: the first attempt plus 3 retries (`backoffLimit` counts retries; with
`restartPolicy: Never`, each retry is a new Pod). The comment's "4 times" counts attempts, not retries.
The waits between attempts grow (10 s, 20 s, 40 s), so the Job is marked `Failed` with
`BackoffLimitExceeded` after a little over a minute. Checked with a Job of the same settings
([`manifests/failing-job.yaml`](assets/exercise-checks/logs/manifests/failing-job.yaml)): four Pods in
`Error`, aged 73 s, 63 s, 43 s and 3 s, `Pods Statuses: 0 Active (0 Ready) / 0 Succeeded / 4 Failed`,
`Job has reached the specified backoff limit` (`k8s.log`, "C5"). The failed Pods stay, so
`kubectl logs <pod>` still works on each; delete the Job to remove them. To run the loader again after
a fix: `kubectl delete job vector-db-loader -n cheese-app-namespace`, then `pulumi up --stack dev
--refresh -y`.
</details>

**C6. Read the scheduler's message.** A frontend copy stays `Pending`, and `kubectl describe pod` ends
with `0/3 nodes are available: 1 node(s) had untolerated taint(s), 2 Insufficient cpu. … preemption:
0/3 nodes are available: 1 Preemption is not helpful for scheduling, 2 No preemption victims found for
incoming pod.` Translate each part. Which lamp of the video's cluster picture is lit?

<details><summary>Answer</summary>

The **scheduler's** lamp. It checked three nodes: one carries a taint the Pod does not tolerate (the
control plane, on kind; GKE does not list its control plane as a node), and two do not have enough
**unrequested** CPU left for the Pod's request. "Preemption" means it also looked for lower-priority Pods
to evict and found none. (This exact message is from B6 on the stand-in, `k8s.log`, "B6 / C6".) Fixes:
lower the request, scale down, or add room. On GKE the cluster autoscaler adds a node when that would
help, up to `max_node_count=2`; then the message adds that the node group's maximum size was reached
(not checked here). For memory you would read `Insufficient memory`, which is the frontend's case
(`2Gi`).
</details>

**C7. `ImagePullBackOff`.** After `pulumi up`, a Pod shows `ErrImagePull`, then `ImagePullBackOff`.
`kubectl describe pod <pod> -n cheese-app-namespace` says `failed to resolve reference
"us-docker.pkg.dev/<project>/cheese-app-repository/cheese-app-frontend-react:<tag>"`. Name three causes
in this tutorial.

<details><summary>Answer</summary>

1. The images were never built and pushed in **this** project: `deploy_images` was skipped, ran in
   another project, or its `pulumi up` stopped at the push (L20's first error was the push's 403).
2. The Artifact Registry **repository** `cheese-app-repository` does not exist: no code creates it
   (`deploy_images/__main__.py:14-15` only builds the URL). Create it once with
   `gcloud artifacts repositories create cheese-app-repository --repository-format=docker --location=us`.
3. The nodes cannot read it: they pull as the account in `security:gcp_service_account_email`
   (`create_cluster.py:50`), `deployment` per README:442, which has Artifact Registry Administrator
   (README:243). If you set another account there, give it Artifact Registry Reader.

Also possible: an image built for arm64 on a Mac outside `deploy_images` (the nodes are amd64; it then
pulls, but fails with `exec format error`). The status alternates: `ErrImagePull` on each try,
`ImagePullBackOff` while kubelet waits before the next one. On the stand-in, a never-pushed placeholder
tag in the placeholder project failed with `failed to authorize: failed to fetch anonymous token: …
403 Forbidden` (kind's nodes have no Google identity), `ErrImagePull`, then `Back-off pulling image`
([`k8s.log`](assets/exercise-checks/logs/k8s.log), "C7"). Your nodes do have an identity, so your
wording will differ (typically `not found`, or a `403`/`denied` on the repository); the cause list does
not.
</details>

**C8. A Python error in a Kubernetes preview.** `pulumi preview --stack dev --refresh` in `deploy_k8s`
fails with `File "/app/deploy_k8s/setup_containers.py", line 70` … `TypeError: 'NoneType' object is not
subscriptable`. You haven't touched the code. What happened?

<details><summary>Answer</summary>

`setup_containers.py:10-14` asks the stack `organization/deploy-images/dev`, **in the same state
backend**, for its outputs `cheese-app-…-tags`, and `:69-71` takes `tags[0]`. If that stack exists but
never finished a `pulumi up` there, the output is `None`, and `None[0]` raises this error (`laptop/c13`,
the recording's local backend, where the images stack only had `init` and a preview). If the stack does
not exist at all, the error is `unknown stack "organization/deploy-images/dev"` instead (digest §6, item
8). README:416's "only required if you have NOT already done this" means: done, with `pulumi up`, into
this same bucket. Run `deploy_images`'s `pulumi up --stack dev -y`, then preview again: the plan shows
`+ 23 to create` (`laptop/c20`, with placeholder tags).
</details>

**C9. A typo that fails late.** You typed
`pulumi config set security:gcp_ksa_service_acount_email gcp-service@<your project>.iam.gserviceaccount.com --stack dev`
(one `c` missing). `pulumi preview` looks normal. What goes wrong, and where would you have caught it?

<details><summary>Answer</summary>

`create_cluster.py:10-12` reads `pulumi.Config("security").get("gcp_ksa_service_account_email")`, which
returns `None` for a key that is not set, without an error. Python's f-strings turn it into the text
`"None"`: the KSA's annotation becomes `iam.gke.io/gcp-service-account: None` (`:158`) and the IAM binding
targets `projects/<project>/serviceAccounts/None` (`:179-181`). The preview is fine, because nothing has
asked Google yet; `pulumi up` then fails at `api-gsa-wi-user`, or, if it got through, the API Pods would
get 403s from Vertex AI. Catch it before `up` with `pulumi config` (the video's extra, `laptop/c12`): it
lists every key; yours would show the misspelt one and lack the right one. Then `pulumi config rm` the
typo and set the right key. (A missing `gcp_service_account_email` is worse in another way: the node pool
then gets no service account from the config and GKE uses the project's default one.) This answer is
read from the code and Pulumi's documented `Config.get`; it was not run against GCP.
</details>

**C10. A bug on line 74?** `deploy_images/__main__.py:74` exports
`pulumi.export("cheese-app-vector-db-cli-tags", frontend_image.tags)`. Does the loader Job get the
frontend's image?

<details><summary>Answer</summary>

No. The variable `frontend_image` is **reused**: line 43 assigns the frontend's `docker_build.Image` to
it, line 62 assigns the vector-db-cli's image to the same name, and line 74 runs after that. The
preview confirms it (`laptop/c03`): `cheese-app-vector-db-cli-tags` is
`…/cheese-app-vector-db-cli:20261107205032`. Confusing, not wrong; a name like `vector_db_cli_image`
would say what it is. Reading the plan or the outputs settles questions like this faster than reading
the code.
</details>

---

## Part D · Think

**D1. Why does the API wait for the loader?** `setup_containers.py:319-321` makes the API Deployment
depend on the loader **Job**; the `cluster-updates` branch makes it depend only on the vector-db Service.
Give one advantage and one disadvantage of each.

<details><summary>Answer</summary>

- **main:** Pulumi waits until the Job is complete before it creates the API, so the API never answers
  RAG questions against an empty collection. Disadvantage: a broken loader blocks the whole API; `pulumi
  up` sits on `vector-db-loader` until its timeout, and **no API Pod exists** until the loader succeeds
  (C5: it can fail for good after four attempts).
- **cluster-updates:** the API starts in parallel; faster deploys, and the frontend and API work even if
  the loader fails. Disadvantage: early RAG requests can fail on a missing collection, and nobody notices
  that the loader failed.

A middle way: start the API at once and give it a readiness check that reports "not ready" until the
collection exists; the Service then sends it no traffic until then.
</details>

**D2. One replica can still clash.** The API runs a single replica with a `ReadWriteOnce` disk. You push
a new image and `pulumi up` changes the Deployment. Can `Multi-Attach` happen even with `replicas: 1`?
What would prevent it?

<details><summary>Answer</summary>

Yes. A Deployment's default strategy is `RollingUpdate`: it starts the **new** Pod before it removes the
old one. If the scheduler puts the new Pod on the other node, it cannot attach the disk the old Pod still
holds: `Multi-Attach error`, stuck in `ContainerCreating`, and the rollout stalls (the old Pod keeps
serving, so nothing is down, but nothing moves). With one node it works by luck. Fixes: `strategy:
Recreate` for Deployments with an RWO disk (old Pod first, then the new one; a short gap), or storage that
several nodes can share (ReadWriteMany). The same holds for `vector-db` (`setup_containers.py:40`). Not
checked here: kind's local disks pin a Pod to the disk's node instead of failing.
</details>

**D3. What to delete first.** Part 1 deletes the game (`kubectl delete -f deploy-k8s-tic-tac-toe.yml`)
before the cluster; part 2 runs `pulumi destroy` and then lists clusters, forwarding rules, disks and
firewall rules. Why does the order matter, and what can survive `destroy` on purpose?

<details><summary>Answer</summary>

Deleting a `LoadBalancer` Service or a PVC asks GKE's controllers to delete the cloud load balancer or
the disk **in the background**. If the cluster goes first, nobody is left to finish that work, and
forwarding rules, firewall rules or `pvc-…` disks can stay behind and keep costing money; the VPC's own
deletion may then fail with "resource is in use". Deleting the Service while the cluster still exists
lets its controllers clean up. `pulumi destroy` removes what the stack created, in reverse order, but
the registry images are kept on purpose (`retain_on_delete=True`, `deploy_images/__main__.py:31, 51,
70`), and the state bucket and the registry repository were never part of the stack. Delete those by
hand when the course is over, and check the console's lists. (From the code and GKE's documented
behaviour; nothing was created in the cloud here.)
</details>

**D4. Workload Identity instead of a key.** In lecture 20 the API read `gcp-service.json` from a folder on
the VM. Here no key file exists in the cluster. How does the API Pod act as `gcp-service`, and what
would happen if you removed `service_account_name=ksa_name` from its Pod spec
(`setup_containers.py:261`)?

<details><summary>Answer</summary>

The Pod runs as the Kubernetes service account `api-ksa`, which is annotated with
`iam.gke.io/gcp-service-account: gcp-service@…` (`create_cluster.py:150-162`). The IAM binding
`api-gsa-wi-user` gives that KSA `roles/iam.workloadIdentityUser` on `gcp-service` (`:184-189`). When the
API's Google library asks the node's metadata server for a token, GKE's Workload Identity returns a
short-lived token for `gcp-service`. Nothing is stored, nothing to leak or rotate. Without
`service_account_name`, the Pod runs as the namespace's `default` KSA, which has no annotation and no
binding: it starts normally (the model comes from GitHub), but the first chat call to Vertex AI fails
with a permission error, and the API returns an error. Pods never get the node's own `deployment`
identity on node pools that use GKE's metadata server, which GKE documents as the default for new node
pools on a cluster with Workload Identity (`create_cluster.py:35-37`; the node pool sets nothing else).
Not checked here (no GKE, no Google account); this follows from
the code and GKE's documentation. The binding itself needs the right to edit `gcp-service`'s IAM policy,
which the README's role list very likely lacks (the video's "Service Account Admin" step, unverified).
</details>

**D5. The database forgets.** After a node repair, the `vector-db` Pod is re-created on a new node. The
RAG chat now answers that it has no context. The PVC `chromadb-pvc` is still `Bound`. What happened, and
what are two fixes?

<details><summary>Answer</summary>

The PVC is mounted at `/chroma/chroma` (`setup_containers.py:150`), the path of older Chroma images. The
Deployment runs the unpinned `chromadb/chroma` (`:132`), and today's image keeps its data in `/data`
(digest §6, item 14: its `/config.yaml` says `persist_path: "/data"`, checked against the registry on
2026-11-07). So the collection lived in the container's own writable layer and died with the Pod; the
10 Gi disk sat unused. The loader Job ran once and does not run again by itself. Fixes: run the loader
again (`kubectl delete job vector-db-loader -n cheese-app-namespace`, then `pulumi up --stack dev --refresh
-y`); for good, mount the PVC at `/data`, or pin the image to a version that uses `/chroma/chroma` (the
`cluster-updates` branch pins `chromadb/chroma:0.5.6`). The restart itself was not run here.
</details>
