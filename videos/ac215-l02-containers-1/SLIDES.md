# L02 lecture slides — Containers I

**Provenance.** One deck: `Lecture02_L02_containers_i_3_.pdf` (deck name `L02_containers_i_3_`, PDF title `L02_containers_i`), 81 slides, "Lecture 2: Containers I", AC215/E115, Pavlos Protopapas, SEAS/Harvard. These are the instructor's lecture slides (PDF), provided by the student for study; the PDFs are not in this repository; slide numbers are PDF page numbers. Everything below is a digest in our own words. It was made from the extracted slide text and from reading every slide image: all nine contact sheets, plus single-page renders of the diagram and screenshot slides. Those renders are small (40 dpi), so tiny screenshot text is marked as uncertain where it matters. The tutorial side is documented in [`digest.md`](digest.md). Below, "tutorial", "README" and "repo" mean `dlops-io/simple-translate` at `62f821b`, as recorded there.

## Outline

The deck has a four-item agenda slide titled "Outline". Slide 3 shows it plain. Slides 4, 8, 25 and 27 reuse it as section dividers, with the current item in bold and a meme picture beside it. Tutorial slides (52–73 and 77) have a grey background; all other slides are white.

- **Slides 1–3 · opening.** Title (1). Logistics (2): DCE waitlisted students were admitted, online students should use the Ed chat because Zoom chat is broken, a course survey, and a team-registration form. Agenda (3).
- **Slides 4–7 · 1. Recap & Motivation.** Divider (4). Pros and cons of virtual machines (5). Pros and cons of virtual environments (6). A four-item wish list, answered in red by "Containers" (7).
- **Slides 8–24 · 2. What is a Container.**
  - Divider (8). Definition, with a host-stack diagram (9). Virtual environments, VMs and containers drawn as three stacks (10).
  - The containerization stack, which introduces namespaces and cgroups (11). Kernel vs user space (12).
  - Namespaces in general (13). PID namespace (14), mount namespace (15), network namespace (16), then IPC, UTS and user namespaces (17).
  - Control groups (18).
  - Security: seccomp and avoiding root (19), examples of blocked system calls (20), AppArmor and SELinux (21).
  - Why containers are so small (22).
  - How macOS and Windows run Linux containers: the question, with a meme (23), then the answer, with two stacks (24).
- **Slides 25–26 · 3. Why use Containers.** Divider (25). Three advantages (26).
- **Slides 27–77 · 4. How to use Containers.**
  - 27: divider.
  - 28–29: other container technologies, and what Docker is.
  - 30–31: Dockerfile → image → container, and the difference between an image and a container.
  - 32–33: anatomy of a Dockerfile, four instructions and then seven.
  - 34–37: images as layers. One layer per instruction (34), the layering model (35), why layers (36), an example stack for a Debian + uv image (37).
  - 38: Docker vocabulary.
  - 39–41: FAQ, many containers from one image. A meme (39), different parameters (40), an ENTRYPOINT/CMD demo (41).
  - 42–51: mounting. Why mounts are needed (42). A table of the three kinds (43). Bind mounts (44–45). Named volumes (46–48). How `-v` tells the two apart (49). `-v` vs `--mount` (50). Summary and read-only mounts (51).
  - 52–73: tutorial. It starts with installing Docker Desktop (52) and `docker --version` (53). A checklist for building the simple-translate app then grows one item per slide:
    - clone (54);
    - build (55), with the `docker build` anatomy (56), the Dockerfile (57), the build output read as layers (58), `docker images` and `docker image history` (59), a cached rebuild (60), list images (61), list containers (62);
    - run (63), with the `docker run` anatomy (64) and a check from a second terminal (65);
    - push (66), with login (67), tag (68), push (69);
    - pull and run (70), with the pull command (71);
    - the full checklist plus a link to the README (72), then cleanup with prune (73).
  - 74–76: debugging. `ps` and `logs` (74), `exec` and overriding the entrypoint (75), `inspect` (76).
  - 77: tutorial, running the app on a VM using Docker.
- **Slides 78–81 · closing, not on the agenda.** A recap of how the Cheese App is built across development and deployment (78). The same picture with three pieces boxed as containers (79). An image-only slide, a film still with no text (80). "Thank you" with a Pikachu picture (81).

## Key ideas

1. **Neither VMs nor virtual environments give you everything.**
   - A VM gives full control of its OS and strong isolation, and every cloud offers VMs. But it is heavy: it consumes the host's resources, its images are large and hard to move, and the hypervisor plus extra operating systems add overhead.
   - A venv lists dependencies explicitly and makes experiments easy to reproduce and share. But setup can be fiddly, it shares the host OS (so conflicts are possible), and it may not carry over between operating systems.

   *Slides 5–6.*
2. **The wish list has four items:** automated setup (OS, libraries and Python environment installed for you), full isolation from the host, frugal use of CPU, memory and disk, and near-instant start-up. Containers meet all four. *Slide 7.*
3. **A container is a program on your machine that acts like a small computer inside it.** It borrows the host's CPU, memory, disk and OS kernel, but has its own user space, filesystem and network. It carries the code together with its dependencies, so it behaves the same wherever it is deployed. *Slide 9.*
4. **Venvs, VMs and containers differ in what each app carries with it.**
   - A venv carries only its libraries, on a shared Python and OS.
   - A VM carries a whole guest OS on a hypervisor.
   - A container carries only binaries and libraries, on a container engine that runs on the host OS.

   That is why the drawing fits six containers where it fits three VMs. *Slide 10.*
5. **Containers are built on two Linux kernel features: namespaces and cgroups.** The OS splits into the kernel, which has low-level access to the hardware, and user space, which holds every program outside the kernel. The container engine (Docker) lives in user space. *Slides 11–12.*
6. **A namespace gives a group of processes its own private view of one kind of system resource.** A process inside a namespace sees only what that namespace contains.
   - **PID:** each container numbers its processes from 1, while the host gives them unique global numbers. In the slide's example, nginx in one container and MySQL in another are both PID 1, and on the host they are 345 and 678.
   - **Mount:** each container has its own view of the filesystem. Two containers can both mount something at `/data`, one Drive_A and the other Drive_B, without seeing each other's.
   - **Network:** each container has its own IP addresses, routing tables and firewall rules.
   - **IPC:** each namespace has its own inter-process communication and shared memory.
   - **UTS:** each namespace has its own host name.
   - **User:** a process that is root inside a container can be an ordinary user on the host.

   *Slides 13–17.*
7. **cgroups limit and meter resources:** CPU, memory, disk I/O and network bandwidth. This makes containers lighter than VMs and adds security, because one container cannot bring the whole machine down by exhausting a resource. *Slide 18.*
8. **Docker uses more kernel features for security.**
   - By default, a seccomp profile removes about 44 of the 300+ system calls. A container cannot call `reboot`. It should also not get `quotactl`, which would let it change disk quotas for the host and every other container.
   - Containers seldom need root, and only what is strictly needed is passed into them.
   - AppArmor and SELinux restrict which files, directories, sockets and processes a container may touch.

   The slide warns explicitly not to confuse these security modules with cgroups, which manage resources. *Slides 19–21.*
9. **Containers are small because a container is only user-space code.** It holds the minimum its program needs. For RAM, CPU, drives, network, GPU and audio it relies on the host's Linux kernel, reached through system calls. *Slide 22.*
10. **On macOS and Windows, Docker runs a stripped-down Linux VM,** and that VM's Linux kernel receives the containers' system calls. On a Mac the VM is HyperKit. On Windows it is WSL2, a custom Linux kernel built into Windows that makes an even thinner VM. *Slides 23–24.*
11. **Why use containers:** they are portable and lightweight, they package the software with all its dependencies, and the same container serves development, testing, training and production. *Slide 26.*
12. **Docker is one container platform among several.**
   - The others listed are LXC (the original Linux containers, with less isolation), Podman (no daemon, Docker-compatible, can run without root), rkt (security-focused) and OrbStack (macOS only).
   - The lecture uses Docker: open source, the industry standard, with Docker Hub and Kubernetes in its ecosystem.

   *Slides 28–29.*
13. **Dockerfile → build → image → run → container.**
   - The Dockerfile is a text recipe. The image is what the build produces, a template. A container is a running instance of that image.
   - Analogies: a handwritten recipe, a meal kit, the cooked dish; or a class and an instance of it.
   - Slide 38 sums it up: images are how you *store* an application, containers how you *run* it.

   *Slides 30–31, 38.*
14. **A Dockerfile is a short list of instructions.**
   - FROM chooses the base image. RUN executes a command at build time, and each RUN adds a layer. ENTRYPOINT sets the program the container runs. CMD sets default arguments or a default command, which `docker run` can override.
   - Slide 33 adds ADD (like COPY, but it also fetches URLs and unpacks archives), ENV (environment variables) and WORKDIR (the working directory for the instructions that follow).

   *Slides 32–33.*
15. **An image is a stack of read-only layers; starting a container adds one writable layer on top.** The bottom layer is a platform image that has no parent and defines the runtime environment. Every layer above it depends on its parent. *Slides 34–35, 37.*
16. **Layers pay off in five ways.** Images share common layers. Only changed layers are rebuilt and shipped. The build cache makes repeat builds fast. A complex setup splits into pieces that are easier to debug. Each layer has a smaller attack surface that is easier to scan. The rebuild demo shows steps marked `CACHED` and a build that takes under a second. *Slides 36, 58–60.*
17. **One image can start many containers, and they need not behave alike.** Arguments after the image name in `docker run` replace the image's CMD. With ENTRYPOINT `echo Hello` and CMD `world`, a plain run prints "Hello world", and a run that adds `Pavlos` prints "Hello Pavlos". *Slides 39–41.*
18. **Containers are ephemeral, and mounts connect them to storage that lasts.** The writable layer is discarded when the container exits, and with `--rm` the whole container goes too. That breaks two needs: editing code on the host and seeing the change live inside the container, and keeping outputs such as trained models. Mounts link host directories or Docker-managed storage into the container. *Slide 42.*
19. **There are three kinds of mount.**
   - A **bind mount** maps a host path you choose. It persists, but only on the host. Use it for code, config and secrets during development.
   - A **named volume** lives where Docker chooses and manages. It persists after the container is removed and can be shared by several containers. Use it for database files and model artifacts.
   - **tmpfs** lives in RAM and does not persist. Use it for ephemeral secrets and scratch space.

   *Slides 43–48, 51.*
20. **`-v` decides the mount type from the source.** A source containing `/` is a host path, so a bind mount. A source without one is a volume name, and the volume is created if it is missing. `--mount` states the type explicitly and is safer: a missing bind source makes it fail loudly, while `-v` quietly creates an empty directory. Append `:ro` to mount read-only. *Slides 49–51.*
21. **The tutorial cycle is clone → build → run → push → pull and run.** Docker Hub is the registry. You authenticate with an access token rather than a password and tag the image under your username. `docker system prune -a` cleans up at the end. *Slides 52–73.*
22. **Debug a misbehaving container with four tools: `ps`, `logs`, `exec`, `inspect`.**
   - `ps -a` also lists containers that exited with an error code.
   - `logs -f` follows a container's output live.
   - `exec` opens a shell in a container that is already running, whereas `run` starts a new one.
   - `inspect` prints the full configuration: mounts, environment and ports.

   If a container exits immediately, start it with the entrypoint replaced by a shell. *Slides 74–76.*
23. **Deploying on a VM shrinks to four steps:** create the VM, SSH in, install Docker, run the container. *Slide 77.*
24. **The course project is the reason for containers.**
   - Building the Cheese App involves several developers on Mac and Windows, Colab on Linux, and a Linux server, each with a different Python setup.
   - The closing slide boxes three pieces as separate containers: the data-collection script, the API/model/editor work, and the server's model training.

   *Slides 78–79.*

## Diagrams

- **Slide 9 · a container on a host.**
  - A four-row stack on the right, each row labelled in blue on its left. Bottom up:
    - "Laptop, Desktop": a dark bar, "CPU, Memory, Disk, …".
    - "Operating System": a grey bar, "MacOS, Windows, …".
    - "Software": a blue bar, "Container Program".
    - "Containers": three dashed boxes side by side, each holding a small "Apps" tile above a "Files" tile.
  - For: the container is ordinary software on your machine, and each container brings its own apps and files.
  - Re-draw as the four bars rising into place, with the three boxes popping out of the "Container Program" bar.
- **Slide 10 · Environments vs Virtualization vs Containerization.** Three stacks side by side, each with "Infrastructure" (dark) at the bottom and "Operating System" (grey) above it. The caption words are colour-coded: "Environments" blue, "Machines" red, "Containerization" green.
  - Left, "Virtual Environments": a dark-blue "Python" bar holds three short dashed boxes, each an App over Libs, labelled "Venv". The boxes are blue, green and red for App1–App3.
  - Middle, "Virtual Machines": a grey "Hypervisor" bar holds three tall solid boxes, each an App over "Bins/lib" over a big "OS" block, labelled "VM".
  - Right, "Containerization": a blue "Container Program" bar holds six short dashed boxes in two rows, each an App over "Bins/lib", labelled "Container". The top row is App1, App2, App3 (blue, green, red). The bottom row is App3, App2, App3 again (gold, purple, pink), which shows that several containers can run the same app.
  - For: the height of each box is what an app must carry. Only the VM boxes contain an OS, so twice as many containers fit in the same width.
  - Re-draw as three columns that grow box by box, with the VM column visibly taller.
- **Slides 11–21 · the recurring containerization stack.**
  - Slide 11, bottom up: "Physical Hardware" (dark), "Operating System" (grey), "Container Engine (Docker)" (blue, with the Docker whale), and the same six containers as slide 10.
  - From slide 12 on, the OS bar splits into a teal "Kernel" bar with a grey "User Space" bar above it.
  - The stack stays identical through slide 21; only the text panel on the right changes.
  - The namespace, cgroup and seccomp examples are therefore text-only on the slides. For a scene we must draw them ourselves:
    - PID: two containers each showing PID 1, mapped to host PIDs 345 and 678.
    - Mount: two containers each with a `/data` that leads to a different drive.
    - cgroups: a meter per container capping CPU and memory.
    - seccomp: a syscall list with `reboot` and `quotactl` crossed out.
  - For: locating each mechanism. Namespaces and cgroups are features of the kernel bar; the engine only asks for them.
- **Slide 22 · why containers are small.**
  - Headline: "Container = User Space of OS".
  - Left, a grey box titled "User Space" holds the three containers (App1–App3 over Bins/lib), a blue "Docker client" bar with the whale, and a blue "Daemon" bar. A thin line runs from the first container down to the client.
  - A line labelled "Syscalls" leaves the Daemon and runs right into a teal box titled "Linux Kernel". Inside the box are two orange tiles, "Namespaces" and "cgroups", and six red resource tiles: RAM, CPU, Drives, Network, GPU, Audio.
  - For: a container is just user-space files and processes, and everything physical goes through the one shared kernel.
  - Precision note for a re-draw: the slide routes the syscalls through the daemon. In reality each container's own processes make system calls straight to the kernel, and the daemon's job is to set up their namespaces and cgroups.
- **Slide 24 · containers on macOS and Windows.**
  - Two stacks side by side, captioned "MacOS" and "Windows". Each one, bottom up: Physical Hardware, Kernel, User Space, then a VM layer ("HyperKit" on the Mac, "WSL2" on Windows), then "Docker Engine", then three containers.
  - Side notes: HyperKit is virtualization technology. WSL2 is a custom Linux kernel built into Windows that runs an even thinner Linux VM.
  - For: why Docker Desktop on a laptop always involves a hidden Linux VM.
  - Note: newer Docker Desktop releases for Mac use Apple's Virtualization framework instead of HyperKit. The principle is the same, but this was not verified in this repo.
- **Slide 30 · from Dockerfile to container.**
  - Hand-drawn in red-brown ink, left to right:
    - a "Docker file" box with five lines (`FROM alpine:latest`, `RUN apk update`, `RUN apk add nmap`, `ENTRYPOINT ["nmap"]`, `CMD ["localhost"]`);
    - a thick blue arrow labelled "Build";
    - a "Docker Image" box with three stacked diamond-shaped sheets;
    - a blue arrow labelled "Run";
    - a "Docker Container" box with a 3-D open box.
  - For: the three nouns and the two verbs that connect them.
- **Slide 34 · Dockerfile lines become layers.**
  - The same hand-written five-line Dockerfile (blue outline, left). A green arrow from each line reaches a stack of five nested diamond outlines on the right, labelled "Docker Image"; the outermost diamond is purple, the rest dark red. The arrows cross, so the pairing is schematic.
  - A speech bubble notes that Nmap (Network Mapper) is an open-source network utility.
  - For: each instruction maps to one slice of the image. Our nuance: only filesystem-changing instructions add content, and slide 59 itself lists ENV, CMD and ENTRYPOINT steps at 0B.
- **Slide 35 · image layering.**
  - A four-bar stack, bottom up: blue "Platform Image (Runtime Environment)", light-grey "Layered Image 1", mid-grey "Layered Image 2", dark "Container (Writable, running application)".
  - Three red chevrons point right to three rounded notes:
    - container: an "application sandbox", where launching adds a writable layer on top of the image;
    - layered images: a read-only "static snapshot", each depending on one or more parents;
    - platform image: defines the runtime, packages and utilities, and has no parent.
  - For: read-only shared base, writable private top.
  - Re-draw as grey slabs that lock and a thin glowing slab that appears per container and vanishes on exit.
- **Slide 37 · layer example, Debian + Python + uv.**
  - Six coloured bars, bottom up: Kernel (grey), Debian Linux (blue), Install Python & Pip (maroon), Upgrade Pip (green), Install UV (orange), UV Sync (red). A hollow arrow on the right points upward, giving the build order.
  - For: a concrete layer stack matching the tutorial's Dockerfile, built up from the base OS through Python and uv to `uv sync`.
  - Precision note: the kernel bar is the host's kernel (slide 22), not part of the image.
- **Slide 38 · vocabulary panel.** Five icon rows: Docker File, Docker Image, Docker Container, Docker Engine, Registry Service. Two grey call-outs on the right sit beside Image and Container: "Images: how you store your application" and "Containers: how you run your application".
- **Slides 39–40 · one image, many containers (memes used as diagrams).**
  - Slide 39: the Spider-Man-pointing-at-Spider-Man meme, the three figures labelled Container 1–3. All containers from one image look alike.
  - Slide 40: a 2×2 grid of the same man in four different outfits, labelled Container 1–4. Same image, different parameters, different behaviour.
  - Re-draw as one image stamp producing four instances, each with its own argument tag.
- **Slide 41 · ENTRYPOINT + CMD demo.** A white "Docker file" panel (`FROM ubuntu:latest`, `RUN apt-get update`, `ENTRYPOINT ["/bin/echo", "Hello"]`, `CMD ["world"]`) beside a dark terminal: a build, then a run printing "Hello world", then a run with `Pavlos` printing "Hello Pavlos". For: run-time arguments replace CMD and keep ENTRYPOINT.
- **Slide 43 · three ways to mount (table).**

  | Type | Who picks the location | Persists? | Typical use |
  |---|---|---|---|
  | Bind mount | you (a host path) | yes, but only on the host | source code, config, secrets (dev) |
  | Named volume | Docker | yes (Docker-managed) | db files, model artifacts |
  | tmpfs | — (RAM) | no | ephemeral secrets / scratch |

  Re-draw as three pipes from container to host disk, Docker's storage area and RAM.
- **Slides 53, 56, 61, 62, 64, 67, 68, 69, 71, 73 · command-anatomy diagrams.**
  - One command sits in the middle in monospace: `docker` in blue, the subcommand on a pink/red highlight, options and arguments on green or orange highlights. Pastel call-out boxes with curved arrows point at each token: blue "docker command", pink/red for the subcommand's meaning, green or orange for an option's meaning.
  - What each slide labels:
    - 53: `--version` gets the CLI version.
    - 56: `build` builds the image, `-t simple-translate` names it, and `-f Dockerfile .` names the Dockerfile, with "." meaning the current directory.
    - 61 and 62: `image ls` and `container ls` list images and containers.
    - 64, six call-outs: `run`; `--rm` cleans up the container and its filesystem on exit; `--name` names the container; `-ti` (t = terminal, i = interactive); `--entrypoint /bin/bash` replaces the Dockerfile's ENTRYPOINT; the final `simple-translate` is the image.
    - 67: `login`, `-u` user name, `-p` access token instead of a password.
    - 68: `tag`, source image (tag defaults to `latest`), target `<USER NAME>/…`.
    - 69: `push` uploads to a remote registry; the user name can be part of the image name.
    - 71: `pull` downloads from a registry.
    - 73: `system prune -a` removes all images not used by any container.
  - Slide 65 shows `docker image ls` and `docker container ls` without call-outs.
  - For: reading a Docker command as verb + object + flags + target. This style is easy to animate token by token.
- **Slide 58 · build output read as layers.**
  - A dark BuildKit log of `docker build -t simple-translate -f Dockerfile .`. Four blue arrows labelled "Step1: Instruction 1" … "Step4: Instruction 4" point at `[1/4] FROM …`, `[2/4] RUN set -ex; …`, `[3/4] ADD . /` and `[4/4] RUN uv sync`.
  - The log also shows the base image's layers downloaded and extracted by sha256 (about 2.8 s), the RUN step taking about 24 s, ADD 0.0 s and `uv sync` about 7.8 s.
  - For: each numbered build step is one Dockerfile instruction.
- **Slide 59 · inspecting the layers.**
  - Two terminal panels. `docker images` lists `hello_world_cmd` (8.83MB) and `simple-translate` (483MB). `docker image history simple-translate` lists about 18 rows, newest first: the app's steps "28 hours ago" on top, the base image's steps "3 weeks ago" below.
  - Metadata steps (CMD, ENTRYPOINT, ENV, ARG, USER) show 0B. The big RUN shows 396MB.
  - For: an image is a visible stack with a size per layer.
- **Slide 60 · the cache at work.** A rebuild log with a blue arrow, "Have seen this before. Use cache", pointing at `CACHED [2/4]`, `[3/4]`, `[4/4]`. The whole build takes 0.6 s. The text underneath says the build reused existing layers, and that other containers can share them. For: the layer cache.
- **Slide 78 · "Recap: How do we build an App?"**
  - A wide red bracket "Development" spans three stages, joined by a purple arrow and then an orange arrow:
    1. A grid of food photos with a "Python Script" box. Below it: Python via uv, Chromium installed separately on Mac and Windows, OS Mac/Windows.
    2. A Colab notebook screenshot with a "Colab" box. Below it: Colab's provided Python, OS Linux.
    3. "Rest API", "Best Model" and "IDE / Code Editor" boxes with a cheese-classifier screenshot. Below it: Python via uv, OS Mac/Windows.
  - Person icons under the stages read "Multiple developers, Using Mac and Windows OS".
  - A green arrow leads to a blue bracket "Deployment" / "Server". Inside, an app screenshot (top), a red "Model Training" box (middle) and the photo grid with "Python Script" (bottom) are joined by curved arrows into a loop: script to training, training to app, app back down to data. Below: Python via uv, OS Linux.
  - For: one project already spans several machines, operating systems and Python setups.
- **Slide 79 · "Isolate work into containers."** The slide-78 picture greyed out, with blue rectangles labelled "Container" over three pieces: the data-collection script stage, the API/model/editor stage, and the server's model-training box. The Colab stage is not boxed. For: each piece of the project becomes its own container, previewing the multi-container work of the next lectures.

## Terms the lecture uses

- **"Container Program"** (slides 9–10), **"Container Engine (Docker)"** (11–21), **"Docker engine"** (19), **"Docker Engine"** (24; defined on 38 as what creates, ships and runs containers), **"Docker client"** and **"Daemon"** (22), "the daemon" reads the Dockerfile (34).
  - The README names only **Docker Desktop**, the app you install (also slide 52), and never the engine or daemon.
  - Our digest draws dockerd + BuildKit inside Docker Desktop's hidden Linux VM.
- **"Kernel"**, **"User Space"** (12); **"Container = User Space of OS"** (22); **"Syscalls"** (22–24).
- **"Namespace"** (11, 13). The six kinds are **"PID Namespace"** (14), **"Mount Namespace"** (15), **"Network Namespace"** (16), and on slide 17 **"IPC Namespace"** (Inter-Process Communication), **"UTS Namespace"** (UNIX Timesharing System) and **"User Namespace"**.
  - Slide 17 glosses UTS as each namespace defining its own "localhost". More exactly, UTS isolates the host name (and domain name).
- **"cgroups (Control Groups)"** (11, 18).
- **"Secure computing mode, seccomp"** (19); the "syscall reboot" and `quotactl` (20); **"AppArmor (Application Armor)"**, **"SELinux (Security-Enhanced Linux)"** (21).
- **"Virtual Environments"**, **"Virtual Machines"**, **"Containerization"**, **"Hypervisor"**, **"Infrastructure"**, **"Bins/lib"**, **"Venv"** (10).
- **"HyperKit"**, **"WSL2"** (24); **"Hyper-V"** (52, as a Windows requirement).
  - Slides 24 and 52 name different Windows mechanisms. Current Docker Desktop for Windows normally uses WSL2.
- **"Dockerfile"** (30, 32–34; also written "Docker file" on 31 and "Docker File" on 38), **"Docker Image"**, **"Docker Container"** (30–31, 38); "template or blueprint" (31).
  - Slide 30 says the image "consists of an iso file and other files". More precisely, an image is a stack of layer archives plus a JSON config, not an ISO (`digest.md` C1).
- **"Platform Image (Runtime Environment)"**, **"Layered Image"**, **"writable layer"**, "application sandbox", "static snapshot", "parent images" (35); **"base OS image"** (32).
  - The README's term for the platform image is the **base image** it picks with `FROM python:3.12-slim-bookworm`.
- **"Image Layering"**, "layer", "cache" (34–37, 60).
- **"Registry Service (Docker Hub or Docker Trusted Registry)"** (38); "remote registry" (69); **"Docker Hub"** (29, 66–71). The README says only "Docker Hub".
- **"Access Token"** (67), the same as the README.
- **"tag"**, "repository namespace", with the default tag `latest` (68). Slides write names generically as `<USER NAME>/<TARGET_IMAGE[:TAG]>`; the README uses the concrete `<USER NAME>/simple-translate-ac215`.
- **Build "a container" vs build "the image".**
  - Slides 30 and 56 say the build produces the image.
  - The checklist slides (55, 63, 66, 70, 72) say "Build a container", as does the README ("Build the docker container", `digest.md` E7).
  - The command builds an *image*; our scripts should say so.
- **"." means "look at the current working directory"** (56). The slide-58 log calls it the **build context** ("load build context"), the term our digest uses. The README does not name it.
- **"ephemeral"** (42); **"mounts"**, **"Bind mount"**, **"Named volume"**, **"tmpfs"** (43); "The Dev Loop", "Secret Management" (45); "Persistence", "Shared Access", "Managed Storage" (47); "least privilege" (51).
  - None of these appear in the L02 README. simple-translate uses no mounts, and `-v` arrives with L03 (`digest.md` §1, Excerpt 5).
- **"Developing App using Containers"** (54–72) and **"Running App on VM using Docker"** (77) match the README headings. The README calls them "Step 3 of 4" and "Step 4 of 4", and the slide links append `-t3` / `-t4` (see Pointers).
- **"simple-translate"** is the tutorial app and image name (54–73). **"hello_world_cmd"** is the demo image (41, 59–60).
- **"docker command"**, **"Docker CLI"** (53).
- Closing slides: **"Development"**, **"Deployment"**, **"Server"**, **"Python Script"**, **"Colab"**, **"Rest API"**, **"Best Model"**, **"IDE / Code Editor"**, **"Model Training"** (78); **"Isolate work into containers"** (79).

## Commands and code on the slides

Slides 30, 32 and 34 show the same hand-written Dockerfile:

```dockerfile
FROM alpine:latest
RUN apk update
RUN apk add nmap
ENTRYPOINT ["nmap"]
CMD ["localhost"]
```

Slides 32–33 name the instructions `FROM`, `RUN`, `ENTRYPOINT`, `CMD`, `ADD`, `COPY` (only as ADD's comparison), `ENV` and `WORKDIR`, and note that `docker run` can override `CMD`.

Slide 41 shows a Dockerfile and a terminal:

```dockerfile
FROM ubuntu:latest
RUN apt-get update
ENTRYPOINT ["/bin/echo", "Hello"]
CMD ["world"]
```

```
> docker build -t hello_world_cmd -f Dockerfile .
> docker run -it hello_world_cmd           → Hello world
> docker run -it hello_world_cmd Pavlos    → Hello Pavlos
```

Mounting (slides 42–51):

```
--rm                                          (slide 42)
docker run -v "$(pwd)":/app <image_name>      (slide 44)
-v "$(pwd)/secrets":/secrets                  (slide 45)
docker volume create mydata                   (slide 46)
docker run -v mydata:/data transcribe-audio   (slide 46)
docker volume ls                              (slide 46, list)
docker volume inspect                         (slide 46, examine)
docker volume rm                              (slide 46, delete)
docker run -v "$(pwd)":/app app               (slide 49, bind mount)
docker run -v appdata:/data app               (slide 49, named volume)
--mount type=bind,source="$(pwd)",target=/app (slide 50)
--mount type=volume,source=mydata,target=/data (slide 50)
:ro                                           (slide 51)
```

Tutorial (slides 52–73):

```
docker run hello-world                                   (52)
docker --version                                         (53)
git clone https://github.com/dlops-io/simple-translate   (54)
docker build -t simple-translate -f Dockerfile .         (56, 58)
docker images                                            (59)
docker image history simple-translate                    (59)
docker build -t hello_world_cmd -f Dockerfile_cmd .      (60)
docker image ls                                          (61, 65)
docker container ls                                      (62, 65)
docker run --rm --name simple-translate -ti --entrypoint /bin/bash simple-translate   (64)
docker login -u <USER NAME> -p <ACCESS TOKEN>            (67)
docker tag <SOURCE IMAGE NAME>[:TAG] <USER NAME>/<TARGET_IMAGE[:TAG]>   (68)
docker push <USER NAME>/<TARGET_IMAGE[:TAG]>             (69)
docker pull [OPTIONS] <USER NAME>/<TARGET_IMAGE[:TAG]>   (71)
docker system prune -a                                   (73)
```

Slide 57 is the tutorial Dockerfile as the lecture shows it. Its instruction lines are below; the slide's inline comments are paraphrased after the block.

```dockerfile
FROM python:3.12-slim-bookworm
# ENV UV_LINK_MODE=copy
# ENV UV_PROJECT_ENVIRONMENT=/home/app/.venv
RUN set -ex; \
   apt-get update && \
   apt-get upgrade -y && \
   apt-get install -y --no-install-recommends build-essential git && \
   pip install --no-cache-dir --upgrade pip && \
   pip install uv
ADD . /
RUN uv sync
ENTRYPOINT ["/bin/bash"]
CMD ["-c", "source /home/app/.venv/bin/activate && exec bash"]
```

Slide 57's comments explain:
- the base is the official Debian-hosted Python image;
- the two ENV lines (commented out) would tell uv to copy packages and where to put the venv;
- `set -ex` stops the build on the first failing command and echoes each command;
- `apt-get update` refreshes the package index and `upgrade -y` upgrades installed packages;
- `ADD . /` copies the current directory into the container's root.

The slide-58 log shows the four steps: `[1/4] FROM docker.io/library/python:3.11-slim-buster@sha256:…`, `[2/4] RUN set -ex; …`, `[3/4] ADD . /`, `[4/4] RUN uv sync`, ending `naming to docker.io/library/simple-translate`. On slide 60 the last three show as `CACHED`.

Debugging (slides 74–76):

```
docker ps / docker ps -a                    (74)
docker logs <name>      (-f to follow)      (74)
docker exec -it <name> /bin/bash            (75)
docker run -it --entrypoint /bin/bash <image>   (75)
docker inspect <name>   → Mounts, Config.Env, NetworkSettings.Ports   (76)
```

**How these compare with the tutorial.** These come from reading the slides against `digest.md` and the repo at `62f821b`; nothing below was built or run for this note.

- **Slide 57 is not the repo's `Dockerfile.txt`.** The repo file differs in four ways:
  - its three ENV lines are active: `DEBIAN_FRONTEND`, `LANG`, `PYTHONUNBUFFERED` (the slide's two ENV lines are different ones, and commented out);
  - it runs `apt-get clean`, where the slide installs `build-essential git`;
  - it uses `COPY . ./`, where the slide uses `ADD . /`;
  - its CMD sources the *relative* `.venv/bin/activate`.
- **The slide-57 CMD path looks wrong as printed.** With `UV_PROJECT_ENVIRONMENT` commented out, `uv sync` would create `/.venv`, not `/home/app/.venv`. The `source` would fail, and the `&&` would end the container. Follow the README's version on screen.
- **The screenshots come from other Dockerfiles and names.**
  - Slide 58's log uses `python:3.11-slim-buster`, not `3.12-slim-bookworm`.
  - Slide 59's `docker image history` shows a richer Dockerfile than slide 57: `USER app`, `WORKDIR /app`, `COPY --chown=app:app`, `ENTRYPOINT ["uv" "run"]`, `CMD ["/bin/bash"]`, an `ARG DEBIAN_PACKAGES`, and a Python 3.12.11 base.
  - Slide 59's `docker images` gives `hello_world_cmd` and `simple-translate` the same IMAGE ID, which is a screenshot artefact.
  - Slide 60's command builds `hello_world_cmd` from `Dockerfile_cmd`, but its log names `simple-translate`.
  - Do not reuse these as "expected output". Our captures in `digest.md` are the reference.
- **Slide 64's run command differs from the README's `docker run --rm -ti simple-translate`.**
  - It adds `--name simple-translate`, as `docker-shell.sh` does.
  - It also adds `--entrypoint /bin/bash`. Overriding the entrypoint also clears the image's CMD, so the venv is *not* activated. A following `python cli.py` would use the base image's Python and fail with `ModuleNotFoundError` (`digest.md` C4, Step 6).
- **Cleanup.** Slide 73 uses `docker system prune -a`; the README uses `docker system prune` without `-a` (`digest.md` E8).
- **Image names.** Slides 68–71 use generic `<USER NAME>/<TARGET_IMAGE[:TAG]>`. The README tags and pushes `<USER NAME>/simple-translate-ac215`, then runs the instructor's `dlops/simple-translate` on the VM, with an implicit pull by `docker run` (`digest.md` E4).
- **Login.** Slide 67 shows `-p <ACCESS TOKEN>` on the command line, as the README does; prefer the prompt (`digest.md` E9).
- **Not in the README:** mounting (42–51), debugging (74–76), the namespaces/cgroups/seccomp internals (11–22), and the `hello_world_cmd` demo (41).
- **In the README but not on the slides:** CPU architecture (arm64 vs amd64) and `docker-build-push.sh`.

## What the lecture stresses

- **VMs are heavy and venvs do not isolate.** These are the two pain points containers solve (slides 5–7).
- **Containers share the host kernel; they are not small VMs.** Isolation comes from kernel namespaces and resource limits from cgroups (slides 9, 11–18, 22).
- **Do not confuse AppArmor/SELinux (security) with cgroups (resource management)** (slide 21, framed as a warning).
- **Least privilege by default.** Containers get a reduced syscall set and cannot reboot the host. They rarely need root. Only the information they need is passed in. Root inside can be non-root outside (slides 17, 19–20).
- **One runaway container must not sink the host.** cgroups prevent resource exhaustion (slide 18).
- **On Mac and Windows there is always a Linux VM underneath** (slides 23–24).
- **Each RUN creates a layer; CMD can be overridden at `docker run`** (slides 32–33, 40–41).
- **Layers are deliberate.** They bring efficiency, incremental updates, caching, modularity and security, and the lecture promises "WE WILL SEE AN EXAMPLE LATER", delivered on slides 58–60 (slide 36).
- **Image vs container.** An image is a read-only template; a container is a writable, running instance, and many can come from one image (slides 31, 35, 38–40).
- **Containers are ephemeral.** Anything written inside is lost on exit, immediately with `--rm`, so use mounts for live code and for results that must persist (slide 42).
- **Always give an absolute host path for bind mounts; `$(pwd)` is the reliable way** (slide 45).
- **`-v` decides by the slash**: a `/` means a host path, no slash means a named volume (slide 49).
- **Prefer `--mount`.** A missing bind source makes `--mount` fail loudly, while `-v` silently creates an empty directory (slide 50, labelled "Gotcha").
- **Mount secrets read-only with `:ro`** (least privilege, slide 51), and inject secret files with a bind mount instead of baking them into the image (slide 45).
- **Authenticate with an access token, not your password** (slide 67).
- **An omitted tag means `latest`** (slide 68).
- **`docker exec` joins a running container; `docker run` starts a new one** (slide 75, "Key Distinction").
- **If a container exits immediately, debug it by overriding the entrypoint with a shell.** Use `ps -a` to see exit codes, `logs -f` for crash output, and `inspect` to check mounts, environment variables and published ports (slides 74–76).
- **Windows users need Hyper-V for Docker** (slide 52, as stated). Check this against current Docker Desktop, which uses WSL2.
- **Clean up afterwards:** exit all containers and remove unused images (slide 73).

## Pointers

- **Logistics (slide 2):**
  - DCE waitlisted students were admitted (see the Ed post).
  - Online students should use Ed chat, channel "lecture2": `https://edstem.org/us/courses/97373/discussion/chat/channels/30245`.
  - Course survey: `https://bit.ly/ac215_2026_survey`.
  - Team form, to fill when your team is formed: `https://bit.ly/ac215_2026_groups`.
  - The last two also appear as QR codes.
  - No homework or milestone deadline appears on the slides.
- **Dockerfile reference:** `https://docs.docker.com/engine/reference/builder/` (slides 32–33).
- **Docker Desktop install (slide 52, with a QR code):**
  - Mac: `https://docs.docker.com/docker-for-mac/install/`.
  - Windows: `https://docs.docker.com/docker-for-windows/install/` (the slide says Hyper-V is required).
  - Linux: `https://docs.docker.com/install/linux/docker-ce/ubuntu/`.
  - Then run `docker run hello-world` to check the install.
  - These are older Docker-docs paths; check that they still resolve before showing them.
- **Tutorial repo:** `https://github.com/dlops-io/simple-translate` (slides 54–55, 63, 66, 70, 72).
- **Detailed tutorial instructions (slide 72, with a QR code):** `https://github.com/dlops-io/simple-translate#developing-app-using-containers-t3`.
- **VM tutorial (slide 77, with a QR code):** `https://github.com/dlops-io/simple-translate#running-app-on-vm-using-docker-t4`.
  - The `-t3` / `-t4` anchors on slides 72 and 77 do not match any heading of the README at `62f821b`. The actual GitHub anchors are `#-developing-app-using-containers` and `#%EF%B8%8F-running-app-on-vm-using-docker` (`digest.md` header and E6).
  - The links therefore open the README at the top.
- **Forward references:**
  - Slide 46's example image `transcribe-audio` matches the `transcribe_audio` stage of the L03 mega-pipeline.
  - Slides 78–79 (the Cheese App split into containers) preview the multi-container lectures that follow, "Containers II".
  - Slide 29 names Kubernetes as part of Docker's ecosystem (covered in L22).
- **Demo app on the closing slides:** the Cheese App. Its screenshots show a cheese-classifier web page, a Colab notebook and the data-collection script (slide 78).

## This video and the slides

**Basis.** The video is built: script v2 with 16 scenes in two parts (`script.md`, `BRIEF.md`, `video.yaml`), real captures from 2026-10-13 (`ASSETS.md`, `assets/terminal/`), and a full cut whose scene start times are in `output/chapters.txt`. The times below come from that cut. No scene uses `lecture_ref` yet. For this cross-check, all nine contact sheets were read again, and slides 57–60 and 64 were re-rendered at 150 dpi in the session scratchpad (not in this repo) to check their code, logs and labels. Every "today" below cites a capture where one exists. Where a slide and a capture disagree, the capture shows what the commands do today.

**Tag form.** `lecture_ref(2, "a–b")` (`explainer/devops.py`) prints "Lecture 2 · slides a–b", top right, across from the README tracker. The helper prints the lecture number without a leading zero, which also matches the deck's own title, "Lecture 2".

### 1. Map: scenes ↔ slides

| Scene (start) | Slides on the same ground | Relation |
|---|---|---|
| S01 · One command on a fresh VM (00:00) | 5–7, 77 | Same concept: one command on a bare VM meets slide 7's wish list (automated setup, quick start-up). The run previews slide 77, which S14–S15 apply. The README ladder and the 3.12-vs-3.14.7 puzzle are tutorial-only. |
| S02 · Image, layer, container, registry (01:22) | 9–12, 22–24, 30–31, 35, 38 | Same concept: the lecture's "What is a Container" and its Docker vocabulary in four minutes. Namespaces and cgroups (11, 13–18) are only implied, by "isolated processes". |
| S03 · A clean slate, and the clone (03:13) | 52, 54, 61–62, 65, 73 | The tutorial applies it. The README prunes at the start without `-a`. The lecture prunes at the end with `-a` (Conflict 6). |
| S04 · Dockerfile step 1: FROM (04:56) | 30, 32, 56–58 | The tutorial applies it. The build-command anatomy is slide 56's. The config card (`Cmd=["python3"]`) and the plain log are tutorial-only. |
| S05 · Step 2: ENTRYPOINT (06:52) | 32–33; 17, 19 (the `root@` prompt) | The tutorial applies it. That a Dockerfile ENTRYPOINT clears the inherited CMD is tutorial-only. It is the Dockerfile twin of Conflict 1. |
| S06 · Step 3: install uv, copy the code (07:58) | 33, 56–58 | The tutorial applies it. The lecture explains "." as "the current working directory". The video's build-context parcel goes further. Slide 58's own log has the same `load .dockerignore` → `2B` line. |
| S07 · Step 4: uv sync, and two Pythons (09:40) | 37 (the "UV Sync" bar), 57–58 | Mostly tutorial-only. The deck never mentions a second Python. Slide 37 draws one Python layer (Conflict 8). |
| S08 · Step 5: CMD, the solution, the build (12:09) | 32–33, 57–58 | The tutorial applies it. Slide 57 is the lecture's copy of the solution, an earlier draft (Conflict 2). The final compact build is the view slide 58 shows. |
| S09 · Run it, translate, exit (14:06) | 13–14, 31, 39–42, 63–65, 74 | Same concept, and the tutorial applies it: the run (63–64), `ps -a` (74), PID 1 (14, shown but not named), many containers from one image and the CMD override (39–41, here the exit-126 puzzle), and `--rm` as "ephemeral" (42). |
| S10 · What's inside the image (16:19) | 22, 34–37, 59 | Same concept, measured: slide 59's two commands, with today's numbers (Conflict 3). The finding that `.git` ends up inside the image is tutorial-only. |
| S11 · The layer cache (18:05) | 36, 58, 60 | Same concept, and the video goes further. Slide 60 shows an all-cached rebuild. The video adds what breaks the cache: the context checksum, `.git/index`, and a fix by reordering the Dockerfile. |
| S12 · Tag and push (20:00) | 36 (only changed layers travel), 38, 66–69 | The tutorial applies it. The stand-in registry, the real push denial and "public by default" are tutorial-only. |
| S13 · Platforms: arm64 vs amd64 (22:04) | none | Tutorial-only. The deck never mentions CPU architecture. |
| S14 · A VM with only Docker (24:39) | 11–12, 23–24, 77 | The tutorial applies slide 77. The V8 half (no hidden VM on a Linux host) is the contrast to slide 24. `apt-get update`, Debian's `docker.io`, `sudo` and the socket are tutorial-only. |
| S15 · One-command deploy (26:35) | 26, 70–72, 77 | The tutorial applies it, with Conflict 4 (whose image runs). "Ship the image, not the recipe" is slide 26's portability point in the tutorial's terms. |
| S16 · Tear down, recap, and what's next (28:36) | 26, 73; 42–51, 78–79 (the L3 teaser) | Recap of the same concepts. The teaser previews the lecture's mounts and slide 79's "Isolate work into containers". Deleting the VM is tutorial-only. |
| no scene | 1–4, 8, 25, 27 (title, logistics, agenda, dividers); 13, 15–21 (the other namespaces, cgroups, security); 28–29 (other container tools); 43–51 (mounts in detail); 74–76 beyond `ps -a` (debugging); 78–81 | Lecture-only. Gaps 1–3 and 5–8 below say which of these are worth carrying. |

### 2. Already in common

| # | Concept | Scene ↔ slides | Does the video's framing agree with the lecture's? |
|---|---|---|---|
| 1 | A container is not a VM. It shares the host's Linux kernel and carries only user-space files. | S02 (V8), S14 ↔ 9–10, 12, 22 | Yes. The video's "not a small VM" is firmer than slide 9's "like a mini computer". The video's "isolated processes" leaves out the lecture's two mechanisms (gap 2). |
| 2 | On a Mac or Windows laptop, a hidden Linux VM supplies the kernel. A Linux host needs none. | S02, S14 ↔ 23–24 | Yes. The video names no VM technology (Conflict 10) and draws no system calls through the daemon (Conflict 9). Both choices are correct. |
| 3 | What a venv, a VM and a container each isolate | S02 (last beat), S16 (V1) ↔ 5–7, 10 | Yes. "What a venv couldn't isolate … is now inside the box" answers slide 6's "No Isolation from Host". GPU drivers that stay "the host's" match slide 22, which puts the GPU inside the kernel box. |
| 4 | An image is read-only layers plus a config. A container is that image plus one writable layer. | S02, S09 ↔ 31, 35 | Yes, closely. The glass slab is slide 35's writable layer "added on top", and the locked stack is its read-only "static snapshot". |
| 5 | Image as class, container as instance; many containers from one image | S02, S09 ↔ 31, 39–40 | Yes, it is the same analogy. The lecture's second analogy (recipe, meal kit, cooked dish, slide 31) and slide 38's "store vs run" are not used. |
| 6 | Dockerfile → build → image → run → container | S02, S04 ↔ 30, 38, 56 | Yes. "Building makes an image" matches slides 30 and 56. The checklist slides say "Build a container" (Conflict 7). |
| 7 | RUN and COPY add layers; other instructions only change settings | S02, S05, S10 ↔ 32, 34, 37 | Partly. Slide 32 agrees ("each RUN creates a new layer"). Slide 34 says every command makes a layer (Conflict 8). The captured `CACHED` step (`laptop/14`) and the `0B` rows (`laptop/34`) settle it. |
| 8 | ENTRYPOINT is the program, CMD its default arguments, and `docker run` arguments replace CMD | S05, S09 ↔ 32–33, 40–41 | Yes. The video adds two things the deck doesn't say: a Dockerfile ENTRYPOINT clears an inherited CMD (`laptop/15`), and replacing CMD can backfire (exit 126, `laptop/36`). |
| 9 | `docker build -t simple-translate -f Dockerfile .` and the final dot | S04, S06 ↔ 56 | Yes. The video turns "the current working directory" into "the build context, sent to the builder", which slide 58's log line `transferring context` already shows. |
| 10 | Each numbered build step is one instruction | S04, S08, S11 ↔ 58, 60 | Yes. The steps are the same four, `[1/4]`–`[4/4]`, in the same order: base, the apt/pip RUN, the copy, `uv sync`. Slide 60's header reads `docker:desktop-linux`, which matches S04's Docker Desktop note. |
| 11 | An unchanged step is reused from the cache | S07, S08, S11 ↔ 36, 60 | Yes. The video adds what invalidates a step, which the lecture leaves out. |
| 12 | Listing an image's layers and their sizes | S10 ↔ 59 | Yes. `docker image history` (slide) and `docker history` (video) are the same command. The numbers differ (Conflict 3). |
| 13 | Layers are shared, and only missing ones travel | S02, S12 ↔ 36 | Yes: "shared, not copied" and `Layer already exists` (`laptop-push/08`). |
| 14 | `--rm`, `-t`, `-i`, and containers as ephemeral | S04, S09 ↔ 42, 64 | Yes. Slide 64's "t gives a terminal, i is interactive" matches S09's labels. Slide 42's "discarded once the container exits" is the dissolving glass slab. |
| 15 | Registry, tag, the default `latest`, and your username in front | S02, S12 ↔ 38, 68–69 | Yes. |
| 16 | Log in with an access token, not your password | S12 ↔ 67 | Yes on the token, no on `-p`. The video already corrects that kindly (Conflict 5). |
| 17 | `docker image ls`, `docker container ls` and `prune` | S03, S16 ↔ 61–62, 65, 73 | Yes. |
| 18 | On the VM: create it, SSH in, install Docker, run | S14–S15 ↔ 77 | Yes. The video adds `apt-get update`, `sudo`, and the question of whose image runs (Conflict 4). |
| 19 | One image, from laptop to production | S15, S16 ↔ 26 | Yes. The video adds the CPU caveat (S13), which the lecture never makes. |
| 20 | bash is PID 1 in its container | S09 ↔ 14 | It is shown (`echo $$` → `1`, `laptop/33` line 5) but not named as the PID namespace (gap 2). |

### 3. Gaps (ranked by value to a student doing the tutorial)

1. **The debugging kit (slides 74–76).** Three facts the video never states:
   - `docker ps -a` lists exited containers with their exit codes, but only without `--rm`, which is why S09's capture is empty.
   - `docker logs <name>` shows a container's output, and `docker exec -it <name> /bin/bash` opens a second shell in a running one.
   - `docker run -it --entrypoint /bin/bash <image>` lets you inspect an image whose container exits at once. Slide 57's draft would be one (Conflict 2).
   
   Every failure in this tutorial (exit 126, `ModuleNotFoundError`) is a case for these tools. **Carry it in** S09, as a tag at the `docker ps -a` beat. The commands themselves belong in the guide.
2. **What "isolated processes" means: namespaces and cgroups (slides 11–18, 22).** This is the lecture's biggest block, and the video never names it. It is visible in S09: bash is PID 1 because the container has its own PID namespace (slide 14). **Carry it in** S02 (two chips on the kernel bar) and S09 (one bridge at `echo $$`).
3. **Ephemeral containers, and mounts as the answer (slides 42–51).** S11 shows the pain: every edit to `cli.py` means a rebuild. Slide 42 names both needs, a live development loop and outputs that persist. Slides 43–51 cover bind mounts vs named volumes vs tmpfs, how `-v` decides by the slash, `--mount` as the safer form, and `:ro`. This image keeps its code in `/` with no `WORKDIR`, so don't mount the repo here; L03 adds `WORKDIR /app` and `-v "$(pwd)":/app`. **Carry it in** S16 (a tag and a bridge on the L3 teaser), and in S11 as a tag only if wanted.
4. **Watching a running container from a second terminal (slide 65).** While the container runs, `docker container ls` lists it. The video only lists before (`laptop/01`) and after (`laptop/32`), and no capture shows a running row. **Carry it in** S09's run beat, as narration only. It is low priority.
5. **Least privilege (slides 17, 19–21).** Containers rarely need root. Docker removes about 44 system calls. AppArmor/SELinux are security, not resource limits like cgroups (slide 21's warning). In the video, S05 reads `root@` and S06 waves off pip's root warning ("the image itself is the isolation"), which is looser than the lecture. The VM install pulls in `apparmor` and `cgroupfs-mount` (`vm-debian12/03` line 8). **Carry it in** S05 (one bridge) and S14 (that install line).
6. **Why an image is small: there is no kernel in it (slide 22).** The bottom row of `docker history` is Debian's files (`debian.sh … bookworm`, 85.3MB, `laptop/34`). Nothing below it is a kernel. **Carry it in** S10.
7. **Why the course cares (slides 78–79).** The Cheese App's pieces are built on Macs, Windows, Colab and a Linux server, and the lecture splits them into containers. That is the "five containers" of the next lecture. **Carry it in** S16's Next card.
8. **Dockerfile instructions the tutorial doesn't use: ADD and WORKDIR (slide 33).** ADD appears in slide 57's draft, and S05 shows the missing working directory (`WorkingDir=""`). **Carry it in** S08's diff note (ADD) and S16's teaser (`WORKDIR /app`, already there). It is low priority.

### 4. Conflicts

| # | Slides say | Tutorial and captures today | Current | How the video should put it kindly |
|---|---|---|---|---|
| 1 | **The run command** (slide 64): `docker run --rm --name simple-translate -ti --entrypoint /bin/bash simple-translate`. The call-out says `--entrypoint` overrides the Dockerfile's ENTRYPOINT. | The README runs `docker run --rm -ti simple-translate` (`laptop/31`: translates). Overriding the entrypoint at run time also drops the image's CMD, the part that activates the venv (`laptop/26`: `which python` → `/.venv/bin/python` only through CMD). The result is a bare bash where `python cli.py` fails, as in `laptop/22` lines 10–14. `--name` also collides with a second run (exercise check C7, exit 125). The slide's exact command was not captured; the mechanism was. | The README's command | S08, after the run checks, one bridge: the lecture's command adds `--entrypoint`, which drops this CMD and the venv with it. Tag "Lecture 2 · slides 64, 75": slide 75 lists `--entrypoint /bin/bash` as a debugging move, which is what it is. |
| 2 | **The Dockerfile** (slide 57): `ADD . /`; `apt-get install … build-essential git`; two commented-out uv `ENV` lines; CMD sources `/home/app/.venv/bin/activate`. | `Dockerfile.txt`: three active `ENV` lines, `apt-get clean`, `COPY . ./`, and CMD sources the relative `.venv/bin/activate` (`laptop/27`). `uv sync` creates `/.venv` (`laptop/21` line 33). With the `UV_PROJECT_ENVIRONMENT` line commented out, the slide's `source` would fail and its `&&` would end the container at once (not run here). | The repo's `Dockerfile.txt` | S08, at the diff, a GREY on-screen note: "lecture slide 57: an earlier draft · build this file". No narration needed. |
| 3 | **Screenshots** (slides 58–60): a `python:3.11-slim-buster` base; `docker images` 483MB, with two images sharing one ID; a `docker image history` with `USER app`, `WORKDIR /app`, `ENTRYPOINT ["uv" "run"]` and Python 3.12.11 (our reading: an L03-style Dockerfile); slide 60's command builds `hello_world_cmd`, but its log names `simple-translate`. | `python:3.12-slim-bookworm@sha256:34386ef0…` (`laptop/09`); `518MB` disk / `144MB` content in Docker 29's columns (`laptop/30`); history 97.5MB / 250kB / 125MB, `ENTRYPOINT ["/bin/bash"]`, `PYTHON_VERSION=3.12.15` (`laptop/34`); all `CACHED` on an unchanged rebuild (`laptop/38`). | The captures | Tags only, at S10 and S11. Never redraw the slides' numbers. S03 already says "your columns may differ". The viewer compares with the terminal panels. |
| 4 | **Whose image runs on the VM** (slides 70–72): "Pull the new container and run it", with a generic `docker pull <USER NAME>/<TARGET_IMAGE[:TAG]>`. There is no word on CPU platforms. | The README runs the instructor's `dlops/simple-translate` (`vm-debian12/06`), a single amd64 manifest (`laptop-push/10`). An arm64 image on an amd64 host fails with `exec format error` (`laptop-push/12`). | The README's command for what runs; the slides' intent for what should | S15 already says it ("the README promises to pull the image you pushed…"), and S13 covers platforms. A tag at S15 is enough. |
| 5 | **Login** (slide 67): `docker login -u <USER NAME> -p <ACCESS TOKEN>`, called secure because it uses a token. | Same command in the README. Docker itself warns `Using --password via the CLI is insecure` (`laptop-push/05` line 2). | Type `docker login -u <USER NAME>` and paste the token | S12 already does this ("a small slip in the README"). Optionally, one bridge noting that the slide has the same form. |
| 6 | **Clean-up** (slide 73): `docker system prune -a`, "remove all images not used by any container". | The README's `docker system prune` removes only dangling images (`laptop/02`: "all dangling images"). | Both are right; they do different jobs | S03 and S16 already say both. Add a tag at S16's `prune -a`. |
| 7 | **"Build a container"** (checklist slides 55, 63, 66, 70, 72; also "Push container", "Pull the new container"). | The build names an image: `naming to docker.io/library/simple-translate:latest` (`laptop/09`). The lecture's own slides 30 and 56 say "image". | Image | S02 already says it about the README. Nothing to add: the deck agrees with itself on slides 30 and 56. |
| 8 | **What an image is made of**: an "iso file and other files" (30); "a layer for every command" (34); slide 37 stacks Kernel, Debian, Python & Pip, Upgrade Pip, Install UV, UV Sync, with no code layer and one Python. | Layers plus a config. `ENV`/`ENTRYPOINT`/`CMD` rows are `0B`. The apt/pip/uv work is one RUN of 97.5MB, `COPY . ./` is a 250kB layer, the bottom is Debian (85.3MB) and no row is a kernel (`laptop/34`). There are two Pythons (`laptop/33` lines 9, 11). | The captures | S02, S05 and S10 already show it. Optionally, in S10, a dashed GREY "kernel: the host's" bar under the stack (Proposals). |
| 9 | **System calls** (slides 22, 24): a "Syscalls" line runs from the Daemon to the Linux kernel, and on a Mac or PC the VM "translate[s] syscalls from the Daemon". | A container's own processes call the kernel directly. Here bash is the container's own PID 1 (`laptop/33` line 5). The daemon only sets up namespaces and cgroups. This is a conceptual point, not something a capture decides. | The video's picture | V8 (S02, S14) already stands the containers on the kernel bar. Keep it that way, with no syscall arrow through `dockerd`. Nothing to say aloud. |
| 10 | **VM technology names** (slides 24, 52): HyperKit on a Mac, and Hyper-V "required" on Windows (slide 24 says WSL2). | Current Docker Desktop uses Apple's Virtualization framework on a Mac and the WSL 2 backend by default on Windows. This was not verified in this repo (no Mac or Windows capture). | Current Docker Desktop (unverified here) | S02 already says "a small, hidden Linux VM" without a product name. Keep it. |
| 11 | **Root** (slide 17): a process running as root inside a container "will have non-root privileges in the host". | That is true only with user-namespace remapping or rootless Docker, which a default install (the captures' engine, Debian's `docker.io`) doesn't turn on. The socket being root-only (`vm-debian12/05`) is the same story. Not captured as such. | Docker's default: root inside is root, limited by capabilities, seccomp and AppArmor | S05's "You're root, the administrator, inside the container" is accurate. Don't add "but harmless outside". Optionally, one bridge to L03's non-root user. |
| 12 | **Links** (slides 72, 77): README anchors ending in `-t3` and `-t4`. | No README heading at `62f821b` has those anchors, so the links open the README at the top (`digest.md` E6). | The README's headings | Not on screen. S03 and S14 name the README sections aloud, which is enough. |

Not counted: slide 54 clones without `.git` (both URLs work); slide 53's `docker --version` on the laptop (the video shows the VM's `sudo docker --version` and says "Docker 29" for the laptop); slide 41's demo prints the instructor's name, which the series never shows or says (BRIEF, "Things never to do on screen").

### 5. Proposals

**General**
- **Tags** cost no narration, only a re-render of the scene. Pin one tag per beat and fade it with that beat's picture. Check that it doesn't overlap S01's top-right Docker Hub glyph or a full-height terminal.
- **Bridges** cost a lexicon entry for new words (`PID` read as letters, `cgroups` as "see groups", `apparmor`), a matching Chinese line in `i18n/zh/narration/g1.yaml` (S01–S09) or `g2.yaml` (S10–S16), and new TTS and timing for that scene only. Two bridges are marked "do" (S08, S09, about 32 words, about 13 s). The rest are "nice".
- **"Namespace"** keeps one meaning in this video, the kernel's. In S12, don't adopt slide 68's "repository namespace".
- **Never on screen:** slide images, memes, or the instructor's name (slide 41's output, slide 55's labels).

**Per scene**
- **S01**
  - (i) *nice:* "Lecture 2 · slides 5–7" with the V1 ladder, from the SAY "Last lecture we climbed its first two rungs", after the Docker Hub glyph has gone.
  - (ii) none: the hook stays a puzzle.
  - (iii) none: the crossed chips (code, venv, uv) already read as slide 7's "Automated Setup".
- **S02**
  - (i) *do:* "Lecture 2 · slides 30–31, 35" from "An image is a stack of read-only layers" through "Think of the image as a class". Then "Lecture 2 · slides 9–12, 22–24" from "And a container is not a small VM" to the end of the scene.
  - (ii) *nice:* after "Containers are isolated processes that share one Linux kernel.": "The lecture names the two kernel features behind this: namespaces and cgroups." (12 words)
  - (iii) *do:* in V8's first half, two small chips on the shared kernel bar, "namespaces" and "cgroups" (slide 22's two tiles inside the kernel box), and the caption "user space" under the TEAL boxes (slide 22's headline). They appear during the same SAY, with no new narration. In the Mac half, keep the dashed VM under the kernel bar, with no arrow through the daemon (Conflict 9).
- **S03**
  - (i) *do:* "Lecture 2 · slides 54, 61–62, 73" from "First, docker container ls lists running containers" to the end of the scene.
  - (ii) none: the SAY already covers `-a`.
  - (iii) none.
- **S04**
  - (i) *do:* "Lecture 2 · slides 32, 56" at "Now the build command. Dash t names the image simple-translate", through the build.
  - (ii) none.
  - (iii) *nice:* two more anatomy labels, `docker` "the CLI" and `build` "build the image", so the line reads token by token as on slide 56. Keep the existing three labels.
- **S05**
  - (i) *do:* "Lecture 2 · slides 32–33" at "Think of ENTRYPOINT as the program to start, and CMD as its default arguments."
  - (ii) *nice:* after "You're root, the administrator, inside the container.": "Today's lecture adds a caution: containers rarely need root, and lecture 3 switches to a normal user." (17 words; gap 5, Conflict 11)
  - (iii) none: V3's "the program" and "its default arguments" already say what slides 32–33 say.
- **S06**
  - (i) *nice:* "Lecture 2 · slides 56–58" at "Here's why the final dot matters."
  - (ii) *nice:* after "…travels to the builder.": "The lecture's build log shows the same two lines: no dockerignore, and the whole folder sent." (16 words)
  - (iii) *nice:* label the PINK parcel route "transferring context", the log's own words, which slide 58 shows too.
- **S07**
  - (i) *nice:* "Lecture 2 · slide 37" as the fat GREEN "RUN uv sync" slab lands ("…and the venv's python links to it.").
  - (ii) none: two Pythons is tutorial-only.
  - (iii) none.
- **S08**
  - (i) *do:* "Lecture 2 · slide 57" at "The README then points to a solution, Dockerfile.txt.", with a GREY note under the diff: "lecture slide 57: an earlier draft · build this file" (Conflict 2). With the bridge below, show "Lecture 2 · slides 64, 75" during it.
  - (ii) *do:* in the run block, after "The fresh bash set its own prompt.": "The lecture's run command adds dash dash entrypoint, which drops this CMD, and the venv with it." (17 words; Conflict 1)
  - (iii) none.
- **S09**
  - (i) *do:* three tags:
    - "Lecture 2 · slides 63–65, 74" from "Now the README's Run Docker Container step" to the `docker ps -a` beat;
    - "Lecture 2 · slides 13–14" at "In a second run, an extra check, echo dollar dollar, shows that bash is process number 1.";
    - "Lecture 2 · slides 40–41" at "Now a puzzle."
  - (ii) *do:* right after that PID sentence: "That's the PID namespace from today's lecture: each container counts its own processes from 1." (15 words; gap 2)
  - (iii) *nice:* a thin GREY dashed outline around the new container, "PID namespace", with a small note "the host numbers it differently" (slide 14; not captured, so no number).
- **S10**
  - (i) *do:* "Lecture 2 · slides 34–37, 59" at "Then docker history lists the layers, newest first."
  - (ii) *nice:* after "…and Python 3.12.15.": "Notice what's missing at the bottom: a kernel. As the lecture puts it, a container is user space." (18 words; gap 6)
  - (iii) *nice:* beside the rescaled stack, slide 37's upward arrow labelled "build order". Under the base slabs, a thin dashed GREY bar "kernel · the host's, not in the image": slide 37's bottom bar, corrected kindly (Conflict 8).
- **S11**
  - (i) *do:* "Lecture 2 · slides 36, 58–60" at "Docker caches every build step."
  - (ii) *nice:* after "…all say CACHED: nothing runs.": "The lecture showed this all-cached rebuild; next, what breaks the cache." (11 words)
  - (iii) *do:* a GREY caption under the four boxes, "one numbered step per instruction" (slide 58's four arrows). Keep the TEAL `CACHED` stamps, the word slide 60 points at.
- **S12**
  - (i) *do:* "Lecture 2 · slides 67–69" at "Next, log in: docker login, dash u with your user name, dash p with your token.", through the push.
  - (ii) *nice:* after "…paste the token when it asks.": "The lecture slide shows the same dash p form, so the same advice applies." (14 words; Conflict 5)
  - (iii) *do:* keep "account" in V6's name breakdown, and don't add slide 68's "repository namespace".
- **S13**
  - (i) none: the scene is tutorial-only. No tag.
  - (ii) none.
  - (iii) none.
- **S14**
  - (i) *do:* "Lecture 2 · slide 77" at "The last README section: Running App on VM using Docker." Then "Lecture 2 · slides 12, 24" at "Here Docker runs right on the VM's Linux kernel".
  - (ii) *nice:* after "…118 megabytes on Debian 13.", with `vm-debian12/03` lines 7–8 added to that panel: "Among them are apparmor and cgroupfs, the lecture's security and resource tools, arriving with Docker." (15 words; gap 5)
  - (iii) *do:* split the VM's bar "Debian · Linux kernel" into "kernel" with "user space · Debian" above it, and put `dockerd` on user space (slide 12's stack). The crossed dashed "Docker Desktop only" box is then exactly slide 24's extra VM layer.
- **S15**
  - (i) *do:* "Lecture 2 · slides 70–71" at "Then the deploy: sudo docker run, dash dash rm, dash t i, dlops slash simple-translate."
    *nice:* "Lecture 2 · slide 26" at "An image freezes all that: ship the image, not the recipe."
  - (ii) *nice:* after "…then starts a container.": "The lecture pulls first with docker pull; docker run does that pull for you." (14 words)
  - (iii) *nice:* label the PINK route from the shelf "pull" (slide 71's verb), as S16's route labels "push" and "run".
- **S16**
  - (i) *do:* "Lecture 2 · slide 73" at "And to reclaim the space your images take on the laptop, run docker system prune dash a." Then "Lecture 2 · slides 42–51, 78–79" on the Next card.
  - (ii) *nice:* at the end of the last SAY: "Mounts are already in today's lecture slides; lecture 3 puts them to work." (13 words; gap 3)
  - (iii) *nice:* on the GREY dashed teaser, rename "mounted" to "bind mount" (slide 43's term). The five TEAL boxes already echo slide 79's "Isolate work into containers".

**The three most valuable**
1. **S09 · the PID namespace at your terminal** (tag "Lecture 2 · slides 13–14" plus a 15-word bridge at `echo $$`). It turns the lecture's longest abstract block into a line the student just typed.
2. **S08 · the lecture's run command and Dockerfile, kindly** (the slide-57 note under the diff, plus the 17-word bridge on slide 64's `--entrypoint`). It protects the student who follows the slides from a container whose venv is not active.
3. **S02 · "namespaces" and "cgroups" on the kernel bar, and "user space" on the containers** (with the two S02 tags). These are the lecture's core terms, placed in the video's existing picture with no new narration.
