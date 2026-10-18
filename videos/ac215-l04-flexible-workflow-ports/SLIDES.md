# L04 lecture slides — Containers II-b

Source: one deck, `L04_containers_ii-b` (44 slides), titled "Lecture 4: Containers II-b"
(AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's lecture slides (PDF),
provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page
numbers. I wrote this digest from the deck's extracted text and from all five contact sheets, and
enlarged slides 9, 17, 26, 34, 35, 37, 38, 39 and 40 to read their diagrams and arrows. Everything
below is in my own words. Only short titles, terms, URLs and single code lines are quoted. The
tutorial side of the lecture is in [`digest.md`](digest.md).

Three notes for anyone citing the deck:

- **The printed footer numbers are not the slide numbers.** The deck was cut from a longer one.
  Its footers run 1, 8, 8, 34–42, 44–72, (none), (none), 81: slides 42 and 43 carry no footer.
  Always cite the PDF page numbers used here.
- **Relation to the L03 deck.** Slides 4–41 are a revised copy of slides 30–69 of the L03 deck
  (see [`../ac215-l03-mega-pipeline/SLIDES.md`](../ac215-l03-mega-pipeline/SLIDES.md)). I matched
  them by text. Changes in this copy: the L03 deck's first "Pick a Smaller Base Image" slide (L03
  slide 36) and its "Measure It" slide (`docker images` / `docker history`, L03 slide 38, footer 43)
  are gone, so no slide carries footer 43 (the footers jump from 42 to 44 between slides 12 and 13).
  The four dividers list four sections instead of L03's seven. Slide 9's bullets were reworded and
  gained a pure-Python footnote. Slide 10's bullets were rewritten, with a new one on Alpine wheels.
  Slide 12's "trim the extras" callout dropped pip's `--no-cache-dir`. Slide 13 dropped `--load`
  (and its callout) from its single-platform command. Slide 15's table header "Anti-pattern" became
  "Avoid these". Slide 17 added `--name gateway` to the last `docker run`. Slides 11, 19 and 20 have
  reworded captions. Where the two decks differ, this deck is the newer wording.
- **How the deck maps onto this episode.** Sections 2–3 (Compose, networking; slides 16–35) teach
  with the same gateway → processor app and the same ports (8090 / 9100 / 9200) as `port_toy`, but
  with different names (see *Terms*). Section 4 (team workflows; slides 36–41) is the idea behind
  `mega-pipeline@flexible-workflow`. Section 1 (build optimization; slides 4–15) has no tutorial of
  its own. The mega-pipeline Dockerfile follows some of its advice and breaks some (see *What the
  lecture stresses*, last block). Slides 42–43 introduce the two tutorials.

## Outline

The deck has four numbered sections (slide 3). Each section opens with a divider that repeats the
outline with the current section in bold. Slides 14, 15 and 26 have a peach background, and slides
42–43 a gray one; the deck does not say what the colors mean.

- Slide 1 · title slide ("Lecture 4: Containers II-b", red AC215/E115 badge, Harvard shield)
- Slide 2 · "Logistics / Reminders": class survey and team-sign-up form, each with a QR code
- Slide 3 · outline: Build Optimization; Docker Compose; Networking; Team Workflows (nothing bold)
- Slides 4–15 · **1. Build Optimization**
  - 4 · divider
  - 5 · "Build Optimization: Why Bother?": four costs of a fat image
  - 6 · the same, with an orange takeaway banner over the middle
  - 7 · "Layer Caching: Order Matters"
  - 8 · "`.dockerignore`: Shrink the Build Context"
  - 9 · "How Python Packages Are Installed": wheel vs source package
  - 10 · "Pick a Smaller Base Image": full vs slim vs alpine
  - 11 · "Multi-Stage Builds"
  - 12 · "Fewer, Leaner Layers"
  - 13 · "Building for the Target Platform"
  - 14 · "Build Secrets: Tokens for Dockerfile RUN Steps" (peach)
  - 15 · "Build Secrets: Supply the Token from Your Terminal", with an anti-pattern table (peach)
- Slides 16–31 · **2. Docker Compose**
  - 16 · divider
  - 17 · "The Problem Compose Solves": the gateway/processor example started by hand
  - 18 · the same, with an orange takeaway banner replacing the example
  - 19 · "What Is Docker Compose?": by hand vs with Compose
  - 20 · "compose.yaml": each key mapped to its `docker run` flag
  - 21 · "build: vs image:"
  - 22 · "Networking for Free": the auto-created compose network
  - 23 · "Volumes": bind mount and named volume in the YAML
  - 24 · "Volumes: Bind Mount vs Named Volume": the two lines dissected
  - 25 · "Environment": inline values vs `env_file`
  - 26 · "Environment: Build Time vs Run Time": the lifetime table (peach)
  - 27 · "Startup Order": what `depends_on` guarantees
  - 28 · "Startup Order": waiting for a healthcheck
  - 29 · "Everyday Compose Commands"
  - 30 · "The Whole App in One File"
  - 31 · "When Compose Isn't Enough": Compose vs Kubernetes
- Slides 32–35 · **3. Networking**
  - 32 · divider
  - 33 · "Your Containers Need to Talk": the two paths
  - 34 · "Gateway → Processor: One Shared Network"
  - 35 · "Browser → Gateway: Publish a Port"
- Slides 36–41 · **4. Team Workflows**
  - 36 · divider
  - 37–38 · "Workflow with Docker: Scenario 1 (early stages of development)", two steps
  - 39–40 · "Workflow with Docker: Scenario 2 (later stages of development)", two steps
  - 41 · "Workflow with Docker: A Flexible Approach"
- Slides 42–43 · **Tutorials** (not in the outline; gray background, magenta titles)
  - 42 · "Tutorial: Mega-pipeline Flexible Workflow" (QR code and GitHub link)
  - 43 · "Tutorial: PORT TOY" (QR code and GitHub link)
- Slide 44 · closing "THANK YOU" picture (a cartoon cat)

## Key ideas

1. **A big image costs you on every deploy, not once.** Each server must pull the image before it
   starts. Every extra package is more to patch and secure. Every code change goes through
   rebuild → push → pull. Storage multiplies by versions and servers. The takeaway banner: ship
   only what the app needs at run time, and keep the part that changes small. (Slides 5–6)
2. **Each Dockerfile instruction is a cached layer, and a change invalidates everything below
   it.** So order the steps from rarely changing to often changing: copy the dependency files,
   install, and copy the code last. Copying all the code before the install makes every code edit
   reinstall every dependency. (Slide 7)
3. **`.dockerignore` decides what goes into the build context.** Docker sends the build context
   to the daemon before building. Excluding Git history, caches, local virtual environments,
   `node_modules`, data files and secrets makes builds faster, and it means a key cannot slip into
   the image by accident. (Slide 8)
4. **Whether you need a compiler depends on wheels.** A wheel is a package that is already built:
   pip only unpacks it. If no wheel fits the environment, pip first builds one from the source
   package, and packages with native code then need compilers and build tools. In the slide's
   pure-Python example, "building" only repackages the same code with install metadata. (Slide 9)
5. **The base image is a trade-off between size and toolchain.** The full `python:3.14` image
   (about 1.63 GB) ships gcc, g++ and make. `-slim` (about 217 MB) is the sensible default when
   your dependencies have compatible wheels. `-alpine` (about 86 MB) is smaller, but it may need
   different wheels, so check that your dependencies support it. (Slide 10)
6. **Multi-stage builds keep the toolchain out of the final image.** A builder stage starts from
   the full image, installs `uv` and syncs the dependencies into `.venv`. A runtime stage starts
   from slim and copies only that `.venv` (plus the code) from the builder. The compilers stay
   behind in the discarded stage. (Slides 10–11)
7. **Layers only add.** A file deleted in a later layer still occupies its earlier layer, so a
   separate cleanup step saves nothing. Chain install and cleanup in one `RUN` with `&&`, and skip
   optional apt packages with `--no-install-recommends`. (Slide 12)
8. **Build for the CPU that will run the image.** `docker build` already uses Buildx and BuildKit.
   `--platform` picks the target architecture: Apple Silicon is arm64, Intel/AMD is amd64, and
   cloud machines can be either. Several platforms at once are built with `--push`, which sends
   the multi-platform image straight to a registry. (Slide 13)
9. **A build-time token belongs in a secret mount.** When a `RUN` step needs a token (for example,
   to install from a private GitHub repo), `RUN --mount=type=secret` makes a file available inside
   the build at `/run/secrets/<id>` for that one step only. `docker build --secret id=…,src=…`
   supplies it from a file on your machine; the shared id is the link. `ENV`, `ARG` and `COPY`
   all leave traces of the token in the image or its history. (Slides 14–15)
10. **Starting a multi-container app by hand does not scale.** It takes one long `docker run` per
    service, a network you create yourself, the right start order, and the whole cycle repeated
    after every change. One app should be one file and one command. (Slides 17–18)
11. **Compose is a file plus a tool.** `compose.yaml` (legacy `docker-compose.yaml`) describes
    services, networks and volumes. `docker compose up` builds what is missing and starts it all,
    including a shared network. `docker compose down` removes it. (Slide 19)
12. **Each `docker run` flag becomes a YAML key.** `-p` → `ports:`, `-v` → `volumes:`, `-e` →
    `environment:`. Each service is one entry, and its name doubles as its hostname. A service
    either builds its image from a folder (`build:`) or pulls a prebuilt one from a registry
    (`image:`). (Slides 20–21, 30)
13. **Compose networks the services for you.** `docker compose up` creates a network and attaches
    every service to it, so the gateway can call `http://processor:9200` without anyone creating a
    network or naming containers. (Slide 22)
14. **The left side of a volume line decides its kind.** A path on the left (`./secrets`) is a
    bind mount of a folder you chose on the host; `:ro` makes it read-only. A bare name on the left
    (`models`) is a named volume whose storage Docker owns and keeps; it must also be declared
    under a top-level `volumes:` key. (Slides 23–24)
15. **Where you set a variable decides when it exists.** `environment:` sets a few non-secret
    values inline; `env_file:` loads them from a file kept out of Git. Both reach the container at
    run time. Dockerfile `ENV` lives through build, image and container. `ARG` and Compose
    `build.args` exist only during the build. The auto-loaded `.env` file and shell variables only
    fill `${VAR}` placeholders in the Compose file itself. (Slides 25–26)
16. **`depends_on` orders start-up; it does not wait for readiness.** "Up" means the container
    started, not that the app inside is ready. To wait, give the dependency a `healthcheck` and
    use `condition: service_healthy`. The other allowed conditions are `service_started` and
    `service_completed_successfully`. (Slides 27–28)
17. **A handful of commands run the daily loop.** `up` (with `-d` for background, `--build` to
    rebuild first), `ps -a`, `logs -f` and `down`. `down -v` also deletes named volumes, which is
    your data. (Slide 29)
18. **Compose stops at one machine.** It is right for development and a single small server.
    Scaling across machines, self-healing, rolling updates and cross-node load balancing need
    Kubernetes, which comes later in the course and keeps the same idea of declared services
    found by name. (Slide 31)
19. **Networking is two separate questions.** (a) Can one service reach another? (b) Can you,
    from your laptop's browser, reach the app? Each container has its own network namespace, so
    neither path works until you wire it. (Slide 33)
20. **Container to container: one shared network, then names.** Put both containers on one
    user-created network and give them names. Docker's DNS then resolves `processor` to the right
    container, so no code needs an IP address. Compose does all three steps (network, attach,
    names) for you. (Slide 34)
21. **Laptop to container: publish a port.** `-p HOST:CONTAINER` (or `ports:`) forwards a port on
    your machine to a port inside one container: `8090:9100` sends `localhost:8090` to the
    gateway's 9100. The processor gets no published port. (Slide 35)
22. **Two team workflows.** Early on (Scenario 1), a lead ("senior") developer writes the
    Dockerfile and the uv files and pushes them to GitHub; everyone pulls them, builds images
    locally, works inside containers, and sends code plus any Dockerfile/uv changes back as pull
    requests, which the lead merges and consolidates. Later (Scenario 2), the lead also builds the
    images and pushes them to Docker Hub; developers pull ready images and rarely rebuild.
    (Slides 37–40)
23. **There is no perfect workflow.** Each team picks its own, and what matters is clear
    communication and agreed rules. (Slide 41)
24. **The tutorials put this into practice.** Mega-pipeline is rerun on your own Google Cloud
    resources (bucket, secrets and authentication, APIs) with the provided Dockerfile, uv files
    and a build-and-run script. `port_toy` explores internal container traffic, localhost
    forwarding, host vs container ports, and Compose. (Slides 42–43)

## Diagrams

- **Slide 6 · takeaway banner.** Not a mechanism: slide 5's four bullets with an orange box laid
  over the middle two, reading "Ship only what you need to RUN, and keep what changes small." Use
  it as the section's thesis line.
- **Slide 7 · cache order.** Three Dockerfile lines in a column, keywords in blue:
  `COPY pyproject.toml uv.lock ./`, `RUN uv sync`, `COPY . .`. Each has a colored callout:
  - Yellow, on the first line: dependencies change rarely and code constantly, so the dependency
    files are copied first.
  - Green, on `RUN uv sync`: this layer stays cached until the dependencies change.
  - Orange, on `COPY . .`: this is the only layer that runs again after a code edit.

  Purpose: invalidation flows downward, so position decides how much a change costs. A re-draw:
  three stacked layer slabs. A code edit relights only the top slab, while an edit to `uv.lock`
  relights the middle and the top. Then swap in the bullet's "classic mistake" order (`COPY . .`
  above the install): now a code edit relights the install slab too.
- **Slide 8 · what `.dockerignore` filters.** Six patterns in a center column (`.git`,
  `__pycache__/`, `.venv/`, `node_modules/`, `secrets/`, `*.csv`). Curved connectors join each to
  a colored label giving the reason:
  - Left side: blue "compiled Python bytecode caches" → `__pycache__/`; yellow "installed JS
    packages, reinstalled in the image" → `node_modules/`; orange "bulky local data files, not
    needed at build time" → `*.csv`.
  - Right side: green "repository history, metadata not needed to run" → `.git`; purple "local
    virtual environment, rebuilt inside the image" → `.venv/`; red "credentials and keys, must
    never enter the image" → `secrets/`.

  Purpose: why each kind of file is filtered; red marks the security case. A re-draw: a project
  folder passes through a sieve labelled `.dockerignore`. Only the code reaches the parcel
  labelled "build context", which travels to the Docker daemon.
- **Slide 9 · source distribution → wheel.** Two outlined boxes with a large blue right arrow
  between them; the caption under the arrow says that building prepares the files for
  installation.
  - Left, "Source distribution": the archive name `cheese_utils-1.0.tar.gz` and its tree:
    `pyproject.toml`, `src/cheese_utils/` (`__init__.py`, `prices.py`), `tests/test_prices.py`.
  - Right, "Built wheel": `cheese_utils-1.0-py3-none-any.whl` holding `cheese_utils/`
    (`__init__.py`, `prices.py`) and `cheese_utils-1.0.dist-info/` (`METADATA`, `WHEEL`, `RECORD`).
  - Footnote: in this pure-Python case the wheel is the same code plus install metadata, but
    packages with native extensions may need compiling when their wheels are built.

  Purpose: show what "build" means. The tests and project file stay behind, a `dist-info` folder
  is added, and only native code would need a compiler. A re-draw can animate files moving from
  the left tree to the right and the `dist-info` folder appearing.
- **Slide 10 · base-image table.** A navy-headed table with three rows: `python:3.14` (~1.63 GB, in
  red; build tools gcc, g++, make included), `python:3.14-slim` (~217 MB, in green; bold "good
  default with compatible wheels"), `python:3.14-alpine` (~86 MB, also in green; smaller, check that
  your dependencies support Alpine). A blue callout from the table says to use build tools in a build
  stage and leave them out of the final image. Purpose: the size gap and why it exists. A re-draw:
  three bars at true scale (the full image is about 7.5× slim), each labelled with what it
  contains.
- **Slide 11 · two stages.** One Dockerfile in two blocks. The top block, `FROM python:3.14 AS
  builder`, installs `uv`, copies `pyproject.toml` and `uv.lock`, and runs `uv sync`. The bottom block, `FROM
  python:3.14-slim AS runtime`, copies `/app/.venv` from the builder, copies the code and runs the
  app with the venv's Python. Callouts:
  - Yellow, on the builder: it has the common build tools and uses uv to install the dependencies
    into `.venv`.
  - Green, on the runtime: it starts from slim and holds only what the app needs.
  - Blue, on `COPY --from=builder`: the prepared `.venv` crosses over, and the build tools stay in
    the builder.
  - A blue box at the bottom repeats the idea in one line.

  Purpose: only the artifact crosses the stage boundary. A re-draw: two containers side by side,
  a large builder (gcc, g++, make, uv, `.venv`) and a slim runtime. Only the `.venv` block slides
  across, and then the builder fades away.
- **Slide 12 · one chained `RUN`.** Starts with `FROM python:3.14-slim`, then one `RUN` that does
  `apt-get update`, installs `build-essential` with `--no-install-recommends`, and removes
  `/var/lib/apt/lists/*`, joined by `&&`. Callouts:
  - Green: `--no-install-recommends` trims the extras.
  - Purple: `build-essential` is the common C/C++ toolchain for dependencies built from source.
  - Blue: chain related commands and clean up within the same layer.
  - Orange: a separate cleanup layer does not shrink the image, so delete the package lists in the
    same step. The installed build tools remain available.

  Purpose: layer additivity. A re-draw: layer N gains an "apt lists" block; a separate layer N+1
  only marks it deleted, and the stack's total height stays the same. Then the chained version:
  one layer, without the block.
- **Slide 13 · target platform.** Two commands with callouts:
  - Blue, on `--platform`: build for the target's CPU, not the laptop's.
  - Purple, on `--push`: send the multi-platform image to a registry.
  - Orange note: Apple Silicon is arm64, Intel/AMD is amd64, clouds are either; check the
    deployment target.

  Purpose: architecture mismatch. A re-draw: an arm64 laptop builds two variants under one tag in
  a registry, and an amd64 server pulls the variant that matches it.
- **Slides 14–15 · how a build secret travels** (peach background).
  - Slide 14 shows the Dockerfile side: the `# syntax=docker/dockerfile:1` line, a
    `RUN --mount=type=secret,id=gh_token` step that reads `/run/secrets/gh_token` into `GH_TOKEN`,
    and a `pip install` from a private GitHub URL that uses it. Callouts:
    - Yellow, on the syntax line: it enables `--mount` and must be the first line.
    - Blue, on `id=gh_token`: names the secret; the same id is reused on `docker build`.
    - Purple, on `/run/secrets/gh_token`: a path inside the container, mounted only for this step.
    - Green, on `$(…)`: runs `cat` to read the file into the variable.
  - Slide 15 shows the terminal side: `docker build --secret id=gh_token,src=$HOME/.gh_token .`.
    Callouts: green, the id is the same as in the `RUN --mount`, and that shared id is the link;
    blue, the `src=` path is the token file on your machine.
  - Below it, a navy-headed table "Avoid these / Risk for secrets": `ENV` → kept in the image
    configuration; `ARG` → may show up in history or build metadata; `COPY` → stays in an earlier
    layer even after a later deletion.

  Purpose: the id connects a host file to a temporary file that exists only during one build
  step. A re-draw: `~/.gh_token` on the host → a tube tagged `gh_token` → a file that appears
  inside the box for one `RUN` step and vanishes when the step ends; the finished image's layers
  are empty of it. Then show the three leaky routes as stains: on the image config (`ENV`), in the
  history list (`ARG`), in a lower layer (`COPY`).
- **Slide 17 · the running example.** Two rounded boxes: "gateway" (subtitle: serves the page) on
  the left and "processor" (subtitle: UPPER-cases the text) on the right. A top arrow to the right
  carries `hello`; a bottom arrow back carries `HELLO`. Below them are the five by-hand commands:
  create the network, build and run the processor, build and run the gateway with `-p`, two `-e`
  flags, a bind mount and a name. Purpose: introduce the app and show how much typing it takes. It
  is `port_toy`'s architecture with different names.
- **Slide 18 · takeaway banner.** Slide 17's bullets, with the example replaced by an orange box:
  "One multi-container app deserves one file and one command."
- **Slide 19 · by hand vs with Compose.** A three-row table: Network (create and attach each by
  hand → automatic and shared), Start it all (N × `docker run`, in order → `docker compose up`),
  Tear down (stop and remove each → `docker compose down`). The Compose column is in green.
- **Slide 20 · YAML ↔ flags.** The full two-service compose file. Green labels with connectors tie
  `ports:` to `-p`, `volumes:` to `-v` and `environment:` to `-e`. A pink callout on `gateway:`
  says each service is one entry and its name is its hostname. Purpose: the file is the same
  commands, declared. A re-draw: the flags from slide 17's commands fly into their YAML keys.
- **Slide 21 · two image sources.** The same file. A blue callout on `build: ./gateway`: Compose
  builds an image from that folder's Dockerfile and files. An orange callout on `image:
  ac215/processor:1.0`: pull a prebuilt image from a registry such as Docker Hub. Purpose: per
  service, choose build or pull. This is the same choice as the team workflows of section 4.
- **Slide 22 · the free network.** A large light-blue rounded rectangle labelled "compose network
  — auto-created on `docker compose up`" holds two white boxes, gateway (left) and processor
  (right). An arrow from gateway to processor is labelled `http://processor:9200`. A darker-blue
  speech bubble points up into the network and lists the two commands you no longer type
  (`docker network create app-net`, `docker run --network app-net --name gateway …`), ending
  with "Compose creates the network for you."
- **Slide 23 · volumes in the YAML.** The gateway service now mounts `./secrets:/secrets:ro` and
  `models:/models`, and a top-level `volumes:` declares `models:`. Callouts:
  - Blue, on the first line: a bind mount, with the host path on the left.
  - Blue, on its suffix: `:ro` means read-only.
  - Green, on `models:/models`: a named volume, persisted by Docker, just a name.
  - Orange, on the top-level block: declare the named volume here.
- **Slide 24 · anatomy of a volume line.** The two lines, enlarged:
  `- ./secrets:/secrets:ro` and `- models:/models`. Callouts on each side of the colon: on the
  left of the first, "a host folder you chose" (blue); on the left of the second, "Named volume
  (Docker owns the storage)" (green); on the right of both, "container path (inside the
  container)" (gray). Purpose: the same `source:target` shape, with two meanings for the source.
  A re-draw: split each line at the colon. The left half becomes a host folder icon or a
  Docker-managed drum, and the right half becomes a path inside the container box.
- **Slide 25 · two ways in for variables.** The gateway service with both `environment:` and
  `env_file: - .env`. A blue callout on `environment:`: inline, like `-e`, for a few non-secret
  values. A green callout on `env_file:`: load a `.env` file kept out of Git, so secrets stay out
  of the YAML. The subtitle says both are injected at run time.
- **Slide 26 · variable lifetime table** (peach). Rows say where the variable is written, columns
  say where it exists: Compose file (`${VAR}`) | Build | Image | Container (run).
  - Dockerfile `ENV`: Build ✓, Image ✓, Container ✓.
  - Dockerfile `ARG`: Build ✓ only.
  - Compose `build.args`: Build ✓ only.
  - Compose `environment:` / `env_file:`: Container ✓ only.
  - `.env` file (auto-loaded): Compose file ✓ only.
  - Shell variable `$VAR`: Compose file ✓ only.

  Under the table, a blue box: on the left, `TAG=1.0` in `.env` or `export TAG=1.0` in the shell;
  an arrow labelled "fills"; on the right, a compose snippet whose processor uses
  `image: ac215/processor:${TAG}`, with `${TAG}` in red. Purpose: a timeline of four stages
  (compose file → build → image → container). A re-draw: one horizontal bar per source, spanning
  the stages where the variable exists.
- **Slide 27 · start order only.** The compose file with a blue callout on `depends_on`:
  processor comes up first, then gateway. A light-blue box: "up" means the container started,
  not that the app is ready.
- **Slide 28 · readiness gate.** The long form: `depends_on:` → `processor:` →
  `condition: service_healthy`, and on the processor a `healthcheck:` with
  `test: curl -f localhost:9200/health`. Callouts:
  - Blue: order (processor first, then gateway).
  - Green, on `condition`: hold the gateway until the check passes.
  - Orange, on `service_healthy`: a fixed Compose value, not a name you make up; the other two
    are `service_started` and `service_completed_successfully`.
  - Green, on `healthcheck`: the probe that decides when the processor is ready.

  A re-draw: a timeline. The processor's container starts; its probe ticks red, red, green; only
  then does the gateway start.
- **Slide 29 · command map.** Seven commands in a column (`up`, `up -d`, `up --build`, `ps -a`,
  `logs -f`, `down`, `down -v`), each with a callout. `up` builds images, creates the network and
  starts every service. `-d` runs in the background. `--build` rebuilds first. `ps -a` shows which
  services are up or stopped. `logs -f` follows every service's output in one stream. `down` stops
  and removes all containers and the network. `-v` also deletes named volumes (your data), and the
  slide ends that orange callout with "Delete!".
- **Slide 30 · the whole app.** The complete compose file next to a blue box: gateway and
  processor in one file, run by one `docker compose up`.
- **Slide 31 · Compose vs Kubernetes.** A two-row table. Scope: one machine vs a cluster of many
  machines. Great for: development and a single small server vs production scale, self-healing
  and rolling updates.
- **Slide 33 · two paths.** Three boxes in a row: "your browser" (on your laptop) → "gateway"
  (service) → "processor" (service). The labels over the arrows are "(b) browser → gateway" and
  "(a) gateway → processor". A footnote says the arrows show the request direction and responses
  return over the same connections. Note that (a) is the right-hand arrow: the slide letters the
  paths in teaching order, not left to right. Purpose: split networking into an internal and an
  external problem.
- **Slide 34 · one shared network.** A rounded box labelled "`app-net` — every container here
  reaches any other by name" contains gateway (`http://gateway:9100`) and processor
  (`http://processor:9200`), with an arrow from gateway to processor. Below are three numbered
  steps: 1, create one shared network; 2, attach each container and name it; 3, reach it by name
  with Docker DNS, no IP (`POST http://processor:9200/`). A small callout on `--name gateway` says
  that name is optional here, because no container calls the gateway. A blue box says Compose does
  all three steps for free. A re-draw: a rail labelled `app-net` with a phone-book icon (DNS) that
  answers "processor".
- **Slide 35 · publishing a port.** On the left, "your browser" at `localhost:8090`. An arrow
  labelled "port forwarding" and `-p 8090:9100` enters an `app-net` box and reaches the gateway at
  `:9100`. The processor at `:9200` is drawn grayed out: it is not reachable from the laptop. A
  banner below reads `8090 : 9100 = HOST : CONTAINER`. At the bottom, the `docker run` form and
  the Compose `ports:` form, both with `127.0.0.1:8090:9100`. Purpose: only the gateway gets a
  door to the host. A re-draw: a door in the laptop wall numbered 8090 opens onto the gateway's
  inner door 9100.
- **Slides 37–40 · team workflow.** One layout in four states.
  - Left column: three colored panels, "Windows" (green), "Linux" (pink), "Mac" (blue). Each holds
    three dashed yellow squares (containers) above a group-of-people icon (developers on that OS).
  - Top center: a pink panel "'Senior' Developer", holding one dashed yellow bar, above a red
    person icon.
  - Center: a dotted box "Source Control" holding "GitHub". In slides 39–40 a second dotted box,
    "Images", holding "DockertHub" (sic), sits to its right.
  - Arrows, slide by slide:
    - 37: senior ↓ GitHub, then a hollow arrow from GitHub left to the developers (they pull the
      Dockerfile and uv files, build and run).
    - 38: a hollow arrow from the developers right to GitHub (pull requests). The senior's merge
      and consolidation is only in the text.
    - 39: senior ↓ GitHub and senior ↘ Docker Hub, then GitHub ← to the developers. That
      developers also pull images from Docker Hub is in the text only.
    - 40: developers → GitHub (pull requests). The rebuilt images going to Docker Hub are in the
      text only.

  Purpose: who builds images, and where they flow, early vs late in a project. A re-draw should
  add the arrows the text describes but the slides do not draw: Docker Hub → developers in
  Scenario 2, and senior → Docker Hub after the merge.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial READMEs (`mega-pipeline@flexible-workflow`, `port_toy`) |
|---|---|---|
| "Build Optimization" | 3–6 | Not a README section. Neither README discusses image size. |
| "registry" | 5, 13, 21 | mega-pipeline README: "pull a prebuilt copy from a registry" (`README.md:69`). |
| "cached layer", "bust the cache" | 7 | Neither README talks about layer caching. |
| "build context", "daemon" | 8 | Not in either README; `digest.md` uses "build context". |
| "`.dockerignore`" | 8 | Not in either README, and neither repo has one (digest G6). |
| "Ready-to-install package (wheel)", "Source package", "Source distribution", "Built wheel", "native extensions" | 9 | Not in the READMEs' prose. The mega-pipeline Dockerfile only mentions wheels in a comment on `UV_LINK_MODE`, which the root README's sample Dockerfile repeats (`README.md:338`). |
| "base image"; `python:3.14`, `-slim`, `-alpine`; "compatible wheels"; "build tools" | 10 | All five mega-pipeline Dockerfiles use `python:3.14-slim-bookworm` plus `build-essential` (and `ffmpeg` in `transcribe_audio`); `port_toy` uses `python:3.14-slim`. |
| "Multi-stage builds", "Builder stage", "Runtime stage" | 10–11 | Not in either tutorial: every Dockerfile there has one stage. |
| "Layers are additive", "build-essential", `--no-install-recommends` | 12 | The mega-pipeline Dockerfile uses both flags and cleans the apt lists in the same `RUN`, as the slide advises. |
| "Buildx", "BuildKit", "target platform", "CPU arch", "multi-platform image" | 13 | mega-pipeline README says "multi-arch" (`README.md:74`). Its `docker-shell.sh prod` runs `docker buildx build` with its own `multi-arch` builder instead of plain `docker build`. |
| "Build secrets", "secret mount", secret "id" | 14–15 | Not in the READMEs. The tutorial's secret is a run-time key, bind-mounted at `/secrets` and named by `GOOGLE_APPLICATION_CREDENTIALS` with `-e`. That is a different mechanism for a different moment (run vs build). |
| "Docker Compose"; `compose.yaml` (legacy `docker-compose.yaml`) | 19–20 | Slides 26 and 29 write `docker-compose.yml`, which is also `port_toy`'s file name. Compose accepts all of these names. |
| "service"; "name is its hostname" | 20 | `port_toy` additionally pins `container_name:` so the by-hand `docker exec gateway …` commands still work. |
| `build:` vs `image:`; "prebuilt image" | 21 | `port_toy` builds both services. mega-pipeline README's "build it locally" vs "pull a prebuilt copy" is the same choice. |
| "compose network" | 22 | `port_toy` names its network `toynet` explicitly; without that it would be `port_toy_default`. |
| "Bind mount", "Named volume", ":ro = read-only" | 23–24 | mega-pipeline's component README says both "bind mount" and "volume mount" for the same `/app` mount. `port_toy` uses no named volume. |
| "Environment"; `environment:`, `env_file:`, `.env`; "build time vs run time"; `build.args`; "Shell variable" | 25–26 | `port_toy` uses only `environment:`. mega-pipeline passes run-time values with `-e` in `docker-shell.sh`; its Dockerfiles use `ENV` (e.g. `UV_PROJECT_ENVIRONMENT`) and one build-only `ARG DEBIAN_PACKAGES`, which are live examples for the slide-26 rows. Neither tutorial uses `env_file:`, a `.env` file or Compose `build.args`. |
| "Startup Order"; `depends_on`; "up = container started, not app ready" | 27 | `port_toy`'s compose file uses the short form of `depends_on` (no readiness wait). |
| "healthcheck", "probe"; `service_healthy`, `service_started`, `service_completed_successfully` | 28 | Not in `port_toy`'s compose file, although its processor already serves `GET /health` and has `curl` installed. |
| "detached" | 29 | `port_toy` README never says "detached". It first runs `docker compose up` in the foreground (stopped with Ctrl+C), then `docker compose up -d`, which "runs the app in the background" (`README.md:492-495`). |
| "Kubernetes", "cluster", "self-healing", "rolling updates", "cross-node load balancing" | 31 | Not in L04's tutorials (later lecture). |
| "network namespace", "Isolated by default", "Containers I" | 33 | `port_toy` README never says "namespace"; it says each container's `localhost` is itself. |
| "one shared network"; "Docker DNS" | 34 | `port_toy` README: "user-defined network `toynet`"; containers "find each other by name". It never says "DNS". |
| "Publish a Port", "port forwarding", "HOST : CONTAINER" | 35 | `port_toy` README: "published port", "host port", "container port", "forward". It adds "ephemeral source port" and the meaning of `127.0.0.1`, which the slides do not explain. |
| gateway, processor, `app-net`, `gateway-img`, `processor-img`, `ac215/processor:1.0` | 17–35 | `port_toy`: `toynet`, `toy-gateway`, `toy-processor`, and the processor is built (`build: ./processor`), not pulled. Same ports 8090 / 9100 / 9200. |
| "Workflow with Docker"; "'Senior' Developer"; "Source Control"; "Images" | 37–40 | mega-pipeline README, "Two ways to work": "a senior dev publishes prebuilt images to DockerHub" (`README.md:72`). |
| "Scenario 1 (early stages of development)" / "Scenario 2 (later stages of development)" | 37–40 | README: "Early in development" / "Later in development" (`README.md:71-72`). |
| "uv files" (= `pyproject.toml` + `uv.lock`) | 37–40 | The READMEs name the files; they never say "uv files". |
| "DockerHub" (box label misspelled "DockertHub") | 39–40 | mega-pipeline READMEs write "DockerHub"; slide 21 and `digest.md` write "Docker Hub". The box label is a typo. |
| "A Flexible Approach"; "Mega-pipeline Flexible Workflow" | 41–42 | README: "the **flexible workflow** in the branch name" (`README.md:74`), realized as the four `docker-shell.sh` modes (none, `dev`, `run`, `prod`). |
| "PORT TOY" | 43 | Repo `port_toy`, README title "Port Toy App". |

## Commands and code on the slides

Verbatim, one physical line each, as printed. A trailing `\` means the slide continues the
command on the next line. Lines separated by "·" are separate lines on the slide.

| Slide | Command / code | Note |
|---|---|---|
| 7 | `COPY pyproject.toml uv.lock ./` · `RUN uv sync` · `COPY . .` | the cache-friendly order |
| 8 | `.git` · `__pycache__/` · `.venv/` · `node_modules/` · `secrets/` · `*.csv` | `.dockerignore` lines |
| 9 | `cheese_utils-1.0.tar.gz` → `cheese_utils-1.0-py3-none-any.whl` | sdist → wheel names |
| 9 | `cheese_utils-1.0.dist-info/` · `METADATA` · `WHEEL` · `RECORD` | what the wheel adds |
| 10 | `python:3.14` · `python:3.14-slim` · `python:3.14-alpine` | base images |
| 11 | `FROM python:3.14 AS builder` | builder stage |
| 11 | `WORKDIR /app` · `RUN pip install uv` · `COPY pyproject.toml uv.lock ./` · `RUN uv sync` | builder steps |
| 11 | `FROM python:3.14-slim AS runtime` | runtime stage |
| 11 | `WORKDIR /app` · `COPY --from=builder /app/.venv /app/.venv` · `COPY . .` | runtime steps |
| 11 | `CMD ["/app/.venv/bin/python", "app.py"]` | runs the venv's Python |
| 12 | `FROM python:3.14-slim` | |
| 12 | `RUN apt-get update \` | |
| 12 | ` && apt-get install -y --no-install-recommends build-essential \` | the slide wraps `build-` / `essential` across two lines |
| 12 | ` && rm -rf /var/lib/apt/lists/*` | cleanup in the same layer |
| 13 | `$ docker build --platform linux/amd64 -t myapp .` | one target platform |
| 13 | `$ docker build --push \` · `--platform linux/amd64,linux/arm64 -t myapp .` | multi-platform, pushed |
| 14 | `# syntax=docker/dockerfile:1` | must be the first line |
| 14 | `RUN --mount=type=secret,id=gh_token \` | |
| 14 | `GH_TOKEN=$(cat /run/secrets/gh_token) &&\` | |
| 14 | `pip install "git+https://GH_USERNAME:${GH_TOKEN}@github.com/org/lib"` | |
| 15 | `$ docker build --secret id=gh_token,src=$HOME/.gh_token .` | |
| 15 | `ENV GH_TOKEN=ghp_xxx` · `ARG GH_TOKEN` · `COPY .gh_token /tmp/token` | the three to avoid |
| 17 | `docker network create app-net` | |
| 17 | `docker build -t processor-img ./processor` | |
| 17 | `docker run -d --network app-net --name processor processor-img` | |
| 17 | `docker build -t gateway-img ./gateway` | |
| 17 | `docker run -d --network app-net -p 8090:9100 \` | |
| 17 | `-e PROCESSOR_HOST=processor -e PROCESSOR_PORT=9200 \` | |
| 17 | `-v "$PWD/gateway:/app" --name gateway gateway-img` | the extracted text shows an en dash in `--name`; the slide image shows two hyphens |
| 19 | `docker network create` · `N x docker run (in order)` · `docker compose up` · `docker compose down` | table cells |
| 20, 30 | `services:` · `gateway:` · `build: ./gateway` · `ports:` · `- "8090:9100"` | |
| 20, 30 | `volumes:` · `- ./gateway:/app` · `environment:` · `PROCESSOR_HOST: processor` · `PROCESSOR_PORT: "9200"` | |
| 20, 30 | `depends_on:` · `- processor` · `processor:` · `image: ac215/processor:1.0` | the processor is pulled, not built |
| 22 | `http://processor:9200` | the call the gateway makes |
| 22 | `$ docker network create app-net` · `$ docker run --network app-net --name gateway …` | "You never ran this" |
| 23 | `- ./secrets:/secrets:ro` · `- models:/models` | |
| 23 | `volumes:` · `models:` | top-level declaration |
| 25 | `env_file:` · `- .env` | |
| 26 | `TAG=1.0` · `export TAG=1.0` · `image: ac215/processor:${TAG}` | interpolation |
| 28 | `depends_on:` · `processor:` · `condition: service_healthy` | long form |
| 28 | `healthcheck:` · `test: curl -f localhost:9200/health` | on the processor |
| 28 | `service_started` · `service_completed_successfully` | the other conditions |
| 29 | `docker compose up` · `docker compose up -d` · `docker compose up --build` | |
| 29 | `docker compose ps -a` · `docker compose logs -f` · `docker compose down` · `docker compose down -v` | |
| 34 | `$ docker network create app-net` | step 1 |
| 34 | `$ docker run --network app-net \` · `--name gateway gateway-img` | step 2 |
| 34 | `$ docker run --network app-net \` · `--name processor processor-img` | step 2 |
| 34 | `POST http://processor:9200/` | step 3 |
| 34 | `http://gateway:9100` · `http://processor:9200` | names in the diagram |
| 35 | `localhost:8090` · `-p 8090:9100` · `:9100` · `:9200` | diagram labels |
| 35 | `$ docker run --network app-net \` · `--name gateway \` · `-p 127.0.0.1:8090:9100 gateway-img` | |
| 35 | `ports:` · `- "127.0.0.1:8090:9100"` | Compose excerpt |
| 42 | `Dockerfile`, `pyproject.toml`, `uv.lock` | files the tutorial provides |

## What the lecture stresses

**Build optimization**

- The section's thesis: ship only what you need to run, and keep what changes small. A fat image
  costs at every deploy, in patching, in team time and in storage. (5–6)
- The "classic mistake": `COPY . .` before installing the dependencies, so every code edit
  reinstalls everything. Put rarely changing steps first. (7)
- Credentials and keys "must never enter the image"; `.dockerignore` is the guard, and it also
  speeds up builds. (8)
- Not every package needs a compiler: only those without a compatible wheel. (9)
- Slim is the good default when wheels exist. With Alpine, check that your dependencies support it
  first. Keep build tools in a build stage, out of the final image. (10–11)
- A cleanup in its own layer saves nothing, because layers only add. Delete in the same `RUN`. (12)
- Build for the deployment target's CPU, not your laptop's, and check what the target is. (13)
- Never pass a token with `ENV` (stored in the image config), `ARG` (can show in history or build
  metadata) or `COPY` (stays in an earlier layer even after deletion). Use a secret mount; the
  `# syntax` line must come first for `--mount` to work. (14–15)

**Compose**

- One multi-container app deserves one file and one command. (18)
- Each service name is also its hostname. (20)
- `.env` files stay out of Git, and inline `environment:` is for a few non-secret values only. (25)
- The place a variable is written decides when it exists: the `.env` file and shell variables only
  fill the Compose file, not the container, and `ARG` / `build.args` disappear after the build. (26)
- "Up" is not "ready": `depends_on` alone only orders start-up. Waiting needs a healthcheck and
  `condition: service_healthy`, and the condition names are fixed keywords. (27–28)
- `docker compose down -v` deletes your named volumes, i.e. your data; the slide's callout ends
  with "Delete!". (29)
- Compose is for one machine; production on many hosts needs Kubernetes. (31)

**Networking**

- Containers are isolated by default: each has its own network namespace until you wire the path.
  (33)
- Reach services by name through Docker DNS, never by IP. Naming a container nobody calls (here
  the gateway) is optional. (34)
- The order in a port mapping is HOST : CONTAINER. Only the gateway publishes a port. (35)

**Team workflows**

- One lead developer owns the Dockerfile and the uv files, reviews and merges every pull request,
  and consolidates the changes into new versions. Later in a project, the lead also builds and
  publishes the images, so others rarely rebuild. (37–40)
- There is no perfect workflow; clear communication and rules are what matter, and each team sets
  its own. (41)

**Where the tutorials diverge from the slides' advice** (my comparison with the repos at the
commits in `digest.md`; not on the slides)

- All five mega-pipeline Dockerfiles copy the whole component folder (`COPY --chown=app:app . ./`)
  *before* `RUN uv sync`, the order slide 7 calls the classic mistake. During development the
  bind mount over `/app` hides most of the cost, because code edits need no rebuild.
- Neither repo has a `.dockerignore` (slide 8). In mega-pipeline this lets an old `secrets/`
  folder inside a component reach the image (digest G6).
- mega-pipeline is single-stage and keeps `build-essential` in the final image (contrast slides
  10–11). It does chain the apt cleanup in one `RUN` with `--no-install-recommends` (slide 12).
- Slide 11 puts the venv at `/app/.venv`. A development bind mount over `/app` (slides 17, 20)
  would hide it. mega-pipeline avoids this with `UV_PROJECT_ENVIRONMENT=/home/app/.venv`. A scene
  that combines the two slides should say so.
- Slides 17, 20–21, 23, 25, 27–28 and 30, and slide 35's diagram, publish `8090:9100`, i.e. on all
  host addresses. Only slide
  35's code uses `127.0.0.1:8090:9100`, and the slide does not explain the difference. `port_toy`
  uses the `127.0.0.1` form everywhere and explains it.
- Slide 25 loads `.env` through `env_file:` (into the container), while slide 26 says the
  auto-loaded `.env` only fills the Compose file. Both are true; they are two different uses of the
  same file name. A script should say that explicitly.

## Pointers

- **Slide 2 · logistics.** A class survey, `https://bit.ly/ac215_2026_survey` (with a QR code), and
  a note that the survey results are on Canvas (linked). A form to fill in when you form a team,
  `https://bit.ly/ac215_2026_groups` (with a QR code). Both items are numbered "1." on the slide.
- **Slide 21 · Docker Hub** is named as the example registry for `image:`.
- **Slide 31 · Kubernetes** is announced for later in the course.
- **Slide 33 · "Containers I"** (Lecture 2) is the back-reference for network namespaces.
- **Slide 42 · tutorial "Mega-pipeline Flexible Workflow".** Repeat the Mega Pipeline workflow on
  your own Google Cloud resources. You set up your own Cloud Storage bucket, your secrets and
  authentication, and the required APIs. Provided: Dockerfile, `pyproject.toml`, `uv.lock`, and a
  shell script that builds and runs the container for development or production. Link:
  `https://github.com/dlops-io/mega-pipeline/tree/flexible-workflow` (with a QR code).
- **Slide 43 · tutorial "PORT TOY"** (container networking and Docker Compose). Four topics:
  internal container communication, how Docker Desktop forwards `localhost` traffic into
  containers, host vs container ports, and how Compose runs it all. The slide also carries a
  second, shorter wording of the same description that begins "How about this shorter version?";
  it looks like a leftover drafting note. Link: `https://github.com/dlops-io/port_toy#-runnin-the-app`
  (with a QR code). The anchor matches no heading in the README at `d190c71`, so the link opens
  the top of the repo page.
- No readings, homework or milestone notes appear in this deck. Slides 42–43 are its only
  tutorial pointers, and the QR codes encode the links printed next to them (not decoded here).

## This video and the slides

**Basis.** The video is built: `script.md` v2 (16 scenes; part 1 = S01–S09 on
`mega-pipeline@flexible-workflow`, part 2 = S10–S16 on `port_toy`), `BRIEF.md`, `video.yaml`,
`ASSETS.md` and the captures in `assets/terminal/` (2026-10-14). The study guide is
`MLOps_Learning/guides/L04-containers-2b-flexible-workflow-ports.md`. For this section I re-read all
five contact sheets and the deck's text. I also re-checked these at the source:

- `port_toy`'s `docker-compose.yml`, both Dockerfiles, and the processor's default port
  (`processor/processor.py:42`: 9200). Slide 17 starts the processor without `-e PORT`, so its
  command behaves the same with `port_toy`'s processor;
- `transcribe_audio/Dockerfile:4`, `:17`, `:21-41` (the one apt `RUN` chain, then
  `COPY --chown=app:app . ./` before `RUN uv sync`) and `docker-shell.sh:62-66`, `:92-95` (its own
  `multi-arch` builder; the two mounts, neither with `:ro`);
- the captures `port-laptop/18`, `20`, `21` (`-p 8090:9100` vs `127.0.0.1`), `port-laptop/66` and
  `mega-laptop/70` (image sizes), `mega-laptop/15` and `17` (what a changed folder costs a
  rebuild), `mega-laptop/72`, `74`, `76` (the Docker Hub images) and `mega-l03-laptop/13` (the key
  inside the image);
- Docker Hub's API for the slides' example image `ac215/processor`. It answered 404, "object not
  found", on 2026-10-16. The control, `dlops/mega-pipeline-transcribe-audio`, answered 200.

Where the slides and the captures disagree, the captures decide what the video shows.

### 1. Map: scenes ↔ slides

| Scene | Slides on the same ground | Relation |
|---|---|---|
| S01 · Build or pull? Whose localhost? | 42–43 (the two tutorials); 37–40 (who builds, who pulls); 33 (the two questions that decide whether anything works) | Same concept, asked as puzzles: the hook poses what sections 3–4 answer. The stale Docker Hub image is tutorial-only (Conflict 11). |
| S02 · Same pipeline, built like a team | 37–41 (Scenarios 1 and 2, no perfect workflow); 42 (your own resources; the provided Dockerfile, uv files and script); 21 (build or pull) | Same concept: V1 is the lecture's section 4. Gap 5. |
| S03 · Get the code: clone, or switch branches | 42 (the branch link) | Tutorial-only (clone, the branch switch, `git stash -u`). |
| S04 · Your bucket and your three values | 42 ("your own Cloud Storage bucket") | Tutorial-only in substance. The slide only names the task. |
| S05 · Three gates: account, role, API | 42 ("your secrets and authentication", "the required Google Cloud APIs") | Tutorial-only in substance (service account, roles, APIs). |
| S06 · docker-shell.sh: one script, two windows | 42 (a script that builds and runs, for development or production); 23–24 (bind mount: host path left, container path right); 25–26 (`-e` lives at run time, `ENV` in the image); 11 (where the venv lives); 12 (build step 2 is one chained `RUN`) | The tutorial applies it. Conflicts 8, 10; Gap 1. |
| S07 · Five components, five honest errors | 7 (`CACHED [2/5]`: one layer reused by several images) | Tutorial-only (the Google calls and their errors). The cache is applied, not named. |
| S08 · dev, run, and a stale image | 37–38 (Scenario 1: develop inside containers, the uv files change, rebuild, send it back); 39–40 (Scenario 2: pull, rarely rebuild); 7 (a changed folder re-runs the copy and `uv sync`) | The tutorial applies it. Conflicts 5, 11; Gaps 3, 5. |
| S09 · prod, a stowaway key, and clean-up | 13 (target platform, multi-platform push); 39–40 (the lead pushes images); 8 (`.dockerignore`, the red `secrets/` entry); 15 (`COPY` leaves a secret in a layer); 5–6, 10–11 (what a 1.48 GB image costs; build tools in the final image) | The tutorial applies it. Conflicts 6, 7, 9; Gaps 2, 7, 8. |
| S10 · Two little computers, one network | 33 (isolated by default: a network namespace each); 34 (one shared network, names); 17 (the gateway/processor app); 43 (the `port_toy` tutorial) | Same concept. |
| S11 · Build, start, read the logs | 12 (the chained apt `RUN`); 7 (the gateway reuses the processor's layer); 17 (the by-hand commands); 34 (attach and name); 35 (publish, HOST : CONTAINER) | Same concept for the network and the port. The tutorial applies 7 and 12. Conflicts 1, 2. |
| S12 · Send a message: ports on the wire | 33 (footnote: replies come back over the same connections); 34 (`POST http://processor:9200/`) | Tutorial-only in substance (source ports, the page). |
| S13 · Who can reach whom | 33–35 (two paths; Docker DNS; only the gateway gets a door); 28 (a healthcheck runs curl inside the processor) | Same concept. Conflict 1; Gap 4. |
| S14 · Change the ports | 35 (HOST : CONTAINER); 26 (`-e` values exist only in the container) | The tutorial applies it. Gap 1. |
| S15 · Compose: the same app, declared | 17–22 (by hand is a chore; one file, one tool; flags → keys; build or pull; the free network); 27 (start order only); 29–30 (everyday commands; the whole app) | Same concept: V8 is slide 20 in motion. Conflicts 2, 3, 4; Gaps 4, 6. |
| S16 · Edit, apply, tear down, recap | 29 (`up -d`, `--build`, `logs -f`, `down`); 17, 23–24 (the gateway's mounted folder); 31 (Compose stops at one machine) | Same concept. Gaps 9, 10. |
| — not in the video | 1–4, 16, 32, 36, 44 (title, logistics, outline, dividers, closing); 9 (wheels); 10–11 as teaching (base-image table, multi-stage); 14 (the build-secret mount); 23–24's named volume; 25's `env_file:`; 26's `.env`, `build.args` and shell rows; 28 (healthcheck); 31 (Kubernetes) | Lecture-only. Slides 4–41 are a revised copy of the L03 deck's 30–69 (see the top of this file). |

### 2. Already in common

| # | Concept | Scenes ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | Build or pull: early on everyone builds from the files in Git; later one person publishes to Docker Hub and the others pull | S02, S08 ↔ 37–40 | Yes. V1's two phases are Scenarios 1 and 2. The video adds what the slides leave out: a tag is only a signpost, and the image behind `dlops/…:latest` is old (Conflict 11). It never says "senior developer" or "pull request" (Gap 5). |
| 2 | The course hands you the Dockerfile, `pyproject.toml`, `uv.lock` and a build-and-run script | S02, S03, S06 ↔ 37, 42 | Yes. The course plays the slides' senior developer, who writes these files and pushes them to GitHub (slide 37). S02's GREEN recipe card (the three files) and PURPLE `docker-shell.sh` chip are slide 42's "We provide" list. |
| 3 | Your own bucket, credentials and APIs | S04, S05 ↔ 42 | Yes. The slide names the three set-up tasks; the video does them. |
| 4 | A host folder seen inside the container: the bind mount | S06, S16 ↔ 17, 23–24 | Yes. V5's two PINK routes are slide 24's `source:target` reading, and S16's "what if" `index.html` edit (an illustration, not a capture) is slide 17's `-v "$PWD/gateway:/app"`. The video never labels the two sides (proposal S06 iii). The lecture's secrets example adds `:ro` (Conflict 10). |
| 5 | Variables set at run time | S06, S11, S14, S16 ↔ 20, 25–26 | Partly. The video uses `-e` and `environment:` correctly, and S14 says "No image was rebuilt: it's only configuration." It never gives the lecture's rule that where you set a variable decides when it exists (Gap 1). |
| 6 | A changed layer rebuilds itself and every layer below it | S07, S08, S11 ↔ 7 | Yes on the mechanism: the `CACHED` steps, "the copy and uv sync steps run again", "the two files match up to the copy line". The lecture's ordering rule is not stated, and the mega-pipeline Dockerfile breaks it (Conflict 5, Gap 3). |
| 7 | One chained `RUN` with `--no-install-recommends` and the apt lists removed in the same step | S06, S11 ↔ 12 | Yes. S11's panel wraps `port_toy`'s line 2 at its `&&`, which is slide 12's shape, line for line. S06's build step 2 is the same pattern with `build-essential ffmpeg`. |
| 8 | Two CPU types, one tag, pushed | S09 ↔ 13 | Yes on the idea. The command differs (Conflict 9). The video credits lecture 2. |
| 9 | Secrets never in the image; `.dockerignore` | S09 ↔ 8, 15 | Yes. S09 proves slide 8's red rule on a real image (`mega-l03-laptop/13`), and slide 15's `COPY` row is what happened there. The video's fix lists only `secrets/` (Gap 2). |
| 10 | Images are big, and size costs | S09 ↔ 5–6, 10 | Partly. S09 shows 1.48 GB and four images of about 830 MB as a clean-up chore. The lecture's reason, that every deploy is a download, is not said (Gap 8). |
| 11 | Each container is isolated: its own namespace, its own `localhost` | S01, S10, S13 ↔ 33 | Yes. "Its own little computer" is slide 33's "own network namespace", but the video never says "namespace" (proposal S10 ii). Puzzle 2 is slide 33's question (a), asked from the wrong side. |
| 12 | One shared network; reach a service by name through Docker DNS, never by IP | S10, S13 ↔ 34 | Yes. The PINK phone book is slide 34's step 3. The video goes further: `nameserver 127.0.0.11`, the real addresses, and names that survive a restart. |
| 13 | Two paths: browser → gateway and gateway → processor | S10, S13 ↔ 33 | Yes. S10's opening picture is slide 33's row of three boxes. The slide letters the paths (a) and (b); the video doesn't name them. |
| 14 | Publish a port, HOST : CONTAINER; only the gateway gets a door | S11, S13, S14 ↔ 35 | Yes. V7's street door and room are slide 35's port forwarding, and the processor's door "facing only the rail" is the slide's grayed-out processor. The video adds the IP part and `0.0.0.0` (Conflict 1). |
| 15 | By hand is a chore: one app, one file, one command | S15 ↔ 17–19, 30 | Yes. V8's collapse into `docker compose up` is slide 18's banner, animated. |
| 16 | Each `docker run` flag becomes a YAML key; a service's name is its hostname | S15 ↔ 20 | Yes. V8 is slide 20's connectors in motion (`-p` → `ports:`, `-e` → `environment:`). `port_toy` also pins `container_name:`. The framing of `volumes:` differs (Conflict 4). |
| 17 | Compose creates the network | S15 ↔ 22 | Partly. `port_toy` names its network in the file, so the video maps `docker network create toynet` onto `name: toynet`. The lecture's point is that you need neither: without the key, Compose would create `port_toy_default` itself. |
| 18 | `depends_on` orders start-up | S15 ↔ 27 | Yes: "starts the processor first". The slide's warning that started is not ready is missing (Gap 4). |
| 19 | The everyday Compose commands | S15, S16 ↔ 29 | Yes. `up`, `up -d`, `up -d --build`, `ps -a`, `logs -f` and `down` all run on screen. The video adds what the slide doesn't: `Ctrl+C` only stops, and takes about 20 s. `down -v` has no use here, because there is no named volume. |
| 20 | Run Compose from the folder that holds the file | S15 ↔ 29 | Yes. S15's "cd into port toy first: Compose reads the file in the current folder" is slide 29's subtitle. |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **Build time vs run time (slides 25–26).** The place a variable is written decides when it exists.
   - Dockerfile `ENV` lives in the build, the image and the container.
   - `ARG` and Compose `build.args` live only during the build.
   - `-e`, `environment:` and `env_file:` live only in the running container.
   - The auto-loaded `.env` file and shell variables only fill `${…}` in the Compose file.

   This is the rule behind every "rebuild or not?" in both tutorials: `PORT` and
   `PROCESSOR_PORT` (S14: configuration, no rebuild), `GOOGLE_APPLICATION_CREDENTIALS` set with
   `-e` (`docker-shell.sh:95`), `UV_PROJECT_ENVIRONMENT` as `ENV` (`Dockerfile:17`), and
   `ARG DEBIAN_PACKAGES` (`Dockerfile:4`: changing it rebuilds build step 2, the slow one). The
   guide's exercise D2 is this table in practice. **Carry it in** S14 (the ponder answer) and S06
   (the `-e` signpost).
2. **What else `.dockerignore` keeps out (slide 8).** The video's fix lists only `secrets/`. Slide
   8 also filters caches, local virtual environments and bulky data. In this tutorial,
   `--download` and the other steps write `input_audios/`, `text_prompts/<group>/` and the other
   data folders into the component folder. Git ignores them (each component's own `.gitignore`,
   e.g. `transcribe_audio/.gitignore:5-6`); Docker copies
   them. Captured: after one container's `--download`, the next `./docker-shell.sh` re-ran the copy
   and `uv sync` (`mega-laptop/15`: `Building 9.4s`, against `0.3s` when nothing changed,
   `mega-laptop/17`). With a key, the recordings and texts would also ride into the image. **Carry
   it in** S09's fix card (text only).
3. **Cache order: dependency files first, code last (slide 7).** S08 says what happens ("after any
   change in the folder, the copy and uv sync steps run again") but not the lecture's rule, nor
   that this Dockerfile does it the other way (Conflict 5). **Carry it in** S08, as a tag and a
   GREY note.
4. **Started is not ready (slides 27–28).** `depends_on` only orders start-up. To wait, the
   dependency needs a `healthcheck` and the gateway `condition: service_healthy`. `port_toy`'s
   processor already serves `GET /health` and has curl (guide E14), so slide 28's check would fit
   as written. Not tried here. It matters as soon as a dependency is slow to come up, such as a
   database. **Carry it in** S15's `depends_on` beat (a GREY note, or the bridge in §5) and S13's
   curl aside.
5. **The team loop: a lead and pull requests (slides 37–41).** In Scenario 1, developers send
   their code and any Dockerfile or uv-file changes back as pull requests, and the lead merges and
   consolidates them. In Scenario 2, the lead also builds and pushes the images, so the others
   rarely rebuild. Slide 41: no workflow is perfect; agree on the rules. V1 has the two phases but
   no lead and no pull request. For a student, it means: after `uv add`, commit both files and send
   them as a pull request. **Carry it in** S02 (V1 labels) and S08 (the `uv add` beat).
6. **Build or pull, per service (slide 21).** In Compose, each service either builds (`build:`) or
   pulls (`image:`). That is part 1's choice inside part 2's file. `port_toy` builds both.
   **Carry it in** S15, as a tag at "the build command becomes build".
7. **Layers only add (slides 12, 15).** A file deleted in a later layer still sits in the earlier
   one. Slide 15: a `COPY`-ed token stays in its layer after a later deletion. So after S09's fix,
   images built before it must go, and a `RUN rm -rf secrets` added to the Dockerfile would not
   help. The video's fix card omits "remove images built before the fix" (the guide's G6 has it).
   **Carry it in** S09's fix card, as one GREY row.
8. **Ship only what runs (slides 5–6, 9–11).** These images keep `build-essential` (and `ffmpeg`
   in transcribe) in the final image: 821 MB to 1.48 GB on a base of 195 MB (`mega-laptop/70`,
   disk usage). The lecture's chain:
   - a compiler is needed only for packages without a matching wheel (9);
   - slim is the default base when wheels exist (10);
   - a builder stage keeps the compilers out of the final image (11).

   The guide's G17 notes that the lock files carry wheels for the compiled packages. Whether these
   images still need `build-essential` was not tested. You don't need any of this to finish the
   tutorial, but it explains S09's sizes and S06's 44.7 s build step 2. **Carry it in** S09's
   `docker images` beat, as a tag and a GREY note.
9. **Read-only mounts and named volumes (slides 23–24, 29).** The lecture mounts its secrets
   `:ro`. A bare name on the left of a volume line is a named volume, which Docker keeps, and
   `down -v` deletes it. Neither tutorial uses a named volume. **Carry it in** S06 (a GREY note on
   the `/secrets` route) and S16 (the `down` beat).
10. **Compose stops at one machine (slide 31).** Kubernetes, later in the course, keeps the idea of
    declared services found by name. **Carry it in** S16's teaser, as a tag only.
11. **Build-time secrets (slides 14–15).** A token that a `RUN` step needs (to install from a
    private repository) goes in through a secret mount, never `ENV`, `ARG` or `COPY`. The tutorial's
    key is the other kind, a run-time secret: mounted at `/secrets` and named with `-e`. Low value
    for doing the tutorial, but it keeps the two apart. **Carry it in** S06's key beat, as a
    "compare" tag.

### 4. Conflicts

| # | The slides say | The tutorial and the captures | Current | How the video should put it |
|---|---|---|---|---|
| 1 | **Publish address.** Slides 17, 20–21, 23, 25, 27–28, 30 and slide 35's diagram publish `8090:9100`. Only slide 35's two code lines write `127.0.0.1:8090:9100`, without saying why. | `port_toy` writes `127.0.0.1:8090:9100` everywhere (`README.md:120-124`, `docker-compose.yml:16`) and explains it (`:232-244`). Captured: the short form asks for 8090 on every address, so it collides with a running `127.0.0.1:8090` (`port-laptop/18`: `port is already allocated`); on 8091 it shows `0.0.0.0:8091->9100/tcp` (`21`). | Both work. The README's form is the one to type, and the safer. | S13 already shows it. Add the slide 35 tag there with a GREY note: "lecture's short form = every address · its code line adds 127.0.0.1". If spoken: "The lecture's short form opens the door on every address; port toy adds 127.0.0.1, this laptop only." |
| 2 | **Names, and where the processor's image comes from.** Network `app-net`, images `processor-img` and `gateway-img`; in Compose the processor is pulled, `image: ac215/processor:1.0` (slides 20–21, 27–28, 30; slide 26 writes the tag as `${TAG}`). | `port_toy`: `toynet`, `toy-processor`, `toy-gateway`; Compose builds both (`build: ./processor`, `docker-compose.yml:29`) and names them `port_toy-processor` and `port_toy-gateway` (`port-laptop/47`, `66`). `ac215/processor` is not on Docker Hub (API 404, 2026-10-16), so a compose file copied from slide 20 would fail at the pull. The ports (8090, 9100, 9200) and the variables (`PROCESSOR_HOST`, `PROCESSOR_PORT`) are the same. | `port_toy`'s names | Nothing spoken. In S15, a GREY note under the processor panel: "the lecture's example pulls an image here · port_toy builds it". Kindly: same app, same ports, other names. |
| 3 | **Compose file name.** Slides 19–20: `compose.yaml` (legacy `docker-compose.yaml`). Slides 26 and 29 write `docker-compose.yml`. | `port_toy`'s file is `docker-compose.yml`, and Compose v5.6.0 read it (`port-laptop/47`). | Both. `compose.yaml` is Compose's preferred name; it still accepts the older ones. | Nothing to change. Optional GREY note on S15's panel header: "Compose also reads compose.yaml". |
| 4 | **What the by-hand run already had.** Slide 17's by-hand gateway run has `-v "$PWD/gateway:/app"`, and you start the services "in the right order" yourself (slides 17, 19). Slide 20 labels `volumes:` as the home of `-v`. | `port_toy`'s Step 1 has no `-v` (`README.md:120-124`). So S15 calls `volumes:` and `depends_on` new keys, with "no by-hand ancestor". | Both, each measured against its own by-hand version | Keep the SAY: "Two keys are new" is true of `port_toy`'s Step 1. In V8, GREY notes: on `volumes:` "the lecture's by-hand run had -v · slide 17"; on `depends_on` "= the order you typed them". |
| 5 | **Cache order.** Slide 7: copy `pyproject.toml uv.lock`, run `uv sync`, then `COPY . .`. The other order is the "classic mistake". | All five Dockerfiles copy the whole folder first (`COPY --chown=app:app . ./`), then `RUN uv sync` (`transcribe_audio/Dockerfile:39-41`). Captured: once a folder had changed, the rebuild re-ran both steps, `Building 9.4s` with `uv sync` 2.0 s (`mega-laptop/15`), against `Building 0.3s` (`17`). | The committed Dockerfile is what students run; the slide's order is the better practice. With uv and the bind mount, the cost here is seconds. | S08 already says what happens. Add the slide 7 tag and a GREY note: "lecture's order: lock files first, code last". If spoken: "This Dockerfile copies the folder before uv sync; with uv, the re-run costs seconds." |
| 6 | **`.dockerignore`.** Slide 8: filter the build context; `secrets/` "must never enter the image". | No branch of mega-pipeline has a `.dockerignore`, and neither has `port_toy`. Captured: an L03 key left in `transcribe_audio/secrets/` was inside the image after `./docker-shell.sh dev` (`mega-l03-laptop/13`, a stand-in file). | The slide's rule: add the file. | S09 says it already. Add the slides 8, 15 tag. |
| 7 | **Build tools in the final image.** Slides 10–11: compilers belong in a builder stage; the runtime starts from slim and receives only the `.venv`. | One stage on `python:3.14-slim-bookworm` that keeps `build-essential` (and `ffmpeg` in transcribe): 821–836 MB, and 1.48 GB for transcribe, on a 195 MB base (`mega-laptop/70`). | The tutorial's Dockerfile. The slide's pattern is an optional improvement, not tried here. | Nothing spoken. On S09's `docker images` beat, a GREY note: "compilers ride along · lecture: builder stage". |
| 8 | **Where the venv lives.** Slide 11 builds it at `/app/.venv` and runs `/app/.venv/bin/python`. Slides 17 and 20 mount a folder over `/app` for development. | `Dockerfile:17` puts the venv at `/home/app/.venv`, because `docker-shell.sh:93` mounts the component folder over `/app`. S06: "the window can't hide it". | Both, each in its own setting. Slide 11's layout is fine without a mount; with a development mount over `/app`, the venv would be hidden (guide C3). | On S06's venv line, the slide 11 tag with a GREY note: "slide 11 keeps .venv in /app · fine without a mount". |
| 9 | **The multi-platform command.** Slide 13: one plain `docker build --push --platform linux/amd64,linux/arm64 -t myapp .`, and `docker build` "already uses Buildx and BuildKit". | `docker-shell.sh:62` creates its own builder (`--name multi-arch`, driver `docker-container`), then runs `docker buildx build --platform linux/amd64,linux/arm64 --push` (`:66`). Not captured: `prod` never ran, and nobody tried the slide's line. The `multi-arch` builder stays selected afterwards (guide G8). | Both are current Docker. Whether the plain form can output two platforms depends on the active builder: Docker's docs say the default builder needs the containerd image store for it, while a `docker-container` builder always can. The script brings its own builder to be sure. | S09 already explains the builder. Add the slide 13 tag and a GREY note: "lecture: one docker build line · the script brings its own builder". |
| 10 | **Secrets mount mode.** Slide 23's example mounts `./secrets:/secrets:ro`, read-only. | `docker-shell.sh:94`: `-v "$SECRETS_DIR":/secrets`, read-write. The code only reads the key, through `GOOGLE_APPLICATION_CREDENTIALS`. | The script is what runs. `:ro` would match how the key is used (not tested). | Nothing spoken. Optional GREY note on V5's `/secrets` route: "the lecture's example adds :ro". |
| 11 | **Scenario 2's images.** Slides 39–40: the lead builds the images and pushes them to Docker Hub; developers pull them and rebuild "on rare occasions". | The script's registry account is `dlops` (`docker-shell.sh:13`). Its `latest` images date from 2025-02-18 and were built from `pipenv-flexible-workflow`: Python 3.8.17, `pipenv shell`, root (`mega-laptop/72`, `74`). In `generate_text`, `ImportError: cannot import name 'genai'` (`76`). | The captures. Scenario 2 works only once your team's lead pushes from this branch. | S08 already says it. Add the slides 39–40 tag at the fix line; the optional bridge is in §5. |
| 12 | **Base-image tags and sizes.** Slide 10: `python:3.14` about 1.63 GB, `-slim` about 217 MB, `-alpine` about 86 MB. | mega-pipeline uses `python:3.14-slim-bookworm` (Debian 12, pinned), `port_toy` `python:3.14-slim` (Debian 13 at capture time). Docker Engine 29.8.2 lists two numbers per image: `python:3.14-slim` 179 MB disk usage and 43.8 MB content, `-slim-bookworm` 195 MB and 47.2 MB (`port-laptop/66`, `mega-laptop/70`; these are the capture's rebuilt copies of the bases). | Both. The slide's sizes are approximate and depend on how and where they are measured. | Nothing spoken. If needed, a GREY note on S09's column view: "sizes vary by tool and platform · the same slim choice". |

Not counted as conflicts:
- The box label "DockertHub" on slides 39–40 is a typo.
- Slide 17 starts the processor without `-e PORT`; `port_toy`'s default is 9200 (`processor.py:42`),
  so the two behave the same.
- Slide 34 calls `--name gateway` optional because nothing calls the gateway. `port_toy` uses the
  name for `docker exec gateway …`, and pins `container_name:` for the same reason.
- Slide 26 says shell variables only fill the Compose file. S07's `export GEMINI_MODEL` is typed in
  the container's own shell, so the Python process started there sees it at run time. No
  contradiction.
- Slide 22's automatic network would be called `port_toy_default`; `port_toy` names it `toynet`
  (Common 17).
- Slide 42 describes the script as building and running "for development or production". It also
  has `run`, which pulls.
- Slide 43 says Docker Desktop forwards `localhost`. The captures ran Docker Engine on Linux, where
  `-p` behaves the same (`ASSETS.md`). The slide's link anchor `#-runnin-the-app` matches no
  heading, so it opens the top of the repo page.
- Slide 33 letters the paths in teaching order: (a) is the right-hand arrow.

### 5. Proposals

Each item is marked **do** (clear value, low risk) or **nice**.

**General**
- **Tags.** Use `lecture_ref(4, "a–b")` from `explainer.devops`: a GREY tag at the top right,
  opposite the tracker. It prints "Lecture 4 · slides a–b", with no leading zero and "slides" even
  for one slide. The proposals below use the form "Lecture 04 · slides a–b" that this task asked
  for (as in the L03 file). Pick one form for the whole series.
  - Show each tag from the quoted words (`vo.wait_until`) for at least 3 s, and let it leave with
    its beat.
  - Never show the slides or their QR codes.
- **Collisions.** Check each tagged frame. One-line README chips sit in the top band, right of the
  tracker, in most walkthrough scenes. S08 puts a small V4 switchboard at the top. S09's first code
  panel is 13.2 wide. S15's YAML panels run from the top edge in the right column (x > 0.2): there,
  pin the tag at the bottom right of the panel, or start it after the panel swap.
- **Narration budget.** The script has 4,297 words against BRIEF's 3,900–4,300, so any bridge
  pushes past the cap unless something is trimmed.
  - Keep at most one bridge: S10's (15 words). S10 has 209 words against its budget of about 230,
    so trim at least 12 words elsewhere, for example in S07 (355 words against about 320).
  - A bridge also needs its line in `i18n/zh/narration/g2.yaml` (`g1.yaml` for S01–S09), a re-voice
    of the scene and new subtitle cues.
  - Tags and diagram labels need no narration and no Chinese, since there is no Chinese on-screen
    text.
- **Recap card** (nice). The five "Test yourself" questions could each carry a tiny slide number:
  Q1 37–40, Q2 42, Q3 8, 15, Q4 35, Q5 33–34.

**Per scene**
- **S01.**
  - (i) **do** · "Lecture 04 · slides 42–43", at "Two puzzles." The two thumbnails are the two
    tutorials of slides 42 and 43.
  - (ii) **nice** · "These are the two tutorials on the lecture's last slides." (10 words)
  - (iii) None. The teaser thumbnails stay glyph-only.
- **S02.**
  - (i) **do** · "Lecture 04 · slides 37–40", at "A team can get an image two ways." **nice** ·
    "Lecture 04 · slide 42", at "This branch is the same pipeline, built the way a real team would
    build it."
  - (ii) **nice** · "The lecture calls these Scenario 1 and Scenario 2; here, the course plays the
    senior developer." (16)
  - (iii) **do** · In V1, title the two shelves as slides 39–40 title their boxes: "Source Control"
    over the Git shelf, "Images" over the Docker Hub shelf. In phase 2, label the teammate who
    pushes "lead ('senior') developer". **nice** · A thin GREY return arrow from the teammates to
    the Git shelf, labelled "pull request", as slides 38 and 40 draw it (Gap 5). Don't copy the
    slides' colour per operating system, since series colours carry meaning. An optional tiny GREY
    "Win · Linux · Mac" under the three teammates sets up S09's two architectures.
- **S03.**
  - (i) None. Slide 42 only links the branch; S02 carries the tag.
  - (ii) None.
  - (iii) None.
- **S04.**
  - (i) None (S05 carries slide 42).
  - (ii) None.
  - (iii) None.
- **S05.**
  - (i) **nice** · "Lecture 04 · slide 42", at "For code, that identity is a service account, with
    one JSON key."
  - (ii) None.
  - (iii) None.
- **S06.**
  - (i) **do** · "Lecture 04 · slides 23–24", at "Dash v puts the component folder at slash app".
    Then **do** · "Lecture 04 · slide 26", at "Dash e sets an environment variable" (Gap 1).
  - (i) **nice** · "Lecture 04 · slide 11", at "As in lecture 3, the venv lives outside slash app",
    with the GREY note of Conflict 8.
  - (i) **nice** · "Lecture 04 · slide 12", at "build step 2, the system packages".
  - (ii) **nice** · "This is the lecture's bind mount: a host folder on the left, a container path
    on the right." (18)
  - (iii) **do** · On V5's two PINK routes, small GREY end labels: "host folder" at the laptop end,
    "container path" at the container end. This is slide 24's two-sided reading of
    `source:target`. **nice** · On the `/secrets` route, a GREY "the lecture's example adds :ro"
    (Conflict 10).
- **S07.**
  - (i) **nice** · "Lecture 04 · slide 7", at "Next, synthesis audio E-N builds in 8 seconds, its
    system layer cached."
  - (ii) None.
  - (iii) None.
- **S08.**
  - (i) **do** · "Lecture 04 · slide 7", at "after any change in the folder, the copy and uv sync
    steps run again.", with the GREY note "lecture's order: lock files first, code last"
    (Conflict 5, Gap 3).
  - (i) **do** · "Lecture 04 · slides 37–38", at "What is dev for? Adding a package".
  - (i) **nice** · "Lecture 04 · slides 39–40", at "So build locally, with no argument or dev"
    (Conflict 11).
  - (ii) **nice** · "In the lecture's Scenario 2, a lead pushes fresh images; until yours does,
    build locally." (15)
  - (iii) **nice** · After the GREEN package chip drops into the image, the two GREEN file glyphs
    slide toward a small Git shelf labelled "pull request" (slide 38). On the fix card, a small
    GREY "Scenario 2" on the BLUE row.
- **S09.**
  - (i) **do** · "Lecture 04 · slide 13", at "Then one buildx build makes amd64 and arm64 images",
    with the GREY note of Conflict 9.
  - (i) **do** · "Lecture 04 · slides 8, 15", at "The gitignore keeps secrets out of Git, not out of
    images, and no branch has a dockerignore."
  - (i) **nice** · "Lecture 04 · slides 5–6, 10–11", at "The transcribe image alone is 1.48
    gigabytes", with the GREY note of Conflict 7 (Gap 8).
  - (ii) **nice** · "The lecture's dockerignore slide lists secrets for exactly this reason, beside
    caches and data files." (15)
  - (iii) **do** · On the fix card, the `.dockerignore` row lists what this repo needs, in slide 8's
    spirit: `secrets/`, the data folders (`input_audios/`, `text_*/`, `output_audios*/`) and
    `__pycache__/`. Text only; the guide's G6 lists the same folders except `__pycache__/` (Gap 2).
  - (iii) **do** · A GREY row on the same card: "remove images built before the fix · a deleted file
    stays in its layer" (slides 12, 15; Gap 7).
  - (iii) **nice** · In the V5 contrast, draw the missing `.dockerignore` as a dashed sieve outline
    in front of the folder that `COPY . ./` packs. Slide 8's idea is a filter in front of the build
    context. This replaces the dashed chip.
- **S10.**
  - (i) **do** · "Lecture 04 · slide 33", at "Think of each container as its own little computer".
    Then **do** · "Lecture 04 · slide 34", at "A network you create joins them like a small home
    network".
  - (ii) **do**, and the one bridge to keep if any · After "Two containers can both use port 9100
    without any clash.": "The lecture calls this a network namespace: each container is isolated
    until you wire it." (15) It gives the video's metaphor the lecture's term.
  - (iii) **do** · Label V6's PINK phone book "Docker DNS", slide 34's term, where it first
    appears. **nice** · In the opening picture, small GREY labels on the two PINK arrows: "outside:
    laptop → container" and "inside: container → container". These are slide 33's two questions,
    without its (a)/(b) lettering.
- **S11.**
  - (i) **do** · "Lecture 04 · slide 12", at "The two Dockerfiles are almost identical: a slim
    Python 3.14 image, plus curl from apt."
  - (i) **nice** · "Lecture 04 · slide 7", at "Docker reuses the processor's apt layer from the
    cache".
  - (i) **do** · "Lecture 04 · slide 35", at "Dash p publishes a port".
  - (ii) None. The SAY already gives the order: IP address, host port, container port.
  - (iii) Already aligned: the panel's rows wrapped at `&&` are slide 12's shape, and V7 names the
    host port and the container port. **nice** · A thin GREY strip "HOST : CONTAINER" under the
    last two numbers of `127.0.0.1:8090:9100`, slide 35's banner in the series style.
- **S12.**
  - (i) **nice** · "Lecture 04 · slide 33", at "But every connection has two ends". Slide 33's
    footnote: replies come back over the same connections.
  - (ii) None.
  - (iii) None.
- **S13.**
  - (i) **do** · "Lecture 04 · slide 35", from "What does the 127.0.0.1 do?" to "That's why the
    README writes 127.0.0.1: this laptop only.", with the GREY note of Conflict 1.
  - (i) **do** · "Lecture 04 · slides 33–34", at "That's the second puzzle: each container has its
    own localhost."
  - (i) **nice** · "Lecture 04 · slide 28", at "One aside: the processor image has curl too", with a
    GREY note "a Compose healthcheck would use it" (Gap 4).
  - (ii) None. S10 carries the namespace bridge.
  - (iii) Already aligned: the laptop's RED bounce off `:9200` is slide 35's grayed processor. The
    phone book keeps S10's "Docker DNS" label.
- **S14.**
  - (i) **do** · "Lecture 04 · slide 26", at "No image was rebuilt: it's only configuration." (Gap 1)
  - (i) **nice** · "Lecture 04 · slide 35", at "First the street door".
  - (ii) **nice** · "In the lecture's table, dash e values exist only at run time, so a new
    container is enough." (18)
  - (iii) **nice** · Under the two chips `PORT=9300` and `PROCESSOR_PORT=9300`, a four-dot lifetime
    strip "compose file · build · image · container" with only "container" lit: slide 26's columns,
    in the series style.
- **S15.**
  - (i) **do** · "Lecture 04 · slides 17–20", at "Almost every flag you typed by hand has a home in
    it."
  - (i) **do** · "Lecture 04 · slide 27", at "the depends on key starts the processor first".
  - (i) **nice** · "Lecture 04 · slide 21", at "the build command becomes build" (Gap 6).
  - (i) **nice** · "Lecture 04 · slide 22", at "An extra network ls shows that Compose made toynet".
  - (ii) **nice** · "The lecture adds a warning: started is not ready, and a health check makes
    Compose wait." (16)
  - (iii) **do** · In V8, the GREY notes of Conflict 4: on `volumes:` "the lecture's by-hand run had
    -v · slide 17"; on `depends_on` "= the order you typed them · started, not ready".
  - (iii) **nice** · As each flag lands, a small GREY "(-p)", "(-e)" or "(-v)" beside its key, as
    slide 20 labels them. Under the processor panel, the GREY note of Conflict 2. On the panel
    header, the note of Conflict 3.
- **S16.**
  - (i) **do** · "Lecture 04 · slide 29", at "Back to the README's order: up dash d starts the app in
    the background".
  - (i) **nice** · "Lecture 04 · slides 23–24", at "The gateway's folder is mounted".
  - (i) **nice** · "Lecture 04 · slide 31", at "Next lecture, a command-line container calls a
    database container by name on a Compose network" (Gap 10).
  - (ii) None.
  - (iii) **nice** · The recap card's slide numbers (see General).
