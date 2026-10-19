# check-only (B4): does the fixed book name match a key of book_mappings? (cli.py read with ast, not imported)
import ast, hashlib, os
tree = ast.parse(open("/app/cli.py").read())
keys = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign)
            and getattr(n.targets[0], "id", "") == "book_mappings")
fn = "Womans Institute Library of Cookery. Volume 2_ Milk, Butter and Cheese Eggs Vegetables.txt"
for label, name in [("split('.')[0]  (cli.py:178)", fn.split(".")[0]), ("os.path.splitext(...)[0]", os.path.splitext(fn)[0])]:
    print(f"{label}: {name!r} -> in book_mappings: {name in keys} | id prefix {hashlib.sha256(name.encode()).hexdigest()[:16]}")
