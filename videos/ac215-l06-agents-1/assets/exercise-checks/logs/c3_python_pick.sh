# c4_python_pick.sh: which Python does the README's `uv sync` pick on a laptop that HAS a Python of its own
# (the check laptop's system Python 3.12.15), before and after uv has downloaded a 3.15 for some other project?
# A throwaway home and a fresh clone (no .python-version); `uv sync --dry-run` resolves but installs nothing.
set -e
git config --global --add safe.directory '*'
cd /tmp && git clone -q /src llm-agent-google-adk && cd llm-agent-google-adk
echo '$ command -v python3; python3 --version'; command -v python3; python3 --version
echo '$ uv python list --only-installed'; uv python list --only-installed
echo '$ uv sync --dry-run 2>&1 | head -4'; uv sync --dry-run 2>&1 | head -4
echo '$ uv python install 3.15'; uv python install 3.15 2>&1 | tail -2
echo '$ uv python list --only-installed'; uv python list --only-installed
echo '$ uv sync --dry-run 2>&1 | grep -v "^ +" | head -6'; uv sync --dry-run 2>&1 | grep -v '^ +' | head -6 || true
