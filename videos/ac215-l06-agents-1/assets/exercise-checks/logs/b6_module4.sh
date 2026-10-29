# b6_module4.sh: module 4 (FastAPI) from the root venv, as exercise B6 runs it, in a container without internet;
# the requests of 4-production-ready/README.md (plus /health and /docs). Run from the repo root.
cd 4-production-ready
uv run --project .. uvicorn app.main:app --port 8080 > /tmp/uvicorn.log 2>&1 &
for i in $(seq 1 60); do curl -s -o /dev/null http://localhost:8080/health && break; sleep 1; done
echo '$ curl -s http://localhost:8080/health'; curl -s http://localhost:8080/health; echo
echo '$ curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/docs'; curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/docs
echo '$ curl -s -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '"'"'{"user_message": "Hello!"}'"'"' -w "\n%{http_code}\n"'
curl -s -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"user_message": "Hello!"}' -w "\n%{http_code}\n"
echo '$ curl -s -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '"'"'{"message": "Hello!"}'"'"' -w "\n%{http_code}\n"'
curl -s -X POST http://localhost:8080/chat -H "Content-Type: application/json" -d '{"message": "Hello!"}' -w "\n%{http_code}\n"
kill %1; sleep 1
echo '--- server log (first lines, and the /chat error) ---'
grep -E 'Uvicorn running|POST /chat|Error:|Error$|app/(main|runner).py|response_text = |await runner' /tmp/uvicorn.log | cut -c1-220 | head -30
