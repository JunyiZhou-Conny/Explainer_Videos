# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:361-367 (Act 3 live: what to look for), unchanged.
**Live:**

```bash
python cli.py --act 3 --scenario standard
```

**What to look for:** The model proposes quantities, but application code chooses transitions, calculates prices, validates constraints, and places the mock order. A successful order has an application receipt. If a valid cart cannot be obtained, the workflow reports that outcome.
