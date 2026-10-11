"""For pages whose bytes differ between two downloads, compare the hashes of the extracted text.
Usage: python -I text_hash_check.py <services_dir> <dl2_dir>"""
import hashlib, sys
from pathlib import Path
services, d = Path(sys.argv[1]), Path(sys.argv[2])
sys.path.insert(0, str(services / "extract"))
from careonex_extract.convert import to_markdown
for f in sorted(d.glob("*.html.0")):
    a, b = f.read_bytes(), f.with_suffix(".1").read_bytes()
    if a == b:
        continue
    ta, tb = (hashlib.sha256(to_markdown(x, "html").encode()).hexdigest() for x in (a, b))
    print(f"bytes differ; text {'IDENTICAL' if ta == tb else 'DIFFERS'}  {f.name[:-2]}")
