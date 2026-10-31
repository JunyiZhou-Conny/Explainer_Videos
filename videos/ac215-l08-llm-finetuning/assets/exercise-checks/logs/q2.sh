# Q2 / C: the silent failure chain, in a fresh clone with an empty /secrets (as dataset-creator/05, 07).
cd /repo/dataset-creator
step 'ls -la /secrets'
step 'python cli.py --generate'
step 'ls -A data | wc -l'
step 'python cli.py --prepare'
step 'wc -c data/instruct-dataset.csv; od -c data/instruct-dataset.csv'
