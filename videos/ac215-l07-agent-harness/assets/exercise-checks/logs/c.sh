# Debugging checks (Part C).
step "python cli.py --act 4 --scenario standard"
step "python cli.py --act 3 --fixture --scenario manager-approval < /dev/null"
step "printf 'yes\napprove\n' | python cli.py --act 3 --fixture --scenario manager-approval | grep -E 'Approve this|Please enter|WORKFLOW|Order placed'"
step "python cli.py --act 2 --compare --context basic"
step "python cli.py --act 1 --fixture"
step "python cli.py --act 4 --customer alice"
step "python cli.py --act 2 --evaluate core --fixture --scenario standard --label x"
step "PYTHONPATH=. python /checks/c_compaction_layer.py"
