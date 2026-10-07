#!/usr/bin/env python3
"""Add a paper to the library: file the PDF under its category and append a catalog entry.

    python tools/ingest.py ~/Downloads/2401.12345.pdf --category reinforcement-learning/policy-optimization
    python tools/ingest.py paper.pdf --category privacy/differential-privacy --id dwork2006calibrating
    python tools/ingest.py --arxiv 1707.06347 --category reinforcement-learning/policy-optimization
    python tools/ingest.py --list-categories

What it does
  1. Reads title / authors / year from the arXiv API (if an arXiv id is given or found in the
     file name) or else from the PDF itself.
  2. Copies the PDF to library/<category>/<id>.pdf  (--move to move it instead; --arxiv downloads it).
  3. Appends a stub entry to library/catalog.yaml (status: unread) for you — or Claude — to fill in:
     one_liner, key_ideas, builds_on (ids of library papers it builds on), tags.
  4. Regenerates library/README.md and library/MAP.md.

New category? Pass --new-category "Title of the category" and it is added to catalog.yaml.
"""

from __future__ import annotations

import argparse
import re
import shutil
import subprocess
import sys
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import catalog  # noqa: E402

ROOT = catalog.ROOT
ARXIV_RE = re.compile(r"(\d{4}\.\d{4,5})(v\d+)?")


def arxiv_meta(arxiv_id: str) -> dict:
    url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
    with urllib.request.urlopen(url, timeout=30) as r:
        root = ET.fromstring(r.read())
    ns = {"a": "http://www.w3.org/2005/Atom"}
    e = root.find("a:entry", ns)
    if e is None or e.find("a:title", ns) is None:
        raise RuntimeError(f"arXiv id {arxiv_id} not found")
    authors = [a.findtext("a:name", namespaces=ns) for a in e.findall("a:author", ns)]
    return {
        "title": " ".join(e.findtext("a:title", namespaces=ns).split()),
        "authors": authors[:4] + (["et al."] if len(authors) > 4 else []),
        "year": int(e.findtext("a:published", namespaces=ns)[:4]),
        "abstract": " ".join((e.findtext("a:summary", namespaces=ns) or "").split()),
    }


def pdf_meta(pdf: Path) -> dict:
    info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
    title = next((l.split(":", 1)[1].strip() for l in info.splitlines() if l.startswith("Title:")), "")
    if not title or "Microsoft Word" in title or len(title) < 8:
        first = subprocess.run(["pdftotext", "-l", "1", str(pdf), "-"], capture_output=True,
                               text=True).stdout
        lines = [l.strip() for l in first.splitlines() if len(l.strip()) > 12]
        title = lines[0] if lines else pdf.stem
    year = re.search(r"(19|20)\d{2}", pdf.stem)
    return {"title": title, "authors": [], "year": int(year.group(0)) if year else 0}


def make_id(meta: dict, fallback: str) -> str:
    surname = (meta.get("authors") or [""])[0].split()[-1:] or [""]
    word = next((w for w in re.findall(r"[A-Za-z][A-Za-z0-9-]+", meta.get("title", ""))
                 if w.lower() not in {"a", "an", "the", "on", "of", "for", "and", "via", "with",
                                      "towards", "learning", "deep"}), fallback)
    raw = f"{surname[0]}{meta.get('year', '')}{word}".lower()
    return re.sub(r"[^a-z0-9]", "", raw) or re.sub(r"[^a-z0-9]", "", fallback.lower())


def append_entry(entry: dict) -> None:
    """Append without re-dumping the whole file, so comments and ordering survive."""
    text = catalog.CATALOG.read_text(encoding="utf-8")
    block = yaml.safe_dump([entry], sort_keys=False, allow_unicode=True, width=100)
    block = "\n".join("  " + l if l else l for l in block.splitlines())
    marker = "\npaths:"
    if marker in text:
        i = text.index(marker)
        text = text[:i].rstrip() + "\n" + block + "\n" + text[i:]
    else:
        text = text.rstrip() + "\n" + block + "\n"
    catalog.CATALOG.write_text(text, encoding="utf-8")


def add_category(slug: str, title: str) -> None:
    text = catalog.CATALOG.read_text(encoding="utf-8")
    line = f"  {slug}:\n    title: {title}\n    description: \"\"\n"
    text = text.replace("categories:\n", "categories:\n" + line, 1)
    catalog.CATALOG.write_text(text, encoding="utf-8")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("pdf", nargs="?", type=Path)
    ap.add_argument("--category", help="category slug, e.g. reinforcement-learning/policy-optimization")
    ap.add_argument("--new-category", metavar="TITLE", help="create --category with this title")
    ap.add_argument("--id", help="citekey; default firstauthorYEARword")
    ap.add_argument("--arxiv", help="arXiv id (metadata + download if no pdf given)")
    ap.add_argument("--move", action="store_true", help="move the PDF instead of copying it")
    ap.add_argument("--list-categories", action="store_true")
    args = ap.parse_args(argv)

    cat = catalog.load()
    if args.list_categories:
        for slug, info in (cat.get("categories") or {}).items():
            print(f"{slug:48s} {info.get('title', '')}")
        return 0
    if not args.category:
        ap.error("--category is required (see --list-categories)")
    if args.category not in (cat.get("categories") or {}):
        if not args.new_category:
            ap.error(f"unknown category {args.category!r}; pass --new-category 'Title' to create it")
        add_category(args.category, args.new_category)

    arxiv_id = args.arxiv
    if not arxiv_id and args.pdf:
        m = ARXIV_RE.search(args.pdf.name)
        arxiv_id = m.group(1) if m else None
    meta = {}
    if arxiv_id:
        try:
            meta = arxiv_meta(arxiv_id)
        except Exception as e:  # offline, or not an arXiv paper
            print(f"(arXiv lookup failed: {e}; falling back to the PDF)")
    if not args.pdf and not arxiv_id:
        ap.error("give a PDF path or --arxiv")
    if args.pdf and not meta:
        meta = pdf_meta(args.pdf)

    pid = args.id or make_id(meta, (args.pdf.stem if args.pdf else arxiv_id))
    if any(p.get("id") == pid for p in cat.get("papers") or []):
        ap.error(f"id {pid!r} already in the catalog (choose another with --id)")
    dest = ROOT / "library" / args.category / f"{pid}.pdf"
    dest.parent.mkdir(parents=True, exist_ok=True)
    if args.pdf:
        (shutil.move if args.move else shutil.copy2)(str(args.pdf), dest)
    else:
        urllib.request.urlretrieve(f"https://arxiv.org/pdf/{arxiv_id}", dest)

    entry = {
        "id": pid, "title": meta.get("title", ""), "short_name": "",
        "authors": meta.get("authors", []), "year": meta.get("year", 0), "venue": "",
        "arxiv": arxiv_id or "", "doi": "", "category": args.category, "tags": [],
        "pdf": dest.relative_to(ROOT).as_posix(), "status": "unread",
        "one_liner": "", "key_ideas": [], "builds_on": [], "cites": [], "videos": [],
    }
    append_entry(entry)
    print(f"added {pid}: {entry['title']}\n  -> {entry['pdf']}")
    print("Fill in one_liner / key_ideas / builds_on in library/catalog.yaml "
          "(or ask Claude: 'catalogue the new paper <id>').")
    return catalog.main([])


if __name__ == "__main__":
    sys.exit(main())
