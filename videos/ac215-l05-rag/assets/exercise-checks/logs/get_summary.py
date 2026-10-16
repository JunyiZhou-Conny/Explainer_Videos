# check-only: reads cli.py --get's output on stdin and prints its ids, each document's length and opening
# (first 12 characters; the full documents contain the Gutenberg producers' names, kept out of these logs)
import ast, sys
out = sys.stdin.read()
for line in out.splitlines():
    if not line.startswith("Results: "):
        print(line)
r = ast.literal_eval(out.split("Results: ", 1)[1].strip())
print("ids:", r["ids"])
print("books:", sorted({m["book"] for m in r["metadatas"]}), "| keys:", sorted(r["included"]))
for i, d in zip(r["ids"], r["documents"]):
    print(f"  {i}  {len(d):3d} chars  {d[:12]!r}")
