# check-only (C5): collection.query(query_texts=...) on the tutorial's collection, which was built from
# 256-number Gemini vectors. Chroma then embeds the text itself, with the collection's own embedding function.
import sys
import chromadb
c = chromadb.HttpClient(host=sys.argv[1], port=int(sys.argv[2])).get_collection("char-split-collection")
print("collection embedding function:", c.configuration_json.get("embedding_function"))
try:
    r = c.query(query_texts=["How is tolminc cheese made?"], n_results=10)
    print("query_texts: OK", r["ids"])
except Exception as e:
    print(f"query_texts: {type(e).__module__}.{type(e).__name__}: {e}")
from chromadb.utils import embedding_functions
ef = embedding_functions.DefaultEmbeddingFunction()
print("Chroma's default embedding function:", type(ef).__name__, "->", len(ef(["How is tolminc cheese made?"])[0]), "numbers")
