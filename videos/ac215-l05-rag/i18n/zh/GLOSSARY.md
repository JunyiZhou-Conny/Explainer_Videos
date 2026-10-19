# AC215 第 5 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 5 — Introduction to RAG (follow-along: llm-rag)*（`videos/ac215-l05-rag`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，用过 LLM，英文技术文档读得很顺；做过第 1 讲（VM、venv、uv）、第 2 讲（现成的 Dockerfile、image 和 container、Docker Hub）、第 3 讲（从 ../secrets 挂载进来的服务账号密钥、bind mount）和第 4 讲（docker-shell.sh、container 网络、port、Compose）；第一次接触检索、embedding 和向量数据库；开着自己 clone 的 dlops-io/llm-rag（`~/AC215/llm-rag`，旁边是 `~/AC215/secrets`），边看边敲命令  
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l05-rag.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5，“三点十一点二”“点 venv”“杠 m”这类读法、数字和符号怎么念）都不适用，只保留显示规则  
英文原稿：`script.md` v2（SAY 行是旁白：140 段、358 句；SHOW 行是画面）；`build/review_spoken.md` 第 16 条（要进词表的说法：通道、尺子、地震仪、空位、“一个小疏漏”、保留 Step 1 / Step 2；需要 `en_display` 的句子）已并入，script.md 的开头要求这一步照用  
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md)、[`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md) 和 [`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md) 定下容器、密钥和网络的词，以及“只有字幕”的整套规则。前四讲已经定下的词一律沿用；新的是 RAG 的词汇（分块、embedding、向量数据库、查询、过滤、prompt、课上的进阶 RAG，A3）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“把书切成 chunk”“调一下 embedding 模型”“建一个 collection”“取 top K”“写 prompt”“system prompt 根本没发出去”“起两个 container”。在实验课上硬说“文本块”“嵌入向量”“集合”“前 K 个”“提示词”，反而像说明书；这些书面词留给标题、章节名和配套文档（A4）。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、代码和课程的网页工具里找东西。命令、参数、chunk type 的值、文件名、路径、collection 名、模型 ID、环境变量、控制台的角色名、报错原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（检索增强生成、检索、分块、切分、向量、向量化、向量数据库、记录、元数据、索引、维度、余弦相似度、最近邻、过滤、上下文、幻觉、微调、重排序、混合检索）一律说中文；用中文 RAG、LangChain、Chroma、Docker 和 Google Cloud 资料里的标准译名，方便搜索。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、标签、进度条、示意控制台、浏览器里的课程网页工具和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“构建 image”“pull 下来”“把 repo clone 下来”“发布一个 port”“写 prompt”“调 embedding 模型”“把书切成 chunk”“建一个 collection”“取 top K”。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（中文 RAG、LangChain、Chroma、Docker 和 Google Cloud 资料：检索增强生成、分块、向量、向量数据库、索引、元数据、余弦相似度、最近邻、幻觉、微调、重排序、混合检索）；和整个系列一致（第 1 讲定下共用的词，第 2–4 讲定下容器、密钥和网络的词）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、chunk type 的值、文件名和目录名、路径、image / container / collection / 模型的名字、环境变量、控制台上的字样和角色名、终端原文和报错名、画面上的标签、README 的章节标题和 README 概述里的 Step 1 / Step 2、书里引用的原词）逐字照抄，不翻译、不变形、不加引号。检查器逼出来的例外：带下划线的名字，以及 [ ] ( ) = < > + 这几个字符，按旁白的说法写（A6、B3）。终端输出、代码面板、README 卡片、示意控制台、浏览器画面、标签、进度条、课件标签和思考题卡片都是英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 venv、root、repo、clone、commit、pin；第 2–4 讲的 container、image、Dockerfile、base image、tag、pull、pipeline、prompt（只指 LLM 的 prompt）、API、ID、port、localhost；这一讲新增 chunk（名词：一段文本）、embedding（名词：模型和它的输出）、collection、top K、system prompt 和 input prompt、LLM、CLI、agent。
3. **其余一律用中文标准术语**：检索增强生成、检索、生成、增强、分块、切分、切分器、分块器、向量、向量化、查询向量、向量数据库、记录、元数据、索引、建索引、维度、批、相似度、余弦相似度、余弦距离、点积、直线距离、夹角、长度、方向、最近邻、分数、排序、排名、结果、距离阈值、过滤、元数据过滤、文档过滤、关键词过滤、关键词排序、上下文、回答、知识库、语言模型、模型、权重、微调、重新训练、幻觉、窗口、重叠、分隔符、段落、百分位、阈值、语义分块、查询改写、混合检索、倒数排名融合、重排序、检索器、候选、服务账号、密钥、角色、项目 ID、启用、计费、网络、挂载、服务、心跳、构建、构建上下文、提示符、目录、终端、脚本、参数、函数、变量。
4. **视频的比喻按意思译，一个比喻一个词**：方框（box）、通道（lane）、图书管理员和开卷考试（librarian、open-book exam）、尺子（ruler，char-split）、剪刀（scissors，recursive-split）、地震仪（seismograph，semantic-split）、接缝（seam）、保险（insurance）、替身（stand-in）、锚点（课件里的 anchor）、性格游戏（the personality game），沿用第 4 讲的关卡（gates）、电话簿（phone book）和门（发布出去的 host port）。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、仓库、克隆、提交、端口、提示词、系统提示词、文本块、嵌入向量、嵌入模型、集合（collection）、智能体（agent）。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **工具链的约束也是规则**：每个英文句子对应一个中文句子（140 段、358 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **chunk、embedding、collection、top K 说英文，书面写“文本块、嵌入向量、集合（collection）”**（A3、A4）。“切成 chunk”“embedding 模型”“建一个 collection”“取 top K”是实验课原话；embedding 和 prompt 本来就在系列清单（ac215-video skill）上；collection 是 Chroma 的词，也在画面上（char-split-collection）；top K 在课件和画面上都是这么写的。这一讲的 SAY 里没有 token，所以“token”的问题不出现。
- **名词说英文，动作说中文**：chunk（一块）↔ 分块（过程）、切成 chunk；embedding（模型和它的输出）↔ 向量化（动词 embed）；但 query 不进清单：名词动词都说“查询”，只有代码的 query 函数和 --query 那一步（query 这一步）照写（A3、A7）。用参数名指代 README 的一步时保留参数这个词：chunk 这一步、embed 这一步、load 这一步、到了 chat 这一步、两次 load。
- **其余 RAG 的词说中文，不为“味道”说英文**：vector → 向量（绝不写“矢量”）、vector database → 向量数据库、record → 记录、metadata → 元数据、index → 索引、dimension → 维度、nearest neighbors → 最近邻、filter → 过滤、context → 上下文、hallucination → 幻觉、fine-tune → 微调、overlap → 重叠（A1、A3）。
- **prompt 照说，书面写“提示词”**：final prompt → 最终的 prompt，system prompt 和 input prompt 照说（input prompt 是代码里的 INPUT_PROMPT，也是终端打印的标签；SYSTEM_INSTRUCTION 按 SAY 说 system prompt）。shell 的 prompt 永远是“提示符”（A7）。
- **相似度和距离方向相反**：余弦相似度（越高越好）↔ 余弦距离（越小越近，Chroma 报的是 1 减去相似度）；英文从不说 Euclidean，所以跟着说“直线距离”；点积（A3、A7）。
- **review_spoken 第 16 条的钉子**：通道（lane，量词“条”）、尺子（char-split）、剪刀（recursive-split）、地震仪（semantic-split）、接缝、保险、锚点、替身、空位（slots）；Step 1 / Step 2（README 概述给两条通道起的名字）保留英文，和进度条的“第 k 步”分开；所有勘误统一说“一个小疏漏”（A9）。唯一没采用的是“对外开放的门”：published door 沿用第 4 讲的“发布出去的门”。
- **带下划线的名字和检查器不收的符号**（A6、B3，同第 3、4 讲）：GCP_PROJECT → GCP project 这个变量；--chunk_type char-split → chunk type 用 char-split；chunk_overlap → chunk overlap 参数；generate_text_embeddings → generate text embeddings 这个函数；SERVICE_DISABLED / PERMISSION_DENIED → service disabled / permission denied；documents[0] → documents 的第 0 项；load() → load 这个词；one minus the similarity → 1 减去相似度；RRF 的公式用文字说。英文行用 en_display 给出字面形式（D4）。
- **命令不拆行**（G3）：整条命令放在全角冒号之后、分句末尾（第 2 步：python cli.py --chunk，chunk type 用 char-split。）；一行放不下的命令按 SAY 的说法称呼，让终端和英文行去显示。
- **书和引文**（A10）：书只用书名，绝不提作者（授课老师的短篇故事也不提名字）；The Complete Book of Cheese、Italian、accomplish、things、Chapter One 和 RRF 的例句 Chester went to the bank of the river in the morning 照画面写；教程问的问题和查询改写的例句是旁白自己的话，要翻译（Tolminc 奶酪是怎么做的？“海豚住在哪里”）。
- **钱**（A9）：按发送的文本付费，绝不说按次计费；89 次调用数的是调用次数，不是钱；按我们的估算只要几美分，以现行的价目表为准。
- **画面标签照画面写**（同第 2–4 讲）：黄色的 your turn 标签；旁白说的 the gray lecture tag → 灰色标签。旁白自己说的照常翻译：额外检查、进度条、代码面板（A11）。
- **录制时**：at the time of recording 每次都译“录制时”，绝不省略（Python 3.12.15、uv 0.13.1）。我们录制时没有 Google 的密钥：凡是调用 Google 的地方，字幕说“有密钥的话，要找的是……”；向量是“课程团队留下的向量”（A9、D6）。
- **系列清单里这一讲没说到的词**（A13）：volume 只出现在目录名 docker-volumes 里（实物：docker-volumes 目录，绝不写“卷”）；PATH、endpoint（心跳就是“心跳”）、LoRA（微调是第 8 讲）、CI、push 都没出现。
- **按英文时间轴读**：中文是边听英文边读的，每句中文读起来的时间要和英文听起来差不多；删掉多余的连接词和重复的主语，绝不删内容；长实物（llm-service-account.json、Gemini Enterprise Agent Platform User、semantic-split-collection、The Complete Book of Cheese）英文没重复的地方不要重复（D8）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令和子命令（git clone、mkdir secrets、cd llm-rag、git diff、git status、git pull、sh docker-shell.sh、docker compose run --rm、docker compose down、docker compose build、docker ps -a、docker inspect、docker images、exit、sudo、python cli.py）、cli.py 的参数（--chunk、--embed、--load、--query、--chat、--get）和 chunk type 的值（char-split、recursive-split、semantic-split）、文件名和路径（cli.py、docker-shell.sh、docker-compose.yml、Dockerfile、.gitignore、.dockerignore、llm-service-account.json、outputs、docker-volumes、secrets、~/AC215、/app、/secrets、/data、/.venv）、名字（llm-rag、llm-rag-cli、llm-service-account、latest、char-split-collection、recursive-split-collection、semantic-split-collection、gemini-embedding-001、gemini-3.1-flash-lite、your-project-id、代码里的 query、config、documents、$contains）、控制台标签和角色名（KEYS、JSON、Storage Admin、Gemini Enterprise Agent Platform User、Agent Platform、Vertex AI User）、旁白提到的屏幕标签（your turn、extra）、README 标题（Prerequisites）和 Step 1 / Step 2、书里和课上的原词（accomplish、things、Chapter One、Italian、The Complete Book of Cheese、Chester 那个例句）。完整清单见 A1（a）；带下划线的名字和检查器不收的符号例外（A6、B3）。
- 产品、组织、课程和名字：RAG、Self-RAG、Google、Google Cloud、Cloud Storage、Vertex AI、Gemini、Docker、Docker Hub、Docker Compose、Compose、Chroma、Chroma UI、SQLite、HNSW、Chrome、Git、Git Bash、WSL、Linux、Mac、Windows、Python、uv、pipenv、Project Gutenberg、JSON、AC215、MLOps Learning、Tolminc、Mara、Chester、student、app、root（A1 b）。
- 实验课口语，封闭清单：venv、root、repo、clone、commit、pin（第 1 讲）；container、image、Dockerfile、base image、tag、pull、pipeline、prompt（只指 LLM 的 prompt）、API、ID、port、localhost（第 2–4 讲）；**chunk（名词）、embedding（名词）、collection、top K、system prompt、input prompt、LLM、CLI、agent（这一讲新增）**。
- 系列清单里保留英文、但这一讲没说到的：volume（只作为目录名 docker-volumes 出现）、PATH、endpoint、LoRA、CI、push（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| retrieval augmented generation | 检索增强生成 | retrieval / retriever | 检索 / 检索器 |
| generation / augmentation | 生成 / 增强 | context | 上下文 |
| knowledge base | 知识库 | language model / the model | 语言模型 / 模型 |
| hallucination | 幻觉 | fine-tune / retrain / weights | 微调 / 重新训练 / 权重 |
| chunking / chunker | 分块 / 分块器 | splitting / splitter | 切分 / 切分器 |
| character splitting | 按字符切分 | recursive splitting | 递归切分 |
| semantic chunking | 语义分块 | overlap / separator | 重叠 / 分隔符 |
| embed（动词） | 向量化 | vector / query vector | 向量 / 查询向量 |
| a list of numbers | 一串数字 | dimension / batch | 维度 / 批 |
| vector database | 向量数据库 | record / metadata | 记录 / 元数据 |
| index / build an index | 索引 / 建索引 | full rebuild / rebuild the index | 完全重建 / 重建索引 |
| query（名词、动词） | 查询 | the question / ask | 问题 / 提问 |
| nearest neighbors | 最近邻 | score / sort / rank | 分数 / 排序 / 排名 |
| similarity / cosine similarity | 相似度 / 余弦相似度 | cosine distance | 余弦距离 |
| dot product | 点积 | straight-line distance | 直线距离 |
| angle / length / direction | 夹角 / 长度 / 方向 | measure | 度量 |
| distance threshold | 距离阈值 | percentile / threshold | 百分位 / 阈值 |
| filter / metadata filter | 过滤 / 元数据过滤 | keyword filter / keyword ranking | 关键词过滤 / 关键词排序 |
| the model's response | 模型的回答 | grounded answers | 有依据的回答 |
| naive RAG / naive retrieval | 朴素 RAG / 朴素检索 | advanced lever | 进阶手段 |
| pre-retrieval / post-retrieval | 检索前 / 检索后 | query rewriting | 查询改写 |
| hybrid search | 混合检索 | reciprocal rank fusion | 倒数排名融合 |
| re-ranking / candidates | 重排序 / 候选 | three phases（Indexing …） | 三个阶段（索引阶段……） |
| lane | 通道 | box | 方框 |
| ruler / scissors / seismograph | 尺子 / 剪刀 / 地震仪 | seam / insurance | 接缝 / 保险 |
| anchor（课件）/ stand-in | 锚点 / 替身 | librarian / open-book exam | 图书管理员 / 开卷考试 |
| service account / key | 服务账号 / 密钥 | role / three gates | 角色 / 三道关卡 |
| enable / switch on | 启用 / 打开 | Project ID | 项目 ID |
| build / build context | 构建 / 构建上下文 | rebuild（image） | 重新构建 |
| Compose service / slots | 服务 / 空位 | network / phone book | 网络 / 电话簿 |
| mount / hide | 挂载 / 盖住 | the published door | 发布出去的门 |
| heartbeat | 心跳 | the container's prompt | container 的提示符 |
| tear down | 拆掉 | a small slip | 一个小疏漏 |
| at the time of recording | 录制时 | an extra check | 额外检查 |
| the staff / the instructor | 课程团队 / 授课老师 | the lecture / the slides | 课上 / 课件 |
| the tracker | 进度条 | step k（README tracker） | 第 k 步 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的一个中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### RAG：概念与课上的框架 / RAG: the idea and the lecture's frame

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| RAG / retrieval augmented generation / That's RAG / the RAG code / the RAG box | RAG / 检索增强生成 / RAG 代码 | S01[2]：RAG，也就是检索增强生成，针对的是前两个。 | RAG 照写（缩写，可以开头，A5）。书面写“检索增强生成（RAG）”。the RAG box → RAG 这个方框。 |
| language model / LLM / the model / trained before that story existed / retraining / weights / the model's memory | 语言模型 / LLM / 模型 / 重新训练 / 权重 / 模型的记忆 | S01[1]：怎样让它根据这个故事回答，又不用重新训练？ | LLM 照写（A1 c），和图上蓝色的方框一致；英文说 language model 时译“语言模型”。No weights moved → 权重一个都没动。 |
| fine-tune / fine-tuning / lecture 8 | 微调 | S01[3]：微调模型呢，又很慢；那是第 8 讲的内容。 | 标准中文；字幕里绝不写 fine-tune（A13）。 |
| four weaknesses / stale training data / specialized knowledge / hallucination / no sources | 四个弱点 / 训练数据过时 / 缺少专业知识 / 幻觉 / 没有出处 | S01[2]：课上列出了四个弱点：训练数据过时、缺少专业知识、幻觉，以及没有出处。 | goes after the first two → 针对的是前两个。 |
| knowledge base / eleven books / old cheese books / the instructor's short story / fictional tale / one particular text | 知识库 / 老书 / 短篇故事 / 虚构的故事 | S01[1]：知识库一共是 11 本书：10 本 Project Gutenberg 上讲奶酪的老书，加上授课老师写的一个短篇故事，一个虚构的故事。 | A10：故事绝不提作者名。11 本书用阿拉伯数字（C1）。 |
| librarian / open-book exam / ten most relevant pages / garbage / paste into the prompt | 图书管理员 / 开卷考试 / 垃圾 | S01[3]：或者让一位图书管理员，把最相关的 10 页递给它：一场开卷考试。 | 我们的比喻（S01）和课上的（B69–B71），各用一个词。you get garbage → 得到的是一堆垃圾。 |
| map of RAG techniques / four questions / This video answers all four | RAG 技术全景图 / 四个问题 | S01[4]：课上那张 RAG 技术全景图很拥挤，但它是从四个问题出发的。 | S16[6] 回答这四个问题：And the four questions? → 那四个问题呢？ |
| box / four boxes / the RAG box / full prompt / related texts / never talks to the model | 方框 / 完整的 prompt / 相关的文本 | S02[0]：数据库从不和模型直接对话。 | V1 的方框。Here's RAG in four boxes → 用四个方框讲清 RAG。 |
| lane / two lanes / top lane / bottom lane / runs once / offline / every question | 通道 / 两条通道 / 上面那条通道 / 下面那条通道 / 离线 | S02[4]：上面的通道只跑一次，离线跑，而且很慢。 | review_spoken 第 16 条定下的词，script.md 开头要求照用；量词“条”。绝不说“车道”“链路”。The top lane is done → 上面这条通道完成了。 |
| Indexing / Retrieval / Augmentation & Generation / three phases / pipeline slide | 索引阶段 / 检索阶段 / 增强和生成 / 三个阶段 | S02[2]：这就是课上那页讲 pipeline 的课件，分三个阶段。 | 课上 B5 的三个阶段。Indexing is the whole top lane → 索引阶段就是上面整条通道；Indexing starts with chunking（S06）→ 建索引从分块开始。 |
| pre-retrieval / post-retrieval / stage / frame / advanced lever / ideas only | 检索前 / 检索后 / 检索前阶段 / 检索后阶段 / 框架 / 进阶手段 | S15[0]：语义分块属于检索前：这是这个教程唯一实现了的进阶手段。 | as ideas only → 只讲思路。 |
| naive RAG / naive retrieval / Beyond naive RAG / advanced RAG | 朴素 RAG / 朴素检索 / 高级 RAG | S15[5]：你会用上它们，是在朴素检索取回了错的 chunk 的时候；而我们那个带过滤的查询，只需要把过滤去掉。 | Naive RAG / Advanced RAG 的通行中文名（“高级 RAG”只用于书面；SAY 说 advanced lever → 进阶手段）。 |
| step 1 and step 2 (the README's two lanes) / Step 1 / Step 2 | Step 1 / Step 2 | S02[3]：README 把两条通道叫作 Step 1 和 Step 2，并给每个方框配了 cli.py 的一个参数：上面是 --chunk、--embed 和 --load，下面是 --query 和 --chat。 | A7：README 概述给两条通道起的名字，保留英文，免得和进度条的“第 k 步”混淆。 |

### 分块 / Chunking

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| chunk / chunks / chunk files / chunk count / chunk size / chunk boundaries / chunk 0 / chunk 1 | chunk / chunk 文件 / chunk 数 / chunk 大小 / chunk 边界 / 文本块（书面） | S06[0]：一个 chunk 小到可以被找到，也小到可以贴进去。 | A3：名词照说，量词“个”；复数不变形；句首写“第 0 个 chunk”“这些 chunk”（A5）。书面写“文本块”。 |
| chunking / chunker / chunk them / the chunk step / chunk, embed and load | 分块 / 分块器 / chunk 这一步 | S02[5]：分块器在你自己的 container 里运行。 | A3。the chunk step（--chunk 那一次运行）→ chunk 这一步；作为动作说“分块”。 |
| splitting / splitter / character splitting / char split / recursive splitting / recursive splitter / semantic splitting | 切分 / 切分器 / 按字符切分 / 递归切分 / 递归切分器 / 语义切分 / char-split / recursive-split / semantic-split | S07[0]：递归切分只给了 chunk 大小，还是 350。 | A3。SAY 说出 --chunk_type 的值时照画面写（Char split ran the chunk step → 用 char-split 时，……；Step 2 does the same for recursive split → 第 2 步对 recursive-split 做同样的事）。 |
| chunk type / chunk type char split / one per chunk type / the chunk type's collection | chunk type | S06[5]：第 2 步：python cli.py --chunk，chunk type 用 char-split。 | A6：中文行里绝不写 --chunk_type；en_display 给出 python cli.py --chunk --chunk_type char-split（D4）。Compare both chunk types → 比较两种 chunk type 的结果。 |
| ruler / window / windows of 350 characters / overlapping by 20 / separator / stepping 330 at a time | 尺子 / 窗口 / 分隔符 / 字符 | S06[2]：分隔符是空的，所以它数的是字符，不是单词，每次前进 330 个。 | V3。Character splitting is a ruler → 按字符切分就是一把尺子。Lines 185 and 186 → 第 185 和 186 行。 |
| scissors / best gap / blank line / paragraphs / line break / space / last resort / every cut falls between words | 剪刀 / 空行 / 段落 / 换行 / 空格 / 切点 | S07[1]：它就像一把会找最佳缝隙的剪刀。 | V3 的 recursive-split。only as a last resort, a single character → 实在不行才切在单个字符上。 |
| overlap / hidden overlap / library default / up to 200 characters / chunk overlap / insurance | 重叠 / 默认值 / 保险 / chunk overlap 参数 | S07[5]：重叠是一份保险，防止把一个意思切成两半。 | The splitter's library default → 这个切分器所在的库的默认值；chunk_overlap 按 A6 写（set chunk overlap yourself → 自己设置 chunk overlap 参数）。 |
| seam / two letters into the word / backs up 20 characters / the last letter of / whole again | 接缝 | S06[7]：第 0 个 chunk 停在 accomplish 这个词的前两个字母上。 | 切开的单词 accomplish 和 things 照画面写（A10）。An extra look at the seam → 额外看一眼接缝。 |
| document's own structure / ideal chunks / goes part of the way / goes further | 文档自身的结构 / 理想的 chunk | S07[6]：课上的观点是：理想的 chunk 应该顺着文档自身的结构。 |  |
| Gutenberg header / closing license / license text / title page / contents / strip them before chunking | 开头声明 / 许可证 / 许可证文本 / 书名页 / 书的目录 | S12[7]：这段声明，还有每本书结尾的许可证，都会像普通文本一样被建进索引：先把它们去掉，再分块。 | A7：书的 contents → 书的目录，绝不单写“目录”（那是文件夹）。Row 0 of a Gutenberg book → Gutenberg 的书的第 0 行。 |
| chunk visualizer / sliders / a link / the course's web tools / Chroma UI / chat tool / Chrome | chunk 可视化工具 / 滑块 / 链接 / 网页工具 / Chroma UI / 对话工具 / Chrome | S06[1]：第 1 步是一个链接：README 里的 chunk 可视化工具。 | README 里的链接，画成浏览器窗口。Open it in Chrome and play with the sliders → 在 Chrome 里打开，拖拖滑块。 |

### embedding 与向量 / Embeddings

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| embedding / embeddings / embedding model / embedding call / embedding values / embedding column / embeddings files | embedding / embedding 模型 / embedding 调用 / embedding 值 / embedding 列 / embeddings 文件 / 嵌入向量（书面）/ 嵌入模型（书面） | S08[0]：接下来是 embedding 模型。 | A3、A13：系列清单保留英文。句首：所谓 embedding，就是……（S16[6]）。书面：嵌入向量、嵌入模型。 |
| embed / is embedded / embed every sentence window / embedding the question / your embed step | 向量化 / embed 这一步 | S14[5]：要找出意思在哪里转折，它得先把每个句子窗口都向量化。 | A3：动词是“向量化”；--embed 那一次运行是 embed 这一步（If you see 0, your embed step didn't finish → 如果你看到 0，说明你的 embed 那一步没跑完）。 |
| vector / vectors / a list of numbers / query vector / document vectors / five-number vector | 向量 / 一串数字 / 查询向量 / 五维向量 | S08[0]：它把每个 chunk 变成一个向量，也就是一串数字，让意思相近的指向相近的方向。 | 绝不写“矢量”（A12）。 |
| direction / meaning / similar meanings / space / sketch / arrow / angle / length / point in similar directions | 方向 / 意思 / 空间 / 示意图 / 箭头 / 夹角 / 长度 | S08[0]：在这张示意图里，讲凝乳的挨着讲凝乳的，许可证文本在别处。 | An embedding is a direction for meaning → 所谓 embedding，就是表示意思的一个方向。用“意思”（口语），不用“语义”，“语义分块”除外（A3）。 |
| cosine similarity / cosine distance / cosine / dot product / straight-line distance / a measure / the usual one | 余弦相似度 / 余弦距离 / 余弦 / 点积 / 直线距离 / 度量 | S08[13]：要是用直线距离，也就是 Chroma 的默认值，或者用点积，长度就会渗进排名：这就是那个游戏的教训。 | 英文从不说 Euclidean，跟着英文写“直线距离”。Chroma reports cosine distance, one minus the similarity → Chroma 报的是余弦距离，也就是 1 减去相似度（B3）。 |
| personality game / five scores / the first candidate / the second candidate / the game's lesson | 性格游戏 / 候选人 | S08[1]：课上的性格游戏把这件事讲得很具体：三个候选人中哪个最像授课老师？ | 课上的例子（A40–A47）；绝不出现人名。 |
| dimension / 256 numbers / natively returns 3072 numbers / the first 256 / a prefix | 维度 / 前缀 | S08[3]：教程用的模型是 gemini-embedding-001，原生返回 3072 个数；代码只要前 256 个，模型训练时就让这段前缀单独也能用。 | C1：3072 不加千位分隔符。both collections now have dimension 256 → 两个 collection 现在的维度都是 256。 |
| batches of 100 / batches of 500 / API error / retries up to 5 times / doubling the wait / a 5-second pause | 批 / API 错误 / 重试 / 等待时间 / 停顿 | S08[4]：遇到 API 错误，它最多重试 5 次，等待时间从 5 秒开始逐次翻倍。 | Chunks go to the model in batches of 100 → 这些 chunk 每批 100 个发给模型。 |
| lengths from 0.369 to 0.402 / not 1 / shorter than 1 | 长度 | S08[11]：它们的长度在 0.369 到 0.402 之间，不是 1。 | C1。 |

### 向量数据库 / The vector database

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| vector database / ordinary database / precise questions / rows whose meaning is like a question | 向量数据库 / 普通数据库 | S09[0]：普通数据库回答的是精确的问题，比如价格在 10 到 50 之间，但它找不到意思和问题相近的行。 | A vector database can. → 向量数据库可以。 |
| record / records / an ID / the text / metadata / book, author and year / hashes the book's name plus the row number / stable | 记录 / 元数据 / 书名 / 作者 / 年份 / 哈希 / 行号 | S09[1]：这个 ID 是对书名加行号做哈希得到的，所以是稳定的。 | metadata with book, author and year → 包含书名、作者和年份的元数据（字幕里不出现代码里的键名）。10 record IDs → 10 条记录的 ID。 |
| collection / collections / one per chunk type / deletes it and creates it again / a full rebuild / inserts / the first insert | collection / 集合（书面）/ 完全重建 / 插入 | S09[2]：而 load 这一步先删掉它，再重新创建，用余弦作为度量：每次 load 都是完全重建。 | A3：Chroma 的词，口语照说；书面写“集合（collection）”。collection 的名字照写（char-split-collection、semantic-split-collection）。 |
| index / builds an index / layered graph / hops down in a few steps / at scale / index folders | 索引 / 建索引 / 分层的图 / 索引目录 / HNSW | S09[3]：所以数据库会建一个索引，就是这几页课件说的那种：一张叫 HNSW 的分层图，搜索几步就能一层层跳下来。 | en_display：H-N-S-W → HNSW（D4）。the index is built → 索引建好了。 |
| Chroma / Chroma service / Chroma container / Chroma's default / SQLite file / persistent / database file | Chroma / Chroma 服务 / SQLite 文件 / 持久化 / 数据库文件 | S09[9]：README 说它是持久化的。 | 产品名，可以开头（Chroma 先过滤……，A5）。画面上 Chroma 服务器的 image 是 chromadb/chroma:latest。 |
| heartbeat / the published door / for you and your browser / port 8000 / port 8000 is still taken / so port 8000 is free next time | 心跳 / 发布出去的门 / port 8000 | S05[3]：在你的笔记本上，心跳通过 localhost:8000 回来，这就是发布出去的那扇门，给你和你的浏览器用。 | 第 4 讲：发布出去的 host port 叫“门”，publish → 发布（review_spoken 建议的“对外开放的门”没有采用，和第 4 讲保持一致）。en_display：localhost port 8000 → localhost:8000。 |
| the docker volumes folder / Chroma's data folder / slash data / owned by root / deleting it later will need sudo | docker-volumes 目录 / 数据目录 / 属主是 root | S05[4]：Docker 已经在你的笔记本上建好了 Chroma 的数据目录，属主是 root，数据库文件就在里面。 | A13：目录名是实物；绝不写“卷”或 volume。en_display：the docker-volumes/ folder。 |

### 查询与过滤 / Query and filters

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| query / querying / a query / the query the code sends / the query function / ask the database | 查询 / query 函数 / 提问 | S11[0]：查询就是找它的最近邻。 | A3：名词和动词都是“查询”（review_spoken 第 16 条）；--query 那一次运行是 query 这一步；代码里的 query() 函数 → query 函数。 |
| nearest neighbors / its 10 nearest / score / scores every stored vector / sort by score | 最近邻 / 分数 / 打分 / 排序 | S11[1]：课上拿查询给每个存好的向量打分。 | C1：课上的数字用阿拉伯数字，用“、”隔开。 |
| top K / keep the top K / K fixed in advance / K results / relevant or not / its 10 places | top K / 结果 | S11[1]：按分数排序，保留 top K，K 是事先定好的。 | A3：top K 照说，和课件、画面一致；K 是一个字母。 |
| similarity / higher is better / smaller is closer / same order, opposite direction / distance threshold | 相似度 / 距离 / 距离阈值 | S11[2]：顺序一样，方向相反。 | Nothing in this code sets a distance threshold → 这份代码里没有任何地方设置距离阈值。 |
| filter / filters / metadata filter / document filter / the book filter / filters act first / whatever survives / however far | 过滤 / 过滤条件 / 元数据过滤 / 文档过滤 / 按书过滤 | S12[4]：过滤先起作用，top K 再用剩下的东西填满 10 个位置，不管有多远。 | The lecture puts metadata filtering after ranking → 课上把元数据过滤放在排序之后。 |
| contains / keyword filter / keyword ranking / keywords / rare words | $contains / 关键词 / 关键词过滤 / 关键词排序 / 罕见词 | S12[6]：还有，$contains 是关键词过滤，不是关键词排序。 | en_display：contains → $contains（D4）。Keywords pin down names → 关键词能锁定名字（绝不说 pin，那是第 1 讲的版本 pin）。 |
| variants / variant 4 / commented out / uncomment / every chunk competes / various filters | 注释掉 / 取消注释 / 竞争 | S12[6]：一个小疏漏：README 说有各种过滤，但只有第 4 种会运行；第 1 到 3 种都被注释掉了。 | C1。 |
| stand-in / the stored vector of one story chunk / the chunk itself / about the wrong cheese | 替身 / 别的奶酪 | S12[3]：所以我们用一个替身：故事里一个 chunk 存好的向量。 | 画面标签 stand-in query 保留英文（A11）。 |
| results / lists of lists / one list per query / IDs, distances, metadata and documents / documents, item zero | 结果 / 列表套列表 / 文档 / documents 的第 0 项 | S11[8]：所以后面 chat 这一步读的是 documents 的第 0 项。 | B3：中文行里绝不写 documents[0]；en_display：documents[0]（D4）。 |
| the word load / a label copied from the load code / connects to Chroma / stops at the key | 标签 | S11[5]：先说一个小疏漏：它打印的是 load 这个词，这个标签是从加载的代码里抄过来的。 | B3：中文行里绝不写 load()，写“load 这个词”；en_display：load()（D4）。 |
| an extra command called get / the get command / the restart check | --get / 重启后的检查 | S12[7]：重启后检查用的那条 --get 命令，用了同样的按书过滤，但没有问题，所以也没有距离。 | cli.py 的一个额外参数（cli-container/42、70）。en_display：--get（D4）。 |

### 生成（chat）/ Generation (chat)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| generation / chat / the chat step / Chat with LLM / the course's chat tool | 生成 / 对话 / chat 这一步 / 对话工具 | S13[1]：到了 chat 这一步，代码再查询一次，这次不加过滤，要 10 个结果。 | A3。Now generation. → 接下来是生成。 |
| prompt / final prompt / system prompt / the user's query / context / how to behave | prompt / 最终的 prompt / system prompt / 上下文 / 提示词（书面）/ 系统提示词（书面） | S13[0]：课上最终的 prompt 有三部分：规定模型行为的 system prompt、用户的查询，以及从数据库检索到的上下文。 | A3、A7：prompt 只指 LLM 的 prompt；shell 的 prompt 是“提示符”。书面写“提示词”“系统提示词”。 |
| input prompt / joined by newlines / followed by the 10 chunks | input prompt / 换行符 | S13[2]：然后它拼出 input prompt：先是问题，后面跟着 10 个 chunk，用换行符连起来。 | A6：代码里的 INPUT_PROMPT，也是它打印出来的标签。 |
| never sent / a config argument / a one-line fix / the older pipenv branch did send it / grounded answers | config 参数 / 有依据的回答 / pipenv 分支 | S13[4]：一个小疏漏，改一行就能修好：通过一个 config 参数把它传进去。 | Without it, the README's promise of grounded answers rests on the chunks alone → 没有它，README 承诺的有依据的回答就只能靠这些 chunk 了。 |
| response / answer / the model's response / real-world rules / Mara / her grandfather / the curd | 回答 / 现实中的规定 / 凝乳 / 祖父 | S13[8]：关于 Tolminc 的现实规定，来自模型的记忆。 | The story is fiction → 这个故事是虚构的。Mara 照写（A10）。 |
| Tolminc / Tolminc cheese / Alpine cheese / how is Tolminc cheese made / cheesemaking | Tolminc / Tolminc 奶酪 / 阿尔卑斯奶酪 / 奶酪 | S01[0]：这个教程要问语言模型一个问题：Tolminc 奶酪是怎么做的？ | A10：问题要翻译，名字照写。 |
| two question marks / a harmless slip / the number 10 | 问号 / 无害的小疏漏 | S13[7]：有密钥的话，要找的是查询，它打印出来带两个问号，一个无害的小疏漏，还有它的 256 个 embedding 值。 | A9。 |

### 语义分块 / Semantic chunking

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| semantic chunking / cut where the meaning changes / where the meaning shifts / anchor / joins neighbors / similarity stays above 0.8 | 语义分块 / 锚点 / 相邻的句子 | S14[0]：在课件上，一个锚点沿着这些句子一路往前走，把相邻的句子并进来，前提是相似度保持在 0.8 以上。 | 课件的版本；代码的规则见下一条。 |
| sentence window / one neighbor on each side / same ingredients, different rule | 句子窗口 / 材料 / 规则 | S14[1]：代码用的是同样的材料，规则却不一样。 | Every sentence gets a window, itself and one neighbor on each side → 每个句子都有一个窗口，包括它自己和两边各一个相邻的句子。 |
| seismograph / plots it over the text / 95th percentile / spike / the biggest 5 percent of gaps | 地震仪 / 百分位 / 第 95 百分位 / 尖峰 / 落差 | S14[3]：接着它在第 95 百分位画一条线，在每个超过这条线的尖峰处切开。 | review_spoken 第 16 条定下的词。gaps（窗口之间的距离）→ 落差：the biggest 5 percent of gaps → 最大的那 5% 的落差；cut at its biggest gaps → 在它最大的几处落差上切开。 |
| generate text embeddings / the function handed to the chunker / the same one the embed step uses | generate text embeddings 这个函数 | S14[5]：看看交给分块器的那个函数：generate text embeddings，和 embed 这一步用的是同一个。 | A6；en_display：generate_text_embeddings（D4）。 |
| budget for it / to chunk the corpus / one book first / put the others back / very uneven / single-topic book | 语料 / 很不均匀 | S14[7]：先只放一本书试试，再把其他的放回去，重新跑一遍。 | by our estimate, about 528 embedding calls → 按我们的估算，大约 528 次 embedding 调用。 |

### 课上的进阶 RAG（S15）/ The lecture's advanced RAG (S15)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| query rewriting / cluttered question / clean one / vague question / invent details | 查询改写 / 杂乱的问题 / 含糊的问题 | S15[1]：用一个模型把杂乱的问题改写成干净的问题，比如“海豚住在哪里”。 | A10：例句要翻译，放在“”里。 |
| hybrid search / keywords pin down names / vectors catch meaning / rank three paragraphs differently | 混合检索 | S15[2]：拿这个问题来说：Chester went to the bank of the river in the morning。 | A10：课上的例句保留英文（要点在 bank 这个词）。The two rank three paragraphs differently → 两种方法给三个段落排出的顺序不一样。 |
| reciprocal rank fusion / one half divided by its rank / adds them up / near paraphrase / wins with 0.75 | 倒数排名融合 / 二分之一 / 排名 / 改写 | S15[3]：倒数排名融合给每个段落记二分之一除以它的排名，每个列表各记一次，再加起来。 | B3：不写公式符号。The near paraphrase wins with 0.75 → 和问题几乎同义的那一段以 0.75 胜出。 |
| re-ranking / re-rank / fast retriever / slower model / 25 candidates / reorders them | 重排序 / 检索器 / 候选 / 重新排序 | S15[4]：检索之后：重排序。 | SAY 没有说出课上的 cross-encoder：a slower model → 一个更慢的模型。 |
| agent / next lecture's agent / retrieval tool / Self-RAG / decides whether to retrieve / checks what it found | agent / 检索工具 / Self-RAG / 智能体（书面） | S16[5]：下节课会用一个 agent 来跑这条命令。 | A13。Self-RAG 照写（课上的名字）。书面写“智能体（agent）”。 |
| stale index / transhumance / an older Tolminc book / replaced that same day / rebuild the index / what was loaded | 过期的索引 / 转场放牧 / 重建索引 | S16[4]：数据库只根据加载进去的内容回答：书一变，就要重建索引。 | A7：重建（索引），不是重新构建（image）。 |

### Google Cloud：账号、密钥、关卡、API 与费用 / Google Cloud: account, key, gates, API, cost

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| service account / llm-service-account / L-L-M service account / create one called | 服务账号 / llm-service-account | S03[2]：接下来是服务账号，在 Google Cloud 控制台里。 | 第 1–4 讲：服务账号。en_display：llm-service-account（D4）。 |
| role / roles / grant / Storage Admin / Gemini Enterprise Agent Platform User / the Agent Platform role / Vertex AI User | 角色 / 授予 / Storage Admin / Gemini Enterprise Agent Platform User / Agent Platform 这个角色 | S03[4]：这里没有任何东西用到 Cloud Storage，所以真正要紧的是 Agent Platform 这个角色。 | 角色名照控制台写（A1 a）；最长的那个单独占一个分句（G1）。 |
| key / JSON key / keys tab / add a JSON key / llm-service-account.json / spends your project's money | 密钥 / JSON 密钥 / KEYS 标签页 / llm-service-account.json | S03[2]：打开它的 KEYS 标签页，添加一个 JSON 密钥，存进 secrets 目录，命名为 llm-service-account.json。 | 第 3、4 讲。That key spends your project's money → 这个密钥花的是你项目的钱。Keep the key beside the repo → 把密钥放在 repo 旁边。 |
| three gates / who you are / what you may do / must be switched on | 三道关卡 | S03[3]：还记得第 4 讲的三道关卡吗：密钥说明你是谁，角色说明你能做什么，API 还必须打开。 | 第 4 讲：关卡；绝不说“门”（那是发布出去的 port）。 |
| API / Vertex AI API / enable / switch on the API / service disabled / permission denied / key file not found | API / Vertex AI API / 启用 / 打开 / service disabled / permission denied / 找不到密钥文件 | S08[8]：报 service disabled：把 API 打开。 | A6：SERVICE_DISABLED 和 PERMISSION_DENIED 按 SAY 写成小写、空格分开，en_display 给出字面形式（D4）。Key file not found 是 SAY 自己的转述 → 找不到密钥文件。 |
| project / Project ID / the ID, not the name / your-project-id / the course's project / GCP project / line 7 / leave line 8 alone | 项目 / 项目 ID / 项目名称 / your-project-id / 课程的项目 / GCP project 这个变量 | S03[6]：第 2 步在编辑器里做：把第 7 行的 GCP project 变量改成自己的项目 ID，是 ID，不是项目名称。 | 第 4 讲：项目 ID。A6：GCP_PROJECT。Skip this, and your calls go to the course's project and fail → 跳过这一步，你的调用就会发到课程的项目上，然后失败。 |
| console / Google Cloud console / in your editor | 控制台 / 编辑器 | S03[2]：接下来是服务账号，在 Google Cloud 控制台里。 | 第 1 讲。示意控制台保留英文标签（A11）。 |
| pay / you pay for the text you send / nothing keeps running there / calls / a few cents by our estimate / the current price list | 付费 / 调用 / 几美分 / 价目表 | S02[5]：两个模型都在 Google 那边运行：你用自己的密钥，按发送的文本付费，那边没有任何东西一直开着。 | A9：绝不说按调用次数计费；我们数的是调用次数。 |
| Google client / creates its Google client / looking for a key file with no name / dies at startup | Google 客户端 | S05[5]：两个变量都是空的，连分块都在启动时就挂了：cli.py 在那里创建 Google 客户端，去找一个没有名字的密钥文件。 | 第 4 讲。 |

### Docker、Compose 与两个 container / Docker, Compose, the two containers

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| container / image / Dockerfile / base image / its Python base included / the CLI container / the Chroma container / CLI image | container / image / Dockerfile / base image / CLI container / 容器（书面）/ 镜像（书面） | S04[0]：第 4 讲把两个 container 放在一个网络上；第 3 讲通过挂载把密钥带了进来。 | A2（第 2–4 讲）。CLI 照写（A1 c）。 |
| tag / the image tag called latest / pin a tag / three version numbers that don't match / oddity | tag / latest / 版本号 / 怪现象 | S05[7]：最后一个怪现象：image 的 tag 叫 latest，而三个版本号对不上；团队应该 pin 一个固定的 tag。 | 第 1 讲的 pin，第 2 讲的 tag。 |
| pull / pulls Chroma's image / No pull, no build / git pull / dependencies / docker compose build | pull / 依赖 / docker compose build | S10[4]：不 pull，也不构建：image 已经有了。 | A2。 |
| build / builds it instead / build context / 112 megabytes / git history / no docker ignore file / no rebuild | 构建 / 构建上下文 / git 历史 / .dockerignore 文件 / 重新构建 | S04[8]：构建上下文有 112 MB，大部分是留着课程团队数据库旧拷贝的 git 历史。 | A7：构建上下文，绝不单写“上下文”。en_display：.dockerignore（D4）。 |
| docker-shell.sh / the script / exports three values / the key's path inside the container / the image name / always start through the script | docker-shell.sh / 脚本 / 三个值 / 密钥的路径 / image 名 | S04[1]：这个脚本 docker-shell.sh 导出三个值：你的项目、密钥在 container 里的路径，还有 image 名。 | 第 4 讲。GOOGLE_APPLICATION_CREDENTIALS 从不写出来（A6）。 |
| Docker Compose / Compose / docker-compose.yml / the compose file / compose run / docker compose run / dash dash r m / that one service | Docker Compose / Compose / docker-compose.yml / compose 文件 / docker compose run / --rm | S04[1]：然后它调用 docker compose run，加上 --rm，只跑那一个服务。 | 第 4 讲。en_display：--rm（D4）。compose run ignores that name → compose run 会忽略这个名字。 |
| service / the CLI service / the Chroma service / depends on Chroma / slots / the script's values / a fixed name | 服务 / CLI 服务 / 空位 / 固定的名字 | S04[3]：两个空位接收脚本给的值，这个服务还依赖 Chroma。 | 第 4 讲：Compose 的 service → 服务。slots → 空位（review_spoken 第 16 条）。 |
| network / one network, by name / phone book / finds Chroma by name / lets the course's web tools in | 网络 / 电话簿 / 按名字 | S05[3]：CLI 通过网络的电话簿，按名字找到 Chroma。 | 第 4 讲：电话簿 = Docker 按名字查找；字幕里绝不写 DNS。 |
| mount / mounts / two mounts / the code mount / slash app / slash secrets / slash dot venv / can't hide it | 挂载 / 两个挂载 / /app / /secrets / /.venv / 盖住 | S04[3]：两个挂载把这个 repo 放到 /app，把 secrets 放到 /secrets。 | 第 4 讲：hide → 盖住。en_display：/app、/secrets、/.venv（D4）。 |
| virtual environment / lives in slash dot venv / outside slash app / rerun / no rebuild | 虚拟环境 | S04[5]：在笔记本上改 cli.py，再跑一次就行；不用重新构建。 | 第 1 讲 A2：英文说 virtual environment，就译“虚拟环境”。 |
| banner / activated / cosmetic / Python 3.12.15 / uv 0.13.1 | 横幅 / 已激活 / 显示问题 | S04[9]：它在激活之前就说已经激活了：只是显示问题。 | 第 1 讲：banner → 横幅。at the time of recording → 录制时（A9）。 |
| the container's prompt / the at sign / the container's ID / changes every run | 提示符 / @ 符号 / container ID | S04[10]：提示符里 @ 符号后面是 container ID；每次运行都会变。 | 第 4 讲。A7：提示符，绝不写 prompt。 |
| second laptop terminal / check the picture with extras / docker ps / docker inspect / docker ps dash a / port 8000 published | 第二个终端 / docker ps / docker inspect / docker ps -a | S05[0]：用 docker ps 这条命令可以看到 Chroma，port 8000 已经发布出去了。 | 第 4 讲。en_display：docker ps -a（D4）。 |
| traps / trap one / trap two / hit on purpose / what if / typing the compose command yourself / both variables come out blank | 陷阱 / 陷阱一 / 陷阱二 / 空的 | S05[5]：接下来是两个陷阱，我们故意踩一下。 | 画面上的框 what if · just watch 保留英文（A11）。 |
| a clone with another name / zip download / an empty one, owned by root, over your code / the stray folder / keep the name | zip 包 / 多出来的目录 / 属主 | S05[6]：名字保持不变，再把多出来的那个目录删掉。 | like the folder a zip download gives you → 比如下载 zip 包解压出来的那种目录。 |
| exit / removed on exit / still up / docker compose down / two warnings / the variables aren't set / harmless / the down command needs neither | 退出 / 警告 / 无害 / docker compose down | S10[2]：它们无害：只有脚本会设置这两个变量，而 down 这条命令两个都不需要。 | 第 4 讲。 |
| restart / Back another day / disposable / the data never lived in it / untouched | 重新启动 / 一次性的 / 原封未动 | S10[5]：那个 container 是一次性的；数据从来不住在它里面。 |  |
| tear down / the images stay / git status / your edit / ignored / stay on your disk / delete it when the course ends | 拆掉 / 拆除（书面）/ git status / 改动 / 被忽略 | S16[2]：而 outputs 和 docker-volumes 两个目录都被忽略，留在你的磁盘上。 | 第 4 讲。Time to tear down. → 该拆掉了。 |

### repo 和里面的文件 / The repo and its files

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| repo / clone / the clone's name exactly L-L-M rag / the clone command / course folder / secrets folder / beside the clone | repo / clone / clone 命令 / 课程目录 / secrets 目录 / llm-rag / 仓库（书面）/ 克隆（书面） | S03[1]：然后额外做一件事：在 clone 旁边建一个 secrets 目录，并且让 clone 的名字一字不差地叫 llm-rag。 | 第 1、4 讲。en_display：llm-rag（D4）。 |
| commit / the commit this video was recorded on / once committed / every clone's history / byte for byte | commit / 历史 / 逐字节 | S08[10]：他们的 chunk 文件和我们的逐字节相同，所以他们的向量就是这条命令会生成的向量。 | 第 1 讲。The staff's own outputs, once committed → 课程团队自己的输出，曾经 commit 过。 |
| cli.py / python cli.py / flag / one flag of cli.py / line 40 / line 372 / the code | cli.py / python cli.py / 参数 / 代码 | S02[6]：每一步都是一条 python cli.py 命令，在第一个 container 里运行。 | 第 1 讲：flag → 参数。 |
| the git ignore file / git ignores them / outputs / the chunk files land in outputs | .gitignore 文件 / outputs 目录 | S06[8]：这些 chunk 文件落在 outputs 目录里，就在你的笔记本上，git 会忽略它们。 | en_display：the .gitignore file、outputs/（D4）。 |
| file name / the first dot / extension / split off only the extension / delete that book's old files | 文件名 / 扩展名 | S09[8]：只去掉扩展名，删掉 outputs 目录里这本书的旧文件，然后重新分块、向量化、加载。 | a small slip cuts its file name at the first dot → 一个小疏漏：代码在第一个点就把文件名截断了。 |

### 带下划线的名字（A6）/ Names with an underscore (A6)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| GCP_PROJECT / --chunk_type / chunk_overlap / generate_text_embeddings / SERVICE_DISABLED / PERMISSION_DENIED / INPUT_PROMPT / SYSTEM_INSTRUCTION / GOOGLE_APPLICATION_CREDENTIALS | GCP project 这个变量 / chunk type / chunk overlap 参数 / generate text embeddings 这个函数 / service disabled / permission denied / input prompt / system prompt / 密钥的路径 | S07[2]：第 3 步：同一条命令，chunk type 换成 recursive-split。 | A6；字面形式只出现在 en_display 里。 |

### 标签、进度条与固定句式 / Tags, tracker, fixed patterns

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the tracker / the gray tag / the lecture slides / the yellow your-turn tag / extra commands / study guide / exercises | 进度条 / 灰色标签 / 课件 / your turn 标签 / 额外的命令 / 学习指南 / 练习 | S01[5]：左上角的进度条显示当前步骤；右上角的灰色标签指向课件。 | A11：标签名照画面写（第 2–4 讲）。 |
| an extra check / extras / an extra look / an extra line count / not in the README / Leaving isn't in the README | 额外检查 / 额外的命令 / README 里没有 | S06[6]：额外数一下 chunk 文件的行数：故事是 24 行，一共 8248 行。 | D6。 |
| at the time of recording / we recorded without a Google key / ran for real / the real error / what to look for | 录制时 / 真实运行 / 真实的报错 / 该看什么 | S01[6]：凡是代码调用 Google 的地方，你会看到命令、真实的报错，以及该看什么。 | A9：绝不省略。 |
| the staff's recorded vectors / the staff's own outputs / the staff's recorded run / the staff's database | 课程团队 / 课程团队留下的向量 / 课程团队的输出 / 运行记录 | S01[6]：Docker、分块和数据库都是真实运行的；embedding 用的是课程团队留下的向量。 | 第 3 讲：the staff → 课程团队。画面上的 recorded 标签保留英文（A11）。 |
| with your key, look for / if yours fails / keeps retrying / read the error | 报错 / 重试 | S08[7]：有密钥的话，要找的是每本书的文件、5 秒的停顿、一张带 embedding 列的表，以及 chunk 旁边新出现的 embeddings 文件。 | D6。 |
| a small slip / two small slips / a harmless slip / a one-line fix | 一个小疏漏 / 两个小疏漏 / 无害的小疏漏 | S03[4]：两个小疏漏。 | A9：所有勘误用同一个说法（review_spoken 第 16 条），后面一定紧跟改法。 |
| Five questions to test yourself / One: … Five: / The answers are in the exercises / Next time: agents | 自测 / 第一题 / 第五题 / 答案在练习里 / 下节课 | S16[7]：五道题，自测一下。 | D6。 |
| part 1 / part 2 / lecture 3 / lecture 4 / lecture 8 / this video / next lecture / the next section | 第一部分 / 第二部分 / 第 3 讲 / 第 4 讲 / 第 8 讲 / 下节课 / 下一节 | S09[11]：第二部分，我们来向它提问。 | A10。this video → 这期视频。 |

### 数字与单位 / Numbers and units

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| line 7 / line 8 / lines 185 and 186 / line 40 / line 372 / row 0 / step 1 / step 3 | 第 7 行 / 第 185 和 186 行 / 第 372 行 / 第 0 行 / 第 1 步 / 第 3 步 | S13[9]：想问你自己的问题，就改 cli.py 的第 372 行。 | C1。 |
| counts: 11 books / 24 chunks / 35 chunks / 8248 / 14228 / 1355 / 64 / 10 results / 7808 characters / 7458 more characters / 23 more windows | 24 个 chunk / 8248 个 / 14228 个 / 10 个结果 | S06[4]：剩下的 7458 个字符还要 23 个窗口：一共 24 个 chunk。 | C1：数字不加千位分隔符，和终端打印的一样；11 本书、11 个文件。 |
| sizes and times: 81 seconds / 112 megabytes / 60-megabyte / 2.11 gigabytes / 826 megabytes / 10 to 20 minutes | 81 秒 / 112 MB / 60 MB / 2.11 GB / 826 MB / 10 到 20 分钟 | S16[1]：这些 image 还在：CLI 的 image 有 2.11 GB，包括它的 Python base image；Chroma 的有 826 MB。 | C2。 |
| versions and models: Python 3.12.15 / uv 0.13.1 / Gemini embedding 001 / Gemini 3.1 Flash Lite | Python 3.12.15 / uv 0.13.1 / gemini-embedding-001 / gemini-3.1-flash-lite | S13[2]：这个 prompt 发给 gemini-3.1-flash-lite。 | C2：模型 ID 照代码写，中英两行都一样（D4）。 |
| dates: October 16, 2026 | 2026 年 10 月 16 日 |  | C2（S01 的卡片；简介）。 |

### 课程、产品与名字 / Course, products, names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / MLOps Learning / the study guide / the instructor / the staff / the course's project | AC215 / MLOps Learning / 学习指南 / 授课老师 / 课程团队 | S16[9]：答案在练习里，每条命令都在学习指南里，就在 MLOps Learning 这个 repo 里。 | A10。 |
| llm-rag / llm-rag-cli / L-L-M rag / L-L-M rag CLI / student / app / root / laptop | llm-rag / llm-rag-cli / student / app / root / 笔记本 | S05[0]：但 CLI container 并不叫 llm-rag-cli：compose run 会忽略这个名字。 | A10。laptop → 笔记本（第 1 讲）。en_display：llm-rag、llm-rag-cli（D4）。 |
| products: Google / Google Cloud / Cloud Storage / Vertex AI / Gemini / Docker / Docker Hub / Chroma / SQLite / HNSW / Chrome / Git Bash / WSL / Linux / Mac / Windows / Python / uv / pipenv / JSON / Project Gutenberg | Google / Google Cloud / Cloud Storage / Vertex AI / Gemini / Docker / Docker Hub / Chroma / SQLite / HNSW / Chrome / Git Bash / WSL / Linux / Mac / Windows / Python / uv / pipenv / JSON / Project Gutenberg | S03[0]：在 Mac 上，提示符看起来不一样；在 Windows 上，用 WSL 或 Git Bash。 | 拉丁字母（A1 b）。 |
| quoted text: accomplish / things / Chapter One / Italian / The Complete Book of Cheese / Chester went to the bank of the river in the morning | accomplish / things / Chapter One / Italian / The Complete Book of Cheese | S12[0]：元数据过滤只留一本书：The Complete Book of Cheese。 | A10：书里和课上的原词照画面写，从不加引号。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 中文 | 说明 |
|---|---|---|
| Video title | AC215 · 第 5 讲：RAG 入门（跟练：llm-rag） | H1。Introduction to RAG → RAG 入门；跟练 = follow-along。 |
| Part 1 title / Part 2 title | AC215 · 第 5 讲（上）：建索引——分块、向量化、加载 / AC215 · 第 5 讲（下）：查询索引——查询、过滤、对话与语义分块 | H1。 |
| Chapters S01-S08: A model that never read the book / Two lanes, one database / Your key, your folders, your project / One script, two containers / Names, mounts, and two traps / Cutting the books: a ruler / Recursive split and its hidden overlap / Meaning as direction: embeddings | 一个没读过这本书的模型 / 两条通道，一个数据库 / 你的密钥、你的目录、你的项目 / 一个脚本，两个容器 / 名字、挂载和两个陷阱 / 切书：一把尺子 / 递归切分和藏起来的重叠 / 意思即方向：嵌入向量（embedding） | H1，书面语体。 |
| Chapters S09-S16: Load: records, an index, a folder on your disk / Exit, and the index survives / Asking the database: rank and cut / Filters come first / Chat: the prompt is the whole trick / Semantic chunking: cut where meaning shifts / Beyond naive RAG: what the lecture adds / Tear down, a stale index, recap | 加载：记录、索引和你磁盘上的一个目录 / 退出之后，索引还在 / 向数据库提问：排序与截断 / 过滤在前 / 对话：诀窍全在提示词（prompt） / 语义分块：在意思转折处切开 / 朴素 RAG 之外：课上补充的内容 / 清理、过期的索引与回顾 | H1。 |

### 配套材料的书面语体 / Written register of the companions

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| written register for the companions: container / image / base image / repo / clone / commit / port / prompt / system prompt / chunk / embedding / embedding model / collection / agent / top K / overlap | 容器 / 镜像 / 基础镜像 / 仓库 / 克隆 / 提交 / 端口 / 提示词 / 系统提示词 / 文本块 / 嵌入向量 / 嵌入模型 / 集合 / 智能体 / 前 K 个 / 重叠 |  | H3、A4：在配套材料里首次出现时加英文括注。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

AC、Admin、Agent、AI、API、app、Bash、Book、build、cd、Cheese、Chapter、char-split、char-split-collection、chat、Chester、Chroma、Chrome、chunk、CLI、cli.py、clone、Cloud、collection、commit、Complete、compose、Compose、config、container、contains、data、diff、docker、Docker、docker-compose.yml、docker-shell.sh、docker-volumes、Dockerfile、dockerignore、documents、down、embed、embedding、embeddings、Enterprise、exit、extra、flash-lite、gemini-、Gemini、gemini-embedding-、get、git、Git、gitignore、Google、GB、history、HNSW、Hub、ID、image、images、input、inspect、Italian、JSON、KEYS、latest、Learning、Linux、LLM、llm-rag、llm-rag-cli、llm-service-account、llm-service-account.json、load、localhost、ls、Mac、Mara、MB、mkdir、MLOps、of、outputs、pin、pipeline、pipenv、Platform、port、Prerequisites、prompt、ps、pull、Python、python、query、RAG、README、recursive-split、recursive-split-collection、repo、rm、root、run、secrets、Self-RAG、semantic-split、semantic-split-collection、sh、SQLite、status、Step、Storage、student、sudo、system、tag、The、Tolminc、top、turn、type、UI、User、uv、venv、Vertex、Windows、WSL、your、your-project-id。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（git clone、mkdir secrets、ls、cd llm-rag、cd ..、git diff、git status、git pull、sh docker-shell.sh、docker compose run --rm、docker compose down、docker compose build、docker compose version、docker ps、docker ps -a、docker inspect、docker images、exit、sudo、python cli.py）、cli.py 的参数（--chunk、--embed、--load、--query、--chat、--get；--chunk_type 见 A6）和 chunk type 的值（char-split、recursive-split、semantic-split）、文件名、目录名和路径（cli.py、docker-shell.sh、docker-compose.yml、Dockerfile、.gitignore、.dockerignore、llm-service-account.json、outputs、docker-volumes、secrets、~/AC215、/app、/secrets、/data、/.venv）、名字（llm-rag、llm-rag-cli、llm-service-account、latest、char-split-collection、recursive-split-collection、semantic-split-collection、gemini-embedding-001、gemini-3.1-flash-lite、your-project-id，以及代码里的 query、config、documents 和 $contains）、环境变量（GCP_PROJECT，见 A6）、控制台标签和角色名（KEYS、JSON、Storage Admin、Gemini Enterprise Agent Platform User、Agent Platform、Vertex AI User）、终端原文和报错名（service disabled 和 permission denied，见 A6）、旁白提到的画面标签（your turn、extra；A11）、README 标题和 README 概述里的 Step 1 / Step 2（A7），以及书里和课上引用的原词（accomplish、things、Chapter One、Italian、The Complete Book of Cheese、Chester 那个问题；A10）。（b）**产品、组织、课程和名字**：RAG、Self-RAG、Google、Google Cloud、Cloud Storage、Vertex AI、Vertex AI API、Gemini、Docker、Docker Hub、Docker Compose、Compose、Chroma、Chroma UI、SQLite、HNSW、Chrome、Git、Git Bash、WSL、Linux、Mac、Windows、Python、uv、pipenv、Project Gutenberg、JSON、AC215、MLOps Learning、Tolminc、Mara、Chester、student、app、root。（c）**中国 MLOps 工程师在实验课上本来就说英文的词，封闭清单**：第 1 讲的 venv、root、repo、clone、commit、pin；第 2–4 讲的 container、image、Dockerfile、base image、tag、pull、pipeline、prompt（只指 LLM 的 prompt）、API、ID、port、localhost；这一讲新增 chunk（A3）、embedding（A3）、collection（A3）、top K（A3）、system prompt 和 input prompt（A3）、LLM、CLI（CLI container、CLI 服务）、agent（A13）。一个词只有在实验课口语真的说英文、而中文生硬、有歧义或和别的术语撞车时才进（c）。绝不为了“味道”说英文：chunking、splitting、splitter、vector、vector database、record、metadata、index、dimension、batch、similarity、distance、score、rank、ranking、nearest neighbors、filter、keyword、context、retrieval、retriever、generation、response、knowledge base、hallucination、fine-tuning、weights、window、overlap、separator、threshold、percentile、query（A3）、heartbeat、network、mount、service、service account、key、role、build、script、folder、terminal、flag、function 都说中文。
- **[A2]** container 和 image（同第 2–4 讲）。字幕说 container 和 image，就像助教在实验课上说的：两个 container、CLI container、Chroma 的 container、构建 image、Chroma 的 image、image 名；量词“个”。标题、章节名、meta.yaml 和配套文档写“容器”“镜像”（A4）。字幕里绝不写“镜像”。base image 照说（its Python base included → 包括它的 Python base image）；tag 照说（the image tag called latest → image 的 tag 叫 latest；a team should pin a tag → 团队应该 pin 一个固定的 tag）；pull 照说（Compose pulls Chroma's image → Compose 先 pull Chroma 的 image；No pull, no build → 不 pull，也不构建；a git pull → git pull 一次）。build → 构建，rebuild an image → 重新构建（no rebuild → 不用重新构建），the build context → 构建上下文（绝不单写“上下文”，那是 RAG 的上下文，A7）。
- **[A3]** RAG 的词（这一讲新增）。**chunk**（名词，一段文本）照说：一个 chunk、24 个 chunk、chunk 文件、chunk 大小（chunk size）、chunk 数（chunk count）、chunk 边界（chunk boundaries），chunk 0 开头时写“第 0 个 chunk”（A5）；chunking（过程）→ 分块，chunker → 分块器，chunk（动词）→ 分块 / 切成 chunk；splitting → 切分，splitter → 切分器，character splitting → 按字符切分，recursive splitting → 递归切分，semantic chunking → 语义分块（semantic splitting → 语义切分）；chunk type 的值照画面写（char-split、recursive-split、semantic-split）。**embedding**（名词）照说：embedding 模型、embedding 调用、256 个 embedding 值、embedding 列；embeddings-*.jsonl 这些文件 → embeddings 文件；embed（动词）→ 向量化（each window is embedded → 每个窗口都要向量化；embedded, stored, and paid for → 向量化、存储，还要付钱）；vector → 向量，a list of numbers → 一串数字，query vector → 查询向量，dimension → 维度，a 256-number vector → 256 维的向量。**数据库**：vector database → 向量数据库，an ordinary database → 普通数据库，record → 记录，metadata → 元数据，collection 照说（Chroma 的词：一个 collection、两个 collection），index → 索引，build an index → 建索引，the index folders → 索引目录，insert → 插入，a full rebuild of a collection → 完全重建，rebuild the index → 重建索引。**查询**：query（名词和动词）→ 查询（a query returns K results → 一次查询返回 K 个结果；querying means → 查询就是），the question → 问题，top K 照说（K 是字母），nearest neighbors → 最近邻，score → 分数，sort → 排序，rank / ranking → 排名 / 排序，results → 结果，distance threshold → 距离阈值，similarity → 相似度，cosine similarity → 余弦相似度，cosine distance → 余弦距离，cosine（度量）→ 余弦，dot product → 点积，straight-line distance → 直线距离，angle → 夹角，length → 长度，direction → 方向，measure → 度量。**过滤**：filter → 过滤（名词要计数时说“过滤条件”：两个过滤条件），metadata filter → 元数据过滤，document filter → 文档过滤，the book filter → 按书过滤，keyword filter / keyword ranking → 关键词过滤 / 关键词排序。**生成**：RAG 和 Self-RAG 照写；retrieval augmented generation → 检索增强生成，retrieval / retrieve → 检索，retriever → 检索器，generation → 生成，augmentation → 增强，context → 上下文，knowledge base → 知识库，the full prompt → 完整的 prompt，the final prompt → 最终的 prompt，system prompt 照说，the input prompt（代码里的 INPUT_PROMPT）→ input prompt，the model's response → 模型的回答，language model → 语言模型，LLM 照说，the model → 模型，weights → 权重，retrain → 重新训练，fine-tune → 微调，hallucination → 幻觉，stale training data → 训练数据过时，no specialized knowledge → 缺少专业知识，no sources → 没有出处，grounded answers → 有依据的回答，naive retrieval / naive RAG → 朴素检索 / 朴素 RAG，advanced → 进阶，lever → 手段，pre-retrieval / post-retrieval stage → 检索前 / 检索后阶段，query rewriting → 查询改写，hybrid search → 混合检索，reciprocal rank fusion → 倒数排名融合，re-ranking → 重排序，candidates → 候选。**README 里用参数名指代的步骤保留参数这个词**：the load step → load 这一步，your embed step → 你的 embed 那一步，the chunk step → chunk 这一步，in chat → 到了 chat 这一步，both loads → 两次 load，both chat commands → 两条 chat 命令，every load → 每次 load；同样的动作作普通动词时说中文（chunk, embed and load again → 重新分块、向量化、加载；we built the index: chunk, embed, load → 我们建好了索引：分块、向量化、加载）。
- **[A4]** 书面和口语的对应。字幕说 repo / clone / commit / container / image / base image / tag / pull / port / prompt / system prompt / chunk / embedding / collection / agent；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 基础镜像 / 标签 / 拉取 / 端口 / 提示词 / 系统提示词 / 文本块 / 嵌入向量（嵌入模型）/ 集合（collection）/ 智能体（agent），核心概念在那里首次出现时加英文括注（旁白以外可以用括号）。repo 作主语时说“这个 repo”。命令不受影响（git clone、docker compose pull 照写）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符不变）；不翻译、不变形、不加引号，不放进《》或代码格式。需要时加一个中文中心词：docker-shell.sh 这个脚本、docker-compose.yml 这个文件 / 这个 compose 文件、docker ps 这条命令、llm-rag 目录、secrets 目录、outputs 目录、docker-volumes 目录、--rm 参数、char-split 这个 chunk type、KEYS 标签页、Storage Admin 这个角色、query 函数、generate text embeddings 这个函数。句子不以实物或小写的保留英文词开头：先放一个中文词（用 docker ps 这条命令……；这个 repo 在 /app……；第 0 个 chunk……；而 load 这一步……；所谓 embedding，就是……；那 semantic-split 行吗？），这样字幕也不会以小写词开头。产品名、大写缩写（RAG、LLM、CLI、HNSW、API）和 README 可以开头（RAG，也就是检索增强生成……；Compose 先 pull……；Chroma 先过滤……；CLI 按名字找到 Chroma……；README 把两条通道叫作 Step 1 和 Step 2……）。
- **[A6]** 带下划线的名字（同第 3、4 讲）。没有 say: 时，检查器把显示行当作朗读文本来查，不接受“字母_字母”（配音会读成“下划线”）；SAY 也从不带着下划线读这些名字。所以中文行按旁白的说法写这样的名字：下划线变成空格，小写同 SAY，总带一个中文中心词，或放在一个显然是名字的位置；英文只是指一下的地方，就按它的作用称呼。对照：GCP_PROJECT → GCP project 这个变量（set GCP project on line 7 → 把第 7 行的 GCP project 变量改成……）；--chunk_type 和它的值 → chunk type 用 char-split / 用 recursive-split 这个 chunk type（所以 python cli.py --chunk --chunk_type char-split 写成“第 2 步：python cli.py --chunk，chunk type 用 char-split。”）；chunk_overlap → chunk overlap 参数；generate_text_embeddings → generate text embeddings 这个函数；SERVICE_DISABLED → service disabled（报 service disabled）；PERMISSION_DENIED → permission denied（报 permission denied）；INPUT_PROMPT → input prompt；SYSTEM_INSTRUCTION → system prompt（SAY 的说法）；GOOGLE_APPLICATION_CREDENTIALS → 密钥的路径（SAY 说 the key's path）；n_results → 结果数。英文行用 en_display 给出字面形式（D4）。等工具链允许显示行保留下划线（I1），就把这些空格形式换回本表的字面形式。
- **[A7]** 要分清的词。第 k 步（README 进度条的一步：Step 3: sh docker-shell.sh → 第 3 步：sh docker-shell.sh）↔ Step 1 / Step 2（README 概述给两条通道起的名字，S02[3]，保留英文，免得像进度条的一步）↔ 阶段（课上的阶段：索引阶段、检索阶段、检索前阶段）。chunk（一块）↔ 分块（过程）↔ chunk 这一步（--chunk 那一步）↔ chunk type（参数的值，A6）。切分（splitting）↔ 分块（chunking）↔ 切 / 切开（一刀）↔ 切点（一刀落在哪儿）。索引（index；也有“建索引”，课上的 Indexing 阶段 → 索引阶段）↔ 目录（任何文件夹：索引目录 = the index folders）↔ 书的目录（一本书的 contents，S12[7]：绝不单写“目录”）。向量（vector）↔ embedding（作为概念的模型和它的输出）↔ 向量化（embed）。相似度（越高越好）↔ 距离（越小越近）↔ 分数（课上的 scores）。查询（query）↔ 问题（用户的 question）↔ 提问（ask）。prompt（LLM 的 prompt）↔ 提示符（shell 的 prompt：the container's prompt → container 的提示符）↔ 提示（hint）。上下文（RAG 的 context）↔ 构建上下文（Docker 的 build context，S04[8]）。窗口（尺子的窗口、句子窗口）↔ 终端（笔记本上的第二个终端）↔ 门（发布出去的 host port，第 4 讲）。过滤（filter）↔ 忽略（git ignores）↔ 去掉（strip）。关键词过滤 ↔ 关键词排序（S12[6]、S15[2]）。记录（collection 里的一条 record）↔ 行（chunk 文件的一行，row 0 → 第 0 行）↔ 录制（我们的录制）↔ 课程团队留下的（课程团队记录下来的向量和运行）。重新构建（image）↔ 重建（collection 或索引）↔ 重新训练（模型）↔ 微调（fine-tune）↔ 重新启动（restart 应用）。加载（load 进数据库）↔ pull（image）↔ 下载（下载 zip 包）↔ 读入（reads 11 files）。模型 ↔ embedding 模型 ↔ LLM ↔ 语言模型，跟着英文走。授课老师（the instructor）↔ 课程团队（the staff）↔ 课上（the lecture）↔ 课件（the lecture slides）。服务（Compose 的 service）↔ 服务账号（service account）。密钥（key 文件）↔ 关键词（keyword）。标签（画面上的标签：your turn 标签）↔ tag（image 的 tag latest）↔ 标签页（控制台的 KEYS tab）。结果（results）↔ 回答（response）↔ 输出（课程团队的 outputs）↔ outputs 目录。通道（lane）↔ 网络（Docker 网络）↔ pipeline（课上讲 pipeline 的那页课件）。方框（图上的 box）↔ container。锚点（课件里的 anchor）↔ 替身（stand-in 查询）。计费 / 付费（billing、paying）↔ 调用（一次 call：89 次调用）。
- **[A8]** 语体：助教带实验课。指令简短，用口语动词（装、跑、删、切、改、敲、贴、拼）；称观众为“你”（一对一跟练；绝不用“您”“大家”“同学们”）；“我们”指录制时的我们（我们录制时没有 Google 的密钥）。中文语序；句子内部可以自由重组。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不堆“一个……的”。不用网络流行语。口语的节奏按意思传达：Here's the question → 这个教程要问的问题是；Here's RAG in five boxes → 用五个方框讲清 RAG；That's RAG → 这就是 RAG；Two rules → 两条规则；Two traps, hit on purpose → 两个陷阱，我们故意踩一下；One last oddity → 最后一个怪现象；Then this, which looks like an error but isn't → 然后是这个：看起来像报错，其实不是；Back another day → 改天回来；Now a search → 现在来搜索；Now generation → 接下来是生成；So where's the system prompt? → 那 system prompt 在哪儿？；Remember the opening question? → 还记得开头那个问题吗？；Back to chunking → 回到分块；No. → 不行。（S14）/ 不会：（S08）；The lecture goes further → 课上走得更远；Time to tear down → 该拆掉了；One last lesson → 最后一个教训；And the four questions? → 那四个问题呢？；a paid call → 一次要付费的调用。
- **[A9]** 精确。限定词照译：only 只，every 每个，all 全部，about 大约，up to 最多，at most 最多，by our estimate 按我们的估算，may / can 可能，never 从不 / 一直没，whenever 只要，however far 不管多远，relevant or not 不管相关不相关，very uneven 很不均匀。at the time of recording 一律译“录制时”，绝不省略（Python 3.12.15、uv 0.13.1）。数量、大小、距离、分数、行号、步骤号和行数和画面完全一致（C1）。勘误语气温和，后面一定紧跟改法，全部用同一个说法：a small slip → 一个小疏漏（A small slip first: → 先说一个小疏漏：；a harmless slip → 一个无害的小疏漏；Two small slips. → 两个小疏漏。；a small slip, with a one-line fix → 一个小疏漏，改一行就能修好）。**思考题**（S06[3]、S07[3]、S08[12]、S12[1]、S14[4]）只问不答，措辞不能泄露答案：S06[3] 不能说 24；S07[3] 不能提重叠或库的默认值；S08[12] 不能说“不会”，也不能说余弦不管长度；S12[1] 不能点出书名，也不能说过滤赢了；S14[4] 不能说 semantic-split 需要 API 或密钥。**钱**：you pay for the text you send → 按你发送的文本付费；that key spends your project's money → 这个密钥花的是你项目的钱；a few cents by our estimate → 按我们的估算只要几美分；Check the current price list → 以现行的价目表为准；you paid only for what you sent → 你只为发送过的内容付了费。Vertex AI 按发送和返回的文本计费：绝不说按次计费（89 次调用数的是调用次数，不是钱）。
- **[A10]** 名字。产品、公司和课程名保留拉丁字母（A1 b）；“哈佛”只出现在标题和简介里。课程：AC215；lecture n → 第 n 讲（that's lecture 8 → 那是第 8 讲的内容；the three gates from lecture 4 → 第 4 讲的三道关卡）；next lecture → 下节课；the lecture → 课上（the lecture lists → 课上列出了；from lecture → 课上的）；the lecture slides → 课件；a slide → 那一页课件（the pipeline slide from lecture → 课上那页讲 pipeline 的课件；in these slides' sense → 就是这几页课件说的那种索引）；part 1 / part 2 → 第一部分 / 第二部分；this video → 这期视频。the instructor → 授课老师（绝不提名字）；the instructor's short story → 授课老师写的短篇故事；the staff → 课程团队（第 3 讲）；the staff's recorded vectors → 课程团队留下的向量；the course's project → 课程的项目；the course's web tools → 课程的网页工具；the course folder → 课程目录（~/AC215）。书只用书名，绝不提作者（The Complete Book of Cheese 照写：它是画面上的过滤值）；Tolminc、Mara 和 Chester 照写；Project Gutenberg 照写，单说 Gutenberg 也照写。书里和课上引用的原文照画面写：切开的单词 accomplish 和 things、Chapter One、过滤字符串 Italian（包含 Italian 的 chunk；the word Italian → Italian 这个词）、RRF 的例句 Chester went to the bank of the river in the morning（要点在 bank 这个词，所以不译）。教程问的问题和查询改写的例句是旁白自己的问题，要翻译（how is Tolminc cheese made? → Tolminc 奶酪是怎么做的？；where do dolphins live → “海豚住在哪里”）。用户名 student、app、root 和占位符 your-project-id 照写；container ID 从不读出来。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（含注释）、README 卡片和小标签、进度条（README › Run Container, step k of N）、课件标签（Lecture 5 · slides A16–A19）、示意控制台、课程网页工具的浏览器框、图里的标注、标签（your turn、extra、illustration、our illustration、recorded · the staff's vectors、real run · no key、lecture example、erratum、at the time of recording、your numbers will differ、concept · not in the tutorial's code、preview · L06、your project pays）和思考题卡片都是英文，场景不用为语言做任何改动。所以旁白提到画面标签时，字幕照画面写：黄色的 your turn 标签（第 2–4 讲）；the gray lecture tag → 灰色标签；extra commands → 额外的命令。旁白用自己的话说的一律翻译：an extra check → 额外检查，the tracker → 进度条，code panels → 代码面板。旁白转述 README 时说“README 里说……”；旁白提到的 README 标题照写英文（Prerequisites 一节）；the next section → 下一节。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、目录、数据库、服务器、网络、内存、磁盘、脚本、视频、用户名、信息、账号、地址、索引、向量、元数据、默认值、幻觉、微调；绝不用 預設、程式、程式碼、檔案、資料夾、資料庫、伺服器、網路、記憶體、磁碟、腳本、影片、使用者、帳號、索引值、矢量（指 vector）。
- **[A13]** 系列清单（ac215-video skill 的清单）在这一讲。embedding 和 prompt 在这一讲进入口语清单（A3）；agent 说了两次（S16[5] next lecture runs this command with an agent → 下节课会用一个 agent 来跑这条命令；S16[9] Next time: agents. → 下节课：agent。；书面写“智能体（agent）”）；pipeline 一次（课上讲 pipeline 的那页课件，S02[2]）；port 只以 port 8000 出现（第 4 讲：port 8000、发布；书面写“端口”）；container、image、Dockerfile、commit、pull 和 repo 同第 1–4 讲。这份稿子里没说到的：volume（只出现在目录名 docker-volumes 里，是实物：docker-volumes 目录，绝不写“卷”或 volume）、PATH、endpoint（心跳就是“心跳”，不是 endpoint）、LoRA（微调是“微调”，第 8 讲）、CI、push。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（输入 exit、Python 3.12.15、第 7 行、port 8000、24 个 chunk、0.8 以上、112 MB、secrets 目录、container 里、top K 的、5% 的）。检查器会在每个显示的句子上报告缺少的空格。实物内部的空格保持原样（docker compose down）；绝不在实物里加空格。紧挨全角标点不加空格（……cd 进 llm-rag。、用户 app，）。绝不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，紧挨实物也一样（输入 exit。）。列举用“、”（--chunk、--embed 和 --load）。不用任何括号：（）、()、《》、【】、[]、<> 都不用——没有 say: 时检查器不接受，双语字幕带也不需要括注。“”只用于中文里引用的想法、词或翻译过来的问题（“海豚住在哪里”）；实物、标签名、书名、书里的原词和终端原文从不加引号。一个中文句子（对应一个英文句子）里不出现 。？！：改用 ，；：（S01[0]：这个教程要问语言模型一个问题：Tolminc 奶酪是怎么做的？是一个句子）。“第 N 步”后面跟说明时用全角冒号，“陷阱一 / 陷阱二”“第一题……第五题”后面也一样。问句保留 ？。
- **[B3]** 检查器不收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后面跟 !、括号、字母_字母）：绝不抄进中文行，用文字说或换一种写法。documents[0] → documents 的第 0 项；load() → load 这个词（it prints the word load → 它打印的是 load 这个词）；one minus the similarity → 1 减去相似度；one half divided by its rank → 二分之一除以它的排名；从来不需要写 8000:8000（说 port 8000）；3,072 → 3072（C1）。允许并照画面保留的：路径里的 /（/app、/secrets、/data、/.venv、~/AC215），文件名和版本号里的 .，localhost:8000 里的 :，参数和名字里的 -（--rm、--chunk、docker ps -a、char-split），@（@ 符号后面），$contains 里的 $，5% 里的 %。

### C. 数字、版本号与单位

- **[C1]** 显示文字里的数字。凡是和画面、终端、代码或课上的数字呼应的，一律用阿拉伯数字，不加千位分隔符，和终端打印的一样（8248、14228、1355、7808、3072；算出来的 7458 也一样）：步骤号（第 1 步、第 3 步）、行号（第 7 行、第 8 行、第 185 和 186 行、第 40 行、第 372 行）、行数和 chunk 编号（第 0 行、第 0 个 chunk、第 1 个 chunk）、变体（第 4 种、第 1 到 3 种）、数量（11 本书、11 个文件、24 个 chunk、35 个、64 个、10 个结果、10 条记录、25 个候选、256 个数、每批 100 个、每批 500 条、重试 5 次、89 次和 148 次调用、528 次、22 个文件）、分数和距离（0.57、0.77、0.43、0.93；0.8；0.369 到 0.402；0 到 0.16；0.28 到 0.31；0.75、0.67、0.42）、维度 256、port 8000、版本号、大小、时间、日期。S01 的故事情节也按这条（11 本书、10 本来自 Project Gutenberg 的老书、最相关的 10 页）。画面上没有的、小的叙述性数量和序数用汉字：两条通道、五个方框、四个弱点、四个问题、三个阶段、两条规则、两个陷阱、两个角色、三个值、两个挂载、三个版本号、两个 collection、两条警告、三个段落、三个手段、两个问号、第一个窗口、第一本书、第二个候选人、第一部分 / 第二部分、第一题……第五题、陷阱一 / 陷阱二。英文用词说一个画面上显示为数字的数时，跟着画面；画面上没有时，跟着英文（both → 两条都 / 两个都；all four → 四个都；all three steps → 三步一起）。
- **[C2]** 单位、版本号、百分比和日期。大小照画面写，加半角空格：112 MB、60 MB、826 MB、2.11 GB、82 MB。时间：81 秒、5 秒、10 到 20 分钟、大约 2.5 分钟。版本号带名字：Python 3.12.15、uv 0.13.1、Docker 29.8.2、Compose 5.6.0；模型 ID 照代码写（gemini-embedding-001、gemini-3.1-flash-lite）。the 95th percentile → 第 95 百分位；the biggest 5 percent → 最大的 5%；one half → 二分之一；1（向量的长度）→ 1。日期：2026 年 10 月 16 日（October 16, 2026）。钱：cents → 几美分，绝不写成多少元或多少美元。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 里，script.md 的每个 SAY 行对应一个条目（140 段）；`en` 和 SAY 行逐字节相同；`zh` 的条目数和 explainer.voice.split_sentences 切出的英文句子数完全相同（这份稿子一共 358 句）。只在一个句子内部重组；绝不合并或拆分句子。短句也单独成一项：Two rules. → 两条规则。；Two small slips. → 两个小疏漏。；Pause and edit. → 暂停一下，改好它。；It's never sent. → 它从来没被发出去。；No weights moved. → 权重一个都没动。；None. → 一个都没有。；No. → 不行。；Can semantic split? → 那 semantic-split 行吗？；How many mention Tolminc? → 有多少提到 Tolminc？；That's RAG. → 这就是 RAG。；Next time: agents. → 下节课：agent。。运行 `python -m explainer.i18n check videos/ac215-l05-rag --lang zh`，直到它打印 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（锚点只用来给中文配音的渲染安排动画节拍）。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示的句子都要通过 explainer.i18n.spoken_problems：不用括号（B2）、不用数学符号（B3）、没有“字母_字母”的名字（A6）、数字后面不跟 !、没有以“种”结尾再跟 ，。！？ 的分句（改写：“每种 chunk type 一个。”可以，“有多少种。”不行：一共几种？ → 一共有几个？）、汉字和拉丁字母或数字之间有半角空格（B1）、每个句子以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），并且每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用正则 `[A-Za-z][A-Za-z'.-]*` 切词：gemini-embedding-001 切成 gemini-embedding-，gemini-3.1-flash-lite 切成 gemini- 和 flash-lite，/.venv 切成 venv，.gitignore 切成 gitignore，$contains 切成 contains，AC215 切成 AC，localhost:8000 切成 localhost，docker ps -a 切成 docker 和 ps。它报出来的拉丁词，要么是该翻译的英文词（通常如此），要么是漏掉的实物：把实物按同样的切法加进 allowed_spoken_latin，并加进对应的术语。故意不列复数（chunks、IDs、collections；embeddings 只作为文件名前缀）：报出来的复数是要去掉的英文词形变化（第 1 讲 A7：10 条记录的 ID、两个 collection）。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都要有一个 en_display 项，写出画面上的字面形式，其余和 SAY 句子逐词相同；同一段里的其他句子写 null。这份稿子的念法 → 字面形式（review_spoken 第 16 条）：L-L-M rag → llm-rag；L-L-M rag CLI → llm-rag-cli；L-L-M service account → llm-service-account；L-L-M service account dot JSON → llm-service-account.json；the git ignore file → the .gitignore file；docker ignore file → .dockerignore file；GCP project → GCP_PROJECT；service disabled / Service disabled → SERVICE_DISABLED；Permission denied → PERMISSION_DENIED；dash dash r m → --rm；slash app / slash secrets / slash data / slash dot venv → /app / /secrets / /data / /.venv；the docker volumes folder → the docker-volumes/ folder；outputs (the folder) → outputs/；localhost port 8000 → localhost:8000；docker ps dash a → docker ps -a；chunk, embed and load … query and chat (S02[3]) → --chunk, --embed and --load … --query and --chat；python cli.py, dash dash chunk / embed / load / query / chat → python cli.py --chunk / --embed / --load / --query / --chat；chunk type char split / recursive split / semantic split → --chunk_type char-split / recursive-split / semantic-split (a bare char split / recursive split / semantic split naming the value → char-split / recursive-split / semantic-split)；chunk overlap → chunk_overlap；Gemini embedding 001 → gemini-embedding-001；Gemini 3.1 Flash Lite → gemini-3.1-flash-lite；H-N-S-W → HNSW；an extra command called get / The get command → an extra command called --get / The --get command；the word load → load()；documents, item zero → documents[0]；contains (S12[6]) → $contains；generate text embeddings → generate_text_embeddings；the semantic split collection → the semantic-split-collection。段落（v2 稿子的扫描结果；block[sentences]，从 0 数；稿子改了要重新扫描）：S02[3:0] S03[1:1, 2:1-2, 3:0, 4:2, 5:0, 6:0] S04[1:1, 3:0, 4:1, 5:0, 7:1, 8:2] S05[0:0,2, 1:1, 3:1, 6:1, 7:1] S06[5:0, 8:0] S07[2:0, 5:2] S08[3:0, 6:0, 8:2-3, 9:0] S09[3:1, 4:0, 6:0, 8:1, 9:0] S10[1:1, 3:1, 5:0] S11[5:0-1, 7:0, 8:0] S12[6:2, 7:0] S13[2:1, 6:0] S14[4:1, 5:2, 6:0, 7:2] S16[2:1]。带下划线的名字（A6）只在 en_display 里还原成字面形式；中文行保留空格形式。英文版自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只翻译它的英文句子：不加命令、参数、括注、中文控制台名或解释；只有英文标明 extra 的地方才说“额外”；保留英文的词不加中文解释（英文行就在正下方）；思考题不加答案（A9）。
- **[D6]** 固定句式。Pause and run it. → 暂停一下，自己跑一遍。 Pause and do both, in your course folder. → 暂停一下，在你的课程目录里把两件事都做了。 Pause and do it all now: account, roles, key, and API. → 现在就暂停，全部弄好：账号、角色、密钥和 API。 Pause and edit. → 暂停一下，改好它。 Pause, and get to this prompt. → 暂停一下，走到这个提示符。 Pause and try these checks; … → 暂停一下，试试这些检查；…… Pause and run both, with your key: … → 暂停一下，用你的密钥两条都跑一遍：…… Pause and run both loads. → 暂停一下，两次 load 都跑一遍。 Pause and restart. → 暂停一下，重新启动。 pause and run both → 暂停一下，两条都跑一遍。 Pause: run both chat commands with your key, then try the tool. → 暂停一下：用你的密钥把两条 chat 命令都跑一遍，再试试这个工具。 Pause and try it, with your key. → 暂停一下，用你的密钥试试。 Pause and tear down now, so … → 现在就暂停，把它拆掉，这样…… When the yellow your-turn tag appears, pause and run the command → 看到黄色的 your turn 标签，就暂停，自己跑一遍命令；extra commands aren't in the README → 额外的命令 README 里没有。An extra check: / Two extra checks: / An extra look / An extra line count / an extra command called --get / Afterwards, an extra: / extras → 额外检查一下：/ 两个额外检查：/ 额外看一眼 / 额外数一下行数 / 一条叫 --get 的额外命令 / 之后再加一个额外步骤：/ 额外检查。This one isn't in the README / Leaving isn't in the README. → README 里没有这一步 / 怎么离开，README 里没写。Step N: / Step N is a link … → 第 N 步：/ 第 N 步是一个链接……；Steps 1 and 2: → 第 1 步和第 2 步：；Step 1 of the next section: → 下一节的第 1 步：。With your key, look for … → 有密钥的话，要找的是……；If yours fails, or keeps retrying, read the error. → 如果你那边失败了，或者一直在重试，就去读报错。at the time of recording → 录制时。A small slip … → 一个小疏漏……（A9）。Five questions to test yourself. → 五道题，自测一下。One: … Five: → 第一题：……第五题：。The answers are in the exercises → 答案在练习里，every command is in the study guide, in the MLOps Learning repo → 每条命令都在学习指南里，就在 MLOps Learning 这个 repo 里。Next time: agents. → 下节课：agent。In part 2, … / Part 2 puts it to work. → 第二部分，……/ 第二部分让它派上用场。
- **[D7]** 文件。narration/g1.yaml = S01–S09（第一部分，建索引），narration/g2.yaml = S10–S16（第二部分，查询索引），即 video.yaml 的两个 part；每个文件以注释开头（覆盖范围、应用的规则：A6 空格形式的名字、B3 用文字写的符号、C1 不加千位分隔符的数字、D4 en_display、没有 say: / anchors:），并保持稿子的顺序。字符串用双引号；字面的双引号或反斜杠要做 YAML 转义。
- **[D8]** 按英文时间轴的长度。中文是边听英文边读的，字幕带在英文分段切换的地方切换（一段中文如果读起来快于每秒 9 个单位，最多多给 1 秒）。每个中文句子读起来的时间要和英文听起来差不多：经验法则是每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也占长度（llm-service-account.json 13.2 个单位，Gemini Enterprise Agent Platform User 20.4，semantic-split-collection 14.3，The Complete Book of Cheese 14.9）：英文没重复的地方不要重复它们；同一段里第一次提到之后，用简短的指代（这个角色、这本书、这个 collection）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文行最多 30 个单位，英文行 96 个字符；纯中文字幕（.zh.srt）每行 22 个单位，每条 2 行。分句写到最多大约 24 个单位，用 ，；： 隔开，让切分器有干净的切点；避免超过 30 个单位却没有标点的分句（单是角色名 Gemini Enterprise Agent Platform User 就有 20 个单位：让它单独占一个分句）。
- **[G2]** 字幕条结尾：工具链去掉条末的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。能用中文词收尾时，就不要以“实物 + 句号”结尾（“……放进 secrets 目录。”比“……放进 secrets。”读起来好，但两者都有效）。
- **[G3]** 命令绝不拆开。切分器把中文行里两个拉丁词之间的空格当作好的切点，所以 python cli.py --chunk 可能落在两行上，观众就没法照抄。把整条命令放在分句末尾、全角冒号之后（第 3 步：sh docker-shell.sh。；第 2 步：python cli.py --chunk，chunk type 用 char-split。），每条字幕最多一条命令，周围的中文要少。一行放不下的命令，或含有带下划线名字的命令，不完整写出：按 SAY 的说法称呼它（the clone command → clone 命令；python cli.py --chunk --embed --load --chunk_type semantic-split → README 里的命令，用 semantic-split 把三步一起跑），让终端和英文行去显示它。在渲染出的 .zh.srt 里检查每一条含命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、部分和章节标题用书面语体（A4：容器、镜像、仓库、端口、提示词、文本块、嵌入向量）；问句保留问号；保留英文的冒号结构（切书：一把尺子；加载：……；对话：……；语义分块：……）；命令、参数、chunk type、目录名和文件名照写（meta.yaml 不受检查；那里可以用括号和下划线）。核心概念的章节带上英文短名，方便搜索，同第 1、3 讲（嵌入向量（embedding）、提示词（prompt））。Introduction to RAG → RAG 入门；第一部分 build the index → 建索引，第二部分 ask the index → 查询索引；chunk, embed, load → 分块、向量化、加载；naive → 朴素。
- **[H2]** 简介（Bilibili / YouTube）：两三句，书面语体，用本词表的术语：这是 AC215 第 5 讲 dlops-io/llm-rag 的跟练视频；观众做了什么、学到什么（一个脚本启动两个容器：命令行容器和 ChromaDB；char-split 和 recursive-split 两种分块，以及默认藏着的重叠；把嵌入向量看作方向，余弦相似度和 Chroma 的余弦距离，两条通道共用一个模型；集合、记录和笔记本磁盘上的 HNSW 索引；过滤先于排序；从没发出去的系统提示词；语义分块，以及课上讲的查询改写、混合检索与重排序）；英文旁白，配中文和中英双语字幕；终端输出录于 2026-10-16，录制时没有 Google 密钥，所以向量是课程团队提交过的，调用 Google 的步骤展示命令、真实的报错和该看什么。
- **[H3]** 配套材料：i18n/zh/README.md（以及 exercises.md / digest.md，如果要做的话）用这份词表、书面语体翻译（仓库、克隆、提交、容器、镜像、基础镜像、端口、提示词、系统提示词、文本块（chunk）、嵌入向量（embedding）、嵌入模型、集合（collection）、向量数据库、元数据、索引、余弦相似度、余弦距离、最近邻、检索增强生成（RAG）、语义分块、重叠（overlap）、服务账号、智能体（agent））；那里可以用括号和下划线（不受检查）。标题和 `<summary>答案</summary>` 要翻译。最后附一张术语表：English | 这里用的词 | 常见的其他说法（嵌入 / 向量化 / 嵌入向量，文本块 / 切块 / 分片，集合，向量库，业界口语里 retrieval 也说“召回”，re-ranking 也说“重排 / 精排”，提示词 / 提示，token 说“词元”）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]** （请求，第 3 讲起一直开着）`explainer.i18n check` 在句子没有 say: 时，把它的朗读检查（_SPOKEN_BAD：括号、数学符号、“字母_字母”的名字）用在显示行上。对只有字幕的视频（这个系列；video.yaml 里没有 languages.zh.voice，词表写的是 voice: none），这些检查保护不了什么，反而逼出了 A6 和 B3（这里：GCP_PROJECT 写成 GCP project 变量，--chunk_type char-split 写成 chunk type 用 char-split，documents[0] 写成 documents 的第 0 项，load() 写成 load 这个词）。建议：词表的 voice 是 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。那时 A6 和 B3 就变成：字面形式照抄。
- **[I2]** （待办，来自第 1 讲 I3）`explainer/subtitles.py` 的 `_cuts` 把中文行里拉丁词之间的空格当作好的切点，所以命令可能被拆开（G3）。建议：在中文行里，把只由空格隔开的一串拉丁词当作不可拆分的整体，除非它单独就超过一行。
