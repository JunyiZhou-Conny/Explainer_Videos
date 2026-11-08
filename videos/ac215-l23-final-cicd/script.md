# AC215 · Lecture 23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys — narration script & visual plan (v2, 2026-11-08, after four reviews: build/review_merge_log.md)

Audience: an AC215 student who has done L1–L22, in particular Docker images, `docker-shell.sh`
scripts with bind mounts and pipenv inside images (L02–L04); the cheese app's services, the Next.js
frontend, the FastAPI `api-service`, Chroma and the vector-db loader (L05, L18); L15 on AWS (IAM
users and access keys, ECR, the AWS CLI); L20 (a deployment container driving Pulumi); L21 (GitHub
Actions: workflows, jobs, steps, runners, repository secrets); L22 (Kubernetes, ingress) as the GCP
path this variant does not take. They have seen Lecture 23, which speaks Google Cloud. New to them:
**Ansible** (inventory, playbooks, plays, tasks, modules), EC2 instances, security groups, key pairs,
and a workflow that **deploys**. They watch with a clone of `dlops-io/cheese-app-aws` open, Docker
running, their own AWS account with billing (this lecture runs a server around the clock until they
delete it: GOLD tags without amounts, the clean-up card in S15) and, for part 2, a GitHub repository
of their own, pausing to run each step.

Goal (BRIEF "Audience and goal"): after the video they can create the IAM policy, user, access key
and EC2 key pair, keep both secrets outside the clone and name the key pair so the code finds it;
start the toolbox with `bash docker-shell.sh` and the three edits the script needs, and say why `sh`
fails on Linux, why the build may stop at the Helm key and what `ansible>=9.0.0` really did; read
`inventory.yml` and a playbook as inventory → play → task → module and tell a `localhost` play from
an `appserver` play; explain the Docker socket mount; run the six playbook commands in README order
and read each first error honestly, and know what success looks like (`failed=0`); follow one
timestamp tag from `date` to a recreated container; draw the server (three open ports, five
containers on `appnetwork`, nginx as the only front door, `/api/` stripped); read `ci_cd_aws.yml`
(which messages build, push or deploy; the four repository secrets; what the runner does); say in the
lecture's words what this workflow is (the CD half, a person pressing release) and what Milestone 5
adds; clean up by hand, because the README's delete deletes nothing; place every earlier lecture on
the server (the review, slides 21–37).

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest, rebuilt around
`cheese-app-aws`), `SLIDES.md` (lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md
rule 9), `assets/` (see `ASSETS.md`). **Where the digest or the slides and the captures disagree, the
captures win**, and the video says so kindly. The tutorial is `dlops-io/cheese-app-aws` @ `5950118`
(`main`, the only branch, no tags, still the head on 2026-11-08: `laptop/01`, `03`): the whole README
(148 lines) top to bottom, then `.github/workflows/ci_cd_aws.yml`, which the README never mentions.
`cheese-app-v4` @ `033f187` is the slides' Google Cloud context only: no panel quotes it, nothing is
captured from it. Nothing in a terminal panel is typed by hand: every output line below names its
capture file and line numbers.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown, no
  raw symbols (`/`, `=`, `%`, `&`, `$`, `→`, `_`, `!`, `>`); commands, flags and paths are on screen
  and said in words: "ansible playbook, deploy docker images, dash i, inventory dot yaml"; "S H,
  docker shell dot S H"; "bash docker shell dot S H"; "extra vars, cluster state equals present";
  "slash run dash" (`/run-`), "slash run deploy app" (`/run-deploy-app`), "backslash run deploy
  app"; "slash secrets"; "dot docker tag"; "C I C D AWS dot yaml"; "nginx dot conf"; "AWS S T S
  get caller identity"; "git add dot". Acronyms the voice mangles are spelled with spaces: "E C R"
  (Kokoro says "ecker" for ECR), "E C 2", "E B S", "S S H", "C S V", "S T S", "O I D C",
  "U S East 1", "public I P address" (never "IPv4", never "AMI": "the machine image"). Three are
  written as one word because the lexicon has them and a spaced capital A is read as the article
  "uh": "AWS", "IAM", "AC215" (said "A C two fifteen"); never "A W S", "I A M", "A C 215".
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command or file name. No `'s` after AWS, GitHub,
  Ansible or any word with a lexicon entry ("the AWS API", "the vault on GitHub"). No homographs:
  never "read", "live", "lives", "close", "lead", "tear", "minute", "content", "record(s)". No
  spoken decimals or version numbers ("version 1", "an older Ansible, version 6", "an old Python");
  versions sit on screen with the chip "at the time of recording". Never read a commit id, a
  timestamp, a container id, a digest or a request id. Numbers are digits; never a "!" after a
  digit. Main clause first, so the Chinese subtitles keep English clause order. American spelling
  on screen and in SAY ("color", "gray"); colour constants stay GREY etc.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; text ≥ 20 pt inside
  the safe frame; every scene ends on an empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card leaves at the start of the next block). The SAY before the card
  speaks the question; the next SAY gives the answer. Nothing during the timer shows the answer.
  Five in the video (BRIEF's table; Conny's 2026-10-21 density decision): P1 S06 (8 s), P2 S10
  (8 s), P3 S12 (8 s), P4 S14 (10 s), P5 S15 (8 s). The cards carry no number.
- `TERM(laptop/NN: lines)`: a laptop terminal beat, full width (12.6 units), title `laptop`, prompt
  `P_LAPTOP = "student@laptop:~/cheese-app-aws/src/deployment$"` (from S05 block 1 on; before it
  `student@laptop:~$` or `student@laptop:~/cheese-app-aws$`, as the SHOW says). The scene types
  the command written just before it in the SHOW line (exactly as the README spells it; extras
  exactly as the capture's line 1 spells it, folding with ` \`), then prints the listed **file**
  lines of `assets/terminal/laptop/NN-*.txt`. Line 1 is the `$ …` command: typed, never printed;
  `[exit N]` is never printed. `…` = print one `…` line; `wrap` = fold long lines; `→ (no output)`
  = the prompt simply returns. When a picture needs the frame, the terminal shrinks to a 3-row strip
  along the bottom; a full terminal and a picture never share the frame.
- `TBX(laptop/NN: lines)`: a **toolbox** beat in the same terminal, title `cheese-app-deployment`,
  prompt taken from the capture's line 35 (`root@<container id>:/app#`; the id changes on every run;
  said once in S05, never read). The command after the `# ` on line 35 is typed (README commands are
  the README's text, character for character); then the listed lines are printed. Lines 1–34 (the
  `bash docker-shell.sh` build log, mostly cached) are never printed after S05. The
  `CryptographyDeprecationWarning` pair (a line containing `CryptographyDeprecationWarning` and the
  next line `  from cryptography.exceptions import InvalidSignature`) is cropped **by text match**
  wherever it occurs (36–37 in `35`–`37`, `40`, `42`, `44`, `46`–`48`; 38–39 in `32`; it is not in
  `28`, `31`, `33`, `34`, `38`, so a line-number crop there would delete shown lines);
  the `community.general` warning block is shown once (S06 block 6, from `40`: 38–41) and cropped
  afterwards. `msg` after a line number = print only the text of that JSON line's `msg` (or `stderr`)
  value, wrapped, prefixed with the line's own `fatal: [host]: FAILED! =>` or `UNREACHABLE! =>` head,
  never the whole JSON (request ids, dates and headers are never shown). The capture-only
  `AWS_CA_BUNDLE` line (`31`: 43) is always cropped.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` with the real line numbers,
  header `path · lines a–b`; at most 12 lines on screen at once (longer ranges are given as two
  panels, the second replacing the first by a Transform). Masked lines appear as in the copy
  (`YOUR_ACCOUNT_ID`, `<EXTERNAL_IP>:`, `<value not copied: see ASSETS.md>` shown as
  `<nextauth-secret>`). `README(a–b)`: a GREY README card, header `README.md · lines a–b`,
  markdown stripped, list markers kept; on the next block it shrinks into the tracker's caption
  (Transform) unless the SHOW keeps it.
- `CONSOLE(title; fields)`: `console_drawing(title, fields)`, a schematic console page (BLUE frame
  labelled "AWS · us-east-1" or "GitHub", GREY form rows with the README's field values), tag
  `illustration`. No logos, no screenshots.
- Trackers (`ReadmeTracker`, top-left), from BRIEF "README step tracker":
  - `TRACKER A n` = "README › Before you deploy", 6 steps: 1 APIs to enable · 2 ECR policy · 3 IAM
    user · 4 Access key · 5 Key pair · 6 Deployment setup (README 7–72).
  - `TRACKER B n` = "README › Deployment Steps", 15 steps: 1 Go to folder · 2 Edit CSV path ·
    3 docker-shell.sh · 4 ECR repositories · 5 Build and push · 6 Create instance · 7 Copy the IP ·
    8 Provision · 9 Key line · 10 Setup containers · 11 Server checks · 12 Nginx config · 13 Setup
    webserver · 14 Open the site · 15 Delete instance (README 74–148).
  - `TRACKER C n` = "ci_cd_aws.yml", caption always "not in the README", 7 steps: 1 Trigger ·
    2 Repo secrets · 3 AWS login · 4 Build and push · 5 SSH key · 6 Deploy step · 7 Commit, push.
  `· extra` after a tracker step = caption " · extra" while a command the README does not have is
  on screen. S01, S02, S11 and S16 have no tracker.
- `LECTURE 23 · a–b` in a SHOW line: the GREY `lecture_ref(23, "a–b")` tag (top right, "Lecture 23 ·
  slides a–b"; "slide" for one) **for that SHOW block only**: it fades in with the redrawn lecture
  picture and out with it at the end of the block. `LECTURE (held)` in the next block keeps it, only
  while the same picture stays on screen. Slide numbers are the PDF pages of `SLIDES.md`, never the
  footers. Every lecture picture is our own redrawing in series colors with the slide's structure
  and terms: no slide image, turkey page, distillation photo, QR code, logo or screenshot; no name
  from any slide.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed line,
  and the SAY says "extra" the first time each kind appears.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint; the SAY of the block, or of
  the step's first block, says "pause" at the playbook runs (B5, B6, B8, B9, B10, B13) and where the
  viewer works alone (A2, B3, C2, C7). Used at A2–A5, B1, B2, B3 (the working toolbox), B4, B5, B6,
  B7, B8, B9 (done before B8: see S08), B10, B11, B13, B14, B15, C2 (the repository and the secrets)
  and C7.
- Working directory: whenever the SHOW returns to `P_LAPTOP` while the toolbox is open, a GREY chip
  says "second laptop terminal · the toolbox stays open · /app is this folder, edits show up inside
  at once" (S05 block 10 is the exception: there the viewer types `exit` first, because the toolbox
  is rebuilt).
- Tags (GREY unless said): `illustration` (every console drawing, the server's screen, the browser,
  every GitHub page, the clean-up card); `extra` (every command the README does not have);
  `extra · stand-in on the laptop` (`standin_tag`: `62`–`65`, never presented as the server); `the
  workflow's own commands, run by hand` (`51`–`53`); `erratum` (a GREY chip on a README or code
  slip; the SAY says "a small slip", "a small gap" or "a kind note", never "erratum"); `at the time of
  recording` beside versions on first show; GOLD `cost_tag(text)` naming the meter only, never an
  amount: S01 ("this lecture runs a server until you delete it"), S07 ("ECR storage · every tag you
  push"), S08 ("EC2 instance · by the hour, until terminated" · "EBS disks · per GB-month" · "public
  IPv4 address · by the hour"), S09 ("Bedrock · per token"), S12 ("three new images in ECR per
  `/run-` push"), S13 ("Actions minutes · private repos"), S15 (the clean-up card).
- Keys are two WHITE glyphs: a **badge** (the access key: talks to the AWS API) and a **key** (the key
  pair: opens SSH); the place that holds them carries the colour (V3 `KeyJourney`).

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| the laptop: your terminal, your clone, `~/secrets/` (the CSV, the `.pem`), the browser | GREY |
| the cloud: AWS `us-east-1`, the EC2 instance, its EBS disks, ECR, the IAM console; GitHub and its runner | BLUE |
| containers and images: the toolbox `cheese-app-deployment`, the three app images, the five containers on the server, the throwaway loader | TEAL |
| shared, not yours: the course's repo and its committed values (all masked), Docker Hub's `nginx:stable` and `chromadb/chroma:latest`, `0.0.0.0/0`, the AWS-managed policies | ORANGE |
| project-owned, pinned: `inventory.yml`, the five playbooks, `nginx.conf`, the timestamp tag and `.docker-tag`, `chromadb/chroma:0.5.18`, `failed=0`, a ✓ | GREEN |
| tools: Ansible, the AWS CLI, Docker, GitHub Actions (the runner program), `aws-actions/configure-aws-credentials` | PURPLE |
| errors and "don't": every first error, `failed=1`, `UNREACHABLE!`, exit codes ≠ 0, the HTTP 410, the delete that fails, a key in the repo | RED |
| your turn, the README tracker, the CI/CD loop's current box, the ponder timer | YELLOW |
| money: the running instance, its disks and public IPv4, ECR storage, Bedrock tokens, Actions minutes on private repos | GOLD |
| lookups and routes: SSH arrows, the Docker socket line, HTTP routes through nginx, `lookup('env', …)`, the commit-message ribbon through the sieves, the tag's trail | PINK |
| the lecture's GCP words before they turn into AWS words; the future (MS5, instance role, OIDC); *skipped* tasks | GREY, dashed |

AWS is a BLUE box labelled "AWS · us-east-1", GitHub a BLUE box labelled "GitHub": no AWS, GitHub,
Docker, Ansible or Kubernetes logos anywhere, and none of slide 16's six service logos.

Running example
- **The laptop**: a fresh Ubuntu 24.04.5 machine with Docker Engine 29.9.3 (`laptop/00`), user
  `student`, terminal title `laptop`, home = the README's parent folder: `~/cheese-app-aws` and
  `~/secrets` side by side (`12`, README 54–60). Prompt `student@laptop:~$` (S03), then
  `student@laptop:~/cheese-app-aws$` (S05 block 1), then `P_LAPTOP`. A GREY chip, once (S05): "your
  prompt shows your own user" (on screen only, not said).
- **The toolbox**: `root@<container id>:/app#` as captured (TBX). Said once in S05: "The prompt ID
  changes on every start".
- **The secrets**: the CSV holds AWS's header and obviously fake placeholder values; on screen and in
  narration only `<aws-access-key-id>` / `<aws-secret-access-key>` (the CSV's text is never printed).
  The `.pem` is a throwaway key made for no account; its text is never shown. The account id is
  always `YOUR_ACCOUNT_ID`; the server's address `<EXTERNAL_IP>`, or the placeholder host
  `EXTERNAL_IP` once it is in the inventory (`43`). No `AKIA…` string anywhere.
- **The honesty sentence** (load-bearing), said once in S01 block 5 and never apologised for again:
  this machine has no AWS account; everything on the laptop ran for real; every command that talks
  to AWS ran exactly as the README writes it, up to its real first error; consoles, the server's
  screen and GitHub's pages are drawings marked `illustration`. Never "the server printed", never
  "the Actions log shows"; never "the deployment works end to end". What success looks like is
  described over the playbook's own task list, never as an output panel.
- **Versions** (on screen with "at the time of recording", never spoken): laptop Docker 29.9.3;
  toolbox aws-cli 2.39.6, ansible 6.7.0 / core 2.13.13, Python 3.8.10, Docker CLI 28.1.1, kubectl
  v1.28.15, no helm (`32`); `nginx:stable` = nginx 1.30.6 (`65`); `chromadb/chroma:latest` =
  `"1.0.0"` (`60`).
- **Never quoted**: commit ids beyond 7 characters (`5950118` on screen only), the `.pem` text, the
  CSV values, `git log` authors, the request id and headers in `42`: 46, container ids, digests,
  build timings other than "132.8s" on its line.

Length and parts: narration target 3,900–4,300 words (`python -m explainer.script`, which counts SAY
words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm)
that is ≈23–24 min of narration, ≈30–32 min with typing, outputs, drawings and five ponder timers.
Part 1 = S01–S10 (**deploy by hand with Ansible**: the README top to bottom; ends on the
illustrated browser and "next, a commit message does the redeploy"). Part 2 = S11–S16 (**let a
commit press the button, clean up, review**). The cut is the README's own seam, "Once the command
runs go to `http://<External IP>/`" (README 143). Each part ends on an empty frame.

| scene | words (BRIEF · band ±15 %) | scene | words (BRIEF · band ±15 %) |
| --- | --- | --- | --- |
| S01 Hook | 203 (220 · 187–253) | S11 WhoPressesRelease | 272 (330 · 281–380) |
| S02 LectureMap | 224 (280 · 238–322) | S12 TwoSieves | 253 (250 · 213–288) |
| S03 ConsoleSetup | 288 (260 · 221–299) | S13 RunnerSecrets | 298 (270 · 230–311) |
| S04 AnsibleInOnePicture | 234 (220 · 187–253) | S14 FollowTheTag | 326 (280 · 238–322) |
| S05 StartToolbox | 331 (320 · 272–368) | S15 Teardown | 201 (210 · 179–242) |
| S06 InsideToolbox | 255 (230 · 196–265) | S16 CourseReview | 344 (350 · 298–403) |
| S07 BuildAndPush | 248 (250 · 213–288) | | |
| S08 CreateAndProvision | 300 (240 · 204–276) | | |
| S09 SetupContainers | 294 (290 · 247–334) | | |
| S10 FrontDoor | 223 (200 · 170–230) | | |
| **part 1** | **2,600** (2,510) | **part 2** | **1,694** (1,690) |

Total **4,294** words (v2, after the review merge), 6 under the series ceiling (4,300). Four scenes
sit outside their ±15 % band, by decision of the merge (build/review_merge_log.md): S08 (+24 over its band: it now
carries the README-order key switch of step 9 and the untested attach), S14 (+4 over: the commit checklist
with four edits and the `git add .` warning), S02 (14 under) and S11 (9 under), trimmed of lines that S02 b6, S11 b7 and
S02 b8 already said, to pay for those. Re-run the counter after any edit; BRIEF's trim order if it runs long: S02's
term-by-term transform (keep four labels), S06's version list, S16's per-slide phrases; never a
README step or a first error.

Notes for scene authors
- **Shared code** (`scenes/common.py`, start from L21's and L15's): tracker factories `tracker_a(k,
  extra=False)`, `tracker_b(k, extra=False)`, `tracker_c(k)` (always captioned "not in the
  README"); `P_LAPTOP`; a helper that takes the toolbox prompt from line 35 of a capture;
  `toolbox_capture(name, pick=…)` (crops lines 1–34, the cryptography pair **by text, not by index**, and, after S06, the
  `community.general` block; `msg=True` extracts a fatal line's `msg`/`stderr` text); tags
  `your_turn`, `extra_tag`, `illustration_tag`, `standin_tag`, `erratum_tag`, `cost_tag`,
  `lecture_ref`; helpers `play_recap(line)` (V4's five counters from a real RECAP line),
  `readme_panel(a, b)`, `console_drawing(title, fields)`; set pieces `KeywordSieves` (V1),
  `TermMap` (V2), `KeyJourney` (V3), `AnsibleMachine` (V4), `SiblingContainers` (V5),
  `TimestampTrail` (V6), `VmLayout` (V7), `ReleaseLoop` (V8). A helper never reuses a scene class
  name from `video.yaml`. `erratum_tag` is not in BRIEF's tag list: add it (L21 has one).
- Capture line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the
  output body, so pick index = file line − 1. Assert the picked text of every highlighted line.
- Multi-line captured commands (`51`, `52`, `53`: the workflow's own `run:` scripts): never typed
  character by character. The terminal shows a GREY heading row "ci_cd_aws.yml · lines a–b · run
  by hand" with tag `extra` and `the workflow's own commands, run by hand`, then the listed output
  lines. `53`'s line 1 (the placeholder `export`) is never shown.
- **Long outputs**: `25` (lines 3, `…`, 20, 28, 34, `…`, 49 — line 49 is the RED "Unable to find
  image" line; 50 wrapped if room); `28` (3, 33, then the prompt); `37`'s task lists as V4 tiles,
  not a scroll; `60` (28, 29 wrap; the pull lines 7–27 never shown); `61` (40, 41); `62` (34–38).
- **Lexicon**: a spelled capital A is read as the article ("A W S" → "uh double-u S", "A C 215" →
  "uh C two hundred fifteen", "I A M" → "eye uh em"), so SAY writes `AWS`, `IAM` and `AC215`, which
  have lexicon entries already. Two phrase keys were added for this video under `# AC215 L23`
  (`underscore 2024` → "underscore twenty twenty-four", `status 410` → "status four ten"); both occur
  in no other video's SAY. Checked with `KokoroBackend.phonemize` on 2026-11-08: "Ansible", "nginx",
  "Chroma", "Bedrock", "kubectl", "playbook", "appserver", "localhost", "E C R", "E C 2", "E B S", "S
  S H", "C S V", "S T S", "O I D C", "U S East 1", "the I P address", "Next auth secret", "sudo",
  "unreachable", "recreated", "here string" all come out right. **Do not** write `ECR` (→
  "ecker"), `AMI` (→ "a M I"), `IPv4` (→ "ipv four"), `OIDC` (→ "oydk"), `ISRG`, or a spaced
  "A W S" / "I A M" / "A C 215" in SAY.
- Subtitle display for the i18n stage (`en_display`): ansible playbook, deploy docker images, dash i,
  inventory dot yaml → `ansible-playbook deploy-docker-images.yml -i inventory.yml` (and the five
  other playbook commands the same way, with `--extra-vars cluster_state=present/absent`); S H,
  docker shell dot S H → `sh docker-shell.sh`; bash docker shell dot S H → `bash docker-shell.sh`;
  slash run dash → `/run-`; slash run deploy app → `/run-deploy-app`; backslash run deploy app →
  `\run-deploy-app`; slash deploy app → `/deploy-app`; slash run tests → `/run-tests`; slash
  secrets → `/secrets`; dot docker tag → `.docker-tag`; docker tag (the variable) → `DOCKER_TAG`;
  C I C D AWS dot yaml → `ci_cd_aws.yml`; inventory dot yaml → `inventory.yml`; nginx dot conf →
  `nginx.conf`; AWS S T S get caller identity → `aws sts get-caller-identity`; docker system
  prune, dash a → `docker system prune -a`; dash f → `-f`; dash I T → `-it`; set dash e → `set -e`;
  git add dot → `git add .`; git commit → `git commit -m "…"`; git push → `git push`; slash API
  slash → `/api/`; slash API slash newsletters → `/api/newsletters`; slash newsletters →
  `/newsletters`; slash M N T slash disk 1 → `/mnt/disk-1`; slash home → `/home`; slash
  deployment → `/deployment`; slash root slash dot S S H → `/root/.ssh`; AC215 underscore 2024
  dot pem → `ac215_2024.pem`; AC215 underscore 2024 → `ac215_2024`; cheese app AC215 key pair →
  `cheese-app-ac215-key-pair`; deployment AC215 user → `deployment-ac215-user`; cheese app E C R policy → `CheeseAppECRPolicy`;
  cheese app deployment → `cheese-app-deployment`; appnetwork → `appnetwork`; cluster state equals
  absent → `cluster_state=absent`; change mode 400 → `chmod 400`; head commit → `head_commit`;
  E C R / E C 2 / E B S / S S H / C S V / S T S / O I D C → ECR / EC2 / EBS / SSH /
  CSV / STS / OIDC; U S East 1 → `us-east-1`; fix typo slash run tests → `fix typo /run-tests`;
  update readme → `update readme`; slash run deploy app in capitals → `/RUN-DEPLOY-APP`; slash
  frontend react → `/frontend-react`; external I P → `EXTERNAL_IP`; AWS S S H key → `AWS_SSH_KEY`;
  docker run, dash I T → `docker run -it`; T 2 large → `t2.large`; status 410 → `410`; here string →
  `here-string (<<<)`; the tag latest → `latest`; Next auth secret → `NEXTAUTH_SECRET`; the when
  lines → the `when:` lines; dot dots → `..`; line 151 → `deploy-setup-containers.yml:151`. In zh all
  of these stay English (glossary rule).
  Metaphors for the zh glossary, rendered the same way every time: "sieve" → 筛子; "badge" → 徽章;
  "toolbox" → 工具箱容器; "front door" → 前门; "release button" → 发布按钮.
- **BRIEF corrections found while scripting** (captures and sources win):
  - B1: `laptop/20` captures `pwd; ls -a` after the move into the folder; `cd src/deployment` is
    typed from `student@laptop:~/cheese-app-aws$` and prints nothing (the README has no command
    here, only "Go to src/deployment folder").
  - `docker-shell.sh:35-48` (14 lines), `inventory.yml:13-30` (18), `deploy-docker-images.yml:18-30`
    (13), `deploy-setup-containers.yml:101-114` (14), `ci_cd_aws.yml:72-90` (19) and
    `README.md:22-44` (23) are longer than 12 lines: each is given as two panels.
  - BRIEF S09 cites `deploy-setup-containers.yml:147-152`; line 147 is blank: the panel is 148–152.
  - `docker-shell.sh:39` mounts `$HOME/.ssh` at `/home/app/.ssh` too (a seventh mount, unused by the
    playbooks): visible in the panel, not animated, not narrated.
  - The `community.general` warning appears only for the playbooks that use `docker_image`
    (`36`, `37`, `40`), not for every command: S06 says "two warnings you'll see".
  - `50` lists 39 subjects: 33 `/run-deploy-app`, one `\run-deploy-app`, five others (the digest's
    "eleven `/run-deploy-app` commits on 2024-11-21" counts one day only; the capture's 33 is the
    whole branch).
  - On the server, `lookup('env', 'DOCKER_TAG')` (`deploy-setup-containers.yml:103-104`) is
    evaluated on the Ansible controller, i.e. inside the toolbox: the tag "wins" because the toolbox
    has `DOCKER_TAG` in CI (`ci_cd_aws.yml:121`), and the laptop's toolbox does not
    (`docker-shell.sh:43-47`), so a laptop run uses the file. In CI the tag also arrives as
    `--extra-vars … docker_tag=$DOCKER_TAG` (`ci_cd_aws.yml:130`), and extra vars outrank
    `set_fact`, so that is the value used (all three agree). S09 describes the playbook's fork; S14
    says the extra variable wins.
  - README order: step 9 (the key line, README 105–111) is needed **before** step 8. The laptop
    toolbox runs as root and mounts nothing at `/root/.ssh` (`docker-shell.sh:35-48`), so with line 4
    active a real provision fails at SSH. S08 does the switch before step 8 (erratum, said kindly);
    S09 only points back. `laptop/44` was captured before the switch: its error (hostname not
    resolved) comes before any key is read, so it is the same either way.
  - `deploy-create-instance.yml:47-57` gives the instance two disks of its own (root 100 GB, a second
    100 GB at `/dev/sdf`, both deleted with the instance); the attach task (`:85-92`) asks for
    `/dev/sdf` again for the separate 50 GB volume, which is pinned to `us-east-1a` (`:30`) while the
    instance has no zone. Not testable here: S08 hedges ("tries to attach"), and provision formats
    `/dev/xvdf`, the instance's own second disk.
  - The key-pair name: the README says `cheese-app-ac215-key-pair`, the code expects `ac215_2024`
    (`laptop/13`). Our stand-in `.pem` kept the README's name (`laptop/14`, `31`: 39); the viewer's
    is `ac215_2024.pem` (GREY chips say so wherever ours shows).
  - Each playbook here has exactly one play (`laptop/37`); V4 draws "two playbooks, one play each".
- Never: the instructor's name (`‹instructor›` if ever needed); slide 4's page or names, slide 20's QR
  code, slide 31's photo; a logo; hand-typed output; a command spelled differently from the README;
  a real-looking key, token, IP, account id or ARN; an illustration or stand-in presented as real;
  "the slides are wrong" (they describe the GCP version); a price; the capture-only machinery
  (`capture-only/*`, the proxy, the relay, the mirror, `AWS_CA_BUNDLE`, the hand-started `dockerd`).

---

## S01 · Thirty-three commits, one backslash — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker. A full-width terminal `laptop`, prompt `student@laptop:~$`, types
`git -C /home/student/cheese-app-aws log --format=%s | sort | uniq -c | sort -rn` (extra) →
TERM(laptop/50: 2–8). Line 2 (`33 /run-deploy-app`) turns YELLOW on "33"; the other lines dim to
40 %.
SAY: This repository has 39 commits, and 33 of them carry the same message: slash run deploy app. That sentence is a button. Pushed to main, it rebuilds the app and redeploys a server.

SHOW: Line 5 (`1 \run-deploy-app`) grows and turns RED; the backslash pulses. The terminal shrinks
away. **V1 `KeywordSieves`, teaser**: one sieve (PURPLE rim, label `contains(…, '/run-')`); 33 small
PINK ribbons fall through it in a quick stream, each lighting a tiny BLUE server box beneath; then
one RED ribbon `\run-deploy-app` hits the sieve and bounces off.
SAY: And once, the slash leans the other way. To the workflow, that is a different sentence, and nothing runs at all. One character.

SHOW: The sieve dims. A YELLOW question card drops in the middle: "How does a sentence deploy a
server, and why did one character stop it?" It shrinks and stays pinned small, top left (S01 has
no tracker; the lecture tag of block 4 owns the top right), to the end of the scene.
SAY: How does a sentence deploy a server, and why did one character stop it? By the end of part 2, you'll push that sentence yourself.

SHOW: LECTURE 23 · 1–4. A title card "Lecture 23 · Final Deployment and Review" and three chips
under it, one per phrase: "Motivation", "Automation", "Review". Beside "Motivation", a small GREY
sketch of our own: a rising curve on a web page with a dashed "now" line, and a PINK arrow from the
page to a small BLUE server box.
SAY: This is the course's last lecture: final deployment and review, in three parts. Its motivation is a playful prediction web page; our reading of it: even a toy prediction app is only useful when it runs somewhere, and stays current.

SHOW: The card fades. Three groups, one per sentence: a GREY laptop with a GREEN ✓ "ran right here"; a BLUE box "AWS ·
us-east-1" with a RED chip "first real error"; a small schematic console page with the tag
`illustration`.
SAY: This recording machine has no AWS account. Everything on the laptop ran for real. Every command that talks to AWS ran exactly as the README writes it, up to its real first error. The consoles, the server and GitHub are drawings, marked illustration.

SHOW: The groups fade. Three chips line up: "Docker running", "your AWS account + billing" with a
GOLD `cost_tag("this lecture runs a server until you delete it")`, "a GitHub repository (part 2)".
Then three samples, each bright on its phrase: a YELLOW `ReadmeTracker` ("README › Deployment Steps
· step 5 of 15"), a code panel header `src/deployment/inventory.yml · lines 1–11`, a YELLOW `▶ your
turn` tag. Fade; empty frame (the pinned question card fades last).
SAY: You need Docker, your own AWS account with billing, and for part 2, a GitHub repository. This lecture runs a server until you delete it. The tracker names the README step, and your turn means pause and run it.

---

## S02 · The final map, in AWS words — `s02_map.py` · `LectureMap`

SHOW: No tracker. LECTURE 23 · 19. **V2 `TermMap`** draws slide 19's bottom flow from left to right,
one box per phrase: "Dev Team" → PINK "Commits" → a BLUE box "GitHub" (Code · Branches · Actions)
→ "GitHub Actions" (Build → Deploy) → a cloud box with three GREY dashed labels "Storage", "Vertex
AI", "Kubernetes" → "Users".
SAY: Here is the lecture's map. The dev team commits to GitHub, GitHub Actions builds and deploys to the cloud, and users reach the app there.

SHOW: LECTURE (held). Above, slide 19's chain appears box by box: "Data Collector" → "Data Processor"
→ "Model Training" → "Model Deploy" → "Backend API" → "Frontend" (WHITE outlines).
SAY: Above it, the app as one chain, from data to frontend.

SHOW: LECTURE (held). First, at the top edge, a GREY dashed chip "slides: Google Cloud · cheese-app-v4"
transforms into a BLUE chip "this video: AWS · cheese-app-aws · as in L15". Then the GCP labels
**transform** into BLUE AWS labels, one per phrase:
"Kubernetes" → "one EC2 server · Docker containers"; "Artifact Registry" (a GREY dashed label that
appears in the cloud box first) → "ECR · 3 repositories"; a GREY dashed "Pulumi (L20)" under
"Deploy" → "Ansible playbooks".
SAY: The slides speak Google Cloud; we follow the AWS repository, as in lecture 15. Now the same map in AWS words. The Kubernetes cluster becomes one E C 2 server running Docker containers. The image registry becomes E C R, with three repositories. Pulumi becomes Ansible playbooks.

SHOW: LECTURE (held). Three more transforms: a GREY dashed "service-account key" chip on the
Actions box → the two WHITE glyphs "IAM access key" (badge) + "EC2 key pair" (key); a PINK `/deploy-app`
on the commit arrow → `/run-deploy-app`; a GREY dashed "ingress" at the cloud's door → a TEAL
"nginx container".
SAY: The service account key becomes two secrets: an IAM access key and an E C 2 key pair. The keyword becomes slash run deploy app, and the ingress becomes one nginx container at the front door.

SHOW: LECTURE (held). The four ML boxes and "Vertex AI" fade to GREY dashed, with one label over
them: "not in this repo · the AWS ML pipeline was L15"; the "Model Deploy → Backend API" arrow goes
dashed, with a GREY chip "a fixed model file, not a pipeline".
SAY: There's no Kubernetes and no Pulumi here: one server, set up by Ansible, and no machine learning lane.

SHOW: LECTURE 23 · 5–6. The map shrinks to the top. Slide 6's five cards in a row (our drawings, no
icons), each gets a mark on its phrase: "data pipeline jobs" GREY dashed ✗ "L15"; "model training &
deployment" GREY dashed ✗ "L15"; "frontend deployment" GREEN ✓; "backend deployment" GREEN ✓ — one
bracket over these two: "always together · one keyword"; "building & pushing containers" GREEN ✓
"three app images".
SAY: The lecture lists five things to automate. For this repo: pipeline jobs and model training, no, those were lecture 15. Frontend and backend deployment, yes, always together. Building and pushing containers, yes: three app images.

SHOW: LECTURE 23 · 17–18. The cards clear. A TEAL crate `cheese-app-deployment` with a GREEN chip
"src/deployment/"; on the left a GREY laptop hand reaches it ("part 1 · you"); on the right a BLUE
runner box reaches it ("part 2 · GitHub's runner").
SAY: The lecture's plan: we already have a deployment container, so let GitHub Actions run it. Here it's called cheese app deployment.

SHOW: LECTURE (held). Over the crate, a GREY dashed chip "invoke CLI in the deployment container"
transforms into two PURPLE lines: "part 1: `ansible-playbook …` typed at its prompt" and "part 2:
`bash -c "… ansible-playbook …"`". Then the crate shrinks; two GREY captions write on: "Part 1 ·
deploy by hand" and "Part 2 · a commit presses the button". Fade; empty frame.
SAY: The slides say: invoke the command line in that container. Here, that means ansible playbook commands. In part 1 you type them; in part 2, they arrive as one long command.

---

## S03 · A policy, a user and two keys — `s03_console.py` · `ConsoleSetup`

SHOW: TRACKER A 1 · extra. Terminal `laptop`, prompt `student@laptop:~$`, types `git ls-remote
https://github.com/dlops-io/cheese-app-aws.git` (extra, `type_time=0.6`) → TERM(laptop/01: 2–3),
each 40-character id cut to `5950118…`; the terminal clears; `git clone
https://github.com/dlops-io/cheese-app-aws.git` (extra, `type_time=0.6`) → TERM(laptop/02: 2); the
terminal clears; `ls -a cheese-app-aws cheese-app-aws/src cheese-app-aws/src/deployment` (extra,
`type_time=0.6`) → TERM(laptop/04: 12–20), line 17 `deployment` YELLOW. One command per sentence.
SAY: These first commands are extra; the README has no clone step. One branch, unchanged since we pinned it, and inside src, the deployment folder.

SHOW: TRACKER A 1. The terminal shrinks away. README(7–13): the heading, then lines 9–13 inside a GREY
dashed box with the chip "inside a comment · renders empty". A small GREY chip appears: "check:
Bedrock › Model access · us-east-1 · the API asks for Claude 3 / 3.5 Sonnet and Titan embeddings
(api-service/api/utils)", and under it a GREY dashed chip "model IDs from 2024 · may be retired:
not checked".
SAY: The list of APIs to enable sits inside a comment; on AWS there's nothing to switch on. One check: the API calls Bedrock models in U S East 1, chosen in 2024, so check your account can still use them.

SHOW: TRACKER A 2. CODE(README.md: 22–33): line 29 `sts:GetCallerIdentity` YELLOW, lines 30–33
`ecr:` actions PURPLE; Transform to CODE(README.md: 34–44): lines 34–38 PURPLE, line 40
`"Resource": "*"` ORANGE.
SAY: Step 2, in the IAM console: create a policy from this JSON. It allows one identity check and nine E C R actions, to log in, push and pull, on any resource.

SHOW: TRACKER A 2. `▶ your turn`. The panel shrinks left; CONSOLE("IAM › Policies › Create policy";
"JSON: (pasted)", "Name: CheeseAppECRPolicy"). A 3-row laptop strip types `sed -n '23,43p'
cheese-app-aws/README.md | python3 -m json.tool` (extra) → TERM(laptop/10: 2, …, 22); a GREEN ✓
on the strip. A RED dashed chip slides onto the panel: "no ecr:CreateRepository → S07".
SAY: Name it cheese app E C R policy, and pause to create it; an extra check shows the JSON parses. It can't create a repository, so you'll make three by hand later.

SHOW: TRACKER A 3. `▶ your turn`. CONSOLE("IAM › Users › Create user"; "User name:
deployment-ac215-user", "Attach policies directly"): three ORANGE chips drop onto the user,
`AmazonS3FullAccess`, `AmazonEC2FullAccess`, `AmazonBedrockFullAccess`, then a GREEN chip
`CheeseAppECRPolicy` (README 48–50).
SAY: Step 3: create a user, deployment AC215 user. It gets three policies AWS manages: full access to S3, E C 2 and Bedrock. And your own E C R policy.

SHOW: TRACKER A 4. `▶ your turn`. CONSOLE("IAM › deployment-ac215-user › Create access key"; "Use
case: Third Party Service", "Access key: <aws-access-key-id>", "[Download .csv file]"). **V3
`KeyJourney` begins**: the WHITE badge glyph pops out of the download button into a GREY folder
`~/secrets/` as a CSV row `<aws-access-key-id>,<aws-secret-access-key>`. Then a laptop strip types
`ls ~; ls -l ~/secrets` → TERM(laptop/12: 2–3, 6): `cheese-app-aws` and `secrets` side by side;
the CSV's name on line 6 (`deployment-ac215-user_accessKeys.csv`) YELLOW, GREY chip "keep AWS's file
name · docker-shell.sh:10 expects it".
SAY: Step 4: create an access key for a third party service, and download the C S V file. Save it in a secrets folder beside your clone, not inside it, so it can never be committed.

SHOW: TRACKER A 5. `▶ your turn`. CONSOLE("EC2 › Key Pairs › Create key pair"; "Name:
cheese-app-ac215-key-pair", "[Download .pem]"). The WHITE key glyph drops into `~/secrets/`
beside the badge; the strip's TERM(laptop/12: 5) line (the `.pem`) turns YELLOW, with a GREY chip
"a throwaway key stands in here".
SAY: Step 5: create an E C 2 key pair, and save its pem file there too. The badge talks to the AWS API; the key opens the S S H door of your server.

SHOW: TRACKER A 5 · extra. Terminal types `cd cheese-app-aws && grep -rn
'cheese-app-ac215-key-pair\|ac215_2024' README.md src/deployment .github` (extra) →
TERM(laptop/13: 2, 5–8, …), wrap; `cheese-app-ac215-key-pair` (line 2) ORANGE, every `ac215_2024`
YELLOW. An `erratum` chip: "three names, one key pair → name yours ac215_2024 (or change
inventory.yml:16 and the key paths)".
SAY: An extra check shows a small gap. The README names the key pair cheese app AC215 key pair. The code expects AC215 underscore 2024, in three files. Easiest fix: use that name, so the file is AC215 underscore 2024 dot pem.

SHOW: TRACKER A 5 · extra. Terminal types `chmod 400 ~/secrets/cheese-app-ac215-key-pair.pem && ls
-l ~/secrets` (extra) → TERM(laptop/14: 2–4); `-r--------` GREEN; a GREY chip on the file name "our
stand-in kept the README's name · yours: ac215_2024.pem". Fade; empty frame.
SAY: Extra: change mode 400 on the pem file. S S H refuses a private key that others can open.

---

## S04 · Ansible in one picture — `s04_inventory.py` · `AnsibleInOnePicture`

SHOW: TRACKER A 6. Two cards side by side: a GREY dashed card "Pulumi · L20: describe the
infrastructure you want"; a PURPLE card "Ansible: an ordered list of tasks · machines from an
inventory". Under the Ansible card, a small GREEN chip "many modules: state: present" next to a GREY
chip "this repo: plenty of `shell` too".
SAY: Step 6, deployment setup, brings a new tool: Ansible. Pulumi, in lecture 20, described the infrastructure you want. Ansible runs an ordered list of tasks against the machines in an inventory. Many of its modules describe a state; this repo also runs plenty of shell commands.

SHOW: The cards leave. **V4 `AnsibleMachine`**: left, the inventory as a GREEN tree `all` (a small
variables card) → `appserver` → one leaf `<EXTERNAL_IP>`. Right, two playbook cards, one play each
(GREY chip "here: one play per playbook"): `deploy-create-instance.yml` with the play "Create App
Application Machine · hosts: localhost" and tiles `ec2_group`, `ec2_vol`, `ec2_instance`;
`deploy-provision-instance.yml` with the play "Configure app server instance · hosts: appserver" and
tiles `apt`, `mount`, `shell`. On "localhost", PURPLE sparks fire inside a small TEAL toolbox; on
"appserver", sparks ride a PINK SSH arrow into a BLUE server box, chip "ubuntu + your key".
SAY: A playbook is a list of plays. Each play names its hosts and holds tasks, and each task calls one module. The hosts line decides where tasks run: localhost means inside your toolbox; appserver means on the server, over S S H.

SHOW: TRACKER A 6. V4's GREEN inventory tree stays left; its `all` variables card **expands** into
CODE(src/deployment/inventory.yml: 1–11) (Transform), and the `appserver` leaf stays pinned beside
the panel (V4's playbook cards leave). Line 3 `ansible_user: ubuntu` YELLOW; line 4 (the CI key path)
and line 7 (the commented local one) each get a YELLOW bookmark "remember · S08"; lines 9–11 PINK,
three small PINK arrows from them to a TEAL label "toolbox environment".
SAY: Here is that inventory, as one file. Ansible logs in as the user ubuntu. Line 4 points at the key for GitHub Actions; line 7, commented out, at the key on your laptop. Lines 9 to 11 take your keys from the environment: nothing to type.

SHOW: TRACKER A 6. Transform to CODE(src/deployment/inventory.yml: 14–25): lines 14 (region), 15
(`t2.large`), 16 (`aws_keypair_name: "ac215_2024"  ## Change this`, YELLOW), 17 (the machine
image, chip "per region" and a GREY chip "if step 6 says InvalidAMIID: pick a current Ubuntu image in
EC2 › AMIs, us-east-1"), 21–22 (the 50 GB disk), 24 (`<nextauth-secret>`, YELLOW).
SAY: Then the machine: the region, U S East 1, and a T 2 large instance. The key pair name, marked change this. An Ubuntu machine image for that region, and the disk names and sizes.

SHOW: TRACKER A 6. README(67–72) card left of the panel 14–25. Bullets 2 and 4 fly as YELLOW ticks
onto lines 14–23 and 16; bullets 1 and 3 fly onto two small GREY chips above the panel, "line 3 ✓
(seen)" and "lines 9–11 ✓ (seen)". `▶ your turn` beside line 24, with a 1-row laptop strip showing,
written out, not executed (tag `extra`): `openssl rand -base64 32`. Then a Transform shows
CODE(src/deployment/inventory.yml: 27–30) with line 30 `<EXTERNAL_IP>:` GREY dashed, chip "after
S08"; the panel's lines 27–30 then Transform back into the tree's `appserver` leaf `<EXTERNAL_IP>`,
GREY dashed.
SAY: The README's four bullets point at exactly these lines. Change two now: the key pair name, unless yours already matches, and line 24, the Next auth secret, to a random value of your own. The host on line 30 comes later.

SHOW: Under the tree, a row of five counters `ok · changed · unreachable · failed · skipped`;
`failed` and `unreachable` get GREEN zeros on "zero". A declarative tile fires once (YELLOW
"changed"), fires again and turns GREEN "ok"; a `shell` tile fires both times. Fade; empty frame.
SAY: Every run ends with a recap; success means failed and unreachable stay at zero. A declarative task run twice reports ok the second time.

---

## S05 · Starting the toolbox: three surprises — `s05_toolbox.py` · `StartToolbox`

Persistent group for the whole scene (counts as one of the three visual groups in every block; the
separate erratum chips of S05 merge into its rows): a small GREEN "your edits" checklist, bottom
right, at most 4 rows visible. It gains a row on each fix: "docker-shell.sh:10 · ../../../secrets"
(block 4); "run with bash" (block 6); "Dockerfile · drop Helm (33–34, 36)" (block 9);
"docker-shell.sh:26 · three ../" and "docker-shell.sh:17 · your account ID" (block 11). It returns in
S14 (its Dockerfile row Transforms into the commit checklist's Helm tick) and S15 (the three edited
files of `laptop/49`).

SHOW: TRACKER B 1. `▶ your turn`. Terminal `laptop`, prompt `student@laptop:~/cheese-app-aws$`,
types `cd src/deployment` → (no output); the prompt becomes `P_LAPTOP`; then types `pwd; ls -a` →
TERM(laptop/20: 2, 8, 12–16, 19–21); `docker-shell.sh` and `inventory.yml` YELLOW. A GREY chip, once:
"your prompt shows your own user".
SAY: Step 1: go to the deployment folder. Here are the playbooks, the inventory and docker shell dot S H.

SHOW: TRACKER B 1. CODE(src/deployment/docker-shell.sh: 9–21): line 10 `CSV_FILE=…` YELLOW; line 13
(the `<<<` here-string) PINK; line 17 `export AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID"` ORANGE with chip
"hard-coded · masked".
SAY: Open the script. It splits the second line of your C S V into two variables. Line 17 hard codes the account ID of the author, a placeholder here.

SHOW: TRACKER B 2 · extra. Terminal types `bash docker-shell.sh` (extra) → TERM(laptop/21: 2) RED.
After line 2 prints, the terminal shrinks to a 3-row strip; the middle takes a small path ladder: `deployment` → `src` → `cheese-app-aws` → `student` → `/home`, one
GREY step per `../`; the fourth lands RED: "/home/secrets ✗".
SAY: Run it as cloned, and it stops: credentials file not found. Four dot dots from the deployment folder end at slash home, one level too far.

SHOW: TRACKER B 2. `▶ your turn`. README(76) card; the terminal types `sed -i
's|^CSV_FILE=.*|CSV_FILE="../../../secrets/deployment-ac215-user_accessKeys.csv"|' docker-shell.sh &&
sed -n '9,11p' docker-shell.sh && ls -l ../../../secrets/deployment-ac215-user_accessKeys.csv` →
TERM(laptop/22: 3, 5); line 3 GREEN. A GREY chip "sed is our editor · use yours".
SAY: Step 2 is that fix: three levels up, with sed or your editor. Now the file is found.

SHOW: TRACKER B 3. Terminal types `sh docker-shell.sh` → TERM(laptop/23: 2) RED.
SAY: Step 3: S H, docker shell dot S H, exactly as written. Surprise 1, on this Ubuntu laptop: a syntax error on line 13, redirection unexpected.

SHOW: TRACKER B 3 · extra. Terminal types `ls -l /bin/sh; head -1 docker-shell.sh` (extra) →
TERM(laptop/24: 2–3): `dash` RED, `#!/bin/bash` GREEN. The terminal shrinks to a 3-row strip; then a
small inset of line 13 with `<<<` circled RED, label "here-string". An `erratum` row joins the edits
checklist: "macOS: sh = bash ✓ · Linux: bash docker-shell.sh".
SAY: Extra: on Ubuntu, S H is dash, which has no here string. And typing S H skips the first line, which asks for bash. On a Mac the README line works; on Linux, use bash instead.

SHOW: TRACKER B 3 · extra. Terminal types `bash docker-shell.sh` (extra) →
TERM(laptop/25: 3, …, 20, 28, 34): line 20 `ERROR [ 9/15]` RED, line 28 `curl: (60) SSL certificate
problem` RED, line 34 `gpg: no valid OpenPGP data found.` RED. Chip "at the time of recording".
SAY: Surprise 2, at the time of recording, on our machine: the build stops at step 9 of 15. Curl can't verify the Helm download site, so no signing key arrives.

SHOW: TRACKER B 3 · extra. TERM(laptop/25: …, 49) continues: line 49 `Unable to find image
'cheese-app-deployment:latest' locally` RED. After line 49 prints, the terminal shrinks to a 3-row
strip showing lines 20, 34, 49; CODE(src/deployment/docker-shell.sh: 3–4) above it: `#set -e`
YELLOW, with a GREY chip "commented out".
SAY: And the script doesn't stop: set dash e is commented out, so it runs an image that was never built. Check the build output, not just the last line.

SHOW: TRACKER B 3 · extra. CODE(src/deployment/Dockerfile: 31–37): lines 33–34 struck through RED,
the word `helm` on line 36 struck RED. The panel shrinks into a GREY chip "Dockerfile 33–34, 36" at
the top right before the terminal grows back; then the terminal types the extra `sed … && git diff
Dockerfile` (line 1 of `27`, folded) → TERM(laptop/27: 10–11, 13–14) (RED `-`, GREEN `+`); then
`bash docker-shell.sh` → TERM(laptop/28: 3, 33): "FINISHED" GREEN.
SAY: Our machine didn't trust that certificate's root. Your laptop may. No playbook uses Helm, so delete these two lines and the word helm, and the toolbox builds.

SHOW: TRACKER B 3 · extra. The prompt changes to `root@b0ed47a6a572:/app#` (from `28`: 35), with a
GREY chip on the id: "changes every start". TBX(laptop/28: 36–38): an empty listing, boxed RED
"empty" (lines 36–37 are the listing, not the cryptography pair: no crop here). The terminal
shrinks to a 3-row strip; then CODE(src/deployment/docker-shell.sh: 26) slides in: `SECRETS_DIR=$(pwd)/../../../../secrets/`
with the four `../` RED. An `erratum` chip: "README: not mentioned".
SAY: Surprise 3: inside the toolbox, slash secrets is empty. Line 26 has the same four dot dots, so Docker mounted an empty folder. The prompt ID changes on every start.

SHOW: TRACKER B 3 · extra. The terminal types `exit` at the toolbox prompt (GREY chip "exit the
toolbox"); the prompt returns to `P_LAPTOP`. Terminal types line 1 of `30` (extra, folded) →
TERM(laptop/30: 2–4): line 3 ORANGE (`YOUR_ACCOUNT_ID`), line 4 GREEN. A GREY chip: "your account
ID: `aws sts get-caller-identity`".
SAY: So fix line 26 like line 10, and put your own account ID on line 17. AWS S T S get caller identity shows it, once your keys work.

SHOW: TRACKER B 3. `▶ your turn`. Terminal types `bash docker-shell.sh` → the build is one GREY line
"… FINISHED" (from `31`: 3); TBX(laptop/31: 36, 39–42, 44–45): the `.pem` and the CSV GREEN, a GREY
chip on line 39 "yours: ac215_2024.pem", four `AWS_` names (values never shown; line 43 cropped). V3: the badge glyph slides into a small TEAL
crate icon beside the terminal. Fade; empty frame.
SAY: Run bash docker shell dot S H again: both files are there, yours named AC215 underscore 2024 dot pem, and four AWS variables are set. Pause, and get to this prompt yourself.

---

## S06 · Inside the toolbox: whose Docker? — `s06_inside.py` · `InsideToolbox`

SHOW: TRACKER B 3 · extra. **V5 `SiblingContainers`**: a GREY laptop frame with a Docker engine (an
image shelf holding `cheese-app-deployment`). CODE(src/deployment/docker-shell.sh: 35–42) beside
it; on each mount line a PINK line connects the TEAL toolbox to the laptop: line 36 (the socket,
thick PINK), 37 (`/app`), 38 (`/secrets`), 40–42 (the three app folders). Line 39 stays GREY, not
animated. Transform to CODE(src/deployment/docker-shell.sh: 43–48): the badge enters the crate as
four `-e` lines (V3).
SAY: How was the toolbox started? Line 36 mounts the Docker socket. Then the deployment folder at slash app, your secrets, and the three app folders. Lines 43 to 46 hand in your keys as environment variables.

SHOW: The panel leaves; V5 stays (laptop, shelf, crate, mounts). A PURPLE `docker build` spark
appears inside the crate and hovers there, with no direction (it travels only in the answer block).
SAY: A question. Inside the toolbox, Ansible runs docker build for the frontend. Whose disk does the image land on: the toolbox's, or your laptop's?
PONDER(8 s, "Inside the toolbox, Ansible runs docker build\nfor the frontend.\nWhose disk does the image land on:\nthe toolbox's, or your laptop's?")

SHOW: The card leaves. Inside the crate a PURPLE `docker build` spark travels **down the PINK socket
line** into the laptop's engine; a TEAL image box lands on the laptop's shelf beside the toolbox,
GREEN chip "sibling". Then a RED dashed `docker system prune -a` spark goes the same way and sweeps
a broom over the whole shelf (a ghost, then undone).
SAY: Your laptop's. No Docker engine runs inside the toolbox; the Docker module of Ansible talks through the socket to your laptop's Docker. So the image lands beside the toolbox, not inside it. That's also why a prune, run from inside, would sweep your laptop.

SHOW: TRACKER B 3 · extra. The picture leaves. TBX(laptop/32: 36, 40, 50–53, 55, 57, 59) printed as
one block under a GREY heading row "versions · extra" (the six commands are not typed; the
cryptography pair at 38–39 is cropped by text). Then the four tool names lift out as PURPLE chips,
one per phrase: `aws-cli 2.39.6`, `Docker CLI 28.1.1`, `kubectl v1.28.15`, `ansible 6.7.0` (the last
turns RED); chip "at the time of recording"; line 59 `helm-exit:1` GREY.
SAY: Extra checks: the AWS command line, Docker, kubectl and Ansible are there, but not the Ansible the Dockerfile asked for.

SHOW: CODE(src/deployment/Dockerfile: 37) alone. The line's text splits on the `>`: `pip install …
ansible` slides left (PURPLE, to pip), and `>` turns into a PINK arrow carrying `=9.0.0` into a file
glyph in a GREY `/` folder. Then a 3-row strip types `33`'s two commands and prints TBX(laptop/33:
36–37) (`'=9.0.0'` RED; these are the listing, not the cryptography pair) and 39–40, 42 (wrap, cut
after `ansible-core-2.13.13`). The file glyph and the strip's RED name pulse together. An `erratum`
chip: "for later: quote it, \"ansible>=9.0.0\", on a newer base image · leave it for this lecture:
deploy-provision-instance.yml:57 (`warn:`) needs this old Ansible".
SAY: Without quotes, the greater than sign in that pip install is a shell redirect. So the root folder holds a file whose name starts with an equals sign: pip wrote its log there, and installed Ansible 6, on an old Python. Quoting fixes it, but leave it for now: the provision playbook relies on this old Ansible.

SHOW: TBX(laptop/40: 38–41) shown alone, small (the only time): the `[WARNING]` line and the
`[DEPRECATION WARNING]` block, plus the cropped cryptography pair restored in GREY for this block
only (`40`: 36–37). Both fold into one GREY chip "warnings · hidden from here on".
SAY: That explains the warnings: the old Python, a collection that doesn't support this Ansible, and an old module name. We hide them from now on.

SHOW: TBX(laptop/34: 37) RED (`InvalidClientTokenId … The security token included in the request is
invalid.`), typed `aws sts get-caller-identity`.
SAY: AWS S T S get caller identity: the security token is invalid. Ours is a placeholder. With your key, this prints your account ID and your user.

SHOW: TBX(laptop/35: 38–41), typed `ansible-inventory -i inventory.yml --graph`: the lines morph into
V4's GREEN tree (`all` → `appserver` → `<EXTERNAL_IP>`). Then TBX(laptop/36: 39, 47, 51, 55, 59)
(typed the loop of `36`: 35, folded): five `playbook: …` lines GREEN. Fade; empty frame.
SAY: The inventory graph shows all, then appserver, then one host. And all five playbooks pass a syntax check. The toolbox is ready.

---

## S07 · Three images, one timestamp — `s07_images.py` · `BuildAndPush`

SHOW: TRACKER B 4. `▶ your turn`. README(81–85) card; CONSOLE("ECR › Private registry ›
Repositories · us-east-1"; three rows `cheese-app-vector-db-cli`, `cheese-app-api-service`,
`cheese-app-frontend-react`, each "Private"). The S03 chip "no ecr:CreateRepository" returns small.
SAY: Step 4: in E C R, in U S East 1, create three empty private repositories: the vector D B tool, the API service and the frontend. Your policy can push to them, but not create them.

SHOW: TRACKER B 5. CODE(src/deployment/deploy-docker-images.yml: 2–13): line 2 `hosts: localhost`
YELLOW; line 9 (the ECR login) PURPLE; line 12 `(date +%Y%m%d%H%M%S)` GREEN; line 13 `register: tag`
GREEN. **V6 `TimestampTrail`, first half**: a GREEN tag card `YYYYmmddHHMMSS` is stamped out of line
12 and hangs from line 13 (after the next Transform, a PINK thread runs from `register: tag` to
`tag.stdout` on line 23).
SAY: The first playbook runs on localhost, inside the toolbox. Task 1 logs Docker in to E C R. Task 2 stamps a tag from the date, down to the second, and registers it, so later tasks can use it.

SHOW: TRACKER B 5. Transform to CODE(src/deployment/deploy-docker-images.yml: 18–24): line 21 `path:
/frontend-react` PINK with a small socket glyph "mounted in S06"; Transform to CODE(…: 25–30): line
29 `push: yes`. V6: the tag clips onto a TEAL image `…/cheese-app-frontend-react:<tag>`, which flies
to a BLUE ECR shelf (registry `YOUR_ACCOUNT_ID.dkr.ecr.us-east-1.amazonaws.com`); two more images
follow (`-api-service`, `-vector-db-cli`). The panel leaves. CODE(src/deployment/deploy-docker-images.yml:
57–58) appears small under the ECR shelf; line 58 `echo {{ tag.stdout}} > .docker-tag` GREEN; the
card's copy drops from it into a GREEN file `.docker-tag`.
SAY: Then it builds the frontend from slash frontend react, the folder the script mounted, names the image with that tag, and pushes it. The API and the vector D B tool follow. Last, it saves the tag in a file: dot docker tag.

SHOW: TRACKER B 5. `▶ your turn`. Toolbox terminal types `ansible-playbook deploy-docker-images.yml
-i inventory.yml` (README 89, verbatim).
SAY: Step 5: ansible playbook, deploy docker images, dash i, inventory dot yaml. Pause and run it.

SHOW: TBX(laptop/40: 43, 45, 46 msg, 49): line 43 `PLAY [Build docker images and push them to
ECR]`; line 46 shows `fatal: [localhost]: FAILED! =>` and the two stderr lines, `aws: [ERROR]: An
error occurred (UnrecognizedClientException) when calling the GetAuthorizationToken operation: The
security token included in the request is invalid.` and `Error: Cannot perform an interactive login
from a non TTY device`, both RED; line 49 becomes V4's counters with `failed=1` RED.
SAY: Our first real error: at the E C R login, the security token is invalid. The second line follows from the first: docker login received an empty password. The recap says failed, 1.

SHOW: TRACKER B 5 · extra. Back at `P_LAPTOP` (GREY chip "second laptop terminal · the toolbox stays
open · /app is this folder, edits show up inside at once"), terminal types `docker images` (extra) →
TERM(laptop/41: 2–4).
SAY: Extra: no image was built. The laptop still holds only the toolbox and its base.

SHOW: TRACKER B 5. No terminal. The 11 task names from TERM(laptop/37: 63–73) as V4 tiles in one play
card "hosts: localhost"; they light GREEN one by one, schematic (no output panel, GREY caption
"what success looks like"). The `.docker-tag` file shows the committed `20241121211313` struck
GREY ("the author's last deploy") and a GREEN `<your tag>` replacing it. A recap row with GREEN
`failed=0`.
SAY: With your keys, all 11 tasks run: three images built on your laptop and pushed, and your tag written to dot docker tag. Look for failed, zero, in the recap.

SHOW: TRACKER B 5 · extra. Terminal types `docker system prune -a` (extra) → TERM(laptop/67: 2–8):
the WARNING list, then `Are you sure you want to continue? [y/N]` with nothing after it (file line 8
is printed without its ` [exit 0]` suffix: docker printed no newline; assert it in the scene). Then
the terminal shrinks to a 3-row strip (lines 2, 8) and the ECR shelf returns above it, now holding a
second set of three images, with a GOLD `cost_tag("ECR storage · every tag you push")`. Fade; empty
frame.
SAY: The last task is docker system prune, dash a. Without dash f, it asks, gets no answer, and removes nothing. Every push stores three more images in E C R, and nothing deletes old tags.

---

## S08 · Create a server, then provision it — `s08_server.py` · `CreateAndProvision`

SHOW: TRACKER B 6. **V4 + V7**: the create play card "Create App Application Machine · hosts:
localhost" with its nine tiles from TERM(laptop/37: 43–51); the tiles fire one by one as PINK API
calls from the TEAL toolbox to the BLUE "AWS · us-east-1" box, which builds **V7 `VmLayout`**: a
security-group wall with three doors 22, 80, 443 and an ORANGE `0.0.0.0/0` label; a GREEN 50 GB disk
("us-east-1a"); a BLUE EC2 box `t2.large` with the WHITE key glyph on its door and two GREEN disks of
its own inside ("100 GB root", "100 GB · /dev/sdf", chip "deleted with the instance"); a PINK SSH
arrow waits (GREY chip "times out after 120 s? your network may block port 22"); the 50 GB disk
moves toward the box and stops at a GREY dashed outline, chip "untested: the attach reuses /dev/sdf,
and the disk is pinned to us-east-1a · watch that task". The tile "Remove EBS volume" stays GREY
dashed ("when: absent").
SAY: Step 6 creates the server from localhost, through the AWS API. First, a security group with ports 22, 80 and 443 open to anyone, and a 50 gigabyte disk. Then a T 2 large instance with your key pair and two 100 gigabyte disks of its own. Last, it tries to attach the 50 gigabyte disk.

SHOW: TRACKER B 6. Three GOLD tags appear beside the EC2 box: `cost_tag("EC2 instance · by the
hour, until terminated")`, `cost_tag("EBS disks · per GB-month")`, `cost_tag("public IPv4 address
· by the hour")`; a GOLD meter starts ticking.
SAY: From here, the meter runs: the instance by the hour until you terminate it, its disks, and its public I P address.

SHOW: TRACKER B 6. `▶ your turn`. Toolbox terminal types `ansible-playbook deploy-create-instance.yml
-i inventory.yml --extra-vars cluster_state=present` (README 94, folded) → TBX(laptop/42: 39, 41–42,
44, 45 wrap): line 42 `ok: [localhost]` GREEN; line 45 RED, cut after `AWS was not able to validate
the provided access credentials`; line 49's counters: `ok=1`, `failed=1` RED. After the RED line, a
GREY dashed chip (tag `not tested`): "on a real account, 'Attach EBS volume' may fail: /dev/sdf is
taken, or another zone · the server still works · the 50 GB volume stays detached and billed (S15)".
SAY: Pause and run step 6. Gathering facts works, then it fails: AWS was not able to validate the provided access credentials. With real keys, watch the untested attach task. If it fails, the server still works; delete that spare disk when you clean up.

SHOW: TRACKER B 6. README(92) card: the heading "Create Compute Instance (VM) Server in GCP" with
"in GCP" underlined and an `erratum` chip "it's an EC2 instance · carried over from the GCP README".
SAY: A kind note: the heading says G C P; it came over from the Google Cloud README.

SHOW: TRACKER B 7. `▶ your turn`. CONSOLE("EC2 › Instances"; "cheese-app-demo · running · t2.large",
"Public IPv4 address: <EXTERNAL_IP>"). The console's address chip flies down into a 3-row laptop strip
at `P_LAPTOP` (GREY chip "second laptop terminal · the toolbox stays open · /app is this folder,
edits show up inside at once") that types line 1 of `43` (sed is our editor) and prints
TERM(laptop/43: 2–5): line 5 `EXTERNAL_IP:` YELLOW, GREY chip "placeholder: we have no server".
SAY: Step 7: copy the public I P address of your instance from the E C 2 console into the inventory, under appserver hosts. Ours is a placeholder name.

SHOW: TRACKER B 9 (shown early). `▶ your turn`. README(107–111) card with an `erratum` chip "README
order: do step 9 before step 8"; the laptop strip (same second terminal) types line 1 of `45` (extra
editor command, folded) → TERM(laptop/45: 3, 5–6): line 3 (the CI key, now commented) GREY, line 6
(the local key) GREEN; `/secrets/ac215_2024.pem` YELLOW, GREY chip "the file in ~/secrets must be
named ac215_2024.pem". The S04 bookmarks "remember · S08" flash.
SAY: A small slip: the key switch of step 9 is needed now. Pause, comment out line 4 and turn on line 7. It reads slash secrets, AC215 underscore 2024 dot pem: that exact name. The key on line 4 isn't in your toolbox.

SHOW: TRACKER B 8. `▶ your turn`. Toolbox terminal types `ansible-playbook
deploy-provision-instance.yml -i inventory.yml` (README 102) → TBX(laptop/44: 39, 41, 42 msg, 45):
`fatal: [EXTERNAL_IP]: UNREACHABLE! =>` `Failed to connect to the host via ssh: ssh: Could not resolve
hostname external_ip: Name or service not known` RED; counters `unreachable=1` RED (captured before
the key switch: the hostname fails before any key is read). V7's PINK SSH arrow from the toolbox
ends at a RED "?" where the server would be. On the last sentence, a GREY chip on the arrow:
`ansible.cfg:2  host_key_checking = False` with "trade-off".
SAY: Step 8: pause and run ansible playbook, deploy provision instance. Unreachable: could not resolve hostname external I P, our placeholder. On yours, Ansible logs in as ubuntu, with your key. Host key checking is off, so a new server is trusted blindly: a trade-off.

SHOW: TRACKER B 8. No terminal. The play card "Configure app server instance · hosts: appserver":
the 38 task names from TERM(laptop/37: 81–118) collapse into four group labels that stack as one
GREEN column left of V7 and light in turn, GREY caption "what success looks like": "Docker CE" (an
engine appears inside the EC2 box), "format + mount `/mnt/disk-1`" (the instance's second disk,
`/dev/xvdf`, docks to a folder), "AWS CLI v2", "aws configure". On "AWS configure",
CODE(src/deployment/deploy-provision-instance.yml: 288–292) replaces the column for 2 s, then leaves;
V3's badge glyph lands on the server, a small counter "badge · copy 1 on the server". Fade; empty
frame.
SAY: On a real server, 38 tasks install Docker, then format the second disk and mount it at slash M N T slash disk 1. They install the AWS command line and run AWS configure with your keys: your badge now has a copy on the server.

---

## S09 · Five containers on one network — `s09_containers.py` · `SetupContainers`

SHOW: TRACKER B 9 (✓, GREY chip "done before step 8"). README(107–111) card, small, with TERM(laptop/45:
3, 6) as a 2-row strip under it: line 3 GREY, line 6 GREEN. The card shrinks into the tracker caption.
SAY: Step 9: the key switch, done before step 8.

SHOW: TRACKER B 10 · extra. A small V7 server with only the `vector-db` container (ORANGE chip
`latest`) and a small TEAL loader beside it. CODE(src/deployment/deploy-setup-containers.yml:
148–152): line 151 `image: "chromadb/chroma:latest"` ORANGE. The panel shrinks to a chip; a laptop
strip (GREY chip "second laptop terminal") types line 1 of `60` (extra, folded) → TERM(laptop/60: 28,
29 wrap): `"1.0.0"` (chip "at the time of recording"), the `HTTP 410` RED; V7's `latest` chip flips
to `1.0.0` and the loader's PINK request comes back RED `410`.
SAY: Two extras before you run step 10. The playbook starts Chroma at the tag latest: at the time of recording, version 1, which answers the old API with status 410, gone.

SHOW: TRACKER B 10 · extra. The strip types line 1 of `61` (extra) → TERM(laptop/61: 40, 41): `HTTP
200` GREEN. The chip on V7 swaps to GREEN `0.5.18`, the request returns GREEN `200`. An `erratum`
chip, as an action: "edit line 151 → chromadb/chroma:0.5.18 before you run step 10 · as
docker-compose.yml:25"; it joins S05's "your edits" checklist as a row.
SAY: The clients and the repo's compose file pin an older version, which answers 200. So change line 151 to that version first.

SHOW: TRACKER B 10 · extra. CODE(src/deployment/deploy-setup-containers.yml: 164–166): `-it` on
line 165 RED. The panel shrinks to a chip; the strip types `docker run --rm -it nginx:stable true`
(extra) → TERM(laptop/66: 2) RED. A GREY chip "untested under Ansible".
SAY: Second, the loader uses docker run, dash I T, which Docker refuses without a terminal. We couldn't test whether Ansible provides one; if that task fails, drop dash I T.

SHOW: TRACKER B 10. `▶ your turn`. Toolbox terminal types `ansible-playbook
deploy-setup-containers.yml -i inventory.yml` (README 116) → TBX(laptop/46: 42 msg, 45): the same
`UNREACHABLE!` RED.
SAY: Step 10: ansible playbook, deploy setup containers. Pause and run it. Ours is unreachable, for the same reason; here is what it does on a real server.

SHOW: TRACKER B 10. V7's server, GREY caption "what success looks like". First,
CODE(src/deployment/deploy-setup-containers.yml: 36–44) appears small, alone with V7, on "a file only
root can open", then leaves: a file `/srv/secrets/aws-credentials` with chip `0600` and V3's badge
(counter "badge · copy 2 on the server · + the API container's environment"). Then, one per phrase:
a PINK line `appnetwork` across the box; two folders `persistent` and `chromadb` on the disk; a PINK
login arrow to ECR.
SAY: It writes your keys to a file only root can open, a second copy on the server, and hands them to the API container as environment variables. It creates a Docker network, appnetwork, and two folders on the data disk, and logs in to E C R.

SHOW: TRACKER B 10. CODE(src/deployment/deploy-setup-containers.yml: 101–104) → Transform to
CODE(…: 106–114): a small fork drawing: `DOCKER_TAG` set in the toolbox's environment → that tag
(PINK); not set → `cat .docker-tag` (GREEN file). A GREY chip: "laptop run: the file · CI run: the
extra variable wins (S14)".
SAY: Then it picks the tag: a docker tag variable in the toolbox's environment wins; otherwise, the dot docker tag file. From your laptop, it's the file.

SHOW: TRACKER B 10. V7 fills, one per phrase: three TEAL images pulled from ECR; TEAL containers
`frontend :3000`, `vector-db :8000` (GREEN chip `0.5.18 · your pin`); a small TEAL loader appears, a
PINK arrow fills the vector-db's disk folder, and the loader vanishes (`--rm`); `api-service :9000`
with a GOLD `cost_tag("Bedrock · per token")`. The three ports are painted on the inside of the
wall; the wall shows no hole for them.
SAY: It pulls the three images and starts the frontend on port 3000 and Chroma on 8000. A throwaway container fills the vector database, then the API starts on 9000. The security group keeps those ports shut.

SHOW: TRACKER B 11. README(120–132) card, all six commands verbatim; "from the GCP console"
underlined, `erratum` chip: "on AWS: `ssh -i <your key>.pem ubuntu@<EXTERNAL_IP>` or EC2 Instance
Connect". `▶ your turn` beside `sudo docker container ls`.
SAY: Step 11: look around on the server. Where the README says G C P console, use S S H as ubuntu with your key, or E C 2 Instance Connect. Then list containers, follow logs, or open a shell.

SHOW: TRACKER B 11 · extra. Laptop terminal (tag `extra · stand-in on the laptop`) types line 1 of
`63` → TERM(laptop/63: 2–5): the IMAGE column YELLOW; then line 1 of `64` → TERM(laptop/64: 4–6), the
client address `172.19.0.1` and the timestamps cropped to `…` (Docker's private bridge, never an IP on screen).
A GREY chip: "nginx: after the next step". Fade; empty frame.
SAY: Here they are on our laptop, as a stand-in. The image column carries the tag: check it there. The nginx lines work only after the next step.

---

## S10 · One front door: nginx — `s10_webserver.py` · `FrontDoor`

SHOW: TRACKER B 12. LECTURE 23 · 37. Slide 37's routing redrawn: "Browser" → "Ingress Controller",
which forks: `/` → "Frontend · 3000"; `/api/` → "API · 9000" → `vector-db:8000`. Then the ingress box
**transforms** into a TEAL `nginx` container standing in V7's server at doors 80/443; the two
branches re-attach to the `frontend` and `api-service` containers.
SAY: The lecture's routing: one address, slash to the frontend, slash API slash to the API. Here the same shape sits on one machine, and the ingress becomes an nginx container.

SHOW: TRACKER B 12. README(136–137) card with chip "already in the repo". CODE(src/deployment/
nginx-conf/nginx/nginx.conf: 25–27) (`listen 80` YELLOW) → Transform to CODE(…: 34–37) (`location
^~ /api/` PINK, line 37 `proxy_pass http://api-service:9000/;`) → Transform to CODE(…: 46–48)
(`location /` → `frontend:3000` PINK).
SAY: Step 12 says create nginx dot conf; it's already in the repo. It listens on port 80. Paths that start with slash API slash go to the API service on 9000; everything else goes to the frontend on 3000.

SHOW: Line 37 stays on screen; a browser request chip `/api/newsletters` hovers at nginx's door. On
"very end", a thin GREY box (no color) frames the end of line 37.
SAY: Predict: the browser asks nginx for slash API slash newsletters. Which path does the API service receive? Look at the very end of line 37.
PONDER(8 s, "The browser asks nginx for /api/newsletters.\nWhich path does api-service receive?")

SHOW: The card leaves. On line 37 the trailing `/` after `9000` turns YELLOW; V7: the request enters,
nginx **cuts** `/api` off (the piece falls away RED), `/newsletters` travels on to `api-service`.
Laptop strip, tag `extra · stand-in on the laptop`, types line 1 of `62` (folded) →
TERM(laptop/62: 34, 36, 38): `api-service received /newsletters` GREEN, `frontend received /`,
`HTTP 301` YELLOW.
SAY: Slash newsletters. The trailing slash after port 9000 replaces the matched prefix. Our stand-ins on the laptop confirm it, and slash API without its last slash gets a redirect.

SHOW: TRACKER B 12. CODE(src/frontend-react/.env.production: 2): `NEXT_PUBLIC_BASE_API_URL=/api`
GREEN; a PINK arrow from the browser to the same host `/api/…`.
SAY: The frontend calls slash API on the same host, and the API mounts its routes without the prefix: they fit.

SHOW: TRACKER B 13. `▶ your turn`. Toolbox terminal types `ansible-playbook
deploy-setup-webserver.yml -i inventory.yml` (README 141) → TBX(laptop/47: 42 msg, 45): RED. Then
the four task names from TERM(laptop/37: 158–161) as tiles over V7, GREY caption "what success looks
like".
SAY: Step 13: pause and run ansible playbook, deploy setup webserver. Unreachable again. On a real server, it copies the config, starts nginx on ports 80 and 443, and restarts it.

SHOW: TRACKER B 14. `▶ your turn` on the browser. A schematic browser (tag `illustration`) with the
address `http://<EXTERNAL_IP>/` and a GREY page outline "Formaggio" (no screenshot); a GREY chip
"blank or 502? step 11: container ls, logs api-service". V7 beside it: door 80 GREEN; door 443 open
and forwarded to nginx, with a GREY dashed "nginx serves nothing here · no HTTPS"; doors 3000, 8000,
9000 drawn shut.
SAY: Step 14: open your server's address in a browser. Only port 80 does the work. Port 443 is open and forwarded to nginx, but nginx serves nothing there: no HTTPS yet.

SHOW: The browser shrinks; a GREY caption "Part 1 · about a dozen commands · five playbooks · by
hand". A PINK commit ribbon `/run-deploy-app` drifts in from the right edge and stops. Fade; empty
frame.
SAY: That's part 1: about a dozen commands and five playbooks, by hand. Next, a commit message does the redeploy.

---

## S11 · CI, CD, and who presses release — `s11_cicd.py` · `WhoPressesRelease`

SHOW: No tracker. LECTURE 23 · 7. **V8 `ReleaseLoop`** drawn: bottom left "Developers"; a PINK arrow
"Commits" up into `Codebase` → `Build` → `Test` (bracket "CI") → `Deploy` → `Monitor` (bracket
"CD"); a commit dot runs along the boxes; dashed PINK lines drop from each box after Codebase into
a GREY bar "Notifications" beside "Developers".
SAY: Part 2 starts with the lecture's loop. Developers commit to the codebase. It is built and tested: that's the C I half. Then it is deployed and monitored: the C D half. Every stage sends notifications back.

SHOW: LECTURE 23 · 36. The same loop: a `Release` box slides in between `Test` and `Deploy`, and
gets its own dashed notification line.
SAY: The version in the review adds one box between test and deploy: release, the moment a tested version is handed over for deployment.

SHOW: LECTURE 23 · 8–10. The loop shrinks to the top. Slide 10's idea redrawn: three GREY developer
icons → a "Shared Repository" box → a pipe "Automated Quality Checks" with three tiles, one per
phrase ("automated tests", "coding standards · style, consistency", "static analysis · defects,
vulnerabilities, without running the code") → "Functional Codebase" (GREEN ✓). A GREY chip: "L09 ·
L21".
SAY: Continuous integration runs scripts on every push. Many developers share one repository, and every change passes automated tests, coding standards, and static analysis, which finds defects without running code. You built this in lectures 9 and 21.

SHOW: LECTURE 23 · 11–12. Slide 12's toggle redrawn: one conveyor of code cards; at its end, first a
RED "RELEASE" button with a GREY hand above it ("continuous delivery"); on "by itself", the button
swaps for a ring "auto" ("continuous deployment"), and the cards stream through.
SAY: Then delivery and deployment. Continuous delivery keeps every change ready to release, but a person presses the button. Continuous deployment ships every passing change by itself.

SHOW: LECTURE 23 · 13–15. Two small GREY cards: "CI for ML: + data quality, + model performance ·
expensive"; "CD for ML: release only within a tolerance · challenge: data drift"; a GREY dashed chip "this repo:
an app, not a model · L15 was the model".
SAY: For machine learning, C I also checks data quality and model performance, which makes it expensive. And C D releases a model only when its metrics are within a tolerance, and must cope with data drift. This repo deploys an app, not a model; lecture 15 was the model.

SHOW: The cards leave; V8 grows back. **This repo's version**: `Codebase`, `Build`, `Release` (chip
"tagged images land in ECR") and `Deploy` light BLUE; `Test` turns a GREY dashed outline "L21";
`Monitor` gets the chip "the run's color + your own check". CODE(.github/workflows/ci_cd_aws.yml:
1–2): line 1 `name: Continuous Integration and Continuous Deployment` with an `erratum` chip "runs no
test: the CD half".
SAY: Now this repo on the loop. Build, release and deploy light up; release is when the tagged images land in E C R. Test stays dashed: the workflow is named continuous integration and continuous deployment, but runs no test. It's the C D half. And monitor is the color of the run, plus your own check of the site.

SHOW: LECTURE 23 · 16–18. A row of six blank GREY service tiles (no logos), one tile turning PURPLE
"GitHub Actions"; then a BLUE runner box reaches the TEAL crate `cheese-app-deployment` with two
arrows "build it", "run it". A GREY caption: "thin YAML · thick container". Fade; empty frame.
SAY: The lecture names several C I C D services; the course uses GitHub Actions, to build the deployment container and run it, on every commit that asks. The workflow file stays thin; the deploy logic is the playbooks you just ran.

---

## S12 · Two sieves on one commit message — `s12_trigger.py` · `TwoSieves`

SHOW: TRACKER C 1. CODE(.github/workflows/ci_cd_aws.yml: 3–9): lines 3–5 (`on: push: branches: [
"main" ]`) PINK; line 9 `if: contains(github.event.head_commit.message, '/run-')` YELLOW. **V1
`KeywordSieves`**: the first sieve forms from line 9 (PURPLE rim, label `/run-`).
SAY: The workflow file, C I C D AWS dot yaml, isn't in the README, so every step on this tracker is extra. It starts on every push to main, but the job runs only if the commit message contains slash run dash.

SHOW: TRACKER C 1. Transform to CODE(.github/workflows/ci_cd_aws.yml: 99–100): line 100 `if:
contains(github.event.head_commit.message, '/run-deploy-app')` YELLOW; the second, smaller sieve
forms under the first, over only the last step's box.
SAY: And the last step, run deployment container, has its own condition on the same message: it must contain slash run deploy app.

SHOW: The panel leaves; V1 full size: a push arrow to `main` drops PINK ribbons onto the two
stacked sieves. Ribbon 1 `update readme`: caught by nothing, it slides off the first sieve; a GREY
chip "job skipped · nothing runs".
SAY: Two sieves, one sentence. The message update readme has no slash run dash, so the job is skipped and nothing runs.

SHOW: Ribbon 2 `fix typo /run-tests` hovers above the sieves.
SAY: Your turn. You push fix typo, slash run tests, to main. Nothing, build and push only, or a full deploy?
PONDER(8 s, "You push 'fix typo /run-tests' to main.\nNothing, build-and-push only,\nor a full deploy?")

SHOW: The card leaves. Ribbon 2 passes the first sieve (GREEN flash), the job box lights, three TEAL
images reach a BLUE ECR shelf with a GOLD `cost_tag("three new images in ECR per /run- push")`;
then the ribbon stops on the second sieve (RED flash); the BLUE server keeps its GREEN chip "old
tag".
SAY: Build and push only. It passes the first sieve, so the runner builds three new images and pushes them to E C R, where they cost storage. It stops at the second sieve, so the server keeps the old tag.

SHOW: Ribbon 3 `/run-deploy-app` passes both sieves (two GREEN flashes); the server's three TEAL
containers blink out and back in.
SAY: Slash run deploy app passes both sieves: new images, and the containers on the server are recreated.

SHOW: Ribbon 4, the history's `\run-deploy-app` (`laptop/50`: 5, small, GREY chip "from the opening"):
the backslash glows; the text `/run-` is searched and not found; the ribbon bounces off the first
sieve, RED. The S01 question card returns for a moment and gets a GREEN ✓.
SAY: And the commit from the opening? Its slash is a backslash. The text slash run dash isn't in it, so it bounces off the first sieve. That's the one character.

SHOW: LECTURE 23 · 20. Slide 20's text redrawn as a GREY card: "workflow file in .github/workflows",
"keyword in the commit message: `/deploy-app`"; the keyword transforms into `/run-deploy-app` with a
GREY chip "the Google Cloud repo's keyword"; under it three lines `git add .`, `git commit -m "your
message /run-deploy-app"`, `git push` (GREY, chip "the slide's three commands, with a dot and this
repo's keyword · typed in S14"; the slide's bare `git add` adds nothing).
SAY: The tutorial slide says the same: a workflow file in dot github, workflows, and a keyword in the commit message. Its keyword, slash deploy app, belongs to the Google Cloud repo. Here it's slash run deploy app.

SHOW: LECTURE off. Two GREY chips under the sieves, one per sentence: "head_commit = the last commit
of the push" (three small ribbons arrive as one push; only the last is fed to the sieves) and
"contains() ignores case" (`/RUN-DEPLOY-APP` passes GREEN). Fade; empty frame.
SAY: Head commit means the last commit of a push, so three commits are judged by the last message only. And the match ignores case.

---

## S13 · Secrets and the runner — `s13_runner.py` · `RunnerSecrets`

SHOW: TRACKER C 2 · extra. `▶ your turn`. CONSOLE("GitHub › New repository"; "Name: cheese-app-aws",
"Private"), tag `illustration`. Then a laptop terminal (prompt `student@laptop:~/cheese-app-aws$`)
shows two lines written out, not executed (as S14's git lines; tag `extra`): `git remote set-url
origin https://github.com/<your-user>/cheese-app-aws.git`, `git push -u origin main`. A GREY chip "a
fork works too · then Actions › enable workflows"; a GREY chip "its last message is 'cleanup': no
/run-, nothing runs" (`laptop/03`).
SAY: Part 2 needs your own GitHub repository. Pause, create an empty private one, point origin at it, and push main. Its last message has no slash run dash, so nothing runs yet.

SHOW: TRACKER C 2. `▶ your turn`. CONSOLE("GitHub › your repository › Settings › Secrets and
variables › Actions"; four rows `AWS_ACCESS_KEY_ID ***`, `AWS_SECRET_ACCESS_KEY ***`,
`AWS_ACCOUNT_ID ***`, `AWS_SSH_KEY ***`). An `erratum` chip: "not in the README · names from
ci_cd_aws.yml:21–22, 33, 81, 102–108".
SAY: First, give GitHub your secrets: in your repository, settings, secrets and variables, actions. Add four: the access key ID, the secret key, your account ID, and AWS S S H key, the whole pem file. The names come from the workflow.

SHOW: TRACKER C 2. **V3**: the badge and the key copy themselves from `~/secrets/` into a BLUE vault
"GitHub · repository secrets"; the counter beside the badge reads "badge · copy 3, on GitHub"; the key
glyph gets its own small counter "key · copy 2"; a small GOLD `cost_tag("Actions minutes · private
repos")` sits on the vault's runner shelf.
SAY: Your badge has a third copy now, in a vault on GitHub, and your key a second. Every copy is one more place to protect.

SHOW: TRACKER C 3. CODE(.github/workflows/ci_cd_aws.yml: 18–23): line 19 `uses:
aws-actions/configure-aws-credentials@v4` PURPLE, lines 21–22 `secrets.…` PINK → Transform to
CODE(…: 25–33): line 27 `aws sts get-caller-identity`, line 28 `aws s3 ls`, line 33 the ECR login
with `secrets.AWS_ACCOUNT_ID` PINK. A BLUE runner box "fresh Ubuntu machine" appears.
SAY: The runner is a fresh Ubuntu machine. An action from AWS sets up its credentials from two secrets. Then it checks who it is, lists S3, and logs Docker in to your E C R registry.

SHOW: TRACKER C 4. CODE(.github/workflows/ci_cd_aws.yml: 41–44): `docker build -t
cheese-app-deployment -f Dockerfile .` TEAL; a GREY chip "the committed Dockerfile → commit the Helm
fix (S05)" and a GREY dashed chip "same certificate error on GitHub's runner? not tested".
SAY: Then it builds the same toolbox, from the committed Dockerfile. So the Helm fix from part 1 belongs in your commit. We didn't test whether runners hit the same certificate error.

SHOW: TRACKER C 4 · extra. CODE(.github/workflows/ci_cd_aws.yml: 46–50): line 48 `date` GREEN, line
50 `>> $GITHUB_ENV` PINK. Laptop strip with the heading row "ci_cd_aws.yml · lines 47–50 · run by
hand" (tags `extra`, `the workflow's own commands, run by hand`) → TERM(laptop/51: 5):
`DOCKER_TAG=20261108011909` GREEN; V6's tag card is stamped again.
SAY: Next, a fresh tag from the date, written to dot docker tag and to a file GitHub keeps between steps. Run by hand, it gives a timestamp.

SHOW: TRACKER C 4. CODE(.github/workflows/ci_cd_aws.yml: 52–58): lines 56–58 (`docker build`,
`docker tag …:${{ env.DOCKER_TAG }}`, `docker push`) TEAL; a GREY chip "lines 60–70: the same for
vector-db-cli and api-service · not built here".
SAY: Then plain docker build, docker tag and docker push for the frontend, and the same for the other two images. In C I, the runner builds the app images, not the playbook.

SHOW: TRACKER C 4. **V5 on a BLUE runner**: the same TEAL crate and the same thick PINK socket line;
the mounts change on their phrase: `/deployment` (GREEN), `/root/.ssh` (PINK), and the three app
folders vanish GREY dashed ("the runner built them already").
SAY: So the toolbox only deploys. Compared with your laptop: same toolbox, same socket. But the deployment folder sits at slash deployment, the keys at slash root slash dot S S H, and no app folders.

SHOW: TRACKER C 5. CODE(.github/workflows/ci_cd_aws.yml: 72–81) → Transform to CODE(…: 83–90): line
81 (`secrets.AWS_SSH_KEY` → `~/.ssh/ac215_2024.pem`) PINK, lines 84–85 `chmod 600`, lines 88–90
(copied into `src/deployment/secrets/`). Laptop strip heading "ci_cd_aws.yml · lines 73–97 · run by
hand" → TERM(laptop/52: 15, 19–21, 25–26). The panel leaves; then V3: the key glyph lands in
`/root/.ssh` of the crate, with the GREEN chip "on the runner only · never committed". Fade; empty
frame.
SAY: Last, the S S H key. The step writes an S S H config, and your key as AC215 underscore 2024 dot pem, with mode 600. It copies both into the deployment folder, on the runner only, never committed.

---

## S14 · Follow one tag to the server — `s14_deploy.py` · `FollowTheTag`

SHOW: TRACKER C 6. CODE(.github/workflows/ci_cd_aws.yml: 113–123): line 114 (the socket) PINK, lines
115–116 (`/deployment`, `/root/.ssh`) GREEN/PINK, lines 117–121 (`-e` …, line 121 `DOCKER_TAG`
YELLOW).
SAY: The deploy step runs the toolbox on the runner, with the socket, two folders, and five environment variables, docker tag among them.

SHOW: TRACKER C 6. Transform to CODE(.github/workflows/ci_cd_aws.yml: 123–131), folded: each `&&`
link becomes a chain bead that lights in turn: `cd /deployment` → permissions → `ls` → ECR login → `deploy-setup-
containers.yml … docker_tag=$DOCKER_TAG` (YELLOW) → `deploy-setup-webserver.yml`.
SAY: Inside, one long command: fix permissions, log in to E C R, run deploy setup containers with the new tag, then deploy setup webserver. Each link runs only if the one before succeeded.

SHOW: TRACKER C 6 · extra. Laptop terminal with the heading row "ci_cd_aws.yml · lines 110–131 · run
by hand" (tags `extra`, `the workflow's own commands, run by hand`) → TERM(laptop/53: 22–27, 29–30):
`Deploying with tag: 20261108011909` GREEN, the `/root/.ssh` listing (`drwx------`, `-rw-------`),
then the two RED lines. After TERM(53) prints, the terminal shrinks to a 3-row strip (lines 22,
29–30); the chain returns above it, the ECR bead RED and the two playbook beads GREY dashed ("never
ran").
SAY: Run by hand, as an extra, it prints the tag and lists the key, then stops at the E C R login with our placeholder key. Neither playbook runs.

SHOW: **V6 `TimestampTrail`, second half**: the GREEN tag card is stamped on the runner by `date`,
rides `DOCKER_TAG` into the TEAL toolbox, then `--extra-vars … docker_tag=` (line 130, YELLOW) into a
PURPLE Ansible glyph; the S09 fork appears small, GREY, with chip "same value · the extra variable
wins over set_fact"; three PINK pulls from ECR to V7's server at that tag.
SAY: Follow one tag. The date stamps it on the runner. It reaches Ansible as an extra variable, which beats anything the playbook sets, so the server pulls the three images at that tag.

SHOW: Each TEAL container on V7's server **is recreated**: the old one blinks out, a short empty gap
(a GREY dashed outline, chip "short gap"), the new one blinks in with the new tag.
SAY: Then each container is recreated: the old one stops, the new one starts, with a short gap between.

SHOW: LECTURE 23 · 18–19. Beside V7, a GREY dashed inset of L22's rolling update: new pods come up
before old ones go; caption "L22 · the slides' K8s deploy". Under both: "this repo: one machine ·
swap, not roll".
SAY: The slides deploy to a Kubernetes cluster, where, as in lecture 22, a rolling update starts new pods before the old ones go. One machine can only swap; it doesn't roll.

SHOW: TRACKER C 7. `▶ your turn`. S05's "your edits" checklist returns and becomes a YELLOW commit
checklist, one tick per sentence: "inventory.yml:30 · your server's IP" (chip "CI deploys to the
committed address"); "inventory.yml:4 on · line 7 commented again (undo step 9)"; "Dockerfile · the
Helm fix" (S05's Dockerfile row Transforms into it) and "deploy-setup-containers.yml:151 · Chroma
pinned". Then a RED chip: "git add . = every modified file · docker-shell.sh:17 (account ID),
inventory.yml:24 (NEXTAUTH secret)".
SAY: Commit four things. Your server address on line 30: C I deploys whatever is committed. Step 9 undone: line 4 on, line 7 off. The Helm fix. The Chroma pin. Git add dot also commits your account ID and Next auth secret, so keep the repository private.

SHOW: TRACKER C 7. A laptop terminal (prompt `student@laptop:~/cheese-app-aws$`) shows three lines
written out, not executed (GREY chip "the slide's three commands, with a dot and this repo's
keyword"): `git add .` (GREY chip "a public repo publishes line 24's secret · keep it private"),
`git commit -m "your message /run-deploy-app"`, `git push`; the three lines light YELLOW one per
phrase. Then a schematic Actions run page (tag `illustration`): job "Explore-GitHub-Actions" with its
step names from the file (no log text), ticking GREEN top to bottom in about 4 s.
SAY: Then the slide's three commands, with this repo's keyword: git add dot, git commit with slash run deploy app in the message, and git push. Pause, and push.

SHOW: TRACKER C 7. V8's `Monitor` box lights with two chips, one per clause: "green run = every step
that ran exited 0" and "reload the site · `sudo docker container ls` → the IMAGE column shows the new tag".
SAY: A green run means every step that ran exited with zero, not that the app works. Reload your site, and find the new tag in the server's image column.

SHOW: LECTURE 23 · 11–12. V8's toggle from S11 returns small as two unlabeled ends side by side: the
RELEASE button (hand above it) and the "auto" ring. Between them, a PINK ribbon `/run-deploy-app`
hovers, attached to neither. No "delivery"/"deployment" labels.
SAY: In the lecture's words: is typing slash run deploy app continuous delivery, or continuous deployment? What would make it the other?
PONDER(10 s, "By the lecture's definitions,\nis typing /run-deploy-app\ncontinuous delivery or continuous deployment?\nWhat would make it the other?")

SHOW: LECTURE (held). The card leaves. The ribbon drops into the hand on the RELEASE button; the label
"continuous delivery" writes on. Then the MS5 version: V8's `Test` box lights with chip "L21", the keyword chip fades, and the button becomes the
"auto" ring with the label "every merge to main · Milestone 5". Fade; empty frame.
SAY: Delivery. A person decides each release by typing the keyword, and nothing is tested first. Deploy every merge to main, behind the tests from lecture 21, and it becomes continuous deployment. That is Milestone 5.

---

## S15 · The delete that deletes nothing — `s15_teardown.py` · `Teardown`

SHOW: TRACKER B 15. README(147) card. V4's create play card with its first three tiles, each showing
its `when:` line or a GREY "no when" chip: "Create security group · `when: cluster_state ==
"present"`" (line 24), "Create EBS volume · `when: cluster_state == "present"`" (line 37), "Create
EC2 instance" (no `when:` line). On the first tile, a GREEN `register: security_group` chip (line 23),
with a PINK thread from it to the third tile's `security_group.group_id` (line 45), plain, no hint.
SAY: Back to the README, for its last step: delete. It runs the same playbook with cluster state equals absent. Look at the when lines. Which of these three tasks run?
PONDER(8 s, "cluster_state=absent.\nWhich of these three tasks run?")

SHOW: TRACKER B 15. `▶ your turn`. The card leaves. Toolbox terminal types `ansible-playbook
deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent` (README 147, folded) →
TBX(laptop/48: 44–45, 47–48, 50, 51 msg, 54): `skipping` twice GREY; line 51 cut to `The task
includes an option with an undefined variable. The error was: 'dict object' has no attribute
'group_id'` RED; counters `ok=1 … failed=1 skipped=2`.
SAY: Run it exactly as written. Security group, skipping. E B S volume, skipping. Then the instance task has no when line, and fails: no attribute group ID. That is before any AWS call.

SHOW: **V4**: the create play card's tiles: the two `when:` tiles grey out, dashed; the "Create EC2
instance" tile has no `when:` and trips RED on a missing `security_group.group_id` link. Then
CODE(src/deployment/deploy-create-instance.yml: 94–100): `id: "{{ ebs_volume.volume_id }}"` RED
dashed ("set only by a create run"); a GREY chip "no task terminates the instance".
SAY: The skipped task never set the security group, so the instance task trips over it. Even past that, the removal needs a volume ID that only a create run registers, and no task terminates the instance. So clean up by hand.

SHOW: LECTURE 23 · 15. A clean-up card (tag `illustration`, GOLD frame, `cost_tag` per line), lines
ticking GREEN as said: "EC2 › Instances: terminate cheese-app-demo"; "EC2 › Volumes: delete
every cheese-app-demo volume left, attached or not (cheese-app-demo-disk outlives the instance)"; "EC2 › Security Groups: app_security_group ·
Key Pairs: yours". A GREY chip on the frame: "lecture: cost is a CD challenge".
SAY: In the E C 2 console, terminate the instance, then delete the 50 gigabyte volume, which outlives it, the security group and your key pair. Cost is one of the lecture's challenges for C D, and this server bills until you do this.

SHOW: The card continues (LECTURE off): "ECR: delete the three repositories"; "IAM: deactivate +
delete the access key · the user and CheeseAppECRPolicy if made only for this"; "GitHub: delete the
four repository secrets".
SAY: In E C R, delete the three repositories. In IAM, deactivate and delete the access key, and the user and the policy if you made them only for this. On GitHub, delete the four secrets.

SHOW: Last card line: "Locally: `docker image rm cheese-app-deployment` (2.52 GB, `laptop/29`)".
Laptop strip types `cd /home/student/cheese-app-aws && git status --short` (extra) →
TERM(laptop/49: 2–4) (S05's "your edits" checklist slides in beside it and collapses into these
three files), with a GREY chip "keep, or `git restore`" and a GREY chip "yours also: deploy-setup-containers.yml
(the Chroma pin), .docker-tag (after a real step 5)". Fade; empty frame.
SAY: On your laptop, remove the toolbox image, two and a half gigabytes, and keep or restore your edited files.

---

## S16 · The course on one server, and recap — `s16_review.py` · `CourseReview`

SHOW: No tracker. LECTURE 23 · 21–37. **V7** at full size as the review board: the BLUE EC2 server
(wall, five containers, disk) and the GREY laptop beside it with the TEAL toolbox; above, BLUE
GitHub with its runner, and ECR.
SAY: The lecture ends with a review of the course, on the server you deployed.

SHOW: LECTURE (held). Each group's badges fade before the next group's arrive; at most 4 badges on V7
at once. Group 1, a YELLOW badge per phrase: "L01–L02 · venvs, VMs, containers" on the
EC2 box, its containers and a small pipenv chip inside one image; "L03 · containers share a bucket"
on a GREY dashed bucket at the edge; "L03–L04 · the senior developer builds and pushes by hand" on
the laptop, which slides a PINK arrow over to the runner: "now the runner's job".
SAY: Virtual machines and containers, lectures 1 and 2. A shared bucket, lecture 3. And the images the senior developer pushed by hand: the runner pushes them now.

SHOW: LECTURE (held). Group 2: slide 25's three bands as thin overlays: "execution" over `frontend`
and `api-service`, "state" over ECR and the disk; then "L11 · labeling" (GREY dashed, off the
server); "L05 · RAG" on the loader, `vector-db` and the chat route; "L06–L07 · agents" on the API;
"L08 · fine-tuning, LoRA, distillation" GREY dashed, with an arrow to a BLUE "Bedrock" box: "ready-made
models"; a small TEAL file glyph "cheese classifier · .keras" drops into `api-service`.
SAY: The solution architecture: frontend and API execute; E C R and the disk hold state. Retrieval, lecture 5, is the loader and Chroma; agents, lectures 6 and 7. Labeling and fine tuning aren't here: the API calls ready-made models through Bedrock, plus the cheese classifier trained earlier, as a file.

SHOW: LECTURE (held). Group 3: "L13, L15 · training jobs, model deployment, pipelines" GREY dashed, off
the server: "on AWS: L15's SageMaker pipeline"; "L18 · API + frontend containers" on `api-service`
and `frontend`; "L09, L21 · the CI loop with release" on the runner; "L20, L22 · routing to services"
on nginx.
SAY: Training and pipelines, lectures 13 and 15, sit beside this server. The API and frontend containers, lecture 18. The C I loop, lectures 9 and 21. Routing, lectures 20 and 22: today's nginx.

SHOW: LECTURE off. **V8's MS5 loop** small at the top (Test lit "L21", keyword gone, "every merge to
main"); over V7, **V3's two GREY dashed overlays**: "instance role" (the server's badge copies
vanish, a short-lived token glyph appears) and "GitHub OIDC" (the vault's badges vanish); then two
small GREEN chip "HTTPS on 443".
SAY: Where next? Put the tests from lecture 21 in front, and deploy every merge to main. Replace the copied keys: a role for the server, and O I D C for GitHub. And add HTTPS.

SHOW: LECTURE off. The recap of this lecture: the five set pieces return small, in a row, each
lighting on its phrase. V3's badge and key sit in GREY `~/secrets/`. V5's crate sits with its PINK
socket line to the laptop's shelf. V4 has two play cards, `localhost` sparking inside the crate and
`appserver` riding a PINK SSH arrow. V6's GREEN tag card runs from `date` to a recreated TEAL
container. V1's two sieves pass one `/run-deploy-app` ribbon. A GOLD broom sweeps V7's server last
("by hand"). Fade.
SAY: Once more, the path. Two secrets on your laptop. A toolbox using your laptop's Docker. Plays on localhost, or on the server over S S H. One tag, from the date command to a recreated container. One sentence that presses release. And clean up by hand.

SHOW: A YELLOW "Test yourself" card, question 1 of 5 (answers in `exercises.md`): "Name the two
secrets, what each opens, and three places the access key ends up after one deploy. What would an
instance role and GitHub OIDC remove?" A small V3 badge-and-key beside it; on "three places", the
badge copies blink in their places.
SAY: Test yourself. One: name the two secrets, what each opens, and three places the access key ends up. What would a role and O I D C remove?

SHOW: Question 2 (a small `sh` chip that flips to `dash` on "Ubuntu", and the `=9.0.0` file): "Why does `sh
docker-shell.sh` fail on Ubuntu but work on a Mac, and what did `pip install ansible>=9.0.0`
actually do?"
SAY: Two: why does S H, docker shell dot S H, fail on Ubuntu but work on a Mac? And what did that unquoted pip install actually do?

SHOW: Question 3 (a small V5 crate with its socket line; a spark runs down the socket on "your laptop"): "A `hosts: localhost` play and a `hosts:
appserver` play: where does each task run, and why can the toolbox's `docker build` fill your
laptop's disk?"
SAY: Three: where do the tasks of a localhost play run, and of an appserver play? And why can the toolbox fill the disk of your laptop?

SHOW: Question 4 (a small V6 tag card that slides along a short trail): "Follow one timestamp from `date` to a running container.
Where is it written down, and how does the server choose between `DOCKER_TAG` and `.docker-tag`?"
SAY: Four: follow one timestamp from the date command to a running container. How does the server choose between the variable and the file?

SHOW: Question 5 (V1's two sieves, small; the four ribbons drop and one bounces): "Which of these
deploy: `update readme`, `fix typo /run-tests`, `/RUN-DEPLOY-APP`, `\run-deploy-app`? In the lecture's words, is this pipeline
continuous delivery or continuous deployment?" A GREY chip "answers: exercises.md · every command:
the study guide". Fade out; empty frame.
SAY: Five: which of these deploy? Update readme, fix typo slash run tests, slash run deploy app in capitals, and backslash run deploy app. And is this pipeline delivery or deployment? Answers are in the exercises.
