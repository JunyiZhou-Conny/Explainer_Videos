# check-only (B7): how many embedding calls semantic-split makes, per book, without calling Google.
# The tutorial's SemanticChunker (semantic_splitter.py) gets a stand-in for generate_text_embeddings
# (cli.py:87-121) that counts the API calls it would make (one per batch, semantic_splitter.py:206 asks for
# batches of 50) and returns random vectors. The number of chunks does not depend on the vectors' values:
# the 95th-percentile rule (semantic_splitter.py:91-96, :239-243) always cuts at the top 5 % of the gaps.
import glob, math, os, sys
import numpy as np
sys.path.insert(0, "/app")
from semantic_splitter import SemanticChunker

calls = 0
rng = np.random.default_rng(0)
def fake_embeddings(chunks, dimensionality=256, batch_size=250, **_):
    global calls
    calls += math.ceil(len(chunks) / batch_size)
    return rng.normal(size=(len(chunks), dimensionality)).tolist()

tot = {"sentences": 0, "chunk_calls": 0, "chunks": 0, "embed_calls": 0}
for f in sorted(glob.glob(os.path.join("/app", "input-datasets", "books", "*.txt"))):
    text = open(f).read()
    calls = 0
    chunks = SemanticChunker(embedding_function=fake_embeddings).split_text(text)
    import re
    n = len(re.split(r"(?<=[.?!])\s+", text))
    embed_calls = math.ceil(len(chunks) / 15)          # cli.py:248-250: batch_size=15 for semantic-split
    lens = [len(c) for c in chunks]
    print(f"{os.path.basename(f)[:40]:40s} sentences {n:5d}  chunk-phase calls {calls:3d}  chunks {len(chunks):4d}"
          f"  embed-phase calls {embed_calls:3d}  chunk length min {min(lens)} median {int(np.median(lens))} max {max(lens)}")
    for k, v in zip(tot, (n, calls, len(chunks), embed_calls)):
        tot[k] += v
print("total:", tot)
