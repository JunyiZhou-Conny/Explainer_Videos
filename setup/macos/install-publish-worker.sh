#!/bin/bash
# Install (or remove) the two launchd jobs that publish released episodes to Bilibili from this Mac.
#
#   com.explainer.publish-worker  every 15 min   python3 tools/publish_worker.py --repo <repo> --upload
#   com.explainer.biliup-renew    Mondays 09:07  biliup renew   (keeps the Bilibili login alive)
#
# Both run in ~/.config/biliup, where biliup keeps its login (cookies.json, never in git). Run once
# from the repository checkout; it logs in to Bilibili and GitHub first if needed:
#
#   bash setup/macos/install-publish-worker.sh               # install or update
#   bash setup/macos/install-publish-worker.sh --uninstall   # remove both jobs
#
# Logs: ~/Library/Logs/explainer-publish.log and ~/Library/Logs/explainer-biliup-renew.log.
# Prerequisites: python3, gh (brew install gh) and biliup (npm install -g @biliup/cli).
set -euo pipefail

REPO_SLUG="${REPO_SLUG:-JunyiZhou-Conny/Explainer_Videos}"
AGENTS="$HOME/Library/LaunchAgents"
COOKIES_DIR="$HOME/.config/biliup"
LOGS="$HOME/Library/Logs"
WORKER_LABEL=com.explainer.publish-worker
RENEW_LABEL=com.explainer.biliup-renew
DOMAIN="gui/$(id -u)"

unload() {   # ignore "not loaded"
    launchctl bootout "$DOMAIN/$1" 2>/dev/null || true
}

if [ "${1:-}" = "--uninstall" ]; then
    for label in "$WORKER_LABEL" "$RENEW_LABEL"; do
        unload "$label"
        rm -f "$AGENTS/$label.plist"
    done
    echo "Removed $WORKER_LABEL and $RENEW_LABEL. The Bilibili login in $COOKIES_DIR is kept."
    exit 0
fi

[ "$(uname)" = Darwin ] || { echo "This installs macOS launchd jobs; run it on the Mac." >&2; exit 1; }
REPO_DIR="$(cd "$(dirname "$0")/../.." && pwd)"
[ -f "$REPO_DIR/tools/publish_worker.py" ] || { echo "Run this from the Explainer_Videos checkout." >&2; exit 1; }

need() {
    command -v "$1" >/dev/null 2>&1 || { echo "Missing '$1'. $2" >&2; exit 1; }
}
need python3 "Install Python 3 (python.org or brew install python)."
need gh "Install the GitHub CLI: brew install gh"
need biliup "Install biliup: npm install -g @biliup/cli"
PYTHON="$(command -v python3)"; GH="$(command -v gh)"; BILIUP="$(command -v biliup)"

gh auth status >/dev/null 2>&1 || { echo "Logging in to GitHub (needed to read releases and comment on issues)..."; "$GH" auth login; }

mkdir -p "$COOKIES_DIR" "$AGENTS" "$LOGS"
chmod 700 "$COOKIES_DIR"
if [ ! -s "$COOKIES_DIR/cookies.json" ]; then
    echo "Logging in to Bilibili: scan the QR code with the Bilibili app."
    (cd "$COOKIES_DIR" && "$BILIUP" login)
fi
[ -s "$COOKIES_DIR/cookies.json" ] || { echo "No $COOKIES_DIR/cookies.json after login; run 'biliup login' there and retry." >&2; exit 1; }
chmod 600 "$COOKIES_DIR/cookies.json"

# launchd starts jobs with a bare PATH; give them the directories these tools live in.
JOB_PATH="$(dirname "$PYTHON"):$(dirname "$GH"):$(dirname "$BILIUP"):/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin"

write_plist() {   # label, schedule XML, log name, program arguments (one <string> per argument)
    local label="$1" schedule="$2" log="$3"; shift 3
    local args="" a
    for a in "$@"; do
        a="${a//&/&amp;}"; a="${a//</&lt;}"; a="${a//>/&gt;}"
        args+="        <string>$a</string>"$'\n'
    done
    cat > "$AGENTS/$label.plist" <<PLIST
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>$label</string>
    <key>ProgramArguments</key>
    <array>
$args    </array>
    <key>WorkingDirectory</key>
    <string>$COOKIES_DIR</string>
    <key>EnvironmentVariables</key>
    <dict>
        <key>PATH</key>
        <string>$JOB_PATH</string>
    </dict>
$schedule
    <key>StandardOutPath</key>
    <string>$LOGS/$log</string>
    <key>StandardErrorPath</key>
    <string>$LOGS/$log</string>
</dict>
</plist>
PLIST
    plutil -lint "$AGENTS/$label.plist" >/dev/null
    unload "$label"
    launchctl bootstrap "$DOMAIN" "$AGENTS/$label.plist"
}

write_plist "$WORKER_LABEL" "    <key>StartInterval</key>
    <integer>900</integer>
    <key>RunAtLoad</key>
    <true/>" explainer-publish.log \
    "$PYTHON" "$REPO_DIR/tools/publish_worker.py" --repo "$REPO_SLUG" --upload

write_plist "$RENEW_LABEL" "    <key>StartCalendarInterval</key>
    <dict>
        <key>Weekday</key>
        <integer>1</integer>
        <key>Hour</key>
        <integer>9</integer>
        <key>Minute</key>
        <integer>7</integer>
    </dict>" explainer-biliup-renew.log \
    "$BILIUP" renew

echo "Installed. The worker runs now and every 15 minutes; biliup renews its login on Mondays."
echo "Watch it:  tail -f $LOGS/explainer-publish.log"
echo "Run now:   launchctl kickstart $DOMAIN/$WORKER_LABEL"
echo "Remove:    bash setup/macos/install-publish-worker.sh --uninstall"
