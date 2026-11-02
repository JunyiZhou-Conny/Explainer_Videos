# AC215 第 13 讲考前版中文字幕词表（中英混用版）

视频：*AC215 · Lecture 13 — Advanced Training Workflows (exam edition)*（`videos/ac215-l13-exam`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生，**Quiz 4 前一天**：听过第 13 讲，翻过 model-training 的 README，会用 Keras 的 `model.fit`，知道 epoch、batch 和 GCS bucket（第 10–11 讲）；不一定真的跑过 Vertex AI 任务，也不一定用两块 GPU 训练过。他们看这期视频是为了答概念性的选择题，并且能说出每个错误选项错在哪；不跟着敲命令。语体：中国 MLOps 助教考前一天的答疑串讲。
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l13-exam.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长，只保留显示规则。但没有 `say:` 时，`python -m explainer.i18n check` 仍会对显示行做朗读检查（括号、数学符号、带下划线的名字、词表里没有的拉丁词、缺少的半角空格）：规则 A6、B3、D3 就是为此而设。
英文原稿：`script.md` v2（SAY 行是旁白：73 段、176 句，只有一部分：S01 16 句、S02 25、S03 31、S04 25、S05 22、S06 22、S07 25、S08 10）；script.md 开头的 en_display 候选清单。课件：`videos/ac215-l13-training-workflows/SLIDES.md`（第 13 讲课件摘要）。代码：`assets/source/`（dlops-io/model-training @ b9aee1c，课上 Experiment Tracking notebook 的第 38 个单元格）。
先例：系列试点 [`ac215-l01-vms-venvs`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md)（repo、clone、commit、pin、lock 文件、笔记本、服务账号、密钥）；容器三讲 L02–L04（container、image、bucket、层、退出码，以及这份文件沿用的纯字幕规则）；[`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md)（权重、一个小疏漏）；[`ac215-l06-agents-1`](../../../ac215-l06-agents-1/i18n/zh/GLOSSARY.md)（notebook、SDK、区域）；[`ac215-l07-agent-harness`](../../../ac215-l07-agent-harness/i18n/zh/GLOSSARY.md)（diff、基线、课程团队，A1–I3 的规则编排）；最近完成的 [`ac215-l08-llm-finetuning`](../../../ac215-l08-llm-finetuning/i18n/zh/GLOSSARY.md)（epoch、batch、loss、梯度、优化器、学习率；job → 任务；D1–D9、G1–G3 的工具链规则）。第 1–8 讲定下的词一律沿用。
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）。

## 为什么要中英混用

- 中国的 MLOps 工程师和助教讲 W&B 和分布式训练时本来就中英混着说：“开一个 run”“这个 run 是活跃的”“加一个 callback”“用 logger 记指标”“config 里有学习率”“做一次 all-reduce”“每个 worker 读 TF config”“配一个 worker pool”。硬说“运行”“回调函数”“配置项”“全归约”，在答疑课上反而像说明书；“运行”还会和动词“跑 / 运行”撞车。
- 这是考前版：选择题的选项里写的是 `wandb.init`、`WandbMetricsLogger`、`MirroredStrategy`、`MultiWorkerMirroredStrategy`、`TF_CONFIG`、`dataset.batch`、`setup.py`、`ModuleNotFoundError`、`RUNNING`。这些名字一旦翻译，就和题目、和画面对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（实验追踪、可复现、依赖、模块、导入路径、策略、副本、梯度、分片、全局 batch、请求超时、服务器实例、无服务器训练、轮询）一律说中文，用 TensorFlow 和 Google Cloud 中文文档里能搜到的标准译名。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：代码面板、示意图标签、标签、选择题卡片和黄色结论行都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在考前一天答疑串讲时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“建一个 bucket”“跑 2 个 epoch”“batch 大小 4”“loss 降下来”“看 notebook”；这期再加上“开一个 run”“活跃的 run”“加一个 callback”“用 logger 记指标”“config 里”“做 all-reduce”“每个 worker”“一个 worker pool”。每个选择都要过三关：答疑课上真的这么说；是能搜到的中文标准译名；和系列保持一致（第 1–8 讲定下的 repo、bucket、image、container、notebook、epoch、batch、loss、权重、梯度、优化器、学习率、区域、密钥、笔记本 = laptop、任务 = job，一律沿用）。

1. **实物原样**：观众要在画面和选项里对照的东西（函数名和类名、文件名和目录名、命令、模块路径、报错、任务状态、config 的键）逐字照抄，不翻译、不变形、不加引号；检查器逼出来的例外是带下划线的名字和 = + < > | ( ) [ ] × 这些字符，按旁白的念法写（A6、B3）。
2. **答疑口语里的英文，封闭清单**：系列沿用的 repo、pin、lock 文件、container、image、bucket、ID、CLI、pipeline、notebook（第 1–6 讲）、epoch、batch（只指训练的 batch）、loss（第 8 讲）；**这期新增 run（W&B 的 run，只作名词）、callback、logger、config（run 的 config）、all-reduce、worker（TF config 里的一台机器）、worker pool**。
3. **其余一律用中文标准术语**：实验追踪、可复现、训练工作流、账本、一行、指针、活跃的 run、封存、历史记录、指标、系统图表、准确率、曲线、环境、代码、数据、产物、笔记、数据版本、快照、版本记录、内容哈希、密钥、命令行参数、包、tar 包、打包脚本、依赖、模块、导入路径、安装、预构建的训练 image、任务、训练任务、自定义任务、提交、轮询、状态、计费、机器、机器类型、区域、策略、副本、同步、梯度、平均、更新、分片、权重、优化器变量、全局 batch、每个副本的 batch、托盘、请求处理函数、请求超时、服务器线程、服务器实例、回收、代理、客户端超时、生命周期、无服务器训练、硬件、题目、选项、错误选项、答案、规则。
4. **视频的比喻按意思译，一个比喻一个词**：账本、一行、笔（callback）、指针（wandb.run）、挂锁 / 封存、购物清单（install_requires）、扫描（find_packages）、孤岛、连线、托盘和一份、旋钮、时钟（生命周期）、工单（任务）、引擎、杠杆。
5. **书面语体**（标题、meta.yaml、配套文档）：仓库、容器、镜像、存储桶、运行（run）、回调（callback）、配置（config）、轮次（epoch）、批次（batch）、全局批次、每副本批次、副本（replica）、训练任务、自定义训练任务（custom job）；类名和函数名照写。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **不出现任何人名**：旁白说 the lecture、the lecture's notebook → 课上、课上的 notebook（A10）。
8. **工具链的约束也是规则**：每个英文句子对应一个中文句子（73 段、176 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；口语轻松、讲得清楚，像考前答疑，但不用网络流行语。

## 关键决定

- **run 保留英文**（A1 c、A7）：W&B 的 run 是这期的核心名词，“运行”会和动词“跑 / 运行”撞车（“运行 python -m trainer.task”）。所以名词说 run（一个 run、活跃的 run、run 的记录），动词说“跑 / 运行”。书面写“运行（run）”。
- **active run → 活跃的 run**，全片一个说法，不写“当前运行”或“激活的 run”；the pointer called wandb.run → 叫 wandb.run 的指针。
- **callback、logger、config 保留英文**：类名就是 WandbCallback、WandbMetricsLogger，选项里写的是 config；书面写 回调（callback）、配置（config）。log（动词）→ 记录 / 写入；history entry → 一条历史记录 / 一条记录。
- **job → 任务**（沿用第 8 讲的“微调任务”）：训练任务、自定义任务（custom job）、持久的任务（durable job）、任务 ID；ticket 这个比喻 → 工单。Google Cloud 中文文档用“作业”，配套文档的对照表里注明（H3）。submit → **提交**；字幕里 commit 一直说英文，所以不冲突（A7）。
- **包、tar 包、package 目录分开**（A7）：Python package → 包（trainer 包）；tarball → tar 包；`package/` 这个目录 → package 目录。uploaded ≠ installed → 上传了 ≠ 安装了，这是 S04 的要点。install_requires 是“购物清单”，从 PyPI 下载（Python Package Index → PyPI，同一个名字，不算括注）。
- **类名照写**：MirroredStrategy、MultiWorkerMirroredStrategy、OneDeviceStrategy、WandbMetricsLogger、ModuleNotFoundError 没有下划线，检查器放行，中文行就写字面形式，方便和选项对照；英文行用 en_display 还原（D4）。
- **带下划线的名字按旁白念法**（A6）：install requires、find packages、init 文件、num replicas in sync、num workers、TF config、strategy.scope、wandb.run.finish。
- **副本、拷贝、分片、一份分开**（A7）：replica → 副本（每块 GPU 一个）；mirrored → 复制（不写“镜像”，书面的“镜像”留给 image）；shard（每台机器一份数据）→ 分片；slice（一个 batch 切给每个副本的那份）→ 一份。Vertex 的 replica count 数的是机器，num workers 数的是 GPU：每次都说清是哪一个（S05）。
- **全局 batch / 每个副本的 batch**：batch 沿用第 8 讲保留英文；书面写 全局批次 / 每副本批次。公式用文字说：32 乘 4 等于 128，除以同步的副本数（B3）。
- **任务状态照画面大写**：QUEUED、PENDING、RUNNING、SUCCEEDED（旁白念的是小写单词，英文行不改）。
- **考试的说法固定**（D6）：题目说 X，就想：Y；第一题 / 第二题 / 第三题；想停的话，就在这里暂停；答案是 C：……；A：……；错误选项。思考题那一段只问不答（A9）。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：调用和属性（wandb.init、wandb.run、wandb.run.finish、wandb.log、init、finish、log、fit、callbacks、strategy.scope、dataset.batch）、类名（WandbMetricsLogger、WandbCallback、MirroredStrategy、MultiWorkerMirroredStrategy、OneDeviceStrategy、ModuleNotFoundError）、文件和目录（setup.py、task.py、augment.py、package 目录、trainer 目录、init 文件、pyproject 文件）、模块和命令（trainer.task、python -m trainer.task、gcloud ai custom-jobs create、import augment、pip）、按旁白念法写的名字（install requires、find packages、num replicas in sync、num workers、TF config）、机型 n1-standard-32、任务状态（QUEUED、PENDING、RUNNING、SUCCEEDED）、指针的 None、包名（wandb、TensorFlow、scikit-learn、requests）。
- 产品、组织、课程和名字：AC215、Weights & Biases（第一次）和 W&B、Google、Vertex AI、Vertex、Keras、TensorFlow、Python、PyPI、Docker、GitHub、gcloud、GPU、CPU、T4（A1 b）。
- 答疑口语，封闭清单：repo、pin、lock 文件、container、image、bucket、ID、CLI、pipeline、notebook（第 1–6 讲）；epoch、batch、loss（第 8 讲）；**run、callback、logger、config、all-reduce、worker、worker pool（这期新增）**。
- 系列清单里保留英文、但这期没说到的：token、prompt、endpoint、volume、venv、PATH、port、agent、adapter、LoRA、Dockerfile、commit（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| run (W&B) / active run | run / 活跃的 run | training run / run record | 训练 run / run 的记录 |
| experiment tracking / tracker | 实验追踪 / 实验追踪工具 | reproducibility / accountability | 可复现 / 可追责 |
| ledger / row | 账本 / 一行 | pointer / points at | 指针 / 指向 |
| init / finish / seal | init / finish / 封存 | config / system charts | config / 系统图表 |
| callback / logger / pen | callback / logger / 笔 | log (verb) / history entry | 记录、写入 / 一条历史记录 |
| loss chart / accuracy / curves | loss 图 / 准确率 / 曲线 | deprecated / replacement | 已弃用 / 替代 |
| environment / artifacts / notes | 环境 / 产物 / 笔记 | data version / snapshot | 数据版本 / 快照 |
| version record / content hash | 版本记录 / 内容哈希 | key / flag | 密钥 / 命令行参数 |
| package / tarball | 包 / tar 包 | the package folder | package 目录 |
| install requires / shopping list | install requires / 购物清单 | find packages / init file | find packages / init 文件 |
| dependency / module | 依赖 / 模块 | import path / locally | 导入路径 / 本地 |
| prebuilt training image | 预构建的训练 image | Python Package Index | PyPI |
| job / custom job / durable job | 任务 / 自定义任务 / 持久的任务 | submit / poll / job id | 提交 / 轮询 / 任务 ID |
| ticket / states / billed | 工单 / 状态 / 计费 | serverless training | 无服务器训练 |
| strategy / replica / in sync | 策略 / 副本 / 同步 | mirrored / one copy per GPU | 复制 / 每块 GPU 一份 |
| gradient / averaged / update | 梯度 / 取平均 / 更新 | all-reduce | all-reduce |
| shard / slice | 分片 / 一份 | islands / wire | 孤岛 / 连线 |
| worker / worker pool | worker / worker pool | replica count / machine type | 副本数 / 机器类型 |
| global batch / per replica batch | 全局 batch / 每个副本的 batch | tray / dial | 托盘 / 旋钮 |
| request handler / request timeout | 请求处理函数 / 请求超时 | server thread / server instance | 服务器线程 / 服务器实例 |
| client timeout / proxies | 客户端超时 / 代理 | lifetime / clock / engine | 生命周期 / 时钟 / 引擎 |
| exam edition / quiz | 考前版 / 小测 | question / option / wrong option | 题目 / 选项 / 错误选项 |
| If the question says X, think Y | 题目说 X，就想：Y | Pause here if you want | 想停的话，就在这里暂停 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有“朗读（say:）”一栏。

### 开头：一个没有曲线的 run / The hook: a run with no curves

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| training run / run / the run exists / a run that finished without a single error | run / 训练 run | S01[0]：这是一个训练 run，跑完了，一个报错都没有。 | A1 c, new: run (the noun: a W&B run, one row of the ledger) stays English, because 运行 collides with the verb (A7): 一个 run, 这个 run, 新的 run, 两个 run, 活跃的 run, run 的记录. The verb run → 跑 / 运行 (跑完, 运行 python -m trainer.task). Written register 运行（run）(A4). |
| Weights and Biases / W and B / W&B / wandb / the wandb SDK | Weights & Biases / W&B / wandb | S01[0]：任务成功了，这个 run 也在 Weights & Biases 里。 | First use Weights & Biases, then W&B (the SAY's W and B; en_display W&B, D4). wandb is the package and SDK as on screen. W&B may open a sentence. |
| config / its config / system charts / CPU and memory | config / 系统图表 / 内存 | S01[0]：它的 config 在，系统图表也在。 | config (a run's config, wandb.config) stays (A1 c); config value → config 值. memory in the system charts is CPU memory → 内存 (A7). Written register 配置（config）. |
| loss chart / accuracy chart / curves / Where are the curves? | loss 图 / 准确率 / 曲线 | S01[1]：但是没有 loss 图，也没有准确率图。 | loss stays (L08); accuracy → 准确率; chart → 图; curves → 曲线 (Where are the curves? → 曲线去哪了？). Hold that thought; we come back to it in a few minutes → 先记着，过几分钟我们再回来 (D6). |
| the gray tag / the lecture slides / the lecture's roadmap / experiment tracking / baseline models / data collection | 灰色标签 / 课件 / 路线图 / 实验追踪 / 基线模型 / 数据收集 | S01[2]：角落里的灰色标签，标出每个想法背后的课件。 | A10: the lecture → 课上; the slides → 课件; the roadmap → 课上的路线图 (S01[2]: 在课上的路线图里，实验追踪很早就搭好，和基线模型一起，紧跟在数据收集之后). baseline → 基线 (L07). |
| exam edition / training workflow / quietly breaks / five places | 考前版 / 训练工作流 / 悄悄出错 | S01[3]：这是第 13 讲的考前版。 | exam edition → 考前版 (as follow-along → 跟练). The five places: run 的记录、包、GPU、batch，还有任务本身. |
| rule / if the question says this, think that / quiz-style question / pick an answer / wrong option | 规则 / 题目 / 小测 / 选项 / 错误选项 | S01[4]：每一部分都以一条规则收尾：题目说这个，就想那个。 | D6: the takeaway formula 题目说 X，就想：Y. quiz-style question → 小测风格的题; wrong option → 错误选项 (hear why each wrong option is wrong → 听听每个错误选项错在哪). |
| reproducibility / accountability / what produced this result / can I repeat it | 可复现 / 可追责 | S01[5]：题目说实验追踪，就想：这个结果是怎么来的，我能不能重复出来？ | The slide words Reproducibility / Accountability are on screen in English (A11) and not said. The lecture names the reason to track at all → 课上讲了为什么要追踪. |

### 一个 run 记录了什么 / What a run records

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| environment / code / data / model / metrics / artifacts / notes | 环境 / 代码 / 数据 / 模型 / 指标 / 产物 / 笔记 | S02[0]：课上列了七样：环境、代码、数据、模型、指标、产物，还有你的笔记。 | artifacts → 产物; notes → 笔记 (≠ 笔记本, the laptop, A7). What should a run record hold? → 一个 run 的记录该存些什么？ |
| GitHub / a versioning system / the pyproject file / the lock file / weights, metrics and logs | GitHub / 版本管理系统 / pyproject 文件 / lock 文件 / 权重 / 日志 | S02[1]：代码在 GitHub，数据在版本管理系统里，环境在 pyproject 文件和 lock 文件里。 | lock 文件 (L01); weights → 权重 (L05). get a question mark → 打了个问号. |
| data version / archived snapshot / version record / content hash / a fixed release of the data | 数据版本 / 快照 / 版本记录 / 内容哈希 / 固定版本 | S02[2]：数据版本是一对东西：bucket 里归档的快照，加上给它命名的版本记录，两者靠内容哈希连起来。 | The one-beat aside (Q1's concept, never its wording). bucket stays (series). This trainer instead downloads a fixed release of the data → 这个训练脚本下载的是一个固定版本的数据; never writes it into the config → 也从不写进 config. Rule six (S08[5]) uses the same words: 归档的快照，加上指向它的记录. |
| ledger / a ledger in which every training run is one row / row / recording by hand | 账本 / 一行 | S02[3]：想象一个账本，每个训练 run 是其中一行。 | V1's metaphor: ledger → 账本, row → 一行 / 这一行 / 第一行 / 第二行. Recording by hand gets forgotten → 手动记录总会忘. |
| the repo trainer / task.py / four calls / logs in / key / passed as a flag | 训练脚本 / task.py / 登录 / 密钥 / 命令行参数 | S02[4]：repo 里的训练脚本 task.py，用四个调用和这个账本打交道。 | key → 密钥 (L01); flag → 命令行参数; never written in the code → 从不写在代码里. No key value ever (A10). |
| wandb.init / init / opens a new row / project / name / a new init | wandb.init / init / 项目 / 名字 | S02[5]：调用 wandb.init 会开一个新行，带上项目、名字和 config：学习率、epoch 数、batch 大小和模型名。 | init / finish / log are the calls as the SAY says them (A1 a): 新的 init, 再 init 一次, 在 init 之后创建. en_display wandb dot init → wandb.init (D4). The four config keys are said in words and translated (学习率、epoch 数、batch 大小和模型名); the screen shows learning_rate, epochs, batch_size, model_name. |
| active run / the pointer called wandb.run / points at it / follows the pointer | 活跃的 run / 指针 / wandb.run | S02[5]：它还把这一行设成活跃的 run，叫 wandb.run 的指针现在就指向它。 | The quiz term: active run → 活跃的 run, always the same (never 当前运行 or 激活的 run). whichever row is active right now → 不管此刻哪一行是活跃的. |
| wandb.run.finish / finish / seals the row / sealed / falls back to nothing / None / execution time | wandb.run.finish / finish / 封存 / None / 执行时间 | S02[6]：然后 wandb.run.finish 把这一行封存，指针变回空。 | A6: wandb.run.finish() → wandb.run.finish (no brackets). sealed → 封存了 (padlock picture). the pointer falls back to nothing → 指针变回空; the slot None is on screen; the SAY says nothing → 空 (to nothing → 指向空). execution time → 执行时间 (execution_time on screen). |
| log the metrics / logs / logger / a logger writes the metrics / record of a run | logger / 记录 / 写入 | S02[8]：题目说 run 的记录，就想：init 开启它，logger 写入指标，finish 关闭它。 | A1 c, new: logger stays (the class is WandbMetricsLogger). log (verb) → 记录 / 写入 (Something still has to log the metrics → 还得有个东西来记录指标). The script avoids the verb records; recorded → 记录了. |
| First question / Pause here if you want / ruled out / with what you know already | 第一题 / 暂停 / 排除 | S02[9]：有三个选项，用你已经知道的就能排除。 | A9: the question block never answers; Which change puts a loss curve on it? → 改哪一处才能让它有 loss 曲线？ Pause here if you want → 想停的话，就在这里暂停 (D6). |

### callback 写进活跃的 run / The callback writes to the active run

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| callback / callbacks of fit / Wandb Metrics Logger / Wandb Callback / created after init | callback / callbacks / fit / WandbMetricsLogger / WandbCallback | S03[0]：答案是 C：在 fit 的 callbacks 里传入 WandbMetricsLogger，并且要在 init 之后创建。 | A1 c, new: callback stays (Keras callback; written 回调（callback）, A4). callbacks is fit's argument (artifact), so it may appear plural; a callback / two callbacks as nouns → 这个 callback / 两个 callback. Class names literal (no underscore; en_display not needed in the Chinese line, the English line gets WandbMetricsLogger / WandbCallback through en_display, D4). |
| a name only labels the row / one number in the config is not a history / logging in again writes no metrics | 标签 / 历史 | S03[0]：A：名字只是给这一行贴个标签。 | A9: wrong options with their letter, in the English order: B：config 里的一个数，不是跨 epoch 的历史。 D：重新登录不会写入任何指标。 |
| pen / a pen that Keras holds during training / at the end of every epoch / wandb.log | 笔 / Keras / epoch / wandb.log | S03[1]：这个 callback 就是训练时 Keras 握在手里的一支笔。 | V1's pen. whichever row is active right now, not the run the pen was created with → 不管此刻哪一行是活跃的，而不是创建这支笔时的那个 run. |
| the lecture's notebook / a callbacks list | notebook | S03[2]：课上的 notebook 正是这么做的。 | notebook stays (L06); the lecture's notebook → 课上的 notebook (A10). |
| history entry / one history entry per epoch / per batch / ticks / entries | 历史记录 / 记录 | S03[3]：默认情况下，每个 epoch 写一条历史记录。 | Per batch happens only if you ask → 每个 batch 记一条，只有你要求时才会. entries / ticks → 条 (六条记录, 第三到第六条, C1). |
| four experiments / no pen / the strip stays empty / our opening run | 实验 | S03[4]：现在做四个实验。 | First, no pen → 第一个，没有笔. That is our opening run → 这就是开头那个 run. |
| fit for two epochs / fit for four more / with no finish in between / the pointer never moved / one run, six entries | 六条记录 | S03[5]：一个 run，六条记录。 | C1: words in the SAY → Hanzi (两个 epoch, 四个 epoch, 第三到第六条). The pointer never moved → 指针从来没动过. |
| finish after the first fit / init again / the same callback / made during row one / the new row | 第一行 / 第二行 | S03[6]：这个 callback 是在第一行时创建的，但它跟着指针走，所以新的一行拿到第一到第四条。 | The first row is sealed with two entries → 第一行封存了，里面两条记录. |
| fit again without a new init / follows the pointer to nothing / you must call init before log / Nothing reaches any row | 报错 | S03[7]：第四个：先 finish，然后不重新 init 就再 fit 一次。 | A9: the error is translated as the SAY paraphrases it: 停下来报错：你必须先调用 init，再 log. Nothing reaches any row → 没有任何一行收到记录. The exact string is on screen with the wandb 0.15.11 chip. |
| creating the logger with no active run fails at once | 马上报错 | S03[8]：没有活跃的 run 时创建这个 logger，会马上报错。 |  |
| imports both callbacks but passes none to fit / the lecture's middle line / the line that is missing | 导入 / 缺的那一行 | S03[9]：课上那段代码中间的那一行，也就是 callback，正是缺的那一行。 | Now the hook → 回到开头 (D6). The repo trainer imports both callbacks but passes none to fit → repo 的训练脚本导入了两个 callback，却一个也没传给 fit. |
| deprecated / its replacement | 弃用 / 替代 | S03[10]：有个细节：这个 notebook 会提示 WandbCallback 已经弃用。 | For the curves, its replacement is the Wandb Metrics Logger → 要画曲线，它的替代是 WandbMetricsLogger. |
| counts history entries / whichever run is open when the epoch ends / a finish ends the count / a new init starts a new one | 计数 | S03[11]：题目问有几条历史记录，就想：每个 epoch 一条，写进 epoch 结束时开着的那个 run。 | D6 takeaway. Second sentence: finish 结束计数，新的 init 开始新的计数 must not open in lower case → 一次 finish 结束计数，一次新的 init 开始新的计数。 |

### 包里装了什么 / What the package carries

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| moves training to the cloud / a Python file with arguments / a package in a bucket / a training job on Vertex AI | Python 文件 / 包 / 训练任务 / Vertex AI | S04[0]：课上分三步把训练从本地搬到云上：一个带参数的 Python 文件、bucket 里的一个包，以及 Vertex AI 上的一个训练任务。 | job → 任务 (L08's 微调任务): 训练任务, 自定义任务 (custom job), 持久的任务 (durable job). Written register 训练任务, 自定义训练任务（custom job）(A4). arguments → 参数. |
| the package folder / setup.py / a trainer folder / an empty init file / the two training scripts | package 目录 / setup.py / trainer 目录 / init 文件 / 训练脚本 | S04[1]：这是 package 目录：setup.py，还有一个 trainer 目录，里面是一个空的 init 文件和两个训练脚本。 | A5 head nouns; A6: __init__.py → init 文件. en_display setup dot py → setup.py (D4). |
| install requires / shopping list / pip / Python Package Index / pinned wandb version | install requires / 购物清单 / pip / PyPI | S04[2]：其中 install requires 是一张购物清单，pip 从 PyPI 下载；这里只有一个 pin 了版本的 wandb。 | A6: install_requires → install requires (en_display restores). Python Package Index → PyPI (same name, D5). pin (L01) stays: pin 了版本的. Setup dot py keeps two lists → setup.py 里有两张清单. |
| find packages / which of your own folders get installed / only folders with an init file / scanner | find packages / 安装 / 扫描 | S04[2]：而 find packages 决定你自己的哪些目录会被安装：只有带 init 文件的目录。 | A6: find_packages() → find packages. find packages skips it → find packages 会跳过它 (not at sentence start, A5). |
| packaging script / tars / compresses / copies it into your bucket / job script / names the module / trainer.task | 打包脚本 / tar 包 / 压缩 / 模块 / trainer.task | S04[3]：打包脚本把 package 目录打成 tar 包，压缩，再复制到你的 bucket。 | tarball → tar 包; the job script points Vertex AI at that file and names the module: trainer dot task → 提交任务的脚本让 Vertex AI 指向这个文件，并给出模块名：trainer.task (G3: at the end, after a colon). |
| your own Docker image / packages, uploads and submits / never trains / prebuilt training image / tarball | Docker image / 预构建的训练 image / 上传 / 提交 | S04[4]：你自己的 Docker image 负责打包、上传和提交，但从不训练。 | image stays (A2); submit → 提交 (A7, ≠ commit); The job runs in Google's prebuilt training image, and your code reaches it only through the tarball → 任务跑在 Google 预构建的训练 image 里，你的代码只能通过 tar 包到那里. |
| TensorFlow / scikit-learn / requests / already ships | TensorFlow / scikit-learn / requests | S04[5]：这个 image 已经自带 TensorFlow、scikit-learn 和 requests，所以训练脚本照样能 import 它们，虽然 setup.py 从没写过。 | D9: although … stays after the main clause. Package names as on screen. |
| the job machine / unwraps the tarball / fetches / is installed / python -m trainer.task | 解开 / python -m trainer.task | S04[6]：在跑任务的机器上，pip 把 tar 包解开。 | Then Vertex runs python dash m trainer dot task → 然后 Vertex 运行：python -m trainer.task (G3; en_display D4). |
| a teammate's module / augment.py / a made-up example / beside the package folder / never leaves your laptop / travels / skips | 模块 / augment.py / 笔记本 | S04[7]：现在加一个队友写的模块 augment.py，一个编出来的例子，放在 package 目录旁边。 | laptop → 笔记本 (L01, A7). Placed next to setup.py instead, it travels, but find packages skips it → 要是放在 setup.py 旁边，它能跟着走，但 find packages 会跳过它. |
| import augment / import path / Module Not Found Error / every dependency installed / locally / the folder you ran from | import augment / 导入路径 / ModuleNotFoundError / 依赖 / 本地 | S04[8]：任务执行到 import augment；Python 在导入路径里找，什么也没找到。 | ModuleNotFoundError has no underscore: written literally in the Chinese line (the SAY says Module Not Found Error; en_display restores the English line, D4). right under the line that says every dependency installed → 就在那行“所有依赖都装好了”的正下方 is a quoted idea, fine in “”; Locally it worked → 在本地是能跑的. |
| the fix / put the file inside the trainer folder / list it in setup.py / a new import line alone moves nothing / the file has to travel | 修法 / 跟着走 | S04[9]：修法：把文件放进 trainer 目录，或者在 setup.py 里列出来。 | Second sentence: 光换一行 import，什么也搬不过去；文件本身得跟着走。 Never present the import change as the fix (script note). |
| adding it to install requires is wrong / downloads from the Python Package Index / someone else's code | 别人的代码 | S04[10]：把它加到 install requires 里是错的。 | a package there with that name would be someone else's code → PyPI 上要是有同名的包，那也是别人的代码. |
| dependencies installed but Module Not Found Error / never travelled inside the package that setup.py builds | 依赖 / 包 | S04[11]：题目说依赖都装好了却报 ModuleNotFoundError，就想：这个文件没有跟着 setup.py 打的包一起走。 |  |

### 一台机器还是多台 / One machine or many

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| training hardware / three shapes / One Device Strategy / Mirrored Strategy / Multi Worker Mirrored Strategy / strategy | 策略 / OneDeviceStrategy / MirroredStrategy / MultiWorkerMirroredStrategy | S05[0]：一台机器、多块 GPU，用 MirroredStrategy。 | Class names written literally in the Chinese line (no underscore, checker-clean; exam options use them); en_display restores the English line (D4). strategy → 策略 (tf.distribute 的策略). three shapes → 三种形态 inside a clause (D3: never 有三种。). |
| machine / one machine / n1-standard-32 / two T4 GPUs / replica count / the middle row | 机器 / n1-standard-32 / T4 / 副本数 | S05[1]：它的多 GPU 脚本向 Vertex AI 要一台机器，机型 n1-standard-32，带两块 T4 GPU。 | A replica count of one there means one machine → 那里的副本数为 1，意思是一台机器 (A7: Vertex's replica count counts machines). GPU measure word 块. |
| replica / replicas in sync / one per GPU / strategy.scope / mirrored / optimizer variable / one copy per GPU | 副本 / 同步 / strategy.scope / 优化器变量 / 复制 | S05[2]：训练脚本创建 MirroredStrategy，再问有多少个副本在同步：每块 GPU 一个，所以是两个。 | replica → 副本 (TensorFlow's Chinese docs). mirrored → 复制 (never 镜像, A2/A7): 在 strategy.scope 里构建并编译模型，所以每个权重和优化器变量都复制了，每块 GPU 一份. A6: strategy.scope() → strategy.scope. |
| one training step / its own slice of the batch / gradient / all-reduce / averaged / the same update | 训练步 / 一份 / 梯度 / all-reduce / 平均 / 更新 | S05[3]：这些梯度在 all-reduce 里汇合、取平均，同一份更新再发回两份拷贝。 | A1 c, new: all-reduce stays (全归约 is never said). gradient → 梯度 (L08). slice → 一份 (≠ 分片, A7). |
| shard / its own shard of the data / no wire / different weights / two separate models / islands | 分片 / 连线 / 独立的模型 / 孤岛 | S05[4]：几步之后，它们的权重就不一样了：是两个独立的模型，不是一个。 | Q4's concept, never its wording. Inside each machine the ring works, but between the machines there is no wire → 每台机器内部，环是通的，但机器之间没有连线. |
| TF config / the list of all the workers / its own index / worker / the wire | TF config / worker / 索引 | S05[5]：每台机器读取一份 TF config：所有 worker 的列表，以及它自己在列表里的索引。 | A6: TF_CONFIG → TF config (en_display restores). A1 c, new: worker stays (a machine in TF config; ≠ num workers, A7). To train one model across machines, use Multi Worker Mirrored Strategy → 要跨机器训练同一个模型，用 MultiWorkerMirroredStrategy (G1: the class name gets a clause of its own). |
| second worker pool / Vertex sets the TF config for you / naming trap / num workers / counts GPUs on one machine | worker pool / num workers / 命名陷阱 | S05[6]：还有一个命名陷阱：repo 和课上一样，把副本数叫作 num workers，但它数的是一台机器上的 GPU。 | A1 c, new: worker pool stays (Vertex's worker-pool-spec; written 工作器池（worker pool）). A6: num_workers → num workers. |
| several machines must train one model / never looks past its own machine | 跨机器 | S05[7]：MirroredStrategy 从不越过自己这台机器。 | First sentence: 题目说多台机器要训练同一个模型，就想 MultiWorkerMirroredStrategy 加 TF config。 |

### 全局 batch 与每个副本的 batch / Global batch, per-replica batch

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| global batch / per replica batch / dataset.batch / the whole tray for one step / equal slices | 全局 batch / 每个副本的 batch / dataset.batch / 托盘 | S06[0]：在策略下，dataset.batch 产出的就是全局 batch，也就是一步用的整个托盘。 | batch stays (L08, a training batch). global batch → 全局 batch; per replica batch → 每个副本的 batch; written register 全局批次 / 每副本批次 (A4). Now the batch → 再看 batch. |
| divided by / the number of replicas in sync / times the replicas | 除以 / 乘以 | S06[1]：所以每个副本的 batch 等于全局 batch 除以同步的副本数。 | B3: never ÷ × =. Turn it around → 反过来. |
| batch by 16 / each GPU gets only 2 / batch by 128 / each GPU gets 16 / 8 replicas | 分 batch | S06[2]：按 16 分 batch，每块 GPU 只拿到 2 个。 | C1 digits as the SAY. Take 8 replicas, and say you want 16 examples on each → 假设有 8 个副本，你想让每个副本拿到 16 个样本. Batch by 128. → 按 128 分 batch。 Each GPU gets 16. → 每块 GPU 拿到 16 个。 (separate sentences, D1). |
| the batch size flag / multiplies it by the replica count / the product / the data pipeline / batch expects the global batch size | batch 大小参数 / 乘积 / 数据 pipeline | S06[3]：它拿 batch 大小参数乘以副本数，再把乘积交给数据 pipeline。 | pipeline stays (series list). Its own comment says it → 它自己的注释就写着. |
| second question / global batch / what each GPU sees per step / 32 times 4 is 128 / split, not copied | 第二题 / 切分 | S06[5]：D：全局 batch 是被切分的，不是复制给每块 GPU。 | A9: S06[4] asks only. Answer: 答案是 B。 训练脚本先做乘法：32 乘 4 等于 128，策略把 128 分成四份，所以每块 GPU 看到 32 个。 A：那是一个从没做乘法的脚本。 C：这个参数是每个副本的大小，不是全局 batch。 |
| multiply before you batch | 先乘再分 | S06[6]：题目说每个副本，就先乘再分 batch：全局 batch 等于每个副本的 batch 乘以副本数。 |  |

### 比请求活得更久的训练 / Training that outlives the request

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| web app / retrain button / training takes an hour / Last mechanism | 网页应用 / 重新训练 | S07[0]：假设一个网页应用有个重新训练的按钮，训练要一个小时。 | Where should that hour run? → 这一个小时该在哪儿跑？ |
| piece of work / lives as long as the thing that holds it / request handler / request timeout | 请求处理函数 / 请求超时 / 生命周期 | S07[1]：放在请求处理函数里，它会在请求超时的时候死掉。 | Every piece of work lives as long as the thing that holds it → 每一份工作，都只能活到装着它的那个东西结束为止. D9 order kept. |
| server thread / server instance / the platform recycles it | 服务器线程 / 服务器实例 / 回收 | S07[2]：放在服务器线程里，它只能活到这个服务器实例结束，而平台想什么时候回收它就什么时候回收。 |  |
| client timeout / moves the wrong clock / proxies / a sleeping laptop | 客户端超时 / 时钟 / 代理 | S07[3]：把客户端超时调长，调的是错的那个时钟。 | The server and the proxies still cut the request, and a sleeping laptop loses the answer anyway → 服务器和代理照样会掐断请求，休眠的笔记本也照样收不到结果. |
| not a clock / logs runs / no engine to execute them | 引擎 / 执行 | S07[4]：而 W&B 根本不是时钟：它记录 run，但没有执行它们的引擎。 |  |
| durable job / submits / returns its id at once / states / queued / pending / running / succeeded / billed only while it runs / poll the id | 持久的任务 / 提交 / 任务 ID / 状态 / QUEUED / PENDING / RUNNING / SUCCEEDED / 计费 / 轮询 | S07[5]：正确的设计：处理函数提交一个持久的任务，马上返回它的 ID。 | States as the screen shows them, in capitals (A1 a, A11): 任务依次经过 QUEUED、PENDING、RUNNING、SUCCEEDED 这些状态，在自己的机器上跑，只在运行时计费. Anyone with access to the project can poll the id → 有项目访问权限的人都能轮询这个 ID. id → ID (series). |
| serverless training / hardware rented only for the training step / no server to manage / you just do not own its lifetime | 无服务器训练 / 租用 / 生命周期 | S07[6]：这就是课上讲的无服务器训练：硬件只为训练这一步租用，也没有服务器要管。 | There is still a machine; you just do not own its lifetime → 机器还是有的，只是它的生命周期不归你管. |
| the ticket / gcloud ai custom-jobs create / region / name / worker pool / machine type / replica count / prebuilt image / module | 工单 / gcloud ai custom-jobs create / 区域 / 机器类型 | S07[7]：在 repo 里，这张工单就是一条命令：gcloud ai custom-jobs create，再带上区域、名字和 bucket 里的包，以及一个 worker pool：机器类型、副本数、预构建的 image 和模块。 | G3: the command at a clause end after a colon. en_display gcloud AI custom jobs create → gcloud ai custom-jobs create (D4). region → 区域 (L06). |
| custom job / shows running / close the laptop for the night / third question | 自定义任务 / 第三题 | S07[8]：你的自定义任务显示 RUNNING，你合上笔记本过夜。 | A9: the question block never says where the job runs. The state as on screen: RUNNING. |
| keeps running on its own machine until it finishes or fails / the CLI container only submitted it / W&B only logs; it never drives training / nothing on your laptop holds the job's state | CLI / container / 状态 | S07[9]：A：CLI container 只负责提交。 | Answer first: 答案是 B：它在自己的机器上一直跑，直到完成或失败 (D9). C：W&B 只负责记录，从不驱动训练。 D：你笔记本上没有任何东西保存着任务的状态。 |
| training takes longer than the request / submit a durable job, return its id, and poll / W&B only watches | 轮询 | S07[10]：题目说训练要跑得比请求还久，就想：提交一个持久的任务，返回它的 ID，然后轮询。 | Second sentence: W&B 只是在旁边看着。 |

### 周二要记住的六条规则 / Six rules for Tuesday

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Six rules for Tuesday / Rule one / Rule six | 规则 / 第一条 / 周二 | S08[0]：周二要记住的六条规则。 | Rule one: … → 第一条：callback 每个 epoch 往活跃的 run 写一条记录；init 开启一个 run，finish 关闭它。 The rules say exactly what the takeaways said (D5). |
| separate strategies make separate models / split across the replicas in sync / a durable job with an id / an archived snapshot plus the record that points at it | 独立的策略 | S08[5]：第六条：数据版本，就是归档的快照，加上指向它的记录。 |  |
| three levers / more data / better models / faster hardware / the bookkeeping that shows whether it helped / Good luck on Tuesday | 杠杆 / 硬件 / 记账 | S08[6]：课上一开始讲了让深度学习变好的三个杠杆：更多数据、更好的模型、更快的硬件。 | Today was the hardware lever, plus the bookkeeping that shows whether it helped → 今天讲的是硬件这个杠杆，再加上能看出它有没有用的记账. Good luck on Tuesday. → 祝你周二考试顺利。 |

### 课程、名字与产品 / Course, names, products

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / Lecture 13 / the lecture / the lecture slides / Quiz 4 / Tuesday | AC215 / 课上 / 课件 / 周二 | S01[2]：在课上的路线图里，实验追踪很早就搭好，和基线模型一起，紧跟在数据收集之后。 | A10. Lecture 13 → 第 13 讲; Quiz 4 only in titles and descriptions. |
| products: Google / Vertex AI / Vertex / Keras / TensorFlow / Python / PyPI / Docker / GitHub / gcloud / GPU / CPU / T4 | Google / Vertex AI / Vertex / Keras / TensorFlow / Python / PyPI / Docker / GitHub / gcloud / GPU / CPU / T4 | S04[6]：然后 Vertex 运行：python -m trainer.task。 | Latin script (A1 b). GPU measure word 块 (两块 T4 GPU, 四块 GPU, 每块 GPU). |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上面词条里出现的拉丁词，字幕行里还可以出现这些（按检查器的切法写，D3）：AC、ai、AI、all-reduce、augment、augment.py、batch、Biases、bucket、callback、callbacks、CLI、config、container、CPU、create、custom-jobs、dataset.batch、Docker、epoch、finish、fit、find、gcloud、GitHub、Google、GPU、ID、image、import、in、init、install、Keras、lock、log、logger、loss、ModuleNotFoundError、MirroredStrategy、MultiWorkerMirroredStrategy、None、notebook、num、OneDeviceStrategy、package、packages、PENDING、pin、pip、pipeline、pool、pyproject、PyPI、python、Python、QUEUED、replicas、repo、requests、requires、run、RUNNING、scikit-learn、setup.py、standard-、strategy.scope、SUCCEEDED、sync、tar、task.py、TensorFlow、TF、trainer、trainer.task、Vertex、wandb、wandb.init、wandb.log、wandb.run、wandb.run.finish、WandbCallback、WandbMetricsLogger、Weights、worker、workers。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只留在三类地方。（a）**实物**，逐字照抄：调用和属性（wandb.init、wandb.run、wandb.run.finish、wandb.log、init、finish、log、fit、callbacks、strategy.scope、dataset.batch）、类名（WandbMetricsLogger、WandbCallback、MirroredStrategy、MultiWorkerMirroredStrategy、OneDeviceStrategy、ModuleNotFoundError）、文件和目录（setup.py、task.py、augment.py、package、trainer、init 文件、pyproject 文件）、模块和命令（trainer.task、python -m trainer.task、gcloud ai custom-jobs create、import augment、pip）、按旁白念法写的名字（A6）、机型 n1-standard-32、报错（ModuleNotFoundError；“必须先调用 init 再 log”按旁白的转述翻译，A9）、画面上的任务状态（QUEUED、PENDING、RUNNING、SUCCEEDED）、指针的 None、包名（wandb、TensorFlow、scikit-learn、requests）。（b）**产品、组织、课程和名字**：AC215、Weights & Biases（第一次）和 W&B、Google、Vertex AI、Vertex、Keras、TensorFlow、Python、PyPI、Docker、GitHub、gcloud、GPU、CPU、T4。（c）**中国 MLOps 工程师答疑时真的说英文的词，封闭清单**：系列沿用的 repo、pin、lock 文件、container、image、bucket、ID、CLI、pipeline、notebook（第 1–6 讲），epoch、batch（只指训练的 batch）、loss（第 8 讲）；这期新增 run（W&B 的 run，只作名词）、callback、logger、config（run 的 config）、all-reduce、worker（TF config 里的一台机器）、worker pool（Vertex AI 配置里的词）。只有答疑口语真的用英文、而中文生硬或和别的词撞车时，一个词才能进（c）（run：“运行”和动词撞车；config：画面和选项都写 config；all-reduce：没人说“全归约”）。不为“味道”用英文：实验追踪、可复现、账本、一行、指针、历史记录、指标、系统图表、曲线、准确率、环境、数据版本、快照、内容哈希、密钥、命令行参数、包、tar 包、依赖、模块、导入路径、安装、预构建的训练 image、任务、提交、轮询、状态、策略、副本、梯度、分片、权重、全局 batch、请求处理函数、请求超时、服务器实例、无服务器训练、题目、选项、答案、规则，都说中文（A3）。
- **[A2]** container 和 image（同第 2–8 讲）。字幕说 container、image：你自己的 Docker image、预构建的训练 image、CLI container；量词“个”。标题、章节名、meta.yaml 和配套文档写 容器、镜像（A4）。tf.distribute 的 mirrored 在字幕里**绝不写“镜像”**（A7），说“复制”（每块 GPU 上复制一份），类名 MirroredStrategy 照写。
- **[A3]** 这期新增的词汇。**实验追踪**：experiment tracking → 实验追踪，track → 追踪，tracker → 实验追踪工具（不是第 8 讲画面上的“进度条”），run → run，training run → 训练 run，run record → run 的记录，ledger → 账本，row → 一行 / 第一行 / 第二行，active run → 活跃的 run，pointer → 指针，points at → 指向，falls back to nothing → 变回空，open → 开 / 开启，closes → 关闭，seal → 封存，config → config，system charts → 系统图表，CPU and memory → CPU 和内存，loss chart → loss 图，accuracy → 准确率，curves → 曲线，metrics → 指标，log（动词）→ 记录 / 写入，logger → logger，callback → callback，pen → 笔，history entry → 一条历史记录 / 一条记录（ticks → 条），deprecated → 已弃用，replacement → 替代。**run 的记录**：environment → 环境，code → 代码，data → 数据，model → 模型，artifacts → 产物，notes → 笔记，versioning system → 版本管理系统，data version → 数据版本，archived snapshot → 归档的快照，version record → 版本记录，content hash → 内容哈希，a fixed release → 一个固定版本。**打包**：package → 包，package 目录，trainer 目录 / trainer 包，init 文件，两张清单，install requires，shopping list → 购物清单，Python Package Index → PyPI，pinned → pin 了版本的，find packages，scanner → 扫描，tar → 打包，tarball → tar 包，compress → 压缩，packaging script → 打包脚本，job script → 提交任务的脚本，module → 模块，teammate's module → 队友写的模块，made-up example → 编的例子，import path → 导入路径，dependency → 依赖，install → 安装，travel → 跟着走，prebuilt training image → 预构建的训练 image，job machine → 跑任务的机器，unwrap → 解开。**tf.distribute**：strategy → 策略，machine → 机器，GPU 量词“块”，replica → 副本，in sync → 同步，mirrored → 复制，optimizer variable → 优化器变量，training step → 训练步 / 一步，slice → 一份，gradient → 梯度，averaged → 取平均，all-reduce，shard → 分片，separate models → 独立的模型，wire → 连线，islands → 孤岛，worker，index → 索引，worker pool，naming trap → 命名陷阱。**batch**：global batch → 全局 batch，per replica batch → 每个副本的 batch，tray → 托盘，dial → 旋钮，batch by n → 按 n 分 batch，divided by → 除以，times → 乘以，the batch size flag → batch 大小参数，data pipeline → 数据 pipeline。**任务**：web app → 网页应用，request handler → 请求处理函数，request timeout → 请求超时，server thread → 服务器线程，server instance → 服务器实例，recycles → 回收，proxies → 代理，client timeout → 客户端超时，clock → 时钟，lifetime → 生命周期，engine → 引擎，durable job → 持久的任务，custom job → 自定义任务，submit → 提交，job id → 任务 ID，poll → 轮询，states → 状态，billed → 计费，serverless training → 无服务器训练，rented → 租用，ticket → 工单，region → 区域，machine type → 机器类型，replica count → 副本数。**考试**：exam edition → 考前版，quiz → 小测，question → 题目 / 题，option → 选项，wrong option → 错误选项，answer → 答案，rule → 规则 / 第 n 条，ruled out → 排除。
- **[A4]** 字幕与书面。字幕说 repo / container / image / bucket / notebook / run / callback / config / epoch / batch / loss / worker pool；标题、章节名、meta.yaml 和配套文档写 仓库 / 容器 / 镜像 / 存储桶 / Colab 笔记本（notebook）/ 运行（run）/ 回调（callback）/ 配置（config）/ 轮次（epoch）/ 批次（batch）/ 损失（loss）/ 工作器池（worker pool），核心概念第一次出现时括注英文（字幕之外可以用括号）；global / per-replica batch 写 全局批次 / 每副本批次；Vertex AI 的 job 写 训练任务、自定义训练任务（custom job）（Google Cloud 中文文档说“作业”；系列从第 8 讲起说“任务”）。W&B、Weights & Biases、Vertex AI、类名、函数名和 setup.py 书面也照写。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符都不改）；不翻译、不变形、不加引号、不加《》或代码格式。需要时加中文中心词：package 目录、trainer 目录、trainer 包、init 文件、pyproject 文件、lock 文件、训练脚本 task.py、模块 augment.py、n1-standard-32 机器。句子不以实物或小写的英文词开头，先放一个中文词（这个 callback……；而 find packages……；其中 install requires……；调用 wandb.init……；这个 run……），所以字幕不会以小写开头。大写的名字、缩写、类名和选项字母（W&B、Weights & Biases、Vertex AI、Keras、Python、Google、GitHub、MirroredStrategy、ModuleNotFoundError、A：、B：）可以放句首。
- **[A6]** 带下划线的名字和代码表达式（同第 3–8 讲）。没有 say: 时，检查器把显示行当朗读文本，拒收 letter_letter、括号、< > | 和 =；SAY 本身也不念下划线。所以中文行按旁白的说法写：install_requires → install requires；find_packages() → find packages；__init__.py → init 文件；num_replicas_in_sync → num replicas in sync（旁白说 the number of replicas in sync 时写“同步的副本数”）；num_workers → num workers；TF_CONFIG → TF config；strategy.scope() → strategy.scope；wandb.run.finish() → wandb.run.finish；WandbMetricsLogger() → WandbMetricsLogger；x × y → x 乘 y。类名和带点的名字没有下划线，照字面写（MirroredStrategy、wandb.init、dataset.batch）。英文行用 en_display 写字面形式（D4）。
- **[A7]** 要分开的词。run（名词：W&B 的 run，账本的一行）≠ 跑 / 运行（动词：跑完，运行 python -m trainer.task）≠ 训练。记录（log；一条记录）≠ 版本记录（数据版本的记录）≠ 账本（ledger）≠ run 的记录（一个 run 存的东西）。活跃的 run（wandb.run）≠ 当前这一行（只说画面）。任务（Vertex AI 的 job：训练任务、自定义任务、持久的任务）≠ 工单（ticket 这个比喻）≠ 进程 / 线程。提交（submit）≠ commit（第 1 讲，保留英文）≠ 上传（upload）。包（Python 包：trainer 包；tar 包）≠ package 目录（`package/`）≠ bucket。安装（pip install）≠ 上传（tar 包上传）≠ 跟着走（travel）：上传了 ≠ 安装了，是 S04 的要点。依赖（从 PyPI 来的）≠ 模块（你自己的 .py 文件）。副本（tf.distribute 的 replica，每块 GPU 一个）≠ 拷贝 / 一份（权重的一份拷贝，batch 的一份）≠ 副本数（Vertex 的 REPLICA_COUNT 数机器，num workers 数 GPU；每次说清是哪个，S05）。worker（TF config 里的一台机器）≠ num workers（一台机器上的 GPU 数）≠ worker pool（Vertex 的一组机器）。机器（VM）≠ 服务器（S07 的 web 服务器）。分片（每台机器的一份数据）≠ 一份（一个 batch 切给每个副本的那份）。image（字幕）≠ 镜像（书面的 image）≠ 复制（mirrored，A2）。笔记本（laptop）≠ notebook（课上的 notebook）≠ 笔记（notes，run 记录的一项）。内存（系统图表里的 CPU 内存）≠ 显存（这期不出现）。题目 / 题（小测的题）≠ 问题（一般的问题；Hold that thought → 先记着）。课上 ≠ 课件 ≠ 课上的 notebook。时钟（生命周期，S07）≠ 超时。区域（region）≠ 位置。
- **[A8]** 语体：考前一天的答疑串讲。短句、讲清楚，用口语动词（开、关、写、记、传、打包、交、切、乘、分）；观众是“你”（不用“您”“大家”“同学们”）；“我们”指这期视频（我们过几分钟再回来）。分句内部用中文语序；分句之间的顺序跟英文（D9）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”（主语清楚时说“封存”，不说“被封存”），不叠“一个……的”。不用网络流行语。口语节奏按意思译：Now the batch. → 再看 batch。；Now the hook. → 回到开头。；Last mechanism. → 最后一个机制。；One run, six entries. → 一个 run，六条记录。；Batch by 128. → 按 128 分 batch。；Each GPU gets 16. → 每块 GPU 拿到 16 个。；Here is the key fact. → 关键在这里。；One word on data. → 关于数据，说一句。
- **[A9]** 精确。量词要译出来：only 只，every 每个 / 每次，all 全部，at once 马上 / 立刻，never 从不，exactly 正是，whichever 不管哪个。考点按英文说的原样说，不打折扣（one per epoch → 每个 epoch 一条，不说“大约”；a callback with no active run fails at once → 马上就报错），也不加英文没说的事实。旁白转述的报错（you must call init before log）按转述翻译（你必须先调用 init，再 log）；带 wandb 0.15.11 标签的原文在画面上，保持英文。思考题三道（S02[9]、S06[4]、S07[8]）；思考题卡片下面那段只问不答，也不暗示：S02[9] 不提 logger 或 callbacks（Three options can be ruled out with what you know already → 有三个选项，用你已经知道的就能排除）；S06[4] 不做乘法；S07[8] 不说任务在哪儿跑。答案段（S03[0]、S06[5]、S07[9]）先给字母（答案是 C：……），再按英文的顺序逐个说错误选项（A：……）。
- **[A10]** 名字。产品、公司和课程保持拉丁字母（A1 b）；“哈佛”只用在标题和简介里。课程：AC215；Lecture 13 → 第 13 讲；the lecture → 课上；the lecture slides → 课件；the lecture's notebook → 课上的 notebook；the lecture's roadmap → 课上的路线图；Quiz 4 只在标题和简介里写（旁白说 Tuesday → 周二）；this video → 这期视频；exam edition → 考前版。不写、不念任何人名（这份脚本里授课老师不出名字）；不出现 W&B 密钥、项目 ID、entity 或任务 ID：任务 ID 只在画面上以 ‹job-id› 出现。W&B 项目 cheese-training-vertex-ai 和 run 名在画面上，旁白不念。
- **[A11]** 画面保持英文。这个系列只翻译旁白：代码面板（含注释）、示意图标签、chip、灰色的课件标签（Lecture 13 · slides a–b）、各种标签（illustration、concept · lecture only、example · not in the repo、wandb 0.15.11）、选择题卡片和红色理由、黄色结论行、回顾里的规则都是英文，场景不需要为中文改动。旁白提到画面上的东西时，字幕照画面写（None、RUNNING、n1-standard-32）；旁白自己的话就翻译（the gray tag → 灰色标签，the pen → 笔，the pointer → 指针，the tray → 托盘）。
- **[A12]** 只用大陆简体：默认、程序、代码、文件、目录、数据、数据集、网络、脚本、视频、信息、账号、函数、参数、内存、优化器、线程、实例、进程；不用繁体或台湾用语（預設、程式、程式碼、檔案、資料夾、資料、網路、腳本、影片、帳號、函式、引數、記憶體、最佳化器、執行緒、執行個體）。
- **[A13]** 系列清单（ac215-video 技能里的清单）在这期的情况。repo（S02、S05、S07）、bucket（S02、S04、S07）、image（S04、S07）、container（S07[9]）、notebook（S03）、ID（S07）、CLI（S07[9]）、pipeline（S06[3]，数据 pipeline）、pin（S04[2]）、lock 文件（S02[1]）；token、prompt、endpoint、volume、venv、PATH、port、agent、adapter、LoRA、Dockerfile 和 commit 这份脚本里没有。不在系列清单里、这里保留的（A1 c，新增）：run、callback、logger、config、all-reduce、worker、worker pool；epoch、batch、loss 同第 8 讲。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（开一个 run、第 13 讲、两块 T4 GPU、8 个副本、按 128 分 batch、package 目录、init 文件、32 乘 4 等于 128）。检查器对每个显示句都会报缺少的空格。实物内部的空格照原样（python -m trainer.task、gcloud ai custom-jobs create、import augment），不在实物里加空格。全角标点两边不加空格（……trainer.task。；W&B，……）。不用 U+00A0 / U+202F。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，实物旁边也一样。并列用 、（TensorFlow、scikit-learn 和 requests；环境、代码、数据；QUEUED、PENDING、RUNNING、SUCCEEDED）。不用任何括号：（）、()、《》、【】、[]、<>（没有 say: 时检查器拒收）。“”只用于想法或旁白当作词语引用的说法（题目说“这个”，就想“那个”）；实物、类名、状态和报错名不加引号。一个中文句子（对应一个英文句子）中间不出现 。？！：用 ，；：。选项字母后用全角冒号（A：名字只是给这一行贴个标签。；答案是 C：……）。结论句保留冒号：题目说 X，就想：Y。
- **[B3]** 检查器拒收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后的 !、括号、letter_letter）：不抄进中文行，用文字说（A6）。32 times 4 is 128 → 32 乘 4 等于 128；divided by → 除以；global = per-replica × replicas → 全局 batch 等于每个副本的 batch 乘以副本数。可以照画面保留的：名字里的 . 和 /（setup.py、wandb.run.finish、trainer.task、dataset.batch、strategy.scope）、命令和名字里的 -（python -m、custom-jobs、n1-standard-32、scikit-learn、all-reduce）、W&B 和 Weights & Biases 里的 &。

### C. 数字、版本号与单位

- **[C1]** 显示文字里的数字。和画面、代码对应的数字，以及 SAY 里写成阿拉伯数字的，一律用阿拉伯数字、不加千位分隔符：第 13 讲、8 个副本、16 个、2 个、128、4 块 GPU、32。SAY 用英文单词说的小数目用汉字：七样、四个调用、五个地方、三步、两张清单、两块 T4、两份、两台机器、三种形态、四个实验、两个 epoch、四个 epoch、六条记录、第三到第六条、第一到第四条、三个选项、三次、六条规则、一个小时、三个杠杆；规则和行：第一条……第六条、第一行、第二行。选项字母 A–D 保持拉丁字母（答案是 B）。
- **[C2]** 单位、版本、名字和日子。不念任何版本号（wandb 0.15.11 只在紫色标签上）。日子：Tuesday → 周二（Six rules for Tuesday → 周二要记住的六条规则；Good luck on Tuesday → 祝你周二考试顺利）。时间：an hour → 一个小时；a few minutes → 几分钟。机型照画面写 n1-standard-32（旁白念 n1 standard 32，英文行用 en_display 还原）。不出现金额（billed only while it runs → 只在运行时计费）。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每一行 SAY 对应一条（73 段）；`en` 和 SAY 行逐字节相同；`zh` 的条数等于 explainer.voice.split_sentences 切出的英文句子数（这份脚本 176 句：S01 16、S02 25、S03 31、S04 25、S05 22、S06 22、S07 25、S08 10）。只在句子内部调整结构，不合并、不拆分句子。短句单独成条：First question. → 第一题。；Now the batch. → 再看 batch。；Now the hook. → 回到开头。；Batch by 128. → 按 128 分 batch。；Each GPU gets 16. → 每块 GPU 拿到 16 个。；Where are the curves? → 曲线去哪了？；One run, six entries. → 一个 run，六条记录。 反复运行 `python -m explainer.i18n check videos/ac215-l13-exam --lang zh`，直到输出 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：不写 say:，也不写 anchors:。字幕按英文音频计时，工具按位置把每个中文句子和对应的英文句子配对（S08 的 vo.wait_until("Rule one") 只对英文生效）。
- **[D3]** 显示行要过检查器。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：没有括号（B2）、没有数学符号（B3）、没有 letter_letter 名字（A6）、数字后没有 !、没有以“种”结尾再接 ，。！？ 的分句、汉字和拉丁字母或数字之间有半角空格（B1）、每句以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用 [A-Za-z][A-Za-z'.-]* 切词，忽略单个字母：W&B 切成 W 和 B（忽略），T4 是 T（忽略），python -m 是 python 和 m，n1-standard-32 是 n 和 standard-，wandb.run.finish、trainer.task、dataset.batch、strategy.scope、scikit-learn、all-reduce、custom-jobs 保持整体。检查器报出来的拉丁词，要么是该翻译的英文词（多数情况），要么是漏列的实物：按同样的切法把实物加进 allowed_spoken_latin 和对应词条。复数故意不列（runs、作名词的 callbacks、epochs、GPUs、作名词的 workers 都没有）：报出复数，就是要去掉的英文词形变化（两个 run、两个 epoch、四块 GPU、所有 worker）；只有 fit 的参数 callbacks 和名字 num workers 是复数形式的实物。
- **[D4]** 英文行（en_display）。双语字幕带显示 SAY 句子，而 SAY 为了配音把实物念成单词。每个这样的句子都写一条 en_display，用画面上的字面形式，其余部分和 SAY 逐词相同；同一段里其他句子写 null。念法 → 字面（script.md 开头的清单加上这份词表补充的）：wandb dot init → wandb.init；wandb dot run → wandb.run；wandb dot run dot finish → wandb.run.finish()；wandb dot log → wandb.log；Wandb Metrics Logger → WandbMetricsLogger；Wandb Callback → WandbCallback；setup dot py → setup.py；task dot py → task.py；augment dot py → augment.py；install requires → install_requires；find packages → find_packages()；python dash m trainer dot task → python -m trainer.task；trainer dot task → trainer.task；Module Not Found Error → ModuleNotFoundError；One Device Strategy → OneDeviceStrategy；Mirrored Strategy → MirroredStrategy；Multi Worker Mirrored Strategy → MultiWorkerMirroredStrategy；TF config → TF_CONFIG；num replicas in sync → num_replicas_in_sync；num workers → num_workers；strategy dot scope → strategy.scope()；dataset dot batch → dataset.batch；gcloud AI custom jobs create → gcloud ai custom-jobs create；n1 standard 32 → n1-standard-32；W and B → W&B；Weights and Biases → Weights & Biases。带下划线的名字（A6）只在 en_display 里还原成字面形式，中文行保持空格分开的写法。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只翻译它对应的英文句子：不加命令、参数、括注、中文的画面名称或解释；保留英文的词不加中文解释（英文行就在下面）；思考题不给答案（A9）；结论句只说黄色结论行说的。A5 需要的几个开头词（这个、其中、而、调用）不带内容。Python Package Index → PyPI 是同一个名字，不算括注。
- **[D6]** 固定说法。If the question says X, think Y. → 题目说 X，就想：Y。（每个结论句；S01[4] 的 if the question says this, think that → 题目说这个，就想那个）。First / Second / Third question. → 第一题。/ 第二题。/ 第三题。 Pause here if you want. → 想停的话，就在这里暂停。 The answer is C: … → 答案是 C：…… A: … → A：…… Hold that thought; we come back to it in a few minutes. → 先记着，过几分钟我们再回来。 Here is the key fact. → 关键在这里。 Now four experiments. → 现在做四个实验。 First, … / Second: … / Third: … / Fourth: … → 第一个，……/ 第二个：……/ 第三个：……/ 第四个：…… One detail: … → 有个细节：…… One naming trap: … → 还有一个命名陷阱：…… One word on data. → 关于数据，说一句。 The fix: … → 修法：…… Last mechanism. → 最后一个机制。 The right design: … → 正确的设计：…… Rule one: … → 第一条：…… Six rules for Tuesday. → 周二要记住的六条规则。 Good luck on Tuesday. → 祝你周二考试顺利。
- **[D7]** 文件。narration/g1.yaml = S01–S08（只有一部分；73 段、176 句），对应 video.yaml 唯一的一部分；文件开头写注释（覆盖范围；用到的规则：A6 空格分开的名字、B3 符号写成文字、C1 数字、D4 en_display、D6 固定说法、没有 say: / anchors:），按脚本顺序排列。用双引号字符串；YAML 里的双引号和反斜杠要转义。
- **[D8]** 按英文时间轴的长度。中文在英文播放时读；字幕带在英文换句的地方切换（读起来超过每秒 9 个单位的中文片段最多多给 1 秒）。每个中文句子应该在听英文句子的时间里读完：每个英文词最多约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以删去多余的连接词和重复的主语，但不删内容。长的实物也占长度（MultiWorkerMirroredStrategy 14.9 个单位，gcloud ai custom-jobs create 14.3，WandbMetricsLogger 9.9，ModuleNotFoundError 10.5）：英文没重复的地方中文不重复；同一段里第二次提到时用简称（这个策略、这条命令、这个 logger、这个报错）。
- **[D9]** 保持英文的分句顺序（系列经验，见 ac215-video 技能）。工具按分句把中英文配对，中文要是把英文放在后面的条件提到前面，相邻两条字幕的意思就对调了。条件、目的和时间状语放在英文放的位置：the trainer imports them although setup.py never names them → 训练脚本照样能 import 它们，虽然 setup.py 从没写过；Inside the request handler, it dies at the request timeout → 放在请求处理函数里，它会在请求超时的时候死掉；it keeps running on its own machine until it finishes or fails → 它在自己的机器上一直跑，直到完成或失败。结论句保持英文的顺序（题目说……，就想……）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文行最多 30 个单位，英文行 96 个字符；纯中文字幕（.zh.srt）每行 22 个单位，每条两行。分句写成最多约 24 个单位，用 ，；： 隔开，给切分器留干净的切点；不要有超过 30 个单位、中间没有标点的分句（MultiWorkerMirroredStrategy 和 gcloud ai custom-jobs create 单独成一个分句）。
- **[G2]** 字幕结尾：工具会去掉每条字幕末尾的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。句末能用中文词的地方，优先用中文词收尾，而不是“实物 + 句号”（……放进 trainer 目录。比……放进 trainer。读起来稳；两种都合法）。
- **[G3]** 不拆命令和长类名。切分器把中文行里两个拉丁词之间的空格当作好切点，所以 python -m trainer.task 或 gcloud ai custom-jobs create 可能被拆到两行。把整条命令放在分句末尾、全角冒号之后（然后 Vertex 运行：python -m trainer.task。；就是一条命令：gcloud ai custom-jobs create，……），每条字幕最多一条命令，周围少放中文。在渲染出来的 .zh.srt 里检查每条带命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频标题和章节名用书面语体（A4：运行、回调、镜像、批次、训练任务）；问句保留问号；保留英文的冒号结构；类名、函数名和文件名照写（检查器不读 meta.yaml，所以那里可以用括号）。核心概念的章节在中文不是常用搜索词时带上英文短名，方便搜索（运行（run）、回调（callback）、全局批次（global batch）），和第 1、3、5–8 讲一样。Advanced Training Workflows → 进阶训练工作流；exam edition → 考前版（跟练 = follow-along）。比喻保留画面（the run with no curves → 没有曲线的运行；training that outlives the request → 比请求活得更久的训练；six rules for Tuesday → 周二要记住的六条规则）。
- **[H2]** 简介（Bilibili / YouTube）：两三句，书面语体，用这份词表的词：AC215 第 13 讲的考前版，写给 Quiz 4 前一天；讲什么（W&B 的运行，init / finish，以及每个轮次往活跃的运行写一条历史记录的回调；打包 Vertex AI 自定义训练任务，以及为什么依赖都装好了还报 ModuleNotFoundError；MirroredStrategy 和 MultiWorkerMirroredStrategy、TF_CONFIG；全局批次和每副本批次；把长时间的训练提交成持久的任务；顺带讲一句数据版本）；每个机制都是一张动画图，配 dlops-io/model-training 的代码作为依据，片中有三道小测风格的题；英文旁白，配中文和中英双语字幕。不写任何人名。
- **[H3]** 配套材料：i18n/zh/README.md（如果做）用这份词表、按书面语体（A4）翻译。最后附术语表：English | 这里的用词 | 其他常见译法（run：run / 运行；callback：callback / 回调；active run：活跃的 run / 当前运行；experiment tracking：实验追踪 / 实验跟踪；replica：副本；global batch：全局 batch / 全局批次；all-reduce：all-reduce / 全归约；shard：分片；custom job：自定义任务 / 自定义作业；serverless：无服务器；poll：轮询；import path：导入路径 / 模块搜索路径）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 不改，只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读文本的检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）。对只有字幕的视频（这里 voice: none），这些检查保护不了什么，却逼出了 A6 和 B3（这里是 install_requires、find_packages()、__init__.py、num_replicas_in_sync、num_workers、TF_CONFIG、strategy.scope()、×）。建议：词表的 voice 是 none 时，只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当作好切点，所以命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
- **[I3]**（说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：每个词条 en 字段里 2–3 个词的英文说法会保持在同一行英文里，zh_subtitle 里 2–7 个汉字的中心词会注册进 jieba，对所有视频的字幕都生效。所以这份文件的 en 和 zh_subtitle 只列真正的术语（不放句子）。
