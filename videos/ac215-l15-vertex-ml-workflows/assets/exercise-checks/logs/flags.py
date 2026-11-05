"""Check-only helper (NOT part of the tutorial). B4: which work functions run when you pass two flags?
Imports each tutorial cli.py as a module (TensorFlow and Pillow stubbed if absent; the workflow
CLI's module-level account lookup answered with a placeholder), replaces its work functions by
prints, then runs the file's own `if __name__ == "__main__":` block (its parser and main()) with
the given argv. Nothing calls AWS."""
import ast
import importlib.util
import sys

sys.path.insert(0, "/checks")
import stubs  # noqa: E402

stubs.install()
import boto3  # noqa: E402


class PlaceholderSTS:
    def get_caller_identity(self, **kwargs):
        return {"Account": "000000000000"}


_client = boto3.client
boto3.client = lambda name, *a, **k: PlaceholderSTS() if name == "sts" else _client(name, *a, **k)


def run(path, funcs, argv):
    sys.path.insert(0, path.rsplit("/", 1)[0])
    spec = importlib.util.spec_from_file_location("cli_under_test", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    for f in funcs:
        setattr(mod, f, (lambda name: lambda *a, **k: print(f"  -> {name}() would run"))(f))
    tree = ast.parse(open(path).read())
    block = next(n for n in tree.body if isinstance(n, ast.If) and "__main__" in ast.unparse(n.test))
    sys.argv = ["cli.py"] + argv
    print(f"$ python cli.py {' '.join(argv)}    # {path}")
    exec(compile(ast.Module(body=block.body, type_ignores=[]), path, "exec"), mod.__dict__)
    sys.path.pop(0)


run("/md/cli.py", ["prepare", "deploy", "predict", "delete"], ["--prepare", "--deploy"])
run("/md/cli.py", ["prepare", "deploy", "predict", "delete"], ["--test"])
run("/wf/cli.py", ["data_collector", "data_processor", "model_training", "model_deploy", "pipeline"],
    ["--data_collector", "--data_processor"])
