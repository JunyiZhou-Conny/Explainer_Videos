# Sourced by every check script. step "<command>" runs it with bash and prints it the way
# assets/terminal/run_steps.sh does: "$ command", its output (stderr joined), "[exit N]".
# Where a command pipes into grep/tail/head, [exit N] is the last command's status.
# $SCRATCH (the session's scratch folder) holds the work copy: $W = a `git archive b8458ff` of
# dlops-io/cheese-app-ci-cd. Every container and image is named l21ex-... / l21ex/...
SCRATCH=${SCRATCH:?set SCRATCH to a scratch folder}
W=$SCRATCH/l21ex/work
IMG=cheese-app-api:b8458ff-l21ex
step() {
  printf '$ %s\n' "$1"
  bash -c "$1" 2>&1
  printf '[exit %s]\n\n' "$?"
}
# build <tag>: build the current folder's Dockerfile, unchanged, as setup.sh does (only the FROM
# image is swapped for the CA-patched base through a named build context; quiet output).
build() {
  docker build -q --network host --build-arg HTTPS_PROXY="$HTTPS_PROXY" --build-arg https_proxy="$HTTPS_PROXY" \
    --build-context python:3.11-slim-bookworm=docker-image://l21ex/py311-ca:check -t "$1" . >/dev/null
}
export -f build
