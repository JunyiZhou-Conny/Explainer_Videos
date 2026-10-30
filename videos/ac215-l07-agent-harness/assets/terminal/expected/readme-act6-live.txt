# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:631-641 (Act 6 live: what to look for; finishing vs delivering), unchanged.
**Live:**

```bash
python cli.py --act 6 --scenario standard
```

**What to look for:** Separate outer-model calls from workflow-model calls. The outer agent cannot replace the confirmed request or approve its own order. After an order is accepted, the tasting plan should use receipt quantities and prices rather than inventing a new cart.

**Concept: finishing execution is different from delivering the answer.** Act 5’s `tasting-plan` scenario and Act 6 use a structured final reply. The harness checks that every required menu has a serving sequence and compatible pairing IDs, then renders quantities, prices and listed allergens from authoritative data. Students still receive readable `agent_text`; `.run(...)` and the existing result keys stay the same. A missing or invalid plan makes a tasting-only or composition result `needs_followup`, even when an order was successfully placed. The `event-shortage` task remains a sourcing summary and email review; it does not require an additional serving plan.

The `delivery.checked` event and `outcome.tasting_delivery` evaluation check expose this distinction. Human review still assesses the reasoning and quality of the prose. See [tasting_delivery.py](formaggio/agents/tasting_delivery.py).
