# Pulumi checks (B5, B6, B7, C7, C8, C9, Q2-Q5): the Pulumi CLI v3.274.0 on its local file backend
# (`pulumi login --local`, as the video's extra b30 did) inside l20ex-pulumi (see pulumi-setup.sh), with
# the empty passphrase of the toolbox (Dockerfile:51). The two exercise projects in pulumi-projects/ stand
# in for deploy_images and deploy_single_vm; no cloud provider, no Google call, nothing billable.
# Each "$ ..." line below is the command run inside l20ex-pulumi (via docker exec), unless it starts
# with "host:", which is the host's Docker CLI acting on the stand-ins (the "VM"). Before Q5 the host puts
# back the marker file that B7 deleted, so the destroy shows what happens to a command's effects.
LOGS=$(cd "$(dirname "$0")" && pwd)
p() { printf '$ %s\n' "$1"; docker exec -w "${2:-/work}" l20ex-pulumi bash -c "$1" 2>&1 | sed -E 's/\x1b\[[0-9;]*m//g'; printf '[exit %s]\n\n' "${PIPESTATUS[0]}"; }
h() { printf '$ host: %s\n' "$1"; sh -c "$1" 2>&1; printf '[exit %s]\n\n' "$?"; }
I=/work/l20ex-images; V=/work/l20ex-vm

echo '## login and stacks'
p "pulumi login --local"
p "pulumi stack init dev" $V
echo '## C8: the VM stack before the images stack exists'
p "pulumi preview --stack dev" $V
p "pulumi stack init dev" $I
p "pulumi stack init dev" $I
p "pulumi stack select dev && pulumi stack ls" $I
echo '## B5: up without -y in a non-interactive session, then with -y'
p "pulumi up --stack dev" $I
p "pulumi up --stack dev -y" $I
echo '## B5 / Q2: the same up again, nothing changed in the code'
p "pulumi preview --stack dev --refresh" $I
p "pulumi up --stack dev --refresh -y" $I
echo '## D2: a tag that only changes with the code'
p "pulumi config set fixed_tag 3ecef56 && pulumi up --stack dev -y >/dev/null && pulumi preview --stack dev --refresh" $I
p "pulumi config rm fixed_tag && pulumi up --stack dev -y >/dev/null && pulumi stack output --stack dev" $I
echo '## B6: the VM stand-in: the container through the Docker provider, a remote.Command over SSH'
p "pulumi up --stack dev --refresh -y" $V
h "docker ps --filter name=l20ex-web --format '{{.Names}}  {{.Image}}  {{.Status}}  {{.Ports}}'; docker inspect -f '{{index .Config.Labels \"image-tag\"}}' l20ex-web"
h "docker exec l20ex-sshd ls /home/student"
p "pulumi up --stack dev --refresh -y" $V
echo '## B6: a new images up (new timestamp), then the VM stack'
p "pulumi up --stack dev -y >/dev/null; pulumi stack output --stack dev" $I
p "pulumi preview --stack dev --refresh --diff 2>&1 | grep -E '^ *[-+~]|replace|image-tag|Resources|to (create|update|replace|delete)|unchanged'" $V
p "pulumi up --stack dev --refresh -y" $V
echo '## B7: drift: someone removes the container by hand'
h "docker rm -f l20ex-web"
p "pulumi preview --stack dev" $V
p "pulumi preview --stack dev --refresh" $V
p "pulumi up --stack dev --refresh -y" $V
echo '## B7 / Q4: drift a command cannot see'
h "docker exec l20ex-sshd rm /home/student/created-by-pulumi && docker exec l20ex-sshd ls -A /home/student | grep -c created || true"
p "pulumi preview --stack dev --refresh" $V
echo '## C9: a key with a passphrase'
p "pulumi config set try_passphrase_key true && pulumi up --stack dev -y" $V
p "pulumi config rm try_passphrase_key && pulumi up --stack dev -y >/dev/null; echo removed the flag" $V
echo '## C7: the exported ssh command without -i'
p "ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 12222 student@127.0.0.1 echo logged in"
p "ssh -o BatchMode=yes -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -p 12222 -i /work/keys/ssh-key-deployment student@127.0.0.1 echo logged in"
echo '## Q5: destroy, and what is left'
h "docker exec l20ex-sshd touch /home/student/created-by-pulumi && docker exec l20ex-sshd ls /home/student"
p "pulumi destroy --stack dev --refresh -y" $V
h "docker ps -a --filter name=l20ex-web --format '{{.Names}}' | wc -l; docker exec l20ex-sshd ls /home/student"
p "pulumi stack ls; pulumi stack output --stack dev" $V
p "pulumi destroy --stack dev -y" $I
p "pulumi stack ls --all" $I
p "pulumi stack rm dev -y" $V
p "pulumi stack ls --all" $I
