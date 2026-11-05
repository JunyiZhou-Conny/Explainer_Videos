# Image checks (B1, B3, B4, C3-C7, C9): the tutorial's app image, built locally from tutorial/app at 46cc62f
# (image-local.Dockerfile; Docker Hub refused the public image's pull with 429 that day). Run from the host's
# Docker CLI; every container is disposable (--rm, or stopped by name at the end of its check).
# Host port 18086 stands in for the README's 8086, so the checks cannot collide with another program on 8086.
. "$(dirname "$0")/lib.sh"
I=l14ex/translation-demo:local
ready() { for i in $(seq 60); do docker logs "$1" 2>&1 | grep -q 'Booting worker' && return 0; sleep 0.5; done; return 1; }

echo '## image'
step "docker image inspect --format 'Os/Arch: {{.Os}}/{{.Architecture}}  User: {{.Config.User}}  Entrypoint: {{json .Config.Entrypoint}}  Cmd: {{json .Config.Cmd}}' $I"

echo '## B1: PORT=9090 with the pipe still at 8080, then the fix'
step "docker run -d --name l14ex-port --rm -e PORT=9090 -p 18086:8080 $I >/dev/null; echo started"
ready l14ex-port
step "curl -sS http://localhost:18086/"
step "docker logs l14ex-port 2>&1 | grep -E 'Starting|Listening'"
step "docker stop l14ex-port >/dev/null; echo stopped"
step "docker run -d --name l14ex-port --rm -e PORT=9090 -p 18086:9090 $I >/dev/null; echo started"
ready l14ex-port
step "curl -s http://localhost:18086/ | grep -o '<title>.*</title>'"
step "docker stop l14ex-port >/dev/null; echo stopped"

echo '## B3: the job argv, as a plan (no API call, no upload)'
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --src en --dest fr --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/"

echo '## B4: an override that leaves out --dest'
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-002/passage.txt --src en --output-uri gs://YOUR_OUTPUT_BUCKET/run-002/ | grep -E 'source_language|destination_language'"

echo '## C3: the four startup mistakes, side by side'
# (a) command python, no arguments: python reads its program from an empty stdin
step "docker run --rm --network none $I python; echo \"exit status: \$?\""
# (b) arguments, no command: the arguments replace CMD and the image has no ENTRYPOINT
step "docker run --rm --network none $I -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/; echo \"exit status: \$?\""
# (c) command python, all eleven values pasted into one argument
step "docker run --rm --network none $I python '-m translation_demo batch --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --src en --dest fr --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/'; echo \"exit status: \$?\""
# (d) neither: the image default, serve, is still running 15 s later
step "docker run -d --name l14ex-neither --network none $I >/dev/null; echo started"
ready l14ex-neither; sleep 15
step "docker inspect -f 'running after 15 s: {{.State.Running}}' l14ex-neither; docker logs l14ex-neither 2>&1 | grep -E 'Listening'"
step "docker stop l14ex-neither >/dev/null; docker rm l14ex-neither >/dev/null; echo removed"

echo '## C4: arguments the program refuses before any cloud call (exit 2)'
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --dest xx --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/ 2>&1 | tail -1"
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --dest xx --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/ >/dev/null 2>&1; echo \"exit status: \$?\""
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri gs://YOUR_INPUT_BUCKET/run-001/passage.txt --output-uri gs://YOUR_OUTPUT_BUCKET 2>&1 | tail -1"
step "docker run --rm --network none $I python -m translation_demo batch --plan --input-uri YOUR_INPUT_BUCKET/run-001/passage.txt --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/ 2>&1 | tail -1"
step "docker run --rm --network none $I sh -c 'python -c \"print(\\\"a\\\" * 5001)\" > /tmp/long.txt && python -m translation_demo batch --plan --text-file /tmp/long.txt --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/' 2>&1 | tail -1"
step "docker run --rm --network none $I python -m translation_demo batch --plan --text-file examples/passage.txt --output-uri gs://YOUR_OUTPUT_BUCKET/run-001/ | grep input_characters"

echo '## C5-C7, B5: the web app, offline (requests sent from inside the container with Python; no translation call)'
post() { # $1 container, $2 path, $3 json
  docker exec "$1" python -c "
import json, sys, urllib.request, urllib.error
req = urllib.request.Request('http://127.0.0.1:8080' + sys.argv[1], data=sys.argv[2].encode(), headers={'Content-Type': 'application/json'}, method='POST')
try:
    r = urllib.request.urlopen(req); body = r.read(); print(r.status, r.headers.get('Content-Type'), len(body), 'bytes')
except urllib.error.HTTPError as e:
    print(e.code, e.read().decode())
" "$2" "$3"
}
button() { docker exec "$1" python -c "
import re, urllib.request
html = urllib.request.urlopen('http://127.0.0.1:8080/').read().decode()
print(re.search(r'<button[^>]*speech-button[^>]*>[^<]*</button>', html).group(0))"; }
for flag in unset true True yes on; do
  if [ "$flag" = unset ]; then envs=""; else envs="-e ENABLE_SPEECH=$flag"; fi
  docker run -d --name l14ex-web --network none $envs $I >/dev/null; ready l14ex-web
  printf '$ ENABLE_SPEECH=%s: the page'"'"'s speech button\n' "$flag"; button l14ex-web 2>&1; printf '[exit %s]\n\n' $?
  docker stop l14ex-web >/dev/null; docker rm l14ex-web >/dev/null
done
docker run -d --name l14ex-web --network none -e ENABLE_SPEECH=true -e GOOGLE_CLOUD_LOCATION=us-central1 $I >/dev/null; ready l14ex-web
printf '$ ENABLE_SPEECH=true, GOOGLE_CLOUD_PROJECT not set: POST /api/speech {"text": "Bonjour à tous", "dest": "fr"}\n'
post l14ex-web /api/speech '{"text": "Bonjour à tous", "dest": "fr"}'; printf '[exit %s]\n\n' $?
docker stop l14ex-web >/dev/null; docker rm l14ex-web >/dev/null
docker run -d --name l14ex-web --network none -e ENABLE_SPEECH=true -e GOOGLE_CLOUD_PROJECT=your-project-id -e GOOGLE_CLOUD_LOCATION=us-central1 $I >/dev/null; ready l14ex-web
printf '$ all three variables, no identity: POST /api/speech {"text": "Bonjour à tous", "dest": "fr"}\n'
post l14ex-web /api/speech '{"text": "Bonjour à tous", "dest": "fr"}'; printf '[exit %s]\n\n' $?
LONG=$(python3 -c 'print("é" * 2001)')
printf '$ all three variables: POST /api/speech with 2,001 x "é" (4,002 UTF-8 bytes)\n'
post l14ex-web /api/speech "{\"text\": \"$LONG\", \"dest\": \"fr\"}"; printf '[exit %s]\n\n' $?
printf '$ all three variables: POST /api/speech {"text": "Bonjour", "dest": "xx"}\n'
post l14ex-web /api/speech '{"text": "Bonjour", "dest": "xx"}'; printf '[exit %s]\n\n' $?
docker stop l14ex-web >/dev/null; docker rm l14ex-web >/dev/null
step "docker ps -a --filter name=l14ex- --format '{{.Names}}' | wc -l"
