#!/bin/bash
# Checks with the tutorial's own image (built by setup.sh from the unchanged Dockerfile at
# b8458ff, tagged $IMG). Run on the session's Docker engine; the work copies live in $SCRATCH.
# Host ports 19000/19001 stand in for the runner's 9000, so nothing collides with other work.
. "$(dirname "$0")/lib.sh"
export W IMG SCRATCH HTTPS_PROXY
section() { printf '## %s\n' "$1"; }

section "B1: the lint job's two commands on b8458ff (ci.yml:61, :66), then on a Black-fixed copy"
step 'docker run --rm $IMG black --check --line-length 120 api/; echo "exit code: $?"'
step 'docker run --rm $IMG flake8 --max-line-length=120 --extend-ignore=E203,W503 api/; echo "exit code: $?"'
step 'rm -rf $SCRATCH/l21ex/fixed && cp -r $W $SCRATCH/l21ex/fixed && cd $SCRATCH/l21ex/fixed && chmod -R a+rwX src/api-service/api && docker run --rm -v "$(pwd)/src/api-service/api":/app/api $IMG black --line-length 120 api/'
step 'cd $SCRATCH/l21ex/fixed && diff -u $W/src/api-service/api/utils.py src/api-service/api/utils.py'
step 'cd $SCRATCH/l21ex/fixed && build cheese-app-api:fixed-l21ex && docker run --rm cheese-app-api:fixed-l21ex black --check --line-length 120 api/; echo "exit code: $?"'
step 'docker run --rm cheese-app-api:fixed-l21ex flake8 --max-line-length=120 --extend-ignore=E203,W503 api/; echo "exit code: $?"'
section "B1 (aside): README Part 7's mount over /app hides the entrypoint (digest G4)"
step 'cd $SCRATCH/l21ex/fixed && docker run --rm -v $(pwd)/src/api-service:/app $IMG black --line-length 120 api/; echo "exit code: $?"'

section "B3: the coverage step as written (ci.yml:94), a fresh workspace, coverage/ not there yet"
step 'rm -rf $SCRATCH/l21ex/ws1 && mkdir -p $SCRATCH/l21ex/ws1 && cd $SCRATCH/l21ex/ws1 && docker run --rm -v $(pwd)/coverage:/app/coverage $IMG pytest tests/unit/ --cov=api --cov-report=term --cov-report=xml --cov-report=html:coverage 2>&1 | grep -E "PermissionError|passed|failed|TOTAL"; echo "exit code: ${PIPESTATUS[0]}"'
step 'cd $SCRATCH/l21ex/ws1 && ls -ld coverage && find coverage -type f | wc -l && docker run --rm $IMG id'
section "B3: the fix: create the folder writable first, write XML and HTML into the mount"
step 'rm -rf $SCRATCH/l21ex/ws2 && mkdir -p $SCRATCH/l21ex/ws2 && cd $SCRATCH/l21ex/ws2 && mkdir -p coverage && chmod 777 coverage && docker run --rm -v $(pwd)/coverage:/app/coverage $IMG pytest tests/unit/ --cov=api --cov-report=term --cov-report=xml:coverage/coverage.xml --cov-report=html:coverage/html 2>&1 | sed -n "/coverage: platform/,/passed/p"; echo "exit code: ${PIPESTATUS[0]}"'
step 'cd $SCRATCH/l21ex/ws2 && ls coverage && ls coverage/html | head -5 && find coverage -type f | wc -l'

section "B4: a coverage bar: --cov-fail-under=50, unit tests only, then unit + integration"
step 'docker run --rm $IMG pytest tests/unit/ --cov=api --cov-report=term --cov-fail-under=50 2>&1 | grep -E "^(Name|api/|TOTAL)|Required test coverage|FAIL|passed"; echo "exit code: ${PIPESTATUS[0]}"'
step 'docker run --rm $IMG pytest tests/unit/ tests/integration/ --cov=api --cov-report=term-missing --cov-fail-under=50 2>&1 | grep -E "^(Name|api/|TOTAL)|Required test coverage|FAIL|passed"; echo "exit code: ${PIPESTATUS[0]}"'

section "B5: the readiness loop instead of sleep 10 (server on host port 19000)"
step 'docker rm -f l21ex-api-server >/dev/null 2>&1; docker run -d --name l21ex-api-server -p 19000:9000 -e DEV=1 $IMG >/dev/null && start=$(date +%s.%N) && for i in $(seq 1 30); do curl -sf http://localhost:19000/health && { echo; echo "ready on try $i after $(echo "$(date +%s.%N) - $start" | bc) s"; exit 0; }; sleep 1; done; docker logs l21ex-api-server; exit 1'
step 'docker rm -f l21ex-api-server'
section "B5: the same loop when the server never comes up (a container that only sleeps)"
step 'docker rm -f l21ex-api-server >/dev/null 2>&1; docker run -d --name l21ex-api-server -p 19001:9000 $IMG sleep 120 >/dev/null && start=$(date +%s) && for i in $(seq 1 30); do curl -sf http://localhost:19001/health && exit 0; sleep 1; done; echo "gave up after $(( $(date +%s) - start )) s"; docker logs l21ex-api-server; exit 1'
step 'docker rm -f l21ex-api-server'

section "C6: a syntax error in service.py; what each job would see"
step 'rm -rf $SCRATCH/l21ex/syntax && cp -r $W $SCRATCH/l21ex/syntax && cd $SCRATCH/l21ex/syntax && printf "\ndef oops(:\n    pass\n" >> src/api-service/api/service.py && tail -3 src/api-service/api/service.py && build cheese-app-api:syntax-l21ex && echo built'
step 'docker run --rm cheese-app-api:syntax-l21ex black --check --line-length 120 api/ 2>&1 | grep -vE "^(Container is running|Executing command)"; echo "exit code: ${PIPESTATUS[0]}"'
step 'docker run --rm cheese-app-api:syntax-l21ex pytest tests/unit/ -v --tb=short 2>&1 | tail -1; echo "exit code: ${PIPESTATUS[0]}"'
step 'docker run --rm cheese-app-api:syntax-l21ex pytest tests/integration/ -v --tb=short 2>&1 | grep -E "SyntaxError|Interrupted|error" | head -4; echo "exit code: ${PIPESTATUS[0]}"'
step 'docker rm -f l21ex-api-server >/dev/null 2>&1; docker run -d --name l21ex-api-server -p 19000:9000 -e DEV=1 cheese-app-api:syntax-l21ex >/dev/null && sleep 10 && curl -f http://localhost:19000/ || { echo "exit code: $?"; docker logs l21ex-api-server 2>&1 | grep -E "SyntaxError|Started reloader|Uvicorn running" ; }'
step 'docker rm -f l21ex-api-server'
