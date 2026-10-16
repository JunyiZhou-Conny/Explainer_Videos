# 中文字幕说明

视频 *AC215 · Lecture 2 — Containers I: one image, from laptop to VM (follow-along: simple-translate)*
（**AC215 · 第 2 讲：容器 I——一个镜像，从笔记本到 VM（跟练：simple-translate）**）是英文旁白，配中文字幕和中英双语字幕，
没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 2 讲的跟练视频：照着教程仓库
[dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) 的 README，在自己的笔记本上分五步写出
Dockerfile，构建并运行镜像，给它打标签、推送到 Docker Hub，最后在一台只装了 Docker 的 VM 上用一条命令把应用跑起来。
画面上的终端输出、代码面板、README 引文和各种标签（`your turn`、`extra`、`stand-in` 等）都是英文原样，方便你对照着敲。

录制时没有 Docker Hub 账号，也没有开云上的 VM：登录和推送成功的那几步发往本机的一个小镜像仓库（画面上标着
`stand-in`），真正推送到 Docker Hub 的那一步显示的是没有账号时的拒绝；VM 那几步在全新的 Debian 12 和 13 容器里录制。
你自己跟着做时，用你的 Docker Hub 账号和你自己的 VM。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l02-containers-1.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l02-containers-1.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l02-containers-1_part1.*`、`_part2.*` | 上下两部分（S01–S09：写 Dockerfile，构建并运行镜像；S10–S16：层、缓存、Docker Hub 与 VM），每部分有自己的视频和字幕文件 |
| `output/ac215-l02-containers-1.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l02-containers-1.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l02-containers-1.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S09），`g2` 是第二部分（S10–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，下载链接见
[`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单
和中文速览在学习指南
[MLOps_Learning · guides/L02-containers-1.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L02-containers-1.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l02-containers-1 --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l02-containers-1 --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l02-containers-1 --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l02-containers-1 --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（129 段），`en` 和 SAY 逐字相同；`zh` 按
`explainer.voice.split_sentences` 切出的英文句子一句对一句（共 377 句），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置；纯中文字幕每行最多 22 个单位、每条最多两行。
SAY 为了让语音读对，把实物念成了单词（dash dash rm、slash dot venv、docker dot I-O）；这些句子在 `en_display:` 里
给出屏幕上的写法（`--rm`、`/.venv`、`docker.io`），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、镜像名和包名、
Dockerfile 指令、终端原文和报错、README 章节标题）一字不改；实验课上本来就说英文的词保留英文：第 1 讲的 VM、venv、
shell、root、repo、clone、commit、pin，加上容器这几讲的 container、image、Dockerfile、base image、registry、tag
（打 tag）、push、pull、digest、socket、Docker daemon、attestation、locale、ID（和第 3 讲同一份清单）；其余用中文标准术语
（层、可写层、构建、构建上下文、构建器、缓存、指令、进程、内核、平台、模拟器、仓库、访问令牌、提示符、目录）。
字幕里不写“镜像”：它也是 Debian mirror 的日常叫法；标题、章节名、简介和这份说明这类书面文字才写容器、镜像、
基础镜像、镜像仓库、标签、推送、拉取。视频里的比喻一个比喻一个词：配方（Dockerfile）、配置卡片、货架（registry）、
包裹（构建上下文）、菜单（多平台 tag）、门（Docker socket）。

画面不翻译，所以旁白提到画面上的标签时，字幕照画面写（黄色的 your turn 标签、灰色的 extra 标签；第 1 讲当时写的是
“轮到你了”“额外”）。字幕检查不允许中文行里出现下划线名字、等号、尖括号和括号，所以几样实物在中文行里用文字描述，
英文行照常显示原样：`VIRTUAL_ENV` → virtual env 这个变量，`--platform=linux/amd64` → --platform 参数设成
linux/amd64，`exit()` → 带括号的 exit，`<USER NAME>/simple-translate-ac215` → 你的用户名/simple-translate-ac215。
README 的几处勘误照英文的语气温和地说（一个小疏漏、一个小缺口、一个小小的不一致），后面紧跟改法；会变的版本号和大小
每次都加“录制时”。双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| image / base image | image / base image | 镜像 / 基础镜像 |
| container | container | 容器 |
| layer / writable layer | 层 / 可写层 | 镜像层 / 容器层 |
| registry | registry | 镜像仓库、注册中心 |
| repository (Docker Hub) | 仓库 | Docker Hub 仓库、存储库 |
| tag / push / pull | tag（打 tag）/ push / pull | 标签 / 推送 / 拉取 |
| build context / builder | 构建上下文 / 构建器 | 构建上下文 / 构建器（buildx 是多平台构建器） |
| layer cache | 层缓存 | 构建缓存 |
| config card (ENTRYPOINT, CMD, ENV) | 配置卡片 | 镜像配置 |
| dangling images | dangling images | 虚悬镜像 |
| digest | digest | 摘要 |
| Docker daemon / socket | Docker daemon / socket | 守护进程 / 套接字 |
| a tag that points at a menu (manifest list) | 菜单 | 清单列表（manifest list） |
| attestation | attestation | 构建证明 |
| access token | 访问令牌（令牌） | 访问令牌 |
| emulator / emulated | 模拟器 / 模拟运行 | 仿真器 |
| locale | locale | 区域设置、语言环境 |
