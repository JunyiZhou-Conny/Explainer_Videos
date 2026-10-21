# AC215 第 7 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 7 — LLM: Agents II (follow-along: agent-harness)*（`videos/ac215-l07-agent-harness`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会读 Python（async / await、dataclass 和装饰器能读懂）；做过第 1 讲（uv、pyproject.toml、uv.lock）、第 2–4 讲（container、docker-shell.sh）、第 5 讲（RAG）和第 6 讲（函数调用、agent 循环和它的上限、MCP，以及 Colab notebook 里最早的 harness 思路：审批关卡、由 Python 算账、回执）；从没自己搭过 agent harness；开着自己的 `~/AC215/agent-harness`、Docker 在运行，有 OpenAI 密钥（开通了计费）就更好，或者用课程的 Agent Harness Colab notebook，边看边敲命令
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l07-agent-harness.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5，数字和符号怎么念）都不适用，只保留显示规则
英文原稿：`script.md` v2（SAY 行是旁白：155 段、339 句；第一部分 S01–S07 是 68 段、148 句，第二部分 S08–S16 是 87 段、191 句）；script.md 开头的 en_display 候选清单、i18n 词表备注（章节名里的比喻、几个习语），以及 `build/review_spoken.md` 第 4、8、9、11、17 条（方法名、易误译的说法、中文语序会跨字幕块的三句、en_display 补充、章节名）都已并入
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词（repo、clone、commit、pin、lock 文件、shell、笔记本、来想一个问题）；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md)、[`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md)、[`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md) 定下容器、密钥、网络的词（层、指纹、进程、shell 历史记录、拆掉）和“只有字幕”的整套规则；[`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md) 定下 RAG 的词（检索、元数据、哈希、通道、一个小疏漏）；[`ac215-l06-agents-1`](../../../ac215-l06-agents-1/i18n/zh/GLOSSARY.md) 定下 agent 的词（agent、notebook、session、harness、工具调用、循环、规划器、批准、回执、交接、上下文工程）。前六讲已经定下的词一律沿用；新的是 harness 本身的词汇（harness 层、准入、审计、行动边界、上下文包、工作流图、指纹、审批单、压缩、胶囊、skill、评测，A3）
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“看一下 trace”“加载一个 skill”“用 fixture 跑一遍”“换一个 label”“diff 一下”“这个 harness”“token 用了多少”“跑一下这个 notebook”。在实验课上硬说“执行记录”“技能”“测试夹具”“标签”，反而像说明书，而且“标签”已经是画面上的 tag；这些书面词留给标题、章节名和配套文档（A4）。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、代码面板和 Colab 里找东西。命令、参数、场景名、label、文件名、类名、终端原文、事件名、模型 ID、奶酪的商品名一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（工具调用、循环、工作流、上下文窗口、压缩、截断、白名单、校验、审批、指纹、哈希、回执、渐进式披露、测试用例、基线、评测集）一律说中文，用中文 agent 工程资料里能搜到的标准译名。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、录下来的输出框、Colab 示意图、标签、进度条、V1 表格和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“pull 下来”“把 repo clone 下来”“写 prompt”“这个 agent”“跑一下 notebook”“建一个 session”，第 6 讲又引入了 harness；这一讲再加上“看一下 trace”“加载一个 skill”“用 fixture 跑”“换一个 label”“看 diff”。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（中文 agent 工程资料：上下文工程、上下文窗口、压缩、截断、渐进式披露、白名单、结构化输出、测试用例、评测集、基线、交接）；和整个系列一致（第 1 讲定下共用的词，第 2–4 讲定下容器、密钥和网络的词，第 5 讲定下 RAG 的词，第 6 讲定下 agent 的词：它们定下的说法全部保留）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、场景 / 模式 / label 的值、文件名和目录名、路径、类名和层名、代码里的值、终端原文、状态名和事件名、模型 ID、包名、店里数据里的奶酪名、Colab 界面上的字样、README 的标题、画面上的标签）逐字照抄，不翻译、不变形、不加引号。检查器逼出来的例外：带下划线的名字，以及 = + < > ( ) [ ] 这几个字符，按旁白的说法写（A6、B3）。终端输出、代码面板、README 卡片、录下来的输出框、Colab 示意图、标签、进度条、课件标签、图里的文字、V1 表格和思考题卡片都是英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的 container、image、base image、pull、port、API、ID、token、Dockerfile；第 5 讲的 prompt、system prompt、LLM、agent、CLI；第 6 讲的 notebook、session、schema、SDK、harness；**这一讲新增 trace、skill、fixture、label、diff、run ID**。
3. **其余一律用中文标准术语**：工具、工具调用、循环、轮、消息、层、环、准入、审计、预算、兜底、上下文、上下文包、空位、政策、规则、校验、重新校验、验证、检查、工作流、图、节点、边、修订、结账、购物车、订单、下单、批准、审批、审批单、指纹、哈希、回执、审核、经理、宿主程序、规划器、记忆、历史、状态、任务、压缩、胶囊、截断、上下文窗口、隔离、白名单、防线、检测器、元数据、参考资料、资源文件、渐进式披露、管理者模式、交接、评测、测试用例、测试集、基线、批次、报告、记分卡、混杂改动、评委、结果、轨迹、成本、证据、在线、离线、脚本模拟。
4. **视频的比喻按意思译，一个比喻一个词**：两栏（two columns）、环和内环（rings）、闸机（turnstile）、接缝（seam）、筛子（sieves）、通道（lanes，沿用第 5、6 讲）、轨道和站（rails、stations）、抽屉（drawers）、胶囊（capsule）、说明书和钥匙（manuals、keys）、手和插座（hands、socket）、回执（receipt，第 6 讲）。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、基础镜像、仓库、克隆、提交、端口、提示词、系统提示词、智能体（agent）、会话（session）、Colab 笔记本（notebook）、技能（skill）、执行记录（trace）；harness 书面也保留英文。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **工具链的约束也是规则**：每个英文句子对应一个中文句子（155 段、339 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **主线一句话，全片同一个说法**：the model proposes; the harness decides → 模型提议；harness 决定。propose → 提议，decide → 决定；两栏 → 左边是模型负责的部分，右边是 harness 负责的部分。harness 照说（第 6 讲已定，书面也是 harness），小写，不放句首：所谓 harness……、这个 harness……（A5）。
- **trace、skill、fixture、label、diff 照说**（A3）：都是屏幕上天天出现的词（Trace 层、`SKILL.md`、`--fixture`、`--label`、`diff -u`），实验课上也这么说；书面写“执行记录（trace）”“技能（skill）”“测试夹具（fixture）”。label 照说还因为“标签”已经是画面上的 tag（灰色标签、your turn 标签）；trust label 另译“信任标注”（A7）。
- **live → 在线，offline → 离线**：画面上成对出现 offline · free 和 live · billed per token；live 指真的调用模型、按 token 计费：在线命令、在线运行、在线模型。不写“实时”（第 3 讲的 live view 才是实时视图），字幕里不写 live。scripted → 脚本模拟的（画面上的 scripted 标签保持英文）。
- **四个 harness 层用类名**：Trace、Budget、Context、CartCheck 照画面写（Cart Check → CartCheck），可以放句首；概念说中文：budget → 预算，context → 上下文。layer → 层，ring → 环，inner ring → 内环，admission → 准入，audit → 审计，fallback → 兜底。
- **Act → 幕**：README 的六个 Act 是一出戏的六幕：第 1 幕……第 6 幕；`--act n` 和进度条在画面上保持原样。
- **request 分两种**（A7）：顾客的需求 → 需求（已确认的需求、今天的需求、宿主程序确认这些需求）；API 或工具的请求 → 请求；Request 1 / Request 2 → 订单 1 / 订单 2。
- **人和程序**（A7）：店里的 manager（你来扮演）→ 经理（经理审批、经理审核）；课上的 manager pattern → 管理者模式；the host（运行 harness、接收审批的应用）→ 宿主程序。approve / decline 是要输入的值，照写。
- **审批的一串词**：approval → 批准（流程叫“审批”：经理审批、审批抽屉、审批单、审批顺序）；fingerprint → 指纹（第 2 讲），hash → 哈希（第 5 讲），SHA-256 照写；ticket → 审批单；receipt → 回执（第 6 讲）；checkout → 结账；validate / revalidate → 校验 / 重新校验；recheck → 重新检查；verify（环境、课上的 Verify 步骤）→ 验证。
- **记忆的一串词**：compaction → 压缩，truncation → 截断，context window → 上下文窗口，capsule → 胶囊，pin（胶囊）→ 钉上（给版本 pin 照说 pin），quarantine → 隔离，allowlist → 白名单，guards → 防线，backstop → 保险，fallback → 兜底。
- **评测的一串词**：evaluation → 评测，test case → 测试用例，case → 用例，scenario → 场景，suite → 测试集，baseline → 基线，batch → 批次，outcome / trajectory / cost → 结果 / 轨迹 / 成本（检查名前缀 outcome、process 照写），improved / regressed / unchanged → 改进 / 退步 / 不变，confounding changes → 混杂改动，judges → 评委，eval set → 评测集。
- **带下划线的名字和代码表达式**（A6、B3，同第 3–6 讲）：build_agent → build agent 这个函数；preview_order → preview order 工具；get_catalog、get_stock、load_skill、read_skill_resource、start_order、get_order_status、assess_event、build_act4 → 空格形式；"order_placed": False → order placed 设为 false；no_cart → no cart；approval_mode="always_require" → approval mode 设为 always require；OPENAI_API_KEY → OpenAI API key；RUN_ID → run ID；harness.without("trace") → harness without trace；.add() / .without() → add 和 without 方法；Context("basic") → basic Context。英文行用 en_display 给出字面形式（D4）。
- **名字**（A10）：两位顾客只说“第一位顾客”“第二位顾客”，他们的 ID 和名字绝不出现在任何中文行或文件里（画面上是遮住的标记）。奶酪用店里数据的商品名，带重音符号：Comté、Époisses、Bûcheron、Taleggio、Mimolette、Munster、Brie（观众要在输出里对照）；地名写中文（宾夕法尼亚、纽约）。授课老师不提名字。
- **勘误统一说“一个小疏漏”**（第 5、6 讲 A9），后面紧跟改法；a harmless slip → 一个无害的小疏漏。**录制时**：at the time of recording 每次都译“录制时”，绝不省略。
- **打印出来的结局照写**（A9）：旁白对比或点名一次运行打印出来的结局时，照屏幕写（最后是 UNRESOLVED，不是 BLOCKED；结果：DECLINED；status 为 saved；状态 placed）；叙述用中文动词（拦下、下单、结束）。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）：每句中文读起来的时间要和英文听起来差不多；条件和主句的先后跟着英文走；review_spoken 第 9 条点名的三句（S05[0]、S09[2]、S06[2]）按 D9 的写法。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令（git clone、ls -a、bash docker-shell.sh、docker ps、docker images、docker inspect、docker exec、docker ps -a、docker image rm、exit、python cli.py --help、python cli.py --act 1 --scenario standard、diff）、参数（--compare、--show-json、--preview-context、--fixture、--inspect-run、--prompt-file、--model、--rm）、场景和模式的值（standard、personalized、missing-details、basic、enriched……）、label（context-fixture-1）、文件名和目录名（docker-shell.sh、Dockerfile、agent-harness、secrets、docs、outputs、SKILL.md、scripts、tasting-planning、vendor-outreach）、类名和层名（Trace、Budget、Context、CartCheck）、代码里的值（OK、null、false、true、approve、decline、no cart、error、allow、placed、saved、no）、终端和 trace 原文（Requested tools、Tool call、Maximum of 8 model calls reached、Retrieved context、Invalid or unauthorized、UNRESOLVED、BLOCKED、DECLINED、status、email transmitted）、事件名（approval.requested、approval.decided、policy.decision、order.placed、run.finished、model.failed）、检查名前缀（outcome、process）、包名和模型 ID（agent-framework、gpt-5.6-luna）、README 的字样（Inspect the context first、Setup）、Colab 界面的字样（Save a copy in Drive、Notebook access、secret）、旁白提到的画面标签（your turn），以及 A6 的空格形式（build agent、preview order、get catalog、get stock、load skill、read skill resource、start order、get order status、assess event、build act 4、order placed、approval mode、always require、OpenAI API key、run ID、harness without trace、basic Context、propose cart）。完整清单见 A1（a）。
- 产品、组织、课程和名字：AC215、OpenAI、Google、Agent Platform、Vertex AI、Docker、Colab、Drive、Jupyter、Python、SQLite、HTML、HTTPS、JSON、SHA-256、SDK、CLI、MCP、LLM、pytest、unittest、README、奶酪的商品名（Comté、Époisses、Bûcheron、Taleggio、Mimolette、Munster、Brie）、PA、NY（A1 b）。
- 实验课口语，封闭清单：repo、clone、commit、pin、lock 文件、shell（第 1 讲）；container、image、base image、pull、port、API、ID、token、Dockerfile（第 2–4 讲）；prompt、system prompt、LLM、agent、CLI（第 5 讲）；notebook、session、schema、SDK、harness（第 6 讲）；**trace、skill、fixture、label、diff、run ID（这一讲新增）**。
- 系列清单里保留英文、但这一讲没说到的：pipeline、endpoint、embedding、volume、venv、PATH、LoRA、CI、push（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| the model proposes; the harness decides | 模型提议；harness 决定 | two columns | 两栏 |
| harness / harness engineer | harness / harness 工程师 | the code around the model | 模型外面的代码 |
| action boundary / concerns | 行动边界 / 关注点 | control flow / verification / sub agents | 控制流 / 验证 / 子 agent |
| move right / give control to code | 往右移 / 把控制权交给代码 | stakes / can't be undone / audit | 风险 / 无法撤销 / 审计 |
| Think / Reason / Plan | 思考 / 推理 / 规划 | Execute / Verify / Response | 执行 / 验证 / 回复 |
| act / Act 1 / six acts | 幕 / 第 1 幕 / 六幕 | scenario / mode / case | 场景 / 模式 / 用例 |
| loop / round / messages | 循环 / 轮 / 消息 | seam | 接缝 |
| trace / Trace | trace / Trace | requested tools / tool call | Requested tools / Tool call |
| harness layer / ring / inner ring | harness 层 / 环 / 内环 | admission / tool audit | 准入 / 工具审计 |
| turnstile / admitted and counted | 闸机 / 放行并计数 | fallback / iterations | 兜底 / 迭代 |
| reports, never repairs | 只报告，从不修复 | a new configuration / copy | 新的配置 / 副本 |
| context / context engineering | 上下文 / 上下文工程 | the invisible layer / the stack | 看不见的那一层 / 上下文栈 |
| context packet / slots | 上下文包 / 空位 | saved preferences / taste | 保存的偏好 / 口味 |
| shop policies / shop rules | 店铺政策 / 店铺规则 | trust label / sources | 信任标注 / 来源 |
| sieves / allergens | 筛子 / 过敏原 | selection / validation | 筛选 / 校验 |
| user message / system rule | user 消息 / 系统规则 | system lane / user lane | system 通道 / user 通道 |
| data, not instructions | 是数据，不是指令 | evidence | 证据 |
| workflow / graph / node / edge | 工作流 / 图 / 节点 / 边 | rails / station | 轨道 / 站 |
| revise loop / revision / attempt | 修订循环 / 修订 / 尝试 | revalidate and place | 重新校验并下单 |
| autonomy spectrum / hybrid | 自主性光谱 / 混合型 | structured output | 结构化输出 |
| manager / manager review | 经理 / 经理审核 | the host | 宿主程序 |
| approval / approve (typed) | 批准 / approve | approval ticket | 审批单 |
| fingerprint / hash / SHA-256 | 指纹 / 哈希 / SHA-256 | checkout / receipt | 结账 / 回执 |
| items / subtotal / product attributes | 商品明细 / 小计 / 商品属性 | stock violation / reserve | 库存违规 / 预留 |
| planner / event / the brief | 规划器 / 活动 / 活动说明 | vendor / allowlist / quarantine | 供应商 / 白名单 / 隔离 |
| five kinds of state / drawer | 五种状态 / 抽屉 | memory / history / tasks | 记忆 / 历史 / 任务 |
| compaction / truncation | 压缩 / 截断 | context window | 上下文窗口 |
| capsule / pins / re-pinned | 胶囊 / 钉上 / 重新钉上 | compaction trigger | 压缩触发条件 |
| guards / backstop / detector | 防线 / 保险 / 检测器 | authoritative | 权威 |
| skill / SKILL.md | skill / SKILL.md | progressive disclosure | 渐进式披露 |
| metadata / reference / asset | 元数据 / 参考资料 / 资源文件 | a hint, not a trigger | 是提示，不是触发条件 |
| hands / socket / manual | 手 / 插座 / 说明书 | manuals, not keys | 是说明书，不是钥匙 |
| agent system / manager pattern | agent 系统 / 管理者模式 | peers / handoffs | 对等的 agent / 交接 |
| outer / proposer / shared clock | 外层 / 提议者 / 共享的时钟 | narrow tools / inside out | 窄工具 / 里外反过来 |
| evaluation / run / run ID | 评测 / 运行 / run ID | events / template | 事件 / 模板 |
| outcome / trajectory / cost | 结果 / 轨迹 / 成本 | judges / LLM as judge | 评委 / 让 LLM 当评委 |
| test case / suite / baseline | 测试用例 / 测试集 / 基线 | eval set / artifact | 评测集 / 产物 |
| label / batch / Batch A | label / 批次 / 批次 A | report / scorecard | 报告 / 记分卡 |
| changed configuration / confounding changes | 改动的配置 / 混杂改动 | improved / regressed / unchanged | 改进 / 退步 / 不变 |
| live / offline / scripted / fixture | 在线 / 离线 / 脚本模拟 / fixture | ran for real | 真实运行 |
| key / placeholder key | 密钥 / 占位密钥 | the staff / the lecture / slides | 课程团队 / 课上 / 课件 |
| a small slip / a harmless slip | 一个小疏漏 / 一个无害的小疏漏 | at the time of recording | 录制时 |
| Something to ponder | 来想一个问题 | tear down | 拆掉 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的一个中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 主线：模型提议，harness 决定 / The rule: the model proposes, the harness decides

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| harness / the harness / harness engineer / harness engineering / the code around the model | harness / harness 工程师 / harness 工程 / 模型外面的代码 | S01[4]：所谓 harness，就是模型外面的代码：循环、它的限制、它的上下文和它的检查。 | A3：字幕和书面都保留英文（第 6 讲 A3 已定：没有通行译名，又是这一讲的主题）。小写，不放句首（A5）：所谓 harness……、这个 harness……。S05[0] 要让“循环”留在第一个分句（D9）：如果你写过一个循环，它调用模型并执行工具调用，那你就是 harness 工程师。 |
| the model proposes; the harness decides / propose / proposal / an unvalidated proposal / decide | 模型提议；harness 决定 / 提议 / 未经验证的提议 / 决定 | S01[4]：课程的 notebook 用一句话说清了：模型提议；harness 决定。 | 全片的主线，处处同一个说法（S01、S16）：模型提议；harness 决定。propose → 提议（模型提议数量），decide → 决定；where it matters, so do you → 在关键的地方，你也一样。 |
| two columns / sort every line of output / the model's part / the harness's part | 两栏 / 模型负责的部分 / harness 负责的部分 | S01[4]：今天我们把输出的每一行，都归到这两栏里。 | V1 的两栏（蓝色在左，绿色在右）：两栏、左边 / 右边。 |
| action boundary / five concerns / control flow / context and memory / verification / sub agents / who decides | 行动边界 / 关注点 / 控制流 / 上下文与记忆 / 验证 / 子 agent | S05[6]：现在这两栏变成了课上的行动边界：五个关注点，左边是模型负责的部分，右边是 harness 的。 | 课件 22 的表（画面上的行名保持英文，A11）：action → 行动（authorize an action → 授权行动），Control flow → 控制流，Tools → 工具，Context & memory → 上下文与记忆，Verification → 验证，Sub agents → 子 agent。filled in → 填好的。 |
| move right / move left / stakes are high / can't be undone / predictable / need an audit / give control to code | 往右移 / 往左移 / 风险高 / 无法撤销 / 可预测 / 审计 / 把控制权交给代码 | S08[0]：回想一下往右移的那个箭头：风险高、操作无法撤销、任务可预测，或者需要审计的时候，就把控制权交给代码。 | 课件 22–23。an action can't be undone → 操作无法撤销（这里用“操作”，指不可逆的那一下；其他地方用“行动”，A7）。Move right when …：保持主句在前，或写成一个分句：风险高或操作无法撤销时就往右移（D9）。 |
| the six steps / Think / Reason / Plan / Execute / Verify / Response / the verify step / the response step / hidden reasoning | 思考 / 推理 / 规划 / 执行 / 验证 / 回复 / 验证步骤 / 回复步骤 / 隐藏的推理 | S05[5]：CartCheck 就是课上的验证步骤。 | 课件 21 的六步条（画面保持英文）：Think 思考、Reason 推理、Plan 规划、Execute 执行、Verify 验证、Response 回复。not hidden reasoning → 不是隐藏的推理。 |
| agent / an agent / the outer agent / the agent outside / LLM | agent / 外层 agent / LLM | S04[0]：第 1 幕从课上的回顾开始：agent 就是一个带着指令和工具的模型，一直运行到任务完成。 | 系列清单（第 5、6 讲）：agent 照说，量词“个”，不放句首（A5）；书面写“智能体（agent）”。the model → 模型。 |
| the lecture's recap / instructions / tools / memory / the lecture's question / what goes into the model | 课上的回顾 / 指令 / 工具 / 记忆 / 课上的问题 | S04[8]：这就是课上的问题：怎么管理进入模型的东西？ | 沿用第 6 讲：instructions → 指令，tools → 工具，memory → 记忆（绝不写“内存”）。 |

### 准备：container、密钥与 Docker / Setup: the container, the key and Docker

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| laptop / your laptop / the clone / secrets folder / one level up / service account | 笔记本 / secrets 目录 / 上一级 / 服务账号 | S02[2]：第 1 步在上一级创建 secrets 目录。 | 第 1 讲：laptop → 笔记本（A7：不是 notebook）。第 3–6 讲：service account → 服务账号。目录名照写，加“目录”。 |
| container / image / base image / mount / environment variable / publish a port / HTTPS | container / image / base image / 挂载 / 环境变量 / port / 发布 / HTTPS | S02[0]：一个 container 挂载这两个目录，密钥以环境变量的形式传进去，不发布任何 port，应用唯一的对外调用是走 HTTPS 去 OpenAI。 | A2（第 2–6 讲）：container、image、base image、port 照说；mount → 挂载，publish → 发布，environment variable → 环境变量。 |
| key / your key / an OpenAI key / a real key / the placeholder / the placeholder key / exports your key | 密钥 / OpenAI 密钥 / 真实的密钥 / 占位符 / 占位密钥 / 导出 | S02[3]：把占位符换成你自己的密钥，或者离线时跳过这一行。 | 第 6 讲：key → 密钥（不写 key，也不写“钥匙”，A7），the placeholder → 占位符，the placeholder key → 占位密钥；变量 OPENAI_API_KEY 按旁白写成 OpenAI API key（A6）。任何一行都不出现密钥的值。 |
| bash docker-shell.sh / builds the image / starts the container / your first build / pulls it / a minute or more | bash docker-shell.sh / 构建 image / 启动 container / 第一次构建 / pull / 一分钟或更久 | S02[4]：第 3 步：bash docker-shell.sh，构建 image 并启动 container。 | 命令放在冒号之后、分句末尾（G3）。pull 照说（A2）：你第一次构建还要先 pull 它。 |
| Dockerfile / lockfile / the layer trick / layer / copies the code | Dockerfile / lock 文件 / 分层技巧 / 层 | S02[5]：Dockerfile 先根据 lock 文件安装，再复制代码：这是第 2 讲讲过的分层技巧。 | 第 1 讲：lockfile → lock 文件；第 2–4 讲：layer → 层（image 的层）；the layer trick → 分层技巧。harness 的层也叫“层”（A7）。 |
| banner / activated / a harmless slip / the at sign / container ID / this prompt / the container prompt | 横幅 / 已激活 / 一个无害的小疏漏 / @ 符号 / container ID / 提示符 | S02[6]：横幅说环境已经激活了，可这时脚本还没激活它：一个无害的小疏漏。 | 和第 5、6 讲一致：横幅、@ 符号后面是 container ID；shell 的 prompt → 提示符（LLM 的 prompt 照说，A7）。 |
| second terminal / docker ps / docker images / docker inspect / configuration / sensitive / integration | 第二个终端 / docker ps / docker images / docker inspect / 配置 / 敏感信息 / 集成 | S02[9]：用 docker inspect，能在 container 的配置里看到你的密钥；真实的密钥要当作敏感信息对待。 | 命令照写小写，不放句首（A5）：Docker ps: no ports. → 先看 docker ps：没有 port。；Docker images: … → 再看 docker images：……。 |
| docker exec / shell in / the README's three lines / hidden / out of your history / keep working in that shell | docker exec / 进到 container 的 shell 里 / 隐藏输入 / 历史记录 | S02[11]：如果是这种情况，就从第二个终端进到 container 的 shell 里，再输入 README 的那三行：密钥隐藏着输入，也不会留在你的历史记录里。 | shell 照说（第 1 讲）。shell in → 进到 container 的 shell 里；your history → 你的历史记录（shell history → shell 历史记录，第 2–4 讲）。 |
| from here on / inside the container | 从这里开始 / 在 container 里运行 | S02[7]：从这里开始，每条命令都在 container 里运行。 |  |

### 离线验证与 Colab / Verify offline, and Colab

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| verify / offline / check the SDK / installed versions / feature | 验证 / 离线 / SDK / 安装的版本 / 功能 | S03[0]：现在在 container 里离线验证。 | verify（验证环境）→ 验证，和课上的 Verify 同一个词（A7：validate → 校验，check → 检查）。true 照写（代码里的值）。 |
| tests / 281 tests / ending in OK / scripted model responses / the machinery / not the model | 测试 / 281 个测试 / OK / 脚本模拟的模型回复 / 这套机制 | S03[1]：它们用的是脚本模拟的模型回复，所以测的是这套机制，不是模型。 | scripted → 脚本模拟的（A3；画面上的 scripted 标签保持英文，A11）。test the machinery, not the model → 测的是这套机制，不是模型（S03、S14 同一个说法）。 |
| logs / deliberate failures / an injected audit outage / approval-identity warning / trust the last line | 日志 / 故意制造的失败 / 注入的审计故障 / 审批身份警告 / 以最后一行为准 | S03[2]：第 3 步显示日志：故意制造的失败，比如注入的审计故障，还有一个第 4 幕会再遇到的审批身份警告。 | the approval-identity warning → 审批身份警告（S03、S10）；Trust the last line. → 以最后一行为准。 |
| model check / the default / a model flag / an environment variable / your account | 模型检查 / 默认值 / --model 参数 / 环境变量 / 账号 | S03[3]：命令行里的 --model 参数优先于环境变量，环境变量又优先于这个默认值；如果你的账号用不了它，就设置其中一个。 | A model flag 就是画面上的 --model：--model 参数（不放句首，A5）。beats → 优先于。 |
| notebook tests / chat view tests / the README's notebook section | notebook 测试 / chat view 测试 / notebook 那一节 | S03[4]：它们也在 container 里运行：9 个 notebook 测试和 12 个 chat view 测试，都是 OK。 | notebook 照说（第 6 讲：“笔记本”是 laptop）。chat view 按旁白写（画面上是 test_chat_view.py）。 |
| Colab / the course Colab / a second road / Save a copy in Drive / a secret / notebook access / the setup cells | Colab / 课程的 Colab / 第二条路 / Drive / secret / Notebook access / 准备单元格 | S03[5]：把副本保存到你的 Drive，把密钥存成一个名叫 OpenAI API key 的 secret，打开 Notebook access，再运行准备单元格。 | 第 6 讲：Colab 界面上的字照写（Save a copy in Drive、Notebook access、Secrets）；a secret → secret；cell → 单元格；the setup cells → 准备单元格；the setup（S03[6]）→ 准备步骤。 |
| pinned packages / not the lockfile / dependencies / drift / identical versions | pin 了版本的包 / 依赖 / 漂移 / 完全一致的版本 | S03[6]：Colab 的准备步骤装的是那七个 pin 了版本的包，而不是 lock 文件，所以它们的依赖可能会漂移；要版本完全一致，就用 Docker。 | 第 1、6 讲：package → 包，pinned → pin 了版本的，dependency → 依赖。package 是“包”，context packet 是“上下文包”（A7）。 |
| recorded / every recorded answer / the staff's saved Colab run / the README's own words | 录下来的回答 / 课程团队 / 保存的运行 | S03[7]：这期视频里每个录下来的回答，都来自这个 notebook 保存的那次运行。 | 第 3–6 讲：the staff → 课程团队。视频里的 recorded → 录制 / 录下来的；写进运行数据库的 recorded → 记录（A7）。 |
| live / live commands / live runs / live answers / the live model / offline / ran for real / free | 在线 / 在线命令 / 在线运行 / 在线模型 / 离线 / 真实运行 / 免费 | S01[7]：离线的部分都是真实运行的；在线命令一直跑到 OpenAI 拒绝占位密钥为止。 | A3：live（真的调用模型、按 token 计费）→ 在线，和画面上的 offline · free / live · billed per token 正好成对：离线 / 在线。不写“实时”（第 3 讲的 live view 才是实时视图），字幕里不写 live。ran for real → 真实运行（第 6 讲）。live memory（S16）→ 在线运行写下的记忆。 |

### 第 1 幕：agent 与循环 / Act 1: the agent and its loop

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| act / Act 1 / six acts / an act 3 command / the act 3 workflow / acts 1 and 2 | 幕 / 第 1 幕 / 六幕 / 第 3 幕的命令 / 第 3 幕的工作流 | S01[5]：教程在一家虚构的奶酪店里分六幕进行，那里什么都不会真的买、真的寄，也不会真的发邮件。 | A3：README 的 Act → 幕（分六幕的一出戏）；act n → 第 n 幕；--act n 和进度条在画面上保持原样。Step 1: act 4. → 第 1 步：第 4 幕。 |
| build agent / one framework agent / the shop instructions / five tools / a structured reply format | build agent / 框架里的 agent / 店里的指令 / 五个工具 / 结构化的回复格式 | S04[1]：在代码里，build agent 这个函数会创建一个框架里的 agent：店里的指令、五个工具，以及结构化的回复格式。 | A6：build_agent → build agent 这个函数。structured → 结构化（第 6 讲 structured output → 结构化输出）。 |
| tool / ask for a tool / the harness runs it / place an order / preview order / an unvalidated proposal / order placed set to false | 工具 / 请求工具 / 下单 / preview order / 未经验证的提议 / order placed 设为 false | S04[2]：而且这五个工具都不能下单：preview order 工具只记录一个未经验证的提议，order placed 设为 false。 | A6：preview_order → preview order 工具，"order_placed": False → order placed 设为 false。place an order → 下单。 |
| scenario / scenario standard / the ask / call 1 / error 401 / the failed run / still recorded | 场景 / standard 场景 / 需求 / 第 1 次调用 / 401 / 失败的运行 / 记录 | S04[3]：你会看到需求、第 1 次调用和五个工具；接着调用失败，报 401：占位密钥。 | 场景名照写（standard、personalized、missing-details……），加“场景”。the ask / the request → 需求（A7）。call 1 → 第 1 次调用（第 6 讲）。The failed run is still recorded → 失败的运行照样会记录下来。 |
| the catalog / get catalog / messages / round / the seam / requested tools / tool call | 商品清单 / get catalog / 消息 / 轮 / 接缝 / Requested tools / Tool call | S04[5]：模型的计划止于 Requested tools；harness 从 Tool call 开始执行。 | 第 6 讲：catalog → 清单（不写“目录”）；这里是“商品清单”。round（循环的一轮）→ 轮（Every round → 每一轮）。seam → 接缝（V2 的比喻）。Requested tools / Tool call 是 trace 里的字样：照画面写（en_display，D4）。 |
| trace / the trace / traces / Trace | trace / Trace | S04[5]：这个 trace 显示的是请求和结果，不是隐藏的推理。 | A3：trace 照说（实验课口语：看一下 trace；Trace 层；SQLite 里的 trace）。小写不放句首：这个 trace……、所有 trace……；类名 Trace 可以开头。trace 里的 requests（工具请求）→ 请求（A7）。 |
| stock / price / pairings / preview / the loop stops / call 6 / answers without asking for a tool | 库存 / 价格 / 搭配 / 预览 / 循环 / 第 6 次调用 | S04[6]：第 6 次调用时，模型直接回答，没有请求工具，循环就停了。 | Then stock, price, pairings and preview. → 然后是库存、价格、搭配和预览。loop → 循环（第 6 讲）。 |
| input tokens / billed input tokens / the input grows / for one answer | 输入 token / 计费 / 一个回答 | S04[6]：消息从 1 条涨到 11 条，输入从 1942 涨到 4540 个 token：一共大约 21000 个计费的输入 token，只为了一个回答。 | token 照说（第 4–6 讲），不加复数；数字不加千位分隔符（C1）。 |
| show JSON / the exact message / a short note / the confirmed request / null / not provided | --show-json / 确切的消息 / 简短的说明 / 已确认的需求 / null / 没有提供 | S04[7]：第 2 步加上 --show-json，看确切的消息：一段简短的说明，加上 JSON 形式的已确认需求，其中 null 表示没有提供。 | dash dash show JSON → --show-json（照画面；en_display，D4）。the confirmed request → 已确认的需求（A7）。null 照写。 |

### 第 1 幕：harness 层与行动边界 / Act 1: harness layers and the action boundary

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| a bare loop / no stop / notebook cell / Colab or Jupyter / wraps build agent in a harness | 裸循环 / 停不下来 / notebook 单元格 / Jupyter | S05[1]：第 3 步是一个 notebook 单元格，在 Colab 或 Jupyter 里用，它把 build agent 包进一个 harness。 | And a bare loop has no stop. → 而一个裸循环是停不下来的。 |
| Trace / Budget / Context / CartCheck / Cart Check / basic Context | Trace / Budget / Context / CartCheck / basic Context | S05[1]：它加上 Trace、Budget，限 8 次模型调用、20 次工具调用和 120 秒，basic Context，还有 CartCheck。 | A1（a）：四个层的类名照画面写（Trace、Budget、Context、CartCheck；Cart Check → CartCheck，en_display）。可以放句首。概念说中文：budget → 预算，context → 上下文。basic Context 按旁白写（A6）。 |
| harness layer / four layers / one feature each / the inner ring / call admission / the tool audit / the shop rules | harness 层 / 四层 / 每层一个功能 / 内环 / 调用准入 / 工具审计 / 店铺规则 | S05[2]：内环永远拆不掉：调用准入、工具审计和店铺规则。 | V3 的环：ring → 环，the inner ring → 内环；admission → 准入，audit → 审计；slide on → 套上，come off → 拆掉。 |
| turnstile / admitted and counted / the lock stays shut / Maximum of 8 model calls reached | 闸机 / 放行并计数 / 锁 / Maximum of 8 model calls reached | S05[3]：每次模型调用都要放行并计数；第九次会失败，报的是：Maximum of 8 model calls reached，而且锁会一直关着。 | turnstile → 闸机（一个词）。报错信息是终端原文，放在“报”后面照抄（同第 4、6 讲）。 |
| the framework's fallback / loop iterations / no call limits / overall time budget | 框架的兜底 / 循环迭代 / 调用次数上限 / 总的时间预算 | S05[4]：没有 Budget，就只剩框架的兜底：40 次循环迭代，没有调用次数上限，也没有总的时间预算。 | fallback → 兜底（A7：backstop → 保险，guards → 防线）；iterations → 迭代（第 6 讲）。 |
| reports, never repairs / the hook / the items / the prose / garbled / passed / failed / no cart | 只报告，从不修复 / 开头的例子 / 商品明细 / 文字 / 写乱 / no cart | S05[5]：回到开头的例子：它检查的是商品明细，不是文字，所以预算写乱了也照样通过。 | the hook → 开头的例子；the prose → 文字（第 6 讲：模型写的文字）；items → 商品明细。状态值 passed / failed / no_cart / not_run 照写（no cart 按 A6）。 |
| harness without trace / the add and without methods / a new configuration / that copy / the original harness | harness without trace / add 和 without 方法 / 新的配置 / 副本 / 原来的 harness | S05[9]：而且 add 和 without 方法从不修改 harness：每次都返回一个新的配置，所以原来那个 harness 的四层都还在。 | A6、B3：harness.without("trace") → harness without trace（不写括号和引号）；.add() / .without() → add 和 without 方法。Yes, and yes. → 是，也是。 |
| missing details / a question back / invented details | missing-details 场景 / 反问 / 编造的细节 | S05[10]：有密钥的话，要找的是反问，而不是编造的细节；CartCheck 应该报告 no cart。 | 场景名照画面写：missing-details 场景（en_display：the missing-details scenario）。 |

### 第 2 幕：上下文 / Act 2: context

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| context / context engineering / the invisible layer / the lecture's stack / slots | 上下文 / 上下文工程 / 看不见的那一层 / 上下文栈 / 空位 | S06[0]：第 2 幕改的是模型看到的东西：课上说的看不见的那一层。 | 第 5、6 讲：context → 上下文，context engineering → 上下文工程。the lecture's stack（课件 16）→ 课上的上下文栈。slots → 空位。 |
| system prompt / shop policies / the reply format / retrieved data / saved preferences / saved taste | system prompt / 店铺政策 / 回复格式 / 检索到的数据 / 保存的偏好 / 保存的口味 | S06[0]：这是按课上的上下文栈画出的一次模型调用：system prompt 和店铺政策、需求、回复格式、五个工具，还有两个空位，留给检索到的数据和保存的偏好。 | system prompt 照说（第 5 讲）。policy → 政策（A7：rules → 规则）。preferences → 偏好，taste → 口味。 |
| basic / enriched / mode / basic mode / both modes | basic / enriched / 模式 / 两种模式 | S06[1]：第 1 幕用的 basic 模式只发前四块，空位留空；而 enriched 把它们填满。 | --context 的值照写；不放句首（A5）：其中 basic……、而 enriched……。 |
| compare / personalized / the second customer / mild cheeses / nonalcoholic pairings / today's request | --compare / personalized / 第二位顾客 / 温和的奶酪 / 无酒精搭配 / 今天的需求 | S06[2]：第 1 步 --compare 用的是 personalized 场景，今天的需求没提第二位顾客保存的口味：温和的奶酪和无酒精搭配。 | dash dash compare → --compare（en_display）。两位顾客不提名字，也不写 ID（A10）。 |
| side-by-side table / verdict / a tie / a regression | 并排对比表 / 结论 / 打平 / 退步 | S06[3]：有密钥的话，它会打印一张并排对比表和一个结论，结论也可能是打平或者退步。 | regression（变差）→ 退步，和 S15 的 regressed 同一个词（这里不写“回归”：那是回归测试）。 |
| single runs / conversation message / context packet / the packets differ | 单次运行 / 对话消息 / 上下文包 | S06[4]：即使没有密钥，也能看到一个真实的差别：basic 发 1 条对话消息，enriched 发 2 条；多出来的那条就是上下文包。 | packet → 上下文包，总带着“上下文”（A7：package 是“包”）。 |
| the override run / funk / funk rating / must win over | 偏好覆盖那次运行 / 浓烈度 / 压过 | S06[5]：第 4 步是偏好覆盖那次运行，要求浓烈度 4 或以上，今天的需求必须压过保存的口味。 | funk / funk rating → 浓烈度（一个词，S01 和 S06 一致）；funky cheeses → 气味浓烈的奶酪。 |
| state check / Pennsylvania / New York / raw milk / raw-milk cart / a fictional rule | 按州的检查 / 宾夕法尼亚 / 纽约 / 生乳 / 虚构的规则 | S06[6]：这条额外的命令会打印：同一辆生乳奶酪的购物车，寄往宾夕法尼亚不通过，寄往纽约通过，依据的是一条虚构的规则。 | state（美国的州）→ 州（A7：应用的 state → 状态）。地名写中文（A10）；PA / NY 照画面。 |
| cases / repeats / 3 times / errors / the report still writes / the label is used up / a new one | 用例 / 重复 / 错误 / 报告 / label | S06[8]：没有密钥时，它在 3 个错误之后就停了，但报告照样会写出来，label 也用掉了：有密钥的话，换一个新的。 | case → 用例（test case → 测试用例；A7：scenario → 场景）。label 照说（A3、A7）。 |
| the docs folder / missing / the README checkpoints / the page linked here | docs 目录 / 检查点 | S06[9]：这里链接的页面，本该放在我们看到缺失的那个 docs 目录里，所以就用 README 的检查点。 | README 里的 Checkpoint 问题 → 检查点。 |
| preview context / inspect the context first / sources / trust label / shop data | --preview-context / Inspect the context first / 来源 / 信任标注 / 店铺数据 | S07[1]：而 enriched 有三个，每个都带一个信任标注：已确认的需求、店铺数据和保存的偏好。 | README 的字样 Inspect the context first 照写（A11）。trust label → 信任标注（A7：不写“标签”，那是 tag）。 |
| sieves / enough stock / nut allergens / the allergy check / the shipping rule / survive | 筛子 / 库存 / 坚果过敏原 / 过敏检查 / 运输规则 | S07[2]：十二种奶酪穿过三层筛子：库存够、不往宾夕法尼亚寄生乳、没有坚果过敏原。 | V4 的 sieves → 筛子。Seven survive. → 七种留了下来。（不写“……七种。”：D3 的“种”规则） |
| retrieved information / outside data / a Python filter / vector search | 检索信息 / 外部数据 / Python 过滤器 / 向量检索 | S07[3]：课上说的检索信息指任何外部数据；在这里它是一个 Python 过滤器，不是第 5 讲的向量检索。 | 第 5、6 讲：retrieval → 检索，filter → 过滤器。 |
| user message / retrieved context / data, not instructions / a system rule / two lanes / system lane / user lane / evidence | user 消息 / Retrieved context / 数据，不是指令 / 系统规则 / 两条通道 / system 通道 / user 通道 / 证据 | S07[4]：这就是课上的两条通道：指令走 system 通道，证据走 user 通道。 | 消息角色照写（第 6 讲：user、system）：user 消息、system 通道、user 通道；lane → 通道（第 5、6 讲）。画面上的标题：Retrieved context；data, not instructions → 是数据，不是指令（S07、S11 同一个说法）。 |
| selection / validation / candidates / block | 筛选 / 校验 / 候选 / 拦下 | S07[6]：筛选能缩小范围，但校验说了算：第 3 幕的工作流会拦下它。 | validate / validation → 校验（第 6 讲 validator → 校验器）；block → 拦下（A9：打印出来的状态词）。 |
| baseline / outranks / the cart's route / out of the model's hands | 基线 / 优先于 / 购物车的路线 | S07[8]：第二部分，harness 会把购物车的路线从模型手里拿走。 | baseline → 基线（S07、S15）。In part 2 → 第二部分（第 6 讲）。 |

### 第 3 幕：工作流、审批与结账 / Act 3: workflow, approval, checkout

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| workflow / the order route / a graph / edges / node / Python owns its edges | 工作流 / 下单路线 / 图 / 边 / 节点 | S08[1]：下单路线是一张图，它的边归 Python 管。 | 第 6 讲：workflow → 工作流。graph → 图，edge → 边，node → 节点。 |
| confirm / propose / validate / the revise loop / the report fails / pairings / manager review / revalidate and place / propose cart | 确认 / 提议 / 校验 / 修订循环 / 报告不通过 / 搭配 / 经理审核 / 重新校验并下单 / propose cart | S08[1]：确认、提议、校验，只有报告不通过才退回提议，最多两次；然后是搭配、需要时经理审核，最后重新校验并下单。 | revise / revision → 修订（revise loop → 修订循环；bounded revision → 有上限的修订）。模型的节点 propose_cart 按旁白写：propose cart 节点（A6）。 |
| rails / the rail / station / a script in the model's seat | 轨道 / 站 / 模型的位置 | S08[5]：第 1 次尝试里有生乳的 Comté，轨道把它退了回去；第 2 次换成 Taleggio：有效，50.10 美元。 | V5 的 rails → 轨道（A7：trajectory → 轨迹）；station → 站。章节名：rails, not suggestions → 是轨道，不是建议。 |
| autonomy spectrum / rule-based / structured output / hybrid / full agent autonomy / a fixed graph / one model step | 自主性光谱 / 基于规则 / 结构化输出 / 混合型 / 完全自主 / 固定的图 | S08[2]：README 把它归在 harness 下面；在课上的自主性光谱上，它靠近结构化输出：一张固定的图，只有一步交给模型。 | 课件 36。files this under → 把它归在……下面。structured output → 结构化输出（第 6 讲）。 |
| quantities / transitions / pricing / validation / placement / receipt / success is a receipt | 数量 / 流转 / 定价 / 校验 / 下单 / 回执 | S08[3]：有密钥的话，模型提议数量；其余的都由代码来做：流转、定价、校验、下单。 | 第 6 讲：receipt → 回执（Success is a receipt. → 成功就是一张回执。）。placement → 下单。 |
| the shipping lesson / a customer's own cart / before / after / records the cart / checks it and stops / may fix it | 运输这一课 / 顾客自己的购物车 / 改之前 / 改之后 | S08[4]：改之前，模型只记录购物车；harness 检查它，然后停下。 | README 的 Before / After（拦下 / 修订）→ 改之前 / 改之后。cart → 购物车，量词“辆”。 |
| fixture / fixtures / attempt / swaps in / sends it back / valid | fixture / 尝试 / 换成 / 退回 / 有效 | S08[5]：额外再跑一个：--fixture 离线走同一条路线，模型的位置上坐的是一个脚本。 | A3：fixture 照说（--fixture 参数，也是 pytest 的词），不加复数。Attempt 1 → 第 1 次尝试。 |
| trap / blocked scenario / unresolved / blocked | 坑 / blocked 场景 / UNRESOLVED / BLOCKED | S08[6]：有个坑：用 fixture 时，blocked 场景会把同一辆购物车一连提议三次，最后是 UNRESOLVED，不是 BLOCKED，所以在 Colab 里，这一课要把 fixture 关掉。 | A9：旁白对比两个打印出来的结局时，照打印的写（UNRESOLVED、BLOCKED）；叙述里的 block → 拦下。 |
| scripted / predictable / guests / threshold / a valid cart | 脚本模拟 / 可以预期 / 位客人 / 门槛 / 有效的购物车 | S09[0]：第 4 步是脚本模拟的，所以审批结果可以预期：纽约 60 位客人，一辆有效的购物车，220.80 美元，超过了 200 美元的门槛。 | 金额照画面（C2）：220 dollars 80 → 220.80 美元，200 dollar threshold → 200 美元的门槛。 |
| manager / manager approval / the host / approve / decline | 经理 / 经理审批 / 宿主程序 / 暂停 / approve / decline | S09[1]：工作流暂停了，你就是经理：回答的是宿主程序，绝不是 agent。 | A7：店里的 manager（一个人）→ 经理；课上的 manager pattern → 管理者模式。the host（运行 harness 的应用）→ 宿主程序（第 6 讲 MCP 里的 host 照说；这一讲不用 MCP）。Type approve. → 输入 approve。 |
| fingerprint / SHA-256 / hash / the items / the subtotal / the policy / the product attributes / taken over | 指纹 / SHA-256 / 哈希 / 商品明细 / 小计 / 政策 / 商品属性 | S09[2]：一个指纹：SHA-256 哈希，覆盖需求、商品明细、小计、政策和商品属性。 | 第 2 讲 fingerprint → 指纹，第 5 讲 hash → 哈希。taken over → 覆盖（让“哈希”留在第一个字幕块，review_spoken 第 9 条）。 |
| stock / recheck / reserve / stock violation | 库存 / 重新检查 / 预留 / 库存违规 | S09[2]：库存是故意排除在外的：它会被重新检查，而不是被批准。 | recheck → 重新检查；revalidate → 重新校验（A7）。 |
| checkout / at checkout / validated and hashed again / the decision / the ticket / matches | 结账 / 再校验一次 / 再算一次哈希 / 决定 / 审批单 / 对得上 | S09[3]：结账时，购物车会再校验一次，再算一次哈希。 | approval ticket → 审批单（A7：receipt → 回执）。 |
| approval / approve / an approval binds this exact cart / authorizes a decision / approval is not placement | 批准 / 绑定 / 授权 / 批准不等于下单 | S09[7]：库存不在指纹里：批准授权的是一个决定；它不预留任何东西。 | 第 6 讲：approval → 批准，approved / pending → 已批准 / 待批准；作为流程叫“审批”（经理审批、审批抽屉）。输入的值 approve / decline 照写。 |
| thinking time / budget | 思考时间 / 预算 | S09[4]：你思考的时间不算进预算。 |  |
| out of stock / a bounded revision | 有上限的修订 / 零次模型调用 / 下单 | S09[8]：一次有上限的修订换成了 Époisses，订单以 50.10 美元下单，模型调用为零。 | grams → 克（C2）。 |
| trace and budget layers / can come off / graph and checkout rules / they stay | trace 层 / budget 层 / 拆掉 / 图和结账的规则 / 保留 | S09[9]：它的 trace 层和 budget 层可以拆掉；校验、审批和重新校验是图和结账的规则，所以保留。 | review_spoken 第 4 条：……是图和结账的规则，所以保留（和英文一样，原因在前，结果在后）。 |

### 第 4 幕：规划器、压缩与记忆 / Act 4: planner, compaction, memory

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| planner / a longer task / event / a 40-guest event | 规划器 / 更长的任务 / 活动 | S10[0]：第 4 幕是一个规划器，处理更长的任务：纽约一场 40 位客人的活动。 | 第 6 讲：planner → 规划器。 |
| long-term / short-term / saved memory / history / tasks / approvals / the audit / five kinds of state | 长期 / 短期 / 保存的记忆 / 历史 / 任务 / 审批 / 审计 / 五种状态 | S10[0]：课上把记忆分成长期和短期；这里对应的是保存的记忆和历史，再加上任务、审批和审计：五种状态。 | state（应用状态）→ 状态（A7：美国的州 → 州）。history → 历史。 |
| drawer / the approval drawer / authorize an action / only one | 抽屉 / 审批抽屉 / 授权行动 | S10[1]：只有一个：审批抽屉。 | V6 的柜子：drawer → 抽屉。The README asks which of these can authorize an action → README 问的是，这些里面哪一个能授权行动。 |
| the first customer / saved memory / before any model call / no tool writes memory | 第一位顾客 / 写记忆 | S10[2]：在任何模型调用之前，harness 就打印出第一位顾客保存的记忆。 | No tool writes memory. → 没有哪个工具能写记忆。 |
| assess the event / the vendor document / draft and save a vendor email / the to-do tools | 评估活动 / 供应商文档 / 起草和保存给供应商的邮件 / 待办工具 | S10[2]：然后是规划器的工具：评估活动、读取供应商文档、起草和保存给供应商的邮件，以及待办工具。 | 这里是普通动词（不是函数名；S13 的 start order、get order status、assess event 才是函数名）。vendor → 供应商。 |
| the brief / short / a finished task / shop stock / vendor availability | 活动说明 / 差 / 完成的任务 / 店里的库存 / 供应商有货 | S10[3]：完成的任务不等于批准，店里的库存也不等于供应商有货。 | the brief → 活动说明（A7：第 6 讲的 newsletter 是“简报”）。300 short → 差 300 克。 |
| approval mode always require / the framework pauses / the save runs / one tool | approval mode 设为 always require / 框架暂停 / 保存 | S10[4]：保存邮件这个工具，approval mode 设为 always require，所以框架会在保存执行之前暂停。 | A6、B3：approval_mode="always_require" → approval mode 设为 always require（同第 6 讲的 mode 设为 any）。 |
| the review / vendor address / a body written by code / status saved / email transmitted no / the file path | 审核 / 供应商地址 / 正文 / status / saved / email transmitted / 文件路径 | S10[5]：然后：status 为 saved，email transmitted 为 no，文件路径。 | 打印出来的字段和值照写（A9）：status 为 saved，email transmitted 为 no。review → 审核。 |
| authoritative / the authoritative block / harmless / predicts it | 权威 / 权威结果那一块 / 无害 | S10[6]：以权威结果那一块为准。 | authoritative → 权威（Authoritative status → 权威状态）。 |
| compaction / compactions / a malicious vendor document / a test decline / synthetic notes / characters | 压缩 / 恶意的供应商文档 / 测试用的拒绝 / 合成笔记 / 字符 | S11[0]：第 2 步离线运行：一个脚本模拟的规划器，带压缩，一份恶意的供应商文档，还有一次测试用的拒绝。 | compaction → 压缩（7 compactions → 7 次压缩）。notes → 笔记（A7：“笔记本”是 laptop）。 |
| context window / the window / kept for the reply / truncation / the oldest messages / back under half | 上下文窗口 / 窗口 / 回复 / 截断 / 最旧的消息 / 一半以下 | S11[1]：超过剩下部分的 80% 时，截断会丢掉最旧的消息，直到历史回到一半以下：26 条变成 5 条。 | percent → %（B3 允许；C2）。 |
| capsule / application state / pins a fresh one / re-pinned / the menu / pending reviews / open work | 胶囊 / 应用状态 / 钉上 / 重新钉上 / 菜单 / 待处理的审核 / 未完成的工作 | S11[3]：每次调用之前，harness 先取出旧胶囊、做压缩，再根据应用状态钉上一个新的。 | capsule → 胶囊。pin（胶囊）→ 钉上（A7：给版本 pin 照说 pin）。 |
| compaction trigger / what persists where / persists | 压缩触发条件 / 持久保存 | S11[4]：这就是课上的压缩触发条件，以及什么东西持久保存在哪里，都写成了代码。 | trigger → 触发条件（S11 和 S12：a hint, not a trigger → 是提示，不是触发条件）。 |
| quarantine / the detector / the real guards / recipient allowlist / allowlist / your review | 隔离 / 检测器 / 防线 / 收件人白名单 / 白名单 / 你的审核 | S11[5]：检测器故意做得很小；真正的防线是收件人白名单，还有你的审核。 | allowlist → 白名单；quarantine → 隔离（lands in quarantine → 被隔离了）；guards → 防线（A7）。 |
| the drafted email / declined / no HTML saved | 起草的邮件 / DECLINED / HTML | S11[6]：结果：DECLINED，没有保存 HTML，7 次模型调用，7 次压缩。 | The result 说的是打印出来的结局：DECLINED（A9）。 |
| memory exercise / masked / stores a preference / the next visit / reads the file | 记忆练习 / 遮住 / 偏好 / 下一次来访 | S11[7]：第 3、4 步是可选的记忆练习；照 README 第 484 行输入，因为这里的 ID 被遮住了。 | ID 本身绝不写出来（A10）：the ID is masked → 这里的 ID 被遮住了。 |
| host-written memory / the host | 值得记住 / 宿主程序 / 记忆 | S11[8]：这个 harness 连这一点也移到了右边：只有宿主程序能写记忆。 | the host → 宿主程序（A7）。 |
| build act 4 / five layers / without compaction | build act 4 / 五层 / 去掉压缩 | S11[9]：第 5 步是 notebook 单元格，给 Colab 用：build act 4 加了五层。 | A6：build_act4 → build act 4。Without compaction（去掉这一层）→ 去掉压缩之后。 |

### 第 5 幕：skill / Act 5: skills

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| skill / skills / the vendor skill / folders of procedure / relevant | skill / 供应商那个 skill / 装着操作流程的目录 | S12[0]：第 5 幕加入了 skill：装着操作流程的目录，agent 只在相关时才加载。 | A3：skill 照说（实验课口语：写一个 skill、加载 skill；画面上有 SKILL.md），不加复数，不放句首。书面写“技能（skill）”。章节名：skills are manuals, not keys → 技能（skill）是说明书，不是钥匙。 |
| expertise gap / context budget | 专业知识缺口 / 上下文预算 | S12[0]：它们解决两个问题：专业知识的缺口，和上下文预算。 | 课件 26（review_spoken 第 8 条：不要译成“节省专业知识”）。 |
| token cost / name and description / main file / SKILL.md / a reference / an asset / progressive disclosure / Discover / Activate / Use resources | token 成本 / 名字和描述 / 主文件 / SKILL.md / 参考资料 / 资源文件 / 渐进式披露 / 发现 / 激活 / 使用资源 | S12[1]：加载 skill 分三步，token 成本一步比一步高：每个 skill 的名字和描述，各大约 100 个 token；然后是它的主文件 SKILL.md；再然后是一份参考资料或资源文件，只在需要时读取。 | 课件 28：progressive disclosure → 渐进式披露；Discover / Activate / Use resources → 发现 / 激活 / 使用资源。references/ → 参考资料，assets/ → 资源文件。 |
| scripts folder / removes that tool / advises / never executes | scripts 目录 / 提建议 / 执行 | S12[2]：这个 harness 故意去掉了那个工具：skill 只提建议，从不执行。 |  |
| metadata / tasting planning / vendor outreach / get stock / load skill / read skill resource | 元数据 / tasting-planning / vendor-outreach / get stock / load skill / read skill resource | S12[3]：一开始只加载元数据：tasting-planning 和 vendor-outreach。 | 第 5 讲：metadata → 元数据。skill 名照画面写（tasting-planning、vendor-outreach；en_display）。A6：get_stock、load_skill、read_skill_resource → get stock、load skill、read skill resource。 |
| stock question / hint / trigger / description | 提示 / 触发条件 / 描述 | S12[4]：有密钥的话，模型根据描述来决定：是提示，不是触发条件。 | hint → 提示（A7：LLM 的 prompt 照说；shell 的 prompt 是“提示符”）。 |
| sourcing path / real path / drafting / email template / backstop | 完整的采购流程 / 六次加载 / 真实路径 / 起草 / 邮件模板 / 代码里的一道保险 | S12[5]：起草一直会被拒绝，直到读过邮件模板为止：这是代码里的一道保险。 | backstop → 保险（A7）。主句在前，同英文（D9）。 |
| recipients / authorize actions / parent folders / absolute paths / symlinks / edited mid-run | 收件人 / 授权行动 / 上级目录 / 绝对路径 / 符号链接 / 运行中途被改过 / 拒绝 | S12[7]：这个 skill 自己就写明了，它不能添加收件人或授权行动；而且每次读取都要经过检查：不许上级目录、绝对路径或符号链接，运行中途改过的文件会被拒绝。 | No. → 不会。（思考题的答案） |
| transmitted / saved file | 发出去 / 保存的文件 | S12[8]：收件人由代码对照白名单检查，而且什么都不会真的发出去；额外检查显示，保存的文件里也是这么写的。 | transmit → 发出去（打印出来的字段 email transmitted 照写：A9）。 |
| the hands / the socket / the manual / MCP / manuals, not keys | 手 / 插座 / 说明书 / MCP / 钥匙 | S12[9]：用课上的话说，工具是手，MCP 是插座，这里没用到，skill 是说明书。 | 课件 29。socket → 插座（第 6 讲 plug → 插头）。keys（打开权限的钥匙）→ 钥匙（A7：API key 是“密钥”）。 |

### 第 6 幕：agent 系统 / Act 6: agent systems

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| agent system / single agent / a graph of agents / two patterns / manager pattern / agents as tools / peers / handoffs | agent 系统 / 单个 agent / 由 agent 组成的图 / 管理者模式 / 把 agent 当工具 / 对等的 agent / 交接 | S13[0]：课上把单个 agent 和由 agent 组成的图做对比，分两种模式：一个管理者把 agent 当工具来调用，或者对等的 agent 互相交接。 | 课件 31–33。manager pattern → 管理者模式（A7：店里的经理是“经理”）；handoffs → 交接（第 6 讲）；peers → 对等的 agent。 |
| a whole workflow / a model inside one node / no handoffs | 一整个工作流 / 一个节点 / 没有交接 | S13[1]：它就是管理者模式，只不过它调用的工具是一整个工作流，就是第 3 幕那个，里面只有一个节点用到模型。 | No handoffs. → 没有交接。 |
| outer model calls / proposer calls per workflow / one shared clock / the budget | 外层模型调用 / 提议者调用 / 共享的时钟 / 预算 | S13[2]：预算是：16 次外层模型调用，20 次工具调用，每个工作流 8 次提议者调用，再加一个共享的 180 秒时钟。 | outer → 外层（第 6 讲 outer layer → 外层）；proposer → 提议者。 |
| the host confirms the requests / picks an ID / narrow tools / start order / get order status / assess event | 需求 / ID / 窄工具 / start order / get order status / assess event | S13[3]：工具都很窄：start order、get order status、assess event。 | A6：start_order、get_order_status、assess_event → start order、get order status、assess event（en_display）。The host confirms the requests → 宿主程序确认这些需求。narrow tools（S16 的清单）→ 窄工具。 |
| two orders sharing one shop / the test decision | 两个订单 / 测试用的决定 | S13[5]：第 3 步离线运行：两个订单共用一家店。 | the test decision（--manager-decision approve）→ 测试用的决定。 |
| Request 1 / Request 2 / is placed / leaving / revalidation / blocked | 订单 1 / 订单 2 / 下单 / 重新校验 / 被拦下 | S13[6]：订单 2 走到重新校验时需要 1600 克：被拦下了。 | Request 1 / Request 2（画面上是 request-1 / request-2）→ 订单 1 / 订单 2。Request 1 is placed, leaving 1,400. → 订单 1 下单了，剩下 1400 克。 |
| the final answer / the app / fills in / the status / invalid or unauthorized / the stock lines / the reason | 最终回答 / 应用 / 填上 / 状态 / Invalid or unauthorized / 库存那几行 / 原因 | S13[7]：被拦下的订单显示 Invalid or unauthorized；下面库存那几行给出了原因。 | 终端原文照抄（A1 a）。the status, placed → 状态 placed（打印出来的值，A9）。app → 应用。 |
| inside out / the agent outside / the fixed graph as its tool | 里外反过来 / 固定的图 | S13[8]：在自主性光谱上，它是混合型，只不过里外反过来：外面是 agent，固定的图是它的工具。 | inside out → 里外反过来（review_spoken 第 17 条）。 |

### 评测 / Evaluation

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the provider's model / the product / must be tested | 服务商的模型 / 产品 / 测试 | S14[0]：服务商的模型和产品之间的一切都是我们的：上下文、harness、工具和 skill。 | 课件 39。So all of it must be tested. → 所以这些全都要测试。 |
| outcome / trajectory / cost / outcome and process checks | 结果 / 轨迹 / 成本 / outcome 检查 / process 检查 | S14[1]：在这里，它们就是 outcome 检查和 process 检查，再加上调用次数和 token。 | 课件 40：outcome → 结果，trajectory → 轨迹（A7：rails → 轨道），cost → 成本；检查名的前缀 outcome、process 照写（画面上是 outcome.proposal、process.manager_authority）。 |
| evaluation / evaluation step 1 / lists the runs / run / a SQLite database / status error | 评测 / 评测第 1 步 / 运行 / SQLite 数据库 / status 为 error | S14[2]：到目前为止的每次运行都在同一个 SQLite 数据库里，包括失败的在线运行，status 为 error。 | evaluation → 评测；evaluation step k（README › 6 · Evaluation › Step k）→ 评测第 k 步。a run → 一次运行。 |
| inspect run / run ID / template | --inspect-run / run ID / 模板 / 照字面输入 / 贴 | S14[3]：这个 --inspect-run 要一个 run ID：照字面输入就会失败，因为它是个模板。 | Inspect run → --inspect-run（en_display），不放句首（A5）。RUN_ID → run ID（A6）。 |
| events / approval requested / approval decided / policy decision / order placed / run finished / model failed | 事件 / approval.requested / approval.decided / policy.decision / order.placed / run.finished / model.failed | S14[4]：事件依次是：approval.requested，带着指纹；approval.decided，由人做出；policy.decision allow、order.placed、run.finished。 | 事件名照画面写，带点（A1 a；en_display 也这样写）；保持英文的顺序（D9）。 |
| evidence / a failure is evidence too / not the prose | 证据 / 失败也是证据 | S14[5]：失败也是证据。 | The evidence for order placed is an event, not the prose. → 下单的证据是一个事件，不是文字。（不以事件名开头） |
| the act 2 evaluation / repeats / labeled / pass / scripted runs | 第 2 幕的评测 / 重复 / label / 通过 / 脚本模拟的运行 | S14[6]：评测第 2 步先离线跑：第 2 幕的评测，脚本模拟，重复两次，label 是 context-fixture-1。 | context fixture 1 → context-fixture-1（en_display）。 |
| report / read the report back / HTML scorecard / default path / the outputs folder | 报告 / HTML 记分卡 / 默认路径 / outputs 目录 | S14[7]：然后把报告读回来，再导出 HTML 记分卡，放到默认路径，或者你自己选的路径。 | scorecard → 记分卡。 |
| label / labels / immutable / batch | label / 不可更改 / 新的 label / 批次 / 这一批 | S14[9]：每个 label 都不可更改：重复用一个，这一批就会停下来。 | A3、A7：label 照说（--label 的值），不加复数，不放句首；batch → 一批 / 批次（Batch A → 批次 A）。 |
| compare / configuration / prompt edit / per case | 比较 / 配置 / 改一次 prompt / 用例 / 逐个用例 | S15[0]：课上提醒，改一次 prompt 可能修好一个用例，又弄坏三个，所以要逐个用例比较。 | compare（动词，也指这一步）→ 比较；参数 --compare 照写。 |
| improvement loop / see a failure / capture a test case / change one layer / run the suite k times / compare with the baseline / merge / iterate | 改进循环 / 测试用例 / 只改一层 / 测试集 / 基线 / 合并 / 迭代 | S15[1]：课上的改进循环：发现失败，记录成测试用例，只改一层，把测试集跑 k 次，和基线比较，然后合并或者继续迭代。 | 课件 42。k 保持字母。 |
| Batch A / Batch B / missing | 批次 A / 批次 B / 缺失 | S15[2]：批次 A 用 enriched 模式跑两个用例，各两次：4 次在线运行。 | Without a key: 0 of 4, with 3 errors and 1 missing. → 没有密钥：4 次里 0 次通过，3 个错误，1 个缺失。 |
| the prompt file / a deliberate change / confirmed constraint rules / appends a line / an action status / diff | prompt 文件 / 有意的改动 / 已确认约束的规则 / 追加一行 / 行动状态 / diff | S15[3]：复制 prompt 文件，在你的笔记本上改这份副本：只做一处有意的改动，保留已确认约束的那些规则。 | 第 1 讲：constraint → 约束。diff 照写（命令，不放句首）。dash dash prompt file → --prompt-file。 |
| changed configuration / confounding changes / the change-one-layer rule / checked in code | 改动的配置 / 混杂改动 / 只改一层 / 由代码检查 | S15[6]：改了代码、数据或模型，它都会指出来：这就是课上“只改一层”的规则，由代码来检查。 | confounding changes → 混杂改动（confounder → 混杂因素）。Changed configuration: prompt. → 改动的配置：prompt。 |
| flags a run / pass or fail flips / errored / unchanged / improved / regressed / fixtures ignore the prompt | 标出 / 翻转 / 报错 / 不变 / 改进 / 退步 | S15[7]：比较只在通过或失败翻转时才标出一次运行；这里每次运行前后两次都报错。 | improved / regressed / unchanged → 改进 / 退步 / 不变（S06 的 regression → 退步）。 |
| what the checks establish / properties / cart validity / approval order / your review / five questions | 证明 / 属性 / 购物车是否有效 / 审批顺序 / 审核 / 五个问题 | S15[9]：它们检查的是属性，比如购物车是否有效、审批的顺序；文字要靠你来审，用 README 里的五个问题。 | establish → 证明（a passing fixture batch establishes → 一批通过的 fixture 运行能证明什么）。 |
| three judges / a model / a human / LLM as judge / lean toward code | 评委 / 人 / 偏向代码 | S15[10]：这个教程用了其中两个：代码，和你。 | 课件 41：judges → 评委，LLM as judge → 让 LLM 当评委。This tutorial uses two → 用了其中两个（不写“……两种。”，D3）。 |
| one difference / one limit / keep your cases / the eval set / the most valuable artifact | 差异 / 局限 / 评测集 / 产物 | S15[11]：还有，留好你的用例：评测集是最有价值的产物。 | eval set → 评测集。 |

### 拆除、回顾与下节 / Tear down, recap, what's next

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the repository map / section 7 / every option / python cli.py --help | repo 地图 / 第 7 节 / 所有选项 / python cli.py --help | S16[0]：第 7 节的 repo 地图最后一条是：python cli.py --help，所有选项都在一个地方。 | repository → repo（字幕，第 1 讲）；section n → 第 n 节。命令放在冒号后面（G3）。 |
| persist / live memory / inventory / tickets / pending workflows / one process / one session | 在线运行写下的记忆 / 库存 / 审批单 / 待处理的工作流 / 进程 / session | S16[1]：库存、订单、审批单和待处理的工作流只存在于一个进程里；任务和历史，只存在于一个 session 里。 | 第 6 讲：session 照说；第 2–4 讲：process → 进程。Traces and live memory stay in SQLite. → 所有 trace 和在线运行写下的记忆都保存在 SQLite 里。 |
| tear down / exit / container shell / --rm / docker ps -a | 拆掉 / exit / --rm / docker ps -a | S16[2]：在每个 container 的 shell 里输入 exit；它是用 --rm 启动的，所以 docker ps -a 里什么都不剩。 | 第 4–6 讲：tear down → 拆掉（Pause, and tear down. → 暂停一下，把它拆掉。）。en_display：--rm、docker ps -a。 |
| trace database / prompts and outputs / redacted | trace 数据库 / 输出 / 脱敏 / 删掉 | S16[3]：里面的 trace 数据库存着你的 prompt 和输出，密钥已经脱敏；用完了就把它删掉。 | redacted → 脱敏。The outputs folder stays on your laptop. → 你笔记本上的 outputs 目录会留着。（不以 outputs 开头） |
| docker image rm / frees / the base image stays / close the terminal / shell history / your usage / delete the runtime | docker image rm / 腾出 / 关掉终端 / shell 历史记录 / 用量 / 运行时 | S16[4]：用 docker image rm，能腾出那 1.77 GB 里的大部分；留下的是 base image。 | Docker image remove → docker image rm（en_display）。第 6 讲：runtime → 运行时。 |
| reflection questions / pick one run | 反思问题 | S16[7]：README 最后有五个反思问题。 |  |
| Test yourself / fixture batch | 自测 / 状态 | S16[8]：哪一种状态能授权一个行动？ | 第 4–6 讲：Test yourself. → 自测一下。What survives harness without trace? → 去掉 trace 之后，harness 还剩下什么？（不以 harness 开头，A5） |
| next / fine-tunes / Agent Platform / formerly Vertex AI / pytest / unittest / a good model | 接下来 / 微调 / Agent Platform / Vertex AI / pytest / unittest / 范例 | S16[9]：第 9 讲用 pytest 测试代码；这里的 281 个测试用的是 unittest，是很好的范例。 | 第 5 讲：fine-tune → 微调。a good model（值得照着学的例子）→ 范例，不写“模型”（A7）。 |

### 带下划线的名字与代码表达式（A6） / Names with an underscore, code expressions (A6)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| build_agent / preview_order / get_catalog / get_stock / load_skill / read_skill_resource / start_order / get_order_status / assess_event / build_act4 / order_placed / no_cart / approval_mode="always_require" / OPENAI_API_KEY / RUN_ID / harness.without("trace") / .add() / .without() / Context("basic") | build agent / preview order / get catalog / get stock / load skill / read skill resource / start order / get order status / assess event / build act 4 / order placed / no cart / approval mode 设为 always require / OpenAI API key / run ID / harness without trace / add 和 without 方法 / basic Context | S12[3]：新的工具是 get stock、load skill 和 read skill resource。 | A6、B3；字面形式只出现在 en_display 里（D4）。 |

### 标签、进度条与固定句式 / Tags, tracker, fixed patterns

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the tracker / the gray tag / the lecture slides / your turn / a tag says your turn | 进度条 / 灰色标签 / 课件 / your turn | S01[6]：左上角的进度条显示 README 的步骤；右上角的灰色标签显示对应的课件。 | 和第 5、6 讲一致；标签名照画面写（A11）。When a tag says your turn, … → 看到标签写着 your turn，就…… |
| an extra / extras / an extra check / not in the README | 额外 / 额外检查 | S02[8]：在第二个终端里做三个额外检查。 | D6。these steps are extras → 这几步都是额外的。 |
| at the time of recording / we recorded this / one honest limit | 录制时 / 录制 | S01[7]：坦白说一个限制：我们在 2026 年 10 月 20 日录制，没有 OpenAI 密钥。 | A9：录制时，绝不省略（Python 3.13.16、agent-framework 1.19.0、gpt-5.6-luna）。 |
| the staff / the study guide / the exercises / customer IDs are masked | 课程团队 / 学习指南 / 练习 | S01[8]：顾客 ID 在画面上遮住了，每条命令都在学习指南里。 | 同第 5、6 讲。 |
| a small slip / a harmless slip | 一个小疏漏 / 一个无害的小疏漏 | S06[6]：一个小疏漏：--compare 不会。 | A9（同第 5、6 讲）：所有勘误用同一个说法，后面紧跟改法。 |
| Something to ponder / Yes, and yes / No | 来想一个问题 / 是，也是 / 不会 | S05[8]：来想一个问题。 | 第 1、2 讲：Something to ponder. → 来想一个问题。五道思考题（S05[8]、S07[5]、S09[6]、S11[2]、S12[6]）不泄露答案（A9）。 |
| Pause and run it / Pause, and tear down | 暂停一下 / 在这里暂停 | S02[2]：暂停一下，跑一遍。 | D6。 |
| part 1 / part 2 / lecture 2 / lecture 5 / Lecture 7 / lecture 8 / Lecture 9 / seven sections | 第一部分 / 第二部分 / 第 2 讲 / 第 7 讲 / 七节 | S01[5]：第 7 讲和 README 分成同样的七节，顺序也一样。 | A10。sections（README 和课上的大纲）→ 节。 |

### 数字与单位 / Numbers and units

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| step 1 / steps 2 and 3 / steps 1 to 3 / setup step 4 / line 484 | 第 1 步 / 第 2、3 步 / 第 1 到第 3 步 / 第 484 行 | S02[7]：暂停一下，跑第 2、3 步，等到出现这个提示符。 | C1。setup step 4 → Setup 的第 4 步；README line 484 → README 第 484 行。 |
| counts: 281 tests / 1,942 tokens / 4,540 / 21,000 / 15,000 characters / 16,000 tokens / 2,400 / 26 messages | 281 个测试 / 1942 / 4540 / 21000 / 15000 个字符 / 16000 个 token | S11[1]：窗口是 16000 个 token，其中 2400 个留给回复。 | C1：不加千位分隔符。 |
| money: 150 dollar budget / 5,600 cents / 6,400 cents / 64 dollars / 220 dollars 80 / 50 dollars 10 / 200 dollar threshold | 150 美元 / 5600 美分 / 6400 美分 / 64 美元 / 220.80 美元 / 50.10 美元 / 200 美元 | S01[1]：第一个提议 1050 克，5600 美分。 | C2：dollars → 美元，cents → 美分，照画面（$220.80 → 220.80 美元）；不换算成人民币。 |
| sizes and times: 1.77 gigabytes / 38 seconds / 100 seconds / 120 seconds / 180-second / grams / 80 percent | 1.77 GB / 38 秒 / 克 / 80% | S02[8]：再看 docker images：1.77 GB，因为框架把所有集成都装上了。 | C2。 |
| versions and model: Python 3.13.16 / agent framework 1.19.0 / GPT 5.6 Luna | Python 3.13.16 / agent-framework 1.19.0 / gpt-5.6-luna | S03[3]：模型检查只打印默认模型，并不调用它：录制时是 gpt-5.6-luna。 | C2：包名和模型 ID 照打印的写，中英两行一致（en_display）。 |
| dates: October 20, 2026 | 2026 年 10 月 20 日 | S01[7]：坦白说一个限制：我们在 2026 年 10 月 20 日录制，没有 OpenAI 密钥。 | C2。 |

### 课程、产品与名字 / Course, products, names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| customer / the first customer / the second customer / customer IDs / masked | 顾客 / 第一位顾客 / 第二位顾客 / 顾客 ID / 遮住 | S11[7]：第一条命令给第二位顾客存一条偏好，记忆在任何模型调用之前就打印出来，即使没有密钥也一样。 | A10：两位顾客不提名字，也不写他们的 ID（画面上是遮住的标记）。 |
| a tasting / guests / a French cheese / no nuts / the shop / a fictional cheese shop | 品鉴会 / 客人 / 法国奶酪 / 坚果 / 店 / 虚构的奶酪店 | S01[0]：一位顾客要为一场品鉴会买奶酪：宾夕法尼亚 12 位客人，150 美元预算，不要坚果，一款法国奶酪，还有一款浓烈度 4 或以上。 |  |
| the request / the confirmed request / today's request / the ask | 需求 / 已确认的需求 / 今天的需求 | S07[8]：所以筛选候选有帮助，但校验说了算，今天的需求优先于保存的偏好。 | A7：顾客的 request → 需求；API 或工具的 request → 请求。 |
| cart / the final cart / order / place an order / no order placed | 购物车 / 最终的购物车 / 订单 / 下单 / 没有下单 | S01[3]：代码检查了购物车本身：1200 克，64 美元，满足店铺规则，没有下单。 |  |
| charge a customer's card / a malformed number / the comma in the wrong place | 刷卡 / 格式错误的数字 / 逗号放错了地方 | S01[2]：这两个里面，你会让哪一个去刷顾客的卡？ |  |
| cheeses: Comté / Époisses / Bûcheron / Taleggio / Mimolette / Munster / Brie | Comté / Époisses / Bûcheron / Taleggio / Mimolette / Munster / Brie | S08[4]：第 2、3 步是运输这一课，用的是一位顾客自己的购物车：Comté、Bûcheron 和 Époisses，寄往宾夕法尼亚。 | A10：店里的商品名照画面写，带重音符号（不写“孔泰”“布里”：观众要在输出里对照）。检查器切出来的是 Comt、poisses、cheron（D3）。 |
| AC215 / the README / the tutorial / agent-harness / the course notebook | AC215 / README / 教程 / agent-harness | S02[1]：先做两个额外步骤：git clone，因为 README 默认你已经有一份；然后进入 agent-harness 目录，所有准备命令都在这里运行。 |  |
| products: OpenAI / Docker / Colab / Drive / Jupyter / Python / SQLite / HTML / HTTPS / JSON / SDK / CLI / MCP / Google / Agent Platform / Vertex AI / pytest / unittest | OpenAI / Docker / Colab / Drive / Jupyter / Python / SQLite / HTML / HTTPS / JSON / SDK / CLI / MCP / Google / pytest / unittest | S16[9]：接下来，第 8 讲会在 Google 的 Agent Platform 上微调模型，它以前叫 Vertex AI。 | 拉丁字母（A1 b）。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 中文 | 说明 |
|---|---|---|
| Video title: AC215 · Lecture 7 — LLM: Agents II (follow-along: agent-harness) | AC215 · 第 7 讲：LLM 智能体 II（跟练：agent-harness） | H1。Agents II → 智能体 II（同第 6 讲的“智能体 I”）；跟练 = follow-along。 |
| Part 1 / Part 2: one agent — setup, the agent loop, harness layers and context (Acts 1–2) / the harness takes control — workflows, approvals, memory, skills, agent systems and evaluation (Acts 3–6) | AC215 · 第 7 讲（上）：一个智能体——环境准备、智能体循环、harness 层与上下文（第 1–2 幕） / AC215 · 第 7 讲（下）：harness 接管——工作流、审批、记忆、技能、智能体系统与评测（第 3–6 幕） | H1。the harness takes control → harness 接管；Acts → 幕。 |
| Chapters S01–S07: Which sentence would you trust? / One container, no ports / Verify offline, and the Colab road / Act 1: an agent, measured / Act 1: wrap it in a harness / Act 2: same agent, different context / Act 2: sieves and lanes | 你会相信哪一句？ / 一个容器，不开端口 / 离线验证，以及 Colab 这条路 / 第 1 幕：给智能体（agent）算一笔账 / 第 1 幕：给它套上 harness / 第 2 幕：同一个智能体，不同的上下文 / 第 2 幕：筛选与两条通道 | H1。an agent, measured → 给智能体（agent）算一笔账（调用、消息和 token 都数出来）；sieves and lanes → 筛选与两条通道（review_spoken 第 17 条）。 |
| Chapters S08–S16: Act 3: rails, not suggestions / Act 3: approve this exact cart / Act 4: a planner with five drawers / Act 4: compaction, the capsule and memory / Act 5: skills are manuals, not keys / Act 6: an agent that calls a workflow / Evaluation: the trace is the evidence / Evaluation: one change, k runs, a diff / Tear down, recap, and what's next | 第 3 幕：是轨道，不是建议 / 第 3 幕：批准的就是这辆购物车 / 第 4 幕：有五个抽屉的规划器 / 第 4 幕：压缩、胶囊与记忆 / 第 5 幕：技能（skill）是说明书，不是钥匙 / 第 6 幕：调用工作流的智能体 / 评测：执行记录（trace）就是证据 / 评测：一处改动，跑 k 次，看 diff / 清理、回顾与下节预告 | H1。rails → 轨道；keys → 钥匙（不是“密钥”，A7）；the trace → 执行记录（trace）；收尾章节同第 6 讲。 |

### 配套材料的书面语体 / Written register of the companions

| English | 书面 | 说明 |
|---|---|---|
| container / image / base image / repo / clone / commit / port / prompt / system prompt / agent / session / notebook / token / pin / lock file / trace / skill / fixture / label / harness | 容器 / 镜像 / 基础镜像 / 仓库 / 克隆 / 提交 / 端口 / 提示词 / 系统提示词 / 智能体（agent）/ 会话（session）/ Colab 笔记本（notebook）/ 词元（token）/ 固定版本（pin）/ 锁文件（lock file）/ 执行记录（trace）/ 技能（skill）/ 测试夹具（fixture）/ 标签（label）/ harness | H3、A4：在配套材料里首次出现时加英文括注；harness 书面也写 harness，首次出现解释一次：harness（模型外面那层由代码执行的循环、限制、上下文和检查）。 |
| action boundary / context engineering / context window / compaction / capsule / progressive disclosure / allowlist / eval set / LLM as judge | 行动边界 / 上下文工程 / 上下文窗口 / 压缩 / 胶囊 / 渐进式披露 / 白名单 / 评测集 / 让 LLM 当评委 | H3：和字幕同一个词。术语对照表的其他常见译法：harness 外壳 / 驾驭框架；trace 链路追踪 / 轨迹记录；fixture 测试夹具 / 固定装置；progressive disclosure 渐进式披露 / 逐步披露；allowlist 白名单 / 允许列表；eval set 评测集 / 评估集；LLM as judge LLM 评委 / LLM 裁判；handoff 交接 / 移交；token 词元 / 令牌。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

AC、access、act、add、Agent、agent、agent-framework、agent-harness、AI、allow、always、API、approval、approval.decided、approval.requested、approve、assess、assets、assistant.md、base、bash、basic、BLOCKED、Brie、Budget、build、call、calls、cart、CartCheck、case、catalog、cd、chat、cheron、CLI、cli.py、clone、Colab、commit、compare、Comt、container、Context、context、context-fixture-、context-live-、context-live-a、context-live-b、copy、core、cp、customer、db、decline、DECLINED、demo-compaction、diff、Docker、docker、docker-shell.sh、Dockerfile、docs、Drive、echo、email、email-decision、enriched、error、evaluate、event、exec、exit、export、extra、failed、false、first、fixture、Framework、GB、get、git、Google、gpt-、harness、help、HTML、html-output、HTTPS、ID、image、images、in、Inspect、inspect、inspect-run、Invalid、JSON、json-output、Jupyter、key、label、Learning、list-runs、LLM、load、lock、ls、luna、malicious、manager-approval、manager-decision、Maximum、MCP、Microsoft、Mimolette、missing-details、mkdir、MLOps、mode、model、model.failed、Munster、no、not、Notebook、notebook、null、NY、observability.sqlite、of、OK、OpenAI、or、order、order.placed、out-of-stock、outcome、outputs、PA、pa-shipping、pa-shipping-blocked、passed、personalized、pin、PLACED、placed、Platform、poisses、policy.decision、port、preference-override、preview、preview-context、printf、process、prompt、prompt-file、prompts、propose、ps、pull、pyproject.toml、pytest、Python、python、reached、read、README、references、remember-preference、repeats、repo、report、Requested、require、resource、Retrieved、rm、rsp、run、run.finished、Save、SAVED、saved、scenario、schema、scripts、SDK、secret、Secrets、secrets、session、Setup、SHA-、shell、shop、show-json、skill、SKILL.md、SQLite、standard、start、status、stock、stock-question、student、system、Taleggio、tasting-planning、tests、the、token、Tool、tools、Trace、trace、transmitted、true、turn、two-orders、unauthorized、unittest、UNRESOLVED、user、uv.lock、vendor-document、vendor-outreach、Vertex、view、view-report、without、your

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令（git clone、ls -a、bash docker-shell.sh、docker ps、docker images、docker inspect、docker exec、docker ps -a、docker image rm、exit、python cli.py --help、python cli.py --act 1 --scenario standard、diff；README 的三行 read 命令只按描述说）、参数（--compare、--show-json、--preview-context、--fixture、--inspect-run、--prompt-file、--model、--rm）、场景和模式的值（standard、personalized、preference-override、missing-details、pa-shipping、manager-approval、out-of-stock、two-orders、basic、enriched；the blocked scenario → blocked 场景）、label（context-fixture-1；act2-context-live-1、context-live-a、context-live-b 只在画面上）、文件名、目录名和路径（docker-shell.sh、Dockerfile、agent-harness、secrets、docs、outputs、SKILL.md、scripts、tasting-planning、vendor-outreach）、类名和层名（Trace、Budget、Context、CartCheck）、代码里的值（OK、null、false、true、approve、decline、no cart、error、allow、placed、saved、no）、终端和 trace 原文（Requested tools、Tool call、Maximum of 8 model calls reached、Retrieved context、Invalid or unauthorized、UNRESOLVED、BLOCKED、DECLINED、status、email transmitted）、事件名（approval.requested、approval.decided、policy.decision、order.placed、run.finished、model.failed）、检查名前缀 outcome 和 process、包名 agent-framework 和模型 ID gpt-5.6-luna（C2）、README 的字样（Inspect the context first、Setup；A11）、Colab 界面的字样（Save a copy in Drive、Notebook access、secret）、旁白提到的画面标签（your turn），以及按旁白说法写的带下划线名字和代码表达式（A6）。（b）**产品、组织、课程和名字**：AC215、OpenAI、Google、Agent Platform、Vertex AI、Docker、Colab、Drive、Jupyter、Python、SQLite、HTML、HTTPS、JSON、SHA-256、SDK、CLI、MCP、LLM、pytest、unittest、README、店里数据中的奶酪名（Comté、Époisses、Bûcheron、Taleggio、Mimolette、Munster、Brie；A10）、PA 和 NY。（c）**中国 MLOps 工程师在实验课上真会说英文的词**，封闭清单：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的 container、image、base image、pull、port、API、ID、token、Dockerfile；第 5 讲的 prompt（只指 LLM 的 prompt）、system prompt、LLM、agent、CLI；第 6 讲的 notebook、session、schema、SDK、harness；这一讲新增 trace（A3）、skill（A3）、fixture（A3）、label（A3）、diff（命令和它的输出，A3）、run ID（A6）。一个词要进（c），必须实验课上真这么说，而且中文生硬、有歧义或和别的词撞车。绝不为了“味道”用英文：tool、tool call、loop、round、message、workflow、graph、node、edge、layer、ring、admission、audit、budget（概念）、context（概念）、packet、slot、policy、rules、validation、revalidation、verification、checkout、cart、order、approval、ticket、fingerprint、hash、receipt、review、manager、host、planner、memory、history、state、task、compaction、capsule、truncation、window、quarantine、allowlist、guard、detector、metadata、reference、asset、progressive disclosure、evaluation、test case、suite、baseline、batch、repeat、report、scorecard、confounder、judge、outcome、trajectory、cost、evidence、live、offline、scripted、fallback、backstop、turnstile、rail、sieve、lane、drawer、seam 都说中文（A3）。
- **[A2]** container 和 image（同第 2–6 讲）。字幕说 container、image、base image，和助教在实验课上一样：一个 container、构建 image、base image 已经在机器上了、container ID、container 的 shell；量词“个”。标题、章节名、meta.yaml 和配套文档写“容器”“镜像”“基础镜像”（A4）；字幕里绝不写“镜像”。pull 照说（your first build also pulls it → 你第一次构建还要先 pull 它）。build → 构建（构建 image；CLI 构建的正是这个）。mount → 挂载，publish a port → 发布 port，no ports → 没有 port（第 4、5 讲）。layer（image 的层）→ 层；the layer trick from lecture 2 → 第 2 讲讲过的分层技巧（第 2–4 讲）。
- **[A3]** harness 的词汇（这一讲新增）。**主线**：the model proposes; the harness decides → 模型提议；harness 决定（S01 和 S16 同一个说法）；propose / proposal → 提议（未经验证的提议），decide → 决定；两栏（左边 / 右边）；harness 照说（第 6 讲），harness 工程师、harness 工程、模型外面的代码。**课上的框架**（SLIDES.md）：action boundary → 行动边界，five concerns → 五个关注点，Control flow / Tools / Context & memory / Verification / Sub agents → 控制流 / 工具 / 上下文与记忆 / 验证 / 子 agent，who decides → 谁来决定，move right / left → 往右移 / 往左移，风险高、无法撤销、可预测、审计，give control to code → 把控制权交给代码；六步 Think / Reason / Plan / Execute / Verify / Response → 思考 / 推理 / 规划 / 执行 / 验证 / 回复（验证步骤、回复步骤），hidden reasoning → 隐藏的推理；the invisible layer → 看不见的那一层，the lecture's stack → 课上的上下文栈，retrieved information → 检索信息，outside data → 外部数据，two lanes → 两条通道（system 通道 / user 通道），长期 / 短期记忆，compaction trigger → 压缩触发条件，what persists where → 什么持久保存在哪里；skills → skill，progressive disclosure → 渐进式披露（发现 / 激活 / 使用资源），专业知识缺口，上下文预算，手 / 插座 / 说明书；agent 系统、单个 agent、由 agent 组成的图、管理者模式、把 agent 当工具、对等的 agent、交接（第 6 讲）；autonomy spectrum → 自主性光谱（基于规则、结构化输出、混合型、完全自主）；结果 / 轨迹 / 成本，评委，让 LLM 当评委，评测集，测试用例，测试集，基线，改进循环，只改一层，合并或者继续迭代。**第 1 幕**：act → 幕（第 1 幕、六幕），循环、轮、消息、接缝、商品清单、场景、需求（the ask）、第 1 次调用、输入 token、计费、确切的消息、已确认的需求；trace 照说（实验课口语：看一下 trace；Trace 层；SQLite 里的 trace）；结构化的回复格式。**harness 层**：harness 层、环、内环、调用准入、放行并计数、工具审计、店铺规则、每层一个功能、套上 / 拆掉、闸机、框架的兜底、循环迭代、调用次数上限、总的时间预算、只报告，从不修复、新的配置、裸循环。**第 2 幕**：上下文、模式（basic、enriched 照写）、空位、店铺政策、检索到的数据、保存的偏好、保存的口味、并排对比表、结论、打平、退步、单次运行、对话消息、上下文包、浓烈度（funk）、按州的检查、生乳、虚构的规则、用例、重复、检查点、来源、信任标注、店铺数据、筛子、过敏原、过敏检查、运输规则、候选、筛选、校验、Python 过滤器、向量检索（第 5 讲）、user 消息、是数据，不是指令、系统规则、证据。**第 3 幕**：工作流（第 6 讲）、下单路线、图 / 边 / 节点、确认 / 提议 / 校验、修订循环、修订、搭配、经理审核、经理审批、重新校验并下单、propose cart 节点（A6）、轨道、站、数量、流转、定价、下单、回执（第 6 讲）、尝试、坑、运输这一课、门槛、经理、宿主程序、指纹（第 2 讲）、哈希（第 5 讲）、商品明细、小计、政策、商品属性、重新检查、结账、决定、审批单、对得上、批准（第 6 讲；作为流程叫“审批”）、授权、预留、库存违规、有上限的修订。**第 4 幕**：规划器（第 6 讲）、活动、保存的记忆、历史、任务、五种状态、抽屉、活动说明、供应商、待办工具、供应商有货、审核、由代码写的正文、权威、压缩、恶意的供应商文档、合成笔记、上下文窗口、截断、最旧的消息、胶囊、应用状态、钉上一个新的、重新钉上、菜单、待处理的审核、未完成的工作、隔离、检测器、防线、收件人白名单、记忆练习、来访。**第 5 幕**：skill 照说（实验课口语：写一个 skill、加载 skill；画面上有 SKILL.md 和 skills/），装着操作流程的目录、元数据（第 5 讲）、主文件、参考资料、资源文件、提示、触发条件、完整的采购流程、邮件模板、保险（backstop）、收件人、上级目录、绝对路径、符号链接、发出去。**第 6 幕**：外层（第 6 讲）、提议者、共享的时钟、窄工具、里外反过来、应用。**评测**：评测、一次运行、run ID 照说（A6）、事件、模板、照字面输入、报告、HTML 记分卡；label 照说（--label 的值：label 是 context-fixture-1；每个 label 都不可更改）；batch → 批次 / 这一批（Batch A → 批次 A）；配置、改动的配置、混杂改动、翻转、改进 / 退步 / 不变、属性、证明、产物（eval set 是最有价值的产物）；diff 照说。**运行方式**：live（真的调用模型、按 token 计费）→ 在线，offline → 离线，正好是画面上的一对（offline · free / live · billed per token）：在线命令、在线运行、在线模型、在线运行的回答或模型的回答、在线运行写下的记忆；不写“实时”（第 3 讲的 live view），字幕里不写 live；scripted → 脚本模拟的（一个脚本模拟的规划器；脚本模拟的运行测的是这套机制，不是模型）；fixture 照说（用 fixture 时、把 fixture 关掉、模型的位置上坐的是一个脚本）；ran for real → 真实运行（第 6 讲）。
- **[A4]** 字幕与书面。字幕说 repo / clone / commit / container / image / base image / port / prompt / system prompt / agent / session / notebook / token / pin / lock 文件 / trace / skill / fixture / label；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 基础镜像 / 端口 / 提示词 / 系统提示词 / 智能体（agent）/ 会话（session）/ Colab 笔记本（notebook）/ 词元（token）/ 固定版本（pin）/ 锁文件（lock file）/ 执行记录（trace）/ 技能（skill）/ 测试夹具（fixture）/ 标签（label），核心概念首次出现时加英文括注（旁白以外可以用括号）。harness 书面也写 harness（第 6 讲 H3）。命令不受影响（git clone、--fixture、--label）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符、重音符号都不改）；不翻译、不变形、不加引号、不加《》或代码格式。需要时加中文中心词：docker-shell.sh 这个脚本、secrets 目录、docs 目录、outputs 目录、scripts 目录、build agent 这个函数、preview order 工具、get catalog 工具、propose cart 节点、missing-details 场景、personalized 场景、standard 场景、blocked 场景、basic 模式、--model 参数、docker ps 这条命令。句子不以实物或小写的英文词开头：前面先放中文（所谓 harness……；这个 harness……；这个 trace……；所有 trace……；这个 skill……；加载 skill……；每个 label……；其中 basic……；而 enriched……；先看 docker ps：……；再看 docker images：……；用 docker inspect……；用 docker image rm……；命令行里的 --model 参数……；这个 --inspect-run……；你笔记本上的 outputs 目录……；比较只在……；下单的证据……），所以字幕也不会以小写字母开头。产品名、大写缩写和类名（OpenAI、Docker、Colab、Python、SQLite、SDK、CLI、MCP、LLM、README、AC215、Dockerfile、Trace、Budget、Context、CartCheck、Comté、Mimolette、Munster）可以开头。
- **[A6]** 带下划线的名字和代码表达式（同第 3–6 讲）。没有 say: 时，检查器把显示行当作朗读文本，拒收 letter_letter、括号、代码里的引号和 =；SAY 本身也从不把这些下划线和括号念出来。所以中文行按旁白的说法写：下划线变空格，大小写同 SAY，加中文中心词或放在明显的名字位置。对照：build_agent → build agent 这个函数；preview_order → preview order 工具；get_catalog → get catalog 工具；get_stock → get stock；load_skill → load skill；read_skill_resource → read skill resource；start_order、get_order_status、assess_event → start order、get order status、assess event；build_act4 → build act 4；"order_placed": False → order placed 设为 false；no_cart → no cart；approval_mode="always_require" → approval mode 设为 always require（同第 6 讲的 mode 设为 any）；OPENAI_API_KEY（变量和 Colab secret 的名字）→ OpenAI API key；RUN_ID → run ID；harness.without("trace") → harness without trace（What survives harness without trace? → 去掉 trace 之后，harness 还剩下什么？）；.add() / .without() → add 和 without 方法；Context("basic") → basic Context；propose_cart → propose cart 节点；test_chat_view.py → chat view 测试（SAY 说的是 chat view tests）。英文行用 en_display 给出字面形式（D4）。等工具链允许显示行保留下划线（I1）时，再把这些空格形式换回字面形式。
- **[A7]** 要分清的词。笔记本（laptop）≠ notebook（Colab、课程的 notebook）≠ 笔记（S11 的合成笔记）。层（harness 层：Trace、Budget……；也指 S02 里 image 的层）≠ 课上看不见的那一层 ≠ 环（V3 的环：层在图上画成环）。状态（应用状态、五种状态）≠ 州（美国的州：按州的检查、宾夕法尼亚 / 纽约）≠ status（打印出来的字段：status 为 error）。需求（顾客的 request：the ask、已确认的需求、今天的需求、宿主程序确认这些需求）≠ 请求（API 或工具的请求：trace 显示的是请求和结果）≠ 订单 1 / 订单 2（Request 1 / Request 2，画面上是 request-1 / request-2）。宿主程序（the host：运行 harness、接收审批的应用）≠ host（第 6 讲 MCP 里的角色；这里不用）。经理（店里的 manager，一个人：你就是经理、经理审批、经理审核）≠ 管理者模式（课上的 manager pattern）。密钥（API key）≠ 钥匙（能打开权限的钥匙：skills are manuals, not keys；审批抽屉上的黄色钥匙）≠ OpenAI API key（变量名，A6）。在线（live：真的调用模型并计费）≠ 实时（第 3 讲的 live view）≠ 录制（录这期视频：录制时、录下来的回答）≠ 记录（写进运行数据库：失败的运行照样会记录下来；记录购物车）。兜底（SDK 的 fallback，40 次迭代）≠ 保险（代码里的 backstop）≠ 防线（真正的 guards：白名单和你的审核）≠ 护栏（课上的 guardrails，第 6 讲）。label（评测批次的 --label 值）≠ 标签（画面上的 tag：灰色标签、your turn 标签）≠ 信任标注（上下文包里来源的 trust label）。上下文包（context packet）≠ 包（package：pin 了版本的包）。pin（版本：pin 了版本）≠ 钉上（胶囊被钉上、重新钉上）。轨道（V5 的 rails）≠ 轨迹（课上的 trajectory）≠ 路线（下单路线、购物车的路线）。模型（the model）≠ 范例（S16[9] 的 a good model）。校验（validate、validation、revalidate → 重新校验：由店规判定）≠ 验证（verify：验证环境、课上的 Verify 步骤）≠ 检查（check：CartCheck 检查商品明细、检查、按州的检查）≠ 重新检查（库存会被重新检查）。批准（approval、approve；输入的 approve、decline 照写）≠ 审批（流程：经理审批、审批抽屉、审批单、审批顺序）≠ 审核（review：经理审核、邮件的审核、你的审核）≠ 反思（README 的反思问题）。回执（receipt：下单的证明）≠ 审批单（approval ticket）≠ 指纹（fingerprint）。用例（评测的 case：测试用例）≠ 场景（--scenario 的值）。节（README 或课上的 section：第 7 节、七节）≠ 部分（视频的 part：第一部分）≠ 幕（act）。提示（hint）≠ prompt（LLM 的 prompt）≠ 提示符（shell 的 prompt：这个提示符、container 的提示符）。活动说明（活动的 brief）≠ 简报（第 6 讲的 newsletter）。行动（action：行动边界、授权行动）≠ 操作（只用于 an action can't be undone → 操作无法撤销）。政策（policy：店铺政策、指纹里的政策）≠ 规则（rules：店铺规则、运输规则、虚构的规则、系统规则）。拆掉（tear down；拆掉一层）≠ 删掉 / 删除（删掉 outputs、删除运行时）≠ 去掉（去掉一个工具；without compaction → 去掉压缩）。课程团队（the staff）≠ 课上（the lecture）≠ 课件（slides）≠ 授课老师（the instructor，绝不提名字）。
- **[A8]** 语体：助教带实验课。短指令，用口语动词（跑、装、敲、改、贴、删、拆、选、输入）；观众是“你”（一对一跟练；不用“您”“大家”“同学们”）；“我们”是录制时的我们（我们没有密钥）。分句内部用中文语序，分句顺序跟着英文（D9）。不要翻译腔：不写“让我们……”（说“我们来……”“先……”），不写“这就是为什么……”（说“所以……”），少用“被”字句，不叠“一个……的”。不用网络流行语。口语节奏按意思传达：Here are two answers → 这是两个回答；The second run printed more → 第二次运行打印了更多内容；Here's what a key gets you → 下面是有密钥时的样子；Then stock, price, pairings and preview → 然后是库存、价格、搭配和预览；Back to the hook → 回到开头的例子；And where does it go? → 那它放在哪儿？；Yes, and yes. → 是，也是。；No. → 不会。；One trap → 有个坑；A capsule. → 一个胶囊。；Then compare, offline. → 然后离线比较。；No handoffs. → 没有交接。；Trust the last line. → 以最后一行为准。
- **[A9]** 准确。量词照译：only 只，every 每个 / 每次，all 全部 / 全都，about 大约，at most 最多，never 从不 / 绝不，even without a key 即使没有密钥。at the time of recording 每次都译“录制时”，绝不省略。数量、行号、步骤号和版本号照屏幕（C1）。勘误语气温和，后面一定紧跟改法，放在一个说法里：a small slip → 一个小疏漏（S06[6]）；a harmless slip → 一个无害的小疏漏（S02[6]）。打印出来的结局：旁白对比或点名一次运行打印出来的结局时，照打印的写（ends unresolved, not blocked → 最后是 UNRESOLVED，不是 BLOCKED；The result: declined → 结果：DECLINED；status saved, email transmitted no → status 为 saved，email transmitted 为 no；the status, placed → 状态 placed；with status error → status 为 error）；叙述里的动词说中文（blocks it → 拦下它；the order places → 订单下单了；is placed → 下单了；ends with no order → 结束，没有订单）。思考题（S05[8]、S07[5]、S09[6]、S11[2]、S12[6]；Something to ponder. → 来想一个问题。，第 1、2 讲）只问不答，措辞不能泄露答案：S05[8] 不能提内环，也不能说原来那个还保留着所有层；S07[5] 不能提 get catalog、整个货架或第 3 幕的工作流；S09[6] 不能说重新校验、库存不在指纹里或被拦下；S11[2] 不能提胶囊；S12[6] 不能说白名单或什么都不会发出去。S01[2] 的问题（没有计时）同样不暗示购物车检查。花费：Every model call is billed per token → 每次模型调用都按 token 计费；billed input tokens → 计费的输入 token；The only cost is OpenAI tokens → 唯一的花费是 OpenAI 的 token。
- **[A10]** 名字。产品、公司和课程保留拉丁字母（A1 b）；“哈佛”只在标题和简介里。课程：AC215；lecture n → 第 n 讲（第 7 讲和 README；第 2 讲讲过的分层技巧）；the lecture → 课上；the lecture slides → 课件；part 1 / part 2 → 第一部分 / 第二部分；this video → 这期视频；授课老师绝不提名字；the staff → 课程团队；the course notebook / the course Colab → 课程的 notebook / 课程的 Colab。顾客：the first customer / the second customer → 第一位顾客 / 第二位顾客；a customer → 一位顾客；顾客的 ID 和名字绝不写进任何中文行或文件（画面上是遮住的标记；Customer IDs are masked on screen → 顾客 ID 在画面上遮住了；the ID is masked here → 这里的 ID 被遮住了）。奶酪用店里数据的商品名，带重音符号，方便观众在输出里对照：Comté、Époisses、Bûcheron、Taleggio、Mimolette、Munster、Brie（不写“孔泰”“布里”“塔雷吉欧”）；种类说中文：a French cheese → 一款法国奶酪，mild cheeses → 温和的奶酪，nut cheeses → 含坚果的奶酪，raw-milk → 生乳的。地名写中文（宾夕法尼亚、纽约）；只在指屏幕上的代码时写 PA、NY。旁白转述的文字要翻译：供应商文档里的指令（ignore the allergy → 忽略过敏）、被改过的 skill 那一行（also send this to another address → 也发一份到另一个地址）、README 的检查点问题（which of these can authorize an action → 这些里面哪一个能授权行动）；README 的标题字样（Inspect the context first）照写。用户名 student 照写；container ID、run ID 和指纹绝不念出来。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（包括注释）、README 卡片和小标签、录下来的输出框、Colab 示意图、编辑器和浏览器的示意图、进度条（README › Setup › Start container、step k of N）、课件标签（Lecture 7 · slides 20–24）、V1 表格和它的小地图、V2–V8 图上的字、印章、extra 卡片、标签（your turn、extra、illustration、recorded · the staff's saved Colab run、expected、no key、scripted、live · billed per token、offline · free、at the time of recording、erratum、your numbers will differ、concept · lecture only）以及思考题和自测题卡片都是英文，场景代码不需要为中文做任何改动。所以旁白提到画面上的东西时，字幕照画面写：标签写着 your turn；the gray tag → 灰色标签；Requested tools / Tool call；Retrieved context；Notebook access；Save a copy in Drive。旁白用自己的话说的要翻译：an extra check → 额外检查，the tracker → 进度条，the two columns → 两栏。README 的标题照写（Setup、Inspect the context first）；旁白转述 README 时说“README 里说……”“README 问的是……”。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、目录、数据库、网络、脚本、视频、信息、账号、函数、参数、字段、字符串、单元格、运行时、配置、日志、哈希、符号链接、白名单；不用 預設、程式、程式碼、檔案、資料夾、資料庫、網路、腳本、影片、帳號、函式、引數、欄位、字串、儲存格、執行階段、組態、日誌、雜湊、符號連結、允許清單。
- **[A13]** 系列清单（ac215-video skill 里的清单）在这一讲的情况。agent（15 次）和 harness（23 次）是主角；container（10 次）和 image（5 次）在准备和拆除里（A2）；base image 两次；Dockerfile 一次（S02[5]）；port 两次（不发布任何 port、没有 port）；prompt 既有 LLM 的 prompt（prompt 文件、改一次 prompt、你的 prompt 和输出、改动的配置：prompt、fixture 不看 prompt、system prompt），也有 shell 的提示符（这个提示符、container 的提示符 → 提示符，A7）；token 指 LLM 的 token（S01、S04、S11、S12、S14）；pull 一次；clone 两次；commit 一次（S16[4]：别让密钥进文件、commit）；session 一次（S16[1]）；notebook 很多次；schema 一次（S16[5] schemas → schema）。这一讲新进清单的：trace、skill、fixture、label、diff。这份稿子里没有：pipeline、endpoint、embedding、volume、venv、PATH（SAY 里的 path 是文件路径 → 路径）、LoRA、CI、push；repo 只出现在 repository map（S16[0] → repo 地图）。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（输入 exit、Python 3.13.16、第 484 行、281 个测试、1.77 GB、220.80 美元、secrets 目录、basic 模式、Comté 和 Mimolette）。检查器对每个显示句都检查缺少的空格。实物内部的空格照原样（python cli.py --help、docker image rm）；绝不在实物内部加空格。全角标点旁边不加空格（……bash docker-shell.sh，构建……；……decline：）。@ 和汉字之间也加空格（@ 符号后面）。不要用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，挨着实物也一样（输入 approve。）。列举用 、（确认、提议、校验；start order、get order status、assess event）。不用任何括号：（）、()、《》、【】、[]、<>（没有 say: 时检查器拒收，双语字幕带也不需要括注）。“”只用于中文里引用的一个想法或词（课上“只改一层”的规则）；实物、标签名、界面字样、终端原文和状态名都不加引号。一个中文句子（对应一个英文句子）内部不出现 。？！：用 ，；：；一句里最好只有一个冒号。英文有冒号时，“第 N 步”后面加全角冒号（Step 1: act 4. → 第 1 步：第 4 幕。）。问句保留 ？。
- **[B3]** 检查器拒收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后面的 !、括号、letter_letter）：绝不抄进中文行；改用文字说或换个说法（A6）。approval_mode="always_require" → approval mode 设为 always require；"order_placed": False → order placed 设为 false；harness.without("trace") → harness without trace；Context("basic") → basic Context；revisions ≤ 2 → 最多两次；26 → 5 messages → 26 条变成 5 条；$ 和 ¢ → 美元和美分（C2）。允许并照画面保留的：路径和名字里的 . 和 /（docker-shell.sh、SKILL.md、python cli.py、approval.requested、order.placed），参数和名字里的 -（--compare、--show-json、--rm、docker ps -a、missing-details、context-fixture-1、gpt-5.6-luna、agent-framework、SHA-256），@（@ 符号后面），%（80%），重音符号（Comté、Époisses、Bûcheron）。

### C. 数字、版本号与单位

- **[C1]** 显示文本里的数字。凡是对应屏幕、终端、代码、课件上的数字，或 SAY 里用阿拉伯数字写的数字，一律用阿拉伯数字，不加千位分隔符，和终端打印的一样（1050、5600、1200、6400、1942、4540、21000、15000、16000、2400、3000、1400、1600、1000）：步骤号（第 1 步、第 2、3 步、第 1 到第 3 步、第 2 到第 4 步、Setup 的第 4 步、评测第 1 步）、幕号（第 1 幕……第 6 幕）、调用序号（第 1 次调用、第 6 次调用）、尝试（第 1 次尝试）、行号（README 第 484 行）、讲和节（第 2 讲、第 7 讲、第 7 节）、数量（12 位客人、60 位客人、40 位客人、281 个测试、9 个 notebook 测试、12 个 chat view 测试、8 次模型调用、20 次工具调用、16 次模型调用、40 次循环迭代、12 次在线运行、4 次在线运行、3 个错误、1 个缺失、26 条变成 5 条、21 条、7 次压缩、1 条对话消息、2 条、4 次运行、0 次）、401、版本、大小、时间、金额、日期。SAY 里用英文单词写的小数量和序数用汉字：两个回答、七节、六幕、五个工具、四层、五层、三层筛子、十二种奶酪、七种、两条通道、三行、两个问题、三步、六次加载、五种状态、两种模式、三种评委、两个订单、五个问题、五个反思问题、一个胶囊、十二条合成笔记、第一位顾客 / 第二位顾客、第一部分 / 第二部分、第一个 / 第二个回答、最多两次、重复两次、三次、零次。句首的 12 guests 在中文里放进分句，仍写数字（宾夕法尼亚 12 位客人）。
- **[C2]** 单位、版本、模型 ID、金额和日期。大小照屏幕加半角空格：1.77 GB。时间：38 秒、大约 100 秒、120 秒、180 秒的时钟、一分钟或更久（SAY 里是单词）。重量：1050 克、900 克、差 300 克、0 克。百分比：80%、一半以下（back under half）。金额照屏幕，不换算成人民币：150 美元、64 美元、220.80 美元（220 dollars 80）、50.10 美元（50 dollars 10）、200 美元的门槛、5600 美分、6400 美分。版本连名字一起写：Python 3.13.16、agent-framework 1.19.0（check_sdk 打印的包名）。模型 ID 照代码写，中英两行一致：gpt-5.6-luna（SAY 里是 GPT 5.6 Luna；en_display，D4）；单说 OpenAI 是公司名。日期：2026 年 10 月 20 日（October 20, 2026）。哈希和 ID 绝不念出来。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 逐句对齐（explainer/i18n.py）。narration/*.yaml 里，script.md 的每个 SAY 行都有一条（155 段）；`en` 和 SAY 行逐字节相同；`zh` 的条数和 explainer.voice.split_sentences 切出的英文句子数完全一样（这份稿子 339 句）。只在句子内部调整结构；绝不合并或拆开句子。短句单独成条：Pause here. → 在这里暂停。；Seven survive. → 七种留了下来。；Type approve. → 输入 approve。；What did you approve? → 你批准的到底是什么？；The manager approves. → 经理批准了。；A capsule. → 一个胶囊。；No. → 不会。；No handoffs. → 没有交接。；Step 1: act 4. → 第 1 步：第 4 幕。；Test yourself. → 自测一下。；Changed configuration: prompt. → 改动的配置：prompt。；Confounding changes: none. → 混杂改动：没有。。运行 `python -m explainer.i18n check videos/ac215-l07-agent-harness --lang zh`，直到它打印 OK。
- **[D2]** 不写 say:，不写 anchors。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（锚点只在中文配音渲染时用来对齐动画）。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：不用括号（B2），不用数学符号（B3），不出现 letter_letter 的名字（A6），数字后面不跟 !，分句不能以“种”结尾再接 ，。！？（Seven survive. → 七种留了下来。，不写“剩下七种。”；This tutorial uses two → 用了其中两个，不写“两种。”；十二种奶酪、五种状态、两种模式、哪一种状态都没问题），汉字和拉丁字母或数字之间有半角空格（B1），每句以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），而且每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器按 [A-Za-z][A-Za-z'.-]* 切词，忽略单个字母：gpt-5.6-luna 切成 gpt- 和 luna，SHA-256 是 SHA-，AC215 是 AC，context-fixture-1 是 context-fixture-，act2-context-live-1 是 act 和 context-live-，Comté 是 Comt，Époisses 是 poisses，Bûcheron 是 cheron，docker-shell.sh 整个一个词，approval.requested 整个一个词，--compare 是 compare，Python 3.13.16 是 Python。检查器报出来的拉丁词，要么是该翻译的英文词（通常如此），要么是漏收的实物：把实物按同样的切法加进 allowed_spoken_latin 和它的词条。复数故意不收（traces、skills、labels、fixtures、tokens、tests、calls、runs 都没有）：报出复数，说明是该去掉的英文词形变化（所有 trace、两个 skill、新的 label、281 个测试）。
- **[D4]** 英文行（en_display）。双语字幕带显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都要在 en_display 里给出屏幕上的字面形式，其余照 SAY 逐字写；同一段里的其他句子写 null。念法 → 字面（script.md 开头的清单、review_spoken 第 11 条，加上这份词表补充的）：python cli.py, dash dash act 1, dash dash scenario standard → python cli.py --act 1 --scenario standard；python cli.py, dash dash help → python cli.py --help；dash dash compare → --compare；dash dash show JSON → --show-json；dash dash preview context → --preview-context；dash dash prompt file → --prompt-file；dash dash fixture → --fixture；dash dash rm → --rm；Inspect run → --inspect-run；docker ps dash a → docker ps -a；Docker image remove → docker image rm；句首的 Docker ps / Docker images / Docker inspect → docker ps / docker images / docker inspect；build agent → build_agent；preview order → preview_order；order placed set to false → "order_placed" set to False；get catalog → get_catalog；get stock → get_stock；load skill → load_skill；read skill resource → read_skill_resource；start order, get order status, assess event → start_order, get_order_status, assess_event；build act 4 → build_act4；Cart Check → CartCheck；harness without trace → harness.without("trace")；the add and without methods → the .add() and .without() methods；basic Context → Context("basic")；approval mode always require → approval_mode="always_require"；no cart → no_cart；maximum of 8 model calls reached → Maximum of 8 model calls reached；requested tools / tool call → Requested tools / Tool call；inspect the context first → Inspect the context first；the missing details scenario → the missing-details scenario；tasting planning and vendor outreach → tasting-planning and vendor-outreach；context fixture 1 → context-fixture-1；status saved, email transmitted no → status: saved, email transmitted: no；with status error → with status: error；approval requested, approval decided, policy decision allow, order placed, run finished → approval.requested, approval.decided, policy.decision allow, order.placed, run.finished（S14[4]）；model failed → model.failed；OpenAI API key（S03[5] 里 secret 的名字）→ OPENAI_API_KEY；GPT 5.6 Luna → gpt-5.6-luna；agent framework 1.19.0 → agent-framework 1.19.0；金额：150 dollar budget → $150 budget，64 dollars → $64，220 dollars 80 → $220.80，50 dollars 10 → $50.10，200 dollar threshold → $200 threshold。带下划线的名字（A6）只在 en_display 里恢复字面形式；中文行保留空格形式。SKILL.md 照写；docker exec 照输入的写。英文版自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它自己的英文句子：不添加命令、参数、括注、中文界面名或解释；只有英文说 extra 的地方才写“额外”；保留英文的词不加中文解释（英文行就在下面）；思考题不给答案（A9）。A5 需要的几个开头词（这个、先看、再看、用、命令行里的）不带内容。the prompt file 写“prompt 文件”，不加 shop_assistant.md；the vendor skill 写“供应商那个 skill”，不加 vendor-outreach。
- **[D6]** 固定说法。Pause and run it. → 暂停一下，跑一遍。Pause here. → 在这里暂停。Pause and run both, with your key. → 暂停一下，用你的密钥把两条都跑一遍。Pause, run steps 2 and 3, and wait for this prompt. → 暂停一下，跑第 2、3 步，等到出现这个提示符。Pause, and verify your setup either way. → 暂停一下，两条路任选一条，把你的环境验证一遍。Pause here if you have a key. → 有密钥的话就在这里暂停。Pause and run steps 8 and 9. → 暂停一下，跑第 8、9 步。Pause and run steps 1 to 3. → 暂停一下，把第 1 到第 3 步跑一遍。Pause and run steps 4 and 5; the cell is for Colab. → 暂停一下，跑第 4、5 步；单元格是给 Colab 用的。Pause and run step 1. → 暂停一下，跑第 1 步。Pause and run steps 2 to 4. → 暂停一下，把第 2 到第 4 步跑一遍。Pause and run evaluation steps 1 and 2. → 暂停一下，跑评测第 1、2 步。Pause and run evaluation step 3. → 暂停一下，跑评测第 3 步。Pause, and tear down. → 暂停一下，把它拆掉。Pause and try them; answers are in the exercises. → 暂停一下，试着答一答；答案在练习里。When a tag says your turn, pause and run the command. → 看到标签写着 your turn，就暂停，自己跑这条命令。With a key, look for … → 有密钥的话，要找的是……；Without a key, … → 没有密钥的话，……；As an extra, … → 额外再跑一个：…… / 再额外……；Three extras from a second terminal. → 在第二个终端里做三个额外检查。an extra check reads the file → 额外检查会读取这个文件；Step N: → 第 N 步：；Steps 2 and 3 are … → 第 2、3 步是……；Evaluation step N … → 评测第 N 步……；at the time of recording → 录制时。A small slip … → 一个小疏漏……（A9）。Something to ponder. → 来想一个问题。Yes, and yes. → 是，也是。Here's what a key gets you, from the staff's saved run. → 下面是有密钥时的样子，来自课程团队保存的运行。Test yourself. → 自测一下。In part 2, … → 第二部分，……；Part 2 picks up at the container prompt → 第二部分从 container 的提示符接着来。
- **[D7]** 文件。narration/g1.yaml = S01–S07（第一部分：一个 agent：准备、循环、它的层和它的上下文；68 段、148 句），narration/g2.yaml = S08–S16（第二部分：harness 接管；87 段、191 句），对应 video.yaml 的两个部分；每个文件开头写一段注释（覆盖范围；用到的规则：A6 空格形式、B3 符号用文字、C1 数字不加分隔符、C2 金额、版本和模型 ID、D4 en_display、不写 say: / anchors:），并保持稿子的顺序。用双引号字符串；YAML 里的双引号和反斜杠要转义。
- **[D8]** 按英文时间轴的长度。中文在英文播放时被阅读；字幕带在英文字幕切换的地方切换（读速超过每秒 9 个单位的中文片段最多多给 1 秒）。每句中文的阅读时间要和英文听起来的时间差不多：每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以去掉多余的连接词和重复的主语，但绝不删内容。长的实物也占长度（python cli.py --act 1 --scenario standard 22.6 个单位，approval mode 设为 always require 18.0，Maximum of 8 model calls reached 17.6，read skill resource 10.5，Invalid or unauthorized 12.7）：英文没重复的地方不要重复；同一段里第一次之后用简短的指代（这条命令、这个工具、这个 skill、这一批、这个场景）。
- **[D9]** 保持英文的分句顺序（系列教训，ac215-video skill）。工具链按分句把中文和英文配对，中文句子如果把条件放在前面（如果……，就……），两个相邻字幕块的意思就会对调。条件、目的和时间状语放在英文放的位置：英文条件在前，中文也在前（If that's you, shell in … → 如果是这种情况，就……；When a tag says your turn, pause … → 看到标签写着 your turn，就暂停……；Before every call, the harness … → 每次调用之前，harness ……）；英文主句在前，中文也把主句放前面，或者把条件放进同一个分句、主动词前不加逗号（Move right when stakes are high … → 风险高或操作无法撤销时就往右移；Drafting is refused until the email template is read → 起草一直会被拒绝，直到读过邮件模板为止；Pause here if you have a key → 有密钥的话就在这里暂停）。review_spoken 第 9 条点名的三句：S05[0] 让“循环”留在第一个分句（如果你写过一个循环，它调用模型并执行工具调用，那你就是 harness 工程师）；S09[2] 让“哈希”放在清单前面（一个指纹：SHA-256 哈希，覆盖需求、商品明细……）；S06[2] 先说口味再说内容（……保存的口味：温和的奶酪和无酒精搭配）。S14[4] 的事件清单保持英文顺序（approval.requested，带着指纹；approval.decided，由人决定；……）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一个字幕块 2 行。分句最好不超过大约 24 个单位，用 ，；： 隔开，让切分器有干净的切点；避免超过 30 个单位、中间没有标点的分句（python cli.py --act 1 --scenario standard 本身就有 22.6 个单位：给它单独一个分句）。
- **[G2]** 字幕块结尾：工具链会去掉字幕块末尾的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。句末用中文词比用“实物 + 句号”更稳（……进入 agent-harness 目录。比 ……进入 agent-harness。读起来稳；两种都合法）。
- **[G3]** 绝不拆开命令。切分器把中文行里两个拉丁词之间的空格当作好的切点，所以 python cli.py --help 可能被拆到两行，观众就没法照抄了。把整条命令放在分句末尾、全角冒号后面（第 3 步：bash docker-shell.sh，……；第 1 步：python cli.py --act 1 --scenario standard。；……最后一条是：python cli.py --help，……），一个字幕块最多一条命令，周围少放中文。单独说的参数（--compare、--show-json、--fixture、--rm）很短，放哪里都行。太长、一行放不下的命令，按 SAY 的叫法说（act 3, scenario standard → 第 3 幕，standard 场景），由终端和英文行显示完整命令。在渲染出来的 .zh.srt 里检查每个带命令的字幕块。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、部分和章节标题用书面语体（A4：容器、端口、智能体、技能、评测）；问句保留问号；保留英文的冒号结构（第 1 幕：……；评测：……）；命令、文件名和代码名照写（meta.yaml 不经过检查器，所以那里可以用括号和下划线）。核心概念的章节带英文短名，方便搜索，和第 1、3、5、6 讲一样：智能体（agent）、技能（skill）。LLM: Agents II → LLM 智能体 II（同第 6 讲的“智能体 I”）；Act n → 第 n 幕；比喻保留画面：sieves and lanes → 筛选与两条通道（review_spoken 第 17 条），rails, not suggestions → 是轨道，不是建议，manuals, not keys → 是说明书，不是钥匙，five drawers → 五个抽屉，the capsule → 胶囊；the harness takes control → harness 接管；harness 保留英文。
- **[H2]** 简介（B 站 / YouTube）：两三句话，书面语体，用这份词表的词：AC215 第 7 讲，跟练 dlops-io/agent-harness 和课程的 Agent Harness Colab notebook；观众做什么、学到什么（在一个不开端口的容器里完成准备和 281 个离线测试；“模型提议，harness 决定”这条主线；用真实数字拆开第 1 幕的循环和它的四个 harness 层；第 2 幕的上下文包；第 3 幕由 Python 掌控的工作流图、绑定指纹的经理审批和结账时的重新校验；第 4 幕的压缩、状态胶囊和只由宿主程序写入的记忆；第 5 幕技能的渐进式披露；第 6 幕调用受管控工作流的智能体；用 trace、fixture 批量评测和只改一处的 A/B 对比 --compare 拿出评测证据）；英文旁白，配中文和中英双语字幕；终端输出录于 2026-10-20，录制时没有 OpenAI 密钥，所以离线和脚本模拟的命令是真实运行，在线命令停在 401，模型的回答来自课程团队保存的 Colab 运行。绝不出现顾客的 ID 或名字。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md / digest.md）用这份词表、按书面语体翻译（A4：仓库、克隆、提交、容器、镜像、端口、提示词、智能体（agent）、会话（session）、Colab 笔记本（notebook）、技能（skill）、执行记录（trace）、测试夹具（fixture）、行动边界、上下文工程、上下文窗口、压缩、胶囊、渐进式披露、白名单、评测集）；harness 保留英文，首次出现时解释一次：harness（模型外面那层由代码执行的循环、限制、上下文和检查）。那里可以用括号和下划线（不经过检查器）。标题和 `<summary>答案</summary>` 要翻译。最后附一张术语对照表：英文 | 这里的说法 | 其他常见译法（harness：外壳 / 驾驭框架；trace：链路追踪 / 轨迹记录；skill：技能；fixture：测试夹具 / 固定装置；compaction：压缩 / 上下文压缩；progressive disclosure：渐进式披露 / 逐步披露；allowlist：白名单 / 允许列表；eval set：评测集 / 评估集；LLM as judge：LLM 评委 / LLM 裁判；handoff：交接 / 移交；token：词元 / 令牌）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 都不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读文本的检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）。对只有字幕的视频（这个系列；video.yaml 里没有 languages.zh.voice，词表里 voice: none）这些检查保护不了什么，反而逼出 A6 和 B3（这里是 build_agent、preview_order、get_catalog、get_stock、load_skill、read_skill_resource、start_order、get_order_status、assess_event、build_act4、order_placed、no_cart、approval_mode="always_require"、OPENAI_API_KEY、RUN_ID、harness.without("trace")、Context("basic")）。建议：词表的 voice 为 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。那时 A6 和 B3 就变成：照抄字面形式。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当作好的切点，所以命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
- **[I3]**（说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：每个词条 en 字段里 2–3 个词的英文说法会被保持在同一行英文里，zh_subtitle 里 2–7 个汉字的中心词会注册进 jieba，对所有视频的字幕都生效。所以这份文件的 en 和 zh_subtitle 两栏只列真正的术语（不放句子）；别的视频以后重新拼接时也会用到它们。
