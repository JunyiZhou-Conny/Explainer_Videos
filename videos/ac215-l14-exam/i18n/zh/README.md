# 中文字幕说明

视频 *AC215 · Lecture 14 — Serverless Deployment (exam edition)*
（**AC215 · 第 14 讲：无服务器部署（考前精讲版）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 14 讲的**考前精讲版**，为周二的第 4 次小测准备：不逐条跟练 README，也不做任何
现场运行，而是用动画把小测考的机制讲透，再拿两个演示仓库的源码和 README 原文作依据：
[dlops-io/serverless-deployment](https://github.com/dlops-io/serverless-deployment)（`main` 分支，提交 `46cc62f`）和
[dlops-io/model-deployment](https://github.com/dlops-io/model-deployment)（`main` 分支，提交 `cf0b7c7`，对应第 15 讲课件
第 11–17 页里 serving 签名的那一半）。开头是一个永远跑不完的 Cloud Run job：和一个好好的翻译 web 应用用同一个镜像，
却一直跑到任务超时被平台停掉。贯穿全片的结论是：**看生命周期，看什么一直开着，看平台调用的是哪个名字**。共八章：

- **S01 开头**：`translation-audio` 这个 job 为什么不结束；这一讲归结为五个考点，右上角的灰色标签标出每个考点的课件页。
- **S02 服务（service）还是作业（job）**：同一个镜像的两个启动命令 `serve` 和 `batch`；service 监听 port、按流量扩缩、
  可以缩容到零，job 跑到完成就退出（失败时退出码 1）；开头那个 job 继承了默认命令 `serve`；Cloud Scheduler 定时触发。
  一道新的选择题。
- **S03 空闲的时间谁来买单**：两个计价器，虚拟机按预配的时长计费，函数和最小实例数为 0 的 Cloud Run service 按调用次数
  和执行时间计费；冷启动和最小实例数；下一讲 Vertex AI 端点的最小副本数也是常驻资源。一道新的选择题。
- **S04 函数还是容器**：部署函数交出源代码、requirements 文件和入口点 `hello_http`，由 Cloud Build 构建镜像；入口点填错时
  构建失败；部署 Cloud Run service 交出现成的镜像；两者最后都是 Cloud Run 上的容器实例。
- **S05 谁能调用，以谁的身份运行**：公开访问和 403；运行时服务账号 `translation-demo-runtime` 和它的角色，没有密钥文件；
  部署者需要 Service Account User；job 自己的服务账号和存储桶角色；三种日志各看什么。
- **S06 预处理放在哪里**：两个客户端各带一份预处理就是客户端的脆弱性；把预处理挪进端点（endpoint），瘦客户端只发
  base64 编码的 JPEG 字节；一次回滚同时修好所有客户端，不用发布客户端。
- **S07 注册 serve**：`preprocess_image` 只返回图片，原始模型要浮点张量，只有 `serving_function`（导出为
  `serving_default`）先预处理、再推理。一道新的选择题。
- **S08 回顾**：周二小测的七条规则，以及下一讲的经验法则和课件第 16 页的三个代价。

画面上的代码面板、README 摘录、示意的控制台小卡、课件标签、示意图标注、规则卡片和思考题卡片都是英文原样，方便你和
仓库、考题对照；只有旁白译成了中文。视频里的三道选择题（S02、S03、S07）是新写的，不是课程的练习题。项目 ID、密钥和
任何人名都不出现在字幕和文件里。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。这期没有分成两部分。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l14-exam.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l14-exam.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l14-exam.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l14-exam.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l14-exam.srt` | 英文字幕 |
| `output/chapters.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml` | 逐句对齐英文的中文译文（字幕用；S01–S08 全片一个文件，66 段旁白、191 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（translation audio、hello underscore HTTP、translation demo runtime、preprocess image、serving function、bytes inputs、serving default），英文行换回屏幕上的写法（`translation-audio`、`hello_http`、`translation-demo-runtime`、`preprocess_image`、`serving_function`、`bytes_inputs`、`serving_default`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、章节名和简介 |

每个考点的完整讲解、命令清单和中文速览在学习指南
[MLOps_Learning · guides/L14-serverless-deployment.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L14-serverless-deployment.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l14-exam --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l14-exam --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l14-exam --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、原因或补充放在后面，中文就不把它们提到句首，否则相邻两条
双语字幕的中英文会互相错开。校对时用字幕切分逐句核对过长句的配对，改过几处：例如“这个 job 继承了 image 的默认命令，
也就是 serve，所以……”让 serve 和英文的 “default command, serve,” 落在同一条；“就有一个热实例一直开着等第一个请求，
它自己的计价器也在走”让“等第一个请求”和 “for the first request” 同条；“代码只是请求默认凭据，而在 Cloud Run 上
平台会……”不把“在 Cloud Run 上”留在前一条。渲染之后，在 `.zh-en.srt` 里再看一遍每条带代码名的字幕。

## 译文风格

按中国 MLOps 助教考前一天带复习课的说法，和第 1–8 讲一致：

- **一字不改**：你要在屏幕上对照的东西：命令 `serve`、`batch`、`python`，文件名 Dockerfile、main.py，job 名和账号名
  `translation-audio`、`translation-demo-runtime`，控制台字样 Execute，状态码 403，方法名 predict，gunicorn，角色名
  Agent Platform User、Service Usage Consumer、Service Account User、Storage Object Viewer、Storage Object Creator，
  产品名 Cloud Run、Cloud Run functions、Cloud Functions、Functions Framework、Cloud Build、Artifact Registry、
  Cloud Scheduler、Vertex AI。字幕检查器不收的几种写法例外：带下划线的名字按旁白的念法写成空格（hello 下划线 http、
  preprocess image、serving function、serving default、bytes inputs），检查器不收的符号用文字说（224 乘 224、
  0 到 1 之间、源代码加入口点）；英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，封闭清单：第 1 讲的 repo；第 2–4 讲的 container、image、port、token、
  Dockerfile、bucket；第 8 讲的 endpoint；这一讲新增 service、job、serverless、resize（service 和 job 也是考题选项里的词）。
- **其余用中文标准术语**（Google Cloud 中文文档和中文技术资料里的译名）：函数、入口点、生命周期、实例、流量、缩容到零、
  触发器、计费、账单、按请求计费、按用量计费、调用、执行时间、空闲、预配、虚拟机、冷启动、最小实例数、热实例、常驻、
  最小副本数、源代码、依赖、构建、部署、查询字符串、权限、调用方、公开访问、服务账号、角色、密钥、默认凭据、身份、
  工作负载、日志、预处理、推理、客户端、瘦客户端、解码、归一化、字节、张量、回滚、注册、导出、签名、模型服务器、
  经验法则、厂商锁定。
- **比喻按意思译，一个比喻一个词**：时间条、计价器、金色阴影、门、工牌、齿轮、配方、插头 / 插座。
- **分清容易混的词**：web 应用的 `serve` 命令不是考题对 serving function 的叫法 serve；`batch` 命令不是 serving function
  接收的“一批字符串”；job 不写“任务”（任务超时是控制台字段 Task timeout，“任务”留给第 8 讲的微调任务和第 13 讲的
  训练任务）；“谁能调用”（公开访问）和“以谁的身份运行”（服务账号）是两扇门，部署者的 Service Account User 是第三个
  箭头；function 一律是“函数”，产品名照写。
- **精确**：课件说法照课件（课件第 11 页、第 16 页），课件里的 Cloud Functions 现在叫 Cloud Run functions；数字照画面
  （8080、5 分钟、224 乘 224、四个概率）；README 没做的事明说（这个 README 没有用 Cloud Scheduler）；思考题的引子只问
  不答，揭晓以字母开头（选 B，……；先试 B）；课程的练习题从不引用。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、存储桶、服务（service）、作业（job）、无服务器（serverless）、
  端点（endpoint）。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| serverless | serverless（字幕）；无服务器（书面） | 无服务器 |
| Cloud Run service | Cloud Run service（字幕）；服务（书面） | 服务 |
| Cloud Run job | Cloud Run job（字幕）；作业（书面） | 任务（易混） |
| entry point | 入口点 | 入口函数 |
| cold start | 冷启动 | 冷启动 |
| minimum instances | 最小实例数 | 最少实例数 |
| provisioned | 预配 | 预置、配置 |
| pay-per-use | 按用量计费 | 按需付费 |
| service account | 服务账号 | 服务帐户 |
| default credentials | 默认凭据 | 默认凭证 |
| endpoint | endpoint（字幕）；端点（书面） | 终端节点 |
| thin client | 瘦客户端 | 轻客户端 |
| serving signature | 签名；serving function | 服务签名 |
| roll back | 回滚 | 回退 |
| vendor lock-in | 厂商锁定 | 供应商锁定 |
