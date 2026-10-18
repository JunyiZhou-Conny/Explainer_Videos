# 中文字幕说明

视频 *AC215 · Lecture 3 — Containers II: five containers, one bucket (follow-along: mega-pipeline)*
（**AC215 · 第 3 讲：容器 II——五个容器，一个存储桶（跟练：mega-pipeline）**）是英文旁白，配中文字幕和中英双语字幕。
它是哈佛 AC215（MLOps & LLMOps）第 3 讲的跟练视频：照着教程仓库
[dlops-io/mega-pipeline](https://github.com/dlops-io/mega-pipeline) 的 README，为五个组件各写一个 Dockerfile，
构建并运行它们的镜像，把一段录音变成英文和法文播客。五个容器之间从不直接通信，只靠一个 Cloud Storage 存储桶传递数据。
画面上的终端输出、代码面板、README 引文和标签都是英文原样，方便你对照着敲。终端输出录于 2026-10-13，录制时没有课程密钥，
所以调用 Google 的步骤只展示命令和该看什么。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l03-mega-pipeline.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l03-mega-pipeline.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l03-mega-pipeline_part1.mp4`、`_part2.mp4` | 上、下两部分：pipeline 与你的第一个 Dockerfile（S01–S07）；包、密钥与全部五个组件（S08–S15） |
| `output/ac215-l03-mega-pipeline.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l03-mega-pipeline.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l03-mega-pipeline.srt` | 英文字幕（上、下两部分也各有自己的 `.srt`、`.zh.srt`、`.zh-en.srt` / `.ass`） |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴 |
| `output/transcript.md` | 按章节排列的完整英文旁白 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：g1 是第一部分（S01–S07），g2 是第二部分（S08–S15）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同，要同步修改） |
| `i18n/zh/meta.yaml` | 中文标题、上下两部分和章节名、简介 |

`output/` 里的文件在场景渲染、拼接之后才生成（见下面“怎么生成”）。MP4 不进 Git，发布时作为 GitHub Release 的附件上传
（[`docs/PUBLISHING.md`](../../../../docs/PUBLISHING.md)）；字幕、章节和文字稿留在仓库里。

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L03-containers-2-mega-pipeline.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L03-containers-2-mega-pipeline.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l03-mega-pipeline --lang zh                # 中文译文和英文是否逐句对齐（158 段、318 句）
python -m explainer.build videos/ac215-l03-mega-pipeline --render-only --jobs 3        # 渲染各场景（1080p60）
python -m explainer.build videos/ac215-l03-mega-pipeline --no-render --crf 27 --burn   # 拼接：英文版、上下两部分、中文 / 双语字幕、烧录版、章节
python -m explainer.build videos/ac215-l03-mega-pipeline --subs-only                   # 只重写字幕（改了译文之后）
```

中文字幕没有单独的时间轴：`script.md` 里每个英文句子对应 `narration/*.yaml` 里的一个中文句子，工具链按英文旁白的计时
把两者配对，再按 GLOSSARY.md 的宽度规则（G1）切成字幕条。双语字幕的英文行默认就是旁白原句；旁白为了配音把实物念成单词的
地方（dash dash r m、slash app、mega-pipeline dot json），`en_display:` 给出屏幕上的写法（`--rm`、`/app`、
`mega-pipeline.json`）。没有中文配音，所以译文里没有 `say:` 和锚点。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、包名、Dockerfile 指令、
报错原文、README 章节标题、屏幕上的 your turn / extra 标签）一字不改；container、image、Dockerfile、bucket、pipeline、
bind mount、push、tag、prompt（只指 Gemini 的 prompt），以及第 1 讲沿用下来的 venv、repo、clone、commit 这些实验课上本来就说
英文的词保留英文；其余用中文标准术语（构建、层、缓存、挂载、构建上下文、构建参数、密钥、服务账号、凭据、应用默认凭据、
访问令牌、身份验证、授权），Google Cloud 的概念用中文文档的译名。README 进度条的步骤叫“第 k 步”，BuildKit 的步骤叫
“构建步骤 k”，两者不混。视频自己的比喻各用一个词：柜子和抽屉（bucket 和它的前缀）、窗（bind mount，写在 /app 下的东西
“直接写进你笔记本上的目录”，从不说“复制回去”）、路标（指向密钥的那个变量）、取件单（长时间运行的操作）。双语字幕的英文原句
就在中文下方，所以中文行不加英文括注。

工具链带来两处写法。带下划线的名字（transcribe_audio、text_prompts、GOOGLE_APPLICATION_CREDENTIALS 等）在中文行里按旁白
的说法写：transcribe audio 目录、text prompts 抽屉、第 10 行那个指向密钥的变量，因为检查器会拒绝带下划线的写法（这项检查是
为中文配音设的，见 GLOSSARY.md 的 I1）；要你输入的命令（`cd transcribe_audio`、`docker build -t transcribe_audio .`）在
英文行里照原样给出。中文行也不用括号和数学符号：写“3.11 及以上”，不写 `>=3.11`。标题、章节名和这份说明用书面语体
（容器、镜像、存储桶、仓库、克隆、推送、绑定挂载）。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 这里的译法 | 常见变体 |
| --- | --- | --- |
| container / image | 字幕：container / image；书面：容器 / 镜像 | 容器实例 |
| layer / writable layer | 层 / 可写层 | 镜像层 / 容器层 |
| build context / build argument (ARG) | 构建上下文 / 构建参数 | 构建变量 |
| bind mount | 字幕：bind mount；书面：绑定挂载 | bind 挂载 |
| bucket | 字幕：bucket；书面：存储桶 | 存储分区、桶 |
| service account | 服务账号 | 服务帐号 |
| application default credentials (ADC) | 应用默认凭据（ADC） | 应用默认凭证 |
| access token | 访问令牌 | token |
| long-running operation | 长时间运行的操作 | LRO |
| push / repo / clone / commit | 字幕照说英文；书面：推送 / 仓库 / 克隆 / 提交 | 代码库 |
