"""Portable skill CLI checks; no render runtime, network, or real-home writes.

Run with: python -m unittest discover -s tests -p test_skill_portability.py -v
"""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import venv


REPO = Path(__file__).resolve().parents[1]
SKILL_NAME = "conny-explainer-video"
SOURCE = REPO / "skill-library" / SKILL_NAME


def file_bytes(root):
    """Capture contents so refusals/idempotent runs can be checked for writes."""
    return {p.relative_to(root).as_posix(): p.read_bytes()
            for p in root.rglob("*") if p.is_file() and not p.is_symlink()}


class SkillPortabilityTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="explainer-skill-test-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.home = self.root / "home"
        self.home.mkdir()
        self.checkout = self.make_checkout("checkout")
        self.skill = self.checkout / "skill-library" / SKILL_NAME
        shutil.copytree(SOURCE, self.skill, ignore=shutil.ignore_patterns("__pycache__", ".installation.json"))
        self.environment = os.environ.copy()
        self.environment.pop("EXPLAINER_WORKSPACE", None)
        self.environment["PYTHONDONTWRITEBYTECODE"] = "1"

    def make_checkout(self, name):
        checkout = self.root / name
        (checkout / "tools").mkdir(parents=True)
        (checkout / "explainer").mkdir()
        # Workspace discovery requires the engine entry point, not its dependencies.
        (checkout / "tools" / "render_episode.py").write_text("# test runner\n")
        return checkout

    def run_helper(self, name, *arguments, cwd=None, skill=None, environment=None):
        return subprocess.run(
            [sys.executable, str((skill or self.skill) / "scripts" / name), *map(str, arguments)],
            cwd=cwd or self.root,
            env=environment or self.environment,
            capture_output=True, text=True, timeout=20,
        )

    def assert_success(self, result):
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def create_episode(self, slug="sample", *arguments, **kwargs):
        result = self.run_helper("new_episode.py", slug, "--topic", "How skills work", *arguments, **kwargs)
        self.assert_success(result)
        return self.checkout / "videos" / slug

    def test_repository_aliases_are_relative_and_resolve_to_canonical_skill(self):
        for directory in (".agents", ".claude"):
            with self.subTest(directory=directory):
                alias = REPO / directory / "skills" / SKILL_NAME
                self.assertTrue(alias.is_symlink())
                self.assertFalse(Path(os.readlink(alias)).is_absolute())
                self.assertEqual(alias.resolve(strict=True), SOURCE.resolve(strict=True))

    def test_null_workspace_scaffolds_from_nested_checkout_and_freezes_style(self):
        defaults_path = self.skill / "defaults.json"
        defaults_before = defaults_path.read_bytes()
        defaults = json.loads(defaults_before)
        self.assertIsNone(defaults["production"]["workspace"])
        nested = self.checkout / "videos" / "existing" / "notes"
        nested.mkdir(parents=True)
        episode = self.create_episode(cwd=nested)
        spec = json.loads((episode / "episode.json").read_text())
        self.assertEqual(spec["production"]["workspace"], ".")
        self.assertEqual(spec["preset"], defaults["preset"])
        self.assertEqual(spec["duration_seconds"], defaults["duration_seconds"])
        self.assertEqual(spec["topic"], "How skills work")
        self.assertEqual(spec["scene_implementation_status"], "not-authored")
        self.assertEqual(spec["sources"], [])
        snapshot = episode / spec["style_snapshot"]
        frozen = snapshot.read_bytes()
        self.assertEqual(spec["style_sha256"], hashlib.sha256(frozen).hexdigest())
        preset = self.skill / "presets" / (spec["preset"] + ".md")
        self.assertEqual(frozen, preset.read_bytes())
        preset.write_text("A later shared-preset revision\n")
        self.assertEqual(snapshot.read_bytes(), frozen)
        self.assertTrue((episode / "storyboard.md").is_file())
        self.assertFalse((episode / "script.json").exists())
        self.assertFalse((episode / "scenes.py").exists())
        self.assertEqual(defaults_path.read_bytes(), defaults_before)
        self.assertNotIn(str(self.root), (episode / "episode.json").read_text())

    def test_explicit_workspace_and_spec_overrides_take_precedence(self):
        explicit = self.make_checkout("explicit target")
        environmental = self.make_checkout("environment target")
        env = {**self.environment, "EXPLAINER_WORKSPACE": str(environmental)}
        result = self.run_helper(
            "new_episode.py", "overrides", "--topic", "A spacecraft panel",
            "--workspace", explicit, "--preset", "nasa-punk", "--minutes", "2.5",
            "--narration-language", "zh-CN", cwd=self.checkout, environment=env,
        )
        self.assert_success(result)
        spec = json.loads((explicit / "videos" / "overrides" / "episode.json").read_text())
        self.assertEqual(spec["preset"], "nasa-punk")
        self.assertEqual(spec["duration_seconds"], 150)
        self.assertEqual(spec["narration"]["language"], "zh-CN")
        self.assertFalse((environmental / "videos").exists())
        self.assertFalse((self.checkout / "videos").exists())

    def test_environment_workspace_overrides_saved_setting(self):
        configured = self.make_checkout("configured")
        environmental = self.make_checkout("environmental")
        defaults_path = self.skill / "defaults.json"
        defaults = json.loads(defaults_path.read_text())
        defaults["production"]["workspace"] = str(configured)
        defaults_path.write_text(json.dumps(defaults))
        env = {**self.environment, "EXPLAINER_WORKSPACE": str(environmental)}
        result = self.run_helper("new_episode.py", "environment", "--topic", "Topic", environment=env)
        self.assert_success(result)
        self.assertTrue((environmental / "videos" / "environment" / "episode.json").is_file())
        self.assertFalse((configured / "videos").exists())

    def test_existing_episode_is_preserved(self):
        episode = self.create_episode()
        (episode / "script.json").write_text('{"authored": true}\n')
        before = file_bytes(episode)
        result = self.run_helper("new_episode.py", "sample", "--topic", "Replacement topic")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("already exists", result.stderr)
        self.assertEqual(file_bytes(episode), before)

    def test_invalid_explicit_workspace_does_not_fall_back_to_checkout(self):
        invalid = self.root / "not-a-checkout"
        invalid.mkdir()
        result = self.run_helper("new_episode.py", "sample", "--topic", "Topic", "--workspace", invalid,
                                 cwd=self.checkout)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((invalid / "videos").exists())
        self.assertFalse((self.checkout / "videos").exists())

    def test_detached_skill_requires_a_workspace(self):
        detached = self.root / "standalone-skill"
        shutil.copytree(self.skill, detached)
        result = self.run_helper("new_episode.py", "sample", "--topic", "Topic", skill=detached)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("--workspace", result.stderr)
        self.assertFalse((self.root / "videos").exists())

    def test_invalid_slug_and_duration_leave_no_episode(self):
        for slug, arguments in (("../escape", ()), ("sample", ("--minutes", "0"))):
            with self.subTest(slug=slug, arguments=arguments):
                result = self.run_helper("new_episode.py", slug, "--topic", "Topic", *arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertFalse((self.checkout / "videos").exists())
        self.assertFalse((self.root / "escape").exists())

    def test_install_plan_is_read_only_and_apply_is_additive_and_idempotent(self):
        unrelated = self.home / ".agents" / "skills" / "another-skill" / "SKILL.md"
        unrelated.parent.mkdir(parents=True)
        unrelated.write_text("Keep this user's existing skill.\n")
        before = file_bytes(self.home)
        plan = self.run_helper("install.py", "--home", self.home)
        self.assert_success(plan)
        self.assertEqual(json.loads(plan.stdout)["mode"], "plan")
        self.assertEqual(file_bytes(self.home), before)
        self.assertFalse((self.home / ".claude").exists())

        result = self.run_helper("install.py", "--home", self.home, "--apply")
        self.assert_success(result)
        self.assertEqual(json.loads(result.stdout)["status"], "installed")
        target = self.home / ".agents" / "skills" / SKILL_NAME
        alias = self.home / ".claude" / "skills" / SKILL_NAME
        self.assertTrue(alias.is_symlink())
        self.assertEqual(alias.resolve(), target)
        self.assertEqual(unrelated.read_text(), "Keep this user's existing skill.\n")
        for relative, expected in file_bytes(self.skill).items():
            self.assertEqual((target / relative).read_bytes(), expected, relative)
        installed_before = file_bytes(target)
        manifest_mtime = (target / ".installation.json").stat().st_mtime_ns
        rerun = self.run_helper("install.py", "--home", self.home, "--apply")
        self.assert_success(rerun)
        self.assertEqual(json.loads(rerun.stdout)["status"], "already-installed")
        self.assertEqual(file_bytes(target), installed_before)
        self.assertEqual((target / ".installation.json").stat().st_mtime_ns, manifest_mtime)

    def test_installer_refuses_local_edits_without_replacing_them(self):
        self.assert_success(self.run_helper("install.py", "--home", self.home, "--apply"))
        target = self.home / ".agents" / "skills" / SKILL_NAME
        (target / "presets" / "swiss.md").write_text("Local customization\n")
        before = file_bytes(self.home)
        result = self.run_helper("install.py", "--home", self.home, "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("local changes", json.loads(result.stderr)["error"])
        self.assertEqual(file_bytes(self.home), before)

    def test_installer_checks_alias_collision_before_creating_canonical_target(self):
        alias = self.home / ".claude" / "skills" / SKILL_NAME
        alias.mkdir(parents=True)
        (alias / "SKILL.md").write_text("An existing independent skill\n")
        before = file_bytes(self.home)
        result = self.run_helper("install.py", "--home", self.home, "--apply")
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse((self.home / ".agents").exists())
        self.assertEqual(file_bytes(self.home), before)

    def test_render_wrapper_finds_episode_checkout_and_forwards_arguments(self):
        episode = self.create_episode()
        (episode / "script.json").write_text("{}\n")
        (episode / "scenes.py").write_text("# authored test scene\n")
        # Preserve the interpreter's stdlib configuration, including relocatable
        # runtimes whose binary cannot run from a bare symlink in another venv.
        venv.EnvBuilder(with_pip=False).create(self.checkout / ".venv")
        (self.checkout / "tools" / "render_episode.py").write_text(
            "import json, os, sys\nprint(json.dumps({'cwd': os.getcwd(), 'args': sys.argv[1:]}))\n"
        )
        unrelated = self.make_checkout("unrelated-current-directory")
        result = self.run_helper("render.py", episode, "--sample", "S01", "--prepare-only", "--jobs", "1",
                                 cwd=unrelated)
        self.assert_success(result)
        invocation = json.loads(result.stdout)
        self.assertEqual(invocation["cwd"], str(self.checkout))
        self.assertEqual(invocation["args"], [str(episode), "--defaults", str(self.skill / "defaults.json"),
                                             "--jobs", "1", "--sample", "S01", "--prepare-only"])


if __name__ == "__main__":
    unittest.main()
