# 中文字幕说明

视频 *AC215 · Lecture 23 — Final deployment and review: Ansible on one EC2 server, then a commit that redeploys (follow-along: cheese-app-aws)*
（**AC215 · 第 23 讲：最终部署与课程回顾——用 Ansible 部署到一台 EC2 服务器，再让一次提交自动重新部署（跟练：cheese-app-aws）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 23 讲“Final Deployment and Review”的跟练视频，对照课件逐页讲解，
并照着教程仓库 [dlops-io/cheese-app-aws](https://github.com/dlops-io/cheese-app-aws) 的 README 从头到尾一步一步做，再读 README 没有提到的
`.github/workflows/ci_cd_aws.yml`（版本见 [`ASSETS.md`](../../ASSETS.md)：`main` @ `5950118`，唯一的分支，2026-11-08 仍是最新）。
课件讲的是 Google Cloud 版本（GKE、GCR、Pulumi、`/deploy-app`）；按系列决定，本片和第 15 讲一样跟 AWS 版走，并温和地逐一对照两边的名词：
Kubernetes 集群 → 一台 EC2 服务器，镜像仓库（registry）→ ECR，Pulumi → Ansible 的 playbook，服务账号密钥 → 访问密钥和密钥对，
关键词 → `/run-deploy-app`，Ingress → 前门的 nginx。分两部分：

- **第一部分（S01–S10）**：从一个谜题开始：这个仓库 39 个提交里有 33 个带着同一条提交信息 `/run-deploy-app`，有一次斜杠却倒向了另一边。
  然后是课上的总图换成 AWS 的说法；在 IAM 控制台建策略 `CheeseAppECRPolicy`、用户 `deployment-ac215-user`、访问密钥和 EC2 密钥对
  （README 的密钥对名字和代码要的 `ac215_2024` 有一个小出入）；一张图看懂 Ansible（inventory、playbook、play、task、模块、recap）；
  启动部署工具箱容器时的三个意外（Ubuntu 上 `sh` 是 dash、Helm 下载站点的证书、空的 `/secrets`）和那条没加引号的 `pip install`；
  挂载的 Docker socket 让镜像落在你笔记本上；用一个时间戳标签构建并推送三个镜像到 ECR；创建并置备（provisioning）一台 EC2 服务器；
  在一个 Docker 网络上启动五个容器（Chroma 的版本固定、`docker run -it`）；nginx 这扇唯一的前门（`/api/` 前缀为什么被去掉）。
- **第二部分（S11–S16）**：课上的 CI/CD 循环、持续交付和持续部署的区别；`ci_cd_aws.yml` 在一条提交信息上的两道筛子（`/run-` 和
  `/run-deploy-app`，以及开头那个反斜杠）；推送到你自己的私有 GitHub 仓库、四个仓库机密（secret）、runner 上做了什么；
  把一个镜像标签从 runner 一路跟到服务器上重新创建的容器；README 的删除命令其实什么也删不掉，所以给出完整的手动清理清单；
  最后把整门课的每一讲放回这台服务器上做回顾，以及五道自测题。

画面上的终端输出、代码面板、README 引文、示意的 AWS 控制台和 GitHub 页面、Ansible 的 recap 和各种标签（`your turn`、`extra`、
`illustration`、`erratum`、金色的费用标签、`Lecture 23 · slides …`）都是英文原样，方便你对照着敲。授课老师的名字从不出现在画面、
字幕、标题、章节名和简介里。

## 怎么录制的

录制机器没有 AWS 账号。笔记本上的每一步都是真实运行的（`assets/terminal/`，录于 2026-11-08，详见 [`ASSETS.md`](../../ASSETS.md)）：
clone、`docker-shell.sh` 的三个意外和修法、工具箱容器的构建、`ansible-playbook` 的语法检查和 inventory 图、nginx 路由在本机替身上的验证。
每条和 AWS 打交道的命令（`aws sts get-caller-identity` 和 README 里的每条 `ansible-playbook` 命令）都照 README 原样执行，一直到真实的第一个报错
（安全令牌无效、AWS was not able to validate the provided access credentials、UNREACHABLE），从不伪造成功的输出。AWS 控制台、服务器和
GitHub 页面是画面上标着 `illustration` 的示意图。账号 ID、密钥、地址和 ARN 只用占位符（`YOUR_ACCOUNT_ID`、`<aws-access-key-id>`）。

本讲会产生费用：EC2 实例、磁盘、公有 IP 地址、ECR 存储和 Bedrock 调用都会计费，服务器会一直计费，直到你手动删除；画面用金色标签标出
每个计费点，不写金额。课件和 README、README 和实际运行不一致的地方（README 没有 clone 这一步；密钥对的名字；第 6 步的标题写着 GCP；
第 9 步的换密钥要提前到第 8 步之前；`nginx.conf` 其实已经在仓库里；删除命令在调用 AWS 之前就失败了），以录到的为准，视频会温和地指出来。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l23-final-cicd.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l23-final-cicd.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l23-final-cicd_part1.*`、`_part2.*` | 上下两部分（S01–S10：手动部署；S11–S16：让一次提交来部署、清理与回顾），每部分有自己的视频和字幕文件 |
| `output/ac215-l23-final-cicd.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l23-final-cicd.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l23-final-cicd.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S10），`g2` 是第二部分（S11–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L23-final-cicd-deployment.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L23-final-cicd-deployment.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l23-final-cicd --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l23-final-cicd --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l23-final-cicd --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l23-final-cicd --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（136 段：第一部分 83 段，第二部分 53 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 360 句：213 + 147），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的和时间从句留在英文放的位置）。
SAY 为了让语音读对，把实物念成了单词（slash run deploy app、E C 2、U S East 1、T 2 large、docker shell dot S H、AC215 underscore 2024 dot pem、
ansible playbook, deploy docker images, dash i, inventory dot yaml、C I C D AWS dot yaml、cluster state equals absent……）；这些条目
（90 段：53 + 37）在 `en_display:` 里给出屏幕上的写法（`/run-deploy-app`、`EC2`、`us-east-1`、`t2.large`、`docker-shell.sh`、`ac215_2024.pem`、
`ansible-playbook deploy-docker-images.yml -i inventory.yml`、`ci_cd_aws.yml`、`cluster_state=absent`……），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名和路径、关键词和提交信息、策略名和用户名、
控制台标签、工作流的步骤名、recap 的计数）一字不改，比如 `aws sts get-caller-identity`、`chmod 400`、`bash docker-shell.sh`、
`docker system prune -a`、`ansible-playbook deploy-provision-instance.yml`、`/secrets/ac215_2024.pem`、`/mnt/disk-1`、`CheeseAppECRPolicy`、
`deployment-ac215-user`、`appnetwork`、Run Deployment Container、Secrets and variables、`fix typo /run-tests`、`update readme`。
旁白引用的终端原文按屏幕照抄（credentials file not found、redirection unexpected、Gathering Facts、AWS was not able to validate the provided
access credentials、UNREACHABLE、410 Gone、skipping），观众要在终端里找它们；旁白转述的照译（安全令牌无效、docker login 收到的是一个空密码）。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、push、pull、container、image、tag、port、registry、pipeline、shell、root、
socket、pin、job、runner、secret、action、run、playbook、provision，加上这一讲的 Ansible 结构词 play、task、inventory、hosts、recap、register、
extra vars，以及 EBS 的 volume；其余用中文标准术语（AWS 中文控制台和文档、中文 CI/CD 资料的译名）：IAM 用户、策略、AWS 托管策略、
访问密钥、私有访问密钥、密钥对、安全组、实例、系统映像（AMI，和容器“镜像”分开）、区域、公有 IP 地址、附加（磁盘）、终止（实例）、
停用（访问密钥）、模块、声明式、持续集成、持续交付、持续部署、发布、工作流、步骤、滚动更新。ECR 里的 repository 说“仓库”，
Git 的 repository 说 repo。视频里的比喻一个比喻一个词：徽章（访问密钥）、钥匙（密钥对）、两份密钥（笔记本上的这两样凭据，和 GitHub 的
secret 分开）、工具箱容器（toolbox）、筛子（工作流的两道条件）、前门（nginx）、发布按钮、保险库（GitHub 上存 secret 的地方）、
总图（课上的 map）、替身（本机代替服务器的 container）、一环（`&&` 串起来的一段）。

字幕检查不允许中文行里出现下划线名字、等号、大于号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：
`ci_cd_aws.yml` → ci cd aws.yml，`head_commit` → head commit，`cluster_state=absent` → cluster state 设为 absent，`DOCKER_TAG` → Docker tag 变量，
`AWS_SSH_KEY` → AWS SSH key，`NEXTAUTH_SECRET` → NextAuth secret，`EXTERNAL_IP` → external IP，`group_id` → group ID，`failed=0` → failed 为 0，
here-string（`<<<`）→ here string，`ansible>=9.0.0` 说成“大于号”“等号”。思考题（五道，带计时）只问不提示，揭晓时用题目自己的话回答。
标题、章节名和简介用书面语体（仓库、克隆、提交、推送、容器、镜像、镜像仓库（registry）、机密（secret）、置备（provisioning））。
双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| playbook / play / task | playbook / play / task | 剧本 / 同左 / 任务 |
| inventory / hosts / module | inventory / hosts / 模块 | 清单 / 主机组 / 同左 |
| recap / register / extra vars | recap / register / extra vars | 执行汇总 / 注册变量 / 额外变量 |
| provision | provision | 置备（provisioning）、配置 |
| toolbox (the deployment container) | 工具箱容器 | 部署容器 |
| IAM user / policy / AWS managed policy | IAM 用户 / 策略 / AWS 托管策略 | 同左 |
| access key / secret access key | 访问密钥 / 私有访问密钥 | 访问密钥 ID 和秘密访问密钥 |
| key pair / security group | 密钥对 / 安全组 | 同左 |
| instance / AMI (machine image) | 实例 / 系统映像 | 同左 / 亚马逊系统映像 |
| attach / terminate / deactivate | 附加 / 终止 / 停用 | 挂接 / 同左 / 同左 |
| ECR repository / registry | 仓库 / registry | 存储库 / 镜像仓库 |
| repository secret | secret | 仓库机密、密钥 |
| continuous delivery / deployment | 持续交付 / 持续部署（说 CI、CD 时照说） | 同左 |
| rolling update | 滚动更新 | 同左 |
