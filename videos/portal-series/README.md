# 项目周记: batch plan

Series rules: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md). Agent how-to:
`.claude/skills/portal-video/SKILL.md`. Weekly digests: [`weeks/`](weeks/). Shared terms:
[GLOSSARY.md](GLOSSARY.md).

## Coverage

What the episodes have already explained. The weekly run (`.claude/skills/portal-video/SKILL.md`,
§W) starts its digest at *Covered through* and treats as new only the PRs below that are missing,
or the commits after the one recorded. Questions live in the standing issue
[#72](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/72). Each run copies this
table into its `WEEKLY` comment there. That copy is current even while the week's batch PR
waits to merge, so a run trusts the newest comment over this file.

**Covered through:** 2026-10-30 (Boston).

| Portal PR | Commit explained | Episodes |
|---|---|---|
| #36 triage MVP | `17228bd` | E1, E2, E4 |
| #41 chat page after the Claude app | `b7ab98e` | E1, E2, E3, E4 |
| #42 verification tools (`npm run verify`, verify-app) | `fe19a23` | E5 |
| #43 backend stack (decision 0006) | `f163e90` | E6 |
| #2, #4, #6, #8, #9, #35, #37 team scaffolding and notes | merged | E4, in passing |

## Week 44 (2026-10-26 → 11-01): the triage chat

Digest: [weeks/2026-w44.md](weeks/2026-w44.md). PR numbers below are InternationalHealthportal's. Nine of the owner's PRs; two carry almost all of
the week's work and are still open (as of 2026-10-30):

- **PR #36**, triage MVP: the knowledge base (15 official pages → 97 fact cards, 7 conflicts), the
  rules engine and a six-arm evaluation (built, shelved before it ran), the 10-27 21:21 turn to "the model judges,
  the output check is the only safety layer" (decision 0004, proposed), the plain chat box, and forty
  more commits, mostly hardening the checker. 60 commits over 36 hours.
- **PR #41**, stacked on #36: the chat page rebuilt after the Claude app (decision 0006, proposed):
  thinking row and receipt, composer and model menu, progress streaming over NDJSON with an early
  911 notice, reveal animation, retry and stop, demo replays, an offline fake model; five review
  angles, Bugbot and Codex rounds. 28 commits plus 18 merges of #36.

The rest (#2, #4, #6, #8, #9, #35, #37) are team scaffolding, meeting notes and the rename to 「项目」;
E4 mentions them in passing.

**The owner's questions** (chat, 2026-10-30), which this batch answers:

> 1. first of all everything is wrapped around the openai api, we sent out a request or a query, and
> they returned something back. However it is distinctly different from the most pristine version of
> an api because there are thinking parts that show thinking for 3 seconds, and I can click and
> expand it, and there are also parts specifically written for parents which are interesting. I am
> not sure how that is accomplished and what else can we do with this particular feature?

> 正在思考啊……这些都是什么功能……我相信可能在 2–3 年前其实并不存在这个什么所谓的思考链，也不存在把这些内容展示给观众……
> 包括这个 UI 的设计……我能在这个之上再去创新什么……主流的对这种 chatbot UI 的一些设计……
> 我们在哪些地方进行的模仿，我们是怎么达成的，还有什么可以做的……一步一步我们的 Claude 花这么多时间去做，他都干了些什么，他解决什么问题。

Style: E1 is Swiss (`episode.json` route); from E2 on, every episode uses the 3Blue1Brown house style on
the `video.yaml` route (owner, 2026-10-30: 「以后用 3BLUE1BROWN STYLE PLEASE」; docs/PORTAL_SERIES.md).

| # | Episode | Question | PRs | Status |
|---|---|---|---|---|
| E1 | [`portal-e1-after-send`](../portal-e1-after-send/) · 不就是调一下 API 吗？ | If it is "just the OpenAI API", where do the parent summary and the receipt come from? | #36 (+ #41 page) | [#58](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/58) · full cut |
| E2 | [`portal-e2-thinking`](../portal-e2-thinking/) · 「思考了 3 秒」到底是什么 | What is the model doing during "thinking", and why do we show a receipt instead of its thoughts? | #41, #36 | [#59](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/59) · full cut (3b1b) |
| E3 | [`portal-e3-copying-claude`](../portal-e3-copying-claude/) · 照着 Claude 抄 | What did we copy from the Claude app, what not, what is ours, and what could we invent? | #41 | [#60](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/60) · full cut (3b1b) |
| E4 | [`portal-e4-build-log`](../portal-e4-build-log/) · 两天、一百多个提交 | What did the agents actually do for two days, what did it cost, and who decided? | #36, #41, the week | [#61](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/61) · full cut (3b1b, 8:55) |
| E5 | [`portal-e5-verify`](../portal-e5-verify/) · agent 怎么证明自己改对了 | Before any person looks, how can an agent prove a change is right? | #42 (draft) | [#66](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/66) · full cut (3b1b, 6:18) |
| E6 | [`portal-e6-backend`](../portal-e6-backend/) · 后端怎么选 | How was the backend chosen, what lost and why, and what does the first data model protect? | #43 (draft) | [#67](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/67) · full cut (3b1b, 7:28) |

### E1 · 不就是调一下 API 吗？ (Isn't it just an API call?)

The four jobs of the harness between "send" and the answer: build the request (15 pages + 89 checked
facts + rules + form first, so it is cached; then the changing context); hand the model a form
(structured outputs, strict JSON schema, 13 boxes; `parentSummaryZh` is why parents get a summary);
check every line (20 lint rules + three around them, one rewrite, a fixed fallback, an emergency
is never taken back); lay the form out as the page and the receipt (which row comes from where; sources is the
model's word alone). The path through PR #36, ChatGPT/Claude vs. ours, and "a new feature is a new
box". Names: harness, system prompt / instructions, prompt caching, structured outputs, JSON schema,
guardrail (lint), fallback.

### E2 · 「思考了 3 秒」到底是什么 (What is "thought for 3 seconds"?)

- **Hook:** the live line 「正在思考 · 11 秒」 and the folded 「思考了 22 秒 ›」 with 过程 「思考 13.5 秒 →
  写 8.7 秒（1717 字）→ 检查通过」 (owner's screenshots).
- **Names:** reasoning models; reasoning tokens (hidden, billed as output); reasoning effort
  (low / medium / high = 思考强度); chain of thought vs. summarized thinking; token streaming (SSE)
  vs. progress streaming (NDJSON); prompt-cache miss when switching model.
- **Mechanism:** the stopwatch phases (thinking = until the first character of the reply arrives;
  writing; checking; rewriting) from `streamProgress.ts`, `server.ts` and `stages.ts`; the server
  reads the model's stream, counts characters per field and forwards only progress, never text
  (decision 0006 addendum, "流的是进度，不是模型的原文"); emergency fields are first in the form, so a
  fixed 911 notice can appear after about 3.5 s instead of about 21 s; the checked answer is then
  revealed paragraph by paragraph over about 2.5 s (a cosmetic typing effect); "stop" really aborts
  the model call.
- **Copy vs. own:** Claude's app streams the answer as it is written and can show a summary of its
  thinking (cite the public docs at production time); we stream progress only and show a receipt,
  because unchecked text may contain a diagnosis or a dose that cannot be taken back.
- **Design space and open decisions:** a developer-only draft view (proposed, not built), reasoning
  summaries, showing tool steps, budget reservation before calls (Codex P3, open).
- **Ponder:** why can't we stream the words and delete them if the check fails? Why does the
  emergency box come first in the form?

### E3 · 照着 Claude 抄 (Copying Claude's chat UI)

- **Hook:** the triage page next to the Claude app layout, element by element.
- **Names:** empty state, suggestion chips, composer, model picker, send/stop button, message
  bubble, regenerate, scroll-to-latest, dark mode, disclaimer line, accessible headings.
- **Mechanism / decision:** decision 0006: one reference per screen, copied one-to-one, no mixing;
  colours and serif body copied for this page only; `docs/design/README.md` lists what was copied,
  what was not (logo, raw reasoning, token streaming, sidebar and history, attachments) and what
  was added for safety and for parents (red do-this-now block, parent wording for 911, labels
  「模拟」, copy-with-label, 400 % zoom, 24 px targets, screen-reader headings).
- **The path:** PR #41's commits: rebuild in 17 minutes, then visual reviews, streaming, state bugs,
  layout at zoom; why "stop" and "send" being one button caused a bug.
- **Design space:** what mainstream chat UIs do that we don't (history, attachments, voice,
  artifacts, memory) and what this product could do that they can't (a two-audience answer for
  student and parent, a shareable summary card, booking handoff).
- **Ponder:** why copy one product exactly instead of picking the best parts of several?

### E4 · 两天、一百多个提交 (What the agents did for two days)

- **Hook:** the digest's commit ticks for #36 and #41 on one Boston-time axis.
- **Names:** issue → branch → PR; stacked PRs; decision record; handoff note; review bots (Bugbot,
  Codex) re-reviewing every push; adversarial probing; regression corpus; unattended run; usage
  limits.
- **Story:** knowledge base reviewed by four isolated agents (75 problems found); the rules engine
  and why it was set aside; the checker's whack-a-mole and the switch to probing about 3,000
  phrasings before pushing (1,060 kept as `lint.probes.json`); two five-hour usage limits and two
  container restarts in one night; the 99 % stop rule; the twelve decisions waiting for the owner.
- **Ponder:** the team dropped word rules for symptoms but kept them for sentences; what would
  make the checker less of a whack-a-mole?

### E5 · agent 怎么证明自己改对了 (How an agent proves its change is right)

Added 2026-10-31 at the owner's request (「开始做吧」), from two PRs opened after the batch was planned.

- **Hook:** a real bug no person had found: an expired referral still links to a new appointment.
  An agent found it by trying every order of actions.
- **Names:** reducer; invariant; exhaustive (model) checking; counterexample; deliberate breakage
  (mutation testing); driving the real app by accessible role and name; evidence.
- **Story:** PR #42's two tools:
  - `npm run verify` walks about 14,000 states in about a second, and catches each of five
    deliberate breakages with a counterexample of two steps or fewer.
  - `verify-app` clicks through the running page like a parent and keeps screenshots and state
    as evidence.

  The tools came from the pstack verification skills, and the finding waits for a person's decision.
- **Ponder:** a test checks the cases someone thought of; what checks the ones nobody thought of?

### E6 · 后端怎么选 (How the backend stack was chosen)

- **Hook:** the prototype has no backend, database or accounts. Accounts, insurance and family
  links all need one place to live.
- **Names:** backend; framework; database and migrations; one-time-code login; container; schema;
  foreign key and cascade; decision record.
- **Story:** PR #43's proposal (decision 「0006」, 提议):
  - TypeScript + Hono + Zod;
  - Postgres with Drizzle;
  - Better Auth with email codes only;
  - Docker Compose, with WSL on Windows.

  Each choice comes with the options it rejected and why. The first data model: roles fixed after
  choosing, a family link only the student can start, insurance cards read-only for parents and
  with no images. It went through a four-angle review (31 comments, 14 kept). Open questions:
  access from China, the email provider, parent edits, retention. The decision number clashes
  with the triage-chat 0006 on PR #41.
- **Ponder:** why decide the database before writing any code?

