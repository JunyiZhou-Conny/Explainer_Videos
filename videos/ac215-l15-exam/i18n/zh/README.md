# 中文字幕说明

视频 *AC215 · Lecture 15 — ML Workflows with Vertex AI (exam edition)*
（**AC215 · 第 15 讲：Vertex AI 上的机器学习工作流（考前版）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 15 讲的考前版，写给 Quiz 4 前一天的你：不跟着 README 逐条敲命令，也没有录制任何
终端输出，而是把小测考的几个机制各画成一张动画图，再用
[dlops-io/ml-workflow](https://github.com/dlops-io/ml-workflow)（`main` 分支，提交 `3730009`）、
[dlops-io/model-deployment](https://github.com/dlops-io/model-deployment)（`main` 分支，提交 `cf0b7c7`）和
[dlops-io/ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws)（`main` 分支，提交 `f165c6e`）里的代码作为依据。
开头是凌晨的三个定时任务：准备数据、训练、部署各占一个钟点，几个月都没出事；直到有一晚准备数据花了 75 分钟，每个任务的
退出码都是 0，endpoint 却在提供一个只用一半数据训练出来的模型。贯穿全片的问法是：**题目说这个，就想那个**。全片只有一部分
（S01–S08）：

- **S01：凌晨两点的竞态**。时钟对数据一无所知；要说的不是“2 点训练”，而是“准备数据完成之后再训练”，这正是 pipeline 的用处。
- **S02：pipeline 是一张图**。工作流管理知道哪一步需要哪一步，记录它的结构是有向无环图（DAG）：任务（task）是节点，数据
  依赖是边。用 kfp 描述图，由 Vertex AI Pipelines 运行（控制台现在叫 Agent Platform），不用自己管 Kubernetes。玩具
  pipeline 的三个 `@dsl.component`（`square`、`add`、`square_root`）和一个 `@dsl.pipeline`：pipeline 函数只跑一次，每次
  调用组件只是放下一个节点（`square` 调用两次，第二个叫 `square-2`）；编译成 YAML，由 SDK 提交成 pipeline 任务，到了
  Google 的机器上才有数字。
- **S03：task.output，造出边的那根连线**。`.output` 是占位符，代表上游 task 成功之后才存在的值；接上它就同时传了数据、
  建了依赖，编译出来的 YAML 里写成 `dependentTasks` 和每个输入的生产者 task。多个输出时用 `.outputs["name"]` 点名。
  写死或猜出来的路径没有边，可能读到上周的过期文件；`.after()` 只管顺序、不传数据。第一题。
- **S04：最大安全重叠**。两个 `square` 之间没有路径，所以并行；`add` 是汇合点，要等齐所有输入。一个预处理、两个训练、
  一个比较：多加一条边答案不变、跑得更久，少一条边就是竞态；一次运行的时长等于它的最长路径。第二题。
- **S05：强制顺序，靠边，不靠时钟**。同一个时钟上的四条泳道：cron 错开时间、后台的 `&`、事件触发加“从实验追踪工具里取最好的
  模型”、pipeline 的边；掷骰子决定预处理多久，只有边那条泳道每次都对。cheese app 的 pipeline 用 `.after()` 把四步串起来，
  YAML 里写成 `dependentTasks`。第三题，然后是只负责启动的步骤：边等的是 task，不是它启动的任务，所以训练步骤要
  `sync=True`。
- **S06：模型注册表、端点、部署与预测**。课件的五步：拿到保存的模型、更新服务签名（解码 JPEG、转成浮点数、缩放到
  224×224）、上传到存储桶、注册（一张目录卡片，不运行、不花钱、还不能调用）、部署到端点（`cheese-app-endpoint`，存在就复用，
  不存在就新建；部署之后一台机器开始计费）。预测时请求把 base64 编码的图片放在 `bytes_inputs` 键下；清理时先取消部署，再删除
  端点，注册表里的卡片和存储桶里的文件都还在。Cloud Run 的经验法则一句带过。
- **S07：cheese app 的 pipeline，以及 AWS 上的同一个 DAG**。数据采集 → 数据处理 → 模型训练 → 模型部署：两个容器组件
  （image 来自 Docker Hub，课件上是 Artifact Registry）和两个 Python 组件。步骤之间不互相调用，经由存储桶里的 `raw.zip`、
  `clean.zip` 和 `model/` 目录按名字交接，所以边用的是 `.after()`。AWS 上的 SageMaker Pipelines 是同一个思路：训练步骤的
  输入引用处理步骤的属性，这个引用就是边，步骤列表的顺序不影响图。
- **S08：小测要记住的七条规则**，以及课上的那条链：DSL 写的配方、YAML、SDK、Kubeflow 引擎、Vertex AI Pipelines。

画面上的代码面板、README 引文、YAML、示意图上的 task 名和标签、选择题卡片、黄色结论卡、课件标签（`Lecture 15 · slides …`）
和七条规则都是英文原样，方便你和小测的选项对照；只有旁白译成了中文。三道选择题是小测风格的新题，不是练习题原文；思考题在
题目出现时只问不答，答案在下一段旁白里，连同每个错误选项错在哪。片中没有运行任何命令，项目 ID、存储桶名、endpoint ID 和
密钥也从不出现。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l15-exam.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l15-exam.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l15-exam.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l15-exam.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l15-exam.srt` | 英文字幕 |
| `output/chapters.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml` | 逐句对齐英文的中文译文（字幕用；S01–S08，76 段旁白、186 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（K F P、d s l dot component、d s l dot pipeline、square 2、dot output、dot outputs、dot after、dependent tasks、sync set to true、bytes inputs、base 64、cheese app endpoint、raw zip、clean zip、the model folder、the Keras export archive、the D S L、background ampersands），英文行换回屏幕上的写法（`kfp`、`@dsl.component`、`@dsl.pipeline`、`square-2`、`.output`、`.outputs["name"]`、`.after()`、`dependentTasks`、`sync=True`、`bytes_inputs`、`base64`、`cheese-app-endpoint`、`raw.zip`、`clean.zip`、`model/`、`ExportArchive`、`DSL`、`background & jobs`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、章节名和简介 |

每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L15-vertex-ml-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L15-vertex-ml-workflows.md)；
跟着 README 逐条操作的版本是同一讲的跟练视频。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l15-exam --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l15-exam --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l15-exam --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或期限放在后面，中文就不把“如果……”“直到……之前”提到
句首，否则相邻两条双语字幕的中英文会互相错开（例如“这个 repo 会复用 cheese-app-endpoint，如果它已经存在；不存在就新建一个”
“机器一直在计费，直到你取消部署”）。kfp 的调用和名字放在分句末尾或全角标点之后（“三个标了 @dsl.component 的 Python 函数：
square、add 和 square root。”），这样字幕切分不会把 Vertex AI Pipelines、Model Registry 这类名字拆到两行上。校对时用工具链的
切分函数（`explainer.subtitles.split_balanced` / `_split_like`）逐句核对了长句的中英配对，并为此调整了两句的措辞：S02[2]
改成“你描述这个图用的是 Kubeflow Pipelines，也就是 kfp 这个库”，让“描述这个图”和“kfp 这个库”落在英文对应的那一段；S06[8]
改成“还不能调用，要等部署到一个 endpoint 上”，让整句和英文同屏，“就想”不再和下一段的 think 错开。渲染之后，在
`.zh-en.srt` 里再看一遍每条带 kfp 调用和产品名的字幕。

## 译文风格

按中国 MLOps 助教考前一天答疑串讲的说法，和第 1–13 讲一致：

- **一字不改**：你要在画面和选项里对照的东西（kfp 的调用和属性 `.output`、`.outputs`、`.after`、`@dsl.component`、
  `@dsl.pipeline`，YAML 的键 `dependentTasks`，玩具 pipeline 的名字 `square`、`add`、`square root`、`square-2`、`a`，示意图里
  的 task 名 prep、train、split、compare、ingest、clean、report、deploy，文件名 `raw.zip`、`clean.zip`，endpoint 名
  `cheese-app-endpoint`，参数 `sync` 和它的值 `True`，类名 `ExportArchive`，分支 `main`，base64，产品名 Vertex AI Pipelines、
  Kubeflow Pipelines、Agent Platform、Model Registry、Artifact Registry、Docker Hub、Cloud Run、SageMaker Pipelines）。字幕
  检查器不收的几种写法例外：带下划线的名字按旁白的念法写成空格（square root、bytes inputs），符号用文字说（`sync=True` 写成
  “sync 设为 True”，`.outputs["name"]` 写成“.outputs，在方括号里写上输出的名字”，224×224 写成“224 乘 224”，2 + 3 + 10 + 1
  写成“2 加 3 加 10 加 1”）；英文行通过 `en_display` 保留原样。
- **保留英文**：答疑课上本来就说英文的词，封闭清单：系列沿用的 repo、commit、container、image、registry、bucket、pipeline、
  SDK、endpoint；这一讲新增 DAG、task（pipeline 图里的一个节点）、component（container component、Python component）。
- **其余用中文标准术语**（Vertex AI、Kubeflow 中文资料和算法教材里的译名，方便搜索）：工作流管理、有向无环图、节点、边、依赖、
  数据依赖、生产者、消费者、占位符、上游、编译、提交、写死、过期数据、并行、汇合点、最大安全重叠、最长路径、竞态、调度、
  错开时间、后台命令、事件、触发、实验追踪工具、签名、解码、浮点数、缩放、注册、地址、复用、流量、计费、预测、客户端、键、
  分数、清理、取消部署、经验法则、属性、引用、步骤列表、托管。
- **比喻按意思译，一个比喻一个词**：时钟（cron）、连线（wire）、输出插口、遥控器（SDK）、压成（编译器把图压成 YAML）、
  汇合点、泳道、骰子、目录卡片（注册表里的一项）、地址（endpoint）、配方（DSL 写的 pipeline）。
- **分清容易混的词**：task 是图里的节点，照说英文；job 是“任务”（cron 任务、SDK 提交的 pipeline 任务、训练步骤启动的训练任务），
  第三题的答案就靠这一点（边等的是 task；pipeline 看不到它启动的任务）。连线是画出来的数据边，`.after` 的是虚线边；
  连线上带的值叫“值”，不说 token。registry 是 Docker image 的仓库，Model Registry 是产品名，“注册”是动作；部署是动作，
  deploy 是 task 名。“错在两处”说的是追踪工具那条泳道的两种错法，不是骰子掷了两次都错。笔记本是 laptop。
- **精确**：数字照旁白写（凌晨 1 点、75 分钟、16 分钟、5 秒）；“最大安全重叠”就是数据需要的边一条不多、一条不少；计费从部署
  开始，到取消部署为止；`main` 分支上训练会自己下载数据集，所以 cheese app 的边传的是顺序，不是数据（和课件不同处照说）；
  思考题只问不答；选择题的答案先给字母，再按英文的顺序逐个说错误选项错在哪（“A：……”“C：……”）。
- 标题、章节名、简介和这份说明用书面语：仓库、容器、镜像、镜像仓库（registry）、存储桶、端点（endpoint）、任务（task）、
  组件（component）、有向无环图（DAG）、模型注册表（Model Registry）、服务签名；pipeline、DAG、kfp 书面也照写。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| pipeline | pipeline | 流水线、管道 |
| DAG (directed acyclic graph) | DAG（字幕）；有向无环图（书面） | 有向无环图 |
| task | task（字幕）；任务（task）（书面） | 任务 |
| component | component（字幕）；组件（书面） | 组件 |
| job | 任务 | 作业 |
| edge | 边 | 依赖边 |
| placeholder | 占位符 | 占位符 |
| join | 汇合点 | 汇聚节点 |
| maximum safe overlap | 最大安全重叠 | 最大并行 |
| longest path | 最长路径 | 关键路径 |
| race | 竞态 | 竞争条件 |
| stale data | 过期数据 | 陈旧数据 |
| endpoint | endpoint（字幕）；端点（书面） | 终端节点 |
| Model Registry | Model Registry（字幕）；模型注册表（书面） | 模型仓库 |
| undeploy | 取消部署 | 解除部署 |
| signature | 签名（字幕）；服务签名（书面） | 服务签名 |
| tracker | 实验追踪工具 | 实验跟踪平台 |
