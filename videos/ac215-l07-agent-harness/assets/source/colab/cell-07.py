# @title Setup Agent Harness Repo
from pathlib import Path
import os
import subprocess
import sys

root = Path.cwd()
if not (root / "formaggio" / "config.py").exists():
    if (root.parent / "formaggio" / "config.py").exists():
        root = root.parent
    else:
        root = root / "agent-harness"
        if not root.exists():
            subprocess.run(["git", "clone", "https://github.com/dlops-io/agent-harness.git", str(root)], check=True)
os.chdir(root)
if str(root) not in sys.path:
    sys.path.insert(0, str(root))
print("Repository:", root)
