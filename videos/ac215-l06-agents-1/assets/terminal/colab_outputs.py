#!/usr/bin/env python3
"""Capture-only helper: copy what the three L06 Colab notebooks hold, without running them (they need an OpenAI key).

Usage: python3 -I colab_outputs.py <dir with the .ipynb files> <video dir>
Writes
  <video dir>/assets/source/colab/<notebook>/cell-NN.py|.md  every non-empty cell's source, unchanged (NN = 0-based
                                                              index in the .ipynb; Colab shows no numbers)
  <video dir>/assets/terminal/expected/colab-<notebook>-cNN-<slug>.txt   the saved output of selected cells
Saved outputs are the staff's last run, stored in the notebook (recorded, not re-run). Text is kept as saved, except:
ANSI colour codes are removed; carriage-return progress lines keep their last state; an HTML-only output is
reported by size (the Cheese Quiz widget's embedded quiz data, `const DATA = {...}`, is printed as JSON); the course
staff's names and e-mail addresses (the Newsletter's readers: its USERS list, cell 16, and the outputs
naming them) are replaced by <reader1>... / <email> (see redact()); the source file is then cell-16.redacted.py.
"""
import json, os, re, sys

NB_DIR, VIDEO = sys.argv[1], sys.argv[2]
NOTEBOOKS = {
    "cheese-quiz": ("L06_cheese_quiz.ipynb", "Cheese Quiz",
                    "https://colab.research.google.com/drive/14UKW-Z7kFPuCwVqyUFcLxeA1KF70fwfm",
                    "2026-09-23 (tool outputs carry generated_at 1790132526..)"),
    "travel-planner": ("L06_travel_planner.ipynb", "Travel Planner",
                       "https://colab.research.google.com/drive/1I_jJEHJsVkGxNoSC1c4wEoVF2QL6vCVY",
                       "date not stored (trip dates 2026-11-06..)"),
    "cheese-newsletter": ("L06_cheese_newsletter_harness.ipynb", "Cheese Newsletter - Harness",
                          "https://colab.research.google.com/drive/1nnHrJ4Si3tpgUQl6HqlcwxKymV1-ecPv",
                          "2026-09-20 13:27 UTC (footer of the saved HTML)"),
}
SELECT = {   # cells whose saved output becomes an expected/ file: index -> slug
    "cheese-quiz": {13: "download", 21: "base-llm", 25: "reasoning-llm", 26: "reasoning-steps", 31: "simple-agent",
                    38: "step1-basic-prompt", 39: "step2-prompt-engineering", 40: "step3-rag", 41: "step4-short-term-memory",
                    42: "step5-long-term-memory", 43: "step6-tool-outputs", 44: "step7-structured-output",
                    48: "fun-facts-tool", 49: "tool-agent", 50: "tools-called", 54: "remote-mcp",
                    57: "fastmcp-server", 59: "local-mcp", 64: "stilton", 65: "brie",
                    75: "guild-star-wars", 77: "guild-greek"},
    "travel-planner": {24: "turn1", 25: "turn2", 26: "turn3", 27: "turn4-yes", 29: "chat-loop"},
    "cheese-newsletter": {8: "install", 27: "run-demo", 30: "preview-1", 31: "preview-2"},
}
ANSI = re.compile(r"\x1b\[[0-9;?]*[ -/]*[@-~]|\x1b\][^\x07]*\x07")
EMAIL = re.compile(r"[\w.+-]+@[\w-]+(?:\.[\w-]+)+")
READERS = []   # first names in the Newsletter's USERS list (cell 16, course staff), read from the notebook below


def redact(text, nb):
    if nb != "cheese-newsletter":
        return text
    text = EMAIL.sub(lambda m: m.group(0) if m.group(0).endswith("@example.com") else "<email>", text)
    for k, name in enumerate(READERS, 1):
        text = re.sub(rf"\b{name}\b", f"<reader{k}>", text)
    return text


def plain(text):
    text = ANSI.sub("", text)
    out = []
    for line in text.split("\n"):
        if "\r" in line.rstrip("\r"):
            line = line.rstrip("\r").split("\r")[-1]
        out.append(line.rstrip())
    return "\n".join(out)


def html_text(h):
    h = re.sub(r"(?is)<(script|style)\b.*?</\1>", "", h)
    h = re.sub(r"(?i)<br\s*/?>|</(p|div|h[1-6]|li|tr)>", "\n", h)
    h = re.sub(r"<[^>]+>", "", h)
    h = h.replace("&amp;", "&").replace("&lt;", "<").replace("&gt;", ">").replace("&#x27;", "'").replace("&quot;", '"').replace("&nbsp;", " ")
    lines = [l.strip() for l in h.splitlines()]
    return "\n".join(l for l in lines if l)


for nb, (fname, title, link, when) in NOTEBOOKS.items():
    cells = json.load(open(os.path.join(NB_DIR, fname)))["cells"]
    if nb == "cheese-newsletter":
        READERS[:] = re.findall(r'"name":\s*"([^"]+)"', "".join(cells[16]["source"]))
    src_dir = os.path.join(VIDEO, "assets", "source", "colab", nb)
    os.makedirs(src_dir, exist_ok=True)
    for i, c in enumerate(cells):
        src = "".join(c["source"])
        if not src.strip():
            continue
        red = redact(src, nb) if (nb, i) == ("cheese-newsletter", 16) else src   # the USERS list
        ext = ".py" if c["cell_type"] == "code" else ".md"
        name = f"cell-{i:02d}{'.redacted' if red != src else ''}{ext}"
        with open(os.path.join(src_dir, name), "w") as f:
            f.write(red if red.endswith("\n") else red + "\n")
    exp_dir = os.path.join(VIDEO, "assets", "terminal", "expected")
    os.makedirs(exp_dir, exist_ok=True)
    for i, slug in SELECT[nb].items():
        c = cells[i]
        first = "".join(c["source"]).strip().splitlines()[0]
        parts = []
        for o in c.get("outputs", []):
            if o["output_type"] == "stream":
                parts.append(f"[{o['name']}]\n" + plain("".join(o["text"])).strip("\n"))
            elif o["output_type"] in ("display_data", "execute_result"):
                d = o["data"]
                if "text/markdown" in d:
                    parts.append("[display: markdown]\n" + "".join(d["text/markdown"]).strip("\n"))
                elif "text/html" in d and nb == "cheese-quiz":
                    h = "".join(d["text/html"])
                    m = re.search(r"const DATA = (\{.*?\});\s*\n", h, re.S)
                    if m:
                        parts.append(f"[display: HTML quiz widget, {len(h)} characters; its embedded quiz data:]\n"
                                     + json.dumps(json.loads(m.group(1)), indent=1, ensure_ascii=False))
                    else:
                        parts.append(f"[display: HTML, {len(h)} characters]\n" + plain("".join(d.get("text/plain", ""))))
                elif "text/html" in d and len("".join(d["text/html"])) > 400:
                    h = "".join(d["text/html"])
                    parts.append(f"[display: HTML, {len(h)} characters; its text:]\n" + html_text(h))
                else:
                    parts.append("[display]\n" + plain("".join(d.get("text/plain", ""))).strip("\n"))
            elif o["output_type"] == "error":
                parts.append("[error]\n" + plain("\n".join(o.get("traceback", []))))
        body = redact("\n\n".join(parts), nb)
        notes = " Course staff's names and e-mail addresses replaced by <reader1>.. / <email>." if body != "\n\n".join(parts) else ""
        header = (f"# recorded: Colab notebook \"{title}\" ({fname}; {link}), cell {i} (0-based index in the .ipynb; "
                  f"first line: {first!r}). Saved output of the staff's last run, {when}; not run here (needs an "
                  f"OpenAI API key). Extracted unchanged by assets/terminal/colab_outputs.py (ANSI codes removed).{notes}\n")
        with open(os.path.join(exp_dir, f"colab-{nb}-c{i:02d}-{slug}.txt"), "w") as f:
            f.write(header + body.rstrip() + "\n")
print("ok")
