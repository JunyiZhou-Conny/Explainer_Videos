# Runs inside debian:12 (see disk.sh). DISK stands in for the VM's second disk.
. /dev/stdin <<'LIB'
step() { printf '$ %s\n' "$1"; sh -c "$1" 2>&1; printf '[exit %s]\n\n' "$?"; }
LIB
cd /tmp
step "truncate -s 64M disk.img && echo 'a blank 64 MB disk image'"
GUARD="blkid -o value -s TYPE disk.img || mkfs.ext4 -q disk.img"
echo '## first run: no filesystem yet'
step "$GUARD"
step "blkid -o value -s TYPE disk.img"
echo '## the app writes data (a chat history file, written with debugfs)'
step "echo 'chat history' > history.txt && debugfs -w -R 'write history.txt history.txt' disk.img && debugfs -R 'ls -l' disk.img 2>/dev/null | grep history"
echo '## second run of the guarded command (a new trigger, a replaced resource...)'
step "$GUARD"
step "debugfs -R 'cat history.txt' disk.img"
echo '## the same second run without the guard (no terminal, as over a Pulumi SSH session)'
step "mkfs.ext4 disk.img < /dev/null"
step "debugfs -R 'cat history.txt' disk.img"
