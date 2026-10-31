---
name: portal-video
description: Make the weekly 项目周记 build-log videos that explain, without code, what Conny's pull requests in the private InternationalHealthportal repository did that week (the triage chat, its harness, its UI), for the founder who directs the agents. Use to plan a week's batch from the PR digest, or to produce, fix or continue one portal-eN episode.
---

# 项目周记 (build-log) videos

Binding rules: [`docs/PORTAL_SERIES.md`](../../../docs/PORTAL_SERIES.md) (audience, beats, length,
evidence, series rules). Production: the conny-explainer-video skill, `docs/BOOTSTRAP.md` and the
episode lifecycle in `AGENTS.md`. Reference episodes: `videos/portal-e2-thinking/` (3b1b, the style from E2 on) and
`videos/portal-e1-after-send/` (Swiss, before the switch). This file is
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
3. **Script** (`script.md`, SHOW/SAY per beat, as in `videos/careonex-e6-measuring-search/`).
   1,000–1,300 words. Count with `python -m explainer.script <dir>/script.md`, time the real speech
   with `explainer.script.synthesize_all`. Then the Chinese captions in `i18n/zh/` (glossary,
   `meta.yaml`, `narration/<id>.yaml` sentence-aligned to the SAY lines;
   `python -m explainer.i18n check videos/<id> --lang zh`). Write numbers as digits where Kokoro
   reads them right (89, 25,000, 5,550 dollars) and check risky words with the voice's `phonemize`
   ("911" needed a lexicon entry).
4. **Review the script before scenes** with two independent reads: accuracy against the code and
   PRs (every claim, every number), and a newcomer read as Conny (is each term named and drawn?
   is anything only asserted? is every recap question answered in the episode?). Fix every wrong
   or confusing finding. On E1 the accuracy read found 12 problems and the viewer read 9; both
   paid for themselves.
5. **Scenes** (`scenes/`, one `VoiceScene` per file, narration from `NARRATION["Snn"]`): the 3b1b
   house style. `scenes/common.py` imports the CareOneX kit (`tag_box`, `chip`, `text_panel`,
   `link`, `token`, `travel`, `source_tag`) and the portal series' own helpers from E2
   (`videos/portal-e2-thinking/scenes/common.py`: the product's screens, the token tape, the
   stopwatch bars). Redraw screens with verbatim strings. `python -m explainer.check` must be
   clean; preview at 480p (`python -m explainer.preview`) and read every contact sheet. Do not use
   `Indicate` on filled boxes (it paints them solid); use `Circumscribe`.
6. **Sample, full render, QA, REVIEW.md**: `python -m explainer.build videos/<id> -q l` for a 480p
   draft, then `python -m explainer.build videos/<id> --burn` for the 1080p60 cut with the bilingual
   subtitles burned in; AGENTS.md's content gates apply. Owner's listening review is waived (AGENTS.md); quote the waiver.
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
