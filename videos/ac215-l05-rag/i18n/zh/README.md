# 中文字幕说明

视频 *AC215 · Lecture 5 — Introduction to RAG (follow-along: llm-rag)*
（**AC215 · 第 5 讲：RAG 入门（跟练：llm-rag）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 5 讲的跟练视频：照着教程仓库
[dlops-io/llm-rag](https://github.com/dlops-io/llm-rag)（`main` 分支，提交 `e17a39f`）的整份 README，
在 11 本讲奶酪的书（10 本 Project Gutenberg 上的老书，加上授课老师写的一个短篇故事）上搭一个检索增强生成（RAG）
系统。视频分两部分：

- **第一部分：建索引**（S01–S09）。先看清 RAG 的两条通道：上面一条只跑一次，把书切成文本块（chunk）、向量化、
  加载进向量数据库；下面一条每个问题都跑，查询、再交给模型回答；两条通道必须共用同一个嵌入模型。然后准备好
  `secrets` 目录、服务账号、密钥、Vertex AI API 和 `GCP_PROJECT`，用 `sh docker-shell.sh` 启动两个容器
  （命令行容器和 Chroma），把 `docker-compose.yml` 读成一张图（按名字指定的网络、发布出去的端口 8000、绑定挂载），
  再故意踩两个陷阱。接着用 `char-split`（350 个字符、重叠 20，一共 8248 个文本块）和 `recursive-split`
  （14228 个：它所在的库默认最多重叠 200 个字符，README 没提）分块；把嵌入向量（embedding）看成表示意思的方向，
  分清余弦相似度和点积，`gemini-embedding-001` 只取前 256 个数；最后把两个集合（collection）加载进 Chroma：
  一条记录里有什么，为什么每次 load 都是完全重建，HNSW 索引是做什么的，数据库文件为什么在你磁盘上的
  `docker-volumes/` 里。
- **第二部分：查询索引**（S10–S16）。退出、`docker compose down` 之后索引还在；查询就是找最近邻、保留前 K 个
  （top K，这份代码取 10），Chroma 报的余弦距离和课上的相似度方向相反，代码里也没有距离阈值；README 那条查询的
  两个过滤条件先于排序起作用，所以 10 个结果讲的都是别的奶酪；对话这一步拼出的提示词（prompt），以及定义了却
  从没发出去的系统提示词（改一行就能修好）；语义分块（`semantic-split`）为什么在 `--chunk` 这一步就要调用 API；
  课上讲的查询改写、混合检索（倒数排名融合）和重排序（只讲思路）；最后是清理、过期的索引和回顾。

画面上的终端输出、代码面板、README 引文、标签（`your turn`、`extra`……）、进度条、示意控制台和课程网页工具的
浏览器画面都是英文原样，方便你对照着敲；只有旁白译成了中文。录制时没有 Google 密钥：Docker、分块和数据库都是
真实运行的，加载的向量是课程团队提交过的（`68e0bde`）；凡是调用 Google 的步骤，画面展示命令、缺少密钥时的
真实报错，以及有密钥时该看什么。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿都在 Git 里。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l05-rag.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l05-rag.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l05-rag_part1.*`、`_part2.*` | 第一部分（S01–S09，建索引）和第二部分（S10–S16，查询索引），各有自己的视频、字幕和章节文件 |
| `output/ac215-l05-rag.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l05-rag.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l05-rag.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文（字幕用；g1 = 第一部分 S01–S09，g2 = 第二部分 S10–S16；共 140 段旁白、358 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（L-L-M rag、dash dash chunk、chunk type char split、slash app、documents, item zero），英文行换回屏幕上的写法（`llm-rag`、`--chunk`、`--chunk_type char-split`、`/app`、`documents[0]`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L05-rag.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L05-rag.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l05-rag --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l05-rag --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l05-rag --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或地点放在句末，中文就不把“如果……”“当……时”
“在……之后”提到句首，否则相邻两条双语字幕的中英文会互相错开。

## 译文风格

按中国 MLOps 助教带实验课的说法，和第 1–4 讲一致：

- **一字不改**：你要输入、要在屏幕上对照的东西（命令、参数、`chunk_type` 的值、文件名和目录名、路径、image /
  collection / 模型的名字、环境变量、控制台标签和角色名、报错原文、README 章节标题和 README 概述里的 Step 1 /
  Step 2、书里和课上引用的原词，比如 accomplish、Chapter One、Italian、The Complete Book of Cheese 和 Chester
  那个例句）。字幕检查器不收的几种写法例外：带下划线的名字按旁白的念法写成空格，再加一个中文中心词
  （GCP project 这个变量、chunk type 用 char-split、chunk overlap 参数、generate text embeddings 这个函数、
  service disabled），检查器不收的符号用文字说（documents 的第 0 项、load 这个词、1 减去相似度、二分之一除以
  它的排名）；英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，第 1–4 讲的 venv、repo、clone、commit、pin、container、image、
  Dockerfile、base image、tag、pull、pipeline、prompt（只指 LLM 的 prompt）、API、ID、port、localhost，这一讲新增
  chunk（名词）、embedding（名词）、collection、top K、system prompt 和 input prompt、LLM、CLI、agent。
- **其余用中文标准术语**：检索增强生成、检索、生成、分块、切分、向量、向量化（动词 embed）、向量数据库、记录、
  元数据、索引、维度、余弦相似度、余弦距离、点积、直线距离、最近邻、查询（名词动词都是）、过滤、上下文、幻觉、
  微调、查询改写、混合检索、倒数排名融合、重排序、服务账号、密钥、角色、挂载、构建。shell 的 prompt 是“提示符”，
  Docker 的 build context 是“构建上下文”，和 RAG 的“上下文”分开。
- **比喻按意思译，一个比喻一个词**：方框、通道、图书管理员和开卷考试、尺子（char-split）、剪刀
  （recursive-split）、地震仪（semantic-split）、接缝、保险、替身、锚点、空位，沿用第 4 讲的三道关卡、电话簿和
  发布出去的门。
- **精确**：录制时会变的版本号一律带“录制时”；教程里的勘误统一说“一个小疏漏”，后面紧跟改法；钱只说按发送的文本
  付费、按我们的估算只要几美分，绝不说按次计费；思考题只问不答。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、克隆、提交、端口、提示词、系统提示词、文本块、
  嵌入向量、嵌入模型、集合、智能体。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| retrieval augmented generation (RAG) | 检索增强生成（RAG） | 检索增强生成 |
| chunk | chunk（字幕）；文本块（书面） | 切块、分片、文本片段 |
| chunking / splitting | 分块 / 切分 | 切块、文本分割 |
| embedding | embedding（字幕）；嵌入向量（书面） | 嵌入、向量表示 |
| embed（动词） | 向量化 | 嵌入、编码 |
| embedding model | embedding 模型（字幕）；嵌入模型（书面） | 向量模型 |
| vector database | 向量数据库 | 向量库 |
| collection | collection（字幕）；集合（书面） | 集合 |
| top K | top K（字幕）；前 K 个（书面） | 前 K 个 |
| retrieval | 检索 | 召回（业界口语） |
| re-ranking | 重排序 | 重排、精排 |
| prompt / system prompt | prompt / system prompt（字幕）；提示词 / 系统提示词（书面） | 提示、系统指令 |
| overlap | 重叠 | 重叠窗口 |
| reciprocal rank fusion | 倒数排名融合 | RRF、倒数秩融合 |
| query rewriting | 查询改写 | 查询重写 |
| agent | agent（字幕）；智能体（书面） | 代理 |
| token | 这一讲的旁白里没有出现 | 词元 |
