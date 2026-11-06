# Q1 / B1: what the v3 API answers for the path nginx hands it. FastAPI 0.120.4 and Starlette 0.49.3 (as
# pinned in src/api-service/uv.lock at 3ecef56) in python:3.13-slim-bookworm, network only for pip. The app is
# rootpath_app.py (the routing lines of api/service.py, see its header), called through Starlette's TestClient
# (no server). ROOT_PATH unset is how the v3 image runs on the Pulumi VM (setup_containers.py:219-225 sets no
# ROOT_PATH; docker-entrypoint.sh:19 passes no --root-path); ROOT_PATH=/api-service is the Kubernetes setting.
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
step "docker run --rm --network host -e HTTPS_PROXY=\$HTTPS_PROXY -e PIP_CERT=/ca.crt -e NO_PROXY=localhost,127.0.0.1 -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v $LOGS/rootpath_app.py:/app/rootpath_app.py:ro -w /app mirror.gcr.io/library/python:3.13-slim-bookworm sh -c '
pip install -q --root-user-action=ignore fastapi==0.120.4 starlette==0.49.3 httpx 2>&1 | grep -v notice
python - <<PY
import importlib, os
from fastapi.testclient import TestClient
for rp in [\"\", \"/api-service\"]:
    os.environ[\"ROOT_PATH\"] = rp
    import rootpath_app; importlib.reload(rootpath_app)
    c = TestClient(rootpath_app.app)
    for path in [\"/status\", \"/\", \"/api-service/status\"]:
        r = c.get(path)
        print(f\"ROOT_PATH={rp!r:15} GET {path:20} -> {r.status_code} {r.text}\")
PY'"
