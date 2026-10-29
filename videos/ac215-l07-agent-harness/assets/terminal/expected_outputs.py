#!/usr/bin/env python3
"""Capture-only helper: copy what the tutorial documents for the steps that cannot run here, without running anything.

Usage: python3 -I expected_outputs.py <L07_agent_harness.ipynb> <video dir>
Writes
  <video dir>/assets/source/colab/cell-NN.py|.md    every non-empty cell of the course Colab, its source unchanged
                                                    (NN = 0-based index in the .ipynb; Colab shows no numbers)
  <video dir>/assets/terminal/expected/colab-cNN-<slug>.txt   the saved output of every executed cell (the staff's
                                                    last run, stored in the notebook; recorded, not re-run)
  <video dir>/assets/terminal/expected/readme-<slug>.txt      README passages that say what a live command prints
                                                    or what to look for (README text, not program output)
Each expected/ file's first line says exactly where it comes from. Text is kept as saved, except: ANSI colour codes
are removed; a DataFrame keeps its text view; an HTML-only output (cell 18's styled table, cell 24's chat view) is
turned into its visible text (tags removed, one block or table row per line, cells joined by " | "); and the two full
names of the course staff (the `name` fields of data/customers.json, read from assets/source/) are replaced by
<name> wherever they occur (cell 0's header -> cell-00.redacted.md; cell 16's customers table). The CLI and the
context packets use only the customer IDs.
"""
import html, json, os, re, sys

NB, VIDEO = sys.argv[1], sys.argv[2]
COLAB = "https://colab.research.google.com/drive/1ZYMsbG0gqsbs-6Pcj8WtT3WhEa4f80EZ"
REPO = "dlops-io/agent-harness, main @ e25dfe9615d78b78e0764a636cc2462f530a1402"
SRC = os.path.join(VIDEO, "assets", "source")
EXP = os.path.join(VIDEO, "assets", "terminal", "expected")
SLUG = {8: "install", 11: "utils", 13: "catalog", 14: "policies", 15: "pairings", 16: "customers",
        17: "request", 18: "data-constraints", 21: "bare-agent", 23: "agent-harness", 24: "response-view"}
# README passages for the live commands (and two notes the scenes quote); line ranges are 1-based and inclusive.
README = [
    ("act1-standard", 175, 200, "Run Act 1: the standard scenario, what the console shows, what to look for"),
    ("act1-missing-details", 242, 252, "Try a variation: missing-details, and the checkpoint"),
    ("act2-intro", 258, 266, "2. Context Engineering: personalized vs basic, what the comparison measures"),
    ("act2-pa-ny", 277, 281, "the PA/NY counterexample each individual Act 2 command prints"),
    ("act3-pa-shipping-preview", 283, 290, "the live Act 3 rejection-and-revision preview inside the Act 2 section"),
    ("act2-evaluate-live", 292, 301, "repeat the context cases: 12 live runs"),
    ("act2-standard", 316, 330, "Optional baseline with overlapping preferences"),
    ("act3-standard", 361, 367, "Act 3 live: what to look for"),
    ("act3-shipping-lesson", 369, 402, "Live PA shipping lesson: what the before and after runs should show"),
    ("act3-manager-fixture", 404, 410, "the scripted manager-approval fixture ($220.80)"),
    ("act4-live", 454, 471, "Act 4 live: the event brief, the stock shortfall, what to look for"),
    ("act4-memory", 481, 488, "Optional memory exercise (live)"),
    ("act5-live", 537, 545, "Run Act 5 (live): what to look for"),
    ("act5-stock-question", 549, 555, "Try selective loading: 900 g, no skill bodies"),
    ("act6-live", 631, 641, "Act 6 live: what to look for; finishing vs delivering"),
    ("act6-two-orders", 643, 658, "Try two competing orders"),
    ("eval-live-compare", 723, 751, "Step 3: a small live comparison"),
    ("eval-judge", 753, 765, "Step 4: what the checks do and do not establish"),
    ("verify", 118, 133, "Verify the environment: the test suite should finish with OK"),
    ("act2-compare-notes", 849, 866, "Act 2 comparison command"),
]
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07")
NAMES = [c["name"] for c in json.load(open(os.path.join(SRC, "data", "customers.json"), encoding="utf-8"))]


def redact(text):
    for name in NAMES:
        text = text.replace(name, "<name>")
    return text


def plain(text):
    text = ANSI.sub("", text)
    out = []
    for line in text.split("\n"):
        if "\r" in line.rstrip("\r"):
            line = line.rstrip("\r").split("\r")[-1]
        out.append(line.rstrip())
    return "\n".join(out)


OBJ_REPR = re.compile(r"^<[\w.]+( object)?( at 0x[0-9a-f]+)?>$")   # e.g. <IPython.core.display.HTML object>


def html_text(h):
    h = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", h)
    h = re.sub(r"(?is)<tr\b.*?</tr>", lambda m: re.sub(r"\s*\n\s*", " ", m.group(0)), h)   # one table row per line
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|h[1-6]|li|tr|summary|pre|header|section|details|table|thead|tbody)>", "\n", h)
    h = re.sub(r"(?i)</t[dh]>", "\t", h)
    h = re.sub(r"(?i)</span>", " ", h)                    # badges side by side stay apart
    h = re.sub(r"<[^>]+>", "", h)
    h = html.unescape(h)
    lines = [re.sub(r"[ \t]+", " ", l.replace("\t", " | ")).strip(" |") for l in h.splitlines()]
    return "\n".join(l for l in lines if l)


cells = json.load(open(NB, encoding="utf-8"))["cells"]
src_dir = os.path.join(SRC, "colab")
os.makedirs(src_dir, exist_ok=True)
os.makedirs(EXP, exist_ok=True)
for i, c in enumerate(cells):
    src = "".join(c["source"])
    if not src.strip():
        continue
    ext = ".py" if c["cell_type"] == "code" else ".md"
    clean = redact(src)
    name = f"cell-{i:02d}{'.redacted' if clean != src else ''}{ext}"
    with open(os.path.join(src_dir, name), "w", encoding="utf-8") as f:
        f.write(clean if clean.endswith("\n") else clean + "\n")

for i, slug in SLUG.items():
    c = cells[i]
    src = "".join(c["source"])
    title = src.splitlines()[0].removeprefix("# @title ").removeprefix("# ").strip()
    parts = []
    for o in c.get("outputs", []):
        if o["output_type"] == "stream":
            parts.append(plain("".join(o["text"])).rstrip("\n"))
        elif "data" in o:
            d = o["data"]
            text = "".join(d.get("text/plain", ""))
            if text and not OBJ_REPR.match(text.strip()):     # a DataFrame or string: its text view, as Jupyter prints it
                parts.append(plain(text))
            elif "text/html" in d:                              # a Styler or the chat view: the HTML's visible text
                parts.append(html_text("".join(d["text/html"])))
        elif o["output_type"] == "error":
            parts.append(plain("\n".join(o.get("traceback", []))))
    body = redact("\n".join(parts))
    head = (f"# recorded (saved output of the course Colab \"Agent Harness\", not re-run here): {COLAB}, cell {i} "
            f"(\"{title}\"), execution count {c.get('execution_count')}; the notebook stores no date."
            + (" The two staff names are replaced by <name>." if body != "\n".join(parts) else ""))
    with open(os.path.join(EXP, f"colab-c{i:02d}-{slug}.txt"), "w", encoding="utf-8") as f:
        f.write(head + "\n" + body.rstrip("\n") + "\n")

readme = open(os.path.join(SRC, "README.md"), encoding="utf-8").read().split("\n")
for slug, a, b, what in README:
    head = (f"# expected (README text, not program output): {REPO}, README.md:{a}-{b} ({what}), unchanged.")
    with open(os.path.join(EXP, f"readme-{slug}.txt"), "w", encoding="utf-8") as f:
        f.write(head + "\n" + "\n".join(readme[a - 1:b]).rstrip("\n") + "\n")
