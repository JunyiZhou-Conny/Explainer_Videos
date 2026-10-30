# 项目周记: the build-log series

Short videos that explain, at the level of ideas, what the owner's own pull requests did in a week
of building the startup prototype in
[JunyiZhou-Conny/InternationalHealthportal](https://github.com/JunyiZhou-Conny/InternationalHealthportal)
(a care-navigation app for Chinese parents and their children studying in Boston; the product
has no final name yet, so it is called 「项目」, which is where the series gets its title). Most of
that code is written by AI agents. These videos let the person who directs them understand
what was built, how it got built, what it copies, and what could come next.

The agent's how-to is the `portal-video` skill (`.claude/skills/portal-video/SKILL.md`). The batch
plan and the weekly digests are in [`videos/portal-series/`](../videos/portal-series/README.md).
[STYLE_GUIDE.md](STYLE_GUIDE.md) and the `3b1b` preset apply; this page adds what this series needs.

## Who it is for

**Conny, the founder.** He directs Claude and other agents every day, reads Python but not
TypeScript, and uses ChatGPT and Claude himself. He sees the product's screens: a "thought for 3
seconds" line, a summary for parents, a model menu. He does not know what these things are called,
how they work, or which of them are standard. He wants:

1. **Names.** The industry term for each thing on screen (structured outputs, prompt caching,
   reasoning effort, streaming, guardrails, fallback…), so he can talk about it and search for it.
2. **The mechanism.** How it works in *our* app, drawn, not coded.
3. **The path.** Which problem the pull request solved, what was tried and dropped, where a human
   decided, and how the agents spent their hours.
4. **Copy vs. own.** What mirrors Claude or ChatGPT, what we deliberately did not copy and why,
   and what we added for our users.
5. **The design space.** What else is possible from here, and which decisions are still only
   proposed (「提议」) and waiting for him.

Teammates and Bilibili viewers are a secondary audience. The owner decided on 2026-10-30 that the
series is public and published to Bilibili like every other episode.

## The unit: one week, one batch

- Each week (Monday to Sunday, Boston time), `tools/pr_digest.py` lists the owner's pull requests
  from a local clone of the portal repository: merged and open, with commit timelines, areas
  touched and decision records. The digest and the PR list it was made from are committed to
  `videos/portal-series/weeks/<YYYY>-w<NN>.md`.
- From the digest, plus the PR descriptions, handoff comments and review threads, the agent plans
  a **batch of one to four episodes**. An episode answers **one question raised by something
  visible** in the product ("what is 'thought for 3 seconds'?"), not one pull request; it may draw on
  several. A week whose interesting part is how the work went can have one build-log episode.
- A quiet week can have no episode. Small PRs (meeting notes, a rename) are mentioned in a
  batch's build-log episode or skipped.
- Episodes are numbered across weeks: `portal-e1-<topic>`, `portal-e2-<topic>`, …; the Studio
  board shows them as 项目周记 E1, E2, ….

## Length and shape

**10 minutes at most; aim for 7–9.** At the house voice (Kokoro `af_heart`, 0.95) the narration
runs about 165 words a minute, and pauses, ponder holds and animations add 10–15 %, so about 145
words make one finished minute: 1,000–1,300 words. E1 (1,487 words, 9:44) is the practical ceiling.
Count with `python -m explainer.script videos/<id>/script.md` before building scenes, and time the
real speech with `explainer.script.synthesize_all`; cut words, never speed.

Every episode has these beats, in this order (scene counts are a guide):

| Beat | What it does | Scenes |
|---|---|---|
| Hook | A real screen from the product, redrawn with its exact strings, and the question it raises | 1 |
| Name it | The industry term(s), once each, in English with the Chinese gloss in the captions | inside the mechanism scenes |
| Mechanism | One animated diagram per core idea, of *our* implementation | 3–5 |
| The path | From the PR timeline: the problem, what was tried, the turn, who decided, what it cost | 1 |
| Copy vs. own | What the reference product does, what we copied, what we refused, what we added | 1 |
| Design space | What becomes possible, and the open decisions waiting for the owner | 1 (may share with the previous) |
| Recap | The ideas in one breath, three test-yourself questions, the next episode | 1 |

At least two pause-and-ponder questions per episode, each answerable from what was just shown.

## Evidence

Everything on screen is real and pinned in the episode's `SOURCES.md`:

- **Code** at a named branch and commit (PRs move: say "as of <date>"). Read in the portal clone,
  never guessed from file names.
- **PR descriptions, handoff comments, review threads, issues** by number and date.
- **Decision records** (`docs/decisions/NNNN-*.md`) with their status: 「提议」 (proposed) is shown
  as an open question, never as settled.
- **Numbers** (tests, costs, timings, commit counts) from the PR's own verification notes or the
  weekly digest. The digest's commit times are in Boston time.
- **Screens** are redrawn in the scene from screenshots the owner provides or from the UI strings
  in the source, copied exactly. A string we could not see is labelled `illustration`.
- **How Claude, ChatGPT or the OpenAI API behave** is stated only from their public documentation
  (cite the page and the date read) or as observed behaviour of the app on a stated date. Never
  claim how their internals are built.

## Rules specific to this series

1. **No TypeScript on screen.** Show the mechanism as a diagram. When the logic itself is the
   point, at most six lines of Python-style pseudo-code, tagged `PSEUDO-CODE · from <path>`. Field
   names (`parentSummaryZh`, `citations`) may appear as labels.
2. **Name things once, then reuse the name.** New terms go into
   [`videos/portal-series/GLOSSARY.md`](../videos/portal-series/GLOSSARY.md) with the Chinese
   rendering used in the captions; later episodes use the same words.
3. **Teammates by role, not by name** (the medical reviewer, the insurance teammate): the source
   repository is private and they have not agreed to appear in a public video. The owner is "you".
4. **Never show** API keys, `.env` files, account or billing identifiers, private Drive links, or
   anything about real patients (the triage cases are fictional, and the video says so).
5. **Medical safety.** The video explains the product's safety design. It never gives medical
   advice itself; example symptoms come from the fictional cases in `prototypes/triage/cases/`.
6. **Honest status.** A draft PR is "not merged yet"; a proposed decision is "proposed"; an
   unreviewed medical rule is "waiting for the medical reviewer".

## Visual language

**3Blue1Brown style (`3b1b`), from E2 on** (owner, 2026-10-30: 「以后用 3BLUE1BROWN STYLE」). E1 was
made in Swiss before that decision and stays as it is. The house dark-diagram toolkit
(`explainer/style.py`, `components.py`, the CareOneX kit `videos/careonex-series/careonex_kit.py`):
near-black background, CMU Serif prose, objects that move and transform rather than slides of
bullets. Series conventions on top of it:

| Meaning | Treatment |
|---|---|
| The product's own screen (chat page, receipt) | a dark rounded panel with strings verbatim, in the product's Chinese |
| Our code (server, checker, page) | BLUE box (`tag_box`, tag OUR CODE) |
| The model / the API | ORANGE box labelled with the model name |
| Hidden reasoning | GREY tokens: there, billed, never shown |
| Text the reader may see | WHITE tokens; checked text GREEN |
| The question, the user's words | YELLOW |
| Danger, emergency, a rule that blocks | RED |
| The reference product (Claude, ChatGPT) | GREY outline with the name in text, never a logo |
| Time | a horizontal axis in seconds; the stopwatch phases as coloured bars |
| A ponder question | the house `pause_and_ponder` card |

## Production

From E2: the `video.yaml` route, as in the CareOneX and AC215 series (`docs/WORKFLOW.md`,
`docs/STYLE_GUIDE.md`): `script.md` (SHOW/SAY), `scenes/` (one file per scene plus `common.py`,
which imports the CareOneX kit), `i18n/zh/` (glossary, `meta.yaml`, sentence-aligned narration),
`video.yaml` with a `publish:` block, built with `python -m explainer.build videos/<id> --burn`
(1080p60, Kokoro `af_heart` 0.95, music, Chinese-above-English subtitles burned in). Release after
merge with `.github/workflows/legacy-release.yml`. Each folder also holds `BRIEF.md`,
`SOURCES.md` and `REVIEW.md`, and the episode lifecycle and content gates in `AGENTS.md` apply.
E1 (`videos/portal-e1-after-send/`, `episode.json` route) remains the record of the Swiss start.

The producing session needs read access to the private portal repository: in a cloud session,
attach it (`add_repo`, read access); locally, clone it next to this checkout. Fetch the PR branches
before running the digest (`git fetch origin <branch>`).
