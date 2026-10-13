"""Run Marco's extract (v5) + chunk (v4) on the real catalog documents, offline.
Usage: python -I marco_extract_check.py <marco_services_dir> <download_dir> <out_dir>"""
import json, sys
from pathlib import Path
services, dl, out = (Path(a) for a in sys.argv[1:4])
sys.path[:0] = [str(services / "extract"), str(services / "chunk")]
from careonex_extract.convert import to_markdown, EXTRACTOR_VERSION
from careonex_chunk.chunker import chunk_markdown, CHUNKER_VERSION
import csv
out.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open(services / "data/catalog/ragfile_list.csv", encoding="utf-8")))
report, allchunks = [], []
for r in rows:
    f = dl / r["file_name"]
    if r["source_url"].startswith("curated/"):
        data = (services / "data/catalog" / r["source_url"]).read_bytes()
    else:
        data = f.read_bytes()
    try:
        md = to_markdown(data, r["kind"], r["file_name"])
    except Exception as e:
        print(f"EXTRACT FAILED {r['file_name']}: {type(e).__name__}: {e}"); report.append({"file": r["file_name"], "error": str(e)}); continue
    (out / (r["file_name"] + ".md")).write_text(md, encoding="utf-8")
    try:
        chunks = chunk_markdown(md, 1600, 2800, 200, 120)
    except Exception as e:
        print(f"CHUNK FAILED {r['file_name']}: {type(e).__name__}: {e}"); report.append({"file": r["file_name"], "md_chars": len(md), "chunk_error": str(e)}); continue
    for c in chunks:
        allchunks.append({"file": r["file_name"], "order": c.order, "chars": c.chars, "heading_path": c.heading_path, "text": c.text})
    report.append({"file": r["file_name"], "md_chars": len(md), "chunks": len(chunks)})
    print(f"{len(md):>7}  chunks={len(chunks):>3}  {r['file_name']}")
print("extractor", EXTRACTOR_VERSION, "chunker", CHUNKER_VERSION, "total chunks", len(allchunks))
(out / "report.json").write_text(json.dumps(report, indent=1))
(out / "chunks.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in allchunks) + "\n")
