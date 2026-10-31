# AC215 第 8 讲视频中文字幕词表（中英混用版）

视频：*AC215 · Lecture 8 — LLM: Finetuning (follow-along: llm-finetuning)*（`videos/ac215-l08-llm-finetuning`）
受众：上哈佛 AC215（MLOps & LLMOps）的中文研究生：做过第 1–7 讲（uv 和 lock 文件；container、bind mount 和 docker-shell.sh；第 5 讲的 RAG，用的是同一个 llm-service-account 和同一个 secrets 目录；结构化输出）；懂基础机器学习（loss、优化器、训练循环），听说过 LoRA，但从没微调过大模型。他们打开自己的 `~/AC215/llm-finetuning` 跟着做，Docker 开着，可能有 GCP 项目和密钥，另一个标签页开着课程的 Colab“Tutorial - Finetuning with QLoRA”。语体：中国 MLOps 助教带实验课。
中文版：**只有字幕，没有中文配音**。英文旁白（Kokoro `af_heart`），中文按英文的时间轴显示：`output/ac215-l08-llm-finetuning.zh-en.mp4` 画面下方烧录的双语字幕带（中文在上，英文原句在下）、`.zh.srt`、`.zh-en.srt` / `.ass`。所以没有 `say:`、没有锚点、没有读法、不管配音时长：第 1 讲里所有关于朗读的规则（F1–F6、C2–C5）都不适用，只保留显示规则。但没有 `say:` 时，`python -m explainer.i18n check` 仍会对显示行做朗读检查（括号、数学符号、带下划线的名字、词表里没有的拉丁词、缺少的半角空格）：规则 A6、B3、D3 就是为此而设。
英文原稿：`script.md` v2（SAY 行是旁白：119 段、357 句；第一部分 S01–S09 是 66 段、192 句，第二部分 S10–S16 是 53 段、165 句）；script.md 开头的 en_display 候选清单和词库说明。课件：`SLIDES.md`（第 8 讲课件的摘要，术语表“Terms the lecture uses”）。
先例：系列试点 [`videos/ac215-l01-vms-venvs/i18n/zh`](../../../ac215-l01-vms-venvs/i18n/zh/GLOSSARY.md) 定下共用的词（repo、clone、commit、pin、lock 文件、shell、笔记本、服务账号、密钥、来想一个问题）；容器三讲 [`ac215-l02-containers-1`](../../../ac215-l02-containers-1/i18n/zh/GLOSSARY.md)、[`ac215-l03-mega-pipeline`](../../../ac215-l03-mega-pipeline/i18n/zh/GLOSSARY.md)、[`ac215-l04-flexible-workflow-ports`](../../../ac215-l04-flexible-workflow-ports/i18n/zh/GLOSSARY.md)（bucket、bind mount、层、退出码，以及这份文件沿用的纯字幕规则）；[`ac215-l05-rag`](../../../ac215-l05-rag/i18n/zh/GLOSSARY.md)（RAG、检索、语言模型、权重、token、横幅、一个小疏漏）；[`ac215-l06-agents-1`](../../../ac215-l06-agents-1/i18n/zh/GLOSSARY.md)（微调、notebook、schema、temperature、区域、单元格、Colab 界面字样）；[`ac215-l07-agent-harness`](../../../ac215-l07-agent-harness/i18n/zh/GLOSSARY.md)（diff、坑、基线、课程团队，以及 A1–I3 的规则编排）。第 1–7 讲定下的词一律沿用。
机器可读版本：[`glossary.yaml`](glossary.yaml)（内容相同，两份要同步修改；`python -m explainer.i18n check` 和字幕切分都读它。两份的术语表由同一份数据生成）

## 为什么要中英混用

- 中国的 MLOps 工程师和助教带实验课时本来就中英混着说：“训练一个 adapter”“跑 2 个 epoch”“batch 大小设成 4”“loss 降到 1.35”“调一下这个 endpoint”“用 LoRA 微调”“加一点 dropout”“用 tokenizer 套聊天模板”。硬说“适配器”“轮次”“损失”“端点”，在实验课上反而像说明书。
- 这是跟练视频：观众要照着敲命令，要在英文 README、终端、代码面板和 Colab 里找东西。命令、参数、文件名、bucket 和区域的名字、报错原文、JSON 键、包名、模型名、Colab 界面字样一旦翻译，就和屏幕对不上了。所以**实物原样，讲解用中文**。
- 已经有通用中文说法、工程师也这么说的概念（微调、权重、梯度、优化器状态、激活值、梯度检查点、量化、反量化误差、分位数、秩、重参数化、困惑度、灾难性遗忘、显存）一律说中文，用中文深度学习资料里能搜到的标准译名。
- 双语字幕带把英文原句放在每行中文的正下方，所以中文行不加任何括注，也不给保留英文的词加中文解释。
- 这个系列不翻译画面：终端、代码面板、README 卡片、录下来的输出框、控制台和 Colab 示意图、标签、进度条和思考题卡片都保持英文，只翻译旁白。

## 总原则

用一位中国 MLOps 助教在实验课上带同学一步步操作时的普通话，只在这样的人真的会说英文的地方说英文，写成英文旁白下面的字幕。观众已经会说“起一个 container”“把 repo clone 下来”“写 prompt”“跑一下 notebook”“建一个 bucket”“看 diff”；这一讲再加上“训练一个 adapter”“跑 2 个 epoch”“batch 大小 4”“loss 降到 1.35”“调一个 endpoint”“用 LoRA / QLoRA”“加 dropout”“用 tokenizer 套模板”。每个选择都要过三关：实验课上真的这么说；是能搜到的中文标准译名；和系列保持一致（第 1 讲定共用词，第 2–4 讲定 container 和 bucket 的词，第 5 讲定 RAG 和模型的词，第 6 讲定“微调”、schema、temperature、“区域”，第 7 讲定 diff 和“基线”：一律沿用）。

1. **实物原样**：观众要输入、要在屏幕上对照的东西（命令、参数、文件名和目录名、路径、服务账号 / bucket / 区域的名字、角色名、报错和打印出来的文字、JSON 键、包名、模型名、数据类型名、Colab 界面字样、README 标题、输出里的开场白、画面上的标签）逐字照抄，不翻译、不变形、不加引号；检查器逼出来的例外是带下划线的名字和 = + < > | ( ) [ ] α 这些字符，按旁白的念法写（A6、B3）。
2. **实验课口语里的英文，封闭清单**：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的 container、image、base image、pull、push、port、API、ID、token、Dockerfile、bucket、bind mount；第 5 讲的 prompt、system prompt、LLM、RAG、CLI、embedding；第 6 讲的 notebook、schema、SDK、temperature；第 7 讲的 diff；**这一讲新增 endpoint、LoRA、QLoRA、PEFT、adapter、epoch、batch（只指训练的 batch）、loss、dropout、tokenizer、trainer、absmax、unscale**。
3. **其余一律用中文标准术语**：微调、全参数微调、指令微调、参数高效微调、指令数据集、数据集、人设、口吻、开场白、口头禅、教师模型、学生模型、合成数据、训练目标、问答对、风格、事实、权重、参数、可训练参数、冻结、基座模型、预训练、服务账号、密钥、角色、控制台、项目、区域、多区域、系统指令、输入、输出、上下文、检索、迭代、退出码、异常、形状、列、行、样本、验证、随机种子、预测下一个词、微调任务、客户端、托管、显存、内存、梯度、优化器、优化器状态、滑动平均、激活值、前向传播、反向传播、梯度检查点、分页、学习率、序列、量化、反量化误差、桶、区间、块、常数、分位数、双重量化、精度、范围、线性层、输出头、归一化层、聊天模板、前缀、秩、矩阵、投影矩阵、更新量、正态分布、均匀分布、正则化、困惑度、灾难性遗忘、基线、基准测试、合并、交付、清理、价格表、训练监控、运行时、单元格。
4. **视频的比喻按意思译，一个比喻一个词**：三个旋钮、桌上摊开的那本书、砖和模具、传送带和带子、显存柱、桶、细条、开关、干洗店的取衣单。
5. **书面语体**（标题、meta.yaml、配套文档）：容器、镜像、仓库、克隆、提交、存储桶、绑定挂载、提示词、系统提示词、端点（endpoint）、适配器（adapter）、轮次（epoch）、批次（batch）、损失（loss）、分词器（tokenizer）、训练器（trainer）；LoRA、QLoRA、PEFT、NF4 书面也照写。
6. **不加括注、不用括号**：双语字幕带里英文原句就在中文下方；没有 say: 时检查器也不允许括号。
7. **人设的名字绝不出现**：旁白和字幕都说“授课老师”（A10）。
8. **工具链的约束也是规则**：每个英文句子对应一个中文句子（119 段、357 句）；显示行要过检查器（D3）；SAY 把实物念成单词的句子都要写 en_display（D4）；中文保持英文的分句顺序（D9）。

大陆简体中文；口语轻松、指令清楚，像助教带实验课，但不用网络流行语。

## 关键决定

- **结论一句话，全片同一个说法**：style is learnable; facts are not guaranteed → 风格学得会；事实没有保证（S02）；it taught a voice, not facts → 教会的是口吻，不是事实（S16）。voice 在这里是说话方式 → **口吻**，绝不写“声音”（没有音频）。
- **fine-tuning → 微调**（第 6 讲已定）：全参数微调、指令微调、参数高效微调；字幕里不写 fine-tune。tuning job → 微调任务。
- **新进封闭清单的英文**（A1 c）：endpoint（系列清单里早就列着，这一讲第一次用到）、LoRA、QLoRA、PEFT、adapter、epoch、训练的 batch、loss、dropout、tokenizer、trainer、absmax、unscale。困惑度、梯度、量化、秩这些中文说法同样通行，所以说中文。
- **显存和内存分开**（A7）：GPU memory → 显存，CPU memory → 内存；这一讲不出现“记忆”。memory column → 显存柱，a memory trick → 省显存的技巧。
- **两种 bucket**（A7）：Cloud Storage 的 bucket 照说（第 3 讲，书面“存储桶”）；量化的 bucket → 桶（每个权重 16 个桶）。**两种 block**：量化时每 64 个权重一**块**；transformer 的 28 个 block → 28 **层**。
- **人设一串**：persona → 人设，openers → 开场白，catchphrases → 口头禅，teacher → 教师模型，student（模型）→ 学生模型，synthetic data → 合成数据，Q&A pair → 一组问答。开场白的词照输出写（Yello、Welcome、good question、glad you ask），整句的模型原话放进“”里翻译（A10）。
- **路线 A / 路线 B**（track A / track B）；the notebook's part A / part B 照标题写 Part A / Part B，和视频的第一部分 / 第二部分分开（A7）。
- **LoRA 的公式用文字说**（A6、B3）：W naught → W₀，alpha over r → alpha 除以 r，B times A → B 乘 A；rank → 秩（秩 8）；query / value projection → query 投影 / value 投影；19 by 2 → 19 乘 2。
- **带下划线的名字和代码表达式**（A6，同第 3–7 讲）：drop duplicates、train test split、wait for job 设为 false、prepare model for k-bit training、target modules、disable adapter、im start / im end；英文行用 en_display 还原字面形式（D4）。
- **数字**（C1）：照终端不加千位分隔符（1146880、16444、30681）；SAY 用单词说的 million / billion 换成 万 / 亿（5.96 亿、115 万、3.758 亿、100 亿、6 亿）。位数写“n 位”（4 位存储，16 位计算）。金额照画面：112.73 美元、57 美分。
- **名字**（A10）：人设用的是授课老师的名字：画面上是灰色的 ‹instructor› 标记，字幕只说“授课老师”；Hugging Face 账号、项目编号、endpoint ID、密钥从不出现。
- **勘误统一说“一个小疏漏”**（第 5–7 讲 A9），后面紧跟改法；课件的笔误说得客气（课件上写的是 18 和 69；四舍五入应该是 19 和 70）。**录制时**：at the time of recording 每次都译“录制时”。
- **按英文时间轴读，保持英文的分句顺序**（D8、D9）。

## 一览：保留英文的词和主要对照

**保留英文**（A1）：

- 实物，逐字照抄：命令（cd、ls -la /secrets、sh docker-shell.sh、bash docker-shell.sh、python cli.py --help / --generate / --prepare / --upload / --train / --chat、exit、docker ps -a、docker images、docker image rm、git status、uv sync、diff）、参数（--rm）、文件和路径（env.dev、cli.py、Dockerfile、pyproject、llm-service-account.json、instruct-dataset.csv、train.jsonl、test.jsonl、dataset-creator、gemini-finetuner、autotrain、secrets、data、/app、/secrets、/.venv）、名字（llm-service-account、cheese-dataset、global、us-central1、US）、角色名（Storage Admin、Agent Platform User、Vertex AI User）、报错和打印文字（KeyError: 'question'、source: not found、DefaultCredentialsError、Uploading file、Training job started、Tuned model info: None、succeeded）、JSON 键（contents、parts、text、user、model、assistant、question、answer）、代码名（drop duplicates、train test split、wait for job、prepare model for k-bit training、target modules、disable adapter、im start / im end、Linear4bit）、包名（transformers、bitsandbytes、trl、peft、torchao、chromadb、langchain、torch）、Colab 界面字样（File、Save a copy in Drive、Runtime、Change runtime type、Secrets、Part A、Part B）、模型名（Gemini 3.1 Flash Lite、Gemini 1.5 Flash、Qwen3 0.6B、OPT 350m）、数据类型（NF4、FP16、BF16、FP32）、开场白（Yello、Welcome、good question、glad you ask、cheese lovers、cheese monker、The、Sure, here's）、标签（your turn、scripted）。
- 产品、组织、课程和名字：AC215、Google、Google Cloud、Cloud Storage、Agent Platform、Vertex AI、Gemini、Docker、Colab、Drive、Hugging Face、Qwen、OPT、TensorBoard、Adam、Python、uv、Debian、Ubuntu、WSL、JSON、JSONL、CSV、SDK、GPU、CPU、T4、A100、README、MLOps Learning（A1 b）。
- 实验课口语，封闭清单：repo、clone、commit、pin、lock 文件、shell（第 1 讲）；container、image、base image、pull、push、port、API、ID、token、Dockerfile、bucket、bind mount（第 2–4 讲）；prompt、system prompt、LLM、RAG、CLI、embedding（第 5 讲）；notebook、schema、SDK、temperature（第 6 讲）；diff（第 7 讲）；**endpoint、LoRA、QLoRA、PEFT、adapter、epoch、batch、loss、dropout、tokenizer、trainer、absmax、unscale（这一讲新增）**。
- 系列清单里保留英文、但这一讲没说到的：pipeline、volume、venv（只作为路径 /.venv 出现）、PATH、agent（只在角色名里）、CI、port（A13）。

**主要对照**（字幕的说法；书面语体见 A4）：

| English | 中文 | English | 中文 |
|---|---|---|---|
| fine-tuning / full fine-tuning | 微调 / 全参数微调 | instruction fine-tuning / PEFT | 指令微调 / 参数高效微调（PEFT） |
| persona / the instructor's voice | 人设 / 授课老师的口吻 | openers / catchphrases | 开场白 / 口头禅 |
| teacher / student (model) | 教师模型 / 学生模型 | synthetic data / training target | 合成数据 / 训练目标 |
| Q&A pair / dataset | 一组问答 / 数据集 | style / facts | 风格 / 事实 |
| three dials / weights | 三个旋钮 / 权重 | retrieval / RAG | 检索 / RAG |
| track A / track B | 路线 A / 路线 B | the staff's saved run | 课程团队保存的运行 |
| service account / key / role | 服务账号 / 密钥 / 角色 | console / project ID | 控制台 / 项目 ID |
| bucket (Cloud Storage) | bucket | bucket (quantization) | 桶 |
| location / multi-region | 区域 / 多区域 | system instruction / system prompt | 系统指令 / system prompt |
| exit status / exception | 退出码 / 异常 | catch-all except | 全捕获的 except |
| shape / column / row | 形状 / 列 / 行 | example (training) / validation | 样本 / 验证 |
| next-word prediction | 预测下一个词 | tuning job / client | 微调任务 / 客户端 |
| endpoint / tuned model | endpoint / 微调后的模型 | cost table / training monitor | 价格表 / 训练监控 |
| GPU memory / CPU memory | 显存 / 内存 | gradients / optimizer states | 梯度 / 优化器状态 |
| activations / gradient checkpointing | 激活值 / 梯度检查点 | paging / paged optimizer | 分页 / 分页优化器 |
| forward / backward pass | 前向传播 / 反向传播 | quantization / dequantization error | 量化 / 反量化误差 |
| block (64 weights) / constant | 块 / 常数 | block (transformer) / layer | 层 |
| quantiles / levels | 分位数 / 级别 | double quantization | 双重量化 |
| 4-bit / 16-bit | 4 位 / 16 位 | precision / range | 精度 / 范围 |
| rank / update | 秩 / 更新量 | W naught / alpha over r | W₀ / alpha 除以 r |
| adapter / LoRA / QLoRA | adapter / LoRA / QLoRA | query / value projection | query 投影 / value 投影 |
| additive / selective / reparameterization | 加性 / 选择性 / 重参数化 | regularization / dropout | 正则化 / dropout |
| epoch / batch / step | epoch / batch / 步 | learning rate / loss | 学习率 / loss |
| tokenizer / trainer / chat template | tokenizer / trainer / 聊天模板 | perplexity / base model | 困惑度 / 基座模型 |
| catastrophic forgetting | 灾难性遗忘 | baseline / benchmark | 基线 / 基准测试 |
| merge / merged model | 合并 / 合并后的模型 | ship / teardown | 交付 / 清理 |
| a small slip / at the time of recording | 一个小疏漏 / 录制时 | A question to pause on | 暂停一下，想一个问题 |

## 术语表

“字幕”是中文字幕行里的写法（标题和配套文档用 A4 的书面形式）；“首次出现”给出例句（SNN[k]：场景 SNN 第 k 段 SAY 里一个英文句子对应的中文句子，k 从 0 数），每一句都能通过检查器。这个系列没有中文配音，所以没有第 1 讲的“朗读（say:）”一栏。

### 开头：学到的是口吻，不是事实 / The hook: a voice, not facts

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Why is the sky blue? / the sky / the physics / refraction / water molecules / air molecules / scatter blue light more than red | 天空 / 折射 / 水分子 / 空气分子 / 散射 | S01[2]：两个都错了：空气分子对蓝光的散射比对红光更强。 | 开头的问题照直问：天空为什么是蓝色的？（S01[0]）。一个怪折射，另一个怪水分子；the physics → 物理（再看物理；物理没有跟着变）。 |
| language model / a small language model / two versions of the same model / the original / the fine-tuned one / a textbook | 语言模型 / 原版 / 教科书 | S01[1]：原版的回答像教科书。 | 沿用第 5 讲：语言模型。the original → 原版 / 原来的模型；the fine-tuned one → 微调后的那个。 |
| fine-tune / fine-tuning / fine-tuned / tunes / full fine-tuning | 微调 / 全参数微调 | S02[1]：微调转的是第三个旋钮：它改的是权重，办法是给模型看大量的例子，每个例子是一个输入加上你想要的输出。 | 第 6 讲已定：微调，字幕里不写 fine-tune。full fine-tuning → 全参数微调（课上的 Full Parameter）。Google tunes Gemini → Google 替你微调 Gemini。notebook 标题 Tutorial - Finetuning with QLoRA 照写（A11）。 |
| instruction fine-tuning / instruction-tuned / never instruction-tuned / instruction dataset / instruction / context / output / task-specific fine-tune | 指令微调 / 指令数据集 / 指令 / 上下文 / 输出 | S02[1]：在这门课里，通常指的是指令微调：一条指令和它的回答，成对出现。 | 课件 4–6。an instruction-tuned model → 经过指令微调的模型；never instruction-tuned → 从没做过指令微调。课上的三部分：指令 / 可选的上下文 / 输出（S05[0]）。人设属于针对特定任务的微调。 |
| persona / a persona dataset / the instructor's voice / in the instructor's voice / the instructor's way | 人设 / 人设数据集 / 口吻 / 授课老师 | S01[1]：微调后的那个，开口先来一句奶酪味十足的问候，用的是授课老师的口吻，然后才解释。 | 这里的 voice 是说话的方式 → 口吻，绝不写“声音”（没有音频；第 1 讲的“授课老师的声音”是真的语音）。answered the instructor's way → 以授课老师的方式回答。人设的名字绝不出现在任何中文行或文件里（A10）。 |
| a cheesy greeting / catchphrases / openers / Yello / Welcome / good question / glad you ask / cheese lovers / your cheese monker | 口头禅 / 开场白 / Yello / Welcome / good question / glad you ask / cheese lovers / cheese monker | S05[5]：一个小疏漏：README 摘录的 prompt 列的开场白比 cli.py 的旧，但 cli.py 自己的样例还是以 Yello 和 Welcome 开头。 | A10：开场白照输出原样写，观众要对照（Yello、Welcome、good question、glad you ask、welcome welcome welcome, cheese lovers、cheese monker）；较长的模型原话放进“”里翻译（“Yello，我是授课老师，你的 cheese monker”）。cheesy 的双关 → 奶酪味十足的。 |
| style / habits / facts / Style is learnable; facts are not guaranteed / sure, here's | 风格 / 习惯 / 事实 / Sure, here's | S02[3]：这就是保存的那次运行给我们的一课：风格学得会；事实没有保证。 | 全片的结论，S02 和 S16 同一个说法：风格学得会；事实没有保证 / 教会的是口吻，不是事实。聊天模型的口头习惯 sure, here's 照模型输出写（Sure, here's）。 |
| the course staff's saved Colab run / saved run / on an A100 / recorded | 课程团队 / A100 | S01[0]：两个回答都来自课程团队保存的 Colab 运行。 | 沿用第 6、7 讲：课程团队、保存的那次运行。画面上的 recorded 标签保持英文（A11）。on the saved A100 run → 在保存的 A100 运行里。 |
| weights / 596 million weights / frozen / trained 1.15 million new ones / a file of about 4.6 megabytes | 权重 / 冻结 | S01[3]：这个模型冻结了 5.96 亿个权重，只训练了 115 万个新的。 | 沿用第 5 讲：权重；frozen → 冻结（全都冻结了）。million / billion 写成 万 / 亿（C1）。 |
| track A / track B / the README / the course Colab | 路线 / Colab | S01[4]：路线 A 走 README：由 Gemini 写一份人设数据集，再由 Google 替你微调 Gemini。 | track → 路线；路线 A / 路线 B 可以放句首。That's track A → 这就是路线 A。不写“A 线”，也不写“轨道”（第 7 讲的 rails）。 |
| one honest limit / no service account key / no GPU | 限制 / 服务账号密钥 / 报错 | S01[6]：有一个限制要说清楚：这段是 2026 年 10 月 31 日录的，没有服务账号密钥，也没有 GPU。 | C2：2026 年 10 月 31 日。要连 Google 的命令都停在缺少密钥这一步；这些真实的报错我们都保留了。 |
| the tracker / the gray tag / the lecture slides / your turn / extra / scripted / expected / recorded / illustration / no key / estimate / erratum / billed | 进度条 / 灰色标签 / 课件 / your turn / scripted | S01[5]：左上角的进度条显示当前步骤；右上角的灰色标签指向课件。 | A11：标签名照画面写；旁白自己的话说中文（进度条、灰色标签、额外的一步）。看到标签写着 your turn，就暂停，自己跑这条命令。tagged scripted → 标着 scripted。 |

### 三个旋钮：prompt、上下文、权重 / Three dials

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| three dials / prompt / context / weights | 三个旋钮 / prompt / 上下文 / 权重 | S02[0]：要改变模型说的话，有三种办法。 | V1。prompt 照说（第 5 讲）；context → 上下文；dial → 旋钮；两种都不碰模型本身。 |
| retrieval / RAG / the RAG app from lecture 5 / looked-up text / the open book on its desk / a useful mental model | 检索 / RAG | S02[4]：一个好用的理解方式：微调动的是模型默认的口吻；RAG 换的是它桌上摊开的那本书。 | 沿用第 5 讲：RAG 照说，可以放句首；retrieval → 检索。A useful mental model → 一个好用的理解方式。 |
| OPT 350m / a model that was never instruction-tuned / the continuation / hello, my cheese name is | OPT 350m / 续写 | S02[2]：这个 notebook 给 OPT 350m 的开头是：“你好，我的奶酪名字是”。 | 模型名照旁白写，两行一致：OPT 350m、Qwen3 0.6B（C2）。模型生成的原话放进“”里翻译（A10）；画面上录下来的输出框是英文。 |
| track A: you never see a weight / track B: a small adapter on a Colab GPU / it is yours to save | Colab / GPU / adapter | S02[4]：路线 B 里，你在 Colab 的 GPU 上训练一个小 adapter，存下来就是你的。 | adapter 照说（A3）。 |

### 准备：密钥放在 repo 旁边 / Setup: a key next to the repo

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| workspace / the AC215 folder / repository / clone / commit / the commit on screen / yours may be newer | 工作区 / repo / clone / commit | S03[0]：README 只给了 repo 的链接，所以 clone 它算是额外的一步。 | 沿用第 1 讲：repo、clone、commit 照说；字幕写 repo，书面写“仓库”（A4）。folder → 目录（第 3 讲，不写“文件夹”）。 |
| folder / dataset-creator / gemini-finetuner / the autotrain folder | 目录 / dataset-creator / gemini-finetuner / autotrain | S03[1]：里面有两个目录，dataset-creator 和 gemini-finetuner，各有同样的六个文件。 | 目录名照写，需要时加“目录”（A5）。 |
| cloud console / service account / llm-service-account / roles / Storage Admin / Agent Platform User / formerly Vertex AI User / keys / a JSON key | 控制台 / 服务账号 / llm-service-account / 角色 / Storage Admin / Agent Platform User / Vertex AI User / 密钥 | S03[2]：创建一个叫 llm-service-account 的服务账号，给它两个角色：Storage Admin，以及 Agent Platform User，以前叫 Vertex AI User。 | 沿用第 1、5 讲：服务账号、密钥（不写 key 或“钥匙”）、角色、控制台；角色名照控制台写（A1 a）。在 Keys 下面添加一个 JSON 密钥；接着用它。 |
| the secrets folder / next to the repository, not inside it / llm-service-account.json / hidden file extensions / dot json dot json / on purpose | secrets 目录 / llm-service-account.json / 文件扩展名 / .json.json | S03[3]：第 3 步：在 repo 旁边建一个叫 secrets 的目录，不要建在 repo 里面。 | en_display：dot json dot json → .json.json（D4）。我们的故意留空；看看这会怎样。 |
| the key / a key outside the clone / committed by accident | 密钥 / commit | S03[4]：放在 clone 外面的密钥，永远不会被不小心 commit 进去。 | key 一律是“密钥”（第 6、7 讲）。画面上的密钥图标是金色的，从不显示内容。 |
| env.dev / project ID / bucket name / lines 6 and 7 | env.dev / 项目 ID / bucket 名称 | S03[5]：额外的第 4 步，是这个文件自己的注释暗示的：在 env.dev 的第 6、7 行填上你自己的项目 ID 和 bucket 名称。 | project → 项目（第 1 讲）。从脚本运行的位置往上找两级目录。 |
| bucket / a bucket of your own / bucket names are global / cheese-dataset / the course bucket / the dataset folder in your bucket | bucket / 全局唯一 / cheese-dataset | S03[6]：每个 bucket 的名称都是全局唯一的，cheese-dataset 是课程的。 | 沿用第 3 讲：字幕里说 bucket（书面写“存储桶”，A4）。A7：Cloud Storage 的 bucket 照说；量化的 bucket 是“桶”（S11）。不放句首（A5）。 |
| the Agent Platform and Storage APIs / enabled | API / 启用 | S03[6]：README 还默认你已经启用了 Agent Platform 和 Storage 的 API，并且有一个你自己的 bucket。 | API 照说（第 2–4 讲）。在这里暂停，把四步都做完。 |

### dataset-creator 的 container / The dataset-creator container

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| sh docker-shell.sh / bash docker-shell.sh / the first build / a fast connection / a few minutes | sh docker-shell.sh / bash docker-shell.sh / 构建 | S04[0]：第 2 步：sh docker-shell.sh。 | 命令放在分句末尾、冒号后面（G3）。这里网速快，用了 45 秒；你那边可能要几分钟。 |
| image / container / builds the image / mounted / bind mount / /app / /secrets / --rm / removes the container when you exit | image / container / 挂载 / bind mount / /app / /secrets / 环境变量 / --rm | S04[1]：它读取 env.dev，构建 image，再挂载两个目录运行它：这个目录变成 /app，你的 secrets 目录变成 /secrets。 | A2（第 2–7 讲）：container、image、bind mount 照说；mount → 挂载，build → 构建，变量 → 环境变量。en_display：/app、/secrets、--rm（D4）。 |
| the banner / activated / an app prefix / harmless / /.venv / the at sign / container ID / yours will differ | 横幅 / 已激活 / 前缀 / /.venv / container ID | S04[2]：@ 符号后面那一段就是 container ID；你的会不一样。 | 沿用第 5–7 讲。对横幅宽容一点；两个都无害。en_display：/.venv。 |
| ls -la /secrets / the README's tip / inside the container / only the folder itself | ls -la /secrets | S04[3]：第 3 步是 README 的提示：在 container 里运行 ls -la /secrets。 | en_display：ls -la /secrets。 |
| python cli.py --help / generate / prepare / upload / credentials / when it first calls Google | python cli.py --help / 参数 / 凭据 | S04[4]：第 4 步：python cli.py --help。 | flag → 参数（第 7 讲）。三个参数：generate、prepare 和 upload（照旁白）。credentials → 凭据。 |
| Debian / Ubuntu / WSL / sh is dash / the source command / source: not found / the repository root / cd into the folder first | 坑 / source: not found / 根目录 | S04[5]：在 Debian、Ubuntu 或 WSL 上，sh 就是 dash，它没有 source 命令：改用 bash docker-shell.sh。 | trap → 坑（第 7 讲）。报错原文照写：source: not found（en_display 同）。先 cd 进这个目录。 |
| docker images / 1.64 gigabytes / the lockfile / 133 packages / chromadb / langchain / never imports | docker images / lock 文件 / chromadb / langchain | S04[6]：这个 lock 文件装了 133 个包，其中有 RAG 那一讲的 chromadb 和 langchain，而这份代码从来不导入它们。 | 沿用第 1 讲：lock 文件、包。docker images reports → 用 docker images 看（A5：命令不放句首）。 |

### 批量制造人设数据 / Manufacturing a persona

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| teacher / the student / the real student / synthetic data / a training target / the teacher's mistakes | 教师模型 / 学生模型 / 合成数据 / 训练目标 | S05[7]：合成数据会带上教师模型的错误，所以要检查教师模型写了什么。 | teacher → 教师模型，the student（模型）→ 学生模型（第 1 步加载真正的学生模型）。A7：学生模型 ≠ 学生（人：像学生会做的那样）。 |
| Gemini 3.1 Flash Lite / the global location / location / us-central1 / US / multi-region | Gemini 3.1 Flash Lite / global / 区域 / us-central1 / US / 多区域 | S05[1]：这里的教师模型是 Gemini 3.1 Flash Lite，在 global 区域调用。 | 沿用第 6 讲：location → 区域（不写“位置”）；global、us-central1、US 照写。模型名照旁白写，两行一致（代码里的 gemini-3.1-flash-lite 在画面上；C2）。serving location → 部署区域。 |
| system instruction / system prompt / input prompt / JSON schema / response schema / question and answer objects / temperature | 系统指令 / system prompt / prompt / JSON schema / response schema / question / answer / temperature | S05[1]：它拿到一段描述人设的系统指令，一个要 20 组问答的输入 prompt，还有一个 JSON schema，规定回答的形状：question 和 answer 两个字段。 | system instruction → 系统指令（Google 中文文档的说法）；system prompt 照说（第 5 讲，README 第 2 步的标题）。schema、temperature 照说（第 6 讲）。temperature 0.9 增加多样性。字段名 question、answer 照写。 |
| Q&A pairs / pairs / a question and an answer / 20 pairs / a hundred | 问答对 / 问题 / 回答 | S05[0]：教程去掉了上下文：每个例子就是一个问题加一个回答。 | pair → 一组问答 / 一对（20 组问答；1000 组）。指画面上的列时，question / answer 照写（question 列）。 |
| python cli.py --generate / batch / every batch / iterations / the number of iterations / a constant on line 170, not a flag | python cli.py --generate / 迭代 / 迭代次数 / 常量 | S05[4]：第 4 步：迭代次数是第 170 行的一个常量，不是参数；想要更大的数据集，就改它。 | 生成时的 batch → 一批（每一批都打印同一行）；训练时的 batch 照说（A7）。NUM_ITERATIONS 不写；旁白说的是 the number of iterations → 迭代次数。 |
| it costs cents / 2 dollars per 1,000 iterations / billed | 美元 / 美分 | S05[2]：有密钥的话，只花几美分：README 估计每 1000 次迭代 2 美元。 | C2：金额照画面，不换算成人民币。画面上的 billed 标签保持英文（A11）。 |
| the key file was not found / exit status / zero / success / Remember that zero | 密钥文件 / 退出码 | S05[2]：可退出码却是 0，也就是成功。 | 沿用第 3 讲：exit status / exit code → 退出码（不写“状态码”）。记住这个 0。命令照样以 0 退出。 |
| specifics / optimal pH levels / confidently | 具体细节 / pH | S05[6]：这个 prompt 要教师模型给出具体细节，比如最适 pH 值。 | 思考题的铺垫（S05[6]）不能泄露答案：不出现“错误”“编造”。继续之前，先想一个问题。 |

### prepare：晚一步才暴露的错误 / Prepare: a failure that surfaces late

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| python cli.py --prepare / a shape of zero by zero / 19 by 2 / a crash / KeyError: 'question' / line 243 | python cli.py --prepare / 形状 / 崩溃 / KeyError: 'question' | S06[0]：0 个错误，形状是 0 乘 0，然后崩溃：cli.py 第 243 行报 KeyError: 'question'。 | 报错原文照写（A1 a）：KeyError: 'question'（en_display 同）。shape → 形状；19 by 2 → 19 乘 2（不写 ×，B3）。 |
| a try block / except / prints it, and carries on / the catch-all / one command later / Read the lines, not the exit code | try 块 / except / 异常 | S06[2]：错误一直都在；那个全捕获的 except 只是把它推迟到了下一条命令。 | Python 关键字照写（try、except）；exception → 异常。看输出的内容，别只看退出码。A7：全捕获 ≠ 第 7 讲的“兜底”。 |
| an empty table / the question column / column / row / rows | question 列 / 列 / 行 | S06[2]：这次 prepare 没找到文件，就建了一张空表，第一次读 question 列就失败了。 | A5：prepare、generate 照旁白写，不加短横线，不放句首（这次 prepare……；在 generate 里……）。 |
| scripted / five hand-written files / in exactly the shape Gemini returns / the 1-byte CSV | 脚本模拟 / 手写 | S06[4]：为了看一次真实的运行，额外加一步：五个手写的文件，标着 scripted，形状和 Gemini 返回的完全一样。 | scripted 标签照写（A11）；旁白说的 hand-written → 手写的。一共 20 组，Gemini 会写一百组左右。 |
| drop duplicates / line 233 / repeats the first question on purpose / opens with a catchphrase | drop duplicates / 去重 | S06[5]：最后一组脚本数据故意重复了第一个问题，第 233 行的 drop duplicates 把它去掉了。 | A6：drop_duplicates → drop duplicates（en_display 还原下划线）。 |
| instruct-dataset.csv / the lecture's term, in the file name | instruct-dataset.csv | S06[6]：这些行保存成 instruct-dataset.csv：文件名里用的就是课上的术语。 | 暂停一下，自己跑一遍 generate 和 prepare。 |

### 从 CSV 到 JSONL，再上传 / Rows to JSONL, then upload

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| format / a CSV row / human and bot labels / the text column / glue it into one text | 格式 / 标记 / text 列 | S07[0]：第 241 到 247 行把它拼成一段文本，加上 human 和 bot 标记，也就是 repo 里 autotrain 目录读的那个 text 列。 | 这里的 labels → 标记（A7：“标签”是画面上的 tag）。路线 A 用不到它。 |
| Gemini tuning / contents / a user turn / a model turn / parts / text / nesting | contents / user / model / parts / text / 嵌套 | S07[1]：第 251 到 257 行构造出 Gemini 微调要的格式：一个叫 contents 的列表，里面有 user 这一轮和 model 这一轮，每一轮都带着 parts 和 text。 | JSON 键和角色值照写（contents、parts、text、user、model、assistant）。turn → 这一轮。 |
| train.jsonl / test.jsonl / JSONL / JSON lines / each example on a single line | train.jsonl / test.jsonl / JSONL / JSON lines / 样本 | S07[2]：这就是 JSONL 里的 L：JSON lines。 | example（训练用）→ 样本（17 个样本）。 |
| train test split / holds out 10 percent / a fixed seed / 17 for training, 2 for validation / validation examples / at most 256 | train test split / 随机种子 / 验证 / 验证样本 | S07[3]：然后 train test split 用固定的随机种子留出 10%：17 个样本用来训练，2 个用来验证。 | A6：train_test_split → train test split。validation → 验证；所以才有这个上限。 |
| next-word prediction / whatever the wrapping | 预测下一个词 | S07[4]：不管外面怎么包装，训练的仍然是预测下一个词，只不过现在预测的是授课老师的回答。 | S07 和 S12 同一个说法：预测下一个词。 |
| the laptop side / git status / ignored / the data folder / your commits | 笔记本 / git status / data 目录 | S07[5]：用 git status 看，data 目录是被忽略的，所以它不会进到你的 commit 里。 | 沿用第 1 讲：laptop → 笔记本（A7：不是 notebook）。bind mount 把这些文件留在了你的 clone 里。 |
| python cli.py --upload / a default credentials error / file not found / Uploading file / no output is documented | python cli.py --upload / DefaultCredentialsError / Uploading file | S07[6]：这次它失败得很明显，报的是 DefaultCredentialsError：文件找不到。 | 异常类名照打印写（DefaultCredentialsError）。要找的是每个文件一行、以 Uploading file 开头的输出。 |
| restart the container / make it first / then pause and upload | container | S07[7]：如果你刚改过 env.dev，就重启 container。 | 一个小疏漏：README 从没说要建这个 bucket（A9）。 |

### 托管的微调任务 / Hand it to Google: the tuning job

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| exit / the container removes itself / docker ps -a | exit / docker ps -a | S08[0]：输入 exit，container 会自己删掉；额外跑一个 docker ps -a，什么都没剩下。 | en_display：docker ps -a。 |
| an extra edit / lines 10 and 11 / point them at your own / no need to rebuild | 修改 / 重新构建 | S08[1]：README 漏掉了一个额外的修改：第 10、11 行还指向课程的 bucket，cheese-dataset。 | 这个目录挂载进了 container。 |
| layer / cached / uv sync / Dockerfile / pyproject / lockfile / diff / instant | 层 / 缓存 / uv sync / Dockerfile / pyproject / lock 文件 / diff | S08[2]：一下就好了：uv sync 之前的每一层都有缓存，因为两个目录共用同一个 Dockerfile、pyproject 和 lock 文件，额外跑一个 diff 就能看到。 | 沿用第 2–4 讲：layer → 层；diff 照说（第 7 讲）。pyproject 照旁白写（画面上是 pyproject.toml）。 |
| the train client / the chat client / tuning jobs / the tuned model / at its own address | 客户端 / 微调任务 / 微调后的模型 | S08[3]：负责训练的客户端在 us-central1 创建微调任务。 | tuning job → 微调任务（job → 任务：没有创建任务）。client → 客户端。 |
| tuning datasets / one epoch / an adapter of size four / Google's managed version / one call starts the job | 微调数据集 / epoch / adapter / 托管 | S08[4]：按我们的理解，这就是你在第二部分要亲手搭的那个思路的 Google 托管版本。 | epoch、adapter 照说（A3）。大小为 4 的 adapter。By our reading → 按我们的理解。 |
| python cli.py --train / the experimental warning / no job was created | python cli.py --train / 实验性警告 | S08[5]：实验性警告没有关系。 | 画面上是 ExperimentalWarning；旁白说 the experimental warning → 实验性警告。 |
| Training job started / a job name / Tuned model info: None / wait for job set to false / hands in the job and leaves / a ticket at the dry cleaner | Training job started / Tuned model info: None / wait for job / 取衣单 | S08[6]：这里 main 调用 train 时把 wait for job 设为 false，所以这条命令交了任务就走，就像在干洗店拿一张取衣单。 | 打印出来的行照写（A9）；A6：wait_for_job=False → wait for job 设为 false（en_display 还原）。干洗店的票 → 取衣单。 |
| GPU memory / Google's problem / watch the job in the console / succeeded / a tuned model and an endpoint | 显存 / succeeded / endpoint | S08[7]：训练需要的显存比笔记本多得多；在这里，那是 Google 要操心的事。 | A7：GPU memory → 显存；CPU memory → 内存；绝不写“记忆”。控制台的状态词 succeeded 照写。endpoint 照说（系列清单；书面“端点（endpoint）”，A4）。 |
| A question to pause on / One question before we move on / Now, try it yourself | 思考题 | S08[8]：暂停一下，想一个问题。 | 思考题引子（第 1 讲：来想一个问题）。问题在卡片上（英文，A11）；引子不暗示答案（A9）。 |

### 费用、endpoint 与聊天 / Cost, endpoint and chat

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the cost table / 0.008 dollars per thousand tokens / 16,444 documents / 3 epochs / 112 dollars 73 / way too much data / 88 documents / 57 cents | 价格表 / token / 文档 | S09[0]：按每千个 token 0.008 美元算，16444 个文档跑 3 个 epoch，一共 112.73 美元；表里说这数据太多了。 | C2：0.008 美元、112.73 美元、57 美分（en_display：$112.73、$0.008）。token 照说（第 4、5 讲）。 |
| Gemini 1.5 Flash / stale / the pricing page | Gemini 1.5 Flash / 价格页面 | S09[1]：这些数字就当是过时的，去看 README 链接的价格页面。 | 一个小疏漏（A9）。 |
| line 107 / the instructor's endpoint / locations / endpoints / an ID / your key can't reach | endpoint / locations / endpoints | S09[2]：第 107 行写的还是授课老师的 endpoint。 | 路径里的词照画面写：一个以 locations、US、endpoints 和一个 ID 结尾的路径。endpoint 的值绝不写出来。 |
| python cli.py --chat / how is cheese made in Greece / the serving location | python cli.py --chat / 部署区域 | S09[3]：它会打印它的问题，“希腊的奶酪是怎么做的”，用授课老师的方式回答。 | 问题放进“”里翻译（A10）；指打印行时 Using serving location 照写。 |
| the hosted demo / optional / the training monitor / loss curves / data distribution | 托管 / 训练监控 / loss 曲线 / 数据分布 | S09[5]：第 4 步：控制台的训练监控会显示你这次任务的 loss 曲线和数据分布。 | loss 照说（A3）。 |
| you never saw a single weight / the weights are in your hands | 权重 | S09[6]：第二部分，权重就在你自己手里了。 | 第一部分到这里结束；In part 2 → 第二部分，……（D6）。 |

### Colab 与显存账单 / Colab, and the 120 GB bill

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| File / Save a copy in Drive / view-only / Runtime / Change runtime type / pick a GPU / a free T4 | File / Save a copy in Drive / 只读 / Runtime / Change runtime type / T4 | S10[0]：先点 File，再点 Save a copy in Drive；原版是只读的。 | Colab 界面字样照写（第 6、7 讲）。notebook 标题照画面写。 |
| section 3 / pins / transformers / bitsandbytes / trl / torchao / peft / LoRA layers | transformers / bitsandbytes / trl / torchao / peft / LoRA 层 | S10[1]：第 3 节 pin 住 transformers、bitsandbytes 和 trl 的版本，并卸载 torchao，notebook 里说，有它在的话 peft 不肯添加 LoRA 层。 | 包名照写（A1 a）。notebook 照说（第 6 讲）；section n → 第 n 节（第 7 讲：节 = notebook 或 README 的小节；2.1 照旁白写）。 |
| Hugging Face token / Colab secrets / public / the optional upload / imports the libraries / prints the versions / mounts your Drive | Hugging Face token / Secrets / 库 / 版本 / 挂载 / 缓存 | S10[2]：第 4 节从 Colab 的 Secrets 里读取你的 Hugging Face token；两个模型都是公开的，所以它主要用于可选的上传。 | 沿用第 6 讲：Colab 的 Secrets 照写。at the time of recording → 录制时（torch 2.11、transformers 5.16）。 |
| part A / part B / cell / section / step | Part A / Part B / 单元格 | S10[2]：暂停一下，跑完 Part A。 | A7：notebook 的 Part A / Part B（标题，照写）≠ 视频的第一部分 / 第二部分。cell → 单元格（第 6 讲）。 |
| 10 billion parameters / 16-bit floats / 20 gigabytes / gradients / the Adam optimizer / two running averages / 32-bit floats / 120 in total / five GPUs with 24 gigabytes each / activations | 参数 / 浮点数 / 梯度 / Adam 优化器 / 滑动平均 / 激活值 | S10[4]：Adam 优化器还要给每个权重保留两个滑动平均，用 32 位浮点数存：80 GB。 | 课件 13–15。100 亿（C1）。n-bit → n 位（16 位浮点数）。五块 24 GB GPU 的显存。 |
| LoRA / QLoRA / adapters / optimizer states / the frozen base / the forward pass | LoRA / QLoRA / adapter / 优化器状态 / 基座 / 前向传播 / 柱子 | S10[5]：QLoRA 把基座用 4 位存储，课上算出的总量降到大约 12 GB。 | LoRA、QLoRA、adapter 照说（A3；书面“适配器（adapter）”，A4）。the base → 基座 / 基座模型。 |

### 量化 / Quantization: 16 buckets per weight

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| quantization / buckets / a range / quantizes / 16 buckets per weight | 量化 / 桶 / 区间 | S11[0]：量化就是把一个区间分成若干个桶，只记下每个数落进了哪个桶。 | A7：量化的 bucket → 桶；Cloud Storage 的 bucket 照说。课上先讲 LoRA；我们跟着 notebook 走。 |
| round / whole numbers / tens | 取整 / 整数 / 位数 | S11[1]：桶越少，需要的位数越少，丢掉的细节也越多。 | Round to tens → 取整到十位。 |
| absmax / the worked example / 127 over the largest / lands exactly on 127 / rounds to an integer | absmax / 例题 | S11[2]：课上的例题用的是 absmax。 | absmax 照说（方法名）。127 除以最大值；1.5 变成 19（B3：不用箭头）。 |
| the dequantization error / quantization always loses a little / the slide shows 18 and 69 | 反量化误差 | S11[3]：那些红色的小缺口就是反量化误差：量化总会丢一点东西。 | 课件的笔误要说得客气：课件上写的是 18 和 69；四舍五入应该是 19 和 70。 |
| one constant for a whole matrix / block / per small block of 64 weights / an absmax constant / precision | 常数 / 块 / absmax / 精度 | S11[4]：所以 bitsandbytes 给每一小块、也就是每 64 个权重，单独存一个 absmax 常数。 | A7：量化的 block → 块；transformer 的 block（28 个）→ 层。 |
| 16 levels / bell-shaped / 4-bit NormalFloat / NF4 / quantiles / a 4-bit index / one byte | 级别 / NormalFloat / NF4 / 分位数 / 索引 / 字节 | S11[5]：每个权重存成一个 4 位的索引；两个正好装进一个字节。 | 4-bit NormalFloat, NF4 → 4 位 NormalFloat，也就是 NF4。NF4、FP16、BF16、FP32 照写。 |
| double quantization / block constants | 双重量化 / 常数 | S11[6]：这些每块的常数加起来也不少，所以双重量化把它们也量化了。 | 课上跳过了它；notebook 把它打开了。 |
| stored in 4 bits, computed in 16 / matrix multiply / a 16-bit copy / BF16 / FP16 / the training chapter | 矩阵乘法 / 副本 | S11[7]：用 4 位存，用 16 位算：每次做矩阵乘法，这一层的权重都会展开成一份 16 位的副本，用完就丢。 | chapter → 章（训练那一章；接下来几章）。 |
| linear layer / Linear4bit / embeddings / the output head / tokenizes / generates / the continuation we met earlier | 线性层 / Linear4bit / embedding / 输出头 | S11[8]：Part B 的第 1 节把小的 OPT 模型打印出来：每个线性层现在都是 Linear4bit，而 embedding 和输出头保持原样。 | embedding 照说（系列清单）；Linear4bit 照打印写。 |
| misconceptions / 4-bit arithmetic / the win is memory, not speed | 误解 / 显存 | S11[9]：有两个误解要丢掉：4 位模型并不做 4 位运算，省下来的是显存，不是速度。 | memory（GPU）→ 显存（A7）。 |

### 4 位的 Qwen 与聊天模板 / Qwen in 4 bits, and its chat template

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| Qwen3 0.6B / the same 4-bit recipe / prepare model for k-bit training / freezes every weight / gradient checkpointing / a memory trick | Qwen3 0.6B / prepare model for k-bit training / 梯度检查点 | S12[0]：第 1 步用同样的 4 位配方，加载真正的学生模型 Qwen3 0.6B。 | A6：prepare_model_for_kbit_training → prepare model for k-bit training（en_display 还原）。gradient checkpointing → 梯度检查点。 |
| parameters / 375.8 million / 596 million / packed two 4-bit values to a byte / embedding weights / the norms / not quantized / the configuration | 参数 / embedding / 归一化层 / 配置 | S12[1]：第 2.1 节数参数：3.758 亿。 | C1：3.758 亿、4.4 亿、2.2 亿、1.556 亿。the norms → 归一化层。 |
| the base model / trainable parameters / zero / Everything is frozen | 基座模型 / 可训练参数 | S12[3]：在 2.3 里，基座模型续写一句话，写着写着就跑题了。 | base model → 基座模型（LLM 的说法；base image 照说英文，A2）。 |
| a 23 megabyte file / samples 1,000 pairs / a row / the brick from part 1 | 砖 / 传送带 | S12[4]：这和路线 A 的格式一模一样：第一部分的那块砖，到了这里。 | V3、V4 的比喻按意思译：brick → 砖，conveyor → 传送带，mould → 模具，ribbon → 带子。 |
| tokenizer / chat template / im start / im end / user / assistant / an empty think block / without thinking / the same prefix | tokenizer / 聊天模板 / im start / im end / user / assistant / think / 前缀 | S12[5]：空的 think 块就是 Qwen3 不思考、直接回答的方式，之后聊天也用同样的前缀。 | tokenizer 照说（A3）。标记按旁白写（im start、im end；A6、B3：不写 <\|…\|>）；en_display 还原。 |
| 900 for training, 100 for testing / the ribbon becomes integers / tokens / the loss covers every token / question and template included | 训练集 / 测试集 / 带子 / token / loss | S12[6]：然后这条带子变成整数，loss 覆盖每一个 token，连问题和模板也算在内。 | 暂停一下，把第 1 到第 3 步跑一遍（D6）。 |

### LoRA：一层薄薄的修正 / LoRA: a thin correction

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| parameter-efficient fine-tuning / PEFT / three families / additive / selective / reparameterization | 参数高效微调 / PEFT / 加性 / 选择性 / 重参数化 | S13[0]：课上把这些方法分成三大类：加性、选择性和重参数化。 | 课件 17–20。LoRA 属于重参数化。PEFT 库。 |
| matrix / 5 by 5 / column / row / rank / rank 1 / rank 2 / barely a saving | 矩阵 / 秩 | S13[1]：这就是秩为 1；秩为 2 需要 20 个。 | rank → 秩（课上的 Rank of BA；秩 8；r 照写）。n by m → n 乘 m（B3）。 |
| the query projection / the value projection / projections / a pair of strips / 2,048 by 8 and 8 by 1,024 | query 投影 / value 投影 / 投影矩阵 / 细条 | S13[2]：Qwen 的 query 投影是一个 2048 乘 1024 的矩阵：200 多万个数。 | 画面上是 q_proj / v_proj；旁白说 query / value projection → query 投影 / value 投影。C1：不加千位分隔符（24576）。 |
| decomposes the update / the frozen W naught / alpha over r / B times A / Only B and A are trained | 更新量 / 分解 / W₀ / alpha | S13[3]：新的这一层，就是冻结的 W₀，加上 alpha 除以 r，再乘以 B 乘 A。 | W naught → W₀（两行一致；en_display）；alpha over r → alpha 除以 r（B3：不写 α 或 /）。只训练 B 和 A。 |
| B starts at zero / A at random / a normal distribution / a uniform one / the pretrained one | 正态分布 / 均匀分布 / 预训练 / 分支 | S13[4]：课上从正态分布里取 A；这个库用的是均匀分布。 | 课件与库的差异，说得客气（BRIEF Conflicts 3）。 |
| the LoRA config / alpha 16 / rank 8 / scaled by 2 / a dropout of 0.1 / regularization | LoRA / alpha / dropout / 正则化 | S13[5]：接下来是 notebook 的第 4 步，LoRA 配置：alpha 16，秩 8，所以更新量缩放 2 倍，再加上 0.1 的 dropout 做正则化。 | dropout 照说（A3）。 |
| target modules / the PEFT library's default / adapts / two of the seven matrices / the 28 blocks / per block / in all | target modules / 默认设置 / 层 | S13[6]：配置里没有写 target modules。 | A6：target_modules → target modules。A7：transformer block → 层（28 层里的每一层；每层）。 |
| capacity / more memory and time / plenty / reload the model in 1.3 first | 容量 | S13[8]：秩越大，容量越大，代价是更多的显存和时间；做人设的话，两个投影矩阵上用秩 8 就够了。 | 思考题的答案在 S13[8]；提问的 S13[7]（现在，你自己试试）不透露答案。 |

### 在小 GPU 上训练 / Training on a small GPU

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| the memory column / by our own estimate / about 7 gigabytes / under 1 / 0.6 billion parameters / fits a T4 / scales | 显存柱 / 估算 / T4 | S14[0]：参数只有 6 亿的话，就算全参数微调，也放得进一块 T4。 | estimate 标签照写（A11）；按我们自己的估算。 |
| activations / on the way forward / the backward pass / gradient checkpointing / recomputes / compute traded for memory | 激活值 / 反向传播 / 梯度检查点 / 重新计算 | S14[1]：梯度检查点只保留少数几个，其余的在需要时重新计算：用计算换显存。 | 课件 57–64。backward pass → 反向传播；forward pass → 前向传播。 |
| the training arguments / sequences capped at 512 tokens / grouped by length / epochs / batches of 4 / a learning rate / a paged 32-bit Adam / paging / CPU memory | 训练参数 / 序列 / epoch / batch / 学习率 / 分页 / 内存 | S14[2]：分页会在 GPU 显存满了的时候，把优化器状态挪到 CPU 内存里。 | epoch、batch（训练）照说（A3）：2 个 epoch，batch 大小为 4。2 乘 10 的负 4 次方（B3）。我们的用不着。 |
| fp16 on and bf16 off / the range of float 32 / no fast BF16 | fp16 / bf16 / 范围 / 精度 / FP32 | S14[3]：T4 没有快速的 BF16，所以这个 notebook 用 FP16 计算。 | 参数 fp16 / bf16 照写；float 32 → FP32。 |
| the trainer / casts them back to float 32 / unscale / trainable parameters / 0.3 percent | trainer / 可训练参数 / unscale | S14[4]：而且这个数字证实了我们的算术：1146880 个可训练参数，占 0.3%。 | trainer 照说（A3；画面上是 SFTTrainer）；FP16 训练没法对它们 unscale。 |
| the gradient flows down through W naught / no gradient / no update | 梯度 | S14[5]：W₀ 在往下传的时候会用到；只是它得不到梯度，也不会被更新。 | 课件 29 的说法在画面上已更正（BRIEF Conflict 6）。 |
| train / 450 steps / 3 minutes and 36 seconds / 6 to 7 minutes on a T4 / the loss falls from 2.0 to 1.35 / TensorBoard | 训练步 / TensorBoard | S14[6]：这个 loss 从 2.0 降到了 1.35。 | 训练步 → 步（450 步）；进度条步骤 → 第 n 步。暂停一下，开始训练。 |

### 有效吗？评估 / Did it work? Perplexity and the sky

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| perplexity / the exponential / the average token loss / equally likely next tokens | 困惑度 | S15[0]：困惑度就是平均每个 token 的 loss 取指数：大致相当于模型在多少个等可能的下一个 token 里做选择。 | perplexity → 困惑度（中文标准译名；loss 照说，A3）。 |
| the base model / the fine-tuned model / 30,681 tokens / a loss of 2.65 / a perplexity of 14.15 | 基座模型 / 测试样本 | S15[1]：在 100 个测试样本、30681 个 token 上，基座模型的 loss 是 2.65，困惑度 14.15。 | C1：数字不加分隔符。 |
| disable adapter / switch the adapter off / catastrophic forgetting / losing old skills while learning new ones / one switch away | disable adapter / 灾难性遗忘 / 开关 | S15[2]：这就是课上讲的灾难性遗忘：学新本事时丢了旧本事；用 LoRA 的话，原来的模型只差一个开关。 | A6：disable_adapter() → disable adapter（en_display 还原）。课件 9–10、36。 |
| every base answer starts with the word the / welcome / Yello / an illustration / the measured numbers | The / 示意 | S15[3]：那些柱子只是示意；实测的数字就在旁边。 | 开头的词照输出写：都以 The 开头（A10）。 |
| What does the drop measure? / this style is what the model now expects | 风格 | S15[4]：它说明这种风格是模型现在预期的，而不是它的回答更正确了。 |  |
| the voice transferred, the physics did not | 口吻 | S15[5]：再看天空：口吻学过去了，物理没有。 | 暂停一下，跑第 5 步（D6）。 |
| a fresh 16-bit model / the baselines differ / a published benchmark / style fit / answer quality | 基线 / 基准测试 / 风格契合度 / 回答质量 | S15[6]：两点友情提示。 | baseline → 基线（第 7 讲）。 |

### 交付、清理与回顾 / Ship it, tear down, recap

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| saves your work / the adapters / 4.6 megabytes in float 32 / your Drive / with the tokenizer | adapter / Drive / tokenizer | S16[0]：先存 adapter：1146880 个数，用 FP32 存大约 4.6 MB，连同 tokenizer 一起存到你的 Drive。 |  |
| the merge / a fresh 16-bit copy of the base / round back onto 16 levels / the merged model / 1.2 gigabytes | 合并 / 合并后的模型 | S16[1]：合并后的模型大约 1.2 GB。 | 不是加进 4 位的权重里。 |
| push / a private Hugging Face repository / ship / an adapter that needs its base / a merged model that stands alone / Google's endpoint | push / Hugging Face / 交付 | S16[2]：所以你可以交付三样东西：一个离不开基座的 adapter，一个能独立运行的合并模型，或者 Google 的 endpoint，权重不在你手里。 | push 照说（第 2–4 讲）；私有的 Hugging Face repo。 |
| Teardown / docker image rm / delete the dataset folder / keep for lecture 10 / delete unused service account keys / disconnect and delete the Colab runtime | 清理 / docker image rm / 运行时 | S16[3]：退出 container，用 docker image rm 删掉两个 image。 | Teardown. → 清理。Pause, and tear down. → 暂停一下，把它们都清理掉。runtime → 运行时（指菜单时照写 Disconnect and delete runtime）。 |
| Here's where we are / Five questions to test yourself / the study guide / the exercises / MLOps Learning / lecture 9 / lecture 10 | 学习指南 / 练习 / MLOps Learning | S16[6]：学习指南和练习都在 MLOps Learning 里。 | 沿用第 5–7 讲。回顾一下。en_display：MLOps_Learning（D4）。 |

### 课程、名字与产品 / Course, names, products

| English | 字幕 | 首次出现 | 说明 |
|---|---|---|---|
| AC215 / the lecture / the lecture slides / the slide / the instructor / the staff / lecture n / part 1 / part 2 | AC215 / 课件 / 授课老师 / 课程团队 | S11[3]：课件上写的是 18 和 69；四舍五入应该是 19 和 70。 | A10（第 1–7 讲）。lecture n → 第 n 讲；授课老师，从不提名字；the slide → 课件。 |
| products: Google / Google Cloud / Gemini / Docker / Colab / Drive / Hugging Face / Qwen / OPT / TensorBoard / Python / uv / JSON / CSV / SDK / GPU / CPU / T4 / A100 | Google / Google Cloud / Gemini / Docker / Colab / Drive / Hugging Face / Qwen / OPT / TensorBoard / Python / uv / JSON / CSV / SDK / GPU / CPU / T4 / A100 | S10[0]：免费的 T4 就够了。 | 拉丁字母（A1 b）。GPU 的量词用“块”（五块 GPU、一块 T4）。 |
| at the time of recording / a small slip / two kind notes | 录制时 / 小疏漏 | S10[2]：第 5 节导入这些库，打印版本，录制时是 torch 2.11 和 transformers 5.16，然后挂载你的 Drive。 | A9：录制时，绝不省略；一个小疏漏，后面紧跟改法。 |

### 检查器允许的拉丁词 / allowed_spoken_latin

除了上面各词条 zh_subtitle 和 first_use 里的拉丁词，字幕行还可以出现下面这些（实物按检查器的切法切开，D3）：

absmax、AC、Adam、adapter、Admin、Agent、AI、alpha、and、answer、API、app、ask、assistant、autotrain、base、bash、batch、BF、bf、billed、bind、bit、bitsandbytes、bot、cd、Change、chat、cheese、cheese-dataset、chromadb、CLI、cli.py、clone、Cloud、Colab、commit、container、contents、copy、CPU、CSV、dash、data、dataset-creator、Debian、DefaultCredentialsError、delete、diff、disable、Disconnect、Docker、docker、docker-shell.sh、Dockerfile、Drive、drop、dropout、duplicates、embedding、end、endpoint、endpoints、env.dev、epoch、erratum、Error、estimate、exit、expected、ExperimentalWarning、extra、Face、False、false、File、file、Finetuning、Flash、float、for、found、FP、fp、free、Gemini、gemini-finetuner、genai、generate、Generating、git、glad、global、good、Google、google-genai、GPU、gs、help、here's、Hugging、human、ID、illustration、im、image、images、in、info、instruct-dataset.csv、job、JSON、JSONL、k-bit、key、KeyError、la、langchain、Learning、Linear、Lite、LLM、llm-dataset-creator、llm-finetune-dataset-small、llm-service-account、llm-service-account.json、location、locations、lock、LoRA、LoraConfig、loss、lovers、ls、MLOps、model、modules、monker、mount、NF、no、None、NormalFloat、not、notebook、OPT、Part、parts、PEFT、peft、pH、pin、Platform、prepare、Processing、proj、projects、prompt、ps、pull、push、pyproject、pyproject.toml、Python、python、QLoRA、query、question、question'、Qwen、RAG、README、recorded、repo、rm、role、Runtime、runtime、Save、schema、scripted、SDK、Secrets、secrets、serving、SFTTrainer、sh、Shape、shell、source、split、start、started、status、Storage、Succeeded、succeeded、Sure、sync、system、target、temperature、TensorBoard、test、test.jsonl、text、The、the、think、token、tokenizer、torch、torchao、train、train.csv、train.jsonl、trainer、Training、training、transformers、trl、Tuned、turn、Tutorial、type、Ubuntu、unscale、upload、Uploading、US、us-central、User、user、Using、uv、uv.lock、value、venv、Vertex、wait、Welcome、welcome、with、WSL、Yello、you、your。

## 规则

规则编号和 glossary.yaml 一致。第 1 讲的 E（屏幕文字）和 F（语音）两组，以及 C 组里关于读法的条目，在这里不适用：这个系列不翻译屏幕，也没有中文配音。

### A. 术语与中英混用

- **[A1]** 混用范围。英文只留在三类地方。（a）**实物**，逐字照抄：命令（cd、ls -la /secrets、sh docker-shell.sh、bash docker-shell.sh、python cli.py --help / --generate / --prepare / --upload / --train / --chat、exit、docker ps -a、docker images、docker image rm、git status、uv sync、diff）、参数（--rm 等）、文件名、目录名和路径（env.dev、cli.py、llm-service-account.json、instruct-dataset.csv、train.jsonl、test.jsonl、dataset-creator、gemini-finetuner、/app、/secrets、/.venv）、服务账号、bucket 和区域的名字（llm-service-account、cheese-dataset、global、us-central1、US）、角色名（Storage Admin、Agent Platform User、Vertex AI User）、报错和打印出来的文字（KeyError: 'question'、source: not found、DefaultCredentialsError、Uploading file、Training job started、Tuned model info: None、succeeded）、JSON 键和角色值（contents、parts、text、user、model、assistant、question、answer）、按旁白念法写的代码名（A6）、包名（transformers、bitsandbytes、trl、peft、torchao、chromadb、langchain、torch）、Colab 界面字样（File、Save a copy in Drive、Runtime、Change runtime type、Secrets、Part A、Part B）、模型名（Gemini 3.1 Flash Lite、Gemini 1.5 Flash、Qwen3 0.6B、OPT 350m）、数据类型名（NF4、FP16、BF16、FP32、fp16、bf16）、人设的开场白（Yello、Welcome、good question、glad you ask、cheese lovers、cheese monker、The、Sure, here's）、旁白点名的画面标签（your turn、scripted）。（b）**产品、组织、课程和名字**：AC215、Google、Google Cloud、Cloud Storage、Agent Platform、Vertex AI、Gemini、Docker、Colab、Drive、Hugging Face、Qwen、OPT、TensorBoard、Adam、Python、uv、Debian、Ubuntu、WSL、JSON、JSONL、CSV、SDK、GPU、CPU、T4、A100、README、MLOps Learning。（c）**实验课口语里的英文，封闭清单**：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的 container、image、base image、pull、push、port、API、ID、token、Dockerfile、bucket、bind mount；第 5 讲的 prompt、system prompt、LLM、RAG、CLI、embedding；第 6 讲的 notebook、schema、SDK、temperature；第 7 讲的 diff；**这一讲新增 endpoint（系列清单里的词，第一次用到）、LoRA、QLoRA、PEFT、adapter、epoch、batch（只指训练的 batch）、loss、dropout、tokenizer、trainer、absmax、unscale**。只有实验课真的说英文、中文说法生硬或撞词时，才加入（c）。其余一律中文（A3）。
- **[A2]** container 和 image（同第 2–7 讲）。字幕说 container、image、base image、bind mount：构建 image、启动 container、container ID、重启 container、删掉两个 image；量词“个”。mount → 挂载，build → 构建，layer → 层（有缓存）。标题、章节名、meta.yaml 和配套文档写 容器、镜像、基础镜像、绑定挂载（A4）。
- **[A3]** 微调的词汇（这一讲新增）。fine-tune → 微调（第 6 讲已定，字幕不写 fine-tune），full fine-tuning → 全参数微调，instruction fine-tuning → 指令微调，经过指令微调的模型，参数高效微调，PEFT 照写。persona → 人设，voice（说话方式）→ 口吻，catchphrases → 口头禅，openers → 开场白，teacher → 教师模型，student（模型）→ 学生模型，synthetic data → 合成数据，training target → 训练目标，Q&A pair → 一组问答 / 问答对，next-word prediction → 预测下一个词。显存一串：GPU memory → 显存，CPU memory → 内存，激活值、梯度、优化器状态、滑动平均、梯度检查点、分页、前向传播 / 反向传播。量化一串：量化、桶、区间、反量化误差、块、常数、分位数、级别、双重量化，n-bit → n 位（4 位存储，16 位计算），精度、范围。LoRA 一串：rank → 秩，更新量，分解，W naught → W₀，alpha over r → alpha 除以 r，B times A → B 乘 A，adapter 照说，query 投影 / value 投影，投影矩阵，transformer block → 层，加性 / 选择性 / 重参数化，dropout 照说，正则化。训练一串：epoch 照说，训练的 batch 照说（batch 大小为 4），学习率，trainer、tokenizer 照说，训练步 → 步（450 步），loss 照说。评估一串：困惑度，基座模型，微调后的模型，灾难性遗忘，基线，基准测试，风格契合度。保存一串：合并，合并后的模型，ship → 交付。路线 A 一串：tuning job → 微调任务，client → 客户端，托管，location → 区域，多区域，endpoint 照说，价格表，训练监控。视频的比喻按意思译，一个比喻一个词：三个旋钮、桌上摊开的那本书、砖、模具、传送带、带子、显存柱、柱子、桶、细条、开关、干洗店的取衣单。
- **[A4]** 字幕与书面。字幕说 repo / clone / commit / container / image / bucket / bind mount / prompt / system prompt / notebook / token / endpoint / adapter / epoch / batch / loss / tokenizer / trainer；标题、章节名、meta.yaml 和配套文档写 仓库 / 克隆 / 提交 / 容器 / 镜像 / 存储桶 / 绑定挂载 / 提示词 / 系统提示词 / Colab 笔记本（notebook）/ 词元（token）/ 端点（endpoint）/ 适配器（adapter）/ 轮次（epoch）/ 批次（batch）/ 损失（loss）/ 分词器（tokenizer）/ 训练器（trainer），核心概念第一次出现时括注英文（旁白以外可以用括号）。LoRA、QLoRA、PEFT、RAG、NF4 书面也照写。命令不受影响。
- **[A5]** 实物的写法。逐字照抄（大小写、点、斜杠、连字符都不改）；不翻译、不变形、不加引号、不加《》或代码格式。需要时加中文中心词：secrets 目录、data 目录、autotrain 目录、question 列、text 列、global 区域、Linear4bit 层。句子不以实物或小写的英文词开头，先放一个中文词（这次 prepare……；在 generate 里……；用 docker images 看……；用 git status 看……；这个 lock 文件……；这里 main……；这个 loss……；每个 bucket……；这个 notebook……；负责训练的客户端……），所以字幕也不会以小写开头。大写的名字、缩写和数据类型名（Gemini、Qwen3、OPT、Colab、README、RAG、LoRA、QLoRA、PEFT、NF4、BF16、FP16、KeyError、W₀、Part A）可以放句首。
- **[A6]** 带下划线的名字和代码表达式（同第 3–7 讲）。没有 say: 时，检查器把显示行当朗读文本，拒收 letter_letter、括号、< > | 和 =；SAY 本身也不念下划线。所以中文行按旁白的说法写：drop_duplicates → drop duplicates；train_test_split → train test split；wait_for_job=False → wait for job 设为 false；prepare_model_for_kbit_training → prepare model for k-bit training；target_modules → target modules；disable_adapter() → disable adapter；<|im_start|> / <|im_end|> → im start / im end；NUM_ITERATIONS → 迭代次数；q_proj / v_proj → query 投影 / value 投影；MLOps_Learning → MLOps Learning；W₀ 照写；alpha over r → alpha 除以 r；(19, 2) → 19 乘 2。英文行用 en_display 给出字面形式（D4）。
- **[A7]** 要分清的词。bucket（Cloud Storage）≠ 桶（量化的桶，S11）。块（量化时每 64 个权重一块）≠ 层（transformer 的 block 或任何 layer：28 层、每层、线性层、LoRA 层、image 的层）。显存（GPU）≠ 内存（CPU）≠ 记忆（这期不用）。口吻（人设的说话方式）≠ 声音（音频，不用）。学生模型 ≠ 学生（人）。教师模型 ≠ 授课老师（从不提名字）。笔记本（laptop）≠ notebook（Colab）。第一部分 / 第二部分（视频）≠ Part A / Part B（notebook 的标题，照写）≠ 第 n 节（notebook 或 README 的小节）≠ 第 n 步（进度条或 notebook 的步骤）≠ n 步（训练步：450 步）≠ 章（这期视频的章节：训练那一章）。一批（--generate 生成时的一批）≠ batch（训练的 batch）。标记（human / bot、聊天模板的标记）≠ 标签（画面上的 tag：灰色标签）。系统指令（Gemini 的 system instruction）≠ system prompt（README 的说法）≠ 提示符（shell 的提示符）。验证（验证样本）≠ 测试（测试集）≠ 检查。基座模型 ≠ base image（A2）。全捕获的 except ≠ 兜底（第 7 讲的 fallback）。参数（命令行参数；模型参数）靠上下文区分。微调任务 ≠ 其他“任务”。区域（location）≠ 位置。课件 ≠ 课上 ≠ 课程团队。
- **[A8]** 语体：助教带实验课。短指令，用口语动词（跑、装、改、贴、删、存、输入、点）；观众是“你”（不用“您”“大家”“同学们”）；“我们”是录制时的我们（我们没有密钥）。分句内部用中文语序，分句顺序跟英文走（D9）。不要翻译腔：不说“让我们……”（说“我们来……”“先……”），不说“这就是为什么……”（说“所以……”），少用“被”字句，不堆“一个……的”。不用网络流行语。口语节奏按意思传达：再看物理；先从小的说起；往回追；现在再跑一次 prepare；哪些层？；有效吗？；清理。；全都冻结了。；我们的用不着。
- **[A9]** 准确。量词照译：only 只，every 每个 / 每次，all 全部，about 大约，at most 最多，never 从不，exactly 正好 / 完全。at the time of recording 每次都译“录制时”，绝不省略。数量、行号、步骤号和版本照画面（C1）。勘误语气温和，后面紧跟改法：一个小疏漏：……；课件笔误说得客气（课件上写的是 18 和 69；四舍五入应该是 19 和 70）。打印出来的结果照打印写：KeyError: 'question'、Tuned model info: None、source: not found、Uploading file、Training job started、succeeded。思考题五道（S05[6]、S08[8]、S10[3]、S12[1]、S13[7]）：引子（继续之前，先想一个问题。／暂停一下，想一个问题。／现在，你自己试试。）不给答案，卡片下面那句也不能泄露：S05[6] 不说教师模型会出错；S08[8] 不说任务在哪里跑；S10[3] 不给出 120 GB；S12[1] 不解释 3.758 亿和 5.96 亿的差距；S13[7] 不给出两个数字。金额：2 美元、0.008 美元、112.73 美元、57 美分，不换算。
- **[A10]** 名字。产品、公司和课程保留拉丁字母（A1 b）；“哈佛”只出现在标题和简介里。课程：AC215；lecture n → 第 n 讲（第 5 讲的 RAG 应用；第 9 讲 / 第 10 讲）；the lecture → 课上；the slides / the slide → 课件；part 1 / part 2 → 第一部分 / 第二部分；this video → 这期视频；the instructor → 授课老师，从不提名字；the staff → 课程团队。人设的名字绝不出现在任何中文行或文件里：画面上是灰色的 ‹instructor› 标记，旁白说 the instructor，字幕也一样（“Yello，我是授课老师，你的 cheese monker”；用授课老师的口吻）。Hugging Face 账号、项目编号、endpoint ID、container ID 和密钥从不写出也不念出。旁白引用的模型原话：开场白的词照输出写（Yello、Welcome、The、Sure, here's、welcome welcome welcome, cheese lovers、good question、glad you ask），整句生成内容放进“”里翻译（“你好，我的奶酪名字是”；“我的奶酪名字是奶酪，我不确定你是不是在开玩笑”；“希腊的奶酪是怎么做的”），因为上面录下来的输出框里是英文原文。用户名 student 照写。
- **[A11]** 画面保持英文。这个系列只翻译旁白：终端输出和提示符、终端标题、代码面板（包括注释）、README 卡片、录下来的输出框和引用框、控制台和 Colab 的示意图、进度条（README › Dataset › Run Container、Colab › Step 4 · Fine-tune、step k of N）、课件标签（Lecture 8 · slides 43–51）、V1–V8 的标注、数据类型标签、额外卡片、各种标签（your turn、extra、illustration、recorded · the staff's saved Colab run (A100)、expected、scripted、no key、billed、estimate、at the time of recording、erratum、your id will differ、concept · lecture only、free）以及思考题和回顾卡片都是英文，场景不用为中文改动。旁白点名画面上的东西时照画面写（标签写着 your turn；标着 scripted）；旁白自己的话要译（进度条、灰色标签、额外的一步、显存柱）。
- **[A12]** 只用大陆简体中文：默认、程序、代码、文件、目录、数据、数据集、网络、脚本、视频、信息、账号、函数、参数、字段、单元格、运行时、配置、内存、显存、优化器、矩阵；不用 預設、程式、程式碼、檔案、資料夾、資料、資料集、網路、腳本、影片、帳號、函式、引數、欄位、儲存格、執行階段、組態、記憶體、最佳化器 等繁体或台湾用语。
- **[A13]** 系列清单在这一讲的情况。container 和 image 在 S04、S08、S16；Dockerfile 一次（S08[2]）；prompt（输入 prompt、system prompt、prompt 改变输入）；token（S09 的价格表、S12、S14、S15）；endpoint（S08、S09、S16）和 LoRA（S10–S16）在系列里第一次用到；embedding（S11、S12）；pipeline、volume、venv（只作为路径 /.venv）、PATH、agent（只在角色名 Agent Platform User 里）、CI、port 这一讲没有。不在系列清单里、这一讲新增保留的：QLoRA、PEFT、adapter、epoch、batch、loss、dropout、tokenizer、trainer、absmax、unscale。

### B. 排版

- **[B1]** 空格。汉字和拉丁字母、数字或实物之间加一个半角空格（输入 exit、第 243 行、133 个包、1.64 GB、112.73 美元、secrets 目录、4 位、秩 8、3.758 亿、2026 年 10 月 31 日、W₀ 从来没变）。检查器对每个显示句都查空格。实物内部的空格照原样（python cli.py --prepare、docker image rm、Gemini 3.1 Flash Lite），不往实物里加空格。全角标点旁边不加空格。不用 U+00A0 / U+202F。
- **[B2]** 标点。中文用全角 ，。、；：？！“”……，挨着实物也一样。列举用 、（transformers、bitsandbytes 和 trl；加性、选择性和重参数化）。不用任何括号：（）、()、《》、【】、[]、<>。“”只用于中文里引用的想法或译出来的原话（模型生成的整句，A10）；实物、标签名、界面字样、终端文字和开场白的词不加引号。每个中文句子（对应一个英文句子）内部没有 。？！：用 ，；：。英文有冒号时，第 N 步后面用全角冒号（第 2 步：sh docker-shell.sh。）。报错原文 KeyError: 'question'、source: not found 保留自己的半角冒号和引号（A1 a）。
- **[B3]** 检查器拒收的符号（= < > + → ← ^ ≤ ≥ × ÷ ≈ α ε σ、== != +=、数字后面的 !、括号、letter_letter、<|…|>）：绝不抄进中文行，用文字说（A6）。19 乘 2；2048 乘 1024；alpha 除以 r；B 乘 A；2 乘 10 的负 4 次方；127 除以最大值；1.5 变成 19；120、40、再到 12 GB。可以照画面保留的：路径和名字里的 . 和 /、参数和名字里的 -（--prepare、docker ps -a、us-central1、k-bit）、%（10%、0.3%）、打印文字里的半角冒号和引号、@（@ 符号）、W₀（下标不算数学符号）。

### C. 数字、版本号与单位

- **[C1]** 显示文本里的数字。凡对应屏幕、终端、代码、课件上的数字，或 SAY 里用阿拉伯数字写的数字，一律用阿拉伯数字，不加千位分隔符，和 trainer 打印的一样（1146880、2293760、5046272、2097152、24576、16384、40960、16444、30681、1000、2048、1024）：步骤和小节号（第 1 步、第 2.1 节或照旁白写 2.1、第 6、7 行、第 241 到 247 行）、讲次（第 5 讲）、数量（133 个包、20 组问答、17 个样本、900 个、100 个测试样本、28 层、450 步、2 个 epoch）、大小、时间、金额、日期、版本。SAY 用单词说的百万、十亿换成 万 / 亿 加数字：5.96 亿、115 万、3.758 亿、4.4 亿、2.2 亿、1.556 亿、100 亿、6 亿、200 多万。SAY 用单词写的小数目用汉字：两个回答、三个旋钮、两条路线、六个文件、两个角色、四步、五个文件、两个坑、三个参数、三大类、七个矩阵、五道题、三样东西、两点友情提示、一百组左右、第三个旋钮。
- **[C2]** 单位、版本、模型名、金额和日期。大小照画面加半角空格：4.6 MB、23 MB、1.64 GB、1.2 GB、20 GB、120 GB、24 GB。时间：45 秒、大约三分半钟、3 分 36 秒、6 到 7 分钟。位数：n 位（4 位、16 位、32 位）。百分比：10%、0.3%。金额照画面，不换算：2 美元、0.008 美元、112.73 美元、57 美分、几美分。版本带名字：torch 2.11、transformers 5.16（录制时）。模型名照旁白写，两行一致：Gemini 3.1 Flash Lite、Gemini 1.5 Flash、Qwen3 0.6B、OPT 350m（代码里的 gemini-3.1-flash-lite 在画面上；和第 5 讲不同，这里不需要 en_display）。日期：2026 年 10 月 31 日。哈希、ID 和 commit 从不念出。

### D. 旁白文件（narration/*.yaml）

- **[D1]** 逐句对齐（explainer/i18n.py）。narration/*.yaml 里 script.md 的每个 SAY 行都有一条（119 段）；`en` 和 SAY 行逐字节相同；`zh` 的条数和 explainer.voice.split_sentences 切出的英文句子数完全一样（这份稿子 357 句）。只在句子内部调整，绝不合并或拆分句子。短句单独成条：再看物理。／记住这个 0。／往回追。／清理。／哪些层？／有效吗？／先从小的说起。／两点友情提示。／全都冻结了。运行 `python -m explainer.i18n check videos/ac215-l08-llm-finetuning --lang zh`，直到输出 OK。
- **[D2]** 不写 say:，不写 anchors。没有中文配音：绝不写 say:，也绝不写 anchors:。字幕按英文音频计时；工具链按位置把每个中文句子和它的英文句子配对。
- **[D3]** 能过检查器的显示行。没有 say: 时，每个显示句都要通过 explainer.i18n.spoken_problems：不用括号（B2），不用数学符号（B3），不出现 letter_letter 名字（A6），数字后面不跟 !，分句不能以“种”结尾再接 ，。！？（“三种办法”在分句中间没问题；不写“有三种。”），汉字和拉丁字母或数字之间有半角空格（B1），每句以 。！？ 或 …… 结尾（后面可以跟 ” 或 」），每个拉丁词都在这份词表里（zh_subtitle、first_use 或 allowed_spoken_latin）。检查器用 [A-Za-z][A-Za-z'.-]* 切词，忽略单个字母：Qwen3 是 Qwen，NF4 是 NF，us-central1 是 us-central，Linear4bit 是 Linear 和 bit，AC215 是 AC，KeyError: 'question' 是 KeyError 和 question'，env.dev、cli.py、train.jsonl、llm-service-account.json 整个算一个词，--prepare 是 prepare，here's 整个算一个词。报出来的拉丁词要么是该译的英文（通常如此），要么是漏掉的实物：按同样的切法加进 allowed_spoken_latin 和对应词条。故意不收复数（adapters、epochs、tokens、layers、images、buckets）：报出复数就是该去掉的英文词形变化（两个 adapter、2 个 epoch、所有 token、两个 image）。
- **[D4]** 英文行（en_display）。双语字幕带显示 SAY 句子，而 SAY 为了配音把实物念成了单词。每个这样的句子都要在 en_display 里给出屏幕上的字面形式，其余照 SAY 逐字写；同一段里的其他句子写 null。念法 → 字面（script.md 开头的清单加上这份词表补充的）：python cli.py dash dash generate / prepare / upload / train / chat / help → python cli.py --generate / --prepare / --upload / --train / --chat / --help；ls dash la slash secrets → ls -la /secrets；slash app → /app；slash secrets → /secrets；slash dot venv → /.venv；dash dash rm → --rm；docker ps dash a → docker ps -a；dot json dot json → .json.json；source, not found → source: not found；key error, question → KeyError: 'question'；tuned model info, none → Tuned model info: None；training job started → Training job started；uploading file → Uploading file；wait for job set to false → wait_for_job=False；disable adapter → disable_adapter()；prepare model for k-bit training → prepare_model_for_kbit_training；drop duplicates → drop_duplicates；train test split → train_test_split；target modules → target_modules；im start / im end → <|im_start|> / <|im_end|>；W naught → W₀；alpha over r → α/r；MLOps Learning → MLOps_Learning；金额：112 dollars 73 → $112.73，0.008 dollars → $0.008，2 dollars → $2。带下划线的名字（A6）只在 en_display 里还原；中文行保留空格形式。英文视频自己的 .srt 不受影响。
- **[D5]** 内容对等。每个中文句子只译它自己的英文句子：不添加命令、参数、括注、中文界面名或解释；只有英文说 extra 的地方才写“额外”；保留英文的词不加中文解释（英文行就在下面）；思考题不给答案（A9）。A5 需要的几个开头词（这个、这次、这里、用、负责训练的）不带内容。
- **[D6]** 固定说法。在这里暂停，把四步都做完。／暂停一下，走到这个提示符。／暂停一下，自己跑一遍 generate 和 prepare。／然后暂停，上传。／接下来看价格表，然后暂停，启动你的任务。／暂停一下，填好你的 endpoint 之后跑一遍。／暂停一下，跑完 Part A。／暂停一下，跑完 Part B。／暂停一下，把第 1 到第 3 步跑一遍。／暂停一下，跑一遍。／暂停一下，开始训练。／暂停一下，跑第 5 步。／暂停一下，把它们都清理掉。／看到标签写着 your turn，就暂停，自己跑这条命令。／有密钥的话，……／没有密钥的话，……／额外加一步：……／第 N 步：／……那一节的第 N 步／录制时／一个小疏漏：……／继续之前，先想一个问题。／暂停一下，想一个问题。／现在，你自己试试。／五道题，自测一下。／回顾一下。／第二部分，……
- **[D7]** 文件。narration/g1.yaml = S01–S09（第一部分：路线 A，用 Gemini 生成人设数据集，再交给托管的微调任务；66 段、192 句），narration/g2.yaml = S10–S16（第二部分：路线 B，在 Colab 里做 QLoRA；53 段、165 句），对应 video.yaml 的两个部分；每个文件开头写一段注释（覆盖范围；用到的规则：A6 空格形式、B3 符号用文字、C1 不加分隔符和 万 / 亿、C2 金额和模型名、D4 en_display、不写 say: / anchors:），保持稿子的顺序。用双引号字符串；YAML 里的双引号和反斜杠要转义。
- **[D8]** 按英文时间轴的长度。中文在英文播放时被阅读；字幕带在英文字幕切换的地方切换（读速超过每秒 9 个单位的中文片段最多多给 1 秒）。每句中文的阅读时间要和英文差不多：每个英文单词最多大约 2 个单位（一个汉字算 1，一个拉丁字母算 0.55），所以去掉多余的连接词和重复的主语，绝不删内容。长实物也占长度（prepare model for k-bit training 17.6 个单位，llm-service-account.json 13.2，python cli.py --generate 13.2，Gemini 3.1 Flash Lite 11.6）：英文没重复的地方不要重复；同一段里第二次提到时用简短的指代（这条命令、这个文件、这个任务、这个模型）。
- **[D9]** 保持英文的分句顺序（系列教训，ac215-video skill）。工具链按分句把中文和英文配对；英文把条件放在后面，中文却放在前面（如果……，就……），相邻两个字幕块的意思就会对调。条件、目的和时间状语放在英文放的位置：有密钥的话，只花几美分；如果你刚改过 env.dev，就重启 container；把它贴到那里；否则 chat 会指向授课老师的 endpoint；分页会在 GPU 显存满了的时候，把优化器状态挪到 CPU 内存里（when 从句放进主句里面）；暂停一下，填好你的 endpoint 之后跑一遍（条件跟英文一样放在主句后面）。

### G. 字幕

- **[G1]** 宽度。双语字幕带：中文一行最多 30 个单位，英文一行 96 个字符；纯中文字幕（.zh.srt）一行 22 个单位，一个字幕块 2 行。分句最好不超过大约 24 个单位，用 ，；： 隔开，给切分器留出干净的切点；避免超过 30 个单位、中间没有标点的分句（Agent Platform User 和模型名单独成一个分句）。
- **[G2]** 字幕块结尾：工具链会去掉字幕块末尾的 。，、；：，保留 ？！…… 和收尾的 ”（subtitles.strip_end）。句末用中文词比用“实物 + 句号”更稳（……进入 dataset-creator 目录。比 ……进入 dataset-creator。读起来稳；两种都合法）。
- **[G3]** 绝不拆开命令。切分器把中文行里两个拉丁词之间的空格当作好切点，所以 python cli.py --prepare 可能被拆到两行，观众就没法照抄了。把整条命令放在分句末尾、全角冒号后面（第 2 步：sh docker-shell.sh。；第 1 步：python cli.py --generate。），一个字幕块最多一条命令，周围少放中文。在渲染出来的 .zh.srt 里检查每个带命令的字幕块。

### H. 标题与配套材料

- **[H1]** 标题（meta.yaml）。视频、部分和章节标题用书面语体（A4：容器、镜像、提示词、端点、存储桶）；问句保留问号；保留英文的冒号结构（量化：……；LoRA：……）；命令、文件名和代码名照写（meta.yaml 不经过检查器，可以用括号）。核心概念的章节带英文简称方便搜索，和第 1、3、5–7 讲一样：端点（endpoint）、量化、LoRA、困惑度。LLM: Finetuning → LLM 微调；比喻保留画面感（三个旋钮；一层薄薄的修正；每个权重 16 个桶；120 GB 的账单）。
- **[H2]** 简介（B 站 / YouTube）：两三句话，书面语体，用这份词表的词：AC215 第 8 讲，跟练 dlops-io/llm-finetuning 和课程的 QLoRA Colab 笔记本；观众做什么、学到什么（路线 A：教师模型 Gemini 写人设数据集，整理成 CSV 和 JSONL，上传到存储桶，交给托管的 Gemini 微调任务并通过端点调用；路线 B：量化、NF4、LoRA，用 QLoRA 训练 Qwen3 0.6B，困惑度评估与保存；结论：微调教会的是口吻，不是事实）；英文旁白，配中文和中英双语字幕；终端输出录于 2026-10-31，没有服务账号密钥和 GPU，所以云端命令停在缺少密钥这一步，正常运行的输出来自 README 和课程团队保存的 Colab 运行。绝不出现人设或授课老师的名字。
- **[H3]** 配套材料：i18n/zh/README.md（以及以后做的 exercises.md / digest.md）用这份词表、按书面语体翻译（A4）。末尾附术语表：English | 这里的说法 | 其他常见译法（fine-tuning：微调 / 精调；endpoint：端点 / 终端节点；adapter：适配器；epoch：轮次 / 训练轮数；loss：损失；perplexity：困惑度；quantization：量化；rank：秩；gradient checkpointing：梯度检查点 / 激活重计算；persona：人设 / 角色；catastrophic forgetting：灾难性遗忘；tokenizer：分词器；tuning job：微调任务 / 调优作业）。
- **[H4]** 配套材料里的代码和命令逐字节不变：代码块、命令、文件名和行内 `code` 都不改；只翻译 # 注释和周围的文字。

### I. 工具链备注

- **[I1]**（请求，第 3 讲起一直未解决）没有 say: 时，`explainer.i18n check` 对显示行套用朗读文本的检查（_SPOKEN_BAD：括号、数学符号、letter_letter 名字）。对只有字幕的视频（这个系列；video.yaml 里没有 languages.zh.voice，词表里 voice: none），这些检查什么也保护不了，反而逼出了 A6 和 B3（这里：drop_duplicates、train_test_split、wait_for_job=False、prepare_model_for_kbit_training、target_modules、disable_adapter()、<|im_start|>、<|im_end|>、α/r、q_proj、v_proj、MLOps_Learning）。建议：词表的 voice 为 none 时，纯显示的句子跳过 _SPOKEN_BAD（保留拉丁词、空格和句末检查）。
- **[I2]**（待办，来自第 1 讲 I3）explainer/subtitles.py 的 `_cuts` 把中文行里拉丁词之间的空格当作好切点，所以命令可能被拆开（G3）。建议：在中文行里，只由空格隔开的一串拉丁词视为不可拆分，除非它本身就超过一行。
- **[I3]**（说明）explainer/subtitles.py 会读所有视频的 glossary.yaml：每个词条 en 字段里 2–3 个词的英文说法会保持在同一行英文里，zh_subtitle 里 2–7 个汉字的中心词会注册进 jieba，对所有视频的字幕都生效。所以这份文件的 en 和 zh_subtitle 只列真正的术语（不写句子）。
