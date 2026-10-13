# Sources and evidence

All claims were verified in this repository's own `.git` on 2026-10-13, in the producing
checkout (JunyiZhou-Conny/Explainer_Videos):

- **A branch is 41 bytes.** `wc -c .git/refs/heads/main` → `41`. Content: forty hex
  characters naming a commit, plus one `\n`. The SHA shown on screen in s02,
  `88adfade790f726ed5b1b0941043708ec9fed18e`, is the repository's real `main` after
  [PR #10](https://github.com/JunyiZhou-Conny/Explainer_Videos/pull/10) merged.
- **A merge commit has two parent lines.** `git cat-file commit 88adfade…` →
  `tree 54789206…`, `parent 6b697f98b7542e44977b14f6fcb6da363863998d`,
  `parent 7548c0756c4dba2879c04f2ef6c0373016097684`. s06 shows these abbreviated.
- **Commit anatomy** (snapshot + parent name) and the behavior of `git branch`,
  `git switch`, `git merge` follow the Git Book, "Git Branching — Branches in a Nutshell"
  (https://git-scm.com/book/en/v2/Git-Branching-Branches-in-a-Nutshell), cross-checked
  against the real cat-file output above.
- The short node names in the graph diagrams (`a1f3c2` etc.) are illustrative labels for a
  generic history, not commits of this repository; the production notes in `script.json`
  forbid relabeling them as real.
