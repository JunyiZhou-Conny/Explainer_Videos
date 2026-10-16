"""explainer.check reports leftover print() debugging in a scene and its helpers, not Terminal.print.

    PYTHONPATH=. python -m pytest -q tests/test_check_prints.py
"""

from explainer.check import debug_prints


def test_builtin_print_is_reported_in_the_scene_and_its_helpers(tmp_path):
    scenes = tmp_path / "scenes"
    scenes.mkdir()
    scene = scenes / "s01_hook.py"
    scene.write_text("class Hook:\n"
                     "    def construct(self):\n"
                     "        rows = t.print(self, ['ok'])       # the terminal helper: scene code\n"
                     "        print('DBG', rows)\n")
    (scenes / "common.py").write_text("def helper():\n    print(f'DBG {1}')\n    return 1\n")
    (scenes / "s02_other.py").write_text("x = 'print(\"in a string\")'\n# print('in a comment')\n")
    assert [(p.name, line) for p, line in debug_prints(scene)] == [("s01_hook.py", 4), ("common.py", 2)]


def test_a_clean_scene_reports_nothing(tmp_path):
    scene = tmp_path / "s01.py"
    scene.write_text("out = t.print(self, ['a'])\nlog.print('x')\n")
    assert debug_prints(scene) == []
