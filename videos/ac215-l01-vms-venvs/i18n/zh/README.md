# 中文字幕说明

视频 *AC215 · Lecture 1 — Virtual machines, virtual environments and uv (follow-along: simple-translate)*
（**AC215 · 第 1 讲：虚拟机、虚拟环境与 uv（跟练：simple-translate）**）是英文旁白，配中文字幕和中英双语字幕。
它是哈佛 AC215（MLOps & LLMOps）第 1 讲的跟练视频：照着教程仓库
[dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) 的 README，先在 Google Cloud 的一台
VM 上用 `sudo pip3` 手动安装一个命令行翻译小应用，再换一台全新的 VM，用 uv 建虚拟环境重装一遍。
画面上的终端输出、代码面板、README 引文和示意控制台都是英文原样，方便你对照着敲。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l01-vms-venvs.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本 |
| `output/ac215-l01-vms-venvs.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l01-vms-venvs.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l01-vms-venvs.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l01-vms-venvs.srt` | 英文字幕 |
| `output/chapters.txt` | 章节时间轴 |
| `i18n/zh/narration/*.yaml` | 逐句对齐英文的中文译文（字幕用；`en_display:` 是英文字幕行的显示形式） |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则 |
| `i18n/zh/meta.yaml` | 中文标题、章节名和简介 |

练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令的完整清单和中文速览在学习指南
[MLOps_Learning · guides/L01-vms-venvs.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L01-vms-venvs.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l01-vms-venvs --lang zh   # 中文译文和英文是否逐句对齐
python -m explainer.build videos/ac215-l01-vms-venvs --burn          # 英文版 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l01-vms-venvs --subs-only     # 只重写字幕（改了译文之后）
```

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、包名、环境变量、
报错原文、控制台按钮、README 章节标题）一字不改；VM、venv、uv、PATH、shell、repo、lock 文件、pin 等实验课上本来就
说英文的词保留英文；其余用中文标准术语（虚拟机、虚拟环境、终端、提示符、包、依赖、解释器、软链接、激活、解析、约束），
GCP 概念用中文控制台的译名（区域、可用区、机器类型、启动磁盘、结算）。双语字幕的英文原句就在中文下方，所以中文行
一般不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)（其中关于中文配音朗读的部分现在不再使用：这个系列只用英文旁白）。
