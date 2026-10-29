# c_module_env.sh: which .env does adk web load for baseline, and which model does the agent tree show? First
# with only the root .env, then after the module README's Setup step `cp .env.example .env` inside baseline/.
source /checks/web.sh
echo '== root .env only'
start_web /tmp/web1.log
tree baseline
echo '$ curl -s http://localhost:8000/apps/baseline/users/student/sessions   # sessions from before this restart'
curl -s http://localhost:8000/apps/baseline/users/student/sessions | uv run python -c "import json,sys; print([s['id'][:8] for s in json.load(sys.stdin)])"
stop_web; grep -E 'Loaded .env' /tmp/web1.log | cut -c1-200
echo '== after: cd baseline && cp .env.example .env && cd ..'
cd baseline && cp .env.example .env && cd ..
grep -v '^#' baseline/.env | grep .
start_web /tmp/web2.log
tree baseline
stop_web; grep -E 'Loaded .env' /tmp/web2.log | cut -c1-200
rm baseline/.env
