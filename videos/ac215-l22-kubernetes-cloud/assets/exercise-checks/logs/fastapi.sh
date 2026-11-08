#!/bin/bash
# Q4 / B8: what the v3 API answers for the path the Ingress hands it. FastAPI 0.120.4 and Starlette 0.49.3
# (as pinned in src/api-service/uv.lock at 3ecef56) in python:3.13-slim-bookworm, network only for pip.
# The app is rootpath_app.py (the routing lines of api/service.py), called through Starlette's TestClient
# (no server). ROOT_PATH=/api-service is what the Kubernetes Deployment sets (setup_containers.py:309-312).
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
step "docker run --rm --network host -e HTTPS_PROXY=\$HTTPS_PROXY -e PIP_CERT=/ca.crt -e NO_PROXY=localhost,127.0.0.1 -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v $LOGS/rootpath_app.py:/app/rootpath_app.py:ro -w /app mirror.gcr.io/library/python:3.13-slim-bookworm sh -c '
pip install -q --root-user-action=ignore fastapi==0.120.4 starlette==0.49.3 httpx 2>&1 | grep -v notice
python - <<PY
import importlib, os
from fastapi.testclient import TestClient
for rp in [\"/api-service\", \"\"]:
    os.environ[\"ROOT_PATH\"] = rp
    import rootpath_app; importlib.reload(rootpath_app)
    c = TestClient(rootpath_app.app)
    for path in [\"/api-service/status\", \"/api-service/\", \"/api-service\", \"/api-servicex/status\", \"/status\"]:
        r = c.get(path, follow_redirects=False)
        print(f\"ROOT_PATH={rp!r:15} GET {path:20} -> {r.status_code} {r.text}\")
PY'"
