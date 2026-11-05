#!/bin/sh
# Capture-only check for the L15 recording, NOT part of the tutorial.
# Installs the SageMaker SDK packages of one version WITHOUT their dependencies (enough to see which
# modules the SDK still ships), then runs the tutorial's own import lines.
# Usage: sagemaker_import_check.sh "<pip requirements>" "<python import line>"...
REQS=$1; shift
pip install --quiet --disable-pip-version-check --root-user-action=ignore --no-deps $REQS || exit $?
pip list --disable-pip-version-check 2>/dev/null | grep -i sagemaker
python -c 'import sagemaker; print("sagemaker is a namespace package:", list(sagemaker.__path__)); import pkgutil; print("its modules:", sorted(m.name for m in pkgutil.iter_modules(sagemaker.__path__)))'
for line in "$@"; do
  echo ">>> $line"
  python -c "$line" 2>&1 | tail -n 1
done
