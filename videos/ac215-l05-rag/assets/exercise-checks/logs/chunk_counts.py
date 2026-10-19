# check-only: chunk counts with the tutorial's own splitters (langchain-text-splitters 0.3.11, from uv.lock)
# for the settings the exercises ask about. Reads /app/input-datasets/books exactly as cli.py:171-181 does.
import glob, math, os, re
from langchain.text_splitter import CharacterTextSplitter, RecursiveCharacterTextSplitter

books = {}
for f in glob.glob(os.path.join("input-datasets", "books", "*.txt")):
    with open(f) as fh:
        books[os.path.basename(f).split(".")[0]] = fh.read()

def char(size, overlap):
    s = CharacterTextSplitter(chunk_size=size, chunk_overlap=overlap, separator='', strip_whitespace=False)
    return lambda t: [d.page_content for d in s.create_documents([t])]
def rec(size, overlap=None):
    s = RecursiveCharacterTextSplitter(chunk_size=size) if overlap is None else \
        RecursiveCharacterTextSplitter(chunk_size=size, chunk_overlap=overlap)
    return lambda t: [d.page_content for d in s.create_documents([t])]

T = "Tolminc Cheese"
print("Tolminc characters:", len(books[T]))
for label, fn in [("char-split 350/20 (cli.py:185-189)", char(350, 20)),
                  ("char-split 700/100", char(700, 100)),
                  ("char-split 700/20", char(700, 20)),
                  ("recursive-split 350, default overlap (cli.py:199-200)", rec(350)),
                  ("recursive-split 350, chunk_overlap=20", rec(350, 20)),
                  ("recursive-split 350, chunk_overlap=0", rec(350, 0))]:
    counts = {b: len(fn(t)) for b, t in books.items()}
    print(f"{label}: Tolminc {counts[T]}, total {sum(counts.values())}")

# the char-split formula: 1 + ceil((len - size) / (size - overlap)) for every book
ok = all(len(char(350, 20)(t)) == 1 + math.ceil((len(t) - 350) / 330) for t in books.values())
print("formula 1 + ceil((len - 350) / 330) matches every book:", ok)
print("RecursiveCharacterTextSplitter default chunk_overlap:", RecursiveCharacterTextSplitter()._chunk_overlap,
      "separators:", RecursiveCharacterTextSplitter()._separators)
