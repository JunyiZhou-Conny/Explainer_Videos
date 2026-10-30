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
| streaming (SSE, NDJSON) | 流式 | — | E2 |
