# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:292-301 (repeat the context cases: 12 live runs), unchanged.
Repeat the new context cases with saved per-run checks and traces:

```bash
python cli.py --act 2 --evaluate core --case personalized --case preference-override --repeats 3 --label act2-context-live-1
python cli.py --view-report act2-context-live-1
```

This runs both modes (12 live runs total). Enriched preference checks can fail even
when the cart is valid. Basic preference use is ungraded; ties are valid outcomes.
See [Tutorial questions and evidence](docs/TUTORIAL_SCENARIOS.md) for the six-act checklist.
