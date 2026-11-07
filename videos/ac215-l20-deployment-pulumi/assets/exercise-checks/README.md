# Exercise checks · ac215-l20-deployment-pulumi (2026-11-05 US Eastern; 2026-11-06 00:56–01:12 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/`, which the
answers cite directly (`vm/NN`, `laptop/<id>`, `expected/…`; provenance in [`ASSETS.md`](../../ASSETS.md)). Logs and
the check scripts are in [`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with
`[exit N]`, as in `assets/terminal/run_steps.sh`; where a step pipes into `grep` or `tail`, `[exit N]` is the last
command's status. In the logs, `<logs>` is this folder, `<assets/source>` is `assets/source/`, and `$WORK` a scratch
folder that was deleted afterwards. The nginx access log and `debugfs` print UTC dates (`06/Nov/2026`).

There was **no Google account, no GCP project, no Docker Hub login and no credentials**, as in the captures. Nothing
here created a cloud resource or called a Google API. No tutorial code ran on the host: the repository's files are
the unchanged copies in `assets/source/` (at `3ecef56`), mounted read-only into disposable containers. No log
contains a person's name, a key, a real project ID, an `sa_` number or an IP address (the one client address in
`nginx.log` is replaced by `<client ip>`); the placeholders are `your-gcp-project` and the README's `ac215-project`.

## Setup (disposable)

- Docker Engine 29.8.2 on the session machine (a fresh daemon, no images at the start). Base images came from
  `mirror.gcr.io` (the same official images, re-tagged under their Docker Hub names), to avoid Docker Hub's
  anonymous pull limit that stopped the L14 and L20 captures: `nginx:stable` (nginx/1.30.6, the version of
  `vm/57`), `python:3.13-slim-bookworm`, `debian:12`.
- [`nginx.sh`](logs/nginx.sh): `nginx:stable` with the repository's `src/deployment/nginx-conf/nginx/nginx.conf`
  mounted read-only, published on host port **18080** (the VM's port 80), in front of two stand-ins on a Docker
  network: containers `l20ex-api` and `l20ex-frontend` answering to the network aliases `api-service` (port 9000)
  and `frontend` (port 3000), the names `nginx.conf` uses. The stand-ins are [`echo_stub.py`](logs/echo_stub.py): they
  answer every request with their name and the path they received, so the log shows what nginx forwarded. They are
  not the app.
- [`fastapi.sh`](logs/fastapi.sh): [`rootpath_app.py`](logs/rootpath_app.py), the routing lines of
  `src/api-service/api/service.py:12-50` (the routes `/` and `/status`, the inner app mounted under `ROOT_PATH`),
  with FastAPI 0.120.4 and Starlette 0.49.3 as pinned in `src/api-service/uv.lock`, called through Starlette's
  `TestClient`. The routers (model, Chroma, Vertex AI) are left out.
- [`disk.sh`](logs/disk.sh) runs [`disk-inner.sh`](logs/disk-inner.sh) in `debian:12` (e2fsprogs 1.47.0) with
  `--network none`: a 64 MB image file stands in for `/dev/disk/by-id/google-persistent-disk-1`; `debugfs` writes and
  reads a file inside the ext4 image, so no device, mount or privilege is needed.
- [`pulumi-setup.sh`](logs/pulumi-setup.sh) ([`pulumi-setup.log`](logs/pulumi-setup.log)): container `l20ex-pulumi`
  (`python:3.13-slim-bookworm`, the Pulumi CLI **v3.274.0**, the toolbox's version in `laptop/b04`, Python SDK
  `pulumi` 3.274.1, `pulumi-command` 1.1.3 and `pulumi-docker` 4.9.0, the plugin versions of `laptop/b34`), with the
  empty `PULUMI_CONFIG_PASSPHRASE` of the toolbox (`src/deployment/Dockerfile:51`) and the host's Docker socket;
  container `l20ex-sshd` (`debian:12`, OpenSSH server on `127.0.0.1:12222`, user `student`, key-only login) standing
  in for the VM's SSH door. Two throwaway RSA keys were generated inside `l20ex-pulumi` at setup
  (`ssh-key-deployment` without a passphrase, `ssh-key-with-passphrase` with one); they never left the containers.
- [`pulumi.sh`](logs/pulumi.sh) runs Pulumi on its **local file backend** (`pulumi login --local`, the video's
  `extra · not for you`, `laptop/b30`) with two small exercise projects, [`pulumi-projects/`](logs/pulumi-projects/):
  `l20ex-images` stands in for `deploy_images` (the same timestamp tag and export name, but its "build" is a
  `local.Command` that only echoes the tag) and `l20ex-vm` for `deploy_single_vm` (a `StackReference` to
  `organization/l20ex-images/dev`, one `docker.Container` on the local Docker daemon instead of `ssh://`, and one
  `remote.Command` over SSH to `l20ex-sshd`). **They are not the tutorial's programs**: the real ones need a GCP
  project (`laptop/b43` stops at the first Google call). They show Pulumi's own behaviour (plans, `-y`, `--refresh`,
  stack references, drift, commands, destroy) with the same CLI and provider versions.

## Checks

| exercise | what was run | result |
| --- | --- | --- |
| Q1, B1 | `nginx.sh` "B1": `curl` of `/`, `/status`, `/api-service/`, `/api-service/status`, `/api-service/podcasts/?limit=3`, `/api-servicex/status`, `/api-service` ([`nginx.log`](logs/nginx.log)) | the API stand-in sees `/`, `/status`, `/podcasts/?limit=3`; `/status` and `/api-servicex/status` go to the frontend unchanged; `/api-service` (no slash) → `301 -> http://localhost/api-service/` |
| B1 | the same with line 37 changed to `proxy_pass http://api-service:9000;` | the API stand-in sees `/api-service/status` and `/api-service/` (prefix kept) |
| Q1, B1 | `fastapi.sh` ([`fastapi.log`](logs/fastapi.log)) | `ROOT_PATH` unset: `GET /status -> 200 {"version":"3.0"}`, `GET /api-service/status -> 404`; `ROOT_PATH=/api-service`: the reverse |
| B2 | `nginx.sh` "B2": README:156-213 run as written, and the same text as a quoted heredoc; `diff`; `nginx -t`; one access-log line each | echo: 58 lines, `log_format  main   - []  ` + two blank lines + `;` (as `vm/45`); heredoc: 57 lines with the three `log_format` lines intact (it differs from the repo's `nginx.conf` only in blank lines and one shortened comment); both pass `nginx -t`; access log `-[]` vs `<client ip> - - [06/Nov/2026:01:00:21 +0000] "GET /api-service/status HTTP/1.1" 200 64 "-" "curl/8.5.0" "-"` |
| B3, C6 | `nginx.sh` "B3", "C6": stop the frontend stand-in with nginx running; then restart nginx; then the API stand-in | nginx running: `/ -> 504`, `/api-service/status` still answered; after `docker restart`: `Exited (1)`, `host not found in upstream "frontend" in /etc/nginx/nginx.conf:48`, `/api-service/status -> 000`; frontend, then nginx started → `/ -> 200`; with the API stand-in stopped: `host not found in upstream "api-service" in /etc/nginx/nginx.conf:37` |
| Q4, B4 | `disk.sh` ([`disk.log`](logs/disk.log)) | first guarded run formats (prints nothing, exit 0); `blkid` → `ext4`; a file `history.txt` written; second guarded run prints `ext4` and formats nothing: the file is still there; the same second run **without** the guard (stdin not a terminal) reformats without asking, and `history.txt: File not found by ext2_lookup` |
| Q2, B5 | `pulumi.sh` "B5": `pulumi up` without `-y`, with `-y`, then `preview --refresh` and `up --refresh -y` again ([`pulumi.log`](logs/pulumi.log)) | without `-y`: `error: --yes or --skip-preview or --preview-only must be passed in to proceed when running in non-interactive mode` (exit 2); with `-y`: the preview is printed, then applied; second run: `+-1 to replace` (the timestamp tag changed, `20261106010441` → `…443`/`…445`) |
| D2 | `pulumi.sh` "D2": `pulumi config set fixed_tag 3ecef56`, up, then `preview --refresh` | `2 unchanged` |
| C8 | `pulumi.sh` "C8": `pulumi preview` in `l20ex-vm` before the images stack exists | `error: Preview failed: unknown stack "organization/l20ex-images/dev"` |
| B5 | `pulumi stack init dev` twice | `Created stack 'dev'`, then `error: stack 'organization/l20ex-images/dev' already exists`; `pulumi stack select dev` works |
| B6 | `pulumi.sh` "B6": VM stack up, up again, a new images up, the VM stack's `preview --refresh --diff` and up | first up `+ 3 created`; again `3 unchanged`; after the new images up: the `StackReference` output changes and the container is `+-1 to replace` (`[diff: ~labels]`), the `remote.Command` unchanged |
| B7, Q4 | `pulumi.sh` "B7": `docker rm -f l20ex-web` on the host; `preview` without and with `--refresh`; then delete the file the `remote.Command` made and `preview --refresh` | without `--refresh`: `3 unchanged`; with it: `+ 1 to create`; `up --refresh -y` recreates it; the deleted file: `3 unchanged` (Pulumi cannot see it) |
| C9 | `pulumi.sh` "C9": a `remote.Command` whose key has a passphrase | `error: ssh: this private key is passphrase protected`, `**creating failed**` |
| C7 | `pulumi.sh` "C7": `ssh` to `l20ex-sshd` without and with `-i` | `student@127.0.0.1: Permission denied (publickey).` (exit 255); with `-i /work/keys/ssh-key-deployment`: `logged in` |
| Q5 | `pulumi.sh` "Q5": `pulumi destroy --stack dev --refresh -y` in `l20ex-vm`, then `l20ex-images`, `pulumi stack rm` | `- 3 deleted`: the container is gone, the file the command made on the "VM" is still there; "The resources in the stack have been deleted, but the history and configuration associated with the stack are still maintained."; both stacks listed until `pulumi stack rm dev -y` |

## Not run (and why)

- **Everything that needs Google or Docker Hub**: the console steps, the APIs, service accounts and keys, OS Login,
  the Artifact Registry push, the real `deploy_images` and `deploy_single_vm` programs, the VM, the firewall, a
  reboot, `gcloud artifacts repositories create/delete`, `gcloud storage rm`, `gcloud compute os-login ssh-keys
  remove`. Their answers cite the README, the code at `3ecef56` and the captured first errors (`laptop/b02d`,
  `b06`, `b09`, `b12`, `b15`-`b22`, `b35b`, `b43`), and say so. Where an answer relies on the Google provider's or
  Compute Engine's documented behaviour (changing a running VM's service account, a newer Ubuntu image replacing the
  VM, the default network's firewall rules), it says "not checked here".
- **The real images**: the api image is 5.07 GB and the `docker-hub.sh` two-platform builds need arm64 emulation;
  the captures `vm/30`-`41`, `laptop/a02` answer those exercises. Chroma's `/data` path is answered from `vm/25`,
  `vm/28`, not re-run.
- **Timing**: `nginx.sh` did not measure how long the `504` took (nginx's proxy timeouts).

## Cleanup

Every container was removed by name (`nginx.log` ends with 0 containers named `l20ex-…`; `l20ex-pulumi` and
`l20ex-sshd` were removed after `pulumi.log`), the Docker network `l20ex-net` too, and all images pulled for these
checks were deleted afterwards (`docker images` empty). The throwaway SSH keys and the Pulumi state lived only inside
`l20ex-pulumi`. The scratch folder `$WORK` was deleted file by file. Nothing was written outside the containers, the
scratchpad and this folder.
