#!/bin/bash
# mkcopy.sh <name> <patch.py> <log>: copies the llm-rag work copy to <name> inside the volume l06ex-rag-work,
# applies <patch.py> (a Python script that edits <name>/cli.py and checks the lines it replaces), and logs the
# diff, as `git diff cli.py` would show it in a student's clone.
name=$1; patch=$2; log=$3
here=$(cd "$(dirname "$0")" && pwd)
docker run --rm -v l06ex-rag-work:/work -v "$here":/checks:ro -w /work python:3.12-slim-bookworm bash -c \
  "cp -a llm-rag $name && python3 /checks/$patch $name/cli.py && diff -u llm-rag/cli.py $name/cli.py" \
  | sed -e 's/Pavlos Protopapas/<instructor>/g' -e 's/[Pp]avlos/<instructor>/g' > "$log"
cat "$log"
