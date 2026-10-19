# check-only (C4): a 768-number query vector against the 256-dimension collection the load step built
import chromadb
c = chromadb.HttpClient(host="llm-rag-chromadb", port=8000).get_collection("char-split-collection")
print("collection:", c.name, "| count:", c.count())
for n in (256, 768):
    try:
        r = c.query(query_embeddings=[[0.01] * n], n_results=10)
        print(f"query with {n} numbers: OK, {len(r['ids'][0])} results")
    except Exception as e:
        print(f"query with {n} numbers: {type(e).__module__}.{type(e).__name__}: {e}")
