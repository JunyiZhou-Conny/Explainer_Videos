#!/usr/bin/env python3
"""Resolve a short request into an editable episode brief; does not invent a script."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import re
import shutil
from workspace import resolve_workspace

SKILL = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('slug')
    parser.add_argument('--topic', required=True)
    parser.add_argument('--preset', choices=sorted(p.stem for p in (SKILL/'presets').glob('*.md')))
    parser.add_argument('--minutes', type=float)
    parser.add_argument('--narration-language')
    parser.add_argument('--workspace', type=Path)
    args = parser.parse_args()
    if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', args.slug):
        parser.error('Use a lowercase hyphenated episode slug.')
    spec = deepcopy(json.loads((SKILL/'defaults.json').read_text()))
    if args.preset: spec['preset'] = args.preset
    if args.minutes is not None:
        if args.minutes <= 0: parser.error('--minutes must be positive')
        spec['duration_seconds'] = round(args.minutes*60, 3)
    if args.narration_language: spec['narration']['language'] = args.narration_language
    try:
        workspace = resolve_workspace(args.workspace, spec, skill=SKILL)
    except ValueError as error:
        parser.error(str(error))
    target = workspace/'videos'/args.slug
    if target.exists(): parser.error(f'Episode already exists; inspect it before editing: {target}')
    target.mkdir(parents=True)
    style = SKILL/'presets'/f"{spec['preset']}.md"
    spec.update(topic=args.topic, skill_source='conny-explainer-video', scene_implementation_status='not-authored',
                sources=[], style_snapshot='style.md', style_sha256=hashlib.sha256(style.read_bytes()).hexdigest())
    spec['production']['workspace'] = '.'  # Relative to the checkout root, not the episode folder.
    (target/'episode.json').write_text(json.dumps(spec, ensure_ascii=False, indent=2)+'\n')
    shutil.copyfile(SKILL/'assets/storyboard-template.md', target/'storyboard.md')
    shutil.copyfile(style, target/'style.md')
    print(target)
    print('Brief created. Author script.json and matching scenes.py, then render a sample.')

if __name__ == '__main__': main()
