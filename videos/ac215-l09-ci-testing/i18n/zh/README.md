# 中文字幕说明

视频 *AC215 · Lecture 9 — CI & unit testing: the pre-commit gate (follow-along: cheese-app-ci-cd + babykev)*
（**AC215 · 第 9 讲：CI 与单元测试——pytest、pre-commit，提交前的质量门（跟练：cheese-app-ci-cd + babykev）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 9 讲“自动化软件开发：CI 与单元测试”的跟练视频，分两部分：

- **第一部分（S01–S09）**：照着教程仓库 [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd)
  的 README（Part 1–4），先看一个课堂上真的被提交进去的 bug，再讲单元、集成、系统三类测试、测试金字塔和封闭测试（hermetic）；
  然后在 Docker 镜像里运行应用和三类 pytest 测试，用 black 和 flake8 分清格式化工具和代码检查工具（linter），
  看“1 passed, 4 skipped”为什么不等于全部通过，最后装上 pre-commit 钩子，看一次提交被拦下、修好、再放行。
- **第二部分（S10–S15）**：跟着 Rahul Dave 的客座讲座项目 [rahuldave/babykev](https://github.com/rahuldave/babykev)
  （步骤笔记在 [rahuldave/babykev-walk](https://github.com/rahuldave/babykev-walk) 的 walk.md，step-00 到 step-05b）：
  uv 的锁文件、`just check` 一条命令当门禁、覆盖率下限、94% 的覆盖率仍然放过一个错的掩码（mask）、hypothesis 属性测试
  自己找到并收缩出最小的反例、用 marker 给不封闭的测试一个诚实的位置，以及为什么钩子之外还需要 CI；最后是 README 的 Docker 清理和回顾。

画面上的终端输出、代码面板、README 引文、门禁表、掩码网格和各种标签（`your turn`、`extra`、`illustration`、`recorded`、
`Lecture 9 · slides …`）都是英文原样，方便你对照着敲。这一讲全程在本地运行，不需要云资源，也不产生任何费用。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-10-19，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出：

- **cheese-app-ci-cd**：在一个全新、空白的容器里录制（`docker:29.8.2-dind`，代替装了 Docker Desktop 的笔记本），
  README 的每条命令按原样、按顺序运行：clone、Part 1–4、Docker Cleanup。README 里没有、但有助于理解的检查（`git log`、`ls -la`、
  等服务器就绪的循环、没有服务器时的系统测试、`git diff` / `git add -u`、被拦下的提交、`pre-commit uninstall` 等）在画面上标着 `extra`。
- **babykev**：在一台普通的 Debian 12 机器上录制（一个全新的 `python:3.12-slim-bookworm` 容器），**没有 Docker**，
  只装了 uv 0.13.2 和 just 1.59.0，按 walk.md 一步步切到 step-00 … step-05b 运行。所以：
  - 需要 Docker 的 recipe 会礼貌地失败（`docker build` 报 `command not found`，构建镜像的 recipe 会说明原因）；
    walk.md 记录的镜像大小（1.15 GB、1.84 GB）和断网运行 `just check` 的实验以 `recorded` 标签展示，来源是 walk.md。
  - 在 step-05a / step-05b，这台 Linux x86 机器上的 `just test` 如实显示 **1 failed, 102 passed**：
    `test_a_question_cannot_see_its_sibling` 要求输出逐位相同，而 torch 2.14.1+cpu 在这里的求和顺序和作者的 Mac 不同。
    作者 Mac 上的 **103 passed** 作为录制记录展示（`recorded`，来源 walk.md）。视频把它讲成一个教学点：hermetic 只保证
    “只有你的代码能让测试失败”，跨机器逐位一致是更强的承诺；这不是 babykev 的 bug，也不是你的操作错误。
- 会变的版本号、带 warning 的计数、耗时和回收的空间大小，字幕里都加“录制时”（black 26.10.1、flake8 7.4.1、pre-commit 4.7.0、
  pytest 9 的“1 warning”、uv 0.13.2、torch 2.14.1、大约 95 MB）。

你自己跟着做时，在装了 Docker Desktop 的笔记本上运行：cheese 的部分结果应当相同；babykev 的镜像会真正构建出来，
`just test` 的结果取决于你的 CPU。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l09-ci-testing.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l09-ci-testing.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l09-ci-testing_part1.*`、`_part2.*` | 上下两部分（S01–S09：cheese-app-ci-cd，测试、格式化与 pre-commit 门禁；S10–S15：babykev，一条命令的门禁、全绿却是错的、属性测试、CI 与收尾），每部分有自己的视频和字幕文件 |
| `output/ac215-l09-ci-testing.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l09-ci-testing.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l09-ci-testing.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S09），`g2` 是第二部分（S10–S15）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，下载链接见
[`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令、真实输出和练习答案
在学习指南 [MLOps_Learning · guides/L09-ci-testing-precommit.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L09-ci-testing-precommit.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l09-ci-testing --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l09-ci-testing --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l09-ci-testing --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l09-ci-testing --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（92 段），`en` 和 SAY 逐字相同；`zh` 按
`explainer.voice.split_sentences` 切出的英文句子一句对一句（共 335 句），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置；纯中文字幕每行最多 22 个单位、每条最多两行。
SAY 为了让语音读对，把实物念成了单词（dash r a、dot git、git commit, dash dash no verify、test underscore broken、
torch dot ones like）；这些句子在 `en_display:` 里给出屏幕上的写法（`-ra`、`.git`、`git commit --no-verify`、`test_broken`、
`torch.ones_like`），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名、路径、镜像名、工具名、recipe 名、
babykev 的 step 标签、错误代码、终端原文，以及进度条上 README 的 Part / Option 名称）一字不改；终端打印的结果也照原样写
（11 passed、10 passed, 1 warning、1 passed, 4 skipped、Skipped、Failed、files were modified by this hook、WRONG）。
实验课上本来就说英文的词保留英文：前几讲的 venv、root、repo、clone、commit、pin、container、image、Dockerfile、tag、port、localhost、
API、ID、bug，加上这一讲的 hook、linter / lint、hermetic、fixture、parametrize、marker、assert、recipe、mask、causal mask、token、
milestone、CI；其余用中文标准术语（测试、单元测试、集成测试、系统测试、冒烟测试、验收测试、测试金字塔、格式化工具、覆盖率、
覆盖率下限、收集器、跳过、暂存、lock 文件、属性测试、反例、收缩、类型检查器）。门禁（gate）是这一讲的主线词：字幕和文档都说门禁，
标题跟 Bilibili 标题一致，写“质量门”；第 4 讲的“关卡”是另一张图（账号、角色、API 三道关），不混用。

画面不翻译，所以旁白提到画面上的标签时，字幕照画面写（黄色的 your turn 标签、灰色的 extra 标签）。字幕检查不允许中文行里出现
下划线名字、等号、加号、尖括号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：`test_broken` → test 下划线 broken，
`--max-line-length=120` → --max-line-length 设成 120，`DEV=1` → DEV 设成 1，`line-length = 100` → line-length 设成 100，
`torch.ones_like` → torch 的 ones like，`branch_mask` → branch mask，`power(3, 2)` → power，参数是 3 和 2。
README 的小疏漏照英文的语气温和地说（统一说“一个小疏漏”），后面紧跟改法；会变的版本号和大小每次都加“录制时”。
双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| gate / gate table / turnstile | 门禁 / 门禁表 / 闸机 | 质量门、质量门禁 |
| commit / stage / history | commit / 暂存 / 历史 | 提交 / 暂存区 |
| hook / pre-commit | hook / pre-commit | 钩子、Git 钩子 |
| formatter / linter / lint | 格式化工具 / linter / lint | 格式化器 / 代码检查工具、静态检查 |
| unit / integration / system test | 单元测试 / 集成测试 / 系统测试 | 同左 |
| smoke test / acceptance test | 冒烟测试 / 验收测试 | 同左 |
| testing pyramid | 测试金字塔 | 同左 |
| hermetic | hermetic | 封闭测试、密封测试、自包含测试 |
| fixture / parametrize / marker | fixture / parametrize / marker | 夹具 / 参数化 / 标记 |
| collect / collector / skip / deselect | 收集 / 收集器 / 跳过 / 排除 | 取消选中 |
| coverage / coverage floor | 覆盖率 / 覆盖率下限 | 代码覆盖率 / 覆盖率阈值 |
| property test / counter example / shrink | 属性测试 / 反例 / 收缩 | 基于属性的测试 / 反例 / 最小化 |
| lockfile | lock 文件 | 锁文件 |
| recipe (just) | recipe | 配方、任务 |
| type checker / diagnostics | 类型检查器 / 诊断 | 类型检查工具 |
| mask / causal mask | mask / causal mask | 掩码 / 因果掩码 |
| state / question / sibling question | 状态 / 问题 / 兄弟问题 | — |
| CI | CI | 持续集成 |
