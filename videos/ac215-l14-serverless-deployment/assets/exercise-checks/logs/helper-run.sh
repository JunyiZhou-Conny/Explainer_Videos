D="$(cd "$(dirname "$0")" && pwd)"
docker run --rm --network none -v "$D/../../source/tutorial":/repo/tutorial:ro -v "$D":/checks:ro \
  python:3.12-slim-bookworm bash /checks/helper.sh
