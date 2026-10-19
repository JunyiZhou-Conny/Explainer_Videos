# b1_two_tools.py: the two functions of agent_tools.py, run by the tutorial's own dispatcher with hand-written
# FunctionCalls (the model's half needs a key), and the same query vector for both (a stand-in: the stored
# vector of a chunk about rennet). Which books do the 10 results come from? Then: authors not in the enum.
from collections import Counter
from standin import collection, stored_vector, call
import agent_tools
col = collection()
embed = stored_vector("Hand-book on cheese making", "rennet")
q = "How much rennet should be added to the milk?"
for fc in (call("get_book_by_author", author="George E. Newell", search_content=q).function_call,
           call("get_book_by_search_content", search_content=q).function_call):
    parts = agent_tools.execute_function_calls([fc], col, embed_func=embed)
    print()
    where = {"author": fc.args["author"]} if "author" in fc.args else None
    r = col.query(query_embeddings=[embed(q)], n_results=10, where=where, include=["metadatas"])
    print(f"== {fc.name}: function response {len(parts[0].function_response.response['content'])} characters; "
          f"the 10 results by book: {dict(Counter(m['book'] for m in r['metadatas'][0]))}")
    print()
print("== the two authors the enum leaves out, as where-filters (what get_book_by_author would get if the enum allowed them):")
for author in ["Milk Industry Foundation", "Woman's Institute of Domestic Arts and Sciences"]:
    r = col.query(query_embeddings=[embed(q)], n_results=10, where={"author": author}, include=["documents"])
    print(f"   author={author!r}: {len(r['ids'][0])} results, a function response of "
          f"{len(chr(10).join(r['documents'][0]))} characters")
for book in ["Cottage Cheese Recipe Book", "Womans Institute Library of Cookery"]:
    m = col.get(where={"book": book}, limit=1, include=["metadatas"])["metadatas"][0]
    print(f"   stored metadata of {book!r}: {m}")
