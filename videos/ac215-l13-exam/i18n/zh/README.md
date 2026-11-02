# 中文字幕说明

视频 *AC215 · Lecture 13 — Advanced Training Workflows (exam edition)*
（**AC215 · 第 13 讲：进阶训练工作流（考前版）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 13 讲的考前版，写给 Quiz 4 前一天的你：不跟着 README 逐条敲命令，也没有录制任何
终端输出，而是把小测考的几个机制各画成一张动画图，再用
[dlops-io/model-training](https://github.com/dlops-io/model-training)（`main` 分支，提交 `b9aee1c`）里的代码和课上
notebook “Experiment Tracking using Weights & Bias” 第 38 个单元格作为依据。开头是一个跑完了、没有一个报错的训练 run：
config 在，系统图表也在，却没有 loss 曲线。贯穿全片的问法是：**题目说这个，就想那个**。全片只有一部分（S01–S08）：

- **S01–S03：run 的记录**。一个 run 的记录该装哪七样东西；数据版本是一对东西（bucket 里归档的快照，加上靠内容哈希指向它的
  版本记录），作为一句旁注。`wandb.init` 在账本里开一个新行，并把它设成活跃的 run（指针 `wandb.run`），`wandb.run.finish()`
  把这一行封存；callback（`WandbMetricsLogger` / `WandbCallback`）是 Keras 握着的一支笔，每个 epoch 往**此刻活跃的** run
  写一条历史记录。四个实验：不传 callback；两次 fit 中间没有 finish（一个 run，六条记录）；finish 之后再 init（新的一行拿到
  第一到第四条）；finish 之后不再 init 就 fit（第一个 epoch 之后报错）。第一题。
- **S04：训练包里装了什么**。`setup.py` 的两张清单：`install_requires` 从 PyPI 下载，`find_packages()` 只装带 init 文件的
  目录；打包脚本把 package 目录打成 tar 包放进 bucket，任务跑在 Google 预构建的训练 image 里。队友的模块（编出来的例子
  `augment.py`）没进包，所以依赖全部装好了，却报 `ModuleNotFoundError`；把它写进 `install_requires` 是错的。
- **S05–S06：GPU 和 batch**。`OneDeviceStrategy`、`MirroredStrategy`（一台机器的多块 GPU，靠 all-reduce 同步）和
  `MultiWorkerMirroredStrategy`（多台机器，靠 `TF_CONFIG`）；两台机器各跑各的 `MirroredStrategy`，会训出两个独立的模型。
  在策略下 `dataset.batch` 给的是全局 batch，每个副本的 batch 等于它除以同步的副本数；repo 的训练脚本先乘再分。第二题。
- **S07–S08：比请求活得更久的训练**。请求处理函数、服务器线程、调长客户端超时和 W&B 为什么都不行；正确的设计是提交一个
  持久的 Vertex AI 自定义任务，马上返回任务 ID，然后轮询（`gcloud ai custom-jobs create`）。第三题，最后是周二要记住的六条
  规则。

画面上的代码面板、README 引文、示意的 W&B 和 Vertex AI 界面、任务状态（`QUEUED`、`RUNNING`……）、选择题卡片、课件标签和
思考题都是英文原样，方便你和小测的选项对照；只有旁白译成了中文。三道选择题是小测风格的新题，不是练习题原文；思考题在题目
出现时只问不答，答案在下一段旁白里，连同每个错误选项错在哪。片中没有运行任何命令，项目 ID、密钥和账号也从不出现。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l13-exam.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l13-exam.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l13-exam.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l13-exam.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l13-exam.srt` | 英文字幕 |
| `output/chapters.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml` | 逐句对齐英文的中文译文（字幕用；S01–S08，73 段旁白、176 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（Weights and Biases、W and B、task dot py、wandb dot init、wandb dot run dot finish、Wandb Metrics Logger、setup dot py、install requires、find packages、python dash m trainer dot task、Module Not Found Error、Mirrored Strategy、Multi Worker Mirrored Strategy、n1 standard 32、strategy dot scope、TF config、num workers、dataset dot batch、gcloud AI custom jobs create），英文行换回屏幕上的写法（`Weights & Biases`、`W&B`、`task.py`、`wandb.init`、`wandb.run.finish()`、`WandbMetricsLogger`、`setup.py`、`install_requires`、`find_packages()`、`python -m trainer.task`、`ModuleNotFoundError`、`MirroredStrategy`、`MultiWorkerMirroredStrategy`、`n1-standard-32`、`strategy.scope()`、`TF_CONFIG`、`num_workers`、`dataset.batch`、`gcloud ai custom-jobs create`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、章节名和简介 |

每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L13-training-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L13-training-workflows.md)；
跟着 README 逐条操作的版本是同一讲的跟练视频。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l13-exam --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l13-exam --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l13-exam --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把让步、时间或原因放在后面，中文就不把“虽然……”“直到……”提到
句首，否则相邻两条双语字幕的中英文会互相错开（例如“所以训练脚本照样能 import 它们，虽然 setup.py 从没写过”）。
命令和报错原文放在分句末尾、全角冒号之后（“然后 Vertex 运行：python -m trainer.task。”），这样字幕切分不会把它们拆到
两行上。校对时用工具链的切分函数（`explainer.subtitles.split_balanced` / `_split_like`）逐句核对了长句的中英配对，
并为此调整了四句的措辞，让英文在对应的分句处切开（S04[0] 把训练“从本地搬到云上”、S05[6] 的“在 Vertex AI 上多出来的机器”、
S07[7] 的“再带上区域、名字和 bucket 里的包”、S07[10] 的“训练要跑得比请求还久”）。渲染之后，在 `.zh-en.srt` 里再看一遍
每条带命令和类名的字幕。

## 译文风格

按中国 MLOps 助教考前一天答疑串讲的说法，和第 1–8 讲一致：

- **一字不改**：你要在画面和选项里对照的东西（调用和属性 `wandb.init`、`wandb.run`、`wandb.log`、`fit`、`callbacks`、
  `dataset.batch`，类名 `WandbMetricsLogger`、`WandbCallback`、`OneDeviceStrategy`、`MirroredStrategy`、
  `MultiWorkerMirroredStrategy`、`ModuleNotFoundError`，文件和模块 `setup.py`、`task.py`、`augment.py`、`trainer.task`，
  命令 `python -m trainer.task`、`gcloud ai custom-jobs create`、`import augment`，机型 `n1-standard-32`，任务状态
  `QUEUED`、`PENDING`、`RUNNING`、`SUCCEEDED`，包名 wandb、TensorFlow、scikit-learn、requests）。字幕检查器不收的几种写法
  例外：带下划线的名字按旁白的念法写成空格（install requires、find packages、num workers、TF config），括号去掉
  （`strategy.scope()` 写成 strategy.scope，`wandb.run.finish()` 写成 wandb.run.finish），公式用文字说（“32 乘 4 等于 128”
  “除以同步的副本数”）；英文行通过 `en_display` 保留原样。
- **保留英文**：答疑课上本来就说英文的词，封闭清单：系列沿用的 repo、pin、lock 文件、container、image、bucket、ID、CLI、
  pipeline、notebook，第 8 讲的 epoch、batch（只指训练的 batch）、loss；这一讲新增 run（W&B 的 run，只作名词）、callback、
  logger、config（run 的 config）、all-reduce、worker（`TF_CONFIG` 里的一台机器）、worker pool。
- **其余用中文标准术语**（TensorFlow 和 Google Cloud 中文文档里的译名，方便搜索）：实验追踪、可复现、训练工作流、活跃的 run、
  历史记录、指标、系统图表、数据版本、快照、版本记录、内容哈希、密钥、命令行参数、包、tar 包、打包脚本、依赖、模块、导入路径、
  预构建的训练 image、任务、训练任务、自定义任务、持久的任务、提交、轮询、计费、策略、副本、同步、梯度、分片、优化器变量、
  全局 batch、每个副本的 batch、请求处理函数、请求超时、服务器线程、服务器实例、客户端超时、生命周期、无服务器训练。
- **比喻按意思译，一个比喻一个词**：账本和一行、笔（callback）、指针（`wandb.run`）、封存、购物清单（`install_requires`）、
  连线、托盘和一份、时钟（生命周期）、工单（任务）、引擎、杠杆。
- **分清容易混的词**：W&B 的 run 是名词，动词的 run 说“跑 / 运行”；replica 是“副本”，mirrored 是“复制”，“镜像”只留给
  书面的 image；shard（每台机器的一份数据）是“分片”，slice（一个 batch 切给每个副本的那份）是“一份”；Vertex 的副本数数的是
  机器，repo 的 num workers 数的是一台机器上的 GPU；包（Python package）、tar 包（tarball）和 package 目录（`package/`）
  是三样东西，上传了不等于安装了；job 是“任务”，submit 是“提交”（字幕里 commit 一直说英文）；笔记是 notes，笔记本是
  laptop；系统图表里的 memory 是内存。
- **精确**：数字照旁白写（8 个副本、16、128、4 块 GPU、32、副本数为 1），叙述里的数量用汉字（七样、四个调用、两块 T4 GPU、
  六条记录）；W&B 的行为按 `setup.py` 固定的 wandb 0.15.11 说；思考题只问不答；选择题的答案先给字母，再按英文的顺序逐个说
  错误选项错在哪（“A：……”“B：……”）。
- 标题、章节名、简介和这份说明用书面语：仓库、容器、镜像、存储桶、运行（run）、回调（callback）、配置（config）、
  轮次（epoch）、批次（batch）、全局批次、每副本批次、副本（replica）、训练任务、自定义训练任务（custom job）；类名和函数名
  照写。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| run (W&B) | run（字幕）；运行（书面） | 运行、实验 |
| active run | 活跃的 run | 当前运行 |
| callback | callback（字幕）；回调（书面） | 回调函数 |
| history entry | 一条历史记录 | 日志条目 |
| config | config（字幕）；配置（书面） | 配置项 |
| source distribution / package | 包 | 源码分发包 |
| tarball | tar 包 | 压缩包 |
| custom job | 自定义任务（字幕）；自定义训练任务（书面） | 自定义作业（Google Cloud 中文文档） |
| durable job | 持久的任务 | 持久化作业 |
| replica | 副本 | 副本 |
| mirrored | 复制 | 镜像（易和 image 混） |
| global batch | 全局 batch（字幕）；全局批次（书面） | 全局批大小 |
| per-replica batch | 每个副本的 batch（字幕）；每副本批次（书面） | 单卡批大小 |
| shard | 分片 | 数据分片 |
| all-reduce | all-reduce | 全归约 |
| worker pool | worker pool（字幕）；工作器池（书面） | 工作池 |
| serverless training | 无服务器训练 | Serverless 训练 |
