# check-only, NOT a tutorial file: a stand-in "laptop" for the git, pre-commit and workflow-lint
# checks. The CA-patched base (py311-ca-check.Dockerfile) + git, pre-commit 4.7.0 (the captures'
# version) and actionlint (from PyPI's actionlint-py wheel, which bundles the binary), user student.
FROM l21ex/py311-ca:check
RUN apt-get update -q && apt-get install -y -q --no-install-recommends git >/dev/null \
 && rm -rf /var/lib/apt/lists/* \
 && pip install -q --no-cache-dir pre-commit==4.7.0 actionlint-py PyYAML \
 && useradd -m -u 1000 student
USER student
RUN git config --global user.name student && git config --global user.email student@laptop \
 && git config --global init.defaultBranch main && git config --global advice.detachedHead false
WORKDIR /home/student
