"""Offline safety checks for pinned asset downloads (stdlib unittest).

Run: python3.12 -m unittest discover -s tests -p 'test_runtime_assets.py'
"""
import hashlib
import importlib.machinery
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SCRIPT = Path(__file__).resolve().parents[1] / "tools/setup-runtime"
LOADER = importlib.machinery.SourceFileLoader("setup_runtime", str(SCRIPT))
SPEC = importlib.util.spec_from_loader(LOADER.name, LOADER)
setup = importlib.util.module_from_spec(SPEC)
LOADER.exec_module(setup)


class RuntimeAssetsTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.asset = "assets/fonts/example.ttf"
        self.good = b"trusted-font"
        self.manifest = {self.asset: {
            "url": "https://example.invalid/font.ttf", "bytes": len(self.good),
            "sha256": hashlib.sha256(self.good).hexdigest(),
        }}
        self.manifest_path = self.root / "assets/manifest.json"
        self.manifest_path.parent.mkdir()
        self.manifest_path.write_text(json.dumps(self.manifest))
        self.original_manifest = self.manifest_path.read_bytes()

    def test_good_download_is_checked_before_publication_and_manifest_is_unchanged(self):
        with patch.object(setup.urllib.request, "urlopen", return_value=io.BytesIO(self.good)):
            setup.prepare_assets(self.root)
        self.assertEqual((self.root / self.asset).read_bytes(), self.good)
        self.assertEqual(self.manifest_path.read_bytes(), self.original_manifest)
        self.assertEqual(list(self.root.rglob("*.partial")), [])

    def test_same_size_bad_hash_never_becomes_an_installed_asset(self):
        with patch.object(setup.urllib.request, "urlopen", return_value=io.BytesIO(b"x" * len(self.good))):
            with self.assertRaises(setup.SetupError):
                setup.prepare_assets(self.root)
        self.assertFalse((self.root / self.asset).exists())
        self.assertEqual(list(self.root.rglob("*.partial")), [])
        self.assertEqual(self.manifest_path.read_bytes(), self.original_manifest)

    def test_existing_modified_file_is_preserved_and_no_download_is_attempted(self):
        asset_path = self.root / self.asset
        asset_path.parent.mkdir()
        asset_path.write_bytes(b"changed-font")
        with patch.object(setup.urllib.request, "urlopen") as network:
            with self.assertRaises(setup.SetupError):
                setup.prepare_assets(self.root)
            network.assert_not_called()
        self.assertEqual(asset_path.read_bytes(), b"changed-font")

    def test_verify_only_missing_asset_is_offline_and_does_not_create_directories(self):
        with patch.object(setup.urllib.request, "urlopen") as network:
            with self.assertRaises(setup.SetupError):
                setup.prepare_assets(self.root, verify_only=True)
            network.assert_not_called()
        self.assertFalse((self.root / self.asset).parent.exists())

    def test_verify_only_accepts_good_local_asset_without_network(self):
        asset_path = self.root / self.asset
        asset_path.parent.mkdir()
        asset_path.write_bytes(self.good)
        with patch.object(setup.urllib.request, "urlopen") as network:
            setup.prepare_assets(self.root, verify_only=True)
            network.assert_not_called()

    def test_asset_without_expected_checksum_is_rejected_before_download(self):
        del self.manifest[self.asset]["sha256"]
        self.manifest_path.write_text(json.dumps(self.manifest))
        with patch.object(setup.urllib.request, "urlopen") as network:
            with self.assertRaises(setup.SetupError):
                setup.prepare_assets(self.root)
            network.assert_not_called()

    def test_path_traversal_is_rejected(self):
        record = self.manifest.pop(self.asset)
        self.manifest["assets/../../outside.ttf"] = record
        self.manifest_path.write_text(json.dumps(self.manifest))
        with self.assertRaises(setup.SetupError):
            setup.load_manifest(self.root)


if __name__ == "__main__":
    unittest.main()
