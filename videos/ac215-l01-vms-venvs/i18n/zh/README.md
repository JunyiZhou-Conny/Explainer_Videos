# 中文版说明

这是视频 *AC215 · Lecture 1 — Virtual machines, virtual environments and uv (follow-along: simple-translate)* 的中文版：**AC215 · 第 1 讲：虚拟机、虚拟环境与 uv（跟练：simple-translate）**。它是哈佛 AC215（MLOps & LLMOps）第 1 讲的跟练视频：照着教程仓库 [dlops-io/simple-translate](https://github.com/dlops-io/simple-translate) 的 README，先在 Google Cloud 的一台 VM 上用 `sudo pip3` 手动安装一个命令行翻译小应用，再换一台全新的 VM，用 uv 建虚拟环境重装一遍。面向上 AC215 的中文研究生：会 Python 和基础机器学习，英文技术文档读得很顺，但第一次在云上开 VM。旁白：神经网络语音合成（TTS）。讲解、标签和比喻译成了中文；终端输出、代码面板、README 引文和示意控制台保持英文原样，好让你对照着敲。字幕是中英双语（中文在上，英文原句在下）。英文原版的旁白稿见 [`../../script.md`](../../script.md)。

## 怎么跟着做

1. **先做完 Tutorial 0**：要有一个开通了结算的 Google Cloud 项目。今天不需要服务账号和密钥，有浏览器就行。
2. **把 README 打开，放在视频旁边。** 视频走的是 README 的两节：*Installing App on VM Manually*（第一部分，10 步）和 *Installing App on VM using UV*（第二部分，12 步）。想让自己电脑上的克隆和画面里的行号完全一致，就检出视频用的提交 `62f821b`（在 [MLOps_Learning](https://github.com/JunyiZhou-Conny/MLOps_Learning) 里运行 `uv run tools/sync_tutorials.py --only 1 --pinned`）。
3. **看左上角的进度条**：它显示 README 的哪一节、第几步（“第 3 步，共 10 步：apt-get update”）。代码面板标出文件和行号（`cli.py · 第 5–9 行`），在自己的克隆里能找到同样的行。
4. **看到黄色的“▶ 轮到你了”就暂停**，在自己的 VM 上跑这条命令，再继续看。灰色的“额外”标签表示 README 里没有这条命令（比如 `which python`）；这些都是安全的检查，也一起跑。
5. **每条命令也都在学习指南里**，可以直接复制：[MLOps_Learning · guides/L01-vms-venvs.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L01-vms-venvs.md)。
6. **用完就删除 VM。** VM 只要还在就在花钱；只停止的话，启动磁盘还在计费。第 7 章和第 15 章各删一次（连同启动磁盘），再确认 VM instances 和 Disks 页面（中文界面：VM 实例、磁盘）都是空的。

终端输出取自 2026-10-12 按 README 实际运行的记录（全新的 Debian 12 / 13 环境，来源见 [`../../ASSETS.md`](../../ASSETS.md)）。uv 和 Python 的版本号会变（录制时是 uv 0.13.0、CPython 3.15.0），以你自己 VM 上的为准。录制时 Google 的非官方翻译接口对第一部分返回了 429（限流），所以第 6 章里正常翻译的结果标着“预期输出”；这一章也讲了怎么读这个 traceback、遇到了怎么办。

## 练习

看完后先别回看，直接做 [`exercises.md`](../../exercises.md)（目前只有英文版）：A 部分是视频最后的五道自测题，B 部分动手（先预测，再运行），C 部分排错，D 部分思考；答案折叠在每道题下面。哪题错了，只回看对应的章节（章节时间见 `output/zh/chapters.txt`）。

## 文件

下表路径都相对于视频目录 `videos/ac215-l01-vms-venvs/`。`output/zh/` 里的文件由下面的构建命令生成；用 `-q l` 生成快速草稿时，视频和字幕的文件名会多一个 `_480p15`。

| 文件 | 说明 |
| --- | --- |
| `output/zh/ac215-l01-vms-venvs.mp4` | 完整中文版视频（1080p60），中英双语字幕已烧录在画面下方 |
| `output/zh/ac215-l01-vms-venvs_part1.mp4` / `_part2.mp4` | 同一视频剪成的上、下两集（第 1–7 章：云端 VM 与手动安装；第 8–15 章：用 uv 管理虚拟环境），每集都有自己的一套字幕文件（`.zh.srt`、`.en.srt`、`.zh-en.srt` / `.ass`） |
| `output/zh/ac215-l01-vms-venvs.zh.srt` | 中文字幕 |
| `output/zh/ac215-l01-vms-venvs.en.srt` | 英文字幕：英文原句，按中文配音的时间轴 |
| `output/zh/ac215-l01-vms-venvs.zh-en.srt` / `.zh-en.ass` | 双语字幕；`.ass` 带样式，就是烧录进视频的那一份，也可以在本地播放器里作为外挂字幕加载 |
| `output/zh/chapters.txt`（`chapters_part1.txt` / `chapters_part2.txt`） | 章节时间轴，章节名取自 `meta.yaml`，可直接贴进 B 站 / YouTube 简介 |
| `output/zh/transcript.md` | 按章节排列的中英对照旁白稿 |
| [`i18n/zh/meta.yaml`](meta.yaml) | 中文标题、分集标题、章节名，以及可直接粘贴的视频简介 |
| `i18n/zh/narration/*.yaml`、`i18n/zh/strings/*.yaml` | 逐句对齐英文的中文旁白（含朗读用的 `say:` 和英文字幕行 `en_display:`）和屏幕文字 |
| [`i18n/zh/GLOSSARY.md`](GLOSSARY.md)、[`i18n/zh/glossary.yaml`](glossary.yaml) | 术语表与翻译规则（两份内容相同，要同步修改） |
| [`exercises.md`](../../exercises.md) | 练习与答案（英文） |

英文版的构建也会顺带生成 `output/ac215-l01-vms-venvs.zh.srt`、`.zh-en.srt` 和 `.zh-en.ass`，即按英文配音时间轴排的中文 / 双语字幕；加 `--burn` 还会输出烧录了双语字幕的 `.zh-en.mp4`。

## 重新生成

在仓库根目录运行：

```bash
python -m explainer.i18n check videos/ac215-l01-vms-venvs                   # 检查中文旁白与英文是否逐句对齐
python -m explainer.script videos/ac215-l01-vms-venvs/script.md --lang zh   # 合成全部中文旁白，逐段和英文比时长
python -m explainer.build videos/ac215-l01-vms-venvs --lang zh -q l         # 480p15 快速草稿（文件名带 _480p15）
python -m explainer.build videos/ac215-l01-vms-venvs --lang zh --crf 25     # 1080p60 成片
```

`--no-burn` 输出不烧录字幕的干净视频，`--subs-only` 只重写字幕、章节和旁白稿，`--only s03,s04` 只重新渲染部分场景。需要 Noto CJK 字体和 XeLaTeX + ctex（`setup/install.sh` 会安装）。中文旁白用工具链默认的 edge `zh-CN-XiaoyiNeural`（`video.yaml` 里没有设置 `languages: {zh: {voice: …}}`）；免费的 Edge 端点没有发布授权，发布前设置 `AZURE_SPEECH_KEY` 和 `AZURE_SPEECH_REGION`，同一个声音就会改走官方的 Azure AI Speech（见 [`docs/LANGUAGES.md`](../../../../docs/LANGUAGES.md)）。

## 中英混用的原则

旁白用中国 MLOps 助教带实验课的口吻。你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、包名、环境变量、报错原文、英文控制台上的按钮、README 的章节标题）一字不改，照英文读：点读“点”，斜杠读“斜杠”，参数前缀读“杠”。VM、venv 跟着英文走；另外只有实验课上本来就说英文的 shell、root、repo、clone、commit、import、traceback、lock 文件、pin、hypervisor 保留英文。其余一律用中文标准术语（虚拟机、虚拟环境、终端、提示符、包、依赖、解释器、软链接、激活、解析、约束），GCP 的概念用中文控制台的译名（区域、可用区、机器类型、启动磁盘、结算）。版本号按整数组读（3.11.2 读“三点十一点二”）。双语字幕的英文原句就在中文下方，所以中文行不加英文括注，只有 hypervisor（虚拟机监控器）、externally managed（由外部管理）、外部 IP（也就是公网 IP）三处例外。完整的规则和每个词的取舍理由见 [GLOSSARY.md](GLOSSARY.md)。

## 对照表

**中文控制台对照。** 片中的控制台是示意图，界面文字和 README 一样用英文。你的 Google Cloud 控制台如果是中文界面，对应关系如下：

| 英文界面 | 中文界面 | 英文界面 | 中文界面 |
| --- | --- | --- | --- |
| Create instance | 创建实例 | Region | 区域 |
| VM instances | VM 实例 | Zone | 可用区 |
| Disks | 磁盘 | Machine type | 机器类型 |
| Authorize | 授权 | Boot disk | 启动磁盘 |
| Delete | 删除 | External IP | 外部 IP |
| Stop | 停止 | Billing | 结算 |
| Enable | 启用 |  |  |

**术语对照。** 中文资料里同一个概念常有几种说法，搜索时可以都试试：

| English | 本片用词 | 其他常见说法 |
| --- | --- | --- |
| symlink | 软链接 | 符号链接 |
| lock file (`uv.lock`) | lock 文件 | 锁文件 |
| pin | pin（把版本 pin 住） | 固定版本 |
| constraint (`requires-python`) | 约束 | 版本约束 |
| resolve / resolver | 解析 / 解析器 | 依赖解析 |
| transitive dependency | 传递依赖 | 间接依赖 |
| endpoint | 接口 | 端点 |
| rate-limited (HTTP 429) | 被限流 | 速率限制 |
| shadowing | 遮蔽 |  |
| idempotent | 幂等（可以放心重复执行） |  |
| externally managed environment (PEP 668) | 由外部管理的环境 |  |

教程仓库的 README 和代码归 AC215 教学团队（哈佛 IACS）所有；片中引用仅用于学习，已获授课老师许可。
