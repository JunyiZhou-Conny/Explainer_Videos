#!/bin/bash
# arun.sh <log> <command...>: runs <command> as student in a throwaway container of the ADK check laptop
# (l06ex/adk-laptop, home = the volume l06ex-adk-home), in ~/AC215/llm-agent-google-adk, with UV_NO_SYNC=1
# (see adk-setup.sh) and the checks' scripts read-only on /checks. Network: none, unless NET=host (for npm or
# PyPI downloads; then the proxy variables are passed). The log holds "$ command", the output and "[exit N]";
# the instructor's name is masked as <instructor>, home paths are kept.
log=$1; shift
here=$(cd "$(dirname "$0")" && pwd)
net=${NET:-none}
px=(); [ "$net" = host ] && px=(-e HTTPS_PROXY=$HTTPS_PROXY -e https_proxy=$HTTPS_PROXY)
{ echo "\$ $*"
  docker run --rm --network "$net" "${px[@]}" -u student -e HOME=/home/student -e UV_NO_SYNC=1 -e PYTHONUNBUFFERED=1 \
    -v l06ex-adk-home:/home/student -v "$here":/checks:ro -w /home/student/AC215/llm-agent-google-adk \
    l06ex/adk-laptop bash -c "{ $*"$'\n'"} 2>&1" 2>&1 </dev/null
  echo "[exit $?]"; } | sed -e 's/Pavlos Protopapas/<instructor>/g' -e 's/[Pp]avlos/<instructor>/g' > "$log"
tail -n 40 "$log"
