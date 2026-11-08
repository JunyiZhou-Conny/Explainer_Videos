# AC215 · Lecture 23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys

A follow-along walkthrough of the Lecture 23 tutorial of Harvard's **AC215 (MLOps & LLMOps, Fall
2026)**, *Final Deployment and Review*, in its AWS variant:
[dlops-io/cheese-app-aws](https://github.com/dlops-io/cheese-app-aws), branch `main` (its only branch)
@ [`5950118`](https://github.com/dlops-io/cheese-app-aws/tree/5950118b0ed97c12c799920846d3eb70b1a47385)
("cleanup", 2024-11-21; still the head of `main` on the recording day). The video follows the whole
README top to bottom, step by step (*API's to enable*, *Setup AWS Keys for Authentication*, *Create AWS
EC2 Key Pair*, *Deployment Setup*, *Deployment Steps*, *Create Empty ECR Repositories*, *Build and Push
Docker Containers to AWS ECR*, *Create Compute Instance*, *Provision Compute Instance*, *Setup Docker
Containers*, *Configure Nginx*, *Setup Webserver*, *Delete the Compute Instance*), then the GitHub
Actions workflow `.github/workflows/ci_cd_aws.yml`, which the README never mentions, and the lecture
slide by slide. The lecture's slides speak Google Cloud (GKE, Artifact Registry, Pulumi, the
`cheese-app-v4` repository); as in [Lecture 15](../ac215-l15-vertex-ml-workflows/), this video follows
the course's AWS repository and maps the lecture's terms onto it: one EC2 server running Docker
containers instead of a Kubernetes cluster, ECR instead of Artifact Registry, Ansible playbooks instead
of Pulumi, an IAM access key and an EC2 key pair instead of a service-account key, `/run-deploy-app`
instead of `/deploy-app`, an nginx container instead of an ingress.

This repository has 39 commits, and 33 of them carry the same message: `/run-deploy-app`. Pushed to
`main`, that sentence rebuilds the app and redeploys a server; once the slash leaned the other way and
nothing ran. **Part 1** deploys by hand, as the README does: the IAM policy, user, access key and key
pair; the `cheese-app-deployment` toolbox container and the three surprises of starting it; Ansible's
inventory, plays, tasks and modules; three images and one timestamp tag in ECR; an EC2 server created,
provisioned and filled with five containers behind one nginx front door. **Part 2** lets a commit press
the button: CI and CD in the lecture's words, the workflow's two sieves on one commit message, the four
repository secrets and what the runner does, one tag followed from `date` to a recreated container, the
README's delete that deletes nothing (and the clean-up by hand), and the whole course placed on the
server you deployed.

Watch it with your clone open, Docker running, your own AWS account with billing, and, for part 2, a
GitHub repository of your own; pause at every `▶ your turn` to run the command. **This lecture runs a
server around the clock until you delete it**: GOLD tags name every meter (no prices), and the clean-up
checklist is in S15. The tracker top left shows the README step (or the workflow step, always "not in
the README"); a gray `extra` tag marks a command that isn't in the README, and a gray "Lecture 23 ·
slides …" tag top right points to the lecture slides the scene stands on.

**What is real and what is drawn.** The recording machine has no AWS account. Everything on the laptop
ran for real on 2026-11-08 (a fresh Ubuntu 24.04 laptop with Docker Engine 29.9.3): the clone, the
`secrets/` folder, every `docker-shell.sh` run, the toolbox and, typed at its prompt, all six
`ansible-playbook` commands of the README, verbatim and in README order, each up to its **real first
error** (AWS rejecting obviously fake keys, a server that doesn't exist, or the playbook's own bug).
The workflow's own `run:` scripts ran by hand on the laptop up to their first real error. The AWS
consoles, the server's side, the browser and GitHub's pages are drawings tagged `illustration`; local
stand-ins (Chroma, nginx and its routes) are tagged as stand-ins, never shown as the server. Account
ids, keys and addresses are placeholders only. Details in [`ASSETS.md`](ASSETS.md). Series format:
[`docs/AC215_SERIES.md`](../../docs/AC215_SERIES.md). Study guide with every command:
[MLOps_Learning · guides/L23-final-cicd-deployment.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L23-final-cicd-deployment.md).

English narration; Chinese and bilingual subtitles (中文字幕说明见 [`i18n/zh/README.md`](i18n/zh/README.md)).

| file | what it is |
| --- | --- |
| `output/ac215-l23-final-cicd.zh-en.mp4` | **the copy to watch**: 1080p60, English narration, bilingual subtitles (Chinese above, English below) burned in, DURATION_FULL. Published as a GitHub release asset: no MP4 is kept in Git ([`docs/PUBLISHING.md`](../../docs/PUBLISHING.md)) |
| `output/ac215-l23-final-cicd.mp4` | the same video without burned-in subtitles; load any `.srt` below in your player. Release asset, not in Git: rebuild it with `--no-render` (see Rebuild) |
| `output/ac215-l23-final-cicd_part1.mp4` | part 1, DURATION_P1: deploy by hand — IAM keys, the Ansible toolbox, ECR, one EC2 server and nginx (S01–S10). Release asset, not in Git |
| `output/ac215-l23-final-cicd_part2.mp4` | part 2, DURATION_P2: let a commit press the button — CI/CD in the lecture's words, the GitHub Actions workflow, teardown and the course review (S11–S16). Release asset, not in Git |
| `output/ac215-l23-final-cicd.srt` | English subtitles (each part has its own `.srt`, `.zh.srt`, `.zh-en.srt` / `.ass`) |
| `output/ac215-l23-final-cicd.zh.srt` | Chinese subtitles (on the English timing) |
| `output/ac215-l23-final-cicd.zh-en.srt` / `.zh-en.ass` | bilingual subtitles |
| `output/chapters.txt`, `chapters_part1.txt`, `chapters_part2.txt` | chapter timestamps |
| `output/transcript.md` | the full narration by chapter |
| `exercises.md` | do these after watching: the five test-yourself questions and the five ponders, hands-on predict-then-run tasks, debugging and think questions, with answers; what was run to check them is in [`assets/exercise-checks/`](assets/exercise-checks/README.md) |
| `digest.md` | the tutorial digest: every step, a code tour with `path:line`, gotchas, errata, and the GCP-to-AWS term map |
| `SLIDES.md` | the lecture behind the tutorial: a digest of the slides in our own words, with slide numbers, and which scene stands on which slides |
| `assets/terminal/` | the **real** terminal sessions every terminal panel prints from (2026-11-08, `laptop/`: the README's commands, the toolbox, the six playbooks, the workflow's scripts by hand, the local stand-ins); provenance in [`ASSETS.md`](ASSETS.md) |
| `assets/source/` | the tutorial files the code panels quote, unchanged at `5950118` except for the masked values listed in `ASSETS.md` |
| `BRIEF.md`, `script.md`, `scenes/` | the design, the narration (SAY) + visual plan (SHOW), and the Manim source |
| `i18n/zh/` | the Chinese subtitle text: glossary and sentence-aligned translation |

Git keeps the subtitles, the chapter files and the transcript; the MP4s (the burned-in copy, the clean
video and the two part cuts) are release assets.

## Chapters

CHAPTERS

## What you'll learn

Five *pause and ponder* moments ask you to predict before the video shows you: whose disk an image
lands on when Ansible runs `docker build` inside the toolbox; which path `api-service` receives when the
browser asks nginx for `/api/newsletters`; what a push of `fix typo /run-tests` to `main` does; whether
typing `/run-deploy-app` is continuous delivery or continuous deployment, and what would make it the
other; and which tasks of the create playbook run with `cluster_state=absent`. Five test-yourself
questions close the video (answers in `exercises.md`).

**Part 1 · deploy by hand — IAM keys, the Ansible toolbox, ECR, one EC2 server and nginx**

1. **Thirty-three commits, one backslash** — the repository's history: 33 of its 39 commits say
   `/run-deploy-app`, a sentence that redeploys a server, and one `\run-deploy-app` that ran nothing; the
   lecture's three parts (motivation, automation, review); what ran for real and what is drawn; what you
   need (Docker, your own AWS account with billing, a GitHub repository for part 2); a server bills until
   you delete it; how the tracker and `▶ your turn` work.
2. **The final map, in AWS words** — the lecture's CI/CD map (dev team → GitHub → GitHub Actions → the
   cloud → users) and the app as one chain; the slides speak Google Cloud, the video follows the AWS
   repository; the term map: Kubernetes → one EC2 server with Docker containers, the image registry →
   ECR with three repositories, Pulumi → Ansible playbooks, the service-account key → an IAM access key
   and an EC2 key pair, `/deploy-app` → `/run-deploy-app`, the ingress → one nginx container; no machine
   learning lane here (that was Lecture 15); the lecture's five things to automate, and which three this
   repository does; the lecture's plan: GitHub Actions runs the deployment container, here
   `cheese-app-deployment`.
3. **A policy, a user and two keys** — clone the repository (extras: there is no clone step); the "API's
   to enable" list sits inside a comment, and the Bedrock models from 2024 to check in `us-east-1`; the
   policy JSON (one identity check, nine ECR actions, any resource; it parses; no
   `ecr:CreateRepository`), `CheeseAppECRPolicy`; the user `deployment-ac215-user` with three AWS-managed
   policies and yours; an access key for a third-party service, its CSV in a `secrets` folder beside the
   clone; the EC2 key pair's `.pem`; the badge (the AWS API) and the key (SSH); the small gap: the README
   names the key pair `cheese-app-ac215-key-pair`, the code expects `ac215_2024` in three files;
   `chmod 400`.
4. **Ansible in one picture** — Ansible next to Pulumi (Lecture 20): an ordered list of tasks against the
   machines of an inventory; playbook → plays → tasks → modules; `hosts: localhost` runs in the toolbox,
   `hosts: appserver` on the server over SSH; `inventory.yml` line by line (user `ubuntu`, line 4's key
   for GitHub Actions, line 7's key for your laptop, keys from the environment; region, `t2.large`, the
   key pair name, the machine image, the disks); the README's four bullets; change the key pair name and
   the `NEXTAUTH_SECRET` now, the host on line 30 later; the recap: `failed` and `unreachable` at zero,
   and a declarative task run twice says `ok`.
5. **Starting the toolbox: three surprises** — step 1, the deployment folder; `docker-shell.sh` reads the
   CSV's second line and hard-codes an account id (line 17); as cloned, "credentials file not found"
   (four `../` lead to `/home`); step 2's fix, three levels up; step 3's `sh docker-shell.sh` on Ubuntu:
   `Syntax error: redirection unexpected` (`sh` is dash, no here-string, and `sh` skips the shebang): use
   `bash`; the build stops at step 9 of 15 (curl can't verify Helm's download site, at the time of
   recording) and, with `set -e` commented out, the script runs an image that was never built: delete the
   Helm lines; `/secrets` is empty (line 26 has the same four `../`): fix it and line 17; the toolbox
   prompt.
6. **Inside the toolbox: whose Docker?** — the mounts: the Docker socket, the deployment folder at
   `/app`, your secrets, the three app folders, your keys as environment variables; images built inside
   land on your laptop, and a prune from inside would sweep your laptop; versions: the AWS CLI, Docker,
   kubectl and Ansible 6, not the Ansible 9 the Dockerfile asked for, because the unquoted `>` in
   `pip install ansible>=9.0.0` wrote pip's log to a file named `=9.0.0`; leave it for this lecture (the
   provision playbook relies on this old Ansible); the warnings, hidden from then on; `aws sts
   get-caller-identity` and the invalid token; the inventory graph; all five playbooks pass a syntax
   check.
7. **Three images, one timestamp** — step 4: three empty private ECR repositories, made by hand; the build
   playbook on `localhost`: the ECR login, a tag from `date` to the second, three images built from the
   mounted folders and pushed, the tag saved to `.docker-tag`; step 5's first real error, at the ECR login
   (the second line follows from the first), `failed=1`, and no image built; what success looks like (11
   tasks, `failed=0`); the last task, `docker system prune -a` without `-f`, asks and removes nothing;
   every push stores three more images in ECR.
8. **Create a server, then provision it** — step 6 from `localhost` through the AWS API: a security group
   open on 22, 80 and 443, a 50 GB disk, a `t2.large` with your key pair and two 100 GB disks of its own,
   and an attach of the 50 GB disk that wasn't tested here; the meters (instance, disks, public IP
   address); AWS rejects the credentials; the heading still says GCP; step 7, the server's address into
   the inventory; the key switch of step 9, needed before step 8; step 8 unreachable (our placeholder
   host); host key checking is off, a trade-off; on a real server, 38 tasks: Docker, the data disk at
   `/mnt/disk-1`, the AWS CLI and `aws configure` with your keys.
9. **Five containers on one network** — two extras before step 10: Chroma at the tag `latest` (version
   1.0.0 at the time of recording) answers the old API with HTTP 410, so pin `0.5.18` on line 151 as the
   compose file does; the loader's `docker run -it`, which Docker refuses without a terminal (untested
   under Ansible); step 10 unreachable, and what it does on a real server: your keys in a root-only file
   and in the API container's environment, the network `appnetwork`, two folders on the data disk, the
   ECR login, the tag (`DOCKER_TAG` in the toolbox wins, otherwise `.docker-tag`; from your laptop, the
   file), the three pulls, `frontend` on 3000, Chroma on 8000, a throwaway loader, the API on 9000, all
   three ports shut by the security group; step 11: SSH as `ubuntu` (or EC2 Instance Connect) where the
   README says GCP console, and the server commands on local stand-ins.
10. **One front door: nginx** — the lecture's routing slide on one machine: the ingress becomes an nginx
    container; step 12's `nginx.conf` is already in the repository: port 80, `/api/` to `api-service:9000`,
    everything else to `frontend:3000`; the trailing slash in `proxy_pass` strips `/api`, confirmed on
    stand-ins, and `/api` without its slash gets a redirect; the frontend calls `/api` on the same host;
    step 13 unreachable, and what it does; step 14 in the browser: only port 80 does the work, 443 is open
    but nginx serves nothing there, no HTTPS yet.

**Part 2 · let a commit press the button — CI/CD in the lecture's words, the GitHub Actions workflow, teardown and the course review**

11. **CI, CD, and who presses release** — the lecture's loop (commit, build, test: CI; deploy, monitor:
    CD; notifications back), and the review's version with a release box; continuous integration: shared
    repository, automated tests, coding standards, static analysis (Lectures 9 and 21); continuous
    delivery (a person presses release) vs continuous deployment (every passing change ships by itself);
    CI and CD for machine learning (data quality, model performance, cost, a tolerance, data drift); this
    repository on the loop: build, release, deploy, and no test, though the workflow is named "Continuous
    Integration and Continuous Deployment"; GitHub Actions runs the deployment container: thin YAML,
    thick container.
12. **Two sieves on one commit message** — `ci_cd_aws.yml` isn't in the README: a push to `main` starts
    it, the job runs only if the message contains `/run-`, and the last step only if it also contains
    `/run-deploy-app`; `update readme`, `fix typo /run-tests` (build and push only, the server keeps the
    old tag), `/run-deploy-app`, and the backslash from the opening; the lecture's tutorial slide with the
    GCP repository's keyword `/deploy-app`; `head_commit` is the last commit of a push, and the match
    ignores case.
13. **Secrets and the runner** — your own private repository, `origin` pointed at it, `main` pushed (its
    last message runs nothing); the four repository secrets the workflow names (two key halves, the
    account id, the whole `.pem`), not in the README; every copy of a key is one more place to protect;
    the runner: a fresh Ubuntu machine, AWS's action sets its credentials, an identity check, `aws s3
    ls`, the ECR login; it builds the toolbox from the committed Dockerfile (so commit the Helm fix); a
    fresh tag into `.docker-tag` and `$GITHUB_ENV` (run by hand); plain `docker build`, `tag` and `push`
    for the three images; the toolbox only deploys, with the deployment folder at `/deployment` and the
    keys at `/root/.ssh`; the SSH key step: a config and `ac215_2024.pem` with mode 600, on the runner
    only.
14. **Follow one tag to the server** — the deploy step's `docker run` (the socket, two folders, five
    variables) and its one long `&&` chain, run by hand up to the ECR login; one tag from `date` on the
    runner to an extra variable that beats anything the playbook sets, three pulls, each container
    recreated with a short gap: one machine swaps, it doesn't roll like the slides' Kubernetes (Lecture
    22); the commit: your server's address, step 9 undone, the Helm fix, the Chroma pin, and `git add .`
    commits your account id and `NEXTAUTH_SECRET`, so keep the repository private; the slide's three
    commands with this repository's keyword; a green run means every step exited 0, not that the app
    works: reload the site and check the image column; delivery, not deployment, until Milestone 5.
15. **The delete that deletes nothing** — README's last step with `cluster_state=absent`: the security
    group and volume tasks are skipped, the instance task has no `when:` and fails on `group_id` before
    any AWS call; even past that, the volume's id exists only in a create run and no task terminates the
    instance; clean up by hand: terminate the instance, delete the 50 GB volume (it outlives the
    instance), the security group and the key pair; the three ECR repositories; the access key (and the
    user and policy if made for this); the four GitHub secrets; the 2.5 GB toolbox image and your edited
    files.
16. **The course on one server, and recap** — the lecture's review (slides 21–37) on the server you
    deployed: VMs and containers (Lectures 1–2), a shared bucket (3), images once pushed by hand, now by
    the runner; execution and state; retrieval (5) in the loader and Chroma, agents (6–7); labeling and
    fine-tuning not here: ready-made models through Bedrock, plus the cheese classifier as a file;
    training and pipelines (13, 15) beside the server; the API and frontend containers (18); the CI loop
    (9, 21); routing (20, 22) as today's nginx; where next: tests in front and a deploy for every merge,
    an instance role and OIDC instead of copied keys, HTTPS; the path once more; five test-yourself
    questions.

The README's, the code's and the slides' small slips are pointed out kindly, with the fix: the README has
no clone step, and its "API's to enable" list is inside a comment (nothing to switch on in AWS; check
Bedrock model access instead); the key pair is `cheese-app-ac215-key-pair` in the README but `ac215_2024`
in the code (name yours `ac215_2024`); README:76's CSV path is right but `docker-shell.sh` has the same
four `../` in `SECRETS_DIR` (line 26) and a hard-coded account id (line 17), which the README doesn't
mention; `sh docker-shell.sh` fails on Linux (use `bash`); the toolbox's Helm lines failed to build at
the time of recording (no playbook uses Helm: delete them), and `set -e` is commented out, so a failed
build still starts a container; `ansible>=9.0.0` is a shell redirect, not a pin (leave it for this
lecture: the provision playbook needs this old Ansible); "Create … Server in GCP", "Provision … in GCP"
and "from the GCP console" mean the EC2 instance, over SSH or EC2 Instance Connect; the key switch of
step 9 is needed before step 8 (and must be undone before you push); README:137 asks you to create
`nginx.conf`, which is already in the repository; the server's Chroma at `latest` answers 410, so pin
`chromadb/chroma:0.5.18`; the loader's `docker run -it` may need its `-it` dropped; the build playbook's
last task, `docker system prune -a`, asks and removes nothing; the README's delete command deletes nothing
(clean up by hand; `exercises.md` B5 sketches a version that finds everything by name, checked offline only); the README never mentions the workflow, its
keyword or its four secrets; the workflow is named "Continuous Integration and Continuous Deployment" but
runs no test; and where the slides differ from the repository: Google Cloud words for AWS pieces, the
keyword `/deploy-app` for `/run-deploy-app`, a Kubernetes rolling update for containers swapped on one
machine, and the slide's `git add` without the dot.

## Rebuild

```bash
python -m explainer.build videos/ac215-l23-final-cicd -q l                          # fast draft
python -m explainer.build videos/ac215-l23-final-cicd --render-only --jobs 3        # 1080p60 scene renders
python -m explainer.build videos/ac215-l23-final-cicd --no-render --crf 27 --burn   # stitch: video, parts, subtitles, burned-in copy, chapters, transcript
python -m explainer.build videos/ac215-l23-final-cicd --subs-only                   # rewrite subtitles only
python -m explainer.i18n check videos/ac215-l23-final-cicd --lang zh                # Chinese text aligned with the English
```

No MP4 is in Git (the burned-in copy is a release asset): after a fresh clone, render the scenes once,
then the `--no-render` line rebuilds the clean video, the two part cuts and the burned-in copy from the
scene renders. The captures can be re-run with `bash assets/terminal/capture.sh setup pre secrets shell-a
shell-b shell-c toolbox toolbox-b playbooks ci extras` (see [`ASSETS.md`](ASSETS.md)); the exercise
checks with the scripts in [`assets/exercise-checks/logs/`](assets/exercise-checks/README.md).

Narration: Kokoro (`af_heart`, speed 0.9), generated locally.

*Course materials belong to the AC215 teaching staff (Harvard IACS); the cheese-app-aws tutorial is used
for study with the instructor's permission and quoted at its pinned commit, with the author's account id,
server address and committed secret masked. The lecture's slides are redrawn in our own pictures, never
shown. The AWS consoles, the server's screen, the browser and the GitHub pages are schematic drawings
(tagged `illustration`), never screenshots; the recording used no AWS account, no GitHub credentials and
no real keys, and every account id, key and address on screen is a placeholder.*
