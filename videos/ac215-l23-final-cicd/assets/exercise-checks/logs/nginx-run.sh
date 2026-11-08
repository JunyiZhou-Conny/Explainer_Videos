#!/bin/sh
# Host side. The repo's nginx.conf (src/deployment/nginx-conf/nginx/nginx.conf at 5950118, read-only),
# run the way deploy-setup-webserver.yml:23-35 runs it (nginx:stable, the conf as /etc/nginx/nginx.conf),
# on a private network l23ex-net, in front of two stand-ins reachable as `api-service` (:9000) and
# `frontend` (:3000) that answer with the path they received (as laptop/62). Requests come from a
# throwaway client container on the same network; no port is published on the host. Container names
# carry the prefix l23ex- (network aliases give them the names nginx.conf uses). In the logged
# commands, $CONF is the repo's file, $NOSLASH an edited copy (a temp file, deleted afterwards), $NG
# the nginx:stable image.
D="$(cd "$(dirname "$0")" && pwd)"; . "$D/lib.sh"
export CONF="$(cd "$D/../../source/src/deployment/nginx-conf/nginx" && pwd)/nginx.conf"
export NG=mirror.gcr.io/library/nginx:stable; PY=mirror.gcr.io/library/python:3.12-slim
export NOSLASH=$(mktemp)
standin() {  # name port
  docker run -d --name l23ex-$1 --network l23ex-net --network-alias $1 $PY python -c "
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        b = ('$1 received ' + self.path + '\n').encode()
        self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
http.server.HTTPServer(('', $2), H).serve_forever()" >/dev/null
}
docker network create l23ex-net >/dev/null
standin api-service 9000; standin frontend 3000; sleep 2
step 'docker run --rm --entrypoint nginx $NG -v'

# B3, Ponder 2: as committed (proxy_pass http://api-service:9000/;)
step 'sed -n "35,37p" $CONF | tr -d "\t"; docker run -d --name l23ex-nginx --network l23ex-net -v $CONF:/etc/nginx/nginx.conf:ro $NG >/dev/null && sleep 2'
step 'docker run --rm --network l23ex-net $NG sh -c "curl -s l23ex-nginx/api/newsletters; curl -s l23ex-nginx/; curl -s -o /dev/null -w \"HTTP %{http_code} -> %{redirect_url}\n\" l23ex-nginx/api"'
docker rm -f l23ex-nginx >/dev/null
# B3: the same file with the trailing slash removed from proxy_pass
sed 's|proxy_pass http://api-service:9000/;|proxy_pass http://api-service:9000;|' "$CONF" > "$NOSLASH"; chmod 644 "$NOSLASH"
step 'diff $CONF $NOSLASH | tr -d "\t"'
step 'docker run -d --name l23ex-nginx --network l23ex-net -v $NOSLASH:/etc/nginx/nginx.conf:ro $NG >/dev/null && sleep 2 && docker run --rm --network l23ex-net $NG sh -c "curl -s l23ex-nginx/api/newsletters; curl -s l23ex-nginx/api/chat/llm"'
docker rm -f l23ex-nginx >/dev/null; rm -f "$NOSLASH"
# C4: no running container answers to api-service when nginx starts (setup-containers failed, or the API crashed)
docker rm -f l23ex-api-service >/dev/null
step 'docker run --name l23ex-nginx --network l23ex-net -v $CONF:/etc/nginx/nginx.conf:ro $NG 2>&1 | grep -E "emerg"; echo "exit status: $(docker inspect -f "{{.State.ExitCode}}" l23ex-nginx)"'
docker rm -f l23ex-nginx l23ex-frontend >/dev/null; docker network rm l23ex-net >/dev/null
