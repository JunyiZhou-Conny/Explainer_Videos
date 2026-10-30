#!/bin/sh
# hrun.sh <check.sh> <log>: run one check script in a throwaway container.
# The pristine work copy (volume l07ex-work, the repo at e25dfe9) is copied to /app (a tmpfs) first, so every
# check starts from a fresh clone with an empty outputs/; the venv (volume l07ex-venv) is mounted read-only.
# --network none: nothing can reach OpenAI. User 1000 (the image's `app` uid). The key is the README's placeholder.
set -e
HERE=$(cd "$(dirname "$0")" && pwd)
docker run --rm --network none -u 1000:1000 \
  --mount type=tmpfs,destination=/app,tmpfs-mode=1777 \
  -v l07ex-work:/work:ro -v l07ex-venv:/venv:ro -v "$HERE":/checks:ro \
  -e HOME=/tmp -e PATH=/venv/bin:/usr/local/bin:/usr/bin:/bin -e VIRTUAL_ENV=/venv \
  -e PYTHONDONTWRITEBYTECODE=1 -e OPENAI_API_KEY=YOUR_OPENAI_API_KEY \
  -w /app python:3.13-slim-bookworm \
  sh -c 'for f in /work/* /work/.[!.]*; do cp -a "$f" /app/ || exit 1; done; . /checks/lib.sh && . /checks/'"$1" > "$HERE/$2" 2>&1 || true
tail -n 3 "$HERE/$2"
