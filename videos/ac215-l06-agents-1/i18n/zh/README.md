# 中文字幕说明

视频 *AC215 · Lecture 6 — LLM: Agents I (follow-along: llm-rag, llm-agent-google-adk)*
（**AC215 · 第 6 讲：LLM 智能体 I（跟练：llm-rag、llm-agent-google-adk）**）是英文旁白，配中文字幕和中英双语字幕，
没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 6 讲的跟练视频，跟的是三份教程材料：
[dlops-io/llm-rag](https://github.com/dlops-io/llm-rag)（`main` 分支，提交 `e17a39f`）的 Agents 一节，外加它依赖的
第 5 讲三步；[dlops-io/llm-agent-google-adk](https://github.com/dlops-io/llm-agent-google-adk)（`main` 分支，提交
`f89faa7`）的整份 README（Getting Started、Running Agents）；以及三个 Colab 笔记本（notebook）：Cheese Quiz、
Travel Planner 和 Cheese Newsletter · Harness。视频分两部分：

- **第一部分：智能体是什么，以及手写函数调用**（S01–S08）。先在 Cheese Quiz 里用同一个模型跑三条通道（一次普通的
  LLM 调用、由 Python 安排顺序的推理工作流、自己决定何时停下的智能体（agent）），看清区别在于谁握着方向盘；再看
  每次调用都是一个全新的信封：记忆就是代码放回信封里的纸。然后回到第 5 讲的两个容器，运行
  `python cli.py --agent --chunk_type char-split`，一步步拆开函数调用：手写的函数声明（名字、描述、JSON schema、
  `enum`、必填字段）是给模型的菜单；第 1 次调用里 `mode="any"` 强制模型写出一个函数调用（点单）；你的 Python
  按名字分发、真正执行检索；第 2 次调用把问题、原封不动的模型那一轮（带着 thought signature）和函数响应一起发回去。
  最后从两次调用推到 agent 循环：停止规则、轮数上限，以及为什么 llm-rag 的 agent 只跑了一圈。
- **第二部分：循环交给框架**（S09–S16）。用 Google 的 Agent Development Kit（ADK）：`uv sync` 在 uv 选中
  CPython 3.15 时失败、用额外的 `uv python pin 3.13` 修好，`uv run adk web` 和 ADK 能接受的目录名，Runner、
  会话（session）、状态和事件（状态是一块共享的白板，`output_key` 和指令里的占位符）；用 MCP（模型上下文协议）
  接上不是你写的工具：以子进程启动、通过标准输入输出通信的文件系统 MCP 服务器，和按 URL 连接的远程 MCP 服务器；三种编排多个智能体的
  方式（顺序写在代码里、由模型决定、由 Python 读取模型给的标签）；最后用 Travel Planner 和 Cheese Newsletter
  两个笔记本讲 harness（套在 agent 外面、由代码执行检查的一层，下一讲的主题）：由 Python 计算的预算、只有人在下一轮
  明确回答 yes 才能打开的审批关卡、以磁盘上的文件回执判定成功，以及为什么只写在提示词里的规则不等于检查。

画面上的终端输出、代码面板、README 引文、Colab 和 ADK 的示意界面、标签（`your turn`、`extra`、`recorded`……）、
进度条和课件标签都是英文原样，方便你对照着敲；只有旁白译成了中文。录制时（2026 年 10 月 18 日）没有任何密钥：
Docker、Chroma、uv、ADK 的 web 服务器和两个 MCP 服务器都是真实运行的；每次模型调用要么没发出去就停了，要么被
拒绝了，所以模型的回答都是课程团队保存的输出，需要密钥的步骤展示命令、真实的报错，以及有密钥时该看什么。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l06-agents-1.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l06-agents-1.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l06-agents-1_part1.*`、`_part2.*` | 第一部分（S01–S08，手写函数调用）和第二部分（S09–S16，循环交给框架），各有自己的视频、字幕和章节文件 |
| `output/ac215-l06-agents-1.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l06-agents-1.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l06-agents-1.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文（字幕用；g1 = 第一部分 S01–S08，78 段旁白、172 句；g2 = 第二部分 S09–S16，75 段、165 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（L-L-M rag、dash dash agent、chunk type char split、dot env、get book by author、mode any、Google API key equals、control C、GPT-4o、Gemini 3.1 Flash-Lite），英文行换回屏幕上的写法（`llm-rag`、`--agent`、`--chunk_type char-split`、`.env`、`get_book_by_author`、`mode="any"`、`GOOGLE_API_KEY=`、`Ctrl+C`、`gpt-4o`、`gemini-3.1-flash-lite`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L06-agents-1.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L06-agents-1.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l06-agents-1 --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l06-agents-1 --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l06-agents-1 --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或地点放在句末，中文就不把“如果……”“当……时”
提到句首，否则相邻两条双语字幕的中英文会互相错开。命令放在分句末尾、全角冒号之后，这样字幕切分不会把一条命令
拆到两行上。

## 译文风格

按中国 MLOps 助教带实验课的说法，和第 1–5 讲一致：

- **一字不改**：你要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、包名、模型 ID、代码里的名字和值、
  报错原文、Colab 和 ADK 界面上的字样、README 章节标题，以及模型写出的搜索文本 cheese making importance location）。
  字幕检查器不收的几种写法例外：带下划线的名字按旁白的念法写成空格，再加一个中文中心词（get book by author 这个函数、
  tool config、output key、MCP servers 参数、apply confirmation 这个函数、send email），检查器不收的符号用文字说
  （`mode="any"` 写成“mode 设为 any”，`GOOGLE_API_KEY=` 写成“Google API key 的等号后面”，`Ctrl+C` 写成 Ctrl-C）；
  英文行通过 `en_display` 保留原样。模型 ID 中英两行一致，照代码写（`gemini-3.1-flash-lite`）。
- **保留英文**：实验课上本来就说英文的词，第 1–5 讲的 repo、clone、commit、pin、lock 文件、import、container、image、
  pull、pipeline、port、localhost、API、ID、token、chunk、embedding、collection、prompt、system prompt、LLM、agent，
  这一讲新增 notebook、session、schema 和 JSON schema、enum、temperature、system instruction、thought signature、
  SDK、MCP 里的 host / client / server、harness、wheel、dev UI。
- **其余用中文标准术语**（Google Gemini、ADK 和 MCP 中文资料里的译名，方便搜索）：工具、工具调用、函数调用、函数声明、
  函数响应、分发器、参数、字段、必填、循环、停止规则、最终回复、上限、迭代、轮、事件、状态、记忆、指令、组件、
  动态控制、决策者、规划器、编排、推理引擎、推理工作流、思考模型、模型上下文协议、定制集成、子进程、标准输入输出、
  工具集、过滤器、web 服务器、标识符、遥测、占位符、单元格、运行时、护栏、成功标准、审批、回执、交接、深度研究、
  上下文工程。
- **比喻按意思译，一个比喻一个词**：方向盘、通道（沿用第 5 讲）、信封和纸、菜单和点单、封印、替身（第 5 讲）、
  轮毂和辐条、白板和格子、插头、流水线、关卡和印章、回执、便条。
- **分清容易混的词**：笔记本是 laptop，Colab 的 notebook 照说；memory 是“记忆”，绝不写“内存”；菜单比喻里的 order
  是“点单”，“谁来定顺序”的 order 是“顺序”；notebook 的 cell 是“单元格”，白板的 cell 是“格子”；`mode="any"` 里的
  any 是值，绝不译成“任何”；State 标签页里的 entries 是“项”，不是密钥；课上的 building blocks 是“组件”，ADK 的
  module 是“模块”。
- **精确**：录制时会变的版本号一律带“录制时”（Python 3.12.15、uv 0.13.1、CPython 3.15.0、ADK 2.12.0）；教程里的
  勘误统一说“一个小疏漏”，后面紧跟改法；凡是调用模型的地方都说清楚要付费（每次调用都要付费、网页搜索按次计费）；
  思考题只问不答；授课老师从不提名字。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、克隆、提交、端口、提示词、系统提示词、智能体（agent）、
  会话（session）、Colab 笔记本（notebook）、MCP 服务器（MCP server）；harness 书面也保留英文。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)（其中提到的“读法”“朗读”规则来自第 1 讲的中文配音版，这个系列只用英文旁白，
不再适用）。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| agent | agent（字幕）；智能体（书面） | 代理、智能代理 |
| function calling / function call | 函数调用 | 工具调用 |
| function declaration | 函数声明 | 函数定义、工具定义 |
| function response | 函数响应 | 函数返回值、工具结果 |
| dispatcher | 分发器 | 调度器 |
| thought signature | thought signature | 思维签名、思考签名 |
| agent loop / stop rule | agent 循环 / 停止规则 | 智能体循环 / 终止条件 |
| session | session（字幕）；会话（书面） | 会话 |
| state / memory | 状态 / 记忆 | 状态 / 内存（误译） |
| Model Context Protocol (MCP) | 模型上下文协议（MCP） | 模型上下文协议 |
| MCP server | MCP server（字幕）；MCP 服务器（书面） | MCP 服务端 |
| orchestrator | 编排 agent | 编排器、协调者 |
| handoff | 交接 | 移交、转交 |
| guardrail | 护栏 | 防护栏、安全护栏 |
| harness | harness | 外壳、驾驭框架 |
| context engineering | 上下文工程 | 语境工程 |
| temperature | temperature | 温度 |
| token | token（字幕）；词元（书面） | 令牌、标记 |
| notebook | notebook（字幕）；Colab 笔记本（书面） | 笔记本 |
