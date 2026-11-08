#!/bin/sh
# Builds the check-only image l23ex-ansible:check (ansible-check.Dockerfile) in a scratch build
# context holding only that file and the session proxy's CA. Run from the host.
D="$(cd "$(dirname "$0")" && pwd)"; . "$D/lib.sh"
CTX=$(mktemp -d); cp "$D/ansible-check.Dockerfile" "$CTX/Dockerfile"; cp /root/.ccr/ca-bundle.crt "$CTX/ca.crt"
step "docker build -q --network host --build-arg HTTPS_PROXY=\$HTTPS_PROXY --build-arg https_proxy=\$HTTPS_PROXY -t l23ex-ansible:check $CTX >/dev/null; echo \"build exit status: \$?\""
rm -f "$CTX/Dockerfile" "$CTX/ca.crt"; rmdir "$CTX"
step 'docker run --rm --network none l23ex-ansible:check sh -c "python --version; ansible --version | head -1; pip list 2>/dev/null | grep -iE \"^(ansible|ansible-core|boto3|botocore) \"; ansible-galaxy collection list 2>/dev/null | grep -E \"amazon.aws|community.aws|community.docker\"; ssh -V"'
