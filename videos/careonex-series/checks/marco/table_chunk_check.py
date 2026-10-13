"""Does Marco's chunker (v4, the branch default) keep the program names with the $1,090 row?

Input: the Side-by-Side text as the E2 extractor wrote it (pymupdf4llm Markdown, the table E2 shows).
Prints every chunk that contains "1,090" and whether it names JACC.
Usage: python -I table_chunk_check.py <marco_services_dir> <side_by_side.md>"""
import sys
from pathlib import Path

services, md = Path(sys.argv[1]), Path(sys.argv[2]).read_text(encoding="utf-8")
sys.path.insert(0, str(services / "chunk"))
from careonex_chunk.chunker import CHUNKER_VERSION, chunk_markdown  # noqa: E402

chunks = chunk_markdown(md, 1600, 2800, 200, 120)
print("chunker", CHUNKER_VERSION, "chunks", len(chunks))
for c in chunks:
    if "1,090" in c.text:
        head = next((ln for ln in c.text.splitlines() if ln.startswith("|")), "")
        print(f"chunk {c.order}: {c.chars} chars · names JACC: {'JACC' in c.text}")
        print("  first table row:", head[:120])
