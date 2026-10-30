# 中文字幕说明

视频 *AC215 · Lecture 7 — LLM: Agents II (follow-along: agent-harness)*
（**AC215 · 第 7 讲：LLM 智能体 II（跟练：agent-harness）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 7 讲的跟练视频，跟的是
[dlops-io/agent-harness](https://github.com/dlops-io/agent-harness)（`main` 分支，提交 `e25dfe9`）的整份 README
（Setup and verification、第 1–7 节和 Troubleshooting），以及课程的 Colab 笔记本（notebook）Agent Harness。教程不要你
自己写智能体（agent）：它直接给你一个带五个工具的 OpenAI 模型，放在一家虚构的奶酪店里（什么都不会真的买、真的寄，
也不会真的发邮件），然后一幕一幕地在它外面加代码。这层代码就是 harness（模型外面那层由代码执行的循环、限制、上下文
和检查），贯穿全片的规则来自课程的笔记本：**模型提议，harness 决定**。视频分两部分：

- **第一部分：一个智能体**（S01–S07）。开头是同一个模型、同一套工具给出的两份回答，其中一份把预算的逗号写错了位置，
  却是唯一一份由代码检查过购物车的回答。然后是环境准备：一个不发布任何端口的 Docker 容器、上一级的空 `secrets` 目录、
  导出 OpenAI 密钥（或者离线时跳过）、`bash docker-shell.sh`；离线验证：`check_sdk`、281 个测试、模型检查，以及
  Colab 这条路。第 1 幕用真实数字拆开 agent 循环（六次模型调用，消息从 1 条涨到 11 条），说明 `preview_order` 为什么
  不能下单，再给它套上四个 harness 层（Trace、Budget、Context、CartCheck）和拆不掉的内环（调用准入、工具审计、
  店铺规则），把每一行输出归到课上的行动边界里。第 2 幕比较 basic 和 enriched 两种上下文：由 Python 筛选的上下文包
  放在一条 user 消息里，标明是数据，不是指令；筛选能缩小范围，但校验说了算。
- **第二部分：harness 接管**（S08–S16）。第 3 幕的下单路线是一张边归 Python 管的工作流图，只有一个节点交给模型；
  经理批准的是一个 SHA-256 指纹，绑定这一辆购物车，结账时还要重新校验。第 4 幕是一个有五种状态的规划器：压缩、
  每次调用前重新钉上的状态胶囊、被隔离的恶意供应商文档，以及只由宿主程序写入的记忆。第 5 幕用渐进式披露加载
  技能（skill）：技能只提建议，从不执行。第 6 幕让一个智能体把第 3 幕的整个工作流当作工具来调用：两次批准，只有一个
  订单下单成功。评测部分用 `--list-runs`、`--inspect-run`、一批测试夹具（fixture）运行、报告和 HTML 记分卡，以及只改
  一处提示词的 A/B 对比（`--compare`）拿出证据，并说清自动检查证明不了什么。最后是清理和回顾。

画面上的终端输出、代码面板、README 引文、示意的 Colab 界面、行动边界表、思考题卡片、标签（`your turn`、`extra`、
`scripted`、`recorded`……）、进度条和课件标签都是英文原样，方便你对照着敲；只有旁白译成了中文。录制时（2026 年
10 月 20 日）没有 OpenAI 密钥：镜像构建、281 个离线测试以及每一条离线和脚本模拟（`--fixture`）的命令都是真实运行的
（录制时是 Python 3.13.16、agent-framework 1.19.0，默认模型 `gpt-5.6-luna`）；每一条在线命令都运行到第一次模型调用，
停在 OpenAI 对 README 占位密钥返回的 401；模型的回答来自课程团队保存的 Colab 运行（标签 `recorded`）和 README 自己的
描述（标签 `expected`）。两位顾客的 ID 在画面上遮住了，字幕里只说“第一位顾客”“第二位顾客”。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l07-agent-harness.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l07-agent-harness.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l07-agent-harness_part1.*`、`_part2.*` | 第一部分（S01–S07，一个智能体：准备、循环、harness 层与上下文）和第二部分（S08–S16，harness 接管），各有自己的视频、字幕和章节文件 |
| `output/ac215-l07-agent-harness.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l07-agent-harness.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l07-agent-harness.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文（字幕用；g1 = 第一部分 S01–S07，68 段旁白、148 句；g2 = 第二部分 S08–S16，87 段、191 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（dash dash compare、build agent、Cart Check、harness without trace、approval mode always require、220 dollars 80、GPT 5.6 Luna、docker ps dash a、Inspect run），英文行换回屏幕上的写法（`--compare`、`build_agent`、`CartCheck`、`harness.without("trace")`、`approval_mode="always_require"`、`$220.80`、`gpt-5.6-luna`、`docker ps -a`、`--inspect-run`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L07-agents-2-harness.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L07-agents-2-harness.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l07-agent-harness --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l07-agent-harness --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l07-agent-harness --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或原因放在后面，中文就不把“如果……”“当……时”提到
句首，否则相邻两条双语字幕的中英文会互相错开。命令和报错原文放在分句末尾、全角冒号之后，这样字幕切分不会把它们
拆到两行上（唯一的例外是 `python cli.py --act 1 --scenario standard`：它比纯中文字幕的一行还长，会在同一条字幕里
折成两行）。渲染之后，在 `.zh.srt` 里再看一遍每条带命令的字幕。

## 译文风格

按中国 MLOps 助教带实验课的说法，和第 1–6 讲一致：

- **一字不改**：你要输入、要在屏幕上对照的东西（命令、参数、场景和模式的值、label、文件名和目录名、类名和层名
  Trace、Budget、Context、CartCheck、代码里的值 approve、decline、null、终端原文 Maximum of 8 model calls reached、
  Invalid or unauthorized、UNRESOLVED、BLOCKED、DECLINED、事件名 approval.requested、order.placed、包名和模型 ID、
  店里数据中带重音符号的奶酪名 Comté、Époisses、Bûcheron、Colab 界面上的字样 Save a copy in Drive、Notebook access，
  以及 README 的标题 Inspect the context first）。字幕检查器不收的几种写法例外：带下划线的名字按旁白的念法写成空格，
  需要时加一个中文中心词（build agent 这个函数、preview order 工具、get stock、load skill、read skill resource、
  build act 4、run ID），检查器不收的符号用文字说（`approval_mode="always_require"` 写成“approval mode 设为
  always require”，`"order_placed": False` 写成“order placed 设为 false”，`harness.without("trace")` 写成
  “harness without trace”，`$220.80` 写成“220.80 美元”）；英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，封闭清单：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的
  container、image、base image、pull、port、API、ID、token、Dockerfile；第 5 讲的 prompt、system prompt、LLM、agent、
  CLI；第 6 讲的 notebook、session、schema、SDK、harness；这一讲新增 trace、skill、fixture、label、diff、run ID。
- **其余用中文标准术语**（中文 agent 工程资料里的译名，方便搜索）：工具调用、循环、轮、层、环、准入、审计、预算、
  兜底、上下文、上下文工程、上下文包、校验、重新校验、验证、工作流、图、节点、边、修订、结账、批准、审批、审批单、
  指纹、哈希、回执、经理、宿主程序、规划器、记忆、压缩、截断、上下文窗口、胶囊、隔离、白名单、元数据、渐进式披露、
  管理者模式、交接、评测、测试用例、测试集、基线、批次、记分卡、混杂改动、评委、结果、轨迹、成本。
- **比喻按意思译，一个比喻一个词**：两栏、环和内环、闸机、接缝、筛子、通道（沿用第 5、6 讲）、轨道和站、抽屉、胶囊、
  说明书和钥匙、手和插座、回执（第 6 讲）。
- **分清容易混的词**：笔记本是 laptop，Colab 的 notebook 照说，合成的 notes 是“笔记”；live 是“在线”（真的调用模型、
  按 token 计费），offline 是“离线”，绝不写“实时”；scripted 是“脚本模拟”；API key 是“密钥”，“技能是说明书，不是钥匙”
  里的 keys 是“钥匙”；店里的 manager 是“经理”，课上的 manager pattern 是“管理者模式”；顾客的 request 是“需求”，
  API 和工具的 request 是“请求”；validate 是“校验”，verify 是“验证”，recheck 是“重新检查”；trust label 是“信任标注”，
  “标签”留给画面上的 tag；trajectory 是“轨迹”，rails 是“轨道”；memory 是“记忆”，绝不写“内存”；应用的 state 是“状态”，
  美国的 state 是“州”；README 的 Act 是“幕”。
- **精确**：录制时会变的版本号和模型 ID 一律带“录制时”（Python 3.13.16、agent-framework 1.19.0、`gpt-5.6-luna`）；
  教程里的勘误统一说“一个小疏漏”，后面紧跟改法；打印出来的结局照屏幕写（最后是 UNRESOLVED，不是 BLOCKED；
  结果：DECLINED；status 为 saved）；思考题只问不答；两位顾客只说“第一位顾客”“第二位顾客”，他们的 ID 和名字不出现
  在任何字幕里；授课老师从不提名字。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、克隆、提交、端口、提示词、系统提示词、智能体（agent）、
  会话（session）、Colab 笔记本（notebook）、技能（skill）、执行记录（trace）、测试夹具（fixture）；harness 书面也保留
  英文。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)（其中提到的“读法”“朗读”规则来自第 1 讲的中文配音版，这个系列只用英文旁白，
不再适用）。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| harness | harness | 外壳、驾驭框架 |
| agent | agent（字幕）；智能体（书面） | 代理、智能代理 |
| context engineering | 上下文工程 | 语境工程 |
| compaction | 压缩 | 上下文压缩 |
| progressive disclosure | 渐进式披露 | 逐步披露 |
| allowlist | 白名单 | 允许列表 |
| trace | trace（字幕）；执行记录（书面） | 链路追踪、轨迹记录 |
| skill | skill（字幕）；技能（书面） | 技能 |
| fixture | fixture（字幕）；测试夹具（书面） | 固定装置 |
| eval set | 评测集 | 评估集 |
| LLM as judge | 让 LLM 当评委 | LLM 评委、LLM 裁判 |
| handoff | 交接 | 移交 |
| token | token（字幕）；词元（书面） | 令牌 |
| memory | 记忆 | 内存（误译） |
