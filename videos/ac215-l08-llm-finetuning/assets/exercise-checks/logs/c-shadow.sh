# C10: a scratch file named like a standard-library module, next to the script that imports torch.
mkdir -p /tmp/work && cd /tmp/work
printf 'import math\nprint(round(math.exp(2.6498), 2))\n' > numbers.py
printf 'import torch\nprint(torch.__version__)\n' > count.py
step 'ls; python count.py 2>&1 | tail -3'
step 'mv numbers.py ppl.py; python count.py'
