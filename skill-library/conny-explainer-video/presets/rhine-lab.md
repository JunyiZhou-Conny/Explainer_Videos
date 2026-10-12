# Rhine Lab / warm scientific archive

Use for research, layered systems, catalogs, retrieval, models, and information revealed through inspection. User explicitly selected Rhine Lab alongside Starfield/NASA-punk. References: 路北路陈's [interactive reconstruction demo](https://www.bilibili.com/video/BV1jebG6zE1E/) and the creator's [RhineLabUI source repository](https://github.com/LBEILC/RhineLabUI). This is an original explanatory design inspired by their principles, not a redistribution of Arknights imagery or a claim of affiliation.

## Reference-specific features

The demo describes a boot sequence, emblem construction, access scan, welcome transition, archive array, and selected-item closeup. Its added interactions include archive categories, scrolling IDs, search, item selection, and a 3D inspection/exploded view. The repository implements real spatial glass and typography with TypeScript/Three.js; ordinary translucent rounded cards alone miss the defining depth and selection behavior.

Use warm off-white, near-black precise type, thin rules, compact archive labels, translucent slabs, controlled depth, and a restrained warm-gold selection accent. A selected object moves forward and reveals information. Neighboring objects and the camera respond coherently. Treat the archive as an organized space the viewer can understand.

## Conny's implementation choices

Paper `#EAE5E1`, ink `#222323`, glass edge `#B9B5AC`, selected warm accent `#CFAD72`. Inter/grotesk headings plus a restrained mono for specimen IDs; Noto Sans CJK SC for Chinese. At 1080p, 72–104 px titles, 36–46 px explanation, at least 30 px meaningful object labels. Tiny technical texture is decorative only; never make an essential fact depend on it. Reserve a stable bottom 170 px caption band.

Keep the initial archive to three to five objects so selection remains legible. Glass should show thickness, edge highlights, occlusion and separation from the background. Use soft spatial shadows and subtle refraction when the renderer supports them. A 2D version must be described as a graphic interpretation, not as an equivalent reproduction of the 3D source.

## Motion grammar

1. Brief terminal/status introduction, then reveal the archive. Skip a long boot every episode.
2. Expand the array with staggered 0.1–0.2 s offsets while preserving alignment.
3. Select one object: bring it forward over 0.7–1.2 s, dim neighbors, and stop the camera.
4. Resolve a frosted/redacted layer into a readable label or document. Reveal only the information currently explained.
5. Rotate or separate layers to explain structure, maintaining a fixed anchor and stable labels.
6. Reassemble and return the object to its place before the next selection.

Do not obscure subtitles with glass or animate the reading surface continuously. Avoid neon holograms, aggressive glitches, blue cyberpunk grids, and unrelated sci-fi jargon. Soft clicks or a short status tone may support actual state changes; keep speech clear.

## Teaching example

Show three archive slabs: `SKILL.md`, `scripts/`, `references/`. Selecting a slab exposes its role. An exploded view separates instructions, executable capability and supporting evidence. Reassemble them into one skill folder, then show three agent access paths to that one object. Use original object names and marks rather than game names or insignia.

## Acceptance and current limit

The viewer can tell what is selected, what moved, and why new information appeared. Depth must help inspection, not merely decorate a slide. Test glass at final contrast and check captions against the brightest background. The repository/demo is evidence for the reference design; each new episode needs an authored scene implementation and an actual sample. A browser demo failing to load does not establish that its documented interactions fail in the original project.
