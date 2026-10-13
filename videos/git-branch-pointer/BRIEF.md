# Brief: Why is a git branch almost free?

Episode request: [issue #12](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/12) —
the pipeline's first end-to-end dry run.

- **Learning objective.** The viewer leaves knowing that a branch is a 41-byte pointer file,
  that commits + parent links form the real graph, and what moves on `commit`, `switch`
  and an ordinary `merge`.
- **Audience.** Knows `git add` / `git commit`; has never branched; currently believes a
  branch is "a copy of the folder". The episode must explicitly break that belief.
- **Style / format.** `swiss` (ready style, shared components in `explainer/styles/swiss.py`),
  180 s, saved production defaults: English narration (Kokoro `af_heart`, 0.95), burned
  Chinese-above-English captions, composed score (engine default).
- **Evidence rule.** The on-screen ref-file bytes, the 41-byte size and the two-parent merge
  commit are real, from this repository itself (SOURCES.md). Abbreviated graph-node names in
  diagrams (`a1f3c2`, `5d08b7`, `c99e41`, `f7d2a9`, `2b61e0`) are illustrative labels; the
  `88adfa…` merge node and its two parents are the real ones.
- **Must include.** The actual content of a ref file; one animated commit-graph mechanism with
  two pointers moving; the exact commands (`git branch`, `git switch`, `git merge`).
- **Skip.** Rebase, remotes, detached HEAD (named in s04's ponder only as a question).
- **Structure.** s01 hook puzzle → s02 the 41 bytes → s03 commits are the graph →
  s04 commit moves one pointer (mechanism + ponder) → s05 switch = move HEAD →
  s06 merge = one commit, two parents (real proof) → s07 recap + try-it-yourself.
