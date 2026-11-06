# 中文字幕说明

视频 *AC215 · Lecture 20 — Deployment: by hand, then Pulumi to a single VM (follow-along: cheese-app-v3)*
（**AC215 · 第 20 讲：部署——先手动把奶酪应用部署到一台虚拟机，再用 Pulumi 写成代码（跟练：cheese-app-v3）**）
是英文旁白，配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 20 讲“Deployment: Pulumi（部署）”的
跟练视频，对照课件逐页讲解，并照着 [dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3)（`main` @ commit `3ecef56`，
2026-11-05 用 `git ls-remote` 复核过，课程网站链接的就是 `main`，见 [`ASSETS.md`](../../ASSETS.md) “Which commit”）README 的
“Deployment to GCP (Manual)” 和 “Deployment to GCP (Single VM Instance)” 两节一步一步做。课件的概念决定讲什么，README 和实录决定
画面上演示什么；两边不一致的地方（箭头方向、课件画四个 container 而实际有五个、GCR 已经改名 Artifact Registry、课件把前端放在
port 80）视频会温和地指出来。分两部分，正好在 README 两节的分界处：

- **第一部分（S01–S08，手动部署）**：从“停掉前端，为什么 API 的地址也不通了”的谜题开始；用 Docker Hub 脚本构建并 push 三个 image
  （README 的 `<…>` 占位符原样敲会报 `syntax error`，以及更安全的 `--password-stdin`）；在控制台开一台 VM，两个勾加上的网络标记和
  默认防火墙；装 Docker、建目录、写入密钥、建 Docker 网络 `cheese-app-network`；依次启动向量数据库、一次性的加载器（载入 14,356 个
  chunk，以及 Chroma 其实存在 `/data` 的小疏漏）、API 和前端；最后让 nginx 作为唯一的公共入口：`location` 块和那个剪掉
  `/api-service` 前缀的结尾斜杠，`echo` 加单引号吃掉 `log_format` 的问题和 heredoc 的写法，然后揭晓谜题（nginx 只在启动时解析一次
  container 名字）。用“21 条命令：能重复、能审查、能撤销吗？”引出基础设施即代码，并先手动删掉这台 VM。
- **第二部分（S09–S16，Pulumi 部署到一台 VM）**：Pulumi 的循环（程序 → 期望状态 → 和 state、实际情况比较 → 计划 → provider），
  `preview` / `up` / `--refresh` / `-y`；第 1 步的四个 API、两个权限不同的服务账号和密钥，以及 README 漏掉的 Artifact Registry
  仓库；部署工具箱 container（录制当天它的 Dockerfile 需要两处一行修复：`bullseye` → `bookworm`，`google-cloud-sdk` →
  `google-cloud-cli`）；OS Login 和 SSH 密钥；第 2 步带时间戳的 image stack（每次 `up` 都重新构建）；第 3、4 步的 VM、围栏和防火墙门、
  provisioning 的命令链（`blkid` 先检查再 `mkfs`）；第 5、6 步通过 SSH 部署 container 和 nginx、stack reference、该把哪把密钥交给
  VM；最后 `pulumi destroy`、六项清理清单、六步和六条原则的回顾，以及第 21–23 讲的预告。

画面上的终端输出、代码面板、README 引文、示意控制台、示意图和各种标签（`your turn`、`extra`、`extra · recording only`、
`extra · not for you`、`extra · not in the README`、`extra · our spelling`、`extra · or edit the file`、`illustration`、`erratum`、
金色的计费标签、课件标签）都是英文原样，方便你对照着敲。课件标签只在重画的课件图还在画面上时出现。授课老师的名字从不出现在画面、
字幕、标题、章节名和简介里；未合并的课程组分支只在 `ASSETS.md` 里作为背景出现。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-05，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
第一部分在 VM 上的每条命令都录在一台全新的 Debian 12 替身机器上，从装 Docker 到 nginx 返回 200 OK、再到谜题的重现，从头到尾都是实录；
笔记本上的步骤也是实录：clone、Docker Hub 脚本的前端构建、部署工具箱的三次构建（两处一行修复前后）、工具版本检查、`ssh-keygen`。
README 里没有、但有助于理解的检查（`git log`、目录权限、Chroma 的心跳、几次 `curl`、`/status`）在画面上标着 `extra`。

录制机器**没有 Google 账号，也没有登录 Docker Hub**。所以：

- 每个云端步骤都录到它遇到的第一个如实的报错为止：`docker push` 的 access denied、工具箱入口脚本的 `invalid_grant`、
  `gcloud` 的 no active account、`pulumi` 的 `PULUMI_ACCESS_TOKEN must be set`、`up` 推送 image 时的 403 Forbidden、
  VM 那个 stack 在第 100 行查找 Ubuntu image 时的 `invalid_grant`。旁白随后说你自己的输出应该是什么。
- 为了还能展示 Pulumi 的 `stack init`、`config set` 和 `preview`，录制时用了本地 backend（`pulumi login --local`），标着
  `extra · not for you`：你用的是工具箱登录好的 state bucket。
- 控制台步骤是按 README 画出来的示意图；成功的 `pulumi up` 建出来的东西是照着代码画的，都标着 `illustration`。从不伪造成功。

本讲会在你自己的 Google Cloud 项目里创建计费的资源：第一部分的 VM 和磁盘，第二部分的 VM、两块磁盘、外部 IP、Artifact Registry
存储和 state bucket。每个计费点都有金色标签；S08 先删掉手动部署的 VM，S16 是完整的收尾清单。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l20-deployment-pulumi.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l20-deployment-pulumi.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l20-deployment-pulumi_part1.*`、`_part2.*` | 上下两部分（S01–S08：手动部署；S09–S16：用 Pulumi 部署），每部分有自己的视频和字幕文件 |
| `output/ac215-l20-deployment-pulumi.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l20-deployment-pulumi.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l20-deployment-pulumi.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S08），`g2` 是第二部分（S09–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L20-deployment-pulumi.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L20-deployment-pulumi.md)。
这一讲部署的应用就是第 18 讲 [`ac215-l18-apis-frontend`](../../../ac215-l18-apis-frontend/) 在本地跑起来的那个，术语沿用它的决定。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l20-deployment-pulumi --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l20-deployment-pulumi --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l20-deployment-pulumi --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l20-deployment-pulumi --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（155 段：第一部分 70 段，第二部分 85 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 351 句：152 + 199），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的、原因和时间从句留在英文放的位置）；
纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，把实物念成了单词（cheese app version 3、slash status、
dash dash version、A M D 64、N 2 D、gcp service dot json、nginx dot conf、E O F、dash y、dash i、Pulumi dot dev dot yaml、
deploy images、block ID、Control C……）；这些句子（76 段：31 + 45）在 `en_display:` 里给出屏幕上的写法（`cheese-app-v3`、`/status`、
`--version`、`AMD64`、`N2D`、`gcp-service.json`、`nginx.conf`、`EOF`、`-y`、`-i`、`Pulumi.dev.yaml`、`deploy_images`、`blkid`、
`Ctrl+C`……），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课一步步部署的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、目录、container / 网络 / image 的名字、
网络标记、角色名、API 名、控制台标签、终端打印的短报错）一字不改，比如 cheese-app-network、cheese-app-vector-db、api-service、
http-server、persistent-folder、conf/nginx、--password-stdin、--refresh、-y、organization/deploy-images/dev、Compute OS Login、
Storage Object Viewer、No such container、Compiled successfully、has no installation candidate、No credentialed accounts、
Created stack dev、403 Forbidden、200 OK。旁白转述的报错和结果译成中文（登录会失败、我们的没能创建、Pulumi 也没能登录）。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、container、image、tag、Dockerfile、port、bucket、registry、
push、pull、chunk、embedding、collection、shell、entrypoint、diff、release、VM、SSH，加上这一讲的 stack、state、config、provider、
backend（只指 Pulumi 的 state 后端）、stack reference、provisioning、trigger、staging、passphrase、heredoc、location、socket、scopes、
playbook；其余用中文标准术语（Google Cloud 中文控制台和文档、Docker / nginx 中文资料、Kubernetes 中文文档的译名）：虚拟机实例、
机器类型、磁盘、启动磁盘、外部 IP、网络、网络标记、防火墙、反向代理、服务账号、角色、密钥、访问令牌、项目、仓库（Artifact Registry
的）、软件源（apt 的）、基础设施即代码、期望状态、实际情况、计划、资源、构造函数、逻辑名、输出、声明式、单点故障。GCP 项目和
Pulumi 项目都是“项目”，Git 的是 repo，Artifact Registry 的是仓库。“幂等”不进字幕，说成“可以放心重跑”“跑两次也安全”。
视频里的比喻一个比喻一个词：唯一的公共入口（port 80 和 nginx）、剪刀（结尾斜杠）、电话簿（Docker 的名字解析，同第 4、10、18 讲）、
工具箱、替身、围栏和门、密封的信封（Pulumi 的输出）、多米诺骨牌（provisioning 的命令链）、管道（stack reference）、积木。

字幕检查不允许中文行里出现下划线名字、尖括号、加号、等号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：
`deploy_images` → deploy images，`deploy_single_vm` → deploy single VM，`retain_on_delete` → retain on delete，`instance_ip` →
instance IP，`docker_build.Image` → docker build Image，`log_format` → log format，`GCP_PROJECT` → GCP project 变量，
`PULUMI_ACCESS_TOKEN must be set` → Pulumi access token must be set，计划里的 `+ ~ - +-` → 加号、波浪号、减号、加减号，
README 的 `<…>` → 占位符 / 尖括号，`Ctrl+C` → Ctrl-C。手动部署的四个 stage 叫“第 1–4 阶段”，课上的六个 step 叫“第 1–6 步”，两套编号不混。
思考题（五道）一律以“想一想。”开头，题干不泄底。标题、章节名和简介用书面语体（容器、镜像、端口、虚拟机、镜像仓库、堆栈（stack）、
置备（provisioning））。双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| VM / VM instance / machine type | VM / VM 实例 / 机器类型 | 虚拟机 / 虚拟机实例 |
| network tag / firewall rule | 网络标记 / 防火墙规则 | 同左 |
| reverse proxy / location block | 反向代理 / location 块 | 同左 |
| service account / key / access token | 服务账号 / 密钥 / 访问令牌 | 同左 |
| registry / Artifact Registry repository | registry / Artifact Registry 仓库 | 镜像仓库 |
| infrastructure as code | 基础设施即代码 | 同左（IaC） |
| desired state / state / reality | 期望状态 / state / 实际情况 | 期望状态 / 状态 / 实际状态 |
| stack / config / backend | stack / config / backend | 堆栈 / 配置 / 状态后端 |
| provider / resource / output | provider / 资源 / 输出 | 提供方 / 资源 / 输出 |
| plan / preview / refresh / destroy | 计划 / preview / --refresh / destroy | 计划 / 预览 / 刷新 / 销毁 |
| stack reference | stack reference | 堆栈引用 |
| provisioning | provisioning | 置备 / 预配 |
| deployment toolbox | 部署工具箱 | 同左 |
| safe to run twice | 跑两次也安全 | 幂等 |
| single point of failure | 单点故障 | 同左 |
