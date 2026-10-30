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
