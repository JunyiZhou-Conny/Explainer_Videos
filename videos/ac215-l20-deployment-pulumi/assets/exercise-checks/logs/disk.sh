# B4: the format step of provision_instance.py:29, run twice, against a 64 MB image file standing in for
# /dev/disk/by-id/google-persistent-disk-1 (no device, no mount, no privileges: debugfs reads and writes
# the ext4 image directly). In debian:12 (e2fsprogs 1.47.0), --network none.
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
SRC=$(cd "$LOGS/../../source" && pwd)
step "sed -n 29p $SRC/src/deployment/deploy_single_vm/provision_instance.py"
step "docker run --rm --network none -v $LOGS/disk-inner.sh:/disk-inner.sh:ro debian:12 bash /disk-inner.sh"
