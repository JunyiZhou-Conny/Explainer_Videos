#!/usr/bin/env python3
"""Offline checks for the shared styles, episode snapshot and release catalog."""
from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / 'skill-library/conny-explainer-video'


def check():
    defaults = json.loads((SKILL/'defaults.json').read_text())
    assert defaults['production']['workspace'] is None, 'Shared defaults must be portable'
    for name in ('.agents', '.claude'):
        alias = ROOT/name/'skills/conny-explainer-video'
        assert alias.is_symlink() and alias.resolve() == SKILL, f'Broken alias: {name}'
    styles = json.loads((ROOT/'catalog/styles.json').read_text())['styles']
    assert {s['id'] for s in styles} == {p.stem for p in (SKILL/'presets').glob('*.md')}
    for style in styles:
        path = ROOT/style['path']
        assert hashlib.sha256(path.read_bytes()).hexdigest() == style['sha256'], f'Update catalog hash: {style["id"]}'
    for spec_path in (ROOT/'videos').glob('*/episode.json'):
        spec = json.loads(spec_path.read_text())
        snapshot = spec_path.parent/spec['style_snapshot']
        assert hashlib.sha256(snapshot.read_bytes()).hexdigest() == spec['style_sha256'], f'Style snapshot changed: {spec_path.parent.name}'
    catalog = json.loads((ROOT/'catalog/videos.json').read_text())
    keys = [(v['source_commit'], v['path']) for v in catalog['artifacts']]
    assert len(keys) == len(set(keys)), 'Duplicate video variants'
    release = json.loads((ROOT/'catalog/release-media.json').read_text())
    selected = {v['release_asset']:v for v in catalog['artifacts'] if 'release_asset' in v}
    assert set(selected) == {v['filename'] for v in release['files']}, 'Release inventory differs'
    for video in release['files']:
        expected = selected[video['filename']]
        assert video['decode_passed'] and video['bytes'] == expected['bytes'] and video['sha256'] == expected['sha256']
        assert any(s['codec_type']=='audio' for s in video['probe']['streams']), 'Missing narration stream'
    # Only inspect the curated public bundle, not private inventories or ignored runtime files.
    paths = [ROOT/'AGENTS.md', ROOT/'CLAUDE.md', ROOT/'README.md']
    for folder in ('skill-library', 'catalog', 'videos/skills-ecosystem'):
        paths += [p for p in (ROOT/folder).rglob('*') if p.is_file() and p.suffix in ('.md','.json','.py','.yaml')]
    for path in paths:
        text = path.read_text()
        assert not re.search(r'/Users/[^/\s]+/|/var/folders/', text), f'Personal absolute path: {path.relative_to(ROOT)}'
    print(f'Checked {len(styles)} presets, {len(keys)} video variants, {len(selected)} release masters and relative agent aliases.')


if __name__ == '__main__':
    check()
