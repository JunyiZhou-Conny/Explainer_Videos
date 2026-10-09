# 《这些讲解视频是怎么做出来的》中文版词表（中英混用版）

视频：*How these explainer videos are made: one human, one AI agent, and a lot of measuring*（`videos/how-these-videos-are-made`，13:40）  
受众：B 站上好奇的普通观众，不需要编程或机器学习背景（英文版的前提也是这样）  
口吻：一位自己做这类工具的中国工程师，讲给朋友听  
第一个用途：英文原片烧录中英双语字幕（中文在上，英文原句在下），即 B 站的标准上传版 `output/<id>.zh-en.mp4`。以后的中文配音版也读同一套文件。  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改）

## 为什么这样中英混用

- 名字保留英文：人名、产品名、工具名（Claude Code、Manim、3Blue1Brown、Andrej Karpathy、Kokoro、edge-tts、faster-whisper、FFmpeg、jieba、LaTeX、Azure AI Speech）。中国工程师就是这么说的，译了反而搜不到。
- 被当作“字符串”引用的东西保留原样：旧井字棋代码里等待的“A hundred”“A million”，声音测试里的 noise、epsilon 和识别模型听成的“Nice”“Excellent”，S05 的英文单词 example，S08 里英文旁白的回答“No”。它们就是画面上和测试里真实出现的字。
- 三个工程词保留英文：commit、lint、bug。中国开发者跟外行说话时也说英文；“提交”会被理解成“提交表格”，“代码检查”说不出是哪个工具。视频第一次说到时在同一句里解释一次。
- 其余一律说普通话，用中文科技媒体和普通观众熟悉的说法：智能体、子智能体、工作流、流水线、工具包、脚本、渲染、语音识别模型、合成语音、评审、截图、帧、交互页面、论文笔记、认知卸载。
- 双语字幕把英文原句放在每一行中文下面，所以中文行里不给中文术语加英文括注。

## 总原则

普通话为主，只在中文使用者本来就说英文的地方保留英文。每个词问三件事：这种场合里真实的中国人怎么说；一个外行能不能听懂（视频引入它的地方解释一次）；同一个东西在另外两期中文版（`tictactoe-255168`、`dwork2006-calibrating-noise`）里怎么说，就怎么说。英文脚本的硬性规定原样适用：用户从不出现姓名；用户的话忠实翻译，不增不减；费用只和完整说明一起出现，中文说明的意思必须完全一致；每个数字都准确；英文脚本里的措辞护栏（模拟的 12 岁孩子、识别模型听成了、还没有记录、183 个子智能体来自 46 次工作流运行且都在这期之前）有固定的中文说法（规则 A8）。

## 用户的决定（必须遵守）

- **不出现姓名。** “the user” 一律是“用户”，第一次（S02）是“这位用户”。不用“他”或“她”：英文说 they / their 的地方，重复“用户”或用“自己”（用户说，AI 很有耐心，可自己却在做大量的“认知卸载”）。
- **用户的话忠实翻译。** 英文引用或转述用户英文原话的地方（S02 第 2、3 条旁白，S11 第 2 条），中文只译这些话，不增不减。如果某处引用的是用户的中文原话，就一字不改地用原话。本片里没有这种情况：用户的四个请求都是英文写的（`assets/quotes.yaml`；中文版的请求 A06b 也是英文打字），所以这里每一句中文都是翻译。S02 和 S08 对请求的概括仍是第三人称概括（用户要求……），不是引语。
- **费用说明的意思不变。** 屏幕上的说明 "API list-price equivalent for the whole session up to Oct 7 · all four requests, not the cost of one video" 译为：**整个会话截至 10 月 7 日、按 API 公开标价折算的金额 · 涵盖全部四个请求，不是一期视频的成本**（两行，在 · 处分开）。S03 的旁白：屏幕上的费用，是整个会话截至 10 月 7 日的花费，按公开的按量计费价格计算：涵盖全部四个请求，不是一期视频。金额本身不读出来，在简介里也只和这条完整说明一起出现。
- **数字一个不改。** 见规则 C1。

## 术语表

“字幕”是显示用的写法；“朗读”是以后中文配音要说的内容，和字幕相同时留空。

### 人与角色

| English | 字幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| the user | 用户；这位用户（S02 第一次） |  | S02：一切从一个人开始，也就是这位用户 | 不出现姓名，不用他/她。 |
| one human / people | 一个真人；人；只有人能做的事 |  | S03：团队：一个真人，就是用户 | “真人”只用在和 AI 智能体对比的地方。 |
| AI | AI；一个 AI | AI |  | 这个语境里说 AI，不说“人工智能”。 |
| AI agent(s) / the agent | AI 智能体（第一次）；智能体 |  | S01：这些视频里几乎所有东西都是 AI 智能体做的 | 规则 A2。不用“代理”，不保留 agent（英文行里已经有）。 |
| sub-agents | 子智能体 |  | S03：它手下有 183 个子智能体，来自 46 次工作流运行，都在这期视频之前 | 给出 183 / 46 时，一定带上“都在这期视频之前”。 |
| Claude Code | Claude Code | Claude Code | S03 | 产品名。 |
| reviewer / review | 评审；评审意见；一轮又一轮的评审 |  | S01：发现问题的评审 | 人和动作都叫“评审”；不用“审稿人”。 |
| director | 导演 |  | S07 |  |
| a simulated 12-year-old / simulated viewer / test viewer | 一个模拟的 12 岁孩子；这个模拟的孩子；模拟观众；试看观众 |  | S07 | sharp but ordinary → 聪明但普通。 |
| cross-scene reviewer | 跨场景检查的评审 |  | S07 |  |
| fixers / skeptical verifiers | 负责修改的智能体（修改者）；持怀疑态度的核查者 |  | S09 | 各有四个，是复数；英文说 one 时才用“有个修改者 / 核查者”。 |
| Andrej Karpathy | Andrej Karpathy | Andrej Karpathy | S02：本项目的想法来自 Andrej Karpathy 的帖子，是第一个请求里引用的 | 拉丁字母（同差分隐私那期的人名规则）；as quoted → 引用的。 |
| 3Blue1Brown | 3Blue1Brown | 3Blue1Brown | S02：视频的风格学的是 3Blue1Brown | 频道名；不说它的制作量有多大。 |
| Dan / Dev | Dan；Dev | Dan / Dev | S07 | 卡片上的真实名字。 |

### 流水线

| English | 字幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| pipeline | 流水线；整条流水线 |  | S01 |  |
| toolkit | 工具包 |  | S03：它写了驱动整条流水线的工具包 |  |
| workflow / workflow run | 工作流；一次工作流运行 |  | S03：工作流就是智能体为了启动子智能体写的程序，每个子智能体只干一件事 | 中文里已经通行（各种 AI 工具都叫“工作流”），外行也听过。 |
| script (script.md) / a workflow script | 脚本；工作流是……写的程序 |  | S01 | “脚本”只指视频脚本；工作流的 script 说“程序”，两者不会撞。 |
| show line / say line / beat | 一行画面；一行台词；每一小段 |  | S04：每一小段都是一行画面配一行台词 | 画面上是真实的英文脚本（SHOW:/SAY:），英文行也写着 show line / say line，中文说它们是什么。 |
| the voice / synthetic voice / Mandarin voice / English-first voices | 语音；合成语音；普通话声音；以英语为主的声音 |  | S03：每种语言各一个合成语音 | “语音”指生成的音频，“声音”指测试里的某一个声音；不用“配音”（像真人配音）。 |
| narration | 旁白 |  | S01 |  |
| speech recognizer | 语音识别模型；识别模型 |  | S03：以及一个语音识别模型 | 不读 ASR。护栏：识别模型把……听成了……。 |
| commit | commit；项目存下的版本 | commit | S03：一百多个 commit 里，除了两个，全是它提交的，commit 就是项目存下的版本 | 保留英文（A1）；解释紧跟在后面，顺序和英文一样。 |
| lint | lint；一个叫 lint 的检查工具 | lint | S06：有个叫 lint 的检查工具，一帧都不画就能把每个场景跑一遍 | 保留英文（A1）。 |
| bug | bug；工具的 bug；内容的 bug | bug | S07：导演还抓到一个更隐蔽的 bug | 日常中文就说 bug；不用“漏洞”（安全漏洞）或“故障”。 |
| render / draft / final cut | 渲染；重新渲染；草稿；成片 |  | S06：工具包先快速渲染一版草稿 | 剪辑软件里人人见过“渲染”。 |
| frame / still / grid / fingerprint | 帧；截图；网格图；每一帧的指纹 |  | S06 | 联系表（contact sheet）里的小图叫“截图”。 |
| scene / scene code / clip / footage / sources | 场景；场景代码；片段；画面；源文件 |  | S04 | “片段”是渲染好的场景视频。 |
| animation cue | 动画触发点；钉在某个具体的中文词上 |  | S08 | “触发点”让没做过动画的人也明白它的作用。 |
| hand-set shifts / word times | 手动设的偏移；每个词的时间 |  | S05 |  |
| usage limits / reset | 用量上限；额度恢复 |  | S03 |  |
| session / request(s) | 会话；请求；第一个请求 |  | S02、S03 | 一律“请求”，和费用说明（全部四个请求）一致；不用“需求”。 |
| paper / PDF / catalog / digest | 论文；PDF；目录记录；给论文编目录；论文笔记 | PDF | S03：用户上传了 36 个 PDF | “论文笔记”同差分隐私中文版简介。 |
| comments | 注释 |  | S03 | 同井字棋词表。 |
| subtitles / subtitle tool / line breaks | 字幕；字幕工具；断行；中英双语字幕 |  | S08、S10 |  |
| test cases / grammar tool / hand-written rules | 测试用例；语法分析工具；手写的规则 |  | S10 |  |
| playground / interactive | 交互页面（一个可以自己动手试的小网页）；能交互的东西；交互 |  | S10：前两期视频各配了一个交互页面，也就是一个可以自己动手试的小网页 | 两期中文版的 playground.html 都叫“交互页面”。 |
| licensed | 有授权的语音；免费的中文语音 |  | S10 |  |
| polish / points / changes / corrections | 润色；条意见；处改动；处更正 |  | S09 |  |
| a Manim pitfall | Manim 的一个坑 | Manim | S07 | 规则 A10。 |
| 画面上的其他工具（不读） | Kokoro；edge-tts；faster-whisper；FFmpeg；jieba；LaTeX；Microsoft Edge；Azure AI Speech |  |  | 名字，保留。 |
| prompt / review instructions（只在画面上） | 评审指令（提示词） |  |  | 旁白不说；留给以后的画面翻译。 |

### 用户的话

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| neural net / hardship / mentor / never isolated | 神经网络；训练它是要吃苦的；导师；从来不是孤立的 | S02 | 规则 A5。 |
| cognitive offloading | 认知卸载（S02 第一次加引号） | S02：可自己却在做大量的“认知卸载”：让 AI 替自己思考 | 中文心理学的标准术语；旁白紧接着解释（让 AI 替自己思考），和英文一样。画面上的引语卡片保持英文。 |
| vision | 设想 | S10：也最接近用户的设想 |  |

### 和另外两期共用

| English | 字幕 | 说明 |
|---|---|---|
| tic-tac-toe / games / marks / orders | 井字棋；255,168 种对局；棋子；24 种顺序 | 同井字棋词表 A8：数“有多少种不同的对局”用“种”。 |
| nine factorial | 九的阶乘 | 这一句讲的是“用文字写出来”，所以写汉字；井字棋那期的字幕写“9 的阶乘”。 |
| X / O / the letter O / a zero | X；O；字母 O；数字 0 | O 读“欧”。 |
| the privacy video / digest / budget bar | 差分隐私那期；差分隐私论文的笔记；隐私预算条 | 绝不说“隐私视频”（规则 A7）。 |
| 被引用的字符串 | “A hundred”；“A million”；英文单词 example；noise；epsilon；“Nice”；“Excellent”；“No” | 画面上或测试里真实出现的字。 |
| Pause for a moment / Pause and try it / Pause and think / Pause on this one | 先暂停一下；暂停一下，自己试试；暂停想一想；这里暂停想一想 | 卡片标题是“暂停想一想”（explainer/locales/zh.yaml）。 |

### 标题（meta.yaml）

| English | 中文 |
|---|---|
| 视频标题 | 【幕后】这些讲解视频是怎么做出来的：一个人、一个 AI 智能体，和大量的测量 |
| S01 Made by something that can't watch it | 做视频的，却看不了视频 |
| S02 What the user asked for | 用户想要什么 |
| S03 Who did what | 谁做了什么 |
| S04 A script that is code | 脚本就是代码 |
| S05 The audio is the clock | 音频就是时钟 |
| S06 Checking without eyes or ears | 没有眼睛和耳朵，怎么检查 |
| S07 Reviewers who pretend | 会扮演角色的评审 |
| S08 Same video, second language | 同一个视频，第二种语言 |
| S09 Bugs in the machinery | 工具链里的 bug |
| S10 What to improve next | 下一步改进什么 |
| S11 A recipe, and a request | 一份配方，和一个请求 |

## 规则

### A. 用词与中英混用

- **A1** 保留英文的范围：（a）人名、产品、工具和服务的名字；（b）被当作字符串引用的词：“A hundred”“A million”、noise、epsilon、“Nice”“Excellent”、example、“No”；（c）PDF 和 AI；（d）封闭清单 commit、lint、bug。新词要加入（d），必须同时满足：中国开发者跟外行说话时也说英文；中文说法有歧义或生硬（“提交”像“提交表格”，“代码检查”说不出是哪个工具）；旁白在同一句里解释一次。不为“洋气”加英文（不要“这个 pipeline 很 robust”）。
- **A2** 智能体一族。agent → 智能体；第一次（S01、S03）说“AI 智能体”，之后说“智能体”；sub-agents → 子智能体；fresh agents → 全新的智能体；agents cataloging the papers → 给论文编目录的智能体。为什么不保留 agent：“智能体”是中文科技媒体和行业的标准说法，外行也认识，而每条字幕下面的英文行都写着 agent。智能体用“它 / 它们”，不用“他”。
- **A3** 被引用的字符串放在中文引号里，拼写不变：旁白念到“A hundred”，就显示一百；识别模型把脚本里的 noise 听成了“Nice”；简短地答了一句“No”。英文里不带引号的词，中文里也不加：脚本里的 noise；英文单词 example。旁白里不翻译画面上的代码和名字。
- **A4** 用户。见上面“用户的决定”。“one human” → 一个真人（和 AI 智能体对比时）。Andrej Karpathy 保留拉丁字母，并保留“引用”的限定：本项目的想法来自 Andrej Karpathy 的帖子，是第一个请求里引用的。
- **A5** 用户的话。见上面“用户的决定”。对照：our brain is a neural net → 我们的大脑就是一个神经网络；training it takes hardship → 训练它是要吃苦的；cognitive offloading → 认知卸载（S02 第一次加引号）；a mentor → 导师；never isolated → 从来不是孤立的；AI should not just be cognitive offloading → AI 不应该只是认知卸载。
- **A6** 和另外两期一致：井字棋；数不同的对局用“种”（255,168 种对局）；棋子；顺序；九的阶乘；差分隐私；隐私预算（条）；交互页面；论文笔记；暂停想一想；中英双语字幕。
- **A7** “the privacy video” → 差分隐私那期（中文版 → 差分隐私的中文版；digest → 差分隐私论文的笔记）；“the tic-tac-toe video” → 井字棋那期。绝不说“隐私视频”：中文里像在说私密视频。“a privacy paper” → 一篇讲隐私的论文。
- **A8** 措辞护栏（英文脚本的硬性规定）的中文固定说法：a simulated 12-year-old → 一个模拟的 12 岁孩子（指这个角色时绝不只说“12 岁孩子”；S01 的 pretending to be a 12-year-old → 假扮成 12 岁的孩子）；the speech recognizer heard "Nice" where the script said noise → 识别模型把脚本里的 noise 听成了“Nice”（主语是识别模型），绝不说“声音说成了……”；no record yet of anyone checking it by ear → 目前还没有记录显示，有人亲耳检查过……；every test viewer on record → 有记录的试看观众；183 sub-agents in 46 workflow runs, before this video → 183 个子智能体，来自 46 次工作流运行，都在这期视频之前；passed all 17 test terms → 17 个测试词全部通过（绝不说“全部读对”）；fixers / verifiers 是复数 → 负责修改的智能体 / 持怀疑态度的核查者；most of them polish → 大多是润色。AI 评审不用感知动词（看、听、看懂）：labels it couldn't decode → 它读不懂；唯一的例外是 S06 故意的“它就是这样‘看’视频的”，和英文一样带着反讽，加引号。
- **A9** 费用。见上面“用户的决定”。
- **A10** 语气。口语、友好、具体，像工程师讲给朋友听：短分句，中文语序，不要翻译腔（不要“让我们……”“这就是为什么……”，不要一串“一个……的”）。“Manim 的一个坑”的“坑”是中国开发者说“陷阱”的日常用词，外行也从“踩坑”里认识它；此外不用网络用语（不要 yyds、一键三连、锅）。称呼观众用“你”；S11 的请求要客气（请在评论区说一声）。只用大陆简体（视频、程序、软件、默认、渲染）。

### B. 排版与标点

- **B1** 空格（同另外两期）。汉字和拉丁字母、阿拉伯数字之间加一个半角空格（AI 智能体、36 个 PDF、12 岁、10 月 7 日、lint 的检查工具、Manim 的一个坑）。全角标点旁边不加空格（念到“A hundred”，、3Blue1Brown：），数字和 % 之间不加（15.3%），数字和名字内部不加。不用 U+00A0。
- **B2** 标点。中文用全角 ，。、；：？！“”‘’……《》；引号用于被引用的字符串和第一次出现的新词（“认知卸载”）；、只用于短的名词并列。一句中文里没有 。？！（一句英文对一句中文），用 ，；： 代替。分句的长串列举用 ，，字幕才能在项目之间断开（S01 第 5 条、S10 第 2 条）。如果英文那半句只能在冒号处断开（英文列表里的逗号不算断点），名词列表就放在 ： 后面用 、，并在中间加一个 ，，好让纯中文字幕换行（S04 第 1 条：这条流水线是一串文件：论文、目录记录、带页码的论文笔记，再到脚本、动画代码和视频。）。
- **B3** 字体（以后翻译画面时用）。用工具链配的 Noto Sans / Serif CJK SC；中文不用斜体，粗体可以。

### C. 数字

- **C1** 每个数字都准确，单位和英文一样。英文旁白用阿拉伯数字的地方、或者数值本身重要的地方，用阿拉伯数字（183、46、36、255,168、36 个里有 4 个、82、30、25、5、4、24、17、103、75、12、15%、16 个小时、11 分钟、20 处、10 月 7 日）；255,168 保留逗号，和井字棋那期一致。英文旁白为了配音把小数拼成单词的地方，中文字幕用阿拉伯数字（2.2 秒、15.3%），英文行用 en_display 显示同样的数字（G2）。英文用单词写的小数目，中文也用汉字（六个小时、三个多小时、大约两天、六次、两次、四次、六个子智能体、第一天、四个请求、五种、三轮、将近两秒、每两秒、五分之一秒）。S05 的“About three seconds: three hundred sixty-two thousand, eight hundred eighty”写成汉字（三十六万两千八百八十），因为这一句讲的就是这个数念出来有多长。
- **C2** 算式用文字说：4 乘 3 乘 2（同井字棋词表 C2），不写 ×。

### D. 旁白文件

- **D1** 逐句对齐（explainer/i18n.py）。narration/g1.yaml（S01–S04）、g2.yaml（S05–S08）、g3.yaml（S09–S11）：每条 SAY 一个条目（46 条），en 和 SAY 逐字节相同，zh 按 explainer.voice.split_sentences 一句对一句（164 句），每句以 。？！ 结尾，句中没有。只在一句之内调整结构。检查：`python -m explainer.i18n check videos/how-these-videos-are-made --lang zh`。
- **D2** 英文原片的双语字幕不需要锚点和 say:（时间来自英文语音）。做中文配音版时再加：场景代码里每个句中 vo.wait_until 短语，只要中文语序变了，就加锚点（用 grep wait_until scenes/*.py 列出来）；凡是语音要读的和显示的不一样，就写 say:（F3）；再做一遍时长检查（`python -m explainer.script videos/how-these-videos-are-made/script.md --lang zh`，每个 SAY 块和英文相差不超过 ±15%）。
- **D3** 内容一致。每句中文只说英文那句说的，不多不少。仅有的补充是中文观众需要、英文听众本来就有的信息：两期视频的名字（差分隐私那期、井字棋那期）、S09 的那个“不是”（画面上 that no 指的那个中文词）、example 前面的“英文单词”。

### E. 画面文字（strings/*.yaml，还没写；只有中文配音版需要）

- **E1** 用本词表的说法。标签：本视频重新绘制（re-created for this video）、旧草稿，按保存的代码重绘（the old draft, redrawn from its saved code）、想法 · 尚未实现（idea · not built yet）、尚未验证（not yet verified）；引语署名：— 用户（口述；已删去口头禅）、— 用户（中文版请求）；请求卡片：请求（摘要）；费用说明见 A9。真实的展品（代码、截图拼版、英文引语卡片、英文脚本）保持原样：翻译过的卡片就不再是真实的东西了。

### F. 语音（只用于中文配音版）

- **F1** 声音用 edge zh-CN-XiaoyiNeural（工具链默认）。发布的视频必须走有授权的 Azure AI Speech API（设置 AZURE_SPEECH_KEY 和 AZURE_SPEECH_REGION），绝不用免费的 Edge 端点（见 docs/LANGUAGES.md、CLAUDE.md）。
- **F2** 渲染前做语音识别回环：每一句用 faster-whisper（语言 zh）转写，标出没有原样回来的保留英文词：Claude Code、Manim、3Blue1Brown、Andrej Karpathy、PDF、commit、lint、bug、A hundred、A million、example、noise、epsilon、Nice、Excellent、No、Dan、Dev、AI。commit、lint、bug、3Blue1Brown、A hundred 和 No 都还没用 Xiaoyi 测过。然后在发布前请一个人逐句听一遍。
- **F3** 可能需要的 say:（要实测，不要预设）：3Blue1Brown 也许要写成“3 Blue 1 Brown”；2.2 秒和 15.3% 在另外两期里都读对了（52.5%）；九的阶乘不需要。say: 里不能有括号、数学符号和下划线（explainer.i18n check 会查）。

### G. 字幕

- **G1** 双语字幕（explainer/subtitles.py）：中文在上（每行最多 30 个单位，汉字算 1，拉丁字母算 0.55），英文原句在下；英文原片里时间跟着英文语音走，某一段中文要是读得比每秒 9 个单位还快，会从相邻一段借最多 1 秒。分句最多约 24 个单位，之间用 ，/；/：；绝不在名字、数字和量词（36 个 PDF、255,168 种对局）或被引用的字符串中间断开。英文句子会在中文断开的地方断开，取最近的、相匹配的分句点，而且绝不在列表里的逗号处断开。所以：中文分句的顺序要跟着英文走（S03 的 commit 解释放在 commits 后面；S08 识别模型把 noise 听成了“Nice”，把 epsilon 听成了“Excellent”，顺序和英文一样）；中文的断点要有英文的断点对得上（冒号对冒号，S04、S07）；日期、数字和单位、主语和谓语不能跨断点（“截至 10 月 7 日”“改过的场景”留在同一段）；每段的阅读速度最好不超过每秒约 7.5 个单位（工具只在超过 9 时才调整）。纯中文的 .zh.srt 每条字幕最多两行，每行 22 个单位：长句中间要有一个 ，。每次改动后把 output/<id>.zh-en.srt 和 .zh.srt 从头到尾读一遍：`python -m explainer.build videos/how-these-videos-are-made --subs-only --crf 25`（成片是用 --crf 25 拼接的；不加的话时长取自原始场景渲染，后面每条字幕会移动约 1 毫秒）。
- **G2** en_display（每句的英文字幕行）只用在英文 SAY 为了配音把小数拼成单词的地方："the biggest 2.2 seconds"（S05 第 5 条第 1 句）和 "15.3 percent longer"（S09 第 3 条第 6 句）。其余都显示 SAY 原句，和英文原片自己的字幕一样。
- **G3** 对英文字幕的副作用。explainer/subtitles.py 的 `_en_terms()` 会读所有 videos/*/i18n/zh/glossary.yaml 的 en 字段，把每个 2–3 个词的写法（按 / ; , : 分开）变成英文断行和断字幕时不拆开的词对，对所有视频都起作用。本词表新增的词对只出现在本片的旁白里（已对照所有 script.md 检查），而且没有一个改变英文原片自己的 .srt（--subs-only --crf 25 之后逐字节相同）。单独写 "privacy budget bar" 时改变过一条字幕（S07：Another reviewer found the privacy budget / bar drawn five different ways. 变成了两条），所以那一项的 en 字段写成 "the privacy budget bar"（4 个词，不计入）。以后改 en 字段时要重新检查。

### H. 标题与简介

- **H1** 标题见上面的标题表。章节标题用平实的中文，只有名字保留英文。
- **H2** 简介（meta.yaml）写给标准上传版（英文原片 + 双语字幕）：讲了什么；README 里的诚实说明（用户从不出现姓名；用户原话只删去口头禅；费用只和完整说明一起出现；重绘的画面都有标注；旁白还没有真人逐句听过）；请观众带时间点留言。做中文配音版时，“制作说明”里关于旁白的那一行要改（见 meta.yaml 里的注释）。

## 还没定 / 需要人来确认

- 智能体 还是 agent：本表选了“智能体”（外行能懂、和英文行互补）。如果目标观众更偏开发者，可以考虑全片改成 agent，要整体改，不能混用。
- commit、lint、bug 用 Xiaoyi 读得怎么样，还没测（F2）。
- “Manim 的一个坑”的“坑”：口语里很自然，但如果审片的人觉得太随意，可以改成“Manim 的一个常见陷阱”（字幕会长 3 个字）。
- 需要一位双语审阅者和一位目标观众通读一遍字幕（docs/LANGUAGES.md 第 6 步）。
