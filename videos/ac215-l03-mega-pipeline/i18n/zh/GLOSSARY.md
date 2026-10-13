# AC215 第 3 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 3 — Containers II: five containers, one bucket (follow-along: mega-pipeline)*（`videos/ac215-l03-mega-pipeline`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，英文技术文档读得很顺；做过第 1 讲（VM、venv、uv）和第 2 讲（现成的 Dockerfile、image 和 container 的区别、层缓存、Docker Hub），这次第一次自己写 Dockerfile；在自己的笔记本上开着 mega-pipeline 的 README，边看边敲命令  
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l03-mega-pipeline.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长，只有显示规则  
英文原稿：`script.md` v2（SAY 行是旁白：158 段、310 句；SHOW 行是画面）  
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md)。L1 已经定下的词沿用 L1 的写法；改动的两处（container / image、屏幕标签名）在规则里写明理由（A2、A11）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“起一个 container”“构建 image”“把 repo clone 下来”“push 到 Docker Hub”“看 bucket 里你们组的抽屉”“激活 venv”。硬译成“启动容器实例”“推送至镜像仓库”，反而像说明书。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端和代码里找东西。命令、参数、文件名、路径、包名、Dockerfile 指令、报错原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（构建、层、缓存、挂载、目录、终端、提示符、包、依赖、密钥、服务账号、凭据、身份验证、授权）一律说中文；Google Cloud 的概念用中文文档的官方译名（服务账号、应用默认凭据、存储桶），方便搜索。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列没有中文配音：画面上的一切（终端、代码面板、README 卡片、标签、进度条）都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众是上 AC215 的中文研究生：英文技术文档读得很顺，平时就说“起一个 container”“构建 image”“把 repo clone 下来”“push 到 Docker Hub”“激活 venv”。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（Docker 和 Google Cloud 的中文文档）；和系列试点（L1）一致。（1）**实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件和目录名、路径、包名、配置项、Dockerfile 指令、终端原文和报错名、屏幕上的标签、README 标题）逐字照抄，不翻译、不变形、不加引号；唯一的例外是检查器逼出来的：带下划线的名字按旁白的说法写（A6）。这个系列不翻译屏幕：终端输出、代码面板、README 卡片、标签和进度条都是英文，只翻译旁白。（2）**实验课口语里的英文**，封闭清单：沿用 L1 的 venv、shell、root、repo、clone、commit、import、traceback、lock 文件；容器这几讲新增 container、image、Dockerfile、bucket、pipeline、bind mount、push、tag（打 tag）、prompt（只指 LLM 的 prompt）、API、ID。（3）**其余一律用中文标准术语**：构建、重新构建、构建步骤 k、构建上下文、构建参数、层、可写层、缓存、挂载、工作目录、指令、配置卡片、目录、终端、提示符、包、软件包、依赖、激活、解析、密钥、服务账号、凭据、应用默认凭据、访问令牌、身份验证、授权、客户端、请求、对象名、前缀、阶段、组件、组名、排行榜、转写、合成、翻译、播客。（4）**视频自己的比喻按意思译**，一个比喻一个词：柜子和抽屉（bucket）、窗（bind mount）、路标（指向密钥的变量）、取件单（长时间运行的操作）、包裹和多米诺骨牌（来自第 2 讲）、清单和小票（pyproject.toml 和 uv.lock，来自第 1 讲）。（5）标题、meta.yaml 和配套文档用**书面语体**：仓库、克隆、提交、容器、镜像、存储桶、推送、绑定挂载。（6）双语字幕带在每行中文下面放英文原句，所以中文行**不加括注，任何括号都不用**（没有 say: 时检查器禁止括号）。（7）工具链的约束也是规则：每个英文句子对应一个中文句子（158 段、310 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）。大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **container / image 说英文，书面写容器 / 镜像**。L1 的规则是“容器、镜像说中文”，但 L1 只在最后几句预告里提到它们（那几句实际上是书面语体）。从这一讲起它们是每句都挂在嘴上的词，实验课上就是“起一个 container”“构建 image”；而且“镜像”日常也指 mirror（L1 叫软件源）。所以字幕说 container / image（量词“个”），标题、章节名、meta.yaml 和配套文档写“容器 / 镜像”（A2、A4）。系列清单（ac215-video skill）也把这两个词列为保留英文。
- **其余 Docker 的词说中文**：build → 构建，layer → 层，cache → 缓存，mount（动词）→ 挂载，build context → 构建上下文，build argument → 构建参数，working folder → 工作目录，instruction → 指令。只有 bind mount 这个名词照说英文（A3）。
- **两种“步骤”分开**：README 进度条的步骤是“第 k 步”；BuildKit 的 [k/5] 是“构建步骤 k”，数字放在后面，永远不会被看成 README 的步骤（A3、A7）。
- **挂载从不“复制”**：bind mount 是一扇窗，写在 /app 下面的东西“直接写进你笔记本上的目录”，绝不说“复制回去”“同步回去”（A7、A9）。
- **带下划线的名字按旁白的说法写**：没有中文配音时，检查器把显示行当朗读文本检查，会拒绝 letter_letter 形式（语音会念出“下划线”）。旁白本来也不念下划线（transcribe audio、text prompts、uv project environment、the key variable），所以中文行照旁白写，后面接一个中文名词（transcribe audio 目录、text prompts 抽屉、uv project environment 这个变量）；带这种名字的命令不写进中文行，由 en_display 在英文行给出字面命令（A6、D4）。工具链放开这条检查以后（I1），换回字面形式。
- **不用括号，符号用文字说**：同样因为检查器，中文行里没有（）、()、《》、【】；双语字幕带也不需要括注（B2）。写“3.11 及以上”，不写 >=3.11（B3）。
- **屏幕不翻译**：这个系列只翻译旁白，所以旁白提到屏幕上的标签时，字幕照画面写：黄色的 your turn 标签、灰色的 extra 标签（L1 写“轮到你了”“额外”，是因为它计划翻译屏幕标签）。旁白用自己的话说的照常翻译：额外检查、进度条、代码面板（A11）。
- **沿用 L1 和 L2 的比喻**：清单 / 小票（pyproject.toml / uv.lock）、用完就扔（可写层）、包裹（构建上下文）、多米诺骨牌（缓存失效）。这一讲新造的比喻各用一个词：柜子和抽屉、窗、路标、取件单；取件单和小票不能混（A7）。
- **密钥、访问令牌、凭据分开**：密钥 = key 文件；访问令牌 = 用密钥换来的短期 token（Docker Hub 的 access token 也叫访问令牌）；凭据 = 认证库要找的 credentials；应用默认凭据（ADC）是那个查找过程（A7）。
- **勘误温和、紧跟改法**：一个小错误 / 一个小疏漏 / 一个无害的小疏漏 / 一个小缺口，后面一定跟着改法（A9）。
- **录制时**：at the time of recording 每次都译“录制时”，绝不省略（A9）。
- **按英文时间轴读**：中文是边听英文边读的，每句中文读起来的时间要和英文听起来差不多；删掉多余的连接词和重复的主语，绝不删内容（D8）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令、参数、文件名和路径、包名、Dockerfile 指令（FROM、ARG、ENV、RUN、USER、WORKDIR、COPY）、配置项、终端原文和报错名、旁白提到的屏幕标签（your turn、extra）、README 标题（Appendix）。完整清单见 A1（a）；带下划线的名字例外（A6）。
- 产品、组织、课程和名字：Google Cloud、Cloud Storage、Speech-to-Text、Text-to-Speech、Vertex AI、Gemini、IAM、ADC、Docker Desktop、Docker Engine、Docker Hub、VS Code、Git BASH、PowerShell、Canvas、GitHub、Debian、PyPI、ElevenLabs、AC215、Tutorial 0、MLOps Learning、mega-pipeline、dlops-io、group-01、student、app，等等（A1 b）。
- 实验课口语，封闭清单：venv、shell、root、repo、clone、commit、import、traceback、lock 文件（沿用 L1）；container、image、Dockerfile、bucket、pipeline、bind mount、push、tag（打 tag）、prompt（只指 LLM 的 prompt）、API、ID（容器这几讲新增）。
- 系列清单里保留英文、但这一讲没用到的：port、volume、PATH、endpoint、embedding、agent、LoRA、CI（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| build / rebuild | 构建 / 重新构建 | build step k（BuildKit） | 构建步骤 k |
| step k（README） | 第 k 步 | build context | 构建上下文 |
| build argument（ARG） | 构建参数 | instruction | 指令 |
| layer / writable layer | 层 / 可写层 | cache / cached | 缓存 / 用缓存 |
| mount（动词） | 挂载 | working folder（WORKDIR） | 工作目录 |
| config card | 配置卡片 | live view / full log | 实时视图 / 完整日志 |
| folder | 目录 | terminal / prompt（shell） | 终端 / 提示符 |
| package（Python / apt） | 包 / 软件包 | dependency / resolve | 依赖 / 解析 |
| activate | 激活 | flag / argument | 参数 |
| environment variable | 环境变量 | relative path | 相对路径 |
| key / key file | 密钥 / 密钥文件 | service account | 服务账号 |
| credentials | 凭据 | application default credentials | 应用默认凭据（ADC） |
| access token | 访问令牌 | auth library / client | 认证库 / 客户端 |
| authentication / authorization | 身份验证 / 授权 | IAM roles | IAM 角色 |
| request / response / call | 请求 / 响应 / 调用 | long-running operation | 长时间运行的操作 |
| object name / prefix | 对象名 / 前缀 | billed / quota | 计费、记在……的账上 / 配额 |
| stage / component | 阶段 / 组件 | group name | 组名 |
| leaderboard | 排行榜 | naming contract | 命名约定 |
| transcribe / transcript | 转写 / 转写文本 | generate | 生成 |
| translate / synthesize | 翻译 / 合成 | podcast script | 播客稿 |
| upload / download | 上传 / 下载 | exit / remove / clean up | 退出 / 删除 / 清理 |
| at the time of recording | 录制时 | an extra check | 额外检查 |
| the tracker / code panels | 进度条 / 代码面板 | Ponder this. | 来想一想。 |
| cabinet / drawer | 柜子 / 抽屉 | window（the bind mount） | 窗 / 这扇窗 |
| signpost | 路标 | ticket stub | 取件单 |
| the list / the receipt | 清单 / 小票 | throwaway | 用完就扔 |
| parcel / dominoes | 包裹 / 多米诺骨牌 | bake it in | 打包进 image |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句，每一句都能通过检查器。这个系列没有中文配音，所以没有 L1 的“朗读（say:）”一栏。


### 容器、镜像与构建 / Containers, images, builds

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| container / containers / in its own container / inside the container / five containers | container / 容器（书面） | S01：五个程序，各自在自己的 container 里，把它变成英文和法文的播客，彼此之间从不发一条消息。 | 实验课口语（A2），量词“个”。标题、meta.yaml 和配套文档写“容器”（A4），和 L1 一致。不译“集装箱”。 |
| image / images / five images / the image's Python / the official Python 3.12 image | image / 镜像（书面） | S01：你要自己写 Dockerfile，而且要构建五个 image，而不是一个。S05：第 1 行从 Debian 12 上的官方 Python 3.12 image 开始。 | 实验课口语（A2）。字幕里不写“镜像”（日常也指 mirror）；书面写“镜像”。image name → image 名；the image's own Python → image 自带的 Python。 |
| container ID / the container's ID / user ID 1000 | container ID / 用户 ID 1000 | S07：@ 符号后面是 container 的 ID，每次运行都不一样。 | ID 照说英文（实验课口语）。ID 本身从不念出来。 |
| Dockerfile / write the Dockerfile / a file named Dockerfile, with no extension | Dockerfile / 一个名叫 Dockerfile、没有扩展名的文件 | S05：第 4 步是这节课的核心：这里没有 Dockerfile，所以你要自己写，一块一块地拼起来。 | 文件名，也是课程里的说法；量词“个”。复数 Dockerfiles → 这些 Dockerfile（英文词不变形，L1 的 A7）。 |
| build / builds the image / the build / rebuild / rebuild the image | 构建 / 重新构建 / 这次构建 | S06：第 5 步构建 image。S11：README 给的办法是：退出，然后用同一条 docker build 命令重新构建 image。 | A3。docker build 命令照写。字幕里不说 build（命令里的除外）。 |
| build step / build step 2 / build steps 1 to 3 / the five build steps | 构建步骤 / 构建步骤 2 / 构建步骤 1 到 3 / 五个构建步骤 | S06：构建步骤 2 是我们那个大 RUN：apt 装了 237 个软件包，下载了 205 MB，然后 pip 装好 uv，一共 46.9 秒。 | BuildKit 的 [k/5]，画面上青色（TEAL）的 build step k 徽标。数字放在名词后面；README 的步骤永远是“第 k 步”（A7）。 |
| build context / the build context | 构建上下文 | S06：最后一个点代表当前目录，也就是构建上下文。 | Docker 中文文档的译名。第 2 讲的比喻：包裹。 |
| build argument / ARG / a variable that exists only during the build | 构建参数 / 只在构建期间存在的变量 | S05：第 3 行声明了一个构建参数，一个只在构建期间存在的变量：Debian 软件包 build-essential 和 ffmpeg。 | 和“参数”（flag）、“环境变量”（ENV）分开。它的名字 DEBIAN_PACKAGES 不写出来（A6）。 |
| layer / one layer / no layers / the biggest layer / one fat layer / B's big layer | 层 / 一层 / 不产生层 / 最大的一层 / 一个特别大的层 | S05：和第 2 讲一样，它们只写在配置卡片上，不产生层。S13：所以 Docker 直接复用了 B 的那个大层。 | 中国工程师口头说“层”（书面“镜像层”）。字幕里不说 layer。 |
| writable layer / a thin writable layer / the throwaway layer / thrown away on exit | 可写层 / 一层薄薄的可写层 / 用完就扔的那一层 | S07：和第 2 讲一样，container 会在上面加一层薄薄的可写层，--rm 让它在退出时被扔掉。 | throwaway → 用完就扔（L1 形容 VM 的说法）。on the container's throwaway layer → 在 container 那层用完就扔的可写层上。 |
| cache / cached / come from the cache / CACHED | 缓存 / 用缓存 / 直接用缓存 / CACHED | S06：构建步骤 1 到 3 直接用缓存。S11：构建步骤 2 和 3 用了缓存。 | 旁白指着终端里的 CACHED 时，照原文写。 |
| live view / compact live view / full log / landmarks | 实时视图 / 精简的实时视图 / 完整日志 / 关键行 | S06：你的终端显示的是精简的实时视图；这里是完整日志里的几处关键行。 | landmarks → 关键行，不用“路标”（路标是 S09 的比喻）。 |
| instruction / RUN instruction / chained with double ampersands | 指令 / RUN 指令 / 用 && 串起来 | S05：第 12 到 21 行是一条 RUN 指令，用 && 串起来，所以只产生一层。 | en_display 把 double ampersands 写成 &&（D4）。 |
| Dockerfile instructions: FROM / ARG / ENV / RUN / USER / WORKDIR / COPY / the FROM line / the copy line | FROM / ARG / ENV / RUN / USER / WORKDIR / COPY / FROM 那一行 / COPY 那一行 | S05：先敲 FROM 那一行，再把 README 的六个代码块按顺序复制到下面。 | 照原样写；复制那一步说“复制那一步”或“COPY 那一步”，绝不说“挂载”（A7）。 |
| config card / card-only lines / writes on the config card | 配置卡片 / 只写配置卡片的那几行 | S11：只写配置卡片的那几行显示 0 字节。 | 第 2 讲里镜像配置的画法。 |
| working folder / WORKDIR / make /app the working folder | 工作目录 / WORKDIR | S05：第 23 和 24 行切换到这个用户，并把 /app 设成工作目录。 |  |
| user app / user ID 1000 / owns /app / running as root / security risk | 用户 app / 用户 ID 1000 / 拥有 /app / 用 root 运行 / 安全风险 | S05：最后，它创建一个叫 app 的用户，用户 ID 1000，拥有 /app：README 里说，用 root 运行有安全风险。 | root 照说英文（L1）。 |
| run / runs the image / start a new container / a fresh container / exit / removed | 运行 / 跑 / 启动 container / 起一个新的 container / 退出 / 被删掉 | S11：输入 exit，container 连同那层用完就扔的可写层一起被删掉，26 个包也跟着没了。 | exit 命令照写。 |
| bind mount / mount / mounts the current folder onto /app / the mount | bind mount / 挂载 / 挂载到 / 绑定挂载（书面） | S01：bind mount 开了一扇通往你笔记本的窗。S07：用 -v 把当前目录，也就是 pwd，挂载到 /app 上。 | 名词照说英文（实验课口语，也是 Docker 的挂载类型名）；动词说“挂载”。绝不说挂载会“复制”（A7）。 |
| dash v / dash dash r m / dash t i / pwd / the current folder / quotes included | -v / --rm / -ti / pwd / 当前目录 / 连引号一起 | S07：输入 docker run，加上 --rm、-ti、带挂载的 -v，再加上 image 名。 | 字面的 -v "$(pwd):/app" 不写进中文行（B3）；参数由 en_display 给出。 |
| Docker / Docker Desktop / Docker Engine / docker version | Docker / Docker Desktop / Docker Engine / docker version | S01：我们录制用的是一台 Debian 12 笔记本，录制时是 Docker Engine 29。 | On a Mac or Windows, Docker Desktop runs the containers → 在 Mac 或 Windows 上，由 Docker Desktop 来跑 container。 |
| docker build / docker run / docker images / docker history / docker image ls / docker image rm / docker image prune | docker build / docker run / docker images / docker history / docker image ls / docker image rm / docker image prune | S15：然后暂停，用 docker image rm 删掉这五个 image，这也是额外步骤。 | 照原样写。带 image 名的完整 docker build / docker run 命令不写进中文行（A6、B3）。 |
| Docker Hub / push / tag / log in / access token / untagged / user name | Docker Hub / push / 打 tag / 登录 / 访问令牌 / 没有 tag 的 / 用户名 | S14：先在那里创建一个访问令牌，然后登录、打 tag、push。 | 书面写“推送”（A4）。untagged → 没有 tag 的。占位符 USER NAME、ACCESS TOKEN 不写出来。 |
| dot dockerignore / dot gitignore / secrets slash | .dockerignore / .gitignore / secrets/ | S14：解决办法第 2 讲也推荐过，在这里算额外步骤：一个叫 .dockerignore 的文件，只有一行：secrets/。 | en_display：.dockerignore、.gitignore、secrets/（D4）。 |
| Git BASH / winpty / the input device is not a T-T-Y / put winpty in front | Git BASH / winpty / the input device is not a TTY / 在前面加上 winpty | S07：在 Windows 上，这些命令要在 Git BASH 里跑，pwd 两边的引号要保留；如果 docker run 报 the input device is not a TTY，就在前面加上 winpty。 | 报错原文照写，用 TTY（en_display 把 T-T-Y 写回 TTY）。 |

### Python、uv 与包 / Python, uv, packages

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| uv / uv init dash dash bare / uv add / uv sync / uv dash dash version / the installer / restart your terminal | uv / uv init --bare / uv add / uv sync / uv --version / 安装脚本 / 重启终端 | S04：现在是这一步本身：uv init --bare。 | uv 照写（L1）。command not found 照写。installed uv 0.13.0 at the time of recording → 录制时装的是 uv 0.13.0。 |
| pyproject.toml / uv.lock / the list / the receipt / lock file | pyproject.toml / uv.lock / 清单 / 小票 / lock 文件 | S08：清单 pyproject.toml 和小票 uv.lock 都在 /app 里，所以它们直接写进了你的笔记本。 | 沿用 L1 的比喻：愿望清单 / 购物小票（简称小票）。lock 文件同 L1（不说“锁文件”）。 |
| package / packages / Debian packages / apt's package lists | 包 / Debian 软件包 / 软件包列表 | S05：它更新 Debian，装上我们要的软件包，再在同一层里删掉 apt 的软件包列表，所以它们不占空间。 | A7：Python 的叫“包”，apt 的叫“软件包”。 |
| dependencies / lower bound / resolves the whole tree / its own dependencies | 依赖 / 下限 / 解析整棵依赖树 | S08：和第 1 讲一样，每个包都会带来自己的依赖，uv 会解析整棵依赖树。 | resolve 译“解析”（L1）。 |
| minimum Python version / range / interval / or newer / falls outside / requires-python | 最低 Python 版本 / 范围 / 及以上 / 落在范围之外 / requires-python | S04：如果你的是 3.13 及以上，image 里的 3.12 就落在范围之外，那就把它改成 3.12。 | interval 也译“范围”（两个词共用一个译法）。不写 >=，说“及以上”（B3）。requires 3.14 or newer → 要求 3.14 或更新。 |
| venv / activated / activation / the venv variable | venv / 激活 / venv 变量 | S07：提示符里没有显示 venv 的名字，但 venv 其实已经激活了。 | VIRTUAL_ENV 叫“venv 变量”（A6）。 |
| system Python / Debian's system Python / the image's own Python / uv's own Python / uv's folder | 系统 Python / Debian 的系统 Python / image 自带的 Python / uv 下载的 Python / uv 的目录 | S05：和第 1 讲里 Debian 的系统 Python 不同，这个 Python 属于 image，所以 pip 可以往里装。 | 沿用 L1 的“系统 Python”。 |
| pip / upgrades pip / pip install uv | pip / 升级 pip / pip install uv | S05：然后它升级 pip，再用 pip 装上 uv。 |  |
| ffmpeg / ffmpeg dash python / build essential / curl / the ffmpeg program | ffmpeg / ffmpeg-python / build-essential / curl / ffmpeg 程序 | S08：这个包叫 ffmpeg-python；单单一个 ffmpeg 是另一个项目。 | en_display：ffmpeg dash python 写回 ffmpeg-python。 |
| package names: google-cloud-storage / google-cloud-speech / ffmpeg-python / google-genai / google-cloud-texttospeech / google-cloud-translate / requests | google-cloud-storage / google-cloud-speech / google-genai / google-cloud-texttospeech / google-cloud-translate / requests | S13：运行它，加上 storage 和 text to speech：一共 26 个包。 | 旁白常只说最后一个词（add storage and translate）：跟着旁白说；完整包名在画面上。 |
| import / imports / module / modules / comes with Python | import / 导入 / 模块 / Python 自带 | S03：前几个 import 是 Python 自带的，但两个 Google Cloud 模块和 ffmpeg 不是。 | 作关键字时 import 照说（L1）；imports all three packages → 能导入这三个包。 |
| compilers / libraries / Google's libraries | 编译器 / 库 / Google 的库 | S06：最大的一层就是那个 RUN，842 MB，装的是编译器、ffmpeg 和它们的库。 |  |
| help / dash dash help / the help text / the README's block / line for line | 帮助 / --help / 帮助文本 / README 里那段 / 逐行一致 | S08：第 9 步：python cli.py --help。 | ask cli.py for its help → 让 cli.py 打印帮助。 |
| flags / arguments / the flags combine / for short | 参数 / 可以合在一起用 / 简写 | S10：额外提示一句：这些参数可以合在一起用，-d、-t、-u 会按顺序把三步都跑完。 | 不说 flag（L1）。or dash d for short → 简写是 -d。 |

### Google Cloud：bucket、密钥与凭据 / Google Cloud: bucket, key, credentials

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Google Cloud / Google Cloud Storage / bucket / the bucket's name / shared bucket | Google Cloud / Cloud Storage / bucket / 存储桶（书面） | S02：这个共享存储就是一个 Google Cloud Storage 的 bucket，画成一个带抽屉的柜子。 | bucket 是实验课口语；书面写“存储桶”（Google Cloud 中文文档）。 |
| object name / prefix / no real folders / one single object name | 对象名 / 前缀 / 没有真正的目录 | S02：bucket 里没有真正的目录：前缀 text prompts，加上组名 group-01，再加上 input- 开头的文件名，这一整串只是一个对象名。 | 字面的对象名拆开来说（A6）。 |
| service account / a robot Google account / the course's service account | 服务账号 / 机器人 Google 账号 / 课程的服务账号 | S04：有了它，你的代码就能以课程的服务账号的身份行事，那是一个机器人 Google 账号，所以要像保管信用卡一样保管它。 | 沿用 L1 的“服务账号”（Google Cloud 中文控制台）。不写“服务帐号”。 |
| key / the course key / key file / mega-pipeline dot json / stand-in / an 82 byte stand-in | 密钥 / 课程密钥 / 密钥文件 / mega-pipeline.json / 替身文件 | S04：第 2 步是密钥：从 Canvas 下载的一个文件，叫 mega-pipeline.json。S14：我们来验证一下，用一个 82 字节的替身文件代替真正的密钥。 | 沿用 L1 的“密钥”。en_display：mega-pipeline.json。 |
| credentials / application default credentials / ADC / default credentials error | 凭据 / 应用默认凭据 / ADC / DefaultCredentialsError | S09：这个查找过程叫应用默认凭据，简称 ADC，它的第一站就是第 10 行的那个变量。 | Google Cloud 中文文档的译名：应用默认凭据。报错名照屏幕原文写（en_display 把 default credentials error 写回 DefaultCredentialsError）。 |
| auth library / Google's auth library / client / storage client / asks who it is | 认证库 / Google 的认证库 / 客户端 / storage 客户端 | S09：你的代码从来不传密钥：客户端会去问 Google 的认证库，它是谁。 | storage client → storage 客户端（代码里是 storage.Client）。 |
| access token / a short-lived access token / every request carries it | 访问令牌 / 短期有效的访问令牌 | S09：认证库用密钥生成一个短期有效的访问令牌，每个发给 Google 的请求都带着它。 | 字幕里不说 token。 |
| authentication / authorization / IAM roles / who is calling / may it do this | 身份验证 / 授权 / IAM 角色 / 谁在调用 / 有没有权限做这件事 | S09：身份验证问的是谁在调用，密钥说是课程的服务账号；授权问的是它有没有权限做这件事，IAM 角色为它打开了 bucket。 | Google Cloud 中文文档的译名。 |
| request / response / call / the audio bytes travel inside the request | 请求 / 响应 / 调用 | S10：音频的字节就放在请求里一起发过去。 |  |
| billed to the course's project / every call and every byte / quota | 记在课程项目的账上 / 每次调用、每个字节 / 配额 | S02：每次调用、每个字节，都记在课程项目的账上，不是你的。 | 沿用 L1 的“计费”一族；your own ElevenLabs quota → 你自己的 ElevenLabs 配额。 |
| Speech-to-Text / Text-to-Speech / Translation / Google's long audio service / Gemini 2.5 Flash Lite / Vertex AI / retires that model | Speech-to-Text / Text-to-Speech / 翻译服务 / 长音频服务 / Gemini 2.5 Flash Lite / Vertex AI / 下线 | S12：Google 会在 2026 年 10 月 20 日下线这个模型。 | 产品名照写；Translation 当服务说时 → 翻译服务 或 翻译这一步。a current model → 一个现行的模型。 |
| the long-running recognize call / an operation / its result call / waits up to 90 seconds | 长时间运行的 recognize 调用 / 操作对象 / result 调用 / 最多等 90 秒 | S10：长时间运行的 recognize 调用会马上交回一个操作对象，就像一张取件单。 | 方法名带下划线（A6）；书面写“长时间运行的操作”。 |
| relative path / starting from the current folder / changed directory away from /app | 相对路径 / 从当前目录算起 / cd 离开了 /app | S05：第 10 行告诉 Google 的库密钥在哪里：secrets/mega-pipeline.json，一个相对路径。 | en_display：secrets/mega-pipeline.json、/app。 |
| permission denied / chown / the chown command on screen | permission denied / chown / 屏幕上的 chown 命令 | S08：如果你用的是 Linux 笔记本，目录又不属于用户 ID 1000，uv add 会报 permission denied：屏幕上的 chown 命令能修好它。 |  |

### 这条 pipeline / The pipeline

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| pipeline / stage / stages / component / components / the first stage, A | pipeline / 阶段 / 组件 / 第一个阶段 | S02：第一个阶段 A，把 input audios 里的录音转写成文字，放进 text prompts。 | pipeline 照说（实验课口语）；组件字母 A 到 E 照写；组件 A、A 的上传代码。 |
| production / services call each other's APIs / shared storage / message bus | 生产环境 / 服务之间互相调 API / 共享存储 / 消息总线 | S02：在生产环境里，服务之间会互相调 API。 |  |
| cabinet / drawer / drawers / the default group's drawer / your group's drawer | 柜子 / 抽屉 / 默认组的抽屉 / 你们组的抽屉 | S02：忘了改的组件会写进默认组的抽屉，可能还会覆盖别人的成果。 | bucket 和它的前缀的画法。 |
| naming contract / the whole wiring / pattern | 命名约定 / 全部的连线 / 同样的模式 | S02：B 用同样的模式下载：这条命名约定，就是全部的连线。 |  |
| group name / your team's name / keeps teams apart / its default has no guard / group-01 | 组名 / 你们组的名字 / 把各组分开 / 默认值没有任何保护 / group-01 | S02：组名把各组分开，但它的默认值没有任何保护。S08：第 8 步：设置你的组名。 | 代码里的 group_name 不写出来（A6）。 |
| leaderboard / live leaderboard / your row lights up / the transcribe cell | 排行榜 / 实时排行榜 / 你那一行会亮起来 / 转写那一格 | S02：每个阶段成功了，实时排行榜上你那一行就会亮起来。 |  |
| voice recording / recordings / transcript / transcribe / podcast / podcast script / English speech / French | 录音 / 转写文本 / 转写 / 播客 / 播客稿 / 英文语音 / 法语 | S02：然后 B 把每份转写文本写成更长的播客稿，放进 text paragraphs。 | transcripts in text prompts → text prompts 里的转写文本。 |
| synthesize / synthesis / translate / translates into French / generate / speaks the French | 合成 / 翻译 / 翻译成法语 / 生成 / 用语音念出法语 | S02：D 把它翻译成法语，放进 text translated，E 再把法语念出来，放进 output audios。 |  |
| download / transcribe / upload / the three verbs / main runs up to three verbs | 下载 / 转写 / 上传 / 三个动作 | S03：在最下面，main 最多执行三个动作，顺序永远是：下载、转写、上传。 | --download、--transcribe、--upload 参数照写；旁白引用打印出来的 download 这个词时照写。 |
| MP3 / FLAC / converts / long audio comes back in pieces / join every piece | MP3 / FLAC / 转成 / 分段返回 / 拼起来 | S10：每段录音，ffmpeg 先把 MP3 转成 FLAC，所以构建参数里要有 ffmpeg。 |  |
| bonus / an optional bonus / ElevenLabs / the instructor's voice / the bonus script / a key file | 附加任务 / 可选的附加任务 / ElevenLabs / 授课老师的声音 / 附加脚本 / 密钥文件 | S13：E 里有一个可选的附加任务，用 ElevenLabs 以授课老师的声音念出法语。 | 绝不出现授课老师的名字。附加脚本是 cli_11.py（能通过检查）。 |
| Gemini model variable / a current model | Gemini 模型变量 / 现行的模型 | S12：之后启动 container 时，要在 Gemini 模型变量里填一个现行的模型。 | GEMINI_MODEL 不写出来（A6）。 |

### 带下划线的名字（A6）/ Names with an underscore (A6)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| transcribe_audio (folder, image, component A, its README) | transcribe audio 目录 / transcribe audio 组件 / transcribe audio 这个 image | S03：进度条切换到 transcribe audio 的 README，它的第 1 步是 cd 进这个目录。 | A6：用旁白的说法；字面的 transcribe_audio 在画面上，出现在命令里时由 en_display 给出。 |
| generate_text / synthesis_audio_en / translate_text / synthesis_audio (folders, images, components B to E) | generate text / synthesis audio en / translate text / synthesis audio | S12：组件 B，也就是 generate text，走的是同一套流程；我们会快一点。 | A6。synthesis_audio_en：旁白为了配音说 E-N；en_display 可以写 synthesis_audio_en。 |
| bucket prefixes: input_audios / text_prompts / text_paragraphs / text_audios / text_translated / output_audios | input audios / text prompts / text paragraphs / text audios / text translated / output audios | S02：C 把播客稿变成英文语音，存进名叫 text audios 的抽屉。 | A6；后面接“抽屉”或“前缀”。 |
| UV_PROJECT_ENVIRONMENT / uv project environment / GOOGLE_APPLICATION_CREDENTIALS / the key variable / the variable from line 10 | uv project environment 这个变量 / 第 9 行那个变量 / 指向密钥的那个变量 / 第 10 行的变量 | S07：第 9 行，也就是 uv project environment 这个变量，防的就是这个。 | A6。 |

### 终端、Git 与报错 / Terminal, Git, errors

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| terminal / prompt / the at sign / your laptop's folder | 终端 / 提示符 / @ 符号 / 你笔记本上的目录 | S07：提示符变了：你是用户 app，在 /app 里，@ 符号后面是 container 的 ID，每次运行都不一样。 | shell 的 prompt 叫“提示符”（L1）；LLM 的 prompt 照说 prompt（A7）。 |
| folder / directory / component folders / the secrets folder / data folders / five folders | 目录 / 组件目录 / secrets 目录 / 数据目录 / 五个目录 | S03：每个目录里都有一个 README、它自己的 cli.py 和一个 secrets 目录，但没有一个有 Dockerfile。 | 终端语境一律说“目录”，不说“文件夹”（L1）。 |
| laptop / on your laptop / the recording laptop | 笔记本 / 你的笔记本上 | S04：我们录制用的这台笔记本没装 uv：报 command not found。 | L1：笔记本电脑，口语说“笔记本”。 |
| ls / cat / grep / echo / which / readlink / cd / cd dot dot | ls / cat / grep / echo / which / readlink / cd / cd .. | S15：在本地，用 cd .. 回到 repo 的根目录。 | en_display：cd dot dot 写回 cd ..。 |
| Git / git status / git-ignored / ignored / git add dash f / never stop ignoring secrets / shell history | Git / git status / 被 Git 忽略 / 忽略 / git add -f / shell 历史记录 | S14：它被 Git 忽略了，所以永远不会传到 GitHub。 | en_display：git add -f。 |
| repo / clone / commit / the latest commit / main branch | repo / clone / commit / 最新的 commit / main 分支 | S03：README 的第一条命令：把 repo clone 下来。 | 同 L1；书面写 仓库 / 克隆 / 提交。 |
| traceback / error / module not found / no module named google | traceback / 报错 / ModuleNotFoundError / No module named google | S07：报 ModuleNotFoundError，No module named google：包还没装。 | 终端原文跟在“报 / 显示”后面照写（L1）；旁白说 module not found 的地方，en_display 写 ModuleNotFoundError。 |
| command not found / cannot access / no such file or directory / None / permission denied | command not found / cannot access / No such file or directory / None | S14：重新构建，再列一次：报 cannot access，No such file or directory。 | 照原样写；If it says None → 如果里面是 None。 |
| warning / Docker flags any variable whose name sounds secret / harmless | 警告 / 名字听起来像密钥的变量 / 无害 | S06：最后它给 image 命名，还有一条关于第 10 行的警告：Docker 会标出任何名字听起来像密钥的变量。 | flags（动词）→ 标出，不是“参数”。 |
| VS Code / editor / edits show up inside at once | VS Code / 编辑器 / 修改 | S07：所以你在 VS Code 里的修改，container 里马上就能看到。 |  |

### 比喻与说法 / Metaphors and phrases

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| window / a window into your laptop / through the window / outside the window / works both ways | 窗 / 这扇窗 / 透过这扇窗 / 在窗外 / 两边都通 | S08：额外检查一下：venv 变量是 /home/app/.venv，在窗外。 | bind mount 的比喻。量词“扇”。不说“窗口”（终端窗口）或 Windows。 |
| written straight into your laptop's folder / stays / lands on the throwaway layer | 直接写进你笔记本上的目录 / 留下来 / 落在用完就扔的那一层上 | S07：写在 /app 下面的东西，会直接写进你笔记本上的目录，而且留下来；其他东西都落在用完就扔的那一层上。 | 绝不说“复制回去 / 同步回去”（A7、A9）。 |
| signpost | 路标 | S09：这个变量就是一个路标：secrets/mega-pipeline.json，从当前目录 /app 算起。 | 指向密钥的那个变量就是路标。 |
| ticket stub / holds a ticket stub / no ticket stub | 取件单 | S13：C 只是拿着一张取件单，最多等 300 秒，然后打印音频会被保存：所以 C 没有上传这一步。 | 长时间运行的操作：交了活，拿一张单，回头再取。不是“小票”（uv.lock，L1）。 |
| parcel / lecture 2's parcel / unpacks all of it | 包裹 / 第 2 讲的包裹 / 全部拆开 | S14：还记得第 2 讲的包裹吗：构建上下文就是整个目录，密钥也在里面，COPY 那一行会把它全部拆开放进去。 | 第 2 讲里构建上下文的画法。 |
| dominoes / knocks over uv sync / like lecture 2's dominoes | 多米诺骨牌 / 推倒 | S11：任何修改，哪怕只是组名，都会像第 2 讲的多米诺骨牌一样，把 uv sync 也推倒。 | 第 2 讲里缓存失效的画法。 |
| bake it in / baked in | 打包进 image | S11：现在新起的 container 不用 uv add 就能导入这三个包：它们已经打包进 image 了。 | L1：baked into an image → 打包进一个镜像；书面（章节名）写“打进镜像”。 |
| the trap / vanish / survives / permanent | 坑 / 消失 / 留下来 / 永久保留 | S11：现在来看那个坑，这也是额外步骤。 |  |
| recipe / the same recipe / speed round / races through the same setup / surprise | 同一套流程 / 快速过一遍 / 飞快地走完 / 意外 | S13：快速过一遍：C、D 和 E。 | 这里的 recipe 指 README 的 13 个步骤（S12），不是第 2 讲的 Dockerfile。 |
| the heart of this lecture / piece by piece / hold on to that word, everything | 这节课的核心 / 一块一块地拼 / 记住这个词 | S05：第 26 行把这个目录里的一切都复制进 image；记住这个词：一切。 |  |

### 标签、进度条与固定句式 / Tags, tracker, fixed patterns

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the tracker / code panels / the yellow your-turn tag / a gray extra tag / study guide / exercises | 进度条 / 代码面板 / your turn 标签 / extra 标签 / 学习指南 / 练习 | S01：左上角的进度条显示 README 的步骤；代码面板会标出文件和行号。 | A11：标签名照画面写；L1 写“轮到你了”“额外”，是因为它计划翻译屏幕上的标签。 |
| an extra check / extras / not in the README / this one isn't from the README | 额外检查 / 额外的命令 / README 里没有 | S03：一个额外检查，README 里没有：列出文件，再显示 commit。 | D6。 |
| at the time of recording / we recorded without a course key | 录制时 / 我们录制时没有课程密钥 | S01：有一点先说清楚：我们录制时没有课程密钥，所以凡是代码要和 Google 打交道的地方，你看到的是命令和该看什么，而不是它的输出。 | 绝不省略（A9）。 |
| a small mistake / a small slip / one harmless slip / a small gap / older Canvas file | 一个小错误 / 一个小疏漏 / 一个无害的小疏漏 / 一个小缺口 / 旧的 Canvas 文件 | S04：一个小错误：各组件的 README 链接的是一个旧的 Canvas 文件，所以用主 README 的链接。 | 一定紧跟改法（A9）。 |
| Ponder this / the ponder's answer, for real / one last question | 来想一想 / 刚才那道题的答案，这次是真的 / 最后一个问题 | S06：来想一想。 | 暂停想一想卡片在画面上是英文（A11）。 |
| with your key, look for / what a missing key looks like / if it fails | 有密钥的话，要找的是 / 缺密钥时的样子 / 如果失败 | S10：有密钥的话，要找的是 Transcribing 加一个文件名、ffmpeg 的日志、响应，还有转写文本。 | 观众会看到的打印词（Transcribing、Uploading、download）照原样写。 |
| Five questions to test yourself / One: … Five: / Answers are in the exercises / Next lecture | 五道自测题 / 第一题 / 第五题 / 答案在练习里 / 下节课 | S15：五道自测题。第一题：D，也就是 translate text，读的是哪个抽屉，又是谁写的？ | D6。 |
| part 1 / part 2 / lecture 1 / lecture 2 / last lecture / next lecture / this lecture | 第一部分 / 第二部分 / 第 1 讲 / 第 2 讲 / 上节课 / 下节课 / 这节课 | S01：和上节课比，有四处变化：你要自己写 Dockerfile，而且要构建五个 image，而不是一个。 | A10。 |

### 数字与单位 / Numbers and units

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| line 21 / lines 5 to 10 / step 7 / steps 10 to 12 / build step 5 | 第 21 行 / 第 5 到 10 行 / 第 7 步 / 第 10 到 12 步 / 构建步骤 5 | S12：第 10 到 12 步：下载、生成、上传。 | C1。 |
| sizes: 1.35 gigabytes / 842 megabytes / 138 kilobytes / 82 byte / zero bytes | 1.35 GB / 842 MB / 约 138 KB / 82 字节 / 0 字节 | S06：额外跑一下 docker images：在这台机器上是 1.35 GB。 | C2。MiB 只在屏幕上写着 MiB 时用。 |
| times: 46.9 seconds / 0.6 seconds / under ten seconds / up to 300 seconds | 46.9 秒 / 0.6 秒 / 不到 10 秒 / 最多 300 秒 | S11：这次构建不到 10 秒。 | C2。 |
| versions: Python 3.11.2 / Python 3.12 / 3.14 or newer / 3.15.0 / uv 0.13.0 / Docker Engine 29 / Debian 12 | Python 3.11.2 / Python 3.12 / 3.14 或更新 / 3.15.0 / uv 0.13.0 / Docker Engine 29 / Debian 12 | S12：完整日志里能看到：uv 下载了它自己的 Python，录制时是 3.15.0，并用它建了 venv。 | C2；at the time of recording → 录制时（A9）。 |
| counts: 26 packages / 237 packages / 1 package / three packages asked for | 26 个包 / 237 个软件包 / 1 个包 / 3 个包 | S08：要了 3 个包，装了 26 个。 | C1。 |
| dates: October 20, 2026 | 2026 年 10 月 20 日 | S12：Google 会在 2026 年 10 月 20 日下线这个模型。 | C2。 |

### 课程、产品与名字 / Course, products, names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / MLOps Learning / Tutorial 0 / the study guide / Canvas / the instructor / the staff | AC215 / MLOps Learning / Tutorial 0 / 学习指南 / Canvas / 授课老师 / 课程团队 | S01：你需要先做完 Tutorial 0，装好 Docker Desktop 和 uv，还要有从 Canvas 下载的课程密钥和你们组的组名。 | A10。 |
| README / the main README / the component READMEs / the appendix / the README's secrets note / the optional last section | README / 主 README / 各组件的 README / Appendix 部分 / README 里关于 secrets 的提示 / 最后那个可选部分 | S05：主 README 的 Appendix 部分有一个示例 Dockerfile，但它的构建参数里是 curl 而不是 ffmpeg：别把它贴进 transcribe audio。 | README 的章节标题照写（Appendix）。 |
| mega-pipeline / dlops-io / group-01 / student / app / last year's solution | mega-pipeline / dlops-io / group-01 / student / app / 去年的参考答案 | S14：课程接下来的方向：去年的参考答案把 secrets 目录放在 repo 外面，运行时挂载到 /secrets。 | A10。 |
| products: Google / Cloud Storage / Speech-to-Text / Text-to-Speech / Vertex AI / Gemini / IAM / Docker Hub / VS Code / Git BASH / PowerShell / GitHub / Debian / Python / PyPI / Unicode / ElevenLabs / macOS / Linux / Windows / Mac | Google / Cloud Storage / Speech-to-Text / Text-to-Speech / Vertex AI / Gemini / IAM / Docker Hub / VS Code / Git BASH / PowerShell / GitHub / Debian / Python / PyPI / Unicode / ElevenLabs / macOS / Linux / Windows / Mac | S05：前四个是：apt 从不提问，文本用 Unicode，Python 立刻输出，uv 复制文件而不是建链接。 | 拉丁字母（A1 b）。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 中文 | 说明 |
|---|---|---|
| Video title | AC215 · 第 3 讲：容器 II——五个容器，一个存储桶（跟练：mega-pipeline） | H1。Containers II → 容器 II。 |
| Part 1 title | AC215 · 第 3 讲（上）：pipeline 与你的第一个 Dockerfile | H1。 |
| Part 2 title | AC215 · 第 3 讲（下）：包、密钥与全部五个组件 | H1。 |
| Chapter S01: Five containers, one bucket | 五个容器，一个存储桶 | H1，书面语体。 |
| Chapter S02: The bucket is the message bus | 存储桶就是消息总线 |  |
| Chapter S03: Clone: five folders, no Dockerfile | 克隆：五个目录，没有 Dockerfile |  |
| Chapter S04: The key, and uv init | 密钥与 uv init |  |
| Chapter S05: Write the Dockerfile, line by line | 逐行写 Dockerfile |  |
| Chapter S06: Build: five steps, one fat layer | 构建：五个步骤，一个特别大的层 |  |
| Chapter S07: Run: a window into your laptop | 运行：一扇通往笔记本的窗 |  |
| Chapter S08: uv add: what lands where | uv add：文件和包各自去了哪里 |  |
| Chapter S09: Who is calling? The key and ADC | 谁在调用？密钥与应用默认凭据（ADC） | H1；核心概念章节带 ADC，方便搜索。 |
| Chapter S10: Transcribe and upload | 转写与上传 |  |
| Chapter S11: Exit, and bake it in | 退出，把包打进镜像 |  |
| Chapter S12: generate_text: same recipe, two surprises | generate_text：同一套流程，两个意外 |  |
| Chapter S13: Synthesize, translate, synthesize | 合成、翻译、再合成 |  |
| Chapter S14: Keep the key out of the image | 别让密钥进镜像 |  |
| Chapter S15: Clean up, recap, and what's next | 清理、回顾和下节预告 |  |

### 配套材料的书面语体 / Written register of the companions

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| written register for the companions: container / image / bucket / bind mount / push / repo / clone / commit / long-running operation / layer | 容器 / 镜像 / 存储桶 / 绑定挂载 / 推送 / 仓库 / 克隆 / 提交 / 长时间运行的操作 / 镜像层 |  | H3、A4。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

AC、access、ADC、add、AI、API、app、Appendix、apt、ARG、audio、audios、bare、BASH、bash、bin、bind、branch、bucket、build、build-essential、BuildKit、CACHED、cannot、Canvas、cat、cd、check-ignore、chown、cli、cli.py、clone、Cloud、CMD、Code、command、commit、container、COPY、CPython、curl、Debian、DefaultCredentialsError、denied、Desktop、device、directory、dlops-io、Docker、docker、Dockerfile、dockerignore、download、echo、ElevenLabs、en、Engine、ENTRYPOINT、entrypoint、ENV、environment、exit、extra、ffmpeg、ffmpeg-python、file、FLAC、Flash、found、FROM、GB、Gemini、generate、Generated、Git、git、GitHub、gitignore、Google、google、google-cloud-speech、google-cloud-storage、google-cloud-texttospeech、google-cloud-translate、google-genai、grep、group-、help、history、home、Hub、IAM、ID、image、images、import、init、input、install、is、KB、Learning、Linux、Lite、LLMOps、local、lock、log、login、ls、Mac、macOS、main、main.py、MB、mega-pipeline、mega-pipeline.json、MiB、MLOps、module、ModuleNotFoundError、mount、MP、named、False、None、not、or、output、paragraphs、permission、pip、pipeline、PowerShell、project、prompt、prompts、prune、push、pwd、py、PyPI、pyproject.toml、Python、python、readlink、README、README.md、repo、requests、requires-python、result、recognize、rm、root、RUN、run、secrets、sh、shell、Speech-to-Text、status、storage、Storage、student、such、sudo、sync、synthesis、tag、text、Text-to-Speech、the、ti、traceback、transcribe、Transcribing、translate、translated、Translation、TTY、turn、Tutorial、Unicode、upload、Uploading、USER、uv、uv.lock、venv、version、Vertex、VS、wc、which、Windows、winpty、WORKDIR、your。

## 规则

规则编号和 glossary.yaml 一致。L1 的 E（屏幕文字）和 F（语音）两组在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（git clone、cd、cd ..、ls、ls -a、cat、grep、echo、which、readlink、curl、sh、pip install uv、uv --version、uv init --bare、uv add、uv sync、python cli.py、docker version、docker build、docker run、docker images、docker history、docker image ls、docker image rm、docker image prune、docker login、docker tag、docker push、git status、git check-ignore、git add -f、chown、winpty、exit）、参数（--rm、-ti、-v、-t、-d、-u、-g、-s、-p、-f、--download、--transcribe、--upload、--generate、--translate、--synthesis、--help、--bare、--version）、文件和目录名（Dockerfile、.dockerignore、.gitignore、pyproject.toml、uv.lock、cli.py、main.py、cli_11.py、mega-pipeline.json、README.md、secrets/、/app、/home/app/.venv、/secrets）、包名（google-cloud-storage、google-cloud-speech、ffmpeg-python、google-genai、google-cloud-texttospeech、google-cloud-translate、requests、build-essential、ffmpeg、curl、pip、uv）、Dockerfile 指令（FROM、ARG、ENV、RUN、USER、WORKDIR、COPY）、配置项（requires-python）、终端原文和报错名（command not found、ModuleNotFoundError、No module named google、DefaultCredentialsError、permission denied、cannot access、No such file or directory、the input device is not a TTY、CACHED、None、download、Transcribing、Uploading）、旁白提到的屏幕标签（your turn、extra；A11）和 README 标题（Appendix）。唯一的例外是带下划线的名字（A6）。（b）**产品、组织、课程和名字**：Google、Google Cloud、Cloud Storage、Speech-to-Text、Text-to-Speech、Vertex AI、Gemini 2.5 Flash Lite、IAM、ADC、Docker、Docker Desktop、Docker Engine、Docker Hub、VS Code、Git、Git BASH、PowerShell、Canvas、GitHub、Debian、Python、PyPI、Unicode、MP3、FLAC、ElevenLabs、macOS、Linux、Windows、Mac、AC215、Tutorial 0、MLOps Learning、mega-pipeline、dlops-io、group-01、student、app。（c）**封闭清单**，中国 MLOps 工程师在实验课上口头就说英文的词：沿用 L1 的 venv、shell、root、repo、clone、commit、import、traceback、lock 文件；容器这几讲新增 container、image、Dockerfile、bucket、pipeline、bind mount、push、tag（打 tag）、prompt（只指 LLM 的 prompt；shell 的 prompt 叫提示符）、API、ID。新词要进（c），必须同时满足：实验课上真的说英文；中文生硬、有歧义或和别的术语撞车。绝不为了“味道”加英文：不说 layer、build、cache、mount（动词）、key、token、credentials、service account、client、request、package、dependency、folder、terminal、stage、component、drawer、leaderboard。
- **[A2]** container 和 image。字幕说 container 和 image，就像助教在实验课上说的：起一个 container、构建 image、image 里、container 退出时；量词“个”（一个 container、五个 image）。标题、章节名、meta.yaml 和配套文档写“容器”“镜像”（A4）：L1 的四句预告写的就是这两个词（那几句实际上是书面语体），Docker 中文文档也这么写。字幕里绝不写“镜像”（日常也指 Debian 的 mirror，L1 叫软件源）。container ID → container ID / container 的 ID；image name → image 名；the official Python 3.12 image → 官方的 Python 3.12 image；five images → 五个 image（不加复数）。
- **[A3]** Docker 的其他词说中文。build → 构建（构建 image、这次构建）；rebuild → 重新构建；build step k（BuildKit 的 [k/5]，青色徽标 build step k）→ 构建步骤 k，数字放在名词后面，免得像 README 的步骤（第 k 步，A7）；build steps 1 to 3 → 构建步骤 1 到 3；the five build steps → 五个构建步骤；build context → 构建上下文；build argument（ARG）→ 构建参数；layer → 层（一层、不产生层、同一层里）；writable layer → 可写层；the throwaway layer → 用完就扔的那一层（L1：用完就扔）；cache → 缓存，cached / come from the cache → 用缓存（终端里的 CACHED 照写）；live view → 实时视图；full log → 完整日志；instruction → 指令（RUN 指令）；config card（第 2 讲的画法）→ 配置卡片；mount（动词）→ 挂载（把当前目录挂载到 /app），名词 bind mount 照说；working folder（WORKDIR）→ 工作目录；run → 运行 / 跑；start a container → 启动 container / 起一个 container；exit → 退出（exit 命令照写）；removed on exit → 退出时被删掉；push → push，tag → 打 tag，log in → 登录，untagged → 没有 tag 的。
- **[A4]** 书面与口头配对。字幕说 repo / clone / commit / container / image / bucket / bind mount / push；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 存储桶 / 绑定挂载 / 推送。the repo 作主语说“这个 repo”。命令本身不受影响（git clone、docker push 照写）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符都不变）；不翻译、不变形，不加引号、书名号或代码格式。需要时后面接一个中文名词：uv sync 这条命令、pyproject.toml 这个文件、.dockerignore 文件、secrets 目录、--rm 参数、ffmpeg-python 这个包、FROM 那一行、RUN 指令。句首不放实物，也不放保留英文的词，前面加一个中文词（输入 docker build……；这个 pyproject.toml……；而 git status……；用 -v……），这样字幕也不会以小写字母开头。
- **[A6]** 带下划线的名字。没有 say: 时，检查器把显示行当朗读文本检查，拒绝 letter_letter 形式（语音会念出“下划线”）。旁白念这些名字时也从不带下划线：它说 transcribe audio、text prompts、uv project environment、the key variable。所以中文行照旁白的说法写：下划线换成空格，和 SAY 一样小写，后面一定接一个中文名词，让人看出这是名字（transcribe audio 目录 / 组件 / image / 的 README；text prompts 抽屉；uv project environment 这个变量）；英文只是指着它的地方，按角色称呼（第 10 行那个变量、组件 A、组名）。对照：transcribe_audio → transcribe audio；generate_text → generate text；synthesis_audio_en → synthesis audio en（SAY 为了配音说 E-N）；translate_text → translate text；synthesis_audio → synthesis audio；input_audios → input audios；text_prompts → text prompts；text_paragraphs → text paragraphs；text_audios → text audios；text_translated → text translated；output_audios → output audios；group_name → 组名；GOOGLE_APPLICATION_CREDENTIALS → 指向密钥的那个变量 / 第 10 行的变量；UV_PROJECT_ENVIRONMENT → uv project environment 这个变量 / 第 9 行那个变量；VIRTUAL_ENV → venv 变量；GEMINI_MODEL → Gemini 模型变量；DEBIAN_PACKAGES → 构建参数；long_running_recognize → 长时间运行的 recognize 调用；ElevenLabs 的密钥文件 → 一个密钥文件。含这种名字的命令（cd transcribe_audio、docker build -t transcribe_audio .）不写进中文行，改用描述（cd 进 transcribe audio 目录；docker build，加上 -t 和 image 名），英文行由 en_display 给出字面命令（D4）。cli_11.py 能通过检查（下划线后面是数字），照写。对象名 text_prompts/group-01/input-….txt 拆开来说（前缀 text prompts，加上组名 group-01，再加上 input- 开头的文件名）。工具链允许显示行保留下划线以后（I1），把这些带空格的写法换回表中的字面形式。
- **[A7]** 易混词对。第 k 步（README 进度条的步骤）≠ 构建步骤 k（BuildKit 的构建步骤）。目录（任何文件夹；终端语境一律说目录，不说文件夹，同 L1）≠ 抽屉（柜子画面里 bucket 的前缀）≠ 前缀（作为字符串的前缀）。bucket（Cloud Storage 的 bucket）≠ 柜子（它的画法）。包（Python 包：uv add、pip）≠ 软件包（apt / Debian 的软件包）；依赖（pyproject.toml 里写的）≠ 包（实际装上的）：要了 3 个包，装了 26 个。提示符（shell 的 prompt）≠ prompt（Gemini 的 prompt，S12）≠ 提示（hint、注意事项）。参数（flag 和打印出来的 arguments；不说 flag）≠ 构建参数（ARG）≠ 变量 / 环境变量（ENV）。密钥（key 文件、服务账号密钥）≠ 访问令牌（用它换来的短期 token；Docker Hub 的 access token 也是）≠ 凭据（credentials，认证库要找的东西）。身份验证（authentication：谁在调用）≠ 授权（authorization：它能不能做这件事）。服务账号 ≠ 账号（Google 或 Docker Hub 账号）。层（image 的层）≠ 可写层（container 的）。复制（COPY，复制那一步）≠ 挂载（mount）：挂载从不复制；写在 /app 下面的文件“直接写进你笔记本上的目录”，绝不说“复制回去 / 同步回去”。构建（build）≠ 生成（generate：Gemini 那一步）。转写（transcribe）≠ 翻译（translate）≠ 合成（synthesize）。上传 / 下载（往返 bucket）≠ push（推到 Docker Hub）。退出（exit container）≠ 删除（docker image rm、被删掉的 container）≠ 清理（clean up）。组名（group name）≠ 用户名（user name）。播客稿（B 写的 podcast script）≠ 脚本（程序：附加脚本、安装脚本）。小票（receipt = uv.lock，L1）≠ 取件单（ticket stub = 长时间运行的操作）。清单（list = pyproject.toml，出自 L1 的愿望清单）≠ 软件包列表（apt 的 package lists）。窗 / 这扇窗（bind mount 的比喻）≠ 窗口（终端或编辑器窗口）≠ Windows（操作系统）。路标（指向密钥的变量）≠ 关键行（完整日志里的 landmarks）。错误（泛指）≠ 异常（Python exception）≠ 报错（屏幕上的出错信息），同 L1。
- **[A8]** 语体：助教带实验课。指令短，动词口语化（装、跑、删、敲、输入、改）；称呼用“你”（跟练视频，一对一；不用“您”“大家”“同学们”）；“我们”指录制时的我们（我们录的时候没有课程密钥）。用中文语序，句子内部可以重组。避免翻译腔：不说“让我们……”（说“我们来……/ 先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不用“一个……的”长链。不用网络流行语。英文的口语节奏按意思转：Here's the chain when it works → 正常情况下，链条是这样的；One honest limit → 有一点先说清楚；so all is well → 所以没问题；Surprise one → 第一个意外；Speed round → 快速过一遍；races through → 飞快地走完；Now the trap → 现在来看那个坑；for real → 这次是真的；Better still → 更好的办法是；Welcome back → 欢迎回来；Two asides → 补充两句；guard it like a credit card → 像保管信用卡一样保管它。
- **[A9]** 准确。限定语照译：only 只，every 每个，at once 马上，up to 最多，about 大约 / 约，under 不到，or newer 及以上，may 可以 / 可能，usually 通常，never 从不 / 永远不。at the time of recording 每次都译“录制时”，绝不省略（uv 0.13.0、Python 3.15.0、Docker Engine 29）。版本、大小、个数、行号、步骤号、构建步骤号和屏幕完全一致。勘误温和，而且一定紧跟改法：a small mistake 一个小错误，a small slip 一个小疏漏，one harmless slip 一个无害的小疏漏，a small gap 一个小缺口。思考题（S02、S06、S07、S12、S14）只问不答，措辞不能泄露答案（S12 不能说 uv 会下载一个 Python；S14 不能说密钥就在里面）。A7 里挂载的说法有约束力（脚本的规则：没有任何东西沿着这扇窗“传过去”）。计费：billed to the course's project → 记在课程项目的账上，not yours → 不是你的。
- **[A10]** 名字。产品、公司、课程保持拉丁字母（A1 b）；“哈佛”只在标题和简介里出现。课程：AC215；lecture n → 第 n 讲（as in lecture 2 → 和第 2 讲一样）；last lecture → 上节课；next lecture → 下节课；this lecture → 这节课；part 1 / part 2 → 第一部分 / 第二部分；Tutorial 0 照写；the instructor → 授课老师（绝不出现名字；点了老师名字的那个 README 标题不引用）；the staff → 课程团队；last year's solution → 去年的参考答案（它的分支：solution 分支）；later tutorials → 后面的教程。用户名 student 和 app、组名 group-01、组件字母 A 到 E 照写；container ID 从不念出来。
- **[A11]** 屏幕保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（含注释）、README 卡片和标签、进度条（README › transcribe_audio，step k of N）、标签（your turn、extra、illustration、expected、erratum、recorded without the key、billed to the course project、at the time of recording、stand-in file · not a real key）、说明文字，以及 with your key、look for 卡片，全是英文，场景不需要任何语言改动。所以旁白提到屏幕上的标签时，字幕照画面写：黄色的 your turn 标签、灰色的 extra 标签（L1 写“轮到你了”，因为它计划翻译屏幕标签；L3 没有）。旁白用自己的话说的照常翻译：an extra check → 额外检查，the tracker → 进度条，code panels → 代码面板。旁白转述 README 时说“README 里说……”。
- **[A12]** 只做大陆简体：默认、程序、代码、文件、目录、服务器、网络、内存、磁盘、脚本、视频、用户名、信息、账号、令牌；不用預設、程式、程式碼、檔案、資料夾、伺服器、網路、記憶體、磁碟、腳本、影片、使用者、帳號、權杖。
- **[A13]** 这一讲没用到的系列词。系列的实验课英文清单（ac215-video skill）还保留 port、volume、PATH、endpoint、embedding、agent、LoRA、CI；这一讲的旁白一个都没说（-v 参数做的是 bind mount，不是 volume；path 是普通的“路径”，a relative path → 相对路径；PATH 这个变量没有出现）。后面几讲从那张清单取用；到时 L1 把 endpoint 译成“接口”的做法让位于清单，就像这一讲的容器 / 镜像（A2）。

### B. 排版

- **[B1]** 空格。中文和拉丁字母、数字、实物之间加一个半角空格（输入 docker build、Python 3.12、第 9 行、26 个包、1.35 GB、secrets 目录、container 里）。检查器对每个显示句都会报缺失的空格。实物内部的空格照原样（uv init --bare），实物内部绝不加空格。全角标点旁不加空格（……cd mega-pipeline。、用户 app，）。不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，实物旁边也一样（输入 exit。）。列举用顿号（google-cloud-storage、google-cloud-speech、ffmpeg-python）。任何括号都不用：（）、()、《》、【】都不用，因为没有 say: 时检查器拒绝括号，双语字幕带也不需要括注。“”只用于中文里引用的想法或词（问它“我是谁”）；实物和标签名不加引号。一个中文句子内部不出现。？！（一个英文句子对应一个中文句子），改用，；：。“第 N 步”“构建步骤 N”后面接说明时用全角冒号。问句保留？。
- **[B3]** 符号。没有 say: 时检查器拒绝数学符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=）、数字后面跟 !、letter_letter 名字（A6）。所以关系用文字说：requires-python 是 3.11 及以上（不写 >=3.11）、最低版本 3.12、a 1 in parentheses → 带括号的 1。字面里有引号、括号或 = 的命令（docker run --rm -ti -v "$(pwd):/app" …、requires-python 那一行、docker login 那一行）不抄进中文行，而是把各部分说出来（docker run，加上 --rm、-ti、带挂载的 -v，再加上 image 名）；SAY 把它念出来的地方，英文行通过 en_display 显示字面形式。允许并照屏幕保留的：路径里的 /（/home/app/.venv、secrets/）、文件名里的 .、参数和名字里的 -、&&（用 && 串起来）、@（@ 符号后面）；用不到 $；不用 ~。

### C. 数字、版本号与单位

- **[C1]** 显示文字里的数字。和屏幕、终端、代码对应的一律用阿拉伯数字：步骤号（第 7 步、第 10 到 12 步）、构建步骤（构建步骤 2）、行号（第 21 行、第 5 到 10 行、第 84 到 91 行）、屏幕上的个数（26 个包、237 个软件包、1 个包、和 26 对比时的 3 个包）、用户 ID 1000、group-01、版本、大小、时间、日期。叙述中的小数目和序数用汉字：五个组件、五个 image、四处变化、三个动作、两个额外检查、两个意外、三个常见原因、六个代码块、第一个阶段、第一部分 / 第二部分、第一题……第五题。英文用单词说、屏幕上是数字的，跟屏幕（three packages asked for, and 26 installed → 要了 3 个包，装了 26 个）；屏幕上没有的，跟英文（all three → 三条都跑一遍）。
- **[C2]** 单位和版本。大小照屏幕写，加半角空格：1.35 GB、1.48 GB、842 MB、205 MB、105 MB、约 845 MB、约 138 KB、82 字节、0 字节（zero bytes）。时间：46.9 秒、0.6 秒、不到 10 秒、最多 90 秒、最多 300 秒。版本带名字：Python 3.11.2、Python 3.12、Python 3.14、3.15.0、uv 0.13.0、Docker Engine 29、Debian 12、Gemini 2.5 Flash Lite。版本范围：3.13 及以上、3.14 或更新。日期：2026 年 10 月 20 日（October 20, 2026）。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每个 SAY 行一条（158 段）；`en` 和 SAY 行逐字节相同；`zh` 按 explainer.voice.split_sentences 的切分，每个英文句子正好一项（这份脚本共 310 句）。只在句子内部重组，绝不合并或拆分。短句也单独一项：Ponder this. → 来想一想。；Pause and run it. → 暂停一下，自己跑一遍。；Welcome back. → 欢迎回来。；Time to clean up. → 该清理了。反复运行 `python -m explainer.i18n check videos/ac215-l03-mega-pipeline --lang zh`，直到打印 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（锚点只给中文配音版安排动画节拍）。字幕按英文音频计时；工具链按位置把每个中文句子和对应的英文句子配对。
- **[D3]** 过得了检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：没有括号（B2）、没有数学符号、没有 letter_letter 名字（A6）、数字后面没有 !、没有以“种”结尾再接，。！？的分句（改写，比如“三种情况。”）、汉字和拉丁字母或数字之间有半角空格（B1）、每句以。！？或……结尾（后面可以跟”或」）、每个拉丁词都在本词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用正则 `[A-Za-z][A-Za-z'.-]*` 切词：group-01 切成 group-，MP3 切成 MP，/home/app/.venv 切成 home、app 和 venv。它报出的拉丁词，要么是该翻译的英文词（通常如此），要么是漏收的实物：按同样的切法把它加进 allowed_spoken_latin，并加进对应的术语条目。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词（dash dash r m、dash t i、dash v、slash app、slash home slash app slash dot venv、secrets slash mega-pipeline dot json、dot gitignore、dot dockerignore、secrets slash、uv dash dash version、uv init dash dash bare、python cli.py dash dash help / download / transcribe / upload、dash d / dash t / dash u、git add dash f、cd dot dot、main dot py、ffmpeg dash python、transcribe dash audio、input dash something dot t x t、T-T-Y、E-N、double ampersands、the at sign）。每个这样的句子都写一项 en_display，显示屏幕上的字面形式（--rm、-ti、-v、/app、/home/app/.venv、secrets/mega-pipeline.json、.gitignore、.dockerignore、secrets/、uv --version、uv init --bare、python cli.py --help、-d、-t、-u、git add -f、cd ..、main.py、ffmpeg-python、transcribe-audio、input-….txt、TTY、synthesis_audio_en、&&、@），其余部分和 SAY 句子逐词一致；同一段里的其他句子写 null。带下划线的名字（A6）只在观众要输入的命令里（cd transcribe_audio、docker build -t transcribe_audio .）在 en_display 里写回字面形式；单纯提到时，两行都保留 SAY 的说法。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它对应的英文句子：不加命令、参数、括注、中文控制台名或解释；“额外”只用在英文标了 extra 的地方；保留英文的词不加中文解释（英文行就在正下方）。
- **[D6]** 固定句式：
  - Pause and run it. → 暂停一下，自己跑一遍。……, and pause to run it. → ……，然后暂停，自己跑一遍。
  - Pause, and catch up to here. / Pause and catch up. → 暂停一下，跟上进度。Pause, and get to this point. → 暂停一下，跟到这一步。
  - Pause and make the change. → 暂停一下，把它改好。Pause and run all three (steps). → 暂停一下，三步都跑一遍。
  - Pause to run X, then exit and rebuild. → 暂停一下，跑 X，然后退出、重新构建。Pause now and write it: → 现在暂停，把它写出来：
  - Pause at the yellow your-turn tag → 看到黄色的 your turn 标签就暂停；a gray extra tag marks a command not in the README → 灰色的 extra 标签表示这条命令 README 里没有。
  - An extra check, not in the README → 一个额外检查，README 里没有。Two extra checks. → 两个额外检查。Another extra: → 再加一个额外检查：Two more extras. → 再做两个额外检查。Last extra: → 最后一个额外检查：An extra tip: → 额外提示一句：
  - Ponder this. → 来想一想。The ponder's answer, for real: → 刚才那道题的答案，这次是真的：
  - Step N: → 第 N 步：Steps 8 and 9: → 第 8 和第 9 步：Steps 10 to 12: → 第 10 到 12 步：
  - With your key, look for … → 有密钥的话，要找的是……A small mistake: → 一个小错误：
  - Five questions to test yourself. → 五道自测题。One: … Five: → 第一题：……第五题：
  - Answers are in the exercises; every command is in the study guide. → 答案在练习里；每条命令都在学习指南里。Next lecture: → 下节课：Welcome back. → 欢迎回来。
- **[D7]** 文件。narration/g1.yaml = S01–S07（第一部分），narration/g2.yaml = S08–S15（第二部分），和 L1 一样；每个文件开头一段注释（覆盖哪些场景、用到的规则：A6 带空格的名字、D4 en_display、没有 say: / anchors），按脚本顺序排列。字符串用双引号；字面的双引号或反斜杠按 YAML 转义。
- **[D8]** 按英文时间轴的长度。中文是在听英文的同时读的，字幕带在英文分段处切换（读得比每秒 9 个单位还快的中文片段，最多多给 1 秒）。每个中文句子读起来的时间要和英文听起来差不多：经验上每个英文单词最多约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也算数（google-cloud-texttospeech 是 14.3 个单位）：英文没有重复的地方，中文不要重复。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一条最多 2 行。分句尽量不超过 24 个单位，用，；：隔开，让切分程序有干净的切点；避免超过 30 个单位又没有标点的分句。
- **[G2]** 字幕结尾：工具链会去掉字幕条末尾的。，、；：，保留？！……和收尾的”（subtitles.strip_end）。能用中文词收尾的，就不要以“实物 + 句号”结尾（“……的 ffmpeg 程序。”比“……ffmpeg。”好读，但两种都合法）。
- **[G3]** 命令不能断开。切分程序把中文行里两个拉丁词之间的空格当成好切点，所以 uv init --bare 或 python cli.py --download 可能被拆到两行，观众就没法照抄了。把整条命令放在分句末尾、全角冒号之后（第 9 步：python cli.py --help。），一条字幕最多一条命令，周围的中文要少；一行放不下的命令（uv add google-cloud-storage google-cloud-speech ffmpeg-python，约 30 个单位）不写进中文行：说“用一条 uv add 命令把三个包都加上”，让终端和英文行显示它。在渲染出来的 .zh.srt 里检查每一条带命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、分部分和章节标题用书面语体（A4：容器、镜像、存储桶、仓库、克隆）；问句保留问号；保留英文的冒号结构（uv add：……、generate_text：……）；命令、目录名和文件名照写，下划线也保留（meta.yaml 不经过检查器）。核心概念章节带英文简称，方便搜索：谁在调用？密钥与应用默认凭据（ADC）。Containers II → 容器 II（第 2 讲的 Containers I 就是容器 I）。
- **[H2]** 简介（B 站 / YouTube）：两三句话。这是 AC215 第 3 讲 dlops-io/mega-pipeline 的跟练视频；观众要做什么、学到什么（五个 Dockerfile、bucket 是组件之间唯一的连接、bind mount、uv add → 退出 → 重新构建的循环、密钥和 ADC、.dockerignore）；英文旁白配中文和中英双语字幕，终端输出录于 2026-10-13，调用 Google 的步骤只展示命令和该看什么。书面语体，用本词表的术语。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md / digest.md）用本词表的书面语体翻译（仓库、克隆、提交、容器、镜像、存储桶、推送、绑定挂载（bind mount）、构建上下文、应用默认凭据（ADC）、长时间运行的操作）；那里可以用括号和下划线（不经过检查器）。标题和 `<summary>答案</summary>` 要翻译。末尾附一张术语表：English | 这里的译法 | 常见变体（镜像层、绑定挂载、存储桶、服务帐号 → 服务账号、LRO）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 照原样；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求）`explainer.i18n check` 在句子没有 say: 时，把语音检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）用在显示行上。对只有字幕的视频（这个系列；video.yaml 没有 languages.zh.voice，词表写 voice: none），这些检查保护不了任何东西，反而逼出了 A6 和 B3。建议：词表的 voice 为 none 时，显示句跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。到那时 A6 改为：带下划线的名字照写（transcribe_audio 目录），按 A6 的对照表。
- **[I2]**（待办，来自 L1 的 I3）explainer/subtitles.py 的 _cuts 把中文行里拉丁词之间的空格当成好切点，命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词不可切分，除非它本身超过一行。
