#!/bin/bash
# Inside ubuntu:24.04 (--network none). Lays out the README's folders (README:54-60): a copy of the
# repo at /home/student/cheese-app-aws and /home/student/secrets beside it, with a placeholder CSV
# (AWS's header, obviously fake values). `docker` is a stand-in script that prints its arguments
# (and fails a build when STUB_BUILD_RC is set), so docker-shell.sh can run to its end here.
. /checks/lib.sh
H=/home/student; mkdir -p $H/secrets /tmp/bin
cp -r /src $H/cheese-app-aws
printf 'Access key ID,Secret access key\r\nPLACEHOLDER_NOT_A_REAL_ACCESS_KEY,PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000\r\n' \
  > $H/secrets/deployment-ac215-user_accessKeys.csv
cat > /tmp/bin/docker <<'STUB'
#!/bin/sh
echo "[stand-in docker] docker $*"
if [ "$1" = build ] && [ -n "$STUB_BUILD_RC" ]; then echo "[stand-in docker] build failed"; exit "$STUB_BUILD_RC"; fi
exit 0
STUB
chmod +x /tmp/bin/docker; export PATH=/tmp/bin:$PATH HOME=$H
cd $H/cheese-app-aws/src/deployment
# README:76's edit (three ../), as the video makes it (laptop/22)
sed -i 's|^CSV_FILE=.*|CSV_FILE="../../../secrets/deployment-ac215-user_accessKeys.csv"|' docker-shell.sh

step 'ls -l /bin/sh; bash --version | head -1'
# Q2: the README's line, then bash
step 'cd /home/student/cheese-app-aws/src/deployment && sh docker-shell.sh; echo "exit status: $?"'
step 'cd /home/student/cheese-app-aws/src/deployment && bash docker-shell.sh; echo "exit status: $?"'
# Q2: the here-string in dash, in bash, and in bash's POSIX mode (what macOS /bin/sh runs)
step "dash -c 'IFS=, read -r a b <<< \"key,secret\"; echo \"a=\$a b=\$b\"'; echo \"exit status: \$?\""
step "bash --posix -c 'IFS=, read -r a b <<< \"key,secret\"; echo \"a=\$a b=\$b\"'; echo \"exit status: \$?\""
# C1: the script started from the repository root instead of src/deployment
step 'cd /home/student/cheese-app-aws && bash src/deployment/docker-shell.sh; echo "exit status: $?"'
# B4: a build that fails, without and with set -e (docker-shell.sh:4 uncommented in a copy)
step 'cd /home/student/cheese-app-aws/src/deployment && STUB_BUILD_RC=1 bash docker-shell.sh; echo "exit status: $?"'
step 'cd /home/student/cheese-app-aws/src/deployment && sed "4s/^#set -e/set -e/" docker-shell.sh > docker-shell-sete.sh && sed -n 4p docker-shell-sete.sh && STUB_BUILD_RC=1 bash docker-shell-sete.sh; echo "exit status: $?"'
# Q2/B1: what the unquoted >= in Dockerfile:37 does to a shell (echo stands in for pip)
step 'mkdir -p /tmp/redirect && cd /tmp/redirect && echo pip install ansible>=9.0.0 openshift docker; ls -l; echo "file holds: $(cat =9.0.0)"'
step 'mkdir -p /tmp/quoted && cd /tmp/quoted && echo pip install "ansible>=9.0.0" openshift docker; ls -l'
