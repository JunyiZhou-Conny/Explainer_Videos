# nginx checks (B1, B2, B3, C6): nginx:stable with the repository's nginx.conf (unchanged, at 3ecef56)
# in front of two stand-ins named api-service (port 9000) and frontend (port 3000) on a Docker network,
# as on the manual VM. Host port 18080 stands in for the VM's port 80. Everything is disposable:
# containers are named l20ex-* (the stand-ins answer to the network aliases api-service and frontend, the
# names nginx.conf uses) on network l20ex-net, all removed at the end. The image's access.log is stdout. Run from the host's Docker CLI; $SRC is assets/source/ (read-only), $WORK a scratch folder.
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
SRC=$(cd "$LOGS/../../source" && pwd)
WORK=${WORK:?set WORK to an empty scratch folder}
export LOGS SRC WORK
py='python:3.13-slim-bookworm'
wait_up() { for i in $(seq 40); do curl -s -o /dev/null "http://localhost:18080/$1" && return 0; sleep 0.25; done; return 1; }

echo '## setup: network, two stand-ins, nginx with the repo nginx.conf'
step "docker network create l20ex-net >/dev/null && echo network l20ex-net"
step "docker run -d --name l20ex-api --network l20ex-net --network-alias api-service -v $LOGS/echo_stub.py:/stub.py:ro $py python /stub.py api-service 9000 >/dev/null && echo l20ex-api started, alias api-service"
step "docker run -d --name l20ex-frontend --network l20ex-net --network-alias frontend -v $LOGS/echo_stub.py:/stub.py:ro $py python /stub.py frontend 3000 >/dev/null && echo l20ex-frontend started, alias frontend"
sleep 2
step "docker run -d --name l20ex-nginx --network l20ex-net -p 18080:80 -v $SRC/src/deployment/nginx-conf/nginx/nginx.conf:/etc/nginx/nginx.conf:ro nginx:stable >/dev/null && echo nginx started"
wait_up ''

echo '## B1: what path does each container see?'
for p in / /status /api-service/ /api-service/status '/api-service/podcasts/?limit=3' /api-servicex/status; do
  step "curl -s http://localhost:18080$p"
done
step "curl -s -o /dev/null -w '%{http_code} -> %{redirect_url}\n' http://localhost:18080/api-service"

echo '## B1: the same, with the trailing slash of proxy_pass removed (line 37)'
step "sed -n 37p $SRC/src/deployment/nginx-conf/nginx/nginx.conf"
sed '37s#proxy_pass http://api-service:9000/;#proxy_pass http://api-service:9000;#' "$SRC/src/deployment/nginx-conf/nginx/nginx.conf" > "$WORK/nginx-noslash.conf"
step "diff $SRC/src/deployment/nginx-conf/nginx/nginx.conf \$WORK/nginx-noslash.conf"
step "docker rm -f l20ex-nginx >/dev/null; docker run -d --name l20ex-nginx --network l20ex-net -p 18080:80 -v $WORK/nginx-noslash.conf:/etc/nginx/nginx.conf:ro nginx:stable >/dev/null && echo nginx started with the variant"
wait_up ''
step "curl -s http://localhost:18080/api-service/status"
step "curl -s http://localhost:18080/api-service/"
step "docker rm -f l20ex-nginx >/dev/null; docker run -d --name l20ex-nginx --network l20ex-net -p 18080:80 -v $SRC/src/deployment/nginx-conf/nginx/nginx.conf:/etc/nginx/nginx.conf:ro nginx:stable >/dev/null && echo nginx started with the repo file again"
wait_up ''

echo '## B3: stop the frontend while nginx keeps running (no restart)'
step "docker stop l20ex-frontend >/dev/null && echo l20ex-frontend stopped"
step "curl -s -o /dev/null -w '/ -> %{http_code}\n' http://localhost:18080/"
step "curl -s http://localhost:18080/api-service/status"
echo '## B3 / C6: now restart nginx, as the opening of the video did'
step "docker restart l20ex-nginx >/dev/null; sleep 2; docker ps -a --filter name=l20ex-nginx --format '{{.Names}}  {{.Status}}'"
step "docker logs l20ex-nginx 2>&1 | grep emerg"
step "curl -s -o /dev/null -w '/api-service/status -> %{http_code}\n' http://localhost:18080/api-service/status"
step "docker start l20ex-frontend >/dev/null && docker start l20ex-nginx >/dev/null; sleep 2; docker ps --filter name=l20ex-nginx --format '{{.Names}}  {{.Status}}'"
step "curl -s -o /dev/null -w '/ -> %{http_code}\n' http://localhost:18080/"
echo '## C6: the API stand-in missing instead'
step "docker stop l20ex-api >/dev/null; docker restart l20ex-nginx >/dev/null; sleep 2; docker logs l20ex-nginx 2>&1 | grep emerg | tail -1"
step "docker start l20ex-api >/dev/null; docker start l20ex-nginx >/dev/null; sleep 2; curl -s http://localhost:18080/api-service/status"

echo '## B2: the README echo (README:156-213) vs a quoted heredoc with the same text'
sed -n 156,213p "$SRC/README.md" > "$WORK/echo-block.sh"
{ printf "cat > conf/nginx/nginx.conf <<'EOF'\n"; sed -n 156,213p "$SRC/README.md" | sed "1s/^echo '//" | sed '$d'; printf 'EOF\n'; } > "$WORK/heredoc-block.sh"
step "head -2 \$WORK/heredoc-block.sh; echo ...; tail -3 \$WORK/heredoc-block.sh"
step "docker run --rm --network none -v $WORK:/w debian:12 bash -c 'mkdir -p /e/conf/nginx /h/conf/nginx; cd /e && bash /w/echo-block.sh; cd /h && bash /w/heredoc-block.sh; cp /e/conf/nginx/nginx.conf /w/echo.conf; cp /h/conf/nginx/nginx.conf /w/heredoc.conf; wc -l /w/echo.conf /w/heredoc.conf'"
step "diff \$WORK/echo.conf \$WORK/heredoc.conf"
step "diff \$WORK/heredoc.conf $SRC/src/deployment/nginx-conf/nginx/nginx.conf && echo 'heredoc file = repo nginx.conf'"
step "sed -n 9,11p \$WORK/heredoc.conf"
step "for f in echo heredoc; do docker run --rm --network none -v $WORK/\$f.conf:/etc/nginx/nginx.conf:ro --add-host api-service:127.0.0.1 --add-host frontend:127.0.0.1 nginx:stable nginx -t 2>&1 | tail -1; done"
echo '## B2: one access-log line from each file'
for f in echo heredoc; do
  step "docker rm -f l20ex-nginx >/dev/null; docker run -d --name l20ex-nginx --network l20ex-net -p 18080:80 -v $WORK/$f.conf:/etc/nginx/nginx.conf:ro nginx:stable >/dev/null; sleep 2; curl -s -o /dev/null http://localhost:18080/api-service/status; sleep 1; docker logs l20ex-nginx 2>/dev/null | tail -1 | sed -E 's/[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+/<client ip>/g'"
done
echo '## cleanup'
step "docker rm -f l20ex-nginx l20ex-api l20ex-frontend >/dev/null; docker network rm l20ex-net >/dev/null; docker ps -a --filter name=l20ex- --format '{{.Names}}' | wc -l"
