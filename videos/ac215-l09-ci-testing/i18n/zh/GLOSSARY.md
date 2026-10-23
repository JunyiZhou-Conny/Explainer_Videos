# AC215 第 9 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 9 — CI & unit testing: the pre-commit gate (follow-along: cheese-app-ci-cd + babykev)*（`videos/ac215-l09-ci-testing`）  
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：会 Python 和基础 ML，英文技术文档读得很顺；做过第 1–4 讲（VM、venv 和 uv、Docker 的 image 和 container、docker-shell.sh 和 entrypoint 的套路）；没写过 pytest 测试，没专门跑过 black 或 flake8，也没装过 git hook；开着自己 clone 的 cheese-app-ci-cd 和（第二部分）babykev，边看边敲命令。这一讲不需要云资源  
中文版：**只有字幕，没有中文配音**（docs/AC215_SERIES.md 第 8 条）。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l09-ci-testing.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5）都不适用，只保留显示规则  
英文原稿：`script.md`（SAY 行是旁白：92 段、335 句；SHOW 行是画面）；设计见 `BRIEF.md`（其中“Chinese glossary heads-up”一条已经考虑，见“关键决定”）  
先例：系列试点 [`ac215-l01-vms-venvs`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词（venv、lock 文件、pin、录制时）；容器几讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md)、[`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md)、[`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md) 定下容器、构建、层、缓存、挂载、port 的词和“只有字幕”的整套规则；最近的 [`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md) 定下“所有勘误统一说一个小疏漏”、带下划线的名字按旁白的说法写。前几讲已经定下的词一律沿用；新的是测试和代码质量的词汇（单元 / 集成 / 系统测试、hermetic、门禁、hook、格式化工具和 linter、覆盖率、fixture 和 marker、属性测试），以及 babykev 模型的几个词（mask、token、状态、问题）  
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“装个 hook”“跑一下 lint”“写个 fixture”“加个 marker”“commit 被拦了”“CI 挂了”“这个 mask 错了”。在实验课上硬说“钩子”“代码检查”“夹具”“标记”“掩码”，反而像说明书；这些书面词留给标题、章节名和配套文档（A4）。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、代码和配置里找东西。命令、参数、文件名、工具名、recipe 名、step 标签、错误代码、终端原文一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（测试、单元测试、集成测试、系统测试、冒烟测试、验收测试、测试金字塔、格式化、覆盖率、暂存、断言、属性测试、反例、类型检查）一律说中文，用中文软件测试、pytest 和 Git 资料里的标准译名，方便搜索。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、标签、进度条、课件标签、门禁表、掩码网格和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“把 repo clone 下来”“构建 image”“起一个 container”“跑一下 pytest”“装个 hook”“跑一下 lint”“commit 被拦了”“CI 挂了”。每个选择过三关：实验课上的真实说法；能搜到的标准中文名（中文 pytest、Git 和软件测试资料：单元测试、集成测试、系统测试、冒烟测试、验收测试、测试金字塔、覆盖率、格式化、暂存、断言、属性测试、反例）；和整个系列一致（第 1 讲定下共用的词，第 2–5 讲定下容器和 Docker 的词）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、image / container / 工具的名字、recipe 名、step 标签、配置键、错误代码、终端原文，以及进度条上 README 的 Part / Option 名称）逐字照抄，不翻译、不变形、不加引号。检查器逼出来的例外（实物里有下划线、=、< >、+ 或括号）按旁白的说法写（A6），英文行显示原样（D4）。终端输出、代码面板、README 卡片、标签、进度条、课件标签、门禁表和思考题卡片都是英文，只翻译旁白。
2. **实验课口语里的英文，封闭清单**：第 1–5 讲的 venv、root、repo、clone、commit、pin、container、image、Dockerfile、tag、port、localhost、API、ID、bug；**这一讲新增 hook、linter 和 lint、hermetic、fixture、parametrize、marker、assert、recipe、mask 和 causal mask、token、milestone、CI**。
3. **其余用中文标准术语**：测试、单元测试、集成测试、系统测试、冒烟测试、验收测试、测试金字塔、边界、门禁、门禁表、闸机、格式化工具、格式化、格式检查、问题（工具报出的 finding）、宽度、覆盖率、覆盖率下限、收集、收集器、摘要、容差、跳过、排除、暂存、重新暂存、工作区、历史、交接链、卫生检查、私钥、合并冲突标记、配置、配置文件、lock 文件（第 1 讲）、依赖组、运行时依赖、开发工具、包管理器、命令运行器、类型检查器、诊断、文档、属性测试、反例、收缩、状态、问题（babykev 的问题）、兄弟问题、序列、逐位相同、参数、服务器、接口、处理函数、路由、校验、测试客户端、黑盒、退出码、构建、重新构建、层、缓存、挂载、凭据、计费。
4. **视频里的比喻按意思译，一个比喻一个词**：门禁（gate）、闸机（turnstile）、历史（HISTORY 金库）、托盘（输入的三个托盘）、边界（hermetic 的边界）、网线 / 那根线（network wire）、收集器（collector 扫过）、交接链（hand-over chain）、烟雾报警器（smoke detector）、日记（为了迁就 bug 改过的测试）。
5. **标题、meta.yaml 和配套文档用书面语体**：容器、镜像、仓库、克隆、提交、钩子（hook）、代码检查工具（linter）、质量门 / 门禁、封闭测试（hermetic）、掩码（mask）。
6. 双语字幕带把英文原句放在每行中文下方，所以中文行不加任何括注（检查器在没有 say: 时也不允许括号）。
7. 工具链的约束也是原则的一部分：一个英文句子对一个中文句子（92 段、335 句）、显示行能通过检查器（D3）、SAY 把实物念成单词的地方一律加 en_display（D4）。大陆简体中文；轻松、清楚的实验课口语，不油滑。

## 关键决定

- **门禁（gate）是主线词**（A1、A4、A7）：字幕和文档都说“门禁”“门禁表”，turnstile 是“闸机”；标题跟 video.yaml 的 Bilibili 标题一致，写“提交前的质量门”。第 4 讲的“关卡”是另一张图（账号、角色、API 三道关），不混用。
- **hook、linter / lint、hermetic、fixture、parametrize、marker、recipe、mask、token、CI 说英文**（A1 c）：BRIEF 的提示（commit、hook、pre-commit、pytest、fixture、marker、black、flake8、ruff、uv、just、lockfile、coverage、CI 保留英文；格式化工具 vs linter）大部分照用。**两处不同**：lockfile 沿用第 1 讲的“lock 文件”；coverage 说“覆盖率”——中国工程师就这么说，publish.description_zh 也写“覆盖率 94%”，而 SAY 里从没把 coverage 当工具名说。这两处是待 Conny 确认的决定。
- **recipe 不译成“配方”**（A1 c）：“配方”是系列里 Dockerfile 的比喻；just 的 recipe 保留英文（just 这个 recipe、setup 这个 recipe）。
- **测试结果照终端写**（A1 a）：11 passed、10 passed, 1 warning、1 passed, 4 skipped、2 failed, 50 passed、1 failed, 102 passed、8 failed, 95 passed、1 passed, 103 deselected、Skipped、Failed、files were modified by this hook、nothing to commit、WRONG、command not found；旁白自己的话照常翻译（跳过、失败、通过）。
- **README 的 Part / Option 照进度条写，视频自己的部分说“第一部分 / 第二部分”**（A7）：Part 2 用两个工具找代码质量问题；Option 2 先等等；第二部分是 Rahul Dave 的客座讲座。
- **babykev 的步骤照 tag 写**（A10）：step-00、step-01 … step-04b、step-05、step-05a、step-05b；tag 不放在句首（到了 step-05a……）。英文行里 SAY 念成单词的（step zero zero、Step five a）给出 step-00、Step 5a（D4）。
- **带下划线的名字和检查器不收的符号**（A6、B3）：test_broken → test 下划线 broken；test_*.py → 文件名以 test 下划线开头；--max-line-length=120 → --max-line-length 设成 120；DEV=1 → DEV 设成 1；line-length = 100 → line-length 设成 100；torch.ones_like → torch 的 ones like；branch_mask → branch mask；power(3, 2) → power，参数是 3 和 2；(3, 4) → x 是 3，y 是 4；Ctrl+C → Ctrl-C。英文行用 en_display 给出字面形式（D4）。
- **S13 的平台说明温和、如实**（A9）：这台 Linux 机器上 1 failed, 102 passed；作者的 Mac 上 103 个全部通过，walk.md 里有记录；hermetic 只保证“只有你的代码能让它失败”，跨机器逐位一致是更强的承诺。绝不说成 babykev 的 bug 或观众的错。
- **画面标签照画面写**（同第 2–5 讲）：黄色的 your turn 标签、灰色的 extra 标签。旁白自己说的照常翻译：额外检查、进度条、门禁表、闸机、四个灰点、标题行（A11）。
- **录制时**：at the time of recording 每次都译“录制时”，绝不省略（大约一分钟、26.10.1 和 7.4.1、pytest 9 的 1 warning、4.7.0、0.13.2、38 个包和 torch 2.14.1、大约 95 MB、那几条无害的警告）（A9）。
- **按英文时间轴读**：中文是边听英文边读的，每句中文读起来的时间要和英文听起来差不多；删掉多余的连接词和重复的主语，绝不删内容；长实物（uvicorn api.service:app、externally-managed-environment、pre-commit run --all-files）英文没重复的地方不要重复（D8）。

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的一个中文句子，k 从 0 数），每一句都和 narration 里的句子一致，都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 开场：bug、门禁与跟练 / The opening: the bug, the gate, the follow-along

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| commit / git commit / a commit / history | commit / git commit / 历史 / 提交（书面） | S01[1]：你输入 git commit。 | 实验课口语（A1 c，第 1 讲起）。再 commit 一次；一个真正的 commit 进入了历史（HISTORY 金库那张图）；没有生成 commit；它永远不能 commit。书面写“提交”（A4）。 |
| gate / a gate / the gate table / the turnstile / anything that can fail and stop you | 门禁 / 门禁表 / 闸机 / 质量门（标题） | S01[1]：课上给能说不的东西起了个名字：门禁，也就是任何会失败、能拦住你的东西。 | 这一讲新增。字幕和文档都说“门禁”（CI 门禁是工程师的日常说法）；“质量门”只用在标题（publish.title_zh）。和第 4 讲的“关卡”分开（A7）。门禁长了牙；在闸机外面；门禁表填满了。 |
| say no / refuse / refusal / the gate refuses / is refused / blocks a commit | 说不 / 拒绝 / 拦下 | S01[1]：今天我们就在你的电脑上搭一个门禁，看着它拒绝一次 commit。 | 这次 commit 被拦了两道；拦下 commit。 |
| machine learning system / the model is a few tiles in a big grid / engineering | 机器学习系统 / 工程 | S01[2]：先退一步看：在一个机器学习系统里，模型只是一大张格子里的几块；其余都是工程。 | tiles → 几块（一大张格子里的几块）。 |
| no cloud, no credentials, no bill / billable / credentials | 凭据 / 计费 | S01[3]：不用云，不用凭据，没有账单：一切都在你的笔记本上跑，这正是重点。 | 凭据（S01、S15：下节课会用到云上的凭据）；今天没有任何计费。 |
| the tracker / 6 sections / the yellow your-turn tag / a gray extra tag / the study guide | 进度条 / your turn 标签 / extra 标签 / 学习指南 | S01[4]：看到黄色的 your turn 标签，就暂停，自己跑这条命令。 | A11、D6，同第 2–5 讲。6 sections today → 今天一共 6 段（C1）。 |
| bug / the buggy line / the wrong square root / revert / the repo's log | bug / 有 bug 的那一行 / revert / log | S02[0]：接着课堂演示把那个错的平方根混了进去，后来又被 revert 拿掉了。 | bug 是实验课口语（A1 c）。revert 照 git log 的写法；这个 repo 自己的 log；额外跑一下 git log。 |
| distance / origin / square root / radius / overshoots the circle | 距离 / 原点 / 平方根 / 半径 | S02[1]：有 bug 的那一行返回 50 的平方根，大约 7.07：冲出了这个圆。 | the point 3 comma 4 → 一个点：x 是 3，y 是 4（A6）；x 的平方加 y 的平方，再开平方。 |
| executable specification / suspects / a diary | 可执行的规格说明 / 嫌疑人 / 日记 | S02[2]：测试就是可执行的规格说明，这个测试本来会在任何人看到演示之前就说不。 | 两个嫌疑人；先相信测试，去改代码；课上的规则；改代码，不改测试（S10）。 |
| trays / normal / edge / invalid / zero exponents / infinity / not a number | 托盘 / 正常 / 边缘 / 非法 / 边缘情况 / 无穷大 / 非数值 | S02[4]：课上把输入分进三个托盘：正常、边缘和非法。 | edge → 边缘（绝不写“边界”，那是 hermetic 的边界，A7）；前面那个非法输入的托盘。 |
| power function / power / 2 to the power 3 / squaring x / a type error / TypeError | power 函数 / power / TypeError | S02[4]：对这里的 power 函数来说，2 的 3 次方是正常输入；指数为零、无穷大和非数值都是边缘情况。 | 函数名照写（A1 a）。power of 3 and 2 → power，参数是 3 和 2（A6）；a type error → TypeError（测试里写的异常名）。 |

### 测试的类型 / Kinds of test

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| test / tests / test file / test folder / suite / the test run | 测试 / 测试文件 / 测试目录 / 测试集 | S02[2]：有一个现成的测试早就知道正确答案。 | A3。字幕里除了实物（tests/unit/、tests 目录、test 下划线 broken）不写 test。每个测试集；两个测试集一起跑。 |
| unit test / unit tests / a unit test | 单元测试 | S03[0]：单元测试完全绕开应用，只单独调用这一个函数。 | A3。书面同。 |
| integration test / integration tests / the integration suite | 集成测试 | S03[1]：集成测试把我们自己的几个部分连起来。 | A3。系统测试文件管自己叫集成测试。 |
| system test / system tests / the system row / the system command | 系统测试 | S03[2]：系统测试把运行中的程序当成一个黑盒。 | A3。marked system（marker）→ 标上了 system；系统测试这一行。 |
| smoke test / the smoke / just smoke local | 冒烟测试 / just smoke local | S03[5]：还有两类测试只占淡淡的两行：冒烟测试，只问它有没有响应；还有验收测试，这个项目暂时还没有。 | A3。在真实模型上跑冒烟测试；那换上正确的 mask，冒烟测试呢？ |
| acceptance test / acceptance tests | 验收测试 | S03[5]：还有两类测试只占淡淡的两行：冒烟测试，只问它有没有响应；还有验收测试，这个项目暂时还没有。 | A3。for now → 暂时。 |
| testing pyramid / many cheap unit tests / few expensive system tests | 测试金字塔 | S03[3]：叠起来，就是测试金字塔：底层是大量便宜的单元测试，顶上是少量昂贵的系统测试。 | 标准中文，书面同。 |
| hermetic / non-hermetic / non hermetic tests / the hermetic claim / not hermetic | hermetic / 不 hermetic / 封闭测试（书面） | S03[4]：一个测试是 hermetic 的，指的是只有你的代码能让它失败。 | 保留英文（A1 c）：课上的词，也是画面上门禁表和边界的标签，中文没有公认的译法（封闭、密封、自包含各说各的）。不放在句首（所谓 hermetic……，A5）。书面写“封闭测试（hermetic）”。 |
| border / a sharper lens / the border picture / inside / outside | 边界 / 视角 / 边界图 | S03[4]：课上还给了一个更锐利的视角：一条边界。 | hermetic 的边界；绝不用于边缘输入（边缘，A7）。在边界图上；这 4 个站在外面。 |
| black box / the running program / a real network wire / the wire | 黑盒 / 网线 | S03[2]：请求离开测试，穿过一根真实的网线到达 port 9000，再以 JSON 的形式回来。 | 请求真的穿过了那根线。 |
| request / handler / routing / validation / test client / in process / no server and no network / FastAPI | 请求 / 处理函数 / 路由 / 校验 / 测试客户端 / FastAPI | S03[1]：测试客户端把请求直接交给 FastAPI 应用，在同一个进程里：路由、校验、处理函数和 power 全都跑了，但没有服务器，也没有网络。 | the app → 应用（同第 2 讲）；get euclidean distance, with x 3 and y 4 → GET euclidean distance，x 是 3，y 是 4（A6）。 |
| kind / a test's kind is named by what runs, not by its folder | 类型 / 哪一类 | S03[5]：关于类型说一句：测试属于哪一类，看的是实际运行了什么，而不是它放在哪个目录。 | A7：和“类”（Python 的 class）分开。 |
| marker / markers / labels for selecting tests / select on purpose / deselect / deselected | marker / 记号 / 选中 / 排除 | S03[5]：这个 repo 的系统测试文件管自己叫集成测试，它的 pytest 配置还定义了一些 marker，也就是用来挑选测试的记号，却没人用；marker 会在第二部分回来。 | 保留英文（A1 c；pytest 的词，BRIEF 的提示）。默认把这个 marker 排除在外；终端打印的 1 deselected / 103 deselected 照写。 |
| gate table columns / what is checked / on every commit | 空表 / 四列 | S03[6]：检查什么，怎么检查，用哪条命令，以及是不是每次 commit 都跑。 | 门禁表的四列（A11：表本身在画面上是英文）。 |

### cheese 应用与 Docker / The cheese app and Docker

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| clone / repo / the README / clone or download from your repository / cheese-app-ci-cd | clone / repo / README / cheese-app-ci-cd / 仓库（书面）/ 克隆（书面） | S04[0]：README 只说从你的仓库 clone 或下载，没给地址，所以这里给出 repo 的地址。 | 同第 1–5 讲；引用 README 时写“你的仓库”（A4）。Clone it → 先 clone（A5）。 |
| ls dash l a / test folders / pytest config / pre-commit config | ls -la / pytest 配置 / pre-commit 配置 | S04[1]：额外看一圈，README 里没有这一步：ls -la。 | D4：ls dash l a → ls -la。 |
| image / container / build / rebuild / cached / cheese-app-api tagged local | image / container / 构建 / 重新构建 / cheese-app-api:local / 镜像（书面）/ 容器（书面） | S05[1]：先构建 image：cheese-app-api:local。 | A2。tagged local → cheese-app-api:local（D4）；旁白说 the image 指镜像名时 → image 名。 |
| sh docker-shell.sh / docker-shell again / shell / prompt / the user is app, not root / the ID changes every run | sh docker-shell.sh / shell / 提示符 / app / root / ID | S04[2]：看一下提示符：用户是 app，不是 root，而且 ID 每次运行都会变。 | 第 2–5 讲。docker-shell again → docker-shell.sh（A5）。 |
| server / start the server / live server / detached / named api-server / control C / stop and remove the server | 服务器 / 运行中的服务器 / 在后台 / api-server / Ctrl-C | S08[0]：在后台启动一个服务器，名字叫 api-server，用 port 9000，DEV 设成 1。 | 第 1 讲。control C → Ctrl-C（两行都这样写；A6 不允许 +）。服务器晚一秒起来；服务器要是没起来。 |
| uvicorn api dot service colon app / host / port 9000 / with reload / the reload flag / application startup complete | uvicorn api.service:app / host / port 9000 / --reload / Application startup complete | S04[3]：在里面启动服务器：uvicorn api.service:app，host 是 0.0.0.0，port 是 9000，加上 --reload。 | G3：长命令按旁白的说法分段写，英文行给出完整命令（D4）。The reload flag → 参数 --reload（A5）。 |
| endpoint / health endpoint / README URLs / JSON object / distance field / curl | 接口 / health 接口 / URL / JSON 对象 / distance 字段 / curl | S04[4]：实际上它返回的是一个 JSON 对象，其中 distance 字段是 5.0，代码里写得很清楚。 | endpoint → 接口（第 1 讲）。不停地 curl health 接口；三次 curl。 |
| One small gap / a small slip / the README says | 小疏漏 | S04[4]：有一个小疏漏：README 说这个接口返回 5.0。 | A9，同第 5 讲：所有勘误统一说“一个小疏漏”。 |
| dash dash rm / nothing is left behind / docker ps dash a / exit | --rm / docker ps -a / exit | S04[5]：因为这个 shell 脚本用了 --rm，什么都不会留下；额外跑一下 docker ps -a 就能确认。 | D4。 |
| mounted / not mounted / the copy baked into the image / until you rebuild / yesterday's copy / you test the past | 挂载 / 副本 / 打包进 image | S04[5]：先提醒一句，很快就会用上：你的文件没有挂载进这个 container。 | A2。先提醒一句，很快就会用上；第一部分的那句提醒这时用上了。 |
| Dockerfile / copies pyproject.toml / installs the dependencies / one fat layer / four thin copy lines / the entrypoint / PATH / its exec line | Dockerfile / 依赖 / 层 / COPY / entrypoint / PATH / exec | S07[0]：这个 entrypoint 把 pytest 放进 PATH，它的 exec 那一行再把 container 交给你传进来的任何命令。 | A2。four thin copy lines → 四行薄薄的 COPY（照画面写指令名）。 |
| exit code / fail a CI step / the whole job fails | 退出码 / CI 的一个步骤 / 整个任务 | S07[0]：靠的是 container 的退出码，docker run 才能让 CI 的一个步骤失败。 | job → 任务（CI 的 job；第 21 讲会展示 job 图）。 |
| docker run, dash dash rm, the image, pytest tests slash unit / with network host, pytest tests slash system / DEV equals 1 | docker run --rm / pytest tests/unit/ / --network host / pytest tests/system/ / DEV | S08[2]：现在是 README 里的系统测试命令：docker run 加上 --network host，跑 pytest tests/system/。 | G3：分段描述；英文行见 D4。DEV equals 1 → DEV 设成 1（A6）。 |
| dev tools / runtime dependencies / open ended pins / no lockfile / groups behind one lockfile | 开发工具 / 运行时依赖 / 依赖组 / lock 文件 | S07[5]：这个 image 把开发工具当成运行时依赖一起发布，版本只有下限，没有 lock 文件；客座讲座则把它们放进依赖组，由一个 lock 文件锁住。 | lockfile → lock 文件（第 1 讲）；版本只有下限；pin 住的是 lock 文件；冻结的是 image。 |

### 格式化工具与 linter / Formatter vs linter

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| formatter / format / formatting / reformat / rewrites code into one layout / never changes behavior | 格式化工具 / 格式化 / 重新格式化 / 排版 | S05[0]：格式化工具把代码改写成统一的排版，从不改变行为。 | A3 / A7。先格式化，再 lint；有 2 个文件会被重新格式化。 |
| linter / lint / linted / config linting / lints the Dockerfile | linter / lint / 代码检查工具（书面） | S05[0]：而 linter 只负责报告：风格问题、可能的 bug、需要人来处理的地方。 | 保留英文（A1 c）。测试代码从来不做 lint；配置文件的 lint；hadolint 对 Dockerfile 做 lint。 |
| quality issues / code quality / style issues / likely bugs / things needing a person | 代码质量 / 质量问题 / 风格问题 | S05[0]：Part 2 用两个工具找代码质量问题，这两个可别搞混。 | Part 2 是 README 的一部分（A7）。 |
| finding / findings | 问题 | S05[2]：在 utils.py 里发现两个问题，逗号后面少了空格，还有空行太多：都是故意留下的乱代码。 | 工具报出的一条 finding 就是一个“问题”（A7）。几乎扫掉了所有问题。 |
| black / flake8 / ruff / F401 / E501 / an unused import / a long quoted sentence | black / flake8 / ruff / F401 / import | S09[7]：这次 commit 被拦了两道：black 重新格式化了文件，flake8 报出 F401，这是任何格式化工具都修不了的；git status 确认 commit 没有生成。 | 工具名照画面小写，不放在句首（A5）。一个没用到的 import；ruff 一个工具兼两个角色。 |
| width / line length / max line length 120 / its default of 88 / 79 / a 95 character line / the width war / line length 100 | 宽度 / --max-line-length / line-length / 默认的 88 | S05[4]：宽度 88 时，black 把那一行折成三行；宽度 120 时，又展开回一行。 | max line length 120 → --max-line-length 设成 120；line length 100 → line-length 设成 100（A6）。折成 / 展开回；宽度之争。 |
| check and diff mode / dash dash check / dash dash diff | --check / --diff | S05[3]：然后是 black，用 --check 和 --diff 模式。 | D4。 |
| Option B / on the host / pip install black and flake8 / externally managed environment / Homebrew Pythons / pipx / one-liner | Option B / 宿主机 / externally-managed-environment / Homebrew / pipx | S05[5]：如果 pip 拒绝，报 externally-managed-environment，Homebrew 的 Python 就会这样，那就用第 3 讲的任意一个虚拟环境，或者 pipx；学习指南里有那一行命令。 | pip 的报错照原样写（第 1 讲也保留 externally managed）；virtual environment → 虚拟环境（第 1 讲）。 |
| safe automatic fixes / unsafe fixes | 安全的自动修复 / 不安全的修复 | S10[4]：有意识地用上不安全的修复，又去掉 32 个；剩下 37 个，这些得靠人。 | ruff 的 --fix 和 --unsafe-fixes（照旁白用文字说）。 |

### pytest

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| pytest / pytest.ini / the config file / options / dash r a / the summary | pytest / pytest.ini / 配置文件 / 选项 / -ra / 摘要 | S06[0]：它还给每次运行加上一些选项，要记住的是 -ra：凡是没有干脆通过的，都会列进这份摘要。 | A5：不放在句首（这时 pytest……）。pytest 9（C2）。 |
| collect / collected / collector / discovery by convention | 收集 / 收集器 / 按约定发现 | S06[1]：看收集器扫过 tests 目录：每个匹配的名字都亮起来，一共 26 个测试。 | A3。是一把双刃剑。 |
| test underscore something / Test / test underscore / test underscore star / test underscore broken / def broken, assert False | test 下划线 / Test / test 下划线 broken / def broken / assert False | S06[3]：想真的让构建失败，就把它叫作 test 下划线 broken。 | A6：test_*.py、Test*、test_*、test_broken 和 def broken(): assert False 的原样写法在英文行（D4）。 |
| break the build / passed / failed / skipped / headline / gray dots | 变红 / 构建失败 / 跳过 / 标题行 / 灰点 | S08[5]：1 passed, 4 skipped，标题行还是绿的。 | 终端计数照打印写（A1 a）；skip → 跳过；标题行；四个灰点，不算失败。 |
| assert / assert rewriting / pytest dot approx / tolerance / floats / pytest dot raises | assert / pytest.approx / pytest.raises / 容差 / 浮点数 | S06[4]：普通的 assert 会被改写，失败时两边的值都会显示出来。 | A3。pytest 的三个动作。 |
| fixture / client / asks for client by name / builds and injects it / a fresh one or the whole run shares one / module global | fixture / client / 注入 / 模块级的全局变量 | S06[5]：用 fixture 会更好。 | 保留英文（A1 c）。有一个设置决定……（fixture 的 scope，旁白没点名）。 |
| parametrize / folds four copies into one function with four inputs | parametrize | S06[5]：而 parametrize 把四份副本折成一个函数，带四组输入。 | 保留英文（A1 c）；文档里写“参数化（parametrize）”。 |
| coverage / the coverage run / 0 percent / coverage reads 94 percent / a list of lines nobody has asked about, not a score | 覆盖率 / 跑覆盖率 | S07[3]：覆盖率是一份没人问过的代码行清单，而不是一个分数。 | 标准中文（A3）。BRIEF 的提示把 coverage 列为保留英文；但中国工程师说“覆盖率”，publish.description_zh 也写“覆盖率 94%”，所以字幕用“覆盖率”；SAY 里从没出现 coverage 这个工具名。 |
| coverage floor / the floor / a 90 percent coverage floor / FAIL Required test coverage / 49.4 percent | 覆盖率下限 / 下限 | S11[2]：下限是门禁，不是目标。 | 下限不变；覆盖率下限一句话说完。 |
| the HTML report / the terminal report | HTML 报告 / 终端里的报告 | S07[4]：有一个陷阱：HTML 报告生成在一个会被 --rm 删掉的 container 里，一 exit 就没了。 | 旁白没点名 term-missing。 |
| warning / 1 warning / a warning this config hides / a harmless warning | 警告 / 1 warning | S07[2]：那个 1 warning 是录制时 pytest 9 的摘要行，把这份配置隐藏掉的一个警告也算了进去：测试相同，结果也相同。 | 终端打印的 1 warning 照写；旁白自己说的 warning → 警告；harmless → 无害的（A9：总带“录制时”）。 |

### 悄悄的跳过 / The silent skip

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| skip / why does it skip / probes the server once, when pytest collects the module / marks the whole class | 跳过 / 探测 / 整个类 | S08[6]：测试文件只探测一次服务器，就在 pytest 收集这个模块的时候。 | the class（Python 的 class）→ 类（A7）。 |
| SKIPPED, API not running at localhost 9000 / localhost | SKIPPED / API not running at localhost:9000 / localhost | S08[5]：只有 -ra 的摘要说了实话：SKIPPED，API not running at localhost:9000。 | 终端原文照写（A1 a）；D4。 |
| a smoke detector with its battery removed will never beep | 烟雾报警器 | S08[6]：拔了电池的烟雾报警器永远不会响，但这不等于没有着火。 | 视频里的比喻（总原则 4）。 |
| readiness wait / health endpoint loop | 循环 / 有回应 | S08[1]：我们先额外加一步：一个循环不停地 curl health 接口，直到它有回应。 | CI 的做法很响亮。 |

### pre-commit 与 hook / pre-commit and hooks

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| hook / hooks / hook file / a policy hook / one local hook / the hook runs exactly what you type | hook / hook 文件 / 策略 hook / 本地 hook / 钩子（书面） | S09[1]：Git 在每次 commit 之前都会运行这个 hook 文件。 | 保留英文（A1 c；BRIEF）。量词“个”（九个 hook）。书面写“钩子（hook）”。 |
| pre-commit / pip install pre-commit / pre-commit install / pre-commit run / dash dash all dash files / pre-commit uninstall | pre-commit / pre-commit install / pre-commit run --all-files / pre-commit uninstall | S09[4]：想让它们照样跑一遍，就用 pre-commit run --all-files。 | 工具和命令照写；小写的实物不放在句首（在 pre-commit 配置里……）。 |
| dot git / outside the repository / every clone installs it again / hands over to pre-commit / the hand-over chain | .git / 交接链 | S09[1]：它放在 .git 里，不属于 repo 的内容：每个 clone 都要重新安装。 | D4：dot git → .git。和前面一样的交接链。 |
| hygiene guards / from whitespace to private keys / large files / merge markers / detect private keys hook | 卫生检查 / 空白字符 / 私钥 / 大文件 / 合并冲突标记 / detect-private-key | S09[2]：配置里列了九个 hook：七个卫生检查，从空白字符到私钥。 | the detect private keys hook → detect-private-key 这个 hook（画面上的 hook id，D4）。 |
| only Python files under src / the tests are never linted | src | S09[2]：再加上 black 和 flake8，宽度都是 120，都只看 src 下面的 Python 文件：测试代码从来不做 lint。 | files: ^src/.*\.py$ 从不写出来；旁白用文字描述。 |
| clean tree / staged files / nothing was staged / re-stage / git add dash u / git diff / git status | 工作区 / 暂存 / 重新暂存 / git add -u / git diff / git status | S09[6]：两个额外步骤把这个循环走完：git diff 显示改了什么；git add -u 把它重新暂存。 | stage → 暂存（Git 中文文档：暂存区）；on a clean tree → 工作区是干净的。 |
| skipped / nothing to commit / Failed / files were modified by this hook / no files to check | Skipped / nothing to commit / Failed / files were modified by this hook | S09[4]：六个 hook 通过，一个没有文件可查，然后 black 失败：files were modified by this hook；它重新格式化了 utils.py。 | 终端原文照写；旁白自己的话照常翻译（black 失败；这里的 Failed 不代表代码坏了）。 |
| sed / sed dash i / needs empty quotes after it / on a Mac | sed / sed -i / 空引号 | S09[7]：最后一个演示，是额外的：用 sed 加一个没用到的 import 并暂存；在 Mac 上，sed -i 后面要跟一对空引号。 | D4：sed dash i → sed -i。 |
| your machine now says no / this gate never ran a single test | 说不 | S09[7]：把文件恢复原样：你的电脑现在会说不了。 | your machine → 你的电脑（S01：在你的电脑上）。 |

### babykev：uv、just 与 walk / babykev: uv, just, the walk

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| guest lecture / Rahul Dave / babykev / machine learning project | 客座讲座 / Rahul Dave / babykev / 机器学习项目 | S10[0]：第二部分是 Rahul Dave 的客座讲座。 | A10。babykev 不放在句首（在 babykev 那边……）。 |
| uv / the package manager uv / just / the command runner just / extras | uv / just / 包管理器 / 命令运行器 | S10[0]：先装两个工具，作为额外步骤：第 2 讲的包管理器 uv，录制时是 0.13.2；还有命令运行器 just，1.59.0。 | lecture 2 → 第 2 讲，照 SAY 说。 |
| tags / step tags / step zero zero / step-00 / step five a / step five b / git switch, dash dash detach / the repo is its own slide deck | tag / step-00 / step-05a / step-05b / git switch --detach / 幻灯片 | S10[1]：这个 repo 本身就是一套幻灯片，用 git switch --detach 就能跳到任意一步。 | A10：步骤照 tag 写；课上每个阶段一步。 |
| uv sync, dash dash locked / the lockfile / locked means stop rather than silently upgrade | uv sync --locked / lock 文件 / --locked | S10[2]：在 step-00，一条命令就建好环境：uv sync --locked。 | lockfile → lock 文件（第 1 讲）。 |
| recipe / recipes / just setup / just check / just test / just fmt / just types / the setup recipe / the image recipe | recipe / just setup / just check / just test / just fmt / just types | S10[2]：单独输入 just，会列出所有 recipe：每个任务一个名字，人、hook，以及之后的 CI 都用它。 | 保留英文（A1 c）：just 自己的词；“配方”留给 Dockerfile（系列用法）。setup 这个 recipe。 |
| contract / uv run pytest / pure guess / confidence / rounded probabilities | 契约 / uv run pytest / 把握 / 四舍五入后的概率 | S10[3]：一个失败是纯粹的猜测被打成了一半的把握；另一个是 77 个四舍五入后的概率，加起来只有 0.77。 | A13。有多大把握；纯粹的猜测应该得零分。 |
| the walk / the walk's next command / as the walk records / the walk's record / walk.md | walk.md | S14[2]：剩下的看 walk.md 里的记录。 | A10：the walk 指 babykev-walk 的 walk.md；不放在句首（按 walk.md……）。 |
| venv path | venv 路径 / 写死 | S11[0]：里面写死了这台机器自己的 venv 路径，所以它永远不会被 commit。 | venv（第 1 讲）。 |
| config files are checked too / a broken hook config / one wrong indent / yamllint / validates pyproject.toml / checks the lockfile | 配置文件 / 缩进 / yamllint / pyproject.toml | S11[3]：在 pre-commit 配置里缩进错一处，yamllint 就会指出具体是哪一行。 | validates → 校验；Restored → 恢复之后。 |
| dot env file / the settings and secrets of one machine / the config's own sentence | .env 文件 / 设置 / 密钥 | S11[4]：接着暂存一个 .env 文件，拒绝的理由就是配置里自己写的那句话：.env 文件装的是一台机器的设置和密钥。 | D4：dot env file → .env file。secrets → 密钥（A7）。 |
| gate styles / format check | 门禁风格 / 格式检查 | S11[5]：两种门禁风格，都没问题：这个只指出问题，由你来跑 just fmt；cheese 的门禁直接改写，再逼你看一眼。 | format check（fmt --check）→ 格式检查（A7）。 |
| documentation / functions, methods and classes / typed and documented / one description | 文档 / 函数 / 方法 / 类型标注 / 说明 | S11[5]：接下来 step-04 和 step-04b 把文档放进门禁：一开始 88 个函数、方法和类里有 50 个带类型标注和文档，下一步是 88 个全都有；删掉一条说明就会拦下 commit。 | one description（一个 docstring）→ 一条说明。 |

### babykev：模型、mask 与属性测试 / babykev: the model, the mask, properties

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the model / the model stack / torch / for the CPU / 38 packages | 模型 / 模型依赖 / torch / CPU | S12[0]：到了 step-05，模型来了：setup 这个 recipe 现在会拉下整套模型依赖，录制时是 38 个包，包括 CPU 版的 torch 2.14.1。 | A13、C2。 |
| request / state / question / sibling question / sequence / packs one state and several questions into one sequence | 状态 / 问题 / 兄弟问题 / 序列 | S12[1]：一个请求把一段状态和几个问题打包进同一个序列。 | A13。偷看一眼，就会把一个答案泄露进另一个。 |
| mask / causal mask / the forbidden cell / branch mask / torch dot ones like / same question / segment ID | mask / causal mask / 禁止的格子 / branch mask / ones like / segment ID / 掩码（书面） | S12[1]：这一个禁止的格子，就是它和 causal mask 的全部区别。 | 保留英文（A1 c、A13）；书面写“掩码（mask）”。branch mask 和 torch 的 ones like 按 A6 写；英文行显示 branch_mask 和 torch.ones_like（D4）。 |
| token / state tokens / two questions of two / the six token picture / a four token picture | token / 状态 token | S13[1]：6 个 token 的图说一切正常；它看不出来。 | 保留英文（A13）。 |
| checker script / printout / WRONG | 检查脚本 / WRONG / 打印结果 | S12[3]：可是 just check 里没有任何东西会运行它；靠眼睛看的打印结果不是测试。 | WRONG 照画面写。 |
| type checker / declared types / ty / 6 diagnostics / types are not in the gate yet | 类型检查器 / 类型 / ty / 诊断 | S12[5]：运行 ty，发现 6 条诊断，可 just check 还是绿的：类型还没进门禁，而门禁之外的检查谁也保护不了。 | ty 小写，不放在句首。同样绿着却看不见的。 |
| half a billion parameters / Hugging Face Hub / a public model host / 6 of 15 right / nothing is trained / an untrained score | 参数 / Hugging Face Hub / 模型托管平台 | S12[6]：15 个里答对了 6 个。 | A13：5 亿参数。 |
| bit for bit equal outputs / bit exactness across machines / a stronger promise / sums in a different order / the author's Mac | 逐位相同 / 逐位一致 / 作者 | S13[0]：失败的那个测试要求输出逐位相同。 | A9、A13：诚实地、温和地说明平台差异。 |
| property test / hypothesis / draw any request shape / 4,686 shapes / asserts that no allowed pair is ever a sibling pair | 属性测试 / hypothesis / 形状 / 断言 | S13[2]：属性测试让 hypothesis 随便抽请求的形状：状态 1 到 6 个 token，最多 4 个问题，每个 1 到 5 个 token。 | A3。hypothesis 照画面小写，不放在句首；4,686 → 4686（C1）。它断言。 |
| counter example / shrinks / the smallest witness / a deliberately wrong fix / the real fix | 反例 / 收缩 / 证据 / 修复 | S13[3]：属性测试不只是说不；它还把最小的证据交到你手上。 | A3。 |
| just test dash m system / deselected | just test -m system / 1 deselected | S14[1]：明确要求时，just test -m system 显示 1 passed, 103 deselected：真实模型确实跑了，而且它必须通过，不能跳过。 | D4；悄悄跳过。 |
| hadolint / command not found / gigabytes / no network | hadolint / command not found / 1.15 GB / 1.84 GB | S14[2]：而且 just check 在一个没有网络的 container 里也跑绿了：hermetic 的说法，用实验证明了。 | C2：gigabytes → GB。 |

### CI 与收尾 / CI and the end

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| CI / CI re-runs the same checks / part 5 of this same repo / lecture 21 / a server nobody can skip | CI / Part 5 / 第 21 讲 / 持续集成（书面） | S14[4]：所以 CI 在一台谁也绕不过的服务器上，把同样的检查再跑一遍：就是同一个 repo 的 Part 5，第 21 讲。 | 保留英文（A1 c）；文档里第一次写“持续集成（CI）”。part 5 of this repo 是 README 的 Part 5（A7）。 |
| git commit, dash dash no verify / walks straight past it / the limit | git commit --no-verify / --no-verify / 绕过 | S14[3]：一个 hook 只在一台机器上运行，而 git commit --no-verify 能直接绕过它。 | D4。 |
| One command for everyone / your milestone / milestone 5 asks at least 70 | milestone | S14[4]：覆盖率下限一句话说完：babykev 选了 90；milestone 5 要求至少 70。 | A10：课程项目的 milestone，保留英文。 |
| Docker cleanup / docker container ls / docker system prune / type y / build cache / docker image ls | 清理 / docker container ls / docker system prune / docker image ls / 构建缓存 | S15[0]：然后是 docker system prune；输入 y：录制时清掉了大约 95 MB 的构建缓存。 | C2。所以不用停。 |
| Five questions to test yourself / One: … Five: / The answers are in the exercises / Next lecture | 五道自测题 / 第一题 / 第五题 / 答案在练习里 / 下节课 | S15[1]：第二题：系统测试在完全没有服务器的情况下也通过了。 | D6，同第 2–5 讲。 |

### 产品、版本、标题与书面语体 / Products, versions, titles, written register

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| products: Docker / Docker Desktop / Git / GitHub / Python / FastAPI / Homebrew / Linux / Mac / CPU / JSON / HTML / URL / Hugging Face Hub | Docker / Docker Desktop / Git / GitHub / Python / FastAPI / Homebrew / Linux / Mac / CPU / JSON / HTML / URL / Hugging Face Hub |  | A1 b。 |
| versions: 3.9 / 3.13.16 / 26.10.1 / 7.4.1 / 4.7.0 / 0.13.2 / 1.59.0 / 2.14.1 / pytest 9 | Python 3.9 / Python 3.13.16 / 26.10.1 / 7.4.1 / 4.7.0 / 0.13.2 / 1.59.0 / torch 2.14.1 / pytest 9 |  | C2；at the time of recording → 录制时（A9）。 |
| Video title | AC215 · 第 9 讲：CI 与单元测试——pytest、pre-commit，提交前的质量门（跟练：cheese-app-ci-cd + babykev） |  | H1；和 video.yaml 的 publish.title_zh 一致。跟练 = follow-along。 |
| the part titles: pytest, black and flake8, and the pre-commit gate / one command, green-but-wrong, and property tests | AC215 · 第 9 讲（上）：pytest、black 与 flake8，以及 pre-commit 门禁 / AC215 · 第 9 讲（下）：一条命令的门禁、全绿却是错的，以及属性测试 |  | H1。 |
| Chapters S01-S09: Who gets to say no? / The bug that almost shipped / Three kinds of test, and a gate / Clone, and run the app / Formatter vs linter / pytest, under the hood / Tests inside the shipping image / The system test and the silent skip / The gate on your machine | 谁有权说不？ / 差点上线的 bug / 三类测试与一道门禁（hermetic） / 克隆仓库，运行应用 / 格式化工具与代码检查工具（linter） / pytest 的内部机制 / 在要交付的镜像里跑测试 / 系统测试与悄悄的跳过 / 你电脑上的门禁 |  | H1，书面语体；核心概念那一章带上 hermetic，方便搜索。 |
| Chapters S10-S15: Guest lecture: uv, just, and two failing tests / One command is the gate / All green, and the mask is wrong / Properties, not examples / Hooks are local; CI checks again / Tear down, recap, and what's next | 客座讲座：uv、just 和两个失败的测试 / 一条命令就是门禁 / 全绿，可掩码（mask）是错的 / 属性，而不是例子 / 钩子只在本地；CI 再查一遍 / 收尾、回顾和下节预告 |  | H1；S15 沿用第 1–4 讲同一个英文标题的中文。 |
| written register for the companions: container / image / repo / clone / commit / hook / linter / formatter / hermetic / coverage / lockfile / mask / CI / gate | 容器 / 镜像 / 仓库 / 克隆 / 提交 / 钩子 / 代码检查工具 / 格式化工具 / 封闭测试 / 覆盖率 / 锁文件 / 掩码 / 持续集成 / 质量门 |  | H3、A4。只用于配套文档（README.md、exercises.md、digest.md），不用于字幕。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上表“字幕”和“首次出现”两栏里的拉丁词，检查器还允许下面这些（按它的切词方式列出，见 D3）：

build、CACHED、cd、confidence、euclidean、GET、pin、service.py

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只保留在三类地方。（a）**实物**，逐字照抄：命令和子命令（git clone、cd、ls -la、sh docker-shell.sh、uvicorn api.service:app、curl、exit、docker ps、docker ps -a、docker build、docker run --rm、docker container ls、docker system prune、docker image ls、pip install black flake8、pip install pre-commit、pre-commit install、pre-commit run、pre-commit run --all-files、pre-commit uninstall、git commit、git commit --no-verify、git log、git diff、git add -u、git status、git switch --detach、sed -i、uv sync --locked、uv run pytest、uv run ty check、ty、just、just setup、just check、just test、just test -m system、just fmt、just types、just smoke local、yamllint、hadolint），参数（--rm、--reload、--max-line-length、--check、--diff、-ra、--network host、--all-files、--locked、--detach、-m system、--no-verify、-u、-i），文件名和目录名（cheese-app-ci-cd、docker-shell.sh、pytest.ini、utils.py、service.py、pyproject.toml、.git、.env、walk.md、tests、tests/unit/、tests/system/、api、src），image、container 和工具名（cheese-app-api:local、api-server、pytest、black、flake8、ruff、ty、uv、just、pre-commit、hypothesis、yamllint、hadolint、pipx、curl、sed、torch、uvicorn），按旁白说法写的代码名（power、pytest.raises、pytest.approx、assert、def broken、assert False、TypeError、branch mask、ones like、segment ID、distance、client），错误代码和终端原文（F401、CACHED、各种 passed / failed / skipped / deselected 计数、SKIPPED、API not running at localhost:9000、Skipped、Failed、files were modified by this hook、nothing to commit、WRONG、command not found、Application startup complete、externally-managed-environment），配置里的词（line-length、DEV、health），babykev 的 step 标签（A10），进度条上 README 的 Part 和 Option 名称（A7），以及旁白提到的画面标签（your turn、extra；A11）。例外是检查器不收的实物（A6）。（b）**产品、组织、课程和名字**：Docker、Docker Desktop、Git、GitHub、Python、FastAPI、Homebrew、Linux、Mac、CPU、JSON、HTML、URL、GET、Hugging Face Hub、AC215、cheese、babykev、Rahul Dave、app、root。（c）**实验课口语，封闭清单**：第 1–5 讲的 venv、root、repo、clone、commit、pin、container、image、Dockerfile、tag、port、localhost、API、ID、bug；这一讲新增 hook（装 hook、hook 文件）、linter 和 lint（跑 lint）、hermetic、fixture、parametrize、marker、assert、recipe（just 的 recipe）、mask 和 causal mask、token、milestone（课程项目的 milestone）、CI。一个词只有在实验课真的说英文、而中文生硬、有歧义或和别的词撞车时才进这个清单（“钩子”像教科书；“代码检查工具”太长，还包括类型检查器；“封闭 / 密封测试”不是公认的术语；“夹具”“参数化”是没人念出口的教科书词；“标记”和托盘、mask 的格子撞车；“配方”是系列里 Dockerfile 的词；“掩码”书面上没问题，但 ML 实验课都说 mask）。绝不为了“味道”说英文：test、unit test、system test、smoke、coverage、gate、formatter、format、collect、skip、stage、history、lockfile、type checker、property test、counter example、shrink、server、endpoint、handler、layer、cache、build 都说中文。
- **[A2]** Docker，同第 2–5 讲。字幕说 container 和 image（起一个 container、构建 image、image 里、打包进 image），量词“个”；标题、章节名、meta.yaml 和配套文档写“容器”“镜像”（A4）。build → 构建，rebuild → 重新构建，Build again → 再构建一次；cached / all cached → 全是缓存（终端的 CACHED 照写）；layer → 层（一个很厚的层；四行薄薄的 COPY）；bake into the image → 打包进 image（同第 4 讲）；mount → 挂载（你的文件没有挂载进这个 container）；the entrypoint → entrypoint（docker-entrypoint.sh，照画面；这个 entrypoint）；exit code → 退出码；detached → 在后台；host → 宿主机（同第 2 讲：在宿主机上）。
- **[A3]** 测试的词（这一讲新增）。test → 测试（测试文件、测试目录、测试集 = suite）；unit test → 单元测试；integration test → 集成测试；system test → 系统测试；smoke test / the smoke → 冒烟测试；acceptance test → 验收测试；testing pyramid → 测试金字塔；kind of test → 哪一类测试 / 类型；hermetic 照说（一个测试是 hermetic 的；不 hermetic 的测试；hermetic 的说法），书面写“封闭测试（hermetic）”；border → 边界（这条边界；在边界图上）；executable specification → 可执行的规格说明；trays → 托盘（正常、边缘、非法；edges → 边缘情况）；collect → 收集，collector → 收集器；discovery by convention → 按约定发现测试；the -ra summary → -ra 的摘要；skip → 跳过（终端的 SKIPPED / Skipped 照写）；deselect → 排除（终端的 deselected 照写）；select on purpose → 特意选中；assert 照说，assert 会被改写；tolerance → 容差；fixture 和 parametrize 照说；marker 照说（labels for selecting tests → 用来挑选测试的记号）；test client → 测试客户端；module global → 模块级的全局变量；in process → 在同一个进程里；property test → 属性测试；hypothesis（工具名，照画面小写）照写；draw any shape → 随便抽形状；counter example → 反例；shrink → 收缩；the smallest witness → 最小的证据；coverage → 覆盖率（指标、那次运行和报告：跑覆盖率、覆盖率 94%），coverage floor / the floor → 覆盖率下限 / 下限；necessary, never sufficient → 必要，但永远不充分。
- **[A4]** 书面和口语的对应。字幕说 repo / clone / commit / container / image / hook / linter / hermetic / mask；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 钩子（hook）/ 代码检查工具（linter）/ 封闭测试（hermetic）/ 掩码（mask）。门禁在字幕和文档里都叫“门禁”；Bilibili 标题和 meta.yaml 的标题写“提交前的质量门”（video.yaml 的 publish.title_zh），所以“质量门”是标题用词，“门禁”是日常用词。引用 README 自己的说法时（clone or download from your repository）写“从你的仓库 clone 或下载”。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符不变）；不翻译、不变形、不加引号，不放进《》或代码格式。需要时加一个中文中心词：pytest.ini 这个配置文件、utils.py 里、api 目录、tests 目录、.git 里、.env 文件、hook 文件、setup 这个 recipe、detect-private-key 这个 hook、--reload 参数、just test 这条命令。小写的实物或保留英文的词（pytest、black、flake8、hypothesis、babykev、just check、walk.md、step-05a、hermetic、mask、git、cheese、utils.py、--reload、entrypoint、commit、clone）绝不放在句首：前面加一个中文词（这时 pytest……；文件已经被 black 改写过了；按 walk.md……；到了 step-05a……；所谓 hermetic……；有一个 mask……；参数 --reload……；这个 entrypoint……；先 clone……；前面 cheese 的 repo……；在 babykev 那边……）。大写的名字、产品或代码词可以开头（Part 2、Option B、README、Git、Docker、CI、Dockerfile），英文句子以终端计数开头时中文也可以（1 passed, 4 skipped……；5 passed……；8 failed, 95 passed……）。SAY 把画面上的完整命令说短了的地方，照画面写（docker-shell again → docker-shell.sh）。
- **[A6]** 检查器不收的实物。没有 say: 时，检查器把显示行当朗读文本来查，不接受“字母_字母”、= < > + 和任何括号。所以这些实物不抄进中文行，而是按旁白的说法写，英文行用 en_display 显示原样（D4）。对照：(3, 4) → x 是 3，y 是 4；GET /euclidean_distance/?x=3&y=4 → GET euclidean distance，x 是 3，y 是 4；power(3, 2) → power，参数是 3 和 2；--max-line-length=120 → --max-line-length 设成 120；test_*.py → 文件名以 test 下划线开头；Test* → 类名以 Test 开头；test_* → 函数名以 test 下划线开头 / test 下划线加星号；test_broken → test 下划线 broken；def broken(): assert False → def broken，内容是 assert False；DEV=1 → DEV 设成 1；Ctrl+C → Ctrl-C（两行都这样写）；line-length = 100 → line-length 设成 100；torch.ones_like → torch 的 ones like；branch_mask → branch mask。等工具链允许显示行保留这些字符（I1），就可以换回原样。
- **[A7]** 要分清的词。Part 2 / Part 3 / Part 4 / Part 5 和 Option B / Option 2 / Option 3（cheese README 的部分和选项，照进度条写）↔ 第一部分 / 第二部分（视频自己的两部分）↔ step-00 … step-05b（babykev 的 tag）↔ 第 k 步（不用：进度条的 step k of N 在画面上是英文）。门禁（gate）↔ 闸机（turnstile 那张图）↔ 第 4 讲的关卡（三道权限关，另一张图）。边界（hermetic 的边界）↔ 边缘（边缘输入）。问题（flake8 / ruff 报出的 finding；babykev 的问题；思考题：看上下文就清楚，门禁表的一行叫“一行”）↔ 报错（错误信息）↔ bug。格式化工具（formatter）↔ linter ↔ 类型检查器（type checker）。格式化（format）↔ 格式检查（format check，fmt --check）↔ lint。暂存（stage，git add）↔ 提交 / commit。跳过（skip）↔ 排除（deselect）↔ 失败（fail）。覆盖率 ↔ 下限。状态（babykev 的状态 token）↔ 问题 ↔ 兄弟问题。一类测试（测试的类型）↔ 类（Python 的 class：类名以 Test 开头；整个类）。测试集（suite）↔ 测试目录。依赖 ↔ 依赖组（groups）↔ 包（38 个包）。配置（config）↔ 设置（setting；.env 文件里的设置）。凭据（credentials，S01、S15）↔ 密钥（.env 文件里的 secrets；private keys 是“私钥”）。
- **[A8]** 语体：带实验课的助教。短指令，口语动词（装、跑、删、敲、改、拦、挂、卸掉）；称观众为“你”（一对一跟练；绝不用“您”“大家”“同学们”）；“我们”指录制时的我们。中文语序；句子内部可以自由调整，但保持英文的分句顺序（字幕带按分句一对一配对）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”“也正因为这样……”），少用“被”，不要一串“一个……的”。不用网络流行语。口语的节奏按意思传达：Time to type → 该动手敲了；Watch the trap → 看好这个陷阱；Now watch it bite → 现在看它咬人；Proof the gate grew teeth → 证明门禁长了牙；Now the lesson → 现在说正题；Now the limit → 再说局限；First, honesty → 先说实话；State the rule once instead → 换个办法：把规则写一次；cuts both ways → 是一把双刃剑；a floor is a gate, not a goal → 下限是门禁，不是目标；Rebuild, or you test the past → 要么重新构建，要么你测的就是过去。
- **[A9]** 准确。限定词照译：only 只，every 每个，all 全部，about / roughly 大约，under a second 不到一秒，up to 最多，at least 至少，by default 默认，on purpose 有意 / 故意，for now 暂时，never 从不 / 永远不。at the time of recording 每次都译“录制时”，绝不省略（大约一分钟；26.10.1 和 7.4.1；pytest 9 的 1 warning；4.7.0；0.13.2 和 1.59.0；38 个包和 torch 2.14.1；大约 95 MB；那几条无害的警告）。计数、版本、宽度、百分比和大小与画面完全一致。勘误要温和，后面紧跟改法，同第 5 讲统一说法：a small gap / slip → 一个小疏漏（README 说返回 5.0）；the README runs the tests immediately → README 接着马上就跑测试；does not quite manage that → 还没完全做到。S13 的平台说明照英文的语气温和地说（这台 Linux 的 CPU 上 1 failed, 102 passed，作者的 Mac 上 103 个全部通过；绝不说成 babykev 的 bug 或观众的错）。思考题（S06、S08、S09、S12、S13）只问不答，措辞不能泄露答案（S08 不能说“跳过”；S09 不能说 black 已经改好了文件；S12 不能说“不能”）。
- **[A10]** 名字。产品、公司和课程名保留拉丁字母（A1 b）；SAY 说 Harvard 时（S01）译“哈佛”，标题和简介里也写“哈佛”。课程：AC215；lecture n → 第 n 讲（第 2 讲、第 3 讲、第 21 讲）；next lecture → 下节课；the lecture → 课上；the guest lecture → 客座讲座，by Rahul Dave → Rahul Dave 的客座讲座（只在旁白里说一次）；the instructor → 授课老师（a Harvard instructor → 哈佛的一位授课老师）；the author → 作者。babykev 的步骤照画面上的 tag 写：step zero zero → step-00，Step 1 / 2 / 3 / 5 → step-01 / step-02 / step-03 / step-05，Steps 4 and 4 b → step-04 和 step-04b，Step five a / five b → step-05a / step-05b；tag 不放在句首（到了 step-05a……；接着 step-02：……）。the walk（babykev-walk 的 walk.md）→ walk.md；as the walk records → walk.md 里有记录。milestone 照说（milestone 5；你做 milestone 时）。用户 app、服务器名 api-server、image 名 cheese-app-api:local 和各个 repo 名照写。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（包括注释）、README 卡片、六个进度条（README › Part 1: Understanding the Codebase，step k of N）、课件标签（Lecture 9 · slides a–b）、标签（your turn、extra、illustration、recorded）、门禁表、掩码网格和思考题卡片都是英文，场景不需要为语言做任何改动。所以旁白提到画面标签时，字幕照画面写：黄色的 your turn 标签、灰色的 extra 标签。旁白用自己的话说的照常翻译：an extra → 额外检查 / 额外步骤 / 作为额外的一次运行，the tracker → 进度条，the gate table → 门禁表，the turnstile → 闸机，four gray dots → 四个灰点，the headline → 标题行。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、目录、服务器、网络、脚本、视频、用户、信息、配置、凭据、进程、字段、对象、函数、类、模块、变量、文档；绝不用 預設、程式、程式碼、檔案、資料夾、伺服器、網路、腳本、影片、使用者、訊息、組態、憑證、行程、物件、函式、模組、變數，也不用台湾意义上的“文件”指文档。
- **[A13]** 模型的词（babykev，S12–S13）。mask 照说（一个 mask；错的 mask；书面写“掩码（mask）”）；causal mask 照说；token 照说（两个状态 token；6 个 token 的图）；state → 状态；question → 问题；sibling question → 兄弟问题（a sibling pair → 兄弟问题的一对）；sequence → 序列；packs … into one sequence → 打包进同一个序列；the forbidden cell → 禁止的格子；rows 5 and 6 → 第 5 行和第 6 行；segment ID 照说；bit for bit equal → 逐位相同，bit exactness across machines → 跨机器逐位一致；sums in a different order → 求和的顺序不一样；half a billion parameters → 5 亿参数；nothing is trained → 什么都没训练；an untrained score → 没训练过的模型的分数；how confident it is → 有多大把握；scored as half confident → 被打成了一半的把握；rounded probabilities → 四舍五入后的概率；the model stack → 整套模型依赖；a public model host → 公开的模型托管平台。

### B. 排版

- **[B1]** 空格。中文和拉丁字母、数字或实物之间加一个半角空格（输入 git commit、Python 3.9、port 9000、11 passed、94%、26 个测试、第 5 行、.git 里、hook 文件、1 GB）。检查器会报出每个漏掉的空格。实物内部的空格保持原样（pre-commit run --all-files），绝不在实物内部加空格。全角标点旁边不加空格（……pre-commit uninstall。、是 hermetic，）。百分号前不加空格：0%、49.4%、90%、94%、100%。绝不用 U+00A0 / U+202F 冒充不换行空格。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，紧挨实物时也一样（输入 exit。）。列举用顿号（测试、格式化工具、linter）。终端原文保留它自己的半角逗号（10 passed, 1 warning；1 passed, 4 skipped），照打印抄。任何括号都不用：（）、()、《》、【】、[]、<> 都不行（没有 say: 时检查器不收，双语字幕带也不需要括注）。“”只用于中文里引用的想法或词；实物和标签名不加引号。一个中文句子里不出现第二个 。？！（一个英文句子对一个中文句子）：用 ，；： 代替（两个问题合成一个问句：这时 pytest 实际打印了什么，这四个测试又是不是 hermetic 的？）。问句保留 ？。
- **[B3]** 检查器不收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈、== != +=、数字后面跟 !、括号、字母_字母）：绝不抄进中文行；按旁白的说法写（A6）。可以照画面保留的：路径里的 /（tests/unit/、tests/system/），文件名和代码名里的 .（pytest.ini、pytest.raises、api.service），image 名或地址里的 :（cheese-app-api:local、api.service:app、localhost:9000），参数和名字里的 -（--all-files、-ra、step-05a、Ctrl-C）；* 避免（test 下划线加星号）；数字后的 %（94%）。

### C. 数字、版本号与单位

- **[C1]** 显示文本里的数字。凡是呼应画面、终端、代码或课件的，用阿拉伯数字：计数（10 个这样的测试、26 个测试、11 passed、22 个测试、这 4 个、70 个问题、32 个、37 个、38 个包、6 条诊断、9 个测试、50 个、88 个、15 个奶酪问题、15 个里答对了 6 个、4686 种形状（不加千位分隔符）、1 到 6 个 token、最多 4 个问题），宽度（88、120、79、95 个字符、100），port、版本、大小、百分比、日期（2025 年 11 月），step 标签，README 的 Part / Option 编号，行号（第 5 行和第 6 行），进度条的段数（英文说 6 sections → 6 段 / 4 段 / 1 段）。画面上没有显示成数字的小的叙述性数量用汉字：一行代码、两个嫌疑人、三个托盘、三条路、四列、九个 hook、七个卫生检查、六个 hook 通过、两个没东西可查、四个 hook、三次 curl、两个额外步骤、两种门禁风格、两个工具、一处不同、两行、六行、五道自测题、第一题……第五题、第一部分 / 第二部分。英文用单词说、画面显示成数字的，跟画面（Ten of those → 10 个这样的测试；画面上 4 skipped 的四个测试 → 这 4 个）。
- **[C2]** 单位、版本和日期。大小照画面写，加半角空格和英文单位：95 MB、1 GB、1.15 GB、1.84 GB（megabytes / gigabytes 从不写全）。版本连着名字写：Python 3.9、Python 3.13.16、pytest 9、black 26.10.1、flake8 7.4.1（说成“分别是 26.10.1 和 7.4.1”）、pre-commit 4.7.0、uv 0.13.2、just 1.59.0、torch 2.14.1。百分比用数字加 %：0%、49.4%、90%、94%、100%；0 percent → 0%。范围：Python 3.9 及以上（or newer）。时长：30 秒、不到一秒、大约一分钟。日期：from November 2025 → 2025 年 11 月的。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 逐句对齐（explainer/i18n.py）。script.md 的每一行 SAY 在 narration/*.yaml 里对应一个条目（92 段）；`en` 和 SAY 行逐字节相同；`zh` 按 explainer.voice.split_sentences 切出的英文句子，一句对一项（这个脚本共 335 句）。只在句子内部调整，绝不合并或拆分。短句也单独占一项：No. → 不会。（S06、S09）/ 不能。（S12）；Why does it skip? → 为什么会跳过？；Now the lesson. → 现在说正题。；Now the limit. → 再说局限。；Hold that thought. → 先记住这一点。；It is never committed. → 它永远不能 commit。；Two rows join the table. → 表里又多了两行。；6 of 15 right. → 15 个里答对了 6 个。。反复运行 python -m explainer.i18n check videos/ac215-l09-ci-testing --lang zh，直到它输出 OK。
- **[D2]** 没有 say:，没有锚点。没有中文配音：绝不写 say:（显示行就是唯一的文本），也绝不写 anchors:（它们只为中文配音版安排动画节拍）。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能通过检查器的显示行。没有 say: 时，每个显示的句子都要通过 explainer.i18n.spoken_problems：没有括号（B2）、没有数学符号（B3）、没有“字母_字母”（A6）、数字后面没有 !、没有以“种”结尾再跟 ，。！？ 的分句、汉字和拉丁字母或数字之间有半角空格（B1）、每句以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），而且每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用正则 [A-Za-z][A-Za-z'.-]* 切词：flake8 切成 flake，step-05a 切成 step- 和 a，ls -la 切成 ls 和 la，-ra 切成 ra，.env 切成 env，--no-verify 切成 no-verify，cheese-app-api:local 切成 cheese-app-api 和 local。它报出的拉丁词，要么是该翻译的英文词（通常如此），要么是漏收的实物：按同样的切法把实物加进 allowed_spoken_latin，并加进对应的术语。
- **[D4]** 英文行（en_display）。双语字幕带的英文行显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都加一个 en_display 项，写出画面上的字面形式，其余部分和 SAY 逐字相同；同一段里的其他句子写 null。对照（SAY → en_display）：the point 3 comma 4 / the distance of 3 comma 4 → (3, 4)；pytest dot raises / pytest dot approx → pytest.raises / pytest.approx；raises a type error → raises a TypeError；get euclidean distance, with x 3 and y 4 → GET /euclidean_distance/?x=3&y=4；power of 3 and 2 → power(3, 2)；ls dash l a → ls -la；uvicorn api dot service colon app, host 0.0.0.0, port 9000, with reload → uvicorn api.service:app --host 0.0.0.0 --port 9000 --reload；application startup complete → Application startup complete；control C → Ctrl-C；dash dash rm → --rm；docker ps dash a → docker ps -a；The reload flag → The --reload flag；cheese-app-api tagged local → cheese-app-api:local；flake8, max line length 120, on the api folder → flake8 --max-line-length=120 api/；in check and diff mode → in --check --diff mode；externally managed environment → externally-managed-environment；files named test underscore something, classes named Test, functions named test underscore → files named test_*.py, classes named Test*, functions named test_*；dash r a → -ra；def broken, assert False → def broken(): assert False；test underscore star → test_*；test underscore broken → test_broken；pytest tests slash unit → pytest tests/unit/；with DEV equals 1 → with DEV=1；docker run with network host, pytest tests slash system → docker run --network host, pytest tests/system/；skipped, API not running at localhost 9000 → SKIPPED, API not running at localhost:9000；dot git → .git；pre-commit run, dash dash all dash files → pre-commit run --all-files；git add dash u → git add -u；sed dash i → sed -i；git switch, dash dash detach → git switch --detach；step zero zero → step-00；uv sync, dash dash locked → uv sync --locked；line length 100 → line-length = 100；dot env file → .env file；Steps 4 and 4 b → Steps 4 and 4b；torch dot ones like → torch.ones_like；branch mask → branch_mask；Step five a / five b → Step 5a / Step 5b；non hermetic → non-hermetic；just test, dash m system → just test -m system；git commit, dash dash no verify → git commit --no-verify；the detect private keys hook → the detect-private-key hook；dash dash no verify → --no-verify。SAY 为了配音在念出来的命令两边加的逗号（dash a, / dash u, / dash r a,），en_display 里去掉。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只翻译它的英文句子，不多也不少：不加命令、参数、括注、中文控制台名或解释；只有英文标了 extra 的地方才写“额外”；不给保留英文的词加中文解释（英文行就在正下方）。允许的改动：SAY 把实物说短或念成单词的地方，照画面写实物（A5、A6、D4：docker-shell again → docker-shell.sh；Locked means → 加上 --locked，意思是），以及 babykev 的 step 标签（A10）。
- **[D6]** 固定句式。Pause and run it. → 暂停一下，自己跑一遍。 Pause and run both. → 暂停一下，两条都跑一遍。 Pause and run them. / Pause and run these. → 暂停一下，把它们都跑一遍。/ 暂停一下，把这些都跑一遍。 Pause and run both forms. → 暂停一下，两种写法都跑一遍。 Pause and do it. → 暂停一下，照着做。 pause and try it / pause and try the first → 暂停一下，试一试 / 暂停一下，试试第一次 pause and print yours → 暂停一下，打印你自己的 pause and walk the loop → 暂停一下，把这个循环走一遍 Pause and run the smoke. → 暂停一下，跑一下冒烟测试。 When the yellow your-turn tag appears, pause and run the command. → 看到黄色的 your turn 标签，就暂停，自己跑这条命令。 A gray extra tag marks a check not in the README. → 灰色的 extra 标签表示这个检查 README 里没有。 An extra … not in the README: → 额外……，README 里没有这一步： an extra（步骤、检查、运行）→ 额外跑一下 / 额外检查 / 额外步骤 / 作为额外的一次运行 / 是额外的。 Something to ponder. / Something to ponder: → 来想一个问题。/ 来想一个问题： A quick ponder: → 快速想一下： Something to ponder before we run it. → 跑之前，先想一个问题。 Hold that thought. → 先记住这一点。 hold that number → 先记住这个数字 at the time of recording → 录制时 5 questions to test yourself. → 五道自测题。 One: … Five: → 第一题：…… 第五题： The answers are in the exercises, and every command is in the study guide. → 答案在练习里，每条命令都在学习指南里。 Every command is in the study guide, linked below. → 每条命令都在学习指南里，链接在下方。 Next lecture brings … → 下节课会用到…… Before the recap, clean up. → 回顾之前，先清理。
- **[D7]** 文件。narration/g1.yaml = S01–S09（第一部分：cheese-app-ci-cd 教程，README Part 1–4），narration/g2.yaml = S10–S15（第二部分：客座讲座的 babykev，然后是 README 的 Docker Cleanup），和 video.yaml 的 parts 一致；每个文件以注释开头（覆盖范围、用到的规则：A6 用文字描述的实物、D4 en_display、没有 say: / 锚点），并保持脚本的顺序。字符串用双引号；字面的双引号或反斜杠要按 YAML 转义。
- **[D8]** 按英文时间轴的长度。中文是边听英文边读的，字幕带在英文分段切换的地方切换（一段中文读起来快于每秒 9 个单位时，最多多给 1 秒）。每个中文句子读起来的时间要和英文听起来差不多：经验上每个英文词最多大约 2 个单位（一个汉字 1，一个拉丁字母 0.55），所以删掉多余的连接词和重复的主语，绝不删内容。长实物也算长度（uvicorn api.service:app 大约 13 个单位，externally-managed-environment 大约 17，pre-commit run --all-files 大约 15）：英文没重复的地方不要重复。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）每行 22 个单位，每条两行。分句写到最多大约 24 个单位，用 ，；： 隔开，让切分器有干净的切点；避免超过 30 个单位却没有标点的分句。
- **[G2]** 字幕条的结尾：工具链会去掉条末的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。能用中文词收尾的，就不要以实物加句号结束（……打包进一个 image 的 Dockerfile。没问题；……检查 api 目录。比 ……api。好读）。
- **[G3]** 命令不拆行。切分器把中文行里两个拉丁词之间的空格当作好切点，所以 pre-commit run --all-files 或 just test -m system 可能被拆到两行，观众就没法照抄了。整条命令放在全角冒号之后、分句末尾（想让它们照样跑一遍，就用 pre-commit run --all-files。；一条命令就建好环境：uv sync --locked。），每条字幕最多一条命令，周围少放中文。一行放不下或含 A6 字符的命令，按 SAY 的说法分段写（uvicorn api.service:app，host 是 0.0.0.0，port 是 9000，加上 --reload；docker run --rm，加上 image 名，再加 pytest tests/unit/）。在渲染出的 .zh.srt 里检查每一条带命令的字幕。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、两部分和章节的标题用书面语体（A4：容器、镜像、仓库、克隆、提交、钩子、质量门 / 门禁、掩码）；问句保留问号；保留英文的冒号结构；命令、工具和文件名照写（pytest、black、flake8、pre-commit、uv、just、just check、CI）；meta.yaml 不经过检查器，所以那里可以用括号。视频标题和 video.yaml 的 publish.title_zh 一致（CI 与单元测试：pytest、pre-commit，提交前的质量门），套用系列格式 AC215 · 第 n 讲：……（跟练：……）。核心概念那一章带上英文短名方便搜索：三类测试与一道门禁（hermetic）。和第 1–4 讲同一个英文标题的场景，用同一个中文（Tear down, recap, and what's next → 收尾、回顾和下节预告）。
- **[H2]** 简介（Bilibili / YouTube）：两三句话：这是 AC215 第 9 讲 dlops-io/cheese-app-ci-cd 和客座讲座 rahuldave/babykev 的跟练视频；观众做什么、学到什么（在镜像里跑单元 / 集成 / 系统测试、测试金字塔和 hermetic 测试、skipped 不等于 passed、black 和 flake8 与 120 的宽度、pre-commit 拦下一次提交；一个锁文件和一条命令 just check、94% 的覆盖率和一个错的 mask、hypothesis 属性测试收缩反例、给不封闭的测试加 marker、CI）；英文旁白，配中文和中英双语字幕，README 的每条命令按原样、按顺序出现，终端输出录于 2026-10-19，不产生费用。书面语体，用这份词表的术语；和 video.yaml 的 publish.description_zh 一致。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后的 exercises.md / digest.md）用这份词表、以书面语体翻译（容器、镜像、仓库、克隆、提交、钩子（hook）、代码检查工具（linter）、格式化工具、封闭测试（hermetic）、覆盖率、测试金字塔、属性测试、反例、掩码（mask）、锁文件 / lock 文件）；那里可以用括号和下划线（不经过检查器）。标题和 `<summary>答案</summary>` 要翻译。结尾放一张术语对照表：English | 这里用的说法 | 常见的其他译法（钩子、代码检查工具 / 静态检查、格式化器、夹具 = fixture、参数化 = parametrize、标记 = marker、密封测试、基于属性的测试、质量门禁、持续集成 = CI）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 不动；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直开着）没有 say: 时，explainer.i18n check 会对显示行做配音卫生检查（_SPOKEN_BAD：括号、数学符号、“字母_字母”）。对只有字幕的视频（这个系列；video.yaml 没有 languages.zh.voice，这份词表写 voice: none），这些检查保护不了任何东西，反而逼出了 A6 和 B3。提议：当词表的 voice 是 none 时，对只显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。那时 A6 就可以换回原样：test_broken、--max-line-length=120、DEV=1、torch.ones_like、branch_mask、line-length = 100。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 _cuts 把中文行里拉丁词之间的空格当作好切点，所以命令可能被拆开（G3）。提议：在中文行里，把只用空格隔开的一串拉丁词当作不可拆的整体，除非它自己就超过一行。
