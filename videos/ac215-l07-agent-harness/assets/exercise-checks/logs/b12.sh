# B12: a comparison with a confounder. Two scripted batches; between them a scratch .py file in the repo root,
# then (third batch) one price in data/catalog.json.
step "python cli.py --act 2 --evaluate core --fixture --case standard --repeats 1 --label ex-a | tail -n 4"
step "printf 'print(\"scratch\")\n' > scratch.py"
step "python cli.py --act 2 --evaluate core --fixture --case standard --repeats 1 --label ex-b | tail -n 4"
step "python cli.py --compare ex-a ex-b | python -c 'import json,sys; r=json.load(sys.stdin); print({k: r[k] for k in (\"changed_configuration\", \"confounding_changes\", \"evaluator_changed\")}); print(sorted({x[\"outcome\"] for x in r[\"results\"]})); print(r.get(\"interpretation\"))'"
step "rm scratch.py && sed -i 's/\"cents_per_100g\": 690/\"cents_per_100g\": 700/' data/catalog.json && grep -c '\"cents_per_100g\": 700' data/catalog.json"
step "python cli.py --act 2 --evaluate core --fixture --case standard --repeats 1 --label ex-c | tail -n 4"
step "python cli.py --compare ex-a ex-c | python -c 'import json,sys; r=json.load(sys.stdin); print({k: r[k] for k in (\"changed_configuration\", \"confounding_changes\", \"evaluator_changed\")}); print(sorted({x[\"outcome\"] for x in r[\"results\"]})); print(r.get(\"interpretation\"))'"
step "python cli.py --compare ex-a"
