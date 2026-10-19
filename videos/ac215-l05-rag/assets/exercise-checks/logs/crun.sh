#!/bin/bash
# crun.sh <app_dir> <log> <command> [docker run args via DARGS env]: runs <command> in a throwaway container of the
# tutorial's image (l05ex-cli), as user app in /app, with <app_dir> mounted on /app as docker-shell.sh +
# docker-compose.yml would (GCP_PROJECT=your-project-id, the key path set, an empty /secrets), /.venv activated
# as docker-entrypoint.sh:12 does. Network: none unless DNET is set (then that network). Log: "$ cmd", output, [exit N].
app=$1; log=$2; shift 2
net=${DNET:-none}
mkdir -p <checks>/secrets-empty
{ echo "\$ $*"
  docker run --rm --network "$net" $DARGS -v "$app":/app -v <checks>/secrets-empty:/secrets \
    -e GCP_PROJECT=your-project-id -e GOOGLE_APPLICATION_CREDENTIALS=/secrets/llm-service-account.json \
    --entrypoint bash l05ex-cli -c "source /.venv/bin/activate && { $*"$'\n'"} 2>&1" 2>&1 </dev/null
  echo "[exit $?]"; } > "$log"
tail -n 25 "$log"
