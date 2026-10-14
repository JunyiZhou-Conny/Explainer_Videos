# Brief: speciesOT E1 · Four verbs and a contract

- **Learning objective.** Conny can open `speciesot_core.py` and say, for any class, which of
  five jobs it does (data, contract, conductor, model, metric); knows what a class, an object,
  `__init__` and `self` are; knows that an abstract class is a contract that Python checks by
  method *name* at construction, never by arguments.
- **Hook.** Four calls in a notebook run a whole experiment — which of 346 lines matter?
- **Mechanisms.** The file's real shape partitioned into five jobs; an object filling up line by
  line as `__init__` runs; a contract with blank slots and the measured TypeError; one call
  (`model.predict`, line 137) giving two different answers.
- **Ponders.** s03 (build an AbstractModel directly?), s05 (adding CellOT: which lines change?).
- **Skip.** Metaclasses, dataclasses, type hints beyond reading them.
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
