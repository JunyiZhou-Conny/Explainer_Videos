# 中文字幕说明

视频 *AC215 · Lecture 8 — LLM: Finetuning (follow-along: llm-finetuning)*
（**AC215 · 第 8 讲：LLM 微调（跟练：llm-finetuning）**）是英文旁白，配中文字幕和中英双语字幕，没有中文配音。
它是哈佛 AC215（MLOps & LLMOps）第 8 讲的跟练视频，跟的是
[dlops-io/llm-finetuning](https://github.com/dlops-io/llm-finetuning)（`main` 分支，提交 `44ef6f0`）的整份 README
（Prerequisites、Setup GCP Service Account、Generate Question Answer Dataset 到 Chat with Fine-tuned Model），以及课程的
Colab 笔记本（notebook）“Tutorial - Finetuning with QLoRA”。开头是同一个小模型的两个版本回答“天空为什么是蓝色的”：
微调后的那个换上了授课老师的口吻，物理却照样答错。贯穿全片的结论是：**微调教会的是口吻，不是事实**。视频分两部分：

- **第一部分：路线 A，README**（S01–S09）。三个旋钮：提示词和检索改变输入，微调改变权重。然后是准备：
  `llm-service-account` 服务账号和它的两个角色、放在仓库旁边的 `secrets/llm-service-account.json`、`env.dev` 里的项目 ID
  和存储桶、`sh docker-shell.sh`（Debian、Ubuntu 和 WSL 上用 `bash docker-shell.sh`）和 `ls -la /secrets`。在
  `dataset-creator` 容器里，教师模型 Gemini 3.1 Flash Lite 按系统指令和 JSON schema 批量生成人设问答；没有密钥时
  `python cli.py --generate` 的退出码却是 0，错误晚一步才在 `--prepare` 里以 `KeyError: 'question'` 暴露。接着用五个手写的
  脚本数据文件（标签 `scripted`）把一组问答从 CSV 的一行跟到 Gemini 要求的 JSONL，再 `--upload`。在 `gemini-finetuner`
  容器里，`--train` 把任务交给 Google 托管的微调（`us-central1`，打印 `Tuned model info: None`），最后看过时的价格表，
  把自己的端点（endpoint）填进代码，用 `--chat` 对话。
- **第二部分：路线 B，Colab 里的 QLoRA**（S10–S16）。从全参数微调的 120 GB 显存账单讲起（LoRA 降到大约 40 GB，QLoRA
  降到大约 12 GB）；量化：absmax、每 64 个权重一个常数、NF4、双重量化，4 位存储、16 位计算；4 位加载的 Qwen3 0.6B
  和它的聊天模板；LoRA 的低秩更新 W₀ 加上 alpha 除以 r 乘 B 乘 A，秩 8、只改 query 和 value 投影，共 1146880 个
  可训练参数；分页优化器、梯度检查点和 FP16 训练 450 步；用 loss 和困惑度评估（14.15 降到 4，但量的是风格契合度，
  不是回答质量）；保存适配器（adapter）、合并、可选地推送到 Hugging Face，最后清理和回顾。

画面上的终端输出、代码面板、README 引文、示意的控制台和 Colab 界面、标签（`your turn`、`extra`、`scripted`、
`expected`、`recorded`……）、进度条、课件标签和思考题卡片都是英文原样，方便你对照着敲；只有旁白译成了中文。录制时
（2026 年 10 月 31 日）没有服务账号密钥，也没有 GPU：镜像构建、两个容器的 shell、`--help` 和 `--prepare` 都是真实运行的；
每一条要连接 Google 的命令都照原样运行，停在缺少密钥这一步，这些真实的报错都保留了。Gemini 生成的数据、上传、微调任务、
费用和与端点的对话来自 README 自己的说明（标签 `expected`）；Colab 的 QLoRA 运行来自课程团队保存的 A100 运行（标签
`recorded`）。数据集的人设用的是授课老师的名字：画面上遮成灰色的 ‹instructor› 标记，字幕里只说“授课老师”，名字不出现
在任何字幕和文件里；项目 ID、endpoint ID、Hugging Face 账号和密钥也从不出现。

## 文件

视频文件（MP4）是 GitHub release 的附件，不放在 Git 里（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；
字幕、章节和文字稿在渲染之后放进 Git。

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l08-llm-finetuning.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l08-llm-finetuning.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l08-llm-finetuning_part1.*`、`_part2.*` | 第一部分（S01–S09，路线 A：Gemini 生成人设数据集，交给托管的微调任务）和第二部分（S10–S16，路线 B：Colab 里的 QLoRA），各有自己的视频、字幕和章节文件 |
| `output/ac215-l08-llm-finetuning.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l08-llm-finetuning.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l08-llm-finetuning.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文（字幕用；g1 = 第一部分 S01–S09，66 段旁白、192 句；g2 = 第二部分 S10–S16，53 段、165 句）。`en_display:` 是英文字幕行的显示形式：旁白把实物念成单词的地方（python cli.py dash dash generate、ls dash la slash secrets、slash dot venv、key error, question、tuned model info, none、wait for job set to false、drop duplicates、prepare model for k-bit training、im start、W naught、alpha over r、disable adapter、0.008 dollars），英文行换回屏幕上的写法（`python cli.py --generate`、`ls -la /secrets`、`/.venv`、`KeyError: 'question'`、`Tuned model info: None`、`wait_for_job=False`、`drop_duplicates`、`prepare_model_for_kbit_training`、`<\|im_start\|>`、`W₀`、`α/r`、`disable_adapter()`、`$0.008`） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格、数字和换行规则（两份内容一致，yaml 供检查器和字幕切分读取） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L08-llm-finetuning.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L08-llm-finetuning.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l08-llm-finetuning --lang zh   # 中文译文和英文是否逐句对齐、显示行是否干净
python -m explainer.build videos/ac215-l08-llm-finetuning --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l08-llm-finetuning --subs-only     # 只重写字幕（改了译文之后）
```

中文字幕跟着英文旁白的时间轴走：每句中文和它对应的英文句子同时出现，双语字幕在中文的分句处切开，再在英文里
相应的分句处切开，一段中文配一段英文。所以译文必须一句对一句（`check` 会核对），每句中文读起来的时间也要和英文
听起来差不多；而且中文要保持英文的分句顺序：英文把条件、时间或原因放在后面，中文就不把“如果……”“当……时”提到
句首，否则相邻两条双语字幕的中英文会互相错开（例如“分页会在 GPU 显存满了的时候，把优化器状态挪到 CPU 内存里”）。
命令和报错原文放在分句末尾、全角冒号之后（“第 1 步：python cli.py --generate。”），这样字幕切分不会把它们拆到两行上。
渲染之后，在 `.zh.srt` 里再看一遍每条带命令的字幕。

## 译文风格

按中国 MLOps 助教带实验课的说法，和第 1–7 讲一致：

- **一字不改**：你要输入、要在屏幕上对照的东西（命令和参数 `python cli.py --prepare`、`docker ps -a`、`--rm`，文件名、
  目录名和路径 `env.dev`、`llm-service-account.json`、`instruct-dataset.csv`、`train.jsonl`、`/secrets`，服务账号、
  存储桶和区域的名字 `llm-service-account`、`cheese-dataset`、`global`、`us-central1`、`US`，角色名 Storage Admin、
  Agent Platform User，报错和打印出来的文字 `KeyError: 'question'`、`source: not found`、`DefaultCredentialsError`、
  `Tuned model info: None`，JSON 键 contents、parts、question、answer，包名 transformers、bitsandbytes、trl、peft，
  模型名 Gemini 3.1 Flash Lite、Qwen3 0.6B、OPT 350m，数据类型 NF4、FP16、BF16，Colab 界面字样 Save a copy in Drive、
  Change runtime type，以及人设输出里的开场白 Yello、Welcome、good question、glad you ask）。字幕检查器不收的几种写法
  例外：带下划线的名字按旁白的念法写成空格（drop duplicates、train test split、prepare model for k-bit training、
  target modules、disable adapter、im start / im end），检查器不收的符号用文字说（`wait_for_job=False` 写成
  “wait for job 设为 false”，`(19, 2)` 写成“19 乘 2”，`α/r` 写成“alpha 除以 r”，`2e-4` 写成“2 乘 10 的负 4 次方”）；
  英文行通过 `en_display` 保留原样。
- **保留英文**：实验课上本来就说英文的词，封闭清单：第 1 讲的 repo、clone、commit、pin、lock 文件、shell；第 2–4 讲的
  container、image、base image、pull、push、port、API、ID、token、Dockerfile、bucket、bind mount；第 5 讲的 prompt、
  system prompt、LLM、RAG、CLI、embedding；第 6 讲的 notebook、schema、SDK、temperature；第 7 讲的 diff；这一讲新增
  endpoint、LoRA、QLoRA、PEFT、adapter、epoch、batch（只指训练的 batch）、loss、dropout、tokenizer、trainer、absmax、
  unscale。
- **其余用中文标准术语**（中文深度学习资料里的译名，方便搜索）：微调、全参数微调、指令微调、参数高效微调、指令数据集、
  人设、口吻、开场白、口头禅、教师模型、学生模型、合成数据、训练目标、问答对、服务账号、密钥、角色、控制台、区域、
  多区域、系统指令、退出码、异常、形状、样本、验证、随机种子、预测下一个词、微调任务、客户端、显存、梯度、优化器状态、
  滑动平均、激活值、前向传播、反向传播、梯度检查点、分页、学习率、量化、反量化误差、桶、块、常数、分位数、双重量化、
  线性层、归一化层、聊天模板、秩、更新量、正则化、困惑度、灾难性遗忘、基线、基准测试、合并、交付、清理。
- **比喻按意思译，一个比喻一个词**：三个旋钮、桌上摊开的那本书、砖和模具、传送带和带子、显存柱、桶、细条、开关、
  干洗店的取衣单。
- **分清容易混的词**：显存是 GPU memory，内存是 CPU memory，这一讲不出现“记忆”；Cloud Storage 的 bucket 照说，量化的
  bucket 是“桶”；量化时每 64 个权重一“块”，transformer 的 block 是“层”（28 层）；voice 是说话方式，译“口吻”，绝不写
  “声音”；教师模型不是授课老师，学生模型不是学生；笔记本是 laptop，Colab 的 notebook 照说；视频的第一部分 / 第二部分
  不同于 notebook 标题里的 Part A / Part B；`--generate` 生成时的“一批”不同于训练的 batch。
- **精确**：录制时会变的版本号一律带“录制时”（torch 2.11、transformers 5.16）；数字照终端写，不加千位分隔符
  （1146880、16444、30681），旁白用单词说的 million / billion 换成 万 / 亿（5.96 亿、115 万、3.758 亿）；金额照画面
  （112.73 美元、57 美分）；教程里的勘误统一说“一个小疏漏”，后面紧跟改法；课件的笔误说得客气（课件上写的是 18 和 69；
  四舍五入应该是 19 和 70）；思考题只问不答。
- 标题、章节名、简介和这份说明用书面语：容器、镜像、仓库、克隆、提交、存储桶、绑定挂载、提示词、系统提示词、
  端点（endpoint）、适配器（adapter）、轮次（epoch）、批次（batch）、损失（loss）、分词器（tokenizer）、训练器（trainer）；
  LoRA、QLoRA、PEFT、NF4 书面也照写。
- 双语字幕的英文原句就在中文下方，所以字幕里的中文不加括注，也不用任何括号。

完整规则见 [GLOSSARY.md](GLOSSARY.md)（其中提到的“读法”“朗读”规则来自第 1 讲的中文配音版，这个系列只用英文旁白，
不再适用）。

## 术语对照

| English | 这里的说法 | 常见的其他译法 |
| --- | --- | --- |
| fine-tuning | 微调 | 精调 |
| endpoint | endpoint（字幕）；端点（书面） | 终端节点 |
| adapter | adapter（字幕）；适配器（书面） | 适配器 |
| epoch | epoch（字幕）；轮次（书面） | 训练轮数 |
| loss | loss（字幕）；损失（书面） | 损失值 |
| perplexity | 困惑度 | 困惑度 |
| quantization | 量化 | 量化 |
| rank | 秩 | 秩 |
| gradient checkpointing | 梯度检查点 | 激活重计算 |
| persona | 人设 | 角色 |
| catastrophic forgetting | 灾难性遗忘 | 灾难性遗忘 |
| tokenizer | tokenizer（字幕）；分词器（书面） | 分词器 |
| tuning job | 微调任务 | 调优作业 |
| token | token（字幕）；词元（书面） | 令牌 |
| GPU memory | 显存 | 内存（易混） |
