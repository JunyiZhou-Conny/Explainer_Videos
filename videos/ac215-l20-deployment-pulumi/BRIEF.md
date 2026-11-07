# Brief · AC215 L20 — Deployment: the cheese app on one VM, by hand and then as code

This is the design of the video, written before the script. Series rules are in `docs/AC215_SERIES.md`.
Facts come from `digest.md` (the verified tutorial digest), `SLIDES.md` (the lecture deck with its
scene map) and `assets/` (real captures, see `ASSETS.md`). **Where the digest or the slides disagree
with the captures, the captures win.** The captures are newer: 2026-11-05, 22:06–23:42 UTC. Each
README command was run as written, on two fresh stand-ins:
- a Debian 12 machine for the VM (`vm/`, hostname `cheese-app-vm`, user `student`);
- an empty Docker engine for the laptop (`laptop/`, `docker:29.8.2-dind`, user `student`).

Conny, 2026-11-02: 「我还是需要每一节Lecture非常仔细的slide by slide然后github repo上一步一步的训练」.
So this is the **full follow-along**:
- the L20 deck (30 slides), slide by slide, wherever the tutorial applies it;
- every README step of the two cheese-app-v3 sections, in order:
  - "Deployment to GCP (Manual)", README:4-222;
  - "Deployment to GCP (Single VM Instance)", README:225-383;
  - the destroy step under "Delete the Compute Instance / Persistent disk", README:387-390.

| topic | digest / slides | captures (use these) |
| --- | --- | --- |
| which commit | `main` @ `3ecef56`; an unmerged staff branch exists | `git ls-remote` on the recording day (`p03`): `main` is still **`3ecef56`** (2025-11-28), and the course site links `main`. The staff branch moved again that day and rewrites the README. It is **context only**: ASSETS.md records it, and the video never names it. The video says once that the README may change and how to check the commit |
| `sh docker-shell.sh` | digest B3: it builds and logs in | **It does not build as committed.** First, Debian 11's security pool returns `404` (`b02`). Then, after fix 1 (`bookworm`, `b02a`), `google-cloud-sdk` has no installation candidate (`b02b`). With fix 2 (`google-cloud-cli`, `b02c`) it builds in 92 s (`b02d`). Both are one-line edits; the video shows each failure, then each fix |
| the public Part A images | digest gotcha 24: probably older than the code | confirmed: `/status` → **404** (`vm/34`); the image's `service.py` has `/square_root/` and no `ROOT_PATH` (`vm/36`); `/docs` is a real Swagger page (`vm/35`). On the manual VM the README's own API check (`/docs`) works |
| Chroma persistence | digest errata 21 (from Chroma's docs) | confirmed: `persist_path: "/data"` (`vm/25`). `docker-volumes/chromadb` stays **empty** (`vm/28`) |
| nginx.conf echo | digest errata 5 | confirmed: `log_format  main   - []` (`vm/45`), and every access-log line is `-[]` (`vm/51`). Routing works |
| a stopped frontend | digest gotchas 11/12 | reproduced: nginx `Exited (1)`, `host not found in upstream "frontend"`, `http://localhost/ -> 000` (`vm/58`). **This is the hook** |
| `docker buildx` builder gotcha | digest gotcha 3: local builds "disappear" | **not reproduced** on Docker 29 / buildx 0.37 (`a04`): a plain `docker build` still loads its result. Only `docker buildx build` without `--load` keeps it in the builder (the WARNING in `a02`). Say it as "older Docker versions"; `docker buildx use default` is still the tidy reset (`a05`) |
| `pulumi preview` | digest: preview shows the plan | real (`b34`): `+ create` lines and the timestamped tag, and **`warning: Skipping preview build because some inputs are unknown`**. A preview never builds; `up` does (`b35b`) |
| what stops each cloud step | digest assumes a key | the sandbox has **no Google account, no Docker Hub login**. Every cloud step stops at its honest first error. Pulumi is shown on its local file backend (extras, `b30`–`b46`) up to its first Google call: the push `403` (`b35b`) and `get_image` `invalid_grant` (`b43`) |
| `pulumi up` success output | digest: "about 30 resources, Outputs: instance_ip …" | **nothing records it.** Show an `illustration` of the resource graph built from the code (`__main__.py:29-34` export names), **never a terminal panel** |
| kubectl | Dockerfile pins 1.34 | `v1.35.9-dispatcher` (`b05`): gcloud's bundled kubectl comes first on `PATH`. One clause; kubectl matters in L22 |
| length | digest §8: ~30.5 min | the plan below is **~4,250 words ≈ 24.5 min of narration**, ~31–33 min with typing, outputs and five ponders |

## Audience and goal

The viewer is an AC215 student who has done L1–L18:
- a cloud VM, SSH, `apt`, and deleting the VM (L1–L2);
- Docker images, containers, `-p HOST:CONTAINER`, bind mounts, `docker-shell.sh`, Docker networks
  and container names (L2–L4);
- service accounts and JSON keys in `secrets/` next to the repo (L10, L15);
- Cloud Run, where Google ran the box for them (L14);
- the cheese app's four services running locally: API, frontend, vector DB and loader (L18).

They have seen Lecture 20 ("Deployment: Pulumi"). They watch with
[dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3) cloned next to their `secrets/`
folder, with Docker Desktop running, a GCP project with billing, and a Docker Hub account. They pause
to run each step. **Real money is involved**: a VM, two disks, an IP and registry storage (GOLD tags).

After the video they can:
- draw the lecture's target picture and explain every arrow: browser → port 80 → nginx → frontend:3000
  or api-service:9000 → vector-db:8000. They can say why only nginx faces the internet;
- deploy the app by hand: push images to Docker Hub, install Docker on a VM, create the folders, the
  network and the five containers (one of them a one-shot loader), then put nginx in front. They can
  read `docker container ls`, the logs and `exec` on the VM, and delete the VM afterwards;
- read nginx's `location` blocks and say which single character strips `/api-service`. They can
  explain why stopping the frontend takes the whole site down;
- explain what Pulumi does: run the program → desired state; compare with state and reality → plan;
  call providers → apply. They know what `preview`, `up`, `--stack`, `--refresh`, `-y` and `destroy`
  do, and what `-y` skips;
- set up the deployment toolbox:
  - enable the four APIs;
  - create the two service accounts and say what each key may do;
  - apply the two one-line Dockerfile fixes;
  - start `sh docker-shell.sh` and check the tools and `gcloud auth list`;
- set up SSH for Pulumi: OS Login, an `ssh-keygen` key with an empty passphrase, the key upload, and
  the `sa_…` username in the stack config;
- run both Pulumi projects in order (`deploy_images`, then `deploy_single_vm`), map each part of the
  output to slide 19's six steps and the file behind each one, and recognise each real error;
- tear down: `pulumi destroy` in the right folder, and know what survives it (registry images, the
  state bucket, the manual VM, the keys).

## Length and parts

The video runs ~31–33 minutes. Narration is 3,900–4,300 words (Kokoro af_heart, speed 0.9 ≈ 174 wpm).
The plan below totals **~4,250 words**. Word budgets per scene are targets (±15 %).

- **Part 1 = S01–S08** (~1,920 words, ~14 min): **by hand.**
  - The hook and the goal picture (slides 4–8).
  - The README's manual section from Docker Hub to nginx, on a fresh Debian 12 VM stand-in.
  - The tally of what we typed, and the teardown the README forgets (slides 9–11, 29).
- **Part 2 = S09–S16** (~2,330 words, ~18 min): **as code.**
  - Pulumi the tool (slides 10–18).
  - The setup: APIs, keys, the toolbox with its two fixes, SSH and OS Login (slides 19–20, 25).
  - The two Pulumi projects as slide 19's steps 2–6 (slides 21–27).
  - Destroy, the recap and the bridge (slides 15–16, 29, 4, 12).

The cut is the README's own seam and the deck's: Part A ends at "You can access the deployed API
using `http://<Your VM IP Address>/`" (README:222). The next section opens with "We will automate all
the deployment steps we did previously" (README:227), and slide 9 ("Deployment Automation") turns
the lecture there. Part 1 ends on S08's tally card, with the question "repeat, review, undo?" left
open. Part 2 answers it.

## Colours (series table, applied)

| meaning | colour |
| --- | --- |
| the laptop and everything on it: the browser, `secrets/` on the host, the host's Docker daemon, the deployment toolbox's outline ("Your Machine" on slide 14) | GREY |
| the cloud: GCP's outline, the Compute Instance (VM), the VPC, the persistent disk, Artifact Registry, the GCS state bucket, Compute Engine APIs, Vertex AI, Docker Hub (a cloud registry too) | BLUE |
| containers and images: `api-service`, `frontend`, `vector-db` / `cheese-app-vector-db`, the loader (dashed), `nginx`, `cheese-app-deployment` (the toolbox, inside its GREY laptop) | TEAL |
| shared or OS-owned: Debian's apt pools (`bullseye-security`, `archive.debian.org`), Google's apt repository, the default buildx builder, `0777` folders on the VM, the VM's system Docker | ORANGE |
| project-owned and pinned: `Pulumi.yaml`, `Pulumi.dev.yaml` and its config keys, the state file (`organization/<project>/dev`), timestamped image tags, `cheese-app-network` / `appnetwork` (the app's private LAN), `nginx.conf` from the repo | GREEN |
| tools: Docker / buildx / BuildKit, gcloud, Pulumi and its providers (gcp, docker, docker-build, command), kubectl, uv, `ssh-keygen` | PURPLE |
| errors and "don't": every honest first error (`404 Not Found`, `has no installation candidate`, `push access denied`, `invalid_grant`, `PULUMI_ACCESS_TOKEN must be set`, `403 Forbidden`, `[emerg] host not found`, `Conflict`), the mangled `log_format`, the README's broken steps, the powerful key where the narrow one belongs | RED |
| your turn, the README tracker, the thing to look at now, ponder timers | YELLOW |
| money: the VM, both disks, the external IP, Artifact Registry storage, the state bucket; the "Don't forget to delete" card (slide 29) | GOLD |
| routes and addresses: URLs, ports, `-p` doors, request arrows, firewall gates and network tags, the SSH tunnel, the `/api-service` prefix and its scissors, the `StackReference` pipe | PINK |
| the past and the future: L18's laptop run, L21–L23 (CI/CD, Kubernetes), slide items the repo does not use (the models bucket, "GCR", NFS) | GREY, dashed |

**Keys** (V8) use colour *by power*. `deployment.json` is a RED-rimmed BLUE key (admin: it can
create and delete everything). `gcp-service.json` is a GREEN key (narrow, read and run).
`ssh-key-deployment` is a PURPLE key (a shell on the VM).

**Request arrows** are drawn in the request direction (browser → nginx → services → vector DB). This
is the opposite of the slides' arrowheads; S02 says so once (SLIDES "Not counted").

## Running example

- **The VM** is a fresh Debian 12 machine standing in for the console-made VM. The prompt is
  `student@cheese-app-vm:~$`, as in `vm/00`. Say once, in S04: "our VM is a stand-in that we can record
  end to end; yours is the one you just made in the console, and every command is the same". Its one
  stand-in line, `WARNING: unable to enable the docker service` (`vm/02`, no systemd), is cropped. A
  single caption says that on a real VM, systemd starts Docker at that point.
- **The laptop** prompt comes from each capture: `student@laptop:~$`, then
  `…/cheese-app-v3/src/frontend-react$`, then `…/src/deployment$`. Inside the toolbox it is
  `root@<id>:/app#`; the container id is never read aloud.
- **The sandbox, said once (S01's follow-along beat), never apologised for again.** This recording
  machine has no Docker Hub login and no Google account. Everything that runs on a machine you own is
  real and complete. Every cloud step stops at its honest first error, and the narration says what
  yours prints instead ("with your key, this line says …"). That line is said, never shown as output.
  The one printed exception is `expected/oslogin-ssh-keys-add.txt`, the README's own snippet, tagged
  `expected`.
- **Pulumi's local backend (S13–S16)** is an `extra`, said plainly: "the README logs Pulumi into a
  bucket; we can't, so to show you the plan we point Pulumi at a local folder: `pulumi login
  --local`. Not in the README; don't run it, your bucket works." Every panel from `b30`–`b46` carries
  the `extra` tag.
- **Placeholders**:
  - `your-gcp-project` is the project (`b01`, `b07`).
  - The README's own `ac215-project` stays where a README command prints it (`b15`, `b19`, `b32`,
    `b41`, `b42`, `b35b`, `b43`). It gets a GREY tag, "the README's default · change to yours", as
    L08 did.
  - The `sa_…` number is **always masked** as `sa_000000000000000000000`: README:290-316, 354; `b19`,
    `b41-2`, `b42`; `Pulumi.dev.yaml:4`.
  - No IP is ever shown: the browser says `http://<instance_ip>/` and the curls are to `localhost`.
- **Versions, all "at the time of recording"**:
  - VM stand-in: Docker 29.9.3; Chroma server 1.0.0; nginx 1.30.6; frontend Next.js 15.0.2; loader and
    API on Python 3.12.12.
  - Laptop: Docker 29.8.2, buildx 0.37.2.
  - Toolbox: Python 3.13.18, uv 0.13.7, gcloud 592.0.0, Pulumi v3.274.0, kubectl v1.35.9.
  - Image sizes: API 5.07 GB, chroma 640 MB, frontend 232 MB, nginx 163 MB (`vm/60`); toolbox 2.61 GB
    (`b36b`).
- **Crops** (ASSETS "Things scenes must handle"):
  - `b02`: the `[IP: 172.17.0.1 38720]` column, which is the recording proxy.
  - `b02d`: its last two lines (the capture's session timeout).
  - `b14`: everything after "…log in with your browser, or".
  - `vm/02`: the systemd WARNING.
  - Never read aloud: digests, container and network ids, the fingerprint and randomart of `b10`, or
    timestamps (say "a timestamp, year-month-day-hour-minute-second").

## Visual set pieces (the 3Blue1Brown part)

The class names go in `scenes/common.py`. None of them collides with a scene class in `video.yaml`.

- **V1 · `MasterDiagram` — the lecture's deployment picture, grown step by step.** Slides 7, 21–24, 26
  and 27, re-drawn in series style. This is the spine of the video, used in S01, S02, S04–S07, S10,
  S13–S16.
  - **Layout.**
    - Top left: a GREY "Your Machine" box with an "IDE / CLI" bar and dashed TEAL container squares.
    - Right: a dotted BLUE GCP outline. Inside it, bottom left, a BLUE Artifact Registry panel with
      three image bars. On the right, the BLUE Compute Instance (VM) panel. Below the VM, a BLUE disk
      cylinder joined to it by a *cable*, labelled `/mnt/disk-1` (not NFS, SLIDES Conflict 5).
    - The slide's GCS "Models" bucket is drawn GREY dashed with the caption "v3 downloads its model
      from GitHub" (Conflict 4).
    - Beside the laptop, a GREEN-and-BLUE *state bucket*, which the slides never draw.
  - **Build order, the deck's own:**
    - 21: the registry receives the developers' arrow; the right half of GCP is empty.
    - 22: the empty VM appears with its disk.
    - 23: three TEAL boxes appear: API 9000, Vector DB 8000, frontend **3000**. The slide's "HTTP 80"
      on the frontend is corrected in place to 3000 (Conflict 6). A dashed TEAL **loader** appears,
      fills the vector DB and vanishes (Conflict 7).
    - 24: nginx appears at the top. The PINK "HTTP 80" door moves from nowhere onto nginx, and the
      request arrows draw in.
    - 27: a GREY browser window on top: the test.
  - **Manual variant (Part 1).** The registry panel is Docker Hub (BLUE, "Docker Hub"); there is no
    state bucket and no VPC. Slide 8's four stages light in turn: Push · Setup VM · Deploy containers
    · Web server.
  - **Labels are today's**: "Artifact Registry" with a small GREY "(GCR on the slides)" the first time
    only (Conflict 1).
- **V2 · `NamePhoneBook` — containers find each other by name (S05, S06, S07).** The GREEN cable
  `cheese-app-network` runs inside the VM. A small phone book lists `cheese-app-vector-db`,
  `api-service`, `frontend`, `nginx`.
  - Each `docker run` plugs a TEAL box into the cable and writes a line in the book.
  - `-p` doors on the VM's wall are PINK: 8000, 9000, 3000, 80.
  - The loader (S05) knocks on `cheese-app-vector-db:8000` by name, pours 14,356 chunks in, and
    leaves (`--rm`).
  - The hook's answer (S07): nginx looks up `frontend` and `api-service` **once, when it starts**.
    When the `frontend` line is erased and nginx restarts, its lookup comes back empty, and nginx
    falls over (RED `[emerg] host not found in upstream "frontend"`). It takes the API's route down
    with it.
- **V3 · `ProxyRoute` — one public door, and the prefix scissors (S07, S15).**
  - A URL travels from the browser, `http://<VM IP>/api-service/status` (on the manual VM:
    `/api-service/`).
  - It passes the PINK firewall gate on port 80; the 9000 and 3000 doors in the VPC wall stay shut.
  - It reaches nginx, where two `location` blocks are signposts (`nginx.conf:35-44`, `:46-55`):
    `^~ /api-service/` and `/`.
  - On the API branch, scissors snip `/api-service`. The `/` at the end of
    `proxy_pass http://api-service:9000/;` is highlighted: "this one character replaces the prefix".
  - The rest of the URL walks on to `api-service:9000` and `{"message":"Welcome to AC215"}` comes back
    (`vm/49`). The other branch goes to `frontend:3000`.
  - In S15 the same picture plays on the Pulumi VM, with the firewall's three gates (80 / 443 / 22)
    from V7.
- **V4 · `EngineLoop` — desired state in, API calls out (slide 14; S09, S13, S14, S16).**
  - Top: a GREY "Your Machine" box. The program (`__main__.py`) runs and drops resource cards into a
    GREEN **desired** tree. Next to it sit two more trees: the **state** (a GREEN scroll from the
    bucket) and **reality** (BLUE cloud objects).
  - `--refresh` pulls the state tree into line with reality. The diff pops glyphs on the desired tree:
    GREEN `+`, YELLOW `~`, RED `-`, `+-`.
  - A PINK down arrow carries API calls to PURPLE provider plugs (gcp, docker-build, docker, command),
    which turn into cloud objects. Slide 14's banner, "Pulumi manages infrastructure through cloud
    APIs", is the caption. In S14 it gains a footnote: "… and SSH, for the inside of the VM" (Conflict 9).
  - `preview` stops after the glyphs. `up` asks "Do you want to perform this update?" (said, not
    printed; Gap 3), and `-y` answers it for you. `destroy` plays the graph backwards.
  - S13: in the preview, an image card shows an "unknown" padlock, and BuildKit is skipped (`b34`).
- **V5 · `ControlRoom` — the deployment toolbox and its wires (S11).**
  - A GREY laptop holds the TEAL `cheese-app-deployment` container. Coloured wires
    (`docker-shell.sh:34-43`) connect them:
    - the Docker socket → the laptop's daemon ("it builds on *your* Docker");
    - `src/deployment` → `/app`;
    - `../../../secrets` → `/secrets`;
    - `docker_config.json` → `/root/.docker/config.json` (credential helpers);
    - the three build contexts → `/api-service`, `/frontend-react`, `/vector-db`.
  - The env strip (`docker-shell.sh:13-17`, `b07`): `GCP_PROJECT`, region, zone,
    `GOOGLE_APPLICATION_CREDENTIALS`, `PULUMI_BUCKET`, and the empty `PULUMI_CONFIG_PASSPHRASE`.
  - Then the entrypoint's chain of five lamps (`docker-entrypoint.sh:10-27`): activate the key → set
    the project → registry helper → state bucket → `pulumi login`. In our run, lamps 1, 4 and 5 go RED
    with real lines from `b02d`; lamps 2 and 3 go GREEN. "With your key, all five are GREEN."
  - The Dockerfile's two RED lines (4 and 29-30) are drawn as the bricks that broke, each swapped for
    its fix.
- **V6 · `TimestampPipe` — two stacks joined by one fact (S13, S15, S16).**
  - Three Dockerfiles become crates on a conveyor. Each is stamped with a timestamp tag
    (`deploy_images/__main__.py:13`, real tag shape from `b34`) and shelved in Artifact Registry.
  - `pulumi.export(…-tags)` copies the stamp onto a ticket. The ticket slides through a PINK pipe,
    `StackReference("organization/deploy-images/dev")` (`setup_containers.py:27`), to the
    `deploy-single-vm` stack.
  - S13: a second `up` stamps new crates, because the stamp changes on every run (ponder 3's twist).
  - S15: the containers on the VM flip to show the new stamp.
  - S16: on `destroy`, the crates stay on the shelf with a small padlock: `retain_on_delete`, GOLD.
- **V7 · `VmFences` — the VPC, its gates and the disk, then the provisioning dominoes (S14).**
  - **Part a: the fences.**
    - The BLUE VPC `cheese-app-network` is drawn (the *same name* as Part 1's Docker network, now a
      cloud network: one sentence).
    - Three PINK gates: 80 opens only for VMs wearing the `http-server` tag, 443 for `https-server`,
      and 22 for every VM (`create_instance.py:51-89`).
    - A disk cylinder appears; the VM wears two tags and plugs the disk in.
    - The VM's IP is a sealed envelope (an `Output`). It opens only when the VM turns GREEN, and its
      address is drawn as `<instance_ip>`, never digits.
    - `b43`'s real plan ticks Disk, Network and three Firewalls with `+`. The `get_image` card then goes
      RED: "the first question that needs Google is: which Ubuntu image is newest?"
  - **Part b: the dominoes (step 4, which no slide draws).** Nine tiles, `provision_instance.py`'s
    `remote.Command`s, in their `depends_on` chain: format · mkdir · mount · stop apt timers ·
    upgrade · base packages · Docker CE · pip · docker group. They fall in order.
    - Replay: the first tile, `blkid … || mkfs.ext4`, refuses to fall, because the disk already has
      a filesystem.
    - Caption: "Pulumi remembers that a script ran, not what it changed: scripts must be safe to run
      twice."
- **V8 · `KeyRing` — three keys, three doors (S10, S12, S15).**
  - S10, slide 25 as a two-row card:
    - `deployment.json` opens "create / SSH / delete" doors (Compute Admin, OS Login, Artifact
      Registry Administrator, Kubernetes Engine Admin, Service Account User, Storage Admin);
    - `gcp-service.json` opens "read images, read models, call Vertex AI" (Storage Object Viewer,
      Vertex AI Administrator, Artifact Registry Reader).
    - The lecture's "your" is said with emphasis: your group's project, not the README's default.
  - S12: the PURPLE `ssh-key-deployment` key is cut. Its public half goes up to the service account's
    OS Login profile, which hands back a Linux username `sa_000…`.
  - S15, slide 26's three callouts on the finished V1, then the code's two honest amendments
    (Conflicts 2 and 3):
    - callout 2 (the image pull) gets a small PINK arrow from the *laptop's* deployment key: Pulumi's
      Docker provider pulls with your credentials;
    - the VM itself wears `deployment@…` (README:355), held back only by scopes;
    - a new PINK arrow, api-service → Vertex AI, carries `gcp-service.json`, the arrow slide 26
      leaves out.
  - Ponder 5 sits on this picture.

The **slide 19 six-step strip** is a small row of six numbered chips: Setup · Images · VM · Provision
· Containers · Web server. Each chip carries its file (`docker-shell.sh`, `deploy_images/`,
`create_instance.py`, `provision_instance.py`, `setup_containers.py`, `setup_webserver.py`). It opens
S10, S13, S14 and S15 with the current chip YELLOW and the earlier ones ticked, and it is the recap in
S16. It is not pinned through the scenes, so the README tracker and `lecture_ref` keep their corners.

## README step tracker (ReadmeTracker, top-left)

There is one tracker per README section, titled with the README's own heading. Steps the README
does not have are marked `extra` in the tracker caption and in the narration ("this one isn't in the
README"). Step titles are ≤ 3 words.

| tracker | README lines | steps |
| --- | --- | --- |
| **M · Deployment to GCP (Manual)** | 4-222 | Local check · Docker login · Push images · Create VM · Install Docker · Make folders · Secret file · Docker network · Vector DB · Load vectors · API service · Frontend · nginx.conf · Run nginx · Open site (15) |
| **P · Deployment to GCP (Single VM Instance)** + "Delete …" | 225-389 | Enable APIs · Service accounts · Run toolbox · Check tools · OS Login · SSH key · Upload key · Inventory (skip) · Images stack · Images up · VM stack · VM up · Check VM · Destroy (14) |

The extras, captured and marked `extra`:
- `vm/00`, `04`, `16`, `18`, `24`, `25`, `28`, `31`–`37`, `39`–`41`, `43`, `45`, `47`–`51`, `58`–`60`;
- `p01`–`p03`, `p05`;
- `a03`–`a06`;
- `b02a`, `b02c` (the fixes), `b07`, `b11`, `b13`, `b30`–`b46`.

`p04` is README 236-259's "copy this json file into the secrets folder", done by hand.

S01, S08's tally and S09 have no tracker. S16's recap has none after its Destroy step.

## Scene plan

Notation:
- `vm/NN` = `assets/terminal/vm/NN-*.txt`; `aNN`, `bNN`, `pNN` = `assets/terminal/laptop/…`;
  `expected/` = `assets/terminal/expected/`.
- Line 1 of a capture is the `$` command (typed, never printed); `[exit N]` is never printed.
- ▶ = a README step the viewer must do. A YELLOW `▶ your turn` tag appears at real checkpoints (about
  one per tracker group).
- CODE(path: a-b) quotes `assets/source/` with real line numbers, ≤ 12 lines on screen.
- `lecture_ref(20, "a–b")`, GREY, top right, **only while that slide's picture or idea is on
  screen**. Slide images never appear.

### Part 1 · By hand

**S01 · One container stops, the site goes dark (~210 words) — `s01_hook.py` · `Hook`.** Cold open,
no tracker.
- The broken thing, as real output, `vm/58`, trimmed to the `docker ps -a` table, the two `[emerg]`
  lines and `http://localhost/ -> 000`:
  - We stopped *one* container (the frontend) and restarted the web server.
  - The API is still `Up 10 minutes`, and so is the vector DB. Yet the whole site, API included,
    answers nothing.
  - The question stays on screen: *"The API is up. Why is the API's address dead too?"* It is
    answered in S07.
- V1 teaser (`lecture_ref(20, "7")`): the goal in ten seconds. The laptop's containers fly to one VM
  in GCP; port 80 is the only door. "Today we build this twice: by hand, then as code."
- `lecture_ref(20, "4–5")`, one beat: the roadmap's red box now sits on "Deployment, Scaling &
  Automation". Everything so far ran on your laptop; users need a server.
- How to follow along:
  - one repo, cheese-app-v3, with `secrets/` next to it;
  - a GCP project with billing (GOLD: this lecture costs money; S08 and S16 tear it all down);
  - a Docker Hub account;
  - the README tracker top-left, code panels with path and lines, `▶ your turn`; the study guide has
    every command.
  - The sandbox sentence (see "Running example"), said here once.

**S02 · From your laptop to one VM (~240) — `s02_goal.py` · `TheGoal`.** Tracker M 1.
- `lecture_ref(20, "7")`: V1 built from slide 7, in request order: browser → HTTP 80 → nginx →
  frontend 3000 / api-service 9000 → vector-db 8000.
  - Say once that the slides' arrowheads point the other way, and that we draw requests the way they
    travel.
  - The loader is the fifth container, dashed (Conflict 7): "the lecture lists the containers you talk
    to; two more do quiet work".
- `lecture_ref(20, "8")`: slide 8's four manual stages become the Part A map (V1 manual variant):
  Push · Setup VM · Deploy containers · Web server.
- ▶ M 1 "Local check" (README:10-16), narration plus a GREY laptop sketch: the three services from
  L18 run locally.
  - Kindly: the README's API check is `/docs`. On v3's code, `/status` → `{"version":"3.0"}` is the
    better check (digest A0, errata 4).
  - One sentence: L18 now teaches a refactored cheese-app-v2. Here you run v3's own `docker-shell.sh`
    scripts (digest §7).
- Which commit, in two sentences: we follow `main` at `3ecef56`, the commit the course site links.
  READMEs move: `git log -1` tells you which one you have (`p02`, extra, the branch list cropped).

**S03 · Images to Docker Hub (~240) — `s03_docker_hub.py` · `DockerHub`.** Tracker M 2–3.
`lecture_ref(20, "8")` (stage 1).
- The Docker Hub token page as an `illustration` (README:19): an access token, never its value.
- ▶ `a01`: `docker login -u <USER NAME> -p <ACCESS TOKEN>` typed as printed →
  `syntax error near unexpected token 'newline'` (RED).
  - Kindly: the angle brackets are part of the placeholder. To the shell, `<` means "read from a file".
    Replace them entirely.
  - Better still: `--password-stdin`, so the token stays out of your history (one line, no capture).
- CODE(`src/frontend-react/docker-hub.sh`: 11-35, two windows):
  - `DOCKER_USERNAME="dlops"` (11): change it to yours (errata 6).
  - `docker buildx create … --use` (27): a new BuildKit builder.
  - Two builds, the second with `--push`. Side by side, `src/api-service/docker-hub.sh:31,35`:
    `linux/amd64,linux/arm64` — one tag, two platforms. The frontend builds amd64 only.
- ▶ `a02` (frontend-react, README:28-31): `Docker Username: dlops`, `Creating new multi-arch
  builder...`, the three-stage build (first lines, `…`, `✓ Compiled successfully`), the WARNING "Build
  result will only remain in the build cache". Then the RED `push access denied … insufficient_scope`:
  "the script pushes to `dlops`, and we're not `dlops`; with your username and login, this is where it
  says pushed".
- The other two images (api-service, vector-db): the same script, two platforms, with no capture here
  (no arm64 emulation, a 5 GB TensorFlow image). "Run all three, then check your Docker Hub page."
  `▶ your turn`.
- Extra, one beat (`a03`, `a05`): `--use` made `multi-arch` your current builder. On older Docker,
  plain `docker build` results then "vanished". On today's Docker they don't (`a04`), and
  `docker buildx use default` is still the tidy reset.
- Shortcut: the README's later `docker run` lines use the public `dlops/…` images, so the VM part works
  even if you skip this. Those images are older than the code (S06 shows how we know).

**S04 · A VM with Docker, folders and a network (~250) — `s04_vm.py` · `VmWithDocker`.** Tracker M
4–8. `lecture_ref(20, "8, 22")` (stage 2; the empty VM).
- The console create form as an `illustration` (README:40-44): N2D, 50 GB disk, ✓ Allow HTTP traffic,
  ✓ Allow HTTPS traffic.
  - What the two ticks really do: they put the network tags `http-server` and `https-server` on the VM,
    which the default firewall opens for 80 and 443. This plants ponder 2.
  - GOLD tag: "billed while it runs; the disk while it exists".
  - The V1 VM panel appears, empty.
- SSH in. The stand-in sentence (see "Running example"); `vm/00` extra, shown briefly (Debian 12, no
  docker).
- ▶ `vm/01` (silent), ▶ `vm/02`: the `+ sh -c …` trace, first lines, `…`, last lines; Docker's apt
  repo for `bookworm`. ▶ `vm/03` `Docker version 29.9.3, build 5457199`. `▶ your turn`.
- ▶ `vm/10`–`15`: the six folder commands, typed fast, one tracker step.
  - README:54-59 lists them as bullets and again as a code block: run them once.
  - Extra `vm/16`: `drwxrwxrwx` root-owned. "`0777` is demo-grade: anyone on the VM may write here."
  - Run everything from your home directory: the later `$(pwd)` mounts depend on it.
- ▶ `vm/17`: `echo '<___Json Key___>' > secrets/gcp-service.json`. We ran it with the README's
  placeholder (extra `vm/18` shows the file holds just that). You paste your `gcp-service` key; never
  show it, never commit it.
- ▶ `vm/19` `docker network create cheese-app-network` → the GREEN cable of V2 appears (the id is not
  read).

**S05 · The vector DB and its loader (~230) — `s05_vector_db.py` · `VectorDb`.** Tracker M 9–10.
`lecture_ref(20, "7–8")`.
- ▶ `vm/20`–`23` (README:86-97): pull; `stop` and `rm` answer `No such container`, which is harmless
  thanks to `|| true` ("the README makes the step safe to re-run": the idea returns in S14); then
  `docker run -d`.
  - Each flag in one line: `--network`, `-p 8000:8000`, `--restart always`, the `-v` mount.
  - V2: the vector DB plugs into the cable.
- Extra `vm/24`: `0.0.0.0:8000->8000/tcp`, heartbeat, version `"1.0.0"`.
- Erratum, kindly (`vm/25`, `vm/28`): Chroma 1.x saves to `/data` (`persist_path: "/data"`), so the
  README's mount at `/chroma/chroma` stays empty. "Your data lives inside the container, not in the
  folder. Mount `/data` if you want it on the VM's disk." Low stakes: the loader reloads everything.
- ▶ `vm/26`, `vm/27` (README:103-112), the loader:
  - `-e CHROMADB_HOST=cheese-app-vector-db`: a name, not an address (V2's phone book);
  - `Python 3.12.12`, `download()`, `load()`, `Creating collection: recursive-split-collection`;
  - 11 `Processing file:` lines (first two, `…`, last) → **14,356 chunks**; it exits.
  - `-e GCP_PROJECT=ac215-project` gets the GREY "README's default" tag.
  - "No Google call: the embeddings were pre-computed; that's why our placeholder key did not matter."
  - The dashed loader in V2 pours and vanishes (`--rm`). `▶ your turn`.
- **PONDER 1** (8 s), then the answer.

**S06 · The API and the frontend (~240) — `s06_api_frontend.py` · `ApiAndFrontend`.** Tracker M
11–12. `lecture_ref(20, "7–8")`.
- ▶ `vm/30` (README:118-127): `Unable to find image … locally`, the pull, the id.
  - The flags that matter: two `-v` mounts (persistent-folder, secrets), `-p 9000:9000`, the key's
    path, `CHROMADB_HOST`.
  - `GCP_PROJECT=ac215-project` → the GREY tag. `GCS_BUCKET_NAME=cheese-app-models` is passed but
    never read (one clause).
  - `30b` is the same command (the capture-only re-run; never shown as a second step).
- Extra `vm/31` (logs): banner, `Loading CNN Model...`, `Uvicorn running on http://0.0.0.0:9000`.
  "The API downloads its CNN from a GitHub release every time it starts" (ASSETS capture-only note,
  one sentence; that is why slide 22's models bucket is drawn grey).
- Extra `vm/32`: the image is **5.07 GB** (GOLD disk chip).
- Extras `vm/33`–`35`: `curl localhost:9000/` → `{"message":"Welcome to AC215"}`; `/status` → RED
  `404`; `/docs` works. Extra `vm/36`: the image has `/square_root/` and no `/status`.
  - Kindly: "the public images are a few commits older than the code you cloned; with your own images
    from S03, `/status` answers."
- ▶ README:133-144, the interactive variant (`vm/38`): RED `Conflict. The container name
  "/api-service" is already in use`.
  - Kindly: it reuses the same name, so remove the running one first: `sudo docker rm -f api-service`
    (extras `vm/39`–`41` show it working: `app@<id>:/app$`, then the detached one again).
  - "Optional: it's the dev mode from L18."
- ▶ `vm/42` (README:150): frontend, `-p 3000:3000`. Extra `vm/43`: `<title>Formaggio</title>`,
  `▲ Next.js 15.0.2`, `BASE_API_URL: /api-service`. "Remember that last value: the page will call
  `/api-service/…` on whatever address it was loaded from."

**S07 · nginx: one public door (~310) — `s07_nginx.py` · `OnePublicDoor`.** Tracker M 13–15.
`lecture_ref(20, "7–8, 24")`.
- Why a reverse proxy: one address for the browser; ports 3000 and 9000 stay inside. V1 manual: nginx
  appears on top and port 80 lands on it (slide 23 → 24's move, told the right way: Conflict 6).
- CODE(`src/deployment/nginx-conf/nginx/nginx.conf`: 35-55), V3 on it: two signposts, the scissors,
  the trailing `/` of `proxy_pass http://api-service:9000/;`. Names resolve on the cable (V2).
- ▶ `vm/44` (README:156-213): silent. Erratum, kindly, with extra `vm/45` (`cat -A`):
  - The `echo '…'` wraps a file that has its own single quotes, so the `log_format` line came out as
    `log_format  main   - []`.
  - Routing is unaffected; the logs are useless (`vm/51`: `-[]`).
  - Fix: write it with a quoted heredoc, or copy the repo's `nginx.conf` with `scp`. One line each, no
    capture.
- ▶ `vm/46` (README:219): `-v …nginx.conf:/etc/nginx/nginx.conf -p 80:80`. Extra `vm/47`: four
  containers (80, 3000, 9000, 8000).
- ▶ "Open site" (README:222): the browser at `http://<Your VM IP Address>/` is a GREY `illustration`
  (home page, footer), with the curls beside it:
  - `vm/48`: `HTTP/1.1 200 OK`, `Server: nginx`, `<title>Formaggio</title>`;
  - `vm/49`: `/api-service/` → `{"message":"Welcome to AC215"}`. V3's scissors play over this line.
  - `▶ your turn`.
- **PONDER 2** (8 s) on the VM wall with its doors.
- The hook's answer, V2: `vm/58` again in context.
  - nginx looks up `frontend` and `api-service` when it starts. With the frontend stopped, the restart
    can't resolve it, `[emerg]`, exit 1, and the API's route falls with it.
  - `vm/59`: `docker start frontend nginx` → 200.
  - "Start order matters, and so does `--restart`" (the frontend's run has none; nor does Pulumi's,
    digest errata 10: exercise E7).

**S08 · Twenty-one commands: repeat, review, undo? (~200) — `s08_by_hand.py` · `ByHand`.** No
tracker until the teardown line. `lecture_ref(20, "9–11")`.
- The tally: README:48-219 shrink into a scrolling column of 21 commands on the VM (without the
  optional interactive one), plus console clicks and three `docker-hub.sh` runs. Each drops a block
  onto the V1 VM.
- Three questions pop over the tower:
  - Repeat: "same thing for staging, tomorrow?"
  - Review: "what exactly is on that VM?"
  - Undo: "how do I delete every piece?"
  - Slide 9's answer: too many steps to keep track of → automate.
- Slides 10–11 in one breath: infrastructure as code, in a real programming language (Python here),
  kept in git and shared, instead of YAML or a DSL. One line of course history: last year's version
  did these five stages as Ansible YAML playbooks; Pulumi maps onto them one to one (digest §7).
- **Teardown now** (errata 7, slide 29's spirit): the README never deletes this VM. Delete it in the
  console (`illustration`: VM instances → Delete, with "delete boot disk" ticked). GOLD meter stops.
  "Part 2 builds it again, as code." End of part 1.

### Part 2 · As code

**S09 · Pulumi: desired state, not steps (~320) — `s09_desired_state.py` · `DesiredState`.** No
tracker. `lecture_ref(20, "12–17")`.
- A program describes *what should exist*, not *what to do*. CODE(`deploy_single_vm/create_instance.py`:
  51-62): one firewall rule.
  - Its shape: a constructor (`gcp.compute.Firewall`), a logical name, arguments.
  - "The lecture's example is a storage bucket: same shape" (slide 17; its code is never shown).
  - Constructors only *register* resources: nothing is created while this line runs.
- V4 the whole way (slide 14):
  - run the program → desired tree;
  - load the state, and with `--refresh` re-read reality;
  - diff → plan glyphs;
  - API calls to providers → cloud objects. The banner caption.
- Slide 15 as a card: seven commands. The tutorial lights `stack`, `config`, `preview`, `up`,
  `destroy`, and `refresh` (as the `--refresh` flag); `new` is greyed ("both projects already exist").
- `lecture_ref(20, "16")`: decode `pulumi up --stack dev --refresh -y` flag by flag (V4).
  - `-y` skips the confirmation: "read the plan when it matters; S14 shows when".
  - `preview` stops before applying.
- The six principles (slide 12), named only; the recap scores them.
- **PONDER 3** (8 s), then the answer: nothing to do, the plan is empty. "Hold that thought for S13."

**S10 · Setup: four APIs, two keys (~240) — `s10_setup.py` · `TwoKeys`.** Tracker P 1–2.
`lecture_ref(20, "19–20, 25")`.
- The six-step strip appears with step 1, "Setup", YELLOW (slide 19). The V1 automated variant: the
  laptop box and an empty GCP outline.
- ▶ P1 (README:229-234): the four APIs as an `illustration` checklist (Compute Engine, Service Usage,
  Cloud Resource Manager, Artifact Registry). One clause: Vertex AI too, from earlier lectures, for the
  app's chat.
- ▶ P2 (README:236-259): the two service accounts as an `illustration` form with the README's role
  lists. Keys: JSON, renamed `deployment.json` / `gcp-service.json`. V8 two-row card (slide 25): one
  key builds, the other runs.
- Where the keys go: extras `p01` (clone), `p05` (tree) and `p04`: the folder `secrets/` *next to*
  `cheese-app-v3/`, three levels up from `src/deployment` (`docker-shell.sh:9`). `▶ your turn`.
- Erratum, kindly (digest errata 1): nothing creates the Artifact Registry repository that the images
  will be pushed to. Create it once, after S11 (the toolbox has gcloud):
  `gcloud artifacts repositories create cheese-app-repository --repository-format=docker --location=us`
  - It is tagged `extra · not in the README`, with no output panel ("look for `Created repository`").
  - "Skip it, and S13's push fails with `Repository … not found`."

**S11 · The deployment toolbox, fixed twice (~310) — `s11_toolbox.py` · `Toolbox`.** Tracker P 3–4.
`lecture_ref(20, "14, 19–20")` ("Your Machine" = this container).
- "Rather than each of you installing different tools…" (README:263): V5 introduces the container and
  its wires; CODE(`src/deployment/docker-shell.sh`: 9-17 then 34-43).
- ▶ `b01`: edit `GCP_PROJECT` (README:266-267; the README says "cd into `deployment`": it is
  `src/deployment`).
- ▶ `b02` `sh docker-shell.sh`, as committed. First lines, then three of the `404 Not Found`
  lines, `ERROR: failed to build`, and the RED `pull access denied`. The proxy column is cropped.
  - CODE(`src/deployment/Dockerfile`: 1-12): `FROM python:3.13-slim-bullseye`.
  - Kindly: Debian 11 has retired, and its security updates moved to an archive, so the tutorial's
    base image can't install packages any more. The script runs `docker run` anyway, hence the second
    error.
  - Fix 1, `b02a`: `bookworm`.
- ▶ `b02b`, again: steps pass until `Package google-cloud-sdk is not available … replace it:
  google-cloud-cli` / `has no installation candidate` (RED).
  - Fix 2: Google renamed the package. `b02c`'s real `git diff` shows the exact two-line change a
    student makes. `▶ your turn`.
- ▶ `b02d`, the third run: `[+] Building 91.9s (21/21) FINISHED`, then the entrypoint (V5's five
  lamps): `Python 3.13.18`, `uv 0.13.7`, the RED `invalid_grant: account not found` ("our key belongs
  to no account; yours activates `deployment@…`"), `Updated property [core/project]`, `Adding
  credentials for: us-docker.pkg.dev`, the bucket and `pulumi login` failures, then the prompt
  `root@<id>:/app#`.
  - The last two lines are cropped.
  - We also got `Bucket does not exist. Creating...`, but the create failed. "Yours creates the bucket
    the first time, then logs in."
- ▶ `b03`–`b05` (README:272-274), one panel: gcloud 592.0.0, Pulumi v3.274.0, kubectl v1.35.9 ("gcloud
  brings its own kubectl"). "At the time of recording."
- ▶ `b06` `gcloud auth list` → `No credentialed accounts.` "Yours lists `deployment@<your
  project>.iam.gserviceaccount.com` as active. If it doesn't, stop here: check the file name in
  `secrets/`."

**S12 · SSH keys and OS Login (~210) — `s12_ssh.py` · `SshKeys`.** Tracker P 5–8. No
`lecture_ref`: say once that "this is the one setup the slides skip".
- Why: Pulumi will log in to the VM over SSH to run scripts and drive Docker (S14, S15). Who logs in?
  The *service account*, through OS Login (V8, PURPLE key).
- ▶ `b08` (README:286), typed as printed: `bash: line 1: YOUR: No such file or directory`. It's the
  same `<…>` lesson as S03: replace the whole placeholder. ▶ `b09` (README:290; the README's default
  project tagged): `You do not currently have an active account selected.` "Yours prints `Updated
  […]`." (said only)
- ▶ `b10` (README:295-297): `cd /secrets`, `ssh-keygen -f ssh-key-deployment`, Enter twice, `cd /app`.
  - **Leave the passphrase empty**: Pulumi can't type one (digest errata 9).
  - The fingerprint and randomart are cropped. Extra `b11`: the two files now sit in your laptop's
    `secrets/`.
- ▶ `b12` (README:302): the honest error, then `expected/oslogin-ssh-keys-add.txt` (tagged
  `expected`, "the README's own snippet"), with `username: sa_000…` highlighted. "Copy *your*
  username: S14 needs it." `▶ your turn`.
- ▶ "Deployment Setup" (README:318-322), erratum, kindly: it asks you to edit `inventory.yml`.
  Extra `b13`: no such file. It belongs to last year's Ansible version → skip it. The Pulumi config in
  S14 replaces it.

**S13 · Step 2: images with timestamps (~320) — `s13_images.py` · `ImagesStack`.** Tracker P 9–10.
`lecture_ref(20, "13, 15, 18–19, 21")`.
- The six-step strip: step 2. V1 at slide 21: the laptop's arrow lands on Artifact Registry ("GCR on
  the slides"); GCP's right half is empty.
- Projects and stacks, the lecture's way (slide 18):
  - one program, three stacks (dev, staging, prod), each with its own state and config;
  - the tutorial has one, `dev`, inside two projects (`deploy_images/Pulumi.yaml`,
    `deploy_single_vm/Pulumi.yaml`). Its full name is `organization/deploy-images/dev`, and that name
    is load-bearing (Conflict 8: don't rename it).
  - The state lives in your bucket (V4's scroll).
- ▶ `b14` (README:332, `cd deploy_images`, `pulumi stack init dev`):
  - we never logged in (S11), so Pulumi offers its own cloud; crop after "or".
  - ▶ `b15`–`b17` (`config set` with the README's default tagged, `preview`, `up`): each prints RED
    `PULUMI_ACCESS_TOKEN must be set …`, which is the honest first error.
  - "With your bucket login these work; here is what they do."
  - The local-backend sentence (see "Running example") and extra `b30`.
- Extras `b31`–`b33`: `Created stack 'dev'`, the config.
  - `pulumi config set` writes `Pulumi.dev.yaml` in your checkout, which still holds the README's
    default until you change it.
  - The empty passphrase (`Dockerfile:51`) means stack secrets aren't really protected: who can read
    the bucket is what counts.
- CODE(`deploy_images/__main__.py`: 12-35): the timestamp (13), the registry URL (14-15), one
  `docker_build.Image` with `platforms`, `push=True`, `retain_on_delete` (23-32), the exports.
  - V6: crates stamped.
- Extra `b34` (preview, one image via `--target`): five plugins downloaded, `+ … Image … create`, the
  stamped tag (the README's default project tagged), and the YELLOW `Skipping preview build because
  some inputs are unknown`. V4: a preview never builds.
- Extra `b35b` (`up`): the real build inside `pulumi up` (`npm ci`, `next build`, `creating (133s)`),
  then the push → RED `403 Forbidden` ("no account here; with your key and the repository from S10,
  this is where the tag lands in the registry").
  - Under emulation on Apple Silicon, expect tens of minutes (`--platform` amd64: the VM is amd64).
- Ponder 3's twist: run `up` twice here and the images rebuild every time, because the stamp is a new
  timestamp on every run (V6). Each push adds GBs to the registry (GOLD).

**S14 · Steps 3–4: the VM, its fences, provisioning (~320) — `s14_vm_stack.py` · `VmStack`.** Tracker
P 11–12. `lecture_ref(20, "14, 19, 22")`.
- The six-step strip: step 3. V1 at slide 22: the empty VM and its disk.
- ▶ `b18`–`b21` (README:349-366: `cd ../deploy_single_vm`, `stack init`, three `config set`,
  `preview`, `up`), shown fast as one panel of the same RED line.
  - Then the local-backend extras `b40`–`b42`: the four keys; `security:ssh_user` is your `sa_` name
    from S12 (masked); `security:gcp_service_account_email` → the README sets it to the deployment
    account (S15 comes back to that).
  - `▶ your turn`: "your project, your `sa_` user".
- CODE(`deploy_single_vm/__main__.py`: 14-26): four calls in slide 19's order: create · provision ·
  containers · web server.
- V7a: the VPC, three gates and tags, the disk, the IP envelope. CODE(`create_instance.py`: 92-103):
  the disk, then `get_image(family="ubuntu-2204-lts")`.
- Extra `b43` (`preview`): `+ gcp:compute:Disk`, `Network`, three `Firewall`s, then
  `create_instance.py, line 100` … RED `invalid_grant`: "the first call that needs Google is the image
  lookup. Our plan ends here; yours continues to about thirty resources."
  - Reading the plan matters: a newer Ubuntu image can turn your next `up` into a VM *replacement*
    (Gap 3, digest gotcha 20). Read it before `-y`.
  - GOLD: VM ~$2/day, two 50 GB disks, an IP (digest §2, "approximate").
- Step 4 (the strip ticks on). The slides name it but draw nothing. V4's banner gets its footnote:
  "… and SSH" (Conflict 9). V7b dominoes. CODE(`provision_instance.py`: 24-31): the `blkid … ||
  mkfs.ext4` guard.
- **PONDER 4** (8 s), then the answer.

**S15 · Steps 5–6: containers over SSH, then test (~320) — `s15_containers.py` · `ContainersOverSsh`.**
Tracker P 13. `lecture_ref(20, "23–27")`.
- The six-step strip: steps 5–6.
- CODE(`setup_containers.py`: 27-31): the `StackReference` → V6's pipe delivers the tags.
- CODE(`setup_containers.py`: 79-98): a Docker provider whose `host` is `ssh://<user>@<ip>`. Pulumi on
  your laptop drives the VM's Docker through an SSH tunnel (PINK), so containers are real resources
  that can be diffed and replaced.
- V1 at slide 23: frontend 3000, vector-db 8000, api-service 9000, and the dashed loader. The network
  is now called `appnetwork`, and the vector DB is `vector-db`.
- V1 at slide 24: nginx; port 80 moves onto it. CODE(`setup_webserver.py`: 42-55): the config upload
  re-runs only when the file's checksum changes (`triggers`): "change `nginx.conf`, and only these
  steps replay".
- **The real result, honestly.** No recording exists of a successful `pulumi up`. An `illustration`
  shows the resource graph turning GREEN, built from the code, and ends on the six export names
  (`__main__.py:29-34`): `instance_name`, `instance_ip`, `zone`, `persistent_disk_name`, `ssh_user`,
  `ssh_command`.
  - Never a terminal panel.
  - Kindly: the exported `ssh_command` lacks `-i /secrets/ssh-key-deployment` (errata 16).
- `lecture_ref(20, "25–26")`: V8 on the finished picture with the amendments. **PONDER 5** (8 s),
  then the answer.
- `lecture_ref(20, "27")`, "Test the App":
  - the browser at `http://<instance_ip>/` (`illustration`);
  - V3 replays with the three gates;
  - the footer's `API version` comes from `/status`, which your images built from `3ecef56` have.
- ▶ "Check VM" (README:371-383):
  - `vm/52` `container ls`;
  - `vm/53` `logs api-service -f` with its `GET /api-service/ 200` lines (Ctrl-C to leave `-f`);
  - `vm/54`, `55` in one beat;
  - `vm/56` `exec … api-service` → `ls`;
  - `vm/57` `exec … nginx` → `nginx version: nginx/1.30.6`.
  - Kindly: these ran on the Part 1 VM stand-in, whose containers have the same names, except that
    Pulumi calls the vector DB `vector-db`.
  - One clause: chat needs a Gemini model Vertex AI still serves (the code's `gemini-2.0-flash-001` is
    retired, digest errata 20).

**S16 · Destroy, recap, and what's next (~290) — `s16_recap.py` · `Recap`.** Tracker P 14.
`lecture_ref(20, "29")` → `"15–16"` → `"19"` → `"12"` → `"4"`.
- The GOLD "Don't forget to delete" card (slide 29, words only).
- ▶ `b22` (README:389) → the same honest RED line. Then extra `b45` on the local backend: `Previewing
  destroy`, `Destroying`, and "The resources in the stack have been deleted, but the history and
  configuration … are still maintained".
- V4 plays backwards: containers (over SSH), VM, disk, firewalls, VPC.
- Kindly (errata 8): run it **in `deploy_single_vm`**. In `deploy_images` it only forgets the images:
  they stay in the registry (`retain_on_delete`, V6's padlock).
- Teardown checklist (GOLD), each line spoken:
  1. `pulumi destroy --stack dev --refresh -y` in `deploy_single_vm`; the VM list is empty.
  2. The registry images: delete `cheese-app-repository` in the console or with gcloud.
  3. The state bucket: last, once no stack holds anything.
  4. The Part 1 VM, if it still runs (S08).
  5. Docker Hub images (free, optional).
  6. The two service-account keys, when the course ends: long-lived credentials.
- Recap, slide 19 replayed: the six-step strip with each file under its chip, the V1 picture growing
  in time-lapse.
- Slide 12 as a scorecard:
  - ✓ real language, ✓ declarative, ✓ state and previews;
  - ✗ components, ✗ tests;
  - "many providers, one cloud".
- Bridge (slide 4's bar): one VM is a single point of failure. L21 automates (CI/CD), L22 swaps the VM
  for a Kubernetes cluster but keeps this toolbox and the images stack, and L23 puts `pulumi up`
  into GitHub Actions.
- Test yourself: the five recap questions, one at a time (answers in exercises.md). Point to the
  study guide.

## Word budget

| scene | words | scene | words |
| --- | --- | --- | --- |
| S01 Hook | 210 | S09 DesiredState | 320 |
| S02 TheGoal | 240 | S10 TwoKeys | 240 |
| S03 DockerHub | 240 | S11 Toolbox | 310 |
| S04 VmWithDocker | 250 | S12 SshKeys | 210 |
| S05 VectorDb | 230 | S13 ImagesStack | 320 |
| S06 ApiAndFrontend | 240 | S14 VmStack | 320 |
| S07 OnePublicDoor | 310 | S15 ContainersOverSsh | 320 |
| S08 ByHand | 200 | S16 Recap | 290 |
| **part 1** | **1,920** | **part 2** | **2,330** |

The total is ≈ **4,250** words ≈ 24.4 min of narration. Typing, the long outputs (`vm/02`, `vm/27`,
`a02`, `b02`, `b35b`), the illustrations and five ponder timers bring it to ~31–33 min. If the script
runs long, trim in this order:
1. S03's builder extra;
2. S06's `vm/36`;
3. S09's principles line;
4. S13's passphrase sentence.

Never trim a README command.

## Ponder questions

Five timed ponders, as Conny decided on 2026-10-21 (3–5 per video); REVIEW.md marks content gate 3
met with that decision. Each is quiz-style, with a YELLOW timer, and answerable from what was shown
just before it. The answer is said right after the timer.

| # | scene | question (as on the card) | answer |
| --- | --- | --- | --- |
| 1 | S05 (8 s) | "The loader ran with --rm\nand is gone.\nAre the 14,356 chunks gone too?" | No. The loader only *sent* them; they live in the vector-db container, which keeps running. (Caveat, from `vm/28`: inside the container, at `/data`, not in the folder the README mounts. Remove that container and they are gone, and the loader can refill it in a minute.) |
| 2 | S07 (8 s) | "Port 9000 is published on the VM.\nFrom your laptop, does\nhttp://<VM IP>:9000/ answer?" | No. The firewall only lets in what the VM's tags allow: 80 and 443 (S04's two ticks). 9000 is open on the VM but shut at the VPC wall. That is the point: one public door |
| 3 | S09 (8 s) | "You run pulumi up again,\nchanged nothing.\nWhat should the plan show?" | Nothing to do: desired = state = reality, so there is no diff and no API calls. (S13: this repo's image stack is the exception, because its tag is a new timestamp each run) |
| 4 | S14 (8 s) | "Why blkid … || mkfs.ext4\ninstead of just mkfs.ext4?" | `mkfs` formats: if the step ever re-runs (re-created resource, new trigger), it would wipe the data disk: Chroma's data, chat history, the model. The guard formats only a disk with no filesystem. Scripts that Pulumi cannot inspect must be safe to run twice |
| 5 | S15 (8 s) | "The running app needs one key.\nWhich would you hand the VM,\nand why not the other?" | `gcp-service`: it can read images and models and call Vertex AI, nothing more. `deployment` can create and delete everything in the project. A compromised VM should not be able to do that. Honest amendment: in this repo, the VM itself runs as `deployment` (README:355), limited by scopes. Try the narrow one (an exercise) |

## Recap questions (S16 "Test yourself"; answers in exercises.md)

1. Trace `http://<instance_ip>/api-service/status`: which gate, which container, which `location`
   block, and which character makes FastAPI see `/status`?
2. What three things does `pulumi up` compare, what does `--refresh` change, and what does `-y` skip?
3. Name the two service accounts, where each key lives (laptop, VM), and what each may do.
4. Which of slide 19's six steps can Pulumi inspect afterwards, and which does it only remember
   running? Why must those scripts be idempotent?
5. What survives `pulumi destroy` in `deploy_single_vm`, and how do you clean it up?

The digest's Q2 (timestamps) and SLIDES' "why keep two stacks of one program?" go to exercises.md.

## Errata and drift to state (kindly, with the fix)

1. **The toolbox doesn't build as committed (S11).** `FROM python:3.13-slim-bullseye`: Debian 11's
   security pool is gone (`b02`). Fix: `python:3.13-slim-bookworm` (`b02a`).
2. **`google-cloud-sdk` no longer installs (S11).** Fix: `google-cloud-cli` and
   `google-cloud-cli-gke-gcloud-auth-plugin` (`b02c`, the exact diff).
3. **Placeholders in angle brackets are shell syntax (S03, S12).** `docker login -u <USER NAME> …`
   (`a01`) and `--project <YOUR GCP_PROJECT>` (`b08`). Fix: replace the whole placeholder, brackets
   included; prefer `--password-stdin`.
4. **`DOCKER_USERNAME="dlops"` is hard-coded in `docker-hub.sh` (S03, `a02`).** Fix: set yours.
5. **Chroma 1.x saves to `/data` (S05, `vm/25`, `vm/28`).** The README's `/chroma/chroma` mount stays
   empty. Fix: mount `/data` if you want the data on the VM's disk.
6. **The public images are older than the code (S06, `vm/34`–`36`).** `/status` → 404. Fix: use `/`
   or `/docs` with them; build your own (S03) for `/status`.
7. **The interactive api-service collides with the detached one (S06, `vm/38`).** Fix: `sudo docker
   rm -f api-service` first.
8. **The nginx.conf `echo` mangles `log_format` (S07, `vm/45`, `vm/51`).** Fix: a quoted heredoc, or
   copy the repo's file.
9. **A stopped frontend takes nginx down (S01, S07, `vm/58`).** Fix: start the frontend before nginx;
   give it a restart policy (exercise).
10. **The README never deletes the manual VM (S08).** Fix: delete it in the console.
11. **The Artifact Registry repository is never created (S10, S13).** Fix: the one `gcloud artifacts
    repositories create … --location=us` line (`extra`, not run here).
12. **"cd into `deployment`" means `src/deployment` (S11).**
13. **ssh-keygen's passphrase must be empty (S12).** Pulumi can't type one.
14. **"Deployment Setup" / `inventory.yml` is an Ansible leftover (S12, `b13`).** Skip it.
15. **The README's `ac215-project` and `sa_…` values (S13, S14).** Replace them with yours; check with
    `pulumi config`.
16. **The exported `ssh_command` omits the key (S15).** Add `-i /secrets/ssh-key-deployment`.
17. **`pulumi destroy` doesn't say which folder, nor that images are retained (S16).**
18. **The code's Gemini model is retired (S15, one clause).** Chat fails until `GENERATIVE_MODEL` is
    updated.
19. **Slides vs repo** (SLIDES Conflicts, updated by the captures), each said once where its picture
    is:
    - GCR → Artifact Registry (S13);
    - frontend on 3000, not 80 (S07, S15);
    - a block disk at `/mnt/disk-1`, not NFS (S04, S14);
    - the models bucket → a GitHub release (S06);
    - five containers, not three (S02);
    - `dev` in two projects, not `cheese-app-dev` (S13);
    - "through cloud APIs" and through SSH (S14);
    - the key split vs the code (S15).
20. **Not errata, but drift said "at the time of recording":**
    - the builder gotcha no longer reproduces (S03);
    - kubectl comes from gcloud (S11);
    - a preview skips the build (S13).

## Costs and teardown

GOLD tags appear where a billable resource is created:
- the manual VM and its 50 GB disk (S04);
- the API image's 5 GB on disk (S06, a disk chip, not money);
- Artifact Registry storage, which grows on every `up` (S13);
- the Pulumi VM `n2d-standard-2` (~$0.08–0.09/h, ~$2/day), the boot and data disks (~$4/month
  together) and the external IP (S14);
- the state bucket (cents, S16).

Prices come from the digest's §2 table, are said as "roughly, check the pricing calculator", and are
never shown as exact. The teardown is in two places: S08 (the manual VM, now) and S16's checklist
(above).

## README commands checklist (for the follow-along review)

Every README instruction, verbatim, in README order per section.

| README instruction | README line | capture | scene |
| --- | --- | --- | --- |
| containers run locally (vector-db, `:9000/docs`, `:3000/`) | 10-16 | narration + sketch | S02 |
| Docker Hub account + Access Token | 19 | `illustration` | S03 |
| `docker login -u <USER NAME> -p <ACCESS TOKEN>` | 21 | `a01` | S03 |
| `sh docker-hub.sh` in `api-service` | 24-26 | not captured (two platforms; panel `api-service/docker-hub.sh:31,35`) | S03 |
| `sh docker-hub.sh` in `frontend-react` | 28-31 | `a02` | S03 |
| `sh docker-hub.sh` in `vector-db` | 33-35 | not captured (as api-service) | S03 |
| create the VM (N2D, 50 GB, HTTP/HTTPS) | 40-44 | `illustration` | S04 |
| SSH into the instance | 46 | the stand-in (`vm/00`) | S04 |
| `curl -fsSL https://get.docker.com -o get-docker.sh` · `sudo sh get-docker.sh` · `sudo docker --version` | 48, 49, 51 | `vm/01`–`03` | S04 |
| six folder commands | 54-68 | `vm/10`–`15` | S04 |
| `echo '<___Json Key___>' > secrets/gcp-service.json` | 74 | `vm/17` | S04 |
| `sudo docker network create cheese-app-network` | 80 | `vm/19` | S04 |
| vector-db: pull · stop · rm · run | 86-97 | `vm/20`–`23` | S05 |
| vector-db-cli: pull · run | 103-112 | `vm/26`, `27` | S05 |
| api-service `docker run -d` | 118-127 | `vm/30` | S06 |
| api-service interactive variant | 133-144 | `vm/38` | S06 |
| frontend `docker run -d` | 150 | `vm/42` | S06 |
| nginx.conf `echo` | 156-213 | `vm/44` | S07 |
| nginx `docker run -d` | 219 | `vm/46` | S07 |
| open `http://<Your VM IP Address>/` | 222 | `illustration` + `vm/48`, `49` | S07 |
| enable four APIs | 229-234 | `illustration` | S10 |
| service accounts `deployment`, `gcp-service`, keys → `secrets/` | 236-259 | `illustration` + `p04`, `p05` | S10 |
| cd `deployment` · change `GCP_PROJECT` · `sh docker-shell.sh` | 266-268 | `b01`, `b02` (+ `b02a`–`b02d`) | S11 |
| `gcloud --version` · `pulumi version` · `kubectl version --client` | 272-274 | `b03`–`b05` | S11 |
| `gcloud auth list` | 278 | `b06` | S11 |
| OS Login (template, example) | 286, 290 | `b08`, `b09` | S12 |
| `cd /secrets` · `ssh-keygen -f ssh-key-deployment` · `cd /app` | 295-297 | `b10` | S12 |
| `gcloud compute os-login ssh-keys add --key-file=/secrets/ssh-key-deployment.pub` | 302 | `b12` + `expected/oslogin-ssh-keys-add.txt` | S12 |
| Deployment Setup (`inventory.yml`) | 318-322 | `b13` (skip) | S12 |
| `deploy_images`: `pulumi stack init dev` · `pulumi config set gcp:project ac215-project` | 330-333 | `b14`, `b15` (+ `b31`, `b32`) | S13 |
| `pulumi preview --stack dev --refresh` | 339 | `b16` (+ `b34`) | S13 |
| `pulumi up --stack dev --refresh -y` | 344 | `b17` (+ `b35b`) | S13 |
| `deploy_single_vm`: `stack init` + three `config set` | 349-355 | `b18`, `b19` (+ `b40`–`b42`) | S14 |
| `pulumi preview --stack dev --refresh` | 361 | `b20` (+ `b43`) | S14 |
| `pulumi up --stack dev --refresh -y` | 366 | `b21` (+ `b44`) | S14 |
| open `http://<instance_ip>/` | 369 | `illustration` | S15 |
| `sudo docker container ls` · three `logs … -f` | 373-376 | `vm/52`–`55` | S15 |
| `sudo docker exec -it api-service /bin/bash` · `… nginx /bin/bash` | 381-382 | `vm/56`, `57` | S15 |
| `pulumi destroy --stack dev --refresh -y` | 389 | `b22` (+ `b45`) | S16 |

## Notes for script and scene authors

- **Shared code** (`scenes/common.py`, starting from L18's and L14's):
  - tracker factories `tracker_m` and `tracker_p` with the step lists above;
  - prompts per capture (`P_VM`, `P_LAPTOP`, `P_FRONTEND`, `P_DEPLOY`, `P_TOOLBOX`). The toolbox
    prompt is read from the capture line, never typed;
  - tags `your_turn`, `extra_tag`, `illustration_tag`, `expected_tag`, `cost_tag` (GOLD),
    `default_tag` ("the README's default · change to yours", GREY), `lecture_ref`;
  - a `six_steps(current)` strip; `browser_window(url, rows)` and `console_form(fields)` for the
    `illustration`s, with no logos;
  - set-piece classes `MasterDiagram` (V1, one layout with the stage methods `stage21()` …
    `stage27()` and a `manual=True` variant), `NamePhoneBook` (V2), `ProxyRoute` (V3), `EngineLoop`
    (V4), `ControlRoom` (V5), `TimestampPipe` (V6), `VmFences` + `ProvisionDominoes` (V7), `KeyRing`
    (V8).
- **Masking**:
  - the `sa_` number is always `sa_000000000000000000000`, applied to the capture text at load time
    (`b19`, `b41`, `b42`, README panels);
  - the instructor's name in `src/vector-db/cli.py:75`, `:440` is `‹instructor›`: better, keep those
    lines out of every panel;
  - the staff branch is never named.
- **The illustration of a successful `pulumi up` (S15)** is a resource graph, not a terminal. Its node
  labels come from the code's logical names (`create_instance.py`, `setup_containers.py`,
  `setup_webserver.py`), and its end card lists the six export names with `<instance_ip>`-style
  placeholders for the values.
- **Long outputs**:
  - `vm/02`, `vm/27`, `a02`, `b02` (the 404 column: three shown), `b02d`, `b34` (the plugin lines collapse
    to one), `b35b` (the build steps collapse; keep `DONE 70.3s`, `DONE 42.3s`, `creating (133s)`, the
    403), `b43` (the traceback collapses to `create_instance.py, line 100` + the `invalid_grant`
    response);
  - format: first lines, `…`, last lines.
- **`vm/53`'s log lines read `GET /api-service/ …`** although nginx stripped the prefix. The image's
  uvicorn runs with `--root-path /api-service` (`vm/37`), which only puts it back for logs and docs
  links. Say so in one clause, or show the lines without dwelling on the path.
- **Never read aloud**: digests, ids, timestamps, the key fingerprint, IPs (there are none), `[exit N]`.
- **Lexicon heads-up** (script stage):
  - names and tools: Pulumi ("PULL-oo-mee"), nginx ("engine-x"), Chroma, uvicorn, gcloud
    ("gee-cloud"), kubectl ("cube-control"), buildx ("build-x"), BuildKit, OS Login, Next.js;
  - code words: `sa_` ("S-A underscore"), `blkid` ("block-I-D"), `mkfs`, `fstab`, `appnetwork`,
    `--refresh`, `-y` ("dash Y");
  - versions and platforms: bookworm, bullseye, `n2d-standard-2` ("N-2-D standard 2"), `amd64`,
    `arm64`;
  - numbers: `0777` ("oh-seven-seven-seven"); ports 80, 443, 22, 3000, 8000, 9000 ("port eighty" …).
- **Chinese glossary heads-up**: stay English for VM, container, image, registry, Docker Hub,
  Artifact Registry, network, port, firewall, network tag, VPC, disk, nginx, reverse proxy, location,
  upstream, Pulumi, stack, project, config, state, backend, provider, resource, preview, refresh,
  destroy, Output, StackReference, service account, key, OS Login, SSH, passphrase, toolbox (工具箱 is
  fine in prose), timestamp tag. Reuse `../ac215-l14-serverless-deployment/i18n/zh/glossary.yaml`
  where it agrees.

## Things never to do on screen

Series rules:
- No slide images, page renders or long slide text; re-draw the idea and cite it with `lecture_ref`,
  only while the picture is on screen.
- No Google/GCP, Docker or Pulumi logos, and no console or browser screenshots: schematic drawings
  tagged `illustration`.
- No real person's name: the instructor is never named on screen or in subtitles (`‹instructor›`).
  The prompt user is `student`, and the staff branch is not named.
- No hand-typed output: every terminal line comes from `assets/terminal/`. `expected` panels name
  their source (only the README's OS Login snippet).
- No command spelled differently from the README. The fixes, `pulumi login --local`, `--target`,
  `docker rm -f`, the registry `create` and every other extra are tagged `extra`.
- No credentials: no key content, token, real-looking project id, `sa_` number or IP. The project
  placeholder is `your-gcp-project`, and the README's `ac215-project` gets its "default" tag.

Lecture-specific:
- Never show a terminal panel of a successful `pulumi up`, a pushed image, a created VM or an
  `instance_ip` value: none was recorded. Use the illustrations, and say "yours prints …".
- Never show or describe a Gemini chat answer.
- Don't call the persistent disk NFS, the registry GCR (except "GCR on the slides" once), or put the
  frontend on port 80.
- Don't present the local Pulumi backend or `--target` as steps to follow: they are recording
  workarounds, and the README's bucket login is the way.
- Don't advise keeping `0777`, committing `secrets/` or `Pulumi.dev.yaml` with real values, a
  passphrase on the deployment SSH key, or `-y` without reading the plan.
- Don't say `pulumi destroy` removes everything: it leaves the registry images, the state bucket, the
  manual VM and the keys.
- Don't name the unmerged staff branch, and don't follow it: `main` @ `3ecef56`.

## Left for exercises.md (not in the video)

- Digest exercises:
  - E1, resize the VM (`allow_stopping_for_update`);
  - E2, an nginx `/healthz` (checksum triggers);
  - E3, a missing repository;
  - E4, `KeyError: 'GCP_ZONE'` outside the toolbox;
  - E5, follow the request;
  - E6, deterministic tags;
  - E7, reboot resilience (the frontend's missing restart policy);
  - E8, drift with and without `--refresh`.
- Try `gcp-service` as `security:gcp_service_account_email` (untested; SLIDES Conflict 3).
- `docker_config.json`'s `gcr.io` helper, the unused `*_using_command.py` files, the
  `Pulumi.dev-test.yaml` stray stack, `GCS_BUCKET_NAME`, and the loader's swallowed exceptions
  (`cli.py:531, 577-579`).
- `b46` (the stacks on disk and the plugin cache), `b36`/`b36b`, `vm/50`, `a04`–`a06` in full.
