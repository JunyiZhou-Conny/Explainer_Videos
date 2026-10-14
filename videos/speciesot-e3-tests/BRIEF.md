# Brief: speciesOT E3 · A test is a question with a known answer

- **Learning objective.** Conny can read and write a pytest test, knows how pytest finds tests,
  can derive known answers from what a metric means (identical → 0, perfect → 1, more shift →
  more distance), uses toy arrays instead of cluster files, and sees why `test_model.py` is a
  script, not a test.
- **Hook.** The package says MMD = 0.326 on toy cells. Is that right?
- **Mechanisms.** Three RBF kernel grids coinciding (MMD → 0); a cloud sliding while the MMD bar
  grows (measured); pairing lines crossing when rows are shuffled; the 5-vs-7 broadcast error.
- **Ponders.** s04 (push a cloud away: what does MMD do?), s05 (does R2Evaluation accept unequal
  cell counts?).
- **Decision surfaced, not made.** Per-cell R² (reconstruction) vs R² of means (benchmark).
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
