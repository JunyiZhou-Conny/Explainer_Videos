#!/usr/bin/env python3
"""Render an authored episode from script.json + saved production defaults.

Examples:
  .venv/bin/python tools/render_episode.py videos/skills-ecosystem --sample s01
  .venv/bin/python tools/render_episode.py videos/skills-ecosystem

This is a thin shim kept for compatibility (defaults.json names it as the runner);
the engine lives in explainer/episode.py and reuses the shared toolkit for speech,
measured captions, the composed score, burn-in and validation.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from explainer.episode import main

if __name__ == "__main__":
    main()
