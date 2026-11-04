# Host wrapper for function.sh: a disposable container, the proxy and its CA for pip only.
D="$(cd "$(dirname "$0")" && pwd)"
SRC="$D/../../source/tutorial/function"
docker run --rm --network host -e HTTPS_PROXY="$HTTPS_PROXY" -e https_proxy="$HTTPS_PROXY" \
  -e PIP_CERT=/ca.crt -e SSL_CERT_FILE=/ca.crt -e PIP_DISABLE_PIP_VERSION_CHECK=1 -e PIP_ROOT_USER_ACTION=ignore \
  -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v "$SRC":/fn:ro -v "$D":/checks:ro \
  python:3.12-slim-bookworm bash /checks/function.sh
