# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:404-410 (the scripted manager-approval fixture ($220.80)), unchanged.
Now make the approval boundary predictable with a **scripted fixture**:

```bash
python cli.py --act 3 --fixture --scenario manager-approval
```

The fixture cart totals $220.80. At the manager prompt, review the request and cart, then type `approve` or `decline`. An approved cart is checked again before placement; declining places no order.
