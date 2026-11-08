#!/bin/bash
# Inside l23ex-ansible:check (ansible 6.7.0 / core 2.13.13, Python 3.8, as in the toolbox), --network none.
# /w is a copy of src/deployment at 5950118. Placeholder AWS values only. Every Ansible command's output
# is filtered of the two-line CryptographyDeprecationWarning (Python 3.8), as in the video.
. /checks/lib.sh
cp -r /src /w && cd /w
export AWS_ACCESS_KEY_ID=PLACEHOLDER_NOT_A_REAL_ACCESS_KEY AWS_SECRET_ACCESS_KEY=PLACEHOLDER_NOT_A_REAL_SECRET_KEY_000000000000
export AWS_DEFAULT_REGION=us-east-1 AWS_ACCOUNT_ID=YOUR_ACCOUNT_ID
F='2>&1 | grep -v -e CryptographyDeprecationWarning -e "from cryptography.exceptions import InvalidSignature"'
# README:97's edit as laptop/43 makes it: the placeholder host name EXTERNAL_IP; here it resolves to
# 127.0.0.1, where a stand-in SSH server (user ubuntu) runs inside this container.
sed -i 's|^        <EXTERNAL_IP>:|        EXTERNAL_IP:|' inventory.yml
echo "127.0.0.1 EXTERNAL_IP" >> /etc/hosts

echo "=== B2, Q4: which tag does the server use? (the playbook's own lines 101-118) ==="
# exactly the commands exercises.md B2 gives (run in /w, a copy of src/deployment = the toolbox's /app)
step "cd /w && { printf -- '- hosts: localhost\\n  connection: local\\n  gather_facts: false\\n  tasks:\\n'; sed -n '101,118p' deploy-setup-containers.yml; } > tagbook.yml && cat .docker-tag && sed -n '1,5p;12,22p' tagbook.yml"
step "cd /w && env -u DOCKER_TAG ansible-playbook tagbook.yml $F | grep -E 'TASK|skipping|ok:|msg'"
step "cd /w && DOCKER_TAG=20261108011909 ansible-playbook tagbook.yml $F | grep -E 'TASK|skipping|ok:|msg'"
step "cd /w && DOCKER_TAG=20261108011909 ansible-playbook tagbook.yml --extra-vars docker_tag=20261108020000 $F | grep -E 'TASK|skipping|ok:|msg'"

echo "=== Q2: the provision playbook's 'warn:' (lines 54-57) on this Ansible ==="
python3 /checks/edit.py warnbook > /dev/null
step "cd /w && ansible-playbook warnbook.yml $F | grep -E 'TASK|changed:|ok:|fatal|WARN|warn'"

echo "=== C3, C6: which key does SSH get? (stand-in server on 127.0.0.1, user ubuntu) ==="
mkdir -p /secrets /root/.ssh /home/ubuntu/.ssh
ssh-keygen -q -t rsa -b 2048 -N '' -C throwaway-for-checks -f /secrets/ac215_2024.pem   # never printed
mv /secrets/ac215_2024.pem.pub /home/ubuntu/.ssh/authorized_keys   # AWS hands you only the .pem
chown -R ubuntu:ubuntu /home/ubuntu/.ssh; chmod 700 /home/ubuntu/.ssh; chmod 600 /home/ubuntu/.ssh/authorized_keys
ssh-keygen -q -A; /usr/sbin/sshd -o ListenAddress=127.0.0.1
python3 /checks/edit.py toggle > /dev/null
# Ansible's default ControlPersist would reuse the first good connection for 60 s and skip the key
# check in the runs after it: every SSH check opens a fresh connection instead.
export ANSIBLE_SSH_ARGS="-C -o ControlMaster=no"
step "cd /w && sed -n '4p;7p' inventory.yml && ls /root/.ssh/ && ansible appserver -i inventory.yml -m ping $F"
step "cd /w && sed -n '4p;7p' inventory-local.yml && ls -l /secrets/ac215_2024.pem | cut -c1-10 && ansible appserver -i inventory-local.yml -m ping $F"
step "cd /w && chmod 644 /secrets/ac215_2024.pem && ansible appserver -i inventory-local.yml -m ping $F; chmod 600 /secrets/ac215_2024.pem"
step "cd /w && env -u AWS_SSH_KEY ansible appserver -i inventory-local.yml -m debug -a var=ansible_ssh_private_key_file -e ansible_connection=local $F"
# The CI toolbox (ci_cd_aws.yml:113-131): the key is mounted at /root/.ssh, /secrets does not exist,
# and AWS_SSH_KEY is not among the -e flags. Same inventory with line 7 still active (step 9 not undone):
step "cd /w && mv /secrets /secrets.off && cp /secrets.off/ac215_2024.pem /root/.ssh/ && chmod 600 /root/.ssh/ac215_2024.pem && ansible appserver -i inventory-local.yml -m ping $F"
step "cd /w && ansible appserver -i inventory.yml -m ping $F; mv /secrets.off /secrets"

echo "=== Ponder 5, B5: the README's delete, then two edits ==="
step "cd /w && ansible-playbook deploy-create-instance.yml -i inventory.yml --extra-vars cluster_state=absent $F | grep -E 'TASK|skipping|ok:|fatal|RECAP|localhost +:' | cut -c1-200"
python3 /checks/edit.py gate > /dev/null
step "cd /w && sed -n '59,63p' create-gated.yml && ansible-playbook create-gated.yml -i inventory.yml --extra-vars cluster_state=absent $F | grep -E 'TASK|skipping|ok:|fatal|localhost +:' | cut -c1-200"
python3 /checks/edit.py fixed > /dev/null
step "cd /w && ansible-playbook create-fixed.yml -i inventory.yml --syntax-check $F; ansible-playbook create-fixed.yml -i inventory.yml --list-tasks $F | grep -vE '^$'"
step "cd /w && ansible-playbook create-fixed.yml -i inventory.yml --extra-vars cluster_state=absent $F | grep -E 'TASK|skipping|ok:|fatal|localhost +:' | sed -E 's/(fatal: \\[localhost\\]: FAILED!).*(botocore.exceptions.[A-Za-z]+: [^\\\"]*).*/\\1 ... \\2/'"
# does ec2_vol's name: become the Name tag the lookup uses? (amazon.aws 3.5.0, the toolbox's version)
step "f=\$(python3 -c 'import ansible_collections.amazon.aws.plugins.modules.ec2_vol as m; print(m.__file__)'); grep -n \"Name\" \$f | grep -iE \"tag|name'\" | head -5"
