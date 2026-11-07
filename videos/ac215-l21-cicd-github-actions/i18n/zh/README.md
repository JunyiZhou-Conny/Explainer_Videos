# 中文字幕说明

视频 *AC215 · Lecture 21 — CI/CD with GitHub Actions II: one push, six fresh machines (follow-along: cheese-app-ci-cd)*
（**AC215 · 第 21 讲：用 GitHub Actions 做 CI——一次 push，六台全新的机器（跟练：cheese-app-ci-cd）**）是英文旁白，
配中文字幕和中英双语字幕，没有中文配音。它是哈佛 AC215（MLOps & LLMOps）第 21 讲“Automating Software Development: CI/CD with
GitHub Actions II”的跟练视频，对照课件逐页讲解，并照着教程仓库 [dlops-io/cheese-app-ci-cd](https://github.com/dlops-io/cheese-app-ci-cd)
的 README 一步一步做“Part 5: GitHub Actions (Remote CI)”，再加可选的“Part 6: Branch Protection”（版本见 [`ASSETS.md`](../../ASSETS.md)：
`main` @ `b8458ff`，唯一的分支，2026-11-06 仍是最新）。同一个仓库的 Part 1–4 是第 9 讲的内容
（[`ac215-l09-ci-testing`](../../../ac215-l09-ci-testing/)），本片只回指，不重做。分两部分：

- **第一部分（S01–S07）**：从一个谜题开始：一次运行的汇总说所有测试都通过了，整个运行却是红的。然后是课上的回顾（本地钩子（hook）只留在
  装过它的笔记本上）、远程钩子（pre-receive、update、post-receive）以及它们在 GitHub.com 上对应的 Actions 和分支保护；课上的 CI 循环；
  把 `.github/workflows/ci.yml` 读成“事件 → 工作流 → job → 步骤”；触发条件（推送到 `main` / `develop`、合并进它们的拉取请求（PR）、临时合并的
  提交）；六个 job 的 `needs` 依赖图；推送到你自己的 GitHub 仓库；在 Actions 页看第一次运行：五个 job 绿，Lint and Format Check 红。
- **第二部分（S08–S16）**：逐个 job 打开日志：镜像只构建一次，存成 tar、作为 artifact 传给每台空的 runner（`docker load -i`）；
  每个步骤都是一道读退出码的门禁（Black 阻断，Flake8 只提示）；unit / integration / system 三个测试 job（`continue-on-error` 把覆盖率
  那一步的失败旁路掉、`curl -f` 这道门禁、`--network host`）；Test Summary 只听它 `needs` 里的测试 job，所以 lint 失败它听不见，课上
  演示提交里的 bug 它却听见了；用 `pre-commit run --all-files` 修好格式，运行变绿；课上的“本地难题”：`git commit --no-verify` 绕过
  本地钩子，CI 把它拦下，但七项卫生检查在 CI 里从来不跑；webhook、仓库机密（secret）和 Slack 通知（以及“这只铃只在有好消息时才响”的一行修复）；
  用分支保护和必需的状态检查把报告变成门禁；最后是 ML 带来的不确定性、下一步的 CD 和五道自测题。

画面上的终端输出、代码面板、job 日志、步骤列表、运行的依赖图、README 引文、示意的 GitHub 页面和各种标签（`your turn`、`extra`、
`illustration`、`Lecture 21 · slides …`）都是英文原样，方便你对照着敲。授课老师的名字从不出现在画面、字幕、标题、章节名和简介里。

## 怎么录制的

终端输出全部来自真实运行（`assets/terminal/`，录于 2026-11-06，详见 [`ASSETS.md`](../../ASSETS.md)），没有手打的输出。录制机器
没法推送到 GitHub，所以同一台机器上的一个空仓库代替“你的仓库”；`ci.yml` 的每个 job 都在一台 Docker 是空的全新机器上照着工作流
文件实际跑过（构建、`docker save` / `docker load`、Black 和 Flake8、三个层级的 pytest、Test Summary 的脚本），再用 `act` 把整个文件
用第二种方式跑了一遍，结论相同。所以 GitHub 网页上的部分（Actions 列表、运行的依赖图、Settings 页）是根据工作流文件绘制的示意图，
画面上标着 `illustration`，里面每一行日志都是真的。README 里没有、但有助于理解的检查（`git ls-remote`、`git remote -v`、`docker images`、
`docker ps`、跳过的 Flake8 本来会说什么、演示提交的那次运行）在画面上标着 `extra`。

本讲不需要云资源，也不需要任何密钥；公开仓库的 Actions 分钟数免费。Slack 的 webhook 地址只用占位符，`SLACK_WEBHOOK_URL` 只写名字，
从不写值。课件和 README、README 和实际运行不一致的地方（README 的截图是早先版本代码的全绿；在 clone 里 `git commit` 显示
nothing to commit；README 说有 Buildx 缓存却没有保存缓存；覆盖率报告因为目录权限写不出来；`def broken()` 不会被 pytest 收集；分支保护的
选择列表按 job 的名字而不是 ID 列出），以录到的为准，视频会温和地指出来。

## 文件

| 文件 | 内容 |
| --- | --- |
| `output/ac215-l21-cicd-github-actions.zh-en.mp4` | 英文旁白 + 烧录在画面下方的中英双语字幕（中文在上，英文原句在下）：最方便直接看的版本，也是上传 Bilibili 的版本 |
| `output/ac215-l21-cicd-github-actions.mp4` | 干净的英文版（无烧录字幕），可以在播放器里加载下面的字幕文件 |
| `output/ac215-l21-cicd-github-actions_part1.*`、`_part2.*` | 上下两部分（S01–S07：读懂、推送、看它运行；S08–S16：逐个 job 拆开看），每部分有自己的视频和字幕文件 |
| `output/ac215-l21-cicd-github-actions.zh.srt` | 中文字幕（按英文旁白的时间轴） |
| `output/ac215-l21-cicd-github-actions.zh-en.srt` / `.zh-en.ass` | 中英双语字幕 |
| `output/ac215-l21-cicd-github-actions.srt` | 英文字幕 |
| `output/chapters.txt`、`chapters_part1.txt`、`chapters_part2.txt` | 章节时间轴（章节名的中文版在 `meta.yaml`） |
| `output/transcript.md` | 按章节排列的旁白全文 |
| `i18n/zh/narration/g1.yaml`、`g2.yaml` | 逐句对齐英文的中文译文：`g1` 是第一部分（S01–S07），`g2` 是第二部分（S08–S16）；`en_display:` 是英文字幕行的显示形式 |
| `i18n/zh/GLOSSARY.md`、`glossary.yaml` | 术语表：哪些词保留英文、哪些用中文，以及字幕的标点、空格和换行规则（两份内容相同） |
| `i18n/zh/meta.yaml` | 中文标题、两部分的标题、章节名和简介 |

视频和字幕要等渲染完成后才会出现在 `output/` 里。视频文件（`.mp4`）不放进 Git：剧集合并后作为 GitHub Release 的附件发布，
下载链接见 [`catalog/videos.json`](../../../../catalog/videos.json) 和 [`docs/VIDEOS.md`](../../../../docs/VIDEOS.md)；
字幕、章节和旁白全文留在 `output/` 里。练习题在 [`../../exercises.md`](../../exercises.md)（英文）；每条命令和中文速览在学习指南
[MLOps_Learning · guides/L21-cicd-github-actions.md](https://github.com/JunyiZhou-Conny/MLOps_Learning/blob/main/guides/L21-cicd-github-actions.md)。

## 怎么生成

```bash
python -m explainer.i18n check videos/ac215-l21-cicd-github-actions --lang zh               # 中文译文和英文是否逐句对齐、能否通过显示检查
python -m explainer.build videos/ac215-l21-cicd-github-actions --render-only --jobs 3       # 渲染各场景（英文旁白）
python -m explainer.build videos/ac215-l21-cicd-github-actions --no-render --crf 27 --burn  # 拼接 + 中文 / 双语字幕 + 烧录版
python -m explainer.build videos/ac215-l21-cicd-github-actions --subs-only                  # 只重写字幕（改了译文之后）
```

`script.md` 里的每一行 SAY 在 `narration/*.yaml` 里对应一个条目（140 段：第一部分 57 段，第二部分 83 段），`en` 和 SAY 逐字相同；
`zh` 按 `explainer.voice.split_sentences` 切出的英文句子一句对一句（共 371 句：162 + 209），不合并、不拆分。字幕按英文旁白录下的时间显示：
双语字幕带在中文句子切开的地方，把英文句子也切在对应的位置，所以中文尽量保持英文的语序（条件、目的和时间从句留在英文放的位置）。
SAY 为了让语音读对，把实物念成了单词（C I dot yaml、dot github, workflows、runs on, ubuntu latest、git commit, dash m、no verify、
utils dot py、if always、Slack webhook URL、test broken……）；这些条目（50 段：10 + 40）在 `en_display:` 里给出屏幕上的写法
（`ci.yml`、`.github/workflows`、`runs-on: ubuntu-latest`、`git commit -m "Add CI pipeline"`、`--no-verify`、`utils.py`、`if: always()`、
`SLACK_WEBHOOK_URL`、`test_broken`……），双语字幕的英文行显示的就是它。

## 译文风格

按中国 MLOps 助教带实验课的说法：你要输入、要在屏幕上对照的东西（命令、参数、文件名和路径、分支名、image 名、YAML 键、`ci.yml` 里的
job 名和步骤名、commit 信息、GitHub 控制台的按钮和页面名、README 的小节名）一字不改，比如 `git remote set-url origin`、
`pre-commit run --all-files`、`git commit --no-verify -m "quick fix"`、`feature/test-protection`、`runs-on: ubuntu-latest`、
`continue-on-error: false`、Lint and Format Check、Test Summary、Load Docker image、Check test results、Secrets and variables、
Require status checks to pass、Push to GitHub。旁白引用的日志和报错按屏幕原文照抄（job Lint and Format Check failed、All tests passed、
nothing to commit, working tree clean、Everything up-to-date、permission denied、pull access denied、would reformat utils.py、
1 failed, 11 passed），观众要在日志里找它们。

实验课上本来就说英文的词保留英文：前几讲的 repo、clone、commit、push、fork、origin、container、image、tag、port、localhost、pipeline、
hook、lint、linter、shell、root、bug、pin，加上这一讲的 job、runner、artifact、action、run、secret、webhook、PR；其余用中文标准术语
（GitHub 中文文档和国内 CI 实践的译名）：工作流、事件、触发条件、步骤、依赖、并行、条件执行、退出码、持续集成、持续部署、静态分析、
编码规范、分支保护、状态检查、暂存、工作区、覆盖率。视频里的比喻一个比喻一个词：门禁（读退出码的步骤，以及课上能拒绝的那道门，
和第 9 讲一致）、铃（Actions 在 push 之后才报告：“是铃，不是门禁”）、行李箱（装镜像的 tar）、旁路（`continue-on-error` 把失败引到
一边）、证人（`act`，第二个证人）、循环（课件第 21 页的 CI 循环）、开头那个谜题（视频的 hook：run 是红的，汇总却全绿；这里不说 hook，
免得和 Git hook 混淆）。

字幕检查不允许中文行里出现下划线名字、等号、尖括号、美元符号和括号，所以几样实物在中文行里按旁白的说法写，英文行照常显示原样：
`$GITHUB_OUTPUT` → GitHub output，`SLACK_WEBHOOK_URL` → Slack webhook URL，`if: always()` → if always，`cheese-app-api:<commit ID>` →
cheese-app-api，冒号，再加 commit ID，`enabled=true` → enabled 为 true，`test_broken` → test 下划线 broken，`def broken(): assert False` →
def broken，assert False，`***` → 三个星号，`main -> main` → main 到 main。标题、章节名和简介用书面语体（仓库、推送、钩子、流水线、
机密（secret）、分支保护）。双语字幕的英文原句就在中文下方，所以中文行不加英文括注。完整规则见 [GLOSSARY.md](GLOSSARY.md)。

## 术语对照

| English | 字幕里的说法 | 书面写法 / 常见的其他译法 |
| --- | --- | --- |
| workflow / event / trigger | 工作流 / 事件 / 触发条件 | 同左 |
| job / step / runner | job / 步骤 / runner | 作业、任务 / 同左 / 运行器 |
| artifact | artifact | 工件、构件、产物 |
| needs (the job graph) / in parallel | needs / 并排、并行 | 依赖 / 并行 |
| exit code / gate | 退出码 / 门禁 | 同左 |
| continue-on-error / if: always() | continue-on-error / if always | 出错继续 / 总是运行 |
| conditional execution | 条件执行 | 同左 |
| repository secret | 仓库 secret | 仓库机密、密钥 |
| webhook / incoming webhook | webhook / incoming webhook | 网络钩子 / 传入 webhook |
| pull request | PR | 拉取请求、合并请求 |
| branch protection / required status checks | 分支保护 / 必需的状态检查 | 分支保护规则 / 同左 |
| pre-receive / update / post-receive hook | 照说 | 服务器端钩子 |
| the local conundrum | 本地难题 | 同左 |
| continuous integration / deployment | 持续集成 / 持续部署（说 CI、CD 时照说） | 持续集成（CI） / 持续部署（CD） |
| non-determinism | 不确定性 | 非确定性 |
