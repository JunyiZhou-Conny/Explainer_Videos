# 中文版说明

这是视频 *Calibrating Noise to Sensitivity — the paper that invented differential privacy* 的中文版：**【论文精读】差分隐私的开山之作：Calibrating Noise to Sensitivity（TCC 2006）**。它讲解 Dwork、McSherry、Nissim 和 Smith 的论文《Calibrating Noise to Sensitivity in Private Data Analysis》（TCC 2006），面向刚接触差分隐私的研究生和研究者，尤其是强化学习、机器学习和医学影像方向的同学。中文旁白由 edge 语音 `zh-CN-XiaoxiaoNeural` 合成，画面上的标签和公式里的文字都译成了中文，字幕是中英双语（中文在上，英文原句在下）。英文原版见 [`../../README.md`](../../README.md)。

## 文件

下表路径都相对于视频目录 `videos/dwork2006-calibrating-noise/`。`output/zh/` 里的文件由下面的构建命令生成。

| 文件 | 说明 |
| --- | --- |
| `output/zh/dwork2006-calibrating-noise.mp4` | 完整中文版视频（1080p60），中英双语字幕已烧录在画面下方 |
| `output/zh/dwork2006-calibrating-noise_part1.mp4` / `_part2.mp4` | 同一视频剪成的上、下两集（定义 → 拉普拉斯机制；隐私预算 → 分离结果 → 后续发展），各自带一套同样的字幕文件 |
| `output/zh/dwork2006-calibrating-noise.zh.srt` | 中文字幕 |
| `output/zh/dwork2006-calibrating-noise.en.srt` | 英文字幕：英文原句，按中文配音的时间轴 |
| `output/zh/dwork2006-calibrating-noise.zh-en.srt` / `.zh-en.ass` | 双语字幕；`.ass` 带样式，就是烧录进视频的那一份，上传时也可以作为外挂字幕 |
| `output/zh/chapters.txt`（`chapters_part1.txt` / `chapters_part2.txt`） | 章节时间轴，章节名取自 `meta.yaml`，可直接贴进 B 站 / YouTube 简介 |
| `output/zh/transcript.md` | 按章节排列的中英对照旁白稿 |
| `i18n/zh/meta.yaml` | 中文标题、分集标题、章节名，以及可直接粘贴的视频简介 |
| [`exercises.md`](exercises.md) | 练习：纸笔题和一道 15 分钟的代码题，答案折叠在每道题下面 |
| [`digest.md`](digest.md) | 论文笔记：带页码的导读、主要结果、勘误和中英术语对照表 |
| [`playground.html`](playground.html) | 交互页面：用浏览器打开，调 ε，切换拉普拉斯 / 高斯 / 均匀噪声，自己扮演攻击者 |
| `i18n/zh/narration/*.yaml`、`i18n/zh/strings/*.yaml` | 逐句对齐英文的中文旁白（含朗读用的 `say:`）和屏幕文字 |
| [`GLOSSARY.md`](GLOSSARY.md)、[`glossary.yaml`](glossary.yaml) | 术语表与翻译规则（两份内容相同） |

英文版的构建也会顺带生成 `output/dwork2006-calibrating-noise.zh.srt`、`.zh-en.srt` 和 `.zh-en.ass`，即按英文配音时间轴排的中文 / 双语字幕；加 `--burn` 还会输出烧录了双语字幕的 `.zh-en.mp4`。

## 重新生成

在仓库根目录运行：

```bash
python -m explainer.i18n check videos/dwork2006-calibrating-noise              # 检查中文旁白与英文是否逐句对齐
python -m explainer.build videos/dwork2006-calibrating-noise --lang zh -q l    # 480p15 快速草稿（文件名带 _480p15）
python -m explainer.build videos/dwork2006-calibrating-noise --lang zh         # 1080p60 成片
```

`--no-burn` 输出不烧录字幕的干净视频，`--subs-only` 只重写字幕、章节和旁白稿，`--only s03,s04` 只重新渲染部分场景。需要 Noto CJK 字体和 XeLaTeX + ctex（`setup/install.sh` 会安装）；中文配音用 edge-tts，需要联网。

## 中英混用的原则

旁白用中国博士生在组会上讲论文的口吻：概念一律用中文差分隐私文献里的标准术语（差分隐私、敏感度、拉普拉斯机制、隐私预算、相邻数据库、数据管理者、记录……），只有符号、人名、论文标题，以及 query、counting query、transcript、leakage、mask、trick、hybrid argument 这几个研究者口头本来就说英文、语音也读得准的词保留英文（paper、setting、clip 只在口头说，书面写论文、设定、梯度裁剪）。双语字幕的英文原句就在中文下方，所以中文行不再给术语加英文括注，只有差分隐私、敏感度、隐私预算这三个核心名字在旁白里各说一次英文；完整的规则和每个词的取舍理由见 [GLOSSARY.md](GLOSSARY.md)。

*片中的论文页面仅用于评论和教学，论文版权归作者和 Springer（LNCS 3876）所有。*
