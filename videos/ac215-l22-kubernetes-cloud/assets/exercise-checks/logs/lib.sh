# Sourced by every check script. Each step prints itself the way assets/terminal/run_steps.sh does:
# "$ command", its output (stderr joined), "[exit N]".
#   step  "<cmd>"  runs on the session machine (the Docker CLI, kind, curl)
#   kstep "<cmd>"  runs inside the stand-in cluster's control-plane node container (kind), where
#                  kubectl v1.34.11 uses the cluster's admin kubeconfig; /work holds manifests/
NODE=${NODE:-l22ex-control-plane}
step() {
  printf '$ %s\n' "$1"
  bash -c "$1" 2>&1
  printf '[exit %s]\n\n' "$?"
}
kstep() {
  printf '$ %s\n' "$1"
  docker exec -w /work -e KUBECONFIG=/etc/kubernetes/admin.conf "$NODE" bash -c "$1" 2>&1
  printf '[exit %s]\n\n' "$?"
}
