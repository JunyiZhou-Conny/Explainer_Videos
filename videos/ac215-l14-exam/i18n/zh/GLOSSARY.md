# AC215 第 14 讲考前精讲版中文字幕词表（中英混用版）

视频：*AC215 · Lecture 14 — Serverless Deployment (exam edition)*（`videos/ac215-l14-exam`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生，第 4 次小测（周二）的前一天：做过第 1–13 讲（虚拟机、container、`docker run` 发布 port、放在 `secrets/` 里的服务账号密钥、Vertex AI 训练任务），上过第 14 讲，大概翻过 `serverless-deployment` 的 README，但还没想透每个答案**为什么**对。他们在笔记本上看，没有打开 clone。语体：中国 MLOps 助教在考前一天带复习课。
这是**考前精讲版**，不是跟练：没有 README 进度条，没有 `your turn` 标签，没有终端录屏，不逐条讲命令，也**不做任何现场运行**：每个面板都是两个演示仓库的源码（`dlops-io/serverless-deployment` @ `46cc62f`，`dlops-io/model-deployment` @ `cf0b7c7`）或我们自己的示意图。
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l14-exam.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长，只保留显示规则。但没有 `say:` 时，`python -m explainer.i18n check` 仍会对显示行做朗读检查（括号、数学符号、带下划线的名字、词表里没有的拉丁词、缺少的半角空格）：规则 A6、B3、D3 就是为此而设。
英文原稿：`script.md` v1（SAY 行是旁白：66 段、191 句；S01–S04 是 34 段、103 句，S05–S08 是 32 段、88 句）。课件：`../ac215-l14-serverless-deployment/SLIDES.md`（第 14 讲，17 页）和第 15 讲课件第 11–17 页。
先例：系列试点 [`ac215-l01-vms-venvs`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md)（repo、服务账号、密钥、虚拟机 / VM、计价器、计费）；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md) 到 [`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md)（container、image、port、token、bucket、部署、请求、构建、退出码，以及纯字幕规则）；[`ac215-l07-agent-harness`](../../../ac215-l07-agent-harness/i18n/zh/GLOSSARY.md)（web 服务器、日志）；最新完成的 [`ac215-l08-llm-finetuning`](../../../ac215-l08-llm-finetuning/i18n/zh/GLOSSARY.md)（endpoint、客户端、凭据、运行时，以及这份文件沿用的 A1–I3 规则编排）。第 1–8 讲定下的词一律沿用。
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教讲 Cloud Run 时本来就中英混着说：“部署成一个 Cloud Run service”“这个 job 跑完就退出”“serverless 部署”“resize 到 224 乘 224”“调一下这个 endpoint”。硬说“作业”“无服务器”“调整尺寸”，在复习课上反而像说明书；而且第 4 次小测的选项是英文的，service 和 job 照说，看题时一眼就对得上。
- 观众要在英文代码面板、README 摘录和考题里找东西。命令（serve、batch）、文件名、job 名和账号名、角色名、控制台字样、状态码一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（函数、入口点、实例、冷启动、最小实例数、缩容到零、计费、空闲、预配、服务账号、默认凭据、预处理、推理、签名、回滚、瘦客户端）一律说中文，用 Google Cloud 中文文档和中文技术资料里能搜到的标准译名。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：代码面板、README 摘录、控制台示意小卡、课件标签、示意图标注、考点图、规则卡片和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在考前一天带复习课时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“构建 image”“开一个 port”“建一个 bucket”“调一个 endpoint”；这期再加上“部署成一个 Cloud Run service”“跑一个 job”“serverless 部署”“resize 到 224 乘 224”。每个选择都要过三关：复习课上真的这么说；是能搜到的中文标准译名；和系列保持一致（第 1 讲定虚拟机 / VM、计价器、计费、服务账号、密钥，第 2–4 讲定 container、image、port、bucket、部署、构建、退出码，第 7 讲定 web 服务器、日志，第 8 讲定 endpoint、客户端、凭据：一律沿用）。

1. **实物原样**：观众要在屏幕上对照的东西（命令 serve、batch、python，文件名，job 名和账号名，角色名，控制台字样 Execute，403，方法名 predict，gunicorn）逐字照抄，不翻译、不变形、不加引号；检查器逼出来的例外是带下划线的名字，按旁白的念法写（A6）。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 repo；第 2–4 讲的 container、image、port、token、Dockerfile、bucket；第 8 讲的 endpoint；**这期新增 service、job、serverless、resize**。
3. **其余一律用中文标准术语**（A3）：函数、入口点、生命周期、实例、流量、缩容到零、触发器、计价器、计费、账单、按请求计费、按用量计费、调用、执行时间、空闲、预配、虚拟机、冷启动、最小实例数、热实例、常驻、最小副本数、源代码、依赖、构建、部署、查询字符串、权限、调用方、公开访问、服务账号、角色、密钥、默认凭据、身份、工作负载、日志、调试、预处理、推理、客户端、瘦客户端、解码、归一化、字节、张量、概率、回滚、版本、发布、注册、导出、模型服务器、签名、经验法则、厂商锁定。
4. **视频的比喻按意思译，一个比喻一个词**：时间条、计价器、金色阴影、门、工牌、齿轮、配方、插头 / 插座。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、仓库、存储桶、服务（service）、作业（job）、无服务器（serverless）、端点（endpoint）。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **复习课语体**：考点、题目、选项、选 B、规则是：；思考题的引子不给答案；课程的练习题从不引用（A9）。
8. **工具链的约束也是规则**：每个英文句子对应一个中文句子（66 段、191 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；口语轻松、讲解清楚，像考前带复习课的助教，但不用网络流行语。

## 关键决定

- **service 和 job 照说**（A1 c，这期新增）：它们是 Cloud Run 的两种资源类型，也是考题选项里的词；字幕写 Cloud Run service / Cloud Run job，书面写“服务（service）”“作业（job）”（沿用 Google Cloud 中文文档的“Cloud Run 作业”）。job 不写“任务”（留给第 8 讲的微调任务、第 13 讲的训练任务）。和“服务账号”“service 名称”分开（A7）。
- **全片的核心判断，一个说法**：read the lifecycle → **看生命周期**（S02、S08）；A function is a container you did not write → **函数就是一个不用你自己写的 container**（S04）；the platform calls exactly the name you registered → **平台只调用你注册的那个名字**（S07、S08）。
- **function → 函数，一个词**（A3、A7）：serverless 产品、Python 函数、serving function 都是“函数”，因为视频正是要把入口点和 serving default 连起来（S07[8]）。产品名照写：Cloud Run functions（现在的名字）、Cloud Functions（课件的名字）；不写“云函数”。entry point → 入口点。
- **serverless 照说**（A1 c），书面“无服务器（serverless）”；Serverless Deployment → 无服务器部署。**resize 照说**（A1 c）；normalize → 归一化，decode → 解码。
- **两个计价器**（第 1 讲：计价器、计费）：billed → 计费，bill → 账单，pay-per-use → 按用量计费，request-based billing → 按请求计费，provisioned → 预配，idle → 空闲，always on → 一直开着 / 常驻，cold start → 冷启动，minimum instances → 最小实例数，warm instance → 热实例。
- **两扇门**（V4）：caller → 调用方，public access → 公开访问；badge → 工牌，service account → 服务账号，default credentials → 默认凭据，identity → 身份，deployment permission → 部署权限。角色名照写。
- **serve 的两个意思**（A7）：web 应用的 serve 命令（S01–S02）≠ 考题对 serving function 的叫法（S07[2]），旁白和字幕都把两者分开。batch 命令 ≠ 一批字符串（S07）。
- **带下划线的名字**（A6）：hello_http → hello 下划线 http（SAY 特意念出 underscore）；preprocess_image → preprocess image；serving_function → serving function；serving_default → serving default；bytes_inputs → bytes inputs；英文行用 en_display 还原（D4）。min_replica_count 旁白当普通话说 → 最小副本数。
- **思考题**（A9）：S02[7]、S03[6]、S07[4] 三张选择题卡片，加上 S06[6] 一句；引子和题干不泄露答案；揭晓以字母开头（选 B，……；先试 B）。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令（serve、batch、python）、文件名（Dockerfile、main.py）、job 名和账号名（translation-audio、translation-demo-runtime）、控制台字样（Execute）、角色名（Agent Platform User、Service Usage Consumer、Service Account User、Storage Object Viewer、Storage Object Creator）、状态码（403）、代码名（hello 下划线 http、preprocess image、serving function、serving default、bytes inputs、predict）、包名（gunicorn）、格式名（JPEG、JSON、base64）。
- 产品、组织和课程：AC215、Google、Google Cloud、Cloud Run、Cloud Run functions、Cloud Functions、Functions Framework、Cloud Build、Artifact Registry、Cloud Scheduler、Vertex AI、Agent Platform、Docker、Python、README、HTTP、HTTPS、URL、CPU、VM（A1 b）。
- 实验课口语，封闭清单：repo（第 1 讲）；container、image、port、token、Dockerfile、bucket（第 2–4 讲）；endpoint（第 8 讲）；**service、job、serverless、resize（这期新增）**。
- 系列清单里保留英文、但这期没说到的：pipeline、volume、venv、PATH、prompt、embedding、CI、agent（只在 Agent Platform 里）（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| Cloud Run service / job | Cloud Run service / job | lifecycle / runs to completion | 生命周期 / 跑到完成 |
| exits / exit status | 退出 / 退出码 | execution / Execute | 执行 / Execute |
| listen / request | 监听 / 请求 | instance / traffic | 实例 / 流量 |
| scale to zero / URL | 缩容到零 / URL | trigger / every night / on demand | 触发器 / 每晚 / 按需 |
| default command / startup command | 默认命令 / 启动命令 | web server / web app | web 服务器 / web 应用 |
| task timeout / troubleshooting table | 任务超时 / 故障排查表 | meter / bill / billed | 计价器 / 账单 / 计费 |
| request-based billing / pay-per-use | 按请求计费 / 按用量计费 | invocation / execution time | 调用、调用次数 / 执行时间 |
| idle time / provisioned hours | 空闲时间 / 预配的时长 | virtual machine / VM | 虚拟机 / VM |
| cold start / minimum instances | 冷启动 / 最小实例数 | warm instance / always on | 热实例 / 一直开着、常驻 |
| minimum replica count / no minimum charge | 最小副本数 / 没有最低收费 | serverless / function | serverless / 函数 |
| entry point / hand over | 入口点 / 交出 | source / requirements file | 源代码 / requirements 文件 |
| HTTP handler / query string | HTTP 处理函数 / 查询字符串 | build / build time / build logs | 构建 / 构建时 / 构建日志 |
| deploy / redeploy | 部署 / 重新部署 | caller / public access | 调用方 / 公开访问 |
| service account / badge / role | 服务账号 / 工牌 / 角色 | key / default credentials | 密钥 / 默认凭据 |
| identity / deployment permission | 身份 / 部署权限 | workload / logs / debug | 工作负载 / 日志 / 调试 |
| preprocessing / inference | 预处理 / 推理 | client / thin client | 客户端 / 瘦客户端 |
| client-side brittleness | 客户端的脆弱性 | gear / recipe | 齿轮 / 配方 |
| decode / resize / normalize | 解码 / resize / 归一化 | bytes / base64 / tensor | 字节 / base64 / 张量 |
| version / roll back / ship | 版本 / 回滚 / 发布 | app store review | 应用商店审核 |
| register / export / signature | 注册 / 导出 / 签名 | model server / plug / socket | 模型服务器 / 插头 / 插座 |
| probability / classified | 概率 / 分类 | rule of thumb / vendor lock-in | 经验法则 / 厂商锁定 |
| the quiz / exam questions / option | 小测 / 考题 / 选项 | the rule / idea (topic) | 规则 / 考点 |
| the slides / slide 16 / next lecture | 课件 / 课件第 16 页 / 下一讲 | Try one / Hold that question | 来试一道 / 先记着这个问题 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 开头：一个永远跑不完的 job / The hook: a job that never finishes

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Cloud Run job / job / a job / the job's execution / Execute | Cloud Run job / job / 执行 / Execute | S01[0]：这是一个叫 translation-audio 的 Cloud Run job。 | A3：job 照说（Cloud Run 的资源类型，也是考题选项里的词），量词“个”；这里不写“任务”（留给第 8 讲的微调任务、第 13 讲的训练任务），字幕里也不写“作业”（只用于书面，A4）。execution → 执行（这次执行）。控制台按钮 Execute 照写（我们点 Execute）。小写的 job 不放句首（A5）。 |
| translation audio / translation-audio / the same image / a translation web app that works perfectly | translation-audio / 翻译 web 应用 | S01[0]：它用的 image 和一个运行得好好的翻译 web 应用一样。 | SAY 把 job 名念成单词；字幕照画面写 translation-audio，英文行用 en_display 还原（D4）。web app → web 应用（第 7 讲：web 服务器）；app → 应用。 |
| task timeout / the output bucket / the platform stops it / 5 minutes | 任务超时 / 输出 bucket / 平台 | S01[1]：它一头撞上我们设的任务超时。 | 控制台字段 Task timeout 在画面上（英文）；旁白自己的话 → 任务超时。the output bucket → 输出 bucket（第 3 讲：bucket 照说）。5 分钟，平台把它停掉了。 |
| Dockerfile / default command / startup command / web server / troubleshooting table / symptom | Dockerfile / 默认命令 / 启动命令 / web 服务器 / 故障排查表 | S01[2]：线索在 Dockerfile 的最后一行：它的默认命令会启动 web 服务器。 | 旁白里的 CMD → 默认命令；startup command → 启动命令（两个启动命令）。web server → web 服务器（第 7 讲）。README 的故障排查表。 |
| Hold that question / five ideas / the quiz / exam questions / Tuesday | 考点 / 小测 / 考题 / 周二 | S01[4]：对这次小测来说，这一讲归结为五个考点。 | 复习课语体（A8）：idea（考试的知识点）→ 考点；the quiz → 小测（Quiz 4 只在画面上）；exam questions → 考题；the question（一道题）→ 题目；option → 选项；Tuesday → 周二。Hold that question → 先记着这个问题。Good luck on Tuesday → 周二小测加油。 |
| the gray tag / the lecture slide / slide n / the slides | 灰色标签 / 课件 / 课件第 n 页 | S01[5]：右上角的灰色标签，标出每个考点背后的那页课件。 | A10：the slides → 课件；slide 16 → 课件第 16 页（Slide 11 says → 课件第 11 页说）；the lecture → 课上；next lecture → 下一讲。标签本身（Lecture 14 · slide 14）保持英文（A11）。 |

### service 还是 job：看生命周期 / Service or job: the lifecycle

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Cloud Run service / service / a service / the service contract / Every deployed service | Cloud Run service / service | S02[2]：这种形状就是 service。 | A3：service 照说（Cloud Run 的资源类型，和考题选项一致），量词“个”；书面写“服务（service）”（A4）。the service contract → service 的约定。和服务账号（A7）、service 名称分开。小写的 service 不放句首：Service or job. → 是 service 还是 job。 |
| lifecycle / shape / Read the lifecycle, not the product names / runs to completion / exits / never finishes on purpose | 生命周期 / 形状 / 跑到完成 / 退出 | S02[7]：看生命周期，别看产品名。 | 全片的核心判断，S02 和 S08 同一个说法：看生命周期。shape → 形状；runs to completion → 跑到完成；exits → 退出；它本来就不会结束：监听就是它的本职工作。 |
| serve / batch / two startup commands / the demo app / the batch arguments / the command python | serve / batch / 演示应用 / batch 参数 / python | S02[0]：这个演示应用两种都有：一个 image，两个启动命令，serve 或 batch。 | A1 a：serve 和 batch 是应用的命令，照画面写；不放句首（这个 serve 命令……；而 batch 是另一种形状）。这里的 batch 是命令 ≠ S07 的“一批字符串”（A7）。batch 参数；命令用 python。 |
| gunicorn / port / 8080 by default / listening / listens on a port / request / requests / answers each request | gunicorn / port / 监听 / 请求 | S02[1]：然后它就等着，来一个请求就回答一个。 | gunicorn 照写（包名，小写，不放句首）。port 照说（第 2–4 讲）；默认 port 8080。listen → 监听；request → 请求（第 2 讲）。 |
| URL / instances / adds instances when traffic rises / scale to zero / traffic | URL / 实例 / 流量 / 缩容到零 | S02[2]：它有 URL，流量上来时加实例，流量停了可以缩容到零。 | instance → 实例（一个退出了的实例就是崩溃了）。scale to zero → 缩容到零；traffic → 流量。URL 照写。 |
| exits with status 1 / exit 0 / the execution shows failed / a false success | 退出码 / 失败 | S02[3]：如果某一步失败，它以退出码 1 退出，所以这次执行显示失败，而不是假的成功。 | 第 3 讲：exit status → 退出码（以退出码 1 退出）。时间条上的 exit 0 / exit 1 标签保持英文（A11）。 |
| the hook / inherited / the fix / the strip ends | 开头 / 继承 / 时间条 | S02[5]：这个 job 继承了 image 的默认命令，也就是 serve，所以它启动了 web 服务器，等着永远不会来的请求。 | Now the hook → 现在回到开头。The fix: → 修复：…… 时间条 = V1 的生命周期条（同一个 image，现在时间条有了尽头）。 |
| Cloud Scheduler / trigger / a nightly run / every night / on demand / timetable | Cloud Scheduler / 触发器 / 每晚 / 按需 / 时间表 | S02[6]：如果要每晚运行，常用的触发器是 Cloud Scheduler，不过这个 README 没有用它。 | Cloud Scheduler 照写（产品）。trigger → 触发器；每晚；按需；Cloud Scheduler 的时间表。Who presses start? → 谁来按开始？ |
| Try one / B, … / the right option / throttled / the loop stalls / crashed | 选项 / 节流 / 卡住 / 崩溃 | S02[8]：A 整个小时都在为一个实例付钱，而且空闲的 service 的 CPU 会被节流，所以循环会卡住。 | 思考题的揭晓以字母开头：B, a job … → 选 B，……；字母 A–D 照写（检查器忽略单个字母）。throttled → 节流；stalls → 卡住。Try one. → 来试一道。（A9：引子不暗示答案） |
| So the rule / the rule / pick a job / pick a service | 规则 | S02[9]：所以规则是：如果题目说它运行、写出结果然后退出，或者说它每晚运行，选 job。 | 规则卡片在画面上是英文（A11）；旁白的 the rule → 规则（所以规则是：／规则是：）。pick → 选。保持英文分句顺序（D9）：这里英文的 if 从句在前，中文也在前。 |

### 空闲时间谁来付钱：两个计价器 / Who pays for idle time: two meters

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| two meters / meter / the gold shading / the yellow ticks / one day | 计价器 / 金色阴影 / 黄色刻度 | S03[0]：我们把它说准确：两个计价器，一天。 | 第 1 讲：meter → 计价器（一直在走；往上涨；不动）。V2 的标注在画面上保持英文（A11）。 |
| virtual machine / VM / the VM row / from boot to shutdown / provisioned hours / provisioned time | 虚拟机 / VM / 预配的时长 / 开机 / 关机 | S03[1]：它的计价器从开机走到关机，不管有没有请求。 | 第 1 讲：virtual machine → 虚拟机（定义句），VM → VM（具体那台、那一行）；量词“台”。provisioned → 预配（Google Cloud 中文文档的说法）：空闲的小时仍然是预配的小时。 |
| idle time / idle / idle gaps / quiet gaps / zero idle cost | 空闲时间 / 空闲 / 间隔 / 零空闲成本 | S03[3]：现在把请求之间的安静间隔拉长。 | idle → 空闲（空闲时间；零空闲成本是有代价的）。 |
| function / a function / the function meter / Cloud Run functions / Cloud Functions | 函数 / Cloud Run functions / Cloud Functions | S03[3]：函数的计价器完全不动：没有请求，就没有费用。 | A3：function（serverless 产品、Python 函数、serving function）一律 → 函数，有意用同一个词：视频把入口点和 serving function 连在一起（S07[8]）。产品名照写（A1 b）：Cloud Run functions（现在的名字）、Cloud Functions（课件的名字）；不写“云函数”。 |
| request-based billing / billed / bill / which bill changes / pay-per-use bill / costs nothing between runs | 按请求计费 / 计费 / 账单 / 按用量计费 | S03[2]：下面一行是一个函数，或者一个按请求计费、最小实例数为 0 的 Cloud Run service，和 README 里一样。 | 第 1 讲：billed → 计费；bill → 账单（哪份账单会变？）；pay-per-use → 按用量计费；request-based billing → 按请求计费（README 的 Request-based 在画面上）。 |
| invocations / every invocation / execution time / running time / how long each one runs | 调用 / 调用次数 / 执行时间 / 运行时间 | S03[2]：它的计价器只随调用次数和每次运行多长时间而动。 | invocation → 调用（每次调用和它的运行时间）；作为计数 → 调用次数；execution time → 执行时间。 |
| cold start / minimum instances / minimum instances 0 / a warm instance / always on / always-on instance | 冷启动 / 最小实例数 / 热实例 / 常驻 | S03[4]：零空闲成本是有代价的，课件第 16 页点出了它：冷启动。 | cold start → 冷启动（标准译名）。minimum instances → 最小实例数（设成 1）；max instances → 最大实例数（只在画面上）。a warm instance → 热实例。always on → 一直开着；always-on things → 常驻资源；常驻实例。 |
| Vertex AI endpoint / endpoint / minimum replica count / deploy call / the part that costs money | Vertex AI endpoint / endpoint / 最小副本数 / 部署调用 | S03[5]：下一讲的 Vertex AI endpoint 也一样：它的部署调用要求最小副本数为 1，README 说这就是花钱的部分。 | 第 8 讲：endpoint 照说（书面“端点（endpoint）”，A4）。SAY 把 min_replica_count 念成单词 → 最小副本数（散文，不需要 en_display）。花钱的部分。 |
| serverless / serverless is cheap / no minimum charge / free work | serverless / 最低收费 | S03[8]：所以规则不是：serverless 很便宜。 | A1 c（新增）：字幕里 serverless 照说，中国工程师就这么说（serverless 部署；书面“无服务器（serverless）”，A4）。没有最低收费；免费干活（D 把没有最低收费和免费干活混为一谈）。 |

### 函数还是 container：你交出什么 / Function or container: what you hand over

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| hand over / deploy / deployment / redeploy / the serverless row | 交出 / 部署 / 重新部署 | S04[0]：课上用四种方式部署同一个翻译应用：虚拟机或 serverless，代码文件或 container。 | hand over → 交出（你要交出什么）。deploy → 部署（第 2 讲）；重新部署；一次部署。代码文件。VM 那一行 / serverless 那一行。 |
| source file / source / requirements file / requirements / main.py / one name | 源文件 / 源代码 / requirements 文件 / 依赖 / main.py | S04[1]：部署函数，你交出一个源文件、它的 requirements 文件，再加一个名字。 | main.py 照写（文件名，A1 a）。requirements 文件（画面上是 requirements.txt）；Cloud Build 安装依赖；源代码加入口点。 |
| hello underscore HTTP / hello_http / an HTTP handler / two language codes | hello 下划线 http / HTTP 处理函数 / 语言代码 | S04[1]：这个文件是 main.py：一个叫 hello 下划线 http 的 HTTP 处理函数，它从请求里读出文本和两个语言代码。 | A6：检查器拒收 hello_http；SAY 特意念出 underscore，因为名字必须一字不差，所以字幕也写 hello 下划线 http（照画面小写）；en_display 写 hello_http（D4）。 |
| entry point / the framework / Not the file name, and not the service name | 入口点 / 框架 / 文件名 / service 名称 | S04[2]：这个名字就是入口点：框架应该调用的那个 Python 函数。 | entry point → 入口点（Google Cloud 中文文档的说法；README 的 --entry-point 在画面上）。入口点填 main。 |
| Cloud Build / Functions Framework / Artifact Registry / publishes an image / build time / build | Cloud Build / Functions Framework / Artifact Registry / 构建 / 构建时 | S04[3]：这只在构建时发生一次，不是每个请求都来一次。 | 产品名照写（A1 b）。build → 构建（第 2 讲；然后由 Google 构建）；publishes → 发布；构建时。 |
| build logs / service logs / the job's execution logs / The function build fails | 构建日志 / service 日志 / 执行日志 / 构建失败 | S04[4]：函数构建失败，构建日志会告诉你原因。 | log → 日志（第 7 讲：服务器日志）。构建日志；service 日志；执行日志。 |
| without managing containers / Google still builds one | 管理 container | S04[5]：你不用管理它，但 Google 照样会构建一个。 | 课件第 11 页的说法，说得客气（A9）。manage → 管理。 |
| a finished image by its URL / builds nothing / built beforehand / base Python / default port / You control all three | 现成的 image / 基础 Python / 默认 port | S04[6]：它的 Dockerfile 选定了基础 Python、默认 port 8080，以及启动命令。 | image、container 照说（A2）。base Python → 基础 Python（参照 base image，A2）。这三样都由你控制。 |
| HTTPS URL / query string / new inputs / with no redeploy | HTTPS / 查询字符串 / 输入 | S04[7]：函数通过查询字符串接收新的输入，不用重新部署。 | query string → 查询字符串（带查询字符串的 URL 在画面上）。 |
| a container instance / A function is a container you did not write | container 实例 | S04[8]：函数就是一个不用你自己写的 container。 | 这一场的结论，S04 和 S08 同一个说法（image 由 Google 构建）。 |

### 谁能调用，以谁的身份运行，去哪看日志 / Who may call it, who it runs as, where to look

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| permission / two permission questions / public app / caller / the left door / the right door | 权限 / 公开应用 / 调用方 / 门 | S05[1]：左边的门是调用方。 | V4 的比喻按意思译：door → 门（左边的门）。caller → 调用方；calls out → 向外调用。permission → 权限。 |
| public access / Allow public access / 403 / turned away / before your code even runs | 公开访问 / 403 | S05[1]：不允许的话，没有权限的调用方会被 403 挡回去，你的代码根本不会运行。 | public access → 公开访问（控制台开关 Allow public access 在画面上）。403 照写（C1）。挡回去 / 挡住。 |
| service account / badge / translation demo runtime / roles / Agent Platform User / Service Usage Consumer | 服务账号 / 工牌 / translation-demo-runtime / 角色 / Agent Platform User / Service Usage Consumer | S05[2]：这个 web 应用戴着一个服务账号工牌 translation-demo-runtime，有两个角色：Agent Platform User 和 Service Usage Consumer。 | 第 1、5 讲：服务账号、角色；角色名照写（A1 a）。V4 的 badge → 工牌（一个比喻一个词）。SAY 把账号念成单词；字幕写 translation-demo-runtime，en_display 还原（D4）。完整的邮箱地址只在画面上。 |
| key / You do not create or download a key / No key file anywhere / default credentials / token / the attached account | 密钥 / 密钥文件 / 默认凭据 / token | S05[3]：哪里都没有密钥文件。 | key → 密钥（系列）；default credentials → 默认凭据（第 8 讲：credentials → 凭据）；token 照说（第 2–4 讲）。平台会给它一个 token。 |
| identity / your own identity / Service Account User / to attach / a deployment permission | 身份 / Service Account User / 挂到 / 部署权限 | S05[4]：这是部署权限，和工牌本身能做什么是两回事。 | identity → 身份（以谁的身份运行）。attach → 挂到。Service Account User 照写。 |
| Storage Object Viewer / Storage Object Creator / input bucket / output bucket / One badge per workload | Storage Object Viewer / Storage Object Creator / 输入 bucket / 输出 bucket / 工作负载 | S05[5]：一个工作负载一个工牌。 | 角色名照写；Agent Platform User 和 Storage 的角色各自单独成一个分句（G1）。workload → 工作负载。 |
| harder to debug / debugging / A finished build is not proof that it works | 调试 / 构建成功 | S05[6]：构建成功不代表它能用。 | debug → 调试（更难调试）。 |

### 预处理放在哪里 / Where preprocessing lives

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| preprocessing / preprocess / a trained model / serve a model | 预处理 / 训练好的模型 | S06[0]：想象两个客户端：一个手机应用，一个网页。 | preprocessing → 预处理（标准译名）。To serve a trained model → 要部署一个训练好的模型（serve 命令照写，A7）。 |
| client / clients / a phone app / a web page / thin client / client release | 客户端 / 手机应用 / 网页 / 瘦客户端 / 客户端发布 | S06[4]：这就是瘦客户端。 | 第 8 讲：client → 客户端。thin client → 瘦客户端（标准译名）。不用发布任何客户端；同步重新发布。 |
| gear / recipe / two copies / code bases | 齿轮 / 配方 / 副本 / 代码库 | S06[1]：这是同一份配方的两个副本，在两个代码库里。 | V5 的比喻：gear → 齿轮；recipe → 配方。code base → 代码库（≠ repo：演示 repo 照说，这个 repo 自己的客户端）。 |
| decode the JPEG / scale the pixels to between 0 and 1 / resize / 224 by 224 / normalize | 解码 / JPEG / 像素 / resize / 224 乘 224 / 归一化 | S06[1]：每个客户端都带着同一个齿轮：解码 JPEG，把像素缩放到 0 到 1 之间，再 resize 到 224 乘 224。 | A1 c（新增）：resize 照说，中国做视觉的工程师就这么说（一个有问题的 resize；不 resize）。decode → 解码；normalize → 归一化；scale → 缩放。224 乘 224（B3）。 |
| client-side brittleness / quietly receives another | 客户端的脆弱性 | S06[2]：课上把这叫做客户端的脆弱性。 | 课件第 13 页的术语 → 客户端的脆弱性（课件标签保持英文，A11）。 |
| raw JPEG bytes / base64 / base64 encodes / JSON / predict | 原始字节 / 字节 / base64 / JSON / predict | S06[3]：客户端发送原始的 JPEG 字节，用 base64 包起来，因为 JSON 装不了原始字节。 | bytes → 字节；base64 照写；做 base64 编码；调用 predict（方法名，A1 a）。 |
| version 1 / version 2 / roll back / rollback / ship / healthy | 版本 / 回滚 / 发布 / 恢复正常 | S06[5]：回滚到版本 1，两个客户端在同一瞬间恢复正常。 | roll back → 回滚；ship → 发布；版本 2。同样的回滚要付出什么代价？（思考题，不给答案，A9） |
| app store review / a web deploy / the clients disagree | 应用商店审核 / 网页部署 / 不一致 | S06[7]：它们上线的时间不同，在这中间，两个客户端的结果不一致。 | 应用商店审核；land → 上线；disagree → 结果不一致。 |

### 注册 serve：先预处理，再调用模型 / Register serve: preprocess, then model

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the chain / decode / convert to floats / four probabilities / one per cheese / classified | 解码 / 浮点数 / 概率 / 奶酪 / 分类 | S07[0]：这条链是：JPEG 字节，解码，转成浮点数，resize，模型，最后是四个概率，每种奶酪一个。 | probability → 概率；Nothing was classified → 根本没有做分类。奶酪的名字只在画面上。 |
| preprocess image / preprocess_image / returns an image, not an answer | preprocess image / 图片 | S07[1]：在这个 repo 里，preprocess image 做前三步，一次处理一张图。 | A6：preprocess_image → preprocess image（照 SAY）；en_display 写 preprocess_image（D4）。 |
| serving function / serving_function / a batch of strings / maps over each one / inference / bytes inputs | serving function / 一批字符串 / 推理 / bytes inputs / 键 | S07[2]：预处理和推理，在同一个函数里。 | A6：serving_function → serving function，bytes_inputs → bytes inputs（照 SAY；en_display 还原）。inference → 推理。一批字符串（A7：不是 batch 命令）。客户端要用的键。 |
| serve (the exam's name) / the function that preprocesses, then predicts / predict | serve / 预测 | S07[2]：考题可能把这个函数叫做 serve：不是 web 应用的 serve 命令，而是先预处理、再预测的那个函数。 | A7：serve 在这期视频里有两个意思，旁白把它们分开：web 应用的 serve 命令（S01–S02）和考题对 serving function 的叫法。predict → 预测。 |
| serving default / serving_default / export / registers / the model server / SavedModel / signature | serving default / 导出 / 注册 / 模型服务器 / 签名 | S07[3]：导出时把它注册在 serving default 这个名字下面，模型服务器调用的就是这个名字背后的东西。 | A6：serving_default → serving default；en_display 写 serving_default。register → 注册；export → 导出；模型服务器；signature → 签名 / serving 签名（书面“签名（signature）”）。SavedModel 只在画面上。 |
| plugs / socket / the raw model / float arrays / float tensors / no longer fit | 插头 / 插座 / 原始模型 / 浮点数组 / 浮点张量 | S07[6]：它要的是浮点张量，所以 JPEG 字节插不进去。 | V6 的比喻：plug → 插头，socket → 插座（试插头之前）。原始模型；tensor → 张量；浮点数组。 |
| the test step / feeds it bytes inputs / one exported version | 测试步骤 / 导出的版本 | S07[7]：这个 repo 的测试步骤加载 serving default，喂给它 bytes inputs，和服务器的做法一样。 | A5：句子以“这个 repo”开头（repo 不放句首）。 |
| the platform calls exactly the name you registered / downstream | 平台 / 下游 | S07[8]：这和函数的入口点是同一个道理：平台只调用你注册的那个名字，名字错了，下游什么也补救不了。 | 这句把入口点和 serving default 连起来（S07[8]、S08[2]），两处同一个说法：平台只调用你注册的那个名字。 |

### 周二的七条规则 / Seven rules for Tuesday

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Seven rules / One: … Seven: / Which one to use? / rule of thumb | 七条规则 / 第一 / 经验法则 | S08[0]：周二的七条规则。 | 回顾里的序号：One: → 第一：……Seven: → 第七：。rule of thumb → 经验法则。 |
| Vertex AI / serve a trained model in production / part of a broader app | Vertex AI / 生产环境 / 更大的应用 | S08[3]：下一讲的经验法则：Vertex AI 用来在生产环境部署训练好的模型，Cloud Run 用在模型只是更大应用一部分的时候。 | D9：保持英文顺序，每个分句产品名在前（Vertex AI 用来……，Cloud Run 用在……的时候）；不要把 when 从句挪到产品名前面。 |
| vendor lock-in / cold starts / harder debugging | 厂商锁定 / 冷启动 / 更难调试 | S08[3]：还要记住课件第 16 页说的代价：厂商锁定、冷启动、更难调试。 | 课件第 16 页的三个代价，用顿号列举（B2）。 |

### 课程、名字与产品 / Course, names, products

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / the lecture / the slides / the instructor / next lecture / lecture n | AC215 / 课上 / 课件 / 授课老师 / 下一讲 | S04[0]：前面几讲填好了 VM 那一行。 | A10（第 1–8 讲）。授课老师从不提名字。Earlier lectures → 前面几讲。 |
| products: Google / Google Cloud / Cloud Run / Cloud Build / Artifact Registry / Cloud Scheduler / Vertex AI / Agent Platform / Docker / Python / JSON / JPEG / HTTP / HTTPS / URL / CPU | Google / Cloud Run / Vertex AI / Agent Platform / Python / JSON / JPEG / HTTP / HTTPS / URL / CPU | S02[0]：课上说，Cloud Run 可以把一个 container 作为 service 或 job 来运行。 | 拉丁字母（A1 b）。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上面各词条 zh_subtitle 和 first_use 里的拉丁词，字幕行还可以出现下面这些（实物按检查器的切法切开，D3）：

AC、Account、Agent、AI、Artifact、base、batch、bucket、Build、bytes、Cloud、Consumer、container、CPU、Creator、default、Docker、Dockerfile、endpoint、Execute、Framework、function、Functions、functions、Google、gunicorn、hello、HTTP、http、HTTPS、illustration、image、inputs、job、JPEG、JSON、main、main.py、MLOps、Object、Online、Platform、port、predict、Prediction、preprocess、Python、python、Quiz、README、Registry、repo、requirements、resize、Run、SavedModel、Scheduler、serve、serverless、Service、service、serving、Storage、token、translation-audio、translation-demo-runtime、URL、Usage、User、Vertex、Viewer、VM、web。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只留在三类地方。（a）**实物**，逐字照抄：应用的命令和修复 job 用的命令（serve、batch、python）、文件名（Dockerfile、main.py；requirements.txt 只在画面上，旁白说 the requirements file → requirements 文件）、画面上的 job 名和账号名（translation-audio、translation-demo-runtime）、旁白点名的控制台字样（Execute）、角色名（Agent Platform User、Service Usage Consumer、Service Account User、Storage Object Viewer、Storage Object Creator）、状态码 403、按旁白念法写的代码名（A6：hello 下划线 http、preprocess image、serving function、serving default、bytes inputs）、方法名 predict、包名 gunicorn、格式名（JPEG、JSON、base64）。（b）**产品、组织和课程**：AC215、Google、Google Cloud、Cloud Run、Cloud Run functions、Cloud Functions、Functions Framework、Cloud Build、Artifact Registry、Cloud Scheduler、Vertex AI、Agent Platform、Docker、Python、README、HTTP、HTTPS、URL、CPU、VM。（c）**实验课口语里的英文，封闭清单**：第 1 讲的 repo；第 2–4 讲的 container、image、port、token、Dockerfile、bucket；第 8 讲的 endpoint；**这期新增 service 和 job（Cloud Run 的两种资源类型，和考题选项的说法一致）、serverless、resize**。只有实验课真的说英文、中文说法生硬或撞词时，才加入（c）。函数、入口点、冷启动、实例、计费、空闲、调用、预处理、推理、签名、回滚、客户端、部署以及 A3 里的一切，一律中文。
- **[A2]** container 和 image（同第 2–8 讲）。字幕说 container、image：一个 container 实例、同一个 image、现成的 image；量词“个”。build → 构建，publish → 发布，base Python → 基础 Python。标题、章节名和 meta.yaml 写“容器”“镜像”（A4）。
- **[A3]** serverless 词汇（这期新增）。生命周期一串：service、job 照说（A1 c），lifecycle → 生命周期，跑到完成，退出，退出码，execution → 执行，listen → 监听，请求，实例，流量，缩容到零，触发器，每晚，按需，时间表，任务超时，默认命令，启动命令，web 服务器，web 应用。计费一串：计价器（第 1 讲）、计费、账单、按请求计费、按用量计费、调用 / 调用次数、执行时间、空闲、预配、虚拟机 / VM、冷启动、最小实例数、热实例、一直开着 / 常驻、最小副本数、没有最低收费。交出什么一串：function → 函数（产品、Python 函数、serving function 都一样）、入口点、交出、源文件、源代码、依赖（文件说 requirements 文件）、HTTP 处理函数、查询字符串、构建、构建时、构建日志、部署、重新部署。身份一串：权限、调用方、公开访问、服务账号、角色、密钥、默认凭据、身份、部署权限、工作负载、日志、调试。模型 endpoint 一串：预处理、推理、客户端、瘦客户端、客户端的脆弱性、解码、归一化、字节、张量、概率、回滚、版本、发布、应用商店审核、注册、导出、模型服务器、签名、经验法则、厂商锁定。视频的比喻按意思译，一个比喻一个词：时间条、计价器、金色阴影、门、工牌、齿轮、配方、插头 / 插座。
- **[A4]** 字幕与书面。字幕说 container / image / repo / bucket / token / endpoint / service / job / serverless / resize；标题、章节名、meta.yaml 和配套文档写 容器 / 镜像 / 仓库 / 存储桶 / 词元（token）/ 端点（endpoint）/ 服务（service）/ 作业（job）/ 无服务器（serverless）/ 调整尺寸（resize），核心概念第一次出现时括注英文（旁白以外可以用括号）。“作业”沿用 Google Cloud 中文文档（Cloud Run 作业），只用于书面。命令和代码名不受影响。
- **[A5]** 实物的写法。逐字照抄；不翻译、不变形、不加引号或《》。需要时加中文中心词：这个 serve 命令、batch 参数、service 名称、service 日志、Agent Platform 角色。句子不以实物或小写的英文词开头（serve、batch、gunicorn、job、service、serverless、resize、repo、endpoint），先放一个中文词（这个 serve 命令……；而 batch 是……；是 service 还是 job；这个 repo……；这个 job……）。大写的名字和缩写（Cloud Run、Cloud Build、Google、README、Dockerfile、JSON、VM、Vertex AI）可以放句首，选项字母 A–D 也可以。
- **[A6]** 带下划线的名字（同第 3–8 讲）。没有 say: 时，检查器把显示行当朗读文本，拒收 letter_letter、括号和 =。所以中文行按旁白的说法写：hello_http → hello 下划线 http（SAY 特意念出 underscore，因为名字必须一字不差；照画面小写）；preprocess_image → preprocess image；serving_function → serving function；serving_default → serving default；bytes_inputs → bytes inputs；min_replica_count → 最小副本数（SAY 当普通话说）。英文行用 en_display 给出字面形式（D4）。
- **[A7]** 要分清的词。service（Cloud Run 资源）≠ 服务账号 ≠ service 名称。serve（web 应用的命令，S01–S02）≠ serve（考题对 serving function 的叫法，S07[2]）；旁白把两者分开，字幕也分开（不是 web 应用的 serve 命令，而是……）。batch（应用的命令）≠ 一批字符串（S07）。“函数”有意只用一个词，指产品、Python 函数和 serving function（S07[8] 把入口点和 serving default 连起来）。job ≠ 任务（第 8 讲的微调任务、第 13 讲的训练任务）≠ 作业（只用于书面）。执行（job 的一次执行）≠ 运行。实例 ≠ 版本 ≠ 修订版本（revision，只在画面上）。发布（发布版本、发布 image、发布客户端）≠ 部署。调用 ≠ 调用方。计费 ≠ 账单 ≠ 付钱。规则（exam rule）≠ 考点（五个考点之一）。课件 ≠ 课上 ≠ 下一讲。repo（演示 repo）≠ 代码库（S06[1]）。
- **[A8]** 语体：考前一天的复习课助教。句子短而直接；讲到考试时用考试的词（考点、题目、选项、选 B、考题、小测、规则是：）；观众是“你”（不用“您”“大家”“同学们”）；“我们”是视频（我们点 Execute）。分句内部用中文语序，分句顺序跟英文走（D9）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句。不用网络流行语。口语节奏按意思传达：来试一道；换个新情况试试；现在回到开头；先记着这个问题；看；该用哪一个？；周二小测加油。
- **[A9]** 准确。量词照译：only 只，every 每个 / 每次，all 全部，at once 同时，exactly 正好 / 完全，never 从不 / 永远不。数字照旁白（C1）。课件和 repo 的差异说得客气、简短，和 SAY 一样（课件里的 Cloud Functions 现在叫 Cloud Run functions；课件用另一种调用来保存它）。思考题：三张卡片加一句（S02[7] 来试一道；S03[6] 换个新情况试试；S06[6] 同样的回滚要付出什么代价？；S07[4] 试插头之前，最后检查一次）。引子和题干不能泄露答案：S02[7] 不暗示 job 或 Cloud Scheduler；S03[6] 不说哪份账单会变；S06[6] 不提两次发布或应用商店；S07[4] 不点出 serving function。揭晓和英文一样以字母开头（B, … → 选 B，……；Try B first → 先试 B）。课程的练习题从不引用，这里和 i18n/zh 里的任何文件都一样。
- **[A10]** 名字。产品、公司和课程保留拉丁字母（A1 b）；“哈佛”只出现在标题和简介里。课程：AC215；the lecture → 课上；the slides → 课件；slide n → 课件第 n 页；next lecture → 下一讲；earlier lectures → 前面几讲；the instructor → 授课老师，从不提名字（旁白从不提任何人名）。服务账号的邮箱、项目 ID、bucket 路径和 image 标签只在画面上，绝不写进中文行。奶酪的名字只在画面上。
- **[A11]** 画面保持英文。这个系列只翻译旁白：代码面板（包括注释）、README 摘录和摘录小卡、示意的控制台小卡、课件标签（Lecture 14 · slide 14）、V1–V6 的标注、考点图、规则卡片、思考题卡片和下面的理由、标签（illustration）以及回顾的各行都是英文，场景不用为中文改动。旁白点名画面上的东西时照画面写（我们点 Execute；translation-demo-runtime）；旁白自己的话要译（灰色标签、黄色刻度、金色阴影）。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、网络、视频、信息、账号、函数、参数、字段、配置、内存、日志、部署、实例；不用 預設、程式、程式碼、檔案、網路、影片、帳號、函式、引數、欄位、組態、記憶體、日誌 等繁体或台湾用语。
- **[A13]** 系列清单在这期的情况。container 和 image 贯穿全片；Dockerfile（S01、S04）；port（S02、S04）；token 一次（S05[3]）；bucket（S01、S05）；endpoint（S01、S03、S06–S08）；repo（S06、S07）。pipeline、volume、venv、PATH、prompt、embedding、CI、agent（只在角色名和产品名 Agent Platform 里）这期没有。新增保留英文的（A1 c）：service、job、serverless、resize。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（输出 bucket、退出码 1、课件第 16 页、224 乘 224、默认 port 8080、被 403 挡回去）。检查器对每个显示句都查空格。实物内部的空格照原样（Cloud Run、Service Usage Consumer）。全角标点旁边不加空格。不用 U+00A0 / U+202F。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，挨着实物也一样。列举用 、（厂商锁定、冷启动、更难调试）。不用任何括号。“”只用于译出来的引文；实物、界面字样和角色名不加引号。每个中文句子（对应一个英文句子）内部没有 。？！：用 ，；：。回顾的序号后面用全角冒号（第一：看生命周期。）。
- **[B3]** 检查器拒收的符号（= < > + → × ÷ ≈、括号、letter_letter、数字后面的 !）：绝不进中文行，用文字说。224 乘 224；0 到 1 之间；源代码加入口点。可以照画面保留的：main.py 里的 .，translation-audio、translation-demo-runtime 里的 -。

### C. 数字与单位

- **[C1]** 数字。SAY 用阿拉伯数字写的，一律阿拉伯数字（8080、403、224 乘 224、5 分钟、退出码 1、版本 1 / 版本 2、最小实例数为 0 / 设成 1、课件第 11 页 / 第 16 页）。SAY 用单词写的小数目用汉字：五个考点、两个启动命令、两个计价器、四种方式、两个权限问题、两个角色、两个客户端、前三步、四个概率、七条规则、三样。回顾的序号用汉字：第一……第七。没有价格和免费额度数字（稿子里也没有）。
- **[C2]** 单位和时间。5 分钟；每小时一次；整个小时；一天；周二。哈希、image 标签、项目 ID 和 commit 从不念出。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 逐句对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每个 SAY 行都有一条（66 段）；`en` 和 SAY 行逐字节相同；`zh` 的条数和 explainer.voice.split_sentences 切出的英文句子数完全一样（这份稿子 191 句）。只在句子内部调整，绝不合并或拆分句子。短句单独成条：几分钟过去了。／先记着这个问题。／是 service 还是 job。／现在回到开头。／来试一道。／哪份账单会变？回顾里英文单独成句的规则，中文也单独成条。运行 `python -m explainer.i18n check videos/ac215-l14-exam --lang zh`，直到输出 OK。
- **[D2]** 不写 say:，不写 anchors。没有中文配音：绝不写 say:，也绝不写 anchors:。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：不用括号（B2），不用数学符号（B3），不出现 letter_letter 名字（A6），数字后面不跟 !，分句不能以“种”结尾再接 ，。！？（“两种都有”这样在分句中间没问题），汉字和拉丁字母或数字之间有半角空格（B1），每句以 。！？ 或 …… 结尾，每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用 [A-Za-z][A-Za-z'.-]* 切词，忽略单个字母：base64 是 base，main.py、translation-audio、translation-demo-runtime 整个算一个词，选项字母 A–D 被忽略。报出来的拉丁词要么是该译的英文（通常如此），要么是漏掉的实物：按同样的切法加进 allowed_spoken_latin 和对应词条。故意不收复数（instances、requests、clients、roles、images、containers）：报出复数就是该去掉的英文词形变化。只有产品名 Cloud Run functions、Cloud Functions、Functions Framework 里的复数是允许的。
- **[D4]** 英文行（en_display）。双语字幕带显示 SAY 句子，而 SAY 为了配音把一些实物念成了单词。每个这样的句子都要在 en_display 里给出屏幕上的字面形式，其余照 SAY 逐字写；同一段里的其他句子写 null。念法 → 字面：translation audio → translation-audio（S01[0]）；hello underscore HTTP → hello_http（S04[1]）；translation demo runtime → translation-demo-runtime（S05[2]）；preprocess image → preprocess_image（S07[1]、S07[2]、S07[5]）；serving function → serving_function（S07[2]、S07[7]；S08[2] 可选，回顾可以保留单词）；bytes inputs → bytes_inputs（S07[2]、S07[7]）；serving default → serving_default（S07[3]、S07[7]）。不还原的：minimum replica count（散文）、the requirements file（散文）、main.py、8080、403（本来就是字面）。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它自己的英文句子：不添加命令、括注、中文界面名或解释；保留英文的词不加中文解释（英文行就在下面）；思考题不给答案（A9）。A5 需要的几个开头词（这个、这次、而、是）不带内容。
- **[D6]** 固定说法。来试一道。／换个新情况试试。／试插头之前，最后检查一次。／选 B，……；选 C，serving function：……／先试 B：……／所以规则是：……／规则是：……／看生命周期，别看产品名。／函数就是一个不用你自己写的 container。／平台只调用你注册的那个名字（S07[8] 和 S08[2]）。／周二的七条规则。／第一：……第七：……／周二小测加油。
- **[D7]** 文件。narration/g1.yaml = S01–S04（开头、service 还是 job、两个计价器、交出什么；34 段、103 句），narration/g2.yaml = S05–S08（身份和日志、预处理、serving 签名、回顾；32 段、88 句）。视频不分部分，两个文件只是分工。每个文件开头写一段注释（覆盖范围；用到的规则：A6 空格形式、B3 符号用文字、C1 数字、D4 en_display、不写 say: / anchors:），保持稿子的顺序。用双引号字符串；YAML 里的双引号和反斜杠要转义。
- **[D8]** 按英文时间轴的长度。中文在英文播放时被阅读；字幕带在英文字幕切换的地方切换。每句中文的阅读时间要和英文差不多：每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以去掉多余的连接词和重复的主语，绝不删内容。长实物也占长度（translation-demo-runtime 13.2 个单位，Service Usage Consumer 12.7，Storage Object Creator 12.1）：英文没重复的地方不要重复；第二次提到时用简短的指代（这个账号、这个函数、这个 job）。
- **[D9]** 保持英文的分句顺序（系列教训，ac215-video skill）。工具链按分句把中文和英文配对；英文把条件放在后面，中文却放在前面，相邻两个字幕块的意思就会对调。条件、目的和时间状语放在英文放的位置：把预处理放在 endpoint，只有在 endpoint 调用了正确的函数时才有用；Vertex AI 用来在生产环境部署训练好的模型，Cloud Run 用在模型只是更大应用一部分的时候；函数构建失败看构建日志，请求失败看 service 日志（每一对条件和结果在同一个分句里，分句内部可以用中文语序）。英文以 if 开头的地方（S02[9]、S08[0]），中文也以“如果”开头。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一个字幕块 2 行。分句最好不超过大约 24 个单位，用 ，；： 隔开，给切分器留出干净的切点；角色名和 translation-demo-runtime 单独成一个分句。
- **[G2]** 字幕块结尾：工具链会去掉字幕块末尾的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。句末用中文词比用“实物 + 句号”更稳。
- **[G3]** 绝不拆开名字。切分器把中文行里两个拉丁词之间的空格当作好切点，所以 Service Usage Consumer、Cloud Run functions 可能被拆到两行。把这样的名字放在分句末尾、全角冒号或顿号后面，周围少放中文；在渲染出来的 .zh.srt 里检查每个带角色名的字幕块。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频和章节标题用书面语体（A4：容器、镜像、服务、作业、端点、无服务器）；问句保留问号；保留英文的冒号结构（服务还是作业：……；注册 serve：……）；代码名照写（meta.yaml 不经过检查器，可以用括号）。中文不是常用搜索词的核心概念，章节名带英文简称方便搜索（作业（job）、服务（service）、端点（endpoint）），和第 1–8 讲一样。exam edition → 考前精讲版（第 4 次小测几期考前版的统一说法；follow-along → 跟练）。Serverless Deployment → 无服务器部署。
- **[H2]** 简介（B 站 / YouTube）：两三句话，书面语体，用这份词表的词：AC215 第 14 讲面向第 4 次小测的考前精讲版，概念优先，以演示仓库 dlops-io/serverless-deployment 和 dlops-io/model-deployment 为依据；讲什么（按生命周期区分 Cloud Run 服务和作业；空闲时间谁付钱；函数和服务各交出什么；谁能调用和以谁的身份运行；预处理放在端点和 serving 签名）；英文旁白，配中文和中英双语字幕；不做现场运行：每个面板都是仓库源码或我们自己的示意图。不出现人名，不出现练习题。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md）用这份词表、按书面语体翻译（A4）。末尾附术语表：English | 这里的说法 | 其他常见译法（serverless：无服务器 / Serverless；service：服务；job：作业 / 任务；function：函数 / 云函数；entry point：入口点 / 入口函数；cold start：冷启动；minimum instances：最小实例数；scale to zero：缩容到零；service account：服务账号 / 服务帐号；preprocessing：预处理；inference：推理；signature：签名；rollback：回滚；thin client：瘦客户端；endpoint：端点 / 终端节点）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 都不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]** （请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读文本的检查（_SPOKEN_BAD）。对只有字幕的视频（这里 voice: none），这些检查什么也保护不了，反而逼出了 A6 和 B3（这里：hello_http、preprocess_image、serving_function、serving_default、bytes_inputs）。建议：词表的 voice 为 none 时，纯显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。
- **[I2]** （待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当作好切点，所以名字可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
- **[I3]** （说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：每个词条 en 字段里 2–3 个词的英文说法会保持在同一行英文里，zh_subtitle 里 2–7 个汉字的中心词会注册进 jieba，对所有视频的字幕都生效。所以这份文件的 en 和 zh_subtitle 只列真正的术语（不写句子）。
