# Setup for pulumi.sh (disposable; nothing from the tutorial repo runs here):
# - l20ex-pulumi: python:3.13-slim-bookworm with the Pulumi CLI v3.274.0 (the toolbox's version, laptop/b04)
#   and the Python SDKs pulumi, pulumi-command 1.1.3, pulumi-docker 4.9.0 (the plugin versions of laptop/b34).
#   Host network (only to reach the session proxy for the downloads; NO_PROXY keeps the CLI and its plugins, which talk gRPC on 127.0.0.1, off it), the session proxy's CA, and the host's
#   Docker socket (the Docker provider creates one container, l20ex-web). The exercise projects are copied in.
# - l20ex-sshd: debian:12 with openssh-server, user student, key-only login, on 127.0.0.1:12222 (host network). It stands
#   in for the VM's SSH door. Its keys are generated in /work/keys at setup and never leave the containers.
. "$(dirname "$0")/lib.sh"
LOGS=$(cd "$(dirname "$0")" && pwd)
step "docker run -d --name l20ex-pulumi --network host -e HTTPS_PROXY=\$HTTPS_PROXY -e https_proxy=\$HTTPS_PROXY -e NO_PROXY=localhost,127.0.0.1 -e no_proxy=localhost,127.0.0.1 -e SSL_CERT_FILE=/ca.crt -e PIP_CERT=/ca.crt -e PULUMI_CONFIG_PASSPHRASE= -e PULUMI_SKIP_UPDATE_CHECK=true -v /root/.ccr/ca-bundle.crt:/ca.crt:ro -v /var/run/docker.sock:/var/run/docker.sock python:3.13-slim-bookworm sleep infinity >/dev/null && echo started l20ex-pulumi"
step "docker exec l20ex-pulumi sh -c 'python - <<PY
import urllib.request, tarfile, io
u = \"https://get.pulumi.com/releases/sdk/pulumi-v3.274.0-linux-x64.tar.gz\"
tarfile.open(fileobj=io.BytesIO(urllib.request.urlopen(u).read())).extractall(\"/opt\")
PY
ln -s /opt/pulumi/pulumi /usr/local/bin/pulumi && pulumi version'"
step "docker exec l20ex-pulumi sh -c 'pip install -q --root-user-action=ignore pulumi pulumi-command==1.1.3 pulumi-docker==4.9.0 2>&1 | tail -2; pip list 2>/dev/null | grep -i pulumi'"
step "docker exec l20ex-pulumi sh -c 'apt-get -qq update >/dev/null 2>&1; apt-get -qq install -y openssh-client >/dev/null 2>&1; ssh -V'"
step "docker cp $LOGS/pulumi-projects l20ex-pulumi:/work && docker exec l20ex-pulumi sh -c 'mkdir -p /work/keys && ls /work'"
step "docker exec l20ex-pulumi sh -c 'cd /work/keys && ssh-keygen -q -t rsa -N \"\" -f ssh-key-deployment && ssh-keygen -q -t rsa -N not-empty -f ssh-key-with-passphrase && ls'"
docker exec l20ex-pulumi cat /work/keys/ssh-key-deployment.pub > /dev/null
step "docker run -d --name l20ex-sshd --network host debian:12 sleep infinity >/dev/null && echo started l20ex-sshd"
step "docker exec l20ex-sshd sh -c 'apt-get -qq update >/dev/null 2>&1; apt-get -qq install -y openssh-server >/dev/null 2>&1; useradd -m -s /bin/bash student && mkdir -p /home/student/.ssh /run/sshd && chmod 755 /run/sshd && echo user student'"
docker exec l20ex-pulumi sh -c 'cat /work/keys/ssh-key-deployment.pub /work/keys/ssh-key-with-passphrase.pub' | docker exec -i l20ex-sshd sh -c 'cat > /home/student/.ssh/authorized_keys; chown -R student /home/student/.ssh; chmod 700 /home/student/.ssh; chmod 600 /home/student/.ssh/authorized_keys'
step "docker exec l20ex-sshd sh -c '/usr/sbin/sshd -o Port=12222 -o ListenAddress=127.0.0.1 -o PasswordAuthentication=no && echo sshd up on 127.0.0.1:12222; wc -l < /home/student/.ssh/authorized_keys'"
