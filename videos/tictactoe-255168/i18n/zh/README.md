# 中文版说明

这是视频 *Why are there exactly 255,168 games of tic-tac-toe?* 的中文版：**井字棋为什么恰好有 255,168 种对局？** 它面向 11–14 岁（小学五六年级到初二）、没学过编程的中国学生和他们的老师：先用纸和笔把井字棋的对局数算出来，再用一段短短的 Python 程序让电脑把每一局都下一遍。旁白：神经网络语音合成（TTS）。画面上的标签和代码注释都译成了中文，字幕是中英双语（中文在上，英文原句在下）。英文原版见 [`../../README.md`](../../README.md)。

## 文件

下表路径都相对于视频目录 `videos/tictactoe-255168/`。`output/zh/` 里的文件由下面的构建命令生成；用 `-q l` 生成的快速草稿，文件名会多一个 `_480p15`。

| 文件 | 说明 |
| --- | --- |
| `output/zh/tictactoe-255168.mp4` | 完整中文版视频（1080p60），中英双语字幕已烧录在画面下方 |
| `output/zh/tictactoe-255168.zh.srt` | 中文字幕 |
| `output/zh/tictactoe-255168.en.srt` | 英文字幕：英文原句，按中文旁白的时间轴 |
| `output/zh/tictactoe-255168.zh-en.srt` / `.zh-en.ass` | 双语字幕；`.ass` 带样式，就是烧录进视频的那一份，上传时也可以作为外挂字幕 |
| `output/zh/chapters.txt` | 章节时间轴，章节名取自 `meta.yaml`，可直接贴进 B 站 / YouTube 简介 |
| `output/zh/transcript.md` | 按章节排列的中英对照旁白稿 |
| [`i18n/zh/meta.yaml`](meta.yaml) | 中文标题、章节名，以及可直接粘贴的视频简介 |
| [`i18n/zh/exercises.md`](exercises.md) | 挑战题：纸笔热身题和“只改一行代码”的编程挑战，答案折叠在每道题下面，最后有“想多了解一点” |
| [`i18n/zh/playground.html`](playground.html) | 交互页面：用浏览器打开就能玩，边下棋边看从这个棋盘往后还可能出现多少种对局，按 X 赢、O 赢和平局分开 |
| [`i18n/zh/assets/play_all_games.py`](assets/play_all_games.py) | 视频里的程序，注释和画面上的中文注释一字不差；用 IDLE 打开按 F5，或在命令行输入 `python play_all_games.py`，输出 `255168`（只用 Python 3，不需要安装第三方库） |
| `i18n/zh/narration/*.yaml`、`i18n/zh/strings/*.yaml` | 逐句对齐英文的中文旁白（含朗读用的 `say:`）和屏幕文字（含代码注释的译文） |
| [`i18n/zh/GLOSSARY.md`](GLOSSARY.md)、[`glossary.yaml`](glossary.yaml) | 术语表与翻译规则（两份内容相同，要同步修改） |

英文版的构建也会顺带生成 `output/tictactoe-255168.zh.srt`、`.zh-en.srt` 和 `.zh-en.ass`，即按英文配音时间轴排的中文 / 双语字幕；加 `--burn` 还会输出烧录了双语字幕的 `.zh-en.mp4`。

## 重新生成

在仓库根目录运行：

```bash
python -m explainer.i18n check videos/tictactoe-255168              # 检查中文旁白与英文是否逐句对齐
python -m explainer.build videos/tictactoe-255168 --lang zh -q l    # 480p15 快速草稿（文件名带 _480p15）
python -m explainer.build videos/tictactoe-255168 --lang zh         # 1080p60 成片
```

`--no-burn` 输出不烧录字幕的干净视频，`--subs-only` 只重写字幕、章节和旁白稿，`--only s03,s04` 只重新渲染部分场景。需要 Noto CJK 字体和 XeLaTeX + ctex（`setup/install.sh` 会安装）；中文旁白的语音在 `video.yaml` 的 `languages: {zh: {voice: …}}` 里设置。

## 中英混用的原则

旁白以普通话为主，只在中文使用者本来就说英文的地方保留英文：玩家 X 和 O、Python、Plan B，以及画面上代码里的名字（explore、winner、None……），这些名字第一次出现时会用中文说明意思（winner 意思是“赢家”，explore 就是“探索”的意思）。已经有标准中文名的概念一律说中文（井字棋、阶乘、函数、列表、递归、回溯），而双语字幕的英文原句就在中文下方，所以中文行不再加英文括注；完整的规则和每个词的取舍理由见 [GLOSSARY.md](GLOSSARY.md)。
