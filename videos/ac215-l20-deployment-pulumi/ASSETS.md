# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** L20 deploys to Google Cloud, and the
recording sandbox has **no GCP project, no Google account, no Docker Hub login and no credentials**.
Everything that runs on a machine you own is captured live, on **2026-11-05**: the whole manual
deployment (Part A) on a fresh Debian 12 machine standing in for the VM, from `get-docker.sh` to
nginx answering on port 80 with the frontend and the API behind it; `docker-hub.sh` building the
production frontend up to Docker Hub's push refusal; the deployment toolbox (`sh docker-shell.sh`)
built and started; every tool check, `ssh-keygen`, every gcloud and Pulumi command of the README.
Every command that needs Google stops at its **honest first error** ("You do not currently have an
active account selected", "PULUMI_ACCESS_TOKEN must be set …", `invalid_grant: account not found`,
`403 Forbidden` on the Artifact Registry push). Console steps are `illustration`s; the only
`expected` output is the README's own OS Login snippet. No output was invented.

**Two real breakages found on the recording day** (the video states both kindly, with the fix):

1. **`sh docker-shell.sh` does not build as committed** (`laptop/b02`). `src/deployment/Dockerfile:4`
   is `FROM python:3.13-slim-bullseye`; Debian 11's security updates moved to `archive.debian.org`
   after its LTS ended (the `bullseye-security` index on deb.debian.org, dated 2026-09-12, still
   lists packages its pool no longer has: `404 Not Found` for curl, gnupg, openssh-client …, while
   archive.debian.org serves them). The build stops at `Dockerfile:11` (`apt-get install … curl …`),
   and the script then runs `docker run` anyway: `Unable to find image 'cheese-app-deployment:latest'
   locally` → `pull access denied`. **Fix 1**: `FROM python:3.13-slim-bookworm` (`b02a`).
2. **Then the gcloud packages are gone** (`laptop/b02b`): Google's apt repository no longer has the
   transitional `google-cloud-sdk` / `google-cloud-sdk-gke-gcloud-auth-plugin` packages
   (`Package google-cloud-sdk is not available … However the following packages replace it:
   google-cloud-cli`; `E: Package 'google-cloud-sdk' has no installation candidate`), at
   `Dockerfile:29-30`. This would fail on bullseye too, once the first problem is fixed another way.
   **Fix 2**: `google-cloud-cli google-cloud-cli-gke-gcloud-auth-plugin` (`b02c`). With both fixes
   the toolbox builds in 92 s (`b02d`) and everything after it was captured in it.

The video's Part B therefore shows: the committed command failing (b02), the two one-line edits,
and the working toolbox. The `git diff` in `b02c` is the exact change a student makes.

## Which commit

**Pinned: `main` @ `3ecef56fea879ac480d260c0906cd95baf05179a`** (2025-11-28 16:00:06 −0500, "v4->v3").

- The course site links the repo's default branch, unpinned (`#deployment-to-gcp-manual`,
  `#deployment-to-gcp-single-vm-instance`). On 2026-11-05 `git ls-remote` (`laptop/p03`) still gave
  `HEAD` = `main` = `3ecef56`; the laptop's fresh clone is at that commit (`laptop/p02`).
- **Context only, not followed:** the unmerged staff branch `work/‹staff›` (name masked in the
  captures; it names a staff member) moved again on the recording day: digest pin `976c4bb`
  (2026-11-01, "added deploy_vm") → **`d1e860d` (2026-11-05 17:19 −0500, "Refactor for kind")**,
  which rewrites `README.md` (447 insertions, 528 deletions against `3ecef56`) and replaces
  `deploy_single_vm/` with `deploy_vm/` + `k8s/`. If it is merged into `main`, Part B of this video
  no longer matches the README; re-check `git ls-remote` before publishing. Other branches:
  `cluster-updates` `e55178c`, `pipenv` `0012c9a` (the Ansible version; its `inventory.yml`, which
  README.md:318-322 still mentions, holds a real IP and is not copied).

## `source/` — the tutorial's own files

From [dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) at `3ecef56`, copied unchanged
with `git show 3ecef56:<path>` at the repo's relative paths (executable bits as committed). Course
material by the AC215 teaching staff (Harvard IACS), used for study with the instructor's permission.
Not copied: images, `deploy_k8s/` (L22), the k8s demo YAMLs, `frontend-simple/`, the vector-db books.

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the two sections: Manual 4-222 (local checks 10-16, Docker Hub 18-35, VM 37-51, folders 53-68, secret 70-75, network 78-81, vector-db 83-98, loader 100-113, api-service 115-128 + interactive 131-145, frontend 147-151, nginx.conf 153-214 (the quoting bug: single quotes at 165-167 inside the `echo '…'`), nginx 216-220, URL 222); Single VM 225-383 (APIs 229-234, service accounts 236-259, toolbox 261-280, OS Login 283-291, ssh-keygen 294-298, key upload + snippet 300-316, "Deployment Setup"/inventory.yml 318-322, images 327-345, VM 347-367, URL + VM commands 369-383); destroy 387-390 |
| `src/deployment/Dockerfile` | the toolbox: `FROM python:3.13-slim-bullseye` (4, breakage 1), apt 11-12, gcloud repo 15-18, Docker repo 21-26, `google-cloud-sdk …` (29-30, breakage 2), kubectl 1.34 (33-41), helm 44, pulumi 47-48, `PULUMI_CONFIG_PASSPHRASE=""` (51), uv 54-55, user app 58-61, `uv sync --frozen` 70, entrypoint 73 |
| `src/deployment/docker-shell.sh` | env (9-17: secrets three levels up, `GCP_PROJECT` 13, `PULUMI_BUCKET` 17), attach-if-running (23-25), build `--platform=linux/amd64` (31), `docker run` mounts (34-50) |
| `src/deployment/docker-entrypoint.sh` | banner 3-7, `activate-service-account` 10, project 11, `configure-docker` 13, bucket check/create 15-20, `pulumi login` 23, stack listing 26-27, `/bin/bash` 30 |
| `src/deployment/docker_config.json` | `credHelpers` for `gcr.io` and `us-docker.pkg.dev` (1-5) |
| `src/deployment/pyproject.toml`, `uv.lock`, `.python-version`, `.gitignore`, `.docker-tag`, `README.md` | the toolbox's Python deps (pulumi ≥3.204, pulumi-gcp ≥9.3.0, -command ≥1.1.3, -docker ≥4.9.0, -docker-build ≥0.0.15, -kubernetes ≥4.23.0); `.gitignore` ignores `/pulumi-*` |
| `src/deployment/nginx-conf/nginx/nginx.conf` | the reverse proxy (`location ^~ /api-service/` → `proxy_pass http://api-service:9000/;` 35-44, `/` → `frontend:3000` 46-55) |
| `src/deployment/deploy_images/{Pulumi.yaml, Pulumi.dev.yaml, __main__.py}` | project `deploy-images` (toolchain uv); timestamp tag 13, registry 14-15, three `docker_build.Image`s (23-71: `platforms`, `push=True`, 30-min timeout, `retain_on_delete`), exports 34-35 … |
| `src/deployment/deploy_single_vm/*` | `Pulumi.yaml`, `Pulumi.dev.yaml` (the instructor's project and `sa_…` user), `Pulumi.dev-test.yaml`, `__main__.py` (the four phases 14-26, exports 29-34), `create_instance.py` (`get_image` 100-103: where every preview stops here), `provision_instance.py`, `setup_containers.py`, `setup_webserver.py`, and the two unused `*_using_command.py` variants |
| `src/api-service/{Dockerfile, docker-hub.sh, docker-shell.sh, docker-entrypoint.sh, pyproject.toml, uv.lock, .gitignore}`, `api/service.py`, `api/utils/llm_{utils,rag_utils,agent_utils,cnn_utils}.py`, `api/routers/{podcast,newsletter,llm_rag_chat}.py` | `docker-hub.sh` (11 `DOCKER_USERNAME="dlops"`, 27 `buildx create … --use`, 31/35 amd64+arm64), v3's `ROOT_PATH` mount and `/status` (`service.py` 12-13, 34-36, 48-50), `GENERATIVE_MODEL = "gemini-2.0-flash-001"` |
| `src/frontend-react/{Dockerfile, Dockerfile.dev, docker-hub.sh, docker-shell.sh, next.config.js, package.json, package-lock.json, .gitignore}`, `src/services/{DataService,Common}.js`, `src/components/layout/Footer.jsx` | the 3-stage standalone build (`# syntax=docker/dockerfile:1.6`, `COPY .env.production .env` 28), `docker-hub.sh` (amd64 only, 31/35), the footer's `/status` call |
| `src/frontend-react/.env.production`, `.env.development` | **one deviation:** line 3 `NEXTAUTH_SECRET=` keeps its key but its committed value is replaced by `<value not copied: see ASSETS.md>` (a credential-like string; series rule). Line 2 `NEXT_PUBLIC_BASE_API_URL=/api-service` is unchanged |
| `src/vector-db/{Dockerfile, docker-hub.sh, docker-shell.sh, docker-entrypoint.sh, docker-compose.yml, pyproject.toml, uv.lock, cli.py, .gitignore}` | the loader (`--download` 487, `load()` 286-292, the try/except that hides failures 531, 577-579) |
| `.gitignore` | the repo root's |

**Names (series rule).** `src/vector-db/cli.py:75` and `:440` contain the instructor's name: a code
panel that quotes those lines masks it as `‹instructor›`. Captures were masked at capture time
(`run_steps.sh` `mask`, the name read at run time from the tutorial's own page, never written here);
none contained it in the end. **Ids:** `README.md` and `Pulumi.dev.yaml` contain the instructor's
project id `ac215-project` and OS Login user `sa_100110341521630214262`; the README commands that
contain them were run verbatim (they are what a student types before replacing them), but a scene
shows the `sa_` number replaced (e.g. `sa_000000000000000000000`, as in `expected/`).

## `terminal/` — real terminal sessions

Captured **2026-11-05 22:06–23:42 UTC** by `terminal/capture.sh`, which runs `terminal/run_steps.sh`
in fresh disposable containers, one segment at a time. Each README command runs exactly as printed
(multi-line commands are read from the README's own lines by `readme a b`, so they are byte-identical),
in README order, and its output goes to its own file: `$ command`, the output, `[exit N]`. Steps
whose name contains `-x-` are extras (not in the README). Two kinds of file: `step` files (no
terminal) and `istep`/`ctstep` files (a real pseudo-terminal through `ptyrun.py`, 100×40, typed
input; `^C` is typed as the byte): `vm/38, 40, 53-57`, `laptop/b02, b02b, b02d, b10, b14`.

| folder | environment | README section |
| --- | --- | --- |
| `vm/` | the VM: `debian:12` (Debian 12 bookworm, x86_64, hostname `cheese-app-vm`), privileged, own network namespace; the GCP image's baseline only (sudo, curl, python3, ca-certificates, user `student` with passwordless sudo). Docker **29.9.3** from the README's `get-docker.sh` (script commit `ada7a56`) | **Deployment to GCP (Manual)** from "SSH into your newly created instance" (README:46) to nginx (219), the URL (222), and the Single-VM section's VM commands (371-383), which use the same container names |
| `laptop/` | a fresh, empty Docker engine standing in for a laptop with Docker Desktop: `docker:29.8.2-dind` (client + engine 29.8.2, buildx v0.37.2), Alpine, user `student` in the `docker` group, git 2.54.0, curl, python3, openssl; home = the README's parent folder (`cheese-app-v3/`, `secrets/`) | Manual: Docker Hub (18-35); **Single VM Instance** (261-389), all of it |
| `expected/` | — | the README's OS Login output snippet (below) |

### `vm/` — the manual deployment on a fresh Debian 12 machine

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | extra | 2026-11-05, Debian 12 bookworm, x86_64, no `docker` yet, home `/home/student` |
| `01-get-docker-download.txt` | README:48 | `curl -fsSL https://get.docker.com -o get-docker.sh`, silent |
| `02-get-docker-install.txt` | README:49 | the script's `+ sh -c …` trace (Docker's apt repo for `bookworm`, docker-ce, buildx, compose, model plugin), the rootless-mode note. **`WARNING: unable to enable the docker service`**: a container has no systemd; on a VM systemd starts dockerd here (capture-only below) |
| `03-docker-version.txt` | README:51 | `Docker version 29.9.3, build 5457199` |
| `04-x-docker-info.txt` | extra | server 29.9.3, overlay2, no images |
| `10`-`15-folders-N.txt` | README:61-67 (the code block; 54-59 lists the same six as bullets) | each `sudo mkdir` / `sudo chmod` silent, exit 0 |
| `16-x-ls.txt` | extra | `conf`, `persistent-folder`, `secrets` owned by root with `drwxrwxrwx`, `get-docker.sh` |
| `17-secret-echo.txt`, `18-x-cat-secret.txt` | README:74, verbatim | the README's placeholder written as the "key": the file contains `<___Json Key___>`. Nothing below needed a key (see 27, 31) |
| `19-network-create.txt` | README:80 | the network id |
| `20-chroma-pull.txt` | README:86 | `chromadb/chroma:latest`, `Digest: sha256:1e0b73a1…` |
| `21-chroma-stop.txt`, `22-chroma-rm.txt` | README:87-88 | `Error response from daemon: No such container: cheese-app-vector-db`, exit 0 thanks to `\|\| true` |
| `23-chroma-run.txt` | README:89-97, verbatim | the container id |
| `24-x-chroma-check.txt` | extra | `0.0.0.0:8000->8000/tcp`; `/api/v2/heartbeat`; **`/api/v2/version` → `"1.0.0"`** |
| `25-x-chroma-logs.txt` | extra | **`persist_path: "/data"`**, `Saving data to: /data` (the Chroma logo in `(((`/`###`) |
| `26-loader-pull.txt` | README:103 | `dlops/cheese-app-vector-db-cli`, `Digest: sha256:718f7040…` |
| `27-loader-run.txt` | README:104-112, verbatim | `Python 3.12.12`, `uv 0.9.9`, `download()`, `load()`, `Creating collection: recursive-split-collection`, 11 files `Processing file: outputs/embeddings-recursive-split-….jsonl` with their `Shape` and `Inserted …` lines: **14,356 chunks**, exit 0. `--download --load` needs **no Google call** (pre-computed embeddings from a GitHub release), so the placeholder key did not matter |
| `28-x-chroma-volume.txt` | extra (digest errata 21) | `docker-volumes/chromadb` on the VM is **empty**; inside the container `/chroma/chroma` is empty and `/data` holds `chroma.sqlite3` (36 MB): the README's mount misses Chroma 1.x's data path |
| `30-api-run.txt` | README:118-127, verbatim | `Unable to find image 'dlops/cheese-app-api-service:latest' locally`, the pull (`Digest: sha256:3412a226…`), the container id. That first start crashed on the recording proxy (capture-only below) |
| `30b-api-run-again.txt` | README:118-127 again, after the capture-only re-tag | the container id |
| `31-x-api-logs.txt` | extra | the entrypoint banner, "The following commands are available: uvicorn_server", TensorFlow's CPU/CUDA notices, **`Loading CNN Model...`** (the model is downloaded at import), the Keras summary (2,422,470 params), `Uvicorn running on http://0.0.0.0:9000` |
| `32-x-api-ps.txt` | extra | both containers up; the api image is **5.07 GB** |
| `33-x-curl-api-root.txt` | extra | `{"message":"Welcome to AC215"}` |
| `34-x-curl-api-status.txt` | extra (digest gotcha 24, **confirmed**) | `HTTP/1.1 404 Not Found` `{"detail":"Not Found"}`: the public image predates v3's `/status` |
| `35-x-curl-api-docs.txt` | extra | `/docs` is a real Swagger page here and `/openapi.json` lists `/`, `/llm-agent/…`, `/llm-cnn/…`, `/llm-rag/…`, …: the old image has no `ROOT_PATH` mount (digest errata 4 applies to v3 code, not to this image) |
| `36-x-image-service-py.txt` | extra | the image's `api/service.py`: 0 matches for `ROOT_PATH\|mount\|/status`; `@app.get("/")`, `@app.get("/square_root/")`, the six routers; `GENERATIVE_MODEL = "gemini-2.0-flash-001"` in four files (retired 2026-06-01, digest gotcha 22) |
| `37-x-entrypoint.txt` | extra | the image's entrypoint: production mode runs `uv run uvicorn api.service:app … --root-path /api-service --lifespan on`; `DEV=1` keeps a shell |
| `38-api-interactive.txt` | README:133-144, verbatim, in a terminal | `docker: Error response from daemon: Conflict. The container name "/api-service" is already in use …`, exit 125: the README runs it with the same name while the detached one runs |
| `39-x-api-rm.txt`, `40-x-api-interactive-after-rm.txt`, `41-x-api-run-detached-again.txt` | extras | after `sudo docker rm -f api-service` the interactive variant opens `app@<id>:/app$` with the banner (typed `exit`); then the detached command again |
| `42-frontend-run.txt` | README:150 | pulls `dlops/cheese-app-frontend-react` (`Digest: sha256:255a23b2…`), container id |
| `43-x-frontend-check.txt` | extra | `<title>Formaggio</title>`; logs `▲ Next.js 15.0.2`, `✓ Ready in 67ms`, `BASE_API_URL: /api-service` |
| `44-nginx-conf-echo.txt` | README:156-213, verbatim | silent, exit 0 |
| `45-x-nginx-conf-logformat.txt` | extra (digest errata 5, **confirmed**) | 58 lines; `cat -A` of lines 7-13: `log_format  main   - []  $`, two whitespace lines, `;$`: the variables were eaten by the nested single quotes |
| `46-nginx-run.txt` | README:219 | pulls `nginx:stable` (`Digest: sha256:42c68eab…`), container id |
| `47-x-container-ls.txt` | extra | the four containers: nginx 80, frontend 3000, api-service 9000, vector-db 8000 |
| `48-x-curl-home.txt` | extra (README:222 "access … `http://<Your VM IP Address>/`", from the VM itself) | `HTTP/1.1 200 OK`, `Server: nginx`, the Next.js headers, `<title>Formaggio</title>` |
| `49-x-curl-api-via-nginx.txt` | extra | `/api-service/` → `{"message":"Welcome to AC215"}` (nginx stripped the prefix); `/api-service/status` → 404 |
| `50-x-curl-api-port.txt` | extra | port 9000 directly; `/api-service/openapi.json` with `"servers":[{"url":"/api-service"}]` |
| `51-x-nginx-logs.txt` | extra | the access log lines are just **`-[]`**: errata 5's visible effect |
| `52-container-ls.txt` | README:373 (written for the Pulumi VM; same container names here) | the four containers |
| `53-logs-api-service.txt` | README:374, in a terminal, `^C` after 5 s | the startup log + the access lines of the curls above (`GET /api-service/ 200`, `GET /api-service/status 404` …), exit 130 |
| `54-logs-frontend.txt`, `55-logs-nginx.txt` | README:375, 376 | Next.js ready lines; nginx's entrypoint lines and the `-[]` access lines |
| `56-exec-api-service.txt` | README:381 | `app@<id>:/app$ ls` → `Dockerfile api docker-entrypoint.sh … uv.lock`, `exit` |
| `57-exec-nginx.txt` | README:382 | `root@<id>:/# nginx -v` → `nginx version: nginx/1.30.6`, `exit` |
| `58-x-frontend-down.txt` | extra (digest gotchas 11/12, **reproduced**) | `docker stop frontend` + `docker restart nginx`: nginx `Exited (1)`, `nginx: [emerg] host not found in upstream "frontend" in /etc/nginx/nginx.conf:48`, `http://localhost/ -> 000` |
| `59-x-frontend-up.txt` | extra | `docker start frontend nginx` → `http://localhost/ -> 200` |
| `60-x-images.txt` | extra | chroma 640 MB, api-service 5.07 GB, frontend 232 MB, nginx 163 MB |

### `laptop/` — Docker Hub, then the Pulumi toolbox

| file | README step | what it shows |
| --- | --- | --- |
| `p00-x-env.txt` | extra | 2026-11-05, Docker 29.8.2, buildx v0.37.2, git 2.54.0, no images |
| `p01-clone.txt`, `p02-x-git-log.txt`, `p03-x-ls-remote.txt` | extra (the README has no clone command) | `Cloning into 'cheese-app-v3'...`; `3ecef56… 2025-11-28 16:00:06 -0500 v4->v3`; the branches (`work/‹staff›` masked; `p02` was masked after capture with the same `sed` the script now runs) |
| `p04-mkdir-secrets.txt`, `p05-x-tree.txt` | README:236-259 (the keys go in `secrets/` next to the repo) | `secrets/deployment.json`, `secrets/gcp-service.json` (placeholders, capture-only below), the `src/` and `src/deployment/` listings |
| `a01-docker-login.txt` | README:21, typed as printed | `bash: -c: line 1: syntax error near unexpected token `newline'`, exit 2: the `<…>` placeholders are shell redirections. Replace them entirely |
| `a02-frontend-docker-hub.txt` | README:28-31 (`frontend-react`, `sh docker-hub.sh`) | `Docker Username: dlops`, `Creating new multi-arch builder...`, BuildKit `docker-container` builder booting, the 3-stage build (`npm ci` 59 s, `npm run build` → `✓ Compiled successfully`), **`WARNING: No output specified with docker-container driver. Build result will only remain in the build cache`**, `Pushing multi-arch image to registry...`, then **`failed to push dlops/cheese-app-frontend-react: push access denied … insufficient_scope: authorization failed`**, exit 1 (the hardcoded `DOCKER_USERNAME="dlops"`, digest gotcha 2, plus no login) |
| `a03-x-buildx-ls.txt` | extra | `multi-arch*` (docker-container, BuildKit v0.34.2) is now the current builder |
| `a04`-`a06-x-…` | extras (digest gotcha 3, **not reproduced**) | with `multi-arch` current, a plain `docker build -t hello-node .` + `docker run hello-node` still works (`v20.20.2`): on Docker 29 / buildx 0.37 `docker build` loads its result by default. Only `docker buildx build` without `--load`/`--push` keeps it in the cache (the WARNING in a02). `docker buildx use default` (a05) is still the tidy reset |
| `b01-set-project.txt` | README:266-267 ("change `GCP_PROJECT` to your project id") | `export GCP_PROJECT="your-gcp-project" # Change to your GCP Project` (a placeholder) |
| **`b02-docker-shell.txt`** | **README:268 `sh docker-shell.sh`, as committed** | `Container 'cheese-app-deployment' is not running. Building …`, `[ 2/16] RUN apt-get update && apt-get install -y curl …`: 22 × `E: Failed to fetch https://deb.debian.org/debian-security/pool/updates/main/… 404 Not Found`, `ERROR: failed to build`, then `Unable to find image 'cheese-app-deployment:latest' locally`, `pull access denied`, exit 125 (breakage 1). The URLs read `https://` and end in `[IP: 172.17.0.1 38720]` only because of the recording proxy (capture-only below); a student sees `http://` and their mirror's IP: crop that column |
| `b02a-x-fix-base.txt` | extra: fix 1 | `4:FROM python:3.13-slim-bookworm` |
| `b02b-docker-shell-bookworm.txt` | README:268 again | steps 2-7 pass; `[ 8/16]` fails: `Package google-cloud-sdk is not available … However the following packages replace it: google-cloud-cli`, `E: Package 'google-cloud-sdk' has no installation candidate`, then the same `pull access denied` (breakage 2) |
| `b02c-x-fix-gcloud-packages.txt` | extra: fix 2 | the `git diff` of `Dockerfile` with both edits |
| **`b02d-docker-shell-fixed.txt`** | README:268 a third time | `[+] Building 91.9s (21/21) FINISHED`, then the entrypoint: `Architecture: x86_64`, `Python 3.13.18`, `uv 0.13.7`; **`ERROR: (gcloud.auth.activate-service-account) There was a problem refreshing auth tokens for account deployment@your-gcp-project…: ('invalid_grant: Invalid grant: account not found'`**; `Updated property [core/project].`; the credHelpers warning + `Adding credentials for: us-docker.pkg.dev`; `Bucket does not exist. Creating...` → `You are attempting to access protected data with no configured credentials`; `Logging into Pulumi using GCS bucket: gs://your-gcp-project-pulumi-state-bucket` → `error: could not log in to the state backend … invalid_grant`; `BucketNotFoundException: 404`, `No stacks found.`; the prompt `root@<id>:/app#`. **The last two lines** (`[ptyrun: timed out …]`, `[exit 137]`) are the capture's own timeout ending the session, not the tutorial |
| `b03-gcloud-version.txt` | README:272 | `Google Cloud SDK 592.0.0`, core/alpha/beta 2026.10.30, bq 2.1.41, bundled Python 3.14.9, gke-gcloud-auth-plugin 0.5.21, gsutil 5.38, kubectl 1.35.9 |
| `b04-pulumi-version.txt` | README:273 | `v3.274.0` |
| `b05-kubectl-version.txt` | README:274 | `Client Version: v1.35.9-dispatcher`, Kustomize v5.7.1: gcloud's bundled kubectl is first on `PATH`, not the apt 1.34 the Dockerfile pins (33-41) |
| `b06-gcloud-auth-list.txt` | README:278 | **`No credentialed accounts.`**: with a real key the README expects `deployment@<project>.iam.gserviceaccount.com` (active) |
| `b07-x-env.txt` | extra | `GCP_PROJECT=your-gcp-project`, region/zone, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/deployment.json`, `PULUMI_BUCKET=gs://your-gcp-project-pulumi-state-bucket`, `PULUMI_CONFIG_PASSPHRASE=` (empty), `/secrets` (+ the empty `.ssh` the mount creates), `/usr/bin/docker`, `/usr/bin/ssh`, the laptop's containers seen through the socket |
| `b08-oslogin-template.txt` | README:286, typed as printed | `bash: line 1: YOUR: No such file or directory`: `<YOUR GCP_PROJECT>` is a redirection |
| `b09-oslogin-example.txt` | README:290 | `ERROR: (gcloud.compute.project-info.add-metadata) You do not currently have an active account selected.` |
| `b10-ssh-keygen.txt` | README:295-297 (`cd /secrets` / `ssh-keygen -f ssh-key-deployment` / `cd /app`), in a terminal, Enter twice | `Generating public/private rsa key pair.`, the two passphrase prompts (left empty), the files, a `SHA256:` fingerprint (`root@<container id>`), the randomart (`RSA 3072`). A throwaway key, deleted with the laptop |
| `b11-x-ls-keys.txt` | extra | `ssh-key-deployment` (`-rw-------`) and `.pub` in `/secrets`, i.e. in the laptop's `secrets/` folder |
| `b12-oslogin-ssh-keys-add.txt` | README:302 | the same "no active account" error; what the README shows instead is `expected/oslogin-ssh-keys-add.txt` |
| `b13-x-inventory.txt` | extra (README:318-322 "Add ssh user details in inventory.yml") | `ls: cannot access 'inventory.yml'`; no such file anywhere in the toolbox (Ansible leftover, digest errata 2) |
| `b14-images-stack-init.txt` | README:332 (`cd deploy_images`, `pulumi stack init dev`), in a terminal | Pulumi was never logged in (b02d), so it offers Pulumi Cloud: `Connect to Pulumi Cloud for state storage, …`, `Press <ENTER> to log in with your browser, or`. The capture's typed key acted as Enter, so the lines after it (`We couldn't launch your web browser …`, the app.pulumi.com URL with a session nonce, `Waiting for login to complete...`, `[exit 143]`) are the capture's doing: **crop after "or"** |
| `b15`-`b22` | README:333, 339, 344, 352-355, 361, 366, 389, verbatim | each: `error: PULUMI_ACCESS_TOKEN must be set for login during non-interactive CLI sessions`, exit 3. (Run without a terminal; in a terminal each would offer the same Pulumi Cloud login as b14.) The honest first error of every Pulumi command when the GCS backend login failed |
| `b30-x-login-local.txt` | extra: `pulumi login --local` (Pulumi's file backend, no account) | `Logged in to <id> as root (file://~)` |
| `b31-x-images-stack-init.txt`, `b32-x-images-config-set.txt` | README:332-333 verbatim, on the local backend | `Created stack 'dev'`; config set silent |
| `b33-x-images-config.txt` | extra | `gcp:project ac215-project`, `pulumi:tags`; `Pulumi.dev.yaml` keeps the committed `encryptionsalt` (works with the empty passphrase); `dev*` with 0 resources |
| `b34-x-images-preview-frontend.txt` | README:339 + `--target` the frontend image (extra: one image of three, for the recording disk) | the five provider plugins downloaded (kubernetes 4.23.0, docker 4.9.0, command 1.1.3, gcp 9.3.0, docker-build 0.0.15), `+ docker-build:index:Image build-cheese-app-frontend-react create`, **`warning: Skipping preview build because some inputs are unknown.`** (preview does not build here), `Outputs:` with `cheese-app-frontend-react-tags: ["us-docker.pkg.dev/ac215-project/cheese-app-repository/cheese-app-frontend-react:20261105233500"]`, the other exports `[unknown]`, `+ 2 to create` |
| `b35-x-images-up-frontend.txt` | README:344 + the same `--target` | the preview again (tag `…:20261105233502`: a new timestamp every run), then the build stops at `x509: certificate signed by unknown authority` resolving `docker/dockerfile:1.6`: pulumi-docker-build had created **its own docker-container BuildKit** (`wonderful_wilbur`), which does not trust the recording proxy. Environmental; kept because b35b continues it |
| **`b35b-x-images-up-frontend-build.txt`** | the same `pulumi up` (without `--refresh`: after b35's failed create the refresh refuses a `--target` not yet in the stack), after capture-only CA config for that builder | the real build inside `pulumi up` (`#13 … DONE 70.3s` npm ci, `#17 … DONE 42.3s` next build, `creating (133s)`), then the push: **`failed to push us-docker.pkg.dev/ac215-project/cheese-app-repository/cheese-app-frontend-react:20261105233941: failed to authorize: failed to fetch anonymous token: … 403 Forbidden`**: the gcloud credential helper had no account, so the push went anonymous. `Resources: 3 unchanged, 2 errored`. A student with a key and the repository gets past this; one without the repository gets digest gotcha 1 |
| `b36-x-images-after.txt`, `b36b-x-images-after.txt` | extra | `dev*` 2 resources, `No output values currently in this stack`; `cheese-app-deployment:latest` 2.61 GB |
| `b40-x-vm-stack-init.txt`, `b41-x-vm-config-set-1..3.txt`, `b42-x-vm-config.txt` | README:352-355 verbatim (`cd deploy_single_vm`), local backend | `Created stack 'dev'`; the four config keys incl. `security:ssh_user sa_…` (mask in a frame) |
| **`b43-x-vm-preview.txt`** | README:361, local backend | `+ gcp:compute:Disk cheese-app-demo-disk`, `+ gcp:compute:Network cheese-app-network`, `+ gcp:compute:Firewall allow-http / allow-https / allow-ssh`, then `create_instance.py, line 100` `gcp.compute.get_image(family="ubuntu-2204-lts", …)` → **`oauth2: cannot fetch token: 400 Bad Request` `{"error":"invalid_grant","error_description":"Invalid grant: account not found"}`**, `+ 6 to create`, `1 errored`, exit 1: the first call that needs Google is the image lookup |
| `b44-x-vm-up.txt` | README:366, local backend | the same preview error; nothing is created |
| `b45-x-destroy.txt` | README:389, local backend | `Previewing destroy`, `Destroying`, `Duration: 1s`, "The resources in the stack have been deleted, but the history and configuration … are still maintained. If you want to remove the stack completely, run `pulumi stack rm dev`." |
| `b46-x-stacks-on-disk.txt` | extra | `organization/deploy-images/dev` (2) and `organization/deploy-single-vm/dev` (0): the fully qualified names `setup_containers.py:27` refers to; `~/.pulumi/stacks/<project>/dev.json` (the file backend's layout, same as in the GCS bucket); the plugins cached in `src/deployment/pulumi-plugins/` on the laptop (`.gitignore`d); `/app` is not a git repository inside the container |

### `expected/`

| file | source | used for |
| --- | --- | --- |
| `oslogin-ssh-keys-add.txt` | README.md:306-314 at `3ecef56` (the README's own "snippet of the output" of README:302), unchanged except the account number and uid/gid replaced by 0s | the `expected` output panel after `b12`'s honest error: `username: sa_000000000000000000000` |

### capture-only (not part of the tutorial)

- **The recording proxy.** The sandbox reaches the internet only through a TLS-intercepting HTTPS
  proxy on the host's loopback. `proxy_relay.py` (container `l20-relay`, port 38720) forwards it onto
  Docker's bridge; each machine trusts its CA; Docker client `proxies` pass it to containers. A
  student's machine needs none of this.
- **`vm/`**: `capture.sh vm-dockerd` starts `dockerd` by hand after `get-docker.sh` (no systemd in a
  container), with Docker's classic image store (`containerd-snapshotter: false`; the recording disk
  could not hold the 1.8 GB-compressed api image twice). `vm/capture-only/`: the loader and api images
  re-tagged with the proxy CA under the same names (`*.Dockerfile`, `*-build.txt`; the README's
  `docker run` lines stay verbatim). `api-first-start.txt`: the first api start died at import on the
  proxy's TLS (`SSLError … github.com … /dlops-io/models/releases/download/v4.0/experiment_1760994796.zip`):
  a real fact worth one sentence (the API downloads its CNN model from GitHub every start), not a
  student error. `rmi-loader.txt`: the loader image removed before the api pull (disk).
- **`laptop/`**: the two key files in `secrets/` are well-formed service-account files around
  throwaway RSA keys generated at capture time for **no account**, `client_email`
  `deployment@your-gcp-project…` / `gcp-service@your-gcp-project…` (`capture-only/placeholder-*.json`,
  private key elided; the keys themselves were never written to the repository). Base images re-tagged
  with the proxy CA, https Debian sources and the relay as proxy so the tutorial's Dockerfiles build
  unchanged: `python:3.13-slim-bullseye`, `python:3.13-slim-bookworm`, `node:20-alpine`
  (`capture-only/*.Dockerfile`). Because of that re-tag, b02/b02b show `https://deb.debian.org`; the
  404s are the same over http (checked from the host: the `bullseye-security` pool files return 404 on
  deb.debian.org and security.debian.org, 200 on archive.debian.org). `hub-mirror-pulls.txt`: Docker
  Hub's anonymous pull limit answered 429 for `python:3.13-slim-bookworm`, so it and
  `docker/dockerfile:1.6` came from `mirror.gcr.io` (same images) and were tagged under their Hub
  names. `buildkitd.default.toml` + `mirror-start.txt` (hubprep): docker-hub.sh's builder got the CA
  and a local `registry:2` mirror serving the CA'd `node:20-alpine`, picked up by the script's own
  `docker buildx create` (its first run, before this, stopped at x509 and is not kept).
  `deployment-buildkitd.default.toml` + `drop-provider-builder.txt` (partB5): the same for the
  builder pulumi-docker-build creates inside the toolbox (+ the CA for `us-docker.pkg.dev`).
- **Re-runs on the day.** vm3 → vm4 (the api TLS crash above); vm4b re-ran `36` alone (a template
  error in its first version); vm5's last six steps used wrong README line numbers and were re-run
  as vm6; partB3's readiness probe (`docker top -eo args`) is refused by this engine, so its
  commands ran from `partB4` in the shell b02d had left open (b02d then hit the 900 s session timeout,
  see its last two lines). The scripts in this folder carry the fixed versions.
- `ptyrun.py` (from L14) and the readiness probes (`wait_http`) send no request a file shows.

## What cannot run here, and how the video shows it

| README step | why not | how the video shows it |
| --- | --- | --- |
| Manual "Ensure you have all your container built and works locally" (README:10-16) | the v3 stack locally is the L18 workflow at another commit; not part of this capture | narration + a GREY laptop diagram; the API check is `/status` (v3 code) or `/` (public image, `vm/33`) |
| Docker Hub sign-up, access token, `docker login` (README:18-21) | needs a Docker Hub account | `laptop/a01` (the placeholder pitfall) and `a02`'s push refusal; the token page is an `illustration` |
| `sh docker-hub.sh` in `api-service` and `vector-db` (README:24-26, 33-35) | `linux/amd64,linux/arm64`: no arm64 emulation (binfmt) here, a ~5 GB TensorFlow image ×2, and the push needs a login | the frontend's run (`a02`, amd64 only) stands for all three; the scene quotes `src/api-service/docker-hub.sh:31,35` for the two-platform difference |
| Create the VM in the console (README:40-44) | console, billing | `illustration` (schematic, never a screenshot): N2D, 50 GB disk, Allow HTTP/HTTPS traffic; `vm/00` is the stand-in's identity |
| "SSH into your newly created instance" (README:46), the browser at `http://<VM IP>/` (222, 369) | no VM, no public IP | the stand-in's terminal (`vm/`), `curl` from the VM itself (`vm/48-50`); the browser view is an `illustration` of the home page with the footer (no screenshot) |
| The real gcp-service key (README:71-74) | none exists | `vm/17` runs the README's placeholder line; chat routes are not exercised (Gemini 2.0 retired, digest gotcha 22) |
| APIs to enable, service accounts + roles + keys (README:229-259) | console, IAM | `illustration`s with the README's role lists; `laptop/p05` shows where the files go |
| gcloud OS Login, key upload (README:286, 290, 302) | no account | `b08`/`b09`/`b12` honest errors; `expected/oslogin-ssh-keys-add.txt` for what success prints |
| Pulumi on the GCS backend (README:332-389) | `pulumi login gs://…` needs the deployment key (b02d) | `b14`-`b22` honest errors, then the same commands on the local file backend (`b30`-`b46`, tagged `extra`) up to their first Google call (`b35b` push 403, `b43` `get_image` invalid_grant) |
| `pulumi up` output with `Outputs: instance_ip …`, ~30 resources (README:366-367) | needs a project and billing | nothing records it (no log or stored output in the repo): the scene shows the command, `b43`'s plan (Disk, Network, three Firewalls), and an `illustration` of the resource graph built from `deploy_single_vm/__main__.py:29-34` (export names) and `create_instance.py`, never a fake terminal panel |
| VM commands after Pulumi (README:371-383) | no Pulumi VM | the same commands on the manual VM stand-in (`vm/52-57`), whose container names match except `cheese-app-vector-db` vs Pulumi's `vector-db` (say so) |
| `pulumi destroy` against real resources (README:389) | nothing was created | `b45` on the local backend (empty stack) + an `illustration` of the reverse-order teardown; GOLD cost tags from the digest's cost table |
