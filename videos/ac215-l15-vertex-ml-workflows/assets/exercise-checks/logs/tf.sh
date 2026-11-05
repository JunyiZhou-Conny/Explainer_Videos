# TensorFlow checks (B1, B5, D4), run inside python:3.11-slim with --network none, using the venv
# setup.sh built (tensorflow-cpu 2.20.0 + keras 3.11.2, the training image's versions, + pillow).
# Mounted read-only: /md = model-deployment-aws, /src = ml-workflow-aws/src (assets/source/, pinned
# commits) and /data = two of model-deployment-aws's sample photos, taken with git show at 077f4db
# (not copied into this repository).
. /checks/lib.sh
export PATH=/venv/bin:$PATH PYTHONDONTWRITEBYTECODE=1 TF_CPP_MIN_LOG_LEVEL=3
cd /tmp
step 'python --version; python -m pip list 2>/dev/null | grep -i -E "^(tensorflow_cpu|keras|numpy|pillow) "'
step 'python /checks/req_size.py /data/brie-1.jpg /data/gouda-2.jpeg'
step 'python /checks/labels.py 2>&1 | grep -v -E "^(WARNING|I0000|E0000)"'
step 'python /checks/skew.py /data/brie-1.jpg /data/gouda-2.jpeg 2>&1 | grep -v -E "^(WARNING|I0000|E0000)"'
