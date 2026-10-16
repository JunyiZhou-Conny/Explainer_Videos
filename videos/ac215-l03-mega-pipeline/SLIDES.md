# L03 lecture slides — Containers II

Source: one deck, `L03_containers_ii.pptx_2_` (71 slides), titled "Lecture 3: Containers II"
(AC215/E115, Pavlos Protopapas, SEAS/Harvard). These are the instructor's lecture slides (PDF),
provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page
numbers. I wrote this digest from the deck's extracted text and from all eight contact sheets, and
enlarged slides 4, 15, 18, 19, 25, 27, 50, 61–63, 65, 67 and 68 to read their diagrams. Everything
below is in my own words. Only short titles, terms, URLs and single code lines are quoted. The
tutorial side of the lecture is in [`digest.md`](digest.md).

Two warnings for anyone citing the deck:

- **The printed footer numbers are not the slide numbers.** The deck was cut from a longer one.
  Its footers run 1, 8–10, 14–30, 73, 33, 74–79, 34–40, 40, 43, 41, 42, 44–72, 80, 81. Always
  cite the PDF page numbers used here.
- **How the deck maps onto the series.** Slides 1–29 (recap, monolith vs microservices, and the
  Mega Pipeline tutorial) belong to this episode. Slides 30–69 (build optimization, Docker
  Compose, networking, team workflows) appear again in the Lecture 4 deck, "Containers II-b". I
  checked that deck by its slide titles only. The series pairs those topics with `port_toy` and
  `mega-pipeline@flexible-workflow` in the L04 episode. The slides' Compose and networking example
  (gateway + processor, ports 8090/9100/9200) is the `port_toy` app. Slide 70 previews
  "Connecting to the Cloud", which the course map lists as Lecture 10.

## Outline

The deck has seven numbered sections (slide 2). Each section opens with a divider slide that
repeats the outline with the current section in bold.

- Slide 1 · title slide
- Slide 2 · outline: Recap; Containers in Architecture: Microservices vs. Monolithic; Tutorial;
  Build Optimization; Docker Compose; Networking; Team Workflows
- Slides 3–4 · **1. Recap**
  - 3 · divider, with a "just a mini recap" meme
  - 4 · "Recap: Environments vs Virtualization vs Containerization" (three layer stacks)
- Slides 5–21 · **2. Containers in Architecture: Microservices vs. Monolithic**
  - 5 · divider, with a Cookie Monster picture choosing between plates labelled "Microservices"
    and "Monolithic"
  - 6 · "Why use Containers?": the online cheese store scenario, traditionally built as a monolith
  - 7 · "Monolithic Architecture" diagram
  - 8 · the same diagram, with a callout that defines HTML, JSON, REST and HTTP
  - 9 · monolith advantages
  - 10–11 · monolith disadvantages (six of them)
  - 12 · "Applications have changed dramatically": a decade ago vs today
  - 13 · the same, plus a "Data Science" point and a meme photo
  - 14 · the monolith diagram again, as a lead-in to the next slide
  - 15 · "Today: Microservice Architecture" diagram
  - 16 · microservice advantages
  - 17 · microservice disadvantages, with a picture captioned "Docker + Kubernetes"
  - 18 · "Software Development Workflow (no Docker)"
  - 19 · "Software Development Workflow (with Docker)"
  - 20 · slide 19 faded behind the open questions about who owns the Dockerfile and the uv files,
    with a meme ("This seems like a lot.")
  - 21 · slide 19 with a Simpsons meme labelled "Students" / "Prof. Protopapas"
- Slides 22–29 · **3. Tutorial** (slides 24–29 have a gray background)
  - 22 · divider
  - 23 · "GCP Authentication Methods": five ways to authenticate
  - 24 · "Tutorial - Building the Mega Pipeline App": goals (with a QR code)
  - 25 · the pipeline diagram (six numbered stages around a GCS bucket)
  - 26 · "Tutorial - Team Challenge!": teams of 5, prizes (Oprah "you get a reward" meme)
  - 27 · "Tutorial (T5)": screenshot of the class Mega Pipeline web app
  - 28 · app URL, the five team tasks A–E, the instructions link (with a QR code)
  - 29 · picture only: a cartoon GIF captioned "Delete! Delete!" (no text; purpose not stated)
- Slides 30–43 · **4. Build Optimization** (slides 35, 42 and 43 have a peach background)
  - 30 · divider
  - 31 · "Build Optimization: Why Bother?": four costs of a fat image
  - 32 · the same, with the takeaway banner
  - 33 · "Layer Caching: Order Matters"
  - 34 · ".dockerignore: Shrink the Build Context"
  - 35 · "How Python Packages Are Installed": wheel vs sdist
  - 36 · "Pick a Smaller Base Image" (first version)
  - 37 · "Pick a Smaller Base Image" (reworded version, same printed footer 40)
  - 38 · "Measure It": `docker images` and `docker history`
  - 39 · "Multi-Stage Builds"
  - 40 · "Fewer, Leaner Layers"
  - 41 · "Building for the Target Platform"
  - 42 · "Build Secrets: Tokens for Dockerfile RUN Steps"
  - 43 · "Build Secrets: Supply the Token from Your Terminal", with an anti-pattern table
- Slides 44–59 · **5. Docker Compose**
  - 44 · divider
  - 45 · "The Problem Compose Solves": the gateway/processor example started by hand
  - 46 · the same, with the takeaway banner
  - 47 · "What Is Docker Compose?": by hand vs with Compose
  - 48 · "compose.yaml": the file mapped to `docker run` flags
  - 49 · "build: vs image:"
  - 50 · "Networking for Free"
  - 51 · "Volumes"
  - 52 · "Volumes: Bind Mount vs Named Volume"
  - 53 · "Environment": inline values vs `env_file`
  - 54 · "Environment: Build Time vs Run Time" (peach background)
  - 55 · "Startup Order": what `depends_on` guarantees
  - 56 · "Startup Order": waiting for a healthcheck
  - 57 · "Everyday Compose Commands"
  - 58 · "The Whole App in One File"
  - 59 · "When Compose Isn't Enough": Compose vs Kubernetes
- Slides 60–63 · **6. Networking**
  - 60 · divider
  - 61 · "Your Containers Need to Talk": the two paths
  - 62 · "Gateway → Processor: One Shared Network"
  - 63 · "Browser → Gateway: Publish a Port"
- Slides 64–69 · **7. Team Workflows**
  - 64 · divider
  - 65–66 · "Workflow with Docker: Scenario 1 (early stages of development)", two steps
  - 67–68 · "Workflow with Docker: Scenario 2 (later stages of development)", two steps
  - 69 · "Workflow with Docker: A Flexible Approach"
- Slide 70 · "Next time: you'll need real authentication"
- Slide 71 · closing "THANK YOU" picture

## Key ideas

1. **Three ways to isolate an app, from thin to thick.** A virtual environment isolates only an
   app's Python libraries on a shared interpreter. A VM gives each app a whole guest OS on a
   hypervisor. A container packages an app with its binaries and libraries and runs on Docker
   over one shared OS, so more of them fit on the same machine. (Slide 4)
2. **A monolith is one program, one stack and one database.** In the cheese store example, the
   UI, catalog, reviews and orders are modules inside one Java server, backed by one Oracle
   database, and browsers and phones talk to it over HTTP with HTML or REST/JSON. (Slides 6–8, 14)
3. **A monolith is simple at first and gets harder over time.** Tools support it well, it ships
   as one package, and you scale it by running more copies of the whole app. But it gets harder
   to change and debug. One failing part can take everything down. Patching one module is
   awkward, and new technology is hard to adopt. Startup is slow, and newcomers must learn the
   whole codebase. (Slides 9–11)
4. **Apps have changed.** Ten years ago an app was a long-lived monolith on one stack and one
   server. Today apps are built from loosely coupled parts, released often and spread over many
   servers. Data-science apps also pull in many data sources and models. (Slides 12–13)
5. **Microservices split the app into services behind an API.** Each module becomes its own
   service with its own storage (database, cloud store, models). An API service routes requests
   from browser, mobile and edge clients. The gains mirror the monolith's pains: easier
   maintenance, fault isolation, targeted patches, freedom of technology, parallel startup.
   (Slides 15–16)
6. **Microservices move the complexity into development and deployment.** Many technologies
   mean many dependency sets to manage, and scaling the whole app gets intricate. The slide's
   answer is "Docker + Kubernetes". (Slide 17)
7. **Docker changes the team's delivery chain.** Without Docker, every developer machine, the
   build server and every production server need the right software installed by hand, and
   production runs a different OS version than the laptops. With Docker, each machine only needs
   Docker. The build server builds an image per release and pushes it to a container registry,
   and production pulls it and runs it. (Slides 18–19)
8. **That raises ownership questions, which section 7 answers.** Who writes the Dockerfile and
   where does it live? Prebuilt images or local builds? Who manages `pyproject.toml` and
   `uv.lock`? (Slides 20–21, answered on 65–69)
9. **There are several ways to authenticate to Google Cloud.** OAuth 2.0 is for users. Service
   accounts (part of IAM) are for automated server-to-server work. API keys are lightweight but
   less secure. Default service accounts come attached to Compute Engine, Kubernetes Engine and
   App Engine. Workload Identity Federation lets outside identities in. (Slide 23)
10. **The tutorial builds a multilingual cheese podcast as a containerized pipeline.** A recorded
    draft is transcribed, improved by a language model, voiced in English, translated, and voiced
    again. Every stage reads its input from a shared GCS bucket and writes its output back. An
    optional ElevenLabs step uses a custom voice. (Slides 24–25)
11. **The tutorial runs as a team race.** Teams of five each complete five tasks (A
    `transcribe_audio`, B `generate_text`, C `synthesis_audio_en`, D `translate_text`, E
    `synthesis_audio`). Results appear per team in the class web app, and there are prizes.
    (Slides 26–28)
12. **Image size is a cost you pay on every deploy.** Each release is pushed to a registry and
    pulled to every server. Extra packages widen what you must secure. Slow builds slow every
    change, and storage multiplies by versions × servers. The rule: ship only what is needed to
    run, and keep the part that changes small. (Slides 31–32)
13. **Order Dockerfile steps from rarely changed to often changed.** Each instruction is a cached
    layer, and changing one rebuilds every layer after it. Copy the dependency files and install
    them first, then copy the code. A code edit then re-runs only the last step. (Slide 33)
14. **`.dockerignore` trims the build context.** Docker sends a folder to the builder before it
    builds. Excluding history, caches, local environments, data files and secrets makes builds
    faster and keeps secrets and junk out of the image. (Slide 34)
15. **How a package installs decides which base image you need.** A wheel is prebuilt and only
    unpacked. A source distribution must be built first, which may need compilers. The full
    `python:3.14` image (~1.63 GB) carries those tools. `-slim` (~217 MB) is the default when
    wheels exist. `-alpine` (~86 MB) uses musl, so wheels are often missing and packages compile.
    A smaller base also means fewer known vulnerabilities. (Slides 35–37)
16. **Measure before you optimize.** `docker images` gives each image's total size, and
    `docker history` gives each layer's size, so you can find the fat layer. (Slide 38)
17. **Multi-stage builds keep build tools out of the final image.** A builder stage on the full
    image installs dependencies into `.venv`. A slim runtime stage copies only that `.venv` and
    the code. (Slides 37, 39)
18. **Layers only add.** Deleting a file in a later layer does not shrink an earlier one, so
    install and clean up in the same `RUN`, chained with `&&`. Skip extras with
    `--no-install-recommends` (apt) and `--no-cache-dir` (pip). (Slide 40)
19. **Build for the CPU you will run on.** `--platform` targets the deployment architecture
    (Apple Silicon is arm64; Intel/AMD is amd64; clouds offer both). `--load` keeps the image
    locally, and `--push` sends a multi-platform image to a registry. (Slide 41)
20. **Give a build step a token through a secret mount.** The token file is mounted for one
    `RUN` step only and is passed with `docker build --secret`, using the same id. `ENV`, `ARG`
    and `COPY` would leave it in the image config, the build history or a layer. (Slides 42–43)
21. **Compose turns a pile of `docker run` commands into one file and one command.** Starting a
    multi-container app by hand means a network, the right start order and many flags per service,
    repeated after every change. `compose.yaml` declares services, networks and volumes, and
    `docker compose up`/`down` starts and removes them all. Each key matches a `docker run` flag.
    (Slides 45–48, 58)
22. **Each service gets its image from a local build or a registry.** `build:` builds from a
    folder's Dockerfile. `image:` pulls a prebuilt image. (Slide 49)
23. **Compose creates a network, and services find each other by name.** The service name is the
    hostname, so the gateway calls `http://processor:9200` without any `docker network create`.
    (Slides 48, 50)
24. **Volumes come in two kinds with the same syntax.** In `source:container`, a path on the left
    means a bind mount of a host folder (here read-only with `:ro`). A bare name means a named
    volume that Docker stores and keeps, declared under a top-level `volumes:`. (Slides 51–52)
25. **Where you set a variable decides when it exists.** Compose `environment:` and `env_file:`
    inject values at run time, and the `.env` file keeps secrets out of Git and out of the YAML.
    Dockerfile `ENV` lives in the build, the image and the container. `ARG` and Compose
    `build.args` exist only during the build. `.env` and shell variables fill `${VAR}` inside
    the Compose file itself. (Slides 53–54)
26. **`depends_on` orders startup but does not wait for readiness.** "Up" only means the
    container started. To wait until the app answers, give the dependency a `healthcheck` and use
    `condition: service_healthy`. (Slides 55–56)
27. **The everyday Compose commands.** `up` (`-d` to detach, `--build` to rebuild), `ps -a`,
    `logs -f`, `down`, and `down -v`, which also deletes named volumes and so your data.
    (Slide 57)
28. **Compose stops at one machine.** It suits development and a single small server. Scaling
    over many machines, self-healing, rolling updates and cross-node load balancing need
    Kubernetes, which uses the same idea of declared services found by name. (Slide 59)
29. **Containers are isolated until you open two kinds of path.** Container to container: put
    both on one network and use names (Docker DNS, no IPs). Browser to container: publish a port,
    `HOST:CONTAINER`, so `localhost:8090` on the laptop reaches port 9100 in the gateway. Each
    container has its own network namespace (from Containers I). (Slides 61–63)
30. **Teams pick a Docker workflow by stage.** Early on, a senior developer writes the Dockerfile
    and uv files. Everyone builds locally and develops in containers, and changes come back as
    pull requests that the senior developer merges and consolidates. Later, the senior developer
    also builds the images and pushes them to Docker Hub. Developers pull and run them and
    rebuild rarely. No workflow is perfect; what matters is clear communication and rules.
    (Slides 65–69)
31. **The class key is a shortcut, and the next lecture replaces it.** Handing out one shared
    service-account key works for a class demo but not in real projects. Containers will need
    their own identities for private registries, cloud storage and Google APIs. (Slide 70)

What the slides leave to the tutorial: they never show the component Dockerfile line by line, the
`uv init --bare` / `uv add` loop, the `-v "$(pwd):/app"` bind-mount development loop, the `cli.py`
flags, `group_name`, `GOOGLE_APPLICATION_CREDENTIALS`, the bucket's folder names, the non-root
`app` user or the `ENTRYPOINT`/`CMD` shell. A scene that needs any of these must take them from
`digest.md`.

## Diagrams

- **Slide 4 · three isolation stacks.** Three columns side by side, labelled underneath "Virtual
  Environments", "Virtualization", "Containerization". Every column has the same two bottom bars:
  "Infrastructure" (charcoal) and "Operating System" (gray). The third bar differs: "Python"
  (navy, yellow text), "Hypervisor" (light gray) and "Docker" (blue, whale logo). On top:
  - Left: three short dashed boxes (blue, green, red), each "AppN" over "Libs", tagged "Venv".
  - Middle: three tall dashed boxes, each "AppN" over "Bins/lib" over a large "OS" block, tagged
    "VM".
  - Right: six small dashed boxes in two rows of three, each "App" over "Bins/lib", tagged
    "Container". The top row is App1/App2/App3 (blue/green/red). The bottom row is App3/App2/App3
    in gold/purple/magenta.

  Purpose: show what each method copies per app (libraries only; a whole OS; binaries and
  libraries), and that containers are light enough that twice as many fit and one app can run
  several times. Our series already has a VM/container diagram in the toolkit; this slide adds the
  venv column.
- **Slide 7 (repeated on 8 and 14) · monolith.** Two clients on the left: "Browser Apps" (browser
  window icon) and "Mobile Apps" (phone icon). Their lines carry the labels "HTML / REST / JSON"
  and "REST / JSON", meet in an elbow connector and enter one gray box, with arrowheads back
  toward the clients for the responses. The gray box is the "Server" (rack icon). It holds four
  stacked bars: "Storefront UI Module" (blue), "Catalog Module" (green), "Reviews Module"
  (orange), "Orders Module" (red), with a Java logo below. A double-headed arrow joins it to one
  database cylinder labelled "Database" / "Oracle". Slide 8 adds a speech bubble over the client
  links that defines the four web terms. Purpose: every feature in one process, one language and
  one shared database.
- **Slide 15 · microservices.** Left column: three clients, "Browser Apps", "Mobile Apps" and
  "Edge Device Apps" (chip icon). Each line is labelled "REST / JSON", and the lines join a
  vertical trunk. From the trunk, one arrow goes to "Storefront UI" (blue, labelled "HTML") and
  one to a large gold "API Service". From the API Service, four arrows fan out to the modules,
  and each module has a double-headed arrow to its own store:
  - "Catalog Module" (green) ↔ "Database"
  - "Reviews Module" (orange) ↔ "Cloud Store" (cloud icon)
  - "Orders Module" (red) ↔ "Database"
  - "Recommendation Module" (purple) ↔ "Models" (two light-bulb icons)

  Purpose: the same features as slide 7, now separate services behind one entry point. Each picks
  its own storage, and an ML component (recommendation + models) slots in as just another
  service. A re-draw can animate slide 7's gray box splitting into these boxes.
- **Slide 18 · delivery chain without Docker.** Left column: three colored OS panels, each with a
  team icon below. "Windows" (green) has Node.js + Python, "Linux" (red) has C++ + Python, "Mac"
  (blue) has Node.js + Python, each with a database-stack icon for installed software. A callout
  defines Node.js. Hollow block arrows run left to right through three dotted boxes: "Source
  Control" (holding "GitHub"), "Build Server" (one Linux panel with a server icon), "Test Servers
  / Production" (two Linux panels, one database icon and one server icon). The captions under the
  stages say:
  - Developers: each machine needs its own OS-specific installs.
  - Source Control: everyone pushes code there.
  - Build Server: it needs all the software and frameworks, and it pulls the code.
  - Production: it needs everything installed too, and it runs a different OS version than the
    laptops.

  Purpose: count the places where dependencies must be installed by hand.
- **Slide 19 · delivery chain with Docker** (also the base of 20 and 21). The same left-to-right
  chain. Each OS panel now holds three identical dashed yellow squares (containers). The build
  server holds a small stack of overlapping squares (images), and each production Linux panel
  holds one square. The captions say that every stage only needs Docker. Containers are set up
  once. The build server builds images per release and pushes them to a container registry.
  Production pulls from the registry and runs them. The registry is named in the captions but not
  drawn as a box. Purpose: one artifact replaces per-machine installs. A re-draw should add the
  registry box between the build server and production.
- **Slide 25 · Mega Pipeline data flow.** Six tiles, each with a numbered colored badge above and
  an icon:
  - **1** "Record Audio" (pink, red microphone), with the instructor's cartoon portrait under it.
  - **2** "Transcribe Audio" (blue, "did you know?" bubble).
  - **3** "Generate Text" (yellow, notepad).
  - **4** "Synthesise Audio" (green, speaker), raised above tile 5.
  - **5** "Translate Text" (purple, A→文 icon).
  - **6** "Synthesise Audio" (green, speaker).

  Hollow "⇒" arrows give the logical order 1 → 2 → 3 → 5 → 6, plus a "⇒" into tile 4 from the
  left, which branches off Generate Text's output. A wide light-gray box along the bottom with a
  cloud icon is labelled "GCS Bucket" / "Audio + Text Files". Colored vertical links tie the
  tiles to the bucket:
  - red elbow, one-way into the bucket, from the Record Audio portrait;
  - blue (2), yellow (3) and purple (5), double-headed;
  - green from tile 4 straight down to the bucket, double-headed, drawn behind tile 5;
  - green elbow from tile 6 to the bucket's right end, double-headed.

  Purpose: the stages never call each other; the bucket is the hand-off. Tiles 2–6 are Tasks A–E
  of slide 28, and tile 1 is the instructor's recording. The README's ElevenLabs bonus is not
  drawn.
- **Slide 27 · class web app (screenshot).** A page headed "AC215: Mega Pipeline App" (dark red
  bar). It has seven columns with tiny icon headers, which read as: Audio Prompts, Transcribed
  Audio, Generated Text, Synthesised Audio, Translated Text (French flag), Synthesised Audio, and
  a last column headed by the instructor's portrait (the custom-voice audio). Under each header
  is a list of entries per team ("Team: group-NN", plus one "pavlos"). Text columns show snippets
  (English podcast text; French in the translated column), and audio columns show audio players.
  Purpose: the leaderboard where each team's output appears stage by stage. Not a mechanism; a
  scene can mimic it as a grid of team rows × stage columns lighting up.
- **Slide 33 · cache order.** A three-line Dockerfile in a code panel, each line with an annotation
  arrow:
  - `COPY pyproject.toml uv.lock ./`: dependencies change rarely and code changes constantly, so
    copy the dependency files first;
  - `RUN uv sync`: stays cached until the dependencies change;
  - `COPY . .`: the only layer that re-runs on a code edit.

  For a scene, draw the layers as a stack. Editing code turns only the top layer red. In the wrong
  order (copy everything, then sync), the same edit turns the sync layer and everything above it
  red.
- **Slide 34 · `.dockerignore` patterns.** A center column of six monospace patterns, each tied by
  a curved arrow to a colored tag. Left tags:
  - "compiled Python bytecode caches" → `__pycache__/`
  - "installed JS packages, reinstalled in the image" → `node_modules/`
  - "bulky local data files, not needed at build time" → `*.csv`

  Right tags:
  - "repository history, metadata not needed to run" → `.git`
  - "local virtual environment, rebuilt inside the image" → `.venv/`
  - "credentials & keys, must never enter the image" (red) → `secrets/`

  Purpose: what is cut from the folder before it is sent to the Docker daemon.
- **Slide 35 · sdist → wheel.** Two file trees joined by a big blue arrow, with the caption
  "Build: prepare files for installation". Left, "Source distribution" `cheese_utils-1.0.tar.gz`:
  `pyproject.toml`, `src/cheese_utils/__init__.py`, `prices.py`, `tests/test_prices.py`. Right,
  "Built wheel" `cheese_utils-1.0-py3-none-any.whl`: `cheese_utils/__init__.py`, `prices.py`
  and a `cheese_utils-1.0.dist-info/` folder with `METADATA`, `WHEEL`, `RECORD`. Purpose: building
  drops the project scaffolding (config, tests) and adds install metadata. A wheel only needs
  unpacking.
- **Slides 36–37 · base-image table.** Three rows (`python:3.14` ~1.63 GB, `-slim` ~217 MB,
  `-alpine` ~86 MB) with a "when to use" column. Slide 36's callout recommends slim for most
  Python and alpine only for experts, and says a smaller base means fewer CVEs. Slide 37's callout
  points to multi-stage builds. A scene can show three bars at true scale (1.63 GB is about
  7.5× slim and 19× alpine).
- **Slide 38 · measuring.** Two terminal panels.
  - Left: `docker images python` lists `3.14` at 1.63GB and `3.14-slim` at 217MB, with the note
    "same Python, a leaner base".
  - Right: `docker history python:3.14-slim` lists layers from newest to oldest: the `CMD` (0B),
    symlinks (16.4kB), Python + pip build (45.2MB), `ENV` lines (0B), apt runtime deps (13.1MB),
    and the Debian base (109MB). The note says to find the fat layer.

  Caution: the listed layers add up to about 167 MB, not 217 MB (the rows are abridged with "…"),
  so a scene should not animate them summing to the total.
- **Slide 39 · multi-stage build.** A Dockerfile in two blocks with right-hand annotations:
  - builder stage on `python:3.14`: installs uv, copies the lock files, `uv sync` into `.venv`;
  - runtime stage on `python:3.14-slim`: `COPY --from=builder` brings over only `/app/.venv`,
    then the code, then a `CMD` that runs the venv's Python.

  A callout sums it up: build in one stage and copy what the app needs into the final one. For a
  scene, draw a big builder box (toolchain, caches, `.venv`) next to a small runtime box. Only the
  `.venv` crosses, and the builder box is discarded.
- **Slide 40 · additive layers.** One `RUN` chain (apt update → install `build-essential` with
  `--no-install-recommends` → `rm -rf /var/lib/apt/lists/*`) with four annotations: trim the
  extras, what build-essential is, chain related commands with `&&`, and a warning that a separate
  cleanup layer does not shrink the image. Mechanism to draw: layer N adds files. Layer N+1
  "deletes" them by masking them, but layer N still ships them. The cure is to download and delete
  in the same layer.
- **Slide 41 · target platform.** Two `docker build` commands with annotations on `--platform`,
  `--load` and `--push`, and a small legend: Apple Silicon = arm64, Intel/AMD = amd64, clouds
  either, so check the target.
- **Slides 42–43 · build secrets.** Slide 42 shows a Dockerfile snippet with four annotations:
  - the `# syntax=` first line enables `--mount`;
  - the `id` names the secret, and the same id is reused on `docker build`;
  - `/run/secrets/gh_token` is a path inside the container that exists only for this step;
  - `$(…)` reads that file into `GH_TOKEN`.

  Slide 43 shows the matching `docker build --secret id=…,src=…` with the note that the shared
  id is the link, and a three-row anti-pattern table (`ENV`, `ARG`, `COPY` and where each leaves
  the token). Scene: a token file on the laptop is lent to one `RUN` step as a temporary mount and
  never lands in a layer.
- **Slide 45 · the example app.** Two rounded boxes: "gateway" ("serves the page") and
  "processor" ("UPPER-cases the text"). An upper arrow labelled "hello" goes from gateway to
  processor, and a lower arrow labelled "HELLO" comes back. Below it is the seven-line by-hand
  command sequence.
- **Slide 47 · by hand vs Compose (table).** Three rows. Network: create and attach each by hand,
  automatic and shared with Compose. Start: N × `docker run` in order, or `docker compose up`.
  Tear down: stop and remove each, or `docker compose down`.
- **Slides 48–49 · annotated `compose.yaml`.** The gateway/processor file, with labels linking
  `ports` to `-p`, `volumes` to `-v` and `environment` to `-e`, and a note that each service entry
  name is also its hostname. Slide 49 re-annotates the same file: `build: ./gateway` means build
  from local files, and `image: ac215/processor:1.0` means pull from a registry such as Docker Hub.
- **Slide 50 · Compose network.** A light-blue rounded panel labelled "compose network —
  auto-created on docker compose up" holds the boxes "gateway" → "processor", with the arrow
  labelled `http://processor:9200`. A dark-blue speech callout below lists the two commands you
  never had to run (`docker network create app-net`, `docker run --network app-net --name
  gateway …`).
- **Slides 51–52 · volumes.** Slide 51 shows the gateway service with `- ./secrets:/secrets:ro`
  (tagged bind mount, host path; `:ro` = read-only) and `- models:/models` (tagged named volume,
  persisted by Docker), plus a top-level `volumes: models:` (tagged "declare the named volume
  here"). Slide 52 isolates the two lines. Both right sides are tagged "container path". The left
  sides are tagged "a host folder you chose" and "named volume (Docker owns the storage)".
- **Slide 54 · variable lifetime (table + mini diagram).** Rows are where you write a variable.
  Columns are the Compose file (`${VAR}`), the build, the image and the running container:
  - Dockerfile `ENV`: build ✓, image ✓, container ✓
  - Dockerfile `ARG` and Compose `build.args`: build only
  - Compose `environment:` / `env_file:`: container only
  - the auto-loaded `.env` file and a shell `$VAR`: the Compose file only

  Below, a `.env` holding `TAG=1.0` (or `export TAG=1.0`) has an arrow labelled "fills" into
  `image: ac215/processor:${TAG}`. A scene can draw four timeline lanes (compose file → build →
  image → container) and light each row's span.
- **Slides 55–56 · startup order.** The same file. On 55, `depends_on: - processor` is tagged
  "processor comes up first, then gateway", and a callout warns that "up" means started, not
  ready. On 56, the short form becomes `processor: condition: service_healthy`. The processor gets
  `healthcheck: test: curl -f localhost:9200/health`. The tags say the condition value is a fixed
  keyword (the other two being `service_started` and `service_completed_successfully`), the
  healthcheck is the probe, and gateway is held until it passes. Scene: two timelines, "container
  started" vs "health OK", with gateway's start pinned to the second.
- **Slide 57 · command map.** Seven `docker compose` lines in a column, each with a tag: `up`,
  `-d`, `--build`, `ps -a`, `logs -f`, `down`, `down -v` (tagged in orange: it also deletes named
  volumes, "your data").
- **Slide 59 · Compose vs Kubernetes (table).** Scope: one machine vs a cluster. Great for:
  development and a small single server vs production scale, self-healing and rolling updates.
- **Slide 61 · two paths.** Three boxes in a row: "your browser / on your laptop" → "gateway /
  service" → "processor / service". The first arrow is labelled "(b) browser → gateway" and the
  second "(a) gateway → processor". The arrows show request direction, and responses return on the
  same connection.
- **Slide 62 · shared network.** A rounded rectangle labelled "`app-net` — every container here
  reaches any other by name" holds "gateway `http://gateway:9100`" → "processor
  `http://processor:9200`". Below it are three numbered steps with commands: create the network,
  attach and name each container, reach it by name through Docker DNS (no IP). A tag notes that
  naming the gateway is optional here because nothing calls it. A callout says Compose does all
  three steps for free.
- **Slide 63 · published port.** On the left, a box "your browser `localhost:8090`". An arrow
  labelled "port forwarding `-p 8090:9100`" crosses into an `app-net` rectangle holding "gateway
  :9100" (bold) and "processor :9200" (grayed out: not reachable from the laptop). A banner reads
  "8090 : 9100 = HOST : CONTAINER". Two code panels show the same mapping as a `docker run` flag
  and as a Compose `ports:` entry, both bound to `127.0.0.1`.
- **Slides 65–68 · team workflows.** On the left are the same three OS panels (Windows, Linux,
  Mac), each with three container squares and a team icon. Top center is a pink "'Senior'
  Developer" panel with one long container bar and a red team icon. Below it is a dotted "Source
  Control / GitHub" box; on 67–68 there is also an "Images / DockertHub" box to its right.
  - 65: senior → GitHub (down arrow), then GitHub → developers (left arrow).
  - 66: developers → GitHub (right arrow). The senior developer merges the pull requests and
    consolidates the Dockerfile and uv files.
  - 67: senior → GitHub and senior → Docker Hub (two arrows), then GitHub → developers. The text
    adds that developers also pull images from Docker Hub, though no arrow is drawn from it.
  - 68: developers → GitHub (pull requests). The senior developer merges, rebuilds and pushes new
    images.

  Purpose: who owns the Dockerfile and the lock files, and where images come from, early vs late
  in a project. A re-draw should add the missing Docker Hub → developers arrow on 67.
- **Not diagrams:** slides 12–13 are a two-column text comparison. The pictures on slides 3, 5,
  13, 17, 20, 21, 26, 29 and 71 are memes or GIFs. Slides 24 and 28 carry QR codes. Slides 31–32
  and 46 are text slides with takeaway banners.

## Terms the lecture uses

| Lecture term | Slides | Note on the tutorial README / digest |
|---|---|---|
| "Virtual Environments" / "Virtualization" / "Containerization"; "Hypervisor"; "Bins/lib" | 4 | Recap of L01–L02 vocabulary; not used in the mega-pipeline README. |
| "Monolithic Architecture" / "Microservice Architecture" | 5–17 | The README says the tutorial will "simulate a microservice architecture" (`README.md:7`). It never says "monolith". |
| "Module" (Storefront UI, Catalog, Reviews, Orders, Recommendation); "API Service" | 7, 14, 15 | The README calls the five pieces "components" (and "services"), not modules. |
| "loosely coupled components" | 12, 13 | Matches the README's "independent services". |
| "Source Control", "Build Server", "Test Servers / Production" | 18–21 | Not in the README. The tutorial has no build server; each student builds locally. |
| "container registry" | 19–21 | The README only offers an optional push to "Docker Hub" (`transcribe_audio/README.md:136-140`). |
| "DockerHub" (written "DockertHub" in the box labels) | 67, 68 | README: "Docker Hub". The box label is a slide typo. |
| "uv files" (= `pyproject.toml` + `uv.lock`) | 20, 65–68 | The README names the files and the `uv init --bare` / `uv add` steps, never "uv files". |
| "OAuth 2.0", "Service Account (part of IAM in GCP)", "API Key", "Default Service Accounts", "Workload Identity Federation" | 23 | The README uses the same phrase "Service Account — part of IAM in GCP" (`README.md:95`). The other four methods are not in the tutorial. |
| "Mega Pipeline App"; "Tutorial (T5)" / "Tutorial 5" | 24–28, 70 | Same app name as the README title. The README does not number it; "T5" is the course's tutorial number. |
| "Record Audio", "Transcribe Audio", "Generate Text", "Translate Text", "Synthesise Audio" | 25 | The README and folder names spell it "synthesize" / "synthesis" (`synthesis_audio_en`, `synthesis_audio`). The slide's step 1 is the instructor's recording (README step 1). |
| "Task A … Task E" with folder names | 28 | Identical to `README.md:116-120`. |
| "GCS Bucket", "Audio + Text Files" | 25 | README: bucket `mega-pipeline-bucket` with named folders (`README.md:71-80`). |
| "Teams", "Team Challenge", "reward" | 24, 26, 28 | README: "groups", "group name", "leaderboard". Slide 24 says separate teams per component. Slide 26 and the README (`README.md:52`) say each team builds all five. Follow the README and slide 26. |
| "build context" | 34 | Not in the README; `digest.md` uses it. |
| "daemon" | 34 | Not in the README. |
| "`.dockerignore`" | 34 | The README has only `.gitignore` (`README.md:103-106`); the tutorial ships no `.dockerignore`. |
| "cached layer", "bust the cache" | 33, 40 | The README speaks of "one `RUN` layer to keep the image small" (`transcribe_audio/README.md:58`) but not of caching. |
| "Prebuilt wheel (.whl)", "Source (sdist)" / "Source package", "build toolchain" | 35–37 | Not in the README. The README installs `build-essential` without saying why. |
| "base image"; `python:3.14`, `-slim`, `-alpine`; "musl"; "CVEs" | 36–38 | The tutorial uses `python:3.12-slim-bookworm` (`transcribe_audio/README.md:41`). L04's branch moves to 3.14 slim. |
| "Multi-stage builds", "builder stage", "runtime stage" | 37, 39 | Not used in L03's tutorial. |
| "Buildx", "BuildKit", "target platform" | 41 | Not in the L03 README. L04's `docker-shell.sh prod` builds multi-arch. |
| "Build secrets", "secret mount" | 42–43 | Not in the README. The tutorial passes its key by a file in `secrets/` plus an `ENV` path. |
| "Docker Compose"; `compose.yaml` (legacy `docker-compose.yaml`) | 47 | Slides 54 and 57 write `docker-compose.yml`, which is also `port_toy`'s file name. Both names work. |
| "service" (one entry per service; name = hostname) | 48 | `port_toy` adds `container_name:` to match. |
| "compose network" | 50 | `port_toy` names its network `toynet`; the slides use `app-net`. |
| "Bind mount" vs "Named volume" | 51–52 | The L03 README calls its `-v "$(pwd):/app"` bind mount "a volume" (`transcribe_audio/README.md:102`). The slides' word is "bind mount". |
| `environment:`, `env_file:`, `.env`, `build.args` | 53–54 | Not in L03. |
| "healthcheck", `service_healthy`, `service_started`, `service_completed_successfully` | 56 | Not in L03 or in `port_toy`'s compose file. |
| "network namespace" | 61 | Back-reference to Containers I (L02). |
| "Docker DNS" | 62 | Not in L03. |
| "publish a port", "port forwarding", "HOST : CONTAINER" | 63 | Not in L03 (no ports there). `port_toy` covers it. |
| gateway, processor, `app-net`, `gateway-img`, `processor-img`, `ac215/processor:1.0` | 45–63 | `port_toy` uses `toynet`, `toy-gateway`, `toy-processor`, and builds the processor (`build: ./processor`) instead of pulling an image. |
| "'Senior' Developer", "Scenario 1 (early stages)", "Scenario 2 (later stages)", "A Flexible Approach" | 65–69 | The L04 branch README describes the same two modes ("a senior dev publishes prebuilt images to DockerHub") and names the branch "flexible workflow". |

## Commands and code on the slides

Verbatim, one physical line each, as printed. A trailing `\` means the slide continues the
command on the next line.

| Slide | Command / code | Note |
|---|---|---|
| 28 | `http://ac215-mega-pipeline.dlops.io/` · `https://github.com/dlops-io/mega-pipeline` | app and instructions links |
| 28 | `transcribe_audio` · `generate_text` · `synthesis_audio_en` · `translate_text` · `synthesis_audio` | Tasks A–E |
| 33 | `COPY pyproject.toml uv.lock ./` · `RUN uv sync` · `COPY . .` | the cache-friendly order |
| 34 | `.git` · `__pycache__/` · `.venv/` · `node_modules/` · `secrets/` · `*.csv` | `.dockerignore` lines |
| 35 | `cheese_utils-1.0.tar.gz` → `cheese_utils-1.0-py3-none-any.whl` | sdist → wheel names |
| 36–37 | `python:3.14` · `python:3.14-slim` · `python:3.14-alpine` | base images |
| 38 | `$ docker images python` | total size per image |
| 38 | `$ docker history python:3.14-slim` | size per layer |
| 39 | `FROM python:3.14 AS builder` | builder stage |
| 39 | `RUN pip install uv` · `COPY pyproject.toml uv.lock ./` · `RUN uv sync` | builder steps (after `WORKDIR /app`) |
| 39 | `FROM python:3.14-slim AS runtime` | runtime stage |
| 39 | `COPY --from=builder /app/.venv /app/.venv` | only the venv crosses |
| 39 | `COPY . .` · `CMD ["/app/.venv/bin/python", "app.py"]` | code, then run with the venv's Python |
| 40 | `FROM python:3.14-slim` | |
| 40 | `RUN apt-get update \` | |
| 40 | `&& apt-get install -y --no-install-recommends` | continues with `build-essential \` |
| 40 | `&& rm -rf /var/lib/apt/lists/*` | cleanup in the same layer |
| 41 | `$ docker build --platform linux/amd64 -t myapp --load .` | single platform, into local Docker |
| 41 | `$ docker build --push --platform linux/amd64,linux/arm64 -t myapp .` | wrapped over two lines on the slide |
| 42 | `# syntax=docker/dockerfile:1` | first line of the Dockerfile |
| 42 | `RUN --mount=type=secret,id=gh_token \` | |
| 42 | `GH_TOKEN=$(cat /run/secrets/gh_token) &&\` | |
| 42 | `pip install "git+https://GH_USERNAME:${GH_TOKEN}@github.com/org/lib"` | |
| 43 | `$ docker build --secret id=gh_token,src=$HOME/.gh_token .` | supplies the token |
| 43 | `ENV GH_TOKEN=ghp_xxx` · `ARG GH_TOKEN` · `COPY .gh_token /tmp/token` | the three anti-patterns |
| 45 | `docker network create app-net` | by hand, step 1 |
| 45 | `docker build -t processor-img ./processor` | |
| 45 | `docker run -d --network app-net --name processor processor-img` | |
| 45 | `docker build -t gateway-img ./gateway` | |
| 45 | `docker run -d --network app-net -p 8090:9100 \` | |
| 45 | `-e PROCESSOR_HOST=processor -e PROCESSOR_PORT=9200 \` | |
| 45 | `-v "$PWD/gateway:/app" gateway-img` | |
| 47 | `docker compose up` · `docker compose down` | |
| 48, 58 | `services:` · `gateway:` · `build: ./gateway` · `- "8090:9100"` · `- ./gateway:/app` | gateway service |
| 48, 58 | `PROCESSOR_HOST: processor` · `PROCESSOR_PORT: "9200"` · `depends_on:` · `- processor` | |
| 48, 58 | `processor:` · `image: ac215/processor:1.0` | processor service |
| 51 | `- ./secrets:/secrets:ro` · `- models:/models` | bind mount and named volume |
| 51 | `volumes:` · `models:` | top-level declaration |
| 53 | `env_file:` · `- .env` | |
| 54 | `TAG=1.0` · `export TAG=1.0` · `image: ac215/processor:${TAG}` | `.env` / shell fill `${TAG}` |
| 56 | `condition: service_healthy` | under `depends_on: processor:` |
| 56 | `test: curl -f localhost:9200/health` | under the processor's `healthcheck:` |
| 57 | `docker compose up` · `docker compose up -d` · `docker compose up --build` | |
| 57 | `docker compose ps -a` · `docker compose logs -f` | |
| 57 | `docker compose down` · `docker compose down -v` | `-v` also deletes named volumes |
| 62 | `$ docker network create app-net` | |
| 62 | `$ docker run --network app-net \` then `--name gateway     gateway-img` | same for `processor` / `processor-img` |
| 62 | `POST http://processor:9200/` | reach it by name |
| 63 | `-p 127.0.0.1:8090:9100 gateway-img` | end of the `docker run` (after `--network app-net`, `--name gateway`) |
| 63 | `- "127.0.0.1:8090:9100"` | Compose `ports:` excerpt |

## What the lecture stresses

- **A monolith's failure modes:** one broken part can take the whole app down, and patches and
  upgrades are hard because everything is tightly coupled. (Slides 10–11)
- **Microservices are not free:** mixed technologies make development and deployment harder, and
  scaling the whole app gets intricate. Docker + Kubernetes is the slide's answer. (Slide 17)
- **The OS mismatch:** production runs a different OS version than the laptops, and every
  stage must have the right software installed. (Slide 18)
- **API keys are the weak option.** Use them with caution. (Slide 23)
- **The build-optimization rule** (orange banner): "Ship only what you need to RUN, and keep
  what changes small." (Slide 32)
- **Classic mistake: copying all the code before installing dependencies.** Every code edit then
  reinstalls everything. (Slide 33) *Tutorial contrast:* the L03 component Dockerfile does exactly
  this: `COPY --chown=app:app . ./` and then `RUN uv sync` (`transcribe_audio/README.md:82-83`,
  `README.md:217-219`). A scene should say so rather than present the README order as best
  practice. In the tutorial's daily loop the bind mount means code edits do not need a rebuild,
  but every rebuild after a `uv add` reinstalls all dependencies.
- **Secrets must never enter the image.** `secrets/` is the red tag in the `.dockerignore`.
  (Slide 34) *Tutorial contrast:* the tutorial keeps the key in `<component>/secrets/`, has no
  `.dockerignore`, and `COPY . ./` bakes it into a layer. The L03 guide verified this.
- **Alpine is for experts:** musl often means no wheel, so packages compile from source. Check that
  dependencies support Alpine. (Slides 36–37)
- **Optimize what is actually big; do not guess.** (Slide 38)
- **Build tools stay out of the final image.** (Slides 37, 39)
- **A separate cleanup layer does not shrink the image.** Clean up in the same `RUN`. (Slide 40)
  *Tutorial match:* the README's apt `RUN` already follows this (`--no-install-recommends`,
  `rm -rf /var/lib/apt/lists/*`, `pip install --no-cache-dir`).
- **Check the deployment target's CPU architecture.** An Apple Silicon laptop builds arm64 by
  default. (Slide 41)
- **Never pass a secret through `ENV`, `ARG` or `COPY`.** It ends up in the image config, the
  history/metadata or an earlier layer. (Slide 43) *Tutorial contrast:* the tutorial's `ENV` holds
  only the key's path, which is fine, but the key file itself is copied in (above).
- **Hand-run multi-container apps don't scale:** "One multi-container app deserves one file and
  one command." (Slide 46)
- **Inline `environment:` is for a few non-secret values.** Secrets go in a `.env` file kept out
  of Git. (Slide 53)
- **Where you write a variable decides when it exists.** (Slide 54)
- **`depends_on` is not readiness:** "up" means the container started, not that the app is ready.
  (Slides 55–56)
- **`docker compose down -v` deletes named volumes, which is your data.** (Slide 57)
- **Compose is single-machine**; production multi-host is Kubernetes. (Slide 59)
- **Containers are isolated by default** until you wire the paths. Request arrows show direction,
  and responses come back on the same connection. (Slide 61)
- **Ports are written `HOST:CONTAINER`**, and the examples bind to `127.0.0.1`. The slides do not
  explain the `127.0.0.1` prefix; `port_toy`'s compose file comments it as "this laptop only".
  (Slide 63)
- **There is no perfect team workflow.** Clear communication and rules matter more, and each team
  can choose its own. (Slide 69)
- **The shared key is a class shortcut.** Handing out one service-account key is fine for a demo
  but not for the real world. (Slide 70)

Notes for scene authors (my observations, not on the slides):

- On slide 39 the final `COPY . .` would overwrite the copied `.venv` with the laptop's own
  `.venv` unless `.venv/` is in `.dockerignore`. That is one more reason for slide 34's entry.
- Slide 56's healthcheck runs `curl` inside the processor image, which a slim base image does not
  include.
- Slide 42 says the `# syntax=` line is required for `--mount`. Verify that against the current
  Docker documentation before narrating it as a hard rule.

## Pointers

- **Tutorial:** "Tutorial (T5) - Building the Mega Pipeline App". The instructions are at
  `https://github.com/dlops-io/mega-pipeline` and the class app at
  `http://ac215-mega-pipeline.dlops.io/`. (Slide 28; screenshot on 27; QR codes on 24 and 28,
  targets not readable at this resolution)
- **Optional:** the ElevenLabs API for a custom voice. (Slide 24) In the README this is the bonus
  step and the `output_audios_pp/` folder.
- **In-class team challenge** with prizes for the first team and for every finisher. (Slide 26)
- **Back-reference:** Containers I, for network namespaces. (Slide 61) In this series that is L02.
- **Forward references:** Kubernetes "later in the course" (slides 17, 59; L22 in this series).
  Next lecture "Connecting to the Cloud": API keys, OAuth 2.0, service accounts & IAM, the
  networking behind `-p` and `localhost`, and cloud storage (GCS & Drive). (Slide 70) The course
  map lists that as Lecture 10; Lecture 4 is "Containers II-b".
- **Material shared with Lecture 4:** sections 4–7 (slides 30–69) reappear in the L04 deck. Their
  hands-on counterparts are the `port_toy` repo (Compose, networking) and the
  `mega-pipeline@flexible-workflow` branch (team workflows, multi-arch builds), both in the L04
  episode.
- **Not on the slides:** no readings, homework or milestone notes.
