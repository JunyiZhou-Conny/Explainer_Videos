# Assets and where they come from

Everything a scene shows as "real" (a terminal output, a source line, a file listing) is read from
a file in `assets/`, never typed by hand into a scene. This file says where each one came from.

**The one thing to know about this lecture's captures:** the lecture speaks Google Cloud (GKE,
Artifact Registry, a service-account key in a GitHub secret); the tutorial this video follows is
the AWS variant `dlops-io/cheese-app-aws` (series decision on issue #125, as L15 did), and the
recording sandbox has **no AWS account, no access key, no EC2 instance, no ECR registry and no
GitHub Actions run**. Everything that runs on the student's laptop is captured live in a fresh
Linux "laptop" (Ubuntu 24.04 + Docker Engine 29.9.3): the clone, the `secrets/` layout, every
`docker-shell.sh` run (as written with `sh`, with `bash`, with the Dockerfile as committed and
without its Helm lines), the toolbox image and, typed at its prompt, **all six `ansible-playbook`
commands of the README, verbatim, in README order**. Each stops at its **honest first error**:
AWS's own `UnrecognizedClientException` / `AuthFailure` for the two playbooks that call AWS
(obviously fake placeholder keys), `Could not resolve hostname external_ip` for the three that SSH
to the server (there is none; `EXTERNAL_IP` is a placeholder where the console's address goes),
and, for the README's delete command, the playbook's own bug (`'dict object' has no attribute
'group_id'`) before any AWS call. The workflow's steps (not in the README) were run by hand on the
laptop up to their first real error. Console clicks, the server's side and the Actions run page are
`illustration`. The README documents **no command output at all**, so there is no `expected/`
folder and nothing is `recorded`: a scene that needs the server's or the cloud's answer describes
what to look for, without an output panel. No output was invented.

**Four findings change the tutorial today (2026-11-08); the video must say them kindly, with the fix:**

1. **`sh docker-shell.sh` (README:77) fails on Linux** — `docker-shell.sh: 13: Syntax error:
   redirection unexpected`, exit 2 (`laptop/23`): Ubuntu's (and Debian's) `/bin/sh` is `dash`
   (`laptop/24`), which has no `<<<`. On macOS `/bin/sh` is bash and the line works. Fix: `bash
   docker-shell.sh` (the script's own shebang, `docker-shell.sh:1`).
2. **The toolbox does not build as committed** — `Dockerfile:33`'s
   `curl https://baltocdn.com/helm/signing.asc` fails certificate verification, `gpg: no valid
   OpenPGP data found`, the `RUN` exits 2, and because `docker-shell.sh` has no `set -e` (`:4` is
   commented) it goes on to `docker run` an image that does not exist: `Unable to find image
   'cheese-app-deployment:latest' locally` … `not found`, exit 125 (`laptop/25`). The same check from the laptop itself, with Ubuntu 24.04's
   up-to-date CA store, fails the same way (`laptop/26`, `curl: (60)`): baltocdn.com is **not**
   re-signed by the recording proxy (it is passed through), and the certificate it serves on
   2026-11-08 chains to Let's Encrypt's new root "ISRG Root YR" (intermediate `YR1`, inspected with
   `openssl s_client` while capturing; not kept), which neither Ubuntu 24.04's nor 20.04's store
   contains. A machine whose store already trusts that root would get past this line; we could not
   test one. Helm's apt repository has also moved (the new `packages.buildkite.com/helm-linux/...`
   key URL answers `302`, `laptop/26`). No playbook uses Helm, so the capture (and the fix the video
   can suggest) deletes the two Helm lines and the word `helm` (`laptop/27`, git diff shown); with
   that the toolbox builds in 132.8 s (`laptop/28`).
3. **`pip install ansible>=9.0.0` (`Dockerfile:37`) is a shell redirect, not a pin** — the image
   holds a file named `/=9.0.0` with pip's log in it, and the toolbox has **ansible 6.7.0 /
   ansible-core 2.13.13 on Python 3.8.10** (`laptop/32`, `33`). Every Ansible command prints
   cryptography's `Python 3.8 is no longer supported` warning (crop it), and the newest
   `community.general` 14.0.0 that `Dockerfile:56` installs warns that it `does not support Ansible
   version 2.13.13` (`laptop/36`, `40`).
4. **The README's delete command deletes nothing** — `--extra-vars cluster_state=absent`
   (README:147) skips the security-group and EBS tasks, then the un-gated "Create EC2 instance" task
   fails on `security_group.group_id`, before any AWS call (`laptop/48`). Clean up in the console
   (digest §4 step 27).

Smaller ones, all captured: the README's CSV path (`../../../`) is not the script's (`../../../../`,
`laptop/21`); `SECRETS_DIR` has the same four `../` and the README does not mention it, so `/secrets`
is empty in the toolbox until it is fixed (`laptop/28` vs `31`); the account id is hard-coded
(`docker-shell.sh:17`, edited in `laptop/30`); the key pair has three names (`laptop/13`).

## Which commit

| repo | pinned | date, subject | how checked |
| --- | --- | --- | --- |
| [dlops-io/cheese-app-aws](https://github.com/dlops-io/cheese-app-aws) | `main` @ **`5950118b0ed97c12c799920846d3eb70b1a47385`** | 2024-11-21 18:27:08 −0500, "cleanup" | `git ls-remote` on 2026-11-08 (`laptop/01`): `HEAD` = `refs/heads/main` = `5950118`; only branch, no tags (`laptop/03`) |
| [dlops-io/cheese-app-v4](https://github.com/dlops-io/cheese-app-v4) | `main` @ `033f18713b9e1e7985a3080e85edab3ff01cefef` | the slides' GCP version | context only (digest §7): nothing is captured from it and no panel quotes it |

## `source/` — the tutorial's own files

Copied with `git show 5950118:<path>`, the repo's relative paths kept (`source/README.md`,
`source/src/deployment/Dockerfile`, …). Course material by the AC215 teaching staff (Harvard IACS),
used for study with the instructor's permission. Not copied: images and the frontend's pages
(`src/frontend-react/src/app`, `components`), `src/frontend-simple/`, the books and the newsletter
and podcast data, `.DS_Store` files.

**Masked values (series rule): every other byte is unchanged, and line numbers are the repo's.**

| file:line | at `5950118` | in the copy |
| --- | --- | --- |
| `src/deployment/docker-shell.sh:17` | the tutorial author's real-looking 12-digit AWS account id | `export AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"` |
| `src/deployment/inventory.yml:30` | the author's server's public IP | `<EXTERNAL_IP>:` |
| `src/deployment/inventory.yml:24` | a committed `NEXTAUTH_SECRET` value | `nextauth_secret: "<value not copied: see ASSETS.md>"` |
| `src/frontend-react/.env.production:3`, `.env.development:5` | the same kind of value | `NEXTAUTH_SECRET=<value not copied: see ASSETS.md>` |
| `src/vector-db/cli.py:125`, `:432` | the instructor's name (a book's "author", a test prompt) | `‹instructor›` |

| file | what a panel quotes from it |
| --- | --- |
| `README.md` | the whole tutorial (148 lines): goal (3-5), the empty "API's to enable" list inside an HTML comment (7-13), the policy JSON (22-44) + name (46), the IAM user and its three AWS-managed policies (48-50), access key "Third Party Service" → CSV (52), the `secrets/` tree (54-60), key pair `cheese-app-ac215-key-pair` (64), "Deployment Setup" bullets (67-72), "Deployment Steps" (74-77: the CSV line 76, `sh docker-shell.sh` 77), the three ECR repositories (79-85), the six playbook commands (89, 94, 102, 116, 141, 147), "get the IP address … update the appserver>hosts" (97), the key-line toggle (107-111), the server commands (120-132, "from the GCP console" 120), nginx (136-137), the URL (143). Headings at 92 and 99 still say "in GCP" |
| `.github/workflows/ci_cd_aws.yml` | 130 lines (the digest counts 131 with the final newline): name (1), trigger + `/run-` gate (3-9), echo steps (12-15), `configure-aws-credentials@v4` (18-23), STS + `s3 ls` (25-28), ECR login (30-33), toolbox build (41-44), `DOCKER_TAG` (46-50), build/tag/push the three app images (52-70), SSH key from `secrets.AWS_SSH_KEY` (72-90), debug listing (92-97), the `/run-deploy-app` gate (99-100) and the deployment container (101-130) |
| `src/deployment/Dockerfile` | `FROM ubuntu:20.04` (2), AWS CLI v2 (13-16), Docker CE (19-28), kubectl + Helm + Python + the unquoted `ansible>=9.0.0` (31-37), user `app` (39-42), `pipenv sync` (50-51), `ansible-galaxy collection install community.general community.kubernetes` (55-56), the commented `ENTRYPOINT` (62), `CMD ["/bin/bash"]` (64) |
| `src/deployment/docker-shell.sh` | 49 lines: `#set -e` (4), the CSV block (9-21, here-string at 13, account id 17 masked), `SECRETS_DIR` (26), `SSH_KEY_PATH` (27), the two build lines (31-32), `docker run` with the socket, the app folders, the AWS variables (35-48) |
| `src/deployment/inventory.yml` | 30 lines: the CI key line (4) and the local one (7), the env lookups (9-11), instance settings (14-23), secret (24, masked), `appserver` host (27-30, masked) |
| `src/deployment/deploy-docker-images.yml`, `deploy-create-instance.yml`, `deploy-provision-instance.yml`, `deploy-setup-containers.yml`, `deploy-setup-webserver.yml` | the five playbooks (59, 108, 297, 207, 37 lines; digest §4-§5 has the line map) |
| `src/deployment/nginx-conf/nginx/nginx.conf` | `listen 80` (25-27), `location ^~ /api/` → `proxy_pass http://api-service:9000/;` (35-44), `/` → `frontend:3000` (47-55) |
| `src/deployment/ansible.cfg`, `.docker-tag`, `.gitignore`, `Pipfile`, `Pipfile.lock`, `docker-entrypoint.sh`, `docker-entrypoint_working.sh` | `host_key_checking = False`; the committed tag `20241121211313`; the (empty) toolbox Pipfile; the two entrypoints the Dockerfile never runs |
| `src/api-service/{Dockerfile, Pipfile, Pipfile.lock, docker-shell.sh, docker-entrypoint.sh}`, `api/service.py`, `api/utils/{llm_utils, llm_rag_utils, llm_cnn_utils}.py` | the API image and its Bedrock models; `chromadb = "==0.5.18"` (`Pipfile:19`); the RAG connection and embedding call (digest G11-G12) |
| `src/vector-db/{Dockerfile, Pipfile, Pipfile.lock, docker-shell.sh, docker-entrypoint.sh, docker-compose.yml, cli.py}` | the loader the playbook runs once per deploy; `chromadb = "0.5.18"` (`Pipfile:14`), the compose file's `chromadb/chroma:0.5.18` (`docker-compose.yml:25`), `--download` / `--load` (`cli.py`, names masked as above) |
| `src/frontend-react/{Dockerfile, Dockerfile.dev, .env.production, .env.development, next.config.js, package.json}`, `src/services/{Common,DataService}.js` | the two-stage Next.js image; `NEXT_PUBLIC_BASE_API_URL=/api` (`.env.production:2`) read by `Common.js:2` |
| `LICENSE` | context only |

There is no Colab notebook for this lecture.

## `terminal/` — real terminal sessions

Captured **2026-11-08 01:13–01:20 UTC** by `terminal/capture.sh` (environment) and
`terminal/run_steps.sh` (the steps), one segment per call:
`bash assets/terminal/capture.sh setup pre secrets shell-a shell-b shell-c toolbox toolbox-b playbooks ci extras`.
Each command's output goes to its own file: the file starts with the command (`$ ...`), then the
output, then its exit status (`[exit N]`). Files whose name contains `-x-` are **extras** (not in
the README; checks the video uses, said as "this one isn't in the README"); the others are README
commands, run exactly as written.

Two kinds of file: **`step` files** (no terminal, plain output, stdin at EOF) and **toolbox files**
(`25`, `28`, `31`-`38`, `40`, `42`, `44`, `46`-`48`): `bash docker-shell.sh` in a real
pseudo-terminal (`ptyrun.py`, 160×50; `25`: 110×50), the build's TTY progress view as
its final screen, then each command typed at the toolbox prompt `root@<container id>:/app#`, then
`exit`. Each toolbox file therefore starts with a (mostly cached) build log: crop to the prompt. A
README command typed in the toolbox is the README's text, character for character. The container id
in the prompt changes on every run.

**Masking at capture time.** `run_steps.sh`'s `mask` filter replaces, in every file, the author's
account id with `YOUR_ACCOUNT_ID`, the author's server IP with `<EXTERNAL_IP>`, the committed
`NEXTAUTH_SECRET` with `<nextauth-secret>` and the instructor's name with `‹instructor›`. The values
are read at run time from the clone at the pinned commit, so neither script contains them. After
the capture a search of `assets/` for each of those values (and for `AKIA` and private-key headers)
found nothing. Where the committed inventory's server address appears (`35`), the file shows
`<EXTERNAL_IP>` (masked); after the README:97 edit (`43`) the inventory holds the placeholder host
name `EXTERNAL_IP` (no brackets), and the playbook outputs show that.

### Environment: `laptop/`

| | |
| --- | --- |
| machine | a privileged `ubuntu:24.04` container in its own network namespace, hostname `laptop`: **Ubuntu 24.04.5 LTS**, x86_64, `/bin/sh` → `dash` (`00`) |
| Docker | **Docker Engine 29.9.3** (client and engine) + buildx v0.38.1, from Docker's apt repository as docs.docker.com installs it on Ubuntu; started by hand (no systemd: capture-only) |
| tools | bash 5.2.21, git 2.43.0, curl 8.5.0, python3 (for `ptyrun.py` and `10`), openssh-client (for the throwaway key) |
| user | `student` (uid 1001) in the `docker` group; home = the README's parent folder: `~/cheese-app-aws` and `~/secrets` side by side (README:55-60, `12`) |
| AWS | **none**. `~/secrets/deployment-ac215-user_accessKeys.csv` has AWS's CSV header (`Access key ID,Secret access key`) and the obviously fake `PLACEHOLDER_NOT_A_REAL_ACCESS_KEY` / `PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000`, which AWS rejects. `~/secrets/cheese-app-ac215-key-pair.pem` is a 2048-bit RSA key generated at capture time by `ssh-keygen` for no account (`capture-only/11`), never written to the repository; its name is the README's (`:64`) |
| toolbox | `cheese-app-deployment`, built by `docker-shell.sh:32` from the tutorial's Dockerfile minus Helm (`27`): 2.52 GB on disk, 595 MB content (`29`). Inside: aws-cli **2.39.6** (its own Python 3.14.8), ansible **6.7.0** / ansible-core **2.13.13** on Python **3.8.10**, Docker CLI **28.1.1**, kubectl **v1.28.15**, no helm (`32`); collections amazon.aws 3.5.0, community.aws 3.6.0, community.docker 2.7.3, community.general 5.8.3 (bundled) and 14.0.0 (Dockerfile:56), community.kubernetes 2.0.1 (`38`) |

### Files, in README order

| file | README step | what it shows |
| --- | --- | --- |
| `00-x-env.txt` | — | date, OS, Docker 29.9.3, buildx, git, bash, `/bin/sh -> dash` |
| `01-x-ls-remote.txt` | — | `HEAD` = `refs/heads/main` = `5950118…`, nothing else |
| `02-x-clone.txt` | — (the README has no clone command) | `git clone https://github.com/dlops-io/cheese-app-aws.git` |
| `03-x-git-log.txt` | — | `5950118… 2024-11-21 18:27:08 -0500 cleanup`; branch `main` only, no tags (no author shown) |
| `04-x-ls.txt` | — | the repo's top level, `src/` (five services incl. `frontend-simple`), `src/deployment/` |
| `capture-only/ubuntu-20.04-base*.{Dockerfile,txt}` | — | the capture-only base (below) |
| `10-x-policy-json.txt` | "Setup AWS Keys" (README:19-46) | the README's policy JSON (lines 23-43) parses: `python3 -m json.tool` echoes it, exit 0 |
| `capture-only/11-throwaway-key.txt` | "Create AWS EC2 Key Pair" (:64) stand-in | `ssh-keygen … -f ~/secrets/cheese-app-ac215-key-pair.pem` (listing only, no key text) |
| `12-secrets-layout.txt` | README:54-60, 64 | `ls ~` → `cheese-app-aws  secrets`; the CSV (115 bytes) and the `.pem` (1675 bytes, `-rw-------`) in `secrets/` |
| `13-x-key-names.txt` | — (E5/G6) | `grep` for both names: README:64 says `cheese-app-ac215-key-pair`; `inventory.yml:4, 7, 16`, `docker-shell.sh:27`, `ci_cd_aws.yml:81, 85, 90, 107, 126` say `ac215_2024` |
| `14-x-chmod-pem.txt` | — (G7) | `chmod 400` on the key, `-r--------` |
| `20-cd-deployment.txt` | README:75 "Go to src/deployment folder" | `pwd` = `/home/student/cheese-app-aws/src/deployment`, `ls -a` |
| `21-x-as-cloned.txt` | — (before README:76's edit) | `bash docker-shell.sh` as cloned: `Error: AWS credentials file not found at ../../../../secrets/deployment-ac215-user_accessKeys.csv`, exit 1 (four `../` lead to `/home/secrets`) |
| `22-edit-csv-file.txt` | README:76 | the edit (sed is the editor), `docker-shell.sh:9-11` after it, and the CSV found at `../../../secrets/…` |
| `23-sh-docker-shell.txt` | **README:77, as written** | `docker-shell.sh: 13: Syntax error: redirection unexpected`, exit 2 |
| `24-x-which-sh.txt` | — | `/bin/sh -> dash`; the script's shebang `#!/bin/bash` (which `sh file` ignores) |
| `25-x-bash-docker-shell-as-committed.txt` | README:77 with `bash`, Dockerfile as committed | the build: layers 1-8 run (AWS CLI, Docker CE), `ERROR [ 9/15]`: `curl: (60) SSL certificate problem: unable to get local issuer certificate`, `gpg: no valid OpenPGP data found.`, `exit code: 2`; then `Unable to find image 'cheese-app-deployment:latest' locally` … `not found`, exit 125 |
| `26-x-helm-repo.txt` | — | the same `curl: (60)` for `https://baltocdn.com/helm/signing.asc` from the laptop itself (`000 20` = no HTTP code, verify result 20 "unable to get local issuer certificate"); Helm's new repository's key URL answers `302` |
| `27-x-drop-helm.txt` | — (fix, see finding 2) | `git diff Dockerfile`: the two baltocdn lines removed, `kubectl helm` → `kubectl` |
| `28-x-docker-shell.txt` | README:77 (`bash`, without Helm) | the full build, `Building 132.8s (20/20) FINISHED`, `naming to docker.io/library/cheese-app-deployment:latest`; at the prompt `ls -la /secrets` is **empty** (G4: `SECRETS_DIR` still has four `../`; Docker created an empty `/home/secrets` on the laptop for the mount) |
| `29-x-docker-images.txt` | — | `cheese-app-deployment:latest` 2.52 GB, and the base `ubuntu:20.04` |
| `30-x-edit-secrets-dir-account.txt` | — (G4, G5) | `SECRETS_DIR=$(pwd)/../../../secrets/` and `AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"` (`docker-shell.sh:10, 17, 26` after the edits) |
| `31-docker-shell.txt` | README:77 (the toolbox as a student uses it from here on; the build re-runs only the `ADD . /app` layer, 17.1 s) | `/secrets` now holds the CSV and the `.pem`; the variable names `AWS_ACCESS_KEY_ID`, `AWS_ACCOUNT_ID`, `AWS_DEFAULT_REGION`, `AWS_SECRET_ACCESS_KEY` (plus `AWS_CA_BUNDLE`: capture-only, from the base image, below) |
| `32-x-versions.txt` | — | versions above; `which helm` → nothing, exit 1 |
| `33-x-redirect-file.txt` | — (G1) | `ls /` shows `'=9.0.0'` next to `app`, `secrets`, `api-service`, `frontend-react`, `vector-db`; the file's first lines `Collecting ansible` / `Downloading ansible-6.7.0-…` and its last `Successfully installed … ansible-6.7.0 ansible-core-2.13.13 … boto3-1.37.38 …` |
| `34-x-sts.txt` | — | `aws sts get-caller-identity` → `An error occurred (InvalidClientTokenId) … The security token included in the request is invalid.` |
| `35-x-inventory-graph.txt` | — | `@all` → `@appserver` → the committed host (masked `<EXTERNAL_IP>`), `@ungrouped` |
| `36-x-syntax-check.txt` | — | `--syntax-check` passes for all five playbooks (`playbook: …`); `deploy-docker-images.yml` prints the `community.general.docker_image` redirect deprecation ("removed in community.general 18.0.0") |
| `37-x-list-tasks.txt` | — | `--list-tasks` of the five playbooks: create-instance 9 tasks, docker-images 11, provision-instance 38, setup-containers 25, setup-webserver 4 |
| `38-x-collections.txt` | — | the collections above |
| `40-deploy-docker-images.txt` | **README:89** | task "Login to AWS ECR": `aws: [ERROR]: An error occurred (UnrecognizedClientException) when calling the GetAuthorizationToken operation: The security token included in the request is invalid.` + `Error: Cannot perform an interactive login from a non TTY device` (docker login got an empty password); `failed=1`. No image is built |
| `41-x-docker-images.txt` | — | still only the toolbox and its base on the laptop |
| `42-create-instance.txt` | **README:94** | "Gathering Facts" ok; "Create security group": `AuthFailure … AWS was not able to validate the provided access credentials` (`DescribeSecurityGroups`, boto3 1.37.38); `failed=1` |
| `43-edit-appserver-host.txt` | README:97 (sed is the editor) | `inventory.yml:27-30` with the placeholder host `EXTERNAL_IP` |
| `44-provision-instance.txt` | **README:102** | "Gathering Facts" → `UNREACHABLE! … ssh: Could not resolve hostname external_ip: Name or service not known` |
| `45-switch-key-line.txt` | README:107-111 | `inventory.yml:3-8` after the toggle: line 4 commented, line 7 active |
| `46-setup-containers.txt` | **README:116** | same `UNREACHABLE!` at "Gathering Facts" |
| `47-setup-webserver.txt` | **README:141** | same |
| `48-delete-instance.txt` | **README:147** | "Create security group" and "Create EBS volume" `skipping`, "Create EC2 instance" `fatal: … The task includes an option with an undefined variable. The error was: 'dict object' has no attribute 'group_id'` … `line 40, column 7`; `ok=1 … failed=1 skipped=2` — before any AWS call |
| `49-x-git-status.txt` | — | the three files the student has changed: `Dockerfile`, `docker-shell.sh`, `inventory.yml` |

Every toolbox file's `[exit N]` is the toolbox shell's last status (the playbook's: 2 = a task failed, 4
= a host unreachable).

### The workflow, by hand: `laptop/50`-`53` (all extras)

`.github/workflows/ci_cd_aws.yml` is not in the README, and no Actions run is ours to show. These
run the workflow's own `run:` scripts on the laptop, on a fresh clone of the pinned commit in
`~/runner/cheese-app-aws` (what `actions/checkout` fetches), with the placeholder secrets and the
throwaway key where `${{ secrets.… }}` stand:

| file | workflow lines | what it shows |
| --- | --- | --- |
| `50-x-keyword-history.txt` | — | the repo's 39 commit subjects counted: `33 /run-deploy-app`, and one `\run-deploy-app` (a backslash: `contains(…, '/run-')` is false, so that push ran nothing) — the workflow was debugged by pushing |
| `51-x-ci-docker-tag.txt` | 46-50 | the timestamp tag written to `.docker-tag` and `$GITHUB_ENV` (a file on the runner): `DOCKER_TAG=20261108011909` |
| `52-x-ci-ssh-setup.txt` | 72-97 | `~/.ssh/config` and `~/.ssh/ac215_2024.pem` written, `chmod 600`, copied to `src/deployment/secrets/`; both listings |
| `53-x-ci-run-deployment-container.txt` | 99-130 | `Deploying with tag: …`; inside the toolbox `ls -la /root/.ssh` (root-owned, `700`/`600`), then the ECR login: `UnrecognizedClientException …` + `Cannot perform an interactive login from a non TTY device`; the `&&` chain stops, exit 1: neither playbook runs. The toolbox image is the one from `28`/`31` (without Helm); the runner would build it from the committed Dockerfile (`:41-44`), which fails as `25` shows if the runner's CA store lacks ISRG Root YR (not tested) |

**Not captured:** the job's `uses:` steps (`actions/checkout@v4`, `aws-actions/configure-aws-credentials@v4`),
`aws sts get-caller-identity` / `aws s3 ls` with the runner's credentials (they would print the
same `InvalidClientTokenId` as `34`), and the three app-image builds of `:52-70`. The README's own
route never builds them either (its build playbook stops at the ECR login, `40`), and the
sandbox's shared disk (5 GB free) could not hold the TensorFlow API image. Scenes show those steps
as workflow code panels.

### Local stand-ins for the server: `laptop/60`-`68` (all extras)

| file | what it shows |
| --- | --- |
| `60-x-chroma-latest.txt` | G10: `chromadb/chroma:latest` (the image `deploy-setup-containers.yml:151` runs; digest `sha256:1e0b73a1…` on 2026-11-08) reports version `"1.0.0"`; `/api/v1/heartbeat` → `{"error":"Unimplemented","message":"The v1 API is deprecated. Please use /v2 apis"} HTTP 410`; `/api/v2/heartbeat` → 200 |
| `61-x-chroma-0518.txt` | the pin the clients and `docker-compose.yml:25` use: `"0.5.18"`, `/api/v1/heartbeat` → 200 |
| `62-x-nginx-routes.txt` | the repo's `nginx.conf`, run as `deploy-setup-webserver.yml:23-35` runs it (`nginx:stable`, network `appnetwork`, the conf as `/etc/nginx/nginx.conf`, ports 80/443) in front of two stand-in containers named `api-service` (9000) and `frontend` (3000) that answer with the path they received: `/api/newsletters` → `api-service received /newsletters`, `/api/chat/llm` → `/chat/llm`, `/` and `/chat` → `frontend`; `/api` (no slash) → `HTTP 301` |
| `63-x-container-ls.txt` | README:122's command (without `sudo`, on the laptop): `nginx` with `0.0.0.0:80->80/tcp, 0.0.0.0:443->443/tcp`, the two stand-ins |
| `64-x-container-logs-nginx.txt` | README:125's command (without `sudo` and `-f`): nginx's start lines and the five requests |
| `65-x-exec-nginx.txt` | in the spirit of README:131 (non-interactive): `nginx version: nginx/1.30.6`, `/etc/nginx` |
| `66-x-run-it-no-tty.txt` | G13: `docker run --rm -it` with no terminal → `cannot attach stdin to a TTY-enabled container because stdin is not a terminal`, exit 1 |
| `67-x-system-prune.txt` | G14: `docker system prune -a` (the build playbook's last task) with stdin at EOF: the warning and `Are you sure you want to continue? [y/N]`, exit 0, nothing removed |
| `68-x-docker-images.txt` | the laptop's images at the end |

The stand-ins are not the app: the 172.x addresses in `64` are Docker's private bridge.

### What cannot run here, and how each is shown

| step | how the video shows it |
| --- | --- |
| IAM policy, user, access key, CSV download (README:15-60) | `illustration`: schematic console drawings (no screenshots, no logos) with the README's field values; `10` shows the JSON is valid; `12` shows the result on disk |
| EC2 key pair (README:62-64) | `illustration`; the throwaway key stands in on disk (`12`) |
| "API's to enable" (README:7-13) | nothing to run: the list is an HTML comment; one sentence |
| "Deployment Setup" (README:67-72) | code panel of `source/src/deployment/inventory.yml` (masked lines) |
| Create the three ECR repositories (README:79-85) | `illustration` (console) |
| What the six playbooks do when AWS accepts the keys | the captured first errors, then the playbooks' task lists (`37`) and code panels of their tasks; the result described ("look for `ok`/`changed` and `failed=0` in the PLAY RECAP"), no output panel |
| The instance's IP from the console (README:97) | `illustration`; `43` shows where it goes |
| SSH to the server and the server commands (README:120-132) | the commands shown verbatim; their local stand-in outputs (`63`-`65`) tagged `extra` and called a stand-in; never presented as the server's |
| `http://<External IP>/` (README:143) | `illustration` (schematic browser); `62` shows the routing for real, on the laptop |
| GitHub secrets, the push with `/run-deploy-app`, the Actions run page | `illustration` + workflow code panels; `50`-`53` for the parts that run by hand |
| Teardown in the console (not in the README) | `illustration` checklist with a GOLD cost tag; `48` shows why it is needed |

### Capture-only (not part of the tutorial)

- **`capture-only/ubuntu-20.04-base.Dockerfile`** (+ its build log): the sandbox reaches the
  internet through a TLS-intercepting proxy that also refuses plain http. `ubuntu:20.04` (the
  toolbox's base) was rebuilt with that proxy's CA (in `/usr/local/share/ca-certificates`, so the
  Dockerfile's own `apt-get install ca-certificates` keeps it), https apt sources and
  `SSL_CERT_FILE`/`PIP_CERT`/`REQUESTS_CA_BUNDLE`/`AWS_CA_BUNDLE`, and re-tagged under the same name,
  so the tutorial's Dockerfile builds unchanged. `AWS_CA_BUNDLE` therefore appears in `31`'s list of
  variable names; a student's toolbox does not have it. The CA does **not** explain finding 2:
  baltocdn.com is not intercepted.
- The laptop's proxy settings (`~/.docker/config.json` `proxies`, the daemon's `HTTPS_PROXY`), the
  relay container `l23-relay` (`proxy_relay.py`: the proxy listens on the host's loopback), and
  Docker Hub pulls through `mirror.gcr.io` (the sandbox's shared IPs hit Docker Hub's anonymous rate
  limit). None of these changes a command or a version a scene shows.
- `dockerd` started by hand in the laptop (no systemd in a container).
- `playbooks` starts with `git checkout -- inventory.yml` and `secrets` with `rm -f` of the
  throwaway key, so a re-run starts from the same state; neither is shown.
- `ptyrun.py`: runs a command in a pseudo-terminal, types the given lines at the expected prompts
  and prints the final screen.

When the capture was done, the laptop container, its Docker volume (all images above) and the relay
were removed (`capture.sh teardown`).

The two `.env.*` copies are tracked as `env.production` / `env.development` (`.gitignore` drops `.env.*`); `scenes/common.py` `_src` reads them under their real names.
