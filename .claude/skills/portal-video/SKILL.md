---
name: portal-video
description: Make the weekly 项目周记 build-log videos that explain, without code, what Conny's pull requests in the private InternationalHealthportal repository did that week (the triage chat, its harness, its UI), for the founder who directs the agents. Use for the Friday-evening weekly run (plan and produce the week's batch without waiting for approval), to plan a batch from the PR digest, or to produce, fix or continue one portal-eN episode.
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

## W. The weekly run (every Friday evening, Boston)

A scheduled task starts a fresh session every Friday at 21:17 Boston time and points it here. The
owner chose (2026-10-31) 「周五晚上」「全自动」「一个常驻 issue」: plan and produce the week's batch
without waiting for his approval, and keep his questions in the standing issue
[#72](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/72). His words for the series:
「每当agent完成了很大的一部分……进行一波视频的总结，可以按照每周做好几集」.

1. **Set up.** §0 (access), then `docs/BOOTSTRAP.md`'s reading order. Fetch every portal branch.
   A scheduled session may start without the GitHub MCP tools; `gh` then does the same work over
   REST (GraphQL is refused inside Claude Code sessions). Ready for review is
   `gh api -X POST repos/<owner>/<repo>/pulls/<n>/ccr/ready_for_review`; review threads are
   `GET …/pulls/<n>/ccr/review_threads` and `POST …/pulls/<n>/ccr/comments/<id>/resolve`.
2. **Find the window.** Coverage says, per portal PR, the commit already explained and the
   episodes that did it, plus a *Covered through* date. It lives in two places: the table in
   `videos/portal-series/README.md` on main, and the table in the newest `WEEKLY` comment on #72.
   The comment is the one that counts when they differ, because it is posted whether or not that
   week's batch PR has merged. Reading main alone would redo a batch still waiting to merge. The
   digest runs from *Covered through* to tomorrow, Boston time; name it by the ISO week of this
   Friday. A missed week simply widens the window. New material = PRs not in Coverage, plus
   commits after the commit Coverage records for a PR. If an earlier batch PR is still open, leave
   it alone, branch from main as usual, and say in the new PR which one should merge first.
3. **Read the questions.** Every comment on #72 after the newest comment whose first line starts
   with `WEEKLY`, plus the questions that comment carried over. These come first in the plan.
4. **Digest** (§1), then decide the batch:
   - one episode per substantial thread: a PR or decision with a mechanism worth drawing, a turn
     in the week, or a question from #72; at most four, each ten minutes or less;
   - routine weeks (docs, notes, renames, small fixes) get no episode of their own: fold them into
     a sentence elsewhere, or, if nothing is substantial, skip the week (step 8 with zero episodes);
   - every question gets an episode or a written reason it waits.
5. **Plan and open.** §2's plan in the README, one *Episode request* issue per episode (labels
   `episode` and `state:scripting`, no `@claude` line), and a claim comment on each.
6. **One branch, one draft PR for the batch.** Use the session's designated branch, or
   `portal/<YYYY>-w<NN>` when none is given (never `episode/<slug>`: CI limits those branches to
   one episode folder). Title `项目周记 <YYYY>-w<NN>: E<a>–E<b>`. The PR body says `Refs #N` for
   each episode issue, **not** `Closes`: a closing keyword shuts the issues at merge, before the
   release has reported back. Each episode's `REVIEW.md` links its own issue; release-on-merge
   uses that link to tell the publish worker where to report. Subscribe to the PR's activity and
   handle CI and review bots as they arrive.
7. **Produce each episode** with §3, all of it: accuracy pass, newcomer pass, frame passes, final
   burn, the caption pair read, `REVIEW.md` with the listening waiver quoted. `CHECKPOINT` on the
   issue at each stage boundary (AGENTS.md), pushing first. Independent reads (accuracy, viewer QA)
   can run as parallel subagents.
8. **Close the week.**
   - Update the README (plan table; Coverage rows with the commits now explained; *Covered
     through* set to today), `GLOSSARY.md` and the week file; index last week's released episodes in `catalog/videos.json` and
     `docs/VIDEOS.md` if they are missing (the site lists a release without them, but the
     catalog carries checksums and durations).
   - When CI is green and every bot thread is answered, mark the PR ready for review (MCP
     `update_pull_request` with `draft: false`). Never merge: the owner's merge is the release.
   - Comment on #72, first line `WEEKLY <YYYY>-w<NN>`: each question and the episode that answers
     it, the questions carried over and why, the PR to merge, the batch's total minutes, and the
     full Coverage table with its *Covered through* date (the README's, after this week's rows).
     A skipped week posts the same comment with the reason and the Coverage unchanged except the
     date.

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

- Collect the owner's questions: the new comments on #72 (or what he asked in chat), quoted in
  the batch plan, plus the visible things the week added to the product.
- Group into one to four episodes, each answering one question raised by something on screen.
  Write the plan into `videos/portal-series/README.md` (episode table + one paragraph per episode:
  the question, the PRs and files, the terms it names, the ponder questions).
- Open one *Episode request* issue per episode, body citing `videos/portal-eN-<topic>/` and the
  branch, **without** the `@claude` line (it wakes a separate agent per issue; the batch session
  produces them itself). Add each to the plan's table.

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
   clean; preview at 480p (`python -m explainer.preview`) and read every contact sheet. The Manim
   traps that cost E2–E6 a render each are under *Pitfalls*.
6. **Sample, full render, QA, REVIEW.md**: `python -m explainer.build videos/<id> -q l` for a 480p
   draft, then `python -m explainer.build videos/<id> --burn` for the 1080p60 cut with the bilingual
   subtitles burned in; AGENTS.md's content gates apply. Owner's listening review is waived (AGENTS.md); quote the waiver.
   Before calling the captions done, read the burned pairs one by one (`output/*.zh-en.srt` or the
   frames): each Chinese line must sit over its own English clause (see *Pitfalls*). REVIEW's
   Verified section states only what was measured on the final file.
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
- **Anchors match the narration verbatim.** `vo.wait_until("…")` searches the raw SAY text,
  case-insensitively but otherwise exact: "one-six-three" never matches "one six three", and a
  missed anchor silently plays the animation late. Anchor on plain words.
- **Bilingual pairs follow clause stops.** The caption splitter cuts the English at a comma or
  period near where the Chinese line breaks; with no stop there, it repeats the whole English
  sentence under each Chinese piece. Keep the two languages in the same clause order, give long
  English sentences a mid-sentence comma, or split the sentence in both languages. A length
  heuristic does not catch a pair that is one clause off; reading the pairs does.
- **Manim:** `Indicate` paints a filled box solid (press it, then `Circumscribe`); an
  `always_redraw` object needs `clear_updaters()` before it fades, or it redraws itself back;
  `DashedLine` has no points of its own, so `point_from_proportion` crashes at 1080p only (work
  from `get_start()`/`get_end()`); dimming filled shapes with `set_opacity` behind a ponder card
  leaves grey patches, so clear the screen for a ponder and redraw after it.
- **Releases follow the merge.** release-on-merge starts one release per new episode spec; the Mac
  worker uploads one per run. A v2 is a manual dispatch and a second Bilibili upload, so fix
  before merging, not after.
