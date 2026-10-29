# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:723-751 (Step 3: a small live comparison), unchanged.
### Step 3: run a small live comparison

**Live; four scheduled runs per batch:**

```bash
python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details --repeats 2 --label context-live-a
```

Create an alternate prompt:

```bash
cp prompts/shop_assistant.md prompts/shop_assistant_v2.md
```

Open the copy in your editor. Make one deliberate change, such as requesting a shorter response with explicit price and action-status labels. Preserve the confirmed-constraint instructions. Do not change source, data, or skills during a batch.

Run the same cases and settings with the changed prompt:

```bash
python cli.py --act 2 --evaluate core --context enriched --case standard --case missing-details --repeats 2 --label context-live-b --prompt-file prompts/shop_assistant_v2.md
```

**Offline comparison:**

```bash
python cli.py --compare context-live-a context-live-b --json-output outputs/context-comparison.json
```

Inspect changed configuration, checks, structured outcomes, response text changes, model-call counts, latency, and token usage when available. Repetition numbers are not matched random seeds, and a small sample does not establish reliability.
