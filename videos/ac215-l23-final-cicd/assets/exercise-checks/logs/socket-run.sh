#!/bin/sh
# Host side. Q3, Ponder 1, B6: a container with only the Docker CLI and the host's socket mounted
# (docker-shell.sh:36 does the same for the toolbox) runs `docker build`. Where does the image land?
# The image is a two-line FROM scratch image tagged l23ex-sibling:check, removed at the end.
D="$(cd "$(dirname "$0")" && pwd)"; . "$D/lib.sh"
export CLI=mirror.gcr.io/library/docker:29-cli
step 'docker info -f "host engine: {{.Name}} {{.ID}}" | cut -c1-40; docker images -q l23ex-sibling:check | wc -l'
step 'docker run --rm -v /var/run/docker.sock:/var/run/docker.sock $CLI sh -c "
  ps -o comm | grep -c dockerd; docker info -f \"engine seen from inside: {{.Name}} {{.ID}}\" | cut -c1-50
  mkdir /ctx && cd /ctx && echo hello > hello.txt && printf \"FROM scratch\nCOPY hello.txt /\n\" > Dockerfile
  docker build -q -t l23ex-sibling:check . >/dev/null && echo built; docker images --format \"{{.Repository}}:{{.Tag}}\" l23ex-sibling
  docker ps --filter ancestor=$CLI --format \"running on that engine: {{.Image}} (this very container)\""'
step 'docker images --format "on the host: {{.Repository}}:{{.Tag}} {{.ID}}" l23ex-sibling:check'
step 'docker image rm l23ex-sibling:check >/dev/null && docker images -q l23ex-sibling:check | wc -l'

# B4: without set -e, a failed build leaves the tag on the image you built before, and docker run starts that one.
# l23ex-tb:latest is built once (label v=1), then a second build that fails at RUN false.
export T=$(mktemp -d)
step 'cd $T && printf "FROM $CLI\nLABEL v=1\n" > Dockerfile && docker build -q -t l23ex-tb:latest . >/dev/null && echo "first build: ok"
printf "FROM $CLI\nLABEL v=2\nRUN false\n" > Dockerfile && docker build -q -t l23ex-tb:latest . >/dev/null 2>&1; echo "second build exit status: $?"
docker run --rm l23ex-tb:latest true && docker image inspect -f "l23ex-tb:latest still carries label v={{index .Config.Labels \"v\"}}" l23ex-tb:latest'
docker image rm l23ex-tb:latest >/dev/null; rm -f "$T/Dockerfile"; rmdir "$T"
