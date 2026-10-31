# 项目周记 E6 · How the backend was chosen — script & visual plan

Series: *项目周记* (`docs/PORTAL_SERIES.md`). Watch after E5. Brief: `BRIEF.md`; every claim's source:
`SOURCES.md`.

Audience: Conny, after E1–E5. Goal: he can name the four jobs of a backend and the choice for each,
say why the language was decided by the page, give the reason each main alternative lost, say what
the first data model protects, retell how review caught the one-word unlink bug, and list what is
still open.

**Narrated.** SAY lines are spoken (Kokoro `af_heart`, 0.95×, over a quiet music bed) and shown as
subtitles (Chinese above, English below). Times are Boston time.

Colours: the page / front end BLUE · the server ORANGE · the database GREEN · login YELLOW · rejected
options GREY with a RED strike · parents and privacy rules YELLOW · problems RED.

---

## S01 · Nowhere to fetch it from — `s01_hook.py` · `Hook`

SHOW: A student's laptop in Boston and a parent's phone in China. Each has its own drawer labelled 「localStorage」, filled from `src/data` (fictional). The student adds an insurance card; the parent's phone asks for it, and an arrow goes out and finds nothing. Three issue cards: accounts (#13), family links (#14), insurance cards (#22), all pointing at one empty box, "one shared place?".
SAY: Right now our prototype has no backend. Everything a user does is saved in that one browser, on that one device, and the clinics and prices it shows are made up. So a parent in China cannot see the insurance card their child added in Boston: there is nowhere to fetch it from. Accounts, family links and insurance cards all need one shared place to live.

SHOW: The decision record's title 「0006：后端用 TypeScript（Hono + Postgres），账号用邮箱验证码，Docker Compose 容器化」, status 「提议」, 2026-10-30, 223 lines, PR #43.
SAY: Late on Friday afternoon an agent wrote a 223-line decision record proposing where. This episode is about how it chose, and what it protects.

---

## S02 · Four jobs — `s02_jobs.py` · `Jobs`

SHOW: A request's path, animated: phone → `web` (the page) → `api` (the server: a login step inside it, "who are you?", then rules and permission checks) → `db` (the database: remembers). The 10/26 rule as a banner: 「做出来的东西能在 Mac 和 Windows 上都跑起来」. A container outline wraps `db · api · web`; then each slot gets its name: Hono + Zod · Postgres + Drizzle · Better Auth, email code · Docker Compose.
SAY: A backend has a few jobs. A server receives every request and checks the rules: who is asking, and are they allowed. A database remembers. A login step proves who you are. And because the team set one hard rule at Monday's meeting, that the product must run on both Mac and Windows, everything goes into containers that start with one command. The record fills each slot: Hono, a small framework for the server, with Zod to check the shape of every request; Postgres for the database; Better Auth with emailed codes for login; and Docker Compose to run the three boxes together.

---

## S03 · The page decides the language — `s03_language.py` · `Language`

SHOW: A browser box: "runs JavaScript / TypeScript". The question.
SAY: The first question was language.

SHOW: Pause-and-ponder card.
SAY: You read Python. Why isn't the backend in Python?

SHOW: The quote 「前端是固定的约束，应该是后端适配前端。」 (decision record). The two prototypes already in TypeScript, in open pull requests: triage (PR #36), insurance (PR #38). One shape of data shared by page and server; a field renamed on the server turns the page's check RED before anything runs.
SAY: Because browsers only run JavaScript, and our page is written in TypeScript, which is JavaScript with type checks added. The record makes it a rule: the front end is a fixed constraint, so the back end adapts to it. Both prototypes, triage and insurance, are already written in TypeScript, in their open pull requests. With one language, the server and the page share a single description of every piece of data; rename a field on the server, and the page fails its check before anyone runs it.

SHOW: The rejected options as cards, each struck through with its reason: Python + FastAPI (its strength is AI retrieval libraries, but the triage proposal 0004 looks up prices, phones and hours in fact cards by code, not by vector search; two copies of every type; two prototypes rewritten) → kept as "a separate service later"; Express 「没有内建的请求检查和类型，要自己拼」; NestJS 「规矩多、样板代码多，对三个人的 MVP 太重」; Supabase / Firebase (user and health data with a third party, before #20 settles privacy). Not struck: Fastify 「同样合适…没有决定性差异」, an equal alternative.
SAY: Python's main advantage would be its libraries for AI retrieval, but the triage proposal looks up prices, phone numbers and opening hours in checked fact cards, not by AI similarity search. So Python stays an exit: a separate service later, behind the TypeScript one. Express lost for having no built-in request checks, NestJS for too much ceremony for three people, and hosted backends like Supabase because user and health data would sit with a third party before the team has settled its privacy rules. Fastify was just as good; the record calls it an equal alternative.

---

## S04 · A database of links — `s04_database.py` · `Database`

SHOW: Postgres as tables joined by arrows: user → family_link ← user, insurance_card → user. Every permission check follows the arrows. Rejected: MongoDB 「家长–学生关联、权限检查是典型的关系型查询」; SQLite 「单文件，不适合以后多人同时在线」.
SAY: For the database, Postgres. The data is about links: a parent is linked to a student, and every permission check follows that link. MongoDB lost for exactly that reason, and SQLite because a single file doesn't suit many people online at once.

SHOW: One insurance field opening up: value · confidence · source · raw text, all in one JSON cell. A grey door labelled pgvector: "search by meaning: not needed today". Migration files numbered 1, 2, 3 applied in the same order on two laptops → identical tables.
SAY: One column is flexible on purpose: an insurance field stores not just a value but how sure the card scanner was, where it came from, and the raw text it was read from. The database we install also comes with an add-on for searching by meaning, but nothing needs it today; it is an open door, not a plan. Changes to the tables travel as numbered migration files, so every copy of the database ends up the same.

---

## S05 · Login without passwords — `s05_login.py` · `Login`

SHOW: An email → a 6-digit code → a 5-minute timer → 3 tries; the record requires keeping only a hash (a lock; the library's default would be plain text). The record's own limits: 1 code per 60 s, at most 5 per hour, per email (on top of the library's IP-based default). A dev-only switch `AUTH_LOG_OTP` prints codes to the server log; production forbids it.
SAY: Login uses no passwords at all. You type your email and receive a six-digit code, valid for five minutes, with three tries, and the record requires the server to keep only a scrambled hash of it, so the codes are never stored as readable text, plus its own limit of one code a minute per address, at most five an hour. The pull request notes you confirmed email-only on Friday. The record's reasons: every Chinese parent has an email address, and nobody has a password to forget.

SHOW: Rejected, struck through: SMS 「发国内号码要花钱」; WeChat 「需要企业资质和开放平台审核」; Clerk / Auth0 「用户数据存在第三方；按用户数收费；国内访问情况不确定」; Lucia 「已停止维护」; building it ourselves 「容易出安全问题」. Chosen: Better Auth, inside our server, writing to our own Postgres.
SAY: Text messages to Chinese numbers cost money, WeChat login needs a registered company, and hosted login services keep user data elsewhere and charge per user. Writing it from scratch is how security holes happen. The library chosen, Better Auth, runs inside our own server, and keeps everything in our own Postgres.

---

## S06 · A data model that protects people — `s06_model.py` · `Model`

SHOW: The `user` card: role student | parent, written once, `input: false`; the quote 「否则学生能把自己改成家长」.
SAY: Then the shape of the data, the part that protects people. Every account has a role, student or parent, written once and, in this first version, not changeable by the user; otherwise, the record notes, a student could make themselves a parent.

SHOW: Pause-and-ponder card, over the two devices.
SAY: Who should be able to start a family link: the student, or the parent?

SHOW: The family link, animated: only the student starts it; an invite code (≥ 8 characters, 72 hours, single use) travels to the parent; the link turns active; the parent sees the student's profile and current insurance card, read-only; triage chats and later data stay behind a lock. 「不存保险卡图片」.
SAY: Only the student can start a family link, because the student is the patient and owns the health data. They create an invite code: at least eight characters, valid for seventy-two hours, usable once. Once linked, a parent sees the student's profile and current insurance card, read-only, and nothing else; anything added later, such as triage chats, is closed to parents by default. For now, card photos are not stored; the card is read on the device, and only the text fields are kept.

---

## S07 · Review, and one missing word — `s07_review.py` · `Review`

SHOW: Four reviewers (outside facts · consistency with the repo · privacy and data model · the issue's checklist) → 31 comments → a judge → 14 kept, applied in the second version (17:31). Three fixes shown before → after: home-made status and source labels for each insurance field (`clear · card · inferred`) → PR #38's own (`confidence · source · raw`) (handoff: 「初稿里保险字段的状态和来源名称是 agent 自己起的，没先读 PR #38 的代码」); linked parents could enter cards → read-only; reuse of the services that carry fictional data → banned.
SAY: The first draft was read by four reviewers from different angles: outside facts, consistency with the repository, privacy and the data model, and the issue's checklist. They raised thirty-one comments, and a judge agent kept fourteen. The second version fixed, among other things, three real mistakes: it had made up its own status and source labels for insurance fields instead of reading the insurance code, let linked parents enter cards, and planned to reuse services that carry fictional data.

SHOW: The second version's written rule for unlinking: `revokedAt` = set · `status` = active (RED) → a parent's request would still succeed. Bugbot, 17:38:29: "Revoke leaves family links active". Fix 17:38:50: `status` = revoked; the parent's request → 403. 「属实，已修复」.
SAY: But the revision added a mistake of its own, and Bugbot caught it. Unlinking only recorded the time and left the link marked active, so a parent would have kept access. One missing word, in a written plan, before any code existed. The fix landed twenty-one seconds after the comment.

SHOW: Pause-and-ponder card.
SAY: If no bot had been watching, what would have caught it?

---

## S08 · What is still open — `s08_open.py` · `Open`

SHOW: The record's success criteria: "after the student unlinks, the parent's request gets 403; automated test" (#13, #14), lit. Status 「提议」 and #11's one open box: 「线下三人确认后，决策状态改为「已采纳」」.
SAY: A test would, and the record already asks for one: after a student unlinks, the parent's next request must be refused, checked automatically. The decision itself is still a proposal; the issue asks the three of you to confirm it in person before it is marked adopted.

SHOW: Open questions: access from China (#44) · an email service that doesn't land in QQ or 163 spam · can parents enter card details (#14) · how long deleted data lingers (#20). Two product calls inside a technical record (YELLOW), both provisional until #14 and #20 decide: parents see nothing new by default · deleting a student's account deletes their card. A housekeeping note: two decisions numbered 0006 (triage chat, 10-28, PR #41 · backend, 10-30, PR #43).
SAY: Still open: whether the servers can be reached from China, which email service stays out of QQ and one-six-three spam folders, whether parents may enter card details, and how long deleted data lingers. Two product calls sit in this technical document, both provisional until those issues decide: parents see nothing new by default, and deleting a student's account deletes their card. And one piece of housekeeping: two different decisions are both numbered six.

---

## S09 · Recap — `s09_recap.py` · `Recap`

SHOW: The four slots with their choices, and the one rule; then the data model's three protections.
SAY: So: TypeScript, because the page decides; Postgres, because the data is links; emailed codes, because every parent has email; containers, because it must run on any laptop. And a data model whose real job is privacy.

SHOW: Three test-yourself questions, then a held pause.
SAY: Three questions. Why isn't the backend in Python? What stops a student from making themselves a parent? And what would have caught the unlink bug without a bot?

SHOW: End card: 「项目周记 · 第 44 周 完」; next week starts from next week's pull requests.
SAY: That ends this week's batch. Next week's episodes start from next week's pull requests.
