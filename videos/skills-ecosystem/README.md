# One Skill Library, Three Coding Agents

[Download the five-minute video](https://github.com/JunyiZhou-Conny/Explainer_Videos/releases/download/incubator-2026-10-12/skills-ecosystem.mp4).

An original Swiss-style explainer of skill instructions, tools, agents, local folder roles,
provenance, shared discovery and a repeatable production workflow. English narration with
Chinese above English captions; 1920×1080 at 30 fps.

- [Episode specification](episode.json) and [frozen style](style.md)
- [Readable script](script.md), [structured narration](script.json), [editable scenes](scenes.py)
- [Source notes](SOURCES.md), [review and limitations](REVIEW.md), [subtitle files](delivery)

After following the repository setup guide, render a sample from the checkout root:

```bash
python3 skill-library/conny-explainer-video/scripts/render.py videos/skills-ecosystem --sample s01
```

Omit `--sample s01` for the full video. The original release predates public packaging;
see SOURCES.md for metadata changes and reproducibility limits. Local inventories and
third-party reference media are intentionally outside this public example.
