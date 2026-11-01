# B2: split sizes for N pairs, and the 256 cap on the validation file. Scripted pairs made by snippets/make_pairs.py (exercises.md B2, as printed).
cd /repo/dataset-creator
for n in 21 100 2600; do
  rm -rf data
  step "python /checks/snippets/make_pairs.py $n"
  step 'python cli.py --prepare | grep Shape'
  step 'wc -l data/train.jsonl data/test.jsonl; python -c "import pandas as pd; print(\"test.csv rows:\", len(pd.read_csv(\"data/test.csv\")), \" train.csv rows:\", len(pd.read_csv(\"data/train.csv\")))"'
done
step 'ls data | head -4'
