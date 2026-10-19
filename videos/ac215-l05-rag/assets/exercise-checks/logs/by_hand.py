# check-only (D5, D6): the lecture's two worked examples, recomputed (numbers from SLIDES.md: A41 table, B44-B48)
import math
people = {"instructor": [4.8, 4.5, 4.2, 3.3, 4.1], "A": [3.3, 4.0, 4.1, 3.1, 4.6],
          "B": [4.8, 2.7, 4.9, 2.5, 4.2], "C": [1.0, 3.6, 3.8, 4.4, 2.2]}
P = people.pop("instructor")
dot = lambda x, y: sum(a * b for a, b in zip(x, y))
print("D6 personality game (A41): measure per candidate")
for n, X in people.items():
    print(f"  {n}: cosine {dot(P, X) / math.sqrt(dot(P, P) * dot(X, X)):.4f}  dot {dot(P, X):.2f}  "
          f"euclidean {math.dist(P, X):.3f}  length {math.sqrt(dot(X, X)):.3f}")
def rrf(ranks, k=0, w=0.5):
    return sum(w / (k + r) for r in ranks)
print("D5 RRF, slides (k=0, w=0.5): ranks (BM25, vector) -> score")
for p, r in {"1": (2, 1), "2": (1, 3), "3": (3, 2)}.items():
    print(f"  paragraph {p} {r}: {rrf(r):.4f}")
four = {"1": (3, 1), "2": (1, 4), "3": (4, 3), "4": (2, 2)}
for k in (0, 60):
    s = {p: rrf(r, k) for p, r in four.items()}
    print(f"D5 with a 4th paragraph 2nd in both lists, k={k}: " +
          ", ".join(f"{p}{four[p]}={v:.6f}" for p, v in s.items()) + " -> order " + " ".join(sorted(s, key=lambda p: -s[p])))
