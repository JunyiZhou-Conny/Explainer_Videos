#!/usr/bin/env python3
"""Run the configured local engine against an authored episode, without shell evaluation."""
import argparse
import json
from pathlib import Path
import subprocess
import sys
from workspace import resolve_workspace

SKILL = Path(__file__).resolve().parents[1]

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('episode', type=Path)
    parser.add_argument('--sample')
    parser.add_argument('--prepare-only', action='store_true')
    parser.add_argument('--jobs', type=int, default=2)
    parser.add_argument('--workspace', type=Path)
    args = parser.parse_args()
    settings = json.loads((SKILL/'defaults.json').read_text())
    episode = args.episode.expanduser().resolve()
    try:
        root = resolve_workspace(args.workspace, settings, start=episode, skill=SKILL)
    except ValueError as error:
        parser.error(str(error))
    configured = settings['production'].get('runner')
    if not configured: parser.error('No runner configured in defaults.json.')
    runner = Path(configured).expanduser()
    if not runner.is_absolute(): runner = root/runner
    python = root/'.venv/bin/python'
    for path in (runner, python, episode/'script.json', episode/'scenes.py'):
        if not path.is_file(): parser.error(f'Required file missing: {path}')
    command = [str(python), str(runner), str(episode), '--defaults', str(SKILL/'defaults.json'), '--jobs', str(args.jobs)]
    if args.sample: command += ['--sample', args.sample]
    if args.prepare_only: command += ['--prepare-only']
    raise SystemExit(subprocess.run(command, cwd=root).returncode)

if __name__ == '__main__': main()
