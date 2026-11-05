# 中文字幕说明

视频 *AC215 · Lecture 14 — Serverless deployment: a function, a service and a job on Cloud Run (follow-along: serverless-deployment)*
（**AC215 · 第 14 讲：无服务器部署——Cloud Run 上的函数、服务与作业（跟练：serverless-deployment）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 14 讲“无服务器部署：Cloud Functions 与 Cloud Run”的
跟练视频，对照课件逐页讲解，并照着教程仓库 [dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment) 的 README
（`main` @ commit `46cc62f`，即 2026-11-04 课程链接实际指向的版本；课程地图里旧的 pin `4eaf343` 只作背景，见
[`ASSETS.md`](../../ASSETS.md) “Which commit”）从“开始之前”一步一步做到收尾清理，分两部分：

- **第一部分（S01–S08）**：从一个只在 localhost 上能跑的翻译页面开始，画出课上的四格地图（交出代码文件还是容器，跑在租来的机器上
  还是无服务器上）；开始之前的项目、区域、克隆仓库和七条 `export`；第 1 部分把翻译处理函数部署成 Cloud Run 函数（`main.py`、
  `requirements.txt` 的两个精确 pin 和入口点 `hello_http`），看 Cloud Build 怎样把代码做成镜像、Functions Framework 怎样在每个实例里
  调用你的函数，入口点填错时在日志里看到什么，再用查询字符串调用它；第 2 部分用一条 `docker run` 在本地跑起预构建的翻译网页，讲清
  `PORT`、`0.0.0.0` 和 `-p 8086:8080`，再把同一个镜像部署成 Cloud Run 服务（service）：最小 / 最大实例数、并发数和 gunicorn 的线程数、
  按请求计费、修订版本（revision），以及 tag 和 digest 的区别。
- **第二部分（S09–S16）**：第 3 部分分开“谁能调用它”和“它以谁的身份运行”两扇门，挂上不需要密钥的运行时服务账号、设好三个环境变量、
  打开 Gemini 语音合成，再用应用默认凭据（ADC）加服务账号模拟（impersonation）和 `uv sync --frozen` 在本地开发；第 4 部分把同一个镜像
  跑成 Cloud Run 作业（job）：两个私有存储桶和按桶授权、Container command 加 11 个独立参数、两种填错的方式、执行后的 attempt 目录和
  作为回执的 manifest，然后用 gcloud 覆盖参数和 helper 脚本从终端提交新的工作；最后逐项清理所有计费资源，用课上的四格地图和三个缺点
  （冷启动、控制和调试受限、厂商锁定）收尾，留五道自测题。

画面上的终端输出、代码面板、README 引文、示意控制台、地图和各种标签（`your turn`、`extra`、`extra · local stand-in`、`illustration`、
`recorded`、`erratum`、金色的计费标签、`Lecture 14 · slides …`）都是英文原样，方便你对照着敲。授课老师的名字从不出现在画面、字幕、
标题、章节名和简介里。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-04，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
在你自己机器上跑的步骤都是实录：clone、Part 2 的 `docker run`（公开镜像现拉，digest 和 README 一致）、网页和 JSON 接口、
Part 3.3 的 `uv sync --frozen` 和本地启动、镜像的 `batch` 命令、helper 脚本的 dry run。README 里没有、但有助于理解的检查
（`git log`、目录列表、`docker top`、`docker ps`、`curl`、`uv tree`、改 `PORT` 的实验，以及用同一版 Functions Framework 在本地跑
第 1 部分处理函数的替身）在画面上标着 `extra`。

录制机器**没有 Google 账号，也没有 GCP 项目**。所以：

- 每个 gcloud 命令框都录到它遇到的第一个如实的报错为止（占位符项目 ID 无效，然后是没有登录的账号）；控制台步骤是按 README 自己的
  字段值画出来的示意图，标着 `illustration`。
- 只有云端才能显示的结果（函数的 URL 回答、部署好的 service、语音、job 写出的文件）标着 `recorded`，引自 README 和它的录制记录。
- 课件和 README 不一致的地方（Python 3.10 → 3.12、按位置传参会对调 source 和 destination、Cloud Functions 改名 Cloud Run functions、
  README 3.3 节许诺的权限和实际授予的不同），以录到的为准，视频会温和地指出来。

本讲会在你自己的 GCP 项目里创建计费的 Cloud Run 函数、服务和作业、存储桶，还会调用付费的语音模型：每个计费点都有金色标签，
S16 是完整的收尾清单。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l14-serverless-deployment.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l14-serverless-deployment.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l14-serverless-deployment_part1.*`、`_part2.*` | 上下两部分（S01–S08：地图、开始之前、Cloud Run 函数、查询字符串、本地镜像、Cloud Run 服务；S09–S16：两扇门和运行时服务账号、语音、ADC 本地开发、作业和存储桶、命令和参数、执行与回执、终端和 helper 脚本、收尾），每部分有自己的视频和字幕文件 |
| `output/ac215-l14-serverless-deployment.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l14-serverless-deployment.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l14-serverless-deployment.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S08），`g2` 是第二部分（S09–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L14-serverless-deployment.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L14-serverless-deployment.md)。
同一讲还有一个先讲概念的考前精讲版 [`ac215-l14-exam`](../../../ac215-l14-exam/)，本片沿用了它的术语决定。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l14-serverless-deployment --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l14-serverless-deployment --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l14-serverless-deployment --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l14-serverless-deployment --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（159 段：第一部分 79 段，第二部分 80 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 357 句：174 + 183），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的和时间从句留在英文放的位置）；
纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，把实物念成了单词（hello underscore HTTP、percent 20、Z H dash C N、
A M D 64、translation demo serve、Control C、no invoker IAM check、ENABLE SPEECH、uv sync with frozen、run zero zero one、dash m、
translated dot txt……）；这些句子（22 段）在 `en_display:` 里给出屏幕上的写法（`hello_http`、`%20`、`zh-cn`、`amd64`、
`translation_demo serve`、`Ctrl+C`、`--no-invoker-iam-check`、`ENABLE_SPEECH`、`uv sync --frozen`、`run-001`、`-m`、`translated.txt`……），
双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、目录、镜像和资源的名字、服务账号 ID、角色名、
控制台按钮和字段、区域名、HTTP 状态码）一字不改，比如 translate-function、translation-demo、translation-audio、
translation-demo-runtime、Allow public access、Request-based billing、Save and redeploy、Service Account User、
Service Account Token Creator、Storage Object Creator、Container command、us-central1。旁白转述的报错译成中文（方法不允许、
语音已关闭、Google 凭据不可用、找不到可执行文件），状态码照写数字。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、pin、container、image、port、bucket、endpoint、pipeline、entrypoint、
worker，加上这一讲的 serverless、service、job、revision、task、tag、digest、manifest、chip、impersonate；其余用中文标准术语（Google Cloud
中文文档的译名）：函数、处理函数、装饰器、入口点、查询字符串、实例、并发数、最小 / 最大实例数、按请求计费、扩缩、冷启动、
服务账号、运行时服务账号、角色、主账号、配额项目、应用默认凭据、令牌、软删除、前缀、回执、厂商锁定。几组容易混的词始终分开：
函数的入口点（entry point）≠ Docker 的 entrypoint；Cloud Run 的 service ≠ 服务账号 ≠ 外部的翻译服务；
“谁能调用它”（公开访问）≠ “它以谁的身份运行”（运行时服务账号）。视频里的比喻一个比喻一个词：门（port 和两扇身份的门）、工牌（服务账号）、
计价器（计费）、回执（manifest）。

字幕检查不允许中文行里出现下划线名字、加号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：`hello_http` →
hello 下划线 http，`translation_demo` → translation demo，`ENABLE_SPEECH` 等三个环境变量 → ENABLE SPEECH 这样的写法，
`Ctrl+C` → Ctrl-C。标题、章节名和简介用书面语体（容器、镜像、仓库、存储桶、服务、作业、修订版本）。双语字幕的英文原句就在中文下方，
所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| serverless | serverless | 无服务器 |
| Cloud Run function / handler / entry point | 函数 / 处理函数 / 入口点 | Cloud Run 函数（旧名 Cloud Functions） |
| service / job / task | service / job / task | 服务 / 作业 / 任务 |
| revision / tag / digest | revision / tag / digest | 修订版本 / 标签 / 摘要 |
| instance / concurrency / min / max instances | 实例 / 并发数 / 最小实例数 / 最大实例数 | 同左 |
| request-based / instance-based billing | 按请求计费 / 按实例计费 | 同左 |
| cold start / scale to zero | 冷启动 / 缩容到零 | 同左 |
| query string | 查询字符串 | 同左 |
| runtime service account / badge | 运行时服务账号 / 工牌 | 服务账号（Service Account） |
| Application Default Credentials | 应用默认凭据 | 应用默认凭据（ADC） |
| impersonate | impersonate | 服务账号模拟（impersonation） |
| quota project / principal | 配额项目 / 主账号 | 同左 / 主体 |
| bucket / prefix / soft delete | bucket / 前缀 / 软删除 | 存储桶 / 对象前缀 / 同左 |
| entrypoint / command / arguments | entrypoint / 命令 / 参数 | 入口点（Docker ENTRYPOINT） / CMD / 参数 |
| manifest / receipt | manifest / 回执 | 清单文件 |
| vendor lock-in | 厂商锁定 | 同左 |
