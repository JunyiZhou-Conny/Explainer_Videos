# AC215 第 6 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 6 — LLM: Agents I (follow-along: llm-rag, llm-agent-google-adk)*（`videos/ac215-l06-agents-1`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python（async / await 能读懂），用过聊天助手；做过第 1 讲（uv、pyproject.toml、uv.lock）、第 2–4 讲（container、docker-shell.sh、挂载进去的服务账号密钥）和第 5 讲（llm-rag 的 RAG pipeline 和它的 ChromaDB collection）；从没给 LLM 写过工具，没用过 agent 框架，没听说过 MCP；开着自己的 `~/AC215/llm-rag`（第 5 讲的 collection 还在磁盘上）、一份新 clone 的 dlops-io/llm-agent-google-adk 和一份 Cheese Quiz 的 Colab 副本，边看边敲命令
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l06-agents-1.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5，“点 venv”“杠 m”“三点十一点二”这类读法、数字和符号怎么念）都不适用，只保留显示规则
英文原稿：`script.md` v2（SAY 行是旁白：153 段、337 句；第一部分 S01–S08 是 78 段、172 句，第二部分 S09–S16 是 75 段、165 句）；`build/review_spoken.md` 第 7 条（逐句翻译会误读的说法：mode any 里的 any 是值，不是“任何”；State 标签页里的 entries 是“项”，不是密钥）和第 12 条（en_display 清单）已并入；script.md 开头的 en_display 候选清单照用（D4）
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词（repo、clone、commit、pin、lock 文件、import、解析、及以上、wheel）；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md)、[`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md)、[`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md) 定下容器、密钥、网络的词（token、Ctrl-C、关卡）和“只有字幕”的整套规则；[`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md) 定下 RAG 的词（chunk、embedding、collection、向量化、索引、替身、通道、一个小疏漏）。前五讲已经定下的词一律沿用；新的是 agent 的词汇（函数声明、函数调用、函数响应、循环、Runner、session、MCP、harness，A3）
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“这个 agent 跑了一圈”“建一个 session”“跑一下这个 notebook”“temperature 调成 0”“enum 里只有 9 个名字”“装一个 MCP server”“token 用了多少”“把版本 pin 住”。在实验课上硬说“智能体”“会话”“笔记本”“温度”“枚举”“模型上下文协议服务器”“词元”，反而像说明书；这些书面词留给标题、章节名和配套文档（A4）。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、代码、Colab 和 ADK 的网页界面里找东西。命令、参数、文件名、路径、包名、模型 ID、代码里的名字、报错原文、界面上的按钮一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（工具、函数调用、函数声明、函数响应、分发器、循环、状态、事件、记忆、指令、规划器、编排、工作流、框架、协议、服务器、护栏、审批、迭代、上下文工程）一律说中文；用 Google Gemini 中文文档、OpenAI 和 ADK 中文资料、MCP 中文资料里的标准译名，方便搜索。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、Colab 和 ADK 的示意界面、标签、进度条和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“pull 下来”“把 repo clone 下来”“写 prompt”“调 embedding 模型”“建一个 collection”，这一讲再加上“这个 agent”“建一个 session”“跑一下 notebook”“temperature 调成 0”“enum 里的值”“JSON schema”“MCP server”“thought signature”。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（Google Gemini 中文文档、OpenAI 和 ADK 中文资料、MCP 中文资料：函数调用、函数声明、函数响应、思考模型、模型上下文协议、上下文工程、护栏）；和整个系列一致（第 1 讲定下共用的词，第 2–4 讲定下容器、密钥和网络的词，第 5 讲定下 RAG 的词）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、包名、模型 ID、代码里的名字和值、终端原文和报错名、Colab 和 ADK 界面上的字样、画面上的标签、README 的章节标题、模型写出的搜索文本）逐字照抄，不翻译、不变形、不加引号。检查器逼出来的例外：带下划线的名字，以及 = + < > ( ) [ ] 这几个字符，按旁白的说法写（A6、B3）。终端输出、代码面板、README 卡片、示意界面、标签、进度条、课件标签和思考题卡片都是英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 repo、clone、commit、pin、lock 文件、import；第 2–4 讲的 container、image、pull、pipeline、port、localhost、API、ID、token；第 5 讲的 chunk、embedding、collection、prompt、system prompt、LLM、agent；这一讲新增 notebook、session、schema（JSON schema）、enum、temperature、system instruction、thought signature、SDK、MCP 里的 host / client / server、harness、wheel、dev UI。
3. **其余一律用中文标准术语**：工具、工具调用、函数调用、函数声明、函数响应、参数、字段、必填、描述、分发器、结果、请求、回复、最终回复、循环、停止规则、上限、迭代、轮、事件、状态、记忆、指令、组件、动态控制、决策者、规划器、编排、工作流、框架、推理引擎、推理工作流、推理模型、思考模型、协议、模型上下文协议、定制集成、子进程、标准输入输出、工具集、过滤器、服务器、web 服务器、浏览器、重定向、标识符、遥测、占位符、单元格、运行时、护栏、成功标准、审批、批准、回执、上下文工程、深度研究、交接、校验器、总结器、分类器、处理函数、结构化输出、解析、包、虚拟环境。
4. **视频的比喻按意思译，一个比喻一个词**：方向盘（steering wheel）、通道（lane，沿用第 5 讲）、信封和纸（envelope、sheets）、菜单和点单（menu、order）、封印（seal）、替身（stand-in，第 5 讲）、轮毂和辐条（hub、spokes）、白板和格子（whiteboard、cells）、插头（plug）、流水线（assembly line）、关卡和印章（gate、stamp）、回执（receipt）、便条（note）、舞台和边界（stage、boundary）。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、仓库、克隆、提交、端口、提示词、系统提示词、嵌入向量、集合（collection）、智能体（agent）、会话（session）、Colab 笔记本（notebook）、MCP 服务器（MCP server）；harness 书面也保留英文。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **工具链的约束也是规则**：每个英文句子对应一个中文句子（153 段、337 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **agent 照说，书面写“智能体（agent）”**（A3、A4）。第 5 讲已经把 agent 放进口语清单，这一讲它是主角（47 次）：这个 agent、agent 函数、LLM agent、顺序 agent、并行 agent、编排 agent、专家 agent、主 agent。句子不以 agent 开头（A5）。
- **函数调用的三件套说中文，用 Google 中文文档的译名**：function declaration → 函数声明，function call → 函数调用，function response → 函数响应，dispatcher → 分发器；call 1 / call 2 → 第 1 次调用 / 第 2 次调用（画面上的 call 1 → your code → call 2 条保持英文）。参数结构里的关键字照说：JSON schema、schema、enum、enum 值 ANY；required → 必填。
- **代码里的设置照说，值照写**：temperature（temperature 设为 0）、tool config（tool_config）、mode 设为 any / mode 为 ANY、system instruction、thought signature、output key、response.text。any 是 mode 的值，绝不译成“任何”（review_spoken 第 7.2 条）。
- **ADK 的运行时对象**：Runner 照写，session 照说（书面“会话（session）”），state → 状态（State 标签页照写），events → 事件，root agent 照说（root_agent）；validator / planner / summarizer → 校验器 / 规划器 / 总结器（按作用称呼，画面上是 ItineraryValidator、TravelPlanner、TripSummarizer）。
- **MCP 的三个角色照说**：MCP server、host、client（中国工程师就这么说：“装一个 MCP server”）；Model Context Protocol → 模型上下文协议。MCP 以外的 server 说中文：web 服务器、服务器日志、停掉服务器（A7）。
- **notebook 照说，因为“笔记本”已经是 laptop**（第 1 讲）：跑一下这个 notebook、notebook 里的单元格；书面写“Colab 笔记本（notebook）”。cell → 单元格（Colab 中文界面），白板上的 cell → 格子（A7）；runtime → 运行时。
- **harness 保留英文**：中文还没有通行译名，下一讲（dlops-io/agent-harness）就以它为题；字幕和标题都写 harness，配套材料首次出现时解释一次（H3）。它的零件说中文：审批关卡、待批准 / 已批准、印章、护栏、成功标准、回执。
- **token 照说**（第 4 讲：LLM 的 token；密钥是 key，访问令牌是 access token）；**key → 密钥**，只有 GOOGLE_API_KEY 这个变量按 SAY 写成 Google API key，以及终端原文 API key not valid。
- **模型 ID 照代码写**（第 5 讲 C2）：gpt-4o、gemini-2.5-flash、gemini-3.1-flash-lite、gemini-2.0-flash，中英两行一致（英文行用 en_display，D4）。单说 Gemini、OpenAI 的模型照写产品名。
- **带下划线的名字和检查器不收的符号**（A6、B3，同第 3–5 讲）：get_book_by_author → get book by author 这个函数；search_content → 搜索文本；tool_config → tool config；mode="any" → mode 设为 any；output_key → output key；mcp_servers → MCP servers 参数；tool_filter → 过滤器；needs_confirmation / apply_confirmation / send_email → needs confirmation / apply confirmation / send email；finalize_itinerary → finalize；GCP_PROJECT → GCP project 变量；GOOGLE_API_KEY= → Google API key 的等号后面；--chunk_type char-split → chunk type 用 char-split；Ctrl+C → Ctrl-C；LLM plus reasoning → LLM 加上推理。英文行用 en_display 给出字面形式（D4）。
- **课上的词跟着课件走**（SLIDES.md）：LLM core → LLM 核心，instructions → 指令，tools → 工具，memory → 记忆（绝不写“内存”），dynamic control → 动态控制，blocks → 组件（不是“模块”：模块是 ADK 的模块目录），decision maker → 决策者，reasoning engine → 推理引擎，Agentic RAG / Self-RAG / Corrective RAG 照写，data / action / orchestration tools → 数据工具 / 行动工具 / 编排工具，handoffs → 交接，deep research → 深度研究，success criteria → 成功标准，guardrails → 护栏，context engineering → 上下文工程。
- **一个意思一个词，分清同形词**（A7）：order 是“点单”（菜单的比喻）还是“顺序”（谁来定顺序）；planner 是“规划器”（课上的节点、baseline 的 agent）还是“课上的旅行规划”（S11[5]）；cell 是“单元格”还是“格子”；catalog 是“清单”，不是“目录”；receipt 是“回执”，不是第 1 讲的“小票”；gate 是“关卡”。
- **勘误统一说“一个小疏漏”**（第 5 讲 A9），后面一定紧跟改法：A small slip / One small slip / Two more slips / a file name slip → 一个小疏漏 / 一个小疏漏 / 还有两个小疏漏 / 文件名的小疏漏。
- **录制时**：at the time of recording 每次都译“录制时”，绝不省略（Python 3.12.15、uv 0.13.1、CPython 3.15.0、ADK 2.12.0、Cheese Agent Tool 还在线）。我们录制时没有任何密钥：凡是调用模型的地方，字幕说“有密钥的话，要找的是……”；模型的回答是“课程团队保存的输出”（A9、D6）。
- **名字**（A10）：授课老师绝不提名字（画面上是 ‹instructor›）；书里的作者从不出现；书用书名或描述（那本茅屋奶酪食谱、Woman's Institute 那本书）；Mara、Anja 照写；两个贯穿全片的问题和 README 的描述是旁白的话，要翻译；地名写中文（巴黎、加州）。
- **系列清单里这一讲没说到的词**（A13）：Dockerfile、PATH、endpoint、LoRA、CI、push 都没出现；volume 只出现在目录名 docker-volumes 里。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）：每句中文读起来的时间要和英文听起来差不多；条件和主句的先后跟着英文走，条件放在分句里面时，主动词之前不加逗号（这一步只要 uv 选中 3.15 就会失败，不写成“只要 uv 选中 3.15，这一步就会失败”）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令和子命令（cd llm-rag、sh docker-shell.sh、python cli.py --agent、python cli.py --load、--get、docker ps、docker compose down、exit、git clone、cd google-adk-tutorial、cd llm-agent-google-adk、ls、grep、curl、uv sync、uv python pin 3.13、uv run adk web、uv run adk --version、adk telemetry disable、--port 8080、git status、npx、Ctrl-C）、文件名、目录名和路径（cli.py、docker-shell.sh、.env、.env.example、.adk、docker-volumes、secrets、llm-rag、llm-agent-google-adk、google-adk-tutorial、1-baseline、baseline、baseline.agent）、包名（onnxruntime、sentence-transformers）、代码里的名字和值（enum、ANY、any、user、system、response、response.text、finalize、yes、USERS、clarification，以及 A6 的空格形式：get book by author、tool config、output key、MCP servers、tools、needs confirmation、apply confirmation、send email、root agent、GCP project、Google API key）、模型 ID（gpt-4o、gemini-2.5-flash、gemini-3.1-flash-lite、gemini-2.0-flash）、终端原文和报错（DefaultCredentialsError、Internal Server Error、API key not valid、address already in use、406）、模型写出的搜索文本（cheese making importance location）、界面字样（Save a copy in Drive、Secrets、Notebook access、State、dev UI）、README 标题（Agents、Running Agents）、旁白提到的画面标签（your turn）。完整清单见 A1（a）；带下划线的名字和检查器不收的符号例外（A6、B3）。
- 产品、组织、课程和名字：AC215、MLOps Learning、Google、Google AI Studio、Gemini、OpenAI、Microsoft、Agent Framework、Agents SDK、SDK、Agent Development Kit、ADK、Runner、Colab、Drive、Docker、Compose、Chroma、Python、CPython、uv、Node、npx、FastMCP、MCP、PyTorch、CUDA、Linux、Chrome、JSON、HTML、URL、RAG、Agentic RAG、Self-RAG、Corrective RAG、Cheese Quiz、Cheese Quiz Guild、Guild、Travel Planner、Cheese Agent Tool、Whole Foods、Woman's Institute、Mara、Anja、student（A1 b）。
- 实验课口语，封闭清单：repo、clone、commit、pin、lock 文件、import（第 1 讲）；container、image、pull、pipeline、port、localhost、API、ID、token（第 2–4 讲）；chunk、embedding、collection、prompt、system prompt、LLM、agent（第 5 讲）；**notebook、session、schema、JSON schema、enum、temperature、system instruction、thought signature、SDK、MCP server、host、client、harness、wheel、dev UI（这一讲新增）**。
- 系列清单里保留英文、但这一讲没说到的：Dockerfile、PATH、endpoint、LoRA、CI、push；volume 只作为目录名 docker-volumes 出现（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| agent / an agent / LLM agents | agent / LLM agent | the agent loop | agent 循环 |
| LLM core / instructions / tools / memory | LLM 核心 / 指令 / 工具 / 记忆 | dynamic control / building blocks | 动态控制 / 组件 |
| steering wheel / decision maker | 方向盘 / 决策者 | hub / spokes / planner | 轮毂 / 辐条 / 规划器 |
| base LLM / reasoning LLM | 基础 LLM / 推理 LLM | reasoning engine / workflow / model | 推理引擎 / 推理工作流 / 推理模型 |
| lane (Lane 1) | 通道（第 1 条通道） | live systems / autonomy | 实时系统 / 自主性 |
| envelope / sheets | 信封 / 纸 | stateless functions | 无状态的函数 |
| role (user / system) | 角色（user / system） | output schema / strict JSON | 输出 schema / 严格的 JSON |
| menu / menu item / order | 菜单 / 菜单项 / 点单 | function declaration | 函数声明 |
| function call / tool call | 函数调用 / 工具调用 | function response | 函数响应 |
| call 1 / call 2 | 第 1 次调用 / 第 2 次调用 | dispatcher | 分发器 |
| parameters / arguments / fields | 参数 / 字段 | required / description | 必填 / 描述 |
| the search text | 搜索文本 | the real function | 真正的函数 |
| temperature / tool config | temperature / tool config | mode any / mode ANY | mode 设为 any / mode 为 ANY |
| thought signature / thinking models | thought signature / 思考模型 | seal / unchanged | 封印 / 原封不动 |
| turn / the model's own turn | 轮 / 模型自己的那一轮 | stand-in | 替身 |
| loop / one lap | 循环 / 一圈 | stop rule / final response | 停止规则 / 最终回复 |
| cap / turns / iterations | 上限 / 轮 / 迭代 | events / streams events | 事件 / 以流的形式输出事件 |
| framework / the library / wrapper | 框架 / 库 / 包装函数 | Runner / session / state | Runner / session / 状态 |
| whiteboard / cells | 白板 / 格子 | output key / placeholder | output key / 占位符 |
| sequential / parallel agent | 顺序 agent / 并行 agent | validator / planner / summarizer | 校验器 / 规划器 / 总结器 |
| module folders | 模块目录 | lock file / resolve / wheel | lock 文件 / 解析 / wheel |
| or newer / upper bound | 及以上 / 上限 | pin / pinned / unpinned | pin / pin 了版本 / 没有 pin 版本 |
| web server / server log | web 服务器 / 服务器日志 | redirect / dev UI | 重定向 / dev UI |
| telemetry / usage data | 遥测 / 使用数据 | identifier / app name | 标识符 / app 名 |
| Model Context Protocol | 模型上下文协议 | host / client / MCP server | host / client / MCP server |
| custom integration / plug | 定制集成 / 插头 | child process / standard input and output | 子进程 / 标准输入输出 |
| toolset / filter | 工具集 / 过滤器 | data / action / orchestration tools | 数据工具 / 行动工具 / 编排工具 |
| orchestrator / specialist | 编排 agent / 专家 agent | handoffs / agents as tools | 交接 / 把 agent 当工具用 |
| deep research / lead agent | 深度研究 / 主 agent | assembly line | 流水线 |
| classifier / label / handler | 分类器 / 标签 / 处理函数 | structured output | 结构化输出 |
| harness / outer layer | harness / 外层 | context engineering | 上下文工程 |
| gate / stamp | 关卡 / 印章 | pending / approved / approval | 待批准 / 已批准 / 批准 |
| guardrail (hard / soft) | 护栏（硬 / 软） | success criteria | 成功标准 |
| receipt / claim | 回执 / 声称 | a note is not a check | 便条不等于检查 |
| mock catalog | 模拟清单 | newsletter / reader | 简报 / 读者 |
| notebook / cell / runtime | notebook / 单元格 / 运行时 | Secrets panel | Secrets 面板 |
| key / the AI Studio key | 密钥 / AI Studio 的密钥 | placeholder (key, value) | 占位密钥 / 占位值 |
| the staff / saved run / saved outputs | 课程团队 / 保存的运行 / 保存的输出 | the instructor / the lecture / slides | 授课老师 / 课上 / 课件 |
| a small slip / two more slips | 一个小疏漏 / 还有两个小疏漏 | at the time of recording | 录制时 |
| an extra check | 额外检查 | tear down | 拆掉 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的一个中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 课上的框架：agent 是什么 / The lecture's frame: what an agent is

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| agent / agents / an agent / the agent / the agent function / LLM agents / AI agent | agent / agent 函数 / LLM agent / 智能体（书面） | S02[6]：课上对 agent 的定义是：一个 LLM，给它指令和工具，它自己运行，直到任务完成。 | A3：系列清单保留英文（第 5 讲 A13 预告过）；量词“个”；不放句首：这个 agent……、而 llm-rag 的 agent……（A5）。书面写“智能体（agent）”。LLM agents（ADK 的 LlmAgent）→ LLM agent；the agent function → agent 函数。 |
| LLM / LLMs / the model / base LLM / reasoning LLM / LLM core / the core / the same model | LLM / 模型 / 基础 LLM / 推理 LLM / LLM 核心 / 核心 | S02[2]：第 1 条通道，基础 LLM：调用 gpt-4o 一次，一个回答，不到 3 秒。 | LLM 照写（A1 c，可以开头，A5）。LLMs are stateless functions → LLM 是无状态的函数（不加复数）。课件的 LLM core → LLM 核心；the core → 核心。 |
| reasoning engine / reasoning workflow / reasoning model / multi-call system / orders the calls | 推理引擎 / 推理工作流 / 推理模型 | S02[4]：这里由你的 Python 安排调用顺序，所以它是推理工作流，不是推理模型。 | 课件 16–18。The lecture calls a multi-call system like this a reasoning engine → 课上把这种多次调用的系统叫作推理引擎。 |
| its five blocks / building blocks / instructions / tools / memory / dynamic control / anatomy / gray out dynamic control | 组件 / 指令 / 工具 / 记忆 / 动态控制 / 结构图 | S02[6]：它的五个组件里，有一个决定下一步：动态控制，也就是方向盘。 | 课件 27–41。block → 组件，绝不写“模块”（那是 ADK 的模块目录，A7）；the lecture's anatomy → 课上的 agent 结构图；gray out → 标成灰色。memory → 记忆，绝不写“内存”。In the lecture's blocks → 对应课上的组件。 |
| steering wheel / who steers / who holds the steering wheel / decides the next step | 方向盘 | S02[7]：变的是谁掌方向盘，还有工具。 | V1 里动态控制的比喻，一个词：方向盘。 |
| lane / the three lanes / Lane 1 / Lane 2 / Lane 3 / run the three lanes | 通道 | S02[7]：所以 agent 并不是更聪明的模型：三条通道用的是同一个模型。 | 系列沿用第 5 讲的 lane → 通道（量词“条”）；Lane 1 → 第 1 条通道（C1）。绝不写“车道”“赛道”。 |
| decision maker / hub / spokes / planner / the spoke to the tools / unroll | 决策者 / 轮毂 / 辐条 / 规划器 | S08[3]：把通向工具的那根辐条展开，就成了一个循环。 | 课件 41 的图，我们的比喻（review_spoken 第 7.1 条：spoke 是名词）。课上的 planner 节点 → 规划器；S11[5] 的 the lecture's planner 指课上的旅行规划例子 → 课上的旅行规划（A7）。 |
| live systems / tools that act / the autonomy to decide / act / neither can act | 实时系统 / 自主性 / 行动 | S01[3]：缺的是：实时系统、能行动的工具，以及自主决定的能力。 | 课件 20–22。 |
| plan five days in Paris / replan / it rains / a flight is late / the lecture's trip / a bigger version | 巴黎 / 重新规划 / 航班延误 / 旅行 | S01[2]：课上问的是一个更大的版本：规划在巴黎的五天，并且在下雨或航班延误时重新规划。 | 地名写中文（巴黎、加州）。条件留在分句里面，主动词之前不加逗号（D9）。rehearses the lecture's trip → 演练的就是课上那趟旅行。 |
| RAG / a straight line / retrieval / the lecture's recap / steps around the search / whether to retrieve / grading / rewriting / web search | RAG / 检索 / 评分 / 改写 / 网页搜索 | S04[0]：课上的回顾让检索更聪明：搜索前后的步骤、到底要不要检索、评分、改写，还有网页搜索。 | 第 5 讲的词（检索、改写）。steps around the search → 搜索前后的步骤（第 5 讲的检索前 / 检索后）。grade their retrieval → 给检索结果打分。 |
| agentic RAG / Agentic RAG / Self-RAG / Corrective RAG / puts a model in front of that menu | Agentic RAG / Self-RAG / Corrective RAG | S04[1]：Agentic RAG 把一个模型放在这份菜单前面，让它来选。 | 课件里的名字（课件 9–14），中国工程师也这么说；可以开头。字幕里不写“代理式 RAG”。 |
| data tools / action tools / orchestration tools / the three families / hand work to another agent | 数据工具 / 行动工具 / 编排工具 | S12[0]：课上把工具分成三类。 | 课件 51。like finalizing a trip or sending email → 比如敲定行程或者发邮件（这里是普通动词，不是工具名）。 |
| handoffs / agents as tools / lecture 7 sketches handoffs | 交接 | S13[7]：这些教程是把 agent 当工具用；第 7 讲会简单讲讲交接。 | 说中文（OpenAI Agents SDK 的中文资料译作“交接”）；字幕里不写 handoff。 |
| deep research / tree of agents / lead agent / parallel web searchers / synthesis / report | 深度研究 / 主 agent / 汇总 / 报告 | S13[0]：教程搭了类似的树：Cheese Quiz Guild，还有简报。 | 课件 44–49。a lead agent, a planner, parallel web searchers, and a synthesis into a report → 一个主 agent、一个规划器、几个并行的网页搜索 agent，最后汇总成一份报告。 |
| success criteria / guardrails / hard guardrail / soft guardrail | 成功标准 / 护栏 / 硬护栏 / 软护栏 | S14[7]：课上把成功标准放在指令里，把护栏放在决策者里。 | 课件 36–37。 |
| context engineering / the craft / next lecture names the craft | 上下文工程 | S03[4]：下节课会给这门手艺起个名字：上下文工程。 | 标准中文。 |
| harness / the harness / outer layer / the harness itself / a harness run | harness / 外层 | S15[5]：下节课把这个外层叫作 harness。 | A3：保留英文：中文还没有通行的译名，而且它是第 7 讲的主题（dlops-io/agent-harness）。书面也写 harness，配套材料首次出现时解释一次（H3）。小写，不放句首：现在来看 harness。 |
| framework / frameworks own the loop / the framework's loop / a framework writes it for you | 框架 | S09[0]：第二部分：循环归框架管。 | 标准中文。 |
| the lecture's formula / an LLM plus reasoning, instructions and tools / the formula gains two pieces | 公式 / 推理 | S16[4]：课上的公式，LLM 加上推理、指令和工具，多了两块：框架运行的循环，以及由你的代码强制执行的检查。 | B3：plus → 加上，绝不写 +。 |

### 信封：模型的输入 / The envelope: the model's inputs

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| envelope / a fresh envelope / sheets / paper / stateless functions / what's inside | 信封 / 纸 / 无状态 | S03[0]：每次调用都是一个全新的信封，模型只知道信封里的东西。 | V2 的比喻，各用一个词：信封、纸（these sheets → 这几页纸）。 |
| managing the model's inputs / system prompt / retrieved documents / the earlier turns / a profile from past sessions / a tool's output / output schema | system prompt / 用户画像 / 输出 schema | S03[1]：先是 system prompt、检索到的文档、之前几轮，再是以往 session 的用户画像、工具的输出和输出 schema。 | 第 5 讲：system prompt 照说；LLM 的 prompt 照说，shell 的 prompt 是“提示符”（A7）。Next section: managing the model's inputs → 下一节：管理模型的输入。 |
| memory / what memory really is / the earlier turns aren't remembered / remembers you next time | 记忆 | S03[3]：记忆，就是你放回信封里的纸。 | agent 的 memory → 记忆，绝不写“内存”。 |
| role / the role user / the role system / swap those two roles | 角色 / user / system | S03[6]：这里 system prompt 用的角色是 user，问题用的角色却是 system。 | 消息的 role → 角色；值 user、system 照写（代码里的字）。Can you spot the slip? → 你能找出这个小疏漏吗？（不提示，A9） |
| top pick / cheddar / American / mild cheeses for kids / Havarti / a mild cheddar from Whole Foods / strict JSON | 首选 / 切达 / 美式奶酪 / 哈瓦蒂 / Whole Foods | S03[2]：注意看首选的变化：切达、美式奶酪，然后是给孩子吃的温和奶酪，再然后是哈瓦蒂。 | 模型的首选：奶酪名用标准中文；商店名 Whole Foods 照写。 |
| the question / a cheese expert / what's the best cheese for a grilled cheese sandwich / describe where cheese making is important in the instructor's book | 问题 / 奶酪专家 / 烤奶酪三明治 / 奶酪制作 | S02[2]：现在 notebook 用三种方式问同一个问题，每次都用同一个模型：做烤奶酪三明治，最好用哪种奶酪？ | A10：两个贯穿全片的问题是旁白自己的话，要翻译；授课老师绝不提名字。 |

### 菜单：函数声明 / The menu: function declarations

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| menu / menu item / a menu of two / an order / call 1 returns an order | 菜单 / 菜单项 / 点单 | S04[10]：第 1 次调用返回一张点单：函数名和参数。 | V3 的比喻：函数声明是菜单，模型写出的函数调用是点单。S13 的 order（先后）是“顺序”（A7）。 |
| function declaration / declarations / a name / a description / parameter descriptions / documentation | 函数声明 / 声明 / 名字 / 描述 / 参数描述 / 文档 | S04[3]：参数以 JSON schema 的形式给出。 | Google 中文 Gemini 文档的译法：函数声明。written by hand → 手写的。 |
| JSON schema / schema / parameters / arguments / fields / required / enum / the enum value | JSON schema / schema / 参数 / 字段 / 必填 / enum / enum 值 | S04[4]：作者必须是 enum 里 9 个名字之一。 | schema、enum 照说（画面上的关键字，实验课口语）。required → 必填（两个字段都是必填的）。arguments、parameters → 参数。 |
| the search text / search term / expand the search term to a sentence or two / the author | 搜索文本 / 搜索词 / 作者 | S04[4]：搜索文本的描述甚至在指导模型：把搜索词扩展成一两句话。 | 参数 search_content 按 SAY 说“搜索文本”（A6）。引用的描述要翻译（旁白的转述）。 |
| get book by author / search one author's book / search all books / let the LLM decide how to retrieve | get book by author | S01[0]：在课程团队录下的那次运行里，回答之前先打印了这两行：一个叫 get book by author 的函数，以及它的参数。 | A6：get_book_by_author 按 SAY 写成 get book by author，带一个中文中心词（这个函数）；en_display 给出 get_book_by_author（D4）。README 的两条描述要翻译：搜一位作者的书，或者搜全部的书；让 LLM 决定怎么检索。 |
| the real function / the collection and an embedding function / your code supplies them | embedding 函数 | S04[5]：模型能控制的只有作者和搜索文本。 | 第 5 讲：collection、embedding 照说。 |
| tool-using agent / pick the right tool / format its inputs / interpret its outputs / picks and formats only by writing | 工具 / 输入格式 / 输出 | S04[6]：课上说，会用工具的 agent 必须选对工具，整理好输入格式，并解读输出。 | 课件 39（课件上写成 interest 是笔误，不照抄）。 |
| 9 names / 11 books / the cottage cheese recipe book / the Woman's Institute book / not on the list / no author at all / a file name slip | 名单 / 茅屋奶酪食谱 / Woman's Institute | S04[8]：Woman's Institute 那本书，1505 个 chunk，干脆没有作者：这是第 5 讲里那个文件名的小疏漏。 | A10：绝不提作者名；书用书名或描述（the cottage cheese recipe book → 那本茅屋奶酪食谱）。 |
| the stage / Google's cloud / Google's data center / two containers on your laptop / a boundary between | 舞台 / 云 / 数据中心 / 边界 | S04[9]：现在看舞台：Gemini 在 Google 的云上，两个 container 在你的笔记本上，中间隔着一条边界。 | where localhost means nothing → 在那里 localhost 毫无意义。 |

### 两次调用：函数调用与函数响应 / Two calls: function call and function response

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| call 1 / call 2 / the first call / a model call / a paid call / an embedding call | 第 1 次调用 / 第 2 次调用 / 模型调用 / 付费调用 / embedding 调用 | S07[7]：每个问题要两次模型调用，加一次 embedding 调用，全都要付费。 | 画面上的 call 1 → your code → call 2 条保持英文；字幕说第 1 次调用 / 第 2 次调用（C1）。So far, one paid call → 到目前为止，一次付费调用。 |
| function call / tool call / a forced tool call / the model writes the call / function response / the result | 函数调用 / 工具调用 / 函数响应 / 结果 | S06[2]：模型必须用一个函数调用来回答。 | Google 中文文档：函数调用、函数响应。forces a tool call → 强制调用工具。 |
| dispatcher / matches each call's name / runs the real function / wraps the result | 分发器 / 匹配 / 包装 | S07[0]：回到你的 Python 里，分发器按名字匹配每个调用，用模型给的参数运行真正的函数，再把结果包装成函数响应。 | 标准中文。 |
| temperature / temperature zero / a design choice / keeps it nearly repeatable | temperature / 设计选择 | S06[1]：课上把 temperature 列为一个设计选择。 | A3：照说（画面上的参数，实验课口语：temperature 调成 0）。temperature zero → temperature 设为 0。 |
| tool config / mode any / mode ANY / the enum value ANY / plain text isn't allowed / back to automatic | tool config / mode 设为 any / mode 为 ANY / enum 值 ANY / 自动 | S06[1]：三个设置：temperature 设为 0，菜单作为工具，以及一个 mode 设为 any 的 tool config。 | A6、B3：中文行里 tool_config 和 mode="any" 不写下划线、等号和引号；any 是 mode 的值，绝不译成“任何”（review_spoken 第 7.2 条）。en_display：tool_config、mode="any"、"mode": "ANY"（D4）。 |
| request / prints the request instead of sending it / one envelope / both declarations with the enum | 请求 / 声明 | S06[4]：一个额外的脚本运行同样的代码，但把请求打印出来，而不是发出去。 | 画面上的 built, not sent 标签保持英文。 |
| system instruction / defines one and never sends it | system instruction | S06[5]：而且没有 system instruction：和第 5 讲一样，cli.py 定义了一个，却从来没发出去。 | Gemini 的字段（画面上有）；第 5 讲 SAY 说 system prompt 所以写 system prompt，这一讲 SAY 说 system instruction。 |
| default credentials error / file not found / needs your key | DefaultCredentialsError / 找不到文件 | S06[6]：查找通过了，问题也打印出来了，但第一次模型调用需要你的密钥：报 DefaultCredentialsError，找不到文件。 | 终端上的类名照写，前面加“报”（同第 4 讲）；en_display：DefaultCredentialsError（D4）。 |
| the model's whole answer / cheese making importance location / four words in the search text / a sentence or two | cheese making importance location / 回答 | S06[8]：四个词，而描述要求的是一两句话。 | 模型写出的搜索文本照写英文（画面上的原文，A1 a）。 |
| ID / thought signature / Gemini's thinking models / sign their turn / the seal / exactly as sent / unchanged | ID / thought signature / 思考模型 / 签名 / 封印 / 原封不动 | S07[5]：原封不动地发回这一轮，封印就不会破。 | A3：thought signature 照说（画面上的 API 字段 thoughtSignature）；thinking models → 思考模型；seal → 封印（V3 里信封上的封印）。 |
| turn / the user's turn / the model's own turn / the earlier turns / turn 1 / every turn | 轮 | S07[4]：第 2 次调用发送三样东西：问题、原封不动的模型自己那一轮，以及你的函数响应。 | 对话的一轮 → 轮。Turn 1……Turn 4 → 第 1 轮……第 4 轮（C1）。 |
| stand-in / a stored chunk's vector stands in / may differ from a real query's | 替身 / 向量 / 真实查询 | S07[2]：有一个替身：没有 Google，我们没法把搜索文本向量化，所以用一个已存 chunk 的向量来替代，这 10 个 chunk 可能和真实查询返回的不一样。 | 第 5 讲：stand-in → 替身，embed → 向量化。画面上粉色的 stand-in 标签保持英文。 |
| passages / today's story / Mara and Anja / one string / characters / stapled to the call | 段落 / 故事 / Mara / Anja / 字符串 / 字符 | S07[3]：它们拼成一个 3509 个字符的字符串，作为响应钉在这个调用上。 | Ten passages came back → 返回了 10 个段落（C1）。Mara、Anja 照写（A10）。 |
| tokens / 247 and 1,269 tokens / token total / only an estimate | token / token 总数 / 估算 | S07[6]：两次调用分别用了 247 和 1269 个 token。 | 第 4 讲：LLM 的 token 照说（密钥是 key，访问令牌是 access token）。不加复数，不加千位分隔符（C1）。 |
| an Alpine valley / its caves / transhumance / the seasonal movement of livestock / the old text / rewrote the book | 阿尔卑斯山谷 / 山洞 / 转场放牧 / 旧文本 | S07[6]：一个阿尔卑斯山谷、它的山洞，还有转场放牧，也就是牲畜随季节迁移。 | 第 5 讲：transhumance → 转场放牧；S07[8] 说书里从没出现这个词时也一样。 |
| the curd / the wheels / an index answers from what was loaded | 凝乳 / 奶酪轮 / 索引 | S07[9]：你在今天这一版书上跑，会用到这样的段落：Mara、凝乳、奶酪轮。 | 第 5 讲：凝乳。An index answers from what was loaded → 索引只根据加载进去的内容回答。 |
| the response object / response dot text / the README promises the response / line 478 | response 对象 / response.text / 第 478 行 | S07[10]：改成打印 response.text，就只有回答了。 | 代码里的 response 照写；en_display：response.text（D4）。模型的 response（它的回答）→ 回答。 |

### 循环 / The loop

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| loop / the agent loop / one lap / runs until the task is done / the smallest piece of one | 循环 / agent 循环 / 一圈 | S08[0]：而 llm-rag 的 agent 只跑了一圈：一次强制的工具调用，然后一个回答。 | From two calls to a loop → 从两次调用到一个循环。 |
| stop rule / final response / a reply with no function call / plain text | 停止规则 / 最终回复 / 回复 / 纯文本 | S08[4]：停止规则：一个不含函数调用的回复，就是最终回复。 | ADK 的 final response → 最终回复。 |
| cap / turn caps / 12 turns / 16 iterations / ends the run with an error | 上限 / 轮数上限 / 迭代 | S08[6]：碰到 Agents SDK 的上限，运行就会以报错结束。 | cap → 上限（no upper bound 也是“没有上限”）；12 turns → 12 轮；16 iterations → 16 次迭代。 |
| Runner / the Runner streams events / this wrapper / the library / from outside | Runner / 事件 / 包装函数 / 库 | S08[5]：在代码里，你是从外面看这个循环的：ADK 的 Runner 以流的形式输出事件，这个包装函数留下最终回复，循环本身在库里面运行。 | Runner 照写（ADK 的类名），可以开头。events → 事件。 |
| SDK / Agents SDK / the SDK ran nothing | SDK / Agents SDK | S06[9]：SDK 什么都没运行；它手里只有声明。 | SDK、OpenAI 的 Agents SDK 照写（A1 b）。 |

### llm-rag 与两个 container（第 5 讲的部分） / llm-rag and the two containers (the L05 part)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Lecture 5 ended on one command / if you are starting fresh / service account key / secrets folder / beside it, never inside | 服务账号密钥 / secrets 目录 | S16[2]：服务账号密钥放在 llm-rag 旁边，绝不放进去；课程结束时把另外两个密钥删掉，或者给它们设上限。 | 第 3–5 讲。Starting fresh? → 从头开始？ |
| docker-shell.sh / GCP project / your own project ID / a placeholder | docker-shell.sh / GCP project 变量 / 项目 ID / 占位值 | S05[1]：第 2 步：编辑 docker-shell.sh，把 GCP project 变量改成你自己的项目 ID；我们用的是占位值。 | A6（同第 5 讲）：GCP_PROJECT → GCP project 变量；en_display：GCP_PROJECT。 |
| Compose / Chroma / the pull message / looks like an error / no such image online / builds it | Compose / Chroma / pull 的消息 / image / 构建 | S05[2]：后面那条 pull 的消息看起来像报错，其实无害：网上没有这个 image，所以 Compose 自己构建。 | 第 4、5 讲：pull、image 照说；build → 构建。 |
| banner / the at sign / the container's ID / new every run / this prompt | 横幅 / @ 符号 / container ID / 提示符 | S05[3]：提示符里 @ 符号后面是 container ID，每次运行都不一样；暂停一下，走到这个提示符。 | 和第 5 讲 S04[10] 一致。 |
| second terminal / docker ps / publishes port 8000 / remember that port | 第二个终端 / docker ps / port 8000 / 发布 | S05[4]：Chroma 发布了 port 8000；记住这个 port，第二部分会用到。 | 第 4、5 讲：port 照说，publish → 发布。 |
| the agents section / python cli.py --agent / chunk type char split / the collection does not exist / line 429 | Agents 一节 / python cli.py --agent / chunk type / char-split / collection / 第 429 行 | S05[5]：现在是 Agents 一节的第 1 步：python cli.py --agent，chunk type 用 char-split。 | A6、G3（同第 5 讲）：--chunk_type char-split → chunk type 用 char-split。README 标题 Agents 照写（A11）。 |
| the index from lecture 5 / that database / the docker volumes folder / pull and rebuild it / chunk, embed and load again | 索引 / 数据库 / docker-volumes 目录 / 重建 | S05[6]：否则就重新分块、向量化、加载。 | 第 5 讲：重建（索引）；the docker volumes folder → docker-volumes 目录（绝不写“卷”）；en_display：docker-volumes/。 |
| the staff's committed embeddings / the embed step / the load step / an extra get command | embed 这一步 / load 这一步 / --get | S05[7]：我们没有密钥，所以 embed 这一步，用的是课程团队 commit 过的 embedding。 | 第 5 讲 A3：load 这一步；get command → --get 命令（en_display：--get）。 |
| 11 books / 8,248 chunks / 24 of them / the instructor's story | chunk / 授课老师的故事 | S05[8]：11 本书，8248 个 chunk；授课老师的故事只占其中 24 个。 | C1：不加千位分隔符。 |
| exit / docker compose down / the two harmless warnings / Chroma still up / tear down | exit / docker compose down / 警告 / 拆掉 | S08[8]：然后运行 docker compose down：两条无害的警告之后，它就停了。 | 第 4、5 讲：tear down → 拆掉。Type exit → 输入 exit。 |
| the course's hosted Cheese Agent Tool / up at the time of recording / try it in Chrome | Cheese Agent Tool / 托管 / Chrome | S07[11]：第 2 步链接到课程托管的 Cheese Agent Tool，录制时还在线；在 Chrome 里试试。 | 工具名照写（A1 b）。 |

### ADK：安装与 uv / ADK: setup and uv

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Agent Development Kit / ADK / Google's Agent Development Kit / a uv environment | Agent Development Kit / ADK / uv 环境 | S09[0]：这次不用 Docker：Google 的 Agent Development Kit，跑在你笔记本上的一个 uv 环境里。 | 产品名照写（A1 b）；ADK 可以开头。“智能体开发套件”只用于配套材料，字幕里不写。 |
| clone / a placeholder for the address / cd google ADK tutorial / no such folder / named after the repo / cd L-L-M agent google ADK | clone / 占位符 / cd google-adk-tutorial / cd llm-agent-google-adk | S09[2]：改成输入：cd llm-agent-google-adk。 | 命令照写（en_display：cd google-adk-tutorial、cd llm-agent-google-adk）。Open a new terminal where you keep your clones → 打开一个新终端，进到你放 clone 的地方。 |
| six numbered module folders / the ADK module on MCP / module READMEs / lock file / so everyone resolves fresh versions | 模块目录 / 模块 / lock 文件 / 解析 | S09[3]：额外的 ls 显示有六个带编号的模块目录，但没有 lock 文件：这个 repo 忽略了它，所以每个人都会重新解析出最新的版本。 | 第 1 讲：lock 文件，resolve → 解析。module → 模块（A7：课上的 blocks 是“组件”）。 |
| dot env / dot env dot example / the root file / root dot env / only the nearest dot env is loaded | .env / .env.example / 根目录的 .env | S09[4]：接下来，把 .env.example 复制成 .env 文件。 | 文件名照写（en_display：.env、.env.example）。 |
| Google API key / a placeholder Google API key / Google API key equals / create a key in Google AI Studio | Google API key / Google API 密钥 / Google AI Studio / 密钥 | S09[5]：然后在 Google AI Studio 里创建一个密钥，粘贴到 .env 里 Google API key 的等号后面。 | A6：GOOGLE_API_KEY= → Google API key 的等号后面（变量名，按 SAY 写）；a placeholder Google API key（变量的值）→ 一个占位的 Google API 密钥。单说 key → 密钥（A7）。 |
| the model line / a current model / the code's fallback / shut down / limits 2.5 Flash to earlier users | 后备模型 / 已停用 / 老用户 | S09[7]：Google 把代码里的后备模型 gemini-2.0-flash 列为已停用，又把 gemini-2.5-flash 限定给老用户使用。 | C2（同第 5 讲）：模型 ID 照代码写，中英两行一致（en_display：Gemini 2.0 Flash → gemini-2.0-flash，2.5 Flash → gemini-2.5-flash）。 |
| the project file / Python 3.10 or newer / ADK 1.8 or newer / no upper bound / sentence transformers | 项目文件 / 及以上 / 上限 / sentence-transformers | S09[8]：项目文件要求 Python 3.10 及以上、ADK 1.8 及以上，没有上限。文件里还列了 Chroma 和 sentence-transformers。 | 第 1 讲：or newer → 及以上。the project file（画面上的 pyproject.toml）→ 项目文件；包名 sentence-transformers 照写（en_display）。 |
| uv sync / no Python at all / downloads the newest / CPython 3.15.0 / resolves 189 packages | uv sync / CPython 3.15.0 / 包 | S09[10]：和第 1 讲一样，周围没有 Python，uv 就下载最新的：录制时是 CPython 3.15.0。 | 第 1 讲：package → 包；at the time of recording → 录制时（A9）。 |
| O-N-N-X runtime / wheels / only up to Python 3.14 / which Chroma pulls in | onnxruntime / wheel / 引入 | S09[11]：Chroma 引入的 onnxruntime，只有到 Python 3.14 为止的 wheel。 | 第 1 讲：wheel 照说。pulls in（依赖）→ 引入，绝不写 pull（A7）。en_display：onnxruntime。 |
| uv python pin 3.13 / the fix / a version pin / your Python pin / pinned / unpinned | uv python pin 3.13 / pin / Python pin | S09[12]：修复办法是一条额外的命令：uv python pin 3.13。 | 第 1 讲：pin 照说（pin 住）。pinned → pin 了版本 / 版本 pin 住了；unpinned → 没有 pin 版本；a version pin doesn't help → pin 版本没用。 |
| PyTorch / CUDA / about 1.6 gigabytes / a Linux PC | PyTorch / CUDA / Linux 电脑 | S09[13]：PyTorch 让它变得很大：大约 1.6 GB，在 Linux 电脑上还要再加大约 3 GB 的 CUDA。 | C2：gigabytes → GB。 |
| uv run ADK dash dash version / 2.12.0 / get your sync to succeed | uv run adk --version / sync | S09[14]：额外检查一下：uv run adk --version，录制时显示 2.12.0。 | 命令照写，小写（en_display：uv run adk --version）。 |

### ADK：adk web 与目录名 / ADK: adk web and the folder names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| uv run ADK web / Running agents / the repository root / version 2.12 / may Google collect usage data | uv run adk web / Running Agents / repo 根目录 / 使用数据 | S10[0]：Running Agents 一节的第 1 步，在 repo 根目录下：uv run adk web。 | README 标题照写（Running Agents、Agents；A11）；en_display：uv run adk web。 |
| telemetry / off by default / the capital Y / pressing enter / answers yes / uv run ADK telemetry disable | 遥测 / 大写的 Y / 回车 / yes / uv run adk telemetry disable | S10[1]：提示文字说遥测默认是关闭的，可大写的 Y 意味着直接按回车就是回答 yes。 | en_display：uv run adk telemetry disable。 |
| web server / the server / server log / the browser / localhost 8000 / curl / redirect / dev UI | web 服务器 / 服务器 / 服务器日志 / 浏览器 / localhost:8000 / curl / 重定向 / dev UI | S10[2]：第 2 步：在浏览器里打开 localhost:8000；额外的 curl 显示它重定向到了 dev UI。 | A7：MCP 以外的 server → 服务器。dev UI 照写（ADK 的名字，画面上是 /dev-ui/）。en_display：localhost 8000 → localhost:8000。 |
| agent dropdown / 7 entries / the nested ones / pick 1 baseline / the page refuses / valid Python identifiers | 下拉菜单 / 1-baseline / 标识符 | S10[3]：按它的 README 选 1-baseline，页面拒绝了：agent 名必须是合法的 Python 标识符。 | 目录名照写（en_display：1-baseline）。 |
| folder name / the app's name / an identifier / letters, digits and underscores / never starting with a digit / an invalid app name | 目录名 / app 名 / 字母 / 数字 / 下划线 | S10[4]：每个目录名都会变成 app 名，而标识符只能包含字母、数字和下划线，并且不能以数字开头。 | 第 1 讲 A6：app 是名字，不是概念：app 名。 |
| renaming / control C / stop the server / drop each leading number / hyphens / underscores | 改名 / Ctrl-C / 连字符 | S10[6]：先按 Ctrl-C 停掉服务器，再去掉每个开头的数字，把连字符换成下划线。 | B3（同第 4 讲）：中文行写 Ctrl-C；en_display：Ctrl+C。 |
| baseline / baseline dot agent / root agent / the root dot env file / the log | baseline / baseline.agent / root agent / 日志 | S10[7]：日志说它加载了根目录的 .env 文件，并在 baseline.agent 里找到了 root agent。 | root agent（root_agent）按 SAY 写（A6）。S11[0] 以 Baseline 开头：在 baseline 里，……（A5）。 |
| the quick start / passes a file where a folder is expected / drop the word web / only prints help | 快速入门 / 帮助信息 | S10[8]：还有两个小疏漏：快速入门在该传目录的地方传了一个文件，各模块的 README 又漏了 web 这个词，所以命令只会打印帮助信息。 | A9：Two more slips → 还有两个小疏漏。 |
| clash / address already in use / dash dash port 8080 | 冲突 / address already in use / --port 8080 | S10[9]：先运行 docker compose down，或者加上 --port 8080。 | 终端原文照写；en_display：--port 8080。 |

### ADK：Runner、session 与状态 / ADK: Runner, session, state

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| session / a session / session state / state / events / its history of events | session / 状态 / session 状态 / 事件 / 事件历史 | S11[2]：另一个额外的请求创建了一个 session：状态是空的，也还没有事件。 | A3：session 照说（ADK 和 web 实验课口语：建一个 session）；书面写“会话（session）”。state → 状态，State 标签页除外（A11）。 |
| whiteboard / a shared whiteboard / cells / that cell / fills its cells at once | 白板 / 格子 | S11[2]：把状态想成一块共享的白板。 | V6。白板上的 cell → 格 / 格子；notebook 的 cell 是“单元格”（A7）。 |
| the three LLM agents / a model / an instruction / an output key / no tools at all | LLM agent / 指令 / output key | S11[0]：在 baseline 里，有三个 LLM agent，每个都有一个模型、一条指令和一个 output key。 | A6：output_key → output key；en_display：output_key。 |
| sequential agent / validator / planner / summarizer / in order / parallel agent | 顺序 agent / 校验器 / 规划器 / 总结器 / 并行 agent | S11[1]：顺序 agent 依次运行它们：校验器、规划器、总结器。 | 画面上是 SequentialAgent / ParallelAgent，SAY 用普通说法。三个 agent（ItineraryValidator、TravelPlanner、TripSummarizer）按作用称呼。 |
| placeholder / its instruction's placeholder / filled from that cell / goes into the state | 占位符 | S11[3]：校验器的回复写进状态，放在它的 output key 下面；规划器运行之前，它指令里的占位符会用那一格的内容填上。 | {key} 那个洞 → 占位符。 |
| the tree the UI loads / an extra request / another extra request is | 树 / 请求 | S11[1]：一个额外的请求显示了 UI 加载的那棵树，模型来自你根目录的 .env；核对一下你的。 | D6 的额外检查句式。 |
| the lecture's planner / prices / the model's guesses / sums from Python | 课上的旅行规划 / 价格 | S11[5]：课上的旅行规划需要实时系统；这条 pipeline 没有工具，所以里面的价格都是模型猜的。 | A7：这里指课上的旅行规划例子（课件 20–22）。pipeline 照说（系列）。 |
| Internal Server Error / API key not valid / the server log / the placeholder reached Google / refused | Internal Server Error / API key not valid / 占位密钥 / 拒绝 | S11[7]：服务器日志说明了原因：API key not valid。 | 终端原文照写（A1 a）。 |
| State tab / three replies in order / the three new entries / the session is a file / plan a trip | State 标签页 / 回复 / 规划 | S11[8]：每个请求是三次模型调用：暂停一下，规划一次旅行。 | entries → 项，绝不写“密钥”或“键”（review_spoken 第 7.4 条）。 |

### MCP：插头与 server / MCP: plugs and servers

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| MCP / the Model Context Protocol / protocol / a custom integration / one pattern | MCP / 模型上下文协议 / 协议 / 定制集成 | S12[2]：每个工具都要做一次定制集成。 | MCP 照写（可以开头）；the Model Context Protocol → 模型上下文协议（标准中文名）。 |
| host / clients / MCP server / remote MCP server / FastMCP server / filesystem server / the server | host / client / MCP server / 远程 MCP server / FastMCP server / 文件系统 server | S12[2]：MCP，也就是模型上下文协议，把它变成一种模式：一个 host 带着若干 client，每个服务对应一个 MCP server。 | A3：MCP 里的 host、client、server 照说（中国工程师说 MCP server）；其他地方 server → 服务器（A7）。书面写 MCP 主机、客户端、服务器（MCP server）。 |
| plug / Plug 1 / Plug 2 / Plug 3 / its own plug / a shared protocol, not a program you run | 插头 | S12[3]：在代码里，每个 server 都是一个单独的插头，教程里有三个。 | V7 的比喻。The lecture's MCP box → 课上那个 MCP 方框（第 5 讲 box → 方框）。 |
| wire one agent to ten services / services / its own protocol / do you see a problem | 服务 | S12[1]：课上问：你看出问题了吗？ | C1：ten services（SAY 写成单词）→ 十个服务。 |
| Install Node / npx / a child process / standard input and output / the agent's toolset / the filter | Node / npx / 子进程 / 标准输入输出 / 工具集 / 过滤器 | S12[5]：这个 agent 的工具集用 npx 启动一个文件系统 server，作为子进程，通过标准输入输出通信。 | tool_filter → 过滤器（A6：字幕里不写带下划线的名字）。 |
| offers 14 / including write and edit / lets three through / list files | 写入 / 编辑 / 放行 / 列出文件 | S12[6]：这个 server 提供 14 个，包括写入和编辑，过滤器放行了三个。 | 工具名（write_file、edit_file）按 SAY 的说法用意思称呼。 |
| a plain function / by URL / passed as MCP servers, not tools | 普通函数 / URL / MCP servers 参数 / tools | S12[7]：先是第一个工具，写成普通函数；然后 notebook 按 URL 连上一个远程 MCP server，作为 MCP servers 参数传进去，而不是 tools。 | A6：mcp_servers → MCP servers 参数（按 SAY 写）；tools 是参数名；en_display：mcp_servers、tools。 |
| 406 / a browser's plain request / web pages / initialize / list tools / call / one cheese fact per call | 406 / 网页 / 初始化 / 列出工具 / 奶酪冷知识 | S12[8]：浏览器的普通请求得到 406：server 在运行，但它说的是 MCP，不是网页。 | fun fact → 冷知识。 |
| in a thread / port 8001 / the comment above / an older saved output | 线程 / port 8001 / 注释 | S12[9]：一个小疏漏：上面的注释写的是 8000，一份较早保存的输出也是。 | A9。 |
| who does the talking / your client process / network access / it still only writes calls | client 进程 / 网络访问 | S12[10]：MCP 并没有给模型任何网络访问权限；它仍然只是写出调用。 |  |

### 多个 agent / Many agents

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| orchestrator / specialist / a whole agent behind one function / decides which to call | 编排 agent / 专家 agent | S13[2]：在 Guild 里，每个专家 agent 都变成一个工具：一个函数背后是一整个 agent。 | orchestrator → 编排 agent（S13、S15）；orchestration → 编排。 |
| who plans the order / first answer / assembly line / its order fixed in Python | 顺序 / 流水线 | S13[1]：顺序 agent 就是一条流水线，顺序在 Python 里写死。 | A7：order（先后）→ 顺序；菜单的 order → 点单。 |
| a rule in prose / no code enforces it / at most 2 review rounds / a cap of 12 turns | 规则 / 强制执行 / 审查 | S13[3]：这是写在文字里的规则；没有代码去强制执行它，除了 12 轮的上限。 | 引用的指令要翻译：follow the assembly line strictly → 严格按流水线来。 |
| three errors getting a response / still produced a quiz / which calls failed / every hop | 测验 / 一跳 | S13[4]：每多一跳，就多一份成本、一段时间和一种失败的可能；暂停一下，跑一遍 Guild。 |  |
| custom agent / classifier / the model's label / one word / if statements / handler / the else branch / clarification | 自定义 agent / 分类器 / 标签 / if 语句 / 处理函数 / else 分支 / clarification | S13[5]：在这个自定义 agent 里，一个分类器往状态里写一个词，再由普通的 if 语句选出处理函数。 | A7：分类的 label → 标签（画面上的标签都带名字：your turn 标签）。The else branch: clarification → 走的是 else 分支：clarification（处理函数的名字）。 |
| the comparison is exact / lowercase the label first / structured output / the exercises try both | 精确匹配 / 小写 / 结构化输出 | S13[6]：比较是精确匹配；先把标签转成小写，或者要求结构化输出。 |  |

### harness：审批关卡与回执 / The harness: approval gate and receipt

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Travel Planner / rehearses / its pinned agents package / a mock catalog / and booking nothing | Travel Planner / 演练 / agents 包 / 模拟清单 / 预订 | S14[0]：巴黎缩成了一份模拟清单：3 个城市、6 家酒店、5 个搜索工具和一个 finalize 工具，什么都不会真的预订。 | A7：catalog → 清单，绝不写“目录”（那是文件夹）。 |
| turn 1 asks which California city / Turn 2 runs five searches / and offers options / the user picks / the exact plan / asks for a yes | 加州 / 选项 / 计划 | S14[1]：第 2 轮做了五次搜索，给出几个选项。 | 要输入的 yes 照写（A1 a）。 |
| the gate / finalize / a finalize call / propose / the approved one / pending / needs confirmation | 关卡 / finalize / 提议 / 已批准 / 待批准 / needs confirmation | S14[2]：这就是关卡。 | gate → 关卡（同一个意思同一个词；第 4 讲的三道关卡也是“关卡”）。finalize（finalize_itinerary，按 SAY 说）照写；needs_confirmation → needs confirmation（A6）。pending / approved → 待批准 / 已批准（画面上黄色的 PENDING、绿色的 APPROVED 印章保持英文）。 |
| approval / apply confirmation / an explicit yes / copies pending to approved / the human's message | 批准 / apply confirmation / 明确的 yes | S14[3]：批准放在另一个函数 apply confirmation 里：只有明确的 yes，才会把待批准的计划复制为已批准。 | A6：apply_confirmation → apply confirmation；en_display：apply_confirmation。A9：S14[3] 后面是思考题：不能说它只在人的消息上运行。 |
| stamp / every retry gets the same stamp / the stamp flips to approved | 印章 / 重试 | S14[4]：在第 3 轮里，什么都没被批准，所以每次重试都会盖上同一个印章。 | V8。 |
| the budget / line by line / 2,690 of the 6,000 dollars / the notebook's own test | 预算 / 美元 / 测试 | S14[5]：印章翻成已批准，finalize 运行，Python 逐行算出预算：2690 美元，上限 6000。 | C1、C2。 |
| checked state / the model's prose / an itinerary that skipped the check / raises an error / prints a warning | 行程 / 抛出异常 / 警告 | S14[6]：用户看到的内容来自检查过的状态，而不是模型写的文字。 | raises an error → 抛出异常（第 4 讲：异常 = Python 的 exception）。 |
| can't talk its way past / on the action tool | 绕不过去 / 行动工具 | S14[7]：这个 notebook 把两者都写进代码，模型怎么说都绕不过去；代码就放在行动工具上。 |  |
| a cheese newsletter per reader / Microsoft's Agent Framework / the users cell / preview only / nothing is sent | 简报 / 读者 / Agent Framework / USERS 单元格 / 预览 | S15[0]：最后一个 notebook 给每位读者写一份奶酪简报，用的是 Microsoft 的 Agent Framework，版本 pin 住了。 | the users cell → USERS 单元格（en_display：the USERS cell）。newsletter → 简报（notebook 标题 Cheese Newsletter 在画面上照旧）。 |
| researcher / editor / send email / web search / at most 16 iterations / one tool call at a time | 研究员 / 编辑 / send email / 网页搜索 | S15[1]：编排 agent 有三个工具：一个带网页搜索的研究员、一个编辑，以及 send email。 | A6：send_email → send email（工具名）；S12[0] 的普通动词 sending email → 发邮件。 |
| validates every draft / hands errors back as the tool's result / saved the HTML / that run had four readers / today's list | 校验 / 草稿 / 工具的结果 / HTML / 名单 | S15[2]：然后 send email 把 HTML 存了下来。 |  |
| receipt / a claim / ignores its words / is that file on disk / the run fails | 回执 / 声称 / 磁盘 | S15[3]：如果没有，这次运行就算失败；成功看的是回执，而不是它声称了什么。 | A7：receipt → 回执（证明动作确实发生了）；第 1 讲把 lock 文件比作“小票”，是另一个意思。 |
| a rule that lives only in the prompt / no embedded URLs / a note is not a check / don't trust, check | 便条 / 检查 | S15[4]：保存的预览里还是有一个，因为没有代码去检查；便条不等于检查。 | 编辑收到的指令要翻译：no embedded URLs → 不要嵌入 URL。don't trust, check → 别信，要查。 |

### Colab notebook / The Colab notebooks

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Colab / notebook / Colab notebooks / the notebook / a later notebook / the last notebook | Colab / notebook | S03[1]：这个 notebook 固定模型和问题，每一步改的是输入。 | A3：notebook 照说（实验课口语：跑一下这个 notebook），因为“笔记本”是 laptop（A7）。书面写“Colab 笔记本（notebook）”。 |
| cell / the install cell / the users cell / the MCP cells / runtime / disconnect and delete the runtime | 单元格 / 安装单元格 / 运行时 | S16[2]：在每个 notebook 里，断开连接并删除运行时。 | Colab 中文界面：单元格、运行时。白板的 cell 是“格子”（A7）。 |
| Cheese Quiz / Cheese Quiz Guild / the Guild / Travel Planner / the newsletter | Cheese Quiz / Cheese Quiz Guild / Guild / Travel Planner / 简报 | S02[0]：先讲概念，在 Cheese Quiz 里。 | notebook 名和章节名照写（A1 b）；the newsletter → 简报。 |
| Save a copy in Drive / the Secrets panel / your OpenAI key / under the name shown / notebook access on | Save a copy in Drive / Secrets 面板 / OpenAI 密钥 / Notebook access | S02[0]：点 Save a copy in Drive，再在 Secrets 面板里用画面上的名字添加你的 OpenAI 密钥，并打开 Notebook access。 | 第 1 讲 A11：要点的菜单和开关照英文写（示意画面上的字）。 |
| it installs two packages / unpinned / it hides all output / if imports fail / that redirect / the quiz files / the setup | 包 / import / 重定向 / 测验文件 / 准备工作 | S02[1]：安装单元格装两个包，没有 pin 版本，还隐藏了全部输出：如果后面 import 失败，就去掉那个重定向再跑一次。 | 第 1 讲：import 照说；redirect → 重定向。 |
| a web search tool that OpenAI hosts / its two searches / one tool used / it counts tools configured, not calls | 网页搜索工具 / 托管 / 调用次数 | S02[5]：它还显示用了一个工具，但这个数统计的是配置的工具，不是调用次数。 |  |
| the staff's recorded run / the staff's saved run / saved outputs / the saved preview | 课程团队 / 保存的输出 / 预览 | S01[7]：模型的回答都是课程团队保存的输出。 | 第 3–5 讲：the staff → 课程团队。画面上的 recorded 标签保持英文（A11）。 |

### 带下划线的名字（A6） / Names with an underscore (A6)

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| get_book_by_author / search_content / tool_config / mode="any" / output_key / mcp_servers / tool_filter / needs_confirmation / apply_confirmation / send_email / finalize_itinerary / root_agent / GCP_PROJECT / GOOGLE_API_KEY / --chunk_type | get book by author / 搜索文本 / tool config / mode 设为 any / output key / MCP servers 参数 / 过滤器 / needs confirmation / apply confirmation / send email / finalize / root agent / GCP project 变量 / Google API key / chunk type | S14[2]：模型发起的 finalize 调用只能提议：如果计划不是已批准的那一份，代码就把它存为待批准，并返回 needs confirmation。 | A6；字面形式只出现在 en_display 里（D4）。 |

### 标签、进度条与固定句式 / Tags, tracker, fixed patterns

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the tracker / the gray tag / the lecture slides / each yellow your-turn tag / the study guide / the exercises | 进度条 / 灰色标签 / 课件 / your turn 标签 / 学习指南 / 练习 | S01[5]：左上角的进度条显示当前步骤；右上角的灰色标签标出对应的课件。 | 和第 5 讲 S01[5] 一致；标签名照画面写（A11）。 |
| an extra check / an extra script / an extra request / the extra curl commands / not in the README / isn't in the README either | 额外检查 / 额外的脚本 / 额外的请求 / README 里没有 | S10[6]：管用的是改名，这也不在 README 里。 | D6。 |
| at the time of recording / we recorded without keys / ran for real / every model call stopped unsent / was refused | 录制时 / 真实运行 / 被拒绝 | S01[7]：我们在 2026 年 10 月 18 日录制，没有任何密钥。 | A9：录制时，绝不省略。 |
| we hide the instructor's name / your terminal shows it / the instructor / the instructor's book | 授课老师 / 授课老师的书 | S01[8]：画面上我们隐去了授课老师的名字；你的终端里会显示。 | A10：绝不提授课老师的名字。 |
| a small slip / one small slip / there are two more slips / a file name slip | 一个小疏漏 / 两个小疏漏 | S09[2]：一个小疏漏：目录名和 repo 名一样。 | A9（同第 5 讲）：所有勘误用同一个说法，后面一定紧跟改法。 |
| Test yourself / One: … Five: / answers and every command / next lecture | 自测 / 第一题 / 第五题 / 下节课 | S16[5]：自测一下。 | D6。 |
| part 1 / part 2 / lecture 1 / lecture 5 / lecture 7 / next lecture / this video | 第一部分 / 第二部分 / 第 5 讲 / 第 7 讲 / 下节课 | S08[9]：第二部分，由框架替我们跑这个循环。 | A10。 |

### 数字与单位 / Numbers and units

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| line 429 / line 478 / step 1 / step 6 / Turn 4 | 第 429 行 / 第 478 行 / 第 1 步 / 第 4 轮 | S05[5]：那是第 429 行，在任何 Gemini 调用之前。 | C1。 |
| counts: 10 passages / 9 names / 11 books / 178 chunks / 1,505 chunks / 8,248 chunks / 3,509 characters / 189 packages / 7 entries / 14 tools / 12 turns / 16 iterations | 10 个段落 / 178 个 chunk / 1505 个 chunk / 3509 个字符 | S04[8]：那本茅屋奶酪食谱，178 个 chunk，作者不在名单上。 | C1：不加千位分隔符。 |
| sizes, times and money: 40 seconds / 3 seconds / 39 seconds / 13 seconds / 1.6 gigabytes / 3 gigabytes / 2,690 / 6,000 dollars | 40 秒 / 1.6 GB / 3 GB / 2690 美元 | S05[3]：构建大约 40 秒后，出现横幅。 | C2。 |
| versions and models: Python 3.12.15 / uv 0.13.1 / CPython 3.15.0 / CPython 3.13 / Python 3.14 / ADK 1.8 / ADK 2.12.0 / 1.27.5 / GPT-4o / Gemini 2.5 Flash / Gemini 3.1 Flash-Lite / Gemini 2.0 Flash | Python 3.12.15 / uv 0.13.1 / CPython 3.15.0 / ADK 2.12.0 / gpt-4o / gemini-2.5-flash / gemini-3.1-flash-lite / gemini-2.0-flash | S09[6]：选 LLM 核心是课上的第一个设计决定，在这里只是一行：换成一个当前的模型，比如 gemini-3.1-flash-lite。 | C2：模型 ID 照代码写，中英两行一致（en_display）。 |
| dates: October 18, 2026 / September 22 | 2026 年 10 月 18 日 / 9 月 22 日 | S05[6]：它在 docker-volumes 目录里；如果你是在 9 月 22 日之前分块的，先 pull，再重建它。 | C2。 |

### 课程、产品与名字 / Course, products, names

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / MLOps Learning / the study guide / the course's | AC215 / MLOps Learning / 学习指南 | S01[8]：每条命令都在学习指南里，就在 MLOps Learning 这个 repo 里。 | 同第 5 讲 S16[9]；en_display：MLOps_Learning。 |
| llm-rag / L-L-M rag / llm-agent-google-adk / student / laptop | llm-rag / llm-agent-google-adk / student / 笔记本 | S01[4]：先手写，用 llm-rag 的 agent；再用框架，Google 的 Agent Development Kit；最后用 harness，在 Colab notebook 里。 | laptop → 笔记本（第 1 讲）；en_display：llm-rag、llm-agent-google-adk。 |
| products: Google / Google AI Studio / Gemini / OpenAI / Microsoft / Agent Framework / Docker / Compose / Chroma / Python / uv / Node / npx / FastMCP / Colab / Drive / Chrome / Linux / PyTorch / CUDA / JSON / HTML / URL | Google / Google AI Studio / Gemini / OpenAI / Microsoft / Agent Framework / Docker / Chroma / Node / FastMCP / Colab / Drive / Chrome / Linux / JSON / HTML / URL | S01[6]：你需要第 5 讲的数据库和密钥，Docker、uv、Node，再加两个密钥：一个来自 Google AI Studio，一个来自 OpenAI，并且开通计费。 | 拉丁字母（A1 b）。 |

### 标题与章节（meta.yaml）/ Titles and chapters (meta.yaml)

| English | 中文 | 说明 |
|---|---|---|
| Video title | AC215 · 第 6 讲：LLM 智能体 I（跟练：llm-rag、llm-agent-google-adk） | H1。Agents I → 智能体 I（同第 2 讲的“容器 I”）；跟练 = follow-along。 |
| Part 1 / Part 2 | AC215 · 第 6 讲（上）：智能体是什么，以及手写函数调用（llm-rag） / AC215 · 第 6 讲（下）：循环交给框架——ADK、MCP、多智能体与 harness | H1。frameworks own the loop → 循环交给框架（字幕说“循环归框架管”）。 |
| Chapters S01–S08: Who searched your database? / Who holds the steering wheel? / Everything the model knows is in the envelope / A menu of two tools / Back in the container: the agent needs an index / Call 1: the model writes the call / Call 2: your code ran it, the model answers / From two calls to a loop | 是谁搜索了你的数据库？ / 谁握着方向盘？ / 模型知道的一切，都在信封里 / 只有两个工具的菜单 / 回到容器：智能体（agent）需要索引 / 第 1 次调用：模型写出调用 / 第 2 次调用：你的代码执行，模型作答 / 从两次调用到一个循环 | H1，书面语体；问句保留问号。 |
| Chapters S09–S16: ADK: clone, configure, and a sync that fails / adk web and the folder names / Runner, session, state: the shared whiteboard / Tools you didn't write: MCP / Many agents: who plans the order? / The harness: only a human says yes / The harness: success is a receipt / Tear down, recap, and what's next | ADK：克隆、配置，和一次失败的 sync / adk web 与目录名 / Runner、会话（session）与状态：共享白板 / 不是你写的工具：MCP / 多个智能体：顺序由谁来定？ / harness：只有人能说 yes / harness：成功要有回执 / 清理、回顾与下节预告 | H1。adk web 是命令，照写小写（同第 1 讲“apt、git 和仓库”）。 |

### 配套材料的书面语体 / Written register of the companions

| English | 书面 | 说明 |
|---|---|---|
| container / image / repo / clone / commit / port / prompt / system prompt / embedding / collection / agent / session / notebook / MCP server / host / client / harness / token / pin / lock file | 容器 / 镜像 / 仓库 / 克隆 / 提交 / 端口 / 提示词 / 系统提示词 / 嵌入向量 / 集合（collection）/ 智能体（agent）/ 会话（session）/ Colab 笔记本（notebook）/ MCP 服务器（MCP server）/ MCP 主机 / MCP 客户端 / harness / 词元（token）/ 固定版本（pin）/ 锁文件（lock file） | H3、A4：在配套材料里首次出现时加英文括注；harness 书面也保留英文，首次出现解释一次。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

AC、access、address、adk、Agent、agent、Agentic、Agents、AI、already、Anja、ANY、any、API、apply、author、baseline、baseline.agent、book、by、cd、Cheese、cheese、Chroma、Chrome、clarification、cli.py、client、clone、collection、commit、Compose、compose、config、confirmation、container、copy、Corrective、CPython、Ctrl-C、CUDA、curl、data、DefaultCredentialsError、dev、Development、disable、Docker、docker、docker-shell.sh、docker-volumes、down、Drive、edit、else、email、embed、embedding、enum、env、env.example、Error、exit、extra、FastMCP、finalize、flash、flash-lite、Foods、Framework、GB、Gemini、gemini-、get、git、Google、google-adk-tutorial、gpt-、grep、Guild、harness、help、host、HTML、ID、if、image、import、importance、in、Institute、instruction、Internal、JSON、key、Kit、Learning、LLM、llm-agent-google-adk、llm-rag、load、localhost、location、lock、ls、making、Mara、MCP、Microsoft、MLOps、mode、Newsletter、Node、not、Notebook、notebook、npx、onnxruntime、OpenAI、output、PC、pin、pipeline、Planner、port、prompt、ps、pull、Python、python、PyTorch、Quiz、RAG、README、repo、response、response.text、root、run、Runner、Running、Save、schema、SDK、Secrets、secrets、Self-RAG、send、sentence-transformers、Server、server、servers、session、sh、signature、State、status、student、Studio、sync、system、telemetry、temperature、thought、token、Tool、tool、tools、Travel、turn、UI、URL、use、user、USERS、uv、valid、version、web、wheel、Whole、Woman's、yes、your。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（cd llm-rag、sh docker-shell.sh、python cli.py --agent、python cli.py --load、--get、docker ps、docker compose down、exit、git clone、cd google-adk-tutorial、cd llm-agent-google-adk、ls、grep、curl、uv sync、uv python pin 3.13、uv run adk web、uv run adk --version、adk telemetry disable、--port 8080、git status、npx、Ctrl-C；--chunk_type 见 A6）、文件名、目录名和路径（cli.py、docker-shell.sh、.env、.env.example、.adk、docker-volumes、secrets、llm-rag、llm-agent-google-adk、google-adk-tutorial、1-baseline、baseline、baseline.agent）、包名（onnxruntime、sentence-transformers）、代码里的名字和值（enum、ANY、any、user、system、response、response.text、finalize、yes、USERS、clarification、tools；带下划线的见 A6）、模型 ID（gpt-4o、gemini-2.5-flash、gemini-3.1-flash-lite、gemini-2.0-flash；C2）、终端原文和报错（DefaultCredentialsError、Internal Server Error、API key not valid、address already in use、406）、模型写出的搜索文本 cheese making importance location、界面字样（Save a copy in Drive、Secrets、Notebook access、State 标签页、dev UI）、README 标题（Agents、Running Agents；A11）和旁白提到的画面标签（your turn；A11）。（b）**产品、组织、课程和名字**：AC215、MLOps Learning、Google、Google AI Studio、AI Studio、Gemini、OpenAI、Microsoft、Agent Framework、Agents SDK、SDK、Agent Development Kit、ADK、Runner、Colab、Drive、Docker、Compose、Chroma、Python、CPython、uv、Node、npx、FastMCP、MCP、PyTorch、CUDA、Linux、Chrome、JSON、HTML、URL、RAG、Agentic RAG、Self-RAG、Corrective RAG、Cheese Quiz、Cheese Quiz Guild、Guild、Travel Planner、Cheese Agent Tool、Whole Foods、Woman's Institute、Mara、Anja、student。（c）**中国 MLOps 工程师在实验课上本来就说英文的词，封闭清单**：第 1 讲的 repo、clone、commit、pin、lock 文件、import；第 2–4 讲的 container、image、pull、pipeline、port、localhost、API、ID、token；第 5 讲的 chunk、embedding、collection、prompt（只指 LLM 的 prompt）、system prompt、LLM、agent；这一讲新增 notebook（A3）、session（A3）、schema 和 JSON schema（A3）、enum（A3）、temperature（A3）、system instruction（A3）、thought signature（A3）、SDK、MCP 里的 host、client 和 server（A3）、harness（A3）、wheel（第 1 讲文档已有）、dev UI。一个词只有在实验课口语真的说英文、而中文生硬、有歧义或和别的术语撞车时才进（c）。绝不为了“味道”说英文：tool、tool call、function call、function declaration、function response、dispatcher、arguments、parameters、fields、required、description、request、response（模型的回答）、reply、final response、loop、lap、stop rule、cap、iteration、turn、event、state、memory、instructions、building block、dynamic control、decision maker、planner、orchestrator、orchestration、workflow、framework、library、wrapper、protocol、custom integration、child process、toolset、filter、server（MCP 以外）、web server、browser、redirect、identifier、telemetry、placeholder、cell、runtime、classifier、label、handler、structured output、guardrail、success criteria、approval、pending、approved、receipt、handoff、deep research、context engineering、reasoning engine、thinking model、catalog、newsletter 都说中文。
- **[A2]** container 和 image（同第 2–5 讲）。字幕说 container 和 image：两个 container、container ID、网上没有这个 image；量词“个”。标题、章节名、meta.yaml 和配套文档写“容器”“镜像”（A4）。字幕里绝不写“镜像”。pull 照说（后面那条 pull 的消息；先 pull，再重建它：这里是 git pull）；pulls in（依赖关系）→ 引入，绝不写 pull（Chroma 引入的 onnxruntime）。build → 构建（Compose 自己构建）。
- **[A3]** agent 的词（这一讲新增）。**agent** 照说（这个 agent、agent 函数、agent 循环、LLM agent、顺序 agent、并行 agent、编排 agent、专家 agent、主 agent、自定义 agent），书面写“智能体（agent）”。**课上的框架**（SLIDES.md）：LLM core → LLM 核心，instructions → 指令（an instruction → 一条指令），tools → 工具，memory → 记忆（绝不写“内存”），dynamic control → 动态控制，building blocks / five blocks → 组件 / 五个组件，the anatomy → agent 结构图，decision maker → 决策者，planner → 规划器，hub / spokes → 轮毂 / 辐条，base LLM → 基础 LLM，reasoning LLM → 推理 LLM，reasoning engine → 推理引擎，reasoning workflow → 推理工作流，reasoning model → 推理模型，a multi-call system → 多次调用的系统，live systems → 实时系统，tools that act → 能行动的工具，the autonomy to decide → 自主决定的能力，Agentic RAG / Self-RAG / Corrective RAG 照写，data tools / action tools / orchestration tools → 数据工具 / 行动工具 / 编排工具，handoffs → 交接，agents as tools → 把 agent 当工具用，deep research → 深度研究，a lead agent → 主 agent，synthesis → 汇总，success criteria → 成功标准，guardrails → 护栏（hard / soft guardrail → 硬护栏 / 软护栏），context engineering → 上下文工程，the lecture's formula → 课上的公式。**函数调用**：function declaration → 函数声明，function call → 函数调用，tool call → 工具调用，a forced tool call → 一次强制的工具调用，function response → 函数响应，dispatcher → 分发器，the real function → 真正的函数，arguments / parameters → 参数，fields → 字段，required → 必填，description → 描述，parameter descriptions → 参数描述，JSON schema 和 schema 照说（output schema → 输出 schema），enum 照说（enum 值 ANY），temperature 照说（temperature 设为 0），tool config 照说（A6），mode 设为 any / mode 为 ANY（A6、B3；any 是值，绝不译成“任何”），automatic → 自动，request → 请求，system instruction 照说，thought signature 照说，thinking models → 思考模型，the search text → 搜索文本（A6），call 1 / call 2 → 第 1 次调用 / 第 2 次调用，a model call → 模型调用，a paid call → 付费调用，token 照说（第 4 讲）。**循环**：loop → 循环，one lap → 一圈，stop rule → 停止规则，final response → 最终回复，reply → 回复，plain text → 纯文本，cap → 上限，turns → 轮，iterations → 迭代，events → 事件，streams events → 以流的形式输出事件，wrapper → 包装函数，the library → 库，framework → 框架，Runner 和 Agents SDK 照写。**ADK**：session 照说（书面“会话（session）”），state → 状态，session state → session 状态，the State tab → State 标签页，history of events → 事件历史，output key 照说（A6），placeholder → 占位符，root agent 照说（A6），validator / planner / summarizer → 校验器 / 规划器 / 总结器，sequential / parallel agent → 顺序 / 并行 agent，dev UI 照说，the agent dropdown → agent 下拉菜单，app name → app 名，identifier → 标识符，telemetry → 遥测，usage data → 使用数据，web server → web 服务器，module / module folders → 模块 / 模块目录，quick start → 快速入门。**MCP**：MCP 照写，the Model Context Protocol → 模型上下文协议，protocol → 协议，custom integration → 定制集成，host、client、MCP server 照说（remote MCP server → 远程 MCP server，FastMCP server，文件系统 server），toolset → 工具集，the filter → 过滤器，child process → 子进程，standard input and output → 标准输入输出，thread → 线程，client process → client 进程，network access → 网络访问。**notebook**：notebook 照说（书面“Colab 笔记本（notebook）”），cell → 单元格，runtime → 运行时，the Secrets panel → Secrets 面板。**harness**：harness 照说（书面也是 harness），outer layer → 外层，gate → 关卡，stamp → 印章，pending / approved → 待批准 / 已批准，approval → 批准，receipt → 回执，claim → 声称，a note → 便条，orchestrator → 编排 agent，specialist → 专家 agent，researcher / editor → 研究员 / 编辑，draft → 草稿，newsletter → 简报，reader → 读者，mock catalog → 模拟清单，classifier → 分类器，label → 标签（A7），handler → 处理函数，if statements → if 语句，else branch → else 分支，structured output → 结构化输出，assembly line → 流水线，hop → 一跳。
- **[A4]** 书面和口语的对应。字幕说 repo / clone / commit / container / image / port / prompt / system prompt / embedding / collection / agent / session / notebook / MCP server / token / pin / lock 文件；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 端口 / 提示词 / 系统提示词 / 嵌入向量 / 集合（collection）/ 智能体（agent）/ 会话（session）/ Colab 笔记本（notebook）/ MCP 服务器（MCP server）/ 词元（token）/ 固定版本（pin）/ 锁文件（lock file），核心概念在那里首次出现时加英文括注（旁白以外可以用括号）。harness 书面也保留英文。repo 作主语时说“这个 repo”。命令不受影响（git clone、uv python pin 3.13 照写）。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符不变）；不翻译、不变形、不加引号，不放进《》或代码格式。需要时加一个中文中心词：docker-shell.sh 这个脚本、.env 文件、llm-rag 目录、docker-volumes 目录、1-baseline 这个名字、get book by author 这个函数、apply confirmation 这个函数、send email 这个工具、finalize 工具、USERS 单元格、--get 命令、docker ps 这条命令。句子不以实物或小写的保留英文词开头：先放一个中文词（这个 agent……；这个 notebook……；这里 system prompt……；在 baseline 里……；而 llm-rag 的 agent……；额外的 ls 显示……；按 Ctrl-C……），这样字幕也不会以小写词开头。产品名、大写缩写和类名（ADK、MCP、LLM、RAG、SDK、Runner、Gemini、Google、OpenAI、Python、Chroma、Compose、Colab、Agentic RAG、Self-RAG、README）可以开头。
- **[A6]** 带下划线的名字（同第 3–5 讲）。没有 say: 时，检查器把显示行当作朗读文本来查，不接受“字母_字母”；SAY 也从不带着下划线读这些名字。所以中文行按旁白的说法写：下划线变成空格，大小写同 SAY，总带一个中文中心词，或放在一个显然是名字的位置；英文只是指一下的地方，就按它的作用称呼。对照：get_book_by_author → get book by author 这个函数；search_content → 搜索文本；tool_config → tool config；mode="any" → mode 设为 any（the enum value ANY → enum 值 ANY；mode ANY → mode 为 ANY）；output_key → output key；mcp_servers → MCP servers 参数（作为 MCP servers 参数传进去，而不是 tools）；tool_filter → 过滤器；needs_confirmation → needs confirmation；apply_confirmation → apply confirmation 这个函数；send_email → send email（工具名；普通动词 sending email → 发邮件）；finalize_itinerary → finalize（SAY 的说法）；root_agent → root agent；GCP_PROJECT → GCP project 变量；GOOGLE_API_KEY= → Google API key 的等号后面；--chunk_type char-split → chunk type 用 char-split（所以 python cli.py --agent --chunk_type char-split 写成“python cli.py --agent，chunk type 用 char-split。”）；mcp_tools、custom_agent 不在 SAY 里。英文行用 en_display 给出字面形式（D4）。等工具链允许显示行保留下划线（I1），就把这些空格形式换回字面形式。
- **[A7]** 要分清的词。笔记本（laptop）↔ notebook（Colab）↔ 记忆（memory，绝不写“内存”）。单元格（notebook 的 cell）↔ 格子 / 那一格（白板的 cell）。组件（课上的 building blocks）↔ 模块（ADK 的模块目录、the ADK module on MCP）。点单（菜单比喻里的 order：第 1 次调用返回一张点单）↔ 顺序（who plans the order：顺序由谁来定）。规划器（课上图里的 planner 节点、深度研究的规划器、baseline 的 TravelPlanner）↔ 课上的旅行规划（S11[5] 的 the lecture's planner，课件 20–22 的旅行例子）↔ 规划（动词：plan a trip → 规划一次旅行）。服务器（web 服务器、服务器日志、停掉服务器）↔ MCP server / FastMCP server / 文件系统 server（MCP 的角色名）↔ 服务（services：十个服务；Compose 的 service）。清单（mock catalog → 模拟清单）↔ 目录（文件夹）↔ 名单（readers' list、9 个名字的名单）。回执（receipt：证明动作发生了）↔ 小票（第 1 讲 lock 文件的比喻，这里不用）。关卡（gate，同第 4 讲的三道关卡）↔ 门（第 4、5 讲发布出去的 host port）↔ 印章（stamp）。标签（分类器给出的 label）↔ 画面上的标签（总带名字：your turn 标签、灰色标签）↔ State 标签页（tab）。密钥（key：API 密钥、服务账号密钥、AI Studio 的密钥）↔ 项（State 标签页里的 entries，绝不写“密钥”或“键”）↔ output key（ADK 的参数名）↔ Google API key（变量名）。token（LLM 的 token）↔ 密钥。回答（模型的回答、answer）↔ 回复（reply：最终回复、三条回复）↔ 函数响应（function response）↔ response 对象（代码里的 response）。调用（call：第 1 次调用、模型调用）↔ 函数调用（function call：模型写出的点单）↔ 工具调用（tool call）。参数（arguments、parameters）↔ 字段（schema 的 fields）。轮（turn：对话的一轮、第 1 轮、12 轮）↔ 圈（lap：只跑了一圈）↔ 迭代（iteration）↔ 一跳（hop）。上限（cap、upper bound）↔ 设上限（给密钥设上限）。占位符（README 地址的占位符、指令里的 {key}）↔ 占位值（GCP project 填的占位值）↔ 占位密钥（placeholder key）。重建（索引或数据库，第 5 讲）↔ 构建（image）↔ 重写（rewrote the book）。批准 / 已批准 / 待批准（approval、approved、pending）↔ 确认（confirmation 只出现在名字 needs confirmation、apply confirmation 里）。拆掉（tear down）↔ 停掉（stop：按 Ctrl-C 停掉服务器）↔ 删除（delete：删掉虚拟环境、删除运行时）↔ 断开连接（disconnect）。prompt（LLM 的 prompt）↔ 提示符（shell 的 prompt：走到这个提示符）。授课老师（the instructor）↔ 课程团队（the staff）↔ 课上（the lecture）↔ 课件（the lecture slides）。
- **[A8]** 语体：助教带实验课。指令简短，用口语动词（跑、装、敲、改、贴、删、拆、选）；称观众为“你”（一对一跟练；绝不用“您”“大家”“同学们”）；“我们”指录制时的我们（我们没有密钥）。中文语序；句子内部可以自由重组，但分句顺序跟着英文（D9）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不堆“一个……的”。不用网络流行语。口语的节奏按意思传达：Here's a question for a cheese expert → 这是一个问奶酪专家的问题；What's missing → 缺的是；Here's the first menu item → 这是第一个菜单项；Now the real function → 再看真正的函数；Two books. → 两本书。；Here's what the staff saw → 下面是课程团队看到的；The staff's answer? → 课程团队拿到的回答呢？；So, who searched your database? → 所以，是谁搜索了你的数据库？；Why? → 为什么？；Now the harness → 现在来看 harness；Back in your Python → 回到你的 Python 里；Ours can't → 我们的不行；First answer: the code → 第一种答案：代码。
- **[A9]** 精确。限定词照译：only 只，every 每个 / 每次，all 全部 / 全都，about 大约，at most 最多，nearly 几乎，never 从不 / 绝不，whenever 只要，at once 马上 / 同时（依上下文：fails at once → 马上就失败；fills its cells at once → 同时填满）。at the time of recording 一律译“录制时”，绝不省略。数量、行号、步骤号、版本号和画面完全一致（C1）。勘误语气温和，后面一定紧跟改法，全部用同一个说法：a small slip → 一个小疏漏（A small slip: → 一个小疏漏：；One small slip: → 一个小疏漏：；Two more slips: → 还有两个小疏漏：；a file name slip in lecture 5 → 第 5 讲里那个文件名的小疏漏；Can you spot the slip? → 你能找出这个小疏漏吗？）。**思考题**（S04[7] 之后、S08[1] 之后、S09[9] 之后、S13[5] 之后、S14[3] 之后；S03[5] 的“找一找”和 S12[1] 的 5 秒停顿也一样）只问不答，措辞不能泄露答案：S04[7] 不能说“两本”，也不能说还能搜到；S08[1] 不能提“没有循环”；S09[9] 不能提 3.15 或“最新的”；S13[5] 不能提大小写；S14[3] 不能说它在人的消息上运行，也不能说“在 agent 启动之前”；S03[5] 不能点出角色对调；S12[1] 不能说“定制集成”。**钱**：Every call is paid → 每次调用都要付费；So far, one paid call → 到目前为止，一次付费调用；all paid → 全都要付费；Every turn is paid → 每一轮都要付费；Web search is billed per call → 网页搜索按次计费（这里是真的按次：它是 OpenAI 托管的搜索）；with billing on → 开通计费；delete or cap the other two keys → 把另外两个密钥删掉，或者给它们设上限。
- **[A10]** 名字。产品、公司和课程名保留拉丁字母（A1 b）；“哈佛”只出现在标题和简介里。课程：AC215；lecture n → 第 n 讲（lecture 5 → 第 5 讲；lecture 7 sketches handoffs → 第 7 讲会简单讲讲交接）；next lecture → 下节课；the lecture → 课上；the lecture slides → 课件；part 1 / part 2 → 第一部分 / 第二部分；this video → 这期视频。the instructor → 授课老师（绝不提名字；On screen we hide the instructor's name → 画面上我们隐去了授课老师的名字）；the instructor's book / story → 授课老师的书 / 故事；the staff → 课程团队；the course's hosted Cheese Agent Tool → 课程托管的 Cheese Agent Tool。书里的作者从不出现（9 个名字只在画面的 enum 面板里）；书用书名或描述（the cottage cheese recipe book → 那本茅屋奶酪食谱；the Woman's Institute book → Woman's Institute 那本书）。故事里的人物 Mara、Anja 照写。两个贯穿全片的问题（describe where cheese making is important in the instructor's book；what's the best cheese for a grilled cheese sandwich?）和 README 的描述（let the LLM decide how to retrieve；search one author's book, or search all books）是旁白自己的话，要翻译；模型写出的搜索文本 cheese making importance location 是画面上的原文，照写。被引用的指令也翻译：follow the assembly line strictly → 严格按流水线来；no embedded URLs → 不要嵌入 URL；expand the search term to a sentence or two → 把搜索词扩展成一两句话。奶酪名用中文（切达、美式奶酪、哈瓦蒂、茅屋奶酪），商店名 Whole Foods 照写；地名用中文（巴黎、加州）。用户名 student 照写；container ID 和 session ID 从不读出来。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（含注释）、README 卡片、Colab 和 ADK 的示意界面、进度条（llm-rag › Agents › step k of N、ADK › Getting Started、Colab · Cheese Quiz › …）、课件标签（Lecture 6 · slides 25–27）、call 1 → your code → call 2 条、图里的标注、印章（PENDING、APPROVED）、标签（your turn、extra、illustration、recorded · the staff's last saved run、expected、stand-in、real run · no key、real run · placeholder key、built, not sent、at the time of recording、erratum、fix · not in the README、your numbers will differ、concept · lecture only、what if · just watch、paid · per call）和思考题卡片都是英文，场景不用为语言做任何改动。所以旁白提到画面上的字时，字幕照画面写：黄色的 your turn 标签（第 2–5 讲）；the gray tag → 灰色标签；the State tab → State 标签页；the Secrets panel → Secrets 面板；Notebook access；Save a copy in Drive。旁白用自己的话说的一律翻译：an extra check → 额外检查，the tracker → 进度条，the agent dropdown → agent 下拉菜单。README 标题照写（Agents 一节、Running Agents 一节）；旁白转述 README 时说“README 里说……”。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、目录、数据库、服务器、网络、内存、磁盘、脚本、视频、用户名、信息、账号、函数、参数、字段、字符串、标识符、单元格、运行时、预览；绝不用 預設、程式、程式碼、檔案、資料夾、資料庫、伺服器、網路、記憶體、磁碟、腳本、影片、使用者、帳號、函式、引數、欄位、字串、識別碼、儲存格、執行階段。
- **[A13]** 系列清单（ac215-video skill 的清单）在这一讲。agent 是主角（47 次，A3）；prompt 和 system prompt（S03、S15，第 5 讲）；embedding 三次（embedding 函数、commit 过的 embedding、embedding 调用）；pipeline 一次（S11[5] 这条 pipeline）；port 很多次（port 8000、8080、8001，第 4、5 讲：发布）；container 两次、image 一次；commit、pull、repo、clone、pin、lock 文件、import 同第 1–5 讲。这份稿子里没说到的：Dockerfile、PATH（只在画面的 no python3 on PATH 里）、endpoint、LoRA、CI、push；volume 只出现在目录名 docker-volumes 里（实物：docker-volumes 目录，绝不写“卷”或 volume）。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（输入 exit、Python 3.12.15、第 429 行、port 8000、8248 个 chunk、2690 美元、1.6 GB、.env 文件、agent 函数、enum 里）。检查器会在每个显示的句子上报告缺少的空格。实物内部的空格保持原样（uv run adk web）；绝不在实物里加空格。紧挨全角标点不加空格（……cd llm-agent-google-adk。、读者，）。@ 符号和汉字之间也加空格（@ 符号后面）。绝不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，紧挨实物也一样（输入 exit。）。列举用“、”（校验器、规划器、总结器）。不用任何括号：（）、()、《》、【】、[]、<> 都不用——没有 say: 时检查器不接受，双语字幕带也不需要括注。“”只用于中文里引用的想法或词；实物、标签名、书名、界面字样、终端原文和模型写出的文本从不加引号。一个中文句子（对应一个英文句子）里不出现 。？！：改用 ，；：（S01[2] 课上问的是一个更大的版本：规划在巴黎的五天……是一个句子）；一个句子里最好只用一个冒号。“第 N 步”“第一题……第五题”后面跟说明时用全角冒号。问句保留 ？。
- **[B3]** 检查器不收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后面跟 !、括号、字母_字母）：绝不抄进中文行，用文字说或换一种写法。mode="any" → mode 设为 any；"mode": "ANY" → mode 为 ANY；GOOGLE_API_KEY= → Google API key 的等号后面；LLM plus reasoning, instructions and tools → LLM 加上推理、指令和工具；Ctrl+C → Ctrl-C（第 4 讲）；{key} 占位符 → 占位符；从来不需要写 8000:8000（说 port 8000）。允许并照画面保留的：路径和文件名里的 . 和 /（.env、.env.example、.adk、baseline.agent、response.text、cli.py），localhost:8000 里的 :，参数和名字里的 -（--agent、--load、--get、--port 8080、--version、1-baseline、char-split、gpt-4o、Ctrl-C），@（@ 符号后面），%。

### C. 数字、版本号与单位

- **[C1]** 显示文字里的数字。凡是和画面、终端、代码、课件或 SAY 里的阿拉伯数字呼应的，一律用阿拉伯数字，不加千位分隔符，和终端打印的一样（8248、1505、3509、1269、2690、6000）：步骤号（第 1 步、第 6 步）、轮次（第 1 轮……第 4 轮）、调用编号（第 1 次调用、第 2 次调用）、通道和插头编号（第 1 条通道、第 3 个插头）、行号（第 429 行、第 478 行）、数量（10 个段落、9 个名字、11 本书、178 个 chunk、1505 个 chunk、8248 个 chunk、24 个、4 个子问题、11 次调用、3509 个字符、247 和 1269 个 token、12 轮、16 次迭代、7 项、189 个包、14 个工具、最多 2 轮审查、3 个城市、6 家酒店、5 个搜索工具）、port 8000 / 8080 / 8001、406、版本号、大小、时间、钱、日期。SAY 写成单词的小的叙述性数量和序数用汉字：三步、两个密钥、五天、五个组件、三条通道、三种方式、两行、两次调用、三样东西、两本书、四个词、两个 container、三类、十个服务、三个插头、三个 LLM agent、三条回复、三项、三次模型调用、六个模块目录、四个目录、两条规则、两条无害的警告、两件事、五次搜索、四次编辑调用、四位读者、两位、三个工具、三个错误、第一部分 / 第二部分、第一题……第五题、第一种 / 第二种 / 第三种答案、第一个菜单项。英文 Ten passages came back（句首写成单词，画面上是 10）→ 返回了 10 个段落。
- **[C2]** 单位、版本号、模型 ID 和日期。大小照画面写，加半角空格：1.6 GB、3 GB。时间：大约 40 秒、不到 3 秒、39 秒、13 秒。钱：2690 美元，上限 6000（dollars → 美元；绝不换算成人民币）。版本号带名字：Python 3.12.15、uv 0.13.1、CPython 3.15.0、CPython 3.13、Python 3.10 及以上、Python 3.14、ADK 1.8 及以上、ADK 2.12.0、2.12 版、旧版本 1.27.5。模型 ID 照代码写，中英两行一致：gpt-4o、gemini-2.5-flash、gemini-3.1-flash-lite、gemini-2.0-flash（第 5 讲 C2；英文行用 en_display，D4）。日期：2026 年 10 月 18 日（October 18, 2026）、9 月 22 日（September 22）。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。narration/*.yaml 里，script.md 的每个 SAY 行对应一个条目（153 段）；`en` 和 SAY 行逐字节相同；`zh` 的条目数和 explainer.voice.split_sentences 切出的英文句子数完全相同（这份稿子一共 337 句）。只在一个句子内部重组；绝不合并或拆分句子。短句也单独成一项：Starting fresh? → 从头开始？；Kept that database? → 那个数据库还留着吗？；Two books. → 两本书。；Why? → 为什么？；The staff's answer? → 课程团队拿到的回答呢？；Test yourself. → 自测一下。；Install Node. → 安装 Node。；Now the harness. → 现在来看 harness。；That's the gate. → 这就是关卡。；Now the real function. → 再看真正的函数。；What ends the loop? → 循环靠什么结束？。运行 `python -m explainer.i18n check videos/ac215-l06-agents-1 --lang zh`，直到它打印 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（锚点只用来给中文配音的渲染安排动画节拍）。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示的句子都要通过 explainer.i18n.spoken_problems：不用括号（B2）、不用数学符号（B3）、没有“字母_字母”的名字（A6）、数字后面不跟 !、没有以“种”结尾再跟 ，。！？ 的分句（“最好用哪种奶酪？”可以，“有几种。”不行）、汉字和拉丁字母或数字之间有半角空格（B1）、每个句子以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），并且每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用正则 `[A-Za-z][A-Za-z'.-]*` 切词，长度 1 的不查：gemini-3.1-flash-lite 切成 gemini- 和 flash-lite，gemini-2.5-flash 切成 gemini- 和 flash，gpt-4o 切成 gpt-，.env 切成 env，.env.example 切成 env.example，.adk 切成 adk，1-baseline 切成 baseline，AC215 切成 AC，localhost:8000 切成 localhost，--port 切成 port，Woman's 保持 Woman's，Ctrl-C 保持 Ctrl-C。它报出来的拉丁词，要么是该翻译的英文词（通常如此），要么是漏掉的实物：把实物按同样的切法加进 allowed_spoken_latin，并加进对应的术语。故意不列复数（agents、tools 除外：tools 是参数名；calls、sessions、tokens、notebooks、cells）：报出来的复数是要去掉的英文词形变化（12 轮、三个 LLM agent、247 个 token）。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都要有一个 en_display 项，写出画面上的字面形式，其余和 SAY 句子逐词相同；同一段里的其他句子写 null。念法 → 字面形式（script.md 开头的清单和 review_spoken 第 12 条，加上本表 C2 的模型 ID）：L-L-M rag → llm-rag；L-L-M agent google ADK → llm-agent-google-adk；cd L-L-M rag → cd llm-rag；cd google ADK tutorial → cd google-adk-tutorial；cd L-L-M agent google ADK → cd llm-agent-google-adk；dot env → .env；dot env dot example → .env.example；the root dot env file → the root .env file；dot ADK folder → .adk/ folder；python cli.py, dash dash agent, chunk type char split → python cli.py --agent --chunk_type char-split；python cli.py, dash dash load, chunk type char split → python cli.py --load --chunk_type char-split；An extra get command → An extra --get command；GCP project → GCP_PROJECT；the docker volumes folder → the docker-volumes/ folder；get book by author → get_book_by_author；mode any → mode="any"；mode ANY / the enum value ANY → "mode": "ANY" / ANY；tool config → tool_config；default credentials error → DefaultCredentialsError；response dot text → response.text；O-N-N-X runtime → onnxruntime；sentence transformers → sentence-transformers；uv run ADK web → uv run adk web；uv run ADK dash dash version → uv run adk --version；ADK telemetry disable → adk telemetry disable；localhost 8000 → localhost:8000；dash dash port 8080 → --port 8080；control C → Ctrl+C；Google API key equals → GOOGLE_API_KEY=；1 baseline → 1-baseline；baseline dot agent → baseline.agent；output key → output_key；MCP servers, not tools → mcp_servers, not tools；needs confirmation → needs_confirmation；apply confirmation → apply_confirmation；send email → send_email；the users cell → the USERS cell；MLOps Learning repo → MLOps_Learning repo；GPT-4o → gpt-4o；Gemini 2.5 Flash / 2.5 Flash → gemini-2.5-flash；Gemini 3.1 Flash-Lite → gemini-3.1-flash-lite；Gemini 2.0 Flash → gemini-2.0-flash。带下划线的名字（A6）只在 en_display 里还原成字面形式；中文行保留空格形式。英文版自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只翻译它的英文句子：不加命令、参数、括注、中文界面名或解释；只有英文标明 extra 的地方才说“额外”；保留英文的词不加中文解释（英文行就在正下方）；思考题不加答案（A9）。the project file 就译“项目文件”，不替它补上 pyproject.toml；the quick start 就译“快速入门”，不补 QUICKSTART.md。
- **[D6]** 固定句式。Pause, and do both. → 暂停一下，把两件事都做了。 pause, and get to this prompt → 暂停一下，走到这个提示符 pause, and load yours → 暂停一下，加载你自己的 Pause here, and run step 1 with your key. → 在这里暂停，用你的密钥跑第 1 步。 Pause and tear down. → 暂停一下，把它拆掉。 Pause, and set up yours. → 暂停一下，把你的设置好。 Pause, and get your sync to succeed. → 暂停一下，让你的 sync 跑成功。 Pause, and get the dev UI open on baseline. → 暂停一下，在 dev UI 里打开 baseline。 pause, and plan a trip → 暂停一下，规划一次旅行 Pause, and run the MCP cells. → 暂停一下，把 MCP 的单元格跑一遍。 pause, and run the Guild → 暂停一下，跑一遍 Guild pause, and run the four turns → 暂停一下，把这四轮跑一遍 pause, and run the demo → 暂停一下，跑一遍演示 pause, and run the three lanes → 暂停一下，把三条通道都跑一遍 Pause, and run the seven steps. → 暂停一下，把这七步跑一遍。 pause to run the setup → 暂停一下，把准备工作跑一遍 Pause at each yellow your-turn tag, and run the command. → 看到黄色的 your turn 标签就暂停，自己跑一遍命令。 With your key, look for … → 有密钥的话，要找的是…… With your key, ask the agent to list files. → 有密钥的话，让 agent 列出文件。 An extra check from a second terminal: → 在第二个终端里做一个额外检查： An extra check, … → 额外检查一下：…… An extra one-liner / An extra script / An extra request / Another extra request / Extra curl commands / An extra grep / An extra ls / an extra curl / An extra get command / an extra docker ps / An extra git status → 一行额外的命令 / 一个额外的脚本 / 一个额外的请求 / 另一个额外的请求 / 额外的几条 curl 命令 / 额外的 grep / 额外的 ls / 额外的 curl / 一条额外的 --get 命令 / 再用一条额外的 docker ps / 额外的 git status。 which isn't in the README either → 这也不在 README 里 a question the README doesn't mention → 一个 README 里没提的问题。 Step N: → 第 N 步： Now the agents section, step 1: → 现在是 Agents 一节的第 1 步： Running agents, step 1, … → Running Agents 一节的第 1 步，…… at the time of recording → 录制时。 A small slip … → 一个小疏漏……（A9）。 Here's what the staff saw. → 下面是课程团队看到的。 In the staff's saved run, … → 在课程团队保存的运行里，…… Test yourself. → 自测一下。 One: … Five: → 第一题：……第五题：。 Answers and every command are in the exercises and the study guide. → 答案和每条命令都在练习和学习指南里。 Next lecture: the harness itself. → 下节课：harness 本身。 In part 2, … → 第二部分，…… Part 2: … → 第二部分：……
- **[D7]** 文件。narration/g1.yaml = S01–S08（第一部分：agent 是什么，以及手写函数调用；78 段、172 句），narration/g2.yaml = S09–S16（第二部分：循环归框架管；75 段、165 句），即 video.yaml 的两个 part；每个文件以注释开头（覆盖范围、应用的规则：A6 空格形式的名字、B3 用文字写的符号、C1 不加千位分隔符的数字、C2 模型 ID、D4 en_display、没有 say: / anchors:），并保持稿子的顺序。字符串用双引号；字面的双引号或反斜杠要做 YAML 转义。
- **[D8]** 按英文时间轴的长度。中文是边听英文边读的，字幕带在英文分段切换的地方切换（一段中文如果读起来快于每秒 9 个单位，最多多给 1 秒）。每个中文句子读起来的时间要和英文听起来差不多：经验法则是每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也占长度（llm-agent-google-adk 11 个单位，gemini-3.1-flash-lite 11.6，cheese making importance location 18.2，python cli.py --agent 11.6，adk telemetry disable 11.6）：英文没重复的地方不要重复它们；同一段里第一次提到之后，用简短的指代（这个 repo、这个函数、这条命令、这个模型）。
- **[D9]** 保持英文的分句顺序（系列教训，ac215-video skill）。工具链按分句把中文和英文配对，所以一个以条件开头的中文句子（如果……，就……）会把两个相邻分句的意思对调。条件、目的、时间状语的位置跟着英文走：英文条件在前，中文也在前（if imports fail later, rerun it → 如果后面 import 失败，就……再跑一次）；英文主句在前，中文也让主句在前，或者把条件放进同一个分句、主动词之前不加逗号（So this step fails whenever uv picks 3.15 → 所以这一步只要 uv 选中 3.15 就会失败；replan if it rains or a flight is late → 并且在下雨或航班延误时重新规划；Swap those two roles before comparing → 先把这两个角色对调，再去比较）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文行最多 30 个单位，英文行 96 个字符；纯中文字幕（.zh.srt）每行 22 个单位，每条 2 行。分句写到最多大约 24 个单位，用 ，；： 隔开，让切分器有干净的切点；避免超过 30 个单位却没有标点的分句（单是 cheese making importance location 就有 18.2 个单位：让它单独占一个分句）。
- **[G2]** 字幕条结尾：工具链去掉条末的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。能用中文词收尾时，就不要以“实物 + 句号”结尾（“……把 .env.example 复制成 .env 文件。”和“……复制成 .env。”都有效，前者读起来更稳）。
- **[G3]** 命令绝不拆开。切分器把中文行里两个拉丁词之间的空格当作好的切点，所以 uv run adk web 可能落在两行上，观众就没法照抄。把整条命令放在分句末尾、全角冒号之后（第 3 步：sh docker-shell.sh。；然后安装：uv sync。；修复办法是一条额外的命令：uv python pin 3.13。），每条字幕最多一条命令，周围的中文要少。含有带下划线名字的命令不完整写出：按 A6 拆成命令和说明（python cli.py --agent，chunk type 用 char-split）；一行放不下的命令按 SAY 的说法称呼，让终端和英文行去显示它。在渲染出的 .zh.srt 里检查每一条含命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、部分和章节标题用书面语体（A4：容器、仓库、克隆、智能体、会话、提示词）；问句保留问号；保留英文的冒号结构（第 1 次调用：……；ADK：……；harness：……）；命令、目录名和文件名照写（adk web 小写，同第 1 讲“apt、git 和仓库”；meta.yaml 不受检查，那里可以用括号和下划线）。核心概念的章节带上英文短名，方便搜索，同第 1、3、5 讲：智能体（agent）、会话（session）。LLM: Agents I → LLM 智能体 I（同第 2 讲“容器 I”）；part 1 what an agent is, and function calling by hand → 智能体是什么，以及手写函数调用；part 2 frameworks own the loop → 循环交给框架；the harness → harness。
- **[H2]** 简介（Bilibili / YouTube）：两三句，书面语体，用本词表的术语：这是 AC215 第 6 讲的跟练视频，跟练 dlops-io/llm-rag 的 Agents 一节、dlops-io/llm-agent-google-adk 和三个 Colab 笔记本；观众做了什么、学到什么（基础 LLM、推理工作流和智能体的区别，每次调用都是无状态的信封；函数声明、函数调用、两次调用和 thought signature；agent 循环、停止规则和轮数上限；ADK 的安装、uv sync 在 Python 3.15 上失败和 uv python pin 3.13、目录名、Runner、会话和状态；MCP；三种编排方式；harness：Python 计算的预算、只有人能打开的审批关卡、以磁盘上的回执判定成功）；英文旁白，配中文和中英双语字幕；终端输出录于 2026-10-18，录制时没有任何密钥，所以模型的回答都是课程团队保存的输出，需要密钥的步骤展示命令、真实的报错和该看什么。
- **[H3]** 配套材料：i18n/zh/README.md（以及 exercises.md / digest.md，如果要做的话）用这份词表、书面语体翻译（仓库、克隆、提交、容器、镜像、端口、提示词、系统提示词、嵌入向量（embedding）、集合（collection）、智能体（agent）、会话（session）、Colab 笔记本（notebook）、函数声明、函数调用、函数响应、模型上下文协议（MCP）、MCP 服务器（MCP server）、护栏、上下文工程）；harness 书面也保留英文，首次出现解释一次：harness（套在 agent 外面、由代码执行检查的一层）。那里可以用括号和下划线（不受检查）。标题和 `<summary>答案</summary>` 要翻译。最后附一张术语表：English | 这里用的词 | 常见的其他说法（agent：智能体 / 代理；function calling：函数调用 / 工具调用；thought signature：思维签名；session：会话；harness：外壳 / 驾驭框架；handoff：移交 / 交接；guardrail：护栏 / 防护栏；token：词元 / 令牌）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]** （请求，第 3 讲起一直开着）`explainer.i18n check` 在句子没有 say: 时，把它的朗读检查（_SPOKEN_BAD：括号、数学符号、“字母_字母”的名字）用在显示行上。对只有字幕的视频（这个系列；video.yaml 里没有 languages.zh.voice，词表写的是 voice: none），这些检查保护不了什么，反而逼出了 A6 和 B3（这一讲最多：get_book_by_author、tool_config、mode="any"、output_key、mcp_servers、needs_confirmation、apply_confirmation、send_email、GOOGLE_API_KEY=、Ctrl+C）。建议：词表的 voice 是 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。那时 A6 和 B3 就变成：字面形式照抄。
- **[I2]** （待办，来自第 1 讲 I3）`explainer/subtitles.py` 的 `_cuts` 把中文行里拉丁词之间的空格当作好的切点，所以命令可能被拆开（G3）。建议：在中文行里，把只由空格隔开的一串拉丁词当作不可拆分的整体，除非它单独就超过一行。
