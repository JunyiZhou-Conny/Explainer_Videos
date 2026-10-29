# notebook.py: runs chosen code cells of a notebook (the copies in assets/source/colab/) into one namespace, as
# Colab would, skipping the install and key cells; display() prints.
import pathlib
def run_cells(notebook, cells, ns=None):
    ns = {} if ns is None else ns
    ns.setdefault("display", print)
    for c in cells:
        src = pathlib.Path(f"/cells/{notebook}/cell-{c}.py").read_text()
        exec(compile(src, f"{notebook}/cell-{c}", "exec"), ns)
    return ns
