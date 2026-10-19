# web.sh: helpers for the adk web checks (sourced). start_web <log>: `uv run adk web` in the background from the
# repo root, waits for Uvicorn; stop_web: Ctrl+C equivalent (SIGINT to that process).
start_web() { uv run adk web > "$1" 2>&1 & WEB=$!; for i in $(seq 1 90); do grep -q 'Uvicorn running' "$1" && return 0; sleep 1; done; echo "adk web did not start"; cat "$1"; }
stop_web() { kill -INT $WEB; wait $WEB 2>/dev/null; }
tree() { curl -s http://localhost:8000/dev/apps/$1/build_graph | uv run python -c "import json, sys; r = json.load(sys.stdin)['root_agent']; print(r['name'], '|', r.get('model') or ''); [print('  ', a['name'], '| model', a['model']) for a in r.get('sub_agents', [])]"; }
