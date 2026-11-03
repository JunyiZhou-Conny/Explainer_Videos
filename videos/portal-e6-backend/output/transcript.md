# 项目周记 E6 · How the backend was chosen: what each piece does, what lost, and what it protects

## 00:00 — Nowhere to fetch it from
Right now our prototype has no backend. Everything a user does is saved in that one browser, on that one device, and the clinics and prices it shows are made up. So a parent in China cannot see the insurance card their child added in Boston: there is nowhere to fetch it from. Accounts, family links and insurance cards all need one shared place to live.
Late on Friday afternoon an agent wrote a 223-line decision record proposing where. This episode is about how it chose, and what it protects.

## 00:33 — Four jobs
A backend has a few jobs. A server receives every request and checks the rules: who is asking, and are they allowed. A database remembers. A login step proves who you are. And because the team set one hard rule at Monday's meeting, that the product must run on both Mac and Windows, everything goes into containers that start with one command. The record fills each slot: Hono, a small framework for the server, with Zod to check the shape of every request; Postgres for the database; Better Auth with emailed codes for login; and Docker Compose to run the three boxes together.

## 01:12 — The page decides the language
The first question was language.
You read Python. Why isn't the backend in Python?
Because browsers only run JavaScript, and our page is written in TypeScript, which is JavaScript with type checks added. The record makes it a rule: the front end is a fixed constraint, so the back end adapts to it. Both prototypes, triage and insurance, are already written in TypeScript, in their open pull requests. With one language, the server and the page share a single description of every piece of data; rename a field on the server, and the page fails its check before anyone runs it.
Python's main advantage would be its libraries for AI retrieval, but the triage proposal looks up prices, phone numbers and opening hours in checked fact cards, not by AI similarity search. So Python stays an exit: a separate service later, behind the TypeScript one. Express lost for having no built-in request checks, NestJS for too much ceremony for three people, and hosted backends like Supabase because user and health data would sit with a third party before the team has settled its privacy rules. Fastify was just as good; the record calls it an equal alternative.

## 02:33 — A database of links
For the database, Postgres. The data is about links: a parent is linked to a student, and every permission check follows that link. MongoDB lost for exactly that reason, and SQLite because a single file doesn't suit many people online at once.
One column is flexible on purpose: an insurance field stores not just a value but how sure the card scanner was, where it came from, and the raw text it was read from. The database we install also comes with an add-on for searching by meaning, but nothing needs it today. It is an open door, not a plan. Changes to the tables travel as numbered migration files, so every copy of the database ends up the same.

## 03:17 — Login without passwords
Login uses no passwords at all. You type your email and receive a six-digit code, valid for five minutes, with three tries, and the record requires the server to keep only a scrambled hash of it, so the codes are never stored as readable text, plus its own limit of one code a minute per address, at most five an hour. The pull request notes you confirmed email-only on Friday. The record's reasons: every Chinese parent has an email address, and nobody has a password to forget.
Text messages to Chinese numbers cost money, WeChat login needs a registered company, and hosted login services keep user data elsewhere and charge per user. Writing it from scratch is how security holes happen. The library chosen, Better Auth, runs inside our own server, and keeps everything in our own Postgres.

## 04:10 — A data model that protects people
Then the shape of the data, the part that protects people. Every account has a role, student or parent, written once. In this first version, the user can't change it; otherwise, the record notes, a student could make themselves a parent.
Who should be able to start a family link: the student, or the parent?
Only the student can start a family link, because the student is the patient and owns the health data. They create an invite code: at least eight characters, valid for seventy-two hours, usable once. Once linked, a parent sees the student's profile and current insurance card, read-only, and nothing else; anything added later, such as triage chats, is closed to parents by default. For now, card photos are not stored; the card is read on the device, and only the text fields are kept.

## 05:04 — Review, and one missing word
The first draft was read by four reviewers from different angles: outside facts, consistency with the repository, privacy and the data model, and the issue's checklist. They raised thirty-one comments, and a judge agent kept fourteen. The second version fixed, among other things, three real mistakes: it had made up its own status and source labels for insurance fields instead of reading the insurance code, let linked parents enter cards, and planned to reuse services that carry fictional data.
But the revision added a mistake of its own, and Bugbot caught it. Unlinking only recorded the time and left the link marked active, so a parent would have kept access. One missing word, in a written plan, before any code existed. The fix landed twenty-one seconds after the comment.
If no bot had been watching, what would have caught it?

## 06:02 — What is still open
A test would, and the record already asks for one: after a student unlinks, the parent's next request must be refused, checked automatically. The decision itself is still a proposal; the issue asks the three of you to confirm it in person before it is marked adopted.
Still open: whether the servers can be reached from China, which email service stays out of QQ and one-six-three spam folders, whether parents may enter card details, and how long deleted data lingers. Two product calls sit in this technical document, both provisional until those issues decide: parents see nothing new by default, and deleting a student's account deletes their card. And one piece of housekeeping: two different decisions are both numbered six.

## 06:51 — Recap
So: TypeScript, because the page decides; Postgres, because the data is links; emailed codes, because every parent has email; containers, because it must run on any laptop. And a data model whose real job is privacy.
Three questions. Why isn't the backend in Python? What stops a student from making themselves a parent? And what would have caught the unlink bug without a bot?
That ends this week's batch. Next week's episodes start from next week's pull requests.
