# Add, test, and refine a video style

A preset saves the design decisions you would otherwise explain in every prompt: layout, typography, palette, motion, diagram behavior, and things to avoid. Keep reusable decisions in [the skill's presets](../skill-library/conny-explainer-video/presets/). Keep the topic, script, one-off changes, and rendered files in the episode.

The repository is the versioned source of truth for shared styles. Agents should read the same preset file, rather than maintain separate descriptions in their private chat histories.

## What is available now

| Preset | Useful visual language | Evidence of implementation |
| --- | --- | --- |
| `3b1b` | Dark backgrounds, semantic color, geometric explanations, intuition before formulas | Existing repository episodes use this pedagogical approach and the `video.yaml` toolkit. The name denotes inspiration, not affiliation or an exact reproduction. |
| `swiss` | Clear grids, large type, cream/black/red, connected diagram transformations | `videos/skills-ecosystem/` supplies a complete authored episode and rendered sample of the workflow. Read its review record for the checks actually performed. |
| `cassette-futurism` | Physical controls, CRT displays, meaningful state changes | Written design preset; representative original episode still needed. |
| `de-stijl` | Unequal orthogonal planes, primary colors, relationships shown through partitions | Written design preset; representative original episode still needed. |
| `bauhaus` | Geometric construction and deliberate typographic composition | Written design preset; representative original episode still needed. |
| `nasa-punk` | Functional aerospace panels, identifiers, equipment modules | Written design preset; representative original episode still needed. |
| `rhine-lab` | Warm scientific archive, selection, glass depth, layered inspection | Written design preset; representative original episode still needed. |
| `pixel-studio` | Original pixel characters, a workroom, visible briefs and review handoffs | Written design preset; representative original episode still needed. |

These are not eight interchangeable renderer themes. A usable description can exist before working scene code. Existing rendered episodes do not prove that every new combination of topic, style, resolution, or narration language works.

## Give the agent references and a reason

A link plus “I like this” is a useful start. A few timestamps make the result much more precise:

```text
Reference: [video URL]
00:18–00:27: I like how the camera follows one object into the next diagram.
01:04–01:15: Keep this strong hierarchy between large labels and small IDs.
02:10–02:20: Avoid this fast flashing transition.
Use case: short explanations of software systems.
Preserve: our English narration and Chinese/English captions.
```

Provide the page or video, its creator if known, and the specific qualities you want to reuse. Useful additional material includes a permitted still, a font or asset license, your own drawing, and examples that show what you dislike. A playlist can be an index; select a few representative moments before claiming it defines a coherent style.

If the agent cannot inspect a video, it should state that limitation and work from the material it can actually see. A title, transcript, thumbnail, or a few sampled frames does not establish full visual and audio review.

## Prompt: ingest a new style

> Use this repository's conny-explainer-video skill. Add a reusable preset called `instrument-notebook` from these references: [links]. I like the annotated drawings at 00:40–01:05 and the calm object transformations at 02:10–02:30. Review the accessible references, record the timestamps and coverage, and separate observed traits from your proposed production values. Write the preset and source notes. Create an original 20–30 second narrated sample explaining one input passing through a process, using our usual bilingual captions. Revise the preset after reviewing the sample. Keep the current default style unchanged and report the actual implementation and review status.

The name in that prompt is a proposed new preset, not an existing option. Choose a short lowercase hyphenated ID and use it consistently in the filename, episode specification, and documentation.

If you want only a proposal, replace the sample instruction with: “Create the preset and a storyboard only; do not render yet.” Otherwise, the sample is where design decisions become testable.

## Turn observations into a useful preset

Use this structure for `skill-library/conny-explainer-video/presets/<id>.md`:

1. **Purpose.** The kinds of explanation the style helps; one sentence about its defining behavior.
2. **Sources and review coverage.** Creator/title/URL, dates or versions where relevant, useful timestamps, and what was inspected: playback, sampled frames, transcript, or source code.
3. **Observed design grammar.** Composition, hierarchy, camera behavior, transitions, how objects reveal information, and the role of sound.
4. **Original implementation choices.** Explicit palette, font candidates and licenses, sizes at the target resolution, spacing, caption reserve, and initial timing values. Do not present chosen values as measurements from the reference.
5. **Teaching recipes.** How to introduce an object, explain a relationship, transform a state, compare alternatives, and recap. Include a small example with original content.
6. **Exclusions and boundaries.** What would make it a generic recolor or damage readability; which adjacent styles it should remain distinct from.
7. **Acceptance criteria.** Observable checks for the sample: what the viewer can follow, read, and understand.
8. **Implementation status.** Sample path, renderer used, reviewed version, checks performed, and unresolved limits.

For example, “make it futuristic” is too vague. “The selected archive slab moves forward, neighboring slabs dim, and its layers separate while labels remain anchored” gives the implementer a testable scene behavior.

Extract design principles into original scenes. Keep third-party reference videos, game artwork, logos, music, and full downloaded reference collections out of a public commit unless their redistribution is permitted. Record links and original analysis instead. A repository's access permission and an asset's reuse license answer different questions.

## Test one difficult scene before a full episode

Choose a sample that includes:

- a concrete object or diagram, with a meaningful state change;
- typical heading and label density, including the longest likely label;
- narration and both caption languages at the final intended size;
- the defining style behavior, such as connected planes, a physical control, or archive depth;
- a transition into or out of that scene.

Inspect the encoded sample at full size and a small viewing size, and listen to it. A still image can establish layout but cannot establish pacing or speech quality. For a spatial style such as Rhine Lab, record whether the sample uses actual 3D geometry or a 2D interpretation.

When reviewing, write concrete findings: “At 00:08, the Chinese subtitle intersects the module label,” or “The status lamp changes before the operation it describes.” Fix those issues, re-render the affected sample, and record the result. Do not claim a preset is production-tested because its Markdown file validates.

## Keep status honest

Use these labels in the preset's notes or its linked review record. They describe distinct evidence, not a compulsory approval ceremony.

| Status | What it establishes |
| --- | --- |
| Draft | A candidate specification exists. |
| Reviewed design | References and the proposed rules have been inspected; record reviewer and scope. |
| Rendered sample | A playable sample exists using identified scene code and renderer. |
| Technically checked | Named checks passed, such as decoding, resolution, frame rate, duration, and subtitle bounds. |
| Human reviewed | A person watched/listened to the named version; record their findings. |
| Released | The identified files are actually available at the linked publication or repository release. |

These labels can coexist. An episode can be technically checked and released while still having a documented lack of human listening review. Preserve that distinction instead of describing it as universally approved.

## Prompt: refine an existing preset

> Refine the `swiss` preset using the latest episode's review. At 01:20–01:45 there are too many unrelated fades, and the small path labels are hard to read. Preserve the palette and grid. Add stronger rules for connected object transformations and readable path labels. Demonstrate the changes on one representative scene, compare before and after, and update the versioned preset and change notes. Keep the original episode render available; do not regenerate other episodes automatically.

For a style variation that should stay local:

> Use `nasa-punk` for this episode, but replace the accent orange with muted blue and remove surface wear. Record those overrides in the episode brief. Keep the shared preset unchanged.

If the variation repeatedly proves useful, ask to promote it into a named preset or revise the shared one. Keep the smallest coherent distinction: two different colors alone rarely need two complete workflow skills.

## Version styles without losing past decisions

Git records the exact preset and production source. Each episode should record the preset ID, the source commit or an equivalent version/hash, and its own deviations. Until a commit exists, mark the source version as pending rather than inventing one.

For a shared change:

1. Inspect the current preset and representative episode; preserve any uncommitted work.
2. Update the rules and source evidence together. Record the reason and the affected behaviors in the change description.
3. Render and review a sample appropriate to the change. A wording fix may need only a document check; a motion or layout change needs a visual sample.
4. Commit the preset, necessary source, and review notes together. Use a branch and pull request when the change needs review across agents.
5. Let future episodes select the new version. Revise older episodes only when requested, keeping their previous specifications and outputs traceable.

An installed personal skill can diverge from the repository. Compare those differences before replacing it, bring useful changes back through the repository, and then update each installation deliberately. Do not solve divergence by silently maintaining several competing “canonical” copies.

## Share the workflow, not only the look

Keep these responsibilities separate in the repository:

| Resource | Responsibility |
| --- | --- |
| `SKILL.md` | The repeatable evidence → script → design → render → review → deliver workflow. |
| `defaults.json` | Preferences for new episodes, independent of topic. |
| `presets/<id>.md` | Visual and motion decisions that can be reused across topics. |
| Skill references and scripts | Production interfaces, setup guidance, and deterministic helpers. |
| `videos/<episode>/` | Resolved brief, sources, script, scenes, overrides, and review for one episode. |
| A release or published artifact | The specific finished files shared with viewers. |

This is how a successful workflow becomes a skill: save the stable sequence, encode repeated choices once, keep tools executable and documented, test it on a new topic, and improve it from specific failures. Another agent can then use a short request because the detailed instructions travel with the repository.

## External renderer candidates

[Multiplane](https://github.com/LBEILC/Multiplane) (Apache-2.0) is the designated candidate
for a future 3D/parallax/alpha scene route: a deterministic headless-Chromium HTML renderer
built for agents, with pixel-exact `verify`, alpha WebM/ProRes output, and segment-level
resume. Evaluated 2026-10-17 against this pipeline: rendering is not our bottleneck, and it
ships no TTS, captions, music or validation, so adopting it wholesale was rejected. Its two
transferable ideas were implemented natively instead (`explainer.golden` golden-frame
regression; the caption-band checks in `explainer.check` and `explainer.style_check`).
Revisit as an optional `episode.py` scene type (an alpha video track with Python-computed
timings injected) only when all three hold: a concrete episode needs 3D/parallax; the
project has reached 1.0 or shown ~6 months of continued maintenance (it was days old at
evaluation, single-maintainer, Node >= 24); and a narrated proof scene with CJK text passes
sample review, as this lifecycle requires of any new route.
