#!/bin/sh
# Host side: shell-in.sh in ubuntu:24.04 (the captures' laptop OS; /bin/sh is dash), no network.
# The tutorial files are the unchanged copies in ../../source (5950118), mounted read-only.
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
docker run --rm --network none -v "$SRC":/src:ro -v "$D":/checks:ro mirror.gcr.io/library/ubuntu:24.04 \
  bash /checks/shell-in.sh
