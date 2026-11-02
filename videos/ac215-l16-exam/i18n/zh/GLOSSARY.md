# AC215 第 16 讲考前精讲版中文字幕词表（中英混用版）

视频：*AC215 · Lecture 16 — System Tradeoffs: networking, runtime config and capacity (with L10) (exam edition)*（`videos/ac215-l16-exam`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生，第 4 次小测（周二）的前一天：做过第 1–14 讲（虚拟机、container、`docker run` 发布 port、`localhost:9000`、从 `secrets/` 挂载的服务账号密钥、cheese app 的 API 和前端），上过或翻过第 10 讲和第 16 讲，可能从没往 VPC 里部署过东西，想答好关于私有和公网地址、负载均衡器、子网、路由表和 NAT、浏览器代码该把请求发到哪里、构建一次和启动时注入配置与密钥、受数据库连接数约束的自动扩缩，以及 PostgreSQL + pgvector 的概念选择题，并说出每个错误选项**为什么**错。他们在笔记本上看，没有打开 clone。语体：中国 MLOps 助教在考前一天带复习课。
这是**考前精讲版**，不是跟练：没有 README 进度条，没有 `your turn` 标签，没有终端录屏，不逐条讲命令，也**不做任何现场运行**：每个面板都是两个演示仓库的源码（`dlops-io/cheese-app-v0` @ `cb6fb94`，`dlops-io/cheese-app-v2` @ `14f2a14`）或我们自己重画的课件示意图。第 16 讲的课件是主要来源，第 10 讲用来开场。
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l16-exam.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长，只保留显示规则。但没有 `say:` 时，`python -m explainer.i18n check` 仍会对显示行做朗读检查（括号、数学符号、带下划线的名字、词表里没有的拉丁词、缺少的半角空格）：规则 A6、B3、D3 就是为此定的。
英文原稿：`script.md` v2（SAY 行是旁白：73 段、206 句；S01–S04 是 39 段、113 句，S05–S08 是 34 段、93 句）。课件：第 16 讲课件（81 页，没有 SLIDES.md）和第 10 讲的 `../ac215-l10-cloud-connect/SLIDES.md`（55 页）。
先例：系列试点 [`ac215-l01-vms-venvs`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md)（repo、笔记本、服务账号、密钥、虚拟机）；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md) 到 [`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md)（container、image、port、push、pull、tag、digest、registry、发布、门、挂载、层、配置卡片、localhost、监听、IP 地址、子网）；[`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md)（embedding、语言模型、向量数据库、检索）；最新完成的跟练 [`ac215-l08-llm-finetuning`](../../../ac215-l08-llm-finetuning/i18n/zh/GLOSSARY.md)（endpoint、托管、交付，以及这份词表沿用的 A1–I3 规则编排）；同系列的考前精讲版 [`ac215-l13-exam`](../../../ac215-l13-exam/i18n/zh/GLOSSARY.md)（副本）和 [`ac215-l14-exam`](../../../ac215-l14-exam/i18n/zh/GLOSSARY.md)（考前精讲版、小测、题目、选项、选 B、灰色标签、课件第 n 页、现场运行、工作负载）。第 1–14 讲定下的词一律沿用。
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）

## 为什么要中英混用

- 中国的 MLOps 工程师讲云上网络时本来就中英混着说：“这个 VPC 切成三个子网”“默认路由指向 NAT”“前端直接调公网 endpoint”“image push 到 registry”“起一个 worker 去下模型”。但子网、路由表、负载均衡器、安全组、副本、连接池这些词，中文资料和云厂商的中文文档早有标准说法，工程师也这么说，就说中文。
- 观众要在英文的示意图、代码面板和考题里找东西。地址、地址块、port、`localhost:9000`、`api.example.com`、路由表的目标（local、Internet Gateway、NAT Gateway）、报错原文 too many connections 一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 第 4 次小测的选项是英文的：VPC、NAT、DNS、endpoint、worker 照说，看题时一眼就对得上；书面材料再括注中文全称（A4）。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：代码面板、README 面板、重画的课件示意图、数据包信封、课件标签、结论卡片和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在考前一天带复习课时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。每个选择都要过三关：复习课上真的这么说；是能搜到的中文标准译名（AWS / Google Cloud 中文文档、中文网络和数据库资料）；和系列保持一致。

1. **实物原样**：观众要在屏幕上对照的东西（地址、地址块、port、`localhost:9000`、`api.example.com`、`/api`、`/secrets`、`-p 9000:9000`、`os.environ`、取值 debug 和 info、报错 too many connections、路由目标 local / Internet Gateway / NAT Gateway、Predict 按钮）逐字照抄，不翻译、不变形、不加引号；检查器逼出来的例外是带下划线的名字和 = + − ÷ ⌊ ⌋ 这些符号，按旁白的念法写（A6、B3）。
2. **复习课口语里的英文，封闭清单**：第 1 讲的 repo；第 2–4 讲的 container、image、port、push、pull、tag、digest、registry、Dockerfile；第 5 讲的 embedding；第 6 讲的 schema；第 8 讲的 endpoint；**这期新增 worker**。
3. **其余一律用中文标准术语**（A3）。
4. **视频的比喻按意思译，一个比喻一个词**：告警、门、隧道、大门、小本子、坏掉的那一跳、插槽、去处、卡片、弹开、隐患。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、仓库、镜像仓库（registry）、端口、端点（endpoint）、工作进程（worker）、虚拟私有云（VPC）、网络地址转换（NAT）、NAT 网关（NAT Gateway）、互联网网关（Internet Gateway）、应用负载均衡器（ALB）。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **复习课语体**：题目、选项、选 C、小测、就想：；思考题的引子不给答案；课程的练习题从不引用（A9）。
8. **工具链的约束也是规则**：每个英文句子对应一个中文句子（73 段、206 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

## 关键决定

- **网络词说中文，缩写和画面上的名字照写**（A1、A3）：子网、公有子网 / 私有子网、路由表、默认路由、local 路由、负载均衡器、安全组、防火墙、数据包、域名、解析器、权威 DNS；VPC、NAT、DNS、IP 照写；Internet Gateway、NAT Gateway 是课件画的 AWS 名字，照画面写（书面：互联网网关、NAT 网关）。
- **private / public 分清**（A7）：私有地址、私有子网、私有网络、私有 registry；公网地址、公网 IP、公网 endpoint、公网 HTTPS 域名；公有子网（AWS 中文文档）；公开网站、本来就是公开的。
- **全片的核心判断，一个说法**：NAT only carries connections that start inside → **NAT 只转发从里面发起的连接**（S03、S08）；the most specific match wins → **最具体的那条匹配胜出**；Downstream limits still bound the result → **下游的限制仍然约束着结果**；结论卡片 If the question says X, think: Y → **题目里出现 X，就想：Y**。
- **比喻一个词**：NAT 的 notebook → 小本子（不写 notebook，也不写笔记本）；front door → 大门（≠ 门，一个 port）；the dead hop → 坏掉的那一跳；slots → 插槽；homes → 去处；chips → 卡片。
- **task → 任务**（A7）：课件里负载均衡器后面运行的 FastAPI container，AWS 中文文档叫“任务”；第一次说 FastAPI 任务；和批处理任务、第 8 讲的微调任务、第 13 讲的训练任务分开。
- **secret 和 key 都是“密钥”**（A3、A7）：视频把两者当成一回事；secret manager → 密钥管理服务；workload → 工作负载；promote → 晋级；staging → 预发环境。
- **worker 照说**（A1 c，这期新增）：P1 的后台进程，工程师就叫 worker；书面写工作进程（worker）。
- **带下划线的名字**（A6）：NEXT_PUBLIC_BASE_API_URL → next public base API URL；GOOGLE_APPLICATION_CREDENTIALS → Google Application Credentials；LOG_LEVEL → log level；proxy_pass → proxy pass；英文行用 en_display 还原（D4）。CIDR 地址块照画面带斜杠写（10.0.0.0/16），en_display 把 SAY 的 slash 还原。
- **思考题**（A9）：S03[8]、S05[7]、S06[6] 三张选择题卡片；引子和题干不泄露答案；揭晓以字母开头（选 C。；选 D。；选 B，200。），错误选项照英文点名（B 不对：……）。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：地址、地址块和 port（127.0.0.1、0.0.0.0、10.0.2.5、10.0.3.7、10.0.0.0/16、/24、0.0.0.0/0、192.168、172.16、172.31、9000、3200、8000、443）、主机名、URL 和路径（localhost、localhost:9000、api.example.com、/api、/secrets、secrets 目录）、参数（-p 9000:9000、host）、代码名（next public base API URL、Google Application Credentials、log level、proxy pass、os.environ）、取值（debug、info）、报错原文（too many connections）、画面字样（Predict、local、Internet Gateway、NAT Gateway、布局 B）、标签（illustration）。
- 产品、组织、课程和缩写：AC215、Google、Google Cloud、Amazon、Compute Engine、Cloud Load Balancing、Cloud NAT、Cloud SQL for PostgreSQL、AlloyDB、Docker、FastAPI、uvicorn、Nginx、ChromaDB、PostgreSQL、pgvector、Git、README、Cheese App；VPC、NAT、IP、DNS、HTTP、HTTPS、SSH、API、SQL、CPU、HTML、CSS、JavaScript（A1 b）。
- 复习课口语，封闭清单：repo（第 1 讲）；container、image、port、push、pull、tag、digest、registry、Dockerfile（第 2–4 讲）；embedding（第 5 讲）；schema（第 6 讲）；endpoint（第 8 讲）；**worker（这期新增）**。
- 系列清单里保留英文、但这期没说到的：pipeline、volume、venv、PATH、prompt、token、bucket、CI、agent（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| IP address / port | IP 地址 / port | private / public address | 私有地址 / 公网地址 |
| private network / packet | 私有网络 / 数据包 | listen / every interface | 监听 / 所有网络接口 |
| publish a port / tunnel / door | 发布 port / 隧道 / 门 | DNS name / resolver | 域名 / 解析器 |
| authoritative DNS | 权威 DNS | load balancer / front door | 负载均衡器 / 大门 |
| firewall / security group | 防火墙 / 安全组 | stateful / reply | 有状态 / 回复 |
| task / service / client / visitor | 任务 / 服务 / 客户端 / 访客 | VPC / block of addresses / bits | VPC / 地址块 / 位 |
| subnet / public / private subnet | 子网 / 公有子网 / 私有子网 | route table / local route | 路由表 / local 路由 |
| default route / default row | 默认路由 / 默认那一行 | most specific match wins | 最具体的那条匹配胜出 |
| Internet Gateway / NAT Gateway | Internet Gateway / NAT Gateway | NAT / mapping / notebook | NAT / 映射 / 小本子 |
| connections that start inside | 从里面发起的连接 | uninvited / dropped / dead hop | 不请自来 / 丢弃 / 坏掉的那一跳 |
| worker / model weights | worker / 模型权重 | static host / static files | 静态托管 / 静态文件 |
| frontend / relative path / layout B | 前端 / 相对路径 / 布局 B | proxy / path rule | 代理 / 路径规则 |
| build time / compiled into | 构建时 / 编译进 | inbound / outbound | 入站 / 出站 |
| release / deploy / rebuild | 发布 / 部署 / 重新构建 | immutable / digest | 不可变 / digest |
| development / staging / production | 开发环境 / 预发环境 / 生产环境 | runtime values / environment variable | 运行时的值 / 环境变量 |
| secret / key / secret manager | 密钥 / 密钥 / 密钥管理服务 | workload / authorized | 工作负载 / 获得授权的 |
| bake into / rotate | 打进 / 轮换 | promote / inject | 晋级 / 注入 |
| autoscaler / replica | 自动扩缩器 / 副本 | signal / policy / target | 信号 / 策略 / 目标值 |
| minimum / maximum / downstream | 最小值 / 最大值 / 下游 | connection / connection limit | 连接 / 连接数上限 |
| connection pool / pooler | 连接池 / 连接池代理 | other clients / admin console / batch job | 其他客户端 / 管理控制台 / 批处理任务 |
| slots / round down | 插槽 / 向下取整 | database tier / at peak | 数据库规格 / 高峰时 |
| relational / foreign key / transaction | 关系型 / 外键 / 事务 | all or nothing | 全有或全无 |
| vector search / similarity search | 向量检索 / 相似度检索 | vector store / metadata | 向量库 / 元数据 |
| managed / the provider / patching | 托管 / 云厂商 / 打补丁 | restore tests / backups / recovery | 恢复演练 / 备份 / 恢复 |
| homes / chips / bounce off | 去处 / 卡片 / 弹开 | alarm / the quiet problem | 告警 / 隐患 |
| the quiz / question / option | 小测 / 题目 / 选项 | the gray tag / the slides / slide n | 灰色标签 / 课件 / 课件第 n 页 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 开头：上线日的三个告警 / The hook: three alarms on launch day

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| launch day / the Cheese App / last week / in the cloud / inside a private network / three alarms go off / within an hour | Cheese App / 上线日 / 云上 / 私有网络 / 告警 | S01[0]：Cheese App 上线日。 | 应用名照 SAY 的大写写 Cheese App，可以放句首（第 3 讲句中写小写的 cheese app）。alarm → 告警（三个告警响了；第一个告警。）。in the cloud → 在云上；a private network → 私有网络（书面：虚拟私有云（VPC），A4）。Within an hour → 不到一个小时。 |
| language model / an outside language model / chat answers / time out / the saved chat history / the database / loads fine | 语言模型 / 外部的语言模型 / 超时 / 聊天记录 / 数据库 | S01[1]：调用外部语言模型的聊天回答都超时了。 | 第 5 讲：language model → 语言模型；the language model API → 语言模型 API。time out → 超时。loads fine → 照常加载。 |
| the page / every visitor / the Predict button / the developer's laptop / worked | 页面 / 访客 / Predict 按钮 / 开发者的笔记本 | S01[2]：页面对每个访客都能加载，但 Predict 按钮失败了。 | visitor → 访客（≠ 客户端，A7）。按钮上的 Predict 照画面写（A11）。laptop → 笔记本（第 1 讲；不写 notebook，A7）。 |
| traffic doubles / the autoscaler adds replicas / the newest ones / fail with too many connections / their processors sit idle | 流量 / 自动扩缩器 / 副本 / too many connections / CPU | S01[3]：最新的几个副本报 too many connections 失败了，而它们的 CPU 闲着。 | replica → 副本（第 13 讲）；autoscaler → 自动扩缩器（Kubernetes 中文文档的“自动扩缩”）。报错原文 too many connections 照写（A1 a）。processor → CPU：画面上的仪表写的是 CPU，助教也这么说（processor use → CPU 使用率；its processor is idle → 它的 CPU 闲着）。At 9 in the morning → 早上 9 点。 |
| one problem nobody has noticed yet / the production key / inside the container image / the quiet problem | 生产环境的密钥 / 隐患 | S01[4]：生产环境的密钥就放在 container image 里面。 | key → 密钥（第 1 讲）。这里的 problem 是没暴露的风险 → 隐患（还有一个没人注意到的隐患；S05[0] the quiet problem → 那个悄无声息的隐患）。container image 照 SAY 说（A2）。 |
| mechanism / Lectures 10 and 16 / addresses / routes and NAT / the browser / configuration / capacity / the database | 机制 / 第 10 讲 / 第 16 讲 / 地址 / 路由 / 浏览器 / 配置 / 容量 | S01[5]：每个告警都对应第 10 讲和第 16 讲里的一个机制。 | 计划那句保持英文的列举顺序：从地址，到路由和 NAT，到浏览器，到配置，到容量，最后到数据库。 |
| the gray tag / top right / names the slides behind each idea / a live run / illustration | 灰色标签 / 课件 / 现场运行 | S01[6]：这里没有任何现场运行。 | 第 14 讲：the gray tag → 灰色标签；a live run → 现场运行。标签本身（Lecture 16 · slide 71、illustration、the lecture's picture (AWS names)）在画面上保持英文（A11）。 |
| the quiz / a question / the question says / option / First question / Pause here if you want | 小测 / 题目 / 选项 / 第一道题 | S03[8]：想停一下的话，就在这里暂停。 | A8（第 14 讲）：the quiz → 小测（Quiz 4 只在画面上）；a question → 题目；option → 选项。First / Second / Third question. → 第一 / 第二 / 第三道题。Pause here if you want. → 想停一下的话，就在这里暂停。 |

### 从 localhost 到大门：地址、port 与负载均衡器 / From localhost to a front door: addresses, ports, the load balancer

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the course app / uvicorn starts FastAPI / host 0.0.0.0 / port 9000 / listen on every interface / bound to 127.0.0.1 / answer only from inside the container | 课程的应用 / uvicorn / FastAPI / host / 0.0.0.0 / 127.0.0.1 / 网络接口 / 监听 / 绑定 | S02[0]：在课程的应用里，uvicorn 在 container 里启动 FastAPI，host 是 0.0.0.0，port 是 9000。 | host 是画面上 uvicorn 的选项（--host 0.0.0.0），照 SAY 说：That host means listen on every interface → 这个 host 的意思是：在所有网络接口上监听。第 4 讲：listen → 监听；0.0.0.0、127.0.0.1 写数字。Bound to 127.0.0.1 instead → 要是绑定到 127.0.0.1。 |
| the container is sealed off / publish a port / dash p, 9000 to 9000 / the tunnel / the laptop's door / the container's door | container / port / 发布 / -p 9000:9000 / 隧道 / 门 | S02[1]：这个 -p 9000:9000，就是从笔记本的门通进 container 那扇门的隧道。 | 第 4、5 讲：port 照说，publish → 发布，port 就是一扇“门”。中文行照画面写参数；英文行用 en_display 把 Dash p, 9000 to 9000 还原成 -p 9000:9000（D4）。句子不能以 -p 开头（A5）：这个 -p 9000:9000……。 |
| localhost / localhost 3200 / localhost 9000 / this machine / the one the code runs on / served at | localhost / localhost:3200 / localhost:9000 / 机器 | S02[2]：所谓 localhost，永远指这台机器：代码运行的那一台。 | 第 4 讲：localhost 照说（谁的 localhost）。照画面带冒号写（localhost:9000）；英文行用 en_display 把 localhost 9000 还原成 localhost:9000。小写的 localhost 不放句首（A5）：所谓 localhost……；这个 localhost……。 |
| IP address / picks the machine / picks the service on it / private / addresses that start with 10 / 192.168 / 172.16 through 172.31 / the internet does not route them | IP 地址 / 私有地址 / 192.168 / 172.16 / 172.31 / 互联网 | S02[3]：IP 地址选的是机器，port 选的是机器上的服务。 | 第 4 讲：IP 地址。private → 私有（私有地址、私有子网）；public → 公网（公网地址、公网 IP）或公有（公有子网），A7。Addresses that start with 10 → 以 10 开头的地址；172.16 through 172.31 → 172.16 到 172.31。route（动词）→ 路由（互联网不会路由它们）。 |
| move the same container into the cloud / 10.0.2.5 / a packet / from the internet / nobody out there has a route to a private address | 10.0.2.5 / 数据包 / 路由 | S02[4]：在私有网络里，它的地址是 10.0.2.5。 | packet → 数据包（V1 的信封；画面上的 src → dst 保持英文）。IP 地址照画面写数字加点（C1）。 |
| your router keeps the world out / the public finds you / a DNS name / a firewall starts closed / a load balancer lets traffic in | 路由器 / 域名 / 防火墙 / 负载均衡器 | S02[5]：在云上，外界通过域名找到你，防火墙一开始是关着的，负载均衡器把流量放进来。 | load balancer → 负载均衡器（画面上的 ALB、api-alb 保持英文；书面写应用负载均衡器（ALB））。DNS name → 域名；the public（互联网上的人）→ 外界；router → 路由器（≠ 路由，A7）。firewall → 防火墙。 |
| resolver / the authoritative DNS / api dot example dot com / the load balancer's public address / port 443 | 解析器 / 权威 DNS / api.example.com / 公网地址 / 443 | S02[6]：然后浏览器连到负载均衡器的 port 443。 | resolver → 解析器；the authoritative DNS → 权威 DNS（DNS 中文资料的标准说法）。课件的占位域名照画面写 api.example.com；英文行用 en_display 还原 api dot example dot com。 |
| ends the HTTPS connection / sends its own request / the task / the task's port 8000 / security group / allows only the load balancer / a stranger's packet bounces / the reply / the firewall remembers the connection / stateful | HTTPS 连接 / 请求 / 任务 / FastAPI 任务 / 安全组 / 回复 / 有状态 | S02[7]：在那里，安全组只允许负载均衡器访问 port 8000。 | task（课件里 ALB 后面运行的 FastAPI container，AWS 中文文档叫“任务”）→ 任务（第一次说 FastAPI 任务，S03[1]）；≠ 批处理任务（S06），≠ 第 8 讲的微调任务、第 13 讲的训练任务（A7）。security group → 安全组；ends the connection → 终止连接；the firewall remembers the connection → 防火墙记得这条连接（画面上的 stateful: reply allowed 保持英文）。 |
| SSH reaches the machine / clients reach the service / the lecture draws Amazon names / the neighbors / Compute Engine / Cloud Load Balancing / Cloud NAT | SSH / 客户端 / 服务 / Amazon / Compute Engine / Cloud Load Balancing / Cloud NAT | S02[8]：SSH 连到机器，而客户端连到服务。 | the service（监听某个 port 的东西）→ 服务；这期没有 Cloud Run service（A7）。The lecture draws Amazon names → 课上画的是 Amazon 的名字；the neighbors → 对应的产品。产品名用拉丁字母，各占一个分句或放在顿号后面（G3）。 |
| If the question says X, think: Y / a 10 dot address / private, unreachable from the internet / public clients / the private target | 公网客户端 / 私有目标 | S02[9]：题目里出现 localhost，就想：代码运行的那台机器。 | 七张结论卡片共用一个说法（D6）：If the question says X, think: Y → 题目里出现 X，就想：Y；If a question asks …, think → 题目问……，就想；If the question gives …, think → 题目给了……，就想。a 10 dot address → 10 开头的地址（en_display：a 10.x address）。 |

### 私有子网、路由表与 NAT / Private subnets, route tables and NAT

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| VPC / one block of addresses / 10.0.0.0 slash 16 / the slash counts the fixed bits out of 32 / slash 16 leaves 16 bits to vary / 65,536 addresses / slash 24 / 256 | VPC / 地址块 / 10.0.0.0/16 / /24 / 位 | S03[0]：一个 VPC 就是一整块地址，这里是 10.0.0.0/16。 | VPC 照说（A1 b；书面写虚拟私有云（VPC））。CIDR 地址块照画面带斜杠写（10.0.0.0/16、/16、/24）；英文行用 en_display 还原 SAY 里的 slash（D4）。bits → 位（32 位里固定的位数）；65,536 → 65536（C1）。 |
| subnet / three subnets / a public one for the load balancer / a private app subnet for the FastAPI tasks / a private data subnet for the database | 子网 / 公有子网 / 私有应用子网 / 私有数据子网 | S03[1]：课上把它切成三个子网。 | 第 4 讲：subnet → 子网。AWS 中文文档：public / private subnet → 公有子网 / 私有子网。The lecture cuts it → 课上把它切成。 |
| route table / the VPC's own block / the local route / the default row / 0.0.0.0 slash 0 / Internet Gateway / NAT Gateway / the default route | 路由表 / local 路由 / 默认路由 / 0.0.0.0/0 / Internet Gateway / NAT Gateway | S03[2]：每个子网都有一张路由表。 | 路由行的目标照画面写（A1 a、A11）：local → local 路由（不写“本地路由”，A7）、Internet Gateway、NAT Gateway（课件用的 AWS 名字；书面写互联网网关（Internet Gateway）、NAT 网关（NAT Gateway））。the default row → 默认那一行；the default route → 默认路由。 |
| a route alone is not enough / slide 13 adds / a public address / an open firewall / necessary, not sufficient | 课件第 13 页 / 公网地址 | S03[3]：光有路由还不够，课件第 13 页补充说：机器还需要公网地址和打开的防火墙。 | D9：保持英文顺序（先说结论，再说课件第 13 页补充，再说补充的内容）。slide n → 课件第 n 页（第 14 讲）。 |
| matches both rows / the most specific match wins / slash 16 beats slash 0 / the packet stays inside / on the local route | 匹配 / /16 / /0 | S03[4]：这个数据包留在里面，走 local 路由。 | the most specific match wins → 最具体的那条匹配胜出（教科书里叫“最长前缀匹配”；画面上写 longer prefix wins）。slash 16 beats slash 0 → /16 胜过 /0（en_display：/16 beats /0）。 |
| NAT / NAT rewrites the private source / its own public address / writes the mapping in its notebook / sends it out | NAT / 源地址 / 改写 / 映射 / 小本子 | S03[5]：NAT 把私有的源地址改写成自己的公网地址，把映射记在小本子上，再发出去。 | NAT 照说（A1 b；书面写网络地址转换（NAT）），可以放句首。NAT 的 notebook（V2）→ 小本子，一个词；不写 notebook（那是第 6、8 讲的 Colab notebook），也不写笔记本（那是 laptop），A7。 |
| the reply comes back / NAT finds the line / hands it to the task / a packet nobody asked for / has no line / dropped / NAT only carries connections that start inside / nothing uninvited gets in | 回复 / 丢弃 / 连接 / 不请自来 | S03[6]：NAT 只转发从里面发起的连接。 | 固定说法（D6，S03[6]、S03[11]、S08[1]）：NAT only carries connections that start inside → NAT 只转发从里面发起的连接。Nothing uninvited gets in → 不请自来的一律进不来。finds the line → 找到那一行；dropped → 丢弃。 |
| NAT fails / every call to the internet stalls / the dead hop / the database packet still matches the local route / the load balancer still reaches the tasks | 一跳 / 卡住 | S03[7]：每个访问互联网的调用，都卡在坏掉的那一跳上。 | hop → 一跳（the dead hop → 坏掉的那一跳）；stalls → 卡住。Now NAT fails. → 现在 NAT 坏了。 |
| a worker / downloads model weights / from a public website / at startup / nobody on the internet may open a connection to it / default route | worker / 模型权重 / 公开网站 / 启动时 | S03[8]：私有子网里的一个 worker，启动时从公开网站下载模型权重，而互联网上谁都不能主动连接它。 | worker 照说（A1 c，这期新增）：工程师就这么叫后台进程，“工作进程”在复习课上太生硬（书面写工作进程（worker））。小写的 worker 不放句首（A5）。public website → 公开网站（≠ 公网地址，A7）。A9：题干不能提 NAT，也不能暗示答案。 |
| C. / refuses uninvited connections / A, the Internet Gateway, would download too / makes the subnet public / a direct path in / guarded only by firewall rules / B fails / D fails / brings requests in to its targets / not a way out | 选 C / 防火墙规则 / 目标 / 出口 | S03[10]：B 不对：local 路由只覆盖 VPC 自己的地址块，而那个网站在外面。 | 揭晓的说法（D6）：C. → 选 C。；A, the Internet Gateway, would … → A，Internet Gateway，也……；B fails: → B 不对：；D fails: → D 不对：。targets → 目标（负载均衡器的目标）；not a way out → 不是出去的路。 |
| If the question says private subnet / the default route goes to NAT / if NAT is down / internet calls fail / traffic inside the VPC, like the database, still works | 互联网调用 | S03[11]：题目里出现私有子网，就想：默认路由指向 NAT。 | D9：And if NAT is down, internet calls fail, while traffic inside the VPC still works → 而如果 NAT 挂了，互联网调用会失败，VPC 内部的流量，比如数据库，照样能用（if 从句在前，和英文一样）。 |

### 浏览器在 VPC 之外 / The browser lives outside the VPC

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| loading a page is two trips / HTML / CSS / JavaScript / a static host / runs on the visitor's own machine / calls the API | 两趟 / HTML / CSS / JavaScript / 静态托管 / API | S04[0]：加载一个页面要跑两趟。 | static host → 静态托管（书面写静态托管服务；画面上的 static host / CDN 保持英文）。JavaScript、HTML、CSS 用拉丁字母。the visitor's own machine → 访客自己的机器。 |
| the browser lives outside the VPC / static files never enter it / every API request / the front door, the load balancer | 静态文件 / API 请求 / 大门 | S04[1]：所以，浏览器在 VPC 外面。 | front door（比喻，S04[1]、S04[5]、S08）→ 大门，一个词；≠ 门（一个 port），A7。 |
| the frontend / in development / next public base API URL / that variable / says localhost 9000 | 前端 / 开发环境 / next public base API URL / 变量 | S04[2]：在开发环境里，前端从 next public base API URL 读取 API 地址，而这个变量写的是 localhost:9000。 | A6：NEXT_PUBLIC_BASE_API_URL 过不了检查器；中文行照 SAY 的念法写（next public base API URL，大小写照念法），英文行用 en_display 还原。Next public variables（S04[8]）→ 所有 next public 变量（不放句首，A5）。 |
| ship that to a visitor / localhost means the visitor's laptop / nothing listens there / the request fails | 监听 / 访客 | S04[3]：把它发给访客，localhost 就成了访客自己的笔记本。 | ship → 发给（这里是把页面发给访客）。Nothing listens there → 那里没有东西在监听（第 4 讲：listen → 监听）。 |
| swap in the private address / never reaches the VPC / means something only inside the visitor's own network / the public HTTPS name works | HTTPS / 公网 HTTPS 域名 | S04[4]：用公网的 HTTPS 域名就行：DNS，负载均衡器，再到一个任务。 | the visitor's own network → 访客自己的网络。HTTPS 照写（A1 b）。 |
| the production file / just slash api / a relative path / goes back to the host that served the page / one public front door / the lecture's layout B / routes slash api to FastAPI | 生产环境 / /api / 相对路径 / 布局 B | S04[5]：生产环境的配置文件里只写了 /api。 | slash api 照画面写 /api（en_display 还原）。layout B → 布局 B（课件第 32 页）。the host that served the page → 提供这个页面的那台主机。D9：That works when one public front door serves both … → 这在一个公网大门同时提供页面和 API 时行得通（when 从句放在主句里面）。 |
| slide 24 writes that rule twice / an Nginx proxy pass / a load balancer path rule / a separate static host / name the public API address | Nginx / proxy pass / 路径规则 / 公网 API 地址 | S04[6]：课件第 24 页把这条规则写了两遍：一条 Nginx 的 proxy pass，或者一条负载均衡器的路径规则。 | A6：proxy_pass → proxy pass（en_display 还原 proxy_pass）。path rule → 路径规则。the code must name the public API address → 代码就必须写明公网 API 地址。 |
| where the private address lives / the proxy's config / inside the VPC / never in browser code | 代理 / 浏览器代码 | S04[7]：绝不出现在浏览器代码里。 | proxy → 代理；config → 配置。Notice where … → 注意……在哪里。 |
| compiled into the JavaScript at build time / every visitor downloads them / public by design / never a secret / NAT does not help here | 构建时 / 编译 / 公开 | S04[8]：所有 next public 变量都会在构建时编译进 JavaScript，所以每个访客都会下载它们：本来就是公开的，绝不是密钥。 | secret → 密钥（A7：视频把 secret 和 key 当成一回事）。Two more facts. → 再说两点。NAT does not help here → NAT 在这里帮不上忙。 |
| code that runs in the browser / the public HTTPS endpoint / never localhost or a 10 dot address / NAT does not help inbound | endpoint / 入站 | S04[9]：调用公网的 HTTPS endpoint，绝不用 localhost 或 10 开头的地址。 | endpoint 照说（第 8 讲；书面写端点（endpoint））。inbound → 入站；outbound → 出站（只用于书面；SAY 说 calls out → 往外的调用）。 |

### 构建一次，启动时配置 / Build once, configure at startup

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| how a release should work / build the image once / push it with a version tag / every deployment pulls that exact version / no rebuild | 发布 / 构建 / push / tag / 部署 / pull / 重新构建 | S05[0]：把 image 构建一次，打上版本 tag 再 push，每次部署都 pull 这个确切的版本。 | 第 2–4 讲：push、pull、tag 照说；build → 构建，release → 发布，deployment → 部署，rebuild → 重新构建。句子不能以 image 开头（A5）：把 image……。 |
| immutable / development / staging / production / its digest never changes / runtime values / plugged in when the container starts / log level debug / info | 不可变 / 开发环境 / 预发环境 / 生产环境 / digest / 运行时的值 / log level / debug / info | S05[1]：这个 image 是不可变的。 | staging → 预发环境（国内团队的常用说法；也叫预生产环境）。digest 照说（第 2 讲）。A6：LOG_LEVEL → log level；值 debug、info 照写（en_display：log level debug → LOG_LEVEL=debug）。D9：… plugged in when the container starts → ……在 container 启动时插进去的运行时的值。 |
| secrets follow the same rule / a secret manager / delivers the key at startup / only to the workload that is authorized for it / never place secrets in source code, in container images, or in Git | 密钥管理服务 / 工作负载 / 授权 / 源代码 / Git | S05[2]：密钥管理服务在启动时交付密钥，只交给获得授权的工作负载。 | secret 和 key 都译“密钥”（第 1 讲；A7）；a secret manager（泛指；SAY 没提 GCP 的产品名）→ 密钥管理服务。workload → 工作负载（第 14 讲）。固定说法（课件第 22 页）：Never place secrets in source code, in container images, or in Git → 绝不要把密钥放进源代码、container image 或 Git。 |
| the laptop version / the run script / mounts the secrets folder at slash secrets / Google Application Credentials / the key's path inside the container | 运行脚本 / secrets 目录 / /secrets / 挂载 / Google Application Credentials | S05[3]：运行脚本把 secrets 目录挂载到 /secrets，再把 Google Application Credentials 指向 container 里密钥的路径。 | 第 2–8 讲：mount → 挂载；the secrets folder → secrets 目录；slash secrets → /secrets（en_display 还原）。A6：GOOGLE_APPLICATION_CREDENTIALS 照 SAY 写 Google Application Credentials（en_display 还原）。The run script（画面上是 docker-shell.sh）→ 运行脚本；SAY 不提密钥文件名。 |
| the project / the ChromaDB host / arrive as environment variables too / os dot environ / when it starts | 项目 / 环境变量 / ChromaDB / os.environ | S05[4]：应用在启动时用 os.environ 读取它们。 | environment variable → 环境变量（第 2–8 讲）。os dot environ 照画面写 os.environ（没有下划线；en_display 还原）。 |
| the README says why / we do not want any secure information in Git / the key lives next to the repository / never inside it | README / 安全信息 / repo | S05[5]：密钥放在 repo 旁边，绝不放在里面。 | README 的那句话在句子里直接译（不加引号：画面上的 README 面板是英文）：we do not want any secure information in Git → 我们不希望任何安全信息进入 Git。repository → repo（第 1 讲）。 |
| the wrong way / bake the key into the image / anyone who can pull the image can read it / rotating it means a rebuild / per environment images / what you tested is not what you ship | 打进 image / 轮换 / 交付 | S05[6]：把密钥打进 image，任何能 pull 这个 image 的人都能读到它。 | bake into → 打进（把密钥打进 image）；rotate → 轮换；ship → 交付（第 8 讲）。per environment images → 每个环境各一个 image。 |
| Second question / a teammate / bakes an API key into the Dockerfile / pushes the image to the team's private registry / which statement is true | 第二道题 / 队友 / API 密钥 / Dockerfile / registry | S05[7]：一个队友把 API 密钥写进 Dockerfile，再把 image push 到团队的私有 registry。 | 第 2 讲：registry 照说（书面写镜像仓库（registry））。Which statement is true? → 哪个说法是对的？A9：题干不能说谁能读到密钥。 |
| D. / the image's settings and layers / readable by anyone who pulls it / a long list of people and machines / copied to every host / ignoring a different file changes nothing / development images leak / separate images break build once | 选 D / 配置 / 层 / 主机 / 构建一次 | S05[8]：选 D。 | settings → 配置（第 2 讲的配置卡片）；layers → 层（第 2 讲）。host → 主机。build once → 构建一次（这条规则的名字，S05 的标题）。A, the private registry, is still … → A，私有 registry，仍然……。 |
| how to move an image to production / the same image, promoted unchanged / environment values and authorized secrets / injected at startup / never rebuild per environment / never bake a secret | 晋级 / 注入 | S05[10]：题目问怎么把 image 发到生产环境，就想：同一个 image，原样晋级。 | promote → 晋级（同一个 image 从开发到预发再到生产；也有人译“提升”）；injected → 注入。move an image to production → 把 image 发到生产环境（不用“推”，会和 push 混）。 |

### 自动扩缩遇上连接数上限 / Autoscaling meets the connection budget

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| an autoscaler / measures a signal / like processor use / applies a policy / a target, a minimum and a maximum / asks for that many replicas / downstream limits still bound the result | 信号 / CPU 使用率 / 策略 / 目标值 / 最小值 / 最大值 / 下游 | S06[0]：但下游的限制仍然约束着结果。 | 课件第 52 页的说明，固定说法：Downstream limits still bound the result → 下游的限制仍然约束着结果。policy → 策略；target → 目标值；the maximum（自动扩缩器的上限）→ 最大值 / 最大副本数。 |
| the database accepts a fixed number of connections / here 100 / other clients already hold some / an admin console / a batch job | 连接 / 其他客户端 / 管理控制台 / 批处理任务 | S06[1]：其他客户端已经占了一些：一个管理控制台，一个批处理任务。 | connection → 连接。other clients → 其他客户端（≠ 访客，A7）。batch job → 批处理任务（≠ 第 8 讲训练的 batch，≠ 第 14 讲的 Cloud Run job）。 |
| each replica opens its own connections / every API process / its own database client / at import / ChromaDB / standing in here for a connection pool | 进程 / 数据库客户端 / 导入时 / 连接池 | S06[2]：这个客户端是 ChromaDB，在这里就把它当作连接池。 | connection pool → 连接池；at import → 导入时；process → 进程。stands in for → 当作（课程没有连接池，图里由 ChromaDB 扮演它；“代替”会被读成“取代”）。 |
| plugging its pool into free slots / until the slots run out / the next replica cannot connect / though its processor is idle | 插槽 / 空闲插槽 | S06[3]：下一个副本连不上，尽管它的 CPU 闲着。 | slots（V5 的插槽网格）→ 插槽；plug into → 插进。 |
| read the rule off the picture / 100 slots, minus 10 for the other clients, leaves 90 / divide by 20 per replica / 4.5 / round down to 4 / set 4 as the autoscaler's maximum | 减去 / 除以 / 向下取整 | S06[4]：除以每个副本的 20：得 4.5。 | B3：minus → 减去，divided by → 除以，取整符号 → 向下取整；中文行里绝不写 − ÷ ⌊ ⌋。A replica cannot open half a pool → 一个副本不能只开半个连接池。 |
| to go higher / add a connection pooler / shrink each pool / buy a bigger database tier / raising the maximum alone does not help | 连接池代理 / 数据库规格 | S06[5]：只调高最大值没有用。 | connection pooler → 连接池代理（PgBouncer 这类，视频不提名字）；database tier → 数据库规格（云数据库的实例规格）。 |
| Third question / each replica opens 15 connections / at peak / the smallest database tier that works | 第三道题 / 高峰 | S06[6]：能用的最小数据库规格是哪一个？ | at peak → 高峰时。A9：题干不能把 180 算出来。 |
| B, 200 / ten pools of 15 make 150 / plus 30 others: 180 / that fits under 200 / forgets the other clients / costs more than it needs to / a higher maximum adds no connections | 选 B | S06[7]：选 B，200。 | Ten pools of 15 make 150 → 十个 15 的连接池就是 150（SAY 里 Ten 是单词：写汉字，C1）。costs more than it needs to → 花了不必要的钱。 |
| the question gives a database connection limit / the limit minus other clients, divided by connections per replica, rounded down / set it as the maximum / the autoscaler does not know the database limit | 连接数上限 / 每个副本的连接数 | S06[9]：再把它设成最大值，因为自动扩缩器不知道数据库的上限。 | connection limit → 连接数上限；connections per replica → 每个副本的连接数。 |

### 关系型加向量：一个数据库 / Relational plus vectors: one database

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| where the data lives / classify it first / users and orders / linked by foreign keys / transactions that are all or nothing / relational / find the five most similar cheeses / vector search | 用户 / 订单 / 外键 / 事务 / 全有或全无 / 关系型 / 向量检索 | S07[0]：先分类。 | 数据库的标准说法：foreign key → 外键，transaction → 事务，all or nothing → 全有或全无，relational → 关系型。vector search → 向量检索（第 5 讲的“检索”）。the five most similar cheeses → 最相似的五种奶酪（表名 users、orders、cheeses 只在画面上）。 |
| ChromaDB as its own container / a vector store with metadata / the team operates it / patches, backups and recovery are yours | 向量库 / 元数据 / 补丁 / 备份 / 恢复 | S07[1]：现在课程把 ChromaDB 单独跑在一个 container 里。 | vector store → 向量库（第 5 讲的 vector database → 向量数据库）。the team → 团队。 |
| three homes / ChromaDB on a virtual machine / a PostgreSQL service with pgvector / a vector search service / vector chips land everywhere / bounce off the two vector-only homes | 去处 / 虚拟机 / PostgreSQL / pgvector / 向量检索服务 / 卡片 / 弹开 | S07[2]：外键和事务会从两个只做向量的去处弹开。 | V6 的比喻，一个比喻一个词：homes → 去处，chips → 卡片，bounce off → 弹开，land → 落进。virtual machine → 虚拟机（第 1 讲）。pgvector 小写照写，不放句首（A5）。 |
| run two databases / stay in sync / an order exists in one / its embedding is missing from the other | 同步 / embedding | S07[3]：你也可以跑两个数据库。 | 第 5 讲：embedding 照说。sync → 同步。 |
| takes every chip / the vector column / the relational columns / the same table / one query / filters with SQL / orders by similarity | 向量列 / 查询 / SQL / 相似度 | S07[4]：只有带 pgvector 的 PostgreSQL 能接住所有卡片。 | column → 列（第 8 讲）；query → 查询；orders by similarity → 按相似度排序。 |
| managed / the provider runs the hosts and the patching / your team still owns the schema, queries, pooling and restore tests / Cloud SQL for PostgreSQL / AlloyDB | 托管 / 云厂商 / 打补丁 / schema / 恢复演练 / Cloud SQL / AlloyDB | S07[5]：在 Google Cloud 上，就是 Cloud SQL for PostgreSQL，或者 AlloyDB。 | managed → 托管（第 8 讲）；the provider → 云厂商；schema 照说（第 6 讲）；pooling → 连接池管理；restore tests → 恢复演练。Cloud SQL for PostgreSQL 单独占一个分句（G3）。 |
| relational and vector needs in one managed database / PostgreSQL plus pgvector / foreign keys, transactions and similarity search, in one place | 托管数据库 / 相似度检索 | S07[6]：外键、事务和相似度检索，都在一个地方。 | plus → 加（PostgreSQL 加 pgvector；不写 +，B3）。similarity search → 相似度检索。 |

### 小测的七条规则 / Seven rules for the quiz

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Seven rules for the quiz / One: … Seven: / the whole picture / every alarm fixed / static files from the edge / NAT for calls out / trace the request / Good luck on the quiz | 七条规则 / 边缘节点 / 追踪请求 | S08[0]：小测的七条规则。 | 回顾的序号写汉字加全角冒号：One: → 第一：……Seven: → 第七：。the edge → 边缘节点；calls out → 往外的调用。Trace the request first. → 先追踪请求。Good luck on the quiz. → 小测加油。 |

### 课程、名字与产品 / Course, names, products

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / the lecture / Lecture 10 / Lecture 16 / the slides / the instructor / the course staff | AC215 / 课上 / 课件 / 授课老师 / 课程团队 | S02[5]：第 10 讲把它总结了一下。 | A10（第 1–14 讲）。授课老师从不提名字。Lecture 10 sums it up → 第 10 讲把它总结了一下。 |
| products and acronyms: Google / Google Cloud / Amazon / Docker / FastAPI / uvicorn / Nginx / ChromaDB / PostgreSQL / pgvector / AlloyDB / Git / README / HTTP / HTTPS / SSH / DNS / API / SQL / CPU | Google / Google Cloud / Amazon / Docker / Nginx / Git / HTTP / DNS / SQL | S07[6]：题目里出现一个托管数据库同时要满足关系型和向量的需求，就想：PostgreSQL 加 pgvector。 | 拉丁字母（A1 b）。 |
| written register for the companions: container / image / registry / repo / port / endpoint / worker / VPC / NAT / NAT Gateway / Internet Gateway / load balancer / CIDR | 容器 / 镜像 / 镜像仓库 / 仓库 / 端口 / 端点 / 工作进程 / 虚拟私有云 / 网络地址转换 / NAT 网关 / 互联网网关 / 应用负载均衡器 | — | A4、H3。核心概念第一次出现时括注英文（虚拟私有云（VPC）、NAT 网关（NAT Gateway））。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上面各词条 zh_subtitle 和 first_use 里的拉丁词，字幕行还可以出现下面这些（实物按检查器的切法切开，D3）：

AC、ALB、AlloyDB、Amazon、API、api.example.com、App、app.example.com、Application、Balancing、base、CDN、Cheese、ChromaDB、CIDR、Cloud、Compute、connections、container、CPU、Credentials、CSS、debug、digest、DNS、Docker、Dockerfile、embedding、endpoint、Engine、Error、FastAPI、for、Gateway、Git、Google、host、HTML、HTTP、HTTPS、illustration、image、info、Internet、IP、JavaScript、Lecture、level、Load、local、localhost、log、many、MLOps、NAT、Network、next、Nginx、os.environ、pass、pgvector、port、PostgreSQL、Predict、proxy、public、pull、push、Quiz、README、registry、repo、schema、secrets、SQL、SSH、tag、TLS、too、URL、uvicorn、VPC、worker

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组在这里不适用：这个系列不翻译屏幕，也没有中文配音。


### A. 术语与中英混用

- **[A1]** 混用范围。英文只留在三类地方。（a）**实物**，逐字照抄：画面上的地址、地址块和 port（127.0.0.1、0.0.0.0、10.0.2.5、10.0.3.7、10.0.0.0/16、/16、/24、/0、0.0.0.0/0、192.168、172.16、172.31、9000、3200、8000、443），主机名、URL 和路径（localhost、localhost:9000、localhost:3200、api.example.com、/api、/secrets、secrets 目录），参数 -p 9000:9000 和 uvicorn 的 host，按 SAY 念法写的代码名（A6：next public base API URL、next public、Google Application Credentials、log level、proxy pass；os.environ 照画面），取值（debug、info），报错原文（too many connections），旁白点名的画面字样（Predict 按钮，路由表目标 local、Internet Gateway、NAT Gateway，布局字母 B）和标签 illustration。（b）**产品、组织、课程和缩写**：AC215、Google、Google Cloud、Amazon、Compute Engine、Cloud Load Balancing、Cloud NAT、Cloud SQL for PostgreSQL、AlloyDB、Docker、FastAPI、uvicorn、Nginx、ChromaDB、PostgreSQL、pgvector、Git、README、Cheese App；VPC、NAT、IP、DNS、HTTP、HTTPS、SSH、API、SQL、CPU、HTML、CSS、JavaScript。（c）**复习课口语里的英文，封闭清单**：第 1 讲的 repo；第 2–4 讲的 container、image、port、push、pull、tag、digest、registry、Dockerfile；第 5 讲的 embedding；第 6 讲的 schema；第 8 讲的 endpoint；**这期新增 worker**。只有口语里真的说英文、中文又生硬或和别的词撞车时，才加入（c）。不为“味道”说英文：子网、路由表、负载均衡器、防火墙、安全组、数据包、副本、自动扩缩器、连接池、预发环境、密钥管理服务、外键、事务以及 A3 里的所有词都说中文。
- **[A2]** container 和 image（同第 2–14 讲）。字幕说 container、image：同一个 container、把 image 构建一次、container image、每个环境各一个 image；量词“个”。build → 构建，rebuild → 重新构建，mount → 挂载，layer → 层，settings（image 的配置）→ 配置。标题、章节名和 meta.yaml 写“容器”“镜像”（A4）。
- **[A3]** 网络、配置和容量词汇（这期新增）。地址一串：IP 地址，私有地址 / 公网地址，私有网络，数据包，网络接口，监听，绑定到，隧道，port 是一扇“门”（第 4 讲），路由器，域名，解析器，权威 DNS，负载均衡器，防火墙，安全组，回复，任务（FastAPI 任务），客户端，访客，服务。路由一串：地址块，位，子网，公有子网 / 私有子网，私有应用子网 / 私有数据子网，路由表，local 路由，默认那一行 / 默认路由，匹配，最具体的那条匹配胜出，改写源地址，映射，小本子，丢弃，从里面发起的连接，不请自来，一跳，卡住。浏览器一串：静态托管，静态文件，大门，前端，相对路径，布局 B，代理，路径规则，构建时，编译进，入站。配置一串：发布，部署，不可变，开发环境 / 预发环境 / 生产环境，运行时的值，环境变量，密钥（secret 和 key 都是），密钥管理服务，工作负载，获得授权的，运行脚本，打进，轮换，晋级，注入，队友。容量一串：自动扩缩器，副本，信号，CPU 使用率，策略，目标值，最小值 / 最大值，下游，连接，连接数上限，连接池，连接池代理，其他客户端，管理控制台，批处理任务，插槽，向下取整，数据库规格，高峰时。数据库一串：关系型，外键，事务，全有或全无，向量检索，相似度检索，向量库，元数据，同步，列，查询，托管，云厂商，打补丁，备份，恢复，恢复演练，虚拟机。视频的比喻按意思译，一个比喻一个词：告警、门、隧道、大门、小本子、坏掉的那一跳、插槽、去处、卡片、弹开、隐患。
- **[A4]** 字幕与书面。字幕说 container / image / repo / registry / port / endpoint / worker / VPC / NAT；标题、章节名、meta.yaml 和配套文档写 容器 / 镜像 / 仓库 / 镜像仓库（registry）/ 端口 / 端点（endpoint）/ 工作进程（worker）/ 虚拟私有云（VPC）/ 网络地址转换（NAT），网关写 NAT 网关（NAT Gateway）、互联网网关（Internet Gateway），ALB 写应用负载均衡器（ALB），核心概念第一次出现时括注英文（旁白以外可以用括号）。VPC、NAT、DNS、CIDR、PostgreSQL、pgvector 书面也照写。代码名不受影响。
- **[A5]** 实物的写法。逐字照抄；不翻译、不变形、不加引号或《》。需要时加中文中心词：secrets 目录、Predict 按钮、local 路由、FastAPI 任务、next public 变量、公网 HTTPS 域名。句子不以实物或小写的英文词开头（localhost、uvicorn、pgvector、os.environ、next public……、-p、/api、image、container、port、push、repo、registry、endpoint、worker），先放一个中文词（所谓 localhost……；这个 -p 9000:9000……；把 image……；所有 next public 变量……；私有子网里的一个 worker……）。大写的名字、缩写和选项字母（Cheese App、NAT、VPC、DNS、SSH、IP、FastAPI、PostgreSQL、ChromaDB、README、Google、Internet Gateway、A、B、C、D）可以放句首。
- **[A6]** 带下划线的名字和代码表达式（同第 3–14 讲）。没有 say: 时，检查器把显示行当朗读文本，拒收 letter_letter、括号、= 和数学符号。所以中文行按旁白的念法写：NEXT_PUBLIC_BASE_API_URL → next public base API URL；NEXT_PUBLIC_ 变量 → next public 变量；GOOGLE_APPLICATION_CREDENTIALS → Google Application Credentials；LOG_LEVEL=debug → log level 是 debug；proxy_pass → proxy pass。APP_ENV、FEATURE_FLAG 和 myapp:v1.4 只在画面上（SAY 不提）。英文行用 en_display 还原字面形式（D4）。
- **[A7]** 要分清的词。私有（私有地址、子网、网络、registry）≠ 公网（公网地址、公网 IP、公网 endpoint、公网 HTTPS 域名）≠ 公有子网（AWS 中文文档的叫法）≠ 公开（公开网站；public by design → 本来就是公开的）。路由（名词和动词）≠ 路由表 ≠ 路由器（家里的路由器）。local 路由（路由目标，照画面写）≠ 本地（不用于这个意思）≠ 在笔记本上。门（一个 port，第 4 讲）≠ 大门（公网入口）≠ Gateway（网关的名字保持英文）。小本子（NAT 的记录本）≠ notebook（第 6、8 讲的 Colab notebook）≠ 笔记本（laptop）。任务（课件里负载均衡器后面的 FastAPI 任务）≠ 批处理任务 ≠ 第 8 讲的微调任务、第 13 讲的训练任务。服务（监听 port 的东西；PostgreSQL 服务；向量检索服务）：这期没有 Cloud Run service。客户端（其他客户端；公网客户端；数据库客户端）≠ 访客 ≠ 浏览器。“密钥”既是 key 也是 secret（视频把两者当成一回事）；secret manager 是密钥管理服务。连接 ≠ 连接池（一个副本的池）≠ 连接池代理。地址块（CIDR）≠ 层（image 的层）。规格（数据库档位）≠ 版本（版本 tag）。题目（小测的题）≠ 问题 / 隐患（告警说的问题）。课件 ≠ 课上 ≠ 课程团队。
- **[A8]** 语体：考前一天带复习课的助教（同第 14 讲）。句子短而直接；讲到考试时用考试的词（题目、选项、选 C、小测、就想：）；观众是“你”（不用“您”“大家”“同学们”）。分句内部用中文语序，分句顺序跟英文走（D9）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句。不用网络流行语。口语节奏按意思带出来：Start on the laptop → 先从笔记本说起；Move the same container into the cloud → 把同一个 container 搬到云上；Now NAT fails → 现在 NAT 坏了；Now the wrong way → 再看错误的做法；Two more facts → 再说两点；Classify it first → 先分类；So read the rule off the picture → 所以，直接从图上读出规则。
- **[A9]** 精确。量词要译出来：only 只，every 每个 / 每次，all 全部，always 永远，never 绝不 / 从不，both 都，alone 光 / 只。数字照说（C1）。课件和仓库的差别按 SAY 的口气简短客气地说（S02：课上用 port 8000，课程仓库用 9000；S06：ChromaDB 在这里当作连接池）。思考题：三张卡片，P1 在 S03[8]，P2 在 S05[7]，P3 在 S06[6]。引子和题干绝不泄露答案：S03[8] 不能提 NAT，也不能说回复怎么回来；S05[7] 不能说谁能读到密钥；S06[6] 不能把 180 算出来。Pause here if you want. → 想停一下的话，就在这里暂停。揭晓照英文以字母开头（C. → 选 C。；D. → 选 D。；B, 200. → 选 B，200。），错误选项照英文点名（A, the Internet Gateway, would … → A，Internet Gateway，也……；B fails: → B 不对：）。课程的练习题在这里和 i18n/zh 的任何地方都不引用、不改写、不作答，题号也不出现。
- **[A10]** 名字。产品、公司和课程用拉丁字母（A1 b）；“哈佛”只出现在标题和简介里。课程：AC215；lecture n → 第 n 讲（Lectures 10 and 16 → 第 10 讲和第 16 讲）；the lecture → 课上；the slides → 课件；slide n → 课件第 n 页；the lecture's layout B → 课上的布局 B；the instructor → 授课老师，从不提名字（SAY 也不提任何人的名字）；the course staff → 课程团队。The lecture draws Amazon names → 课上画的是 Amazon 的名字。项目 ID、密钥、密钥文件名和 endpoint ID 从不写进中文行；api.example.com 和 10.0.2.5 是课件自己的占位符。
- **[A11]** 画面保持英文。这个系列只翻译旁白：代码面板（含注释）、README 面板和摘录小卡、重画的课件示意图及其标注（VPC、子网、路由行、Internet Gateway、NAT Gateway、ALB、Route 53、ECR、CIDR 尺子、NAT 映射行、课件第 52 页的四个框、第 76 页的三联图）、数据包信封（src → dst）、课件标签（Lecture 16 · slides 13–14、Lecture 10 · slide 11）、小卡（illustration、the lecture's picture (AWS names)、stateful: reply allowed、longer prefix wins）、结论卡片、思考题卡片和错误理由、回顾行都是英文，场景不需要任何语言改动。旁白点名画面上的东西时，字幕照画面写（Predict 按钮；local 路由；Internet Gateway；NAT Gateway；too many connections）；旁白用自己的话说的，就翻译（the gray tag → 灰色标签；the front door → 大门；NAT 的 notebook → 小本子；the slots → 插槽）。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、网络、视频、信息、账号、函数、参数、配置、内存、数据库、数据包、路由、端口、子网、网关、服务器、连接；不用繁体或台湾说法：預設、程式、程式碼、檔案、網路、影片、帳號、函式、引數、組態、記憶體、資料庫、封包、連接埠、子網路、閘道、伺服器、連線。
- **[A13]** 系列清单（ac215-video skill 的清单）在这期的用法。container、image 贯穿全片（S01、S02、S05、S07）；port（S02、S04）；repo（S05[5]）；registry、push、pull、tag、digest（S05）；Dockerfile（S05[7]、S05[9]）；embedding（S07[3]）；schema（S07[5]）；endpoint（S04[9]、S08[2]）。pipeline、volume、venv、PATH、prompt、token、bucket、CI、agent 这份稿子里没有。这期新增的保留英文词（A1 c）：worker。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（是 10.0.2.5、port 是 9000、课件第 13 页、早上 9 点、第 10 讲、secrets 目录、4.5、100 个连接）。检查器会报出每个显示句里缺的空格。实物内部的空格保持原样（Cloud Load Balancing、Google Application Credentials、-p 9000:9000）；实物内部绝不加空格（10.0.0.0/16、localhost:9000）。全角标点旁边不加空格。不用 U+00A0 / U+202F。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，实物旁边也一样。列举用顿号（HTML、CSS 和 JavaScript；外键、事务和相似度检索）。不用任何括号。“”只用于翻译过来的引语；实物、画面字样和 README 的那句话（S05[5] 直接译在句子里）都不加引号。一个中文句子（对应一个英文句子）里面不出现 。？！：用 ，；：。结论卡片的“就想：”和回顾的序号用全角冒号（就想：……；第一：……）。
- **[B3]** 检查器拒收的符号（= < > + → ← × ÷ ≈ ≤ ≥ −、⌊ ⌋、括号、letter_letter、数字后跟 !）：绝不写进中文行，用文字说。minus → 减去；divided by → 除以；rounded down → 向下取整；plus（PostgreSQL plus pgvector；plus 30 others）→ 加；0.0.0.0 slash 0 → 0.0.0.0/0（斜杠可以用）。照画面保留、可以用的：地址和名字里的 .（10.0.2.5、os.environ、api.example.com），地址块和路径里的 /（10.0.0.0/16、/api、/secrets），参数里的 -（-p），主机:port 里的 :（localhost:9000、-p 9000:9000）。

### C. 数字与单位

- **[C1]** 数字。SAY 或画面写成数字的，一律用阿拉伯数字，不加千位分隔符：地址照画面写（10.0.2.5、10.0.3.7、127.0.0.1、0.0.0.0、192.168、172.16 到 172.31），地址块（10.0.0.0/16、/16、/24、/0），port（9000、3200、8000、443），数量（65536、256、32 位、16 位、100 个连接、10、90、20、4.5、4、15、30、10 个副本、150、180、200、250），讲次和课件页码（第 10 讲、课件第 13 页、课件第 24 页），时间（早上 9 点）。SAY 用单词写的小数目用汉字：三个告警、三个子网、两趟、两个数据库、三个去处、七条规则、五种最相似的奶酪、十个 15 的连接池、一个小时。序数用汉字：第一个告警、第一道题、第一：……第七：。
- **[C2]** 单位和时间。At 9 in the morning → 早上 9 点；Within an hour → 不到一个小时；Last week → 上周；This morning → 今天早上；at startup → 启动时；at build time → 构建时；at import → 导入时；at peak → 高峰时；one day → 总有一天。没有价格（金色价签只是一个图）。哈希、digest 值、项目 ID 和提交号从不读出来。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 逐句对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每个 SAY 行都有一条（73 段）；`en` 和 SAY 行逐字节相同；`zh` 的条数和 explainer.voice.split_sentences 切出的英文句子数完全一样（这份稿子 206 句）。只在句子内部调整，绝不合并或拆分句子。短句单独成条：第一个告警。／第三个告警。／先从笔记本说起。／现在 NAT 坏了。／选 C。／选 D。／先分类。／除以每个副本的 20：得 4.5。（一条）／That fits under 200. → 200 装得下。回顾里每条单独成句的规则单独成条。反复运行 `python -m explainer.i18n check videos/ac215-l16-exam --lang zh`，直到输出 OK。
- **[D2]** 不写 say:，不写 anchors。没有中文配音：绝不写 say:，也绝不写 anchors:。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：不用括号（B2），不用数学符号（B3），不出现 letter_letter 名字（A6），数字后面不跟 !，分句不能以“种”结尾再接 ，。！？（“五种最相似的奶酪”在分句中间没问题），汉字和拉丁字母或数字之间有半角空格（B1），每句以 。！？ 或 …… 结尾，每个拉丁词都列在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用 [A-Za-z][A-Za-z'.-]* 切词，忽略单字母词：api.example.com、os.environ、app.example.com 整个算一个词，localhost:9000 算 localhost，-p 9000:9000 算 p（忽略），10.x 算 x（忽略），AC215 算 AC。检查器报出的拉丁词，要么是该翻译的英文词（通常如此），要么是漏列的实物：把实物加进 allowed_spoken_latin 和对应词条。复数形式故意不列（除了报错原文 too many connections 里的 connections）：报出复数，就是该去掉的英文词形变化（两个 image、三个副本）。
- **[D4]** 英文行（en_display）。双语字幕带显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都要在 en_display 里给出屏幕上的字面形式，其余照 SAY 逐字写；同一段里的其他句子写 null。念法 → 字面（script.md 的清单加上这份词表补充的）：localhost 3200 → localhost:3200；localhost 9000 → localhost:9000；Dash p, 9000 to 9000 → -p 9000:9000；api dot example dot com → api.example.com；10.0.0.0 slash 16 → 10.0.0.0/16；Slash 16 leaves … / Slash 24 leaves … → /16 leaves … / /24 leaves …；0.0.0.0 slash 0 → 0.0.0.0/0；slash 16 beats slash 0 → /16 beats /0；a 10 dot address / 10 dot addresses → a 10.x address / 10.x addresses；slash api → /api；next public base API URL → NEXT_PUBLIC_BASE_API_URL；Next public variables → NEXT_PUBLIC_ variables；Google Application Credentials → GOOGLE_APPLICATION_CREDENTIALS；slash secrets → /secrets；os dot environ → os.environ；log level debug → LOG_LEVEL=debug；proxy pass → proxy_pass。不改的：host 0.0.0.0, port 9000（SAY 的写法就是画面的写法）。带下划线的名字（A6）只在 en_display 里还原；中文行保持空格形式。英文版自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它自己的英文句子：不添加地址、命令、括注、中文界面名或解释；保留英文的词不加中文解释（英文行就在下面）；思考题不给答案（A9）。A5 需要的几个开头词（所谓、这个、把、所有）不带内容。
- **[D6]** 固定说法。第一个告警。／第二个告警。／第三个告警。／这就是第一个（第二个）告警。题目里出现 X，就想：Y（S02[9]、S03[11]、S04[9]、S07[6]）；题目问怎么……，就想：（S05[10]）；题目给了……，就想：（S06[9]）。第一道题。／第二道题。／第三道题。／想停一下的话，就在这里暂停。／哪个说法是对的？／选 C。／X 不对：……／NAT 只转发从里面发起的连接（S03[6]、S03[11]、S08[1]）。／下游的限制仍然约束着结果。／绝不要把密钥放进源代码、container image 或 Git。／小测的七条规则。／第一：……第七：……／先追踪请求。／小测加油。
- **[D7]** 文件。narration/g1.yaml = S01–S04（开头、地址和大门、子网、路由表和 NAT、在 VPC 之外的浏览器；39 段、113 句），narration/g2.yaml = S05–S08（构建一次、连接数预算、一个数据库、回顾；34 段、93 句）。视频不分部分，两个文件只是分工。每个文件开头写一段注释（覆盖范围；用到的规则：A6 空格形式、B3 符号用文字、C1 数字和地址、D4 en_display、不写 say: / anchors:），并保持稿子的顺序。用双引号字符串；YAML 里的双引号和反斜杠要转义。
- **[D8]** 按英文时间轴的长度。中文在英文播放时被阅读；字幕带在英文字幕切换的地方切换。每句中文的阅读时间要和英文差不多：每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以去掉多余的连接词和重复的主语，绝不删内容。长实物也占长度（Google Application Credentials 15.4 个单位，Cloud SQL for PostgreSQL 11.6，next public base API URL 11.0，Cloud Load Balancing 9.9，api.example.com 7.2）：英文没重复的地方中文也别重复；第一次之后用短的指代（这个变量、这个域名、这个地址、这条路由）。
- **[D9]** 保持英文的分句顺序（系列教训，ac215-video skill）。工具链按分句把中文和英文配对；英文把条件放在后面，中文却放在前面，相邻两个字幕块的意思就会对调。条件、目的和时间状语放在英文放的位置：A route alone is not enough, slide 13 adds: … → 光有路由还不够，课件第 13 页补充说：……；Ship that to a visitor, and localhost means the visitor's laptop → 把它发给访客，localhost 就成了访客自己的笔记本；That works when one public front door serves both → 这在一个公网大门同时提供页面和 API 时行得通（when 从句放进主句里面也可以）；The next replica cannot connect, though its processor is idle → 下一个副本连不上，尽管它的 CPU 闲着；set it as the maximum, because the autoscaler does not know the database limit → 再把它设成最大值，因为自动扩缩器不知道数据库的上限。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一个字幕块 2 行。分句最好不超过大约 24 个单位，用 ，；： 隔开，给切分器留出干净的切点；Google Application Credentials、Cloud SQL for PostgreSQL、next public base API URL 各自单独成一个分句。
- **[G2]** 字幕块结尾：工具链会去掉字幕块末尾的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。读起来一样顺时，句末用中文词比用“实物 + 句号”更稳（两种都合法）。
- **[G3]** 绝不拆开名字。切分器把中文行里两个拉丁词之间的空格当作好切点，所以 Google Application Credentials、next public base API URL、Cloud Load Balancing、Cloud SQL for PostgreSQL 可能被拆到两行。把这样的名字放在分句末尾、全角冒号或顿号后面，周围少放中文；在渲染出来的 .zh.srt 里检查每个带这些名字的字幕块。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频和章节标题用书面语体（A4：容器、镜像、端口、虚拟私有云（VPC）、NAT 网关）；问句保留问号；保留英文的冒号结构；代码名照写（meta.yaml 不经过检查器，可以用括号）。中文不是常用搜索词的核心概念，章节名带英文简称方便搜索（NAT 网关（NAT Gateway）、负载均衡器（load balancer）），和第 1–14 讲一样。exam edition → 考前精讲版（同第 14 讲）。System Tradeoffs → 系统权衡；with L10 → 含第 10 讲。比喻保留画面：three alarms → 三个告警，a front door → 大门，the connection budget → 连接数预算，Seven rules for the quiz → 小测的七条规则。
- **[H2]** 简介（B 站 / YouTube）：两三句话，书面语体，用这份词表的词：AC215 第 16 讲面向第 4 次小测的考前精讲版，以第 10 讲开场，概念优先，以演示仓库 dlops-io/cheese-app-v0 和 dlops-io/cheese-app-v2 为依据；讲什么（localhost、私有和公网地址、端口、DNS 和负载均衡器；子网、路由表和 NAT 网关；浏览器代码为什么必须调用公网 HTTPS 端点；一个不可变镜像，启动时注入运行时配置和密钥；最大副本数受数据库连接数约束；PostgreSQL + pgvector）；英文旁白，配中文和中英双语字幕；不做现场运行。不出现任何人名，不引用练习题。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md）用这份词表、按书面语体翻译（A4）。末尾附术语表：English | 这里的说法 | 其他常见译法（VPC：虚拟私有云 / 专有网络；subnet：子网；route table：路由表；NAT gateway：NAT 网关；Internet Gateway：互联网网关 / Internet 网关；load balancer：负载均衡器 / 负载均衡；security group：安全组；private / public IP：私有 IP / 公网 IP（私网 IP / 公有 IP）；replica：副本；autoscaler：自动扩缩器 / 自动伸缩；connection pool：连接池；staging：预发环境 / 预生产环境 / 测试环境；promote：晋级 / 提升；secret manager：密钥管理服务 / Secret Manager；foreign key：外键；transaction：事务；vector search：向量检索 / 向量搜索）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 都不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]** （请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读文本的检查（_SPOKEN_BAD）。对只有字幕的视频（这里 voice: none），这些检查什么也保护不了，反而逼出了 A6 和 B3（这里：NEXT_PUBLIC_BASE_API_URL、GOOGLE_APPLICATION_CREDENTIALS、LOG_LEVEL=debug、proxy_pass，以及 S06 的减号、除号和取整符号）。建议：词表的 voice 为 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。
- **[I2]** （待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当作好切点，所以名字可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
- **[I3]** （说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：每个词条 en 字段里 2–3 个词的英文说法会保持在同一行英文里，zh_subtitle 里 2–7 个汉字的中心词会注册进 jieba，对所有视频的字幕都生效。所以这份文件的 en 和 zh_subtitle 只列真正的术语（不写句子）。
