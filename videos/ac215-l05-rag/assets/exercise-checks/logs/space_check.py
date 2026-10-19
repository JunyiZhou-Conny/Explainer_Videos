# check-only (D1): cosine (the tutorial's "hnsw:space") vs Chroma's default space (l2) on the staff's
# char-split vectors (68e0bde), with stored chunk vectors as stand-in queries.
import glob, json
import numpy as np
import chromadb

rows = []
for f in sorted(glob.glob("outputs/embeddings-char-split-*.jsonl")):
    for i, l in enumerate(open(f)):
        d = json.loads(l)
        rows.append((d["book"], i, d["embedding"]))
V = np.array([r[2] for r in rows], dtype=np.float64)
norms = np.linalg.norm(V, axis=1)
print(f"{len(rows)} vectors x {V.shape[1]} numbers; lengths min {norms.min():.3f}, max {norms.max():.3f}")

# brute force, every stored vector as a query: does the top 10 change between cosine and L2?
U = V / norms[:, None]
def top(q_idx, k=10):
    q = V[q_idx]
    cos_d = 1 - U @ (q / np.linalg.norm(q))
    l2_d = ((V - q) ** 2).sum(axis=1)
    return list(np.argsort(cos_d, kind="stable")[:k]), list(np.argsort(l2_d, kind="stable")[:k])
same_order = same_set = 0
for qi in range(len(V)):
    a, b = top(qi)
    same_order += a == b
    same_set += set(a) == set(b)
print(f"queries: {len(V)} | same top 10 in the same order: {same_order} | same 10 chunks, any order: {same_set}")

# normalised vectors: cosine and L2 must agree exactly
Vn = U
diff = 0
for qi in range(0, len(V), 50):
    q = Vn[qi]
    a = list(np.argsort(1 - Vn @ q, kind="stable")[:10]); b = list(np.argsort(((Vn - q) ** 2).sum(axis=1), kind="stable")[:10])
    diff += a != b
print(f"after normalising every vector to length 1: {diff} of {len(range(0, len(V), 50))} sampled queries differ")

# the same comparison in Chroma: the tutorial's cosine collection vs a collection with the default space
client = chromadb.HttpClient(host="llm-rag-chromadb", port=8000)
cos = client.get_collection("char-split-collection")
try:
    client.delete_collection("l2-check")
except Exception:
    pass
l2 = client.create_collection("l2-check")          # no metadata: Chroma's default space
for s in range(0, len(rows), 500):
    batch = rows[s:s + 500]
    l2.add(ids=[f"{b}-{i}" for b, i, _ in batch], embeddings=[e for _, _, e in batch])
print("l2-check configuration space:", l2.configuration_json.get("hnsw", {}).get("space"),
      "| char-split-collection space:", cos.configuration_json.get("hnsw", {}).get("space"))
t = cos.get(where={"book": "Tolminc Cheese"}, include=["embeddings", "documents"])
i = next(k for k, d in enumerate(t["documents"]) if "curd" in d)
v = t["embeddings"][i]
print("stand-in query: stored vector of", t["ids"][i])
rc = cos.query(query_embeddings=[v], n_results=10, include=["distances", "metadatas"])
rl = l2.query(query_embeddings=[v], n_results=10, include=["distances"])
print("cosine:", [f"{d:.4f}" for d in rc["distances"][0]])
print("l2:    ", [f"{d:.4f}" for d in rl["distances"][0]])
print("cosine top-10 books:", sorted(set(m["book"] for m in rc["metadatas"][0])))
print("l2 top-10 ids from:", sorted(set(x.rsplit("-", 1)[0] for x in rl["ids"][0])))
client.delete_collection("l2-check")
