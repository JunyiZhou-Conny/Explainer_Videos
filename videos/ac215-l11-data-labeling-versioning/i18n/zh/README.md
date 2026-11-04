# 中文字幕说明

视频 *AC215 · Lecture 11 — Data labeling and versioning: a label is a record, a version is a fingerprint (follow-along: data-labeling + data-versioning)*
（**AC215 · 第 11 讲：数据标注与版本管理——Label Studio、CORS、DVC 与 gcsfuse（跟练：data-labeling + data-versioning）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 11 讲“数据标注、版本管理与监控”的跟练视频，
照着两个教程仓库的 README 从头做到尾，分两部分：

- **第一部分（S01–S08）**：[dlops-io/data-labeling](https://github.com/dlops-io/data-labeling)（commit `03c3e27`）。
  从“两个同名的 cheese_dataset 目录”这个谜题开始；建服务账号 `data-service-account` 和 JSON 密钥，下载并整理 21 张奶酪照片，
  建 bucket 和 `cheeses_unlabeled` / `cheeses_labeled` 两个目录；用一条 `docker run` 在本地容器里跑起 Label Studio
  （Linux 上数据目录归 root 所有导致容器退出的修法）；配置 source / target storage，看清是谁在碰照片的字节：
  Label Studio 用密钥签发预签名 URL，浏览器拿着这张“票”直接去 Google 取图，所以 CORS 规则要配在 bucket 上；
  一条标注在磁盘上就是一张指回原图的 JSON 小纸条；用容器名从命令行容器读回标注（Label Studio 1.23.0 默认关闭 legacy token 导致的 401 和修法）；
  最后是 docker-compose 的 Extra 一节和清理。
- **第二部分（S09–S16）**：[dlops-io/data-versioning](https://github.com/dlops-io/data-versioning)（课程 pin 住的 README `b240b1a`，
  在 starter 分支 `data-versioning-ac215` 的 `23762e4` 上运行，外加 Dockerfile 第 36 行的一词修复）。从 starter 建你自己的私有仓库；
  gcsfuse 和 bind mount 怎样把 bucket 挂成目录、`--implicit-dirs` 的陷阱、为什么笔记本上的目录是空的；`dvc init`、默认 remote、
  `dvc add` 怎样按 MD5 指纹把文件放上缓存的“架子”、写出 manifest 和指针文件；`dvc push`、`git tag dataset_v20`，和授课老师的 tag 一字不差；
  第二个版本 `dataset_v21` 只多推两个对象；在 Colab 里用 `dvc get --rev` 做时间旅行（以及 `--quiet` 藏起来的错误）；监控、收尾清单和回顾。

画面上的终端输出、代码面板、README 引文、示意控制台和 Label Studio / GitHub / Colab 页面、地图、签了名的票、保安、指纹架子、绳子和各种标签
（`your turn`、`extra`、`stand-in`、`illustration`、`recorded`、金色的计费标签、`Lecture 11 · slides …`）都是英文原样，方便你对照着敲。
画面上出现授课老师名字的地方遮成 ‹instructor›，字幕里一律写“授课老师”。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-10-23，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。
README 的每条命令按原样、按顺序运行；README 里没有、但有助于理解的检查（`git log`、`tree`、`ls`、`md5sum`、`docker container ls -a`、
`docker logs`、等待循环、`git diff` 等）在画面上标着 `extra`。

录制机器**没有 Google 账号、没有 bucket、没有浏览器，也没有通往 GitHub 的 SSH 通道**。所以：

- 本地的部分都是实录：Label Studio 容器、它的 API、Docker 网络和 Compose、DVC 容器的构建（包括 starter 构建失败）、`dvc init`、`dvc add`、
  缓存的目录结构、git 的提交和 tag。
- 每个需要真实凭据的云端步骤都录到它如实的失败为止（找不到 `/secrets/data-service-account.json`、bucket 挂不上）。目录列表里出现的密钥
  是一个明显无效的替身，每个云端步骤之前都移走了；视频在 S05 如实说明了这一点。
- 你自己跟着做时应当看到的成功结果标着 `recorded`，并注明出处（README、代码本身的输出、Colab notebook 里保存的输出）；
  Label Studio 里的点击和上传用它自己的 API 调用在本地重放，标着 `stand-in`（所以替身里是 3 个 task，你那边是 21 个）；
  `dvc push` 的推送摘要来自一个本地的替身 remote。
- 会变的版本号字幕里都加“录制时”（Label Studio 1.23.0、DVC 3.63.0、Colab 里的 DVC 3.67.1）。

本讲会在你自己的 GCP 项目里存几 MB 数据：每个计费点都有金色标签，S16 是完整的收尾清单。只要还有哪个 tag 要用，就别删 `dvc_store`。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l11-data-labeling-versioning.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l11-data-labeling-versioning.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l11-data-labeling-versioning_part1.*`、`_part2.*` | 上下两部分（S01–S08：Label Studio、预签名 URL、bucket 上的 CORS、标注即记录、Compose 和清理；S09–S16：你自己的仓库、挂载的 bucket、按指纹命名的文件、指针与 tag、第二个版本、Colab 时间旅行、监控和收尾），每部分有自己的视频和字幕文件 |
| `output/ac215-l11-data-labeling-versioning.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l11-data-labeling-versioning.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l11-data-labeling-versioning.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S08），`g2` 是第二部分（S09–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，下载链接见
[`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令、真实输出和练习答案
在学习指南 [MLOps_Learning · guides/L11-data-labeling-versioning.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L11-data-labeling-versioning.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l11-data-labeling-versioning --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l11-data-labeling-versioning --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l11-data-labeling-versioning --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l11-data-labeling-versioning --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（113 段），`en` 和 SAY 逐字相同；`zh` 按
`explainer.voice.split_sentences` 切出的英文句子一句对一句（共 348 句：第一部分 167 句，第二部分 181 句），不合并、不拆分。
字幕按英文旁白录下的时间显示：双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序
（条件和时间从句留在英文放的位置）。SAY 为了让语音读对，把实物念成了单词（dash d、8080 colon 8080、slash secrets、
data-service-account dot json、cheese dataset、DVC store、Image 1、dataset v20、implicit dirs、the quiet flag、dash r）；
这些句子（40 段）在 `en_display:` 里给出屏幕上的写法（`-d`、`-p 8080:8080`、`/secrets`、`data-service-account.json`、`cheese_dataset`、
`dvc_store`、`Image_1`、`dataset_v20`、`--implicit-dirs`、`--quiet`、`-r`），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、image / container / 网络的名字、
服务账号名、角色名、控制台和 Label Studio 上的按钮、模板名、奶酪选项、tag 和分支名、版本号、HTTP 状态码）一字不改；
旁白转述的报错信息译成中文（找不到文件、它的数据目录不可写、包 google-cloud-sdk 没有可安装的候选版本、未知的 Git 修订版本），
终端和英文行保留原文。实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、pin、root、container、image、tag、push、port、
localhost、bind mount、bucket、ADC、CORS、origin，加上这一讲的 label、task、ground truth、source storage、target storage、pre-signed URL、
legacy token、personal token、DVC、remote、manifest、MD5、entrypoint、capability、max age、starter、fork、patch、diff；
其余用中文标准术语（Google Cloud、MDN 和 Git 的中文文档）：标注、数据集、版本管理、指纹、缓存、指针文件、前缀、对象、标记对象、
数据湖、挂载、挂载点、服务账号、密钥、凭据、访问令牌、跨域、同源规则、预检请求、响应头、分支、暂存、安全目录、监控、漂移。
label（点的类别词、磁盘上的那张小纸条）、标注（这个活动和那条记录）和标签（只指画面上的 your turn / extra / 金色标签）始终分开。

视频里的比喻按意思译，一个比喻一个词：站（标注站、版本管理站）、街道（Docker 网络）、门（发布的 port）、票（签了名的网址）、
保安（CORS，同第 10 讲）、小纸条（一条 label）、架子（缓存里以指纹前 2 个字符命名的目录）、绳子（tag → 指针文件 → manifest → 照片）、
电话簿（Docker DNS）、时间旅行（回到之前的版本）。README 的疏漏照英文的语气温和地说（统一说“一个小疏漏”），后面紧跟改法。
字幕检查不允许中文行里出现下划线名字，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：`cheese_dataset` → cheese dataset，
`cheeses_unlabeled` / `cheeses_labeled` → cheeses unlabeled / cheeses labeled，`dvc_store` → DVC store，`dataset_v20` → dataset v20，
`depends_on` → depends on 这个设置。授课老师的名字从不出现在字幕、标题、章节名和简介里。双语字幕的英文原句就在中文下方，
所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。
