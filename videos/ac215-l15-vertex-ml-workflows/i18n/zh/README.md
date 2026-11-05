# 中文字幕说明

视频 *AC215 · Lecture 15 — ML workflows: deploy one model, then automate the pipeline on SageMaker (follow-along: model-deployment-aws + ml-workflow-aws)*
（**AC215 · 第 15 讲：机器学习工作流——在 SageMaker 上部署一个模型，再用 pipeline 自动化整条流程（跟练：model-deployment-aws、ml-workflow-aws）**）
是英文旁白，配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 15 讲“ML Workflows（模型部署与 ML pipeline）”的
跟练视频，对照课件逐页讲解。课件讲的是 Google Cloud 上的 Vertex AI；按系列决定，视频跟的是课程的 AWS 版教程
[dlops-io/model-deployment-aws](https://github.com/dlops-io/model-deployment-aws)（`main` @ commit `077f4db`）和
[dlops-io/ml-workflow-aws](https://github.com/dlops-io/ml-workflow-aws)（`main` @ commit `f165c6e`），两个 commit 都在 2026-11-05
用 `git ls-remote` 复核过（见 [`ASSETS.md`](../../ASSETS.md) “Which commits”）。课件的概念决定讲什么，README 和实录决定画面上演示什么，
两边名词不同的地方（bucket → S3、服务账号密钥 → IAM 用户加角色、endpoint → endpoint 配置加 endpoint、Vertex AI Pipelines → SageMaker
Pipelines、Kubeflow 的 DSL → SageMaker 的步骤类和属性引用）视频会逐一指出来。分两部分：

- **第一部分（S01–S09，model-deployment-aws）**：从“三个数还是四个数”的谜题开始，画出 endpoint 背后的三样东西（产物、container、机器）；
  在控制台建 IAM 用户、访问密钥、`SageMakerExecutionRole` 和 bucket，`aws configure`；构建 CLI container 时遇到今天才会出现的两个问题
  （arm64 构建行在 Intel 机器上的 `exec format error`，以及 Pipfile 里 `sagemaker = "*"` 解析成 SDK 3、导入失败），各用一行修好；
  讲清预处理放在客户端还是模型里（服务签名）；`--prepare` 生成的 SavedModel、版本目录 `1` 和 `model.tar.gz`；`--deploy` 一次创建的模型、
  endpoint 配置和 endpoint；`--predict` 为每张照片发送的 150,528 个数字，以及本地 TensorFlow Serving 替身给出的真实回答；
  `--delete` 的三种方式和它漏掉的那个 endpoint。
- **第二部分（S10–S16，ml-workflow-aws）**：从“四个人守着四个终端”到编排器和工作流管理；控制台里的快速设置、Unified Studio 域、
  `ml-workflow-user` 和两个角色；手动运行数据采集器、数据处理器和本地训练（两处小修复：类别数改成 4、`persistent` 目录的所有者）；
  把两个 image push 到你自己账号的 ECR；在 workflow container 里用 SDK 提交一个处理任务（Processing job），看懂生产模式；
  最后读懂由属性引用连成的五步 SageMaker Pipeline（缓存、`DeployModel` 这个 Lambda 步骤、经过 bucket 传递的文件），逐项清理所有计费资源，
  用课上的“工厂和配方”收尾，留自测题。

画面上的终端输出、代码面板、README 引文、示意控制台、示意图和各种标签（`your turn`、`extra`、`extra · local stand-in`、
`extra · capture stub`、`illustration`、`recorded`、`erratum`、金色的计费标签、课件标签）都是英文原样，方便你对照着敲。
课件标签只在重画的课件图还在画面上时出现。授课老师的名字从不出现在画面、字幕、标题、章节名和简介里。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-05，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
在你自己机器上跑的步骤都是实录：两次 clone、CLI container 的构建（包括两处一行修复前后）、数据采集器抓图和打包、数据处理器的查重和
TFRecords、本地训练、`package-trainer.sh` 打出的 tar 文件。README 里没有、但有助于理解的检查（`git log`、目录列表、版本检查、
`saved_model_cli` 读出的签名、`git status`，以及 S3 换成 stub 的 `--prepare`、公开的 TensorFlow Serving 2.13 image 做的本地替身、
离线生成的 pipeline JSON 定义）在画面上标着 `extra`。

录制机器**没有 AWS 账号**。所以：

- 每个 AWS 调用都录到它遇到的第一个如实的报错为止（找不到凭据，或者 AWS 拒绝明显假的占位密钥）；控制台步骤是按 README 画出来的示意图，
  标着 `illustration`。
- 只有云端才能显示的结果：`--predict` 的 README 输出标着 `recorded`，引自 README；训练任务、处理任务和 pipeline 的运行图是示意，
  标着 `illustration`；本地替身标着 `extra · local stand-in`。从不伪造成功。
- 课件、两份 README 和实录不一致的地方（README 的预测输出来自一个更旧的三分类模型、README 说的模型注册表其实是普通的 SageMaker 模型、
  签名的变化在训练脚本里而不在部署步骤里、课上的四步在这里拆成五步），以录到的为准，视频会温和地指出来。

本讲会在你自己的 AWS 账号里创建计费的 endpoint、训练和处理任务、S3 存储、ECR 仓库和 pipeline 步骤：每个计费点都有金色标签，
S16 是完整的收尾清单。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l15-vertex-ml-workflows.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l15-vertex-ml-workflows.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l15-vertex-ml-workflows_part1.*`、`_part2.*` | 上下两部分（S01–S09：部署一个模型；S10–S16：自动化工作流），每部分有自己的视频和字幕文件 |
| `output/ac215-l15-vertex-ml-workflows.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l15-vertex-ml-workflows.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l15-vertex-ml-workflows.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S09），`g2` 是第二部分（S10–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L15-vertex-ml-workflows.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L15-vertex-ml-workflows.md)。
同一讲还有一个先讲概念的考前精讲版 [`ac215-l15-exam`](../../../ac215-l15-exam/)，本片沿用了它和它一致的术语决定。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l15-vertex-ml-workflows --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l15-vertex-ml-workflows --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（139 段：第一部分 75 段，第二部分 64 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 390 句：210 + 180），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的、原因和时间从句留在英文放的位置）；
纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，把实物念成了单词（A R N、A R M 64、A M D 64、dash dash prepare、
model dot tar dot G Z、M L M5 extra large、endpoint config dot JSON、star、less than 3、slash persistent slash model、or true、D S L、
cheese app endpoint……）；这些句子（51 段：22 + 29）在 `en_display:` 里给出屏幕上的写法（`ARN`、`arm64`、`amd64`、`--prepare`、
`model.tar.gz`、`ml.m5.xlarge`、`endpoint_config.json`、`"*"`、`"<3"`、`/persistent/model`、`|| true`、`DSL`、`cheese-app-endpoint`……），
双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、目录、用户 / 角色 / bucket 的名字、pipeline 的
步骤名、控制台标签、模型的 label、区域和实例类型、终端打印的短报错）一字不改，比如 model-deployment、SageMakerExecutionRole、
CheeseAppSageMakerExecutionRole、ml-workflow-user、DataCollector、DeployModel、raw-data、us-east-1、ml.m5.xlarge、
exec format error、Unable to locate credentials、AWS not configured、Permission denied。旁白转述的报错译成中文（没有凭据、
找不到凭据、AWS 拒绝了我们的假密钥、账号查询失败了）。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、pin、container、image、tag、Dockerfile、bucket、endpoint、
entrypoint、pipeline、registry、notebook、release、label、epoch、shell、root、serverless、SDK、CLI、URI、IAM，加上这一讲的 push、
upsert、stub、socket 和只指 SDK 对象的 processor；其余用中文标准术语（AWS 中文控制台和文档、TensorFlow 文献的译名）：IAM 用户、角色、
策略、访问密钥、凭据、令牌、区域、域、快速设置、实例、签名、预处理、缩放、归一化、浮点数、概率、准确率、计算图、权重、导出、编排器、
工作流管理、托管、调度、缓存、属性引用、步骤、边、数据采集器、数据处理器、训练任务、处理任务。视频里的比喻一个比喻一个词：计价器（计费）、
墙（export 的密钥掉在 container 的墙外）、前门（模型的签名）、遥控器（SDK）、工厂 / 配方（pipeline）。

字幕检查不允许中文行里出现下划线名字、星号、尖括号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：`"*"` → 星号，
`"<3"` → 小于 3，`get_execution_role` → get execution role，`serving_default` → serving default，`saved_model.pb` → saved model 那个
pb 文件，`endpoint_config.json` → endpoint config 那个 JSON 文件，`--data_collector` → 带上 data collector 参数。
标题、章节名和简介用书面语体（容器、镜像、仓库、存储桶、端点、端点配置、镜像仓库、服务签名、属性引用、处理任务、推送）。
双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| endpoint / endpoint configuration | endpoint / endpoint 配置 | 端点 / 端点配置 |
| IAM user / role / policy | IAM 用户 / 角色 / 策略 | 同左 |
| access key / credentials / token | 访问密钥 / 凭据 / 令牌 | 同左 |
| execution role / ARN | 执行角色 / ARN | 同左（Amazon 资源名称） |
| bucket | bucket | 存储桶 |
| registry / ECR repository | registry / ECR 仓库 | 镜像仓库 |
| push / upsert | push / upsert | 推送 / 创建或更新 |
| stub / stand-in | stub / 替身 | 桩 / 本地替代 |
| signature / serving default | 签名 / serving default | 服务签名（serving signature） |
| SavedModel / tarball | SavedModel / tar 包 | 同左 / 压缩包 |
| model registry | 模型注册表 | 同左 |
| orchestrator / workflow management | 编排器 / 工作流管理 | 同左 |
| Processing job / Training job | 处理任务 / 训练任务 | 同左 |
| property reference / step / edge | 属性引用 / 步骤 / 边 | 同左 |
| caching / scheduling | 缓存 / 调度 | 同左 |
| scale to zero | 缩容到零 | 同左 |
