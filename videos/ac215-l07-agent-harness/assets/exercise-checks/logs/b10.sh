# B10: memory, offline and persistent: --fixture with --memory-db (README.md:836 "--customer", cli.py:49).
step "python cli.py --act 4 --fixture --memory-db outputs/my-memory.sqlite --customer shivas --remember-preference 'Prefer nonalcoholic pairings today' --email-decision decline | grep -E '^Memory for'"
step "python cli.py --act 4 --fixture --memory-db outputs/my-memory.sqlite --customer shivas --email-decision decline | grep -E '^Memory for'"
step "python cli.py --act 4 --fixture --memory-db outputs/my-memory.sqlite --customer shivas --remember-preference 'mild cheeses' --email-decision decline | grep -E '^Memory for'"
step "python cli.py --act 4 --fixture --customer shivas --email-decision decline | grep -E '^Memory for'"
step "python cli.py --act 4 --fixture --customer pavlos --memory-db outputs/my-memory.sqlite --email-decision decline | grep -E '^Memory for'"
step "ls outputs/"
