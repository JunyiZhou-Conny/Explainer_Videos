# L23 · Final Deployment and Review (GCP lecture, AWS tutorial) — tutorial digest

- **Ed lesson:** https://edstem.org/us/courses/97373/lessons/166048/ (not opened; the lecture side is `SLIDES.md`).
- **Series decision (Conny, issue #125):** L23 follows the **AWS** variant of the tutorial, exactly as L15 did (`videos/ac215-l15-vertex-ml-workflows/`). The lecture slides speak Google Cloud (GKE, Artifact Registry, Vertex AI, a service-account key in a GitHub secret); they decide the *concepts*. The AWS repo and our captures decide what the video *shows*. Section 7 maps one vocabulary onto the other. The course site lists this repo for L23 as the AWS variant, marked "No K8s" (source: the coordinator's lecture entry and the previous digest's citation of the course-site file `tutorials_demo.md:288-294`; that file is not in this sandbox, so the citation was not re-checked).
- **Primary repo:** `dlops-io/cheese-app-aws`, branch `main`, commit `5950118b0ed97c12c799920846d3eb70b1a47385`, committed 2024-11-21 18:27:08 -0500 (message "cleanup"; it deletes 26 lines from `src/deployment/deploy-setup-containers.yml`). The branch has 39 commits; the 20 commits that touch the workflow file include a run of eleven `/run-deploy-app` commits on 2024-11-21, i.e. the workflow was debugged by pushing.
  - Re-checked with `git ls-remote` on 2026-11-08: `HEAD` = `refs/heads/main` = `5950118`. **No other branches, no tags.**
  - The repo is a year older than the GCP version (`cheese-app-v4` is from 2025-12). Several things it installs at build time are unpinned (see §6), so "it worked in 2024" and "it builds today" are different claims; this digest says which one each line makes.
- **Context repo (the slides' GCP version):** `dlops-io/cheese-app-v4`, `main`, `033f18713b9e1e7985a3080e85edab3ff01cefef`, 2025-12-02 14:13:03 -0500 ("Test pipeline /run-ml-pipeline"). `git ls-remote` on 2026-11-08: `main` = `HEAD` = `033f187`; one other branch, `pipenv` @ `31f38b1`. Used only to explain slides 17–20 (§7); nothing in the video's walkthrough comes from it.
- **README sections covered:** the whole of `cheese-app-aws/README.md` (148 lines), top to bottom: "Cheese App AWS" → "Deployment to AWS" (`:3-5`) → "API's to enable in AWS before you begin" (`:7-13`, empty) → "Setup AWS Keys for Authentication" (`:15-60`) → "Create AWS EC2 Key Pair" (`:62-64`) → "Deployment Setup" (`:67-72`) → "Deployment Steps" (`:74-77`) → "Create Empty ECR Repositories" (`:79-85`) → "Build and Push Docker Containers to AWS ECR" (`:87-90`) → "Create Compute Instance (VM) Server in GCP" (`:92-97`) → "Provision Compute Instance in GCP" (`:99-103`) → "Setup Docker Containers in the Compute Instance" (`:105-132`) → "Configure Nginx file for Web Server" (`:136-137`) → "Setup Webserver on the Compute Instance" (`:139-143`) → "Delete the Compute Instance / Persistent disk" (`:145-148`). The README never mentions the GitHub Actions workflow; the CI/CD half of this lecture lives only in `.github/workflows/ci_cd_aws.yml` (131 lines), which this digest walks as its own Part.
- **Colab notebooks:** none.
- **Files read in full:** `README.md`; `.github/workflows/ci_cd_aws.yml`; everything in `src/deployment/` (`Dockerfile`, `docker-shell.sh`, `docker-entrypoint.sh`, `docker-entrypoint_working.sh`, `inventory.yml`, `ansible.cfg`, `Pipfile`, `.docker-tag`, the five `deploy-*.yml` playbooks, `nginx-conf/nginx/nginx.conf`); `src/api-service/` (`Dockerfile`, `docker-entrypoint.sh`, `docker-shell.sh`, `Pipfile`, `api/service.py`, the router imports, `api/utils/llm_rag_utils.py`; the other utils grepped); `src/vector-db/` (`Dockerfile`, `docker-entrypoint.sh`, `docker-shell.sh`, `docker-compose.yml`, the setup, `download()`, `load()` and argparse parts of `cli.py`); `src/frontend-react/` (`Dockerfile`, `Dockerfile.dev`, `.env.*`, `next.config.js`, `Common.js`, the `DataService.js` URL lines, `package.json`).
- **How claims were checked (2026-11-08):**
  - Every `path:line` below was checked with `sed -n`/`cat -n`/`grep -n` at `5950118`. Paths are relative to `cheese-app-aws/` unless prefixed `cheese-app-v4/`.
  - The deployment image was built here from the tutorial's own `src/deployment/Dockerfile` (unchanged copy, in a scratch folder), on a capture-only `ubuntu:20.04` re-tag that adds the sandbox proxy's CA and https apt sources (as in L15). The unchanged build **fails** in this sandbox at the Helm step (§6 G3); a second build from a capture-only copy with the two Helm lines removed succeeded and is what the version numbers below come from.
  - Inside that image: `ansible --version`, `ansible-galaxy collection list`, `ansible-doc` for every module the playbooks use, `ansible-playbook --syntax-check` for all five playbooks (all pass), `ansible-playbook --list-tasks`, `ansible-inventory --graph`, and `ansible-playbook deploy-docker-images.yml`, `deploy-create-instance.yml … cluster_state=present` and `… cluster_state=absent` run with **AWS's documented dummy keys** (`AKIAIOSFODNN7EXAMPLE` / `wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY`) and `AWS_ACCOUNT_ID=YOUR_ACCOUNT_ID`, each up to its first real error. No Docker socket was mounted into these runs.
  - `docker-shell.sh:1-21` was run under `dash` (`sh`) and `bash` in `ubuntu:20.04` against a placeholder CSV holding the dummy keys.
  - The vector store's download (`https://github.com/dlops-io/datasets/releases/download/v4.0/cheese-books-embeddings.zip`, 22,925,732 bytes) was downloaded and inspected as data (zip listing, one JSON line), never executed.
  - `chromadb/chroma:latest` (pulled 2026-11-08; `/api/v2/version` answers `"1.0.0"`) was run for one minute to probe `/api/v1/heartbeat` and `/api/v2/heartbeat`, then removed.
  - Not built: the api-service image (TensorFlow 2.17, large) and the frontend image. Claims about them are from the files and marked *(read, not run)*.
  - All capture images and build cache were deleted afterwards.

**Masking rule for every frame and file.** The repo commits several things that must never appear unmasked:
- `src/deployment/docker-shell.sh:17` hard-codes the tutorial author's 12-digit AWS account id → show `export AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"`.
- `src/deployment/inventory.yml:30` lists the author's server's public IP → show `<EXTERNAL_IP>:`.
- `inventory.yml:24` and `src/frontend-react/.env.production:3` (and `.env.development:5`) commit `NEXTAUTH_SECRET` values → show `<nextauth-secret>`.
- Access keys only ever as `<aws-access-key-id>` / `<aws-secret-access-key>`, or AWS's own documented dummy pair, labelled as such. ECR registry hosts as `YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com`.
- The repo's commit authors are staff: never show `git log` author lines.

---

## 1. What you build

The cheese app you have been building all term (Next.js frontend, FastAPI API, ChromaDB vector DB plus its loader) goes live on **one AWS virtual machine**, and two kinds of automation take over from your hands:

**Part 1 — Ansible from your laptop (the README).** Everything runs inside one toolbox container, `cheese-app-deployment` (Ubuntu 20.04 + AWS CLI v2 + Docker CLI + kubectl + Ansible), started by `sh docker-shell.sh` in `src/deployment/`. From its shell you run five Ansible playbooks against an inventory file:

| README step | Playbook | Runs on | What it does |
| --- | --- | --- | --- |
| Build and push (`README.md:89`) | `deploy-docker-images.yml` | `localhost` (the toolbox, using your laptop's Docker daemon through the mounted socket) | logs in to ECR, builds `cheese-app-frontend-react`, `cheese-app-api-service`, `cheese-app-vector-db-cli`, tags each `:<YYYYmmddHHMMSS>`, pushes to ECR, writes the tag to `.docker-tag` |
| Create instance (`:94`) | `deploy-create-instance.yml` with `cluster_state=present` | `localhost` (AWS API calls through boto3) | security group (22, 80, 443 open to the world), a 50 GB gp3 EBS volume, a `t2.large` EC2 instance from an Ubuntu AMI with your key pair, waits for SSH |
| Provision (`:102`) | `deploy-provision-instance.yml` | `appserver` over SSH, `become: true` | installs Docker CE, mounts the data disk at `/mnt/disk-1`, installs AWS CLI v2, writes your access keys with `aws configure` |
| Setup containers (`:116`) | `deploy-setup-containers.yml` | `appserver` | writes `/srv/secrets/aws-credentials`, creates Docker network `appnetwork`, logs the VM in to ECR, pulls the three images at the saved tag, starts `frontend` (3000), `vector-db` (`chromadb/chroma:latest`, 8000), runs the vector-db CLI once to download and load the embeddings, starts `api-service` (9000) |
| Setup webserver (`:141`) | `deploy-setup-webserver.yml` | `appserver` | copies `nginx-conf/nginx/` to `/conf`, starts `nginx:stable` on 80/443 with `/api/` → `api-service:9000`, `/` → `frontend:3000` |
| Delete (`:147`) | `deploy-create-instance.yml` with `cluster_state=absent` | `localhost` | meant to tear down; **fails before any AWS call** at this commit (§6 G9) |

Then you open `http://<EXTERNAL_IP>/` (`README.md:143`).

**Part 2 — GitHub Actions does the redeploy (`.github/workflows/ci_cd_aws.yml`, not in the README).** On every push to `main` whose commit message contains `/run-`, a fresh GitHub-hosted Ubuntu runner checks out the repo, logs in to AWS with three repository secrets, builds the three app images with plain `docker build`, tags them with a fresh timestamp and pushes them to ECR. If the message also contains `/run-deploy-app`, it builds the same `cheese-app-deployment` toolbox image and runs two of the playbooks inside it: `deploy-setup-containers.yml` (with the new tag) and `deploy-setup-webserver.yml`. The VM must already exist and be provisioned, and its IP must already be committed in `inventory.yml`: CI never creates or provisions the machine.

There are **no tests** anywhere in the workflow: like the GCP version (`cheese-app-v4/README.md:157`, "The CI part is not implemented in this tutorial"), this is continuous *deployment* only, even though the workflow is named "Continuous Integration and Continuous Deployment" (`ci_cd_aws.yml:1`).

```
 YOUR LAPTOP                                             GITHUB  <you>/cheese-app-aws
 +---------------------------------------------+         +-------------------------------------------+
 | secrets/  (CSV access keys, .pem key pair)  |  push   | .github/workflows/ci_cd_aws.yml           |
 | src/deployment$ sh docker-shell.sh          | ------> | secrets: AWS_ACCESS_KEY_ID,               |
 |  -> cheese-app-deployment (toolbox)         |  main   |   AWS_SECRET_ACCESS_KEY, AWS_ACCOUNT_ID,  |
 |     ansible-playbook deploy-*.yml           |         |   AWS_SSH_KEY                             |
 +----------------------+----------------------+         +---------------------+---------------------+
        build+push      |  create, provision,                 msg has "/run-"  | build+push (docker)
        (laptop docker) |  setup over SSH                     "/run-deploy-app"| setup-containers +
                        v                                                      v setup-webserver
 +--------------------------------------------------------------------------------------------------+
 | AWS us-east-1                                                                                    |
 |  ECR: cheese-app-frontend-react / cheese-app-api-service / cheese-app-vector-db-cli  :<timestamp>|
 |  EC2 t2.large "cheese-app-demo" (Ubuntu), security group 22/80/443, EBS at /mnt/disk-1           |
 |    docker network "appnetwork":                                                                  |
 |      nginx :80 --/api/--> api-service :9000 --> vector-db :8000 (Chroma)                         |
 |            \----/-----> frontend :3000                       Bedrock (Claude, Titan) <- api      |
 +--------------------------------------------------------------------------------------------------+
                                     ^ browser: http://<EXTERNAL_IP>/
```

## 2. Prerequisites and costs

### Accounts and local installs
- An AWS account with billing enabled, console access, and Amazon Bedrock model access in `us-east-1` for the models the API calls (`anthropic.claude-3-5-sonnet-20240620-v1:0` in `api/utils/llm_utils.py:35`, `anthropic.claude-3-sonnet-20240229-v1:0` in `llm_rag_utils.py:22` and `llm_cnn_utils.py:47`, `amazon.titan-embed-text-v1` in `llm_rag_utils.py:21`). The README does not mention Bedrock model access at all (open question in §10).
- Docker on the laptop. Nothing else: AWS CLI, Ansible and kubectl live in the toolbox image.
- A GitHub repo of your own (a fork or a copy) for Part 2, with Actions enabled.

### AWS services and the empty "APIs" section
`README.md:7-13` has a heading "API's to enable in AWS before you begin" whose list (ECR, IAM, VPC, Security Groups, Load Balancer) is inside an HTML comment, so it renders as an empty section. AWS has no per-API enablement step like GCP; the video can say so in one sentence and move on. No load balancer is used anywhere in the code.

### Identity: one IAM user, one key pair
- **Customer-managed policy `CheeseAppECRPolicy`** (`README.md:19-46`): `sts:GetCallerIdentity` plus nine ECR actions (`GetAuthorizationToken`, `BatchCheckLayerAvailability`, `PutImage`, `InitiateLayerUpload`, `UploadLayerPart`, `CompleteLayerUpload`, `ListImages`, `BatchGetImage`, `GetDownloadUrlForLayer`) on `"Resource": "*"`. It does **not** include `ecr:CreateRepository`; that is why the README has you create the three repositories in the console (`:79-85`).
- **IAM user `deployment-ac215-user`** (`:48-50`) with AWS-managed policies `AmazonS3FullAccess`, `AmazonEC2FullAccess`, `AmazonBedrockFullAccess`, plus `CheeseAppECRPolicy`.
- **Access key** for "Third Party Service" (`:52`), downloaded as `deployment-ac215-user_accessKeys.csv` and saved in a `secrets/` folder next to the clone (`:54-60`). `docker-shell.sh:13` reads line 2 of that CSV as `AWS_ACCESS_KEY_ID,AWS_SECRET_ACCESS_KEY`.
- **EC2 key pair** (`:64`): the README names it `cheese-app-ac215-key-pair`; the code expects a key pair named `ac215_2024` (`inventory.yml:16`, with the comment `## Change this`) and a private key file `ac215_2024.pem` (`inventory.yml:4`, `:7`; `docker-shell.sh:27`; `ci_cd_aws.yml:81`). Pick one name and use it in all three places (§6 G6).
- The same access key does everything: it pushes images from the laptop and from CI, creates the EC2 resources, is written onto the VM twice (`aws configure` in `deploy-provision-instance.yml:288-292`, and `/srv/secrets/aws-credentials` in `deploy-setup-containers.yml:36-44`), and is passed as environment variables into the api-service and vector-db containers (`deploy-setup-containers.yml:165-168`, `:184-186`), which use it to call Bedrock. See C6.

### Values committed in the repo that you must change
| File:line | Value at this commit | Change to |
| --- | --- | --- |
| `src/deployment/docker-shell.sh:10` | `CSV_FILE="../../../../secrets/deployment-ac215-user_accessKeys.csv"` (four levels up) | the path to your CSV; the README's own layout needs three levels (`README.md:76`) |
| `docker-shell.sh:26` | `SECRETS_DIR=$(pwd)/../../../../secrets/` | the same folder (the README does not mention this line) |
| `docker-shell.sh:17` | the author's account id | `YOUR_ACCOUNT_ID` (your 12-digit id) |
| `inventory.yml:4` / `:7` | CI key path active, local path commented | for local runs, the `/secrets/...` line (`README.md:107-111`) |
| `inventory.yml:16` | `aws_keypair_name: "ac215_2024"` | your key pair's name |
| `inventory.yml:17` | `aws_ami_id: "ami-0e86e20dae9224db8"` | an Ubuntu AMI in your region (AMI ids are per region; this one is for `us-east-1`; which Ubuntu release it is was not checked) |
| `inventory.yml:24` | a committed `NEXTAUTH_SECRET` | your own random value |
| `inventory.yml:30` | the author's server IP | your instance's public IP, after the create step (`README.md:97`) |

### What costs money, and how to switch it off
*(Prices are AWS's public on-demand list prices for `us-east-1` as we know them; not re-checked against a live price page on 2026-11-08 — say "roughly" and point to the pricing pages.)*
- **EC2 `t2.large`** (`inventory.yml:15`), running 24/7 from the create step until you terminate it: about $0.09 per hour.
- **EBS:** the instance's two 100 GB gp2 volumes (`deploy-create-instance.yml:47-57`, deleted with the instance) and the separate 50 GB gp3 volume (`:27-37`), which survives the instance and keeps billing until you delete it.
- **Public IPv4 address** on the instance: AWS bills public IPv4 addresses by the hour.
- **ECR storage:** three images per deploy, a new timestamp tag every time; nothing ever deletes old tags.
- **Bedrock:** per token, every chat message.
- **GitHub Actions:** free minutes on public repos; billed minutes on private ones beyond the free tier.
- **Switch-off:** the README's delete command fails at this commit (§6 G9). Clean up in the console (or with the AWS CLI): terminate the instance, delete the leftover 50 GB volume, delete security group `app_security_group`, delete the three ECR repositories, delete (or deactivate) the access key, delete the key pair and the IAM user if you made them only for this. Shown as an `illustration` checklist in the video.

## 3. Concepts this tutorial teaches

### C1. Integration, delivery, deployment — and what this workflow actually does (slides 7–12)
CI: every change is merged into a shared branch often and checked automatically (build, tests, linting). Continuous delivery: every change that passes is *ready* to release, but a person presses the button. Continuous deployment: every change that passes goes to production with no person in between. `ci_cd_aws.yml` has no test step, so it is CD with the gates switched off: a push to `main` with the right words in the message rebuilds and redeploys whatever is in the commit. Misconception to defuse: a green workflow run means "the steps exited 0", not "the app works".

### C2. Two sieves on one string: the commit message **[ANIMATE]** (slides 18, 20)
`on: push: branches: [ "main" ]` (`ci_cd_aws.yml:3-5`): every push to `main` creates a workflow run. Then two `contains()` filters read the same string, `github.event.head_commit.message`:
- job level, `if: contains(github.event.head_commit.message, '/run-')` (`:9`): without `/run-` the whole job is skipped;
- step level, `if: contains(github.event.head_commit.message, '/run-deploy-app')` (`:100`): only the final "Run Deployment Container" step is gated.
So `/run-deploy-app` builds, pushes **and** deploys; any other message containing `/run-` (for example `/run-tests`) builds and pushes new images but deploys nothing; a message without `/run-` does nothing. `head_commit` is the last commit of the push: a push of three commits is judged by the last message only. `contains()` on strings is case-insensitive in GitHub Actions expressions. The slides' keyword is `/deploy-app` (GCP repo); here it is `/run-deploy-app` (§7).

### C3. One toolbox, two operators, sibling containers **[ANIMATE]** (slides 17–18)
The same `src/deployment/Dockerfile` builds the toolbox on your laptop (`docker-shell.sh:32`) and on the runner (`ci_cd_aws.yml:41-44`). Inside it, `docker` commands do not run a Docker daemon of their own: the host's socket is mounted (`docker-shell.sh:36`, `ci_cd_aws.yml:114`), so `docker build`/`docker push` from Ansible's `docker_image` module create **sibling** images on the host's daemon. That is why the build paths are `/frontend-react`, `/api-service`, `/vector-db` (`deploy-docker-images.yml:21`, `:34`, `:47`): `docker-shell.sh:40-42` mounts the three app folders at exactly those paths. Difference between the two operators:
- laptop: the deployment folder is mounted at `/app` (`docker-shell.sh:37`), secrets at `/secrets` (`:38`), the shell is interactive (`-ti`, `:35`) and you type the playbooks;
- runner: the deployment folder is mounted at `/deployment` (`ci_cd_aws.yml:115`), the CI-written secrets folder at `/root/.ssh` (`:116`), and a `bash -c` string runs two playbooks non-interactively (`:123-131`). The runner never mounts the app folders: CI builds the app images with plain `docker build` on the runner itself (`:52-70`), not with the playbook.
- `ENTRYPOINT` is commented out in the toolbox Dockerfile (`Dockerfile:62`; `CMD ["/bin/bash"]` at `:64`), so `docker-entrypoint.sh` (which would write `~/.aws/credentials` and log in to ECR) never runs. Nothing breaks, because the AWS CLI and boto3 read `AWS_ACCESS_KEY_ID`/`AWS_SECRET_ACCESS_KEY`/`AWS_DEFAULT_REGION` from the environment (`docker-shell.sh:43-45`), and both `deploy-docker-images.yml:9` and the CI step `:129` do their own ECR login.

### C4. Ansible in one picture: inventory, plays, tasks, modules **[ANIMATE]** (not in the slides)
- **Inventory** (`inventory.yml`): group `all` with variables (`:2-25`) and one child group `appserver` with one host, the VM's IP (`:27-30`). `ansible-inventory -i inventory.yml --graph` prints `@all` → `@appserver` → the IP (captured).
- **Playbook** = a list of plays; each play has `hosts:` (`localhost` or `appserver`), optional `connection: ssh` and `become: true` (sudo on the VM), and a list of **tasks**; each task calls one **module** (`shell`, `apt`, `file`, `copy`, `docker_image`, `docker_container`, `docker_network`, `ec2_group`, `ec2_vol`, `amazon.aws.ec2_instance`, …) with arguments.
- `hosts: localhost` plays run inside the toolbox and talk to AWS's API (create-instance) or to the host Docker daemon (docker-images). `hosts: appserver` plays SSH to the VM as `ubuntu` (`inventory.yml:3`) with the `.pem` key and run each module there.
- Modules are mostly **declarative**: `state: present` / `state: started` say what should be true, and re-running converges instead of duplicating. `shell:` tasks are the exception: they run every time (`deploy-provision-instance.yml:118-137`, `:288-292`). The `when:` lines (`deploy-create-instance.yml:24`, `:37`, `:74`, …) make one playbook do both create and delete — in intention (§6 G9).
- `ansible.cfg:2` sets `host_key_checking = False`, and `inventory.yml:8` passes `-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null`: a fresh VM's host key is accepted blindly. Convenient for a course, a trade-off worth naming.

### C5. One timestamp, followed from build to running container **[ANIMATE]** (slides 18–19, 36)
- Laptop route: `date +%Y%m%d%H%M%S` (`deploy-docker-images.yml:12`) → registered as `tag` → image names `<registry>/cheese-app-…:{{ tag.stdout }}` (`:23`, `:36`, `:49`) → pushed (`:25-56`) → saved with `echo {{ tag.stdout }} > .docker-tag` (`:58`). The committed `.docker-tag` holds `20241121211313` (`src/deployment/.docker-tag:1`), the author's last tag.
- CI route: `echo $(date +%Y%m%d%H%M%S) > …/.docker-tag` and `DOCKER_TAG` into `$GITHUB_ENV` (`ci_cd_aws.yml:46-50`) → `docker tag …:latest …:${{ env.DOCKER_TAG }}` and `docker push` (`:57-70`) → `-e DOCKER_TAG` into the toolbox (`:121`) and again as `--extra-vars … docker_tag=$DOCKER_TAG` (`:130`).
- On the VM: `deploy-setup-containers.yml` copies `.docker-tag` over (`:67-71`), then sets `docker_tag` from the `DOCKER_TAG` environment variable if it is set (`:101-104`), else from the file (`:106-114`); pulls the three images at that tag (`:120-129`); and recreates each container (`recreate: yes`, `:136`, `:153`, `:180`).
- What this is **not**: a rolling update. Each container is stopped and replaced in place on one machine, so there is a short outage per deploy; contrast with v4's Kubernetes rolling update (§7). "Release" in the slides' loop = the moment the timestamped image lands in ECR.

### C6. Who holds which credential, where **[ANIMATE]** (slides 18–19)
One IAM user's access key pair travels: CSV in `secrets/` → shell variables (`docker-shell.sh:13-15`) → toolbox environment (`:43-46`) → Ansible variables via `lookup('env', …)` (`inventory.yml:9-11`, `deploy-setup-containers.yml:8-11`) → the VM (`aws configure`, `deploy-provision-instance.yml:288-292`; `/srv/secrets/aws-credentials`, mode 0600, `deploy-setup-containers.yml:36-44`) → the api-service and vector-db loader as environment variables (`:165-168`, `:184-186`). In CI the same values come from repository secrets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID` (`ci_cd_aws.yml:21-22`, `:33`, `:102-104`), and the SSH private key from `AWS_SSH_KEY` (`:81`, `:108`). Second identity: the EC2 **key pair**, whose private half lets Ansible SSH in as `ubuntu`. Lesson for the video: long-lived keys copied onto a server work, but AWS's preferred pattern is an **instance role** (the VM gets temporary credentials without a key file) and, for GitHub, OIDC federation instead of stored keys; mention as the "next step", not as the tutorial.

### C7. One VM, five containers, one front door **[ANIMATE]** (slide 37 shows the same shape with Kubernetes)
On Docker network `appnetwork` (`deploy-setup-containers.yml:47-53`), containers reach each other by name. `nginx` publishes 80 and 443 (`deploy-setup-webserver.yml:29-31`) and is the only entry the security group lets in besides SSH (`deploy-create-instance.yml:12-21`; ports 3000/8000/9000 are published on the VM but closed by the security group). `nginx.conf`:
- `location ^~ /api/ { proxy_pass http://api-service:9000/; … }` (`nginx.conf:35-44`): the trailing `/` in `proxy_pass` replaces the matched `/api/` prefix, so the browser's `/api/newsletters` reaches FastAPI as `/newsletters`, which is where `service.py:25` mounts that router.
- `location / { proxy_pass http://frontend:3000; … }` (`:47-55`).
- The frontend calls `/api/...` on the same host because `.env.production:2` sets `NEXT_PUBLIC_BASE_API_URL=/api`, which `Common.js:2` reads at build time.
- Data: Chroma persists to `/mnt/disk-1/chromadb` (`deploy-setup-containers.yml:162`), the API's `/persistent` to `/mnt/disk-1/persistent` (`:193`), both on the disk mounted by the provision playbook (`deploy-provision-instance.yml:159-176`).
- The vector DB is filled once per deploy by a throwaway container: `cheese-app-vector-db-cli … cli.py --download --load --chunk_type recursive-split` (`deploy-setup-containers.yml:164-173`), which downloads pre-computed chunks and embeddings from a GitHub release and loads them into collection `recursive-split-collection` (`src/vector-db/cli.py:470-487`, `:293-311`).

### C8. Same lecture, other cloud: the term map (slides 17–20)
| Slides (GCP, `cheese-app-v4`) | This repo (AWS, `cheese-app-aws`) |
| --- | --- |
| Artifact Registry / "GCR" | ECR (three repositories, created by hand) |
| GKE cluster, Deployments, rolling update | one EC2 VM, `docker_container` with `recreate: yes` |
| Pulumi programs (`pulumi up`) | Ansible playbooks (`ansible-playbook`) |
| service-account JSON key, secret `GOOGLE_APPLICATION_CREDENTIALS` | IAM user access key CSV; secrets `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`, `AWS_SSH_KEY` |
| `google-github-actions/auth@v1` | `aws-actions/configure-aws-credentials@v4` |
| commit keyword `/deploy-app` | `/run-deploy-app` (and `/run-` for build-only) |
| Ingress / Google HTTPS load balancer | `nginx` container on port 80 |
| `/run-ml-pipeline` → Vertex AI Pipelines | nothing: the AWS repo has no ML workflow (the AWS ML pipeline is L15's `ml-workflow-aws`, SageMaker) |
| Gemini / Vertex AI embeddings | Bedrock: Claude 3 / 3.5 Sonnet, Titan embeddings |

## 4. Step-by-step walkthrough

README order. "Capture" says what the video can show for real from this sandbox (no AWS credentials).

### Part A — one-time setup in the console (`README.md:1-72`)
1. **Read the goal** (`:3-5`): deploy with Ansible playbooks, "automate all the deployment steps".
2. **"API's to enable"** (`:7-13`): renders empty (commented list). Capture: none; one sentence.
3. **Create policy `CheeseAppECRPolicy`** (`:19-46`): IAM → Policies → Create policy → JSON, paste `:22-44`, "Review Policy", name, create. Capture: `illustration` (schematic console). Extra check that can be captured: the JSON parses (`python3 -m json.tool` or `jq .` on a copy).
4. **Create IAM user `deployment-ac215-user`** with `AmazonS3FullAccess`, `AmazonEC2FullAccess`, `AmazonBedrockFullAccess` (`:48`), and attach `CheeseAppECRPolicy` (`:50`). Capture: `illustration`.
5. **Create an access key** → "Third Party Service" → download the CSV (`:52`), save it as `secrets/deployment-ac215-user_accessKeys.csv` next to the clone (`:54-60`; the tree shows `cheese_app_aws` and `secrets` side by side). Capture: `illustration`; locally, a placeholder CSV with AWS's documented dummy keys, labelled.
6. **Create EC2 key pair** (`:64`) and save the `.pem` in `secrets/`. Capture: `illustration`. Add (not in README): `chmod 400` on the `.pem` (§6 G7), and the name mismatch (§6 G6).
7. **"Deployment Setup"** (`:67-72`): four bullets saying "add … details in inventory.yml": ansible user (`inventory.yml:3`), instance details (`:14-23`), access-key details (`:9-12`, env lookups, nothing to type), key pair (`:4`/`:7`, `:16`). Capture: code panel of `inventory.yml` with the masked lines.

### Part B — start the toolbox (`README.md:74-77`)
8. `cd src/deployment` (`:75`).
9. **Edit `CSV_FILE`** in `docker-shell.sh` to `"../../../secrets/deployment-ac215-user_accessKeys.csv"` (`:76`; the file has four `../` at `docker-shell.sh:10`). Also edit `SECRETS_DIR` (`:26`) and `AWS_ACCOUNT_ID` (`:17`) — not in the README (§6 G4, G5).
10. **`sh docker-shell.sh`** (`:77`). It reads the CSV (`docker-shell.sh:11-21`), builds `cheese-app-deployment` for `linux/amd64` (`:32`) and opens a root shell in `/app` (`:35-48`). Capture: real, with caveats: on Linux `sh` is `dash` and the script stops at line 13 with `Syntax error: redirection unexpected` (captured, §6 G2) — `bash docker-shell.sh` works; the unchanged build fails in this sandbox at the Helm step (§6 G3), so the capture uses the capture-only Dockerfile without Helm and says so. Extra checks worth capturing inside: `aws --version` (2.39.6 at the time of recording), `ansible --version` (core 2.13.13, §6 G1), `docker --version` (CLI 28.1.1), `ansible-inventory -i inventory.yml --graph`, and `aws sts get-caller-identity` up to its error with dummy keys (`InvalidClientTokenId`).

### Part C — registry and images (`README.md:79-90`)
11. **Create three empty private ECR repositories** in `us-east-1` (`:81-85`): `cheese-app-vector-db-cli`, `cheese-app-api-service`, `cheese-app-frontend-react`. Capture: `illustration`. Not in README, CLI alternative: `aws ecr create-repository --repository-name <name> --region us-east-1` (needs `ecr:CreateRepository`, which the README's policy lacks; a console user with admin rights can run it).
12. **`ansible-playbook deploy-docker-images.yml -i inventory.yml`** (`:89`). Tasks (`deploy-docker-images.yml:8-60`): ECR login → timestamp → build+push frontend, api-service, vector-db-cli (each with `platform: linux/amd64/v2`) → save `.docker-tag` → `docker system prune -a`. Capture: real up to its first error: with dummy keys, task "Login to AWS ECR" fails with `UnrecognizedClientException … The security token included in the request is invalid.` followed by `Error: Cannot perform an interactive login from a non TTY device` (captured 2026-11-08; the second line is `docker login` receiving an empty password). What success looks like: `expected`/described only (the README documents no output).

### Part D — the machine (`README.md:92-103`)
13. **`ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present`** (`:94`). Tasks (`deploy-create-instance.yml`): security group `app_security_group` 80/443/22 from `0.0.0.0/0` (`:7-24`); EBS 50 GB gp3 in `us-east-1a` (`:27-37`); EC2 instance (`:40-61`, no `when:`); wait for `running` (`:65-74`); wait for SSH (`:76-82`); attach the EBS volume at `/dev/sdf` (`:85-92`); a second SSH wait (`:102-104`); `add_host` (`:106-108`). Capture: real up to its first error: task "Create security group" → `AuthFailure … AWS was not able to validate the provided access credentials` (captured with dummy keys). The heading says "in GCP" (§10 E1).
14. **Copy the instance's public IP** from the console into `inventory.yml` under `appserver: hosts:` (`README.md:97`; `inventory.yml:27-30`). Capture: `illustration` + code panel with `<EXTERNAL_IP>:`. Extra (not in README): `aws ec2 describe-instances --filters Name=tag:Name,Values=cheese-app-demo --query "Reservations[].Instances[].PublicIpAddress"`.
15. **`ansible-playbook deploy-provision-instance.yml -i inventory.yml`** (`:102`). 38 tasks (`--list-tasks`, captured): remove old Docker apt sources, import Docker's GPG key, add the Docker repo (code name from `lsb_release -cs`, or `focal` for releases not in the list, `:18-28`), install `docker-ce`, format `/dev/xvdf` if empty and mount it at `/mnt/disk-1` (`:159-176`), disable unattended upgrades, `apt upgrade`, install python3-docker etc., install AWS CLI v2, `aws configure` with your keys (`:288-292`), start Docker. Capture: `--list-tasks` and `--syntax-check` are real; a run needs a reachable host: show the command, then `illustration`/described (an SSH-unreachable error to a documentation IP such as `203.0.113.10` could be captured as the honest first error).

### Part E — containers and web server (`README.md:105-143`)
16. **Switch the key line** (`:107-111`): for a laptop run, comment out `inventory.yml:4` and uncomment `:7`. Capture: code panel.
17. **`ansible-playbook deploy-setup-containers.yml -i inventory.yml`** (`:116`). Tasks (`deploy-setup-containers.yml:16-207`): debug prints, `/srv/secrets/aws-credentials`, network `appnetwork`, `/mnt/disk-1/persistent` and `/mnt/disk-1/chromadb` (mode 0777), copy `.docker-tag`, ECR login on the VM, choose the tag, pull three images, start `frontend` (3000, `NEXTAUTH_SECRET`/`NEXTAUTH_URL`), start `vector-db` (`chromadb/chroma:latest`, 8000), run the loader once, start `api-service` (9000, AWS keys, `S3_BUCKET_NAME`, Chroma host/port, two volumes), print network info. Capture: `--syntax-check` real; run: show command + `illustration`. Watch for §6 G10 (Chroma `latest`) and G11 (embedding size) in the narration of what to expect.
18. **Inspect on the server** (`:120-132`): SSH in, then `sudo docker container ls`, `sudo docker container logs api-service -f`, `… frontend -f`, `… nginx -f`, `sudo docker exec -it api-service /bin/bash`, `sudo docker exec -it nginx /bin/bash`. The README says "from the GCP console" (§10 E2); on AWS: `ssh -i secrets/<key>.pem ubuntu@<EXTERNAL_IP>` or EC2 Instance Connect. Capture: commands shown; output `illustration` or described. (The `nginx` lines only work after step 20; the README lists them here.)
19. **"Configure Nginx file"** (`:136-137`): the file already exists, `nginx-conf/nginx/nginx.conf`. Capture: code panel `nginx.conf:34-55`.
20. **`ansible-playbook deploy-setup-webserver.yml -i inventory.yml`** (`:141`): ensure `appnetwork`, copy `./nginx-conf/nginx` → `/conf`, start `nginx:stable` on 80/443 with `/conf/nginx/nginx.conf` mounted, restart it. Capture: `--syntax-check` real; run: `illustration`.
21. **Open `http://<External IP>/`** (`:143`). Capture: `illustration` (schematic browser), never a screenshot of someone's live app. Extra that *can* be captured locally: the nginx routing itself, by running `nginx:stable` with this `nginx.conf` and two tiny stand-in containers named `api-service` and `frontend` on a local network, then `curl localhost/api/x` vs `curl localhost/` — tag `extra`.

### Part F — CI/CD with GitHub Actions (not in the README; `.github/workflows/ci_cd_aws.yml`)
22. **Add four repository secrets** (Settings → Secrets and variables → Actions → New repository secret): `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`, `AWS_SSH_KEY` (the whole `.pem` text). Names from `ci_cd_aws.yml:21-22`, `:33`, `:81`, `:102-108`. The README never lists them (§10 E4). Capture: `illustration`.
23. **Commit the inventory with your VM's IP and the CI key line active** (`inventory.yml:4` as shipped), because the runner reads the committed file.
24. **Push with the keyword:** `git commit -m "… /run-deploy-app"` then `git push` to `main`. What runs (`ci_cd_aws.yml`): echo context (`:12-15`) → checkout (`:16-17`) → AWS credentials (`:18-23`) → `aws sts get-caller-identity` and `aws s3 ls` (`:25-28`) → ECR login (`:30-33`) → `ls` (`:38-40`) → build the toolbox (`:41-44`) → timestamp to `.docker-tag` and `$GITHUB_ENV` (`:46-50`) → build/tag/push frontend, vector-db-cli, api-service (`:52-70`) → write `~/.ssh/config` and `~/.ssh/ac215_2024.pem` from `AWS_SSH_KEY`, copy both into `src/deployment/secrets/` (`:72-90`) → list them (`:92-97`) → **only with `/run-deploy-app`:** run the toolbox with the socket, `src/deployment` at `/deployment`, the secrets at `/root/.ssh`, fix permissions, ECR login, `deploy-setup-containers.yml` with `--extra-vars` and `-vv`, then `deploy-setup-webserver.yml` (`:99-131`). Capture: the workflow file as code panels; the local git commit with the keyword can be captured in a scratch repo; the run itself is `illustration` (no Actions run is ours to show).
25. **Verify:** reload `http://<EXTERNAL_IP>/`; on the VM, `sudo docker container ls` shows the new tag in the IMAGE column.

### Part G — teardown (`README.md:145-148`, plus what is missing)
26. **`ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent`** (`:147`). Capture: real, and it fails locally: "Create security group" and "Create EBS volume" are skipped, then "Create EC2 instance" fails with `The task includes an option with an undefined variable. The error was: 'dict object' has no attribute 'group_id'` (captured 2026-11-08). Nothing is deleted (§6 G9).
27. **Manual cleanup** (not in README): terminate instance `cheese-app-demo`; delete the 50 GB volume `cheese-app-demo-disk`; delete security group `app_security_group`; delete the ECR repositories (or their images); deactivate/delete the access key; delete the key pair; remove the four GitHub secrets. Capture: `illustration` checklist with a GOLD cost tag.

## 5. Code tour

### Key files
| Path | Lines | Role |
| --- | --- | --- |
| `README.md` | 148 | the AWS deployment steps |
| `.github/workflows/ci_cd_aws.yml` | 131 | the CI/CD workflow |
| `src/deployment/Dockerfile` | 65 | the toolbox image |
| `src/deployment/docker-shell.sh` | 49 | start the toolbox on a laptop |
| `src/deployment/inventory.yml` | 30 | hosts and variables |
| `src/deployment/deploy-docker-images.yml` | 60 | build and push |
| `src/deployment/deploy-create-instance.yml` | 108 | security group, EBS, EC2 |
| `src/deployment/deploy-provision-instance.yml` | 297 | Docker, disk, AWS CLI on the VM |
| `src/deployment/deploy-setup-containers.yml` | 208 | the app's containers |
| `src/deployment/deploy-setup-webserver.yml` | 38 | nginx |
| `src/deployment/nginx-conf/nginx/nginx.conf` | 57 | routes |
| `src/deployment/docker-entrypoint.sh`, `docker-entrypoint_working.sh` | 52, 55 | unused (ENTRYPOINT commented out) |

### Excerpt 1: the trigger (`ci_cd_aws.yml:3-9`)
```yaml
on:
  push:
    branches: [ "main" ]

jobs:
  Explore-GitHub-Actions:
    if: contains(github.event.head_commit.message, '/run-')
```
and the second sieve (`:99-100`):
```yaml
      - name: Run Deployment Container
        if: contains(github.event.head_commit.message, '/run-deploy-app')
```

### Excerpt 2: logging in to AWS in CI (`ci_cd_aws.yml:18-33`)
```yaml
      - name: Configure AWS Credentials
        uses: aws-actions/configure-aws-credentials@v4
        with:
          aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
          aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
          aws-region: us-east-1  
          
      - name: Verify AWS Credentials
        run: |
          aws sts get-caller-identity
          aws s3 ls

      - name: Login to Amazon ECR
        id: login-ecr
        run: |
          aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com
```

### Excerpt 3: one image, one timestamp (`ci_cd_aws.yml:46-58`)
```yaml
      - name: Generate Docker tag
        run: |
          echo $(date +%Y%m%d%H%M%S) > ${{ github.workspace }}/src/deployment/.docker-tag
          export DOCKER_TAG=$(cat ${{ github.workspace }}/src/deployment/.docker-tag)
          echo "DOCKER_TAG=$DOCKER_TAG" >> $GITHUB_ENV
      
      - name: Build and Push Docker Images
        run: |
          # Frontend React
          cd ${{ github.workspace }}/src/frontend-react/
          docker build -t cheese-app-frontend-react -f Dockerfile .
          docker tag cheese-app-frontend-react:latest ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/cheese-app-frontend-react:${{ env.DOCKER_TAG }}
          docker push ${{ secrets.AWS_ACCOUNT_ID }}.dkr.ecr.us-east-1.amazonaws.com/cheese-app-frontend-react:${{ env.DOCKER_TAG }}
```
(`:60-70` repeat this for `vector-db` and `api-service`.)

### Excerpt 4: running the toolbox in CI (`ci_cd_aws.yml:113-131`)
```yaml
          docker run --rm --name cheese-app-deployment \
            -v /var/run/docker.sock:/var/run/docker.sock \
            -v ${{ github.workspace }}/src/deployment:/deployment \
            -v ${{ github.workspace }}/src/deployment/secrets:/root/.ssh \
            -e AWS_ACCESS_KEY_ID \
            -e AWS_SECRET_ACCESS_KEY \
            -e AWS_DEFAULT_REGION \
            -e AWS_ACCOUNT_ID \
            -e DOCKER_TAG \
            cheese-app-deployment \
            /bin/bash -c "cd /deployment && \
```
…then (`:124-131`) `chown`/`chmod` of `/root/.ssh`, `ls -la /root/.ssh`, ECR login, `ANSIBLE_STDOUT_CALLBACK=debug ansible-playbook deploy-setup-containers.yml -i inventory.yml --extra-vars "… docker_tag=$DOCKER_TAG" -vv`, `ansible-playbook deploy-setup-webserver.yml -i inventory.yml`. `-e NAME` with no value copies the variable from the step's `env:` (`:101-108`).

### Excerpt 5: reading the CSV (`docker-shell.sh:9-21`, account id masked)
```bash
# Read AWS credentials from CSV file
CSV_FILE="../../../../secrets/deployment-ac215-user_accessKeys.csv"
if [ -f "$CSV_FILE" ]; then
    # Skip the header line and read the second line, removing any quotes and whitespace
    IFS=',' read -r AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY <<< "$(sed -n '2p' "$CSV_FILE" | tr -d '"' | tr -d ' ')"
    export AWS_ACCESS_KEY_ID=$(echo "$AWS_ACCESS_KEY_ID" | tr -d '\r')
    export AWS_SECRET_ACCESS_KEY=$(echo "$AWS_SECRET_ACCESS_KEY" | tr -d '\r')
    export AWS_DEFAULT_REGION="us-east-1"
    export AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"
else
    echo "Error: AWS credentials file not found at $CSV_FILE"
    exit 1
fi
```
`<<<` (here-string) is a bash feature: this is the line `dash` rejects (§6 G2).

### Excerpt 6: the toolbox run on a laptop (`docker-shell.sh:32-48`)
```bash
docker build -t $IMAGE_NAME --platform=linux/amd64 -f Dockerfile .

# Run the container
docker run --rm --name $IMAGE_NAME -ti \
-v /var/run/docker.sock:/var/run/docker.sock \
-v "$BASE_DIR":/app \
-v "$SECRETS_DIR":/secrets \
-v "$HOME/.ssh":/home/app/.ssh \
-v "$BASE_DIR/../api-service":/api-service \
-v "$BASE_DIR/../frontend-react":/frontend-react \
-v "$BASE_DIR/../vector-db":/vector-db \
-e AWS_ACCESS_KEY_ID=$AWS_ACCESS_KEY_ID \
-e AWS_SECRET_ACCESS_KEY=$AWS_SECRET_ACCESS_KEY \
-e AWS_DEFAULT_REGION=$AWS_DEFAULT_REGION \
-e AWS_ACCOUNT_ID=$AWS_ACCOUNT_ID \
-e SSH_KEY_PATH=$SSH_KEY_PATH \
$IMAGE_NAME
```
The container runs as root (the Dockerfile creates user `app` at `:39-42` but never switches to it), so `/home/app/.ssh` is not root's `~/.ssh`; Ansible uses the explicit key path from the inventory anyway. `SSH_KEY_PATH` is exported but nothing reads it; the inventory's local line reads `AWS_SSH_KEY` and falls back to `/secrets/ac215_2024.pem` (`inventory.yml:7`).

### Excerpt 7: the inventory (`inventory.yml:1-30`, masked)
```yaml
all:
  vars:
    ansible_user: ubuntu
    ansible_ssh_private_key_file: "/root/.ssh/ac215_2024.pem" ## Github Actions

    ## from local mac
    # ansible_ssh_private_key_file: "{{ lookup('env', 'AWS_SSH_KEY') | default('/secrets/ac215_2024.pem', true) }}"   
    ansible_ssh_common_args: '-o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null'
    aws_access_key: "{{ lookup('env','AWS_ACCESS_KEY_ID') }}"
    aws_secret_key: "{{ lookup('env','AWS_SECRET_ACCESS_KEY') }}"
    aws_account_id: "{{ lookup('env','AWS_ACCOUNT_ID') }}"
    aws_application_credentials: "/secrets/deployment-ac215-user_accessKeys.csv"

    aws_region: "us-east-1"
    aws_instance_type: "t2.large"
    aws_keypair_name: "ac215_2024"  ## Change this 
    aws_ami_id: "ami-0e86e20dae9224db8"  
    docker_network_name: "appnetwork"
    machine_instance_name: "cheese-app-demo"
    machine_disk_size: 100
    persistent_disk_name: "cheese-app-demo-disk"
    persistent_disk_size: 50
    aws_instance_name: "cheese-app-demo"
    nextauth_secret: "<nextauth-secret>"
    nextauth_url: "http://{{ inventory_hostname }}"

  children:
    appserver:
      hosts:
        <EXTERNAL_IP>:
```
Unused at this commit: `aws_application_credentials`, `machine_instance_name`, `nextauth_url` (the container gets `NEXTAUTH_URL` directly, `deploy-setup-containers.yml:145`).

### Excerpt 8: build and push with Ansible (`deploy-docker-images.yml:1-30`)
```yaml
- name: "Build docker images and push them to ECR"
  hosts: localhost
  gather_facts: false
  vars:
    aws_account_id: "{{ lookup('env','AWS_ACCOUNT_ID') }}"
    ecr_registry: "{{ aws_account_id }}.dkr.ecr.{{ aws_region }}.amazonaws.com"
  tasks:
  - name: Login to AWS ECR
    shell: "aws ecr get-login-password --region {{ aws_region }} | docker login --username AWS --password-stdin {{ ecr_registry }}"

  - name: "Get timestamp for docker tag"
    shell: "(date +%Y%m%d%H%M%S)"
    register: tag
  - name: Print tag
    debug:
      var: tag

  - name: Build frontend container image
    community.general.docker_image:
      build:
        path: /frontend-react
        platform: linux/amd64/v2
      name: "{{ ecr_registry }}/cheese-app-frontend-react:{{ tag.stdout}}"
      source: build
  - name: Push frontend image to ECR
    community.general.docker_image:
      name: "{{ ecr_registry }}/cheese-app-frontend-react:{{ tag.stdout}}"
      repository: "{{ ecr_registry }}/cheese-app-frontend-react:{{ tag.stdout}}"
      push: yes
      source: local
```
`community.general.docker_image` is a redirect to `community.docker.docker_image`; at build time today the playbook prints a deprecation warning that the redirect "will be removed in community.general 18.0.0" (captured from `--syntax-check`).

### Excerpt 9: create, and the teardown that cannot work (`deploy-create-instance.yml:39-46`, `:94-100`)
```yaml
    # # Replace GCP instance with EC2 instance
    - name: Create EC2 instance
      amazon.aws.ec2_instance:
        instance_type: "{{ aws_instance_type }}"
        image_id: "{{ aws_ami_id }}"
        region: "{{ aws_region }}"
        security_group: "{{ security_group.group_id }}"
        key_name: "{{ aws_keypair_name }}"
```
```yaml
    # Replace GCP disk removal with EBS volume removal
    - name: Remove EBS volume
      ec2_vol:
        region: "{{ aws_region }}"
        id: "{{ ebs_volume.volume_id }}"
        state: absent
      when: cluster_state == "absent"
```
The create task has no `when:` and no `state:`; nothing in the file terminates the instance.

### Excerpt 10: pick the tag, run the containers (`deploy-setup-containers.yml:101-114`, `:131-145`)
```yaml
    - name: Set docker tag from environment if available
      set_fact:
        docker_tag: "{{ lookup('env', 'DOCKER_TAG') }}"
      when: lookup('env', 'DOCKER_TAG') != ""

    - name: Set docker tag from file if environment variable is not set
      block:
        - name: Read docker tag from file
          shell: "cat .docker-tag"
          register: tag_file
        - name: Set docker tag from file
          set_fact:
            docker_tag: "{{ tag_file.stdout }}"
      when: lookup('env', 'DOCKER_TAG') == ""
```
```yaml
    - name: Create frontend container
      docker_container:
        name: "frontend"
        image: "{{ aws_account_id }}.dkr.ecr.{{ aws_region }}.amazonaws.com/cheese-app-frontend-react:{{ docker_tag }}"
        state: started
        recreate: yes
        pull: yes
        restart: yes
        published_ports:
          - 3000:3000
        networks:
          - name: "{{docker_network_name}}"
        env:
          NEXTAUTH_SECRET: "{{ nextauth_secret }}"  
          NEXTAUTH_URL: "http://{{ inventory_hostname }}"  
```
`lookup('env', …)` reads the environment of the *controller* (the toolbox), not of the VM. `cat .docker-tag` runs on the VM, in the SSH user's home, where `:67-71` copied the file.

### Excerpt 11: the loader run (`deploy-setup-containers.yml:164-173`)
```yaml
    - name: Load Vector DB
      shell: docker run --rm -it 
        -e AWS_ACCESS_KEY_ID="{{ aws_access_key }}" 
        -e AWS_SECRET_ACCESS_KEY="{{ aws_secret_key }}" 
        -e AWS_DEFAULT_REGION="{{ aws_region }}"
        -e CHROMADB_HOST="vector-db" 
        -e CHROMADB_PORT="8000" 
        --network "{{docker_network_name}}" 
        "{{ aws_account_id }}.dkr.ecr.{{ aws_region }}.amazonaws.com/cheese-app-vector-db-cli:{{ docker_tag }}" 
        cli.py --download --load --chunk_type recursive-split
```
The image's entrypoint turns the arguments into `pipenv run python cli.py --download --load --chunk_type recursive-split` (`src/vector-db/docker-entrypoint.sh:5-13`).

### Excerpt 12: the routes (`nginx.conf:34-55`)
```nginx
		# API - Make this location block handle all /api paths
		location ^~ /api/ {
			# Remove the rewrite since we want to preserve the full path after /api/
			proxy_pass http://api-service:9000/;
```
```nginx
		# Frontend
		location / {
			proxy_pass http://frontend:3000;
```
(each block also sets `X-Forwarded-For`, `X-Forwarded-Proto`, `X-Real-IP`, `Host`, `proxy_redirect off`, `proxy_buffering off`.)

### Excerpt 13: the toolbox Dockerfile's install line (`Dockerfile:31-37`)
```dockerfile
RUN curl -fsSL https://pkgs.k8s.io/core:/stable:/v1.28/deb/Release.key | gpg --dearmor -o /etc/apt/keyrings/kubernetes-apt-keyring.gpg && \
    echo 'deb [signed-by=/etc/apt/keyrings/kubernetes-apt-keyring.gpg] https://pkgs.k8s.io/core:/stable:/v1.28/deb/ /' | tee /etc/apt/sources.list.d/kubernetes.list  && \
    curl https://baltocdn.com/helm/signing.asc | apt-key add -&& \
    echo "deb https://baltocdn.com/helm/stable/debian/ all main" | tee /etc/apt/sources.list.d/helm-stable-debian.list && \
    apt-get update && \
    apt-get install -y --no-install-recommends kubectl helm python3.9 python3-pip && \
    pip install ansible>=9.0.0 openshift docker apache-libcloud boto3 botocore pipenv
```

## 6. Gotchas and common errors

Verified ones first; *(reasoned, not run)* marks the rest.

- **G1. `pip install ansible>=9.0.0` is a shell redirect, not a version pin** (`Dockerfile:37`). Unquoted, `>=9.0.0` sends pip's output to a file named `=9.0.0` in `/` and installs whatever pip picks. Captured: the file `/=9.0.0` exists in the built image and holds pip's log; the image has **ansible 6.7.0 / ansible-core 2.13.13** on Python 3.8.10 (`pip3 show ansible`, `ansible --version`). Fix: `pip install "ansible>=9.0.0"` — but ansible 9 needs a newer Python than Ubuntu 20.04's 3.8, so the honest fix is a newer base image. Side effect worth knowing: `deploy-provision-instance.yml:56-57` uses `args: warn: false`, which ansible-core 2.14+ rejects; it only works *because* the pin failed.
- **G2. `sh docker-shell.sh` fails on Linux** (`README.md:77`, `docker-shell.sh:13`). On Debian/Ubuntu `sh` is `dash`, which has no `<<<`: captured `head.sh: 13: Syntax error: redirection unexpected`, exit 2. On macOS `sh` is bash and it works. Fix: `bash docker-shell.sh`. (The shebang is `#!/bin/bash`, `:1`, but `sh file` ignores shebangs.)
- **G3. The unchanged toolbox build failed here at the Helm repository** (`Dockerfile:33-34`): `curl https://baltocdn.com/helm/signing.asc` → `SSL certificate problem: unable to get local issuer certificate`, then `gpg: no valid OpenPGP data found`, exit 2. In this sandbox `baltocdn.com` is not intercepted by the proxy; it presents a Let's Encrypt certificate issued by intermediate `YR1` (valid 2026-09-16 to 2026-12-15) that the sandbox's CA bundle cannot chain. Whether a student's machine hits the same error was not determined (open question). Helm is not used by any playbook in this repo, so the capture build drops those two lines and says so in ASSETS.md.
- **G4. The README's CSV path and the script's disagree** (`README.md:76` three `../`, `docker-shell.sh:10` four). With the README's folder layout (`:56-59`), three is right. The README tells you to edit this line; it does not tell you that `SECRETS_DIR` (`docker-shell.sh:26`) has the same four `../` and also needs editing, or `/secrets` in the toolbox will be empty.
- **G5. The account id is hard-coded** (`docker-shell.sh:17`). Leave it and the ECR login and every image name point at someone else's registry (`AccessDenied`/`not authorized` on push). Not mentioned in the README. Fix: your own id (`aws sts get-caller-identity --query Account --output text`).
- **G6. Three names for one key pair.** README `cheese-app-ac215-key-pair` (`:64`), inventory `aws_keypair_name: "ac215_2024"` (`inventory.yml:16`), key file `ac215_2024.pem` (`inventory.yml:4`, `:7`, `ci_cd_aws.yml:81-90`, `:126`). `key_name` must match the key pair's name in EC2, and the file path must match where the `.pem` is. Easiest: name the key pair `ac215_2024` or change all of them.
- **G7. SSH refuses a world-readable key** *(standard OpenSSH behaviour, not run here)*: "UNPROTECTED PRIVATE KEY FILE!" if the `.pem` is not `chmod 400`/`600`. The CI step does this for its copy (`ci_cd_aws.yml:84-85`, `:124-127`); on a laptop you do it yourself.
- **G8. The local/CI key line is a manual toggle** (`README.md:107-111`, `inventory.yml:4`/`:7`). The committed file is set for GitHub Actions; a laptop run with it fails to find `/root/.ssh/ac215_2024.pem`. Remember to switch it back before pushing, or CI will look in `/secrets`.
- **G9. Teardown does not tear anything down** (`README.md:147`). With `cluster_state=absent` the security-group and EBS tasks are skipped, so `security_group.group_id` is undefined when the un-gated "Create EC2 instance" task (`deploy-create-instance.yml:40-61`) renders its arguments. Captured: `fatal: … 'dict object' has no attribute 'group_id'`, before any AWS call. Even past that, `Remove EBS volume` needs `ebs_volume.volume_id`, which is only registered on `present`, and no task terminates the instance *(reasoned, not run)*. Delete by hand (§4 step 27).
- **G10. `chromadb/chroma:latest` on the server vs `chromadb==0.5.18` in the clients** (`deploy-setup-containers.yml:151`; `src/vector-db/Pipfile.lock`, `src/api-service/Pipfile.lock`; the local compose file pins `chromadb/chroma:0.5.18`, `src/vector-db/docker-compose.yml:25`). Captured on 2026-11-08: today's `latest` reports version `1.0.0` and answers `/api/v1/heartbeat` with HTTP 410 `{"error":"Unimplemented","message":"The v1 API is deprecated. Please use /v2 apis"}`; the 0.5.x client speaks `/api/v1`. So a deploy today should fail at "Load Vector DB", and the API (which connects at import time, `llm_rag_utils.py:73-77`) should fail to start *(the last two: reasoned, not run)*. Fix: pin the server to `chromadb/chroma:0.5.18`, as the compose file does.
- **G11. The downloaded embeddings do not match the AWS embedding model.** `cli.py --download` fetches `cheese-books-embeddings.zip` (v4.0 release, `src/vector-db/cli.py:470-487`): inspected, its `outputs/embeddings-recursive-split-*.jsonl` rows carry 256-number vectors (the GCP pipeline's size; `cli.py:41` keeps the GCP comment `# EMBEDDING_DIMENSION = 256`). The API embeds each question with Titan `amazon.titan-embed-text-v1` (`llm_rag_utils.py:21`, `:79-86`), which `cli.py:36` itself says is 1536-dimensional. A 1536-number query against a 256-dimension collection is rejected by Chroma *(reasoned, not run)*. The RAG chat route cannot work as committed; the plain LLM chat (`/llm`) does not use Chroma.
- **G12. `llm_rag_utils.py` uses `json` without importing it** (`:81`, `:86`, `:124`, `:137`; the imports are `:1-13`). Every RAG chat request raises `NameError`, caught and returned as HTTP 500 (`:145-151`) *(read, not run)*. Same file: `generation_config["max_tokens"]` (`:127`) is not a key of `generation_config` (`:34-38` has `max_output_tokens`). App bugs, not deployment bugs: one sentence in the video, if any.
- **G13. `docker run -it` inside an Ansible `shell` task** (`deploy-setup-containers.yml:165`). Docker refuses `-t` when stdin is not a terminal (captured locally with Docker 29: `cannot attach stdin to a TTY-enabled container because stdin is not a terminal`, exit 1; older Docker prints `the input device is not a TTY`). Whether Ansible's SSH session gives this task a terminal (its SSH plugin requests one with `-tt` by default) was not tested. If the task fails, drop `-it`: the loader needs no terminal.
- **G14. `docker system prune -a` at the end of the build playbook** (`deploy-docker-images.yml:59-60`, named "Remove all unused containers"). Without `-f` it asks for confirmation; with no input it answers no and exits 0 (captured in the toolbox image's Docker CLI with stdin at EOF: prompt, then `[exit 0]`). If it ever did run, it would prune **your laptop's** images (the socket is the host's), not the toolbox's.
- **G15. The 50 GB volume and the instance's own second disk both want `/dev/sdf`** *(reasoned, not run)*. `ec2_instance` already maps a 100 GB gp2 volume at `/dev/sdf` (`deploy-create-instance.yml:53-57`), then "Attach EBS volume" asks for `/dev/sdf` again (`:85-92`). Expect the attach to fail ("already in use"), leaving the 50 GB volume detached and billed; the provision playbook then formats and mounts the instance's own `/dev/xvdf` (on Xen-based `t2`, `sdf` appears as `xvdf`), which is deleted with the instance. The EBS volume is also pinned to `us-east-1a` (`:30`) while the instance may launch in any zone of the default VPC.
- **G16. "Wait for SSH" waits on the instance's public IP from inside the toolbox** (`:76-82`, repeated `:102-104`). If your laptop's network blocks outbound 22, the play times out after 120 s even though the instance is fine *(reasoned)*.
- **G17. A `/run-` commit without `deploy-app` still pushes images.** The job condition is `/run-` (`ci_cd_aws.yml:9`); only the last step needs `/run-deploy-app` (`:100`). Every such push adds three images to ECR (storage cost) and leaves the VM on the old tag.
- **G18. CI deploys to whatever IP is committed.** The runner uses `inventory.yml` from the commit: if the instance was recreated (new public IP) and the file was not updated, `deploy-setup-containers.yml` fails with an SSH timeout *(reasoned)*. Public IPs change when an instance is stopped and started.
- **G19. Ports 3000, 8000, 9000 are published on the VM** (`deploy-setup-containers.yml:139-140`, `:154-155`, `:181-182`) but closed by the security group (`deploy-create-instance.yml:12-21` opens only 80, 443, 22). Good: everything goes through nginx. Port 443 is open and nginx publishes it, but `nginx.conf` has only a `listen 80` server: there is no HTTPS (`nginx.conf:25-27`).
- **G20. SSH open to the world** (`deploy-create-instance.yml:19-21`: port 22 from `0.0.0.0/0`). Fine for a class demo; in practice restrict to your IP.
- **G21. Secrets in the repo.** A `NEXTAUTH_SECRET` is committed twice (`inventory.yml:24`, `.env.production:3`) and an account id once (`docker-shell.sh:17`). Generate your own (`openssl rand -base64 32`) and never commit access keys: the `secrets/` folder sits *outside* the clone for this reason (`README.md:56-59`). In CI, `src/deployment/secrets/` is created on the runner only (`ci_cd_aws.yml:88-90`) and never committed.

## 7. Where this sits in the course

### What the lecture's GCP version does, and how this repo differs (slides 17–20)
The slides present `dlops-io/cheese-app-v4` (`033f187`): two workflows, `app-ci-cd-gcp.yml` (job gated by `/deploy-app`, `cheese-app-v4/.github/workflows/app-ci-cd-gcp.yml:9`) and `ml-ci-cd-gcp.yml` (job gated by `/run-`, step-level `/run-data-collector`, `/run-data-processor`, `/run-ml-pipeline`, `ml-ci-cd-gcp.yml:9`, `:37`, `:57`, `:77`). GitHub authenticates to GCP with a service-account key stored as secret `GOOGLE_APPLICATION_CREDENTIALS` (`cheese-app-v4/README.md:133-145`; `app-ci-cd-gcp.yml:18-21`), builds the deployment container and runs `pulumi up` twice (`deploy-k8s-update.sh:4`, `:9`) to push images and roll the GKE Deployments. `cheese-app-v4/README.md:157`: "The CI part is not implemented in this tutorial."

The AWS repo keeps the pattern — commit keyword → runner → same toolbox container → deploy with the new timestamp tag — and swaps every component (table in C8). Two differences the video should say out loud, kindly:
1. **No Kubernetes and no Pulumi:** one VM with Docker containers managed by Ansible. The slides' "deploy to the K8s cluster" becomes "recreate the containers on the VM".
2. **No ML lane:** nothing in this repo runs a training pipeline; the slides' Vertex AI arc (slides 17–19) has no AWS counterpart here. L15's `ml-workflow-aws` (SageMaker Pipelines) is the AWS ML pipeline of this series.

### What earlier lectures gave you
- Containers and `docker-shell.sh` pattern (L02 onward); the cheese app's frontend/API/vector-db services (the app lectures); RAG with Chroma (the LLM lectures); the deployment container and Ansible on a single VM appear in the course's earlier deployment tutorials; Pulumi (L20) and Kubernetes (L22) are the GCP path this AWS variant does *not* use; GitHub Actions basics (L21, `cheese-app-ci-cd`). Lecture numbers for the review slides 21–37 are in `SLIDES.md` (they print another year's numbers).

## 8. Video plan (suggestion)

Two parts, 25–35 minutes, ~4,000 words. Part 1 = the README by hand (concepts C3, C4, C6, C7); Part 2 = the push button (C1, C2, C5) and the review.

**Part 1 — Deploy by hand with Ansible**
1. Hook (1.5 min): `git commit -m "/run-deploy-app"` and a server changes — how? Then the honest hook: the README's own delete command fails (show the captured error at the end of Part 2 as the payoff).
2. The final picture (2 min): slide 19's map, redrawn for AWS (C8 table as a transform from GCP labels to AWS labels).
3. Identity (3 min, V: key journey C6): policy, user, access key CSV, key pair; mask everything; G6 name mismatch.
4. The toolbox (3 min, V: sibling containers C3): `docker-shell.sh` excerpt, G2 (`sh` vs `bash`, captured), G4/G5 edits, G1 redirect (captured `/=9.0.0`), in-container versions.
5. Ansible in one picture (2.5 min, V: inventory → play → task → module C4), `ansible-inventory --graph`, `--syntax-check`.
6. Build and push (2.5 min, V: timestamp C5 first half): ECR repos (illustration), `deploy-docker-images.yml` up to its captured first error.
7. Create and provision (3 min): `deploy-create-instance.yml` (captured AuthFailure), IP into inventory, provision task list; G15 as a short "watch out".
8. Containers and nginx (3.5 min, V: one VM, five containers C7): setup-containers, the `/api/` prefix strip (local nginx demo `extra`), G10 Chroma `latest` (captured 410).
**Part 2 — Let GitHub press the button**
9. CI vs CD (2 min, slides 7–12): loop with the test gates greyed out.
10. Two sieves (2.5 min, V: C2): trigger excerpt; ponder.
11. Secrets and the runner (2.5 min): four secrets (illustration), the SSH-key step, Excerpt 4.
12. Follow one tag (2.5 min, V: C5 complete): runner → ECR → VM → recreated containers; not a rolling update (contrast v4).
13. Teardown and cost (2.5 min): captured G9 error, manual checklist, GOLD tag.
14. Review and recap (2 min): slides 21–37 as the course map; what to do next (instance roles, OIDC, tests in CI).

**Ponders (4, quiz-style, timer):**
- After C3: "The toolbox runs `docker build`. Whose disk do the images land on: the toolbox's or your laptop's?" (Laptop: the socket is the host's.)
- After C2: "You push with message `fix typo /run-tests`. What happens: nothing, build-and-push only, or full deploy?" (Build and push only.)
- After C5: "CI sets `DOCKER_TAG` and also copies `.docker-tag`. If both exist and differ, which tag does the VM run?" (The environment variable: `:101-104`; and the extra-var wins anyway.)
- Before G9: "`cluster_state=absent`: which tasks run?" (Instance creation is not gated — and fails on an undefined variable.)

## 9. Exercises
1. **Predict, then run (local):** `sh docker-shell.sh` vs `bash docker-shell.sh` on a Linux machine with a placeholder CSV. Explain the error from the line number.
2. **Find the pin (local):** build the toolbox (drop the Helm lines if needed), then `ls /` and `ansible --version`. Where did `>=9.0.0` go? Rewrite the line so the pin works, and say why it still would not install ansible 9 on this base image.
3. **Trigger table (paper):** for each message — `update readme`, `/run-deploy-app`, `/RUN-DEPLOY-APP`, `test /run-x` — say whether the job runs, whether images are pushed, whether the VM changes.
4. **Routing (local, `extra`):** run `nginx:stable` with the repo's `nginx.conf` on a network with two stand-in containers named `api-service` (port 9000) and `frontend` (port 3000) that echo the request path; `curl localhost/api/newsletters` and `curl localhost/`. Which path does `api-service` see? Remove the trailing `/` from `proxy_pass` and repeat.
5. **Fix the teardown (paper or local `--syntax-check`):** add `when: cluster_state == "present"` to the instance task, add a task that terminates instances tagged `Name: cheese-app-demo` with `state: absent`, and look the volume up by name instead of by a registered id. Run `ansible-playbook … cluster_state=absent` with dummy keys: which task fails now, and with what error?
6. **Think:** list every place the access key ends up (laptop file, env, VM files, container env, GitHub). Which would an EC2 instance role remove? Which would GitHub OIDC remove?
7. **Debug:** the site loads but chat answers with HTTP 500. Using G10–G12, list three checks on the VM (`sudo docker container logs api-service`, the Chroma version endpoint, the collection's dimension) and what each would show.

## 10. Errata and open questions

### Errata (README vs code; state kindly, with the fix)
- **E1.** Headings "Create Compute Instance (VM) Server in GCP" (`README.md:92`) and "Provision Compute Instance in GCP" (`:99`): the playbooks create and provision an **EC2** instance on AWS. Carried over from the GCP README.
- **E2.** "You can SSH into the server from the GCP console" (`:120`): on AWS, `ssh -i <key>.pem ubuntu@<EXTERNAL_IP>` or EC2 Instance Connect in the EC2 console.
- **E3.** CSV path (`:76` vs `docker-shell.sh:10`), plus `SECRETS_DIR` (`:26`) and the hard-coded account id (`:17`) the README does not mention (G4, G5).
- **E4.** The README never mentions the GitHub Actions workflow or its four secrets; the commit keyword `/run-deploy-app` appears only in the workflow and the commit history.
- **E5.** Key-pair name: README `cheese-app-ac215-key-pair` vs code `ac215_2024` (G6).
- **E6.** `sh docker-shell.sh` needs bash (G2).
- **E7.** "Delete the Compute Instance / Persistent disk" (`:145-148`) fails and deletes nothing (G9).
- **E8.** "API's to enable in AWS" (`:7-13`) is empty because its list is commented out; AWS needs no API enablement, but Bedrock model access may be needed (open question).
- **E9.** `Dockerfile:37` pin is a redirect (G1); `Dockerfile:33-34` Helm repo failed to build here (G3).
- **E10.** Chroma server `latest` vs client 0.5.18 (G10); embeddings 256-d vs Titan 1536-d (G11); `json` not imported in `llm_rag_utils.py` (G12).
- **E11.** `/dev/sdf` used twice; EBS volume in a fixed zone (G15) *(reasoned)*.
- **E12.** The workflow is named "Continuous Integration and Continuous Deployment" (`ci_cd_aws.yml:1`) but has no integration tests (C1).

### Open questions (could not determine here)
- Whether `baltocdn.com` (Helm's Debian repo) still serves valid packages to a normal machine today, i.e. whether the unchanged `docker build` and the CI step `ci_cd_aws.yml:41-44` fail for students too.
- Which Ubuntu release `ami-0e86e20dae9224db8` is and whether it is still available in `us-east-1` (needs AWS credentials). The provision playbook falls back to Docker's `focal` repository for any release not in its list (`deploy-provision-instance.yml:18-28`), which would include 24.04 `noble`.
- Whether Bedrock in `us-east-1` still serves `anthropic.claude-3-sonnet-20240229-v1:0` and `anthropic.claude-3-5-sonnet-20240620-v1:0` on 2026-11-08, and whether model access must be requested first; both are older models that may be retired.
- Whether "Load Vector DB" (`docker run -it` under Ansible over SSH) gets a terminal (G13).
- Whether the `/dev/sdf` attach and the `us-east-1a` zone actually fail (G15).
- The course-site file that lists this repo for L23 (`tutorials_demo.md`) is not in this sandbox; the "AWS variant, No K8s" label is taken from the coordinator's lecture entry.
