#!/bin/bash
# crun.sh <venv> <log> <command...>: runs <command> in a throwaway python:3.12-slim-bookworm container with the
# venv /colab/<venv> (volume l06ex-colab) first on PATH, the notebooks' cells read-only on /cells (the copies in
# assets/source/colab/) and the checks' scripts on /checks. No network: no OpenAI call can happen.
venv=$1; log=$2; shift 2
here=$(cd "$(dirname "$0")" && pwd)
{ echo "\$ $*"
  docker run --rm --network none -v l06ex-colab:/colab -v "$here":/checks:ro -v "$here/../../source/colab":/cells:ro \
    -e PATH=/colab/$venv/bin:/usr/local/bin:/usr/bin:/bin -e PYTHONUNBUFFERED=1 -w /checks python:3.12-slim-bookworm \
    bash -c "{ $*"$'\n'"} 2>&1" 2>&1 </dev/null
  echo "[exit $?]"; } | sed -e 's/Pavlos Protopapas/<instructor>/g' -e 's/[Pp]avlos/<instructor>/g' > "$log"
tail -n 60 "$log"
