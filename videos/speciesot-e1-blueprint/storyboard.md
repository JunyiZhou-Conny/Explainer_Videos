# E1 storyboard · Four verbs and a contract

Narration: `script.json`. Implemented in `scenes.py` (the series' reference scene file).

| Scene | Teaching point | Beats | Evidence |
|---|---|---|---|
| s01 | Where to start reading | Notebook cell (e24_src_example) with the four calls highlighted one by one; it shrinks; the real file shape (one hairline per line) draws; "345 lines"; five brackets light up on "Data, contract, conductor, model, metric". | READ IN CODE |
| s02 | Class vs object, init, self | Blueprint card → line 115 call → empty object; `__init__` lines 214–225 highlighted one by one while the object card gains one row per line; `self.lr` ringed; a second object with `lr = 0.01`. | READ IN CODE |
| s03 | Abstract class = contract | AbstractModel lines 35–48 (decorators, then raises); zoom out; contract card with blank slots; ponder; measured TypeError card; IdentityModel and scGenModel cards sign it (parentheses in red) — "inheritance"; line 19–20 note on abc.ABC. | MEASURED / READ IN CODE |
| s04 | The conductor | Experiment chip + three verbs; config.yaml 30–45 → model chips and evaluation chips (TransformFromCopy from the YAML rows); token walks the models list; predictions; 2 × 2 grid of placeholder scores; evaluate lines 141–145, line 145 highlighted, scores fall away, "returns None" MEASURED. | READ IN CODE / MEASURED |
| s05 | Polymorphism | predict loop 135–138, line 137; two lanes from the same mouse cloud: IdentityModel returns the same cloud (baseline), scGenModel shifts it toward a dashed human target ("planned — episode 4"); ponder; lines 107–115 with the if-chain highlighted and a ghost `CellOTModel ?`. | READ IN CODE |
| s06 | Recap | Three recap cards; the five-jobs table with classes and line ranges. | — |
