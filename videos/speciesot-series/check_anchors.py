"""Static check: every vo.wait_until("phrase") in scenes.py occurs in the narration line of
the `with self.say(i)` block it sits in, and every say(i) index exists. No rendering.

    python3 videos/speciesot-series/check_anchors.py videos/speciesot-e1-blueprint [...]
"""
import ast
import json
import sys
from pathlib import Path


def check(project):
    project = Path(project)
    script = json.loads((project / "script.json").read_text())
    lines = {s["id"].upper(): [l["en"] for l in s["lines"]] for s in script["scenes"]}
    tree = ast.parse((project / "scenes.py").read_text())
    problems, used = [], {}
    for cls in [n for n in tree.body if isinstance(n, ast.ClassDef) and n.name in lines]:
        said = set()
        for node in ast.walk(cls):
            if not isinstance(node, ast.With):
                continue
            for item in node.items:
                call = item.context_expr
                if (isinstance(call, ast.Call) and isinstance(call.func, ast.Attribute)
                        and call.func.attr == "say" and call.args
                        and isinstance(call.args[0], ast.Constant)):
                    i = call.args[0].value
                    said.add(i)
                    if i >= len(lines[cls.name]):
                        problems.append(f"{cls.name}: say({i}) but the scene has "
                                        f"{len(lines[cls.name])} lines")
                        continue
                    text = lines[cls.name][i]
                    for sub in ast.walk(node):
                        if (isinstance(sub, ast.Call) and isinstance(sub.func, ast.Attribute)
                                and sub.func.attr in ("wait_until", "until", "time_until")
                                and sub.args and isinstance(sub.args[0], ast.Constant)):
                            phrase = sub.args[0].value
                            if phrase not in text and phrase.lower() not in text.lower():
                                problems.append(f"{cls.name} say({i}): anchor {phrase!r} not in "
                                                f"{text[:70]!r}…")
        used[cls.name] = said
        # say(i) inside a loop (e.g. range) can't be resolved statically; only report gaps
        # when every index is a literal.
        if said and said != set(range(len(lines[cls.name]))) and not any(
                isinstance(n, ast.For) for n in ast.walk(cls)):
            problems.append(f"{cls.name}: voices lines {sorted(said)} of "
                            f"{len(lines[cls.name])}")
    missing = set(lines) - {c.name for c in tree.body if isinstance(c, ast.ClassDef)}
    problems += [f"{m}: no scene class" for m in sorted(missing)]
    return problems


if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        probs = check(p)
        bad += len(probs)
        print(f"{Path(p).name}: {'ok' if not probs else ''}")
        for pr in probs:
            print("  -", pr)
    sys.exit(1 if bad else 0)
