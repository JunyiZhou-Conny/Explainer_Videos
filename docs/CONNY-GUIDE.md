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
- **撞上 usage limit / 中途换模型**：这是设计内场景。代理在会话可能结束前必须推送分支并在
  issue 留 DONE / NEXT / WARN 交接注（AGENTS.md 交接协议）。你只需把同一个 issue 链接 +
  kickoff prompt 发给下一个代理（哪家模型都行），它会从交接注的 NEXT 继续，而不是重做。
  Claude 和 GPT 之间就是这样"通信"的——信箱是 issue 线程，不是聊天框。
- **弱模型的现实预期**：管道部分（渲染、字幕、配乐、校验）它们能跑通；短板在脚本创意、
  manim 排版和看帧 QA。所以**样片关卡对弱模型尤其重要**——20 秒就能看出能不能用，
  不行就换强模型接手制作，brief 和素材照用。
- **同题竞赛**：想对比两个模型，开两个 issue（slug 加后缀，如 `-a`/`-b`），各自一条分支
  互不干扰，看完两个样片再决定谁继续。

## 4. 你的三个审核时刻

| 时刻 | 你做什么 | 在哪 |
| --- | --- | --- |
| Brief（可选但推荐） | 看学习目标和场景结构对不对 | PR 里的 `BRIEF.md` |
| 样片（20–30 秒） | 看风格、听发音，口语回一句 | PR 评论 |
| 全片 | 戴耳机完整看一遍，留签字 | PR 评论，如"听过了，可以合并" |

签字会被原文引进 `REVIEW.md`——这是合并前唯一的硬性人工闸门，发布工具会检查这条记录
（认 "human review" 或 "listening sign-off" 字样，代理会替你写对格式）。

## 5. 合并之后（基本不用你管）

合并 → `episode-release.yml` 自动渲染终版、打 `episode/<slug>-vN` 标签、传资产和 PUBLISH
清单 → issue 切到 `state:publishing` → Mac 上的 `tools/publish_worker.py` 上传 B 站、
回帖 BV 号、关 issue。唯一的本地依赖是 Mac 上 biliup 的登录态（每周 `biliup renew` 一次）。

收尾小事：合并后 PR 页面点一下 Delete branch；目录（`catalog/videos.json` +
`docs/VIDEOS.md`）由收尾的代理补一条小 PR。

## 6. 出问题了看哪

- **代理没接单**：看 issue 有没有代理的评论；没有就按第 3 节手动指派。
- **卡住**：`state:` 标签 + PR 最后一条评论就是现场；`blocked:question` 意味着在等你答复。
- **CI 红**：不用管，接单代理的职责是把它修绿；红着超过一天可在 PR 里 @ 它或换人。
- **标签和实际不符**：以文件为准（AGENTS.md 的规矩），顺手把标签改对。

就这些。写好问题，审两次片，签一次字——其余交给流水线。
