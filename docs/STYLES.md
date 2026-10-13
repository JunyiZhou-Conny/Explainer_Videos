# Style catalog

Choose the visual grammar that helps explain the idea. The same preset can serve different
subjects; write topic-specific scenes and test a meaningful narrated segment.

A style is **ready** only when it ships its four-part contract: machine-readable tokens
(`presets/<id>.tokens.json`), a reusable components module (`explainer/styles/`), committed
reference frames (`presets/<id>.reference/`), and a reviewed sample (docs/STYLE-LIFECYCLE.md).
`explainer/style_check.py` asserts the tokens against rendered pixels; prose alone does not
make a style real. The table below is generated from [catalog/styles.json](../catalog/styles.json)
by `tools/gen_style_status.py` — edit the JSON, not the table.

<!-- styles-table:generated -->
| ID | Useful for | Read the specification | Status |
| --- | --- | --- | --- |
| `3b1b` | Math, algorithms, quantitative intuition | [Dark diagrams](../skill-library/conny-explainer-video/presets/3b1b.md) | Ready — complete episodes (legacy toolkit); example `videos/tictactoe-255168` |
| `swiss` | Folder maps, processes, evidence and comparisons | [Swiss](../skill-library/conny-explainer-video/presets/swiss.md) | Ready — complete example, technical + sampled-frame review; example `videos/skills-ecosystem` |
| `cassette-futurism` | Hardware/software, terminals and states | [Cassette futurism](../skill-library/conny-explainer-video/presets/cassette-futurism.md) | Design specification — sample pending |
| `de-stijl` | Components, partitions, allocation and relationships | [De Stijl](../skill-library/conny-explainer-video/presets/de-stijl.md) | Design specification — sample pending |
| `bauhaus` | Construction, form/function, typographic explanation | [Bauhaus](../skill-library/conny-explainer-video/presets/bauhaus.md) | Design specification — sample pending |
| `nasa-punk` | Engineering systems, exploration and equipment | [NASA-punk / Starfield](../skill-library/conny-explainer-video/presets/nasa-punk.md) | Design specification — sample pending |
| `rhine-lab` | Research, archives, retrieval and layered systems | [Rhine Lab](../skill-library/conny-explainer-video/presets/rhine-lab.md) | Blocked on renderer (needs 3D/glass compositing the engine does not provide) |
| `pixel-studio` | Making-of and collaboration stories | [Pixel studio](../skill-library/conny-explainer-video/presets/pixel-studio.md) | Blocked on renderer (needs logical-resolution integer upscaling the engine does not provide) |
<!-- /styles-table -->

Swiss has no claimed human listening review; see [its review](../videos/skills-ecosystem/REVIEW.md).
The original dark family uses `video.yaml`; the Swiss example uses `episode.json`. The styles
are conceptually reusable across renderers, but no automatic format conversion is supplied.

[Add/refine a style](STYLE-LIFECYCLE.md) · [Machine-readable catalog](../catalog/styles.json)
