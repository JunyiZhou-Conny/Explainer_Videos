# One shared recipe, multiple agents

The version-controlled `skill-library/conny-explainer-video/` folder in the video repository is
the source of truth. Edit it on a branch and share the commit. Each agent still needs its own
rendering tools, permissions and runtime; a skill does not transfer account sessions or desktop control.

## Use a checkout (recommended)

Clone the repository and open that folder in your agent. `AGENTS.md` points to this skill;
`CLAUDE.md` imports those instructions. The project `.agents/skills/conny-explainer-video` and
`.claude/skills/conny-explainer-video` entries are relative symlinks to this same folder, so they
move with the checkout. Check the actual skill picker in your client. If its environment does
not discover symlinks or repository skills, this prompt works without installing a personal copy:

> Read AGENTS.md and skill-library/conny-explainer-video/SKILL.md in this repository. Use that
> version. Explain Git branches for a beginner in NASA-punk style, using the saved video defaults.

Codex, Cursor and Claude Code provide skill discovery, but command syntax and precedence can
vary by client/version. Prefer its actual picker. Typical invocations are `$conny-explainer-video`
for Codex and `/conny-explainer-video` for Cursor or Claude Code. If both a personal snapshot and
the repository skill exist, explicitly request the repository version when working here.

References: [Codex](https://learn.chatgpt.com/docs/build-skills),
[Cursor](https://cursor.com/docs/skills), [Claude Code](https://code.claude.com/docs/en/skills).

## Optional personal snapshot

For invoking the recipe outside this checkout, the additive installer can create
`~/.agents/skills/conny-explainer-video` and a Claude alias at
`~/.claude/skills/conny-explainer-video`. Run from the repository root:

```bash
python3 skill-library/conny-explainer-video/scripts/install.py
python3 skill-library/conny-explainer-video/scripts/install.py --apply
```

The first command is a dry run. It refuses conflicting paths and edited or different prior
installations; it does not overwrite existing skills. `--home` accepts an existing temporary
home directory for testing. Its manifest records copied hashes and origin, not client discovery.
A personal installation is a snapshot, not a second authoring source or automatic sync.

If a previous version already exists (including Conny's earlier Mac installation), use the
repository entry point now. Compare local edits before planning any personal upgrade. Do not
use a force overwrite or duplicate the skill in every agent directory. Pulling the repository
updates its project aliases, but does not mutate personal snapshots or remote machines.

## Preferences and moving between machines

Shared future defaults live in `defaults.json`; shared style guidance lives in `presets/`.
The current request overrides a saved episode, which overrides shared defaults. A temporary
experiment belongs in the episode. Commit intended shared refinements with a reason and sample.

`production.workspace` is `null` for portability. Helpers locate a checkout from the episode,
current directory or skill location. Pass `--workspace` or set `EXPLAINER_WORKSPACE` when needed.
Do not commit machine-specific absolute paths or credentials. Remote/cloud agents must clone
and set up their own checkout; a Mac installation does not configure them.

Before starting a long job, ask each intended agent for a brief and check the loaded skill path,
preset, duration and languages. Then render a representative sample with that runtime. File
placement, client discovery, invocation and successful rendering are separate checks.
