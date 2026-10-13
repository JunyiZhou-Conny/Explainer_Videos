"""Run the team's extract + chunk code on every catalog source, offline (no AWS).
Usage: python -I offline_pipeline.py <services_dir> <download_dir> <out_dir>"""
import csv, hashlib, json, sys, time
from pathlib import Path
import requests

services, dl, out = (Path(a) for a in sys.argv[1:4])
sys.path[:0] = [str(services / "extract"), str(services / "chunk")]
from careonex_extract.convert import to_markdown, EXTRACTOR_VERSION
from careonex_chunk.chunker import chunk_markdown, CHUNKER_VERSION

dl.mkdir(parents=True, exist_ok=True); out.mkdir(parents=True, exist_ok=True)
rows = list(csv.DictReader(open(services / "data/catalog/ragfile_list.csv", encoding="utf-8")))
report, all_chunks = [], []
for r in rows:
    f = dl / r["file_name"]
    if r["source_url"].startswith("curated/"):
        data = (services / "data/catalog" / r["source_url"]).read_bytes()
    elif f.exists():
        data = f.read_bytes()
    else:
        resp = requests.get(r["final_url"] or r["source_url"], timeout=60, headers={"User-Agent": "careonex-agents data service (explainer reproduction)"})
        resp.raise_for_status(); data = resp.content; f.write_bytes(data); time.sleep(0.5)
    sha = hashlib.sha256(data).hexdigest()
    md = to_markdown(data, r["kind"], r["file_name"])
    (out / (r["file_name"] + ".md")).write_text(md, encoding="utf-8")
    chunks = chunk_markdown(md, 1600, 2800, 200)
    for c in chunks:
        all_chunks.append({"file": r["file_name"], "program": r["program"], "order": c.order, "chars": c.chars, "heading_path": c.heading_path, "text": c.text})
    report.append({"file": r["file_name"], "kind": r["kind"], "program": r["program"], "bytes": len(data), "sha_matches_catalog": sha == r["sha256"], "md_chars": len(md), "chunks": len(chunks)})
    print(f"{r['kind']:4} {len(data):>8} B  sha={'ok ' if sha == r['sha256'] else 'NEW'} md={len(md):>6}  chunks={len(chunks):>3}  {r['file_name']}", flush=True)
print("total chunks:", len(all_chunks), "extractor", EXTRACTOR_VERSION, "chunker", CHUNKER_VERSION)
(out / "report.json").write_text(json.dumps(report, indent=1))
(out / "chunks.jsonl").write_text("\n".join(json.dumps(c, ensure_ascii=False) for c in all_chunks) + "\n", encoding="utf-8")
