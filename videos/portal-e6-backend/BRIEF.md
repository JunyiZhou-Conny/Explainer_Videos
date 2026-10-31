# Brief: How the backend stack was chosen (项目周记 E6 · 后端怎么选)

Series: [docs/PORTAL_SERIES.md](../../docs/PORTAL_SERIES.md) · batch plan:
[videos/portal-series/README.md](../portal-series/README.md) · issue
[#67](https://github.com/JunyiZhou-Conny/Explainer_Videos/issues/67) · 3Blue1Brown style (the house default).

- **Question.** The owner, 2026-10-31: 「开始做吧」, for the two PRs opened after the week's batch was planned.
  This one is InternationalHealthportal PR #43, 「后端选型提议（0006）」.
- **Learning objective.** The viewer can:
  - name the four jobs of a backend (server, database, login, run-anywhere containers) and the tool chosen for each;
  - explain the one rule that decided the language (the front end is fixed, so the back end adapts);
  - give the reason each main alternative lost;
  - say what the first data model protects (fixed roles, student-started links, read-only cards with no images);
  - retell how review caught mistakes, including the one-word unlink bug;
  - list what is still open and waits for the team's sign-off.
- **Audience.** Conny after E1–E5. Reads Python, not TypeScript; no backend experience; cares about
  parents and privacy.
- **Style / format.** `3b1b`, `video.yaml` route as in E2–E4: 1080p60, Kokoro `af_heart` 0.95, music,
  Chinese-above-English subtitles burned in. Target 7–9 minutes, 1,000–1,250 words.
- **Evidence rule.**
  - Every claim comes from `docs/decisions/0006-backend-stack.md` at `f163e90`, the PR, its comments, issue #11, or primary tool pages (`SOURCES.md`).
  - Rejected options are quoted with the record's own reasons.
  - Inferences are marked as such or left out.
- **Must include.**
  - Today's prototype keeps its data in one browser.
  - The four jobs and the choices for each.
  - The rule 「前端是固定的约束，应该是后端适配前端。」
  - Why not Python, and the Python exit.
  - Why Postgres (links are relational), with pgvector as an option only.
  - Email codes (6 digits, 5 minutes, 3 tries, hashed, rate-limited) and the rejected alternatives.
  - The data model's protections, and the review: 31 → 14, the second version's fixes, and the `revoked` bug fixed 21 s after Bugbot.
  - What stays open: China access, email provider, parent edits, retention.
  - Two product calls made inside the record.
  - The two decisions numbered 0006, flagged, not resolved.
- **Skip.** Code, config files and tool versions beyond what the record states. Hosting choices (issue #44).
- **Ponder questions.**
  - S03: You read Python. Why isn't the backend in Python? (Answered at once.)
  - S07: One missing word kept an unlinked parent's access. What would have caught it if no bot had? (Answered in S08: the record's own success test, a 403 after unlinking.)
  - S09 recap questions:
    - Why isn't the backend in Python?
    - What stops a student from making themselves a parent?
    - What would have caught the unlink bug without a bot?
