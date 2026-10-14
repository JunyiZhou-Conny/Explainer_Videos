# Brief: speciesOT E4 · scGen as arithmetic, behind one adapter

- **Learning objective.** Conny can draw scGen (encode → +δ → decode), map it onto
  `setup`/`train`/`predict`, name the three different things called scgen in the project and
  where each lives, and explain why `scGenModel` should be an adapter around exactly one of them.
- **Hook.** Predict a human cell with one subtraction and one addition?
- **Mechanisms.** Autoencoder squeeze/rebuild; mean crosses and the δ arrow; held-out cells
  shifted; one arrow failing a second cell type; the package boundary with one door.
- **Ponders.** s03 (what must hold for one arrow to work for every type?), s06 (switch
  implementation: how many files change?) — answered in s07.
- **Recommendation (INFERRED).** To reproduce the benchmark numbers, wrap the cellot autoencoder
  (it made them); settle it with Josh first.
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
