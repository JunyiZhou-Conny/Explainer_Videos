# Check-only image (not the tutorial's toolbox): the toolbox's Ansible, ansible 6.7.0 /
# ansible-core 2.13.13 on Python 3.8 (laptop/32, 33), with boto3 for the AWS modules and
# openssh-client and openssh-server for the SSH checks (a stand-in server on 127.0.0.1, user
# `ubuntu`, inside the same disposable container). The session proxy's CA is added so pip and apt can download
# through the sandbox's TLS-intercepting proxy; it plays no part in any check.
FROM mirror.gcr.io/library/python:3.8-slim
COPY ca.crt /usr/local/share/ca-certificates/session-proxy.crt
ENV SSL_CERT_FILE=/usr/local/share/ca-certificates/session-proxy.crt \
    PIP_CERT=/usr/local/share/ca-certificates/session-proxy.crt \
    PIP_DISABLE_PIP_VERSION_CHECK=1 PIP_ROOT_USER_ACTION=ignore PIP_NO_CACHE_DIR=1
RUN sed -i 's|http://deb.debian.org|https://deb.debian.org|g' /etc/apt/sources.list.d/debian.sources && \
    apt-get -o Acquire::https::CAInfo=/usr/local/share/ca-certificates/session-proxy.crt update -qq && \
    apt-get -o Acquire::https::CAInfo=/usr/local/share/ca-certificates/session-proxy.crt install -y -qq --no-install-recommends openssh-client openssh-server >/dev/null && \
    rm -rf /var/lib/apt/lists/* && \
    useradd -m -s /bin/bash ubuntu && mkdir -p /run/sshd
RUN pip install -q "ansible==6.7.0" boto3 botocore
