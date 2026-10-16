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
  them by text. Changes in this copy: the L03 deck's first "Pick a Smaller Base Image" slide and
  its "Measure It" slide (`docker images` / `docker history`, footer 43) are gone, which is why the
  footers jump from 42 to 44 between slides 12 and 13. Slide 9's bullets were reworded and gained a
  pure-Python footnote. Slide 13 dropped `--load` from its single-platform command. Slide 17 added
  `--name gateway` to the last `docker run`. Slides 11, 19 and 20 have reworded captions. Where the
  two decks differ, this deck is the newer wording.
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
  default with compatible wheels"), `python:3.14-alpine` (~86 MB; smaller, check that your
  dependencies support Alpine). A blue callout from the table says to use build tools in a build
  stage and leave them out of the final image. Purpose: the size gap and why it exists. A re-draw:
  three bars at true scale (the full image is about 7.5× slim), each labelled with what it
  contains.
- **Slide 11 · two stages.** One Dockerfile in two blocks. The top block, `FROM python:3.14 AS
  builder`, installs `uv`, copies the lock files and runs `uv sync`. The bottom block, `FROM
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
    Callouts: green "same id as the `RUN --mount`, that is the link"; blue "a local path, the token
    file on your machine".
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
  carries `hello`; a bottom arrow back carries `HELLO`. Below them are the six by-hand commands:
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
  slide ends that callout with a red "Delete!".
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
| "Ready-to-install package (wheel)", "Source package", "Source distribution", "Built wheel", "native extensions" | 9 | Not in the READMEs. The mega-pipeline Dockerfile only mentions wheels in a comment on `UV_LINK_MODE`. |
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
| "detached" | 29 | `port_toy` README runs Compose in the foreground and stops it with Ctrl+C. |
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
- Where you write a variable decides when it exists: the `.env` file and shell variables only fill
  the Compose file, not the container, and `ARG` / `build.args` disappear after the build. (26)
- "Up" is not "ready": `depends_on` alone only orders start-up. Waiting needs a healthcheck and
  `condition: service_healthy`, and the condition names are fixed keywords. (27–28)
- `docker compose down -v` deletes your named volumes, i.e. your data; the slide marks it with a
  red "Delete!". (29)
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
- Slides 17–30 and slide 35's diagram publish `8090:9100`, i.e. on all host addresses. Only slide
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
