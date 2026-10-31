# Review record: How do you choose a backend? (项目周记 E6 · 后端怎么选)

Produced 2026-10-31 by a Claude Code cloud session (issue
[#67](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/67)) on branch
`claude/funny-cannon-6at1kg`, in the 3Blue1Brown style (the house default since 2026-10-30). Verified
facts and unclaimed reviews are kept separate.

## Content gates (AGENTS.md)

1. **Hook.** s01 shows a student's laptop in Boston and a parent's phone in China, each with its own
   `localStorage` drawer. The parent asks for the insurance card the student added and gets nothing:
   there is nowhere to fetch it from. Accounts, family links and cards need one shared place. ✔
2. **Intuition before formalism; an animated mechanism per core idea.**
   - s02: a request travels phone → page → login → server → database; then the Monday rule, and the same
     sealed `db · api · web` box landing on a Mac and a Windows laptop with one command.
   - s03: the browser runs JavaScript, so the page decides; one shared description of the data, and a
     renamed field failing the page's check; one question answered by a fact-card lookup against an AI
     similarity search; the options and why they lost.
   - s04: the tables and the link every permission check follows; one insurance field's four parts lit as
     spoken; migration files bringing two databases to the same tables.
   - s05: email → a six-digit code with its clock and tries, the stored hash, the per-email limits; the
     options and why they lost.
   - s06: the role written once; the student's "start link" against the parent's struck one; an invite
     code travelling to the phone; the link, what the parent sees and what stays closed.
   - s07: four reviewers → 31 comments → a judge agent → 14; three before/after fixes; then the written
     unlinking rule with `status = active`, Bugbot's finding, the one-word fix, and the request refused.
   - s08: the record's own 403 test; the 「提议」 status and #11's box; what is open; the two-0006 clash.

   No code on screen beyond field names and the record's labels. ✔
3. **Ponder moments and recap.** Three pause-and-ponder cards with a held pause:
   - s03: "You read Python. Why isn't the backend in Python?" Answered at once.
   - s06: "Who should be able to start a family link: the student, or the parent?" Answered at once.
   - s07: "If no bot had been watching, what would have caught it?" s08 answers it (a test would).

   s09 recaps the four choices and the data model's job, asks three test-yourself questions (answered in
   s03, s06, s08), then holds a 5 s pause. ✔
4. **Written for the ear; anchored cues.**
   - "163" is said "one-six-three", the way the mail service is named; "403" is never spoken (the
     narration says "refused"); 223 and seventy-two hours were checked at the phoneme level.
   - Chinese strings (the record's quotes) are shown, never read.
   - Every reveal waits on a word anchor; a script check confirms every anchor occurs in its narration,
     and the lint reports none missing. ✔
5. **Simulated-viewer QA over the full draft.** Findings and fixes below. ✔
6. **Measured checks + human review.** Measured values under *Verified*. Human review: **waived** by
   Conny (AGENTS.md, 2026-10-22): 「我大概率是不会进行审片的，因为我觉得做得已经非常好了，就让bugbot来检查就好了」.
   No human has listened to this cut. ✔ (waiver)

## Research and script review before scenes

- **Research.** An independent agent read decision 0006 (`docs/decisions/0006-backend-stack.md`, 223
  lines at `f163e90`), the three commits, the PR body and review thread, issue #11 and the 10-26 meeting
  summary, and checked the outside facts against each tool's own documentation (Hono, Zod, Drizzle,
  Better Auth, Lucia, pgvector, Docker Compose, WSL2).
- **Accuracy read** (a second independent agent, against the three commits, the PR, the issues and
  `main`'s docs): 15 findings, all applied. They are listed in `SOURCES.md`. The ones that changed the
  story:
  - the first draft took its field *names* from 0005; what it invented were the status and source labels;
  - the unlinking mistake was introduced by the revision, in a written plan; no parent ever had access;
  - Fastify is an equal alternative, not a rejected option;
  - #11 asks the three to confirm in person; nothing is signed;
  - the hash and the per-email limits are the record's requirements, not the library's defaults;
  - the owner's email-only confirmation is in the PR body; the reasons are the record's.

## Whole-video QA (first draft, 7:05)

**Who reviewed.** An independent agent played Conny, knowing nothing about backends, working from the
bilingual subtitles and one frame every 3 s (plus exact frames it pulled to time static stretches). I
also made two frame-by-frame passes over every scene (one before and one after the fixes).

**Gates as first judged.** Hook: pass. Mechanisms: **partial** (containers, Python against retrieval,
the hash and card photos were cards or labels). Ponder: pass with a gap (none between 1:18 and 5:31).
Recap: pass.

**Fixes.**

- [05:24–05:33][WRONG] After the fix, the red "a parent's request would still succeed" stayed on screen.
  FIX: it turns into "one word, revoked: the parent's request is refused", which also names the word.
- [00:49–00:56][MISSING] Containers were a dashed outline. FIX: the same sealed `db · api · web` box
  lands on a Mac and a Windows laptop; one command; same result.
- [00:56–01:06][CONFUSING] Hono and Zod named, never explained; Drizzle shown, never said. FIX: the
  narration says "Hono, a small framework for the server, with Zod to check the shape of every request";
  the four picks are glossed on screen; Drizzle is dropped from the picture.
- [01:48–02:00][SLOW] The Python card sat for 12 s. FIX: one question answered two ways, a fact-card
  lookup by code against an AI similarity search (labelled an illustration); "vector search" became
  "AI similarity search" to match the narration.
- [02:39–02:50][SLOW/CONFUSING] The insurance field was static, "JSON" unexplained, "the reader" unknown.
  FIX: each part lights as it is spoken; "one flexible box (JSON)"; "how sure the card scanner was".
- [05:39][CONFUSING] 403 unexplained. FIX: "403 = refused".
- [02:48][CONFUSING] "Database image". FIX: "the database we install also comes with…".
- [06:22–06:28][LAYOUT] The two-0006 box showed for under 2 s. FIX: it arrives with "one piece of
  housekeeping" and holds 1.8 s after the line.
- [00:00, 00:23][SLOW] Black openings. FIX: the devices appear with the first word; the record arrives
  on "an agent wrote".
- [04:11–04:17][SLOW] Empty devices under "only the student". FIX: a "start link" on the student's laptop
  and a struck one on the parent's phone, after a new ponder on who should start the link (which also
  closes the four-minute gap between ponders).
- [03:13][WRONG timing] The hash came late and its purpose was unsaid. FIX: it appears on "keep only a
  scrambled", and the narration adds "so the codes are never stored as readable text". (Not "a stolen
  copy reveals no codes": a six-digit code's hash can be guessed offline, so that would overclaim.)
- [01:17][CONFUSING] Why the page's language binds the server. FIX: "…TypeScript, which is JavaScript
  with type checks added."
- [03:57][CONFUSING] `input: false` on screen. FIX: dropped; the chips say what it means.
- [04:54][CONFUSING] "A judge". FIX: "a judge agent".
- [02:06–02:18, 03:33–03:45][LAYOUT] The option cards mixed English and Chinese; Fastify shown, never
  said. FIX: the reasons are in English throughout (the captions carry the Chinese); the narration adds
  "Fastify was just as good; the record calls it an equal alternative."
- [captions] The Better Auth line shortened so it no longer repeats across two cues; s01's and s03's
  sentences reordered so their Chinese and English halves pair up; 「这些数据讲的是关联」 → 「这些数据的核心是关联」,
  「放在 TypeScript 后端的后面」 → 「由 TypeScript 后端来调用」, 「以编号的迁移文件传递」 → 「用带编号的迁移文件同步」,
  「还有一件内务」 → 「还有一处要整理的」.
- [LAYOUT] Caught in my frame passes and fixed: the four tool names overlapping under the diagram (now a
  2×2 legend); text overflowing the browser box; a dimmed box showing a grey patch behind two ponder
  cards (both ponders now clear the screen); the migration arrows pointing at nothing (two databases
  drawn); the invite-code facts over the laptop; red marks colliding with the chips above;
  "status =active" missing a space; text touching the recap cards' edges.

## Verified

(filled in after the final render)

## Not claimed

- **No human listened** to this cut; the listen is waived (above). Prosody, pacing by ear and music
  balance by ear are unverified.
- **No ASR round trip.** Risky words were checked at the phoneme level instead, and all read as
  intended: Hono, Zod, Postgres, Better Auth, Docker Compose, NestJS, Supabase, Fastify, MongoDB, SQLite,
  QQ, one-six-three, Bugbot, 223, seventy-two.
- **No backend exists yet.** Decision 0006 is a proposal in an open draft PR; every choice in the video
  is the record's proposal, not running code. The success test is required, not written.
- The fact-card/similarity picture in s03, the `InsuranceCard` shape in s03, the code `K7QW-3MRT`, the
  hash `#a91f…e03c` and the two laptops in s02 and s04 are illustrations.
- The owner's email-only confirmation is quoted from the PR body; the record itself does not carry it.
- The Chinese captions were checked by the viewer pass for meaning, not by a separate translator.
