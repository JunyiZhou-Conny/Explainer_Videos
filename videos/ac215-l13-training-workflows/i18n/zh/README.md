# 中文字幕说明

视频 *AC215 · Lecture 13 — Advanced training workflows: a run is a record, a job is a rented machine (follow-along: model-training + two Colab notebooks)*
（**AC215 · 第 13 讲：进阶训练工作流——运行是一份记录，任务是一台租来的机器（跟练：model-training + 两个 Colab 笔记本）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 13 讲“进阶训练工作流”（W&B 实验追踪、Vertex AI 无服务器训练、
GPU 和多 GPU）的跟练视频，照着课上的两个 Colab notebook 和教程仓库的 README 从头做到尾，分两部分：

- **第一部分（S01–S07）**：两个 Colab notebook。从“两张表，两个冠军”这个谜题开始：同样的数据、同样的五个奶酪分类模型，
  notebook A 和 notebook B 却选出了不同的最佳模型。先看 notebook A 手写的 `experiment_<时间戳>/` 目录记下了什么、漏掉了什么
  （没有随机种子的划分、按字符串排序的准确率、`validation_percent` 的小疏漏）；再看 notebook B 用 Weights & Biases（W&B）把五个 run
  放到同一条 epoch 轴上：为什么只有带 callback 的 `2_block` 有曲线，为什么 `wandb.config = {...}` 让 run 的 config 变成空的，
  以及 init / callback / finish 三行的正确写法；然后讲清无服务器训练就是“只为训练这一步租一台机器”，并照着
  [dlops-io/model-training](https://github.com/dlops-io/model-training)（commit `b9aee1c`）的 README 准备 Vertex AI API、
  GPU 配额、`secrets` 目录、服务账号 `model-trainer` 和 JSON 密钥、bucket 和 W&B 密钥。
- **第二部分（S08–S15）**：构建本地的 model-trainer CLI 容器（“驾驶舱”）：今天会遇到的两处 Dockerfile 报错和两处一行修复
  （第 2 行换成 bookworm，第 37 行换成 `google-cloud-cli`），证明它只负责提交、从不 import TensorFlow；看 `setup.py` 和 `task.py`，
  用 `sh package-trainer.sh` 把训练代码打成 4 KB 的 tar 包传到 bucket；用 `sh cli.sh` 提交 Vertex AI 自定义任务，用 `sh -x` 看清
  W&B 密钥怎样明文出现在任务参数里；分清提交任务的服务账号和运行任务的服务代理，在本地替身里重放任务的第一步（`pip install` tar 包、
  三把 W&B 密钥的登录结果）；任务会打印什么、W&B 能显示什么；一块 GPU 需要一致的三个开关；`MirroredStrategy` 的数据并行
  （拆分全局 batch、all-reduce 平均梯度、在 `strategy.scope()` 里建模型）；最后是没有保存下来的模型、收尾清单和回顾。

画面上的终端输出、代码面板、notebook 单元格和它们保存下来的输出、README 引文、示意控制台、W&B 和 Colab 的示意图、训练地图、账本、
三枚徽章、开关面板、副本示意图和各种标签（`your turn`、`extra`、`stand-in`、`illustration`、`recorded`、金色的计费标签、
`Lecture 13 · slides …`）都是英文原样，方便你对照着敲。画面上出现授课老师名字的地方遮成 ‹instructor›，字幕里一律写“授课老师”。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-10-23，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
README 的每条命令按原样、按顺序运行；README 里没有、但有助于理解的检查（`git log`、`ls`、`git diff`、`echo` 密钥长度、
容器里的 `import tensorflow`、`sh -x`、`gcloud auth list`、`pip list`、`docker ps` 等）在画面上标着 `extra`。

录制机器**没有 Google 凭据、没有 W&B 账号、没有 GPU，也没有浏览器**。所以：

- 本地的部分都是实录：clone、`secrets` 目录、驾驶舱容器的构建（包括两次失败和两处修复）、它的 entrypoint、tar 包、容器里的检查、
  `python cli.py` 的第一处报错。
- 每个需要 Google、Vertex AI 或 W&B 的步骤（`gsutil cp`、`sh cli.sh` 和 `sh cli-multi-gpu.sh` 里的 `gcloud ai custom-jobs create`、
  任务本身、W&B 页面）都录到它如实的失败为止。目录列表里出现的密钥是一个明显无效的替身，容器启动之前就移走了；视频在 S07 如实说明了这一点。
- 两个 notebook 的结果来自课上那两份 notebook 里保存下来的输出（授课老师在 Tesla T4 上的运行，2025-10-14 和 2025-10-20），标着 `recorded`；
  任务日志的样子按 `task.py` 自己的 print 语句拼出来，同样注明出处。
- Vertex 任务的第一步（在普通的 Python 3.10 容器里 `pip install` tar 包）和训练脚本的 W&B 登录（空密钥、默认的 `16`、40 个字符的占位密钥），
  以及 notebook B 的 `pip install wandb` 和 `wandb.config` 的离线检查，都在本地替身里重放，标着 `stand-in`。
- 会变的版本号字幕里都加“录制时”（wandb 0.31.0、Debian 软件源的状态、Google 还在提供的 GPU image）。

本讲的 Vertex AI 任务在运行期间会向你的 GCP 项目计费，GPU 只要挂着就计费：每个计费点都有金色标签（不写具体金额，请以官方价目页为准），
S15 是完整的收尾清单，包括学期结束时删掉 `model-trainer` 的密钥、轮换跟着任务出去过的 W&B 密钥。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l13-training-workflows.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l13-training-workflows.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l13-training-workflows_part1.*`、`_part2.*` | 上下两部分（S01–S07：两张表、notebook A 的实验目录、W&B 的 run 和空的 config、无服务器训练和准备工作；S08–S15：驾驶舱的构建、tar 包、提交任务、两种身份、日志和指标、GPU 的三个开关、MirroredStrategy、收尾），每部分有自己的视频和字幕文件 |
| `output/ac215-l13-training-workflows.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l13-training-workflows.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l13-training-workflows.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S07），`g2` 是第二部分（S08–S15）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，下载链接见
[`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令、真实输出和练习答案
在学习指南 [MLOps_Learning · guides/L13-training-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L13-training-workflows.md)。
同一讲的考前复习版在 [`../../../ac215-l13-exam/`](../../../ac215-l13-exam/)，两者的术语一致。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l13-training-workflows --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l13-training-workflows --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l13-training-workflows --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l13-training-workflows --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（106 段），`en` 和 SAY 逐字相同；`zh` 按
`explainer.voice.split_sentences` 切出的英文句子一句对一句（共 351 句：第一部分 149 句，第二部分 202 句），不合并、不拆分。
字幕按英文旁白录下的时间显示：双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序
（条件和时间从句留在英文放的位置，比如“用在你必须自己托管的时候”“芯片只在三个都打开时才会亮”“这是录制时的情况”都放在句末）。
SAY 为了让语音读对，把实物念成了单词（W and B、wandb init、model fit、two block、validation percent、dash U、set dash e、x86 64、
slash secrets、python dash m trainer dot task、sh dash x、model trainer、api key not configured、model save）；这些句子（46 段）在
`en_display:` 里给出屏幕上的写法（`W&B`、`wandb.init`、`model.fit`、`2_block`、`validation_percent`、`-U`、`set -e`、`x86_64`、
`/secrets`、`python -m trainer.task`、`sh -x`、`model-trainer`、`api_key not configured`、`model.save`、`--model-dir`），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、image 和 container 的名字、服务账号名、
角色名、控制台和 Colab 的菜单项、W&B 的项目名、notebook 的列名、版本号、HTTP 状态码）一字不改；终端和代码里的状态行与报错原文照抄
（404 Not Found、no installation candidate、API key must be 40 characters long, yours was 2、Training Job Complete、GPU Available）。
实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、pin、root、shell、container、image、base image、tag、Dockerfile、
entrypoint、bucket、API key、endpoint、diff、Colab、notebook、pipeline、label，第 8 讲和考前版的 epoch、batch、loss、run、callback、config、
all-reduce、worker pool，加上这一讲的 release、secret、zip、dict、worker pool spec；其余用中文标准术语（Google Cloud 和 TensorFlow 的
中文文档、机器学习文献）：实验追踪、可复现、可追责、单元格、运行时、划分、训练集、验证集、测试集、随机种子、微调、冻结、权重、指标、
准确率、系统图表、曲线、tar 包、依赖、模块、命令行参数、预构建的 image、任务、自定义任务、无服务器训练、计费、配额、区域、服务账号、
服务代理、密钥、角色、软件源、归档源、加速器、副本、梯度、全局 batch、学习率、收尾。job 一律是“任务”，copy 一律是“拷贝”（“副本”只留给
replica），laptop 是“笔记本”，lecture notes 的“笔记”和它分开；“标签”只指画面上的标签（黄色标签、金色标签），数据的类别词说 label。

视频里的比喻按意思译，一个比喻一个词：杠杆（三个让深度学习变好的办法）、账本和一行（ledger 和它的 row）、地图和这条线（训练地图上的
Colab 和 repo 两条线）、抽屉（run 的 config）、散落的字典（被赋值挪走的 wandb.config）、驾驶舱（本地的 CLI 容器）、铭牌（pip 读的 setup.py）、
徽章和挂绳（三种身份）、另一栋楼（W&B）、开关（GPU 的三个条件）、租（无服务器训练）。README 和 notebook 的疏漏照英文的语气温和地说
（统一说“一个小疏漏”），后面紧跟改法。字幕检查不允许中文行里出现下划线、等号或括号，所以几样实物在中文行里按旁白的说法写，英文行照常
显示原样：`validation_percent` / `test_percent` → validation percent / test percent，`2_block` → 2 block，`train_base` → train base，
`find_packages()` → find packages，`__init__.py` → init 文件，`--wandb_key` → 密钥参数，`--batch_size=32` → batch 大小参数是 32，
`GCP_REGION` → region 变量，`--model-dir` → model dir 参数。授课老师的名字从不出现在字幕、标题、章节名和简介里。双语字幕的英文原句
就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。
