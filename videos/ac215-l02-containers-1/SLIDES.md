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
