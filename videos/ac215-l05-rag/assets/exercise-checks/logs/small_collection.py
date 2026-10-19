# check-only (B7): a query for 10 results on a collection that holds only 7 records (as semantic-split on one book)
import chromadb, random
random.seed(0)
client = chromadb.HttpClient(host="llm-rag-chromadb", port=8000)
c = client.create_collection(name="seven-check", metadata={"hnsw:space": "cosine"})
c.add(ids=[f"s-{i}" for i in range(7)], documents=[f"chunk {i}" for i in range(7)],
      embeddings=[[random.uniform(-1, 1) for _ in range(256)] for _ in range(7)])
r = c.query(query_embeddings=[[random.uniform(-1, 1) for _ in range(256)]], n_results=10)
print("records:", c.count(), "| n_results=10 ->", len(r["documents"][0]), "documents")
client.delete_collection("seven-check")
