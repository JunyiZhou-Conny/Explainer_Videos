#!/bin/bash
# Runs inside the capture laptop (see capture.sh) as user `student`, recording each tutorial command's
# output to its own file: "$ command", the output, "[exit N]".
# Usage: run_steps.sh <out_dir> <segment>
# README.md:N = dlops-io/cheese-app-v3 @ 3ecef56 (main), mounted read-only at /source/README.md;
# README commands are read from those exact lines (`readme a b`), so they run byte for byte as printed.
# Segments (file prefix = part of the video):
#   pre        (laptop/p..) clone, commit, branches, the sibling secrets/ folder, capture-only base images
#   tb-commit  (laptop/b01-b02a) README:404-406 `cd deployment` + `sh docker-shell.sh` as committed
#              (fails), then the two one-line Dockerfile fixes found for L20
#   tb-shell   (laptop/b03) `sh docker-shell.sh` again: builds; its shell stays open (run DETACHED by
#              capture.sh) until tb-close
#   tb-wait    capture-only: waits until that shell's prompt is up
#   tb-readme  (laptop/b1x-b5x) every README command of the K8s sections at the toolbox prompt: tool
#              checks, the warm-up's gcloud create/delete, deploy_images, deploy_k8s, kubectl, destroy
#   tb-local   (laptop/c..) extras: the same Pulumi programs on Pulumi's local file backend, up to their
#              first call that needs Google
#   kind-up    (kind/k00-k01) extra: the labelled stand-in cluster (kind) + capture-only wiring
#   kind-readme (kind/k02-k4x) the README's kubectl commands, from the toolbox, against the stand-in
#   kind-extra (kind/k5x-k7x) extras: rollout, self-healing, scaling, labels, DNS, a Job, port-forward
#   kind-down  (kind/k8x) extra: cleanup the stand-in
#   tb-close   capture-only: types `exit` into the open toolbox shell
# Steps whose name contains "-x-" are extras (not README steps): checks the video uses.
# capture-only work (proxy CA, placeholder keys, waiting for a prompt) is never shown as a README step.
OUT=$1; SEG=$2; export OUT
HERE="$(cd "$(dirname "$0")" && pwd)"
README=/source/README.md
umask 022
cd ~

mask() { if [ -n "$NAME_RE" ]; then sed -E "s/${NAME_RE}/‹instructor›/Ig"; else cat; fi; }
nocolor() { sed 's/\x1b\[[0-9;]*m//g'; }
step() {  # step <name> <command...>   (no terminal: plain output, as in a script)
  local name=$1; shift
  { echo "\$ $*"; bash -c "$*" 2>&1 | nocolor; echo "[exit ${PIPESTATUS[0]}]"; } | mask > "$OUT/$name.txt"
}
istep() {  # istep <name> <command> [<prompt regex | file:PATH> <typed line>]...   (in a terminal, typed)
  local name=$1 cmd=$2; shift 2
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $cmd"
    python3 "$HERE/ptyrun.py" --cols "${PTY_COLS:-100}" --rows "${PTY_ROWS:-40}" --timeout "${PTY_TIMEOUT:-900}" \
      "${args[@]}" -- bash -c "$cmd"
    echo "[exit $?]"; } | mask > "$OUT/$name.txt"
}
readme() { sed -n "$1,$2p" "$README"; }   # readme <first> <last>: README lines, verbatim
rl() { readme "$1" "$1" | sed 's/^[-*] *Run //; s/^[-*] *//; s/^`//; s/`$//'; }  # one inline README command
C=cheese-app-deployment
CENV=(-e CAPTURE=1)
case $SEG in kind*)
  # capture-only: the toolbox inherits the recording proxy from its capture-only base image; the
  # stand-in's API server (test-cluster-control-plane) is reached directly, as on a laptop with no proxy
  NP=localhost,127.0.0.1,test-cluster-control-plane,.svc,.cluster.local
  CENV=(-e NO_PROXY=$NP -e no_proxy=$NP);;
esac
cstep() {  # cstep <name> <workdir> <command>: typed at the deployment container's prompt (docker exec)
  local name=$1 wd=$2; shift 2
  { echo "\$ $*"; docker exec "${CENV[@]}" -w "$wd" $C bash -c "$*" 2>&1 | nocolor; echo "[exit ${PIPESTATUS[0]}]"; } | mask > "$OUT/$name.txt"
}
ctstep() {  # ctstep <name> <workdir> <shown command> <exec'd command> [<regex> <typed>]...: the same, in a terminal
  local name=$1 wd=$2 shown=$3 cmd=$4; shift 4
  local args=()
  while [ $# -gt 0 ]; do args+=(--expect "$1" --send "$2"); shift 2; done
  { echo "\$ $shown"
    python3 "$HERE/ptyrun.py" --cols 100 --rows 40 --timeout 300 "${args[@]}" -- docker exec -it "${CENV[@]}" -w "$wd" $C bash -c "$cmd"
    echo "[exit $?]"; } | mask > "$OUT/$name.txt"
}
make_key() {  # make_key <account>: capture-only, see the comment inside
  # There is NO real key here. A throwaway RSA key, generated now for no account and never written to
  # the repository, makes a well-formed service-account key file, so gcloud and Google's libraries load
  # it and the first real call fails where a student's would succeed (ASSETS.md, "What cannot run here").
  mkdir -p "$OUT/capture-only" ~/secrets
  openssl genrsa -out /tmp/throwaway.pem 2048 2>/dev/null
  ACCT=$1 python3 - <<'PYEOF'
import json, os
acct = os.environ["ACCT"]
info = {"type": "service_account", "project_id": "your-gcp-project",
        "private_key_id": "0000000000000000000000000000000000000000",
        "private_key": open("/tmp/throwaway.pem").read(),
        "client_email": f"{acct}@your-gcp-project.iam.gserviceaccount.com",
        "client_id": "000000000000000000000", "auth_uri": "https://accounts.google.com/o/oauth2/auth",
        "token_uri": "https://oauth2.googleapis.com/token"}
json.dump(info, open(os.path.expanduser(f"~/secrets/{acct}.json"), "w"), indent=2)
info["private_key"] = "<a throwaway RSA key generated at capture time for no account; not committed>"
json.dump(info, open(os.environ["OUT"] + f"/capture-only/placeholder-{acct}.json", "w"), indent=2)
PYEOF
  rm -f /tmp/throwaway.pem
}
capture_only_retag() {  # capture_only_retag <image> [base]: recording sandbox only (CAPTURE_CA set)
  # The sandbox's TLS is re-signed by its proxy (and plain http is refused). The image is rebuilt with
  # that proxy's CA (+ the CA env vars; for a base image also https Debian sources and the proxy itself,
  # so RUN steps can download) and re-tagged under the SAME name, so the tutorial's Dockerfile builds
  # unchanged. See ASSETS.md.
  [ -n "$CAPTURE_CA" ] || return 0
  local img=$1 kind=${2:-app} d user safe
  d=$(mktemp -d); cp "$CAPTURE_CA" "$d/capture-ca.crt"; chmod 644 "$d/capture-ca.crt"
  docker image inspect "$img" >/dev/null 2>&1 || docker pull -q "$img" >/dev/null 2>&1 \
    || { docker pull -q "mirror.gcr.io/library/$img" >/dev/null && docker tag "mirror.gcr.io/library/$img" "$img" && docker rmi -f "mirror.gcr.io/library/$img" >/dev/null; }
  user=$(docker image inspect -f '{{.Config.User}}' "$img")
  safe=$(echo "$img" | tr '/:' '__')
  {
    echo "# capture-only, NOT part of the tutorial: $img + the recording proxy's CA, re-tagged as $img"
    echo "FROM $img"
    echo "USER root"
    echo "COPY capture-ca.crt /usr/local/share/capture-ca.crt"
    echo "RUN for f in /etc/ssl/certs/ca-certificates.crt; do [ -f \$f ] && cat /usr/local/share/capture-ca.crt >> \$f; done; \\"
    echo "    for f in /etc/apt/sources.list.d/debian.sources /etc/apt/sources.list; do [ -f \$f ] && sed -i 's|http://deb.debian.org|https://deb.debian.org|g; s|http://security.debian.org|https://security.debian.org|g' \$f; done; true"
    echo "ENV SSL_CERT_FILE=/etc/ssl/certs/ca-certificates.crt REQUESTS_CA_BUNDLE=/etc/ssl/certs/ca-certificates.crt \\"
    echo "    PIP_CERT=/etc/ssl/certs/ca-certificates.crt NODE_EXTRA_CA_CERTS=/usr/local/share/capture-ca.crt UV_NATIVE_TLS=1 \\"
    echo "    CLOUDSDK_CORE_CUSTOM_CA_CERTS_FILE=/etc/ssl/certs/ca-certificates.crt"
    [ "$kind" = base ] && echo "ENV HTTPS_PROXY=$CAPTURE_RELAY https_proxy=$CAPTURE_RELAY NO_PROXY=localhost,127.0.0.1 no_proxy=localhost,127.0.0.1"
    [ -n "$user" ] && echo "USER $user"
  } > "$d/Dockerfile"
  mkdir -p "$OUT/capture-only"
  cp "$d/Dockerfile" "$OUT/capture-only/$safe.Dockerfile"
  step "capture-only/$safe-build" "docker build -q -t $img $d"
  rm -rf "$d"
}
CUE=/tmp/l22-cue-shell
CTRLC=$'\x03'
DEP=cheese-app-v3/src/deployment

case $SEG in
# ------------------------------------------------------------------------------------------------
pre)
  step p00-x-env "date -u '+%Y-%m-%d %H:%M UTC'; uname -sm; docker version --format 'Docker client {{.Client.Version}}, engine {{.Server.Version}}'; git --version; kind version; docker images"
  # the README has no clone command (the course's repos are cloned in its setup); the usual one
  step p01-clone "git clone https://github.com/dlops-io/cheese-app-v3.git"
  step p02-x-git-log "git -C cheese-app-v3 log -1 --format='%H %ci %s'; git -C cheese-app-v3 branch -r | sed 's|work/[a-z]*|work/‹staff›|'"
  step p03-x-ls-remote "git ls-remote https://github.com/dlops-io/cheese-app-v3.git | sed 's|refs/heads/work/[a-z]*|refs/heads/work/‹staff›|'"
  # README.md:236-259 (L20's service accounts): the deployment key goes into the secrets folder next to the repo
  step p04-mkdir-secrets "mkdir -p secrets"
  make_key deployment
  step p05-x-tree "ls -la; ls -la secrets; ls cheese-app-v3/src/deployment cheese-app-v3/src/deployment/deploy_k8s"
  capture_only_retag python:3.13-slim-bullseye base
  capture_only_retag python:3.13-slim-bookworm base
  ;;
# ------------------------------------------------------------------------------------------------
tb-commit)
  # README.md:404-406 "Start Deployment Docker Container": `cd deployment` (= src/deployment), then
  # `sh docker-shell.sh`. Before the first run, GCP_PROJECT in docker-shell.sh:13 is set to your
  # project (L20's README:266-267; the K8s section does not repeat it): here a placeholder.
  cd $DEP
  step b01-x-set-project "sed -i 's/\"ac215-project\" # Change/\"your-gcp-project\" # Change/' docker-shell.sh; grep -n 'GCP_PROJECT=' docker-shell.sh"
  istep b02-docker-shell "$(rl 406)"
  # extra: the two one-line fixes found on 2026-11-05 (L20 captures b02a/b02c), applied together
  step b02a-x-fix-dockerfile "sed -i 's/^FROM python:3.13-slim-bullseye/FROM python:3.13-slim-bookworm/; s/google-cloud-sdk google-cloud-sdk-gke-gcloud-auth-plugin/google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin/' Dockerfile; git diff Dockerfile"
  ;;
tb-shell)
  # README.md:406 again, with both fixes: builds; the shell stays open until $CUE exists (tb-close)
  cd $DEP
  rm -f $CUE
  PTY_TIMEOUT=10800 istep b03-docker-shell-fixed "$(rl 406)" "file:$CUE" "exit"
  ;;
tb-wait)
  for i in $(seq 1500); do
    docker exec $C sh -c 'for p in /proc/[0-9]*; do tr "\0" " " < $p/cmdline 2>/dev/null; echo; done' 2>/dev/null | grep -qx '/bin/bash ' && break
    sleep 2
  done
  sleep 3
  docker exec $C true && echo "toolbox shell is up"
  ;;
tb-close)
  touch $CUE
  ;;
# ------------------------------------------------------------------------------------------------
tb-readme)
  # README.md:407-413 "Check versions of tools" + "gcloud auth list"
  cstep b10-gcloud-version /app "$(rl 408)"
  cstep b11-kubectl-version /app "$(rl 409)"
  cstep b12-kubectl-version-client /app "$(rl 410)"
  cstep b13-gcloud-auth-list /app "$(rl 413)"
  cstep b14-x-tools /app "which -a kubectl; ls -la /usr/bin/kubectl; dpkg -S /usr/bin/kubectl; dpkg-query -W kubectl google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin; gke-gcloud-auth-plugin --version; helm version --short; pulumi version; uv --version; python --version; env | grep -E '^(GCP_|GOOGLE_|PULUMI_|USE_GKE)' | sort; ls -la /secrets; ls /app"
  # Warm-up "Create Simple Kubernetes Cluster Tutorial", README.md:539-542
  cstep b15-gke-create-test-cluster /app "$(readme 541 541)"
  # README.md:415-434 "Build and Push Docker Containers to GCR" (deploy_images), verbatim
  cstep b20-images-stack-init /app/deploy_images "$(readme 420 420)"
  cstep b21-images-config-set /app/deploy_images "$(readme 421 421)"
  cstep b22-images-preview /app/deploy_images "$(readme 428 428)"
  cstep b23-images-up /app/deploy_images "$(readme 433 433)"
  # README.md:436-455 "Create & Deploy Cluster" (deploy_k8s), verbatim
  cstep b30-k8s-stack-init /app/deploy_k8s "$(readme 440 440)"
  cstep b31-k8s-config-set-1 /app/deploy_k8s "$(readme 441 441)"
  cstep b31-k8s-config-set-2 /app/deploy_k8s "$(readme 442 442)"
  cstep b31-k8s-config-set-3 /app/deploy_k8s "$(readme 443 443)"
  cstep b32-k8s-preview /app/deploy_k8s "$(readme 449 449)"
  cstep b33-k8s-up /app/deploy_k8s "$(readme 454 454)"
  # README.md:476-486 "Try some kubectl commands", with no cluster yet (no kubeconfig in the toolbox)
  n=40
  for l in 478 479 480 484 485; do cstep "b$n-kubectl-noconfig-$l" /app "$(readme $l $l)"; n=$((n+1)); done
  # README.md:488-493 "If you want to shell into a container in a Pod"
  cstep b45-kubectl-get-pods-ns-noconfig /app "$(readme 490 490)"
  # README.md:509-512 "Delete Cluster" and the warm-up's README.md:578-581
  cstep b50-k8s-destroy /app/deploy_k8s "$(readme 511 511)"
  cstep b51-gke-delete-test-cluster /app "$(readme 580 580)"
  # extra (digest Step 8): what Pulumi's connect-k8s-command runs (create_cluster.py:192-199)
  cstep b52-x-get-credentials /app "gcloud container clusters get-credentials cheese-app-cluster --zone us-central1 --project your-gcp-project"
  ;;
# ------------------------------------------------------------------------------------------------
tb-local)
  # extras: Pulumi's local file backend (`pulumi login --local`) needs no cloud account, so the two
  # programs run up to their first call that needs Google (ASSETS.md)
  cstep c00-x-login-local /app "pulumi login --local"
  cstep c01-x-images-stack-init /app/deploy_images "$(readme 420 420)"
  cstep c02-x-images-config-set /app/deploy_images "$(readme 421 421)"
  cstep c03-x-images-preview /app/deploy_images "$(readme 428 428)"
  cstep c10-x-k8s-stack-init /app/deploy_k8s "$(readme 440 440)"
  cstep c11-x-k8s-config-set-1 /app/deploy_k8s "$(readme 441 441)"
  cstep c11-x-k8s-config-set-2 /app/deploy_k8s "$(readme 442 442)"
  cstep c11-x-k8s-config-set-3 /app/deploy_k8s "$(readme 443 443)"
  cstep c12-x-k8s-config /app/deploy_k8s "pulumi config; pulumi stack ls"
  cstep c13-x-k8s-preview /app/deploy_k8s "$(readme 449 449)"
  cstep c14-x-k8s-up /app/deploy_k8s "$(readme 454 454)"
  cstep c15-x-k8s-destroy /app/deploy_k8s "$(readme 511 511)"
  cstep c16-x-stacks /app "pulumi stack ls --all; ls ~/.pulumi/stacks/*; ls /app/pulumi-plugins"
  ;;
tb-local2)
  # capture-only stand-in, clearly labelled: c13 shows that deploy_k8s needs the image stack's outputs
  # (setup_containers.py:10-14, 70). Building the three images is L20's step (its b35b) and does not
  # fit the recording disk (the API image alone is ~5 GB), so a tiny Pulumi YAML program, under the
  # same project and stack name (organization/deploy-images/dev), exports the three `-tags` outputs
  # with PLACEHOLDER tags. deploy_k8s then runs unchanged and shows its real plan.
  mkdir -p "$OUT/capture-only"
  docker exec $C sh -c 'mkdir -p /tmp/standin-images && cd /tmp/standin-images && printf "%s\n" \
    "# capture-only stand-in for deploy_images outputs (placeholder tags, nothing is built)" \
    "name: deploy-images" "runtime: yaml" "outputs:" \
    "  cheese-app-api-service-tags: [\"us-docker.pkg.dev/your-gcp-project/cheese-app-repository/cheese-app-api-service:placeholder\"]" \
    "  cheese-app-frontend-react-tags: [\"us-docker.pkg.dev/your-gcp-project/cheese-app-repository/cheese-app-frontend-react:placeholder\"]" \
    "  cheese-app-vector-db-cli-tags: [\"us-docker.pkg.dev/your-gcp-project/cheese-app-repository/cheese-app-vector-db-cli:placeholder\"]" \
    > Pulumi.yaml'
  docker exec $C cat /tmp/standin-images/Pulumi.yaml > "$OUT/capture-only/standin-images-Pulumi.yaml"
  cstep capture-only/standin-images-up /tmp/standin-images "pulumi up --stack dev -y; pulumi stack output --stack dev"
  cstep c20-x-k8s-preview-with-tags /app/deploy_k8s "$(readme 449 449)"
  cstep c21-x-k8s-up-with-tags /app/deploy_k8s "$(readme 454 454)"
  cstep c22-x-k8s-after-up /app/deploy_k8s "pulumi stack --show-urns | head -40; pulumi stack output"
  cstep c23-x-k8s-destroy /app/deploy_k8s "$(readme 511 511)"
  ;;
# ------------------------------------------------------------------------------------------------
kind-up)
  # extra: the labelled stand-in for the README's `gcloud container clusters create test-cluster
  # --num-nodes 2` (README.md:541): kind, one control plane + two worker nodes, in the laptop's Docker
  step k00-x-kind-env "date -u '+%Y-%m-%d %H:%M UTC'; kind version; docker version --format 'Docker engine {{.Server.Version}}'"
  # The containerdConfigPatches are capture-only (ASSETS.md): the recording sandbox's kernel refuses a
  # negative oom_score_adj (runc's default for the pause container) and its nested cgroup v1 has no
  # systemd slices, so containerd clamps OOM scores and uses the cgroupfs driver. A laptop needs neither.
  cat > ~/kind-test-cluster.yaml <<'YAML'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
# capture-only (recording sandbox), see ASSETS.md:
containerdConfigPatches:
- |-
  [plugins."io.containerd.cri.v1.runtime"]
    restrict_oom_score_adj = true
  [plugins."io.containerd.cri.v1.runtime".containerd.runtimes.runc.options]
    SystemdCgroup = false
YAML
  docker image inspect kindest/node:v1.34.11 >/dev/null 2>&1 || docker pull -q kindest/node:v1.34.11 >/dev/null 2>&1 \
    || { docker pull -q mirror.gcr.io/kindest/node:v1.34.11 >/dev/null && docker tag mirror.gcr.io/kindest/node:v1.34.11 kindest/node:v1.34.11; }
  step k01-x-kind-create "cat kind-test-cluster.yaml; kind create cluster --name test-cluster --image kindest/node:v1.34.11 --config kind-test-cluster.yaml"
  # capture-only: the nodes' containerd trusts the recording proxy's CA (kind already passes the
  # proxy settings to the nodes); the toolbox joins kind's network and gets kind's kubeconfig, which
  # authenticates with a client certificate (GKE's uses gke-gcloud-auth-plugin instead)
  mkdir -p "$OUT/capture-only"
  {
    for n in $(kind get nodes --name test-cluster); do
      docker cp "$CAPTURE_CA" $n:/usr/local/share/ca-certificates/capture-ca.crt
      # + Google's Docker Hub mirror first (the sandbox's shared egress IP hits Docker Hub's 429 limit)
      docker exec $n sh -c 'mkdir -p /etc/containerd/certs.d/docker.io && printf "server = \"https://registry-1.docker.io\"\n\n[host.\"https://mirror.gcr.io\"]\n  capabilities = [\"pull\", \"resolve\"]\n" > /etc/containerd/certs.d/docker.io/hosts.toml'
      docker exec $n sh -c 'update-ca-certificates >/dev/null 2>&1; systemctl restart containerd' && echo "$n: CA + docker.io mirror added, containerd restarted"
    done
    docker network connect kind $C && echo "$C joined network kind"
    kind get kubeconfig --internal --name test-cluster | docker exec -i $C sh -c 'mkdir -p /root/.kube && cat > /root/.kube/config' && echo "kubeconfig written to $C:/root/.kube/config"
  } > "$OUT/capture-only/wiring.txt" 2>&1
  sleep 20
  ;;
# ------------------------------------------------------------------------------------------------
kind-readme)
  # The README's kubectl commands, typed at the toolbox prompt, against the stand-in
  cstep k02-kubectl-version /app "$(rl 409)"
  # README.md:551-561 (warm-up) = README.md:476-486 (main section): the same five commands
  n=3
  for l in 553 554 555 559 560; do cstep "k0$n-kubectl-$l" /app "$(readme $l $l)"; n=$((n+1)); done
  # README.md:563-566 "Deploy the App" (the YAML is in /app = src/deployment)
  cstep k10-kubectl-apply-tic-tac-toe /app "$(readme 565 565)"
  # README.md:568-571 "Get the Loadbalancer external IP", right away
  cstep k11-kubectl-get-services /app "$(readme 570 570)"
  cstep k12-x-rollout /app "kubectl rollout status deployment/web --timeout=300s; kubectl get pods -o wide"
  sleep 30
  cstep k13-kubectl-get-services-later /app "$(readme 570 570)"
  # README.md:488-493 "If you want to shell into a container in a Pod", verbatim
  cstep k20-kubectl-get-pods-ns /app "$(readme 490 490)"
  cstep k21-kubectl-get-pod-api /app "$(readme 491 491)"
  ctstep k22-kubectl-exec-api /app "$(readme 492 492)" "$(readme 492 492)"
  # README.md:618-657, the Kubernetes half of "Debugging Containers", every command verbatim
  n=30
  for l in 620 623 626 631 634 635 638 639 642 643 646 649 653; do cstep "k$n-debug-$l" /app "$(readme $l $l)"; n=$((n+1)); done
  ctstep k43-debug-656 /app "$(readme 656 656)" "$(readme 656 656)"
  ;;
kind-readme2)
  # re-run of k06/k07 alone: as recorded, a first kind-readme pass (before the NO_PROXY fix above) was
  # stopped late and its leftover process overwrote these two files (ASSETS.md, "Re-runs")
  cstep k06-kubectl-559 /app "$(readme 559 559)"
  cstep k07-kubectl-560 /app "$(readme 560 560)"
  ;;
# ------------------------------------------------------------------------------------------------
kind-extra)
  # extras (digest §3, Steps 8-12): what the README's objects do, on the stand-in
  cstep k50-x-get-deploy-rs-pods /app "kubectl get deployment,replicaset,pods,service,endpoints -o wide; kubectl get pods --show-labels"
  ctstep k51-x-exec-web /app "kubectl exec --stdin --tty deployment/web -- /bin/sh" "kubectl exec --stdin --tty deployment/web -- /bin/sh" \
    '[#$] $' 'hostname; ls; exit'
  cstep k52-x-dns /app "kubectl run dns-check --image=busybox:1.36 --restart=Never --rm -i --quiet -- sh -c 'nslookup web.default.svc.cluster.local | tail -3; wget -qO- http://web | head -5'"
  P=$(docker exec $C kubectl get pods -l run=web -o jsonpath='{.items[0].metadata.name}')
  cstep k53-x-delete-pod /app "kubectl delete pod $P; kubectl get pods -l run=web"
  sleep 15
  cstep k54-x-pods-after-delete /app "kubectl get pods -l run=web -o wide"
  cstep k55-x-scale /app "kubectl scale deployment web --replicas=4; kubectl rollout status deployment/web --timeout=180s; kubectl get pods -l run=web -o wide; kubectl get endpoints web"
  cstep k56-x-scale-back /app "kubectl scale deployment web --replicas=2; sleep 10; kubectl get pods -l run=web"
  cstep k57-x-port-forward /app "kubectl port-forward service/web 8080:80 >/tmp/pf.log 2>&1 & PF=\$!; sleep 4; curl -s -i http://localhost:8080/ | head -12; cat /tmp/pf.log; kill \$PF"
  # a run-to-completion Job (the loader pattern of setup_containers.py:199-243), and its debugging
  cstep k60-x-job-create /app "kubectl create job hello-job --image=busybox:1.36 -- sh -c 'echo loading...; sleep 5; echo done'; kubectl wait --for=condition=complete job/hello-job --timeout=180s; kubectl get jobs,pods"
  cstep k61-x-job-logs /app "kubectl logs job/hello-job"
  cstep k62-x-job-describe /app "kubectl describe job hello-job"
  cstep k63-x-namespaces /app "kubectl get namespaces; kubectl create namespace cheese-app-namespace; kubectl get pods --namespace=cheese-app-namespace; kubectl delete namespace cheese-app-namespace"
  cstep k64-x-events /app "kubectl get events --sort-by=.lastTimestamp | tail -15"
  cstep k65-x-kubeconfig /app "kubectl config get-contexts; kubectl config view --minify | grep -E 'server:|user:|client-certificate|exec' | sed -E 's/(client-(certificate|key)-data:).*/\1 <redacted>/'"
  ;;
# ------------------------------------------------------------------------------------------------
kind-down)
  # extra: the digest's tip (delete the Service first so a cloud LB goes too), then the stand-in
  cstep k80-x-kubectl-delete /app "kubectl delete -f deploy-k8s-tic-tac-toe.yml; kubectl delete job hello-job"
  step k81-x-kind-delete "kind delete cluster --name test-cluster; docker ps -a --format '{{.Names}}'"
  ;;
esac
