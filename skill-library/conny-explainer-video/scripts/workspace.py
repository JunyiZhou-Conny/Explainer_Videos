"""Locate a production checkout without saving a machine-specific home path."""
import os
from pathlib import Path


def resolve_workspace(explicit=None, settings=None, start=None, skill=None):
    configured = (settings or {}).get('production', {}).get('workspace')
    chosen = explicit or os.environ.get('EXPLAINER_WORKSPACE') or configured
    if chosen:
        root = Path(chosen).expanduser().resolve()
        if not (root / 'tools/render_episode.py').is_file():
            raise ValueError(f'No episode runner in {root}; use --workspace with the repository root.')
        return root
    for origin in (start, Path.cwd(), skill):
        if origin is None:
            continue
        path = Path(origin).expanduser().resolve()
        for root in (path, *path.parents):
            if (root / 'tools/render_episode.py').is_file() and (root / 'explainer').is_dir():
                return root
    raise ValueError('Open the Explainer_Videos checkout, or set --workspace / EXPLAINER_WORKSPACE.')
