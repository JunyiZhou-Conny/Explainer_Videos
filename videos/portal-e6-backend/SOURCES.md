# Sources: 项目周记 E6 · How do you choose a backend?

Everything on screen or in the narration comes from one of the sources below. The portal repository
is private; paths are given so a reader with access can check them. Read 2026-10-31.

## The record (JunyiZhou-Conny/InternationalHealthportal)

- **PR #43**, draft, open: decision 0006, the backend stack. Branch `claude/wonderful-meitner-r752lh`, read at `f163e90`.
- **The record.** `D` below is `docs/decisions/0006-backend-stack.md` at `f163e90` (223 lines, status 「提议」, dated 2026-10-30). Its title is 「0006：后端用 TypeScript（Hono + Postgres），账号用邮箱验证码，Docker Compose 容器化」.
- **Commits** (Boston time, EDT; Beijing is 12 hours ahead), Fri 2026-10-30:
  - `57cbffa`, 17:24:18: the first draft, 172 lines; the PR opened 17:24:32;
  - `1f5f2c5`, 17:31:17: the second version, after the review;
  - Cursor Bugbot on `1f5f2c5` at 17:38:29: "Revoke leaves family links active" (Medium);
  - `f163e90`, 17:38:50: the one-line fix; reply 「属实，已修复」 at 17:38:57;
  - the handoff comment at 20:28.
- **Context:**
  - issue #11, 「【决策】后端选型：数据库、账号认证、怎么容器化」;
  - issues #12, #13, #14, #20, #22, #44;
  - the meeting summary of Mon 2026-10-26 (`docs/meetings/2026-10-26/summary.md`);
  - `docs/ARCHITECTURE.md` §1;
  - decisions 0004 (triage, PR #36) and 0005 (insurance card, PR #38);
  - the other 0006, `docs/decisions/0006-triage-chat-copies-claude.md` (PR #41).

An independent accuracy pass checked the script against the three commits, the PR body and
threads, the issues, PRs #36/#38/#41, `main`'s docs and the outside documentation. It corrected
the points marked ✱.

| Claim in the video | Source |
| --- | --- |
| Today the prototype has no backend: data from `src/data`, state in the browser's `localStorage`; the clinics and prices shown are made up ✱ | `D` 「问题陈述」; `docs/ARCHITECTURE.md` §1 (clinics, insurers, pharmacies and prices are fictional; the school, neighbourhoods and 911/988 are real) |
| A parent in China cannot see the card a student added in Boston; accounts (#13), family links (#14) and insurance cards (#22) need one shared place | `D` 「问题陈述」; the issues named |
| Late Friday afternoon an agent wrote a 223-line decision record ✱ | `57cbffa` 17:24 (172 lines) → `f163e90` 17:38 (223 lines); author: the agent session in the PR body |
| A backend's jobs: a server that checks the rules, a database that remembers, a login step, containers | the episode's own framing of `D`'s four sections (language/framework, database, auth, containers) |
| The one hard rule from Monday's meeting: it must run on Mac and Windows: 「唯一的硬性要求：做出来的东西能在 Mac 和 Windows 上都跑起来（容器化，例如 Docker）」 | `docs/meetings/2026-10-26/summary.md`:24 |
| The choices: Hono and Zod (server), Postgres (database), Better Auth with emailed codes (login), Docker Compose (`db`, `api`, `web`) | `D`:32, :45, :53, :69, :75, :81, :87 |
| Browsers only run JavaScript; the page is TypeScript; 「前端是固定的约束，应该是后端适配前端。」 | `D`:21–26 (the quote at :25) |
| Both prototypes, triage and insurance, already TypeScript, in open pull requests ✱ | PR #36 (triage), PR #38 (insurance), both unmerged; the handoff warns that `D` relies on their code |
| One description of the data shared by page and server; rename a field on the server and the page fails its check | `D`:32, :77–78 (Hono `hc`, `AppType`); Hono RPC guide, <https://hono.dev/docs/guides/rpc> (both ends need `strict`; the root tsconfig has it). The `InsuranceCard` / `memberId` / `groupNumber` shape on screen is labelled an illustration |
| Python's strength, AI retrieval libraries, isn't needed: the triage proposal looks up prices, phone numbers and hours in checked fact cards by code, not by vector search ✱ | `D`:36 (「由代码查询，不是向量检索」); 0004 is itself a proposal, in unmerged PR #36 |
| Python stays an exit: a separate service later, behind the TypeScript one | `D`:39 (types generated from a Zod → OpenAPI file; example need: fine-tuning an open model, from 0004) |
| Express: 「没有内建的请求检查和类型，要自己拼」; NestJS: 「规矩多、样板代码多，对三个人的 MVP 太重」; Supabase / Firebase: user and health data with a third party before the privacy rules (#20) are settled | `D`:34, :35, :37 |
| Fastify: 「同样合适……没有决定性差异」, an equal alternative, not rejected ✱ | `D`:33 (marked 「备选」; the handoff lists it under 放弃, the record governs) |
| Postgres because the data is links: parent ↔ student, every permission check follows the link | `D`:45 |
| MongoDB lost: 「家长–学生关联、权限检查是典型的关系型查询」; SQLite: 「单文件，不适合以后多人同时在线」 | `D`:47, :46 |
| One flexible column: each insurance field stores `{value, confidence, source, raw}` | `D`:164–188 (JSONB keyed by 0005's `FieldKey`); matches PR #38 `prototypes/insurance/src/extract.ts`:10–20 |
| The image `pgvector/pgvector:pg17` ships an add-on for searching by meaning; nothing needs it today: 「以后需要按语义相似度查找时，启用 pgvector 扩展即可，不用换库」 | `D`:45, :81 (a migration with `CREATE EXTENSION IF NOT EXISTS vector;`); <https://github.com/pgvector/pgvector>; Drizzle has 「no specific code to create an extension」 (<https://orm.drizzle.team/docs/extensions/pg>) |
| Table changes travel as numbered migration files | `D`:81 (drizzle-kit); <https://orm.drizzle.team/docs/migrations> |
| No passwords: email → a 6-digit code, 5 minutes, 3 tries | `D`:82–86; Better Auth email-OTP defaults (6 digits, 300 s, 3 attempts), <https://www.better-auth.com/docs/plugins/email-otp> |
| The record requires a stored hash (`storeOTP: 'hashed'`; the library's default is `plain`) and its own per-email limit, 1 code / 60 s and 5 / hour, in dev and production ✱ | `D`:84–85; Better Auth's own limiter counts by IP address, is off in development and keeps counts in memory (<https://www.better-auth.com/docs/concepts/rate-limit>), so the per-email rule is the record's addition |
| `AUTH_LOG_OTP` prints codes in development only | `D`:86 |
| 「MVP 只用邮箱验证码（Junyi 2026-10-30 确认）」 ✱ | PR #43 body only; the record does not say it, and the handoff still lists email-only among the points to confirm in person |
| The record's reasons: every Chinese parent has an email (QQ, 163 …); no password to forget | `D`:59 |
| SMS 「发国内号码要花钱」; WeChat 「需要企业资质和开放平台审核」; Clerk / Auth0 「用户数据存在第三方；按用户数收费；国内访问情况不确定」; from scratch 「容易出安全问题」 | `D`:61, :62, :54, :57. Lucia 「已停止维护」 (`D`:55; lucia-auth.com: "deprecated in March 2025") and Auth.js (`D`:56) are in the record, not on screen |
| Better Auth runs inside our own server and keeps everything in our own Postgres ✱ | `D`:53 (drawn inside the `api` box in s02) |
| `role`: student or parent, written once, `input: false` (Better Auth's default is `true`), not changeable by the user in this first version: 「否则学生能把自己改成家长」 ✱ | `D`:98–116; <https://www.better-auth.com/docs/concepts/database> (`input` defaults to `true`); the email-OTP plugin accepts additional fields for new users |
| Only the student starts a family link, because the patient owns the health data: 「关联只能由学生发起」 | `D`:150 |
| The invite code: at least 8 characters, 72 hours, usable once (stored as HMAC-SHA256) | `D`:152–156 |
| Once linked, the parent sees the profile and the current card, read-only; later data such as triage is closed to parents by default | `D`:185, :162 |
| 「不存保险卡图片」, for the MVP; the card is read on the device; only the text fields are kept ✱ | `D`:181; 0005:33 (on-device OCR, in unmerged PR #38) |
| Four review angles (outside facts, consistency with the repo, privacy and data model, the issue's checklist); 31 comments, a judge kept 14; the second version 17:31 | PR #43 body (「31 条原始意见经裁判复查后保留 14 条」); the 31 are not on GitHub; commit `1f5f2c5` |
| Three fixes in the second version ✱: home-made status and source labels per insurance field (`clear · card · inferred`) → PR #38's own (`confidence · source · raw`); linked parents could enter cards → parents read-only; reuse of the services that carry fictional data → banned in the backend | `57cbffa`:136–143 (field *names* from 0005; the labels inside invented), :142 (`createdByUserId`, parent as enterer) → `D`:185; `D`:79 (「不 import `src/services/`、`src/adapters/`、`src/data/`（它们会把模拟数据带进后端）」) |
| The handoff admits: 「初稿里保险字段的状态和来源名称是 agent 自己起的，没先读 PR #38 的代码」 | PR #43 handoff comment, 20:28 |
| The revision added a mistake of its own ✱: unlinking only set `revokedAt`, the status stayed `active`, so a parent would have kept access; in a written plan, before any code existed | `1f5f2c5`:161 (「解除只写 `revokedAt`」); `57cbffa`:130 had only 「学生可以随时解除」; `f163e90`:161 sets `status='revoked'` too. The `revokedAt = set` row on screen is a neutral illustration ✱ |
| Bugbot 17:38:29 "Revoke leaves family links active"; fix 17:38:50, 21 s later; 「属实，已修复」 | PR #43 review thread; commit `f163e90` |
| The record's own success test: after the student unlinks, the parent's next request gets 403, checked by an automated test ✱ | `D`:198–204 (tagged #13 and #14; already in `1f5f2c5`:202) |
| The decision is still a proposal; #11's open box: 「线下三人确认后，决策状态改为「已采纳」」 ✱ | `D` status line; issue #11 acceptance criteria; PR body |
| Still open: access from China (#44); an email service that stays out of QQ / 163 spam; whether parents may enter card details (#14); how long deleted data lingers (#20) | `D`:220–223 |
| Two product calls, provisional until #14 and #20 decide ✱: parents see nothing new by default; deleting a student's account deletes their card | `D`:162, :222; `D`:190–194 (`ON DELETE CASCADE`), :223 |
| Two decisions numbered 0006: triage chat copies Claude (2026-10-28, PR #41) and backend stack (2026-10-30, PR #43) | `0006-triage-chat-copies-claude.md` (commit `e8df1b7`, 10-28 01:59) and `D`; `main` holds 0000–0003 only; the decisions README has no collision rule |
| Week 44 | ISO week of Fri 2026-10-30 |

## Corrections from the accuracy pass

These were wrong or imprecise in the first draft of the script and are fixed in the video:

- "invented insurance field names" (the names came from 0005; what was invented were the status and source labels inside each field);
- "Bugbot found one more mistake from the first draft" (the revision introduced it, in a written plan; no parent ever had access);
- Fastify struck through as rejected (the record calls it an equal alternative);
- "the issue asks all three of you to sign it" (one box: confirm in person, then mark it adopted);
- "two product calls hide in this document" (they sit there, provisional until #14 and #20 decide);
- the `revokedAt` row showed 17:31, the commit time (now a neutral "set");
- "from checked fact cards, not from search" (looked up by code, not by AI similarity search; 0004 is a proposal);
- "let parents edit the card" (linked parents could enter cards);
- "you confirmed it because every parent has email" (the PR notes the confirmation; the reasons are the record's);
- the hash and per-email limits presented as library defaults (they are the record's own requirements);
- "the data itself is fictional" (the clinics and prices are);
- the prototypes "already TypeScript" (in open, unmerged pull requests);
- the login gate drawn between page and server (it runs inside the server);
- "never" for the role and the card photos (the record limits both to this first version).
