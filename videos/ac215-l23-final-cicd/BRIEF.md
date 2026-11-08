# Brief · AC215 L23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys

The design of this video, written before the script. Series rules: `docs/AC215_SERIES.md`.
Facts: `digest.md` (the verified tutorial digest, rebuilt around `cheese-app-aws`), `SLIDES.md` (the
lecture deck, 38 slides, and its scene map) and `assets/` (real captures, see `ASSETS.md`). **Where
the digest or the slides and the captures disagree, the captures win.** The captures are the newest
source: 2026-11-08, 01:13–01:20 UTC, a fresh Ubuntu 24.04.5 "laptop" with Docker Engine 29.9.3, user
`student` (`laptop/00`), every README command typed exactly as written.

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**: the L23 deck slide by slide wherever the tutorial applies it
(motivation, automation, the review), and the README of `dlops-io/cheese-app-aws` step by step, in
order, followed by the repo's GitHub Actions workflow, which the README never mentions.

**Series decision (issue #125): L23 follows the AWS variant, exactly as L15 did.** The slides speak
Google Cloud (GKE, Artifact Registry, Vertex AI, a service-account key, `/deploy-app`); the video
follows `cheese-app-aws` (`main` @ `5950118`, the course site's AWS variant, "No K8s") and maps the
slides' terms onto its pieces, kindly and once per term. `cheese-app-v4` @ `033f187` is context for
slides 17–20 only: no panel quotes it and nothing is captured from it.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which commit | `5950118` (main, 2024-11-21, "cleanup") | unchanged: `git ls-remote` on 2026-11-08: `HEAD` = `refs/heads/main` = `5950118`, the only branch, no tags (`laptop/01`, `03`) |
| `sh docker-shell.sh` (README:77) | digest G2 | `laptop/23`: `docker-shell.sh: 13: Syntax error: redirection unexpected`, exit 2; `/bin/sh -> dash` (`24`). On macOS `sh` is bash and the line works. Fix: `bash docker-shell.sh` |
| the toolbox build | digest G3 (failed in the sandbox, open question) | `laptop/25`: as committed, `ERROR [ 9/15]` `curl: (60) SSL certificate problem` on `baltocdn.com/helm/signing.asc`, `gpg: no valid OpenPGP data found`, then (no `set -e`) `Unable to find image 'cheese-app-deployment:latest' locally`, exit 125. The same `curl: (60)` from the laptop itself (`26`): the site is **not** intercepted by the recording proxy. Without the two Helm lines it builds in 132.8 s (`27`, `28`). Say "at the time of recording, on our machine"; a machine that already trusts the new root may pass |
| `/secrets` in the toolbox | digest G4 (README misses `SECRETS_DIR`) | `laptop/28`: **empty**; after editing `SECRETS_DIR` and the account id (`30`), `31` shows the CSV and the `.pem` |
| Ansible version | digest G1 | `laptop/32`, `33`: ansible **6.7.0** / core **2.13.13** on Python **3.8.10**; a file named `/=9.0.0` holds pip's log |
| the six playbook commands | digest §4 (dummy keys) | all six run verbatim in the toolbox, each to its **first real error** with obviously fake placeholder keys: `40` `UnrecognizedClientException` + `Cannot perform an interactive login from a non TTY device`; `42` `AuthFailure` at "Create security group"; `44`, `46`, `47` `UNREACHABLE! … Could not resolve hostname external_ip`; `48` `'dict object' has no attribute 'group_id'`, before any AWS call |
| the inventory host | digest: the author's IP | masked: `<EXTERNAL_IP>` in the committed file (`35`); after README:97's edit the placeholder host name `EXTERNAL_IP` (`43`). Never an address |
| the key pair's name | digest G6 | `laptop/13`: README `cheese-app-ac215-key-pair`, code `ac215_2024` in `inventory.yml:4, 7, 16`, `docker-shell.sh:27`, `ci_cd_aws.yml:81-126`; the toolbox's `/secrets` holds `cheese-app-ac215-key-pair.pem` (`31`), not the `ac215_2024.pem` the inventory's default expects |
| the workflow | digest Part F (not runnable) | run by hand on the laptop up to its first error (`50`–`53`, all extras): 33 `/run-deploy-app` commits and one `\run-deploy-app` (`50`); `DOCKER_TAG=20261108011909` (`51`); the SSH files (`52`); the deploy step stops at the ECR login, neither playbook runs (`53`). No Actions run page exists for us: `illustration` only |
| Chroma on the server | digest G10 | `laptop/60`: `chromadb/chroma:latest` = `"1.0.0"`, `/api/v1/heartbeat` → **HTTP 410**; `61`: `0.5.18` → 200 |
| nginx routing | digest C7 | `laptop/62`, live on the laptop with two stand-ins: `/api/newsletters` → `api-service received /newsletters`; `/` → `frontend received /`; `/api` → `HTTP 301` |
| README:120–132 (server commands) | digest step 18 | no server: run on the laptop as stand-ins (`63`–`65`), always tagged `extra · stand-in on the laptop`, never presented as the server's output |
| app images (`ci_cd_aws.yml:52-70`) | digest: not built | not built (the README's route never builds them, `40`; disk). Code panels only |
| README output | — | the README documents **no output at all**: no `expected/` folder, nothing `recorded`. Where the cloud's answer would come, the scene describes what to look for, without an output panel |

## Audience and goal

An AC215 student who has done L1–L22, in particular:
- Docker images, `docker-shell.sh` scripts with bind mounts, pipenv inside images (L02–L04);
- the cheese app's services: the Next.js frontend, the FastAPI `api-service`, Chroma and the
  vector-db loader (L05, L18);
- L15 on AWS (IAM users and access keys, ECR, the AWS CLI), L20 (a deployment container driving
  Pulumi), L21 (GitHub Actions: workflows, jobs, steps, runners, repository secrets), L22
  (Kubernetes, ingress) — the last two as the GCP path this variant does not take.

New to them: **Ansible** (inventory, playbooks, plays, tasks, modules), EC2 instances, security
groups, key pairs, and a workflow that **deploys**. They watch with their clone of
[dlops-io/cheese-app-aws](https://github.com/dlops-io/cheese-app-aws) open, Docker running, their own
AWS account with billing (GOLD tags; this lecture runs a server around the clock until they delete
it) and a GitHub repository of their own for part 2, pausing to run each step.

After the video they can:
- create the IAM policy, user, access key and EC2 key pair the README asks for, keep both secrets
  outside the clone, and name the key pair so the code finds it;
- start the deployment toolbox (`bash docker-shell.sh`), with the three edits the script needs, and
  explain why `sh` fails on Linux, why the build may stop at the Helm key, and what
  `ansible>=9.0.0` really did;
- read `inventory.yml` and a playbook as inventory → play → task → module, and tell a `localhost`
  play (talks to AWS's API or to the laptop's Docker) from an `appserver` play (SSH to the server);
- explain the Docker socket mount: the toolbox's `docker build` fills the **laptop's** Docker;
- run the six playbooks in README order and read each one's first error honestly; know what
  success looks like (`failed=0` in the PLAY RECAP);
- follow one timestamp tag from `date` to ECR to a recreated container on the server;
- draw the server: a security group with three open ports, five containers on `appnetwork`, nginx
  as the only front door, `/api/` stripped before the API sees it;
- read `ci_cd_aws.yml`: which commit messages build, push or deploy; which four repository secrets
  it needs; what the runner does that the laptop did;
- say in the lecture's words what this workflow is (the CD half, with a person pressing release)
  and what Milestone 5 would add (tests in front, deploy on merge);
- tear everything down by hand, because the README's delete command deletes nothing;
- place every earlier lecture on the server they just deployed (the review, slides 21–37).

## Length and parts

~31 minutes. Narration 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm). The plan below
totals **~4,200 words ≈ 24 min of narration**; typing, real outputs, the console and GitHub drawings
and five ponder timers bring it to ~30–32 min. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S10** (~2,510 words, ~18–19 min): **deploy by hand with Ansible** — the README top
  to bottom. Hook; the lecture's map in AWS words; identity in the console; Ansible's inventory; the
  toolbox; inside the toolbox; build and push; create and provision the server; the containers; the
  front door and the browser.
- **Part 2 = S11–S16** (~1,690 words, ~12–13 min): **let a commit press the button, tear down,
  review** — the lecture's CI/CD (slides 7–18), the workflow's trigger, its secrets and runner, one
  tag followed to the server, teardown, and the course review (slides 21–37) placed on the server.

The cut is the README's own seam: "Once the command runs go to `http://<External IP>/`" (README:143)
is the moment the app is live by hand. Part 1 ends on the (illustrated) browser and the question that
part 2 answers: "next time, a commit message does all of this. How?"

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop: your terminal, your clone, `~/secrets/` (the CSV, the `.pem`), the browser | GREY |
| the cloud: AWS `us-east-1`, the EC2 instance, its EBS disks, ECR, the IAM console; GitHub and its runner (a remote machine) | BLUE |
| containers and images: the toolbox `cheese-app-deployment`, the three app images, the five containers on the server, the throwaway loader | TEAL |
| shared, not yours: the course's repo and its committed values (the author's account id, IP and secret, all masked), Docker Hub's `nginx:stable` and `chromadb/chroma:latest`, `0.0.0.0/0`, the AWS-managed policies | ORANGE |
| project-owned, pinned: `inventory.yml`, the five playbooks, `nginx.conf`, the timestamp tag and `.docker-tag`, the pins that work (`chromadb/chroma:0.5.18`), `failed=0`, a ✓ | GREEN |
| tools: Ansible, the AWS CLI, Docker, GitHub Actions (the runner program), `aws-actions/configure-aws-credentials` | PURPLE |
| errors and "don't": every first error, `failed=1`, `UNREACHABLE!`, exit codes ≠ 0, the HTTP 410, the delete that fails, a key in the repo | RED |
| your turn, the README tracker, the CI/CD loop's current box, the ponder timer | YELLOW |
| money: the running instance, its disks and public IPv4, ECR storage, Bedrock tokens, Actions minutes on private repos | GOLD |
| lookups and routes: SSH arrows, the Docker socket line, HTTP routes through nginx, `lookup('env', …)`, the commit-message string flowing through the sieves, the tag's trail | PINK |
| the lecture's GCP words before they turn into AWS words; the future (MS5, instance role, OIDC); *skipped* tasks | GREY, dashed |

Keys are drawn as two distinct WHITE glyphs: a **badge** for the access key (talks to AWS's API) and
a **key** for the key pair (opens SSH); the place that holds them carries the colour. No AWS, GitHub,
Docker or Ansible logos anywhere: AWS is a BLUE box labelled "AWS · us-east-1", GitHub a BLUE box
labelled "GitHub".

## Running example

- **The laptop**: user `student`, terminal title `laptop`, prompt
  `student@laptop:~/cheese-app-aws/src/deployment$` (`laptop/20`); `~/cheese-app-aws` and
  `~/secrets` side by side (`12`, README:55-60). Say once: "your prompt shows your own user".
- **The toolbox**: prompt `root@<container id>:/app#` as captured; the id changes on every run (say
  it once, never read it). Toolbox files start with a (mostly cached) build log: crop to the prompt.
- **The secrets**: `~/secrets/deployment-ac215-user_accessKeys.csv` holds AWS's CSV header and
  obviously fake placeholder values; on screen and in narration only `<aws-access-key-id>` /
  `<aws-secret-access-key>`. The `.pem` is a throwaway key made for no account; its text is never
  shown. The account id is always `YOUR_ACCOUNT_ID`; the server's address `<EXTERNAL_IP>` (or the
  placeholder host `EXTERNAL_IP` once it is in the inventory, `43`).
- **How the cloud steps are shown, said once in S01 and not apologised for again**: "This recording
  machine has no AWS account. Everything on your laptop ran live, and every command that talks to
  AWS ran exactly as the README writes it, up to its real first error. The console, the server's
  screen and GitHub's pages are drawings, marked *illustration*."
- **Versions, all "at the time of recording"**: laptop Docker 29.9.3; toolbox aws-cli 2.39.6,
  ansible 6.7.0 / core 2.13.13, Python 3.8.10, Docker CLI 28.1.1, kubectl v1.28.15, no helm (`32`);
  `nginx:stable` = nginx 1.30.6 (`65`); `chromadb/chroma:latest` = 1.0.0 (`60`).
- **Crops**: the `CryptographyDeprecationWarning` lines (every Ansible command) and the
  `community.general` warnings (shown and explained once, in S06/S07, then cropped); build logs show
  first lines, `…`, the last lines; `AWS_CA_BUNDLE` (capture-only) is cropped from `31`'s variable
  list; `53`'s first line (the placeholder `export`) is cropped, the panel starts at `docker run`;
  timestamps, request ids, digests and container ids are never read aloud.

## Visual set pieces (the 3Blue1Brown part)

Class names go in `scenes/common.py`; none collides with a scene class in `video.yaml`.

- **V1 · `KeywordSieves` — two sieves on one sentence (S01, S12).** A commit message is a PINK
  ribbon of text. A push to `main` drops it onto two stacked sieves, both reading
  `github.event.head_commit.message`: the job sieve (`contains(…, '/run-')`, `ci_cd_aws.yml:9`)
  and, over the last step only, the deploy sieve (`contains(…, '/run-deploy-app')`, `:100`). Four
  ribbons fall in turn: `update readme` (caught by nothing: no job), `fix typo /run-tests` (through
  the first, stopped at the second: the job runs, three new images reach ECR with a GOLD storage
  tick, the server stays on the old tag), `/run-deploy-app` (through both: the server's containers
  are recreated), and the history's `\run-deploy-app` (`laptop/50`: a backslash, so `/run-` is not
  in it; it bounces off the first sieve, RED). A small note: `head_commit` = the last commit of the
  push; the match ignores case. S01 shows only the 33-vs-1 count and the bounce, as the question.
- **V2 · `TermMap` — slide 19's map, then the same map in AWS words (S02).** Re-draw slide 19 in
  series style: Dev Team → (PINK commits) → GitHub (Code, Branches, Actions) → GitHub Actions
  (Build → Deploy) → a cloud box (Storage, Vertex AI, Kubernetes) → Users; above, the app chain
  Data Collector → Data Processor → Model Training → Model Deploy → Backend API → Frontend. Then
  the GREY dashed GCP labels **transform** into BLUE AWS labels one by one: Kubernetes → "one EC2
  server · Docker containers"; Artifact Registry → "ECR · 3 repositories"; Pulumi (L20) → "Ansible
  playbooks"; service-account key → "IAM access key + EC2 key pair"; `/deploy-app` → `/run-deploy-app`;
  ingress → `nginx` container. The four ML boxes and Vertex AI fade to GREY dashed with the label
  "not in this repo · the AWS ML pipeline was L15". Last beat: slide 6's five cards become a
  scorecard for this repo: data pipeline jobs ✗ (L15), model training & deployment ✗ (L15),
  frontend deployment ✓, backend deployment ✓ (one bracket: "always together, one keyword"),
  building & pushing containers ✓ ("three app images").
- **V3 · `KeyJourney` — two secrets and every place they end up (S03, S06, S08, S13, S16).** The
  access-key badge starts in GREY `~/secrets/` as a CSV row, and travels with PINK arrows:
  `docker-shell.sh:13-15` (shell variables) → the TEAL toolbox's environment (`:43-46`) →
  `lookup('env', …)` into Ansible (`inventory.yml:9-11`) → the BLUE server twice (`aws configure`,
  `deploy-provision-instance.yml:288-292`; `/srv/secrets/aws-credentials`, mode 0600,
  `deploy-setup-containers.yml:36-44`) → the env of the `api-service` and the loader (`:165-168`,
  `:184-186`) → in S13 a BLUE GitHub vault of four repository secrets (`ci_cd_aws.yml:21-22`, `:33`,
  `:81`, `:102-108`). Each new copy leaves a small badge glyph behind; by S13 there are seven. The
  key pair's key travels a shorter path: `~/secrets/` → `/secrets` in the toolbox → SSH into the
  server as `ubuntu`; in CI, `AWS_SSH_KEY` → `~/.ssh/ac215_2024.pem` on the runner → `/root/.ssh` in
  the toolbox. In S16 two GREY dashed "next step" overlays remove most badges: an instance role
  (the server gets short-lived credentials, no key file) and GitHub OIDC (no stored AWS keys).
- **V4 · `AnsibleMachine` — inventory → play → task → module (S04, S07, S08, S09).** The inventory
  is a GREEN tree: `all` (a variables card) → `appserver` → one host leaf `<EXTERNAL_IP>` (the real
  graph, `laptop/35`). A playbook is a stack of play cards; each play card says `hosts:` and holds
  task tiles; each tile names one module (`ec2_group`, `ec2_vol`, `ec2_instance`, `apt`, `mount`,
  `docker_image`, `docker_container`, `shell`). The `hosts:` line decides where the tiles fire:
  `localhost` → PURPLE sparks inside the TEAL toolbox that leave as PINK API calls to the BLUE AWS
  box (create-instance) or down the socket to the laptop's Docker (docker-images); `appserver` →
  sparks ride a PINK SSH arrow into the BLUE server (`ansible_user: ubuntu`, the `.pem`). A
  declarative tile (`state: present`) turns GREEN "ok" on a second run instead of acting again; a
  `shell:` tile always acts. A `when:` tile greys out, dashed, when its condition is false (S15).
  The PLAY RECAP is a row of counters `ok · changed · unreachable · failed · skipped`; success is
  `failed=0` and `unreachable=0`.
- **V5 · `SiblingContainers` — one crate, the laptop's Docker (S05, S06, S13).** The GREY laptop
  holds a Docker engine (an image shelf). `docker-shell.sh:35-48` runs the TEAL toolbox; six PINK
  mount lines connect it to the laptop: the socket `/var/run/docker.sock`, `src/deployment` → `/app`,
  `secrets` → `/secrets`, the three app folders → `/api-service`, `/frontend-react`, `/vector-db`.
  A `docker build` typed inside the toolbox travels **down the socket**: the new image lands on the
  laptop's shelf beside the toolbox, a sibling, not inside it. `docker system prune -a` from inside
  would sweep the laptop's shelf (`deploy-docker-images.yml:59-60`; `laptop/67`: it asks and, with
  no answer, does nothing). In S13 the same crate sits on a BLUE runner: the mounts change
  (`/deployment`, `/root/.ssh`; no app folders, the runner built the images itself with plain
  `docker build`), the socket stays.
- **V6 · `TimestampTrail` — one tag from `date` to a running container (S07, S14).** A GREEN tag
  card `YYYYmmddHHMMSS` is stamped by `date` (`deploy-docker-images.yml:12`; in CI
  `ci_cd_aws.yml:46-50`, the real `DOCKER_TAG=20261108011909` from `laptop/51`). It clips onto three
  TEAL images (`…/cheese-app-frontend-react:<tag>`, `-api-service`, `-vector-db-cli`), which fly to
  three BLUE ECR shelves (registry `YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com`). A copy of the
  card drops into `.docker-tag` (the committed one reads `20241121211313`, the author's last
  deploy). In S14 the trail continues: the card rides `DOCKER_TAG` into the toolbox and
  `--extra-vars … docker_tag=` into Ansible, which pulls the three images at that tag on the server
  (`deploy-setup-containers.yml:101-129`) and **recreates** each container (`recreate: yes`): the old
  container blinks out, the new one blinks in, a short gap in between. A GREY dashed inset shows
  L22's rolling update for contrast (new pods up before old ones go): "this repo has one machine,
  so it swaps, it doesn't roll."
- **V7 · `VmLayout` — one server, five containers, one front door (S08, S09, S10, S16).** A BLUE
  EC2 box with a security-group wall: three doors open to `0.0.0.0/0` (ORANGE), 22, 80, 443
  (`deploy-create-instance.yml:12-21`); a GOLD meter beside it (instance, disks, public IPv4). S08
  builds the inside: Docker engine, the disk at `/mnt/disk-1`. S09 fills it: a PINK `appnetwork`
  line, TEAL containers `frontend :3000`, `vector-db :8000` (ORANGE `latest` chip), `api-service
  :9000`; the loader appears, fills the vector DB and vanishes (`--rm`). The 3000/8000/9000 doors are
  painted on the inside but the wall has no hole for them. The Chroma drift: the `latest` chip flips
  to `1.0.0`, the loader's PINK request `/api/v1/heartbeat` comes back RED `410`; swapping the chip
  for GREEN `0.5.18` turns it `200` (`laptop/60`, `61`). S10 adds `nginx` at doors 80/443: a browser
  request `/api/newsletters` enters, nginx **cuts the `/api` prefix off** (the trailing `/` in
  `proxy_pass http://api-service:9000/;`) and passes `/newsletters` on; `/` goes to `frontend:3000`
  (`laptop/62`). Door 443 is open but nothing listens: "no HTTPS". S16 reuses it as the review board.
- **V8 · `ReleaseLoop` — the lecture's loop and the release button (S11, S14, S16).** Slide 7's
  loop re-drawn: Developers → (PINK commits) → Codebase → Build → Test → Deploy → Monitor, with
  dashed PINK notification lines back to a Developers bar; the CI half and the CD half bracketed.
  Slide 36's Release box slides in between Test and Deploy. This repo's version lights only
  Codebase → Build → Release (= the tagged images land in ECR) → Deploy; **Test** stays a GREY dashed
  outline labelled "L21" (`ci_cd_aws.yml` runs no test, though its `name:` says Continuous
  Integration); **Monitor** is the run's colour plus your own check of the site. Then slide 12's
  toggle: one conveyor ends at a RED RELEASE button with a person's hand (delivery) or at an
  "auto" ring (deployment). In S14, the hand on the button is typing `/run-deploy-app`. In S16 the
  loop's MS5 version: Test lit (from L21), the keyword gone, deploy on every merge to `main`.

## README step tracker (ReadmeTracker, top-left)

Three trackers, titled with the README's own headings; the third is the workflow file, which the
README never mentions, so every step on it is `extra`. Step titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **A · Before you deploy** ("API's to enable", "Setup AWS Keys", "Create AWS EC2 Key Pair", "Deployment Setup") | 7–72 | APIs to enable · ECR policy · IAM user · Access key · Key pair · Deployment setup (6) |
| **B · Deployment Steps** (through "Delete the Compute Instance") | 74–148 | Go to folder · Edit CSV path · docker-shell.sh · ECR repositories · Build and push · Create instance · Copy the IP · Provision · Key line · Setup containers · Server checks · Nginx config · Setup webserver · Open the site · Delete instance (15) |
| **C · ci_cd_aws.yml** (not in the README: every step `extra`) | workflow 1–131 | Trigger · Repo secrets · AWS login · Build and push · SSH key · Deploy step · Commit, push (7) |

- A1 = README 7–13; A2 = 19–46; A3 = 48–50; A4 = 52–60; A5 = 62–64; A6 = 67–72.
- B1 = 75; B2 = 76; B3 = 77; B4 = 79–85; B5 = 87–90; B6 = 92–95; B7 = 97; B8 = 99–103; B9 = 105–111;
  B10 = 115–117; B11 = 120–132; B12 = 136–137; B13 = 139–142; B14 = 143; B15 = 145–148.
- C1 = workflow 3–9 (+ 99–100); C2 = the four `secrets.*` names; C3 = 18–33; C4 = 41–70; C5 = 72–97;
  C6 = 99–131; C7 = slide 20's three commands with this repo's keyword.
- Extras on A/B (captured, marked `extra`): `laptop/01`–`04` (pin, clone — the README has no clone
  command —, log without authors, listing), `10`, `13`, `14`, `21`, `24`–`30`, `32`–`38`, `41`, `49`,
  `60`–`68`.
- S01, S02, S11 and S16 have no tracker.

## Scene plan

Notation:
- `laptop/NN` = `assets/terminal/laptop/NN-*.txt`. Line 1 of a capture is the `$` command; in
  toolbox files the command is the line typed at the `root@…:/app#` prompt. `[exit N]` is never
  printed as text.
- ▶ = a README step the viewer must do; a YELLOW `▶ your turn` tag at real checkpoints only.
- CODE(path: a-b) quotes `assets/source/` with real line numbers (masked lines as in ASSETS.md),
  ≤ 12 lines on screen at once.
- `lecture_ref(23, "a–b")`, GREY, top right, **only while that slide's picture or idea is on
  screen**. Slide numbers are the PDF pages of `SLIDES.md`, never the footers.
- Every cloud step: the README command typed verbatim, its real first error, then a short "what
  success looks like" said over the playbook's task list, never as an output panel.

### Part 1 · Deploy by hand with Ansible

**S01 · Thirty-three commits, one backslash (~220 words) — `s01_hook.py` · `Hook`.** Cold open, no
tracker.
- The broken thing, real: `laptop/50` (the repo's commit subjects counted): `33 /run-deploy-app`
  … `1 \run-deploy-app`. "Thirty-three times, someone redeployed a server by writing the same
  sentence. Once, the slash leaned the other way, and nothing happened at all." V1's teaser: the
  33 ribbons pass a sieve, the backslash one bounces RED. On screen, the question that stays:
  *"How does a sentence deploy a server, and why did one character stop it?"*
- `lecture_ref(23, "1–4")`: the last lecture, "Final Deployment and Review": motivation, automation,
  review. Slide 4's idea in one sentence (never the page, never its names): even a toy prediction
  app is only useful if it is running somewhere and kept current.
- The AWS decision, said kindly once: the lecture's slides speak Google Cloud; the course also has an
  AWS version of this tutorial, `cheese-app-aws`, and that is the one we follow, as in L15. Same
  ideas, other cloud; S02 maps the words.
- The honesty sentence (Running example) and how to follow along: Docker, an AWS account with
  billing (GOLD: "this lecture runs a server until you delete it"), a GitHub repo for part 2; the
  tracker, code panels with path and lines, `▶ your turn`; the study guide has every command.

**S02 · The final map, in AWS words (~280) — `s02_map.py` · `LectureMap`.** No tracker (lecture).
- `lecture_ref(23, "19")`: V2's map, drawn as the lecture draws it; one sentence each for the
  bottom flow (dev team, GitHub, Actions, cloud, users) and the chain on top.
- V2's transform into AWS words, one label at a time (the C8 table of the digest). Two differences
  said out loud: no Kubernetes and no Pulumi (one server, Ansible); no ML lane in this repo (L15
  was the AWS pipeline).
- `lecture_ref(23, "5–6")`: the five things the lecture wants automated, scored for this repo (V2's
  last beat).
- `lecture_ref(23, "17–18")`: "we already have a deployment container": here `cheese-app-deployment`
  from `src/deployment/`, which **you** drive in part 1 and GitHub's runner drives in part 2. The
  lecture's "invoke the CLI in the deployment container" is, here, `ansible-playbook` commands typed
  in it (part 1) or passed to it in a `bash -c` string (part 2).
- The plan in one sentence per part.

**S03 · A policy, a user and two keys (~260) — `s03_console.py` · `ConsoleSetup`.** Tracker A1–A5.
- Extra first (not in the README): `laptop/01` (the pin, 7 characters on screen), `02` (`git clone
  https://github.com/dlops-io/cheese-app-aws.git`), `04` (the top level; `src/` with five services).
- A1: README 7–13 renders an empty list (it sits in an HTML comment). One sentence: AWS has no
  per-API switch like Google Cloud; the API service calls Bedrock models in `us-east-1`, so check
  that your account has access to them (the README doesn't say; digest open question).
- A2 ▶: CODE(README.md: 22-44) in two halves: `sts:GetCallerIdentity` + nine `ecr:` actions,
  `"Resource": "*"`; the IAM console drawing (`illustration`) → name `CheeseAppECRPolicy` (46).
  Extra `laptop/10`: the JSON parses. Note for later: it has no `ecr:CreateRepository`, which is why
  you create the three repositories by hand in S07.
- A3 ▶: user `deployment-ac215-user` + three AWS-managed policies (ORANGE chips: `AmazonS3FullAccess`,
  `AmazonEC2FullAccess`, `AmazonBedrockFullAccess`) + the custom one (48–50), `illustration`.
- A4 ▶: access key, "Third Party Service", download the CSV (52); `illustration` with
  `<aws-access-key-id>` only. V3 begins: the badge. README 54–60's tree and the real `laptop/12`:
  `~/cheese-app-aws` and `~/secrets` side by side, "outside the clone, so it can never be committed".
- A5 ▶: key pair (64), `illustration`; on the recording laptop a throwaway key stands in (`12`). V3's
  second glyph, the key: "the badge talks to AWS's API; the key opens the server's SSH door". Extra
  `laptop/13`: three names for one key pair → fix: call it `ac215_2024`, or change
  `inventory.yml:16` and the key paths. Extra `14`: `chmod 400` (SSH refuses a key others can read).

**S04 · Ansible in one picture (~220) — `s04_inventory.py` · `AnsibleInOnePicture`.** Tracker A6.
- New tool, one line: Pulumi (L20) described the infrastructure you want; Ansible runs an ordered
  list of tasks against machines listed in an inventory, and most tasks describe a state rather than
  a command.
- V4 with the real file: CODE(src/deployment/inventory.yml: 1-11) — `ansible_user: ubuntu`, the two
  key lines (4 active for GitHub Actions, 7 for a laptop: "remember these, S09"), the env lookups
  (9-11, nothing to type: they read the toolbox's environment); CODE(13-30) — region, `t2.large`,
  `aws_keypair_name: "ac215_2024"  ## Change this`, the AMI (per region), the names, the masked
  secret (24) and host (30).
- README 69–72's four bullets as YELLOW checks on those lines; what you change now: the key pair
  name (16), your own `nextauth_secret` (`openssl rand -base64 32`, said, not typed), and later the
  host (30).
- V4's play/task/module picture with one real play heading (`deploy-create-instance.yml`'s
  "Create App Application Machine", `hosts: localhost`) and one `appserver` play; the PLAY RECAP
  counters. `ansible.cfg:2` `host_key_checking = False` in one clause: convenient, a trade-off.

**S05 · Starting the toolbox: three surprises (~320) — `s05_toolbox.py` · `StartToolbox`.** Tracker
B1–B3.
- B1 ▶ `cd src/deployment` (`laptop/20`: the real `pwd` and listing).
- CODE(src/deployment/docker-shell.sh: 9-21, account id masked): reads line 2 of the CSV into two
  variables with `<<<` (13), region, the **hard-coded account id** (17). Extra `21`: as cloned,
  `Error: AWS credentials file not found at ../../../../secrets/…` (four `../`).
- B2 ▶ README 76's edit (`22`: the line after it, the CSV found).
- B3 ▶ `sh docker-shell.sh` exactly as written → `23` RED: `13: Syntax error: redirection unexpected`.
  Extra `24`: `/bin/sh -> dash`; the script's first line says `#!/bin/bash`, which `sh file`
  ignores. Kindly: on a Mac `sh` is bash and the README line works; on Linux type `bash
  docker-shell.sh`.
- Surprise 2 (extra `25`, Dockerfile as committed): the build's first lines, `…`, `ERROR [ 9/15]`,
  `curl: (60) SSL certificate problem: unable to get local issuer certificate`, `gpg: no valid
  OpenPGP data found.`; then, because `#set -e` (4) is commented out, the script still runs `docker
  run` → `Unable to find image 'cheese-app-deployment:latest' locally`. Said carefully: the Helm
  repository's certificate chains to a root our machine's store didn't have at the time of
  recording; yours may; no playbook here uses Helm, so the fix is to delete the two Helm lines and
  the word `helm` (CODE(Dockerfile: 31-37) with lines 33-34 struck; extra `27`'s diff). Then
  `28`: "Building 132.8s (20/20) FINISHED".
- Surprise 3 (extra `28` → `30` → B3 ▶ `31`): inside, `ls -la /secrets` is **empty**: line 26's
  `SECRETS_DIR` has the same four `../`, and the README doesn't mention it; Docker quietly created an
  empty folder. Edit 26, and put your own account id on 17 (`30`; how to read yours: `aws sts
  get-caller-identity` shows it, said not run). Re-run → `31`: the CSV and the `.pem` are there, and
  four `AWS_` variable names (no values; `AWS_CA_BUNDLE` cropped). `▶ your turn`.

**S06 · Inside the toolbox: whose Docker? (~230) — `s06_inside.py` · `InsideToolbox`.** Tracker B3
(extras).
- V5 with CODE(docker-shell.sh: 35-48): the six mounts and the four `-e` lines (V3: the badge enters
  the crate as environment variables).
- PONDER 1 (8 s), then the answer with V5's socket beat.
- Extra checks, each one line on screen and one sentence: `32` versions; `33`: `ls /` shows a file
  called `=9.0.0` next to `app` and `secrets` — `pip install ansible>=9.0.0` unquoted is a shell
  redirect: pip's output went to that file and pip installed **ansible 6.7.0** (core 2.13.13) on
  Python 3.8.10. Fix: quote it; and since ansible 9 needs a newer Python than Ubuntu 20.04's, the
  honest fix is a newer base image. The two warnings every command prints (`Collection
  community.general does not support Ansible version 2.13.13`, cryptography's Python 3.8 notice):
  explained once here, cropped afterwards.
- `34`: `aws sts get-caller-identity` → `InvalidClientTokenId … The security token included in the
  request is invalid.` "Ours is a placeholder; with your key this prints your account id and your
  user." `35`: `ansible-inventory -i inventory.yml --graph` = V4's tree, real. `36`: all five
  playbooks pass `--syntax-check`.

**S07 · Three images, one timestamp (~250) — `s07_images.py` · `BuildAndPush`.** Tracker B4–B5.
- B4 ▶ the three ECR repositories (README 81–85) in a console drawing (`illustration`), private,
  `us-east-1`; why by hand: the policy from S03 can push but not create.
- V6's first half over CODE(deploy-docker-images.yml: 1-12) and CODE(18-30): `hosts: localhost`,
  the ECR login (`shell:`), the `date` tag, `community.general.docker_image` build with `path:
  /frontend-react` ("the folder S06 mounted") and push. The other two images and `Save docker tag`
  (58) as tiles from `37`'s task list (11 tasks).
- B5 ▶ `ansible-playbook deploy-docker-images.yml -i inventory.yml` → `40`: the deprecation warning
  (once), `TASK [Login to AWS ECR]` `fatal`, the two stderr lines (`UnrecognizedClientException …
  invalid`, `Cannot perform an interactive login from a non TTY device`: "docker login was handed
  an empty password"), PLAY RECAP `failed=1`. Extra `41`: no image was built.
- What success looks like (no panel): eleven tasks, each image built on **your laptop's** Docker and
  pushed, `.docker-tag` rewritten with your tag (the committed `20241121211313` is the author's
  last), `failed=0`. The last task, `docker system prune -a` (extra `67`): without `-f` it asks and,
  with no answer, removes nothing; if it ever ran, it would prune the laptop (the ponder's answer).
  GOLD: ECR stores every tag you push.

**S08 · Create a server, then provision it (~240) — `s08_server.py` · `CreateAndProvision`.**
Tracker B6–B8.
- V4 + V7: the create-instance play's tiles, from `37`: security group (22/80/443 from
  `0.0.0.0/0`), a 50 GB EBS volume, an EC2 `t2.large` from the AMI with your key pair, wait for
  `running`, wait for SSH, attach the volume, `add_host`. GOLD tags appear: instance (by the hour,
  until terminated), disks, public IPv4.
- B6 ▶ README 94's command → `42`: `Gathering Facts` ok, `Create security group` → `AuthFailure …
  AWS was not able to validate the provided access credentials`, `failed=1`. Kindly: the heading
  says "in GCP"; it is an EC2 instance (carried over from the Google Cloud README).
- B7 ▶ README 97: read the instance's public IPv4 in the EC2 console (`illustration`, value
  `<EXTERNAL_IP>`) and put it under `appserver: hosts:` → `43` (the placeholder host).
- B8 ▶ README 102 → `44`: `UNREACHABLE! … Could not resolve hostname external_ip`: "there is no
  server behind our placeholder; on yours, Ansible logs in as ubuntu with your key". What success
  does: 38 tasks (`37`): Docker CE, format and mount the data disk at `/mnt/disk-1`, AWS CLI v2,
  and `aws configure` with your keys: V3's badge lands on the server (first copy there).

**S09 · Five containers on one network (~290) — `s09_containers.py` · `SetupContainers`.** Tracker
B9–B11.
- B9 ▶ README 107–111: the key-line toggle → `45` (line 4 commented, line 7 active). The default path
  is `/secrets/ac215_2024.pem`, so the file in `~/secrets` must have that name (S03's fix), or set
  `AWS_SSH_KEY`. Before pushing in part 2 you switch it back.
- B10 ▶ README 116 → `46`: the same `UNREACHABLE!`. What success does, as V7's fill: the
  credentials file (V3: second copy on the server), `appnetwork`, two folders on the disk, an ECR
  login on the server, **pick the tag** (CODE(deploy-setup-containers.yml: 101-114): `DOCKER_TAG`
  from the environment if set, else `.docker-tag`), pull three images, start `frontend`, `vector-db`,
  run the loader once, start `api-service`.
- Two things to watch for, real on the laptop, extras:
  - CODE(147-152) `chromadb/chroma:latest`; `60`: today's `latest` is `1.0.0` and answers the old
    API with **HTTP 410**; `61`: `0.5.18`, the version both clients and the repo's own
    `docker-compose.yml:25` pin, answers 200. Fix: pin the server image to `0.5.18`.
  - CODE(164-166) the loader runs `docker run --rm -it`; `66`: Docker refuses `-t` without a
    terminal. Whether Ansible's SSH session gives it one was not tested: if that task fails, drop
    `-it`.
- B11 ▶ README 120–132, the six commands verbatim. Kindly: "from the GCP console" means, on AWS,
  `ssh -i <your key>.pem ubuntu@<EXTERNAL_IP>` or EC2 Instance Connect. Their outputs are shown
  from the laptop as stand-ins (`63`, `64`, `65`, tag `extra · stand-in on the laptop`): what the
  columns mean (the IMAGE column carries the tag), and that the `nginx` lines only work after the
  next step.

**S10 · One front door: nginx (~200) — `s10_webserver.py` · `FrontDoor`.** Tracker B12–B14.
- `lecture_ref(23, "37")`: the review's routing picture (one URL, `/` to the frontend, `/api/` to
  the API) re-drawn, then the ingress box turns into an `nginx` container on V7's server: same
  shape, one machine. The slide's `/api/` is exactly this repo's path.
- B12: CODE(nginx-conf/nginx/nginx.conf: 25-27, 34-37, 46-48): `listen 80`, `location ^~ /api/` →
  `proxy_pass http://api-service:9000/;`, `location /` → `frontend:3000`. README 137 says "create";
  the file is already there.
- PONDER 2 (8 s), then extra `62`: the real answers from the laptop's stand-ins; `/api` without the
  slash → 301. Why it matters: `.env.production:2` sets `NEXT_PUBLIC_BASE_API_URL=/api`, so the
  browser calls the same host and nginx forwards.
- B13 ▶ README 141 → `47`: `UNREACHABLE!`. B14 ▶ `http://<External IP>/` in a schematic browser
  (`illustration`). V7: only 80 is used; 443 is open in the wall but no server block listens on it
  (no HTTPS); 3000/8000/9000 are closed by the security group.
- Part 1 outro: about a dozen commands and five playbooks, by hand. "Next: a commit message does
  the redeploy. That's the lecture's real subject."

### Part 2 · Let a commit press the button

**S11 · CI, CD, and who presses release (~330) — `s11_cicd.py` · `WhoPressesRelease`.** No tracker
(lecture).
- `lecture_ref(23, "7")`: V8's loop drawn: commits, the CI half, the CD half, notifications back to
  the developers from every box. `lecture_ref(23, "36")`: the review version adds Release.
- `lecture_ref(23, "8–10")`: CI by what it runs: automated tests, coding standards (style and
  consistency), static analysis (likely defects and vulnerabilities, without running the code),
  many developers, one shared repository, a working codebase out. "You built exactly this in L09
  and L21."
- `lecture_ref(23, "11–12")`: delivery vs deployment as V8's toggle: a person presses release, or
  every passing change goes out by itself.
- `lecture_ref(23, "13–15")`, ~40 words: for ML, CI also checks data quality and model performance,
  which makes it expensive; CD releases a model only within tolerance and watches for drift. "This
  repo deploys an app, not a model; L15 was the model."
- This repo on V8: Build, Release, Deploy lit; Test dashed GREY "L21"; the workflow's `name:` says
  "Continuous Integration and Continuous Deployment" (CODE(.github/workflows/ci_cd_aws.yml: 1-2)),
  kindly: "it is the CD half".
- `lecture_ref(23, "16–18")`: many CI/CD services (one sentence, no logos); GitHub Actions builds the
  deployment container and runs it. Thin YAML, thick container: the deploy logic is the playbooks
  you just ran.

**S12 · Two sieves on one commit message (~250) — `s12_trigger.py` · `TwoSieves`.** Tracker C1.
- CODE(ci_cd_aws.yml: 3-9) and CODE(99-100): `on: push: branches: [ "main" ]`, the job's `if:`,
  the last step's `if:`. V1 in full with the four ribbons; the S01 question answered: the
  backslash.
- PONDER 3 (8 s), answered with V1's second ribbon.
- `lecture_ref(23, "20")`: the lecture's tutorial slide: a workflow file in `.github/workflows`,
  and a keyword in the commit message. Its keyword is `/deploy-app` (the Google Cloud repo's); here
  it is `/run-deploy-app`. Its three commands, written out: `git add .`, `git commit -m "your
  message /run-deploy-app"`, `git push` (shown, typed in S14).
- Two precise details: `head_commit` is the **last** commit of a push; the match ignores case.

**S13 · Secrets and the runner (~270) — `s13_runner.py` · `RunnerSecrets`.** Tracker C2–C5.
- C2 ▶: four repository secrets (Settings → Secrets and variables → Actions, `illustration`):
  `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, `AWS_ACCOUNT_ID`, `AWS_SSH_KEY` (the whole `.pem`
  text). The README never lists them; their names come from the workflow. Values shown only as
  `***`. V3: the badge's copy into the vault.
- C3: CODE(ci_cd_aws.yml: 18-23) `aws-actions/configure-aws-credentials@v4`; CODE(25-33): `aws sts
  get-caller-identity`, `aws s3 ls`, the ECR login with `secrets.AWS_ACCOUNT_ID` (the same
  `InvalidClientTokenId` as `34` without a real key: said, not shown).
- C4: CODE(41-44): the runner builds the same toolbox from the committed Dockerfile — so the Helm fix
  from S05 belongs in your commit (whether GitHub's runner hits the same certificate error was not
  tested). CODE(46-50) + extra `51`: `DOCKER_TAG=20261108011909` into `$GITHUB_ENV`. CODE(52-58):
  plain `docker build` / `docker tag` / `docker push` of the frontend; 60-70 repeat it for the other
  two (not built here). Contrast with V5 on a BLUE runner: the runner builds the app images itself;
  the toolbox only deploys.
- C5: CODE(72-90) + extra `52`: `~/.ssh/config` and `~/.ssh/ac215_2024.pem` written from the
  secret, `chmod 600`, copied to `src/deployment/secrets/` (on the runner only, never committed).

**S14 · Follow one tag to the server (~280) — `s14_deploy.py` · `FollowTheTag`.** Tracker C6–C7.
- C6: CODE(ci_cd_aws.yml: 113-123) the toolbox on the runner (socket, `/deployment`, `/root/.ssh`,
  five `-e`), CODE(124-131) the `bash -c` chain: permissions, ECR login, `deploy-setup-containers.yml`
  with `--extra-vars … docker_tag=$DOCKER_TAG`, then `deploy-setup-webserver.yml`. Extra `53`
  (from `docker run`): `Deploying with tag: 20261108011909`, the `/root/.ssh` listing, then the ECR
  login's `UnrecognizedClientException`: the `&&` chain stops and neither playbook runs.
- V6's second half: tag → ECR → server → recreated containers; the L22 rolling-update inset (the
  slides' "deploy to the K8s cluster" = "recreate the containers on the server" here).
  `lecture_ref(23, "18–19")` while the two pictures sit side by side.
- C7 ▶ what to commit first, as a YELLOW checklist: your server's IP in `inventory.yml:30` (CI
  deploys to whatever IP is committed), line 4 active again (the CI key path), the Helm fix. Then
  the three commands with this repo's keyword; the Actions run page (`illustration`, step names
  from the file, no log text). Monitor, in this repo: the run's colour means "every step exited 0",
  not "the app works": reload the site; on the server `sudo docker container ls` shows the new tag
  in the IMAGE column.
- `lecture_ref(23, "11–12")`: PONDER 4 (10 s), answered with V8's toggle and the MS5 outlook in one
  sentence.

**S15 · The delete that deletes nothing (~210) — `s15_teardown.py` · `Teardown`.** Tracker B15.
- PONDER 5 (8 s) over CODE(deploy-create-instance.yml: 39-46) and the `when:` lines (24, 37).
- B15 ▶ README 147 → `48`: two tasks `skipping`, then `Create EC2 instance`: `fatal: … 'dict
  object' has no attribute 'group_id'`, PLAY RECAP `ok=1 … failed=1 skipped=2`, before any AWS call.
  V4: the two `when:` tiles grey out, dashed; the third tile has no `when:` and trips. Even past it,
  CODE(94-100)'s removal needs a volume id that only a create run registers, and no task terminates
  the instance. "So clean up by hand."
- The teardown card (see "Costs and teardown"), `illustration`, GOLD, each line spoken briefly.
  `lecture_ref(23, "15")` for one clause: cost is one of the lecture's CD challenges.

**S16 · The course on one server, and recap (~350) — `s16_review.py` · `CourseReview`.** No
tracker.
- `lecture_ref(23, "21–37")`: the lecture closes by walking back through the course; here every
  review slide lights a part of V7's server and the laptop beside it, with **this year's** lecture
  numbers (SLIDES.md "Pointers"), one short phrase each, ~12 s per group:
  - 22 venvs, VMs, containers (L01–L02) → the EC2 server, the containers, pipenv inside each image;
  - 23 independent containers through a shared bucket (L03); 24 the "senior developer" who rebuilds
    and pushes images by hand (L03–L04) → that job is now the runner's;
  - 25 the solution architecture, process / execution / state → frontend and API (execution),
    ECR and the disk (state);
  - 26 labeling (L11); 27–31 the LLM lectures: instruction tuning, RAG (L05) → the loader, Chroma
    and the chat route; agents (L06–L07); LoRA and distillation (L08) → not on this server: the API
    calls ready-made models through Bedrock;
  - 32–34 training jobs, model deployment, pipelines (L13, L15) → on AWS, L15's SageMaker pipeline,
    not on this server;
  - 35 API and frontend containers (L18) → `api-service`, `frontend`;
  - 36 the CI loop with Release (L09, L21) → today's Release box;
  - 37 routing to services (L20, L22) → today's nginx.
- V8's MS5 loop and V3's two overlays as "where next": tests in front (L21), deploy on every merge,
  an instance role and OIDC instead of copied keys, Chroma pinned, HTTPS.
- Recap questions (5, one at a time; answers in exercises.md). Point to the study guide and
  exercises in MLOps_Learning. End on an empty frame.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 220 | S11 WhoPressesRelease | 330 |
| S02 LectureMap | 280 | S12 TwoSieves | 250 |
| S03 ConsoleSetup | 260 | S13 RunnerSecrets | 270 |
| S04 AnsibleInOnePicture | 220 | S14 FollowTheTag | 280 |
| S05 StartToolbox | 320 | S15 Teardown | 210 |
| S06 InsideToolbox | 230 | S16 CourseReview | 350 |
| S07 BuildAndPush | 250 | | |
| S08 CreateAndProvision | 240 | | |
| S09 SetupContainers | 290 | | |
| S10 FrontDoor | 200 | | |
| **part 1** | **2,510** | **part 2** | **1,690** |

Total ≈ **4,200** words ≈ 24 min of narration. If the script runs long, trim S02's term-by-term
transform (keep four labels), S06's version list and S16's per-slide phrases (group them) first;
never trim a README step or a first error.

## Ponder questions

Five timed ponders (Conny, 2026-10-21: 3–5 per video; REVIEW.md marks content gate 3 met with that
decision). Each is quiz-style with a YELLOW timer and answerable from what was just shown; the
answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S06 (8 s) | "Inside the toolbox, Ansible runs docker build\nfor the frontend.\nWhose disk does the image land on:\nthe toolbox's, or your laptop's?" | The laptop's: `docker` in the toolbox talks to the laptop's engine through the mounted socket (`docker-shell.sh:36`); the image is a sibling of the toolbox, and a `prune -a` from inside would sweep the laptop |
| 2 | S10 (8 s) | "The browser asks nginx for /api/newsletters.\nWhich path does api-service receive?" | `/newsletters`: the trailing `/` in `proxy_pass http://api-service:9000/;` replaces the matched `/api/` (`laptop/62`: `api-service received /newsletters`); that is where FastAPI mounts the router |
| 3 | S12 (8 s) | "You push 'fix typo /run-tests' to main.\nNothing, build-and-push only,\nor a full deploy?" | Build and push only: the job's `/run-` sieve passes, the deploy step's `/run-deploy-app` sieve does not; three new images land in ECR (storage), the server keeps the old tag |
| 4 | S14 (10 s) | "By the lecture's definitions,\nis typing /run-deploy-app\ncontinuous delivery or continuous deployment?\nWhat would make it the other?" | Delivery's release button: a person decides each release, and nothing is tested first. Deploying every merge to `main`, behind L21's tests, makes it continuous deployment (MS5) |
| 5 | S15 (8 s) | "cluster_state=absent.\nWhich tasks run, and what gets deleted?" | The security group and EBS tasks are skipped (`when: … == "present"`); "Create EC2 instance" has no `when:` and fails on the undefined `security_group.group_id`; nothing is deleted (`laptop/48`) |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Name the two secrets this tutorial creates, what each one opens, and three places the access key
   ends up after one deploy. What would an instance role and GitHub OIDC remove?
2. Why does `sh docker-shell.sh` fail on Ubuntu but work on a Mac, and what did `pip install
   ansible>=9.0.0` actually do?
3. A `hosts: localhost` play and a `hosts: appserver` play: where does each task run, and why can the
   toolbox's `docker build` fill your laptop's disk?
4. Follow one timestamp from `date` to a running container. Where is it written down, and how does
   the server choose between `DOCKER_TAG` and `.docker-tag`?
5. Which of these deploy: `update readme`, `fix /run-tests`, `/RUN-DEPLOY-APP`, `\run-deploy-app`?
   In the lecture's words, is this pipeline continuous delivery or continuous deployment?

## Errata and drift to state (kindly, with the fix)

1. **`sh docker-shell.sh` fails on Linux** (README 77; `laptop/23`, `24`) → `bash docker-shell.sh`;
   on macOS the README line works (S05).
2. **The toolbox did not build as committed at the time of recording** (`Dockerfile:33-34`;
   `laptop/25`, `26`) → delete the two Helm lines and `helm` (no playbook uses it); and since
   `docker-shell.sh` has no `set -e`, read the build's output, not just the last line (S05; the same
   fix in your commit for CI, S13).
3. **The README's CSV path has three `../`, the script four; `SECRETS_DIR` and the account id need
   editing too, and the README doesn't say so** (`docker-shell.sh:10, 17, 26`; `laptop/21`, `28`,
   `30`, `31`) (S05).
4. **`ansible>=9.0.0` is a redirect, not a pin** (`Dockerfile:37`; `laptop/32`, `33`) → quote it, on a
   newer base image (S06).
5. **Three names for one key pair** (README 64 vs `inventory.yml:4, 7, 16`, `docker-shell.sh:27`,
   the workflow; `laptop/13`, `31`) → name it `ac215_2024`, or change them all (S03, S09).
6. **"in GCP" headings and "SSH … from the GCP console"** (README 92, 99, 120) → it is EC2; `ssh -i …
   ubuntu@<EXTERNAL_IP>` or EC2 Instance Connect (S08, S09).
7. **The "API's to enable" list is commented out** (README 7–13) → nothing to enable on AWS; check
   Bedrock model access (S03).
8. **The server runs `chromadb/chroma:latest`, the clients speak 0.5.18** (`deploy-setup-containers.yml:151`;
   `laptop/60`, `61`) → pin `chromadb/chroma:0.5.18`, as `docker-compose.yml:25` does (S09).
9. **`docker run -it` in an Ansible task** (`deploy-setup-containers.yml:165`; `laptop/66`) → if
   "Load Vector DB" fails, drop `-it` (untested under Ansible; say so) (S09).
10. **The README's delete command deletes nothing** (README 147; `laptop/48`) → clean up in the
    console (S15).
11. **The workflow, its four secrets and the keyword are not in the README**; the slides' keyword
    `/deploy-app` belongs to the Google Cloud repo (S12, S13).
12. **The workflow is named "Continuous Integration and Continuous Deployment" but runs no test**
    (`ci_cd_aws.yml:1`) → it's the CD half; put L21's tests in front (S11, S14).
13. **Slide 20's bare `git add`** stages nothing → `git add .` on screen, no narration (S12/S14).
14. Not in the video (exercises.md only, reasoned, not run): the instance's own disk and the 50 GB
    volume both ask for `/dev/sdf`, and the volume is pinned to `us-east-1a` (digest G15); the RAG
    route's 256- vs 1536-number embeddings and the missing `import json` (G11, G12); "Wait for SSH"
    from the toolbox needs outbound port 22 (G16).

**Slides vs repo** (SLIDES.md's conflicts, re-read against the AWS repo and the captures): one EC2
server with containers instead of a K8s cluster, Ansible instead of Pulumi, ECR instead of Artifact
Registry, an IAM access key and a key pair instead of a service-account key (S02); no ML lane here
(S02, S11, S16); the slides' "invoke the CLI in the deployment container" = `ansible-playbook` in
the toolbox (S02, S14); "release" = the timestamped images landing in ECR (S11, S14); slide 37's
`/api/` is exactly this repo's nginx path (S10); slide 19's Model Deploy → Backend API arrow has no
counterpart here (S02, dashed); the review slides' lecture numbers are another year's: on screen,
this year's (S16).

## Costs and teardown

GOLD tags **without amounts** (as in L15): "billed by the hour", "billed per GB-month", "per
token"; point to AWS's pricing pages. Where they appear:
- S01: one GOLD line: "this lecture runs a server until you delete it";
- S07: ECR storage, a new set of three images per deploy, nothing deletes old tags;
- S08: the `t2.large` instance from create to terminate, its disks (the separate 50 GB volume
  outlives the instance), its public IPv4 address;
- S09/S16: Bedrock per token for every chat message;
- S12/S13: a `/run-` commit pushes three more images; Actions minutes on private repos.

Teardown card (S15), each line spoken, all `illustration`:
1. EC2 → Instances: terminate `cheese-app-demo`.
2. EC2 → Volumes: delete `cheese-app-demo-disk` (it survives the instance).
3. EC2 → Security Groups: delete `app_security_group`; Key Pairs: delete yours.
4. ECR: delete the three repositories (or their images).
5. IAM: deactivate and delete the access key; delete the user and `CheeseAppECRPolicy` if you made
   them only for this.
6. GitHub: delete the four repository secrets.
7. Locally: `docker image rm cheese-app-deployment` (2.52 GB on our laptop, `29`), and keep or
   `git restore` your three edited files (`49`: `Dockerfile`, `docker-shell.sh`, `inventory.yml`).

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order, and the workflow's steps after it.

| README instruction | README line | capture | scene |
| --- | --- | --- | --- |
| "API's to enable in AWS before you begin" (empty) | 7–13 | source panel | S03 |
| IAM → Policies → Create Policy → JSON, paste, "Review Policy", name `CheeseAppECRPolicy` | 19–46 | `illustration`; `laptop/10` (extra) | S03 |
| Create user `deployment-ac215-user`, three managed policies, attach `CheeseAppECRPolicy` | 48–50 | `illustration` | S03 |
| Create access key → Third Party Service → download the CSV; save in `secrets/` | 52–60 | `illustration`; `laptop/12` | S03 |
| Create key pair `cheese-app-ac215-key-pair`, save the `.pem` in `secrets/` | 64 | `illustration`; `laptop/12`, `13`, `14` | S03 |
| "Deployment Setup": four details in `inventory.yml` | 67–72 | CODE `inventory.yml`; `laptop/35` | S04, S06 |
| Go to `src/deployment` | 75 | `laptop/20` | S05 |
| `CSV_FILE="../../../secrets/deployment-ac215-user_accessKeys.csv"` | 76 | `laptop/21` (extra), `22` | S05 |
| `sh docker-shell.sh` | 77 | `laptop/23` (+ `24`–`31`) | S05, S06 |
| Create the three empty ECR repositories | 79–85 | `illustration` | S07 |
| `ansible-playbook deploy-docker-images.yml -i inventory.yml` | 89 | `laptop/40` | S07 |
| `ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=present` | 94 | `laptop/42` | S08 |
| Get the IP from the console, update `appserver>hosts` | 97 | `illustration`; `laptop/43` | S08 |
| `ansible-playbook deploy-provision-instance.yml -i inventory.yml` | 102 | `laptop/44` | S08 |
| The key-line toggle in `inventory.yml` | 107–111 | `laptop/45` | S09 |
| `ansible-playbook deploy-setup-containers.yml -i inventory.yml` | 116 | `laptop/46` | S09 |
| SSH in; `sudo docker container ls`; `… logs api-service -f`; `… logs frontend -f`; `… logs nginx -f`; `sudo docker exec -it api-service /bin/bash`; `sudo docker exec -it nginx /bin/bash` | 120–132 | shown verbatim; `laptop/63`–`65` stand-ins (extra) | S09 |
| "Create nginx.conf file for defaults routes" | 136–137 | CODE `nginx.conf`; `laptop/62` (extra) | S10 |
| `ansible-playbook deploy-setup-webserver.yml -i inventory.yml` | 141 | `laptop/47` | S10 |
| go to `http://<External IP>/` | 143 | `illustration` | S10 |
| `ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent` | 147 | `laptop/48` | S15 |
| (workflow) trigger and gates | `ci_cd_aws.yml` 3–9, 99–100 | CODE; `laptop/50` | S12 |
| (workflow) four repository secrets | 21–22, 33, 81, 102–108 | `illustration` | S13 |
| (workflow) AWS login, toolbox build, tag, image builds, SSH key | 18–97 | CODE; `laptop/51`, `52` | S13 |
| (workflow) deployment container | 99–131 | CODE; `laptop/53` | S14 |
| (slide 20) `git add .` · `git commit -m "… /run-deploy-app"` · `git push` | — | shown; run page `illustration` | S14 |

## Things never to do

Series list: no slide images or PDF pages in a frame or the repo (re-draw, cite the PDF page
number); no logos (AWS, GitHub/Octocat, Docker, Ansible, Kubernetes, the six CI/CD services of
slide 16); no real person's name on screen or in subtitles (the instructor is `‹instructor›` if ever
needed; slide 4's page and its names, slide 20's QR code and slide 31's photo are never drawn); no
hand-typed "output"; no command spelled differently from the README; no credentials, keys, tokens,
IPs, account ids, ARNs or project ids that look real.

Lecture-specific:
- **Never show an unmasked committed value**: the author's account id (`YOUR_ACCOUNT_ID`), the
  server IP (`<EXTERNAL_IP>` / `EXTERNAL_IP`), the `NEXTAUTH_SECRET` (`<nextauth-secret>`), the
  `‹instructor›` lines of `vector-db/cli.py`. Code panels quote `assets/source/` only.
- Never show a key that looks like one: no `AKIA…`, no `.pem` text, no CSV row other than
  `<aws-access-key-id>,<aws-secret-access-key>`; the placeholder `export` line of `53` is cropped.
  AWS's own documented example keys may be quoted only with the label "AWS's documentation example".
- **Never present an illustration or a stand-in as the real thing**: the IAM/EC2/ECR consoles, the
  server's screen, the browser and GitHub's pages are `illustration`; `63`–`65` and `62` are
  `extra · stand-in on the laptop`; `50`–`53` are "the workflow's own commands, run by hand". Never
  say "the server printed" or "the Actions log shows".
- Never say the deployment works end to end today: we could not run it, and the Chroma drift would
  break it. Say what success looks like, never that it happened.
- Never show prices or amounts; GOLD tags name the meter only.
- Never show `git log` author lines, staff names or staff branch names; 7-character commit ids.
- Never show the capture-only machinery: `capture-only/*`, the proxy, the relay, the mirror,
  `AWS_CA_BUNDLE`, the hand-started `dockerd`.
- Never say the slides are wrong about Google Cloud: they describe the GCP version; the video
  follows the AWS version and maps the words.
- `lecture_ref` only while that slide's picture or idea is on screen.

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, start from L21's and L15's):
  - tracker factories `tracker_a`, `tracker_b`, `tracker_c` with the step lists above (`tracker_c`
    always captioned "not in the README");
  - prompts `P_LAPTOP = "student@laptop:~/cheese-app-aws/src/deployment$"` and a helper that takes
    the toolbox prompt from the capture; terminal title `laptop`, toolbox title `cheese-app-deployment`;
  - tags `your_turn`, `extra_tag`, `illustration_tag`, `standin_tag` ("extra · stand-in on the
    laptop"), `cost_tag` (GOLD, no amounts), `lecture_ref`;
  - helpers `toolbox_capture(name, pick=…)` (crops the build log and the two warnings),
    `play_recap(line)` (V4's counters from a real RECAP line), `readme_panel(a, b)`,
    `console_drawing(title, fields)` (schematic, no logos);
  - set-piece classes `KeywordSieves` (V1), `TermMap` (V2), `KeyJourney` (V3), `AnsibleMachine`
    (V4), `SiblingContainers` (V5), `TimestampTrail` (V6), `VmLayout` (V7), `ReleaseLoop` (V8). A
    helper never reuses a scene class name from `video.yaml`.
- **Long outputs**: `25` (first lines, `…`, the `ERROR` lines, the last three), `28` (the
  `FINISHED` line, the prompt), the Ansible failures (`40`, `42`, `48`): the `fatal` line wrapped
  and cut to its `msg`/`stderr` text, never the whole JSON; `37`'s task lists as tiles, not a
  scroll; `60`, `62`: the pull lines cut.
- **Two windows on screen** (laptop terminal + toolbox prompt) never happen: the toolbox file is one
  terminal whose prompt changes from `student@laptop` to `root@…:/app#`.
- **The order is the README's**, with the workflow after it; the lecture's CI/CD slides come at the
  start of part 2, where the commit-message trigger needs them.
