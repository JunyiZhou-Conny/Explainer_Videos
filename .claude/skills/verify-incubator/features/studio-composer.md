# Studio new-episode composer

On `new.html` Conny describes an episode (question, audience, sources, style, length, scope, who
will make it). 生成 issue → opens GitHub's new-issue form prefilled with the `episode-request.yml`
template. When a person or a non-default agent will claim the episode, it adds a dispatch note
telling automatic agents to stand down and shows the kickoff prompt to paste into that agent.

## Sub-features

- `composer-required` refuses to open an issue until question, audience and sources are filled (alert 问题、观众、素材三项必填。).
- `composer-issue` opens `github.com/JunyiZhou-Conny/Explainer_Videos/issues/new` with `template`, `title`
  (`[episode] ` + first line of the question), `question`, `audience`, `sources`, `style` and the optional `length` and `scope`.
- `composer-dispatch` appends `Dispatch: … automatic agents must not claim it.` to `sources` for the two manual choices.
- `composer-prompt` shows the kickoff prompt (`Read docs/BOOTSTRAP.md …`) for manual choices, or on 复制 kickoff prompt.

## How to get to it (user POV)

- Choose `新视频` in the Studio navigation.
- Open `new.html` directly.

## Driving it with control.py

Preconditions:

- `$C studio-up --run $RUN` printed `READY …`. Any data mode works, `--offline` included: this page reads no data.

- **Composer journey.** Run `$C browse --run $RUN --name composer .claude/skills/verify-incubator/features/steps/composer.json`.
  Every step prints `ok` and the exit code is `0`.
- **Required fields.** Choose 生成 issue → on the empty form. The `dialog` step catches an alert containing `三项必填`.
- **Prefilled issue.** Fill the three fields, choose `GPT / Cursor / 其他`, then choose 生成 issue →. The `popup` step
  catches the new window. `evidence/composer-issue.json` has `template` `episode-request.yml`, title
  `[episode] 为什么 git 分支几乎零成本？`, the audience text, and `sources` ending with
  `Dispatch: this episode will be claimed manually (a non-Claude agent); automatic agents must not claim it.`
- **Kickoff prompt.** After that click, `#promptText` is visible. `evidence/composer-kickoff-prompt.txt` starts with
  `Read docs/BOOTSTRAP.md in JunyiZhou-Conny/Explainer_Videos`.
- **Proof.** Open `evidence/composer-composer.png` and `composer-composer.aria.txt`. The form keeps the entered values,
  and the prompt box is shown below the buttons.

## Gotchas

- github.com is stubbed inside the browser (`browser.cjs` answers every github.com request with `stub`), so a
  proof never reaches GitHub. Never drive this page with the stub removed: the real form is one click from a
  real issue that summons agents.
- With the default `@claude 自动接单` choice, the page shows no prompt and adds no dispatch note. Assert the
  absence of both, not their presence.
- The style dropdown preselects `swiss (ready)`, and an empty style falls back to `swiss (ready)` in
  `openIssue()`. The saved default for new episodes is `3b1b` (`defaults.json`, AGENTS.md since 2026-10-30).
  The journey records the `style` it sees in `composer-issue.json` and does not assert either value. Report
  the mismatch rather than editing the journey to hide it.
- 复制 needs clipboard permission, which headless Chromium lacks. The page then shows an alert (复制失败…).
  Prove the prompt through `#promptText`, not through the clipboard.
