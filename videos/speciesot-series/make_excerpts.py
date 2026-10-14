"""Regenerate excerpts.py from an unpacked copy of Josh's src/speciesot.

    python3 videos/speciesot-series/make_excerpts.py <path to src/speciesot>

Writes only the lines the series shows (real line numbers), the four Tests/ files, the
e24_replica notebook cells and outputs, line lengths for the file-shape minimap, and the
sha256 of every source. After a regeneration, re-check every line number quoted in the five
episodes' script.json: a changed hash means the code moved.
"""
import hashlib
import json
import sys
from pathlib import Path

RANGES = [(1, 159), (161, 186), (212, 294), (300, 335)]
TESTS = ["config.yaml", "toy_config.yaml", "test_evaluation.py", "test_model.py"]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main(src):
    src = Path(src)
    core = src.joinpath("speciesot_core.py").read_text().splitlines()
    excerpt = {n: core[n - 1] for a, b in RANGES for n in range(a, b + 1)}
    files = {k: src / "Tests" / k for k in TESTS}
    whole = {k: {i + 1: l for i, l in enumerate(p.read_text().splitlines())}
             for k, p in files.items()}
    nb = json.loads((src / "Tests/e24_replica.ipynb").read_text())
    cells = ["".join(c["source"]) for c in nb["cells"]]
    outs = []
    for c in nb["cells"]:
        o = ""
        for x in c.get("outputs", []):
            if "text" in x:
                o += "".join(x["text"])
            elif "data" in x:
                o += "".join(x["data"].get("text/plain", ""))
        outs.append(o)
    hashes = {"speciesot_core.py": sha(src / "speciesot_core.py"),
              **{k: sha(p) for k, p in files.items()},
              "e24_replica.ipynb": sha(src / "Tests/e24_replica.ipynb")}
    lens = [len(l.rstrip()) for l in core]
    kinds = "".join("c" if l.strip().startswith("#") else ("b" if not l.strip() else "x")
                    for l in core)
    out = ['"""Excerpts of Josh\'s speciesot package, as attached by Conny on 2026-10-14.',
           "",
           "Only the lines the series shows on screen. Line numbers are the real ones. Regenerate",
           "with make_excerpts.py; the sha256 of each source file is recorded below so a changed",
           "source is noticed.",
           '"""', "",
           f"SOURCE_SHA256 = {json.dumps(hashes, indent=4)}", "",
           f"CORE = {json.dumps(excerpt, indent=0, ensure_ascii=False)}", ""]
    for k, v in whole.items():
        out.append(f"{k.split('.')[0].upper()} = {json.dumps(v, indent=0, ensure_ascii=False)}")
        out.append("")
    out.append(f"E24_CELLS = {json.dumps(cells, indent=0, ensure_ascii=False)}")
    out.append("")
    out.append(f"E24_OUTPUTS = {json.dumps(outs, indent=0, ensure_ascii=False)}")
    out.append("")
    out.append("# Length and kind of every line of speciesot_core.py (x = code, c = comment, "
               "b = blank),\n# for the file-shape minimap. No content.")
    out.append(f"LINE_LENGTHS = {lens}")
    out.append(f'LINE_KINDS = "{kinds}"')
    out.append('''

def _int_keys(d):
    return {int(k): v for k, v in d.items()}


CORE = _int_keys(CORE)
CONFIG = _int_keys(CONFIG)
TOY_CONFIG = _int_keys(TOY_CONFIG)
TEST_EVALUATION = _int_keys(TEST_EVALUATION)
TEST_MODEL = _int_keys(TEST_MODEL)


def rows(source, a, b):
    """[(line_number, text)] for lines a..b of an excerpt dict."""
    return [(n, source[n]) for n in range(a, b + 1)]
''')
    Path(__file__).with_name("excerpts.py").write_text("\n".join(out))


if __name__ == "__main__":
    main(sys.argv[1])
