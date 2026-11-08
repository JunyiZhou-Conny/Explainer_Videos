#!/bin/sh
# Host side. Two pip questions, each in a fresh official Python image with network for pip only
# (session proxy + its CA): (1) on Python 3.8 (the toolbox's python3, laptop/32), what does pip pick for
# "ansible" unpinned, and for the pin Dockerfile:37 meant, "ansible>=9.0.0"? --dry-run: nothing is
# installed. (2) a newer ansible-core (2.17, Python 3.12) runs the provision playbook's lines 54-57.
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
. "$D/lib.sh"
P="--network host -e HTTPS_PROXY=$HTTPS_PROXY -e https_proxy=$HTTPS_PROXY -e PIP_CERT=/ca.crt -e SSL_CERT_FILE=/ca.crt
 -e PIP_DISABLE_PIP_VERSION_CHECK=1 -e PIP_ROOT_USER_ACTION=ignore -e PIP_NO_CACHE_DIR=1 -v /root/.ccr/ca-bundle.crt:/ca.crt:ro"
docker run --rm $P -v "$D":/checks:ro mirror.gcr.io/library/python:3.8-slim sh -c '. /checks/lib.sh
step "python --version"
step "pip install -q --dry-run --no-deps --ignore-installed --report - ansible | python -c \"import json,sys; print(\\\"ansible          ->\\\", [i[\\\"metadata\\\"][\\\"version\\\"] for i in json.load(sys.stdin)[\\\"install\\\"]])\""
step "pip install -q --dry-run --no-deps --ignore-installed \"ansible>=9.0.0\" 2>&1 | grep -oE \"9\\.0\\.1 Requires-Python [^;]*|8\\.7\\.0 Requires-Python [^;]*|ERROR: No matching distribution.*\""'
docker run --rm $P -v "$SRC/src/deployment":/src:ro -v "$D":/checks:ro mirror.gcr.io/library/python:3.12-slim sh -c '. /checks/lib.sh
pip install -q "ansible-core==2.17.*" >/dev/null 2>&1
step "python --version; ansible --version | head -1"
mkdir /w && cp /src/deploy-provision-instance.yml /w/ && python3 /checks/edit.py warnbook >/dev/null
step "cd /w && ansible-playbook warnbook.yml 2>&1 | grep -E \"TASK|changed:|ok:|fatal|Unsupported\""'
