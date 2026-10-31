# 项目周记 glossary

Terms named in the series, with the Chinese used in the captions and the episode that first
explains them. Later episodes reuse these words; add a row when an episode names a new term.

| Term | Captions (zh) | Means, in this product | First in |
|---|---|---|---|
| harness | harness | The code around a model call: builds the request, sets the reply's form, checks it, renders it | E1 |
| instructions / system prompt | instructions，系统提示词 | The fixed top of every request: BU pages, checked facts, rules, the form's description | E1 |
| token | token | The unit models read and bill by; the BU booklet is about 25,000 | E1 |
| prompt caching | prompt caching，提示缓存 | Reusing an unchanged request prefix; cached input costs a tenth (Luna) or a twentieth (Terra) | E1 |
| structured outputs | structured outputs，结构化输出 | A JSON schema the reply must fit; strict mode allows no missing or extra field | E1 |
| JSON schema / output contract | 输出合同 | The 13-box form (`OUTPUT_SCHEMA`) | E1 |
| fact card | 事实卡 | A phone number, price or opening hour with its source sentence and expiry date; the model is sent only the checked fact | E1 |
| lint (output guardrail) | lint，输出检查 | Our checker: 20 rules over every line the reader sees | E1 |
| rewrite | 重写 | One retry with the checker's findings sent back to the model | E1 |
| fallback | 兜底 | Fixed text we wrote, shown when the model's reply cannot pass | E1 |
| an emergency is never taken back | 紧急不收回 | Once any version says emergency, the rewrite and the fallback must stay emergency | E1 |
| receipt (thinking panel) | 收据（思考过程） | The folded rows: process, sources, check, judgment, model | E1 |
| reasoning model, reasoning effort | 推理模型，思考强度 | A model that reasons in hidden, billed steps before writing; effort (低/中/高) sets how much | E1 (named), E2 |
| chain of thought | 思维链，chain of thought | Asking a model to write out its steps first (2022); reasoning models now do it themselves | E2 |
| reasoning tokens | 推理 token | The tokens a reasoning model writes for itself: not returned, still in the context, billed as output; counted in the usage report | E2 |
| reasoning summary | 推理摘要 | A model-written summary of hidden reasoning (OpenAI's `summary` parameter, Claude's app); we do not show one | E2 |
| stopwatch: thinking / writing | 思考 / 写 | Thinking = until the first character of the answer arrives; writing = from there until the model finishes; then checking | E2 |
| token streaming (SSE) | 流式输出，server-sent events | Words sent to the screen as the model writes them; how most chat apps work, and how OpenAI sends to our server | E2 |
| progress streaming (NDJSON) | 只流进度 | What our server sends the page: one JSON line per update (stage, box, character count, emergency flag), never the words | E2 |
| early 911 warning | 提前的 911 提醒 | Fixed text we wrote, shown as soon as the first boxes say emergency, before the checked answer | E2 |
| replay (reveal) | 回放 | The checked answer played out in at most 2.5 s; emergency answers appear at once | E2 |
| empty state | 空状态，也就是首屏 | The page before the first message: greeting, composer, suggestions | E3 |
| suggestion chips | 建议 | Ready-made questions under the composer; ours start demo replays | E3 |
| composer | 输入框 | The input box; ours holds 谁在问 · 保险 · 在哪里, the model menu and the send key | E3 |
| send / stop key | 发送键 / 停止键 | One button slot: send turns into stop while waiting (the source of two bugs in PR #41) | E3 |
| action row | 操作按钮 | Under an answer: 复制, 复制给家长 (students), 重新回答 (latest live answer) | E3 |
| one reference per screen | 每个界面只照抄一个参考 | Decision 0006: copy one mature product exactly, no mixing; the chat page copies Claude's app | E3 |
| Jakob's law | 雅各布定律 | Users spend most of their time on other sites, so they prefer yours to work the same way (NN/g) | E3 |
| draft PR · ready for review | 草稿 PR · 标成可以 review | A PR opened after the first commit stays a draft; the workflow says a person marks it ready, which also starts Codex's reviews | E4 |
| review bot | review bot | Bugbot (Cursor, every push) and Codex (OpenAI, once a PR is ready): comment, never change code | E4 |
| handoff note | 交接 | A comment an agent leaves on its PR when it stops: done, not done, next (waiting for Junyi), traps | E4 |
| proposed / adopted | 提议 / 已采纳 | A decision record's status; agents draft as 提议, only a person sets 已采纳 | E4 |
| stacked PR | 叠在上面的 PR | A PR based on another PR's branch (#41 on #36), merging it in to stay current | E4 |
| miss / false alarm | 漏判 / 误报 | The checker letting a bad line through / flagging a harmless one | E4 |
| adversarial probing | 对抗探测 | Agents writing thousands of risky and harmless phrasings to attack the checker before pushing | E4 |
| regression corpus | 探测说法（回归测试） | `lint.probes.json`: 1,060 phrasings the checker once got wrong, replayed by the unit tests | E4 |
| reproduce first | 先复现再修 | A fix agent first shows the bug happening, then fixes it (「逐条先复现再修」) | E4 |
| unattended run · usage limit | 无人值守 · 用量上限 | Agents working with no person watching; a 5-hour usage cap that pauses the session | E4 |
| stop rule | 收尾的约定 | The owner's 「做到 99% 就停……最晚周四晚上 7 点（按北京时间算）收尾」 | E4 |
| reducer | reducer | The one function every change to the app's data goes through: old state + one action → next state | E5 |
| exhaustive check | 穷举检查 | Try every order of a few actions in a small world, check rules in every state; `npm run verify` | E5 |
| shortest story (trace) | 最短复现 | The fewest steps that break a rule; a layer-by-layer search finds it first | E5 |
| known finding | 已知发现（未修） | A broken rule the check records instead of hiding; the check fails if it ever disappears, so the note gets deleted | E5 |
| deliberate breakage (mutation) | 故意改坏（变异测试） | Break the code on purpose to see the check fail; a check never seen to fail proves nothing | E5 |
| role and accessible name | 角色和无障碍名称 | How verify-app finds a control: what it is (button, link) and the label a screen reader announces | E5 |
| evidence | 证据 | What an app-driving run must keep: screenshot, saved state, no browser errors, project rules checked | E5 |
| backend | 后端 | The server, database and login behind the page; the project has none yet | E6 |
| container (Docker Compose) | 容器 | A sealed box that runs the same on Mac and Windows; `docker compose up` starts db · api · web | E6 |
| one-time code | 邮箱验证码 | Login without passwords: a 6-digit code by email, 5 minutes, 3 tries, stored only as a hash | E6 |
| family link | 家庭关联 | The student ↔ parent link; only the student starts it with a one-use invite code; parents read only | E6 |
| migration | 迁移文件 | A numbered file that changes the tables, so every copy of the database ends up the same | E6 |
| 403 | 拒绝访问 | The server's "refused"; the record's test: after unlinking, the parent's next request gets it | E6 |
