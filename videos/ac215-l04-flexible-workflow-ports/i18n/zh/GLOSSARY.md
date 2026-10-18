# AC215 第 4 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose (follow-along: mega-pipeline flexible-workflow, port_toy)*（`videos/ac215-l04-flexible-workflow-ports`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，英文技术文档读得很顺；做过第 1 讲（VM、venv、uv）、第 2 讲（现成的 Dockerfile、image 和 container、层缓存、Docker Hub、平台）和第 3 讲（用课程密钥跑五个 container 的 mega-pipeline、bind mount、uv add）；这一讲第一次自己管服务账号、用包装脚本、在“构建还是 pull”之间做选择，也第一次接触 container 网络、port 和 Compose；开着两个 clone（mega-pipeline 的 flexible-workflow 分支和 port_toy），边看边敲命令  
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l04-flexible-workflow-ports.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5，“三点十一点二”“点 venv”“杠 m”这类读法、数字和符号怎么念）都不适用，只保留显示规则  
英文原稿：`script.md` v2（SAY 行是旁白：156 段、372 句；SHOW 行是画面）；`build/review_spoken.md` 第 22 条（要进词表的说法和需要 `en_display` 的段落）和第 29 条（章节名）已并入  
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词；容器两讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md) 和 [`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md) 定下容器的词和“只有字幕”的整套规则。前三讲已经定下的词一律沿用；新的是第二部分的网络词汇（A13）和 flexible workflow 的词（服务账号、三道关卡、构建还是 pull、docker-shell.sh）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“起一个 container”“构建 image”“从 Docker Hub pull 下来”“push 上去”“先 stash 一下再 checkout”“-p 发布一个 port”“container 里的 localhost 是它自己”。硬译成“启动容器实例”“从镜像注册中心拉取”“贮藏更改后检出分支”，反而像说明书。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、浏览器和 `docker-compose.yml` 里找东西。命令、参数、文件名、路径、image 名、环境变量、Compose 的键、IAM 角色名、报错原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（构建、层、缓存、挂载、目录、终端、提示符、脚本、分支、密钥、服务账号、角色、权限、网络、子网、地址、连接、数据包、监听、映射、请求、进程、信号、退出码）一律说中文；Google Cloud、Git 和 Docker 的概念用它们中文文档的官方译名，方便搜索。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、标签、进度条、示意控制台和 port_toy 的网页都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（Docker、Git 和 Google Cloud 的中文文档）；和整个系列一致（第 1 讲定下共用的词，第 2、3 讲定下容器的词）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、image / 包 / 网络的名字、配置项和 Compose 的键、环境变量、IAM 角色名、终端原文和报错名、控制台上的字样、画面上的标签、README 的章节标题）逐字照抄，不翻译、不变形、不加引号。检查器逼出来的例外：带下划线的名字，以及 + < > ( ) = 这几个字符，按旁白的说法写（A6、B3）。终端输出、代码面板、README 卡片、标签和进度条都是英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 VM、venv、shell、root、repo、clone、commit、import、pin；第 2、3 讲的 container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、bucket、pipeline、bind mount、prompt（只指 LLM 的 prompt）、API、ID；这一讲新增 port（连同 host port、container port）、localhost、stash、checkout、token（只指 LLM 的 token）、assert。
3. **其余一律用中文标准术语**：构建、重新构建、构建步骤 k、构建器、层、缓存、挂载、目录、工作区目录、组件目录、终端、提示符、脚本、模式、参数、环境变量、包、软件包、分支、已跟踪、未跟踪、被忽略、服务账号、密钥、访问令牌、角色、权限、启用、结算、计费、组件、阶段、组名、网络、子网、地址、连接、数据包、发布、监听、映射、请求、回复、服务（Compose 的 service）、键（Compose 的 key）、进程、信号、退出码、前台、后台、重新创建。
4. **视频的比喻按意思译，一个比喻一个词**：配方（recipe，第 2 讲）、路标（signpost，第 3 讲）、窗（bind mount，第 3 讲）、盒子（box）、三堆和墙（切换分支时的三堆文件和两堵墙）、关卡（gate）、小电脑（little computer）、局域网（home network）、电话簿（phone book）、导轨（rail）、临街的门和房间（street door 和 room，也就是 host port 和 container port）。
5. **书面语体**（标题、meta.yaml、配套文档）：仓库、克隆、提交、容器、镜像、基础镜像、镜像仓库、存储桶、推送、拉取、绑定挂载、端口。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **工具链的约束也是规则**：每个英文句子对应一个中文句子（156 段、372 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **port 说英文，书面写“端口”**（A13）。系列清单（ac215-video skill）把 port 列为保留英文；第 3 讲的 A13 也写明后面几讲从那张清单取用。这一讲的画面和命令里到处是它：PORTS 那一列、PORT 变量、ports 这个键、port is already allocated、README 的 Step 2: Check the ports 和 Step 3: Change the ports。所以字幕说 port（量词“个”），和观众盯着看的东西一致；标题、章节名、meta.yaml 和配套文档写“端口”，就像 container / image 书面写“容器 / 镜像”。host port、container port 照说：它们是 README 给 -p 三段起的名字（IP 地址、host port、container port）。localhost 照写（它是一个字面的主机名）。
- **其余网络的词说中文**：network → 网络，subnet → 子网，address → 地址，connection → 连接，packet → 数据包，publish（一个 port）→ 发布，listen → 监听，mapping → 映射，temporary port → 临时 port，request / reply → 请求 / 回复，hostname → 主机名。不为了“味道”说英文。
- **两种“发布”**：英文把 image 推到 Docker Hub 和用 -p 开放一个 port 都叫 publish，中文也都用“发布”；上下文总能分清（A3、A7）。
- **stash、checkout、assert、token 进封闭清单**：“先 stash 一下”“checkout 成功了”“assert 会拦住你”“按 token 计费”都是实验课原话；中文的“贮藏”“检出”“断言”“词元”反而生硬。token 只指 LLM 的 token；身份验证用的那个永远是“访问令牌”（第 3 讲）。
- **Compose 的 service 说“服务”，YAML 的 key 说“键”**：Docker 中文文档就这么叫；“键”和“密钥”（key 文件）分开（A7）。
- **processor 和“处理器”分开**：processor 是 port_toy 里那个 container 的名字，照写；S06 和 S09 的 processor types 指 CPU，译“处理器类型 / 多种处理器”（A7）。
- **带下划线的名字和检查器不收的符号**（A6、B3，同第 3 讲）：port_toy → port toy，port_toy-gateway → port toy 加上 -gateway，PROCESSOR_PORT → processor port 这个变量，container_name / depends_on → container name / depends on 这个键；Ctrl+C → Ctrl-C；chmod +x → 用 chmod 加上可执行权限；git checkout -- . → git checkout 加上 -- 和一个点；<your-project-id> 的尖括号用文字说。英文行用 en_display 给出字面形式（D4）。
- **比喻**：沿用第 2 讲的“配方”、第 3 讲的“路标”和“窗”；这一讲新造的各用一个词：盒子、三堆、墙、关卡、小电脑、局域网、电话簿、导轨、临街的门、房间。门（host port）和房间（container port）是一对；关卡（S05）不叫“门”，免得和第二部分撞车。
- **画面标签照画面写**（同第 2、3 讲）：黄色的 your turn 标签、灰色的 extra 标签。旁白自己说的照常翻译：额外检查、进度条、代码面板、完整日志。
- **勘误温和、紧跟改法**：一个小疏漏（assert 只拒绝空值、Vertex AI User、目标语言和 ElevenLabs、日志里写死的 8090）、一个小缺口（stash 不管未跟踪的文件、README 没说怎么建 bucket）、一个小小的不准确（run 并不总是从 registry pull）（A9）。
- **录制时**：at the time of recording 每次都译“录制时”，绝不省略（Docker Engine 29.8.2、Python 3.14.8）。我们录制时没有 Google 账号：凡是调用 Google 的地方，字幕说“有密钥的话，要找的是……”。
- **章节名按意思译**（第 29 条）：五个真实的报错（five honest errors：其中 generate 那一步其实是悄无声息的退出码 0，但仍是真实的结果）、偷渡的密钥（stowaway key）、线路上的端口（ports on the wire）、声明式写法（declared）。
- **按英文时间轴读**：中文是边听英文边读的，每句中文读起来的时间要和英文听起来差不多；删掉多余的连接词和重复的主语，绝不删内容（D8）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令、参数、文件名和路径、分支 / image / 构建器 / 网络 / container / 账号的名字、占位值、docker-shell.sh 的模式（dev、run、prod）、Compose 的键、环境变量（PORT）、IAM 角色名（Storage Admin、Agent Platform User、Cloud Speech Client、Cloud Translation API User、Vertex AI User）、apt 软件包 ffmpeg（S07，同第 3 讲）、终端原文和报错名、旁白提到的屏幕标签（your turn、extra）、浏览器按钮 Send、README 标题（Get the Code、How to Run a Component、Quick Reference、Prerequisites、Handy commands）。完整清单见 A1（a）；带下划线的名字和检查器不收的符号例外（A6、B3）。
- 产品、组织、课程和名字：Google Cloud、Cloud Storage、Speech-to-Text、Text-to-Speech、Vertex AI、Gemini、IAM、Docker Engine、Docker Hub、Docker Compose、BuildKit、buildx、Git BASH、GitHub、pipenv、uv、gcloud、ElevenLabs、Apple Silicon、amd64、arm64、JSON、IP、AC215、Tutorial 0、student、app，等等（A1 b）。
- 实验课口语，封闭清单：VM、venv、shell、root、repo、clone、commit、import、pin（第 1 讲）；container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、bucket、pipeline、bind mount、prompt（只指 LLM 的 prompt）、API、ID（第 2、3 讲）；**port（host port、container port）、localhost、stash、checkout、token（只指 LLM 的 token）、assert（这一讲新增）**。
- 系列清单里保留英文、但这一讲没用到的：volume（只作为 Compose 的键 volumes 出现）、PATH、endpoint、embedding、agent（只出现在角色名 Agent Platform User 里）、LoRA、CI（A14）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| build / rebuild / build locally | 构建 / 重新构建 / 在本地构建 | build step k（BuildKit） | 构建步骤 k |
| step k（README） | 第 k 步 | builder / build engine | 构建器 / 构建引擎 |
| layer / system layer / cached | 层 / 系统层 / 用了缓存 | full log | 完整日志 |
| processor types（CPU） | 处理器类型 / 多种处理器 | stale image | 过期的 image |
| recipe | 配方 | signpost | 路标 |
| box | 盒子 | window（bind mount） | 窗 / 这扇窗 |
| mount（动词） | 挂载 | environment variable | 环境变量 |
| script / mode / case statement | 脚本 / 模式 / case 语句 | no argument | 不带参数 |
| workspace folder | 工作区目录 | component folder | 组件目录 |
| branch / switch branches | 分支 / 切换分支 | tracked / untracked / ignored | 已跟踪 / 未跟踪 / 被忽略 |
| three piles / wall | 三堆 / 墙 | discard / put away | 丢弃 / 收起来 |
| service account | 服务账号 | key / JSON key | 密钥 / JSON 密钥 |
| access token | 访问令牌 | token（LLM） | token |
| gate / gate 1 | 关卡 / 第 1 关 | role / grant | 角色 / 授予 |
| permission error | 权限错误 | enable / switched on | 启用 / 打开 |
| billing / bills | 结算 / 计费 | placeholder / angle brackets | 占位符 / 尖括号 |
| group name / project ID | 组名 / 项目 ID | prefixes / drawers | 前缀 / 抽屉 |
| exit code / exit status | 退出码 | Google client / on import | Google 客户端 / 导入时 |
| network / subnet | 网络 / 子网 | address / IP address | 地址 / IP 地址 |
| little computer | 小电脑 | home network | 局域网 |
| phone book | 电话簿 | rail | 导轨 |
| publish（a port） | 发布 | listen / internal only | 监听 / 只在内部 |
| street door / room | 临街的门 / 房间 | mapping | 映射 |
| temporary port | 临时 port | connection / packet | 连接 / 数据包 |
| request / reply | 请求 / 回复 | hostname | 主机名 |
| every address / this laptop only | 所有地址 / 只限这台笔记本 | hard-coded | 写死 |
| Compose service | 服务 / 服务名 | Compose key | 键 |
| foreground / background | 前台 / 后台 | process / signal | 进程 / 信号 |
| stopping gracefully | 优雅地停止 | killed | 被强行杀掉 |
| recreate / apply | 重新创建 / 生效 | tear down | 拆掉 |
| at the time of recording | 录制时 | an extra check | 额外检查 |
| the tracker / code panels | 进度条 / 代码面板 | Ponder this. | 来想一想。 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN：一个英文句子对应的一个中文句子），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。


### 容器、镜像、构建还是 pull / Containers, images, build or pull

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| container / containers / a container calls a database container | container / 容器（书面） | S02：直接通信的 container，第二部分再讲。 | 实验课口语（A2，同第 2、3 讲），量词“个”。标题、meta.yaml 和配套文档写“容器”（A4）。 |
| image / images / local image / the Docker Hub image / the dlops image / finished images | image / 本地 image / 镜像（书面） | S01：这条命令来自这节课的 README，在一台从没构建过这个 image 的笔记本上运行：本地没有 image，它就从 Docker Hub pull 一个下来。 | 实验课口语（A2）。字幕里绝不写“镜像”；书面写“镜像”。image name → image 名；finished images → 做好的 image。 |
| stale image / a February 2025 Python 3.8 image / any local image of that name wins | 过期的 image / 过期的镜像（书面） | S08：实际上，只要本地有同名的 image，不管多旧都会被用上；否则它运行 Docker Hub 上的 image，只在第一次 pull。 | stale → 过期的（第 1 讲：过期的 lock 文件）。章节名 S08：dev、run 和一个过期的镜像。 |
| build / build locally / builds / rebuild / a fresh build / the build | 构建 / 在本地构建 / 重新构建 / 这次构建 | S08：所以要在本地构建，不带参数或者用 dev；run 只用于你们组从这个分支 push 到你们自己 Docker Hub 账号下的 image。 | A3。docker build、buildx build 照写。字幕里不说 build（命令和模式说明里的除外）。 |
| build or pull / pull / pulls / pulled only the first time / and everyone else pulls | pull / 构建还是 pull / 拉取（书面） | S02：后来，一个人把做好的 image 发布到 Docker Hub，其他人都直接 pull。 | 实验课口语（第 2 讲）：pull 下来、pull 一个。书面写“拉取”（标题：构建还是拉取？）。 |
| push / publish / publishes / check what it would publish | push / 发布 / 推送（书面） | S09：第 4 步，prod，负责发布。 | push 照说（第 2、3 讲）；publish image → 发布（英文发布 port 也用 publish，A13：发布一个 port）。书面写“推送”。 |
| tag / look closely at the tag / under one tag / signpost | tag / 路标 | S02：仔细看这个 tag。 | tag 照说（第 2 讲：打 tag）；“标签”留给画面上的视频标签（A7）。把 tag 比作 signpost → 路标（第 3 讲给指向密钥的变量用的同一个比喻）。 |
| it's a signpost to one particular image / nothing promises it matches the commit you have | 路标 | S02：它是一个路标，指向某一个特定的 image：某一天、用某个版本的配方构建出来的。 | Nothing promises it matches the commit you have → 没有任何东西保证它和你手上的 commit 对得上。 |
| recipe / the recipe in Git / not your recipe / some version of the recipe | 配方 | S02：项目早期，每个人都用 Git 里的配方自己构建。 | 第 2 讲把 Dockerfile 比作配方；这里的配方卡片是 Dockerfile、pyproject.toml 和 uv.lock（V1）。不说“菜谱”。 |
| registry / pulls from the registry | registry / 镜像仓库（书面） | S08：一个小小的不准确：README 的概述说 run 会从 registry pull。 | 第 2 讲。书面写“镜像仓库”。 |
| Docker Hub / Docker Hub account / Docker username / dlops / dlops images | Docker Hub / Docker Hub 账号 / Docker Hub 用户名 / dlops / dlops 的 image | S06：第 10 行是密钥在 container 里的路径；第 13 行是 Docker Hub 账号的名字，dlops。 | DOCKER_USERNAME → 脚本里的 Docker Hub 用户名（A6）。dlops（课程的 Docker Hub 账号）≠ dlops-io（GitHub 组织）。 |
| base image / pulls the base image / the Python base image | base image / 基础镜像（书面） | S11：你第一次构建时，还会 pull Python 的 base image。 | 第 2 讲：字幕说 base image，书面写“基础镜像”。 |
| build step / build step 2 / the system packages / writing out the image | 构建步骤 / 构建步骤 2 / 系统软件包 / 写出 image | S06：有两步占了几乎全部时间：构建步骤 2，也就是系统软件包，还有写出 image；第一次构建还会 pull base image。 | A3、A7：BuildKit 的 [k/5] 永远是“构建步骤 k”；“第 k 步”是 README 的步骤。 |
| layer / system layer / apt layer / copy layer / cached / reuses from the cache | 层 / 系统层 / apt 那一层 / COPY 那一层 / 缓存 / 用了缓存 | S07：接下来，synthesis audio en 的构建只要 8 秒：它的系统层用了缓存。 | 第 3 讲。the copy line → COPY 那一行；only the copy layer is new → 只有 COPY 那一层是新的。 |
| full log / the full log shows | 完整日志 | S06：完整日志说明了 uv sync 为什么这么快：image 自带的 Python，录制时是 3.14.8，已经满足 3.14 及以上，所以 uv 一个都不用下载。 | 第 3 讲。at the time of recording → 录制时（A9）。 |
| builder / build engine / multi-arch / processor types / makes it current / docker buildx use default | 构建器 / 构建引擎 / 处理器类型 / multi-arch / buildx | S09：它会重新创建一个叫 multi-arch 的构建器，一个能为多种处理器构建的构建引擎。 | builder → 构建器（第 2 讲）。processor types → 处理器类型 / 多种处理器：绝不写 processor（那是 port_toy 的 container，A7）。Dash dash use makes it current → 加了 --use，它就成了当前的构建器。 |
| amd64 / arm64 / Apple-silicon Mac / cloud VM | amd64 / arm64 / Apple Silicon 的 Mac / 云上的 VM | S09：然后一条 buildx build 做出 amd64 和 arm64 两个 image，用同一个 tag 一起 push 上去：和第 2 讲一样，Apple Silicon 的 Mac 会 pull 其中一个，云上的 VM 会 pull 另一个。 | 平台名照写（第 2 讲）。 |
| box / opens the box / your code, their environment / slides over its app folder | 盒子 / 打开这个盒子 | S08：一个额外的 inspect 打开了这个盒子：创建于 2025 年 2 月 18 日，Python 3.8.17，启动 pipenv shell，以 root 运行。 | V1 里封好的盒子（一个 image；S11 里是 container：inside its own box → 在它自己的盒子里）。your code, their environment → 你的代码，他们的环境；slides over → 盖在……上。 |
| teammate / a real team / your team / built like a team | 队友 / 团队 / 你们组 | S08：有个队友从没构建过这个 image，直接输入 docker-shell.sh run。 | A10。Your team owns its bucket → 你们组有自己的 bucket。 |
| surprise / puzzle / two puzzles / the first puzzle, solved / the second puzzle | 意外 / 谜题 | S08：对 generate text 来说，这就是开头那个导入错误：第一个谜题，解开了。 | surprise → 意外（第 3 讲）。 |

### docker-shell.sh、模式与挂载 / docker-shell.sh, modes, mounts

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| docker-shell.sh / one script / the script / wrapper script / the long docker build and docker run commands | docker-shell.sh / 脚本 / 包装脚本（书面） | S02：而且每个组件都有一个脚本，docker-shell.sh，里面装着那两条很长的 docker build 和 docker run 命令。 | 文件名；“这个脚本”。画面上敲的是 ./docker-shell.sh（G3）。 |
| mode / case statement / first word / no argument / no word / default / dev / run / prod | 模式 / case 语句 / 不带参数 / 默认模式 / dev / run / prod | S06：脚本里的 case 语句，把你输入的第一个词变成一种模式。 | 模式名照写（实物）。No word: build, then run → 什么都不加：先构建，再运行。Dev only builds … → 用 dev 只构建，用 run 只运行，用 prod 则为两种处理器构建并 push（A5：句子不以 dev 开头）。 |
| Using local image / Local image not found / Creating a Pipfile | Using local image / Local image not found / Creating a Pipfile | S08：第 3 步，run，跳过构建：显示 Using local image，因为本地已经有一个。 | 终端原文，跟在“显示 / 提示 / 报”后面照写（第 1 讲）。Local image not found → 提示 Local image not found，于是……。 |
| pipenv / Pipfile / pipenv shell / an environment pipenv made / pipenv-flexible-workflow / owned by root | pipenv / Pipfile / pipenv shell / pipenv 建的环境 / pipenv-flexible-workflow / 属于 root | S08：这是 pipenv，这门课在 uv 之前用的工具。 | en_display：pipenv flexible workflow → pipenv-flexible-workflow（D4）。 |
| window / two windows into your laptop / the window shows it at once / through the window | 窗 / 两扇窗 / 这扇窗 | S06：运行时会开两扇通往你笔记本的窗。 | 第 3 讲 bind mount 的比喻；量词“扇”。不说“窗口”（终端窗口）。密钥从不被复制（A9）。 |
| mount / mounts / bind mount / the secrets mount | 挂载 / 两个挂载 / bind mount / 绑定挂载（书面） | S06：在同一个目录里再开一个终端，额外跑一个 docker inspect，就能列出这两个挂载。 | 动词和泛指的名词说“挂载”；bind mount 照说（第 3 讲）。 |
| environment variable / signpost / a signpost to the key / the signpost points to /secrets | 环境变量 / 路标 / 指向密钥的那个变量 | S06：再用 -e 设置一个环境变量：一个路标，告诉 Google 的库密钥在哪里。 | GOOGLE_APPLICATION_CREDENTIALS 不写出来（A6）。 |
| /app / /secrets / component folder / the secrets folder beside the repo | /app / /secrets / 组件目录 / repo 旁边的 secrets 目录 | S06：用 -v 把组件目录放到 /app，把 repo 旁边的 secrets 目录放到 /secrets。 | en_display：slash app → /app，slash secrets → /secrets（D4）。 |
| pwd / the folder you're in / build paths from pwd / the key's path / run it from the component folder | pwd / 你当前所在的目录 / 路径 | S06：第 8 和第 9 行用 pwd，也就是你当前所在的目录，拼出路径。 | path → 路径（A14）。$(pwd) 不写出来（B3）。 |
| venv / the venv lives outside slash app / the window can't hide it / python comes from the venv | venv | S06：和第 3 讲一样，venv 放在 /app 外面，所以这扇窗盖不住它。 | 第 1 讲。hide → 盖住（和第 3 讲“挂载没有盖住那些包”一致；“挡不住”会被读成“拦不住”）。 |
| user app / the at sign / container ID, new every run / hostname | 用户 app / @ 符号 / container ID / 主机名 | S06：你已经在里面了，用户是 app，在 /app 里；@ 符号后面是 container ID，每次运行都不一样。 | 第 3 讲。its hostname is the container ID → 它的主机名就是 container ID。 |
| second terminal / opened in the same folder / new terminal | 第二个终端 / 同一个目录 | S15：在第二个终端里，先 cd 进 port toy：Compose 读的是当前目录里的文件。 | cd into port toy → cd 进 port toy（A6）。 |
| chmod plus x / executable / harmless | chmod / 可执行 / 没有坏处 | S06：第 5 步，用 chmod 加上可执行权限，没有坏处：额外的 ls 显示它本来就是可执行的。 | B3：检查器拒绝 +；en_display 写 chmod +x。 |
| Windows / Git BASH / winpty / put winpty in front / the input device is not a TTY | Windows / Git BASH / winpty / the input device is not a TTY | S06：第 6 步，在 Windows 上：用 Git BASH，如果 Docker 报 the input device is not a TTY，就在前面加上 winpty。 | 第 3 讲。en_display：T-T-Y → TTY。 |
| uv sync / uv add / adding a package / bakes it into the image | uv sync / uv add / 打包进 image | S08：加包的时候：在 container 里跑 uv add，它会透过这扇窗更新 pyproject.toml 和 uv.lock；然后用 dev 把它打包进 image。 | bake it in → 打包进 image（第 3 讲）。 |

### Git：clone 与切换分支 / Git: clone, switch branches

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| branch / switch branches / this branch checked out / the branch's files | 分支 / 切换分支 / 这个分支的文件 | S03：在你的工作区目录里 clone 这个 repo，直接 checkout 到这个分支：git clone，加上 --branch flexible-workflow。 | 第 1 讲：branch → 分支。带 URL 的完整 clone 命令不写进中文行（G3）；en_display：--branch。 |
| checkout / git checkout / the checkout works / and Git refuses | checkout / git checkout / 拒绝 | S03：第 3 步：git checkout flexible-workflow，Git 拒绝了，原因有两个。 | 新进封闭清单：“checkout 成功了”是实验课说法。Git 作为产品名可以放在句首。 |
| stash / git stash / git stash -u / stashes untracked files too / your edits wait in the stash | stash / git stash / git stash -u | S03：额外跑一个 git stash -u，把未跟踪的文件也 stash 起来，checkout 就成功了。 | 新进封闭清单（stash 一下、还在 stash 里）。puts your edits away → 把你的修改收起来。en_display：git stash -u。 |
| tracked / untracked / ignored / three piles | 已跟踪 / 未跟踪 / 被忽略 / 三堆 | S03：在 transcribe audio 里，Dockerfile、pyproject.toml、uv.lock 和密钥都是被忽略的。 | Git 中文界面的“未跟踪”（第 1 讲）。Three piles. → 分成三堆。 |
| wall / the first wall falls / overwritten / sit where the branch has files of its own | 墙 / 第一堵墙 / 被覆盖 | S03：README 的提示解决的是第一个原因：git stash 把你的修改收起来，第一堵墙倒了。 | V2 里红色的墙。 |
| git checkout dash dash dot / discards your edits / leaves untracked files alone | 丢弃 / 未跟踪的文件 | S03：另一个办法是 git checkout，加上 -- 和一个点：它丢弃你的修改，不动未跟踪的文件。 | B3：单独的点写成“一个点”；en_display：git checkout -- . |
| git fetch origin / upstream / updates | git fetch origin / 上游 / 更新 | S03：在这里它什么都没打印：clone 下来的 repo 本来就有所有分支，上游也没有任何变化。 | Yours may list updates → 你的可能会列出一些更新。 |
| git branch / star / the commit we recorded / the commit this video pins / git log / git diff / grep | git branch / 星号 / 我们录制时的那个 commit / pin 住的 commit / git log / git diff / grep | S03：第 5 步，git branch：星号在 flexible-workflow 上。 | pin（第 1 讲）。at the commit we recorded（S03）→ 停在我们录制时的那个 commit；git log shows the commit this video pins（S10）→ git log 显示这个视频 pin 住的 commit。 |
| replaced without a word / copy them out first | 替换 | S03：额外检查显示，你在第 3 讲里那些被忽略的 Dockerfile、pyproject.toml 和 uv.lock，已经被这个分支的版本一声不吭地替换了：想留着的话，先把它们复制出来。 | A8。 |
| main / your clone from lecture 3 / if you cloned fresh / the next chapter | main / 第 3 讲的 clone / 重新 clone / 下一章 | S03：它在 main 上；如果你是重新 clone 的，直接跳到下一章。 | A10。 |

### 运行之前：目录结构、三个值、bucket / Before you run: layout, three values, bucket

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| workspace folder / your workspace / go up one level / folder layout / beside the repo / never inside it | 工作区目录 / 目录结构 | S04：运行之前，先看 README 里的目录结构：你的密钥放在 repo 旁边的 secrets 目录里，绝不放进 repo。 | README 里的 your-workspace 占位，也就是 ~/AC215。工作区目录 ≠ 工作目录（WORKDIR，第 3 讲）≠ 组件目录（A7）。 |
| three values / project ID / your bucket / group name / placeholders / type your own | 三个值 / 项目 ID / 组名 / 占位值 | S04：第 2 步：每个 cli.py 都在开头附近设置三个值：你的项目 ID、你的 bucket 和你们的组名。 | 占位值 your-project-id、your-team-bucket、group-01 照写；type your own → 换成你自己的。 |
| what ships / blank / the course's project and bucket / the instructor's group name / the course's resources | 留空 / 课程的项目和 bucket / 授课老师的组名 / 课程的资源 | S04：一个额外的 grep 显示 repo 里原本写的是什么：三个文件留空，但 generate text 和 translate text 里已经写着课程的项目和 bucket，还有授课老师的组名。 | A10：绝不出现名字。 |
| assert / an assert stops you / rejects an empty value / the guard works / help stops at the assert / AssertionError | assert / 空值 / AssertionError | S04：一个小疏漏：README 说如果你忘了改，assert 会拦住你，但它只拒绝空值。 | 新进封闭清单（Python 的 assert 语句，实验课就这么说）。here, the guard works → 在这里，这道检查起作用了。 |
| permission error / permission errors / at Google | 权限错误 / 在 Google 那边 | S05：在 Google 那边，报的是权限错误。 | 第 2、3 关在 Google 那边失败（V3）；不说“许可错误”。 |
| target language / Spanish / French / the final voice | 目标语言 / 西班牙语 / 法语 | S04：在 translate text 里，还要把目标语言从西班牙语改成法语。 | 第 1 讲。 |
| prefixes / drawers / lands under your group's name | 前缀 / 抽屉 | S04：第 3 步，你的 bucket：各个组件读写这些前缀，每个输出都落在你们组名的下面。 | 第 3 讲。 |
| bucket / your team's bucket / create the bucket in the console / a shared bucket | bucket / 存储桶（书面） | S04：还有一个小缺口：README 没说怎么创建 bucket，而且它的示例上传文件叫 test.mp3。 | 第 3 讲。en_display：test dot mp3 → test.mp3。 |
| upload a short recording / input audios / input, dash, something, dot mp3 / the transcript keeps that name | 短录音 / input audios 目录 / 转写文本 | S04：然后把一段短录音上传到一个叫 input audios 的目录里，文件名以 input- 开头、以 .mp3 结尾。 | A6；en_display：input-something.mp3。 |

### Google Cloud：服务账号、密钥与三道关卡 / Google Cloud: service account, key, three gates

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| service account / your own service account / mega-pipeline-sa / identity / callers | 服务账号 / 身份 / 调用方 | S05：对代码来说，这个身份就是一个服务账号，配一个 JSON 密钥。 | 第 1、3 讲：服务账号（不写“服务帐号”）。 |
| prove who they are / have permission / only lets in | 身份 / 权限 | S05：你的 bucket 只放行能证明自己是谁、而且有权限的调用方。 | 证明自己是谁 = 身份验证，有权限 = 授权（第 3 讲）；这里照英文的大白话说。 |
| key / JSON key / one shared key / a long generated name / whoever holds it / never commit or paste it | 密钥 / JSON 密钥 / 共用的密钥 / 密钥文件 | S05：谁拿到它，谁就能花你项目的钱：绝不要 commit，也不要贴到任何地方。 | 第 3 讲。it arrives with a long generated name → 文件名是一长串自动生成的字符。 |
| short-lived token / access token | 访问令牌 / 短期有效的访问令牌 | S05：Google 的库会把这个密钥换成一个短期有效的访问令牌，每个打到 Google API 门口的调用，都必须通过三道关卡。 | 第 3 讲：access token 绝不说 token（A7）。API doors → API 门口。 |
| gate / three gates / gate 1 / who you are / what you may do / switched on | 关卡 / 三道关卡 / 第 1 关 | S05：第 1 关问你是谁：没有密钥，调用在你的 container 里就失败了。 | V3。编号的关卡写数字（第 1 关、第 2 关、第 3 关；C1）。不说“闸门”，也不说“门”（门是 API 的门，第二部分又是 host port）。 |
| role / grant / four roles / needs a role / Text-to-Speech needs no role | 角色 / 授予 / 四个角色 / IAM 角色 | S05：给它授予四个角色：所有组件都要的 Storage Admin，Gemini 要的 Agent Platform User，还有 Cloud Speech Client 和 Cloud Translation API User。 | 角色名照控制台写（A1 a）。 |
| Vertex AI User / finds nothing now / role picker | Vertex AI User / 搜不到 | S05：一个小疏漏：generate text 的 README 还写着 Vertex AI User，现在已经搜不到这个角色了。 | 勘误：语气温和，紧跟改法（Agent Platform User）。 |
| API / the APIs / the five APIs / enable / switches on all five | API / 启用 / 打开 | S05：接着用 gcloud services enable 这条命令，把五个 API 全部打开。 | 第 1 讲：enable → 启用。 |
| console / in the console / create a service account / download a JSON key / rename it | 控制台 / 创建 / 下载 / 重命名 | S05：把它重命名为 mega-pipeline.json，放进 repo 旁边的 secrets 目录。 | 第 1 讲：控制台。提到控制台上的按钮和字段时照英文写（A1 a）。 |
| gcloud / the set project command / placeholder / angle brackets / redirections / without brackets | gcloud / 占位符 / 尖括号 / 重定向 | S05：照原样输入的话，设置项目的那条命令会失败：shell 把占位符两边的尖括号当成了重定向。 | B3：中文行里不出现尖括号。Type your own project ID, without brackets → 输入你自己的项目 ID，不要带尖括号。 |
| no active account / the login step / logged in | 没有活动账号 / 登录那一步 | S05：我们的笔记本没有 Google 账号，所以 gcloud 提示没有活动账号：这就是 Tutorial 0 里的登录那一步。 | 转述 You do not currently have an active account selected（英文旁白也是转述）。 |
| billing / a project with billing / bill your project / your project pays / spend your project's money / storage | 结算 / 计费 / 存储费 | S01：第一部分需要 Tutorial 0，以及一个开通了结算的 Google Cloud 项目；第二部分只需要 Docker。 | 第 1 讲：Billing → 结算，动作 → 计费。the bucket bills a little storage → bucket 会一直收一点存储费。 |
| bills per audio minute / bills per token / token / first chunk / a short clip | 按音频分钟数计费 / 按 token 计费 / token / 第一段 / 短音频 | S07：Speech-to-Text 按音频的分钟数计费，而且这个分支只保留长录音的第一段：用一段短音频。 | token 只用于 LLM 的 token（A7）。 |
| DefaultCredentialsError / default credentials error / was not found / gate 1, failing inside the container | DefaultCredentialsError | S07：下载这一步先打印它的参数，然后就停了：报 DefaultCredentialsError，找不到 /secrets/mega-pipeline.json 这个文件。 | 报错名照写；后半句按关键字转述（D8）。en_display：DefaultCredentialsError: File /secrets/mega-pipeline.json was not found. |
| usual causes / the script run from the wrong folder | 常见原因 | S07：常见原因有：secrets 目录里没有密钥，文件名不对，或者在错误的目录里运行了脚本。 | another file name → 文件名不对。 |
| Google client / builds the Google client on import / even help needs the key | Google 客户端 / 导入时 | S07：现在 help 停在第 23 行，那一行在导入时就创建 Google 客户端：连 help 都需要密钥。 | 第 3 讲：client → 客户端，imports → 导入。help（--help 那个检查）照说。 |
| help / the first check, help, matches the README / the README's help | help / --help / 和 README 一致 | S06：第一个检查是 help，和 README 里的一致。 | 旁白用 help 指 python cli.py --help；中文行跟着旁白写。 |

### 五个组件 / The five components

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| component / components / stage / stages / the five stages / never call each other | 组件 / 阶段 / 五个阶段 | S02：五个阶段没有变，它们仍然从不互相调用：每个都写进 bucket，下一个再从里面读。 | 第 3 讲。 |
| download / transcribe / generate / synthesis / translate / upload / the generate step | 下载 / 转写 / 生成 / 合成 / 翻译 / 上传 | S07：在 synthesis audio 里也一样：先下载，再合成。 | 第 3 讲的动词。The generate step prints only its arguments and the word generate → 生成这一步只打印参数和 generate 这个词。 |
| transcript / a text file / locally and in the bucket | 转写文本 / 文本文件 / 本地和 bucket 里 | S07：有密钥的话，要找的是转写文本，然后是 text prompts 下 group-01 里的一个文本文件，本地和 bucket 里都有。 | A6；en_display：text_prompts/group-01。 |
| exit status 0 / exits with status 0 / exit code 137 / killed | 退出码 / 退出码 0 / 退出码 137 / 被强行杀掉 | S07：退出码 0 并不能证明它做了任何事。 | exit status 和 exit code 都译“退出码”（A7：不是状态码）。Exit code 137 means killed → 退出码 137 表示被强行杀掉。 |
| loop / prompts / no prompts to work on | 循环 / prompt | S07：下载失败了，所以循环里没有 prompt 可处理。 | LLM 的 prompt 照说（第 3 讲）；shell 的 prompt 是“提示符”。 |
| Gemini model variable / a variable picks the Gemini model / the Gemini library won't import | Gemini 模型变量 / Gemini 的库 | S07：在 generate text 的 README 里还多一步：用一个变量选择 Gemini 模型。 | GEMINI_MODEL 不写出来（A6）。the Gemini library won't import → Gemini 的库导入不了。 |
| ElevenLabs bonus / reads its key from inside /app / point it at /secrets | ElevenLabs 附加任务 | S07：还有那个可选的 ElevenLabs 附加任务，是从 /app 里面读密钥的：把它改成指向 /secrets。 | 第 3 讲。 |

### 镜像里的密钥与清理 / The key in the image, clean-up

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the copy line / takes the whole folder / gitignore / dockerignore / the key is inside | COPY 那一行 / .gitignore / .dockerignore | S09：那个 .gitignore 让 secrets 进不了 Git，却挡不住它进 image；而且哪个分支都没有 .dockerignore。 | en_display：.gitignore、.dockerignore（旁白说 gitignore、dockerignore）。章节名 S09：偷渡的密钥。 |
| stowaway key | 偷渡的密钥 |  | 只用于章节名 S09（H1）。 |
| log in with an access token / shell history / set the Docker username | 访问令牌 / shell 历史记录 | S09：跑 prod 之前，先用访问令牌登录；用 -p 的话，它会留在你的 shell 历史记录里。 | 第 3 讲。en_display：dash p → -p。 |
| clean-up / free space / Port toy costs nothing | 清理 / 删掉 | S09：第一部分的清理。 | 第 3 讲。The transcribe image alone is 1.48 gigabytes → 光 transcribe 的 image 就有 1.48 GB。 |

### port_toy：网络 / port_toy: networks

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| network / a network you create / Docker's default network / built-in networks / toynet | 网络 / 默认网络 / 内置网络 / toynet | S10：从 README 的 Handy commands 里拿一条：docker network ls 把它列出来，旁边是 Docker 的三个内置网络。 | A13。Docker's default network has none → Docker 的默认网络没有电话簿。 |
| rail / the rail both containers will plug into | 导轨 | S10：Docker 打印出新网络的 ID：这就是两个 container 都要接上去的那根导轨。 | V6 里青色的导轨；量词“根”。不说“轨道”（像火车轨道）。 |
| little computer / its own little computer / its own full set of ports / without any clash | 小电脑 / 一整套 port / 冲突 | S10：把每个 container 想成一台独立的小电脑，有自己的 localhost，也有自己的一整套 port。 | V6。 |
| network namespace / isolated / until you wire it | 网络命名空间 / 隔离 | S10：这节课把这叫作网络命名空间：每个 container 都是隔离的，直到你把它们连起来。 | 这节课的术语（幻灯片第 33 页），只在 S10 的衔接句里说一次；和第 2 讲 PID 命名空间里的“命名空间”同一个词（内核意义上的）。until you wire it → 直到你把它们连起来。 |
| home network / a small home network / phone book / Docker's built-in phone book / turns names into addresses | 局域网 / 家里的小局域网 / 电话簿 / 内置的电话簿 | S10：你自己创建的网络把它们连起来，就像家里的小局域网，还带一本电话簿，把 container 名变成地址。 | V6（局域网）；电话簿就是 Docker 在 127.0.0.11 的 DNS，字幕里不说 DNS（英文也不说）。 |
| address / IP address / subnet / toynet's own address range, its subnet / addresses can change when a container restarts | 地址 / IP 地址 / 地址范围 / 子网 | S13：一个 container 重启时，地址可能会变；名字不会变。 | A13。 |
| gateway / processor / port toy / a web page / forwards your text / turns it into capitals | gateway / processor / port toy / 网页 / 转发 / 大写 | S10：这个 port toy 让两个 container 直接通信，而且只需要 Docker：一个 gateway 提供网页，把你的文字转发给一个 processor，processor 再把它变成大写。 | container 名照写（A1 a）；port_toy → port toy（A6）。processor ≠ 处理器（A7）。 |
| Prerequisites / docker run hello-world / Hello from Docker / checks that Docker is running | Prerequisites / hello-world / Hello from Docker | S10：先看 Prerequisites：用 docker run hello-world 检查 Docker 有没有在运行。 | B3：Hello from Docker 去掉感叹号。 |
| clone or download / prints no command / the README's tree | README 里的目录树 | S10：两个额外检查：文件和 README 里的目录树一致，一个 gateway，一个 processor；git log 显示这个视频 pin 住的 commit。 | the README says clone or download but prints no command → README 说 clone 或下载，却没给命令（画面上灰色的说明引用 README 的那一行）。 |
| slim Python 3.14 image / curl from apt / runs it with dash u / prints reach the logs at once | 精简版的 Python 3.14 image / -u / 日志 | S11：两个 Dockerfile 几乎一模一样：一个精简版的 Python 3.14 image，再从 apt 装上 curl。 | en_display：dash u → -u。 |

### port / Ports

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| port / ports / port 9200 / both use port 9100 | port / 端口（书面） | S01：第二个意外来自另一个教程：一个在 port 9200 上监听的服务器。 | A13：新进封闭清单；量词“个”；书面写“端口”。 |
| host port / container port / host side first | host port / container port / host 那一侧 | S11：顺序是 IP 地址、host port、container port：127.0.0.1，意思是只限这台笔记本，然后是 8090 号门，最后是 9100 号房间。 | A13：README 给 -p 三段起的名字。书面写宿主机端口 / 容器端口。 |
| publish / publishes a port / published / not published / dash p | 发布 / 发布出去的 port / -p | S11：这里的 -p 会发布一个 port：它在你笔记本上开一扇临街的门，通向 container 里面的一个房间。 | A13。listening, but not published → 在监听，但没有发布。 |
| listen / listens on 9200 / internal only / nothing on your laptop leads to it | 监听 / 只在内部 | S11：它在自己的盒子里监听 9200，但你笔记本上没有任何东西通向它。 | A13。 |
| street door / door 8090 / door 8091 / the room inside / room 9100 / doors on the laptop must be unique / rooms never collide | 临街的门 / 8090 号门 / 房间 / 9100 号房间 | S14：笔记本上的门必须各不相同；container 里的房间永远不会撞车。 | V7：门 = host port，房间 = container port；量词“扇”“个”。move your gateway's door → 把 gateway 的门挪过去。 |
| mapping / the gateway's mapping / the new mapping / PORTS column | 映射 / PORTS 那一列 | S13：而 processor 的 PORTS 那一列是空的：在监听，但没有发布。 | A13。PORTS 照写（列名）。 |
| temporary port / every connection has two ends / stapled it to the packet / destination | 临时 port / 连接 / 两端 / 数据包 / 目的地 | S12：它的操作系统挑了一个临时的，55620，把它钉在数据包上。 | A13。README 里的 ephemeral source port；书面写“临时源端口”。Yours will differ → 你的会不一样。 |
| operating system / nothing rewrites it inside the network / reads the sender's port | 操作系统 / 发送方 | S12：在 processor 那边，看到的是同一个数字，因为在网络内部没有任何东西会改写它。 | the sender's port → 发送方的 port。 |
| 127.0.0.1 / this laptop only / 0.0.0.0 / every address / other machines on your network / 127.0.0.11 | 只限这台笔记本 / 所有地址 | S13：用 8091 号门就成功了，映射显示 0.0.0.0：所有地址，所以你所在网络里的其他机器也能连进来。 | 地址写数字（C2）。 |
| localhost / whose localhost / its own localhost / localhost is the gateway itself / localhost 8090 | localhost / 谁的 localhost / 自己的 localhost | S13：在 gateway 里面，localhost 就是 gateway 自己，而它那里没有任何东西在 9200 上监听。 | A13。en_display：localhost 8090 → localhost:8090。 |
| port is already allocated / our gateway holds 8090 / the container was still created | port is already allocated / 占着 | S13：Docker 拒绝了，报 port is already allocated：我们的 gateway 占着 8090。 | 终端原文照写。 |
| can't connect / connection refused / nobody listens on 9200 anymore / a wrong name fails differently | 连不上 / 连接被拒绝 | S14：额外在 gateway 上跑一下 docker logs，就知道原因：它通过名字找到了 processor，但连接被拒绝了，已经没有人在 9200 上监听。 | 旁白是转述，中文也转述（画面上是 ConnectionRefusedError）。 |
| Empty reply from server / the captured request / no error handling / quietly | Empty reply from server / 错误处理 | S14：页面没有错误处理，所以上面什么都不会变；我们录下的那次请求只拿到 curl 的报错：Empty reply from server。 | It does, but quietly → 确实失败了，只是悄无声息。 |
| PORT / the processor's PORT / PORT set to 9200 / the gateway's processor port / the two settings must agree / configuration | PORT 变量 / processor port 这个变量 / 设置 / 配置 | S14：两个设置必须一致：processor 的 PORT，和 gateway 的 processor port。 | PORT 照写；PROCESSOR_PORT → processor port（A6）。It's only configuration → 这只是配置。 |
| hard-coded / trust docker ps and the page instead | 写死 | S14：那段文字是写死在第 53 行的。 | 实验课说法“写死”。 |
| browser / address bar / type a message / click Send / reply / in capitals / Processor's reply | 浏览器 / 地址栏 / Send / 回复 | S12：第 1 步的最后，在浏览器里打开 localhost:8090，输入一条消息，点 Send。 | 按钮名照写（A1 a）；click → 点（第 1 讲）。 |
| curl / request / the same request the page sends / we recorded without a browser | curl / 请求 | S12：我们录制时没有浏览器，所以用 curl 发了和网页一模一样的请求；这是它拿到的回复。 | 录到的 curl 代替了 Send 按钮（画面下方的 REPLY 条）；画面上不会把 curl 当成这一步来敲。 |
| docker exec / docker exec -it gateway sh / opens a shell inside / ok | docker exec / sh / ok | S13：用 docker exec 在 gateway 里面运行 curl，按名字 processor 去问 port 9200。 | The answer: ok. → 回答是：ok。en_display：dash i t → -it。 |
| name conflict / Conflict / clean up before Compose / only hello-world's old container left | 名字冲突 / Conflict | S14：跳过这一步，Compose 就会遇到名字冲突。 | 画面上是终端原文 Conflict；旁白说 name conflict → 名字冲突。 |

### Compose

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Docker Compose / Compose / docker-compose.yml / excerpt / the whole file | Docker Compose / Compose / docker-compose.yml / 节选 | S15：README 里只给了节选；把完整的 docker-compose.yml 打开。 | 产品名，可以放在句首（A5）。 |
| key / the volumes key / the depends on key / container name / ports / environment / networks / build | 键 / volumes 这个键 / depends on 这个键 / container name 这个键 | S15：有两个键是新的：volumes 这个键把 gateway 的目录挂载到 /app，depends on 这个键让 processor 先启动。 | YAML 的 key 是“键”（绝不说“密钥”，A7）。container_name、depends_on 按 A6。 |
| by-hand commands / has a home in it / the README's table / its Compose version / collapses into one command | 手动命令 / Compose 的写法 | S15：README 的那张表把每条手动敲的命令和它在 Compose 里的写法一一对应。 | Almost every flag you typed by hand has a home in it → 你手动敲过的参数，几乎每一个都能在里面找到位置。 |
| service / names them after the folder and the service / each line prefixed with its service | 服务 / 服务名 | S15：然后它创建网络和两个 container，打印出两个横幅，每一行前面都标着它的服务名。 | Compose 的 service → 服务（Docker 中文文档）；port_toy-gateway → port toy 加上 -gateway（A6）。banner → 横幅（第 1 讲）。 |
| docker compose up / up -d / up -d --build / docker compose down / docker compose ps -a / compose exec / compose logs -f | docker compose up / up -d / docker compose down / docker compose ps | S16：回到 README 的顺序：up -d 在后台启动应用，把提示符还给你。 | en_display：up dash d → up -d，dash a → -a，dash f → -f，dash dash build → --build。 |
| foreground / background / returns your prompt / follows the log / stops only the following | 前台 / 后台 / 跟踪日志 | S16：用 compose logs -f 持续跟踪 gateway 的日志；按 Ctrl-C 只停止跟踪。 | The prompt → 提示符（A7）。 |
| Control C / press Control C | Ctrl-C | S15：按 Ctrl-C 是停止；down 才是删除。 | B3：检查器拒绝 Ctrl+C；Ctrl-C 是另一种常见写法。en_display 写 Ctrl+C。 |
| stopping gracefully / Gracefully Stopping / about 20 seconds | 优雅地停止 | S15：Compose 说它正在优雅地停止，但要花大约 20 秒。 | “优雅停止”是 graceful shutdown 的标准中文说法。 |
| process / first process / the polite stop signal / unless it's written to catch it / kills it | 进程 / 第一个进程 / 礼貌的停止信号 / 强行杀掉 | S15：所以 Docker 对每个 container 等 10 秒，然后强行杀掉它。 | Python, each container's first process, ignores … → 作为每个 container 的第一个进程，Python 会忽略这个礼貌的停止信号，除非程序里专门写了捕获它的代码。 |
| exited / Exited / still there | 退出了 / Exited | S15：用 docker compose ps -a 一看：两个 container 都退出了，但还在那里。 | A5：英文以 Docker compose ps dash a 开头；中文先放一个中文词再接命令（用 docker compose ps -a 一看……）。en_display：dash a → -a。 |
| recreate / recreates only the gateway / apply / change it back and apply again / reload / rereads its page | 重新创建 / 生效 / 刷新 | S16：页面在 8095 上有回应；把它改回去，再让它生效一次。 | apply → 生效（绝不说“应用”，那是 the app；A7）。 |
| changed code that's copied into an image needs --build / only the copy layer is new / without a rebuild | 重新构建 | S16：那个 gateway 的目录是挂载进去的，而且它每次加载都会重新读页面：改动在下次刷新时就能看到，不用重新构建。 | en_display：dash dash build → --build。 |
| the images remain / sharing about 200 megabytes / remove them to free space | 约 200 MB | S16：这些 image 还在，共用大约 200 MB；删掉它们可以腾出空间。 | C2。 |
| the app / sets the app up by hand / starts the app in the background | 应用 | S10：第 1 步手动把应用搭起来。 | 第 1 讲：the app → 应用（概念）；字面名字 app（用户 app）照写。 |
| tear down / edit, apply, tear down, recap | 拆掉 / 拆除（书面） | S16：最后，docker compose down；ps -a 里什么都不剩。 | down removes the containers and the network → down 删除 container 和网络。 |

### 标签、进度条与固定句式 / Tags, tracker, fixed patterns

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the tracker / code panels / the yellow your-turn tag / gray extra tags / study guide / exercises | 进度条 / 代码面板 / your turn 标签 / extra 标签 / 学习指南 / 练习 | S01：看到黄色的 your turn 标签就暂停；灰色的 extra 标签表示 README 里没有的命令。 | A11：标签名照画面写（第 2、3 讲）。 |
| an extra check / extra checks / an extra command / not in the README / handy commands | 额外检查 / 额外的命令 / README 里没有 / Handy commands | S03：两个额外检查：git branch 显示，当前分支是 flexible-workflow，停在我们录制时的那个 commit；transcribe audio 里有 Dockerfile、这个脚本、pyproject.toml 和 uv.lock，就是你第 3 讲写过的那些。 | D6。the README's handy commands → README 的 Handy commands 一节（章节标题，A11）。 |
| at the time of recording / we recorded on Linux / One honest limit / we had no Google account | 录制时 | S01：我们是在 Linux 上录制的，录制时用的是 Docker Engine 29.8.2。 | A9：绝不省略。One honest limit → 有一点先说清楚（A8，第 3 讲）；we had no Google account → 我们录制时没有 Google 账号。 |
| with your key, look for / with your key, you'd see / what to look for / the real error a missing key gives | 报错 | S01：凡是代码调用 Google 的地方，你会看到命令、缺少密钥时的真实报错，以及该看什么。 | D6：with your key, look for → 有密钥的话，要找的是……；with your key, you'd see → 有密钥的话，你会看到……；what to look for → 该看什么；the real error a missing key gives → 缺少密钥时的真实报错。 |
| a small slip / a small gap / another small gap / a small inaccuracy / two small slips / one aside | 一个小疏漏 / 一个小缺口 / 一个小小的不准确 / 两个小疏漏 / 补充一句 | S13：补充一句：processor 的 image 里其实也有 curl，虽然 README 暗示它没有。 | A9：后面一定紧跟改法。 |
| Ponder this / the answer / solved | 来想一想 | S05：来想一想。 | 思考卡片在画面上是英文（A11）。问题绝不泄露答案（A9）。 |
| To test yourself / pause after each question / One: … Five: / Answers are in the exercises / Next lecture | 自测一下 / 每道题之后都暂停一下 / 第一题 / 第五题 / 答案在练习里 / 下节课 | S16：自测一下，每道题之后都暂停一下。 | D6。 |
| part 1 / part 2 / lecture 2 / lecture 3 / this lecture / next lecture / parts 1 and 2 together | 第一部分 / 第二部分 / 第 2 讲 / 第 3 讲 / 这节课 / 下节课 | S09：第二部分：互相直接通信的 container。 | A10。 |
| step 2 / step 3 of How to Run / the Quick Reference / step 1 sets the app up by hand | 第 2 步 / How to Run 那一节 / Quick Reference 那一节 | S07：回到 container 里，看 Quick Reference 那一节。 | A7、A11：README 的章节标题照写英文。 |

### 带下划线的名字（A6）/ Names with an underscore (A6)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| transcribe_audio / generate_text / synthesis_audio_en / translate_text / synthesis_audio (folders, images, components) | transcribe audio / generate text / synthesis audio en / translate text / synthesis audio | S06：现在 cd 进 transcribe audio，运行 docker-shell.sh，不带参数。 | A6，同第 3 讲；后面一定接中文名词，或放在一看就是名字的位置。 |
| input_audios / text_prompts / text_prompts/group-01 (bucket prefixes) | input audios / text prompts / text prompts 下的 group-01 | S07：有密钥的话，要找的是转写文本，然后是 text prompts 下 group-01 里的一个文本文件，本地和 bucket 里都有。 | A6。 |
| port_toy / port toy / port_toy-gateway / port toy, dash gateway | port toy / port toy 加上 -gateway | S15：Compose 构建了两个 image，全部用了缓存，并按目录名和服务名给它们命名：port toy 加上 -gateway。 | A6。S15：names them after the folder and the service → 按目录名和服务名给它们命名：port toy 加上 -gateway。en_display：port_toy-gateway。 |
| GOOGLE_APPLICATION_CREDENTIALS / GEMINI_MODEL / PROCESSOR_PORT / DOCKER_USERNAME / container_name / depends_on | 指向密钥的那个变量 / Gemini 模型变量 / processor port 这个变量 / Docker Hub 用户名 / container name 这个键 / depends on 这个键 | S15：原来的 --name 变成了 container name，构建命令变成了 build。 | A6。S15[1] 以 Dash dash name 开头：中文写“原来的 --name……”（A5）。 |

### 数字与单位 / Numbers and units

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| line 7 / lines 8 and 9 / line 23 / lines 13 and 14 / line 38 / line 32 / line 53 | 第 7 行 / 第 8 和第 9 行 / 第 23 行 / 第 53 行 | S06：第 7 行给 image 命名，container 也用这个名字。 | C1。 |
| ports and addresses: 8090 / 8091 / 8095 / 9100 / 9200 / 9300 / 55620 / 127.0.0.1 / 127.0.0.11 / 0.0.0.0 | 8090 / 9100 / 9200 / 127.0.0.1 / 0.0.0.0 | S12：再发一次，这个数字就变了：新的连接，新的临时 port。 | C2：写数字，绝不写汉字数字。 |
| versions: Python 3.8.17 / Python 3.14 / 3.14.8 / 3.14 or newer / Docker Engine 29.8.2 | Python 3.8.17 / Python 3.14 / 3.14 及以上 / Docker Engine 29.8.2 | S01：可这个 repo 的 Dockerfile 写的是 Python 3.14。 | C2；at the time of recording → 录制时（A9）。 |
| sizes and times: 1.48 gigabytes / about 200 megabytes / 8 seconds / about 50 seconds / under a second / about 20 seconds / 10 seconds per container | 1.48 GB / 约 200 MB / 8 秒 / 约 50 秒 / 不到 1 秒 / 约 20 秒 | S11：不到 1 秒就构建完了。 | C2。 |
| dates: February 18, 2025 / February 2025 | 2025 年 2 月 18 日 / 2025 年 2 月 | S01：这个 image 是 2025 年 2 月构建的，用的是 Python 3.8。 | C2。 |

### 课程、产品与名字 / Course, products, names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / Tutorial 0 / MLOps Learning / the study guide / the instructor / the other tutorial | AC215 / Tutorial 0 / MLOps Learning / 学习指南 / 授课老师 / 另一个教程 | S01：每条命令也都在学习指南里。 | A10。 |
| mega-pipeline / flexible-workflow / dlops-io / port_toy / student / app / root / laptop | mega-pipeline / flexible-workflow / dlops-io / student / app / root / 笔记本 | S08：提示符显示的是 root。 | A10。laptop → 笔记本（第 1 讲）。 |
| products: Google / Google Cloud / Speech-to-Text / Text-to-Speech / Vertex AI / Gemini / Docker / Docker Engine / Docker Hub / Docker Compose / BuildKit / Git / Git BASH / GitHub / Python / pipenv / uv / gcloud / ElevenLabs / Linux / Mac / Windows / Apple Silicon / JSON | Google / Google Cloud / Speech-to-Text / Text-to-Speech / Vertex AI / Gemini / Docker / Docker Engine / Docker Hub / Docker Compose / BuildKit / Git / Git BASH / GitHub / Python / pipenv / uv / gcloud / ElevenLabs / Linux / Mac / Windows / Apple Silicon / JSON | S01：在 Mac 或 Git BASH 里，提示符和少数几条消息会不一样；命令和 port 不会变。 | 拉丁字母（A1 b）。 |
| database / a command-line container / ChromaDB (L05) | 数据库 / 命令行 container | S16：下节课，一个命令行 container 会在 Compose 网络上，按名字调用一个数据库 container，用的还是同样的 secrets 挂载：第一部分和第二部分合在一起。 | 第 5 讲预告。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 中文 | 说明 |
|---|---|---|
| Video title | AC215 · 第 4 讲：容器 II-b——构建还是拉取、端口与 Compose（跟练：mega-pipeline flexible-workflow、port_toy） | H1。Containers II-b → 容器 II-b。 |
| Part 1 title / Part 2 title | AC215 · 第 4 讲（上）：flexible-workflow——你自己的云资源、一个脚本、构建还是拉取 / AC215 · 第 4 讲（下）：port_toy——网络、端口与 Compose | H1。 |
| Chapters S01-S09: Build or pull? Whose localhost? / Same pipeline, built like a team / Get the code: clone, or switch branches / Your bucket and your three values / Three gates: account, role, API / docker-shell.sh: one script, two windows / Five components, five honest errors / dev, run, and a stale image / prod, a stowaway key, and clean-up | 构建还是拉取？谁的 localhost？ / 同一条 pipeline，像团队一样搭建 / 获取代码：克隆，或切换分支 / 你的存储桶和三个值 / 三道关卡：账号、角色、API / docker-shell.sh：一个脚本，两扇窗 / 五个组件，五个真实的报错 / dev、run 和一个过期的镜像 / prod、偷渡的密钥与清理 | H1，书面语体。 |
| Chapters S10-S16: Two little computers, one network / Build, start, read the logs / Send a message: ports on the wire / Who can reach whom / Change the ports / Compose: the same app, declared / Edit, apply, tear down, recap | 两台小电脑，一个网络 / 构建、启动、看日志 / 发一条消息：线路上的端口 / 谁能连到谁 / 修改端口 / Compose：同一个应用的声明式写法 / 修改、生效、拆除与回顾 | H1。 |

### 配套材料的书面语体 / Written register of the companions

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| written register for the companions: container / image / base image / registry / bucket / bind mount / push / pull / repo / clone / commit / port / port mapping / ephemeral source port / host port / container port | 容器 / 镜像 / 基础镜像 / 镜像仓库 / 存储桶 / 绑定挂载 / 推送 / 拉取 / 仓库 / 克隆 / 提交 / 端口 / 端口映射 / 临时源端口 / 宿主机端口 / 容器端口 |  | H3、A4。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

AC、add、Admin、Agent、AI、allocated、already、amd、API、app、Apple、apt、arm、assert、AssertionError、audio、audios、base、BASH、bind、branch、bucket、build、BuildKit、buildx、CACHED、case、cat、cd、Change、Check、checkout、chmod、cli、cli.py、Client、clone、Cloud、Code、commit、Component、Compose、compose、config、Conflict、container、create、Creating、credentials、Ctrl-C、curl、d、default、DefaultCredentialsError、depends、dev、device、diff、dlops、dlops-io、Docker、docker、docker-compose.yml、docker-shell.sh、Dockerfile、dockerignore、ElevenLabs、Empty、en、enable、Engine、environment、exec、exit、Exited、extra、fetch、ffmpeg、File、file、flexible-workflow、found、from、gateway、GB、gcloud、Gemini、generate、Get、Git、git、GitHub、gitignore、Google、Gracefully、grep、group-、Handy、Hello、hello-world、help、home、host、How、Hub、IAM、ID、image、images、import、input、input-、inspect、IP、is、it、JSON、latest、Learning、Linux、Local、local、localhost、log、login、logs、ls、Mac、main、MB、mega-pipeline、mega-pipeline-sa、mega-pipeline.json、mount、mp、multi-arch、name、network、networks、not、ok、origin、pipeline、pipenv、pipenv-flexible-workflow、Pipfile、Platform、PORT、port、PORTS、ports、prefixes、Prerequisites、processor、prod、project、prompt、prompts、ps、pull、push、pwd、py、pyproject.toml、Python、python、Quick、README、README.md、Reference、registry、reply、repo、rm、root、Run、run、secrets、Send、server、services、set、sh、shell、Silicon、Speech、Speech-to-Text、stash、Step、Stopping、Storage、student、sync、synthesis、tag、test、text、Text-to-Speech、the、to、token、toy、toynet、transcribe、translate、Translation、TTY、turn、Tutorial、up、use、User、Using、uv、uv.lock、venv、Vertex、VM、volumes、was、Windows、winpty、your、your-project-id、your-team-bucket。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（git clone、git branch、git fetch origin、git checkout、git stash、git stash -u、git diff、git log、grep、ls、cd、cd ..、chmod、winpty、exit、python cli.py、./docker-shell.sh、docker-shell.sh dev / run / prod、docker build、docker run、docker images、docker image rm、docker inspect、docker exec、docker ps、docker ps -a、docker logs、docker login、docker network create、docker network ls、docker network inspect、docker buildx use default、buildx build、docker compose up、up -d、up -d --build、docker compose down、docker compose ps、docker compose ps -a、docker compose exec、docker compose logs -f、docker run hello-world、gcloud config set project、gcloud services enable、uv add、uv sync、pipenv shell、curl、sh）、参数（--branch、-u、--help、--rm、--name、--build、--use、-v、-e、-p、-it、-a、-f、-d）、文件和目录名（Dockerfile、docker-shell.sh、cli.py、pyproject.toml、uv.lock、mega-pipeline.json、docker-compose.yml、.gitignore、.dockerignore、Pipfile、README.md、test.mp3、secrets/、/app、/secrets、/secrets/mega-pipeline.json、/home/app/.venv）、分支 / image / 构建器 / 网络 / container / 账号的名字（main、flexible-workflow、pipenv-flexible-workflow、mega-pipeline、dlops、dlops-io、multi-arch、default、toynet、gateway、processor、hello-world、mega-pipeline-sa）、录制用的占位值（your-project-id、your-team-bucket、group-01）、docker-shell.sh 的模式（dev、run、prod）、Compose 的键（build、ports、environment、volumes、networks；container_name 和 depends_on 按 A6）、环境变量（PORT；带下划线的按 A6）、IAM 角色名（Storage Admin、Agent Platform User、Cloud Speech Client、Cloud Translation API User、Vertex AI User）、apt 软件包 ffmpeg（S07，同第 3 讲）、终端原文和报错名（DefaultCredentialsError、AssertionError、Using local image、Local image not found、Creating a Pipfile、the input device is not a TTY、port is already allocated、Empty reply from server、Conflict、Hello from Docker、Exited、ok）、旁白提到的屏幕标签（your turn、extra；A11）、浏览器按钮 Send 和 README 标题（Get the Code、How to Run a Component、Quick Reference、Prerequisites、Handy commands）。例外是带下划线的名字和检查器不收的字面形式（A6、B3）。（b）**产品、组织、课程和名字**：Google、Google Cloud、Cloud Storage、Speech-to-Text、Text-to-Speech、Vertex AI、Gemini、IAM、Docker、Docker Engine、Docker Hub、Docker Compose、Compose、BuildKit、buildx、Git、Git BASH、GitHub、Python、pipenv、uv、gcloud、ElevenLabs、Linux、Mac、Windows、Apple Silicon、amd64、arm64、JSON、IP、AC215、Tutorial 0、MLOps Learning、student、app。（c）**封闭清单**，中国 MLOps 工程师在实验课上口头就说英文的词：第 1 讲的 VM、venv、shell、root、repo、clone、commit、import、pin；第 2、3 讲的 container、image、Dockerfile、base image、registry、tag（打 tag）、push、pull、bucket、pipeline、bind mount、prompt（只指 LLM 的 prompt；shell 的 prompt 叫提示符）、API、ID；这一讲新增 port（host port、container port；A13）、localhost、stash（stash 一下、还在 stash 里）、checkout（checkout 成功了；git checkout 这个动作）、token（只指 LLM 的 token：Gemini 按 token 计费）、assert（Python 的语句：assert 会拦住你）。新词要进（c），必须同时满足：实验课上真的说英文；中文生硬、有歧义或和别的术语撞车。绝不为了“味道”加英文：不说 layer、build、cache、mount（动词）、builder、key、credentials、service account、role、permission、gate、network、subnet、address、connection、packet、publish、listen、mapping、request、reply、service（Compose）、key（YAML）、process、signal、exit code、folder、terminal、script、mode、branch、untracked、ignored、stage、component、flag。
- **[A2]** container 和 image（同第 2、3 讲）。字幕说 container 和 image，就像助教在实验课上说的：起一个 container、构建 image、image 里、container 退出时、本地 image、Docker Hub 上的 image；量词“个”（一个 container、两个 image、五个 image）。标题、章节名、meta.yaml 和配套文档写“容器”“镜像”（A4）。字幕里绝不写“镜像”（日常也指 mirror）。base image 照说（书面“基础镜像”）；registry 照说（书面“镜像仓库”）；Docker Hub 上的一个 repository 只在书面里叫“仓库”（第 2 讲）。image name → image 名；the dlops image → dlops 的 image；a stale image → 过期的 image；finished images → 做好的 image。
- **[A3]** Docker 的其他词说中文。build → 构建（构建 image、在本地构建、这次构建）；rebuild → 重新构建；build step k（BuildKit 的 [k/5]，青色徽标）→ 构建步骤 k，数字放在名词后面，免得像 README 的步骤（第 k 步，A7）；layer → 层（系统层、apt 那一层、COPY 那一层）；cache → 缓存，cached → 用了缓存（终端里的 CACHED 照写）；full log → 完整日志；writing out the image（导出）→ 写出 image；builder → 构建器（第 2 讲），a build engine → 构建引擎，processor types（CPU 的种类，S06、S09）→ 处理器类型 / 多种处理器（绝不写 processor，那是 port_toy 的 container，A7）；mount（动词）→ 挂载，both mounts → 两个挂载；名词 bind mount 照说；window（bind mount，第 3 讲）→ 窗；run → 运行 / 跑；start a container → 启动 container / 起一个 container；exit → 退出（exit 命令照写）；removed → 删掉；recreate → 重新创建；publish（image）→ 发布（push 到 Docker Hub），publish（port）→ 发布（A13）：英文两处都用 publish，中文也都用“发布”；pull → pull（第 2 讲），push → push，tag → tag / 打 tag，log in → 登录；using local image / local image not found 照终端原文写。
- **[A4]** 书面与口头配对。字幕说 repo / clone / commit / container / image / base image / registry / bucket / bind mount / push / pull / port；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 基础镜像 / 镜像仓库 / 存储桶 / 绑定挂载 / 推送 / 拉取 / 端口。the repo 作主语说“这个 repo”。命令本身不受影响（git clone、docker push 照写）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符都不变）；不翻译、不变形，不加引号、书名号或代码格式。需要时后面接一个中文名词：docker-shell.sh 这个脚本、uv sync 这条命令、secrets 目录、--rm 参数、toynet 这个网络、PORT 变量、volumes 这个键、Storage Admin 这个角色、COPY 那一行。句首不放实物，也不放保留英文的词，前面加一个中文词（输入 docker ps……；用 -p……；这个 docker-shell.sh……；而 git stash……；在 gateway 里面……），这样字幕也不会以小写字母开头。产品名和 README（课程里对这个文件的叫法）可以放在句首（Docker 拒绝了……；Compose 构建了两个 image……；Text-to-Speech 不需要角色；README 的提示解决的是第一个原因……）。
- **[A6]** 带下划线的名字，同第 3 讲。没有 say: 时，检查器把显示行当朗读文本检查，拒绝 letter_letter 形式（语音会念出“下划线”）。旁白念这些名字时也从不带下划线。所以中文行照旁白的说法写：下划线换成空格，和 SAY 一样小写，后面一定接一个中文名词，让人看出这是名字；英文只是指着它的地方，按角色称呼。对照：transcribe_audio → transcribe audio（目录 / 组件 / image）；generate_text → generate text；synthesis_audio_en → synthesis audio en（SAY 为了配音说 E-N）；translate_text → translate text；synthesis_audio → synthesis audio；input_audios → input audios 目录；text_prompts → text prompts；text_prompts/group-01 → text prompts 下的 group-01；port_toy → port toy（这个 repo / 目录）；port_toy-gateway → port toy 加上 -gateway；GOOGLE_APPLICATION_CREDENTIALS → 指向密钥的那个变量 / 路标；GEMINI_MODEL → Gemini 模型变量；PROCESSOR_PORT → processor port 这个变量（the gateway's processor port → gateway 的 processor port 变量）；DOCKER_USERNAME → 脚本里的 Docker Hub 用户名；container_name → container name 这个键；depends_on → depends on 这个键；group_name → 组名。含这种名字的命令（cd transcribe_audio、cd ../generate_text、cd port_toy）不写进中文行，改用描述（cd 进 transcribe audio 目录；cd 进 port toy），英文行由 en_display 给出字面命令（D4）。工具链允许显示行保留下划线以后（I1），把这些带空格的写法换回表中的字面形式。
- **[A7]** 易混词对。第 k 步（README 进度条的步骤；port_toy README 的 Step 1–4 各节，英文说 step 时也是）≠ 构建步骤 k（BuildKit 的构建步骤）。processor（port_toy 的 container，名字，照写）≠ 处理器（CPU：two processor types → 两种处理器）。gateway（container 的名字）≠ 关卡（S05 的 gate）。门（S05：API 的门；第二部分：笔记本上临街的门 = host port）≠ 房间（container 里的房间 = container port）≠ 窗（bind mount）≠ 窗口（终端或浏览器窗口）≠ Windows（操作系统）。盒子（把 container 或 image 画成盒子）≠ 配方（recipe：Dockerfile、pyproject.toml、uv.lock）。路标（S06 指向密钥的变量；S02 的 image tag）≠ tag（tag 本身）≠ 标签（画面上的视频标签：your turn 标签）。密钥（JSON 密钥文件）≠ 访问令牌（用它换来的短期令牌；Docker Hub 的 access token）≠ token（LLM 的 token：Gemini 按 token 计费）≠ 键（Compose / YAML 的 key：volumes 这个键）。服务账号（service account）≠ 账号（Google 或 Docker Hub 账号）≠ 服务（Compose 的 service；gcloud services 也叫服务）。身份（你是谁，第 1 关）≠ 角色（你能做什么，第 2 关）≠ 启用（API 打开了没有，第 3 关）。发布（publish：用 -p 发布 port，或把 image 发布到 Docker Hub）≠ 监听（listen）≠ 映射（docker ps 显示的 mapping）。host port ≠ container port ≠ 临时 port（S12 的 ephemeral source port）。localhost（一台机器对自己的称呼）≠ 127.0.0.1（回环地址，写数字）≠ 0.0.0.0（所有地址）。网络（Docker 网络）≠ 局域网（家庭网络的比喻）≠ 子网（它的地址范围）。地址（IP 地址）≠ 名字（电话簿解析的 container 名）。已跟踪 / 未跟踪 / 被忽略（Git 的三堆）≠ 拒绝（Git 拒绝 checkout）。丢弃（git checkout -- . 丢弃修改）≠ 收起来（git stash）≠ 删除（rm、docker image rm）。构建（build）≠ 生成（generate：Gemini 那一步）。转写 ≠ 翻译 ≠ 合成；上传 / 下载（往返 bucket）≠ push / pull（往返 Docker Hub），同第 3 讲。退出（exit 一个 container）≠ 停止（Ctrl-C）≠ 删除（down）≠ 清理（clean up）≠ 拆掉（tear down）。退出码（exit code / exit status）≠ 状态码（HTTP，第 1 讲）。应用（the app，概念，第 1 讲）≠ 生效（apply 一个改动：再执行 up -d 让它生效）。工作区目录（workspace，~/AC215）≠ 工作目录（WORKDIR，第 3 讲）≠ 组件目录（component folder）。提示符（shell 的 prompt）≠ prompt（Gemini 的 prompt）≠ 提示（hint；gcloud 提示……）。错误（泛指）≠ 异常（Python exception）≠ 报错（屏幕上的出错信息），同第 1 讲。
- **[A8]** 语体：助教带实验课。指令短，动词口语化（装、跑、删、敲、输入、改、切、挪）；称呼用“你”（跟练视频，一对一；不用“您”“大家”“同学们”）；“我们”指录制时的我们（我们录制时没有 Google 账号）。用中文语序，句子内部可以重组。避免翻译腔：不说“让我们……”（说“我们来……/ 先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不用“一个……的”长链。不用网络流行语。英文的口语节奏按意思转：One honest limit → 有一点先说清楚；Look closely at → 仔细看；Here's why → 原因是这样的；Starting fresh? → 从头开始？；Two puzzles → 两个谜题；the first puzzle, solved → 第一个谜题，解开了；It does, but quietly → 确实失败了，只是悄无声息；without a word → 一声不吭地；the first wall falls → 第一堵墙倒了；Nothing changed → 什么都没变；One aside → 补充一句；Back in the container → 回到 container 里；To finish → 最后；Why do this? → 为什么要这么做？
- **[A9]** 准确。限定语照译：only 只，every 每个，at once 马上，about 大约 / 约，nearly all 几乎全部，under 不到，or newer 及以上，may 可能，can take minutes 可能要几分钟，never 绝不 / 从不，almost 几乎，however old 不管多旧。at the time of recording 每次都译“录制时”，绝不省略（Docker Engine 29.8.2、Python 3.14.8）。版本、大小、个数、port、地址、行号、步骤号、构建步骤号和屏幕完全一致。勘误温和，而且一定紧跟改法：a small slip 一个小疏漏，a small gap 一个小缺口，a small inaccuracy 一个小小的不准确，two small slips 两个小疏漏。思考题（S05、S08、S13、S14；S07 的“Did it call Gemini?”）只问不答，措辞不能泄露答案：S05 不能说是哪一关失败；S08 不能提到 Python 3.8；S13 不能说没有人应答；S14 不能说是哪个变量，也不能说不用重新构建。钱：bill your project / your project pays → 记在你项目的账上 / 你的项目付钱；Speech-to-Text bills per audio minute → 按音频分钟数计费；Gemini bills per token → 按 token 计费。第 3 讲 A7 里挂载的说法有约束力：密钥从不被复制，/secrets 只在 container 运行时显示它。
- **[A10]** 名字。产品、公司、课程保持拉丁字母（A1 b）；“哈佛”只在标题和简介里出现。课程：AC215；lecture n → 第 n 讲（in lecture 3 → 在第 3 讲里；your clone from lecture 3 → 你第 3 讲的 clone）；next lecture → 下节课；this lecture → 这节课；part 1 / part 2 → 第一部分 / 第二部分；Tutorial 0 照写；the instructor → 授课老师（绝不出现名字：授课老师的组名只出现在没改动的终端原文里）；the course's project and bucket → 课程的项目和 bucket；the other tutorial → 另一个教程；this course's tool before uv → 这门课在 uv 之前用的工具。用户名 student、app、root，占位值 your-project-id、your-team-bucket、group-01 照写；container ID 从不念出来；a teammate → 队友；a real team → 真正的团队；your team → 你们组（课程里的团队就是组）。
- **[A11]** 屏幕保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（含注释）、README 卡片和小条、进度条（README › section，step k of N；port_toy README › …）、标签（your turn、extra、illustration、expected、erratum、recorded without a key、at the time of recording、stand-in file · not a real key、your numbers will differ、your project pays）、说明文字、示意控制台和 port_toy 的网页全是英文，场景不需要任何语言改动。所以旁白提到屏幕上的标签时，字幕照画面写：黄色的 your turn 标签、灰色的 extra 标签（第 1 讲写“轮到你了”，是因为它计划翻译屏幕标签；第 2、3 讲没有）。旁白用自己的话说的照常翻译：an extra check → 额外检查，the tracker → 进度条，code panels → 代码面板，the full log → 完整日志。旁白转述 README 时说“README 里说……”；旁白点名的 README 章节标题照写英文（Quick Reference 那一节、How to Run 那一节的第 2 步、Handy commands 里的命令、Prerequisites 一节）。
- **[A12]** 只做大陆简体：默认、程序、代码、文件、目录、服务器、网络、内存、磁盘、脚本、视频、用户名、信息、账号、令牌、地址、端口（书面）；不用預設、程式、程式碼、檔案、資料夾、伺服器、網路、記憶體、磁碟、腳本、影片、使用者、帳號、權杖、連接埠。
- **[A13]** port 和网络的词（这一讲新增）。port 进封闭清单：系列清单（ac215-video skill）保留它的英文，第 3 讲的 A13 写明后面几讲从那张清单取用，而这一讲的画面和命令里到处是它（PORTS 那一列、PORT 变量、ports 这个键、port is already allocated、README 的 Step 2: Check the ports 和 Step 3: Change the ports），字幕和观众盯着看的东西一致。量词“个”（一个 port；three port numbers → 三个 port 数字）；英文怎么排就怎么写：port 9200 或 9200 这个 port；英文说 listens on 9200 时写“监听 9200”。host port 和 container port 照说，它们是 README 给 -p 三段起的名字（IP 地址、host port、container port）；host 单独出现只在“host 那一侧”（host side first）。localhost 照写（字面的主机名）：whose localhost → 谁的 localhost；its own localhost → 自己的 localhost。其余网络的词说中文：network → 网络；a network you create → 你自己创建的网络；Docker's default network → Docker 的默认网络；built-in networks → 内置网络；subnet → 子网；address / IP address → 地址 / IP 地址；every address → 所有地址；this laptop only → 只限这台笔记本；connection → 连接；connect / can't connect → 连 / 连不上；the connection was refused → 连接被拒绝；packet → 数据包；publish（port）→ 发布；published → 发布出去的；listen / listening → 监听；internal only → 只在内部；mapping → 映射；temporary port → 临时 port；destination → 目的地；request → 请求；reply → 回复；hostname → 主机名；other machines on your network → 你所在网络里的其他机器；bind（port，S16）→ 绑定。书面语体（标题、meta.yaml、文档）：端口、端口映射、发布的端口、监听端口、临时端口（README 的 ephemeral source port：临时源端口），host port / container port 旁边写宿主机端口 / 容器端口。
- **[A14]** 这一讲没用到的系列词。系列清单里的 volume 只作为 Compose 的键 volumes 出现（实物：volumes 这个键；gateway 的目录是“挂载”进去的，中文里从不叫 volume）；PATH 没有出现（文件的 path 是“路径”：build paths from pwd → 用 pwd 拼出路径；the key's path → 密钥的路径）；agent 只出现在角色名 Agent Platform User 里；endpoint、embedding、LoRA、CI 都没说。第 5 讲（ChromaDB、embedding）从那张清单取用。

### B. 排版

- **[B1]** 空格。中文和拉丁字母、数字、实物之间加一个半角空格（输入 docker ps、Python 3.14、第 9 行、port 9200、8090 号门、1.48 GB、secrets 目录、container 里）。检查器对每个显示句都会报缺失的空格。实物内部的空格照原样（docker compose up -d），实物内部绝不加空格。全角标点旁不加空格（……cd 进 port toy。、用户 app，）。不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，实物旁边也一样（输入 exit。）。列举用顿号（Dockerfile、pyproject.toml 和 uv.lock）。任何括号都不用：（）、()、《》、【】、<> 都不用，因为没有 say: 时检查器拒绝括号，双语字幕带也不需要括注。“”只用于中文里引用的想法或词（问它“你是谁”）；实物、标签名和终端原文不加引号。一个中文句子内部不出现。？！（一个英文句子对应一个中文句子），改用，；：。“第 N 步”“构建步骤 N”后面接说明时用全角冒号。问句保留？。
- **[B3]** 检查器拒绝的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后面跟 !、括号、letter_letter）不抄进中文行，改用文字说或换一种写法。Ctrl+C → Ctrl-C（这个键的另一种常见写法，检查器也收；英文行由 en_display 显示 Ctrl+C）；chmod +x → 用 chmod 加上可执行权限 / chmod 那一步；占位符 <your-project-id> → 占位符，它的尖括号 → 尖括号；$(pwd) → pwd；git checkout -- . → git checkout 加上 -- 和一个点（混在全角标点里，单独一个点看不出来，第 2 讲）；3.14 or newer → 3.14 及以上（不写 >=3.14）；Hello from Docker! → Hello from Docker（去掉感叹号，句子以。结尾）。允许并照屏幕保留的：路径里的 /（/secrets/mega-pipeline.json、cd ..）、文件名和地址里的 .（127.0.0.1、127.0.0.11、0.0.0.0）、地址加 port 的 :（localhost:8090、-p 127.0.0.1:8095:9100）、参数和名字里的 -、@（@ 符号后面）；用不到 *（git branch：星号在 flexible-workflow 上）。

### C. 数字、版本号与单位

- **[C1]** 显示文字里的数字。和屏幕、终端、代码对应的一律用阿拉伯数字：步骤号（第 2 步、第 5 步）、构建步骤（构建步骤 2）、行号（第 7 行、第 8 和第 9 行、第 13 和第 14 行、第 53 行）、关卡编号（第 1 关、第 2 关、第 3 关：画面上的关卡带编号）、port（8090、8091、8095、9100、9200、9300、55620）、地址（127.0.0.1、127.0.0.11、0.0.0.0）、退出码（退出码 0、退出码 137）、用户 ID、版本、大小、时间、日期、group-01。叙述中的小数目和序数用汉字：两个谜题、三个值、五个文件、四个角色、五个 API、三道关卡、三堆、两个原因、两扇窗、两个 image、两个 container、三个额外检查、第一个谜题、第一部分 / 第二部分、第一题……第五题。英文用单词说、屏幕上是数字的，跟屏幕；屏幕上没有的，跟英文（all five → 五个都跑一遍；both → 两个都）。
- **[C2]** 单位、版本、port 和日期。大小照屏幕写，加半角空格：1.48 GB、约 200 MB。时间：8 秒、约 50 秒、不到 1 秒、约 20 秒、每个 container 10 秒、可能要几分钟。版本带名字：Python 3.8.17、Python 3.14、3.14.8、Docker Engine 29.8.2、uv 0.13.0。范围：3.14 及以上。port 和地址写数字，绝不写汉字数字：port 9200、8090 号门、9100 号房间、127.0.0.1、0.0.0.0、127.0.0.11；带 port 的地址照屏幕写：localhost:8090（SAY 说 localhost 8090）。日期：2025 年 2 月 18 日（February 18, 2025）、2025 年 2 月（February 2025）。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每个 SAY 行一条（156 段）；`en` 和 SAY 行逐字节相同；`zh` 按 explainer.voice.split_sentences 的切分，每个英文句子正好一项（这份脚本共 372 句）。只在句子内部重组，绝不合并或拆分。短句也单独一项：Ponder this. → 来想一想。；Pause and run it. → 暂停一下，自己跑一遍。；Pause and switch. → 暂停一下，切换过去。；Two puzzles. → 两个谜题。；Three piles. → 分成三堆。；Nothing. → 什么都没有。；Run it. → 运行它。；Here's why. → 原因是这样的。；No. → 没有。反复运行 `python -m explainer.i18n check videos/ac215-l04-flexible-workflow-ports --lang zh`，直到打印 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（锚点只给中文配音版安排动画节拍）。字幕按英文音频计时；工具链按位置把每个中文句子和对应的英文句子配对。
- **[D3]** 过得了检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：没有括号（B2）、没有数学符号（B3）、没有 letter_letter 名字（A6）、数字后面没有 !、没有以“种”结尾再接，。！？的分句（改写：两种方式。→ 有两种方式拿到。或 两个办法。）、汉字和拉丁字母或数字之间有半角空格（B1）、每句以。！？或……结尾（后面可以跟”或」）、每个拉丁词都在本词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用正则 `[A-Za-z][A-Za-z'.-]*` 切词：group-01 切成 group-，amd64 切成 amd，arm64 切成 arm，input-….mp3 切成 input- 和 mp，/home/app/.venv 切成 home、app 和 venv，Ctrl-C 是一个词。它报出的拉丁词，要么是该翻译的英文词（通常如此），要么是漏收的实物：按同样的切法把它加进 allowed_spoken_latin，并加进对应的术语条目。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都写一项 en_display，显示屏幕上的字面形式，其余部分和 SAY 句子逐词一致；同一段里的其他句子写 null。这份脚本的念法 → 字面形式：dash dash branch → --branch；git stash dash u → git stash -u；git checkout dash dash dot → git checkout -- .；git branch: star, flexible-workflow → git branch: * flexible-workflow；test dot mp3 → test.mp3；input, dash, something, dot mp3 → input-something.mp3；dash v / dash e / dash p / dash u / dash i t / dash a / dash f → -v / -e / -p / -u / -it / -a / -f；up dash d → up -d；dash dash r m / dash dash name / dash dash build / dash dash use → --rm / --name / --build / --use；chmod plus x → chmod +x；slash app / slash secrets → /app / /secrets；file slash secrets slash mega-pipeline.json → File /secrets/mega-pipeline.json；default credentials error → DefaultCredentialsError；text prompts, slash group-01 → text_prompts/group-01（观众要找的路径）；the at sign → @；T-T-Y → TTY；localhost 8090 → localhost:8090；pipenv flexible workflow → pipenv-flexible-workflow；port toy, dash gateway → port_toy-gateway；Control C → Ctrl+C；dash p 127.0.0.1, 8095, 9100 → -p 127.0.0.1:8095:9100。段落（扫描 v2 脚本得到；脚本改了就重扫）：S03[0,8,9] S04[6,7] S06[4,5,8,9,10] S07[0,2,8,13] S08[9] S09[0,2,3,6] S11[0,3,4,5] S12[0] S13[10] S14[3] S15[1,2,3,8,10,11] S16[0,1,2,4,6,9]。带下划线的名字（A6）只在观众要输入或要找的路径和命令里（text_prompts/group-01、port_toy-gateway；S07[8] 的 synthesis_audio_en 可以保留念法）在 en_display 里写回字面形式；单纯提到时，两行都保留 SAY 的说法（transcribe audio、port toy、container name、depends on、the gateway's processor port）。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它对应的英文句子：不加命令、参数、括注、中文控制台名或解释；“额外”只用在英文标了 extra 的地方；保留英文的词不加中文解释（英文行就在正下方）。
- **[D6]** 固定句式：
  - Pause and run it. → 暂停一下，自己跑一遍。Pause and run both. → 暂停一下，两条都跑一遍。Pause and run them. → 暂停一下，把它们跑一遍。
  - Pause and try dev and run yourself. → 暂停一下，自己试试 dev 和 run。Pause and switch. → 暂停一下，切换过去。Pause and edit them. → 暂停一下，把它们改好。
  - Pause, and set up your account, key and APIs. → 暂停一下，把账号、密钥和 API 都设置好。Pause, and run all five with your key, checking the bucket after each. → 暂停一下，用你的密钥把五个都跑一遍，每跑完一个就看看 bucket。Pause and check yours. → 暂停一下，检查你自己的。
  - Pause, and create yours. → 暂停一下，创建你自己的网络。Pause and create yours.（S04，bucket）→ 暂停一下，创建你自己的 bucket。Pause and start both. → 暂停一下，把两个都启动。Pause, send a message, and leave both running. → 暂停一下，发一条消息，两个都别停。Pause, and test from both sides. → 暂停一下，从两边都试一试。
  - Pause and move your gateway's door. → 暂停一下，把你的 gateway 的门也挪过去。Pause and fix yours. → 暂停一下，把你的也修好。Pause and clean up. → 暂停一下，清理干净。Pause, and run the whole cycle. → 暂停一下，把整个流程跑一遍。Pause and shut it down. → 暂停一下，把它关掉。
  - Pause at the yellow your-turn tag → 看到黄色的 your turn 标签就暂停；gray extra tags mark commands the README doesn't have → 灰色的 extra 标签表示 README 里没有的命令。
  - An extra check / Two extra checks / Three extra checks inside / Another handy command / An extra … → 一个额外检查 / 两个额外检查 / 在里面做三个额外检查 / 再来一条 Handy commands 里的命令 / 额外的……
  - Ponder this. → 来想一想。Step N: / Step N, … → 第 N 步：/ 第 N 步，……
  - With your key, look for … → 有密钥的话，要找的是……；With your key, you'd see … → 有密钥的话，你会看到……
  - A small slip: / A small gap: / Another small gap: / A small inaccuracy: / Two small slips. → 一个小疏漏：/ 一个小缺口：/ 还有一个小缺口：/ 一个小小的不准确：/ 两个小疏漏。One aside: → 补充一句：
  - To test yourself, pause after each question. → 自测一下，每道题之后都暂停一下。One: … Five: → 第一题：……第五题：Answers are in the exercises. → 答案在练习里。Next lecture, … → 下节课，……In part 2: … → 第二部分：……Every command is also in the study guide. → 每条命令也都在学习指南里。
- **[D7]** 文件。narration/g1.yaml = S01–S09（第一部分，mega-pipeline flexible-workflow），narration/g2.yaml = S10–S16（第二部分，port_toy），和 video.yaml 的 parts 一致；每个文件开头一段注释（覆盖哪些场景、用到的规则：A6 带空格的名字、B3 写成文字的符号、D4 en_display、没有 say: / anchors），按脚本顺序排列。字符串用双引号；字面的双引号或反斜杠按 YAML 转义。
- **[D8]** 按英文时间轴的长度。中文是在听英文的同时读的，字幕带在英文分段处切换（读得比每秒 9 个单位还快的中文片段，最多多给 1 秒）。每个中文句子读起来的时间要和英文听起来差不多：经验上每个英文单词最多约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也算数（DefaultCredentialsError 是 12.7 个单位，/secrets/mega-pipeline.json 14.9，Cloud Translation API User 14.3）：英文没有重复的地方，中文不要重复；长的终端消息按关键字转述（报 DefaultCredentialsError：找不到 /secrets/mega-pipeline.json 这个文件）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一条最多 2 行。分句尽量不超过 24 个单位，用，；：隔开，让切分程序有干净的切点；避免超过 30 个单位又没有标点的分句。
- **[G2]** 字幕结尾：工具链会去掉字幕条末尾的。，、；：，保留？！……和收尾的”（subtitles.strip_end）。能用中文词收尾的，就不要以“实物 + 句号”结尾（“……的 toynet 网络。”比“……toynet。”好读，但两种都合法）。
- **[G3]** 命令不能断开。切分程序把中文行里两个拉丁词之间的空格当成好切点，所以 docker network create toynet 可能被拆到两行，观众就没法照抄了。把整条命令放在分句末尾、全角冒号之后（第 2 步：git fetch origin。），一条字幕最多一条命令，周围的中文要少；一行放不下的命令（带 URL 的 git clone --branch flexible-workflow、S11 的 docker run、带五个 API 的 gcloud services enable）不完整写进中文行：照旁白的说法点名（git clone，加上 --branch flexible-workflow；用 gcloud services enable 这条命令把五个都打开），让终端和英文行显示它。在渲染出来的 .zh.srt 里检查每一条带命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、分部分和章节标题用书面语体（A4：容器、镜像、仓库、克隆、拉取、推送、端口、存储桶）；问句保留问号；保留英文的冒号结构（docker-shell.sh：……、Compose：……）；命令、模式名、分支名、目录名和文件名照写，下划线也保留（meta.yaml 不经过检查器，括号也可以用）。Containers II-b → 容器 II-b（第 2 讲容器 I，第 3 讲容器 II）。章节名按英文的意思译，不逐字：S07 five honest errors → 五个真实的报错（五个里有一个是悄无声息的退出码 0，但仍是真实的结果）；S09 a stowaway key → 偷渡的密钥；S12 ports on the wire → 线路上的端口；S15 declared → 声明式写法。
- **[H2]** 简介（B 站 / YouTube）：两三句话，书面语体，用本词表的术语：这是 AC215 第 4 讲 dlops-io/mega-pipeline（flexible-workflow 分支）和 dlops-io/port_toy 的跟练视频；观众要做什么、学到什么（自己的服务账号、密钥和存储桶；三道关卡；docker-shell.sh 和它的模式；构建还是拉取、过期的镜像；别让密钥进镜像；每个容器自己的 localhost、Docker 网络上的名字、发布的端口和监听的端口、-p；Compose）；英文旁白配中文和中英双语字幕，终端输出录于 2026-10-14，录制时没有 Google 账号。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md / digest.md）用本词表的书面语体翻译（仓库、克隆、提交、容器、镜像、基础镜像、镜像仓库、存储桶、推送、拉取、端口、端口映射、绑定挂载（bind mount）、服务账号、访问令牌、临时源端口）；那里可以用括号和下划线（不经过检查器）。标题和 `<summary>答案</summary>` 要翻译。末尾附一张术语表：English | 这里的译法 | 常见变体（端口 / port、宿主机端口、容器端口、镜像仓库 / 注册表、服务帐号 → 服务账号、优雅停止）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 照原样；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直开着）`explainer.i18n check` 在句子没有 say: 时，把语音检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）用在显示行上。对只有字幕的视频（这个系列；video.yaml 没有 languages.zh.voice，词表写 voice: none），这些检查保护不了任何东西，反而逼出了 A6 和 B3（这一讲：Ctrl-C 代替 Ctrl+C、chmod 要描述、port_toy 写成 port toy）。建议：词表的 voice 为 none 时，显示句跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。到那时 A6 和 B3 改为：字面形式照写（port_toy 目录、Ctrl+C、chmod +x）。
- **[I2]**（待办，来自第 1 讲的 I3）explainer/subtitles.py 的 _cuts 把中文行里拉丁词之间的空格当成好切点，命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词不可切分，除非它本身超过一行。
