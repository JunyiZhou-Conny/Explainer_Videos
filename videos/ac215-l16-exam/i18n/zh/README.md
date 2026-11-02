# 中文字幕说明

视频 *AC215 · Lecture 16 — System Tradeoffs: networking, runtime config and capacity (with L10) (exam edition)*
（**AC215 · 第 16 讲：系统权衡——网络、运行时配置与容量（含第 10 讲）（考前精讲版）**）是英文旁白，配中文字幕和中英双语字幕，
没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 16 讲“System Tradeoffs: Performance, Cost, and Design Choices”的
**考前精讲版**，以第 10 讲“Connecting to the Cloud”开场，为第 4 次小测准备：不逐条跟练 README，而是把小测考的机制
各画成一张动起来的示意图，再用两个演示仓库的代码和 README 原文作依据：
[dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0)（`main` 分支，提交 `cb6fb94`）和
[dlops-io/cheese-app-v2](https://github.com/dlops-io/cheese-app-v2)（`main` 分支，提交 `14f2a14`）。开头是 Cheese App
上线日的三个告警：调用外部语言模型的聊天回答超时，数据库却照常有回应；Predict 按钮在访客那里失败，在开发者的笔记本上
却是好的；早上流量翻倍，新加的副本报 `too many connections`，CPU 却闲着。还有一个没人注意到的隐患：生产环境的密钥打进了
镜像。每个告警对应一个机制，全片一个部分，八个场景：

- **S01 上线日**：三个告警和一个隐患。
- **S02 从 localhost 到大门**（第 10 讲课件第 4–11 页，第 16 讲课件第 4、8–11、18–20、27 页等）：uvicorn 监听 `0.0.0.0` 和 `127.0.0.1` 的区别，`-p 9000:9000` 这条隧道，
  `localhost` 永远指代码运行的那台机器；IP 地址选机器、端口选服务，10、192.168、172.16 到 172.31 开头的是私有地址；
  搬到云上之后，外界通过域名、解析器和权威 DNS 找到负载均衡器的公网地址，经端口 443 进来，负载均衡器再连到私有地址上
  端口 8000 的任务，安全组只放行负载均衡器。
- **S03 私有子网、路由表与 NAT 网关**（第 16 讲课件第 5–7、12–16 页等）：虚拟私有云（VPC）`10.0.0.0/16` 切成一个公有子网和
  两个私有子网；两张路由表都把 VPC 自己的地址块交给 `local` 路由，区别只在默认那一行 `0.0.0.0/0`（Internet Gateway
  或 NAT Gateway）；最长前缀匹配；NAT 改写源地址、把映射记在“小本子”上，只转发从内部发起的连接。NAT 坏了，互联网调用
  失败，数据库照常可用：第一个告警。
- **S04 浏览器在 VPC 之外**（课件第 23–24、30–32、62–64 页等）：加载页面的两趟，前端的 `NEXT_PUBLIC_BASE_API_URL` 写着
  `localhost:9000`，发给访客就指向访客自己的笔记本：第二个告警。私有地址 `10.0.2.5` 在浏览器里也到不了；能用的是公网
  HTTPS 域名，或者由同一个公网大门转发的相对路径 `/api`（`proxy_pass` 或负载均衡器的路径规则）。`NEXT_PUBLIC_` 变量
  构建时编进 JavaScript，本来就是公开的；NAT 帮不了入站。
- **S05 构建一次，启动时配置**（课件第 17、21–22、29 页；第 10 讲课件第 42–43 页）：同一个不可变镜像在开发、预发和生产环境之间晋级，
  digest 不变；`LOG_LEVEL` 这样的运行时配置和密钥在启动时注入，密钥由密钥管理服务只交给获得授权的工作负载，绝不放进源码、
  镜像或 Git。课程的笔记本版本：运行脚本把 secrets 目录挂载到 `/secrets`，并设置 `GOOGLE_APPLICATION_CREDENTIALS`；
  应用用 `os.environ` 读取配置。
- **S06 自动扩缩遇上连接数预算**（课件第 43–45、52、55、67 页）：自动扩缩器的信号、策略和上下限；每个副本自带连接池，插槽用完后
  下一个副本连不上：第三个告警。最大副本数 = ⌊（连接数上限 − 其他客户端）÷ 每个副本的连接数⌋，图上的例子是
  ⌊(100 − 10) ÷ 20⌋ = 4；想再往上，要加连接池代理、调小连接池或换更大的数据库规格，只调高最大值没有用。
- **S07 关系型加向量：一个数据库**（课件第 65–68、71、75–76 页）：外键和事务是关系型需求，找最相似的奶酪是向量检索；ChromaDB、
  带 pgvector 的 PostgreSQL 服务和向量检索服务三个去处里，只有 PostgreSQL + pgvector 两样都接得住；两个数据库会不同步；
  托管不等于不用管。Google Cloud 上对应 Cloud SQL for PostgreSQL 或 AlloyDB。
- **S08 小测的七条规则**：七条规则的回顾，修好所有告警后的全貌，和“先追踪请求”。

S03、S05、S06 各有一道新写的选择题（思考题），出题之后可以暂停再听揭晓。这些题是视频自己的，不是课程的练习题；
字幕不引用、不转述、也不解答课程的练习题。

画面上的代码面板、README 引文、重画的课件示意图（VPC、子网、路由表各行、Internet Gateway、NAT Gateway、ALB、
Route 53、ECR、CIDR 刻度尺、NAT 映射行、数据包信封）、课件标签（`Lecture 16 · slide 71`、`Lecture 10 · slide 11`）、
`illustration` 等小标签、要点卡片、思考题卡片和回顾的七行都是英文原样，方便你对照课件和仓库；只有旁白译成了中文。
**这个视频不做任何现场运行**：没有终端录屏，每个面板都是两个仓库的源码（照原样复制在 `assets/source/` 下，`.env.*`
两个文件去掉了开头的点，内容不变）或我们自己重画的课件示意图。课件的图用的是 AWS 的名字，课程跑在 Google Cloud 上，
S02 用一句话给出对应的产品。`api.example.com` 和 `10.0.2.5` 是课件自己的示例；项目 ID、密钥和密钥文件名从不出现在任何
字幕和文件里。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l16-exam.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l16-exam.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l16-exam.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l16-exam.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l16-exam.srt` | 英文字幕 |
| `output/chapters.txt` | 章节时间轴（八个场景） |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml` | 逐句对齐英文的中文译文（字幕用；全片一个文件，S01–S08，73 段旁白、206 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（dash p, 9000 to 9000、localhost 3200、localhost 9000、api dot example dot com、a 10 dot address、10.0.0.0 slash 16、slash 16、slash 24、0.0.0.0 slash 0、slash 16 beats slash 0、slash api、next public base API URL、next public variables、proxy pass、log level debug、slash secrets、Google Application Credentials、os dot environ），英文行换回屏幕上的写法（`-p 9000:9000`、`localhost:3200`、`localhost:9000`、`api.example.com`、`10.x`、`10.0.0.0/16`、`/16`、`/24`、`0.0.0.0/0`、`/16 beats /0`、`/api`、`NEXT_PUBLIC_BASE_API_URL`、`NEXT_PUBLIC_`、`proxy_pass`、`LOG_LEVEL=debug`、`/secrets`、`GOOGLE_APPLICATION_CREDENTIALS`、`os.environ`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、章节名和简介 |

配套的学习指南（第 10 讲，cheese-app-v0 的每条命令和中文速览）：
[MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L10-cloud-connect-cheese-app-v0.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l16-exam --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l16-exam --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l16-exam --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或原因放在后面，中文就不把“如果……”“当……时”“因为……”
提到句首，否则相邻两条双语字幕的中英文会互相错开（例如“这个 container 是封起来的，直到你发布一个 port”；“下一个副本
连不上，尽管它的 CPU 闲着”；“这行得通的前提是：一个公网大门同时提供页面和 API……”）。地址、地址块和路径写在分句里
原样不拆（“这个 -p 9000:9000，就是……”“/16 胜过 /0”）。渲染之后，在 `.zh-en.srt` 里再看一遍每条带地址、端口或变量名的字幕。

## 译文风格

按中国 MLOps 助教考前答疑的说法，和第 1–14 讲一致：

- **一字不改**：屏幕上要对照的东西（地址和地址块 `127.0.0.1`、`0.0.0.0`、`10.0.2.5`、`10.0.3.7`、`10.0.0.0/16`、`/16`、
  `/24`、`0.0.0.0/0`，端口 9000、3200、8000、443，主机、URL 和路径 `localhost`、`localhost:9000`、`api.example.com`、
  `/api`、`/secrets`，参数 `-p 9000:9000`，`os.environ`，取值 debug、info，打印出来的 `too many connections`，路由目标
  `local`、Internet Gateway、NAT Gateway，Predict 按钮，课上的布局 B）。字幕检查器不收的几种写法例外：带下划线的名字按
  旁白的念法写成空格（next public base API URL、next public 变量、Google Application Credentials、log level、proxy pass），
  检查器不收的符号用文字说（减去、除以、向下取整、加）；英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，封闭清单：第 1 讲的 repo；第 2–4 讲的 container、image、port、push、pull、tag、
  digest、registry、Dockerfile；第 5 讲的 embedding；第 6 讲的 schema；第 8 讲的 endpoint；这一讲新增 worker。产品和缩写
  照写：VPC、NAT、IP、DNS、HTTPS、SSH、API、SQL、CPU、FastAPI、uvicorn、Nginx、ChromaDB、PostgreSQL、pgvector、
  Compute Engine、Cloud Load Balancing、Cloud NAT、Cloud SQL for PostgreSQL、AlloyDB。
- **其余用中文标准术语**（AWS 和 Google Cloud 中文文档、中文网络和数据库资料里的译名，方便搜索）：私有地址、公网地址、
  私有网络、数据包、网络接口、监听、路由器、域名、解析器、权威 DNS、负载均衡器、防火墙、安全组、任务、客户端、访客、
  地址块、子网、公有子网、私有子网、路由表、默认路由、匹配、源地址、映射、丢弃、静态托管、静态文件、前端、相对路径、
  代理、路径规则、构建时、入站、发布、部署、不可变、开发环境、预发环境、生产环境、环境变量、密钥、密钥管理服务、
  工作负载、运行脚本、轮换、晋级、注入、自动扩缩器、副本、策略、目标值、下游、连接数上限、连接池、连接池代理、插槽、
  向下取整、数据库规格、关系型、外键、事务、向量检索、相似度检索、向量库、元数据、托管、云厂商、恢复演练。
- **比喻按意思译，一个比喻一个词**：告警、门（端口）、隧道（`-p`）、大门（公网入口）、小本子（NAT 的映射表）、坏掉的
  那一跳、插槽、去处、卡片、弹开、隐患。
- **分清容易混的词**：私有（地址、子网、registry）≠ 公网（地址、endpoint、HTTPS 域名）≠ 公有子网 ≠ 公开（公开网站、本来
  就是公开的）；`local` 路由是路由表上的目标，不写“本地路由”，“在笔记本上”说的是 laptop；门是端口，大门是公网入口，
  Gateway 照写；小本子是 NAT 的映射表，不是 Colab 的 notebook，也不是笔记本电脑；任务是负载均衡器后面的 FastAPI 任务，
  批处理任务是另一回事；客户端 ≠ 访客 ≠ 浏览器；连接 ≠ 连接池 ≠ 连接池代理；规格是数据库档位，版本是 image 的 tag；
  题目是小测的题，问题和隐患是告警说的事；课件 ≠ 课上 ≠ 课程团队。
- **精确**：量词照译（只、每个、永远、绝不、都、光）；数字照屏幕写，不加千位分隔符（65536、256）；课件和仓库的差别
  按旁白的口气简短地说（课上用端口 8000，课程仓库用 9000；ChromaDB 在 S06 的图里当作连接池）；思考题的引子和题干
  不泄露答案，揭晓以选项字母开头（“选 C。”“选 D。”“选 B，200。”），错误选项按英文的说法逐个说（“B 不对：……”）。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、镜像仓库（registry）、端口、端点（endpoint）、工作进程
  （worker）、虚拟私有云（VPC）、网络地址转换（NAT）、NAT 网关（NAT Gateway）、互联网网关（Internet Gateway）、
  应用负载均衡器（ALB）；VPC、NAT、DNS、CIDR、PostgreSQL、pgvector 书面也照写。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| VPC | VPC（字幕）；虚拟私有云（书面） | 专有网络 |
| subnet | 子网 | 子网 |
| public / private subnet | 公有子网 / 私有子网 | 公共子网 / 专用子网 |
| route table | 路由表 | 路由表 |
| most specific match | 最具体的那条匹配（字幕）；最长前缀匹配（书面） | 最长匹配 |
| NAT gateway | NAT Gateway（字幕）；NAT 网关（书面） | NAT 网关 |
| Internet Gateway | Internet Gateway（字幕）；互联网网关（书面） | Internet 网关 |
| load balancer | 负载均衡器 | 负载均衡 |
| security group | 安全组 | 安全组 |
| private / public IP | 私有地址 / 公网地址 | 私网 IP / 公有 IP |
| inbound | 入站 | 入向 |
| staging | 预发环境 | 预生产环境、测试环境 |
| promote | 晋级 | 提升 |
| secret manager | 密钥管理服务 | Secret Manager |
| autoscaler | 自动扩缩器 | 自动伸缩 |
| replica | 副本 | 实例 |
| connection pool | 连接池 | 连接池 |
| connection pooler | 连接池代理 | 连接池中间件 |
| database tier | 数据库规格 | 数据库档位、实例类型 |
| foreign key | 外键 | 外键 |
| transaction | 事务 | 事务 |
| vector search | 向量检索 | 向量搜索 |
| managed | 托管 | 全托管 |
