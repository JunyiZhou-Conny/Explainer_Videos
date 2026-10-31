# Brief: Copying Claude's chat page (项目周记 E3 · 照着 Claude 抄)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · issue
[#60](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/60) · 3Blue1Brown style, now the
house default (owner, 2026-10-30: 「开始做下一集 E3 吧，以后默认用3blue1brown的style」).

- **Question.** Conny, 2026-10-30: 「包括这个 UI 的设计……我能在这个之上再去创新什么……主流的对这种 chatbot UI 的一些设计……
  我们在哪些地方进行的模仿，我们是怎么达成的，还有什么可以做的」.
- **Learning objective.** The viewer can name the parts of a mainstream chat page (empty state,
  suggestion chips, composer, model menu, send/stop key, user bubble, answer column, action row,
  scroll-to-latest, disclaimer line); say what decision 0006 decided and why (one reference per
  screen, copied one-to-one, no mixing) and which part he decided himself (the colours and serif);
  sort the page's features into copied / not copied (and why) / added for safety and for parents;
  retell how the agents built it in PR #41; and name what mainstream apps have that we do not, and
  what only this product could do.
- **Audience.** Conny after E1–E2. Uses Claude's app and ChatGPT daily, so the comparison is concrete;
  knows the receipt, progress streaming and the early 911 warning (E2). Reads Python, not TypeScript.
- **Style / format.** `3b1b`, `video.yaml` route as in E2: 1080p60, Kokoro `af_heart` 0.95, music,
  Chinese-above-English subtitles burned in. Target 8–9 minutes, 1,150–1,300 words.
- **Evidence rule.** The page is redrawn in its own colours (the hex values in `docs/design/README.md`)
  with verbatim strings from the portal source at `b7ab98e`. What was copied from Claude's app is
  taken from our own design doc (the agent's record of what it copied), not from screenshots of
  Claude's app; Claude's app is drawn as a grey outline with no logo or name styling. Claims about
  Claude's and ChatGPT's features come from their help centres and announcements (SOURCES.md). The
  build path comes from PR #41's commits, description and review threads.
- **Must include.** The element names on a redrawn page; decision 0006's three options and its
  choice; "copied" with the colour table scoped to this page; "not copied" with a reason each; "added
  for safety and for parents"; the path through PR #41 including the stop/send bug; what mainstream
  apps have that we don't; what we could invent; the open decisions.
- **Skip.** Streaming and the receipt in depth (E2); the agents' two days and the review bots in
  depth (E4); TypeScript.
- **Ponder questions.** Why copy one product exactly instead of the best parts of several? What
  would a parent in China need from this page that a student in Boston doesn't?
