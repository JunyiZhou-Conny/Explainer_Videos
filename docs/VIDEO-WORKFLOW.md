# Make a video from an idea

Open this repository in your agent, choose a saved style, and describe what the viewer should understand. You do not need to repeat the visual specification every time. The reusable recipe lives in [conny-explainer-video](../skill-library/conny-explainer-video/SKILL.md); the episode folder records the choices for one video.

## The everyday prompt

Copy this, replacing the topic and source:

> Use the conny-explainer-video skill in this repository. Make a video explaining Git branches for someone who has used Git but does not understand branching. Use the `nasa-punk` preset and saved production defaults. Use the source code and examples in the attached project as evidence. Show one change moving through two branches and a merge. Build a representative narrated sample, fix the issues it reveals, then complete the video. Deliver the MP4, bilingual subtitles, editable source, and review notes.

An even shorter request works once the context is clear:

> Make a Swiss explainer of this folder for a beginner. Use our saved defaults and explain what each important part does with one concrete example.

The agent should read [AGENTS.md](../AGENTS.md), the skill, and the selected preset. If the application does not discover the skill automatically, explicitly give it `skill-library/conny-explainer-video/SKILL.md`. A skill supplies instructions; the executing agent still needs filesystem access, rendering tools, and any account access required by the task.

The saved defaults for new preset-based episodes are **five minutes, 1920 × 1080, 30 fps, English narration, and Chinese subtitles above English**. Existing episodes keep their own settings. Your current request overrides the episode specification, which overrides saved defaults.

> Use `rhine-lab`, make this episode two minutes, and keep the usual narration and subtitles. These are overrides for this episode only.

Changing the requested duration or language does not prove the renderer supports it. The agent must select and verify a suitable route. The newer `episode.json` engine currently supports English narration and the 1080p30 layout; existing language-version tooling has a separate documented route in [LANGUAGES.md](LANGUAGES.md).

## What to provide

Three things are usually enough to start: **the idea, the audience, and the evidence**. Name a style when you want something other than the default.

| Provide | Example | Why it matters |
| --- | --- | --- |
| Learning objective | “Explain why a branch is a reference, then demonstrate a merge.” | Gives the video one clear destination. |
| Audience and assumed knowledge | “I know `git add` and `git commit`; I have never used branches.” | Controls how much background to explain. |
| Topic sources | Repository files, a paper with relevant pages, notes, or links | Supports the claims and concrete examples. |
| Style | `swiss`, `3b1b`, `nasa-punk`, or another saved preset | Reuses layout, motion, typography, and diagram conventions. |
| Overrides, if any | Two minutes; vertical format; slower delivery; a particular pronunciation | Records the exceptions for this episode. |
| Must include / exclude | “Show the actual command; skip advanced rebasing.” | Keeps the scope useful. |
| Intended destination | Personal study, a class, Bilibili, or a public release | Helps choose aspect ratio, packaging, and companion material. |

For a **paper**, provide its title/link or permitted file, the question you care about, and relevant pages. For a **codebase**, identify the checkout and the feature or execution path to explain. For a **folder audit**, give the relevant directory and ask the agent to separate observed provenance from unknown authorship. For a **new visual style**, provide reference links and timestamped moments you like; see [STYLE-LIFECYCLE.md](STYLE-LIFECYCLE.md).

Share only the files needed for the episode. References can stay as links when redistribution is not appropriate. A public video about a personal folder should use a deliberately chosen example or redacted view, rather than displaying a full private inventory.

## A fuller brief when the idea is complex

This is an input template, not another paragraph you must write for every video:

```text
Use this repository's conny-explainer-video skill.
Episode: git-branches
Audience: beginner who can commit changes
Objective: understand branch pointers and one ordinary merge
Sources: the attached demo repository and its commit history
Style: nasa-punk
Specifications: saved defaults
Must show: two branches, one new commit, one merge, exact commands
Skip: rebase, cherry-pick, remote collaboration
Tone: calm, concrete, one concept at a time
Deliver: complete video, subtitles, script, scenes, source notes, review
```

Missing optional choices should use saved defaults or reasonable choices recorded in the brief. The agent should ask about a material ambiguity while continuing independent work; it should not require you to restate the entire style.

## What the agent does

1. **Inspect the sources.** Identify the facts the episode will teach. Record file paths, paper pages, or web references. Keep uncertainty visible.
2. **Save the brief and storyboard.** Resolve settings into the episode specification. Pair each narration beat with something the viewer can see happen.
3. **Author the script and scenes.** Write English narration and a faithful Chinese translation. Keep the chosen visual grammar consistent while building diagrams for this topic.
4. **Render a representative sample.** Choose a segment containing the hardest diagram, motion, and caption layout. Inspect and listen; use what it reveals to improve the full episode.
5. **Complete the video.** Render the remaining scenes, assemble narration, and generate the captions and companion files.
6. **Review and deliver.** Check facts, pronunciation, pacing, visuals, subtitle readability, and encoded media. Record what was actually checked and any remaining limits.

A sample is part of producing the complete requested video. If you want to stop after the sample, say so explicitly. A style preset is a design specification: selecting `rhine-lab` still requires an authored archive sequence and tested scene code.

## One-time setup versus each episode

Clone the repository and open it as the agent's workspace. Follow [local production setup](../skill-library/conny-explainer-video/references/local-production.md) for the newer engine, or [the existing paper-video workflow](WORKFLOW.md) for a `video.yaml` project. Setup installs the required runtime and retrieves the documented fonts and voice assets. Installing the skill by itself does not install those dependencies.

The repository holds the shared skill source. Repository skill aliases make that source available to compatible agents; see [cross-agent use](../skill-library/conny-explainer-video/references/cross-agent-use.md). A personal installation is a snapshot and may have local edits. Compare it with the repository before updating it. Cloud or remote agents need access to the same repository version and their own working runtime.

For everyday work, the agent can perform the commands. These examples are run **from the repository root** after setup:

```bash
# New engine: create an editable brief, not a finished movie.
python3 skill-library/conny-explainer-video/scripts/new_episode.py git-branches \
  --topic "Explain Git branches" --preset nasa-punk --workspace .

# After script.json and scenes.py have been authored:
python3 skill-library/conny-explainer-video/scripts/render.py videos/git-branches --sample s01
python3 skill-library/conny-explainer-video/scripts/render.py videos/git-branches
```

The scaffold refuses an existing episode directory so that a new request does not overwrite previous work. To revise an existing episode, ask the agent to inspect that directory and edit its actual sources.

Two production formats coexist:

| Route | Episode files | Render command | Use it for |
| --- | --- | --- | --- |
| Existing toolkit | `video.yaml`, `script.md`, `scenes/` | `.venv/bin/python -m explainer.build videos/tictactoe-255168` | Existing dark-diagram episodes and their established language workflow. |
| New preset workflow | `episode.json`, `script.json`, `scenes.py` | Skill's `scripts/render.py` helper above | New authored preset-based episodes; `skills-ecosystem` is a complete Swiss example. |

Read the episode's own specification before rendering. Do not rename one format into the other or assume the older 1080p60 defaults equal the newer 1080p30 defaults. Choose the route that supports the episode and preserve it unless a migration is deliberately implemented and tested.

## Revise a video or change future preferences

Useful revision prompts refer to the effect you want and, when possible, a timestamp:

> In `git-branches`, at 00:42 the branch pointer moves before the explanation. Hold it until “the branch now points here,” then animate the move. Keep the script, other scenes, and preset unchanged. Re-render the affected section and verify the final caption timing.

> Make the typography larger and the pacing slower for this episode only. Record the changes in its specification; keep the shared Swiss preset unchanged.

> For future videos, change the default duration to four minutes. Update the versioned defaults and documentation, while preserving specifications already saved for existing episodes.

Style-wide changes use the lifecycle in [STYLE-LIFECYCLE.md](STYLE-LIFECYCLE.md). A successful one-off experiment does not become everyone's new default automatically.

## Resume with another agent

Keep decisions in files, so the next agent does not depend on a previous chat. The handoff should name:

- the episode directory, repository commit/branch, selected preset version, and production route;
- the learning objective, source references, resolved settings, and approved or settled design decisions;
- the current script/scenes, generated sample or full output, and known defects;
- which checks ran, which require listening or full playback, and the next concrete task.

One agent may research and script, another may implement scenes, and another may inspect the rendered artifact. Assign distinct file ownership if they work concurrently. Designate one agent to assemble changes and maintain the episode record.

> Continue `videos/git-branches`. Read its brief, storyboard, source notes, and review notes first. Inspect the current sample. Finish the remaining scenes using the recorded NASA-punk design, then render and review the full episode. Preserve the existing sources and report any necessary deviation.

The final handoff should link the actual playable video, editable sources, subtitle files, and review record. It should distinguish **draft**, **reviewed sources/design**, **rendered**, **technically checked**, **human reviewed**, and **released**. These are separate facts: successful encoding cannot establish listening quality, and a local render cannot establish publication. Follow the user's requested scope for uploading and identify the actual release or destination when it is published.
