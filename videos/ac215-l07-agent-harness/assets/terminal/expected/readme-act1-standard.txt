# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:175-200 (Run Act 1: the standard scenario, what the console shows, what to look for), unchanged.
**Live:**

```bash
python cli.py --act 1 --scenario standard
```

The standard scenario requests a tasting for 12 guests in PA, with a $150 cheese budget, a confirmed nut allergy, at least one French cheese, and at least one cheese with funk level 4 or higher.

This will:

- Supply the confirmed request and shop instructions to the agent.
- Expose catalog, stock, pricing, pairing, and proposal tools.
- Display the agent's response and an independent check of its final cart.
- Record the run without placing an order or silently repairing the proposal.

The console starts with the customer ask in plain language, followed by numbered model/tool calls and compact argument/result summaries. Model steps show the latest tool results in context, elapsed time, and token usage when available.

The ask is rendered from the confirmed fields in [scenarios.json](data/scenarios.json); the fixtures do not store a separate original customer sentence. This display does not change the message sent to the model. To see that exact message, including its structured request, and detailed JSON tool payload previews, add `--show-json`:

```bash
python cli.py --act 1 --scenario standard --show-json
```

`--show-json` also applies to progress logs in the other individual act runs. Long JSON payloads are labeled as truncated previews; use `--inspect-run RUN_ID` for the full recorded model/tool payloads. SQLite tracing remains complete in either display mode. Explicit inspection commands such as `--preview-context` and `--inspect-run`, and the existing `--show-context` option, still display their requested details. These logs describe visible execution, not hidden model reasoning.

**What to look for:** Does the proposal satisfy the independent cart check? Does the response distinguish a proposal from an order? An invalid proposal is useful evidence for the later workflow lesson.
