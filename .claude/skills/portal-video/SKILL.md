---
name: portal-video
description: Make the weekly 项目周记 build-log videos that explain, without code, what Conny's pull requests in the private InternationalHealthportal repository did that week (the triage chat, its harness, its UI), for the founder who directs the agents. Use to plan a week's batch from the PR digest, or to produce, fix or continue one portal-eN episode.
---

# 项目周记 (build-log) videos

Binding rules: [`docs/PORTAL_SERIES.md`](../../../docs/PORTAL_SERIES.md) (audience, beats, length,
evidence, series rules). Production: the conny-explainer-video skill, `docs/BOOTSTRAP.md` and the
episode lifecycle in `AGENTS.md`. Reference episode: `videos/portal-e1-after-send/`. This file is
the *how* for this series.

## 0. Access

The source repository `JunyiZhou-Conny/InternationalHealthportal` is private.

- Cloud session: attach it with `add_repo` (read is enough), then clone it next to this checkout
  (`../InternationalHealthportal`).
- Local: clone it next to this checkout.
- Fetch every branch the week touched: `git -C ../InternationalHealthportal fetch origin`.
  Open PRs stack (a PR's base can be another PR's branch); the digest handles that.

## 1. The week's digest (once per week)

1. List the PRs from GitHub (MCP `list_pull_requests` with `state: all`, or
   `gh pr list --state all --json number,title,state,isDraft,author,headRefName`) and save the
   list as `videos/portal-series/weeks/<YYYY>-w<NN>.prs.json`.
2. Run, from this repository's root (Boston-time week, `--until` is the day after):

   ```bash
   python3 tools/pr_digest.py --repo ../InternationalHealthportal \
     --since 2026-10-26 --until 2026-11-02 \
     --prs videos/portal-series/weeks/2026-w44.prs.json --pr-author JunyiZhou-Conny \
     --out videos/portal-series/weeks/2026-w44.md
   ```

3. Read, for each substantial PR: its description, its handoff comments (`## 交接` on the PR), its
   review threads (Bugbot, Codex), its issue, and every decision record the digest lists. Append a
   short "What happened" note per PR under the generated digest: the problem, the turn(s), who
   decided what, what is still open. Facts only, each with its source.

## 2. Plan the batch

- Collect the owner's questions: what he asked in chat (quote it in the batch plan), plus the
  visible things the week added to the product.
- Group into one to four episodes, each answering one question raised by something on screen.
  Write the plan into `videos/portal-series/README.md` (episode table + one paragraph per episode:
  the question, the PRs and files, the terms it names, the ponder questions).
- Open one *Episode request* issue per episode, body citing `videos/portal-eN-<topic>/` and the
  branch, **without** the `@claude` line unless the owner asked for automatic production (it wakes
  an agent per issue). Add each to the plan's table.

## 3. Produce one episode

Follow BOOTSTRAP's reading order, claim the issue, then:

1. **Brief** (`BRIEF.md`): learning objective, audience (Conny; what he already knows from earlier
   episodes, per `GLOSSARY.md`), the scene beats from PORTAL_SERIES, terms to name, ponder
   questions, and what to skip.
2. **Sources** (`SOURCES.md`): the portal branch and commit, every file, PR, comment and decision
   used, the screenshots, and for every on-screen number where it comes from.
3. **Script** (`script.json`, English + Chinese per line). 1,050–1,350 words. Run
   `render.py <dir> --prepare-only` and size `episode.json`'s `duration_seconds` to the measured
   minimum plus 8–10 %; the reference scenes' `pause()` spends that slack after ponder questions.
   Write numbers as digits where Kokoro reads them right (89, 25,000, 5,550 dollars) and check
   risky words with the voice's `phonemize` ("911" needed a lexicon entry). Spoken forms: say "SHS" as "the student clinic", prices in
   words, no field names read aloud except where the scene shows them.
4. **Review the script before scenes** with two independent reads: accuracy against the code and
   PRs (every claim, every number), and a newcomer read as Conny (is each term named and drawn?
   is anything only asserted? is every recap question answered in the episode?). Fix every wrong
   or confusing finding. On E1 the accuracy read found 12 problems and the viewer read 9; both
   paid for themselves.
5. **Scenes** (`scenes.py`): reuse the reference episode's helpers (`EpisodeScene` with
   `header`/`pause`/`clear_body`/`dim_body`, `wrap`, `screen`, `receipt`, `node`, `chip`, `ponder`,
   `flash`). Use `flash` (an outline sweep), not `Indicate`, on filled boxes: `Indicate` paints
   them solid red. Redraw screens with verbatim strings. Keep every element above the
   caption band (y > −2.45). `explainer.check` must be clean.
6. **Sample, full render, QA, REVIEW.md** as in the conny-explainer-video skill and AGENTS.md's
   content gates. Owner's listening review is waived (AGENTS.md); quote the waiver.
7. Add new terms to `videos/portal-series/GLOSSARY.md` and update the plan's status.

## Reading TypeScript for a Python reader

The agents write the portal in TypeScript; the video translates. Useful mappings when reading it:
`interface`/`type` ≈ a `TypedDict` or dataclass; `async`/`await` ≈ Python's; `?.` and `??` ≈
"if not None"; `export function` ≈ a module-level `def`; React components (`.tsx`) are functions
that return the page's markup and re-run when their state changes. Explain behaviour in those
terms, never syntax.

## Pitfalls

- The triage app has two stacked PRs (#36 brain, #41 page). Pin the commit of the branch you read;
  the episode says "as of" that date.
- Most commits are authored as Claude or as Conny depending on the session; authorship in git does
  not tell you who decided. Decisions are in `docs/decisions/` and in the PR text.
- Times in PR text are sometimes Beijing time or UTC; the digest is Boston time. Say which.
