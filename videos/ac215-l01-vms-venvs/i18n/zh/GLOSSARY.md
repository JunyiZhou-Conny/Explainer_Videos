# AC215 第 1 讲视频中文版词表（中英混用版）

视频：*AC215 · Lecture 1 — Virtual machines, virtual environments and uv (follow-along: simple-translate)*（`videos/ac215-l01-vms-venvs`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，英文技术文档读得很顺；第一次在云上开 VM，第一次弄清 import 去哪儿找包；边看边在自己的 VM 上敲命令  
语音：edge `zh-CN-XiaoyiNeural`（工具链默认；发布版走官方 Azure AI Speech，见 F1）；读音尚未实测，见 F5  
英文原稿：`script.md`（SAY 行是旁白，SHOW 行是画面）；`build/review_spoken.md` 第 16 条的建议已并入（改动见“关键决定”）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“开一台 VM”“SSH 进去”“把 repo clone 下来”“激活 venv”“uv sync 一下”“先看 traceback 的第一个错误”“把版本 pin 住”。硬译成“安全外壳登录”“克隆代码仓库”“同步命令”，反而像说明书。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端和控制台里找东西。命令、文件名、路径、包名、报错原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（虚拟机、虚拟环境、终端、提示符、命令、参数、目录、包、依赖、解释器、软链接、环境变量、管道、容器、镜像、限流）一律说中文；GCP 的概念（区域、可用区、机器类型、启动磁盘、外部 IP、结算、计费）用 GCP 中文控制台的官方译名，控制台是中文界面的同学也能对上。
- 双语字幕（中文在上，英文原句在下）已经把每个英文原词放在中文正下方，所以中文行不加英文括注。
- 读法也照中国工程师的习惯：“点 venv”“pyproject 点 toml”“点 local 斜杠 bin”“杠 m”“状态码四二九”“PEP 六六八”“Python 三点十三”。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文。观众是上 AC215 的中文研究生：英文技术文档读得很顺，平时就说“开一台 VM”“SSH 进去”“把 repo clone 下来”“激活 venv”“uv sync 一下”。每个选择过三关：实验课上的真实说法；GCP 中文控制台和中文技术文档里能搜到的标准中文名；普通话语音（edge zh-CN-XiaoyiNeural）读得对。（1）实物原样：观众要输入、要在屏幕上对照的东西（命令、参数、文件名、目录和路径、包名、环境变量和配置项、代码里的名字、终端原文和报错类名、英文控制台上的按钮和页面、README 的章节标题）在字幕和标签里逐字照抄，旁白用英文读，点读“点”、斜杠读“斜杠”、参数前缀读“杠”，/usr 照英文读 user；从不翻译、不变形、不加引号。终端输出、代码面板、README 引文、示意控制台保持英文，只翻译讲解。（2）跟着英文走：virtual machine → 虚拟机、VM → VM，virtual environment → 虚拟环境、venv → venv；另有一张封闭清单，是实验课上口头本来就说英文的词：shell、root、repo、clone、commit、import、traceback、lock 文件、pin、hypervisor，以及引用报错原文的 externally managed。（3）其余一律用中文标准术语：终端、提示符、命令、参数、目录、home 目录、包、软件包、依赖、包管理器、解释器、标准库、软链接、环境变量、管道、激活、隔离、解析、约束、范围、校验和、容器、镜像、接口、状态码、限流；GCP 概念用中文控制台的译名：区域、可用区、机器类型、启动磁盘、外部 IP、结算、计费。（4）视频自造的比喻按意思译，一个比喻一个词：架子（一层）、罐子、公用厨房和掌勺的、工具箱、门、愿望清单和购物小票、计价器、“约束不是 pin”。（5）读法按中国工程师的习惯：版本号按整数组读（三点十一点二），状态码、PEP 编号、课号逐位读（四二九、PEP 六六八、AC 二一五），都写进 say:。（6）双语字幕在中文下面放英文原句（念成单词的实物用 en_display 写回字面形式），所以中文行不加英文括注；只有三处字幕括注：hypervisor（虚拟机监控器）、externally managed（由外部管理）、外部 IP（也就是公网 IP）。（7）工具链的约束也是规则：每个英文句子对应一个中文句子（118 段、391 句）；锚点保持动画同步；显示和朗读不同时必须写 say:。大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **跟着英文走**：英文说 virtual machine / virtual environment，中文说虚拟机 / 虚拟环境；英文说 VM / venv，中文也说 VM / venv。S01 的“virtual 出现两次”在中文里正好是“虚拟”这个词出现两次。
- **实物原样，讲解用中文**：终端输出、提示符、代码面板（含注释）、README 引文卡、示意控制台的按钮和字段名、README 章节标题、文件名、路径、命令、包名在画面上一字不改；标签、标注、比喻、进度条的步骤说明、tag 用中文（A11、E2）。
- **点 / 斜杠 / 杠**：第 16 条建议 say: 用英文 dot / slash / dash，改为中国工程师的读法：. 读“点”（点 venv、pyproject 点 toml、sys 点 path），/ 读“斜杠”，参数前缀的 - 读“杠”（杠 t、ls 杠 a、python3 杠 m venv），名字里的连字符不读（simple translate、apt get、dist packages）。/usr 照英文旁白读 user（user local、user lib），因为下一句要解释“这个 user 拼作 usr”。第 16 条的显示形式（字幕 = 字面实物）全部保留，并补上 U-S-R（review_merge_log）。
- **版本号按整数组读**：3.11.2 读“三点十一点二”，3.10 读“三点十”，0.13.0 读“零点十三点零”。这是版本号的含义（3.10 比 3.9 新），也是 Python 圈的说法；edge 默认按小数读，所以每个版本号都写 say:（C2）。状态码、PEP 编号、课号逐位读：四二九、PEP 六六八、AC 二一五（C3）。
- **比喻**：shelf → 架子，单位“一层”（不是第 16 条的“书架”：书架上不放罐子，也和“公用厨房”不搭）；jar → 罐子；shared kitchen / cook → 公用厨房 / 掌勺的；toolbox → 工具箱，就是一个 venv 自己的那层架子，不另造第三样东西（第 16 条、review_pedagogy 第 18 条）；door → 门；wish list → 愿望清单；receipt → 购物小票，简称小票（不是第 16 条的“收据”：收据只证明付了钱，小票逐项列出买了什么、多少钱，正好对应 lock 文件逐个列出精确版本和校验和）；the meter → 计价器（出租车“打表”）。
- **约束不是 pin**：constraint → 约束，pin → pin（“pin 住”），因为紧接着的命令就叫 uv python pin，“把版本 pin 住”也是实验课原话。lock 文件的“锁定”和 pin 分开。pin 是合法拼音，必须先听（F5）。
- **四对容易撞车的词**：镜像只指容器镜像（Debian mirror 叫软件源）；目录只指文件夹（apt 的 package catalog 叫软件包列表）；包是 pip / uv 装的，软件包是 apt 装的；应用是概念，app 只是 pyproject.toml 里那个名字（A6）。
- **控制台**：概念用 GCP 中文控制台的译名；要点的按钮和页面照英文说（点 Create instance、点 SSH、点 Authorize、进 VM instances 页面），和示意控制台、README 的链接一致；中文界面对照只放进配套 README 和简介（H3）。
- **README 进度条**：章节标题保持 README 原文（观众要在 README 里找它）；说明行写“第 3 步，共 10 步：apt-get update”，额外命令加“ · 额外”（E3）。
- **勘误**：旁白说“一个小错误”，一定紧跟改法；标签写“勘误”。
- **报错原文**：externally managed、command not found、ModuleNotFoundError、requirement already satisfied 照原文说，前面加“报 / 显示 / 提示”；externally managed 首次字幕括注“由外部管理”。
- **只有三处字幕括注**：hypervisor（虚拟机监控器）、externally managed（由外部管理）、外部 IP（也就是公网 IP）。
- **读音未实测**：写这份词表的环境连不上 edge 的朗读服务（F5、I2），所以读音规则来自两份先例和中国工程师的读法，F5 列出了第一次合成后必须听的词和备用写法。

## 读音待实测清单（F5）

| 写法 | 风险 | 读错时的备用写法 |
|---|---|---|
| pin（约束不是 pin、pin 住） | 合法拼音 pīn，可能读成“拼” | 整片改说“固定版本”（约束不是固定版本；把它固定下来），S10 标签同改；不用“锁定”（那是 lock 文件的词） |
| 行（第 25 行、那一行、行号、最后一行） | 可能读成 xíng（早先的 Xiaoxiao 在差分隐私视频里常这样） | 代码第 25 行 / 那句输出 / 最后那句报错 |
| venv、README、PATH | 可能逐字母读 | lexicon.zh.yaml：venv → v env，README → read me，PATH → path |
| sudo、repo、curl | 可能读成拼音或逐字母 | sudo → soo doo；repo 改说“仓库”；curl 逐字母可接受 |
| gcloud、googletrans、googleapis、pyproject、toml、pyenv、pipx、uvx、MLOps、CPython | 读不顺 | say: 已写 g cloud；其余备用 google trans、google apis、py env、pip x、uv x、M L ops |
| python3、pip3 | 预计读“python 三”“pip 三”（正确） | 读成 three 也可接受 |
| Module Not Found Error | 驼峰拆词后应读对 | — |
| 三点十一点二、四二九、PEP 六六八、AC 二一五 | 汉字数字，预计稳定 | — |
| 两个依赖 | 显示“2 个”时会读“二个” | say: 已写“两个” |

## 术语表

“字幕 / 屏幕”是显示用的写法（中文字幕行和画面标签）；“朗读”是声音实际说的内容，写进 narration.yaml 的 `say:`，空白表示与显示相同。“首次出现”给出例句；只在字幕里出现的括注见 A3。


### 虚拟机、虚拟环境与容器 / VMs, virtual environments, containers

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| virtual machine / VM | 虚拟机（定义句、概念句）/ VM（具体那台机器、操作步骤、标签）；量词：一台 | 虚拟机 / VM | S01：虚拟机就是一整台你租来、用完就扔的电脑。S01 梯子：在云端 VM 上手动安装 | 跟着英文走（A2）：英文说 virtual machine 就说虚拟机，说 VM 就说 VM。实验课上“开一台 VM”“SSH 进 VM”“把 VM 删掉”都是原话；定义句和 S01 的“虚拟”双关要用虚拟机。标签优先用短的 VM。 |
| virtual environment / venv | 虚拟环境（定义句、概念句）/ venv（简称、操作语境）；量词：一个 | 虚拟环境 / venv | S01：虚拟环境就是给一个项目专用的一套 Python 包。S08：虚拟环境其实就是一个目录，通常叫 .venv | 跟着英文走：virtual environment → 虚拟环境，venv → venv。中国工程师两种都说（“建个 venv”“激活虚拟环境”）。不简称“虚拟”或“环境”：“环境”留给 externally managed 那个“环境”和环境变量。venv 的读音待实测（F5）。 |
| hypervisor | hypervisor（首次字幕括注：虚拟机监控器） | hypervisor | S03：有一种软件叫 hypervisor（虚拟机监控器），它把这台机器切成一片一片。V1 标签：hypervisor | 云计算圈口头就说英文；教材译名“虚拟机监控器”（VMM）只做一次字幕括注（A3），方便搜索。 |
| server / data center / slice of a server / virtual CPUs / memory / disk / storage network | 服务器 / 数据中心 / 一片（切出来的一块）/ 虚拟 CPU / 内存 / 磁盘 / 存储网络 |  | S03：虚拟机就是 Google 某个数据中心里，一台真实服务器切出来的一片。 | “磁盘”和 GCP 中文界面一致（启动磁盘、磁盘页面），不说“硬盘”。 |
| operating system / OS / OS tools / system libraries (C) / drivers / GPU drivers | 操作系统 / 系统工具 / 用 C 写的系统库 / 驱动 / GPU 驱动 |  | S08：有些东西 venv 隔离不了：操作系统、用 C 写的系统库，还有驱动。 | 标签 “OS tools” → 系统工具；“the operating system” 不缩写成 OS（旁白）。 |
| container / image / Docker / Dockerfile / Docker image | 容器 / 镜像 / Docker / Dockerfile / Docker 镜像；标签：容器 · 第 2 讲 | 容器 / 镜像 / Docker / Dockerfile | S15：这一层就是容器，下节课讲。S15：今天做的一切，都打包进一个镜像。 | 中文标准说法。“镜像”只指容器镜像（Python 3.12 的镜像）：Debian 的 mirror、package source 叫“软件源”，GCP 的 OS image（旁白不出现）叫“系统映像”，免得撞车（A6）。 |

### 云控制台与计费 / Cloud console and billing

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| Google Cloud / GCP / console / project / Compute Engine / Compute Engine API / enable | Google Cloud（标签可写 GCP）/ 控制台 / 项目 / Compute Engine / Compute Engine API / 启用 | Google Cloud / 控制台 / 项目 / Compute Engine / Compute Engine API / 点 Enable | S03：在控制台里，先确认选中的是你在 Tutorial 0 建的项目，然后打开 Compute Engine，再进 VM instances。 | 产品名保持英文；控制台、项目、启用是 GCP 中文界面的叫法。要点的按钮照英文说（点 Enable，见下一条）。 |
| console buttons and pages: Create instance / VM instances / Disks / SSH / Authorize / Delete / Stop / Enable | 示意控制台上保持英文原样；字幕：点 Create instance / 点 SSH / 点 Authorize / 点 Delete / VM instances 页面 / Disks 页面 | 点 Create instance / 点 SSH / 点 Authorize / 点 Delete / VM instances / Disks | S03：点 Create，等绿勾出现，再点 SSH。要是让你授权这次连接，就点 Authorize。 | 要点的东西照英文说，和示意控制台、README 的链接一致：观众要找的就是这几个英文字样。中文控制台对照（创建实例、VM 实例、磁盘、授权、删除、停止、启用）只写进配套 README 和简介（H3），旁白不说。口头说“点”，书面写“点击”。 |
| instance / select your instance | 实例 |  | S07：选中你的实例，点 Delete，暂停视频，等它删完。 | GCP 中文界面：虚拟机实例。select your instance → 选中你的实例。 |
| name / region / zone / machine type / boot disk | 名称 / 区域 / 可用区 / 机器类型 / 启动磁盘 |  | S03：区域和可用区，就是这台机器实际放在哪里。机器类型决定 CPU 和内存，e2-small 就够用了。启动磁盘选 Debian 12。 | GCP（以及 AWS）中文文档和控制台的标准译名：region 区域、zone 可用区。旁白不说 region、zone（英文字幕行有）。示意表单的字段名保持英文（E2）。 |
| external IP (address) / Ephemeral / reserved IP address / static IP | 外部 IP（首次字幕括注：也就是公网 IP）/ 临时 / 预留的 IP 地址 | 外部 IP / 预留的 IP 地址 | S03：保留外部 IP（也就是公网 IP），它默认就是开着的。S07：预留的 IP 地址也一样一直在计费。 | “外部 IP”对应控制台的 External IPv4；中国工程师口头更常说“公网 IP”，字幕括注一次接上（A3）。 |
| billing / a project with billing on / billed by the second / charging / costs money / estimate | 结算（开通了结算的项目）/ 计费（按秒计费）/ 在花钱 / 费用估算 |  | S01：一个开通了结算的 Google Cloud 项目。S03：CPU 和内存在 VM 运行期间按秒计费，闲着也照样算。 | GCP 中文界面把 Billing 叫“结算”（结算账号）；“计费”是动作。旁白不说 billing。 |
| the meter / cost meter / the meter starts / never stops on its own / stops where it is | 计价器（金色表盘）；计价器开始跳了；自己不会停；停在原处 |  | S03：从这一刻起，计价器就开始跳了。 | 出租车“打表”的计价器：只要 VM 还在，表就在走。表盘没有数字，所以不说具体金额。 |
| Stop vs Delete / delete, don't stop | 停止 / 删除；章节：要删除，别只停止 |  | S07：为什么要删除，而不只是停止？ | 停止 = 关机，磁盘还在，还在计费；删除 = 连启动磁盘一起没了。 |
| SSH / SSH in / SSH window / SSH session / authorize the connection | SSH / SSH 进去 / SSH 窗口 / SSH 会话 / 授权这次连接 | SSH / SSH 进去 / SSH 窗口 | S03：然后点 SSH……浏览器里会打开一个终端，已经登录到你的新 VM 上了。 | 按字母读；不译“安全外壳”。 |
| gcloud / the gcloud tool / gcloud compute instances list / gcloud compute disks list | gcloud 命令行工具 / gcloud compute instances list / gcloud compute disks list | g cloud 命令行工具 / g cloud compute instances list / g cloud compute disks list | S07：如果你笔记本上装了 gcloud 命令行工具，两条额外的命令也能做同样的检查。 | say: 写 g cloud（中国工程师读 G cloud；连写的 gcloud 读音没把握）。 |
| Tutorial 0 / service account / keys / a web browser / laptop | Tutorial 0 / 服务账号 / 密钥 / 浏览器 / 笔记本电脑（口语：笔记本） | Tutorial 0 / 服务账号 / 密钥 / 浏览器 / 笔记本 | S01：开始之前，先做完 Tutorial 0。今天不用服务账号，也不用密钥，有个浏览器就行。 | Tutorial 0 是课程里的名字，照写；服务账号是 GCP 中文界面的译名。 |

### 终端、shell 与 apt / Terminal, shell and apt

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| terminal / command / one-liner / output / type / press enter | 终端 / 命令 / 一行命令 / 输出 / 输入 / 按回车 |  | S04：第 3 步：输入 sudo apt-get update。 | type → 输入（不用“键入”）；one-liner → 一行命令。 |
| shell / child shell / subshell / parent shell / reload your shell / this shell only | shell / 子 shell / 父 shell / 重新加载 shell / 只对当前这个 shell 有效 | shell / 子 shell / 父 shell | S09：安装脚本最后几行和第 8 步给了两个办法：重新加载 shell，或者 source 一下 env 文件。 | 中国工程师只说 shell（“外壳”“壳层”没人用）。 |
| prompt / your prompt now starts with app / your username | 提示符 / 提示符以 app 开头 / 用户名 |  | S04：注意看提示符：冒号后面现在显示你所在的目录。S12：你的提示符现在以 app 开头，外面带括号。 | 提示符 ≠ 提示（hint）。字幕写“以 app 开头，外面带括号”，不写 (app)，这样不用 say:。 |
| root / administrator / full administrator rights / sudo / run as administrator | root / 管理员 / 管理员权限 / sudo | root / 管理员 / sudo | S01：它是我们的，而且我们有 root 权限，也就是完整的管理员权限。S04：sudo 让它以管理员身份运行。 | root、sudo 照说；full administrator rights → 完整的管理员权限，run as administrator → 以管理员身份运行。sudo 的读音待实测（F5）。 |
| apt / apt-get / package manager | apt / apt-get / 包管理器 | apt / apt get / 包管理器 | S04：Debian 的包管理器是 apt，sudo 让它以管理员身份运行。S04：其中 apt-get 稳定、适合写进脚本，用在 Dockerfile 和自动化构建里；短一点的 apt 手敲起来更友好。 | say: 里 apt-get 写 apt get（名字里的连字符不读，F3）。 |
| package catalog / list of packages that exist / Debian package / package sources / Debian mirrors | 软件包列表 / 软件包 / 软件源；标签：Debian 软件源 |  | S04：而 update 会下载软件包列表：有哪些包、各自最新是什么版本。在 Google 的 VM 上会多几行，那是 Google 自己的软件源。 | apt 管的叫“软件包”。catalog 不译“目录”（目录 = 文件夹），mirror 不译“镜像”（镜像 = 容器镜像），见 A6。 |
| home folder / home directory / ~ / the wavy tilde | home 目录 / ~ / 波浪号；标签：~ = 你的 home 目录 | home 目录 / 波浪号 | S04：这个波浪号代表你的 home 目录。 | 实验课口语就说“home 目录”（也有人说家目录）。它和 /usr（系统的）是一对，见 A6。 |
| folder / directory / path (of a file) | 目录 / 路径 |  | S12：或者直接用路径调用 venv 里的 python。 | 终端语境一律说“目录”，不说“文件夹”；path → 路径；PATH 是环境变量名，不译。 |
| PATH / a list of folders called PATH / the first match / the PATH it started with | PATH / 一个叫 PATH 的目录列表 / 第一个匹配的 | PATH | S09：你输入一个命令，shell 就去一个叫 PATH 的目录列表里，从左到右找，运行第一个匹配的。 | 环境变量名，照写照说，绝不译“路径”。大写的 PATH 可能被逐字母读，待实测（F5，备用：lexicon.zh.yaml 改拼）。 |
| environment variable / a variable called virtual env | 环境变量 / VIRTUAL_ENV | 环境变量 / virtual env | S12：激活还会设置一个叫 VIRTUAL_ENV 的环境变量（say: virtual env）。 | 英文旁白说 variable，中文说“环境变量”，更准确也更常用。下划线不能进 say:（会读成“下划线”，check 会报）。 |
| source / sourcing / the env file / startup files | source（source 一下）/ env 文件 / 启动文件 | source / env 文件 / 启动文件 | S09：用 source 更快：它把那个目录放到 PATH 的最前面。 | source 是命令名，口语“source 一下”。.profile、.bashrc 统称“启动文件”。 |
| pipe / the vertical bar | 管道 / 竖线 |  | S09：这根竖线是管道：它把脚本直接交给 shell。 | 中文标准说法。 |
| curl / follow redirects / silent / still show errors / fail on HTTP errors / error page | curl / 跟随重定向 / 错误页面 | curl | S09：先用 curl 下载一个脚本：它会跟随重定向，安静运行但仍然显示错误，遇到 HTTP 错误就直接失败，而不是把错误页面交给 shell。 | S09 的说法：跟随重定向、安静运行但仍然显示错误、遇到 HTTP 错误就直接失败。curl 读音待实测。四个参数说明标签：-L 跟随重定向 / -s 静默 / -S 仍显示错误 / -f 遇到 HTTP 错误就失败。 |
| which / the which command / ls / cd / cat / os-release / os-release file | which / which 命令 / ls / cd / cat / os-release 文件 | which / which 命令 / ls / cd / os release 文件 | S03：这个 which 命令会告诉你，一个名字会运行哪个程序。 | 命令名照说；ls、cd 按字母读。 |
| git / repo / clone / commit / branch / git status / untracked | git / repo / 仓库（标签、章节名、文档）/ clone / 克隆（标签）/ commit / 提交（文档）/ 分支 / git status / 未跟踪 | git / repo / clone / commit / 分支 / git status / 未跟踪 | S04：第 5 步：把 repo clone 下来。S11：而 git status 说，uv.lock 还没被跟踪。 | 口头说 repo、clone、commit 是中国开发者的日常；书面（标签、章节名、文档）写仓库、克隆、提交（A4）。“untracked”用 git 中文界面的“未跟踪”。 |
| executable / not executable / run as a program | 可执行 / 不可执行 |  | S12：它本身都不是可执行的。 | run as a program → 当成程序运行。 |

### Python、包与 pip / Python, packages and pip

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| Python / system Python / python3 / plain python / CPython | Python / 系统 Python / python3 / 不带 3 的 python / CPython | Python / 系统 Python / python3 / python / CPython | S03：再问一下 python3 的版本。S06：输入 python3 cli.py，要带 3，因为这里没有不带 3 的 python。 | 系统 Python = Debian 自带、给操作系统自己用的那个 Python。python3 的读音预计是“python 三”，待实测。 |
| interpreter / a real interpreter / engine (metaphor) | 解释器 / 引擎（比喻） |  | S08：它通常不是拷贝，只是一个软链接，指向别处一个真正的解释器。 | 中文标准术语。a real interpreter → 一个真正的解释器。 |
| symlink / link (to a real interpreter) | 软链接（文档：软链接，即符号链接） | 软链接 | S08：……只是一个软链接，指向别处一个真正的解释器。S12：python，一个指向 uv 下载的那个 Python 的软链接。 | 英文旁白说 link，中文一律说“软链接”：单说“链接”像网页链接；“符号链接”是书面说法，写进文档。 |
| package / Python package / third-party package | 包 / Python 包 / 第三方包；量词：个 |  | S01：我们让 pip 装两个 Python 包，pip 拒绝了。 | pip 和 uv 装的是“包”；apt 装的是“软件包”（A6）。不说 package。 |
| dependency / dependencies / dependencies of their own / transitive dependency / dependency tree | 依赖 / 传递依赖（文档；也叫间接依赖）/ 依赖树 |  | S10：两个依赖：art，6.5 及以上；googletrans，正好是 4.0.2。S11：包自己也有依赖。 | 依赖 = pyproject.toml 里写的；包 = 实际装上的：“2 个依赖变成了 11 个包”。dependencies of their own → 包自己也有依赖。 |
| standard library / comes with Python | 标准库 / Python 自带 |  | S02：前两个 import，argparse 和 asyncio，是 Python 自带的。 |  |
| import / how Python finds an import | import（关键字，照写） | import | S05：想象一下 Python 是怎么找到 import 的东西的。 | 口头就说 import（“import 一下 googletrans”）；标签 import httpx 原样。 |
| pip / pip3 / python3-pip / Debian's own packaged copy of pip | pip / pip3 / python3-pip | pip / pip3 / python3 pip | S05：第 7 步：sudo apt install python3-pip。这是 Debian 自己打包的 pip，给 Debian 的 Python 用。 | Debian's own packaged copy of pip → Debian 自己打包的 pip。名字里的连字符不读（python3 pip）。 |
| sys dot path / the list called sys dot path / the folders Python searches | sys.path | sys 点 path | S05：这条额外的一行命令会打印一个叫 sys.path 的列表（say: sys 点 path）：也就是 Python 会搜索的那些目录。 | the folders Python searches → Python 会搜索的那些目录（不说“Python 要找的那些目录”：听起来像 Python 在找这些目录）。sys 的读音待实测（英文版 Kokoro 读成 siz）。 |
| site-packages / dist-packages | site-packages / dist-packages | site packages / dist packages | S08：通常的叫法是 site-packages；Debian 把系统的那几个叫 dist-packages。 | 目录名，照写；say: 去掉连字符。 |
| PEP 668 / the rule that makes pip respect it / the guard | PEP 668 / 保护机制 | PEP 六六八 / 保护机制 | S05：而 PEP 668 就是让 pip 遵守这一点的规则（say: PEP 六六八）。 | Python 圈把 PEP 编号逐位读（PEP 八、PEP 六六八），C3。 |
| externally managed / externally-managed-environment | externally managed（首次字幕括注：由外部管理）/ externally-managed-environment（标签照写） | externally managed | S01：报错说这个环境是 externally managed（由外部管理），还建议用虚拟环境。 | 引用报错原文，保留英文；字幕括注一次中文意思（A3）。S05“这就是 externally managed 的意思”不再括注。 |
| break-system-packages / the flag break-system-packages / overrides the guard | --break-system-packages（这个参数）/ 绕过保护 | break system packages 这个参数 | S05：第 8 步是 README 里的命令：sudo pip3 install，加上 --break-system-packages 这个参数。 | 参数照写；say: 不读前缀的两个杠，名字里的连字符也不读（英文旁白同样只说名字）。 |
| system-wide / shared by every user / for every program on the machine | 系统级 / 所有用户共用 |  | S05：在 user local 下面的 dist-packages 里，仍然是系统的，所有用户共用。 | for every program on the machine → 机器上的每个程序。 |
| shadowing / hide the one from apt / hidden | 遮蔽（标签）/ 挡住（旁白）/ 被挡住（标签 hidden） | 挡住 | S05：这时 Python 会先找到这一份，把 apt 那份挡住。标签：遮蔽 · 所有用系统 Python 的程序都受影响 | 旁白用口语“挡住”；标签和文档用术语“遮蔽”（变量遮蔽的同一个词）。 |
| clash / conflict / warning | 冲突 / 警告 |  | S05：警告说，以 root 身份运行 pip，可能会和系统的包管理器冲突。 |  |
| terminal messages: requirement already satisfied / command not found / ModuleNotFoundError | requirement already satisfied / command not found / ModuleNotFoundError（终端原文照写） | requirement already satisfied / command not found / Module Not Found Error | S05：如果你的输出里有 requirement already satisfied……S09：报 command not found。S13：报 ModuleNotFoundError。 | 观众在终端里看到的原文，照写照说，前面加“报 / 显示 / 提示”。驼峰名在 say: 里拆成单词。 |

### 虚拟环境与 uv / Virtual environments and uv

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| bin folder / a python inside / launchers from the packages | bin 目录 / 启动脚本 |  | S08：第一，一个 bin 目录，里面有个 python。 | launchers from the packages → 包带的启动脚本；a python inside → 里面有个 python。 |
| pyvenv.cfg / config file / include system site packages is false / home / prompt is app | pyvenv.cfg / 配置文件 / include-system-site-packages 是 false / home / prompt 是 app | pyvenv 点 cfg / 配置文件 / include system site packages 是 false / home / prompt 是 app | S08：第三，一个小小的配置文件，pyvenv.cfg。S12：还有配置文件：home 是真正解释器所在的目录，include-system-site-packages 是 false，prompt 是 app。 | 配置项名照写；屏幕上的 = 在字幕和 say: 里都说成“是”（B3）。 |
| activate / activation / the activate script / deactivate | 激活 / activate 脚本 / deactivate | 激活 / activate 脚本 / deactivate | S12：激活其实只改了 PATH。S12：再加一个叫 deactivate 的命令，把这些全部撤销。 | “激活虚拟环境”是中文通用说法；activate、deactivate 是脚本和命令名，照说。 |
| isolate / isolation / prove the isolation | 隔离 / 验证隔离 |  | S13：我们用几个额外命令来验证隔离。 |  |
| uv / uvx / uv sync / uv run / uv add / uv tree / uv python pin | uv / uvx / uv sync / uv run / uv add / uv tree / uv python pin | uv / uvx / uv sync / uv run / uv add / uv tree / uv python pin | S09：第 7 步一行命令就能装好 uv。S10：第 9 步是 uv sync。 | uv 按字母读 U V。命令名不翻译（不说“同步命令”），后面接中文名词：uv sync 这条命令、uv 自己的目录。 |
| the venv module / pip-tools / pyenv / pipx / python3 dash m venv | venv 模块 / pip-tools / pyenv / pipx / python3 -m venv | venv 模块 / pip tools / pyenv / pipx / python3 杠 m venv | S09：一个很快的工具顶了好几个：venv 模块、pip、用来锁版本的 pip-tools、用来装 Python 的 pyenv，还有 pipx。 | pyenv、pipx 读音待实测（英文版 Kokoro 把 pipx 读成 pips），备用 say: py env、pip x。 |
| pyproject.toml / requires-python / name | pyproject.toml / requires-python / name | pyproject 点 toml / requires python / name | S04：还有 pyproject.toml，列着这个应用需要什么。S10：第 6 行又是一个范围：Python 3.13 及以上。 | 文件名、键名照写；say: 写 pyproject 点 toml。 |
| uv.lock / lock file / a shared lock / a stale lock / the locked flag | uv.lock / lock 文件 / 共用的 lock 文件 / 过期的 lock 文件 / --locked 参数 | uv 点 lock / lock 文件 / locked 参数 | S04：也没有记录精确版本的 lock 文件。S11：在自动化构建里，给 uv sync 加上 --locked 参数，lock 文件缺失或过期，它就拒绝执行。 | 中国开发者说“lock 文件”（package-lock、poetry.lock 都这么叫）；统一用它，不用“锁文件”。动词用“锁定”（锁定精确版本），和 pin 分开（A6）。 |
| requirements file / requirements.txt | requirements 文件 / requirements.txt | requirements 文件 | S04：没有 requirements 文件，也没有记录精确版本的 lock 文件。 |  |
| resolve / resolved / resolving / resolver | 解析 / 解析了 13 个 / 依赖解析 / 解析器（文档） |  | S11：所谓解析，就是给依赖树里的每个包选定一个精确版本，而且这些版本要彼此兼容。 | 中文标准说法（依赖解析）。S02 的 parsed arguments 也叫“解析好的参数”，场景不同，不冲突；讲依赖时尽量说全“解析依赖”。 |
| constraint / range / exact / greater-or-equal / double equals / or newer / older than | 约束 / 范围 / 精确版本（一个版本）/ 大于等于 / 双等号 / 及以上 / 低于 |  | S10：大于等于表示一个范围；双等号表示一个确定的版本。 | “3.13 or newer”一律写“3.13 及以上”，“older than 3.15”写“低于 3.15”。 |
| pin / pin it / a constraint is not a pin / dot python version / the 3.13 series | pin（pin 住）/ 约束不是 pin / .python-version / 3.13 系列 | pin / pin 住 / 约束不是 pin / 点 python version / 三点十三系列 | S10：问题就在这儿：约束不是 pin。S10：想在哪儿都用同一个 Python，就把它 pin 住。 | 保留英文：紧接着的命令就叫 uv python pin，“把版本 pin 住”是实验课原话。pin 是合法拼音（pīn），可能被读成“拼”，必须人工听（F5）。lock 文件的“锁定”和 pin 分开（A6）。 |
| download addresses / checksums / exact version / plus sign | 下载地址 / 校验和 / 精确版本 / 加号 |  | S11：然后 uv 把它们写进一个新文件 uv.lock，连同下载地址和校验和。 |  |
| environment marker / only on Python older than 3.15 / skipped | 只在低于 3.15 的 Python 上 / 跳过；文档：环境标记（marker） | 只在低于三点十五的 Python 上 / 跳过 | S11：在 uv.lock 里，anyio 需要 typing-extensions，但只在低于 3.15 的 Python 上。 |  |
| deterministic / reproducible / idempotent / safe to re-run anytime | 确定下来 / 可复现 / 幂等（文档）/ 随时重跑都没问题 |  | S11：随时重跑都没问题。S15：怎样才能让 Python 版本确定下来？ | 旁白不说“幂等”（英文旁白也不说 idempotent）；README 原文和文档写“幂等（可以放心重复执行）”。 |
| pipenv / Pipfile / Pipfile.lock / pipenv install / pipenv sync / pipenv shell / exit | pipenv / Pipfile / Pipfile.lock / pipenv install / pipenv sync / pipenv shell / exit | pipenv / Pipfile / Pipfile 点 lock / pipenv install / pipenv sync / pipenv shell / exit | S14：而 pipenv shell 会在 venv 里开一个新的 shell。输入 exit 就能退出。 | 命令和文件名照写；标签 “a subshell · type exit to leave” → 子 shell · 输入 exit 退出。 |

### 应用、网络与报错 / The app, the network and errors

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| the app / cli.py / command-line app / main / main function | 应用 / cli.py / 命令行应用 / main 函数 | 应用 / cli 点 py / main 函数 | S02：在 GitHub 上打开 cli.py，待会儿你会把它 clone 到 VM 上。 | 概念说“应用”；app 只用于字面名字（name = "app"、提示符里的 (app)），两者不混。 |
| argparse / options / arguments / default / parsed arguments / Namespace | argparse / 选项 / 参数 / 默认值 / 解析好的参数 / Namespace | argparse / 选项 / 参数 / 默认值 | S02：最下面，argparse 定义了四个选项，每个都有默认值。 | argparse 的 options 用“选项”；命令行上的 flag 和打印出来的 arguments 用“参数”。 |
| dash t / dash s / dash d / dash f / ls dash a | -t / -s / -d / -f / ls -a | 杠 t / 杠 s / 杠 d / 杠 f / ls 杠 a | S06：杠 t 指定文本，杠 s 指定源语言，杠 d 指定目标语言。 | 中国工程师把参数前缀的 - 读“杠”。字幕显示真实参数。 |
| flag / the flag | 参数（这个参数） |  | S05：这个参数绕过了保护；sudo 让 pip 以管理员身份写文件。 | 不说 flag、开关。 |
| banner / ASCII art / AC215 | 横幅 / ASCII 字符画 / AC215 | 横幅 / ASCII 字符画 / AC 二一五 | S02：这个 main 函数先打印一个横幅，用 ASCII 字符画写着 AC215。 | 课号逐位读（C3）。 |
| event loop / asynchronous / an awaited call / Translator | 事件循环 / 异步 / 一次 await 调用 / Translator | 事件循环 / 异步 / await / Translator | S02：最后一行启动事件循环并运行 main，因为 googletrans 4 是异步的。 | googletrans 4 读 googletrans 四（像 Python 3、Vue 3 那样）。 |
| HTTPS request / web request / endpoint / unofficial / API key / JSON / no promises | HTTPS 请求 / 网络请求 / 接口 / 非官方 / API key / JSON | HTTPS 请求 / 接口 / API key / JSON | S02：这是 Google 非官方的翻译接口：免费，不用 API key，也不做任何保证。 | no promises → 不做任何保证。endpoint → 接口：中文工程师说“调接口”“这个接口”；不说“端点”（书面、生硬）。文档可写“接口（endpoint）”。 |
| translate dot googleapis dot com | translate.googleapis.com | translate 点 googleapis 点 com | S02：从 VM 发到 translate.googleapis.com 的一个 HTTPS 请求。 | 域名照写，say: 里点读“点”。 |
| status code / 429 / too many requests / rate-limiting / rate limit | 状态码 / 429 / 请求太多 / 限流 | 状态码 / 四二九 / 请求太多 / 限流 | S06：原因是状态码 429：请求太多。Google 的非官方接口在对我们的机器限流。 | HTTP 状态码逐位读（四零四、四二九，C3）。“限流”是中文工程师的标准说法。 |
| traceback / chained traceback / two errors / the cause / the wrapper / the last line / scroll up | traceback / 链式 traceback / 两个错误 / 原因 / 外层包装 / 最后一行 / 往上翻 | traceback / 链式 traceback | S06：这是一个链式 traceback：两个错误。V8 标签：1 · 原因 / 2 · 外层包装 | Python 的固定说法，屏幕上就是 Traceback，中文工程师照说。“链式”对应 Python 中文文档的“异常链”。 |
| error / exception / raise / catch / chained to the original / directly caused | 错误 / 异常 / 抛出 / 捕获 / 接在原来的错误后面 / 直接导致了 |  | S06：它什么错误都接住，再抛出一条更友好的消息，接在原来的错误后面。 | 错误 = 泛指（两个错误、第一个错误）；异常 = Python 的 exception；报错 = 屏幕上的出错信息（A6）。 |
| raise exception equals True / library default (False) | raise_exception=True / 库的默认值（False） | raise exception 等于 True | S02：第 25 行有个细节以后会用到：raise_exception=True。 | 代码原样显示（B3）；say: 里不能有下划线和等号。 |
| typo / x x / invalid destination language / the valid codes | xx / 语言代码 | x x | S06：这条额外的命令故意打错了：xx 不是一种语言。第一个错误说的是：目标语言无效。 | typo → 打错了；invalid destination language → 目标语言无效（意译，英文原文在画面上）；the valid codes → 有效的语言代码。 |
| English / Italian / Spanish / French / source language / destination language / translation | 英语 / 意大利语 / 西班牙语 / 法语 / 源语言 / 目标语言 / 译文 |  | S02：所以不带任何选项运行 cli.py，就会把 I love cheese 翻译成意大利语。 |  |
| I love cheese / the Input line / the Output line | I love cheese / Input 那一行 / Output 那一行 | I love cheese / Input 那一行 / Output 那一行 | S06：只要走到了 Input 那一行，import 就都成功了。 | 示例文本和输出前缀是程序真实的输入输出，照写照说。 |

### 读出来的路径、文件名和参数（review_spoken 第 16 条）/ Paths, files and flags spoken as words (review_spoken #16)

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| user local / user lib / U-S-R | /usr/local / /usr/lib；“这里的 user 拼作 usr” | user local / user lib / U S R | S05：版本是 pip 23.0.1，对应 Python 3.11，在 user lib 下面一个叫 dist-packages 的目录里。这里的 user 拼作 usr：是系统的文件，不是你的 home 目录。 | 照英文旁白读 user（Linux 圈常见读法），下一句再澄清拼写；字幕显示真实路径。绝不译“用户本地”“用户库”（这正是 review_pedagogy 第 7 条担心的误解）。 |
| dot venv / the dot venv folder | .venv / .venv 目录 | 点 venv / 点 venv 目录 | S10：然后它在 .venv 里建了一个虚拟环境。 | 中国工程师读“点 venv”；第 16 条建议的 dot venv 改为“点”。 |
| dot local slash bin | .local/bin（S09：你 home 目录下的 .local/bin）/ ~/.local/bin（标签） | 点 local 斜杠 bin | S09：把 uv 和 uvx 装到你 home 目录下的 .local/bin 里。 | “/”读“斜杠”。 |
| source dot venv slash bin slash activate | source .venv/bin/activate | source 点 venv 斜杠 bin 斜杠 activate | S12：第 10 步：source .venv/bin/activate。 |  |
| dot python version | .python-version | 点 python version | S10：会写一个小文件，叫 .python-version。 |  |
| python3 dash m venv | python3 -m venv | python3 杠 m venv | S08：它建议用 python3 -m venv，这是建 venv 的经典做法。 |  |
| the locked flag | --locked 参数 | locked 参数 | S11：在自动化构建里，给 uv sync 加上 --locked 参数。 | 长参数只读名字，不读两个杠（和英文旁白一致）。 |
| file names said as words: pyproject.toml / uv.lock / cli.py / pyvenv.cfg / Pipfile.lock | pyproject.toml / uv.lock / cli.py / pyvenv.cfg / Pipfile.lock | pyproject 点 toml / uv 点 lock / cli 点 py / pyvenv 点 cfg / Pipfile 点 lock | S06：输入 python3 cli.py。 | 文件名里的点读“点”（F3）。 |
| hyphenated names: simple-translate / apt-get / python3-pip / pip-tools / typing-extensions / e2-small / ac215-l01 | simple-translate / apt-get / python3-pip / pip-tools / typing-extensions / e2-small / ac215-l01 | simple translate / apt get / python3 pip / pip tools / typing extensions / e2 small / AC 二一五 L 零一 | S04：第 6 步：cd simple-translate。S03：名称，比如 ac215-l01。 | 名字中间的连字符不读；只有参数前缀的 - 读“杠”（F3）。 |

### 版本号、编号与数字 / Versions, codes and numbers

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| Python versions: 3.10 / 3.11 / 3.11.2 / 3.12 / 3.13 / 3.13.5 / 3.14 / 3.15 / 3.15.0 | 3.10 / 3.11 / 3.11.2 / 3.12 / 3.13 / 3.13.5 / 3.14 / 3.15 / 3.15.0 | 三点十 / 三点十一 / 三点十一点二 / 三点十二 / 三点十三 / 三点十三点五 / 三点十四 / 三点十五 / 三点十五点零 | S03：Debian 12 自带 Python 3.11.2（say: Python 三点十一点二），给操作系统自己用。 | 版本号按“整数组”读（C2）：3.10 比 3.9 新，读“三点十”，不读小数的“三点一零”。edge 默认按小数读，所以每个版本号都写 say:。 |
| package versions: 0.13 / 0.13.0 / 0.13.3 / 0.27.2 / 0.28 / 0.28.1 / 4.0.2 / 6.5 / 23.0.1 | 0.13 / 0.13.0 / 0.13.3 / 0.27.2 / 0.28 / 0.28.1 / 4.0.2 / 6.5 / 23.0.1 | 零点十三 / 零点十三点零 / 零点十三点三 / 零点二十七点二 / 零点二十八 / 零点二十八点一 / 四点零点二 / 六点五 / 二十三点零点一 | S05：我们的 googletrans 需要 0.27.2 及以上的 httpx（say: 零点二十七点二）。 | 同 C2。 |
| codes: 429 / PEP 668 / AC215 / Python 3 / googletrans 4 | 429 / PEP 668 / AC215 / Python 3 / googletrans 4 | 四二九 / PEP 六六八 / AC 二一五 / Python 三 / googletrans 四 | S06：原因是状态码 429（say: 四二九）。 | 编号逐位读（C3）。 |
| Step 3 / step 3 of 10 / line 25 / lines 32 to 37 | 第 3 步 / 第 3 步，共 10 步 / 第 25 行 / 第 32 到 37 行 |  | S02：第 32 到 37 行会接住那次调用的任何错误。 | 不用 say:（edge 能读“第 3 步”）；“行”是多音字，必须人工听（F6）。 |
| counts: 2 dependencies / 2 packages / installed 12 / installed 11 / resolved 13 / the other 9 / over a hundred packages | 2 个依赖 / 2 个包 / 装了 12 个 / 装了 11 个 / 解析了 13 个 / 另外 9 个 / 一百多个软件包 | 两个依赖 / 两个包（其余个数照显示，不写 say:） | S05：我们要了 2 个包，结果装了 12 个（say: 两个包）。 | 和终端、屏幕呼应的个数写数字（C1）；2 后面跟量词时 say: 写“两”（C4）。其余数字 edge 能读，可不写 say:。 |
| Debian 12 / Debian 13 / bookworm / Ubuntu 24.04 | Debian 12 / Debian 13 / 代号 bookworm / Ubuntu 24.04 | Debian 十二 / Debian 十三 / bookworm | S03：结果是 Debian 12，代号 bookworm。 | 发行版的大版本号按整数读（edge 自动）；Ubuntu 24.04 只在画面上。 |

### 视频自造的说法与比喻 / Phrases and metaphors of this video

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| the word virtual (used twice) / one will live inside the other | “虚拟”这个词 / 一个会装在另一个里面 |  | S01：今天这节课，“虚拟”这个词会出现两次。 | 双关在中文里自然成立：虚拟机、虚拟环境。 |
| ladder / rung / the first two rungs / four ways / a kind of fragility | 梯子 / 一级 / 前两级 / 四种方式 / 一类隐患 |  | S01：今天我们爬前两级。 | fragility 不译“脆弱性”（听起来像安全漏洞），用“隐患”。梯子四级标签：1 在 VM 上手动安装 / 2 同样的 VM，改用 uv / 3 Docker，在你的笔记本上 / 4 在 VM 上运行 Docker 镜像。 |
| quick and dirty / the clean way / messy | 简单粗暴 / 干净的做法 / 乱糟糟的 |  | S07：这就是简单粗暴的做法。 | “简单粗暴”是现成的中文对应。 |
| shelves / shelf / top shelf / bottom shelf / one shared shelf / jar / search-light | 架子（单位：层）/ 最上面一层 / 最下面一层 / 一层公用的架子 / 罐子 / 探照灯 |  | S05：把它们想成一层一层的架子。每次 import，Python 都从最上面一层往下找，拿第一个对上的。 | 第 16 条建议“书架”，改为“架子”：书架上不放罐子，也和“公用厨房”不搭。一层 = 一个 sys.path 目录。探照灯只在标签和文档里出现。 |
| shared kitchen / apt is the cook | 公用厨房 / 掌勺的是 apt；标签：公用厨房 |  | S05：系统 Python 是一间公用厨房，掌勺的是 apt。 | “掌勺的”比“厨师”更像中文的说法，也带出“谁说了算”。 |
| the last install wins, for everyone | 最后装的说了算，对所有人都一样 |  | S05：最后装的那个说了算，对所有人都一样，两个项目里总有一个会坏。标签：只有一层 · 最后装的说了算，所有人都一样 |  |
| toolbox / give each project its own toolbox | 工具箱 / 给每个项目一个自己的工具箱 |  | S08：解决办法是给每个项目一个自己的工具箱。这个工具箱，就是虚拟环境。 | 工具箱 = 一个 venv 自己的那层架子（第 16 条），不另造第三样东西；标签和旁白都用“工具箱”。 |
| Same engine, different toolbox | 引擎还是那个引擎，工具箱换了一个（标签：同一个引擎，不同的工具箱） |  | S08：引擎还是那个引擎，工具箱换了一个。 | 引擎 = 解释器（标签 interpreter → 解释器）。 |
| doors / knock on every door / the first door / walks in | 门 / 把每扇门都敲一遍 / 第一扇门 / 走进去 |  | S12：激活之前，python 把 PATH 里的每扇门都敲了一遍，什么也没找到。 | 标签 command not found 照写（终端原文）。 |
| wish list / receipt / why the receipt matters | 愿望清单 / 购物小票（简称小票） |  | S11：这个 pyproject.toml 文件是你的愿望清单。而 uv.lock 文件是购物小票。 | 第 16 条建议“收据”，改为“购物小票”：收据只证明付了钱；超市小票逐项列出买了什么、多少钱，正好对应 lock 文件逐个列出精确版本和校验和。 |
| Two wishes grow into a tree | 两个愿望，长成了一棵树 |  | S11：两个愿望，长成了一棵树。 | “长”读 zhǎng，人工听（F6）。 |
| a whole computer you rent and throw away / wreck it, delete it / one more layer / baked into an image | 一整台租来、用完就扔的电脑 / 随便折腾，用完就删 / 再加一层 / 打包进一个镜像 |  | S15：这台 VM 给了我们一整台机器，能随便折腾，用完就删。 |  |
| find them a home / that's the whole lesson in one picture | 给它们安个家；整节课的要点，就在这一张图里 |  | S02：我们去弄一台电脑，给它们安个家。 | 这里的 home 是比喻，不是 home 目录。 |

### 标签、进度条与固定句式 / Tags, tracker and fixed patterns

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| README tracker: README › section / step k of N: label / · extra | README › Installing App on VM Manually（章节标题保持原文）/ 第 k 步，共 N 步：步骤名 / · 额外 |  | S03：TRACKER A1 → 第 1 步，共 10 步：创建 VM | 章节标题是观众要在 README 里找的原文，不翻译（A11）；步骤说明翻译（E3）。 |
| tracker steps A: Create VM / SSH / apt-get update / Install git / Clone / cd / Install pip / Install packages / Run it / Delete VM | 创建 VM / SSH 登录 / apt-get update / 安装 git / 克隆仓库 / cd / 安装 pip / 安装包 / 运行 / 删除 VM |  |  | 书面写法（克隆仓库，不写 clone repo），命令名照写。 |
| tracker steps B: Install uv / Reload shell / uv sync / Activate (others as in A) | 安装 uv / 重新加载 shell / uv sync / 激活 |  |  |  |
| your turn / your-turn tag | ▶ 轮到你了 / “轮到你了”标签 | 轮到你了 | S01：看到黄色的“轮到你了”标签，就暂停视频，在你自己的 VM 上跑这条命令。 |  |
| extra / extra · not in the README / extras are safe | 额外 / 额外 · README 里没有 / 额外的命令都是安全的 |  | S01：灰色的“额外”标签表示这条命令 README 里没有；额外的命令都是安全的，也一起跑吧。 | 旁白：这条额外的命令 / 再做三个额外的检查 / 最后再加一个额外步骤。 |
| illustration / what if | 示意 / 假设 |  |  | 和差分隐私视频的“示意”一致。 |
| expected output / real capture / at the time of recording | 预期输出 / 实际输出 · 2026-10-12 / 录制时 | 录制时 | S09：录制时的版本是 0.13.0。 | 预期 vs 实际，一对；“录制时”每次照说（A9）。 |
| erratum / a small mistake / with an easy fix | 勘误（标签）/ 一个小错误 / 改起来很简单 |  | S11：这里 README 有一个小错误，改起来很简单。 | 旁白绝不说“勘误”“错误百出”；语气温和，后面一定跟改法（A9）。 |
| preview / today / L2 / first time only / package list varies by VM | 预览 / 今天 / 第 2 讲（放不下时保留 L2）/ 仅首次 / 软件包列表因 VM 而异 |  |  |  |
| Pause and ponder (card) / Something to ponder / Now predict / A quick puzzle | 暂停想一想（卡片标题，explainer/locales/zh.yaml）/ 来想一个问题 / 先预测一下 / 先出个小题 |  | S05：来想一个问题。 | 卡片标题由工具链翻译；卡片上的问题最多两行，以？结尾。 |
| Pause and run it / Pause and try it / Pause here / Pause until | 暂停一下，自己跑一遍 / 暂停一下，试试看 / 先在这里暂停 / 暂停视频，等到…… |  | S04：暂停一下，自己跑一遍。 | 固定句式见 D5。 |
| Test yourself / five questions / One: … Five: / The answers are in the exercises / Next time: containers | 自测 / 五道题 / 第一题：…… 第五题： / 答案在练习里 / 下节课：容器 |  | S15：最后，留五道题给你自测。 |  |
| code panel header: path · lines a–b / path · line n | path · 第 a–b 行 / path · 第 n 行 |  |  | 用 re: 键翻译（E4）。 |
| the tracker / code panels / study guide / exercises | 进度条 / 代码面板 / 学习指南 / 练习 |  | S01：左上角的进度条显示 README 的步骤。代码面板会标出文件和行号。 |  |

### 课程、产品与名字 / Course, products and names

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| AC215 · MLOps & LLMOps / Harvard / Lecture 1 / next lecture / part 1 / part 2 | AC215 · MLOps 与 LLMOps / 哈佛 / 第 1 讲 / 下节课 / 第一部分 / 第二部分 | AC 二一五 / 下节课 / 第一部分 / 第二部分 | S07：第二部分：同一个应用，换一台新的 VM，用干净的做法。 | 口头：今天这节课、下节课；书面：第 1 讲、第 2 讲。哈佛只在标题和简介里出现。 |
| README / the README's tip / README card / open the README beside this video | README / README 里的提示 / README 引文卡 | README | S01：想跟着做的话，把 README 打开，放在视频旁边。S04：README 在这里有个提示：apt-get 和 apt 做的是同一件事。 | 照写照说（文件名，也是课程里的叫法）；所有格说“README 的 / README 里”。读音待实测（F5，备用 read me）。README 引文卡的引文保持英文（A11）。 |
| simple-translate / dlops-io / MLOps Learning / the study guide | simple-translate / dlops-io / MLOps Learning / 学习指南 | simple translate / MLOps Learning / 学习指南 | S01：每条命令也都在学习指南里，在 MLOps Learning 这个 repo 里。 | MLOps 的读音待实测（F5）。 |
| Google / GitHub / PyPI / Debian / Ubuntu / Docker / AWS / Astral | Google / GitHub / PyPI / Debian / Ubuntu / Docker / AWS / Astral | Google / GitHub / Debian / Docker / AWS | S03：Google 的数据中心。 | 产品和公司名保持拉丁字母。 |
| the cheese app / its API service / the AWS version / the pipenv branch | cheese app / API 服务 / AWS 版本 / pipenv 分支 | cheese app / API 服务 / AWS 版本 / pipenv 分支 | S14：这个 repo 的 pipenv 分支用的就是它，单独的 AWS 版本和后面 cheese app 的 API 服务也一样。 | cheese app 是课程项目名，照说。 |
| student (the username) / ac215-l01 (the VM) / app (the project name) / classmate / Monday / next Monday | student / ac215-l01 / app / 同学 / 周一 / 下周一 | student / app / 同学 | S03：我们的提示符显示 student；你的会显示你自己的用户名。 |  |
| argparse / asyncio / art / googletrans / httpx / anyio / certifi / httpcore / h2 / idna / typing-extensions | argparse / asyncio / art / googletrans / httpx / anyio / certifi / httpcore / h2 / idna / typing-extensions（包名照写） | argparse / asyncio / art / googletrans / httpx / anyio / certifi / httpcore / h2 / idna / typing extensions | S11：我们的 googletrans 需要 httpx，一个 HTTP 库；它又需要 anyio、certifi、httpcore、h2，还有更多。 | 包名不翻译、不加“库”字头；需要时后面加“这个包”。列举用顿号。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| Video title | AC215 · 第 1 讲：虚拟机、虚拟环境与 uv（跟练：simple-translate） |  |  | 跟练 = follow-along，B 站常用。 |
| Part 1 title | AC215 · 第 1 讲（上）：云端 VM 与简单粗暴的手动安装 |  |  |  |
| Part 2 title | AC215 · 第 1 讲（下）：用 uv 管理虚拟环境 |  |  |  |
| Chapter S01: Why won't pip install? | pip 为什么不让装？ |  |  | 保留问句。 |
| Chapter S02: The app: cli.py | 这个应用：cli.py |  |  |  |
| Chapter S03: Renting a computer: the VM | 租一台电脑：虚拟机（VM） |  |  | 核心概念章节附英文简称，方便搜索（H1）。 |
| Chapter S04: apt, git and the repo | apt、git 和仓库 |  |  | 书面写“仓库”（A4）。 |
| Chapter S05: The system Python and PEP 668 | 系统 Python 与 PEP 668 |  |  |  |
| Chapter S06: Run it, and read the traceback | 运行它，读懂 traceback |  |  |  |
| Chapter S07: Delete, don't stop | 要删除，别只停止 |  |  |  |
| Chapter S08: What a virtual environment is | 虚拟环境（venv）到底是什么 |  |  | 核心概念章节附英文简称。 |
| Chapter S09: Installing uv | 安装 uv |  |  |  |
| Chapter S10: uv sync: which Python? | uv sync：用哪个 Python？ |  |  |  |
| Chapter S11: uv sync: resolve, lock, install | uv sync：解析、锁定、安装 |  |  |  |
| Chapter S12: Activation is just PATH | 激活，其实只是改 PATH |  |  |  |
| Chapter S13: Prove the isolation | 验证隔离 |  |  |  |
| Chapter S14: The older way: pipenv | 老办法：pipenv |  |  |  |
| Chapter S15: Tear down, recap, and what's next | 收尾、回顾和下节预告 |  |  |  |

### 配套材料 / Companion docs (README.md, exercises.md, digest.md)

| English | 字幕 / 屏幕 | 朗读（say:） | 首次出现 | 说明 |
|---|---|---|---|---|
| headings of exercises.md: Part A · The five questions from the end of the video / Part B · Hands-on (predict, then run) / Part C · Debugging / Part D · Think | A 部分 · 视频最后的五道题 / B 部分 · 动手（先预测，再运行）/ C 部分 · 排错 / D 部分 · 思考 |  |  |  |
| <summary>Answer</summary> | <summary>答案</summary> |  |  |  |
| symlink / subshell / transitive dependency / resolver / environment marker / wheel / hash | 软链接（符号链接）/ 子 shell / 传递依赖（间接依赖）/ 解析器 / 环境标记 / wheel 包 / 哈希 |  |  | 文档用书面形式，首次出现附英文。 |
| idempotent / reproducible / deterministic / rate-limited / endpoint / shadowing / externally managed environment | 幂等 / 可复现 / 确定 / 被限流 / 接口 / 遮蔽 / 由外部管理的环境（externally managed） |  |  |  |
| zh-CN console equivalents: Create instance / VM instances / Disks / Authorize / Delete / Stop / Enable / Billing | 创建实例 / VM 实例 / 磁盘 / 授权 / 删除 / 停止 / 启用 / 结算 |  |  | 只放进配套 README 和简介，给控制台是中文界面的观众对照（H3）。 |

## 规则


### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**：观众要输入、要在屏幕上找的字面内容。命令和子命令（sudo、apt、apt-get、git、pip、pip3、python3、uv、uvx、curl、sh、source、which、ls、cd、gcloud、deactivate、pipenv、uv sync / run / add / tree / python pin）、参数（-t、-a、-m、--break-system-packages、--locked）、文件和目录名（pyproject.toml、uv.lock、.venv、cli.py、pyvenv.cfg、Pipfile.lock、os-release、.python-version、~/.local/bin、/usr/local）、包名（googletrans、art、httpx、anyio、certifi、httpcore、h2、idna、typing-extensions、argparse、asyncio）、环境变量和配置项（PATH、VIRTUAL_ENV、sys.path、site-packages、dist-packages、requires-python、include-system-site-packages、home、prompt）、代码里的名字（Translator、Namespace、main、raise_exception）、终端原文和报错类名（externally managed、command not found、ModuleNotFoundError、requirement already satisfied）、英文控制台上要点的按钮和页面（Create instance、VM instances、Disks、SSH、Authorize、Delete、Enable）、README 的章节标题。（b）**产品、组织、课程和人名**：Google Cloud、GCP、Compute Engine、Debian、Ubuntu、Python、CPython、GitHub、PyPI、Docker、AWS、AC215、Tutorial 0、simple-translate、MLOps Learning、cheese app、JSON、HTTPS、API key、CPU、PEP 668、student。（c）**封闭清单**：VM、venv（跟着英文，见 A2），以及实验课上口头本来就说英文的 shell、root、repo、clone、commit、import、traceback、lock 文件、pin、hypervisor。新词要进（c），必须同时满足：中国 MLOps 工程师在实验课上就说英文；中文生硬、有歧义或和别的术语撞车；语音读得对（F5）。其余一律用中文（术语表）。绝不为了“味道”加英文：不说 package、dependency、endpoint、flag、folder、terminal、interpreter、container、image、billing、region、zone。
- **[A2]** 跟着英文走。virtual machine → 虚拟机，VM → VM；virtual environment → 虚拟环境，venv → venv。英文在哪儿用全称、在哪儿用简称，中文照做；定义句一定用全称（虚拟机就是……；虚拟环境其实就是一个目录……）。不简称“虚拟”或“环境”。S01 的“virtual 出现两次”在中文里正好是“虚拟”这个词出现两次。量词：一台 VM / 一台虚拟机，一个 venv / 一个虚拟环境。
- **[A3]** 字幕括注只有三处，都只在首次出现时加：hypervisor（虚拟机监控器）（S03）、externally managed（由外部管理）（S01）、外部 IP（也就是公网 IP）（S03）。放在分句末尾，不插进名词短语中间；只进显示文字，say: 里不写；括注之后的锚点要写显式 anchors:（D2）。中文行不给中文术语加英文括注：英文原句就在正下方。三处都在第一部分，第二部分不再重复。
- **[A4]** 书面与口头配对。旁白和字幕说 repo / clone / commit / 点；标签、章节名、meta.yaml、配套文档写 仓库 / 克隆 / 提交 / 点击。the repo 作主语说“这个 repo”。命令本身不受影响（git clone 照写）。
- **[A5]** 实物的写法。实物在字幕和标签里逐字照抄（大小写、点、斜杠、连字符、下划线都不变），旁白用英文读（读法 F3）；不翻译，不加复数和时态，不加引号、书名号或代码格式。需要时后面接一个中文名词：uv sync 这条命令、pyproject.toml 这个文件、PATH 这个环境变量、.venv 目录、--locked 参数、googletrans 这个包。句首不放实物，前面加一个中文词（而 pipenv shell……；这个 pyproject.toml 文件……；输入 uv sync……）：字幕好读，语音也不在句首撞上英文。
- **[A6]** 易混词对。镜像 = 容器镜像，绝不用于 Debian mirror（软件源）或 GCP OS image（系统映像）。目录 = 文件夹（.venv 目录、bin 目录），apt 的 package catalog 叫软件包列表，不叫目录。包（pip、uv 装的 Python 包）≠ 软件包（apt 装的）。依赖（pyproject.toml 里写的）≠ 包（实际装上的）。lock 文件 / 锁定（uv.lock、--locked、锁定精确版本）≠ pin（uv python pin、约束不是 pin）。约束（≥ 3.13 的范围）≠ 精确版本。提示符（prompt）≠ 提示（hint，pip 给的建议）。参数（flag、命令行 arguments）≠ 选项（argparse 的 options，只在 S02）。错误（泛指：两个错误、第一个错误）≠ 异常（Python exception）≠ 报错（屏幕上的出错信息）。激活（activate）≠ 启用（enable API）≠ 启动（start）。停止（Stop：磁盘还在、还在计费）≠ 删除（Delete）。结算（Billing，开通结算的项目）≠ 计费（按秒计费）。外部 IP ≠ 预留的 IP 地址。home 目录（~，你的）≠ /usr（系统的，读 user，绝不译“用户”）。应用（the app，概念）≠ app（name = "app" 这个字面名字）。软链接 ≠ 链接（网页链接）。解析依赖（resolve）和解析参数（parse，S02）同用“解析”，讲依赖时说全“解析依赖”。架子（shelf，sys.path 的一层）≠ 工具箱（toolbox，一个 venv 自己的那层架子）≠ 工具（tool，uv 本身）。
- **[A7]** 中文句子里的英文词不变形：不加复数、时态、冠词、所有格（很多包、两个 venv、uv 的、README 的）。量词：一台 VM、一个 venv、一个 repo、一条命令、一个参数、一个包、一个依赖、一个文件、一个目录、一层架子、一个罐子、一扇门、一张小票、一份愿望清单、一个 lock 文件、一个 shell、一个 traceback、一行代码 / 一行输出、一个提示符。复数用“这些 / 很多 / 几个”，不用“们”。
- **[A8]** 语体：助教带实验课。指令短，动词口语化（装、跑、删、点、输入），称呼用“你”（跟练视频，一对一；不用“您”“大家”“同学们”），“我们”指录制时的我们（我们录的时候，Google 拒绝了请求）。用中文语序，句子内部可以重组。避免翻译腔：不说“让我们……”（说“我们来……/ 先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句和“一个……的”长链。不用网络流行语（yyds、绝绝子、一键三连）。英文的口语节奏按意思转：Here's the catch → 问题就在这儿；Now, honestly → 说实话；To be fair → 公平地说；quick and dirty → 简单粗暴；for real → 这次是真的；Fresh matters → 全新很重要。
- **[A9]** 准确。限定语照译：by default 默认，usually 通常，may 可能，only 只，every 每个，exactly 正好，or newer 及以上，older than 低于，over a hundred 一百多个。“at the time of recording”每次都译成“录制时”，绝不省略：它告诉观众版本号会变。版本、个数、行号、步骤号和屏幕完全一致。勘误温和（一个小错误），而且一定紧跟改法。思考题（S05、S10、S11、S13）只问不答，措辞不能泄露答案（S10 不能说“uv 会自己下载”）。
- **[A10]** 名字。产品、公司、课程保持拉丁字母（Google、GitHub、Debian、Ubuntu、Docker、AWS、PyPI、Astral、MLOps Learning、cheese app）；哈佛只在标题和简介里写中文。用户名 student、VM 名 ac215-l01、项目名 app 照写。课程：AC215（say: AC 二一五）；Lecture 1 书面写“第 1 讲”，口头说“今天这节课”；next lecture → 下节课；L2 标签 → 第 2 讲（放不下时保留 L2）；Tutorial 0 照写；part 1 / part 2 → 第一部分 / 第二部分。
- **[A11]** 实物原样，讲解用中文。终端输出、提示符、终端标题（ssh · ac215-l01）、代码面板（含 # 注释：那是观众 clone 下来的真实文件）、README 引文卡（灰色引用，README.md · line N）、示意控制台上的英文界面文字、README 的章节标题（Installing App on VM Manually、Installing App on VM using UV）都保持英文原样；只翻译旁边的说明、tag、标注和比喻。旁白转述 README 时说“README 里说……”。
- **[A12]** 只做大陆简体：默认、程序、代码、文件、目录、服务器、网络、内存、磁盘、脚本、视频、用户名、信息。不用預設、程式、程式碼、檔案、資料夾、伺服器、網路、記憶體、磁碟、腳本、影片、使用者。

### B. 排版

- **[B1]** 空格。中文和拉丁字母、数字、实物之间加一个半角空格，字幕、标签、文档和 say: 都一样（输入 sudo apt-get update、.venv 目录、PATH 里、第 3 步、11 个包、Python 3.11.2、home 目录）。say: 里缺空格 check 会报，词典改拼也靠空格匹配。实物内部的空格照原样（uv python pin 3.13），实物内部绝不加空格。全角标点旁不加空格（……cd simple-translate。）。不用 U+00A0 / U+202F 冒充不换行空格（norm() 会把它变成普通空格）。
- **[B2]** 标点。中文用全角：，。、；：？！（）“”……，实物旁边也一样（输入 python3 cli.py。）。列举用顿号（anyio、certifi、httpcore、h2）。“”只用于中文标签名（“轮到你了”标签、“额外”标签）和“虚拟”这个词；实物不加引号。一个中文句子内部不出现。？！（一个英文句子对应一个中文句子），改用，；：。“第 N 步：”后面用全角冒号。标签末尾不加句号，问句保留？。命令里本来的引号、竖线、等号只出现在画面上，字幕里用文字说（这根竖线）。
- **[B3]** 字幕里的实物和符号。不用反引号或代码字体。屏幕上连成一体的代码片段原样显示（raise_exception=True、python3 -m venv、ls -a、--locked）；屏幕上的关系或运算，在字幕里用文字说：include-system-site-packages 是 false，prompt 是 app；Python 3.13 及以上（不写 >=3.13）；大于等于、双等号；低于 3.15。路径按屏幕原样（.local/bin、/usr/local、.venv/bin/activate），~ 只在标签和“这个波浪号”里出现。
- **[B4]** 字体。工具链把自家字体和 Noto Sans / Serif / Sans Mono CJK SC 配对（explainer/i18n.py CJK_FONTS），等宽标签里的中文自动用 Noto Sans Mono CJK SC，实物仍用自家等宽字体。中文不用斜体（英文 slant=ITALIC 的地方在 i18n.active() 下改为正体）；粗体可以。

### C. 数字、版本号与编号

- **[C1]** 显示文字里的数字。和屏幕、终端、代码呼应的一律用阿拉伯数字：步骤号（第 3 步）、行号（第 25 行）、个数（2 个依赖、装了 12 个、11 个包、解析了 13 个、另外 9 个）、版本号、状态码、年份。叙述里的小数目和序数用汉字：两个项目、三个部分、四种方式、前两级、一个小错误、三个额外检查、五道题、第一 / 第二 / 第三（S08 三个部分）、第一部分 / 第二部分、第一题……第五题。over a hundred → 一百多个。
- **[C2]** 版本号的读法（say:）。按“整数组”读，组之间说“点”：3.11.2 三点十一点二，3.10 三点十，3.13 三点十三，3.13.5 三点十三点五，3.15.0 三点十五点零，0.13.0 零点十三点零，0.27.2 零点二十七点二，0.28.1 零点二十八点一，0.13.3 零点十三点三，4.0.2 四点零点二，6.5 六点五，23.0.1 二十三点零点一。这是版本号的含义（3.10 比 3.9 新，S10 的数轴上就排在 3.9 后面），也是 Python 圈的说法；edge 默认按小数读（三点一零、三点一一），所以每个含版本号的句子都写 say:。显示文字保持数字。
- **[C3]** 编号逐位读。HTTP 状态码 429 → 四二九（像四零四）；PEP 668 → PEP 六六八；AC215 → AC 二一五；ac215-l01 → AC 二一五 L 零一；e2-small → e2 small。产品大版本号按整数读：Python 3 → Python 三，googletrans 4 → googletrans 四，Debian 12 → Debian 十二（edge 自动）。日期 2026-10-12 只在画面上。
- **[C4]** “两”和“二”。显示写“2 个依赖”“2 个包”，say: 写“两个依赖”“两个包”（edge 会读成“二个”；井字棋视频实测过“二局”）。版本号和名字里的 2 读“二”（零点二十七点二、e2、h2）。叙述里本来就写汉字的“两”不受影响。
- **[C5]** 符号的读法：>= 大于等于；== 双等号；=（代码里）等于，（配置里）是；< 低于；| 竖线（管道）；~ 波浪号；/ 斜杠；.（文件名、域名、sys.path）点；参数前缀的 - 杠（-t 杠 t，ls -a ls 杠 a，python3 -m venv python3 杠 m venv）；长参数的 -- 不读（--locked → locked 参数）；名字里的连字符不读（apt-get → apt get）；( ) 不读，说“外面带括号”。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 每个 SAY 行一条（共 118 段）；en 与 SAY 行逐字节相同；zh 的条目数等于 explainer.voice.split_sentences 切出的英文句子数（全片 391 句）。只在句子内部重组，绝不合并或拆分。短句也各占一条：Why refuse? → 为什么要拒绝？；Command not found. → 报 command not found。；ModuleNotFoundError. → 报 ModuleNotFoundError。；What happens? → 会怎么样？；Does it work? → 能导入吗？；What changed? → 变了什么？；Now predict. → 先预测一下。；Something to ponder. → 来想一个问题。做 TTS 之前先运行 python -m explainer.i18n check videos/ac215-l01-vms-venvs --lang zh。
- **[D2]** 锚点。场景里 vo.wait_until 的短语凡是指向实物、数字、版本或术语的，都写 anchors:，目标用显示形式（pyproject.toml、uv.lock、.venv、PATH、第 9 步、429）。目标必须在预定的那一句里第一次出现：AlignedClip.time_of 取整段里第一个包含目标的句子。本片的实物重复得很多（uv.lock、pyproject.toml 在一段里常出现两三次），必要时目标带上一个相邻的中文词（“而 uv.lock”“读 pyproject.toml”）。时间按显示句的字符位置估算：长的拉丁实物每个字母都算一个字符，读起来却快得多（source .venv/bin/activate 25 个字符，读出来约 2 秒），后面的词会估得偏晚，目标要往前挪；say: 比显示长的地方（版本号三点十一点二、四二九）正相反。对照词级时间（Whisper）检查。中文语序对调两个锚定短语时，场景在 i18n.active() 下按中文顺序等。
- **[D3]** 时长。VoiceScene 等中文音频播完：音频长了画面停住，短了固定时长的动画后面会留空白。每段中文和英文时长相差不超过 ±15%：删多余的连接词，不删内容。版本号、实物和 say: 展开会让中文变长，S10、S11、S14（英文本身就慢）要特别看。渲染前检查：python -m explainer.script videos/ac215-l01-vms-venvs/script.md --lang zh（同时填好渲染用的 TTS 缓存）。
- **[D4]** 内容对等。每个中文句子只翻译对应的英文句子：不加命令、参数、中文控制台名称或术语解释；“额外”只在英文标出的地方说。唯一的增补是三处字幕括注（A3）。
- **[D5]** 固定口头句式。Pause and run it. → 暂停一下，自己跑一遍。Pause and try it. → 暂停一下，试试看。Pause here, and get your VM to this point. → 先在这里暂停，把你的 VM 也弄到这一步。Pause, and catch up to here. → 暂停一下，跟上进度。Pause until … → 暂停视频，等到……（等你的终端打开 / 直到提示符以 simple-translate 结尾 / 等它删完）。pause to run both / all three → 暂停一下，两条都跑一遍 / 三条都跑一遍。Pause and do it now, before you forget. → 现在就暂停去删，免得忘了。Something to ponder. → 来想一个问题。Now predict. → 先预测一下。A quick puzzle: → 先出个小题：。This command isn't from the README → 这条命令不是 README 里的。An extra check: / Two extra checks. / Last, an extra: → 额外检查一下：/ 两个额外检查。/ 最后再加一个额外步骤：。a small mistake in the README, with an easy fix → README 里有一个小错误，改起来很简单。Step N: → 第 N 步：。Before you go, five questions to test yourself. → 最后，留五道题给你自测。One: … Five: → 第一题：…… 第五题：。The answers are in the exercises. → 答案在练习里。Next time: containers. → 下节课：容器。卡片标题“暂停想一想”由工具链给（explainer/locales/zh.yaml），卡片问题最多两行，以？结尾，计时秒数不变。

### E. 屏幕文字（strings/*.yaml）

- **[E1]** 标签用中文：短的名词短语，用旁白的同一个词（架子、工具箱、公用厨房、愿望清单、小票、约束不是 pin、计价器、门），可以用 → · ≈。标签里的实物照写（~ = 你的 home 目录、import httpx、2 个依赖）。标签只写中文，不加英文小字：英文原句在字幕里。
- **[E2]** 画面上保持英文的东西（A11）：终端输出和提示符、终端标题、代码面板（含注释）、README 引文卡的引文、示意控制台的界面文字（页面名、按钮、表单字段名、确认对话框“Delete ac215-l01? …”）、浏览器地址栏、README 章节标题、文件 / 包 / 命令 chip、架子和门上的路径标签、版本号 chip。经过 tr() 的这类字符串在 strings.yaml 里加原样映射（README 章节标题、控制台文字、引文），这样 build/i18n/missing.zh.json 只列真正漏译的；代码面板的注释不加条目（Code hook 只在有条目时才翻译注释）。
- **[E3]** README 进度条。标题行保持原文：README › Installing App on VM Manually / README › Installing App on VM using UV。说明行：step k of N: 步骤名 → 第 k 步，共 N 步：步骤名；“ · extra” → “ · 额外”。步骤名：A 节 创建 VM / SSH 登录 / apt-get update / 安装 git / 克隆仓库 / cd / 安装 pip / 安装包 / 运行 / 删除 VM；B 节第 7–10 步 安装 uv / 重新加载 shell / uv sync / 激活，其余同 A 节。实现：最好由 ReadmeTracker 分别翻译模板和步骤名（I1）；在那之前，用每个步骤名一个 re: 键（'re:step (\d+) of (\d+): Install git' → '第 \1 步，共 \2 步：安装 git'），带 · extra 的再各加一个。
- **[E4]** 面板标题。code_panel 的“path · lines a–b”“path · line n”用两个 re: 键：'re:(.+) · lines (\d+)–(\d+)' → '\1 · 第 \2–\3 行'，'re:(.+) · line (\d+)' → '\1 · 第 \2 行'。PANEL 的自定义标题照译：uv installer · its last lines → uv 安装脚本 · 最后几行；uv.lock · lines 5–12 (generated on your VM) → uv.lock · 第 5–12 行（在你的 VM 上生成）；~/.profile line 29 · ~/.bashrc line 115 · added by the installer → ~/.profile 第 29 行 · ~/.bashrc 第 115 行 · 由安装脚本添加。README 引文卡标题（README.md · line 62）同第一种。
- **[E5]** tag 对照：▶ your turn → ▶ 轮到你了；extra · not in the README → 额外 · README 里没有；illustration → 示意；what if → 假设；expected output → 预期输出；real capture · 2026-10-12 → 实际输出 · 2026-10-12；at the time of recording → 录制时；erratum → 勘误；preview → 预览；today → 今天；L2 → 第 2 讲；first time only → 仅首次；package list varies by VM → 软件包列表因 VM 而异；copy it from here → 从这里复制；copy from the README, quotes included → 从 README 复制，连引号一起；your username here → 这里是你的用户名；~ = your home folder → ~ = 你的 home 目录；not in the repo → 仓库里没有；no activation needed → 不用激活；not executable → 不可执行；just read: no pipenv on this VM → 只看不跑：这台 VM 没装 pipenv；optional · needs the gcloud CLI on your laptop → 可选 · 笔记本上要装 gcloud 命令行工具。
- **[E6]** 不带作用域的单个字母、数字和符号（Y、?、1、2、3、L2、xx）绝不放进 strings.yaml：tr() 会把所有场景里同样的字符串一起改掉。需要时用带场景作用域的键（'s10_which_python|?': '？'）。
- **[E7]** 着色。场景给英文子串着色（t2c）的地方，中文标签必须原样包含那个子短语的中文；实物不变，所以按实物着色的（art、googletrans、uv.lock、.venv/bin）自动保留。英文的大写强调改成给中文上色或加粗。
- **[E8]** 宽度。汉字约 1 em 宽：中文标签按英文标签的外框来适配，不照搬 font_size；放不下时缩短中文，绝不截断实物。终端和代码面板的宽度、行数、位置与英文版完全一致。

### F. 语音（TTS）

- **[F1]** 声音。中文旁白用 edge zh-CN-XiaoyiNeural（speed 1.0），是工具链的中文默认（explainer/build.py DEFAULT_VOICES），video.yaml 不用设 languages.zh.voice。它在另两个视频里读英文词和数字都很稳（两片 417 句 ASR 回环没有系统性误读），这正是本片大量实物需要的。发布：免费的 Edge 端点没有发布授权；设置 AZURE_SPEECH_KEY 和 AZURE_SPEECH_REGION 后，工具链自动改走官方 Azure AI Speech（同一个声音），TTS 缓存按后端区分，发布版会重新合成全部句子（再跑一遍 D2、D3）。edge 不支持自定义 SSML 或拼音，读错只能靠改写或 lexicon.zh.yaml 改拼。
- **[F2]** 什么时候必须写 say:。显示文字里有以下任何一种：文件名、域名或 sys.path 里的点（pyproject.toml、uv.lock、cli.py、pyvenv.cfg、Pipfile.lock、translate.googleapis.com）；路径里的 / 或 ~（.local/bin、.venv/bin/activate）；参数前缀的 -（-t、ls -a、-m）或 --（--break-system-packages、--locked）；下划线（VIRTUAL_ENV、raise_exception）；= == >= < | 括号；名字里的连字符（apt-get、python3-pip、site-packages、dist-packages、simple-translate、typing-extensions、pip-tools、e2-small、ac215-l01、.python-version）；驼峰报错名（ModuleNotFoundError）；版本号（C2）；逐位读的编号（429、PEP 668、AC215，C3）；量词前的 2（C4）；字幕括注（A3）；usr（读 U S R）、xx（读 x x）。不需要 say:：普通命令和名字（uv、pip、apt、sudo、git、venv、PATH、Debian 12）、第 3 步、第 25 行、除 2 以外的个数。
- **[F3]** 读法表（say:）。pyproject.toml pyproject 点 toml；uv.lock uv 点 lock；cli.py cli 点 py；pyvenv.cfg pyvenv 点 cfg；Pipfile.lock Pipfile 点 lock；sys.path sys 点 path；translate.googleapis.com translate 点 googleapis 点 com；.venv 点 venv；.venv/bin/activate 点 venv 斜杠 bin 斜杠 activate；.local/bin 点 local 斜杠 bin；.python-version 点 python version；/usr/local user local；/usr/lib user lib；usr U S R；~ 波浪号；-t 杠 t；ls -a ls 杠 a；python3 -m venv python3 杠 m venv；--break-system-packages break system packages；--locked locked；VIRTUAL_ENV virtual env；raise_exception=True raise exception 等于 True；include-system-site-packages = false include system site packages 是 false；apt-get apt get；python3-pip python3 pip；site-packages site packages；dist-packages dist packages；simple-translate simple translate；typing-extensions typing extensions；pip-tools pip tools；e2-small e2 small；ac215-l01 AC 二一五 L 零一；AC215 AC 二一五；gcloud g cloud；ModuleNotFoundError Module Not Found Error；xx x x；429 四二九；PEP 668 PEP 六六八；版本号见 C2。
- **[F4]** 词典。EXPLAINER_LANG=zh 时只加载 explainer/lexicon.zh.yaml（共用的 lexicon.yaml 不参与，所以英文版的 uv's、README's、sys、pipx 条目对中文无效）。改拼只用于 say:，改拼后的文本就是 TTS 缓存键；匹配区分大小写、按整词（汉字也算词边界），所以 say: 里每个拉丁词两边都要有空格（B1）。只在人工听出读错之后才加条目；备好的候选：README → read me，PATH → path，venv → v env，sudo → soo doo，pyenv → py env，pipx → pip x，uvx → uv x。中文的修正绝不放进 lexicon.yaml；显示文字绝不因读音改动。
- **[F5]** 实测状态与必听清单。本词表写的时候（2026-10-12）在这个环境里合成不了 edge 语音：Bing 的 WebSocket 握手返回 403（同一端点的 HTTPS 声音列表可以访问），工具链的 EdgeBackend 又没有把 HTTPS 代理交给 aiohttp（I2），所以上面的读音规则来自两份先例和中国工程师的读法，没有实测。第一次合成后必须做 ASR 回环（faster-whisper large-v3-turbo，语言设为 zh），并人工听下面这些（按风险排序）：pin（合法拼音，可能读成“拼”；读错就整片改说“固定版本”：约束不是固定版本、把它固定下来，S10 标签同改；不改用“锁定”，那是 lock 文件的词）；“行”（第 25 行、那一行、行号、最后一行，可能读成 xíng；不行就改“代码第 25 行”“那句输出”）；venv、README、PATH（可能逐字母读）；sudo、repo、curl、gcloud、googletrans、googleapis、pyproject、toml、pyenv、pipx、uvx、MLOps、CPython；python3、pip3（预计读“python 三”“pip 三”）；Module Not Found Error；所有版本号的 say:（三点十一点二）；四二九、PEP 六六八、AC 二一五。拉丁词转写回来是同音字或大小写不同的不算问题；Whisper 自己的毛病（长句截断、名字拼法不同）也不算。
- **[F6]** 多音字，人工听：行（háng：第 25 行、那一行、行号、一行命令；本片最多）、重（chóng：重新、重建、重跑、重连）、长（zhǎng：长成一棵树）、载（zài：下载）、得（děi：你得先 cd）、还（hái）、空（kōng：空的）、数（shù：数轴）、种（zhǒng：一种语言）、调（diào：调用）、为（wèi：因为）、处（chǔ：处理）。只做整词改写，不做单字规则。

### G. 字幕

- **[G1]** 双语格式。中文在上（字大），英文 SAY 原句在下（字小），由 narration.yaml 配对，时间跟中文音频。宽度按工具链单位算：一个汉字 1，一个拉丁字符 0.55（source .venv/bin/activate ≈ 13.8，include-system-site-packages ≈ 15.4）。写句子时让每个分句不超过约 24 单位；代码在 30（双语）和 22（纯中文字幕）处切。
- **[G2]** 字幕结尾：去掉每条字幕末尾的。，、；：，保留？！…… 和收尾的”）（工具链已实现，subtitles.strip_end）。
- **[G3]** 英文行（en_display）。SAY 行把实物念成单词（dot venv、user local、dash t、the locked flag、virtual env、raise exception equals True、sys dot path、translate dot googleapis dot com、x x、U-S-R），所以每个念出实物的句子都手写 en_display，英文行显示屏幕上的字面形式（.venv、/usr/local、-t、--locked、VIRTUAL_ENV、raise_exception=True、sys.path、translate.googleapis.com、xx、usr），和中文行、画面一致。没写的句子显示 SAY 原文。英文版自己的 .srt 不受影响。
- **[G4]** 命令不断行。字幕切分把中文行里两个拉丁词之间的空格当成好的断点，所以 sudo apt-get update、uv python pin 3.13、source .venv/bin/activate 可能被切成两行，观众没法照抄。写法上：整条命令放在分句末尾、全角冒号后面（第 3 步：输入 sudo apt-get update。），一条字幕里最多一条命令，命令前后的中文尽量短；在预览里检查每条带命令的字幕。工具链待办见 I3。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、分 P 和章节标题用术语表里的写法：书面语（仓库、克隆、提交），问句保留问号，“uv sync：……”的冒号结构照搬，命令和文件名照写。核心概念章节附英文简称方便搜索：租一台电脑：虚拟机（VM）、虚拟环境（venv）到底是什么。
- **[H2]** 简介（B 站 / YouTube）：一段话说清这是 AC215 第 1 讲的跟练（simple-translate 的前两个 walkthrough），列出会学到的东西，附学习指南、练习和英文 README 的链接，中英对照列出核心术语（虚拟机 VM、虚拟环境 venv、lock 文件 uv.lock、约束 constraint、pin、解析 resolve、externally managed、PEP 668），以及中文控制台对照（H3）。标签：AC215、MLOps、uv、虚拟环境、虚拟机、Python、GCP、跟练。
- **[H3]** 配套材料：i18n/zh/README.md、exercises.md（如果做 digest.md 同理），按本词表和排版规则翻译，用书面语（仓库、克隆、提交、软链接（符号链接）、幂等、传递依赖）。标题和 <summary>答案</summary> 翻译。附两张表：中英术语对照表（English | 本片用词 | 常见变体：符号链接、间接依赖、锁文件、端点、速率限制）；中文控制台对照（Create instance 创建实例、VM instances VM 实例、Disks 磁盘、Authorize 授权、Delete 删除、Stop 停止、Enable 启用、Billing 结算、Region 区域、Zone 可用区、Machine type 机器类型、Boot disk 启动磁盘、External IP 外部 IP）。
- **[H4]** 代码和命令逐字节不变：配套材料里的代码块、命令、文件名、行内 `code` 一个字符都不改，只翻译 # 注释和周围的说明文字（注释可译，因为这里不是在引用 repo 里的文件）。

### I. 工具链待办

- **[I1]** （待办）ReadmeTracker（explainer/devops.py）把说明行拼成一个字符串 f"step {k} of {N}: {label}"，strings.yaml 只能逐个步骤名写 re: 键（E3）。建议：用 tr() 分别翻译模板（locales/zh.yaml："step {k} of {n}: {label}": "第 {k} 步，共 {n} 步：{label}"）、步骤名和“ · extra”后缀。只在 i18n.active() 时生效，英文版逐帧不变。
- **[I2]** （待办）explainer/voice.py 的 EdgeBackend 没有把 HTTPS_PROXY 交给 edge_tts.Communicate（aiohttp 默认不读代理环境变量），在只能走代理的环境里会一直等到超时；建议传 proxy=os.environ.get("HTTPS_PROXY")。即使传了，2026-10-12 在本环境里 Bing 仍对 WebSocket 握手返回 403（HTTPS 的声音列表正常），所以中文合成要在能直连 Bing 的机器上做，或者走 Azure（F1）。双语复核（2026-10-12）时又试了一次，重试约一分钟后同样是 403；复核环境的出口代理明确不支持 WebSocket 升级，没有可调的设置，所以复核的时长检查用的是估算模型（见 narration/*.yaml 文件头）。
- **[I3]** （待办）explainer/subtitles.py 的 _cuts 把中文行里拉丁词之间的空格算作好的断点，命令会被切开（G4）。术语表 en 字段里的两三个词的命令（uv sync、uv python pin、git status、pipenv shell）只保护英文行。建议：在中文行里，把连续的拉丁 token 串（中间只有空格）当作不可切的整体，除非它本身就超过一行。
- **[I4]** （说明）python -m explainer.i18n check 会检查 say:（没有 say: 时检查显示文字）里的括号、数学符号（= < > 等）、带下划线的名字、缺失的中西文空格，以及不在本词表朗读 / 字幕 / 首次出现形式或 allowed_spoken_latin 里的拉丁词。它把 pyproject.toml 这样带点的写法当成一个词，所以 say: 写成 pyproject 点 toml 后，pyproject、toml 两个词都要在本词表里（已列入）。它不检查：say: 里的版本号读法是否和显示一致、数字后面的“个”（C4）、标签里的拉丁词。
