"""Why Marco's table reader (extract v5, doas_tables.py) refuses the real 2026 Side-by-Side PDF.

For each page: the ruled tables PyMuPDF finds (strategy "lines", as doas_tables uses), their column
count, and the first rows. doas_tables needs one row with exactly 7 cells whose cells 2-7 name the
six programs of that page. Usage: python -I doas_pages.py <nj_doas_programs_side_by_side_2026.pdf>"""
import json
import sys

import pymupdf

doc = pymupdf.open(sys.argv[1])
report = []
for i, page in enumerate(doc, 1):
    tables = []
    for t in page.find_tables(strategy="lines").tables:
        rows = t.extract()
        tables.append({"columns": t.col_count, "rows": t.row_count,
                       "first_rows": [[" ".join((c or "").split())[:24] for c in r] for r in rows[:3]]})
    report.append({"page": i, "tables": tables})
    for t in tables:
        print(f"page {i}: {t['columns']} columns x {t['rows']} rows")
        for r in t["first_rows"]:
            print("   ", r)
json.dump(report, sys.stdout if len(sys.argv) < 3 else open(sys.argv[2], "w"), indent=1)
