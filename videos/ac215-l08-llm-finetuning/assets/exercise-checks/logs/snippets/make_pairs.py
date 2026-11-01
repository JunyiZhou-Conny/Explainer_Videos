# make_pairs.py N: write N scripted pairs into data/ as cheese_qa_<i>.txt, 20 per file (the shape --generate writes).
import json, os, sys
n = int(sys.argv[1]); os.makedirs("data", exist_ok=True)
for f in range((n + 19) // 20):
    pairs = [{"question": f"Scripted question {k}?", "answer": f"Good question! Scripted answer {k}."}
             for k in range(f * 20, min(n, f * 20 + 20))]
    with open(f"data/cheese_qa_{f}.txt", "w") as out:
        json.dump(pairs, out, indent=2)
print(f"{n} pairs in {(n + 19) // 20} files")
