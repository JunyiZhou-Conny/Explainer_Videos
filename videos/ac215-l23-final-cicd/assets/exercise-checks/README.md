# Exercise checks · ac215-l23-final-cicd (2026-11-08, 02:25–02:40 UTC)

What was run to verify [`exercises.md`](../../exercises.md), beyond the captures in `assets/terminal/laptop/`, which the
answers cite directly (`laptop/NN`; provenance in [`ASSETS.md`](../../ASSETS.md)). The check scripts and their logs
are in [`logs/`](logs/). Every step in a log starts with its command (`$ …`) and ends with `[exit N]`, as in
`assets/terminal/run_steps.sh`; where a step pipes into `grep`, `cut` or `sed`, `[exit N]` is the last command's
status, and steps whose status matters print it themselves (`exit status: N`).

**No AWS account, no keys, no GitHub run.** As in the captures, nothing here created a cloud resource or reached an AWS
API: every check that runs tutorial files ran with `--network none`, and the only AWS values are the captures'
obviously fake `PLACEHOLDER_NOT_A_REAL_…` keys and the account placeholder `YOUR_ACCOUNT_ID`. The SSH keys are
throwaway keys made inside a disposable container and never printed. The "server" in the SSH checks is a stand-in
`sshd` on `127.0.0.1` inside the same container, reached under the placeholder host name `EXTERNAL_IP` (as
`laptop/43` writes it into the inventory); the nginx checks use stand-ins for `api-service` and `frontend`, as
`laptop/62` does. No log contains a person's name, a key, a real account id or a public IP address.

## Setup (disposable; nothing from the repository ran on the host)

- The repository: `dlops-io/cheese-app-aws` at `5950118b0ed97c12c799920846d3eb70b1a47385`, still the head of `main`
  (`git ls-remote` on 2026-11-08, before these checks). The tutorial files are the unchanged copies in
  [`../source/`](../source/), mounted **read-only**; each check works on a copy inside its container.
- Docker Engine 29.8.2 on the session machine. Base images pulled from `mirror.gcr.io/library/`: `ubuntu:24.04` (the
  captures' laptop OS), `python:3.8-slim`, `python:3.12-slim`, `nginx:stable` (nginx 1.30.6, as `laptop/65`) and
  `docker:29-cli`.
- [`setup.sh`](logs/setup.sh) ([`setup.log`](logs/setup.log)) builds the check-only image `l23ex-ansible:check` from
  [`ansible-check.Dockerfile`](logs/ansible-check.Dockerfile): Python 3.8 with **ansible 6.7.0 / ansible-core
  2.13.13** (the toolbox's versions, `laptop/32`, `33`), amazon.aws 3.5.0, community.aws 3.6.0, community.docker 2.7.3
  (as `laptop/38`), boto3/botocore 1.37.38 (as `laptop/42`), and OpenSSH 9.2 client and server. The session proxy's CA
  is added only so pip and apt can download; it plays no part in any check. This image is **not** the tutorial's
  toolbox (its build needs the Helm fix and 2.5 GB); it has the same Ansible, collections and boto3.
- [`lib.sh`](logs/lib.sh): the `step` function. [`edit.py`](logs/edit.py): makes the edited copies the checks run
  (a playbook made of the provision playbook's lines 54-57, the inventory with README:107-111's switch, the delete
  playbook with one and with two fixes). [`teardown-fixed.yml`](logs/teardown-fixed.yml): the four delete tasks of B5.

## Checks

| exercise | script → log | what was run | result |
| --- | --- | --- | --- |
| Q2, B4, C1 | [`shell-run.sh`](logs/shell-run.sh) → [`shell-in.sh`](logs/shell-in.sh) ([`shell.log`](logs/shell.log)) | `ubuntu:24.04`, `--network none`; the README's folders (`~/cheese-app-aws`, `~/secrets` with a placeholder CSV), README:76's edit; `docker` replaced by a stand-in script that prints its arguments (and fails a build on request) | `sh docker-shell.sh`: `docker-shell.sh: 13: Syntax error: redirection unexpected`, exit status 2; `bash`: reaches `docker build` and `docker run`, the `/secrets` mount still `…/src/deployment/../../../../secrets/`; `dash -c` with `<<<`: syntax error; `bash --posix -c` with `<<<`: works (`a=key b=secret`); started from the repository root: `Error: AWS credentials file not found at ../../../secrets/deployment-ac215-user_accessKeys.csv`, exit status 1; a failing build without `set -e`: `docker run` still runs, exit status 0; with line 4 uncommented: stops after the build, exit status 1; `echo pip install ansible>=9.0.0 openshift docker` writes a 37-byte file `=9.0.0` holding `pip install ansible openshift docker`; quoted, it prints the line and makes no file |
| Q2, B1, C7 | [`pip-run.sh`](logs/pip-run.sh) ([`pip.log`](logs/pip.log)) | `python:3.8-slim` (3.8.20): `pip install --dry-run` (nothing installed); `python:3.12-slim` with ansible-core 2.17.14 running the provision playbook's lines 54-57 | unpinned `ansible` on Python 3.8 → `['6.7.0']`; `"ansible>=9.0.0"` → `ERROR: No matching distribution found for ansible>=9.0.0` (`8.7.0 Requires-Python >=3.9`, `9.0.1 Requires-Python >=3.10`); ansible-core 2.17: `Unsupported parameters for (ansible.legacy.command) module: warn` (the same lines on 2.13.13: `changed`, in `ansible.log`) |
| B2, Q4 | [`ansible-run.sh`](logs/ansible-run.sh) → [`ansible-in.sh`](logs/ansible-in.sh) ([`ansible.log`](logs/ansible.log)) | the exact commands of B2: a play made of `deploy-setup-containers.yml:101-118`, run three times | no `DOCKER_TAG`: `Using docker tag: 20241121211313` (the committed `.docker-tag`); `DOCKER_TAG=20261108011909`: that tag, the file tasks skipped; the same plus `--extra-vars docker_tag=20261108020000`: `20261108020000` (extra vars beat `set_fact`) |
| C3, C4, C5 | same | `ansible appserver -m ping` against the stand-in `sshd` (user `ubuntu`, only the throwaway key authorized), Ansible's SSH connection sharing turned off so every run opens a fresh connection | inventory as committed (line 4, key in `/root/.ssh` missing): `UNREACHABLE!` … `no such identity: /root/.ssh/ac215_2024.pem: No such file or directory` … `Permission denied (publickey,password)`; line 7 active, key `/secrets/ac215_2024.pem` mode 600: `pong`; the same key mode 644: `WARNING: UNPROTECTED PRIVATE KEY FILE!` … `Permissions 0644 for '/secrets/ac215_2024.pem' are too open.` … `Permission denied`; line 7 with no `AWS_SSH_KEY` resolves to `/secrets/ac215_2024.pem`; the CI shape (key only in `/root/.ssh`, no `/secrets`) with line 7 still active: `no such identity: /secrets/ac215_2024.pem` … `Permission denied`; with line 4: `pong` |
| Ponder 5, B5 | same | the README's delete; then a copy with `when: cluster_state == "present"` on "Create EC2 instance"; then a copy with the four tasks of `teardown-fixed.yml` | as `laptop/48`: `'dict object' has no attribute 'group_id'`, `ok=1 … failed=1 skipped=2`; with the `when:`: six tasks skipped, then "Remove EBS volume": `'dict object' has no attribute 'volume_id'`; fixed: `--syntax-check` passes, and the first task that runs is "Terminate EC2 instance", which fails only because the container has no network (`botocore.exceptions.EndpointConnectionError: Could not connect to the endpoint URL`); amazon.aws 3.5.0's `ec2_vol` writes `tags['Name'] = name` when it creates a volume (lines 513, 861), so the lookup by Name tag finds `cheese-app-demo-disk` |
| Ponder 2, B3, C6 | [`nginx-run.sh`](logs/nginx-run.sh) ([`nginx.log`](logs/nginx.log)) | the repo's `nginx.conf` in `nginx:stable` (1.30.6) on a private network with the two stand-ins; requests from a client container; no port published on the host | as committed: `api-service received /newsletters`, `frontend received /`, `/api` → `HTTP 301 -> http://l23ex-nginx/api/`; without the trailing `/` in `proxy_pass`: `api-service received /api/newsletters`, `… /api/chat/llm`; with no `api-service` running: `nginx: [emerg] host not found in upstream "api-service" in /etc/nginx/nginx.conf:37`, exit status 1 |
| Ponder 1, Q3, B4, B6 | [`socket-run.sh`](logs/socket-run.sh) ([`socket.log`](logs/socket.log)) | `docker:29-cli` with the host's socket mounted, as `docker-shell.sh:36` mounts it; a two-line `FROM scratch` image; then a build that fails | inside: no `dockerd` process, the same engine name and ID as the host's; the image built inside is listed **on the host**; `docker ps` inside lists the container itself; after a failing rebuild (exit status 1) the tag still points at the earlier image (label `v=1`), and `docker run` starts it |
| Q5, Ponder 3, B7 | [`trigger.py`](logs/trigger.py) ([`trigger.log`](logs/trigger.log)) | reads the two `contains()` conditions from `ci_cd_aws.yml` (lines 9 and 100) and applies GitHub's documented rule for `contains()` on strings (case-insensitive substring) to seven messages | `update readme` and `\run-deploy-app`: job skipped; `fix typo /run-tests` and `deploy /run-deploy`: build and push only; `/run-deploy-app`, `/RUN-DEPLOY-APP`, `redeploy: /run-deploy-app-now`: both run. **A model of the documented rule, not a GitHub run** |

## Not run (and why)

- **Everything that needs AWS**: ECR, EC2, the security group and volumes, what the fixed delete (B5) does against a
  real account, Bedrock, the instance-metadata hop limit (D1). Answers about them cite the code at `5950118`, the
  captures' honest first errors and AWS's documentation, and say so.
- **GitHub Actions**: no workflow run was possible (no repository of ours, no secrets). The trigger table (B7) applies
  GitHub's documented `contains()` rule to the file's own conditions; `head_commit` (the last commit of a push) and
  the runner's behaviour are from GitHub's documentation.
- **The tutorial's own toolbox image**: not rebuilt for the checks (2.5 GB, and its Helm step fails as `laptop/25`
  shows). `l23ex-ansible:check` carries the same Ansible, collections and boto3; the toolbox's own outputs are the
  captures `laptop/28`-`48`.
- **macOS**: that `/bin/sh` on a Mac runs bash is Apple's documented default, not run here; the check shows only that
  bash in POSIX mode accepts `<<<`.
- **An Ubuntu server's SSH answer**: the stand-in `sshd` (Debian's defaults) offers `publickey,password`; a stock EC2
  Ubuntu image disables password logins, so a real server says `Permission denied (publickey)`. Not run.

## Cleanup

Every check container ran with `--rm` or was removed by name (`l23ex-…`), and the network `l23ex-net` was removed. The
images built for these checks (`l23ex-ansible:check`, and `l23ex-sibling:check` / `l23ex-tb:latest`, removed inside
their scripts) and the base images pulled for them (`mirror.gcr.io/library/…`: `ubuntu:24.04`, `python:3.8-slim`,
`python:3.12-slim`, `nginx:stable`, `docker:29-cli`) were removed afterwards, each by name. The temporary files the
scripts made (`mktemp`) were deleted by path. Nothing was written outside the containers and this folder.
