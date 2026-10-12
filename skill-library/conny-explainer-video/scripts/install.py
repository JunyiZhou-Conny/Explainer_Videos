#!/usr/bin/env python3
"""Plan or add this one portable skill; never replace an existing path.

Python 3.9+, standard library only. Default mode is read-only.
"""

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import sys
from datetime import datetime, timezone


SKILL_NAME = "conny-explainer-video"
MANIFEST_NAME = ".installation.json"
MANIFEST_KIND = "conny-personal-skill-installation"
IGNORED_NAMES = {".git", "__pycache__", ".DS_Store", MANIFEST_NAME}


class InstallError(Exception):
    pass


def exists(path):
    return os.path.lexists(path)


def fingerprint(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return {"sha256": digest.hexdigest(), "size_bytes": path.stat().st_size}


def inventory(directory):
    files = {}
    for path in sorted(directory.rglob("*")):
        relative = path.relative_to(directory)
        if any(part in IGNORED_NAMES for part in relative.parts):
            continue
        if path.is_symlink():
            raise InstallError("Bundle symlinks are unsupported: " + str(path))
        if path.is_file():
            files[relative.as_posix()] = fingerprint(path)
        elif not path.is_dir():
            raise InstallError("Bundle contains a non-regular entry: " + str(path))
    return files


def validate_bundle(source):
    skill = source / "SKILL.md"
    if not skill.is_file() or skill.is_symlink():
        raise InstallError("Source must contain an ordinary SKILL.md file.")
    text = skill.read_text(encoding="utf-8")
    frontmatter = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
    if not frontmatter:
        raise InstallError("SKILL.md must start with YAML frontmatter.")
    name = re.search(r"(?m)^name:\s*['\"]?([^'\"\r\n]+)['\"]?\s*$", frontmatter[1])
    if not name or name[1].strip() != SKILL_NAME:
        raise InstallError("This installer only supports " + SKILL_NAME + ".")
    if not re.search(r"(?m)^description:\s*\S", frontmatter[1]):
        raise InstallError("SKILL.md requires a description.")
    try:
        preferences = json.loads((source / "defaults.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as error:
        raise InstallError("Cannot read valid defaults.json: " + str(error)) from error
    if not isinstance(preferences, dict) or preferences.get("schema_version") != 1:
        raise InstallError("defaults.json must use schema_version 1.")
    preset = preferences.get("preset")
    if not isinstance(preset, str) or not re.fullmatch(r"[a-z0-9]+(?:-[a-z0-9]+)*", preset):
        raise InstallError("defaults.json needs a valid preset name.")
    if not (source / "presets" / (preset + ".md")).is_file():
        raise InstallError("Default preset file is missing: presets/" + preset + ".md")


def check_parent_paths(home, roots):
    if not home.is_dir():
        raise InstallError("Installation home must already be a directory: " + str(home))
    for root in roots:
        relative = root.relative_to(home)
        current = home
        for component in relative.parts:
            current = current / component
            if exists(current) and (current.is_symlink() or not current.is_dir()):
                raise InstallError("Parent path must be an ordinary directory: " + str(current))


def inspect_existing(target, alias, files):
    target_state = "create"
    if exists(target):
        if target.is_symlink() or not target.is_dir():
            raise InstallError("Refusing to replace existing target: " + str(target))
        manifest_path = target / MANIFEST_NAME
        if manifest_path.is_symlink():
            raise InstallError("Refusing a symlinked installation manifest.")
        try:
            manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
        except (OSError, ValueError) as error:
            raise InstallError("Existing target is not an intact managed installation: " + str(target)) from error
        if not isinstance(manifest, dict) or any((
            manifest.get("kind") != MANIFEST_KIND,
            manifest.get("schema_version") != 1,
            manifest.get("skill_name") != SKILL_NAME,
            manifest.get("canonical_path") != str(target),
            manifest.get("claude_alias") != str(alias),
            manifest.get("files") != files,
        )):
            raise InstallError("Existing installation differs from this bundle; no files changed.")
        if inventory(target) != files:
            raise InstallError("Installed files contain local changes; no files changed.")
        target_state = "unchanged"
    alias_state = "create"
    if exists(alias):
        if not alias.is_symlink() or alias.resolve() != target:
            raise InstallError("Refusing to replace existing Claude path: " + str(alias))
        alias_state = "unchanged"
    return target_state, alias_state


def copy_exclusive(source, target, files):
    target.mkdir()  # Fail if another process created the target after planning.
    for relative, expected in files.items():
        source_file = source / relative
        if source_file.is_symlink():
            raise InstallError("Source changed to a symlink during installation: " + relative)
        data = source_file.read_bytes()
        if len(data) != expected["size_bytes"] or hashlib.sha256(data).hexdigest() != expected["sha256"]:
            raise InstallError("Source changed during installation: " + relative)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        with destination.open("xb") as handle:
            handle.write(data)
        destination.chmod(source_file.stat().st_mode & 0o777)
    if inventory(target) != files:
        raise InstallError("Post-copy file verification failed.")


def install(source, home, apply):
    source = source.resolve()
    home = home.resolve()
    validate_bundle(source)
    files = inventory(source)
    target = home / ".agents" / "skills" / SKILL_NAME
    alias = home / ".claude" / "skills" / SKILL_NAME
    if source == target:
        raise InstallError("Run the installer from an authoring/release bundle, not its installed target.")
    check_parent_paths(home, (target.parent, alias.parent))
    target_state, alias_state = inspect_existing(target, alias, files)
    result = {
        "mode": "apply" if apply else "plan",
        "skill_name": SKILL_NAME,
        "source": str(source),
        "canonical_path": str(target),
        "canonical_action": target_state,
        "claude_alias": str(alias),
        "claude_action": alias_state,
        "cursor_action": "none; uses native ~/.agents/skills discovery",
        "file_count": len(files),
        "total_bytes": sum(item["size_bytes"] for item in files.values()),
        "manifest": str(target / MANIFEST_NAME),
        "files": files,
        "discovery_verified": False,
    }
    if not apply:
        return result
    # Check every collision before the first write. No force or update mode exists.
    check_parent_paths(home, (target.parent, alias.parent))
    inspect_existing(target, alias, files)
    for parent in (target.parent, alias.parent):
        parent.mkdir(parents=True, exist_ok=True)
    if target_state == "create":
        copy_exclusive(source, target, files)
        manifest = {
            "kind": MANIFEST_KIND,
            "schema_version": 1,
            "skill_name": SKILL_NAME,
            "installed_at_utc": datetime.now(timezone.utc).isoformat(),
            "canonical_path": str(target),
            "claude_alias": str(alias),
            "provenance": {
                "source_bundle": str(source),
                "owner": "Conny",
                "authoring_assistance": "Codex",
                "reference_attribution": "See each preset's sources and evidence notes.",
            },
            "files": files,
            "discovery_verified": False,
        }
        with (target / MANIFEST_NAME).open("x", encoding="utf-8") as handle:
            json.dump(manifest, handle, indent=2, ensure_ascii=False)
            handle.write("\n")
    if alias_state == "create":
        alias.symlink_to(target, target_is_directory=True)
    if alias.resolve() != target or inventory(target) != files:
        raise InstallError("Post-install verification failed; inspect the reported paths.")
    result["status"] = "already-installed" if target_state == alias_state == "unchanged" else "installed"
    result["verified"] = ["copied file hashes", "Claude alias target"]
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--apply", action="store_true", help="Apply the additive plan; otherwise read-only.")
    parser.add_argument("--home", type=Path, default=Path.home(), help="Existing installation home; useful for isolated verification.")
    args = parser.parse_args()
    source = Path(__file__).resolve().parents[1]
    try:
        result = install(source, args.home.expanduser().resolve(), args.apply)
    except (InstallError, OSError, RuntimeError) as error:
        print(json.dumps({"status": "refused-or-incomplete", "error": str(error),
                          "note": "No existing file is replaced. A failure after writes may leave the new bundle for inspection."}, indent=2), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
