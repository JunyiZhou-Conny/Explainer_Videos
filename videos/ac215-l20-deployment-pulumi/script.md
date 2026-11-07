# AC215 · Lecture 20 — Deployment: the cheese app on one VM, by hand and then as code — narration script & visual plan (v2, 2026-11-06: four reviews merged, see `build/review_merge_log.md`)

Audience: an AC215 student who has done L1–L18: a cloud VM, SSH, `apt` and deleting the VM (L1–L2);
images, containers, `-p HOST:CONTAINER`, bind mounts, `docker-shell.sh`, Docker networks and
container names (L2–L4); service accounts and JSON keys in `secrets/` next to the repo (L10, L15);
Cloud Run, where Google ran the box for them (L14); the cheese app's API, frontend, vector DB and
loader running locally (L18). They have seen Lecture 20 ("Deployment: Pulumi", one deck of 30
slides). New to them: a reverse proxy and its `location` blocks, prefix stripping, a firewall that
opens ports by network tag, infrastructure as code, Pulumi's program → desired state → diff →
provider calls, projects and stacks, state backends, `preview` / `up` / `--refresh` / `-y` /
`destroy`, OS Login and the `sa_…` user, Docker over SSH, `StackReference`, `remote.Command` and
idempotent scripts. They watch with `dlops-io/cheese-app-v3` cloned next to their `secrets/` folder,
Docker running, a GCP project with billing and a Docker Hub account, pausing to run each step.
**Real money is involved**: a VM, two disks, an external IP, registry storage, a state bucket (GOLD
tags; a teardown at the end of each part).

Goal (BRIEF "Audience and goal"): after the video they can draw the lecture's target picture and
explain every arrow (browser → port 80 → nginx → frontend:3000 or api-service:9000 → vector-db:8000)
and why only nginx faces the internet; deploy the app by hand (Docker Hub, Docker on a VM, folders,
network, five containers with a one-shot loader, nginx in front), read the container list, logs and
`exec`, and delete the VM; say which single character strips `/api-service` and why a stopped
frontend takes the whole site down; explain Pulumi's loop and what `preview`, `up`, `--stack`,
`--refresh`, `-y` and `destroy` do (and what `-y` skips); set up the toolbox (four APIs, two service
accounts and what each key may do, the two one-line Dockerfile fixes, `sh docker-shell.sh`, tool
checks, `gcloud auth list`); set up SSH for Pulumi (OS Login, a passphrase-less key, the upload, the
`sa_…` user in the stack config); run both Pulumi projects in order, map their output onto slide
19's six steps and the file behind each, recognise each real error; tear down, and know what
survives `pulumi destroy`.

Sources of truth: `BRIEF.md` (design, binding), `digest.md` (tutorial digest), `SLIDES.md`
(lecture-slide digest, binding next to the digest: docs/AC215_SERIES.md rule 9), `assets/` (see
`ASSETS.md`). Where the digest or the slides and the captures disagree, the captures win, and the
video says so kindly. **Which README**: `dlops-io/cheese-app-v3` `README.md` @ **`3ecef56`**
(`main`, 2025-11-28, unchanged on the recording day per `laptop/p03`; the course site links `main`),
sections "Deployment to GCP (Manual)" (README:4–222), "Deployment to GCP (Single VM Instance)"
(225–383) and "Delete the Compute Instance / Persistent disk" (387–390). An unmerged staff branch
exists and rewrites the README; it is context for `ASSETS.md` only and is **never named or shown**.
Nothing in a terminal panel is typed by hand: every output line below names its capture file and
line numbers. Captures: 2026-11-05, 22:06–23:42 UTC.

Conventions
- `SAY:` lines are spoken verbatim by the TTS voice (one `voiceover` block each, 1–3 sentences, at
  most about 60 words) and become the subtitles. Plain spoken English: no backticks, no markdown,
  no raw symbols (`/`, `=`, `%`, `&`, `$`, `→`, `_`, `<`, `>`); commands, flags and paths are on
  screen and said in words ("change into src, deployment", "slash api service", "pulumi up, stack
  dev, refresh, dash y", "Control C"). File names are said "nginx dot conf", "service dot py",
  "deployment dot json", "gcp service dot json", "Pulumi dot dev dot yaml", "inventory dot yml";
  `docker-shell.sh` is written as such (lexicon entry exists). Container and network names are said
  in words ("api service", "cheese app vector db", "cheese app network", "app network"). The
  Docker Hub scripts are "the Docker Hub script". `src` is written `src` (said "S R C" as in other
  scripts). Numbers are digits; never a "!" after a digit; no `'s` after a digit; no spoken decimals
  (5.07 GB is "about five gigabytes", 91.9 s "about 92 seconds", versions stay on screen with "at
  the time of recording" and are not spoken; Chroma's `"1.0.0"` is "Chroma version one").
- Every spoken sentence starts with a capital letter or a digit (`explainer.voice.split_sentences`
  splits only there; the same split drives TTS gaps, subtitle cues and the one-to-one Chinese
  alignment). No sentence opens with a lower-case command, tool or file name, and none opens with
  "nginx" (write "The web server …", "The nginx container …"). No `'s` on a word with a lexicon
  entry or candidate (Pulumi, nginx, Chroma, uvicorn, gcloud, kubectl, BuildKit). No bare "a" right
  before a lexicon entry or candidate. No homographs: never "read", "live", "lives", "close",
  "lead", "tear", "minute(s)", "content", "record" ("capture", "sit", "stay", "check", "delete it
  all", "down to the second"). The main clause comes first so the Chinese subtitles keep English
  clause order.
- **README headings, not numbers.** The two README sections have no numbered lists, so the SAY
  names each step by its README heading or action ("Install Docker on VM", "Create folders",
  "Run vector db cli"); the lecture's numbered **steps 1–6** (slide 19) are said as "step 2",
  "step 4", and only ever mean slide 19's steps. The tracker's step numbers are on screen, not
  spoken.
- `SHOW:` lines describe what is on screen during that `SAY:` line, and what moves. Something moves
  about every 4 s except under a ponder timer; at most 3 visual groups at once; every scene ends on
  an empty frame.
- `PONDER(n s, "question")`: after that SAY block, `pause_and_ponder(self, "question", seconds=n)`
  (silent YELLOW timer; the card is removed at the start of the next block). Five in the video,
  BRIEF's table and numbers, Conny's 2026-10-21 density decision: P1 S05, P2 S07, P3 S09, P4 S14,
  P5 S15, all 8 s. The SAY before each card speaks the question; the answer is the next SAY. Nothing
  during the timer shows the answer.
- `TERM(id: lines)`: a terminal beat. `vm/NN` = `assets/terminal/vm/NN-*.txt` (`vm/30b` included);
  `aNN`, `bNN`, `pNN` = `assets/terminal/laptop/<id>-*.txt` (`b02a`, `b02b`, `b02c`, `b02d`,
  `b19-1..3` = `b19-vm-config-set-1..3`, `b41-1..3` = `b41-x-vm-config-set-1..3`, `b35b`, `b36b`);
  `expected/oslogin` = `assets/terminal/expected/oslogin-ssh-keys-add.txt`. The scene types the
  command written just before it in the SHOW line (in backticks, exactly as the README spells it;
  extras exactly as the capture's line 1 spells it, folding with ` \`), then prints the listed
  **file** lines. Line 1 is the `$ …` command: typed, never printed (`b10` and `b14` hold their
  README block's commands on lines 1–3 / 1–2: all typed); `[exit N]` is never printed. Inside the
  list: `…` = print one `…` line; `wrap` = fold long lines; `crop "…"` = print that line only up to
  the quoted text; `→ (no output)` = the prompt simply returns. Blank output lines are dropped.
  Multi-line README commands (`vm/23`, `vm/27`, `vm/30`, `vm/38`, `vm/44`) are typed in full from
  the capture's own lines 1–n (they are byte-identical to the README); `vm/44` (58 lines) is typed
  as a fast scroll in a tall terminal, never read.
- Prompts (constructed; captures hold only the command): the VM `student@cheese-app-vm:~$` (as in
  `vm/00`), title `cheese-app-vm`; the laptop `student@laptop:~$`,
  `student@laptop:~/cheese-app-v3/src/frontend-react$`, `student@laptop:~/cheese-app-v3/src/deployment$`,
  title `laptop`. Inside the toolbox the prompt is `root@<id>:/app#` as printed by `b02d:77` (shown
  once from the file; afterwards the constructed `root@toolbox:/app#` is **not** used: the scene
  reuses the printed string), `…:/secrets#` (S12, between `cd /secrets` and `cd /app`), and
`…:/app/deploy_images#`, `…:/app/deploy_single_vm#` after the
  `cd`s. Container ids are never read aloud. Terminal titles: `cheese-app-vm`, `laptop`,
  `laptop · toolbox`.
- **Masking at load time** (BRIEF "Masking"): every `sa_` + 21-digit number in a capture or a
  README card is replaced by `sa_000000000000000000000` (`b19-2`, `b41-2`, `b42:6`, README:354);
  the README's `ac215-project` stays where a README command prints it and gets the GREY
  `default_tag` "the README's default · change to yours"; `your-gcp-project` is the placeholder of
  `b01`, `b02d`, `b07`. `b02:57-171`'s `[IP: 172.17.0.1 38720]` column is cropped (`crop "404  Not
  Found"`); `vm/02:16` (`WARNING: unable to enable the docker service`) and `b02d:78-79` (the
  capture's own timeout) are never printed; `b14` is cropped after line 7's "or"; `b10:10-22`
  (fingerprint, randomart) are never printed.
- `CODE(path: a–b)`: `code_panel(...)` quoting `assets/source/path` with the real line numbers,
  header `path · lines a–b`; at most 12 lines on screen. Paths are relative to
  `assets/source/` (`src/deployment/…`, `src/frontend-react/…`, `src/api-service/…`). A "README
  card" is a GREY quote of README text, header `README.md · lines a–b` (markdown stripped).
  `src/vector-db/cli.py:75` and `:440` name the instructor: never in a panel's line range (if one
  ever is, it shows `‹instructor›`).
- `EXPECTED(expected/oslogin: lines)`: a GREY-outlined panel quoting those lines, tagged
  `expected · README:306–314` (the README's own output snippet). The only `expected` panel.
- `TRACKER [k] n`: the `ReadmeTracker`, top-left in every walkthrough scene, for README section
  `k` at step n. `TRACKER [k] n · extra` = same step, caption " · extra" while a command the README
  does not have is on screen. Titles are the README's own headings. Step titles ≤ 3 words (BRIEF
  table):
  - [M] "README › Deployment to GCP (Manual)" (README:4–222), 15: 1 Local check · 2 Docker login ·
    3 Push images · 4 Create VM · 5 Install Docker · 6 Make folders · 7 Secret file · 8 Docker
    network · 9 Vector DB · 10 Load vectors · 11 API service · 12 Frontend · 13 nginx.conf · 14 Run
    nginx · 15 Open site.
  - [P] "README › Deployment to GCP (Single VM Instance)" (README:225–389, the destroy heading
    included), 14: 1 Enable APIs · 2 Service accounts · 3 Run toolbox · 4 Check tools · 5 OS Login ·
    6 SSH key · 7 Upload key · 8 Inventory (skip) · 9 Images stack · 10 Images up · 11 VM stack ·
    12 VM up · 13 Check VM · 14 Destroy.
  S01, S08 (tally and questions), S09 and S16 after its destroy block have no tracker; S02's first
  three blocks have none.
- **Six-step strip** (BRIEF, slide 19): a row of six numbered chips "1 Setup · 2 Images · 3 VM ·
  4 Provision · 5 Containers · 6 Web server", each with its file under it (`docker-shell.sh`,
  `deploy_images/`, `create_instance.py`, `provision_instance.py`, `setup_containers.py`,
  `setup_webserver.py`). It opens S10, S13, S14 and S15 (current chip YELLOW, earlier ones ticked
  GREEN), then shrinks away: it is never pinned, so the tracker and `lecture_ref` keep their
  corners. S16 replays it as the recap.
- `(extra)` after a command: not in the README. A small GREY tag `extra` sits beside the typed
  line, and the SAY says "extra" the first time each kind appears. `extra · our spelling` on `p01`
  (the README has no clone command). `extra · not for you` on `b30` (Pulumi's local backend, a
  recording workaround) and `extra · recording only` on `--target` (`b34`, `b35b`). Every panel
  from `b30`–`b46` carries `extra`.
- `▶ your turn`: a YELLOW tag beside the command at a real checkpoint (about one per tracker group);
  the SAY of that block says "pause". The video doesn't wait: the viewer pauses.
- Tags (GREY unless said): `illustration` on every console form, the Docker Hub token page, every
  browser window, the resource graph of a successful `pulumi up` (S15) and every lecture redrawing
  that shows cloud machinery; `expected · README:306–314` (S12); `erratum` on every README or slide
  slip (the SAY says "a small slip" or "a small note", never "erratum"); `at the time of recording`
  beside every version on first show; `default_tag` (see Masking). GOLD `cost_tag()` where a
  billable resource appears: the manual VM and its disk (S04), Artifact Registry storage (S13), the
  Pulumi VM, its two disks and IP (S14), the state bucket (S16 checklist); a GOLD-outlined "disk"
  chip on the 5.07 GB API image (S06). Prices only in S14, as "roughly", never exact on screen.
- `LECTURE 20 · a–b` in a SHOW line: the GREY `lecture_ref(20, "a–b")` tag (`explainer.devops`) sits
  top right ("Lecture 20 · slides a–b"; "slide" for one) **for that SHOW block only**: it fades in
  with the redrawn lecture picture and fades out at the end of the block. `LECTURE (held)` in the
  next block keeps it, only while the same picture stays on screen. A SHOW line without a LECTURE
  mark has no lecture tag. Every lecture picture is our own redrawing in series colours with the
  slide's structure and terms: no slide image, QR code, logo, glitch art, cartoon or screenshot.
  Request arrows run in the request direction (browser → nginx → services → vector DB), the
  opposite of the slides' arrowheads (said once, S02).
- **The sandbox framing** (BRIEF "Running example", load-bearing): said once, in S01 (block 7).
  Afterwards every Google or Docker Hub error is the next line of the lesson, and "yours prints …"
  is said, never shown as output (the one printed exception is `expected/oslogin`). Never imply that
  a push, VM, `pulumi up` or destroy against real resources happened.

Colours (BRIEF "Colours", fixed for the whole video)

| meaning | colour |
| --- | --- |
| the laptop and everything on it: the browser, `secrets/` on the host, the host's Docker daemon, the toolbox's outline ("Your Machine", slide 14) | GREY |
| the cloud: GCP's outline, the VM, the VPC, the persistent disk, Artifact Registry, the GCS state bucket, the Compute Engine APIs, Vertex AI, Docker Hub | BLUE |
| containers and images: `api-service`, `frontend`, `vector-db` / `cheese-app-vector-db`, the loader (dashed), `nginx`, `cheese-app-deployment` (inside its GREY laptop) | TEAL |
| shared or OS-owned: Debian's apt pools (`bullseye-security`), Google's apt repository, the default buildx builder, the `0777` folders on the VM, the VM's system Docker | ORANGE |
| project-owned and pinned: `Pulumi.yaml`, `Pulumi.dev.yaml` and its keys, the state file, timestamped image tags, `cheese-app-network` / `appnetwork` (the app's private LAN), the repo's `nginx.conf` | GREEN |
| tools: Docker / buildx / BuildKit, gcloud, Pulumi and its providers (gcp, docker, docker-build, command), kubectl, uv, `ssh-keygen` | PURPLE |
| errors and "don't": every honest first error, the mangled `log_format`, the README's broken steps, the powerful key where the narrow one belongs | RED |
| your turn, the README tracker, the thing to look at now, the current six-step chip, ponder timers | YELLOW |
| money: the VM, both disks, the external IP, Artifact Registry storage, the state bucket; the "Don't forget to delete" card | GOLD |
| routes and addresses: URLs, ports, `-p` doors, request arrows, firewall gates and network tags, the SSH tunnel, the `/api-service` prefix and its scissors, the `StackReference` pipe | PINK |
| the past and the future: L18's laptop run, L21–L23, slide items the repo does not use (the models bucket, "GCR", NFS) | GREY, dashed |

Keys (V8) are coloured by power: `deployment.json` a RED-rimmed BLUE key, `gcp-service.json` a
GREEN key, `ssh-key-deployment` a PURPLE key.

Running example
- **The VM** is a fresh Debian 12 machine standing in for the console-made VM (`vm/`, hostname
  `cheese-app-vm`, user `student`, Docker 29.9.3 from the README's `get-docker.sh`). Said once, S04
  block 3. A single GREY caption (S04 block 4, not spoken): "on a real VM, systemd starts Docker
  here".
- **The laptop** (`laptop/`, a fresh Docker 29.8.2 engine, buildx 0.37.2, user `student`):
  `cheese-app-v3/` and `secrets/` side by side (`p05`); `secrets/` holds `deployment.json` and
  `gcp-service.json`, well-formed files around throwaway keys for **no account** (never shown as a
  panel; ASSETS capture-only).
- **Pulumi's local backend** (S13–S16): `pulumi login --local` (`b30`) is an `extra · not for you`,
  said plainly once in S13 block 5. Every panel from `b31`–`b46` carries `extra`.
- **Placeholders**: `your-gcp-project` (`b01`, `b02d`, `b07`); the README's `ac215-project` with its
  `default_tag`; `sa_000000000000000000000` (masked); no IP anywhere (browser bars say
  `http://<Your VM IP Address>/` and `http://<instance_ip>/`; curls are to `localhost`).
- **Versions** (on screen with "at the time of recording", not spoken): VM Docker 29.9.3, Chroma
  server 1.0.0, nginx 1.30.6, Next.js 15.0.2, Python 3.12.12 in the loader and API; laptop Docker
  29.8.2, buildx 0.37.2; toolbox Python 3.13.18, uv 0.13.7, gcloud 592.0.0, Pulumi v3.274.0,
  kubectl v1.35.9. Image sizes: API 5.07 GB, chroma 640 MB, frontend 232 MB, nginx 163 MB (`vm/60`);
  toolbox 2.61 GB (`b36b`).

Length and parts: narration target 3,900–4,300 words (`python -m explainer.script`, which counts SAY
words; its minute figure assumes 155 wpm and is ignored). At Kokoro af_heart speed 0.9 (≈174 wpm),
≈24.5 min of narration, ≈31–33 min with typing, the long outputs (`vm/02`, `vm/27`, `a02`, `b02`,
`b35b`), the illustrations and five ponder timers. Per-scene counts and the BRIEF bands are in the
table at the end of this file ("Word count").
Part 1 = S01–S08 (by hand: slides 4–11, the manual README section on the Debian 12 stand-in; ends on
S08's teardown and "Part 2 builds it again, as code"). Part 2 = S09–S16 (as code: slides 12–29;
ends on the last test-yourself card, then an empty frame). The cut is the README's own seam
(README:222 → 227) and the deck's (slide 9).

Notes for scene authors
- Shared code (`scenes/common.py`, started from L18's and L14's): tracker factories `tracker_m`
  and `tracker_p` with the step lists above; prompts `P_VM`, `P_LAPTOP`, `P_FRONTEND`, `P_DEPLOY`
  (the toolbox prompt string is taken from `b02d:77`); tags `your_turn`, `extra_tag` (+ `our
  spelling`, `not for you`, `recording only` variants), `illustration_tag`, `expected_tag(source)`,
  `erratum_tag`, `cost_tag(text)` (GOLD), `default_tag`, `lecture_ref`; `six_steps(current)`;
  `browser_window(url, rows)`; `console_form(fields)`; the masking helper for `sa_…`; set pieces
  `MasterDiagram` (V1, `stage21()` … `stage27()`, `manual=True`), `NamePhoneBook` (V2),
  `ProxyRoute` (V3), `EngineLoop` (V4), `ControlRoom` (V5), `TimestampPipe` (V6), `VmFences` +
  `ProvisionDominoes` (V7), `KeyRing` (V8). Never reuse a scene class name for a helper.
- TERM line numbers are *file* lines (line 1 = the `$` command); `Capture.pick()` indexes the output
  body, so pick index = file line − 1. Assert the picked text for every highlighted line.
- **The 14,356 counter** (S05): `vm/27` never prints the total. The eleven `Finished inserting N
  items` lines (`vm/27:37, 50, 69, 82, 99, 113, 127, 140, 156, 168, 180`: 923 + 714 + 3569 + 926 +
  2623 + 1198 + 1146 + 678 + 2147 + 269 + 163) feed a YELLOW counter beside the terminal; the counter
  is the scene's arithmetic on real lines (a diagram, not a terminal line).
- **BRIEF corrections found while scripting** (captures win):
  - `b35b`: `npm ci` is `#13 … DONE 71.1s` (`b35b:141`), `next build` is `#17 … DONE 54.2s`
    (`b35b:205`), and the push fails at `creating (148s)` (`b35b:226-228`); BRIEF's "DONE 70.3s,
    DONE 42.3s, creating (133s)" do not occur. The 403 is printed in full only at `b35b:260` (the
    Diagnostics block). `b35b:293-297`: `3 unchanged`, `2 errored`, `Duration: 2m31s`.
    `b35b:1` is `pulumi up --stack dev -y --target '…'` (no `--refresh`, flag order as captured):
    typed as captured, tagged `extra · recording only`.
  - `b35b:230-256` is a Python `KeyboardInterrupt` traceback from the language host after the
    failed push: never printed (collapsed into the `…` before `b35b:258`).
  - The API's CNN is downloaded **only when it is missing** (`src/api-service/api/utils/llm_cnn_utils.py:122`
    `if not os.path.exists(best_model_path)`), into `/persistent/experiments`, so on the manual VM
    it lands in `persistent-folder`; BRIEF's "every time it starts" is not said. S06 says "from a
    GitHub release into the persistent folder, not from a bucket".
  - `vm/02:14-15` ("Using systemd to manage Docker service", `+ sh -c systemctl enable …`) are not
    printed either, so the cropped `vm/02:16` leaves no dangling line.
  - `b14` holds two commands (`cd deploy_images`, `pulumi stack init dev`) on lines 1–2; `b18`
    holds only `pulumi stack init dev` (no `cd` capture): S14 types `cd ../deploy_single_vm` with a
    GREY chip "README:349, no output" and no output panel.
  - `p04` is `mkdir -p secrets` (a stand-in for "copy the key into the secrets folder"): shown as
    a GREY chip, not typed, in S10.
  - Slide 7 draws **four** containers (NGINX, API, front end, vector DB); only the loader is
    missing there. S02 says "a fifth" (Conflict 7's "two more do quiet work" applies to slide 8).
  - `docker-shell.sh:13-17` holds `GCP_PROJECT` … `PULUMI_BUCKET`; the empty
    `PULUMI_CONFIG_PASSPHRASE` comes from `Dockerfile:51` (shown in `b07:7`). S11's env strip
    quotes both, each with its own source.
- Lexicon heads-up (script stage; check phonemes with `explainer/voice.py`, phrase keys where another
  video uses the bare word): Pulumi ("PULL-oo-mee"), nginx ("engine-x"), Chroma, uvicorn, gcloud
  ("gee-cloud"), kubectl ("cube-control"), buildx (exists), BuildKit, OS Login, Next.js (exists),
  Formaggio, bookworm, bullseye, Debian, Ubuntu, Gemini, Vertex, ssh keygen ("S S H keygen"),
  "block ID" and "make file system" are plain words (the SAY never says `blkid` or `mkfs`), "S A"
  (the `sa_` user), "N 2 D", "A M D 64", "ARM 64", "src" ("S R C"), `docker-shell.sh` (exists),
  "dlops" ("D L ops"), "multi-arch" ("multi arc"), "heredoc" ("here doc"), "scp" ("S C P"),
  "yml"/"yaml" ("yammel"), `14,356` (no entry needed), "0777" is said "zero seven seven seven".
  Added to `explainer/lexicon.yaml` under `# AC215 L20` (v2): `Pulumi`, `pulumi`, `kubectl`,
  `heredoc`, `Formaggio` (no other video's SAY says them) and the phrase keys `db cli` and
  `inventory dot yml` (bare `cli` and `yml` are in finished videos' SAY).
- Subtitle display for the i18n stage (`en_display`): slash api service → `/api-service`; slash
  status → `/status`; slash docs → `/docs`; slash data → `/data`; chroma chroma → `/chroma/chroma`;
  slash secrets → `/secrets`; slash app → `/app`; mnt disk 1 → `/mnt/disk-1`; nginx dot conf →
  `nginx.conf`; service dot py → `service.py`; deployment dot json → `deployment.json`; gcp service
  dot json → `gcp-service.json`; Pulumi dot dev dot yaml → `Pulumi.dev.yaml`; inventory dot yml →
  `inventory.yml`; cheese app network → `cheese-app-network`; app network → `appnetwork`; cheese app
  vector db → `cheese-app-vector-db`; vector db → `vector-db`; api service → `api-service`; deploy
  images → `deploy_images`; deploy single VM → `deploy_single_vm`; create instance, provision
  instance, setup containers, setup webserver → the `.py` names; pulumi up, stack dev, refresh, dash
  y → `pulumi up --stack dev --refresh -y`; pulumi login local → `pulumi login --local`; dash y →
  `-y`; refresh flag → `--refresh`; password standard in → `--password-stdin`; docker rm dash f →
  `docker rm -f`; organization, deploy
  images, dev → `organization/deploy-images/dev`; retain on delete → `retain_on_delete`; Control C →
  `Ctrl+C`; ls dash l a → `ls -la`; Chroma DB host → `CHROMADB_HOST`; GCP project → `GCP_PROJECT`;
  Pulumi access token must be set → `PULUMI_ACCESS_TOKEN must be set`; the quoted error phrases in
  quotes ("no such container", "syntax error near unexpected token newline", "host not found in
  upstream frontend", "invalid grant, account not found", "has no installation candidate",
  "skipping preview build because some inputs are unknown", "no credentialed accounts", "created
  stack dev"). Added by the spoken review: http server → `http-server`; https server →
  `https-server`; allow http → `allow-http`; compute Firewall → `compute.Firewall`; persistent folder →
  `persistent-folder`; conf nginx → `conf/nginx`; frontend react → `frontend-react`; src deployment →
  `src/deployment`; vector db cli → `vector-db-cli`; or true → `|| true`; the remove flag → `--rm`;
  ssh keygen → `ssh-keygen`; ssh key deployment → `ssh-key-deployment`; google cloud SDK →
  `google-cloud-sdk`; google cloud CLI → `google-cloud-cli`; docker build Image → `docker_build.Image`;
  instance IP → `instance_ip`; plus, tilde, minus, plus minus → `+`, `~`, `-`, `+-`; slash api service
  slash status → `/api-service/status`; dash i slash secrets slash ssh key deployment → `-i
  /secrets/ssh-key-deployment`; pulumi stack init dev, pulumi stack select dev, stack init, config set
  → as is; block ID → `blkid`; make file system → `mkfs`; dash dash version → `--version`; E O F →
  `EOF`. In zh all of these stay English (glossary rule). Metaphors for the zh glossary,
  rendered the same way every time: "one public door" → 唯一的公共入口; "scissors" → 剪刀; "the
  phone book" → 通讯录 (DNS); "lamps" → 指示灯; "sealed envelope" → 密封的信封; "dominoes" → 多米诺骨牌;
  "the pipe" → 管道; "the toolbox" → 工具箱 (the container keeps its English name on screen).
- Never: the instructor's name (`‹instructor›`), the staff branch's name, a slide image or long slide
  text, a Google/GCP, Docker or Pulumi logo, a console or browser screenshot, a real-looking key,
  token, project id, `sa_` number or IP, a terminal panel of a successful push, VM creation,
  `pulumi up` or `instance_ip` value, a Gemini answer, the persistent disk called NFS, the registry
  called GCR (except "the slide still calls it GCR" once), the frontend on port 80, the local Pulumi
  backend or `--target` as steps to follow, advice to keep `0777`, to commit `secrets/` or a real
  `Pulumi.dev.yaml`, to put a passphrase on the deployment SSH key, or to use `-y` without checking
  the plan, and "destroy removes everything".

---

## S01 · One container stops, the site goes dark — `s01_hook.py` · `Hook`

SHOW: Black frame, no tracker, no lecture tag. A full-width terminal slides in, title
`cheese-app-vm`, prompt `student@cheese-app-vm:~$` (tag `extra`). It types line 1 of `vm/58` (folds
with ` \` into four rows) → TERM(vm/58: 2–8). On "one container" line 6 `frontend  Exited (0) …` turns
YELLOW; on "restarted the web server" line 5 `nginx  Exited (1) …` turns RED; on "still up" lines 7–8
(`api-service  Up 10 minutes`, `cheese-app-vector-db  Up 16 minutes`) tick GREEN.
SAY: We stopped one container, the frontend, and restarted the web server in front of it. The API container is still up, and so is the vector database.

SHOW: TERM(vm/58: 10, 11) prints below: the `[emerg] host not found in upstream "frontend"` line RED,
then `http://localhost/ -> 000` with `000` RED and a PINK chip beside it "nothing answers". A GREY
ghost line `http://localhost/api-service/ -> ?` writes under it and stays GREY and dashed (never
output: `vm/58:1` curls only `/`), with a GREY chip "same door: nginx is down".
SAY: Yet the whole site answers nothing, the address of the API included.

SHOW: The terminal shrinks to a strip at the top. A YELLOW card settles in the centre: "The API is
up. Why is the API's address dead too?" It holds, then shrinks into the top-right corner as a small
YELLOW sticky note (it stays until S07 block 11 in spirit; here it fades at the end of block 4).
SAY: Today's puzzle: the API is running, so why is its address dead too? We answer it once we have built this by hand.

SHOW: LECTURE 20 · 7. The strip fades. **V1 `MasterDiagram`** teaser at full size, slide 7 redrawn:
top left a GREY box "Local Computer" with an "IDE / CLI" bar, the word "Containers" and six small
dashed TEAL squares (the slide's generic containers), which stay there; a dotted BLUE outline "GCP" on
the right with a BLUE "Compute Instance (VM)" panel. A hollow GREY arrow drops from the laptop into
GCP and four named TEAL boxes grow inside the VM (nginx on top, API, frontend, vector DB). A PINK
door "80" appears on the VM's top edge; a GREY browser window drops above GCP with a PINK arrow down
to the door.
SAY: Here is the goal, the lecture's picture of deployment: the containers from your laptop move to one virtual machine in Google Cloud, with port 80 the only door. We build it twice: by hand, then as code.

SHOW: LECTURE 20 · 4–5. The diagram slides away. Slide 4 redrawn small: a wide GREY arrow with "POC",
"Prototype", "MVP" and dashed boundaries; staggered GREY bars below; a dashed YELLOW box moves down
one bar, from "Build Cheese App" to "Deployment, Scaling & Automation". Under it, slide 5's line as a
GREY laptop with a check mark "runs on your computer" and a BLUE server with a "?" "reaches users".
SAY: On the course roadmap, the marker has moved to deployment, scaling and automation. Everything so far ran on your own computer. Users need a server.

SHOW: The roadmap fades; the V1 laptop from block 4 waits small in a corner. Four chips slide onto
it, one per phrase: GREY "cheese-app-v3 + secrets/ beside
it", GREY "a GCP project with billing", GREY "a Docker Hub account", and a GOLD-outlined cost chip
"this lecture costs money · delete it at the end of each part" (GOLD `cost_tag`).
SAY: You need cheese app version 3 with your secrets folder beside it, a Google Cloud project with billing, and a Docker Hub account. This costs real money, so each part ends by deleting everything.

SHOW: The chips fade. Top-left a sample YELLOW `ReadmeTracker` ("README › Deployment to GCP
(Manual) · step 1 of 15"); in the middle a small sample code panel header `nginx.conf · lines 35–44`;
beside a sample command a YELLOW `▶ your turn` pulses, each on its phrase.
SAY: The tracker in the corner names the README step, code panels name their file and lines, and a yellow tag, your turn, means pause and run it.

SHOW: The samples fade. The S01 terminal returns small and shrinks into the left column of a GREY
card in the centre with two columns: left "a machine you own → real,
complete" (GREEN tick), right "Google · Docker Hub → stops at its first honest error" (RED dot) with a
GREY footer "and we say what yours prints". Fade; empty frame.
SAY: One honest note: our recording machine has no Google account and no Docker Hub login. What runs on a machine you own is real; every cloud step stops at its first honest error, and we say what yours prints.

---

## S02 · From your laptop to one VM — `s02_goal.py` · `TheGoal`

SHOW: No tracker yet. LECTURE 20 · 7. **V1** at full size, built in request order, one hop per
phrase: a GREY browser window top; a PINK arrow "HTTP 80" down onto a TEAL box `nginx` at the top of
the BLUE VM panel; from nginx two PINK arrows, one to TEAL `frontend · 3000`, one to TEAL
`api-service · 9000`; from the API a PINK arrow down to TEAL `vector-db · 8000`.
SAY: Let's draw the goal properly. A browser sends a request to port 80, where nginx passes pages to the frontend on port 3000 and data calls to the API on 9000. The API asks the vector database on 8000.

SHOW: LECTURE (held). A small GREY ghost of the slide's arrowheads (pointing at nginx and at the API)
flashes beside the PINK arrows and flips around to match them. Then a dashed TEAL box "loader"
appears beside the vector DB, pours a short stream of dots into it, and fades. (Slide 7's two
stores are not drawn here: the models bucket arrives in S06 block 3, the disk in S14 block 1.)
SAY: The slide draws its arrowheads the other way; we draw requests the way they travel. The slide shows four containers. There is a fifth: a loader that fills the vector database once and then leaves.

SHOW: LECTURE 20 · 8. V1 manual variant: the GREY laptop box on the left, a BLUE "Docker Hub" panel
in the middle, the VM on the right. Slide 8's four stages light as YELLOW chips along the bottom, one
per phrase: "1 Push" (an arrow laptop → Docker Hub), "2 Setup VM" (the VM panel outline glows), "3
Deploy containers" (four TEAL boxes + the dashed loader blink inside), "4 Web server" (nginx on top
glows).
SAY: The lecture splits the manual route into four stages: push the images, set up the VM, deploy the containers, and put a web server in front. That is our map for part 1.

SHOW: The four chips shrink to a thin row under the top edge. TRACKER [M] 1 (tracker appears: "README
› Deployment to GCP (Manual)", 15 dots). A README card (`README.md · lines 10–16`): "Ensure you have
all your container built and works locally · vector-db: ChromaDB is up and running · api-service:
http://localhost:9000/docs · frontend-react: http://localhost:3000/". Beside it a GREY laptop sketch
(GREY-dashed, "L18 · your laptop") with three TEAL boxes, each ticking GREEN on its phrase.
SAY: The README starts with a check, not a command: your containers run locally. The vector database is up, the API shows its docs on port 9000, and the frontend its home page on 3000.

SHOW: A small GREY note card (tag `erratum`) under the README card: "on v3's code: `/status` →
`{"version":"3.0"}`" (CODE(src/api-service/api/service.py: 34–36) as a three-line inset).
SAY: A small note: on this code, slash status is a better API check than the docs page. It answers version three point zero, so you know which code runs.

SHOW: A GREY-dashed chip "L18 · cheese-app-v2 (refactored)" slides in beside the laptop sketch and a
GREY arrow points from it to a TEAL-outlined chip "this video · cheese-app-v3 · its own
docker-shell.sh scripts".
SAY: If you followed lecture 18 lately, it now teaches a refactored version 2; here you run version 3, with this repository's scripts.

SHOW: TRACKER [M] 1 · extra. The sketch fades. A full-width terminal `laptop`, prompt
`student@laptop:~$`. It types `git clone https://github.com/dlops-io/cheese-app-v3.git` (tag
`extra · our spelling`) → TERM(p01: 2); then line 1 of `p02` (extra; folds) → TERM(p02: 2) only (the
branch list, lines 3–7, is not printed). The commit hash on line 2 glows YELLOW (not read), the date
`2025-11-28` PINK. A GREY chip: "the course site links: main". Fade; empty frame.
SAY: We follow main, the branch the course site links; on recording day it was this November 2025 commit. READMEs change; git log shows which one you have.

---

## S03 · Images to Docker Hub — `s03_docker_hub.py` · `DockerHub`

SHOW: TRACKER [M] 2. LECTURE 20 · 8. The stage chip "1 Push" glows YELLOW in the thin row. A schematic
GREY page "Docker Hub · Account settings · Personal access tokens" (tag `illustration`, no logo)
with a button "Generate new token" and a masked field `••••••••••••` that never reveals.
SAY: Stage 1: push the images. Create an access token in your Docker Hub account settings; it is a password for scripts, so never show it.

SHOW: Full-width terminal `laptop`, prompt `student@laptop:~$`. It types `docker login -u <USER
NAME> -p <ACCESS TOKEN>` → TERM(a01: 2–3) RED. The two `<` characters on the typed line pulse PINK;
a small PINK label under them: "redirection".
SAY: Typed exactly as the README prints it, the login fails: syntax error near unexpected token newline. Angle brackets are redirections to the shell, so replace the whole placeholder, brackets included.

SHOW: A GREY card (tag `extra`, no output panel): `echo "$TOKEN" | docker login -u <you> --password-stdin`
with `<you>` in YELLOW and `--password-stdin` highlighted GREEN. A struck-through GREY ghost of `-p
<ACCESS TOKEN>` beside it.
SAY: Better: the flag password standard in keeps the token out of your shell history.

SHOW: TRACKER [M] 3. The terminal moves down to a 3-row strip. CODE(src/frontend-react/docker-hub.sh:
7–14): line 11 `DOCKER_USERNAME="dlops"` YELLOW; a GREY pencil chip "→ your Docker Hub user".
SAY: Now the Docker Hub script, one in each service folder. Line 11 sets the user name to dlops, the course account: change it to yours.

SHOW: The panel scrolls: CODE(src/frontend-react/docker-hub.sh: 25–35). Line 27 (`docker buildx
create … --use --name multi-arch`) PURPLE; lines 31 and 35 YELLOW, `--push` on 35 PINK. A second
small panel slides in on the right: CODE(src/api-service/docker-hub.sh: 31–35) with
`linux/amd64,linux/arm64` PINK on lines 31 and 35; a TEAL crate labelled "one tag" splits into two
small crates "amd64" and "arm64".
SAY: Line 27 creates and selects a new BuildKit builder; the script builds, then builds again to push. The API script builds for A M D 64 and ARM 64; the frontend script, A M D 64 only.

SHOW: The panels fade. A small README card (`README.md · lines 24–35`) lists the three headings in
README order, "api-service · frontend-react · vector-db-cli", each with `sh docker-hub.sh`; the
frontend row lights YELLOW ("captured"), the other two stay GREY ("same command · block 8"). The
terminal grows back to full width as a new window, with a GREY chip "a new terminal · not a docker
shell" (README:20, 25), prompt
`student@laptop:~/cheese-app-v3/src/frontend-react$`; it types `sh docker-hub.sh` → TERM(a02: 2–5,
…, 124, 131, …, 172 wrap). Line 2 `Docker Username: dlops` YELLOW; line 131 `✓ Compiled
successfully` GREEN; on "warning" line 172 (the WARNING) turns ORANGE.
SAY: Inside frontend react, outside any docker shell, run it. It prints dlops, creates the builder, and builds: compiled successfully. The warning says this build stays in the builder cache.

SHOW: TERM(a02: 173, …, 254 wrap): `Pushing multi-arch image to registry...`, then the RED `ERROR:
failed to build: … push access denied …`. A BLUE "Docker Hub" panel on the right shows a crate
bouncing off a RED padlock "dlops".
SAY: Then the push: access denied. We are not dlops, and not logged in; with your name and login, this is where it says pushed.

SHOW: Three TEAL crates line up in README order: `api-service` (GREY-dashed, "not captured here: two
platforms · TensorFlow"), `frontend-react` (ticked "captured"), `vector-db-cli` (GREY-dashed, "not
captured here: two platforms"); above the two dashed crates the typed command `sh docker-hub.sh` is
shown as a GREY ghost line with its folder prompt and no output. A YELLOW `▶ your turn` beside them; a
GREY chip "check your Docker Hub page: three repositories".
SAY: Run the same script in api service and vector db; we did not capture those two-platform builds. Those two build for two chip types, one of them emulated: expect a long api service build, and on Linux register Q E M U first. Pause, run all three, and check Docker Hub.

SHOW: The terminal fades. A GREY card: "README's VM commands use `dlops/…` public images → part 1
works even if you skip this stage". A small GREY-dashed clock icon beside "a little older than the
code". Then a GREY chip: "`dlops/cheese-app-…` → `<you>/cheese-app-…`". Fade; empty frame.
SAY: Skip this stage and part 1 still works, using the public dlops images, which are a little older than the code. If you pushed yours, replace dlops with your user name in the VM commands.

---

## S04 · A VM with Docker, folders and a network — `s04_vm.py` · `VmWithDocker`

SHOW: TRACKER [M] 4. LECTURE 20 · 8. Stage chip "2 Setup VM" YELLOW. A schematic console form (tag
`illustration`, `console_form`, no logo): "Create an instance" with fields filled one per phrase:
"Machine type: N2D" (YELLOW), "OS and storage: disk size 50 GB" (YELLOW), "Networking: ☑ Allow HTTP
traffic ☑ Allow HTTPS traffic" (YELLOW), the rest "default" in GREY.
SAY: Stage 2: set up the VM. In the console, create a VM instance with the defaults, except machine type N 2 D, a 50 gigabyte disk, and HTTP and HTTPS allowed.

SHOW: No lecture tag (slide 22 draws no tags or gates). The form shrinks left. The empty BLUE VM
panel of V1 appears on the right with its disk cylinder below it on a cable. The two ticks fly from
the form onto the VM as two PINK name tags `http-server`, `https-server`; a dotted PINK fence
"firewall · network edge" draws itself around the VM, a little outside its box; two gates "80" and
"443" open in the fence, each tied by a thin line to its tag. From here on, `-p` doors open on the VM's
box (inside the fence), firewall gates only in the fence. A GOLD `cost_tag`: "billed while it runs · the disk while it exists".
SAY: Those two ticks add network tags, http server and https server; the default firewall opens 80 and 443 only to VMs with them. The VM now bills while it runs, its disk while it exists.

SHOW: TRACKER [M] 4 · extra. The VM panel shrinks to the top right. Full-width terminal
`cheese-app-vm`, prompt `student@cheese-app-vm:~$`. It types line 1 of `vm/00` (extra; folds) →
TERM(vm/00: 3, 4, 8, 9, 10): `cheese-app-vm`, `Debian GNU/Linux 12 (bookworm)`, `x86_64`,
`which-docker-exit:1` (YELLOW: "no docker yet"), `/home/student`. The date line 2 is not printed. A
GREY chip "stand-in for your VM".
SAY: Pause, create yours, and SSH in with the SSH button in the VM instances list. Our VM is a stand-in we can capture end to end: a fresh Debian 12 machine without Docker. Every command is the same on yours.

SHOW: TRACKER [M] 5. It types `curl -fsSL https://get.docker.com -o get-docker.sh` → TERM(vm/01: →
(no output)); then `sudo sh get-docker.sh` → TERM(vm/02: 2–3, …, 8 wrap, 12 wrap, …, 21–24) (lines
14–16 never printed). On "bookworm" the word `bookworm` on line 8 turns YELLOW. A GREY caption, not
spoken: "on a real VM, systemd starts Docker here". The VM panel in the corner gets an ORANGE layer
"Docker".
SAY: Install Docker with the official script: download it with curl, run it with sudo. It adds the Docker repository for bookworm and installs the engine, buildx and compose.

SHOW: It types `sudo docker --version` → TERM(vm/03: 2) with `at the time of recording` beside it. A
YELLOW `▶ your turn` beside the command.
SAY: Then check it with sudo docker, dash dash version. Pause here and install Docker on your VM.

SHOW: TRACKER [M] 6. A README card (`README.md · lines 53–68`) shows the six bullets and the code
block side by side; a GREY "=" sign between them and a YELLOW chip "run them once". Then it types
the six commands fast: `sudo mkdir persistent-folder`, `sudo mkdir secrets`, `sudo mkdir -p
conf/nginx`, `sudo chmod 0777 persistent-folder`, `sudo chmod 0777 secrets`, `sudo chmod -R 0777
conf` → TERM(vm/10 … vm/15: → (no output)) each.
SAY: Next, create folders: persistent folder, secrets and conf nginx, writable by anyone. The README lists these six commands twice: run them once, from your home directory.

SHOW: TRACKER [M] 6 · extra. It types `ls -la` (extra) → TERM(vm/16: 8, 10, 11): the three
`drwxrwxrwx … root root` lines, `drwxrwxrwx` ORANGE, `root root` YELLOW. A GREY chip "demo grade:
anyone on the VM may write here". A small PINK chip on `$(pwd)` "later mounts use the current
folder".
SAY: An extra check: the folders belong to root, but anyone may write there: fine for a demo VM only. Stay in your home directory: later mounts use the current folder.

SHOW: TRACKER [M] 7. It types `echo '<___Json Key___>' > secrets/gcp-service.json` → TERM(vm/17: →
(no output)); TRACKER [M] 7 · extra: `cat secrets/gcp-service.json` (extra) → TERM(vm/18: 2)
YELLOW. A GREEN key icon "gcp-service.json" slides into the VM's `secrets/` box, with a GREY-dashed
"your key text here" label; a RED "never commit · never show" chip; a GREY chip "your laptop:
secrets/gcp-service.json · made in S10 if you have none".
SAY: Now the app's key, gcp service dot json, written with echo; ours holds just the placeholder. Paste in the gcp service key from your laptop's secrets folder; part 2 shows how to make one. Never show or commit it.

SHOW: TRACKER [M] 8. It types `sudo docker network create cheese-app-network` → TERM(vm/19: 2) (the
id GREY, not read). **V2 `NamePhoneBook`** appears in the VM panel: a GREEN cable labelled
`cheese-app-network` and an empty small phone book "names on this network". A YELLOW `▶ your turn`
beside the `network create` line. Fade; empty frame.
SAY: Last, create the Docker network, cheese app network: a private network where our containers find each other by name. Pause and run these three steps.

---

## S05 · The vector DB and its loader — `s05_vector_db.py` · `VectorDb`

SHOW: TRACKER [M] 9. LECTURE 20 · 7–8. Stage chip "3 Deploy containers" YELLOW. Terminal
`cheese-app-vm`. It types `sudo docker pull chromadb/chroma:latest` → TERM(vm/20: 2, …, 26–27);
then `sudo docker stop cheese-app-vector-db || true` → TERM(vm/21: 2) ORANGE (not RED); then `sudo
docker rm cheese-app-vector-db || true` → TERM(vm/22: 2) ORANGE. The `|| true` on both typed lines
glows GREEN; a GREEN chip "safe to run again".
SAY: Stage 3: the containers. Pull the Chroma image, then stop and remove any old vector database. The error, no such container, is harmless here: or true makes the step safe to run again.

SHOW: It types the README's `sudo docker run -d \` block (vm/23: 1–9, folded as in the README) →
TERM(vm/23: 10) (id GREY). Flags glow one per phrase: `--network cheese-app-network` GREEN, `-p
8000:8000` PINK, `--restart always` YELLOW, `-v ./docker-volumes/chromadb:/chroma/chroma` GREY. In
V2 (small, right) a TEAL box `cheese-app-vector-db` plugs into the cable, a PINK door "8000" opens
on the VM's box (inside the fence), and its name writes into the phone book.
SAY: Then run it detached on cheese app network, publishing port 8000, restarting always, with a data folder mounted. Its name goes into the phone book.

SHOW: TRACKER [M] 9 · extra. A 3-row strip types line 1 of `vm/24` (extra; folds) → TERM(vm/24:
3 wrap, 4, 5): `0.0.0.0:8000->8000/tcp` PINK, the heartbeat, `"1.0.0"` with `at the time of
recording`.
SAY: An extra check: the port is published, the heartbeat answers, Chroma version one at the time of recording.

SHOW: TRACKER [M] 10. Full terminal again. It types `sudo docker pull dlops/cheese-app-vector-db-cli`
→ TERM(vm/26: 2, …, 45–46); then the README's `sudo docker run --rm \` block (vm/27: 1–9). On the
typed lines: `-e CHROMADB_HOST=cheese-app-vector-db` PINK with a chip "a name, not an address" (V2's
phone book entry glows); `-e GCP_PROJECT=ac215-project` with the GREY `default_tag`.
SAY: Now the loader, run vector db cli. It finds the database by name, cheese app vector db, not by address. The project is the README's default; change it to yours.

SHOW: TERM(vm/27: 13, 18–20, 24, 25 wrap, …, 37, …, 169, …, 180) scrolls: `Python version: Python
3.12.12`, `download()`, `load()`, `Creating collection: recursive-split-collection`, `Number of
files to process: 11`, the first `Processing file:` line, the last file's lines. Beside it the
YELLOW counter (see Notes) climbs with each `Finished inserting` line to **14,356**. In V2 a dashed
TEAL loader box knocks on `cheese-app-vector-db:8000` and pours a stream of dots into the vector DB.
SAY: It downloads, creates the collection, and loads eleven files: 14,356 chunks in all. The embeddings come precomputed, so our placeholder key never mattered.

SHOW: The dashed loader box fades out of V2 (its phone book line is struck through GREY: `--rm`). A
YELLOW `▶ your turn` beside the typed `docker run --rm` line.
SAY: The loader ran with the remove flag, so it exits and is gone. Pause and run both containers now.

SHOW: The terminal shrinks to a strip; V2 fills the frame: the vector DB box with a YELLOW "?" over
it (its inside not drawn), the empty spot where the loader stood.
SAY: A question. The loader is gone. Are the 14,356 chunks gone too?
PONDER(8 s, "The loader ran with --rm\nand is gone.\nAre the 14,356 chunks gone too?")

SHOW: The "?" lifts: the dots are inside the vector DB box; a YELLOW arrow points at them, labelled
"inside the container". A GREY chip: "remove the container → gone · the loader refills it".
SAY: No. The loader only sent them; they sit in the vector database container, which keeps running. Remove it, and the loader must fill a new one.

SHOW: TRACKER [M] 10 · extra (the fix goes back to step 9's command). The strip types line 1 of
`vm/25` (extra) → TERM(vm/25: 3, 21):
`persist_path: "/data"` YELLOW. Then line 1 of `vm/28` (extra; folds) → TERM(vm/28: 8–11, 18–19,
23): the empty `docker-volumes/chromadb` (RED chip "empty") and `/data … chroma.sqlite3` (GREEN chip
"here"). A GREY `erratum` tag on a GREY ghost of block 2's typed `-v …:/chroma/chroma`, with a GREEN
fix chip, the exact flag `-v ./docker-volumes/chromadb:/data`. Fade; empty frame.
SAY: But where inside that container? A small slip: Chroma saves to slash data, so the folder the README mounts stays empty. To keep the data on the VM disk, mount slash data instead, rerun the stop, remove and run lines, then the loader.

---

## S06 · The API and the frontend — `s06_api_frontend.py` · `ApiAndFrontend`

SHOW: TRACKER [M] 11. LECTURE 20 · 7–8. Terminal `cheese-app-vm`. It types the README's `sudo docker
run -d --name api-service \` block (vm/30: 1–10) → TERM(vm/30: 11, 12, …, 55–57) (digest and id
GREY, not read). Line 11 `Unable to find image … locally` YELLOW.
SAY: Next, run api service. The image is not on the VM yet, so docker run pulls it first.

SHOW: The typed block stays; flags glow one per phrase: the two `-v` lines GREEN, `-p 9000:9000`
PINK, `GOOGLE_APPLICATION_CREDENTIALS=/secrets/gcp-service.json` GREEN, `CHROMADB_HOST=cheese-app-vector-db`
PINK; `GCP_PROJECT=ac215-project` gets the GREY `default_tag`; `GCS_BUCKET_NAME=cheese-app-models`
dims to GREY with a chip "passed, never used". In V2 (small) a TEAL `api-service` box plugs into the
cable, door "9000" on the VM's box (inside the fence).
SAY: Two mounts, persistent folder and secrets; port 9000; the key path; and the database by name. The project is the README's default, and the bucket name is passed but never used.

SHOW: TRACKER [M] 11 · extra. It types line 1 of `vm/31` (extra) → TERM(vm/31: 2, 5, …, 26, 27 wrap,
…, 53). `Loading CNN Model...` YELLOW; `Uvicorn running on http://0.0.0.0:9000` GREEN. A small
GREY-dashed bucket "Models" (slide 7's store, drawn here for the first time) appears, gets a GREY
strike and a GREY chip "GitHub release → /persistent/experiments".
SAY: The logs show loading CNN model, then uvicorn running on port 9000. The model comes from a GitHub release, not a bucket, so our picture grays out the slide's bucket.

SHOW: It types line 1 of `vm/32` (extra) → TERM(vm/32: 5, 7): `dlops/cheese-app-api-service:latest
… 5.07GB` with a GOLD-outlined "disk" chip "about 5 GB on the VM disk".
SAY: And the image is big, about five gigabytes on disk, with TensorFlow inside.

SHOW: Three short strips, one per phrase, each typed (extra): `curl -s -i http://localhost:9000/` →
TERM(vm/33: 2, 8) GREEN; line 1 of `vm/35` (folds) → TERM(vm/35: 8, 14) (the Swagger `<title>` and
the info line); `curl -s -i http://localhost:9000/status` → TERM(vm/34: 2, 8) RED. Beside the 404 a
GREY `erratum` chip "public image older than your clone: no /status · your own images answer it"
(the `vm/36` block was cut for length, BRIEF trim order item 2; `vm/36` stays in ASSETS for
exercises.md).
SAY: Three extra curl checks: the root says welcome to AC215, and slash docs shows the docs page. Slash status says 404: the public image is older than your clone.

SHOW: A README card (`README.md · line 131`): "If you want to run in interactive mode like we did in
development". It types the README's `sudo docker run --rm -ti --name api-service \` block (vm/38:
1–12) → TERM(vm/38: 13 wrap) RED: `Conflict. The container name "/api-service" is already in use`.
SAY: The README then offers an interactive variant. Run as written, it fails: the name api service is in use, because the detached container still runs.

SHOW: TRACKER [M] 11 · extra. It types `sudo docker rm -f api-service` (extra) → TERM(vm/39: 2);
the README's interactive block again (vm/40: 1–12, typed fast) → TERM(vm/40: 13, 16, …, 24, 25):
`app@<id>:/app$ exit` (the id GREY); then the detached block again (vm/41: 1–10, fast) →
TERM(vm/41: 11). A GREY chip "optional · the dev mode from L18".
SAY: Remove the running one with docker rm dash f, and the variant opens a shell. It is optional: we exit and start the detached one again.

SHOW: TRACKER [M] 12. It types `sudo docker run -d --name frontend -p 3000:3000 --network
cheese-app-network dlops/cheese-app-frontend-react` (folds) → TERM(vm/42: 2, …, 55–57). TRACKER [M]
12 · extra: line 1 of `vm/43` (extra; folds) → TERM(vm/43: 6, 7, 12, 13): `<title>Formaggio</title>`,
`▲ Next.js 15.0.2`, `✓ Ready in 67ms`, `BASE_API_URL: /api-service` (YELLOW, a PINK chip "the page
calls /api-service/… on its own address"). In V2 a TEAL `frontend` box plugs in, door "3000" on the VM's box (inside
the fence). A YELLOW `▶ your turn` beside the frontend command. Fade; empty frame.
SAY: Then the frontend, on port 3000. The extra check shows the title, Formaggio, and the base API URL, slash api service, which the page calls on its own address. Pause and start both.

---

## S07 · nginx: one public door — `s07_nginx.py` · `OnePublicDoor`

SHOW: No tracker for this block. LECTURE 20 · 8, 24. V1 manual variant: the VM with its three TEAL
boxes and three PINK doors 3000, 9000, 8000 on the wall; a GREY browser above, confused between two
addresses ("…:3000" and "…:9000"). Then a TEAL `nginx` box drops in at the top of the VM, a PINK
door "80" lands on it, and the browser's two addresses merge into one "http://<VM IP>/".
SAY: Stage 4: a web server in front. A reverse proxy gives the browser one address: nginx listens on port 80 and forwards each request inside the VM.

SHOW: CODE(src/deployment/nginx-conf/nginx/nginx.conf: 35–44). **V3 `ProxyRoute`** beside it: a
PINK URL tile `/api-service/status` travels in from the left; line 35 `location ^~ /api-service/ {`
lights as a signpost, and the tile turns toward `api-service:9000`.
SAY: In the repository's nginx dot conf, the location block on line 35 catches paths that start with slash api service. It passes them to api service on port 9000.

SHOW: Line 37 `proxy_pass http://api-service:9000/;` YELLOW; its final `/` pulses PINK with a
label "this one character". V3: PINK scissors snip `/api-service` off the tile, which walks on as
`/status`.
SAY: Look at the end of that address: one slash. With it, nginx swaps the matched prefix for that slash, so slash api service slash status reaches the API as just slash status.

SHOW: The panel scrolls: CODE(src/deployment/nginx-conf/nginx/nginx.conf: 46–55). Line 47
`location / {` lights; a second tile `/` turns toward line 48 `proxy_pass http://frontend:3000;`.
V2's phone book (small) glows on `api-service` and `frontend`: "names on cheese-app-network".
SAY: Everything else goes to the next block, the frontend on 3000. Both targets are container names on cheese app network.

SHOW: TRACKER [M] 13. Terminal `cheese-app-vm`, tall. It types the README's `echo 'user  nginx; …'
> conf/nginx/nginx.conf` block (vm/44: 1–58) as a fast scroll → TERM(vm/44: → (no output)). The
terminal shrinks to a strip. The README card `README.md · lines 165–167` shows the `log_format`
lines; a PINK arc joins the outer `echo '` to the first inner `'` on README:165 ("the quote closes
here"); the text between the next pair turns GREY "outside quotes"; `$remote_addr`, `$remote_user`,
`$time_local` each shrink to nothing ("empty variables"). TRACKER [M] 13 · extra: the strip types line
1 of `vm/45` (extra; folds) → TERM(vm/45: 2, 6–8), and the card's remains TransformMatchingShapes into
its `log_format  main   - []  $` RED. Three groups: the strip, the card, the arc.
SAY: The README writes this file with one long echo in single quotes. But the file holds single quotes too, so the shell eats the log format and leaves a dash and two brackets.

SHOW: A strip types `sudo docker logs nginx 2>&1 | tail -6` (extra) → TERM(vm/51: 3–7) (`-[]`
lines, RED). GREY `erratum` tag; a GREEN fix card with three lines (no capture):
`cat > conf/nginx/nginx.conf <<'EOF'` · "paste the README's text between the quotes" · `EOF`.
SAY: Routing still works, but the access logs are useless. Write it with a quoted heredoc instead: cat, the same text, then E O F.

SHOW: TRACKER [M] 14. It types `sudo docker run -d --name nginx -v
$(pwd)/conf/nginx/nginx.conf:/etc/nginx/nginx.conf -p 80:80 --network cheese-app-network
nginx:stable` (folds) → TERM(vm/46: 2, …, 36–38). TRACKER [M] 14 · extra: `sudo docker container
ls` (extra) → TERM(vm/47: 2–6), the four PORTS cells PINK. In V2 the `nginx` box plugs in, door "80" on the VM's box (inside the fence).
SAY: If you used the echo, rewrite the file this way first. Then run nginx with that file mounted, publishing port 80. The container list shows four: ports 80, 3000, 9000 and 8000.

SHOW: TRACKER [M] 15. A GREY browser window (`browser_window`, tag `illustration`) with address
`http://<Your VM IP Address>/`: a schematic home page (title bar "Formaggio", a hero block, a footer
row). A small schematic chip (tag `illustration`) "VM instances · External IP column" points at the
address bar. Beside it a `cheese-app-vm` strip types line 1 of `vm/48` (extra; folds) → TERM(vm/48:
2–3, 10): `HTTP/1.1 200 OK` GREEN, `Server: nginx`, `<title>Formaggio</title>`.
SAY: Open the external IP of your VM, from the VM instances list, in a browser, and the home page appears. On the VM, curl agrees: 200 OK, served by nginx, title Formaggio.

SHOW: The strip types line 1 of `vm/49` (extra; folds) → TERM(vm/49: 2, 9) only (the `/status`
404 half is not shown): `{"message":"Welcome to AC215"}` GREEN. V3's scissors replay small over the
line. A YELLOW `▶ your turn` beside the browser.
SAY: Slash api service says welcome to AC215: the prefix was cut on the way. Pause and open your site.

SHOW: The browser and strip fade. The VM box at full size with its four doors 80, 3000, 9000, 8000,
and S04's firewall fence around it; the fence's gates are drawn but unlabelled (a "?" at the 9000
spot). A GREY laptop outside with a PINK arrow "…:9000" stopping in front of the fence (no answer
shown).
SAY: A question. Port 9000 is published on the VM. Does it answer from your laptop?
PONDER(8 s, "Port 9000 is published on the VM.\nFrom your laptop, does\nhttp://<VM IP>:9000/ answer?")

SHOW: The gates get their labels: the 80 and 443 gates (PINK, tied to `http-server`, `https-server`)
and a third, GREY gate "22 · SSH (default rule)". The laptop's PINK arrow bounces off the closed 9000
spot in the fence (RED); the 80 gate glows GREEN. A GREY caption "open on the VM · shut at the fence".
SAY: No. The two ticks opened only 80 and 443; no rule opens 9000. Port 9000 is open on the VM but shut at the network edge: one public door.

SHOW: The puzzle card from S01 returns small. V2 at full size: the phone book with `frontend` and
`api-service` lines; a `frontend` box stops (GREY) and its phone-book line is erased; nginx restarts
and its lookup arrow returns empty; RED stamp `[emerg] host not found in upstream "frontend"`; the
nginx box goes RED, the PINK door "80" on it closes (a RED bar across it) and the browser's arrow
stops at it; then the route to `api-service` fades. A strip shows TERM(vm/58: 5–6, 10)
(typed line not repeated; a GREY chip "from the opening").
SAY: Now the puzzle. The web server looks up frontend and api service once, at start. With the frontend stopped, the restart fails that lookup and exits, taking the API route with it.

SHOW: The strip types line 1 of `vm/59` (extra; folds) → TERM(vm/59: 4–6, 9): both `Up 3 seconds`
GREEN, `http://localhost/ -> 200` GREEN. In V2 the boxes turn TEAL again and the routes reconnect. A
GREY chip "no restart policy" under `frontend`, `api-service` and `nginx` (only the vector DB command,
README:96, has `--restart always`). Fade; empty frame.
SAY: Start the frontend, then nginx, and the site answers 200 again. Start order matters, and so does a restart policy, which only the vector database command has.

---

## S08 · Twenty-one commands: repeat, review, undo? — `s08_by_hand.py` · `ByHand`

SHOW: No tracker. A narrow scrolling column of the 21 VM commands of README:48–219 (the optional
interactive one excluded), each a one-line GREY chip (long ones truncated with "…"), counted by a
YELLOW number in the corner that climbs to **21**; beside the column, a small GREY "console clicks"
chip and three TEAL "docker-hub.sh" chips (laptop). Each command drops a small block onto the V1 VM
panel on the right, which becomes a tower.
SAY: Let's count what we typed. Twenty-one commands on the VM, plus console clicks, plus three Docker Hub scripts on the laptop. Each one added a block to the VM.

SHOW: Three YELLOW speech bubbles pop over the tower, one per phrase: "Repeat? staging, tomorrow",
"Review? what exactly is on that VM?", "Undo? delete every piece".
SAY: Now three questions. Repeat: can you build the same thing for a staging copy tomorrow? Review: what exactly is on that VM? Undo: how do you delete every piece?

SHOW: LECTURE 20 · 9. The bubbles shrink into a single GREY card, slide 9's idea in our words: "too
many steps to keep track of → automate" (no logo). Under the card the tower's blocks flicker in a
scrambled order ("keep track of?") and line up neatly on "let a tool do them".
SAY: The lecture answers with one idea: too many steps to keep track of, so let a tool do them.

SHOW: LECTURE 20 · 10–11. The tower turns into a GREEN file icon `__main__.py` (Python) with a GREY
"git" ribbon; beside it a GREY-dashed struck card "YAML / DSL". Three GREY chips under the file:
"servers", "networks", "software".
SAY: That is infrastructure as code. You describe the servers, the networks and the software in a real programming language, Python here, and keep it in Git to share. No YAML file, no special language.

SHOW: A GREY-dashed card "earlier · Ansible playbooks (YAML)" with five lines "images · VM ·
provision · containers · web server"; arrows map them one to one onto five GREEN chips "this version ·
Pulumi (Python)".
SAY: An earlier version of the course did these same stages as Ansible playbooks, written in YAML. This version does them with Pulumi, one to one.

SHOW: The cards fade. A GREY `extra` tag and a schematic console list (tag `illustration`): "VM
instances · cheese-app-vm" with a checkbox ticked, a "Delete" button, and a confirm dialog with
"☑ delete boot disk". A GOLD meter beside it ticks, then stops at the "Delete" click; a GOLD chip
"the README never deletes this VM". A YELLOW `▶ your turn` beside the Delete button; after the click
the list shows a GREY "No VM instances" (illustration, not a capture).
SAY: One more thing the README never says: delete this VM now, before part 2. In the console, open VM instances, select it, and delete it with its boot disk. Pause and delete yours; the list should be empty.

SHOW: The V1 VM panel empties and fades to an outline. A GREY caption: "part 2 · as code". Fade;
empty frame.
SAY: Part 2 builds it all again, as code, and lets a tool remember every piece.

---

## S09 · Pulumi: desired state, not steps — `s09_desired_state.py` · `DesiredState`

SHOW: No tracker. LECTURE 20 · 17. S08's tower of 21 command blocks returns small on the left (GREY,
"steps"); it Transforms into a single GREEN card on the right listing three nouns: "a firewall: port
80", "a VM", "a disk" ("what should exist"). Then the card Transforms into
CODE(src/deployment/deploy_single_vm/create_instance.py: 51–62), three parts lighting one per phrase: line 51 `gcp.compute.Firewall(` PURPLE "constructor"; line 52
`"allow-http",` YELLOW "logical name"; lines 53–61 GREEN "arguments" (`ports=["80"]`,
`source_ranges=["0.0.0.0/0"]`, `target_tags=["http-server"]` each PINK).
SAY: Part 2. Each Pulumi program says what should exist, not what to do. One firewall rule from this repository: a constructor, compute Firewall; a logical name, allow http; and arguments: port 80, from anywhere, for VMs tagged http server.

SHOW: LECTURE (held). A GREY-dashed card beside it, the slide's example in outline only (no code):
"Bucket( name, location, website )", with the same three coloured brackets. Then the panel's line 51
gets a small GREY stamp "registered", and an empty BLUE cloud outline stays empty (a GREY "nothing
created yet").
SAY: The lecture's bucket example has the same shape. Running this line creates nothing: the constructor only registers the resource.

SHOW: LECTURE 20 · 14. **V4 `EngineLoop`**: top a GREY box "Your Machine"; the PURPLE "pulumi CLI"
runs `__main__.py`, which drops resource cards into a GREEN tree "desired".
SAY: This is the lecture's picture of Pulumi: the command line tool runs your program, which produces the desired state, a tree of resources.

SHOW: LECTURE (held). Two more trees slide in: a GREEN scroll "state" (from a small BLUE bucket) and
BLUE cloud objects "reality". A PINK "--refresh" sweep lines the state tree up with reality (one
stale card updates).
SAY: Pulumi also loads its state, what it created last time, from your bucket. The refresh flag first checks that state against what really exists.

SHOW: LECTURE (held). The desired tree is compared with the state tree; glyphs pop on its cards:
GREEN `+`, YELLOW `~`, RED `-`, and one `+-`. They line up as a plan list.
SAY: Then it compares desired with current, and each difference becomes a plan line: plus to create, tilde to update, minus to delete, plus minus to replace.

SHOW: LECTURE (held). A PINK down arrow carries the plan to four PURPLE provider plugs ("gcp",
"docker-build", "docker", "command"), which turn into BLUE cloud objects. The banner writes under
the picture: "Pulumi manages infrastructure through cloud APIs".
SAY: Finally it calls the providers, plugins for Google Cloud, Docker and more, which make the API calls. The banner on the slide: Pulumi manages infrastructure through cloud APIs.

SHOW: LECTURE 20 · 15. V4 shrinks left. A card of seven commands: `new`, `up`, `preview`, `destroy`,
`stack`, `config`, `refresh`; `stack`, `config`, `preview`, `up`, `destroy` light YELLOW, `refresh`
YELLOW-outlined with a chip "as the --refresh flag", `new` GREY with a chip "both projects already
exist".
SAY: The lecture lists seven commands. The tutorial uses five: stack, config, preview, up and destroy, with refresh only as a flag. The command new stays gray, because both projects already exist.

SHOW: LECTURE 20 · 16. The card fades. A wide strip: `pulumi up --stack dev --refresh -y`, each
part lighting on its phrase: `up` PURPLE ("preview, ask, apply"), `--stack dev` GREEN ("which
environment"), `--refresh` PINK ("sync state with reality first"). V4 small beside it replays the
refresh sweep.
SAY: Now the README's command: pulumi up, stack dev, refresh, dash y. Up previews, asks, then applies. Stack dev picks the environment. Refresh syncs the state with reality first.

SHOW: LECTURE (held). `-y` lights YELLOW. A GREY dialog pops "Do you want to perform this update?
yes / no" and a YELLOW hand clicks "yes" for you; a RED-outlined chip "your chance to check the plan"
fades. A second strip `pulumi preview --stack dev --refresh` ends at the plan list with a GREY stop
sign "nothing applied".
SAY: Dash y answers yes to the question, do you want to perform this update, and skips your chance to check the plan. Step 3 shows when that matters. Preview stops before anything changes.

SHOW: The strips fade. V4 at full size, all three trees identical, nothing in the plan list yet.
SAY: A question. You run pulumi up again and changed nothing. What should the plan show?
PONDER(8 s, "You run pulumi up again,\nchanged nothing.\nWhat should the plan show?")

SHOW: The three trees glow GREEN together ("desired = state = reality"); the plan list stays empty
with a GREY "no changes"; the PINK down arrow stays dark. A small YELLOW sticky note "hold that
thought: S13" in the corner. Fade; empty frame.
SAY: Nothing to do. Desired equals state equals reality, so there is no difference, and nothing is created, changed or deleted. Hold that thought: one stack in this repository breaks the rule.

---

## S10 · Setup: four APIs, two keys — `s10_setup.py` · `TwoKeys`

SHOW: No tracker for this block. LECTURE 20 · 19. The **six-step strip** builds chip by chip, each
file writing under its chip; chip 1 "Setup" turns YELLOW. Below it the V1 automated variant: the GREY
laptop box (top left) and an empty dotted BLUE GCP outline.
SAY: The lecture splits the automated deployment into six steps: setup, images, VM, provisioning, containers and web server. Each maps to a file; we start with step 1.

SHOW: TRACKER [P] 1 (tracker appears: "README › Deployment to GCP (Single VM Instance)", 14 dots).
LECTURE 20 · 20. The strip shrinks away. A schematic checklist (tag `illustration`, no logo): "APIs &
Services": "Compute Engine API", "Service Usage API", "Cloud Resource Manager API", "Artifact
Registry API", each ticked GREEN on its phrase; a fifth GREY-dashed line "Vertex AI API · from
earlier lectures".
SAY: First, enable four APIs: Compute Engine, Service Usage, Cloud Resource Manager and Artifact Registry. The app's chat also needs Vertex AI, from earlier lectures.

SHOW: TRACKER [P] 2. **V8 `KeyRing`** opens as an empty two-row card on the right: row 1 "builds
things" (three closed doors create · SSH · delete), row 2 "runs things" (read images · read stored
files · use Vertex AI). A schematic IAM form (tag `illustration`) slides in beside row 1: "Create
service account · deployment" with the README's six roles (README:241–246) as chips: Compute Admin,
Compute OS Login, Artifact Registry Administrator, Kubernetes Engine Admin, Service Account User,
Storage Admin; the chips fly onto row 1's doors. A "Create key · JSON" button; the key file renames to
`deployment.json` (RED-rimmed BLUE key icon) and hangs on row 1.
SAY: Then create two service accounts. Deployment gets six roles, among them Compute Admin, Compute OS Login, Artifact Registry Administrator and Storage Admin. Create a JSON key, and rename it deployment dot json.

SHOW: The same form for "gcp-service" beside row 2, with three role chips (README:253–255): Storage
Object Viewer, Vertex AI Administrator, Artifact Registry Reader, flying onto row 2's doors; its key
renames to `gcp-service.json` (GREEN key icon) and hangs on row 2.
SAY: The second, gcp service, gets three roles: Storage Object Viewer, Vertex AI Administrator and Artifact Registry Reader. Its key becomes gcp service dot json.

SHOW: LECTURE 20 · 25. The finished V8 card (slide 25's two keys) moves to the centre; the forms are
gone. The word "your" in a GREY line "admin on **your** group's project" pulses YELLOW, beside a
struck GREY `ac215-project`.
SAY: Why two? Deployment builds things. It needs admin rights on your group's project, not the README's default, to create the VM and log in. The narrow account only runs things: it reads images and stored files and uses Vertex AI.

SHOW: TRACKER [P] 2 · extra. A terminal `laptop` 3-row strip shows the typed line 1 of `p01` (extra,
already done in S02; GREY), then a GREY chip "your keys → secrets/ (README:249, 258)" standing for
`p04`, then line 1 of `p05` (extra; folds) → TERM(p05: 6–7, 11–12): `cheese-app-v3` and `secrets`
side by side, the two key files inside `secrets`. A PINK arrow from
`src/deployment` climbs three folders up to `secrets/` with a chip `docker-shell.sh:9 · ../../../secrets`.
A YELLOW `▶ your turn`.
SAY: Both keys go into a secrets folder next to your clone, not inside it. The deployment script of the next step looks three folders up from src deployment to find it. Pause and place your keys.

SHOW: A GREY `erratum` card: "nothing creates the registry repository", then a GREY card (tag
`extra · not in the README`, no output panel): `gcloud artifacts repositories create
cheese-app-repository --repository-format=docker --location=us` with a GREEN chip "look for: Created
repository", a RED ghost "skip it → the push fails" and a GREY chip "you run it at the end of S11".
Fade; empty frame.
SAY: One step is missing from the README: nothing creates the Artifact Registry repository. We create it with one extra gcloud line in the next step, once the deployment container runs; skip it, and the push fails.

---

## S11 · The deployment toolbox, fixed twice — `s11_toolbox.py` · `Toolbox`

SHOW: TRACKER [P] 3. LECTURE 20 · 14, 20. **V5 `ControlRoom`** left: a GREY laptop holding a TEAL
container `cheese-app-deployment` ("Your Machine"). CODE(src/deployment/docker-shell.sh: 9–17) right;
lines 9–17 light one by one and the names on 13–17 fly onto the container's side as small labels
(`GCP_PROJECT`, `GCP_REGION`, `GCP_ZONE`, `GOOGLE_APPLICATION_CREDENTIALS`, `PULUMI_BUCKET`); last, a
GREY label `PULUMI_CONFIG_PASSPHRASE=""` joins them with its source chip "Dockerfile:51". (No README
card: the SAY paraphrases README:263.)
SAY: Rather than each of you installing different tools, the README packs them into one container, the deployment toolbox. Lines 9 to 17 of docker-shell.sh set its environment.

SHOW: The panel scrolls: CODE(src/deployment/docker-shell.sh: 34–43). In V5, one coloured wire per
phrase from the laptop into the container: line 35 the Docker socket (GREY → "your Docker daemon"),
line 36 `src/deployment → /app`, line 37 `secrets → /secrets` (keys glow), line 39
`docker_config.json → /root/.docker/config.json` (PURPLE "credential helpers"), lines 41–43 three
build contexts `/api-service`, `/frontend-react`, `/vector-db`.
SAY: Lines 34 to 43 wire it to your laptop. They mount the Docker socket, so it builds on your Docker, then deployment as slash app, the secrets, a Docker config and the three service folders.

SHOW: Terminal `laptop`, prompt `student@laptop:~/cheese-app-v3/src/deployment$`. A GREY `erratum`
chip on a README card (`README.md · line 266`): "cd into `deployment`" → "src/deployment". It types
line 1 of `b01` (tag `extra · or edit the file`; folds) → TERM(b01: 2): `export
GCP_PROJECT="your-gcp-project" # Change to your GCP Project`, the value YELLOW.
SAY: Change into src deployment. In docker-shell.sh, set GCP project to your project ID; ours is a placeholder.

SHOW: It types `sh docker-shell.sh` → TERM(b02: 2–3, 12, …, 135 crop "404  Not Found", 136 crop
"404  Not Found", 137 crop "404  Not Found", …, 166 wrap, 167, 168 wrap). The three `404 Not Found`
lines RED, `ERROR: failed to build` RED, `Unable to find image …` ORANGE, `pull access denied` RED.
SAY: Now run docker-shell.sh, as committed. Downloads answer 404 not found, the build stops, and the script runs the container anyway: pull access denied.

SHOW: The terminal shrinks to a strip. In V5 the container's base becomes a small wall of Dockerfile
bricks; brick "line 4" turns RED, brick "lines 29–30" stays GREY (not reached yet).
CODE(src/deployment/Dockerfile: 1–12): line 4 `FROM
python:3.13-slim-bullseye` RED, line 11–12 (`apt-get install … curl …`) ORANGE. A small ORANGE shelf
"Debian 11 · bullseye-security" whose boxes slide off to a GREY-dashed "archive". GREY `erratum` tag.
The strip types line 1 of `b02a` (extra; folds) → TERM(b02a: 2): `4:FROM python:3.13-slim-bookworm`
GREEN; the RED brick in the Dockerfile swaps for a GREEN one.
SAY: The cause is line 4: the base image is Debian 11, bullseye, whose security updates moved to an archive. Fix 1: change bullseye to bookworm, Debian 12.

SHOW: Full terminal. It types `sh docker-shell.sh` again → TERM(b02b: 3, 12–17, 18 wrap, …, 34, 37,
38, 46, 47). Steps 2–7 GREEN; `ERROR [ 8/16] …` RED; `Package google-cloud-sdk is not available`
ORANGE; `However the following packages replace it:` / `google-cloud-cli` GREEN; `E: Package
'google-cloud-sdk' has no installation candidate` RED. A two-line inset CODE(src/deployment/Dockerfile:
29–30) beside the strip, line 30 RED; in V5, brick "lines 29–30" turns RED.
SAY: Run it again. Now it stops at line 29: google cloud SDK has no installation candidate. Google renamed it, and apt even names the replacement, google cloud CLI.

SHOW: It types line 1 of `b02c` (extra; folds) → TERM(b02c: 2–23) as a coloured diff: the `-` lines
10 and 19 RED, the `+` lines 11 and 20 GREEN. V5's RED brick "lines 29–30" swaps for GREEN. A YELLOW `▶ your turn`.
SAY: Fix 2: rename both packages. Here is the real diff of the two fixes, one line each. Pause and make both edits.

SHOW: It types `sh docker-shell.sh` a third time → TERM(b02d: 3, …, 31, 34, 35, 36 wrap): `[+]
Building 91.9s (21/21) FINISHED` GREEN, the banner, then the RED `ERROR:
(gcloud.auth.activate-service-account) … 'invalid_grant: Invalid grant: account not found'`. In V5
the entrypoint's chain of five lamps appears (`docker-entrypoint.sh:10-27`): lamp 1 "activate key"
goes RED.
SAY: The third run builds in about 92 seconds, and the entrypoint starts. First error: invalid grant, account not found. Our key belongs to no account; yours activates the deployment account.

SHOW: TERM(b02d: 52, 61, 63, 65, 66, 70, 71 wrap, 76, 77): `Updated property [core/project].` and
`Adding credentials for: us-docker.pkg.dev` GREEN (lamps 2 and 3 GREEN), `Bucket does not exist.
Creating...` → `You are attempting to access protected data …` RED (lamp 4 RED), `Logging into Pulumi
using GCS bucket …` → `error: could not log in to the state backend …` RED (lamp 5 RED), `No stacks
found.`, then the prompt `root@<id>:/app#` (id GREY). A GREY chip "with your key: five GREEN lamps".
SAY: The project and registry helper pass. Then the state bucket: ours could not be created, and Pulumi could not log in. Yours creates the bucket the first time, logs in, and leaves you here.

SHOW: TRACKER [P] 4. Terminal `laptop · toolbox`, prompt from `b02d:77`. It types `gcloud --version`
→ TERM(b03: 2, 11), `pulumi version` → TERM(b04: 2), `kubectl version --client` → TERM(b05: 2), each
with `at the time of recording`. On "surprise" `v1.35.9-dispatcher` YELLOW beside a GREY ghost
"Dockerfile:33 · K8S_MINOR=1.34"; a small PURPLE arrow "apt picks Google's kubectl package (1:592)
over pkgs.k8s.io 1.34".
SAY: Check the tools: gcloud, Pulumi and kubectl. One surprise: kubectl is newer than the Dockerfile pins, because Google's apt repository has its own kubectl package with a higher version, and apt picks it.

SHOW: It types `gcloud auth list` → TERM(b06: 3) RED: `No credentialed accounts.` Beside it a
GREY ghost line (said, not output): "yours: * deployment@<your project>.iam.gserviceaccount.com".
Then the GREY `extra · not in the README` card from S10 returns under it: `gcloud artifacts
repositories create cheese-app-repository --repository-format=docker --location=us`, GREEN chip
"look for: Created repository" (no output panel: not run here). A YELLOW `▶ your turn` covers both
lines. Fade; empty frame.
SAY: Last check: gcloud auth list. Ours says no credentialed accounts. Yours lists the deployment account as active; if not, check the file name in secrets. Then create the registry repository with the extra line from earlier. Pause and run both.

---

## S12 · SSH keys and OS Login — `s12_ssh.py` · `SshKeys`

SHOW: TRACKER [P] 5. No lecture tag; a GREY chip "not on the slides". **V8**: the PURPLE key
`ssh-key-deployment` appears beside the BLUE deployment key; a small sketch: the GREY laptop → PINK
SSH line → an outlined BLUE VM, with a badge "who logs in? deployment, via OS Login".
SAY: This is the one setup the slides skip. Pulumi will log in to the VM over SSH to run scripts and drive Docker. Who logs in? The deployment service account, through OS Login: the VM accepts a key registered to that account's login profile, under a Linux username Google derives from it.

SHOW: Terminal `laptop · toolbox`. It types `gcloud compute project-info add-metadata --project <YOUR
GCP_PROJECT> --metadata enable-oslogin=TRUE` (folds) → TERM(b08: 2) RED; the `<` and `>` pulse PINK
as in S03.
SAY: First, turn OS Login on for the project. Typed as printed, the template fails with no such file. It is the angle bracket lesson again: replace the whole placeholder.

SHOW: It types `gcloud compute project-info add-metadata --project ac215-project --metadata
enable-oslogin=TRUE` (folds; `ac215-project` with `default_tag`) → TERM(b09: 2 wrap) RED: `You do not
currently have an active account selected.` A GREY ghost (said, not output): "yours: Updated […]".
SAY: The README example uses its own project, which you change to yours. Ours says no active account; yours prints updated.

SHOW: TRACKER [P] 6. It types the README's three lines `cd /secrets`, `ssh-keygen -f
ssh-key-deployment`, `cd /app` (b10: 1–3) → TERM(b10: 4–8): `Enter passphrase (empty for no
passphrase):` and `Enter same passphrase again:` each followed by a YELLOW "⏎" (Enter, empty);
lines 10–22 (fingerprint, randomart) are never printed. The prompt changes to `…:/secrets#` after
line 1 and back to `…:/app#` after line 3 (the `b02d:77` string with the path swapped). A
RED-outlined GREY chip "no passphrase: Pulumi cannot type one". V8: the PURPLE key is cut into two halves, "private" and ".pub".
SAY: Next, the key: in slash secrets, run ssh keygen with the name ssh key deployment, press Enter twice, and go back to slash app. No passphrase: Pulumi cannot type one.

SHOW: TRACKER [P] 6 · extra. It types `ls -la /secrets` (extra) → TERM(b11: 6–9): the two new files
YELLOW, `-rw-------` on the private key GREEN. A PINK arrow from `/secrets` back to the laptop's
`secrets/` folder: "the same folder".
SAY: The two files now sit in the secrets folder on your laptop: the private key, readable only by you, and the public half.

SHOW: TRACKER [P] 7. It types `gcloud compute os-login ssh-keys add
--key-file=/secrets/ssh-key-deployment.pub` (folds) → TERM(b12: 2 wrap) RED. Then EXPECTED(
expected/oslogin: 2–10) slides in beside it (tag `expected · README:306–314`), `username:
sa_000000000000000000000` YELLOW. V8: the `.pub` half flies up to a BLUE card "deployment · OS Login
profile", which hands back a YELLOW name tag `sa_000…`. A YELLOW `▶ your turn`.
SAY: Then upload the public half to the OS Login profile. Ours stops at the same error; the README shows yours, ending in a username that starts with S A. Copy it: the VM stack's config needs it.

SHOW: TRACKER [P] 8. A README card (`README.md · lines 318–322`): "Deployment Setup · Add ssh user
details in inventory.yml file …" with a GREY `erratum` tag. TRACKER [P] 8 · extra: it types line 1
of `b13` (extra; folds) → TERM(b13: 2) RED. A GREY-dashed chip "earlier · Ansible" and a GREEN
arrow "→ Pulumi config (S14)". Fade; empty frame.
SAY: A small slip: the next heading asks you to edit inventory dot yml. No such file exists; it belongs to an earlier, Ansible version of the course. The Pulumi config replaces it.

---

## S13 · Step 2: images with timestamps — `s13_images.py` · `ImagesStack`

SHOW: No tracker for this block. LECTURE 20 · 19, 21. The six-step strip: chip 1 ticked GREEN, chip
2 "Images · deploy_images/" YELLOW; it shrinks away. V1 at slide 21: the GREY laptop box drops an
arrow onto a BLUE registry panel at the bottom left of GCP, with three image bars (Cheese App Image,
API Service Image, Vector DB CLI); the right half of GCP empty. The panel's label reads "Artifact
Registry" with a small GREY "(GCR on the slides)" that fades after the phrase.
SAY: Step 2: build and push the images. Your laptop's arrow lands on the registry; slide 21 still calls it GCR, its retired name: today it is Artifact Registry.

SHOW: LECTURE 20 · 13, 18. One GREEN file card "one program" with three stack cards under it, "dev",
"staging", "prod", each with its own small GREEN scroll "state" and GREY "config". Then the cards
regroup into the tutorial's reality: two project cards `deploy_images/Pulumi.yaml` ("deploy-images")
and `deploy_single_vm/Pulumi.yaml` ("deploy-single-vm"), each with one stack "dev".
SAY: Pulumi keeps environments apart as stacks of one program, dev, staging and production, each with its own state and config. The tutorial has one stack, dev, per project.

SHOW: LECTURE (held). On "Its full name": the `deploy-images` stack card shows its full name
`organization/deploy-images/dev` in GREEN; a PINK dotted line runs from it to a GREY ghost of
`setup_containers.py:27` ("used by name"); a RED-outlined chip "don't rename". Then that group dims,
and on "Every stack" (`vo.wait_until("Every stack")`) both stack scrolls slide into a small BLUE
bucket "your state bucket".
SAY: Its full name, organization, deploy images, dev, is used by the VM project, so do not rename it. Every stack state sits in your bucket.

SHOW: TRACKER [P] 9. Terminal `laptop · toolbox`. It types `cd deploy_images` and `pulumi stack init
dev` (b14: 1–2) → TERM(b14: 3, 5, 7 crop "or"): `Connect to Pulumi Cloud for state storage …`, `Press
<ENTER> to log in with your browser, or` ORANGE. A GREY chip "no bucket login (S11) → Pulumi offers
its own cloud"; then a GREY chip `pulumi stack select dev` · "second time".
SAY: Change into deploy images and run pulumi stack init dev. Without a bucket login, Pulumi offers its own cloud and waits for a browser. If yours says the stack already exists, use pulumi stack select dev.

SHOW: The same terminal types `pulumi config set gcp:project ac215-project` (`default_tag`) →
TERM(b15: 2) RED; TRACKER [P] 10: `pulumi preview --stack dev --refresh` → TERM(b16: 2) RED; `pulumi
up --stack dev --refresh -y` → TERM(b17: 2) RED. Then TRACKER [P] 9 · extra: it types `pulumi login
--local` (tag `extra · not for you`) → TERM(b30: 2 crop "as root") with the container id GREY.
SAY: Config set, preview and up all print: Pulumi access token must be set. To show them anyway, we use a local folder, pulumi login local: extra, and not for you.

SHOW: On the local backend (all `extra`): `pulumi stack init dev` → TERM(b31: 2) GREEN; `pulumi
config set gcp:project ac215-project` → TERM(b32: → (no output)); line 1 of `b33` (folds) →
TERM(b33: 2–3, 6–9): `gcp:project  ac215-project` with `default_tag`, `dev*` with `0`. A GREY file
icon `Pulumi.dev.yaml` glows "committed in the repo · config set rewrites it · shows in git status:
keep it on your branch" (`b33:5`, the `encryptionsalt` line, is not printed). The passphrase sentence of BRIEF S13 was cut for length (BRIEF trim order, item 4).
SAY: Stack init answers created stack dev, and config set writes your project into Pulumi dot dev dot yaml.

SHOW: CODE(src/deployment/deploy_images/__main__.py: 9–15): line 13 YELLOW (`timestamp_tag =
datetime.datetime.now().strftime("%Y%m%d%H%M%S")`), lines 14–15 PINK (`repository_name`,
`registry_url`). **V6 `TimestampPipe`** starts: three Dockerfiles become TEAL crates on a conveyor.
SAY: Now the program. Line 13 makes a timestamp, down to the second, and lines 14 and 15 build the registry address.

SHOW: CODE(src/deployment/deploy_images/__main__.py: 23–32): lines 23–25 (`docker_build.Image`,
the tag) YELLOW, line 28 `platforms=[docker_build.Platform.LINUX_AMD64]` PINK, line 29 `push=True`
GREEN, line 31 `retain_on_delete=True` GOLD; on "Lines 34 and 35" the panel scrolls to
CODE(src/deployment/deploy_images/__main__.py: 33–35), lines 34–35 `pulumi.export(…)` GREEN. V6: each crate
is stamped with a timestamp tag and shelved; `pulumi.export` copies the stamp onto a ticket. On
"Apple silicon", a GREY chip with a small chip icon "Apple silicon → amd64 under emulation: slow"
beside line 28, and a BLUE VM chip "the VM is amd64".
SAY: Each image is one docker build Image resource: a timestamped tag, push true, retain on delete, and one platform, A M D 64. An Apple silicon Mac emulates that slowly. Lines 34 and 35 export the tag for the other project.

SHOW: TRACKER [P] 10 · extra. It types line 1 of `b34` (tag `extra · recording only`; folds) →
TERM(b34: 3–7, …, 30, 35, …, 41–43 wrap, …, 48): the five `Downloading plugin` lines collapse into
one PURPLE chip "5 providers", `+ docker-build:index:Image build-cheese-app-frontend-react create`
GREEN, `warning: Skipping preview build because some inputs are unknown.` YELLOW, the stamped tag
(the `ac215-project` part with `default_tag`, the timestamp YELLOW), `+ 2 to create`. V4 small: a
padlock "unknown" on one card; a GREY "no build in a preview".
SAY: The extra preview, frontend only: five provider plugins, one image to create with its timestamped tag, and a warning: skipping preview build. A preview never builds.

SHOW: It types line 1 of `b35b` (tag `extra · recording only`; folds) → TERM(b35b: 5, …, 141, …, 170,
205, …, 223, …, 260 wrap, …, 293–295): `#13 DONE 71.1s` (npm ci), `✓ Compiled successfully`, `#17
DONE 54.2s`, `pushing layers`, then the Diagnostics line ending `403 Forbidden` RED, `2 errored`. V6:
the crate is built, then bounces off a RED padlock on the registry shelf. A GREY chip "with your key +
the repository from S11 → the tag lands". TRACKER [P] 10: a YELLOW `▶ your turn` beside the README's
`pulumi up --stack dev --refresh -y` (from block 5, shown again as a GREY ghost line).
SAY: Up does build: the npm install, the Next.js build, then the push, which fails here with 403 forbidden. Yours builds all three images, slowly, and ends with each tag in the outputs. Pause and run it.

SHOW: The YELLOW sticky note "hold that thought" from S09 returns. V6: a second `up` stamps three NEW
crates with a later timestamp beside the first three; the shelf grows; a GOLD `cost_tag` "registry
storage · grows with every changed layer". Fade; empty frame.
SAY: Remember the earlier question? This stack breaks the rule: each up rebuilds the images, because the timestamp is new every run. Each run can add image layers to the registry, and storage costs money.

---

## S14 · Steps 3–4: the VM, its fences, provisioning — `s14_vm_stack.py` · `VmStack`

SHOW: No tracker for this block. LECTURE 20 · 19, 22. The six-step strip: chips 1–2 ticked, chip 3
"VM · create_instance.py" YELLOW; it shrinks away. V1 at slide 22: the empty BLUE VM panel appears on
the right, a BLUE disk cylinder under it on a cable labelled `/mnt/disk-1`; a GREY-dashed "NFS"
label on the cable flips to "attached disk" (GREY `erratum` dot); the GREY-dashed models bucket
stays dim.
SAY: Step 3: create the VM. The slide draws a network share beside it; in this code that is a second disk, mounted at mnt disk 1.

SHOW: TRACKER [P] 11. Terminal `laptop · toolbox`. A GREY chip "README:349 · cd into deploy_single_vm"
types `cd ../deploy_single_vm` (no output panel). Then, fast, one 3-line panel each: `pulumi stack
init dev` → TERM(b18: 2); the three `pulumi config set …` lines (b19-1, b19-2, b19-3: line 1 each,
`sa_…` masked, `ac215-project` with `default_tag`) → each TERM(…: 2); TRACKER [P] 12: `pulumi preview
--stack dev --refresh` → TERM(b20: 2); `pulumi up --stack dev --refresh -y` → TERM(b21: 2). All the
same RED line, stacked.
SAY: Change into deploy single VM, then stack init, three config sets, preview and up: without the bucket login, each prints the same error.

SHOW: TRACKER [P] 11 · extra. On the local backend (`extra`): `pulumi stack init dev` → TERM(b40: 2);
the three `config set` lines (b41-1, b41-2, b41-3: line 1 each) → no output; `pulumi config` →
TERM(b42: 2–6): `security:ssh_user  sa_000000000000000000000` YELLOW ("from S12, masked"),
`security:gcp_service_account_email  deployment@ac215-project…` PINK ("the account the VM runs as"),
`gcp:project` with `default_tag`. The `default_tag` also sits on the `ac215-project` inside the email,
on the typed `b41-3` line and on `b42`. A YELLOW `▶ your turn`.
SAY: On the local backend, the config shows the project, your masked username, and the account the VM runs as: deployment at your own project, not the README's. Pause, set all three, and check them with pulumi config.

SHOW: CODE(src/deployment/deploy_single_vm/__main__.py: 15–26): lines 15, 18, 21–23, 26 light in
order, each with a small chip of its slide-19 step: "3 VM", "4 Provision", "5 Containers", "6 Web
server".
SAY: The main file makes four calls, in the lecture's order: create the instance, provision it, set up the containers, set up the web server.

SHOW: **V7a `VmFences`**: a BLUE VPC outline `cheese-app-network` (a GREY chip "same name as part
1's Docker network, now a cloud network"); three PINK gates on its edge, one per phrase: "80 ·
http-server", "443 · https-server", "22 · every VM" (from `create_instance.py:51-89`, small GREY
reference).
SAY: Create instance builds the fences first. There is a cloud network, also called cheese app network, and three firewall gates: 80 and 443 for the tagged VMs, 22 for every VM.

SHOW: CODE(src/deployment/deploy_single_vm/create_instance.py: 92–103): lines 92–97 (the disk, `size`,
`pd-standard`) BLUE, lines 100–103 (`gcp.compute.get_image(family="ubuntu-2204-lts", …)`) YELLOW. V7a:
a disk cylinder appears; the VM wears the two tags, plugs in the disk; a sealed PINK envelope
`<instance_ip>` hangs on it, labelled "Output: opens when the VM exists".
SAY: Then a 50 gigabyte data disk, and a lookup of the newest Ubuntu image. The VM address is an output, a sealed envelope that opens once the VM exists.

SHOW: TRACKER [P] 12 · extra. It types `pulumi preview --stack dev --refresh` (local backend,
`extra`) → TERM(b43: 6–10, …, 21–22, …, 41 wrap, …, 44–45): the five `+ … create` lines GREEN (V7a
ticks Disk, Network, three Firewalls), `File "/app/deploy_single_vm/create_instance.py", line 100`
YELLOW, `Response: {"error":"invalid_grant" …}` RED, `+ 6 to create`, `1 errored`. The `get_image`
card in V7a goes RED.
SAY: The real preview plans a disk, a network and three firewalls, then stops at line 100, invalid grant: the image lookup is the first call needing Google. Yours goes on to about thirty resources.

SHOW: A YELLOW card "check the plan before -y" with a GREY example line "~ gcp:compute:Instance …
replace" (labelled "illustration of what to look for", not output). A GOLD `cost_tag`: "VM n2d-standard-2
≈ $2/day · boot + data disks · external IP · roughly: check the pricing calculator". TRACKER [P] 12:
a YELLOW `▶ your turn` beside a GREY ghost of `pulumi up --stack dev --refresh -y`.
SAY: Check the plan before dash y: a newer Ubuntu image can turn the next up into a VM replacement. Then pause and run up. From here it costs roughly two dollars a day, plus disks and an address.

SHOW: LECTURE 20 · 14, 19. The six-step strip returns: chip 3 ticked, chip 4 "Provision ·
provision_instance.py" YELLOW, with a GREY chip "no slide draws this step". V4's banner "Pulumi
manages infrastructure through cloud APIs" returns and gains a GREY footnote "… and SSH, for the
inside of the VM". **V7b `ProvisionDominoes`**: nine numbered tiles with short labels (≤ 8 characters, ≥ 20 pt), in
two rows snaking 5 + 4 with a `depends_on` arrow at the turn (1 format · 2 mkdir · 3 mount · 4 timers ·
5 upgrade · 6 packages · 7 Docker · 8 pip · 9 group), joined by `depends_on` arrows, fall in order.
SAY: Step 4, provisioning, has no slide picture: it happens inside the VM, over SSH. Nine remote commands run in a chain: format and mount the disk, update, install Docker.

SHOW: CODE(src/deployment/deploy_single_vm/provision_instance.py: 24–31): line 29 YELLOW, the part
`blkid -o value -s TYPE …` GREEN and `|| mkfs.ext4 …` RED-outlined. Caption: "Pulumi remembers that
a command ran, not what it changed". (The domino replay belongs to the ponder answer.)
SAY: Pulumi remembers that a command ran, not what it changed. Look at the first one: block ID checks for a filesystem, and only if there is none, make file system formats the disk.

SHOW: The panel and dominoes dim; the first tile alone at the centre.
SAY: A question. Why check with block ID first, instead of just formatting the disk?
PONDER(8 s, "Why blkid … || mkfs.ext4\ninstead of just mkfs.ext4?")

SHOW: V7b replay: the tiles stand up again; the first tile refuses to fall (a GREEN check "has a
filesystem"). Then a GHOST replay: without the guard, the tile falls onto the disk cylinder, which
empties (its two GREY labels "chat history", "model" vanish, RED). Then the guarded tile again, disk
intact, GREEN. Caption: "scripts must be safe to run twice". Fade; empty frame.
SAY: Because formatting erases. If this step ever ran again, after a new trigger or a replaced resource, plain formatting would wipe the data disk: the chat history and the model. Scripts Pulumi cannot inspect must be safe to run twice.

---

## S15 · Steps 5–6: containers over SSH, then test — `s15_containers.py` · `ContainersOverSsh`

SHOW: No tracker for this block. LECTURE 20 · 19. The six-step strip: chips 1–4 ticked, chip 5
"Containers · setup_containers.py" YELLOW; it shrinks away. CODE(src/deployment/deploy_single_vm/
setup_containers.py: 27–31): line 27 `pulumi.StackReference("organization/deploy-images/dev")` PINK,
lines 29–31 GREEN. V6 returns: the ticket with the timestamp slides through a PINK pipe labelled with
the stack name, from the images stack to the VM stack.
SAY: Step 5: the containers. The VM program asks the images stack for its tags, through a stack reference to organization, deploy images, dev. So run up in deploy images first.

SHOW: CODE(src/deployment/deploy_single_vm/setup_containers.py: 79–90): line 81 `host=… f"ssh://{ssh_user}@{ip}"`
PINK, lines 84–85 `"-i", "/secrets/ssh-key-deployment"` PURPLE. A PINK tunnel runs from the GREY
laptop to the VM: "Pulumi → SSH → the VM's Docker". TEAL container cards on the laptop side get GREEN
"+" glyphs, as in V4.
SAY: Then a Docker provider whose host is SSH, with your key, so each container on the VM is a resource Pulumi can compare and replace.

SHOW: LECTURE 20 · 23. V1 at slide 23: a GREY arrow from the registry to the VM; three TEAL boxes
appear: `frontend` with a GREY ghost label "HTTP 80" that flips to PINK "3000" (GREY `erratum` dot),
`vector-db · 8000`, `api-service · 9000`; the dashed TEAL `vector-db-loader` appears, pours dots into
`vector-db`, and fades. A GREEN cable `appnetwork` joins them. A GREY `erratum` dot on `vector-db`
with the chip "same mount slip as part 1: data in /data, not on the disk" (`setup_containers.py:150–155`
mounts `/chroma/chroma`).
SAY: Three containers appear: the frontend, the vector database on 8000, the API on 9000. The slide puts the frontend on 80; the code, on 3000.

SHOW: LECTURE 20 · 24. The strip flashes chip 6 "Web server · setup_webserver.py" YELLOW. A TEAL
`nginx` box appears at the top of the VM; the PINK "HTTP 80" door slides from nowhere onto it; the
request arrows draw in (browser → nginx → frontend / api-service → vector-db). Two GREY ghost doors
"3000" and "9000" on the VPC wall stay shut, RED.
SAY: Step 6: the web server. The nginx container appears on top, and port 80 moves onto it.

SHOW: CODE(src/deployment/deploy_single_vm/setup_webserver.py: 44–55): line 45 `checksum =
file_checksum(…)` YELLOW, line 53 `triggers=[nginx_conf_asset, checksum]` GREEN. A small `nginx.conf`
file icon gets edited (one line changes YELLOW); only three tiles "upload · move · restart" replay,
the rest stay still.
SAY: Its config file is uploaded with a checksum as a trigger. Change nginx dot conf, and only these steps run again.

SHOW: A GREY-outlined panel (tag `illustration`, never a terminal): "a successful pulumi up · drawn
from the code" (`create_instance.py`, `setup_containers.py`, `setup_webserver.py` logical names):
the finished V1 picture lights GREEN in five layers: fences, disk + VM, one chip "9 provision steps",
containers, nginx; then an end card with the six export names
(`__main__.py:29-34`): `instance_name`, `instance_ip: <instance_ip>`, `zone`, `persistent_disk_name`,
`ssh_user: sa_000…`, `ssh_command`.
SAY: No successful pulumi up was captured. So here is what it builds, drawn from the code. It ends on six outputs, among them the instance IP.

SHOW: The end card's `ssh_command` row expands: CODE(src/deployment/deploy_single_vm/__main__.py: 34)
with a GREY `erratum` tag and a GREEN insert `-i /secrets/ssh-key-deployment` sliding into a copy of
the command.
SAY: A small slip: the exported SSH command leaves out the key. Add dash i slash secrets slash ssh key deployment.

SHOW: LECTURE 20 · 25–26. The finished V1 picture; slide 26's three callouts drawn as RED-dashed
bubbles with numbered PINK circles: 1 on the laptop's down arrow `deployment.json` "create VM, SSH";
2 on the registry → VM arrow `gcp-service.json` "read images"; 3 on the GREY-dashed models bucket link
`gcp-service.json` "read models".
SAY: The lecture marks the job of each key: deployment creates the VM and logs in, the narrow key reads images and models.

SHOW: LECTURE (held). The two keys hover over the VM, BLUE-with-RED and GREEN, both dim.
SAY: A question. The running app needs one key. Which would you hand the VM, and why not the other?
PONDER(8 s, "The running app needs one key.\nWhich would you hand the VM,\nand why not the other?")

SHOW: LECTURE (held). The GREEN key slides onto the VM and lights; the BLUE key gets a RED "creates
VMs, disks, buckets" chip and moves back to the laptop.
SAY: The gcp service key: it reads images and stored objects and uses Vertex AI; it cannot create VMs, disks or buckets. Deployment can, which a compromised VM should never hold.

SHOW: LECTURE (held). Amendments, one per phrase: a small PINK arrow from the laptop's BLUE key to
callout 2 ("Pulumi pulls with your deployment credentials"); the VM outline gets a RED-rimmed BLUE
badge `deployment@…` with a GREY "scopes" fence around it (README:355); a new PINK arrow
`api-service → Vertex AI` labelled with the GREEN key `gcp-service.json`. A GREY chip "this repo: the
VM runs as deployment · try the narrow one → exercises".
SAY: Two footnotes. This repository pulls the images with your deployment credentials and runs the VM itself as deployment, capped only by scopes, a list of what the VM may call. And the API calls Vertex AI with the narrow key. Try the narrow one as an exercise.

SHOW: LECTURE 20 · 27. The picture's title becomes "Test the App". A GREY browser window (tag
`illustration`) at `http://<instance_ip>/`: the schematic home page with its footer row "Frontend
version · API version" (the API version cell YELLOW, a PINK chip "from /status"). V3 replays small
on the VM: the tile passes the 80 gate, the scissors snip, the 3000 / 9000 gates stay shut.
SAY: The lecture's last step: test the app. Open your instance IP; the footer shows the API version from slash status.

SHOW: TRACKER [P] 13. Terminal `cheese-app-vm` (a GREY chip "our part 1 stand-in · same names except
vector-db"). It types `sudo docker container ls` → TERM(vm/52: 2–6), the last NAMES cell
`cheese-app-vector-db` YELLOW beside a GREY ghost "Pulumi: vector-db". Then `sudo docker container
logs api-service -f` → TERM(vm/53: 2, …, 26, …, 53–56, 59) (`^C` YELLOW: "Control C stops
following"; a GREY chip beside lines 54–56: "uvicorn logs the path with --root-path /api-service
added back (vm/37:20)"); `sudo docker container logs frontend -f` → TERM(vm/54: 2, 7–9) and `sudo docker container
logs nginx -f` → TERM(vm/55: 9–11, 15), typed fast.
SAY: On the VM, through the console's SSH button or the fixed SSH command, the README checks: list the containers, follow each log, Control C to stop. Our stand-in names the database cheese app vector db.

SHOW: It types `sudo docker exec -it api-service /bin/bash` → TERM(vm/56: 2–6) (the id in the
prompt GREY); `sudo docker exec -it nginx /bin/bash` → TERM(vm/57: 2–5): `nginx version:
nginx/1.30.6` with `at the time of recording`. A small GREY note card: "chat: GENERATIVE_MODEL in the four
llm_*_utils.py files → a model Vertex AI lists as available · then up in deploy_images and
deploy_single_vm" (no chat answer shown). A YELLOW `▶ your turn`. Fade; empty
frame.
SAY: Exec into api service and into nginx. One note: chat needs a Gemini model Vertex AI still serves; change it in the API's helper files, then run up in both projects.

---

## S16 · Destroy, recap, and what's next — `s16_recap.py` · `Recap`

SHOW: LECTURE 20 · 29. No tracker for this block. A GOLD card in the centre, words only (no picture):
"Don't forget to delete". GOLD meters beside it: VM, disks, IP, registry, bucket.
SAY: The lecture ends with a slide of its own: don't forget to delete.

SHOW: TRACKER [P] 14. Terminal `laptop · toolbox`, prompt in `…/deploy_single_vm#`. It types `pulumi
destroy --stack dev --refresh -y` → TERM(b22: 2) RED; TRACKER [P] 14 · extra: the same command on the
local backend (`extra`) → TERM(b45: 2, 6, 10, 12 wrap, 13): `Previewing destroy`, `Destroying`,
`Duration: 1s`, "The resources in the stack have been deleted, but the history and configuration …
are still maintained." A YELLOW `▶ your turn` beside the typed README `pulumi destroy` line.
SAY: In deploy single VM, run pulumi destroy, stack dev, refresh, dash y. Pause and run yours. Ours shows the login error; on the local backend, with nothing to delete, it finishes in a second.

SHOW: V4 plays backwards on the finished V1: RED `-` glyphs pop and the parts fade in reverse order,
one per phrase: the containers (through the PINK SSH tunnel), the VM, the disk, the firewalls, the
network.
SAY: Destroy plays the graph backwards: the containers over SSH, then the VM, the disk, the firewalls and the network.

SHOW: Two folder cards: `deploy_single_vm` (GREEN tick "destroys the VM") and `deploy_images`
(YELLOW "only forgets the images"); V6's shelf of crates stays, each with a small GOLD padlock
`retain_on_delete`. GREY `erratum` tag "the README doesn't say which folder".
SAY: Run it in deploy single VM; in deploy images it only forgets the images, which stay in the registry, retained on delete.

SHOW: No tracker. A GOLD teardown checklist, items ticking one per phrase: "1 `pulumi destroy --stack
dev --refresh -y` in deploy_single_vm · the VM list is empty", "2 `gcloud artifacts repositories
delete cheese-app-repository --location=us`" (GREY card, tag `extra`, no output panel: not run), "3
`gcloud storage rm -r gs://your-gcp-project-pulumi-state-bucket` · last" (GREY card, tag `extra`, no
output panel; the name from `docker-shell.sh:17`).
SAY: Your teardown checklist. One: destroy the VM stack, and check the VM list is empty. Two: delete the registry repository with gcloud. Three: the state bucket, last, once no stack holds anything.

SHOW: The checklist continues: "4 the part 1 VM, if it still runs", "5 Docker Hub images · free,
optional", "6 the two service-account keys, when the course ends".
SAY: Four: the part 1 VM, if it still runs. Five: your Docker Hub images, free and optional. Six: when the course ends, both service account keys.

SHOW: LECTURE 20 · 19. The checklist shrinks away. The six-step strip at full width, each chip with
its file; above it V1 grows in time-lapse, one layer per chip (setup → registry → VM → provisioning
tiles → containers → nginx and the browser).
SAY: The recap is the lecture's six steps, each with its file: docker-shell.sh, deploy images, create instance, provision instance, setup containers and setup webserver.

SHOW: LECTURE 20 · 12. The six principles (moved here from S09) appear as six GREY chips, then become a
scorecard: "real languages ✓", "declarative ✓",
"state & previews ✓" GREEN; "components ✗", "tests ✗" GREY; "multi-cloud" with a GREY chip "many
providers, one cloud".
SAY: The lecture also names six principles. Real language, declarative, state with previews: yes. Components and tests: not here. Many providers, but one cloud.

SHOW: LECTURE 20 · 4. The roadmap from S01 returns small; the single VM pulses RED "single point of
failure". GREY-dashed chips slide in along the bar: "L21 · CI/CD", "L22 · Kubernetes · same toolbox,
same images stack", "L23 · pulumi up in GitHub Actions".
SAY: One VM is a single point of failure. Lecture 21 automates builds and tests, lecture 22 moves to Kubernetes with this toolbox, and lecture 23 runs pulumi up from GitHub Actions.

SHOW: Clear. A YELLOW card "Test yourself · 1/5": "Trace `http://<instance_ip>/api-service/status`:
which gate, which container, which location block, and which character makes FastAPI see
`/status`?"
SAY: Test yourself. Trace your instance IP slash api service slash status: which gate, which container, which location block, and which character makes the API see slash status?

SHOW: One card on screen at a time: card 1/5 Transforms into 2/5, then 3/5, on the sentence
boundaries (`vo.wait_until`). Card 2/5: "What three things does `pulumi up` compare, what does
`--refresh` change, and what does `-y` skip?" Card 3/5: "Name the two service accounts, where each key
sits (laptop, VM), and what each may do."
SAY: What three things does pulumi up compare, what does refresh change, and what does dash y skip? Name the two service accounts, where each key sits, and what each may do.

SHOW: Card 3/5 Transforms into 4/5, then 5/5. Card 4/5: "Which of slide 19's six steps can Pulumi
inspect afterwards, and which does it only remember running? Why must those scripts be safe to run
twice?" Card 5/5: "What survives `pulumi destroy` in deploy_single_vm, and how do you clean it up?"
After card 5 fades: a GREY pointer card "answers: exercises.md · study guide". Fade; empty frame.
SAY: Which of the six steps can Pulumi inspect afterwards, and which does it only remember? What survives destroy? Answers are in the exercises and the study guide.

---

## Word count

`python -m explainer.script videos/ac215-l20-deployment-pulumi/script.md` (SAY words; re-run after
any edit). At ≈174 wpm: ≈24.7 min of narration, ≈31–33 min with typing, outputs, illustrations and
five ponder timers. Every scene is inside its BRIEF band (target ±15 %); S06 and S15 sit at the
edges of theirs.

| scene | words (BRIEF · band) | scene | words (BRIEF · band) |
| --- | --- | --- | --- |
| S01 Hook | 224 (210 · 179–242) | S09 DesiredState | 297 (320 · 272–368) |
| S02 TheGoal | 219 (240 · 204–276) | S10 TwoKeys | 219 (240 · 204–276) |
| S03 DockerHub | 244 (240 · 204–276) | S11 Toolbox | 316 (310 · 264–357) |
| S04 VmWithDocker | 258 (250 · 213–288) | S12 SshKeys | 202 (210 · 179–242) |
| S05 VectorDb | 227 (230 · 196–265) | S13 ImagesStack | 323 (320 · 272–368) |
| S06 ApiAndFrontend | 205 (240 · 204–276) | S14 VmStack | 358 (320 · 272–368) |
| S07 OnePublicDoor | 339 (310 · 264–357) | S15 ContainersOverSsh | 368 (320 · 272–368) |
| S08 ByHand | 189 (200 · 170–230) | S16 Recap | 308 (290 · 247–334) |
| **part 1** | **1,905** (1,920) | **part 2** | **2,391** (2,330) |

**Total 4,296** (series ceiling 4,300). The first three items of BRIEF's trim order are used: S03's
builder extra (block cut; `a03`–`a05` stay in ASSETS for exercises.md), S06's `vm/36` (folded into a
chip on the curl block), S09's principles (moved to S16's scorecard); S13's passphrase sentence was
already gone. Any later addition names its cut in the same scene; S15 is at its band's ceiling.
