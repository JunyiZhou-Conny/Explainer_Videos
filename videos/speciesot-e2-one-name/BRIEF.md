# Brief: speciesOT E2 · One name, five places

- **Learning objective.** Conny can trace a config value from `Tests/config.yaml` to the attribute
  `setup()` reads, explain why the edits bounced between three files, tell KeyError from
  AttributeError, read a traceback bottom-up, and fix the `x_dimension`/`x_dimensions` twin
  everywhere it lives (config.yaml:37, toy_config.yaml:19, core 104, 220, 253).
- **Hook.** Deleting one letter silences the crash; the bug stays (network sized for 1000 genes).
- **Mechanisms.** Three windows and two wires (editable install + autoreload; yaml.safe_load);
  a token travelling four hops; dictionary drawers; the silent second drawer.
- **Ponders.** s04 (KeyError or AttributeError?), s05 (typed in the config, or from the data?).
- **Caveat on screen.** Measured with a stand-in scgen; on the cluster a different scgen error
  can come first (E4).
- **Audience.** Conny: computational-biology researcher, strong on single-cell biology, scGen and
  optimal transport; self-described near-zero intuition for abstraction, Python packaging and
  testing. Watches with Josh's `src/speciesot/` open.
- **Style / format.** `swiss`, English narration (Kokoro `af_heart`, 0.95×), Chinese above English
  captions burned in, composed score; duration fitted per `episode.json`.
- **Evidence.** Josh's `src/` as attached 2026-10-14 (hashes in `../speciesot-series/excerpts.py`),
  the speciesOT repo at `109bf12`, and our own measurements (`../speciesot-series/checks/`).
  See `SOURCES.md`; tags on screen follow `../speciesot-series/SERIES.md`.
- **Destination.** Conny's personal study. Shows unpublished code by Josh; publishing needs
  Conny's decision and Josh's agreement.
- **Series.** `../speciesot-series/SERIES.md`. Request: this session's prompt (2026-10-14), no
  GitHub issue opened for it.
