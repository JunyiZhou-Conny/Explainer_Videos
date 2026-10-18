# 中文字幕说明

视频 *AC215 · Lecture 4 — Containers II-b: build or pull, ports and Compose (follow-along: mega-pipeline
flexible-workflow, port_toy)*（**AC215 · 第 4 讲：容器 II-b——构建还是拉取、端口与 Compose（跟练：mega-pipeline
flexible-workflow、port_toy）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 4 讲的跟练视频，分两部分：

- **第一部分**照着 [dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) 的 `flexible-workflow`
  分支：克隆这个分支，或者把第 3 讲的克隆切过去（`git stash -u` 解决第二次拒绝）；建立自己的服务账号、密钥和
  存储桶，弄清一次调用要过的三道关卡（密钥、角色、API）；读懂 `docker-shell.sh` 的四种模式和两个绑定挂载；
  分清在本地构建镜像和从 Docker Hub 拉取镜像，看懂 `run` 为什么会交给你一个 2025 年 2 月的 Python 3.8 镜像，
  以及怎样不让旧密钥混进镜像。
- **第二部分**照着 [dlops-io/port_toy](https://github.com/dlops-io/port_toy)：每个容器都有自己的 `localhost`，
  在自建网络上靠名字互相找到；发布的端口、监听的端口和临时源端口各是什么，`-p 127.0.0.1:8090:9100` 的三段
  怎么读；改宿主机端口、改容器端口，只靠配置修好；最后用 Docker Compose 跑同一个应用，并分清 Ctrl+C、`down`、
  `up -d` 和 `up -d --build`。

画面上的终端输出、代码面板、README 引文、标签（`your turn`、`extra`……）、进度条和示意控制台都是英文原样，方便你
对照着敲；只有旁白译成了中文。录制时没有 Google 账号：凡是调用 Google 的步骤，画面展示命令、缺少密钥时的真实
报错，以及有密钥时该看什么。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿都在 Git 里。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l04-flexible-workflow-ports.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l04-flexible-workflow-ports.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l04-flexible-workflow-ports_part1.*`、`_part2.*` | 第一部分（S01–S09，mega-pipeline）和第二部分（S10–S16，port_toy），各有自己的视频、字幕和章节文件 |
| `output/ac215-l04-flexible-workflow-ports.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l04-flexible-workflow-ports.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l04-flexible-workflow-ports.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文（字幕用；g1 = 第一部分 S01–S09，g2 = 第二部分 S10–S16；共 156 段旁白、372 句）。`en_display:` 是英文字幕行的显示形式：旁白把命令念成单词的地方（dash p、slash app、Control C），英文行换回屏幕上的写法（`-p`、`/app`、`Ctrl+C`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器读取） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L04-containers-2b-flexible-workflow-ports.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L04-containers-2b-flexible-workflow-ports.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l04-flexible-workflow-ports --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l04-flexible-workflow-ports --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l04-flexible-workflow-ports --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在英文切分的地方切分中文。
所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文听起来差不多。

## 译文风格

按中国 MLOps 助教带实验课的说法，和第 1–3 讲一致：

- **一字不改**：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、分支 / image / 网络 / container 的名字、
  Compose 的键、环境变量、IAM 角色名、报错原文、README 章节标题、屏幕上的标签）。字幕检查器不收的几种写法例外：
  带下划线的名字按旁白的念法写成空格（transcribe audio 目录、port toy、depends on 这个键），`Ctrl+C` 写成 Ctrl-C，
  `chmod +x` 说成“用 chmod 加上可执行权限”；英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，第 1 讲的 VM、venv、shell、root、repo、clone、commit、import、pin，
  第 2、3 讲的 container、image、Dockerfile、base image、registry、tag、push、pull、bucket、pipeline、bind mount、
  prompt（只指 LLM 的 prompt），这一讲新增 port（host port、container port）、localhost、stash、checkout、token
  （只指 LLM 的 token）、assert。
- **其余用中文标准术语**：构建、层、缓存、挂载、构建器、服务账号、密钥、访问令牌、角色、启用、网络、子网、地址、
  连接、数据包、发布、监听、映射、请求、回复、服务（Compose 的 service）、进程、信号、退出码、已跟踪 / 未跟踪 /
  被忽略。
- **比喻按意思译，一个比喻一个词**：配方、路标、窗、盒子、三堆和墙、关卡、小电脑、局域网、电话簿、导轨、临街的门
  （host port）和房间（container port）。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、克隆、拉取、推送、存储桶、端口。
- 双语字幕的英文原句就在中文下方，所以中文行不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| container / image | container / image（字幕）；容器 / 镜像（书面） | 容器 / 镜像 |
| port / host port / container port | port（字幕）；端口、宿主机端口、容器端口（书面） | 端口、主机端口 |
| publish a port / listen | 发布 / 监听 | 暴露端口 |
| ephemeral (source) port | 临时 port；临时源端口（书面） | 临时端口、短暂端口 |
| bind mount | bind mount（字幕）；绑定挂载（书面） | 绑定挂载 |
| registry | registry（字幕）；镜像仓库（书面） | 注册表 |
| service account | 服务账号 | 服务帐号 |
| access token | 访问令牌 | 访问令牌、token |
| gracefully stopping | 优雅地停止 | 优雅停止、平滑关闭 |
| user-defined network | 你自己创建的网络 | 用户自定义网络 |
