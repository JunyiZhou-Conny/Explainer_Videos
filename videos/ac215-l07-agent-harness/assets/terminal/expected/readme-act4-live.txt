# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:454-471 (Act 4 live: the event brief, the stock shortfall, what to look for), unchanged.
**Live:**

```bash
python cli.py --act 4
```

The event brief specifies 1,000 g Comté, 1,000 g Mimolette, and 1,200 g Époisses for 40 guests in NY. The cheese quote is $177.80. Shop Époisses stock is 900 g, leaving a 300 g shortfall.

This will give the agent tools to:

- Assess the confirmed menu and identify the stock shortfall.
- Maintain a visible task list and retrieve vendor evidence.
- Draft an availability inquiry for the approved recipient.
- Request human review before writing a local mock-email HTML file.

When prompted, type `approve` or `decline`. An approved save prints the file path. The repository is mounted from your host, so the file is also available under the host repository's `outputs/` directory.

**What to look for:** A completed task is not an approval. Shop stock does not establish vendor availability. The authoritative artifact status must agree with the actual save or decline.
