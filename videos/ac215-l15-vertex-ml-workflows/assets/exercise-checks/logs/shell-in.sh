# Shell checks (C4, C5, C7), run inside debian:12 (sh = dash, as on Ubuntu/Debian) with --network
# none. /src = ml-workflow-aws/src read-only (assets/source/). `aws` and `docker` are stand-in scripts
# on PATH that only print what they were asked: nothing is built, nothing calls AWS.
. /checks/lib.sh
mkdir -p /tmp/bin
printf '#!/bin/sh\n# stand-in: "aws configure get <key>" with nothing configured prints nothing\nexit 0\n' > /tmp/bin/aws
printf '#!/bin/sh\necho "[stand-in docker] docker $*"\n' > /tmp/bin/docker
chmod +x /tmp/bin/aws /tmp/bin/docker
export PATH=/tmp/bin:$PATH
step 'ls -l /bin/sh; bash --version | head -1'
# C7: the collector's docker-shell.sh with no keys configured, as the README runs it (sh) and with bash
step 'cd /src/data-collector && sh docker-shell.sh; echo "exit status: $?"'
step 'cd /src/data-collector && bash docker-shell.sh; echo "exit status: $?"'
# C4: README B:169 pasted whole; a failed account lookup; || true
step 'bash -c '"'"'export REGION=us-east-1 [YOUR DEVELOPMENT REGION]; echo "export exit status: $?"; echo "REGION=$REGION"'"'"''
step 'bash -c '"'"'ACCOUNT_ID=$(false); REGION=us-east-1; REPO=cheese-app-data-collector; TAG=latest; ECR_URI="$ACCOUNT_ID.dkr.ecr.$REGION.amazonaws.com/$REPO:$TAG"; echo "ECR URI: $ECR_URI"'"'"''
step 'bash -c '"'"'false || true; echo "exit status after || true: $?"'"'"''
# C5: README A:161 typed as written (echo stands in for aws: the shell fails before any program runs)
step 'bash -c '"'"'echo delete-endpoint --endpoint-name <your-endpoint-name>'"'"'; echo "exit status: $?"'
