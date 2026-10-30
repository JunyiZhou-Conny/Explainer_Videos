# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:849-866 (Act 2 comparison command), unchanged.
### Act 2 comparison command

`python cli.py --act 2 --compare` runs two fresh live sessions on `personalized` and
prints both answers and a side-by-side table. It measures both menus against the
customer's mild-cheese preference, counts distinct varieties (not grams), and shows
cart validity, calls and total token usage. The verdict reports improvement, a tie,
or a regression; it does not assume enriched will win. Empty or unknown carts are
unmeasured, and invalid carts cannot support an overall improvement claim.

Use `--scenario preference-override` to examine today's request taking priority;
that scenario does not use the all-mild rubric to declare a winner. Add `--show-json`
for full progress details, or `--json-output outputs/context-comparison.json` to save
the table. Traces are recorded in the normal database. Individual Act 2 runs also
show a separate PA policy probe; Act 3 demonstrates rejection and live model revision
with `--scenario pa-shipping`.

`python cli.py --compare BEFORE AFTER` still compares two saved evaluation labels
without running the agents.
