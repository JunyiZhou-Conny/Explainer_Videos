# expected (README text, not program output): dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402, README.md:481-488 (Optional memory exercise (live)), unchanged.
**Optional memory exercise — live:**

```bash
python cli.py --act 4 --customer shivas --remember-preference "Prefer nonalcoholic pairings today"
python cli.py --act 4 --customer shivas
```

Compare the printed memory on the second visit. The host persists the explicitly supplied preference; the model has no memory-write tool. Default live preference memory survives across runs, while standalone fixtures use isolated memory unless you supply `--memory-db`.
