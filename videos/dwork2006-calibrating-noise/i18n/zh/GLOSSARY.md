# 差分隐私论文视频中文版词表（中英混用版）
视频：*Calibrating Noise to Sensitivity — the paper that invented differential privacy*（`videos/dwork2006-calibrating-noise`）  
受众：刚接触差分隐私的 RL、ML、医学影像方向研究生和研究者；风格是中国博士生在 B 站讲论文  
语音：edge `zh-CN-XiaoyiNeural`（工具链默认，commit 875166f；发布版走官方 Azure AI Speech，见 F1）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改）
## 为什么要中英混用
- 中国的 DP/ML 研究者讲论文时本来就中英混着说：“这个 query 的敏感度”“一个 trick”“交互式的 setting”“这篇 paper”。这些词硬译成“查询请求”“技巧”“设定”，听起来反而像教科书在念稿。
- 但混用只在真实的人会这么说的地方才自然。已有标准中文名、观众也这么说的概念（差分隐私、敏感度、隐私预算、拉普拉斯机制、噪声尺度、相邻数据库、随机响应）一律说中文，这样也能直接搜到中文教材和论文。
- 观众是 DP 新手。curator、odds 这类词，RL 和医学影像方向的学生用英文也不熟，保留英文没有好处，反而多一道坎。
- 双语字幕（中文在上、英文原句在下）已经把每个英文原词放在中文正下方，所以中文行不再加英文括注。英文只在三处由旁白说出来（差分隐私、敏感度、隐私预算），把最核心的三个名字和英文文献接上。
- 中文语音会读错一部分英文和多音字。两轮实测后，几个听起来自然但读不稳的说法换掉了：row 的“行”（被读成 xíng）、bin（被读成“病”）、log、odds、拉丁拼写的 epsilon。这两轮用的是早先的声音（Xiaoxiao、Yunxi）；后来改用 Xiaoyi，这些改写全部保留，因为它们本来也是更自然的中文。
## 总原则
用一位中国博士生在 B 站讲论文时的流利普通话，只在这样的人真的会说英文的地方说英文。观众是刚接触差分隐私的 RL、医学影像方向研究生。每个选择都要过三关：这个场合的真实说话人怎么说；领域里标准、可搜索的中文名（首次出现时引入一次）；普通话语音（edge zh-CN-XiaoyiNeural）不会读错。（1）保留英文的：符号和变量（显示字形；ε 读“艾普西隆”，其余字母读英文名）；人名、产品、缩写、会议和论文标题；以及一张很短的封闭清单，都是 DP/ML 研究者口头说英文、语音也读得稳的词：query、counting query、mask、trick、hybrid argument，原文自己的用词 transcript 和 leakage，另外 paper、setting、clip 只用于口头（标签写论文、设定、裁剪）。（2）其余概念一律用中文，采用中文 DP 文献的术语：差分隐私、敏感度、隐私预算、拉普拉斯机制、噪声尺度、机制、相邻数据库、统计距离、隐私损失、随机响应、本地化差分隐私、组合定理、成员推理攻击、重构攻击、数据管理者（curator）、记录（row）、桶（bin）、对数（log）、先验/后验概率比（odds）。最后五个替换了草稿里没过受众关或语音关的英文。（3）双语字幕在每行中文下面放英文原句，所以中文行不加英文括注。例外：旁白在三处说出英文（差分隐私、敏感度、隐私预算）；少数只在字幕里出现的短括注，给保留英文的词配中文（transcript（交互历史）），或给出教材别名（相邻数据库（也叫相邻数据集））。（4）工具链的约束也是规则的一部分：每个英文句子对应一个中文句子（共 259 句）；约 400 个锚点要保持动画同步；显示文字和应读内容不同时必须写 say:。用大陆简体中文；书面语（论文、标签、标题、文档）用规范中文，口语轻松，像组会讲论文，但不用网络流行语。
## 相对草稿的主要改动
- **curator → 数据管理者**（简称“管理者”）：新手观众不说 curator，中文 DP 文献写“可信的数据管理者”。S11 结尾改为“让可信的管理者留在回路里”。
- **row：“行” → “记录”**（n 条记录，每人一条；只差一条记录；什么才算一个人的一条记录？）。早先的两个 edge 声音（Xiaoxiao、Yunxi）在多数语境把“行”读成 xíng（转写成“型/形”），“一条记录”每次都读对，也是教材原话。草稿禁用“一条记录”，现在反过来。
- **bin → 桶**：早先的两个声音都把 bin 读成“病”，而这个视频满是“病人”。
- **log → 对数**，**odds → 先验/后验概率比**（贝叶斯那句改为“后验概率比等于先验概率比乘上这个比值”）：log、odds 都读不稳；“几率”在日常中文里就是“概率”；“旧”会被听成“就”。
- **ε 的朗读**：显示仍是 ε，say: 里写“艾普西隆”（26/26 读对；拉丁 epsilon 只有 6/18 读对）。草稿禁止写“艾普西隆”，现在只禁止出现在显示文字里。e 写成大写 E。
- **counting query 口头用英文**：“计数”每次都被读成/听成“技术”。字幕括注一次“计数查询”。
- **transcript 保留英文**，括注改成“交互历史”：“交互记录”会和“记录”（= row）撞车。
- **中文字幕行不再加英文括注**（英文行就在下面）。只保留三处口头英文（差分隐私、敏感度、隐私预算）和两类只在字幕里的短括注：给保留英文的词配中文（query（查询）、mask（掩码）等），给中文术语配教材别名（相邻数据库（也叫相邻数据集）、统计距离（即 TV 距离）、ε-不可区分性（即 ε-差分隐私））。
- **术语改成文献主流写法**：本地化差分隐私、成员推理攻击、重构攻击（“重建”对医学影像观众是图像重建）、输入扰动 / 输出扰动、高级组合定理、开放问题。
- **去掉误导性译法**：sanitize 不译“脱敏”（脱敏是遮盖标识符，正是视频批驳的做法），改为“做隐私处理”；中文句子里不出现英文 private；“越敏感的问题”改为“敏感度越高的 query”；privacy violation 译“侵犯隐私”，和 leakage（泄露量）分开。
- **口语更地道**：引用原文用词时说“原文”（原文管它叫 leakage）；setting 可以口头说；clip 口头说、标签写“梯度裁剪”；recipe → 公式；ratio test → 比值这一关；fixed rule → 确定性的规则；ε set by policy → 人为选定的；奇偶性为奇 → 有奇数个 1；轨迹比值 trick → 算轨迹概率比时的那个 trick；“想多想一会儿” → “需要多想一会儿”；“来自测一下” → “最后留几道题给大家自测”。
- **口号拆成三句**：隐私，留给个体。/ 准确，留给总体。/ 这就是差分隐私的取舍。（英文三句，对应三个条目。）
- **拉普拉斯机制不说英文**，论文标题不口头意译（S01 本来就超时）；英文名由章节名、回顾卡和简介提供。
- **SuLQ**：改为“只问次线性数量的 query”（次线性的是数量）。
- **卡片**：et al. 保留；F/M 作为模拟数据保留；硬币 H/T 只有在场景改用专用键后才改成“正/反”（全局字符串表会把机制符号 M 和图节点 F、H 一起改掉）。
- **补上工具链约束**：每个英文句子对应一个中文句子（259 句）、约 400 个锚点、时长 ±15%、say: 的写法、edge 语音、字幕宽度单位、字幕切分修复。
- **语音：Xiaoxiao → Xiaoyi**（commit 875166f，见 F1）：Xiaoxiao 读旁白保留的英文词口音很重（noise → Nice、epsilon → Excellent），中英混用就失去了意义；Xiaoyi 的英文词和数字都读得准。针对 Xiaoxiao 定下的改写（艾普西隆、记录、桶、对数、先验/后验概率比、SuLQ 读 sulk 等）全部保留。
- **敏感度是一**：旁白不说“敏感度为一”（“为一”和“唯一”同音，会被听成“唯一”），字幕写“敏感度是 1”；画面标签仍写“敏感度为 1”。
- **小规模随机样本**：S10 的“小随机样本”改为“小规模随机样本”（瓦片两行：小规模 / 随机样本），旁白同样改。
- **视频标题**：【论文精读】差分隐私的开山之作：Calibrating Noise to Sensitivity（TCC 2006）。
## 评审分歧的裁决
裁决标准：这个场合的真实说话人怎么说；领域标准、可搜索的中文名（引入一次）；语音不会读错。

| 议题 | 分歧 | 裁决 | 理由 |
|---|---|---|---|
| query | 教学评审要“查询”；草稿和研究者评审保留 query | 保留 query；字幕括注一次“查询” | DP 研究者口头就说 query；语音读得对；括注提供搜索词 |
| curator | 两份评审要中文；草稿保留英文 | 数据管理者 | 新手观众用英文也不熟；中文 DP 文献有标准说法 |
| transcript | 教学评审要“交互记录”；其他保留英文 | 保留 transcript，括注“交互历史” | 原文用词；“交互记录”会和“记录”（row）撞车 |
| hybrid argument | 教学评审要“混合论证” | 保留英文，括注“混合论证” | 密码学的固定说法，口头常说英文，读证明时会遇到 |
| odds | 两份评审保留 odds；TTS 评审建议改“几率” | 先验/后验概率比 | odds 读不清，“几率”有歧义；这里的 odds 正是两个世界的概率比 |
| bin | 研究者评审保留 bin；教学评审括注“桶”；TTS 评审建议视语音而定 | 桶 | 早先的两个声音（Xiaoxiao、Yunxi）都读成“病”（实测） |
| log | 草稿 log；TTS 评审改“对数” | 对数（显示和朗读都用） | 读不稳；“取对数”同样自然 |
| ε 朗读 | 草稿禁用“艾普西隆”；TTS 评审要求用 | say: 里写“艾普西隆”，显示 ε | 实测 26/26 对 6/18；中文数学课本来就这么读 |
| 中文行里的英文括注 | 草稿、教学评审要加；TTS 评审要删 | 删英文括注；保留中文括注和教材别名；三处口头英文 | 英文行就在下面；括注会占宽度、影响锚点 |
| 拉普拉斯机制的英文 | 教学评审要口头说；TTS 评审反对 | 不口头说；章节名和回顾卡附英文 | 拉普拉斯本身就是音译；英文行和卡片已经显示 |
| 口头 DP、bound | 研究者评审允许 | 不说；setting 可以说 | 英文旁白从不说 DP；“上界”口头也自然；setting 很常用 |
| et al. | 草稿改“等” | 卡片保留 et al.；口头说“和合作者” | 名字下面单独一个“等 2003”像错字 |
| F/M、H/T | 草稿改“女/男”“正/反” | F/M 保留；H/T 等场景改用专用键再改 | 全局字符串表会误改符号 M 和图节点 |
| 口号 | 三种写法 | 隐私，留给个体。/ 准确，留给总体。/ 这就是差分隐私的取舍。 | 英文三句；“留给”通顺；“取舍”是研究者用词 |
| 字幕长度 | 30/22 或 24 | 写作时按 24 单位；代码在 30/22 处切 | 留余量，同时遵守代码 |
| 语音 | Xiaoxiao 或 Yunxi；后来加测 Xiaoyi | Xiaoyi（最初裁决为 Xiaoxiao，commit 875166f 改） | Xiaoxiao 读保留的英文词口音很重（noise → Nice、epsilon → Excellent、Claude → Clark、diverge → Vert），抵消了中英混用；Xiaoyi 对比测试 17/17 个测试词、数字全对，全片回环没有系统性误读；女声，和英文女声、井字棋中文版一致；Yunxi 还漏读过 sensitivity |
## 草稿开放问题的决定
1. **Laplace**：用“拉普拉斯”，不口头说英文。
2. **核心概念**：中文（敏感度、隐私预算、噪声尺度、机制），三处口头英文。
3. **paper 与论文**：口头说 paper，引用原文用词或结论时说“原文”，书面写“论文”。
4. **英文字幕行用数字和符号**：要，手写成 en_display（工具链已支持，I6）；没写 en_display 的句子显示 SAY 原文。
5. **语音**：edge zh-CN-XiaoyiNeural（最初定的是 Xiaoxiao，见 F1）；中文发音词典 explainer/lexicon.zh.yaml（已建，I5）。
6. **x′、f(x)**：读 x prime、f x（实测读对）。
7. **MathTex 里的中文**：工具链已用 XeLaTeX + ctex，直接在 \text{} 里翻译。
8. **字幕末尾标点**：去掉。，、；：，保留？！……（工具链已实现，I2）。
9. **繁体**：只做简体。
10. **屏幕标签是否双语**：默认只写中文；例外见规则 E1。
11. **美国模拟数据**：保留数值、日期、邮编和 F/M，只译表头。
12. **playground.html**：另做一轮，使用本词表。
## TTS 实测摘要
两轮测试（用的是早先的声音）：TTS 评审约 37 句；终稿另测 49 句 × 2 个声音（Xiaoxiao、Yunxi），用 faster-whisper-large-v3-turbo 转写。转写只是代替人耳的近似，标出来的句子仍要人工听。

| 写法 | 结果 | 决定 |
|---|---|---|
| epsilon（拉丁） | 6/18 正确，其余为 Excel/Excellent | say: 写“艾普西隆”（26/26） |
| 行（row） | n 行、只差一行、那一行、改变一行、每人一行 → 型/形 | 改用“记录”（一条记录 6/6） |
| bin | 两个声音都 → “病” | 改用“桶” |
| odds / 旧 | ODS、奥子 / “就” | 先验/后验概率比 |
| log | LOG / Loud | 对数 |
| 计数查询 / 计数 query | 6/6 → 技术 | 口头说 counting query（读对） |
| f(x′) 直接写 | 撇号被吞，读成 FX | say: 写 f x prime |
| query、curator、transcript、leakage、mask、clip、setting、paper、hybrid argument、Differential Privacy、privacy budget、lambda、sigma、delta、DP-SGD | 读对 | 可以保留 |
| trick | Xiaoxiao 有一次 → trip | 保留，人工听（Xiaoyi 回环里都读对） |
| Dwork | Xiaoxiao 有一次 → Work | 人工听，必要时加中文词典改拼（Xiaoyi 回环里读对） |
| SuLQ | 读成“苏LQ” / SoilQ | explainer/lexicon.zh.yaml 改拼为 sulk（Xiaoyi 回环里读作 sulk） |

**改用 Xiaoyi 之后**（commit 875166f）。先做了对比测试：Xiaoxiao 读旁白保留的英文词口音很重（noise → Nice、epsilon → Excellent、Claude → Clark、diverge → Vert），Xiaoyi 17 个测试词和所有数字全部读对。然后把两个视频全部 417 个中文句子（本片 259 句）用 Xiaoyi 合成，再用 faster-whisper large-v3-turbo 转写回来：没有发现系统性误读。剩下标出来的都是 Whisper 自己的问题：长句被截断；同音字（阶乘 → 阶层、艾普西隆 → 艾普希龙）；人名拼法不同（Dinur → De Nair、Kenthapadi → Cancer Party、Talwar → Tover）；把 lambda 写成 λ。另一类是按中文习惯读字母（d 读 di、t 读 ti、E 读 yi），这是普通话数学课的正常读法，不算读错。上表的改写全部保留：它们本来也是更自然的中文。S10 另改了一处，与声音无关：“敏感度为一”的“为一”和“唯一”同音，朗读改说“敏感度是一”（标签仍写“敏感度为 1”）。
## 术语表
“字幕 / 屏幕”是显示用的写法（中文字幕行和画面标签）；“朗读”是声音实际说的内容，写进 narration.yaml 的 `say:`，空白表示与显示相同。“首次出现”给出引入方式；只在字幕里出现的括注见规则 A3。
### 核心概念 / Core concepts
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| differential privacy (DP) | 差分隐私；DP 只用于紧凑标签和复合名称（DP-SGD、用 DP 保护的公开表） | 差分隐私（S01 一次：差分隐私，differential privacy） | S01：它开创了我们今天所说的差分隐私，differential privacy，并在 2017 年获得了哥德尔奖。S12 命名卡片：差分隐私（differential privacy） | 中文：所有中文 DP 教材、课程、报告都这么说。S01 旁白顺带说一次英文（edge 读得很清楚），把中文名和英文文献接上。旁白不说“DP”，因为英文旁白本身从不说 DP。 |
| epsilon-indistinguishability (Definition 1, the paper's name); '-indistinguishable' (Theorem 2 card) | ε-不可区分性；定理里写“满足 ε-不可区分性” | 艾普西隆不可区分性 | S04：这就是原文的定义，原文叫它 ε-不可区分性（即 ε-差分隐私）——括注只进字幕。定义卡：TeX \textbf{定义 1}\quad + ε + “-不可区分性”；定理 2 卡：“定理 2：满足\ ” + ε + “-不可区分性”（显式 TeX 空格，见 B1） | 中文：不可区分性是密码学的标准译名。中文教材只把这个定义叫 ε-差分隐私，所以首次字幕括注这个别名。只有引用原文的陈述（定义 1、定理 2）时才说“不可区分”，我们自己的表述一律说“满足 ε-差分隐私”。 |
| private (adj.) / privately / 'a private mechanism' / 'in private' (coin) | “M 是 ε-private” → M 满足 ε-差分隐私；“统计量是 private 的” → 不泄露隐私；privately → 用差分隐私 / 在差分隐私下；private deep learning → 差分隐私深度学习；in private（掷硬币）→ 私下 |  | S01：发布一个统计量，怎样才算不泄露隐私？ | 按句式译成中文。中文句子里绝不出现英文 private，不用“私有”，也不用“隐私的 + 名词”：统计量本身谈不上“隐私的”，只有发布会不会泄露隐私。 |
| sensitivity, S(f) (L1 / global sensitivity) | 敏感度 S(f)；文档：全局敏感度（global sensitivity，本文即 L1 敏感度） | 敏感度，S f（S01 一次：敏感度，sensitivity） | S01：一个数，叫敏感度，sensitivity；S01 想法卡与 S13 回顾卡：敏感度（sensitivity） | 中文：中文 DP 文献的标准术语。不写“灵敏度”“敏感性”：医学影像方向的观众会把“灵敏度”理解成诊断试验的真阳性率。 |
| 'a more sensitive question needs more noise' (S07) / 'sensitive surveys' (S02, Warner) | S07：敏感度越高的 query，噪声越大（标签：敏感度越高 → 噪声越大；隐私越强（ε 越小）→ 噪声越大）；S02：敏感问题调查 |  |  | 技术含义一律带“度”。单说“越敏感的问题”指话题更敏感（毒品、政治），而 S02 讲 Warner 时恰好要用这个日常含义，两者不能撞车。“噪声越大”是地道说法，“更多噪声”是翻译腔。 |
| query / queries / counting query; question(s) | query（不加复数：很多 query）；counting query；question → 问题；S01/S08/S11 卡片标题 Query 保持英文 | query / counting query / 问题 | S02 SuLQ 句：意思是只问次线性数量的 query（查询）；S06 首次 counting query（计数查询）。括注只进字幕，第二部分首次再注一次 | 英文：DP 研究者口头就说 query、counting query，edge 每次都读对。“计数”每次都被读成/听成“技术”（计数查询 → 技术查询），所以口头用英文复合词。字幕括注一次中文（查询、计数查询），方便搜索。旁白里口语化的 question 仍译“问题”。 |
| mechanism, M | 机制 M | 机制 M | S04：运行这个机制，也就是数据管理者随机作答的规则 | 中文：标准术语（拉普拉斯机制、指数机制）。 |
| Laplace distribution / Laplace noise / Laplace mechanism | 拉普拉斯分布 / 拉普拉斯噪声 / 拉普拉斯机制；记号 Lap(·) 不变 | 拉普拉斯分布 / 拉普拉斯噪声 / 拉普拉斯机制（不说英文） | S07：原文用的是拉普拉斯分布；章节 S07 与 S13 回顾卡：拉普拉斯机制（Laplace mechanism） | 中文：教科书里的人名术语，学生口头就说拉普拉斯。旁白不加英文：拉普拉斯本身就是音译，英文字幕行、S07 章节名和 S13 回顾卡都会显示 Laplace mechanism。文档注明期刊里也写“Laplace 机制”。“not Laplace's fault” → 这不是拉普拉斯噪声的问题。 |
| Lap(S(f)/ε): 'Laplace noise of scale S of f over epsilon' | Lap(S(f)/ε)；尺度为 S(f)/ε 的拉普拉斯噪声 | 尺度为 S f 除以艾普西隆的拉普拉斯噪声 |  | 记号与原文完全一致。 |
| scale (λ, scale parameter) / noise scale | 尺度 λ / 尺度参数 λ / 噪声尺度 | 尺度 lambda / 噪声尺度 | S07：它的宽度由尺度参数 λ 决定 | 中文：概率论标准术语，公式读起来干净：噪声尺度 = 敏感度 / ε。 |
| noise | 噪声 |  |  | 中文。不用“噪音”（那是声音）。 |
| privacy loss | 隐私损失；S04 括号下的标签：t 处的隐私损失 |  | S04：这个比值的对数，就是 t 处的隐私损失；S04 标签：t 处的隐私损失 | 中文：通用术语。S04 的标签和旁白说法一致，由场景分支按中文语序拼成 t + “处的隐私损失”（s04_definition.py，i18n.active()），strings 里已没有 privacy loss at 这个键（规则 E4）。 |
| leakage (the paper's word for ε) | leakage（首次括注：泄露量） | leakage | S04：ε 是人为选定的，原文管它叫 leakage（泄露量） | 英文：旁白在引用原文的用词，所以保留英文，字幕括注中文。edge 读得对。同一场景里的“privacy violation”译“侵犯隐私”，与“泄露量”分开。 |
| privacy budget / budget | 隐私预算 / 预算 | 隐私预算（S09 一次：隐私预算，privacy budget） | S09：所以隐私损失会累加，ε 就像一笔隐私预算，privacy budget；S02 标签：隐私预算 | 中文：中文 DP 文献通用。在第二部分开头命名这个概念时，旁白说一次英文。 |
| neighbors / neighboring databases | 相邻数据库 / 相邻；标签：相邻：只差一条记录 | 相邻数据库 | S04：这样的两个数据库叫作相邻数据库（也叫相邻数据集）——括注只进字幕 | 中文：和原文的 database、画面一致。中文教材几乎都写“相邻数据集”，所以括注一次这个搜索词。“邻居”只作比喻。 |
| database x / dataset | 数据库 x；英文说 dataset 时（S13 医学影像题）用数据集 | 数据库 x |  | 中文。 |
| row / one row per person / one person's row / records | 记录：一条记录；n 条记录，每人一条；Alice 的记录；一个人的一条记录；标签同（n rows → n 条记录；rows needed → 需要的记录数） | 记录（朗读中绝不用“行”表示 row） | S03：持有数据库 x：n 条记录，每人一条 | 中文，按朗读效果选定。早先的两个 edge 声音（Xiaoxiao、Yunxi）大多把表示 row 的“行”读成 xíng（n 行、只差一行、那一行、改变一行、每人一行都被转写成“型/形”），而“一条记录”每次都读对。“记录”也是教材原话（两个数据集只相差一条记录），和原文的 hospital records 一致。“proven in one line”改说“一个不等式就证完了”。 |
| curator / trusted curator / trusted server | 数据管理者（简称管理者）；可信的数据管理者；可信服务器；标签：管理者；“管理者拒绝回答” | 数据管理者 / 管理者 | S03：一台可信的服务器，也就是数据管理者，持有数据库 x | 中文（改动）。RL、医学影像方向的新手不会说 curator（他们只知道“策展人”），中文 DP 文献写“可信的数据管理者”，三份评审里两份要求改。edge 能读 curator，所以这是按受众选，不是按 TTS 选。英文字幕行仍显示 curator。 |
| analyst / attacker / adversary | 分析者 / 攻击者；文档的形式化陈述里 𝒜 写“敌手” | 分析者 / 攻击者 |  | 中文。“敌手”是密码学的书面用语，只用于 digest.md 的形式化定义。 |
| transcript | transcript（首次括注：交互历史） | transcript | S04：分析者能看到的一切，原文叫 transcript（交互历史）；第二部分 S09 首次再注一次 | 英文：原文自己的术语，定理 1 就是关于它的。顺手的中文“交互记录”会和“记录”（= row）撞车，现代中文文献也没有固定译名。edge 读得对。标签保留 transcript t = [a₁, a₂, …]。 |
| paper notation footnote: 𝒯 = transcript, San = sanitizer | 论文记号：𝒯 = transcript，San = sanitizer | （不朗读） |  | 标签写“论文”。原文记号不翻译；不写“脱敏器”。 |
| statistical distance (the paper: 'statistical difference') | 统计距离；文档：统计距离（即总变差距离，total variation distance） | 统计距离 | S05：密码学常常满足于更弱的东西：统计距离（即 TV 距离）——括注只进字幕 | 中文：密码学的说法。ML 观众和 exercises.md 熟悉的是总变差（TV）距离，所以括注一次别名。 |
| ratio / log ratio / log density / on a log scale / ln | 比值 / 对数比值 / 对数密度 / 取对数之后 / 公式里保留 ln；“the log of three” → 3 的对数 | 比值 / 对数比值 / 对数密度 / 取对数之后；ln 3 读“三的对数” | S04：这个比值的对数，就是 t 处的隐私损失 | 中文（草稿用 log，已改）。单独的 log 音节读不稳（被听成 Loud、Lock），而“取对数”在中文数学口语里同样自然。ratio 全片统一为“比值”。 |
| Bayes' rule; new odds / old odds; prior / posterior; likelihood ratio | 贝叶斯公式；new odds → 后验概率比；old odds → 先验概率比；“this ratio” 仍是 比值；文档：odds（几率，即 p/(1−p)）、似然比 | 根据贝叶斯公式，后验概率比等于先验概率比乘上这个比值 | S04 攻击者那句；标签：后验概率比 = 先验概率比 × 比值 | 中文（改动）。odds 在早先的两个声音（Xiaoxiao、Yunxi）里都读不清（被听成 ODS、奥子）；“几率”在日常中文里就是“概率”；“赔率”是博彩赔付。这里的 odds 正好是两个世界的概率之比，而先验/后验是 ML 观众熟悉的说法。不说“旧”（会听成“就”），用“先验”正好避开。文档给出 odds（几率）和似然比，方便搜索。 |
| ratio test ('to pass the ratio test, a mechanism must be random') | 比值这一关；标签：想过比值这一关，机制必须是随机的 |  | S05 | 英文是口语化的 test；“检验”会让人想到假设检验或级数的比值判别法。 |
| composition (theorems); Dwork–Rothblum–Vadhan 'composition: k questions cost ~√k' | 组合定理；DRV 卡片：高级组合：k 个问题的代价 ∼√k | 组合定理 | S12：隐私预算发展成了一套组合定理 | 中文：通用术语；√k 的结果在中文里叫“高级组合定理”。卡片的 Tex 串：“高级组合：$k$ 个问题的代价 $\sim\!\sqrt{k}$”。 |
| exponential mechanism | 指数机制 |  | S12：给每个可能的答案打分，后来成了 McSherry 和 Talwar 的指数机制 | 中文：通用术语。 |
| randomized response / Warner's coin / local differential privacy (local DP) | 随机响应 / Warner 的硬币 / 本地化差分隐私；卡片 Local DP → 本地化差分隐私 | 随机响应 / Warner 的硬币 / 本地化差分隐私 | S02：1965 年，Stanley Warner 提出了随机响应，用于敏感问题调查；S12：就是我们今天说的本地化差分隐私 | 中文：随机响应是 DP 领域的说法。“本地化差分隐私”是中文 LDP 综述和多数期刊论文的写法；文档列出变体“本地差分隐私 / 局部差分隐私”。 |
| (ε, δ) / delta / 'a tiny slack' / Gaussian noise is back in | (ε, δ)-差分隐私 / δ / 一个极小的松弛量 δ；标签：高斯噪声回来了，代价是一个极小的 δ | 艾普西隆 delta 差分隐私 / delta / 一个很小的松弛量 delta | S12 | 记号不变；“松弛量”是优化里的自然说法。标签保持 TeX 片段顺序（文字在前，δ 在后）。文档写：近似差分隐私（approximate DP）、纯差分隐私、高斯机制。 |
| DP-SGD / gradient / clip / per-example gradient / clipping | DP-SGD（仅卡片）/ 梯度 / clip（朗读与字幕）/ 梯度裁剪（标签与文档）/ 每个样本的梯度 | 梯度 / clip / 每个样本的梯度 | S12 旁白：把每个样本的梯度 clip（梯度裁剪）到一定大小以内；S06 标签：差分隐私深度学习：把每个样本的梯度裁剪到 C 以内 | 口头说 clip 是中文 ML 圈的自然混用，edge 读得对；标签和文档写可搜索的“梯度裁剪 / 逐样本梯度裁剪”。不加词形变化（不写 clipped）。DP-SGD、RAPPOR 不进旁白，因为英文旁白也不说。 |
| membership inference (attack) | 成员推理攻击；卡片：成员推理攻击（2017） | 问“某个病人在不在训练集里”的攻击（S12 英文旁白不说术语名） | S12 卡片 | 中文：“成员推理攻击”是中文 ML 安全综述里的主流写法。 |
| reconstruction (Dinur–Nissim attack) | 重构攻击；标签：太多精确答案 ⇒ 重构数据库 | 重构 | S02 | 中文：中文隐私文献的常用说法。对医学影像观众来说，“重建”指 CT/MR 图像重建。 |
| differencing attack / 'our subtraction (attack)' | 差分攻击（章节 S01：差分攻击（differencing attack））；回扣：我们那个做减法的攻击 | 差分攻击 / 我们那个做减法的攻击 | S01 章节名 | 中文 DP 教程正是用“差分攻击”讲这个医院例子。章节名附英文，免得有密码学背景的观众联想到差分密码分析。 |
| interactive / non-interactive; setting; sanitize; one-shot release; published table | 交互式 / 非交互式；setting（朗读、字幕）/ 设定（标签、章节名）；sanitize → 做隐私处理；一次性发布；公开发布的表；标签：交互式：问、答、再问 / 非交互式：只发布一次 | 交互式的 setting / 非交互式 / 做隐私处理 / 一次性发布 | S03：先交代一下 setting；这叫交互式的 setting；发布一张经过隐私处理的表，然后撒手不管，叫非交互式 | 中文 ML 口语到处在说 setting，而口头的“设定”偏向小说设定。DP 发布绝不叫“脱敏”：数据脱敏指遮盖标识符，正是视频里证明会失败的“去掉名字”。 |
| adaptively / refused | 自适应地 / 拒绝回答（标签：拒绝） |  |  | 中文。 |
| hybrid argument / chain trick / trick | hybrid argument（首次括注：混合论证）/ 链式 trick / trick | hybrid argument / trick | S08：这种链式 trick 叫 hybrid argument（混合论证），最后还会再出现；S08 标签：hybrid argument | 英文：密码学固定说法，中文理论圈口头也说英文，观众以后读证明会遇到。括注给出教材译名“混合论证”。trick 是最常见的混用词（一个 trick）。 |
| histogram / bin | 直方图 / 桶（d 个桶、每个桶、第 3 个桶、5000 个桶） | 直方图 / 桶 | S06：把一条记录可能的取值分成 d 个桶 | 中文（草稿用 bin，已改）。早先的两个声音（Xiaoxiao、Yunxi）都把 bin 读成“病”（每个病、5000 个病），而这个视频满是“病人”。“桶”是 CS/DP 的说法（分桶、桶计数），也不会和均匀噪声那里要用的“区间”撞车。 |
| L1 norm / L1 distance | L1 范数 / L1 距离 | L1 范数 / L1 距离（照常书写，edge 读对） | S06：这就是 L1 范数，原文用它衡量一列数的敏感度 | 中英混合，和中文 ML 的说法一致。 |
| dimension / coordinates; triangle inequality | 维度 / 分量；三角不等式 |  |  | 中文：标准术语。 |
| mask / parity / 'an odd number of ones inside their mask' | mask（首次括注：掩码）；奇偶；mask 内有奇数个 1 / 偶数个 1；卡片：有多少条记录在自己的 mask 内有奇数个 1？ | mask / 奇数个一 / 偶数个一 | S11：给每条记录一个自己的 mask（掩码），也就是一组比特位置 | mask 保留英文（ML、CS 圈口头就说，edge 读对）。奇偶照英文旁白直说“奇数个 1”；“奇偶性为奇”是生硬的直译。 |
| bit / bit string / bit flips | 比特 / 比特串 / 比特翻转；标签：d = 8 比特；Pr[比特翻转] |  |  | 中文音译，读音接近 bit。 |
| min cut / 1-sensitive / social network / link | 最小割 / 敏感度是 1（旁白、字幕：所以敏感度是 1）/ 敏感度为 1（只用于画面标签）/ 社交网络 / 边；标签：每条可能的边 = 一条记录（有 / 无） | 最小割 / 敏感度是一 / 社交网络 / 边 | S10 | 中文：“最小割”是算法课的标准术语。朗读说“敏感度是一”，不说“敏感度为一”：“为一”和“唯一”同音，会被听成“唯一”。S06 的“敏感度是 1。”同理。画面标签（1-sensitive、→ sensitivity 1）保留“敏感度为 1”。作定语的“敏感度为 2 的 query”（S09）不受影响。 |
| statistical disclosure control / scramble inputs / scramble outputs | 统计披露控制（短标签：披露控制）/ 输入扰动 / 输出扰动 | 要么扰动输入的数据，要么扰动输出的答案 | S02 | 标签用 DP、PPML 里固定的名词术语（输入扰动、输出扰动）；旁白像英文一样用动词说。 |
| anonymous / anonymized / names removed / de-identification | 匿名 / 匿名化 / 去掉姓名；卡片：“匿名”≠ 匿名；结尾引语：“放心，已经匿名化了。”；文档：去标识化 | 匿名 / 匿名化 |  | 中文。“脱敏”“匿名化”只用来描述视频批驳的那种朴素做法。 |
| raw data | 原始数据 |  | S11、S12 | 中文。 |

### 符号与读法 / Symbols and readings
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| epsilon, ε | ε（U+03B5，与屏幕上 \varepsilon 的字形一致） | 艾普西隆（只写在 say: 里） |  | 显示用字形 ε；朗读写“艾普西隆”，这也是中文数学课的读法。两轮测试里，拉丁字母 epsilon 只有 6/18 被转写成 epsilon（其余是 Excel、Excellent），直接写 ε 也一样不稳；“艾普西隆” 26/26 全对。草稿禁止写“艾普西隆”只适用于显示文字。 |
| e to the epsilon / e to the minus epsilon / e to the n epsilon | e^ε / e^(−ε) / e^(nε) | E 的艾普西隆次方 / E 的负艾普西隆次方 / E 的 n 乘艾普西隆次方 |  | say: 里写大写 E（小写 e 曾被读成“一”）。中文课堂本来就常把 e 读作“伊”，两种读法都能接受。“n epsilon”读作“n 乘艾普西隆”。 |
| lambda λ, sigma σ, delta δ, alpha α, Delta Δ | λ、σ、δ、α、Δ | lambda、sigma、delta、alpha（Δᵢ 只在画面上，不朗读） |  | 这几个拉丁读法 edge 读得对（Lambda、Sigma、Delta 原样转写）。书面不写“拉姆达、西格玛、德尔塔”。 |
| x, x′ (x prime), y, t, f(x), f(x′), S(f) | x、x′、y、t、f(x)、f(x′)、S(f)（撇号 U+2032） | x、x prime、y、t、f x、f x prime、S f |  | 变量按英文字母读。朗读文本里直接写 f(x′)，撇号会被吞掉（读成 FX），所以 say: 一律写 x prime。 |
| n, d, k, C, M, Y, Yᵢ, aᵢ, fₜ | n、d、k、C、M、Y、Yᵢ、aᵢ、fₜ（Unicode 下标） | n、d、k、C、M、Y（下标不朗读，用文字描述） |  | 变量保持字母。 |
| one over n / one over lambda / two over epsilon / S of f over epsilon / d over epsilon / square root of n / one over d of the budget | 1/n、1/λ、2/ε、S(f)/ε、d/ε；根号 n；1/d 的预算 | n 分之一、lambda 分之一、艾普西隆分之二、S f 除以艾普西隆、d 除以艾普西隆、根号 n、d 分之一的预算 |  | 单位分数和小数字分数读“B 分之 A”；符号商读“A 除以 B”。字幕可以写紧凑的 a/b，但 √ 写成“根号”。 |
| minus one over lambda / two sigma / epsilon over twice the sensitivity / one plus epsilon / a ratio of two and a ratio of one half | −1/λ / 两倍 σ / ε 除以两倍敏感度 / 1 + ε / 比值是 2 和比值是 1/2 | 负的 lambda 分之一 / 两倍 sigma / 艾普西隆除以两倍敏感度 / 一加艾普西隆 / 比值是二和比值是二分之一 |  | 数值用“二”，个数和倍数用“两”。 |
| Pr[…] (probability of …) | 画面公式保留 Pr[…]；字幕与朗读改写成“……的概率” | ……的概率 |  | 不按符号读。 |
| setting a parameter: 'epsilon one tenth', 'epsilon one half', 'with epsilon equal to one' | ε 取 0.1 的时候 / ε 取 0.5 / ε 取 1 时（字幕） | 艾普西隆取零点一的时候 / 艾普西隆取零点五 / 艾普西隆取一的时候 |  | 设参数用“取”，“等于”留给公式和定义。say: 里“一”后面绝不直接跟“时”（“等于一时”被听成“等于10”），一律说“……的时候”。 |
| Definition 1 / Proposition 1, 2 / Theorem 1, 2, 3 / Lemma 1, 2 / Section 4 / Example 2 | 定义 1 / 命题 1、2 / 定理 1、2、3 / 引理 1、2 / 第 4 节 / 例 2 | 定义一 / 命题一 / 定理一 / 引理一 / 第四节 |  | 中文数学书面用语。script.md 里方括号中的页码引用不朗读。 |
| percentages / 'X percent sure' / years / decimals | 52.5%、62%；最多有 62% 的把握；2006 年；43.7 | 百分之五十二点五；最多有百分之六十二的把握；二零零六年；四十三点七 | S04、S08 | “X percent sure” → “有 X 的把握”。edge 能正确读普通数字；只有写 say: 时才需要拼成汉字。 |
| about / roughly | 约 / 大约 / 左右（字幕不用 ≈） | 大约 / 左右 |  | ≈ 只用于画面。 |

### 视频里的说法与画面 / Phrases and visuals of this video
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| two worlds / world x / world x′ | 两个世界 / 世界 x / 世界 x′ | 两个世界 / 世界 x / 世界 x prime | S04 | 视频自造的比喻，直译即可。 |
| tent / slope / ramp / gap (between tents) / slide / band | 帐篷形 / 斜率 / 斜坡 / 高度差 / 平移量 / 带（带内、带外）；标签：\|高度差\| ≤ 平移量 × 1/λ；shift/scale → 平移量/尺度 |  | S07 | 画面比喻。S07 的竖直差距统一叫“高度差”；S06 答案的变化叫“变化量”，两个 gap 分开。 |
| uniform noise; Gaussian / bell curve / parabola; tails (of a distribution) | 均匀噪声；高斯噪声 / 钟形曲线 / 抛物线；尾部；标签：拉普拉斯：始终在带内 / 高斯：冲出带外 | 均匀噪声；高斯 / 钟形曲线 / 抛物线；尾部 | S07 | 中文：大家都说“高斯”。分布的 tails 是“尾部”，硬币的 tails 是“反面”。均匀噪声说“在 −10 到 +10 之间均匀分布”。 |
| Good noise must never rule an output out / privacy needs noise whose log density is never steep / Averages hide catastrophes that are rare for each person | 好的噪声，绝不能把任何输出排除在外 / 隐私需要对数密度处处不陡的噪声 / 平均值会掩盖那些对每个人都很罕见的灾难 |  | S05、S07 | 视频的结论句；简短，便于引用。 |
| Privacy for individuals. / Accuracy for populations. / That is the bargain. | 隐私，留给个体。/ 准确，留给总体。/ 这就是差分隐私的取舍。（标签两行：隐私，留给个体 / 准确，留给总体） |  | S08（三个英文句子 → 三个中文条目） | “留给”构成自然的对仗（“给 + 形容词”不通）；研究者说这种权衡用“取舍”（“这笔交易”是直译，还带点不正当交易的意味）。用“准确”，不用“精度”“准确率”。 |
| one definition / one number / one recipe; 'the recipe in the title' | 一个定义 / 一个数 / 一个公式；S07：这就是标题里的那条公式 |  | S01、S02、S07 | 用“公式”，不用“配方”（烹饪或化学用词）：这个 recipe 本来就是公式 Lap(S(f)/ε)。 |
| Calibrate the noise to the sensitivity (title phrase) | 按敏感度校准噪声 |  | S03 | 与“敏感度”一致。 |
| Any fixed rule that ever changes its answer has a jump (like that) somewhere | 任何确定性的规则，只要答案会变，就一定在某处有跳变 |  | S01（旁白与标签） | fixed 指“确定性的”；“固定规则”会被理解成“一成不变的规则”，削弱 S05 的结论。 |
| What makes a statistic private? / How much noise is enough? | 发布统计量，怎样才算不泄露隐私？/ 噪声加多少才够？ |  | S01 |  |
| rounding to the nearest ten / rounding cut / jump | 四舍五入到十位 / 取整分界线 / 跳变 |  | S01 |  |
| ε is set by policy / ε — a choice (policy) / S(f) — a fact about f / 'Epsilon is a choice. Sensitivity is a fact.' | ε 是人为选定的；标签：ε：人为选择（政策）/ S(f)：f 本身的性质 / S(f) 与实际数据库无关；ε 是选择，敏感度是事实 | 艾普西隆是人为选定的 | S04、S06 | “由政策决定”听起来像政府规定了 ε。“政策”只留在标签括号里，也和 RL 的“策略”分开。 |
| trajectory-ratio trick (RL analogy, S09); policy (RL); environment | 算轨迹概率比时的那个 trick；标签：RL：分析者 = 环境（约掉），管理者 = 策略 | 懂强化学习的话，这就是算轨迹概率比时的那个 trick | S09 | RL 圈说“轨迹概率比”，这个 trick 他们从重要性采样里就熟悉；“重要性采样”写进文档，不加进旁白（内容对等）。 |
| same in both worlds: cancels | 两个世界里都一样：约掉 |  | S09 |  |
| noise of typical size two / a rounding error (idiom) / percent of the answer | 噪声一般在 2 左右；图例：噪声一般在 2 左右，不依赖于 n（文字 + n 两段，保持原顺序）；到了 100 万人，这点噪声可以忽略不计；占答案的百分之几 |  | S08 | 不说“典型大小为 2”；这个习语绝不译成“舍入误差”。 |
| Careful with the quantifiers / for every / for at least 2/3 / most / at most / unless / any ONE query | 注意量词 / 对任意 / 至少 2/3 / 大多数 / 最多（不超过）/ 除非 / 单单一个（事先已知的）query |  | S11、S12 | 必须准确翻译，S11 的论点就靠它们。英文大写强调改成给“单个 / 大多数”上色或加粗，绝不用拉丁或全角大写。 |
| Keep a curator in the loop / Want broad accuracy + strong privacy? | 让可信的管理者留在回路里 / 想要大范围的准确，又要强隐私？ |  | S11 结尾 | 呼应“人在回路中”（human in the loop）。 |
| spike in one bin / zoom in / zoom into bin 3 / zoom further | 某个桶冒出一个尖峰，放大看看 / 放大第 3 个桶 / 再放大 |  | S09 |  |
| swap rows one at a time / n swaps / even half ≈ a random poll of all rows | 一次替换一条记录 / n 次替换 / 偶数那一半 ≈ 对所有记录的随机抽样调查 |  | S11 | 用“替换”，不用“交换”（交换指两样东西互换）。 |
| exponentially large / exponential in d / every four extra bits per row doubles the rows | 指数级大 / 随 d 指数增长 / 每条记录每多 4 个比特，需要的记录数就翻一倍；标签：约 3300 万 / 约 6700 万 / 约 1.34 亿 |  | S11 | 让翻倍关系一眼可见。 |
| salt and pepper (mixed like) | 像椒盐一样混在一起 |  | S11 | 观众在图像处理里见过“椒盐噪声”。 |
| map (our map) | 地图 |  | S02：先画一张地图，看看这篇 paper 从哪儿来 | 视频自造的比喻，直译即可。 |
| illustration (tag) / proof idea / Still open | 示意 / 证明思路 / 开放问题 | （标签，不朗读） |  | 中文学界说“still open”就是“开放问题”。 |
| Pause and ponder / Pause the video if you need more time / Pause: / Before I show you, pause: | 暂停想一想（卡片标题，explainer/locales/zh.yaml） | 暂停想一想：……？/ 需要多想一会儿的话，可以先暂停视频。/ 暂停一下：/ 先别急着看答案，暂停一下： | S01 起 | 英文两句，中文就两个条目。“想多想”是口误式的重复；改后的说法是 B 站常用语。 |
| Test yourself / Some questions to test yourself; pause after each / Let's recap / One: … Four: | 自测（标题） | 最后留几道题给大家自测，每道题后面都可以暂停一下 / 我们来回顾一下 / 第一，…… 第四，…… | S13 | 口头的“来自测一下”会被听成“来自”+“测一下”。 |
| In this video / Here is one you can answer yourself | 本期内容 / 这一题你可以自己回答 |  | S01、S08 |  |
| hospital database / patient / condition X / has X / no X / Alice exposed / one week later / with(out) Alice / same answer | 医院数据库 / 病人 / 疾病 X / 有 X / 无 X / Alice 暴露了 / 一周后 / 有 Alice / 没有 Alice / 答案相同 |  | S01 | 统一用口语的“病人”；字母 X 按英文读。 |
| heads / tails (coin); coin glyphs H / T; yes / no; says yes; tell the truth | 正面 / 反面；硬币字形保持 H/T（定稿，见 [E3]）；S02 分支标签：正面 / 反面，结果标签：H → “是” / T → “否”；S04：→“是” / →“否”；“是” / “否”；回答“是”；说真话 | 正面 / 反面；是 / 否（S02：正面答“是”，反面答“否”） | S02、S04 | 分布的 tails 是“尾部”。strings.yaml 里绝不直接映射不带作用域的单个字母 H、T。S04 公式写 '\Pr[\text{回答“是”}\mkern-6mu]'（见 C2）。 |
| study / smokers / heart disease / insurer / stranger; privacy violation / not a privacy breach | 研究 / 吸烟者 / 心脏病 / 保险公司 / 陌生人；侵犯隐私；标签：不算侵犯隐私 |  | S04 | 用“侵犯隐私”，和同一场景里的 leakage（泄露量）分开。 |
| statistic / count / true answer / true count / released answer / output t / noise ÷ answer / pure noise | 统计量 / 计数 / 真实答案 / 真实计数 / 发布的答案（短标签：发布值）/ 输出 t / 噪声 ÷ 答案 / 纯噪声 |  |  | “计数”在画面上没问题；口头用 counting query 代替“计数查询”（同音“技术”）。 |
| privacy level / database size (S08 circled inputs) | 隐私参数 ε / 数据库规模 n |  | S08 |  |
| cryptography conference / define security first, (against every possible attacker,) then prove it | 密码学会议 / 先定义安全性（针对所有可能的攻击者），再去证明 |  | S02 |  |
| Statisticians and data miners | 统计学家和数据挖掘研究者 |  | S11 |  |
| census / US Census Bureau / state totals / counties, tracts, blocks / published tables protected with DP | 人口普查 / 美国人口普查局 / 各州总数 / 县、普查区、普查街区 / 用 DP 保护的公开表 |  | S12 | 官方中文译名。 |
| income cap / cap every value at $1M / largest income | 收入上限 / 每个值都封顶在 $1M / 数据库里最高的收入 | 收入上限 / 每个值都先封顶在一百万美元 | S06 | 图表上的金额标签保持 $52k…$1B。 |
| medical imaging dataset / slices / summed gradient | 医学影像数据集 / 切片 / 梯度之和 |  | S13 | 医学影像方向的说法。 |
| median / average | 中位数 / 平均值 |  | S13 |  |
| week 1 / week 2 | 第一周 / 第二周（标签与字幕一致） |  | S08 | 标签和字幕同时出现，数字写法要一致。 |
| companion notes (exercises.md); 'link in the description' | 配套笔记（链接见简介） | 配套笔记 | S13 | B 站习惯：简介就是视频描述。 |
| framework / noisy sums / only sums / a tiny chance of a large leak | 框架 / 带噪声的求和 / 只能处理求和 / 以极小的概率发生大量泄露 |  | S02 |  |
| SuLQ (sub-linear queries) | SuLQ；卡片 Sub-Linear Queries 保持英文 | 一个叫 SuLQ 的框架，意思是只问次线性数量的 query（explainer/lexicon.zh.yaml 读作 sulk） | S02 | 次线性的是 query 的数量，而不是单个 query。卡片保留英文，因为缩写就是从那里来的。say: 里 SuLQ 两侧留空格，词典才能匹配。 |
| privacy = a property of the process / not of how the released table looks / … whatever else the attacker knows | 隐私是发布过程（机制）的性质 / 而不是发布出来的表长什么样 / ……无论攻击者还知道什么 |  | S02 |  |
| worst-case belief change / bounded / before / after | 最坏情况下的信念变化 / 有界 / 之前 / 之后 |  | S02 |  |
| noise with exponential tails / (its shape comes later) | 尾部指数衰减的噪声 / （形状稍后揭晓） |  | S04 |  |
| refusing depends only on the queries' sensitivity, not the data | 是否拒绝只取决于 query 的敏感度，与数据无关 |  | S09 | 要点：拒绝本身不泄露任何信息。 |
| a ranking / a set / a string of bits / anything with a distance | 一个排名 / 一个集合 / 一个比特串 / 凡是能定义距离的输出 |  | S10 |  |
| Distance to a property / Small random samples / Outputs that aren't numbers (S10 tiles); Beyond counting | 到某个性质的距离 / 小规模随机样本（两行瓦片：小规模 / 随机样本）/ 输出不是数；不止于计数 | 比如只看一个小规模随机样本 | S10 | 用“小规模随机样本”，不用“小随机样本”；瓦片、标题和旁白一致。 |
| every choice of masks is another query / mask: the bits that count | 每选一组 mask，就是一个新的 query / mask：要数的那些比特 |  | S11 |  |
| the trained model / 'Was Alice in the training set?' / scaled up / many users: the true rate still comes through / each user flips their own coin | 训练好的模型 / “Alice 在训练集里吗？” / 放大版 / 用户多了，真实比例照样能估出来 / 每个用户自己掷硬币 |  | S12 |  |
| choosing ε in practice / when no one can be trusted with the data | 实践中如何选 ε / 没有任何一方值得托付数据时 |  | S12 |  |
| rate / true rate / estimated true rate / people asked / said 'yes' | 比例 / 真实比例 / 估计出的真实比例 / 被调查人数 / 回答“是” |  | S02 |  |
| public voter list / hospital records, names removed / attacker's copy | 公开的选民名单 / 去掉姓名的病历 / 攻击者还原出的副本 |  | S02 |  |

### 人名、机构与标题 / People, organisations, titles
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| Cynthia Dwork, Frank McSherry, Kobbi Nissim, Adam Smith | Cynthia Dwork、Frank McSherry、Kobbi Nissim 和 Adam Smith；之后只用姓 | 英文发音（拉丁词两侧留半角空格；中文版的改拼只在 explainer/lexicon.zh.yaml，规则 F4） | S01 首次给全名（与英文旁白一致） | 现代研究者保留拉丁字母，绝不音译（不写“德沃克”）。代词：Dwork 用“她”；McSherry、Nissim、Smith 用“他”。Dwork 要人工听一遍：早先的 Xiaoxiao 有一次吞掉了 D（Xiaoyi 回环里读对）。 |
| Other researchers: Stanley Warner, Latanya Sweeney, Irit Dinur, Denning, Adam & Wortmann, Evfimievski, Gehrke & Srikant, Blum, Kenthapadi, Mironov, Naor, Talwar, Rothblum, Vadhan, Abadi, Shokri | 原样拉丁字母；卡片上的 & 与 et al. 保留；朗读与字幕：Abadi 和合作者 | 英文发音（Kenthapadi、Talwar、Rothblum 这类少见的名字要人工听；读错时加 lexicon.zh.yaml 条目，见 F4） | 首次给全名（照英文旁白），之后用姓 | 代词：Sweeney、Dinur 用“她”，Warner 用“他”。Xiaoyi 回环里人名没有系统性读错，只有 Whisper 的拼法差异（Dinur → De Nair、Kenthapadi → Cancer Party、Talwar → Tover）。引用卡片保留 et al.（名字下面单独一个“等 2003”像错字）。 |
| Classic eponyms: Bayes, Laplace, Gauss, Gödel (Shannon, Hamming, Chebyshev in other videos) | 贝叶斯、拉普拉斯、高斯、哥德尔（香农、汉明、切比雪夫） |  |  | 历史人物用教科书音译，中文使用者本来就这么说。以他们命名的记号保持拉丁字母：Lap(·)、N(·)。 |
| Gödel Prize 2017 / TCC Test-of-Time Award 2016 | 2017 年哥德尔奖 / 2016 年 TCC 时间检验奖 | 二零一七年哥德尔奖 / 二零一六年 TCC 时间检验奖 |  |  |
| TCC / ICALP / LNCS | TCC / ICALP / LNCS | 照常书写（edge 按字母读） | S02：TCC，一个密码学会议 | 缩写保留。say: 里不要拆开写（拆开的“-”可能被读成“减”）。 |
| Paper title: Calibrating Noise to Sensitivity in Private Data Analysis | 《Calibrating Noise to Sensitivity in Private Data Analysis》；S13 引用卡不变 | 英文原题，前后各一个逗号停顿；不加口头中文意译 | S01 | 论文标题原样引用，方便观众查找。口头再加中文意译会让本来就长的段落多出约 4 秒；意译“在隐私数据分析中按敏感度校准噪声”放进 B 站简介。字幕切分绝不能切在《…》里面。 |
| 'Differential Privacy' (Dwork, ICALP 2006 invited paper) | 标题就叫《Differential Privacy》；特邀论文 | 标题就叫 Differential Privacy；特邀论文 | S12 | 命名时刻：英文名本身就是重点。 |
| Example people: Alice, Bob, Carol, Dan, Eve, Ann, Cy, Dee, Erin, Femi, Bea, Cal; voter list A. Ruiz, K. Osei, M. Novak | 原样保留 | 英文发音 |  | Alice、Bob 在中文 CS 里也是标准角色。Alice 用“她”。 |
| Google, RAPPOR, Chrome, Apple, iPhone | Google、RAPPOR、Chrome、苹果（卡片保留 Apple）、iPhone | Google、Chrome 浏览器、苹果、iPhone | S12 | 按中国研究者的叫法。RAPPOR 只出现在卡片上。 |
| Massachusetts / the governor / Americans | 马萨诸塞州 / 州长 / 美国人 |  | S02 | 标准中文地名。 |
| Sweeney table headers: name / ZIP / born / sex / diagnosis; asthma, flu, cardiac, fracture; F / M | 姓名 / 邮编 / 出生日期 / 性别 / 诊断；哮喘、流感、心脏病、骨折；F / M 保留 | 邮编、出生日期和性别 | S02 | F/M 和邮编、日期一样作为美国模拟数据保留（表头“性别”已说明）。单独的“M”条目还会改掉 s04/s11 里的机制符号 M，“F”会改掉 s10 的图节点。 |

### 标题与章节 / Titles and chapters (meta.yaml)
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| Video title | 【论文精读】差分隐私的开山之作：Calibrating Noise to Sensitivity（TCC 2006） | （不朗读） |  | “论文精读”是观众会搜的类型标签，“开山之作”是“开创某领域的论文”的惯用说法；英文标题保留，方便搜索。 |
| Part 1 title | 差分隐私（上）：定义与拉普拉斯机制 | （不朗读） |  |  |
| Part 2 title | 差分隐私（下）：隐私预算、不止于计数，以及一次性发布的极限 | （不朗读） |  |  |
| Chapter S01: The differencing attack | 差分攻击（differencing attack） | （不朗读） |  | 附英文，免得被理解成差分密码分析。 |
| Chapter S02: Where this paper sits | 这篇论文从哪里来 | （不朗读） |  | 书面标题用“论文”。 |
| Chapter S03: The setup: a trusted curator | 设定：可信的数据管理者 | （不朗读） |  | 书面用“设定”；curator → 数据管理者。 |
| Chapter S04: Defining privacy | 定义隐私 | （不朗读） |  |  |
| Chapter S05: Why so strict? | 为什么这么严格？ | （不朗读） |  |  |
| Chapter S06: Sensitivity | 敏感度（sensitivity） | （不朗读） |  | 核心概念章节：保留英文方便搜索。 |
| Chapter S07: The Laplace mechanism | 拉普拉斯机制（Laplace mechanism） | （不朗读） |  | 核心概念章节：保留英文方便搜索。 |
| Chapter S08: Privacy for individuals, accuracy for populations | 隐私留给个体，准确留给总体 | （不朗读） |  |  |
| Chapter S09: Many questions: the privacy budget | 很多问题：隐私预算（privacy budget） | （不朗读） |  | 核心概念章节：保留英文方便搜索。 |
| Chapter S10: Beyond counting | 不止于计数 | （不朗读） |  |  |
| Chapter S11: Interactive vs one-shot releases | 交互式 vs 一次性发布 | （不朗读） |  | 中文标题里常用 vs。 |
| Chapter S12: What grew from this paper | 这篇论文之后 | （不朗读） |  |  |
| Chapter S13: Recap and questions | 回顾与思考题 | （不朗读） |  |  |

### 配套材料（exercises.md、digest.md） / Companion docs (exercises.md, digest.md)
| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| Headings: Warm-up / Understanding the definition / Understanding the noise / The separation (harder) / Code it (15 minutes) / Reading the paper with this map / Small errata / Glossary for newcomers / In one paragraph / Where it led | 热身 / 理解定义 / 理解噪声 / 分离结果（较难）/ 动手写代码（15 分钟）/ 带着这张地图读论文 / 勘误与阅读笔记 / 新手词汇表 / 一段话概括 / 后续发展 |  |  |  |
| <summary>Answer</summary> | <summary>答案</summary> |  |  |  |
| total variation distance / statistical difference (the paper's word) | 总变差距离（TV 距离）/ 统计差异 |  | exercises 5、digest |  |
| global / local / smooth sensitivity | 全局敏感度 / 局部敏感度 / 平滑敏感度（smooth sensitivity） |  | exercises 3、digest |  |
| sequential / parallel composition; advanced composition | 序列组合（串行组合）/ 并行组合；高级组合定理 |  | exercises 2、9 |  |
| pure / approximate DP; Gaussian mechanism; central DP (trusted-curator model) | 纯差分隐私 / 近似差分隐私（approximate DP）；高斯机制；中心化差分隐私 |  | exercises 8、digest |  |
| utility / privacy–utility trade-off | 可用性 / 隐私与可用性的权衡 |  | digest |  |
| importance sampling (ratio) | 重要性采样（比） |  | digest：S09 RL 类比的出处 |  |
| adversary 𝒜 | 敌手 𝒜（对任意敌手 𝒜） |  | digest 定义 1、附录 A |  |
| Example / Remark / Claim / Appendix / Eqn. | 例 / 注 / 断言 / 附录 / 式 |  |  |  |
| Hamming distance / metric space / Lipschitz constant / semantic security / simulatability / contingency table / covariance matrix / minimum spanning tree / pairwise independent / Reed–Solomon code / normalizing constant | 汉明距离 / 度量空间 / Lipschitz 常数 / 语义安全 / 可模拟性 / 列联表 / 协方差矩阵 / 最小生成树 / 两两独立 / Reed–Solomon 码 / 归一化常数 |  | digest | 中文 ML 里写拉丁字母的现代人名术语保持拉丁字母。 |
| US Census 2020 Disclosure Avoidance System | 2020 年人口普查披露规避系统（DAS） |  | digest |  |
| de-identification (vs anonymization) | 去标识化（区别于匿名化） |  | digest、简介 | 《个人信息保护法》区分“去标识化”和“匿名化”，正是 Sweeney 的论点。 |
| per-example gradient clipping / privacy accounting ('privacy budget, tracked') | 逐样本梯度裁剪 / 隐私预算核算；标签：隐私预算，全程记账 |  | S12、digest |  |

## 规则

### A. 术语与中英混用

- **[A1]** 混用判断。只有以下情况保留英文：（a）符号、希腊字母、变量；（b）人名、产品、缩写、会议、论文标题；（c）封闭清单：query、counting query、mask、trick、hybrid argument、transcript 和 leakage（原文用词），以及只用于口头的 paper、setting、clip。新词要进入（c），必须同时满足：中国 DP/ML 研究者组会上就说英文；中文生硬、有歧义或与别的术语撞车；中文语音在 ASR 检查（规则 F5）里读得对。从草稿清单删除：curator → 数据管理者（受众原因）；log → 对数、odds → 先验/后验概率比、bin → 桶（语音原因）。绝不为了“味道”加英文（不说“private 深度学习”，口头不说 DP）。每个选择在旁白、字幕、标签、章节名、exercises.md、digest.md 中保持一致。
- **[A2]** 口头英文注释：只有三处，每处对应具体句子。S01“它开创了我们今天所说的差分隐私，differential privacy……”；S01“……一个数，叫敏感度，sensitivity……”；S09“……ε 就像一笔隐私预算，privacy budget。”这些是读出来的，所以字幕里也有。旁白不再加别的英文：Laplace、statistical distance、privacy loss 等由英文字幕行显示。
- **[A3]** 只在字幕里出现的括注：每个不超过约 7 个宽度单位，每部分一次（第二部分首次出现再注一次），放在分句末尾，绝不插进名词短语中间（不写“query（查询）f”）。只有两类：（i）给保留英文的词配中文：query（查询）、counting query（计数查询）、transcript（交互历史）、leakage（泄露量）、hybrid argument（混合论证）、mask（掩码）、clip（梯度裁剪）；（ii）给中文术语配教材别名：相邻数据库（也叫相邻数据集）、统计距离（即 TV 距离）、ε-不可区分性（即 ε-差分隐私）。中文行不给中文术语加英文括注：正下方的英文行已经有了。括注只用于显示：say: 里不写；括注后面的锚点需要显式 anchors:（规则 D2）。
- **[A4]** 书面与口头配对。旁白和字幕说 paper / setting / clip；标签、章节名、meta.yaml 和文档写“论文 / 设定 / 梯度裁剪”。“this paper”作主语时说“这篇 paper”；引用原文的用词或结论时说“原文”（原文管它叫 leakage，原文证明了……），这样也避免 paper 一个接一个。固定搭配在口头也保留“论文”（特邀论文）。
- **[A5]** private 的译法。“M is (ε-)private” → M 满足（ε-）差分隐私；“a release/statistic is private” → 不泄露隐私；privately → 用差分隐私 / 在差分隐私下；private deep learning → 差分隐私深度学习；in private（掷硬币）→ 私下。引用原文陈述（定义 1、定理 2）时用“ε-不可区分（性）”。不用“私有”，不用“隐私的 + 名词”，不出现英文 private。
- **[A6]** 易混词对。敏感度（S(f)）≠ 敏感问题（S02 里指话题敏感）≠ 灵敏度（诊断试验的真阳性率）：“a more sensitive query”绝不译成“越敏感的问题”。泄露量（leakage = ε）≠ 侵犯隐私（privacy violation）。DP 发布叫“做隐私处理”，绝不叫“脱敏”（脱敏是遮盖标识符；“脱敏”“匿名化”只用来说去掉名字的做法）。记录（row）≠ transcript（不译“交互记录”）。ε 的“set by policy”= 人为选定，RL 的 policy = 策略。硬币反面 ≠ 分布尾部。准确 ≠ 精度、准确率。噪声 ≠ 噪音。相邻 ≠ 邻居。重构攻击 ≠ 图像重建。桶（bin）≠ 区间（均匀噪声的区间）。S06 的变化量 ≠ S07 的高度差。替换（换掉一条记录）≠ 交换。fixed rule = 确定性的规则。习语“a rounding error”= 可以忽略不计，不译“舍入误差”。差分攻击（这个医院攻击）≠ 差分密码分析。
- **[A7]** 中文句子里的英文词不做任何变形：不加复数、时态、冠词、所有格 's（很多 query、clip 到 C、Warner 的硬币）。量词：一个 query、一个 mask、一个 trick、一篇 paper、一份 transcript、一个桶、一条记录；复数用“很多 / 这些 / 几个”，绝不用“们”。
- **[A8]** 语体。用中文语序和语法，句子内部可以自由重组。避免翻译腔：不说“让我们……”（说“我们来……/来看……”），不说“这就是为什么……”（说“所以……”），上下文清楚时省掉“它”“你的”，少用“被”字句和“一个……的”长链。给观众指令时称“大家”（大家可以先暂停），思想实验里用“你”（现在你是攻击者）；不用“您”。设参数用“取”（ε 取 0.5），“等于”留给公式和定义。“X percent sure”→“有 X 的把握”；about → 大约 / 左右。语气像友好的组会，旁白不用网络流行语（不用“锅”“yyds”“一键三连”）。
- **[A9]** 准确。量词和限定语必须准确翻译：for every / any 对任意，at least 至少，at most 最多 / 不超过，most 大多数，unless 除非，roughly 大约，tiny 极小，bound 上界（口头也说“上界”，不说单字“界”）。不夸大也不弱化结论（S11、S12）。思考题不能因措辞泄露答案（S06 不能说“总共只变 2”）。
- **[A10]** 人名。现代研究者保留拉丁字母原拼写：首次给全名（与英文旁白一致），之后用姓。绝不音译。代词：Dwork、Sweeney、Dinur、Alice 用“她”；McSherry、Nissim、Smith、Warner 用“他”。旁白列举用顿号，最后一个名字前加“和”；卡片上的 & 和 et al. 不变；口头说“Abadi 和合作者”。经典人名用中文：贝叶斯、拉普拉斯、高斯、哥德尔（记号保持拉丁：Lap(·)、N(·)）。机构和地名：美国人口普查局、马萨诸塞州、苹果（卡片上保留 Apple）；产品保持拉丁（Google、Chrome、iPhone、RAPPOR、DP-SGD）；例子里的人物保留英文名。
- **[A11]** 标题与引用。英文论文标题在显示文字里原样放在《》中，say: 里用英文读（不写《》，前后各一个逗号停顿，不加口头意译）。引用行（C. Dwork, F. McSherry, K. Nissim, A. Smith；TCC 2006 · LNCS 3876, pp. 265–284）保持不变。script.md 中方括号里的页码和定义编号不朗读。
- **[A12]** 只做大陆简体中文（数据库、信息、默认、算法、视频、本地化；不用“資料庫、資訊、預設、演算法、影片”）。暂不做繁体版。

### B. 排版

- **[B1]** 空格。中文与拉丁字母、数字、希腊字母或行内公式之间加一个半角空格，适用于字幕、Pango 的 Text 标签、文档和 say:（用 ε 控制、2006 年、41 个病人、L1 范数、发来一个 query）。say: 里的空格也是必需的：python -m explainer.i18n check 会报缺空格（词典正则现在把汉字也当作词边界，“Dwork的”也能匹配，但规则不变）。全角标点旁不加空格，数字和 %、° 之间不加，连字符复合词内部不加（ε-不可区分性、(ε, δ)-差分隐私、DP-SGD）。拉丁符号（→、= 等）和中文开引号之间也不加：写 →“是”，不写 → “是”，因为引号字形本身已带半个字宽的空白（S04 的 strings 这样写；S02 的“H → “是””“T → “否””目前还带空格，与本规则不一致）。Tex/MathTex 里 xeCJK 只在同一段文字内部自动加中西文间距；\text{…} 末尾紧接数学、以及分开的 Tex/MathTex 片段之间都不会加，要手写 TeX 空格：\text{答案}\ 0、\text{至多}\ n\sigma、\text{全部}\ 2^8、“用的是多大的\ ” + $\varepsilon$、“那么\ ”、“定理 2：满足\ ” + ε。不要用 U+00A0 / U+202F 伪造不换行空格：norm() 和 split_balanced() 会把它变成普通空格。
- **[B2]** 标点。中文用全角标点：，。、；：？！（）“”‘’——……《》，英文词前后也一样；引号用“”，嵌套用‘’。列举用顿号。只有公式、数字和元组里用半角（(Carol, 有 X)）。一个中文句子内部不出现。？！（每个英文句子对应一个中文句子），改用，；：。标签末尾不加句号，问句保留？。行首不能是标点。画面上的“……”和中文引号“”‘’由工具链自动改用 CJK 字体（explainer/i18n.py install()，对 Text 生效）：拉丁自家字体排在 Pango 回退列表最前，它的 U+2026 落在基线上，引号也太窄。所以场景不用再自己写 t2f（s02_map.py 里留下的 t2f 已多余，但无害）。“——”不改字体：自家字体的两个 U+2014 连成一条完整的破折号，CJK 字体的两个之间反而断开；标签里放不下或断开难看时改用逗号（S09：“（每个桶），仍随 d 增长”）。
- **[B3]** 字体。工具链把自家字体和 Noto Sans / Serif / Sans Mono CJK SC 配对（explainer/i18n.py 的 CJK_FONTS），就用这些字体名。汉字约 1 em 宽：每个中文标签按英文标签的外框来适配，而不是照搬 font_size；数字、公式、人名、颜色、位置与英文版完全一致。中文不用斜体：英文用 slant=ITALIC 的名字或引语（S12 命名卡“差分隐私（differential privacy）”、S13 结尾引语“放心，已经匿名化了。”），中文版通过 i18n.active() 分支改为正体，因为 Pango 只会把汉字机械地斜过来。粗体可以用：Noto Serif CJK SC 有真正的粗体。

### C. 数字与数学

- **[C1]** 显示文字中的数字。数值、结果、年份、百分比、小数、引用编号用阿拉伯数字（41、42、52.5%、ε 取 0.5、2006 年、第 4 节、5000 个桶）。成语、约数、叙述中的小数目和序数用汉字（一条记录、两个世界、三个核心想法、一半、五五开、成千上万步、第一 / 第二、第一周）。字幕里的大数用“万 / 亿”加数字，不加千分位逗号（100 万、3300 万、1.34 亿、10 亿美元）；9999 以内不加分隔。图表和公式保留原数字（n = 10,000；1,000,000；$1M；$52k）。负号用 −（U+2212）。
- **[C2]** 画面公式。MathTex/Tex 的公式与英文完全一致；只翻译 \text{} 里的词和 Tex 的文字串（误差、事件 A、统计距离、阴影面积、噪声尺度、每个桶、除非、答案、比特翻转、至多）。含中文的 TeX 会自动用 XeLaTeX + ctex 排版（i18n.cjk_tex_template），不需要拆成单独的 Text 对象。公式保留 ln。中文闭引号”紧挨数学括号时，加 \mkern-6mu 把括号拉近（”的右半边是空白）：'\Pr[\text{回答“是”}\mkern-6mu]'。\text{} 里的全角：，后面去掉英文的 \quad（最多用 \,）：'\text{对于很小的}\ \varepsilon\text{：}\,'、'任意分析者，'。中西文之间要显式写的 TeX 空格见 B1。
- **[C3]** 字幕里的数学要和声音一致。只有按符号本身来读的保留符号：变量、希腊字母、f(x)、S(f)、x′、紧凑分数 a/b、幂 e^ε、数字、%。读出来的运算写成文字：等于、乘、加、减、不超过、至少、约、根号 n、无穷大、3 的对数。字幕里不出现 LaTeX 源码，也不出现 ≤ ≈ × → √ ∞（它们实际按全角显示，但 units() 按半角计宽，会撑爆字幕）。
- **[C4]** say: 读法表。ε 艾普西隆；e^ε E 的艾普西隆次方；e^(−ε) E 的负艾普西隆次方；e^(nε) E 的 n 乘艾普西隆次方；1/n n 分之一；1/λ lambda 分之一；−1/λ 负的 lambda 分之一；2/ε 艾普西隆分之二；S(f)/ε S f 除以艾普西隆；d/ε d 除以艾普西隆；√n 根号 n；√k 根号 k；2σ 两倍 sigma；ε/(2S) 艾普西隆除以两倍敏感度；1 + ε 一加艾普西隆；x′ x prime；f(x) f x；S(f) S f；ln 3 三的对数；Pr[A] A 的概率；ε = 0.1 艾普西隆取零点一的时候。年份逐位读（二零零六年），整数“四十一”，小数“四十三点七”，百分数“百分之六十二”；数值用“二”，个数和倍数用“两”。

### D. 旁白文件（narration.yaml）

- **[D1]** 句子对齐（explainer/i18n.py）。i18n/zh/narration.yaml 里每个 SAY 行一条（共 78 段）；en 与 SAY 行逐字节相同，zh 的条目数必须和 explainer.voice.split_sentences 切出的英文句子数一致（本脚本共 259 句）。只在句子内部重组，绝不合并或拆分句子。单词句（“No.”“Say, Alice's.”“Sensitivity one.”）也各占一条；“Privacy for individuals. Accuracy for populations. That is the bargain.”同样是三条。做 TTS 之前先运行 python -m explainer.i18n check videos/dwork2006-calibrating-noise。
- **[D2]** 锚点。场景里调用 vo.wait_until / until 约 400 次，很多落在句子中间。没有 anchors: 条目时，英文短语会被映射到中文显示句里相同的相对字符位置。凡是中文语序移动了这个短语（前置的“除非……”、重排的列举、短语前面加了只在字幕里的括注），以及每个指明术语、数字或符号的短语，都要加锚点，目标写词表里的形式。目标必须在预定的那一句里第一次出现：AlignedClip.time_of 取整条 SAY 里第一个包含目标的句子。尽量选中文文本。补充四点（S04–S13 实测）：
  - 锚点按显示句里的字符位置估算时间（工具链按字符数在句子时长里插值）。读出来比显示长的片段（1/ε → 艾普西隆分之一、ε → 艾普西隆、1/2 → 二分之一）会让后面的词估得偏早；拉丁词（query、Google、Rothblum）正相反，每个字母都算一整个字符，后面的词估得偏晚。要对照词级时间（Whisper）检查，需要时把目标往前或往后挪一点：S11“都是 1，所以交互式的管理者”、S12“Chrome 浏览器里”、S13“才算一个人”。
  - 只在字幕里的括注也会让它前面的词估得偏早：time_of 把不朗读的（……）也算进句长，紧挨在括注前面的术语就估早了。S05 的 'statistical distance' 因此指向“（即 TV 距离）”，不指向“统计距离”（在 Xiaoyi 下早了约 0.7 秒）；S06 counting query 那句的锚点“比如医院那个”是同样的做法。
  - 中文语序把两个锚定短语对调时，锚点跟中文顺序走，场景在 i18n.active() 下按这个顺序等：S04 的 'in absolute value' → “它的绝对值”现在排在 'it must be at most' → “都不能超过”前面（s04_definition.py 的中文分支先写绝对值竖线，再写 ≤ ε）。
  - 本片的时长和锚点都是用 Xiaoyi 测的；换声音后要重新检查。发布时改走 Azure 端点会重新合成全部句子，也要再跑一遍 D3 的时长对比。
- **[D3]** 时长。VoiceScene 会等中文音频播完，所以音频更长时画面停住，更短时固定时长的动画之后会留空白。目标是每段中文与英文时长相差不超过 ±15%：删掉多余的连接词，但不删内容。渲染前检查每段时长：python -m explainer.script videos/dwork2006-calibrating-noise/script.md --lang zh（工具链 I7，已实现；同时填好渲染用的 TTS 缓存）。
- **[D4]** 内容对等。每个中文句子只翻译对应的英文句子，不多加：不加人名、产品或结论（旁白里不加 RAPPOR、DP-SGD、重要性采样，不口头翻译论文标题）。唯一的增补是三处口头英文注释（A2）和只在字幕里的括注（A3）。
- **[D5]** 固定口头句式。“Pause and ponder: …?”→“暂停想一想：……？”，下一句“Pause the video if you need more time.”→“需要多想一会儿的话，可以先暂停视频。”“Pause:”→“暂停一下：”；“Before I show you, pause:”→“先别急着看答案，暂停一下：”；“Here is one you can answer yourself.”→“这一题你可以自己回答。”；“Let's recap.”→“我们来回顾一下。”；“One: … Four:”→“第一，…… 第四，……”；“Some questions to test yourself; pause after each.”→“最后留几道题给大家自测，每道题后面都可以暂停一下。”卡片标题“暂停想一想”（explainer/locales/zh.yaml），黄色粗体样式不变；卡片上的问题最多两行，以？结尾；计时秒数不变。标题：自测、本期内容。

### E. 屏幕文字（strings.yaml）

- **[E1]** 标签用旁白的术语，但更短：电报式名词短语，可以用 → ⇒ ≈ × 和缩写（DP、RL）。标签只写中文，例外：S12 命名卡“差分隐私（differential privacy）”；概览和回顾卡上的核心概念名（S01 想法卡、S13 回顾面板：敏感度（sensitivity）、拉普拉斯机制（Laplace mechanism），放得下的话）；保留英文清单里的词（query、mask、transcript、hybrid argument、SuLQ、Sub-Linear Queries）。定义 1 卡可以通过受 i18n.active() 控制的场景改动加一行灰色小字“（即今天的 ε-差分隐私）”；不改场景时由字幕别名括注承担这个联系。
- **[E2]** 一个英文键对应一个中文串。strings.yaml 按英文原文精确匹配，不区分类型和场景（带场景作用域的键除外，见 E3），所以共用的键在每处都得到同一个中文（“Sensitivity”既是 S01 的想法卡，也是 S13 的回顾面板；“Query”是 S01、S08、S11 的卡片标题）。选一个各处都通顺的中文，或者在场景里改英文键。有意保留英文的字符串（Query、SuLQ、Sub-Linear Queries、mask r、RL:、人名、引用、TCC 2006）加原样映射，这样 build/i18n/missing.zh.json 只列真正漏译的。
- **[E3]** 不带作用域的单个字母和符号（H、T、F、M、A–J、?、.、·、vs、no）绝不放进 strings.yaml：tr() 会把 s04、s11 的机制符号 M、s10 的图节点 F 和 H 以及其他所有地方一起改掉。带场景作用域的键（'<场景文件名>|<英文>'，工具链已支持）可以用，只作用于那个场景文件：（a）有意保留的符号词加原样映射，什么也不翻译，只让 missing.zh.json 保持干净（'s05_strict|vs': 'vs'、's12_legacy|vs': 'vs'）；（b）只在一处翻译（'s13_recap|?': '？'、's10_beyond|.': '。'、's04_definition|no': '“否”'、's05_strict|no': '无'、's11_separation|MOST': '大多数'）。同一场景里如果还有别的同名串（例如 MathTex 里的 '?'），就改用场景分支（S04 的 Warner 卡片由 ponder_at 自己换成“？”）。硬币字形保持 H/T（定稿）：S02 分支标签写“正面 / 反面”，结果标签写“H → “是”” / “T → “否””，旁白说“正面答‘是’，反面答‘否’”；S04 写“→“是”” / “→“否””。原先计划的“H（正面）→“是””放不下（会伸进人群格子）。F/M 作为美国模拟数据保留。
- **[E4]** 拆片的 Tex/MathTex。很多标签由几段拼成（文字 + ε + 文字）。翻译时选能保持各段位置的语序：“Theorem 2: ”+ ε +“-indistinguishable”→“定理 2：满足\ ”+ ε +“-不可区分性”；“Gaussian noise is back in, for a tiny ”+ δ →“高斯噪声回来了，代价是一个极小的\ ”+ δ；“What counts as ”+“one person's row”+“?”→“什么才算”+“一个人的一条记录”+“？”；“What's the ”+ ε +“?”→“用的是多大的\ ”+ ε +“？”；“noise of typical size 2, the same for every”+ n →“噪声一般在 2 左右，不依赖于”+ n；“Warner's coin: what is its”+ ε +“?”→“Warner 的硬币对应多大的”+ ε +“？”（ε 前的间距由场景给出；场景只把结尾换成“？”，并让 ε 和“？”坐在拉丁字母的基线上：s04_definition.py 的 ponder_at）。找不到保持顺序的中文时，就改场景（加 i18n.active() 分支），绝不硬凑不自然的中文：S04 括号标签“privacy loss at”+ t 由场景按中文语序拼成 t +“处的隐私损失”，strings 里不再有这个键。含行内公式的 Tex 串同理（“If $A$ reads each row”→“如果 $A$ 对每条记录”；“composition: $k$ questions cost …”→“高级组合：$k$ 个问题的代价 …”）。
- **[E5]** 着色子短语。场景用 t2c 给英文子串着色的地方，中文标签必须原样包含该子短语的中文；工具链用同一张表翻译 t2c 等的键（I4，已实现）。英文大写强调（Any ONE query、MOST queries）改为给“单个 / 大多数”上色或加粗。
- **[E6]** 模拟数据保持原样：美国日期、邮编数字、F/M、金额（$52k…$1B）、Sweeney 表里的人名。只翻译表头。

### F. 语音（TTS）

- **[F1]** 语音。中文旁白用 edge zh-CN-XiaoyiNeural（speed 1.0）：女声，与英文的 af_heart 对应，也和井字棋视频的中文声音一致。它是工具链的中文默认（explainer/build.py DEFAULT_VOICES，commit 875166f），所以 video.yaml 不用设 languages.zh.voice，只有换声音时才设。为什么不用最初选定的 Xiaoxiao：用 faster-whisper large-v3-turbo 做 ASR 回环，Xiaoxiao 读旁白保留的英文词口音很重（noise → Nice、epsilon → Excellent、Claude → Clark、diverge → Vert），中英混用就失去了意义；同为普通话声音的 Xiaoyi 在对比测试里 17 个测试词和所有数字全部读对，两个视频全部 417 个中文句子（本片 259 句）的回环也没有发现系统性误读（剩下的标记见“TTS 实测摘要”）。针对 Xiaoxiao 定下的改写（ε 读艾普西隆、row → 记录、bin → 桶、log → 对数、odds → 先验/后验概率比、SuLQ 读 sulk、敏感度是一等）全部保留：它们本来也是更自然的中文。备选 zh-CN-YunxiNeural（男声）：早先测试里它同样把 bin 读成“病”，还漏读过一次 sensitivity。edge 不支持自定义 SSML 或拼音，读错只能靠改写。发布：免费的 Edge 朗读端点没有用于发布视频的授权；官方 Azure AI Speech API 提供同一个声音，授权允许用于发布的视频。设置 AZURE_SPEECH_KEY 和 AZURE_SPEECH_REGION 后，工具链自动把 edge 声音改走 Azure（explainer/voice.py 的 AzureBackend；EXPLAINER_EDGE_VIA_AZURE=0 可关闭）。TTS 缓存按后端区分，所以发布版会重新合成全部句子（见 D2、D3）。
- **[F2]** 什么时候必须写 say:。凡显示文字里含希腊字母、′、公式或函数记号（f(x)、S(f)、1/n、e^ε）、任何宽度的括号、《》、%，或只在字幕里的括注，都要写 say:。say: 里的数字写成汉字（见读法表 C4）；没有 say: 的句子保留数字，edge 能读对（早先用 Xiaoxiao 测过 2006 年、52.5%、0.5、42，都转写正确；Xiaoyi 在对比测试里数字全对）。say: 里不出现希腊字母、LaTeX、括号、《》、× ÷ ≤ ≈ → √ 等运算符，也不出现夹在空格字母之间的连字符。
- **[F3]** 实测读错的地方，靠改写解决（早先的 edge 声音 Xiaoxiao、Yunxi，用 faster-whisper 检查；改用 Xiaoyi 后这些改写全部保留）。拉丁 epsilon → Excel/Excellent：读“艾普西隆”。表示 row 的“行”多数语境读成 xíng（型/形）：row 一律用“记录”，“one line”改写；口头绝不用“行”表示 row。bin → 病：用“桶”。odds → ODS/奥子，“旧”→“就”：用“先验/后验概率比”。log → Loud/Lock：用“对数”。“计数”→“技术”：说 counting query。“等于一时”→“等于10”：说“……的时候”。小写 e → “一”：写大写 E。直接写 f(x′) 会吞掉撇号：写“f x prime”。读得对的：query、counting query、curator、transcript、leakage、mask、clip、setting、paper、hybrid argument、Differential Privacy、privacy budget、lambda、sigma、delta、x prime、DP-SGD、数据管理者、记录、桶、似然比、根号 n。trick 在 Xiaoxiao 里有一次听成 trip（Xiaoyi 回环里都读对）：仍要人工听。与声音无关的一处：“敏感度为一”的“为一”和“唯一”同音，说“敏感度是一”。Xiaoyi 有时按中文习惯读字母（d 读 di、t 读 ti、E 读 yi），这是普通话数学课的正常读法，不用改写。
- **[F4]** 人名与词典。EXPLAINER_LANG=zh 时只加载中文词典 explainer/lexicon.zh.yaml（voice.load_lexicon；共用的 lexicon.yaml 不参与），改拼后的文本就是 TTS 缓存键。say: 里每个拉丁词两边都加半角空格（规则 B1），改拼才会匹配（respell，edge 和 azure 后端都用）。目前只有一条：SuLQ → sulk（否则读成“苏LQ”/SoilQ）。Xiaoyi 回环里人名没有系统性读错，只有 Whisper 的拼法差异（Dinur → De Nair、Kenthapadi → Cancer Party、Talwar → Tover），所以没有再加条目；Kenthapadi、Talwar、Rothblum 这类少见的名字仍要人工听。名字读不对时只在 lexicon.zh.yaml 里加只用于 say: 的改拼；绝不改显示的人名，中文的修正也绝不放进 lexicon.yaml。需要人工听的多音字：差（只差 chà / 差分、差值 chā）、重构（chóng）、数一数（shǔ）、还、处（t 处 chù）、长（增长 zhǎng）、为。
- **[F5]** 渲染前做 ASR 检查。把每个中文句子合成出来，用 /opt/tts-eval 的 faster-whisper-large-v3-turbo（语言设为 zh）转写；拉丁词、人名、艾普西隆、lambda/sigma/delta 或数字没被转写回来的句子都要标出来。逐句人工听，改写，再测。发音正确只是转写成同音字的（“先验”转成“先焰”、“奇数”转成“积数”、“阶乘”转成“阶层”、“艾普西隆”转成“艾普希龙”）不算问题；Whisper 自己的毛病也不算：长句被截断、人名拼法不同、把 lambda 写成 λ。

### G. 字幕

- **[G1]** 双语格式。中文行在上（字大），英文 SAY 原句在下（字小），由 narration.yaml 配对；时间轴跟随中文音频。宽度按工具链的单位算（一个汉字 1，一个拉丁字符 0.55：transcript 约 5.5，论文标题约 33）。写句子时让每个分句不超过 24 个单位；代码在 30（双语）和 22（纯中文字幕）处切分。在，；：或分句之间断开，绝不切在英文术语、数字加量词（5000 个桶）、第 4 节、公式或《…》里面。
- **[G2]** 字幕结尾。去掉每条字幕末尾的。，、；：；保留？！……和收尾的”）。工具链已实现（explainer/subtitles.py 的 strip_end，由 tracks() 调用；I2）。
- **[G3]** 英文行。narration.yaml 的 en 必须与 SAY 行逐字节相同，而 SAY 行把数字和数学写成读法（forty-one、e to the epsilon）。双语字幕的英文行最好显示数字和符号（41、e^ε、1/n、x′）：每句加一个可选的、手写的 en_display（自动转换不安全：one row、no single person）。工具链已支持（I6），本片四个旁白文件都已用上 en_display；没写的句子，英文行显示 SAY 原文。

### H. 标题与配套材料

- **[H1]** 标题（i18n/zh/meta.yaml）。视频标题、分 P 标题和章节标题用词表里的写法。核心概念章节附英文术语（敏感度（sensitivity）、拉普拉斯机制（Laplace mechanism）、很多问题：隐私预算（privacy budget）、差分攻击（differencing attack）），方便在章节列表里搜索。B 站简介写出论文标题的中文意译（在隐私数据分析中按敏感度校准噪声），附配套笔记链接，并中英对照列出核心术语；标签：差分隐私、differential privacy、敏感度、拉普拉斯机制、隐私预算、随机响应、论文精读。
- **[H2]** 配套材料：i18n/zh/exercises.md 和 i18n/zh/digest.md，按本词表和排版规则翻译。用书面语（论文、对数、梯度裁剪；形式化陈述里 𝒜 写“敌手”；例 / 注 / 断言 / 附录 / 式）。标题和 <summary>答案</summary> 要翻译；页码（p. 270）、公式和引用保持不变。两份文档末尾都加中英术语对照表（英文 | 本片用词 | 常见变体：Laplace 机制；本地 / 局部差分隐私；成员推断；相邻数据集 / 兄弟数据集；亚线性 / 次线性；序列 / 串行组合；计数查询；全变差距离），并注明 S(f) 是全局敏感度，不是诊断试验的灵敏度。
- **[H3]** exercises.md 里的代码。标识符、API 名、字符串字面量、文件名和行内 `code` 逐字节不变（laplace_mechanism、rng.laplace、rng.normal、digest.md），代码照样能运行；只翻译 # 注释和代码周围的说明文字。
- **[H4]** playground.html 另做一轮，界面文字使用本词表。

### I. 工具链待办

标“已完成”的条目已对照代码确认，保留在这里说明规则依赖什么。

- **[I1]**（已完成）build.py 的 DEFAULT_VOICES 曾指向不存在的后端 kokoro-zh；现在中文默认是 edge zh-CN-XiaoyiNeural（commit 875166f），video.yaml 不必再设 languages.zh.voice（规则 F1）。
- **[I2]**（代码已完成，回归测试未加；这部分代码还在改，最近是 commit cd67aa4）explainer/subtitles.py：不在数字和后面的中文量词之间切、不在《…》里切（实在太长时只在《…》内的空格处切）、不在数字内部切（两个数字之间的“,”或“.”之后），下一个字符是标点时也不切；拼回片段时，汉字和汉字之间不加空格，汉字和拉丁字母/数字之间保留空格（B1）；只去掉一条字幕末尾的标点（G2，strip_end），合并进来的句子保留自己的句末标点；把短于约 1 秒的句子字幕并入相邻一条。还缺：用 S01 的论文标题句和“5000 个桶”写回归测试。
- **[I3]**（部分完成）python -m explainer.i18n check 现在检查朗读文本（say:，没有 say: 时是显示文字）：括号和《》、数学符号（ε δ λ σ α Δ ′ √ ≤ ≥ ≈ × ÷ ^ = < > → ← +）、n!、带下划线的名字、以“种”结尾的分句、汉字与拉丁字母/数字之间缺空格，以及不在本词表朗读/字幕/首次出现形式或 allowed_spoken_latin 里的拉丁词（能抓住“private 深度学习”这类问题）；另外检查句数、句末和句内标点、锚点目标是否存在。还没做：朗读文本里的数字、%、/ 报错；通过读法表比对 say: 与显示文字；检查标签里的拉丁词；列出没有锚点的 wait_until 短语。
- **[I4]**（已完成）i18n.install() 用 tr() 翻译 t2c / t2w / t2s / t2f / t2g、tex_to_color_map 和 substrings_to_isolate 的键；带场景作用域的键写成 '<场景文件名>|<英文>'（如 's04_definition|no'），只在那个场景文件里生效（规则 E3）。
- **[I5]**（已完成）EXPLAINER_LANG=zh 时只加载 explainer/lexicon.zh.yaml（voice.load_lexicon），改拼后的文本就是 TTS 缓存键；用于只作用于 say: 的改拼。中文的修正绝不放进英文视频共用的 lexicon.yaml。
- **[I6]**（已完成）narration.yaml 支持可选的逐句 en_display，用于英文字幕行（规则 G3）。
- **[I7]**（已完成）python -m explainer.script videos/dwork2006-calibrating-noise/script.md --lang zh 合成中文旁白（同时填好渲染用的 TTS 缓存），逐段对比中英时长，标出超过 ±15% 的段（规则 D3）。
