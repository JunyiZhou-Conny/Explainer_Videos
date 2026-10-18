from IPython.display import HTML, FileLink, display

display(HTML(Path(receipts[0]["path"]).read_text(encoding="utf-8")))
for receipt in receipts:
    display(FileLink(receipt["path"]))
