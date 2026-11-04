# Setup on the session machine (Docker Engine 29.8.2): pull the public image by tag, then by digest (B2).
. "$(dirname "$0")/lib.sh"
step 'date -u +%Y-%m-%dT%H:%MZ; docker version --format "client {{.Client.Version}} / engine {{.Server.Version}}"'
step "docker images --digests cgumb/ac215-translation-demo"
step "docker pull -q $IMAGE"
step "docker pull $DIGEST_REF"
step "docker images --digests cgumb/ac215-translation-demo"
step "docker image inspect --format '{{.Id}} {{.Os}}/{{.Architecture}} {{json .RepoDigests}}' $IMAGE"
