"""Download every HTML source twice with the team's User-Agent; compare hashes to each other and the catalog.
Usage: python -I html_hashes.py <catalog.csv> <out_dir>"""
import csv, hashlib, sys, time
from pathlib import Path
import requests
UA = "careonex-agents data service (+https://github.com/nadirbt/careonex-agents)"
rows = [r for r in csv.DictReader(open(sys.argv[1], encoding="utf-8")) if r["kind"] == "html"]
out = Path(sys.argv[2]); out.mkdir(parents=True, exist_ok=True)
for r in rows:
    hs = []
    for k in range(2):
        b = requests.get(r["final_url"] or r["source_url"], timeout=60, headers={"User-Agent": UA}).content
        (out / f"{r['file_name']}.{k}").write_bytes(b)
        hs.append(hashlib.sha256(b).hexdigest())
        time.sleep(1.0)
    print(f"{'same' if hs[0]==hs[1] else 'DIFF'}  catalog={'match' if hs[0]==r['sha256'] or hs[1]==r['sha256'] else 'no   '}  {len(b):>7}  {r['file_name']}", flush=True)
