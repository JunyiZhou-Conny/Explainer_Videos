# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

## `source/` — the tutorial's own files

Copied unchanged with `git show <commit>:<path>` (each file checked against its git blob hash), at
the repo's own relative paths, so that a code panel's `path · lines a–b` matches a viewer's clone.

- `source/mega-pipeline/`: [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline),
  branch **`flexible-workflow`**, commit `cc67f3b8fc471f4fe1afe73d03e89466bae7d485` (2026-09-18,
  "latest mega pipeline flexible flow"; still the branch head on 2026-10-14, `mega-laptop/03-x-branch.txt`):
  - `README.md` (Get the Code `:30-52`, Two ways to work `:67-76`, folder layout `:105-119`,
    Configure each `cli.py` `:123-134`, bucket prefixes `:150-158`, Service Account & Secrets
    `:169-203` with the `gcloud` commands `:191-199`, How to Run a Component `:207-226`, Quick
    Reference `:230-274`, GCS sample code `:280-317`, sample Dockerfile `:319-372`, Windows notes
    `:374-380`), `.gitignore`;
  - for each component `transcribe_audio/`, `generate_text/`, `synthesis_audio_en/`,
    `translate_text/`, `synthesis_audio/`: `README.md`, `Dockerfile`, `docker-shell.sh` (mode 755,
    as committed), `pyproject.toml`, `uv.lock`, `cli.py`, `.gitignore`; plus the bonus
    `synthesis_audio/cli_11.py`.
- `source/port_toy/`: [dlops-io/port_toy](https://github.com/dlops-io/port_toy), branch `main`,
  commit `d190c7122fc35cc1f7e15e467d2babdfc24b5c0c` (2026-09-20, "gateway: show the real host port
  in the diagram"): `README.md`, `.gitignore`, `docker-compose.yml`, `gateway/Dockerfile`,
  `gateway/gateway.py`, `gateway/index.html`, `processor/Dockerfile`, `processor/processor.py`.
- `source/mega-pipeline-main/`: the same repo's `main` (the L03 tutorial), commit
  `c6bbc9ba88984e1234b68ccf5cdf7c00f7e9accc` (2026-09-27), for the "what changed since L03" panels:
  `README.md` (L03 put the key inside each component, `:97`), `transcribe_audio/.gitignore` (ignores
  `docker-shell.sh`, `Dockerfile`, `pyproject.toml`, `uv.lock`, `:4-7` — why the branch switch
  silently replaces them, G1), `transcribe_audio/cli.py` (joins all `response.results`, which
  `flexible-workflow` does not, E6), `generate_text/pyproject.toml`.
- `source/mega-pipeline-pipenv-flexible-workflow/`: branch `pipenv-flexible-workflow`, commit
  `32fcdb7aa3ffb3eaf3d09bdde123a02a42f2be12` (2025-02-18), the source of the `dlops/mega-pipeline-*`
  images on Docker Hub that `./docker-shell.sh run` falls back to (E1):
  `transcribe_audio/Dockerfile` (`FROM python:3.8-slim-buster`, `pipenv sync`,
  `CMD ["-c", "pipenv shell"]`), `transcribe_audio/Pipfile`, `generate_text/Pipfile`
  (`google-generativeai`, not `google-genai`), `translate_text/Pipfile`.

Not copied: the repos' PNGs (`mega-pipeline-bucket.png` is a console screenshot, which the series
never shows; `mega-pipeline-flow.png` and `port_toy/browser-gateway-processor.png` are redrawn as
diagrams). Course material by the AC215 teaching staff (Harvard IACS), used for study with the
instructor's permission.

## `terminal/` — real terminal sessions

Captured on **2026-10-14, 00:29–00:40 UTC** by `terminal/capture.sh` (which starts a fresh "laptop"
per part) and `terminal/run_steps.sh` (which types the README's commands one by one). Each file starts
with the command (`$ ...`; multi-line commands keep the README's ` \` lines), then its output, then its
exit status (`[exit N]`); ANSI colour codes are removed. Every README command of both tutorials is run
in README order, exactly as written, unless the tables below say otherwise. Files with `x-` in their
name are **extras** (not README steps: checks, gotcha demos); scenes mark them `extra`.

| folder | what |
| --- | --- |
| `port-laptop/` | port_toy, the whole README (Steps 1–4, handy commands), plus extras (00–74) |
| `mega-laptop/` | mega-pipeline `flexible-workflow`: clone, `cli.py` edits, every `./docker-shell.sh` mode that can run here, for all five components, and the registry fallback |
| `mega-transcribe_audio/`, `mega-generate_text/`, `mega-synthesis_audio_en/`, `mega-translate_text/`, `mega-synthesis_audio/` | commands typed at each component container's prompt (`python cli.py …`) |
| `mega-l03-laptop/` | the README's other way in: switching an L03 clone to `flexible-workflow` |
| `gcloud-laptop/` | the README's `gcloud` commands on a laptop where gcloud has no account |
| `expected/` | README text for outputs that cannot be captured here or that the scenes compare with; first line of each says where it comes from |
| `capture-only/` | not tutorial material: the two base-image Dockerfiles the capture needs and their build logs, and per-folder timings (UTC time and duration of each step; for terminal sessions the seconds to Ctrl+C and to exit) |
| `capture.sh`, `run_steps.sh`, `tty_session.py`, `proxy_relay.py` | the scripts that made all of the above |

An earlier port_toy run (2026-10-13 20:12 UTC) was replaced by this one: there `curl` and
`docker compose` ran without a terminal (progress meters and plain Compose lines a student never sees)
and one browser stand-in raced the gateway's start. The rerun is the same command list with those
fixed and the README's handy commands added.

### `port-laptop/` — port_toy, the whole README, on "your laptop"

Captured **2026-10-14, 00:32–00:34 UTC** (`capture.sh port`). Laptop: a fresh, empty Docker Engine
29.8.2 (client and engine, API 1.56, linux/amd64), Docker Compose v5.6.0, buildx v0.37.2, git 2.54.0,
curl 8.22.0. Images: `python:3.14-slim` (Debian 13 "trixie", Python 3.14.8, digest `a2b82f3c…`),
processor curl 8.14.1. Every README command is typed exactly as written, in README order.

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date, Docker / Compose / buildx / git / curl versions |
| `01-hello-world.txt` | README.md:28-30 (Prerequisites) | `docker run hello-world`: pull, "Hello from Docker!" (terminal render) |
| `02-clone.txt`, `03-cd.txt` | README.md:81-85 | `git clone https://github.com/dlops-io/port_toy.git` (the README says "Clone or download" and links the repo; the clone command itself is not printed), `cd port_toy` |
| `04-ls.txt` | extra | the files of README.md:59-69, commit `d190c71` |
| `05-network-create.txt`, `06-network-ls.txt` | README.md:91-93 + extra | `docker network create toynet` → network id; `docker network ls` lists `toynet` |
| `07-build-processor.txt` (+ `.plain.txt`) | README.md:100 | first build, terminal view (`Building 7.5s (9/9)`); `.plain.txt` = its step-by-step log (apt installs curl) |
| `08-build-gateway.txt` (+ `.plain.txt`) | README.md:101 | `Building 0.3s`: `[2/4] RUN apt-get … curl` is `CACHED` — the two Dockerfiles are identical up to `COPY`, so the gateway reuses the processor's layer |
| `09-images.txt` | extra | `toy-gateway`, `toy-processor`, 198 MB each on disk (48.8 MB content) |
| `10-run-processor.txt`, `11-run-gateway.txt` | README.md:108-111, :119-125 | the container ids |
| `12-logs-processor.txt`, `13-logs-gateway.txt` | README.md:131-134 | `processor listening on port 9200 (internal only)`; `gateway listening on port 9100  →  open http://localhost:8090` (two spaces around `→`; the README's sample has one, E15) |
| `14-send.txt`, `15-send-again.txt` | README.md:145-157 (browser) | **browser stand-in** (see below): the JSON the page receives, `{"upper": "HELLO FROM THE LAPTOP", "listen_port": 9200, "sender_port": 55620, "gateway_out_port": 55620}`; the second send gets a new ephemeral port (55634) |
| `16-ps.txt`, `17-ps-short.txt` | README.md:197-207 + extra | `docker ps`: `127.0.0.1:8090->9100/tcp` for the gateway, empty PORTS for the processor; 17 is the same in the README's three columns (`--format 'table {{.Image}}\t{{.Ports}}\t{{.Names}}'`) |
| `18-x-all-addresses-taken.txt` … `21-x-ps-all-addresses.txt` | extra (README.md:236-242, cheat sheet :540-543, :550) | `-p 8090:9100` while 8090 is taken → `Bind for 127.0.0.1:8090 failed: port is already allocated`, exit 125 (the container is created anyway, 19 removes it); with 8091 the PORTS column shows `0.0.0.0:8091->9100/tcp` (all addresses) |
| `22-curl-8090.txt` | README.md:250-252 | `curl http://localhost:8090` in a terminal: the page's HTML (154 lines at 80 columns) |
| `23-curl-9200.txt` | README.md:258-260 | `curl: (7) Failed to connect to localhost:9200 after 0 ms: Could not connect to server`, exit 7 |
| `24-exec-processor.txt` | README.md:272-280 | `docker exec gateway curl http://processor:9200/health` → `ok`. Without `-t`, curl's progress meter shows (stderr), and `ok` (no newline) lands at the end of the meter's line, as on a real terminal |
| `25-exec-localhost.txt` | README.md:284-288 | the same with `localhost` → `curl: (7) Failed to connect to localhost port 9200`, exit 7 |
| `26-x-exec-localhost-9100.txt` | extra | inside the gateway, `localhost:9100` *is* the gateway (the page's first lines) |
| `27-x-processor-has-curl.txt` | extra (E14) | the processor image has curl 8.14.1 too (`processor/Dockerfile:2`), although README.md:294 implies it does not |
| `28-network-inspect.txt`, `29-x-dns.txt` | Handy commands README.md:576 + extra | `toynet` 172.19.0.0/16, processor .2, gateway .3; inside the gateway `/etc/resolv.conf` says `nameserver 127.0.0.11` (Docker's embedded DNS) and `getent hosts` resolves both names |
| `29b-exec-it-sh.txt` | Handy commands README.md:566 | `docker exec -it gateway sh`; typed `hostname`, `ls` (`Dockerfile gateway.py index.html`), `exit` |
| `30-rm-gateway.txt` … `35-ps-8095.txt` | README.md:339-355 (+ extras 33-35) | gateway re-run on host port 8095; the send works on 8095 (32, browser stand-in); `localhost:8090` now refused (33); the log banner still says `open http://localhost:8090` (34, E15); PORTS `127.0.0.1:8095->9100/tcp` (35) |
| `36-rm-processor.txt`, `37-run-processor-9300.txt` | README.md:369-378 | |
| `38-send-fails.txt` | README.md:380 "It should fail" | browser stand-in: `curl: (52) Empty reply from server`, exit 52. The gateway drops the connection without an answer, so the page (no `catch`, `index.html:95-100`) simply does not update (E16, G13) |
| `39-logs-gateway-refused.txt`, `40-logs-processor-9300.txt` | extra | why: the gateway's traceback ends in `ConnectionRefusedError: [Errno 111] Connection refused` (`gateway.py:34`); the processor listens on 9300 |
| `41-rm-gateway.txt` … `43-send-9300.txt` | README.md:388-402 | gateway with `PROCESSOR_PORT=9300` back on 8090; the send works, `listen_port` 9300 |
| `44-rm-both.txt`, `45-network-rm.txt`, `46-x-after-cleanup.txt` | README.md:415-418 + extra | both removed, `toynet` gone (only the exited hello-world container remains) |
| `47-compose-up.txt` | README.md:454-456, Ctrl+C :507 | `docker compose up` in a terminal: the build view (`port_toy-gateway`, `port_toy-processor` are new image names, built from cache), `[+] up 5/5` (2 images, network `toynet`, 2 containers), the two banners, the request lines of 49 and 51, then Ctrl+C: `Gracefully Stopping...`, both `exited with code 137`. Ctrl+C was pressed 3.9 s in; the command ended at 24.3 s (G12: Python as PID 1 ignores SIGTERM, Docker waits 10 s per container, gateway first, then processor) |
| `48-compose-ps.txt` | README.md:480 | `docker compose ps` (second terminal, while 47 runs) |
| `49-send-compose.txt` | README.md:460 | browser stand-in, works |
| `50-network-ls-compose.txt` | extra | Compose created `toynet` (the file names it, `docker-compose.yml:37-39`) |
| `51-compose-exec.txt` | README.md:481 | `docker compose exec gateway curl http://processor:9200/health` → `ok` without a progress meter: `compose exec` gives curl a terminal (the README writes `curl ...`; this is the full command of README.md:273) |
| `52-compose-ps-a-stopped.txt` | README.md:521-525 | after Ctrl+C: both `Exited (137)`, still listed |
| `53-compose-down.txt`, `54-compose-ps-a-after.txt` | README.md:511-515 | `[+] down 3/3`: 2 containers and the network removed; `ps -a` empty |
| `55-compose-up-d.txt`, `56-compose-ps-d.txt` | README.md:491-495 | `[+] up 3/3` in the background |
| `56b-compose-logs-f.txt`, `56c-x-send-while-logs.txt` | Handy commands README.md:572 | `docker compose logs -f gateway` follows the log; a send from a second terminal (56c) appears as a `POST` line; Ctrl+C ends it (exit 130) |
| `56d-compose-exec-sh.txt` | Handy commands README.md:573 | `docker compose exec gateway sh`; typed `hostname`, `echo $PROCESSOR_HOST $PROCESSOR_PORT` → `processor 9200`, `exit` |
| `57-x-edit-port.txt` … `60-compose-up-d-restored.txt` | README.md:487-495 ("repeat the port experiments") | the edit `127.0.0.1:8090:9100` → `8095` (git diff; made by a capture-only `sed`, a student uses an editor); `docker compose up -d` recreates only the gateway (`Container gateway Started 10.5s`, the processor stays `Running`); the send works on 8095 (59); then the file restored and `up -d` again |
| `61-x-edit-processor.txt`, `62-compose-up-d-build.txt` (+ `.plain.txt`, `.plain.2.txt`) | README.md:497-501 | a one-line edit of `processor.py` (copied into the image by `COPY . .`); `docker compose up -d --build` rebuilds both images (only the processor's `COPY` layer is new) and recreates only the processor; the gateway keeps `Running` |
| `63-x-compose-logs.txt` | extra | `docker compose logs`, both services |
| `64-compose-down-running.txt`, `65-compose-ps-a-empty.txt`, `66-x-images-remain.txt` | README.md:509-515 | `down` while the app runs in the background: `Removed 10.2s` each, 20.8 s in all (G12); "The built images remain": `port_toy-*` and `toy-*`, 198 MB each |
| `67-x-g11-by-hand.txt` … `69c-x-g11-cleanup.txt` | extra, gotcha G11 / Exercise 7 | Compose right after the by-hand steps: `WARN … a network with name toynet exists but was not created by compose. Set external: true to use an existing network`, then `Conflict. The container name "/processor" is already in use`, exit 1. With only the network left over (69b), Compose v5.6.0 **warns and uses it** (no error; the digest's open question Q5); `compose down` then leaves that network (69c removes it by hand) |
| `70-x-ex3-no-network.txt` … `74-x-ex3-cleanup.txt` | extra, Exercise 3 | processor started without `--network`: from the gateway `curl: (6) Could not resolve host: processor` (71); the send gets `Empty reply from server` (72); the gateway's log ends in `socket.gaierror: [Errno -2] Name or service not known` (73) |

#### How the port_toy captures differ from a student's laptop

- **The laptop.** A `docker:29.8.2-dind` container with its own network namespace stands in for
  Docker Desktop: `localhost` there is the laptop's (so `-p 127.0.0.1:8090:9100` and
  `curl http://localhost:8090` behave as on a Mac or PC), and the fixed names `gateway`/`processor`
  belong to nobody else. The terminal is Linux bash as user `student`, workspace `~/AC215`.
- **The browser** (README.md:147-149, :353, :380, :402, :460) is replaced by `curl` sending exactly
  the page's request (`index.html:95-99`: `POST /` with `{"text": …}`); these are the
  `$SEND` lines (`curl -sS -X POST http://localhost:8090 -H 'Content-Type: application/json' -d
  '{"text": "hello from the laptop"}' -w '\n'`). The JSON is what the page turns into its card:
  `upper` → "Processor's reply"; `gateway_out_port`, `listen_port`, `sender_port` → the three port
  lines (`index.html:107-111`, each label padded to 30 characters). A scene that draws the page
  fills it from these JSON values and tags it `illustration`; `expected/port_toy-page-ports.txt` is
  the README's own sample. Typed text in the page is "hello from my browser" by default
  (`index.html:32`); the captures send "hello from the laptop".
- **Terminal view vs plain.** Commands whose output depends on a terminal (`docker build`,
  `docker compose up/down/up -d`, `docker run hello-world`, `curl` on the laptop, `docker exec …
  curl`, the interactive shells) were run in a real 80×40 pseudo-terminal (`tty_session.py`,
  rendered with the `pyte` terminal emulator 0.8.2): the file is what the terminal shows at the end,
  wrapped at 80 columns. The others ran without a terminal (their output is the same).
  `NN-….plain.txt` is a build's step-by-step log, replayed with `docker buildx history logs`.
- **Base image and apt.** Builds here need the recording proxy's CA certificate and https apt
  sources. `capture-only/base-python-3.14-slim.Dockerfile` rebuilt `python:3.14-slim` *under the
  same name* inside the laptop (log: `capture-only/base-python-3.14-slim-build.txt`), so the
  tutorial's Dockerfiles build unchanged. Visible effects: the `FROM` digest in build logs
  (`dcc61fa5…`) is the rebuilt image's, not Docker Hub's (`a2b82f3c…`); apt's `Get:` lines say
  `https://deb.debian.org` (a student sees `http://`); no base-image download appears in the first
  build (a student's first build pulls `python:3.14-slim`, ~45 MB).
- **Proxy.** The laptop's engine, git and curl reach the internet through a capture-only relay
  (`proxy_relay.py`) to the recording machine's proxy; `~/.docker/config.json` "proxies" passes it to
  builds and containers (Docker Desktop: Settings › Resources › Proxies). `NO_PROXY` keeps
  `localhost` direct, so the port tests are unaffected.
- **Registry mirror.** The laptop's engine pulls Docker Hub images through `mirror.gcr.io`
  (`--registry-mirror`): on 2026-10-14 the recording machine's shared IP got Docker Hub's anonymous
  `429 Too Many Requests` for `docker run hello-world`. The pull lines are the same either way, and
  the hello-world digest (`5e230903…`) is Docker Hub's.
- **Waits.** Before each browser stand-in the capture waits until the container's log shows its
  `listening` line (a person clicks Send seconds later); without it a request can race the server's
  start and get an empty reply.
- **Ids, ports and times** (container ids, ephemeral ports 55620…, timestamps) change on every run.

### `mega-laptop/` — mega-pipeline `flexible-workflow`, on "your laptop"

Captured **2026-10-14, 00:34–00:40 UTC** (`capture.sh mega`), on a fresh laptop (same kind as
port_toy's: Docker Engine 29.8.2, buildx v0.37.2, git 2.54.0, user `student`, workspace `~/AC215`).
Inside the images: `python:3.14-slim-bookworm` (Debian 12, **Python 3.14.8**), pip 26.2.1 (already the
newest, `pip install --upgrade pip` changes nothing), **uv 0.13.0** from `pip install uv`, packages
installed by `uv sync` exactly as `uv.lock` pins them (e.g. google-cloud-speech 2.40.0,
google-cloud-storage 3.14.1, google-genai 2.23.0, google-cloud-texttospeech 2.37.0,
google-cloud-translate 3.27.0). There is **no service-account key** anywhere (no GCP account here):
`~/AC215/secrets/` exists but is empty. Numbering: 0x setup, 1x Task A, 3x B, 4x C, 5x D, 6x E,
7x the registry fallback.

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | date and versions |
| `01-clone.txt`, `02-cd.txt` | README.md:34-37 ("Starting fresh?") | `git clone --branch flexible-workflow …`, `cd mega-pipeline` |
| `03-x-branch.txt`, `04-x-ls.txt` | extra (checkpoint of README.md:45, :52) | `* flexible-workflow`, commit `cc67f3b` (the pinned one); the five folders; `transcribe_audio` holds `Dockerfile README.md cli.py docker-shell.sh pyproject.toml uv.lock` (+ `.gitignore`) |
| `05-x-modes.txt` | extra (E12) | all five `docker-shell.sh` are `-rwxr-xr-x` after the clone (git mode 100755) |
| `06-x-secrets-folder.txt` | extra (layout README.md:105-119) | `mkdir secrets` beside the repo: `mega-pipeline  secrets`, the folder empty (the key would go here) |
| `07-x-cli-values.txt` | extra (E2, E4) | the shipped values: `""` in transcribe / synthesis_audio_en / synthesis_audio; the instructor's `"ac215-project"`, `"mega-pipeline-bucket"`, `"pavlos-advanced"` in generate_text and translate_text |
| `10-a-x-ls-l.txt` | extra | `transcribe_audio/` before anything runs |
| `11-a-x-edit-cli.txt` | README.md:123-134, transcribe_audio/README.md:46-56 | `git diff cli.py`: the three values set to the **placeholders** `"your-project-id"`, `"your-team-bucket"`, `"group-01"` (README's example group) by a capture-only `sed`; a student types their own in an editor. The same edit for B, D, E: `30-b-…`, `50-d-…`, `60-e-…`; for C see 41 |
| `12-a-docker-shell.txt` (+ `.plain.txt`) | README.md:212, transcribe_audio/README.md:65 | `./docker-shell.sh` in a terminal: `Docker Username: dlops, Build Mode: dev-run`, the build (`Building 99.5s`: `[2/5]` (apt, pip, uv) 44.7 s, `[5/5] RUN uv sync` 1.6 s, export 52.9 s), `Run Docker container...`, `Using local image...`, then the container's prompt `app@0ceffb272288:/app$` where `python cli.py --help` was typed (identical to transcribe_audio/README.md:98-107) and `exit`. `.plain.txt` = the full build log (1,473 lines: apt installs 245 packages, 205 MB, for `build-essential ffmpeg`; ten harmless `update-alternatives: warning` lines; pip's "Running pip as the 'root' user" warning; `uv sync`: `Using CPython 3.14.8 interpreter at: /usr/local/bin/python3`, `Creating virtual environment at: /home/app/.venv`, `Installed 26 packages`) |
| `13-a-x-docker-ps.txt`, `14-a-x-mounts.txt` | extra (second terminal while 12 runs) | the container is named like the image (`--name $IMAGE_NAME`); its two bind mounts: `…/mega-pipeline/transcribe_audio -> /app`, `…/AC215/secrets -> /secrets` |
| `15-a-x-g9-second-shell.txt` (+ `.plain.txt`) | extra, gotcha G9 | `./docker-shell.sh` in a second terminal while the first container runs: it rebuilds (`COPY` and `uv sync` re-run, because the first container's `--download` had created `input_audios/` and `text_prompts/` in the build context), then `docker: Error response from daemon: Conflict. The container name "/mega-pipeline-transcribe-audio" is already in use`, exit 125 |
| `16-a-x-host-after.txt` | extra | back on the laptop: `input_audios/` and `text_prompts/` exist in the component folder (made by `--download` before it failed); `git status` shows only ` M cli.py` (empty folders, and both are ignored) |
| `17-a-dev.txt` (+ `.plain.txt`) | README.md:213 | `./docker-shell.sh dev`: `Build Mode: dev`, everything `CACHED`, no container |
| `18-a-run-local.txt` | README.md:214 | `./docker-shell.sh run` with the local image present: `Using local image...` (no registry), prompt, `exit` (E18) |
| `19-a-x-ls-l-script.txt`, `20-a-chmod.txt` | extra + README.md:220-224 | the script is already executable; `chmod +x docker-shell.sh` prints nothing (E12) |
| `21-a-x-images.txt` | extra | `mega-pipeline-transcribe-audio` 1.48 GB on disk (386 MB content) |
| `31-b-docker-shell.txt` (+ `.plain.txt`) | README.md:212 in `generate_text/` | `Building 52.6s`: a new apt layer (54 packages, 74.5 MB for `build-essential` only), `uv sync` installs 34 packages; prompt, `python cli.py --help` (identical to generate_text/README.md:114-123), `exit` |
| `40-c-docker-shell.txt` (+ `.plain.txt`) | README.md:212 in `synthesis_audio_en/` | `Building 8.2s`: `CACHED [2/5]` — the four non-transcribe Dockerfiles are identical up to that line, so B's apt layer is reused; at the prompt `python cli.py --help` → `AssertionError: Update group name` (cli.py **not edited yet**, G2), `exit` |
| `41-c-x-edit-cli.txt` | README.md:123-134 | the C edit, made on the laptop **while the container runs** (the bind mount shows it inside at once: `mega-synthesis_audio_en/02-help.txt`) |
| `51-d-docker-shell.txt`, `61-e-docker-shell.txt` (+ `.plain.txt`) | README.md:212 in `translate_text/`, `synthesis_audio/` | `Building 7.9s` each (apt layer cached); at the prompt even `python cli.py --help` fails with `DefaultCredentialsError: File /secrets/mega-pipeline.json was not found.` (the API client is built at import, G3) |
| `70-x-images.txt` | extra | the five local images: transcribe 1.48 GB, the others 821–836 MB |
| `71-x-rm-local-image.txt` | extra | `docker image rm mega-pipeline-transcribe-audio`: stands in for a teammate who never built it |
| `72-run-registry.txt` | README.md:214 ("falls back to DockerHub") | **E1/G7 for real**: `Local image not found, using image from registry...`, pull of `dlops/mega-pipeline-transcribe-audio:latest`, then pipenv: `Creating a Pipfile for this project...`, `Launching subshell in virtual environment...`, prompt `(app) root@36615ab6e34b:/app#`; typed: `python --version` → **Python 3.8.17**, `which python` → `/root/.local/share/virtualenvs/app-4PlAip0Q/bin/python`, `python cli.py --help` works (the old image's packages; Python 3.8's argparse says `optional arguments:`), `exit` |
| `73-x-host-after-registry.txt` | extra | side effect on the laptop: a new **`Pipfile` owned by root** in `transcribe_audio/` (the image runs as root, `/app` is your folder), `?? Pipfile` in `git status` |
| `74-x-registry-image.txt` | extra (E1) | the pulled image: created **2025-02-18**, `PYTHON_VERSION=3.8.17`, `GOOGLE_APPLICATION_CREDENTIALS=../secrets/mega-pipeline.json`, `cmd ["-c","pipenv shell"]`, `user ""` (root); 1.17 GB |
| `75-x-rm-local-image-b.txt`, `76-run-registry-b.txt`, `77-x-host-after-registry-b.txt` | README.md:214 in `generate_text/` | the same for B: Python 3.8.17, and `python cli.py --help` → `ImportError: cannot import name 'genai' from 'google' (unknown location)` (the 2025 image has `google-generativeai`, `source/mega-pipeline-pipenv-flexible-workflow/generate_text/Pipfile`); another root-owned `Pipfile`. The typed `exit` ran (session exit status 1 = the failed import's) but its echo is missing from the render: pipenv's relay closed first |
| `78-x-images-all.txt`, `79-x-git-status-all.txt` | extra | both `dlops/…` images (1.17 GB, 1.02 GB) beside the local ones; the clone after everything: five edited `cli.py`, two stray `Pipfile`s |

### `mega-<component>/` — typed at each container's prompt

While a component's `./docker-shell.sh` terminal was open (the files above), each command below ran
in that same container, as user `app` in `/app`, after sourcing the venv exactly as the image's `CMD`
does (`Dockerfile:44-46`), so that each gets its own file and exit status (`docker exec` from a
second terminal; the output is what the first terminal would show). Files keep README order.

| file | README step | what it shows |
| --- | --- | --- |
| `mega-transcribe_audio/01-help.txt` | transcribe_audio/README.md:98 | the help text, identical to the README's block (:98-107) |
| `…/02-x-whoami.txt` … `08-x-venv.txt` | extra | user `app` uid 1000; `which python` → `/home/app/.venv/bin/python`; Python 3.14.8; `$GOOGLE_APPLICATION_CREDENTIALS` = `/secrets/mega-pipeline.json`; `/secrets` empty; `/app` = the laptop's folder (the bind mount); `$VIRTUAL_ENV` `/home/app/.venv` lives outside `/app`, uv 0.13.0 |
| `…/09-download.txt` | README.md:237 | `Args: Namespace(download=True, …)`, `download`, then `google.auth.exceptions.DefaultCredentialsError: File /secrets/mega-pipeline.json was not found.` at `storage.Client()` (cli.py:39), exit 1. **Kept as instructive**: this is exactly what a missing or misplaced key looks like (G3) |
| `…/12-x-ls-after.txt` | extra | `input_audios/` and `text_prompts/group-01/` were created (empty) before the failure |
| `mega-generate_text/01-help.txt` | generate_text/README.md:114 | identical to the README's block (:114-123): the Gemini client is created at import (cli.py:25) but asks for credentials only on a request |
| `…/02-download.txt` | README.md:245 | `DefaultCredentialsError` at `storage.Client(project=gcp_project)` (cli.py:41). Kept: the key problem surfaces here for B |
| `…/03-generate.txt` | README.md:246 | `Args: …`, `generate`, **exit 0, nothing else**: with no downloaded prompts the loop has nothing to do and Gemini is never called. Kept: a silent "success" that did nothing |
| `…/05-gemini-model.txt` | generate_text/README.md:91-94 | `export GEMINI_MODEL=gemini-2.5-flash` then `python cli.py --generate`: the same silent no-op |
| `…/06-x-python-version.txt` | extra | Python 3.14.8; `text_prompts/group-01/` and `text_paragraphs/group-01/` exist, empty |
| `mega-synthesis_audio_en/01-x-help-unedited.txt` | extra, G2 | before the edit: `AssertionError: Update group name` (cli.py:19) |
| `…/02-help.txt` | synthesis_audio_en/README.md:98 | after the edit (41): the assert passes, and now `TextToSpeechLongAudioSynthesizeClient()` at import (cli.py:23) raises `DefaultCredentialsError`, so even `--help` fails without the key (G3) |
| `…/03-download.txt` | README.md:253 | the same import-time error |
| `mega-translate_text/01-help.txt`, `02-download.txt` | translate_text/README.md:113, README.md:262 | `translate.Client()` at import (cli.py:22) → `DefaultCredentialsError` |
| `mega-synthesis_audio/01-help.txt`, `02-download.txt` | synthesis_audio/README.md:98, README.md:270 | the same at cli.py:22 |
| `mega-synthesis_audio/04-x-cli11-help.txt` | extra, E10 | `python cli_11.py --help` → `FileNotFoundError: … 'secrets/11lab_api_key.txt'` (read at import, cli_11.py:33, relative to `/app`, not `/secrets`) |

Run but **not kept** (each printed the same `DefaultCredentialsError` as the `--download` just before
it, so they add nothing; their timings are in `capture-only/`): A `python cli.py --transcribe`
(README.md:238, at `speech.SpeechClient()`), A `--upload` (:239), B `--upload` (:247), C `--synthesis`
(:254), D `--translate`, `--upload` (:263-264), E `--synthesis` (:271). Scenes type these commands and
show no output panel (or say "the same error, for the same reason").

The `--help` text of C, D and E with a key in place: `expected/mega-<component>-help.txt` (the
component READMEs' blocks; they match the code's argparse strings on this branch).

### `mega-l03-laptop/` — "Already have the repo from the last tutorial?" (README.md:39-48)

Same laptop, a second workspace `~/AC215-l03` standing in for a student who did L03: L03's clone
(`git clone https://github.com/dlops-io/mega-pipeline.git`, branch `main` @ `c6bbc9b`) plus the files
an L03 student has (capture-only, listed here): `transcribe_audio/Dockerfile` and `pyproject.toml`
(the versions L03's capture wrote, `../ac215-l03-mega-pipeline/assets/terminal/files/`),
`generate_text/Dockerfile` (same source), one-line stand-ins for the two `uv.lock` files,
`group_name = "group-01"` in `transcribe_audio/cli.py`, and a **placeholder**
`transcribe_audio/secrets/mega-pipeline.json` where L03 put the key (79 bytes:
`{"placeholder": "stands in for the L03 key in this capture; not a credential"}`).

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-l03-clone.txt`, `01-x-l03-state.txt` | extra (L03's clone) | the L03 state: ` M transcribe_audio/cli.py`, untracked `generate_text/Dockerfile`, `generate_text/uv.lock`; ignored `transcribe_audio/{Dockerfile,pyproject.toml,uv.lock,secrets/mega-pipeline.json}`; L03's Dockerfile starts `FROM python:3.12-slim-bookworm` |
| `02-cd.txt`, `03-fetch.txt` | README.md:42-43 | `git fetch origin` prints nothing (the clone already has every branch) |
| `04-checkout.txt` | README.md:44 | **both** refusals at once: `Your local changes to the following files would be overwritten by checkout: transcribe_audio/cli.py` and `The following untracked working tree files would be overwritten by checkout: generate_text/Dockerfile generate_text/uv.lock`, `Aborting`, exit 1 |
| `05-stash.txt`, `06-checkout-after-stash.txt` | README.md:48 (`git stash`) | the README's fix clears the first refusal only; the untracked files still block (G1, E8) |
| `07-x-stash-u.txt`, `08-checkout-ok.txt`, `09-branch.txt` | extra (G1 fix) + README.md:44-45 | `git stash -u`; then `branch 'flexible-workflow' set up to track 'origin/flexible-workflow'. Switched to a new branch 'flexible-workflow'`; `git branch` → `* flexible-workflow` |
| `10-x-after.txt`, `11-x-dockerfile-replaced.txt` | extra (G1, G6) | the ignored L03 `Dockerfile` was **silently replaced** by the branch's (`FROM python:3.14-slim-bookworm`); `transcribe_audio/secrets/mega-pipeline.json` is still there (ignored, README.md:50 "stay put"); two stashes |
| `12-x-dev-old-key.txt` (+ `.plain.txt`) | README.md:213 | `./docker-shell.sh dev` in that folder (apt layer cached from the main run) |
| `13-x-key-in-image.txt` | extra (G6, E7) | `docker run --rm --entrypoint ls mega-pipeline-transcribe-audio -la /app /app/secrets`: the key file is **inside the image** (`COPY --chown=app:app . ./`, no `.dockerignore`); `prod` would push it |

### `gcloud-laptop/` — the README's `gcloud` commands (README.md:191-199)

Captured 2026-10-14 00:29–00:30 UTC (`capture.sh gcloud`). Each command in a fresh `debian:12`
container with **no network** (`--network none`: nothing can reach Google), the recording machine's
Google Cloud SDK **570.0.0** (core 2026.05.22, bundled Python 3.14.5) mounted read-only, and one empty
home folder kept between commands: gcloud installed, never logged in (no account, no credentials).

| file | README step | what it shows |
| --- | --- | --- |
| `00-env.txt` | extra | Debian 12, `gcloud --version` |
| `01-config-set-project.txt` | README.md:192, typed **exactly as written** | in an interactive bash (a terminal; prompt `student@laptop:~$`): `-bash: syntax error near unexpected token 'newline'` — `<your-project-id>` is a placeholder; bash reads `<` and `>` as redirections. Kept as instructive. (`-bash` because the terminal is a login shell; zsh, the macOS default, prints `zsh: parse error near '\n'`; exit status 2) |
| `02-config-set-project-filled.txt` | README.md:192, placeholder filled | `gcloud config set project your-project-id` → `Updated property [core/project].` (gcloud only stores the setting) |
| `03-services-enable.txt` | README.md:193-198 | `ERROR: (gcloud.services.enable) You do not currently have an active account selected. Please run: $ gcloud auth login …`, exit 1. Kept as instructive: what you see when Tutorial 0's `gcloud auth login` was skipped. With an account it enables the five APIs; the tutorial documents no output for that |
| `04-x-auth-list.txt`, `05-x-config-list.txt` | extra | `No credentialed accounts.`; the configuration with `project = your-project-id`. The two `[component_manager] disable_update_check` / `[core] disable_usage_reporting` lines come from the recording machine's SDK installation, not from a student's default; scenes leave them out |

### Differences from a student's laptop (mega-pipeline)

- **The laptop, proxy, registry mirror, terminal renders**: as for port_toy above. The bind mounts
  point into the dind container's filesystem, as Docker Desktop's point into the Mac's or PC's.
- **Base image.** `capture-only/base-python-3.14-slim-bookworm.Dockerfile` rebuilt
  `python:3.14-slim-bookworm` under the same name with the proxy CA, https apt sources and
  `SSL_CERT_FILE` / `REQUESTS_CA_BUNDLE` / `PIP_CERT` (log: `capture-only/base-python-3.14-slim-bookworm-build.txt`),
  so `Dockerfile` is the tutorial's, unchanged. Visible effects: `[1/5] FROM …@sha256:d86a6f29…` is the
  rebuilt image (the pulled `python:3.14-slim-bookworm` is `48b13b00…`); no base download in the first build; apt's `Get:`
  lines say `https://`; inside the containers `env` would show the three CA variables.
- **No key, no GCP.** Every Google call stops at `DefaultCredentialsError`; nothing reached a bucket or
  an API. The placeholder values `your-project-id` / `your-team-bucket` are not real resources.
- **In-container commands** ran through `docker exec` in the running container (see above), not typed
  at its prompt; only `python cli.py --help` and `exit` were typed in each session file. The prompt
  to draw is the session's, `app@<id>:/app$`.
- **The edits** to `cli.py` were made by `sed` (capture-only); `git diff` shows them.
- **Ownership and modes.** The laptop's user `student` and the image's `app` are both uid 1000, so the
  container can write to the mount as on Docker Desktop. Folders created from inside show
  `drwxrwsrwx` / setgid bits that come from the capture's umask and parent folder, not from the tutorial.
- **Registry images** were pulled through `mirror.gcr.io`; their digests (`30e5dbdd…` transcribe,
  `c1f1ccbe…` generate-text) are the ones Docker Hub's `dlops/…:latest` index had when the digest's
  registry metadata was read (2026-10-12, E1).
- **Versions move.** uv 0.13.0, Python 3.14.8, pip 26.2.1, the package versions and the Docker /
  Compose versions were current on 2026-10-14: narration says "at the time of recording".

## `expected/` — what the READMEs document (not captures)

Each file starts with a `#` line naming its source (repo, commit, file and lines); a command line is
marked `$`. Scenes tag these panels `expected` (`expected_tag`).

| file | source | used for |
| --- | --- | --- |
| `mega-transcribe_audio-help.txt`, `mega-generate_text-help.txt` | transcribe_audio/README.md:98-107, generate_text/README.md:114-123 | reference only: the real runs (`mega-transcribe_audio/01-help.txt`, `mega-generate_text/01-help.txt`) are identical |
| `mega-synthesis_audio_en-help.txt`, `mega-translate_text-help.txt`, `mega-synthesis_audio-help.txt` | synthesis_audio_en/README.md:99-107, translate_text/README.md:114-123, synthesis_audio/README.md:99-107 | C, D, E `python cli.py --help` **with the key in place** (here they fail at import). Their text matches the code's argparse strings on this branch |
| `port_toy-logs.txt` | port_toy README.md:139-140 | compare with `port-laptop/12-…`, `13-…`: the real banner has two spaces around `→` |
| `port_toy-page-ports.txt` | port_toy README.md:154-156 | the page's port card as the README shows it (example port 44456); the real numbers of a run are in `port-laptop/14-send.txt` |
| `port_toy-docker-ps.txt` | port_toy README.md:204-206 | compare with `port-laptop/17-ps-short.txt` (same three columns) |

## Illustrations (no capture is possible; schematic drawings tagged `illustration`)

| what | based on |
| --- | --- |
| GCP console, service account: IAM & Admin › Service accounts › Create (`mega-pipeline-sa`); roles Storage Admin (`roles/storage.admin`), Agent Platform User (`roles/aiplatform.user`; "Vertex AI User" finds nothing), Cloud Speech Client (`roles/speech.client`), Cloud Translation API User (`roles/cloudtranslate.user`); Keys › Add Key › Create new key › JSON | mega-pipeline README.md:175-183 (no screenshot, no logo, no key content, no real project id) |
| GCP console, APIs & Services › Library › search › Enable, for Cloud Storage, Vertex AI, Speech-to-Text, Cloud Translation, Text-to-Speech | README.md:187-189 |
| Your bucket and its prefixes `input_audios/`, `text_prompts/`, `text_paragraphs/`, `text_translated/`, `text_audios/`, `output_audios/`, `output_audios_pp/`, each with `<group_name>/` | README.md:150-158 (the repo's `mega-pipeline-bucket.png` is a console screenshot and is not used) |
| The key file going into `<your-workspace>/secrets/mega-pipeline.json` | README.md:105-119, :183; the real empty folder is `mega-laptop/06-x-secrets-folder.txt` |
| The port_toy page in a browser (text box, Send, "Processor's reply", the port card, the diagram) | `source/port_toy/gateway/index.html`; values from the run's JSON (`port-laptop/14-send.txt` etc.) |
| Docker Hub (`dlops/mega-pipeline-*`) for `run` and `prod` | docker-shell.sh:13, :62-66, :86-88; `mega-laptop/72-…`, `74-…` |

## Not captured, and how the video shows them

| README step | why | on screen |
| --- | --- | --- |
| Create the service account, grant roles, download the JSON key (mega README.md:175-183) | GCP console; needs a GCP account; the key is a credential | console illustration (above); never a key's content |
| Enable the APIs in the console (README.md:189) | GCP console | illustration |
| `gcloud services enable …` succeeding (README.md:193-198) | needs a logged-in account and a billed project | the command, typed exactly; `gcloud-laptop/03-services-enable.txt` shows the no-account error; no success panel (the tutorial documents none); narration: check with `gcloud services list --enabled` (digest A4, a check, not a README step) |
| Create the bucket and put an `input-*.mp3` in `input_audios/` | needs GCP; the README gives no command (E5) | bucket illustration; the README's sample upload code (README.md:301-317) as a code panel from `source/` |
| The Quick Reference commands doing their job (README.md:236-272; component READMEs "Testing your code") | need the key and paid Google APIs (Storage, Speech-to-Text, Vertex AI Gemini, Text-to-Speech, Translation) | the commands typed exactly; the real no-key outputs listed above where kept; for success nothing in the repo documents output (no Colab, no logs): no output panel, narration says what to look for (digest A7-A11) and to check the bucket in the console (illustration) |
| `./docker-shell.sh prod` (README.md:215; component READMEs "Publish the container") | needs `docker login` to Docker Hub and push rights to `dlops` (or your own org); would publish an image; the arm64 half needs emulation | the command and the script lines it runs (`source/mega-pipeline/transcribe_audio/docker-shell.sh:51-68`); nothing documents its output |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>` (transcribe_audio/README.md:129 and the same block in the other component READMEs) | credentials | command only, placeholders as written |
| `winpty …` / Git BASH (README.md:226, :374-380) | Windows only | text only |
| `git checkout -- .` (README.md:48, the alternative to `git stash`) | the capture took the `git stash` branch of that sentence | command only |
| `uv add <package>` (component READMEs, e.g. transcribe_audio/README.md:89) | a placeholder, no package named | command only (L03's video captured `uv add`) |
| ElevenLabs: `11lab_api_key.txt` in `secrets/` (synthesis_audio/README.md, "OPTIONAL") | needs an ElevenLabs API key | `mega-synthesis_audio/04-x-cli11-help.txt` shows what happens without it |
| Docker Desktop's own UI | not needed: every port_toy step ran on the stand-in laptop | — |

## Re-running

```bash
cd videos/ac215-l04-flexible-workflow-ports
export CA_BUNDLE=/root/.ccr/ca-bundle.crt   # only behind the recording proxy (with HTTPS_PROXY set)
export PYTHON=<a python with pyte>          # pip install pyte; renders the terminal views
bash assets/terminal/capture.sh port        # ~3 min
bash assets/terminal/capture.sh mega        # ~7 min; the laptop's volume grows to ~8 GB, removed at the end
bash assets/terminal/capture.sh gcloud      # uses the recording machine's gcloud installation, no network
```

Each part empties its own folders first and removes its laptop at the end; the relay container
`l04-relay` stays until removed by hand. Ids, ephemeral ports, timestamps, build times and the newest
package versions change on every run. `mega` deletes the seven redundant failure captures listed above
after running them.
