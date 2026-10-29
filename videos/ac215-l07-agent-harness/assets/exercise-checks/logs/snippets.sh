# The Python snippets of exercises.md, run exactly as printed: saved under outputs/ in a fresh clone, run from /app.
mkdir -p outputs
for s in b1 b2 b3 b4 b5 b6 b13; do
  cp /checks/snippets/$s.py outputs/$s.py
  step "PYTHONPATH=. python outputs/$s.py"
done
