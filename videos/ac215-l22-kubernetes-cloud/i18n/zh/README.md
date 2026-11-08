# 中文字幕说明

视频 *AC215 · Lecture 22 — Scaling: Kubernetes in the cloud (follow-along: cheese-app-v3)*
（**AC215 · 第 22 讲：扩展——云上的 Kubernetes，先手动体验一个测试集群，再用 Pulumi 把奶酪应用部署到 GKE（跟练：cheese-app-v3）**）
是英文旁白，配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 22 讲“Scaling: Kubernetes (cloud)（扩展）”的
跟练视频，对照课件逐页讲解，并照着 [dlops-io/cheese-app-v3](https://github.com/dlops-io/cheese-app-v3)（`main` @ commit `3ecef56`，
录制当天 2026-11-07 没有变化，课程网站链接的就是 `main`，见 [`ASSETS.md`](../../ASSETS.md) “Which commit”）README 的
“Create Simple Kubernetes Cluster Tutorial”、“Deployment with Scaling using Kubernetes”、“Create & Deploy Cluster” 和
“Debugging Containers” 一步一步做。课件的概念决定讲什么，README 和实录决定画面上演示什么；两边不一致的地方（课件把运行时写成
Docker 而 GKE 用的是 containerd、课件只建一个节点而 README 建两个、Google Container Registry 已经关停、README 的虚线箭头方向、
README 的输出块比代码旧、调试命令里的 namespace 不存在）视频会温和地指出来。分两部分，正好在课件删除测试集群、转向 Pulumi 代码的地方：

- **第一部分（S01–S08，手动体验 Kubernetes）**：从“凌晨两点一个 API container 崩了，谁来重启它？”开始，引出故障转移、负载均衡和扩展
  三个诉求；编排工具和集群，控制平面（API server、etcd、调度器、控制器）和工作节点（kubelet、kube-proxy、containerd、Pod），
  kubectl 的语法；部署工具箱照提交的原样还是构建失败，需要和第 20 讲一样的两处一行修复（`bullseye` → `bookworm`，
  `google-cloud-sdk` → `google-cloud-cli`，加上 GKE 认证插件）；`gcloud container clusters create test-cluster`；在一个标注清楚的
  本地替身集群（kind，不是 GKE）上部署 tic-tac-toe：Deployment 和 Service、label 和 selector、外部 IP 一直 pending 的原因、
  被删掉又自己回来的 Pod、`kubectl scale`、集群 DNS、namespace 和 `-n`；最后删除测试集群。
- **第二部分（S09–S16，用 Pulumi 把奶酪应用部署到 GKE）**：从第 20 讲的一台 VM 一块一块对到集群上（Deployment、加载器 Job、带 DNS 名字的
  Service、两个 PVC、Ingress controller、Workload Identity、私有网络和 Cloud NAT、一到两个节点的节点池）和它的费用；两个服务账号和
  README 漏掉的两个一次性步骤；images stack 和 stack reference；`deploy_k8s` 的 config、23 个资源的计划和 `pulumi up` 的创建顺序；
  跟着一次点击从 `sslip.io` 经过云负载均衡器和 nginx Ingress controller 走到 Pod，以及为什么裸 IP 返回 404；用 `get-credentials`
  重新连上集群，用 kubectl 查看应用、进到 Pod 里；README 调试命令的两处修正；Pod 和节点两层扩展、资源请求（requests）、Pending 和
  自动扩缩器，以及为什么挂着磁盘的 API 不能随便扩；最后 `pulumi destroy`、清点残留资源和回顾。

画面上的终端输出、代码面板、README 引文和 expected 面板、示意控制台、示意图、三个诉求的勾选卡片、kubectl 语法卡片和各种标签
（`your turn`、`extra`、`extra · not for you`、`extra · our spelling`、`stand-in: kind, not GKE`、`illustration`、`erratum`、
`at the time of recording`、金色的计费标签、课件标签）都是英文原样，方便你对照着敲。课件标签只在重画的课件图还在画面上时出现。
授课老师的名字从不出现在画面、字幕、标题、章节名和简介里；未合并的课程组分支只在提交的文字里写作 `work/‹staff›`。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-07，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出：
部署工具箱照原样构建失败、两处修复后大约 92 秒构建成功，README 里的每条 gcloud、Pulumi 和 kubectl 命令都在工具箱的提示符下敲过。

录制机器**没有 Google 账号，也没有任何凭据**。所以：

- 每个需要 Google 的步骤都录到它遇到的第一个如实的报错为止：`gcloud` 的 no active account、`pulumi` 的
  `PULUMI_ACCESS_TOKEN must be set`、`pulumi up` 在第一个资源（网络）上的 `invalid_grant: account not found`。旁白随后说你自己的输出应该是什么。
- 为了还能展示 Pulumi 的 `stack init`、`config` 和 `preview`，录制时用了本地 backend，标着 `extra · not for you`；`deploy_k8s` 的
  真实计划（`+ 23 to create`）是在一个带占位 tag 的替身 images stack 上算出来的，什么都没构建。
- kubectl 的热身和调试命令在笔记本 Docker 里的一个 kind 集群（一个控制平面、两个工作节点）上原样运行，画面标着
  `stand-in: kind, not GKE`：它没有云负载均衡器、节点池、自动扩缩器和 Workload Identity。
- 控制台步骤和成功的 `pulumi up` 建出来的集群是照着 README 和代码画的示意图，标着 `illustration`。从不伪造成功。

本讲会在你自己的 Google Cloud 项目里创建按小时计费的资源：第一部分的测试集群，第二部分的区域集群、一到两个节点、负载均衡器、
NAT 网关和两块磁盘（按我们的估算大约每天 5 到 8 美元）。每个计费点都有金色标签；S08 删掉测试集群，S16 是 `pulumi destroy`
和清点残留（集群、转发规则、名字里带 `pvc` 的磁盘、防火墙规则、registry 里的 image）。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l22-kubernetes-cloud.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l22-kubernetes-cloud.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l22-kubernetes-cloud_part1.*`、`_part2.*` | 上下两部分（S01–S08：手动体验 Kubernetes；S09–S16：用 Pulumi 部署到 GKE），每部分有自己的视频和字幕文件 |
| `output/ac215-l22-kubernetes-cloud.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l22-kubernetes-cloud.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l22-kubernetes-cloud.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S08），`g2` 是第二部分（S09–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L22-kubernetes-cloud.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L22-kubernetes-cloud.md)。
这一讲部署的应用和工具箱就是第 20 讲 [`ac215-l20-deployment-pulumi`](../../../ac215-l20-deployment-pulumi/) 用过的那些，术语沿用它的决定。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l22-kubernetes-cloud --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l22-kubernetes-cloud --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l22-kubernetes-cloud --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l22-kubernetes-cloud --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（151 段：第一部分 76 段，第二部分 75 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 333 句：169 + 164），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文保持英文的分句顺序（条件、目的、原因和时间短语留在英文放的位置，
比如“可以跳过，如果你在第 20 讲做过”“缩回 1 个，等你用完以后”）；纯中文字幕每行最多 22 个单位、每条最多两行。SAY 为了让语音读对，
把实物念成了单词（test cluster, two nodes、us east 1 c、dash f、dash n、cheese app namespace、run web、vector db、
web dot default dot svc dot cluster dot local、deploy k8s、setup containers、ip address、app URL、ROOT PATH、slash api service、
pod name、plus 23……）；这些句子（53 句：20 + 33）在 `en_display:` 里给出屏幕上的写法（`test-cluster --num-nodes 2`、`us-east1-c`、
`-f`、`-n cheese-app-namespace`、`run: web`、`vector-db`、`web.default.svc.cluster.local`、`deploy_k8s`、`setup_containers.py`、
`ip_address`、`app_url`、`ROOT_PATH`、`/api-service`、`<pod-name>`、`+ 23 to create`……），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课一步步把应用部署到 Kubernetes 的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、目录、
Kubernetes 对象名、namespace、label、image 名、集群名、可用区、状态词、终端打印的短报错）一字不改，比如 kubectl get pods、
gcloud container clusters get-credentials cheese-app-cluster、-n cheese-app-namespace、run: web、vector-db、cheese-app-ingress、
us-east1-c、Pending、Running、Completed、connection refused、No credentialed accounts、Created stack dev、
NoneType object is not subscriptable、404 Not Found、200 OK。

实验课上本来就说英文的词保留英文：前几讲的 repo、commit、container、image、tag、Dockerfile、port、registry、bucket、push、shell、
VM、SSH、stack、state、config、provider、backend、stack reference，加上这一讲的 Pod、Deployment、ReplicaSet、Service、Job、Ingress、
Ingress controller、PVC、kubectl、Helm、kubeconfig、namespace、label、selector、requests、API server、etcd、kubelet、kube-proxy、
dispatcher、Workload Identity；其余用中文标准术语（Kubernetes 中文文档和 GKE 中文控制台的译名）：编排工具、集群、节点、工作节点、
控制平面、调度器、控制器、节点池、副本、期望状态、自愈、故障转移、负载均衡、负载均衡器、扩展、自动扩缩器、私有网络、子网、路由器、
NAT 网关、区域集群、外部 IP、主机名、服务账号、密钥、弃用警告。几组容易混的词分开说：Service（对象）和服务、Deployment（对象）和
部署（动作）、label 和画面上的标签、requests（资源请求）和 HTTP 请求、Pulumi 的 state 和集群的状态。stand-in 一律是“替身”，
README 里没有的 extra 一律是“额外”。视频里的比喻一个比喻一个词：大脑和双手（控制平面和 kubelet）、集群的记忆（etcd）、
恒温器（控制循环）、装对象的目录（namespace）、一扇门和门后的前台（负载均衡器和 Ingress controller）、计费表、指示灯。

字幕检查不允许中文行里出现下划线名字、尖括号、加号、等号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：
`deploy_k8s` → deploy k8s，`deploy_images` → deploy images，`setup_containers.py` → setup containers，`create_cluster.py` →
create cluster，`ip_address` → ip address，`app_url` → app URL，`ROOT_PATH` → ROOT PATH 变量，`--replicas=4` → replicas 设成 4，
`<pending>` → pending，`<pod-name>` → pod name 占位符，`+ 23 to create` → 要创建 23 个。思考题（五道）题干不泄底，答案在下一句旁白里。
标题、章节名和简介用书面语体（容器、镜像、仓库、虚拟机（VM）、堆栈（stack）、命名空间（namespace）、标签（label）、资源请求（requests））。
双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| orchestrator / cluster / node / worker node | 编排工具 / 集群 / 节点 / 工作节点 | 同左 |
| control plane | 控制平面 | 控制面 |
| scheduler / controller | 调度器 / 控制器 | 同左 |
| Pod / Deployment / ReplicaSet / Service / Job | 同左 | 同左（Kubernetes 中文文档也保留英文） |
| namespace | namespace | 命名空间 / 名字空间 |
| label / selector | label / selector | 标签 / 选择算符、选择器 |
| desired state / self-healing | 期望状态 / 自愈 | 同左 |
| replicas | 副本 | 副本数 |
| requests | requests | 资源请求 |
| node pool / autoscaler | 节点池 / 自动扩缩器 | 节点池 / 自动伸缩 |
| PVC (persistent volume claim) | PVC | 持久卷申领 |
| Ingress / Ingress controller | Ingress / Ingress controller | 入口 / 入口控制器 |
| failover / load balancing / scaling | 故障转移 / 负载均衡 / 扩展 | 同左 / 扩缩容 |
| Workload Identity | Workload Identity | 工作负载身份 |
| stand-in (kind cluster) | 替身 | 本地替代集群 |
