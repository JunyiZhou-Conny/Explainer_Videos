# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:643-658 (Try two competing orders), unchanged.
### Try two competing orders

**Offline:**

```bash
python cli.py --act 6 --fixture --scenario two-orders --manager-decision approve
```

This starts two confirmed requests sharing one checkout and inventory. Both request review. The test host approves both, but the first order consumes stock: the second should be blocked by final stock validation.

This will demonstrate:

- Separate workflow handles and approval tickets for each request.
- Host-controlled resume of a pending workflow.
- Shared resource constraints across otherwise valid requests.
- A distinction between approval and successful placement.
