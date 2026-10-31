# Conny 的操作手册：怎么开项目、喂上下文、换模型跑

> 这份手册写给监工（你）。代理的规则在 [AGENTS.md](../AGENTS.md)，这里只讲你要做的事。
> 原则一句话：**一切从 issue 开始，一切以仓库里的文件为准。** 没落在 issue/PR/文件里的事等于没发生。

## 1. 开一集新视频（标准流程）

1. 打开 **Issues → New issue → Episode request** 模板。
2. 把三个必填项写实：
   - **The question to understand**：一个明确的问题，不是一个领域。
     好："为什么 git 分支几乎零成本？" 差："讲讲 git"。
   - **Audience**：观众已经会什么、还不会什么、带着什么误解。这一栏决定视频的难度和钩子。
   - **Topic sources**：证据从哪来（见下一节）。代理只能教素材支撑得住的内容。
3. 风格选 ready 的（swiss / 3b1b），时长不填就是默认 5 分钟。
4. 提交即可。模板尾部的 `@claude` 会唤醒代理自动接单（GitHub App 已安装）；
   如果想用别的代理/模型跑，见第 3 节。

之后代理会：开 `episode/<slug>` 分支和草稿 PR → 写 BRIEF/SOURCES → 发 20–30 秒样片等你审
→ 全片 → 等你签字。`state:` 标签随时告诉你走到哪了；标签和文件冲突时以文件为准。

## 2. 怎么喂上下文（外部仓库、分支、notebook）

全部写进 issue 的 **Topic sources** 栏，格式随意但要可定位：

```
- 仓库: JunyiZhou-Conny/speciesOT, 分支 baseline
- 重点文件: src/speciesot/speciesot_core.py (214-225 行), src/speciesot/Tests/config.yaml
- 实验 notebook: src/speciesot/Tests/e24_replica.ipynb
- 论文: scGen (Lotfollahi 2019), 只用到 §2 的模型结构
```

要点：

- **钉到具体位置**（文件、行号、分支、页码）。给弱模型的锚点越具体，产出越不跑偏。
- **访问权要跟上**：云端 Claude 会话需要把外部仓库挂进会话（对话里说一句
  "attach JunyiZhou-Conny/speciesOT" 即可）；Cursor/本地跑则把两个仓库放进同一个
  workspace。issue 里写明"需要访问 speciesOT"让接单的代理自己去要。
- 证据规则不变：屏幕上出现的代码/数据必须真实，来源钉进该集的 `SOURCES.md`。

## 3. 用不同的模型/代理跑

流水线对模型是中立的：闸门（CI、像素检查、样片评审、签字）托住下限，谁来跑规则都一样。

- **换代理接单**：开 issue 时删掉模板尾部的 `@claude` 段（或无视它），把 issue 链接发给你想用的
  代理（Cursor、本地 Claude、GPT……），指令直接用 **`docs/BOOTSTRAP.md` 里的 kickoff prompt**
  （复制即可）——它保证任何模型拿到的上下文完全一致：同样的阅读顺序、同一个参考剧集、
  同一套交接规则。
- **认领要落痕**：代理的第一个动作是在 issue 里评论认领（模型 + 平台 + 分支），避免撞车。
  一集只允许一条分支、一个 PR。
- **撞上 usage limit**：等额度重置，回到**同一个会话**说一句"继续"。同一个会话保留着它的
  工作记忆（试过什么、为什么、你在聊天里给的口味反馈），这是质量最稳的做法。
- **万不得已才换模型**：代理在每个阶段边界（brief、脚本、样片、场景、全片）都会推送分支并在
  issue 留 `CHECKPOINT` 评论（DONE / NEXT / WARN），所以任何时候被切断，损失不超过当前阶段。
  真要换人，把同一个 issue 链接 + kickoff prompt 发给下一个代理，它从最近检查点的 NEXT 继续。
  但它拿不到前一个会话的工作记忆，渲染缓存也要重做，质量会掉一截。
  Claude 和 GPT 之间就是这样"通信"的——信箱是 issue 线程，不是聊天框。
- **制作进度页告诉你每集走到哪**（网站首页）：每集一张卡片，进度条按阶段（素材 → 脚本 → 场景 →
  审查 → 修改 → 渲染 → 拼接 → 合并 → 上传 → 上线）显示大约完成多少；最上面"需要你处理"只列
  真正等你的事（回答问题、合并 PR、在 Mac 上跑上传），课程地图一眼看全 AC215 的 23 讲。
  一个会话的分支一天多没推送也没检查点，卡片会标"一天多没动静"——通常是撞了用量限制、在聊天里
  等你回复，或你让它暂停了，去那个会话看一眼。数据在 issue 有动静后一两分钟内自动刷新。
- **弱模型的现实预期**：管道部分（渲染、字幕、配乐、校验）它们能跑通；短板在脚本创意、
  manim 排版和看帧 QA。所以**样片关卡对弱模型尤其重要**——20 秒就能看出能不能用，
  不行就换强模型接手制作，brief 和素材照用。
- **同题竞赛**：想对比两个模型，开两个 issue（slug 加后缀，如 `-a`/`-b`），各自一条分支
  互不干扰，看完两个样片再决定谁继续。

## 4. 你的三个审核时刻（2026-10-22 起默认可选）

| 时刻 | 你做什么 | 在哪 |
| --- | --- | --- |
| Brief（可选但推荐） | 看学习目标和场景结构对不对 | PR 里的 `BRIEF.md` |
| 样片（20–30 秒） | 看风格、听发音，口语回一句 | PR 评论 |
| 全片 | 戴耳机完整看一遍，留签字 | PR 评论，如"听过了，可以合并" |

你说过不审片、让 Bugbot 和 QA 把关，所以这三个时刻现在都是**可选的**：代理照样把样片贴在
PR 上留档，但不停下来等你；`REVIEW.md` 里引用你的豁免原话代替听审签字（AGENTS.md 里有原文）。
发布工具仍会检查这条记录（认 "human review" 或 "listening sign-off" 字样，代理会写对格式）。
哪天你想亲自听某一集，在 PR 里留一句话，你的原话就会替代豁免。

## 5. 合并之后（基本不用你管）

合并 → `release-on-merge.yml` 找出这个 PR 新加的每一集（还没有 `episode/<slug>-v*` 发布、
B 站登记表里也没有），自动启动它的发布流程（`episode.json` 用 `episode-release.yml`，`video.yaml`
用 `legacy-release.yml`）：渲染终版、打 `episode/<slug>-vN` 标签、传资产和 PUBLISH 清单 →
issue 切到 `state:publishing` → Mac 上的 `tools/publish_worker.py` 上传 B 站、回帖 BV 号、
关 issue。已经发布过的集要重发（出 v2）仍在 Actions 里手动运行发布流程，因为 v2 会在 B 站
再传一次。

**Mac 一次性设置**：在仓库目录运行 `bash setup/macos/install-publish-worker.sh`。它先登录
GitHub 和 B 站（扫码），再装两个定时任务：每 15 分钟跑一次上传脚本（每次最多传一集），
每周一续一次 B 站登录。之后不用管；日志在 `~/Library/Logs/explainer-publish.log`，
卸载加 `--uninstall`。前提是装好 `gh`（`brew install gh`）和 biliup（`npm install -g @biliup/cli`）。

收尾小事：合并后 PR 页面点一下 Delete branch；目录（`catalog/videos.json` +
`docs/VIDEOS.md`）由收尾的代理补一条小 PR。

## 6. 项目周记：每周把自己的 PR 做成视频

讲 InternationalHealthportal 这周做了什么的系列（规则见 [PORTAL_SERIES.md](PORTAL_SERIES.md)，
计划见 `videos/portal-series/README.md`）。每集 10 分钟以内，只讲概念，不读代码。每周一次，
把下面这段发给一个新的 Claude 会话（会话里要挂上两个仓库：Explainer_Videos 和
InternationalHealthportal）：

> 用 portal-video skill。做这周（<起始日>–<结束日>）的项目周记：先跑 PR 周报，按我这周看到、
> 想问的东西规划一批视频（我的问题：<随手写几条>），每集开一个 issue，然后从第一集开始做。

- **你的问题最值钱。** 看界面时想到的「这是什么、怎么做到的、还能怎么做」，直接写进去；代理会把每个
  问题对应到一集，并在脚本里用 PR、决策记录和代码核对过的事实回答。
- **周报**在 `videos/portal-series/weeks/`：这周你名下的每个 PR、提交时间线（波士顿时间）、动了哪些
  目录、改了哪些决策。不想看视频时它本身就是一份周报。
- **公开发布**：这个系列和其他视频一样公开、上传 B 站（2026-10-30 定的）。视频里队友只称角色，
  不出现 key、账号和真实用户数据。

## 7. 出问题了看哪

- **代理没接单**：看 issue 有没有代理的评论；没有就按第 3 节手动指派。
- **卡住**：`state:` 标签 + PR 最后一条评论就是现场；`blocked:question` 意味着在等你答复。
- **CI 红**：不用管，接单代理的职责是把它修绿；红着超过一天可在 PR 里 @ 它或换人。
- **标签和实际不符**：以文件为准（AGENTS.md 的规矩），顺手把标签改对。

就这些。写好问题，审两次片，签一次字——其余交给流水线。
