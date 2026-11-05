#!/bin/sh
# Capture-only check for the L15 recording, NOT part of the tutorial.
# What pip's resolver (the one inside `pipenv lock`) picks TODAY for a Pipfile's [packages] on this
# container's Python, without installing anything: pip install --dry-run --report.
# Usage: resolve_check.sh <requirement>...
python --version
# a current pip first: it reads PyPI's metadata files instead of downloading every wheel
pip install --quiet --disable-pip-version-check --root-user-action=ignore --upgrade pip || exit $?
pip --version
pip install --quiet --disable-pip-version-check --root-user-action=ignore --dry-run --ignore-installed \
  --report /tmp/report.json "$@" || exit $?
python - <<'PY'
import json
items = json.load(open("/tmp/report.json"))["install"]
v = {i["metadata"]["name"].lower(): i["metadata"]["version"] for i in items}
print(len(v), "packages would be installed, among them:")
keys = ("sagemaker", "tensorflow", "keras", "boto3", "numpy", "torch", "nvidia-", "mlflow", "gevent")
for k in sorted(v):
    if k.startswith(keys):
        print(f"  {k}=={v[k]}")
PY
