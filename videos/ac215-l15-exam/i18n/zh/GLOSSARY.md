# AC215 第 15 讲考前版中文字幕词表（中英混用版）

视频：*AC215 · Lecture 15 — ML Workflows with Vertex AI (exam edition)*（`videos/ac215-l15-exam`）
受众：Quiz 4 前一天的 AC215（哈佛 MLOps & LLMOps）中文研究生：上过（或翻过）第 15 讲，会 Python，在前几讲见过 Docker 和 cheese app 的采集器、处理器和训练器（第 2–4 讲的 container 和 bucket，第 13 讲的 Vertex AI 自定义任务），可能从没跑过 ml-workflow 或 model-deployment。他们不开 repo、不敲命令，只想把 pipeline 是 DAG、task.output 造出的边、并行、强制顺序和模型部署这几道选择题想清楚，并说出每个错误选项错在哪。语体：中国 MLOps 助教考前串讲。
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l15-exam.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长，只保留显示规则。但没有 `say:` 时，`python -m explainer.i18n check` 仍会对显示行做朗读检查（括号、数学符号、带下划线的名字、词表里没有的拉丁词、缺少的半角空格）：A6、B3、D3 三条规则就是为此而写。
英文原稿：`script.md` v2（SAY 行是旁白：76 段、186 句；S01 23、S02 24、S03 28、S04 24、S05 34、S06 21、S07 17、S08 15 句）；script.md 开头的 en_display 候选清单和词库说明。课件：`../ac215-l15-vertex-ml-workflows/SLIDES.md`（只读）。
先例：系列试点 [`ac215-l01-vms-venvs`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md)（repo、commit、笔记本指电脑）；容器三讲 L2–L4（container、image、registry、bucket、退出码、部署、配方，以及这份文件沿用的纯字幕规则）；L05–L07（工作流；图 / 边 / 节点）；[`ac215-l08-llm-finetuning`](../../../ac215-l08-llm-finetuning/i18n/zh/GLOSSARY.md)（endpoint、托管，A1–I3 的规则编排）；同为考前版的 [`ac215-l13-exam`](../../../ac215-l13-exam/i18n/zh/glossary.yaml)（考前版、小测、job 译“任务”、提交、计费、连线、实验追踪工具，以及选择题和结论卡的固定说法 D6）。第 1–13 讲定下的说法一律沿用。
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成；“说明”一栏与 yaml 的 note 逐字相同，保留英文，免得两份走样）

## 为什么要中英混用

- 中国的 MLOps 工程师讲 Kubeflow / Vertex AI Pipelines 时本来就中英混着说：“这个 DAG”“调用 component 会创建一个 task”“把上游 task 的 .output 传进去”“用 .after 排一下顺序”“部署到 endpoint”。硬说“任务（task）”“组件”，考前串讲反而像在念说明书，而且会和 job（任务）撞车。
- 这是考前版：观众要在英文选项、代码面板和 YAML 里认出这些东西。kfp 的调用和属性（.output、.outputs、.after、@dsl.component、@dsl.pipeline）、YAML 的 dependentTasks、玩具 pipeline 的函数名和 task 名、文件名、endpoint 的名字一旦翻译，就和题目对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（有向无环图、节点、边、依赖、上游、占位符、并行、最长路径、竞态、编译、签名、注册、部署、取消部署、流量、预测、计费）一律说中文，用 Vertex AI 中文文档和算法教材里能搜到的标准译名。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：代码和 README 面板、示意图标注、标签、选择题卡片、黄色结论卡和七条规则都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教考前一天带大家串讲时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“建一个 bucket”“推一个 image 到 registry”“调一个 endpoint”“提交一个任务”；这期再加上“一个 DAG”“创建一个 task”“写一个 component”“上游 task 的 .output”“用 .after 排顺序”。每个选择都要过三关：考前串讲真的这么说；是能搜到的标准中文名；和系列一致（第 1–13 讲定下的说法一律沿用）。

1. **实物原样**：观众要在屏幕上和选项里对照的东西（kfp 的调用和属性、dependentTasks、square / add / square root / square-2、prep / train / split / compare 这些 task 名、raw.zip、clean.zip、cheese-app-endpoint、bytes inputs、sync 和 True、ExportArchive、main）逐字照抄，不翻译、不变形、不加引号；检查器逼出来的例外是带下划线的名字和 = ( ) [ ] " 这些字符，按旁白的念法写（A6、B3）。
2. **口语里的英文，封闭清单**：系列已有的 repo、commit、container、image、registry、bucket、pipeline、SDK、CLI、endpoint；**这一期新增 DAG、task、component**（container component、Python component）。
3. **其余一律用中文标准术语**：工作流、有向无环图、节点、边、依赖、生产者、消费者、步骤、调用、占位符、上游、连线、插口、编译、提交、执行、任务、写死、过期数据、并行、汇合点、最大安全重叠、最长路径、竞态、错开时间、后台命令、事件、触发、实验追踪工具、泳道、部署、签名、注册、目录卡片、地址、流量、计费、预测、客户端、取消部署、属性、引用、配方、托管、小测。
4. **视频的比喻按意思译，一个比喻一个词**：时钟、连线、插口、遥控器、压成（编译器把图压成 YAML）、汇合点、泳道、骰子、目录卡片、地址、配方。
5. **书面语体**（标题、meta.yaml、配套文档）：仓库、提交、容器、镜像、镜像仓库（registry）、存储桶、端点（endpoint）、有向无环图（DAG）、任务（task）、组件（component）、模型注册表（Model Registry）、服务签名；pipeline、DAG、kfp 书面也照写。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **不出现人名**；不写项目 ID、bucket 名、endpoint ID、密钥（A10）。
8. **工具链的约束也是规则**：每个英文句子对应一个中文句子（76 段、186 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；考前串讲的语气：清楚、不赶，不用网络流行语。

## 关键决定

- **task 留英文，job 译“任务”**（A1 c、A7）：task 是 pipeline 图里的节点（kfp 的 PipelineTask），题目和代码都这么叫；job 沿用第 13 讲译“任务”（cron 任务、pipeline 任务、训练任务、编译好的任务）。第三道思考题的关键就在这里：**边等的是 task，pipeline 看不到它启动的任务**。
- **DAG 留英文**，第一次说全称“有向无环图”（S02[0]）；有向 / 无环；节点 / 边沿用第 7 讲。
- **component 留英文**（kfp 的词，屏幕上是 @dsl.component）；container component、Python component 照说，书面写 容器组件 / Python 组件。
- **连线和边分开**（A7）：wire（带着值的那根数据线）→ 连线；edge（图的边）→ 边；.after 画的是虚线边，不是连线。线上跑的 token 是“值”，不是 LLM 的 token。
- **kfp 的写法**（A6、B3、D4）：dot output → .output；dot outputs → .outputs，“在方括号里写上输出的名字”用文字说；dot after → .after（不带括号）；sync=True → sync 设为 True；bytes_inputs → bytes inputs；square_root → square root；英文行用 en_display 还原字面形式。
- **竞态、过期数据、写死**：race → 竞态（不说“赛跑”）；stale → 过期；hard-code → 写死；a guessed path → 猜出来的路径；this run / last run → 这次运行 / 上一次运行（这期没有 W&B 的 run，所以 run 这个名词说中文）。
- **最大安全重叠、汇合点、最长路径**：maximum safe overlap → 最大安全重叠（照题目直译，方便对照）；join → 汇合点；longest path → 最长路径（旁白没说 critical path，不加“关键路径”）。
- **部署四步**：upload → 上传，register → 注册，Model Registry 照写，catalog card → 目录卡片，endpoint 照说、书面“端点（endpoint）”，deploy → 部署，traffic → 流量，billing → 计费，predict → 预测，undeploy → 取消部署。registry（Docker 的镜像仓库）和 Model Registry 分开。
- **考前版的固定说法**（D6，和第 13 讲一致）：题目说 X，就想：Y；选项要是……，就想：……；来做一题；想停的话，就在这里暂停；答案是 B；祝你小测顺利。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：.output、.outputs、.after、@dsl.component、@dsl.pipeline、kfp、dependentTasks、square、add、square root、square-2、prep、train、split、compare、ingest、clean、report、deploy（作为 task 名时）、raw.zip、clean.zip、model 目录、cheese-app-endpoint、bytes inputs、sync、True、ExportArchive、main、base64、标签名（illustration、README example、slide 37、main today）。
- 产品、组织、课程和名字：AC215、Google、Google Cloud、Vertex AI、Vertex AI Pipelines、Kubeflow、Kubeflow Pipelines、Kubernetes、Agent Platform、Model Registry、Artifact Registry、Cloud Run、Docker、Docker Hub、Keras、TensorFlow、Python、YAML、JPEG、AWS、SageMaker、SageMaker Pipelines、GitHub、README、DSL、SDK。
- 口语里的英文，封闭清单：repo、commit、container、image、registry、bucket、pipeline、SDK、CLI、endpoint（系列已有）；**DAG、task、component（这一期新增）**。
- 系列清单里保留英文、但这一期没说到的：token、prompt、volume、venv、PATH、agent、port、epoch、batch、loss（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| job / cron job / pipeline job | 任务 / cron 任务 / pipeline 任务 | task / tasks | task |
| workflow / workflow management | 工作流 / 工作流管理 | directed acyclic graph / DAG | 有向无环图 / DAG |
| directed / acyclic | 有向 / 无环 | graph / node / edge | 图 / 节点 / 边 |
| dependency / data dependency | 依赖 / 数据依赖 | producer / consumer | 生产者 / 消费者 |
| component / Python function | component / Python 函数 | pipeline function / call | pipeline 函数 / 调用 |
| compiler / compile / compiled YAML | 编译器 / 编译 / 编译出来的 YAML | submit / execute | 提交 / 执行 |
| the SDK, the lecture's remote control | SDK，课上说的遥控器 | laptop / machine | 笔记本 / 机器 |
| placeholder / upstream | 占位符 / 上游 | succeed / fail | 成功 / 失败 |
| wire / plug in / output socket | 连线 / 接上 / 输出插口 | dashed edge / order without data | 虚线边 / 只管顺序、不传数据 |
| hard-code / guessed path | 写死 / 猜出来的路径 | stale data / last run's file | 过期数据 / 上一次运行的文件 |
| this run / at run time | 这次运行 / 运行的时候 | a named output | 有名字的输出 |
| in parallel / join | 并行 / 汇合点 | token (a value on a wire) | 值 |
| maximum safe overlap | 最大安全重叠 | longest path | 最长路径 |
| race / half-written | 竞态 / 写了一半 | preprocess / train / deploy | 预处理 / 训练 / 部署 |
| lane / roll / die | 泳道 / 掷 / 骰子 | cron offsets / background commands | cron 错开时间 / 后台命令 |
| event / fire | 事件 / 触发 | tracker / leaderboard | 实验追踪工具 / 排行榜 |
| launcher | 只负责启动的步骤 | correct by construction | 从结构上就保证了正确 |
| signature / decode / resize | 签名 / 解码 / 缩放 | upload / register | 上传 / 注册 |
| Model Registry / catalog card | Model Registry / 目录卡片 | endpoint / address | endpoint / 地址 |
| deploy / traffic / billing | 部署 / 流量 / 计费 | predict / client / key | 预测 / 客户端 / 键 |
| cleanup / undeploy / delete | 清理 / 取消部署 / 删除 | rule of thumb | 经验法则 |
| collector / processor | 数据采集器 / 数据处理器 | container / Python component | container / Python component |
| property / reference / list of steps | 属性 / 引用 / 步骤列表 | recipe / managed | 配方 / 托管 |
| quiz / question / option / answer | 小测 / 题目 / 选项 / 答案 | the lecture / the slides / course staff | 课上 / 课件 / 课程团队 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的中文句子，k 从 0 数），每一句都能通过检查器；“说明”与 glossary.yaml 的 note 相同。这个系列没有中文配音，所以没有“朗读（say:）”一栏。

### 开头：凌晨两点的竞态 / The 2 a.m. race

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| nightly jobs / job / cron job / pipeline job / training job | 任务 / 每晚的任务 / 时钟 | S01[0]：时钟上排着每晚的三个任务。 | job → 任务 (L13, the sibling exam edition: 任务 for a job): a cron job → cron 任务, the pipeline job the SDK submits → pipeline 任务, the job a training step launches → 训练任务 / 它的任务, the compiled job → 编译好的任务. Kept apart from task, which stays English (A7). For months, it works → 几个月来，一切正常. |
| prepare the data / preparation / preprocessing / preprocess / at 1 in the morning | 准备数据 / 预处理 / 凌晨 | S01[0]：凌晨 1 点准备数据。 | S01's preparation → 准备数据 (the night story); from S04 on preprocessing / preprocess → 预处理 (Q-style wording: 预处理、训练、部署). Times: 1 in the morning → 凌晨 1 点; Train at 2. → 2 点训练。; Deploy at 3. → 3 点部署。 (C2: digits, 点; never a.m.). |
| half written / a half-written file / half the data / ships whatever training produced | 写了一半 / 一半的数据 | S01[1]：2 点，训练照样开始，读的是一个只写了一半的文件。 | half-written → 写了一半 (S01, S05[3]); half-finished results → 没算完的结果 (S04[5]); trained on half the data → 只用一半数据训练出来的. |
| exit status / status zero / exit 0 | 退出码 / 失败 | S01[2]：每个任务的退出码都是 0。 | 退出码 (L2-L4). The pair is parallel and short: Nothing failed. → 没有一个失败。 Nothing was right either. → 可也没有一个是对的。 The GREEN / RED lines on screen stay English (A11). |
| endpoint / serves a model / the model | endpoint / 模型 | S01[2]：而 endpoint 现在提供的，是一个只用一半数据训练出来的模型。 | endpoint stays (series list; first used in L08): 一个 endpoint, 这个 endpoint, 删除 endpoint. Written register 端点（endpoint）(A4). serves → 提供 / 对外提供. |
| the cheese app / four steps / a person at a terminal / Data Collector / Data Processor / Model Training / Model Deploy | cheese app / 步骤 / 终端 | S01[3]：课上也从同一个问题讲起：cheese app 的四个步骤，每一步都由一个人在终端上运行。 | cheese app stays (the course project's name, L4-L8). The slide tiles (1 Data Collector, 2 Data Processor, 3 Model Training, 4 Model Deploy, CLI) are on screen in English (A11). step → 步骤 / 一步 / 每一步. |
| automate / execute / this flow | 执行 / 自动化 / 流程 | S01[3]：能不能把这个流程自动化？ | The slide's two questions, translated as questions (the headline on screen stays English): How do we execute these steps? → 这些步骤要怎么执行？ |
| pipeline / instruction | pipeline / 指令 | S01[4]：这正是 pipeline 的用处。 | pipeline stays (series list, L3; L13): 一个 pipeline, 这个 pipeline, pipeline 函数, pipeline 任务. Written register also keeps pipeline (L3's titles do: pipeline 与你的第一个 Dockerfile). Not: train at 2. → 不是：2 点训练。 Instead: train when preparation has finished. → 而是：准备数据完成之后再训练。 |
| graphs / wires / overlap / order / deployment | 图 / 连线 / 重叠 / 顺序 / 部署 | S01[5]：接下来的安排：图、连线、重叠、顺序、部署，还有 cheese app。 | graph → 图, edge → 边, node → 节点 (L07's decision). wire → 连线 (L13's word for the wire). deploy / deployment → 部署 (L2). |
| gray tag / lecture tag / live run / illustration | 灰色标签 / 课件 / 现场运行 | S01[6]：这里没有任何现场运行。 | A11: tag names as on screen (illustration, README example, slide 37, main today, kfp 2.14.6 · read, not run); the narration's own words in Chinese: 灰色标签, 右上角. names the slides behind each idea → 标出每个想法背后的课件页. |
| race / race condition / fixed times / schedule | 竞态 / 时钟 / 调度 | S01[7]：选项要是在固定时间调度步骤，就想：竞态，时钟对数据一无所知。 | race (condition) → 竞态 (the standard term, 竞态条件 in the written register): 这就是竞态 (S04[5]); think race or wrong model → 就想：竞态，或者部署错了模型 (S05[11]). Never 赛跑 (the picture is a race, the concept is a race condition). |

### pipeline 是一张图：task 是节点，依赖是边 / A pipeline is a graph

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| workflow management / workflow | 工作流管理 / 工作流 | S02[0]：工作流管理，用课上的话说，知道哪一步需要哪一步。 | workflow → 工作流 (L06; L13's 训练工作流). ML Workflows (the lecture title) → 机器学习工作流 (H1). |
| directed acyclic graph / DAG / DAGs / pipelines are DAGs | 有向无环图 / DAG | S02[0]：记录这件事的结构叫有向无环图，也就是 DAG。 | A1 c, new: DAG stays (the quiz word; say it in every rule: pipeline 是 DAG; 同一个 DAG); directed acyclic graph → 有向无环图 (the standard term) once, S02[0]. Written register 有向无环图（DAG）. |
| directed / acyclic / producer / consumer | 有向 / 无环 / 生产者 / 消费者 | S02[1]：有向，是因为数据只朝一个方向流，从生产者流到消费者。 | Acyclic, because no step ever waits on itself. → 无环，是因为没有哪一步会等它自己。 producer task → 生产者 task (S03[2]). |
| task / tasks / node / nodes | task / 节点 | S02[1]：这些 task 就是节点；数据依赖就是边。 | A1 c, new: task stays (kfp's word and the quiz's: calling a component creates a task; PipelineTask): 一个 task, 两个 task, 上游 task, 预处理 task. Kept apart from 任务 = a job (A7): the edge waits for the task, not for the job the task launched (S05[8]). Written register 任务（task）where the context makes it unambiguous, else task. |
| edge / edges / data dependency / data dependencies / dependency | 边 / 数据依赖 / 依赖 | S03[3]：一个参数，就同时给了 add 数据和依赖。 | edge → 边 (L07): 一条边, 这些边, 虚线边, 数据不需要的边, 边上. dependency → 依赖 (L13). |
| Vertex AI Pipelines / Kubeflow Pipelines / K F P / kfp / Kubernetes / Agent Platform / console | Vertex AI Pipelines / Kubeflow Pipelines / kfp / Kubernetes / Agent Platform / 控制台 | S02[2]：你描述这个图用的是 Kubeflow Pipelines，也就是 kfp 这个库，而且不用你管 Kubernetes。 | Product names in Latin script (A1 b, A10). K F P → kfp (the package name as on screen; en_display: the kfp library, D4). Today's console calls it Agent Platform. → 现在的控制台把它叫作 Agent Platform。 Vertex runs / executes → Vertex 运行 / 执行. |
| toy pipeline / demo repo / slides | 玩具 pipeline / 示例 repo / 课件 | S02[3]：这是课件和示例 repo 里的那个玩具 pipeline。 | toy → 玩具 (玩具 pipeline, 玩具图 S04[0]: Back to the toy graph. → 回到那个玩具图。). repo stays (L1). |
| component / Python function / d s l dot component / d s l dot pipeline | component / Python 函数 / @dsl.component / @dsl.pipeline | S02[3]：三个标了 @dsl.component 的 Python 函数：square、add 和 square root。 | A1 c, new: component stays (kfp's word, on screen as @dsl.component): 一个 component, component 调用. Written register 组件（component）. d s l dot component / d s l dot pipeline → @dsl.component / @dsl.pipeline (en_display, D4). A fourth, marked d s l dot pipeline, wires them together. → 第四个标了 @dsl.pipeline，把它们连起来。 |
| square / add / square root / square 2 / pipeline input | square / add / square root / square-2 | S02[5]：这里 square 被调用了两次，所以一个 component 产生了两个 task；第二个叫 square-2。 | The toy's function and task names stay as on screen (A1 a); square_root → square root (A6); square 2 → square-2 (en_display). The values: on screen 9.0, 16.0, 25.0, 5.0; the SAY and the subtitle say 9, 16, 25, 5 (C1). Calling square on a, the pipeline's input, which defaults to 3 → 在 a 上调用 square，a 是 pipeline 的输入，默认值是 3. |
| pipeline function / component call / calling a component | pipeline 函数 / 调用 | S02[4]：在 pipeline 函数运行时，这些 component 调用什么都不算。 | A5: no sentence opens with lower-case pipeline: 在 pipeline 函数运行时 (a time adverbial with a Chinese head word). The function ran once, and produced only a graph. → 这个函数只跑了一次，产出的只有一个图。 |
| output socket / socket | 输出插口 / 数字 | S02[4]：还没有数字。 | socket (the drawn socket on a task node) → 插口; plug it in → 接上 (S03[1]). Never 套接字 (that is a network socket). |
| compiler / compile / YAML file / compiled YAML | 编译器 / 编译 / YAML 文件 | S02[6]：编译器把这个图压成一个 YAML 文件。 | YAML stays; the compiled YAML → 编译出来的 YAML; writes down → 写下 (S03[2]). Your laptop compiles and submits. → 你的笔记本负责编译和提交。 |
| Vertex AI SDK / remote control / submit | Vertex AI SDK / 遥控器 / 提交 / pipeline 任务 | S02[6]：Vertex AI SDK，也就是课上说的遥控器，把它提交成一个 pipeline 任务。 | SDK stays (L6). submit → 提交 (L13; ≠ commit, which stays English, A7). aip.PipelineJob is on screen only; a pipeline job → pipeline 任务. |
| laptop / machine / Google machines | 笔记本 / 机器 / container | S02[7]：直到这时，在 Google 的机器上，每个 task 才有了 container，数字才出现。 | laptop → 笔记本 (L1; never notebook, which is a Jupyter notebook). machine → 机器 (一台机器). container stays (L2). Vertex executes. → 执行的是 Vertex。 |
| compiled job | 编译好的任务 | S02[8]：什么都不会运行，要等到编译好的任务真正运行。 | The S02 takeaway: If an option says calling train in the pipeline function trains the model, think again: it only creates a task. → 选项要是说，在 pipeline 函数里调用 train 就会训练模型，再想想：它只是创建了一个 task。 (D6). |

### .output：造出边的那根连线 / task.output: the wire that makes an edge

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| dot output / placeholder / upstream task / succeed | .output / 占位符 / 上游 / 成功 | S03[1]：这里的 .output 是一个占位符，代表一个只有上游 task 成功之后才存在的值。 | dot output → .output (en_display .output, D4); never translated, never opens a sentence (A5: 这里的 .output, 第一个 square task 的 .output). upstream → 上游; succeeds → 成功; Not a number. → 不是一个数。 |
| wire / plug in / path of wires | 连线 / 接上 | S03[1]：把它接上，就画出了一根连线。 | wire → 连线 (measure word 根); 9 rides the wire into add → 9 顺着连线进入 add. path of wires → 连线组成的路径 (S04[0], S04[10]). The PINK solid / dashed edges are pictures; the words stay 连线 and 边. |
| dependent tasks / dependentTasks / producer task | dependentTasks / 生产者 task | S03[2]：编译出来的 YAML 把每根连线写了两遍：add 的 dependentTasks 列出 square 和 square-2，每个输入也写明了它的生产者 task。 | dependent tasks → dependentTasks (the YAML key, en_display, D4); in the compiled YAML they become dependent tasks → 在编译出来的 YAML 里，它们变成了 dependentTasks (S05[6]). |
| run time / turns green / argument | 变绿 | S03[3]：运行的时候，square 变绿，然后 9 才顺着连线进入 add。 | At run time → 运行的时候 (never 运行时, which is a runtime, L08). green check → 绿色的勾 (S07[0]). |
| dot outputs / output name / several outputs / named output | .outputs / 输出的名字 | S03[4]：有多个输出时，就点名要哪一个：用 .outputs，在方括号里写上输出的名字。 | dot outputs → .outputs (en_display .outputs["name"], D4; the brackets and quotes cannot be in the Chinese line, B3, so the Chinese says them in words). a named output → 一个有名字的输出 (S08[1]). |
| hard-code / hard-coded path / guessed path / this run | 写死 / 路径 / 这次运行 | S03[5]：改成把路径写死，就没有连线：train 马上开始，和 prep 一起跑。 | hard-code → 写死; guess → 猜 (a guessed path → 猜出来的路径); a path you assumed → 你假设的路径. this run → 这次运行 (the noun run of a pipeline run is said in Chinese here: there is no W&B run in this video, unlike L13); this run's value / file → 这次运行的值 / 文件; last run's → 上一次运行的. |
| stale data / stale read / last run | 过期数据 / 过期 | S03[6]：那里的文件是上周的，这一步在过期数据上成功了。 | stale → 过期 (maybe stale → 可能是过期的). the stale read from earlier → 前面说的读到过期数据 (S07[3]). A guessed path looks like a dependency to you, not to the pipeline. → 猜出来的路径在你看来像依赖，在 pipeline 看来不是。 |
| prep / train / split / compare / ingest / clean / report / deploy (task names) | prep / train / split / compare / ingest / clean / report | S03[9]：A 把路径写死了：没有边，所以 train 可能马上开始，读到上一次运行的文件。 | The illustration's neutral task names stay as on screen when the SAY names the task (train starts right away → train 马上开始); when the SAY says the activity (training, the comparison, the big training) it is Chinese (训练, 比较, 大的那个训练). train_cnn / train_tree are on screen only. deploy as a task name in S05[8] / S05[10] → deploy; as an activity → 部署. |
| dot after / dashed edge / ordering edge | .after / 虚线边 / 顺序 | S03[7]：要只管顺序、不传数据，就用 .after 加一条虚线边：这个 task 会等另一个成功，但边上什么都不传。 | dot after → .after (en_display .after(), D4; no brackets in the Chinese line, B3). Dot after: order, but no data. → .after：有顺序，没有数据。 is the one place a sentence may open with the artifact (a recap label, as L13's rule rows); elsewhere 用 .after. |
| ponder / option / answer / multiple choice | 选项 / 答案 / 暂停 | S03[8]：想停的话，就在这里暂停。 | D6 fixed phrases (L13): Try one. → 来做一题。 Your turn to compute one. → 轮到你算一题。 One more, a subtle one. → 再来一题，有点绕。 B. → 答案是 B。 B, 16 minutes. → 答案是 B，16 分钟。 A / C / D open their sentences with the bare letter (C 会等，但……; D 在……). |
| hand over / plain dot output / refuse | 等待 / 拒绝 | S03[10]：D 在任何东西运行之前就失败了：有两个输出时，kfp 不接受单独的 .output。 | The kfp error text is on the PURPLE-chipped panel only (A11), never quoted in a subtitle. Naming the output hands over this run's file, and creates the wait. → 点名这个输出，就把这次运行的文件传了过去，也建立了等待。 |
| takeaway / takeaway card | 题目 / 选项 / 结论 | S03[11]：题目说 .output，就想：等上游成功，拿到这次运行的值。 | D6 (L13): If the question says X, think Y. → 题目说 X，就想：Y。 If an option says / uses / schedules … → 选项要是……，就想：……. The YELLOW takeaway card stays English (A11); the subtitle translates the SAY. |

### 最大安全重叠 / Maximum safe overlap

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| in parallel / parallel | 同时 / 并行 | S04[10]：两个步骤之间要是没有连线组成的路径，就想：并行。 | parallel → 并行 (never 平行). Vertex is free to run them at the same time → Vertex 可以同时运行它们. |
| join / join task | 汇合点 / 输入 | S04[1]：这个 add 是一个汇合点。 | join (a task with several incoming edges) → 汇合点; a join waits for all its inputs → 汇合点要等齐所有输入 (S08[2]). Never 连接 (that is a SQL join). |
| preprocessing task / training / comparison | 预处理 / 训练 / 比较 | S04[2]：同样的形状，放大一号：一个预处理 task，两个读它输出的训练，再加一个读两个模型的比较。 | training (one training run) → 训练 (两个训练, 大的那个训练, 小的那个训练); comparison → 比较; compare as a task name stays (C ignores the edges … compare waits for both models → compare 要等两个模型). |
| light up / incoming wire / value token | 亮起来 / 值 | S04[3]：一个 task 亮起来，要等每根输入连线都带上值。 | token here is the value marker riding a wire → 值 (A7: never token, which is the LLM token in this series). The comparison starts exactly when the slower one ends → 比较正好在慢的那个结束时开始. |
| extra edge / half-finished results / time zero | 边 / 0 时刻 / 竞态 | S04[4]：加一条数据不需要的边：答案一样，跑得更久。 | Replace those wires with guessed paths → 把这些连线换成猜出来的路径; starts at time zero → 在 0 时刻就开始. That is a race. → 这就是竞态。 |
| maximum safe overlap | 最大安全重叠 | S04[6]：最大安全重叠的意思是：数据需要的边，一条不多，一条也不少。 | maximum safe overlap → 最大安全重叠 (the quiz's phrase, translated literally so it can be matched; written register 最大安全重叠（maximum safe overlap）in the chapter title, H1). |
| longest path / the run lasts its longest path | 最长路径 | S04[6]：这样一次运行的时长就等于它的最长路径。 | longest path → 最长路径 (the SAY never says critical path; do not add 关键路径). The longest path is ingest, clean, the big training, and compare. → 最长路径是 ingest、clean、大的那个训练和 compare。 |
| upstream failure / fail / failed task | 失败 / 上游 | S04[6]：如果上游有 task 失败，汇合点就永远不会运行。 | fail → 失败 (a failed training → 失败的训练; fails if the job fails → 任务失败它也失败). |
| minutes / plus / in sequence | 分钟 / 加 / 依次 / 一个接一个 | S04[8]：2 加 3 加 10 加 1。 | B3: plus → 加 (never +). 16 minutes → 16 分钟. A adds every task in sequence. → A 把所有 task 依次加起来。 D runs the two trainings one after the other. → D 让两个训练一个接一个地跑。 overlap with → 和……重叠. |

### 强制顺序：靠边，不靠时钟 / Enforcing order: edges, not clocks

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| sequence / preprocess / train / deploy | 顺序 / 预处理 / 训练 / 部署 | S05[0]：现在说顺序：预处理、训练、部署。 | Q-style chain → 预处理、训练、部署 (the same words in S05[11] and the S08 rules). |
| lane / clock lane / background lane / tracker lane / edge lane | 泳道 | S05[1]：第一条泳道：cron 错开时间。 | V4's four lanes → 泳道 (第一条泳道 … 第四条泳道; 时钟那条泳道, 后台那条泳道, 追踪工具那条泳道, 边那条泳道). The lane labels on screen stay English (A11). |
| cron / cron offsets | cron / 错开时间 | S05[11]：选项要是用 cron 错开时间、后台命令，或者追踪工具里最好的模型，就想：竞态，或者部署错了模型。 | cron stays (the tool's name, ORANGE clock); cron offsets → cron 错开时间; a cron job → cron 任务. |
| background ampersand / background command | 后台 / 后台命令 | S05[1]：第二条泳道：后台的 &。 | & is said in the SAY (background ampersands) and shown on screen; the Chinese line writes & (not rejected by the checker) and 后台; en_display candidate: Lane two, background & jobs. (D4; decided in narration step). The background lane is broken on every roll, because nothing waits. → 后台那条泳道每次都出错，因为什么都不等。 |
| event / fire / trigger | 事件 / 触发 | S05[4]：这个事件可能在第一个文件写出来时就触发，那时预处理还没做完。 | event → 事件; fire / trigger → 触发. |
| tracker / best model / leaderboard | 实验追踪工具 / 追踪工具 / 排行榜 | S05[4]：而且追踪工具里最好的模型，是所有运行里最好的，不是这次运行的。 | tracker → 实验追踪工具 at first use (S05[1]), then 追踪工具 (L13 A3: tracker → 实验追踪工具, never 进度条). The leaderboard is on screen only; the GREY dashed old run and today's model stay English labels. |
| roll / die | 骰子 / 掷 | S05[2]：掷一下骰子，决定预处理要多久。 | Roll the length of preprocessing. → 掷一下骰子，决定预处理要多久。 40 minutes. → 40 分钟。 Then 75. → 然后 75。 Then 55. → 然后 55。 on every roll → 每一次都. |
| stretch / broken | 拉长 / 出错 | S05[4]：它只是被拉长了。 | broken → 出错 (fine at 40, broken at 75 → 40 没问题，75 就出错). The tracker lane fails twice. → 追踪工具那条泳道错在两处（two failure modes, not two rolls）。 |
| collector / processor / collection / processing / data collector / data processor | 数据采集器 / 数据处理器 / 采集 / 处理 | S05[5]：这个 cheese app 的 pipeline 正是这样做的：采集之后处理，处理之后训练，训练之后部署，每一步都用 .after。 | The steps by meaning: collector / processor → 数据采集器 / 数据处理器 (S07[1]: 采集器和处理器 after the first), collection / processing → 采集 / 处理. The image names dlops/cheese-app-data-collector etc. are on screen only. |
| README | README | S05[6]：README 也说得很直白：每一步都要等上一步成功之后才开始。 | README stays (A1 b); the quoted README line is on screen in English, the subtitle translates the SAY's paraphrase. |
| launch / launcher / another machine | 启动 | S05[8]：一条边等的是 task，而这个 task 5 秒后就成功了。 | The P3 point, said exactly (A9): the edge waits for the task, never the job: 边等的是 task；pipeline 从来看不到它启动的任务. launcher → 只负责启动的步骤 (The repo's training step is such a launcher. → 这个 repo 的训练步骤就是这种只负责启动的步骤。). |
| sync set to true / failed training | sync / 训练任务 | S05[10]：把 sync 设为 True 之后，它会等自己的任务，任务失败它也失败，所以 deploy 永远不会在失败的训练之后运行。 | sync set to true → sync 设为 True (A6; en_display sync=True, D4; True as on screen at model.py:62). |
| commit / course staff | commit / 课程团队 | S05[10]：最近一次 commit 把这个等待写明了。 | commit stays (L1). The commit author is never named: the course staff → 课程团队 (A10). explicit → 写明 / 显式. |
| correct by construction / wrong model / previous model | 错的模型 | S05[11]：从预处理到训练再到部署的边，从结构上就保证了正确。 | correct by construction → 从结构上就保证了正确. deploy may ship the previous model → deploy 可能把上一个模型发布出去. |

### Model Registry、endpoint、部署与预测 / Registry, endpoint, deploy, predict

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| deployment / saved model / upload / register / bucket | 部署 / 保存的模型 / 上传 / 注册 / bucket | S06[0]：课上把部署画成五步：拿到保存的模型，更新它的签名，上传到 bucket，注册，再部署到 endpoint。 | bucket stays (L3; written 存储桶). upload → 上传; register → 注册; deploy → 部署 (L2). |
| signature / serving signature / decode / floats / resize | 签名 / 解码 / 浮点数 / 缩放 | S06[1]：签名这一步把预处理搬进模型里：解码 JPEG，转成浮点数，缩放到 224 乘 224，再调用模型。 | serving signature → 签名 (written 服务签名). B3: 224 by 224 → 224 乘 224. The signature unfolds it → 签名把它解开. |
| Keras export archive / ExportArchive | Keras / ExportArchive | S06[1]：课件用一种方式保存，repo 用的是 Keras 的 ExportArchive。 | The SAY says Keras export archive; the subtitle writes the class name ExportArchive (en_display: the Keras ExportArchive, D4). tf.saved_model.save is on the slide panel only (never in a subtitle: underscores, A6). |
| Model Registry / catalog card / registry card | Model Registry / 目录卡片 | S06[2]：注册就是建一张目录卡片。 | Model Registry stays (product name; written 模型注册表（Model Registry）). catalog card (the V5 picture) → 目录卡片; the registry card → 注册的那张卡片. Kept apart from registry (L2: a Docker image registry, S07[1]) (A7). Nothing is running, and it costs nothing. → 什么都没在运行，也不花钱。 Can you call it? → 能调用它吗？ Not yet. → 还不能。 |
| address / reuse / cheese app endpoint | 地址 / 复用 / cheese-app-endpoint | S06[3]：这个 repo 会复用 cheese-app-endpoint，如果它已经存在；不存在就新建一个。 | cheese app endpoint → cheese-app-endpoint (the endpoint's display name, en_display, D4). Next, the endpoint: an address. → 接下来是 endpoint：一个地址。 No endpoint id is ever written (A10). |
| deploy / traffic / billing / machine | 流量 / 机器 / 计费 | S06[4]：部署就是在这个地址下面放一台机器，把全部流量都给它。 | traffic → 流量; billing → 计费 (L13); you pay for that machine → 你要为这台机器付钱. Money is never quantified (no price is said). |
| predict / prediction / client / base 64 / bytes inputs / scores | 预测 / 客户端 / base64 / 键 / bytes inputs / 分数 | S06[5]：预测时，客户端把每张 JPEG 用 base64 编码，放在 bytes inputs 这个键下面。 | base 64 → base64 (en_display, D4); bytes inputs → bytes inputs (A6; en_display bytes_inputs). The four probability bars carry the tag README example; the class is never named (the README does not say which cheese). |
| cleanup / undeploy / delete | 清理 / 取消部署 / 删除 | S06[6]：清理时先取消部署模型，机器就停了，然后删除 endpoint。 | undeploy → 取消部署 (the Vertex AI Chinese documentation's term); delete → 删除. |
| Cloud Run / rule of thumb | Cloud Run / 经验法则 | S06[7]：而按课件的经验法则，Cloud Run 适合模型只是一个更大应用的一部分的时候。 | The pipeline's deploy step makes the same two calls. → pipeline 里的部署步骤做的也是这两个调用。 |
| registered / callable / deployed | 已注册 / 可调用 / 已部署 | S06[8]：题目说已部署，就想：机器一直在计费，直到你取消部署。 | S06's takeaway, D6 and D9 (English order: billing, then until). If the question says registered, think: not callable until it is deployed to an endpoint. → 题目说已注册，就想：还不能调用，要等部署到一个 endpoint 上。 |

### cheese app 的 pipeline，以及 AWS 上的同一个 DAG / The Cheese App pipeline, and the same DAG on AWS

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| green check | 绿色的勾 | S07[0]：每一步成功时，都会打上一个绿色的勾。 | Now the whole cheese app pipeline: collector, processor, training, deploy. → 现在看完整的 cheese app pipeline：采集器、处理器、训练、部署。 |
| container component / Python component / published image / registry / Docker Hub / Artifact Registry | container component / Python component / image / registry / Docker Hub / Artifact Registry | S07[1]：训练和部署是 Python component，调用的是 Vertex AI SDK。 | container component / Python component stay (kfp's kinds; written 容器组件 / Python 组件). image and registry stay (L2): 发布好的 image, 从 registry 拉取 (pull → 拉取). Google's machines cannot see your laptop → Google 的机器看不到你的笔记本. |
| raw zip / clean zip / model folder / bucket file | raw.zip / clean.zip / model 目录 | S07[2]：每一步都从 bucket 读，再写回去：raw.zip、clean.zip，然后是 model 目录。 | raw zip / clean zip → raw.zip / clean.zip; the model folder → model 目录 (en_display: raw.zip, clean.zip, the model/ folder, D4). The steps never call each other. → 这些步骤从不互相调用。 |
| by name / model name | 名字 | S07[2]：这个 pipeline 只决定每一步什么时候开始。 | So deploy finds the model by name, in the model folder, and the edges make that name safe. → 所以 deploy 按名字在 model 目录里找模型，而这些边保证了这个名字是安全的。 |
| main branch / dataset | main 分支 / 数据集 | S07[4]：和课件有一处不同：现在的 main 分支上，训练会自己下载数据集，所以这些边传的是顺序，不是数据。 | main 分支 (the branch name stays). Slide conflicts are said kindly, in one clause (A9). |
| AWS / SageMaker Pipelines / step / output property / step properties / reference / referencing | AWS / SageMaker Pipelines / 步骤 / 输出属性 / 引用 | S07[5]：训练步骤的输入指向处理步骤的输出属性，这个引用就是边。 | SageMaker Pipelines and AWS stay (names). property → 属性; reference / referencing → 引用. SageMaker builds the same DAG from step properties. → SageMaker 用步骤属性搭出同一个 DAG。 |
| shuffle / list of steps | 打乱 / 步骤列表 | S07[6]：把 pipeline 的步骤列表打乱，图也不会动：顺序来自引用。 | the graph does not move → 图也不会动. |

### 七条规则 / Seven rules for the quiz

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| rule / seven rules | 规则 / 第一条 | S08[0]：第一条：pipeline 是 DAG。 | Seven rules. → 七条规则。 One: / Two: … / Seven: → 第一条：/ 第二条：… / 第七条： (L13's rule rows). The seven rule rows on screen stay English (A11). Billing starts at deploy. → 计费从部署开始。 |
| recipe / D S L / Kubeflow engine / managed | 配方 / DSL / Kubeflow 引擎 / 托管 | S08[5]：还有课上的那条链：用 DSL 写的配方，印成 YAML，由 SDK 提交，在 Kubeflow 引擎上运行，由 Vertex AI Pipelines 托管，不用自己搭 Kubernetes。 | D S L → DSL (en_display, D4). recipe → 配方 (L2's metaphor word). managed → 托管 (L08). |
| quiz | 小测 | S08[6]：祝你小测顺利。 | quiz → 小测 (L13); Quiz 4 only in titles and descriptions. When you are done, undeploy and delete the endpoint. → 用完之后，取消部署，再删除 endpoint。 |

### 课程、名字与产品 / Course, names, products

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / lecture / Lecture 15 / slides / course staff / exam edition | AC215 / 课上 / 课件 / 课程团队 / 考前版 | S07[4]：和课件有一处不同：现在的 main 分支上，训练会自己下载数据集，所以这些边传的是顺序，不是数据。 | A10 (L1-L13): Lecture 15 → 第 15 讲; the lecture → 课上; the slides → 课件; the course staff → 课程团队; exam edition → 考前版; the instructor is never named and never mentioned in this script. |
| Google / Google Cloud / Vertex AI / Kubeflow / Kubernetes / Docker / Docker Hub / Keras / TensorFlow / Python / YAML / JPEG / AWS / SageMaker / Cloud Run / GitHub | Google / Vertex AI / Kubeflow / Kubernetes / Docker / Keras / TensorFlow / Python / YAML / JPEG / AWS / SageMaker / GitHub | S02[7]：直到这时，在 Google 的机器上，每个 task 才有了 container，数字才出现。 | Latin script (A1 b). No logos, no versions spoken (kfp 2.14.6 is on the PURPLE chip only). |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上面各词条 zh_subtitle 和 first_use 里的拉丁词，字幕行还可以出现下面这些（实物按检查器的切法切开，D3）：

A、AC、add、after、Agent、AI、app、Artifact、AWS、B、base、base64、bucket、bytes、C、cheese、cheese-app-endpoint、clean、clean.zip、CLI、Cloud、CNN、Collector、commit、compare、component、container、cron、D、DAG、DAGs、Data、dependentTasks、deploy、Deploy、Docker、DSL、dsl.component、dsl.pipeline、endpoint、ExportArchive、GitHub、Google、Hub、illustration、image、ingest、inputs、JPEG、Keras、kfp、KFP、Kubeflow、Kubernetes、Lecture、main、Model、model、output、outputs、pipeline、Pipelines、Platform、prep、Processor、Python、raw.zip、README、registry、Registry、repo、report、root、Run、SageMaker、split、square、square-、sync、task、TensorFlow、train、Training、tree、True、Vertex、YAML

## 规则

规则编号和 glossary.yaml 一致（英文原文在 yaml 里；这里是中文摘要，冲突时以 yaml 为准）。第 1 讲的 E（屏幕文字）和 F（语音）两组在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只留在三类地方：（a）**实物**，逐字照抄：.output、.outputs、.after、@dsl.component、@dsl.pipeline、kfp、dependentTasks、玩具 pipeline 的名字（square、add、square root、square-2、a）、旁白点名的 task 名（prep、train、split、compare、ingest、clean、report、deploy）、raw.zip、clean.zip、model 目录、cheese-app-endpoint、bytes inputs、sync 和 True、ExportArchive、main 分支、base64、标签名；（b）**产品、组织和课程的名字**（AC215、Google、Vertex AI Pipelines、Kubeflow Pipelines、Kubernetes、Agent Platform、Model Registry、Artifact Registry、Cloud Run、Docker Hub、Keras、YAML、JPEG、AWS、SageMaker Pipelines、README、DSL、SDK 等）；（c）**口语封闭清单**：repo、commit、container、image、registry、bucket、pipeline、SDK、CLI、endpoint，以及这一期新增的 DAG、task、component。其余一律说中文。
- **[A2]** container、image、registry（同第 2–13 讲）。字幕照说：每个 task 才有了 container；发布好的 image；从 registry 拉取。书面写 容器、镜像、镜像仓库（registry）。Model Registry 是产品名，字幕里不简称 registry（A7）。
- **[A3]** 这一期新增的词汇：见 yaml 的 A3 全表。要点：有向无环图（只在 S02[0] 说一次全称）、节点、边、依赖、生产者 / 消费者、pipeline 函数、调用、创建一个 task、编译、提交、pipeline 任务、执行；占位符、上游、连线、输出插口、接上、运行的时候、有名字的输出、写死、猜出来的路径、过期数据、这次运行、虚线边；并行、汇合点、值（线上的 token）、亮起来、最大安全重叠、最长路径、竞态；预处理 / 训练 / 部署、泳道、cron 错开时间、后台命令、事件、触发、实验追踪工具（之后简称追踪工具）、排行榜、掷骰子、被拉长、只负责启动的步骤、从结构上就保证了正确；签名、解码、浮点数、缩放、上传、注册、目录卡片、地址、复用、流量、计费、预测、客户端、键、分数、清理、取消部署、删除、经验法则；属性、引用、步骤列表；小测、题目、选项、答案、规则、结论。
- **[A4]** 字幕与书面。字幕说 repo / commit / container / image / registry / bucket / endpoint / task / component；标题、章节名、meta.yaml 和配套文档写 仓库 / 提交 / 容器 / 镜像 / 镜像仓库（registry）/ 存储桶 / 端点（endpoint）/ 任务（task）/ 组件（component），核心概念第一次出现时括注英文。pipeline、DAG、kfp、Model Registry 书面照写（有向无环图（DAG）、模型注册表（Model Registry））。
- **[A5]** 实物的写法。逐字照抄，不翻译、不变形、不加引号、不加《》或代码格式；需要时加中文中心词：model 目录、bytes inputs 这个键、kfp 这个库、main 分支、pipeline 函数。句子不以实物、点号或小写英文词开头，先放一个中文词（这里的 .output……；这些 task……；这里 square……；这个 add……；这个 repo……；在 pipeline 函数运行时……；把 sync 设为 True……）。大写的名字和缩写（Vertex、README、DAG、YAML、SageMaker、AWS）和选项字母 A–D 可以开头；S03[11] 的复习标签 .after： 是例外（同第 13 讲的规则行）。
- **[A6]** 带下划线的名字和代码表达式（同第 3–13 讲）：square_root → square root；bytes_inputs → bytes inputs；sync=True → sync 设为 True；.after() → .after；.outputs["name"] → .outputs，在方括号里写上输出的名字；train_cnn / train_tree 不进字幕（旁白说“大的那个训练 / 小的那个训练”）；tf.saved_model.save、aip.PipelineJob 只在屏幕上。英文行用 en_display 还原（D4）。
- **[A7]** 要分清的词。task（图里的节点，留英文）≠ 任务（job）；步骤（README 和课件说的 step）≠ task（kfp 对象），照旁白用词；连线（数据线）≠ 边（图的边；.after 是虚线边）；值（线上跑的 token）≠ token（不用）；registry（Docker 的镜像仓库）≠ Model Registry（产品）≠ 注册（动作）；部署（动作）≠ deploy（task 名）；运行的时候 ≠ 运行时（runtime，不用）≠ 这次运行（名词）；笔记本（电脑）≠ notebook（不用）；提交（submit）≠ commit；竞态 ≠ 赛跑（不用）；汇合点 ≠ 连接（不用）；并行 ≠ 平行（不用）；插口 ≠ 套接字（不用）。
- **[A8]** 语体：考前串讲的助教。短句，口语动词（调用、创建、接上、等、传、跑、读、写、部署、删）；观众是“你”（不用“您”“大家”“同学们”）；这期不跑任何东西，用不着“我们”。分句内部用中文语序，分句顺序跟英文走（D9）。不要翻译腔，不用网络流行语。短句按意思传节奏：没有一个失败。不是一个数。还没有数字。执行的是 Vertex。然后 75。它只是被拉长了。还不能。
- **[A9]** 准确。量词照译（只、每个 / 每次 / 每一步、全部、正好、永远不 / 从不、两次 / 两遍、马上）。考点照英文原样说，不弱化、不添加：边等的是 task；汇合点要等齐所有输入；一次运行的时长等于最长路径；计费从部署开始；只注册不能调用。三道思考题（S03[8]、S04[7]、S05[7]）的引导句只提问，不提示（S05[7] 的“记清楚一条边到底在等什么”不能说出 task 或任务）；答案段（S03[9]、S04[8]、S05[8]）先说“答案是 B”，再按英文顺序说每个错误选项。练习题 Q11–Q13 不出现在任何中文文件里。课件和 repo 不一致时，用一个分句客气地说（和课件有一处不同：……）。
- **[A10]** 名字。产品、公司和课程保留拉丁字母；“哈佛”只出现在标题和简介里。第 15 讲；课上；课件；示例 repo；课程团队（commit 作者）；Quiz 4 只在标题和简介里（旁白的 the quiz → 小测）；这期视频；考前版。不写也不念任何人名；不写项目 ID、项目编号、bucket 名、endpoint ID、W&B entity 或密钥。
- **[A11]** 画面保持英文：代码和 README 面板（包括注释）、示意图标注、标签（illustration、README example、slide 37、main today、kfp 2.14.6 · read, not run）、灰色课件标签、选择题卡片和红色理由行、黄色结论卡、S01 的 Nothing failed. / Nothing was right. 两行和七条规则都是英文，场景不需要改。旁白点名屏幕上的东西时照画面写；旁白自己的话说中文（灰色标签、右上角、绿色的勾、第一条泳道）。
- **[A12]** 只用大陆简体中文（默认、程序、代码、文件、目录、数据、函数、参数、调用、节点、依赖、并行、部署、计费、客户端），不用繁体和台湾用语（程式、檔案、資料、函式、呼叫、節點、相依性、平行處理、計費、用戶端）。
- **[A13]** 系列清单在这一期：pipeline（全片）、endpoint（S01、S06、S08）、container（S02[7]、S07[1]）、image 和 registry（S07[1]）、bucket（S06、S07）、repo、commit（S05[10]）、SDK；token 不用（线上的值说“值”）；prompt、volume、venv、PATH、agent、port、epoch、batch、loss 不在这份稿子里。封闭清单新增 DAG、task、component。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（凌晨 1 点、75 分钟、5 秒、224 乘 224、第 15 讲、一个 task、这里的 .output、model 目录、main 分支）。实物内部的空格照原样，不在实物里加空格。全角标点旁不加空格。不用 U+00A0 / U+202F。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，挨着实物也一样；列举用 、。不用任何括号。“”只用于中文里引用的想法；实物、标签名、README 原句和界面字样不加引号。一个中文句子（对应一个英文句子）中间没有 。？！，用 ，；：。选项字母后用全角冒号或逗号（C：.after 不需要数据。；答案是 B，16 分钟。）。
- **[B3]** 检查器拒收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后的 !、括号、letter_letter）不抄进中文行，用文字说：2 加 3 加 10 加 1；224 乘 224；sync 设为 True；.outputs 加上输出的名字；.after。可以保留：名字里的 . 和 -（raw.zip、.output、square-2、cheese-app-endpoint）、@、&（S05[1] 的“后台的 &”，检查器不拒收）。

### C. 数字与单位

- **[C1]** 屏幕上的数字和 SAY 里写成数字的，用阿拉伯数字：凌晨 1 点、2 点、3 点、75 分钟、40 分钟、16 分钟、5 秒、3、9（屏幕上的 9.0、16.0、25.0、5.0 旁白念 9、16、25、5）、2 加 3 加 10 加 1、224 乘 224、第 15 讲；退出码都是 0。SAY 用单词说的小数目用汉字：四个步骤、三个任务、两个训练、五步、四个分数、七条规则、两次。S08 的 One: … Seven: → 第一条：…… 第七条：。
- **[C2]** 不念版本号（kfp 2.14.6 只在紫色标签上）。时间：1 in the morning → 凌晨 1 点（不写 a.m.，也不写 1:00）；time zero → 0 时刻。不报金额（你要为这台机器付钱；机器一直在计费）。机器型号只在屏幕上。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐：script.md 的每条 SAY 在 narration/*.yaml 里有一条（76 段）；`en` 与 SAY 逐字节相同；`zh` 的条数等于 split_sentences 切出的英文句数（共 186 句：S01 23、S02 24、S03 28、S04 24、S05 34、S06 21、S07 17、S08 15）。只在句内调整，不合并、不拆分。短句单独成条：2 点训练。3 点部署。没有一个失败。还没有数字。执行的是 Vertex。不是一个数。来做一题。答案是 B。40 分钟。然后 75。它只是被拉长了。能调用它吗？还不能。七条规则。跑 `python -m explainer.i18n check videos/ac215-l15-exam --lang zh` 直到输出 OK。
- **[D2]** 没有 say:，没有 anchors:。字幕按英文音频计时，按位置配对。
- **[D3]** 显示行要过检查器：无括号、无数学符号、无 letter_letter、数字后无 !、不以“种”加标点收尾、中英之间有半角空格、句末是 。！？ 或 ……、每个拉丁词都在本词表里。检查器的切词：.output 算 output，@dsl.component 算 dsl.component，square-2 算 square-，raw.zip、cheese-app-endpoint 整体算一个，base64 算 base，AC215 算 AC；单个字母（选项 A–D、输入 a）忽略。
- **[D4]** 英文行（en_display）：SAY 把实物念成单词的句子写 en_display，用屏幕上的字面形式，其余与 SAY 一字不差；同段其他句子写 null。dot output → .output；dot outputs, with the output's name → .outputs["name"]；dot after → .after()；d s l dot component / pipeline → @dsl.component / @dsl.pipeline；the K F P library / K F P → the kfp library / kfp；the D S L → the DSL；dependent tasks → dependentTasks；square 2 → square-2；sync set to true → sync=True；bytes inputs → bytes_inputs；raw zip / clean zip → raw.zip / clean.zip；the model folder → the model/ folder；cheese app endpoint → cheese-app-endpoint；base 64 → base64；the Keras export archive → the Keras ExportArchive。可选（翻译时定，全片一致）：background ampersands → background & jobs。
- **[D5]** 内容对等：只译本句，不加命令、注释或解释；保留英文的词不加中文解释；思考题不给答案；结论卡照卡片说。A5 需要的“这里的、这些、这个、用、把”和答案字母前的“答案是”不算添加内容。
- **[D6]** 固定说法（与第 13 讲一致）：If the question says X, think Y. → 题目说 X，就想：Y。If an option … → 选项要是……，就想：……。think again → 再想想。Try one. → 来做一题。Your turn to compute one. → 轮到你算一题。One more, a subtle one. → 再来一题，有点绕。Pause here if you want. → 想停的话，就在这里暂停。B. → 答案是 B。B, 16 minutes. → 答案是 B，16 分钟。Now the contrast. → 再看对比。Here is the plan: … → 接下来的安排：……。Back to the toy graph. → 回到那个玩具图。Seven rules. → 七条规则。One: … → 第一条：……。Good luck on the quiz. → 祝你小测顺利。
- **[D7]** 文件：narration/g1.yaml = S01–S08（一个部分；76 段、186 句），开头写注释（覆盖范围和用到的规则），按稿子顺序；用双引号字符串，en_display 里的 .outputs[\"name\"] 要转义。
- **[D8]** 按英文时间轴读：每个中文句子大约在英文句子的时长内读完，最多约每个英文词 2 个单位（汉字 1，拉丁字母 0.55）；删多余的连接词和重复主语，不删内容。长名字（cheese-app-endpoint、Vertex AI Pipelines、Kubeflow Pipelines、@dsl.component）英文不重复的地方不重复，段内第二次用“这个 endpoint”“这个库”“它”。
- **[D9]** 保持英文的分句顺序：条件、目的、时间状语放在英文的位置（这个 repo 会复用 cheese-app-endpoint，如果它已经存在；不存在就新建一个；机器一直在计费，直到你取消部署；比较正好在慢的那个结束时开始；Cloud Run 适合模型只是一个更大应用的一部分的时候）。结论句两半按顺序（题目说……，就想：……）。

### G. 字幕

- **[G1]** 宽度：双语字幕带中文每行最多 30 个单位、英文 96 个字符；纯中文字幕（.zh.srt）每行 22 个单位、每条两行。分句最多约 24 个单位，用 ，；： 隔开；不写超过 30 个单位的无标点分句（S07[1] 和 S08[5] 两个最长的句子写成一串短分句）。
- **[G2]** 字幕条末尾的 。，、；： 会被去掉，？！…… 和后引号保留。句末用中文词收尾更稳（……然后是 model 目录。）。
- **[G3]** 不拆名字：中文行里拉丁词之间的空格会被当成切点，Vertex AI Pipelines、Kubeflow Pipelines、SageMaker Pipelines、Agent Platform、Model Registry、Artifact Registry、Docker Hub、Cloud Run、square root、bytes inputs 可能被拆到两行。把这些名字放在分句末尾或全角标点之后，渲染后逐条检查 .zh.srt。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）用书面语体（端点、有向无环图、模型注册表）；问句保留问号；保留英文的冒号结构；kfp 名和文件名照写（meta.yaml 不过检查器，可以用括号）。核心概念章节括注英文便于搜索：有向无环图（DAG）、最大安全重叠（maximum safe overlap）、端点（endpoint）。ML Workflows with Vertex AI → Vertex AI 上的机器学习工作流；exam edition → 考前版。比喻保留画面：凌晨两点的竞态；造出边的那根连线；靠边，不靠时钟；小测要记住的七条规则。
- **[H2]** 简介：两三句，书面语体，用本词表的说法：第 15 讲的考前版，写给 Quiz 4 前一天；讲什么（kfp 里 pipeline 是由 task 和数据边组成的 DAG；.output / .outputs 传递这次运行的值并造出边，写死的路径和 .after；最大安全重叠和最长路径；用边而不是 cron、后台命令或追踪工具里最好的模型来保证预处理 → 训练 → 部署；Model Registry → 端点 → 部署 → 预测，以及 ml-workflow 的 pipeline；SageMaker Pipelines 是同一个 DAG）；每个机制一张动画图，以 dlops-io 仓库的代码为依据，三道小测风格的选择题；英文旁白，配中文和中英双语字幕。不出现人名。
- **[H3]** 配套材料（i18n/zh/README.md，如果做）用书面语体翻译，末尾附术语对照表：English | 本片用法 | 其他常见译法（pipeline：pipeline / 流水线 / 管道；DAG：有向无环图；task：task / 任务；component：component / 组件；edge：边 / 依赖边；placeholder：占位符；join：汇合点 / 汇聚节点；maximum safe overlap：最大安全重叠 / 最大并行；longest path：最长路径 / 关键路径；race：竞态 / 竞争条件；stale data：过期数据 / 陈旧数据；endpoint：端点 / 终端节点；Model Registry：模型注册表 / 模型仓库；undeploy：取消部署 / 解除部署；signature：服务签名）。
- **[H4]** 配套材料里的代码和命令逐字节保留，只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读检查（_SPOKEN_BAD）。只有字幕的视频这些检查保护不了什么，反而逼出 A6 和 B3（这里：square_root、bytes_inputs、sync=True、.after()、.outputs["name"]）。建议：词表 voice 为 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当好切点，产品名可能被拆开（G3）。建议：中文行里只由空格隔开的一串拉丁词视为不可拆分，除非它本身超过一行。
- **[I3]**（说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：en 里 2–3 个词的英文说法保持在同一行，zh_subtitle 里 2–7 个汉字的中心词注册进 jieba，对所有视频生效。所以 en 和 zh_subtitle 只列真正的术语，不写句子。
