"""Check-only helper (NOT part of the tutorial). Lets a tutorial cli.py be imported without the
heavy packages it does not need for the check: any module in STUB that is not installed is
replaced by an empty stand-in module whose attributes are dummies. Nothing here talks to AWS."""
import importlib.abc
import importlib.machinery
import importlib.util
import sys
import types

STUB = ("tensorflow", "PIL", "sagemaker", "requests", "dask", "sklearn")


class _Dummy:
    def __init__(self, *a, **k):
        pass

    def __call__(self, *a, **k):
        return _Dummy()

    def __getattr__(self, name):
        return _Dummy()


class _Module(types.ModuleType):
    def __getattr__(self, name):
        if name.startswith("__"):
            raise AttributeError(name)
        return _Dummy


class _Finder(importlib.abc.MetaPathFinder, importlib.abc.Loader):
    def find_spec(self, name, path, target=None):
        if name.split(".")[0] not in STUB:
            return None
        for finder in sys.meta_path:
            if finder is self:
                continue
            try:
                spec = finder.find_spec(name, path, target)
            except Exception:
                spec = None
            if spec is not None:
                return None  # the real package is installed: use it
        return importlib.machinery.ModuleSpec(name, self, is_package=True)

    def create_module(self, spec):
        m = _Module(spec.name)
        m.__path__ = []
        return m

    def exec_module(self, module):
        pass


def install():
    sys.meta_path.insert(0, _Finder())
