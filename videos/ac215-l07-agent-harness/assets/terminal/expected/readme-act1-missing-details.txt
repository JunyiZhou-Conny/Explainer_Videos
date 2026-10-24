# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:242-252 (Try a variation: missing-details, and the checkpoint), unchanged.
**Live:**

```bash
python cli.py --act 1 --scenario missing-details
```

The destination and allergy information are missing. Look for clarification instead of invented details.

**Code to read:** [act1_agent.py](acts/act1_agent.py), [tools.py](formaggio/agents/tools.py), and [shop_assistant.md](prompts/shop_assistant.md).

**Checkpoint:** Explain why calling `preview_order` does not authorize or place an order.
