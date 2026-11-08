#!/bin/sh
# Host side: ansible-in.sh in the check-only image l23ex-ansible:check (setup.sh), with no network.
# The tutorial files are the unchanged copies in ../../source (5950118), mounted read-only.
D="$(cd "$(dirname "$0")" && pwd)"; SRC="$D/../../source"
docker run --rm --network none -v "$SRC/src/deployment":/src:ro -v "$D":/checks:ro l23ex-ansible:check \
  bash /checks/ansible-in.sh
