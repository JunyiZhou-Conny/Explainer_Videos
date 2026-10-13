# AC215 第 2 讲视频中文字幕词表（中英混用版，只有字幕）

视频：*AC215 · Lecture 2 — Containers I: one image, from laptop to VM (follow-along: simple-translate)*（`videos/ac215-l02-containers-1`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，英文技术文档读得很顺；做过第 1 讲（云上的 VM、venv、uv）和 Tutorial 0（Docker Desktop、GCP 项目），第一次写 Dockerfile、第一次弄清 image 和 container；边看边在自己的笔记本上敲命令，最后在自己的 VM 上部署  
语音：**没有中文配音**。这个系列只有英文旁白；中文是按英文时间轴显示的字幕（`output/<id>.zh-en.mp4` 下方的双语字幕带、`<id>.zh.srt`、`<id>.zh-en.srt` / `.ass`）。所以没有 `say:`、没有锚点、没有读法、不测时长，第 1 讲里所有关于朗读的规则（F1–F6、C2–C5、“三点十一点二”“点 venv”这类读法）都不适用；只保留显示规则  
英文原稿：`script.md`（SAY 行是旁白，SHOW 行是画面；129 段、371 句）  
先例：系列试点 [`../../../ac215-l01-vms-venvs/i18n/zh/`](../../../ac215-l01-vms-venvs/i18n/zh/)（共用术语一律沿用第 1 讲，除非下面的规则说明为什么不）；同时在写的第 3 讲 [`../../../ac215-l03-mega-pipeline/i18n/zh/`](../../../ac215-l03-mega-pipeline/i18n/zh/)（容器 II：容器相关的词和这里完全一致；第 3 讲提到的“第 2 讲的包裹”“多米诺骨牌”就是这一讲引入的画面）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 助教带实验课时本来就中英混着说：“写个 Dockerfile”“构建 image”“起一个 container”“给 image 打 tag”“push 到 Docker Hub”“pull 下来”“把 repo clone 下来”“激活 venv”。硬译成“容器镜像”“推送到镜像注册中心”反而像说明书；字幕里的“镜像”还会和 Debian 的 mirror（第 1 讲叫“软件源”）撞车。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端和 Docker Hub 页面上找东西。命令、参数、文件名、路径、image 名、Dockerfile 指令、报错原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念一律说中文：层、可写层、构建、构建上下文、缓存、指令、进程、内核、平台、模拟器、仓库、访问令牌、提示符、目录、软件包、部署。
- 双语字幕（中文在上，英文原句在下）已经把每个英文原词放在中文正下方，所以中文行不加括注；而且没有 say: 时 check 根本不允许括号（D3）。
- 这个系列不翻译画面：终端、代码面板、README 引文、标签（your turn、extra、stand-in……）、进度条、“Pause and ponder”卡片都是英文。旁白提到画面上的标签时，字幕照画面写（黄色的 your turn 标签）。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众是上 AC215 的中文研究生：英文技术文档读得很顺，平时就说“开一台 VM”“把 repo clone 下来”“激活 venv”“写个 Dockerfile”“构建 image”“起一个 container”“打 tag”“push 到 Docker Hub”“pull 下来”。每个选择过三关：实验课上的真实说法；Docker 和 Google Cloud 中文文档里能搜到的标准中文名；和整个系列一致（第 1 讲定下了共用术语；第 3 讲用同一套容器词汇）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、image 名和包名、Dockerfile 指令、配置字段、终端原文和报错、README 的章节标题）逐字照抄，从不翻译、不变形、不加引号；check 不允许的字符（下划线、=、< >、括号和引号）出现在实物里时，用文字描述（A6），英文行用 en_display 给出字面形式（D4）。这个系列画面一律不翻译：终端输出、代码面板、README 引文卡、标签、进度条、思考卡片都保持英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 VM、venv、shell、root、repo、clone、commit、pin；容器这几讲新增 container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、digest、socket、Docker daemon、attestation、locale、ID。
3. **其余一律用中文标准术语**：层、只读层、可写层、配置卡片、指令、构建、重新构建、构建步骤、构建上下文、构建器、缓存、层缓存、精简视图、完整日志、校验和、指纹、进程、主进程、内核、平台、多平台、机器码、模拟器、仓库（Docker Hub 上的一个 repository）、账号、用户名、访问令牌、密码、读写权限、后台服务、根目录、工作目录、提示符、终端、目录、包、软件包、软件包列表、激活、部署、计费。
4. **视频的比喻按意思译，一个比喻一个词**：配方（把 Dockerfile 比作 recipe）、配置卡片、类和实例、货架（registry 的 shelves）、包裹（构建上下文）、多米诺骨牌（缓存连锁失效，只在画面里）、菜单（多平台 tag）、门（socket）、计价器、梯子和“级”（第 1 讲）、数轴（第 1 讲）。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、基础镜像、镜像仓库、标签、推送、拉取、仓库、克隆、提交。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方。
7. **工具链的约束也是规则**：每个英文句子对应一个中文句子（129 段、371 句）；显示行要能通过 check（D3）；SAY 把实物念成单词的句子要写 en_display（D4）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **container 和 image 说英文**（和第 3 讲一致）：字幕里说 container、image，量词“个”；标题、章节名、meta.yaml、配套文档写“容器”“镜像”。字幕里不写“镜像”：它也是 Debian mirror 的日常说法。第 1 讲在预告下节课时写过“容器”“镜像”，那是书面语体；从第 2 讲起，字幕和实验课一样中英混说。base image 也照说英文（画面上的标签就是 base image），书面写“基础镜像”。
- **其余 Docker 概念用中文**：build → 构建，layer → 层，cache → 缓存，build context → 构建上下文，builder → 构建器，instruction → 指令，kernel → 内核，platform → 平台。不为了“味道”说英文。
- **registry、仓库、repo 三分**：registry（Docker Hub 整体，书面“镜像仓库”）；仓库（Docker Hub 上的一个 repository，四段式长名字里的第三段）；repo（git 仓库，口语，书面才写“仓库”，那时 Docker Hub 的一律写“Docker Hub 仓库”）。
- **tag 和“标签”分开**：字幕里 Docker 的 tag 说 tag（打 tag、tag 是 latest），“标签”留给画面上的视频标签（黄色的 your turn 标签、灰色的 extra 标签）；书面里“标签”指 Docker tag（章节名“打标签并推送”）。
- **画面标签照画面写**（和第 3 讲一致）：第 1 讲写“轮到你了”“额外”，是因为当时计划把画面也翻译；现在画面是英文，所以字幕写 your turn 标签、extra 标签。旁白自己说的 an extra check 照常译“额外检查”。
- **只有 Dockerfile 的五步叫“第 k 步”**：README 只给这五步编号，旁白也只给它们编号；BuildKit 的步骤叫“构建步骤”（FROM 那一步、pip 那一步），不编号；进度条的 step k of N 留在画面上。
- **check 不允许的实物用文字描述**（A6）：VIRTUAL_ENV → virtual env 这个变量；raise_exception=True → 把 raise exception 设为 True；--progress=plain → --progress 参数设成 plain；--platform=linux/amd64 → --platform 参数设成 linux/amd64；`<USER NAME>` → 你的用户名；exit() → 带括号的 exit；(app) → 带括号的 app。英文行用 en_display 给出字面形式。
- **单独的点用文字说**：构建命令末尾的 . → 末尾那个点；COPY . ./ 里的 . 和 ./ → 那个点、点斜杠（混在中文标点里，单独一个点看不出来）。
- **比喻**：Dockerfile 是“配方”（不是“菜谱”）；registry 的 shelves 是“货架”（不用第 1 讲 sys.path 的“架子”）；构建上下文是“包裹”；多平台 tag 是“菜单”；socket 是“门”。
- **勘误**：一个小疏漏（README 说 build the docker container；docker login 用 -p）、一个小缺口（没有 .dockerignore；跳过了 apt-get update）、一个小小的不一致（requires-python 和 3.12 的 image；README 拉的是授课老师的 image）、一个小错误；后面一定紧跟改法（和第 3 讲同一套词）。
- **“录制时”**每次都译，绝不省略：3.12.15、uv 0.13.0、CPython 3.15.0、Docker 29、518 MB、20.10.24、26.1.5 都会变。
- **章节标题**：书面语体；和第 1 讲英文标题相同的一章沿用第 1 讲的中文（收尾、回顾和下节预告）；Containers I → 容器 I（第 3 讲是容器 II）。

## 保留英文的词（这一讲）

| 类别 | 词 |
|---|---|
| 实验课口语（封闭清单） | VM、venv、shell、root、repo、clone、commit、pin（第 1 讲）；container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、digest、socket、Docker daemon、attestation、locale、ID（容器这几讲新增，和第 3 讲同一份） |
| 命令和子命令 | docker container ls、docker stop、docker system prune（-a）、docker image ls、docker image inspect、docker build、docker run、docker ps -a、docker history、docker login、docker tag、docker push、docker buildx use default、git clone、git status、git add -f、git diff、git checkout、ls、ls -a、cd、cat、cp、diff（-u）、echo $$、which python、python --version、python cli.py、source、exec bash、bash -c、exit、pip install uv、uv sync、sudo apt install docker.io、sudo apt-get update、sudo docker --version、sudo docker run --rm -ti dlops/simple-translate、sudo docker login |
| 参数 | --rm、-t、-i、-ti、-f、-a、-u、-p、-c、--progress、--platform、--version |
| 文件、目录、路径 | Dockerfile、Dockerfile.txt、.dockerignore、.gitignore、.git、.vscode、.venv、/.venv、.venv/bin/activate、cli.py、pyproject.toml、uv.lock、docker-shell.sh、docker-build-push.sh、README、/usr/local/bin、/bin/bash、index 文件 |
| image、tag、包和构建器的名字 | python:3.12-slim-bookworm、simple-translate、simple-translate-ac215、dlops/simple-translate、hello-world、latest、library、docker.io、uv、pip、art、default、desktop-linux、linux/amd64、amd64、arm64 |
| Dockerfile 指令和配置字段 | FROM、RUN、COPY、ENV、ENTRYPOINT、CMD、null、requires-python |
| 终端原文和报错 | CACHED、DONE、failed to read dockerfile、nothing to commit、ModuleNotFoundError、No module named art、cannot execute binary file、push access denied、Mounted from library/python、exec format error、no matching manifest、Unable to locate package、Not Found、permission denied、toomanyrequests、dangling images |
| README 章节标题 | Developing App using Containers、Build Docker Image、Run Docker Container、Pushing Docker Image to Docker Hub、Running App on VM using Docker |
| 画面标签（旁白提到时） | your turn、extra |
| 产品、组织、课程、名字 | Docker、Docker Desktop、Docker Hub、Google、Google Cloud、Debian、bookworm、Python、CPython、Git、Git Bash、VS Code、Mac、Windows、Linux、Intel、AMD、Apple Silicon、CPU、E2、SSH、UTF-8、AC215、Tutorial 0、MLOps Learning、student、app、VM instances、Disks |

系列里常被问到、但这一讲没有出现的词：port、volume、endpoint、pipeline、embedding、prompt（LLM）、agent、LoRA、CI。第 1 讲把 endpoint 定为“接口”；pipeline、prompt（只指 LLM 的 prompt；shell 的 prompt 是“提示符”）、bind mount 由第 3 讲定为保留英文；其余留给用到它们的那一讲决定。

## 主要译名对照

| English | 这里的说法 |
|---|---|
| layer / read-only layer / writable layer | 层 / 只读层 / 可写层 |
| config card | 配置卡片 |
| instruction | 指令 |
| build / rebuild / build step | 构建 / 重新构建 / 构建步骤 |
| build context / builder | 构建上下文 / 构建器 |
| cache / layer cache / reused | 缓存 / 层缓存 / 重用 |
| compact view / full log | 精简视图 / 完整日志 |
| checksum / fingerprint | 校验和 / 指纹 |
| process / main process / kernel | 进程 / 主进程 / 内核 |
| class / instance | 类 / 实例 |
| start-up command line / default arguments | 启动命令行 / 默认参数 |
| top folder / working directory | 根目录 / 工作目录 |
| repository (Docker Hub) / account / user name | 仓库 / 账号 / 用户名 |
| access token / password | 访问令牌（简称令牌）/ 密码 |
| platform / multi-platform / machine code / emulator | 平台 / 多平台 / 机器码 / 模拟器 |
| deploy / ship | 部署 / 交付 |
| recipe / solution | 配方 / 参考答案 |
| stand-in | 替身 |
| background service | 后台服务 |
| package (Python) / package (apt) / package lists | 包 / 软件包 / 软件包列表 |
| on disk / content (docker image ls) | 磁盘占用 / 内容大小 |
| exit code | 退出码 |
| runtime error | 运行时错误 |
| a small slip / gap / mismatch / mistake | 一个小疏漏 / 小缺口 / 小小的不一致 / 小错误 |
| at the time of recording | 录制时 |
| written: container / image / base image / registry / tag / push / pull | 容器 / 镜像 / 基础镜像 / 镜像仓库 / 标签 / 推送 / 拉取 |

## 术语表

“字幕写法”是中文字幕行里的写法（标题和文档用 A4 的书面写法）；“首次出现”给出该词第一次出现的场景里的例句（每句都能通过 check）；没有中文配音，所以没有“朗读”一栏。

### 四个词：image、层、container、registry / The four words

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| image / images / a Docker image / the official Python image / image name | image / Docker image / image 名 / 镜像（书面） | S01：Docker 下载了一个 image，一共 7 层，然后在里面启动一个 shell。S02：一个 Docker image 把这些全都打包成一个可以复制的东西：系统文件、Python、各种包和代码。 | 实验课口语（A2），量词“个”。标题、meta.yaml、文档写“镜像”（A4）。字幕里不用“镜像”（它也是 Debian mirror 的日常说法）。the official Python image → 官方的 Python image；the image's top folder → image 的根目录。 |
| container / containers / a container is not a small VM | container / 容器（书面） | S02：运行一个 image，就得到一个 container：还是那些层，共用，再在最上面加一层薄薄的可写层，外加一个主进程。S02：而且，container 不是一台小 VM。 | 实验课口语（A2），量词“个”。标题和文档写“容器”。不说“集装箱”。 |
| base image / the base image's Python / inherited from the base image | base image / 基础镜像（书面） | S04：额外用 docker image inspect 读一下配置卡片：没有 ENTRYPOINT，CMD 是 python3，是从 base image 继承来的。 | 实验课口语，也是画面上的标签 base image。the pip of the base image → base image 自带的 pip。书面写“基础镜像”。 |
| layer / layers / read-only layer / a stack of read-only layers / in seven layers / add a layer | 层 / 只读层 / 镜像层（书面） | S02：一个 image 就是一叠只读层。每一层放的是某个构建步骤新增或改动的文件。 | 中国工程师就说“层”（书面“镜像层”）。字幕不写 layer。in seven layers（画面计数器显示 7 layers）→ 一共 7 层（C1）；add a layer → 加一层；no layer is added → 也没有加层。 |
| writable layer / a thin writable layer / writable layer and all | 可写层 | S02：进程结束，container 就停了，而 --rm 会把它删掉，连同可写层一起。 | 同第 3 讲。thin → 薄薄的。 |
| process / main process / process number 1 / the container lives as long as that process | 进程 / 主进程 | S09：第二次运行时，额外检查 echo $$ 显示 bash 是 1 号进程。只要这个进程还在，container 就还在。 | process number 1 → 1 号进程；PID 1 只出现在画面上。It ended the container's process → 它结束了 container 的进程。 |
| class / instance | 类 / 实例 | S02：可以把 image 想成一个类，每个 container 就是一个实例。 | 面向对象的类比。“实例”在第 1 讲也指 GCP 实例；控制台页面 VM instances 保持英文。 |
| registry / a registry like Docker Hub / stores images by name / shelves | registry / 货架 / 镜像仓库（书面） | S02：像 Docker Hub 这样的 registry，按名字把 image 存在货架上。 | 实验课口语；书面写“镜像仓库”。shelves → 货架（商店的货架），不用第 1 讲 sys.path 的“架子”。和“仓库”（Docker Hub 上的一个 repository）分开（A7）。 |
| tag / a tag / tagged latest / tag the image / latest | tag / 打 tag / latest / 标签（书面） | S02：所谓 tag，就是指向某一个 image 的名字，比如 latest。S12：接着给 image 打 tag。 | 口语：打 tag、tag 是 latest。字幕里“标签”留给画面上的视频标签（your turn 标签）；书面里“标签”指 Docker tag（章节名“打标签并推送”）。 |
| kernel / Linux kernel / the core of the operating system / isolated processes / share one Linux kernel | 内核 / Linux 内核 / 相互隔离的进程 | S02：VM 会启动自己的内核，也就是操作系统的核心。而 container 是一些相互隔离的进程，共用同一个 Linux 内核。 | 标准中文。“核心”只用在 the core of the operating system 这句解释里。 |
| Docker Desktop / hidden Linux VM / a small, hidden Linux VM / right on the VM's own Linux | Docker Desktop / Linux VM | S02：在 Mac 或 Windows 笔记本上，Docker Desktop 用一台隐藏的小 Linux VM 来提供这个内核。在云上的 VM 里，Docker 直接跑在 VM 自己的 Linux 上。 | unlike Docker Desktop on a Mac → 不像 Mac 上的 Docker Desktop。 |
| operating system / system files / libraries / setup / had to cooperate | 操作系统 / 系统文件 / 库 | S02：在第 1 讲里，每台新 VM 都要重新配置一遍，还得操作系统配合。S02：第 1 讲里 venv 隔离不了的东西，系统文件和库，现在都装进了盒子里。 | 第 1 讲：旁白不把“操作系统”缩写成 OS。the box → 盒子（画面上那个青色的盒子）。 |

### Dockerfile 与指令 / The Dockerfile and its instructions

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| Dockerfile / a file called Dockerfile / capital D, no extension / the recipe | Dockerfile / 配方 | S02：配方就是 Dockerfile，Docker 一次读一条指令。S04：在 simple-translate 目录里建一个叫 Dockerfile 的文件：大写 D，没有扩展名。 | 文件名，也是课程里的叫法。recipe 一律译“配方”（the recipe for this image → 这个 image 的配方；ship the image, not the recipe → 交付 image，而不是配方）。和“参考答案”（solution）分开。 |
| instruction / instructions / one instruction at a time / add a layer / only write on the card | 指令 | S02：会改文件的指令，比如 RUN 和 COPY，会加一层。别的指令，比如 CMD，只写在卡片上。 | Dockerfile 的指令不说“命令”（命令是在终端里输入的）。add a layer → 加一层；only write on the card → 只写在卡片上。 |
| Dockerfile instructions: FROM / ENTRYPOINT / RUN / COPY / CMD / ENV / the FROM line / the COPY line | FROM / ENTRYPOINT / RUN / COPY / CMD / ENV / FROM 那一行 / COPY 那一行 | S06：第 3 步加两条指令。RUN pip install uv 用 base image 自带的 pip 来装 uv。 | 原样，和 Dockerfile 里一样大写。three ENV lines → 三行 ENV。 |
| Step 1 to Step 5 (the README's Dockerfile steps) / Dockerfile step 1 / Step 2 adds one line | 第 1 步 / 第 2 步 / 第 5 步 | S04：Dockerfile 的第 1 步只有一条指令：FROM python:3.12-slim-bookworm。S05：第 2 步加一行：ENTRYPOINT /bin/bash。 | 旁白只给这五步编号（README 也只给这五步编号）。进度条的 step k of N 在画面上保持英文。BuildKit 的步骤是“构建步骤”，绝不说“第 k 步”（A7）。 |
| python:3.12-slim-bookworm / slim / bookworm / the official Python image, on a slim Debian 12 called bookworm | python:3.12-slim-bookworm / slim / bookworm | S04：这是官方的 Python image，基于精简版的 Debian 12，代号 bookworm。 | SAY 读作 FROM python, 3.12, slim bookworm；中文行照屏幕写 image 名，en_display 写 FROM python:3.12-slim-bookworm（D4）。slim → 精简版；bookworm → 代号 bookworm（第 1 讲）。 |
| config card / the card / settings like environment variables / config only / zero bytes | 配置卡片 / 环境变量 / 只是配置 | S02：旁边还有一张小小的配置卡片：放环境变量这类设置，还有要启动哪个程序。 | image 配置的示意图（第 3 讲称之为第 2 讲的“配置卡片”）。The ENV, ENTRYPOINT and CMD rows are zero bytes: config only → ENV、ENTRYPOINT 和 CMD 这几行都是 0 字节：只是配置。 |
| ENTRYPOINT / CMD / the entrypoint / the command (slot) / default arguments / the program to start / null | ENTRYPOINT / CMD / 默认参数 / null | S05：可以把 ENTRYPOINT 想成要启动的程序，把 CMD 想成它的默认参数。S05：ENTRYPOINT 是 bash，CMD 现在是 null。 | the program to start → 要启动的程序。SAY 里小写的 the entrypoint、the command（指配置里的槽位）写成 ENTRYPOINT 和 CMD，和卡片上的方块一致。Setting an entrypoint resets the command you inherited → 一设置 ENTRYPOINT，从 base image 继承来的 CMD 就被清空了。 |
| start-up command line / one command line / join / bash, dash c, then that string / the string / a quoted command | 启动命令行 / 字符串 | S08：在卡片上，ENTRYPOINT 和 CMD 拼成一条命令行：bash、-c，再加上那个字符串。单独的 bash -c 会运行这个字符串，然后退出。 | join → 拼成；CMD holds dash c and one quoted command → CMD 包含 -c 和一条带引号的命令（A6：带方括号和引号的字面形式不写进中文行）。 |
| exec bash / swaps this bash for an interactive one / sources the activate script / interactive | exec bash / 交互式 / activate 脚本 | S08：接着 exec bash 把这个 bash 换成一个交互式的 bash，它保留新的 PATH，还给你一个提示符。 | source 作为命令保留（source 一下，第 1 讲）；the activate script → activate 脚本（第 1 讲）。 |
| solution / Dockerfile.txt / the README points to a solution / copy it over yours with cp | 参考答案 / Dockerfile.txt / cp | S08：README 接着给了一个参考答案：Dockerfile.txt 这个文件。S08：所以最快的办法是一条额外的命令：用 cp 把它复制过来，覆盖你的 Dockerfile。 | solution → 参考答案（第 3 讲把去年的 solution 也译作参考答案）。引用 README 标题 Solution Dockerfile 时保留原文。 |
| ENV lines / no questions from apt / a UTF-8 locale / unbuffered logs / one bigger RUN / update and upgrade / clean up | locale / UTF-8 / 日志不缓冲 / 更新 / 升级 / 清理 | S08：首先是三行 ENV：让 apt 不再提问，用 UTF-8 的 locale，日志不缓冲。S08：其次是一条更大的 RUN：更新并升级 Debian 软件包，做清理，升级 pip，再装 uv。 | locale 是实验课口语（A1 c：区域设置、语言环境、本地化几个译名互相打架）。the order of ENTRYPOINT and CMD doesn't matter → ENTRYPOINT 和 CMD 的顺序无所谓。 |
| docker-shell.sh / docker-build-push.sh / repo helper / commented-out line 12 / builds and runs in one go | docker-shell.sh / docker-build-push.sh / 辅助脚本 / 被注释掉的第 12 行 | S09：这个 repo 里有个辅助脚本 docker-shell.sh，一次就能构建并运行。S13：它就是 docker-shell.sh 里被注释掉的第 12 行。 | 文件名原样。in one go → 一次就。 |

### 构建：上下文、构建器与缓存 / Building: context, builder, cache

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| build / the build / rebuild / builds / build command | 构建 / 重新构建 / 再构建一次 / 构建命令 | S04：接下来是构建命令。S05：暂停一下，再构建一次。S11：再构建一次。 | 同第 3 讲（A3）。docker build 命令照写。字幕里除了命令本身不写 build。why it keeps rebuilding → 为什么老是重新构建。 |
| build step / build steps / the FROM step / the pip step / the apt and pip step / the three steps after it | 构建步骤 / FROM 那一步 / pip 那一步 | S11：Docker 会缓存每一个构建步骤。S11：FROM 重用了 base image，它后面的三步都显示 CACHED：什么都没跑。 | BuildKit 的 [k/4]。绝不说“第 k 步”（A7）。Which of the four steps run again? → 四个构建步骤里，哪几个会重新运行？ |
| build context / the final dot / this folder / parcel / packs the whole folder into one parcel / unpacks | 构建上下文 / 末尾那个点 / 包裹 / 拆开 | S04：末尾那个点就是构建上下文：也就是这个目录，Docker 会把它发给构建器。S06：Docker 把整个目录打成一个包裹，也就是构建上下文，发给构建器。 | Docker 中文文档的译名：构建上下文。包裹是第 2 讲的画面（第 3 讲：第 2 讲的包裹）。末尾那个点用文字说（B3）。 |
| builder / the builder / desktop linux / default / multi-platform builder / buildx | 构建器 / desktop-linux / default / 多平台构建器 / buildx | S04：在 Docker Desktop 上，构建器叫 desktop-linux，不叫 default。S13：第二个办法：docker-build-push.sh 用的是 buildx，也就是 Docker 的多平台构建器。 | SAY 说 desktop linux；中文行和 en_display 写 desktop-linux（D4）。switch back with docker buildx use default → 再用 docker buildx use default 切回来。 |
| compact view / full log / the extra flag for the full log / dash dash progress equals plain | 精简视图 / 完整日志 / --progress | S04：你的终端显示的是精简视图。这里看到的是完整日志；想看完整日志，就加上 --progress 参数，设成 plain。 | A6：--progress=plain 不写进中文行（有 =）。同第 3 讲：精简视图、完整日志。 |
| cache / caches / layer cache / CACHED / DONE / reused / the cache comes back | 缓存 / 层缓存 / CACHED / DONE / 重用 | S05：FROM 那一步显示 CACHED：什么都没下载，也没有加层。S07：先注意：pip 那一步是 CACHED，COPY 却是 DONE：它又跑了一遍，虽然我们只加了一行。 | 旁白指着终端里的 CACHED、DONE 时保留原文。reuses the base → 重用了 base image。Same files, so the cache comes back? → 文件一样，缓存就回来了吗？ |
| checksum / fingerprint / parent step / its instruction is unchanged / the first step that changes / dominoes | 校验和 / 指纹 / 上一步 / 多米诺骨牌 | S11：一个步骤，只要它的上一步和它自己的指令都没变，就会被重用。对 COPY 来说，复制进来的文件的校验和也得一致。第一个变了的步骤会重新运行，它后面的每一步也一样。 | 第 1 讲：校验和。指纹徽章和多米诺骨牌式的连锁反应是画面（第 3 讲称之为第 2 讲的多米诺骨牌）；SAY 里没说 dominoes，字幕也不说。 |
| slow steps first / copy only the files uv sync needs / then copy the rest / reorder the Dockerfile | 慢的步骤放前面 / 调整顺序 | S11：在你自己的项目里，把慢的步骤放前面：先只复制 uv sync 需要的文件，运行它，再复制其余的。 | how would you reorder the Dockerfile → 你会怎么调整 Dockerfile 的顺序。 |
| dockerignore / dot dockerignore / a dockerignore file / the gitignore file / could leave some out / filtered out | .dockerignore / .gitignore / 排除 / 过滤掉 | S06：一个叫 .dockerignore 的文件可以把一些文件排除在外，但这个 repo 里没有。S06：日志也证实了：没有 .dockerignore 文件，所以什么都没被过滤掉。 | 文件名带点（D4：en_display 写 .dockerignore）。add one listing dot git, dot venv and your secrets folder → 加一个，写上 .git、.venv 和你的 secrets 目录。 |
| hidden git folder / dot git / index file / the editor's VS Code folder / git history | .git 目录 / index 文件 / .vscode 目录 / Git 历史 | S06：每个文件都会进去，隐藏的 .git 目录和你的 Dockerfile 也不例外。S11：Git 重写了它自己的 index 文件，就在隐藏的 .git 目录里，而这个目录也在构建上下文里。 | D5：the hidden git folder → 隐藏的 .git 目录；the editor's VS Code folder → 编辑器的 .vscode 目录。index 是 git 自己的文件名（这里不说“索引”或“暂存区”）。 |

### 运行 container / Running a container

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| run / docker run / dash dash rm / dash t i / dash i / dash t / it cleans up afterwards / lets you type into it | docker run / --rm / -ti / -i / -t | S04：现在是运行命令：docker run --rm -ti simple-translate。其中 --rm 负责事后清理；-ti 让你能往里面输入。S09：参数 -i 接上你的键盘，-t 给它一个终端。 | 参数照屏幕写；en_display 写 --rm、-ti（D4）。整条命令放在全角冒号后面（G3）。 |
| exit / type exit / exit with parentheses / exit code 126 / What did exit do? | exit / 退出 / 退出码 | S04：输入带括号的 exit 就能离开。S09：那 exit 做了什么？它结束了 container 的进程，所以 container 停了，然后 --rm 把它删掉了。 | A6：exit() 用文字描述（带括号的 exit）。红色标签写 exit 126；旁白说 exit code 126 → 退出码 126。 |
| prompt / Python prompt / a bare prompt / Read it left to right / the at sign / the container's ID / app in parentheses | 提示符 / Python 提示符 / @ 符号 / container 的 ID | S05：暂停一下，自己跑一遍：只有一个光秃秃的提示符。从左往右读。你是 root，也就是 container 里的管理员。@ 符号后面是 container 的 ID，每次运行都不一样，所以你的会不同。 | 第 1 讲：提示符（不是“提示”）。The prompt now shows app in parentheses → 提示符前面多了带括号的 app（A6）。 |
| the slash / the top folder of the image / working directory / this image sets no working directory | 根目录 / 工作目录 | S05：那个斜杠表示你从 image 的根目录开始，因为这个 image 没有设置工作目录。 | top folder → 根目录（A7：和用户 root 分开）。同第 3 讲：working directory → 工作目录（第 3 讲里的 WORKDIR）。 |
| root / the administrator / you're root / running as root / non-root user | root / 管理员 / 非 root 用户 | S06：另外，pip 还警告说不该用 root 运行。在第 1 讲里这个警告很重要；在这里，image 本身就是隔离。 | 第 1 讲。a non-root user（下节课）→ 一个非 root 用户。 |
| docker ps dash a / lists every container, even stopped ones / Nothing is left / untouched | docker ps -a / 停了的 container / 原封不动 | S09：额外检查 docker ps -a，会列出所有 container，连停了的也算。什么都没剩下；image 原封不动。 | en_display 写 docker ps -a（D4）。 |
| words after the image name / they replace CMD and only CMD / script name / binary / so bash refuses / cannot execute binary file | image 名 / 脚本名 / 二进制文件 / cannot execute binary file | S09：写在 image 名后面的词会替换 CMD，而且只替换 CMD。于是 bash 把 python 当成脚本名，在 /usr/local/bin 里找到了 Python 程序。那是一个二进制文件，所以 bash 拒绝了：cannot execute binary file，退出码 126。 | 报错原文照写。a Python program → Python 程序（A7：程序 ≠ 进程）。 |
| replace CMD with your own dash c string / in one go / translate to French | -c 字符串 / 法语 | S09：想一次就跑完，就像这个额外命令一样，用你自己的 -c 字符串替换 CMD：先激活，再翻译成法语。 | 这条命令本身带引号、&& 和 -d fr：不写进中文行（A6）。 |

### uv、venv 与两个 Python（承接第 1 讲）/ uv, venv and two Pythons (from L1)

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| venv / virtual environment / slash dot venv / dot venv / creates a venv at slash dot venv | venv / 虚拟环境 / /.venv / .venv | S01：这是云上一台全新的虚拟机：没有我们代码的副本，没有虚拟环境，没有 uv。S07：然后它在 /.venv 建了一个 venv，装了 11 个包。 | 第 1 讲 A2：跟着英文走（virtual environment → 虚拟环境，venv → venv）。en_display 写 /.venv、.venv（D4）。 |
| virtual machine / VM / a fresh VM / ac215-l02 | 虚拟机 / VM / ac215-l02 | S01：它只有 Docker，我们只输入一条命令。 | 第 1 讲 A2：virtual machine → 虚拟机，VM → VM；量词“台”。VM 名 ac215-l02 只出现在画面上。 |
| uv / uv sync / pip install uv / the installer / we installed the installer, not the packages | uv / uv sync / pip install uv | S06：我们装了装包的工具，却没装包。S07：第 4 步加上 RUN uv sync；加在末尾，保存。 | 第 1 讲。这里的 the installer 指 uv 本身（一个装包的工具），不是第 1 讲的“安装脚本”。 |
| pyproject.toml / requires-python / line 6 asks for 3.13 or newer / uv.lock / no uv.lock | pyproject.toml / requires-python / uv.lock / 3.13 及以上 | S07：这个 image 的 Python 是 3.12，而 pyproject.toml 第 6 行要求 3.13 及以上。 | 第 1 讲：or newer → 及以上，不写 &gt;=。the repo has no uv.lock, so each build writes its own → 这个 repo 里没有 uv.lock，所以每次构建都会自己写一个。 |
| CPython / downloads its own Python / the newest stable Python it knows in the range / two Pythons | CPython / 最新的稳定版 / 两个 Python | S07：和第 1 讲里那台 Debian 12 的 VM 一样，uv 自己下载了一个 Python：录制时是 CPython 3.15.0。 | Python 不加复数：两个 Python（第 1 讲 A7）。this second Python, in uv's own folder → 这第二个 Python，放在 uv 自己的目录里。 |
| number line / the requirement covers 3.13 and newer / it falls outside / the range / links to it | 数轴 / 范围 / 落在范围外 / 软链接 | S07：在数轴上，这个要求覆盖 3.13 及以上。而 base image 的 3.12 落在范围外，所以 uv 下载了范围内它知道的最新稳定版 Python，venv 里的 python 软链接到它。 | 第 1 讲的数轴和软链接（symlink）。 |
| activation is just PATH / activate / activating the venv / puts its bin folder in front / the word python first finds | 激活 / PATH / bin 目录 | S07：回想一下第 1 讲：激活其实只是改 PATH。没有任何东西激活这个 venv，所以 python 这个词先找到的是 /usr/local/bin 里的 Python，来自 base image。 | 第 1 讲。user local bin → /usr/local/bin（D4）。 |
| user local bin / /usr/local/bin / the PATH that puts user local bin first | /usr/local/bin | S10：它们下面是 base image 自己的几行：最底下是 Debian bookworm，然后是把 /usr/local/bin 放在最前面的 PATH，还有 Python 3.12.15。 | SAY 说 user local bin；中文行写路径（第 1 讲：绝不译“用户本地”）。 |
| which python / python --version / the venv's own python / points into dot venv / the virtual env variable is set | which python / python --version / virtual env 这个变量 | S08：这几个额外检查说是：which python 指向 .venv 里面，版本是 3.15.0，virtual env 这个变量也设置好了。 | A6：VIRTUAL_ENV 写成 virtual env 这个变量；en_display 写 VIRTUAL_ENV。 |
| isolate / isolation / the image itself is the isolation | 隔离 | S06：在这里，image 本身就是隔离。 | 第 1 讲。 |
| pinned / nothing in the recipe is pinned / the Python range is open / an image freezes all that / ship the image, not the recipe | pin 住 / 冻结 / 交付 | S15：配方里什么都没 pin 住：pip 装的是最新的 uv，Python 的范围没有上限，这个 repo 里也没有 uv.lock，所以每次构建都会自己写一个。一个 image 会把这一切都冻结下来：要交付 image，而不是配方。 | 第 1 讲保留了 pin（pin 住）。ship → 交付。 |

### 应用 / The app

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| the app / cli.py / python cli.py / its default text / I love cheese / I love brie / Good morning | 应用 / cli.py / python cli.py / I love cheese / I love brie / Good morning | S01：我们在里面运行这个应用，它的默认文本 I love cheese 翻成了意大利语。S11：作为额外的一步，试试看：把第 49 行的 I love cheese 改成 I love brie。 | 程序的真实输入照写（第 1 讲）。外语输出只在画面上，字幕不写（comes back in Spanish → 翻成了西班牙语）。 |
| English / Italian / Spanish / French / translation / the README's translation | 英语 / 意大利语 / 西班牙语 / 法语 / 翻译 | S09：在提示符后面，输入 README 里的翻译：Good morning，从英语翻成西班牙语。 | 第 1 讲。README 里那条带引号和参数的命令不写（A6）。 |
| request / your laptop's network / Google refused the request / runtime error / try it later | 请求 / 网络 / 运行时错误 | S09：如果你的最后报了运行时错误，那是 Google 拒绝了请求：过一会儿再试；Docker 没问题。 | 第 1 讲：请求、网络。这个报错只是说出来、没有打印（没有录屏），所以翻译。 |
| raise exception equals True / the older cli.py / quietly prints your input back | 旧版的 cli.py / 原样打出来 | S15：额外检查一下还会发现，发布出来的 image 比 repo 落后：它的 cli.py 是旧版，没有把 raise exception 设为 True。 | A6：raise_exception=True 用文字描述；en_display 写 raise_exception=True。If Google refuses a request, that version quietly prints your input back → 如果 Google 拒绝请求，那一版会悄悄把你的输入原样打出来。 |

### 终端原文与报错 / Terminal text and errors

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| failed to read dockerfile / ModuleNotFoundError / no module named art / exec format error / no matching manifest | failed to read dockerfile / ModuleNotFoundError / No module named art / exec format error / no matching manifest | S03：作为额外的一步，现在就跑一下 README 里的构建命令：报 failed to read dockerfile。S06：然后是 python cli.py，又一个额外检查：报 ModuleNotFoundError，No module named art。 | 终端原文照写，前面加“报 / 显示”（第 1 讲）。no module named art：去掉屏幕上的引号（A6）；en_display 保留。 |
| push access denied / permission denied / toomanyrequests / too many requests / Unable to locate package / Not Found errors | push access denied / permission denied / toomanyrequests / Unable to locate package / Not Found | S14：在我们的替身里，也就是一个软件包列表为空的全新 Debian，它失败了：Unable to locate package。S15：如果连 pull 本身都失败了，报 toomanyrequests：Docker Hub 按网络地址限制匿名 pull 的次数，一整个教室的人可能会碰到。 | SAY 说 too many requests、unable to locate package；中文行写屏幕原文（D4）。out of date, with Not Found errors → 已经过期，会报 Not Found。 |
| nothing to commit / git status / the gitignore file lists Dockerfile on line 3 / so git hides yours / git add dash f | nothing to commit / git status / git add -f / 忽略 | S04：有个意外：额外用 git status 看一下，显示 nothing to commit，可我们刚建了一个文件。这里的 .gitignore 文件第 3 行写着 Dockerfile，所以 git 把你的忽略了。想照样 commit 它，就用 git add -f。 | 第 1 讲：commit 保留。hides → 忽略（git 自己的说法）。 |
| git diff / git checkout / undo the edit / the build context now has a different checksum | git diff / git checkout / 撤销修改 | S11：用 git diff 能看到这处改动；现在构建上下文的校验和不一样了。S11：现在用 git checkout 撤销修改。 | 命令原样。 |
| diff / dash u / less-than and greater-than signs / an extra diff shows what it adds | diff / diff -u / 小于号和大于号 | S08：额外用 diff 看一下它多了什么；如果你的输出是小于号和大于号，就加上 -u。 | B3：&lt; 和 &gt; 用文字说。 |
| warning / warns / insecure / a password on the command line | 警告 / 不安全 / 密码 | S12：登录它时会警告：在命令行里写密码不安全。 | 终端里的 WARNING 行由 SAY 转述，所以翻译。 |

### 清理与 docker 命令 / Cleanup and docker commands

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| docker container ls / it lists running containers / only the header / the Docker daemon / so start Docker Desktop | docker container ls / 表头 / Docker daemon | S03：首先，docker container ls 列出正在运行的 container。这里只显示了表头，所以什么都没在运行。如果你的连不上 Docker daemon，就启动 Docker Desktop 再试。 | Docker daemon 是实验课口语，也是报错原文里的词（Cannot connect to the Docker daemon）；只在文档里写“守护进程（daemon）”。 |
| docker stop / stop any running container / with its ID | docker stop / ID | S03：接着，停掉所有正在运行的 container。这里没有要停的；如果你有，docker stop 加上它的 ID 就行。 | ID 保留（口语）。 |
| docker system prune / dash a / dangling images / the ones without a name / named images / unused image / reclaim | docker system prune / dangling images / 没有名字的 image / 没在用的 image / 回收空间 | S03：看第三项：dangling images，也就是没有名字的 image。S03：加上 -a 的话，prune 会删掉所有没在用的 image。 | dangling images 是 prune 警告的原文（文档里写“虚悬镜像”，H3）。Despite the README's heading → 虽然 README 的标题这么写。Nothing to reclaim here → 这里没有空间可回收。 |
| docker image ls / on disk / content / compressed / the unpacked copy / your columns may differ | docker image ls / 磁盘占用 / 内容大小 / 压缩后 / 解压后 | S10：首先是 docker image ls：录制时，磁盘占用 518 MB，内容大小 144 MB。内容就是压缩后的那些层，也就是传到 registry 的部分；磁盘占用还要加上解压后的那一份。 | 画面上的列名是 DISK USAGE 和 CONTENT SIZE（A7）。Your columns may differ → 你的列可能不一样。 |
| hello-world / Tutorial 0 / it has a name, so it survived | hello-world / Tutorial 0 | S03：你的可能还会显示 hello-world：它有名字，所以留了下来。 | 名字原样。 |
| docker image inspect / reads the config card / predict a Python prompt | docker image inspect | S04：所以我们预测会出现 Python 提示符。 | An extra docker image inspect → 额外用 docker image inspect。 |
| docker history / newest first / read it bottom-up / top-down | docker history / 从下往上 / 从上往下 | S10：然后 docker history 列出各层，最新的在最上面。从下往上读，就是从上往下读 Dockerfile。 | the apt and pip step at 97.5 megabytes, our code at 250 kilobytes → apt 和 pip 那一步 97.5 MB，我们的代码 250 KB（C2）。 |
| ls / ls dash a / cat / cd / git clone / clone it here / cd into simple-translate | ls / ls -a / cat / cd / git clone | S03：在这里 clone，然后 cd 进 simple-translate。暂停一下，两条都跑一遍。S03：额外检查一下，README 里没有这一步：ls -a。 | 第 1 讲。look around with ls → 用 ls 四处看看。 |

### Docker Hub、tag 与 push / Docker Hub, tags and pushing

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| Docker Hub / account / a free Docker Hub account / sign up / user name | Docker Hub / 账号 / 免费的 Docker Hub 账号 / 注册 / 用户名 | S01：你需要运行着的 Docker Desktop、一个免费的 Docker Hub 账号，还有你的 Google Cloud 项目，最后开 VM 要用。 | 不写“帐号”“使用者名称”。 |
| access token / your token / read and write access / not the default / shown only once / works like a password | 访问令牌 / 令牌 / 读写权限 | S12：首先，注册，再建一个访问令牌，权限选读写，不要用默认的。马上复制：它只显示一次，作用和密码一样。 | 同第 3 讲（字幕不写 token）。介绍过之后可以简称“令牌”（your token → 你的令牌；check your token can write → 检查你的令牌有写权限）。 |
| docker login / dash u / dash p / log in / logging in / your token stays in your shell history / paste the token when it asks | docker login / -u / -p / 登录 / shell 历史记录 | S12：这是 README 的一个小疏漏：用 -p 的话，你的令牌会留在 shell 历史记录里。改成输入 docker login、-u 和你的用户名，等它问的时候再粘贴令牌。 | A6：README 这一行有 &lt;USER NAME&gt; 和 &lt;ACCESS TOKEN&gt;，用文字描述（docker login，-u 加你的用户名，-p 加你的令牌）。We have no account, so we couldn't run it → 我们没有账号，所以没法跑。 |
| stand-in / a small registry on our own machine / just watch those / on the stand-in | 替身 / 只看就好 | S12：所以有些步骤用了替身，也就是我们自己机器上的一个小 registry：那些只看就好。 | 同第 3 讲（替身）。画面标签 stand-in · local registry, not Docker Hub 保持英文（A11）。 |
| docker tag / your user name, slash simple-translate-ac215 / two names, one ID / a second name, not a copy | docker tag / 你的用户名/simple-translate-ac215 / 两个名字，一个 ID | S12：然后给 image 打 tag：docker tag，先写 simple-translate，再写你的用户名/simple-translate-ac215。S12：额外用 docker image ls 看一下：两个名字，一个 ID；是第二个名字，不是一份副本。 | A6、G3：README 这一行用文字描述；en_display 保留 SAY 的 your user name。 |
| the long name in four parts / the registry, docker dot I-O, the default / your account / the repository / the tag / library | docker.io / 仓库 / library | S12：把这个长名字分成四段来读：registry，也就是默认的 docker.io；你的账号；仓库；还有 tag，latest。没有账号部分的名字，比如我们的第一个名字，都归在 library 下面。 | docker dot I-O → docker.io（D4）。the repository → 仓库（Docker Hub 上的 repository；A7）。 |
| docker push / push / upload each layer / a digest line / only missing layers travel / mounted from library python | docker push / push / 上传每一层 / digest / Mounted from library/python | S12：你的应该会上传每一层，最后一行是 digest。S12：在 Docker Hub 上，连 base image 的那几层也可能显示 Mounted from library/python：它本来就有这些层。 | push 保留（书面“推送”）。digest 是打印出来的词：a fingerprint of the whole image → 整个 image 的指纹。 |
| Docker Hub repository / public by default / private / anyone can pull it, git folder and all | Docker Hub 仓库 / 公开 / 私有 | S12：还要记住：新建的 Docker Hub 仓库默认是公开的。谁都能 pull 它，连 .git 目录一起。 | make it private → 设成私有。 |
| pull / pulls it from Docker Hub / anonymous pulls / the pull itself fails | pull / 匿名 pull / 拉取（书面） | S15：这台 VM 上还没有这个 image，所以 Docker 从 Docker Hub 把它 pull 下来，一共 7 层，然后启动一个 container。 | 和 push 一样是实验课口语。Docker downloads an image（S01）→ 下载（那里英文说的是 download）。 |

### 平台 / Platforms

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| platform / platforms / linux slash amd64 / amd64 / arm64 / Intel or AMD / Apple Silicon / M-series Mac | 平台 / linux/amd64 / amd64 / arm64 / Apple Silicon / M 系列 Mac | S13：我们的机器是 Intel 或 AMD 的，image 上写的是 linux/amd64。在 Apple Silicon 的 Mac 上，你会看到 arm64。 | 平台名原样；en_display 写 linux/amd64（D4）。an ordinary Intel or AMD machine → 一台普通的 Intel 或 AMD 机器。 |
| machine code / CPU / emulator / unless an emulator steps in / emulated / slower, but it works / the CPU must speak the image's language | 机器码 / CPU / 模拟器 / 模拟运行 | S13：一个 image 里的每个程序，bash、Python、uv，都是给某一种 CPU 用的机器码。S13：在 Mac 上，它是模拟运行的：慢一些，但能用。 | the CPU must speak the image's language → CPU 得会说这个 image 的语言。Docker Desktop has one built in → Docker Desktop 自带一个。 |
| menu / a tag can point at a menu / one image per platform / row / two kinds of arm / no menu | 菜单 / 每个平台一个 image | S13：一个 tag 可以指向一份菜单，每个平台一个 image。这个 python tag 列了五个平台：amd64、两种 arm，还有两种比较少见的。 | 多平台索引的示意（文档里叫“清单列表”，manifest list，H3）。Docker pulls the row that matches your machine → Docker 会 pull 和你的机器对得上的那一行。 |
| attestation / a record of how the image was built | attestation | S13：我们在替身上 push 的是一份小菜单：amd64，外加一个 attestation，也就是记录这个 image 是怎么构建出来的。 | 保留英文（A1 c）：Docker 自己的词，输出里就有（attestation manifest）；“证明”容易读成 proof。文档可以写“构建证明（attestation）”。 |
| the two fixes / build for the VM's platform / dash dash platform equals linux slash amd64 / build both and push one menu / multi-platform | 两个办法 / 多平台 / --platform | S13：有两个办法，README 里都没有。第一：为 VM 的平台构建，加上 --platform 参数，设成 linux/amd64。S13：第二：docker-build-push.sh 用 buildx 把两个平台都构建出来，再 push 一份菜单。 | A6：--platform=linux/amd64 不写（有 =）。Two fixes, neither in the README → 有两个办法，README 里都没有。 |

### VM 部分 / The VM part

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| create a VM / E2 machine / Debian 12 or 13 / the README gives no settings / E2 machines are amd64 | E2 机器 / Debian 12 / Debian 13 | S14：README 没给任何配置。一台普通的 E2 机器，装 Debian 12 或 13 就行；E2 机器都是 amd64。 | 第 1 讲：machine type → 机器类型；E2 保留。bookworm 是 Debian 12 的代号（旁白只说了这一个）。 |
| the meter starts / bills by the second while it runs / its disk while it exists / it costs money | 计价器 / 按秒计费 / 磁盘 | S14：计价器开始跳了：VM 运行时按秒计费，它的磁盘只要还在就计费。 | 第 1 讲：计价器、计费、磁盘。 |
| SSH in / SSH terminal / wait until its SSH terminal is open | SSH 进去 / SSH 终端 | S14：接着，SSH 进去。现在暂停：创建你的 VM，等到它的 SSH 终端打开。 | 第 1 讲。 |
| sudo apt install docker dot I-O / docker.io / Debian's own Docker package / older than the laptop's, but plenty | sudo apt install docker.io / docker.io | S14：然后安装 Docker：sudo apt install docker.io。S14：这是 Debian 自己打包的 Docker：录制时 Debian 12 上是 20.10.24，Debian 13 上是 26.1.5。比笔记本上的旧，但够用了。 | docker dot I-O → docker.io（D4）。Debian's own Docker package → Debian 自己打包的 Docker（第 1 讲：Debian 自己打包的 pip）。 |
| sudo apt-get update / package lists / empty / out of date / 92 new packages / a 107 megabyte download / Answer Y | sudo apt-get update / 软件包列表 / 软件包 / 输入 Y | S14：README 的一个小缺口：这一节跳过了第 1 讲用过的 sudo apt-get update。S14：现在安装成功了：在 Debian 12 上是 92 个新软件包，下载 107 MB。 | 第 1 讲：apt 管的是软件包，它的目录叫软件包列表。Run the update first, an extra, and pause after it → 先跑 update，这是额外的一步，跑完先暂停。 |
| sudo docker dash dash version / sudo / and why sudo / the Docker socket / the door to Docker's background service / the docker group | sudo docker --version / sudo / Docker socket / 后台服务 / 门 / docker 组 | S14：不加 sudo 的话，这个额外的 docker ps 会被拒绝：Docker socket 上 permission denied，socket 就是通往 Docker 后台服务的那扇门。只有 root 和 docker 组能打开它。 | socket 是实验课口语（“套接字”是教科书用语，A1 c）。en_display 写 sudo docker --version（D4）。 |
| deploy / the deploy / sudo docker run dash dash rm dash t i dlops slash simple-translate / one-command deploy | 部署 / sudo docker run --rm -ti dlops/simple-translate | S15：然后是部署：sudo docker run --rm -ti dlops/simple-translate。暂停一下，自己跑一遍。 | 中文行里写出来的最长命令（约 26 个单位）：单独放在冒号后面（G3）。 |
| the instructor's image / dlops slash simple-translate / is no menu / the published image lags the repo / built on September 16 | 授课老师的 image / dlops/simple-translate / 发布出来的 image | S13：授课老师的 image，dlops/simple-translate，不是菜单：只有一个 image，只有 amd64。S15：这个 image 是 9 月 16 日用 uv 0.12.15 构建的，范围内 uv 当时知道的最新稳定版 Python 是 3.14.7。 | A10：绝不写授课老师的名字。lags → 比 repo 落后。 |
| delete the VM / with its boot disk / VM instances / Disks / both are empty | 删除 / 启动磁盘 / VM instances / Disks | S16：README 的最后一步：删除 VM，连同它的启动磁盘，然后确认 VM instances 和 Disks 两个页面都是空的。现在就暂停去做。 | 第 1 讲：控制台页面用英文名（VM instances 页面、Disks 页面），启动磁盘。 |
| clean up / the optional chores / reclaim the space your images take / docker system prune dash a / thanks to dash dash rm | 清理 / 杂事 / docker system prune -a | S16：走之前，先清理一下。额外检查 docker ps -a，没有留下任何 container，多亏了 --rm。 | en_display 写 docker system prune -a（D4）。 |

### 梯子、回顾、固定句式与课程 / Ladder, recap, fixed patterns and the course

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| the ladder / rungs / the first two rungs / today, the other two / package the app as a Docker image | 梯子 / 一级 / 前两级 | S01：今天的教程 simple-translate 到这里就结束了。上节课我们爬了它的前两级：先在 VM 上手动安装，再用 uv。 | 第 1 讲的梯子（梯子、一级、前两级）。 |
| a container slid in between / the venv now lives in an image / you built it, pushed it to a registry, and ran it | 插到了中间 | S16：第 1 讲给了我们一台装着 venv 的 VM。今天，container 插到了中间：venv 现在住在一个 image 里，就在 /.venv。 | 结尾的画面（V1）。 |
| the tracker / the three trackers at top left / code panels / study guide / exercises | 进度条 / 代码面板 / 学习指南 / 练习 | S01：想跟着做的话，把 README 打开，放在视频旁边。左上角的三个进度条显示我们在哪儿：在笔记本上，在 Docker Hub 上，还是在 VM 上。 | 第 1 讲。on the laptop → 在笔记本上（第 1 讲：笔记本电脑，口语说笔记本）。 |
| your turn / the yellow your-turn tag / extra / a gray extra tag / extras | your turn 标签 / extra 标签 / 额外检查 | S01：看到黄色的 your turn 标签，就暂停，自己跑这条命令；灰色的 extra 标签表示这个检查 README 里没有。 | A11，同第 3 讲：标签名照画面写（第 1 讲写“轮到你了”“额外”，是因为当时计划翻译画面标签）。旁白自己说的 an extra → 额外检查 / 额外的一步。 |
| at the time of recording | 录制时 | S03：你的列可能不一样：这是录制时的 Docker 29。 | 绝不省略（A9）。 |
| a small slip / a small gap / a small mismatch / a small mistake | 小疏漏 / 小缺口 / 不一致 / 小错误 | S02：README 里有一个小疏漏：它说要构建 docker container。构建得到的是 image；运行得到的才是 container。 | a small mismatch → 一个小小的不一致。同第 3 讲；后面一定跟改法（A9）。SAY 引用的 README 原话，围绕其中的实物翻译（it says build the docker container → 它说要构建 docker container）；英文行里是原话。 |
| Something to ponder / Now predict / Now a puzzle / Now ponder / Now the answer / Hold that thought / the opening question | 来想一个问题 / 先预测一下 / 先出个小题 / 来想一想 / 揭晓答案 / 开头那个问题 | S06：来想一个问题：uv 装好了，代码也进了 image。那 python cli.py 能跑起来吗？ | D6。“暂停想一想”卡片在画面上保持英文（A11）。 |
| Five questions to test yourself / One / Five / The answers are in the exercises / every command is in the study guide | 五道自测题 / 第一题 / 第五题 / 答案在练习里 | S16：五道自测题。第一题：image 和 container 有什么区别，--rm 又删掉了什么？ | D6。回顾题保留问号；一句英文里有几个问题时，在一个中文句子里用逗号连起来（D1：句中不出现？）。 |
| Containers 2 (next lecture) / five containers working together / a working directory / a non-root user / your laptop's folder mounted inside a container | 下节课 / 容器 II / 协同工作 / 挂载 | S16：下节课是容器 II：五个 container 协同工作，一个工作目录，一个非 root 用户，还有把你笔记本上的目录挂载进 container。 | 第 3 讲的标题是“容器 II”；mount → 挂载（第 3 讲）。 |
| AC215 / lecture 1 / last lecture / today / part 1 / part 2 / Tutorial 0 / the instructor / MLOps Learning | AC215 / 第 1 讲 / 上节课 / 今天 / 第一部分 / 第二部分 / Tutorial 0 / 授课老师 / MLOps Learning | S09：在第二部分：image 里有什么，为什么老是重新构建，以及怎么把它送到 VM 上。 | A10。 |
| README / the README section / the README's heading / the README's headings: Developing App using Containers / Build Docker Image / Run Docker Container / Pushing Docker Image to Docker Hub / Running App on VM using Docker | README / Developing App using Containers / Build Docker Image / Run Docker Container / Pushing Docker Image to Docker Hub / Running App on VM using Docker | S03：现在进入 README 的 Developing App using Containers 这一节。S14：README 的最后一节：Running App on VM using Docker。 | 章节标题照写（观众要在 README 里找它）；the section → 这一节；the step → 这一步。 |
| products: Docker / Google / Google Cloud / Debian / Python / Git / Git Bash / VS Code / Mac / Windows / Linux / GitHub | Docker / Google / Google Cloud / Debian / Python / Git / Git Bash / VS Code / Mac / Windows / Linux | S03：在 Mac 上，你的提示符会不一样；在 Windows 上，用 Git Bash。 | 拉丁字母（A1 b）。your Google Cloud project → 你的 Google Cloud 项目（第 1 讲）。 |
| service account / keys / Google Cloud project | 服务账号 / 密钥 / 项目 | S01：今天不需要服务账号，也不需要密钥。 | 第 1 讲。 |
| simple-translate / simple-translate-ac215 / student / app / dlops | simple-translate / simple-translate-ac215 / student / app / dlops | S04：参数 -t 给 image 起名叫 simple-translate；-f 指定配方。 | 名字原样（A10）。 |
| sizes: 50 megabytes / 63 kilobytes / 518 megabytes / 144 megabytes / 97.5 megabytes / 250 kilobytes / 125 megabytes / 107 megabytes / 118 megabytes / zero bytes | 50 MB / 63 KB / 518 MB / 144 MB / 97.5 MB / 250 KB / 125 MB / 107 MB / 118 MB / 0 字节 | S04：Docker 下载了 base image：4 层，压缩后不到 50 MB，然后把结果存为 simple-translate，tag 是 latest。 | C2。 |
| versions: 3.12 / 3.12.15 / 3.13 / 3.14.7 / 3.15.0 / 0.13.0 / 0.12.15 / Docker 29 / 20.10.24 / 26.1.5 | 3.12 / 3.12.15 / 3.13 / 3.14.7 / 3.15.0 / 0.13.0 / 0.12.15 / Docker 29 / 20.10.24 / 26.1.5 | S01：额外检查一下，README 里没有这一步：这是哪个 Python？是 3.14.7。可这个 image 的配方是从 Python 3.12 开始的。先记住这个问题；今天我们会两次解开它。 | C2；at the time of recording → 录制时（A9）。 |
| line 3 / line 6 / line 7 / line 11 / line 12 / line 49 / Step 3 / process number 1 / exit code 126 | 第 3 行 / 第 6 行 / 第 49 行 / 第 3 步 / 退出码 126 | S13：在第 11 行填你的用户名，在第 7 行填 simple-translate-ac215，也就是 README 里的名字。先登录，再用 bash 运行它。 | C1。 |

### 标题与配套材料（meta.yaml、文档）/ Titles and companions

| English | 字幕写法 | 首次出现（例句） | 说明 |
|---|---|---|---|
| Video title | AC215 · 第 2 讲：容器 I——一个镜像，从笔记本到 VM（跟练：simple-translate） |  | H1；和第 1、3 讲同一个格式。跟练 = follow-along。 |
| the part titles: write a Dockerfile, build and run the image / layers, cache, Docker Hub and a VM | AC215 · 第 2 讲（上）：写 Dockerfile，构建并运行镜像 / AC215 · 第 2 讲（下）：层、缓存、Docker Hub 与 VM |  | H1。 |
| Chapters S01-S08: One command on a fresh VM / Image, layer, container, registry / A clean slate, and the clone / Dockerfile step 1: FROM / Step 2: ENTRYPOINT / Step 3: install uv, copy the code / Step 4: uv sync, and two Pythons / Step 5: CMD, the solution, the build | 全新 VM 上的一条命令 / 镜像、层、容器与镜像仓库（registry） / 清理干净，克隆仓库 / Dockerfile 第 1 步：FROM / 第 2 步：ENTRYPOINT / 第 3 步：安装 uv，复制代码 / 第 4 步：uv sync 与两个 Python / 第 5 步：CMD、参考答案与构建 |  | H1，书面语体；核心概念章节附 registry，方便搜索。 |
| Chapters S09-S16: Run it, translate, exit / What's inside the image / The layer cache / Tag and push / Platforms: arm64 vs amd64 / A VM with only Docker / One-command deploy / Tear down, recap, and what's next | 运行、翻译、退出 / 镜像里有什么 / 层缓存 / 打标签并推送 / 平台：arm64 与 amd64 / 只装了 Docker 的 VM / 一条命令完成部署 / 收尾、回顾和下节预告 |  | H1；S16 和第 1 讲的英文标题相同，沿用第 1 讲的中文。 |
| written register for the companions: container / image / base image / layer / writable layer / build context / layer cache / registry / repository / tag / push / pull / access token / daemon / socket / dangling image / manifest list / attestation | 容器 / 镜像 / 基础镜像 / 镜像层 / 可写层 / 构建上下文 / 层缓存 / 镜像仓库 / 仓库 / 标签 / 推送 / 拉取 / 访问令牌 / 守护进程 / 套接字 / 虚悬镜像 / 清单列表 / 构建证明 |  | H3、A4。只用于配套文档（README.md、exercises.md、digest.md），不进字幕。 |
| headings of exercises.md / &lt;summary&gt;Answer&lt;/summary&gt; | A 部分 / B 部分 / C 部分 / D 部分 / 答案 |  | 同第 1 讲（A 部分 · 视频最后的五道题 / B 部分 · 动手（先预测，再运行）/ C 部分 · 排错 / D 部分 · 思考）。 |

## 规则

规则编号和 `glossary.yaml` 一一对应（A 术语、B 排版、C 数字、D 旁白文件、G 字幕、H 标题与配套材料、I 工具链）。第 1 讲的 E（屏幕文字）和 F（语音）两组在这个系列里不适用：画面不翻译，也没有配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（docker container ls、docker stop、docker system prune、docker system prune -a、docker image ls、git clone、cd、ls、ls -a、cat、docker build、docker run、docker image inspect、git status、git add -f、git diff、git checkout、diff、diff -u、cp、python cli.py、python --version、which python、source、exec bash、bash -c、echo $$、exit、docker ps -a、docker history、docker login、docker tag、docker push、docker buildx use default、sudo apt install docker.io、sudo apt-get update、sudo docker --version、sudo docker run --rm -ti dlops/simple-translate、sudo docker login、pip install uv、uv sync）、参数（--rm、-t、-i、-ti、-f、-a、-u、-p、-c、--progress、--platform、--version）、文件和目录名（Dockerfile、Dockerfile.txt、.dockerignore、.gitignore、.git、.vscode、.venv、/.venv、.venv/bin/activate、cli.py、pyproject.toml、uv.lock、docker-shell.sh、docker-build-push.sh、README、/usr/local/bin、/bin/bash）、image / tag / 包名（python:3.12-slim-bookworm、simple-translate、simple-translate-ac215、dlops/simple-translate、hello-world、latest、library、docker.io、uv、pip、art）、Dockerfile 指令和配置字段（FROM、RUN、COPY、ENV、ENTRYPOINT、CMD、null、requires-python）、平台名（linux/amd64、amd64、arm64）、构建器名（default、desktop-linux）、终端原文和报错（CACHED、DONE、failed to read dockerfile、nothing to commit、ModuleNotFoundError、No module named art、cannot execute binary file、push access denied、Mounted from library/python、exec format error、no matching manifest、Unable to locate package、Not Found、permission denied、toomanyrequests、dangling images、digest）、旁白提到的画面标签（your turn、extra；A11）、README 的章节标题（Developing App using Containers、Build Docker Image、Run Docker Container、Pushing Docker Image to Docker Hub、Running App on VM using Docker）。例外是 check 不允许的实物（A6）。（b）**产品、组织、课程和名字**：Docker、Docker Desktop、Docker Hub、Google、Google Cloud、Debian、bookworm、Python、CPython、Git、Git Bash、VS Code、Mac、Windows、Linux、Intel、AMD、Apple Silicon、CPU、E2、SSH、UTF-8、AC215、Tutorial 0、MLOps Learning、simple-translate、dlops、student、app。（c）**封闭清单**，中国 MLOps 工程师在实验课上本来就说英文的词：第 1 讲的 VM、venv、shell、root、repo、clone、commit、pin；容器这几讲新增（和第 3 讲同一份）container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、digest、socket、Docker daemon、attestation、locale、ID。新词要进（c），必须同时满足：实验课上真的说英文；中文生硬、有歧义或和别的术语撞车（“镜像”也指 mirror；“套接字”“守护进程”是教科书用语；“证明”会读成 proof；locale 有“区域设置 / 语言环境 / 本地化”几个译名互相打架）。绝不为了“味道”说英文：不说 layer、build、builder、cache、build context、kernel、process、platform、emulator、menu、token、password、account、user name、folder、terminal、package、prompt、flag、deploy。
- **[A2]** container 和 image。字幕里说 container 和 image，和助教在实验课上一样：起一个 container、构建 image、image 里、container 停了；量词“个”（一个 container、两个 image、两个名字一个 ID）。标题、章节名、meta.yaml、配套文档写“容器”“镜像”（A4），和第 1 讲预告里的写法、Docker 中文文档一致。字幕里不写“镜像”（它也是 Debian mirror 的日常说法，第 1 讲叫“软件源”）。image name → image 名；the image's top folder → image 的根目录；the official Python image → 官方的 Python image；a Docker image → 一个 Docker image；base image 照说 base image（也是画面上的标签），书面写“基础镜像”。第 1 讲预告下节课时写的是“容器 / 镜像”；从第 2 讲起字幕中英混说（和第 3 讲一样）。
- **[A3]** 其余 Docker 概念用中文。build → 构建（构建 image、再构建一次、这次构建）；rebuild → 重新构建；build step（BuildKit 的 [k/4]）→ 构建步骤（Docker 会缓存每一个构建步骤；四个构建步骤；FROM 那一步 / pip 那一步 / apt 和 pip 那一步）；build context → 构建上下文；builder → 构建器（multi-platform builder → 多平台构建器；构建器的名字 default、desktop-linux 照写）；layer → 层（一层、7 层、加一层、两个新层）；read-only layer → 只读层；writable layer → 可写层（一层薄薄的可写层）；cache → 缓存（layer cache → 层缓存；reused → 重用；缓存回来了）；终端里的 CACHED、DONE 照写；compact view → 精简视图；full log → 完整日志；instruction → 指令（RUN 指令、一次读一条指令）；config card → 配置卡片（只写在卡片上；只是配置）；start-up command line → 启动命令行；default arguments → 默认参数；the program to start → 要启动的程序；process → 进程，main process → 主进程，process number 1 → 1 号进程；kernel → 内核；platform → 平台；machine code → 机器码；emulator → 模拟器，emulated → 模拟运行；run → 运行 / 跑；start a container → 启动 container / 起一个 container；exit → 退出（命令 exit 照写）；stop → 停止 / 停了；delete → 删除 / 删掉；deploy → 部署；push / pull 照说（书面推送 / 拉取）；download → 下载（Docker 下载了一个 image；uv 自己下载一个 Python）；upload each layer → 上传每一层；tag（动词）→ 打 tag（给 image 打 tag）；log in → 登录；sign up → 注册。
- **[A4]** 书面与口头配对。字幕说 repo / clone / commit / container / image / base image / registry / tag / push / pull；标题、章节名、meta.yaml、配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 基础镜像 / 镜像仓库 / 标签 / 推送 / 拉取。the repo 作主语说“这个 repo”。命令本身不受影响（git clone、docker push、docker tag 照写）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符都不变）；不翻译，不变形，不加引号、书名号或代码格式。需要时后面接一个中文名词：docker build 这条命令、Dockerfile.txt 这个文件、.dockerignore 文件、.git 目录、/usr/local/bin 目录、--rm 参数、RUN 指令、FROM 那一行、simple-translate 这个 image、desktop-linux 这个构建器。句首不放小写的实物或口语英文词（image、container、registry、tag、repo、pip、bash、exit、git diff、docker-build-push.sh、-t、--rm）：前面加一个中文词（一个 image 就是……；而 container……；像 Docker Hub 这样的 registry……；所谓 tag……；这个 repo……；输入 docker build……；用 git diff……；参数 -t……；那 exit 做了什么？），字幕就不会以小写字母开头。大写开头的名字、产品和指令可以放在句首（Docker、README、Dockerfile、Git、VM、FROM、ENTRYPOINT、CMD、RUN），和英文一样。SAY 把屏幕上的完整命令说短了时（an extra image ls），照屏幕写（docker image ls）。
- **[A6]** check 不允许的实物。没有 say: 时，check 把显示行当成朗读文本检查，不允许 letter_letter 形式的名字、= < > + 和任何括号。所以这些实物不抄进中文行，按旁白的说法用文字描述，英文行用 en_display 给出字面形式（D4）。对照：VIRTUAL_ENV（the virtual env variable）→ virtual env 这个变量；raise_exception=True（raise exception equals True）→ 把 raise exception 设为 True；--progress=plain → --progress 参数设成 plain；--platform=linux/amd64 → --platform 参数设成 linux/amd64；README 的占位符 `<USER NAME>` → 你的用户名，所以 `<USER NAME>/simple-translate-ac215` → 你的用户名/simple-translate-ac215，`docker login -u <USER NAME> -p <ACCESS TOKEN>` → docker login，-u 加你的用户名，-p 加你的令牌；exit()（exit with parentheses）→ 带括号的 exit；提示符里的 (app)（app in parentheses）→ 带括号的 app；`No module named 'art'` → No module named art（引号还会粘在单词上）；`ENTRYPOINT ["/bin/bash"]` → ENTRYPOINT /bin/bash；`CMD ["-c", "source .venv/bin/activate && exec bash"]` → CMD 包含 -c 和一条带引号的命令（SAY 也是这么描述的）；README 的翻译命令 `python cli.py -t "Good morning" -s "en" -d "es"` → 输入 README 里的翻译：Good morning，从英语翻成西班牙语；`docker run --rm simple-translate -c "source .venv/bin/activate && python cli.py -d fr"` → 不写，SAY 只说“你自己的 -c 字符串”；less-than and greater-than signs → 小于号和大于号。等工具链允许显示行保留这些字符（I1），可以换回字面形式。
- **[A7]** 易混词对。第 k 步（README 里 Dockerfile 的 Step 1 到 5，旁白只给这五步编号）≠ 构建步骤（BuildKit 的步骤，这个脚本里从不编号）≠ 进度条的 step k of N（画面上的英文，不念出来）。层（image 的层）≠ 可写层（container 的）≠ 一级（第 1 讲梯子的一级）。仓库（Docker Hub 上的一个 repository）≠ repo（git 仓库；只在标题和文档里写“仓库”，那时 Docker Hub 的一律写“Docker Hub 仓库”）≠ registry（整个 Docker Hub；书面“镜像仓库”）。tag（Docker tag；打 tag）≠ 标签（画面上的视频标签：黄色的 your turn 标签、灰色的 extra 标签；书面里“标签”指 Docker tag）。配方（把 Dockerfile 比作 recipe）≠ 参考答案（solution，Dockerfile.txt）。包裹（构建上下文）≠ 包（Python 包：11 个包）≠ 软件包（apt / Debian 的：92 个新软件包）。构建（build）≠ 运行（run）≠ 部署（deploy）。复制（COPY、cp）≠ 下载（download）≠ pull。退出（exit）≠ 停止（container 停了、docker stop）≠ 删除（--rm 删掉、删除 VM）≠ 清理（docker system prune、clean up）≠ 回收（reclaim space）。根目录（top folder /）≠ root（用户）≠ base image。提示符（shell 或 Python 的 prompt）≠ 提示（hint）。参数（flag、默认参数）≠ 指令（Dockerfile instruction）≠ 命令（command；CMD 照写 CMD）。进程（process）≠ 程序（program：要启动的程序、Python 程序）。内核（kernel）≠ 核心（只用在 the core of the operating system 这句解释里）。平台（CPU 平台）≠ 菜单（多平台 tag）≠ 一行（菜单里的一行）。货架（registry 的 shelves）≠ 第 1 讲的架子（sys.path）。门（Docker socket）和第 1 讲的门（PATH 目录）是同一类画面。校验和（checksum，复制进来的文件）≠ 指纹（fingerprint：缓存的徽章、digest）≠ digest（打印出来的词）。访问令牌（Docker Hub access token，介绍过后简称令牌）≠ 密码。账号 ≠ 用户名。磁盘占用 / 内容大小（docker image ls 的 DISK USAGE / CONTENT SIZE）。小疏漏（slip）≠ 小缺口（gap）≠ 小小的不一致（mismatch）≠ 小错误（mistake），和第 3 讲一致。错误（泛指）≠ 异常（Python exception）≠ 报错（屏幕上的出错信息）≠ 运行时错误（runtime error），和第 1 讲一致。
- **[A8]** 语体：助教带实验课。指令短，动词口语化（装、跑、删、敲、输入、改、建）；称呼用“你”（跟练视频，一对一；不用“您”“大家”“同学们”）；“我们”指录制时的我们（我们没有账号，所以没法跑）。用中文语序，句子内部可以重组。避免翻译腔：不说“让我们……”（说“我们来……/ 先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不用“一个……的”长链。不用网络流行语。英文的口语节奏按意思转：Here's a fresh virtual machine → 这是一台全新的虚拟机；Just watch → 先看就好；Hold that thought → 先记住这个问题；One surprise → 有个意外；Here's why the final dot matters → 末尾那个点为什么重要，原因在这儿；Remember lecture 1 → 回想一下第 1 讲；for real → 这次是真的；plenty → 够用了；slid in between → 插到了中间；Docker is fine → Docker 没问题；That's not a Docker problem → 这不是 Docker 的问题；Before you go, clean up → 走之前，先清理一下。
- **[A9]** 准确。限定语照译：only 只，every 每个，all 全部，may 可能，usually 通常，under 不到，about 大约，or newer / and newer 及以上，the newest stable 最新的稳定版，by default 默认，right away 马上，at once 一次就。at the time of recording 每次都译成“录制时”，绝不省略（3.12.15、0.13.0、3.15.0、Docker 29、518 MB、144 MB、20.10.24、26.1.5）。版本、大小、个数、行号、步骤号和屏幕完全一致。勘误温和，后面一定紧跟改法：一个小疏漏（README 说 build the docker container；docker login 用 -p）、一个小缺口（没有 .dockerignore；跳过了 apt-get update）、一个小小的不一致（requires-python 和 3.12 的 image；README 拉的是授课老师的 image）。思考题（S06、S07、S09、S11、S13）只问不答，措辞不能泄露答案（S07 不能说 uv 会下载 Python；S06 不能暗示包没装；S13 不能说“不能”）。
- **[A10]** 名字。产品、公司、课程保持拉丁字母（A1 b）；“哈佛”只在标题和简介里出现。课程：AC215；lecture 1 → 第 1 讲；last lecture → 上节课；next time → 下节课；today → 今天；part 1 / part 2 → 第一部分 / 第二部分；Containers 2（下节课的标题）→ 容器 II，和第 3 讲的标题一致；Tutorial 0 照写；the instructor → 授课老师（绝不写名字）；授课老师的 image dlops/simple-translate 照写。用户名 student、VM 名 ac215-l02、image 名 simple-translate 和 simple-translate-ac215、Docker Hub 的命名空间 library、venv 的提示符 app 照写；container ID 从不念出来。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（含注释）、README 引文卡、三个进度条（README › Developing App using Containers，step k of N）、标签（your turn、extra、illustration、stand-in · local registry, not Docker Hub、watch only · don't type、erratum、real capture · 2026-10-13、at the time of recording、preview）、计价器表盘、“Pause and ponder”卡片都是英文，场景不用做任何语言改动。所以旁白提到画面上的标签时，字幕照画面写：黄色的 your turn 标签、灰色的 extra 标签（第 1 讲写“轮到你了”“额外”，是因为当时计划翻译画面标签；第 2、3 讲没有）。旁白用自己的话说的照常翻译：an extra check → 额外检查，as an extra → 这是额外的一步，a stand-in → 替身，the tracker → 进度条，code panels → 代码面板。旁白转述 README 时说“README 里说……”。
- **[A12]** 只用大陆简体：默认、程序、代码、文件、目录、服务器、网络、内存、磁盘、脚本、视频、用户名、信息、账号、令牌、进程、字节；不用預設、程式、程式碼、檔案、資料夾、伺服器、網路、記憶體、磁碟、腳本、影片、使用者、帳號、權杖、行程。

### B. 排版

- **[B1]** 空格。中文和拉丁字母、数字、实物之间加一个半角空格（输入 docker build、Python 3.12、第 49 行、11 个包、518 MB、.git 目录、container 里、1 号进程、M 系列 Mac）。check 会检查每个显示句子缺不缺空格。实物内部的空格照原样（docker run --rm -ti simple-translate），实物内部绝不加空格。全角标点旁不加空格（……cd simple-translate。是 bash，）。中文占位符和实物用斜杠相连时不加空格（你的用户名/simple-translate-ac215）。不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角：，。、；：？！“”……，实物旁边也一样（输入 exit。）。列举用顿号（bash、Python、uv）。**任何括号都不用**：（）、()、《》、【】都不行，没有 say: 时 check 不允许，双语字幕带也不需要括注。“”只用于中文里引用的想法或词；实物和标签名不加引号。一个中文句子内部不出现。？！（一个英文句子对应一个中文句子），改用，；：。“第 N 步”后面接说明时用全角冒号。问句保留？。破折号——可以用（自家字体能画），但多数时候冒号更好读。
- **[B3]** 符号和单独的点。没有 say: 时，check 不允许数学符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=）、数字后面跟 !、letter_letter 形式的名字（A6）。所以关系用文字说：3.13 及以上（不写 >=3.13）、低于 3.15、小于号和大于号。照屏幕保留、check 也允许的有：路径和名字里的 /（/usr/local/bin、linux/amd64、dlops/simple-translate）、文件名里的 .、参数和名字里的 -、image 名里的 :（python:3.12-slim-bookworm）、&&（用 && 串起来）、$$（echo $$）、@（@ 符号后面）。单独的 . 和 ./ 用文字说，因为一个孤零零的点混在中文标点里看不出来：构建命令末尾的点 → 末尾那个点；COPY copies this folder, dot, into dot slash → 把这个目录，也就是那个点，复制到 image 的根目录，也就是点斜杠（英文行用 en_display 给出 . 和 ./）。

### C. 数字、单位与版本号

- **[C1]** 显示文字里的数字。和屏幕、终端、代码对应的一律用阿拉伯数字：步骤号（第 1 步到第 5 步）、行号（第 3 行、第 6 行、第 7 行、第 11 行、第 12 行、第 49 行）、屏幕上显示的个数（有 7 layers 计数器时的 7 层、4 层、11 个包、92 个新软件包、91 个、退出码 126、1 号进程、0 字节）、版本、大小、日期。叙述里的小数目和序数用汉字：四个词、三个进度条、两个 Python、两个名字、一个 ID、两层新的 / 两个新层、四个构建步骤、三行 ENV、四段、五个平台、两种 arm、两个办法、两件可选的杂事、第一部分 / 第二部分、第一题……第五题、一个月。英文用单词说、屏幕显示数字时，跟屏幕（in seven layers，屏幕上有 7 layers 计数器 → 一共 7 层）；屏幕上没有时，跟英文（pause and run both → 两条都跑一遍）。
- **[C2]** 单位、版本号与日期。大小照 Docker 的打印，加半角空格、用英文单位：50 MB、63 KB、518 MB、144 MB、97.5 MB、250 KB、125 MB、107 MB、118 MB；zero bytes → 0 字节；under 50 megabytes compressed → 压缩后不到 50 MB。版本带上名字：Python 3.12、Python 3.12.15、Python 3.14.7、CPython 3.15.0、Python 3.13、uv 0.13.0、uv 0.12.15、Docker 29、20.10.24、26.1.5、Debian 12、Debian 13。范围：3.13 及以上；the Python range is open → Python 的范围没有上限。日期：September 16 → 9 月 16 日；a month apart → 相隔一个月。没有配音，所以不存在“读法”。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。script.md 的每个 SAY 行在 narration/*.yaml 里一个条目（129 段）；`en` 和 SAY 行逐字节相同；`zh` 的条目数和 explainer.voice.split_sentences 切出的英文句子数完全相同（这个脚本 371 句）。只在句子内部重组，绝不合并或拆分。短句也单独一项：It's 3.14.7. → 是 3.14.7。；No. → 不能。（S06、S13：回答“能跑吗”）；Why? → 为什么？；Rebuild. → 再构建一次。；Answer Y. → 输入 Y。；Type exit. → 输入 exit。；Now predict. → 先预测一下。；Now a puzzle. → 先出个小题。；Now ponder. → 来想一想。；Now the answer. → 现在揭晓答案。；Two optional chores. → 还有两件可选的杂事。；And why sudo? → 那为什么要 sudo？。跑 `python -m explainer.i18n check videos/ac215-l02-containers-1 --lang zh`，直到输出 OK。
- **[D2]** 不写 say:，不写锚点。没有中文配音：绝不写 say:（显示行就是唯一的文字），绝不写 anchors:（锚点只给中文配音版安排动画节拍用）。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 显示行要能通过 check。没有 say: 时，每个显示句子都要通过 explainer.i18n.spoken_problems：没有括号（B2），没有数学符号（B3），没有 letter_letter 形式的名字（A6），数字后面不跟 !，分句不以“种”加，。！？结尾（改写：“两种比较少见的。”可以，“有两种。”不行），汉字和拉丁字母或数字之间有半角空格（B1），每句以。！？或……结尾（后面可以再跟 ” 或 」），每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。check 用正则 `[A-Za-z][A-Za-z'.-]*` 切词：simple-translate-ac215 切成 simple-translate-ac，ac215-l02 切成 ac，/.venv 切成 venv，arm64 切成 arm，UTF-8 切成 UTF-。check 报出的拉丁词，要么是该翻译的英文词（通常如此），要么是漏收的实物：按同样的切法把它加进 allowed_spoken_latin，并加进对应的词条。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都写一项 en_display，给出屏幕上的字面形式，其余部分和 SAY 逐字相同；同一段的其他句子写 null。对照（SAY → en_display）：dash dash rm → --rm；dash t i → -ti；dash t / dash f / dash a / dash u / dash p / dash c / dash i → -t / -f / -a / -u / -p / -c / -i；dash dash progress equals plain → --progress=plain；dash dash platform equals linux slash amd64 → --platform=linux/amd64；linux slash amd64 → linux/amd64；slash bin slash bash → /bin/bash；slash dot venv → /.venv；dot venv → .venv；user local bin → /usr/local/bin；dot dockerignore / dockerignore file → .dockerignore / .dockerignore file；the gitignore file → the .gitignore file；the final dot / this folder, dot → .；dot slash → ./；docker dot I-O → docker.io；dlops slash simple-translate → dlops/simple-translate；your user name, slash simple-translate-ac215 → `<your user name>/simple-translate-ac215`；echo dollar dollar → echo $$；docker ps dash a → docker ps -a；git add dash f → git add -f；sudo docker dash dash version → sudo docker --version；docker system prune dash a → docker system prune -a；desktop linux → desktop-linux；FROM python, 3.12, slim bookworm → FROM python:3.12-slim-bookworm；mounted from library python → Mounted from library/python；the virtual env variable → the VIRTUAL_ENV variable；raise exception equals True → raise_exception=True；exit with parentheses → exit()；no module named art → No module named 'art'；too many requests → toomanyrequests；unable to locate package → Unable to locate package。README 的占位符保留 SAY 的 your user name。英文版自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只翻译它的英文句子：不加命令、参数、括注、中文控制台名或解释；只在英文标了 extra 的地方说“额外”；不给保留英文的词加中文注释（英文行就在正下方）。唯一允许的改动：SAY 把实物说短了或念成了单词时，照屏幕写实物（A5、B3）；SAY 说 the hidden git folder、the editor's VS Code folder 时，写出目录名（隐藏的 .git 目录、编辑器的 .vscode 目录）。
- **[D6]** 固定句式。Pause and run it. → 暂停一下，自己跑一遍。Pause and run both. → 暂停一下，两条都跑一遍。Pause and do it. / Pause and do that. → 暂停一下，照着做。Pause and do it now. → 现在就暂停去做。Pause and build. → 暂停一下，构建一次。Pause and build again. → 暂停一下，再构建一次。Pause and run the build. → 暂停一下，跑一下构建。Pause and create the file. → 暂停一下，把文件建好。Pause and make yours. → 暂停一下，建好你自己的令牌。Pause and log in. → 暂停一下，登录。Pause and run it with your own name. → 暂停一下，用你自己的用户名跑一遍。Pause now: create your VM, and wait until … → 现在暂停：创建你的 VM，等到……　pause after it → 跑完先暂停。Pause and run it, then … → 暂停一下，自己跑一遍，然后……　Just watch → 先看就好；just watch those → 那些只看就好。When the yellow your-turn tag appears, pause and run the command → 看到黄色的 your turn 标签，就暂停，自己跑这条命令。a gray extra tag marks a check that isn't in the README → 灰色的 extra 标签表示这个检查 README 里没有。One extra check, not in the README: / An extra check, not in the README: → 额外检查一下，README 里没有这一步：　an extra / as an extra / another extra → 这是额外的一步 / 作为额外的一步 / 又一个额外检查。Two extra checks → 两个额外检查。this scene and the next are extras / this scene is all extras → 这一段和下一段都是额外内容 / 这一段全是额外内容。Something to ponder: → 来想一个问题：　Now predict. → 先预测一下。Now a puzzle. → 先出个小题。Now ponder. → 来想一想。Now the answer. → 现在揭晓答案。And the opening question: → 再回到开头那个问题：　That answers the question from part 1. → 第一部分留下的问题，这下有答案了。Hold that thought → 先记住这个问题。Step N adds … → 第 N 步加上……　Dockerfile step 1 → Dockerfile 的第 1 步。Type exit. / Type exit to leave. → 输入 exit。/ 输入 exit 退出。Five questions to test yourself. → 五道自测题。One: … Five: → 第一题：……第五题：　The answers are in the exercises, and every command is in the study guide. → 答案在练习里，每条命令都在学习指南里。Next time, Containers 2: → 下节课是容器 II：
- **[D7]** 文件。narration/g1.yaml = S01–S09（第一部分），narration/g2.yaml = S10–S16（第二部分），和第 1 讲一样；每个文件开头一段注释（覆盖哪些场景、用了哪些规则：A6 文字描述的实物、D4 en_display、不写 say:/锚点），按脚本顺序排列。字符串用双引号；字面的双引号和反斜杠要按 YAML 转义。
- **[D8]** 按英文时间轴的长度。观众是边听英文边读中文，字幕带在英文分段的地方切换（一段中文读起来快于每秒 9 个单位时，最多多给 1 秒）。每个中文句子读起来要和英文听起来差不多长：经验上每个英文词最多约 2 个单位（汉字算 1，拉丁字符算 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也算长度（sudo docker run --rm -ti dlops/simple-translate 约 26 个单位，python:3.12-slim-bookworm 约 14 个）：英文没重复的地方不要重复。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位、每条最多 2 行。分句最好不超过约 24 个单位，用，；：隔开，给切分程序留出干净的切点；避免超过 30 个单位却没有标点的分句。
- **[G2]** 字幕条结尾：工具链会去掉条末的。，、；：，保留？！……和收尾的 ”（subtitles.strip_end）。能用中文词收尾时，不要以“实物 + 句号”结尾（……这个 image。比 ……simple-translate。好读，但两种都合法）。
- **[G3]** 命令不能被拆开。切分程序把中文行里两个拉丁词之间的空格当成好切点，所以 docker run --rm -ti simple-translate 或 docker system prune -a 可能被拆成两行，观众就没法照抄了。把整条命令放在分句末尾、全角冒号后面（第 2 步加一行：ENTRYPOINT /bin/bash。），一条字幕最多一条命令，周围的中文尽量少。这里写出来的最长命令是 sudo docker run --rm -ti dlops/simple-translate（约 26 个单位）和 docker buildx use default；一行放不下、或者含有 A6 字符的命令用文字描述（docker tag，先写 simple-translate，再写你的用户名/simple-translate-ac215）。渲染出 .zh.srt 后，逐条检查含命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、分集和章节标题用书面语体（A4：容器、镜像、基础镜像、镜像仓库、标签、推送、仓库、克隆）；问句保留问号；保留英文的冒号结构（Dockerfile 第 1 步：FROM）；命令、指令和文件名照写（meta.yaml 不经过 check，可以用括号）。核心概念章节附英文简称，方便搜索：镜像、层、容器与镜像仓库（registry）。Containers I → 容器 I（第 3 讲是容器 II）。和第 1 讲英文标题相同的章节沿用第 1 讲的中文（Tear down, recap, and what's next → 收尾、回顾和下节预告）。
- **[H2]** 简介（B 站 / YouTube）：两三句话：这是 AC215 第 2 讲 dlops-io/simple-translate 的跟练视频；观众做了什么、学到什么（五步写出 Dockerfile，构建并运行，image 和 container 的区别，ENTRYPOINT 和 CMD，为什么写着 Python 3.12 的 image 跑的是 3.15，层缓存，打 tag 并推送，平台，在只装了 Docker 的 VM 上一条命令部署）；英文旁白、中文和双语字幕，README 的每条命令按原样、按顺序出现，终端输出录于 2026-10-13。书面语体，用这份词表的译名。
- **[H3]** 配套材料：i18n/zh/README.md（以及 exercises.md / digest.md，如果做的话）按这份词表、用书面语体翻译（容器、镜像、基础镜像、镜像层、可写层、构建上下文、层缓存、镜像仓库（registry）、仓库、标签、推送、拉取、访问令牌、多平台构建、守护进程（daemon））；这些文件不经过 check，可以用括号和下划线。标题和 `<summary>答案</summary>` 要翻译。文末一张术语表：English | 这里的说法 | 常见的其他译法（镜像层、构建缓存、注册中心、虚悬镜像（dangling image）、套接字、守护进程、清单列表（manifest list）、构建证明（attestation））。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名、行内 `code` 一律不改；只翻译 # 注释和周围的说明。

### I. 工具链

- **[I1]**（请求，和第 3 讲的 I1 相同）explainer.i18n check 在句子没有 say: 时，把语音检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）用在显示行上。对只有字幕的视频（这个系列；video.yaml 没有 languages.zh.voice，这份词表写的是 voice: none），这些检查什么也保护不了，反而逼出了 A6 和 B3。建议：词表的 voice 是 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。那样 A6 就只剩字面形式：virtual env 这个变量 → VIRTUAL_ENV 这个变量、--progress=plain、--platform=linux/amd64、exit()。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 _cuts 把中文行里拉丁词之间的空格当成好切点，所以命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
