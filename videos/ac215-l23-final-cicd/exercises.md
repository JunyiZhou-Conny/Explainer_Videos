# Exercises · AC215 L23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys

Do these after watching, **without** re-watching first. Re-watch only the chapter you got wrong
(chapter times are in `output/chapters.txt`). Outputs quoted below are real: the captures of
2026-11-08 (`assets/terminal/laptop/NN`: a fresh Ubuntu 24.04 laptop with Docker Engine 29.9.3,
the tutorial's toolbox built from its own Dockerfile minus the Helm lines, **no AWS account**, keys
that are obviously fake placeholders; provenance in [`ASSETS.md`](ASSETS.md)), and the extra checks
run for these exercises, listed with their scripts and logs in
[`assets/exercise-checks/`](assets/exercise-checks/README.md). The repository is
`dlops-io/cheese-app-aws` at `5950118` (`main`, its only branch); `README:NN` means line NN of its
README, `ci_cd_aws.yml:NN` a line of `.github/workflows/ci_cd_aws.yml`, and other paths are under
`src/deployment/` unless they say otherwise. Nothing here touched AWS or ran on GitHub: whatever only
AWS or GitHub can show is answered from the code at the pinned commit and from AWS's or GitHub's
documentation, and the answer says so. Account ids, keys and server addresses are placeholders
(`YOUR_ACCOUNT_ID`, `<aws-access-key-id>`, `<EXTERNAL_IP>`). Versions are those at the time of
recording; yours may be newer. The lecture's slides speak Google Cloud; where a question uses the
lecture's words, the answer maps them onto this AWS repository, as the video does.

---

## Part A · The five questions from the end of the video

**Q1. Name the two secrets, what each opens, and three places the access key ends up after one
deploy. What would an instance role and GitHub OIDC remove?**

<details><summary>Answer</summary>

- **The IAM access key** (the "badge"): the CSV `deployment-ac215-user_accessKeys.csv` (README:52-60).
  It signs calls to the **AWS API**: ECR logins and pushes, creating the security group, the volume and
  the instance, and the API container's Bedrock calls.
- **The EC2 key pair's private key** (the "key"): the `.pem` file (README:64). It opens **SSH** to the
  server as `ubuntu` (`inventory.yml:3-7`), which every `hosts: appserver` play needs. It cannot call
  the AWS API, and the access key cannot open SSH.

Where the access key ends up after one deploy by hand and one by CI:

1. **Your laptop**: `~/secrets/` (outside the clone, README:54-60), then the toolbox's environment
   (`docker-shell.sh:13-15`, `:43-46`), where `inventory.yml:9-11` reads it.
2. **The server**, three times: the root user's AWS configuration (`aws configure set …` in
   `deploy-provision-instance.yml:288-292`, a play with `become: true`, `:4`); the file
   `/srv/secrets/aws-credentials`, mode 0600 (`deploy-setup-containers.yml:36-44`), mounted into
   `api-service` at `/secrets` (`:194`); and the environment of `api-service` (`:184-186`) and of the
   loader (`:166-168`), which anyone allowed to run `docker inspect` on the server can read.
3. **GitHub**: the repository secrets `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`
   (`ci_cd_aws.yml:21-22`, `:102-103`), and the runner's environment during every run.

An **instance role** removes the server's copies: the AWS CLI and boto3 on the server (and in its
containers) would get short-lived credentials from the instance itself, so `aws configure`, the
credentials file and the `-e`/`env:` key lines go away. **GitHub OIDC** removes the two key secrets
on GitHub: `configure-aws-credentials` would assume a role with a token GitHub issues for each run.
Neither removes the `.pem` (still a secret, `AWS_SSH_KEY`) or your laptop's CSV (D1 goes further).
Both are AWS's and GitHub's documented patterns; neither is in this repository, and neither was run
here.
</details>

**Q2. Why does `sh docker-shell.sh` fail on Ubuntu but work on a Mac? And what did the unquoted
`pip install ansible>=9.0.0` actually do?**

<details><summary>Answer</summary>

- `sh docker-shell.sh` asks **`/bin/sh`** to read the file; the shebang `#!/bin/bash`
  (`docker-shell.sh:1`) only counts when you run the file itself (`./docker-shell.sh`). On Ubuntu and
  Debian `/bin/sh` is **dash** (`laptop/24`: `/bin/sh -> dash`), which has no here-string `<<<`, the
  bash feature line 13 uses to split the CSV's second line. dash stops before running anything:
  `docker-shell.sh: 13: Syntax error: redirection unexpected`, exit 2 (`laptop/23`; again in
  [`shell.log`](assets/exercise-checks/logs/shell.log)). On macOS `/bin/sh` runs bash by default
  (Apple's documented setup, not run here), and bash accepts `<<<` even in its POSIX mode
  (`bash --posix` prints `a=key b=secret` in the same log). On Linux, type `bash docker-shell.sh`.
- In a Dockerfile `RUN` line the command goes through `/bin/sh -c`, and an unquoted `>` is an
  **output redirect**: the shell ran `pip install ansible openshift docker apache-libcloud boto3
  botocore pipenv` with pip's output sent to a file named `=9.0.0` in `/` (the build's working folder
  at that point; `WORKDIR /app` comes later, `Dockerfile:46`). The toolbox has that file
  (`laptop/33`: `'=9.0.0'` in `ls /`, starting `Collecting ansible`), and pip installed an
  **unpinned** Ansible: the newest release that supports the base image's Python 3.8, **ansible
  6.7.0 / ansible-core 2.13.13** (`laptop/32`; `pip install --dry-run ansible` on Python 3.8 →
  `['6.7.0']`, [`pip.log`](assets/exercise-checks/logs/pip.log)). The same redirect, replayed with
  `echo`, writes `pip install ansible openshift docker` into `=9.0.0` (`shell.log`).
- Quoting it, `"ansible>=9.0.0"`, would not get you Ansible 9 on this image: pip answers `ERROR: No
  matching distribution found for ansible>=9.0.0` (ansible 9.0.1 requires Python ≥ 3.10, `pip.log`),
  so the build would stop. A newer base image would work, but brings an ansible-core that rejects the
  provision playbook's `args: warn: false` (`deploy-provision-instance.yml:56-57`): ansible-core 2.17
  says `Unsupported parameters for (ansible.legacy.command) module: warn` (`pip.log`; the same lines
  run on 2.13.13, `ansible.log`). That's why the video leaves the line alone for this lecture.
</details>

**Q3. Where do the tasks of a `hosts: localhost` play run, and of a `hosts: appserver` play? And why
can the toolbox fill the disk of your laptop?**

<details><summary>Answer</summary>

- **`hosts: localhost`** (`deploy-docker-images.yml:2`, `deploy-create-instance.yml:2`): **inside the
  toolbox**, which is Ansible's controller. Its `shell:` tasks run there (the ECR login, `date`), its
  AWS modules call the AWS API from there with boto3 (security group, volume, instance), and its
  Docker modules talk to a Docker engine from there.
- **`hosts: appserver`** (`deploy-provision-instance.yml:2`, `deploy-setup-containers.yml:2`,
  `deploy-setup-webserver.yml:2`): **on the server**. Ansible connects over SSH as `ubuntu` with the
  `.pem` (`inventory.yml:3-7`), becomes root (`become: true`), and runs each module there. Lookups such
  as `lookup('env', …)` still run on the controller, the toolbox (that's how the server gets your keys,
  Q4 and C5).
- **The disk**: there is no Docker engine in the toolbox. `docker-shell.sh:36` mounts your laptop's
  socket, `/var/run/docker.sock`, so every Docker call from the toolbox, including the playbook's
  three image builds (`deploy-docker-images.yml:18-56`), is carried out by **your laptop's engine**
  and the images land on your laptop's disk, beside the toolbox image itself (2.52 GB, `laptop/29`).
  Checked with a CLI-only container and the socket ([`socket.log`](assets/exercise-checks/logs/socket.log)):
  no `dockerd` inside, the same engine ID as the host, and the image it built is listed on the host.
  The same is why the playbook's last task, `docker system prune -a` (`:59-60`), would sweep **your
  laptop's** unused images if it ever got a "y" (it doesn't, `laptop/67`).
</details>

**Q4. Follow one timestamp from `date` to a running container. Where is it written down, and how
does the server choose between `DOCKER_TAG` and `.docker-tag`?**

<details><summary>Answer</summary>

**By hand (part 1):** "Get timestamp for docker tag" runs `date +%Y%m%d%H%M%S` in the toolbox and
registers it as `tag` (`deploy-docker-images.yml:11-13`) → it names the three images
`YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com/cheese-app-…:<tag>` (`:23`, `:36`, `:49`), which are
pushed to ECR (`:25-56`) → "Save docker tag" writes it to `.docker-tag` (`:57-58`) in `/app`, which is
your clone's `src/deployment` (so the file in your clone changes) → `deploy-setup-containers.yml` copies
`.docker-tag` to the server (`:67-71`) → picks the tag (`:101-114`) → pulls the three images at that
tag (`:120-129`) → recreates `frontend` and `api-service` from them (`recreate: yes`, `:136`, `:180`)
and runs the loader once with the vector-db image (`:164-173`).

**By CI (part 2):** the runner writes `date +%Y%m%d%H%M%S` to `.docker-tag` and appends
`DOCKER_TAG=…` to `$GITHUB_ENV`, a file GitHub reads between steps (`ci_cd_aws.yml:46-50`;
`laptop/51`: `DOCKER_TAG=20261108011909`) → `docker tag …:${{ env.DOCKER_TAG }}` and `docker push`
(`:57-70`) → the deploy step's `env:` (`:106`) → `-e DOCKER_TAG` into the toolbox (`:121`) and
`--extra-vars "… docker_tag=$DOCKER_TAG"` (`:130`).

**Written down:** in `.docker-tag` (your clone, or the runner's workspace, and the copy on the
server), in `$GITHUB_ENV` on the runner, as the image tags in ECR, and in the IMAGE column of
`sudo docker container ls` on the server (README:122).

**The choice:** `lookup('env', 'DOCKER_TAG')` is evaluated in the **toolbox**. If `DOCKER_TAG` is set
there and not empty, `set_fact` takes it (`:101-104`); otherwise the play runs `cat .docker-tag` on the
server and takes that (`:106-114`). Your laptop's toolbox never has `DOCKER_TAG` (`docker-shell.sh:43-47`),
so a run by hand uses the file; CI sets it. And in CI the tag also arrives as an extra variable, which
outranks `set_fact`. Run with the playbook's own lines 101-118
([`ansible.log`](assets/exercise-checks/logs/ansible.log)): no variable → `Using docker tag:
20241121211313` (the committed file); `DOCKER_TAG=20261108011909` → that tag; the same plus
`--extra-vars docker_tag=20261108020000` → `20261108020000`. In CI all three hold the same value.
</details>

**Q5. Which of these deploy: `update readme`, `fix typo /run-tests`, `/RUN-DEPLOY-APP`,
`\run-deploy-app`? In the lecture's words, is this pipeline continuous delivery or continuous
deployment?**

<details><summary>Answer</summary>

Two sieves read the same string, the message of the push's **last** commit
(`github.event.head_commit.message`): the job runs only if it contains `/run-` (`ci_cd_aws.yml:9`),
and the last step, "Run Deployment Container", only if it also contains `/run-deploy-app` (`:100`).
GitHub documents `contains()` on strings as **case-insensitive**.

| message | job (build and push three images) | deploy step | the server |
| --- | --- | --- | --- |
| `update readme` | skipped | — | unchanged; nothing runs |
| `fix typo /run-tests` | runs | skipped | unchanged, on the old tag; three new images in ECR, billed as storage |
| `/RUN-DEPLOY-APP` | runs | runs | **redeployed** (the match ignores case) |
| `\run-deploy-app` | skipped | — | unchanged: a backslash, so `/run-` is not in it |

Only `/RUN-DEPLOY-APP` deploys. ([`trigger.log`](assets/exercise-checks/logs/trigger.log) applies the
documented rule to the file's own two conditions; it is a model, not a GitHub run.) The fourth is a
real commit of this repository (`laptop/50`: `1 \run-deploy-app` next to `33 /run-deploy-app`).

In the lecture's words (slides 11-12) it is **continuous delivery**: a person decides each release by
typing the keyword; continuous deployment would ship every change by itself. Strictly, it is
delivery without the CI half in front: the workflow is named "Continuous Integration and Continuous
Deployment" (`ci_cd_aws.yml:1`) but runs no test, so nothing has proved the change "ready to
release" when you press the button. D2 turns it into continuous deployment.
</details>

### The five ponders

**Ponder 1 (whose disk).** Inside the toolbox, Ansible runs `docker build` for the frontend. Whose
disk does the image land on: the toolbox's or your laptop's?
<details><summary>Answer</summary>

Your laptop's. The toolbox has the Docker CLI but no engine; the socket mount (`docker-shell.sh:36`)
sends the build to your laptop's engine, so the image is a **sibling** of the toolbox, not inside it.
Checked with a CLI-only container: the image it built shows up in the host's `docker images`, and
`docker ps` inside lists the container itself
([`socket.log`](assets/exercise-checks/logs/socket.log)). See Q3.
</details>

**Ponder 2 (the trailing slash).** The browser asks nginx for `/api/newsletters`. Which path does
`api-service` receive?
<details><summary>Answer</summary>

`/newsletters`. `location ^~ /api/` matches (`nginx.conf:35`), and because
`proxy_pass http://api-service:9000/;` (`:37`) ends with a path (`/`), nginx replaces the matched
prefix `/api/` with it. FastAPI mounts its routers without the prefix, so they fit. Captured with
stand-ins (`laptop/62`: `api-service received /newsletters`), and again in
[`nginx.log`](assets/exercise-checks/logs/nginx.log), where `/api` without its last slash gets
`HTTP 301 -> …/api/`. B3 removes the slash.
</details>

**Ponder 3 (`/run-tests`).** You push `fix typo /run-tests` to `main`: nothing, build-and-push only,
or a full deploy?
<details><summary>Answer</summary>

Build-and-push only. The message contains `/run-` (first sieve, `ci_cd_aws.yml:9`), so the runner
builds the toolbox and the three app images and pushes them to ECR with a new tag (`:41-70`); it does
not contain `/run-deploy-app` (second sieve, `:100`), so "Run Deployment Container" is skipped and the
server keeps the old tag. Every such push adds three images to ECR, and nothing deletes old tags.
</details>

**Ponder 4 (delivery or deployment).** By the lecture's definitions, is typing `/run-deploy-app`
continuous delivery or continuous deployment? What would make it the other?
<details><summary>Answer</summary>

Continuous delivery: a person presses "release" by typing the keyword (slide 12's red button). It
becomes continuous deployment when every change merged into `main` deploys by itself, behind the tests
of Lecture 21: trigger on every push to `main`, a test job, and the deploy job `needs:` it, with no
keyword. That is what Milestone 5 asks for (D2 has the edits).
</details>

**Ponder 5 (`cluster_state=absent`).** Which of the first three tasks of `deploy-create-instance.yml`
run?
<details><summary>Answer</summary>

"Create security group" and "Create EBS volume" are **skipped** (`when: cluster_state == "present"`,
lines 24 and 37). "Create EC2 instance" has **no** `when:` (lines 40-61), so it runs, and fails while
filling in its arguments: the skipped task registered `security_group` without a `group_id`, so
`security_group.group_id` (line 45) is undefined: `'dict object' has no attribute 'group_id'`,
`ok=1 … failed=1 skipped=2`, before any AWS call (`laptop/48`; again in
[`ansible.log`](assets/exercise-checks/logs/ansible.log)). Nothing is deleted. B5 fixes it.
</details>

---

## Part B · Hands-on (predict, then run)

**B1. Where did the pin go?** In your toolbox (`bash docker-shell.sh`, after the video's fixes),
predict what these print, then run them:

```bash
ls /
head -3 "/=9.0.0"; tail -1 "/=9.0.0" | cut -c1-120
ansible --version | head -1
```

Then predict what `pip install "ansible>=9.0.0"` (quoted) would do in the same image.

<details><summary>Answer</summary>

`ls /` lists a file `'=9.0.0'` beside `app`, `secrets`, `api-service`, `frontend-react` and
`vector-db` (the last three are your mounts). It holds pip's log: `Collecting ansible`, `Downloading
ansible-6.7.0-py3-none-any.whl (42.8 MB)`, …, and finally `Successfully installed … ansible-6.7.0
ansible-core-2.13.13 …`. `ansible --version` says `ansible [core 2.13.13]` (`laptop/32`, `33`). Each
Ansible command also prints cryptography's `Python 3.8 is no longer supported` warning, because pip
here is Python 3.8's (Ubuntu 20.04's `python3`). Quoted, pip finds no Ansible 9 for Python 3.8 and
stops: `ERROR: No matching distribution found for ansible>=9.0.0` (ansible 8.7.0 needs Python ≥ 3.9,
9.0.1 needs ≥ 3.10; [`pip.log`](assets/exercise-checks/logs/pip.log)). In a Dockerfile that error ends
the build, which is better than a silent wrong version, but it doesn't give you Ansible 9 (Q2).
</details>

**B2. Which tag will the server use?** The tag choice in `deploy-setup-containers.yml:101-118`
only needs core Ansible, so you can run those exact lines in your toolbox, on `localhost`. At the
toolbox prompt (in `/app`):

```bash
{ printf -- '- hosts: localhost\n  connection: local\n  gather_facts: false\n  tasks:\n'; sed -n '101,118p' deploy-setup-containers.yml; } > tagbook.yml
cat .docker-tag
ansible-playbook tagbook.yml
DOCKER_TAG=20261108011909 ansible-playbook tagbook.yml
DOCKER_TAG=20261108011909 ansible-playbook tagbook.yml --extra-vars docker_tag=20261108020000
rm tagbook.yml
```

Predict the last line of each run (`Using docker tag: …`) and which tasks say `skipping`.

<details><summary>Answer</summary>

1. No `DOCKER_TAG`: the environment task is skipped, the file block runs: `Using docker tag:
   20241121211313`, the committed `.docker-tag` (or your own tag, if a real step 5 already wrote it).
2. `DOCKER_TAG=20261108011909`: the environment task runs, both file tasks are skipped: `Using docker
   tag: 20261108011909`.
3. The same plus `--extra-vars docker_tag=20261108020000`: the tasks run as in 2, yet the result is
   `Using docker tag: 20261108020000`. Extra variables have the highest precedence in Ansible, so
   `set_fact` cannot override them. That's CI's case (`ci_cd_aws.yml:130`), where both carry the same
   tag anyway.

Run exactly like this in a container with the toolbox's Ansible 6.7.0 / core 2.13.13
([`ansible.log`](assets/exercise-checks/logs/ansible.log)). On the real server the file is read
there (`cat .docker-tag` in an `appserver` play); here, on `localhost`, it's the toolbox's copy.
</details>

**B3. Take away nginx's trailing slash.** Run the repository's `nginx.conf` on your laptop in front
of two stand-ins that answer with the path they receive, as the video's capture did. From
`src/deployment` (a second laptop terminal, not the toolbox):

```bash
docker network create l23-try
for s in api-service:9000 frontend:3000; do
  docker run -d --name try-${s%%:*} --network l23-try --network-alias ${s%%:*} python:3.12-slim python -c "
import http.server
class H(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        b = ('${s%%:*} received ' + self.path + '\n').encode()
        self.send_response(200); self.send_header('Content-Length', str(len(b))); self.end_headers(); self.wfile.write(b)
http.server.HTTPServer(('', ${s##*:}), H).serve_forever()"
done
docker run -d --name try-nginx --network l23-try -v "$(pwd)/nginx-conf/nginx/nginx.conf":/etc/nginx/nginx.conf:ro nginx:stable
docker run --rm --network l23-try nginx:stable curl -s try-nginx/api/newsletters
```

Then make a copy without the slash, `sed 's|api-service:9000/;|api-service:9000;|'
nginx-conf/nginx/nginx.conf > /tmp/nginx-no-slash.conf`, replace `try-nginx` with one that mounts the
copy, and ask again. Predict both answers. Clean up with `docker rm -f try-nginx try-api-service
try-frontend && docker network rm l23-try`.

<details><summary>Answer</summary>

As committed: `api-service received /newsletters`. Without the slash: `api-service received
/api/newsletters` (and `/api/chat/llm` for `/api/chat/llm`): with no path in `proxy_pass`, nginx
passes the request's path unchanged ([`nginx.log`](assets/exercise-checks/logs/nginx.log), nginx
1.30.6). The real API mounts its routers at `/newsletters`, `/podcasts`, `/llm`, `/llm-rag`, …, without
`/api` (`src/api-service/api/service.py:25-30`), so every API call from the site would get a 404 from
FastAPI. The trailing slash is what makes the frontend's
`NEXT_PUBLIC_BASE_API_URL=/api` (`src/frontend-react/.env.production:2`) and the API fit together.
</details>

**B4. A build that fails, with and without `set -e`.** Make the toolbox build fail on purpose and run
the script twice. In `src/deployment` on your laptop:

```bash
cp Dockerfile /tmp/Dockerfile.bak && cp docker-shell.sh /tmp/docker-shell.sh.bak
echo 'RUN false' >> Dockerfile
bash docker-shell.sh                       # predict: what starts, if anything?
sed -i '4s/^#set -e/set -e/' docker-shell.sh
bash docker-shell.sh; echo "exit $?"       # predict again
cp /tmp/Dockerfile.bak Dockerfile && cp /tmp/docker-shell.sh.bak docker-shell.sh
```

<details><summary>Answer</summary>

Without `set -e` (line 4 is commented out as committed) the script ignores the failed `docker build`
and goes on to `docker run cheese-app-deployment`. If you built the toolbox earlier, the tag still
points at that **earlier** image and you get a prompt in an old toolbox without noticing; if you
never built it, `Unable to find image 'cheese-app-deployment:latest' locally` and a failed pull, exit
125 (`laptop/25`, the video's Helm failure). With `set -e` the script stops right after the failed
build with exit status 1. Checked with a stand-in `docker` ([`shell.log`](assets/exercise-checks/logs/shell.log):
without `set -e` the run line still runs; with it, exit status 1 after the build) and with real Docker
([`socket.log`](assets/exercise-checks/logs/socket.log): after a failing rebuild, exit status 1, the
tag still carries the old image's label `v=1`, and `docker run` starts it). When you work by hand,
read the build's own output, not just the last line.
</details>

**B5. Make the delete delete.** In a copy of `deploy-create-instance.yml`:

1. Add `when: cluster_state == "present"` to "Create EC2 instance" (after `register: instance`,
   line 61) and run README:147's command against the copy. Predict which task fails now, and how.
2. Replace "Remove EBS volume" (lines 94-100) with tasks that find what to delete by **name**:
   terminate the instance tagged `Name: cheese-app-demo`, delete the volume tagged
   `cheese-app-demo-disk`, delete the security group `app_security_group`. In what order, and why?
   Run `--syntax-check`, then the delete command with your placeholder keys and predict the first task
   that fails.

<details><summary>Answer</summary>

1. Six tasks are skipped now, and "Remove EBS volume" fails the same way the instance task did:
   `'dict object' has no attribute 'volume_id'`. The volume's id is registered only by a create run
   (`ebs_volume`, line 36), and a delete run is a new run, often days later
   ([`ansible.log`](assets/exercise-checks/logs/ansible.log)).
2. One version is [`teardown-fixed.yml`](assets/exercise-checks/logs/teardown-fixed.yml):
   `amazon.aws.ec2_instance` with `state: absent`, `filters: {"tag:Name": "{{ aws_instance_name }}"}`
   and `wait: yes`; `amazon.aws.ec2_vol_info` with a `tag:Name` filter on `{{ persistent_disk_name }}`;
   `amazon.aws.ec2_vol` with `state: absent` for each volume found; `amazon.aws.ec2_group` with
   `state: absent`. Order: **instance first** (its two 100 GB disks go with it,
   `delete_on_termination: true`, lines 51 and 56, and the 50 GB volume is released if it was
   attached), **then the 50 GB volume**, **then the security group**, which AWS refuses to delete
   while an instance still uses it. The lookup works because `ec2_vol` writes its `name:` as the
   volume's `Name` tag (amazon.aws 3.5.0, the toolbox's version). It passes `--syntax-check`, and with
   `cluster_state=absent` the first task that runs is "Terminate EC2 instance", a real AWS call (in the
   offline check it stopped at `EndpointConnectionError`, because the container had no network; with a
   network and placeholder keys, expect AWS's `AuthFailure`, as in step 6). What AWS does with real
   keys was not run here:
   check the console afterwards anyway (S15's list), and keep deleting the ECR repositories, the key
   pair and the access key by hand, which no playbook here created.
</details>

**B6. See your own toolbox from inside it.** At the toolbox prompt, predict, then run:

```bash
docker ps --format '{{.Names}}  {{.Image}}'
docker images
ps aux | grep -c [d]ockerd
```

<details><summary>Answer</summary>

`docker ps` lists `cheese-app-deployment` itself (plus anything else running on your laptop), and
`docker images` lists your laptop's images: the toolbox and its `ubuntu:20.04` base (`laptop/29`, `41`),
and after a real step 5 the three app images. `ps` finds no `dockerd` (0): the toolbox has only the
CLI, talking through your laptop's socket. Same result with a CLI-only container
([`socket.log`](assets/exercise-checks/logs/socket.log)).
</details>

**B7. More messages for the sieves.** Without GitHub, fill in "job / deploy step" for: `deploy
/run-deploy`, `redeploy: /run-deploy-app-now`, and a push of three commits whose messages are
`/run-deploy-app`, `wip`, `fix lint` (in that order). Then do it for real on your repository, with a
change you can afford to deploy.

<details><summary>Answer</summary>

`deploy /run-deploy`: job runs (it contains `/run-`), deploy skipped (`/run-deploy` is not
`/run-deploy-app`). `redeploy: /run-deploy-app-now`: both run, because `contains()` is a substring
test, not a word match ([`trigger.log`](assets/exercise-checks/logs/trigger.log), a model of GitHub's
documented rule). The three-commit push: **nothing** runs. `head_commit` is the push's last commit,
`fix lint`, and the keyword two commits earlier is never read (GitHub's documentation of the push
event; not run here). Put the keyword in the last commit, or push it as an empty commit:
`git commit --allow-empty -m "redeploy /run-deploy-app"`.
</details>

---

## Part C · Debugging

**C1. "credentials file not found" after the fix.** You fixed `CSV_FILE` as README:76 says, then
started the script from the repository root to save a `cd`: `bash src/deployment/docker-shell.sh`
prints `Error: AWS credentials file not found at
../../../secrets/deployment-ac215-user_accessKeys.csv`. The file is there. Why?

<details><summary>Answer</summary>

Relative paths are resolved from the **shell's current folder**, not the script's. From
`~/cheese-app-aws`, three `../` lead to `/`, and there is no `/secrets/…`
([`shell.log`](assets/exercise-checks/logs/shell.log): exit status 1). The rest of the script relies
on the same thing: `BASE_DIR=$(pwd)` (line 25) is mounted at `/app`, `SECRETS_DIR` (line 26) and
`docker build … -f Dockerfile .` (line 32) all assume you are in `src/deployment`. Run it from there,
as README:75 says.
</details>

**C2. Which line is the error?** Step 5 ends with two RED lines:

```
aws: [ERROR]: An error occurred (UnrecognizedClientException) when calling the GetAuthorizationToken operation: The security token included in the request is invalid.
Error: Cannot perform an interactive login from a non TTY device
```

A classmate starts searching for TTY settings. What is the real problem, and what would change if
`docker-shell.sh:17` still held the author's account id while your keys were valid?

<details><summary>Answer</summary>

The first line. `aws ecr get-login-password` failed because AWS did not accept the key (in the
capture, a placeholder; for you: a typo, a deleted or deactivated key, or a CSV read wrongly), so it
printed nothing, and `docker login --password-stdin` received an empty password and complained about
the terminal (`laptop/40`, `deploy-docker-images.yml:9`). Read the first error, as in Lecture 1. Check
the key with `aws sts get-caller-identity` in the toolbox (`laptop/34` shows the same rejection).

With valid keys but someone else's account id, the login token is for **your** registry, but
`ecr_registry` (`deploy-docker-images.yml:6`) and every image name point at the author's
`<their-id>.dkr.ecr.us-east-1.amazonaws.com`, so the login and the pushes are refused (an
authorization error from ECR; reasoned from the code, not run here). The id comes from
`AWS_ACCOUNT_ID` (line 17 → `-e AWS_ACCOUNT_ID`, line 46 → `lookup('env', 'AWS_ACCOUNT_ID')`), so put
your own on line 17 and restart the toolbox.
</details>

**C3. "no such identity".** Step 8 with a real server, from your laptop's toolbox, ends with:

```
fatal: [<EXTERNAL_IP>]: UNREACHABLE! => … no such identity: /root/.ssh/ac215_2024.pem: No such file or directory … Permission denied (publickey).
```

<details><summary>Answer</summary>

`inventory.yml` still has line 4 active, the GitHub Actions key path `/root/.ssh/ac215_2024.pem`, and
your laptop's toolbox has nothing there: `docker-shell.sh` mounts your key at `/secrets` (line 38),
not at `/root/.ssh` (its line 39 mounts `$HOME/.ssh` at `/home/app/.ssh`, and the toolbox runs as
root). ssh skips the missing key, has no other key the server accepts, and is refused. Fix: README
step 9's switch (comment out line 4, activate line 7) **before** step 8, and name the file
`ac215_2024.pem`. Reproduced against a stand-in SSH server: line 4 → `no such identity:
/root/.ssh/ac215_2024.pem` … `Permission denied (publickey,password)`; line 7 with the key in
`/secrets` → `pong` ([`ansible.log`](assets/exercise-checks/logs/ansible.log); the stand-in also
offers passwords, a stock Ubuntu server on EC2 says only `(publickey)`).
</details>

**C4. "UNPROTECTED PRIVATE KEY FILE".** After the switch, step 8 now fails with `WARNING:
UNPROTECTED PRIVATE KEY FILE!` … `Permissions 0644 for '/secrets/ac215_2024.pem' are too open.`
What happened, and why didn't the CI copy have the problem?

<details><summary>Answer</summary>

OpenSSH ignores a private key that others can read, and then has no key to offer (`This private key
will be ignored.` … `Permission denied`; reproduced in [`ansible.log`](assets/exercise-checks/logs/ansible.log)).
The file probably lost its mode when it was copied or downloaded. Fix it on your laptop:
`chmod 400 ~/secrets/ac215_2024.pem` (the video's extra in S03; `laptop/14` shows `-r--------`); the
toolbox sees the same file through the mount. The workflow sets its copies to 600 itself
(`ci_cd_aws.yml:84-85`, and again inside the toolbox, `:124-127`).
</details>

**C5. The laptop deploy worked, the CI deploy doesn't.** You deployed by hand (step 9 switched), then
committed everything and pushed `/run-deploy-app`. The images are pushed, but "Run Deployment
Container" fails at the first task with `UNREACHABLE!` … `no such identity: /secrets/ac215_2024.pem`.

<details><summary>Answer</summary>

You committed the **laptop** key line. In CI the key is written to `/root/.ssh/ac215_2024.pem` inside
the toolbox (`ci_cd_aws.yml:81`, `:88-90`, `:116`), and there is no `/secrets`. Line 7 asks for
`lookup('env', 'AWS_SSH_KEY')` with a default of `/secrets/ac215_2024.pem`; `AWS_SSH_KEY` is in the
step's `env:` (`:108`), but it is not among the `-e` flags of the `docker run` (`:117-121`), so inside
the toolbox it is empty and the default wins (and if it were passed, it would hold the key's text, not
a path). Reproduced in the CI shape (key only in `/root/.ssh`): line 7 → `no such identity:
/secrets/ac215_2024.pem`; line 4 → `pong` ([`ansible.log`](assets/exercise-checks/logs/ansible.log)).
Fix: undo step 9 before you commit (line 4 on, line 7 off), as the video's commit checklist says;
the ECR login and image builds before it don't use the inventory, which is why they passed.
</details>

**C6. nginx won't stay up.** Step 13 finishes, but the browser can't connect, and on the server
`sudo docker container ls -a` shows `nginx` as `Exited (1)`. `sudo docker container logs nginx` ends
with `[emerg] … host not found in upstream "api-service" in /etc/nginx/nginx.conf:37`. What does
nginx want, and where would you look next?

<details><summary>Answer</summary>

nginx resolves every `proxy_pass` host when it starts, through Docker's DNS on `appnetwork`, which
knows only **running** containers. No running `api-service` → nginx refuses to start (reproduced:
exit status 1, [`nginx.log`](assets/exercise-checks/logs/nginx.log)). So the API is the problem: look
at step 10's output and `sudo docker container ls -a`, `sudo docker container logs api-service`.
Likely causes in this repository: step 10 stopped before "Create api-service container" because "Load
Vector DB" failed (Chroma `latest` answers the old API with HTTP 410, `laptop/60`, so pin
`chromadb/chroma:0.5.18` at `deploy-setup-containers.yml:151`; or Docker refused `-it` without a
terminal, `laptop/66`, so drop `-it` at `:165`), or the API container crashed while starting (it
connects to Chroma when it imports its RAG code, `src/api-service/api/utils/llm_rag_utils.py`; read,
not run). Fix the cause, run step 10 again, then step 13.
</details>

**C7. "I quoted the pin, now provision fails".** To get Ansible 9 you moved the toolbox to a newer
base image and wrote `pip install "ansible>=9.0.0"`. The toolbox builds, but step 8 fails at "Remove
Docker repositories from /etc/apt/sources.list.d/" with `Unsupported parameters for
(ansible.legacy.command) module: warn`.

<details><summary>Answer</summary>

`deploy-provision-instance.yml:56-57` passes `args: warn: false` to `shell:`. The old ansible-core
2.13 in the original toolbox accepts it (the same lines run, `changed`); newer ansible-core rejects it
(2.17.14: the error above, [`pip.log`](assets/exercise-checks/logs/pip.log)). Delete the two lines
`args:` / `warn: false`: the task works without them. Then expect the other warnings the video hid to
change too (`community.general.docker_image` is a redirect that will be removed, `laptop/40`; use
`community.docker.docker_image`).
</details>

---

## Part D · Think

**D1. Fewer copies of the keys.** Sketch what changes, file by file, to use an instance role on the
server and GitHub OIDC in the workflow. What would still be a long-lived secret afterwards?

<details><summary>Answer</summary>

- **Server, instance role:** an IAM role with ECR pull and Bedrock access, attached to the instance
  (an instance profile on `amazon.aws.ec2_instance`). Delete "Configure AWS credentials"
  (`deploy-provision-instance.yml:288-292`), the credentials file (`deploy-setup-containers.yml:31-44`)
  and the key lines of the containers (`:166-168`, `:184-186`); the AWS CLI on the server and boto3 in
  the containers find the role's short-lived credentials on their own. AWS's documentation recommends a
  metadata hop limit of 2 when containers on the instance need them (not checked here).
- **GitHub, OIDC:** an IAM role that trusts GitHub's token issuer for your repository and branch;
  in the workflow `permissions: id-token: write` and `role-to-assume:` instead of the two keys
  (`ci_cd_aws.yml:18-23`). The deploy step then must pass the temporary credentials into the toolbox,
  including `AWS_SESSION_TOKEN`, which the current `env:`/`-e` lists (`:101-108`, `:117-121`) don't
  carry, and stop writing keys to the server (the role does that job now).
- **Still long-lived:** the SSH private key (`AWS_SSH_KEY`, needed by every `appserver` play; AWS
  Systems Manager could replace SSH, a bigger change), your laptop's access key (AWS's IAM Identity
  Center sign-in, `aws sso login`, would make it short-lived too), and `NEXTAUTH_SECRET`
  (`inventory.yml:24`, committed: move it into a repository secret).
</details>

**D2. From delivery to deployment.** Write down the edits that make this workflow continuous
deployment, as Milestone 5 asks, without losing the safety the keyword gave.

<details><summary>Answer</summary>

Trigger on every push to `main` (the merge of a pull request) and drop both `contains()` conditions
(`:9`, `:100`); add a test job (Lecture 21's lint and tests) and make the build-and-deploy job
`needs:` it, so only a green test run deploys; protect `main` so changes arrive through pull requests
with those checks required (Lecture 21's branch protection). The keyword's safety, a human choosing
the moment, moves into the review of the pull request. If you want a human button back for
production, a GitHub environment with required reviewers on the deploy job gives you delivery again,
on purpose. Also commit the server address and the CI key line once, so every deploy has what it
needs (C5), and keep ECR in check (a lifecycle policy that expires old tags), since every merge now
pushes three images.
</details>

**D3. Swap, not roll.** Each deploy recreates `frontend` and `api-service` in place
(`recreate: yes`) and runs the loader in between. What does a visitor see during a deploy, and how
could one machine avoid it?

<details><summary>Answer</summary>

A gap: for a moment there is no `frontend`/`api-service` container, and those requests fail (nginx
answers with an error page, typically 502), and while the loader rebuilds the collection (`src/vector-db/cli.py:305-310` deletes it,
then creates it again) RAG answers have nothing or half the data to search. The API is also recreated
after the loader finishes, so its gap can be long. Note that `recreate: yes` recreates even when the
tag hasn't changed. And nginx looks up `api-service` and `frontend` once, when it starts (C6): a
recreated container may get a new address on `appnetwork`, which is one reason the webserver playbook
ends with "Restart nginx container", and why CI runs it after every deploy (`ci_cd_aws.yml:131`;
reasoned from nginx's documented behaviour, not run here). On one machine you can do blue/green: start the new containers beside the old
ones under other names (`api-service-green`), wait until they answer, switch nginx's upstream and
`nginx -s reload`, then remove the old ones; and load the vector DB into a new collection, switching
the API to it, instead of deleting the live one. Kubernetes (Lecture 22, the slides' version) does the
first part for you with a rolling update.
</details>

**D4. What still bills?** You terminated the instance in the console and stopped there. What is still
on your bill, and what is free to leave?

<details><summary>Answer</summary>

Still billing: the **50 GB volume** `cheese-app-demo-disk`, which was created on its own
(`deploy-create-instance.yml:27-37`) and outlives the instance (if the attach failed it was never
attached at all); the **ECR images**, three per `/run-` push, all kept; **Bedrock** only when something
calls it (nothing does once the server is gone); GitHub Actions minutes on a private repository only
when a run happens. Gone with the instance: its two 100 GB disks (`delete_on_termination: true`) and
its public IPv4 address (an auto-assigned one is released at termination; AWS's documentation). Free
to leave, but delete anyway for safety: the security group, the key pair, the IAM user, policy and
access key (a leaked key costs more than any disk), and the four repository secrets. That is S15's
checklist; B5 automates the first three AWS resources.
</details>

**D5. Why `linux/amd64` everywhere?** `docker-shell.sh:32` builds the toolbox with
`--platform=linux/amd64`, and the playbook builds the app images with `platform: linux/amd64/v2`
(`deploy-docker-images.yml:22`, `:35`, `:48`), while CI uses plain `docker build`
(`ci_cd_aws.yml:56`, `:62`, `:68`). Why the difference, and what happens on an Apple-silicon Mac?

<details><summary>Answer</summary>

The images must run on the server, a `t2.large` (`inventory.yml:15`), which is an x86-64 machine. On
an Apple-silicon Mac Docker builds arm64 images by default, which would not start there, so the
laptop route asks for amd64 explicitly (Docker Desktop emulates it, slowly). GitHub's `ubuntu-latest`
runners are x86-64, so a plain build there is already amd64. The toolbox never runs on the server, so
its own pin isn't needed for that (its Dockerfile even picks the AWS CLI by `uname -m`, line 13); on a
Mac it just means the toolbox runs emulated. (Reasoned from the files and the instance type; the
video's laptop was x86-64, so no emulation was recorded.)
</details>
