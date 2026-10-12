---
name: conny-explainer-video
description: Create Conny's narrated explainer videos using saved visual presets, production specifications, and bilingual subtitles. Use when asked to make or revise an explainer video, reuse a named video style, or turn a reference video into a reusable preset.
metadata:
  owner: conny
  version: "1.1.0"
---

# Conny's explainer videos

In a video-incubator checkout, use this repository version as the shared source of truth; personal installations are snapshots. Resolve paths relative to this `SKILL.md`. Read [defaults.json](defaults.json), then the requested `presets/<preset>.md`. Use the saved preset when none is specified. List actual preset files when asked what is available; distinguish observed reference features from proposed design choices.

Use this precedence: **current explicit request → saved episode specification → defaults.json**. A style changes visual choices, not the topic, duration, narration language, or subtitle requirements unless the user says so. Do not ask the user to repeat saved preferences. Missing optional details can use sensible defaults; ask only about a choice that materially blocks the requested result.

## Production

1. **Evidence.** Inspect the actual topic sources. For local folders or skills, separate configuration, executable tools, instructions, caches, and provenance evidence. Unknown authorship stays unknown. For visual references, keep timestamps and observation notes; metadata, transcripts, and thumbnails alone do not establish full viewing.
2. **Script and storyboard.** Save an episode specification and a snapshot of the selected preset (`style.md`) with the resolved preset, duration, dimensions, frame rate, languages, sources, and output directory. Write narration and Chinese translation with scene-level timing. Let explanations build one idea at a time. Read paths as understandable words while retaining exact spelling on screen.
3. **Design.** Apply the selected preset's layout, typography, palette, motion, diagram conventions, and exclusions. Preserve readable captions and continuity between scenes. Use original assets and layouts guided by the observed design principles. Record which reference traits informed the choices.
4. **Render.** Check the available production tools and the configured workspace/runner in `defaults.json`. Use an existing verified runner when available; inspect its arguments before execution. The installer is not a renderer. If no runner is configured, inspect the production workspace and establish a working render route. Preview a representative narrated segment before producing the full episode. Continue through the requested complete video; a preview does not replace it.
5. **Quality review.** Measure the encoded duration, resolution, frame rate, and audio. Listen to the narration; inspect pronunciation, missing or silent clips, and music balance. Check both subtitle languages against the script and their timing, wrapping, contrast, and safe margins. Inspect each scene boundary and play the complete output for pacing, motion, factual content, and continuity. Repair concrete defects before delivery.
6. **Deliver.** Provide the playable video and its actual path, plus the episode specification, script, editable source, subtitle files, and source/evidence notes. Report what was rendered and reviewed, and any unresolved limitations. Rendering does not establish publication or user approval.

Keep generated media and episode-specific source outside this installed skill. Update saved preferences only when the user asks to change future defaults. A one-video override belongs in that episode's specification.

For installation, cross-agent invocation, and where to edit preferences, read [references/cross-agent-use.md](references/cross-agent-use.md). The workflow does not require a particular model, provider, renderer, or paid service; use tools that meet the selected specification and are available in the executing environment.

For the available checkout rendering engine, episode scaffold and commands, read [references/local-production.md](references/local-production.md). `scripts/new_episode.py` resolves the saved brief; `scripts/render.py` runs an authored episode. Neither substitutes for designing the new topic's scenes. Available presets: `3b1b`, `swiss`, `cassette-futurism`, `de-stijl`, `bauhaus`, `nasa-punk`, `rhine-lab`, and `pixel-studio`.

When work spans agents or sessions, use [references/production-handoff.md](references/production-handoff.md) to keep design decisions and verification attached to the episode.

For short prompts and the style lifecycle, read `docs/VIDEO-WORKFLOW.md` and `docs/STYLE-LIFECYCLE.md` in the production checkout. Shared changes belong in this versioned bundle; episode experiments stay with the episode.
