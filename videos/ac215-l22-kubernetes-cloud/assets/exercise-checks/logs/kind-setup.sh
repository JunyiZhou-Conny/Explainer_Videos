#!/bin/bash
# The stand-in cluster for the exercise checks: kind v0.31.0 (node image kindest/node:v1.34.11, the
# version of the video's captures), cluster `l22ex`: 1 control plane + 2 workers, in the session
# machine's Docker engine. It is NOT GKE: no cloud load balancer, no node pool or autoscaler, no Workload
# Identity. Usage: KIND=<kind binary> bash kind-setup.sh up|info|down
# Capture-only wiring (as in assets/terminal/run_steps.sh, segment kind-up; not part of the tutorial):
# - the session reaches the internet only through an HTTPS proxy on the machine's loopback; a relay
#   (assets/terminal/proxy_relay.py, run as `python3 proxy_relay.py 0.0.0.0 38723 127.0.0.1 <proxy port>`)
#   makes it reachable from the kind network at 172.17.0.1:38723, and kind passes HTTPS_PROXY to the nodes;
# - each node's containerd trusts the proxy's CA and uses mirror.gcr.io for Docker Hub images (Docker
#   Hub's anonymous pull limit);
# - containerdConfigPatches: the sandbox kernel refuses a negative oom_score_adj and its cgroup v1 has
#   no systemd slices (see ASSETS.md "capture-only"); a laptop needs neither.
. "$(dirname "$0")/lib.sh"
KIND=${KIND:-kind}
CA=${CA_BUNDLE:-/root/.ccr/ca-bundle.crt}
RELAY=${RELAY:-http://172.17.0.1:38723}
case $1 in
up)
  echo '## up'
  cat > /tmp/l22ex-kind.yaml <<'YAML'
kind: Cluster
apiVersion: kind.x-k8s.io/v1alpha4
nodes:
- role: control-plane
- role: worker
- role: worker
# capture-only (recording sandbox), see the header:
containerdConfigPatches:
- |-
  [plugins."io.containerd.cri.v1.runtime"]
    restrict_oom_score_adj = true
  [plugins."io.containerd.cri.v1.runtime".containerd.runtimes.runc.options]
    SystemdCgroup = false
YAML
  step "date -u '+%Y-%m-%d %H:%M UTC'; $KIND version; docker version --format 'Docker engine {{.Server.Version}}'"
  step "HTTPS_PROXY=$RELAY https_proxy=$RELAY HTTP_PROXY= http_proxy= $KIND create cluster --name l22ex --image kindest/node:v1.34.11 --config /tmp/l22ex-kind.yaml 2>&1 | grep -E 'Creating|✓|Set kubectl'"
  rm -f /tmp/l22ex-kind.yaml
  for n in $($KIND get nodes --name l22ex); do
    docker cp "$CA" $n:/usr/local/share/ca-certificates/capture-ca.crt
    docker exec $n sh -c 'mkdir -p /etc/containerd/certs.d/docker.io && printf "server = \"https://registry-1.docker.io\"\n\n[host.\"https://mirror.gcr.io\"]\n  capabilities = [\"pull\", \"resolve\"]\n" > /etc/containerd/certs.d/docker.io/hosts.toml; update-ca-certificates >/dev/null 2>&1; systemctl restart containerd' && echo "(capture-only) $n: proxy CA + docker.io mirror, containerd restarted"
  done
  sleep 20
  docker exec "$NODE" mkdir -p /work
  kstep "kubectl get nodes"
  ;;
info)
  step "$KIND get clusters; docker ps --format '{{.Names}}  {{.Image}}' | grep l22ex"
  ;;
down)
  echo '## down'
  step "$KIND delete cluster --name l22ex; docker ps -a --format '{{.Names}}' | grep -c l22ex"
  ;;
esac
