display(HTML(Path(receipts[1]["path"]).read_text(encoding="utf-8")))
for receipt in receipts:
    display(FileLink(receipt["path"]))
