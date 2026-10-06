# 井字棋视频中文版词表（中英混用版）

视频：*Why are there exactly 255,168 games of tic-tac-toe?*（`videos/tictactoe-255168`）  
受众：11–14 岁（小学五六年级到初二）、没学过编程的中国学生  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改）

## 为什么要中英混用（code-switching）

- 很多词本来就是代码里的英文名字。explore、winner、None 是程序里真实存在的名字，译成“探索函数”“赢家函数”“无”，等于给观众讲了一个程序里没有的东西，回头看代码也对不上。
- 中国的编程老师和程序员本来就这么说：“explore 函数”“返回 None”“for 循环”“用 Python 写”。这是这个场景里真实的说法，不是为了洋气。
- 反过来，已经有标准中文名的概念（井字棋、阶乘、函数、列表、递归、回溯）就用中文。这些地方硬塞英文，听起来像在显摆。
- 英文名字第一次出现时加注一次意思（winner =“赢家”，explore =“探索”，None =“没有人”）。英语国家的孩子读代码时白拿的那一层意思，中国孩子也能拿到，代码里的英文就成了桥，而不是墙。
- 双语字幕把每个英文原词都显示在中文下面；递归、回溯两张卡片再加一个灰色小英文。这样一个视频能同时照顾中文观众、双语观众，也方便以后用英文搜索这些概念。

## 总原则

以普通话为主，只在中文使用者本来就说英文的地方保留英文。判断每个词时问一句：一位中国老师或程序员，对一个 11 到 14 岁（小学五六年级到初二）、没学过编程的孩子，实际会怎么说？（1）这些保留英文、用英文读：玩家 X 和 O（O 读“欧”，绝不读“零”或“圈”）；Python；画面上代码里出现的所有名字和关键字（explore、winner、None、board、player、total、WIN_LINES、range、print、for、if、return……），后面接中文名词（explore 函数、返回 None、for 循环），第一次读到时在同一句里加注一次意思（winner，意思是“赢家”；explore 就是“探索”的意思；None，意思是“没有人”）；Plan B；配套材料里的 minimax。译成“探索函数”“赢家函数”“无”，说的是程序里根本不存在的东西，这才是听起来别扭的译法。（2）领域里已有标准中文名的，用中文：井字棋、对局、阶乘、函数、列表、调用、返回、递归、回溯、注释、平局。这些地方说英文反而做作。递归、回溯这两个以后会在英文资料里遇到的概念，卡片上加一个灰色小英文（recursion、backtracking），两种叫法都能搜到；旁白只说中文。（3）视频自己造的说法按意思翻：ghost games → 幽灵对局，Pause and ponder → 暂停想一想。（4）英文特意用大白话、避开术语的地方，中文也用大白话（== 一样、!= 不是、空格子、彻底算透了、谁更有希望赢）；需要标准术语时，配一句白话解释引入一次（返回（交回结果）；“索引”放在配套练习里）。双语字幕（中文在上、英文原句在下）已经把每个英文原词都显示出来，所以中文字幕行不再加英文括注。数字一律用阿拉伯数字、半角逗号分节。旁白用 edge 的 zh-CN-XiaoxiaoNeural，所有朗读文本遵守下面的 TTS 规则。语气：友好、具体、短句，大陆简体中文，不幼稚。

## 相对草稿的主要改动

- 代码名（winner、explore、None）仍保留英文，但第一次读到时在同一句里加注意思（“赢家”“探索”“没有人”）。代码里的英文这样才成为桥梁。
- “返回”作为标准术语保留，第一次出现时标签写“返回（交回结果）”，避免理解成手机的“返回键”；== / != 的标签改成“一样 / 不是”，不让 == 和赋值的 = 都叫“等于”。
- 棋盘的横行改叫“排”，“行”只留给代码行（只改一行代码、“撤销”那一行）；“三子连成一线”绝不说“连成一排”。
- “空格”改成“空格子”；“被数了”改成“被算了”；“6 乘 5 得 30”改成“等于”；“胜负检查”改成“判断输赢”；标签“X 胜”改成“X 赢”。
- “幽灵结局”取消，只用“幽灵对局”一个词；计数器“第一个 O 的位置：3”改成“放法”，避免被看成“在 3 号格”。
- 量词：问“有多少种不同的对局”及其答案用“种”，具体某一局和胜负统计用“局”，绝不用“盘”；朗读时“种”不放在句末（会被读成“重”）。
- 函数不再借数学课的“一次函数”来解释；递归的定义改成“函数自己调用自己，就叫作递归”（递归是过程，不是函数）；阶乘不再说“简称”。
- “破解”改成“彻底算透了”，“占优”改成“谁更有希望赢”，“回顾”改成“小结”，“弄坏”改成“改坏”，结尾“动手去探索吧！”呼应 explore。
- O 读“欧”（中文里字母 O 的标准读法），只要求绝不读成“零”或“圈”；Plan B 允许在旁白里说（画面同时出现，中文口语本来就说）。
- 朗读改用 edge zh-CN-XiaoxiaoNeural，数字不再手写读法（实测读对），只在实测出错处写 say:（两局、两步、阶乘号、括号、符号）。
- 递归、回溯卡片上的灰色英文小字保留（方便双语观众和以后搜索），旁白不读英文。
- 代码注释的中文版通过 localized() 读取本地化程序文件显示到画面，而不是通过 strings.yaml；字幕切分和 t2c 颜色需要先改工具链（见 I 节）。

## 术语表

“字幕 / 屏幕”是显示用的写法（字幕和画面标签）；“朗读”是声音实际说的内容，只有和显示不同时才写进 narration.yaml 的 `say:`。

### 棋盘与对局 / Board and games

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| tic-tac-toe | 井字棋 |  |  | 中文。孩子们都叫井字棋，说英文反而怪。 |
| game (one complete play-through: the whole ordered list of moves) | 对局；一局；这一局；每一局 | 对局 / 一局 | 这里说的“一局”，指的是从第一步到最后一步、按顺序排好的全部走法。 | 不用“游戏”“棋局”“盘”：棋局也指棋盘上的局面，而视频专门区分“棋盘一样”和“对局一样”。 |
| how many (different) games: counting distinct possible games | N 种对局；有多少种不同的对局？；1,440 种对局；5,328 种对局；255,168 种对局；formula: = 1,440 种 | ……种对局（种 never ends a spoken clause） |  | 问“有多少种不同的对局”及其直接答案用“种”；朗读时“种”后面必须跟名词（句末的“多少种。”被读成“多少重”）。 |
| games as tallies and splits; 'games' (S04 table header and laptop counter) | X 赢了 131,184 局；1,440 局在第 5 步结束；1 局；1 + 1 = 2 局；header/counter: 局数 | 两局 for 2 (say: 两局) |  | 单独一局、叶子、柱子数值、胜负统计用“局”。2 局要在 say: 里写成“两局”。 |
| move / on move 5 / the fifth move | 一步；第 5 步；在第 5 步 | 第五步（edge reads 第 5 步 correctly）；2 步 → say: 两步 |  | 步数从 1 开始，一律写“第 N 步”。 |
| step (of the counting method: 'in three steps', First/Second/Third) | 三个步骤；第一，…第二，…第三，… | 分三个步骤 |  | 计数方法的阶段叫“步骤”，绝不用“步”。 |
| square / squares 0–8 | 格子、格；0 号格 … 8 号格 | 格子；零号格 | 9 个格子从 0 到 8 编号，从左到右、从上到下。 | 格子编号从 0 开始，一律“N 号格”，不写“第 N 格”。 |
| empty square | 空格子（tight labels may use 空位） | 空格子 | 空格子里放一个点。 | 改：不用“空格”（编程里指空格键/空格字符），一律“空格子”。 |
| board / empty board | 棋盘；空棋盘 | 棋盘 |  | 代码里的 board 不读出来。 |
| mark (X's three marks, O's first mark, one more mark) | 三个 X；第一个 O；2 个 O；generic: 棋子（多一个棋子） | 三个 X；两个 O；棋子 |  | 用字母称呼棋子：三个 X、第一个 O；不分玩家时说“棋子”。 |
| X / O (the players and their marks) | X / O | X: English letter name; O: 欧 (ōu), the standard Chinese name of the letter. Never 零, never 圈. |  | 保留字母。O 读“欧”（中国学生读字母 O 就是这样），绝不能读成“零”或“圈”。 |
| three in a row | 三子连成一线；连成一线 | 三个连成一条线 |  | 不说“连成一排”（排只指横排），不说“三连”。 |
| winning line(s); line on the board | 获胜线；8 条获胜线；线；哪条线？ | 获胜线 | 获胜线：能让人赢的一排、一列或一条对角线。 | 棋盘上的“线”；代码的一行叫“行”。 |
| row / column / diagonal / top row / 3 rows, 3 columns and 2 diagonals | 排（横排）/ 列（竖列）/ 对角线；最上面一排；3 排、3 列和 2 条对角线 | 排 / 列 / 对角线 |  | 改：棋盘的行叫“排”，“行”只留给代码行；顺便去掉 háng/xíng 多音字。 |
| parallel | 平行；和 O 那条线平行的一排或一列 | 平行 |  | 学校几何用词。 |
| corner / edge / center (as first moves and as squares) | boards: 角 / 边 / 中心；counted: 每个角格 27,732（×4）· 每个边格 29,592（×4）· 中心 25,872（×1）；（4 个角格）（4 个边格）（1 个中心） | 下在角上 / 下在边上 / 下在正中间 | 边格，也就是每条边正中间的那一格 | “每条边”是整条边（含两个角），单个格子要说“角格 / 边格”。 |
| named squares: top-right / top-middle / bottom-middle / bottom-right | 右上角那格 / 上边中间那格 / 下边中间那格 / 右下角那格 |  |  | 旁白像英文一样按位置称呼格子；编号（N 号格）用于标签和代码。 |
| win / X wins / X won! / X wins on move 5 | 赢；X 赢了！；labels: X 赢 / O 赢；X 在第 5 步赢了 | 赢 |  | 改：标签也用“赢”，不用“胜”。 |
| draw / draws | 平局 |  |  | 井字棋孩子们都说“平局”；“和棋”像下象棋。 |
| whose turn / X to move / X's turn / switch turns / go first | 轮到谁；轮到 X；轮到对方；先走；label ← 轮到谁：X 还是 O | 轮到 X |  | 选择疑问句用“还是”。 |
| order / orders | 顺序；6 种顺序 | 顺序 |  |  |
| flipped or turned (rotated, mirrored) | 翻转或旋转（the same pair in the companions; never 镜像） | 翻转或旋转 | 棋盘翻转或旋转之后的版本，也分开算。 | 视频和配套材料统一用“翻转 / 旋转”。 |

### 计数与数学 / Counting and maths

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| choices multiply / 9 groups of 8 | 选择数相乘；9 个 8 = 72；9 种选择 / 8 种选择 | 九个八，所以选择数要相乘 |  | “9 个 8”正是小学乘法的说法；视频里不点名“乘法原理”（配套材料可提分步乘法计数原理）。 |
| 9 × 8 × 7 × … × 1 (the chained product) | 从 9 一直乘到 1（连乘） | 从九一直乘到一 | 继续乘下去：9 乘 8 乘 7，一直乘到 1。 | 新增：小学就学过“连乘”。 |
| factorial / nine factorial / 3 factorial | 阶乘；9 的阶乘；3 的阶乘（symbols 9!, 3! only inside formulas） | 九的阶乘 | 数学家给这种连乘起了个名字：9 的阶乘，写成 9 后面加一个感叹号。 | 改：不说“简称”（那是缩写）。字幕写“9 的阶乘”，符号只出现在公式里。 |
| 255,168 and 362,880 (the headline numbers); all comma-grouped numbers | 255,168；362,880；131,184；77,904；46,080 | edge reads the digits correctly; for any other backend: 二十五万五千一百六十八 / 三十六万两千八百八十 … |  | 屏幕和字幕：半角逗号分节。edge 朗读正确，say: 不用手写数字。 |
| about 48 / 73 / 82 thousand | 约 4.8 万；7.3 万；约 8.2 万 | 约四点八万（edge default; no say: override） |  | 中文按“万”计。 |
| just over half / half / about 6 in 10 games / fewer than half | 一半多一点；一半；所有对局的一半；每 10 局大约赢 6 局；赢不到一半 | 每十局大约赢六局 |  | 改：加“每”表示比率。 |
| × = ≠ ≈ + − in subtitles and speech | 乘 / 等于 / 不等于 / 约等于 / 加 / 减；9 乘 8 等于 72；6 乘 5 等于 30；再减去 432 |  |  | 乘积一律“等于”，不用“得”。 |
| 10 to the power of 120 / a 1 followed by 120 zeros | 10 的 120 次方；1 后面跟着 120 个零（formula 10^{120} on screen） | 十的一百二十次方 |  | 感叹句以“零”结尾，不写“0！”。 |
| digits (6 digits) / = one digit | （6 位数）；= 一位数字 |  |  |  |

### 视频自造说法 / Phrases this video coined

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| ghost games / ghost endings / made-up endings | 幽灵对局（first subtitle in “”）；counter 幽灵对局计数：N；S08 每个幽灵对局算一次 | 幽灵对局 | 我们把这些编出来的对局叫作“幽灵对局”。 | 改：只用一个词“幽灵对局”，去掉“幽灵结局”。 |
| made-up moves after someone already won (caption) / never played | 有人赢了之后编出来的走法；从没下过 |  |  |  |
| real game(s) | 真实对局；每一局真实对局只算一次 | 真实的对局 |  |  |
| counted 24 times / count each real game only once / counted just once / counted 6 times | 被算了 24 次；每一局只算一次；只算了一次；算了 6 次 | 被算了二十四次 |  | 改：“被算了 24 次”“只算一次”，不用“数”。 |
| stop early / early win | 提前结束；提前赢 | 提前结束 |  |  |
| Pause and ponder | 暂停想一想（card title, explainer/locales/zh.yaml） | 暂停想一想：… |  | 改：朗读和卡片标题完全一致。 |
| Plan B | Plan B（caption: Plan B：让电脑把每一局都下一遍） | Plan B (English; tested fine on edge) | 手算变得这么乱的时候，我们还有 Plan B。 | 保留英文：日常中文就说 Plan B；旁白说它时，画面上正好显示 Plan B。 |
| Don't count cleverly | 别巧算了 |  |  | “巧算”正是小学的说法。 |
| counted by hand / counting by hand gets messy | 手算过；手算越来越乱 | 手算 |  | 用“手算”，避开“数数”（shǔshù）。 |
| tangled mess | 一团乱麻 |  |  | 意象相同的中文成语。 |

### 程序 / The program

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| computer | 电脑 |  |  | 孩子们说“电脑”；“计算机”像课本。 |
| program / prints / output / run | 程序；输出（程序只输出 3）；运行程序；label 输出 | 输出 |  | 说“输出”，不说“打印”。 |
| Python / programming language | Python；编程语言；label Python = 一种给电脑下指令的语言 | Python (English) | 我们用的编程语言叫 Python；在 Python 里，…… | 保留英文。 |
| list (Python list) | 列表 |  | 我们用一个列表来存 9 个格子。 | 中国的 Python 课都叫“列表”。 |
| spots in a list, numbered starting from zero | 列表里的位置从零开始编号 | 从零开始 |  | 像英文一样用“位置”；“索引 / 下标”放到配套练习里。 |
| dot "." | 点；label 一个点，重复 9 次 | 一个点 | 空格子里放一个点。 | 代码里的 "." 原样保留。 |
| function | 函数；label 函数 = 一小段有名字的程序 | 函数 | 接下来是一个函数：在编程里，函数就是一小段有名字的程序。 | 改：用“在编程里”点明，不和数学课的“一次函数”挂钩。 |
| mini-program | 一小段（有名字的）程序 | 一小段程序 |  | 绝不写“小程序”（微信小程序）。 |
| winner (the function) | winner；winner 函数；code winner(board) | winner (English; never at the start of a sentence) | 这个函数叫 winner，意思是“赢家”，它会检查每一条线。 | 保留英文，首次加注“赢家”；不放句首（会被读成“威娜”）。 |
| explore (the function) vs. exploring | explore 函数；探索 (the activity: chapter 探索每一局; 试走 → 探索 → 撤销) | explore (English) | 接下来是最巧妙的部分：一个叫 explore 的函数，explore 就是“探索”的意思。 | 函数名保留英文，首次加注“探索”，这样“试走 → 探索 → 撤销”能和代码对上。 |
| None (nobody) | None；label 没找到 → None（没有人） | None (English; ear-check, splice an English 'None' if misheard) | 如果没有一条线符合，winner 就什么也没找到，于是返回 None，意思是“没有人”。 | 保留英文并加注“没有人”；TTS 容易读成“难”，要人工听一遍。 |
| hands back (return) | 返回；S05 label 返回（交回结果）；返回数字 1 | 返回 | first label: 返回（交回结果） | 用标准词“返回”，第一次在标签上加注“交回结果”，避免理解成手机的“返回键”。 |
| == 'is the same as' / != 'is not' (S05 labels) | == 一样；!= 不是 | 一样 / 不是 |  | 改：“一样 / 不是”，避免和赋值的 = 混淆。 |
| for each line: squares a, b, c | 对每一条线：格子 a、b、c |  |  | 这个标签就是 for a, b, c in WIN_LINES: 的中文解释。 |
| other code names: board, player, next_player, total, square, range(9), WIN_LINES, print, play_all_games, def/if/for/in/not/is/return | Unchanged in code. Glossed by the existing side labels: ← 轮到谁：X 还是 O (player)；← 轮到对方 (next_player)；← 0 到 8 号格 (range(9))；累加到 total（总数）(total +=)；8 条获胜线 (WIN_LINES) | Never spoken in English except winner, explore, None (and never names with _ or brackets) |  | 代码名不翻译；每一行高亮代码旁边已有中文标签说明作用。 |
| add to the total (label on total +=) | 累加到 total（总数） | 累加 |  | “累加”是课本对 total += x 的说法；（总数）解释代码名。 |
| comment (# …) | 注释；label # … = 写给人看的说明（注释）/（电脑会跳过它） | 注释 |  | 中文版的代码注释也是中文，和这张卡片一致。 |

### 递归与回溯 / Recursion and backtracking

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| stopping rules | 停止条件；两个停止条件 | 停止条件 |  | 自然的说法，接近术语“终止条件”；视频里不说“递归出口”。 |
| finished game | 下完的对局 |  |  |  |
| call / calls itself / each call | 调用；自己调用自己；label 每调用一次：多一个棋子 | 调用 (diàoyòng; ear-check) |  | 标准术语；第一次出现时讲清编程里的意思。 |
| recursive / recursion | 递归 (card: 递归 + small grey tag 'recursion'; sub-line 函数自己调用（问）自己) | 递归 | 像这样，函数自己调用自己，也就是自己问自己同一个问题，就叫作递归。 | 中文。改：“函数自己调用自己，叫作递归”（递归是过程）。卡片加灰色小字 recursion。 |
| tree / upside-down tree / game tree | 树；一棵倒过来的树；整棵树（博弈树 in the companions only） | 一棵倒过来的树 |  |  |
| branch / chops whole branches off the tree | 分支；砍掉一大片分支 | 分支 |  | 用“分支”，不用“树枝”。 |
| leaf / leaves | 叶子；label 叶子 = 下完的对局 | 叶子 |  | “叶子节点”的口语说法，正式名放配套材料。 |
| whiteboard / one shared board | 白板；label 共用\n一个\n棋盘 | 白板 |  |  |
| undo / undo the move / the undo line | 撤销；撤销这一步；“撤销”那一行；label ← 撤销 | 撤销 | 这叫“撤销”这一步，这样下一个分支就能从头开始。 | “撤销”就是孩子们熟悉的 Ctrl+Z；代码里没有 undo 这个名字，注释写 # 撤销这一步。不用“悔棋”。 |
| backtracking | 回溯 (card: = 回溯 + small grey tag 'backtracking') | 回溯 | 先试走一条路，再退回来试下一条，这就叫回溯。 | 卡片加灰色小字 backtracking。 |
| try → explore → undo | 试走 → 探索 → 撤销 | 先试走一步，往下探索，再撤销 |  | 和循环注释 # 试走一步 / # 撤销这一步、以及 explore =“探索”呼应。 |
| winner check / spot a winner / draw check | 判断输赢（checklist 判断输赢；label ← 判断输赢；实验 2：删掉“判断输赢”）；exercise 10: 判断平局的那两行 | 判断输赢 | 删掉判断输赢的那两行 | 改：统一用“判断输赢”。 |
| Experiment 1 / 2; Break it on purpose!; still there | 实验 1：删掉“撤销”那一行；实验 2：删掉“判断输赢”；故意把程序改坏！；还在 | 故意把它改坏 | 想弄懂一个程序，有个好办法：故意把它改坏。 | 改：引号标出代码行的名字；“改坏”而不是“弄坏”。 |

### 结果与更大的棋 / Results and bigger games

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| solved (it has solved tic-tac-toe) | 把井字棋彻底算透了 | 彻底算透了 |  | 改：“破解”会联想到破解版。 |
| play perfectly / perfect play → draw / best for X / O's mistake | 双方都下得完美；双方都不失误 → 平局；对 X 最好；O 的失误 | 双方都不失误 |  |  |
| chess / chess programs | 国际象棋；国际象棋程序 | 国际象棋 |  | 绝不写“象棋”。 |
| Claude Shannon | 克劳德·香农；later 香农；label （香农，1950 年） | 克劳德·香农 | 1950 年，数学家兼工程师克劳德·香农估计…… | 通行译名（香农熵），用间隔号；那一刻双语字幕显示 Claude Shannon，所以标签从简。 |
| observable universe / atoms | label 可观测宇宙中的原子；narration 我们能观测到的整个宇宙 | 我们能观测到的整个宇宙 |  | 改：旁白用“我们能观测到的整个宇宙”。 |
| look a few moves ahead / estimate who's winning / practice games | 往后看几步 + 估计谁更有希望赢；≈ 谁更有希望赢？；（从几百万局练习中学来） | 往后看几步，再估计谁更有希望赢 |  | 改：不用“占优”“盘”。 |
| Recap | 小结 | 我们来小结一下 |  | 改：用“小结”。 |
| Your turn! / challenges / linked in the description | 轮到你了！；挑战题；程序 + 挑战题：链接在视频简介里 | 轮到你了 |  | “视频简介”在 B 站和 YouTube 都适用。 |
| Have fun exploring! | 动手去探索吧！ | 动手去探索吧 |  | 新增：呼应 explore = 探索。 |
| chapter titles and video title (meta.yaml) | 井字棋为什么恰好有 255,168 种对局？ \| 1 到底有多少种对局？ 2 填满棋盘：9 的阶乘 3 对局会提前结束 4 手算越来越乱 5 教电脑学规则 6 探索每一局 7 只改一行代码 8 255,168 是怎么来的 9 更复杂的棋，轮到你了 |  |  | 改：第 1、7、8、9 章标题。 |

### 配套材料 / Companions

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| minimax | minimax 算法（极小化极大算法） | minimax | minimax 算法（极小化极大算法） | 保留英文，首次附中文名。 |
| for loop | for 循环 |  |  | 课本和程序员都这么说。 |
| index (companions only) | 索引（也叫下标），从 0 开始 | 索引 | 编程课里把列表里的位置编号叫作“索引”（index），也有人叫“下标”。 | 视频里像英文一样说“位置”；配套材料给出课本和 CSP 的叫法。 |
| comment out (companions) | 注释掉（在行首加 #） |  |  | 第 9、10 题里“删掉”一行的安全做法。 |
| Warm-ups / Coding challenges / For the curious / Hint / Answer / Hint and solution / Expected answer | 热身（纸笔题）/ 编程挑战 / 想多了解一点 / 提示 / 答案 / 提示与参考代码 / 正确结果应为 131,184 |  |  | 代码答案只是众多正确写法之一，所以叫“参考代码”。 |
| Python 3, no extra installs needed / run it | 用 Python 3 就行，不需要安装第三方库；用 IDLE 打开，按 F5 运行，或在命令行输入 python play_all_games.py；playground.html 用浏览器打开就能玩 |  |  | 按中国课堂习惯写运行说明；说明 playground 不用安装任何东西。 |
| Tiny tic-tac-toe / two in a row wins | 迷你井字棋；两子连成一线就赢 |  |  |  |
| playground UI: Undo / New game / Games that can still happen from here / This game is finished… | 撤销 / 重新开始 / 从这里往后还可能出现的对局 / 这一局结束了：正好算 1 局。/ 在每个空格子上显示从这里往后的对局数 |  |  | 和视频用词一致（撤销、空格子、算）。 |

### 易错标签 / Tricky on-screen labels

| English | 字幕 / 屏幕 | 朗读 | 首次出现 | 说明 |
|---|---|---|---|---|
| places for first O: N / places for second O: N (S03 counters) | 第一个 O 的放法：N / 第二个 O 的放法：N (re: keys, number last) |  |  | 改：用“放法”不用“位置”，数字放最后。 |
| ghost endings counted: N / orders shown: N / games counted | 幽灵对局计数：N / 已列出的顺序：N / 对局计数 |  |  | 计数器用“计数”；数字放在全角冒号后的最后。 |
| X in 6 / X in 7 / X in 8 / O in 6 / O in 8 (S06 tree edges, f'{sym} in {s}') | X 下 6 号格 …（re:([XO]) in (\d) → \1 下 \2 号格） |  |  | 这是格子编号，写“N 号格”，不写“第 6”（会被当成第 6 步）。 |
| X wins 15,648 of 25,872 / X wins 14,232 of 29,592 (S08 bars) | 25,872 局中 X 赢 15,648 局 (re: key; whole before part) |  |  | 中文先说整体再说部分。 |
| X's 3rd mark: move 5 | 第 3 个 X：第 5 步 |  |  | t2c 键 X's 3rd mark 要译成“第 3 个 X”，颜色才保得住。 |
| this 1 game was counted / 24 times in 362,880 (two Text objects) | 这 1 局被算了 / 24 次（在 362,880 里） |  |  | 第二行保留两个上色的数字（24 和 362,880）。 |
| a dot, / 9 times; start: empty board, / X's turn; count each real game / only once; Count the games / that end on move 7; 1 game / (a draw) | 一个点，/ 重复 9 次；开始：空棋盘，/ 轮到 X；每一局真实对局 / 只算一次；统计在第 7 步 / 结束的对局；1 局 /（平局） |  |  | 拆成两个 Text 的标签要成对翻译，每一半单独读也通顺。 |
| S06 side labels | ← 轮到谁：X 还是 O；← 有人赢了？→ 1；← 棋盘满了？→ 1（平局）；← 0 到 8 号格；← 试每一个空格子；← 轮到对方；← 统计从这里往后有多少局；← 撤销；轮到 X / 轮到 O |  |  | 每个标签都是对应代码行的中文解释。 |
| S04 breakdowns and table | O 连成一线的方法；8 条线 × 6 种顺序 ×（6 × 5 × 4：3 个 X 的放法）；X 已经赢了；12 对（O 的线，X 的平行线）× 6 × 6；3 排 × 另外 2 排 + 3 列 × 另外 2 列 = 12 对；第几步结束 / 局数；X 之前赢了吗？/ O 之前赢了吗？/ 赢还是平局？；第 5 步就已经结束 |  |  | 中文内容用全角括号，纯数学用半角；“already over at move 5”不加！。 |
| S01/S02 labels | 井字棋有多少种不同的对局？；棋盘一样，顺序不同 → 不同的对局；旋转过的棋盘 → 也是不同的对局；100？/ 100 万？；仔细地算 / 一段短短的程序 / 它是怎么来的？；如果对局从不提前结束呢？；X 赢了！；从不提前结束 / 真实对局 / 太多了！/ 多出来的对局？ |  |  |  |
| S05/S07/S08/S09 labels | 棋盘 · 获胜线 · 判断输赢；不全一样 / 全是点；共用一个棋盘；还在；？！；棋盘满了；幽灵对局\n又回来了；手算过；在 4 条获胜线上；先下中心：X 每 10 局大约赢 6 局；先下边格：X 赢不到一半；X 总能赢吗？；整棵树也一样：；→ 平局；井字棋：255,168（6 位数）；国际象棋：至少 1 后面跟着 120 个零（香农，1950 年）；可观测宇宙中的原子：大约 1 后面跟着 80 个零；选择数相乘 → 9 的阶乘；对局会提前结束 → 幽灵对局；只统计 X 赢的对局；如果 O 先走呢？ |  |  |  |
| ponder cards | 井字棋一共有多少种不同的对局？\n把你猜的数写下来！ \| X 在第 5 步赢下的对局有多少种？\n提示：（1）哪条线？\n（2）X 按什么顺序填？\n（3）2 个 O 能放在哪儿？ \| 如果删掉\n“撤销”那一行，会怎样？ \| 这次改成删掉“判断输赢”。\n会输出什么数？\n（提示：你见过它！） \| X 的第一步下在哪儿，能下出的不同对局最多：\n角、边，还是中心？ | spoken ponder openers never end on 种: 暂停想一想：有多少种对局是 X 在第 5 步赢下的？ |  | MOST 的大写强调改成“最多”；读出来的问题不以“种”结尾。 |

## 规则

### A. 中英混用与用词 / Code-switching and vocabulary

- **A1** 中英混用的范围。只有这些保留英文：X 和 O；Python；画面上代码里的名字和关键字（explore、winner、None、board、player、next_player、total、square、range、WIN_LINES、print、play_all_games、def/if/for/in/not/is/return）；Plan B（旁白在“还有另一个办法”处可以说，因为那时画面正好显示它）；配套材料里的 minimax 和 for 循环。其余一律说普通话，用中国课堂和程序员实际用的词。不为“洋气”加英文（不要“这个 count 很 tricky”）。新词的判断标准：中国老师对这些学生会不会用英文说？翻译后会不会指向程序里不存在的东西？
- **A2** 代码名首次出现时加注一次。winner、explore、None 第一次读到时，在同一句里给出日常意思（这样仍是一句英文对一句中文）：这个函数叫 winner，意思是“赢家”，它会检查每一条线。/ 一个叫 explore 的函数，explore 就是“探索”的意思。/ 返回 None，意思是“没有人”。名字本身在画面、字幕和朗读里都保持英文；加注不等于改名，“探索函数”“赢家函数”仍然禁用。其他代码名由已有的中文侧标签解释（player → ← 轮到谁：X 还是 O；range(9) → ← 0 到 8 号格；total += → 累加到 total（总数））。不要为关键字另加新的画面元素：每一行高亮代码旁边已经有中文标签说明它做什么。
- **A3** 卡片上的英文小字。只有“递归”“回溯”两张卡片显示英文：中文词下方一个灰色小字 recursion / backtracking（在 s06_explore.py 里加几行，用 i18n.active() 判断）。如果不改场景代码，退而求其次：“= 回溯（backtracking）”，以及灰色副标题“recursion：函数自己调用（问）自己”。旁白不读这两个英文词。
- **A4** 用大陆简体中文：程序（不是程式）、函数（不是函式）、列表（不是串列）、递归、电脑、视频。绝不用“小程序”（指微信小程序），国际象棋绝不简称“象棋”（那是中国象棋）。本词表只管简体版；繁体/台湾版需要另做词表（井字遊戲/圈圈叉叉、程式、函式、遞迴）。
- **A5** 白话对白话，标准术语引入一次。英文特意用大白话的地方，中文也用大白话：is the same as → 一样；is not → 不是；mini-program → 一小段有名字的程序；spots in a list → 位置；who's winning → 谁更有希望赢；solved → 彻底算透了。中文有一个课本里处处可见的标准术语时，就用它，并用白话解释一次：hands back → 返回，由 S05 的标签“返回（交回结果）”引入。赋值的 = 绝不叫“等于”，需要说时用“放进 / 存进”。
- **A6** 函数的引入方式。用编程的意思引入（在编程里，函数就是一小段有名字的程序），绝不和数学课的“一次函数”挂钩：很多观众还没学过，而且数学里的函数并不是一段有名字的程序。“返回”“调用”同理：13 岁的孩子先想到的是日常意思，所以第一次出现时要讲清编程里的意思。
- **A7** “数”的用法。“被计入”用“算”（这一局被算了 24 次、每一局只算一次、只算了一次）；程序做的计数用“统计”（代码注释、挑战卡片、配套材料）；“数”（shǔ）只用于一个一个地数（数一数、数叶子）。计数器标签用“计数”（对局计数、幽灵对局计数：N）。不说“数数”（shǔshù），说“手算”。
- **A8** “对局”的量词。数“有多少种不同的对局”时用“种”：问题及其直接答案（标题 255,168 种对局、有多少种不同的对局？、1,440 种对局、5,328 种对局）。具体的一局（一局、这一局、每一局、叶子标签 1 局）、统计与拆分（X 赢了 131,184 局、1,440 局在第 5 步结束、表头“局数”）以及“下一局”用“局”。绝不用“盘”。同一处问“有多少种”，不能用“……局”来回答。
- **A9** 步、格、步骤。走棋的步数从 1 开始，写“第 N 步”。格子编号从 0 开始，写“N 号格”（绝不写“第 N 格”；树上的“X in 6”写成“X 下 6 号格”）。计数方法的阶段叫“步骤 / 第一、第二、第三”，绝不用“步”。
- **A10** “线”“排”“行”。棋盘上的线叫“线”（获胜线、对角线、连成一线）。棋盘的横行叫“排”（横排：最上面一排、3 排），竖的叫“列”（竖列）。代码的一行叫“行”（一行代码、“撤销”那一行、只改一行代码）。这样“行”永远指代码；“三子连成一线”绝不说成“连成一排”（排只指横的）。
- **A11** 旁白和字幕里的代码名照代码原样书写（大小写、下划线），朗读时不带括号（读 explore，不读 explore()），用英文读，绝不翻译、变形、加复数或加中文引号。只提画面上看得见的名字，其他代码用中文描述。代码名绝不放句首，前面要有中文词（这个函数叫 winner / 如果 winner…… / 而 explore……）。TTS 测试中，句首的 winner 被读成“威娜”，放在“叫”后面就正常。
- **A12** 人名。有通行译名的用译名（Claude Shannon → 克劳德·香农，之后简称香农；间隔号用 U+00B7 “·”）。双语字幕会显示英文原名，所以画面标签保持简短：（香农，1950 年）。没有通行中文译名的人名保留拉丁字母、用英文读（见 explainer/lexicon.yaml）。

### B. 排版与标点 / Typography and punctuation

- **B1** 空格。中文与拉丁字母、阿拉伯数字之间加一个半角空格，字幕、标签、代码注释和 say: 都一样（X 在第 5 步赢了、explore 函数、Python 里、1950 年、约 4.8 万、被算了 24 次）。TTS 词典靠空格匹配：Python 把汉字算作 \w，“返回None”永远匹配不上。全角标点旁边不加空格（……255,168。/ X 赢了！）。数字和代码名内部绝不加空格。公式保留英文的空格（9 × 8 = 72），紧凑标签照英文（×24、(4×3×2×1)）。不要用 U+00A0 / U+202F 冒充不换行空格：i18n.norm() 和 split_balanced() 用 str.split()，会把它们吞掉。
- **B2** 标点。中文用全角 ，。、；：？！（）“”‘’……《》；并列用顿号（0、1、2 号格；3 排、3 列和 2 条对角线）；“”用于首次出现的自造词（“幽灵对局”）、引用的词，以及动词后面的代码行名称（删掉“撤销”那一行、删掉“判断输赢”）。半角只出现在数字内部（255,168、4.8）、公式、代码、阶乘的“!”、表示未知数的单独“?”，以及警示牌里的“!”。单独的“?!”改成“？！”。括中文内容用全角（），括纯数学内容用半角 ()。
- **B3** 阶乘号与感叹号。半角“!”只出现在公式里。全角“！”绝不直接跟在数字或公式后面，要改写成以汉字结尾（“被算了 24 次！”可以；写“1 后面跟着 120 个零！”，不写“120 个 0！”）。“same 9 × 8 as before!”→“和前面一样：9 × 8”（不加！）。第 2 章标题用“9 的阶乘”，不用“9!”。

### C. 数字与数学 / Numbers and maths

- **C1** 画面和字幕上的数字。凡是数学内容（个数、结果、因数、步数、格子号、年份）一律用阿拉伯数字，分节用半角逗号，与英文画面完全一致（1,440 · 5,328 · 255,168 · 362,880）。标签里的数字串必须和英文一模一样，因为场景靠匹配这个字符串给数字上色（t2c）。数字里绝不能出现全角“，”（255，168 会被看成两个数）。约数用“万”加数字（约 4.8 万、7.3 万、约 8.2 万；标签“100 万？”）。英文拼成单词或习惯上用汉字的地方用汉字：一局（表示“一”）、两个停止条件、三个步骤、三子连成一线、一百？一百万？、从零开始。
- **C2** 公式与文字。画面上的公式保留英文符号和排版（× = ≠ ≈ ! ⋯ 10^{120}）；MathTex 里可以有中文（ctex）：\text{ 条线}、\text{ 种}；数学模式里保留 1{,}440 的写法（裸逗号会多出空格）。字幕像英文旁白一样用文字说运算：9 乘 8 等于 72；6 乘 5 等于 30（一律“等于”，不用“得”）；再减去 432；9 的阶乘；10 的 120 次方。读法：× 乘，+ 加，− 减，= 等于，≠ 不等于，≈ 约等于，n! n 的阶乘，10^n 10 的 n 次方。

### D. 旁白对齐与锚点 / Narration alignment and anchors

- **D1** 逐句对齐（explainer/i18n.py）。每条 SAY 逐句翻译：一句英文对一句中文（按 explainer.voice.split_sentences 切分），每句以 。？！ 结尾。句子内部不能出现 。？！：句中的问句用“：”或“，”，句内可以用“；”。例：'Take a guess. A hundred? A million? Pause the video and write your guess down.' → 猜一猜。/ 一百？/ 一百万？/ 暂停一下视频，把你猜的数写下来。只有朗读形式和显示文字不同时才写 say:（见 F 节）。写完运行 `python -m explainer.i18n check videos/tictactoe-255168`。
- **D2** 锚点。凡是 wait_until 短语里提到术语、数字、格子、步数或代码名的，都要加锚点，目标用本词表的写法（'nine factorial' → '9 的阶乘'，'Flipped or turned' → '翻转'，'a function called explore' → '叫 explore 的函数'）。目标必须出现在显示文字里，而且在那一句里唯一（time_of 取第一个匹配；X、第 5 步、9 的阶乘常常重复）。尽量用中文作目标：time_of 按字符位置估算时间，每个拉丁字母都算一个字，紧跟在长英文词后面的目标会触发得偏晚。
- **D3** 暂停想一想。卡片标题是“暂停想一想”（explainer/locales/zh.yaml），旁白开头就说“暂停想一想：……”。'Pause the video' → 暂停一下视频；'Pause and guess' → 暂停一下，猜一猜。提示编号用（1）（2）（3）。读出来的问题不能以“种”结尾：暂停想一想：有多少种对局是 X 在第 5 步赢下的？（卡片上可以写“X 在第 5 步赢下的对局有多少种？”）。

### E. 画面标签与代码 / Labels and code panels

- **E1** 标签与旁白一致。同一个意思，标签必须和旁白用同一个词（幽灵对局、撤销、回溯、获胜线、判断输赢、9 的阶乘、赢、返回、空格子），不用意思相同但字不同的简写（写“X 赢”，不写“X 胜”）。标签是简短的名词短语，每行最多约 12 个汉字，句末不加“。”。同样的 font_size，汉字看起来比拉丁字母大，所以按英文标签的外框来缩放中文，不要照搬 font_size。英文大写强调（the MOST）改成“最多”，场景能加中文 t2c 就上色，否则用普通字。
- **E2** 计数器。“文字：N”式的计数器，数字放在全角冒号后面的最后，用 strings.yaml 的 re: 键实现（board_tally 给最后 len(N) 个字形上色）。计数器写的是“个数”，不是“位置”：第一个 O 的放法：3（不写“第一个 O 的位置：3”，会被理解成“在 3 号格”）、幽灵对局计数：24、已列出的顺序：6、对局计数。
- **E3** 局部上色。场景用 t2c 给英文子串上色（'undo'、'draw'、'ghost games'、'(a draw)'、"X's 3rd mark"、'9 × 8'、'255,168'、'X'、'O'）。中文标签必须原样包含这些子串的中文（撤销、平局、幽灵对局、（平局）、第 3 个 X），并且 i18n 层要用同一张表翻译 t2c 的键（工具链工作，见 I 节）。X 和 O 保留字母，所以它们的颜色照常生效。
- **E4** 一个英文键，一个中文译文。strings.yaml 以英文原文为键，同一个英文字符串在所有位置得到同一个中文。选一个处处都通的中文（'games' → 局数，S04 表头和笔记本电脑计数器都适用；'center' → 中心；'1 game' → 1 局；'move 5' → 第 5 步），否则就改场景里的英文键。拆成两个 Text 的标签要成对翻译，每一半单独读也通顺（一个点，/ 重复 9 次；这 1 局被算了 / 24 次（在 362,880 里））。
- **E5** 代码注释用中文，并且通过本地化的程序文件显示到画面上，绝不通过 strings.yaml。在 `scenes/common.py` 里设 `PROGRAM_PATH = localized(ASSETS / "play_all_games.py")`（现在直接读 assets/，中文副本只会改变下载文件）。不要在 strings.yaml 里翻译代码行：s06_explore.py 的 glyphs() 和 comment() 按 SRC 的字符位置取字形，面板文字必须和源码一致。注释统一为：`# 横排` / `# 竖列` / `# 对角线` / `# 有人赢了` / `# 棋盘满了：平局` / `# 试走一步` / `# 统计从这里往后有多少局` / `# 撤销这一步`。S08 结尾那段代码写死在 s08_answer.py 里：用 strings.yaml 翻译，保留开头 4 个空格：`'    # (winner and explore from before)'` → `'    # （前面的 winner 和 explore）'`。`# 255168`、终端里的 `$ python play_all_games.py` 和输出 `255168` 不变。
- **E6** 中文版程序（i18n/zh/assets/play_all_games.py）。代码名、关键字、字符串（'X'、'O'、'.'）、数字和排版一律不变；中文只出现在行尾注释和文档字符串里，绝不用中文做代码名。所有行号保持不变：文档字符串仍是 5 行，explore() 仍在第 23–35 行，第 37、40 行仍在 S08 高亮的位置。不加“# -*- coding -*-”行（会让每行下移；Python 3 默认 UTF-8），存为无 BOM 的 UTF-8。检查方法：把两个文件的注释和文档字符串都去掉后 diff，结果必须为空。中文注释的渲染宽度不能超过英文原注释（等宽拉丁字母约 0.6 em，汉字约 1 em），因为 explore_code() 按最长一行把面板缩放到 EXPLORE_WIDTH；上面这套注释每一条都更窄。中文版下载文件就是这一个。

### F. 朗读（TTS） / Narration voice

- **F1** 声音。在 video.yaml 里设 `languages: {zh: {voice: {backend: edge, voice: zh-CN-XiaoxiaoNeural, speed: 1.0}}}`（女声，和英文版的 af_heart 对应）。按现在的代码，--lang zh 会失败：build.py 默认用 'kokoro-zh'，而 voice.get_backend() 不认识它；Kokoro 又会把所有文字都按 en-us 处理。免费的 edge 声音不接受自定义 SSML 或拼音，所以多音字和英文词只能靠改写或拼接音频解决。
- **F2** 只在实测出错的地方写 say:。edge 能按显示的数字正确朗读（255,168、362,880、29,592、77,904、1,440 和 1950 年都正确），所以 say: 保留显示的数字。必须写 say: 的情况：局、步前面的 2 → 两局 / 两步（edge 读成“二局”）；n! 绝不出现（写“n 的阶乘”；edge 把“9!”读成“九”，把“3! = 6”读成“三等于六”）。如果改用别的引擎，要按“万”分组写出读法（二十五万五千一百六十八、七万七千九百零四、四万六千零八十；量词前和“万/千”开头用“两”，算式和序数用“二”；年份逐位读），或者加一个先去掉数字间逗号的中文规范化步骤。
- **F3** say: 的卫生规则（朗读文本）。数字后面不跟“!”；不出现 × ÷ → ≈ == != += 等符号；不出现任何宽度的括号（edge 会把括号念出来，“递归（recursion）”会被整个读出）；代码名不带括号；不读带下划线或括号的名字（WIN_LINES、next_player、range(9) 会被读成“下划线”“左括号”）；分句不以“种”结尾（“多少种。”被听成“多少重”）；不加英文括注。如果做纯中文字幕，（recursion）/（backtracking）由字幕程序添加，绝不写进旁白文本，因为旁白文本也会送进 TTS。
- **F4** 普通话声音里的英文词。在 edge 上，X、Python、explore、winner（不放句首时）和 Plan B 都读成了英文；O 读“欧”，这是对的。None 无论怎么拼写，都被转写成“难/南/那”：它读出来时画面上一定有，后面也一定有“意思是‘没有人’”，但仍要找一个不懂 Python 的人听一遍；如果听错，就用同性别的英文声音拼接一个 None。发音修正放在分语言的词典里（explainer/lexicon.zh.yaml，按 EXPLAINER_LANG 选择，并计入 TTS 缓存键）；绝不要把 X、O、None、winner 放进共用的 lexicon.yaml（会改变英文视频，而且 EdgeBackend.respell() 会把英文拼读喂给中文声音）。
- **F5** 多音字：先改写，实在不行再按整词固定。本词表已经去掉了最麻烦的几个：横行叫“排”（棋盘话题里不出现读 háng 的“行”）、“空格子”（避开 kòng/kōng）、“被计入”用“算”（关键句里不出现 shǔ/shù 的“数”）、一律“等于”（避开“得”）、“手算”（避开“数数”）。其余的在草稿渲染里用耳朵检查：一行代码 / 那一行（háng）、数一数 / 数叶子（shǔ）、调用（diào）、重复 / 重新（chóng）、还（hái）、落（luò）、倒过来（dào）、角（jiǎo）、种（zhǒng）。任何修正都必须按整词：按单字把“行”定为 háng 会弄坏“运行”，把“数”定为 shǔ 会弄坏“数学家”“数字”。

### G. 字幕 / Subtitles

- **G1** 双语字幕。中文在上，英文原句在下，由 narration.yaml 配对；绝不为了配合中文去改英文。中文字幕行不加英文括注。一句中文控制在约 30 个宽度单位以内，好放进一条双语字幕（纯中文字幕每行 22），长句在“，”处断开。绝不在“第 5 步”“5 号格”“explore 函数”“1,440 局”“9 的阶乘”或任何数字、代码名中间断行。
- **G2** 字幕结尾。每条字幕末尾的“。”或“，”（以及“、；：”）去掉；“？！……”和后引号保留。字幕中间的标点照留。绝不用空格表示停顿：半角空格已经专门用于中文与字母、数字之间。

### H. 标题、语气与配套材料 / Titles, register and companions

- **H1** 标题（meta.yaml）。视频：井字棋为什么恰好有 255,168 种对局？章节：1 到底有多少种对局？2 填满棋盘：9 的阶乘 3 对局会提前结束 4 手算越来越乱 5 教电脑学规则 6 探索每一局 7 只改一行代码 8 255,168 是怎么来的 9 更复杂的棋，轮到你了。开头的标签“where does it come from?”写成“它是怎么来的？”，和第 8 章用词一致。
- **H2** 语气。称呼观众用“你”（或“我们”），绝不用“小朋友”“宝贝”。短句、具体，友好但不幼稚。不用网络用语（一键三连、yyds、三连），少用儿化。按意思传达英文的节奏，不逐字翻：Here's the catch. → 问题就在这儿。/ Not a chance. → 完全不可能。/ Surprise: → 没想到吧：/ sneaked in a win first → 抢先赢了 / Let's recap. → 我们来小结一下。/ Have fun exploring! → 动手去探索吧！选择疑问句用“还是”（轮到谁：X 还是 O；角、边，还是中心？），陈述句用“或 / 或者”。
- **H3** 受众前提。11–14 岁跨越小学五六年级到初二。不要默认他们学过数学里的函数、乘方（七年级）、阶乘（高中）、Python 或递归/回溯（高中选修 / CSP-J）；视频用大白话定义函数、列表、阶乘和递归，并在“10 的 120 次方”旁边保留“1 后面跟着 120 个零”。逗号分节没问题（四年级《大数的认识》就教三位一节）。
- **H4** 配套材料。提供 i18n/zh/exercises.md、i18n/zh/playground.html 和 i18n/zh/assets/play_all_games.py，按本词表翻译（热身、编程挑战、提示与参考代码、正确结果应为、for 循环、minimax 算法（极小化极大算法）、与视频一致的“翻转/旋转”、撤销、空格子）；中文视频简介里放链接（“视频简介”在 B 站和 YouTube 都适用）。代码块保留代码名，注释改成中文（# 平局也不算）。加一个“想多了解一点”板块，衔接课堂和 CSP 用语：索引（也叫下标）从 0 开始；== 在编程课里读作“等于”；递归口诀“问题一层层‘递’下去，答案一层层‘归’回来”；分步乘法计数原理（高中会学）；9 的阶乘 = 9 个格子的全排列数；删掉“判断输赢”后，explore 就是经典的全排列回溯程序；深度优先搜索（DFS）；撤销那一行就是 CSP 教练说的“恢复现场”；停止条件 = 终止条件（递归边界）；博弈树、叶子节点。按中国课堂习惯写运行说明：用 IDLE 打开，按 F5 运行，或在命令行输入 python play_all_games.py；不需要安装第三方库；playground.html 用浏览器打开就能玩。第 9、10 题写“删掉（或在行首加 # 把它注释掉）”。

### I. 中文版构建前的工具链工作 / Toolkit work needed before the zh build

- **I1** 字幕切分（explainer/subtitles.py）：要改代码，不能只靠人工检查。今天已复现：`_split_k('答案是 255,168。', 2, 30)` 返回 `['答案是', '255, 168。']`（数字中间被插了空格）；“1,440 局在第 5 步结束，5,328 局在第 6 步结束……”被切成“……5,328 局在第”/“6 步结束……”。修法：(a) `_cuts` 里，两个数字之间的“,”“.”后面不能切；(b) 挨着汉字的空格永远不是优先切点；(c) `_split_k` 重新拼接时，从原文切片恢复两段之间的原样文字，而不是猜用空串还是空格（现在插入空格，才出现“255, 168”）；(d) 不在“第 N 步”“N 号格”、数字加量词、代码名加“函数”中间切。用“答案是 255,168。”“X 赢了 131,184 局，O 赢了 77,904 局，46,080 局是平局。”和 1,440/5,328 那句写回归测试。在 `tracks()` 里实现 G 节的字幕结尾规则，并把短于约 1 秒的句子（一百？/ 一百万？/ 完全不可能。）并入下一条字幕。
- **I2** i18n 层。(1) 在 install() 里用 tr() 翻译 t2c / t2w / t2s 的键，让语义颜色保留下来（规则 E3）。(2) 扩展 `python -m explainer.i18n check`：检查 F 节的 say: 卫生规则、say: 与显示文字数字不一致的情况，以及场景里没有中文锚点的 wait_until 短语。(3) EXPLAINER_LANG=zh 时加载 explainer/lexicon.zh.yaml。(4) 修正 build.py 的 DEFAULT_VOICES（或者始终在 video.yaml 里设 languages.zh.voice）。(5) 未翻译字符串报告（build/i18n/missing.zh.json）会列出代码行：它们本来就该是英文。
