# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:316-330 (Optional baseline with overlapping preferences), unchanged.
### Optional baseline with overlapping preferences

**Live; runs both modes in separate sessions:**

```bash
python cli.py --act 2 --scenario standard
```

This will:

- Run the same assistant once with basic context and once with enriched context.
- Keep the prompt, model, tools, and customer brief the same.
- Show both responses, cart checks, and model-call counts.

**What to look for:** Which facts are already available in enriched mode? Which products were filtered out? Did the model need different tool calls? One pair of runs does not establish that enriched context always performs better.
