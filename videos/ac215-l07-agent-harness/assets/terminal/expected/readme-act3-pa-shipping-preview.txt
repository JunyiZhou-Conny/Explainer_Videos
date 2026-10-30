# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:283-290 (the live Act 3 rejection-and-revision preview inside the Act 2 section), unchanged.
For a live rejection-and-revision demonstration using a submitted customer cart:

```bash
python cli.py --act 3 --scenario pa-shipping
```

Look for `Cart attempt 1: shipping`, a live model revision, and a receipt only if
the corrected cart passes. The submitted cart is input data; the model chooses the replacement.
