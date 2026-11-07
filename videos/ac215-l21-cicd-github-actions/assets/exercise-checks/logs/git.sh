#!/bin/bash
# Runs inside l21ex/laptop:check (laptop-check.Dockerfile) as user student, network through the
# session proxy (pre-commit downloads its hook environments), with /dlops/cheese-app-ci-cd = the read-only clone of
# dlops-io/cheese-app-ci-cd. A bare repository ~/fork.git that already holds b8458ff stands in for
# a fork on GitHub (nothing here can push to GitHub). Nothing from the repository runs except the
# pre-commit hooks its config pins (pre-commit-hooks v4.5.0, Black 24.1.1, Flake8 7.0.0).
step() { printf '$ %s\n' "$1"; bash -c "$1" 2>&1; printf '[exit %s]\n\n' "$?"; }
cd ~
echo "## setup: a clone at b8458ff whose origin is a stand-in fork that already has b8458ff"
step 'git config --global --add safe.directory /dlops/cheese-app-ci-cd/.git && git clone -q /dlops/cheese-app-ci-cd cheese-app-ci-cd && cd cheese-app-ci-cd && git reset -q --hard b8458ff && git init -q --bare ~/fork.git && git push -q ~/fork.git HEAD:refs/heads/main && git remote set-url origin ~/fork.git && git fetch -q origin && git branch -q -u origin/main && git log -1 --format="%h %s"'
cd ~/cheese-app-ci-cd || exit 1
echo "## C3: README Part 5 'Push to GitHub' on a fork"
step 'git add .'
step 'git commit -m "Add CI pipeline"'
step 'git push'
step 'git commit --allow-empty -m "Trigger CI" && git push 2>&1 | tail -1'
echo "## C4: the hook stops a commit; what happens if you just commit again"
step 'pip install -q pre-commit==4.7.0 2>&1 | tail -1; pre-commit install'
step 'sed -i "s/z = power(x, 2) + power(y, 2)/z=power(x,2)+power(y,2)/" src/api-service/api/service.py && git add . && git commit -m "quick fix" 2>&1 | grep -E "Black|Flake8|reformatted|\[INFO\] Installing|^\[main" ; git status --short'
step 'git commit -m "quick fix"; echo "exit code: $?"; git status --short'
step 'git diff --stat; git add . && git commit -m "quick fix" | grep -vE "no files to check"; echo "exit code: ${PIPESTATUS[0]}"; git status --short; git log -1 --format="%h %s"'
echo "## Ponder 5 / D1: a private key file (placeholder content), with and without the hooks"
step 'printf -- "-----BEGIN RSA PRIVATE KEY-----\nplaceholder, not a key\n-----END RSA PRIVATE KEY-----\n" > id_rsa && git add id_rsa && git commit -m "add key" | grep -E "private|id_rsa"; echo "exit code: ${PIPESTATUS[0]}"'
step 'git commit --no-verify -m "add key" && git status --short'
step 'grep -n "api/" /dlops-src-ci.yml | grep -E "black|flake8"'
step 'pre-commit run --all-files | grep -E "Detect private|id_rsa"; echo "exit code: ${PIPESTATUS[0]}"'
