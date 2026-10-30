# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:258-266 (2. Context Engineering: personalized vs basic, what the comparison measures), unchanged.
**Question: What useful information did we add, and did the agent use it appropriately?**

Use `personalized` for the main comparison. Its current request omits the customer's
saved mild-cheese and nonalcoholic-pairing preferences. Both modes receive the same
request, tools and policies; only enriched receives the saved profile. The output
shows actual cheese funk levels and a separate personalization check (mild = funk 0–2).
Basic is not penalized for missing information. Read the final pairing prose manually;
that is not automatically scored. `standard` remains a baseline where preferences
repeat the request, so improvement may be small or absent.
