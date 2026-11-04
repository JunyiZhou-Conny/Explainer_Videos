# 中文字幕说明

视频 *AC215 · Lecture 10 — Connecting to the cloud: one key, three containers, one browser (follow-along: cheese-app-v0)*
（**AC215 · 第 10 讲：连接云端——服务账号（Service Account）认证、Docker 网络与 CORS（跟练：cheese-app-v0）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 10 讲“连接云端：网络、身份验证与存储”的跟练视频，
照着教程仓库 [dlops-io/cheese-app-v0](https://github.com/dlops-io/cheese-app-v0) 的 README（commit `cb6fb94`，2026-10-08）
从头做到尾，分两部分：

- **第一部分（S01–S09）**：从一个奶酪聊天机器人的三次调用和三个小谜题开始，画出贯穿全讲的地图（笔记本、两条 Docker 网络、
  三个服务、Google 那扇有人把守的门）；创建服务账号 `llm-service-account`，授予两个角色，下载 JSON 密钥；把密钥放进所有仓库之外的
  `secrets/` 目录，用绑定挂载送到容器里的 `/secrets`（以及 `.gitignore` 没有保护密钥的陷阱）；建 Docker 网络、跑起 ChromaDB，
  分块并向量化 11 本书；应用默认凭据（ADC）按顺序查找的三个位置，密钥怎样换成一小时有效的访问令牌；IAM 格子和 401 / 403 的区别；
  最后跑起 API 服务，修好 `api-service/docker-shell.sh` 第 14 行（网络已存在时脚本直接中断）。
- **第二部分（S10–S15）**：容器名靠 Docker DNS、浏览器只认 localhost，为什么两个地址不能互换；前端容器、`-p 3200:3000` 的两个端口号、
  端口号的三段，以及 `0.0.0.0` 为什么让这些端口也朝着你的 Wi-Fi；浏览器亲自串起的三个调用、origin、预检请求和 CORS 白名单；
  奶酪专家智能体（agent）和一个不属于你的微调模型（默认 endpoint 指向授课老师的项目，所以是 403）；`docker compose down`
  之后向量数据为什么还在、什么才会让它消失，下一讲的存储桶；收尾清单和回顾。

画面上的终端输出、代码面板、README 引文、示意控制台和浏览器、地图、ADC 梯子、IAM 格子、CORS 流程图和各种标签（`your turn`、`extra`、
`illustration`、`recorded`、金色的计费标签、`Lecture 10 · slides …`）都是英文原样，方便你对照着敲。画面上出现授课老师名字的地方遮成
‹instructor›，字幕里一律写“授课老师”。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-10-19/20，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
录制机器是一个全新、空白的 Docker 环境（`docker:29.8.2-dind`，代替装了 Docker Desktop 的笔记本），README 的每条命令按原样、按顺序运行；
README 里没有、但有助于理解的检查（`git log`、`tree`、第二次建网络、`docker ps`、`curl`、容器之间的名字解析、`docker network connect`、
一行 Python 的 ADC 检查等）在画面上标着 `extra`。

录制机器**没有 Google 账号**，而这一讲讲的正是凭据。所以：

- 本地的部分都是实录：clone、secrets 目录约定、Docker 网络、两个镜像的构建、ChromaDB、uvicorn、Next.js、端口、容器 DNS、CORS 和持久化。
- 每个需要真实 Google 凭据的步骤都录到它如实的失败为止（`DefaultCredentialsError`：找不到 `/secrets/llm-service-account.json`）。
  目录列表里出现的密钥文件是一个明显无效的替身，云端步骤之前就删掉了；视频在 S05 如实说明了这一点。
- 你自己跟着做时应当看到的成功结果（向量化和加载的输出、256 维的 embedding 等）标着 `recorded`，并注明出处（README 和代码本身的输出）；
  对话、智能体和微调模型的回答没有任何来源记录过原文，所以视频只讲该看什么，不放输出面板。
- 会变的版本号、计数和耗时，字幕里都加“录制时”（8248 和 14228 个 chunk、ChromaDB 1.0.0、170 个包大约三分钟、773 个包、Next.js 14.2.4）。

本讲的 embedding、对话、智能体和微调模型调用会向你自己的 GCP 项目计费：每个计费点都有金色标签，S14–S15 是完整的收尾清单。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l10-cloud-connect.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l10-cloud-connect.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l10-cloud-connect_part1.*`、`_part2.*` | 上下两部分（S01–S09：服务账号、密钥与挂载、向量数据库、ADC、IAM 和 API；S10–S15：地址与 Docker DNS、前端和端口、浏览器与 CORS、智能体与微调模型、什么能留下、收尾），每部分有自己的视频和字幕文件 |
| `output/ac215-l10-cloud-connect.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l10-cloud-connect.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l10-cloud-connect.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S09），`g2` 是第二部分（S10–S15）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，下载链接见
[`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令、真实输出和练习答案
在学习指南 [MLOps_Learning · guides/L10-cloud-connect-cheese-app-v0.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L10-cloud-connect-cheese-app-v0.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l10-cloud-connect --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l10-cloud-connect --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l10-cloud-connect --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l10-cloud-connect --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（90 段），`en` 和 SAY 逐字相同；`zh` 按
`explainer.voice.split_sentences` 切出的英文句子一句对一句（共 382 句），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件和时间从句留在英文放的位置）；
纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，把实物念成了单词（dash p, 3200 colon 3000、localhost 9000 slash docs、
dash v、slash secrets、llm-service-account dot json、set dash e、control C、dash dash rm）；这些句子（37 段）在 `en_display:` 里给出屏幕上的写法
（`-p 3200:3000`、`localhost:9000/docs`、`-v`、`/secrets`、`llm-service-account.json`、`set -e`、`Ctrl-C`、`--rm`），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、镜像 / 容器 / 网络 / collection 的名字、
地址和端口、服务账号名、角色名、控制台标签、错误信息、HTTP 状态码、请求头名字）一字不改；终端打印的结果也照原样写
（Name or service not known、Connection refused、pull access denied、DefaultCredentialsError、200 OK、Ready、Local）。
实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、pin、root、shell、container、image、port、host port、container port、
localhost、bind mount、bucket、API、ID、chunk、embedding、collection、agent、endpoint、hook，加上这一讲的 IAM、ADC、OAuth、API key、
bearer token、JSON Web Token、CORS、origin、Docker DNS、Wi-Fi；其余用中文标准术语（Google Cloud 和 MDN 的中文文档）：服务账号、密钥、
私钥、公钥、签名、凭据、应用默认凭据、访问令牌、元数据服务器、身份联合、最小权限、身份验证、授权、角色、挂载、回环地址、跨域、
预检请求、请求头、幂等、分块、向量化。身份验证（是谁）和授权（能做什么、在哪里）始终分开，绝不笼统地写“认证”；401 是没有有效的令牌，
403 是身份验证通过了、但授权失败了。

视频里的比喻按意思译，一个比喻一个词：房子（笔记本、每个容器）、街道（一个 Docker 网络）、电话簿（Docker DNS）、门（发布的端口）、
隧道（端口转发）、传送门（挂载）、工牌（服务账号）、令牌柜台和一小时有效的票（访问令牌）、白名单、通行证和保安（CORS）。
README 的小疏漏照英文的语气温和地说（统一说“一个小疏漏”），后面紧跟改法；`api-service/docker-shell.sh` 第 14 行是“这个 repo 里最大的疏漏，
不是你的错”。字幕检查不允许中文行里出现下划线名字，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：
`GOOGLE_APPLICATION_CREDENTIALS` → Google application credentials 这个变量，`GCP_PROJECT` → GCP project 这个变量，
`uvicorn_server` → uvicorn server。授课老师的名字从不出现在字幕、标题、章节名和简介里。双语字幕的英文原句就在中文下方，
所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| service account / badge | 服务账号 / 工牌 | 服务账号（Service Account） |
| key / JSON key / private key / public key | 密钥 / JSON 密钥 / 私钥 / 公钥 | 服务账号密钥 |
| credentials / application default credentials | 凭据 / 应用默认凭据，ADC | 应用默认凭据（ADC） |
| access token / bearer token / JSON Web Token | 访问令牌、令牌 / bearer token / JSON Web Token | 不记名令牌 / JWT |
| metadata server / federation | 元数据服务器 / 身份联合 | 工作负载身份联合 |
| authentication / authorization / grant | 身份验证 / 授权 / 授予 | 认证、鉴权 |
| role / permission / least privilege | 角色 / 权限 / 最小权限 | IAM 角色 / 最小权限原则 |
| bind mount / mount | bind mount / 挂载 | 绑定挂载 |
| network / Docker DNS / loopback | 网络 / Docker DNS / 回环地址 | 容器网络 / 容器名解析 / 本地回环 |
| publish a port / host port / container port | 发布 port / host port / container port | 端口映射 / 宿主机端口 / 容器端口 |
| origin / cross origin / preflight / guest list | origin / 跨域 / 预检请求 / 白名单 | 源 / 跨源 / 预检 / 允许的源 |
| CORS | CORS | 跨源资源共享 |
| idempotent | 幂等 | 同左 |
| chunk / embed / embedding / collection | chunk / 向量化 / embedding / collection | 分块 / 嵌入 / 嵌入向量 / 集合 |
| agent / fine-tuned model / endpoint | agent / 微调过的模型 / endpoint | 智能体 / 微调模型 / 端点 |
| storage bucket / prefix | bucket / 前缀 | 存储桶 / 对象前缀 |
